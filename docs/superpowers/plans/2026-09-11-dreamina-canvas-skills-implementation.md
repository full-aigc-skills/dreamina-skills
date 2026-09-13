# Dreamina Canvas Skills Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Add thirteen dependency-ordered `dreamina-canvas-*` Skills, beginning with the CLI contract and atomic command families and ending with canvas composition and the user-facing orchestrator.

**Architecture:** `dreamina-canvas-cli` is the single command/error/idempotency authority. Atomic Skills depend on it; media and timeline Skills combine atomic contracts without copying prompt guidance; `compose` and `use` are implemented last. Existing `dreamina-prompt-*` Skills remain the creative-prompt authority.

**Tech Stack:** Agent Skills Markdown, `agents/openai.yaml`, Python 3 `unittest`, JSON fixtures, installed `dreamina-canvas` CLI for separately authorized read-only verification.

**Spec:** `docs/superpowers/specs/2026-09-11-dreamina-canvas-skills-design.md`

## Global Constraints

- The final repository inventory is exactly 26 Skills: 13 existing Dreamina Skills plus 13 new Canvas Skills.
- Only `dreamina-canvas-use` allows implicit invocation; the other twelve Canvas Skills set `policy.allow_implicit_invocation: false`.
- The initial offline contract is derived from the 2026-09-11 user-provided Dreamina Octo CLI guide; live `version`, `schema`, `model`, and `voice` output overrides prose.
- Never hard-code model names, voice names, ratios, resolutions, durations, or batch limits as timeless facts.
- Saving is non-charging. Quote, confirm, and run are separate, and paid execution requires action-time approval.
- Exit code 20 resumes the same `submitId`; it never authorizes a new submission.
- Do not install the CLI, authenticate, or run a paid canary without separate authorization at that action boundary.
- Do not persist or print OAuth credentials, cookies, signed URLs, or credit confirmation tokens.
- Each task follows RED → GREEN → focused regression → quick validation → TRACE → commit.

---

### Task 1: Establish the Canvas suite contract and inventory gate

**Files:**
- Create: `verification/dreamina-canvas-guide-contract.json`
- Create: `tests/test_canvas_skill_inventory.py`
- Create: `tests/fixtures/dreamina_canvas/schema-root.json`
- Modify: `.claude-plugin/plugin.json`
- Modify: `README.md`
- Modify: `README.zh-CN.md`

**Interfaces:**
- Consumes: the 2026-09-11 Dreamina Octo CLI guide and the existing 13-Skill inventory.
- Produces: `CANVAS_SKILLS`, a 13-name canonical inventory reused by later tests; an offline command/exit-code fixture with no model catalog.

- [x] **Step 1: Write the failing inventory test**

```python
CANVAS_SKILLS = {
    "dreamina-canvas-cli", "dreamina-canvas-auth",
    "dreamina-canvas-discover-models", "dreamina-canvas-create",
    "dreamina-canvas-compose", "dreamina-canvas-generate-image",
    "dreamina-canvas-generate-video", "dreamina-canvas-generate-audio",
    "dreamina-canvas-manage-timeline", "dreamina-canvas-quote-and-run",
    "dreamina-canvas-resume-operation", "dreamina-canvas-download-assets",
    "dreamina-canvas-use",
}

def test_canvas_skill_inventory_is_complete():
    actual = {p.name for p in (ROOT / "skills").iterdir() if p.name.startswith("dreamina-canvas-")}
    assert actual == CANVAS_SKILLS
```

- [x] **Step 2: Run the test and preserve the RED result**

Run: `python3 -m unittest tests/test_canvas_skill_inventory.py -v`

Expected: FAIL because none of the thirteen Canvas Skill directories exist.

- [x] **Step 3: Add the guide contract fixture and inventory metadata**

Record command families `auth`, `model`, `voice`, `canvas`, `node`, `operation`, `resource`, `schema`, and `version`; exit codes `0,1,2,10,11,12,13,20,21,22`; and required actions `none,login,confirm,retry,resume,upgrade,human_intervention,contact_support`. Do not include concrete model or voice values.

- [x] **Step 4: Add the thirteen target paths to package metadata and READMEs**

The manifest and bilingual tables must state the layer and invocation policy for every new Skill. Do not claim implementation is complete until later tasks create and validate every directory.

- [x] **Step 5: Run fixture validation and commit the RED baseline**

Run: `python3 -m json.tool verification/dreamina-canvas-guide-contract.json`

