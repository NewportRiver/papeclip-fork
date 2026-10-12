# Domain Manifest Schema

Every Paperclip domain manifest is a bounded, evidence-labeled map from intent to implementation and verification.

Required sections:

- `Purpose` and non-goals
- `Ownership and boundaries`
- `Entry points`
- `Files and markers`
- `Dependencies and reverse dependents`
- `Data/schema/migration relationships`
- `Configuration and secrets`
- `Invariants and state transitions`
- `Tests and operation recipes`
- `Security and side-effect boundaries`
- `Evidence and review commit`
- `Known gaps`

Use source-relative paths and marker IDs from `engineering/markers/MARKER_INDEX.json`. Every claim must be labeled `repository-derived`, `structural`, `inferred`, `runtime-verified`, `planned`, or `blocked`.

A manifest is complete when a fresh agent can locate the owning implementation, identify prerequisites and risks, and select the smallest relevant verification command without reading the whole repository.
