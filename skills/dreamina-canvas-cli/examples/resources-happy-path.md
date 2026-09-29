# 上传、查验与下载素材

示意命令中的 `<...>` 是占位符，须用当前 CLI 返回的值替换后执行；不要原样复制。

上传是外部写入，只在用户要求使用本地素材且路径获准后执行。先保存稳定 `resourceId`；画布上已有来源节点时，后续优先用 `node:<nodeId>` 保留关系，冻结素材才用 `res:<resourceId>`。

```bash
dreamina-canvas resource upload --file ./product.png --name "商品图"
dreamina-canvas resource get <resourceId> --project-id <projectId>
dreamina-canvas node create image --title "商品图" --resource-id <resourceId> --import-kind local_upload --project-id <projectId>
mkdir -p ./downloads
dreamina-canvas resource download <resourceId> --project-id <projectId> --output ./downloads
```

`node create image --resource-id` 是挂载已登记资源，不是文生图生成。下载后核验 CLI 回执中的字节数和 SHA-256，再报告完成。
