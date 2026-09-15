---
name: dreamina-3d-use
description: Route a Dreamina 3D orchestration request to the right workflow. Use when the user wants to turn a DCC preview into a Dreamina render without naming the source DCC.
metadata:
  type: router
  plugin: codex-dreamina-3d
  status: stable
---

# codex-dreamina-3d-use

## When to use

The user wants a Dreamina 3D render but has not specified whether the source
preview comes from Blender or Maya. This Skill routes to the right workflow.

## Three explicit entries

- `preview_only`: produce and validate a local Blender/Maya preview, then stop
  at `PreviewValidated` without web handoff or paid submission.
- `jimeng_web`: delegate to `codex-dreamina-3d-jimeng-web` and stop at
  `JimengLinkReady`. A ready link is not a submitted or Completed Seedance
  artifact.
- `auto_seedance`: delegate to `codex-dreamina-3d-auto-seedance`; require
  approval, submit once, query the same ID, download, and verify before
  `Completed`.

If the user's intent does not distinguish these outcomes, explain them and ask
for one choice. Never silently upgrade a local preview into a web or paid
operation.

## Report availability honestly

State each entry's availability before the user chooses. Do not imply a
capability is production-ready when it is not:

- `preview_only` and `auto_seedance` are production routes on macOS + Blender.
- `jimeng_web` is `OPTIONAL_UNAVAILABLE` whenever the user-installed official
  uploader is absent. Report it as optional and unavailable, never as verified.
  Probe for it; never install or enable it to make the route available.
- `codex-dreamina-3d-from-maya` is **experimental** with runtime status
  `NOT_RUN`. It is fixture-compatible only and is not part of the production
  release. Do not present Maya as production-ready, and do not route a user
  there without saying so.

## Workflow

1. **Discover companions.** Call `discover_companions(search_roots)` from
   `scripts/capability_probe.py`. Do not crawl user directories and do not
   install anything.
2. **Choose the companion.** Call `select_companion(candidates, requested=None)`.
   - zero companions: surface `install_guidance()` and stop.
   - one companion: route to `codex-dreamina-3d-from-blender`, or to
     `codex-dreamina-3d-from-maya` only after flagging it experimental.
   - two companions: ask the user to pick.
3. **Select entry.** Report availability per the section above, then apply the
   explicit route.
4. **Delegate** to the selected bounded Skill and stop.

## Never do

- Never install or modify a companion plugin.
- Never skip the companion detection step.
- Never proceed to Dreamina submission before the preview is validated.
- Never report `jimeng_web` as production-verified while the official add-on is
  absent.
- Never treat `JimengLinkReady` as `Completed`.
- Never present the Maya route as part of the production release.

## Gate signals

- Local preview status: `PreviewValidated` in the job ledger.
- Dreamina submission status: `Submitted | Querying | Unknown` in the ledger.
- Final artifact acceptance: `Completed` (only after `result.sha256` is on
  disk and matches the declared hash).
- Web handoff status: `JimengLinkReady`, or `OPTIONAL_UNAVAILABLE` when the
  official add-on is absent. Neither is Seedance completion.
