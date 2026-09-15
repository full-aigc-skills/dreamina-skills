---
name: dreamina-3d-resume
description: Resume a paused Dreamina 3D job from its ledger state. Use when the user wants to continue an in-flight job without re-paying or re-exporting.
metadata:
  type: workflow
  plugin: codex-dreamina-3d
  status: stable
---

# codex-dreamina-3d-resume

## When to use

The user references an existing job id and wants to continue without
restarting local export or remote submission. The job ledger is the
single source of truth for what has already happened.

Use `McpDesignClient` for all Dreamina Design operations. Resume may call only
the typed status, account, submit, and query mappings; after a stored
`design_submit_id` exists it may call only the query mapping.

## Workflow

For a persisted `auto_with_budget` job, automatically resume only the safe
next state: capability/quote work before a submission, or query/download work
after its stored submit identifier. Never convert a budget stop, missing web
prerequisite, failed validation, `Unknown`, or failed job into a new paid
submission without a new user instruction.

1. **Load.** `JobLedger.read()` on the user's job file. If the file does
   not exist, stop and ask the user to specify a valid `job_id`.
2. **Map state → next action.**

   | Current state       | Next action                                                                 |
   |---------------------|------------------------------------------------------------------------------|
   | `Draft`             | ask the user to choose a companion DCC                                        |
   | `DccSelected`       | resume from the PreviewSpecified step                                         |
   | `PreviewSpecified`  | re-validate the existing preview receipt; on mismatch re-export              |
   | `PreviewValidated`  | resume capability resolution                                                  |
   | `CapabilityResolved`| resume quote (do not reuse a quote for inputs that have changed)              |
   | `Quoted`            | ask the user to confirm or reject the quote                                   |
   | `Approved`          | check `submit.design_submit_id` — if present, only query, never resubmit      |
   | `Submitted`         | only query the design plugin; never re-export or re-submit                   |
   | `Querying`          | continue polling                                                             |
   | `Completed`         | verify the on-disk artifact hash; if missing, transition to Failed           |
   | `Failed` / `Unknown`| ask the user to authorise a recovery action (re-quote / re-query / restart)  |

3. **Never repeat completed work.**
   - A `Completed` job must never be re-submitted or re-exported.
   - A `Submitted`/`Querying`/`Unknown` job must never be re-exported.
   - Only `Draft`, `DccSelected`, and `PreviewSpecified` may re-invoke the
     DCC adapter, and only if the on-disk artifact hash no longer matches.

## Never do

- Never auto-resubmit a paid action.
- Never silently rewrite history; append to the job ledger instead.
- Never invent a `design_submit_id`; the design plugin is the only source.
