## Design

`dreamina-setup` is a small onboarding skill for `dreamina-canvas`, distinct from the classic `dreamina` CLI. It hands off ongoing authentication, command construction, and generation to the existing Canvas skills. The setup examples use the guide's three OS installer commands but require authorization before execution and verify the resulting binary rather than assuming installer success.

Existing `examples/happy-path.md` files receive task-specific command sequences. The entrypoint SKILL.md files already link to those examples, keeping the commands out of the always-loaded body. Generation examples show `--run --wait` as an *authorized later step* and a no-`--run` draft path. Model, ratio, resolution, duration, voice, resource and node identifiers remain placeholders resolved from live CLI outputs.

The package manifest and inventory tests include the new skill. A focused regression test checks onboarding coverage and guide-command examples; existing lint, package, CLI contract, and pytest gates remain in use.
