## Context

参见 `proposal.md`。技能仓是插件中受管技能的事实源，消费侧已经能够校验 release tag、peeled SHA 和摘要，因此 producer 必须提供同等强度的发布身份。

## Goals / Non-Goals

**Goals:**

- 在技能源阻止低质量、断链或不可独立安装的内容进入 release。
- 以 release 事件驱动消费插件升级，并携带可二次验证的 tag 与 commit。

**Non-Goals:**

- 不在技能源保存插件 harness。
- 不绕过 GitHub secret 可见性或使用本地高权限 OAuth token。
- 不修改既有 tag。

## Decisions

1. TRACE 使用仓库内固定版本的确定性评分器并设 4.5 门槛，保证本地与 CI 可复现。
2. dispatch 仅监听 `release.published`，从 Git tag 解引用得到 commit 后发送；相比 `push main`，它不会向插件暴露未发布状态。
3. 每个消费插件单独发送事件并校验 HTTP 响应，避免部分失败被掩盖。
4. 上游内容错误在技能源修复并发布新版本，插件只通过 vendor 更新接收，不保留受管目录的私有补丁。

## Risks / Trade-offs

- [多个插件消费同一包] → 工作流维护显式 consumer 矩阵，每个目标独立记录结果。
- [secret 未向新仓库开放] → 保持工作流失败，提示管理员扩展 `SKILLS_SYNC_TOKEN` 可见性后重跑。
- [TRACE 规则演进] → 固定评分器 commit，并通过独立升级变更调整门槛或规则。

## Migration Plan

1. 初始化 OpenSpec 并建立发布契约。
2. 修复技能自包含问题，补 TRACE 和引用检查。
3. 提交、推送并等待 CI。
4. 创建新 tag 与 Release；确认 producer dispatch 成功。
5. 消费插件校验 payload 后更新锁并发布新插件版本。
