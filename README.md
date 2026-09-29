<div align="center">

# dreamina-skills

**Dreamina（即梦）AIGC skills — text-to-image, image-to-image, text-to-video, and image-to-video via CLI, OpenCLI, and Prompt workflows**

[![GitHub](https://img.shields.io/badge/github-full--aigc--skills%2Fdreamina-skills-green.svg)](https://github.com/full-aigc-skills/dreamina-skills)
[![License](https://img.shields.io/badge/license-Apache%202.0-blue.svg)](LICENSE)
[![Agent Skills](https://img.shields.io/badge/Agent%20Skills-Compatible-purple.svg)](https://agentskills.io)

English | [简体中文](./README.zh-CN.md)

[Introduction](#-introduction) · [Install](#-install) · [Skills](#-skills) · [Supported Agents](#-supported-agents) · [Ecosystem](#-ecosystem)

</div>

---

## 📖 Introduction

**dreamina-skills** is a curated collection of Agent Skills for AI coding agents, part of the [Full AIGC Skills](https://github.com/full-aigc-skills) ecosystem.

This package includes **33 skills**: 17 Design/legacy skills, 10 Canvas skills (nine CLI entrypoints and one orchestrator), and six Dreamina 3D skills. Each skill loads its operation references and scenarios on demand.

Official command ownership is enforced by
[`dreamina-canvas-command-coverage.json`](verification/dreamina-canvas-command-coverage.json)
and [`dreamina-cli-command-coverage.json`](verification/dreamina-cli-command-coverage.json).
Canvas Skills are packaged by `full-aigc-plugins/dreamina-canvas-plugin`;
classic CLI, OpenCLI, and Prompt Skills are packaged by
`full-aigc-plugins/dreamina-design-plugin`.

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

## 📦 Install

```bash
npx skills add full-aigc-skills/dreamina-skills
```

Or install specific skills: `npx skills add full-aigc-skills/dreamina-skills --skill <skill-name>`

## 🎯 Design CLI, OpenCLI and Prompt Skills (13)

| Skill | Description |
|-------|-------------|
| `dreamina-cli` | Umbrella skill covering installation, updates, CLI v1.4.18 contracts, OAuth/headless login, account checks, all generation commands, session CRUD, task query/download, logs, troubleshooting, and routing to the four execution skills. |
| `dreamina-cli-image2image` | Run image-guided editing through `dreamina image2image`, including model, size, batch, session, and async-result rules. |
| `dreamina-cli-image2video` | Route and run image-, frame-, storyboard-, or multimodal-reference video tasks with command-specific ratio constraints. |
| `dreamina-cli-text2image` | Run prompt-only image generation through `dreamina text2image` with validated model and resolution combinations. |
| `dreamina-cli-text2video` | Run prompt-only video generation with v1.4.18 ratio, duration, resolution, and async-result handling. |
| `dreamina-opencli-image2image` | Guide browser-command fallbacks for image editing when the local Dreamina CLI is unavailable. |
| `dreamina-opencli-image2video` | Guide browser-command fallbacks for image-to-video workflows when the local Dreamina CLI is unavailable. |
| `dreamina-opencli-text2image` | Run standard-member text-to-image workflows through OpenCLI browser commands. |
| `dreamina-opencli-text2video` | Run standard-member text-to-video workflows through OpenCLI browser commands. |
| `dreamina-prompt-image2image` | Author precise image-edit prompts for element, style, background, restoration, and multi-reference changes. |
| `dreamina-prompt-image2video` | Author prompts for single-image, first/last-frame, multi-frame, and multimodal video generation. |
| `dreamina-prompt-text2image` | Author structured Dreamina text-to-image prompts with scene, style, color, composition, and quality guidance. |
| `dreamina-prompt-text2video` | Author structured Dreamina text-to-video prompts with motion, camera, timing, scene, and evaluation guidance. |

The other four Design skills are `dreamina-design-use`, `dreamina-shot-annotator`, `dreamina-video-evaluator`, and `dreamina-video-production`.

## 🤖 Supported Agents

Works with [Claude Code](https://code.claude.com), [Codex](https://developers.openai.com/codex), [Cursor](https://cursor.com), [OpenCode](https://opencode.ai), [Gemini CLI](https://geminicli.com), [GitHub Copilot](https://github.com/features/copilot), [Windsurf](https://codeium.com/windsurf), and [70+ others](https://agentskills.io/clients).

### Claude Code Installation

**Option 1: npx skills CLI (Recommended)**

```bash
npx skills add full-aigc-skills/dreamina-skills
```

**Option 2: Manual Installation**

```bash
git clone https://github.com/full-aigc-skills/dreamina-skills.git
cp -r dreamina-skills/skills/* .claude/skills/
```

For more details, see the [Claude Code Skills Guide](https://code.claude.com/docs/en/skills) and [Agent Skills Spec](https://agentskills.io/).

## 🌐 Ecosystem

| Resource | Link |
|----------|------|
| **Full AIGC Skills** | [github.com/full-aigc-skills](https://github.com/full-aigc-skills) |
| **Agent Skills Spec** | [agentskills.io](https://agentskills.io) |
| **Skills CLI** | [github.com/vercel-labs/skills](https://github.com/vercel-labs/skills) |

## 📄 License

Apache 2.0 — see [LICENSE](LICENSE).
