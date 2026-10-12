# Test Status

## Verified

- Git checkout and fork remote inspected.
- Existing documentation/source references used by the engineering guide were confirmed present.
- New engineering files are Markdown and contain no intentional credentials.
- Before this pass, `git diff --check` passed for the engineering guide.

## Not run

- `pnpm install` — pnpm is unavailable on the current host.
- `pnpm typecheck`
- `pnpm test` / `pnpm test:run`
- `pnpm build`
- `pnpm db:check`/migration checks
- browser/e2e suites
- Docker build and server health checks

## Required verification after prerequisites

```sh
pnpm install
pnpm -r typecheck
pnpm test:run
pnpm build
pnpm db:migrate
pnpm dev:once
curl http://localhost:3100/api/health
```

Run narrower checks first for a targeted change. Treat external-provider smoke tests as separate from core build verification.
