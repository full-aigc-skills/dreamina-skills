# Error Recovery — Canvas Text-to-Audio (Music) Task

只按退出码 + `error.code` + `requiredAction` 分流，不解析本地化文案。

| 场景 | 退出码 | 恢复动作 |
|------|--------|----------|
| music 传了 `--voice-name` | 2 | 删除 `--voice-name`；音乐是模型驱动。 |
| 模型不支持 music 模式 | 2 | 重跑 `model list --type audio`，换 music 模式模型。 |
| duration 超模型上限 | 2 | 取 discovery 上限内时长，或换模型。 |
| 传了 `--count` | 2 | 删除；音频节点不接受 `--count`。 |
| 草稿待付费确认 | 10 | 展示报价，取精确上限批准；复用返回 node / task ID。 |
| 未登录 / 会话过期 | 11 | `dreamina-canvas-cli-auth` 重认证，同身份重试。 |
| 权限 / 权益不足 | 12 | 不重试，上报用户。 |
| 版本不兼容 | 13 | 按 `error.clientUpgrade.upgradeUrl` 升级。 |
| 运行中未收敛 | 20 | `operation wait` 同 `submitId` 续等。 |
| 可重试服务故障 | 21 | 退避重试，仍用同一 `submitId`。 |
| 需人工介入 | 22 | 交接用户（完整命令、报错、version、requestId）。 |

## 红线

- 永不在 music 上传 `--voice-name`，不在任何音频节点上传 `--count`。
- 付费只发生在 `dreamina-canvas-cli` 内。
- 永不因失败生成新 `submitId` / `nodeId` 重提任务。
- 永不把 token、签名 URL、cookie 写入日志或状态文件。
