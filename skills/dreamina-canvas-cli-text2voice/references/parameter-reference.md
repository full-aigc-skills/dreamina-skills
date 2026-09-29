# Parameter Reference — Canvas Text-to-Voice

> 以 `dreamina-canvas schema` 与 live voice 目录为最终事实源。

## 全局 flag

同其他任务技能：`--format json`（必传）、`--non-interactive`、`--yes`、
`--profile`、`--region cn`。

## 音色发现：`voice list`

| 参数 | 必填 | 说明 |
|------|------|------|
| `--offset <n>` | 否 | 分页偏移，默认 0 |
| `--count <n>` | 否 | 每页条数（指南示例 50） |

分页翻完仍无目标音色 → 目录里不存在；不得臆造 voiceName。

## 草稿保存：`node create audio --mode tts`

| 参数 | 必填 | 取值/约束 |
|------|------|-----------|
| `--title` | 推荐 | 节点标题 |
| `--prompt` | 是 | 旁白文本，逐字进 `--prompt` |
| `--mode` | 是 | 恒为 `tts` |
| `--voice-name` | **是** | live `voice list` 返回的 voiceName |
| `--model` | **禁止** | TTS 由音色驱动，不传模型 |
| `--count` | **禁止** | 音频节点不接受 `--count` |
| `--duration` | 否 | 由文本长度与音色自然决定；不臆造 |
| `--run` | **本技能禁止** | 付费只发生在 quote-and-run |

## 付费链 / 观察 / 下载

与其他任务技能同构：`node quote` → `node confirm`（精确
`--credit-ceiling`）→ `node run`（每 node 一个稳定 `--submit-id`）→
`operation status/wait <submitId> --project-id <id>` →
`resource get/download <resourceId> --project-id <id>`。

```bash
dreamina-canvas --format json node create audio \
  --title "旁白" --prompt "欢迎使用即梦画布" \
  --mode tts --voice-name <voiceName>
```
