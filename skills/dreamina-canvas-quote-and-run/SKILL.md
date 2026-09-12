---
name: dreamina-canvas-quote-and-run
description: Use when an agent or script must quote, confirm, and run a saved Dreamina Canvas node, bind approval to an exact quote and credit ceiling, and never mint a new submitId for recovery.
license: Complete terms in LICENSE
---

# Dreamina Canvas Quote → Confirm → Run

This Skill owns the safety transaction for paid execution. The transaction
is always: `node quote` against the latest authoritative draft, then
`node confirm` to bind user approval to an exact credit ceiling, then
`node run` with a caller-minted `submitId`. Reusing the same `submitId`
on recovery replays the original submission and never re-bills.

Reference detail is in
[references/credit-approval.md](references/credit-approval.md).

## When to use

- The caller wants to actually run a previously saved node (after the
  structural work is finished and the user has authorised the spend).
- A prior `node quote` returned `confirmable=false`; this Skill explains
  why and what to do next.
- A `node run` failed with exit code 20 (`resume`); this Skill explains
  how to continue without re-billing. Always re-quote before retrying.

## When **not** to use

- For saving a draft without running. That is `node create <type>` without
  `--run`, owned by the relevant domain Skill.
- For re-quoting after a silent change to the saved draft; this Skill
  always re-quotes from the live authoritative draft.

## The three-step transaction

```bash
# 1. Re-quote from the live draft (always the latest authoritative state)
dreamina-canvas --format json node quote --node-id <nodeId> \
  --project-id "$PROJECT_ID"
# → items[] (one entry per node, ordered), totalMaxCredits, confirmable,
#   confirmationRequired, creditConfirmation.minimumCreditCeiling

# 2. Confirm the spend ceiling (mints a short-lived credit-approval token)
token=$(dreamina-canvas --format json node confirm \
  --node-id <nodeId> \
  --project-id "$PROJECT_ID" \
  --credit-ceiling "$CEILING" \
  | jq -r '.data.credit-approval token')

# 3. Run with the existing submitId; reuse the same id on retry
dreamina-canvas --format json node run \
  --node-id <nodeId> \
  --project-id "$PROJECT_ID" \
  --credit-token "$token" \
  --submit-id "$SUBMIT_ID"
```

## Binding rules (read carefully)

The credit `token` is bound to **who + which canvas + which batch of nodes
+ ceiling + batch summary**. It is **not** bound to the prompt text.

Two direct consequences:

- Editing the prompt between confirm and run is fine **as long as the
  latest live quote is still within the approved ceiling**. `node run`
  re-quotes the latest draft and runs only if the total stays under
  the ceiling.
- The token cannot be moved to a different node set. Different nodes need
  a new confirm.

`node confirm` refuses to mint a token when:

- Any node is un-quotable (`confirmable=false`).
- The supplied `--credit-ceiling` is below the latest total (returns
  Conflict).

## The submitId is the only billable identity

Generate `submitId` yourself (lowercase UUID) and persist it **before**
`node run`. Reusing the same `submitId` replays the original submission
and never re-bills. Switching to a new `submitId` **is** a new run and
re-bills.

`--submit-id ""` (explicit empty) is rejected with exit code 2; this is the
deliberate trap that prevents an unset shell variable from silently
minting a fresh idempotency key.

## Per-item batch behaviour

`node run` may take multiple `--node-id` values. The response `data.items[]`
is the same length and order as the input. Per-item outcomes:

- `REJECTED` (any item) → `cli.node_run_rejected`, exit code 2. Rejection
  is terminal; retry is useless.
- `unknown` (any item, no rejection) → `cli.node_run_unknown`, exit code 20,
  `requiredAction: resume`.
- All accepted → exit code 0.

If submission fails entirely, the failure envelope includes
`partialData.items[]` with each item's `nodeId` / `submitId`. Absence of a
`state` field in an item is **not** failure — it means the call did not
return a verdict for that item; the operation may still be in flight
server-side. Use `operation status <submitId>` to inspect each item.

## Recovery rules

- An ambiguous or timed-out response is reconciled **by ID**, not by
  re-submitting.
- `operationRef` (alias for `submitId`) is the key; pass it to
  `operation status` or `operation wait`.
- `submission.state = absent` plus `resubmittable = true` is the **only**
  case where re-submission is permitted. A missing `submission` field is
  treated as "accepted by server", never as "absent" — assuming absent
  when the server actually accepted would cause a duplicate bill.

## What this Skill will not do

- Persist `credit-approval token`, signed URLs, cookies, OAuth tokens, or
  any provider task identifier.
- Re-quote with a stale draft.
- Mint a new `submitId` on retry; it must be reused.
- Branch on localized `message` text — only on exit code, `error.code`,
  and `error.requiredAction`.
- Use `--yes` instead of `--credit-ceiling` when the price is knowable
  in advance.
