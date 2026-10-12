# Paperclip Engineering and Operations Guide

Status: repository-derived working guide
Repository: `NewportRiver/papeclip-fork`
Upstream: `paperclipai/paperclip`
Baseline inspected: `bfe7c6357d1e0c945c8cb84259153cb3b6542d28` (`canary/v2026.1011.0-canary.12`)

This guide is an engineering orientation document for the fork. It is intentionally derived from the repository's implementation, package manifests, deployment documents, and source layout. When this guide conflicts with an implementation contract, prefer `AGENTS.md`, `doc/SPEC-implementation.md`, `doc/DEVELOPING.md`, and `doc/DATABASE.md` in that order of specificity.

## 1. What Paperclip is

Paperclip is a control plane for autonomous AI companies. It does not require one particular agent runtime. It stores companies, goals, org charts, agents, tasks/issues, comments, approvals, budgets, activity, workspaces, skills, artifacts, and execution history, then invokes external agents through adapters.

The central architectural boundary is:

- Control plane: Paperclip server, database, scheduler, governance, API, and operator UI.
- Execution plane: local CLIs, processes, HTTP/webhook agents, gateways, sandboxes, and plugins invoked by adapters.

An agent has an adapter type and adapter configuration. The adapter defines how the agent is called, observed, authenticated, and stopped. Built-in adapter families include process/HTTP-style execution, local Claude/Codex/Gemini/OpenCode/Pi/Cursor/Grok/Kimi runtimes, OpenClaw gateway integration, and Hermes local/gateway integration.

## 2. Repository architecture

Important roots:

- `server/` — Express REST API, authentication, orchestration, schedulers, runtime services, connector services, and server-side UI serving.
- `ui/` — React/Vite board application and Storybook stories.
- `packages/db/` — Drizzle schema, migrations, embedded PostgreSQL integration, database client, migration checks.
- `packages/shared/` — shared TypeScript types, API path constants, validators, schemas, and cross-layer contracts.
- `packages/adapters/` — built-in agent adapters and adapter utilities.
- `packages/adapter-utils/` — shared adapter/runtime helpers.
- `packages/plugins/` — plugin runtime and plugin SDK packages.
- `packages/skills-catalog/` — shipped skills catalog package.
- `packages/teams-catalog/` — shipped team templates/catalog package.
- `cli/` — the `paperclipai` command-line interface.
- `skills/` — Paperclip runtime/operational skills; distinct from the app's company skills catalog.
- `scripts/` — development runners, release tooling, checks, smoke tests, and code-generation helpers.
- `docker/` — Dockerfiles and Compose deployment variants.
- `doc/` — product, implementation, deployment, database, connector, security, and operational contracts.

The workspace is a pnpm monorepo. Workspace members include `packages/*`, adapter packages, plugins (with explicit exclusions), `server`, `ui`, and `cli`. Root overrides and patches are defined in both `package.json` and `pnpm-workspace.yaml`; keep those lists synchronized.

## 3. Runtime request and execution model

A normal path is:

1. A board user or agent calls the REST API/UI.
2. The server authenticates the actor and resolves instance/company membership and permissions.
3. Services read or mutate company-scoped records through the shared DB layer.
4. A task/heartbeat scheduler selects eligible work.
5. The selected agent adapter creates or resumes an execution.
6. The adapter injects task/company/goal context and runtime policy into the external agent.
7. The server records run state, output, activity, costs, artifacts, and failures.
8. Governance rules can pause, reject, retry, or request human review.

The server process contains the lightweight scheduler/worker for heartbeat checks, stuck-run detection, and budget checks. V1 does not require a separate queue service.

Control-plane invariants include:

- Business entities are company-scoped.
- The org graph is a strict reporting tree with no cycles.
- Tasks have a single assignee and atomic checkout semantics.
- Mutating operations produce activity/audit records.
- Approval gates govern configured actions.
- Budget hard limits can auto-pause work.
- Recovery must not blindly replay tool calls; interrupted executions preserve ownership and visible stop/recovery evidence.

## 4. Data and persistence

Paperclip uses PostgreSQL through Drizzle ORM.

### Development default: embedded PostgreSQL

When `DATABASE_URL` is unset, the server starts embedded PostgreSQL and stores it under:

