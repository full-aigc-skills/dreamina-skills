# Validation Checklist — Canvas Text-to-Voice Task

交付前逐项确认：

- [ ] 三检通过（version / schema / auth account），
      证据记录在案。
- [ ] 旁白文本为用户定稿，逐字进入 `--prompt`，无静默改写。
- [ ] voiceName 来自 live `voice list`，非旧对话复用。
- [ ] tts 草稿未传 `--model` / `--count`；未传 `--run`。
- [ ] nodeId 已持久化；付费链由 quote-and-run 执行并展示过报价。
- [ ] 异步等待复用同一 `submitId`；exit 20/21 未催生新 ID。
- [ ] 音频产物经 `resource get` + `resource download` 落盘、SHA-256 校验，
      时长与文本长度量级相符（不符标 `NOT_VERIFIED`）。
