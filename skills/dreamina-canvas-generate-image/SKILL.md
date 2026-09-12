---
name: dreamina-canvas-generate-image
description: "Use when an agent or script must save or run a Dreamina Canvas image node (t2i or i2i), compose ordered node: and res: references, separate generation edits from sparse metadata edits, and hand off paid execution to dreamina-canvas-quote-and-run."
license: Complete terms in LICENSE
---

# Dreamina Canvas Image Node

This Skill owns the **Canvas image node** — saving drafts, editing, and
the transition into the paid chain. It does **not** approve spend; that
is `dreamina-canvas-quote-and-run`.

Reference detail is in
[references/image-node-contract.md](references/image-node-contract.md).

## When to use

- The caller wants to save or update an image node, with or without
  references to other nodes or resources.
- The caller wants to switch from `t2i` to `i2i` (or back) on an existing
  draft.
- The caller wants to clear generation without losing the node identity.

## When **not** to use

- For approving or running generation — that is `dreamina-canvas-quote-and-run`.
- For author-only prompt guidance — the existing `dreamina-prompt-*`
  Skills own that.

## Modes

```bash
# Text-to-image draft (no spend)
dreamina-canvas --format json node create image \
  --title "<title>" --prompt "<prompt>" \
  --mode t2i --model <model> --ratio <ratio> --resolution <resolution> \
  --count <n>

# Image-to-image draft; at least one image-bearing ref is required
dreamina-canvas --format json node create image \
  --prompt "<prompt>" --mode i2i --model <model> \
  --ref node:<sourceNodeId>
# or
dreamina-canvas --format json node create image \
  --prompt "<prompt>" --mode i2i --model <model> \
  --ref res:<frozenResourceUuid>
```

`--mode` may be omitted only when the references make it unambiguous. As
soon as any generation parameter changes, pass `--mode` explicitly.

## References (`--ref`)

Every `--ref` is `type:value`. Two types are first-class for image
generation:

| Type | Meaning | Behaviour |
|------|---------|-----------|
| `node:node_xxx` | Reference the latest resource of the named node | The reference becomes a canvas edge; if the source is regenerated the reference follows. |
| `res:<lowercase UUID>` | Freeze to a specific resource | No edge; immune to source regeneration. |

`uri:` and `vid:` are reserved and currently rejected by the server.

### Reference rule per mode

- `t2i`: text inputs allowed; **image, Element, or resource references are
  not accepted**.
- `i2i`: at least one **Image, Element, or image resource** reference is
  required. Text references are allowed additionally.

## Prompt placeholders

`{{type:value}}` inside `--prompt` becomes a reference when the placeholder
is mentioned in the prompt text. Mixing prompt placeholders with explicit
`--ref` flags deduplicates by first occurrence (prompt order, then
`--ref` order).

To write a literal `{{`, double it: `{{{{`. The placeholder survives a
round-trip through `node show`; the saved value can be passed directly
back into the next `node edit --prompt`.

## Generation is a full replace; metadata is sparse

This is the single most-confused rule in the Canvas suite.

- **Generation edit** (changing `--mode`, `--model`, `--ratio`,
  `--resolution`, `--count`, `--prompt`, `--ref`): you **must** provide
  the **complete** new generation block. Omitting a parameter clears it.
- **Metadata edit** (title / description / tags): sparse; only the flags
  you pass are updated.
- **Clear generation**: `--clear-generation` (only valid on `node edit`),
  mutually exclusive with all generation flags.

```bash
# Full generation replacement (must include all generation flags)
dreamina-canvas --format json node edit image \
  --node-id <nodeId> \
  --prompt "<new prompt>" --mode t2i \
  --model <m> --ratio <r> --resolution <res> --count <n> \
  --ref node:<upstreamId>

# Sparse metadata edit
dreamina-canvas --format json node edit image \
  --node-id <nodeId> \
  --title "<new title>"

# Clear generation
dreamina-canvas --format json node edit image \
  --node-id <nodeId> --clear-generation
```

## Paid execution is not this Skill's job

`node create image --run` (or the `quote → confirm → run` chain) is paid
execution. Always hand off to `dreamina-canvas-quote-and-run`. This Skill
never:

- Calls `--run` itself.
- Supplies `--credit-ceiling` or `--credit-token`.
- Persists `credit-approval token`.

## Failure → recovery

| Failure | requiredAction | What to do next |
|---------|----------------|-----------------|
| `cli.invalid_generation_reference` (exit 2) | none | Fix the reference: add `node:` or `res:` prefix; lowercase canonical UUID for resource; no internal short links. |
| Model or ratio not in discovery payload (exit 2) | none | Re-run `model search --type image --detail full` and use the current names. |
| Reference required (i2i without an image ref) | none | Add at least one `node:` or `res:` of an image / Element / image resource. |
| Image generation requires `--resolution` but it is missing (exit 2) | none | Pass `--resolution` from the discovery payload. |

## What this Skill will not do

- Approve spend.
- Persist tokens, signed URLs, cookies, or session material.
- Edit generation as a partial update; missing flags are treated as cleared.
- Pass `multi_modal` (or other server-internal aliases) where the public
  mode is `m2v` / `t2i` / etc.

## Policy

Invocation requires:
- Confirmed installation of dreamina-canvas
- Live model discovery result for image
- For paid execution: explicit handoff to dreamina-canvas-quote-and-run

Forbids:
- Calling --run from this Skill
- Supplying --credit-ceiling or --credit-token
- Persisting credit-approval token, signed URLs, cookies, or OAuth tokens
- Treating generation edit as a sparse update

Default prompt:

> Save image drafts via node create/edit image. Generation edits replace
> the full block; metadata edits are sparse. Hand off paid execution to
> dreamina-canvas-quote-and-run; never pass --run from this Skill.
>
