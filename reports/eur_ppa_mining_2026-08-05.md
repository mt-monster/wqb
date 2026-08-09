# EUR 区域 PPA 挖掘报告 — ml_factor_proj 数据集

**日期**：2026-08-05
**区域/池/延迟**：EUR / TOP1200 / delay=1
**数据集**：`ml_factor_proj`
**目标**：从 EUR 选定数据集挖掘 3 个可提交 PPA（Power Pool Alpha）

---

## 1. 数据集选型依据

按 `wq-brain-ppa-mining` skill §1.0 前置硬门槛（coverage≥0.85、alphaCount≤50、fieldCount≥10）
在 EUR/TOP1200/delay=1 的 178 个数据集中筛选，`ml_factor_proj` 各项指标最优：

| 指标 | 值 | 门槛 | 判定 |
|---|---|---|---|
| coverage | 1.00 | ≥0.85 | ✅ 满分 |
| fieldCount | 333 | ≥10 | ✅ |
| alphaCount | 0 | ≤50 | ✅ 完全未开发 |
| userCount | 0 | — | ✅ 零竞争 |
| valueScore | 5.0 | — | 中上 |
| pyramidMultiplier | 1.5 | — | EUR 区最高档 |

**字段结构**（333 个字段全部为 MATRIX 类型、coverage 全 = 1.0）：

- `change_*` 基本面/价量变化率 243 个
- `mean_global_feature_0..39` 40 个（ML 潜因子均值）
- `log_variance_global_feature_0..39` 40 个（ML 潜因子对数方差）
- `change_*_active_return` 期限结构族 10 个窗口（1m/2m/3m/6m/9m/12m/18m/24m/36m/60m）

---

## 2. 回测执行记录

（本节由实际批次数据填充）

---

## 3. 结论与建议

（本节由实际批次数据填充）
