# 图生视频 VIP 契约（CLI v1.4.18）

- `image2video`、`frames2video`、`multimodal2video` 只有
  `seedance2.0_vip` 可选 1080p 或 4k。
- `seedance2.0fast_vip` 仍只支持 720p。
- `seedance2.5` 支持 480p / 720p / 1080p，不支持 4k。
- `multiframe2video` 不接受 model_version（含 `seedance2.5`），可选 720p/1080p。
- token 使用小写 `480p`、`720p`、`1080p`、`4k`。

```bash
dreamina frames2video --first=./start.png --last=./end.png --prompt="自然过渡" --model_version=seedance2.0_vip --video_resolution=1080p --poll=0
dreamina image2video --image=./input.png --prompt="镜头慢推" --model_version=seedance2.5 --video_resolution=720p --duration=15 --poll=0
```
