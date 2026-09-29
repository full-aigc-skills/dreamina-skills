# Validation Checklist — Canvas Text-to-Image Task

交付前逐项确认：

- [ ] `dreamina-canvas version` / `schema` / `auth account`
      三检已通过，证据（commit、flag 清单、账号判定）记录在案。
- [ ] prompt 来自用户确认或 `dreamina-prompt-text2image` 定稿，未静默改写。
- [ ] `--model` / `--ratio` / `--resolution` / `--count` 全部来自 live
      discovery，无硬编码、无旧 v1.4.18 token。
- [ ] 草稿保存返回 `nodeId`，已持久化；未传 `--run`。
- [ ] 付费链由 `dreamina-canvas-cli` 执行，报价展示过用户，
      `--credit-ceiling` 为精确批准值。
- [ ] 异步等待复用同一 `submitId`；exit 20/21 未催生新 ID。
- [ ] 产物经 `resource get` + `resource download` 落盘并完成 SHA-256 校验。
- [ ] 输出区分事实 / 推断 / `NOT_VERIFIED`，含失败与跳过项。
