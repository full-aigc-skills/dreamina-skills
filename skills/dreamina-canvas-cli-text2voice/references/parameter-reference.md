# Parameter Reference — Canvas Text-to-Voice

> 以 `dreamina-canvas schema` 与 live voice 目录为最终事实源。公开版 1.0.3 起
> tts 存在 legacy 与 `--scenario` 场景两族形态；下列表格按形态区分。

## 全局 flag

同其他任务技能：`--format json`（必传）、`--non-interactive`、`--yes`、
`--profile`、`--region cn`。

## 音色发现：`voice list`

| 参数 | 必填 | 说明 |
|------|------|------|
| `--offset <n>` | 否 | 分页偏移，默认 0 |
| `--count <n>` | 否 | 每页条数，范围 1..100（指南示例 50） |
| `--model <canonical-model>` | 否 | 1.0.3 起可选：只返回该模型的音色目录；翻页保持同一模型 |

分页翻完仍无目标音色 → 目录里不存在；不得臆造 voiceName。

## 草稿保存：`node create audio --mode tts`

### legacy 形态（不传 `--scenario`）

| 参数 | 必填 | 取值/约束 |
|------|------|-----------|
| `--title` | 推荐 | 节点标题 |
| `--prompt` | 是 | 旁白文本，逐字进 `--prompt` |
| `--mode` | 是 | 恒为 `tts` |
| `--voice-name` | **是** | live `voice list` 返回的 voiceName |
| `--model` | **禁止** | legacy tts 由音色驱动；传 `--model` 必须同时传 `--scenario` |
| `--count` | **禁止** | 音频节点不接受 `--count` |
| `--duration` | 否 | 由文本长度与音色自然决定；不臆造 |
| `--run` | **本技能禁止** | 付费只发生在 quote-and-run |

### 场景形态（`--scenario`，公开版 1.0.3 起）

| 参数 | 必填 | 取值/约束 |
|------|------|-----------|
| `--scenario` | 场景形态必填 | `text-reading`（朗读）或 `omni-dubbing`（全能配音）；要求 `--mode tts` + 显式 `--model` |
| `--model` | **是** | 实时 `model list --type audio` 中声明支持场景的模型 |
| `--voice-name` | text-reading **是**；omni-dubbing 可选 | 全能配音下是单个目录音色，服务端转换为音频参考；从 `voice list --model` 选取 |
| `--ref` | omni-dubbing 可选 | 参考音频素材 `node:<id>` / `res:<id>`，可重复；与音色共享发现结果报告的参考上限；仅全能配音可用 |

## 付费链 / 观察 / 下载

与其他任务技能同构：`node quote` → `node confirm`（精确
`--credit-ceiling`）→ `node run`（每 node 一个稳定 `--submit-id`）→
`operation status/wait <submitId> --project-id <id>` →
`resource get/download <resourceId> --project-id <id>`。

```bash
# legacy 朗读
dreamina-canvas --format json node create audio \
  --title "旁白" --prompt "欢迎使用即梦画布" \
  --mode tts --voice-name <voiceName>

# 全能配音：选音色
dreamina-canvas --format json node create audio \
  --title "商品配音" --prompt "<口播文案>" --mode tts \
  --model <scenarioModel> --scenario omni-dubbing \
  --voice-name <voiceName>

# 全能配音：用参考素材（上传或已有音频节点）
dreamina-canvas --format json node create audio \
  --title "参考音色配音" --prompt "<口播文案>" --mode tts \
  --model <scenarioModel> --scenario omni-dubbing \
  --ref "node:<audioNodeId>"
```
