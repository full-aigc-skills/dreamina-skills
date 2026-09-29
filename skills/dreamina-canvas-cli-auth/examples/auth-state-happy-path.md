# 登录与账户自检

示意命令中的 `<...>` 是占位符，须用当前 CLI 返回的值替换后执行；不要原样复制。

用户授权登录后，在浏览器完成设备授权；只有服务端账户查询成功才报告已就绪。

```bash
dreamina-canvas auth login
dreamina-canvas auth account
dreamina-canvas auth status
```

`auth status` 只看本地状态。Agent 无交互环境可运行 `dreamina-canvas --non-interactive auth login`，按 CLI 返回的 challenge 继续 `dreamina-canvas auth wait --device-code <本次设备码>`；不得公开或持久化设备码。`auth login --force`、`auth refresh`、`auth logout` 分别用于明确要求的重新登录、续期和退出。
