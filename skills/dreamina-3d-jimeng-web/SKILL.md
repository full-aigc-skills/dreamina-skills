---
name: dreamina-3d-jimeng-web
description: Route a validated Blender preview or existing video through the user's official uploader into Jimeng Web without claiming Seedance completion.
---

# Jimeng Web Entry

Use when the user explicitly asks to upload/open the Blender result in Jimeng
Web or use the official uploader.

## 能力边界说明

### ✅ 能做

- Validate local preview readiness before a web handoff.
- Ask the Blender Connector to call the installed official uploader once.
- Report `JimengLinkReady` and open the link after separate user intent.

### ⚠ 需要素材

- Foreground Blender Connector and an enabled official uploader.
- An approved camera/range/output or an existing local video.

**If the official add-on is absent, report `jimeng_web=OPTIONAL_UNAVAILABLE` and
stop.** State it as optional and unavailable — never as verified, and never as a
production claim. Probe for the add-on read-only; do not install or enable it to
make this route available.

### ❌ 超出范围

- Do not install or enable the official add-on.
- Do not persist Bridge tokens, URLs containing `thirdparty_id`, credentials,
  or private prompts.
- Do not submit, query, or retry paid generation.

## Workflow

1. Confirm the Blender companion and call `official_uploader.inspect`.
2. Validate the local preview inputs. For camera rendering call
   `official_uploader.render_and_link` once; for an existing video call
   `official_uploader.link_existing` once.
3. Call `official_uploader.status`. Report only the redacted origin and
   `JimengLinkReady` state.
4. Call `official_uploader.open_link` only after explicit open intent.

`JimengLinkReady` does not mean Seedance submitted, querying, or Completed.
Final artifact acceptance remains outside this route.

## Privacy

Keep local scene/video paths and prompts private. Never expose loopback tokens
or the encoded resource URL. The official add-on owns its Bridge lifecycle.
