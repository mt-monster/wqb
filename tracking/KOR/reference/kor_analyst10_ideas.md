# analyst10 GEM Ideas (KOR / TOP600 / delay1)

## 字段

- 主信号（smartest pred_surps 族，MATRIX，cov 0.83-0.96，users 1-4）：anl10_smartest_net_fy1_pred_surps_v1、anl10_smartest_sal_fy1_pred_surps_v1、anl10_smartest_pre_fy1_pred_surps_v1、anl10_smartest_ebi_fy1_pred_surps_v1、anl10_smartest_gps_fy1_pred_surps_v1
- 辅助（nums 覆盖广度族）：anl10_smartest_pre_fq1_nums、anl10_smartest_gps_fq1_nums；次选 anl10_salrevise_ratio_to_close_fy1_7862
- 禁用：revise_value 族（wave97-99 判死）、historical_estimate_currency（货币代码）、det/past VECTOR 元数据族

## 特征

- MATRIX 直接使用（无需 vec_avg/ts_backfill，cov≥0.83）；pred_surps 为模型标准化预测惊喜但仍偏态 → rank 强制；nums 计数 → rank 强制；惊喜信号半衰期短 → ts_decay_linear 用 5 短窗

## 建议

- PEAD 主机制正向；industry 组内相对化（wave 143 验证 +0.10S）；多口径一致性用双 rank 加权（禁 add(A,B) 裸混）；nums 低覆盖 = 惊喜不可靠 → if_else 门控 / bucket 分组

**Dataset**: analyst10
**Region**: KOR
**Delay**: 1

**Concept**: Predicted Earnings Surprise Drift (PEAD)
- **Mechanism**: The proprietary model-predicted surprise forecasts consensus revisions before they happen; stocks with high predicted net-income surprise drift upward as actual revisions confirm the model, a forward-looking PEAD distinct from backward revision momentum. expected_exposure: predicted earnings surprise drift.
- **Fields**: `anl10_smartest_net_fy1_pred_surps_v1`
- **Implementation Example**: `rank(ts_decay_linear({anl10_smartest_net_fy1_pred_surps_v1}, 5))`
- **Direction**: positive

**Concept**: Industry-Relative Predicted Surprise
- **Mechanism**: Ranking predicted surprise within industry removes sector-wide estimate waves and isolates firm-specific expected outperformance; wave 143 proved industry grouping beats sector (+0.10 Sharpe). expected_exposure: industry-neutral surprise.
- **Fields**: `anl10_smartest_sal_fy1_pred_surps_v1`
- **Implementation Example**: `group_rank(rank({anl10_smartest_sal_fy1_pred_surps_v1}), industry)`
- **Direction**: positive

**Concept**: Multi-Item Surprise Consistency
- **Mechanism**: When predicted surprises on both net income and EBIT agree in direction, the signal is a genuine fundamental expectation shift rather than item-specific model noise; consistent double-confirmation strengthens drift. expected_exposure: confirmed surprise composite.
- **Fields**: `anl10_smartest_net_fy1_pred_surps_v1`, `anl10_smartest_ebi_fy1_pred_surps_v1`
- **Implementation Example**: `add(multiply(0.5, rank({anl10_smartest_net_fy1_pred_surps_v1})), multiply(0.5, rank({anl10_smartest_ebi_fy1_pred_surps_v1})))`
- **Direction**: positive

**Concept**: Coverage-Gated Surprise Reliability
- **Mechanism**: Predicted surprises for thinly-covered names are model extrapolations with low information content; gating on analyst coverage count keeps surprises where consensus dynamics actually trade. expected_exposure: quality-gated surprise.
- **Fields**: `anl10_smartest_pre_fy1_pred_surps_v1`, `anl10_smartest_pre_fq1_nums`
- **Implementation Example**: `if_else(rank({anl10_smartest_pre_fq1_nums}) > 0.3, rank({anl10_smartest_pre_fy1_pred_surps_v1}), 0)`
- **Direction**: positive

**Concept**: Neglected Firm Premium
- **Mechanism**: Low analyst coverage marks neglected stocks with slower information incorporation; the neglected-firm premium compensates for limited attention and higher information uncertainty. expected_exposure: neglected firm premium.
- **Fields**: `anl10_smartest_gps_fq1_nums`
- **Implementation Example**: `multiply(-1, rank({anl10_smartest_gps_fq1_nums}))`
- **Direction**: negative

**Concept**: Surprise Momentum Acceleration
- **Mechanism**: A rising predicted surprise over the last month signals accelerating model confidence ahead of the earnings event; the time-derivative of expectation catches the drift earlier than the level. expected_exposure: surprise acceleration.
- **Fields**: `anl10_smartest_gps_fy1_pred_surps_v1`
- **Implementation Example**: `rank(ts_delta({anl10_smartest_gps_fy1_pred_surps_v1}, 22))`
- **Direction**: positive
