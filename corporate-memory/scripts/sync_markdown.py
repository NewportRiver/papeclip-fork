#!/usr/bin/env python3
"""Synchronize approved Markdown manuals into shared corporate memory."""
from __future__ import annotations

import argparse
import sys
from pathlib import Path

from corporate_memory import CorporateMemoryService

ALLOWED_ROOTS = (
    Path("/home/architect/HERMES_SELF_IMPROVEMENT").resolve(),
    Path("/home/architect/HERMES_GEMINI_WORKSPACE/corporate-knowledge").resolve(),
)


def allowed(path: Path) -> bool:
    resolved = path.resolve()
    return any(resolved == root or root in resolved.parents for root in ALLOWED_ROOTS)


def sync_file(service: CorporateMemoryService, path: Path) -> dict[str, object]:
    path = path.resolve()
    if not allowed(path):
        raise ValueError(f"source is outside the approved manual roots: {path}")
    if path.suffix.lower() != ".md":
        raise ValueError(f"source must be Markdown: {path}")
    body = path.read_text(encoding="utf-8")
    source = str(path)
    existing = service.db.execute(
        "SELECT id, version FROM knowledge_records WHERE source=? ORDER BY updated_at DESC LIMIT 1",
        (source,),
    ).fetchone()
    if existing is None:
        return service.write_ordinary(
            title=path.stem.replace("_", " ").replace("-", " "),
            body=body,
            domain="Engineering Governance",
            owner="Technology Department",
            source=source,
        )
    return service.write_ordinary(
        record_id=existing["id"],
        title=path.stem.replace("_", " ").replace("-", " "),
        body=body,
        domain="Engineering Governance",
        owner="Technology Department",
        source=source,
    )


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("paths", nargs="+", type=Path)
    parser.add_argument("--db", default="/home/architect/.local/share/newport-river/corporate-memory.sqlite3")
    args = parser.parse_args()
    service = CorporateMemoryService(args.db, "sop-sync", "employee")
    try:
        for path in args.paths:
            print(path, sync_file(service, path))
    finally:
        service.close()
    return 0


if __name__ == "__main__":
    sys.exit(main())
