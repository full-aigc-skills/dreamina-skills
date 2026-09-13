---
name: dreamina-canvas-discover-models
description: Use when an agent must look up the live set of available generation models, voices, ratios, resolutions, durations, batch limits, and per-model requirements for the dreamina-canvas CLI. Never accepts hard-coded model or voice names from outside the current discovery payload.
license: Complete terms in LICENSE
---

# Dreamina Canvas Discovery

This Skill teaches every other `dreamina-canvas-*` Skill how to ask the CLI
what is currently supported. It exists so that no caller hard-codes model
names, voice names, ratios, resolutions, durations, or batch limits.

Reference detail is in
[references/capability-discovery.md](references/capability-discovery.md).

## When to use

- Before the first generation in any workflow that takes a `--model`,
  `--voice-name`, `--ratio`, `--resolution`, `--duration`, or `--count`.
- Before any audio music generation (must confirm the active environment's
  audio model and that the caller has not cached a name from a different
  environment).
- When a generation fails with "model not found" or a `--voice-name`
  rejection: re-discover rather than retrying with a remembered value.

## When **not** to use

- As a substitute for `dreamina-canvas-cli` argv construction rules.
- To bypass a `--credit-ceiling` decision; discovery tells you the legal
  parameter values, it never approves spend.

## Select commands from the live schema

Run `version` and `schema` before building discovery argv. If `schema`
declares `model search`, use `model search --detail full`. If it declares
`model list` instead, use `model list`; that compatibility shape already
returns per-mode flags, enums, bounds, and reference requirements.

Never send an optional flag merely because a guide mentions it. Pass
`voice list --language <code>` only when the live schema declares it; public
1.0.0 accepts only `--offset` and `--count` for `voice list`.

## Discovery commands

```bash
# Summary catalog (one row per model)
dreamina-canvas --format json model search --type image

# Compatibility shape (only when the live schema declares model list)
dreamina-canvas --format json model list --type image

# Full spec per model (every legal flag, enum, bound, batch limit)
dreamina-canvas --format json model search --type image --detail full

# Single model full spec when you already have a name
dreamina-canvas --format json model <model-id> --type image

# TTS voice catalog (add --language only when the live schema declares it)
dreamina-canvas --format json voice list --offset 0 --count 50

# Argument spec for any subcommand (for the exact flag names)
dreamina-canvas --format json schema "node create image"
```

Use only the model command shape returned by `schema`. With `model search`,
run summary discovery and then `--detail full`; with `model list`, read its
full per-mode specifications directly. Never go from a remembered model name
to generation: the catalog moves.

## What to read from the discovery payload

The live full payload (`model search --detail full` or `model list`, as
declared by schema) is the **only** authoritative source for:

- `--model` identifiers and aliases
- `--ratio` legal values per model
- `--resolution` legal values per model (some require it explicitly)
- `--duration` (video, music)
- `--count` upper bound, taken from `generation.maxBatchGenCount`
- Required references, VIP / entitlement flags (`generation.isVip`,
  `vipConfigs[]`), per-model constraints

For audio:

- TTS `--voice-name` must come from `voice list` or from `model search
  --type audio --detail full`. The CLI resolves the public voice name into
  the server-side authoritative identifier.
- Music `--model` must come from `model search --type audio --detail full`
  filtered to `MODE=music`. Music **does not** use a server-implicit default;
  the CLI refuses `--model` missing with `cli.audio_music_model_required` and
  exit code 2.

## Hard rule: never cache across environments

The discovery payload is per environment (`distribution` × `edition` ×
profile). A model name valid in one environment is not portable to another.

- Re-run `model search --type image --detail full` whenever the active
  profile or environment changes (`dreamina-canvas version` reports
  `distribution` and `edition`; trust them).
- Re-run discovery after any CLI upgrade that bumps `commit`/`buildTime`.

## What this Skill will not do

- Recommend a specific model, ratio, resolution, or voice by name.
- Treat a remembered name as equivalent to a re-discovery.
- Save the discovery payload to a public log, fixture, or example. Use
  placeholders like `<model>` / `<voice-name>` / `<ratio>` instead.

## Policy

Invocation requires:
- Confirmed installation of dreamina-canvas
- Confirmed active profile and environment via dreamina-canvas version

Forbids:
- Hard-coding or recommending a specific model name, voice name, ratio, resolution, duration, or batch count
- Treating a discovery payload from one environment as valid in another
- Saving raw discovery payloads into public logs, fixtures, or examples

Default prompt:

> Before generation, inspect `schema`, then use its declared full model
> discovery shape (`model search --detail full` or `model list`) and `voice
> list` for TTS. Add optional flags only when the live schema declares them.
>
