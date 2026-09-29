# Happy Path — Agent 环境登录全流程

用户：「帮我登录即梦画布，我要开始用了。」（CLI 已装好）

```bash
# 1. 非交互登录，取 device code
dreamina-canvas --format json --non-interactive auth login
# → challenge payload：device code + 授权 URL；把 URL 发给用户打开

# 2. 续等（同一 code；超时就再 wait）
dreamina-canvas --format json auth wait --device-code <code> --timeout 10m

# 3. 服务端自检（唯一可信的"已登录"证据）
dreamina-canvas --format json auth account
# → 报告服务端识别的账号（按隐私规则处理标识）

# 4. 交接后续任务技能（如 dreamina-canvas-cli 准备画布素材）
```

TTY 环境把第 1-2 步换成 `dreamina-canvas auth login`（阻塞到用户完成
浏览器授权）即可。
