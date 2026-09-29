# Parameter Reference — Canvas Text-to-Audio (Music)

> 以 `dreamina-canvas schema` 与 live 音频模型目录为最终事实源。

## 全局 flag

同其他任务技能：`--format json`（必传）、`--non-interactive`、`--yes`、
`--profile`、`--region cn`。

## 模型发现：`model list --type audio`

- 只有 mode 列表包含 `music` 的音频模型可用于本任务（官方指南 §4）。
- 负载里的 duration 上限、分辨率/采样规格按模型读取。

## 草稿保存：`node create audio --mode music`

| 参数 | 必填 | 取值/约束 |
|------|------|-----------|
| `--title` | 推荐 | 节点标题 |
| `--prompt` | 是 | 风格/情绪描述（体裁+情绪+节奏+乐器） |
| `--mode` | 是 | 恒为 `music` |
| `--model` | **是** | 支持 music 模式的音频 model 值 |
| `--duration` | **是** | >0 秒；上限取该模型 discovery 规格 |
| `--voice-name` | **禁止** | 音乐是模型驱动，不传音色 |
| `--count` | **禁止** | 音频节点不接受 `--count` |
| `--run` | **本技能禁止** | 付费只发生在 quote-and-run |

## 付费链 / 观察 / 下载

与其他任务技能同构：`node quote` → `node confirm`（精确
`--credit-ceiling`）→ `node run`（每 node 一个稳定 `--submit-id`）→
`operation status/wait <submitId> --project-id <id>` →
`resource get/download <resourceId> --project-id <id>`。

```bash
dreamina-canvas --format json node create audio \
  --title "背景音乐" --prompt "轻快、有科技感的电子音乐" \
  --mode music --model <model> --duration <seconds>
```
