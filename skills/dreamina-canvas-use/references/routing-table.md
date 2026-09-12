# Routing table for dreamina-canvas-use

The end-to-end Skill is a **thin router**. It does not duplicate command
details, exit-code tables, model catalogs, or node schemas — those
belong to the lower-level Skills.

## Lower-level Skill inventory (do not re-implement here)

| Skill | Purpose |
|-------|---------|
| `dreamina-canvas-cli` | argv construction, exit-code routing, stdout/stderr separation |
| `dreamina-canvas-auth` | login / refresh / logout / profile isolation |
| `dreamina-canvas-discover-models` | live model / voice / ratio / resolution / duration discovery |
| `dreamina-canvas-create` | canvas lifecycle and `--project-id` reuse |
| `dreamina-canvas-compose` | non-charging DAG composition |
| `dreamina-canvas-generate-image` | image node (t2i / i2i) |
| `dreamina-canvas-generate-video` | video node (t2v / first_last_frame / m2v) |
| `dreamina-canvas-generate-audio` | audio node (tts / music) |
| `dreamina-canvas-manage-timeline` | timeline track replacement |
| `dreamina-canvas-quote-and-run` | quote → confirm → run safety transaction |
| `dreamina-canvas-resume-operation` | observe and recover async runs by submitId |
| `dreamina-canvas-download-assets` | verify and download completed node resources |

All twelve have `allow_implicit_invocation: false`. Only this Skill
(`dreamina-canvas-use`) may be invoked implicitly.

## Canonical end-to-end sequence

```text
dreamina-canvas-cli                  (pre-flight: version + schema)
  → dreamina-canvas-auth              (auth account confirms logged-in)
  → dreamina-canvas-discover-models   (model / voice discovery)
  → dreamina-canvas-create            (canvas create + --use)
  → dreamina-canvas-compose           (save drafts in dependency order)
  → dreamina-canvas-quote-and-run     (quote → confirm → run)
  → dreamina-canvas-resume-operation  (operation status / wait)
  → dreamina-canvas-download-assets   (resource get / download, SHA-256)
```

The Skill may skip steps when the user did not ask for them. It must not
add steps that the user did not ask for.

## Lifecycle reporting

Every final response surfaces these stages in order:

1. Saved draft id(s) (`nodeId`, `mutationVersion`).
2. Quoted amount (`totalMaxCredits`, `confirmable`,
   `confirmationRequired`).
3. User approval (`--credit-ceiling` value used; never the token).
4. Submission acceptance (`submitId`, `nodeId`, exit code).
5. Terminal completion (`submission.state == "completed"` plus
   `resourceId`).
6. Verified artifact (canonical local path, byte count, SHA-256).

If any stage fails, the response includes the failure exit code, the
`requiredAction`, and the recommended next step.

## What this Skill will not do

- Persist tokens, signed URLs, cookies, or `credit-approval token`.
- Approve spend on the user's behalf.
- Bypass the lower-level Skills' guardrails.
- Mint a `submitId`.
- Implicit-invoke the other twelve Canvas Skills; each is explicit.
