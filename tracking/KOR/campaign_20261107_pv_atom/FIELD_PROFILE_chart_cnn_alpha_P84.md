# 字段画像：chart_cnn_alpha / pattern_scores（KOR / TOP600 / D1）

生成时间：2026-11-08 · 战役：KOR 10 颗 ATOM REGULAR · 类别：未开采类别开荒（P84）

## 一、数据集级画像

| 维度 | chart_cnn_alpha | pattern_scores |
|---|---|---|
| category | model | pv |
| 字段数 | 1010（全 MATRIX） | 504（全 MATRIX） |
| coverage | 0.885（族内 0.90–0.97） | 1.000 |
| alphaCount | 34 | 49 |
| userCount | 25 | 22 |
| tier / score | tier1 / 0.914 | tier1 / 0.930 |
| 形态 | CNN 图像模型的分位概率 / 置信度 | 技术形态相似度得分 |
| 拥挤度判读 | 极低（aC34 / uc25） | 极低（aC49 / uc22） |

**为什么选 chart_cnn_alpha 优先**：其命名族与 ASI 区已验证出全绿 alpha（S2.11 / prod0.68）的 probability_label 分位概率骨架同源；
本区 13 个完整五分位概率族可直接复刻「分位概率价差 + 短窗 ts_rank + 大 decay」配方，这是本战役中唯一有跨区正面先验的结构。

## 二、chart_cnn_alpha 字段族结构

字段名文法：模型族 x 期限 x 分位档 x 统计量。

- 模型族：equity_star1b1 / equity2b2 / eqstar4 / leapstar1 / leapstar4b1 / leap_star3 / leapstar6 / malta_star1 / malta_star2b1 / maltastar2 / malta1 / malta2 / malta3 / equity_star6
- 期限桶（按字段数）：60d(209) / 50d(90) / 5d(57) / 40d(52) / 20d(52) / 100d(51) / 80d(50) / 30d(45) / 120d(38) / 10d(38) / 180d(24) / 200d(19) / 70d(19)
- 统计量：prob{k}（落在第 k 分位的概率）、confscore{k}（该分位置信度）、label（硬标签）、rank（预计算期望分位）、bucket{k}（分桶概率）

### 13 个「完整五分位」概率族（可直接构价差，无需补字段）

| 族 | 期限 | 5 档字段名模板 |
|---|---|---|
| imgpred_eqstar4_60dret_q5 | 60d | imgpred_eqstar4_60dret_q5_prob0..4（另 confscore0..4、label） |
| cnn_predicted_prob_q5_bucket*_50d_equity2b2 | 50d | cnn_predicted_prob_q5_bucket0..4_50d_equity2b2 |
| cnn_predicted_prob_q5_bucket*_60d_equity2b2 | 60d | cnn_predicted_prob_q5_bucket0..4_60d_equity2b2 |
| img_leapstar4b1_50d_qtile5 | 50d | img_leapstar4b1_50d_qtile5_prob0..4 |
| img_leapstar4b1_70d_qtile5 | 70d | img_leapstar4b1_70d_qtile5_prob0..4 |
| img_maltastar2_20d_qtile5 | 20d | img_maltastar2_20d_qtile5_prob0..4 |
| img_maltastar2_80d_qtile5 | 80d | img_maltastar2_80d_qtile5_prob0..4 |
| img_pred_leap_star3_80d_5bucket | 80d | img_pred_leap_star3_80d_5bucket_prob0..4 |
| img_pred_leap_star3_120d_5bucket | 120d | img_pred_leap_star3_120d_5bucket_prob0..4 |
| img_pred_malta3_60d_5bucket | 60d | img_pred_malta3_60d_5bucket_prob0..4（另 rank） |
| img_pred_malta3_180d_5bucket | 180d | img_pred_malta3_180d_5bucket_prob0..4 |
| img_equity_star1b1_rank10_quantile5 | 10d | img_equity_star1b1_rank10_quantile5_prob0..4 |
| img_equity_star1b1_rank60_quantile5 | 60d | img_equity_star1b1_rank60_quantile5_prob0..4 |

