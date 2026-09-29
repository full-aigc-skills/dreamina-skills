# Model Guide — Canvas Image-to-Image

> 模型与参数是运行时事实：只从 live discovery 取。i2i 与 t2i 共用图像
> 模型池，但各模型对参考图数量/类型可能有额外约束，以 discovery 为准。

## 发现流程

```bash
dreamina-canvas --format json model list --type image
dreamina-canvas --format json model find "<关键字>" --type image
```

读返回负载时额外关注 i2i 相关字段：允许的参考类型（Image/Element）、
参考数量上限、是否要求显式 resolution。不同模型的约束不同。

## i2i 选模型要点

| 场景 | 做法 |
|------|------|
| 风格迁移/换风格 | prompt 描述目标风格；模型选 discovery 默认项即可，风格主要靠 prompt |
| 保持主体改背景 | prompt 明说"保持主体不变"；参考图给全（主体+背景源图） |
| 商品图改海报 | 单图 i2i + 强约束 prompt；高分辨率需求先筛 resolution 白名单 |
| 低清素材修复 | 源图先 `resource upload`；必要时对**产物**做 upscale（见下） |

## 参考图策略

- 画布上已有节点 → `node:<nodeId>`：源节点再生成时引用跟随，保上下游。
- 只要冻结某次产物 → `res:<resourceId>`：不受源节点变化影响。
- 多图参考（如主体+风格两张）→ 多个 `--ref` 按顺序传入；数量上限以
  discovery 为准，超出 exit 2。

## upscale 的模型问题

- upscale 不是选生成模型：走 `node upscale image` 自身的 mode /
  resolution 档位（如 pro），先 `--dry-run` 看 schema 与本地校验。
- `--detail` 仅 pro 档可用；非 pro 传了会被拒。
- upscale 产物是新节点；要再做 i2i 编辑时引用新节点。

## 权益与计费

- i2i 与 upscale 分别计费；upscale 通常接近一次生成的价格。
- 先 `node quote` 展示，再精确批准；同一节点先 i2i 再 upscale 是
  **两笔**独立报价，合并展示总额，但批准动作各自发生。
- 模型白名单随账号权益变化；discovery 缺模型时先 `auth account`。

## 漂移处理

每次任务前重跑 discovery；复用上次 model 值前确认其仍在白名单。
参考图约束（数量/类型）变动是服务端行为，本地无法预判，被 exit 2
拒绝时重读 discovery 负载而不是重试同一条命令。
