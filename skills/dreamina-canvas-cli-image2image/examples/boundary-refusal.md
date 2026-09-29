# Boundary Refusal — 拒绝越权

## 场景 A：跳过上传直接引用本地路径

用户：「`--ref` 里直接写 `/Users/me/photo.jpg` 不就行了。」

- Canvas 只接受 `node:` / `res:` 引用；`file://` / `uri:` / 本地路径
  一律被服务端拒绝。
- 回复：先 `resource upload --file` 拿 `res:<uuid>` 再建草稿。

## 场景 B：upscale 混用主生成批准

用户：「刚才 `node confirm` 已经批过了，直接用它跑 upscale。」

- upscale 独立定价，批准 token 仅限 upscale 作用域；`node confirm`
  token 在 `node upscale image` 上无效。
- 回复：走 `node upscale image --dry-run` → 展示报价 → 重新取得精确
  上限批准（归 `dreamina-canvas-cli` 执行）。

## 场景 C：把重风格当增量补丁

用户：「只把 prompt 换了，其他参数保持原样，别重传。」

- `node edit image` 的生成编辑是**全量替换**：漏传 flag 即清空该项。
- 回复：用 `node show` 读出当前完整生成块，修改后整块回传；元数据
  （title 等）才可以稀疏更新。

## 场景 D：要求本技能直接跑付费命令

任何附加 `--run` / `--credit-ceiling` / `--credit-token` 的请求一律
拒绝；付费边界属于 `dreamina-canvas-cli`。
