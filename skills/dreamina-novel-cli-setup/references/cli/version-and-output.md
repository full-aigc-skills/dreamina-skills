# CLI 版本与结果判读

基线：本机 `jimeng-novel version` 为 1.0.1。未来版本重新读取当前命令 `--help` 和 `schema get`。自动化读取 `-j` 的 status、data、error、context；`running` 保留任务身份继续查询；任何未知错误先看 hint，绝不盲目重提。
