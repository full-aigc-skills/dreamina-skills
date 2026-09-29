# Error Recovery — Canvas Text-to-Image Task

只按退出码 + `error.code` + `requiredAction` 分流，不解析本地化文案。

| 场景 | 退出码 | 恢复动作 |
|------|--------|----------|
| argv / flag 名错误 | 2 | 对照 `schema` 修正后重存草稿（免费阶段）。 |
| 模型 / 比例 / 分辨率被拒 | 2 | 重跑 discovery 取当前值；禁止回退旧 CLI token。 |
| 草稿待付费确认 | 10 | 展示报价，取精确上限批准；复用返回的 node / task ID。 |
| 未登录 / 会话过期 | 11 | `dreamina-canvas-cli-auth` 重认证，同身份重试。 |
| 权限 / 权益不足 | 12 | 不重试，上报用户。 |
| 版本不兼容 | 13 | 按 `error.clientUpgrade.upgradeUrl` 升级。 |
| 运行中未收敛 | 20 | `operation wait` 同 `submitId` 续等。 |
| 可重试服务故障 | 21 | 退避重试，仍用同一 `submitId`。 |
| 需人工介入 | 22 | 交接用户。 |

## 红线

- 永不为本技能内的命令附加 `--run` 或 credit 参数。
- 永不因失败而生成新 `submitId` / `nodeId` 重提任务。
- 永不把 token、签名 URL、cookie 写入日志或状态文件。
