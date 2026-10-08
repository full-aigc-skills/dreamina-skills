## Why

validate_artifact 的公开 version_ranges 参数被忽略，调用方无法约束生产者版本。

## What Changes

- 修复已确认缺陷并增加可观察行为回归。
- 保持现有单轮、人工审批和默认兼容性边界。

## Capabilities

### New Capabilities

无。

### Modified Capabilities

- `host-neutral-skill-identity`: 完善既有契约与失败路径。

## Impact

控制器/适配器/文档与本地测试；不新增外部调用授权，不启用多轮自动化。
