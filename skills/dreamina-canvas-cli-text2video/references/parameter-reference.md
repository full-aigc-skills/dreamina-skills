# Parameter Reference — Canvas Text-to-Video

> 以 `dreamina-canvas schema` 与 live discovery 为最终事实源。

## 全局 flag

同文生图任务：`--format json`（必传）、`--non-interactive`、`--yes`、
`--profile`、`--region cn`。

## 草稿保存：`node create video`（免费）

| 参数 | 必填 | 取值/约束 |
|------|------|-----------|
| `--title` | 推荐 | 节点标题 |
| `--prompt` | 是 | 必须含运动意图（镜头/主体运动/节奏）；纯画面描述不足以驱动视频 |
| `--mode` | 生成参数变化时必填 | 本任务恒为 `t2v` |
| `--model` | 是 | `model list --type video` 返回的 model 值 |
| `--duration` | **是** | >0 秒；缺省 5；上限取 discovery 的模型规格 |
| `--ratio` | 否 | 仅当该模型契约接受时传；按比例推断的模型**不传** |
| `--resolution` | 否 | 以该模型白名单为准 |
| `--count` | 否 | 数量上限以 discovery 为准 |
| `--ref` | **t2v 禁止** | 有素材的视频任务走 `dreamina-canvas-cli-ref2video`（m2v / first_last_frame） |
| `--run` | **本技能禁止** | 付费只发生在 quote-and-run |

编辑规则与图片一致：`node edit video` 生成参数全量替换、元数据稀疏、
`--clear-generation` 互斥。

## 付费链 / 观察 / 下载

与文生图任务同构：`node quote` → `node confirm`（精确
`--credit-ceiling`）→ `node run`（每 node 一个稳定 `--submit-id`）→
`operation status/wait <submitId> --project-id <id>` →
`resource get/download <resourceId> --project-id <id>`。

视频任务额外注意：`operation wait` 建议 `--timeout 10m --interval 5s`；
本地超时（exit 20）不取消服务端任务。

## 旧 v1.4.18 → Canvas 映射（禁止原样搬运）

| 旧 `dreamina text2video` | Canvas 对应 |
|------|------|
| `--prompt=` | `--prompt` |
| `--ratio=`（旧默认 16:9） | `--ratio`，仅当模型契约接受；默认以 discovery 为准 |
| `--model_version=` | `--model <live discovery model 值>` |
| `--resolution_type=` | 无对应；按 discovery 规格 |
| `--duration=` / `--fps` | `--duration`（必填，模型上限） |
| `--poll=0/30` + `query_result` | `node quote/confirm/run` + `operation wait` |
| `user_credit` | `node quote` |

```bash
dreamina-canvas --format json node create video \
  --title "示例" --prompt "<motion prompt>" \
  --mode t2v --model <model> --ratio <ratio> --duration 5
```