`~/.paperclip/instances/default/db/`

The server creates the database and applies migrations for an empty instance. This is the lowest-friction local mode. Resetting this development instance deletes that directory and its data.

### Local external PostgreSQL

The repository supplies Docker Compose for PostgreSQL 17. Configure `DATABASE_URL`, then run:

```sh
pnpm db:migrate
pnpm dev
```

### Hosted PostgreSQL

Supabase or another PostgreSQL-compatible provider can be used. Use a direct connection for migrations. If runtime uses a transaction pooler, set `DATABASE_MIGRATION_URL` to a direct connection and normally set `DATABASE_PREPARED_STATEMENTS=false`.

Relevant database settings:

```text
DATABASE_URL
DATABASE_MIGRATION_URL
DATABASE_PREPARED_STATEMENTS
DATABASE_POOL_MAX
DATABASE_IDLE_TIMEOUT_SECONDS
DATABASE_CONNECT_TIMEOUT_SECONDS
DATABASE_MAX_LIFETIME_SECONDS
DATABASE_APPLICATION_NAME
```

The schema is under `packages/db/src/schema/`; migrations are under `packages/db/src/migrations/`. Database changes require schema edits, exports, migration generation, migration safety checks, and typecheck.

Commands:

```sh
pnpm db:generate
pnpm db:migrate
pnpm --filter @paperclipai/db check:migrations
```

### File/object storage

Local storage defaults under the Paperclip instance data root, including uploaded assets, local secrets state, and workspace-related data. Production/cloud deployments can use S3-compatible storage. Treat database, object storage, and workspace data as separate recovery domains.

## 5. Deployment modes and network exposure

Canonical auth modes:

- `local_trusted` — local trusted operator, normally loopback-only, no human login friction.
- `authenticated` — login-required operation.

Authenticated exposure policies:

- `private` — LAN, VPN, or tailnet/private-network deployment.
- `public` — internet-facing deployment with explicit public URL and stronger checks.

Bind is independent from auth:

- `loopback` — localhost only.
- `lan` — all interfaces / `0.0.0.0`.
- `tailnet` — detected Tailscale address.
- `custom` — explicit host/IP.

Prefer loopback behind a reverse proxy for public deployments. Do not expose a local-trusted instance directly to an untrusted network.

Typical onboarding and diagnostics:

```sh
pnpm paperclipai onboard
pnpm paperclipai onboard --yes
pnpm paperclipai doctor
pnpm paperclipai auth bootstrap-ceo
```

The first-admin browser claim is available for fresh authenticated/private instances. Public authenticated instances should use the high-entropy CLI bootstrap invite path.

Important runtime settings:

```text
PAPERCLIP_DEPLOYMENT_MODE=local_trusted|authenticated
PAPERCLIP_DEPLOYMENT_EXPOSURE=private|public
PAPERCLIP_BIND=loopback|lan|tailnet|custom
PAPERCLIP_PUBLIC_URL=https://...
PAPERCLIP_ALLOWED_HOSTNAMES=...
PAPERCLIP_PORT=3100
HOST=127.0.0.1 or 0.0.0.0
```

## 6. Configuration and secrets

`.env.example` is a minimal starting point, not a complete configuration catalog. The source contains hundreds of test, adapter, cloud, runner, and deployment-specific variables. Configure only the variables needed for the selected deployment.

Core local configuration:

```text
PORT=3100
PAPERCLIP_PORT=3100
HOST=127.0.0.1
DATABASE_URL=...                 # omit for embedded PostgreSQL
BETTER_AUTH_SECRET=<high entropy secret>
PAPERCLIP_TOOL_ACTION_SIGNING_SECRET=<high entropy secret>
PAPERCLIP_HOME=<optional data root>
PAPERCLIP_DATA_DIR=<optional isolated dev root>
```

Authentication:

```text
BETTER_AUTH_SECRET
BETTER_AUTH_URL
BETTER_AUTH_BASE_URL
BETTER_AUTH_TRUSTED_ORIGINS
PAPERCLIP_AUTH_PUBLIC_BASE_URL
PAPERCLIP_AUTH_BASE_URL_MODE
PAPERCLIP_AUTH_RATE_LIMIT_ENABLED
PAPERCLIP_AUTH_DISABLE_SIGN_UP
```

