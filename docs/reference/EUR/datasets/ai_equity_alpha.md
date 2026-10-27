# ai_equity_alpha — EUR 字段画像

> 自动生成于 2026-10-20 17:55　|　[← 返回索引](README.md)

## 一、数据集元信息

| 项 | 值 |
|---|---|
| 数据集 ID | `ai_equity_alpha` |
| 名称 | AI Equity Alpha Forecasts |
| 类别 | MODEL |
| 数据字段数(平台) | 582 |
| 覆盖率 | 0.8601 |
| 平台已有 alpha | 66 |
| valueScore | 4.0 |
| 金字塔倍率 | 1.3 |
| 数据类型 | VECTOR |
| delay | 1 |
| 状态 | scanned |

## 二、数据集描述（平台原文）

> ⚠️ 平台目录描述存在**错配**（已实测：insiders1 / imbalance5 的描述指向无关数据集）。以「五、全字段明细」的真实字段语义为准。

This dataset provides machine learning-driven forecasts of total return alpha for a broad universe of listed equities, with prediction horizons ranging from 1 to 12 months. It includes a comprehensive set of 291 explainability factors per stock, spanning areas such as accounting forensics, sentiment analysis, business model clarity, technical indicators, credit risk, valuation models, and more. The dataset delivers both daily and weekly updates, offering granular insights into the drivers of predicted returns. By combining forward-looking alpha scores with detailed factor breakdowns, this resource enables researchers and quantitative analysts to identify potential outperformers, understand the underlying reasons for forecasts, and enhance equity selection and risk management strategies. It

## 三、字段画像汇总

| 维度 | 结果 |
|---|---|
| 字段总数 | **582** |
| 类型分布 | VECTOR×582 |
| 平均覆盖率 | **0.860** |
| 覆盖率区间 | 0.86 ~ 0.86 |
| 更新频率（推断） | 事件/逐笔型（VECTOR） |
| 可用性评级 | 良（覆盖 70–90%，sub/robust 需关注） |

**覆盖率分档**

| 档 | 字段数 | 占比 |
|---|---:|---:|
| 高 (≥0.90) | 0 | 0.0% |
| 中 (0.70–0.90) | 582 | 100.0% |
| 低 (0.50–0.70) | 0 | 0.0% |
| 稀疏 (<0.50) | 0 | 0.0% |

**历史实测分布（field_profile_perf）**

| 判定 | 字段数 | 占比 |
|---|---:|---:|
| UNTESTED | 582 | 100.0% |

- 该数据集全部字段**尚未实测**（UNTESTED）⇒ 优先做尽

## 四、语义维度地图（自动归类）

| 语义族 | 字段数 | 平均覆盖 | 代表字段 |
|---|---:|---:|---|
| 盈利与财务 | 201 | 0.86 | accruals_analysis_factor、accruals_contribution_score、asset_impairment_frequency_metric |
| 其他 | 112 | 0.86 | accounting_forensics_factor、accounting_forensics_factor_3、balance_sheet_trend_metric |
| 价量与波动 | 97 | 0.86 | alpha_excess_return_forecast、alpha_score、business_model_volatility_score |
| 修正与预期 | 57 | 0.86 | analyst_coverage_breadth_metric、analyst_coverage_density_metric、analyst_earnings_revision_frequency |
| 风险与质量 | 53 | 0.86 | business_model_clarity_score、business_model_clarity_score_2、business_model_clarity_score_3 |
| 情绪与新闻 | 25 | 0.86 | buzz_intensity_score、buzz_intensity_score_2、buzz_trend_metric |
| 持仓与资金流 | 18 | 0.86 | fund_flow_prediction_metric、fund_flow_prediction_metric_2、fund_flow_prediction_metric_3 |
| 宏观与行业 | 10 | 0.86 | forecast_yield_metric、forecast_yield_metric_2、forecast_yield_metric_3 |
| 搜索与替代数据 | 9 | 0.86 | accounting_forensics_factor_2、company_size_factor_2、financing_structure_analysis_2 |

## 五、全字段明细

> 按 `best_sharpe` 降序（未测者置后）。`判定` 来自 `field_profile_perf`：ALIVE=历史测出过 S≥闸线（**不代表可提交**）；UNTESTED=未测；UNUSABLE/DEAD/AXIS_ONLY=已证否或仅可作轴。

