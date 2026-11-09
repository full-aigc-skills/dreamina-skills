## ADDED Requirements

### Requirement: Documented node deletion transaction

The base CLI skill SHALL document the `node delete` transaction for public
releases that declare it: a summary/execute step gated by a short-lived
`deleteConfirmationToken` minted by `node delete confirm`, a stable
`--update-id` reused across confirm, execute and retry, and a read-only
`node delete status` reconciliation that never mints credentials. The
documentation SHALL state that `--yes` cannot replace the deletion token,
that groups are unsupported, and that batch `--node-id` input is
deduplicated in order within the declared bound.

#### Scenario: Approve then delete nodes

- **WHEN** a caller runs `node delete` for a node batch and the CLI requires
  confirmation
- **THEN** the skill routes through `node delete confirm` with the same
  `--update-id`, executes with the minted `--delete-token`, and reconciles
  uncertain outcomes via `node delete status` instead of re-submitting

### Requirement: Documented node position placement

The CLI skill references SHALL document the paired `--x` / `--y` placement
flags for typed node create/edit where the live schema declares them,
including the grouping rule (parent-local coordinates inside a group) and
the pairing constraint, without encouraging callers to place nodes when the
user has no layout requirement.

#### Scenario: Explicit layout request

- **WHEN** a user asks to move or lay out nodes on the canvas
- **THEN** the skill uses the paired position flags declared by the current
  schema and keeps positions parent-local for grouped nodes

## MODIFIED Requirements

### Requirement: Nine stable CLI entry skills

The package SHALL retain exactly nine dreamina-canvas-cli entry skills: the
base skill and setup, auth, text2image, image2image, text2video, ref2video,
text2voice and text2audio suffixes. Common operations — including node
deletion and placement — SHALL live in references and examples rather than
separate installable helper skills. Audio scenario capability
(`text-reading`, `omni-dubbing`) SHALL be owned by the `text2voice` entry
together with the shared audio-node references.

#### Scenario: Resolve an operation after consolidation

- **WHEN** a command owner is loaded from the coverage manifest
- **THEN** it resolves to an existing one of the nine CLI skills with
  locally reachable operation documentation

#### Scenario: Route a dubbing request

- **WHEN** a user asks for omni-dubbing with a chosen voice or reference
  audio material
- **THEN** the request resolves to the `text2voice` entry plus the shared
  audio-node references, constructs `--mode tts` with `--scenario
  omni-dubbing` per the live schema, and never hard-codes a catalog model
  or voice name
