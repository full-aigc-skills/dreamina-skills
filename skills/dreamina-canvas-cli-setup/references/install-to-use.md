# dreamina-canvas installation and update

Installation or update changes the user's machine. Explain the source and
target directory, then obtain explicit authorization before running either
installer.

## Installers (domestic public build)

macOS / Linux (the supplied first-use guide):

```bash
curl -fsSL https://jimeng.jianying.com/canvas-cli/install.sh | bash
```

Windows PowerShell: `irm https://jimeng.jianying.com/canvas-cli/install.ps1 | iex`.
Windows CMD: `curl.exe -fsSLO https://jimeng.jianying.com/canvas-cli/install.bat && install.bat`.
Choose exactly one installer for the current OS. After installation, reopen the
terminal or apply the installer's stated PATH change if the command is missing.

Overseas public build:

```bash
curl -fsSL https://lf3-static.bytednsdoc.com/obj/eden-cn/psj_hupthlyk/ljhwZthlaukjlkulzlp/dreamina_canvas_cli_oversea/install.sh | bash
```

To choose a target directory, set `DREAMINA_CANVAS_INSTALL_DIR` or the
compatible `INSTALL_DIR` only to a user-approved path. Do not silently change
shell startup files.

## Post-install verification

```bash
dreamina-canvas --help
dreamina-canvas --format json version
dreamina-canvas --format json schema
```

The installer output and live `version`/`schema` responses are authoritative.
Do not claim readiness from the download exit code alone.

## 安装位置与本地文件

| 位置 | 用途 |
|------|------|
| `~/.local/bin/dreamina-canvas` | macOS/Linux 默认安装位置；Windows Git Bash 在 `~/bin/dreamina-canvas.exe`；自定义目录以安装提示为准 |
| `~/.agents/skills/dreamina-canvas-cli/` | 随安装包提供的 Agent Skill，排障时可重读 |
| `<用户配置目录>/dreamina-canvas/contexts/<profile-and-environment>.json` | 当前选中的画布 |
| `<用户配置目录>/dreamina-canvas/operations/<profile-and-environment>/<submitId>.json` | 任务恢复信息 |

用户配置目录：macOS 通常 `~/Library/Application Support/`，Linux 通常
`~/.config/` 或 `$XDG_CONFIG_HOME`，Windows 通常用户 `AppData`。
**不要手工修改**本地状态或凭据文件；不要把日志/配置/输出中的敏感信息
发到公开渠道。

## 常见问题（与官方指南 §7 对账）

### 1. 安装后找不到 `dreamina-canvas` 命令
- 重开终端或 Agent 会话再跑 `--help`（最常见：PATH 未在当前 shell 生效）。
- 按安装脚本的提示把安装目录加入 PATH。
- 仍失败 → 重新执行安装命令。

### 2. 登录后仍提示未登录或无权限
- `dreamina-canvas --format json auth account` 看服务端识别的账号
  （`auth status` 只看本地，不能单独作为登录证据）。
- 登录态失效 → `auth login` 重新授权；切换账号用 `auth login --force`。
- 服务端返回权限/权益限制（exit 12）→ 按产品页面检查账号状态，不重试。

### 3. 模型、比例或分辨率不支持
- 先更新 CLI 再重试（问题可能已在新版本解决）。
- 让 Agent 重新查询 `model list`；**不要**照抄旧文档、历史对话或
  其他环境的模型名。

### 4. 任务长时间没有结果
- 用**原** submitId 继续 `operation status/wait`；不要重复提交。
- 把画布 webUrl 给用户，网页端同样能看到状态。

### 5. Agent 使用了旧命令
- 让 Agent 重读 `~/.agents/skills/dreamina-canvas-cli/SKILL.md`，并跑
  `dreamina-canvas schema` 或对应 `--help`。
- 旧版 `dreamina text2image` / `dreamina image2video` 等命令**不适用**于
  画布 CLI；本包内迁移路径见 `dreamina-canvas-cli-*` 任务技能。

### 6. 反馈问题（四件套）
一次性提供：完整命令、完整错误信息、`dreamina-canvas version` 输出、
错误结果中的 `meta.requestId`（如有）；生成任务再加 projectId/submitId。
不要在公开渠道发送密码、Cookie、访问令牌、签名链接或本地凭据文件。
