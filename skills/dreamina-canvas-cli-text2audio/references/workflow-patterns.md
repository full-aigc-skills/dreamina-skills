# Workflow Patterns — Canvas Text-to-Audio (Music)

> 音乐生成任务的标准模式。

---

## 工作流 1：标准单曲（最常用）

```bash
# 1. 三检 + model list --type audio（过滤 music 模式）
dreamina-canvas --format json model list --type audio

# 2. music 草稿（--model + --duration；不传 --voice-name）
dreamina-canvas --format json node create audio \
  --title "背景音乐" --prompt "<style / mood description>" \
  --mode music --model <model> --duration <seconds>
# → 持久化 nodeId

# 3. 交接 quote-and-run：quote → 批准 → run
# 4. 交接 resume-operation：operation wait
# 5. 交接 download-assets：resource get / download + SHA-256 + 时长核对
```

---

## 工作流 2：多轨 BGM（同项目多段）

**场景**: 一款视频要片头/过渡/片尾三段不同 BGM

```bash
# 1. 三段各自 discovery + 草稿（可同模型不同 prompt，也可不同模型）
# 2. 交接 quote-and-run：逐节点 quote → 汇总总额 → 一次批准
# 3. 逐 node run → 逐 operation wait → 逐下载校验
# 4. 交付按"片头/过渡/片尾"命名，附各自 resourceId
```

---

## 工作流 3：变体探索

**场景**: 用户要"同风格但两个版本，一快一慢"

```bash
# 1. 两个草稿：prompt 分别写 "快节奏/慢节奏"，时长可不同
# 2. 批量报价 → 总额批准 → 逐节点运行
# 3. 交付两版 + 差异说明（BPM 提示词差异）
```

**要点**: 变体 = 多个草稿节点；不存在 `--count` 一把出多版。

---

## 错误处理剧本

### 场景：传了 `--voice-name`（exit 2）
删掉；音乐是模型驱动。

### 场景：模型不支持 music（exit 2）
重跑 `model list --type audio`，换 music 模式模型。

### 场景：duration 超上限（exit 2）
取 discovery 的模型上限内时长，或换支持更长时长的模型。

### 场景：exit 10 / 11 / 20 / 21 / 22
与其他任务技能一致：展示报价等批准 / 重认证 / 同 submitId 续等 /
退避重试 / 四件套交接用户。

---

## 最佳实践

1. **prompt 四要素**——体裁+情绪+节奏+乐器，具体优于笼统。
2. **music 模型先过滤**——不是所有音频模型都支持 music。
3. **时长核对**——产物时长与 `--duration` 不符标 `NOT_VERIFIED`。
4. **多轨命名交付**——按用途命名（片头/BGM/片尾），附 resourceId。
5. **每次 discovery**——音频模型目录漂移频繁。
