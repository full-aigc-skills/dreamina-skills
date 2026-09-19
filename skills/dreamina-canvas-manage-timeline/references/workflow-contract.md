# dreamina-canvas-manage-timeline 工作流契约

## 前置条件

- 已明确目标对象、输入来源、输出格式与验收标准。
- 已确认执行环境、工具能力、身份范围与版本。
- 涉及写入、付费、发布或不可逆动作时，已获得与本步骤绑定的显式授权。

## 状态模型

`DISCOVERED → PREFLIGHTED → PLANNED → EXECUTING → VERIFYING → COMPLETED`

任何阶段都可以进入 `BLOCKED`；只有保留原范围、原幂等键且确认不会重复副作用时，才可进入 `RECOVERING`。

## 执行契约

- 预检：确认目标、输入、约束、可用工具、成功标准和失败边界。
- 执行：按最小充分步骤执行，并在关键状态变化处记录证据。
- 证据：输出结果、验证证据、未完成项、风险和明确的下一步。

## 输出字段

至少提供：`status`、`scope`、`actions`、`evidence`、`artifacts`、`skipped`、`risks`、`next_action`。未知值使用 `NOT_VERIFIED`，不得猜测。
