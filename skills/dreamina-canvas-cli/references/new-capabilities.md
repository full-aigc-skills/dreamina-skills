# 新版 Canvas CLI 能力与版本边界

依据：用户提供的首次使用指南（更新记录至 2026-11-05 v1.3.0）；本机升级后只读 `dreamina-canvas version` 和 `schema` 实测为 **1.3.0 / c6a5530a**。1.2.0 的回退副本用于对比命令增量。运行时仍以用户本机的 schema 为准。

## 每次执行前

先运行 `dreamina-canvas version`、`dreamina-canvas schema`，再对目标命令运行 `--help`。版本更新或切换 profile、个人/团队空间后，重新查询模型、音色、权益与当前画布。若本机 schema 没有用户所需命令，报告版本和缺失能力；升级 CLI 属独立操作，须按当前任务授权执行。

## 团队空间与画布

1. `team ls` 发现有权访问的团队；`space current` 查看当前个人或团队空间。
2. 仅在用户选定目标空间后执行 `space use`；团队空间所需 team ID 取自实时返回值。
3. 切换后重新执行 `auth account`、`canvas ls` 与必要的模型查询。画布、账户积分及生成权限以当前空间为准，不沿用切换前的 projectId 或报价。

这些命令从 1.2.0 起就在本机 schema 中存在。`canvas ls` 只查询，不会切换当前画布；需要指定画布时按 [画布身份](canvas.md) 使用明确的 projectId。

## 节点、样片和后处理

1.2.0 与 1.3.0 schema 均声明 `node delete`、`node delete confirm`、`node delete status`，以及节点创建/编辑的 `--x`、`--y` 位置参数。删除会改变画布；先确认目标节点与影响，再按实时 schema 中的确认/状态流程执行。

样片转正使用 `node promote video-sample`，图片抠图使用 `node cutout image`，视频超清使用 `node upscale video`，视频补帧使用 `node interpolate video`。这些操作在 1.2.0/1.3.0 schema 中有 `--dry-run`、`--submit-id` 和积分确认参数。先以当前命令契约检查源节点、可用模式和报价；向用户展示**该操作**的实时报价及上限，获得批准后用稳定 submitId 提交。结果不明时查询原 submitId，不能换 ID 重做。图片放大继续由 `dreamina-canvas-cli-image2image` 的独立报价流程负责。

样片生成参数必须从当前模型规格读取；不要把普通视频草稿或已受理的样片当作已转正成片。导演台命令族为 `director`，帮助列有 `catalog`、`create`、`show`、`apply`、`pull`、`push`、`preview`、`freeze`、`export`、`resume-export`。1.3.0 还支持通过导演台场景命令 `object.merge` 合并静态零件、`object.pivot` 设置自定义锚点；先用当前导演台 schema 核对正文版本和对象条件，合并后再制作动画，不把旧场景盲目升级。预览、同步与导出是不同结果，交付时分别核验。

## 1.3.0 工作流批量生成与模板复用

1.3.0 新增 `workflow` 命令族；已核实的报价、批准、运行、模板实例化及恢复步骤见 [工作流与模板](workflow-and-templates.md)。**1.2.0** 的 schema 没有该命令族；用户本机未声明时，说明版本差异并停在预检阶段，不得猜测参数或把旧版多个 `node run` 称作工作流模板。

批量执行时逐项保存返回身份、报价与结果；任何未知状态先按原身份查询。节点保存、样片、导演台预览和最终下载分别报告，不互相替代。
