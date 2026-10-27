# acquisition_model — EUR 字段画像

> 自动生成于 2026-10-20 17:55　|　[← 返回索引](README.md)

## 一、数据集元信息

| 项 | 值 |
|---|---|
| 数据集 ID | `acquisition_model` |
| 名称 | Corporate Acquisition Likelihood Model |
| 类别 | OTHER |
| 数据字段数(平台) | 15 |
| 覆盖率 | 0.7484 |
| 平台已有 alpha | 14 |
| valueScore | 3.0 |
| 金字塔倍率 | 1.5 |
| 数据类型 | VECTOR |
| delay | 1 |
| 状态 | scanned |

## 二、数据集描述（平台原文）

> ⚠️ 平台目录描述存在**错配**（已实测：insiders1 / imbalance5 的描述指向无关数据集）。以「五、全字段明细」的真实字段语义为准。

This dataset provides predictive rankings of publicly traded companies most likely to be acquired within the next year. It leverages both advanced natural language processing of global news articles and analysis of structured financial and corporate data, including M&A activity, proxy fights, credit risk, and valuation metrics. By combining text-based signals with fundamental indicators, the model offers percentile scores across global, regional, sector, and industry levels, as well as flags for recent corporate actions. Investors and analysts can use these insights to identify potential takeover targets, anticipate price movements driven by acquisition speculation, and inform event-driven trading strategies.

## 三、字段画像汇总

| 维度 | 结果 |
|---|---|
| 字段总数 | **15** |
| 类型分布 | VECTOR×15 |
| 平均覆盖率 | **0.748** |
| 覆盖率区间 | 0.75 ~ 0.75 |
| 更新频率（推断） | 低频（季/年） |
| 可用性评级 | 良（覆盖 70–90%，sub/robust 需关注） |

**覆盖率分档**

| 档 | 字段数 | 占比 |
|---|---:|---:|
| 高 (≥0.90) | 0 | 0.0% |
| 中 (0.70–0.90) | 15 | 100.0% |
| 低 (0.50–0.70) | 0 | 0.0% |
| 稀疏 (<0.50) | 0 | 0.0% |

**历史实测分布（field_profile_perf）**

| 判定 | 字段数 | 占比 |
|---|---:|---:|
| UNTESTED | 12 | 80.0% |
| DEAD | 3 | 20.0% |

- 已实测字段：**3** 个（20%），best_sharpe 最高 **-0.41**，中位 -0.72

## 四、语义维度地图（自动归类）

| 语义族 | 字段数 | 平均覆盖 | 代表字段 |
|---|---:|---:|---|
| 宏观与行业 | 7 | 0.75 | country_percentile_acquisition_likelihood、industry_percentile_acquisition_likelihood、region_company_size_percentile_rank |
| 风险与质量 | 4 | 0.75 | global_percentile_acquisition_likelihood、global_company_size_percentile_rank、global_credit_quality_percentile_rank |
| 持仓与资金流 | 2 | 0.75 | global_fundamental_factor_percentile_rank、region_fundamental_factor_percentile_rank |
| 情绪与新闻 | 2 | 0.75 | global_text_factor_percentile_rank、region_text_factor_percentile_rank |

## 五、全字段明细

> 按 `best_sharpe` 降序（未测者置后）。`判定` 来自 `field_profile_perf`：ALIVE=历史测出过 S≥闸线（**不代表可提交**）；UNTESTED=未测；UNUSABLE/DEAD/AXIS_ONLY=已证否或仅可作轴。

