# Authentication state machine

## Command matrix

| Command | Effect | Side-effect | Notes |
|---------|--------|-------------|-------|
| `auth login` | Start device-authorisation login | Local: writes challenge state; Server: registers device | TTY blocks; non-TTY returns the challenge payload. |
| `auth wait --device-code <code>` | Wait for a previously started authorisation | None beyond credential write | `--timeout` default 10m; `0` polls once. |
| `auth account` | Server-side identity check | Read-only server call | Authoritative for "am I logged in?". |
| `auth status` | Local credential inspection | Read-only file read | Never sufficient alone for "logged in". |
| `auth refresh` | Refresh credentials in their refresh window | Writes refreshed local credential | Do not call speculatively. |
| `auth logout` | Idempotent logout | Local: deletes credential; overseas build also revokes server-side | |

## Failure → recovery map

| Failure | requiredAction | What to do next |
|---------|----------------|-----------------|
| `auth login` returns a challenge in non-TTY | n/a (script must hand it off) | Display the device URL/code to the user; do not loop. |
| Any command returns exit 11 | `login` | Re-run `auth login` for the active profile, then retry with the **same** `projectId` / `submitId` / `nodeId`. |
| `auth account` returns a different account than expected | n/a (escalate) | Hand off to the user; this is not a script-fixable condition. |
| `auth refresh` returns exit 2 | n/a | Token is outside its refresh window; fall back to `auth login`. |
| Any command returns exit 12 | `human_intervention` | Do not retry; ask the user to check account / entitlement. |

## Profile isolation rules

- Profile names must match `[A-Za-z0-9._-]+`.
- One profile per isolated environment (work / personal / CI / a single test
  script).
- Never read or write another profile's `~/.config/dreamina-canvas/contexts/`
  or `~/.config/dreamina-canvas/operations/` directly — go through the CLI.

## What is never echoed

Tokens, cookies, signed URLs, `credit-approval token`, `storageId`, and any
provider task identifier must never appear in stdout, stderr, log files,
fixture data, or skill journals. If a script accidentally captures one,
rotate the credential immediately rather than redacting and re-using.
