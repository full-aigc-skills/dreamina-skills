# 准备画布与素材

本场景不执行生成：no paid action。只补齐后续任务缺少的身份和素材。

1. 通过 [模型发现](discovery.md) 的 model list/model find 选择当前能力。
2. 通过 [画布操作](canvas.md) 创建或确认 projectId；canvas create 跨进程重试复用 ID，canvas ls 不切换上下文。
3. 按 [资源操作](resources.md) resource upload 注册素材，再 resource get 核对原 resourceId。
4. 需要可见节点时用 node create image --resource-id <resourceId> --import-kind local_upload 导入；记录 nodeId。
5. 后续优先 node:<nodeId> 保留画布关系；用户要求冻结时用 res:<resourceId>。

输入：媒体类型、已存在画布或名称、可读素材。输出：projectId/webUrl、resourceId/nodeId 清单、实时模型规格。
副作用：画布创建、资源上传与节点保存；不带 --run，不批准积分。
恢复：查询原 ID；只有确定未完成的步骤才恢复，不把整个准备流程从头重复。
验收：资源成功、节点可查询，已保存的身份可以跨进程使用。

场景命令见 [准备实例](../examples/preparation-happy-path.md)。
