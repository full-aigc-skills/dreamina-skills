## MODIFIED Requirements

### Requirement: First-use Canvas setup is discoverable
The package MUST provide dreamina-canvas-cli-setup for installation and initial readiness of dreamina-canvas, replacing dreamina-setup through a documented migration. It MUST distinguish Canvas from the classic CLI, cover macOS/Linux, Windows PowerShell and CMD, verify help/version/schema and delegate account authorization to dreamina-canvas-cli-auth without claiming readiness from local status alone.

#### Scenario: User requests Canvas setup
- **WHEN** a first-time user requests Canvas installation
- **THEN** the agent selects dreamina-canvas-cli-setup, verifies the binary, and hands authorized login to dreamina-canvas-cli-auth
