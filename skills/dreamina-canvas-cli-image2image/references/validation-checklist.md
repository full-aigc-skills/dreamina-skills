# Validation Checklist — Canvas Image-to-Image Task

交付前逐项确认：

- [ ] 三检通过（version / schema ×2 / auth account），证据记录在案。
- [ ] 本地源文件已 `resource upload`，`resourceId` 小写 canonical UUID
      已持久化；未用 `file://` / `uri:` 伪引用。
- [ ] i2i 草稿带至少一个图像引用；prompt 经用户确认或
      `dreamina-prompt-image2image` 定稿。
- [ ] `--model` / `--ratio` / `--resolution` / `--count` 全部来自 live
      discovery，无旧 v1.4.18 token。
- [ ] 重风格编辑给了完整生成块（全量替换），未漏 flag。
- [ ] 付费链由 `dreamina-canvas-cli` 执行；upscale 走自身
      报价，未混用 `node confirm` token。
- [ ] 异步等待复用同一 `submitId`；exit 20/21 未催生新 ID。
- [ ] 产物经 `resource get` + `resource download` 落盘并 SHA-256 校验；
      upscale 产物确认为新节点、源节点未被覆盖。
