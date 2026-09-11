# 图生视频参数参考（CLI v1.4.18）

| 命令 | 必填输入 | 比例 | 分辨率 |
|---|---|---|---|
| `image2video` | image、prompt | 可传 `--ratio`；Seedance 2.5 禁止显式传，跟随首帧 | 必填；Seedance 2.5 支持 480p/720p/1080p |
| `frames2video` | first、last | 可传 `--ratio`；Seedance 2.5 禁止显式传，跟随首帧 | 必填；Seedance 2.5 支持 480p/720p/1080p |
| `multiframe2video` | images（2–20） | 无 `--ratio`，跟随首图 | 必填；720p/1080p（不支持 Seedance 2.5） |
| `multimodal2video` | 至少 image/video/audio 之一 | 可传 `--ratio`；省略时 16:9 | 必填；Seedance 2.5 支持 480p/720p/1080p |

不要跨命令推断比例或模型能力；每次都运行 `dreamina <command> --help` 做运行时发现。
`multimodal2video` 允许纯音频输入（仅 `seedance2.5`，参考时长 2–30 秒）。
模型 token、时长与输入上限见
[`dreamina-cli` skill 的统一 v1.4.18 契约](https://github.com/full-aigc-skills/dreamina-skills/blob/main/skills/dreamina-cli/references/dreamina-cli-v1.4.18-contract.md)（如未安装：`npx skills add full-aigc-skills/dreamina-skills --skill dreamina-cli`）。

```bash
dreamina image2video --image=./input.png --prompt="镜头推进" --video_resolution=720p --poll=0
dreamina image2video --image=./input.png --prompt="镜头慢推" --model_version=seedance2.5 --video_resolution=1080p --duration=12 --poll=0
```
