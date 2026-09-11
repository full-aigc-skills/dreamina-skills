---
name: dreamina-canvas-auth
description: Use when an agent or script must check, refresh, or recover Dreamina Canvas authentication, distinguish local login state from server-recognized identity, and isolate credentials across profiles. Never prints or persists tokens.
license: Complete terms in LICENSE
---

# Dreamina Canvas Authentication

This Skill owns authentication state for the `dreamina-canvas` CLI. It does
**not** generate, quote, or submit anything; it only governs login, status
checks, refresh, logout, and profile isolation.

Reference detail is in
[references/auth-state.md](references/auth-state.md).

## When to use

- Before any command that may require credentials (use `auth account` to
  confirm, not `auth status`).
- When a prior command returned exit code 11 (`requiredAction: login`) or
  exit code 12 (permission denied).
- When switching between isolated profiles (`--profile <name>`).
- When the user explicitly asks to log in, log out, or refresh credentials.

## When **not** to use

- For installing or upgrading the CLI binary itself (`dreamina-canvas-cli`).
- For running paid commands; this Skill only confirms and refreshes the
  identity, it never invokes generation.

## The two "am I logged in?" questions

These answer two different things and the answers can disagree:

| Command | Question answered | Talks to server? | Trust for "logged in"? |
|---------|-------------------|------------------|------------------------|
| `auth status` | "do I have a non-expired local token for this profile?" | No — local file only | Never alone |
| `auth account` | "what does the server currently recognise this profile as?" | Yes | Yes — the only authoritative check |

Always treat `auth account` as the source of truth for "is this profile
logged in?" `auth status` exists only to inspect local state when debugging.

A common failure mode: local token looks fine, but the server has revoked
it. The CLI will surface this as exit code 11 with `requiredAction: login`;
re-login and retry the original command with the **same identifiers**
(`projectId`, `submitId`, `nodeId`).

## Login flow

```bash
# TTY: blocks until the user completes browser authorisation
dreamina-canvas --format json auth login --profile <name>

# Non-TTY (script / agent): returns a recoverable challenge
dreamina-canvas --format json auth login --profile <name>
# → challenge payload includes a device code; do NOT loop here, hand it to a human

# Continue waiting on the same device code from any process
dreamina-canvas --format json auth wait --device-code <code> --timeout 10m
```

`--timeout` defaults to 10 minutes; `--timeout 0` polls once. Do not loop on
`auth login` in a script; use `auth wait` so that a separate process (or the
user in a browser) can complete the step.

## Refresh and logout

- `auth refresh` — only when the credential is still in its refresh window.
  Do not call it speculatively.
- `auth logout` — idempotent. The overseas build (`distribution != cn`)
  revokes server-side before deleting local credentials.

## Profile isolation

Credentials, login state, and the active canvas context are all keyed by
`--profile`. Profile names may contain only letters, digits, `.`, `_`, and
`-`. Keep one profile per isolated environment (work / personal / CI).

```bash
dreamina-canvas --profile work auth login
dreamina-canvas --profile personal auth account
```

The two profiles do not interfere with each other. The active profile is
the only one that subsequent `node create`, `canvas create --use`, and
similar commands will pick up by default.

## What this Skill will not do

- Persist, log, or echo OAuth tokens, cookies, signed URLs, or any other
  credential material.
- Auto-retry on exit code 12 (permission denied); that requires a human.
- Run generation commands even when authenticated; that is the role of
  `dreamina-canvas-quote-and-run`.
