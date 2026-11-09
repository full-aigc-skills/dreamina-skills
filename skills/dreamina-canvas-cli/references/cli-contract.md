# dreamina-canvas CLI contract (seed)

This is the seed contract used by the Canvas Skills. Runtime truth comes from
the installed binary:

```bash
dreamina-canvas --format json version
dreamina-canvas --format json schema
```

Original recorded probe (commit `ae2c968`, edition `public`, distribution `cn`,
build `2026-09-05T08:54:32Z`); a 2026-11-09 read-only probe found local
public cn 1.2.0 (`cee4f27a`). New capabilities and version boundary are in
[new-capabilities.md](new-capabilities.md):

- Global flags (place before the subcommand): `--format`, `--non-interactive`,
  `--yes`, `--profile`, `--region`.
- Original command families: `auth`, `model`, `voice`, `canvas`, `node`,
  `operation`, `resource`, `schema`, `version`. Local 1.2.0 also declares
  `team`, `space` and `director`.
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