另有 leaps 家族五分位：img100d_return_quintile0..4_prob_leap1、img200d_return_quintile0..4_prob_leap1、
以及 probability_rank5_next60d_return_p0..4_{equity_star6,leap_star1}（已是 rank 口径）。

## 三、pattern_scores 字段族结构

字段名文法：形态名 x 统计量 x 回看窗。

- 统计量：mean / min / max / std / median / quantile95 / dynamic / adaptive / avg
- 回看窗：lookback60 / lookback120
- 形态（按字段数）：reversal_v_top / symm_triangle_down / asc_triangle / common_gap_down / cont_falling_wedge / desc_triangle_up / breakaway_gap_up / common_gap_up / cont_rising_wedge / falling_wedge / rising_wedge / reversal_v_bottom / desc_triangle / cont_v_bottom 等 30+ 个

**降级预警（跨数据集证据）**：同为「图表形态相似度」家族的 continuation_score（560 字段 / cov1.0 / aC56）本轮已测，10 个代表形态最高 S 仅 0.94（median_similarity_cup_handle），多数 0.1–0.6。
pattern_scores 与本集同构，先验偏弱；本轮只在 chart_cnn_alpha 试完后有余量再探。

## 四、模板库（12 个结构互异 · P84 实发）

标注来源：forum = 平台论坛/跨区实证记忆；paper = 外部文献机制；self = 自建。

| # | 模板 | 结构轴 | 核心表达式骨架 | 来源 |
|---|---|---|---|---|
| T1 | 分位概率价差 | 一阶水平差 | subtract(group_rank(prob4,g), group_rank(prob0,g)) | self |
| T2 | 短窗 ts_rank + 大 decay | 时序秩 + 平滑 | group_rank(ts_rank(spread, W_short), country) | forum（ASI 破 prod 配方） |
| T3 | 一阶差分 | 变化量 | group_rank(ts_delta(spread, 22), g) | self |
| T4 | 跨期限结构差 | 期限维度差 | prob4(60d) - prob4(180d) | paper（预测期限结构） |
| T5 | 置信度加权概率 | 概率 x 置信度 | group_rank(multiply(prob4, confscore4), g) | self |
| T6 | 预计算期望分位 | 直接读 rank 字段 | group_rank(ts_rank(*_rank, 10), country) | self |
| T7 | 预测不稳定（二阶） | 方差 | subtract(0.5, group_rank(ts_std_dev(spread, 22), g)) | self |
| T8 | 跨模型一致性 | 模型维度差 | prob4(模型A) - prob4(模型B) | self（ensemble disagreement） |
| T9 | leaps 五分位跨档差 | 一阶水平差（另一模型族） | quintile4 - quintile0 | self |
| T10 | rank 加速度 | 秩的二阶差分 | ts_delta(ts_rank(prob4, 22), 22) | self |
| T11 | 长窗 leaps 五分位差 | 一阶水平差（200d） | quintile4 - quintile0 | self |
| T12 | 单腿水平 | 纯水平 | group_rank(prob4, g) | baseline |

## 五、P84 派发记录

| 批 | multisim id | 设置 | 条数 | 模板 |
|---|---|---|---|---|
| P84A | JEO8qff54zEcscjjKG1ryt | decay4 / trunc0.08 / REVERSION_AND_MOMENTUM / industry | 8 | T1 T4 T5 T8 T9 T11 T12 T3 |
| P84B | 3DddQc6kL4QJc9z1fLp6UlUD | decay22 / trunc0.08 / REVERSION_AND_MOMENTUM / country | 8 | T2 T6 T2(W5) T10 T7 T9+rank T1(equity2b2) T1(star1b1) |

算子数全部落在 2–4，远低于 12 上限。

## 六、工具坑（本轮新增）

- validate_expressions 的参数键是 alpha_expressions（不是 expressions）。
- validate_expressions 不读取调用方 region，硬编码按 USA/TOP3000 取字段表，KOR 字段一律被判 unknown_fields；本区字段存在性只能以 get_datafields(region=KOR) 为准。
- lookINTO_SimError_message 对运行中的 multisim 返回 status:null 且 raw.progress 给进度，可当轮询用。