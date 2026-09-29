# Workflow Patterns — Canvas Text-to-Image

> Canvas 文生图的标准工作流模式与错误处理方案。
> 付费步骤一律发生在 `dreamina-canvas-cli`；本文件只串任务级流程。

---

## 工作流 1：标准单次生成（最常用）

**场景**: 用户有一个写好的提示词，要直接生成图片

```bash
# 1. 三检（version / schema / auth account）
# 2. 发现
dreamina-canvas --format json model list --type image

# 3. 免费草稿
dreamina-canvas --format json node create image \
  --title "<title>" --prompt "<prompt>" \
  --mode t2i --model <model> --ratio <ratio> --resolution <resolution> --count 1
# → 持久化 nodeId

# 4. 交接 dreamina-canvas-cli：
#    node quote → 展示报价 → node confirm（精确 --credit-ceiling）→ node run
# 5. 交接 dreamina-canvas-cli：operation wait <submitId>
# 6. 交接 dreamina-canvas-cli：resource get / download + SHA-256
```

**适用**: 绝大多数单张生成。

---

## 工作流 2：异步批量生成（多张草稿，统一批准）

**场景**: 用户要一组图（如 4 张候选），不想逐张等待

```bash
# 1. 逐张存草稿（全部免费）
for spec in "a:16:9" "b:1:1" "c:16:9" "d:9:16"; do ... node create image ...; done
# → 持久化每个 nodeId

# 2. 交接 dreamina-canvas-cli 批量报价：
#    逐节点 node quote，汇总展示总报价
# 3. 用户给一个精确总上限 → node confirm / node run
#    每个 node 一个稳定 --submit-id（长度与顺序一致）
# 4. 逐 submitId operation wait；失败节点单独报，不连坐重提
```

**适用**: 3+ 张图、A/B 候选、多比例同题。

**注意**: 批量不等于免确认；一次批准只覆盖展示过的报价。

---

## 工作流 3：画布项目管理（替代旧 session）

**场景**: 一个项目内连续多次生成，需要可追溯、可回画布查看

```bash
# 1. 建画布并设为当前
dreamina-canvas --format json canvas create "<项目名>" --use
# → 持久化 projectId 与 webUrl

# 2. 之后所有 node 命令自动落在该画布；跨进程/跨设备续作时
#    显式传 --project-id <projectId>

# 3. 查看近期画布（只读，不切换当前画布）
dreamina-canvas --format json canvas ls --limit 20
```

**适用**: 系列创作、品牌项目、需要打开 webUrl 人工挑选的场景。
旧 CLI 的 `--session=<id>` 无 Canvas 对应；组织单位是画布 + `--profile`。

---

## 工作流 4：先查后改（与提示词技能协作）

**场景**: 提示词技能产出 prompt，用户批准后执行

```text
1. dreamina-prompt-text2image 定稿 prompt → 用户批准
2. 本技能执行：
   a. model list --type image 发现
   b. 把 prompt 建议的比例/分辨率映射到 discovery 白名单内的值
   c. node create image --mode t2i …（免费草稿）
   d. 交接 quote-and-run 报价 → 批准 → 运行
   e. 交接 download-assets 校验落盘
3. 报告 nodeId / 报价 / submitId / resourceId + 哈希
```

**适用**: 标准协作流程；prompt 未定稿时绝不进入第 2 步。

---

## 工作流 5：挑图迭代（count > 1 或编辑重跑）

**场景**: 首轮结果不满意，基于同一节点迭代

```bash
# 1. 首轮 count=4，挑中 1 张（记其 resourceId）
# 2. 基于原节点做全量替换编辑（生成编辑必须给完整块）
dreamina-canvas --format json node edit image \
  --node-id <nodeId> \
  --prompt "<refined prompt>" --mode t2i \
  --model <model> --ratio <ratio> --resolution <resolution> --count 4
# 3. 重新 node quote → 用户重新批准 → node run（新一轮计费）
```

**红线**: 迭代是**新一轮生成**，会再次计费；必须重新报价、重新批准。

---

## 错误处理剧本

### 场景：exit 2（命令或参数不正确）
对照 `schema` 修正 argv；不要原样重试。常见根因：
model/ratio/resolution 不在白名单、漏传 `--resolution`、t2i 带了 `--ref`。

### 场景：exit 10（等待积分确认）
报价已生成、草稿已保存、**未提交**。把报价展示给用户，取得精确
`--credit-ceiling` 批准后，复用返回的 node / task ID 继续；不要新建节点。

### 场景：exit 11（需要登录）
`dreamina-canvas-cli-auth` 重认证（`auth login` / `auth wait`），用同一身份
重试原命令。

### 场景：exit 20（本地等待超时）
服务端任务仍在跑。保存 projectId + submitId，稍后
`operation wait <submitId> --project-id <projectId>` 续等；禁止重提。

### 场景：exit 21（可重试服务故障）
指数退避后重试**同一 submitId**；仍失败则升级处理。

### 场景：exit 22 / requiredAction=human_intervention
连同 nodeId / submitId / 退出码交接用户，附官方要求的排查四件套：
完整命令、完整报错、`dreamina-canvas version` 输出、meta.requestId。

---

## 报价与额度管理

- `node quote` 是查询，**不等于批准**；批准是用户对着精确上限点头。
- 报价超过 `--credit-ceiling` 时 CLI 运行前停止——这是保护，不是故障。
- 每次对话的首次付费前展示报价；同一批准额度内可连续执行，超额度
  必须重新批准。

## 登录与配置故障排查

```bash
# 服务端账号自检（唯一可信）
dreamina-canvas --format json auth account
# 本地态检查（仅排障）
dreamina-canvas --format json auth status
# 凭据续期（仅在 refresh window 内）
dreamina-canvas --format json auth refresh
# 重登录
dreamina-canvas --format json auth login --force
```

本地状态文件（用户配置目录下，勿手改）：
`dreamina-canvas/contexts/<profile-and-environment>.json`（当前画布）、
`dreamina-canvas/operations/<profile-and-environment>/<submitId>.json`
（任务恢复信息）。macOS 通常在 `~/Library/Application Support/`。

## 最佳实践

1. **先草稿后付费**——任何生成先 `node create` 落草稿，确认参数再进付费链。
2. **discovery 每次必跑**——模型/比例/分辨率白名单会变；旧值直接复用是高发故障源。
3. **持久化四类 ID**——projectId / nodeId / submitId / resourceId，缺一无法恢复。
4. **submitId 永不重铸**——续等、重试、跨进程恢复都用同一 ID；新 ID = 新计费。
5. **报错先看 requiredAction**——脚本只按退出码 + requiredAction 分流，不解析文案。
6. **交付必带哈希**——`resource download` 后 SHA-256 校验才算完成。
7. **反馈问题带四件套**——完整命令、完整报错、`dreamina-canvas version`、requestId。
