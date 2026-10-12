# Agentic Paperclip Understanding and Automation Roadmap

## Goal

Enable an engineering agent to safely set up, operate, improve, modify, troubleshoot, and eventually explain the Paperclip system from repository evidence plus runtime verification.

The objective is not to place every source line into one prompt. The objective is a navigable, queryable, evidence-backed knowledge system that can retrieve the right context, execute the right verification, and record what it learned.

## The limit we are overcoming

A flat file catalog answers "what files exist?" but not:

- which files implement a user journey
- which route calls which service and schema
- what configuration controls a behavior
- what invariant a function protects
- which test proves the behavior
- what runtime evidence is required before changing it
- what can safely be automated

We therefore use progressive semantic compression and verification.

## Knowledge layers

### Layer 0 — Source of truth

The actual repository, package manifests, source, schemas, migrations, tests, docs, scripts, configs, release notes, and Git history.

### Layer 1 — Structural catalog

`engineering/catalog/FILE_CATALOG.json` and `FUNCTION_INDEX.md` index every tracked file and extracted symbol. This layer provides coverage and retrieval coordinates, not semantic proof.

### Layer 2 — Domain manifests

Create one manifest per major bounded context:

- server/API and authentication
- companies/goals/org chart
- tasks/issues/comments/documents
- heartbeat/execution/recovery
- adapters and Hermes integration
- database/schema/migrations
- workspaces/sandboxes/runtime services
- connectors/MCP/skills
- UI/operator journeys
- CLI/deployment/maintenance
- runner and provider qualification

Each manifest should state:

- purpose and boundaries
- owning packages/directories
- important entrypoints
- data tables and migrations
- environment variables
- public API routes/contracts
- invariants and security rules
- linked tests and fixtures
- operational runbooks
- known gaps
- evidence level and inspected commit

### Layer 3 — Contract graph

Represent relationships as explicit edges:

```text
route -> service -> schema/table -> migration
route -> auth/policy check
task state -> scheduler -> adapter -> runtime event
adapter -> provider credential -> external process/API
feature -> UI route -> API route -> test/e2e fixture
config variable -> loader -> behavior
```

The first implementation can be Markdown/JSON. A graph database is optional; stable IDs and links matter more than storage technology.

### Layer 4 — Executable verification recipes

Every important capability gets a verification recipe containing:

- prerequisites
- setup/isolation instructions
- command or API call
- expected evidence
- cleanup
- failure interpretation
- security/cost boundary

Examples:

- boot local trusted instance
- authenticated first-admin bootstrap
- create company and CEO
- assign and checkout task
- invoke Hermes heartbeat
- pause and resume task
- budget hard-stop
- database migration and restore
- connector authorization
- workspace creation/recovery
- adapter cancellation

A recipe is not marked verified from documentation alone.

### Layer 5 — Agent operating skills

Provide role-specific skills rather than one giant prompt:

- repository navigator
- Paperclip operator
- database/migration engineer
- adapter engineer
- UI engineer
- connector/MCP engineer
- recovery engineer
- security reviewer
- test/release engineer
- Hermes integration engineer

Each skill should contain triggers, allowed tools, required context, safe defaults, verification, rollback, and escalation rules.

### Layer 6 — Runtime evidence

Capture bounded evidence from real runs:

- health response
- startup/migration log
- API request/response contract
- task/run state transitions
- adapter stdout/stderr and normalized events
- cost/budget records
- database snapshots or migration status
- browser/e2e result
- stop/recovery evidence

Evidence must be redacted and linked to a recipe, commit, instance, and timestamp. Never use raw secrets or unrestricted transcripts as knowledge artifacts.

### Layer 7 — Continuous reconciliation

A maintenance loop checks:

- source changes without documentation updates
- docs pointing to missing files
- manifests with stale paths/symbols
- tests with no feature mapping
- environment variables without operator docs
- routes without auth/company-scope notes
- migrations without safety records
- skills that reference removed commands
- catalog provenance older than the source baseline

