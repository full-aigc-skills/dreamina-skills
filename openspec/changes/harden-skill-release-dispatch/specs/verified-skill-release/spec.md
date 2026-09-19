## Purpose

确保每个技能包在正式发布前达到可验证质量，并让消费插件只基于不可变 release 身份执行升级。

## ADDED Requirements

### Requirement: Skill changes pass deterministic quality gates
技能内容变更 MUST 通过结构校验、断链检查和确定性 TRACE 评估；发布门禁 MUST 在任一技能低于规定阈值时失败。

#### Scenario: Package is ready for release
- **WHEN** 包内所有技能及其引用资源完成评估
- **THEN** 结构检查无错误且每个技能的 TRACE 总分不低于 4.5

#### Scenario: A skill has a broken reference
- **WHEN** `SKILL.md` 或随附文档引用不存在的包内资源或违规的跨技能相对路径
- **THEN** 发布检查失败并报告来源文件和目标

### Requirement: Published versions are immutable
技能包 MUST 使用新的语义版本 tag 发布，MUST NOT 移动或覆盖已发布 tag。

#### Scenario: Content changes after a release
- **WHEN** 已发布技能内容需要修正
- **THEN** 仓库创建新版本 tag 和 GitHub Release，而不是改写旧 tag

### Requirement: Consumers receive exact release identity
正式 release 发布后，producer MUST 将包名、tag 和 tag 的 peeled commit SHA 发送给每个实际消费插件；凭据缺失或请求失败 MUST 使工作流失败。

#### Scenario: Release notification succeeds
- **WHEN** GitHub Release 进入 published 状态且 tag 指向提交
- **THEN** 每个消费插件收到包含匹配 tag 与 commit 的 `repository_dispatch`

#### Scenario: Dispatch credential is unavailable
- **WHEN** `SKILLS_SYNC_TOKEN` 对技能仓不可见
- **THEN** producer 工作流明确失败且不伪造成功状态

### Requirement: Granular installation is self-contained
每个可单独安装的技能 MUST 将必需引用资源包含在自己的目录中，或使用明确的技能名与安装命令完成跨技能交接。

#### Scenario: User installs one skill
- **WHEN** 用户使用 `npx skills add ... --skill <name>` 仅安装该技能
- **THEN** 技能引用的本地文档、示例和脚本均可解析
