# Agentic Understanding Task Backlog

Branch: `develop/agentic-understanding`
Status: planned

Task states: `TODO`, `IN_PROGRESS`, `BLOCKED`, `DONE`.

## Phase 0 — Baseline and governance

### AU-001 — Record branch baseline
- State: DONE
- Depends on: none
- Deliverable: branch from synchronized `master`, baseline in `engineering/CURRENT_WORK.md`.
- Acceptance: branch/status/HEAD recorded and working tree clean before task edits.

### AU-002 — Define evidence and automation policy
- State: DONE
- Depends on: AU-001
- Deliverable: `engineering/ENGINEERING_FUNDAMENTALS.md`, roadmap, confidence model.
- Acceptance: repository-derived, runtime-verified, planned, and blocked states are distinct; side-effect levels are documented.

### AU-003 — Define metadata schema and regeneration contract
- State: DONE
- Depends on: AU-002
- Deliverable: `engineering/catalog/FILE_METADATA_SCHEMA.md`, catalog scripts.
- Acceptance: catalog has provenance, limitations, deterministic inputs, and a documented regeneration command.

## Phase 1 — Knowledge map

### AU-010 — Create package/domain manifest schema
- State: TODO
- Depends on: AU-003
- Deliverable: `engineering/manifests/MANIFEST_SCHEMA.md` and validation script.
- Acceptance: manifest fields cover purpose, boundaries, owners, entrypoints, dependencies, config, data, tests, runbooks, invariants, evidence, and gaps.

### AU-011 — Manifest server/API/auth domain
- State: TODO
- Depends on: AU-010
- Deliverable: `engineering/manifests/server-api-auth.md`.
- Acceptance: routes, auth loaders, actor types, company/instance checks, error contracts, and tests are linked to source paths.

### AU-012 — Manifest database/schema/migrations domain
- State: TODO
- Depends on: AU-010
- Deliverable: `engineering/manifests/database.md`.
- Acceptance: DB client, schema roots, migration workflow, backup/restore, pooling modes, and migration tests are mapped.

### AU-013 — Manifest task/goal/company domain
- State: TODO
- Depends on: AU-010
- Deliverable: `engineering/manifests/company-work.md`.
- Acceptance: company, goal, project, issue/task, comments, artifacts, assignment, and scope invariants are mapped.

### AU-014 — Manifest heartbeat/execution/recovery domain
- State: TODO
- Depends on: AU-010
- Deliverable: `engineering/manifests/execution-recovery.md`.
- Acceptance: scheduler, state transitions, locks, adapter boundary, stop, retry, pause, watchdog, and recovery paths are mapped.

### AU-015 — Manifest adapters/Hermes/plugins domain
- State: TODO
- Depends on: AU-010
- Deliverable: `engineering/manifests/adapters-hermes-plugins.md`.
- Acceptance: adapter packages, plugin SDK/runtime, Hermes adapter, credentials, invocation contracts, and tests are mapped.

### AU-016 — Manifest UI/CLI/deployment domain
- State: TODO
- Depends on: AU-010
- Deliverable: `engineering/manifests/ui-cli-deployment.md`.
- Acceptance: UI routes, API clients, CLI commands, Docker/Compose paths, bind/auth modes, and operator docs are mapped.

### AU-017 — Manifest connectors/MCP/skills/workspaces domain
- State: TODO
- Depends on: AU-010
- Deliverable: `engineering/manifests/integrations-runtime.md`.
- Acceptance: connection auth, MCP, skills, workspace/runtime services, sandbox boundaries, and security docs are mapped.

### AU-018 — Map tests and fixtures to capabilities
- State: TODO
- Depends on: AU-011, AU-012, AU-013, AU-014, AU-015, AU-016, AU-017
- Deliverable: capability-to-test matrix under `engineering/catalog/`.
- Acceptance: each critical capability names at least one test/recipe or an explicit coverage gap.

### AU-019 — Add catalog freshness check
- State: TODO
- Depends on: AU-010
- Deliverable: script/check that compares catalog provenance and tracked-file state.
- Acceptance: stale catalog produces a clear non-zero result; refresh produces a clean result.

## Phase 2 — Contract graph

### AU-020 — Define stable contract IDs
- State: TODO
- Depends on: AU-010
- Deliverable: ID convention for routes, services, tables, migrations, adapters, recipes, and tests.
- Acceptance: IDs are stable across documentation refreshes and link to source paths.

### AU-021 — Map route/service/schema edges
- State: TODO
- Depends on: AU-011, AU-012, AU-020
- Deliverable: machine-readable and Markdown control-plane graph.
- Acceptance: selected core routes trace through service and schema layers.

### AU-022 — Map task execution state machine
- State: TODO
- Depends on: AU-014, AU-020
- Deliverable: state diagram plus transition/source/test links.
- Acceptance: valid transitions, locks, stop, retry, pause, and recovery boundaries are explicit.

### AU-023 — Map configuration and environment variables
- State: TODO
- Depends on: AU-011, AU-012, AU-015, AU-016, AU-017
- Deliverable: layered operator configuration index.
- Acceptance: core variables map to loader/consumer/docs; test-only variables are separated.

### AU-024 — Map security and side-effect boundaries
- State: TODO
- Depends on: AU-011, AU-015, AU-017, AU-020
- Deliverable: security/control matrix.
- Acceptance: human, agent, connector, MCP, workspace, provider, and production side effects have explicit controls and escalation levels.

## Phase 3 — Executable operation

