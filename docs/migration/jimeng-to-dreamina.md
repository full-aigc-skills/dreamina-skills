# `jimeng-skills` 到 `dreamina-skills` 迁移说明

本次迁移统一仓库、插件清单和可安装 Skill 标识。产品中文名“即梦”及官方域名
`jimeng.jianying.com` 保留；旧 Skill 标识不再作为可安装入口，避免重复触发。

| 旧 Skill 标识 | 新 Skill 标识 |
|---|---|
| `jimeng-cli-image2image` | `dreamina-cli-image2image` |
| `jimeng-cli-image2video` | `dreamina-cli-image2video` |
| `jimeng-cli-text2image` | `dreamina-cli-text2image` |
| `jimeng-cli-text2video` | `dreamina-cli-text2video` |
| `jimeng-opencli-image2image` | `dreamina-opencli-image2image` |
| `jimeng-opencli-image2video` | `dreamina-opencli-image2video` |
| `jimeng-opencli-text2image` | `dreamina-opencli-text2image` |
| `jimeng-opencli-text2video` | `dreamina-opencli-text2video` |
| `jimeng-prompt-image2image` | `dreamina-prompt-image2image` |
| `jimeng-prompt-image2video` | `dreamina-prompt-image2video` |
| `jimeng-prompt-text2image` | `dreamina-prompt-text2image` |
| `jimeng-prompt-text2video` | `dreamina-prompt-text2video` |

`dreamina-cli` 原本已使用目标名称，保持不变。仓库地址同步从
`full-aigc-skills/jimeng-skills` 迁移到 `full-aigc-skills/dreamina-skills`。

## 使用方迁移

```bash
npx skills add full-aigc-skills/dreamina-skills
```

已有脚本、Agent 配置或文档若固定引用旧 Skill 标识，应按上表替换；不提供旧标识别名。
Dreamina CLI 的参数能力必须通过当前 `dreamina <command> --help` 发现，版本基线见
[`dreamina-cli-v1.4.18-contract.md`](../../skills/dreamina-cli/references/dreamina-cli-v1.4.18-contract.md)。
