# Design — sync canvas skills to CLI 1.0.3

## 事实源与采集方式

以本机安装的公开版 1.0.3 二进制只读输出为唯一事实源（未登录状态下
`version` / `schema` 均可执行；不采集需要登录的模型目录）：

- `dreamina-canvas --format json version`
  → `1.0.3 / 244064d / 2026-10-14T03:28:54Z / releaseDate 2026-10-09`。
- `dreamina-canvas --format json schema`
  → 命令族、flag 约束、`declaredExitCodes`、`successData`。

模型目录（含 Seed Audio 1.0）是服务端事实，登录后经
`model list --type audio` 实时发现；技能正文按既有策略只使用占位符，不固化
模型名。

## schema 差异 → 文档映射

| 1.0.3 schema 事实 | 落点 |
|---|---|
| `node delete`：`--node-id` 1..100 去重、不支持 group；`--update-id` 确认/重试复用；`--delete-token` 由 `node delete confirm` 签发，`--yes` 不可替代；`declaredExitCodes` 含 10/20 | 新建 `references/node-deletion.md`；`command-contract.md` 短期凭证条款；`error-routing.md` 读命令清单补 `node delete status` |
| `node delete confirm` → `deleteConfirmationToken` + `expiresAtMs`；`node delete status` 只读回查 `idempotentReplay` | `node-deletion.md` 全流；覆盖表新条目 |
| `--x/--y` 成组、组内父相对坐标（全部 create/edit 类型） | `command-contract.md` 构造条款；`composition.md` 提示 |
| `--tag default-tag-1..5` / `--clear-tags`；`--dry-run` 本地校验；`--resource-source <res>@<project>` | `command-contract.md` 一段式登记，不逐类型展开 |
| `node find --name/--tag` | `composition.md` 查找节 |
| `voice list --model`（可选 canonical model，翻页保持同模型） | `discovery.md`、`discovery-capability-discovery.md`、`text2voice` 的 parameter-reference 与 model-guide |
| `audio --scenario text-reading|omni-dubbing`（requires tts + explicit model）；`--voice-name` 全能配音可选、服务端转音频参考；`--ref` 仅全能配音 | `audio-node.md`、`audio-node-audio-node-contract.md`、`text2voice` SKILL/参考/示例 |
| `--ref` 约束 `node|res|uri|vid`（uri/vid 不再是保留拒收） | `composition.md`、`video-node.md`、`image-node-*-contract.md`、guide-contract fixture `referenceSyntax` |
| 顶层退出码集合与命令族不变 | fixture 断言不动，仅刷新版本块与 source 溯源 |

## 关键取舍

1. **不复制整个 schema 进 Markdown。** 仓库原则是"schema 为运行时事实源，
   Markdown 只补充跨领域协议边界"。新增文档聚焦删除确认流与字段互斥语义
   这类 schema 单字段说不清的协议。
2. **两套 confirm 的区分必须显式。** 顶层 `node confirm`（积分批准）与
   `node delete confirm`（删除凭证）同名不同义，删除文档中用对照表防止误用。
3. **退出码 10 的语义扩展。** 既有文档把 exit 10 描述为"积分确认"；1.0.3 中
   `node delete` 也声明 10/20。按"draft/删除批次已保存、等待确认"的共性修订
   表述，不发明新码。
4. **基线刷新保持测试断言兼容。** `source` 字段追加刷新记录但保留原始指南
   日期（`2026-09-11`，`test_canvas_skill_inventory` 断言）；命令族与退出码
   集合不变；`audioModes` 仍为 `["tts","music"]`（mode 枚举未变），新增
   `ttsScenarios` 键承载场景枚举，测试未对键集合做封闭断言。
5. **覆盖表以 dreamina-canvas-cli 为 owner。** 删除是跨模式公共操作，证据
   token（`node delete` 等）落在公共技能语料内，满足
   `test_official_command_coverage` 的 owner 存在性与证据包含断言。

## 验证策略

- `uv run python -m unittest discover -s tests`：全量测试（含覆盖表一致性、
  库存、套件校验、指南对齐）。
- `uv run python scripts/lint_skills.py`：技能结构 lint。
- 人工复核：每个改动文件中的命令形态与 1.0.3 schema 原文逐条对照。
