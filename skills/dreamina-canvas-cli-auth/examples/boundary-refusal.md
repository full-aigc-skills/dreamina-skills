# Boundary Refusal — 拒绝越权

## 场景 A：凭 auth status 宣称已登录

用户：「status 显示 logged in，直接干活吧。」

- `auth status` 只读本地文件，服务端可能已撤销；唯一可信自检是
  `auth account`。
- 回复：跑一次 `auth account` 确认服务端身份再进任务。

## 场景 B：要求记录凭据备用

用户：「把 token 存下来，下次省得登。」

- 凭据不落盘、不进日志（红线归 `dreamina-canvas-cli-auth`）。
- 回复：登录态由 CLI 按 profile 管理；续期用 `auth refresh`，
  重登用 `auth login`。

## 场景 C：跳过浏览器授权

任何"绕过用户浏览器确认"的授权请求一律拒绝；授权动作必须用户
亲手完成。

## 场景 D：登录后直接跑付费生成

登录闭环只到 `auth account`；付费生成走任务技能 + quote-and-run
的报价批准链，不在本技能执行。
