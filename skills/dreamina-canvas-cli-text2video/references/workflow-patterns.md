# Workflow Patterns — Canvas Text-to-Video

> 文生视频任务的标准模式。视频生成耗时长、单价高，报价与终态确认
> 比图片任务更重要。

---

## 工作流 1：标准单次生成（最常用）

```bash
# 1. 三检 + discovery（model list --type video：时长上限/比例规则/分辨率）
# 2. prompt 含运动意图（未定稿先交接 dreamina-prompt-text2video）
# 3. 免费草稿
dreamina-canvas --format json node create video \
  --title "<title>" --prompt "<motion prompt>" \
  --mode t2v --model <model> --ratio <ratio> --duration 5
# → 持久化 nodeId

# 4. 交接 quote-and-run：quote（注明秒数/分辨率）→ 批准 → run
# 5. 交接 resume-operation：
dreamina-canvas --format json operation wait <submitId> --project-id <projectId> \
  --timeout 10m --interval 5s
# 6. 交接 download-assets：resource get / download + SHA-256
```

**适用**: 常规短片、单镜头素材。

---

## 工作流 2：多候选批量（同题多比例/多模型）

**场景**: 用户要 3 版同题视频挑一版

```bash
# 1. 逐版存草稿（t2v 无引用；比例/模型按白名单）
#    版 A：model_1 + 16:9；版 B：model_1 + 9:16；版 C：model_2 + 16:9
# 2. 交接 quote-and-run 逐节点报价，汇总展示（视频候选单价高，务必
#    逐条列出时长/分辨率/单价）
# 3. 一次精确总上限 → 逐 node run（各自 submitId）
# 4. 逐 submitId operation wait；视频等待时间长，exit 20 后换时间续等
```

**注意**: 视频批量费用高，批准前给用户"全跑/只跑 A+C"的裁剪选择。

---

## 工作流 3：镜头迭代（同节点多轮）

**场景**: 第一版运动幅度不够，要"再激烈一点"

```bash
# 1. node show 读回当前生成块
# 2. node edit video 全量替换（prompt 改运动描述；duration/model/ratio 一并重传）
# 3. 重新 quote → 重新批准 → run（新一轮计费）
```

**红线**: 与图片任务一致——编辑即全量替换；每轮都是新计费。

---

## 工作流 4：先保存后统一生成（画布工作流）

**场景**: 用户先搭整张画布（多个视频/图片节点），确认积分后统一生成

```bash
# 1. 全部节点只存草稿（不加 --run）
# 2. 让用户打开 webUrl 检查画布内容与参数
# 3. 逐节点 node quote，汇总展示总积分
# 4. 用户批准总额 → 逐 node run（每 node 一个 submitId）
# 5. 逐任务 operation wait；可并行等待多个 submitId
```

**适用**: 批量内容生产、先搭后付。这是 Canvas 相对旧 CLI 的核心优势之一。

---

## 错误处理剧本

### 场景：缺 `--duration`（exit 2）
补上时长（缺省 5，模型上限内）。

### 场景：显式 `--ratio` 被拒（exit 2）
该模型按比例推断：删掉 `--ratio` 重存草稿。

### 场景：时长超模型上限（exit 2）
换支持更长时长的模型，或分段生成；不要反复重试同参数。

### 场景：视频长时间无结果
任务可能仍在跑：exit 20 不是失败。保存 projectId/submitId，稍后
续等；同时把 webUrl 给用户，画布上也能看实时状态。**不要重提**——
新 submitId = 新计费。

### 场景：exit 22 / human_intervention
附四件套交接：完整命令、完整报错、`dreamina-canvas version`、
meta.requestId（生成任务再加 projectId/submitId）。

---

## 报价与额度管理（视频特化）

- 视频报价随 **模型 × 时长 × 分辨率 × count** 变化，展示时四项齐全。
- 多候选场景先给裁剪选择，再要总额批准。
- 同一批准额度内可连续执行；任何参数变化（时长/分辨率/数量）都应
  视为新报价重新确认。

## 最佳实践

1. **prompt 必带运动意图**——镜头词 + 主体动作 + 节奏，缺了效果不可控。
2. **duration 是模型属性**——超上限换模型，不硬闯。
3. **长任务善用 exit 20**——等待超时就续等，不取消也不重提。
4. **先画布后付费**——多节点场景先存草稿给用户看 webUrl 再统一生成。
5. **每次 discovery**——视频模型规格变动频繁。
6. **交付带时长与哈希**——终态以 resource get + SHA-256 为准。
