# Credit approval and the quote-confirm-run chain

## Approval vocabulary

| Mechanism | Effect |
|-----------|--------|
| `--credit-ceiling <n>` | Confirm only if the latest authoritative quote is `<= n`. Always preferred when the price is knowable. |
| `--credit-token <t>` | Reuse a token minted by a prior `node confirm`. Mutually exclusive with `--credit-ceiling`. |
| Interactive `y/N` | Only in TTY mode. The prompt shows the price. |
| `--yes` | Approve any amount. Use only when the price is unknowable in advance. |

## `creditConfirmation` payload

The successful `node confirm` returns a `creditConfirmation` object that
includes:

- `credit-approval token` — short-lived; never persisted.
- `minimumCreditCeiling` — a suggested ceiling. Absence does **not** mean
  zero; it means the server could not bound the spend and you must escalate.

## Quote (`node quote`) response shape

- `items[]` — one entry per node, ordered to match the request.
- `totalMaxCredits` — upper bound of the latest authoritative draft.
- `confirmable` — `false` means at least one node is un-quotable.
- `confirmationRequired` — `true` means even after passing the ceiling the
  user must explicitly approve (rare; only when the draft changed between
  quote and confirm).

## Confirm (`node confirm`) refusal conditions

`node confirm` does not mint a token when:

- Any node in the batch is un-quotable. The partial total is **not** an
  approval — it is just the partial price.
- `--credit-ceiling` is below the latest authoritative total. The response
  is a Conflict and the token is not issued.

## Run (`node run`) per-item outcomes

For a batch, provide one stable `--submit-id` for every `--node-id`, with
equal length and order. Persist the complete ordered mapping before calling
`node run`; recovery reuses each item's original ID.

| Outcome | Exit | Meaning |
|---------|------|---------|
| All items accepted | 0 | Submission accepted for every node; poll for completion. |
| Any item `REJECTED` | 2 | `cli.node_run_rejected`. Rejection is terminal; do not retry. |
| Any item `unknown`, no rejection | 20 | `cli.node_run_unknown`, `requiredAction: resume`. |
| Per-item submission failure | varies | The failure envelope includes `partialData.items[]` with the surviving `nodeId` / `submitId` per item. |

## Recovery checklist

1. Persist `submitId` **before** calling `node run`.
2. On any non-zero exit, write `submitId` and the exit code to the
   per-process journal (mode `0600`).
3. To continue: `dreamina-canvas --format json operation status <submitId>
   --project-id <projectId>` and decide based on `submission.state` and
   `submission.resubmittable`.
4. If `submission.state == "absent"` and `resubmittable == true`, escalate
   to the user. Do not auto-retry.

## What this Skill will not do

- Persist tokens, signed URLs, cookies, or session material.
- Skip re-quoting when the draft changed.
- Reuse a token on a different node set.
- Auto-retry on `REJECTED` (terminal).
- Parse localized `message` text.
