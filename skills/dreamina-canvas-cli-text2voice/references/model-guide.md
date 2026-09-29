# Voice & Model Guide — Canvas Text-to-Voice

> 音色目录是运行时事实：只从 live `voice list` 取，不背音色名、不复用
> 旧对话里的 voiceName。

## 发现流程

```bash
dreamina-canvas --format json voice list --offset 0 --count 50
```

- 用 `--offset` / `--count` 翻页遍历；把候选音色（voiceName、风格描述）
  列给用户挑。
- `--voice-name` 填的是 payload 里的 **voiceName 字段值**，不是展示名。

## 选音色要点

| 场景 | 做法 |
|------|------|
| 旁白/解说 | 让用户在候选里选；描述差异（性别/年龄/风格）给用户听感预期 |
| 多角色配音 | 每个角色一个 tts 草稿、各自 voiceName；同一批准额度内连续执行 |
| 长文本 | 按语义拆成多段（单段过长可能超时或质量下降），逐段草稿 |

## tts 的模型问题

- **TTS 不传 `--model`**：音色本身绑定合成能力，模型由服务端按音色路由。
- 传了 `--model` 会被 exit 2 拒绝——这是指南 §4 明示的互斥规则。

## 计费

- tts 按次报价；先 `node quote` 展示，再精确批准。
- 多段旁白逐段报价、汇总展示总额，一次批准一个总额。

## 漂移处理

音色目录随版本扩充/调整；每次任务前重新 `voice list`，旧 voiceName
失效时换音色并告知用户。
