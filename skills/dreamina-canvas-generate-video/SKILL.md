---
name: dreamina-canvas-generate-video
description: Use when an agent or script must save or run a Dreamina Canvas video node with mode t2v, first_last_frame, or m2v. Never accepts i2v or multi_modal as a mode. Preserves user-requested ratios only when the discovered model contract permits them.
license: Complete terms in LICENSE
---

# Dreamina Canvas Video Node

This Skill owns the **Canvas video node**. It exists so that video
references, modes, and ratio constraints are correct without confusing
`i2v` (which does not exist) with `m2v`, or `multi_modal` (a server
internal alias) with the public mode set.

Reference detail is in
[references/video-node-contract.md](references/video-node-contract.md).

## When to use

- The caller wants to save a video draft (t2v, first_last_frame, or m2v).
- The caller wants to edit an existing video node, including replacing
  the entire generation block.
- The caller wants to switch modes on an existing draft and needs the
  reference rules explained.

## When **not** to use

- For approving or running generation — that is `dreamina-canvas-quote-and-run`.
- For the audio track of a video — that is `dreamina-canvas-generate-audio`.

## Modes — the public set

```text
t2v               text-to-video
first_last_frame  one or two ordered frames
m2v               image / video / Element / multimodal guidance
```

There is **no `i2v` mode**. The server-internal alias `multi_modal` must
not be passed; the CLI rejects it with exit code 2. Image-to-video,
video-guided generation, Element references, and "single image to video
with a preserved ratio" all use `m2v`.

```bash
# t2v
dreamina-canvas --format json node create video \
  --prompt "<prompt>" \
  --mode t2v --model <m> --ratio <r> --resolution <res> --duration 5

# first_last_frame (one frame)
dreamina-canvas --format json node create video \
  --prompt "<transition prompt>" \
  --mode first_last_frame --model <m> \
  --ref node:<firstFrameNodeId> --duration 5

# first_last_frame (two frames)
dreamina-canvas --format json node create video \
  --prompt "<transition prompt>" \
  --mode first_last_frame --model <m> \
  --ref node:<firstFrameNodeId> --ref node:<lastFrameNodeId> --duration 5

# m2v (image / video / Element guidance)
dreamina-canvas --format json node create video \
  --prompt "<motion prompt>" \
  --mode m2v --model <m> \
  --ref node:<imageOrVideoNodeId> --duration 5
```

## `--duration`

Mandatory for any video draft in seconds, must be `> 0`, default 5.
Take the upper bound from the discovered model spec; do not invent.

## `--ratio`

Some video models reject an explicit `--ratio` (for example, image- and
frame-driven modes follow the source frame ratio). Discovery wins; if the
model spec says the ratio is inferred from the first frame, do **not**
pass `--ratio`.

## `first_last_frame` rules

- One or two `--ref` entries are allowed.
- When two frames are supplied the source ratios of the two images must
  match.
- The output ratio is determined by the **first** frame; passing two
  frames with mismatched ratios is rejected by the server.

## Reference rules

Same surface as `dreamina-canvas-generate-image`:

- `node:node_xxx` — follow the node (canvas edge).
- `res:<lowercase UUID>` — freeze to a specific resource.
- `uri:` / `vid:` — reserved, rejected.
- Internal short links (`video_xxx`, `image_xxx`) — rejected.

Video nodes may reference Image, Element, or Video nodes/resources.

## Generation is a full replace

Identical to image:

- Touching `--mode`, `--model`, `--ratio`, `--resolution`, `--duration`,
  `--count`, `--prompt`, `--ref` requires the **complete** new block.
- Metadata is sparse; only the flags you pass are updated.
- `--clear-generation` is the opt-out (mutually exclusive with
  generation flags).

## Paid execution is not this Skill's job

Hand off to `dreamina-canvas-quote-and-run`. This Skill never calls
`--run`, never sets `--credit-ceiling` or `--credit-token`, never
persists tokens.

## Failure → recovery

| Failure | requiredAction | What to do next |
|---------|----------------|-----------------|
| `--mode i2v` rejected (exit 2) | none | Switch to `m2v`. |
| `--mode multi_modal` rejected (exit 2) | none | Switch to `m2v`. |
| Two-frame `first_last_frame` ratios disagree (exit 2) | none | Pick two frames with matching source ratios. |
| Explicit `--ratio` rejected by the model (exit 2) | none | Re-run discovery; remove `--ratio` if the model infers from the first frame. |
| Missing `--duration` (exit 2) | none | Pass `--duration` (default 5, model bound applies). |

