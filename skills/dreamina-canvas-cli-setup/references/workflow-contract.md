# Workflow Contract — Canvas CLI Install Task

本契约定义 `dreamina-canvas-cli-setup` 的输入、输出、状态与授权边界。

## 输入

| 输入 | 必填 | 说明 |
|------|------|------|
| 操作系统与终端类型 | 是 | 决定三个安装器中哪一个 |
| 安装授权 | 是 | 安装/升级改变本机，必须显式授权 |
| 失败现象（排障时） | 否 | 完整命令 + 报错 + version 输出 |

## 输出

- 安装证据：安装器输出摘要 + 安装位置。
- 验证证据：`--help` 命令族清单、`version`/`schema` 结构化输出。

## 状态机

```text
AUTHORIZED → INSTALLED → VERIFIED → HANDED_OFF
                    ↘ TROUBLESHOOTED → VERIFIED
```

- 未授权不得进入 `INSTALLED`。
- `VERIFIED` 的唯一证据是 live `--help` / `version` / `schema`，
  不是下载退出码。

## 授权边界

- 需显式授权：运行安装器（含升级）、自定义安装目录。
- 免费只读：检查现有安装（`version` / `--help` / `ls` 安装目录）。
- 禁止：登录、付费命令、静默改 shell 启动文件。

## 与相邻技能的分界

| 需求 | 去向 |
|------|------|
| 登录授权与账号自检 | `dreamina-canvas-cli-auth` |
| 深层安装契约（海外版/目录变量） | 本技能的 [安装契约](install-to-use.md) |
| 首次使用全流程引导 | `dreamina-canvas-cli-setup` |
