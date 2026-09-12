# Timeline contract

## Creation

```bash
dreamina-canvas --format json node create timeline \
  --title "<title>" \
  --clip <bare-node-or-uuid>[,option=value]... \
  --audio-clip <bare-node-or-uuid>[,option=value]...
```

Either track flag must be supplied at least once on creation. An
audio-only timeline is valid; the server fills the visual track with an
empty placeholder.

## Editing

### Track replacement (destructive)

```bash
dreamina-canvas --format json node edit timeline \
  --node-id <nodeId> \
  --clip <new-list> \
  --clip <new-list> \
  [--audio-clip <new-list> ...]
```

The server deletes every existing clip on each track that received at
least one flag and rebuilds from scratch. Clip identities are re-issued.
**Unsubmitted per-clip edits on the original timeline are lost.**

### Track replacement warning checklist

Before calling, the Skill must answer "yes" to all of:

1. The user explicitly asked for a track replacement.
2. The user understands the original clip identities are gone.
3. The new list is complete (no implicit "carry over the old ones").

If any answer is "no" or unknown, do not pass either flag.

### Metadata-only edit (safe)

```bash
dreamina-canvas --format json node edit timeline \
  --node-id <nodeId> \
  --title "<new title>" \
  --tag "<tag>"
```

Sparse update; both tracks untouched.

### Clear tracks

```bash
dreamina-canvas --format json node edit timeline \
  --node-id <nodeId> \
  --clear-tracks
```

Mutually exclusive with `--clip` and `--audio-clip`.

## Clip option reference

| Option | Source type | Unit | Default |
|--------|-------------|------|---------|
| `duration=<ms>` | image | ms | canvas default image duration |
| `trim=<start>-<len>` | video / audio | ms | full source duration |
| `speed=<factor>` | video / audio | multiplier | 1 |
| `volume=<0-1>` | video / audio | fraction | 1 |
| `muted` | video / audio | flag | unset |
| `start=<ms>` | audio | ms | 0 |

Omitted options are empty; the server fills them from the source asset.

## Reference format on the timeline

- `--clip` and `--audio-clip` take a **bare** node id (`node_xxx`) or a
  lowercase canonical UUID for a resource.
- Do **not** add the `node:` or `res:` prefix; the CLI returns
  `cli.invalid_resource_reference` (exit 2).
- For visual clips use video or image node IDs (or image-resource UUIDs).
- For audio clips use music resource UUIDs (or audio node IDs).

## Audio-only timeline

When only `--audio-clip` is supplied (and no `--clip`), the CLI accepts
the draft and the server inserts an empty visual track. This is the
documented pattern for "audio-only composition".

## Paid execution

Hand off to `dreamina-canvas-quote-and-run`. The timeline node is paid
execution only when paired with `--run`; this Skill never calls that.

## Failure → recovery

| Failure | requiredAction | What to do next |
|---------|----------------|-----------------|
| `--clip` / `--audio-clip` reject a bare id | none | Verify the id; remove any `node:` / `res:` prefix. |
| Track replacement accidentally issued | human_intervention | Surface to the user; the replacement is irreversible from the client. |
| Missing options not filled by the server | none | Pass the options explicitly or re-check the source asset's metadata. |

## What this Skill will not do

- Approve spend.
- Persist tokens, signed URLs, cookies, or session material.
- Pass `node:` or `res:` prefix on `--clip` / `--audio-clip`.
- Silently merge old and new clip lists.
- Guess missing options locally.
