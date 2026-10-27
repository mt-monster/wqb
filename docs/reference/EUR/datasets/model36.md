# model36 — EUR 字段画像

> 自动生成于 2026-10-20 17:55　|　[← 返回索引](README.md)

## 一、数据集元信息

| 项 | 值 |
|---|---|
| 数据集 ID | `model36` |
| 名称 | SmartRatios Model |
| 类别 | MODEL |
| 数据字段数(平台) | 43 |
| 覆盖率 | 0.8509 |
| 平台已有 alpha | 118 |
| valueScore | 2.0 |
| 金字塔倍率 | 1.3 |
| 数据类型 | — |
| delay | 1 |
| 状态 | — |

## 二、数据集描述（平台原文）

> ⚠️ 平台目录描述存在**错配**（已实测：insiders1 / imbalance5 的描述指向无关数据集）。以「五、全字段明细」的真实字段语义为准。

This dataset provides a comprehensive mapping between Reuters Instrument Codes (RICs) and Bloomberg IDs for securities across global markets. By linking these two widely used security identifiers, the dataset enables seamless integration and cross-referencing of data from different financial data providers. This mapping is essential for portfolio managers, analysts, and quantitative researchers who need to consolidate, validate, or enrich datasets from multiple sources. While not directly predictive of price movements, accurate identifier mapping is a foundational tool for building robust multi-source analytics, backtesting strategies, and ensuring data consistency in quantitative models.

## 三、字段画像汇总

| 维度 | 结果 |
|---|---|
| 字段总数 | **43** |
| 类型分布 | MATRIX×43 |
| 平均覆盖率 | **0.851** |
| 覆盖率区间 | 0.76 ~ 0.94 |
| 更新频率（推断） | 日频 |
| 可用性评级 | 良（覆盖 70–90%，sub/robust 需关注） |

**覆盖率分档**

| 档 | 字段数 | 占比 |
|---|---:|---:|
| 高 (≥0.90) | 21 | 48.8% |
| 中 (0.70–0.90) | 22 | 51.2% |
| 低 (0.50–0.70) | 0 | 0.0% |
| 稀疏 (<0.50) | 0 | 0.0% |

**历史实测分布（field_profile_perf）**

| 判定 | 字段数 | 占比 |
|---|---:|---:|
| UNTESTED | 43 | 100.0% |

- 该数据集全部字段**尚未实测**（UNTESTED）⇒ 优先做尽

## 四、语义维度地图（自动归类）

| 语义族 | 字段数 | 平均覆盖 | 代表字段 |
|---|---:|---:|---|
| 风险与质量 | 17 | 0.85 | credit_risk_leverage_score_d1、creditworthiness_letter_rating_numeric_d1、default_risk_global_percentile_d1_2 |
| 宏观与行业 | 16 | 0.85 | default_risk_country_percentile_d1_2、default_risk_region_percentile_d1_2、star_sr_country_rank_d1 |
| 盈利与财务 | 5 | 0.87 | credit_risk_profitability_score_d1、star_sr_profitability_d1、credit_risk_coverage_score_d1 |
| 价量与波动 | 4 | 0.85 | credit_risk_liquidity_score_d1、star_sr_liquidity_d1、credit_risk_liquidity_score_main |
| 其他 | 1 | 0.84 | mdl36_index_rating |

## 五、全字段明细

> 按 `best_sharpe` 降序（未测者置后）。`判定` 来自 `field_profile_perf`：ALIVE=历史测出过 S≥闸线（**不代表可提交**）；UNTESTED=未测；UNUSABLE/DEAD/AXIS_ONLY=已证否或仅可作轴。

