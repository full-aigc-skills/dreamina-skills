# 设计

- `dreamina-novel-use` 是短剧任务入口，识别已有输入与阶段并按技能名称交接。
- `dreamina-novel-cli` 维护 CLI 版本、画布身份、报价、异步恢复公共契约；六个任务技能只写自己的阶段。
- 各技能自含 references/examples/agents 元数据，支持按单项安装；不引用兄弟目录。
- 以本机 `jimeng-novel` 1.0.1 帮助、schema 和官方安装包内 `jimeng-drama` Skill 为事实来源；实际模型和价格运行时查询。
- 不运行付费生成作为静态发布门禁；测试验证结构、身份、引用、命令映射与 TRACE 质量。
