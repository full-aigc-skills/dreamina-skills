---
name: dreamina-canvas-create
description: Use when an agent or script must create, list, or select a Dreamina Canvas. Owns the idempotent --project-id rule: every concurrent or cross-process retry must reuse the same lowercase UUID; never depend on the local --use context from another process.
license: Complete terms in LICENSE
---

# Dreamina Canvas Lifecycle

This Skill owns canvas identity. It governs how a canvas is created, listed,
selected, and — most importantly — how the resulting `projectId` is reused
across processes. The `projectId` is the only thing that makes generation
calls idempotent.

Reference detail is in
[references/canvas-context.md](references/canvas-context.md).

## When to use

- Before the first `node create` / `node edit` / `node run` in a workflow that
  must address a specific canvas.
- When an existing canvas needs to be selected for a follow-up run.
- When two concurrent scripts must share a single canvas safely.

## When **not** to use

- For generating nodes (the domain Skills own that).
- For mutating `--use` context without an explicit user request.

## Create rule (read this twice)

```bash
# Generate the idempotency key yourself; do NOT let the CLI generate one
PROJECT_ID=$(uuidgen | tr 'A-Z' 'a-z')

# Persist it before any generation call
echo "$PROJECT_ID" > .state/project-id

# Create the canvas with that project-id; pass --use only when the
# current single-user sequential flow wants it
dreamina-canvas --format json canvas create "我的画布" \
  --project-id "$PROJECT_ID" --use
```

Re-running `canvas create` with the **same** `--project-id` is a no-op that
returns the existing canvas. Switching to a new `--project-id` creates a new
canvas every time.

## `--use` and the local canvas context

`canvas create --use` writes a profile-and-environment-keyed file under
`dreamina-canvas/contexts/<profile-and-environment>.json` containing the
chosen `projectId`. Subsequent commands that omit `--project-id` fall back
to this file.

`--use` is **only** safe when:

- A single user is running a single sequential flow in a single process.
- The caller is willing to discard the default canvas context if it is wrong.

`--use` is **not** safe when:

- Two or more processes may write the contexts file concurrently
  (byte-level interleaving).
- A cross-process retry must reuse the original `projectId` — the contexts
  file may not reflect the original choice by then.
- Concurrent automation needs deterministic identity for every command.

In those cases pass `--project-id <uuid>` explicitly on every call.

## Listing

```bash
dreamina-canvas --format json canvas ls --limit 20
```

`--limit` and `--offset` paginate. Use the returned `projectId` values
verbatim when piping into other commands; do not retype them.

## Failure → recovery

| Failure | requiredAction | What to do next |
|---------|----------------|-----------------|
| `canvas create` returns a different `projectId` than the one passed | n/a | Treat as a contract violation; surface to the user; do not overwrite the persisted id. |
| `canvas ls` returns exit 11 | `login` | Re-authenticate, then re-list. |
| Concurrent processes report the same `projectId` was auto-created | n/a | Stop; one process owns the id and the others must pass it explicitly. |

## What this Skill will not do

- Create a canvas without a caller-supplied `--project-id`.
- Persist OAuth tokens, cookies, signed URLs, or `credit-approval token`.
- Mutate the contexts file outside of an explicit `--use` request.
- Skip re-validation of the live `--project-id` before a paid call.
