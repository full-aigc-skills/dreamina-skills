---
name: dreamina-canvas-auth
description: Use when an agent or script must check, refresh, or recover Dreamina Canvas authentication, distinguish local login state from server-recognized identity, and isolate credentials across profiles. Never prints or persists tokens.
license: Complete terms in LICENSE
---

# Dreamina Canvas Authentication

This Skill owns authentication state for the `dreamina-canvas` CLI. It does
**not** generate, quote, or submit anything; it only governs login, status
checks, refresh, logout, and profile isolation.

Reference detail is in
[references/auth-state.md](references/auth-state.md).

## When to use

- Before any command that may require credentials (use `auth account` to
  confirm, not `auth status`).
- When a prior command returned exit code 11 (`requiredAction: login`) or
  exit code 12 (permission denied).
- When switching between isolated profiles (`--profile <name>`).
- When the user explicitly asks to log in, log out, or refresh credentials.

## When **not** to use

- For installing or upgrading the CLI binary itself (`dreamina-canvas-cli`).
- For running paid commands; this Skill only confirms and refreshes the
  identity, it never invokes generation.

## The two "am I logged in?" questions

These answer two different things and the answers can disagree:

| Command | Question answered | Talks to server? | Trust for "logged in"? |
|---------|-------------------|------------------|------------------------|
| `auth status` | "do I have a non-expired local token for this profile?" | No — local file only | Never alone |
| `auth account` | "what does the server currently recognise this profile as?" | Yes | Yes — the only authoritative check |

Always treat `auth account` as the source of truth for "is this profile
logged in?" `auth status` exists only to inspect local state when debugging.

A common failure mode: local token looks fine, but the server has revoked
it. The CLI will surface this as exit code 11 with `requiredAction: login`;
re-login and retry the original command with the **same identifiers**
(`projectId`, `submitId`, `nodeId`).

## Login flow

```bash
# TTY: blocks until the user completes browser authorisation
dreamina-canvas --format json auth login --profile <name>

# Non-TTY (script / agent): returns a recoverable challenge
dreamina-canvas --format json auth login --profile <name>
# → challenge payload includes a device code; do NOT loop here, hand it to a human

# Continue waiting on the same device code from any process
dreamina-canvas --format json auth wait --device-code <code> --timeout 10m
```

`--timeout` defaults to 10 minutes; `--timeout 0` polls once. Do not loop on
`auth login` in a script; use `auth wait` so that a separate process (or the
user in a browser) can complete the step.

## Refresh and logout

- `auth refresh` — only when the credential is still in its refresh window.
  Do not call it speculatively.
- `auth logout` — idempotent. The overseas build (`distribution != cn`)
  revokes server-side before deleting local credentials.

## Profile isolation

Credentials, login state, and the active canvas context are all keyed by
`--profile`. Profile names may contain only letters, digits, `.`, `_`, and
`-`. Keep one profile per isolated environment (work / personal / CI).

```bash
dreamina-canvas --profile work auth login
dreamina-canvas --profile personal auth account
```

The two profiles do not interfere with each other. The active profile is
the only one that subsequent `node create`, `canvas create --use`, and
similar commands will pick up by default.

## What this Skill will not do

- Persist, log, or echo OAuth tokens, cookies, signed URLs, or any other
  credential material.
- Auto-retry on exit code 12 (permission denied); that requires a human.
- Run generation commands even when authenticated; that is the role of
  `dreamina-canvas-quote-and-run`.

## Policy

Invocation requires:
- Confirmed installation of dreamina-canvas
- User consent for any interactive login or browser authorisation step

Forbids:
- Persisting or logging OAuth tokens, cookies, signed URLs, or session material
- Speculative auth refresh when the credential is not in its refresh window
- Auto-retrying on permission denied (exit 12)
- Generating, quoting, or submitting any paid command

Default prompt:

> Use auth account as the authoritative "am I logged in?" check. auth status
> is local-only and never enough on its own. Reuse the original projectId /
> submitId / nodeId after re-authentication.
>

<!-- QUALITY_BASELINE_V1 -->
## When to use（什么时候使用）

当用户需要 **配置或诊断本地认证与运行前置条件** 时加载本技能。先从请求中提取目标、输入、约束、交付格式和验收标准；描述摘要为：Use when an agent or script must check, refresh, or recover Dreamina Canvas authentication, distinguish local login state from server-recognized identity, and isolate credentials across profiles. Never prints or persists tokens.。

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

检查本地工具、配置位置、权限和当前认证状态；任一关键条件未知时停止在只读阶段。
### Step 3：形成计划

列出将调用的工具、会改变的对象、成功标准以及失败后的安全退出方式。
### Step 4：执行动作

通过受支持的交互入口完成最小配置，并立即清理敏感输入；每个外部调用均保留可关联的状态或回执。
### Step 5：验证交付

只报告可用性、身份范围和脱敏错误，不输出凭据内容，并把事实、推断和未验证项分开陈述。

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

不回显、记录或提交密钥；不替用户创建账户、购买额度或接受条款。 如果请求需要别的技能，不复制其正文；按技能名称进行交接，并保留当前任务上下文。

## Progressive disclosure

- 需要确定输入/输出、状态和授权点时，读取 `references/workflow-contract.md`。
- 需要交付前自检时，读取 `references/validation-checklist.md`。
- 遇到超时、部分成功或恢复场景时，读取 `references/error-recovery.md`。
- 首次运行、拒绝越权和失败恢复分别参考 `examples/happy-path.md`、`examples/boundary-refusal.md`、`examples/failure-recovery.md`。
