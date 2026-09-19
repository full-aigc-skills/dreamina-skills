---
name: dreamina-canvas-create
description: "Use when an agent or script must create, list, or select a Dreamina Canvas. Owns the idempotent --project-id rule: every concurrent or cross-process retry must reuse the same lowercase UUID; never depend on the local --use context from another process."
license: Complete terms in LICENSE
---

# Dreamina Canvas Lifecycle

This Skill owns canvas identity. It governs how a canvas is created, listed,
selected, and — most importantly — how the resulting `projectId` is reused
across processes. The `projectId` is the only thing that makes generation
calls idempotent.

Reference detail is in
[references/canvas-context.md](references/canvas-context.md).

## When to use

- Before the first `node create` / `node edit` / `node run` in a workflow that
  must address a specific canvas.
- When an existing canvas needs to be selected for a follow-up run.
- When two concurrent scripts must share a single canvas safely.

## When **not** to use

- For generating nodes (the domain Skills own that).
- For mutating `--use` context without an explicit user request.

## Create rule (read this twice)

```bash
# Generate the idempotency key yourself; do NOT let the CLI generate one
PROJECT_ID=$(uuidgen | tr 'A-Z' 'a-z')

# Persist it before any generation call
echo "$PROJECT_ID" > .state/project-id

# Create the canvas with that project-id; pass --use only when the
# current single-user sequential flow wants it
dreamina-canvas --format json canvas create "我的画布" \
  --project-id "$PROJECT_ID" --use
```

Re-running `canvas create` with the **same** `--project-id` is a no-op that
returns the existing canvas. Switching to a new `--project-id` creates a new
canvas every time.

## `--use` and the local canvas context

`canvas create --use` writes a profile-and-environment-keyed file under
`dreamina-canvas/contexts/<profile-and-environment>.json` containing the
chosen `projectId`. Subsequent commands that omit `--project-id` fall back
to this file.

`--use` is **only** safe when:

- A single user is running a single sequential flow in a single process.
- The caller is willing to discard the default canvas context if it is wrong.

`--use` is **not** safe when:

- Two or more processes may write the contexts file concurrently
  (byte-level interleaving).
- A cross-process retry must reuse the original `projectId` — the contexts
  file may not reflect the original choice by then.
- Concurrent automation needs deterministic identity for every command.

In those cases pass `--project-id <uuid>` explicitly on every call.

## Listing

```bash
dreamina-canvas --format json canvas ls --limit 20
```

`--limit` and `--offset` paginate. Use the returned `projectId` values
verbatim when piping into other commands; do not retype them.

## Failure → recovery

| Failure | requiredAction | What to do next |
|---------|----------------|-----------------|
| `canvas create` returns a different `projectId` than the one passed | n/a | Treat as a contract violation; surface to the user; do not overwrite the persisted id. |
| `canvas ls` returns exit 11 | `login` | Re-authenticate, then re-list. |
| Concurrent processes report the same `projectId` was auto-created | n/a | Stop; one process owns the id and the others must pass it explicitly. |

## What this Skill will not do

- Create a canvas without a caller-supplied `--project-id`.
- Persist OAuth tokens, cookies, signed URLs, or `credit-approval token`.
- Mutate the contexts file outside of an explicit `--use` request.
- Skip re-validation of the live `--project-id` before a paid call.

## Policy

Invocation requires:
- Confirmed installation of dreamina-canvas
- A caller-supplied lowercase UUID for --project-id on creation

Forbids:
- Letting the CLI auto-generate --project-id in a multi-step or cross-process workflow
- Mutating the local --use contexts file outside an explicit user request
- Reusing a projectId returned from a response that contradicts the request

Default prompt:

> Always pass --project-id explicitly on cross-process retries and in any
> concurrent flow. Use --use only for a single sequential user flow. Never
> retype the returned projectId; pipe it.
>

<!-- QUALITY_BASELINE_V1 -->
## When to use（什么时候使用）

当用户需要 **在明确输入、预算和交付约束后执行生成或写入操作** 时加载本技能。先从请求中提取目标、输入、约束、交付格式和验收标准；描述摘要为："Use when an agent or script must create, list, or select a Dreamina Canvas. Owns the idempotent --project-id rule: every concurrent or cross-process retry must reuse the same lowercase UUID; never depend on the local --use context from another process."。

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

校验输入、模型/工具能力、输出路径、预算上限和审批状态；任一关键条件未知时停止在只读阶段。
### Step 3：形成计划

列出将调用的工具、会改变的对象、成功标准以及失败后的安全退出方式。
### Step 4：执行动作

按一次批准执行并记录请求标识；模糊结果先查询而不是重提；每个外部调用均保留可关联的状态或回执。
### Step 5：验证交付

验证产物存在性、格式、哈希/标识、成本状态和质量门禁，并把事实、推断和未验证项分开陈述。

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

付费、发布、覆盖、上传或外部写入必须使用当前任务的显式授权；不自动扩大次数和预算。 如果请求需要别的技能，不复制其正文；按技能名称进行交接，并保留当前任务上下文。

## Progressive disclosure

- 需要确定输入/输出、状态和授权点时，读取 `references/workflow-contract.md`。
- 需要交付前自检时，读取 `references/validation-checklist.md`。
- 遇到超时、部分成功或恢复场景时，读取 `references/error-recovery.md`。
- 首次运行、拒绝越权和失败恢复分别参考 `examples/happy-path.md`、`examples/boundary-refusal.md`、`examples/failure-recovery.md`。
