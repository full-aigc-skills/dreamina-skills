---
name: dreamina-canvas-download-assets
description: Use when an agent or script must register a local file as a Dreamina Canvas project resource (`resource upload`, with a stable idempotent resourceId), or verify the readiness of a generated Canvas resource and download it to a user-approved path with a verifiable SHA-256 and byte count. Never persists signed URLs.
license: Complete terms in LICENSE
---

# Dreamina Canvas Asset Download

This Skill owns the final delivery step. It reads a `resourceId` from a
completed node, checks that the resource is ready, and downloads it to a
user-approved directory with a verifiable SHA-256.

Reference detail is in
[references/artifact-verification.md](references/artifact-verification.md)
and [references/resource-upload.md](references/resource-upload.md).

## When to use

- The caller has a completed node and needs the underlying file(s).
- A previous download attempt failed partway and the caller needs to
  re-verify integrity.
- A user wants to inspect media metadata (duration, dimensions, codec)
  before opening the file.

## When **not** to use

- For re-running generation. That is `dreamina-canvas-quote-and-run`.
- For attaching a registered resource to a node. This Skill registers and
  retrieves resources; binding them belongs to `dreamina-canvas-compose`
  and `dreamina-canvas-generate-image`.

## The two-step delivery

```bash
# 1. Verify the resource is ready and read its stable facts
dreamina-canvas --format json resource get <resourceId> \
  --project-id "$PROJECT_ID"
# → readiness, byte count, media metadata, source nodeId

# 2. Atomic download into the user-approved directory
dreamina-canvas --format json resource download <resourceId> \
  --project-id "$PROJECT_ID" \
  --output "$USER_APPROVED_DIR"
# → canonical local path, byte count, SHA-256, media metadata
```

The download command writes via temp file + atomic rename and returns the
**final** size + SHA-256 from the on-disk file, not from a pre-flight
estimate. Trust only the post-write response.

## Output directory rules

- The output directory must be user-approved; the Skill never invents one.
- The directory must exist and be writable before calling
  `resource download`.
- The CLI writes to a canonical filename inside `--output`; it does not
  preserve the original remote filename.
- The download is atomic: a partial file will never appear in `--output`;
  either the file is complete with a verified checksum or nothing is left
  behind.

## Registering a local asset (`resource upload`)

The `resource` family is **not** read/download only: CLI 1.0.0 ships
`resource upload`, which registers a local image / video / audio file (or a
server-reachable image URL) and returns the stable `resourceId` every
downstream reference uses.

```bash
dreamina-canvas --format json resource upload \
  --file "$LOCAL_PATH" \
  --project-id "$PROJECT_ID" \
  --resource-id "$STABLE_UUID" \
  --import-kind local_upload
```

Two rules dominate this command:

- **Persist `--resource-id` before the call and reuse it verbatim.** It is the
  only idempotency identity; a fresh UUID on retry registers a second resource.
  On an ambiguous response, query `resource get <resourceId>` instead.
- **`--import-kind` is a declaration, not a permission.** `external_generated`
  records provenance only; it bypasses no authorisation and makes nothing
  trusted.

Full flag contract, the post-upload reference forms (`res:<resourceId>` vs a
bare ID in Element slots), and the failure table are in
[references/resource-upload.md](references/resource-upload.md).

## The `uri:` and `vid:` boundary

The CLI `schema` lists `uri:value` and `vid:value` among the accepted reference
**forms** for `--ref` and inside `{{...}}` prompt placeholders. The same schema
does **not** assert that the server accepts any particular `uri:` / `vid:`
value, and this repository holds no locked evidence for a concrete accepted
value.

So treat `uri:` / `vid:` as declared-but-unevidenced: prefer `node:` (when an
upstream node exists) or `res:` (a registered resource). Do not write an
example, Skill, or receipt that promises a `uri:` / `vid:` reference will
resolve — the runtime is the authority and a Skill text must not override it.

## What this Skill will not do

- Persist signed URLs, cookies, OAuth tokens, `storageId`, or provider
  task identifiers.
- Echo or log the response body's `signedUrl` / `downloadUrl` /
  `providerTaskId` fields, even when present; the Skill forbids
  persisting or echoing signed URLs in any form.
- Download into a directory the user has not explicitly named.
- Re-derive a `resourceId` from anything other than `node show` /
  `operation status` output, or the `resourceId` echoed by a persisted
  `resource upload --resource-id`; never guess.
- Treat a successful pre-flight `resource get` as proof of completion;
  the final word is the post-download SHA-256.

## Verification gate

The Skill considers a download successful only when:

- Exit code is 0.
- The returned `byteCount` matches `wc -c <path>` on the file.
- The returned `sha256` matches `shasum -a 256 <path>`.
- `media` metadata is present and consistent with the file's actual
  codec / dimensions (spot-check with `ffprobe` if available).

Any mismatch is treated as a hard failure; the file is quarantined (or
deleted if the caller prefers) and the user is informed.

## Policy

Invocation requires:
- Confirmed installation of dreamina-canvas
- A known lowercase resourceId and projectId
- A user-approved output directory

Forbids:
- Persisting signed URLs, storageId, OAuth tokens, cookies, or provider task IDs
- Downloading into a directory the user has not explicitly named
- Treating a pre-flight resource get as proof of download success
- Quarantining or deleting files without explicit user consent

Default prompt:

> Always verify the file after download via byte count + SHA-256. Use only
> the post-write response as truth. Never persist signed URLs or storage
> IDs.
>

<!-- QUALITY_BASELINE_V1 -->
## When to use（什么时候使用）

当用户需要 **为当前请求选择并执行可验证、可恢复的专业工作流** 时加载本技能。先从请求中提取目标、输入、约束、交付格式和验收标准；描述摘要为：Use when an agent or script must verify the readiness of a generated Dreamina Canvas resource and download it to a user-approved path, producing a verifiable SHA-256 and byte count. Never persists signed URLs.。

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
