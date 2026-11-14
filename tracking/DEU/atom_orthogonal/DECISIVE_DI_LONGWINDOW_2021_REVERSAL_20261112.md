# ★★重大认知修正：2021 不是「DEU 内部人死年」，是我的构造在 2021 死

日期：2026-11-12
触发：核查已提交 ACTIVE 件 `Vk65zLzG`（DEU/TOP500/D1，S 1.79 / F 1.69 / 2Y 2.07 / sub 1.44 / TO 12.0%，**checks fail=[] 全 PASS**）

## 一、Vk65zLzG 是什么

```
add(add(add(add(
  rank(ts_sum(ts_backfill(directional_indicator, 66), 252)),          # ← insiders 腿（1/5 权重）
  rank(ts_mean(predicted_surprise_f12m_ebitda_4, 5))),
  rank(ts_mean(predicted_surprise_pct_fy2_earnings_4, 22))),
  rank(ts_mean(mean_estimate_change_pct_f12m_ebitda_14d_4, 5))),
  rank(ts_mean(mean_estimate_change_pct_f12m_ebitda_90d_3, 22)))
```

设置：DEU/TOP500/**D1**/**decay 4**/SUBINDUSTRY/trunc 0.08/**nanHandling OFF**
塔归属：**DEU/D1/INSIDERS ×1.6 + DEU/D1/MODEL ×1.8**（effective 2）

## 二、逐年对照——2021 完全反向

| 年 | Vk65zLzG (DI 长窗族) | 我的 A/B/C/HHI 族 (mLapjPLX) |
|---|---:|---:|
| 2014 | 1.39 | 0.74 |
| 2015 | 2.77 | 1.81 |
| 2016 | 1.23 | 1.80 |
| 2017 | 1.46 | 0.88 |
| 2018 | 2.95 | 2.10 |
| 2019 | 1.12 | 2.39 |
| **2020** | **0.58** | **1.24** |
| **2021** | **2.91（全期最强）** | **−0.03（全期最弱）** |
| 2022 | 1.90 | 1.11 |
| 2023 | 1.67 | 3.06 |

## 三、三条修正

1. **「2021 是 DEU 内部人交易死年」的结论作废**。2021 是 `directional_indicator` 长窗构造**最强的一年（2.91）**。此前诊断（PnL 平滑下滑 −1.8%、无事件断点）只能说明「我的构造在 2021 失效」，不能说明「市场无信息」。
2. **失效机理**：2021 年 DEU 内部人交易的**方向性**（净买入/卖出）携带强信息，而「持仓变化 Δ66」被噪声淹没。⇒ 差分型腿在 2021 失效，水平/累积型腿在 2021 极强。
3. **互补性成立且已实证**：DI 长窗族弱在 2020（0.58），我的族强在 2020（1.24）；我的族弱在 2021（−0.03），DI 族强在 2021（2.91）。**两者正交**，组合理论上限高于任一单品。

## 四、我此前误判 DI 字段的原因

此前测 `directional_indicator` 用 **Δ66**（变化型）⇒ S 0.67、TO 55% 偏置 ⇒ 判「弱」。
正确用法是 **`ts_sum(ts_backfill(directional_indicator,66), 252)`**（年度净方向累积，水平型）。
⇒ 教训：**对累积型/水平型字段施加差分算子会摧毁信号**；字段的「矩」必须与字段语义匹配（DI 是流量累积 → 用 ts_sum 长窗；持仓是存量 → 用 Δ + ts_ir）。

## 五、同时被推翻的两个设置结论

`Vk65zLzG` 用 **nanHandling OFF + decay 4** 全闸通过（S 1.79）。此前我得出「decay 0 单调最优（8/8 臂）」与「nan ON 更好」，那是在**我的构造族内**成立，**不能外推到 DI 族**。⇒ 设置最优依赖构造族，必须按族重扫。

## 六、行动

1. **BE136**（已派 `4q6wYNZD4YmcgHazm4h9eV`，9 臂）：把 `directional_indicator` 长窗腿作为**第 4 正交维**并入 M0，扫 176/252/504 三窗 + 纯四腿版 + 去 cap 桶版。
2. 若有效，下一步按 「DI 族 × 我的族」权重配比扫（等权 / 2:1 / 1:2），并单独为 DI 族扫 nan/decay。
3. **self-corr 风险**：`Vk65zLzG` 已 ACTIVE 且 S 1.79。新件主体是 A/B/C/HHI（与它的 4 analyst 腿差异大），但共享 DI 腿，**提交前必须测 SELF_CORRELATION**。
