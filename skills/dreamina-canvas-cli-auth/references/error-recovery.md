# Error Recovery — Canvas CLI Auth Task

| 场景 | 现象 | 恢复动作 |
|------|------|----------|
| 登录态失效 | exit 11 | `auth login` 重授权，同一身份重试原命令。 |
| 账号不符 | account 返回非预期账号 | 确认 `--profile`；换号用 `--force`。 |
| 授权页面打不开 | 用户无法完成浏览器步骤 | 手动贴 URL；仍失败按四件套反馈。 |
| wait 反复超时 | 授权未完成 | 同 code 续等；过期则重新 login 拿新 code。 |
| refresh 被拒 | 不在 refresh window | 不投机；等窗口或重新 login。 |
| logout 后仍可用 | 缓存/多 profile | 确认目标 profile；服务端态以 `auth account` 复核。 |

## 红线

- 不以 `auth status` 单独作为登录证据。
- 不在日志持久化 token / cookie / device code。
- 不在本技能运行付费命令。
