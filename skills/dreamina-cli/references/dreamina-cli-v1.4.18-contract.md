# Dreamina CLI v1.4.18 契约

> 来源：2026-09-11 通过官方安装入口 `curl -s https://jimeng.jianying.com/cli | bash`
> 安装的 v1.4.18 元数据，以及本机 `dreamina <subcommand> -h` 输出。二进制自报
> `ec1b9fa-dirty`（commit `ec1b9fa`，build time `2026-09-09T09:09:35Z`）。
> 执行真实任务前仍须重跑对应子命令 help；本文件是已审计快照，不替代运行时 schema。

## v1.4.18 变化

- 视频生成新增比例控制，但不是所有视频命令都接受 `--ratio`。
- `text2video`、`image2video`、`frames2video`、`multimodal2video` 接受
  `1:1`、`3:4`、`16:9`、`4:3`、`9:16`、`21:9`。
- `multiframe2video` 不暴露 `--ratio`，输出比例从首图推断。
- `image2video` 与 `frames2video` 使用 `seedance2.5` 时禁止显式传 `--ratio`，
  输出比例跟随首帧。
- `seedance2.5` 视频输出支持 480p、720p、1080p，时长 4–30 秒。

## 图片生成

| 命令 | 模型 | `resolution_type` |
|---|---|---|
| `text2image` | 3.0/3.1 | 1k、2k |
| `text2image` / `image2image` | 4.0/4.1/4.5/4.6/4.7/5.0 | 2k、4k |
| `text2image` / `image2image` | `5.0Pro` | 1.5k、2k、4k |

- `--resolution_type` 必填。
- `--width` 与 `--height` 必须成对提供、为正整数，并与 `--ratio` 互斥。
- 自定义尺寸边长/总像素同时受限：
  - 1k：边长 512–2016，总像素不超过 1,763,584；
  - 2k：边长 768–3072，总像素不超过 4,194,304；
  - 4k：边长 1536–6240，总像素不超过 16,777,216。
- `generate_num` 范围 1–10。
- CLI token 是 `5.0Pro`；“Seedream 5.0 Pro”只用于展示。

## 视频生成

| 命令 | 比例行为 | Seedance 2.5 | 分辨率 |
|---|---|---|---|
| `text2video` | 可传 `--ratio`；省略时 16:9 | 支持显式比例 | 480p/720p/1080p |
| `image2video` | 可传 `--ratio`；省略时跟随首帧 | 禁止显式比例，跟随首帧 | 480p/720p/1080p |
| `frames2video` | 可传 `--ratio`；省略时跟随首帧 | 禁止显式比例，跟随首帧 | 480p/720p/1080p |
| `multimodal2video` | 可传 `--ratio`；省略时 16:9 | 支持显式比例 | 480p/720p/1080p |
| `multiframe2video` | 无 `--ratio`，跟随首图 | 不支持；固定模型 | 720p/1080p |

- 所有视频生成命令仍须显式传 `--video_resolution`。
- `image2video` 的 `--image`、`--prompt`、`--video_resolution` 必填。
- `seedance1.0fast` 时长 5–10 秒；`seedance1.5pro` 时长 5–12 秒；
  Seedance 2.0 家族时长 4–15 秒；`seedance2.5` 时长 4–30 秒。
- `multimodal2video` 允许 `seedance2.5` 纯音频输入；参考音视频总时长 2–30 秒。
- `multiframe2video` 接受 2–20 张图；单段时长 1–8 秒，总时长至少 2 秒。

## 异步状态

- `querying`：任务仍在进行，不是成功终态。
- `success`：成功终态。
- `fail`：失败终态；读取并报告 `fail_reason`。
- 兼容读取历史别名 `failed`，但文档和新代码统一写 `fail`。

## 防漂移流程

1. 从页面“右上角头像 → 即梦插件与 CLI”获取当前官方安装入口。
2. 审计安装脚本后升级 CLI。
3. 运行 `dreamina version`、`dreamina -h` 和每个生成子命令的 `-h`。
4. 更新 `verification/dreamina-cli-v1.4.18-contract.json` 中的版本、哈希和命令能力。
5. 运行仓库测试、逐 Skill 校验及 TRACE 检查。
