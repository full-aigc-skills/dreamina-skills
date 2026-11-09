# 工作流批量生成与模板复用（CLI 1.3.0）

以下命令名和 flag 来自本机公开版 cn `dreamina-canvas 1.3.0 / c6a5530a` 的只读 schema。先运行 `dreamina-canvas version`、`dreamina-canvas schema` 和目标命令 `--help`；旧版本没有 `workflow` 时停止，不把节点批量运行冒充模板工作流。

## 选择来源与预检

`workflow capabilities --project-id <projectId>` 只读返回启用状态、生成与后处理能力、限额及模板可见范围。`workflow quote` 的 `--source` 必须是 `group`、`template` 或 `retry`，并带对应身份：

| 来源 | 必须从当前返回值取得的输入 |
|---|---|
| `group` | `--group-node-id`、`--expected-draft-version`；可按 schema 使用 `--definition-revision` |
| `template` | `--template-id`、`--template-version` |
| `retry` | 原 `--run-id`；可逐个重复传 `--selected-combo-ids` / `--selected-step-ids` |

`--run-kind` 从 `normal|trial|batch|retry` 中按需求选择；先查当前能力和限额。需要组合变量时，读取 `schema 'workflow quote'` 中 `combos-file` 的 `fileContent`/`fileExample` 契约，用当前模板变量定义填写真实值，不把示例直接提交。`--from-node-ids`、`--selected-combo-ids`、`--selected-step-ids` 均一次传一个 ID，多个值重复 flag，不用逗号连接。

## 报价、批准与运行

先给 `workflow quote` 提供稳定的 `--request-id`、`--project-id`、`--source` 及对应来源参数。它只返回报价计划，不提交工作流、不扣积分。记录 `quoteId`、`planDigest`、`expiresAtMs`、逐组合报价、`totalMaxCredits`、`finalOutputCount`、`confirmationRequired`、`canStart`；不能运行时按返回原因修正输入。

需要确认时，向用户展示本次工作流的组合、产物数及总积分上限，取得批准后执行 `workflow confirm --quote-id <quoteId> --max-credits <approvedCredits>`，得到短期 `creditConfirmationToken`。仅将该 token 传给同一报价的 `workflow run --quote-id <quoteId> --submit-id <stableUuid> --credit-confirmation-token <token>`；不需要确认时按当前 schema 省略 token。`workflow confirm` 的 `--max-credits` 与普通 `node confirm` 的 `--credit-ceiling` 是不同契约，不能互换。token 只留在进程内存，不写入日志或文件。

```bash
# 下列占位值来自当前 CLI 返回值；先查 capabilities 和所选模板版本。
dreamina-canvas --format json workflow quote --request-id <quoteRequestUuid> \
  --project-id <projectId> --source template \
  --template-id <templateId> --template-version <version> --run-kind batch
# 展示返回的 quoteId、totalMaxCredits 和 finalOutputCount，取得本次批准后：
dreamina-canvas --format json workflow confirm --quote-id <quoteId> \
  --max-credits <approvedCredits>
dreamina-canvas --format json workflow run --quote-id <quoteId> \
  --submit-id <stableUuid> --credit-confirmation-token <inMemoryToken>
```

报价有 `expiresAtMs`；过期后重新报价并取得适用的新批准，不用旧 quoteId 或 token 强行运行。

在运行前持久记录同一 `submitId` 和报价身份。受理后保存 `rootRunId`、`comboRunIds`，用 `workflow get <runId>`、`workflow wait <runId>` 或 `workflow list --project-id <projectId>` 观察原运行；等待超时不代表失败。响应不明时先按原身份查询；不能换新 submitId 重跑。`workflow cancel <runId>` 会改变远端运行，只有用户要求取消时才调用；取消请求也使用稳定 `--request-id`。

## 模板复用

用 `workflow template list` 查询可见模板，`workflow template get <templateId> --version <version>` 检查所选版本及变量定义。`workflow template instantiate` 需要 `--template-id`、`--version`、`--target-project-id`，并可传 `--variables-file` 与落位坐标。变量文件按 `schema 'workflow template instantiate'` 的 `fileContent`/`fileExample` 结构填写；实例化前确认目标画布和空间。实例化写入画布，但不等于已经运行生成。保存稳定 `--request-id`，结果未知时用相同请求身份恢复；`workflow template instantiation <instantiateId>` 查询实例化状态。实例化后如需生成，重新按上述工作流报价与批准。

1.3.0 的 JSON envelope `schemaVersion` 为 `2`。错误以退出码、`error.code`、`requiredAction`、`error.operationRef` 等结构化字段判断，避免解析本地化文案；反馈问题时附完整命令、错误、CLI 版本及可用的 `meta.requestId`，隐藏凭据。每个必要产物还需检查最终资源与下载校验，不能以运行受理代替完成。
