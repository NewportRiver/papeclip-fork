# Engineering Fundamentals

These principles adapt the Hermes engineering fundamentals to Paperclip's control-plane architecture.

1. Evidence before claims. Distinguish repository-derived facts, live runtime evidence, and planned behavior.
2. Control plane versus execution plane. Paperclip governs and records; adapters invoke external runtimes.
3. Company boundaries are mandatory. Every business record, route, agent key, skill, connector, and activity path must enforce the correct company/instance scope.
4. Contracts stay synchronized. Schema, shared types, server services, UI clients, adapters, docs, and tests move together when behavior crosses layers.
5. Durable state is explicit. Source, database, object storage, secrets references, workspaces, and runtime configuration have separate recovery responsibilities.
6. Smallest safe change first. Use the narrowest workflow, targeted verification, and additive documentation before broad refactors.
7. No hidden autonomy. Heartbeats, schedules, budgets, approvals, retries, pause state, and recovery must remain inspectable.
8. Stop is a first-class operation. Cancellation must preserve verified stop evidence and must not silently replay tool calls.
9. Secrets never enter logs, Markdown, fixtures, task text, or Git history.
10. Generated artifacts are not proof. A dashboard, registry, or report must point to the source evidence that produced it.
11. Backward compatibility is deliberate. Migrations, adapter protocols, and public APIs require explicit compatibility and rollback reasoning.
12. A change is not complete until it is exercised or its verification blocker is recorded plainly.

## Development Skill: Markdown Registry Maintenance

The Markdown registry is a core development method, not decorative documentation. It gives engineers and agents a current navigation map of the repository's manuals, contracts, plans, skills, tests, release notes, and durable engineering records.

Use this skill when:

- adding or removing Markdown documentation
- creating a new engineering plan, manifest, runbook, skill, or decision record
- changing documentation entry points or repository structure
- reconciling source changes with their operational and engineering documentation
- preparing a branch for fresh-session handoff or recovery

Required workflow:

1. Edit the authoritative Markdown source, not the generated registry.
2. Run:

   ```sh
   python3 engineering/scripts/refresh_md_registry.py
   ```

3. Inspect the generated diff for unexpected files, duplicate/incorrect headings, or transient artifacts.
4. Run `git diff --check`.
5. Confirm new durable documents are linked from the appropriate entry point (`README.md`, `AGENTS.md`, or `engineering/README.md`).
6. Update `CURRENT_WORK.md`, `TEST_STATUS.md`, `JOURNAL.md`, or a decision/bug record when the change affects durable project state.
7. Commit the source document and regenerated registry together.

Rules:

- `engineering/MASTER_MD_REGISTRY.md` is generated navigation metadata, not the source of truth.
- The registry must not be hand-edited.
- Historical documents remain historical; do not rewrite them merely to make the index appear current.
- Do not index secrets, generated logs, credentials, or transient runtime output as durable documentation.
- A registry entry proves a file exists and is indexed; it does not prove the documented behavior works.
- Pair registry coverage with tests, executable recipes, or runtime evidence when making capability claims.
- Regenerate after material Markdown changes and before branch handoff/review.

The registry is especially valuable for agentic development: an agent can discover the correct contract, plan, skill, test, or recovery document before modifying code, while preserving a bounded context window and a traceable source path.
