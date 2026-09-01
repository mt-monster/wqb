# S1 字段笔记：analyst_consensus（KOR / TOP600 / delay1）

- 数据集类型：VECTOR 2325 + MATRIX 18（字段总数 2343）
- S1 白名单：95 字段（ledger `s1_analyst_consensus_d1`，source=s2_nested）
- ideas 文档：KOR_delay1_analyst_consensus_ideas.md（8 概念，带 expected_exposure 标签）
- GEM 产出：59 式（wave=s2_analyst_consensus_d1）+ 3 条手工 group 骨架补槽

## 字段分类

| 族 | 代表字段 | 语义 | 风险 |
|---|---|---|---|
| EPS 预期水平 | mean/median/max/min_estimate_eps_annual12_3 | 分析师年度 EPS 一致预期 | 慢变，需 4w_prior 差分激活 |
| EPS 修正（4 周） | mean_estimate_four_weeks_prior_(fxadj_)eps_annual12_3 | 4 周前快照 | 修正方向=动量暴露 |
| 税前利润一致预期 | mean_estimate_pretax_annual12_2 / four_weeks_prior | 非 EPS 利润表腿 | 与 EPS 修正在 KOR 低拥挤 |
| 分散度 | stddev_estimate_eps_annual12_3 / stddev_four_weeks_prior_eps_annual12_3 | 预测分歧 | 分散度压缩=不确定性消除（lowvol 暴露） |
| 修正广度 | count_net_income_estimates / count_net_income_3mth_prior | 覆盖分析师数变化 | 稀疏字段需防 CW |
| 毛利率一致预期 | mean/max_estimate_grossmargin_annual12(_tribes) | 毛利预期水平 | tribes 口径与主口径冗余 |
| 意外值 | mean_surprise_value_grossmargin_annual12(_tribes) | 实际-预期 | 事件后漂移暴露 |
| 股利预期 | mean/median_estimate_dividend_annual12(_2) | 分红一致预期 | KOR 分红信号弱先验 |

## 特征工程建议（初始信号）

1. 修正漂移：rank(subtract(vec_avg(当期), vec_avg(4w_prior)))——pretax/eps/fxadj_eps 三线。
2. 分散度压缩：rank(subtract(vec_avg(4w_prior stddev), vec_avg(当期 stddev)))。
3. 修正广度/幅度比：count 差分 ÷ mean 差分（防单点大修正主导）。

## 进阶信号（建议）

4. group 骨架：group_rank(vec_avg(mean_estimate_eps_annual12_3), industry)、
   group_zscore(pretax 修正, sector)、group_neutralize(surprise rank, industry)。
5. flash vs consensus：mean_flash_estimate_eps_annual12_3 对 mean_estimate 比值（先行指标）。

## 预处理决策

- VECTOR 字段一律 vec_avg 聚合为 MATRIX 后再横截面运算（平台硬要求）。
- 差分型信号需外层 rank 防厚尾；count 类字段 cov 中等，先观察 CW 再决定。
- 禁用 _t 时间戳类字段（oth496 教训，本集无此族）。
- 死路规避：评级修正×SH 族（KOR-MLPROJ-RATING-SH-SATURATED）不复刻；本波用一致预期原值/修正，不碰 change_6m_rating_revision。
