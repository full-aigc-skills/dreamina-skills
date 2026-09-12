# Canvas Skill TRACE evaluation

Evaluator: `skill-trace-evaluation/scripts/trace_evaluate.py` (static base
score + evidence packet). Each of the thirteen Canvas Skills was evaluated
**separately**; no aggregate score is used as evidence for any individual
Skill.

Compatibility note: the upstream plan asked for a "quick validation" plus a
"strict TRACE" per Skill. The stable, runnable local implementation is the
TRACE evaluator referenced above; the plugin-level structural validation is
performed separately by `plugin-creator/scripts/validate_plugin.py` and by
`scripts/validate_canvas_skill_suite.py`.

| Skill | T | R | A | C | E | mean | ≥ 3.0 |
|-------|---|---|---|---|---|------|-------|
| `dreamina-canvas-cli` | 3.58 | 3.50 | 4.38 | 3.98 | 3.75 | 3.84 | PASS |
| `dreamina-canvas-auth` | 3.58 | 3.50 | 4.38 | 3.98 | 3.75 | 3.84 | PASS |
| `dreamina-canvas-discover-models` | 3.58 | 3.50 | 4.38 | 3.98 | 3.75 | 3.84 | PASS |
| `dreamina-canvas-create` | 4.33 | 3.55 | 4.45 | 3.92 | 3.90 | 4.03 | PASS |
| `dreamina-canvas-quote-and-run` | 3.58 | 3.58 | 4.38 | 3.92 | 3.75 | 3.84 | PASS |
| `dreamina-canvas-resume-operation` | 3.58 | 3.50 | 4.38 | 3.98 | 3.75 | 3.84 | PASS |
| `dreamina-canvas-download-assets` | 3.58 | 3.62 | 4.38 | 3.98 | 3.90 | 3.89 | PASS |
| `dreamina-canvas-generate-image` | 3.58 | 3.50 | 4.38 | 3.98 | 3.75 | 3.84 | PASS |
| `dreamina-canvas-generate-video` | 3.58 | 3.58 | 4.38 | 3.92 | 3.75 | 3.84 | PASS |
| `dreamina-canvas-generate-audio` | 4.03 | 3.75 | 4.50 | 3.92 | 3.75 | 3.99 | PASS |
| `dreamina-canvas-manage-timeline` | 3.58 | 3.55 | 4.38 | 3.92 | 3.90 | 3.87 | PASS |
| `dreamina-canvas-compose` | 3.58 | 3.55 | 4.38 | 3.92 | 3.90 | 3.87 | PASS |
| `dreamina-canvas-use` | 3.58 | 3.58 | 4.38 | 4.05 | 3.75 | 3.87 | PASS |

## Summary

- **13/13 Skills at or above the 3.0 TRACE threshold.**
- Per-Skill means: min 3.84, max 4.03, mean 3.88.
- Weakest dimension across the suite is `R` (retrieval/discovery) at
  3.50–3.75, driven by the fact that these are short, task-focused Skills
  with no bundled scripts. This is by design: each Skill delegates
  execution to the installed CLI rather than shipping code.
- These evaluations were run against the frozen Skill bytes that the
  downstream plugin pins. Re-running them is deterministic for the static
  base score.
