# Happy Path — 单段旁白端到端

用户：「把这段欢迎语文案配成女声旁白。」

```bash
# 0. 三检（dreamina-canvas-cli）
dreamina-canvas version
dreamina-canvas --format json schema
dreamina-canvas --format json auth account

# 1. 音色分页发现，列候选给用户挑
dreamina-canvas --format json voice list --offset 0 --count 50
# → 用户选定 <voiceName>

# 2. tts 草稿（文本逐字；--voice-name；不传 --model）
dreamina-canvas --format json node create audio \
  --title "欢迎语旁白" \
  --prompt "欢迎使用即梦画布" \
  --mode tts --voice-name <voiceName>
# → 持久化 nodeId；免费

# 3. 交接 dreamina-canvas-cli：quote → 批准 → run
# 4. 交接 dreamina-canvas-cli（operation wait）
# 5. 交接 dreamina-canvas-cli：下载 + SHA-256 + 时长核对
```

交付：nodeId、报价与批准上限、submitId、resourceId、本地路径 + 哈希 + 时长。
