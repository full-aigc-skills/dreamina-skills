# Profile & Canvas Workflow — 多项目隔离（替代旧 session）

用户：「工作项目和私人文案分开，别串账号和画布。」

```bash
# 1. 两个 profile 各登录一次（凭据与画布上下文按 profile 隔离）
dreamina-canvas --format json auth login --profile work
dreamina-canvas --format json auth login --profile personal

# 2. 每块画布归属于当前 profile 的上下文
dreamina-canvas --format json --profile work canvas create "Q4 视觉物料" --use
# → projectId_work（webUrl 可发给设计同事看）
dreamina-canvas --format json --profile personal canvas create "随笔配图" --use
# → projectId_personal

# 3. 之后所有 node/operation/resource 命令显式带 --profile 与 --project-id
dreamina-canvas --format json --profile work node create image \
  --title "头图" --prompt "<prompt>" --mode t2i \
  --model <model> --ratio 16:9 --resolution <resolution> --count 1
# 交接 quote-and-run / resume-operation / download-assets 时同样带全

# 4. 查看近期画布（只读，不切换当前画布）
dreamina-canvas --format json --profile work canvas ls --limit 20
```

要点：`canvas ls` 不会切当前画布；当前画布记录在
`dreamina-canvas/contexts/<profile-and-environment>.json`。跨设备续作靠
显式 `--project-id`，不靠隐式上下文。
