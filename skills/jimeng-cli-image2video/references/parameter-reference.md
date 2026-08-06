# 图生视频参数参考（CLI v1.4.15）

| 命令 | 必填输入 | 模型 | 分辨率 |
|---|---|---|---|
| `image2video` | image、prompt | 1.0fast、1.5pro、2.0 家族、seedance2.5 | 必填；VIP 可 1080p/4k；seedance2.5 仅 480p/720p |
| `frames2video` | first、last | 1.5pro、2.0 家族、seedance2.5 | 必填；VIP 可 1080p/4k；seedance2.5 仅 480p/720p |
| `multiframe2video` | images（2–20） | 固定 | 必填；720p/1080p（不支持 seedance2.5） |
| `multimodal2video` | 至少 image/video/audio 之一 | 2.0 家族、seedance2.5 | 必填；VIP 可 1080p/4k；seedance2.5 仅 480p/720p |

非 VIP 模型仅支持 720p；`seedance2.5` 仅 480p/720p，不支持 VIP 高分辨率。
v1.4.15 起 `multimodal2video` 允许纯音频输入（仅 `seedance2.5`，参考时长 2–30 秒）。
模型 token、时长与输入上限见
[`dreamina-cli` skill 的统一 v1.4.15 契约](https://github.com/full-aigc-skills/jimeng-skills/blob/main/skills/dreamina-cli/references/dreamina-cli-v1.4.15-contract.md)(如未安装:`npx skills add full-aigc-skills/jimeng-skills --skill dreamina-cli`)。

```bash
dreamina image2video --image=./input.png --prompt="镜头推进" --video_resolution=720p --poll=0
dreamina image2video --image=./input.png --prompt="镜头慢推" --model_version=seedance2.5 --video_resolution=720p --duration=12 --poll=0
```