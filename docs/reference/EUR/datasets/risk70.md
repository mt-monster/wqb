# risk70 — EUR 字段画像

> 自动生成于 2026-10-20 17:55　|　[← 返回索引](README.md)

## 一、数据集元信息

| 项 | 值 |
|---|---|
| 数据集 ID | `risk70` |
| 名称 | Multi-Factor Model |
| 类别 | RISK |
| 数据字段数(平台) | 87 |
| 覆盖率 | 0.9817 |
| 平台已有 alpha | 6112 |
| valueScore | 1.0 |
| 金字塔倍率 | 1.0 |
| 数据类型 | — |
| delay | 1 |
| 状态 | — |

## 二、数据集描述（平台原文）

> ⚠️ 平台目录描述存在**错配**（已实测：insiders1 / imbalance5 的描述指向无关数据集）。以「五、全字段明细」的真实字段语义为准。

This dataset provides comprehensive global equity ownership data, tracking holdings by institutions, mutual funds, insiders, and stakeholders. It aggregates information from regulatory filings such as SEC Form 13F, UK share registers, and other international sources, offering detailed position-level data including shares held, percentage ownership, and changes over time. The dataset enables analysis of institutional trading patterns, herding behavior, and the impact of ownership changes on stock returns. By monitoring shifts in institutional ownership and identifying high-conviction positions, researchers can gain insights into market sentiment, potential price movements, and the effectiveness of copycat or contrarian investment strategies. This data is valuable for constructing factors re

## 三、字段画像汇总

| 维度 | 结果 |
|---|---|
| 字段总数 | **87** |
| 类型分布 | MATRIX×87 |
| 平均覆盖率 | **0.982** |
| 覆盖率区间 | 0.33 ~ 1.00 |
| 更新频率（推断） | 快照（按库表更新，需实测） |
| 可用性评级 | 优（覆盖 ≥90%，可直接做尽） |

**覆盖率分档**

| 档 | 字段数 | 占比 |
|---|---:|---:|
| 高 (≥0.90) | 84 | 96.6% |
| 中 (0.70–0.90) | 2 | 2.3% |
| 低 (0.50–0.70) | 0 | 0.0% |
| 稀疏 (<0.50) | 1 | 1.1% |

**历史实测分布（field_profile_perf）**

| 判定 | 字段数 | 占比 |
|---|---:|---:|
| UNTESTED | 83 | 95.4% |
| DEAD | 3 | 3.4% |
| UNUSABLE | 1 | 1.1% |

- 已实测字段：**3** 个（3%），best_sharpe 最高 **1.00**，中位 0.38

## 四、语义维度地图（自动归类）

| 语义族 | 字段数 | 平均覆盖 | 代表字段 |
|---|---:|---:|---|
| 宏观与行业 | 53 | 0.99 | airlines_sector_exposure、auto_components_sector_exposure、banking_sector_exposure |
| 其他 | 10 | 0.97 | current_market_cap_usd、rsk70_mfm2_euetrd_exeurexp、rsk70_mfm2_euetrd_indadj |
| 价量与波动 | 8 | 0.99 | rsk70_mfm2_euetrd_strevrsl、rsk70_mfm2_euetrd_momentum、momentum_factor_exposure |
| 风险与质量 | 5 | 0.97 | broad_market_factor_exposure、rsk70_mfm2_euetrd_beta、rsk70_mfm2_euetrd_srisk |
| 盈利与财务 | 5 | 0.95 | rsk70_mfm2_euetrd_earnyild、rsk70_mfm2_euetrd_divyild、rsk70_mfm2_euetrd_earnqlty |
| 持仓与资金流 | 4 | 1.00 | european_hedge_fund_ownership_count、hedge_fund_ownership_percent_europe、rsk70_mfm2_euetrd_shortint |
| 情绪与新闻 | 1 | 0.96 | rsk70_mfm2_euetrd_newssent |
| 修正与预期 | 1 | 0.91 | rsk70_mfm2_euetrd_anlystsn |

## 五、全字段明细

> 按 `best_sharpe` 降序（未测者置后）。`判定` 来自 `field_profile_perf`：ALIVE=历史测出过 S≥闸线（**不代表可提交**）；UNTESTED=未测；UNUSABLE/DEAD/AXIS_ONLY=已证否或仅可作轴。

