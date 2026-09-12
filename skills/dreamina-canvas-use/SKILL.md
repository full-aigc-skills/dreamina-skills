---
name: dreamina-canvas-use
description: Use when an agent or user wants the canonical Dreamina Canvas end-to-end workflow without naming a specific Skill. Routes to the smallest applicable Skill chain and reports saved drafts, quoted amounts, approval, submission acceptance, terminal completion, and verified artifacts.
license: Complete terms in LICENSE
---

# Dreamina Canvas (end-to-end)

This Skill is the **single implicitly invokable** entry point for the
Dreamina Canvas suite. It selects the smallest applicable Skill chain
from the other twelve Canvas Skills and orchestrates the full flow:

```text
saved draft  →  quoted amount  →  user approval  →
submission accepted  →  terminal completion  →  verified artifact
```

Reference routing detail is in
[references/routing-table.md](references/routing-table.md).

## When to use

- The user asks for "the canvas workflow" or "Dreamina Canvas" without
  naming a specific Skill.
- The agent wants to compose a multi-node Canvas end-to-end and report
  each lifecycle stage back to the user.

## When **not** to use

- For advanced users who already know which lower-level Skill they want;
  call that Skill directly.
- For installing, authenticating, or running any paid command without
  explicit user authorisation.

## Routing rules

| User intent | Skill chain (in order) |
|-------------|-----------------------|
| "Set up Dreamina Canvas / install / log in" | `dreamina-canvas-cli` → `dreamina-canvas-auth` |
| "Find a model / voice / ratio / resolution" | `dreamina-canvas-discover-models` |
| "Create / select a canvas" | `dreamina-canvas-create` |
| "Save a draft image / video / audio node" | `dreamina-canvas-generate-image` / `…video` / `…audio` |
| "Compose a graph of nodes (image / video / audio / timeline)" | `dreamina-canvas-compose` (then hand to quote-and-run) |
| "Edit a timeline (clip / audio-clip / trim / speed)" | `dreamina-canvas-manage-timeline` |
| "Quote → confirm → run a saved node" | `dreamina-canvas-quote-and-run` |
| "Continue / observe an async run" | `dreamina-canvas-resume-operation` |
| "Download a finished resource" | `dreamina-canvas-download-assets` |

This Skill **does not duplicate** global flags, exit-code tables, model
catalogs, or node schemas; those belong to the lower-level Skills.

## Lifecycle reporting

Every final response from this Skill must surface, in order:

1. The saved draft identifier(s) (`nodeId`, `mutationVersion`).
2. The quoted amount (`totalMaxCredits`, `confirmable`,
   `confirmationRequired`).
3. The user approval (`--credit-ceiling` value used; never the token).
4. The submission acceptance (`submitId`, `nodeId`, exit code).
5. The terminal completion (`submission.state == "completed"` plus
   `resourceId`).
6. The verified artifact (canonical local path, byte count, SHA-256).

If any stage fails, the Skill returns the failure exit code, the
`requiredAction`, and the next step the caller should take.

## What this Skill will not do

- Persist tokens, signed URLs, cookies, or `credit-approval token`.
- Approve spend on the user's behalf.
- Bypass the lower-level Skills' guardrails.
- Mint a `submitId` itself; it only forwards the one minted by
  `dreamina-canvas-quote-and-run`.
- Implicit-invoke the other twelve Canvas Skills: each of them is
  explicit. This Skill is the only one that may be invoked implicitly.

## Invocation policy

`allow_implicit_invocation: true` for **this Skill only**. All twelve
other `dreamina-canvas-*` Skills set `allow_implicit_invocation: false`.

## Policy

Invocation requires:
- Confirmed installation of dreamina-canvas
- User's authorisation for each paid stage

Forbids:
- Persisting tokens, signed URLs, cookies, or credit-approval token
- Approving spend on the user's behalf
- Duplicating the lower-level Skills' command, exit-code, or model details
- Minting a submitId; only forward the one from dreamina-canvas-quote-and-run

Default prompt:

> Route to the smallest applicable Skill chain. Always surface saved
> draft, quoted amount, user approval, submission acceptance, terminal
> completion, and verified artifact. Never duplicate the lower-level
> Skills' details. Never approve spend.
>