Commit:

```bash
git add verification tests .claude-plugin README.md README.zh-CN.md
git commit -m "test(canvas): define Skill inventory and CLI guide contract"
```

### Task 2: Implement `dreamina-canvas-cli` as the foundation Skill

**Files:**
- Create: `skills/dreamina-canvas-cli/SKILL.md`
- Create: `skills/dreamina-canvas-cli/agents/openai.yaml`
- Create: `skills/dreamina-canvas-cli/references/cli-contract.md`
- Create: `skills/dreamina-canvas-cli/references/error-routing.md`
- Create: `tests/scenarios/dreamina-canvas-cli.json`
- Modify: `tests/test_canvas_skill_inventory.py`

**Interfaces:**
- Consumes: `verification/dreamina-canvas-guide-contract.json`.
- Produces: the shared rules for argv construction, `--format json`, stdout/stderr separation, profiles/environments, ID persistence, exit-code routing, and runtime schema discovery.

- [x] **Step 1: Add failing foundation assertions**

```python
def test_cli_skill_owns_cross_cutting_invariants():
    text = skill_text("dreamina-canvas-cli")
    for token in ("--format json", "requiredAction", "submitId", "exit code 20", "stdout", "stderr"):
        assert token in text
```

- [x] **Step 2: Verify RED**

Run: `python3 -m unittest tests.test_canvas_skill_inventory.CanvasSkillInventoryTests.test_cli_skill_owns_cross_cutting_invariants -v`

Expected: FAIL because `skills/dreamina-canvas-cli/SKILL.md` is missing.

- [x] **Step 3: Write the minimal foundation Skill**

The Skill must require `dreamina-canvas version` and the relevant `schema "<command path>"` before command construction; classify exit codes without parsing localized messages; preserve non-empty lowercase UUID `projectId`/`submitId`; and stop before install, login, or paid execution unless separately authorized.

- [x] **Step 4: Add explicit-only UI policy**

```yaml
interface:
  display_name: "Dreamina Canvas CLI"
  short_description: "Use the Dreamina Canvas CLI contract safely"
policy:
  allow_implicit_invocation: false
```

- [x] **Step 5: Validate behavior and quality**

Run:

```bash
python3 -m unittest tests/test_canvas_skill_inventory.py -v
/Library/Frameworks/Python.framework/Versions/3.13/bin/python3 /Users/wandl/.codex/skills/.system/skill-creator/scripts/quick_validate.py skills/dreamina-canvas-cli
```

Run strict TRACE and the scenario asserting that exit 20 yields “resume the same operation” rather than a new `node run` command.

- [x] **Step 6: Commit**

```bash
git add skills/dreamina-canvas-cli tests
git commit -m "feat(canvas): add CLI foundation Skill"
```

### Task 3: Implement `dreamina-canvas-auth`

**Files:**
- Create: `skills/dreamina-canvas-auth/SKILL.md`
- Create: `skills/dreamina-canvas-auth/agents/openai.yaml`
- Create: `skills/dreamina-canvas-auth/references/auth-state.md`
- Create: `tests/scenarios/dreamina-canvas-auth.json`
- Modify: `tests/test_canvas_skill_inventory.py`

**Interfaces:**
- Consumes: `dreamina-canvas-cli` error and profile rules.
- Produces: routes for `auth login`, `wait`, `status`, `account`, `refresh`, and `logout` without exposing credentials.

- [x] **Step 1: Write the failing auth boundary test**

```python
def test_auth_distinguishes_local_and_server_identity():
    text = skill_text("dreamina-canvas-auth")
    assert "auth status" in text and "auth account" in text
    assert "local" in text.lower() and "server" in text.lower()
    assert "token" in text and "不得" in text
```

- [x] **Step 2: Verify RED**

Run the single test and expect missing-Skill failure.

- [x] **Step 3: Implement auth flows**

Document TTY blocking login, non-TTY challenge recovery through `auth wait --device-code`, post-login `auth account` verification, profile isolation, and exit-code 11 recovery using the same original operation identity.

- [x] **Step 4: Validate and commit**

Run the inventory test, quick validator, strict TRACE, and scenarios for local-valid/server-revoked credentials and non-TTY login recovery.

```bash
git add skills/dreamina-canvas-auth tests
git commit -m "feat(canvas): add authentication Skill"
```

### Task 4: Implement `dreamina-canvas-discover-models`

