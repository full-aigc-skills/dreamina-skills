---
name: dreamina-canvas-compose
description: Use when an agent or script must save a multi-node Canvas graph (Text, Element, Image, Video, Audio, Timeline) for later approval, without performing any paid execution. Owns dependency order and batch planning.
license: Complete terms in LICENSE
---

# Dreamina Canvas Composition

This Skill owns the **non-charging** side of Canvas structure. It saves
nodes in dependency order, persists every returned `nodeId`, and hands off
the run to `dreamina-canvas-quote-and-run` after the user has reviewed the
full graph.

Reference detail is in
[references/composition-dag.md](references/composition-dag.md).

## When to use

- The caller wants to assemble a Canvas with multiple nodes of different
  types and explicit dependencies.
- The caller wants a saved, runnable DAG before approving any spend.
- The caller wants explicit run batches (because `node run` does not do
  DAG scheduling on its own).

## When **not** to use

- For actually running the graph — that is
  `dreamina-canvas-quote-and-run` after this Skill saves the structure.
- For a single media node — call `dreamina-canvas-generate-image` /
  `…video` / `…audio` directly.

## Default-only-save contract

Saving a node never implies running it. This Skill never:

- Calls `--run`.
- Sets `--credit-ceiling` or `--credit-token`.
- Persists tokens.
- Approves spend on the user's behalf.

The composed canvas is **only** the saved structure. Paid execution is a
separate step the user must explicitly authorise.

## Dependency order

Create upstream nodes **before** downstream ones that reference them.
The returned `nodeId` from an upstream node becomes the `--ref
node:<nodeId>` of a downstream node.

```text
Element / Text / Image (referenced by downstream nodes)
  → Image / Video / Audio (consume the references)
    → Timeline (consumes the visual / audio references)
```

The Skill persists every returned `nodeId` keyed by a stable caller
alias. Never re-derive a `nodeId` from memory — read it from the response.

## Text and Element commands

This Skill owns non-generating Text and Element structure:

```bash
dreamina-canvas --format json node create text \
  --title "<title>" --text "<body>"
dreamina-canvas --format json node edit text \
  --node-id <textNodeId> --text "<new body>"

dreamina-canvas --format json node create element \
  --title "<title>" --main <imageNodeId>
dreamina-canvas --format json node edit element \
  --node-id <elementNodeId> --voice <audioNodeId> \
  --auxiliary <otherImageNodeId>
```

Element slots accept bare Node IDs or resource UUIDs, not `node:`/`res:`
syntax. Validate every binding against the live schema and resolved media type;
do not duplicate one image in both main and auxiliary slots.

## Locate and inspect nodes

Use `node find` for filtered summaries and `node show` for full views before
composing references:

```bash
dreamina-canvas --format json node find --type image --status success --limit 50
dreamina-canvas --format json node show --node-id <nodeId>
```

## Reference syntax on the canvas

- `node:node_xxx` — follow the node; creates a canvas edge. Used in
  `--ref` for Image / Video / Audio / Timeline nodes, and inside prompt
  placeholders `{{node:node_xxx}}`.
- `res:<lowercase UUID>` — frozen reference; no edge. Used when the
  caller wants to pin a specific resource rather than follow a node.
- Element slot bindings (`--main`, `--voice`, `--auxiliary`,
  `--description`) take **bare** node ids or lowercase UUIDs. Do **not**
  prefix with `node:` / `res:`; the CLI rejects with
  `cli.invalid_resource_reference`.
- `uri:` / `vid:` — reserved, rejected.

## Element vs frozen resource

Element bindings have two modes (the response's `bindingMode` echoes
which one was chosen):

| Input | Meaning | `bindingMode` |
|-------|---------|---------------|
| `node_xxx` | follow the source node; reference tracks regeneration | `follow_node` |
| `<lowercase UUID>` | freeze to the resource at write time | `frozen_resource` |

If you have a node id but want to freeze the resource as of "now", do:

```bash
RES_ID=$(dreamina-canvas --format json node show --node-id <nodeId> \
  | jq -r '.data.resourceId')
# then pass $RES_ID (bare) into the slot
```

This Skill documents the rule; binding creation is owned by
`dreamina-canvas-generate-image` / `…video` etc.

## DAG scheduling is the caller's job

`node run` does not perform DAG scheduling. The Skill must build explicit
topological run batches before any paid execution:

1. Group nodes by layer: layer 0 has no incoming `node:` references,
   layer N+1 only references layers `≤ N`.
2. Submit each layer as one `node run` invocation with the
   corresponding `--node-id` set.
3. Persist each layer's `submitId` and wait for terminal state before
   the next layer (see `dreamina-canvas-resume-operation`).
4. Hand each layer to `dreamina-canvas-quote-and-run` with the user's
   approved ceiling.

## Failure → recovery

| Failure | requiredAction | What to do next |
|---------|----------------|-----------------|
| `node create` returns a different `nodeId` than expected | none | Stop; re-read the response, treat as contract violation. |
| Downstream reference (`node:<id>`) rejected | none | Verify the upstream `nodeId` was persisted and reused exactly. |
| `node:foo` passed to an Element slot | none | Strip the `node:` prefix; pass bare id or resource UUID. |
| `multi_modal` or `i2v` passed to a video node | none | Switch to `m2v` / correct public mode. |

## What this Skill will not do

- Approve spend or call `--run`.
- Persist tokens, signed URLs, cookies, or session material.
- Mint a `submitId`; the run batches only describe which nodeIds to
  quote / confirm / run.
- Schedule the DAG server-side; it does not happen.

## Policy

Invocation requires:
- Confirmed installation of dreamina-canvas
- A user-approved canvas structure plan
- For paid execution: explicit handoff to dreamina-canvas-quote-and-run

Forbids:
- Calling --run from this Skill
- Supplying --credit-ceiling or --credit-token
- Persisting tokens, signed URLs, cookies, or session material
- Assuming node run performs DAG scheduling
- Re-deriving a nodeId from memory; always read it from the response

Default prompt:

> Compose the canvas as a saved graph. Create upstream nodes before
> downstream references. Persist every nodeId. Plan explicit run
> batches because node run does not perform DAG scheduling. Hand off
> paid execution to dreamina-canvas-quote-and-run.
>

<!-- QUALITY_BASELINE_V1 -->
## When to use（什么时候使用）

当用户需要 **在明确输入、预算和交付约束后执行生成或写入操作** 时加载本技能。先从请求中提取目标、输入、约束、交付格式和验收标准；描述摘要为：Use when an agent or script must save a multi-node Canvas graph (Text, Element, Image, Video, Audio, Timeline) for later approval, without performing any paid execution. Owns dependency order and batch planning.。

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