| # | 字段名 | 类型 | 覆盖 | 语义族 | 测次 | best_S | best_2Y | best_sub | 判定 | 描述 |
|---:|---|---|---:|---|---:|---:|---:|---:|---|---|
| 1 | `country_percentile_acquisition_likelihood` | VECTOR | 0.748 | 宏观与行业 | 1 | -0.41 | -0.92 | -0.07 | DEAD | Percentile score of M&A target likelihood within the company’s headquarters country (100 = highest, 1 = lowest) |
| 2 | `industry_percentile_acquisition_likelihood` | VECTOR | 0.748 | 宏观与行业 | 1 | -0.72 | -0.41 | -0.24 | DEAD | Percentile score from the M&A Target Model comparing the company to peers in the same Region+Industry; 100 = highest tar |
| 3 | `global_percentile_acquisition_likelihood` | VECTOR | 0.748 | 风险与质量 | 1 | -0.76 | -0.26 | -0.16 | DEAD | Percentile score from the M&A Target Model versus all companies globally; 100 = highest target likelihood, 1 = lowest |
| 4 | `global_company_size_percentile_rank` | VECTOR | 0.748 | 风险与质量 | 0 | — | — | — | UNTESTED | Percentile rank of the size component versus all companies globally; 100 = most favorable on size dimension |
| 5 | `global_credit_quality_percentile_rank` | VECTOR | 0.748 | 风险与质量 | 0 | — | — | — | UNTESTED | Percentile rank of the model’s credit-based component versus all companies globally; 100 = strongest, 1 = weakest |
| 6 | `global_fundamental_factor_percentile_rank` | VECTOR | 0.748 | 持仓与资金流 | 0 | — | — | — | UNTESTED | Percentile rank of the fundamentals component versus all companies globally; 100 = strongest, 1 = weakest |
| 7 | `global_text_factor_percentile_rank` | VECTOR | 0.748 | 情绪与新闻 | 0 | — | — | — | UNTESTED | Global percentile rank based on text/news-driven factors in the M&A Target model (100 = highest, 1 = lowest) |
| 8 | `global_valuation_percentile_rank` | VECTOR | 0.748 | 风险与质量 | 0 | — | — | — | UNTESTED | Percentile rank of the valuation component versus all companies globally; 100 = most favorable, 1 = least |
| 9 | `region_company_size_percentile_rank` | VECTOR | 0.748 | 宏观与行业 | 0 | — | — | — | UNTESTED | Percentile rank for the Size component within the M&A Target region set (100 = highest/largest, 1 = lowest) |
| 10 | `region_credit_quality_percentile_rank` | VECTOR | 0.748 | 宏观与行业 | 0 | — | — | — | UNTESTED | Percentile rank (1–100) of credit-based factors within the region peer set; higher values indicate stronger credit profi |
| 11 | `region_fundamental_factor_percentile_rank` | VECTOR | 0.748 | 持仓与资金流 | 0 | — | — | — | UNTESTED | Percentile rank of the fundamentals component versus companies in the same M&A region; 100 = strongest, 1 = weakest |
| 12 | `region_percentile_acquisition_likelihood` | VECTOR | 0.748 | 宏观与行业 | 0 | — | — | — | UNTESTED | Percentile score from the M&A Target Model versus companies in the same M&A region set; 100 = highest target likelihood, |
| 13 | `region_text_factor_percentile_rank` | VECTOR | 0.748 | 情绪与新闻 | 0 | — | — | — | UNTESTED | Percentile rank (1–100) of the model’s text/news factors for the company relative to peers in the same M&A Target region |
| 14 | `region_valuation_percentile_rank` | VECTOR | 0.748 | 宏观与行业 | 0 | — | — | — | UNTESTED | Percentile rank of the valuation component versus companies in the same M&A region; 100 = most favorable, 1 = least |
| 15 | `sector_percentile_acquisition_likelihood` | VECTOR | 0.748 | 宏观与行业 | 0 | — | — | — | UNTESTED | Percentile score of M&A target likelihood within the Region+Sector peer group (100 = highest, 1 = lowest) |

## 六、本地回测证据

- 本地累计回测 **8** 条；其中 `ra_failed_checks` 为空的 **0** 条（⚠ 空不等于过关，2Y 为 NULL 者需复检）

