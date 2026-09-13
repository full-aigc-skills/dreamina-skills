---
name: dreamina-canvas-cli
description: Use when an agent must install, verify, update, or invoke dreamina-canvas and safely construct argv, route exit codes, separate stdout/stderr, persist identifiers, and avoid hard-coded catalogs.
license: Complete terms in LICENSE
---

# Dreamina Canvas CLI Foundation

This Skill owns the cross-cutting invariants every other `dreamina-canvas-*` Skill
relies on. It does **not** generate, quote, or submit anything; it only governs how
commands are built, how failures are interpreted, and how identifiers are persisted.

The reviewed CLI guide is
[references/cli-contract.md](references/cli-contract.md) and the routing rules are
in [references/error-routing.md](references/error-routing.md).
For authorized first-time installation and update, read
[references/install-to-use.md](references/install-to-use.md).

## When to use

- Before constructing any argv for `dreamina-canvas` from another Canvas Skill.
- When the binary is missing or requests an upgrade and the user wants the
  official domestic or overseas installer workflow.
- When a `dreamina-canvas` invocation returned a non-zero exit code or a JSON
  error envelope on stderr.
- When deciding whether the next step is to wait, retry, re-quote, or hand the
  task back to the user.

## When **not** to use

- For domain-specific generation guidance (`dreamina-canvas-generate-image`,
  `dreamina-canvas-generate-video`, etc.).
- For logging in or running any paid command — those are separately authorized
  at the action boundary (see `dreamina-canvas-auth` and the human-in-the-loop
  gates in this Skill set).

## Mandatory pre-flight

If the command is absent, stop and obtain installation authorization before
using the official command in `install-to-use.md`. After installation run
`dreamina-canvas --help`, then continue with the machine-readable checks below.

Before any non-trivial command:

1. `dreamina-canvas version` — confirm the binary is installed and capture the
   `commit`, `edition`, `distribution`, `buildTime`, `releaseDate`. Treat this
   output as authoritative; do not trust README prose for the current behavior.
2. `dreamina-canvas schema "<command path>"` (with `--format json`) — confirm
   the flag and value names used by this Skill. The guide seed values may
   lag the live binary.
3. `dreamina-canvas auth account` (when any later command may need credentials)
   — confirm the server recognises the active profile. `auth status` is local
   only; never trust it for "logged in".

Only after these three succeed may the caller construct the real command. Never
optimise them away, even for read-only commands, because schema drift is the
most common silent-failure cause.

## argv construction

Always pass `--format json` **before** the subcommand. The binary is the only
authoritative output channel; without `--format json` the result depends on
whether stdout is a TTY.

Global flags (place before the subcommand):

- `--format json` — required for any machine-driven call.
- `--non-interactive` — recommended whenever the agent cannot answer prompts.
- `--yes` — opt-in only; it never bypasses credit approval or capability gates.
- `--profile <name>` — isolate credentials and the active canvas context.
- `--region <cn>` — domestic public build fixed to `cn`; the overseas build
  omits the flag.

Never:

- Build argv by string interpolation. Use argv lists.
- Re-use a `--submit-id` value that came from an empty shell variable; pass
  `--submit-id ""` only when the script has already validated it is non-empty.
  An explicit empty value is rejected with exit code 2.
- Add `--run` to `node create` / `node edit` unless the caller has authorised
  the credit spend at this exact moment.

## stdout and stderr

- stdout in `--format json` mode contains only the declared JSON payload
  (`{"schemaVersion": "...", "ok": true, "data": {...}}` or
  `{"ok": false, "error": {...}}`).
- stderr carries everything else: progress, diagnostics, and on failure the
  single structured error envelope JSON object. stdout is empty during a
  failure.
- Therefore `dreamina-canvas --format json <cmd> > result.json` always gives a
  clean result file; never mix pipe stages from concurrent processes into one
  `jq` pipeline (their JSON bytes will interleave).

## Exit code routing

Do **not** parse localised `message` text. Branch only on the numeric exit code
and, for non-zero exits, on `error.code` plus `error.requiredAction`. Stable
codes from the CLI itself are namespaced `cli.*`; server-side business codes
are forwarded unchanged.

When `exit code 20` arrives it means the operation is still in flight and
recoverable: continue with the same `submitId` through `operation wait`; it
**never** authorises a new submission.

| Exit | Meaning | Next action |
|------|---------|-------------|
| 0 | success | continue |
| 1 | uncategorized internal failure | alert; investigate |
| 2 | invalid command, argument, or input schema | fix the command; do not retry |
| 11 | login required or session expired | re-authenticate then retry with the same identity |
| 12 | permission / capability / entitlement denied | do not retry; escalate |
| 13 | environment or release compatibility blocked | upgrade per `error.clientUpgrade.upgradeUrl` |
| 20 | recoverable; not converged in this run | continue with `operationRef` (`operation wait`) |
| 21 | retryable service or transport failure | back off and retry |
| 22 | human intervention required | hand off |

`requiredAction` values are one of `none`, `login`, `confirm`, `retry`,
`resume`, `upgrade`, `human_intervention`, `contact_support`. They are the
authoritative next-step hint for scripts.

## Identifier persistence

- `projectId`, `submitId`, `nodeId`, `updateId`, `resourceId`, `quoteId` are
  lowercase canonical UUIDs. Reuse the same `submitId` to continue a run;
  reusing it never re-bills. Switching to a new `submitId` re-bills.
- Generate them with `uuidgen | tr 'A-Z' 'a-z'`, persist them in
  process-managed state files (mode `0600`), and pass them explicitly on every
  cross-process retry.
- `submitId` empty (explicit or after a failed variable expansion) is
  rejected with exit code 2 — never let a missing variable silently mint a new
  idempotency key.

## What this Skill will not do

- Install or update the CLI without explicit user authorization; log in,
  refresh tokens, or perform paid generation from this foundation Skill.
- Persist OAuth tokens, cookies, signed URLs, or `credit-approval token`.
- Branch on localised human-language messages.
- Mutate the local `--use` canvas context unless the caller asked explicitly.

## Policy

Invocation requires:
- Confirmed installation of dreamina-canvas, or explicit authorization to use
  an official installer
- Verified --format json contract via dreamina-canvas schema

Forbids:
- Installing or updating the CLI without explicit user authorization
- Logging in, refreshing tokens, or running paid commands
- Persisting OAuth tokens, cookies, signed URLs, or credit-approval token

Default prompt:

> Before any non-trivial dreamina-canvas call, run version + schema, pass
> --format json, and route failures by exit code + requiredAction. Never
> hard-code model or voice names.
>
