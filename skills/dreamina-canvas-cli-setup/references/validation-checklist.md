# Validation Checklist — Canvas CLI Install Task

交付前逐项确认：

- [ ] 安装/升级动作均在用户显式授权之后执行。
- [ ] 安装器与当前 OS/终端匹配（三选一，无混用）。
- [ ] 安装位置已知并告知用户（默认或批准的自定义目录）。
- [ ] `dreamina-canvas --help` 可见 auth、canvas、model、node、
      operation、resource 等命令族。
- [ ] `version` / `schema` 结构化输出正常（非仅凭下载退出码判定成功）。
- [ ] 排障场景：先重开终端验证 PATH，再升级重试，最后按四件套反馈。
- [ ] 已交接 `dreamina-canvas-cli-auth` 做登录授权（或说明用户暂不登录）。
