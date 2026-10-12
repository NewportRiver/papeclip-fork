# Configuration and Environment Index

Status: structural/static; runtime configuration has not been exercised because `pnpm` is unavailable in this Android environment.

## Primary configuration surfaces

| ID | Surface | Source | Notes |
|---|---|---|---|
| CFG-ROOT-PACKAGE | workspace scripts/dependencies | `package.json` | root package manager and workspace behavior |
| CFG-WORKSPACE | package boundaries | `pnpm-workspace.yaml` | workspace package discovery |
| CFG-ENV | documented environment | `.env.example` | sanitized variable surface; values must remain redacted |
| CFG-DOCKER | container deployment | `docker-compose.yml`, `doc/DOCKER.md` | service, database, ports, volumes |
| CFG-DEPLOYMENT | deployment modes | `doc/DEPLOYMENT-MODES.md` | trusted/private/public operational boundaries |
| CFG-DATABASE | persistence modes | `doc/DATABASE.md` | PostgreSQL, embedded, hosted, migrations |
| CFG-SERVER | server runtime | `server/package.json`, `server/src/` | API and control-plane configuration |
| CFG-CLI | operator CLI | `cli/` | commands and local administration |
| CFG-UI | operator UI | `ui/` | browser client and route/API usage |

## Indexing rules

- Record variable names and consuming source locations, never secret values.
- Distinguish required, optional, development-only, test-only, and deployment-only variables.
- Link every security-sensitive variable to its redaction and rotation procedure.
- Verify behavior at runtime before marking a variable operationally confirmed.
