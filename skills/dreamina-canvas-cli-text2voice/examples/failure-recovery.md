# Failure Recovery — 模式互斥与运行中断

场景：tts 草稿保存返回 exit 2。

```bash
# 错误：沿图片/视频任务的习惯传了 --model（或 --count）
dreamina-canvas --format json node create audio \
  --prompt "<text>" --mode tts --voice-name <voiceName> --model <model>
# 正确：删掉 --model（--count 同理）；TTS 只认 --voice-name
dreamina-canvas --format json node create audio \
  --prompt "<text>" --mode tts --voice-name <voiceName>
```

场景：voiceName 不存在（exit 2）。

```bash
# 重跑音色目录，取当前 voiceName；旧名失效则换音色并告知用户
dreamina-canvas --format json voice list --offset 0 --count 50
```

场景：付费运行后断开，退出码 20。

```bash
# 同一 submitId 续等（dreamina-canvas-cli）
dreamina-canvas --format json operation wait <stableUuid> --project-id <projectId>
# 21 → 退避重试同一 ID；22 → 连同 nodeId/submitId 交接用户
```
