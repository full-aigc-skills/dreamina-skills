# Failure Recovery — 时长缺失与运行中断

场景：草稿保存返回退出码 2，提示缺少 `--duration`。

```bash
# 错误：沿用旧 CLI 思维不传时长
# 正确：补时长（缺省 5，先看 discovery 的模型上限）
dreamina-canvas --format json node create video \
  --prompt "<finalized prompt>" \
  --mode t2v --model <model> --ratio <ratio> \
  --duration 5
```

场景：显式 `--ratio` 被模型拒绝（退出码 2）。

```bash
# 重跑 discovery；契约写明“按比例推断/不接受 ratio”时删掉 --ratio
dreamina-canvas --format json model list --type video
dreamina-canvas --format json node create video \
  --prompt "<finalized prompt>" \
  --mode t2v --model <model> --duration 5
```

场景：`node run` 后断开，退出码 20。

```bash
# 同一 submitId 续等（dreamina-canvas-cli）
dreamina-canvas --format json operation wait <stableUuid> --project-id <projectId>
# 21 → 退避重试同一 ID；22 → 连同 nodeId/submitId 交接用户
```
