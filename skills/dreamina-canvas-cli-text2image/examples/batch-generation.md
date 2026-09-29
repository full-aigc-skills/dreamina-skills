# Batch Generation — 多草稿批量出图

用户：「同一主题给我出 4 张不同比例的候选图。」

```bash
# 0. 三检 + 发现（一次 discovery 供所有草稿）
dreamina-canvas --format json model list --type image
# → <model> 及其 ratio / resolution 白名单

# 1. 逐张免费草稿（t2i 无引用）
dreamina-canvas --format json node create image --title "候选-横版" \
  --prompt "<finalized prompt>" --mode t2i --model <model> \
  --ratio 16:9 --resolution <resolution> --count 1   # → nodeId_A
dreamina-canvas --format json node create image --title "候选-方图" \
  --prompt "<finalized prompt>" --mode t2i --model <model> \
  --ratio 1:1 --resolution <resolution> --count 1    # → nodeId_B
dreamina-canvas --format json node create image --title "候选-竖版" \
  --prompt "<finalized prompt>" --mode t2i --model <model> \
  --ratio 9:16 --resolution <resolution> --count 1   # → nodeId_C

# 2. 交接 dreamina-canvas-cli：逐节点 node quote，
#    把 3 条报价（含比例/分辨率/数量）汇总给用户
# 3. 用户给一个精确总上限 → node confirm → node run
#    每个 node 一个稳定 --submit-id，长度与顺序一致
# 4. 逐 submitId 交接 dreamina-canvas-cli（operation wait）
# 5. 逐 resourceId 交接 dreamina-canvas-cli 下载 + SHA-256
```

要点：批量只合并"展示与批准"，不合并"计费与确认"；任一节点失败单独
报，不影响其他节点，也绝不整批重提。