## Agent workflow for any engineering request

1. Classify intent: orientation, operation, bug, feature, review, recovery, or release.
2. Query the structural catalog for the affected layer/domain.
3. Load the relevant domain manifest and contract edges.
4. Read the owning source, tests, and contributor rules.
5. State facts, assumptions, risk, and verification plan.
6. Make the smallest safe change on a branch.
7. Run the narrowest verification recipe.
8. Update code, tests, manifest, decision/bug/journal records, and indexes.
9. Run broader checks when scope requires.
10. Report verified, unverified, and blocked claims separately.

## Automation control levels

### Level 0 — Read-only analysis

Catalog, search, document synthesis, dependency mapping, and status reporting. No side effects.

### Level 1 — Safe local maintenance

Refresh catalogs, registries, docs, generated indexes, and test reports. No credentials, deployments, or destructive operations.

### Level 2 — Isolated development

Create branches, run tests, start disposable instances, apply reversible local migrations, and create fixtures.

### Level 3 — Controlled integration

Modify source, database migrations, adapters, or deployment configuration only with tests, review records, rollback notes, and explicit scope.

### Level 4 — Production/external side effects

Push releases, change cloud resources, send external messages, alter provider credentials, or run autonomous agent workloads. Requires explicit authorization, audit evidence, and a recovery checkpoint.

Default agents should operate at Level 0–1 and request escalation for Levels 2–4.

## Priority implementation sequence

### Phase A — Make the map useful

- keep the file/symbol catalog current
- build package-level manifests for `server`, `packages/db`, `packages/shared`, `packages/adapters`, `ui`, `cli`, and `packages/paperclip-runner`
- map package manifests to tests and docs
- add a stale-catalog check

Exit criterion: an agent can identify ownership and nearby evidence for any tracked source file.

### Phase B — Map the control plane

- document route/service/schema relationships
- identify auth, company-scope, budget, approval, checkout, pause, and recovery invariants
- map migrations to affected tables and tests
- document configuration loaders and core environment variables

Exit criterion: an agent can explain a normal task execution path and name the files/tests involved.

### Phase C — Make operation executable

- create isolated local boot recipe
- add health, onboarding, company, task, heartbeat, stop, and recovery recipes
- capture sanitized evidence
- add failure interpretation and cleanup

Exit criterion: an agent can operate a disposable Paperclip instance without relying on chat memory.

### Phase D — Add agentic service roles

- publish the role-specific skills
- enforce tool and side-effect boundaries
- make each skill require evidence and update records
- connect Hermes through the existing adapter only after local recipes pass

Exit criterion: agents can perform bounded operations with audit trails and escalation.

### Phase E — Close the learning loop

- compare commits against manifests and recipes
- detect unindexed new routes/configs/migrations
- run targeted verification after changes
- update feature/bug/decision/journal records automatically where safe
- keep human review for security, external side effects, and production changes

Exit criterion: the fork continuously improves its own operational documentation without inventing facts.

## Design rules for maximum utility

- Retrieval beats prompt stuffing.
- Stable IDs beat fragile filenames.
- Domain context beats whole-repository context.
- Tests are evidence links, not merely quality gates.
- Runtime traces are required for behavior claims.
- Every automation action needs preconditions and rollback.
- Generated indexes must never replace authoritative source.
- Keep stock/upstream behavior distinct from NewportRiver customizations.
- Preserve a clean boundary between Paperclip state and Hermes state.
- Optimize for fresh-session resumption: a new agent should know what to read, what is verified, and what to do next.

## Current gap

The fork currently has the structural catalog and engineering memory layer. It does not yet have complete domain manifests, route/service/schema contract graphs, executable local recipes, or runtime evidence because pnpm is unavailable in the current Termux environment. Those are the next high-value additions.
