# Node deletion (`node delete`)

This operation owns the destructive removal of canvas nodes. It is a
**confirmation-gated write**: a short-lived token from `node delete confirm`
authorizes the actual delete, and `--yes` can never replace it. Added in
public CLI 1.0.3; only use it when the live schema declares the family.

All shapes below are taken from the CLI's own `schema` output; that output
remains the runtime authority.

## When to use

- The user explicitly asks to delete, remove, or clean up nodes on a canvas.
- A composed graph has obsolete nodes and the user approved their removal.

## When **not** to use

- For undo — deletion is destructive; there is no documented restore.
- For groups: `node delete` does not support group targets. Expand the
  group's member node IDs first if the user wants them gone.
- As a substitute for editing a node's generation parameters.

## The three-step transaction

```bash
# 1. Summarize / execute the batch delete (repeatable --node-id, or comma-
#    separated; deduplicated in order; 1..100 distinct ids)
dreamina-canvas --format json node delete \
  --node-id <nodeId> --node-id <otherNodeId> \
  --project-id "$PROJECT_ID"
# → nodeIds[], updateId, savedDraftVersion, idempotentReplay
#   When confirmation is required, take the returned updateId forward.

# 2. Confirm the batch: mints the short-lived deletion token (in-memory only)
token=$(dreamina-canvas --format json node delete confirm \
  --node-id <nodeId> --node-id <otherNodeId> \
  --update-id "$UPDATE_ID" \
  --project-id "$PROJECT_ID" \
  | jq -r '.data.deleteConfirmationToken') # also note expiresAtMs

# 3. Execute the delete with the token; --update-id MUST be the same value
dreamina-canvas --format json node delete \
  --node-id <nodeId> --node-id <otherNodeId> \
  --update-id "$UPDATE_ID" \
  --delete-token "$token" \
  --project-id "$PROJECT_ID"
```

## Identity rules (read this twice)

- `--update-id` is the stable identity of one deletion batch: generate (or
  accept the CLI-generated value) once, then **reuse the exact same value**
  in confirm, execute, and every retry. Switching to a new update-id turns
  the retry into a new deletion batch.
- `--delete-token` is short-lived (`expiresAtMs` in the confirm payload).
  Keep it in process memory only; never log or persist it. An expired token
  means re-running **confirm with the same update-id**, not a new batch.
- `node delete status` is the read-only reconciliation path: it reports the
  first deletion result for the batch (`found`, `result`,
  `savedDraftVersion`, `idempotentReplay`, optional `error`) without
  minting credentials or deleting anything. Use it after ambiguous or
  timed-out responses before deciding to retry.

## Two confirms, two tokens — do not mix them

| | `node confirm` | `node delete confirm` |
|---|---|---|
| Approves | paid generation (credit ceiling) | destructive node deletion |
| Mints | `creditConfirmationToken` | `deleteConfirmationToken` |
| Bound to | node batch + ceiling | node batch + `--update-id` |
| Consumed by | `node run --credit-token` | `node delete --delete-token` |

A credit token cannot authorize deletion, and a delete token cannot authorize
spend. `--yes` replaces neither.

## Deletion does not free spend by itself

Deleting a node removes canvas structure; it is not a refund or a
cancellation of already-submitted generation tasks. For in-flight tasks,
keep reconciling the original `submitId` via `operation status` / `wait`.

## Failure → recovery

| Failure | Exit / signal | What to do next |
|---------|---------------|-----------------|
| Confirmation required | 10 (`confirm`) | Run `node delete confirm` with the same `--update-id`; show the user what will be removed; then execute with the token. |
| Ambiguous / timed-out response | 20 (`resume`) or transport failure | Run `node delete status` with the same ids; only retry the delete when status proves the batch was not applied. |
| `delete-token` expired | 2 | Re-run `node delete confirm` with the same `--update-id`; reuse the new token. |
| Group id passed to `--node-id` | 2 | Groups are unsupported; expand to member node IDs. |
| Login lost mid-transaction | 11 | Re-authenticate, then continue the **same** update-id batch. |

## What this operation will not do

- Delete without an explicit user-approved batch.
- Persist or log `deleteConfirmationToken`.
- Use `--yes` in place of the deletion token.
- Target groups or assume server-side cascade semantics.

## Policy

Invocation requires:
- Confirmed installation of dreamina-canvas with the `node delete` family
  declared by schema
- A user-approved list of node IDs (never inferred silently)

Forbids:
- Persisting the deletion token or any approval material
- Reusing a credit token for deletion or vice versa
- Minting a fresh update-id to "restart" an unclear deletion
- Deleting nodes the user did not name or approve

Default prompt:

> Node deletion is token-gated: summarize with node delete, mint the token
> via node delete confirm with the same --update-id, execute with
> --delete-token, and reconcile uncertain outcomes via node delete status.
> Never let --yes replace the token.
>
