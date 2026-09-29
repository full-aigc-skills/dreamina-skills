# Install Guide — 平台差异与排障

> 安装只认官方安装器；验证只认 live 输出。

## 平台差异

| 平台 | 安装器 | 默认位置 |
|------|--------|----------|
| macOS / Linux | `install.sh` | `~/.local/bin/dreamina-canvas` |
| Windows PowerShell | `install.ps1` | 用户目录（以安装提示为准） |
| Windows CMD | `install.bat` | 同上 |
| Windows Git Bash | `install.sh` 或 bat | `~/bin/dreamina-canvas.exe` |

- 自定义目录：`DREAMINA_CANVAS_INSTALL_DIR` / `INSTALL_DIR`，
  仅限用户批准的路径；不静默改 shell 启动文件。
- 海外版安装器 URL 见 本技能的 [安装契约](install-to-use.md)。

## 排障决策树

```
dreamina-canvas: command not found
├── 刚装完？→ 重开终端/Agent 会话（PATH 未生效，最高发）
├── 安装脚本提示目录不在 PATH？→ 按提示加入后重开终端
├── 自定义过安装目录？→ 确认该目录在 PATH
└── 仍失败 → 重跑安装器；再失败按指南带四件套反馈
```

## 反馈四件套（指南要求）

完整命令、完整报错、`dreamina-canvas version` 输出、
`meta.requestId`（如有）。**先更新 CLI 再重试**——问题可能已在新
版本解决。

## 升级策略

- 重跑原安装器即就地升级；升级后重新 `version`/`schema` 验证。
- 技能正文与 CLI 行为冲突时以 live 输出为准；schema 漂移是最常见的
  "命令突然不对了"根因。
