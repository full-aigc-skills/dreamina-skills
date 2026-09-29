# Async Generation — 视频长任务与终端解耦

视频生成动辄数分钟，进程退出/断线后凭持久化 ID 恢复。

```bash
# 1. 免费草稿 → 交接 quote-and-run：quote → 批准 → node run
# → 持久化 projectId / submitId（0600 状态文件）

# --- 任意时刻恢复 ---
# 2. 单次查询
dreamina-canvas --format json operation status <submitId> --project-id <projectId>

# 3. 续等
dreamina-canvas --format json operation wait <submitId> --project-id <projectId> \
  --timeout 10m --interval 5s
# exit 0  → 任务终态，交接 download-assets 校验落盘
# exit 20 → 服务端仍在跑：保存 ID，稍后继续 wait
# exit 21 → 退避重试同一 submitId
```

要点：与旧 CLI 的 `query_result --submit_id` 不同，Canvas 的恢复单元是
`operation status/wait <submitId>`；本地 operations 目录里的恢复文件只是
兜底，Agent 以自己持久化的 ID 为准。
