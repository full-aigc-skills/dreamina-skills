# 首次安装与就绪检查示例

以下安装命令来自用户提供的即梦画布 CLI 入门指南。**先确认操作系统、官方来源、安装目录并取得用户授权，再执行其中一条**；不要把三条都运行。若已有可用 CLI，直接从验证开始。

```bash
# macOS / Linux
curl -fsSL https://jimeng.jianying.com/canvas-cli/install.sh | bash

# Windows PowerShell
irm https://jimeng.jianying.com/canvas-cli/install.ps1 | iex

# Windows CMD
curl.exe -fsSLO https://jimeng.jianying.com/canvas-cli/install.bat && install.bat
```

安装后的只读验证和获授权后的登录：

```bash
dreamina-canvas --help
dreamina-canvas version
dreamina-canvas schema
dreamina-canvas auth login
dreamina-canvas auth account
```

`--help` 应显示 `auth`、`canvas`、`model`、`node`、`operation`、`resource`。`auth account` 才能确认服务端识别当前账号。Agent 自动化可将全局 `--format json` 放在子命令前；无交互登录使用 `dreamina-canvas --non-interactive auth login`，保留本次 challenge，随后按 CLI 返回信息运行 `auth wait`，不要反复发起新的登录。安装后若 `command not found`，先按安装输出修正 PATH 或重新打开终端，再复查版本与 schema。

指南给出的 macOS/Linux 默认可执行文件位置是 `~/.local/bin/dreamina-canvas`；其他系统及自定义安装以安装器实际输出为准。不要据此猜测安装成功。

报告示例：`CLI_READY` 只表示命令及 schema 可用；`ACCOUNT_READY` 还需要 `auth account` 成功。未获登录授权时明确报告 `ACCOUNT_NOT_CHECKED`。
