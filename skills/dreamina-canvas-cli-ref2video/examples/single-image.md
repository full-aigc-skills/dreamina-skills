# Single Image Motion — 单图微动（m2v）

用户：「让这张老人微笑的照片轻轻动起来，5 秒。」（./grandpa.jpg）

```bash
# 1. 三检 + discovery
dreamina-canvas --format json model list --type video
# → 记录 <model>、时长上限、比例规则（帧驱动通常按首帧推断）

# 2. 上传并冻结
dreamina-canvas --format json resource upload --file "$PWD/grandpa.jpg" --name "grandpa"
# → 持久化 res:<uuid>

# 3. m2v 草稿（不传 --ratio：按比例推断）
dreamina-canvas --format json node create video \
  --title "grandpa-微笑" \
  --prompt "老人自然地微笑，轻微点头，光线柔和，镜头固定" \
  --mode m2v --model <model> \
  --ref res:<frozenResourceUuid> \
  --duration 5
# → 持久化 nodeId；免费

# 4. 交接 dreamina-canvas-cli：quote → 批准 → run
# 5. 交接 dreamina-canvas-cli（operation wait）
# 6. 交接 dreamina-canvas-cli 下载 + SHA-256
```

要点：微动类 prompt 写"轻微/自然/镜头固定"，避免大幅运动破坏肖像
真实感；要更大幅度时改 prompt 重新编辑（全量替换）再跑新一轮。
