---
name: dreamina-3d-from-blender
description: Drive a Blender preview through the validated Dreamina 3D pipeline. Use when the user has a Blender scene and wants a Seedance 2.5 render from it.
metadata:
  type: workflow
  plugin: codex-dreamina-3d
  source_dcc: codex-blender
  status: stable
---

# codex-dreamina-3d-from-blender

## When to use

The user wants a Dreamina 3D render from a Blender scene. Companion
`codex-blender` is already installed.

## Workflow

### Automatic run policy

When the user provides one `auto_with_budget` envelope — approved reference
upload, model/resolution/duration preferences, a maximum charge, and
permission for one remote submission — perform the following workflow without
asking at every state transition. Resolve capability, validate the preview,
obtain and compare the quote, submit once only when it is within the cap,
query the recorded identifier, download, and independently verify the final
artifact. Return one final artifact inventory.

Stop and ask only when the quote exceeds the cap, a required reference was
not authorized for upload, a platform-mandated confirmation or web
prerequisite is pending, validation fails, or recovery would require another
paid submission. `interactive` retains the review at each gate; `review_only`
does not upload or submit.

Because Dreamina Design currently exposes no authoritative quote tool,
`auto_with_budget` stops at `QUOTE_UNAVAILABLE`. The user may instead approve
one fully specified `auto_exact_request`; that grants one submission only and
does not bypass the native paid-action approval in Dreamina Design.

1. **Inspect.** Call `inspect_scene(executable=codex-blender_adapter,
   scene=<user_scene>)`. Reject if the scene cannot be inspected.
2. **Specify preview.** Collect user-approved camera, frame range, output
   path, and dimensions. Build a `PreviewSpec`.
3. **Export.** Call `request_preview_export(...)` with the user's prompt
   metadata embedded in the request payload. Independent re-hash is
   performed by the orchestrator — never trust the producer's declared
   sha256 alone.
4. **Validate.** Run `validate_artifact(receipt, current_file)` from
   `scripts/handoff_validator.py`. On any error, transition the job to
   `Failed` with the classified `error_category`.
5. **Resolve readiness.** Use `McpDesignClient` to call
   `dreamina_cli_status` and `dreamina_account`. On user action required, stop
   with the returned remediation.
6. **Bind request.** Build `QuoteInputs(prompt, model, resolution, ratio,
   duration)` and the validated preview reference. Record that an authoritative
   quote is unavailable; never synthesize one.
7. **Authorize.** Require `auto_exact_request` (or a future authoritative
   quote within `auto_with_budget`) plus reference-upload and one-submit flags.
8. **Submit.** Let `McpDesignClient` call `dreamina_submit_video`; Dreamina
   Design obtains native approval internally. Persist `submit_id` before
   reporting `Submitted`.
9. **Query.** Let `McpDesignClient` call `dreamina_query_task` for the stored
   identifier and approved download root. `Unknown` is query-only.
10. **Download + verify.** Re-hash the downloaded artifact and compare to
    the declared hash; reject on mismatch.

## Ledger transitions

Drive the job through `Draft → DccSelected → PreviewSpecified →
PreviewValidated → CapabilityResolved → Quoted → Approved → Submitted →
Querying → Completed | Failed | Unknown` exactly once each.

## Never do

- Never resubmit a job whose `design_submit_id` is already set.
- Never skip the preview validation gate.
- Never send DCC scene data to the design plugin — only the validated
  artifact reference (artifact_id + sha256), the user prompt, and the
  quote inputs.
- Never use `scripts/design_handoff.py` for a production route. It is a
  fixture-only compatibility harness for deterministic tests.
