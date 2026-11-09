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
- 2026-11-09, version `1.3.0`, commit `c6a5530a` — adds the `workflow`
  family. Team, space, director and post-processing commands appeared in
  intermediate releases; see [new-capabilities.md](new-capabilities.md).

- Global flags (place before the subcommand): `--format`, `--non-interactive`,
  `--yes`, `--profile`, `--region`.
- Original command families: `auth`, `model`, `voice`, `canvas`, `node`,
  `operation`, `resource`, `schema`, `version`. Local 1.3.0 also declares
  `team`, `space`, `director` and `workflow`.
- Output envelope (success):
  `{"schemaVersion": "<current>", "ok": true, "data": {...}}`.
  The inspected 1.3.0 binary returns `schemaVersion: "2"`; consumers must
  read the current schema instead of assuming the original `"1"`.
- Output envelope (failure, written to stderr): `{"ok": false, "error": {...}}`.
- Project, resource and submit IDs are canonical UUIDs; node IDs are opaque node_ identifiers returned by the CLI, never generated as UUIDs.

The historical 1.0.x seed fixture is
`verification/dreamina-canvas-guide-contract.json` in the repository root.
Do **not** use it as the current release contract; treat `dreamina-canvas schema`
as the only valid source for the installed binary.