**Files:**
- Create: `skills/dreamina-canvas-discover-models/SKILL.md`
- Create: `skills/dreamina-canvas-discover-models/agents/openai.yaml`
- Create: `skills/dreamina-canvas-discover-models/references/capability-discovery.md`
- Create: `tests/scenarios/dreamina-canvas-discover-models.json`
- Modify: `tests/test_canvas_skill_inventory.py`

**Interfaces:**
- Consumes: `dreamina-canvas-cli` runtime schema rules.
- Produces: model, voice, ratio, resolution, duration, input-specification, VIP, and maximum-batch discovery results for media Skills.

- [x] **Step 1: Write the failing no-hard-coded-catalog test**

```python
def test_discovery_uses_runtime_catalogs():
    text = skill_text("dreamina-canvas-discover-models")
    for command in ("model search", "--detail full", "voice list", "schema"):
        assert command in text
    assert "不要硬编码" in text
```

- [x] **Step 2: Verify RED, then implement runtime discovery**

Require full-detail model lookup before generation, pagination for voices, exact model lookup when a name is chosen, and explicit propagation of server constraints. Explain that account membership and model `isVip` metadata answer different questions.

- [x] **Step 3: Validate and commit**

Run quick validation, TRACE, and scenarios that reject a remembered model value absent from the current discovery payload.

```bash
git add skills/dreamina-canvas-discover-models tests
git commit -m "feat(canvas): add runtime capability discovery Skill"
```

### Task 5: Implement `dreamina-canvas-create`

**Files:**
- Create: `skills/dreamina-canvas-create/SKILL.md`
- Create: `skills/dreamina-canvas-create/agents/openai.yaml`
- Create: `skills/dreamina-canvas-create/references/canvas-context.md`
- Create: `tests/scenarios/dreamina-canvas-create.json`
- Modify: `tests/test_canvas_skill_inventory.py`

**Interfaces:**
- Consumes: foundation ID/profile/environment rules.
- Produces: an idempotently created or selected `projectId` and rules for safe current-canvas context use.

- [x] **Step 1: Write the failing idempotency test**

```python
def test_create_reuses_explicit_project_id_for_cross_process_retry():
    text = skill_text("dreamina-canvas-create")
    assert "canvas create" in text and "--project-id" in text
    assert "并发" in text and "--use" in text
```

- [x] **Step 2: Verify RED, then implement create/list/select behavior**

Require a caller-persisted lowercase UUID for cross-process retry, permit `--use` only for a single-user sequential flow, and require explicit `--project-id` in concurrent automation.

- [x] **Step 3: Validate and commit**

```bash
git add skills/dreamina-canvas-create tests
git commit -m "feat(canvas): add canvas creation Skill"
```

### Task 6: Implement the quote-confirm-run safety transaction

**Files:**
- Create: `skills/dreamina-canvas-quote-and-run/SKILL.md`
- Create: `skills/dreamina-canvas-quote-and-run/agents/openai.yaml`
- Create: `skills/dreamina-canvas-quote-and-run/references/credit-approval.md`
- Create: `tests/scenarios/dreamina-canvas-quote-and-run.json`
- Modify: `tests/test_canvas_skill_inventory.py`

**Interfaces:**
- Consumes: saved node IDs, current project ID, foundation error routing, and an explicit user decision.
- Produces: quote details, approved ceiling, per-item submission identities, and a no-resubmission recovery handoff.

- [x] **Step 1: Write the failing paid-action guard test**

```python
def test_paid_run_requires_authoritative_quote_and_action_time_approval():
    text = skill_text("dreamina-canvas-quote-and-run")
    assert text.index("node quote") < text.index("node confirm") < text.index("node run")
    assert "credit-ceiling" in text and "partialData.items" in text
    assert "--yes" in text and "默认" not in approval_paragraph(text)
```

- [x] **Step 2: Verify RED, then implement the transaction**

Treat exit 10 as a non-charging pause, reject `confirmable=false`, preserve ordered per-item IDs, keep the credit token only in memory, and re-quote the latest draft at run time. Never infer that an absent `minimumCreditCeiling` means zero.

- [x] **Step 3: Validate and commit**

Run scenarios for ceiling too low, modified draft below/above ceiling, token scope mismatch, mixed batch rejection, and unknown item state.

```bash
git add skills/dreamina-canvas-quote-and-run tests
git commit -m "feat(canvas): add quote and run safety Skill"
```

### Task 7: Implement operation recovery

