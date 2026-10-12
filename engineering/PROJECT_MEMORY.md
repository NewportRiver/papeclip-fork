# Project Memory

## Identity

Paperclip is an MIT-licensed Node.js/React control plane for autonomous AI companies. This fork is `NewportRiver/papeclip-fork`, based on upstream `paperclipai/paperclip`.

## Architecture

The server owns REST APIs, auth, orchestration, scheduling, connectors, and runtime services. The React/Vite UI is the board surface. Drizzle/PostgreSQL stores control-plane state. Adapters connect external agent runtimes. Shared packages define cross-layer contracts. The CLI handles onboarding, configuration, diagnostics, and operator workflows.

## Canonical concepts

Company → goals/projects → issues/tasks/comments/documents/artifacts → agent assignment → heartbeat/run → output/cost/activity/review. Agents form a strict reporting tree. Work is company-scoped and should remain traceable to a goal.

## Deployment facts

Canonical modes are `local_trusted` and `authenticated`; authenticated exposure is `private` or `public`. Bind is independently `loopback`, `lan`, `tailnet`, or `custom`. PostgreSQL can be embedded, Docker-hosted, or external/hosted.

## Repository conventions

Read `AGENTS.md`, then `doc/GOAL.md`, `doc/PRODUCT.md`, `doc/SPEC-implementation.md`, `doc/DEVELOPING.md`, and `doc/DATABASE.md` before broad changes. New repository plans belong in `doc/plans/`. Durable fork-specific engineering state belongs in `engineering/`.

## Integration boundary

`@paperclipai/hermes-paperclip-adapter` allows Hermes to be coordinated as an employee. Paperclip governs organization/task/run state; Hermes retains its own local runtime, skills, memory, providers, and recovery state.

## Important constraints

The current Android/Termux checkout has Node `v26.2.0` but no `pnpm`; dependency installation and runtime tests remain unverified until pnpm is available. Do not interpret that local blocker as a Paperclip product limitation.
