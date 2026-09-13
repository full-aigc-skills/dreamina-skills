# 即梦 CLI 官方安装到使用工作流

本参考以官方 v1.4.18 用户指南为能力基线，供 `dreamina-cli` 在首次安装、认证、
账户检查、生成、异步查询、下载、Session 管理、更新和故障排查时按需读取。
参数和模型仍以本机 `dreamina <subcommand> -h` 为运行时事实源。

## 权限和安全边界

- 安装、更新、登录态变更、Session 删除以及任何生成任务都可能改变本机或远端状态；
  执行前说明影响并取得用户明确授权。
- 图片和视频生成可能消耗会员权益或积分。提交前展示最终命令、模型、尺寸/分辨率、
  时长和数量，并再次确认消费范围。
- 不公开日志中的 OAuth 材料、设备码、用户标识或其他敏感信息。
- 视频首次生成若受合规限制，应让用户先在即梦网页端完成首次生成；不得绕过。

## 1. 安装、更新与发现 Skill

官方安装和更新入口相同：

```bash
curl -fsSL https://jimeng.jianying.com/cli | bash
```

执行前先取得安装或更新授权。完成后重新打开终端，或采用安装器明确输出的 PATH
命令，然后验证：

```bash
dreamina -h
dreamina version
```

若命令异常，优先更新 CLI 并重试原命令一次。官方指南对随 CLI 下载的 Skill 路径
存在 `~/.dreamina/dreamina/SKILL.md` 与 `~/.dreamina_cli/dreamina/SKILL.md`
两种写法；不要猜测，按以下顺序检查实际存在的文件，再复制到当前 Agent 可读取的
Skill 目录。复制、覆盖或安装 Skill 前仍须获得用户授权。

## 2. 登录、切换账号与账户自检

交互登录必须由用户在系统默认外部浏览器中完成网页授权：

```bash
dreamina login
dreamina user_credit
```

Agent 或无交互环境可发起 headless 登录，但必须把授权材料交给用户，不得代替用户
点击授权：

```bash
dreamina login --headless
dreamina login checklogin --device_code=<device_code> --poll=30
```

`--poll=0` 只检查一次。账号切换和退出会改变本地 OAuth 状态，先确认再执行：

```bash
dreamina relogin
dreamina logout
```

每次登录或重新登录结束后，都运行 `dreamina user_credit`，并明确报告成功、复用登录
态或失败。若 Agent 启动登录所得 URL 报“非法应用”，停止自动化登录，让用户先登录
即梦 Web，再在人工终端运行 `dreamina login` 并手动完成授权。

## 3. 生成能力全清单

执行任一生成命令前先运行对应的 `-h`，检查本地素材可读性，展示付费参数并取得
明确授权。以下命令族必须能够被识别并路由：

```bash
dreamina text2image --prompt="<prompt>" --ratio=1:1 --resolution_type=2k --poll=30
dreamina image2image --images=./input.png --prompt="<prompt>" --resolution_type=2k --poll=30
dreamina text2video --prompt="<prompt>" --duration=5 --ratio=16:9 --video_resolution=720p --poll=30
dreamina image2video --image=./first_frame.png --prompt="<prompt>" --duration=5 --video_resolution=720p --poll=30
dreamina frames2video --first=./start.png --last=./end.png --prompt="<prompt>" --duration=5 --video_resolution=720p --poll=30
dreamina multiframe2video --images=./a.png,./b.png --prompt="<prompt>" --duration=3 --video_resolution=720p --poll=30
dreamina multimodal2video --image=./input.png --audio=./music.mp3 --prompt="<prompt>" --model_version=seedance2.0fast --duration=5 --video_resolution=720p --poll=30
dreamina image_upscale --image=./input.png --resolution_type=2k --poll=30
```

命令覆盖标识：`dreamina text2image`、`dreamina image2image`、
`dreamina text2video`、`dreamina image2video`、`dreamina frames2video`、
`dreamina multiframe2video`、`dreamina multimodal2video`、
`dreamina image_upscale`。

具体模型、比例、分辨率、时长、批量和多帧 transition 约束，转到对应
`dreamina-cli-*` 执行 Skill；复杂模式由 `dreamina-cli-image2video` 覆盖。

## 4. 异步查询、下载和任务历史

保存每次提交返回的 `submit_id`。`querying` 仅表示已受理，不表示生成成功：

```bash
dreamina query_result --submit_id=<submit_id>
dreamina query_result --submit_id=<submit_id> --download_dir=./downloads
dreamina list_task --gen_status=success
```

轮询到 `success` 或 `fail` 为止；失败时报告 `fail_reason`。未知提交结果必须先按同一
`submit_id` 查询，不得盲目重新提交。下载后验证文件存在、媒体类型和尺寸。

## 5. Session 完整 CRUD

默认 Session 为 `0`。项目隔离需要先创建 Session，再把返回 ID 传给生成命令：

```bash
dreamina session create "<project_name>"
dreamina session list
dreamina session search "<keyword>"
dreamina session rename <session_id> "<new_name>"
dreamina session delete <session_id>
dreamina text2image --session=<session_id> --prompt="<prompt>" --ratio=16:9 --resolution_type=2k --poll=30
```

删除前展示目标 Session ID 和名称并取得明确授权；不得把默认 Session `0` 当作用户
指定的项目 Session。

## 6. 故障排查闭环

排查时依次收集并报告：

1. 完整执行命令。
2. 终端错误描述。
3. `dreamina version` 输出。
4. `~/.dreamina_cli/logs/` 下与该命令时间对应的最小日志片段。
5. 生成任务的 `submit_id`（如有）。

先删除或遮蔽敏感值。随后在获得授权后优先更新 CLI，重试同一命令一次。若仍失败，
带上述材料联系官方支持；业务问题和功能需求按官方指南联系 `@张成`。

常见分支：

- `dreamina: command not found`：重开终端，采用安装器输出的 PATH 指令，再检查安装。
- 未登录或无权限：先运行 `dreamina user_credit`。
- `AigcComplianceConfirmationRequired`：前往即梦 Web 完成授权确认，再重试。
- 长时间 `querying`：保存 `submit_id`，继续 `query_result`，不要重新提交。
