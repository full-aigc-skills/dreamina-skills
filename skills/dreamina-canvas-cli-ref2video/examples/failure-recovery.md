# Failure Recovery — 模式误用与运行中断

场景：草稿保存返回退出码 2，模式被拒。

```bash
# 错误：沿旧 CLI 习惯传 --mode i2v
dreamina-canvas --format json node create video \
  --prompt "<motion prompt>" --mode i2v ...
# 正确：单图改 m2v（首尾帧场景改 first_last_frame）
dreamina-canvas --format json node create video \
  --prompt "<motion prompt>" \
  --mode m2v --model <model> \
  --ref res:<frozenResourceUuid> --duration 5
```

场景：双帧 `first_last_frame` 报比例不一致（退出码 2）。

```bash
# 校验两帧比例，裁/补到一致后再按先首后尾提交
# 输出比例跟随首帧；无法一致时退回单帧 m2v
```

场景：`node run` 后断开，退出码 20。

```bash
# 同一 submitId 续等（dreamina-canvas-cli）
dreamina-canvas --format json operation wait <stableUuid> --project-id <projectId>
# 21 → 退避重试同一 ID；22 → 连同 nodeId/submitId 交接用户
```
