# model238 — EUR 字段画像

> 自动生成于 2026-10-20 17:55　|　[← 返回索引](README.md)

## 一、数据集元信息

| 项 | 值 |
|---|---|
| 数据集 ID | `model238` |
| 名称 | SmartHoldings Model |
| 类别 | MODEL |
| 数据字段数(平台) | 44 |
| 覆盖率 | 0.8702 |
| 平台已有 alpha | 26 |
| valueScore | 4.0 |
| 金字塔倍率 | 1.3 |
| 数据类型 | MATRIX |
| delay | 1 |
| 状态 | scanned |

## 二、数据集描述（平台原文）

> ⚠️ 平台目录描述存在**错配**（已实测：insiders1 / imbalance5 的描述指向无关数据集）。以「五、全字段明细」的真实字段语义为准。

This dataset provides a comprehensive global ranking of stocks based on predicted future changes in institutional ownership, leveraging a quantitative model that reverse engineers fund manager purchasing profiles using fundamental and technical factors. It includes detailed ranks at global, regional, country, sector, and industry levels, as well as components measuring screening attractiveness and changes in sentiment. By identifying stocks likely to experience increased or decreased institutional buying, the dataset offers valuable signals for long/short strategies, portfolio construction, and risk management. Its predictive power is supported by backtesting, showing positive returns and high Sharpe Ratios, making it a robust tool for forecasting price movements driven by institutional fl

## 三、字段画像汇总

| 维度 | 结果 |
|---|---|
| 字段总数 | **44** |
| 类型分布 | MATRIX×44 |
| 平均覆盖率 | **0.870** |
| 覆盖率区间 | 0.77 ~ 0.96 |
| 更新频率（推断） | 快照（按库表更新，需实测） |
| 可用性评级 | 良（覆盖 70–90%，sub/robust 需关注） |

**覆盖率分档**

| 档 | 字段数 | 占比 |
|---|---:|---:|
| 高 (≥0.90) | 22 | 50.0% |
| 中 (0.70–0.90) | 22 | 50.0% |
| 低 (0.50–0.70) | 0 | 0.0% |
| 稀疏 (<0.50) | 0 | 0.0% |

**历史实测分布（field_profile_perf）**

| 判定 | 字段数 | 占比 |
|---|---:|---:|
| UNTESTED | 44 | 100.0% |

- 该数据集全部字段**尚未实测**（UNTESTED）⇒ 优先做尽

## 四、语义维度地图（自动归类）

| 语义族 | 字段数 | 平均覆盖 | 代表字段 |
|---|---:|---:|---|
| 持仓与资金流 | 28 | 0.88 | country_relative_investment_rank_d1、global_institutional_preference_rank_d1、global_screening_factor_alignment_rank_d1 |
| 价量与波动 | 9 | 0.88 | mdl238_global_owner_rank_d1、global_change_in_preference_rank_d1、mdl238_global_change_rank_d1 |
| 风险与质量 | 4 | 0.83 | mdl238_global_screening_rank_d1、global_screening_factor_alignment_rank、mdl238_global_screening_rank |
| 宏观与行业 | 3 | 0.84 | mdl238_region_screening_rank_d1、mdl238_region_screening_rank、regional_screening_factor_alignment_rank |

## 五、全字段明细

> 按 `best_sharpe` 降序（未测者置后）。`判定` 来自 `field_profile_perf`：ALIVE=历史测出过 S≥闸线（**不代表可提交**）；UNTESTED=未测；UNUSABLE/DEAD/AXIS_ONLY=已证否或仅可作轴。

