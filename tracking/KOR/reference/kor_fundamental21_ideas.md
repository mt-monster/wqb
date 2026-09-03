# fundamental21 GEM Ideas (KOR / TOP600 / delay1)

## 字段

- 主信号（fnd27 族，cov≈0.71，users=0）：fnd27_allcategories_insight_allcategories_insight、fnd27_allcategories_momentum_allcategories_momentum、fnd27_allcategories_pulse_allcategories_pulse、fnd27_allcategories_insight_materiality_insight、fnd27_allcategories_momentum_materiality_momentum、fnd27_allcategories_insight_allcategoriesindustrypercentile_insight
- 辅助：fnd27_volume_ttmdaily_allcategories_articlevolumettm（关注度）、fnd21_accidentandsafetymanagement_impactpercentagettm（治理风险冲击）
- 禁用：fnd21_* insight/momentum/pulse 族（cov 0.26-0.31 < 0.4 硬门）

## 特征

- VECTOR 事件流 → vec_avg + ts_backfill 22（ESG 月度更新为主，洞多必须补）；评分类偏态 → rank 强制；TTM 慢信号 → ts_decay_linear(22) 平滑；industrypercentile 已预计算行业相对但仍套 rank 归一

## 建议

- 慢变质量信号走长窗（22/66）；industry 组内相对化（wave 143 验证 +0.10S）；momentum 斜率信号方向待验证（改善→正）；negative 冲击族用 multiply(-1, rank(...))

**Dataset**: fundamental21
**Region**: KOR
**Delay**: 1

**Concept**: ESG Quality Premium
- **Mechanism**: High aggregate ESG insight marks better governance and lower tail risk; chaebol-market investors slowly price governance quality, producing a quality drift. expected_exposure: ESG governance quality premium.
- **Fields**: `fnd27_allcategories_insight_allcategories_insight`
- **Implementation Example**: `rank(ts_decay_linear(ts_backfill(vec_avg({fnd27_allcategories_insight_allcategories_insight}), 22), 22))`
- **Direction**: positive

**Concept**: ESG Momentum Drift
- **Mechanism**: A positive trailing-twelve-month slope of ESG insight signals improving governance trajectory that the market underweights versus level-based ratings; improvers drift upward. expected_exposure: ESG improvement momentum.
- **Fields**: `fnd27_allcategories_momentum_allcategories_momentum`
- **Implementation Example**: `rank(ts_backfill(vec_avg({fnd27_allcategories_momentum_allcategories_momentum}), 22))`
- **Direction**: positive

**Concept**: Industry-Relative ESG Percentile
- **Mechanism**: Pre-computed within-industry ESG percentile isolates firm-specific governance quality from sector baselines; industry-relative outperformers are slowly re-rated (wave 143 showed industry grouping beats sector +0.10 Sharpe). expected_exposure: industry-neutral ESG quality.
- **Fields**: `fnd27_allcategories_insight_allcategoriesindustrypercentile_insight`
- **Implementation Example**: `group_rank(rank(ts_backfill(vec_avg({fnd27_allcategories_insight_allcategoriesindustrypercentile_insight}), 22)), industry)`
- **Direction**: positive

**Concept**: Materiality-Focused ESG Quality
- **Mechanism**: Restricting ESG scoring to material categories removes noise from irrelevant topics; material ESG quality carries stronger fundamental information than headline scores. expected_exposure: material ESG quality.
- **Fields**: `fnd27_allcategories_insight_materiality_insight`
- **Implementation Example**: `rank(ts_decay_linear(ts_backfill(vec_avg({fnd27_allcategories_insight_materiality_insight}), 22), 22))`
- **Direction**: positive

**Concept**: ESG Short-Term Pulse Reversal
- **Mechanism**: The real-time pulse score captures short-term ESG news spikes; extreme positive pulses reflect overreaction to governance headlines that revert as fundamentals dominate. expected_exposure: ESG news overreaction reversal.
- **Fields**: `fnd27_allcategories_pulse_allcategories_pulse`
- **Implementation Example**: `multiply(-1, rank(ts_backfill(vec_avg({fnd27_allcategories_pulse_allcategories_pulse}), 5)))`
- **Direction**: negative

**Concept**: Governance Risk Impact Avoidance
- **Mechanism**: High trailing impact share of accident/safety and ethics news flags elevated governance tail risk; the market discounts such firms too slowly, so avoiding high-impact names earns a risk-avoidance premium. expected_exposure: governance risk discount.
- **Fields**: `fnd21_accidentandsafetymanagement_impactpercentagettm`
- **Implementation Example**: `multiply(-1, rank(ts_backfill(vec_avg({fnd21_accidentandsafetymanagement_impactpercentagettm}), 66)))`
- **Direction**: negative
