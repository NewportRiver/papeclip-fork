# Engineering Decisions

## D-001 — Keep fork-specific engineering memory separate from upstream product docs

Status: accepted

The fork retains upstream `doc/` contracts and adds `engineering/` for NewportRiver-specific durable state, development history, and recovery-oriented records. This avoids rewriting upstream intent while making the fork restartable for our workflows.

## D-002 — Record evidence class on operational claims

Status: accepted

Records distinguish repository-derived facts, live runtime evidence, and planned/contract behavior. A source document or feature inventory is not evidence that a live provider, database, browser, or adapter run succeeded.

## D-003 — Use additive backfill, not mass rewriting

Status: accepted

Existing README, AGENTS, product, implementation, database, deployment, release, skills, and test documents remain authoritative. The engineering framework links to them and summarizes verified facts rather than duplicating or replacing them.

## D-004 — Preserve control-plane/execution-plane separation

Status: accepted

Paperclip governs company work and records execution; adapters own external runtime invocation. Hermes integration follows the same boundary.