| # | 字段名 | 类型 | 覆盖 | 语义族 | 测次 | best_S | best_2Y | best_sub | 判定 | 描述 |
|---:|---|---|---:|---|---:|---:|---:|---:|---|---|
| 1 | `accounting_forensics_factor` | VECTOR | 0.861 | 其他 | 0 | — | — | — | UNTESTED | Analysis of accounts for signs of financial trouble or strength. |
| 2 | `accounting_forensics_factor_2` | VECTOR | 0.861 | 搜索与替代数据 | 0 | — | — | — | UNTESTED | Alternative analysis of accounts for signs of financial trouble or strength. |
| 3 | `accounting_forensics_factor_3` | VECTOR | 0.861 | 其他 | 0 | — | — | — | UNTESTED | Analysis of accounts for signs of financial trouble or strength. |
| 4 | `accruals_analysis_factor` | VECTOR | 0.861 | 盈利与财务 | 0 | — | — | — | UNTESTED | Accounting-based measure reflecting accruals contribution to financial analysis. |
| 5 | `accruals_contribution_score` | VECTOR | 0.861 | 盈利与财务 | 0 | — | — | — | UNTESTED | Score indicating the contribution of accruals to financial analysis. |
| 6 | `alpha_excess_return_forecast` | VECTOR | 0.861 | 价量与波动 | 0 | — | — | — | UNTESTED | Forecast of excess return relative to a benchmark. |
| 7 | `alpha_score` | VECTOR | 0.861 | 价量与波动 | 0 | — | — | — | UNTESTED | Numeric score indicating relative forecasted return for a security. |
| 8 | `analyst_coverage_breadth_metric` | VECTOR | 0.861 | 修正与预期 | 0 | — | — | — | UNTESTED | Breadth of analyst coverage for the security. |
| 9 | `analyst_coverage_density_metric` | VECTOR | 0.861 | 修正与预期 | 0 | — | — | — | UNTESTED | Extent of analyst coverage for the security. |
| 10 | `analyst_earnings_revision_frequency` | VECTOR | 0.861 | 修正与预期 | 0 | — | — | — | UNTESTED | Frequency of analyst earnings forecast revisions. |
| 11 | `analyst_earnings_revision_intensity` | VECTOR | 0.861 | 修正与预期 | 0 | — | — | — | UNTESTED | Intensity of recent analyst earnings forecast revisions. |
| 12 | `analyst_forecast_revision_factor` | VECTOR | 0.861 | 修正与预期 | 0 | — | — | — | UNTESTED | Model capturing changes in analyst forecasts or recommendations. |
| 13 | `analyst_forecast_revision_factor_2` | VECTOR | 0.861 | 修正与预期 | 0 | — | — | — | UNTESTED | Metric capturing changes in analyst forecasts or recommendations. |
| 14 | `analyst_opinion_metric` | VECTOR | 0.861 | 修正与预期 | 0 | — | — | — | UNTESTED | Factor reflecting analyst opinions or perspectives. |
| 15 | `analyst_opinion_metric_2` | VECTOR | 0.861 | 修正与预期 | 0 | — | — | — | UNTESTED | Factor reflecting analyst opinions or perspectives. |
| 16 | `analyst_recommendation_consensus` | VECTOR | 0.861 | 修正与预期 | 0 | — | — | — | UNTESTED | Consensus level among analyst recommendations. |
| 17 | `analyst_recommendation_consensus_2` | VECTOR | 0.861 | 修正与预期 | 0 | — | — | — | UNTESTED | Alternative measure of analyst recommendation consensus. |
| 18 | `analyst_sentiment_consistency_score` | VECTOR | 0.861 | 修正与预期 | 0 | — | — | — | UNTESTED | Consistency of analyst sentiment over time. |
| 19 | `analyst_sentiment_consistency_score_2` | VECTOR | 0.861 | 修正与预期 | 0 | — | — | — | UNTESTED | Alternative measure of analyst sentiment consistency. |
| 20 | `analyst_sentiment_shift_score` | VECTOR | 0.861 | 修正与预期 | 0 | — | — | — | UNTESTED | Recent changes in analyst sentiment or recommendations. |
| 21 | `analyst_sentiment_shift_score_2` | VECTOR | 0.861 | 修正与预期 | 0 | — | — | — | UNTESTED | Alternative measure of analyst sentiment shift. |
| 22 | `analyst_target_price_deviation` | VECTOR | 0.861 | 修正与预期 | 0 | — | — | — | UNTESTED | Deviation of analyst target price from current price. |
| 23 | `asset_impairment_frequency_metric` | VECTOR | 0.861 | 盈利与财务 | 0 | — | — | — | UNTESTED | Frequency of asset write-downs or impairments. |
| 24 | `asset_impairment_frequency_metric_2` | VECTOR | 0.861 | 盈利与财务 | 0 | — | — | — | UNTESTED | Alternative measure of asset impairment frequency. |
| 25 | `asset_impairment_probability` | VECTOR | 0.861 | 盈利与财务 | 0 | — | — | — | UNTESTED | Likelihood that a company's assets will be written down due to impairment risk. |
| 26 | `asset_impairment_probability_2` | VECTOR | 0.861 | 盈利与财务 | 0 | — | — | — | UNTESTED | Probability of asset value reduction due to impairment. |
| 27 | `asset_impairment_risk` | VECTOR | 0.861 | 盈利与财务 | 0 | — | — | — | UNTESTED | Risk of asset value reduction due to impairment or write-downs. |
| 28 | `asset_liquidity_score` | VECTOR | 0.861 | 盈利与财务 | 0 | — | — | — | UNTESTED | Score indicating how easily assets can be converted to cash. |
| 29 | `asset_liquidity_score_2` | VECTOR | 0.861 | 盈利与财务 | 0 | — | — | — | UNTESTED | Alternative measure of asset liquidity. |
| 30 | `asset_replacement_cost_factor` | VECTOR | 0.861 | 修正与预期 | 0 | — | — | — | UNTESTED | Estimated cost to replace the company's assets. |
| 31 | `asset_replacement_cost_factor_2` | VECTOR | 0.861 | 修正与预期 | 0 | — | — | — | UNTESTED | Alternative estimate of the cost to replace company assets. |
| 32 | `asset_replacement_cost_factor_3` | VECTOR | 0.861 | 修正与预期 | 0 | — | — | — | UNTESTED | Third estimate of the cost to replace company assets. |
| 33 | `asset_turnover_ratio_metric` | VECTOR | 0.861 | 盈利与财务 | 0 | — | — | — | UNTESTED | Ratio indicating efficiency in using assets to generate revenue. |
| 34 | `asset_utilization_efficiency_score` | VECTOR | 0.861 | 盈利与财务 | 0 | — | — | — | UNTESTED | Efficiency in utilizing assets to generate returns. |
| 35 | `asset_utilization_efficiency_score_2` | VECTOR | 0.861 | 盈利与财务 | 0 | — | — | — | UNTESTED | Alternative measure of asset utilization efficiency. |
| 36 | `asset_utilization_efficiency_score_3` | VECTOR | 0.861 | 盈利与财务 | 0 | — | — | — | UNTESTED | Third measure of asset utilization efficiency. |
| 37 | `balance_sheet_trend_metric` | VECTOR | 0.861 | 其他 | 0 | — | — | — | UNTESTED | Model analyzing trends and changes in balance sheet items. |
| 38 | `balance_sheet_trend_metric_2` | VECTOR | 0.861 | 其他 | 0 | — | — | — | UNTESTED | Model analyzing trends and changes in balance sheet items. |
| 39 | `business_model_clarity_score` | VECTOR | 0.861 | 风险与质量 | 0 | — | — | — | UNTESTED | Certainty or uncertainty surrounding a company's business model. |
| 40 | `business_model_clarity_score_2` | VECTOR | 0.861 | 风险与质量 | 0 | — | — | — | UNTESTED | Alternative certainty or uncertainty score for business model. |
| 41 | `business_model_clarity_score_3` | VECTOR | 0.861 | 风险与质量 | 0 | — | — | — | UNTESTED | Score indicating the certainty or uncertainty of a company's business model. |
| 42 | `business_model_transparency_factor` | VECTOR | 0.861 | 其他 | 0 | — | — | — | UNTESTED | Degree of transparency in the company's business model. |
| 43 | `business_model_volatility_score` | VECTOR | 0.861 | 价量与波动 | 0 | — | — | — | UNTESTED | Volatility in the company's business model or operations. |
| 44 | `buzz_intensity_score` | VECTOR | 0.861 | 情绪与新闻 | 0 | — | — | — | UNTESTED | Measure of the level of market or media attention for a security. |
| 45 | `buzz_intensity_score_2` | VECTOR | 0.861 | 情绪与新闻 | 0 | — | — | — | UNTESTED | Measure of the level of market or media attention for a security. |
| 46 | `buzz_trend_metric` | VECTOR | 0.861 | 情绪与新闻 | 0 | — | — | — | UNTESTED | Measure of changes in market or media attention over time. |
| 47 | `cash_conversion_efficiency_score` | VECTOR | 0.861 | 盈利与财务 | 0 | — | — | — | UNTESTED | Efficiency of converting earnings into cash flow. |
| 48 | `cash_conversion_efficiency_score_2` | VECTOR | 0.861 | 风险与质量 | 0 | — | — | — | UNTESTED | Alternative measure of cash conversion efficiency. |
| 49 | `cashflow_trend_analysis` | VECTOR | 0.861 | 盈利与财务 | 0 | — | — | — | UNTESTED | Model analyzing trends and changes in cash flow statements. |
| 50 | `cashflow_trend_analysis_2` | VECTOR | 0.861 | 盈利与财务 | 0 | — | — | — | UNTESTED | Model analyzing trends and changes in cash flow statements. |
| 51 | `combined_technical_indicators` | VECTOR | 0.861 | 价量与波动 | 0 | — | — | — | UNTESTED | Aggregated technical indicators for momentum and mean reversion. |
| 52 | `combined_technical_indicators_2` | VECTOR | 0.861 | 价量与波动 | 0 | — | — | — | UNTESTED | Alternative aggregated technical indicators for momentum and reversion. |
| 53 | `combined_technical_indicators_3` | VECTOR | 0.861 | 价量与波动 | 0 | — | — | — | UNTESTED | Third aggregated technical indicators for momentum and reversion. |
| 54 | `company_physics_model_2` | VECTOR | 0.861 | 价量与波动 | 0 | — | — | — | UNTESTED | Mathematical model of shareholder returns using financial and technical properties. |
| 55 | `company_size_factor` | VECTOR | 0.861 | 其他 | 0 | — | — | — | UNTESTED | Factor representing the scale or market capitalization of a company. |
| 56 | `company_size_factor_2` | VECTOR | 0.861 | 搜索与替代数据 | 0 | — | — | — | UNTESTED | Alternative factor representing company scale or market capitalization. |
| 57 | `company_size_factor_3` | VECTOR | 0.861 | 其他 | 0 | — | — | — | UNTESTED | Third factor representing company scale or market capitalization. |
| 58 | `company_size_factor_4` | VECTOR | 0.861 | 其他 | 0 | — | — | — | UNTESTED | Factor representing the scale or market capitalization of a company. |
| 59 | `company_size_factor_5` | VECTOR | 0.861 | 其他 | 0 | — | — | — | UNTESTED | Factor representing the scale or market capitalization of a company. |
| 60 | `competitive_advantage_indicator` | VECTOR | 0.861 | 盈利与财务 | 0 | — | — | — | UNTESTED | Indicator of a company's ability to maintain profits due to competitive advantage. |
| 61 | `competitive_advantage_model` | VECTOR | 0.861 | 其他 | 0 | — | — | — | UNTESTED | Model analyzing the sustainability of a company's competitive advantage. |
| 62 | `competitive_advantage_model_2` | VECTOR | 0.861 | 其他 | 0 | — | — | — | UNTESTED | Model analyzing the sustainability of competitive advantage. |
| 63 | `competitive_advantage_score` | VECTOR | 0.861 | 盈利与财务 | 0 | — | — | — | UNTESTED | Indicator of a company's ability to maintain profits over competitors. |
| 64 | `correlation_risk_factor` | VECTOR | 0.861 | 盈利与财务 | 0 | — | — | — | UNTESTED | Model assessing the risk from correlated movements in assets. |
| 65 | `correlation_risk_factor_2` | VECTOR | 0.861 | 盈利与财务 | 0 | — | — | — | UNTESTED | Alternative model assessing risk from correlated asset movements. |
| 66 | `correlation_risk_factor_3` | VECTOR | 0.861 | 盈利与财务 | 0 | — | — | — | UNTESTED | Third model assessing risk from correlated asset movements. |
| 67 | `correlation_risk_factor_4` | VECTOR | 0.861 | 盈利与财务 | 0 | — | — | — | UNTESTED | Factor assessing risk from correlated movements in assets. |
| 68 | `correlation_risk_factor_5` | VECTOR | 0.861 | 盈利与财务 | 0 | — | — | — | UNTESTED | Factor assessing risk from correlated movements in assets. |
| 69 | `creditworthiness_assessment_factor` | VECTOR | 0.861 | 风险与质量 | 0 | — | — | — | UNTESTED | Model output assessing the risk of default or creditworthiness. |
| 70 | `creditworthiness_assessment_factor_2` | VECTOR | 0.861 | 风险与质量 | 0 | — | — | — | UNTESTED | Model assessing the risk of default or creditworthiness. |
| 71 | `debt_coverage_ratio_metric` | VECTOR | 0.861 | 盈利与财务 | 0 | — | — | — | UNTESTED | Ratio indicating the ability to cover debt obligations. |
| 72 | `debt_servicing_capacity_score` | VECTOR | 0.861 | 盈利与财务 | 0 | — | — | — | UNTESTED | Score reflecting the company's ability to service its debt. |
| 73 | `debt_to_equity_ratio_factor` | VECTOR | 0.861 | 盈利与财务 | 0 | — | — | — | UNTESTED | Ratio of total debt to shareholders' equity. |
| 74 | `dividend_consistency_factor` | VECTOR | 0.861 | 盈利与财务 | 0 | — | — | — | UNTESTED | Consistency of dividend payments over time. |
| 75 | `dividend_consistency_factor_2` | VECTOR | 0.861 | 盈利与财务 | 0 | — | — | — | UNTESTED | Alternative measure of dividend consistency. |
| 76 | `dividend_growth_rate_factor` | VECTOR | 0.861 | 盈利与财务 | 0 | — | — | — | UNTESTED | Rate of growth in dividend payments. |
| 77 | `dividend_payout_ratio_metric` | VECTOR | 0.861 | 盈利与财务 | 0 | — | — | — | UNTESTED | Proportion of earnings paid out as dividends. |
| 78 | `dividend_policy_analysis` | VECTOR | 0.861 | 盈利与财务 | 0 | — | — | — | UNTESTED | Analysis of dividend payments and company dividend policies. |
| 79 | `dividend_policy_analysis_2` | VECTOR | 0.861 | 盈利与财务 | 0 | — | — | — | UNTESTED | Alternative analysis of dividend payments and company policies. |
| 80 | `dividend_policy_analysis_3` | VECTOR | 0.861 | 盈利与财务 | 0 | — | — | — | UNTESTED | Third analysis of dividend payments and company policies. |
| 81 | `dividend_policy_analysis_4` | VECTOR | 0.861 | 盈利与财务 | 0 | — | — | — | UNTESTED | Analysis of dividend payments and company dividend policies. |
| 82 | `dividend_policy_analysis_5` | VECTOR | 0.861 | 盈利与财务 | 0 | — | — | — | UNTESTED | Analysis of dividend payments and company dividend policies. |
| 83 | `dividend_policy_stability_score` | VECTOR | 0.861 | 盈利与财务 | 0 | — | — | — | UNTESTED | Stability and predictability of the company's dividend policy. |
| 84 | `dividend_yield_stability_metric` | VECTOR | 0.861 | 盈利与财务 | 0 | — | — | — | UNTESTED | Stability of dividend yield over time. |
| 85 | `dividend_yield_stability_metric_2` | VECTOR | 0.861 | 盈利与财务 | 0 | — | — | — | UNTESTED | Alternative measure of dividend yield stability. |
| 86 | `earnings_growth_rate_analysis` | VECTOR | 0.861 | 盈利与财务 | 0 | — | — | — | UNTESTED | Analysis of earnings growth rates and their sustainability. |
| 87 | `earnings_growth_rate_analysis_2` | VECTOR | 0.861 | 盈利与财务 | 0 | — | — | — | UNTESTED | Alternative analysis of earnings growth rates and sustainability. |
| 88 | `earnings_growth_rate_analysis_3` | VECTOR | 0.861 | 盈利与财务 | 0 | — | — | — | UNTESTED | Analysis of earnings growth rates and their sustainability. |
| 89 | `earnings_per_share_growth_metric` | VECTOR | 0.861 | 盈利与财务 | 0 | — | — | — | UNTESTED | Growth rate of earnings per share. |
| 90 | `earnings_per_share_growth_metric_2` | VECTOR | 0.861 | 盈利与财务 | 0 | — | — | — | UNTESTED | Alternative measure of earnings per share growth. |
| 91 | `earnings_per_share_growth_metric_3` | VECTOR | 0.861 | 盈利与财务 | 0 | — | — | — | UNTESTED | Third measure of earnings per share growth. |
| 92 | `earnings_quality_score_10` | VECTOR | 0.861 | 盈利与财务 | 0 | — | — | — | UNTESTED | Assessment of the reliability and sustainability of reported earnings. |
| 93 | `earnings_quality_score_9` | VECTOR | 0.861 | 盈利与财务 | 0 | — | — | — | UNTESTED | Assessment of the reliability and sustainability of reported earnings. |
| 94 | `earnings_surprise_frequency_score` | VECTOR | 0.861 | 盈利与财务 | 0 | — | — | — | UNTESTED | Frequency of earnings results differing from expectations. |
| 95 | `earnings_surprise_frequency_score_2` | VECTOR | 0.861 | 盈利与财务 | 0 | — | — | — | UNTESTED | Alternative measure of earnings surprise frequency. |
| 96 | `earnings_surprise_magnitude_score` | VECTOR | 0.861 | 盈利与财务 | 0 | — | — | — | UNTESTED | Magnitude of earnings surprises relative to expectations. |
| 97 | `feature_agreement_indicator` | VECTOR | 0.861 | 其他 | 0 | — | — | — | UNTESTED | Indicator if the field relates to a data agreement. |
| 98 | `feature_cao_indicator` | VECTOR | 0.861 | 其他 | 0 | — | — | — | UNTESTED | Indicator if the field relates to a chief administrative officer. |
| 99 | `feature_category_label` | VECTOR | 0.861 | 其他 | 0 | — | — | — | UNTESTED | Label indicating the grouping of features by analytical purpose. |
| 100 | `feature_claim_indicator` | VECTOR | 0.861 | 其他 | 0 | — | — | — | UNTESTED | Indicator if the field relates to a legal claim. |
| 101 | `feature_column_indicator` | VECTOR | 0.861 | 其他 | 0 | — | — | — | UNTESTED | Indicator if the field is a column in the data table. |
| 102 | `feature_column_name` | VECTOR | 0.861 | 其他 | 0 | — | — | — | UNTESTED | Name of the column in the data table for the feature. |
| 103 | `feature_coo_indicator` | VECTOR | 0.861 | 其他 | 0 | — | — | — | UNTESTED | Indicator if the field relates to a chief operating officer. |
| 104 | `feature_data_type` | VECTOR | 0.861 | 其他 | 0 | — | — | — | UNTESTED | Data type of the feature, such as float or text. |
| 105 | `feature_description_text` | VECTOR | 0.861 | 其他 | 0 | — | — | — | UNTESTED | Textual description explaining the feature or factor. |
| 106 | `feature_dispute_indicator` | VECTOR | 0.861 | 其他 | 0 | — | — | — | UNTESTED | Indicator if the field relates to a legal dispute. |
| 107 | `feature_example_indicator` | VECTOR | 0.861 | 其他 | 0 | — | — | — | UNTESTED | Indicator if the field is a sample value for the feature. |
| 108 | `feature_example_value` | VECTOR | 0.861 | 其他 | 0 | — | — | — | UNTESTED | Sample value for the feature or factor. |
| 109 | `feature_float_indicator` | VECTOR | 0.861 | 其他 | 0 | — | — | — | UNTESTED | Indicator if the feature is a float data type. |
| 110 | `feature_general_counsel_indicator` | VECTOR | 0.861 | 其他 | 0 | — | — | — | UNTESTED | Indicator if the field relates to a general counsel. |
| 111 | `feature_london_england_indicator` | VECTOR | 0.861 | 其他 | 0 | — | — | — | UNTESTED | Indicator if the field relates to London, England. |
| 112 | `feature_losses_indicator` | VECTOR | 0.861 | 其他 | 0 | — | — | — | UNTESTED | Indicator if the field relates to legal losses. |
| 113 | `feature_name_label` | VECTOR | 0.861 | 其他 | 0 | — | — | — | UNTESTED | Name or label of the feature or factor. |
| 114 | `feature_nan_indicator` | VECTOR | 0.861 | 其他 | 0 | — | — | — | UNTESTED | Indicator for missing or undefined data in the feature. |
| 115 | `feature_plus_x_innovation_hub_indicator` | VECTOR | 0.861 | 其他 | 0 | — | — | — | UNTESTED | Indicator if the field relates to Plus X Innovation Hub. |
| 116 | `feature_string_indicator` | VECTOR | 0.861 | 其他 | 0 | — | — | — | UNTESTED | Indicator if the feature is a string data type. |
| 117 | `feature_subcategory_label` | VECTOR | 0.861 | 其他 | 0 | — | — | — | UNTESTED | Label indicating the sub-grouping of features for detailed analysis. |
| 118 | `feature_subscriber_parties_indicator` | VECTOR | 0.861 | 其他 | 0 | — | — | — | UNTESTED | Indicator if the field relates to subscriber parties. |
| 119 | `feature_text_indicator` | VECTOR | 0.861 | 其他 | 0 | — | — | — | UNTESTED | Indicator if the feature is a text data type. |
| 120 | `feature_worldquant_llc_indicator` | VECTOR | 0.861 | 其他 | 0 | — | — | — | UNTESTED | Indicator if the field relates to WorldQuant, LLC. |
| 121 | `financial_change_trend_analysis` | VECTOR | 0.861 | 其他 | 0 | — | — | — | UNTESTED | Analysis of trends across all financial statements. |
| 122 | `financial_statement_volatility_factor` | VECTOR | 0.861 | 价量与波动 | 0 | — | — | — | UNTESTED | Measure of variability in key financial statement items. |
| 123 | `financial_statement_volatility_factor_2` | VECTOR | 0.861 | 价量与波动 | 0 | — | — | — | UNTESTED | Alternative measure of financial statement volatility. |
| 124 | `financial_yield_analysis` | VECTOR | 0.861 | 盈利与财务 | 0 | — | — | — | UNTESTED | Analysis of financial yields such as dividend or earnings yield. |
| 125 | `financial_yield_analysis_2` | VECTOR | 0.861 | 盈利与财务 | 0 | — | — | — | UNTESTED | Alternative analysis of financial yields such as dividend or earnings yield. |
| 126 | `financial_yield_analysis_3` | VECTOR | 0.861 | 盈利与财务 | 0 | — | — | — | UNTESTED | Analysis of financial yields such as dividend or earnings yield. |
| 127 | `financing_structure_analysis` | VECTOR | 0.861 | 其他 | 0 | — | — | — | UNTESTED | Analysis of a company's financing activities and capital structure. |
| 128 | `financing_structure_analysis_2` | VECTOR | 0.861 | 搜索与替代数据 | 0 | — | — | — | UNTESTED | Alternative analysis of company financing activities and structure. |
| 129 | `financing_structure_analysis_3` | VECTOR | 0.861 | 其他 | 0 | — | — | — | UNTESTED | Third analysis of company financing activities and structure. |
| 130 | `financing_structure_analysis_4` | VECTOR | 0.861 | 其他 | 0 | — | — | — | UNTESTED | Analysis of a company's financing activities and capital structure. |
| 131 | `financing_structure_analysis_5` | VECTOR | 0.861 | 其他 | 0 | — | — | — | UNTESTED | Analysis of a company's financing activities and capital structure. |
| 132 | `forecast_accuracy_variance_score` | VECTOR | 0.861 | 修正与预期 | 0 | — | — | — | UNTESTED | Variance in the accuracy of analyst or model forecasts. |
| 133 | `forecast_dispersion_metric` | VECTOR | 0.861 | 修正与预期 | 0 | — | — | — | UNTESTED | Dispersion among analyst or model forecasts. |
| 134 | `forecast_dispersion_metric_2` | VECTOR | 0.861 | 搜索与替代数据 | 0 | — | — | — | UNTESTED | Alternative measure of forecast dispersion. |
| 135 | `forecast_error_magnitude_metric` | VECTOR | 0.861 | 盈利与财务 | 0 | — | — | — | UNTESTED | Magnitude of errors in earnings or revenue forecasts. |
| 136 | `forecast_error_magnitude_metric_2` | VECTOR | 0.861 | 搜索与替代数据 | 0 | — | — | — | UNTESTED | Alternative measure of forecast error magnitude. |
| 137 | `forecast_error_magnitude_metric_3` | VECTOR | 0.861 | 其他 | 0 | — | — | — | UNTESTED | Third measure of forecast error magnitude. |
| 138 | `forecast_value_accuracy_metric` | VECTOR | 0.861 | 其他 | 0 | — | — | — | UNTESTED | Metric evaluating the value and accuracy of forecasts. |
| 139 | `forecast_value_accuracy_metric_2` | VECTOR | 0.861 | 其他 | 0 | — | — | — | UNTESTED | Metric evaluating the accuracy and value of forecasts. |
| 140 | `forecast_value_accuracy_metric_3` | VECTOR | 0.861 | 其他 | 0 | — | — | — | UNTESTED | Metric evaluating the value and accuracy of forecasts. |
| 141 | `forecast_yield_metric` | VECTOR | 0.861 | 宏观与行业 | 0 | — | — | — | UNTESTED | Analysis of expected future yields for a security. |
| 142 | `forecast_yield_metric_2` | VECTOR | 0.861 | 宏观与行业 | 0 | — | — | — | UNTESTED | Alternative analysis of expected future yields for a security. |
| 143 | `forecast_yield_metric_3` | VECTOR | 0.861 | 宏观与行业 | 0 | — | — | — | UNTESTED | Analysis of expected future yields for a security. |
| 144 | `free_cashflow_margin_factor` | VECTOR | 0.861 | 盈利与财务 | 0 | — | — | — | UNTESTED | Free cash flow as a percentage of revenue. |
| 145 | `free_cashflow_yield_metric` | VECTOR | 0.861 | 盈利与财务 | 0 | — | — | — | UNTESTED | Free cash flow as a percentage of market capitalization. |
| 146 | `fund_flow_prediction_metric` | VECTOR | 0.861 | 持仓与资金流 | 0 | — | — | — | UNTESTED | Model predicting the movement of funds into or out of securities. |
| 147 | `fund_flow_prediction_metric_2` | VECTOR | 0.861 | 持仓与资金流 | 0 | — | — | — | UNTESTED | Alternative model predicting fund movements into or out of securities. |
| 148 | `fund_flow_prediction_metric_3` | VECTOR | 0.861 | 持仓与资金流 | 0 | — | — | — | UNTESTED | Third model predicting fund movements into or out of securities. |
| 149 | `fund_flow_prediction_metric_4` | VECTOR | 0.861 | 持仓与资金流 | 0 | — | — | — | UNTESTED | Model predicting the movement of funds into or out of securities. |
| 150 | `fund_flow_prediction_metric_5` | VECTOR | 0.861 | 持仓与资金流 | 0 | — | — | — | UNTESTED | Model predicting the movement of funds into or out of securities. |
| 151 | `historic_earnings_surprise_score` | VECTOR | 0.861 | 盈利与财务 | 0 | — | — | — | UNTESTED | Measure of past earnings results versus expectations. |
| 152 | `historic_earnings_surprise_score_2` | VECTOR | 0.861 | 盈利与财务 | 0 | — | — | — | UNTESTED | Score measuring past earnings results versus expectations. |
| 153 | `historic_earnings_surprise_score_3` | VECTOR | 0.861 | 盈利与财务 | 0 | — | — | — | UNTESTED | Score measuring past earnings results versus expectations. |
| 154 | `income_statement_trend_metric` | VECTOR | 0.861 | 其他 | 0 | — | — | — | UNTESTED | Model analyzing trends and changes in income statement items. |
| 155 | `information_opacity_score` | VECTOR | 0.861 | 风险与质量 | 0 | — | — | — | UNTESTED | Measure of the lack of transparency or clarity in information. |
| 156 | `information_opacity_score_2` | VECTOR | 0.861 | 风险与质量 | 0 | — | — | — | UNTESTED | Alternative measure of information transparency or clarity. |
| 157 | `information_opacity_score_3` | VECTOR | 0.861 | 风险与质量 | 0 | — | — | — | UNTESTED | Third measure of information transparency or clarity. |
| 158 | `information_opacity_score_4` | VECTOR | 0.861 | 风险与质量 | 0 | — | — | — | UNTESTED | Score measuring the lack of transparency or clarity in information. |
| 159 | `information_opacity_score_5` | VECTOR | 0.861 | 风险与质量 | 0 | — | — | — | UNTESTED | Score measuring the lack of transparency or clarity in information. |
| 160 | `intrinsic_valuation_estimate` | VECTOR | 0.861 | 修正与预期 | 0 | — | — | — | UNTESTED | Model estimating the fundamental value of a company. |
| 161 | `intrinsic_valuation_estimate_2` | VECTOR | 0.861 | 修正与预期 | 0 | — | — | — | UNTESTED | Alternative model estimating the fundamental value of a company. |
| 162 | `intrinsic_valuation_estimate_3` | VECTOR | 0.861 | 修正与预期 | 0 | — | — | — | UNTESTED | Model estimating the fundamental value of a company. |
| 163 | `liquidity_buffer_indicator` | VECTOR | 0.861 | 价量与波动 | 0 | — | — | — | UNTESTED | Indicator of the company's short-term liquidity position. |
| 164 | `long_term_business_uncertainty` | VECTOR | 0.861 | 其他 | 0 | — | — | — | UNTESTED | Measure of uncertainty in a company's business model over a long horizon. |
| 165 | `long_term_business_uncertainty_2` | VECTOR | 0.861 | 其他 | 0 | — | — | — | UNTESTED | Measure of uncertainty in a company's business model over a long horizon. |
| 166 | `long_term_physics_model` | VECTOR | 0.861 | 价量与波动 | 0 | — | — | — | UNTESTED | Factor modeling shareholder returns over a long period using mathematical models. |
| 167 | `long_term_physics_model_2` | VECTOR | 0.861 | 价量与波动 | 0 | — | — | — | UNTESTED | Factor modeling shareholder returns over a long period using mathematical models. |
| 168 | `long_term_technical_trend_indicator` | VECTOR | 0.861 | 价量与波动 | 0 | — | — | — | UNTESTED | Technical indicator measuring long-term price trends. |
| 169 | `long_term_technical_trend_indicator_2` | VECTOR | 0.861 | 价量与波动 | 0 | — | — | — | UNTESTED | Alternative technical indicator measuring long-term price trends. |
| 170 | `long_term_technical_trend_indicator_3` | VECTOR | 0.861 | 价量与波动 | 0 | — | — | — | UNTESTED | Third technical indicator measuring long-term price trends. |
| 171 | `long_term_technical_trend_indicator_4` | VECTOR | 0.861 | 价量与波动 | 0 | — | — | — | UNTESTED | Technical indicator measuring long-term price trends. |
| 172 | `long_term_technical_valuation_model` | VECTOR | 0.861 | 价量与波动 | 0 | — | — | — | UNTESTED | Technical valuation model focused on long-term price trends. |
| 173 | `long_term_technical_valuation_model_2` | VECTOR | 0.861 | 价量与波动 | 0 | — | — | — | UNTESTED | Alternative technical valuation model focused on long-term price trends. |
| 174 | `long_term_technical_valuation_model_3` | VECTOR | 0.861 | 价量与波动 | 0 | — | — | — | UNTESTED | Technical valuation model focused on long-term price trends. |
| 175 | `market_attention_score` | VECTOR | 0.861 | 情绪与新闻 | 0 | — | — | — | UNTESTED | Measure of market or media attention to a security. |
| 176 | `medium_term_business_uncertainty` | VECTOR | 0.861 | 其他 | 0 | — | — | — | UNTESTED | Measure of uncertainty in a company's business model over a medium horizon. |
| 177 | `medium_term_business_uncertainty_2` | VECTOR | 0.861 | 其他 | 0 | — | — | — | UNTESTED | Measure of uncertainty in a company's business model over a medium horizon. |
| 178 | `medium_term_physics_model` | VECTOR | 0.861 | 价量与波动 | 0 | — | — | — | UNTESTED | Factor modeling shareholder returns over a medium period. |
| 179 | `medium_term_physics_model_2` | VECTOR | 0.861 | 价量与波动 | 0 | — | — | — | UNTESTED | Factor modeling shareholder returns over a medium period. |
| 180 | `medium_term_technical_trend_indicator` | VECTOR | 0.861 | 价量与波动 | 0 | — | — | — | UNTESTED | Technical indicator measuring medium-term price trends. |
| 181 | `medium_term_technical_trend_indicator_2` | VECTOR | 0.861 | 价量与波动 | 0 | — | — | — | UNTESTED | Alternative technical indicator measuring medium-term price trends. |
| 182 | `medium_term_technical_trend_indicator_3` | VECTOR | 0.861 | 价量与波动 | 0 | — | — | — | UNTESTED | Third technical indicator measuring medium-term price trends. |
| 183 | `medium_term_technical_trend_indicator_4` | VECTOR | 0.861 | 价量与波动 | 0 | — | — | — | UNTESTED | Technical indicator measuring medium-term price trends. |
| 184 | `medium_term_technical_valuation_model` | VECTOR | 0.861 | 价量与波动 | 0 | — | — | — | UNTESTED | Technical valuation model focused on medium-term price trends. |
| 185 | `medium_term_technical_valuation_model_2` | VECTOR | 0.861 | 价量与波动 | 0 | — | — | — | UNTESTED | Alternative technical valuation model focused on medium-term price trends. |
| 186 | `medium_term_technical_valuation_model_3` | VECTOR | 0.861 | 价量与波动 | 0 | — | — | — | UNTESTED | Technical valuation model focused on medium-term price trends. |
| 187 | `momentum_reversal_indicator` | VECTOR | 0.861 | 价量与波动 | 0 | — | — | — | UNTESTED | Indicator of potential reversal in price momentum. |
| 188 | `momentum_reversal_indicator_2` | VECTOR | 0.861 | 价量与波动 | 0 | — | — | — | UNTESTED | Alternative indicator of momentum reversal. |
| 189 | `momentum_score` | VECTOR | 0.861 | 盈利与财务 | 0 | — | — | — | UNTESTED | Score representing the tendency of an asset's price to continue moving in its current direction. |
| 190 | `nlp_sentiment_alpha_factor` | VECTOR | 0.861 | 情绪与新闻 | 0 | — | — | — | UNTESTED | Analysis of stock perception and performance using natural language processing. |
| 191 | `nlp_sentiment_alpha_factor_2` | VECTOR | 0.861 | 情绪与新闻 | 0 | — | — | — | UNTESTED | Alternative analysis of stock perception and performance using NLP. |
| 192 | `nlp_sentiment_alpha_factor_3` | VECTOR | 0.861 | 情绪与新闻 | 0 | — | — | — | UNTESTED | Analysis of perception and sentiment using natural language processing. |
| 193 | `operating_cashflow_growth_metric` | VECTOR | 0.861 | 盈利与财务 | 0 | — | — | — | UNTESTED | Growth rate of operating cash flow. |
| 194 | `operating_cashflow_growth_metric_2` | VECTOR | 0.861 | 盈利与财务 | 0 | — | — | — | UNTESTED | Alternative measure of operating cash flow growth. |
| 195 | `operating_cashflow_stability_factor` | VECTOR | 0.861 | 盈利与财务 | 0 | — | — | — | UNTESTED | Stability of operating cash flows over time. |
| 196 | `operating_cashflow_stability_factor_2` | VECTOR | 0.861 | 盈利与财务 | 0 | — | — | — | UNTESTED | Alternative measure of operating cash flow stability. |
| 197 | `operating_cashflow_stability_factor_3` | VECTOR | 0.861 | 盈利与财务 | 0 | — | — | — | UNTESTED | Third measure of operating cash flow stability. |
| 198 | `operating_cashflow_stability_factor_4` | VECTOR | 0.861 | 盈利与财务 | 0 | — | — | — | UNTESTED | Fourth measure of operating cash flow stability. |
| 199 | `operating_expense_ratio_factor` | VECTOR | 0.861 | 盈利与财务 | 0 | — | — | — | UNTESTED | Ratio of operating expenses to total revenue. |
| 200 | `operating_income_variability_score` | VECTOR | 0.861 | 风险与质量 | 0 | — | — | — | UNTESTED | Variability in operating income over time. |
| 201 | `operating_income_variability_score_2` | VECTOR | 0.861 | 风险与质量 | 0 | — | — | — | UNTESTED | Alternative measure of operating income variability. |
| 202 | `operating_leverage_factor` | VECTOR | 0.861 | 其他 | 0 | — | — | — | UNTESTED | Degree to which operating income is affected by changes in sales. |
| 203 | `operating_leverage_factor_2` | VECTOR | 0.861 | 搜索与替代数据 | 0 | — | — | — | UNTESTED | Alternative measure of operating leverage. |
| 204 | `operating_leverage_factor_3` | VECTOR | 0.861 | 其他 | 0 | — | — | — | UNTESTED | Third measure of operating leverage. |
| 205 | `operating_margin_trend_score` | VECTOR | 0.861 | 盈利与财务 | 0 | — | — | — | UNTESTED | Trend in operating margin over recent periods. |
| 206 | `operating_profit_margin_factor` | VECTOR | 0.861 | 盈利与财务 | 0 | — | — | — | UNTESTED | Operating profit as a percentage of revenue. |
| 207 | `operating_profit_margin_factor_2` | VECTOR | 0.861 | 盈利与财务 | 0 | — | — | — | UNTESTED | Alternative measure of operating profit margin. |
| 208 | `operating_profit_margin_factor_3` | VECTOR | 0.861 | 盈利与财务 | 0 | — | — | — | UNTESTED | Third measure of operating profit margin. |
| 209 | `operational_efficiency_metric` | VECTOR | 0.861 | 其他 | 0 | — | — | — | UNTESTED | Measure of how effectively a company utilizes its resources. |
| 210 | `operational_efficiency_metric_2` | VECTOR | 0.861 | 其他 | 0 | — | — | — | UNTESTED | Model analyzing operational efficiency. |
| 211 | `operational_efficiency_model` | VECTOR | 0.861 | 其他 | 0 | — | — | — | UNTESTED | Model analyzing operational efficiency of a company. |
| 212 | `operational_efficiency_score` | VECTOR | 0.861 | 风险与质量 | 0 | — | — | — | UNTESTED | Score measuring how effectively a company uses its resources. |
| 213 | `perception_trend_metric` | VECTOR | 0.861 | 修正与预期 | 0 | — | — | — | UNTESTED | Measure of changes in market or analyst perception over time. |
| 214 | `predicted_earnings_surprise` | VECTOR | 0.861 | 盈利与财务 | 0 | — | — | — | UNTESTED | Model output predicting future earnings surprises. |
| 215 | `predicted_earnings_surprise_2` | VECTOR | 0.861 | 盈利与财务 | 0 | — | — | — | UNTESTED | Model output predicting future earnings surprises. |
| 216 | `predicted_earnings_surprise_3` | VECTOR | 0.861 | 盈利与财务 | 0 | — | — | — | UNTESTED | Model output predicting future earnings surprises. |
| 217 | `present_physics_model` | VECTOR | 0.861 | 价量与波动 | 0 | — | — | — | UNTESTED | Factor modeling current shareholder returns using mathematical models. |
| 218 | `present_physics_model_2` | VECTOR | 0.861 | 价量与波动 | 0 | — | — | — | UNTESTED | Factor modeling current shareholder returns. |
| 219 | `price_momentum_reversal_indicator` | VECTOR | 0.861 | 价量与波动 | 0 | — | — | — | UNTESTED | Indicator of reversal in recent price momentum. |
| 220 | `price_momentum_strength_metric` | VECTOR | 0.861 | 价量与波动 | 0 | — | — | — | UNTESTED | Strength of recent price momentum for the security. |
| 221 | `price_to_book_ratio_metric` | VECTOR | 0.861 | 价量与波动 | 0 | — | — | — | UNTESTED | Ratio of market price to book value per share. |
| 222 | `price_to_book_ratio_metric_2` | VECTOR | 0.861 | 价量与波动 | 0 | — | — | — | UNTESTED | Alternative measure of price to book value ratio. |
| 223 | `price_to_cashflow_ratio_metric` | VECTOR | 0.861 | 盈利与财务 | 0 | — | — | — | UNTESTED | Ratio of share price to cash flow per share. |
| 224 | `price_to_cashflow_ratio_metric_2` | VECTOR | 0.861 | 盈利与财务 | 0 | — | — | — | UNTESTED | Alternative measure of price to cash flow ratio. |
| 225 | `price_to_cashflow_ratio_metric_3` | VECTOR | 0.861 | 盈利与财务 | 0 | — | — | — | UNTESTED | Third measure of price to cash flow ratio. |
| 226 | `price_to_earnings_ratio_factor` | VECTOR | 0.861 | 盈利与财务 | 0 | — | — | — | UNTESTED | Ratio of share price to earnings per share. |
| 227 | `price_to_free_cashflow_ratio` | VECTOR | 0.861 | 盈利与财务 | 0 | — | — | — | UNTESTED | Ratio of share price to free cash flow per share. |
| 228 | `price_to_free_cashflow_ratio_2` | VECTOR | 0.861 | 盈利与财务 | 0 | — | — | — | UNTESTED | Alternative measure of price to free cash flow ratio. |
| 229 | `price_to_operating_cashflow_ratio` | VECTOR | 0.861 | 盈利与财务 | 0 | — | — | — | UNTESTED | Ratio of share price to operating cash flow per share. |
| 230 | `price_to_operating_cashflow_ratio_2` | VECTOR | 0.861 | 盈利与财务 | 0 | — | — | — | UNTESTED | Alternative measure of price to operating cash flow ratio. |
| 231 | `price_to_sales_ratio_metric` | VECTOR | 0.861 | 价量与波动 | 0 | — | — | — | UNTESTED | Ratio of share price to sales per share. |
| 232 | `price_to_sales_ratio_metric_2` | VECTOR | 0.861 | 价量与波动 | 0 | — | — | — | UNTESTED | Alternative measure of price to sales ratio. |
| 233 | `price_to_sales_ratio_metric_3` | VECTOR | 0.861 | 价量与波动 | 0 | — | — | — | UNTESTED | Third measure of price to sales ratio. |
| 234 | `profit_margin_stability_score` | VECTOR | 0.861 | 盈利与财务 | 0 | — | — | — | UNTESTED | Stability of profit margins over time. |
| 235 | `profit_margin_stability_score_2` | VECTOR | 0.861 | 盈利与财务 | 0 | — | — | — | UNTESTED | Alternative measure of profit margin stability. |
| 236 | `profitability_consistency_factor` | VECTOR | 0.861 | 盈利与财务 | 0 | — | — | — | UNTESTED | Consistency of profitability across periods. |
| 237 | `profitability_consistency_factor_2` | VECTOR | 0.861 | 盈利与财务 | 0 | — | — | — | UNTESTED | Alternative measure of profitability consistency. |
| 238 | `profitability_consistency_factor_3` | VECTOR | 0.861 | 盈利与财务 | 0 | — | — | — | UNTESTED | Third measure of profitability consistency. |
| 239 | `pure_alpha_generation_metric` | VECTOR | 0.861 | 价量与波动 | 0 | — | — | — | UNTESTED | Model designed to generate returns independent of market direction. |
| 240 | `pure_alpha_generation_metric_2` | VECTOR | 0.861 | 价量与波动 | 0 | — | — | — | UNTESTED | Alternative model for generating returns independent of market direction. |
| 241 | `pure_alpha_generation_metric_3` | VECTOR | 0.861 | 价量与波动 | 0 | — | — | — | UNTESTED | Third model for generating returns independent of market direction. |
| 242 | `pure_alpha_generation_metric_4` | VECTOR | 0.861 | 价量与波动 | 0 | — | — | — | UNTESTED | Metric designed to generate returns independent of market direction. |
| 243 | `pure_alpha_generation_metric_5` | VECTOR | 0.861 | 价量与波动 | 0 | — | — | — | UNTESTED | Metric designed to generate returns independent of market direction. |
| 244 | `recent_business_uncertainty` | VECTOR | 0.861 | 其他 | 0 | — | — | — | UNTESTED | Measure of uncertainty in a company's business model in the recent period. |
| 245 | `recent_business_uncertainty_2` | VECTOR | 0.861 | 其他 | 0 | — | — | — | UNTESTED | Measure of uncertainty in a company's business model in the recent period. |
| 246 | `relative_valuation_comparison` | VECTOR | 0.861 | 其他 | 0 | — | — | — | UNTESTED | Valuation based on comparison to peers or benchmarks. |
| 247 | `relative_valuation_comparison_2` | VECTOR | 0.861 | 搜索与替代数据 | 0 | — | — | — | UNTESTED | Alternative valuation based on comparison to peers or benchmarks. |
| 248 | `relative_valuation_comparison_3` | VECTOR | 0.861 | 其他 | 0 | — | — | — | UNTESTED | Valuation based on comparison to peers or benchmarks. |
| 249 | `replacement_asset_value_model` | VECTOR | 0.861 | 盈利与财务 | 0 | — | — | — | UNTESTED | Model estimating the cost to replace a company's assets. |
| 250 | `replacement_asset_value_model_2` | VECTOR | 0.861 | 盈利与财务 | 0 | — | — | — | UNTESTED | Alternative model estimating the cost to replace a company's assets. |
| 251 | `replacement_asset_value_model_3` | VECTOR | 0.861 | 盈利与财务 | 0 | — | — | — | UNTESTED | Model estimating the cost to replace a company's assets. |
| 252 | `return_on_assets_consistency_score` | VECTOR | 0.861 | 盈利与财务 | 0 | — | — | — | UNTESTED | Consistency of return on assets over time. |
| 253 | `return_on_equity_trend_score` | VECTOR | 0.861 | 盈利与财务 | 0 | — | — | — | UNTESTED | Trend in return on equity over time. |
| 254 | `return_on_equity_trend_score_2` | VECTOR | 0.861 | 盈利与财务 | 0 | — | — | — | UNTESTED | Alternative measure of return on equity trend. |
| 255 | `revenue_growth_consistency_score` | VECTOR | 0.861 | 盈利与财务 | 0 | — | — | — | UNTESTED | Consistency of revenue growth over multiple periods. |
| 256 | `revenue_growth_consistency_score_2` | VECTOR | 0.861 | 盈利与财务 | 0 | — | — | — | UNTESTED | Alternative measure of revenue growth consistency. |
| 257 | `revenue_growth_consistency_score_3` | VECTOR | 0.861 | 盈利与财务 | 0 | — | — | — | UNTESTED | Third measure of revenue growth consistency. |
| 258 | `reversion_score` | VECTOR | 0.861 | 盈利与财务 | 0 | — | — | — | UNTESTED | Score representing the tendency of an asset's price to revert to its mean. |
| 259 | `share_buyback_activity_analysis` | VECTOR | 0.861 | 其他 | 0 | — | — | — | UNTESTED | Analysis of company share repurchase activities. |
| 260 | `share_buyback_activity_analysis_2` | VECTOR | 0.861 | 搜索与替代数据 | 0 | — | — | — | UNTESTED | Alternative analysis of company share repurchase activities. |
| 261 | `share_buyback_activity_analysis_3` | VECTOR | 0.861 | 其他 | 0 | — | — | — | UNTESTED | Third analysis of company share repurchase activities. |
| 262 | `share_buyback_activity_analysis_4` | VECTOR | 0.861 | 其他 | 0 | — | — | — | UNTESTED | Analysis of company share repurchase activities. |
| 263 | `share_buyback_activity_analysis_5` | VECTOR | 0.861 | 其他 | 0 | — | — | — | UNTESTED | Analysis of company share repurchase activities. |
| 264 | `shareholder_treatment_metric` | VECTOR | 0.861 | 持仓与资金流 | 0 | — | — | — | UNTESTED | Analysis of financing cashflow items and related metrics affecting shareholders. |
| 265 | `shareholder_treatment_metric_2` | VECTOR | 0.861 | 持仓与资金流 | 0 | — | — | — | UNTESTED | Alternative analysis of financing cashflow items affecting shareholders. |
| 266 | `shareholder_treatment_metric_3` | VECTOR | 0.861 | 持仓与资金流 | 0 | — | — | — | UNTESTED | Analysis of financing cashflow items and related shareholder metrics. |
| 267 | `shareholder_yield_metric` | VECTOR | 0.861 | 盈利与财务 | 0 | — | — | — | UNTESTED | Analysis of total returns to shareholders from dividends and buybacks. |
| 268 | `shareholder_yield_metric_2` | VECTOR | 0.861 | 盈利与财务 | 0 | — | — | — | UNTESTED | Alternative analysis of total returns to shareholders from dividends and buybacks. |
| 269 | `shareholder_yield_metric_3` | VECTOR | 0.861 | 盈利与财务 | 0 | — | — | — | UNTESTED | Third analysis of total returns to shareholders from dividends and buybacks. |
| 270 | `shareholder_yield_metric_4` | VECTOR | 0.861 | 盈利与财务 | 0 | — | — | — | UNTESTED | Analysis of total returns to shareholders from dividends and buybacks. |
| 271 | `short_interest_ratio_metric_2` | VECTOR | 0.861 | 其他 | 0 | — | — | — | UNTESTED | Ratio of shares sold short to total shares outstanding. |
| 272 | `short_term_physics_model` | VECTOR | 0.861 | 价量与波动 | 0 | — | — | — | UNTESTED | Factor modeling shareholder returns over a short period. |
| 273 | `short_term_physics_model_2` | VECTOR | 0.861 | 价量与波动 | 0 | — | — | — | UNTESTED | Factor modeling shareholder returns over a short period. |
| 274 | `short_term_technical_trend_indicator` | VECTOR | 0.861 | 价量与波动 | 0 | — | — | — | UNTESTED | Technical indicator measuring short-term price trends. |
| 275 | `short_term_technical_trend_indicator_2` | VECTOR | 0.861 | 价量与波动 | 0 | — | — | — | UNTESTED | Alternative technical indicator measuring short-term price trends. |
| 276 | `short_term_technical_trend_indicator_3` | VECTOR | 0.861 | 价量与波动 | 0 | — | — | — | UNTESTED | Technical indicator measuring short-term price trends. |
| 277 | `short_term_technical_valuation_model` | VECTOR | 0.861 | 价量与波动 | 0 | — | — | — | UNTESTED | Technical valuation model focused on short-term price trends. |
| 278 | `short_term_technical_valuation_model_2` | VECTOR | 0.861 | 价量与波动 | 0 | — | — | — | UNTESTED | Alternative technical valuation model focused on short-term price trends. |
| 279 | `short_term_technical_valuation_model_3` | VECTOR | 0.861 | 价量与波动 | 0 | — | — | — | UNTESTED | Technical valuation model focused on short-term price trends. |
| 280 | `technical_indicator_composite` | VECTOR | 0.861 | 价量与波动 | 0 | — | — | — | UNTESTED | Quantitative model of momentum, reversion, and other price properties. |
| 281 | `technical_indicator_composite_2` | VECTOR | 0.861 | 价量与波动 | 0 | — | — | — | UNTESTED | Alternative quantitative model of momentum, reversion, and price properties. |
| 282 | `technical_indicator_composite_3` | VECTOR | 0.861 | 价量与波动 | 0 | — | — | — | UNTESTED | Aggregated technical indicators for momentum and reversion. |
| 283 | `trend_in_buzz_score` | VECTOR | 0.861 | 情绪与新闻 | 0 | — | — | — | UNTESTED | Metric indicating changes in market or media attention over time. |
| 284 | `trend_in_buzz_score_2` | VECTOR | 0.861 | 情绪与新闻 | 0 | — | — | — | UNTESTED | Metric indicating changes in market or media attention over time. |
| 285 | `trend_in_perception_score` | VECTOR | 0.861 | 修正与预期 | 0 | — | — | — | UNTESTED | Metric indicating changes in market or analyst perception over time. |
| 286 | `trend_in_perception_score_2` | VECTOR | 0.861 | 修正与预期 | 0 | — | — | — | UNTESTED | Metric indicating changes in market or analyst perception over time. |
| 287 | `valuation_model_suite` | VECTOR | 0.861 | 其他 | 0 | — | — | — | UNTESTED | Suite of models estimating company value and forecasting changes in valuation. |
| 288 | `valuation_model_suite_2` | VECTOR | 0.861 | 搜索与替代数据 | 0 | — | — | — | UNTESTED | Alternative suite of models estimating company value and changes. |
| 289 | `volatility_of_returns_factor` | VECTOR | 0.861 | 价量与波动 | 0 | — | — | — | UNTESTED | Volatility of recent stock returns. |
| 290 | `accounting_forensics_factor_4` | VECTOR | 0.860 | 其他 | 0 | — | — | — | UNTESTED | Analysis of accounts for signs of trouble and strength. |
| 291 | `accounting_forensics_factor_41` | VECTOR | 0.860 | 其他 | 0 | — | — | — | UNTESTED | Subtle analysis of accounts for signs of trouble and strength. |
| 292 | `accounting_forensics_factor_5` | VECTOR | 0.860 | 其他 | 0 | — | — | — | UNTESTED | Subtle analysis of accounts for signs of trouble and strength. |
| 293 | `accounting_forensics_factor_51` | VECTOR | 0.860 | 其他 | 0 | — | — | — | UNTESTED | Analysis of accounts for signs of trouble and strength. |
| 294 | `accruals_contribution_score_2` | VECTOR | 0.860 | 盈利与财务 | 0 | — | — | — | UNTESTED | Score measuring the contribution of accruals to financial analysis. |
| 295 | `accruals_contribution_score_3` | VECTOR | 0.860 | 盈利与财务 | 0 | — | — | — | UNTESTED | Score quantifying the impact of accruals in financial analysis. |
| 296 | `accruals_contribution_score_4` | VECTOR | 0.860 | 盈利与财务 | 0 | — | — | — | UNTESTED | Score quantifying the contribution of accruals in financial analysis. |
| 297 | `accruals_contribution_score_5` | VECTOR | 0.860 | 盈利与财务 | 0 | — | — | — | UNTESTED | Accounting measure indicating the contribution of accruals. |
| 298 | `accruals_contribution_score_51` | VECTOR | 0.860 | 盈利与财务 | 0 | — | — | — | UNTESTED | Accounting measure indicating the contribution of accruals to financial analysis. |
| 299 | `analyst_earnings_revision_score_3` | VECTOR | 0.860 | 修正与预期 | 0 | — | — | — | UNTESTED | Score capturing changes in analyst earnings forecasts or recommendations. |
| 300 | `analyst_earnings_revision_score_4` | VECTOR | 0.860 | 修正与预期 | 0 | — | — | — | UNTESTED | Score capturing changes in analyst earnings forecasts. |
| 301 | `analyst_forecast_change_metric_2` | VECTOR | 0.860 | 修正与预期 | 0 | — | — | — | UNTESTED | Measure of changes in analyst forecasts or recommendations. |
| 302 | `analyst_forecast_change_metric_21` | VECTOR | 0.860 | 修正与预期 | 0 | — | — | — | UNTESTED | Models capturing changes in analyst forecasts or recommendations. |
| 303 | `analyst_forecast_change_score` | VECTOR | 0.860 | 修正与预期 | 0 | — | — | — | UNTESTED | Score reflecting the magnitude of recent changes in analyst forecasts or recommendations. |
| 304 | `analyst_forecast_revision_factor_3` | VECTOR | 0.860 | 修正与预期 | 0 | — | — | — | UNTESTED | Models capturing changes in analyst forecasts or recommendations. |
| 305 | `analyst_forecast_revision_factor_4` | VECTOR | 0.860 | 修正与预期 | 0 | — | — | — | UNTESTED | Models capturing changes in analyst forecasts or recommendations. |
| 306 | `analyst_opinion_metric_4` | VECTOR | 0.860 | 修正与预期 | 0 | — | — | — | UNTESTED | Metric summarizing analyst opinions or recommendations. |
| 307 | `analyst_opinion_metric_5` | VECTOR | 0.860 | 修正与预期 | 0 | — | — | — | UNTESTED | Metric summarizing analyst recommendations or outlook. |
| 308 | `analyst_opinion_metric_6` | VECTOR | 0.860 | 修正与预期 | 0 | — | — | — | UNTESTED | Metric summarizing analyst recommendations or outlook. |
| 309 | `analyst_opinion_metric_7` | VECTOR | 0.860 | 修正与预期 | 0 | — | — | — | UNTESTED | Factor reflecting analyst opinions or perspectives. |
| 310 | `analyst_opinion_metric_8` | VECTOR | 0.860 | 修正与预期 | 0 | — | — | — | UNTESTED | Factor reflecting analyst opinions or perspectives. |
| 311 | `analyst_sentiment_score_10` | VECTOR | 0.860 | 修正与预期 | 0 | — | — | — | UNTESTED | Score reflecting analyst sentiment for a security. |
| 312 | `analyst_sentiment_score_7` | VECTOR | 0.860 | 修正与预期 | 0 | — | — | — | UNTESTED | Score reflecting analyst opinions or perspectives on a security. |
| 313 | `analyst_sentiment_score_8` | VECTOR | 0.860 | 修正与预期 | 0 | — | — | — | UNTESTED | Score summarizing analyst sentiment towards a security. |
| 314 | `analyst_sentiment_score_9` | VECTOR | 0.860 | 修正与预期 | 0 | — | — | — | UNTESTED | Score reflecting the sentiment of analysts regarding a security. |
| 315 | `analyst_view_score_2` | VECTOR | 0.860 | 修正与预期 | 0 | — | — | — | UNTESTED | Factor reflecting analyst opinions or perspectives. |
| 316 | `asset_impairment_probability_3` | VECTOR | 0.860 | 盈利与财务 | 0 | — | — | — | UNTESTED | Probability score estimating the risk of asset value reduction due to impairment. |
| 317 | `asset_impairment_risk_score_4` | VECTOR | 0.860 | 盈利与财务 | 0 | — | — | — | UNTESTED | Probability of asset value reduction due to impairment events. |
| 318 | `asset_impairment_risk_score_41` | VECTOR | 0.860 | 盈利与财务 | 0 | — | — | — | UNTESTED | Probability of asset value reduction due to impairment events. |
| 319 | `asset_impairment_risk_score_5` | VECTOR | 0.860 | 盈利与财务 | 0 | — | — | — | UNTESTED | Probability that a company's assets will be written down due to impairment. |
| 320 | `balance_sheet_trend_metric_3` | VECTOR | 0.860 | 其他 | 0 | — | — | — | UNTESTED | Model analyzing trends and changes in balance sheet items. |
| 321 | `balance_sheet_trend_metric_31` | VECTOR | 0.860 | 其他 | 0 | — | — | — | UNTESTED | Model analyzing trends and changes in balance sheet items. |
| 322 | `balance_sheet_trend_metric_4` | VECTOR | 0.860 | 其他 | 0 | — | — | — | UNTESTED | Model analyzing trends and changes in balance sheet items. |
| 323 | `balance_sheet_trend_metric_41` | VECTOR | 0.860 | 其他 | 0 | — | — | — | UNTESTED | Model analyzing trends and changes in balance sheet items. |
| 324 | `balance_sheet_trend_metric_5` | VECTOR | 0.860 | 其他 | 0 | — | — | — | UNTESTED | Model analyzing trends and changes in balance sheet items. |
| 325 | `business_model_clarity_score_4` | VECTOR | 0.860 | 风险与质量 | 0 | — | — | — | UNTESTED | Certainty or uncertainty surrounding a company's business model. |
| 326 | `business_model_clarity_score_41` | VECTOR | 0.860 | 风险与质量 | 0 | — | — | — | UNTESTED | Certainty or uncertainty surrounding a company's business model. |
| 327 | `business_model_clarity_score_5` | VECTOR | 0.860 | 风险与质量 | 0 | — | — | — | UNTESTED | Certainty or uncertainty surrounding a company's business model. |
| 328 | `buzz_intensity_score_3` | VECTOR | 0.860 | 情绪与新闻 | 0 | — | — | — | UNTESTED | Score measuring the level of market or media attention to a security. |
| 329 | `buzz_intensity_score_4` | VECTOR | 0.860 | 情绪与新闻 | 0 | — | — | — | UNTESTED | Score indicating the level of attention a security receives in the market. |
| 330 | `buzz_intensity_score_5` | VECTOR | 0.860 | 情绪与新闻 | 0 | — | — | — | UNTESTED | Score indicating the intensity of market or media attention. |
| 331 | `buzz_intensity_score_6` | VECTOR | 0.860 | 情绪与新闻 | 0 | — | — | — | UNTESTED | Measure of market or media attention to a security. |
| 332 | `buzz_intensity_score_61` | VECTOR | 0.860 | 情绪与新闻 | 0 | — | — | — | UNTESTED | Measure of market or media attention to a security. |
| 333 | `buzz_intensity_score_7` | VECTOR | 0.860 | 情绪与新闻 | 0 | — | — | — | UNTESTED | Measure of market or media attention to a security. |
| 334 | `buzz_trend_metric_2` | VECTOR | 0.860 | 情绪与新闻 | 0 | — | — | — | UNTESTED | Metric indicating changes in market or media attention over time. |
| 335 | `buzz_trend_metric_3` | VECTOR | 0.860 | 情绪与新闻 | 0 | — | — | — | UNTESTED | Measure of changes in market or media attention over time. |
| 336 | `buzz_trend_metric_31` | VECTOR | 0.860 | 情绪与新闻 | 0 | — | — | — | UNTESTED | Measure of changes in market or media attention over time. |
| 337 | `buzz_trend_metric_4` | VECTOR | 0.860 | 情绪与新闻 | 0 | — | — | — | UNTESTED | Measure of changes in market or media attention over time. |
| 338 | `cashflow_trend_analysis_10` | VECTOR | 0.860 | 盈利与财务 | 0 | — | — | — | UNTESTED | Model analyzing trends and changes in cash flow statements. |
| 339 | `cashflow_trend_analysis_101` | VECTOR | 0.860 | 盈利与财务 | 0 | — | — | — | UNTESTED | Model analyzing trends and changes in cash flow statements. |
| 340 | `cashflow_trend_analysis_11` | VECTOR | 0.860 | 盈利与财务 | 0 | — | — | — | UNTESTED | Model analyzing trends and changes in cash flow statements. |
| 341 | `cashflow_trend_analysis_111` | VECTOR | 0.860 | 盈利与财务 | 0 | — | — | — | UNTESTED | Model analyzing trends and changes in cash flow statements. |
| 342 | `cashflow_trend_analysis_12` | VECTOR | 0.860 | 盈利与财务 | 0 | — | — | — | UNTESTED | Model analyzing trends and changes in cash flow statements. |
| 343 | `cashflow_trend_analysis_3` | VECTOR | 0.860 | 盈利与财务 | 0 | — | — | — | UNTESTED | Analysis of trends and changes in cash flow statements over time. |
| 344 | `cashflow_trend_analysis_4` | VECTOR | 0.860 | 盈利与财务 | 0 | — | — | — | UNTESTED | Analysis of cash flow statement trends and their implications. |
| 345 | `cashflow_trend_analysis_5` | VECTOR | 0.860 | 盈利与财务 | 0 | — | — | — | UNTESTED | Analysis of changes and trends in cash flow statements. |
| 346 | `cashflow_trend_analysis_6` | VECTOR | 0.860 | 盈利与财务 | 0 | — | — | — | UNTESTED | Analysis of cash flow statement trends and variations. |
| 347 | `cashflow_trend_analysis_7` | VECTOR | 0.860 | 盈利与财务 | 0 | — | — | — | UNTESTED | Analysis of trends in cash flow statements over time. |
| 348 | `cashflow_trend_analysis_8` | VECTOR | 0.860 | 盈利与财务 | 0 | — | — | — | UNTESTED | Analysis of cash flow statement trends and their significance. |
| 349 | `cashflow_trend_analysis_9` | VECTOR | 0.860 | 盈利与财务 | 0 | — | — | — | UNTESTED | Analysis of cash flow statement trends and their impact. |
| 350 | `cashflow_variation_score_2` | VECTOR | 0.860 | 盈利与财务 | 0 | — | — | — | UNTESTED | Score indicating the variability in a company's cash flows. |
| 351 | `cashflow_variation_score_3` | VECTOR | 0.860 | 盈利与财务 | 0 | — | — | — | UNTESTED | Degree of fluctuation in a company's cash flow over time. |
| 352 | `combined_technical_indicators_4` | VECTOR | 0.860 | 价量与波动 | 0 | — | — | — | UNTESTED | Aggregated technical indicators for momentum and reversion. |
| 353 | `combined_technical_indicators_41` | VECTOR | 0.860 | 价量与波动 | 0 | — | — | — | UNTESTED | Aggregated technical indicators for momentum and reversion. |
| 354 | `combined_technical_indicators_5` | VECTOR | 0.860 | 价量与波动 | 0 | — | — | — | UNTESTED | Aggregated technical indicators for momentum and reversion. |
| 355 | `company_physics_model_3` | VECTOR | 0.860 | 价量与波动 | 0 | — | — | — | UNTESTED | Mathematical models of shareholder returns compounding financial and technical properties. |
| 356 | `company_physics_model_31` | VECTOR | 0.860 | 价量与波动 | 0 | — | — | — | UNTESTED | Mathematical model of shareholder returns compounding. |
| 357 | `company_physics_model_4` | VECTOR | 0.860 | 价量与波动 | 0 | — | — | — | UNTESTED | Mathematical model of shareholder returns compounding. |
| 358 | `company_physics_model_41` | VECTOR | 0.860 | 价量与波动 | 0 | — | — | — | UNTESTED | Mathematical models of shareholder returns compounding financial and technical properties. |
| 359 | `company_size_factor_6` | VECTOR | 0.860 | 其他 | 0 | — | — | — | UNTESTED | Factor representing the scale or market capitalization of a company. |
| 360 | `company_size_factor_7` | VECTOR | 0.860 | 其他 | 0 | — | — | — | UNTESTED | Factor representing the scale or market capitalization of a company. |
| 361 | `competitive_advantage_indicator_2` | VECTOR | 0.860 | 盈利与财务 | 0 | — | — | — | UNTESTED | Indicator of a company's ability to maintain profits over competitors. |
| 362 | `correlation_risk_factor_6` | VECTOR | 0.860 | 盈利与财务 | 0 | — | — | — | UNTESTED | Assessment of risk from correlated movements in assets. |
| 363 | `correlation_risk_factor_61` | VECTOR | 0.860 | 盈利与财务 | 0 | — | — | — | UNTESTED | Model assessing the risk from correlated movements in assets. |
| 364 | `correlation_risk_factor_7` | VECTOR | 0.860 | 盈利与财务 | 0 | — | — | — | UNTESTED | Assessment of risk from correlated movements in assets. |
| 365 | `correlation_risk_factor_71` | VECTOR | 0.860 | 盈利与财务 | 0 | — | — | — | UNTESTED | Model assessing the risk from correlated movements in assets. |
| 366 | `correlation_risk_factor_8` | VECTOR | 0.860 | 盈利与财务 | 0 | — | — | — | UNTESTED | Model assessing the risk from correlated movements in assets. |
| 367 | `credit_default_risk_assessment_3` | VECTOR | 0.860 | 风险与质量 | 0 | — | — | — | UNTESTED | Assessment of the likelihood that a company will default on its obligations. |
| 368 | `credit_default_risk_assessment_4` | VECTOR | 0.860 | 风险与质量 | 0 | — | — | — | UNTESTED | Assessment of the probability of a company defaulting on obligations. |
| 369 | `credit_default_risk_assessment_5` | VECTOR | 0.860 | 风险与质量 | 0 | — | — | — | UNTESTED | Model assessing the risk of default or creditworthiness of a company. |
| 370 | `credit_default_risk_assessment_51` | VECTOR | 0.860 | 风险与质量 | 0 | — | — | — | UNTESTED | Assessment of the risk of default or creditworthiness. |
| 371 | `credit_default_risk_assessment_6` | VECTOR | 0.860 | 风险与质量 | 0 | — | — | — | UNTESTED | Model assessing the risk of default or creditworthiness of a company. |
| 372 | `credit_risk_model_score_2` | VECTOR | 0.860 | 风险与质量 | 0 | — | — | — | UNTESTED | Score from models assessing the risk of default or creditworthiness. |
| 373 | `credit_risk_model_score_3` | VECTOR | 0.860 | 风险与质量 | 0 | — | — | — | UNTESTED | Score from models assessing the risk of default or creditworthiness. |
| 374 | `creditworthiness_assessment_factor_3` | VECTOR | 0.860 | 风险与质量 | 0 | — | — | — | UNTESTED | Factor assessing the risk of default or creditworthiness of a company. |
| 375 | `creditworthiness_assessment_factor_4` | VECTOR | 0.860 | 风险与质量 | 0 | — | — | — | UNTESTED | Factor assessing a company's credit risk and default probability. |
| 376 | `creditworthiness_assessment_factor_5` | VECTOR | 0.860 | 风险与质量 | 0 | — | — | — | UNTESTED | Factor assessing the credit risk and default probability of a company. |
| 377 | `creditworthiness_assessment_factor_6` | VECTOR | 0.860 | 风险与质量 | 0 | — | — | — | UNTESTED | Factor assessing a company's credit risk and default probability. |
| 378 | `creditworthiness_assessment_factor_7` | VECTOR | 0.860 | 风险与质量 | 0 | — | — | — | UNTESTED | Model assessing the risk of default or creditworthiness of a company. |
| 379 | `debt_coverage_ratio_metric_10` | VECTOR | 0.860 | 盈利与财务 | 0 | — | — | — | UNTESTED | Ratio measuring a company's ability to cover its debt obligations. |
| 380 | `debt_maturity_profile_score_11` | VECTOR | 0.860 | 盈利与财务 | 0 | — | — | — | UNTESTED | Assessment of the timing and structure of a company's debt maturities. |
| 381 | `debt_to_assets_ratio_metric_12` | VECTOR | 0.860 | 盈利与财务 | 0 | — | — | — | UNTESTED | Ratio of total debt to total assets for solvency risk assessment. |
| 382 | `debt_to_assets_ratio_metric_3` | VECTOR | 0.860 | 盈利与财务 | 0 | — | — | — | UNTESTED | Ratio comparing a company's total debt to its total assets. |
| 383 | `debt_to_capital_ratio_metric_11` | VECTOR | 0.860 | 盈利与财务 | 0 | — | — | — | UNTESTED | Proportion of debt in a company's capital structure for financial analysis. |
| 384 | `debt_to_enterprise_value_ratio_metric_11` | VECTOR | 0.860 | 盈利与财务 | 0 | — | — | — | UNTESTED | Ratio of total debt to enterprise value for capital structure evaluation. |
| 385 | `debt_to_equity_ratio_metric_14` | VECTOR | 0.860 | 盈利与财务 | 0 | — | — | — | UNTESTED | Ratio measuring a company's financial leverage by comparing total debt to equity. |
| 386 | `debt_to_equity_ratio_metric_15` | VECTOR | 0.860 | 盈利与财务 | 0 | — | — | — | UNTESTED | Ratio measuring a company's financial leverage using debt and equity values. |
| 387 | `debt_to_equity_ratio_metric_151` | VECTOR | 0.860 | 盈利与财务 | 0 | — | — | — | UNTESTED | Financial leverage ratio comparing total debt to equity. |
| 388 | `debt_to_equity_ratio_metric_16` | VECTOR | 0.860 | 盈利与财务 | 0 | — | — | — | UNTESTED | Ratio comparing a company's total debt to its equity base. |
| 389 | `debt_to_equity_ratio_metric_17` | VECTOR | 0.860 | 盈利与财务 | 0 | — | — | — | UNTESTED | Financial leverage ratio of total debt to equity. |
| 390 | `debt_to_equity_ratio_metric_18` | VECTOR | 0.860 | 盈利与财务 | 0 | — | — | — | UNTESTED | Ratio of total debt to equity, indicating financial leverage. |
| 391 | `debt_to_equity_ratio_metric_19` | VECTOR | 0.860 | 盈利与财务 | 0 | — | — | — | UNTESTED | Ratio of total debt to equity for financial leverage assessment. |
| 392 | `debt_to_equity_ratio_metric_20` | VECTOR | 0.860 | 盈利与财务 | 0 | — | — | — | UNTESTED | Financial leverage ratio of total debt to equity. |
| 393 | `debt_to_equity_ratio_metric_21` | VECTOR | 0.860 | 盈利与财务 | 0 | — | — | — | UNTESTED | Ratio of total debt to equity for leverage analysis. |
| 394 | `debt_to_equity_ratio_metric_22` | VECTOR | 0.860 | 盈利与财务 | 0 | — | — | — | UNTESTED | Ratio of total debt to equity for leverage evaluation. |
| 395 | `debt_to_equity_ratio_metric_23` | VECTOR | 0.860 | 盈利与财务 | 0 | — | — | — | UNTESTED | Ratio of total debt to equity for leverage measurement. |
| 396 | `debt_to_equity_ratio_metric_24` | VECTOR | 0.860 | 盈利与财务 | 0 | — | — | — | UNTESTED | Ratio of total debt to equity for financial leverage analysis. |
| 397 | `debt_to_equity_ratio_metric_25` | VECTOR | 0.860 | 盈利与财务 | 0 | — | — | — | UNTESTED | Ratio of total debt to equity for leverage assessment. |
| 398 | `debt_to_equity_ratio_metric_26` | VECTOR | 0.860 | 盈利与财务 | 0 | — | — | — | UNTESTED | Ratio of total debt to equity for leverage calculation. |
| 399 | `debt_to_equity_ratio_metric_27` | VECTOR | 0.860 | 盈利与财务 | 0 | — | — | — | UNTESTED | Ratio of total debt to equity for leverage purposes. |
| 400 | `debt_to_equity_ratio_metric_28` | VECTOR | 0.860 | 盈利与财务 | 0 | — | — | — | UNTESTED | Ratio of total debt to equity for financial leverage. |
| 401 | `debt_to_equity_ratio_metric_29` | VECTOR | 0.860 | 盈利与财务 | 0 | — | — | — | UNTESTED | Ratio of total debt to equity for leverage analysis. |
| 402 | `debt_to_equity_ratio_metric_30` | VECTOR | 0.860 | 盈利与财务 | 0 | — | — | — | UNTESTED | Ratio of total debt to equity for leverage measurement. |
| 403 | `debt_to_equity_ratio_metric_31` | VECTOR | 0.860 | 盈利与财务 | 0 | — | — | — | UNTESTED | Ratio of total debt to equity for leverage analysis. |
| 404 | `debt_to_equity_ratio_metric_32` | VECTOR | 0.860 | 盈利与财务 | 0 | — | — | — | UNTESTED | Ratio of total debt to equity for leverage calculation. |
| 405 | `debt_to_market_cap_ratio_metric_11` | VECTOR | 0.860 | 盈利与财务 | 0 | — | — | — | UNTESTED | Ratio of total debt to market capitalization for financial risk analysis. |
| 406 | `debt_to_market_cap_ratio_metric_2` | VECTOR | 0.860 | 盈利与财务 | 0 | — | — | — | UNTESTED | Ratio of a company's total debt to its market capitalization. |
| 407 | `dividend_analysis_score_2` | VECTOR | 0.860 | 盈利与财务 | 0 | — | — | — | UNTESTED | Analysis of dividend payments and policies. |
| 408 | `dividend_policy_analysis_6` | VECTOR | 0.860 | 盈利与财务 | 0 | — | — | — | UNTESTED | Analysis of a company's dividend payment policies and their sustainability. |
| 409 | `dividend_policy_analysis_7` | VECTOR | 0.860 | 盈利与财务 | 0 | — | — | — | UNTESTED | Analysis of dividend payments and policies. |
| 410 | `dividend_policy_analysis_8` | VECTOR | 0.860 | 盈利与财务 | 0 | — | — | — | UNTESTED | Analysis of dividend payments and policies. |
| 411 | `earnings_growth_analysis_2` | VECTOR | 0.860 | 盈利与财务 | 0 | — | — | — | UNTESTED | Analysis of earnings growth rates and sustainability. |
| 412 | `earnings_growth_rate_analysis_4` | VECTOR | 0.860 | 盈利与财务 | 0 | — | — | — | UNTESTED | Analysis of earnings growth rates and sustainability. |
| 413 | `earnings_growth_rate_analysis_5` | VECTOR | 0.860 | 盈利与财务 | 0 | — | — | — | UNTESTED | Analysis of earnings growth rates and sustainability. |
| 414 | `earnings_quality_score_3` | VECTOR | 0.860 | 盈利与财务 | 0 | — | — | — | UNTESTED | Score assessing the reliability and sustainability of reported earnings. |
| 415 | `earnings_quality_score_4` | VECTOR | 0.860 | 盈利与财务 | 0 | — | — | — | UNTESTED | Score evaluating the quality and sustainability of earnings. |
| 416 | `earnings_quality_score_5` | VECTOR | 0.860 | 盈利与财务 | 0 | — | — | — | UNTESTED | Score assessing the quality and sustainability of earnings. |
| 417 | `earnings_quality_score_6` | VECTOR | 0.860 | 盈利与财务 | 0 | — | — | — | UNTESTED | Assessment of the reliability and sustainability of reported earnings. |
| 418 | `earnings_quality_score_61` | VECTOR | 0.860 | 盈利与财务 | 0 | — | — | — | UNTESTED | Assessment of the reliability and sustainability of reported earnings. |
| 419 | `efficiency_model_score_2` | VECTOR | 0.860 | 风险与质量 | 0 | — | — | — | UNTESTED | Score reflecting operational efficiency of a company. |
| 420 | `efficiency_model_score_3` | VECTOR | 0.860 | 风险与质量 | 0 | — | — | — | UNTESTED | Score reflecting operational efficiency of a company. |
| 421 | `efficiency_model_score_4` | VECTOR | 0.860 | 风险与质量 | 0 | — | — | — | UNTESTED | Score reflecting operational efficiency of a company. |
| 422 | `efficiency_model_score_5` | VECTOR | 0.860 | 风险与质量 | 0 | — | — | — | UNTESTED | Score reflecting operational efficiency of a company. |
| 423 | `efficiency_model_score_6` | VECTOR | 0.860 | 风险与质量 | 0 | — | — | — | UNTESTED | Score reflecting operational efficiency of a company. |
| 424 | `financial_change_trend_analysis_2` | VECTOR | 0.860 | 其他 | 0 | — | — | — | UNTESTED | Analysis of trends across all financial statements. |
| 425 | `financial_change_trend_analysis_21` | VECTOR | 0.860 | 其他 | 0 | — | — | — | UNTESTED | Analysis of trends across all financial statements. |
| 426 | `financial_change_trend_analysis_3` | VECTOR | 0.860 | 其他 | 0 | — | — | — | UNTESTED | Analysis of trends across all financial statements. |
| 427 | `financial_change_trend_analysis_31` | VECTOR | 0.860 | 其他 | 0 | — | — | — | UNTESTED | Analysis of trends across all financial statements. |
| 428 | `financial_yield_analysis_4` | VECTOR | 0.860 | 盈利与财务 | 0 | — | — | — | UNTESTED | Analysis of financial yields such as dividend or earnings yield. |
| 429 | `financial_yield_analysis_41` | VECTOR | 0.860 | 盈利与财务 | 0 | — | — | — | UNTESTED | Analysis of financial yields such as dividend or earnings yield. |
| 430 | `financial_yield_analysis_5` | VECTOR | 0.860 | 盈利与财务 | 0 | — | — | — | UNTESTED | Analysis of financial yields such as dividend or earnings yield. |
| 431 | `financing_analysis_score_2` | VECTOR | 0.860 | 风险与质量 | 0 | — | — | — | UNTESTED | Analysis of a company's financing activities and structure. |
| 432 | `financing_structure_analysis_6` | VECTOR | 0.860 | 其他 | 0 | — | — | — | UNTESTED | Assessment of a company's financing activities and capital structure. |
| 433 | `financing_structure_analysis_7` | VECTOR | 0.860 | 其他 | 0 | — | — | — | UNTESTED | Analysis of a company's financing activities and structure. |
| 434 | `financing_structure_analysis_8` | VECTOR | 0.860 | 其他 | 0 | — | — | — | UNTESTED | Analysis of a company's financing activities and structure. |
| 435 | `forecast_sentiment_nlp_alpha_factor_2` | VECTOR | 0.860 | 情绪与新闻 | 0 | — | — | — | UNTESTED | Analysis of perception of stock and its performance using NLP. |
| 436 | `forecast_value_accuracy_metric_4` | VECTOR | 0.860 | 其他 | 0 | — | — | — | UNTESTED | Metric evaluating the value and accuracy of forecasts. |
| 437 | `forecast_value_accuracy_metric_5` | VECTOR | 0.860 | 其他 | 0 | — | — | — | UNTESTED | Metric evaluating the value and accuracy of forecasts. |
| 438 | `forecast_yield_metric_4` | VECTOR | 0.860 | 宏观与行业 | 0 | — | — | — | UNTESTED | Metric evaluating the expected future yield of a security. |
| 439 | `forecast_yield_metric_5` | VECTOR | 0.860 | 宏观与行业 | 0 | — | — | — | UNTESTED | Metric assessing the expected yield based on forecasts. |
| 440 | `forecast_yield_metric_6` | VECTOR | 0.860 | 宏观与行业 | 0 | — | — | — | UNTESTED | Metric evaluating the expected yield from forecasts. |
| 441 | `forecast_yield_metric_7` | VECTOR | 0.860 | 宏观与行业 | 0 | — | — | — | UNTESTED | Metric assessing the expected yield based on forecast models. |
| 442 | `forecast_yield_metric_8` | VECTOR | 0.860 | 宏观与行业 | 0 | — | — | — | UNTESTED | Analysis of expected future yields. |
| 443 | `forecast_yield_metric_81` | VECTOR | 0.860 | 宏观与行业 | 0 | — | — | — | UNTESTED | Analysis of expected future yields. |
| 444 | `forecast_yield_metric_9` | VECTOR | 0.860 | 宏观与行业 | 0 | — | — | — | UNTESTED | Analysis of expected future yields. |
| 445 | `forecasted_alpha_ranking` | VECTOR | 0.860 | 价量与波动 | 0 | — | — | — | UNTESTED | Ranking of securities based on their predicted excess returns. |
| 446 | `fund_flow_prediction_metric_6` | VECTOR | 0.860 | 持仓与资金流 | 0 | — | — | — | UNTESTED | Model predicting the movement of funds into or out of securities. |
| 447 | `fund_flow_prediction_metric_61` | VECTOR | 0.860 | 持仓与资金流 | 0 | — | — | — | UNTESTED | Prediction of fund movements into or out of securities. |
| 448 | `fund_flow_prediction_metric_7` | VECTOR | 0.860 | 持仓与资金流 | 0 | — | — | — | UNTESTED | Prediction of fund movements into or out of securities. |
| 449 | `fund_flow_prediction_metric_71` | VECTOR | 0.860 | 持仓与资金流 | 0 | — | — | — | UNTESTED | Model predicting the movement of funds into or out of securities. |
| 450 | `fund_flow_prediction_metric_8` | VECTOR | 0.860 | 持仓与资金流 | 0 | — | — | — | UNTESTED | Model predicting the movement of funds into or out of securities. |
| 451 | `historic_earnings_surprise_score_4` | VECTOR | 0.860 | 盈利与财务 | 0 | — | — | — | UNTESTED | Measure of past earnings results versus expectations. |
| 452 | `income_statement_trend_metric_2` | VECTOR | 0.860 | 其他 | 0 | — | — | — | UNTESTED | Model analyzing trends and changes in income statement items. |
| 453 | `income_statement_trend_metric_21` | VECTOR | 0.860 | 其他 | 0 | — | — | — | UNTESTED | Model analyzing trends and changes in income statement items. |
| 454 | `income_statement_trend_metric_3` | VECTOR | 0.860 | 其他 | 0 | — | — | — | UNTESTED | Model analyzing trends and changes in income statement items. |
| 455 | `income_statement_trend_metric_31` | VECTOR | 0.860 | 其他 | 0 | — | — | — | UNTESTED | Model analyzing trends and changes in income statement items. |
| 456 | `income_statement_trend_metric_4` | VECTOR | 0.860 | 其他 | 0 | — | — | — | UNTESTED | Model analyzing trends and changes in income statement items. |
| 457 | `information_opacity_score_6` | VECTOR | 0.860 | 风险与质量 | 0 | — | — | — | UNTESTED | Measure of the lack of transparency or clarity in information. |
| 458 | `information_opacity_score_61` | VECTOR | 0.860 | 风险与质量 | 0 | — | — | — | UNTESTED | Measure of the lack of transparency or clarity in information. |
| 459 | `information_opacity_score_7` | VECTOR | 0.860 | 风险与质量 | 0 | — | — | — | UNTESTED | Measure of the lack of transparency or clarity in information. |
| 460 | `intrinsic_valuation_estimate_4` | VECTOR | 0.860 | 修正与预期 | 0 | — | — | — | UNTESTED | Estimate of a company's fundamental value based on intrinsic valuation models. |
| 461 | `intrinsic_valuation_estimate_5` | VECTOR | 0.860 | 修正与预期 | 0 | — | — | — | UNTESTED | Estimate of a company's value using intrinsic valuation models. |
| 462 | `intrinsic_valuation_estimate_6` | VECTOR | 0.860 | 修正与预期 | 0 | — | — | — | UNTESTED | Estimate of fundamental company value using intrinsic models. |
| 463 | `intrinsic_valuation_estimate_7` | VECTOR | 0.860 | 修正与预期 | 0 | — | — | — | UNTESTED | Estimate of company value using intrinsic valuation techniques. |
| 464 | `intrinsic_valuation_estimate_8` | VECTOR | 0.860 | 修正与预期 | 0 | — | — | — | UNTESTED | Estimate of the fundamental value of a company. |
| 465 | `intrinsic_valuation_estimate_81` | VECTOR | 0.860 | 修正与预期 | 0 | — | — | — | UNTESTED | Model estimating the fundamental value of a company. |
| 466 | `intrinsic_valuation_estimate_9` | VECTOR | 0.860 | 修正与预期 | 0 | — | — | — | UNTESTED | Model estimating the fundamental value of a company. |
| 467 | `long_term_indicators_score_2` | VECTOR | 0.860 | 风险与质量 | 0 | — | — | — | UNTESTED | Technical indicators measuring long-term trends. |
| 468 | `long_term_physics_model_3` | VECTOR | 0.860 | 价量与波动 | 0 | — | — | — | UNTESTED | Factor modeling shareholder returns over a long period using mathematical models. |
| 469 | `long_term_physics_model_31` | VECTOR | 0.860 | 价量与波动 | 0 | — | — | — | UNTESTED | Factor modeling shareholder returns over a long period. |
| 470 | `long_term_physics_model_4` | VECTOR | 0.860 | 价量与波动 | 0 | — | — | — | UNTESTED | Factor modeling shareholder returns over a long period using mathematical models. |
| 471 | `long_term_physics_model_41` | VECTOR | 0.860 | 价量与波动 | 0 | — | — | — | UNTESTED | Factor modeling shareholder returns over a long period. |
| 472 | `long_term_technical_trend_indicator_5` | VECTOR | 0.860 | 价量与波动 | 0 | — | — | — | UNTESTED | Technical indicator measuring long-term price trends. |
| 473 | `long_term_technical_trend_indicator_51` | VECTOR | 0.860 | 其他 | 0 | — | — | — | UNTESTED | Technical indicators measuring long-term trends. |
| 474 | `long_term_technical_trend_indicator_6` | VECTOR | 0.860 | 其他 | 0 | — | — | — | UNTESTED | Technical indicators measuring long-term trends. |
| 475 | `long_term_technical_valuation_model_4` | VECTOR | 0.860 | 价量与波动 | 0 | — | — | — | UNTESTED | Technical valuation model focused on long-term price trends. |
| 476 | `long_term_technical_valuation_model_41` | VECTOR | 0.860 | 价量与波动 | 0 | — | — | — | UNTESTED | Technical valuation models focused on long-term price trends. |
| 477 | `long_term_technical_valuation_model_5` | VECTOR | 0.860 | 价量与波动 | 0 | — | — | — | UNTESTED | Technical valuation models focused on long-term price trends. |
| 478 | `long_term_uncertainty_score_2` | VECTOR | 0.860 | 风险与质量 | 0 | — | — | — | UNTESTED | Measure of uncertainty in a company's business model over a long horizon. |
| 479 | `media_attention_trend_score` | VECTOR | 0.860 | 情绪与新闻 | 0 | — | — | — | UNTESTED | Metric indicating the trend in market or media attention over time. |
| 480 | `medium_term_business_uncertainty_3` | VECTOR | 0.860 | 其他 | 0 | — | — | — | UNTESTED | Measure of uncertainty in a company's business model over a medium horizon. |
| 481 | `medium_term_indicators_score_2` | VECTOR | 0.860 | 风险与质量 | 0 | — | — | — | UNTESTED | Technical indicators measuring medium-term trends. |
| 482 | `medium_term_physics_model_3` | VECTOR | 0.860 | 价量与波动 | 0 | — | — | — | UNTESTED | Factor modeling shareholder returns over a medium period. |
| 483 | `medium_term_physics_model_31` | VECTOR | 0.860 | 价量与波动 | 0 | — | — | — | UNTESTED | Factor modeling shareholder returns over a medium period. |
| 484 | `medium_term_physics_model_4` | VECTOR | 0.860 | 价量与波动 | 0 | — | — | — | UNTESTED | Factor modeling shareholder returns over a medium period. |
| 485 | `medium_term_physics_model_41` | VECTOR | 0.860 | 价量与波动 | 0 | — | — | — | UNTESTED | Factor modeling shareholder returns over a medium period. |
| 486 | `medium_term_technical_trend_indicator_5` | VECTOR | 0.860 | 价量与波动 | 0 | — | — | — | UNTESTED | Technical indicator measuring medium-term price trends. |
| 487 | `medium_term_technical_trend_indicator_51` | VECTOR | 0.860 | 其他 | 0 | — | — | — | UNTESTED | Technical indicators measuring medium-term trends. |
| 488 | `medium_term_technical_trend_indicator_6` | VECTOR | 0.860 | 其他 | 0 | — | — | — | UNTESTED | Technical indicators measuring medium-term trends. |
| 489 | `medium_term_technical_valuation_model_4` | VECTOR | 0.860 | 价量与波动 | 0 | — | — | — | UNTESTED | Technical valuation model focused on medium-term price trends. |
| 490 | `medium_term_technical_valuation_model_41` | VECTOR | 0.860 | 价量与波动 | 0 | — | — | — | UNTESTED | Technical valuation models focused on medium-term price trends. |
| 491 | `medium_term_technical_valuation_model_5` | VECTOR | 0.860 | 价量与波动 | 0 | — | — | — | UNTESTED | Technical valuation models focused on medium-term price trends. |
| 492 | `medium_term_uncertainty_score_2` | VECTOR | 0.860 | 风险与质量 | 0 | — | — | — | UNTESTED | Measure of uncertainty in a company's business model over a medium horizon. |
| 493 | `moat_strength_score_2` | VECTOR | 0.860 | 盈利与财务 | 0 | — | — | — | UNTESTED | Indicator of a company's competitive advantage and ability to maintain profits. |
| 494 | `moat_strength_score_3` | VECTOR | 0.860 | 盈利与财务 | 0 | — | — | — | UNTESTED | Indicator of a company's competitive advantage and ability to maintain profits. |
| 495 | `moat_strength_score_4` | VECTOR | 0.860 | 盈利与财务 | 0 | — | — | — | UNTESTED | Indicator of a company's competitive advantage and ability to maintain profits. |
| 496 | `nlp_sentiment_alpha_factor_4` | VECTOR | 0.860 | 情绪与新闻 | 0 | — | — | — | UNTESTED | Analysis of perception of stock and its performance using natural language processing. |
| 497 | `nlp_sentiment_alpha_factor_5` | VECTOR | 0.860 | 情绪与新闻 | 0 | — | — | — | UNTESTED | Analysis of perception of stock and its performance using natural language processing. |
| 498 | `operating_income_score_3` | VECTOR | 0.860 | 风险与质量 | 0 | — | — | — | UNTESTED | Assessment of a company's operating income relative to its peers. |
| 499 | `operational_efficiency_metric_4` | VECTOR | 0.860 | 其他 | 0 | — | — | — | UNTESTED | Metric evaluating the effectiveness of a company's operations. |
| 500 | `operational_efficiency_metric_5` | VECTOR | 0.860 | 其他 | 0 | — | — | — | UNTESTED | Metric assessing the operational effectiveness of a company. |
| 501 | `operational_efficiency_metric_6` | VECTOR | 0.860 | 其他 | 0 | — | — | — | UNTESTED | Metric evaluating operational efficiency in resource utilization. |
| 502 | `operational_efficiency_metric_7` | VECTOR | 0.860 | 其他 | 0 | — | — | — | UNTESTED | Metric evaluating the effectiveness of company operations. |
| 503 | `operational_efficiency_metric_8` | VECTOR | 0.860 | 其他 | 0 | — | — | — | UNTESTED | Measure of how effectively a company utilizes its resources. |
| 504 | `operational_efficiency_score_2` | VECTOR | 0.860 | 风险与质量 | 0 | — | — | — | UNTESTED | Score measuring how effectively a company uses its resources. |
| 505 | `operational_efficiency_score_3` | VECTOR | 0.860 | 风险与质量 | 0 | — | — | — | UNTESTED | Score evaluating the efficiency of a company's operations. |
| 506 | `operational_efficiency_score_4` | VECTOR | 0.860 | 风险与质量 | 0 | — | — | — | UNTESTED | Score measuring the efficiency of company operations. |
| 507 | `operational_efficiency_score_5` | VECTOR | 0.860 | 风险与质量 | 0 | — | — | — | UNTESTED | Score measuring operational efficiency in company processes. |
| 508 | `operational_efficiency_score_6` | VECTOR | 0.860 | 风险与质量 | 0 | — | — | — | UNTESTED | Score measuring the efficiency of company operations. |
| 509 | `operational_efficiency_score_7` | VECTOR | 0.860 | 风险与质量 | 0 | — | — | — | UNTESTED | Score evaluating the efficiency of company operations. |
| 510 | `operational_efficiency_score_8` | VECTOR | 0.860 | 风险与质量 | 0 | — | — | — | UNTESTED | Score measuring the efficiency of company operations. |
| 511 | `operational_efficiency_score_9` | VECTOR | 0.860 | 风险与质量 | 0 | — | — | — | UNTESTED | Score evaluating the efficiency of company operations. |
| 512 | `predicted_earnings_surprise_4` | VECTOR | 0.860 | 盈利与财务 | 0 | — | — | — | UNTESTED | Model output predicting future earnings surprises. |
| 513 | `present_physics_model_3` | VECTOR | 0.860 | 价量与波动 | 0 | — | — | — | UNTESTED | Factor modeling current shareholder returns. |
| 514 | `present_physics_model_31` | VECTOR | 0.860 | 价量与波动 | 0 | — | — | — | UNTESTED | Factor modeling current shareholder returns. |
| 515 | `present_physics_model_4` | VECTOR | 0.860 | 价量与波动 | 0 | — | — | — | UNTESTED | Factor modeling current shareholder returns. |
| 516 | `projected_excess_return` | VECTOR | 0.860 | 价量与波动 | 0 | — | — | — | UNTESTED | Model output for the expected excess return of a security. |
| 517 | `pure_alpha_generation_metric_6` | VECTOR | 0.860 | 价量与波动 | 0 | — | — | — | UNTESTED | Model designed to generate returns independent of market direction. |
| 518 | `recent_uncertainty_score_2` | VECTOR | 0.860 | 风险与质量 | 0 | — | — | — | UNTESTED | Measure of uncertainty in a company's business model in the recent period. |
| 519 | `relative_valuation_comparison_4` | VECTOR | 0.860 | 其他 | 0 | — | — | — | UNTESTED | Valuation based on comparison to peers or benchmarks. |
| 520 | `relative_valuation_comparison_41` | VECTOR | 0.860 | 其他 | 0 | — | — | — | UNTESTED | Valuation based on comparison to peers or benchmarks. |
| 521 | `relative_valuation_comparison_5` | VECTOR | 0.860 | 其他 | 0 | — | — | — | UNTESTED | Valuation based on comparison to peers or benchmarks. |
| 522 | `replacement_asset_value_model_4` | VECTOR | 0.860 | 盈利与财务 | 0 | — | — | — | UNTESTED | Model estimating the cost to replace a company's assets. |
| 523 | `replacement_asset_value_model_5` | VECTOR | 0.860 | 盈利与财务 | 0 | — | — | — | UNTESTED | Model estimating the cost to replace a company's assets. |
| 524 | `replacement_asset_value_model_6` | VECTOR | 0.860 | 盈利与财务 | 0 | — | — | — | UNTESTED | Model estimating the cost to replace a company's assets. |
| 525 | `replacement_asset_value_model_61` | VECTOR | 0.860 | 修正与预期 | 0 | — | — | — | UNTESTED | Estimate of the cost to replace a company's assets. |
| 526 | `replacement_asset_value_model_7` | VECTOR | 0.860 | 修正与预期 | 0 | — | — | — | UNTESTED | Estimate of the cost to replace a company's assets. |
| 527 | `replacement_asset_value_model_71` | VECTOR | 0.860 | 盈利与财务 | 0 | — | — | — | UNTESTED | Model estimating the cost to replace a company's assets. |
| 528 | `share_buyback_activity_analysis_6` | VECTOR | 0.860 | 其他 | 0 | — | — | — | UNTESTED | Analysis of company share repurchase activities and their impact. |
| 529 | `share_buyback_activity_analysis_7` | VECTOR | 0.860 | 其他 | 0 | — | — | — | UNTESTED | Analysis of company share repurchase activities. |
| 530 | `share_buyback_activity_analysis_71` | VECTOR | 0.860 | 其他 | 0 | — | — | — | UNTESTED | Analysis of company share repurchase activities. |
| 531 | `share_buyback_activity_analysis_8` | VECTOR | 0.860 | 其他 | 0 | — | — | — | UNTESTED | Analysis of company share repurchase activities. |
| 532 | `shareholder_equity_growth_rate_2` | VECTOR | 0.860 | 盈利与财务 | 0 | — | — | — | UNTESTED | Rate at which shareholder equity is increasing or decreasing over time. |
| 533 | `shareholder_equity_growth_rate_3` | VECTOR | 0.860 | 盈利与财务 | 0 | — | — | — | UNTESTED | Annualized growth rate of shareholder equity over a specified period. |
| 534 | `shareholder_equity_growth_rate_31` | VECTOR | 0.860 | 盈利与财务 | 0 | — | — | — | UNTESTED | Growth rate of shareholder equity over a specified period. |
| 535 | `shareholder_equity_growth_rate_4` | VECTOR | 0.860 | 盈利与财务 | 0 | — | — | — | UNTESTED | Rate of change in shareholder equity over a period. |
| 536 | `shareholder_equity_growth_rate_5` | VECTOR | 0.860 | 盈利与财务 | 0 | — | — | — | UNTESTED | Growth rate of shareholder equity over time. |
| 537 | `shareholder_equity_growth_rate_6` | VECTOR | 0.860 | 盈利与财务 | 0 | — | — | — | UNTESTED | Rate at which shareholder equity changes over time. |
| 538 | `shareholder_equity_growth_rate_7` | VECTOR | 0.860 | 盈利与财务 | 0 | — | — | — | UNTESTED | Growth rate of shareholder equity over a given period. |
| 539 | `shareholder_equity_to_assets_ratio_metric_2` | VECTOR | 0.860 | 盈利与财务 | 0 | — | — | — | UNTESTED | Ratio of shareholder equity to total assets, indicating financial stability. |
| 540 | `shareholder_equity_to_assets_ratio_metric_3` | VECTOR | 0.860 | 盈利与财务 | 0 | — | — | — | UNTESTED | Ratio of shareholder equity to total assets for financial stability. |
| 541 | `shareholder_equity_to_assets_ratio_metric_4` | VECTOR | 0.860 | 盈利与财务 | 0 | — | — | — | UNTESTED | Ratio of shareholder equity to total assets for stability assessment. |
| 542 | `shareholder_equity_to_assets_ratio_metric_5` | VECTOR | 0.860 | 盈利与财务 | 0 | — | — | — | UNTESTED | Ratio of shareholder equity to total assets for stability analysis. |
| 543 | `shareholder_equity_to_assets_ratio_metric_6` | VECTOR | 0.860 | 盈利与财务 | 0 | — | — | — | UNTESTED | Ratio of shareholder equity to total assets for stability evaluation. |
| 544 | `shareholder_return_compounding_factor_3` | VECTOR | 0.860 | 价量与波动 | 0 | — | — | — | UNTESTED | Mathematical model of shareholder returns compounding over time. |
| 545 | `shareholder_treatment_metric_4` | VECTOR | 0.860 | 其他 | 0 | — | — | — | UNTESTED | Metric evaluating how a company treats its shareholders through financial actions. |
| 546 | `shareholder_treatment_metric_5` | VECTOR | 0.860 | 其他 | 0 | — | — | — | UNTESTED | Metric evaluating shareholder treatment through financial actions. |
| 547 | `shareholder_treatment_metric_6` | VECTOR | 0.860 | 持仓与资金流 | 0 | — | — | — | UNTESTED | Analysis of financing cashflow items and related metrics affecting shareholders. |
| 548 | `shareholder_treatment_metric_61` | VECTOR | 0.860 | 持仓与资金流 | 0 | — | — | — | UNTESTED | Analysis of financing cashflow items and related metrics affecting shareholders. |
| 549 | `shareholder_treatment_metric_7` | VECTOR | 0.860 | 持仓与资金流 | 0 | — | — | — | UNTESTED | Analysis of financing cashflow items and related metrics affecting shareholders. |
| 550 | `shareholder_treatment_metric_71` | VECTOR | 0.860 | 持仓与资金流 | 0 | — | — | — | UNTESTED | Analysis of financing cashflow items and related metrics affecting shareholders. |
| 551 | `shareholder_treatment_metric_8` | VECTOR | 0.860 | 持仓与资金流 | 0 | — | — | — | UNTESTED | Analysis of financing cashflow items and related metrics affecting shareholders. |
| 552 | `shareholder_yield_metric_10` | VECTOR | 0.860 | 盈利与财务 | 0 | — | — | — | UNTESTED | Total returns to shareholders from dividends and buybacks. |
| 553 | `shareholder_yield_metric_101` | VECTOR | 0.860 | 盈利与财务 | 0 | — | — | — | UNTESTED | Analysis of total returns to shareholders from dividends and buybacks. |
| 554 | `shareholder_yield_metric_11` | VECTOR | 0.860 | 盈利与财务 | 0 | — | — | — | UNTESTED | Total returns to shareholders from dividends and buybacks. |
| 555 | `shareholder_yield_metric_111` | VECTOR | 0.860 | 盈利与财务 | 0 | — | — | — | UNTESTED | Analysis of total returns to shareholders from dividends and buybacks. |
| 556 | `shareholder_yield_metric_5` | VECTOR | 0.860 | 盈利与财务 | 0 | — | — | — | UNTESTED | Metric evaluating total returns to shareholders from dividends and buybacks. |
| 557 | `shareholder_yield_metric_6` | VECTOR | 0.860 | 盈利与财务 | 0 | — | — | — | UNTESTED | Metric assessing total returns to shareholders from dividends and buybacks. |
| 558 | `shareholder_yield_metric_7` | VECTOR | 0.860 | 价量与波动 | 0 | — | — | — | UNTESTED | Metric assessing total returns to shareholders from distributions. |
| 559 | `shareholder_yield_metric_8` | VECTOR | 0.860 | 盈利与财务 | 0 | — | — | — | UNTESTED | Metric evaluating shareholder returns from dividends and buybacks. |
| 560 | `shareholder_yield_metric_9` | VECTOR | 0.860 | 价量与波动 | 0 | — | — | — | UNTESTED | Metric evaluating total returns to shareholders from distributions. |
| 561 | `short_term_indicators_score_2` | VECTOR | 0.860 | 风险与质量 | 0 | — | — | — | UNTESTED | Technical indicators measuring short-term trends. |
| 562 | `short_term_physics_model_3` | VECTOR | 0.860 | 价量与波动 | 0 | — | — | — | UNTESTED | Factor modeling shareholder returns over a short period. |
| 563 | `short_term_physics_model_31` | VECTOR | 0.860 | 价量与波动 | 0 | — | — | — | UNTESTED | Factor modeling shareholder returns over a short period. |
| 564 | `short_term_physics_model_4` | VECTOR | 0.860 | 价量与波动 | 0 | — | — | — | UNTESTED | Factor modeling shareholder returns over a short period. |
| 565 | `short_term_technical_trend_indicator_4` | VECTOR | 0.860 | 其他 | 0 | — | — | — | UNTESTED | Technical indicators measuring short-term trends. |
| 566 | `short_term_technical_trend_indicator_5` | VECTOR | 0.860 | 其他 | 0 | — | — | — | UNTESTED | Technical indicators measuring short-term trends. |
| 567 | `short_term_technical_valuation_model_4` | VECTOR | 0.860 | 价量与波动 | 0 | — | — | — | UNTESTED | Technical valuation models focused on short-term price trends. |
| 568 | `short_term_technical_valuation_model_41` | VECTOR | 0.860 | 价量与波动 | 0 | — | — | — | UNTESTED | Technical valuation model focused on short-term price trends. |
| 569 | `short_term_technical_valuation_model_5` | VECTOR | 0.860 | 价量与波动 | 0 | — | — | — | UNTESTED | Technical valuation models focused on short-term price trends. |
| 570 | `size_factor_2` | VECTOR | 0.860 | 其他 | 0 | — | — | — | UNTESTED | Factor representing the scale or market capitalization of a company. |
| 571 | `technical_indicator_composite_4` | VECTOR | 0.860 | 价量与波动 | 0 | — | — | — | UNTESTED | Aggregated technical indicators for momentum and reversion. |
| 572 | `technical_indicator_composite_5` | VECTOR | 0.860 | 价量与波动 | 0 | — | — | — | UNTESTED | Aggregated technical indicators for momentum and reversion. |
| 573 | `technical_indicator_composite_6` | VECTOR | 0.860 | 价量与波动 | 0 | — | — | — | UNTESTED | Aggregated technical indicators for momentum and reversion. |
| 574 | `trend_in_buzz_score_3` | VECTOR | 0.860 | 情绪与新闻 | 0 | — | — | — | UNTESTED | Measure of changes in market or media attention over time. |
| 575 | `trend_in_buzz_score_31` | VECTOR | 0.860 | 情绪与新闻 | 0 | — | — | — | UNTESTED | Measure of changes in market or media attention over time. |
| 576 | `trend_in_perception_score_3` | VECTOR | 0.860 | 修正与预期 | 0 | — | — | — | UNTESTED | Measure of changes in market or analyst perception over time. |
| 577 | `trend_in_perception_score_31` | VECTOR | 0.860 | 修正与预期 | 0 | — | — | — | UNTESTED | Measure of changes in market or analyst perception over time. |
| 578 | `trend_in_perception_score_4` | VECTOR | 0.860 | 修正与预期 | 0 | — | — | — | UNTESTED | Measure of changes in market or analyst perception over time. |
| 579 | `trend_in_perception_score_41` | VECTOR | 0.860 | 修正与预期 | 0 | — | — | — | UNTESTED | Measure of changes in market or analyst perception over time. |
| 580 | `trend_in_perception_score_5` | VECTOR | 0.860 | 修正与预期 | 0 | — | — | — | UNTESTED | Measure of changes in market or analyst perception over time. |
| 581 | `valuation_model_suite_3` | VECTOR | 0.860 | 其他 | 0 | — | — | — | UNTESTED | Suite of models estimating company value from intrinsic to replacement and forecasting changes in valuation. |
| 582 | `write_down_risk_score_2` | VECTOR | 0.860 | 盈利与财务 | 0 | — | — | — | UNTESTED | Risk of asset value reduction due to impairment. |

