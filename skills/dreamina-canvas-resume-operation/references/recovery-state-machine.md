# Operation recovery state machine

## Diagram

```
            ┌─────────────────┐
            │  (no record)    │
            └─────────────────┘
                    │  operation status
                    ▼
       ┌─────────────────────────┐
       │  submission.state       │
       └─────────────────────────┘
        │              │              │
   "absent"     "in_progress"    "completed"
        │              │              │
   resubmittable   keep waiting    fetch resource
   == true?       via status /    via resource get
        │          wait            or resource download
        ▼
   ┌──────────────┐
   │ escalate to  │   ← never auto-retry
   │ user         │
   └──────────────┘
```

## Decision rules (script-friendly)

```text
if submission is missing:
    treat as accepted → continue with status / wait
elif submission.state == "completed":
    switch to dreamina-canvas-download-assets
elif submission.state == "in_progress":
    keep waiting via operation status or operation wait
elif submission.state == "absent" and resubmittable == true:
    escalate to the user; never auto-retry
elif submission.state == "absent" and resubmittable != true:
    treat as accepted → continue waiting
else:
    treat as accepted → continue waiting
```

## What "absent" really means

Server has **no** record of this `submitId`. Two possibilities:

- The original request never reached the server.
- The server's retention window for that submission fact has expired.

In either case, the only safe answer is: **ask the user**. Auto-retrying
risks double-billing if the original request did reach the server but the
fact was lost in transit between the response and the journal.

## `operation wait` vs `operation status`

- `operation status` is single-shot, non-advancing, cheap to call.
- `operation wait` blocks locally with `--timeout` and polls at
  `--interval` until the operation reaches a terminal state.
- Local timeout on `operation wait` returns exit code 20; the operation
  is still running server-side. Call `operation status` to confirm, then
  decide whether to extend `--timeout`.

## `--timeout` semantics

`--timeout` constrains only the **local** wait. It does not cancel the
server-side operation. After a local timeout the caller must decide
whether to:

- Continue with a longer `--timeout`, or
- Hand off to the user for a longer-lived observation.

## Journal hygiene

After every `node run` (or any other submitter), persist:

- `projectId`
- `nodeId`
- `submitId`
- exit code
- timestamp

Mode `0600`. Never persist tokens, signed URLs, cookies, or the raw
response body of `node confirm`.

## What this Skill will not do

- Cancel a server-side operation (the CLI does not support that and the
  user should not be misled).
- Mint a new `submitId`.
- Assume the operation is dead just because the local wait timed out.
