## ADDED Requirements

### Requirement: Honor explicit handoff version ranges
validate_artifact SHALL use explicit version_ranges for producer compatibility and diagnostics. None SHALL preserve default ranges; an empty map SHALL reject every producer. Other artifact checks SHALL remain active.

#### Scenario: Explicit range override
- **WHEN** a caller supplies a version range
- **THEN** in-range artifacts are accepted and out-of-range artifacts are rejected using the supplied range
