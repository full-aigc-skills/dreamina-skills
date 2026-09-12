# Video node contract

## Public mode set

| Mode | Allowed references | Notes |
|------|--------------------|-------|
| `t2v` | text nodes only | Text-to-video. |
| `first_last_frame` | 1 or 2 image / image-resource / Element refs | Two frames must have matching source ratios. |
| `m2v` | image / video / Element / resource refs | Image-to-video, video guidance, Element guidance, and "preserve ratio" all use `m2v`. |

`i2v` does not exist; `multi_modal` is the server-internal alias and must
not be passed. Both are rejected with exit code 2.

## Required flags

- `--mode` — mandatory for any video draft.
- `--model` — from `model search --type video --detail full`.
- `--ratio` — only when the model spec allows it (some m2v / image-driven
  models infer the ratio from the first frame; do **not** pass `--ratio`
  in those cases).
- `--resolution` — when the model spec declares it required.
- `--duration` — seconds, `> 0`, default 5. Use the model spec's bound.
- `--prompt` — required for any generation edit.
- `--ref` — required for `first_last_frame` (one or two) and `m2v`.

## Reference syntax

- `node:node_xxx` — follow the node; creates a canvas edge.
- `res:<lowercase UUID>` — freeze to a specific resource; no edge.
- `uri:` / `vid:` — reserved; rejected.
- Internal short links (`video_xxx`, `image_xxx`) — rejected.

## Two-frame rule

When `first_last_frame` is given two `--ref` entries, the source ratios
of the two images must match. Mismatched ratios are rejected by the
server. The output ratio is determined by the **first** frame.

## Generation edit (full replace)

```bash
dreamina-canvas --format json node edit video \
  --node-id <nodeId> \
  --prompt "<new prompt>" --mode m2v \
  --model <m> --ratio <r> --resolution <res> --duration <n> \
  --ref node:<upstreamId>
```

Missing flags are cleared. Metadata is sparse.

## Paid execution

Hand off to `dreamina-canvas-quote-and-run`. This Skill never calls
`--run`.

## Failure → recovery

| Failure | requiredAction | What to do next |
|---------|----------------|-----------------|
| `--mode i2v` rejected | none | Use `m2v`. |
| `--mode multi_modal` rejected | none | Use `m2v`. |
| Two-frame `first_last_frame` ratios disagree | none | Pick frames with matching ratios. |
| Explicit `--ratio` rejected | none | Re-discover; if the model infers from the first frame, omit `--ratio`. |
| Missing `--duration` | none | Pass `--duration` from the model spec. |

## What this Skill will not do

- Approve spend.
- Persist tokens, signed URLs, cookies, or session material.
- Accept `i2v` or `multi_modal`.
- Treat generation edits as partial.
