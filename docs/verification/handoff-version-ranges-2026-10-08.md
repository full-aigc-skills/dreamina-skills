# 本地修复验证 — 2026-10-08

OpenSpec：`fix-handoff-version-overrides`。版本：1.7.1 本地候选。
运行环境：macOS，`/opt/anaconda3/bin/python3` 3.13.5；全部测试离线，无新外部生成调用。

## 修复内容

- 把 version_ranges 从 validate_artifact 传到结构校验与兼容性判断，错误信息也显示调用方范围。
- None 保留默认范围，显式映射整体替换默认范围；{} 拒绝所有生产者。
- 原有文件路径、字节数、摘要、元数据校验不变；不改版本比较算法。
- 所属技能补充参数说明，包 manifest 准备 1.7.1 候选。

## 验证结果

- 本地契约测试：78 项通过。
- 新增公开 validate_artifact 入口回归先确认 version_ranges 被忽略导致失败，修复后通过。
- 真实临时文件测试覆盖：显式 1.x 范围接受、默认拒绝 1.x、默认 0.x 兼容、显式范围拒绝默认版本、空映射拒绝所有生产者、文件改变仍拒绝。
- 33 个技能 lint、单独安装资源/链接、Canvas 套件校验：零错误。
- TRACE：33 个技能，平均 4.652，最低 4.55，门槛 4.50；使用本地与固定提交 91cd3e8e2aafd73d73fc037ce75dee7b6b663ffb 字节一致的 evaluator。
- OpenSpec 增量严格校验通过；3 项主规格严格校验通过。

## 兼容性与未验证边界

- 未运行 DCC、真实服务、付费或 CI 验证；这些不是本次参数传递修复的本地证据。
- 未提交、推送、打 tag 或发布。既有 harden-skill-release-dispatch 变更及其待发布任务保持原样。
- 插件锁定的 Canvas 技能未受本次 3D validator 修改影响，无需重新 vendor。

## 源码关联

验证输入共 13 个文件，按仓库相对路径排序，以 `path + NUL + bytes + NUL` 拼接后 SHA-256：

`94e9b44b399db8531e3ce413c940a0e5c60f90a774940a37ad77146e8c081cf3`

范围：本次 handoff validator、所属 SKILL.md、tests/*.py 与 .claude-plugin/plugin.json。
此指纹绑定当前本地实现，不代表远端提交或发布制品。
