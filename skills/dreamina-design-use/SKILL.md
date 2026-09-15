---
name: dreamina-design-use
description: Thin router Skill for Dreamina Design image and video workflows. Selects between the 13 packaged Dreamina Skills (dreamina-cli-* and dreamina-prompt-*) and never duplicates their prompt or CLI bodies.
---

# dreamina-design-use

This Skill is the **router** for `codex-dreamina-design`. It does **not**
contain prompt templates, CLI invocation recipes, or model catalogs of its
own — every such instruction lives in a separate packaged Dreamina Skill
that this router points to.

## When to use

Invoke this Skill when a user asks Codex to:

* generate or edit a Dreamina image;
* generate a Dreamina video (text-to-video, image-to-video, frames-to-video,
  multimodal-to-video);
* resume an in-flight Dreamina task and download verified artifacts;
* look up the current Dreamina CLI capability snapshot.
* install, authenticate, inspect account readiness, manage Sessions, query
  tasks, download results, or diagnose Dreamina CLI logs through automation.

## MCP automation first

Prefer the packaged `dreamina_design` MCP tools over composing terminal
commands. It exposes capability/status, verified install or upgrade,
memory-only headless authentication flows, account checks, all image/video
modes (including upscale and multi-frame), task query/list/download, Session
CRUD, and redacted diagnostics.

Installation/upgrade, authentication changes, paid generation, and Session
mutations pause for Codex and/or native user confirmation. Never bypass that
pause. Headless login returns a short-lived `flow_id`; use it for
`check_login` and never request or persist a raw device code.

## Routing rules

The router chooses between the 13 packaged Dreamina Skills based on:

| User intent                     | Packaged Skill               |
|---------------------------------|------------------------------|
| text-to-image                   | `dreamina-cli-text2image`    |
| image-to-image                  | `dreamina-cli-image2image`   |
| text-to-video                   | `dreamina-cli-text2video`    |
| image-to-video                  | `dreamina-cli-image2video`   |
| frames-to-video                 | `dreamina-cli`                |
| multimodal / multi-frame video  | `dreamina-cli`                |

If the user's request is ambiguous (matches more than one mode), the
router must refuse to guess and ask for clarification instead.

## Boundaries

* **No hard-coded model or resolution catalog.** Models, resolutions,
  ratios, durations and reference caps come from the live capability
  snapshot produced by `scripts.dreamina_adapter.DreaminaAdapter`.
* **No silent login.** Generation consumes membership benefits or
  credits; every submission must go through
  `scripts/approval_guard.ApprovalGuard` with an explicit
  `ApprovalReceipt`.
* **No web-prerequisite bypass.** The first Dreamina video requires the
  user to acknowledge the web-console prerequisite via
  `scripts.video_service.VideoService.record_web_prerequisite_acknowledgement`.
  Silent bypass is impossible.
* **No blind resubmission.** When a submission outcome is ambiguous,
  `scripts.operation_ledger.OperationLedger.query` is invoked by submit
  ID before any new submission is attempted.
* **Verified packaged instructions.** The router Skill never embeds another
  Skill's body. The 13 complete upstream Skill trees are packaged locally
  and must remain byte-identical to the verified upstream
  `full-aigc-skills/dreamina-skills` commit. Run
  `scripts/verify_skill_snapshot.py` to confirm parity.

## Operational steps

1. Read the live capability snapshot via
   `scripts.dreamina_adapter.DreaminaAdapter.capability_snapshot()`.
2. Choose the packaged Skill per the table above. If no packaged Skill
   matches, refuse and ask the user to clarify.
3. Build the request via `scripts.image_service.ImageService` (image) or
   `scripts.video_service.VideoService` (video) — both reject
   unsupported tokens before any CLI call.
4. Require an `ApprovalReceipt` bound to the canonical SHA-256
   `request_fingerprint` (see
   `scripts.image_service.build_request_fingerprint` /
   `scripts.video_service.build_video_request_fingerprint`).
5. Submit via the argv-only `DreaminaAdapter.run(...)` exactly once per
   batch; per-item results are preserved.
6. On ambiguous or terminal-unknown state, query by `submit_id` via
   `OperationLedger.query`; never resubmit blindly.
7. Download artifacts via `scripts.artifact_service.ArtifactService`,
   which validates SHA-256, truncations, and media metadata before
   declaring the task complete.

Example routing check:

```text
用户：用首尾两张图生成视频
路由：video / frames2video -> dreamina-cli
下一步：先读取实时 help，展示将消费积分的精确请求，等待明确批准后提交
```

## Out of scope

This Skill does **not**:

* implement any Dreamina private API;
* embed private credentials or account snapshots;
* hard-code model / resolution / ratio catalogs;
* bypass the web-console first-video prerequisite;
* retry submissions on ambiguous state without a
  `query_result --submit_id=<submit_id>` query.
