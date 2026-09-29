# Happy Path — 文生图端到端

用户：「帮我生成一张"一只橘猫坐在窗边，柔和晨光，浅景深"的图，1:1。」

```bash
# 0. 三检（dreamina-canvas-cli）
dreamina-canvas version
dreamina-canvas --format json schema
dreamina-canvas --format json auth account

# 1. 提示词已定稿（用户直给）；否则先交接 dreamina-prompt-text2image

# 2. 发现（dreamina-canvas-cli 选定命令；以下值仅为占位）
dreamina-canvas --format json model list --type image
# → 记录 <model> <ratio=1:1> <resolution> 白名单

# 3. 免费草稿（本技能职责终点之一）
dreamina-canvas --format json node create image \
  --title "橘猫窗边" \
  --prompt "一只橘猫坐在窗边，柔和晨光，浅景深" \
  --mode t2i --model <model> --ratio 1:1 \
  --resolution <resolution> --count 1
# → 持久化 nodeId / mutationVersion；此步免费

# 4. 付费链交接 dreamina-canvas-cli
#    node quote → node confirm（用户精确批准 --credit-ceiling）→ node run

# 5. 异步观察交接 dreamina-canvas-cli
#    operation wait --submit-id <stableUuid>

# 6. 下载校验交接 dreamina-canvas-cli
#    resource get → resource download → SHA-256 校验
```

交付：nodeId、报价与批准上限、submitId、resourceId、本地路径 + 哈希。
