---
name: dreamina-canvas-compose
description: Use when an agent or script must save a multi-node Canvas graph (Text, Element, Image, Video, Audio, Timeline) for later approval, without performing any paid execution. Owns dependency order and batch planning.
license: Complete terms in LICENSE
---

# Dreamina Canvas Composition

This Skill owns the **non-charging** side of Canvas structure. It saves
nodes in dependency order, persists every returned `nodeId`, and hands off
the run to `dreamina-canvas-quote-and-run` after the user has reviewed the
full graph.

Reference detail is in
[references/composition-dag.md](references/composition-dag.md).

## When to use

- The caller wants to assemble a Canvas with multiple nodes of different
  types and explicit dependencies.
- The caller wants a saved, runnable DAG before approving any spend.
- The caller wants explicit run batches (because `node run` does not do
  DAG scheduling on its own).

## When **not** to use

- For actually running the graph — that is
  `dreamina-canvas-quote-and-run` after this Skill saves the structure.
- For a single media node — call `dreamina-canvas-generate-image` /
  `…video` / `…audio` directly.

## Default-only-save contract

Saving a node never implies running it. This Skill never:

- Calls `--run`.
- Sets `--credit-ceiling` or `--credit-token`.
- Persists tokens.
- Approves spend on the user's behalf.

The composed canvas is **only** the saved structure. Paid execution is a
separate step the user must explicitly authorise.

## Dependency order

Create upstream nodes **before** downstream ones that reference them.
The returned `nodeId` from an upstream node becomes the `--ref
node:<nodeId>` of a downstream node.

```text
Element / Text / Image (referenced by downstream nodes)
  → Image / Video / Audio (consume the references)
    → Timeline (consumes the visual / audio references)
```

The Skill persists every returned `nodeId` keyed by a stable caller
alias. Never re-derive a `nodeId` from memory — read it from the response.

## Text and Element commands

This Skill owns non-generating Text and Element structure:

```bash
dreamina-canvas --format json node create text \
  --title "<title>" --text "<body>"
dreamina-canvas --format json node edit text \
  --node-id <textNodeId> --text "<new body>"

dreamina-canvas --format json node create element \
  --title "<title>" --main <imageNodeId>
dreamina-canvas --format json node edit element \
  --node-id <elementNodeId> --voice <audioNodeId> \
  --auxiliary <otherImageNodeId>
```

Element slots accept bare Node IDs or resource UUIDs, not `node:`/`res:`
syntax. Validate every binding against the live schema and resolved media type;
do not duplicate one image in both main and auxiliary slots.

## Locate and inspect nodes

Use `node find` for filtered summaries and `node show` for full views before
composing references:

```bash
dreamina-canvas --format json node find --type image --status success --limit 50
dreamina-canvas --format json node show --node-id <nodeId>
```

## Reference syntax on the canvas

- `node:node_xxx` — follow the node; creates a canvas edge. Used in
  `--ref` for Image / Video / Audio / Timeline nodes, and inside prompt
  placeholders `{{node:node_xxx}}`.
- `res:<lowercase UUID>` — frozen reference; no edge. Used when the
  caller wants to pin a specific resource rather than follow a node.
- Element slot bindings (`--main`, `--voice`, `--auxiliary`,
  `--description`) take **bare** node ids or lowercase UUIDs. Do **not**
  prefix with `node:` / `res:`; the CLI rejects with
  `cli.invalid_resource_reference`.
- `uri:` / `vid:` — reserved, rejected.

## Element vs frozen resource

Element bindings have two modes (the response's `bindingMode` echoes
which one was chosen):

| Input | Meaning | `bindingMode` |
|-------|---------|---------------|
| `node_xxx` | follow the source node; reference tracks regeneration | `follow_node` |
| `<lowercase UUID>` | freeze to the resource at write time | `frozen_resource` |

If you have a node id but want to freeze the resource as of "now", do:

```bash
RES_ID=$(dreamina-canvas --format json node show --node-id <nodeId> \
  | jq -r '.data.resourceId')
# then pass $RES_ID (bare) into the slot
```

This Skill documents the rule; binding creation is owned by
`dreamina-canvas-generate-image` / `…video` etc.

## DAG scheduling is the caller's job

`node run` does not perform DAG scheduling. The Skill must build explicit
topological run batches before any paid execution:

1. Group nodes by layer: layer 0 has no incoming `node:` references,
   layer N+1 only references layers `≤ N`.
2. Submit each layer as one `node run` invocation with the
   corresponding `--node-id` set.
3. Persist each layer's `submitId` and wait for terminal state before
   the next layer (see `dreamina-canvas-resume-operation`).
4. Hand each layer to `dreamina-canvas-quote-and-run` with the user's
   approved ceiling.

## Failure → recovery

| Failure | requiredAction | What to do next |
|---------|----------------|-----------------|
| `node create` returns a different `nodeId` than expected | none | Stop; re-read the response, treat as contract violation. |
| Downstream reference (`node:<id>`) rejected | none | Verify the upstream `nodeId` was persisted and reused exactly. |
| `node:foo` passed to an Element slot | none | Strip the `node:` prefix; pass bare id or resource UUID. |
| `multi_modal` or `i2v` passed to a video node | none | Switch to `m2v` / correct public mode. |

## What this Skill will not do

- Approve spend or call `--run`.
- Persist tokens, signed URLs, cookies, or session material.
- Mint a `submitId`; the run batches only describe which nodeIds to
  quote / confirm / run.
- Schedule the DAG server-side; it does not happen.

## Policy

Invocation requires:
- Confirmed installation of dreamina-canvas
- A user-approved canvas structure plan
- For paid execution: explicit handoff to dreamina-canvas-quote-and-run

Forbids:
- Calling --run from this Skill
- Supplying --credit-ceiling or --credit-token
- Persisting tokens, signed URLs, cookies, or session material
- Assuming node run performs DAG scheduling
- Re-deriving a nodeId from memory; always read it from the response

Default prompt:

> Compose the canvas as a saved graph. Create upstream nodes before
> downstream references. Persist every nodeId. Plan explicit run
> batches because node run does not perform DAG scheduling. Hand off
> paid execution to dreamina-canvas-quote-and-run.
>
