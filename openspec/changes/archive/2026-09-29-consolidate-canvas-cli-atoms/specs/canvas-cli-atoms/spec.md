## ADDED Requirements

### Requirement: Nine stable CLI entry skills
The package SHALL retain exactly nine dreamina-canvas-cli entry skills: the base skill and setup, auth, text2image, image2image, text2video, ref2video, text2voice and text2audio suffixes. Common operations SHALL live in references and examples rather than separate installable helper skills.

#### Scenario: Resolve an operation after consolidation
- **WHEN** a command owner is loaded from the coverage manifest
- **THEN** it resolves to an existing one of the nine CLI skills with locally reachable operation documentation

### Requirement: Portable operation documentation
Each CLI skill SHALL retain its own required resources after granular installation. References to another skill SHALL use its name and an installation instruction rather than sibling file paths. Mode-specific constraints and paid recovery boundaries SHALL survive the migration.

#### Scenario: Install one skill
- **WHEN** a single CLI skill is copied into an otherwise empty skills directory
- **THEN** the package resource checker succeeds without access to sibling resources

### Requirement: Explicit migration and evidence boundaries
The package SHALL publish old-to-new ownership mappings, preserve the frozen classic CLI skills, and distinguish historical generation evidence from verification of this refactor.

#### Scenario: Resume an existing submission
- **WHEN** the new skill handles an uncertain generation outcome
- **THEN** it queries the original submitId without silently creating a new paid submission
