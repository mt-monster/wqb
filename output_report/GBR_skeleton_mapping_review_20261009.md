# 审核点②：「语义 → 骨架族」映射表（数据实证版，待你裁决）

> 2026-10-09 ｜ 依据：GBR 全部 2,614 条实测，按「sem_type × 骨架族」交叉出 **实测 maxS 矩阵**。
> 结论先行：**我初版的 `SEM_PREFERRED` 有一半格子被数据推翻** —— 最刺眼的三处：
> ① `delta`（时序差分）在 6 类语义上都是最强族，我初版却几乎没给它首位；
> ② `ts_rank`/`ts_zscore` 在我初版里占位很多，实测几乎处处弱；
> ③ `count` 的最强形态根本不是单字段骨架，而是**对偶字段差** `subtract(rank(raised), rank(lowered))`。

---

## 一、实测矩阵（maxS，括号=条数，★=出过 ALIVE）

| sem_type | delta | level_rank | subtract | gn_first | quantile | decay_linear | av_diff | double_window | ts_rank | ts_zscore |
|---|---|---|---|---|---|---|---|---|---|---|
| **count** | 1.35(65) | 1.36(42) | **★1.96**(138) | ★1.95(28) | **★1.96**(43) | ★1.90(14) | · | 0.11(2) | ★1.66(8) | 0.71(14) |
| **ratio** | **★2.15**(151) | ★1.62(43) | 0.39 | ★1.62(3) | ★1.78(7) | ★1.73(8) | **★2.02**(83) | · | 0.86(3) | · |
| **estimate_level** | **★1.90**(136) | ★1.78(57) | ★1.58(16) | 1.57(10) | 1.57(1) | 1.37(2) | 1.06(1) | · | ★1.79(23) | ★1.60(3) |
| **probability** | **★1.80**(122) | 1.41(36) | 0.95 | 1.24(1) | · | 1.36(2) | 1.48(16) | · | ·(0) | 0.49(1) |
| **percentile** | **★2.61**(50) | ★1.63(47) | 0.48 | **★1.91**(44) | 1.00(2) | ★1.60(9) | 0.85(9) | ★1.71(7) | 0.49(2) | 1.02(3) |
| **score** | 0.92(36) | **★1.61**(53) | 0.51 | 0.39 | ·(未试) | −0.22 | 0.75 | 0.19 | 1.25(7) | 0.00(3) |
| **level_amount** | **★1.78**(28) | 1.04(15) | 0.41 | · | 0.59(4) | · | 0.73(8) | 0.02(1) | −0.32(1) | 0.65(29) |
| **sentiment** | 0.57(7) | 1.40(30) | 0.35 | −0.24 | **★1.75**(6) | −0.60 | −0.51 | · | 0.35(3) | 0.22(5) |
| **revision_change** | 0.30(15) | **★1.62**(23) | · | 1.16(2) | 0.40(2) | 1.50(3) | · | · | 0.87(3) | · |
| **dispersion** | 1.01(16) | 0.54(15) | 0.75 | · | · | · | −0.73 | · | · | · |
| unknown（兜底） | 1.17(66) | ★1.68(73) | 1.49(37) | ★1.75(8) | ★1.76(12) | ★1.77(26) | 1.09(14) | 0.51(15) | 0.88(1) | 1.39(1) |

> 数据说明：同一格子可能由少数数据集主导（如 percentile×delta 的 2.61 来自 model38）；Phase 4 会用复活补测后的新数据重估。

---

## 二、初版 vs 数据：逐格对照（⇒ 为建议修订）

| sem_type | 初版（我拍的） | 实测证据 | ⇒ **v2 建议** | 置信 |
|---|---|---|---|---|
| count | gn_first / level_rank / delta | `subtract 对偶差` 1.96 与 `quantile` 1.96 并列最强；**level_rank 只 1.36** | **subtract_pair → quantile → gn_first → decay_linear** | 实证强 |
| ratio | level_rank / ts_rank / decay_linear | **delta 2.15、av_diff 2.02 远超 level_rank 1.62；ts_rank 0.86 弱** | **delta → av_diff → quantile → level_rank** | 实证强 |
| percentile | level_rank / decay_linear / gn_first | **delta 2.61 全矩阵最高**；gn_first 1.91、double_window 1.71 | **delta → gn_first → double_window → level_rank** | 实证强 |
| estimate_level | delta / level_rank / ts_zscore | delta 1.90 ✓；**ts_rank 1.79(n=23) > ts_zscore 1.60(n=3)** | **delta → ts_rank → level_rank**（微调次序） | 实证 |
| probability | level_rank / ts_rank / decay_linear | **delta 1.80 最强；ts_rank 从未试过** | **delta → level_rank → av_diff** | 实证 |
| score | level_rank / ts_rank / quantile | level_rank 1.61 是唯一出过 ALIVE 的族；quantile 未验证 | **level_rank → ts_rank**（quantile 标「待证」） | 实证 |
| level_amount | ts_zscore / ts_rank / delta | **数据直接打脸**：delta 1.78 强、ts_zscore 0.65(n=29) 弱、ts_rank −0.32 | **delta → level_rank**（ts_zscore 降为对照族） | 实证强 |
| sentiment | delta / ts_zscore / level_rank | **quantile 1.75 是唯一 ALIVE 族**；delta 0.57 弱 | **quantile → level_rank**（delta 降级） | 实证 |
| revision_change | level_rank / delta / ts_rank | level_rank 1.62 ✓；decay_linear 1.50；**delta 0.30 弱** | **level_rank → decay_linear → ts_rank** | 实证 |
| dispersion | level_rank / ts_rank / decay_linear | 无任何族出过 ALIVE（delta 1.01 最高） | **delta → divide**（全族标「低置信待证」） | 弱 |
| unknown | level_rank / delta / ts_rank | gate 2.07、decay_linear 1.77、quantile 1.76、gn_first 1.75、level_rank 1.68 都出过 | **level_rank → delta → decay_linear → gate**（兜底多配一族） | 中 |

---

## 三、★ 映射表之外的两个结构性发现（需要你裁决）

**① `count` 语义的最强形态是「对偶字段差」，不是单字段骨架。**
`subtract(rank(est_12m_pre_raisednum_4wks), rank(est_12m_pre_lowerednum_4wks))` 这类构造 S1.96，
而同一字段的单字段 level_rank 只 1.36。⇒ **count 语义的字段若存在 `raised/lowered`、`up/down` 对偶字段，
应优先生成对偶差**，单字段骨架降为补充。这需要 `skeleton_panel gen` 支持「对偶字段配对」（当前不支持）。

**② 「门控 gate」族被低估了。**
`unknown×gate = 2.07(n=95)`、`percentile×gate = 2.37(n=5)` —— 但在我的初版映射里 gate 一族都没进。
⇒ v2 建议把 `gate`（trade_when 门控）加入 unknown/percentile 的优选族。

---

## 四、请你裁决的三件事

1. **v2 映射表整体**是否认可（上表「⇒ v2 建议」列）？哪个格子要改？
2. **对偶差配对**：count 语义是否按「对偶字段差优先」执行（我同步给 `gen` 加配对支持）？
3. **gate 族**是否正式进入优选族（unknown / percentile 两类）？

确认后我将：更新 `SEM_PREFERRED` → 重跑 `gap-report` 生成 v2 缺口 → 进入审核点③（闸门阈值）→ 审核点④（3a 复活清单）。
