# Error Recovery — Canvas Reference-to-Video Task

只按退出码 + `error.code` + `requiredAction` 分流，不解析本地化文案。

| 场景 | 退出码 | 恢复动作 |
|------|--------|----------|
| `--mode i2v` / `multi_modal` 被拒 | 2 | 改 `m2v`（单图）或 `first_last_frame`（有序帧）。 |
| 引用非法（file://、uri:、短链） | 2 | `resource upload` 后改 `res:<lowercaseUuid>`。 |
| 双帧源比例不一致 | 2 | 换源比例一致的帧；输出比例跟随首帧。 |
| 模型拒绝显式 `--ratio` | 2 | 重跑 discovery；按比例推断时删除 `--ratio`。 |
| 缺 `--duration` | 2 | 补时长（缺省 5，模型上限内）。 |
| 草稿待付费确认 | 10 | 展示报价，取精确上限批准；复用返回 node / task ID。 |
| 未登录 / 会话过期 | 11 | `dreamina-canvas-cli-auth` 重认证，同身份重试。 |
| 权限 / 权益不足 | 12 | 不重试，上报用户。 |
| 版本不兼容 | 13 | 按 `error.clientUpgrade.upgradeUrl` 升级。 |
| 运行中未收敛 | 20 | `operation wait` 同 `submitId` 续等。 |
| 可重试服务故障 | 21 | 退避重试，仍用同一 `submitId`。 |
| 需人工介入 | 22 | 交接用户。 |

## 红线

- 永不传 `i2v` / `multi_modal`；它们是旧 CLI 与服务端别名，不是公开模式。
- 永不上 `file://` / `uri:` / 本地路径冒充引用。
- 付费只发生在 `dreamina-canvas-cli` 内。
- 永不因失败生成新 `submitId` / `nodeId` 重提任务。
- 永不把 token、签名 URL、cookie 写入日志或状态文件。
