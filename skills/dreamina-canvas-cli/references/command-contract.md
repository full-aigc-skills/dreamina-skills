# 公共调用契约

## 前置与输入
使用 `dreamina-canvas --help`、`dreamina-canvas version` 和 `dreamina-canvas schema` 核对当前制品。schema 返回整棵树；定位所需命令，或运行该命令的 `--help`，不把命令路径作为 schema 的位置参数。
同一会话可复用相同 CLI 制品的契约；版本、环境或 profile 改变后重新发现。模型和音色来自当前环境的查询结果。
需要服务端权限的操作，先交给 `dreamina-canvas-cli-auth` 检查；无需登录的 help/version/schema 不强行要求认证。

## 构造与输出
使用 argv 数组；不把用户文本插值进 shell。全局参数 `--format json`、`--non-interactive`、`--profile`、`--region` 位于子命令前。
分别读取 stdout 与 stderr，保留退出码；按 `error.code` 和 `requiredAction` 路由，不依赖本地化 message。
成功响应读 `data`。失败读 error；有 `partialData.items` 时逐项保存已经返回的身份。退出 0 或取得 submitId 不代表媒体已经成功生成。

## 身份与副作用
`projectId`、`resourceId`、`submitId` 使用各自契约要求的小写 UUID。`nodeId` 是 CLI 返回的 node_ 标识，不能把所有 ID 当成 UUID。`updateId` 依实时 schema 管理。
首次写入前持久化支持的幂等键；跨进程显式传 projectId/profile，不依赖其他进程的 --use。
普通节点 create/edit 不带 --run 只保存草稿；修改生成参数是完整替换，元数据编辑是稀疏更新。
Never persist or log tokens, cookies, signed URLs or creditConfirmationToken; keep short-lived approval material in-memory only.

## 恢复与验收
exit code 20 表示可恢复操作，使用原 submitId 查询。退出 21 的写请求也可能已到服务端，先核对状态再决定重试。
仅服务端明确 absent 且 resubmittable=true 才允许按原身份恢复提交；未知状态不生成新 submitId。
验收记录版本、操作、输入身份、输出身份、终态及文件 size/SHA-256。未运行的登录或生成明确写 NOT_RUN。
