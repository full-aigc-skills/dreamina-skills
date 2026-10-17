# dreamina-canvas CLI contract (seed)

This is the seed contract used by the Canvas Skills. Runtime truth comes from
the installed binary:

```bash
dreamina-canvas --format json version
dreamina-canvas --format json schema
```

Recorded live probes (edition `public`, distribution `cn`):

- 2026-09-05, commit `ae2c968` — initial public 1.0.0 seed.
- 2026-10-17, commit `244064d`, version `1.0.3`, build
  `2026-10-14T03:28:54Z` — adds the `node delete` family
  (confirm/status), paired `--x`/`--y` placement flags, node
  `--tag`/`--clear-tags`, `--dry-run`, `--resource-source`, `voice list
  --model`, `node find --name/--tag`, and the audio `--scenario`
  (`text-reading` | `omni-dubbing`) contract.

- Global flags (place before the subcommand): `--format`, `--non-interactive`,
  `--yes`, `--profile`, `--region`.
- Command families: `auth`, `model`, `voice`, `canvas`, `node`, `operation`,
  `resource`, `schema`, `version`.
- Output envelope (success):
  `{"schemaVersion": "1", "ok": true, "data": {...}}`
- Output envelope (failure, written to stderr): `{"ok": false, "error": {...}}`.
- Project, resource and submit IDs are canonical UUIDs; node IDs are opaque node_ identifiers returned by the CLI, never generated as UUIDs.

The authoritative fixture is `verification/dreamina-canvas-guide-contract.json`
in the repository root. Do **not** copy values from this document into tests;
treat `dreamina-canvas schema` as the only valid source for the current
binary.
