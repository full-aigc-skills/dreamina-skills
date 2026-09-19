## Context

当前 DCC 插件已经发布为 `blender-design` 与 `maya-design`，但 Dreamina 3D 技能仍校验 `codex-blender` 与 `codex-maya`，实际回执会被拒绝。探针还只读取 `.codex-plugin/plugin.json`。

## Decisions

- 公共插件身份固定为 `dreamina-3d`、`blender-design`、`maya-design`。
- 保留 `.codex-plugin` 作为 Codex 宿主 manifest 路径，但同时读取 `.zcode-plugin/plugin.json` 与 `kimi.plugin.json`。
- 只修改当前可安装内容；历史设计文档保留旧名称作为迁移证据。
- 使用 patch 版本发布，不移动已有 tag。

## Risks

- 旧 companion 安装目录不会继续匹配；这是有意的契约迁移，当前已发布插件均使用新身份。
- 三种 manifest 的字段可能不同；探针仅依赖共同字段 `name`、`version`、`receipt_contract_versions`。
