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
