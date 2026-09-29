# Boundary Refusal — 拒绝越权

## 场景 A：坚持用 i2v

用户：「就给我跑 `--mode i2v`。」

- Canvas 没有 `i2v` 模式；CLI 以退出码 2 拒绝，服务端别名
  `multi_modal` 同样被拒。
- 回复：单图走 `m2v`，有序首尾帧走 `first_last_frame`；由素材形态决定，
  不由旧习惯决定。

## 场景 B：跳过上传

用户：「`--ref` 直接写 `./product.png`。」

- 只接受 `node:` / `res:`；本地路径、`file://`、`uri:` 一律拒绝。
- 回复：先 `resource upload --file` 再冻结 `res:<uuid>`。

## 场景 C：双帧比例不一致也要硬跑

用户：「两张图比例不同，无所谓，直接生成。」

- 服务端拒绝双帧源比例不一致的请求（退出码 2）；输出比例跟随首帧。
- 回复：先裁/补到一致比例，或改为单帧 `m2v`。

## 场景 D：让本技能直接跑付费命令

任何附加 `--run` / `--credit-ceiling` / `--credit-token` 的请求一律
拒绝；付费边界属于 `dreamina-canvas-cli`。
