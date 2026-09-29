# Task Contract — Canvas CLI Install

## 职责划分

| 环节 | 责任技能 |
|------|----------|
| argv/退出码通则 | `dreamina-canvas-cli` |
| 安装契约内部（海外版、目录变量、验证清单） | 本技能的 [安装契约](install-to-use.md) |
| 登录与凭据 | `dreamina-canvas-cli-auth` / `dreamina-canvas-cli-auth` |
| 首次使用体检 | `dreamina-canvas-cli-setup` |

## 安装命令形态（官方指南 §2）

```bash
# macOS / Linux
curl -fsSL https://jimeng.jianying.com/canvas-cli/install.sh | bash

# Windows PowerShell
irm https://jimeng.jianying.com/canvas-cli/install.ps1 | iex

# Windows CMD
curl.exe -fsSLO https://jimeng.jianying.com/canvas-cli/install.bat && install.bat
```

- 三选一；装错 shell 的组合是常见失败源。
- 升级 = 重跑同一安装器（就地升级）。

## 验证命令形态

```bash
dreamina-canvas --help                    # 看到 auth/canvas/model/node/operation/resource
dreamina-canvas --format json version     # 结构化版本
dreamina-canvas --format json schema      # 命令契约
```

## 运行时真相来源

1. 安装器输出（来源与目标目录）。
2. live `--help` / `version` / `schema`。

文档与 live 输出冲突时，以 live 输出为准并标记 `NOT_VERIFIED`。
