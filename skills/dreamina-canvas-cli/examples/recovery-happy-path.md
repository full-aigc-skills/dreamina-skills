# 同一任务的状态与恢复

示意命令中的 `<...>` 是占位符，须用当前 CLI 返回的值替换后执行；不要原样复制。

任务受理、等待超时或退出码 20 均不代表生成失败。保留 `projectId` 和原 `submitId`，执行只读查询或继续等待，不发起新的 `node run`。

```bash
dreamina-canvas operation status <submitId> --project-id <projectId>
dreamina-canvas operation wait <submitId> --project-id <projectId> --timeout 10m --interval 5s
dreamina-canvas node show --node-id <nodeId> --project-id <projectId>
```

终态成功后仍需取得 `resourceId`，再交给 `dreamina-canvas-cli` 检查和下载。失败时按结构化 `requiredAction` 处理，不靠本地化错误文案猜测。
