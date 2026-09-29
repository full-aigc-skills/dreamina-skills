# Validation Checklist — Canvas CLI Auth Task

交付前逐项确认：

- [ ] 登录子命令与环境匹配（TTY=login；Agent=non-interactive+wait）。
- [ ] Agent 流程未原地轮询 login；device code 经 `auth wait` 续等。
- [ ] 闭环自检用 `auth account`（服务端），未以 `auth status` 充当
      登录证据。
- [ ] 换账号使用 `--force`；退出确认当前 profile 无误。
- [ ] refresh 仅在 refresh window 内调用。
- [ ] 日志/交付物不含 token、cookie、device code 残留。
- [ ] 交付含服务端账号结论（按隐私规则）与下一步交接。
