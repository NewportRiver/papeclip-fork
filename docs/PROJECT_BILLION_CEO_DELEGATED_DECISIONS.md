# Project BILLION — Programmatic CEO access to Paperclip Decisions (fork)

**Status: development branch, NOT installed or accepted on Architect1.**
Fork: `NewportRiver/papeclip-fork`.
Source checkout: `/home/architect/PAPERCLIP_NEWPORT_RIVER` (installed Paperclip v0.3.1).
Company: `dcb9fb2c-78cb-42ee-8a41-87fc6595d5ab`.
CEO: `f63771b3-68ea-4f92-8f9b-8d7cba2679f2`.

## Verified root cause

In `server/src/routes/decisions.ts`, the existing formal Decision queue's list endpoint calls `assertBoard(req)`. The original `POST /decisions/:id/decide` also calls `boardUserId(req)`, which calls `assertBoard(req)`. A CEO agent's heartbeat JWT therefore cannot use either board endpoint. Adding an `AGENTS.md` skill alone cannot change these server-side gates.

## Change in this branch

The fork gains a **separate, opt-in scoped agent API**, not an impersonated board session.

- `GET /api/companies/:companyId/ceo-decision-queue?limit=50` — lists open Decisions for a *single configured company* to the *single configured CEO* using a genuine agent-run JWT. For board-only cards it returns **metadata only**. For eligible routine cards it also returns the body and option labels. The board UI and original board-only APIs are untouched.
- `POST /api/companies/:companyId/ceo-decisions/:id/decide` — permits the configured CEO to select an option on **only** an effect-free, explicitly tagged routine coordination card. Body: `{ "optionId": "proceed", "rationale": "10+ character reason", "idempotencyKey": "unique-uuid-or-scoped-key" }`.
- Uses Paperclip's existing company agent authorization check and requires a genuine heartbeat JWT, matching agent, company and run. This is not a board token.
- Records `delegatedCeoDecision` with CEO agent ID, run ID, rationale, and authority in Decision metadata and adds `decision.agent_routine_decided` activity attributed to the agent. For compatibility, legacy `decidedByUserId` stores a **namespaced** `agent:<uuid>` sentinel; this is not an actual user or a board approval. Consider a first-class `decidedByAgentId` schema migration before broader deployment.
- Existing signed-spec validation, decision claiming, idempotency, expiry and wake-origin-agent continuation remain handled by the original service.

**Eligibility is fail-closed**:
- exact `ruleKey: "project_billion.routine_coordination.v1"`;
- `metadata: { "kind": "routine_coordination" }` and no extra metadata keys;
- no effect in **any** option, no dynamic input fields, no target snapshots, no bundle;
- decision is open and unexpired, origin agent must be different from CEO;
- standard agent authorization must allow queue access/management;
- no direct broker order, issue mutation, credential change, budget change, archive, approval execution or board permissions.

This changes only routine **recorded coordination votes**. A result may wake the requesting agent, but is **not** an authorization to bypass its own operation's security and review requirements.

## Opt-in configuration

The feature is **off** unless the Paperclip server process explicitly sets:

```sh
PAPERCLIP_CEO_DECISIONS_MODE=read
PAPERCLIP_CEO_DECISIONS_COMPANY_ID=dcb9fb2c-78cb-42ee-8a41-87fc6595d5ab
PAPERCLIP_CEO_DECISIONS_AGENT_ID=f63771b3-68ea-4f92-8f9b-8d7cba2679f2
```

Start in `read` mode. After the full tests and a controlled harmless interaction pass, switch to `routine` to enable the narrow POST endpoint. `off` (or unset) denies both. **No live-money, PAPER_ONLY, risk, credential or broker settings are changed.**

These settings belong in the trusted Paperclip service environment, not in agent `AGENTS.md`, the GitHub repository, or a chat-visible credential. They are configuration values, not passwords, but configuration changes should remain auditable.

## Routine decision producer contract

From a genuine **issue-scoped** Engineer/Analyst/Trader/Fund Manager heartbeat, create a Decision with:

```json
{
  "title": "Which approved test sequence should we run first?",
  "body": "Both choices are existing authorized local test workflows; no effect is executed by this card.",
  "ruleKey": "project_billion.routine_coordination.v1",
  "metadata": { "kind": "routine_coordination" },
  "options": [
    { "id": "proceed", "label": "Run existing unit tests first", "effects": [] },
    { "id": "revise", "label": "Run existing smoke tests first", "effects": [] }
  ],
  "continuationPolicy": "wake_origin_agent",
  "idempotencyKey": "unique-caller-key"
}
```

The actual Decision creation API requires the origin agent to have a genuine issue-scoped run. Do not create a test decision using synthetic IDs, raw SQL, or borrowed board credentials.

## Architect1 installation procedure for Hermes

1. From `/home/architect/PAPERCLIP_NEWPORT_RIVER`, inspect `git status --short`, `git remote -v`, version and current service ownership. Back up configuration and DB using the existing verified backup process. Do **not** overwrite the dirty installed checkout.
2. Fetch `feature/ceo-scoped-decisions-v1` from the fork and create a **separate test worktree** pinned to its current commit. Preserve existing `paperclip.service` and production listeners.
3. Run `pnpm --filter @paperclipai/server typecheck` and `pnpm exec vitest run --config server/vitest.config.ts server/src/services/ceo-decision-delegation.test.ts`. Fix defects on this branch; do not falsely report an unrun test as passing.
4. Exercise the feature in a **separate test instance** using a separate database and port: default off => 403; scoped read mode returns expected metadata for CEO => 200; other agents, forged/runless and other-company actors => 403; old board endpoints unchanged.
5. Use an authentic issue-scoped Engineer heartbeat to create one harmless routine coordination Decision. Under a genuine CEO heartbeat in `routine` mode, read, choose an eligible option, post rationale + idempotency key, confirm server status and audit, then verify the origin agent resumes. Check replay and expiry behavior.
6. Attempt a **nonempty-effect** test Decision, an archive proposal, a bundle, and a self-originated Decision: all must remain board-only. Board-only Decisions and Approvals must not become agent-actionable.
7. Only after acceptance, schedule an authorized maintenance change on the installed Paperclip service from the tested branch, with backup, single supervised process tree, health check and rollback plan. Do not change systemd unit startup blindly. Preserve the local modifications via worktrees/patches rather than resetting them.
8. Add the CEO queue scan to existing heartbeat instructions (no daemon or persistent JWT). Read queue metadata each heartbeat, decide only bounded routine cards, otherwise escalate via proper board UI or issue interaction.
9. Report actual branch SHA, build/tests, API responses, Decision ID, audit event, continuation evidence, deployment state, and exact remaining blockers.

## Failure mode and release limitation

This patch is a narrow operator-controlled extension, **not** an upstream generalized agent-approval mechanism. The legacy `decidedByUserId` compatibility sentinel requires integration testing against decision UI display, recovery and retention code paths before deployment. An alternative production design is a proper `decidedByAgentId` field with a DB migration and agent-aware audit/recovery. If runtime tests expose this as incompatible, do not enable `routine`; preserve read-only queue access and implement the schema migration first.

All formal Decisions outside the exact routine contract remain board-only. Agents cannot approve their own governed actions or substitute this endpoint for human or board approvals.
