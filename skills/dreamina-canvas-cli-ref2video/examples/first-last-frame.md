# First-Last Frame — 首尾帧过渡

用户：「从这张花蕾图渐变到盛开图，6 秒。」（./bud.png ./bloom.png）

```bash
# 1. 三检 + discovery；本地校验两帧比例一致（不一致先裁/补）
dreamina-canvas --format json model list --type video

# 2. 有序上传
dreamina-canvas --format json resource upload --file "$PWD/bud.png"   --name "bud"    # → res:S
dreamina-canvas --format json resource upload --file "$PWD/bloom.png" --name "bloom"  # → res:E

# 3. first_last_frame 草稿（先首后尾；输出比例跟随首帧）
dreamina-canvas --format json node create video \
  --title "花开" \
  --prompt "花蕾逐渐绽放成盛开的花朵，自然舒展，光线渐亮" \
  --mode first_last_frame --model <model> \
  --ref res:<S> --ref res:<E> \
  --duration 6
# 模型支持且与首帧一致时可显式 --ratio；否则不传

# 4. 交接 quote-and-run → resume-operation → download-assets
```

要点：
- 只有首帧时去掉第二个 `--ref`，模式不变。
- 双帧源比例不一致会被 exit 2 拒绝；输出比例永远跟随**首帧**。
- 转场节奏由 prompt 控制（"快速切换" vs "缓慢过渡"）。
