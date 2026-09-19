---
name: dreamina-canvas-quote-and-run
description: Use when an agent or script must quote, confirm, and run a saved Dreamina Canvas node, bind approval to an exact quote and credit ceiling, and never mint a new submitId for recovery.
license: Complete terms in LICENSE
---

# Dreamina Canvas Quote → Confirm → Run

This Skill owns the safety transaction for paid execution. The transaction
is always: `node quote` against the latest authoritative draft, then
`node confirm` to bind user approval to an exact credit ceiling, then
`node run` with a caller-minted `submitId`. Reusing the same `submitId`
on recovery replays the original submission and never re-bills.

Reference detail is in
[references/credit-approval.md](references/credit-approval.md).

## When to use

- The caller wants to actually run a previously saved node (after the
  structural work is finished and the user has authorised the spend).
- A prior `node quote` returned `confirmable=false`; this Skill explains
  why and what to do next.
- A `node run` failed with exit code 20 (`resume`); this Skill explains
  how to continue without re-billing. Always re-quote before retrying.

## When **not** to use

- For saving a draft without running. That is `node create <type>` without
  `--run`, owned by the relevant domain Skill.
- For re-quoting after a silent change to the saved draft; this Skill
  always re-quotes from the live authoritative draft.

## The three-step transaction

```bash
# 1. Re-quote from the live draft (always the latest authoritative state)
dreamina-canvas --format json node quote --node-id <nodeId> \
  --project-id "$PROJECT_ID"
# → items[] (one entry per node, ordered), totalMaxCredits, confirmable,
#   confirmationRequired, creditConfirmation.minimumCreditCeiling

# 2. Confirm the spend ceiling (mints a short-lived credit-approval token)
token=$(dreamina-canvas --format json node confirm \
  --node-id <nodeId> \
  --project-id "$PROJECT_ID" \
  --credit-ceiling "$CEILING" \
  | jq -r '.data.credit-approval token')

# 3. Run with the existing submitId; reuse the same id on retry
dreamina-canvas --format json node run \
  --node-id <nodeId> \
  --project-id "$PROJECT_ID" \
  --credit-token "$token" \
  --submit-id "$SUBMIT_ID"

# Batch: one --submit-id per --node-id, equal length and order
dreamina-canvas --format json node run \
  --node-id <node1> --node-id <node2> \
  --submit-id <id1> --submit-id <id2> \
  --project-id "$PROJECT_ID" --credit-token "$token"
```

## Binding rules (read carefully)

The credit `token` is bound to **who + which canvas + which batch of nodes
+ ceiling + batch summary**. It is **not** bound to the prompt text.

Two direct consequences:

- Editing the prompt between confirm and run is fine **as long as the
  latest live quote is still within the approved ceiling**. `node run`
  re-quotes the latest draft and runs only if the total stays under
  the ceiling.
- The token cannot be moved to a different node set. Different nodes need
  a new confirm.

`node confirm` refuses to mint a token when:

- Any node is un-quotable (`confirmable=false`).
- The supplied `--credit-ceiling` is below the latest total (returns
  Conflict).

## The submitId is the only billable identity

Generate `submitId` yourself (lowercase UUID) and persist it **before**
`node run`. Reusing the same `submitId` replays the original submission
and never re-bills. Switching to a new `submitId` **is** a new run and
re-bills.

`--submit-id ""` (explicit empty) is rejected with exit code 2; this is the
deliberate trap that prevents an unset shell variable from silently
minting a fresh idempotency key.

## Per-item batch behaviour

`node run` may take multiple `--node-id` values. The response `data.items[]`
is the same length and order as the input. Per-item outcomes:

Before a batch call, mint and persist one `--submit-id` per `--node-id`.
The two lists must have equal length and order. On retry, reuse every ID in
its original position; a single batch-wide ID is invalid, and replacing any
item's ID can re-bill that item.

- `REJECTED` (any item) → `cli.node_run_rejected`, exit code 2. Rejection
  is terminal; retry is useless.
- `unknown` (any item, no rejection) → `cli.node_run_unknown`, exit code 20,
  `requiredAction: resume`.
- All accepted → exit code 0.

If submission fails entirely, the failure envelope includes
`partialData.items[]` with each item's `nodeId` / `submitId`. Absence of a
`state` field in an item is **not** failure — it means the call did not
return a verdict for that item; the operation may still be in flight
server-side. Use `operation status <submitId>` to inspect each item.

## Recovery rules

- An ambiguous or timed-out response is reconciled **by ID**, not by
  re-submitting.
- `operationRef` (alias for `submitId`) is the key; pass it to
  `operation status` or `operation wait`.
- `submission.state = absent` plus `resubmittable = true` is the **only**
  case where re-submission is permitted. A missing `submission` field is
  treated as "accepted by server", never as "absent" — assuming absent
  when the server actually accepted would cause a duplicate bill.

## What this Skill will not do

- Persist `credit-approval token`, signed URLs, cookies, OAuth tokens, or
  any provider task identifier.
- Re-quote with a stale draft.
- Mint a new `submitId` on retry; it must be reused.
- Branch on localized `message` text — only on exit code, `error.code`,
  and `error.requiredAction`.
- Use `--yes` instead of `--credit-ceiling` when the price is knowable
  in advance.

## Policy

Invocation requires:
- Confirmed installation of dreamina-canvas
- User-supplied projectId, nodeIds, submitId, and credit ceiling
- Explicit action-time approval for the spend

Forbids:
- Persisting credit-approval token, signed URLs, cookies, or OAuth tokens
- Re-quoting from a stale draft
- Minting a new submitId on retry
- Using --yes when the ceiling is knowable in advance
- Treating a missing submission.state field as 'absent'

Default prompt:

> Always re-quote from the latest authoritative draft before run. Bind
> approval with --credit-ceiling, not --yes. Reuse the same submitId on
> recovery; switching submitId re-bills.
>

<!-- QUALITY_BASELINE_V1 -->
## When to use（什么时候使用）

当用户需要 **在明确输入、预算和交付约束后执行生成或写入操作** 时加载本技能。先从请求中提取目标、输入、约束、交付格式和验收标准；描述摘要为：Use when an agent or script must quote, confirm, and run a saved Dreamina Canvas node, bind approval to an exact quote and credit ceiling, and never mint a new submitId for recovery.。

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
