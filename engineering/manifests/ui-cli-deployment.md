# UI, CLI, and Deployment Domain Manifest

Evidence: repository-derived/structural. Runtime: blocked on Android until Node/pnpm/Docker prerequisites are available.

## Owning areas
- `ui/`
- `cli/`
- `docker-compose.yml`
- `doc/DOCKER.md`
- `doc/DEPLOYMENT-MODES.md`
- `scripts/`

## Responsibilities
Operator navigation, API clients, CLI lifecycle commands, local/deployed startup, ports, volumes, auth exposure, health checks, logs, and cleanup.

## Invariants
Trusted/local, private/authenticated, and public modes must remain distinct; deployment exposure must not silently widen; cleanup must not delete unintended state.

## Verification
Planned: AU-016 manifest, AU-030 environment probe, AU-031 disposable local boot, AU-032 authenticated bootstrap.

## Gaps
UI/API runtime and Docker health are unverified on this Android host.
