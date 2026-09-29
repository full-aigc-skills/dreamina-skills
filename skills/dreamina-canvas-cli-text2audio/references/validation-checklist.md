# Validation Checklist — Canvas Text-to-Audio (Music) Task

交付前逐项确认：

- [ ] 三检通过（version / schema / auth account），
      证据记录在案。
- [ ] prompt 为四要素风格描述（体裁+情绪+节奏+乐器），经用户确认。
- [ ] `--model` 来自 live `model list --type audio` 且支持 music 模式。
- [ ] `--duration` >0 且不超该模型 discovery 上限。
- [ ] music 草稿未传 `--voice-name` / `--count`；未传 `--run`。
- [ ] nodeId 已持久化；付费链由 quote-and-run 执行并展示过报价。
- [ ] 异步等待复用同一 `submitId`；exit 20/21 未催生新 ID。
- [ ] 音频产物经 `resource get` + `resource download` 落盘、SHA-256 校验，
      时长与请求 `--duration` 一致（不符标 `NOT_VERIFIED`）。
