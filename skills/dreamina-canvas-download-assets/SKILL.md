---
name: dreamina-canvas-download-assets
description: Use when an agent or script must verify the readiness of a generated Dreamina Canvas resource and download it to a user-approved path, producing a verifiable SHA-256 and byte count. Never persists signed URLs.
license: Complete terms in LICENSE
---

# Dreamina Canvas Asset Download

This Skill owns the final delivery step. It reads a `resourceId` from a
completed node, checks that the resource is ready, and downloads it to a
user-approved directory with a verifiable SHA-256.

Reference detail is in
[references/artifact-verification.md](references/artifact-verification.md).

## When to use

- The caller has a completed node and needs the underlying file(s).
- A previous download attempt failed partway and the caller needs to
  re-verify integrity.
- A user wants to inspect media metadata (duration, dimensions, codec)
  before opening the file.

## When **not** to use

- For re-running generation. That is `dreamina-canvas-quote-and-run`.
- For accepting user-uploaded files. The CLI's `resource` family is read
  / download only; uploads use a different flow and are out of scope here.

## The two-step delivery

```bash
# 1. Verify the resource is ready and read its stable facts
dreamina-canvas --format json resource get <resourceId> \
  --project-id "$PROJECT_ID"
# → readiness, byte count, media metadata, source nodeId

# 2. Atomic download into the user-approved directory
dreamina-canvas --format json resource download <resourceId> \
  --project-id "$PROJECT_ID" \
  --output "$USER_APPROVED_DIR"
# → canonical local path, byte count, SHA-256, media metadata
```

The download command writes via temp file + atomic rename and returns the
**final** size + SHA-256 from the on-disk file, not from a pre-flight
estimate. Trust only the post-write response.

## Output directory rules

- The output directory must be user-approved; the Skill never invents one.
- The directory must exist and be writable before calling
  `resource download`.
- The CLI writes to a canonical filename inside `--output`; it does not
  preserve the original remote filename.
- The download is atomic: a partial file will never appear in `--output`;
  either the file is complete with a verified checksum or nothing is left
  behind.

## What this Skill will not do

- Persist signed URLs, cookies, OAuth tokens, `storageId`, or provider
  task identifiers.
- Echo or log the response body's `signedUrl` / `downloadUrl` /
  `providerTaskId` fields, even when present; the Skill forbids
  persisting or echoing signed URLs in any form.
- Download into a directory the user has not explicitly named.
- Re-derive a `resourceId` from anything other than `node show` /
  `operation status` output; never guess.
- Treat a successful pre-flight `resource get` as proof of completion;
  the final word is the post-download SHA-256.

## Verification gate

The Skill considers a download successful only when:

- Exit code is 0.
- The returned `byteCount` matches `wc -c <path>` on the file.
- The returned `sha256` matches `shasum -a 256 <path>`.
- `media` metadata is present and consistent with the file's actual
  codec / dimensions (spot-check with `ffprobe` if available).

Any mismatch is treated as a hard failure; the file is quarantined (or
deleted if the caller prefers) and the user is informed.

## Policy

Invocation requires:
- Confirmed installation of dreamina-canvas
- A known lowercase resourceId and projectId
- A user-approved output directory

Forbids:
- Persisting signed URLs, storageId, OAuth tokens, cookies, or provider task IDs
- Downloading into a directory the user has not explicitly named
- Treating a pre-flight resource get as proof of download success
- Quarantining or deleting files without explicit user consent

Default prompt:

> Always verify the file after download via byte count + SHA-256. Use only
> the post-write response as truth. Never persist signed URLs or storage
> IDs.
>