### AU-030 — Install prerequisite and environment probe
- State: TODO
- Depends on: AU-001
- Deliverable: safe probe documenting Node, pnpm, Docker, PostgreSQL, ports, storage, and platform.
- Acceptance: probe is read-only and writes sanitized evidence.

### AU-031 — Disposable local boot recipe
- State: TODO
- Depends on: AU-012, AU-016, AU-030
- Deliverable: isolated `local_trusted` boot recipe.
- Acceptance: boot, health, logs, data root, shutdown, and cleanup are proven.

### AU-032 — Authenticated/private bootstrap recipe
- State: TODO
- Depends on: AU-011, AU-031
- Deliverable: private authenticated onboarding/first-admin recipe.
- Acceptance: auth flow and failure/cleanup behavior are recorded without secrets.

### AU-033 — Company/agent/task lifecycle recipe
- State: TODO
- Depends on: AU-013, AU-031
- Deliverable: API/UI lifecycle recipe.
- Acceptance: create company, goal, agent, project/task, assign, comment, and inspect activity.

### AU-034 — Database migration/backup/restore recipe
- State: TODO
- Depends on: AU-012, AU-031
- Deliverable: migration and clean-room restore recipe.
- Acceptance: schema status, backup artifact, restore boot, and health check are proven.

### AU-035 — Heartbeat with deterministic fake adapter
- State: TODO
- Depends on: AU-014, AU-033
- Deliverable: fake adapter test/recipe.
- Acceptance: assignment, checkout, run events, completion, failure, and cost path are captured without provider cost.

### AU-036 — Stop/pause/recovery recipe
- State: TODO
- Depends on: AU-014, AU-035
- Deliverable: deterministic interruption and recovery recipe.
- Acceptance: no blind tool replay; stop evidence, ownership, recovery action, and escalation are visible.

### AU-037 — Hermes adapter local/gateway recipe
- State: TODO
- Depends on: AU-015, AU-035, AU-036
- Deliverable: Hermes integration recipe.
- Acceptance: Hermes run, task bridge, stop, output, and failure evidence are proven in an isolated environment.

### AU-038 — Connector/MCP least-privilege recipe
- State: TODO
- Depends on: AU-017, AU-024, AU-031
- Deliverable: fixture-based connector/MCP authorization recipe.
- Acceptance: allowed, ask, denied, secret redaction, and cleanup states are tested.

## Phase 4 — Agent service roles

### AU-040 — Repository navigator skill
- State: TODO
- Depends on: AU-018, AU-020
- Deliverable: role skill for catalog/domain/contract retrieval.
- Acceptance: fresh agent can locate owning files and evidence for a selected behavior.

### AU-041 — Operator skill
- State: TODO
- Depends on: AU-031, AU-032, AU-033
- Deliverable: bounded local Paperclip operator skill.
- Acceptance: agent can run lifecycle recipes and report evidence without external side effects.

### AU-042 — Database/recovery engineer skill
- State: TODO
- Depends on: AU-034, AU-024
- Deliverable: migration/backup/restore skill.
- Acceptance: destructive actions require isolation and confirmation; restore claims require boot proof.

### AU-043 — Adapter/Hermes engineer skill
- State: TODO
- Depends on: AU-035, AU-036, AU-037
- Deliverable: adapter troubleshooting and development skill.
- Acceptance: deterministic fake runtime is used before live provider testing.

### AU-044 — Security/release reviewer skill
- State: TODO
- Depends on: AU-018, AU-024, AU-034
- Deliverable: review skill for secrets, permissions, migrations, external effects, and release readiness.
- Acceptance: reviewer returns evidence-backed pass, fail, or unresolved status.

## Phase 5 — Continuous improvement

### AU-050 — Documentation drift detector
- State: TODO
- Depends on: AU-019, AU-018
- Deliverable: source/doc/manifest/test drift report.
- Acceptance: report distinguishes stale generated indexes from authoritative documentation gaps.

### AU-051 — Change-to-knowledge update helper
- State: TODO
- Depends on: AU-050, AU-020
- Deliverable: helper that proposes affected manifests, tests, and engineering records from a Git diff.
- Acceptance: proposal is reviewable and does not silently rewrite durable docs.

### AU-052 — Fresh-session resumption benchmark
- State: TODO
- Depends on: AU-040, AU-041, AU-050
- Deliverable: benchmark prompt and expected outputs.
- Acceptance: a new agent reconstructs state, selects the right task, runs a safe check, and updates current work.

### AU-053 — Agentic maintenance loop
- State: TODO
- Depends on: AU-050, AU-051, AU-052
- Deliverable: bounded loop that checks evidence, selects the next low-risk improvement, executes, verifies, and logs.
- Acceptance: loop has explicit side-effect ceiling, stop condition, audit trail, and no recursive scheduling.

### AU-054 — Capability coverage dashboard
- State: TODO
- Depends on: AU-018, AU-050
- Deliverable: generated coverage report for domains, contracts, recipes, tests, and runtime evidence.
- Acceptance: uncovered critical capabilities are visible and prioritized.

## Definition of done for the branch

The branch is ready for review when:

- all `DONE` tasks have artifacts and verification evidence
- remaining tasks are ordered and dependency-valid
- manifests, contract graph, recipes, skills, and drift checks are linked from `engineering/README.md`
- `TEST_STATUS.md` distinguishes run, skipped, blocked, and not-applicable checks
- no secrets or raw credentials exist in generated artifacts
- `git diff --check` passes
- a fresh-session resumption benchmark can identify the next safe task
