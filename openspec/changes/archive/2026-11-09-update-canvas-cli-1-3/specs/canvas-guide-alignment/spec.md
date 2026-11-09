## ADDED Requirements

### Requirement: New Canvas capabilities route to their owning skill

当用户请求团队空间、样片、导演台、后处理或工作流批量生成时，Canvas 编排技能 MUST 指向对应操作参考。工作流 MUST 使用当前 CLI 声明的报价、批准、运行、恢复和模板实例化契约。执行前 MUST 根据当前 CLI `version`、`schema` 和命令 `--help` 核实能力与参数；未声明的能力 MUST 明确停止而不能猜测命令。

#### Scenario: Installed CLI is older than the requested capability

- **WHEN** 用户请求 1.3.0 的工作流模板复用，而本机 CLI 仅显示 1.2.0 且 schema 没有该命令
- **THEN** 技能报告版本与缺失能力，不拼造命令或将普通批量 `node run` 冒充工作流模板。

#### Scenario: A post-processing operation may consume credits

- **WHEN** 用户要求样片转正、超清、抠图或补帧
- **THEN** 技能先核对当前命令契约与实时报价，获得该操作的授权后才提交，并复用原 submitId 查询结果。