| # | 字段名 | 类型 | 覆盖 | 语义族 | 测次 | best_S | best_2Y | best_sub | 判定 | 描述 |
|---:|---|---|---:|---|---:|---:|---:|---:|---|---|
| 1 | `rsk70_mfm2_euetrd_strevrsl` | MATRIX | 1.000 | 价量与波动 | 1 | 1.00 | — | — | DEAD | Short-Term Reversal Style Factor Loading |
| 2 | `rsk70_mfm2_euetrd_newssent` | MATRIX | 0.960 | 情绪与新闻 | 1 | 0.38 | — | — | DEAD | News Sentiment Style Factor Loading |
| 3 | `rsk70_mfm2_euetrd_momentum` | MATRIX | 1.000 | 价量与波动 | 1 | 0.35 | — | — | DEAD | Momentum Style Factor Loading |
| 4 | `airlines_sector_exposure` | MATRIX | 1.000 | 宏观与行业 | 0 | — | — | — | UNTESTED | Exposure or weight to the airlines industry sector within the model. |
| 5 | `auto_components_sector_exposure` | MATRIX | 1.000 | 宏观与行业 | 0 | — | — | — | UNTESTED | Exposure or weight to the auto components industry sector within the model. |
| 6 | `banking_sector_exposure` | MATRIX | 1.000 | 宏观与行业 | 0 | — | — | — | UNTESTED | Exposure or weight to the banking industry sector within the model. |
| 7 | `broad_market_factor_exposure` | MATRIX | 1.000 | 风险与质量 | 0 | — | — | — | UNTESTED | Exposure or sensitivity to the overall market factor in the risk model. |
| 8 | `capital_goods_sector_exposure` | MATRIX | 1.000 | 宏观与行业 | 0 | — | — | — | UNTESTED | Exposure or weight to the capital goods industry sector within the model. |
| 9 | `communications_services_exposure_score` | MATRIX | 1.000 | 宏观与行业 | 0 | — | — | — | UNTESTED | Exposure or sensitivity to the communications services sector factor. |
| 10 | `construction_sector_exposure` | MATRIX | 1.000 | 宏观与行业 | 0 | — | — | — | UNTESTED | Exposure or weight to the construction industry sector within the model. |
| 11 | `consumer_durables_exposure_score` | MATRIX | 1.000 | 宏观与行业 | 0 | — | — | — | UNTESTED | Exposure or sensitivity to the consumer durables sector factor. |
| 12 | `consumer_services_exposure_score` | MATRIX | 1.000 | 宏观与行业 | 0 | — | — | — | UNTESTED | Exposure or sensitivity to the consumer services sector factor. |
| 13 | `country_austria_exposure_score` | MATRIX | 1.000 | 宏观与行业 | 0 | — | — | — | UNTESTED | Exposure or sensitivity to the Austria country factor. |
| 14 | `country_exposure_bel` | MATRIX | 1.000 | 宏观与行业 | 0 | — | — | — | UNTESTED | Exposure or weight to companies domiciled in Belgium. |
| 15 | `country_exposure_deu` | MATRIX | 1.000 | 宏观与行业 | 0 | — | — | — | UNTESTED | Exposure or weight to companies domiciled in Germany. |
| 16 | `country_exposure_dnk` | MATRIX | 1.000 | 宏观与行业 | 0 | — | — | — | UNTESTED | Exposure or weight to companies domiciled in Denmark. |
| 17 | `country_exposure_esp` | MATRIX | 1.000 | 宏观与行业 | 0 | — | — | — | UNTESTED | Exposure or weight to companies domiciled in Spain. |
| 18 | `country_exposure_gbr` | MATRIX | 1.000 | 宏观与行业 | 0 | — | — | — | UNTESTED | Exposure or weight to companies domiciled in the United Kingdom. |
| 19 | `country_exposure_irl` | MATRIX | 1.000 | 宏观与行业 | 0 | — | — | — | UNTESTED | Exposure or weight to companies domiciled in Ireland. |
| 20 | `country_exposure_nld` | MATRIX | 1.000 | 宏观与行业 | 0 | — | — | — | UNTESTED | Exposure or weight to companies domiciled in the Netherlands. |
| 21 | `country_finland_exposure_score` | MATRIX | 1.000 | 宏观与行业 | 0 | — | — | — | UNTESTED | Exposure or sensitivity to the Finland country factor. |
| 22 | `country_france_exposure_score` | MATRIX | 1.000 | 宏观与行业 | 0 | — | — | — | UNTESTED | Exposure or sensitivity to the France country factor. |
| 23 | `country_italy_exposure_score` | MATRIX | 1.000 | 宏观与行业 | 0 | — | — | — | UNTESTED | Exposure or sensitivity to the Italy country factor. |
| 24 | `country_norway_exposure_score` | MATRIX | 1.000 | 宏观与行业 | 0 | — | — | — | UNTESTED | Exposure or sensitivity to the Norway country factor. |
| 25 | `country_portugal_exposure_score` | MATRIX | 1.000 | 宏观与行业 | 0 | — | — | — | UNTESTED | Exposure or sensitivity to the Portugal country factor. |
| 26 | `country_southafrica_exposure_score` | MATRIX | 1.000 | 宏观与行业 | 0 | — | — | — | UNTESTED | Exposure or sensitivity to the South Africa country factor. |
| 27 | `country_sweden_exposure_score` | MATRIX | 1.000 | 宏观与行业 | 0 | — | — | — | UNTESTED | Exposure or sensitivity to the Sweden country factor. |
| 28 | `country_switzerland_exposure_score` | MATRIX | 1.000 | 宏观与行业 | 0 | — | — | — | UNTESTED | Exposure or sensitivity to the Switzerland country factor. |
| 29 | `current_market_cap_usd` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | The current market capitalization of the company in US dollars. |
| 30 | `diversified_financials_europe_exposure_score` | MATRIX | 1.000 | 宏观与行业 | 0 | — | — | — | UNTESTED | Exposure or sensitivity to the diversified financials sector factor within the European universe. |
| 31 | `energy_sector_exposure_score_2` | MATRIX | 1.000 | 宏观与行业 | 0 | — | — | — | UNTESTED | Exposure or sensitivity to the energy sector factor. |
| 32 | `european_hedge_fund_ownership_count` | MATRIX | 1.000 | 持仓与资金流 | 0 | — | — | — | UNTESTED | Number of hedge funds holding a position in the security within the European universe. |
| 33 | `food_products_sector_exposure` | MATRIX | 1.000 | 宏观与行业 | 0 | — | — | — | UNTESTED | Exposure or weight to the food products industry sector within the model. |
| 34 | `food_retail_europe_exposure_score` | MATRIX | 1.000 | 宏观与行业 | 0 | — | — | — | UNTESTED | Exposure or sensitivity to the food retail sector factor within the European universe. |
| 35 | `hardware_sector_exposure` | MATRIX | 1.000 | 宏观与行业 | 0 | — | — | — | UNTESTED | Exposure or weight to the hardware industry sector within the model. |
| 36 | `healthcare_sector_exposure_score_2` | MATRIX | 1.000 | 宏观与行业 | 0 | — | — | — | UNTESTED | Exposure or sensitivity to the healthcare sector factor. |
| 37 | `hedge_fund_ownership_percent_europe` | MATRIX | 1.000 | 持仓与资金流 | 0 | — | — | — | UNTESTED | Percentage of shares owned by hedge funds in European companies. |
| 38 | `household_products_exposure_score` | MATRIX | 1.000 | 宏观与行业 | 0 | — | — | — | UNTESTED | Exposure or sensitivity to the household products sector factor. |
| 39 | `industry_count_short` | MATRIX | 1.000 | 宏观与行业 | 0 | — | — | — | UNTESTED | The number of distinct industry sectors represented in the short leg of the portfolio or model. |
| 40 | `insurance_sector_exposure` | MATRIX | 1.000 | 宏观与行业 | 0 | — | — | — | UNTESTED | Exposure or weight to the insurance industry sector within the model. |
| 41 | `machinery_sector_exposure_score` | MATRIX | 1.000 | 宏观与行业 | 0 | — | — | — | UNTESTED | Exposure or sensitivity to the machinery sector factor. |
| 42 | `media_sector_exposure` | MATRIX | 1.000 | 宏观与行业 | 0 | — | — | — | UNTESTED | Exposure or weight to the media industry sector within the model. |
| 43 | `metals_mining_exposure_score` | MATRIX | 1.000 | 宏观与行业 | 0 | — | — | — | UNTESTED | Exposure or sensitivity to the metals and mining sector factor. |
| 44 | `momentum_factor_exposure` | MATRIX | 1.000 | 价量与波动 | 0 | — | — | — | UNTESTED | Exposure or sensitivity to the momentum style factor in the risk model. |
| 45 | `oil_gas_sector_exposure_score` | MATRIX | 1.000 | 宏观与行业 | 0 | — | — | — | UNTESTED | Exposure or sensitivity to the oil and gas sector factor. |
| 46 | `other_materials_sector_exposure` | MATRIX | 1.000 | 宏观与行业 | 0 | — | — | — | UNTESTED | Exposure or weight to the other materials industry sector within the model. |
| 47 | `pharmaceuticals_europe_exposure_score` | MATRIX | 1.000 | 宏观与行业 | 0 | — | — | — | UNTESTED | Exposure or sensitivity to the pharmaceuticals sector factor within the European universe. |
| 48 | `real_estate_europe_exposure_score` | MATRIX | 1.000 | 宏观与行业 | 0 | — | — | — | UNTESTED | Exposure or sensitivity to the real estate sector factor within the European universe. |
| 49 | `retail_sector_exposure` | MATRIX | 1.000 | 宏观与行业 | 0 | — | — | — | UNTESTED | Exposure or weight to the retail industry sector within the model. |
| 50 | `rsk70_mfm2_euetrd_beta` | MATRIX | 1.000 | 风险与质量 | 0 | — | — | — | UNTESTED | Beta Style Factor Loading |
| 51 | `rsk70_mfm2_euetrd_cntadj` | MATRIX | 1.000 | 宏观与行业 | 0 | — | — | — | UNTESTED | Country adjusted factor loading |
| 52 | `rsk70_mfm2_euetrd_earnyild` | MATRIX | 1.000 | 盈利与财务 | 0 | — | — | — | UNTESTED | Earnings Yield Style Factor Loading |
| 53 | `rsk70_mfm2_euetrd_exeurexp` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | Europe Exposure Style Factor Loading |
| 54 | `rsk70_mfm2_euetrd_indadj` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | Industrial adjustment factor loading |
| 55 | `rsk70_mfm2_euetrd_indmom` | MATRIX | 1.000 | 价量与波动 | 0 | — | — | — | UNTESTED | Industrial Momentum Style Factor Loading |
| 56 | `rsk70_mfm2_euetrd_ltrevrsl` | MATRIX | 1.000 | 价量与波动 | 0 | — | — | — | UNTESTED | Long-Term Reversal Style Factor Loading |
| 57 | `rsk70_mfm2_euetrd_market` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | Market Market Factor Loading |
| 58 | `rsk70_mfm2_euetrd_midcap` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | Midcap Style Factor Loading |
| 59 | `rsk70_mfm2_euetrd_primaryindustry` | MATRIX | 1.000 | 宏观与行业 | 0 | — | — | — | UNTESTED | Industry factor loading |
| 60 | `rsk70_mfm2_euetrd_resvol` | MATRIX | 1.000 | 价量与波动 | 0 | — | — | — | UNTESTED | Residual Volatility Style Factor Loading |
| 61 | `rsk70_mfm2_euetrd_season` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | Season Style Factor Loading |
| 62 | `rsk70_mfm2_euetrd_shortint` | MATRIX | 1.000 | 持仓与资金流 | 0 | — | — | — | UNTESTED | Short Interest Style Factor Loading |
| 63 | `rsk70_mfm2_euetrd_size` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | Size Style Factor Loading |
| 64 | `rsk70_mfm2_euetrd_srisk` | MATRIX | 1.000 | 风险与质量 | 0 | — | — | — | UNTESTED | Final specific risk annualized in units of %-squared |
| 65 | `rsk70_mfm2_euetrd_srisku` | MATRIX | 1.000 | 风险与质量 | 0 | — | — | — | UNTESTED | Unadjusted initial specific risk annualized in units of %-squared |
| 66 | `rsk70_mfm2_euetrd_srtindcnt` | MATRIX | 1.000 | 宏观与行业 | 0 | — | — | — | UNTESTED | Industry factor loading |
| 67 | `rsk70_trsd_drteue_2mfm` | MATRIX | 1.000 | 价量与波动 | 0 | — | — | — | UNTESTED | Specific returns |
| 68 | `semiconductor_sector_exposure` | MATRIX | 1.000 | 宏观与行业 | 0 | — | — | — | UNTESTED | Exposure or weight to the semiconductor industry sector within the model. |
| 69 | `short_interest_europe_factor_score` | MATRIX | 1.000 | 持仓与资金流 | 0 | — | — | — | UNTESTED | Exposure to the short interest factor within the European universe, reflecting short selling activity. |
| 70 | `software_sector_exposure_score` | MATRIX | 1.000 | 宏观与行业 | 0 | — | — | — | UNTESTED | Exposure or sensitivity to the software sector factor. |
| 71 | `telecom_services_exposure_score` | MATRIX | 1.000 | 宏观与行业 | 0 | — | — | — | UNTESTED | Exposure or sensitivity to the telecom services sector factor. |
| 72 | `transportation_sector_exposure` | MATRIX | 1.000 | 宏观与行业 | 0 | — | — | — | UNTESTED | Exposure or weight to the transportation industry sector within the model. |
| 73 | `utilities_sector_exposure_score_2` | MATRIX | 1.000 | 宏观与行业 | 0 | — | — | — | UNTESTED | Exposure or sensitivity to the utilities sector factor. |
| 74 | `primary_industry_classification` | MATRIX | 0.997 | 宏观与行业 | 0 | — | — | — | UNTESTED | The main industry classification assigned to the company or security. |
| 75 | `country_adjustment_factor` | MATRIX | 0.991 | 宏观与行业 | 0 | — | — | — | UNTESTED | Adjustment factor applied to account for country-specific effects in the model. |
| 76 | `industry_adjustment_factor` | MATRIX | 0.991 | 宏观与行业 | 0 | — | — | — | UNTESTED | Adjustment factor applied to account for industry-specific effects in the model. |
| 77 | `rsk70_mfm2_euetrd_divyild` | MATRIX | 0.972 | 盈利与财务 | 0 | — | — | — | UNTESTED | Dividend Yield Style Factor Loading |
| 78 | `rsk70_mfm2_euetrd_btop` | MATRIX | 0.959 | 价量与波动 | 0 | — | — | — | UNTESTED | Book-to-Price Style Factor Loading |
| 79 | `rsk70_mfm2_euetrd_leverage` | MATRIX | 0.958 | 其他 | 0 | — | — | — | UNTESTED | Leverage Style Factor Loading |
| 80 | `rsk70_mfm2_euetrd_earnqlty` | MATRIX | 0.938 | 盈利与财务 | 0 | — | — | — | UNTESTED | Earnings Quality Style Factor Loading |
| 81 | `rsk70_mfm2_euetrd_growth` | MATRIX | 0.916 | 其他 | 0 | — | — | — | UNTESTED | Growth Style Factor Loading |
| 82 | `rsk70_mfm2_euetrd_earnvar` | MATRIX | 0.916 | 盈利与财务 | 0 | — | — | — | UNTESTED | Earnings Variability Style Factor Loading |
| 83 | `rsk70_mfm2_euetrd_anlystsn` | MATRIX | 0.912 | 修正与预期 | 0 | — | — | — | UNTESTED | Analysts' Sentiment Style Factor Loading |
| 84 | `rsk70_mfm2_euetrd_profit` | MATRIX | 0.907 | 盈利与财务 | 0 | — | — | — | UNTESTED | Profit Style Factor Loading |
| 85 | `rsk70_ytlqsvni_drteue_2mfm` | MATRIX | 0.868 | 风险与质量 | 0 | — | — | — | UNTESTED | Investment Quality Style Factor Loading |
| 86 | `rsk70_gse_drteue_2mfm` | MATRIX | 0.788 | 其他 | 0 | — | — | — | UNTESTED | ESG Style Factor Loading |
| 87 | `rsk70_rbg_tnc_drteue_2mfm` | MATRIX | 0.331 | 宏观与行业 | 0 | — | — | — | UNUSABLE | Great Britain Country Factor Loading |

## 六、本地回测证据

本地库无该数据集的回测记录。

> 说明：`backtest_results` 只收录已持久化的波次（当前 EUR 共 1157 行）；本次会话的直接派发未写库，故此处为空**不代表未做尽**，实测结论见配套战役档案。

## 七、判死记录（sealed dead_end）

无针对本数据集的 `dead_end` 记录。