## What this Skill will not do

- Approve spend.
- Persist tokens, signed URLs, cookies, or session material.
- Accept `i2v` or `multi_modal` as a mode.
- Treat generation edits as a partial update.

## Policy

Invocation requires:
- Confirmed installation of dreamina-canvas
- Live model discovery result for video
- For paid execution: explicit handoff to dreamina-canvas-quote-and-run

Forbids:
- Passing --mode i2v or --mode multi_modal
- Calling --run from this Skill
- Supplying --credit-ceiling or --credit-token
- Persisting tokens, signed URLs, cookies, or session material

Default prompt:

> Public video modes are t2v, first_last_frame, m2v. There is no i2v and
> no multi_modal --mode value. When the user says 'image to video' or
> wants to preserve a ratio, use m2v. Hand off paid execution.
>

<!-- QUALITY_BASELINE_V1 -->
## When to use（什么时候使用）

当用户需要 **在明确输入、预算和交付约束后执行生成或写入操作** 时加载本技能。先从请求中提取目标、输入、约束、交付格式和验收标准；描述摘要为：Use when an agent or script must save or run a Dreamina Canvas video node with mode t2v, first_last_frame, or m2v. Never accepts i2v or multi_modal as a mode. Preserves user-requested ratios only when the discovered model contract permits them.。

## Rules

- 先读后写：先确认当前状态与真实能力，再执行会改变外部状态的动作。
- 权限最小化：只使用完成当前步骤所需的文件、工具、账户与网络范围。
- 证据优先：运行结果、资源 ID、版本、哈希或测试输出缺失时，明确标记为 `NOT_VERIFIED`。
- 幂等优先：保留请求标识与阶段状态；结果不明确时先查询，不进行盲目重试。
- 隐私安全：日志、示例、回执和错误信息不得包含 token、cookie、密钥或个人敏感数据。

## Workflow

### Step 1：澄清意图

确认本技能是否匹配目标；若只是相邻需求，交给更精确的技能。
### Step 2：执行预检

校验输入、模型/工具能力、输出路径、预算上限和审批状态；任一关键条件未知时停止在只读阶段。
### Step 3：形成计划

列出将调用的工具、会改变的对象、成功标准以及失败后的安全退出方式。
### Step 4：执行动作

按一次批准执行并记录请求标识；模糊结果先查询而不是重提；每个外部调用均保留可关联的状态或回执。
### Step 5：验证交付

验证产物存在性、格式、哈希/标识、成本状态和质量门禁，并把事实、推断和未验证项分开陈述。

## Validation checklist

- [ ] 技能触发条件与用户意图一致，没有把相邻任务误路由到本技能。
- [ ] 输入、目标对象、版本和输出位置均已明确，且没有使用猜测值替代必填值。
- [ ] 所有写入、付费、发布或不可逆动作都在用户授权范围内。
- [ ] 结果已用独立检查验证；仅有“命令成功”或“文件存在”不算完整验收。
- [ ] 输出包含实际证据、失败/跳过项、剩余风险和可执行的下一步。

## Gotchas

1. **把计划当结果**：文档或提示词不等于真实执行；必须标明实际运行层级。
2. **错误重试**：超时或响应丢失可能已经产生远端状态，先查询再决定是否重试。
3. **隐式扩大范围**：批量、全量、发布、覆盖和付费不是普通读写的自然延伸。
4. **版本漂移**：引用外部资源时记录版本、tag 或提交；不要把可变分支当发布证据。
5. **证据过期**：缓存、旧截图和历史测试不能证明当前环境；在交付前刷新关键证据。

## 不适用与边界

付费、发布、覆盖、上传或外部写入必须使用当前任务的显式授权；不自动扩大次数和预算。 如果请求需要别的技能，不复制其正文；按技能名称进行交接，并保留当前任务上下文。

## Progressive disclosure

- 需要确定输入/输出、状态和授权点时，读取 `references/workflow-contract.md`。
- 需要交付前自检时，读取 `references/validation-checklist.md`。
- 遇到超时、部分成功或恢复场景时，读取 `references/error-recovery.md`。
- 首次运行、拒绝越权和失败恢复分别参考 `examples/happy-path.md`、`examples/boundary-refusal.md`、`examples/failure-recovery.md`。
