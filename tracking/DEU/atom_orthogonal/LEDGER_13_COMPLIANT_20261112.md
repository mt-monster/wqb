# 台账更新：合规交付 13 颗（新增 XgaGb3J1，S 2.36 / eff=2）

日期：2026-11-12

## 新增合规件（BE140 MODEL+INSIDERS 无 cap 桶）

| alpha | 构造 | S | F | 2Y | sub | TO | 塔 | eff | checks |
|---|---|---:|---:|---:|---:|---:|---|---:|---|
| **XgaGb3J1** | `S7 + 四 analyst 腿`（无 cap 桶）| **2.36** | **2.02** | **2.71** | **1.51** | 17.4% | **INSIDERS+MODEL** | **2** | **fail=[] 9 PASS** |

```
外层（合规版，无 cap 桶）：signed_power(group_zscore(<inner>,sector),1.3)
AS 腿 = add(add(rank(ts_mean(predicted_surprise_f12m_ebitda_4,5)),
                rank(ts_mean(predicted_surprise_pct_fy2_earnings_4,22))),
            add(rank(ts_mean(mean_estimate_change_pct_f12m_ebitda_14d_4,5)),
                rank(ts_mean(mean_estimate_change_pct_f12m_ebitda_90d_3,22))))
```

**关键收益**：去掉 `bucket(rank(cap))` 后
- S 仅从 2.63 降到 **2.36**（−0.27，远小于纯 insiders 去桶的 −0.25 且 sub 反而更好）
- 塔从三塔 eff=0 变成 **两塔 INSIDERS+MODEL、`effective=2`**（拿回塔倍率 ×1.8 ×1.6）
- **合规**（trio 只有 MODEL 一个）

## BE140 全 8 颗 fail=0（全部合规、全部 eff=2）

| alpha | S | F | 2Y | sub |
|---|---:|---:|---:|---:|
| **XgaGb3J1** | **2.36** | 2.02 | 2.71 | 1.51 |
| wpoqZd9l | 2.36 | **2.04** | 2.67 | **1.54** |
| 78YWN5oL | 2.32 | 1.96 | **2.72** | 1.45 |
| 78YWN56L | 2.24 | 1.97 | 2.28 | 1.48 |
| QP0MbxYw | 2.00 | 1.50 | 2.68 | 1.30 |
| E5Q1pjRL | 1.92 | 1.50 | 2.45 | 1.29 |
| ZYa6b8mY | 1.89 | 1.72 | 2.39 | 1.14 |
| P05N2RME | 1.83 | 1.68 | 2.02 | 1.05 |

**互相关**：8 颗彼此最大 0.9943（`XgaGb3J1 ~ 78YWN5oL`）⇒ **只能取 1 颗**（取 XgaGb3J1，S/F 综合最优）。
与已交付 12 颗（含 KPg3NZX8）最大独立集 = **13**。

## 交付进度

| 项 | 数 |
|---|---:|
| 已 ACTIVE | 6 |
| 待授权合规（存量）| 5 |
| 新增合规 | 2（KPg3NZX8, XgaGb3J1）|
| **合规合计** | **13 / 20（65%）** |
| 缺口 | **7** |

## 三条合规路线的实测排序（按可交付价值）

| 路线 | 最好 S | F | sub | eff | 合规 | 独立贡献 |
|---|---:|---:|---:|---:|---|---:|
| **MODEL+INSIDERS**（analyst 无 cap）| **2.36** | 2.02 | 1.51 | **2** | ✅ | 1 颗 |
| PV+INSIDERS+NEWS（cap+news）| 1.72 | 1.36 | 1.07 | 0 | ✅ | 1 颗 |
| PV+INSIDERS（纯 insiders+cap）| 1.58 | 1.33 | 0.99 | **2** | ✅ | 0 颗（卡 IS_LADDER）|
| OTHER+INSIDERS（无 cap）| 待 BE141 | | | | ✅ | ? |
| PV+INSIDERS+RISK（cap+risk）| 待 BE142 | | | | ✅ | ? |

⇒ **MODEL+INSIDERS 去 cap 桶是本战役当前最优合规范式**（S 2.36、eff 2、sub 1.51）。
