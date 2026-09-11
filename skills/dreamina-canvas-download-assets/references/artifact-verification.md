# Artifact verification

## Required verification gate

The Skill considers a download successful only when **all** of the
following hold for the file on disk after the CLI returns:

- The CLI returned exit code 0.
- `wc -c <path>` equals the `byteCount` reported in the response.
- `shasum -a 256 <path>` equals the `sha256` reported in the response.
- The `media` block in the response is consistent with the file's actual
  container / codec / dimensions (spot-check with `ffprobe` when the
  caller has it).

A mismatch is a hard failure. Quarantine or delete the file only after
explicit user consent; never silently.

## Atomic-write semantics

`resource download` writes via a temp file in the target directory and
atomically renames into place. Two consequences:

- A partial download never appears in the target directory.
- The response's `byteCount` and `sha256` are read **from the on-disk
  file**, not estimated up front.

Trust the post-write response. A successful `resource get` (pre-flight)
is informational; the verification gate runs on the post-write response.

## Resource ID format

`resourceId` is a lowercase canonical UUID only. The following are
rejected by the CLI with `cli.invalid_generation_reference` (exit code 2):

- Uppercase or mixed case UUIDs
- `urn:uuid:` prefix
- Hyphen-stripped UUIDs
- `resource_` prefix
- Internal short links like `image_xxx`, `video_xxx`, `audio_xxx`

If the caller has any of these, run `node show --node-id <nodeId>` to get
the canonical `resourceId` instead of guessing.

## Reference freezing (optional but useful)

If the caller wants to freeze a resource (instead of following the node),
the Element binding rules apply:

- Pass a bare lowercase UUID into `--main`, `--voice`, or `--auxiliary`
  to freeze (`bindingMode = frozen_resource`).
- Pass a bare `node_xxx` to follow the node (`bindingMode = follow_node`).
- Do **not** pass `node:` prefix to those slots; that returns
  `cli.invalid_resource_reference` (exit code 2).

This Skill does not perform the freezing itself; it documents the rule
because download may be the next step after a frozen binding.

## Failure → recovery

| Failure | requiredAction | What to do next |
|---------|----------------|-----------------|
| `resource get` returns exit 11 | `login` | Re-authenticate, then re-query. |
| `resource get` returns exit 2 on the resourceId | none | Fix the resourceId from `node show`; do not retry. |
| `resource download` writes a file but the post-write SHA-256 disagrees | `human_intervention` | Quarantine the file (with consent) and surface to the user; do not reuse the resourceId until the source is re-verified. |
| `resource download` returns exit 13 | `upgrade` | Upgrade the CLI per `error.clientUpgrade.upgradeUrl`. |
| Network interrupted mid-download | `retry` | Re-run; the atomic-write semantics ensure no partial file is left behind. |

## What this Skill will not do

- Persist signed URLs, `storageId`, `providerTaskId`, or any URL pointing
  at the underlying storage layer.
- Print the response body's URL fields even when present.
- Treat a successful `resource get` as proof of download success.
- Accept a directory the user has not explicitly named.
- Mutate or rename the downloaded file under a name the user has not
  approved.