| alpha | S | F | 2Y | sub | TO | RA失败数 | wave | 表达式（截断） |
|---|---:|---:|---:|---:|---:|---|---:|---|
| `mLmjXbwX` | 0.16 | 0.04 | 1.46 | 0.17 | 0.01 | ["LOW_SHARPE | 218 | `days_from_last_change(vec_sum(country_percentile_acquisition_likelihood))` |
| `N1a7OrX8` | 0.12 | 0.02 | 1.42 | 0.10 | 0.01 | ["LOW_SHARPE | 218 | `days_from_last_change(vec_avg(global_percentile_acquisition_likelihood))` |
| `JjN7dOMj` | 0.10 | 0.02 | 1.45 | 0.08 | 0.01 | ["LOW_SHARPE | 218 | `days_from_last_change(vec_avg(sector_percentile_acquisition_likelihood))` |
| `vRrjmlRa` | 0.07 | 0.01 | 1.45 | 0.10 | 0.01 | ["LOW_SHARPE | 218 | `days_from_last_change(vec_avg(industry_percentile_acquisition_likelihood))` |
| `O0N79Z0J` | 0.07 | 0.01 | 1.38 | 0.17 | 0.01 | ["LOW_SHARPE | 218 | `ts_mean(days_from_last_change(vec_avg(region_percentile_acquisition_likelihood)), 120)` |
| `e7bzrKn6` | -0.41 | -0.13 | -0.92 | -0.07 | 0.04 | ["LOW_SHARPE | 218 | `group_rank(divide(ts_av_diff(ts_backfill(vec_sum(country_percentile_acquisition_likelihood` |
| `d5bjQmnw` | -0.72 | -0.32 | -0.41 | -0.24 | 0.04 | ["LOW_SHARPE | 218 | `divide(ts_av_diff(ts_backfill(vec_avg(industry_percentile_acquisition_likelihood), 22), 25` |
| `58zlvOnX` | -0.76 | -0.36 | -0.26 | -0.16 | 0.04 | ["LOW_SHARPE | 218 | `divide(ts_av_diff(ts_backfill(vec_avg(global_percentile_acquisition_likelihood), 22), 252)` |

## 七、判死记录（sealed dead_end）

- `EUR-ACQUISITION-MODEL-COLD-ZERO-YIELD`（2026-09-23T18:02:26）family=mna_target_likelihood_percentile (acquisition_model 全 15 字段 VECTOR percentile)：{"family": "mna_target_likelihood_percentile (acquisition_model 全 15 字段 VECTOR percentile)", "reason": "wave218 8 探针全灭 max/sharpe/=0.16（best 2y 1.46 但 IS 无强度），达 EUR profile fast_kill 线（新集 8 探针无 /S/>=0.5 即判死）。字段全冷门（users<=4）理论 prod≈0，死因是纯信号缺席。2 条 group_cartesian_product/group_count 单位错误被自动隔离（VECTOR 字段不能喂 group_* 轴）。", "source": "registry_dead_end", "salvage": {"alpha_ids": [], "count": 0, "source_w
- `EUR-EVENT-RELATION-WEAK`（2026-09-23T18:22:52）family=event_relation 实体关系强度族（relation_strength_rank/score × merger/partner/financial/general）：{"family": "event_relation 实体关系强度族（relation_strength_rank/score × merger/partner/financial/general）", "reason": "wave233 8 探针全灭 max/sharpe/=0.43 < 0.5 → 达 EUR fast_kill 判死线。字段全冷门（users<=1）理论 prod≈0，纯信号缺席。OTHER 塔已连续三集判死（acquisition_model 0.16 / insider_feats 多样性墙 / event_relation 0.43）。", "source": "registry_dead_end", "salvage": {"alpha_ids": [], "count": 0, "source_waves": [], "sealed_at": "2026-
- `EUR-INSIDER-FEATS-WEAK`（2026-09-23T18:35:49）family=insider_feats 内部人买卖比率族（buy/sell ratio × tx count × lookback）：{"family": "insider_feats 内部人买卖比率族（buy/sell ratio × tx count × lookback）", "reason": "wave238 10 探针全灭 best /sharpe/=0.47 < 0.5 → 达 fast_kill 判死线。此前 w232 多样性闸（flow 单 exposure）+ 字段名拼接幻觉 + 低覆盖无 backfill 三轮门禁墙已记录。OTHER 塔 4 候选全灭（acquisition_model/insider_feats/event_relation + ml_factor_proj 平台无字段）。", "source": "registry_dead_end", "salvage": {"alpha_ids": [], "count": 0, "source_waves": [], "sealed_at

