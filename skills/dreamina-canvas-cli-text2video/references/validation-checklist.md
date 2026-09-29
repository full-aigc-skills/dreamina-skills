# Validation Checklist — Canvas Text-to-Video Task

交付前逐项确认：

- [ ] 三检通过（version / schema / auth account），
      证据记录在案。
- [ ] prompt 含运动意图且经用户确认或 `dreamina-prompt-text2video` 定稿。
- [ ] `--duration` 已传、>0、不超 discovery 模型上限。
- [ ] `--model` / `--ratio` 来自 live discovery；模型不接受 ratio 时未传。
- [ ] 草稿保存返回 `nodeId` 并持久化；未传 `--run`。
- [ ] 付费链由 `dreamina-canvas-cli` 执行，报价展示过用户，
      `--credit-ceiling` 为精确批准值。
- [ ] 异步等待复用同一 `submitId`；exit 20/21 未催生新 ID。
- [ ] 视频产物经 `resource get` + `resource download` 落盘并完成
      SHA-256 校验；时长与分辨率符合 discovery 规格。
