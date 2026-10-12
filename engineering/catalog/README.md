# Code and File Catalog

Generated: `2026-10-12T02:39:48.534700+00:00`
Indexed commit: `136ecedda4db8ce98bf8e6ffce82531261cbace6`

This catalog is generated from `git ls-files`. It provides structural metadata for every tracked file and extracted symbols for source files. It is an index, not a replacement for code review or runtime proof.

## Inventory counts

- `asset/other`: 380
- `build/deployment-script`: 245
- `configuration/data`: 553
- `documentation`: 962
- `engineering-index`: 7
- `schema-migration`: 379
- `source-code`: 5795
- `test-fixture`: 1360
- `tracked`: 9683

## Architectural layers

- **adapter** — 801 files
- **authentication** — 186 files
- **budgets-costs** — 42 files
- **chat-connectors** — 77 files
- **connectors** — 68 files
- **database** — 397 files
- **general** — 4540 files
- **github-integration** — 172 files
- **governance** — 32 files
- **heartbeat-execution** — 127 files
- **hermes-integration** — 70 files
- **mcp** — 197 files
- **observability** — 7 files
- **plugin** — 500 files
- **recovery** — 115 files
- **release** — 98 files
- **runner** — 1755 files
- **sandbox** — 215 files
- **skills** — 367 files
- **telemetry** — 34 files
- **testing** — 482 files
- **ui-storybook** — 401 files
- **workspace** — 277 files

## How to regenerate

```sh
python3 engineering/scripts/build_code_catalog.py
```

Machine-readable detail is in `engineering/catalog/FILE_CATALOG.json`. The catalog deliberately uses `confidence: automated-structural`; update `engineering/ARCHITECTURE.md` or a decision record when semantic interpretation is confirmed.
