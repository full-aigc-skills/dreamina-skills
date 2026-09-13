---
name: dreamina-cli-image2video
description: Use when the user provides image, video, or audio references and wants Dreamina 即梦 video generation through `image2video`, `frames2video`, `multiframe2video`, or `multimodal2video`. Covers CLI v1.4.18 runtime ratio discovery, required video resolution, Seedance model constraints, input limits, and async terminal statuses.
license: Complete terms in LICENSE.txt
---

# 即梦 CLI 图生视频

先按输入意图选命令，再运行对应的 `dreamina <command> -h`：

## When to use and boundary

用于至少有一张参考图或一个参考视频的 CLI 视频任务。不该用于纯文本视频、图片生成或纯提示词润色；这些场景改用对应的 `dreamina-cli-*` 或 `dreamina-prompt-*` 技能。

协作路由：`dreamina-prompt-image2video` 负责单图、首尾帧、多帧和多模态提示词；
本 Skill 负责本地 `dreamina` CLI 执行；用户明确选择 OpenCLI 传输时改用
`dreamina-opencli-image2video`，不要同时提交两条执行链。

| 场景 | 命令 | 关键输入 |
|---|---|---|
| 单图动画 | `image2video` | `--image`、必填 `--prompt` |
| 首尾帧过渡 | `frames2video` | `--first`、`--last` |
| 2–20 张故事板 | `multiframe2video` | `--images` |
| 图/视频/音频全能参考 | `multimodal2video` | 至少一张图、一个视频或一个音频 |

## v1.4.18 硬约束

- 所有四种模式都必须显式传 `--video_resolution`。
- 分辨率 token 使用小写 `480p`/`720p`/`1080p`/`4k`；`480p` 仅 `seedance2.5` 支持。
- `multiframe2video` 固定模型，不接受 `seedance2.5`，只接受 720p/1080p。
- `seedance2.5` 支持 480p/720p/1080p，不支持 4k；其他模型组合以运行时 help 为准。
- `image2video` 支持 `seedance1.0fast`、`seedance1.5pro`、Seedance 2.0 家族与 `seedance2.5`。
- `frames2video` 支持 `seedance1.5pro`、Seedance 2.0 家族与 `seedance2.5`。
- `multimodal2video` 支持 Seedance 2.0 家族与 `seedance2.5`；`seedance2.5` 允许**纯音频**输入。
- `seedance2.5` 时长 4–30 秒，参考音视频总时长 2–30 秒。
- 比例必须在运行时通过 `dreamina <command> --help` 发现：`image2video`、`frames2video`、
  `multimodal2video` 暴露 `--ratio`，`multiframe2video` 不暴露并跟随首图。
- `image2video` 与 `frames2video` 使用 `seedance2.5` 时禁止显式传 `--ratio`，比例跟随首帧；
  `multimodal2video` 可显式传比例，省略时默认 16:9。

完整矩阵见 [`dreamina-cli` skill 的 v1.4.18 契约](https://github.com/full-aigc-skills/dreamina-skills/blob/main/skills/dreamina-cli/references/dreamina-cli-v1.4.18-contract.md)（如未安装：`npx skills add full-aigc-skills/dreamina-skills --skill dreamina-cli`）。

## 最小正确示例

```bash
dreamina image2video --image=./photo.png --prompt="镜头缓慢推近" --video_resolution=720p --poll=0
dreamina frames2video --first=./start.png --last=./end.png --prompt="季节自然变化" --video_resolution=720p --poll=0
dreamina multiframe2video --images=./a.png,./b.png --prompt="人物转身走向远处" --video_resolution=720p --poll=0
dreamina multimodal2video --image=./subject.png --audio=./music.mp3 --prompt="按音乐节奏运镜" --video_resolution=720p --poll=0
```

3 张以上多帧故事，每 N 张图提供 N−1 个 transition；单段时长 1–8 秒：

```bash
dreamina multiframe2video \
  --images=./a.png,./b.png,./c.png \
  --transition-prompt="从 A 走向 B" \
  --transition-prompt="从 B 走向 C" \
  --transition-duration=3 \
  --transition-duration=3 \
  --video_resolution=1080p \
  --poll=0
```

## 异步闭环

### Step 1：路由与验证

根据输入意图选择四个命令之一，验证文件可读，再用对应 `--help` 在运行时校验模型、时长、比例和分辨率。

### Step 2：提交

检查积分、说明消费影响、异步提交并保存 `submit_id`。

### Step 3：终态闭环

对 `querying` 持续调用 `query_result`，直到 `success` 或 `fail`。失败时报告
`fail_reason`。遇到 `AigcComplianceConfirmationRequired` 时提示用户先在 Web 端完成授权。

## Gotchas

1. **模式误路由**：单图、首尾帧、故事板、全能参考的参数名不同。
2. **分辨率遗漏**：四个命令都必须传 `video_resolution`；`seedance2.5` 支持 480p/720p/1080p。
3. **多帧越权**：multiframe 不接受 model_version，也不能用 4k，也不可用 `seedance2.5`。
4. **transition 数量**：N 张图需要 N−1 条 transition。
5. **比例误传**：`seedance2.5` 的 image/frames 模式禁止显式比例；multiframe 根本没有 `--ratio`。
6. **音频单独提交**：`multimodal2video` 的 `seedance2.5` 允许纯音频输入（参考音视频总时长 2–30 秒）。
7. **时长越界**：`seedance2.5` 4–30 秒；Seedance 2.0 家族 4–15 秒；超出会被拒。

## References

- [`dreamina-cli` skill 的 v1.4.18 参数契约](https://github.com/full-aigc-skills/dreamina-skills/blob/main/skills/dreamina-cli/references/dreamina-cli-v1.4.18-contract.md)（如未安装：`npx skills add full-aigc-skills/dreamina-skills --skill dreamina-cli`）
- [模式选择](references/mode-guide.md)
- [参数参考](references/parameter-reference.md)
- [VIP 指南](references/official-doc-vip-guide.md)
- [工作流模式](references/workflow-patterns.md)
- [示例](examples/single-image.md)
