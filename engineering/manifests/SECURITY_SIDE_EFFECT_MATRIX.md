# Security and Side-Effect Matrix

Status: repository-derived design baseline; live enforcement remains unverified until Paperclip is run.

| Boundary | Default | Requires approval | Evidence required |
|---|---|---|---|
| Source/catalog/document read | allow | no | source path/query |
| Generated index/manifest update | allow on branch | no | generator output and diff |
| Local test/worktree mutation | allow in isolation | no | test output and cleanup |
| Git commit | restricted | task authorization | diff, checks, commit |
| Git push/PR | restricted | explicit task authorization | remote ref/PR URL |
| Database migration | restricted | explicit approval | migration output and backup |
| External provider invocation | restricted | explicit approval | redacted run evidence and cost |
| Connector/MCP access | deny by default | per-connector approval | allow/ask/deny trace |
| Production deployment | deny by default | human approval | health, rollback, audit record |
| Credential read/export | deny | never through agent context | use provider/auth mechanism |

## Required controls

- Secrets are never stored in catalogs, manifests, logs, or evidence.
- Fake adapters and fixtures precede live provider tests.
- Destructive actions require an isolated data root and rollback plan.
- Stop/pause/recovery paths must be tested before long-running autonomy.
- Runtime claims require command output, health response, test result, or trace.
- Android is treated as an operator/recovery node; server execution is a later deployment target.
