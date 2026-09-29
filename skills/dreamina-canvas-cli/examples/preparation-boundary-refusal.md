# Boundary Refusal — 拒绝越权

## 场景 A：准备阶段就要生成

用户：「传完图顺便直接跑一张出来。」

- 本技能只做准备，全部免费；生成是各任务技能的职责，付费链属于
  `dreamina-canvas-cli`。
- 回复：先交付 ID 集合，确认任务类型后交接对应任务技能走草稿→报价→批准。

## 场景 B：把别名当 model 值

用户：「就写 5.0Pro，别查了。」

- `--model` 只接受 discovery 的 model 值；别名直接当参数会被 exit 2。
- 回复：用 `model find "5.0Pro"` 解析出 model 值再记录。

## 场景 C：要求 canvas ls 切画布

用户：「ls 里选第二块当当前画布。」

- `canvas ls` 只读不切换；切当前画布用 `canvas create --use` 或对应命令。
- 回复：明确目标画布后执行切换，并把新 projectId 交付。

## 场景 D：丢失 resourceId 要求"找回"

resourceId 未持久化时无法用本技能找回（列表接口不保证按名称反查）。
- 回复：重新上传并立即记录新 resourceId；旧素材如已导入节点可从
  `node show` 读回其资源引用。
