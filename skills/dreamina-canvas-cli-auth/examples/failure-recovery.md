# Failure Recovery — 登录态失效与换号

场景：任务命令返回 exit 11（需要登录）。

```bash
# 重新授权（同一身份），然后重试原命令
dreamina-canvas --format json auth login
dreamina-canvas --format json auth account   # 自检
# 用同一身份重试之前失败的原命令
```

场景：换账号。

```bash
# --force 清当前登录态后重新授权
dreamina-canvas --format json auth login --force
dreamina-canvas --format json auth account   # 确认已是新账号
```

场景：`auth wait` 反复超时。

```bash
# 同一 device code 再 wait；授权过期则重新 login 拿新 code
dreamina-canvas --format json auth wait --device-code <code> --timeout 10m
```
