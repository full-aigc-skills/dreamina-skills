---
name: dreamina-canvas-discover-models
description: Use when an agent must look up the live set of available generation models, voices, ratios, resolutions, durations, batch limits, and per-model requirements for the dreamina-canvas CLI. Never accepts hard-coded model or voice names from outside the current discovery payload.
license: Complete terms in LICENSE
---

# Dreamina Canvas Discovery

This Skill teaches every other `dreamina-canvas-*` Skill how to ask the CLI
what is currently supported. It exists so that no caller hard-codes model
names, voice names, ratios, resolutions, durations, or batch limits.

Reference detail is in
[references/capability-discovery.md](references/capability-discovery.md).

## When to use

- Before the first generation in any workflow that takes a `--model`,
  `--voice-name`, `--ratio`, `--resolution`, `--duration`, or `--count`.
- Before any audio music generation (must confirm the active environment's
  audio model and that the caller has not cached a name from a different
  environment).
- When a generation fails with "model not found" or a `--voice-name`
  rejection: re-discover rather than retrying with a remembered value.

## When **not** to use

- As a substitute for `dreamina-canvas-cli` argv construction rules.
- To bypass a `--credit-ceiling` decision; discovery tells you the legal
  parameter values, it never approves spend.

## Select commands from the live schema

Run `version` and `schema` before building discovery argv. If `schema`
declares `model search`, use `model search --detail full`. If it declares
`model list` instead, use `model list`; that compatibility shape already
returns per-mode flags, enums, bounds, and reference requirements.

Never send an optional flag merely because a guide mentions it. Pass
`voice list --language <code>` only when the live schema declares it; public
1.0.0 accepts only `--offset` and `--count` for `voice list`.

## Discovery commands

```bash
# Summary catalog (one row per model)
dreamina-canvas --format json model search --type image

# Compatibility shape (only when the live schema declares model list)
dreamina-canvas --format json model list --type image

# Full spec per model (every legal flag, enum, bound, batch limit)
dreamina-canvas --format json model search --type image --detail full

# Single model full spec when you already have a name
dreamina-canvas --format json model <model-id> --type image

# TTS voice catalog (add --language only when the live schema declares it)
dreamina-canvas --format json voice list --offset 0 --count 50

# Argument spec for any subcommand (for the exact flag names)
dreamina-canvas --format json schema "node create image"
```

Use only the model command shape returned by `schema`. With `model search`,
run summary discovery and then `--detail full`; with `model list`, read its
full per-mode specifications directly. Never go from a remembered model name
to generation: the catalog moves.

## What to read from the discovery payload

The live full payload (`model search --detail full` or `model list`, as
declared by schema) is the **only** authoritative source for:

- `--model` identifiers and aliases
- `--ratio` legal values per model
- `--resolution` legal values per model (some require it explicitly)
- `--duration` (video, music)
- `--count` upper bound, taken from `generation.maxBatchGenCount`
- Required references, VIP / entitlement flags (`generation.isVip`,
  `vipConfigs[]`), per-model constraints

For audio:

- TTS `--voice-name` must come from `voice list` or from `model search
  --type audio --detail full`. The CLI resolves the public voice name into
  the server-side authoritative identifier.
- Music `--model` must come from `model search --type audio --detail full`
  filtered to `MODE=music`. Music **does not** use a server-implicit default;
  the CLI refuses `--model` missing with `cli.audio_music_model_required` and
  exit code 2.

## Hard rule: never cache across environments

The discovery payload is per environment (`distribution` × `edition` ×
profile). A model name valid in one environment is not portable to another.

- Re-run `model search --type image --detail full` whenever the active
  profile or environment changes (`dreamina-canvas version` reports
  `distribution` and `edition`; trust them).
- Re-run discovery after any CLI upgrade that bumps `commit`/`buildTime`.

## What this Skill will not do

- Recommend a specific model, ratio, resolution, or voice by name.
- Treat a remembered name as equivalent to a re-discovery.
- Save the discovery payload to a public log, fixture, or example. Use
  placeholders like `<model>` / `<voice-name>` / `<ratio>` instead.

## Policy

Invocation requires:
- Confirmed installation of dreamina-canvas
- Confirmed active profile and environment via dreamina-canvas version

Forbids:
- Hard-coding or recommending a specific model name, voice name, ratio, resolution, duration, or batch count
- Treating a discovery payload from one environment as valid in another
- Saving raw discovery payloads into public logs, fixtures, or examples

Default prompt:

> Before generation, inspect `schema`, then use its declared full model
> discovery shape (`model search --detail full` or `model list`) and `voice
> list` for TTS. Add optional flags only when the live schema declares them.
>

<!-- QUALITY_BASELINE_V1 -->
## When to use（什么时候使用）

当用户需要 **只读发现、检查或汇总当前资源状态** 时加载本技能。先从请求中提取目标、输入、约束、交付格式和验收标准；描述摘要为：Use when an agent must look up the live set of available generation models, voices, ratios, resolutions, durations, batch limits, and per-model requirements for the dreamina-canvas CLI. Never accepts hard-coded model or voice names from outside the current discovery payload.。

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

确认查询范围、身份上下文、分页上限和输出字段；任一关键条件未知时停止在只读阶段。
### Step 3：形成计划

列出将调用的工具、会改变的对象、成功标准以及失败后的安全退出方式。
### Step 4：执行动作

执行有界只读查询并保留来源标识；每个外部调用均保留可关联的状态或回执。
### Step 5：验证交付

返回资源标识、查询条件、分页状态和未验证项，并把事实、推断和未验证项分开陈述。

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

不创建、不修改、不删除资源；若后续需要写操作，先交给对应写入技能并重新确认。 如果请求需要别的技能，不复制其正文；按技能名称进行交接，并保留当前任务上下文。

## Progressive disclosure

- 需要确定输入/输出、状态和授权点时，读取 `references/workflow-contract.md`。
- 需要交付前自检时，读取 `references/validation-checklist.md`。
- 遇到超时、部分成功或恢复场景时，读取 `references/error-recovery.md`。
- 首次运行、拒绝越权和失败恢复分别参考 `examples/happy-path.md`、`examples/boundary-refusal.md`、`examples/failure-recovery.md`。
