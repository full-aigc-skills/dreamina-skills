# Failure Recovery — 上传失败与模型找不到

场景：`model find "某模型"` 返回空。

```bash
# 错误：按记忆臆造一个 model 值进后续命令
# 正确：翻全量列表人工筛，或换关键字再 find
dreamina-canvas --format json model list --type image
# 从负载里挑规格匹配的 model 值
```

场景：`resource upload` 退出码 21（可重试服务故障）。

```bash
# 上传幂等但重复上传产生新 resourceId；重试间隔退避
# 成功后立即持久化新 resourceId；旧 ID 若已记录且 resource get 正常则继续可用
dreamina-canvas --format json resource get <oldResourceId> --project-id <projectId>
```

场景：`canvas create` 退出码 2。

```bash
# 对照 schema 修正 flag（常见：名称含特殊字符、漏 --use）
dreamina-canvas --format json schema
```
