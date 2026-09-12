# Canvas DAG composition

## Pattern: top-down construction

```text
user prompt
   │
   ▼
Text node(s)            ← optional, supply reusable context
   │
   ▼
Element node(s)         ← follow_node for live subjects; frozen_resource for snapshots
   │
   ▼
Image / Video / Audio   ← --ref node:<textNodeId> / node:<elementNodeId>
   │
   ▼
Timeline node           ← --clip <image|video nodeId>, --audio-clip <music resource UUID>
```

Each level persists the returned `nodeId` keyed by a stable caller alias.
Never re-use a `nodeId` you only remember from a previous run.

## Reference rules (recap)

| Slot | Syntax |
|------|--------|
| `--ref` on Image / Video / Audio / Timeline | `node:node_xxx` or `res:<uuid>` |
| Element `--main`, `--voice`, `--auxiliary` | bare `node_xxx` or bare `<uuid>` (no prefix) |
| Element `--description` | free text |
| Prompt placeholder | `{{node:node_xxx}}` or `{{res:<uuid>}}` |

`uri:` / `vid:` are reserved and rejected by the server.

## DAG batching for `node run`

`node run` does not schedule DAGs. Build explicit layers:

```text
layer 0: nodes with no incoming node: refs
layer 1: nodes whose node: refs all live in layer 0 (or earlier)
layer 2: ...
```

For each layer:

1. Persist the set of `nodeId`s as a batch.
2. Hand off to `dreamina-canvas-quote-and-run` for the quote → confirm →
   run cycle (one ceiling per layer is normal; mixing layers in one
   batch blurs the approval boundary).
3. Persist each layer's `submitId` and wait for terminal state via
   `dreamina-canvas-resume-operation` before quoting the next layer.
4. Download each layer's resources via `dreamina-canvas-download-assets`
   if needed.

## Default-only-save contract

Saving a node never implies running it. This Skill only writes drafts;
paid execution is a separate user-authorised step.

## Failure → recovery

| Failure | requiredAction | What to do next |
|---------|----------------|-----------------|
| `nodeId` returned differs from what you expected | none | Stop; re-read the response and treat the saved id as authoritative. |
| `node:` prefix passed to an Element slot | none | Strip the prefix; pass bare id or UUID. |
| `res:<uuid>` with uppercase or stripped dashes | none | Reformat to lowercase canonical UUID. |
| Downstream reference rejected | none | Verify the upstream `nodeId` is persisted and reused verbatim. |

## What this Skill will not do

- Approve spend, call `--run`.
- Persist tokens, signed URLs, cookies, or session material.
- Mint a `submitId` (that is the quote-and-run Skill's job).
- Schedule the DAG server-side.
- Re-derive a `nodeId` from anything other than the create response.
