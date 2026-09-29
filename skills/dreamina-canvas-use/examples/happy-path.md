# 新用户最小画布流程

示意命令中的 `<...>` 是占位符，须用当前 CLI 返回的值替换后执行；不要原样复制。

先按需交给 `dreamina-canvas-cli-setup` 完成安装、版本/schema 和账户验证。下列命令展示阶段，不构成对运行或积分的预授权。

```bash
dreamina-canvas model list --type image
dreamina-canvas canvas create "我的第一块画布" --use
dreamina-canvas node create image --title "雪地狐狸" --mode t2i --prompt "一只在雪地里的狐狸" --model "<model值>" --ratio "<支持比例>" --resolution "<支持分辨率>"
dreamina-canvas node quote --node-id <nodeId> --project-id <projectId>
# 展示报价、取得用户明确批准后，交给 quote-and-run 复用同一 nodeId / submitId
# 经批准的交互模式也可使用 node create image --run --wait
# 完成后：
dreamina-canvas operation wait <submitId> --project-id <projectId>
dreamina-canvas resource get <resourceId> --project-id <projectId>
dreamina-canvas resource download <resourceId> --project-id <projectId> --output ./downloads
```

报告分别列出草稿、报价、批准、提交、终态和文件校验。保存草稿并不表示已生成；下载文件还需按回执核验大小及 SHA-256。
