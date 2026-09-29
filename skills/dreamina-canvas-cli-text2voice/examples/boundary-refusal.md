# Boundary Refusal — 拒绝越权

## 场景 A：给 TTS 指定模型

用户：「用你们最强的模型来配这段音。」

- TTS 由 `--voice-name` 驱动，**不传 `--model`**（官方指南 §4 明示）；
  传了会被 exit 2 拒绝。
- 回复：音色本身就是合成能力的入口；要换效果就换 voiceName。

## 场景 B：一次出多个版本

用户：「同一段文字给我出 5 个版本挑。」

- 音频节点**不接受 `--count`**；多版本 = 多个草稿节点，各自计费。
- 回复：建 5 个 tts 草稿（可同 voiceName 也可不同）→ 批量报价 →
  总额批准 → 逐节点运行。

## 场景 C：要求免批准直跑

任何跳过报价与精确上限批准的执行请求一律拒绝；付费边界属于
`dreamina-canvas-cli`。

## 场景 D：音乐任务混入

用户：「顺便再生成一段背景音乐。」

- 音乐是 `dreamina-canvas-cli-text2audio`（`--mode music`，`--model`，
  不传 `--voice-name`）；两技能 flag 互斥，不共用一个命令。
