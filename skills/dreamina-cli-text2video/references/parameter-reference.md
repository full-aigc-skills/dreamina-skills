# text2video 参数参考（CLI v1.4.18）

| 参数 | 必填 | 取值/约束 |
|---|---|---|
| `--prompt` | 是 | 非空提示词 |
| `--video_resolution` | 是 | `seedance2.5` 支持 480p/720p/1080p；其他模型以运行时 help 为准 |
| `--duration` | 否 | Seedance 2.0 家族 4–15 秒；`seedance2.5` 4–30 秒；默认 5 |
| `--ratio` | 否 | 1:1、3:4、16:9、4:3、9:16、21:9；省略时默认 16:9 |
| `--model_version` | 否 | seedance2.0、seedance2.0fast、seedance2.0_vip、seedance2.0fast_vip、seedance2.0mini、seedance2.5 |
| `--session` / `--poll` | 否 | 非负数 |

```bash
dreamina text2video --prompt="镜头缓慢推进" --duration=5 --ratio=16:9 --model_version=seedance2.0fast --video_resolution=720p --poll=0
dreamina text2video --prompt="城市延时摄影" --duration=20 --ratio=16:9 --model_version=seedance2.5 --video_resolution=720p --poll=0
```

完整矩阵见
[`dreamina-cli` skill 的统一 v1.4.18 契约](https://github.com/full-aigc-skills/dreamina-skills/blob/main/skills/dreamina-cli/references/dreamina-cli-v1.4.18-contract.md)（如未安装：`npx skills add full-aigc-skills/dreamina-skills --skill dreamina-cli`）。
