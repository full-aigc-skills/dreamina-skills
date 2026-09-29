# Canvas CLI 原子技能迁移

本次保留九个 CLI 入口，移除重复可安装辅助技能。编排、评估与旧 CLI 兼容技能保留。未发布，消费插件固定路径需要更新。

| 原入口 | 新责任技能 | 操作文档 |
|---|---|---|
| `dreamina-canvas-auth` | `dreamina-canvas-cli-auth` | `references/auth-state.md` |
| `dreamina-canvas-discover-models` | `dreamina-canvas-cli` | `references/discovery.md` |
| `dreamina-canvas-create` | `dreamina-canvas-cli` | `references/canvas.md` |
| `dreamina-canvas-download-assets` | `dreamina-canvas-cli` | `references/resources.md` |
| `dreamina-canvas-quote-and-run` | `dreamina-canvas-cli` | `references/execution.md` |
| `dreamina-canvas-resume-operation` | `dreamina-canvas-cli` | `references/recovery.md` |
| `dreamina-canvas-compose` | `dreamina-canvas-cli` | `references/composition.md` |
| `dreamina-canvas-manage-timeline` | `dreamina-canvas-cli` | `references/timeline.md` |
| `dreamina-canvas-ready` | `dreamina-canvas-cli` | `references/preparation.md` |
| `dreamina-canvas-generate-image` | `dreamina-canvas-cli` | `references/image-node.md` |
| `dreamina-canvas-generate-video` | `dreamina-canvas-cli` | `references/video-node.md` |
| `dreamina-canvas-generate-audio` | `dreamina-canvas-cli` | `references/audio-node.md` |
| `dreamina-setup` | `dreamina-canvas-cli-setup` | `references/first-use.md` |

## 迁移规则

- 新生成请求进入九个 CLI 入口，旧 CLI 仅在用户明确要求时使用。
- 原独有参考和场景保留于目标技能，不再调用已移除的技能名。
- 生成模式规则归对应任务技能；公共命令参数、身份、执行和恢复由总技能维护。
- 消费插件在采用本地变更前需更新 vendor 清单、固定路径、技能数量及命令路由。
- 历史生成证据在 verification/dreamina-canvas-historical-evidence.json；不能代替本次真实运行验收。

## 本地验证

77 项测试通过；33 个技能结构、资源和套件检查通过；CI 固定 TRACE 评估器门槛通过。具体分数和边界见 verification/dreamina-canvas-atomic-verification.json。本次没有登录、上传、创建远端草稿、付费生成、提交或推送。
