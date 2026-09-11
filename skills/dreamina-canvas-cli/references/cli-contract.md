# dreamina-canvas CLI contract (seed)

This is the seed contract used by the Canvas Skills. Runtime truth comes from
the installed binary:

```bash
dreamina-canvas --format json version
dreamina-canvas --format json schema
```

Recorded live probe (commit `ae2c968`, edition `public`, distribution `cn`,
build `2026-09-05T08:54:32Z`):

- Global flags (place before the subcommand): `--format`, `--non-interactive`,
  `--yes`, `--profile`, `--region`.
- Command families: `auth`, `model`, `voice`, `canvas`, `node`, `operation`,
  `resource`, `schema`, `version`.
- Output envelope (success):
  `{"schemaVersion": "1", "ok": true, "data": {...}}`
- Output envelope (failure, written to stderr): `{"ok": false, "error": {...}}`.
- Identifiers are lowercase canonical UUIDs.

The authoritative fixture is `verification/dreamina-canvas-guide-contract.json`
in the repository root. Do **not** copy values from this document into tests;
treat `dreamina-canvas schema` as the only valid source for the current
binary.
