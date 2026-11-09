## Evidence and version boundary

用户提供的指南列出 1.0.3 至 1.3.0 增量。原本机 1.2.0 核实团队空间、样片转正、导演台和后处理命令；用户授权升级后 1.3.0/c6a5530a schema 核实新增 `workflow` 命令族及参数。对旧版仍使用版本检测和能力缺失时停止的方式表达。

## Skill ownership

- `dreamina-canvas-cli` 维护空间、画布公共操作、导演台、节点删除、后处理和工作流发现。
- `dreamina-canvas-cli-image2image` 指向图片抠图；`dreamina-canvas-cli-ref2video` 指向样片转正、视频超清与补帧。
- `dreamina-canvas-use` 与 `dreamina-design-use` 负责用户意图路由。
- 保留现有报价、批准、submitId 恢复和产物校验规则；所有新付费操作单独确认实时报价。
