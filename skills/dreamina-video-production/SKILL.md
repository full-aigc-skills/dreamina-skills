---
name: dreamina-video-production
description: Use when creating a complete Dreamina video project from a local reference video, including analysis, redesign or authorized replication, batch generation, evaluation, audio, subtitles, composition, recovery, and verified export.
---

# Dreamina Video Production

Orchestrate one reference video into one verified final MP4. Every step below is
a separate Dreamina tool call; the project ledger is the only source of truth
for what has already happened.

## Example request

```text
Use dreamina-video-production with /approved/input.mp4 in original-redesign mode.
Show the complete storyboard, task count, model specifications, and maximum credit
ceiling before requesting one whole-batch approval. Do not submit paid work yet.
```

## 能力边界说明

### ✅ 能做

- Create and resume a private, versioned video project.
- Analyze a local reference video into shots, frames, contact sheets, and a typed recut.
- Plan exact Dreamina requests, quote the whole batch, and activate one non-expandable allowance.
- Execute, evaluate, compose, verify, and export the result with a comparison report.

### ⚠ 需要素材

- A local reference video inside an approved root.
- Enrolled trusted media tools (`ffmpeg`, `ffprobe`, and optionally `whisper` and a narration provider).
- Native confirmation for enrollment, rights, whole-batch approval, and export.

### ❌ 超出范围

- Do not call `ffmpeg`, `ffprobe`, or any local binary directly. Only the project tools may.
- Do not assert rights on the user's behalf. Only the user's literal assertion is recorded.
- Do not resubmit a paid request. `Submitted`, `Querying`, and `Unknown` are query-only.
- Do not treat a Jimeng Web link as Seedance completion.

## Workflow

1. **Read status first.** Call `dreamina_video_project` with `action=runtime_status`,
   then `action=get` for an existing project. Never guess the current state.
2. **Enroll tools when required.** `action=enroll_media_tools` is a native-gated side
   effect. It binds each executable by absolute path, owner, and digest.
3. **Seed and analyze.** `dreamina_analyze_reference_video` with `action=seed` copies the
   source under containment; `frames`, `sheets`, and `recut` derive versions from it.
4. **Annotate via the specialist.** Hand contact sheets to
   `dreamina-shot-annotator`. Persist only through
   `dreamina_validate_shot_analysis`, which refuses a stale machine fingerprint.
5. **Design.** `dreamina_create_redesign`. `original_redesign` replaces expressive
   content; `authorized_replication` additionally requires a complete, unexpired,
   scope-matching rights assertion.
6. **Quote, then approve.** `dreamina_quote_video_batch` returns the exact request
   fingerprints and the total credit ceiling. `dreamina_approve_video_batch` activates
   one whole-batch allowance after native confirmation. An activated batch can only
   reduce work.
7. **Execute.** `dreamina_execute_video_batch` with `run_next`, `reconcile`, or `resume`.
   `reconcile` never submits.
8. **Evaluate via the specialist.** Measure first, then hand the measurement to
   `dreamina-video-evaluator`. The same semantic payload must never serve as both
   the design intent and the acceptance verdict.
9. **Compose, verify, export.** `dreamina_compose_video`, then
   `dreamina_export_video_project`, which verifies every required gate before it
   touches the destination.

## Gate signals

- `PreviewValidated` / analysis version: local, deterministic evidence.
- `JimengLinkReady`: a web handoff finished. Never Seedance completion.
- `Submitted` / `Querying` / `Unknown`: paid, query-only.
- `Completed`: only after a downloaded artifact was independently re-hashed.

## Never do

- Never skip the status read before a transition.
- Never let one semantic payload serve as both design and acceptance verdict.
- Never claim a skipped gate passed.
