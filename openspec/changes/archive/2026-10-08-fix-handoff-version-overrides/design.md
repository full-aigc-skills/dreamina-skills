## Context

见 proposal.md；在当前 Brownfield 代码和规格上增量修复。

## Goals / Non-Goals

目标是恢复既有安全与兼容性承诺；不实现多轮执行、不安装工具、不运行付费 Canary。

## Decisions

将公开参数传递到结构校验；使用 None 区分默认值和显式空范围，复用现有 compatible_producer，不更改版本比较算法或默认范围。

## Risks / Trade-offs

- 本地 mock 回归不证明真实服务或 Windows 当前版本通过；历史证据注明日期。
- 首次提交前进程退出可能导致标记已尝试但未发送，仍只对账，优先防止重复计费。

## Migration Plan

先红灯回归、实现、完整相关检查；本地准备补丁版本。发布与远端操作单独遵循授权。
