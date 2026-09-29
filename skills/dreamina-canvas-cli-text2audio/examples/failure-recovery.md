# Failure Recovery — 模式互斥与运行中断

场景：music 草稿保存返回 exit 2。

```bash
# 错误：沿用 TTS 的习惯传了 --voice-name（或传了 --count）
dreamina-canvas --format json node create audio \
  --prompt "<style>" --mode music --model <model> --duration 30 --voice-name <v>
# 正确：删掉 --voice-name（--count 同理）；music 只认 --model + --duration
dreamina-canvas --format json node create audio \
  --prompt "<style>" --mode music --model <model> --duration 30
```

场景：模型不支持 music 模式（exit 2）。

```bash
# 重跑音频模型目录，过滤 mode 含 music 的模型
dreamina-canvas --format json model list --type audio
```

场景：付费运行后断开，退出码 20。

```bash
# 同一 submitId 续等（dreamina-canvas-cli）
dreamina-canvas --format json operation wait <stableUuid> --project-id <projectId>
# 21 → 退避重试同一 ID；22 → 连同 nodeId/submitId 交接用户
```
