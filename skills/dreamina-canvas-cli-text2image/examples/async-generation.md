# Async Generation — 提交后与终端解耦

用户先批准付费，Agent 提交后需要把终端关掉/断线也能续查。

```bash
# 1. 免费草稿（同上）
dreamina-canvas --format json node create image \
  --title "异步示例" --prompt "<finalized prompt>" \
  --mode t2i --model <model> --ratio <ratio> --resolution <resolution> --count 1
# → 持久化 nodeId

# 2. 交接 dreamina-canvas-cli：node quote → 用户批准 → node run
# → 持久化 submitId（mode 0600 状态文件）+ projectId

# --- 进程可在此退出；任意时刻、任意进程恢复 ---

# 3. 续查（dreamina-canvas-cli）
dreamina-canvas --format json operation status <submitId> --project-id <projectId>
dreamina-canvas --format json operation wait  <submitId> --project-id <projectId> \
  --timeout 10m --interval 5s
# exit 20 = 服务端仍在跑：换个时间再 wait，同一 submitId
```

要点：恢复信息本就落在
`dreamina-canvas/operations/<profile-and-environment>/<submitId>.json`
（用户配置目录），但 Agent 必须把自己持有的 projectId/submitId 记入
任务状态，不能依赖去翻本地文件。