**Files:**
- Create: `skills/dreamina-canvas-resume-operation/SKILL.md`
- Create: `skills/dreamina-canvas-resume-operation/agents/openai.yaml`
- Create: `skills/dreamina-canvas-resume-operation/references/recovery-state-machine.md`
- Create: `tests/scenarios/dreamina-canvas-resume-operation.json`
- Modify: `tests/test_canvas_skill_inventory.py`

**Interfaces:**
- Consumes: non-empty `projectId` and `submitId`, exit code, `requiredAction`, `submission.state`, and `submission.resubmittable`.
- Produces: terminal success/failure, continued wait, or human-review outcome without automatic resubmission.

- [x] **Step 1: Write the failing recovery invariant test**

```python
def test_recovery_never_changes_submit_id():
    text = skill_text("dreamina-canvas-resume-operation")
    assert "operation status" in text and "operation wait" in text
    assert "resubmittable" in text and "不要重新提交" in text
```

- [x] **Step 2: Verify RED, then implement the state machine**

Map `in_progress` and `completed` to continued observation, treat a missing submission fact conservatively as accepted, and route `absent + resubmittable=true` to human reconciliation rather than automatic `node run`.

- [x] **Step 3: Validate and commit**

```bash
git add skills/dreamina-canvas-resume-operation tests
git commit -m "feat(canvas): add resumable operation Skill"
```

### Task 8: Implement verified asset downloads

**Files:**
- Create: `skills/dreamina-canvas-download-assets/SKILL.md`
- Create: `skills/dreamina-canvas-download-assets/agents/openai.yaml`
- Create: `skills/dreamina-canvas-download-assets/references/artifact-verification.md`
- Create: `tests/scenarios/dreamina-canvas-download-assets.json`
- Modify: `tests/test_canvas_skill_inventory.py`

**Interfaces:**
- Consumes: successful node/resource identity and a user-approved output directory.
- Produces: canonical local path, byte count, SHA-256, media metadata, and source `resourceId`.

- [x] **Step 1: Write the failing artifact-evidence test**

```python
def test_download_requires_resource_fact_and_receipt():
    text = skill_text("dreamina-canvas-download-assets")
    for token in ("resource get", "resource download", "SHA-256", "resourceId"):
        assert token in text
```

- [x] **Step 2: Verify RED, then implement safe download behavior**

Require resource readiness before download, constrain output to the approved directory, trust only the final atomic-write response, and avoid persisting signed URLs or storage-provider identifiers.

- [x] **Step 3: Validate and commit**

```bash
git add skills/dreamina-canvas-download-assets tests
git commit -m "feat(canvas): add verified asset download Skill"
```

### Task 9: Implement image generation and editing

**Files:**
- Create: `skills/dreamina-canvas-generate-image/SKILL.md`
- Create: `skills/dreamina-canvas-generate-image/agents/openai.yaml`
- Create: `skills/dreamina-canvas-generate-image/references/image-node-contract.md`
- Create: `tests/scenarios/dreamina-canvas-generate-image.json`
- Modify: `tests/test_canvas_skill_inventory.py`

**Interfaces:**
- Consumes: discovered image-model contract, ordered references, `dreamina-prompt-text2image` or `dreamina-prompt-image2image`, and optional quote/run handoff.
- Produces: a saved image node and mutation version; when separately approved, a stable submission handoff.

- [x] **Step 1: Write failing image-mode/reference tests**

```python
def test_image_skill_separates_t2i_and_i2i_references():
    text = skill_text("dreamina-canvas-generate-image")
    assert "--mode t2i" in text and "--mode i2i" in text
    assert "node:" in text and "res:" in text
    assert "完整替换" in text and "--clear-generation" in text
```

- [x] **Step 2: Verify RED, then implement draft-first image workflows**

For generation edits, require the complete new prompt and ordered reference set. For metadata-only edits, omit all generation flags. Default to saving without `--run`; route paid execution through `dreamina-canvas-quote-and-run`.

- [x] **Step 3: Validate and commit**

Run t2i text-reference, i2i node/resource-reference, metadata-only edit, cleared generation, and out-of-catalog parameter scenarios.

```bash
git add skills/dreamina-canvas-generate-image tests
git commit -m "feat(canvas): add image node Skill"
```

### Task 10: Implement video generation

