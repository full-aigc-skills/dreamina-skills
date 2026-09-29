# Audio Model Guide — Canvas Text-to-Audio (Music)

> 音频模型目录是运行时事实：只从 live `model list --type audio` 取。

## 发现流程

```bash
dreamina-canvas --format json model list --type audio
```

- 过滤条件：mode 列表包含 `music`。TTS-only 模型不能用于本任务。
- 读负载：duration 上限、可用规格。

## 选模型与时长要点

| 场景 | 做法 |
|------|------|
| 短 BGM 循环 | 选 music 模式默认模型，时长 15–30s |
| 主题曲/片头 | 按 duration 上限筛模型；prompt 写清结构与情绪走向 |
| 特定体裁 | prompt 层解决（"中国风民乐 + 弦乐"）；模型差异以 discovery 为准 |

## prompt 写法（音乐特有）

- 具体优于笼统：`"轻快、有科技感的电子音乐，120 BPM，合成器为主"`
  优于 `"电子音乐"`。
- 写清情绪走向（"前奏舒缓，副歌激昂"）可获得更有结构的成品。
- 避免歌词请求：music 模式产出纯音乐；带歌词的歌曲不在本任务范围。

## `--duration` 纪律

- 必填、>0；上限是模型属性，超出 exit 2。
- 交付核对产物时长与请求值一致；不符标 `NOT_VERIFIED`。

## 计费

- 按时长/模型报价；先 `node quote` 展示（注明秒数与体裁），再精确批准。
- 多轨 BGM 逐轨报价、汇总总额。

## 漂移处理

音频模型上下架频繁；每次任务前重跑 discovery，旧 model 值复用前确认
仍在列表且仍支持 music 模式。
