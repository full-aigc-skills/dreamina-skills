---
name: dreamina-canvas-generate-video
description: Use when an agent or script must save or run a Dreamina Canvas video node with mode t2v, first_last_frame, or m2v. Never accepts i2v or multi_modal as a mode. Preserves user-requested ratios only when the discovered model contract permits them.
license: Complete terms in LICENSE
---

# Dreamina Canvas Video Node

This Skill owns the **Canvas video node**. It exists so that video
references, modes, and ratio constraints are correct without confusing
`i2v` (which does not exist) with `m2v`, or `multi_modal` (a server
internal alias) with the public mode set.

Reference detail is in
[references/video-node-contract.md](references/video-node-contract.md).

## When to use

- The caller wants to save a video draft (t2v, first_last_frame, or m2v).
- The caller wants to edit an existing video node, including replacing
  the entire generation block.
- The caller wants to switch modes on an existing draft and needs the
  reference rules explained.

## When **not** to use

- For approving or running generation — that is `dreamina-canvas-quote-and-run`.
- For the audio track of a video — that is `dreamina-canvas-generate-audio`.

## Modes — the public set

```text
t2v               text-to-video
first_last_frame  one or two ordered frames
m2v               image / video / Element / multimodal guidance
```

There is **no `i2v` mode**. The server-internal alias `multi_modal` must
not be passed; the CLI rejects it with exit code 2. Image-to-video,
video-guided generation, Element references, and "single image to video
with a preserved ratio" all use `m2v`.

```bash
# t2v
dreamina-canvas --format json node create video \
  --prompt "<prompt>" \
  --mode t2v --model <m> --ratio <r> --resolution <res> --duration 5

# first_last_frame (one frame)
dreamina-canvas --format json node create video \
  --prompt "<transition prompt>" \
  --mode first_last_frame --model <m> \
  --ref node:<firstFrameNodeId> --duration 5

# first_last_frame (two frames)
dreamina-canvas --format json node create video \
  --prompt "<transition prompt>" \
  --mode first_last_frame --model <m> \
  --ref node:<firstFrameNodeId> --ref node:<lastFrameNodeId> --duration 5

# m2v (image / video / Element guidance)
dreamina-canvas --format json node create video \
  --prompt "<motion prompt>" \
  --mode m2v --model <m> \
  --ref node:<imageOrVideoNodeId> --duration 5
```

## `--duration`

Mandatory for any video draft in seconds, must be `> 0`, default 5.
Take the upper bound from the discovered model spec; do not invent.

## `--ratio`

Some video models reject an explicit `--ratio` (for example, image- and
frame-driven modes follow the source frame ratio). Discovery wins; if the
model spec says the ratio is inferred from the first frame, do **not**
pass `--ratio`.

## `first_last_frame` rules

- One or two `--ref` entries are allowed.
- When two frames are supplied the source ratios of the two images must
  match.
- The output ratio is determined by the **first** frame; passing two
  frames with mismatched ratios is rejected by the server.

## Reference rules

Same surface as `dreamina-canvas-generate-image`:

- `node:node_xxx` — follow the node (canvas edge).
- `res:<lowercase UUID>` — freeze to a specific resource.
- `uri:` / `vid:` — reserved, rejected.
- Internal short links (`video_xxx`, `image_xxx`) — rejected.

Video nodes may reference Image, Element, or Video nodes/resources.

## Generation is a full replace

Identical to image:

- Touching `--mode`, `--model`, `--ratio`, `--resolution`, `--duration`,
  `--count`, `--prompt`, `--ref` requires the **complete** new block.
- Metadata is sparse; only the flags you pass are updated.
- `--clear-generation` is the opt-out (mutually exclusive with
  generation flags).

## Paid execution is not this Skill's job

Hand off to `dreamina-canvas-quote-and-run`. This Skill never calls
`--run`, never sets `--credit-ceiling` or `--credit-token`, never
persists tokens.

## Failure → recovery

| Failure | requiredAction | What to do next |
|---------|----------------|-----------------|
| `--mode i2v` rejected (exit 2) | none | Switch to `m2v`. |
| `--mode multi_modal` rejected (exit 2) | none | Switch to `m2v`. |
| Two-frame `first_last_frame` ratios disagree (exit 2) | none | Pick two frames with matching source ratios. |
| Explicit `--ratio` rejected by the model (exit 2) | none | Re-run discovery; remove `--ratio` if the model infers from the first frame. |
| Missing `--duration` (exit 2) | none | Pass `--duration` (default 5, model bound applies). |

## What this Skill will not do

- Approve spend.
- Persist tokens, signed URLs, cookies, or session material.
- Accept `i2v` or `multi_modal` as a mode.
- Treat generation edits as a partial update.

## Policy

Invocation requires:
- Confirmed installation of dreamina-canvas
- Live model discovery result for video
- For paid execution: explicit handoff to dreamina-canvas-quote-and-run

Forbids:
- Passing --mode i2v or --mode multi_modal
- Calling --run from this Skill
- Supplying --credit-ceiling or --credit-token
- Persisting tokens, signed URLs, cookies, or session material

Default prompt:

> Public video modes are t2v, first_last_frame, m2v. There is no i2v and
> no multi_modal --mode value. When the user says 'image to video' or
> wants to preserve a ratio, use m2v. Hand off paid execution.
>
