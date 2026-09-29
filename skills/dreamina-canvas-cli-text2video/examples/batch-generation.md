# Batch Generation — 多候选视频

用户：「同一段雨夜街道，给我 16:9 和 9:16 各一版，预算之内都跑。」

```bash
# 1. 三检 + discovery（记录时长上限与比例规则）
dreamina-canvas --format json model list --type video

# 2. 两版免费草稿
dreamina-canvas --format json node create video --title "雨夜-横" \
  --prompt "雨夜霓虹街道，镜头缓慢推进，地面倒影流动" \
  --mode t2v --model <model> --ratio 16:9 --duration 5   # → nodeId_H
dreamina-canvas --format json node create video --title "雨夜-竖" \
  --prompt "雨夜霓虹街道，镜头缓慢推进，地面倒影流动" \
  --mode t2v --model <model> --ratio 9:16 --duration 5   # → nodeId_V

# 3. 交接 dreamina-canvas-cli：
#    逐节点 node quote → 按「模型×时长×分辨率×数量」逐条列报价 →
#    用户给精确总上限 → node confirm / node run（各自稳定 submitId）

# 4. 并行等待（dreamina-canvas-cli）
dreamina-canvas --format json operation wait <submitId_H> --project-id <projectId> --timeout 10m --interval 5s
dreamina-canvas --format json operation wait <submitId_V> --project-id <projectId> --timeout 10m --interval 5s

# 5. 交接 dreamina-canvas-cli 逐 resourceId 下载 + SHA-256
```

要点：视频候选单价高，报价必须逐条列出可裁剪；任一版 exit 20 只是
本地等待结束，换时间续等同一 submitId。
