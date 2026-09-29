# Failure Recovery — 运行中未收敛

场景：`node run` 已由 `dreamina-canvas-cli` 交接执行，进程
在轮询中断开，退出码 20（recoverable）。

```bash
# 错误：重提整个任务（会重复计费）
# 正确：用持久化的 submitId 续等（dreamina-canvas-cli）
dreamina-canvas --format json operation wait <stableUuid> --project-id <projectId>
```

- 同一 `submitId` 续等永不重复计费；新 `submitId` 才会。
- 若 `operation wait` 返回 21，按退避间隔重试，仍用同一 ID。
- 若返回 22，把已持久化的 nodeId / submitId / 退出码一并交接用户。

场景：草稿保存返回退出码 2，`error.code` 指向未知 flag。

```bash
dreamina-canvas --format json schema | jq '.data.flags'
# 对照修正 argv 后重存草稿；草稿阶段免费，可直接重试。
```
