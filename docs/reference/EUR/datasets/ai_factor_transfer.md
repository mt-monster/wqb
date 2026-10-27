# ai_factor_transfer — EUR 字段画像

> 自动生成于 2026-10-20 17:55　|　[← 返回索引](README.md)

## 一、数据集元信息

| 项 | 值 |
|---|---|
| 数据集 ID | `ai_factor_transfer` |
| 名称 | AI Enhanced Equity Factor Transfer |
| 类别 | MODEL |
| 数据字段数(平台) | 20 |
| 覆盖率 | 1.0 |
| 平台已有 alpha | 27 |
| valueScore | 2.0 |
| 金字塔倍率 | 1.3 |
| 数据类型 | MATRIX |
| delay | 1 |
| 状态 | scanned |

## 二、数据集描述（平台原文）

> ⚠️ 平台目录描述存在**错配**（已实测：insiders1 / imbalance5 的描述指向无关数据集）。以「五、全字段明细」的真实字段语义为准。

This dataset leverages advanced AI techniques to extract and transfer high-level equity factor features from a sophisticated quantitative research framework to other datasets. It includes a rich set of features such as price momentum, money flow strength, volume anomalies, liquidity alignment, and technical indicators like Bollinger Bands and Williams %R. Each feature is semantically defined and generated through AI-driven processes, ensuring clarity and consistency. By capturing nuanced interactions between price, volume, and liquidity, the dataset provides actionable signals for predicting price movements and constructing robust quantitative models. Its transfer learning approach enables the application of proven factor knowledge across diverse datasets, enhancing the predictive power an

## 三、字段画像汇总

| 维度 | 结果 |
|---|---|
| 字段总数 | **20** |
| 类型分布 | MATRIX×20 |
| 平均覆盖率 | **1.000** |
| 覆盖率区间 | 1.00 ~ 1.00 |
| 更新频率（推断） | 快照（按库表更新，需实测） |
| 可用性评级 | 优（覆盖 ≥90%，可直接做尽） |

**覆盖率分档**

| 档 | 字段数 | 占比 |
|---|---:|---:|
| 高 (≥0.90) | 20 | 100.0% |
| 中 (0.70–0.90) | 0 | 0.0% |
| 低 (0.50–0.70) | 0 | 0.0% |
| 稀疏 (<0.50) | 0 | 0.0% |

**历史实测分布（field_profile_perf）**

| 判定 | 字段数 | 占比 |
|---|---:|---:|
| UNTESTED | 20 | 100.0% |

- 该数据集全部字段**尚未实测**（UNTESTED）⇒ 优先做尽

## 四、语义维度地图（自动归类）

| 语义族 | 字段数 | 平均覆盖 | 代表字段 |
|---|---:|---:|---|
| 价量与波动 | 20 | 1.00 | balanced_price_oscillator、balanced_price_oscillator_2、cumulative_money_flow_volume_adjusted |

## 五、全字段明细

> 按 `best_sharpe` 降序（未测者置后）。`判定` 来自 `field_profile_perf`：ALIVE=历史测出过 S≥闸线（**不代表可提交**）；UNTESTED=未测；UNUSABLE/DEAD/AXIS_ONLY=已证否或仅可作轴。

