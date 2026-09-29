# Parameter Reference — Canvas Reference-to-Video

> 以 `dreamina-canvas schema`、`schema`
> 与 live discovery 为最终事实源。

## 素材摄入（与 i2i 共用上传契约）

| 命令 | 关键参数 | 说明 |
|------|----------|------|
| `resource upload` | `--file`、`--name` | 返回 `resourceId`（小写 UUID），持久化 |
| `node create image --resource-id <id> --import-kind local_upload` | 契约归 `dreamina-canvas-cli` | 帧素材导入为画布节点，之后优先 `node:` 引用 |

`--ref` 只接受 `node:<nodeId>` / `res:<resourceId>`；`uri:` / `vid:` /
`file://` / 短链一律拒绝。

## 模式选择（本任务核心）

| 模式 | 引用 | 适用 |
|------|------|------|
| `m2v` | 1 个图像/视频/Element 引用（可加） | 单图"动起来"、运动引导、多模态参考 |
| `first_last_frame` | 1–2 个**有序**帧引用 | 首帧生成，或首尾帧 + 转场 |
| ~~`i2v`~~ / ~~`multi_modal`~~ | — | **不存在**；CLI 以 exit 2 拒绝，不得传入 |

双帧规则：两帧源比例必须一致；输出比例跟随**首帧**。

## 草稿保存：`node create video`

| 参数 | 必填 | 取值/约束 |
|------|------|-----------|
| `--prompt` | 是 | 运动/转场意图 |
| `--mode` | 生成参数变化时必填 | `m2v` 或 `first_last_frame` |
| `--model` | 是 | `model list --type video` 的 model 值 |
| `--duration` | **是** | >0，缺省 5，上限取 discovery |
| `--ratio` | 视模型 | 帧驱动模型通常按首帧推断 → **不传**；discovery 写明支持时可传且须与首帧一致 |
| `--resolution` | 否 | 模型白名单 |
| `--ref` | 是（帧任务） | 有序传入；先首后尾 |
| `--run` | **本技能禁止** | 付费只发生在 quote-and-run |

## 付费链 / 观察 / 下载

与文生视频同构：`node quote` → `node confirm` → `node run`
（每 node 一个稳定 `--submit-id`）→ `operation status/wait` →
`resource get/download`。视频等待用 `--timeout 10m --interval 5s`。

## 旧 v1.4.18 → Canvas 映射（禁止原样搬运）

| 旧 `dreamina image2video` / `frames2video` / `multimodal2video` | Canvas 对应 |
|------|------|
| 单图生视频（`image2video`） | `--mode m2v` + 1 引用 |
| 首尾帧（`frames2video`） | `--mode first_last_frame` + 2 有序引用 |
| 多帧故事（`multiframe2video`） | 无直接对应；拆为多个 `first_last_frame`/`m2v` 节点，由时间轴技能串接 |
| 多模态参考（`multimodal2video`） | `--mode m2v`（多模态参考归 m2v 域） |
| `--image_path=` | `resource upload` → `res:` / 导入节点 `node:` |
| `--video_resolution=` | `--resolution` / 模型档位，以 discovery 为准 |

```bash
dreamina-canvas --format json node create video \
  --prompt "<motion prompt>" --mode m2v --model <model> \
  --ref res:<frozenResourceUuid> --duration 5
```
