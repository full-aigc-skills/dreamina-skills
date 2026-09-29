# Model Guide — Canvas Text-to-Image

> 模型、比例、分辨率是**运行时事实**：只从 live discovery 取，不背目录、
> 不跨环境搬运。文档（含本指南）与 live 输出冲突时以 live 为准。

## 发现流程

```bash
# 1. 列出当前账号可用的图像模型及规格
dreamina-canvas --format json model list --type image

# 2. 按常用名/别名定位模型
dreamina-canvas --format json model find "<名称关键字>" --type image

# 3. 细读返回负载：每个模型带 mode、ratio 白名单、resolution 白名单、
#    引用要求与数量上限 —— 这些就是全部合法参数值
```

- `--model` 必须填 discovery 返回的 **model 字段值**；列表里的别名
  （中文名、 marketing 名）只用于 `model find` 查找，**不得**直接当参数。
- 旧 CLI 的 `3.0 / 4.0 / 5.0 / 5.0Pro` 这类 token 在 Canvas 不一定存在同名
  模型；不得按旧记忆映射，以 discovery 为准。

## 选择要点

| 场景 | 做法 |
|------|------|
| 默认出图 | 选 discovery 列表中标记为默认/推荐项的 model，比例/分辨率取其默认 |
| 高分辨率海报 | 先按 `resolution` 白名单筛模型，再确认 `ratio` 支持目标比例 |
| 批量挑图 | `--count` 上限以 discovery 为准；超出则拆多次草稿 |
| 特定风格 | prompt 层面解决（交接 `dreamina-prompt-text2image`），不要假设存在“风格模型” |

## 比例与分辨率绑定规则

- 比例必须在该模型的 ratio 白名单内；白名单外一律 exit 2，重试无用。
- 图片生成要求显式 `--resolution`（缺省会被拒）；取值以该模型的
  resolution 白名单为准。
- 不存在"自定义宽高"的通用入口；如 live schema 声明了相应字段才可使用。

## 权益与计费

- 可用模型集合随账号权益变化； discovery 返回为空或缺模型时，先
  `auth account` 确认账号，再按 exit 12/13 处理，不要猜测。
- 价格不体现在 discovery：先 `node quote` 看实时报价，用户精确批准
  `--credit-ceiling` 后才 `node run`。
- 2K 与 4K、不同 count 的报价可能相差数倍；报价展示时连同分辨率与
  数量一起报，避免只报单价。

## 漂移处理

模型上下架、比例白名单变动是常态。每次任务执行前重跑 discovery；
把上一次任务的 model 值直接复用到新任务前，先确认它仍在白名单中。
