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

