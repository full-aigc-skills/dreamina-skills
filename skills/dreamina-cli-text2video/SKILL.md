---
name: dreamina-cli-text2video
description: Use when the user wants to submit, poll, or troubleshoot Dreamina 即梦 text-to-video tasks through `dreamina text2video`. Covers CLI v1.4.18 runtime ratio discovery, required video resolution, Seedance model constraints, sessions, and async terminal statuses.
license: Complete terms in LICENSE.txt
---

# 即梦 CLI 文生视频

执行前先运行 `dreamina text2video --help`。本技能记录 v1.4.18 稳定工作流；实际 help 始终是参数事实源。

## When to use and boundary

用于无参考媒体的 CLI 文生视频提交、轮询和故障诊断。不该用于图生视频、故事板或单纯提示词创作；改用 `dreamina-cli-image2video` 或 prompt 技能。

协作路由：`dreamina-prompt-text2video` 负责视频提示词；本 Skill 负责本地
`dreamina` CLI 执行；用户明确选择 OpenCLI 传输时改用
`dreamina-opencli-text2video`，不要重复提交。

## 必须遵守

- 每次提交显式传 `--video_resolution`，token 必须是小写 `480p`/`720p`/`1080p`/`4k`。`480p` 仅 `seedance2.5` 支持。
- `seedance2.0_vip` 支持 720p/1080p/4k；其他 Seedance 2.0 家族模型仅支持 720p。
- `seedance2.5`：480p/720p/1080p，时长 4–30 秒。
- 在运行时从 `dreamina text2video --help` 发现比例取值；v1.4.18 为
  1:1、3:4、16:9、4:3、9:16、21:9，省略 `--ratio` 时默认 16:9。
- 文生视频公开模型仅为 Seedance 2.0 家族与 `seedance2.5`，不要传旧 3.x 或 Seedance 1.x token。
- Seedance 2.0 家族时长 4–15 秒，默认模型 `seedance2.0fast`；`seedance2.5` 时长 4–30 秒。
- 提交前说明会消耗积分；耗时场景优先异步提交。

## 标准执行

```bash
dreamina user_credit
dreamina text2video \
  --prompt="镜头缓慢推进，一只橘猫在窗台伸懒腰，晨光穿过窗帘" \
  --duration=5 \
  --ratio=16:9 \
  --model_version=seedance2.0fast \
  --video_resolution=720p \
  --poll=0
```

VIP 高分辨率：

```bash
dreamina text2video \
  --prompt="航拍海岸线，浪花沿岩石展开，电影感长镜头" \
  --duration=8 \
  --ratio=16:9 \
  --model_version=seedance2.0_vip \
  --video_resolution=1080p \
  --poll=0
```

v1.4.18 Seedance 2.5 长视频（4–30 秒，480p/720p/1080p）：

```bash
dreamina text2video \
  --prompt="延时摄影：城市从黎明到夜空的连续变化，云层流动，灯光渐次亮起" \
  --duration=20 \
  --ratio=16:9 \
  --model_version=seedance2.5 \
  --video_resolution=720p \
  --poll=0
```

## 异步闭环

### Step 1：验证

运行 `dreamina text2video --help`，在运行时校验模型、duration、`--ratio` 与分辨率组合。

### Step 2：提交

检查积分、说明消费影响、异步提交并保存 `submit_id`。

### Step 3：终态闭环

对 `querying` 持续调用 `query_result`，直到 `success` 或 `fail`。失败时报告
`fail_reason`。遇到 `AigcComplianceConfirmationRequired` 时提示用户先在 Web 端完成授权。

## Gotchas

1. **分辨率遗漏**：每次都必须传 `video_resolution`。
2. **token 大小写**：使用 `480p`/`720p`/`1080p`/`4k`，不是大写 P。
3. **模型越界**：文生视频不接受 Seedance 1.x 或旧 3.x。
4. **高分辨率误用**：`seedance2.5` 可用 1080p 但不可用 4k；其他模型以当前 help 为准。
5. **时长越界**：Seedance 2.0 家族 4–15 秒，`seedance2.5` 4–30 秒，超出会被拒。
6. **长任务误判**：poll 超时仍为 `querying` 时继续查询，不立即重提；长视频尤其需要更长 `--poll`。

## References

- [`dreamina-cli` skill 的 v1.4.18 参数契约](https://github.com/full-aigc-skills/dreamina-skills/blob/main/skills/dreamina-cli/references/dreamina-cli-v1.4.18-contract.md)（如未安装：`npx skills add full-aigc-skills/dreamina-skills --skill dreamina-cli`）
- [参数参考](references/parameter-reference.md)
- [模型选择](references/model-guide.md)
- [VIP 指南](references/official-doc-vip-guide.md)
- [工作流模式](references/workflow-patterns.md)
- [示例](examples/basic-generation.md)
