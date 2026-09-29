# CLI 就绪与命令契约

先只读核对安装制品。自动化时把 `--format json` 放在子命令前；本文其余示例为便于人工阅读使用简写。

```bash
dreamina-canvas --help
dreamina-canvas version
dreamina-canvas schema
dreamina-canvas node create image --help
```

`--help` 应列出 auth、canvas、model、node、operation、resource。若报错，保存完整命令、错误、`version` 输出和 `meta.requestId`；生成任务还需 `projectId` 与 `submitId`。日志或反馈不得包含凭据。缺少命令时转交 `dreamina-canvas-cli-setup`。
