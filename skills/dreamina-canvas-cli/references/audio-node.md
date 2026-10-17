# audio 节点共享机制

本文件维护节点引用、编辑和清空机制；模式必填项以对应 dreamina-canvas-cli 任务技能的 parameter-reference 为唯一来源。下列模式形态用于解释共享机制。

This operation owns the **Canvas audio node**. The two modes (`tts`, `music`)
have opposite field requirements, and a missing or wrongly-applied field
is rejected with `cli.audio_music_model_required` (exit code 2) for music
or with the mode-specific contract for TTS.

Reference detail is in
[references/audio-node-contract.md](../references/audio-node-audio-node-contract.md).

## When to use

- The caller wants to synthesize speech from text (TTS).
- The caller wants to generate a music clip from a prompt (music).
- The caller wants to dub content with a chosen voice or reference audio
  material (omni-dubbing scenario, public 1.0.3).
- The caller wants to switch an existing audio node from one mode to
  the other and needs the field set explained.

## When **not** to use

- For approving or running generation — that is `dreamina-canvas-cli`.
- For the visual track of an audio-bearing composition — that is
  `dreamina-canvas-cli`.

## TTS

Public 1.0.3 shapes `tts` in three forms; the live schema is authoritative:

```bash
# Legacy TTS: voice drives the model; --model is not supplied
dreamina-canvas --format json node create audio \
  --prompt "<text to speak>" \
  --mode tts \
  --voice-name "<discovered-voice>"

# Scenario TTS: explicit model + scenario
dreamina-canvas --format json node create audio \
  --prompt "<text to speak>" \
  --mode tts \
  --model "<scenario-capable-model-from-discovery>" \
  --scenario text-reading \
  --voice-name "<discovered-voice>"

# Omni-dubbing: voice OR reference audio material
dreamina-canvas --format json node create audio \
  --prompt "<dubbing script or intent>" \
  --mode tts \
  --model "<scenario-capable-model-from-discovery>" \
  --scenario omni-dubbing \
  --voice-name "<optional-single-catalog-voice>" \
  --ref "node:<audioNodeId>"
```

- Legacy TTS requires `--voice-name`. The CLI resolves the public name into
  the authoritative server-side identifier; a `--model` without
  `--scenario` is rejected.
- `--scenario` (`text-reading` | `omni-dubbing`) requires `--mode tts` and
  an explicit `--model` selected from live audio discovery.
- For `text-reading`, `--voice-name` remains mandatory.
- For `omni-dubbing`, `--voice-name` is an **optional single catalog
  voice** converted server-side into an audio reference; the alternative
  (or complement) is `--ref` typed audio references (`node:` / `res:`),
  repeatable, sharing the reference limits that discovery reports.

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

| Form | Required | Forbidden / optional |
|------|----------|----------------------|
| `tts` (legacy) | `--voice-name` | `--model` (without `--scenario`) |
| `tts` + `--scenario text-reading` | `--model`, `--scenario`, `--voice-name` | — |
| `tts` + `--scenario omni-dubbing` | `--model`, `--scenario` | `--voice-name` optional (single catalog voice); `--ref` allowed (audio references) |
| `music` | `--model`, `--duration > 0` | `--voice-name` |

`--count` is **not** accepted on audio nodes — a single output only.

## Generation is a full replace

Same as image / video: touching generation flags means submitting the
complete new block. Metadata is sparse. `--clear-generation` is the
opt-out and is mutually exclusive with generation flags.

```bash
# Sparse metadata edit; generation remains unchanged
dreamina-canvas --format json node edit audio \
  --node-id <nodeId> --title "<new title>"
```

## Paid execution is not this operation's job

Hand off to `dreamina-canvas-cli`. This operation never calls
`--run`, never sets `--credit-ceiling` or `--credit-token`, never
persists tokens.

## Failure → recovery

| Failure | requiredAction | What to do next |
|---------|----------------|-----------------|
| `cli.audio_music_model_required` (exit 2) | none | Re-run the schema-selected full audio discovery command, pick a `music` model, retry. |
| `--voice-name` rejected on TTS | none | Re-run `voice list` (optionally narrowed with `--model`); add other flags only if schema declares them. |
| `--model` passed on legacy TTS without `--scenario` (exit 2) | none | Either remove `--model` (legacy voice-driven path) or add `--scenario` with a scenario-capable model from live discovery. |
| `--scenario` passed without `--model` (exit 2) | none | Pick a scenario-capable model from live audio discovery and pass it explicitly. |
| `--ref` passed outside omni-dubbing (exit 2) | none | Remove `--ref`, or switch to `--scenario omni-dubbing` with an explicit model. |
| `--voice-name` passed on music (exit 2) | none | Remove `--voice-name`; supply `--model` instead. |
| `--count` passed on audio (exit 2) | none | Remove `--count`; audio is single-output. |
| Missing `--duration` on music (exit 2) | none | Pass `--duration` from the discovery bound. |

## What this operation will not do

- Approve spend.
- Persist tokens, signed URLs, cookies, or session material.
- Accept `--count` on audio nodes.
- Use a remembered voice or music-model name across environments.
- Implicit-default the music model.

## Policy

Invocation requires:
- Confirmed installation of dreamina-canvas
- Live voice list (for TTS) or live audio model discovery (for music)
- For paid execution: explicit handoff to dreamina-canvas-cli

Forbids:
- Calling --run from this operation
- Passing --count on audio nodes
- Supplying --model on TTS without --scenario, or --voice-name on music
- Implicit-defaulting the music model
- Persisting tokens, signed URLs, cookies, or session material

Default prompt:

> Legacy TTS requires --voice-name; scenario TTS adds an explicit --model
> plus --scenario (text-reading keeps --voice-name, omni-dubbing takes an
> optional voice or --ref audio references). Music requires --model +
> --duration. Never pass --count on audio nodes. Never default the music
> model. Hand off paid execution to dreamina-canvas-cli.
>
