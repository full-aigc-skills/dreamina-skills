# Happy Path — 图生图端到端

用户：「把这张本地照片转成水墨画风格」（提供 `./photo.jpg`）。

```bash
# 0. 三检（dreamina-canvas-cli）
dreamina-canvas version
dreamina-canvas --format json schema
dreamina-canvas --format json auth account

# 1. 本地上传 → 冻结资源引用
dreamina-canvas --format json resource upload --file "$PWD/photo.jpg" --name "photo"
# → 持久化 res:<lowercaseUuid>

# 2. 发现（dreamina-canvas-cli 选定命令；值仅为占位）
dreamina-canvas --format json model list --type image
# → 记录 <model> <ratio> <resolution> 白名单

# 3. 提示词定稿（交接 dreamina-prompt-image2image）后存 i2i 草稿
dreamina-canvas --format json node create image \
  --title "photo-水墨" \
  --prompt "<finalized prompt>" \
  --mode i2i --model <model> \
  --ref res:<frozenResourceUuid>
# → 持久化 nodeId；免费

# 4. 付费链交接 dreamina-canvas-cli
#    node quote → node confirm（精确 --credit-ceiling）→ node run

# 5. 异步观察交接 dreamina-canvas-cli（operation wait）

# 6. 下载校验交接 dreamina-canvas-cli
#    resource get → resource download → SHA-256

# 7. （可选）高清放大：干跑 → 独立报价 → 执行（dreamina-canvas-cli）
#    产物是新节点，源节点不变
```

交付：res 引用、nodeId、报价/批准、submitId、resourceId、本地路径 + 哈希。
