# Dreamina Canvas setup

Use this operation when the user asks to install, update, or make **`dreamina-canvas`** ready for the first time. The classic `dreamina` CLI is a different product path; hand its setup to `dreamina-cli` by skill name when that is what the user requested.

## When to use

用户首次接入即梦画布 CLI、安装后找不到命令、登录后仍被服务端拒绝，或希望确认当前 CLI 是否可用时使用。只需生成图片或视频且环境已就绪时，交给对应 Canvas 技能。

## Rules

- 每次只选当前操作系统的一条安装命令；先核对官方来源与目标目录。
- 安装和授权登录属于不同动作，各自按用户请求执行。检查现有安装不触发更新。
- `version`、`schema` 和 `auth account` 分别证明制品、命令契约和服务端账户状态；缺一项就报告具体未就绪阶段。

## Workflow

### Step 1: Discover

Identify the operating system, shell, current `dreamina-canvas` location, and whether the user wants installation or only a readiness check. Do not run an installer if a working CLI already satisfies the request.

### Step 2: Install when requested

Show the OS-specific official installer from [examples/happy-path.md](../examples/first-use-happy-path.md), its source and expected target, and obtain explicit authorization before changing the machine. Do not silently modify shell startup files.

### Step 3: Verify the binary

Run `dreamina-canvas --help`, `dreamina-canvas version`, and `dreamina-canvas schema`. If the command is missing, reopen the terminal or use the installer's stated PATH instruction, then retry the check. Installer exit code alone does not establish readiness.

### Step 4: Verify identity when requested

If the user authorized login, start `auth login` and let the user finish browser authorization. In a non-interactive session, use the challenge returned by the CLI and continue the same flow with `auth wait`; do not expose or persist credentials. Confirm the account with `auth account`, since `auth status` checks only local state.

### Step 5: Report readiness

Report the observed CLI version/distribution, schema availability, and server-recognized account readiness. Stop before canvas creation, resource upload, or paid generation unless separately requested.

After setup, hand off command construction to **`dreamina-canvas-cli`**, account recovery to **`dreamina-canvas-cli-auth`**, and creative work to **`dreamina-canvas-use`**. Install a named companion separately if a granular installation did not include it: `npx skills add full-aigc-skills/dreamina-skills --skill <skill-name>`.

## Boundaries

- Use live `schema`, command `--help`, model and voice discovery as runtime authority. The guide examples are starting shapes, not fixed catalogs.
- Installation, login, profile changes, resource upload, and spending each have their own authorization boundary. An installation request does not authorize generation.
- In a support report, request the full command, complete error, `dreamina-canvas version`, and `meta.requestId` if present; for generation also request `projectId` and `submitId`. Redact tokens, cookies, signed URLs, and local credential files.
- 不存储登录凭据、设备码或访问令牌；排障遵循最小权限，只读取用户指定的命令结果。

## 不适用

已完成安装且只要求创建画布、上传素材或生成内容时，不该用 setup 重跑安装或登录；分别交给对应 Canvas 技能。用户说的是经典 `dreamina` CLI 时，也不使用本技能。

## Validation checklist

- [ ] `--help` 显示 auth、canvas、model、node、operation、resource。
- [ ] `version` 返回实际版本和发行信息，`schema` 可读取当前命令契约。
- [ ] 如已获登录授权，`auth account` 确认服务端识别账户；只读检查未被说成登录完成。
- [ ] 报告没有把安装、登录、画布创建或积分生成混为一个授权动作。

## Gotchas

- PATH 尚未在当前终端生效：按安装输出修正后重新运行 `--help`，不要仅凭安装器成功退出判断可用。
- `auth status` 是本地状态；服务端权限以 `auth account` 和实际错误为准。
- 文档参数会变化：模型查询和节点命令先看当前 `schema` / `--help`。

Read [examples/happy-path.md](../examples/first-use-happy-path.md) for the three OS commands and verification sequence. For an unauthorized installer, read [examples/boundary-refusal.md](../examples/first-use-boundary-refusal.md); for a headless login, read [examples/noninteractive-login.md](../examples/first-use-noninteractive-login.md). Read [references/troubleshooting.md](../references/first-use-troubleshooting.md) and [examples/failure-recovery.md](../examples/first-use-failure-recovery.md) only when setup or login fails.
