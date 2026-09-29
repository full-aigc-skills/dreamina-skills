# 草稿报价、确认与运行

示意命令中的 `<...>` 是占位符，须用当前 CLI 返回的值替换后执行；不要原样复制。

先保存草稿、记录 `projectId` 和 `nodeId`，再查询最新报价。向用户展示报价及上限；仅在用户明确批准后执行确认。以下是当前 CLI 的显式事务，`submitId` 在首次运行前生成并持久化；重复调用沿用同一 ID。

```bash
dreamina-canvas --format json node quote --node-id <nodeId> --project-id <projectId>
dreamina-canvas --format json node confirm --node-id <nodeId> --project-id <projectId> --credit-ceiling <已批准上限>
# 从确认结果的 data.creditConfirmationToken 取得短期 token；仅保留在进程内
dreamina-canvas --format json node run --node-id <nodeId> --project-id <projectId> --submit-id <稳定UUID> --credit-token "<本次确认返回的token>"
```

报价不等于批准。退出码 10 是等待确认，节点已保存但尚未提交；复用返回的节点及任务身份继续。若结果不明，先按 `submitId` 查询，不能换 ID 再提交。
