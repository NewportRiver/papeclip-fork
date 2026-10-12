# Execution and Recovery Domain Manifest

Evidence: repository-derived/structural. Runtime: unverified.

## Owning areas
- `server/src/` execution, heartbeat, scheduler, recovery, and workspace services
- `server/src/vendor/paperclip-runner/`
- `packages/` runner/adapter-related packages
- `tests/` runner/recovery fixtures

## Responsibilities
Task assignment, heartbeat scheduling, execution checkout, run events, adapter invocation, stop/pause/retry, locks, failure handling, recovery, artifacts, and cost tracking.

## Invariants
No duplicate ownership; stop must be observable; retries must not blindly replay unsafe work; recovery must identify the last known state; external provider work must be bounded and auditable.

## Verification
Planned: AU-035 deterministic fake adapter, AU-036 interruption/recovery, AU-037 Hermes adapter.

## Gaps
Exact state transitions and runtime semantics require AU-014/AU-022 and executable fixtures.
