# Boundary Refusal — 拒绝越权

## 场景 A：要求免批准直跑

用户：「别问价格，直接生成跑出来就行。」

- 本技能只保存免费草稿；付费执行必须经
  `dreamina-canvas-cli` 展示报价并取得精确
  `--credit-ceiling` 批准。
- 回复：先给出草稿 nodeId 与预计报价获取方式，等批准后再交接付费链。

## 场景 B：要求复用旧 CLI 参数

用户：「就按我以前 `dreamina text2image --model_version=5.0
--resolution_type=2k` 的写法来。」

- 旧 v1.4.18 token 已随 sunset 失效于 Canvas 语境；只接受 live
  discovery 的模型 / 分辨率 / 比例值。
- 回复：解释迁移对照（见 `references/parameter-reference.md` 末节），
  并用 discovery 当前值重建命令。

## 场景 C：让本技能直接跑付费命令

任何「在本技能里加 `--run` / `--credit-ceiling` / `--credit-token`」
的请求一律拒绝；付费边界属于 `dreamina-canvas-cli`。
