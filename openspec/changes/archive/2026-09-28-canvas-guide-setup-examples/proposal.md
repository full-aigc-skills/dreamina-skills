## Why

The supplied first-use Canvas CLI guide exposes a complete setup path and concrete command examples that are currently scattered or absent from the packaged skills. Some existing examples still use older installer and model-discovery syntax.

## What Changes

- Add `dreamina-setup` as the first-use entry for the **Canvas** CLI: platform-specific installation guidance, PATH check, version/schema verification, login, and account readiness.
- Reconcile Canvas command guidance against the supplied guide and the locally installed CLI's read-only `version` and `schema` output. Keep live schema authoritative when guide and binary differ.
- Put task-specific, runnable example shapes in the corresponding Canvas skills, with placeholders for live model values and persistent IDs.
- Update package inventory and tests so the new skill and examples remain discoverable.

## Scope

This change concerns skill source and documentation. It does not install or update the user's CLI, log in, submit generation, spend credits, or publish a release.
