# Error Recovery — Canvas Image-to-Image Task

只按退出码 + `error.code` + `requiredAction` 分流，不解析本地化文案。

| 场景 | 退出码 | 恢复动作 |
|------|--------|----------|
| 引用格式非法（file://、uri:、短链） | 2 | 改 `res:<lowercaseUuid>`；本地文件先 `resource upload`。 |
| i2i 缺图像引用 | 2 | 上传源图并补 `--ref res:<uuid>`。 |
| 模型 / 比例 / 分辨率被拒 | 2 | 重跑 discovery；禁止回退旧 CLI token。 |
| upscale 用错批准 token | 2 | 走 `node upscale image` 自身报价/批准（dreamina-canvas-cli）。 |
| 草稿待付费确认 | 10 | 展示报价，取精确上限批准；复用返回 node / task ID。 |
| 未登录 / 会话过期 | 11 | `dreamina-canvas-cli-auth` 重认证，同身份重试。 |
| 权限 / 权益不足 | 12 | 不重试，上报用户。 |
| 版本不兼容 | 13 | 按 `error.clientUpgrade.upgradeUrl` 升级。 |
| 运行中未收敛 | 20 | `operation wait` 同 `submitId` 续等。 |
| 可重试服务故障 | 21 | 退避重试，仍用同一 `submitId`。 |
| 需人工介入 | 22 | 交接用户。 |

## 红线

- 永不上 `file://` / `uri:` / 本地路径冒充引用。
- 付费只发生在 `dreamina-canvas-cli` 或 upscale 自身报价链。
- 永不因失败生成新 `submitId` / `nodeId` 重提任务。
- 永不把 token、签名 URL、cookie 写入日志或状态文件。
