## ADDED Requirements

### Requirement: 短剧任务按阶段路由
Agent MUST 根据已有创意、小说、剧本、资产、分镜或片段进入最早未完成阶段，并保持用户原文与已有画布身份。

#### Scenario: 用户已有完整分镜
- **WHEN** 用户提供带台词的分镜并要求生成短剧
- **THEN** Agent 从分镜/生成阶段推进，不要求重新生成故事大纲

### Requirement: 计费与异步恢复
技能 MUST 在服务端生成前展示报价或明确无法预估的费用，取得该批明确批准；结果不明时 MUST 查询原身份而不重复提交。

#### Scenario: 批量节点运行等待超时
- **WHEN** `node run` 返回 `running` 或提交结果不明
- **THEN** Agent 使用同一节点 key 的 `node result` 续查，且不再次 `node run`

### Requirement: 可独立安装
八个技能 MUST 各自包含入口、资源和元数据，包清单 MUST 声明全部技能；跨技能交接 MUST 使用技能名和安装命令。

#### Scenario: 只安装后期技能
- **WHEN** 只安装 `dreamina-novel-cli-post`
- **THEN** 该技能的本地 references 与 examples 可读，且无需兄弟技能目录
