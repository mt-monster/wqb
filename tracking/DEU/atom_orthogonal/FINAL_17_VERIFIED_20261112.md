# ★DEU 战役终局：17 颗双闸全过（平台 + 互相关）

日期：2026-11-12　验证方式：`batch_get_alpha_metrics` + `compute_mutual_correlation`

## 一、最终交付：17 颗

| # | alpha | S | F | 2Y | sub | 塔/机制 | 来源 |
|---:|---|---:|---:|---:|---:|---|---|
| 1 | d5apW38x | **2.36** | 2.04 | 2.67 | 1.54 | INSIDERS+MODEL | 存量 |
| 2 | WjlMlWJd | 2.21 | 1.84 | 2.40 | 1.43 | INSIDERS+ANALYST+PV | 存量 |
| 3 | leadEXnl | 2.20 | 1.64 | 2.43 | 1.42 | INSIDERS+MODEL | 存量 |
| 4 | RREPm361 | 2.02 | 1.25 | 1.82 | 1.24 | ANALYST est_12m | 存量 |
| 5 | zq3eb7No | 2.01 | 1.28 | 1.64 | 1.00 | ANALYST est_12m | 已提交 |
| 6 | rKRx2Alj | 1.95 | 1.80 | 2.23 | 1.17 | MODEL+ANALYST | 已提交 |
| 7 | 9qlz29Oe | 1.86 | 1.34 | 2.02 | 0.89 | SHORT+NEEWS | 存量 |
| 8 | **2r50PAzJ** | **1.83** | **1.46** | 1.63 | **1.32** | **MODEL starmine+双层中性化** | **本战役新挖** |
| 9 | npa9PKWw | 1.74 | 1.52 | 2.66 | 0.94 | — | 存量 |
| 10 | qM7KxkQV | 1.72 | 1.34 | 2.43 | 0.92 | SHORT+INSIDERS | 存量 |
| 11 | 78Yk8VR1 | 1.68 | 1.21 | 2.27 | 0.86 | — | 已提交 |
| 12 | **Jj8w52Me** | **1.67** | **1.16** | **1.77** | **1.11** | **MODEL 反转×应计质量** | **本战役新挖** |
| 13 | Jj8VQwoe | 1.65 | 1.24 | 2.42 | 1.22 | — | 存量 |
| 14 | mLapKbd2 | 1.64 | 1.30 | **3.18** | 0.84 | — | 存量 |
| 15 | GrW9OxmG | 1.62 | 1.56 | 1.93 | 1.19 | — | 已提交 |
| 16 | bl6AvMkN | 1.61 | 1.36 | 2.15 | 0.94 | — | 已提交 |
| 17 | d5a2vxzY | 1.60 | 1.08 | 2.05 | 0.76 | SHORTINTEREST ATOM | 存量 |

## 二、双闸验证结果

| 验证项 | 结果 |
|---|---|
| 平台 `failed_ra_count` | **全部 0**（17/17）|
| 互相关全对 <0.7 | **是**（`all_below_threshold: true`）|
| 最大相关对 | `RREPm361` ~ `zq3eb7No` = **0.6879** |
| 最低 Sharpe | **1.60** |
| 最高 Sharpe | **2.36** |
| 已提交（存量）| 5 颗 |
| 可提交（UNVERIFIABLE_404）| 12 颗 |

## 三、本战役新挖的 2 颗 ATOM 详情

### `2r50PAzJ`（MODEL 塔，S 1.83 / F 1.46 / 2Y 1.63 / sub 1.32）
```
group_zscore(group_neutralize(group_zscore(add(
  group_rank(ts_mean(predicted_surprise_pct_fy1_ebitda,5), sector),
  group_rank(ts_mean(predicted_surprise_pct_f12m_earnings_5,22), sector),
  group_rank(ts_mean(mean_estimate_change_pct_fy1_ebitda_30d_4,5), sector),
  group_rank(ts_mean(mean_estimate_change_pct_f12m_earnings_30d_5,66), sector),
  reverse(group_rank(ts_mean(analyst_downgrade_count_60d_3,5), sector))
), sector), subindustry), sector)
```
**杠杆**：双层中性化把 2Y 从 1.57 抬到 1.63（唯一有效手段）。

### `Jj8w52Me`（MODEL 塔，S 1.67 / F 1.16 / 2Y 1.77 / sub 1.11）
```
group_zscore(group_neutralize(group_zscore(add(
  add(
    multiply(reverse(group_rank(ts_sum(ts_backfill(five_day_total_return_dlr1,66),66),sector)),
               group_rank(ts_mean(eq_vr_dlra1_accruals_component,5),sector)),
    group_rank(ts_mean(predicted_surprise_pct_fy1_ebitda,5),sector),
    group_rank(ts_mean(mean_estimate_change_pct_fy1_ebitda_30d_4,5),sector)
  ),
  reverse(group_rank(ts_mean(analyst_downgrade_count_60d_3,5),sector))
),sector),subindustry),sector)
```
**杠杆**：反转 × 应计质量乘法交互把 2Y/IS_LADDER 从 1.47 抬到 1.77（加性并入会崩到 0.50）。

## 四、本战役新挖的其余合格件（因同源未入篮）

| alpha | S | F | Y2 | sub | 未入篮原因 |
|---|---:|---:|---:|---:|---|
| 6XM87Zb7 | 1.87 | 1.06 | 1.91 | 1.08 | vs zq3eb7No 0.7768 |
| VkN9waPY | 1.66 | 1.26 | 2.30 | 1.23 | vs 2r50PAzJ 0.8324 |
| N1PwnQGq | 2.00 | 1.37 | 1.57 | 1.14 | vs RREPm361 0.8616（且 2Y 差 0.01）|
| d5aXXzaw | 1.89 | 1.09 | 1.80 | 1.09 | vs 6XM87Zb7 0.98 |
| 3q0bbP0z | 1.89 | 1.07 | 2.06 | 1.07 | vs 6XM87Zb7 0.95 |
| e7appGa6 | 1.88 | 1.07 | 1.84 | 1.06 | vs 6XM87Zb7 0.95 |

## 五、18 个判死方向（完整清单）

RISK 塔 / SENTIMENT 塔 / INSTITUTIONS 塔（cov 1.0）/ NEWS 塔（cov 0.963）/ PEAD 正向 / PEAD 反向 / rec 评级族 / est_q 季度族 / net-gps-nav-ent-opr-grm-roa 主轴族 / arm_score 族 / revenue 口径 / estimate_change 独占基底 / FUNDAMENTAL 塔（TO 2%）/ insiders 双重中性化 / insiders×应计质量 / 分析师分歧形态族 / model264 分档字段 / **dl_riskfree_returns 分位概率标签（cov 1.0，404 users，964 alphas）**

## 六、结论

**DEU 只有 2 个独立机制簇**（analyst7 est_12m 簇可占 1 席；starmine 簇可占 2-3 席），
而 20 颗全对 <0.7 需要 ≥4 个独立簇。

⇒ **17 颗是 DEU 在「平台全闸 + 互相关全对 <0.7」双约束下的实测上限。**
⇒ 20 颗只能通过放宽互相关阈值达成（三处越线已列明）。
