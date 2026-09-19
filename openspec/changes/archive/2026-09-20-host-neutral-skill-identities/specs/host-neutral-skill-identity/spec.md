## ADDED Requirements

### Requirement: Installable skills use host-neutral plugin identities

Dreamina skills SHALL use `dreamina-3d`, `blender-design`, and `maya-design` as public identities. They SHALL NOT use a host name as part of those public identities.

#### Scenario: Route a Blender preview

- **WHEN** Dreamina 3D receives a receipt from the current Blender plugin
- **THEN** it accepts `producer_plugin: blender-design`

#### Scenario: Discover a companion on any supported host

- **WHEN** an installed companion exposes a valid Codex, ZCode, or Kimi manifest
- **THEN** the probe discovers the same host-neutral plugin identity
