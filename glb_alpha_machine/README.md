# GLB Alpha Machine — 一二三阶流水线

## 概述

参考顾问 `machine_lib.py` + `Alpha Machine1.ipynb` 的代码,适配 **GLB / TOP3000 / SUBINDUSTRY** 区域的全自动一二三阶 alpha 挖掘流水线。

**核心增强**:每 10 个 pool(轮) 输出一次统计总结(完成率、用时、速率、错误数),写入 `glb_summary.log`。

## 流程

| 阶 | 输入 | 操作 | 候选数 | 输出 |
|---|---|---|---|---|
| 一阶 | GLB 字段(x 每数据集 top 15) | `get_first_order(fields, ops_set, "glb")` | ≤15000 | 模拟 → 每10轮总结 |
| 二阶 | 一阶 IS top 2000 → 取 top 300 | `group_neutralize/rank/normalize/scale/zscore(x, glb_groups)` | ~300×5×Ngroups | 模拟 → 每10轮总结 |
| 三阶 | 二阶 IS top 300 → 取 top 100 | `trade_when(open_events, x, exit_events)` | ~100×13×2 | 模拟 → 每10轮总结 |
| 检查 | 三阶 IS top 200 | `check_submission` | — | 可提交 GOLD |

## 目录结构

```
glb_alpha_machine/
├── glb_machine_lib.py    # 自包含库(顾问代码复刻 + 修复)
├── glb_pipeline.py       # 主流水线脚本
├── glb_summary.log       # 每10轮总结记录
├── log_glb_first.txt     # 一阶进度日志
├── log_glb_second.txt    # 二阶进度日志
├── log_glb_third.txt     # 三阶进度日志
└── cache/                # pickle 缓存(字段、候选、断点)
```

## 用法

```bash
# 先扫描 GLB 字段(快速,不模拟)
python glb_pipeline.py field_scan

# 仅跑一阶
python glb_pipeline.py stage1

# 仅跑二阶(需一阶已模拟)
python glb_pipeline.py stage2

# 仅跑三阶(需二阶已模拟)
python glb_pipeline.py stage3

# 检查可提交 alpha
python glb_pipeline.py stage4

# 全部顺跑
python glb_pipeline.py
```

所有阶段支持断点续跑(进度记录在 `log_glb_*.txt`)。

## 关键配置(改 `glb_pipeline.py` 顶部)

- `REGION = "GLB"` / `UNIVERSE = "TOP3000"` / `NEUT = "SUBINDUSTRY"`
- `FIRST_ORDER_MAX = 15000` — 一阶候选上限
- `FIELD_PER_DATASET = 15` — 每数据集取字段数
- `PICK_FIRST = 2000` / `PICK_SECOND_IN = 300` / `PICK_THIRD_IN = 100`
- `summary_every=10` — 每 10 个 pool 输出总结

## 顾问代码来源

- `D:/BaiduNetdiskDownload/WQ第五六节课代码/顾问参考代码/machine_lib.py`
- `D:/BaiduNetdiskDownload/WQ第五六节课代码/顾问参考代码/Alpha Machine1.ipynb`