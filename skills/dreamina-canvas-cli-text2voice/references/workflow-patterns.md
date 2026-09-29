# Workflow Patterns — Canvas Text-to-Voice

> TTS 任务的标准模式。音频任务体量小、单价低，但多段旁白的组织与
> 音色一致性是主要复杂度。

---

## 工作流 1：标准单段旁白（最常用）

```bash
# 1. 三检 + voice list 翻页选音色
dreamina-canvas --format json voice list --offset 0 --count 50

# 2. tts 草稿（文本逐字、--voice-name、不传 --model）
dreamina-canvas --format json node create audio \
  --title "旁白" --prompt "<narration text>" \
  --mode tts --voice-name <voiceName>
# → 持久化 nodeId

# 3. 交接 quote-and-run：quote → 批准 → run
# 4. 交接 resume-operation：operation wait
# 5. 交接 download-assets：resource get / download + SHA-256 + 时长合理性
```

---

## 工作流 2：多段旁白批量配音

**场景**: 一段文案拆 5 段，同一音色

```bash
# 1. 同一 voiceName 建 5 个 tts 草稿（title 标第几段）
# 2. 交接 quote-and-run：逐节点 quote → 汇总总额 → 一次批准
# 3. 逐 node run（各自 submitId）→ 逐 operation wait
# 4. 按段下载校验；命名带序号便于拼接
```

**要点**: 分段靠语义边界（句子/段落），不要在词中间切断；拼接归
用户侧或时间轴技能域。

---

## 工作流 3：多角色对话配音

**场景**: 两个角色交替的文案

```bash
# 1. voice list 选两个音色（角色 A / 角色 B），列给用户确认
# 2. 按台词归属建草稿：A 的台词 --voice-name <A>，B 的台词 <B>
# 3. 批量报价 → 总额批准 → 逐节点运行下载
```

**要点**: 角色与音色的映射关系写入交付说明，避免用户后期对不上。

---

## 错误处理剧本

### 场景：传了 `--model`（exit 2）
删掉 `--model`；TTS 只由 `--voice-name` 驱动。

### 场景：voiceName 不存在（exit 2）
重新 `voice list` 取当前目录的 voiceName；旧名字失效就换音色并告知用户。

### 场景：传了 `--count`（exit 2）
删掉；音频节点不接受 `--count`。

### 场景：exit 10 / 11 / 20 / 21 / 22
与其他任务技能一致：展示报价等批准 / 重认证 / 同 submitId 续等 /
退避重试 / 四件套交接用户。

---

## 最佳实践

1. **文本逐字进 prompt**——旁白是定稿文案，不静默改写、不擅自缩写。
2. **音色每次重查**——目录会漂移；旧 voiceName 不保证存在。
3. **多段先拆语义边界**——按句/段切分，段间留拼接余地。
4. **交付带时长**——旁白时长与文本长度明显不符时标记 `NOT_VERIFIED`。
5. **submitId 永不重铸**——续等复用同一 ID。
