# Setup troubleshooting

| Symptom | Read-only check | Next step |
|---|---|---|
| `dreamina-canvas: command not found` | Inspect installer output and current PATH | Reopen terminal or apply the installer's stated PATH change with user authorization; rerun `--help` and `version` |
| Local login exists but command says unauthenticated | `dreamina-canvas auth account` and `auth status` | Complete a fresh browser authorization using the same profile; `auth account` is the server check |
| Unknown model or flag | `dreamina-canvas schema` and command `--help` | Use the installed binary's `model list` / `model find` shape, then its returned model value |
| A generation wait times out | `operation status <submitId> --project-id <projectId>` | Continue the original operation; do not submit again with a new ID |

Do not inspect or publish credential files. For a support report collect the complete command, error, `dreamina-canvas version`, and request ID if returned; redact sensitive values.
