# Audio node contract

## TTS

Public 1.0.3 shapes `tts` in three forms (live schema is authoritative):

```bash
# Legacy: voice-driven, no model
dreamina-canvas --format json node create audio \
  --prompt "<text to speak>" \
  --mode tts \
  --voice-name "<public-voice-name>"

# Scenario: explicit model + scenario
dreamina-canvas --format json node create audio \
  --prompt "<text to speak>" \
  --mode tts \
  --model "<scenario-capable-model>" \
  --scenario text-reading \
  --voice-name "<public-voice-name>"

# Omni-dubbing: optional single catalog voice and/or audio references
dreamina-canvas --format json node create audio \
  --prompt "<dubbing script or intent>" \
  --mode tts \
  --model "<scenario-capable-model>" \
  --scenario omni-dubbing \
  --voice-name "<optional-single-catalog-voice>" \
  --ref "node:<audioNodeId>"
```

- Legacy: required `--voice-name`; `--model` without `--scenario` is
  rejected. The CLI resolves the public name server-side.
- `--scenario` is `text-reading | omni-dubbing`, requires `--mode tts` and
  an explicit `--model`.
- `text-reading` keeps `--voice-name` mandatory.
- `omni-dubbing` makes `--voice-name` optional (a single catalog voice,
  converted server-side into an audio reference) and accepts repeatable
  typed `--ref` audio references (`node:` / `res:`), sharing the
  reference limits reported by discovery.
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
| `--voice-name` (TTS) | `voice list --offset 0 --count 50`, optionally narrowed with `--model <canonical-model>`; keep the same model while paginating; paginate until `nextOffset` is absent. |
| `--model` (scenario TTS) | Live audio discovery; only models the payload marks as scenario-capable. Never a remembered name. |
| `--model` (music) | Use the full audio payload from `model search --detail full` or `model list`, whichever schema declares, then filter to `music` mode. |

A remembered name from another environment or older CLI commit is not
authoritative.

## Paid execution

Hand off to `dreamina-canvas-cli`. This operation never calls
`--run`.

## Failure → recovery

| Failure | requiredAction | What to do next |
|---------|----------------|-----------------|
| `cli.audio_music_model_required` (exit 2) | none | Re-discover; pass a `MODE=music` model. |
| `--voice-name` rejected (exit 2) | none | Re-enumerate voices; pick a current public name. |
| `--model` without `--scenario` on tts (exit 2) | none | Remove `--model`, or add `--scenario` with a scenario-capable model. |
| `--scenario` without `--model` (exit 2) | none | Pass an explicit scenario-capable model from live discovery. |
| `--ref` outside omni-dubbing (exit 2) | none | Remove `--ref`, or switch to `--scenario omni-dubbing`. |
| `--voice-name` on music (exit 2) | none | Remove `--voice-name`; supply `--model`. |
| `--count` on audio (exit 2) | none | Remove `--count`. |
| Missing `--duration` on music (exit 2) | none | Pass `--duration`. |

## What this operation will not do

- Approve spend.
- Persist tokens, signed URLs, cookies, or session material.
- Accept `--count` on audio nodes.
- Use a remembered voice / music-model name across environments.
