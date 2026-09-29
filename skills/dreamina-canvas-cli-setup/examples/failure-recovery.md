# Failure Recovery — PATH 与升级排障

场景：装完 `dreamina-canvas: command not found`。

```bash
# 1. 最高发：PATH 未在当前 shell 生效 → 重开终端
# 2. 检查默认位置是否存在
ls -la ~/.local/bin/dreamina-canvas
# 3. 存在但不在 PATH → 按安装器提示加入（明示用户后执行）
export PATH="$HOME/.local/bin:$PATH"
dreamina-canvas --help
# 4. 不存在 → 重跑安装器
```

场景：命令行为与文档不符（schema 漂移）。

```bash
# 先升级再重试——问题可能已在新版本解决
curl -fsSL https://jimeng.jianying.com/canvas-cli/install.sh | bash
dreamina-canvas --format json version
dreamina-canvas --format json schema "<command path>"
```

场景：升级仍失败。

```bash
# 按指南四件套反馈：完整命令、完整报错、version 输出、requestId
dreamina-canvas version || echo "version 也不可用时，附安装器完整输出"
```
