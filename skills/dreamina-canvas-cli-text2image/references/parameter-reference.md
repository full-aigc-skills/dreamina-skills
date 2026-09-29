# Parameter Reference — Canvas Text-to-Image（dreamina-canvas CLI）

> 以 `dreamina-canvas schema` 与 live discovery 为最终事实源；
> 本表是与指南对账后的稳定形态。旧 v1.4.18 参数仅列于文末映射表，禁止原样搬运。

## 全局 flag（放在子命令之前）

| flag | 必填 | 说明 |
|------|------|------|
| `--format json` | 是 | 机器驱动调用必传；否则结果取决于 TTY |
| `--non-interactive` | 脚本环境推荐 | 禁用交互提示；付费确认不能用提示绕过 |
| `--yes` | 否 | 仅参数可确认的操作；绝不绕过积分确认 |
| `--profile <name>` | 否 | 凭据与画布上下文隔离 |
| `--region cn` | 否 | 国内公开版固定 cn；海外版无此 flag |

## 草稿保存：`node create image`（免费，不进入生成流程）

| 参数 | 必填 | 取值/约束 |
|------|------|-----------|
| `--title` | 推荐 | 画布上显示的节点标题 |
| `--prompt` | 是 | 非空；含 `{{type:value}}` 占位符时按引用解析 |
| `--mode` | 生成参数变化时必填 | 本任务恒为 `t2i` |
| `--model` | 是 | 取 `model list --type image` 返回的 **model 值**；别名只用于查找 |
| `--ratio` | 否 | 取 discovery 中该模型支持的比例；缺省按模型默认 |
| `--resolution` | 是（图片生成） | 取 discovery 中该模型支持的分辨率 |
| `--count` | 否 | 生成数量；范围以 discovery 为准 |
| `--ref` | **t2i 禁止** | t2i 不接受图像/Element/资源引用（i2i 见对应任务技能） |
| `--run` | **本技能禁止** | 付费执行只发生在 `dreamina-canvas-cli` |

编辑既有节点用 `node edit image`：生成参数是**全量替换**（漏传即清空），
元数据（title/description/tags）是稀疏更新；`--clear-generation` 与生成
flag 互斥。

## 付费链（交接 `dreamina-canvas-cli`）

| 命令 | 作用 | 关键约束 |
|------|------|----------|
| `node quote --node-id <id>` | 查询已保存节点的预计积分 | 报价 ≠ 批准；免费 |
| `node confirm …` | 用户精确批准 | `--credit-ceiling` 为精确上限；token 不落盘 |
| `node run …` | 提交生成 | 每个 node 一个稳定 `--submit-id`；复用不重复计费 |

## 观察与下载

| 命令 | 说明 |
|------|------|
| `operation status <submitId> --project-id <id>` | 单次查询任务状态 |
| `operation wait <submitId> --project-id <id> --timeout 10m --interval 5s` | 等终态；超时（exit 20）不取消服务端任务 |
| `resource get <resourceId> --project-id <id>` | 查询产物状态 |
| `resource download <resourceId> --project-id <id> --output <dir>` | 下载到**已存在**的目录 + SHA-256 校验 |

## 旧 v1.4.18 → Canvas 映射（仅供迁移对照，禁止原样搬运）

| 旧 `dreamina text2image` | Canvas 对应 |
|------|------|
| `--prompt=` / `--ratio=` | `--prompt` / `--ratio`（argv 列表，非等号拼接） |
| `--model_version=5.0`、`5.0Pro` | `--model <live discovery model 值>` |
| `--resolution_type=1k/2k/4k` | `--resolution <live discovery 值>` |
| `--generate_num=N` | `--count N` |
| `--width/--height` | 以 live schema 为准；不存在时不得臆造 |
| `--session=<id>` | 无对应；用画布（`canvas create --use`，projectId）+ `--profile` 组织 |
| `--poll=0/30` + `query_result` | 草稿 + `node quote/confirm/run` + `operation wait` |
| `user_credit` | `node quote`（报价以服务端实时返回为准） |

```bash
dreamina-canvas --format json node create image \
  --title "示例" --prompt "<finalized prompt>" \
  --mode t2i --model <model> --ratio <ratio> --resolution <resolution> --count 1
```
