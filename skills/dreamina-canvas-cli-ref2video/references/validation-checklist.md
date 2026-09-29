# Validation Checklist — Canvas Reference-to-Video Task

交付前逐项确认：

- [ ] 三检通过（version / schema / auth account），
      证据记录在案。
- [ ] 每帧素材已 `resource upload`，`res:<lowercaseUuid>` 持久化；
      未用 `file://` / `uri:` 伪引用。
- [ ] 模式选择正确：单图 → `m2v`；有序首尾帧 → `first_last_frame`；
      未出现 `i2v` / `multi_modal`。
- [ ] 双帧场景两图源比例一致且按先首后尾顺序传入；输出比例跟随首帧。
- [ ] `--duration` 已传、>0、不超 discovery 模型上限；模型按比例推断时
      未传 `--ratio`。
- [ ] 草稿保存返回 `nodeId` 并持久化；未传 `--run`。
- [ ] 付费链由 `dreamina-canvas-cli` 执行，报价展示过用户。
- [ ] 异步等待复用同一 `submitId`；exit 20/21 未催生新 ID。
- [ ] 视频产物经 `resource get` + `resource download` 落盘并 SHA-256 校验。
