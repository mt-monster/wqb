**Dataset**: fundamental6
**Region**: MEA
**Delay**: 1

# MEA fundamental6 S1 ideas（TOP300/d1，Worldscope 高覆盖年度字段，VECTOR）

数据集理解：Worldscope 年度基本面，VECTOR 慢变量为主，白名单字段 cov 0.82-0.92。
wave69 "全字段 EVENT" 判死被用户豁免且已被 S1 证伪（正常 VECTOR 元数据）；
若单字段报 'does not support event inputs' 即剔除该字段，不恋战。
预处理：年度慢字段 `ts_backfill(…,365)`；比率一律两字段 divide；禁盈利水平场（LEVEL 饱和判死）。

**Concept**: 税前利润动量（SUE 同构换数据源）
- **Mechanism**: 税前利润意外经波动标准化，财报后漂移
- **Fields**: `fundamental_pretax_income`
- **Implementation Example**: `rank(divide(ts_av_diff(ts_backfill({fundamental_pretax_income},365),252),ts_std_dev(ts_backfill({fundamental_pretax_income},365),252)))`
- **Direction**: 正

**Concept**: 留存收益变化动量（内生融资能力改善）
- **Mechanism**: 留存收益同比变化，区分内生增长强弱
- **Fields**: `fundamental_retained_earnings`
- **Implementation Example**: `rank(ts_delta(ts_backfill({fundamental_retained_earnings},365),252))`
- **Direction**: 正

**Concept**: EBITDA 相对折旧的现金生成效率变化
- **Mechanism**: EBITDA 扣除折旧后的现金创造效率变化，资产质量信号
- **Fields**: `fundamental_ebitda`, `annual_depreciation_and_amortization`
- **Implementation Example**: `rank(ts_delta(divide(subtract(ts_backfill({fundamental_ebitda},365),ts_backfill({annual_depreciation_and_amortization},365)),ts_backfill({fundamental_ebitda},365)),252))`
- **Direction**: 正

**Concept**: 库存周期反转（需求转弱预警）
- **Mechanism**: 库存快速堆积预示需求走弱，反向交易
- **Fields**: `fundamental_inventory_total_annual`
- **Implementation Example**: `-1 * rank(ts_delta(ts_backfill({fundamental_inventory_total_annual},365),252))`
- **Direction**: 负

**Concept**: 净权益积累速率（资产负债表扩张质量）
- **Mechanism**: 普通股权益的稳健增长代表内生价值创造
- **Fields**: `fundamental_common_equity_total`
- **Implementation Example**: `rank(ts_delta(ts_backfill({fundamental_common_equity_total},365),252))`
- **Direction**: 正
