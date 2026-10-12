# Architecture Record

## Layers

```text
Board/UI + CLI
      |
REST/API + auth + company access checks
      |
Domain services + scheduler + governance + activity
      |
Drizzle DB / storage / secrets / workspace services
      |
Adapters and plugins
      |
External agents, CLIs, gateways, sandboxes, providers
```

## Important boundaries

- UI is an operator surface, not the source of authorization truth.
- Server services enforce company/instance scope and control-plane invariants.
- Database migrations are part of the deployable contract.
- Adapters own runtime-specific invocation and credential semantics.
- Plugins extend the self-hosted system without requiring every integration in core.
- Telemetry, OpenTelemetry traces, and local run-log events are distinct data paths.

## Main flows

### Task execution

Create/assign task → validate actor and company → checkout/lock task → select adapter → start/resume heartbeat → capture events/output/cost/artifacts → review/approval → complete, pause, fail, or recover.

### Authenticated startup

Load deployment mode/public URL → initialize database and migrations → establish auth/session configuration → bootstrap or claim first admin as permitted → serve API/UI.

### Recovery

Persist state and stop evidence → detect interrupted/stuck execution → preserve ownership and history → continue only through bounded adapter semantics or create visible recovery work → require human escalation when the safe path is unavailable.

## Data model emphasis

Core entities are company-scoped. Agents use a strict reports-to tree. Tasks/issues have parentage, a single assignee, blockers, comments/documents/artifacts, and activity history. Budgets and costs are recorded at company/agent/project/task scopes as supported by the current implementation.
