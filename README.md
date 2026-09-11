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

This package includes **13 Dreamina skills** plus **13 in-progress Canvas skills** that target the `dreamina-canvas` CLI. Each skill is a self-contained `SKILL.md` file that AI agents load on-demand.

### Canvas Skill inventory (in progress)

| Layer | Skill | Invocation |
|-------|-------|------------|
| Foundation | `dreamina-canvas-cli` | explicit |
| Atomic | `dreamina-canvas-auth` | explicit |
| Atomic | `dreamina-canvas-discover-models` | explicit |
| Atomic | `dreamina-canvas-create` | explicit |
| Atomic | `dreamina-canvas-quote-and-run` | explicit |
| Atomic | `dreamina-canvas-resume-operation` | explicit |
| Atomic | `dreamina-canvas-download-assets` | explicit |
| Domain | `dreamina-canvas-generate-image` | explicit |
| Domain | `dreamina-canvas-generate-video` | explicit |
| Domain | `dreamina-canvas-generate-audio` | explicit |
| Domain | `dreamina-canvas-manage-timeline` | explicit |
| Orchestration | `dreamina-canvas-compose` | explicit |
| Orchestration | `dreamina-canvas-use` | implicit |

Canvas Skills consume the guide contract at `verification/dreamina-canvas-guide-contract.json` and rely on the installed CLI's `version`, `schema`, `model`, and `voice` output for runtime truth. They are not yet implemented; subsequent tasks create and validate every directory.

## 📦 Install

```bash
npx skills add full-aigc-skills/dreamina-skills
```

Or install specific skills: `npx skills add full-aigc-skills/dreamina-skills --skill <skill-name>`

## 🎯 Skills (13)

| Skill | Description |
|-------|-------------|
| `dreamina-cli` | Umbrella skill for CLI v1.4.18 contracts, runtime video-ratio discovery, OAuth login, session CRUD, task history, and routing to the four execution skills. |
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
