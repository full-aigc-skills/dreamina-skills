# Workflow Patterns — Canvas Reference-to-Video

> 素材摄入 + 模式选择 + 草稿 + 付费链的成段流程。
> 模式选择矩阵与决策树见 `model-guide.md`。

---

## 工作流 1：单图微动（m2v，最常用）

**场景**: 一张照片"动起来"

```bash
# 1. 三检 + discovery（model list --type video）
# 2. 上传帧
dreamina-canvas --format json resource upload --file "$PWD/photo.jpg" --name "photo"
# → 持久化 res:<uuid>（或导入节点后用 node:<nodeId>）

# 3. m2v 草稿
dreamina-canvas --format json node create video \
  --title "照片动起来" --prompt "<motion prompt>" \
  --mode m2v --model <model> \
  --ref res:<frozenResourceUuid> --duration 5
# 帧驱动模型按比例推断时不传 --ratio

# 4. 交接 quote-and-run → resume-operation → download-assets
```

**适用**: 微动化、产品展示、单素材短片。

---

## 工作流 2：首尾帧过渡（first_last_frame）

**场景**: 从画面 A 平滑变到画面 B

```bash
# 1. 分别上传首帧与尾帧（校验两帧源比例一致）
dreamina-canvas --format json resource upload --file "$PWD/start.png" --name "start"  # → res:S
dreamina-canvas --format json resource upload --file "$PWD/end.png"   --name "end"    # → res:E

# 2. 有序双引用草稿
dreamina-canvas --format json node create video \
  --title "首尾过渡" --prompt "<transition prompt>" \
  --mode first_last_frame --model <model> \
  --ref res:<S> --ref res:<E> --duration 5
# 输出比例跟随首帧；模型支持且与首帧一致时才传 --ratio

# 3. 交接 quote-and-run → resume-operation → download-assets
```

**变体**：只有首帧时传 1 个 `--ref`。

---

## 工作流 3：多帧叙事（拆节点 + 时间轴串接）

**场景**: 3 帧以上讲一个连续故事（旧 CLI 的 multiframe2video 无对应）

```bash
# 1. 相邻帧两两建 first_last_frame 草稿（或首帧 m2v + 后续帧过渡）
# 2. 每个草稿独立 quote/run（各自 submitId）
# 3. 全部完成后交接 dreamina-canvas-cli 把片段排进时间轴
#    （剪辑/拼接属于该技能域，本分技能不复制）
```

**要点**: Canvas 没有"一次多帧"入口；拆节点反而获得每段单独重跑、
单独计费的能力。

---

## 工作流 4：多模态参考（m2v）

**场景**: 图 + 视频/主体混合参考（旧 multimodal2video）

```bash
# 1. 每份素材各自 upload（res:A 图、res:B 视频…）
# 2. m2v 草稿按顺序传多个 --ref（数量/类型上限以 discovery 为准）
dreamina-canvas --format json node create video \
  --title "多模态" --prompt "<组合意图>" \
  --mode m2v --model <model> \
  --ref res:<A> --ref res:<B> --duration 5
```

**要点**: 被拒（exit 2）时重读 discovery 负载的素材约束，不要重试同参。

---

## 工作流 5：先画布后统一生成

**场景**: 一整组镜头草稿搭好后统一批准生成

```bash
# 1. 全部镜头只存草稿（m2v / first_last_frame 混合）
# 2. 给用户 webUrl 检查
# 3. 逐节点 quote 汇总 → 总额批准 → 逐 node run
# 4. 并行 operation wait 多个 submitId
```

---

## 错误处理剧本

### 场景：`--mode i2v` / `multi_modal` 被拒（exit 2）
改 `m2v` 或 `first_last_frame`；这两个值在 Canvas 不存在。

### 场景：双帧比例不一致（exit 2）
裁/补一致再传；或退回单帧 m2v。

### 场景：引用非法（exit 2）
先 `resource upload`；用 `res:<lowercaseUuid>` 或导入节点 `node:<nodeId>`。

### 场景：模型拒绝显式 `--ratio`（exit 2）
删 `--ratio`；帧驱动模型按首帧推断。

### 场景：缺 `--duration`（exit 2）
补时长（缺省 5，模型上限内）。

### 场景：exit 20 / 21 / 22
同文生视频：`operation wait` 同 submitId 续等 / 退避重试 / 交接用户
（四件套：完整命令、报错、version、requestId）。

---

## 最佳实践

1. **先决策模式再动命令** —— 素材形态决定 m2v / first_last_frame，不由旧习惯决定。
2. **双帧先校比例** —— 上传前本地校验两帧比例，省一轮 exit 2。
3. **node 跟随、res 冻结** —— 画布节点用 `node:`，锁定外部素材用 `res:`。
4. **每镜头独立节点** —— 单独重跑、单独计费、单独交付。
5. **discovery 每任务必跑** —— 素材类型/数量上限是服务端属性。
6. **交付带时长与哈希** —— resource get + SHA-256 才算终态。
