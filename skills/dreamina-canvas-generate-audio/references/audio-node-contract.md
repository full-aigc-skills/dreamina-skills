# Audio node contract

## TTS

```bash
dreamina-canvas --format json node create audio \
  --prompt "<text to speak>" \
  --mode tts \
  --voice-name "<public-voice-name>"
```

- Required: `--voice-name`. The CLI resolves the public name server-side.
- Forbidden: `--model`.
- Output: a single audio resource (no batch).

## Music

```bash
dreamina-canvas --format json node create audio \
  --prompt "<music prompt>" \
  --mode music \
  --model "<music-model-from-discovery>" \
  --duration 30
```

- Required: `--model` from the schema-selected full audio discovery payload,
  filtered to `music` mode; `--duration > 0` seconds, default 30.
- Forbidden: `--voice-name`.
- Output: a single audio resource (no batch).

## Cross-mode rules

- `--count` is not accepted on audio nodes.
- Switching modes on an existing node is a full generation replace —
  re-supply the **complete** new block (prompt + mode + required fields).
- `--clear-generation` is the opt-out; mutually exclusive with generation
  flags.

## Discovery requirements

| Field | Source |
|-------|--------|
| `--voice-name` (TTS) | `voice list --offset 0 --count 50`; add `--language` only if schema declares it, and paginate until `nextOffset` is absent. |
| `--model` (music) | Use the full audio payload from `model search --detail full` or `model list`, whichever schema declares, then filter to `music` mode. |

A remembered name from another environment or older CLI commit is not
authoritative.

## Paid execution

Hand off to `dreamina-canvas-quote-and-run`. This Skill never calls
`--run`.

## Failure → recovery

| Failure | requiredAction | What to do next |
|---------|----------------|-----------------|
| `cli.audio_music_model_required` (exit 2) | none | Re-discover; pass a `MODE=music` model. |
| `--voice-name` rejected (exit 2) | none | Re-enumerate voices; pick a current public name. |
| `--model` on TTS (exit 2) | none | Remove `--model`. |
| `--voice-name` on music (exit 2) | none | Remove `--voice-name`; supply `--model`. |
| `--count` on audio (exit 2) | none | Remove `--count`. |
| Missing `--duration` on music (exit 2) | none | Pass `--duration`. |

## What this Skill will not do

- Approve spend.
- Persist tokens, signed URLs, cookies, or session material.
- Accept `--count` on audio nodes.
- Use a remembered voice / music-model name across environments.
