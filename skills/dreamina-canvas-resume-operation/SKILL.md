---
name: dreamina-canvas-resume-operation
description: Use when an agent or script must continue, observe, or recover a Dreamina Canvas async operation by its submitId, never by minting a new submitId. Owns the operation state machine and the resubmittable invariant.
license: Complete terms in LICENSE
---

# Dreamina Canvas Operation Recovery

This Skill owns how an in-flight or stuck `submitId` is observed, waited
on, or recovered. It **never** authorises a new submission: when recovery
is impossible, it escalates to the user.

Reference detail is in
[references/recovery-state-machine.md](references/recovery-state-machine.md).

## When to use

- A `node run` (or any paid command) returned exit code 20 with
  `requiredAction: resume`.
- A previous process timed out, crashed, or lost its in-memory state but
  persisted `projectId` + `submitId`.
- The user wants to know whether a previously started run is still in
  flight, completed, or failed.

## When **not** to use

- For starting a new run. That is `dreamina-canvas-quote-and-run`.
- For re-quoting a draft that has not been approved yet.

## The two observation commands

```bash
# Pure read; never advances server-side state
dreamina-canvas --format json operation status <submitId> \
  --project-id <projectId>

# Poll to terminal state with a bounded local timeout
dreamina-canvas --format json operation wait <submitId> \
  --project-id <projectId> --timeout 10m --interval 5s
```

`operation status` is always safe to call. `operation wait` returns exit 0
only when the operation reaches a terminal state. A local timeout on
`operation wait` returns exit code 20; **the server keeps running**, the
local wait was just over budget.

## Submission state machine

`operation status` returns a `submission` block:

| `submission.state` | Meaning | Resubmittable? |
|--------------------|---------|----------------|
| `absent` | Server currently has no record of this submission. Does **not** prove the original request never reached the server; could also be retention expiry. | `resubmittable == true` only in this state. Treat as ambiguous and escalate. |
| `in_progress` | The server has accepted the submission; no terminal resource yet. | Never true. |
| `completed` | Terminal resource available; download via `dreamina-canvas-download-assets`. | Never true. |

A missing `submission` field is treated as **"accepted by server"**, never
as `absent`. Assuming `absent` when the server actually accepted would
cause a duplicate bill.

## Resubmit invariant

- `submission.resubmittable == true` appears **only** when `state == "absent"`.
- This is the **only** moment a re-submission is allowed.
- All other states require `operation status` / `operation wait`; never
  a fresh `node run` with a new `submitId`.

## Per-item state

For batch operations, the same rules apply per item. A missing `state`
field on an item is **not** failure; the call did not return a verdict for
that item. Use `operation status <submitId>` to inspect each item.

## Failure → recovery

| Failure | requiredAction | What to do next |
|---------|----------------|-----------------|
| `operation status` returns exit 11 | `login` | Re-authenticate, then re-query. |
| `operation wait` times out locally | `resume` | Increase `--timeout` or come back later; the operation is still running server-side. |
| `submission.state == "absent"` + `resubmittable == true` | `human_intervention` | Surface to the user; do not auto-resubmit. |
| `submission.state == "absent"` + `resubmittable == false` (or missing) | `resume` | Treat as accepted; continue waiting. |
| Server returns exit 21 | `retry` | Bounded back off and retry. |

## What this Skill will not do

- Mint a new `submitId`.
- Re-submit when `resubmittable` is not explicitly `true`.
- Treat a missing `submission` field as `absent`.
- Persist tokens, signed URLs, cookies, or session material.

## Policy

Invocation requires:
- Confirmed installation of dreamina-canvas
- A persisted lowercase projectId and submitId

Forbids:
- Minting a new submitId on retry
- Treating a missing submission.state as 'absent'
- Auto-resubmitting when resubmittable is not explicitly true
- Persisting tokens, signed URLs, cookies, or session material

Default prompt:

> Recover by ID, never by minting a new submitId. Treat a missing
> submission field as 'accepted by server', not as 'absent'. Only the
> absent + resubmittable=true combination allows a fresh node run.
>

<!-- QUALITY_BASELINE_V1 -->
## When to use（什么时候使用）

当用户需要 **从已记录状态恢复中断任务，避免重复提交或重复计费** 时加载本技能。先从请求中提取目标、输入、约束、交付格式和验收标准；描述摘要为：Use when an agent or script must continue, observe, or recover a Dreamina Canvas async operation by its submitId, never by minting a new submitId. Owns the operation state machine and the resubmittable invariant.。

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

核对任务标识、最后成功阶段、远端状态、预算和授权范围；任一关键条件未知时停止在只读阶段。
### Step 3：形成计划

列出将调用的工具、会改变的对象、成功标准以及失败后的安全退出方式。
### Step 4：执行动作

仅继续尚未完成且可证明安全的阶段；每个外部调用均保留可关联的状态或回执。
### Step 5：验证交付

返回复用结果、新执行步骤、未恢复项和下一人工决策点，并把事实、推断和未验证项分开陈述。

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

没有幂等键、远端状态或用户授权时不重提任务；恢复不扩大原批准范围。 如果请求需要别的技能，不复制其正文；按技能名称进行交接，并保留当前任务上下文。

## Progressive disclosure

- 需要确定输入/输出、状态和授权点时，读取 `references/workflow-contract.md`。
- 需要交付前自检时，读取 `references/validation-checklist.md`。
- 遇到超时、部分成功或恢复场景时，读取 `references/error-recovery.md`。
- 首次运行、拒绝越权和失败恢复分别参考 `examples/happy-path.md`、`examples/boundary-refusal.md`、`examples/failure-recovery.md`。
