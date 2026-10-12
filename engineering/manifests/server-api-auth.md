# Server/API/Auth Domain Manifest

Evidence: repository-derived/structural. Runtime: blocked until dependencies are available.

## Purpose
HTTP/API control plane, authentication, authorization, instance/company scope, and operator-facing server boundaries.

## Owning areas
- `server/src/`
- `server/package.json`
- `packages/shared/`
- `doc/DEPLOYMENT-MODES.md`
- `doc/DEVELOPING.md`

## Entry points
- Server package scripts and server source entrypoints: inspect `server/package.json` and `server/src/`.
- API routes/services: locate through `engineering/catalog/FUNCTION_INDEX.md` and markers.

## Dependencies
Database package, shared types, configuration, deployment mode, connector/adapter boundaries, UI and CLI clients.

## Invariants
Authentication, company scope, actor permissions, deployment exposure, and secret handling must be explicit before external access is enabled.

## Verification
Planned: AU-031/AU-032 boot and authenticated bootstrap recipes; AU-021 route/service/schema graph.

## Gaps
Exact route graph and runtime auth behavior require AU-011/AU-021 and a dependency-enabled environment.
