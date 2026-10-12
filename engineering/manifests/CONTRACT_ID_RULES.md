# Stable Contract ID Rules

Contract IDs bind plans, manifests, source, tests, recipes, and runtime evidence without relying on fragile line numbers.

## Prefixes

- `REQ-` product or implementation requirement
- `DOM-` bounded domain
- `ROUTE-` HTTP/API route
- `SVC-` service/module boundary
- `DB-` table/schema/migration boundary
- `CFG-` configuration/environment key
- `ADP-` adapter/provider boundary
- `TEST-` test or fixture
- `RUN-` executable operation recipe
- `EVD-` runtime evidence record
- `T-` development task
- `F-` file marker
- `S-` source-symbol marker

## Identity rules

1. IDs are uppercase and ASCII with a stable semantic slug where useful.
2. File and symbol markers are generated hashes of stable path/symbol identity.
3. Contract IDs are manually curated and must not be derived from line numbers.
4. Every contract records `source`, `tests`, `evidence`, and `status`.
5. Unknown relationships are recorded as `GAP`, never invented.
6. Renaming a symbol does not silently preserve its contract; record a compatibility alias or migration.
7. Generated indexes record their source commit and generator.

## Required relationship

```text
T-task -> REQ/DOM -> F-file -> S-symbol/ROUTE/DB -> TEST/RUN -> EVD-evidence
```
