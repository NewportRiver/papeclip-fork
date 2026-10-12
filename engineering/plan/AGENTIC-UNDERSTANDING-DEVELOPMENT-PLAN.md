# Agentic Understanding Development Plan

Branch: `develop/agentic-understanding`
Base: `master` at the branch creation point
Owner: NewportRiver engineering
Status: planned

## Objective

Build a durable, evidence-backed engineering knowledge and automation layer that allows an agent to understand, operate, modify, test, recover, and improve Paperclip without loading the entire repository into one context or inventing runtime claims.

## Success definition

A fresh engineering agent can:

1. Find the owning domain/package for a requested behavior.
2. Trace a behavior across UI/API/service/schema/adapter/test boundaries.
3. Identify required configuration, secrets, prerequisites, and risks.
4. Run an isolated verification recipe.
5. Make a bounded change with tests and rollback notes.
6. Update the relevant manifest, index, test status, and journal records.
7. Explain what is repository-derived, runtime-verified, planned, or blocked.

## Non-goals

- Loading all source into one prompt.
- Replacing upstream product or implementation contracts.
- Creating a pretend semantic graph without evidence.
- Automatically modifying production, credentials, providers, or external services.
- Treating generated indexes as authoritative source.

## Workstreams

### A. Knowledge foundation

File catalog, package manifests, domain manifests, stable IDs, Markdown registry, schema/versioning, and stale-index detection.

### B. Control-plane understanding

Routes, services, auth/company scope, schema/migrations, task state machine, heartbeat execution, budgets, approvals, pause, stop, and recovery.

### C. Executable operations

Disposable local boot, health, onboarding, company/agent/task lifecycle, heartbeat, pause/resume, migration, backup/restore, and cleanup recipes.

### D. Agent service roles

Role-specific skills with triggers, context retrieval, tools, permissions, side-effect levels, verification, rollback, and escalation.

### E. Continuous improvement

Change detection, documentation reconciliation, evidence capture, regression records, capability coverage, and fresh-session resumption.

## Milestones and exit criteria

### M0 — Baseline and branch

Exit: branch exists from clean synchronized master; repository baseline and constraints are recorded.

### M1 — Knowledge map

Exit: all major packages have manifests; catalog and registry regenerate; every manifest names ownership, entrypoints, dependencies, tests, and gaps.

### M2 — Contract graph

Exit: core routes/services/schema/migrations/tests and task execution paths are linked with stable IDs and evidence levels.

### M3 — Local operation

Exit: an isolated instance can boot, pass health, onboard, create a company/agent/task, and cleanly shut down using documented recipes.

### M4 — Execution and recovery

Exit: heartbeat, adapter invocation, stop, pause/resume, budget enforcement, failure, and recovery behavior have recipes and captured evidence.

### M5 — Agent roles

Exit: role-specific skills can safely perform read-only analysis and bounded local maintenance, escalating external side effects.

### M6 — Continuous reconciliation

Exit: changes can identify stale catalogs/manifests/docs/tests, refresh safe indexes, and open explicit follow-up tasks without silently altering product behavior.

## Verification policy

Every milestone requires:

- source diff review
- `git diff --check`
- relevant unit/typecheck/build/test command
- recipe output or explicit blocker
- updated `engineering/TEST_STATUS.md`
- updated `engineering/CURRENT_WORK.md`
- journal entry for durable lessons

Runtime proof must include commit, instance/data root, timestamp, command, result, and redaction status. Secrets and unrestricted transcripts are never stored.

## Risks and mitigations

- Scope explosion → implement one domain manifest and one recipe at a time.
- Stale generated metadata → record source commit and add freshness checks.
- False semantic confidence → require evidence level on every claim.
- Destructive automation → default to read-only/isolated levels and require escalation.
- Provider cost/security → use fixtures and fake adapters before live providers.
- Android/Termux constraints → support remote Paperclip hosting and keep local checks lightweight.
- Upstream divergence → keep custom engineering files additive and periodically compare upstream changes.

## Recommended execution order

Complete tasks in `TASKS.md` by dependency order. Do not start live adapter/provider work before the disposable local control-plane path is verified.
