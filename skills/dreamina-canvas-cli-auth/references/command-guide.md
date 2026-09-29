# Command Guide — auth 七子命令场景选择

> 官方指南 §3 的命令表 + 环境化选择。安全红线以
> `dreamina-canvas-cli-auth` 为准。

## 选择矩阵

| 场景 | 命令 |
|------|------|
| TTY 首次登录 | `auth login` |
| 换账号 / 登录态损坏 | `auth login --force` |
| Agent/脚本首次登录 | `--non-interactive auth login` → 取 device code |
| 续等授权 | `auth wait --device-code <code>`（默认最长 10 分钟；`--timeout 0` 轮询一次） |
| 登录闭环自检 | `auth account` |
| 本地态排障 | `auth status`（不作登录证据） |
| 续期 | `auth refresh`（仅 refresh window 内） |
| 退出 | `auth logout` |

## Agent 环境流程

```bash
dreamina-canvas --format json --non-interactive auth login
# → device code + 授权 URL；把 URL 呈现给用户，不要原地轮询
dreamina-canvas --format json auth wait --device-code <code> --timeout 10m
dreamina-canvas --format json auth account   # 唯一可信自检
```

## 常见误判

| 误判 | 纠正 |
|------|------|
| auth status 显示已登录 = 可用 | 服务端可能已撤销；以 `auth account` 为准 |
| wait 超时 = 授权失败 | 授权可能仍在进行；同 code 续等 |
| refresh 越早越好 | 仅在 refresh window 内调用，不投机 |
| 换账号直接 login | 用 `--force` 清当前态再授权 |
