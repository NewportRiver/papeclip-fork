# Adapters, Hermes, and Plugins Domain Manifest

Evidence: repository-derived/structural. Runtime: unverified.

## Owning areas
- `adapters/`
- `packages/` adapter/plugin packages
- Hermes-related adapter and gateway smoke-test paths
- `server/src/vendor/paperclip-runner/`

## Responsibilities
Translate Paperclip task/run contracts to external agent runtimes, including Hermes, custom processes, HTTP endpoints, plugins, skills, output capture, stop behavior, and error normalization.

## Security boundary
Credentials remain outside catalogs and documentation. Adapter invocation must declare side effects, workspace, timeout, stop mechanism, output limits, and cost/accounting behavior.

## Verification
Planned: AU-015 manifest, AU-035 fake adapter, AU-037 Hermes local/gateway recipe, AU-043 adapter engineer skill.

## Gaps
Live provider behavior, gateway reachability, and cancellation semantics require a dependency-enabled isolated environment.
