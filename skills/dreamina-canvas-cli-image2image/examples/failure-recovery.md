# Failure Recovery — 引用错误与运行中断

场景：i2i 草稿保存返回退出码 2，`error.code=cli.invalid_generation_reference`。

```bash
# 错误：把本地路径塞进 --ref
# 正确：先上传再冻结引用
dreamina-canvas --format json resource upload --file "$PWD/photo.jpg"
# → res:<lowercaseUuid>
dreamina-canvas --format json node create image \
  --prompt "<finalized prompt>" --mode i2i --model <model> \
  --ref res:<lowercaseUuid>
```

场景：付费运行后进程断开，退出码 20。

```bash
# 用持久化的 submitId 续等（dreamina-canvas-cli）
dreamina-canvas --format json operation wait <stableUuid> --project-id <projectId>
# 21 → 退避重试同一 ID；22 → 连同 nodeId/submitId 交接用户
```

场景：重风格后发现比例被清空。

- 原因：`node edit image` 全量替换时漏传 `--ratio`。
- 恢复：`node show --node-id <nodeId>` 读回旧值（若已被覆盖则以
  discovery 默认重建），整块回传修正后的生成参数；草稿阶段免费。
