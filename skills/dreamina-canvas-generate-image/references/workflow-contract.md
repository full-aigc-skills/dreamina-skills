# dreamina-canvas-generate-image 工作流契约

## 前置条件

- 已明确目标对象、输入来源、输出格式与验收标准。
- 已确认执行环境、工具能力、身份范围与版本。
- 涉及写入、付费、发布或不可逆动作时，已获得与本步骤绑定的显式授权。

## 状态模型

`DISCOVERED → PREFLIGHTED → PLANNED → EXECUTING → VERIFYING → COMPLETED`

任何阶段都可以进入 `BLOCKED`；只有保留原范围、原幂等键且确认不会重复副作用时，才可进入 `RECOVERING`。

## 执行契约

- 预检：校验输入、模型/工具能力、输出路径、预算上限和审批状态。
- 执行：按一次批准执行并记录请求标识；模糊结果先查询而不是重提。
- 证据：验证产物存在性、格式、哈希/标识、成本状态和质量门禁。

## 输出字段

至少提供：`status`、`scope`、`actions`、`evidence`、`artifacts`、`skipped`、`risks`、`next_action`。未知值使用 `NOT_VERIFIED`，不得猜测。
