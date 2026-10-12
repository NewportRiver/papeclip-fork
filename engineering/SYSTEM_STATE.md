# System State

## Source state

- Fork remote: `https://github.com/NewportRiver/papeclip-fork.git`
- Upstream lineage: `paperclipai/paperclip`
- Baseline inspected: `0ce8f4c7349f4a87be10c4f0eeecdcb80cd83ca7`
- Upstream-derived tag at the prior baseline: `canary/v2026.1011.0-canary.12`
- Root package version is not declared; workspace packages currently report `0.3.1`.

## Runtime state

Not exercised in this pass. The repository requires Node >=24.11 and pnpm 9+. The host has Node v26.2.0 and lacks pnpm.

## Durable state domains

1. Git source and engineering records.
2. PostgreSQL control-plane state and migrations.
3. Local/object storage for assets and instance data.
4. Encrypted secrets or external secret-manager references.
5. Agent workspace/runtime service state.
6. External provider and connector state.
7. Hermes state when the Hermes adapter is used.

A source checkout alone is not a complete restore.

## Verification state

- Repository orientation: verified from files and Git.
- Documentation references: verified during prior guide pass.
- Markdown framework: source-written; registry refresh and Git validation pending.
- Dependency installation: not run.
- Typecheck/build/unit/e2e/server health: not run in this environment.
