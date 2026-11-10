# EUR × predictive_starmine 字段画像（2026-11-08）

> 平台目录：638/638 全量（complete=true）；arm_* 主字段族 30 个（MATRIX）
> 塔位：**字段平台归属 = MODEL(×1.3，已点亮)**（RRAvGrn0/bl6KwjwK 实测 pyramids 均含 MODEL）⇒ **塔价值低，本战役降级**

## 一、arm 字段族（30 个，节选）

| 字段 | cov | uC/aC | 语义 |
|---|---|---|---|
| arm_secondary_earnings_component_score_3/7 | 0.91/0.74 | 1/1 | 次要盈利成分评分（RRAvGrn0 在用 _3） |
| arm_preferred_earnings_component_score(/_6) | 0.94/0.75 | 2/2 | 首要盈利成分评分（RRAvGrn0 在用） |
| arm_revenue_component_score_3/4 | 0.94/0.75 | 0/0-1 | **营收成分评分——全冷门，未开采** |
| arm_recommendations_component_score_3/6 | 0.94/0.75 | 0-1 | 评级成分评分 |
| arm_score_change_{1d,3d,7d,30d,60d,90d}_{2,3,4,6,7,21} | 0.74-0.94 | 0-1 | 评分变化（多窗口多版本） |
| arm_country_rank_score / arm_global_rank_score / arm_region_rank_decimal | 0.75-0.94 | 0-1 | 国家/全球/区域排名 |
| arm_score_5pt_scale / arm_new_activity_flag | 0.75-0.95 | 0-1 | 五分制评分 / 活动标志 |

## 二、EUR 实证

- **RRAvGrn0**（ACTIVE，[INSIDERS,MODEL]，S1.99/prod 0.5437/self 0.2459）：二阶差分/极值差读数 `rank(ts_max_diff(rank(arm_secondary_earnings_component_score_3),149)) − ts_rank(ts_delta(ts_delta(arm_preferred_earnings_component_score,22),22),500) + rank(ts_sum(avg_top_buy_shares,66))`。
- rank 水平读数 6 条 S 0.10–0.49 判死（arm_score_5pt_scale_2 等）。
- ⚠ A1Q729Ll 邻居 XgWxwWRl（starmine surprise+FCF 卫星）死于 prod_sibling YP5OG79M=0.82。

## 三、结论

1. arm 字段点亮的是 MODEL 塔（已点亮）⇒ 按「已点亮塔不选」纪律，本战役不投主槽。
2. 若后续篮子缺口需要补位：arm_revenue_component_score 二阶差分读数是唯一冷门候选（aC 0），须过 self(vs RRAvGrn0)+prod 双闸。
