## Why

dreamina-canvas 公开版 CLI 已从 1.0.1 升级到 1.0.3（commit `244064d`，构建
`2026-10-14T03:28:54Z`）。官方更新记录为：支持 Seed Audio 1.0，全能配音支持
选择音色或参考素材；支持删除节点和调整节点位置。技能包当前记录的契约停留在
1.0.0/1.0.1 探针，存在以下与实时 schema 冲突的内容：

- `references/discovery.md` 声称 `voice list` 只有 `--offset/--count`；1.0.3
  新增 `--model`（按 canonical model 过滤并保持同模型翻页）。
- `references/audio-node*.md`、`text2voice` 技能声称"TTS 禁止 `--model`、
  `--voice-name` 恒必填"；1.0.3 的 `--scenario`（`text-reading` / `omni-dubbing`）
  允许 tts 携带 `--model`，全能配音下 `--voice-name` 变为可选（服务端转成音频
  参考），并接受 `--ref` 参考素材。
- `references/composition.md`、`video-node.md`、`image-node-*-contract.md` 与
  `verification/dreamina-canvas-guide-contract.json` 把 `uri:` / `vid:` 标为
  "reserved, rejected"；1.0.3 schema 的 `--ref` 约束已接受
  `node|res|uri|vid` 四种类型化引用。
- 节点删除（`node delete` + `node delete confirm` + `node delete status`）与
  节点位置（`--x/--y` 成组、组内父相对坐标）完全没有文档与命令覆盖记录。

## What Changes

- 新增 `references/node-deletion.md`：批量删除的确认令牌流（update-id 复用、
  delete-token 短期凭证、`--yes` 不可替代、status 只读回查、不支持群组）。
- 在公共契约与组合文档中登记 1.0.3 新的跨切面 flag：`--x/--y`、`--tag`/
  `--clear-tags`、`--dry-run`、`--resource-source`，以及 `node find --name/--tag`。
- 按 1.0.3 schema 重写音频节点契约：tts 的 legacy / text-reading / omni-dubbing
  三形态及字段互斥表；`voice list --model` 发现路径。
- 将 `uri:` / `vid:` 引用从"保留且拒收"改为"实时 schema 声明即接受"。
- 刷新验证基线：`dreamina-canvas-guide-contract.json`（版本块 1.0.3、
  referenceSyntax、ttsScenarios）与 `dreamina-canvas-command-coverage.json`
  （补 `node delete` 三个命令的 owner 与证据）。
- 同步 `tests/test_official_command_coverage.py` 的命令集合。

## Capabilities

### New Capabilities

无（全部落在既有能力内的增量修订）。

### Modified Capabilities

- `canvas-cli-atoms`: 新增节点删除与位置操作的文档化要求；修订音频场景与
  引用语法契约。

## Impact

- 受影响技能：`dreamina-canvas-cli`（references、examples、SKILL.md 索引）、
  `dreamina-canvas-cli-text2voice`（SKILL.md、parameter-reference、model-guide、
  examples）。
- 验证与测试：两个 verification fixture、覆盖测试集合；不改变技能数量（仍为
  33 个目录、九个 CLI 入口），不改变退出码与命令族集合。
- 兼容性：文档继续声明"schema 是运行时事实源"；Seed Audio 1.0 属于模型目录
  事实，按既有策略不在技能正文中固化模型名。