## 六、本地回测证据

- 本地累计回测 **23** 条；其中 `ra_failed_checks` 为空的 **23** 条（⚠ 空不等于过关，2Y 为 NULL 者需复检）

| alpha | S | F | 2Y | sub | TO | RA失败数 | wave | 表达式（截断） |
|---|---:|---:|---:|---:|---:|---|---:|---|
| `gJW1zMje` | 1.54 | 1.22 | 2.01 | 0.81 | 0.04 | 0 | w666 | `multiply(normalize(ts_backfill(vec_avg(accruals_contribution_score_3), 504), useStd=true, ` |
| `E5VwAElr` | 1.48 | 1.17 | 1.97 | 0.78 | 0.03 | 0 | w666 | `multiply(normalize(ts_backfill(vec_avg(accruals_contribution_score_3), 504), useStd=true, ` |
| `npAgb2Kx` | 1.44 | 1.13 | 1.95 | 0.76 | 0.03 | 0 | w666 | `multiply(normalize(ts_backfill(vec_avg(accruals_contribution_score_3), 504), useStd=true, ` |
| `gJW1Ko9K` | 1.19 | 0.92 | 2.08 | 0.61 | 0.06 | 0 | w667b | `multiply(normalize(ts_backfill(vec_avg(accruals_contribution_score_3), 504), useStd=true, ` |
| `ZYmo9RY0` | 1.12 | 0.65 | 2.02 | 0.30 | 0.05 | 0 | w649 | `group_rank(ts_backfill(vec_avg(cash_conversion_efficiency_score), 22), sector)` |
| `N1eOGXxE` | 1.12 | 0.65 | 2.02 | 0.30 | 0.05 | 0 | w649 | `scale(group_rank(ts_backfill(vec_avg(cash_conversion_efficiency_score), 22), sector), long` |
| `A1Q35R9l` | 1.07 | 0.70 | 1.90 | 0.29 | 0.05 | 0 | w649 | `normalize(ts_backfill(vec_avg(cash_conversion_efficiency_score), 22), useStd=true, limit=3` |
| `zqrWEvZX` | 1.04 | 0.68 | 1.91 | 0.29 | 0.06 | 0 | w649 | `zscore(ts_backfill(vec_avg(cash_conversion_efficiency_score), 22))` |
| `GrgoNqa3` | 1.01 | 0.56 | 1.82 | 0.32 | 0.05 | 0 | w649 | `signed_power(group_rank(ts_backfill(vec_avg(cash_conversion_efficiency_score), 22), indust` |
| `2rj7MdbN` | 0.98 | 0.74 | 1.97 | 0.49 | 0.02 | 0 | w667b | `normalize(ts_backfill(vec_avg(accruals_contribution_score_3), 504), useStd=true, limit=2)` |
| `2rjKx18b` | 0.96 | 0.56 | 1.76 | 0.28 | 0.06 | 0 | w649 | `signed_power(group_rank(ts_backfill(vec_avg(cash_conversion_efficiency_score), 22), sector` |
| `58jv1Zbn` | 0.91 | 0.53 | 1.50 | 0.14 | 0.20 | 0 | w649 | `ts_ir(ts_backfill(vec_avg(cash_conversion_efficiency_score), 22), 66)` |
| `rKdWw1pj` | 0.68 | 0.23 | 1.28 | 0.08 | 0.18 | 0 | w649 | `signed_power(group_rank(ts_zscore(ts_backfill(vec_avg(cash_conversion_efficiency_score), 2` |
| `GrgoKGb5` | 0.63 | 0.24 | 1.58 | 0.09 | 0.13 | 0 | w642 | `signed_power(group_rank(ts_backfill(vec_avg(earnings_surprise_magnitude_score), 22), secto` |
| `0mj8Nprr` | 0.63 | 0.22 | 2.30 | 0.25 | 0.17 | 0 | w642 | `signed_power(group_rank(ts_backfill(vec_avg(earnings_surprise_magnitude_score), 22), marke` |

