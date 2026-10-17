from __future__ import annotations

import hashlib
import json
import os
import re
import sqlite3
import uuid
import fcntl
from pathlib import Path
from typing import Any


class AuthorizationError(PermissionError):
    pass


class ValidationError(ValueError):
    pass


ROLE_PERMISSIONS = {
    "employee": {"search", "read", "propose", "write_ordinary"},
    "reviewer": {"search", "read", "propose", "write_ordinary", "review"},
    "publisher": {"search", "read", "propose", "write_ordinary", "review", "publish"},
    "admin": {"search", "read", "propose", "write_ordinary", "review", "publish", "backup"},
}

SENSITIVE_MARKERS = re.compile(
    r"(?:api[_ -]?key|password|private[_ -]?key|access[_ -]?token|refresh[_ -]?token|cvc|credential)\s*[:=]\s*(?!\[REDACTED\])[A-Za-z0-9_./+=-]{8,}|(?<![A-Za-z0-9])(?:sk|ghp|xoxb|ya29)-[A-Za-z0-9_-]{10,}",
    re.IGNORECASE,
)


class CorporateMemoryService:
    def __init__(self, db_path: str | Path, actor: str, role: str = "employee") -> None:
        if role not in ROLE_PERMISSIONS:
            raise AuthorizationError(f"unknown role: {role}")
        self.db_path = Path(db_path)
        self.db_path.parent.mkdir(parents=True, exist_ok=True)
        self.actor = actor
        self.role = role
        self.db = sqlite3.connect(self.db_path, timeout=10, isolation_level=None)
        self.db.row_factory = sqlite3.Row
        self.db.execute("PRAGMA foreign_keys=ON")
        self.db.execute("PRAGMA busy_timeout=10000")
        self.db.execute("PRAGMA journal_mode=WAL")
        self._migrate()

    def close(self) -> None:
        self.db.close()

    def _migrate(self) -> None:
        migrations_dir = Path(__file__).resolve().parents[2] / "migrations"
        migrations = sorted(migrations_dir.glob("*.sql"))
        lock_path = self.db_path.with_suffix(self.db_path.suffix + ".migration.lock")
        with lock_path.open("a+") as lock:
            fcntl.flock(lock.fileno(), fcntl.LOCK_EX)
            try:
                for migration in migrations:
                    version = int(migration.name.split("_", 1)[0])
                    migration_table_exists = self.db.execute(
                        "SELECT 1 FROM sqlite_master WHERE type='table' AND name='schema_migrations'"
                    ).fetchone()
                    already_applied = migration_table_exists and self.db.execute(
                        "SELECT 1 FROM schema_migrations WHERE version=?", (version,)
                    ).fetchone()
                    if already_applied:
                        continue
                    with self.db:
                        self.db.executescript(migration.read_text())
                        self.db.execute("INSERT OR IGNORE INTO schema_migrations(version) VALUES (?)", (version,))
            finally:
                fcntl.flock(lock.fileno(), fcntl.LOCK_UN)

    def _require(self, operation: str) -> None:
        if operation not in ROLE_PERMISSIONS[self.role]:
            self._audit(operation, None, "denied", f"role={self.role}")
            raise AuthorizationError(f"role {self.role} cannot {operation}")

    def _audit(self, operation: str, record_id: str | None, outcome: str, detail: str) -> None:
        self.db.execute(
            "INSERT INTO audit_log(actor, operation, record_id, outcome, detail) VALUES (?, ?, ?, ?, ?)",
            (self.actor, operation, record_id, outcome, detail),
        )

    @staticmethod
    def _validate_text(value: str, field: str) -> None:
        if not value or not value.strip():
            raise ValidationError(f"{field} must not be empty")
        if SENSITIVE_MARKERS.search(value):
            raise ValidationError(f"{field} contains a prohibited secret or private-memory marker")

    def propose(
        self,
        *,
        title: str,
        body: str,
        domain: str,
        scope: str,
        classification: str,
        owner: str,
        source: str,
        rationale: str,
        evidence_class: str = "observed",
    ) -> str:
        self._require("propose")
        for value, field in ((title, "title"), (body, "body"), (domain, "domain"), (owner, "owner"), (source, "source"), (rationale, "rationale")):
            self._validate_text(value, field)
        if scope not in {"Corporate", "Department", "Project"}:
            raise ValidationError("invalid scope")
        if classification not in {"Internal", "Confidential"}:
            raise ValidationError("invalid classification")
        if classification == "Confidential" and self.role == "employee":
            raise AuthorizationError("employees cannot propose Confidential records")
        record_id = f"NR-MEM-{uuid.uuid4().hex[:12].upper()}"
        proposal_id = f"NR-PROP-{uuid.uuid4().hex[:12].upper()}"
        content_hash = hashlib.sha256(body.encode()).hexdigest()
        with self.db:
            self.db.execute(
                "INSERT INTO knowledge_records(id, domain, scope, classification, owner, source, status, title, body, created_by) VALUES (?, ?, ?, ?, ?, ?, 'Proposed', ?, ?, ?)",
                (record_id, domain, scope, classification, owner, source, title, body, self.actor),
            )
            self.db.execute(
                "INSERT INTO revisions(record_id, version, title, body, changed_by) VALUES (?, 1, ?, ?, ?)",
                (record_id, title, body, self.actor),
            )
            self.db.execute(
                "INSERT INTO evidence(id, record_id, evidence_class, source_path, content_hash) VALUES (?, ?, ?, ?, ?)",
                (f"NR-EVD-{uuid.uuid4().hex[:12].upper()}", record_id, evidence_class, source, content_hash),
            )
            self.db.execute(
                "INSERT INTO knowledge_proposals(id, record_id, proposer, rationale, status) VALUES (?, ?, ?, ?, 'Pending')",
                (proposal_id, record_id, self.actor, rationale),
            )
            self._audit("propose", record_id, "allowed", f"proposal={proposal_id}")
        return proposal_id

    def search(self, query: str, limit: int = 20) -> list[dict[str, Any]]:
        self._require("search")
        self._validate_text(query, "query")
        terms = [term for term in re.findall(r"[\w-]+", query) if term]
        if not terms:
            raise ValidationError("query must contain searchable text")
        match_query = " AND ".join(f'"{term.replace(chr(34), chr(34) * 2)}"*' for term in terms)
        rows = self.db.execute(
            "SELECT k.id, k.domain, k.scope, k.classification, k.owner, k.source, k.status, k.title, k.body, k.version FROM knowledge_search s JOIN knowledge_records k ON k.id=s.record_id WHERE k.status='Approved' AND knowledge_search MATCH ? ORDER BY k.updated_at DESC LIMIT ?",
            (match_query, max(1, min(limit, 100))),
        ).fetchall()
        self._audit("search", None, "allowed", f"query={query[:80]}")
        return [dict(row) for row in rows]

    def write_ordinary(
        self,
        *,
        title: str,
        body: str,
        domain: str,
        owner: str,
        source: str,
        record_id: str | None = None,
    ) -> dict[str, Any]:
        """Create or revise ordinary internal knowledge without a review gate."""
        self._require("write_ordinary")
        for value, field in ((title, "title"), (body, "body"), (domain, "domain"), (owner, "owner"), (source, "source")):
            self._validate_text(value, field)
        if record_id is None:
            record_id = f"NR-MEM-{uuid.uuid4().hex[:12].upper()}"
            with self.db:
                self.db.execute(
                    "INSERT INTO knowledge_records(id, domain, scope, classification, owner, source, status, title, body, version, created_by, approved_by, approved_at) VALUES (?, ?, 'Corporate', 'Internal', ?, ?, 'Approved', ?, ?, 1, ?, ?, CURRENT_TIMESTAMP)",
                    (record_id, domain, owner, source, title, body, self.actor, self.actor),
                )
                self.db.execute("INSERT INTO revisions(record_id, version, title, body, changed_by) VALUES (?, 1, ?, ?, ?)", (record_id, title, body, self.actor))
                self._audit("write_ordinary", record_id, "allowed", "created")
            return {"record_id": record_id, "version": 1, "status": "Approved"}
        current = self.db.execute("SELECT version, status FROM knowledge_records WHERE id=?", (record_id,)).fetchone()
        if current is None:
            raise KeyError(record_id)
        if current["status"] != "Approved":
            raise AuthorizationError("ordinary writes cannot modify a pending or rejected record")
        version = current["version"] + 1
        with self.db:
            self.db.execute("UPDATE knowledge_records SET title=?, body=?, version=?, updated_at=CURRENT_TIMESTAMP WHERE id=?", (title, body, version, record_id))
            self.db.execute("INSERT INTO revisions(record_id, version, title, body, changed_by) VALUES (?, ?, ?, ?, ?)", (record_id, version, title, body, self.actor))
            self._audit("write_ordinary", record_id, "allowed", f"revised version={version}")
        return {"record_id": record_id, "version": version, "status": "Approved"}

    def read(self, record_id: str) -> dict[str, Any]:
        self._require("read")
        row = self.db.execute(
            "SELECT * FROM knowledge_records WHERE id=? AND status='Approved'", (record_id,)
        ).fetchone()
        if row is None:
            raise KeyError(record_id)
        self._audit("read", record_id, "allowed", "approved record")
        return dict(row)

    def review(self, proposal_id: str, decision: str, notes: str = "") -> dict[str, Any]:
        self._require("review")
        if decision not in {"approve", "reject"}:
            raise ValidationError("decision must be approve or reject")
        proposal = self.db.execute("SELECT * FROM knowledge_proposals WHERE id=?", (proposal_id,)).fetchone()
        if proposal is None or proposal["status"] != "Pending":
            raise KeyError(proposal_id)
        status = "Approved" if decision == "approve" else "Rejected"
        with self.db:
            self.db.execute("UPDATE knowledge_proposals SET status=?, reviewed_by=?, reviewed_at=CURRENT_TIMESTAMP WHERE id=?", (status, self.actor, proposal_id))
            self.db.execute("UPDATE knowledge_records SET status=?, approved_by=CASE WHEN ?='Approved' THEN ? ELSE NULL END, approved_at=CASE WHEN ?='Approved' THEN CURRENT_TIMESTAMP ELSE NULL END, updated_at=CURRENT_TIMESTAMP WHERE id=?", (status, status, self.actor, status, proposal["record_id"]))
            self._audit("review", proposal["record_id"], "allowed", f"proposal={proposal_id};decision={decision};notes={notes[:120]}")
        return {"proposal_id": proposal_id, "status": status, "record_id": proposal["record_id"]}

    def publish(self, proposal_id: str) -> dict[str, Any]:
        self._require("publish")
        row = self.db.execute("SELECT status, record_id FROM knowledge_proposals WHERE id=?", (proposal_id,)).fetchone()
        if row is None:
            raise KeyError(proposal_id)
        if row["status"] != "Approved":
            raise AuthorizationError("only approved proposals can be published")
        self._audit("publish", row["record_id"], "allowed", f"proposal={proposal_id}")
        return {"proposal_id": proposal_id, "record_id": row["record_id"], "status": "Published"}

    def backup(self, destination: str | Path) -> str:
        self._require("backup")
        destination = Path(destination)
        destination.parent.mkdir(parents=True, exist_ok=True)
        target = sqlite3.connect(destination)
        try:
            self.db.backup(target)
        finally:
            target.close()
        self._audit("backup", None, "allowed", str(destination))
        return str(destination)

    def health(self) -> dict[str, Any]:
        integrity = self.db.execute("PRAGMA integrity_check").fetchone()[0]
        version = self.db.execute("SELECT MAX(version) FROM schema_migrations").fetchone()[0]
        return {"ok": integrity == "ok", "integrity": integrity, "schema_version": version}


def token_roles() -> dict[str, tuple[str, str]]:
    raw = os.environ.get("CORPORATE_MEMORY_TOKENS_JSON", "")
    if not raw:
        return {}
    parsed = json.loads(raw)
    return {token: (value["actor"], value["role"]) for token, value in parsed.items()}
