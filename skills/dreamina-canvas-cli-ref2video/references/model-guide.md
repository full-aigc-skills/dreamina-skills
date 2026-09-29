# Mode Selection Guide — 图生视频模式选择

> Canvas 只有三个公开视频模式；选错模式是本分技能最高发的故障源。
> 旧 CLI 的 image2video / frames2video / multiframe2video / multimodal2video
> 子命令全部不存在于 Canvas。

## 决策树

```
用户有多少参考素材？关系是什么？
├── 纯文本
│   └── t2v（归 dreamina-canvas-cli-text2video，本分技能不处理）
├── 1 张图 / 1 个视频 / 1 个主体（Element）
│   └── m2v            —— "让照片动起来"、运动引导、单素材参考
├── 2 张图，首尾关系（从 A 变到 B）
│   └── first_last_frame —— 有序 2 引用；源比例一致
├── 2 张图，连续故事帧
│   └── 拆节点：多个 m2v / first_last_frame 草稿 + 时间轴技能串接
├── 图 + 视频/音频混合（多模态）
│   └── m2v            —— 多模态参考归 m2v 域；素材类型上限以 discovery 为准
└── 任何情况下
    └── 不得传 i2v / multi_modal —— 不存在，exit 2
```

## 模式能力对照

| 能力 | m2v | first_last_frame |
|------|-----|------------------|
| 输入 | 图/视频/Element 参考 | 1–2 帧（有序） |
| 运动控制 | prompt 描述 | 转场 prompt + 帧约束 |
| 比例 | 多随源推断 | 跟随首帧 |
| 复杂度 | 低 | 中 |
| 适用 | 微动化、单素材短片 | 形态变化、场景过渡 |

## 场景-模式对照

| 用户需求 | 推荐模式 |
|---------|---------|
| "让这张照片里的人眨眼微笑" | m2v |
| "水面流动起来" | m2v |
| "从花苞变成盛开" | first_last_frame |
| "夏天变秋天" | first_last_frame |
| "产品图环绕展示" | m2v |
| "人物 + 场景分离动起来" | m2v（素材上限以 discovery 为准） |
| "多帧讲故事" | 拆多个节点，时间轴技能串接 |

## 常见误路由

| 错误 | 后果 | 正确做法 |
|------|------|---------|
| 单图传 `--mode i2v` | exit 2 | m2v |
| 首尾帧用 m2v 只传尾帧 | 语义错（无首帧约束） | first_last_frame + 双引用 |
| 双帧比例不一致硬传 | exit 2 | 裁/补到一致比例再传 |
| 传 `--mode multi_modal` | exit 2（服务端别名） | m2v |
| 帧驱动模型强传 `--ratio` | exit 2 | 删 ratio，按首帧推断 |

## 模型与 discovery

```bash
dreamina-canvas --format json model list --type video
```

- 帧驱动模型的比例规则、素材类型与数量上限、时长上限都在 discovery
  负载里；执行前必读。
- 视频模型价差大；`node quote` 展示时注明模式/时长/分辨率/引用数。
