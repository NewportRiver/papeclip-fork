# Newport River Server Migration and Fresh-Agent Runbook

Status: planned and partially verified
Owner: NewportRiver engineering
Purpose: give a fresh Hermes or engineering agent a safe, discoverable procedure for setting up Paperclip on the Newport River server.

This document is an operating checklist, not proof that the migration has completed. Commands and runtime claims must be executed on the target server and recorded as evidence.

## Target boundary

- Intended host: Windows machine `Architect1`, reached from Android through the Windows LAN address `192.168.1.34`.
- Intended Linux environment: WSL user `architect`.
- Intended deployment: Paperclip control plane plus PostgreSQL, Hermes adapter/runtime, backups, monitoring, and durable project memory.
- Current hardware details are user-provided and require live verification before capacity claims.
- Never copy credentials, private keys, invite URLs, database URLs, or unrestricted logs into this repository.

## Fresh-agent start sequence

A fresh agent must read these files before changing anything:

1. `AGENTS.md`
2. `engineering/README.md`
3. `engineering/PROJECT_MEMORY.md`
4. `engineering/CURRENT_WORK.md`
5. `engineering/SYSTEM_STATE.md`
6. `engineering/TEST_STATUS.md`
7. this runbook
8. `doc/DEVELOPING.md`, `doc/DATABASE.md`, `doc/DOCKER.md`, and `doc/DEPLOYMENT-MODES.md`
9. the Hermes adapter documentation and the Hermes recovery/project-memory records

Then inspect the live target. Do not assume that a previous Android checkout, server, database, or adapter process is still valid.

## Phase 0 — establish a safe checkpoint

- Confirm the target host, WSL distribution, user, working directory, Git remotes, branch, and clean/dirty state.
- Confirm SSH reachability from the operator node without printing private material.
- Confirm time synchronization, available disk, RAM, CPU, GPU visibility if relevant, open ports, and running Paperclip/PostgreSQL/Hermes processes.
- Record a redacted baseline in an evidence file outside secrets.
- Create or verify a rollback point before installation or migration.
- Do not delete an existing checkout, database, workspace, or service until ownership and backup status are known.

Suggested read-only checks on the server:

```sh
hostname
whoami
pwd
git status --short --branch
git remote -v
node --version
pnpm --version
psql --version
df -h
free -h
ss -ltnp
```

## Phase 1 — obtain and inspect the source

- Clone or update `https://github.com/NewportRiver/papeclip-fork.git`.
- Check out the intended branch, normally `develop/agentic-understanding` for engineering work or a reviewed release branch for service deployment.
- Verify the commit and compare it with the remote before installing dependencies.
- Read the repository instructions and regenerate/check durable indexes after any intentional documentation changes.
- Confirm whether the deployment is a clean install, migration of an existing instance, or a parallel rehearsal. These paths must not be conflated.

## Phase 2 — verify prerequisites

- Node must satisfy the repository's current documented version requirement.
- Install/use the repository-supported pnpm version through the approved mechanism; do not silently substitute an incompatible package manager.
- Select the database mode deliberately: embedded PGlite for disposable development only, PostgreSQL for the intended persistent server deployment.
- Confirm Docker/Compose availability only if that deployment mode is chosen.
- Confirm a supported process supervisor/service strategy for WSL/Windows. Do not assume a shell process survives logout or reboot.
- Confirm the Hermes runtime, provider credentials, adapter package, and any required CLI tools are available without exposing secret values.

Unresolved prerequisites must be recorded as `blocked`, not worked around by inventing configuration.

## Phase 3 — configure the Paperclip control plane

- Copy the appropriate environment template without committing the resulting secret-bearing file.
- Choose the security model explicitly:
  - `local_trusted` for loopback-only disposable/local work.
  - `authenticated/private` for trusted LAN, VPN, or tailnet access.
  - `authenticated/public` only after reverse proxy, TLS, rate limiting, bootstrap, and exposure review.
- Choose bind/reachability separately from authentication: loopback, LAN, tailnet, or custom.
- Configure PostgreSQL, storage paths, public/base URL, logging, and trusted runtime settings according to the current deployment docs.
- Keep secrets in the server's protected environment or secret manager. Store only variable names, redacted fingerprints, and configuration decisions in evidence.
- Run the supported onboarding/doctor flow and retain sanitized output.

Expected initial commands, subject to current repository docs:

```sh
pnpm install
pnpm paperclipai doctor
pnpm paperclipai onboard
```

Do not run migration-destructive commands until the database backup and rollback plan is confirmed.

## Phase 4 — initialize and verify the instance

- Apply or verify database migrations using the supported command.
- Start Paperclip through the chosen supervisor.
- Verify `/api/health` and the intended authenticated access path.
- Create/claim the first administrator using the documented private bootstrap flow; never place a bootstrap invite URL in Git or chat logs.
- Create a test company and minimal test agent/task only after the instance boundary is confirmed.
- Verify company isolation, activity logging, authentication, restart persistence, and clean shutdown.
- Capture runtime evidence containing commit, host, data-root identifier, timestamp, command, result, and redaction status.

## Phase 5 — integrate Hermes safely

- Read the current Hermes-Paperclip adapter documentation and inspect its source/configuration contract.
- Configure Paperclip to govern task/company/run state while Hermes retains its local providers, skills, memory, and recovery state.
- Begin with a deterministic fake adapter or no-cost test worker.
- Verify one complete loop: assign task → heartbeat/run → result/activity → review/close.
- Verify stop, pause/resume, timeout, failure, retry, and recovery behavior before enabling live Hermes work.
- Confirm that the adapter cannot cross company boundaries or bypass Paperclip approval/budget controls.
- Only then connect the intended Hermes instance and provider.

## Phase 6 — persistence, recovery, and operations

Back up and document all durable state domains separately:

- Git source and engineering records.
- PostgreSQL database and migration version.
- Paperclip local/object storage and artifact paths.
- Protected configuration/secret references, without copying secret values.
- Agent workspaces and runtime state.
- External connector/provider state.
- Hermes memory, skills, provider configuration, and recovery records.

Test restoration into a disposable location. A backup that has not been restored is not verified.

Document:

- service start/stop/restart commands
- health and log locations
- backup schedule and retention
- restore procedure
- upgrade and rollback procedure
- port and firewall policy
- operator access path
- emergency stop procedure
- ownership of each data path

## Completion gate

Migration is not complete until all of the following have real evidence:

- source commit and branch recorded
- prerequisites verified
- dependencies installed successfully
- database migrations completed
- Paperclip starts under the intended supervisor
- health endpoint succeeds
- administrator bootstrap succeeds
- persistent restart succeeds
- fake-agent lifecycle succeeds
- Hermes adapter lifecycle succeeds, or the exact blocker is recorded
- backup and disposable restore succeed
- secrets are absent from repository, evidence, and logs
- `engineering/TEST_STATUS.md`, `engineering/CURRENT_WORK.md`, `engineering/SYSTEM_STATE.md`, and `engineering/JOURNAL.md` are updated

Until then, status must remain `planned`, `partially verified`, or `blocked` as appropriate.

## Known gaps to resolve

- Exact server hardware and current OS/WSL state are not independently verified here.
- Exact Paperclip branch/release to deploy must be selected at migration time.
- pnpm availability and dependency installation must be verified on the server.
- PostgreSQL topology, storage paths, supervisor, reverse proxy, TLS, and firewall policy are not yet recorded.
- Hermes adapter version/configuration and provider policy require live inspection.
- No end-to-end Paperclip or Hermes runtime evidence exists in this repository yet.
