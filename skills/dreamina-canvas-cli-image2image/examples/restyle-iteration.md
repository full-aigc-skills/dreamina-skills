# Restyle Iteration — 画布节点重风格迭代

用户：「上次那张图再试两版：一版更淡的墨色，一版加暖色调。」

```bash
# 1. 读回当前生成块（全量替换前必做）
dreamina-canvas --format json node show --node-id <nodeId>

# 2. 版 A：全量替换（注意块完整：mode/model/ratio/resolution/count/prompt/ref）
dreamina-canvas --format json node edit image \
  --node-id <nodeId> \
  --prompt "<淡墨版 prompt>" --mode i2i \
  --model <model> --ratio <ratio> --resolution <resolution> --count 2 \
  --ref res:<frozenResourceUuid>
# 3. 交接 quote-and-run：quote → 批准 → run（新一轮计费）

# --- 版 A 完成后对同一节点再做版 B ---
# 4. 重新 node show（确认当前块），再整块替换为暖色版参数
# 5. 重新 quote → 重新批准 → run
```

要点：每一版都是新一轮生成、独立计费；节点身份保留，画布历史可回溯。
要并行试两版且不想互相覆盖时，复制为新节点（另存草稿）而不是反复
编辑同一节点。
