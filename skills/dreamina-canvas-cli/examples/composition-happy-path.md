# 保存文本、主体与画布关系

示意命令中的 `<...>` 是占位符，须用当前 CLI 返回的值替换后执行；不要原样复制。

以下命令只保存节点，不执行付费生成。实际参数先查当前 `schema`；素材引用优先 `node:<nodeId>`，再按依赖顺序建立下游节点。

```bash
dreamina-canvas node create text --title "分镜说明" --text "镜头一：海面日落"
dreamina-canvas node create element --title "主角" --description "稳定的角色外观" --main "<图片节点ID>"
```

保存返回的 `nodeId` 和 `mutationVersion`。本机公开版 1.0.0 的主体槽位使用裸节点 ID；`node:` 前缀会被拒绝。若其他版本的 schema 不同，以当前 schema 为准。
