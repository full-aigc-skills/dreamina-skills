## Why

可安装的 Dreamina 3D 技能仍把早期 Codex 专用插件名当成公共身份，导致 Codex、ZCode、Kimi 三种宿主看到不一致的路由和回执契约。

## What Changes

- 将 Dreamina 3D、Blender 和 Maya 的公共身份改为宿主无关名称。
- 让 companion 探针识别 Codex、ZCode 与 Kimi manifest。
- 更新当前插件仓链接、发布版本与回归测试。

## Capabilities

### New Capabilities

None.

### Modified Capabilities

- `host-neutral-skill-identity`: 可安装技能必须使用宿主无关身份，并能在三种宿主 manifest 下发现 companion。

## Impact

影响 Dreamina 3D 技能正文、探针、回执校验、README、测试和技能包 patch 版本；不修改历史规格证据。
