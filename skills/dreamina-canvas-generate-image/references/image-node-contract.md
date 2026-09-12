# Image node contract

## Creation

```bash
dreamina-canvas --format json node create image \
  --title "<title>" \
  --prompt "<prompt>" \
  --mode t2i \
  --model <discovered-model> \
  --ratio <discovered-ratio> \
  --resolution <discovered-resolution> \
  --count <1..maxBatchGenCount> \
  [--ref node:<nodeId> | --ref res:<uuid>]...
```

`--mode` may be omitted when no generation parameter is being supplied
yet, but as soon as any generation flag is present, pass `--mode`
explicitly.

## Editing

### Generation edit (full replace)

Any edit that touches `--mode`, `--model`, `--ratio`, `--resolution`,
`--count`, `--prompt`, or `--ref` must include the **complete** new
generation block. The CLI does not merge; missing flags are cleared.

```bash
dreamina-canvas --format json node edit image \
  --node-id <nodeId> \
  --prompt "<new prompt>" \
  --mode t2i \
  --model <m> --ratio <r> --resolution <res> --count <n> \
  --ref node:<upstreamId>
```

### Metadata edit (sparse)

```bash
dreamina-canvas --format json node edit image \
  --node-id <nodeId> \
  --title "<new title>" \
  --description "<new description>" \
  --tag "<tag>"
```

Only the flags you supply are updated. To clear: `--clear-title`,
`--clear-description`, `--clear-tags`.

### Clear generation

```bash
dreamina-canvas --format json node edit image \
  --node-id <nodeId> --clear-generation
```

Mutually exclusive with all generation flags.

## Reference rules

| Reference | Allowed in `t2i`? | Allowed in `i2i`? | Edge created? |
|-----------|-------------------|-------------------|---------------|
| `node:node_xxx` | ❌ | ✅ | ✅ (follows the node) |
| `res:<uuid>` (image / Element / image resource) | ❌ | ✅ | ❌ (frozen) |
| `node:<textNodeId>` | ✅ | ✅ | ✅ |
| `uri:`, `vid:` | ❌ (reserved, rejected) | ❌ | n/a |
| Internal short links (`image_xxx`, etc.) | ❌ | ❌ | n/a |

## `i2i` minimum

At least one of:

- `node:node_xxx` of an Image node
- `node:node_xxx` of an Element node whose main / auxiliary is image
- `res:<uuid>` of an image resource

Text references are optional additions.

## Paid execution

This Skill never approves spend. The handoff is:

```text
saved image nodeId + mutationVersion
  → dreamina-canvas-quote-and-run (quote → confirm → run)
  → dreamina-canvas-resume-operation (operation status / wait)
  → dreamina-canvas-download-assets (resource get / download)
```

The `submitId` for run is owned by the quote-and-run Skill; this Skill
never mints or persists it.

## Failure → recovery

| Failure | requiredAction | What to do next |
|---------|----------------|-----------------|
| `cli.invalid_generation_reference` | none | Fix the ref format; never retry with a guessed id. |
| `cli.invalid_resource_reference` | none | An Element slot (--main / --voice / --auxiliary) was given `node:` prefix; strip it. |
| Model or ratio rejected (exit 2) | none | Re-run `model search --type image --detail full`; replace the cached value. |
| `image generation requires --resolution` (exit 2) | none | Pass `--resolution` from the discovery payload. |
| Generation edit lost references because `--ref` was omitted | none | Re-run `node edit image` with the **complete** new ref set. |

## What this Skill will not do

- Approve spend, mint tokens, call `--run`.
- Edit generation as a partial update.
- Pass `multi_modal` or any other server-internal alias to `--mode`.
- Persist tokens, signed URLs, cookies, or session material.
- Reuse remembered model / ratio / resolution names across environments.
