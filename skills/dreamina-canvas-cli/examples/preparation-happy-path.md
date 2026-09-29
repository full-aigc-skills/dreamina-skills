# 新画布与参考素材准备

用户：建立新品视觉画布并上传三张参考图。本示例只保存画布与素材，不提交生成。
前置：账户可用、三张文件可读；把 `<...>` 替换为实际值，首次写入前持久化 projectId 和每个 resourceId。

```bash
dreamina-canvas --format json model list --type image
dreamina-canvas --format json model find "<模型名称关键字>" --type image
dreamina-canvas --format json canvas create "新品视觉" --project-id <projectId> --use
dreamina-canvas --format json canvas ls --limit 20
dreamina-canvas --format json resource upload --project-id <projectId> --resource-id <resourceId1> --file "<ref1绝对路径>" --name ref1
dreamina-canvas --format json resource upload --project-id <projectId> --resource-id <resourceId2> --file "<ref2绝对路径>" --name ref2
dreamina-canvas --format json resource upload --project-id <projectId> --resource-id <resourceId3> --file "<ref3绝对路径>" --name ref3
dreamina-canvas --format json resource get <resourceId1> --project-id <projectId>
dreamina-canvas --format json node create image --project-id <projectId> --resource-id <resourceId1> --import-kind local_upload --title ref1
```

对其余素材执行同样的资源状态检查与节点导入；每步读取真实返回值后再继续，不能构造虚假的 res:A 身份。导入节点后记录返回的 nodeId，后续使用 node:<nodeId>；需冻结资产时使用 res:<resourceId>。

输出：画布 projectId/webUrl、三个 resourceId、已导入 nodeId、当前模型规格。
验收：资源查询成功、节点内容可读取、没有运行付费生成。上传不确定时先 resource get 查询原 resourceId；建画布重试复用 projectId，不能换新 ID。