| # | 字段名 | 类型 | 覆盖 | 语义族 | 测次 | best_S | best_2Y | best_sub | 判定 | 描述 |
|---:|---|---|---:|---|---:|---:|---:|---:|---|---|
| 1 | `balanced_price_oscillator` | MATRIX | 1.000 | 价量与波动 | 0 | — | — | — | UNTESTED | Price-Volume Ratio |
| 2 | `balanced_price_oscillator_2` | MATRIX | 1.000 | 价量与波动 | 0 | — | — | — | UNTESTED | Compares short-term and long-term price trends to measure their balance. |
| 3 | `cumulative_money_flow_volume_adjusted` | MATRIX | 1.000 | 价量与波动 | 0 | — | — | — | UNTESTED | Relative Strength (RSI) |
| 4 | `cumulative_money_flow_volume_adjusted_2` | MATRIX | 1.000 | 价量与波动 | 0 | — | — | — | UNTESTED | Logarithmic Price Transform |
| 5 | `liquidity_money_flow_alignment` | MATRIX | 1.000 | 价量与波动 | 0 | — | — | — | UNTESTED | Relative Turnover (RTN63D) |
| 6 | `liquidity_money_flow_alignment_2` | MATRIX | 1.000 | 价量与波动 | 0 | — | — | — | UNTESTED | Indicates whether liquidity and money flow are moving together. |
| 7 | `liquidity_weighted_returns_ma` | MATRIX | 1.000 | 价量与波动 | 0 | — | — | — | UNTESTED | 13-week price change |
| 8 | `liquidity_weighted_returns_ma_2` | MATRIX | 1.000 | 价量与波动 | 0 | — | — | — | UNTESTED | Commodity Channel Index (CCI) |
| 9 | `momentum_williams_r_adjusted` | MATRIX | 1.000 | 价量与波动 | 0 | — | — | — | UNTESTED | Return momentum |
| 10 | `momentum_williams_r_adjusted_2` | MATRIX | 1.000 | 价量与波动 | 0 | — | — | — | UNTESTED | Price momentum (from ABN_VOLM) |
| 11 | `money_flow_strength_typical_price` | MATRIX | 1.000 | 价量与波动 | 0 | — | — | — | UNTESTED | Assesses the relative strength of money flow adjusted for typical price levels. |
| 12 | `money_flow_strength_typical_price_2` | MATRIX | 1.000 | 价量与波动 | 0 | — | — | — | UNTESTED | ADL trend component |
| 13 | `short_term_price_change` | MATRIX | 1.000 | 价量与波动 | 0 | — | — | — | UNTESTED | Williams %R |
| 14 | `short_term_price_change_2` | MATRIX | 1.000 | 价量与波动 | 0 | — | — | — | UNTESTED | Chaikin Money Flow (CMF) |
| 15 | `typical_price_bollinger_band_position` | MATRIX | 1.000 | 价量与波动 | 0 | — | — | — | UNTESTED | Shows the position of the typical price within Bollinger Bands. |
| 16 | `typical_price_bollinger_band_position_2` | MATRIX | 1.000 | 价量与波动 | 0 | — | — | — | UNTESTED | Price Volume Oscillator (PVO) |
| 17 | `volume_anomaly_price_positioning` | MATRIX | 1.000 | 价量与波动 | 0 | — | — | — | UNTESTED | Examines the relationship between unusual trading volume events and the current price level. |
| 18 | `volume_anomaly_price_positioning_2` | MATRIX | 1.000 | 价量与波动 | 0 | — | — | — | UNTESTED | Detrended Price Oscillator (DPO) |
| 19 | `volume_trend_money_flow_interaction` | MATRIX | 1.000 | 价量与波动 | 0 | — | — | — | UNTESTED | Analyzes how volume trends interact with money flow dynamics. |
| 20 | `volume_trend_money_flow_interaction_2` | MATRIX | 1.000 | 价量与波动 | 0 | — | — | — | UNTESTED | Bollinger Band (BB) indicator |

## 六、本地回测证据

本地库无该数据集的回测记录。

> 说明：`backtest_results` 只收录已持久化的波次（当前 EUR 共 1157 行）；本次会话的直接派发未写库，故此处为空**不代表未做尽**，实测结论见配套战役档案。

## 七、判死记录（sealed dead_end）

- `EUR-STAR-RELVAL-EVEBITDA-2Y-DEAD`（2026-08-25）family=starmine RelVal EV/EBITDA ts_delta × v_rev/wedge：{"dataset": "predictive_starmine", "id": "EUR-STAR-RELVAL-EVEBITDA-2Y-DEAD", "reason": "Wave68 naked rank(ts_delta(rel_val_ev_ebitda_component_score_3,5)) S1.09 2Y=0.10. Wave69 win mix mLj81962 S1.34 F0.77 TVR9.6% prod 0.645 OK but 2Y=0.02 IS_LADDER. Year-regime accident. self 0.64 vs 78jdv6b1.", "rule": "Leave RelVal EV/EBITDA ts_delta family. Do not deepen v_rev/wedge on this slow. Do not clone 
- `EUR-AFT-OSC2-WEAK`（2026-08-25）family=ai_factor_transfer _2 oscillators/money-flow：{"dataset": "ai_factor_transfer", "id": "EUR-AFT-OSC2-WEAK", "reason": "Wave70 56 exprs on unused _2 fields (anomaly/DPO/liq_2/PVO/ADL/CCI/BPO_2). Max S0.58 F0.16. Wave18 already killed base oscillators. Do not mix PV.", "rule": "Leave ai_factor_transfer. Next unused whitelist: global_seasonal_model non-return seasonal features. Do not deepen RelVal EV/EBITDA or v_rev/wedge.", "salvage": "none", "

