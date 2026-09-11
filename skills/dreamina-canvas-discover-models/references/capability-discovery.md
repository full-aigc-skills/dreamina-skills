# Capability discovery for dreamina-canvas

## Required pre-flight sequence

```bash
# 1. Confirm binary and environment
dreamina-canvas --format json version

# 2. Confirm active profile
dreamina-canvas --format json auth account

# 3. Discover candidates (summary)
dreamina-canvas --format json model search --type image
dreamina-canvas --format json model search --type video
dreamina-canvas --format json model search --type audio

# 4. Confirm full spec for the chosen model
dreamina-canvas --format json model <model-id> --type image

# 5. For TTS, enumerate voices
dreamina-canvas --format json voice list --language zh-CN --offset 0 --count 50
# continue paginating with --offset <nextOffset> until nextOffset is absent

# 6. Confirm flag names with the live schema
dreamina-canvas --format json schema "node create image"
dreamina-canvas --format json schema "node create video"
dreamina-canvas --format json schema "node create audio"
```

## Per-resource-type notes

### Image

- `--model` / `--ratio` / `--resolution` must come from discovery.
- `--count` upper bound is `generation.maxBatchGenCount`.
- Some image models require `--resolution` explicitly. If the model spec
  declares `resolution` as required, omitting it is rejected with exit code 2.

### Video

- `--mode` is mandatory (`t2v` | `first_last_frame` | `m2v`).
- `--duration` is in seconds, must be `> 0`, default 5.
- `first_last_frame` accepts a single first frame or two ordered frames;
  when two frames are given their source ratios must match.
- The server may document the model mode as `multi_modal`; **never** pass
  `multi_modal` to `--mode`. Use `m2v`.

### Audio (TTS)

- `--voice-name` is mandatory. The CLI resolves the public name to the
  authoritative server-side identifier.
- `--model` is forbidden for TTS.

### Audio (Music)

- `--model` is mandatory; take it from `model search --type audio --detail
  full` filtered to `MODE=music`.
- `--voice-name` is forbidden for music.
- `--duration` is in seconds, must be `> 0`, default 30.
- The CLI refuses to default the music model; a missing `--model` returns
  `cli.audio_music_model_required` and exit code 2.

## VIP and entitlement signals

`model search --detail full` exposes `generation.isVip` and `vipConfigs[]`.
These describe **what the model requires**, not what the active account has.
Do not treat them as a credit balance or membership signal — that comes from
`auth account` plus the live quote response.

## When discovery disagrees with cached memory

Always prefer the discovery payload. Replace any cached value with the new
one and continue. Do not patch the cache and retry.
