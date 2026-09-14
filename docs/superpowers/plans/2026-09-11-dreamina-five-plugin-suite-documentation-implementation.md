# Dreamina Five-Plugin Suite Documentation Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Deliver the thirty bilingual documents the suite specification enumerates — six documents each for `codex-blender`, `codex-maya`, `dreamina-canvas`, `dreamina-design`, and `dreamina-3d` — and prove they pass the specification's document-quality gates.

**Architecture:** Each plugin owns its six documents and keeps its own source of truth. A single cross-repository validator (`scripts/validate_five_plugin_docs.py` in this repository) applies the specification's §11 gates uniformly, so "the suite is documented" is a reproducible check rather than five independent claims.

**Tech Stack:** Markdown (bilingual), Mermaid, Python 3 `unittest`, `scripts/validate_five_plugin_docs.py`, `scripts/validate_architecture_filenames.py`.

**Spec:** `docs/superpowers/specs/2026-09-11-dreamina-five-plugin-suite-documentation-design.md`

## Global Constraints

- Each plugin contributes exactly six documents: `README.md`, `README.zh-CN.md`, `docs/<Stem>-Architecture.md`, `docs/<Stem>-Architecture.zh_CN.md`, `docs/<Stem>-Technical-Solution.md`, `docs/<Stem>-Technical-Solution.zh_CN.md`.
- Bilingual pairs must have identical top-level section counts and identical identifier/command/schema/version/status tokens.
- No document may claim an unverified runtime state as fact.
- A document set is complete only when `scripts/validate_five_plugin_docs.py` reports it with zero failing gates.
- A plugin's documents describe that plugin's *current* architecture. Superseded designs are archived, never restored to satisfy a naming gate.

## Status at the time this plan was written

The three earlier deliverables of the specification — the specification itself, the dependency-ordered plan (this file), and the document set — are not equally advanced:

| Deliverable | Status |
|---|---|
| The specification | delivered |
| This implementation plan | delivered |
| 30 documents | **26/30** |

Per-repository document and gate status (`python3 scripts/validate_five_plugin_docs.py`):

| Repository | Documents | Gates |
|---|---|---|
| `codex-maya-plugin` | 6/6 | all pass |
| `codex-dreamina-canvas-plugin` | 6/6 | all pass |
| `codex-dreamina-design-plugin` | 6/6 | all pass |
| `codex-dreamina-3d-plugin` | 6/6 | all pass |
| `codex-blender-plugin` | **2/6** | gate 8 fails (no Architecture document) |

---

### Task 1: Establish the cross-repository document validator

**Files:**
- Create: `scripts/validate_five_plugin_docs.py`
- Create: `docs/superpowers/plans/2026-09-11-dreamina-five-plugin-suite-documentation-implementation.md`

**Interfaces:**
- Consumes: the five plugin repositories checked out side by side, and the §11 gate list.
- Produces: a single command that reports per-repository document counts and per-gate results for the whole suite.

- [x] **Step 1: Implement the validator**

`scripts/validate_five_plugin_docs.py` locates each plugin's six documents, applies gates 1-8 that are mechanically checkable, and reports a per-repository pass/fail table plus suite totals.

- [x] **Step 2: Implement gate 6 as an identifier-class comparison**

Gate 6 (`identifiers, commands, schema fields, versions and statuses consistent across languages`) is implemented by classifying inline code spans into `flag`, `version`, `path`, `schema-type`, and `exit-code`, then requiring set equality per class. Comparing *every* inline code span is explicitly rejected: prose wraps code spans across lines and across markdown structure, which produces false positives in every repository.

- [x] **Step 3: Run it and preserve the result**

Run: `python3 scripts/validate_five_plugin_docs.py`

Expected: `TOTAL 26/30 documents; 1 failing gate results`, with the single failure being `codex-blender-plugin` gate 8.

- [x] **Step 4: Commit**

```bash
git add scripts tests
git commit -m "test: add five-plugin documentation gate validator"
```

### Task 2: `codex-dreamina-canvas-plugin` documents

