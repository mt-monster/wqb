# predictive_starmine eq_vr_dlra1 GEM Ideas (wave121)

**Dataset**: predictive_starmine
**Region**: EUR
**Delay**: 1


**Concept**: 应计成分水平（慢腿）
- **Implementation Example**: `rank(ts_mean({eq_vr_dlra1_accruals_component}, 66))`
- **Rationale**: 应计成分反映公司盈利质量，高应计可能预示盈利操纵，与现金流成分形成对照

**Concept**: 现金流成分水平（慢腿）
- **Implementation Example**: `rank(ts_mean({eq_vr_dlra1_cashflow_component}, 66))`
- **Rationale**: 现金流成分反映公司真实盈利能力，高现金流成分预示高质量盈利

**Concept**: 应计-现金流差异（慢腿）
- **Implementation Example**: `rank(ts_mean(subtract({eq_vr_dlra1_accruals_component}, {eq_vr_dlra1_cashflow_component}), 66))`
- **Rationale**: 应计-现金流差异捕捉盈利质量，高差异可能预示盈利不可持续

**Concept**: 经营效率成分水平（慢腿）
- **Implementation Example**: `rank(ts_mean({eq_vr_dlra1_operating_efficiency_component}, 66))`
- **Rationale**: 经营效率成分反映公司运营效率，高效率预示成本控制能力

**Concept**: 应计成分变化（快腿）
- **Implementation Example**: `rank(ts_delta({eq_vr_dlra1_accruals_component_change}, 21))`
- **Rationale**: 应计成分变化反映盈利质量变化趋势，正变化可能预示盈利恶化

**Concept**: 现金流成分变化（快腿）
- **Implementation Example**: `rank(ts_delta({eq_vr_dlra1_cashflow_component_change}, 21))`
- **Rationale**: 现金流成分变化反映真实盈利变化趋势，正变化预示盈利改善

**Concept**: 经营效率变化（快腿）
- **Implementation Example**: `rank(ts_delta({eq_vr_dlra1_operating_efficiency_change}, 21))`
- **Rationale**: 经营效率变化反映运营效率变化趋势，正变化预示成本改善

**Concept**: 应计×现金流交互（组合）
- **Implementation Example**: `rank(multiply(ts_zscore({eq_vr_dlra1_accruals_component}, 66), ts_zscore({eq_vr_dlra1_cashflow_component}, 66)))`
- **Rationale**: 应计与现金流的交互项，捕捉"高应计+高现金流"与"低应计+低现金流"的差异