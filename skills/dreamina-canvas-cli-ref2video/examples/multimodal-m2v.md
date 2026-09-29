# Multimodal References — 多模态参考（m2v）

用户：「拿这张人物照和这个场景视频合成一段人物走进场景的视频。」

```bash
# 1. 三检 + discovery —— 必读素材约束：类型/数量上限以 discovery 为准
dreamina-canvas --format json model list --type video

# 2. 每份素材各自上传
dreamina-canvas --format json resource upload --file "$PWD/person.png" --name "person"  # → res:P
dreamina-canvas --format json resource upload --file "$PWD/scene.mp4"  --name "scene"    # → res:C

# 3. m2v 多引用草稿（按意图顺序传）
dreamina-canvas --format json node create video \
  --title "人物入景" \
  --prompt "人物自然地走进场景，镜头跟随，光影融合" \
  --mode m2v --model <model> \
  --ref res:<P> --ref res:<C> \
  --duration 5
# 若 exit 2：重读 discovery 的素材类型/数量约束并调整引用，不重复原命令

# 4. 交接 quote-and-run → resume-operation → download-assets
```

要点：旧 CLI 的 `multimodal2video` 子命令在 Canvas 不存在，多模态参考
统一归 `m2v`；素材上限是服务端属性，每次以 discovery 为准。
