# Model Guide — Canvas Text-to-Video

> 视频模型的差异比图片大：时长上限、比例规则、分辨率档位各不相同，
> 只从 live discovery 取。

## 发现流程

```bash
dreamina-canvas --format json model list --type video
dreamina-canvas --format json model find "<关键字>" --type video
```

读负载时锁定三个字段：**duration 上限**、**ratio 规则**（显式支持 vs
按首帧/模型推断）、**resolution 档位**。

## 选模型要点

| 场景 | 做法 |
|------|------|
| 常规短片 | discovery 默认视频模型，时长 5s 起步 |
| 长镜头 | 先按 duration 上限筛模型；prompt 写清镜头运动避免"静止感" |
| 特定画幅（如竖屏） | 按 ratio 白名单筛；白名单外比例 exit 2，重试无用 |
| 高画质 | 按 resolution 档位筛；同时确认时长与画幅仍受支持 |

## `--duration` 纪律

- 必填、>0、缺省 5；**上限是模型属性**，不是参数——超出被拒 exit 2。
- 需要更长时长时换模型或分段生成（分段归时间轴/合成技能域）。
- 报价随时长增长显著上升；报价展示时注明秒数。

## `--ratio` 纪律

- 模型的 ratio 规则分两类：显式接受（可传）与自动推断（**不传**）。
- discovery 写明"按首帧/模型推断"时传了 `--ratio` 会被 exit 2 拒绝。
- t2v 无首帧可推断，多数模型要求显式比例；仍以 discovery 为准。

## prompt 纪律（视频特有）

- prompt 必须含**运动描述**：镜头（推/拉/摇/环绕）、主体动作、节奏。
- 纯静态画面描述会被模型"脑补"成微弱运动，效果不可控。
- 分镜、转场等复杂叙事先交接 prompt 技能拆成单镜头任务。

## 权益与计费

- 视频单价显著高于图片；不同模型价差也大。先 `node quote` 展示
  （含时长/分辨率），再精确批准。
- 白名单随账号权益变化；缺模型时先 `auth account` 再按 exit 12/13。

## 漂移处理

每次任务前重跑 discovery；时长上限与比例规则是服务端属性，会变。
被拒时重读负载，不要重复同一条命令。
