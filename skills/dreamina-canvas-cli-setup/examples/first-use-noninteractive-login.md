# Agent 无交互登录

登录已经获得用户授权且 Agent 终端无法应答提示时，先发起一次 `dreamina-canvas --non-interactive auth login`，将 CLI 返回的授权入口交给用户。保留本次 challenge 的必要标识，仅在进程内继续 `dreamina-canvas auth wait --device-code <本次设备码>`。完成后执行 `dreamina-canvas auth account`。等待超时只表示当前等待结束；不要在循环中重发 login，也不要公开设备码或凭据。
