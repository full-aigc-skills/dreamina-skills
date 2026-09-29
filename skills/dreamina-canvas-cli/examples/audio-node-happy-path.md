# 配音与音乐

示意命令中的 `<...>` 是占位符，须用当前 CLI 返回的值替换后执行；不要原样复制。

先发现音色或音频模型。下列是交互终端新任务示例：CLI 在 `--run` 阶段展示实时报价并等待用户确认；先保存 `submitId`。只需草稿时去掉 `--run --wait`，已有草稿通过 `dreamina-canvas-cli` 继续，Agent 非交互运行也走该显式事务。

```bash
dreamina-canvas voice list --offset 0 --count 50
dreamina-canvas node create audio --run --wait --submit-id <稳定UUID> --title "旁白" --mode tts --prompt "欢迎使用即梦画布" --voice-name "<voiceName>"

dreamina-canvas model list --type audio
dreamina-canvas node create audio --run --wait --submit-id <稳定UUID> --title "背景音乐" --mode music --prompt "轻快、有科技感的电子音乐" --model "<支持music的model>" --duration <支持秒数>
```

TTS 传 `--voice-name` 而不传 `--model`；音乐相反。
