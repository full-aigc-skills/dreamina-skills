# 实时模型与音色发现

先读 `schema` 和对应 `--help`；以下 `model list` / `model find` 形式已由本机公开版 1.0.0 的 help 确认。旧指南可能出现 `model search`，仅当当前制品声明它时才使用。

```bash
dreamina-canvas model list --type image
dreamina-canvas model list --type video
dreamina-canvas model list --type audio
dreamina-canvas model find "模型名称" --type image
dreamina-canvas voice list --offset 0 --count 50
```

将结果中的 `model` 值传给 `--model`，不能把搜索别名当模型标识。比例、分辨率、时长、数量和权益也从该模型的当前结果读取；TTS 的 `voiceName` 来自 `voice list`。