## 七、判死记录（sealed dead_end）

- `EUR-AIEQ-VOL-SCORE-PRODCORR`（2026-08-23）family=ai_equity_alpha financial_statement_volatility_factor / alpha_score dominant legs：{"region": "EUR", "dataset": "ai_equity_alpha", "rule": "Do not use financial_statement_volatility_factor or alpha_score as the dominant (weight>=0.6) leg. Wrappers/group/ts_av_diff/SLOW-X-FAST mix still prod 0.78-0.83.", "evidence": {"rKjpl3g3": {"sharpe": 2, "prod": 0.8144, "expr": "rank(add(vec_avg(financial_statement_volatility_factor), vec_avg(alpha_score)))"}, "omqn3Lkn": {"sharpe": 1.35, "p
- `EUR-AIEQ-ANALYST-REV-NOSCORE-WEAK`（2026-08-24）family=ai_equity_alpha analyst revision without vol/score：{"dataset": "ai_equity_alpha", "max_abs_sharpe": 0.57, "best": "Vk7X7dv0", "wave": 38, "id": "EUR-AIEQ-ANALYST-REV-NOSCORE-WEAK", "family": "ai_equity_alpha analyst revision without vol/score", "reason": "Wave38 slot4 analyst revision/forecast/target/opinion without vol/score max /S/0.57. Weak set, do not occupy another slot.", "rule": "Do not occupy slots with AIEQ analyst-revision family without
- `EUR-AIEQ-FORENSIC-ACCRUAL-MIX-PROD`（2026-08-24）family=ai_equity forensic+accrual mix dominant：{"dataset": "ai_equity_alpha", "example_id": "KP7nJl8g", "sharpe": 0.96, "fitness": 0.58, "two_year_sharpe": 1.9, "prod_corr": 0.8161, "wave": 39, "reason": "0.6 forensic + 0.4 invert accruals S0.96 F0.58 2Y1.90 TVR8.3% but prod 0.8161. 2Y already passes; Mode A will not break prod. Leave forensic/accrual as dominant.", "rule": "Do not use forensic+accrual mix as dominant. Mode B must change AIEQ 
- `EUR-AIEQ-W50-QOC-LIQ-CLARITY-WEAK`（2026-08-24）family=ai_equity quality/opacity/unused liquidity/clarity x v_rev x wedge：{"best": {"RR7pJvNd": 1.31}, "dataset": "ai_equity_alpha", "max_sharpe": {"5d": 0.55, "clarity": 0.88, "eq": 0.72, "liq": 1.31, "opacity": 1.12}, "reason": "Wave50 AIEQ unused VECTOR 3leg all missed cheap gate. Best asset_liquidity_score_2 S1.31. five_day 0.55. Do not grind.", "rule": "Do not occupy slots with earnings_quality, information_opacity, liquidity_buffer/asset_liquidity_score_2, busines
- `EUR-AIEQ-W55-SHTR-FDISP-FACC-FFLOW-WEAK`（2026-08-24）family=ai_equity_alpha：{"best": {"alpha": "bljL3bal", "sharpe": 1.2}, "dataset": "ai_equity_alpha", "do_not_retry": ["shareholder_treatment_metric", "forecast_dispersion_metric", "forecast_error_magnitude_metric", "forecast_value_accuracy_metric", "forecast_accuracy_variance_score", "fund_flow_prediction_metric_2", "pure_alpha_generation_metric_2", "perception_trend_metric", "combined_technical_indicators_2", "price_to_
- `EUR-AIEQ-W56-BUYB-BUZZ-FIN-SIZE-WEAK`（2026-08-24）family=ai_equity_alpha：{"best": {"alpha": "pwj6Q0Yv", "sharpe": 1.35}, "dataset": "ai_equity_alpha", "do_not_retry": ["share_buyback_activity_analysis", "buzz_intensity_score", "financing_structure_analysis_2", "company_size_factor_2", "income_statement_trend_metric", "nlp_sentiment_alpha_factor_2", "medium_term_business_uncertainty"], "reason": "Wave56 0.30/0.40/0.30 x v_rev/wedge: max S1.35 failed cheap gate", "wave":
- `EUR-AIEQ-W57-EQA-FCHG-PTB-DEBT-WEAK`（2026-08-24）family=ai_equity_alpha：{"best": {"alpha": "3ql7Ymoe", "sharpe": 0.82}, "dataset": "ai_equity_alpha", "do_not_retry": ["shareholder_equity_to_assets_ratio_metric", "financial_change_trend_analysis", "operating_income_variability_score", "price_to_book_ratio_metric", "operating_expense_ratio_factor", "operating_income_score_3", "debt_to_capital_ratio_metric", "debt_to_enterprise_value_ratio_metric", "debt_maturity_profile

