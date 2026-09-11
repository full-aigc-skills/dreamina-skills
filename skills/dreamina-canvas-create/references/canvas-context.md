# Canvas context and identity

## State owned by this Skill

- `projectId` — lowercase canonical UUID. The only identity used by all
  downstream node, operation, and resource calls.
- Local contexts file — `dreamina-canvas/contexts/<profile-and-environment>.json`,
  mode `0600`, holding the `--use` choice. Owned by the CLI; this Skill
  never edits it directly.

## Idempotent create pattern

```bash
PROJECT_ID=$(uuidgen | tr 'A-Z' 'a-z')
mkdir -p .state
echo "$PROJECT_ID" > .state/project-id

dreamina-canvas --format json canvas create "<name>" \
  --project-id "$PROJECT_ID" --use
```

## Reuse across processes

Always read `.state/project-id` (or its environment-specific equivalent) on
startup and pass it explicitly to every downstream command. Never rely on
the contexts file in cross-process flows; it may be missing, stale, or
written by a sibling process.

## Concurrency rules

- Two processes may share the same `projectId` safely **only** when neither
  one passes `--use` and every node / operation / resource call includes
  the explicit `--project-id`.
- Two processes must **not** both write to the contexts file. The contexts
  file is single-writer.
- Two processes must **not** auto-generate different `projectId`s and then
  race on the same logical canvas — pick one process to mint the id, the
  rest must read it.

## Listing

`canvas ls --limit <n> --offset <n>` paginates. Treat each page as
best-effort; canvases may be created or removed between calls. When piping
into other commands, pipe the raw `projectId` value, never a retyped copy.

## Failure → recovery

| Failure | requiredAction | What to do next |
|---------|----------------|-----------------|
| `canvas create` returns exit 2 with an invalid `projectId` | none | The id was empty or not lowercase canonical UUID; regenerate and retry with the explicit value. |
| `canvas create` returns exit 13 | upgrade | Upgrade the CLI per `error.clientUpgrade.upgradeUrl`. |
| A response carries a different `projectId` than the request | n/a | Stop and surface; never overwrite the persisted id. |
| Concurrent writes to the contexts file | n/a | Refactor to pass `--project-id` explicitly and stop using `--use`. |

## What this Skill will not do

- Invent a `projectId` other than the one the caller persisted.
- Auto-mint a `projectId` on the caller's behalf inside a multi-step flow.
- Echo, log, or persist the contexts file path with sensitive content.
