# Happy Path — 图生视频端到端

用户：「把这张产品图做成 5 秒展示视频，镜头环绕。」（提供 `./product.png`）

```bash
# 0. 三检（dreamina-canvas-cli）
dreamina-canvas version
dreamina-canvas --format json schema
dreamina-canvas --format json auth account

# 1. 帧上传 → 冻结引用
dreamina-canvas --format json resource upload --file "$PWD/product.png" --name "product"
# → 持久化 res:<lowercaseUuid>

# 2. 视频发现（dreamina-canvas-cli 选定命令；值仅为占位）
dreamina-canvas --format json model list --type video
# → 记录 <model>、时长上限、比例规则（帧驱动通常按首帧推断 → 不传 --ratio）

# 3. 模式选择：单图“动起来” → m2v（本技能核心判断）
dreamina-canvas --format json node create video \
  --prompt "镜头环绕产品缓慢旋转，高光扫过表面" \
  --mode m2v --model <model> \
  --ref res:<frozenResourceUuid> \
  --duration 5
# → 持久化 nodeId；免费

# 4. 付费链交接 dreamina-canvas-cli
#    node quote → node confirm（精确 --credit-ceiling）→ node run

# 5. 异步观察交接 dreamina-canvas-cli（operation wait）

# 6. 下载校验交接 dreamina-canvas-cli
#    resource get → resource download → SHA-256
```

首尾帧变体：再上传尾帧得到第二个 `res:<uuid>`，改 `--mode first_last_frame`
并**有序**传两个 `--ref`（先首后尾，源比例一致）。
