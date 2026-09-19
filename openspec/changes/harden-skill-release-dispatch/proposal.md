## Why

技能仓发布与消费插件升级之间缺少统一的不可变身份、TRACE 质量门禁和可靠通知，部分工作流仍从 `main` 发送旧仓库事件，导致插件无法安全发现新版本。

## What Changes

- 技能内容变更必须通过确定性 TRACE 与结构检查。
- 正式 release 发布后，计算 tag 的 peeled commit SHA 并通知实际消费插件。
- dispatch payload 明确携带技能包、tag 和 commit；通知失败必须显式失败。
- 修复影响独立安装的断链或缺失资源，并发布新的不可变版本。

## Capabilities

### New Capabilities

- `verified-skill-release`: 定义技能质量门禁、不可变发布和消费插件通知契约。

### Modified Capabilities

无。

## Impact

影响技能内容、TRACE 报告、CI、release dispatch workflow、版本与插件锁更新；不移动任何已发布 tag。
