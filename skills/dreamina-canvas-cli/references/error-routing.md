# Error routing for dreamina-canvas

Branch only on numeric exit code plus `error.code` and `error.requiredAction`.
Never parse the localized `error.message`.

## Exit codes (union across all subcommands)

| Exit | Meaning | requiredAction candidates | Recovery |
|------|---------|---------------------------|----------|
| 0 | success | none | continue |
| 1 | uncategorized internal failure | none / contact_support | alert; do not retry blindly |
| 2 | invalid command, argument, or input schema | none / human_intervention | fix the command; retry is useless |
| 11 | login required or session expired | login | re-authenticate, then retry with the same identity |
| 12 | permission / capability / entitlement denied | human_intervention / contact_support | do not retry; escalate |
| 13 | environment or release compatibility blocked | upgrade | upgrade per `error.clientUpgrade.upgradeUrl` |
| 20 | recoverable; not converged in this run | resume | continue with `operationRef` |
| 21 | retryable service / transport failure | retry | bounded back off, then retry |
| 22 | human intervention required | human_intervention | hand off |

## requiredAction enum

`none | login | confirm | retry | resume | upgrade | human_intervention | contact_support`.

## Read vs write semantics

- Read commands (`model`, `voice`, `canvas ls`, `node find`, `node show`,
  `operation status`, `resource get`, `schema`, `version`) return a
  non-terminal state with exit 0 and `ok: true`. Continue.
- `operation wait` returns exit 0 only when the operation reaches a terminal
  state. Local timeout on `operation wait` returns exit 20; the operation is
  still running server-side, not cancelled.

## Submission edge cases

- `--credit-ceiling <n>` is the only safe approval: it caps the spend even
  when `--yes` is also present.
- `--submit-id ""` (explicit empty) is rejected with exit 2; it is the
  deliberate trap that prevents a shell variable expansion failure from
  silently minting a new idempotency key.
- `submission.state = absent` plus `resubmittable = true` is the only moment
  when re-submission is allowed; treat a missing `submission` field as
  "accepted by server", never as "absent".
