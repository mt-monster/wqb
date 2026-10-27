# model135 — EUR 字段画像

> 自动生成于 2026-10-20 17:55　|　[← 返回索引](README.md)

## 一、数据集元信息

| 项 | 值 |
|---|---|
| 数据集 ID | `model135` |
| 名称 | Alternative technical factor models |
| 类别 | MODEL |
| 数据字段数(平台) | 137 |
| 覆盖率 | 0.5525 |
| 平台已有 alpha | 179 |
| valueScore | 3.0 |
| 金字塔倍率 | 1.3 |
| 数据类型 | — |
| delay | 1 |
| 状态 | — |

## 二、数据集描述（平台原文）

> ⚠️ 平台目录描述存在**错配**（已实测：insiders1 / imbalance5 的描述指向无关数据集）。以「五、全字段明细」的真实字段语义为准。

This dataset provides a comprehensive mapping between Bloomberg IDs (BBID) and Refinitiv Instrument Codes (RIC), enabling seamless integration and cross-referencing of securities across major financial data platforms. By facilitating accurate instrument identification, it supports data normalization and aggregation from multiple sources, which is essential for building robust multi-source trading models, conducting security-level research, and ensuring consistency in price and volume analytics. While not directly predictive, this mapping is a foundational resource for linking datasets that can be used to forecast price movements and enhance quantitative research workflows.

## 三、字段画像汇总

| 维度 | 结果 |
|---|---|
| 字段总数 | **137** |
| 类型分布 | VECTOR×137 |
| 平均覆盖率 | **0.552** |
| 覆盖率区间 | 0.55 ~ 0.55 |
| 更新频率（推断） | 事件/逐笔型（VECTOR） |
| 可用性评级 | 中（覆盖 50–70%，截面偏窄） |

**覆盖率分档**

| 档 | 字段数 | 占比 |
|---|---:|---:|
| 高 (≥0.90) | 0 | 0.0% |
| 中 (0.70–0.90) | 0 | 0.0% |
| 低 (0.50–0.70) | 137 | 100.0% |
| 稀疏 (<0.50) | 0 | 0.0% |

**历史实测分布（field_profile_perf）**

| 判定 | 字段数 | 占比 |
|---|---:|---:|
| UNUSABLE | 137 | 100.0% |

- 无带 `n_tests>0` 的有效实测记录；但历史判定已存在（UNTESTED 0 / UNUSABLE 137 等）。⚠ 历史判定可能**过时**（如 analyst7 的旧判死已作废），做尽前须重跑。

## 四、语义维度地图（自动归类）

| 语义族 | 字段数 | 平均覆盖 | 代表字段 |
|---|---:|---:|---|
| 价量与波动 | 103 | 0.55 | mdl135_d01_fmc、mdl135_d01_icc、mdl135_d01_if |
| 其他 | 21 | 0.55 | mdl135_d01_os、mdl135_d01_xda、mdl135_d02_os |
| 风险与质量 | 7 | 0.55 | mdl135_d01_bb、mdl135_d04_isr、mdl135_d3_isr |
| 持仓与资金流 | 4 | 0.55 | mdl135_d02_bb、mdl135_d04_bb、mdl135_d5_bb |
| 搜索与替代数据 | 1 | 0.55 | mdl135_d3_isrs |
| 宏观与行业 | 1 | 0.55 | mdl135_gsubind |

## 五、全字段明细

> 按 `best_sharpe` 降序（未测者置后）。`判定` 来自 `field_profile_perf`：ALIVE=历史测出过 S≥闸线（**不代表可提交**）；UNTESTED=未测；UNUSABLE/DEAD/AXIS_ONLY=已证否或仅可作轴。