**Files:**
- Create: `skills/dreamina-canvas-generate-video/SKILL.md`
- Create: `skills/dreamina-canvas-generate-video/agents/openai.yaml`
- Create: `skills/dreamina-canvas-generate-video/references/video-node-contract.md`
- Create: `tests/scenarios/dreamina-canvas-generate-video.json`
- Modify: `tests/test_canvas_skill_inventory.py`

**Interfaces:**
- Consumes: discovered video contract, ordered references, existing Dreamina video prompt Skills, and quote/recovery protocols.
- Produces: saved `t2v`, `first_last_frame`, or `m2v` node plus optional approved submission handoff.

- [x] **Step 1: Write the failing video-mode test**

```python
def test_video_skill_uses_only_public_canvas_modes():
    text = skill_text("dreamina-canvas-generate-video")
    for mode in ("t2v", "first_last_frame", "m2v"):
        assert mode in text
    assert "没有 `i2v`" in text
```

- [x] **Step 2: Verify RED, then implement mode routing**

Require one or two proportion-compatible frame references for `first_last_frame`; use `m2v` for image/video/Element guidance; preserve user-requested ratios only when the discovered model contract permits them.

- [x] **Step 3: Validate and commit**

```bash
git add skills/dreamina-canvas-generate-video tests
git commit -m "feat(canvas): add video node Skill"
```

### Task 11: Implement audio generation

**Files:**
- Create: `skills/dreamina-canvas-generate-audio/SKILL.md`
- Create: `skills/dreamina-canvas-generate-audio/agents/openai.yaml`
- Create: `skills/dreamina-canvas-generate-audio/references/audio-node-contract.md`
- Create: `tests/scenarios/dreamina-canvas-generate-audio.json`
- Modify: `tests/test_canvas_skill_inventory.py`

**Interfaces:**
- Consumes: voice/model discovery and quote/recovery protocols.
- Produces: one saved TTS or music node and optional approved submission identity.

- [x] **Step 1: Write failing TTS/music exclusivity tests**

```python
def test_audio_skill_enforces_mode_specific_fields():
    text = skill_text("dreamina-canvas-generate-audio")
    assert "tts" in text and "--voice-name" in text
    assert "music" in text and "--model" in text
    assert "不接受 `--count`" in text
```

- [x] **Step 2: Verify RED, then implement audio rules**

Require a discovered voice and forbid model for TTS; require a discovered audio model and positive duration for music; forbid implicit/default music-model assumptions.

- [x] **Step 3: Validate and commit**

```bash
git add skills/dreamina-canvas-generate-audio tests
git commit -m "feat(canvas): add audio node Skill"
```

### Task 12: Implement timeline management

**Files:**
- Create: `skills/dreamina-canvas-manage-timeline/SKILL.md`
- Create: `skills/dreamina-canvas-manage-timeline/agents/openai.yaml`
- Create: `skills/dreamina-canvas-manage-timeline/references/timeline-contract.md`
- Create: `tests/scenarios/dreamina-canvas-manage-timeline.json`
- Modify: `tests/test_canvas_skill_inventory.py`

**Interfaces:**
- Consumes: verified image/video/audio node or resource IDs.
- Produces: ordered visual/audio tracks or a metadata-only timeline mutation.

- [x] **Step 1: Write the failing destructive-replacement guard test**

```python
def test_timeline_edit_warns_before_track_replacement():
    text = skill_text("dreamina-canvas-manage-timeline")
    assert "--clip" in text and "--audio-clip" in text
    assert "整体替换" in text and "未提交" in text
```

- [x] **Step 2: Verify RED, then implement timeline parsing rules**

Cover image duration, video/audio trim and speed, volume/muted, audio start, audio-only timelines, metadata-only edits, and the loss boundary when either track flag rebuilds the corresponding track.

- [x] **Step 3: Validate and commit**

```bash
git add skills/dreamina-canvas-manage-timeline tests
git commit -m "feat(canvas): add timeline management Skill"
```

### Task 13: Implement multi-node composition

**Files:**
- Create: `skills/dreamina-canvas-compose/SKILL.md`
- Create: `skills/dreamina-canvas-compose/agents/openai.yaml`
- Create: `skills/dreamina-canvas-compose/references/composition-dag.md`
- Create: `tests/scenarios/dreamina-canvas-compose.json`
- Modify: `tests/test_canvas_skill_inventory.py`

**Interfaces:**
- Consumes: canvas creation, media nodes, text nodes, Element bindings, timeline nodes, and explicit dependency order.
- Produces: a saved, non-charging canvas graph plus ordered batches eligible for separate quote/run approval.

