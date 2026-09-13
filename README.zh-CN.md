<div align="center">

# dreamina-skills

**Dreamina（即梦）AIGC 技能 — 文生图、图生图、文生视频、图生视频，覆盖 CLI、OpenCLI 与 Prompt 工作流**

[![GitHub](https://img.shields.io/badge/github-full--aigc--skills%2Fdreamina-skills-green.svg)](https://github.com/full-aigc-skills/dreamina-skills)
[![License](https://img.shields.io/badge/license-Apache%202.0-blue.svg)](LICENSE)
[![Agent Skills](https://img.shields.io/badge/Agent%20Skills-兼容-purple.svg)](https://agentskills.io)

[English](./README.md) | 简体中文

</div>

---

## 📖 简介

**dreamina-skills** 是一组 AI 编码智能体技能，属于 [Full AIGC Skills](https://github.com/full-aigc-skills) 生态。包含 **13 个 Dreamina 技能** 与 **13 个尚在创建中的 Canvas 技能**（面向 `dreamina-canvas` CLI）。

## 📦 安装

```bash
npx skills add full-aigc-skills/dreamina-skills
```

## 🎯 技能列表 (13)

| 技能 | 描述 |
|------|------|
| `dreamina-cli` | dreamina CLI v1.4.18 总览技能，覆盖安装更新、OAuth/headless 登录、账户检查、全部生成命令、查询下载、会话 CRUD、日志排障、运行时视频比例发现和子命令路由。 |
| `dreamina-cli-image2image` | 通过 `dreamina image2image` 执行图像编辑，覆盖模型、尺寸、批量、会话和异步结果规则。 |
| `dreamina-cli-image2video` | 在单图、首尾帧、故事板和多模态参考之间路由，并执行命令级比例约束。 |
| `dreamina-cli-text2image` | 通过 `dreamina text2image` 执行文生图，并校验模型与分辨率组合。 |
| `dreamina-cli-text2video` | 执行文生视频，覆盖 v1.4.18 比例、时长、分辨率与异步结果闭环。 |
| `dreamina-opencli-image2image` | 本地 Dreamina CLI 不可用时，指导通过 OpenCLI 浏览器命令完成图像编辑。 |
| `dreamina-opencli-image2video` | 本地 Dreamina CLI 不可用时，指导通过 OpenCLI 浏览器命令完成图生视频。 |
| `dreamina-opencli-text2image` | 通过 OpenCLI 浏览器命令执行普通会员文生图工作流。 |
| `dreamina-opencli-text2video` | 通过 OpenCLI 浏览器命令执行普通会员文生视频工作流。 |
| `dreamina-prompt-image2image` | 为元素、风格、背景、修复和多参考编辑编写精确的图生图提示词。 |
| `dreamina-prompt-image2video` | 为单图、首尾帧、多帧和多模态视频生成编写提示词。 |
| `dreamina-prompt-text2image` | 编写覆盖场景、风格、色彩、构图和质量约束的结构化文生图提示词。 |
| `dreamina-prompt-text2video` | 编写覆盖运动、镜头、时间、场景和评估规则的结构化文生视频提示词。 |

### Canvas 技能清单（建设中）

| 层 | 技能 | 调用方式 |
|----|------|----------|
| 基础 | `dreamina-canvas-cli` | 显式 |
| 原子 | `dreamina-canvas-auth` | 显式 |
| 原子 | `dreamina-canvas-discover-models` | 显式 |
| 原子 | `dreamina-canvas-create` | 显式 |
| 原子 | `dreamina-canvas-quote-and-run` | 显式 |
| 原子 | `dreamina-canvas-resume-operation` | 显式 |
| 原子 | `dreamina-canvas-download-assets` | 显式 |
| 领域 | `dreamina-canvas-generate-image` | 显式 |
| 领域 | `dreamina-canvas-generate-video` | 显式 |
| 领域 | `dreamina-canvas-generate-audio` | 显式 |
| 领域 | `dreamina-canvas-manage-timeline` | 显式 |
| 编排 | `dreamina-canvas-compose` | 显式 |
| 编排 | `dreamina-canvas-use` | 隐式 |

Canvas 技能遵守 `verification/dreamina-canvas-guide-contract.json` 中的引导契约，并以安装版 CLI 的 `version`、`schema`、`model`、`voice` 输出为运行时真相；尚未实现，后续 Task 会逐个创建并验证目录。

## 🤖 支持的智能体

适用于 [Claude Code](https://code.claude.com)、[Codex](https://developers.openai.com/codex)、[Cursor](https://cursor.com)、[OpenCode](https://opencode.ai)、[Gemini CLI](https://geminicli.com)、[GitHub Copilot](https://github.com/features/copilot)、[Windsurf](https://codeium.com/windsurf) 及 [70+ 其他](https://agentskills.io/clients)。

### Claude Code 安装

**方式一：npx skills CLI（推荐）**

```bash
npx skills add full-aigc-skills/dreamina-skills
```

**方式二：手动安装**

```bash
git clone https://github.com/full-aigc-skills/dreamina-skills.git
cp -r dreamina-skills/skills/* .claude/skills/
```

## 📄 License

Apache 2.0
