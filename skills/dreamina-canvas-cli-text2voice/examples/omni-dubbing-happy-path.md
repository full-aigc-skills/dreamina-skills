# Happy Path — 全能配音（选音色或参考素材，公开版 1.0.3 起）

用户：「用全能配音给这段口播文案配音，音色照我给的这段参考音频来。」

```bash
# 0. 三检（dreamina-canvas-cli）
dreamina-canvas version
dreamina-canvas --format json schema
dreamina-canvas --format json auth account

# 1. 发现支持场景的音频模型；把候选模型给用户确认
dreamina-canvas --format json model list --type audio
# → 用户选定 <scenarioModel>（必须来自实时结果，不背模型名）

# 2. 用户选择音色来源：
#    a. 选一个目录音色：voice list --model <scenarioModel> 翻页列候选
dreamina-canvas --format json voice list --model <scenarioModel> \
  --offset 0 --count 50
#    b. 用参考音频：上传素材后以节点或资源引用
dreamina-canvas --format json resource upload --file ./reference.wav \
  --name "参考音频"

# 3. omni-dubbing 草稿（二选一：--voice-name 或 --ref；可并存，受参考上限约束）
dreamina-canvas --format json node create audio \
  --title "商品口播" \
  --prompt "<逐字确认的口播文案>" \
  --mode tts --model <scenarioModel> --scenario omni-dubbing \
  --ref "node:<参考音频节点ID>"
# → 持久化 nodeId；免费

# 4. 交接 dreamina-canvas-cli：quote → 用户批准 ceiling → run
# 5. 交接 dreamina-canvas-cli（operation wait）
# 6. 交接 dreamina-canvas-cli：下载 + SHA-256 + 时长核对
```

要点：`--scenario` 必须与显式 `--model` 成对；`--ref` 仅全能配音可用；
用户只给方向不给音色时先列候选再生成。交付物同 legacy 路径：nodeId、
报价与批准上限、submitId、resourceId、本地路径 + 哈希 + 时长。