- [x] **Step 1: Write the failing DAG and reference test**

```python
def test_compose_saves_graph_before_any_paid_run():
    text = skill_text("dreamina-canvas-compose")
    assert "Text" in text and "Element" in text and "Timeline" in text
    assert "node run" in text and "DAG" in text
    assert "默认只保存" in text
```

- [x] **Step 2: Verify RED, then implement composition**

Create upstream nodes before downstream `node:` references, distinguish follow-node Element bindings from frozen resource bindings, persist every returned node ID, and form explicit topological run batches because `node run` performs no DAG scheduling.

- [x] **Step 3: Validate and commit**

```bash
git add skills/dreamina-canvas-compose tests
git commit -m "feat(canvas): add canvas composition Skill"
```

### Task 14: Implement `dreamina-canvas-use` last

**Files:**
- Create: `skills/dreamina-canvas-use/SKILL.md`
- Create: `skills/dreamina-canvas-use/agents/openai.yaml`
- Create: `skills/dreamina-canvas-use/references/routing-table.md`
- Create: `tests/scenarios/dreamina-canvas-use.json`
- Modify: `tests/test_canvas_skill_inventory.py`

**Interfaces:**
- Consumes: all twelve lower-level Canvas Skills.
- Produces: the single implicitly discoverable end-to-end Dreamina Canvas workflow.

- [x] **Step 1: Write failing routing and invocation-policy tests**

```python
def test_only_use_skill_allows_implicit_invocation():
    for name in CANVAS_SKILLS - {"dreamina-canvas-use"}:
        assert load_openai_yaml(name)["policy"]["allow_implicit_invocation"] is False
    assert load_openai_yaml("dreamina-canvas-use")["policy"]["allow_implicit_invocation"] is True
```

- [x] **Step 2: Verify RED, then implement the thin router**

Route authentication, discovery, canvas creation, draft generation, composition, timeline, quote/run, recovery, and download requests without duplicating their command details. Every final response must separate saved draft, quoted amount, user approval, submission acceptance, terminal completion, and artifact verification.

- [x] **Step 3: Run end-to-end offline scenarios**

Required scenarios: draft-only canvas; approved image generation; unapproved exit-10 pause; interrupted video resumed with the same submit ID; mixed batch with per-item results; timeline replacement warning; verified asset download.

- [x] **Step 4: Validate and commit**

```bash
git add skills/dreamina-canvas-use tests
git commit -m "feat(canvas): add top-level Canvas orchestration Skill"
```

### Task 15: Complete repository-wide validation and publish the source SHA

**Files:**
- Create: `scripts/validate_canvas_skill_suite.py`
- Create: `verification/dreamina-canvas-skill-suite.json`
- Modify: `.claude-plugin/plugin.json`
- Modify: `README.md`
- Modify: `README.zh-CN.md`

**Interfaces:**
- Consumes: all 13 Canvas Skills and existing 13 Dreamina Skills.
- Produces: a published commit SHA that `codex-dreamina-canvas-plugin` can pin and verify byte-for-byte.

- [x] **Step 1: Add repository-wide validation**

The script must assert directory/frontmatter equality, 26 unique Skill names, exact manifest coverage, invocation policy, valid local links, no scaffold placeholders, no credential patterns, and no hard-coded catalog fixture masquerading as runtime truth.

- [x] **Step 2: Run the full gate**

```bash
python3 -m unittest discover -s tests -v
python3 scripts/validate_canvas_skill_suite.py
git diff --check
```

Run quick validation and strict TRACE separately for each of the thirteen Canvas Skills. Do not use one aggregate score as evidence for all Skills.

- [x] **Step 3: Record runtime boundary**

If installation/authentication was not separately approved, record `cli_runtime=NOT_RUN`, `auth=NOT_RUN`, and `paid_canary=NOT_RUN`. If read-only runtime inspection was approved, record exact version/commit/edition/distribution and schema hash without recording account secrets.

- [x] **Step 4: Commit and push**

```bash
git add scripts verification .claude-plugin README.md README.zh-CN.md
git commit -m "test(canvas): verify and publish Canvas Skill suite"
git push origin main
```

- [x] **Step 5: Prove publication**

Compare `git rev-parse HEAD`, `git rev-parse '@{upstream}'`, and `git ls-remote origin refs/heads/main`. Pass the identical 40-character SHA to the plugin packaging plan.
