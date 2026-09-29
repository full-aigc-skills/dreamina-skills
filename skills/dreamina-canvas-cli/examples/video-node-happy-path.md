# 三种视频模式

示意命令中的 `<...>` 是占位符，须用当前 CLI 返回的值替换后执行；不要原样复制。

参数从当前视频模型结果读取。保存草稿时不带 `--run --wait`；已有草稿应通过 `dreamina-canvas-cli` 运行，不再创建节点。下列是交互终端新任务示例：CLI 在 `--run` 阶段展示实时报价并等待用户确认；执行前生成并保存稳定 `submitId`。Agent 非交互运行应走显式报价、确认、提交链。

```bash
dreamina-canvas node create video --run --wait --submit-id <稳定UUID> --title "海边日落" --mode t2v --prompt "海面日落，镜头缓慢推进" --model "<model值>" --ratio "<支持比例>" --resolution "<支持分辨率>" --duration <支持秒数>

dreamina-canvas node create video --run --wait --submit-id <稳定UUID> --title "商品短片" --mode m2v --prompt "镜头缓慢推近，主体保持稳定" --model "<model值>" --ratio "<支持比例>" --resolution "<支持分辨率>" --duration <支持秒数> --ref "node:<图片或视频节点ID>"

dreamina-canvas node create video --run --wait --submit-id <稳定UUID> --title "首尾帧过渡" --mode first_last_frame --prompt "从第一张图平滑过渡到第二张图" --model "<model值>" --ratio "<与首帧一致且模型支持的比例>" --resolution "<支持分辨率>" --duration <支持秒数> --ref "node:<首帧节点ID>" --ref "node:<尾帧节点ID>"
```

当前 CLI 使用 `t2v`、`m2v`、`first_last_frame`，没有 `i2v` 模式。两个帧引用保持首、尾顺序。