**Files:**
- Package: `codex-dreamina-canvas-plugin/README.md`
- Package: `codex-dreamina-canvas-plugin/README.zh-CN.md`
- Package: `codex-dreamina-canvas-plugin/docs/Codex-Dreamina-Canvas-Plugin-Architecture.md`
- Package: `codex-dreamina-canvas-plugin/docs/Codex-Dreamina-Canvas-Plugin-Architecture.zh_CN.md`
- Package: `codex-dreamina-canvas-plugin/docs/Codex-Dreamina-Canvas-Plugin-Technical-Solution.md`
- Package: `codex-dreamina-canvas-plugin/docs/Codex-Dreamina-Canvas-Plugin-Technical-Solution.zh_CN.md`

**Interfaces:**
- Consumes: the plugin's delivered behaviour and its `docs/verification/` evidence.
- Produces: six bilingual documents that pass every §11 gate.

- [x] **Step 1: Write the six documents**
- [x] **Step 2: State the implementation status explicitly**

The architecture document must not leave the reader guessing whether its content is a target design or delivered behaviour. It carries an explicit status line.

- [x] **Step 3: Run the gates**

```bash
python3 scripts/validate_five_plugin_docs.py --root /Users/wandl/workspaces/workspace-partme-ai
```

Expected: `codex-dreamina-canvas-plugin: 6/6 docs` with every gate `PASS`.

- [x] **Step 4: Regression-guard the gates**

The canvas repository additionally encodes gates 2-9 as `tests/test_doc_quality.py`, so its documents cannot silently regress. Negative tests confirm the gates fail on injected violations.

### Task 3: `codex-maya-plugin` documents

- [x] **Step 1: Write the six documents** — `Codex-Maya-Plugin-Architecture.md` and `Codex-Maya-Plugin-Technical-Solution.md` plus their `zh_CN` pairs, alongside the two READMEs.
- [x] **Step 2: Run the gates** — expected `6/6 docs`, every gate `PASS`.

### Task 4: `codex-dreamina-design-plugin` documents

- [x] **Step 1: Write the six documents** — `Codex-Dreamina-Design-Plugin-Architecture.md` and `Codex-Dreamina-Design-Plugin-Technical-Solution.md` plus their `zh_CN` pairs, alongside the two READMEs.
- [x] **Step 2: Run the gates** — expected `6/6 docs`, every gate `PASS`.
- [x] **Step 3: Repair bilingual status drift**

The Chinese README described the canary as having reached `success` but omitted the `APPROVED` status token the English README carries. Gate 6 (`schema-type` class) flagged it. The Chinese sentence was corrected to carry both tokens.

### Task 5: `codex-dreamina-3d-plugin` documents

- [x] **Step 1: Write the six documents** — `Codex-Dreamina-3D-Plugin-Architecture.md` and `Codex-Dreamina-3D-Plugin-Technical-Solution.md` plus their `zh_CN` pairs, alongside the two READMEs.
- [x] **Step 2: Run the gates** — expected `6/6 docs`, every gate `PASS`.

### Task 6: `codex-blender-plugin` documents

**Files:**
- Package: `codex-blender-plugin/README.md` (present)
- Package: `codex-blender-plugin/README.zh-CN.md` (present)
- Package: `codex-blender-plugin/docs/Codex-Blender-Plugin-Architecture.md` (not present at `docs/`)
- Package: `codex-blender-plugin/docs/Codex-Blender-Plugin-Architecture.zh_CN.md` (not present at `docs/`)
- Package: `codex-blender-plugin/docs/Codex-Blender-Plugin-Technical-Solution.md` (not present at `docs/`)
- Package: `codex-blender-plugin/docs/Codex-Blender-Plugin-Technical-Solution.zh_CN.md` (not present at `docs/`)

**Interfaces:**
- Consumes: the plugin's current Harness architecture, whose approved specification is `codex-blender-plugin/docs/superpowers/specs/2026-09-12-codex-blender-harness-design.md`.
- Produces: the four remaining documents, written against the **current** architecture.

- [ ] **Step 1: Do not restore the archived pair**

