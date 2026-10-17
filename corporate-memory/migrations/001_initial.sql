PRAGMA foreign_keys = ON;
PRAGMA journal_mode = WAL;

CREATE TABLE IF NOT EXISTS schema_migrations (
    version INTEGER PRIMARY KEY,
    applied_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS knowledge_records (
    id TEXT PRIMARY KEY,
    domain TEXT NOT NULL,
    scope TEXT NOT NULL CHECK (scope IN ('Corporate', 'Department', 'Project')),
    classification TEXT NOT NULL CHECK (classification IN ('Internal', 'Confidential')),
    owner TEXT NOT NULL,
    source TEXT NOT NULL,
    status TEXT NOT NULL CHECK (status IN ('Proposed', 'Approved', 'Rejected', 'Deprecated')),
    title TEXT NOT NULL,
    body TEXT NOT NULL,
    version INTEGER NOT NULL DEFAULT 1,
    created_by TEXT NOT NULL,
    created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
    approved_by TEXT,
    approved_at TEXT,
    CHECK (status != 'Approved' OR (approved_by IS NOT NULL AND approved_at IS NOT NULL))
);

CREATE TABLE IF NOT EXISTS organizational_records (
    id TEXT PRIMARY KEY,
    record_type TEXT NOT NULL,
    name TEXT NOT NULL,
    body TEXT NOT NULL,
    source TEXT NOT NULL,
    status TEXT NOT NULL DEFAULT 'Approved',
    created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS approved_decisions (
    id TEXT PRIMARY KEY,
    title TEXT NOT NULL,
    decision TEXT NOT NULL,
    authority TEXT NOT NULL,
    source TEXT NOT NULL,
    decided_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS projects (
    id TEXT PRIMARY KEY,
    name TEXT NOT NULL,
    description TEXT NOT NULL,
    owner TEXT NOT NULL,
    status TEXT NOT NULL,
    source TEXT NOT NULL,
    created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS personnel_references (
    id TEXT PRIMARY KEY,
    role TEXT NOT NULL,
    reference TEXT NOT NULL,
    source TEXT NOT NULL,
    classification TEXT NOT NULL DEFAULT 'Confidential',
    created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS evidence (
    id TEXT PRIMARY KEY,
    record_id TEXT NOT NULL REFERENCES knowledge_records(id),
    evidence_class TEXT NOT NULL,
    source_path TEXT NOT NULL,
    content_hash TEXT NOT NULL,
    captured_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS revisions (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    record_id TEXT NOT NULL REFERENCES knowledge_records(id),
    version INTEGER NOT NULL,
    title TEXT NOT NULL,
    body TEXT NOT NULL,
    changed_by TEXT NOT NULL,
    changed_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
    UNIQUE(record_id, version)
);

CREATE TABLE IF NOT EXISTS knowledge_proposals (
    id TEXT PRIMARY KEY,
    record_id TEXT NOT NULL REFERENCES knowledge_records(id),
    proposer TEXT NOT NULL,
    rationale TEXT NOT NULL,
    status TEXT NOT NULL CHECK (status IN ('Pending', 'Approved', 'Rejected')),
    created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
    reviewed_by TEXT,
    reviewed_at TEXT
);

CREATE TABLE IF NOT EXISTS audit_log (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    actor TEXT NOT NULL,
    operation TEXT NOT NULL,
    record_id TEXT,
    outcome TEXT NOT NULL,
    detail TEXT NOT NULL,
    created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE VIRTUAL TABLE IF NOT EXISTS knowledge_search USING fts5(
    record_id UNINDEXED,
    title,
    body,
    domain,
    content='knowledge_records',
    content_rowid='rowid'
);

CREATE INDEX IF NOT EXISTS idx_knowledge_status_scope ON knowledge_records(status, scope, classification);
CREATE INDEX IF NOT EXISTS idx_proposals_status ON knowledge_proposals(status);
CREATE INDEX IF NOT EXISTS idx_evidence_record ON evidence(record_id);