Agent/provider credentials are adapter-specific. Common examples include provider API keys, local CLI login state, agent API keys, gateway tokens, MCP credentials, GitHub connection credentials, and cloud/runtime credentials. Keep them in the deployment secret manager or Paperclip's intended encrypted secret mechanism; do not commit them or put them in company-readable configuration.

Secrets with particularly high impact include:

- `BETTER_AUTH_SECRET`
- `PAPERCLIP_TOOL_ACTION_SIGNING_SECRET`
- `PAPERCLIP_SECRETS_MASTER_KEY` / `PAPERCLIP_SECRETS_MASTER_KEY_FILE`
- provider API keys
- `PAPERCLIP_AGENT_*` private keys/tokens
- GitHub, AWS, Vercel, connector, and cloud broker credentials
- database URLs containing passwords

The repository explicitly distinguishes first-party telemetry, OpenTelemetry observability, and local run-log events. Do not assume the word “observability” means data leaves the instance. Inspect the path and configuration before changing privacy behavior.

## 7. Installation and development

Prerequisites from the repository:

- Node.js `>=24.11.0`
- pnpm `9+`; the root package declares `pnpm@9.15.4`
- Git
- PostgreSQL only when using external DB mode
- Docker for container/Compose paths
- Optional agent CLIs and provider credentials for live adapter execution

The inspected Termux host has Node `v26.2.0`, but pnpm is not currently installed. No dependency installation was performed during this documentation pass.

Standard setup:

```sh
pnpm install
pnpm dev
```

The default dev server serves API and UI at:

`http://localhost:3100`

Health checks:

```sh
curl http://localhost:3100/api/health
curl http://localhost:3100/api/companies
```

Useful development variants:

```sh
pnpm dev:once
pnpm dev:server
pnpm dev:ui
pnpm dev:both
pnpm dev:mobile
pnpm dev:list
pnpm dev:stop
```

Use `--data-dir` for an isolated local instance:

```sh
pnpm dev --data-dir ./tmp/paperclip-dev
```

## 8. Build, test, and quality gates

Root scripts expose the main checks:

```sh
pnpm build
pnpm typecheck
pnpm test
pnpm test:e2e
pnpm test:release-smoke
pnpm check:node-version
pnpm check:module-boundaries
pnpm check:no-git-push
```

The cheap default is `pnpm test`, which runs Vitest. Browser suites are opt-in. Run the narrowest relevant test first, then broaden for release/PR handoff.

Database changes additionally require:

```sh
pnpm --filter @paperclipai/db check:migrations
pnpm db:generate
pnpm -r typecheck
```

The project uses patched dependencies. Do not casually remove patches or regenerate the lockfile. The repository policy says GitHub Actions owns `pnpm-lock.yaml`; pull requests should not commit lockfile changes unless the project workflow explicitly requires them.

## 9. Docker operation

Build from the repository root:

```sh
docker build -t paperclip-local .
```

Run with persistent state:

```sh
docker run --name paperclip \
  -p 3100:3100 \
  -e HOST=0.0.0.0 \
  -e PAPERCLIP_HOME=/paperclip \
  -e BETTER_AUTH_SECRET="$(openssl rand -hex 32)" \
  -e PAPERCLIP_TOOL_ACTION_SIGNING_SECRET="$(openssl rand -hex 32)" \
  -v "$(pwd)/data/docker-paperclip:/paperclip" \
  paperclip-local
```

Compose quickstart:

```sh
BETTER_AUTH_SECRET="$(openssl rand -hex 32)" \
PAPERCLIP_TOOL_ACTION_SIGNING_SECRET="$(openssl rand -hex 32)" \
  docker compose -f docker/docker-compose.quickstart.yml up --build
```

Compose PostgreSQL stack:

```sh
BETTER_AUTH_SECRET="$(openssl rand -hex 32)" \
  docker compose -f docker/docker-compose.yml up --build
```

Persist the `/paperclip` data mount and PostgreSQL volume. Use immutable image digests for production rather than mutable tags. The standard image includes agent tooling and a remote provider pack; downstream images must preserve the pack when using remote provider execution.

## 10. CLI responsibilities

