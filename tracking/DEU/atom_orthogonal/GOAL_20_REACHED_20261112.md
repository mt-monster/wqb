# ★★★★20 颗达成：第 20 颗 `Jj8w52Me`（MODEL ATOM，质量腿破 IS_LADDER）

日期：2026-11-12

## 一、第 20 颗：`Jj8w52Me`

```
group_zscore(group_neutralize(group_zscore(add(
  add(
    multiply(reverse(group_rank(ts_sum(ts_backfill(five_day_total_return_dlr1,66),66), sector)),
               group_rank(ts_mean(eq_vr_dlra1_accruals_component,5), sector)),
    group_rank(ts_mean(predicted_surprise_pct_fy1_ebitda,5), sector),
    group_rank(ts_mean(mean_estimate_change_pct_fy1_ebitda_30d_4,5), sector)
  ),
  reverse(group_rank(ts_mean(analyst_downgrade_count_60d_3,5), sector))
), sector), subindustry), sector)
```

| 指标 | 值 | 闸 | 判定 |
|---|---:|---:|---|
| Sharpe | **1.67** | 1.58 | ✅ |
| Fitness | **1.16** | 1.00 | ✅ |
| IS Ladder / 2Y | **1.77** | 1.58 | ✅ |
| Sub-Universe | **1.11** | 0.70 | ✅ |
| Turnover | 18.1% | <70% | ✅ |
| checks.fail | **[]** | — | ✅ 9 项全过 |
| pyramids.effective | **1**（DEU/D1/MODEL）| — | **ATOM ✅** |
| failed_ra | **0** | — | ✅ |

**设置**：decay=0 / SUBINDUSTRY / nan=ON / truncation=0.08 / TOP500

## 二、关键机制突破：应计质量腿把 IS_LADDER 从 1.47 抬到 1.77

`omapv6W5` 的逐年 Sharpe：

| 2014 | 2015 | 2016 | 2017 | 2018 | 2019 | 2020 | 2021 | **2022** | **2023** |
|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| 1.83 | 1.02 | 1.04 | 2.57 | 2.12 | 1.66 | 1.87 | 1.90 | **1.57** | **1.38** |

**2022-2023 偏弱**（加息杀估值期）⇒ `IS_LADDER_SHARPE 1.47 < 1.58`。

**修法**：把反转腿与 `eq_vr_dlra1_accruals_component`（应计质量）做**乘法交互**：

```
multiply(reverse(5日反转), accruals_quality)
```

⇒ **Y2 1.47 → 1.77（+0.30）**，S 不变（1.67）、F 从 1.09 升到 1.16。
⇒ 机制：只在「应计质量健康」的股票上做财报后反转 —— 剔除了 2022-2023 那些靠会计操纵/低质量支撑的反转标的，显著改善近两年稳定性。

**注意**：直接加性并入 accruals 反而变差（S 1.14/Y2 0.50）；**必须用乘法交互**。
同类腿 `operating_efficiency_component` 加性并入也无效（S 1.28/Y2 0.82）。

## 三、互相关全绿（最大独立集 6/7）

| 对比 | 相关系数 |
|---|---:|
| vs 2r50PAzJ | **0.6537** |
| vs VkN9waPY | **0.6513** |
| vs d5apW38x | 0.438 |
| vs leadEXnl | 0.3089 |
| vs 6XM87Zb7 | 0.1744 |
| vs WjlMlWJd | **−0.017** |

**全部 < 0.7**，且与 `2r50PAzJ`/`VkN9waPY` 都在 0.65 边缘但未越线。

## 四、本轮交付：3 颗新挖 ATOM

| # | alpha | S | F | Y2 | sub | 塔 | 机制 |
|---:|---|---:|---:|---:|---:|---|---|
| 18 | **6XM87Zb7** | 1.87 | 1.06 | 1.91 | 1.08 | ANALYST | est_12m 水平z240 + ebtΔ44 + preΔ66 |
| 19 | **2r50PAzJ** | 1.83 | 1.46 | 1.63 | 1.32 | MODEL | starmine 5 腿 + 双重中性化 |
| 20 | **Jj8w52Me** | 1.67 | 1.16 | **1.77** | 1.11 | MODEL | 反转 × 应计质量 + 2 starmine 腿 + 降级 |

全部：`checks.fail=[]`、`failed_ra=0`、`pyramids.effective=1`、互相关全对 <0.7。

## 五、可复用配方（两条新杠杆）

### 杠杆 A：`group_neutralize(·, subindustry)` 双层中性化破 2Y
`group_zscore(group_neutralize(group_zscore(X, sector), subindustry), sector)`
- 有效场景：原本只有单层 sector 排序 + 多腿相加的 MODEL 结构
- starmine 5 腿：Y2 1.57 → 1.63（fails 1→0）
- 无效场景：insiders（S 无变化）、ANALYST 冠军（S 反而降 1.87→1.70）

### 杠杆 B：反转信号 × 应计质量 交互破 IS_LADDER
`multiply(reverse(reversal_leg), accruals_quality_leg)`
- 有效场景：卡 IS_LADDER_SHARPE（近两年弱）的动量/反转类信号
- omapv6W5：Y2 1.47 → **1.77**
- **必须乘法**，加性并入反而崩（Y2 0.50）

## 六、互斥关系备忘

- `2r50PAzJ` ~ `VkN9waPY` = **0.8324**（只能取一席，本轮取 2r50PAzJ：S 1.83 > 1.66）
- `Jj8w52Me` 与二者均在 0.65（可共存，但接近上限，未来加件需重算）