| # | 字段名 | 类型 | 覆盖 | 语义族 | 测次 | best_S | best_2Y | best_sub | 判定 | 描述 |
|---:|---|---|---:|---|---:|---:|---:|---:|---|---|
| 1 | `credit_risk_leverage_score_d1` | MATRIX | 0.941 | 风险与质量 | 0 | — | — | — | UNTESTED | Percentile score reflecting leverage factors in credit risk assessment (daily version). |
| 2 | `credit_risk_profitability_score_d1` | MATRIX | 0.941 | 盈利与财务 | 0 | — | — | — | UNTESTED | Numeric score for profitability-related factors; higher indicates better profitability |
| 3 | `creditworthiness_letter_rating_numeric_d1` | MATRIX | 0.941 | 风险与质量 | 0 | — | — | — | UNTESTED | Continuous implied rating score aligned to the letter-grade scale (not a PD%); higher indicates stronger credit quality |
| 4 | `default_risk_country_percentile_d1_2` | MATRIX | 0.941 | 宏观与行业 | 0 | — | — | — | UNTESTED | Float percentile rank (0–100) of the company’s financial health within its country peer group; higher indicates better credit quality |
| 5 | `default_risk_global_percentile_d1_2` | MATRIX | 0.941 | 风险与质量 | 0 | — | — | — | UNTESTED | Float percentile rank (0–100) of financial health globally; higher indicates better credit quality |
| 6 | `default_risk_region_percentile_d1_2` | MATRIX | 0.941 | 宏观与行业 | 0 | — | — | — | UNTESTED | Float percentile rank (0–100) of financial health within the region; higher indicates better credit quality |
| 7 | `star_sr_country_rank_d1` | MATRIX | 0.941 | 宏观与行业 | 0 | — | — | — | UNTESTED | Percentile rank (1–100) within the company’s country of its 1‑year default probability; higher means lower default risk |
| 8 | `star_sr_global_rank_d1` | MATRIX | 0.941 | 风险与质量 | 0 | — | — | — | UNTESTED | Global percentile rank (1–100) of the company’s 1‑year default probability from SmartRatios; higher means lower default risk |
| 9 | `star_sr_leverage_d1` | MATRIX | 0.941 | 风险与质量 | 0 | — | — | — | UNTESTED | Percentile rank (1–100) reflecting only the leverage factors; higher indicates better credit quality |
| 10 | `star_sr_profitability_d1` | MATRIX | 0.941 | 盈利与财务 | 0 | — | — | — | UNTESTED | Percentile rank (1–100) reflecting only the profitability factors in the SmartRatios Credit Risk Model; higher indicates better credit quali |
| 11 | `star_sr_region_rank_d1` | MATRIX | 0.941 | 宏观与行业 | 0 | — | — | — | UNTESTED | Regional percentile rank (1–100) of the company’s 1‑year default probability; higher means lower default risk |
| 12 | `default_risk_sector_percentile_d1_2` | MATRIX | 0.939 | 宏观与行业 | 0 | — | — | — | UNTESTED | Float percentile rank (0–100) within the company’s sector; higher indicates better credit quality |
| 13 | `star_sr_sector_rank_d1` | MATRIX | 0.939 | 宏观与行业 | 0 | — | — | — | UNTESTED | Percentile rank (1–100) within the same region and sector of the company’s 1‑year default probability; higher means lower default risk |
| 14 | `credit_risk_liquidity_score_d1` | MATRIX | 0.939 | 价量与波动 | 0 | — | — | — | UNTESTED | Numeric score for liquidity-related factors; higher indicates stronger liquidity |
| 15 | `star_sr_liquidity_d1` | MATRIX | 0.939 | 价量与波动 | 0 | — | — | — | UNTESTED | Percentile rank (1–100) reflecting only the liquidity factors; higher indicates better credit quality |
| 16 | `credit_risk_growth_score_d1` | MATRIX | 0.938 | 风险与质量 | 0 | — | — | — | UNTESTED | Numeric score for growth-related factors affecting credit health; higher indicates stronger growth profile |
| 17 | `star_sr_growth_d1` | MATRIX | 0.938 | 风险与质量 | 0 | — | — | — | UNTESTED | Percentile rank (1–100) reflecting only the growth and stability factors; higher indicates better credit quality |
| 18 | `credit_risk_coverage_score_d1` | MATRIX | 0.937 | 盈利与财务 | 0 | — | — | — | UNTESTED | Numeric score for coverage factors (e.g., ability to cover interest/debt); higher indicates better coverage |
| 19 | `star_sr_coverage_d1` | MATRIX | 0.937 | 风险与质量 | 0 | — | — | — | UNTESTED | Percentile rank (1–100) reflecting only the coverage factors; higher indicates better credit quality |
| 20 | `default_risk_industry_percentile_d1_2` | MATRIX | 0.934 | 宏观与行业 | 0 | — | — | — | UNTESTED | Float percentile rank (0–100) within the company’s industry; higher indicates better credit quality |
| 21 | `star_sr_industr_rank_d1` | MATRIX | 0.934 | 宏观与行业 | 0 | — | — | — | UNTESTED | Percentile rank (1–100) within the same region and industry of the company’s 1‑year default probability; higher means lower default risk |
| 22 | `mdl36_index_rating` | MATRIX | 0.836 | 其他 | 0 | — | — | — | UNTESTED | Financial health rating |
| 23 | `credit_risk_leverage_score_main` | MATRIX | 0.764 | 风险与质量 | 0 | — | — | — | UNTESTED | Float percentile score (0–100) for the leverage component; higher indicates better leverage profile and lower credit risk |
| 24 | `credit_risk_profitability_score_main` | MATRIX | 0.764 | 盈利与财务 | 0 | — | — | — | UNTESTED | Float percentile score (0–100) for the profitability component; higher indicates stronger profitability and lower credit risk |
| 25 | `creditworthiness_letter_rating_numeric_main` | MATRIX | 0.764 | 风险与质量 | 0 | — | — | — | UNTESTED | Continuous numeric implied rating score aligned to the letter-grade scale (not a PD%); higher is safer |
| 26 | `default_risk_country_percentile_main` | MATRIX | 0.764 | 宏观与行业 | 0 | — | — | — | UNTESTED | Float 0–100 percentile rank of the company’s 1-year default probability within its country; higher values indicate lower default risk |
| 27 | `default_risk_global_percentile_main` | MATRIX | 0.764 | 风险与质量 | 0 | — | — | — | UNTESTED | Float 0–100 global percentile rank of the company’s 1-year default probability; higher values indicate lower default risk |
| 28 | `default_risk_region_percentile_main` | MATRIX | 0.764 | 宏观与行业 | 0 | — | — | — | UNTESTED | Float 0–100 regional percentile rank of the company’s 1-year default probability; higher values indicate lower default risk |
| 29 | `star_sr_country_rank` | MATRIX | 0.764 | 宏观与行业 | 0 | — | — | — | UNTESTED | Current 1–100 percentile rank by country of the company’s 1-year default probability; higher values indicate lower default risk |
| 30 | `star_sr_global_rank` | MATRIX | 0.764 | 风险与质量 | 0 | — | — | — | UNTESTED | Current global 1–100 percentile rank of the company’s 1-year default probability based on SmartRatios; higher values indicate lower default  |
| 31 | `star_sr_leverage` | MATRIX | 0.764 | 风险与质量 | 0 | — | — | — | UNTESTED | Percentile rank reflecting only the leverage factors of the model; 100 best, 1 worst |
| 32 | `star_sr_profitability` | MATRIX | 0.764 | 盈利与财务 | 0 | — | — | — | UNTESTED | Percentile rank reflecting only the profitability factors of the model; 100 best, 1 worst |
| 33 | `star_sr_region_rank` | MATRIX | 0.764 | 宏观与行业 | 0 | — | — | — | UNTESTED | Current regional 1–100 percentile rank of the company’s 1-year default probability; higher values indicate lower default risk |
| 34 | `default_risk_sector_percentile_main` | MATRIX | 0.763 | 宏观与行业 | 0 | — | — | — | UNTESTED | Float percentile rank (0–100) within the same region and sector by 1-year default probability; higher means safer |
| 35 | `star_sr_sector_rank` | MATRIX | 0.763 | 宏观与行业 | 0 | — | — | — | UNTESTED | Current 1–100 percentile rank of the company’s 1-year default probability among firms in the same region and sector; higher values indicate  |
| 36 | `credit_risk_liquidity_score_main` | MATRIX | 0.762 | 价量与波动 | 0 | — | — | — | UNTESTED | Float percentile score (0–100) for the liquidity component; higher indicates stronger liquidity and lower credit risk |
| 37 | `star_sr_liquidity` | MATRIX | 0.762 | 价量与波动 | 0 | — | — | — | UNTESTED | Percentile rank reflecting only the liquidity factors of the model; 100 best, 1 worst |
| 38 | `credit_risk_coverage_score_main` | MATRIX | 0.761 | 风险与质量 | 0 | — | — | — | UNTESTED | Float percentile score (0–100) for the coverage component; higher indicates better coverage and lower credit risk |
| 39 | `star_sr_coverage` | MATRIX | 0.761 | 风险与质量 | 0 | — | — | — | UNTESTED | Percentile rank reflecting only the coverage factors of the model; 100 best, 1 worst |
| 40 | `credit_risk_growth_score_main` | MATRIX | 0.761 | 风险与质量 | 0 | — | — | — | UNTESTED | Float percentile score (0–100) for the growth and stability component; higher indicates better growth/stability and lower credit risk |
| 41 | `star_sr_growth` | MATRIX | 0.761 | 风险与质量 | 0 | — | — | — | UNTESTED | Percentile rank reflecting only the growth and stability factors of the model; 100 best, 1 worst |
| 42 | `default_risk_industry_percentile_main` | MATRIX | 0.759 | 宏观与行业 | 0 | — | — | — | UNTESTED | Float 0–100 percentile rank of the company’s 1-year default probability within its region and industry; higher values indicate lower default |
| 43 | `star_sr_industr_rank` | MATRIX | 0.759 | 宏观与行业 | 0 | — | — | — | UNTESTED | Current 1–100 percentile rank of the company’s 1-year default probability among firms in the same region and industry; higher values indicat |

