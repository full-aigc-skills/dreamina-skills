---
name: dreamina-3d-auto-seedance
description: Automatically turn a validated DCC preview into an approved Seedance video through Dreamina Design MCP, with submit-once recovery and verified download.
---

# Automatic Seedance Entry

Use when the user explicitly wants the validated Blender preview turned
into a final Seedance video automatically rather than opened in Jimeng Web.

## 能力边界说明

### ✅ 能做

- Validate the local preview receipt and current SHA-256.
- Discover live Dreamina capabilities/account readiness.
- Obtain action-time approval, submit once, query, download and verify.

### ⚠ 需要用户确认

- A paid request must have an exact model, resolution, duration and either an
  authoritative maximum-charge envelope or explicit `auto_exact_request`
  permission when Dreamina exposes no quote API.
- Dreamina authentication or Web compliance prerequisites may require user
  action.

### ❌ 超出范围

- Never send the `.blend` scene; send only the validated preview.
- Never resubmit after timeout or an unknown state.
- Never treat CLI exit zero or `querying` as Completed.

## Workflow

1. Require `PreviewValidated`; independently re-hash the local artifact.
2. Instantiate `McpDesignClient` over the host's MCP tool invoker. It may call
   only `dreamina_cli_status`, `dreamina_account`, `dreamina_submit_video`, and
   `dreamina_query_task`.
3. Build the exact `multimodal2video` request from live capability data.
4. Never invent a quote. If none is available, stop unless the exact request
   has `auto_exact_request` authorization; native paid-action approval still
   occurs inside `dreamina_submit_video`.
5. Call `dreamina_submit_video` once and persist its submit ID before reporting
   `Submitted`.
6. Call `dreamina_query_task` for the same ID until success, failure, or
   `Unknown`; unknown permits query-only recovery.
7. Download into the approved root, verify media metadata, bytes and SHA-256,
   then and only then transition to `Completed`.

## Privacy

Keep account identity, credentials, approval material and local absolute paths
out of the cross-plugin ledger. Persist non-secret hashes, submit IDs, states,
timestamps and error categories only.