| # | 字段名 | 类型 | 覆盖 | 语义族 | 测次 | best_S | best_2Y | best_sub | 判定 | 描述 |
|---:|---|---|---:|---|---:|---:|---:|---:|---|---|
| 1 | `mdl135_d01_bb` | VECTOR | 0.552 | 风险与质量 | 0 | — | — | — | UNUSABLE | Bollinger Bands indicator calculated with a 10-day lookback; likely refers to the band width, z-score, or similar normalized measure derived |
| 2 | `mdl135_d01_fmc` | VECTOR | 0.552 | 价量与波动 | 0 | — | — | — | UNUSABLE | Chaikin Money Flow over 10 days; assesses buying/selling pressure by combining price and volume (typically between -1 and +1) |
| 3 | `mdl135_d01_icc` | VECTOR | 0.552 | 价量与波动 | 0 | — | — | — | UNUSABLE | Commodity Channel Index over 10 days; oscillator of price deviation from its mean to identify cyclical trends, normalized |
| 4 | `mdl135_d01_if` | VECTOR | 0.552 | 价量与波动 | 0 | — | — | — | UNUSABLE | Force Index over 10 days; volume-weighted price movement indicator reflecting the strength of moves |
| 5 | `mdl135_d01_ifm` | VECTOR | 0.552 | 价量与波动 | 0 | — | — | — | UNUSABLE | Money Flow Index calculated over a 10-day window; a volume-weighted oscillator that measures buying and selling pressure |
| 6 | `mdl135_d01_isr` | VECTOR | 0.552 | 价量与波动 | 0 | — | — | — | UNUSABLE | Relative Strength Index computed over a 10-day period, a momentum indicator measuring speed and change of price movements (normalized) |
| 7 | `mdl135_d01_isrs` | VECTOR | 0.552 | 价量与波动 | 0 | — | — | — | UNUSABLE | Stochastic Relative Strength Index calculated over a 10-day window; a momentum oscillator applying stochastic calculations to RSI values, us |
| 8 | `mdl135_d01_iv` | VECTOR | 0.552 | 价量与波动 | 0 | — | — | — | UNUSABLE | Vortex Indicator over 10 days; trend and reversal strength indicator (typically includes +VI and -VI components) |
| 9 | `mdl135_d01_ivn` | VECTOR | 0.552 | 价量与波动 | 0 | — | — | — | UNUSABLE | Negative Volume Index computed over a 10-day period, measuring price trends associated with declining trading volumes |
| 10 | `mdl135_d01_lda` | VECTOR | 0.552 | 价量与波动 | 0 | — | — | — | UNUSABLE | Accumulation/Distribution Line over 10 trading days, integrating price and volume to track money flow |
| 11 | `mdl135_d01_oa` | VECTOR | 0.552 | 价量与波动 | 0 | — | — | — | UNUSABLE | Awesome Oscillator over 10 days; momentum indicator based on the difference between two moving averages of the midpoint price, normalized |
| 12 | `mdl135_d01_os` | VECTOR | 0.552 | 其他 | 0 | — | — | — | UNUSABLE | Stochastic Oscillator over 10 days; compares close to the 10-day high–low range, typically normalized 0–100 |
| 13 | `mdl135_d01_rta` | VECTOR | 0.552 | 价量与波动 | 0 | — | — | — | UNUSABLE | 10-day Average True Range, a normalized measure of volatility based on recent high, low, and closing prices over the past 10 days |
| 14 | `mdl135_d01_tpv` | VECTOR | 0.552 | 价量与波动 | 0 | — | — | — | UNUSABLE | Volume Price Trend indicator computed over a 10-day window; measures cumulative volume adjusted by the direction and magnitude of price chan |
| 15 | `mdl135_d01_vbo` | VECTOR | 0.552 | 价量与波动 | 0 | — | — | — | UNUSABLE | On-Balance Volume over 10 trading days; cumulative volume flow to gauge accumulation or distribution |
| 16 | `mdl135_d01_vme` | VECTOR | 0.552 | 价量与波动 | 0 | — | — | — | UNUSABLE | Ease of Movement over 10 days; relates price change to volume to gauge price-volume efficiency |
| 17 | `mdl135_d01_xda` | VECTOR | 0.552 | 其他 | 0 | — | — | — | UNUSABLE | 10-day Average Directional Movement Index, a normalized technical indicator that measures trend strength over a 10-day period |
| 18 | `mdl135_d01ntr` | VECTOR | 0.552 | 价量与波动 | 0 | — | — | — | UNUSABLE | Trailing 10-day return for the security, as defined by the provider (simple or log), aligned to PIT discipline |
| 19 | `mdl135_d02_bb` | VECTOR | 0.552 | 持仓与资金流 | 0 | — | — | — | UNUSABLE | Bollinger Bands statistics over 20 days, such as band width or relative position within the bands |
| 20 | `mdl135_d02_fmc` | VECTOR | 0.552 | 价量与波动 | 0 | — | — | — | UNUSABLE | Chaikin Money Flow over 20 days; price-volume measure of buying/selling pressure |
| 21 | `mdl135_d02_icc` | VECTOR | 0.552 | 价量与波动 | 0 | — | — | — | UNUSABLE | Commodity Channel Index over 20 days; oscillator of price deviation from its mean to identify cyclical trends, normalized |
| 22 | `mdl135_d02_if` | VECTOR | 0.552 | 价量与波动 | 0 | — | — | — | UNUSABLE | Force Index technical indicator calculated over a 20-day period, reflecting price and volume-based momentum |
| 23 | `mdl135_d02_ifm` | VECTOR | 0.552 | 价量与波动 | 0 | — | — | — | UNUSABLE | Money Flow Index calculated over a 20-day window; a volume-weighted oscillator that measures buying and selling pressure |
| 24 | `mdl135_d02_isr` | VECTOR | 0.552 | 价量与波动 | 0 | — | — | — | UNUSABLE | 20-day Relative Strength Index, a normalized momentum indicator measuring the speed of price changes |
| 25 | `mdl135_d02_isrs` | VECTOR | 0.552 | 价量与波动 | 0 | — | — | — | UNUSABLE | Stochastic RSI (Stochastic Relative Strength Index) calculated over 20 days, measuring momentum by applying the stochastic formula to RSI va |
| 26 | `mdl135_d02_iv` | VECTOR | 0.552 | 价量与波动 | 0 | — | — | — | UNUSABLE | Vortex Indicator over 20 days; trend-following measure based on upward and downward price movement |
| 27 | `mdl135_d02_ivn` | VECTOR | 0.552 | 价量与波动 | 0 | — | — | — | UNUSABLE | Negative Volume Index computed over a 20-day period, emphasizing price trends on days of decreasing volume |
| 28 | `mdl135_d02_lda` | VECTOR | 0.552 | 价量与波动 | 0 | — | — | — | UNUSABLE | Accumulation/Distribution Line over 20 trading days, measuring cumulative money flow volume based on price and volume |
| 29 | `mdl135_d02_oa` | VECTOR | 0.552 | 价量与波动 | 0 | — | — | — | UNUSABLE | Awesome Oscillator over 20 days; momentum indicator based on the difference between two moving averages of the midpoint price, normalized |
| 30 | `mdl135_d02_os` | VECTOR | 0.552 | 其他 | 0 | — | — | — | UNUSABLE | Stochastic Oscillator over 20 days; compares close to the 20-day high–low range, typically normalized 0–100 |
| 31 | `mdl135_d02_rta` | VECTOR | 0.552 | 价量与波动 | 0 | — | — | — | UNUSABLE | 20-day Average True Range, a normalized measure of volatility based on recent high, low, and closing prices over the past 20 days |
| 32 | `mdl135_d02_tpv` | VECTOR | 0.552 | 价量与波动 | 0 | — | — | — | UNUSABLE | Volume Price Trend indicator computed over a 20-day window; measures cumulative volume adjusted by the direction and magnitude of price chan |
| 33 | `mdl135_d02_vbo` | VECTOR | 0.552 | 价量与波动 | 0 | — | — | — | UNUSABLE | 20-day On-Balance Volume, a cumulative indicator that adds or subtracts volume based on price moves to measure buying and selling pressure o |
| 34 | `mdl135_d02_vme` | VECTOR | 0.552 | 价量与波动 | 0 | — | — | — | UNUSABLE | Ease of Movement technical indicator calculated over a 20-day period, measuring the relationship between price change and volume |
| 35 | `mdl135_d02_xda` | VECTOR | 0.552 | 其他 | 0 | — | — | — | UNUSABLE | 20-day Average Directional Movement Index, a normalized technical indicator that measures trend strength over a 20-day period |
| 36 | `mdl135_d02ntr` | VECTOR | 0.552 | 价量与波动 | 0 | — | — | — | UNUSABLE | Trailing 20-trading-day return of the security (provider convention typically simple return), computed point-in-time with D1 delay |
| 37 | `mdl135_d04_bb` | VECTOR | 0.552 | 持仓与资金流 | 0 | — | — | — | UNUSABLE | Bollinger Bands-derived measure over a 40-day lookback (e.g., %B or band width/position), z-score normalized |
| 38 | `mdl135_d04_fmc` | VECTOR | 0.552 | 价量与波动 | 0 | — | — | — | UNUSABLE | Chaikin Money Flow over 40 days, a volume-weighted measure of buying and selling pressure, z-score normalized |
| 39 | `mdl135_d04_icc` | VECTOR | 0.552 | 价量与波动 | 0 | — | — | — | UNUSABLE | Commodity Channel Index over 40 days; oscillator of price deviation from its mean to identify cyclical trends, normalized |
| 40 | `mdl135_d04_if` | VECTOR | 0.552 | 价量与波动 | 0 | — | — | — | UNUSABLE | Force Index technical indicator calculated over a 40-day period, gauging buying and selling pressure using price and volume |
| 41 | `mdl135_d04_ifm` | VECTOR | 0.552 | 价量与波动 | 0 | — | — | — | UNUSABLE | Money Flow Index calculated over a 40-day window; a volume-weighted oscillator that measures buying and selling pressure |
| 42 | `mdl135_d04_isr` | VECTOR | 0.552 | 风险与质量 | 0 | — | — | — | UNUSABLE | Relative Strength Index over a 40-day lookback, z-score normalized |
| 43 | `mdl135_d04_isrs` | VECTOR | 0.552 | 价量与波动 | 0 | — | — | — | UNUSABLE | Stochastic RSI over 40 days, fast momentum oscillator scaled 0–100 indicating overbought or oversold |
| 44 | `mdl135_d04_iv` | VECTOR | 0.552 | 价量与波动 | 0 | — | — | — | UNUSABLE | Vortex Indicator over 40 days; trend-following measure based on upward and downward price movement |
| 45 | `mdl135_d04_ivn` | VECTOR | 0.552 | 价量与波动 | 0 | — | — | — | UNUSABLE | Negative Volume Index over 40 trading days, emphasizing periods with declining volume |
| 46 | `mdl135_d04_lda` | VECTOR | 0.552 | 价量与波动 | 0 | — | — | — | UNUSABLE | Accumulation/Distribution Line over a 40-day window; cumulative money flow based on price and volume indicating buying/selling pressure over |
| 47 | `mdl135_d04_oa` | VECTOR | 0.552 | 价量与波动 | 0 | — | — | — | UNUSABLE | Awesome Oscillator over 40 days; momentum indicator based on the difference between two moving averages of the midpoint price, normalized |
| 48 | `mdl135_d04_os` | VECTOR | 0.552 | 其他 | 0 | — | — | — | UNUSABLE | Stochastic Oscillator over 40 days; compares close to the 40-day high–low range, typically normalized 0–100 |
| 49 | `mdl135_d04_rta` | VECTOR | 0.552 | 价量与波动 | 0 | — | — | — | UNUSABLE | Average True Range over 40 days, volatility measure in price units |
| 50 | `mdl135_d04_tpv` | VECTOR | 0.552 | 价量与波动 | 0 | — | — | — | UNUSABLE | Volume Price Trend indicator computed over a 40-day window; measures cumulative volume adjusted by the direction and magnitude of price chan |
| 51 | `mdl135_d04_vbo` | VECTOR | 0.552 | 价量与波动 | 0 | — | — | — | UNUSABLE | On-Balance Volume over 40 days; cumulative indicator reflecting volume flow |
| 52 | `mdl135_d04_vme` | VECTOR | 0.552 | 价量与波动 | 0 | — | — | — | UNUSABLE | Ease of Movement value for a 40-day window, measuring the ease with which price moves are made (combining volume and price change); larger v |
| 53 | `mdl135_d04_xda` | VECTOR | 0.552 | 其他 | 0 | — | — | — | UNUSABLE | 40-day Average Directional Movement Index, a normalized technical indicator that measures trend strength over a 40-day period |
| 54 | `mdl135_d04ntr` | VECTOR | 0.552 | 价量与波动 | 0 | — | — | — | UNUSABLE | 40-day return, trailing price return aligned to point-in-time discipline |
| 55 | `mdl135_d21_opd` | VECTOR | 0.552 | 价量与波动 | 0 | — | — | — | UNUSABLE | Detrended Price Oscillator over 12 days; filters long-term trend to isolate medium-term cycles |
| 56 | `mdl135_d2_im` | VECTOR | 0.552 | 价量与波动 | 0 | — | — | — | UNUSABLE | Mass Index over 2 days; uses the high–low range to identify potential trend reversals |
| 57 | `mdl135_d2_ist` | VECTOR | 0.552 | 价量与波动 | 0 | — | — | — | UNUSABLE | True Strength Index over 2 days; momentum measure using double-smoothed price changes |
| 58 | `mdl135_d2_oc` | VECTOR | 0.552 | 其他 | 0 | — | — | — | UNUSABLE | Composite coincident technical indicator representing aggregated signals over a 2-day recent window, proprietary calculation |
| 59 | `mdl135_d2_ou` | VECTOR | 0.552 | 价量与波动 | 0 | — | — | — | UNUSABLE | Ultimate Oscillator over 2 days, multi-timeframe momentum of buying pressure scaled 0–100 |
| 60 | `mdl135_d2_ovp` | VECTOR | 0.552 | 价量与波动 | 0 | — | — | — | UNUSABLE | Percentage Volume Oscillator with 2-day parameters; percent difference between short- and long-term volume EMAs indicating short-term volume |
| 61 | `mdl135_d3_bb` | VECTOR | 0.552 | 价量与波动 | 0 | — | — | — | UNUSABLE | Bollinger Bands value calculated over the past 3 trading days, reflecting price volatility and relative position within a 3-day moving avera |
| 62 | `mdl135_d3_fmc` | VECTOR | 0.552 | 价量与波动 | 0 | — | — | — | UNUSABLE | Chaikin Money Flow over 3 days, short-horizon money flow volume |
| 63 | `mdl135_d3_icc` | VECTOR | 0.552 | 价量与波动 | 0 | — | — | — | UNUSABLE | Commodity Channel Index over 3 days; oscillator of price deviation from its mean to identify cyclical trends, normalized |
| 64 | `mdl135_d3_if` | VECTOR | 0.552 | 价量与波动 | 0 | — | — | — | UNUSABLE | Force Index computed over a 3-day period, combining price change and volume to gauge short-term buying/selling pressure |
| 65 | `mdl135_d3_ifm` | VECTOR | 0.552 | 价量与波动 | 0 | — | — | — | UNUSABLE | Money Flow Index over a 3-day lookback, blending price and volume to indicate buying and selling pressure |
| 66 | `mdl135_d3_im` | VECTOR | 0.552 | 价量与波动 | 0 | — | — | — | UNUSABLE | Mass Index over 3 days; range-expansion volatility indicator for potential trend reversals |
| 67 | `mdl135_d3_isr` | VECTOR | 0.552 | 风险与质量 | 0 | — | — | — | UNUSABLE | Relative Strength Index over a 3-day lookback, z-score normalized |
| 68 | `mdl135_d3_isrs` | VECTOR | 0.552 | 搜索与替代数据 | 0 | — | — | — | UNUSABLE | 3-day Stochastic RSI, a normalized oscillator applying a stochastic transform to RSI values |
| 69 | `mdl135_d3_ist` | VECTOR | 0.552 | 价量与波动 | 0 | — | — | — | UNUSABLE | True Strength Index over 3 days; momentum measure using double-smoothed price changes |
| 70 | `mdl135_d3_iv` | VECTOR | 0.552 | 价量与波动 | 0 | — | — | — | UNUSABLE | Vortex Indicator over 3 days; trend-following measure based on upward and downward price movement |
| 71 | `mdl135_d3_ivn` | VECTOR | 0.552 | 价量与波动 | 0 | — | — | — | UNUSABLE | Z-score normalized Negative Volume Index calculated over a 3-day period, measuring price movement on lower-volume days |
| 72 | `mdl135_d3_lda` | VECTOR | 0.552 | 价量与波动 | 0 | — | — | — | UNUSABLE | 3-day Accumulation Distribution Line, measuring the cumulative flow of money into and out of a security using both price and volume over a 3 |
| 73 | `mdl135_d3_oa` | VECTOR | 0.552 | 价量与波动 | 0 | — | — | — | UNUSABLE | Awesome Oscillator over 3 days; momentum via the difference between short- and long-period moving averages of price |
| 74 | `mdl135_d3_oc` | VECTOR | 0.552 | 其他 | 0 | — | — | — | UNUSABLE | Composite coincident technical indicator representing aggregated signals over a 3-day recent window, proprietary calculation |
| 75 | `mdl135_d3_os` | VECTOR | 0.552 | 其他 | 0 | — | — | — | UNUSABLE | Stochastic Oscillator over 3 days; compares close to the 3-day high–low range, typically normalized 0–100 |
| 76 | `mdl135_d3_ou` | VECTOR | 0.552 | 价量与波动 | 0 | — | — | — | UNUSABLE | Ultimate Oscillator over 3 days; weighted blend of multiple timeframes’ buying pressure and volatility indicating short-term momentum |
| 77 | `mdl135_d3_ovp` | VECTOR | 0.552 | 价量与波动 | 0 | — | — | — | UNUSABLE | Percentage Volume Oscillator with 3-day parameters; percent difference between short- and long-term volume EMAs indicating short-term volume |
| 78 | `mdl135_d3_rta` | VECTOR | 0.552 | 价量与波动 | 0 | — | — | — | UNUSABLE | Average True Range over 3 days; short-term volatility measure based on true range |
| 79 | `mdl135_d3_tpv` | VECTOR | 0.552 | 价量与波动 | 0 | — | — | — | UNUSABLE | Volume Price Trend indicator calculated over 3 days, a cumulative price-volume trend measure |
| 80 | `mdl135_d3_vbo` | VECTOR | 0.552 | 价量与波动 | 0 | — | — | — | UNUSABLE | On-Balance Volume calculated using a 3-day lookback, measuring cumulative volume flow based on pricing direction to detect volume trends sup |
| 81 | `mdl135_d3_vme` | VECTOR | 0.552 | 价量与波动 | 0 | — | — | — | UNUSABLE | Ease of Movement over 3 days, relating price change to volume |
| 82 | `mdl135_d3_xda` | VECTOR | 0.552 | 风险与质量 | 0 | — | — | — | UNUSABLE | 3-day Average Directional Movement Index (trend strength indicator, calculated with 3-day lookback, z-score normalized) |
| 83 | `mdl135_d3ntr` | VECTOR | 0.552 | 价量与波动 | 0 | — | — | — | UNUSABLE | 3-day trailing return for the security, typically a simple return aligned with point-in-time discipline |
| 84 | `mdl135_d4_im` | VECTOR | 0.552 | 价量与波动 | 0 | — | — | — | UNUSABLE | Mass Index over 4 days; high–low range-based indicator to detect potential trend reversals |
| 85 | `mdl135_d4_oc` | VECTOR | 0.552 | 其他 | 0 | — | — | — | UNUSABLE | Composite coincident technical indicator representing aggregated signals over a 4-day recent window, proprietary calculation |
| 86 | `mdl135_d4_ovp` | VECTOR | 0.552 | 价量与波动 | 0 | — | — | — | UNUSABLE | Percentage Volume Oscillator with 4-day parameters; percent difference between short- and long-term volume EMAs, expressed as a percentage |
| 87 | `mdl135_d5_bb` | VECTOR | 0.552 | 持仓与资金流 | 0 | — | — | — | UNUSABLE | Bollinger Bands-derived measure over a 5-day lookback (e.g., %B or band width/position), z-score normalized |
| 88 | `mdl135_d5_fmc` | VECTOR | 0.552 | 价量与波动 | 0 | — | — | — | UNUSABLE | Chaikin Money Flow over 5 days, assesses buying and selling pressure from price and volume |
| 89 | `mdl135_d5_icc` | VECTOR | 0.552 | 价量与波动 | 0 | — | — | — | UNUSABLE | Commodity Channel Index over 5 days; oscillator of price deviation from its mean to identify cyclical trends, normalized |
| 90 | `mdl135_d5_if` | VECTOR | 0.552 | 价量与波动 | 0 | — | — | — | UNUSABLE | Force Index calculated over 5 days, combining price and volume to measure buying and selling pressure |
| 91 | `mdl135_d5_ifm` | VECTOR | 0.552 | 价量与波动 | 0 | — | — | — | UNUSABLE | Money Flow Index over 5 days, volume-weighted momentum oscillator indicating overbought or oversold conditions |
| 92 | `mdl135_d5_im` | VECTOR | 0.552 | 价量与波动 | 0 | — | — | — | UNUSABLE | Mass Index over 5 days, range-expansion indicator used to flag potential trend reversals |
| 93 | `mdl135_d5_isr` | VECTOR | 0.552 | 风险与质量 | 0 | — | — | — | UNUSABLE | Relative Strength Index over a 5-day lookback, z-score normalized |
| 94 | `mdl135_d5_isrs` | VECTOR | 0.552 | 价量与波动 | 0 | — | — | — | UNUSABLE | Stochastic RSI over 5 days, momentum oscillator indicating overbought or oversold states |
| 95 | `mdl135_d5_iv` | VECTOR | 0.552 | 价量与波动 | 0 | — | — | — | UNUSABLE | Vortex Indicator over 5 days; trend-following measure based on upward and downward price movement |
| 96 | `mdl135_d5_ivn` | VECTOR | 0.552 | 价量与波动 | 0 | — | — | — | UNUSABLE | Negative Volume Index over 5 trading days, emphasizing price moves on lower-volume days |
| 97 | `mdl135_d5_lda` | VECTOR | 0.552 | 持仓与资金流 | 0 | — | — | — | UNUSABLE | Accumulation/Distribution Line over 5 days; cumulative money flow measure of buying/selling pressure |
| 98 | `mdl135_d5_oa` | VECTOR | 0.552 | 价量与波动 | 0 | — | — | — | UNUSABLE | Awesome Oscillator over 5 days, measuring market momentum via SMA differences |
| 99 | `mdl135_d5_oc` | VECTOR | 0.552 | 其他 | 0 | — | — | — | UNUSABLE | Composite coincident technical indicator representing aggregated signals over a 5-day recent window, proprietary calculation |
| 100 | `mdl135_d5_os` | VECTOR | 0.552 | 其他 | 0 | — | — | — | UNUSABLE | Stochastic Oscillator over 5 days; compares close to the 5-day high–low range, typically normalized 0–100 |
| 101 | `mdl135_d5_ovp` | VECTOR | 0.552 | 价量与波动 | 0 | — | — | — | UNUSABLE | Percentage Volume Oscillator with 5-day parameters; percent difference between short- and long-term volume EMAs, expressed as a percentage |
| 102 | `mdl135_d5_rta` | VECTOR | 0.552 | 价量与波动 | 0 | — | — | — | UNUSABLE | 5-day Average True Range, a normalized measure of volatility based on recent high, low, and closing prices over the past 5 days |
| 103 | `mdl135_d5_tpv` | VECTOR | 0.552 | 价量与波动 | 0 | — | — | — | UNUSABLE | Volume Price Trend over 5 days, combining price trend and volume to indicate direction and strength of moves |
| 104 | `mdl135_d5_vbo` | VECTOR | 0.552 | 价量与波动 | 0 | — | — | — | UNUSABLE | On-Balance Volume over 5 days; cumulative volume-based indicator |
| 105 | `mdl135_d5_vme` | VECTOR | 0.552 | 价量与波动 | 0 | — | — | — | UNUSABLE | Ease of Movement over 5 days, relating price change to volume to gauge price-volume ease |
| 106 | `mdl135_d5_xda` | VECTOR | 0.552 | 其他 | 0 | — | — | — | UNUSABLE | 5-day Average Directional Movement Index, a normalized technical indicator that measures trend strength over a 5-day period |
| 107 | `mdl135_d5ntr` | VECTOR | 0.552 | 价量与波动 | 0 | — | — | — | UNUSABLE | 5-day return, trailing price return aligned to point-in-time discipline |
| 108 | `mdl135_d62_opd` | VECTOR | 0.552 | 价量与波动 | 0 | — | — | — | UNUSABLE | Detrended Price Oscillator over a 26-day period, identifying cycles by removing longer-term price trends |
| 109 | `mdl135_d63_opd` | VECTOR | 0.552 | 价量与波动 | 0 | — | — | — | UNUSABLE | Detrended Price Oscillator over 36 days; removes long-term trend to highlight cyclical deviations |
| 110 | `mdl135_d6_oc` | VECTOR | 0.552 | 其他 | 0 | — | — | — | UNUSABLE | Composite coincident technical indicator representing aggregated signals over a 6-day recent window, proprietary calculation |
| 111 | `mdl135_d6_ovp` | VECTOR | 0.552 | 价量与波动 | 0 | — | — | — | UNUSABLE | Percentage Volume Oscillator with 6-day parameters; percent difference between short- and long-term volume EMAs, expressed as a percentage |
| 112 | `mdl135_d7_oc` | VECTOR | 0.552 | 其他 | 0 | — | — | — | UNUSABLE | Coincident indicators for 7 day |
| 113 | `mdl135_d81_opd` | VECTOR | 0.552 | 价量与波动 | 0 | — | — | — | UNUSABLE | Detrended Price Oscillator value computed using an 18-day lookback period, measuring short-term price cycles with the long-term trend remove |
| 114 | `mdl135_d8_oc` | VECTOR | 0.552 | 其他 | 0 | — | — | — | UNUSABLE | Coincident indicators for 8 day |
| 115 | `mdl135_d8_opd` | VECTOR | 0.552 | 价量与波动 | 0 | — | — | — | UNUSABLE | Detrended Price Oscillator calculated over an 8-day window, an oscillator removing long-term trends to identify short-term price cycles and  |
| 116 | `mdl135_gsubind` | VECTOR | 0.552 | 宏观与行业 | 0 | — | — | — | UNUSABLE | Numeric subindustry identifier (float) from vendor taxonomy without a codebook |
| 117 | `mdl135_im` | VECTOR | 0.552 | 价量与波动 | 0 | — | — | — | UNUSABLE | Z-score normalized Mass Index calculated over a 1-day period, identifying potential trend reversals by analyzing range expansion |
| 118 | `mdl135_ist` | VECTOR | 0.552 | 价量与波动 | 0 | — | — | — | UNUSABLE | True Strength Index over 1 day; momentum measure using double-smoothed price changes |
| 119 | `mdl135_macd_1d` | VECTOR | 0.552 | 价量与波动 | 0 | — | — | — | UNUSABLE | 1-day Moving Average Convergence Divergence (MACD calculated with 1-day moving averages or shortest parameters, measures rapid price momentu |
| 120 | `mdl135_macd_2d` | VECTOR | 0.552 | 价量与波动 | 0 | — | — | — | UNUSABLE | Moving Average Convergence Divergence computed with very short-term 2-day parameterization, indicating momentum and trend |
| 121 | `mdl135_macd_3d` | VECTOR | 0.552 | 价量与波动 | 0 | — | — | — | UNUSABLE | Moving Average Convergence Divergence indicator calculated with a 3-day window, representing short-term price momentum shifts |
| 122 | `mdl135_macd_4d` | VECTOR | 0.552 | 价量与波动 | 0 | — | — | — | UNUSABLE | 4-day Moving Average Convergence Divergence (difference between short- and long-term moving averages for price, calculated with 4-day parame |
| 123 | `mdl135_mktcap` | VECTOR | 0.552 | 其他 | 0 | — | — | — | UNUSABLE | Market capitalization of the company, likely in millions of USD, not normalized |
| 124 | `mdl135_oc` | VECTOR | 0.552 | 其他 | 0 | — | — | — | UNUSABLE | Composite coincident technical indicator representing aggregated signals for the most recent day, proprietary calculation |
| 125 | `mdl135_ou` | VECTOR | 0.552 | 价量与波动 | 0 | — | — | — | UNUSABLE | Ultimate Oscillator value calculated for a 1-day period, integrating multi-timeframe momentum |
| 126 | `mdl135_ovp` | VECTOR | 0.552 | 价量与波动 | 0 | — | — | — | UNUSABLE | Percentage Volume Oscillator with 1-day parameters; percent difference between short- and long-term volume EMAs indicating short-term volume |
| 127 | `mdl135_vlc` | VECTOR | 0.552 | 价量与波动 | 0 | — | — | — | UNUSABLE | Close Location Value: a normalized measure indicating the position of the closing price within the day’s price range (e.g., between low and  |
| 128 | `mdl135_willimsr_10d` | VECTOR | 0.552 | 其他 | 0 | — | — | — | UNUSABLE | Williams %R (Percent Range) technical indicator, using a 10-day lookback window, normalized |
| 129 | `mdl135_willimsr_20d` | VECTOR | 0.552 | 风险与质量 | 0 | — | — | — | UNUSABLE | Williams Percent Range over a 20-day lookback, z-score normalized |
| 130 | `mdl135_willimsr_3d` | VECTOR | 0.552 | 其他 | 0 | — | — | — | UNUSABLE | Williams %R (Percent Range) technical indicator calculated using a 3-day lookback window, normalized |
| 131 | `mdl135_willimsr_40d` | VECTOR | 0.552 | 风险与质量 | 0 | — | — | — | UNUSABLE | Williams Percent Range over a 40-day lookback, z-score normalized |
| 132 | `mdl135_willimsr_5d` | VECTOR | 0.552 | 其他 | 0 | — | — | — | UNUSABLE | Williams %R (Percent Range) technical indicator, using a 5-day lookback window, normalized |
| 133 | `triple_ema_rate_change_10d` | VECTOR | 0.552 | 价量与波动 | 0 | — | — | — | UNUSABLE | TRIX (Triple Exponential Average) oscillator computed with a 10-day window, a momentum indicator based on triple-smoothed EMA to reduce nois |
| 134 | `triple_ema_rate_change_20d` | VECTOR | 0.552 | 价量与波动 | 0 | — | — | — | UNUSABLE | TRIX (Triple Exponential Average Oscillator) over a 20-day period; momentum indicator highlighting turning points |
| 135 | `triple_ema_rate_change_3d` | VECTOR | 0.552 | 价量与波动 | 0 | — | — | — | UNUSABLE | TRIX over 3 days; triple exponentially smoothed price oscillator capturing short-term momentum and filtering noise |
| 136 | `triple_ema_rate_change_40d` | VECTOR | 0.552 | 价量与波动 | 0 | — | — | — | UNUSABLE | TRIX over 40 days; triple-smoothed momentum oscillator based on the rate of change of a triple EMA |
| 137 | `triple_ema_rate_change_5d` | VECTOR | 0.552 | 价量与波动 | 0 | — | — | — | UNUSABLE | TRIX momentum oscillator over 5 days, rate of change of a triple-smoothed EMA |

## 六、本地回测证据

本地库无该数据集的回测记录。

> 说明：`backtest_results` 只收录已持久化的波次（当前 EUR 共 1157 行）；本次会话的直接派发未写库，故此处为空**不代表未做尽**，实测结论见配套战役档案。

## 七、判死记录（sealed dead_end）

无针对本数据集的 `dead_end` 记录。

