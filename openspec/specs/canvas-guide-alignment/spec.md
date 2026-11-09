# canvas-guide-alignment Specification

## Purpose
Keep first-use Dreamina Canvas setup and common CLI examples discoverable, accurate against the installed command contract, and safe across authorization and asynchronous recovery boundaries.

## Requirements

### Requirement: First-use Canvas setup is discoverable
The package MUST provide dreamina-canvas-cli-setup for installation and initial readiness of dreamina-canvas, replacing dreamina-setup through a documented migration. It MUST distinguish Canvas from the classic CLI, cover macOS/Linux, Windows PowerShell and CMD, verify help/version/schema and delegate account authorization to dreamina-canvas-cli-auth without claiming readiness from local status alone.

#### Scenario: User requests Canvas setup
- **WHEN** a first-time user requests Canvas installation
- **THEN** the agent selects dreamina-canvas-cli-setup, verifies the binary, and hands authorized login to dreamina-canvas-cli-auth

### Requirement: Guide examples are owned by the relevant skills
Each common command family in the supplied guide MUST have a concrete example in the corresponding Canvas skill, including model and voice discovery, canvas/resource preparation, image/video/audio generation, status/recovery/download, and the other node operations. Examples MUST use live-discovered parameter placeholders and MUST distinguish saving a draft from a paid run.

#### Scenario: User requests a guide workflow
- **WHEN** an agent reads the relevant skill's example
- **THEN** it finds the command shape, required prior discovery or approval, expected identifiers, and a safe continuation after an asynchronous result

### Requirement: Documented commands follow current CLI contract
The examples MUST prefer the currently installed CLI's `schema` and `--help` over stale guide syntax. The package MUST include a regression check for the new setup skill and the example inventory.

#### Scenario: Guide and CLI differ
- **WHEN** the guide names a command differently from live schema
- **THEN** the skill shows the current CLI form and identifies the guide form as version-dependent instead of presenting it as universally runnable

### Requirement: New Canvas capabilities route to their owning skill

当用户请求团队空间、样片、导演台、后处理或工作流批量生成时，Canvas 编排技能 MUST 指向对应操作参考。工作流 MUST 使用当前 CLI 声明的报价、批准、运行、恢复和模板实例化契约。执行前 MUST 根据当前 CLI `version`、`schema` 和命令 `--help` 核实能力与参数；未声明的能力 MUST 明确停止而不能猜测命令。

#### Scenario: Installed CLI is older than the requested capability

- **WHEN** 用户请求 1.3.0 的工作流模板复用，而本机 CLI 仅显示 1.2.0 且 schema 没有该命令
- **THEN** 技能报告版本与缺失能力，不拼造命令或将普通批量 `node run` 冒充工作流模板。

#### Scenario: A post-processing operation may consume credits

- **WHEN** 用户要求样片转正、超清、抠图或补帧
- **THEN** 技能先核对当前命令契约与实时报价，获得该操作的授权后才提交，并复用原 submitId 查询结果。
