# Happy Path — 背景音乐端到端

用户：「给产品视频配一段 30 秒科技感 BGM。」

```bash
# 0. 三检（dreamina-canvas-cli）
dreamina-canvas version
dreamina-canvas --format json schema
dreamina-canvas --format json auth account

# 1. 发现支持 music 模式的音频模型
dreamina-canvas --format json model list --type audio
# → 选定 <model>，记录其 duration 上限

# 2. music 草稿（--model + --duration；不传 --voice-name）
dreamina-canvas --format json node create audio \
  --title "产品视频BGM" \
  --prompt "轻快、有科技感的电子音乐，120 BPM，合成器为主" \
  --mode music --model <model> --duration 30
# → 持久化 nodeId；免费

# 3. 交接 dreamina-canvas-cli：quote（注明秒数）→ 批准 → run
# 4. 交接 dreamina-canvas-cli（operation wait）
# 5. 交接 dreamina-canvas-cli：下载 + SHA-256 + 时长核对
```

交付：nodeId、报价与批准上限、submitId、resourceId、本地路径 + 哈希 + 时长。
