---
name: dreamina-canvas-resume-operation
description: Use when an agent or script must continue, observe, or recover a Dreamina Canvas async operation by its submitId, never by minting a new submitId. Owns the operation state machine and the resubmittable invariant.
license: Complete terms in LICENSE
---

# Dreamina Canvas Operation Recovery

This Skill owns how an in-flight or stuck `submitId` is observed, waited
on, or recovered. It **never** authorises a new submission: when recovery
is impossible, it escalates to the user.

Reference detail is in
[references/recovery-state-machine.md](references/recovery-state-machine.md).

## When to use

- A `node run` (or any paid command) returned exit code 20 with
  `requiredAction: resume`.
- A previous process timed out, crashed, or lost its in-memory state but
  persisted `projectId` + `submitId`.
- The user wants to know whether a previously started run is still in
  flight, completed, or failed.

## When **not** to use

- For starting a new run. That is `dreamina-canvas-quote-and-run`.
- For re-quoting a draft that has not been approved yet.

## The two observation commands

```bash
# Pure read; never advances server-side state
dreamina-canvas --format json operation status <submitId> \
  --project-id <projectId>

# Poll to terminal state with a bounded local timeout
dreamina-canvas --format json operation wait <submitId> \
  --project-id <projectId> --timeout 10m --interval 5s
```

`operation status` is always safe to call. `operation wait` returns exit 0
only when the operation reaches a terminal state. A local timeout on
`operation wait` returns exit code 20; **the server keeps running**, the
local wait was just over budget.

## Submission state machine

`operation status` returns a `submission` block:

| `submission.state` | Meaning | Resubmittable? |
|--------------------|---------|----------------|
| `absent` | Server currently has no record of this submission. Does **not** prove the original request never reached the server; could also be retention expiry. | `resubmittable == true` only in this state. Treat as ambiguous and escalate. |
| `in_progress` | The server has accepted the submission; no terminal resource yet. | Never true. |
| `completed` | Terminal resource available; download via `dreamina-canvas-download-assets`. | Never true. |

A missing `submission` field is treated as **"accepted by server"**, never
as `absent`. Assuming `absent` when the server actually accepted would
cause a duplicate bill.

## Resubmit invariant

- `submission.resubmittable == true` appears **only** when `state == "absent"`.
- This is the **only** moment a re-submission is allowed.
- All other states require `operation status` / `operation wait`; never
  a fresh `node run` with a new `submitId`.

## Per-item state

For batch operations, the same rules apply per item. A missing `state`
field on an item is **not** failure; the call did not return a verdict for
that item. Use `operation status <submitId>` to inspect each item.

## Failure → recovery

| Failure | requiredAction | What to do next |
|---------|----------------|-----------------|
| `operation status` returns exit 11 | `login` | Re-authenticate, then re-query. |
| `operation wait` times out locally | `resume` | Increase `--timeout` or come back later; the operation is still running server-side. |
| `submission.state == "absent"` + `resubmittable == true` | `human_intervention` | Surface to the user; do not auto-resubmit. |
| `submission.state == "absent"` + `resubmittable == false` (or missing) | `resume` | Treat as accepted; continue waiting. |
| Server returns exit 21 | `retry` | Bounded back off and retry. |

## What this Skill will not do

- Mint a new `submitId`.
- Re-submit when `resubmittable` is not explicitly `true`.
- Treat a missing `submission` field as `absent`.
- Persist tokens, signed URLs, cookies, or session material.