| # | 字段名 | 类型 | 覆盖 | 语义族 | 测次 | best_S | best_2Y | best_sub | 判定 | 描述 |
|---:|---|---|---:|---|---:|---:|---:|---:|---|---|
| 1 | `country_relative_investment_rank_d1` | MATRIX | 0.963 | 持仓与资金流 | 0 | — | — | — | UNTESTED | Normalized (0-100) score of the stock's likelihood of institutional ownership within its country |
| 2 | `global_institutional_preference_rank_d1` | MATRIX | 0.963 | 持仓与资金流 | 0 | — | — | — | UNTESTED | Normalized (0-100) score of the stock's likelihood of institutional ownership at global level |
| 3 | `global_screening_factor_alignment_rank_d1` | MATRIX | 0.963 | 持仓与资金流 | 0 | — | — | — | UNTESTED | Normalized (0-100) score of the stock’s style-fit (screening component) globally, adjusted for peer ownership |
| 4 | `mdl238_country_rank_d1` | MATRIX | 0.963 | 持仓与资金流 | 0 | — | — | — | UNTESTED | Rank (1–100) representing the likelihood of institutional ownership for the stock within its country according to the Sm |
| 5 | `mdl238_global_rank_d1` | MATRIX | 0.963 | 持仓与资金流 | 0 | — | — | — | UNTESTED | Rank (1–100) representing the likelihood of institutional ownership for the stock across the global universe according t |
| 6 | `mdl238_global_screening_rank_d1` | MATRIX | 0.963 | 风险与质量 | 0 | — | — | — | UNTESTED | Peers-adjusted screening (style fit) score for a stock, ranked 1-100 at the global level, indicating how well its charac |
| 7 | `mdl238_region_rank_d1` | MATRIX | 0.963 | 持仓与资金流 | 0 | — | — | — | UNTESTED | Rank (1–100) representing the likelihood of institutional ownership for the stock within its region according to the Sma |
| 8 | `mdl238_region_screening_rank_d1` | MATRIX | 0.963 | 宏观与行业 | 0 | — | — | — | UNTESTED | Peers-adjusted screening (style fit) score for a stock, ranked 1-100 within its region, indicating how well its characte |
| 9 | `regional_institutional_preference_rank_d1` | MATRIX | 0.963 | 持仓与资金流 | 0 | — | — | — | UNTESTED | Normalized (0-100) score of the stock's likelihood of institutional ownership within its region |
| 10 | `regional_screening_factor_alignment_rank_d1` | MATRIX | 0.963 | 持仓与资金流 | 0 | — | — | — | UNTESTED | Normalized (0-100) score of the stock’s style-fit (screening component) in its region, adjusted for peer ownership |
| 11 | `global_peer_investment_concentration_rank_d1` | MATRIX | 0.963 | 持仓与资金流 | 0 | — | — | — | UNTESTED | Normalized (0-100) peer ownership score for the stock at the global level |
| 12 | `mdl238_global_owner_rank_d1` | MATRIX | 0.963 | 价量与波动 | 0 | — | — | — | UNTESTED | Peer ownership score of the stock globally, ranked 1-100 where 100 indicates highest peer ownership and liquidity risk |
| 13 | `mdl238_region_owner_rank_d1` | MATRIX | 0.963 | 持仓与资金流 | 0 | — | — | — | UNTESTED | Peer ownership score of the stock within its region, ranked 1-100 where 100 indicates highest peer ownership and liquidi |
| 14 | `regional_peer_investment_concentration_rank_d1` | MATRIX | 0.963 | 持仓与资金流 | 0 | — | — | — | UNTESTED | Normalized (0-100) peer ownership score for the stock in its region |
| 15 | `mdl238_sector_rank_d1` | MATRIX | 0.961 | 持仓与资金流 | 0 | — | — | — | UNTESTED | Rank (1–100) representing the likelihood of institutional ownership for the stock within its sector according to the Sma |
| 16 | `sector_relative_investment_rank_d1` | MATRIX | 0.961 | 持仓与资金流 | 0 | — | — | — | UNTESTED | Normalized (0-100) score of the stock's likelihood of institutional ownership within its sector |
| 17 | `global_change_in_preference_rank_d1` | MATRIX | 0.961 | 价量与波动 | 0 | — | — | — | UNTESTED | Normalized (0-100) score of the recent change momentum for the stock globally |
| 18 | `mdl238_global_change_rank_d1` | MATRIX | 0.961 | 价量与波动 | 0 | — | — | — | UNTESTED | Rank (1–100) measuring recent changes or momentum in institutional ownership for the stock, globally |
| 19 | `mdl238_region_change_rank_d1` | MATRIX | 0.961 | 价量与波动 | 0 | — | — | — | UNTESTED | Rank (1-100) of recent changes or momentum in ownership signals for the stock within its region, reflecting directional |
| 20 | `regional_change_in_preference_rank_d1` | MATRIX | 0.961 | 价量与波动 | 0 | — | — | — | UNTESTED | Normalized (0-100) score of the recent change momentum for the stock in its region |
| 21 | `industry_relative_investment_rank_d1` | MATRIX | 0.956 | 持仓与资金流 | 0 | — | — | — | UNTESTED | Normalized (0-100) score of the stock's likelihood of institutional ownership within its industry |
| 22 | `mdl238_industry_rank_d1` | MATRIX | 0.956 | 持仓与资金流 | 0 | — | — | — | UNTESTED | Rank (1–100) representing the likelihood of institutional ownership for the stock within its industry according to the S |
| 23 | `country_relative_investment_rank` | MATRIX | 0.779 | 持仓与资金流 | 0 | — | — | — | UNTESTED | Normalized (0–100) float value for the stock’s Smart Holdings score within its country |
| 24 | `global_institutional_preference_rank` | MATRIX | 0.779 | 持仓与资金流 | 0 | — | — | — | UNTESTED | Normalized (0–100) float percentile rank of the stock’s Smart Holdings score globally. Higher value = higher likelihood |
| 25 | `global_screening_factor_alignment_rank` | MATRIX | 0.779 | 风险与质量 | 0 | — | — | — | UNTESTED | Normalized (0–100) float value indicating the stock's style-fit or screening component, globally, adjusted for peer char |
| 26 | `mdl238_country_rank` | MATRIX | 0.779 | 持仓与资金流 | 0 | — | — | — | UNTESTED | Country rank (1–100) of Smart Holdings score. Higher rank = higher likelihood of institutional ownership within that cou |
| 27 | `mdl238_global_rank` | MATRIX | 0.779 | 持仓与资金流 | 0 | — | — | — | UNTESTED | Global rank (1–100) of Smart Holdings model score. Higher ranks imply greater probability of global institutional owners |
| 28 | `mdl238_global_screening_rank` | MATRIX | 0.779 | 风险与质量 | 0 | — | — | — | UNTESTED | Global rank (1–100) of the stock’s style-fit or screening component, adjusted for peer characteristics. Higher values re |
| 29 | `mdl238_region_rank` | MATRIX | 0.779 | 持仓与资金流 | 0 | — | — | — | UNTESTED | Regional rank (1–100) of Smart Holdings score. Higher rank = higher likelihood of institutional ownership within the reg |
| 30 | `mdl238_region_screening_rank` | MATRIX | 0.779 | 宏观与行业 | 0 | — | — | — | UNTESTED | Regional rank (1–100) of the stock’s style-fit or screening component, peer-adjusted. Higher rank suggests stronger regi |
| 31 | `regional_institutional_preference_rank` | MATRIX | 0.779 | 持仓与资金流 | 0 | — | — | — | UNTESTED | Normalized (0–100) float value for the stock’s Smart Holdings score within its region |
| 32 | `regional_screening_factor_alignment_rank` | MATRIX | 0.779 | 宏观与行业 | 0 | — | — | — | UNTESTED | Normalized (0–100) float value indicating the stock's style-fit or screening component within the region, adjusted for p |
| 33 | `global_peer_investment_concentration_rank` | MATRIX | 0.779 | 风险与质量 | 0 | — | — | — | UNTESTED | Normalized (0–100) float value measuring global peer crowding/risk, where higher values indicate higher global instituti |
| 34 | `mdl238_global_owner_rank` | MATRIX | 0.779 | 持仓与资金流 | 0 | — | — | — | UNTESTED | Global rank (1–100) of peer crowding/capacity risk. 100 = highest global institutional ownership (most crowded), 1 = low |
| 35 | `mdl238_region_owner_rank` | MATRIX | 0.779 | 持仓与资金流 | 0 | — | — | — | UNTESTED | Regional rank (1–100) of peer crowding. 100 = highest regional institutional ownership (most crowded), 1 = lowest. Highl |
| 36 | `regional_peer_investment_concentration_rank` | MATRIX | 0.779 | 持仓与资金流 | 0 | — | — | — | UNTESTED | Normalized (0–100) float value measuring regional peer crowding. High values mean higher institutional ownership regiona |
| 37 | `global_change_in_preference_rank` | MATRIX | 0.779 | 价量与波动 | 0 | — | — | — | UNTESTED | Normalized (float, 0–100) global rank of the Change Component, representing recent changes (momentum) in ownership signa |
| 38 | `mdl238_global_change_rank` | MATRIX | 0.779 | 价量与波动 | 0 | — | — | — | UNTESTED | Global rank (1–100) for the momentum or recent change component, representing the degree of recent increase in instituti |
| 39 | `mdl238_region_change_rank` | MATRIX | 0.779 | 价量与波动 | 0 | — | — | — | UNTESTED | Regional rank (1–100) indicating the strength of recent change or momentum in institutional ownership within the region |
| 40 | `regional_change_in_preference_rank` | MATRIX | 0.779 | 价量与波动 | 0 | — | — | — | UNTESTED | Normalized (float, 0–100) regional rank of the Change Component, representing momentum in institutional ownership signal |
| 41 | `mdl238_sector_rank` | MATRIX | 0.778 | 持仓与资金流 | 0 | — | — | — | UNTESTED | Sector rank (1–100) of Smart Holdings score. Higher values represent higher expected institutional ownership in that sec |
| 42 | `sector_relative_investment_rank` | MATRIX | 0.778 | 持仓与资金流 | 0 | — | — | — | UNTESTED | Normalized (0–100) float value reflecting the stock’s Smart Holdings score within its sector |
| 43 | `industry_relative_investment_rank` | MATRIX | 0.774 | 持仓与资金流 | 0 | — | — | — | UNTESTED | Normalized (0–100) float value representing the stock’s Smart Holdings score within its industry |
| 44 | `mdl238_industry_rank` | MATRIX | 0.774 | 持仓与资金流 | 0 | — | — | — | UNTESTED | Industry rank (1–100) of Smart Holdings score. Higher rank means higher probability of institutional ownership within th |

