# 实时模型与音色发现

先读 `schema` 和对应 `--help`；以下 `model list` / `model find` 形式已由本机公开版 1.0.3 的 help 确认。旧指南可能出现 `model search`，仅当当前制品声明它时才使用。

```bash
dreamina-canvas model list --type image
dreamina-canvas model list --type video
dreamina-canvas model list --type audio
dreamina-canvas model find "模型名称" --type image
dreamina-canvas voice list --offset 0 --count 50
dreamina-canvas voice list --model "<canonical-model>" --offset 0 --count 50
```

将结果中的 `model` 值传给 `--model`，不能把搜索别名当模型标识。比例、分辨率、时长、数量和权益也从该模型的当前结果读取；TTS 的 `voiceName` 来自 `voice list`（可先用 `--model` 收敛到单个模型的音色目录，翻页保持同一模型）。音频模型目录会随版本扩充（如公开版 1.0.3 引入 Seed Audio 1.0），一律以实时查询结果为准，不在文档或会话里固化模型名。
