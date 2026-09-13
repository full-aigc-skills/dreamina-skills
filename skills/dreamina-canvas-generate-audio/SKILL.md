---
name: dreamina-canvas-generate-audio
description: Use when an agent or script must save or run a Dreamina Canvas audio node in either TTS or music mode. Forbids --count, requires --voice-name for TTS, and refuses an implicit default model for music.
license: Complete terms in LICENSE
---

# Dreamina Canvas Audio Node

This Skill owns the **Canvas audio node**. The two modes (`tts`, `music`)
have opposite field requirements, and a missing or wrongly-applied field
is rejected with `cli.audio_music_model_required` (exit code 2) for music
or with the mode-specific contract for TTS.

Reference detail is in
[references/audio-node-contract.md](references/audio-node-contract.md).

## When to use

- The caller wants to synthesize speech from text (TTS).
- The caller wants to generate a music clip from a prompt (music).
- The caller wants to switch an existing audio node from one mode to
  the other and needs the field set explained.

## When **not** to use

- For approving or running generation — that is `dreamina-canvas-quote-and-run`.
- For the visual track of an audio-bearing composition — that is
  `dreamina-canvas-manage-timeline`.

## TTS

```bash
dreamina-canvas --format json node create audio \
  --prompt "<text to speak>" \
  --mode tts \
  --voice-name "<discovered-voice>"
```

- `--voice-name` is mandatory. The CLI resolves the public name into the
  authoritative server-side identifier.
- `--model` is **forbidden** for TTS; the model is selected from the
  voice's underlying TTS model, not user-supplied.

## Music

```bash
dreamina-canvas --format json node create audio \
  --prompt "<music prompt>" \
  --mode music \
  --model "<music-model-from-discovery>" \
  --duration 30
```

- `--model` is mandatory. Take it from the live full audio discovery shape
  selected by schema (`model search --detail full` or `model list`), filtered
  to a `music` mode entry.
- `--voice-name` is **forbidden** for music.
- `--duration` must be `> 0` seconds; default 30.
- The CLI refuses to default the music model. A missing `--model`
  returns `cli.audio_music_model_required` (exit code 2). Do not retry
  with a name remembered from a different environment.

## Field exclusivity

| Mode | Required | Forbidden |
|------|----------|-----------|
| `tts` | `--voice-name` | `--model` |
| `music` | `--model`, `--duration > 0` | `--voice-name` |

`--count` is **not** accepted on audio nodes — a single output only.

## Generation is a full replace

Same as image / video: touching generation flags means submitting the
complete new block. Metadata is sparse. `--clear-generation` is the
opt-out and is mutually exclusive with generation flags.

## Paid execution is not this Skill's job

Hand off to `dreamina-canvas-quote-and-run`. This Skill never calls
`--run`, never sets `--credit-ceiling` or `--credit-token`, never
persists tokens.

## Failure → recovery

| Failure | requiredAction | What to do next |
|---------|----------------|-----------------|
| `cli.audio_music_model_required` (exit 2) | none | Re-run the schema-selected full audio discovery command, pick a `music` model, retry. |
| `--voice-name` rejected on TTS | none | Re-run `voice list`; add `--language` only if schema declares it. |
| `--model` passed on TTS (exit 2) | none | Remove `--model`; let the voice drive the model. |
| `--voice-name` passed on music (exit 2) | none | Remove `--voice-name`; supply `--model` instead. |
| `--count` passed on audio (exit 2) | none | Remove `--count`; audio is single-output. |
| Missing `--duration` on music (exit 2) | none | Pass `--duration` from the discovery bound. |

## What this Skill will not do

- Approve spend.
- Persist tokens, signed URLs, cookies, or session material.
- Accept `--count` on audio nodes.
- Use a remembered voice or music-model name across environments.
- Implicit-default the music model.

## Policy

Invocation requires:
- Confirmed installation of dreamina-canvas
- Live voice list (for TTS) or live audio model discovery (for music)
- For paid execution: explicit handoff to dreamina-canvas-quote-and-run

Forbids:
- Calling --run from this Skill
- Passing --count on audio nodes
- Supplying --model on TTS or --voice-name on music
- Implicit-defaulting the music model
- Persisting tokens, signed URLs, cookies, or session material

Default prompt:

> TTS requires --voice-name; music requires --model + --duration. Never
> pass --count on audio nodes. Never default the music model. Hand off
> paid execution to dreamina-canvas-quote-and-run.
>
