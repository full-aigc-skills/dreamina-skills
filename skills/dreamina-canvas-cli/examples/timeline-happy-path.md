# 创建时间轴

示意命令中的 `<...>` 是占位符，须用当前 CLI 返回的值替换后执行；不要原样复制。

先从 CLI 结果取到已完成的视频与音频节点标识，再按当前 `node create timeline --help` 构造片段。下面是指南中的参数形状；具体 clip 语法以本机 schema 为准。

```bash
dreamina-canvas node create timeline --title "成片时间轴" --clip "<当前schema要求的视频片段表达式>" --audio-clip "<当前schema要求的音频片段表达式>"
```

编辑现有时间轴前先展示将被替换的轨道；服务端可能重建片段标识，保存原节点与资源回执供核对。
