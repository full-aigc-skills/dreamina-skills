# Registering a local asset (`resource upload`)

`resource upload` is the **write** half of the `resource` family: it registers a
local file (or a server-reachable image URL) as a project resource and returns
the stable `resourceId` that every downstream reference uses.

Everything below is taken from the CLI's own `schema` output. That output is the
runtime authority; this document must not contradict it.

## Command shape

```bash
# Local file (image / video / audio)
dreamina-canvas --format json resource upload \
  --file "$LOCAL_PATH" \
  --project-id "$PROJECT_ID" \
  --resource-id "$STABLE_UUID" \
  --import-kind local_upload

# Server-reachable image only
dreamina-canvas --format json resource upload \
  --source-url "$PUBLIC_IMAGE_URL" \
  --project-id "$PROJECT_ID" \
  --resource-id "$STABLE_UUID"
```

Declared properties: `writes=true`, `reads=false`, `confirmation=false`,
declared exit codes `0, 2, 11, 12, 13, 21, 22, 1`.

## Flag contract

| Flag | Contract |
|---|---|
| `--file` | Local image, video, or audio path. Mutually exclusive with `--source-url`. |
| `--source-url` | Server-reachable **image** URL only. Mutually exclusive with `--file`. |
| `--type` | `image` \| `video` \| `audio`; overrides extension inference. |
| `--project-id` | Project UUID; omitted means the current project. |
| `--resource-id` | UUID idempotency key. Generated when omitted, **always echoed back as `resourceId`**; reuse the same value across process retries. |
| `--name` | Display name; omitted means the file name. |
| `--import-kind` | `local_upload` (default) \| `external_generated`. |

Passing both `--file` and `--source-url` is a contract violation, not a
precedence rule: the schema marks them mutually exclusive.

## The idempotency rule

`--resource-id` is the only identity this command exposes. Persist it **before**
the call and reuse it verbatim on every retry. When a response is ambiguous:

- Do **not** mint a fresh UUID to get past the ambiguity — that registers a
  second resource.
- Query `resource get <resourceId>` and reconcile by ID.

A repeated `--source-url` is not deduplicated by anything the schema declares;
only `--resource-id` carries the idempotency contract.

## After the upload

The returned bare `resourceId` is the frozen reference form:

- On a canvas: `res:<resourceId>` inside `--ref` or `{{res:<resourceId>}}`.
- In Element slots (`--main` / `--voice` / `--auxiliary`): pass it **bare**,
  without the `res:` prefix. Prefixing returns
  `cli.invalid_resource_reference` (exit code 2).

Uploading is **not** the same as attaching: the upload registers a resource, it
does not itself place anything on a canvas or trigger generation.

## `--import-kind` is a declaration, not a permission

`external_generated` records that the file came from another platform's
generator. It changes provenance metadata only. It does not bypass any
authorisation, does not make the asset trusted, and does not change pricing.

## Failure → recovery

| Failure | requiredAction | What to do next |
|---|---|---|
| Both `--file` and `--source-url` supplied | none | Drop one; they are mutually exclusive. |
| `--source-url` with a non-image payload | none | `--source-url` is image-only; use `--file` for video / audio. |
| Exit 11 | `login` | Re-authenticate, then reuse the same `--resource-id`. |
| Exit 2 on the argument set | none | Fix the argument; do not retry unchanged. |
| Ambiguous / timed-out response | resume | Query `resource get <resourceId>` with the persisted ID. Never mint a new ID. |
| Exit 13 | `upgrade` | Upgrade the CLI per `error.clientUpgrade.upgradeUrl`. |

## What this contract forbids

- Claiming `resource upload` is unavailable. It is part of the CLI 1.0.0
  `resource` family, alongside `resource get` and `resource download`.
- Treating `--import-kind external_generated` as an authorisation.
- Minting a second `--resource-id` to escape an ambiguous result.
- Promising that a `uri:` / `vid:` reference will resolve (see the SKILL.md
  boundary note).