## 六、本地回测证据

本地库无该数据集的回测记录。

> 说明：`backtest_results` 只收录已持久化的波次（当前 EUR 共 1157 行）；本次会话的直接派发未写库，故此处为空**不代表未做尽**，实测结论见配套战役档案。

## 七、判死记录（sealed dead_end）

- `EUR-M36-CREDIT-DEFAULTRISK-PROD`（2026-08-23）family=model36 credit / default_risk dominant：{"dataset": "model36", "expr_pattern": "rank/group_zscore(default_risk_global_percentile_d1_2)", "settings": "EUR TOP2500 COUNTRY decay6", "example_id": "2rlv7dOY", "sharpe": 0.96, "fitness": 0.58, "prod_corr": 0.9072, "reason": "Credit/default_risk dominant not near-gate (max S0.96 F0.58) and prod 0.91>=0.7. Do not Mode A clone decay/neut. Next only ts_av_diff or group_mean residual, or leave MOD
- `EUR-M36-DEFAULTRISK-RESID-PROD`（2026-08-23）family=model36 default_risk residual：{"dataset": "model36", "example_id": "9qX9r0OK", "expr_pattern": "rank(subtract(default_risk_global_percentile_d1_2, group_mean(..., industry)))", "fitness": 0.58, "prod_corr": 0.8578, "reason": "Industry residual lifts S to 1.04 vs naked 0.96 but Fitness still 0.58 and prod 0.86. ts_av_diff weaker. Leave MODEL credit/default_risk.", "settings": "EUR TOP2500 COUNTRY decay6", "sharpe": 1.04, "wave"
- `EUR-NEWS38-CONCEPT-WEAK`（2026-08-25）family=news38 densified tone/polarity/relevance concepts：{"dataset": "news38", "id": "EUR-NEWS38-CONCEPT-WEAK", "reason": "Wave64 56 exprs / 7 concept slots (tone invert, pos-neg score/freq, relevance-gated tone, relevance-heat, related_num, analytics-score). Max S0.61 F0.20 (ak7dLe55). Heat slot max S0.53 F0.36. No cheap-gate. Slow-leg /S/<1 so do not mix PV.", "rule": "Leave news38 standalone densify concepts. Do not mix v_rev/wedge. Skip news54 times

