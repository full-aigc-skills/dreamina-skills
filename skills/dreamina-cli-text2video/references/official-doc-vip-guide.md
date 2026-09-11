# 文生视频 VIP 契约（CLI v1.4.18）

- 只有 `seedance2.0_vip` 可选 1080p 或 4k。
- `seedance2.0fast_vip` 仍只支持 720p。
- `seedance2.5` 支持 480p / 720p / 1080p，不支持 4k。
- 4k 同时依赖 VIP 权益与后端可用性。
- 参数 token 使用 `480p`/`720p`/`1080p`/`4k`，小写 `p`。

```bash
dreamina text2video --prompt="电影感海岸航拍" --model_version=seedance2.0_vip --video_resolution=1080p --poll=0
```
