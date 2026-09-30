# HKG analyst39 Ideas — wave s2_analyst39_d1

**Dataset**: analyst39
**Region**: HKG
**Delay**: 1


Dataset: `analyst39` | Region: HKG | Delay: 1 | Universe: TOP800 | Type: MATRIX (49 fields)
Category: analyst | Pyramid: HKG/D1/ANALYST (未点亮) + HKG/D1/FUNDAMENTAL (跨塔腿)

## 数据事实（S1 实测）
49 字段全 MATRIX 无 VECTOR；cov 0.88–0.98 主体；中性化实证 STATISTICAL 2.73% > SECTOR/SUBINDUSTRY 0%；decay 5 最优；win 先验 HKG-QMWLONOE-TRADEWHEN-BREAKTHROUGH。

---

**Concept**: EPS 同比增速动量 — 盈利同比加速是港股最稳的盈利动量来源，group_rank 行业内定位避免行业 beta
- **Implementation Example**: `group_rank({anl39_ghcspea}, subindustry)`
- **Rationale**: YoY 增速剔除季节性，直接捕捉基本面改善；cov 0.975 高覆盖

**Concept**: EPS 环比修正加速 — 季度环比 EPS 变化捕捉最近盈利动能拐点，ts_rank 长窗度量历史分位
- **Implementation Example**: `group_rank(ts_rank({anl39_epschngin}, 252), subindustry)`
- **Rationale**: 环比比 YoY 更快反应拐点；ts_rank 避免水平值噪声

**Concept**: 毛利率趋势改善 — 短期毛利率相对长期改善是定价能力提升领先信号，构造短长差趋势
- **Implementation Example**: `group_rank(subtract({anl39_qgrosmgn}, {anl39_ttmgrosmgn}), subindustry)`
- **Rationale**: 单一价差信号（短期质量 vs 长期质量），有明确经济含义

**Concept**: 去杠杆价值信号 — 总债务/权益比同比下降=财务风险改善，港股估值对杠杆敏感
- **Implementation Example**: `group_rank(subtract({anl39_qtotd2eq2}, {anl39_qtotd2eq}), subindustry)`
- **Rationale**: 单一价差信号（去杠杆动量）

**Concept**: 有形账面价值增长 — 剔除商誉的干净价值因子，ts_delta 捕捉增长而非水平
- **Implementation Example**: `group_rank(ts_delta({anl39_qtanbvps}, 66), subindustry)`
- **Rationale**: 港股账面价值有效；增长优于水平

**Concept**: 盈利质量交叉验证 — 含非经常性 EPS 减剔除非经常性 EPS=非经常性贡献度，高贡献预示盈利质量差
- **Implementation Example**: `multiply(group_rank(subtract({anl39_qepsinclxo}, {anl39_roxlcxspeq}), subindustry), -1)`
- **Rationale**: 单一价差（含/不含非经常性 EPS 差=应计质量）；应计异象

**Concept**: 分析师分歧逆向 — 目标价估计离散度/均值=归一化分歧度，trade_when 门控仅在有覆盖时开仓
- **Implementation Example**: `trade_when({anl39_tp_all_delay_1_numofests} > 0, multiply(group_rank(divide({anl39_tp_all_delay_1_stddev}, {anl39_tp_all_delay_1_mean}), subindustry), -1), -1)`
- **Rationale**: 复刻 HKG-QMWLONOE-TRADEWHEN 先验；稀疏字段必须门控

**Concept**: 账面价值季度 z-score — 普通股账面价值季度值的时间序列 z-score，industry 分组补 group 变量多样性
- **Implementation Example**: `group_rank(ts_zscore({anl39_spvbq}, 252), industry)`
- **Rationale**: 补 group 变量；z-score 度量偏离历史均值程度

**Concept**: 年度剔除非经常性 EPS 变化 — 年度核心 EPS 的年度变化，捕捉可持续盈利增长
- **Implementation Example**: `group_rank(ts_delta({anl39_roxlcxspea}, 252), subindustry)`
- **Rationale**: 剔除非经常性=核心盈利；年度窗口降低噪声

**Concept**: TTM EPS 同比变化衰减平滑 — TTM EPS 同比变化的衰减加权平滑，降低换手
- **Implementation Example**: `group_rank(ts_decay_linear({anl39_ghcspemtt}, 21), subindustry)`
- **Rationale**: 衰减平滑降换手，适合港股小宇宙

**Concept**: 第二历史财年毛利率水平 — 更早财年毛利率作为稳定基线
- **Implementation Example**: `group_rank({anl39_agrosmgn2}, subindustry)`
- **Rationale**: 历史毛利率作为质量基线，与近期毛利率配对可做趋势

**Concept**: 季度vs年度有形账面价值差 — 季度有形账面价值相对年度的差值，捕捉近期账面改善
- **Implementation Example**: `group_rank(subtract({anl39_qtanbvps}, {anl39_atanbvps}), subindustry)`
- **Rationale**: 单一价差（近期 vs 长期账面）

**Concept**: ROE 代理比率 — EPS/账面价值 构造 ROE 代理，比率型字段用 group_zscore 中性化
- **Implementation Example**: `group_zscore(divide({anl39_roxlcxspeq}, {anl39_spvbq}), subindustry)`
- **Rationale**: 比率型；直接可得盈利能力

**Concept**: 5 年毛利率长窗 rank — 长期毛利率水平的时间序列分位定位
- **Implementation Example**: `group_rank(ts_rank({anl39_grosmgn5yr}, 504), subindustry)`
- **Rationale**: 长窗 rank 度量结构性质量位置