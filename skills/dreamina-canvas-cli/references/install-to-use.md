# dreamina-canvas installation and update

Installation or update changes the user's machine. Explain the source and
target directory, then obtain explicit authorization before running either
installer.

Domestic public build:

```bash
curl -s https://jimeng.jianying.com/canvas-cli | bash
```

Overseas public build:

```bash
curl -fsSL https://lf3-static.bytednsdoc.com/obj/eden-cn/psj_hupthlyk/ljhwZthlaukjlkulzlp/dreamina_canvas_cli_oversea/install.sh | bash
```

To choose a target directory, set `DREAMINA_CANVAS_INSTALL_DIR` or the
compatible `INSTALL_DIR` only to a user-approved path. Do not silently change
shell startup files.

After installation or update, verify the actual artifact:

```bash
dreamina-canvas --help
dreamina-canvas --format json version
dreamina-canvas --format json schema
```

The installer output and live `version`/`schema` responses are authoritative.
Do not claim readiness from the download exit code alone.
