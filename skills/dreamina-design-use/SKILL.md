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
  Skill's body. A consuming plugin must pin this repository by immutable tag,
  peeled commit SHA and per-file digest, then run its own vendor parity check.
  This source skill does not pretend that a plugin-internal snapshot verifier
  is present after granular installation.

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

<!-- QUALITY_BASELINE_V1 -->
## When to use（什么时候使用）

当用户需要 **为当前请求选择并执行可验证、可恢复的专业工作流** 时加载本技能。先从请求中提取目标、输入、约束、交付格式和验收标准；描述摘要为：Thin router Skill for Dreamina Design image and video workflows. Selects between the 13 packaged Dreamina Skills (dreamina-cli-* and dreamina-prompt-*) and never duplicates their prompt or CLI bodies.。

## Rules

- 先读后写：先确认当前状态与真实能力，再执行会改变外部状态的动作。
- 权限最小化：只使用完成当前步骤所需的文件、工具、账户与网络范围。
- 证据优先：运行结果、资源 ID、版本、哈希或测试输出缺失时，明确标记为 `NOT_VERIFIED`。
- 幂等优先：保留请求标识与阶段状态；结果不明确时先查询，不进行盲目重试。
- 隐私安全：日志、示例、回执和错误信息不得包含 token、cookie、密钥或个人敏感数据。

## Workflow

### Step 1：澄清意图

确认本技能是否匹配目标；若只是相邻需求，交给更精确的技能。
### Step 2：执行预检

确认目标、输入、约束、可用工具、成功标准和失败边界；任一关键条件未知时停止在只读阶段。
### Step 3：形成计划

列出将调用的工具、会改变的对象、成功标准以及失败后的安全退出方式。
### Step 4：执行动作

按最小充分步骤执行，并在关键状态变化处记录证据；每个外部调用均保留可关联的状态或回执。
### Step 5：验证交付

输出结果、验证证据、未完成项、风险和明确的下一步，并把事实、推断和未验证项分开陈述。

## Validation checklist

- [ ] 技能触发条件与用户意图一致，没有把相邻任务误路由到本技能。
- [ ] 输入、目标对象、版本和输出位置均已明确，且没有使用猜测值替代必填值。
- [ ] 所有写入、付费、发布或不可逆动作都在用户授权范围内。
- [ ] 结果已用独立检查验证；仅有“命令成功”或“文件存在”不算完整验收。
- [ ] 输出包含实际证据、失败/跳过项、剩余风险和可执行的下一步。

## Gotchas

1. **把计划当结果**：文档或提示词不等于真实执行；必须标明实际运行层级。
2. **错误重试**：超时或响应丢失可能已经产生远端状态，先查询再决定是否重试。
3. **隐式扩大范围**：批量、全量、发布、覆盖和付费不是普通读写的自然延伸。
4. **版本漂移**：引用外部资源时记录版本、tag 或提交；不要把可变分支当发布证据。
5. **证据过期**：缓存、旧截图和历史测试不能证明当前环境；在交付前刷新关键证据。

## 不适用与边界

不超出用户给定范围；写入、付费、发布和不可逆动作需要明确授权。 如果请求需要别的技能，不复制其正文；按技能名称进行交接，并保留当前任务上下文。

## Progressive disclosure

- 需要确定输入/输出、状态和授权点时，读取 `references/workflow-contract.md`。
- 需要交付前自检时，读取 `references/validation-checklist.md`。
- 遇到超时、部分成功或恢复场景时，读取 `references/error-recovery.md`。
- 首次运行、拒绝越权和失败恢复分别参考 `examples/happy-path.md`、`examples/boundary-refusal.md`、`examples/failure-recovery.md`。
