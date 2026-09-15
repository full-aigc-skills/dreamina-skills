---
name: dreamina-video-evaluator
description: Use when judging generated Dreamina shot clips against measured gates, producing shot_evaluation.schema.json content only.
---

# Dreamina Video Evaluator

Evaluate only, and only after measurement. This Skill produces
`shot_evaluation.schema.json` content and nothing else.

## Example request

```text
Use dreamina-video-evaluator for shot S03 attempt 1 after reading its measured
gates and approved design. If retry is necessary, select only the next request
fingerprint already present in the activated batch allowance.
```

## 能力边界说明

### ✅ 能做

- Read the measured clip gates for one shot attempt.
- Judge whether the clip satisfies the design intent.
- Return `accepted`, a prequoted `retry`, `rejected`, or `manual_review`.

### ⚠ 需要素材

- A measured artifact with its SHA-256 and deterministic gate results.
- The design version the attempt was generated from.

### ❌ 超出范围

- Do not produce `shot_annotation.schema.json`. Shot semantics belong to `dreamina-shot-annotator`.
- Do not re-measure media or override the measured gates.
- Do not request more attempts than the batch quote already covers.
- Do not resubmit. `retry` must reference an attempt the quote already enumerated.

## Workflow

1. Receive the measured gates for exactly one shot attempt.
2. Compare against the design intent for that shot.
3. Return the evaluation with one of the four decisions, and for `retry` the prequoted attempt.

## Never do

- Never accept a clip whose measured gates failed.
- Never invent an attempt beyond the quote.
- Never blur the line between design intent and acceptance verdict.