## 六、本地回测证据

本地库无该数据集的回测记录。

> 说明：`backtest_results` 只收录已持久化的波次（当前 EUR 共 1157 行）；本次会话的直接派发未写库，故此处为空**不代表未做尽**，实测结论见配套战役档案。

## 七、判死记录（sealed dead_end）

- `EUR-M238-D1-RANK-COMBO-PROD`（2026-08-24）family=model238 d1 rank combos of screening/change/industry/country：{"dataset": "model238", "example_id": "1YwozLvz", "expr_pattern": "rank mixes of mdl238_*_d1 screening/change/industry/country", "fitness": 0.85, "prod_corr": 0.896, "reason": "Intra-dataset d1 rank combos do not beat wave26 single-field rank(mdl238_global_screening_rank) S1.32 F0.87. Best 1YwozLvz S1.28 F0.85 2Y1.48 prod 0.896; lej73Xm7 S1.16 prod 0.8851; mutual 0.96. LOW_SUB 0.35-0.42 persists. 
- `EUR-MH-ESTREV-RESID-INVERT-CROWD`（2026-08-24）family=multi_horizon long_term estimate_revision industry residual full invert：{"dataset": "multi_horizon_alpha", "example_id": "1YwozEAW", "expr_pattern": "rank(subtract(long_term_estimate_revision_europe_rank, group_mean(..., industry))) and its full invert as dominant", "fitness": -0.99, "mutual_vs_m238": -0.74, "prod_corr": 0.7748, "prod_min": -0.9477, "reason": "Has independent IS (/S/1.48, self vs Wj71Q12o 0.17) but the profitable invert aligns with model238 institutio
- `EUR-M238-UNCROWDED-ALIGN-INDREL-PROD`（2026-08-24）family=model238 uncrowded alignment / industry_relative / preference：{"dataset": "model238", "example_id": "9qX9pVKe", "expr_pattern": "rank(alignment_d1 / industry_relative / preference) and mixes", "fitness": 0.9, "prod_corr": 0.8787, "reason": "Uncrowded m238 fields have IS but do NOT beat the change/screening prod ~0.89 wall. 9qX9pVKe industry_relative S1.34 F0.90 2Y1.59 prod=0.8787; ZY7jE0qd alignment S1.24 prod=0.8923; E5lqGwR9 three-way S1.22 prod=0.8889; LO

