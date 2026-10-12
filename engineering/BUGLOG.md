# Buglog and Engineering Lessons

This is a durable lesson log, not a copy of every issue or CI failure.

## BL-001 — Source checkout is not a recovery plan

- Evidence: `doc/DATABASE.md`, `doc/DOCKER.md`, `doc/ENGINEERING-OPERATIONS-GUIDE.md`.
- Lesson: restore requires database, object/local storage, secrets references, workspace/runtime state, and provider configuration in addition to Git.
- Guardrail: maintain recovery records by state domain and perform clean-room boot/migration tests.

## BL-002 — Pooler and migration connections have different requirements

- Evidence: `doc/DATABASE.md`.
- Lesson: transaction poolers may require prepared statements disabled and direct migration connectivity.
- Guardrail: use `DATABASE_MIGRATION_URL` for direct schema operations and test the selected hosted connection mode.

## BL-003 — Telemetry, traces, and run logs are different paths

- Evidence: `AGENTS.md` and source path guidance.
- Lesson: privacy and review requirements depend on the actual data path, not a filename containing “observability.”
- Guardrail: classify changes by telemetry, OpenTelemetry, or local run-log path before review.

## BL-004 — Lockfile/patch policy is part of the build contract

- Evidence: `doc/DEVELOPING.md`, `pnpm-workspace.yaml`.
- Lesson: patched dependencies and CI-owned lockfile behavior can make a locally plausible change non-reproducible.
- Guardrail: preserve workspace patch/override synchronization and follow the repository lockfile policy.

## BL-005 — Local tooling gaps must remain explicit

- Evidence: current Termux inspection.
- Lesson: without pnpm, source inspection is possible but runtime/build claims are not.
- Guardrail: record unrun commands in `TEST_STATUS.md`; do not convert absence of tooling into a product defect.
