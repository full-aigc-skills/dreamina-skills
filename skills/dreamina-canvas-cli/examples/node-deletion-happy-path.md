# 删除画布节点（确认令牌流）

示意命令中的 `<...>` 是占位符，须用当前 CLI 返回的值替换后执行；不要原样复制。

删除是确认门控的破坏性写操作：先摘要批次，再由 `node delete confirm` 签发短期令牌，最后带令牌执行；`--yes` 不能替代令牌。完整契约见 [节点删除与位置](../references/node-deletion.md)。当前公开版 1.0.3 起提供该命令族；执行前以当前 `schema` 为准。

```bash
# 1. 摘要待删除批次（可重复 --node-id；不支持群组）；记录返回的 updateId
dreamina-canvas --format json node delete \
  --node-id "<nodeId1>" --node-id "<nodeId2>" \
  --project-id "<projectId>"

# 2. 用户确认后签发删除令牌；--update-id 必须与摘要一致，令牌只留在内存
dreamina-canvas --format json node delete confirm \
  --node-id "<nodeId1>" --node-id "<nodeId2>" \
  --update-id "<updateId>" \
  --project-id "<projectId>"

# 3. 带令牌执行删除；重试沿用同一 updateId 与新签发的令牌
dreamina-canvas --format json node delete \
  --node-id "<nodeId1>" --node-id "<nodeId2>" \
  --update-id "<updateId>" \
  --delete-token "<deleteConfirmationToken>" \
  --project-id "<projectId>"

# 结果不明时先只读回查，不要重复提交
dreamina-canvas --format json node delete status \
  --node-id "<nodeId1>" --node-id "<nodeId2>" \
  --update-id "<updateId>" \
  --project-id "<projectId>"
```

删除节点不会取消或退款已在跑的生成任务；在途任务继续用原 `submitId` 查询。
