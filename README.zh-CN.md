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

**dreamina-skills** 是一组 AI 编码智能体技能，属于 [Full AIGC Skills](https://github.com/full-aigc-skills) 生态。包含 **33 个技能**：17 个 Design/历史兼容技能、10 个 Canvas 技能（9 个 CLI 原子入口 + 1 个编排入口）、6 个 Dreamina 3D 编排技能。

官方命令归属由
[`dreamina-canvas-command-coverage.json`](verification/dreamina-canvas-command-coverage.json)
和 [`dreamina-cli-command-coverage.json`](verification/dreamina-cli-command-coverage.json)
持续校验。Canvas Skill 由 `full-aigc-plugins/dreamina-canvas-plugin` 打包；传统
CLI、OpenCLI 与 Prompt Skill 由 `full-aigc-plugins/dreamina-design-plugin` 打包。

## 📦 安装

```bash
npx skills add full-aigc-skills/dreamina-skills
```

## 🎯 Design CLI、OpenCLI 与 Prompt 技能 (13)

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

其余 4 个 Design 技能为 `dreamina-design-use`、`dreamina-shot-annotator`、`dreamina-video-evaluator` 和 `dreamina-video-production`。

### Canvas 原子技能

九个 CLI 技能保持独立；模型、画布、素材、报价运行、恢复和时间轴是总技能内部的标准操作，不再发布同名辅助技能。文生图等场景见各自 examples/。

| 技能 | 职责 |
|---|---|
| `dreamina-canvas-cli` | 公共契约、模型音色、画布资源、节点共享机制、报价运行、恢复与校验 |
| `dreamina-canvas-cli-setup` | 安装、升级与环境检查 |
| `dreamina-canvas-cli-auth` | 登录、授权等待、账户、刷新与退出 |
| `dreamina-canvas-cli-text2image` | t2i 文生图 |
| `dreamina-canvas-cli-image2image` | i2i 图生图与独立定价的图片放大 |
| `dreamina-canvas-cli-text2video` | t2v 文生视频 |
| `dreamina-canvas-cli-ref2video` | m2v 与 first_last_frame 参考视频 |
| `dreamina-canvas-cli-text2voice` | tts 语音 |
| `dreamina-canvas-cli-text2audio` | music 音乐 |
| `dreamina-canvas-use` | 唯一隐式 Canvas 编排入口 |

首次安装使用 `dreamina-canvas-cli-setup`。每个操作按输入、动作、副作用、输出、恢复和验收组织，按需读取 references/。跨技能按名称安装，不依赖相邻目录。

旧的五个 `dreamina-cli*` 技能冻结，仅服务明确的旧版请求。辅助技能迁移表见 [Canvas 迁移说明](docs/canvas-atomic-migration.md)。消费者更新前需检查固定路径，当前本地整理不代表已发布或真实生成验收。

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
