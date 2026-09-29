# 文生图与图生图

示意命令中的 `<...>` 是占位符，须用当前 CLI 返回的值替换后执行；不要原样复制。

`--model`、`--ratio`、`--resolution` 必须来自当前 `model list` 和 schema。下面前两条只保存草稿；已有草稿在用户确认报价后使用 `dreamina-canvas-cli` 的 `node run`，不要再次 `node create`。

```bash
dreamina-canvas node create image --title "雪地狐狸" --mode t2i --prompt "一只在雪地里的狐狸，电影感光线" --model "<model值>" --ratio "<支持比例>" --resolution "<支持分辨率>" --count 1

dreamina-canvas node create image --title "商品海报" --mode i2i --prompt "保持商品外观不变，改成户外广告风格" --model "<model值>" --ratio "<支持比例>" --resolution "<支持分辨率>" --ref "node:<图片节点ID>" --count 1

# 另一种路径：交互终端新建任务；CLI 在 --run 阶段展示实时报价并等待用户确认
dreamina-canvas node create image --run --wait --submit-id <预先保存的稳定UUID> --title "雪地狐狸" --mode t2i --prompt "一只在雪地里的狐狸，电影感光线" --model "<model值>" --ratio "<支持比例>" --resolution "<支持分辨率>" --count 1
```

若要导入已上传图片而非生成，使用 `dreamina-canvas-cli` 的资源挂载示例。

查询、仅改标题和超清是三个不同动作。仅改标题不重新生成；超清需单独报价与授权，`--detail` 只适用于当前模型支持的 `pro` 模式。

```bash
dreamina-canvas node find --type image --status success --limit 50
dreamina-canvas node show --node-id <nodeId>
dreamina-canvas node edit image --node-id <nodeId> --title "新的标题"
dreamina-canvas node upscale image --node-id <nodeId> --mode <支持模式> --resolution <支持分辨率> --wait
```
