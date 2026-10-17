## 1. 契约采集与差异确认

- [x] 1.1 只读采集 1.0.3 `version` / `schema`，登记版本块与差异清单
- [x] 1.2 对照技能语料定位全部过时声明（1.0.0/1.0.1、voice --language、
      uri/vid 拒收、TTS 禁 model 等）

## 2. 技能内容同步

- [x] 2.1 新建 `node-deletion.md` 并在 `dreamina-canvas-cli` SKILL.md 登记
- [x] 2.2 `command-contract.md` 登记 `--x/--y`、`--tag`、`--dry-run`、
      `--resource-source` 与删除短期凭证
- [x] 2.3 `discovery.md` / `discovery-capability-discovery.md` 更新
      `voice list --model` 与版本声明
- [x] 2.4 `audio-node.md` / `audio-node-audio-node-contract.md` 重写 tts
      场景契约（legacy / text-reading / omni-dubbing）
- [x] 2.5 `composition.md` / `video-node.md` / `image-node-*-contract.md`
      修正 `uri:` / `vid:` 与 `node find --name/--tag`
- [x] 2.6 `error-routing.md` / `cli-contract.md` / 示例同步
- [x] 2.7 `text2voice` SKILL.md、parameter-reference、model-guide、示例
      按全能配音契约更新

## 3. 基线与测试

- [x] 3.1 刷新 `dreamina-canvas-guide-contract.json`（版本、referenceSyntax、
      ttsScenarios、source 溯源）
- [x] 3.2 `dreamina-canvas-command-coverage.json` 增补 `node delete` 三命令
      并同步 `tests/test_official_command_coverage.py`
- [x] 3.3 全量 unittest 与 lint 通过；复核改动与 schema 一致
