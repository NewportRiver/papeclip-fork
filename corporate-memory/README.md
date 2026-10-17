# Newport River Corporate Memory

Standalone institutional memory service for approved corporate knowledge. It is intentionally separate from Hermes-01 and Gemini-02 personal memory directories.

## Boundaries

- SQLite is the structured retrieval layer; source Markdown and evidence remain canonical.
- Employee roles can search, read approved records, propose controlled knowledge, and create/revise ordinary Internal knowledge without a separate review gate.
- Reviewers can approve/reject proposals; publishers can publish approved proposals.
- Only admins can create backups through the service API.
- Secrets, credentials, OAuth state, private conversations, private memory, and personnel-sensitive content are rejected or kept outside this database.
- Scope (`Corporate`, `Department`, `Project`) and classification (`Internal`, `Confidential`) are stored on every knowledge record. Authorization is enforced by role, not by labels alone.

## Run

```bash
cd corporate-memory
export CORPORATE_MEMORY_DB=/var/lib/newport-river/corporate-memory.sqlite3
export CORPORATE_MEMORY_TOKENS_JSON='{"hermes-01":{"actor":"hermes-01","role":"employee"},"cto-review":{"actor":"cto","role":"reviewer"},"memory-admin":{"actor":"memory-admin","role":"admin"}}'
export CORPORATE_MEMORY_ACCESS_TOKEN=hermes-01
PYTHONPATH=src python -m corporate_memory.mcp_stdio
```

The MCP server implements `initialize`, `tools/list`, and `tools/call` over stdio. Tools are `search_knowledge`, `read_knowledge`, `write_ordinary_knowledge`, `propose_knowledge`, `review_knowledge`, `publish_knowledge`, and `memory_health`.

`write_ordinary_knowledge` is the low-friction write path. It is limited to ordinary Internal corporate knowledge and records the author, revision number, timestamp, and audit event. Organizational records, approved decisions, personnel references, credentials, financial commitments, and destructive production actions remain outside this path and require their existing governance controls.

## Verification

```bash
PYTHONPATH=src python -m pytest -q
```

## Backup

Use the admin `backup` operation or SQLite's online backup API. Keep the database outside the Git repository. Backups must be encrypted and access-controlled by deployment policy.

## Paperclip integration

Paperclip already provides a governed MCP tool gateway and supports MCP server connections. This service is intentionally exposed as a standalone stdio MCP server so Paperclip can register it as a connector without changing organizational assignments or governance. The integration test currently verifies the MCP protocol surface; deployment registration remains environment-specific.