The `cli/` package publishes the `paperclipai` command. It handles onboarding, configuration, doctor checks, auth bootstrap, instance/runtime operations, and operator-facing workflows. The root development alias is:

```sh
pnpm paperclipai <command>
```

The published CLI is intended to work against installed/server packages; local development uses the workspace TypeScript entrypoint.

## 11. Adapter and plugin engineering

Adapters are the execution boundary. A new adapter must define at least:

- how the agent is invoked or woken
- how identity and credentials are supplied
- how heartbeat/task context is delivered
- how output, cost, artifacts, and status are reported
- how cancellation and stop evidence work
- how failures are classified and recovered

Keep adapter-specific configuration in the adapter package. Synchronize shared contracts across `packages/shared`, server routes/services, UI clients, and database schema when behavior crosses layers.

Plugins extend the self-hosted runtime without adding every integration to core. Connector work should follow `doc/connections/CONNECTOR-PLAYBOOK.md`. Do not confuse:

- company skills: user-facing shared capabilities inside a company
- `skills/`: Paperclip runtime/operator skills
- `packages/skills-catalog/`: shipped catalog package
- external agent skills: runtime-specific instructions owned by the adapter/agent

## 12. Hermes integration

This fork includes the workspace dependency `@paperclipai/hermes-paperclip-adapter`. The adapter lets Paperclip manage Hermes as an employee while Hermes remains the execution runtime.

Recommended boundary:

- Paperclip owns company/org/task/goal governance, assignment, approval, budgets, and run history.
- Hermes owns its local agent loop, skills, memory, terminal tools, provider configuration, and local maintenance/recovery workflows.
- Credentials should remain scoped to the smallest control plane that needs them.
- Recovery should document both Paperclip instance state and Hermes local state.

For an Android/Termux deployment, prefer hosting Paperclip on a workstation/VPS/container and connecting Hermes through the supported adapter or gateway. A direct all-in-Termux deployment should first prove Node, pnpm, embedded PostgreSQL, process execution, and any required browser/native dependencies.

## 13. Operational safety

Before exposing an instance:

1. Select `authenticated/private` or `authenticated/public` intentionally.
2. Set high-entropy auth and tool-signing secrets.
3. Set a canonical `PAPERCLIP_PUBLIC_URL` for authenticated deployments.
4. Configure allowed hostnames and trusted origins narrowly.
5. Use a database backup and restore test.
6. Set company/agent/project budgets.
7. Review adapter permissions and connector access.
8. Keep MCP/runtime private-host allowlists explicit.
9. Avoid placing provider tokens in repo files, task text, artifacts, or logs.
10. Verify stop, pause, approval, and recovery behavior before enabling autonomous schedules.

## 14. Recovery and backup

Recovery consists of more than a Git checkout. Preserve and test:

- source revision and package manifests
- database and migration state
- Paperclip instance data root
- uploaded/object-storage data
- encrypted secret material or its external secret-manager references
- company/agent/adapter configuration
- workspace and runtime-service state where required
- deployment environment and reverse-proxy configuration
- Paperclip version/image digest
- Hermes state separately when the Hermes adapter is used

Use `pnpm db:backup` and the documented restore procedures. Never claim restore readiness from source alone; perform a clean-room migration/boot test and a health check.

## 15. Known baseline limitations of this guide

- This guide covers engineering-relevant configuration and the main operational paths, not every test-only environment variable.
- The repository contains many advanced cloud, runner, E2E, adapter, and release variables. Their authoritative definitions remain in source and the relevant `doc/` files.
- This fork was cloned and inspected, but dependencies were not installed and the server was not started during this pass because pnpm is absent on the current Termux host.
- The guide should be refreshed when the fork changes its deployment model, package-manager policy, adapter contract, database mode, or Hermes integration.

## Source documents consulted

- `AGENTS.md`
- `package.json`
- `pnpm-workspace.yaml`
- `.env.example`
- `doc/GOAL.md`
- `doc/PRODUCT.md`
- `doc/SPEC-implementation.md`
- `doc/DEVELOPING.md`
- `doc/DATABASE.md`
- `doc/DEPLOYMENT-MODES.md`
- `doc/DOCKER.md`
- `server/package.json`
- `packages/db/package.json`
