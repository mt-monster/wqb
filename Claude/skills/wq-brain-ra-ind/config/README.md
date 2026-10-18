# IND 配置视图（config/）

> ⚠ **本目录不是事实源**。真身在 `tracking/IND/config/`；本目录只给**视图 + 差异说明 + 证据索引**。
> 原因：`wqb.profiles explain / render / sync-cells` 按 `tracking/<R>/config/` 解析，
> 覆盖值强制 `_evidence`；把真身搬进 skill 会复制事实源并断掉 profiles 链。
> 机器可读摘要见 [`region_view.json`](region_view.json)（改配置后须同步其 `as_of` 与要点）。

## 三表分工

| 表 | 管什么 | 真身 |
|---|---|---|
| `settings.json` | 区域固定仿真设置 + `_spre_*` 步 1 产物（排除族 / 正交方向 / win 配方 / prod 饱和） | `tracking/IND/config/settings.json` |
| `thresholds.json` | 审查阈值（review / near / quick_scan / probe_scoring / hard_gates） | `tracking/IND/config/thresholds.json` |
| `cells.json` | 组合级覆盖（区域 × 类别），每个覆盖须同级 `_evidence` | `tracking/IND/config/cells.json` |

```bash
$WQ_PY -m wqb.profiles explain --region IND --dataset <dataset>
$WQ_PY -m wqb.profiles check   --region IND
```
