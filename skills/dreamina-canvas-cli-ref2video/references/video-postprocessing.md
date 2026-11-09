# 视频样片与后处理

开始前读取 `dreamina-canvas version`、`schema` 和目标命令 `--help`；模型的样片能力及转正参数来自当前 `model list/find`，不复用历史模型名或价格。

| 用户目标 | 本机 1.2.0 已核实的命令 | 验收重点 |
|---|---|---|
| 样片转正片 | `node promote video-sample` | 样片源节点、转正后节点/资源和终态分别核对 |
| 视频超清 | `node upscale video` | 输出分辨率来自实时 schema 与报价 |
| 视频补帧 | `node interpolate video` | 目标 fps 来自实时 schema 与服务端能力 |

三个后处理命令都可能消耗积分，分别走自身的 `--dry-run` 报价、用户批准的 `--credit-ceiling`、稳定的 `--submit-id` 与 `operation status/wait`。不要复用普通 `node confirm` 或其他后处理操作的批准信息。即使生成视频的费用已批准，转正、超清、补帧仍需分别展示实时报价。等待超时只代表本地等待结束；继续查询原 submitId。下载后按资源元数据核对字节数和 SHA-256。

样片生成属于视频节点的模型参数选择；先检查当前模型是否提供样片及转正能力，不猜测 `--mode` 值。普通 `m2v`、`first_last_frame` 和 `t2v` 的草稿规则仍由各自场景技能维护。
