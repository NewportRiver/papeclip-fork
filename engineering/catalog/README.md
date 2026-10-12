# Code and File Catalog

Generated: `2026-10-12T01:51:32.441404+00:00`
Indexed commit: `2ba6e64baf1f41b0c335299404387ceba77cf263`

This catalog is generated from `git ls-files`. It provides structural metadata for every tracked file and extracted symbols for source files. It is an index, not a replacement for code review or runtime proof.

## Inventory counts

- `asset/other`: 380
- `build/deployment-script`: 245
- `configuration/data`: 553
- `documentation`: 947
- `engineering-index`: 3
- `schema-migration`: 379
- `source-code`: 5795
- `test-fixture`: 1360
- `tracked`: 9664

## Architectural layers

- **adapter** — 800 files
- **authentication** — 185 files
- **budgets-costs** — 42 files
- **chat-connectors** — 77 files
- **connectors** — 68 files
- **database** — 396 files
- **general** — 4525 files
- **github-integration** — 172 files
- **governance** — 32 files
- **heartbeat-execution** — 127 files
- **hermes-integration** — 69 files
- **mcp** — 197 files
- **observability** — 7 files
- **plugin** — 499 files
- **recovery** — 114 files
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
