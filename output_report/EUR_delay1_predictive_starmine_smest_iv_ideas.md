# predictive_starmine smest/iv GEM Ideas (wave122)

**Dataset**: predictive_starmine
**Region**: EUR
**Delay**: 1


**Concept**: smest 盈利预测水平（慢腿）
- **Implementation Example**: `rank(ts_mean({smest_f12m_earnings_5}, 66))`
- **Rationale**: smest 盈利预测反映分析师对公司未来盈利的预期，高预测预示增长潜力

**Concept**: smest EBITDA 预测水平（慢腿）
- **Implementation Example**: `rank(ts_mean({smest_f12m_ebitda_5}, 66))`
- **Rationale**: smest EBITDA 预测反映分析师对公司未来 EBITDA 的预期，高预测预示运营改善

**Concept**: smest 收入预测水平（慢腿）
- **Implementation Example**: `rank(ts_mean({smest_f12m_revenue_4}, 66))`
- **Rationale**: smest 收入预测反映分析师对公司未来收入的预期，高预测预示市场份额扩张

**Concept**: iv 内在价值 CAGR（慢腿）
- **Implementation Example**: `rank(ts_mean({iv_cagr_base_year_3}, 66))`
- **Rationale**: iv 内在价值 CAGR 反映公司长期增长潜力，高 CAGR 预示价值低估

**Concept**: iv 贴现率（慢腿）
- **Implementation Example**: `rank(ts_mean({iv_discount_rate_3}, 66))`
- **Rationale**: iv 贴现率反映市场对公司风险的定价，低贴现率预示风险低估

**Concept**: iv 远期 EPS CAGR（慢腿）
- **Implementation Example**: `rank(ts_mean({iv_forward_5yr_eps_cagr_3}, 66))`
- **Rationale**: iv 远期 EPS CAGR 反映公司长期盈利增长预期，高 CAGR 预示成长潜力

**Concept**: smest 预测变化（快腿）
- **Implementation Example**: `rank(ts_delta({smest_f12m_earnings_5}, 21))`
- **Rationale**: smest 预测变化反映分析师预期调整，正变化预示盈利上调

**Concept**: iv CAGR × smest 预测交互（组合）
- **Implementation Example**: `rank(multiply(ts_zscore({iv_cagr_base_year_3}, 66), ts_zscore({smest_f12m_earnings_5}, 66)))`
- **Rationale**: iv CAGR 与 smest 预测的交互项，捕捉"高内在价值+高盈利预测"与"低内在价值+低盈利预测"的差异