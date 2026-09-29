# Happy Path — 文生视频端到端

用户：「生成一段 5 秒视频：雨夜霓虹街道，镜头缓慢推进。」

```bash
# 0. 三检（dreamina-canvas-cli）
dreamina-canvas version
dreamina-canvas --format json schema
dreamina-canvas --format json auth account

# 1. 提示词已定稿（含运动意图）；否则先交接 dreamina-prompt-text2video

# 2. 视频发现（dreamina-canvas-cli 选定命令；值仅为占位）
dreamina-canvas --format json model list --type video
# → 记录 <model>、ratio 白名单、时长上限

# 3. 免费草稿
dreamina-canvas --format json node create video \
  --title "雨夜霓虹" \
  --prompt "雨夜霓虹街道，镜头缓慢推进，地面倒影流动" \
  --mode t2v --model <model> --ratio <ratio> \
  --duration 5
# → 持久化 nodeId / mutationVersion；免费

# 4. 付费链交接 dreamina-canvas-cli
#    node quote → node confirm（精确 --credit-ceiling）→ node run

# 5. 异步观察交接 dreamina-canvas-cli（operation wait）

# 6. 下载校验交接 dreamina-canvas-cli
#    resource get → resource download → SHA-256
```

交付：nodeId、报价与批准上限、submitId、resourceId、本地路径 + 哈希 + 时长。
