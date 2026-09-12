---
name: dreamina-canvas-manage-timeline
description: Use when an agent or script must build or edit a Dreamina Canvas timeline (visual clips and audio clips). Warns before track replacement because the server drops uncommitted changes and regenerates clip identities.
license: Complete terms in LICENSE
---

# Dreamina Canvas Timeline

This Skill owns the Canvas timeline node. A timeline has two tracks: a
visual track (`--clip`) and an audio track (`--audio-clip`). The most
common surprise is that **passing either flag rebuilds the corresponding
track**, throwing away any unsaved work and reissuing clip identities.

Reference detail is in
[references/timeline-contract.md](references/timeline-contract.md).

## When to use

- The caller wants to assemble a video with both visual and audio tracks
  on the canvas.
- The caller wants to swap an individual clip with explicit trim / speed
  / volume options.
- The caller wants a metadata-only edit (title / tags) without touching
  the tracks.

## When **not** to use

- For video generation parameters — that is `dreamina-canvas-generate-video`.
- For audio generation parameters — that is `dreamina-canvas-generate-audio`.
- For approval or paid execution — that is `dreamina-canvas-quote-and-run`.

## Create

```bash
dreamina-canvas --format json node create timeline --title "<title>" \
  --clip <visualNodeId1> \
  --clip <visualNodeId2>,trim=1000-4000,speed=2 \
  --clip <imageNodeId>,duration=3000 \
  --audio-clip <musicResourceId>,start=0,volume=0.5
```

- Either `--clip` or `--audio-clip` (or both) must be supplied on creation.
- An audio-only timeline is valid; the server adds an empty visual track
  for the canvas to remain consistent.

## Clip options

`--clip` and `--audio-clip` accept a comma-separated option list:

| Option | Applies to | Unit | Default |
|--------|------------|------|---------|
| `duration=<ms>` | image clips | milliseconds | canvas default image duration |
| `trim=<start>-<len>` | video / audio | milliseconds | full source duration |
| `speed=<factor>` | video / audio | multiplier | 1 |
| `volume=<0-1>` / `muted` | video / audio | boolean / fraction | full |
| `start=<ms>` | audio clips | milliseconds | 0 |

Omitted options are left empty and the server fills them in from the
source asset. Never guess duration or trim locally.

## Track replacement is destructive

This is the rule that trips every first-time caller:

> Supplying either `--clip` or `--audio-clip` to `node edit timeline`
> **rebuilds the corresponding track**. The server deletes the existing
> clips, re-creates them per the supplied list, and issues **new clip
> identities**. Any unsaved per-clip edits the user had on the original
> timeline are lost.

Before calling `node edit timeline` with either flag, the Skill must:

1. Confirm the user wants a full track replacement (not metadata-only).
2. Confirm the user accepts that clip identities will change.
3. Build the **complete** new list for the affected track; do not
   attempt to "add a clip" by mixing old and new.

If only the title / tags / description needs to change, do **not** pass
either `--clip` or `--audio-clip`.

## Metadata-only edit

```bash
dreamina-canvas --format json node edit timeline \
  --node-id <nodeId> \
  --title "<new title>"
```

Sparse update; the tracks are untouched.

## Clear tracks

```bash
dreamina-canvas --format json node edit timeline \
  --node-id <nodeId> \
  --clear-tracks
```

Mutually exclusive with `--clip` and `--audio-clip`.

## Reference syntax on the timeline

- `--clip` and `--audio-clip` take **bare** node IDs (`node_xxx`) or
  lowercase canonical UUIDs for resources. Do **not** use the `node:` or
  `res:` prefix — those return `cli.invalid_resource_reference` (exit 2).

## Paid execution

Hand off to `dreamina-canvas-quote-and-run`. This Skill never calls
`--run`.

## Failure → recovery

| Failure | requiredAction | What to do next |
|---------|----------------|-----------------|
| `node_xxx` rejected on `--clip` / `--audio-clip` | none | Verify the bare ID; do not add `node:` prefix. |
| Two frames disagree on ratio | none | Confirm `trim` / `duration` units are in milliseconds. |
| `--clip` / `--audio-clip` accidentally included in a metadata-only edit | human_intervention | Surface to the user that the track was rebuilt; this is irreversible from the client. |

## What this Skill will not do

- Approve spend.
- Persist tokens, signed URLs, cookies, or session material.
- Pass `node:` or `res:` prefix on `--clip` / `--audio-clip`.
- Silently merge old and new clip lists; track replacement is destructive
  and the user must consent.
- Guess missing options locally; let the server fill them from the source.
