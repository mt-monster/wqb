**Dataset**: fundamental72
**Region**: MEA
**Delay**: 1

# MEA fundamental72 S1 ideas（TOP300/d1，白名单季度族，VECTOR）

数据集理解：Bloomberg PIT 季报 point-in-time，季度族在 MEA/TOP300 cov 0.8-0.88。
预处理：VECTOR 慢变量一律 `ts_backfill(…,120)` 再进时序算子；金额类跨公司不可比走比率或变化率；
禁盈利水平场（LEVEL zscore252 族 PROD 0.7879 已饱和判死），只做动量/变化/二阶差分等正交维度。

**Concept**: 盈余意外持续性（SUE 换字段版，与论坛模板同构但换 pit 字段与窗口）
- **Mechanism**: 盈利意外经标准差标准化后的滚动均值，捕捉财报后漂移
- **Fields**: `fnd72_pit_or_is_q_inc_bef_xo_less_min_int_pref_dvd`
- **Implementation Example**: `rank(divide(ts_av_diff(ts_backfill({fnd72_pit_or_is_q_inc_bef_xo_less_min_int_pref_dvd},120),252),ts_std_dev(ts_backfill({fnd72_pit_or_is_q_inc_bef_xo_less_min_int_pref_dvd},120),252)))`
- **Direction**: 正（盈余意外为正 → 后续收益）

**Concept**: 现金转化质量裂口（CFO 与净利润的相对强弱，应计质量反向代理）
- **Mechanism**: 经营现金流相对净利润的时序强弱差，识别应计虚高公司
- **Fields**: `fnd72_pit_or_cf_q_cf_cash_from_oper`, `fnd72_pit_or_cf_q_cf_net_inc`
- **Implementation Example**: `rank(subtract(ts_zscore(ts_backfill({fnd72_pit_or_cf_q_cf_cash_from_oper},120),252),ts_zscore(ts_backfill({fnd72_pit_or_cf_q_cf_net_inc},120),252)))`
- **Direction**: 正（现金转化改善 → 盈利质量提升）

**Concept**: 留存收益加速度（二阶变化捕捉内生增长拐点）
- **Mechanism**: 留存收益二阶差分，区分加速积累与减速公司
- **Fields**: `fnd72_pit_or_bs_q_bs_retain_earn`
- **Implementation Example**: `rank(ts_delta(ts_delta(ts_backfill({fnd72_pit_or_bs_q_bs_retain_earn},120),63),63))`
- **Direction**: 正

**Concept**: 资本开支过度投资折价（反转）
- **Mechanism**: MEA 小盘产能过剩，激进扩产公司折价
- **Fields**: `fnd72_pit_or_cf_q_cf_cap_expend_prpty_add`
- **Implementation Example**: `-1 * rank(ts_delta(ts_backfill({fnd72_pit_or_cf_q_cf_cap_expend_prpty_add},120),252))`
- **Direction**: 负（扩产越快越折价）

**Concept**: 经营利润率动量（比率的变化，非水平）
- **Mechanism**: 经营利润除以总资产的变化率，盈利效率改善动量
- **Fields**: `fnd72_pit_or_is_q_is_oper_inc`, `fnd72_pit_or_bs_q_bs_tot_asset`
- **Implementation Example**: `rank(ts_delta(divide(ts_backfill({fnd72_pit_or_is_q_is_oper_inc},120),ts_backfill({fnd72_pit_or_bs_q_bs_tot_asset},120)),252))`
- **Direction**: 正
