# Workflow Contract — Canvas CLI Auth Task

本契约定义 `dreamina-canvas-cli-auth` 的输入、输出、状态与授权边界。

## 输入

| 输入 | 必填 | 说明 |
|------|------|------|
| 环境类型 | 是 | TTY 交互 or Agent/脚本 |
| 账号意图 | 是 | 登录 / 换号(--force) / 续期 / 退出 |
| profile | 否 | 多账号隔离名 |

## 输出

- 授权结果：`auth account` 的服务端识别结论（按隐私规则处理标识）。
- 闭环证据：device code 流程的完成状态。

## 状态机

```text
NOT_LOGGED_IN → LOGIN_STARTED → WAITING → AUTHORIZED → VERIFIED
VERIFIED → REFRESHED / LOGGED_OUT
```

- `WAITING` 可用同一 device code 多次 `auth wait` 续等。
- 只有 `VERIFIED`（auth account 成功）才算登录完成。

## 授权边界

- 允许：auth 七子命令（全部免费）。
- 需用户参与：浏览器授权动作本身。
- 禁止：本技能内运行任何付费命令；持久化凭据材料。

## 与相邻技能的分界

| 需求 | 去向 |
|------|------|
| 凭据安全红线、profile 机制、refresh window 细节 | `dreamina-canvas-cli-auth` |
| 安装 CLI | `dreamina-canvas-cli-setup` |
| 登录后的生成任务 | 各任务技能 |
