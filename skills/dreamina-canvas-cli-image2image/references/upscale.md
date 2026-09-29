# 图片放大

## Image upscale

`node upscale image` creates a new node and never overwrites the source. It is
a separately priced operation with an upscale-scoped approval token; a token
from `node confirm` is invalid here.

```bash
# Local-only validation
dreamina-canvas --format json node upscale image \
  --node-id <sourceImageNodeId> --mode pro --resolution 2K --dry-run

# After showing the live quote and receiving an exact ceiling approval
dreamina-canvas --format json node upscale image \
  --node-id <sourceImageNodeId> --submit-id <stableUuid> \
  --mode pro --resolution 2K --credit-ceiling <approvedCeiling> --wait
```

`--detail` is accepted in `pro` mode only; confirm it in
`schema` before passing it — never carry it into
non-pro modes.

Persist one stable `submitId` per source before execution. On exit 20 or 21,
query or retry with the same ID; never substitute a new identity.



参数与模型以当前 `node upscale image --help` 为准；保留同一 submitId 查询恢复。
