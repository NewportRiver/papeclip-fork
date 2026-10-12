# Database and Migration Domain Manifest

Evidence: repository-derived/structural. Runtime: blocked until PostgreSQL/toolchain is available.

## Owning areas
- `packages/db/`
- `doc/DATABASE.md`
- `scripts/`
- migration/schema files identified by the catalog role `migration/schema`

## Responsibilities
Persistence schema, Drizzle/database client behavior, migrations, embedded/PostgreSQL deployment modes, backup, restore, and data lifecycle.

## Dependencies
Server services, task/company/goal domains, deployment configuration, Docker/Compose, operational backup paths.

## Invariants
Migrations must be reviewable and reversible where possible; backups must be created before destructive changes; restored data must boot and pass health checks.

## Verification
Planned: AU-034 migration/backup/restore recipe; AU-012 schema manifest; AU-021 route/service/schema graph.

## Gaps
Live migration and clean-room restore are unverified because `pnpm` is unavailable on Android.
