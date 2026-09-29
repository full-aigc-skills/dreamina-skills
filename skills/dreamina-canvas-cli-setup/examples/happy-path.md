# Happy Path — 新机器安装全流程

用户：「帮我在这台 Mac 上装一下即梦画布 CLI。」

```bash
# 0. 确认 OS/终端与现有状态（只读）
uname -a
command -v dreamina-canvas || echo "not installed"

# 1. 说明来源与目标目录，取得用户显式授权后执行（macOS/Linux 示例）
curl -fsSL https://jimeng.jianying.com/canvas-cli/install.sh | bash
# → 记录安装器输出中的安装位置

# 2. 重开终端（或按提示应用 PATH），验证可用性
dreamina-canvas --help
# 成功标准：能看到 auth、canvas、model、node、operation、resource

# 3. 结构化验证
dreamina-canvas --format json version
dreamina-canvas --format json schema

# 4. 交接 dreamina-canvas-cli-auth：登录 → auth account 自检
```

要点：升级时重跑同一安装器即可；验证永远以 live `--help`/`version`/
`schema` 为准。


验证命令形态：`dreamina-canvas --help`、`dreamina-canvas version`、`dreamina-canvas schema`；授权登录后再通过 `auth account` 验证账户。
