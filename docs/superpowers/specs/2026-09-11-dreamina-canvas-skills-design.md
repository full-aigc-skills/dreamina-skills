# Dreamina Canvas Skills Design

## Goal

Add a canonical, dependency-ordered Skill suite for the `dreamina-canvas` CLI. The suite exposes low-level CLI invariants before domain generation and high-level canvas composition, while reusing existing Dreamina prompt Skills instead of copying their guidance.

## Source contract

The initial contract comes from the user-provided Dreamina Octo CLI guide dated 2026-09-11. Runtime truth comes from the installed artifact's `version`, `schema`, `model`, and `voice` commands. The guide may seed offline fixtures, but must never become a hard-coded model catalog.

## Skill inventory and layers

### Layer 0 — CLI foundation

- `dreamina-canvas-cli`

### Layer 1 — atomic command/protocol Skills

- `dreamina-canvas-auth`
- `dreamina-canvas-discover-models`
- `dreamina-canvas-create`
- `dreamina-canvas-quote-and-run`
- `dreamina-canvas-resume-operation`
- `dreamina-canvas-download-assets`

### Layer 2 — media and timeline Skills

- `dreamina-canvas-generate-image`
- `dreamina-canvas-generate-video`
- `dreamina-canvas-generate-audio`
- `dreamina-canvas-manage-timeline`

### Layer 3 — high-level orchestration Skills

- `dreamina-canvas-compose`
- `dreamina-canvas-use`

Only `dreamina-canvas-use` is intended for implicit invocation. The other twelve Skills are explicit building blocks used directly by advanced users or selected by the orchestrator.

## Responsibility boundaries

- `dreamina-canvas-cli` owns global flags, JSON envelopes, stdout/stderr separation, exit-code routing, profiles, environments, schema discovery, identifiers, and retry invariants.
- Atomic Skills map one stable CLI command family or one indivisible safety protocol. `quote → confirm → run` remains together because splitting it would weaken the credit-approval boundary.
- Media Skills own Canvas node schemas and reference rules, not creative prompt methodology. They route prompt authoring to existing `dreamina-prompt-*` Skills when those are available.
- `compose` builds non-charging canvas structure and dependency order. It does not approve spend or assume that `node run` performs DAG scheduling.
- `use` selects the smallest applicable Skill chain and reports verified identifiers, costs, operation states, and downloaded artifacts.

## Non-negotiable invariants

- Saving a node never implies running it.
- Models, voices, ratios, resolutions, durations, and batch limits are discovered at runtime.
- Generation edits replace the complete generation block; metadata edits are sparse.
- `node:` and `res:` references are distinct and validated before mutation.
- Paid execution requires an authoritative quote and an action-time approval bounded by a credit ceiling or confirmation token.
- An empty or changed `submitId` must never be used for recovery.
- Exit code 20 resumes the same operation; it never authorizes resubmission.
- Tokens, cookies, signed URLs, and credit confirmation tokens are never persisted or logged.

## Delivery boundary

This repository is the Skill source of truth. The `partme-ai/codex-dreamina-canvas-plugin` repository packages a pinned source SHA and adds Codex plugin manifests, runtime adapter tests, marketplace metadata, and installation acceptance. It must not fork Skill content.

## Verification

- Every Skill gets its own RED/GREEN behavior scenario, quick validation, TRACE evaluation, and retrieval/application check.
- Repository inventory tests assert 26 total Skills: the existing 13 Dreamina Skills plus 13 Canvas Skills.
- Offline fixtures cover every public exit code and required action without installation, login, or paid generation.
- Live verification is read-only unless installation, authentication, or a paid canary is separately authorized.
- `verification/dreamina-canvas-command-coverage.json` maps every official
  `dreamina-canvas` command to one owning Skill and a verifiable evidence token.
- `verification/dreamina-cli-command-coverage.json` does the same for the
  classic `dreamina` CLI and records Prompt/OpenCLI supporting routes without
  confusing them with the local CLI execution owner.
