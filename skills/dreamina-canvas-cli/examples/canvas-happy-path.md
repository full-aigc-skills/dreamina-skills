# 创建与查找画布

示意命令中的 `<...>` 是占位符，须用当前 CLI 返回的值替换后执行；不要原样复制。

```bash
dreamina-canvas canvas create "我的第一块画布" --use
dreamina-canvas canvas ls --limit 20
```

保存返回的 `projectId` 和 `webUrl`。`canvas ls` 不改变当前画布；跨终端操作显式传 `--project-id <projectId>`，重试创建复用同一个预先保存的项目 ID。创建是服务端写入，应在用户要求创建画布后执行。
