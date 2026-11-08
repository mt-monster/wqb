# DEU Analyst 数据集字段画像汇总（2026-11-06，S1 存档）

> 目标战役：DEU Analyst ATOM ×10。画像数据源：平台 get_datafields（DEU/TOP500/D1，filter_sharpe=false 全量），逐数据集原始目录存 `tracking/DEU/atom_analyst/fields/<ds>_fields.json`。
> ⚠ 平台集级 coverage 已多次证伪，本表覆盖率为字段级中位数/分桶，判死以「连续多年空窗」口径的实测为准（探针 longCount + get_alpha_yearly_stats）。

## 一、数据集全景（18 个 analyst 数据集，3 个已判死不入场）

| 数据集 | 名称/机制 | 字段数 | 类型分布 | cov≥0.3 | cov≥0.6 | 覆盖中位 | 状态/结论 |
|---|---|---:|---|---:|---:|---:|---|
| analyst7 | Broker Estimates（修正计数网格 27 后缀×15 指标 + rec/act_q 族） | 608 | MATRIX:608 | 556 | 425 | 0.7 | 可入场 |
| analyst8 | Daily Split Data（拆股事件） | 10 | VECTOR:9 MATRIX:1 | 0 | 0 | 0 | cov0 需存在性探针 |
| analyst10 | Performance-Weighted Analyst Estimates（StarMine SmartEstimate） | 53 | MATRIX:40 VECTOR:8 SYMBOL:5 | 0 | 0 | 0 | cov0 需存在性探针 |
| analyst15 | Earnings forecasts（国家/行业/指数层聚合） | 537 | MATRIX:533 SYMBOL:4 | 0 | 0 | 0 | cov0 需存在性探针 |
| analyst16 | Real Time Estimates | 66 | SYMBOL:28 VECTOR:38 | 0 | 0 | 0 | cov0 需存在性探针 |
| analyst39 | Analyst estimates & financial ratios | 24 | MATRIX:24 | 0 | 0 | 0 | cov0 需存在性探针 |
| analyst46 | Analyst Investment insight（TipRanks，已判死 max|S|0.40） | 5 | MATRIX:5 | 0 | 0 | 0 | cov0 需存在性探针 |
| analyst47 | Alternative Analyst Investment insight（raw 版，5 字段） | 5 | MATRIX:5 | 5 | 1 | 0.53 | 可入场 |
| analyst69 | Fundamental Analyst Estimates（FactSet） | 292 | MATRIX:104 VECTOR:188 | 0 | 0 | 0 | cov0 需存在性探针 |
| analyst83 | Smart Conference call transcript（电话会文本特征） | 345 | VECTOR:345 | 345 | 0 | 0.34 | 可入场 |
| analyst9 | Analyst Estimate Daily（修正广度 VECTOR，已测 8 条 best 0.73） | 51 | VECTOR:51 | 51 | 20 | 0.58 | 可入场 |
| analyst93 | Europe Analyst Estimate Daily（4 族判死 + prod 饱和族） | 100 | VECTOR:100 | 100 | 100 | 0.64 | 可入场 |
| analyst94 | Fundamental Income and Dividend Model | 34 | VECTOR:17 MATRIX:17 | 0 | 0 | 0 | cov0 需存在性探针 |
| analyst_consensus | Standardized Analyst Consensus Forecasts | 1972 | VECTOR:1954 MATRIX:18 | 0 | 0 | 0 | cov0 需存在性探针 |
| analyst_factor_signals | Global Analyst Factor Signals（108 MATRIX 字段） | 108 | MATRIX:108 | 103 | 49 | 0.56 | 可入场 |
| analyst35 | ESG Model | — | — | — | — | — | **已判死**（ledger） |
| analyst44 | Integrated Broker Estimates | — | — | — | — | — | **已判死**（机制真实但强度不足 max S0.69，2026-11-04 复核） |
| analyst48 | Dividend estimation | — | — | — | — | — | **已判死**（ledger） |

## 二、历史回测覆盖（wqb.db backtest_results, DEU）

| 数据集 | 已测 | best S | ≥1.25 | 结论 |
|---|---:|---:|---:|---|
| analyst93 | 131 | 1.57 | 16 | 4 族判死 + recprofitability 族 prod 饱和 |
| analyst_earnings_ibes | 115 | 2.17 | 58 | **已不在 analyst 类目录**（平台重分类），历史产出已提交 MODEL 塔 |
| analyst_factor_signals | 94 | 1.23 | 0 | 全押 estimate_change_3mo 族；分歧度/偏度/斜率族零测 |
| analyst7 | 61 | 1.30 | 1 | 608 字段仅 61 测，广度/推荐/PEAD/区间分歧族基本未测 |
| analyst44 | 42 | 1.37 | 12 | 已判死 |
| analyst9 | 8 | 0.73 | 0 | 修正广度族弱（VECTOR 口径） |
| analyst47 | 8 | 1.46 | 1 | 但 1.46 为多腿 add（含跨集字段），纯 ATOM 强度未知 |
| analyst_consensus | 3 | 0.72 | 0 | 字段全 cov0（平台口径），需存在性探针 |

## 三、优先级（S0 白名单）

1. **analyst7** —— 最大真实矿脉：608 MATRIX 字段 cov 中位高、修正计数网格（raised/lowerednum × 15 指标 × 4 窗口）+ rec 推荐族 + act_q 惊喜族，历史仅 61 测。
2. **analyst_factor_signals 分歧度族** —— eps/revenue/netprofit 的 coeff_var/skewness/asymmetry/trend_slope 字段（cov 0.89-0.93）零回测；机制先验强（Diether 2002）。
3. **analyst83** —— 345 个电话会文本特征字段（cov 0.34），零回测，备选。
4. **analyst47** —— 5 字段小集，1 批探针可清。
5. cov0 数据集（analyst10/15/16/39/69/94/8/consensus）—— 仅当上述矿脉产出不足时，用 2-3 条存在性探针再定。
6. analyst9/93 —— 弱/死，不再投入（除非有新机制面）。

## 四、避雷（self-corr 池）
本赛季已提交 14 颗 ACTIVE，其中 ANALYST 塔 2 颗均基于 `eps_y1_estimate_change_3mo`（analyst_factor_signals）：
- `2rjrMZ25`：eps_y1 单字段双窗 ATOM（S1.77）
- `LLM93nGa`：eps_y1 + shortinterest 门控（S1.88）
⇒ **estimate_change_3mo 族整族禁用**；修正方向类（trend_slope/T5 广度）须逐一过 self 验证。

## 五、分布特征/更新频率
- analyst7 / factor_signals 字段级覆盖率、userCount/alphaCount 拥挤度见 fields/*.json；时间维（更新频率、NaN 结构）在探针回收后按「三分法判读」补充记录。
- analyst7 est_12m_ebi_raised_1wk 平台级 a1446 最拥挤；DEU 侧拥挤度待 prod 直方图。
