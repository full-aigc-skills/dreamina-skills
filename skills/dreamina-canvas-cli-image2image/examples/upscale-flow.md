# Upscale Flow — 高清放大完整流程

用户：「这张最终稿放大到 4K 给我。」（产物节点 <resultNodeId>）

```bash
# 1. 干跑校验（免费；契约归 dreamina-canvas-cli）
dreamina-canvas --format json node upscale image \
  --node-id <resultNodeId> --mode <m> --resolution <r> --dry-run
# pro 档如需 --detail，先 schema 确认

# 2. 展示 upscale 报价（与生成是两笔独立费用）
# 3. 用户对 upscale 单独给精确上限 → 执行
dreamina-canvas --format json node upscale image \
  --node-id <resultNodeId> --submit-id <stableUuid> \
  --mode <m> --resolution <r> --credit-ceiling <approvedCeiling> --wait
# exit 20/21 → 同一 submitId 续等/退避重试

# 4. 产物是新节点 <upscaledNodeId>：源节点未被覆盖
# 5. 交接 dreamina-canvas-cli 下载新节点资源 + SHA-256
```

要点：`node confirm` 的批准 token 对 upscale **无效**，反之亦然；
upscale 是独立定价分支，永远单独报价、单独批准。
