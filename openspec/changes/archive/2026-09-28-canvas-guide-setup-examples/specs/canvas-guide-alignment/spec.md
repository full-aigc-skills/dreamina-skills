## ADDED Requirements

### Requirement: First-use Canvas setup is discoverable
The package MUST provide `dreamina-setup` for users who request installation and initial readiness of `dreamina-canvas`. It MUST distinguish Canvas from the classic `dreamina` CLI and cover macOS/Linux, Windows PowerShell, and Windows CMD instructions. It MUST verify help, version, schema, and server-recognized account state, and handle a missing PATH without claiming readiness.

#### Scenario: User requests Canvas setup
- **WHEN** a first-time user asks an agent to install and prepare the Canvas CLI
- **THEN** the agent can select `dreamina-setup`, show the relevant installer and authorization boundary, and verify the installed CLI and account before reporting ready

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
