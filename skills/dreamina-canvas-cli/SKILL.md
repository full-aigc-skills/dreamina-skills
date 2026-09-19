---
name: dreamina-canvas-cli
description: Use when an agent must install, verify, update, or invoke dreamina-canvas and safely construct argv, route exit codes, separate stdout/stderr, persist identifiers, and avoid hard-coded catalogs.
license: Complete terms in LICENSE
---

# Dreamina Canvas CLI Foundation

This Skill owns the cross-cutting invariants every other `dreamina-canvas-*` Skill
relies on. It does **not** generate, quote, or submit anything; it only governs how
commands are built, how failures are interpreted, and how identifiers are persisted.

The reviewed CLI guide is
[references/cli-contract.md](references/cli-contract.md) and the routing rules are
in [references/error-routing.md](references/error-routing.md).
For authorized first-time installation and update, read
[references/install-to-use.md](references/install-to-use.md).

## When to use

- Before constructing any argv for `dreamina-canvas` from another Canvas Skill.
- When the binary is missing or requests an upgrade and the user wants the
  official domestic or overseas installer workflow.
- When a `dreamina-canvas` invocation returned a non-zero exit code or a JSON
  error envelope on stderr.
- When deciding whether the next step is to wait, retry, re-quote, or hand the
  task back to the user.

## When **not** to use

- For domain-specific generation guidance (`dreamina-canvas-generate-image`,
  `dreamina-canvas-generate-video`, etc.).
- For logging in or running any paid command — those are separately authorized
  at the action boundary (see `dreamina-canvas-auth` and the human-in-the-loop
  gates in this Skill set).

## Mandatory pre-flight

If the command is absent, stop and obtain installation authorization before
using the official command in `install-to-use.md`. After installation run
`dreamina-canvas --help`, then continue with the machine-readable checks below.

Before any non-trivial command:

1. `dreamina-canvas version` — confirm the binary is installed and capture the
   `commit`, `edition`, `distribution`, `buildTime`, `releaseDate`. Treat this
   output as authoritative; do not trust README prose for the current behavior.
2. `dreamina-canvas schema "<command path>"` (with `--format json`) — confirm
   the flag and value names used by this Skill. The guide seed values may
   lag the live binary.
3. `dreamina-canvas auth account` (when any later command may need credentials)
   — confirm the server recognises the active profile. `auth status` is local
   only; never trust it for "logged in".

Only after these three succeed may the caller construct the real command. Never
optimise them away, even for read-only commands, because schema drift is the
most common silent-failure cause.

## argv construction

Always pass `--format json` **before** the subcommand. The binary is the only
authoritative output channel; without `--format json` the result depends on
whether stdout is a TTY.

Global flags (place before the subcommand):

- `--format json` — required for any machine-driven call.
- `--non-interactive` — recommended whenever the agent cannot answer prompts.
- `--yes` — opt-in only; it never bypasses credit approval or capability gates.
- `--profile <name>` — isolate credentials and the active canvas context.
- `--region <cn>` — domestic public build fixed to `cn`; the overseas build
  omits the flag.

Never:

- Build argv by string interpolation. Use argv lists.
- Re-use a `--submit-id` value that came from an empty shell variable; pass
  `--submit-id ""` only when the script has already validated it is non-empty.
  An explicit empty value is rejected with exit code 2.
- Add `--run` to `node create` / `node edit` unless the caller has authorised
  the credit spend at this exact moment.

## stdout and stderr

- stdout in `--format json` mode contains only the declared JSON payload
  (`{"schemaVersion": "...", "ok": true, "data": {...}}` or
  `{"ok": false, "error": {...}}`).
- stderr carries everything else: progress, diagnostics, and on failure the
  single structured error envelope JSON object. stdout is empty during a
  failure.
- Therefore `dreamina-canvas --format json <cmd> > result.json` always gives a
  clean result file; never mix pipe stages from concurrent processes into one
  `jq` pipeline (their JSON bytes will interleave).

## Exit code routing

Do **not** parse localised `message` text. Branch only on the numeric exit code
and, for non-zero exits, on `error.code` plus `error.requiredAction`. Stable
codes from the CLI itself are namespaced `cli.*`; server-side business codes
are forwarded unchanged.

When `exit code 20` arrives it means the operation is still in flight and
recoverable: continue with the same `submitId` through `operation wait`; it
**never** authorises a new submission.

| Exit | Meaning | Next action |
|------|---------|-------------|
| 0 | success | continue |
| 1 | uncategorized internal failure | alert; investigate |
| 2 | invalid command, argument, or input schema | fix the command; do not retry |
| 11 | login required or session expired | re-authenticate then retry with the same identity |
| 12 | permission / capability / entitlement denied | do not retry; escalate |
| 13 | environment or release compatibility blocked | upgrade per `error.clientUpgrade.upgradeUrl` |
| 20 | recoverable; not converged in this run | continue with `operationRef` (`operation wait`) |
| 21 | retryable service or transport failure | back off and retry |
| 22 | human intervention required | hand off |

`requiredAction` values are one of `none`, `login`, `confirm`, `retry`,
`resume`, `upgrade`, `human_intervention`, `contact_support`. They are the
authoritative next-step hint for scripts.

## Identifier persistence

- `projectId`, `submitId`, `nodeId`, `updateId`, `resourceId`, `quoteId` are
  lowercase canonical UUIDs. Reuse the same `submitId` to continue a run;
  reusing it never re-bills. Switching to a new `submitId` re-bills.
- Generate them with `uuidgen | tr 'A-Z' 'a-z'`, persist them in
  process-managed state files (mode `0600`), and pass them explicitly on every
  cross-process retry.
- `submitId` empty (explicit or after a failed variable expansion) is
  rejected with exit code 2 — never let a missing variable silently mint a new
  idempotency key.

## What this Skill will not do

- Install or update the CLI without explicit user authorization; log in,
  refresh tokens, or perform paid generation from this foundation Skill.
- Persist OAuth tokens, cookies, signed URLs, or `credit-approval token`.
- Branch on localised human-language messages.
- Mutate the local `--use` canvas context unless the caller asked explicitly.

## Policy

Invocation requires:
- Confirmed installation of dreamina-canvas, or explicit authorization to use
  an official installer
- Verified --format json contract via dreamina-canvas schema

Forbids:
- Installing or updating the CLI without explicit user authorization
- Logging in, refreshing tokens, or running paid commands
- Persisting OAuth tokens, cookies, signed URLs, or credit-approval token

Default prompt:

> Before any non-trivial dreamina-canvas call, run version + schema, pass
> --format json, and route failures by exit code + requiredAction. Never
> hard-code model or voice names.
>

<!-- QUALITY_BASELINE_V1 -->
## When to use（什么时候使用）

当用户需要 **为当前请求选择并执行可验证、可恢复的专业工作流** 时加载本技能。先从请求中提取目标、输入、约束、交付格式和验收标准；描述摘要为：Use when an agent must install, verify, update, or invoke dreamina-canvas and safely construct argv, route exit codes, separate stdout/stderr, persist identifiers, and avoid hard-coded catalogs.。

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
