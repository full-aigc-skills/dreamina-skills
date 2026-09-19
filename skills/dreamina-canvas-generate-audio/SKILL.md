---
name: dreamina-canvas-generate-audio
description: Use when an agent or script must save or run a Dreamina Canvas audio node in either TTS or music mode. Forbids --count, requires --voice-name for TTS, and refuses an implicit default model for music.
license: Complete terms in LICENSE
---

# Dreamina Canvas Audio Node

This Skill owns the **Canvas audio node**. The two modes (`tts`, `music`)
have opposite field requirements, and a missing or wrongly-applied field
is rejected with `cli.audio_music_model_required` (exit code 2) for music
or with the mode-specific contract for TTS.

Reference detail is in
[references/audio-node-contract.md](references/audio-node-contract.md).

## When to use

- The caller wants to synthesize speech from text (TTS).
- The caller wants to generate a music clip from a prompt (music).
- The caller wants to switch an existing audio node from one mode to
  the other and needs the field set explained.

## When **not** to use

- For approving or running generation — that is `dreamina-canvas-quote-and-run`.
- For the visual track of an audio-bearing composition — that is
  `dreamina-canvas-manage-timeline`.

## TTS

```bash
dreamina-canvas --format json node create audio \
  --prompt "<text to speak>" \
  --mode tts \
  --voice-name "<discovered-voice>"
```

- `--voice-name` is mandatory. The CLI resolves the public name into the
  authoritative server-side identifier.
- `--model` is **forbidden** for TTS; the model is selected from the
  voice's underlying TTS model, not user-supplied.

## Music

```bash
dreamina-canvas --format json node create audio \
  --prompt "<music prompt>" \
  --mode music \
  --model "<music-model-from-discovery>" \
  --duration 30
```

- `--model` is mandatory. Take it from the live full audio discovery shape
  selected by schema (`model search --detail full` or `model list`), filtered
  to a `music` mode entry.
- `--voice-name` is **forbidden** for music.
- `--duration` must be `> 0` seconds; default 30.
- The CLI refuses to default the music model. A missing `--model`
  returns `cli.audio_music_model_required` (exit code 2). Do not retry
  with a name remembered from a different environment.

## Field exclusivity

| Mode | Required | Forbidden |
|------|----------|-----------|
| `tts` | `--voice-name` | `--model` |
| `music` | `--model`, `--duration > 0` | `--voice-name` |

`--count` is **not** accepted on audio nodes — a single output only.

## Generation is a full replace

Same as image / video: touching generation flags means submitting the
complete new block. Metadata is sparse. `--clear-generation` is the
opt-out and is mutually exclusive with generation flags.

```bash
# Sparse metadata edit; generation remains unchanged
dreamina-canvas --format json node edit audio \
  --node-id <nodeId> --title "<new title>"
```

## Paid execution is not this Skill's job

Hand off to `dreamina-canvas-quote-and-run`. This Skill never calls
`--run`, never sets `--credit-ceiling` or `--credit-token`, never
persists tokens.

## Failure → recovery

| Failure | requiredAction | What to do next |
|---------|----------------|-----------------|
| `cli.audio_music_model_required` (exit 2) | none | Re-run the schema-selected full audio discovery command, pick a `music` model, retry. |
| `--voice-name` rejected on TTS | none | Re-run `voice list`; add `--language` only if schema declares it. |
| `--model` passed on TTS (exit 2) | none | Remove `--model`; let the voice drive the model. |
| `--voice-name` passed on music (exit 2) | none | Remove `--voice-name`; supply `--model` instead. |
| `--count` passed on audio (exit 2) | none | Remove `--count`; audio is single-output. |
| Missing `--duration` on music (exit 2) | none | Pass `--duration` from the discovery bound. |

## What this Skill will not do

- Approve spend.
- Persist tokens, signed URLs, cookies, or session material.
- Accept `--count` on audio nodes.
- Use a remembered voice or music-model name across environments.
- Implicit-default the music model.

## Policy

Invocation requires:
- Confirmed installation of dreamina-canvas
- Live voice list (for TTS) or live audio model discovery (for music)
- For paid execution: explicit handoff to dreamina-canvas-quote-and-run

Forbids:
- Calling --run from this Skill
- Passing --count on audio nodes
- Supplying --model on TTS or --voice-name on music
- Implicit-defaulting the music model
- Persisting tokens, signed URLs, cookies, or session material

Default prompt:

> TTS requires --voice-name; music requires --model + --duration. Never
> pass --count on audio nodes. Never default the music model. Hand off
> paid execution to dreamina-canvas-quote-and-run.
>

<!-- QUALITY_BASELINE_V1 -->
## When to use（什么时候使用）

当用户需要 **在明确输入、预算和交付约束后执行生成或写入操作** 时加载本技能。先从请求中提取目标、输入、约束、交付格式和验收标准；描述摘要为：Use when an agent or script must save or run a Dreamina Canvas audio node in either TTS or music mode. Forbids --count, requires --voice-name for TTS, and refuses an implicit default model for music.。

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
