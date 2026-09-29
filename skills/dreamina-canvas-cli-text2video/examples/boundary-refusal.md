# Boundary Refusal — 拒绝越权

## 场景 A：免批准直跑

用户：「直接跑，别给我看什么报价。」

- 本技能只保存免费草稿；付费执行必须经
  `dreamina-canvas-cli` 展示报价并取得精确
  `--credit-ceiling` 批准。回复：草稿 nodeId + 报价获取方式，等批准。

## 场景 B：按旧 CLI 习惯强塞 16:9

用户：「老命令默认就是 16:9，直接给我 16:9。」

- Canvas 的比例以 discovery 的模型契约为准；模型不接受显式
  `--ratio` 时必须省略，由源或模型推断。
- 回复：先跑 discovery，按当前契约给可用比例清单供用户选。

## 场景 C：给 t2v 塞参考图

用户：「文生视频顺便把这张产品图垫进去。」

- `t2v` 不接受图像/帧引用；垫图任务属于
  `dreamina-canvas-cli-ref2video`（`m2v` / `first_last_frame`）。
- 回复：确认意图后改走图生视频技能链。

## 场景 D：让本技能直接跑付费命令

任何附加 `--run` / `--credit-ceiling` / `--credit-token` 的请求一律
拒绝；付费边界属于 `dreamina-canvas-cli`。
