# Paperclip Engineering Framework

This directory is the durable engineering memory and development log for the `NewportRiver/papeclip-fork` repository. It complements, rather than replaces, the upstream product and implementation contracts in `doc/`.

## Start here

1. `ENGINEERING_FUNDAMENTALS.md` — working principles and invariants.
2. `PROJECT_MEMORY.md` — stable architecture and project facts.
3. `CURRENT_WORK.md` — restartable current state and next actions.
4. `SYSTEM_STATE.md` — source, runtime, persistence, recovery, and verification boundaries.
5. `ARCHITECTURE.md` — engineering map and data/control flow.
6. `TEST_STATUS.md` — verified and unverified checks.
7. `MASTER_MD_REGISTRY.md` — generated Markdown inventory.

## Development record

- `FEATURES.md` — capability inventory derived from product docs and code.
- `BUGLOG.md` — durable bug lessons and observed failure patterns.
- `DECISIONS.md` — architectural decisions and tradeoffs.
- `JOURNAL.md` — dated engineering history.
- `templates/` — templates for future entries.

## Update policy

Every material development change should update the smallest relevant record: a decision, feature, bug lesson, test status, journal entry, or current-work snapshot. Do not store credentials or raw session transcripts here. Generated/runtime output stays outside this durable framework unless it is intentionally summarized as evidence.

Refresh the Markdown registry with:

```sh
python3 engineering/scripts/refresh_md_registry.py
```
