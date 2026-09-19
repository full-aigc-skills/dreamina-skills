---
name: dreamina-canvas-use
description: Use when an agent or user wants the canonical Dreamina Canvas end-to-end workflow without naming a specific Skill. Routes to the smallest applicable Skill chain and reports saved drafts, quoted amounts, approval, submission acceptance, terminal completion, and verified artifacts.
license: Complete terms in LICENSE
---

# Dreamina Canvas (end-to-end)

This Skill is the **single implicitly invokable** entry point for the
Dreamina Canvas suite. It selects the smallest applicable Skill chain
from the other twelve Canvas Skills and orchestrates the full flow:

```text
saved draft  →  quoted amount  →  user approval  →
submission accepted  →  terminal completion  →  verified artifact
```

Reference routing detail is in
[references/routing-table.md](references/routing-table.md).

## When to use

- The user asks for "the canvas workflow" or "Dreamina Canvas" without
  naming a specific Skill.
- The agent wants to compose a multi-node Canvas end-to-end and report
  each lifecycle stage back to the user.

## When **not** to use

- For advanced users who already know which lower-level Skill they want;
  call that Skill directly.
- For installing, authenticating, or running any paid command without
  explicit user authorisation.

## Routing rules

| User intent | Skill chain (in order) |
|-------------|-----------------------|
| "Set up Dreamina Canvas / install / log in" | `dreamina-canvas-cli` → `dreamina-canvas-auth` |
| "Find a model / voice / ratio / resolution" | `dreamina-canvas-discover-models` |
| "Create / select a canvas" | `dreamina-canvas-create` |
| "Save a draft image / video / audio node" | `dreamina-canvas-generate-image` / `…video` / `…audio` |
| "Compose a graph of nodes (image / video / audio / timeline)" | `dreamina-canvas-compose` (then hand to quote-and-run) |
| "Edit a timeline (clip / audio-clip / trim / speed)" | `dreamina-canvas-manage-timeline` |
| "Quote → confirm → run a saved node" | `dreamina-canvas-quote-and-run` |
| "Continue / observe an async run" | `dreamina-canvas-resume-operation` |
| "Download a finished resource" | `dreamina-canvas-download-assets` |

This Skill **does not duplicate** global flags, exit-code tables, model
catalogs, or node schemas; those belong to the lower-level Skills.

## Lifecycle reporting

Every final response from this Skill must surface, in order:

1. The saved draft identifier(s) (`nodeId`, `mutationVersion`).
2. The quoted amount (`totalMaxCredits`, `confirmable`,
   `confirmationRequired`).
3. The user approval (`--credit-ceiling` value used; never the token).
4. The submission acceptance (`submitId`, `nodeId`, exit code).
5. The terminal completion (`submission.state == "completed"` plus
   `resourceId`).
6. The verified artifact (canonical local path, byte count, SHA-256).

If any stage fails, the Skill returns the failure exit code, the
`requiredAction`, and the next step the caller should take.

## What this Skill will not do

- Persist tokens, signed URLs, cookies, or `credit-approval token`.
- Approve spend on the user's behalf.
- Bypass the lower-level Skills' guardrails.
- Mint a `submitId` itself; it only forwards the one minted by
  `dreamina-canvas-quote-and-run`.
- Implicit-invoke the other twelve Canvas Skills: each of them is
  explicit. This Skill is the only one that may be invoked implicitly.

## Invocation policy

`allow_implicit_invocation: true` for **this Skill only**. All twelve
other `dreamina-canvas-*` Skills set `allow_implicit_invocation: false`.

## Policy

Invocation requires:
- Confirmed installation of dreamina-canvas
- User's authorisation for each paid stage

Forbids:
- Persisting tokens, signed URLs, cookies, or credit-approval token
- Approving spend on the user's behalf
- Duplicating the lower-level Skills' command, exit-code, or model details
- Minting a submitId; only forward the one from dreamina-canvas-quote-and-run

Default prompt:

> Route to the smallest applicable Skill chain. Always surface saved
> draft, quoted amount, user approval, submission acceptance, terminal
> completion, and verified artifact. Never duplicate the lower-level
> Skills' details. Never approve spend.
>

<!-- QUALITY_BASELINE_V1 -->
## When to use（什么时候使用）

当用户需要 **为当前请求选择并执行可验证、可恢复的专业工作流** 时加载本技能。先从请求中提取目标、输入、约束、交付格式和验收标准；描述摘要为：Use when an agent or user wants the canonical Dreamina Canvas end-to-end workflow without naming a specific Skill. Routes to the smallest applicable Skill chain and reports saved drafts, quoted amounts, approval, submission acceptance, terminal completion, and verified artifacts.。

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
