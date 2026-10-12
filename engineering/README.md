# Paperclip Engineering Framework

This directory is the durable engineering memory and development log for the `NewportRiver/papeclip-fork` repository. It complements, rather than replaces, the upstream product and implementation contracts in `doc/`.

## Start here

1. `ENGINEERING_FUNDAMENTALS.md` — working principles and invariants.
2. `AGENTIC-UNDERSTANDING-ROADMAP.md` — layered knowledge, verification, and automation plan.
3. `PROJECT_MEMORY.md` — stable architecture and project facts.
4. `CURRENT_WORK.md` — restartable current state and next actions.
5. `SYSTEM_STATE.md` — source, runtime, persistence, recovery, and verification boundaries.
6. `ARCHITECTURE.md` — engineering map and data/control flow.
7. `TEST_STATUS.md` — verified and unverified checks.
8. `MASTER_MD_REGISTRY.md` — generated Markdown inventory.

## Development record

- `plan/AGENTIC-UNDERSTANDING-DEVELOPMENT-PLAN.md` — branch objective, milestones, and exit criteria.
- `plan/TASKS.md` — dependency-ordered executable task backlog.
- `manifests/` — bounded-domain manifests, contract-ID rules, configuration index, and security matrix.
- `scripts/check_catalog_freshness.py` — fails when generated catalogs do not match the current Git tree.
- `FEATURES.md` — capability inventory derived from product docs and code.
- `BUGLOG.md` — durable bug lessons and observed failure patterns.
- `DECISIONS.md` — architectural decisions and tradeoffs.
- `JOURNAL.md` — dated engineering history.
- `templates/` — templates for future entries.

## Update policy

Every material development change should update the smallest relevant record: a decision, feature, bug lesson, test status, journal entry, or current-work snapshot. Do not store credentials or raw session transcripts here. Generated/runtime output stays outside this durable framework unless it is intentionally summarized as evidence.

Indexes and reverse-engineering metadata live under `catalog/`:

- `catalog/FILE_CATALOG.json` — metadata for every tracked file.
- `catalog/FUNCTION_INDEX.md` — extracted source symbols and locations.
- `catalog/FILE_METADATA_SCHEMA.md` — schema, evidence levels, and method limits.

Coded retrieval markers live under `markers/`:

- `markers/MARKER_INDEX.json` — stable file/symbol markers and task mappings.
- `markers/TASK_MARKER_MAP.md` — human-readable task-to-code cross-reference.
- `markers/TASK_MARKERS.md` — stable task marker list.
- `markers/README.md` — marker types and query examples.

Refresh the Markdown registry with:

```sh
python3 engineering/scripts/refresh_md_registry.py
```

Regenerate the code catalog after source or tracked-file changes:

```sh
python3 engineering/scripts/build_code_catalog.py
```
