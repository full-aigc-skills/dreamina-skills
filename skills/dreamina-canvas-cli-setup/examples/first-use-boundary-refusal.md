# 只读检查与安装边界

用户说“看看我的即梦画布能否使用”时，只检查 `command -v dreamina-canvas`、`dreamina-canvas --help`、`dreamina-canvas version` 和 `dreamina-canvas schema`。如果缺失，说明所需安装命令、来源与目标目录，等待用户明确要求安装；不因“检查”而运行安装器、登录或创建画布。