The Jimeng-uploader-era pair is archived at `codex-blender-plugin/docs/archive/legacy-uploader/` (`Codex-Blender-Plugin-Architecture{,.zh_CN}.md` and `Codex-Blender-Plugin-Technical-Solution{,.zh_CN}.md`). It was superseded on 2026-09-12 when the plugin was redesigned as a dual-mode transactional Harness: managed bootstrap and Connector Add-on sharing one session, command, transaction, preview, and export core, with the official uploader demoted to research material and Dreamina submission moved to `codex-dreamina-3d`. Restoring those files to `docs/` to satisfy the filename gate would publish a superseded architecture as current. This step is a deliberate omission, not an oversight.

- [ ] **Step 2: Write `Codex-Blender-Plugin-Architecture.md` and `.zh_CN.md` against the Harness design**

Cover the drivers, the managed-versus-Connector topology, the transport-neutral core, the main-thread command queue, the trust boundary, the transaction/preview/export state model, failure and recovery behaviour, and the security posture. Draw context and state diagrams in Mermaid. Source every claim from the Harness specification and the plugin's `docs/verification/` evidence; do not describe uploader behaviour as current.

- [ ] **Step 3: Write `Codex-Blender-Plugin-Technical-Solution.md` and `.zh_CN.md`**

Cover Blender discovery and launch, the argv/JSON adapter contract, the command and receipt schemas, the execution-policy envelope, atomic receipt/status writes, the test strategy, and the macOS-Apple-Silicon / Windows-x64 release gates with Linux marked experimental.

- [ ] **Step 4: Run the gates**

```bash
python3 scripts/validate_five_plugin_docs.py --root /Users/wandl/workspaces/workspace-partme-ai
```

Expected: `codex-blender-plugin: 6/6 docs` with every gate `PASS`, and `TOTAL 30/30 documents; 0 failing gate results`.

- [ ] **Step 5: Commit**

```bash
git -C /Users/wandl/workspaces/workspace-partme-ai/codex-blender-plugin add docs
git -C /Users/wandl/workspaces/workspace-partme-ai/codex-blender-plugin commit -m "docs: add Harness architecture and technical solution"
```

### Task 7: Cross-plugin consistency

**Interfaces:**
- Consumes: all five plugins' documents.
- Produces: the §13 item 4 guarantee — plugin boundaries, handoff schema, approval semantics, and failure recovery stated consistently wherever two plugins' documents overlap.

- [ ] **Step 1: Verify the `ArtifactReceipt` 1.0.0 contract is stated identically**

`codex-blender` produces it, `codex-maya` produces it, `codex-dreamina-3d` consumes it. Compare the field list and version string across the three plugins' documents.

- [ ] **Step 2: Verify approval semantics do not contradict**

`dreamina-canvas`, `dreamina-design`, and `dreamina-3d` all describe quote-bound, single-use approval. Check that a claim made in one plugin's document is not negated in another's.

- [ ] **Step 3: Verify the plugin ownership table is consistent**

Each plugin's "non-goals" section must name the sibling that owns the out-of-scope capability, and the named sibling must claim it.

### Task 8: Publish and record

- [ ] **Step 1: Run the whole suite gate from a clean checkout list**

```bash
python3 scripts/validate_five_plugin_docs.py --root /Users/wandl/workspaces/workspace-partme-ai
python3 scripts/validate_canvas_skill_suite.py
python3 -m unittest discover -s tests
git -C <each plugin repository> diff --check
```

- [ ] **Step 2: Record the result**

Write the per-repository document counts and per-gate results into a verification note, and mark this plan's remaining steps complete.

## Completion Gate

```text
suite_documents_present              = 30/30
per_plugin_document_count            = 6/6 x5
gate_1_architecture_filenames        = PASS
gate_2_single_h1_balanced_fences     = PASS
gate_3_no_placeholders               = PASS
gate_4_no_secrets_or_local_paths     = PASS
gate_5_bilingual_section_parity      = PASS
gate_6_identifier_token_parity       = PASS
gate_7_relative_links_resolve        = PASS
gate_8_mermaid_present               = PASS
cross_plugin_consistency             = PASS
```

Every line must be measured by `scripts/validate_five_plugin_docs.py` plus the per-repository `git diff --check`. A hundred-percent document count with a self-declared pass is not evidence; the validator's output is.
