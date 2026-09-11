# 文生视频模型选择（CLI v1.4.18）

| 模型 token | 分辨率 | 时长 | 场景 |
|---|---|---|---|
| `seedance2.0fast` | 720p | 4–15 秒 | 默认快速迭代 |
| `seedance2.0` | 720p | 4–15 秒 | 标准高质量 |
| `seedance2.0mini` | 720p | 4–15 秒 | 轻量方案 |
| `seedance2.0fast_vip` | 720p | 4–15 秒 | VIP 快速通道 |
| `seedance2.0_vip` | 720p、1080p、4k | 4–15 秒 | 高分辨率最终输出 |
| `seedance2.5` | 480p、720p、1080p | 4–30 秒 | 长视频 / 延时摄影 / 镜头叙述 |

文生视频不接受旧 3.x 或 Seedance 1.x token。每次都显式传
`--video_resolution`，并使用小写 `p`。`seedance2.5` 不能用 1080p/4k；如需
高分辨率请仍走 `seedance2.0_vip`。
