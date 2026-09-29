# Workflow Patterns — Canvas Image-to-Image

> 含素材摄入、i2i 编辑、迭代与 upscale 的标准模式。
> 付费步骤一律发生在 `dreamina-canvas-cli`（upscale 自身报价链除外）。

---

## 工作流 1：单图风格迁移（最常用）

**场景**: 用户给一张本地图，要换风格/改图

```bash
# 1. 三检 + discovery（model list --type image）
# 2. 上传并冻结
dreamina-canvas --format json resource upload --file "$PWD/photo.jpg" --name "photo"
# → 持久化 res:<uuid>

# 3. i2i 草稿（prompt 交接 dreamina-prompt-image2image 定稿）
dreamina-canvas --format json node create image \
  --title "photo-水墨" --prompt "<finalized prompt>" \
  --mode i2i --model <model> \
  --ratio <ratio> --resolution <resolution> \
  --ref res:<frozenResourceUuid> --count 1
# → 持久化 nodeId

# 4. 交接 quote-and-run：quote → 批准 → run
# 5. 交接 resume-operation / download-assets
```

**适用**: 改图、换风格、海报化。

---

## 工作流 2：批量统一风格（同一 res 引用，多草稿）

**场景**: 一组照片统一转成同一风格

```bash
# 1. 每张图各自 upload（各自 res:<uuid>）
# 2. 逐张建 i2i 草稿，prompt 相同、引用各自 res:
# 3. 交接 quote-and-run 批量报价 → 一次批准 → node run（每 node 一个 submitId）
```

**要点**: 风格一致性靠 prompt 与同一 model；不要试图用"一个节点多引用"
代替多草稿——i2i 参考数量有上限，且独立草稿便于单独重跑某一张。

---

## 工作流 3：画布节点重风格（全量替换编辑）

**场景**: 画布上已有图像节点，要在保留节点身份的前提下重做

```bash
# 1. 读回当前生成块（避免漏传）
dreamina-canvas --format json node show --node-id <nodeId>

# 2. 全量替换编辑
dreamina-canvas --format json node edit image \
  --node-id <nodeId> \
  --prompt "<new prompt>" --mode i2i \
  --model <model> --ratio <ratio> --resolution <resolution> --count <n> \
  --ref res:<frozenResourceUuid>

# 3. 重新 quote → 重新批准 → run（新一轮计费）
```

**红线**: 生成编辑漏传 flag = 清空该项；只改标题等元数据才允许稀疏更新。

---

## 工作流 4：挑图 → 再编辑 → 高清放大

**场景**: i2i 出图满意后，要高清版交付

```bash
# 1. i2i 产物节点 <resultNodeId>
# 2. （可选）对产物再做一轮 i2i 微调 —— 同工作流 3
# 3. upscale 干跑（免费；契约在 dreamina-canvas-cli）
dreamina-canvas --format json node upscale image \
  --node-id <resultNodeId> --mode <m> --resolution <r> --dry-run

# 4. 展示 upscale 报价（独立一笔）→ 用户精确批准 → 执行
#    产物是新节点 <upscaledNodeId>；源节点保持不变
# 5. 下载 <upscaledNodeId> 的最新资源 + SHA-256
```

**要点**: i2i 与 upscale 是两次独立计费；upscale 批准 token 与
`node confirm` 不通用。

---

## 工作流 5：多图参考（主体 + 风格分离）

**场景**: 用户给两张图——"把这个主体放进这种风格里"

```bash
dreamina-canvas --format json resource upload --file "$PWD/subject.png" --name "subject"  # → res:S
dreamina-canvas --format json resource upload --file "$PWD/style.png"   --name "style"    # → res:T

dreamina-canvas --format json node create image \
  --title "主体+风格" --prompt "<组合意图>" \
  --mode i2i --model <model> \
  --ref res:<S> --ref res:<T> --count 1
```

**要点**: 参考顺序按 `--ref` 出现顺序；数量上限以 discovery 为准；
被拒（exit 2）时先重读负载确认约束，不要反复重试。

---

## 错误处理剧本

### 场景：`cli.invalid_generation_reference`（exit 2）
`res:` 后必须是 CLI 返回的小写 canonical UUID；`file://`、`uri:`、
`image_xxx` 短链一律非法。本地文件先 `resource upload`。

### 场景：i2i 缺图像引用（exit 2）
补 `--ref res:<uuid>`（或导入节点后用 `node:<nodeId>`）。

### 场景：upscale 用错 token（exit 2）
`node confirm` 的批准 token 对 upscale 无效；走 upscale 自身报价链。

### 场景：重风格后参数被清空
`node edit image` 全量替换漏传导致。恢复：`node show` 读回（若已覆盖
则以 discovery 默认重建）→ 整块回传修正。

### 场景：exit 20 / 21 / 22
同文生图任务：`operation wait` 同 submitId 续等 / 退避重试 / 交接用户
（附完整命令、报错、version、requestId）。

---

## 最佳实践

1. **先上传后引用**——Canvas 没有任何"直接引用本地路径"的入口。
2. **res 冻结、node 跟随**——要锁定某次产物用 `res:`，要保画布上下游用 `node:`。
3. **编辑前 node show**——全量替换前先读回当前块，防止手滑清空参数。
4. **upscale 单独报价**——独立定价、独立批准、新节点产物。
5. **每次 discovery**——i2i 参考约束随模型与版本变化。
6. **交付必带哈希**——`resource download` 后 SHA-256 校验。
