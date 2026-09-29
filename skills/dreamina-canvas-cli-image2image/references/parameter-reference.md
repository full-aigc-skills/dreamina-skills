# Parameter Reference — Canvas Image-to-Image

> 以 `dreamina-canvas schema`、`schema`、
> `schema` 与 live discovery 为最终事实源。

## 素材摄入（i2i 前置，免费侧）

| 命令 | 关键参数 | 说明 |
|------|----------|------|
| `resource upload` | `--file <绝对路径>`、`--name <标签>` | 本地图/视频/音频 → 资源；返回小写 canonical `resourceId`，必须持久化 |
| `resource get` | `<resourceId>`、`--project-id` | 查询素材状态 |
| `node create image --resource-id <id> --import-kind local_upload` | 见 `dreamina-canvas-cli` 契约 | 把已上传资源导入为画布节点；之后优先 `node:` 引用保上下游 |

引用写法（`--ref` 只接受两类）：

| 写法 | 适用 |
|------|------|
| `node:<nodeId>` | 引用画布节点最新产物，保留上下游；素材已是节点时**优先** |
| `res:<resourceId>` | 冻结引用一份确定素材；UUID 必须来自 CLI 返回 |

`uri:` / `vid:` / `file://` / 内部短链一律被服务端拒绝。

## 草稿与编辑：`node create/edit image --mode i2i`

| 参数 | 必填 | 取值/约束 |
|------|------|-----------|
| `--prompt` | 是 | 编辑意图（"保持主体不变，换成水墨风格"） |
| `--mode` | 生成参数变化时必填 | 本任务恒为 `i2i` |
| `--model` | 是 | discovery 的 model 值 |
| `--ratio` / `--resolution` / `--count` | 否 | 均取该模型白名单；`--resolution` 图片生成必填 |
| `--ref` | **是（至少一个图像引用）** | Image / Element / 图片资源；可加文本引用 |
| `--clear-generation` | 仅 edit | 清空生成设置；与所有生成 flag 互斥 |

**全量替换规则**：`node edit image` 动任何一个生成参数（mode/model/
ratio/resolution/count/prompt/ref）就必须给完整新块；漏传 = 清空。
元数据（title/description/tags）才是稀疏更新。

## 高清放大：`node upscale image`（独立定价）

| 参数 | 说明 |
|------|------|
| `--node-id <源图节点>` | 必填；产物写入**新节点**，源节点不变 |
| `--mode <m>` / `--resolution <r>` | 以 `schema` 与报价为准 |
| `--detail` | 仅 pro 模式；先 schema 确认再传 |
| `--dry-run` | 本地校验，免费 |
| `--submit-id` / `--credit-ceiling` / `--wait` | 与主生成链相同的幂等纪律 |

**upscale 的批准 token 仅限 upscale 作用域**；`node confirm` 的 token
在此无效，反之亦然。

## 旧 v1.4.18 → Canvas 映射（禁止原样搬运）

| 旧 `dreamina image2image` / `image_upscale` | Canvas 对应 |
|------|------|
| `--image_path=` 本地路径 | `resource upload --file` → `--ref res:<uuid>` |
| `--model_version=` | `--model <live discovery model 值>` |
| `--resolution_type=` | `--resolution <live discovery 值>` |
| `--strength` / `--wps` | 以 live schema 为准；未声明不得臆造 |
| `image_upscale` | `node upscale image`（独立报价，新建节点） |

```bash
dreamina-canvas --format json node create image \
  --prompt "<edit prompt>" --mode i2i --model <model> \
  --ref res:<frozenResourceUuid>
```
