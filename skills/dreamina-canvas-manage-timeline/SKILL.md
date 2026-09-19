---
name: dreamina-canvas-manage-timeline
description: Use when an agent or script must build or edit a Dreamina Canvas timeline (visual clips and audio clips). Warns before track replacement because the server drops uncommitted changes and regenerates clip identities.
license: Complete terms in LICENSE
---

# Dreamina Canvas Timeline

This Skill owns the Canvas timeline node. A timeline has two tracks: a
visual track (`--clip`) and an audio track (`--audio-clip`). The most
common surprise is that **passing either flag rebuilds the corresponding
track**, throwing away any unsaved work and reissuing clip identities.

Reference detail is in
[references/timeline-contract.md](references/timeline-contract.md).

## When to use

- The caller wants to assemble a video with both visual and audio tracks
  on the canvas.
- The caller wants to swap an individual clip with explicit trim / speed
  / volume options.
- The caller wants a metadata-only edit (title / tags) without touching
  the tracks.

## When **not** to use

- For video generation parameters — that is `dreamina-canvas-generate-video`.
- For audio generation parameters — that is `dreamina-canvas-generate-audio`.
- For approval or paid execution — that is `dreamina-canvas-quote-and-run`.

## Create

```bash
dreamina-canvas --format json node create timeline --title "<title>" \
  --clip <visualNodeId1> \
  --clip <visualNodeId2>,trim=1000-4000,speed=2 \
  --clip <imageNodeId>,duration=3000 \
  --audio-clip <musicResourceId>,start=0,volume=0.5
```

- Either `--clip` or `--audio-clip` (or both) must be supplied on creation.
- An audio-only timeline is valid; the server adds an empty visual track
  for the canvas to remain consistent.

## Clip options

`--clip` and `--audio-clip` accept a comma-separated option list:

| Option | Applies to | Unit | Default |
|--------|------------|------|---------|
| `duration=<ms>` | image clips | milliseconds | canvas default image duration |
| `trim=<start>-<len>` | video / audio | milliseconds | full source duration |
| `speed=<factor>` | video / audio | multiplier | 1 |
| `volume=<0-1>` / `muted` | video / audio | boolean / fraction | full |
| `start=<ms>` | audio clips | milliseconds | 0 |

Omitted options are left empty and the server fills them in from the
source asset. Never guess duration or trim locally.

## Track replacement is destructive

This is the rule that trips every first-time caller:

> Supplying either `--clip` or `--audio-clip` to `node edit timeline`
> **rebuilds the corresponding track**. The server deletes the existing
> clips, re-creates them per the supplied list, and issues **new clip
> identities**. Any unsaved per-clip edits the user had on the original
> timeline are lost.

Before calling `node edit timeline` with either flag, the Skill must:

1. Confirm the user wants a full track replacement (not metadata-only).
2. Confirm the user accepts that clip identities will change.
3. Build the **complete** new list for the affected track; do not
   attempt to "add a clip" by mixing old and new.

If only the title / tags / description needs to change, do **not** pass
either `--clip` or `--audio-clip`.

## Metadata-only edit

```bash
dreamina-canvas --format json node edit timeline \
  --node-id <nodeId> \
  --title "<new title>"
```

Sparse update; the tracks are untouched.

## Clear tracks

```bash
dreamina-canvas --format json node edit timeline \
  --node-id <nodeId> \
  --clear-tracks
```

Mutually exclusive with `--clip` and `--audio-clip`.

## Reference syntax on the timeline

- `--clip` and `--audio-clip` take **bare** node IDs (`node_xxx`) or
  lowercase canonical UUIDs for resources. Do **not** use the `node:` or
  `res:` prefix — those return `cli.invalid_resource_reference` (exit 2).

## Paid execution

Hand off to `dreamina-canvas-quote-and-run`. This Skill never calls
`--run`.

## Failure → recovery

| Failure | requiredAction | What to do next |
|---------|----------------|-----------------|
| `node_xxx` rejected on `--clip` / `--audio-clip` | none | Verify the bare ID; do not add `node:` prefix. |
| Two frames disagree on ratio | none | Confirm `trim` / `duration` units are in milliseconds. |
| `--clip` / `--audio-clip` accidentally included in a metadata-only edit | human_intervention | Surface to the user that the track was rebuilt; this is irreversible from the client. |

## What this Skill will not do

- Approve spend.
- Persist tokens, signed URLs, cookies, or session material.
- Pass `node:` or `res:` prefix on `--clip` / `--audio-clip`.
- Silently merge old and new clip lists; track replacement is destructive
  and the user must consent.
- Guess missing options locally; let the server fill them from the source.

## Policy

Invocation requires:
- Confirmed installation of dreamina-canvas
- Explicit user consent for any track replacement
- For paid execution: explicit handoff to dreamina-canvas-quote-and-run

Forbids:
- Calling --run from this Skill
- Passing node: or res: prefix on --clip or --audio-clip
- Silently merging old and new clip lists
- Persisting tokens, signed URLs, cookies, or session material

Default prompt:

> Passing --clip or --audio-clip to node edit timeline rebuilds the
> corresponding track and issues new clip identities. Confirm with the
> user before destructive edits; for title-only changes omit both flags.
> Hand off paid execution.
>

<!-- QUALITY_BASELINE_V1 -->
## When to use（什么时候使用）

当用户需要 **为当前请求选择并执行可验证、可恢复的专业工作流** 时加载本技能。先从请求中提取目标、输入、约束、交付格式和验收标准；描述摘要为：Use when an agent or script must build or edit a Dreamina Canvas timeline (visual clips and audio clips). Warns before track replacement because the server drops uncommitted changes and regenerates clip identities.。

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

确认目标、输入、约束、可用工具、成功标准和失败边界；任一关键条件未知时停止在只读阶段。
### Step 3：形成计划

列出将调用的工具、会改变的对象、成功标准以及失败后的安全退出方式。
### Step 4：执行动作

按最小充分步骤执行，并在关键状态变化处记录证据；每个外部调用均保留可关联的状态或回执。
### Step 5：验证交付

输出结果、验证证据、未完成项、风险和明确的下一步，并把事实、推断和未验证项分开陈述。

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

不超出用户给定范围；写入、付费、发布和不可逆动作需要明确授权。 如果请求需要别的技能，不复制其正文；按技能名称进行交接，并保留当前任务上下文。

## Progressive disclosure

- 需要确定输入/输出、状态和授权点时，读取 `references/workflow-contract.md`。
- 需要交付前自检时，读取 `references/validation-checklist.md`。
- 遇到超时、部分成功或恢复场景时，读取 `references/error-recovery.md`。
- 首次运行、拒绝越权和失败恢复分别参考 `examples/happy-path.md`、`examples/boundary-refusal.md`、`examples/failure-recovery.md`。
