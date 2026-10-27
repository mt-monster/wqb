# socialmedia15 — EUR 字段画像

> 自动生成于 2026-10-20 17:55　|　[← 返回索引](README.md)

## 一、数据集元信息

| 项 | 值 |
|---|---|
| 数据集 ID | `socialmedia15` |
| 名称 | Sentiment Indicators |
| 类别 | SOCIALMEDIA |
| 数据字段数(平台) | 45 |
| 覆盖率 | 0.3424 |
| 平台已有 alpha | 125 |
| valueScore | 2.0 |
| 金字塔倍率 | 1.1 |
| 数据类型 | — |
| delay | 1 |
| 状态 | — |

## 二、数据集描述（平台原文）

> ⚠️ 平台目录描述存在**错配**（已实测：insiders1 / imbalance5 的描述指向无关数据集）。以「五、全字段明细」的真实字段语义为准。

This dataset provides real-time sentiment indicators for a wide range of financial assets, including individual companies, company groups, currencies, commodities, and countries. It leverages advanced natural language processing to analyze news and social media content, generating minutely and daily scores for various behavioral and thematic factors such as sentiment, optimism, fear, trust, volatility, and more. The dataset includes both the volume of media coverage ("buzz") and a rich set of sentiment and event-based metrics, enabling users to track shifts in market mood and behavioral signals. These indicators can be used to enhance quantitative models, inform trading strategies, and anticipate price movements by capturing the collective psychology and reactions of market participants in

## 三、字段画像汇总

| 维度 | 结果 |
|---|---|
| 字段总数 | **45** |
| 类型分布 | VECTOR×45 |
| 平均覆盖率 | **0.342** |
| 覆盖率区间 | 0.26 ~ 0.37 |
| 更新频率（推断） | 事件/逐笔型（VECTOR） |
| 可用性评级 | 低（覆盖 <50%，仅作条件/分组或放弃） |

**覆盖率分档**

| 档 | 字段数 | 占比 |
|---|---:|---:|
| 高 (≥0.90) | 0 | 0.0% |
| 中 (0.70–0.90) | 0 | 0.0% |
| 低 (0.50–0.70) | 0 | 0.0% |
| 稀疏 (<0.50) | 45 | 100.0% |

**历史实测分布（field_profile_perf）**

| 判定 | 字段数 | 占比 |
|---|---:|---:|
| UNUSABLE | 45 | 100.0% |

- 无带 `n_tests>0` 的有效实测记录；但历史判定已存在（UNTESTED 0 / UNUSABLE 45 等）。⚠ 历史判定可能**过时**（如 analyst7 的旧判死已作废），做尽前须重跑。

## 四、语义维度地图（自动归类）

| 语义族 | 字段数 | 平均覆盖 | 代表字段 |
|---|---:|---:|---|
| 风险与质量 | 12 | 0.33 | scl15_attrition_score、scl15_conflict、scl15_litigation |
| 其他 | 10 | 0.37 | scl15_anger、scl15_fear、scl15_gloom |
| 情绪与新闻 | 10 | 0.34 | scl15_buzz、scl15_emotionvsfact、scl15_joy |
| 价量与波动 | 6 | 0.32 | scl15_pricedirection、scl15_stress、scl15_volatility |
| 盈利与财务 | 4 | 0.37 | dividend_trend_score、scl15_debt_score、scl15_earn_score |
| 持仓与资金流 | 2 | 0.31 | scl15_fundamentalstrength、scl15_d1_fundamentalstrength |
| 修正与预期 | 1 | 0.37 | scl15_analystrating |

## 五、全字段明细

> 按 `best_sharpe` 降序（未测者置后）。`判定` 来自 `field_profile_perf`：ALIVE=历史测出过 S≥闸线（**不代表可提交**）；UNTESTED=未测；UNUSABLE/DEAD/AXIS_ONLY=已证否或仅可作轴。

| # | 字段名 | 类型 | 覆盖 | 语义族 | 测次 | best_S | best_2Y | best_sub | 判定 | 描述 |
|---:|---|---|---:|---|---:|---:|---:|---:|---|---|
| 1 | `dividend_trend_score` | VECTOR | 0.371 | 盈利与财务 | 0 | — | — | — | UNUSABLE | Score of dividend trend, scaled -1 to 1, where negative indicates falling dividends and positive indicates rising dividends |
| 2 | `scl15_analystrating` | VECTOR | 0.371 | 修正与预期 | 0 | — | — | — | UNUSABLE | Upgrade/downgrade activity scaled from -1 (downgrades) to 1 (upgrades) |
| 3 | `scl15_anger` | VECTOR | 0.371 | 其他 | 0 | — | — | — | UNUSABLE | Displeasure or anger toward the stock on a 0 to 1 scale, where 1 denotes maximum resentment |
| 4 | `scl15_attrition_score` | VECTOR | 0.371 | 风险与质量 | 0 | — | — | — | UNUSABLE | Score from 0 to 1 indicating staff reductions at a company; 1 means more layoffs |
| 5 | `scl15_buzz` | VECTOR | 0.371 | 情绪与新闻 | 0 | — | — | — | UNUSABLE | Media attention or intensity score from 0 to 1 indicating how much the stock is being talked about; zero implies other scores may be unavail |
| 6 | `scl15_conflict` | VECTOR | 0.371 | 风险与质量 | 0 | — | — | — | UNUSABLE | Score from -1 to 1 measuring disagreement versus agreement/conciliation in media coverage |
| 7 | `scl15_debt_score` | VECTOR | 0.371 | 盈利与财务 | 0 | — | — | — | UNUSABLE | Bankruptcy/default risk on a 0 to 1 scale, where 1 indicates higher bankruptcy risk |
| 8 | `scl15_earn_score` | VECTOR | 0.371 | 盈利与财务 | 0 | — | — | — | UNUSABLE | Score from -1 to 1 denoting future earnings growth or surprise; positive values indicate positive surprise, with 1 as the maximum positive |
| 9 | `scl15_emotionvsfact` | VECTOR | 0.371 | 情绪与新闻 | 0 | — | — | — | UNUSABLE | Net emotional sentiment on the stock, ranging from -1 (more negative emotion) to +1 (more positive emotion) |
| 10 | `scl15_fear` | VECTOR | 0.371 | 其他 | 0 | — | — | — | UNUSABLE | Level of fear regarding the stock on a 0 to 1 scale, where 1 denotes maximum fear |
| 11 | `scl15_fundamentalstrength` | VECTOR | 0.371 | 持仓与资金流 | 0 | — | — | — | UNUSABLE | Media-derived score from -1 to 1 representing positivity about accounting fundamentals net of negative references |
| 12 | `scl15_gloom` | VECTOR | 0.371 | 其他 | 0 | — | — | — | UNUSABLE | Negative future outlook or gloom, scaled 0 to 1, with 1 indicating maximum gloom |
| 13 | `scl15_innovation` | VECTOR | 0.371 | 其他 | 0 | — | — | — | UNUSABLE | Company innovativeness on a 0 to 1 scale, where 1 indicates maximum innovation |
| 14 | `scl15_joy` | VECTOR | 0.371 | 情绪与新闻 | 0 | — | — | — | UNUSABLE | Happiness or affection sentiment toward the stock on a 0 to 1 scale, with 1 meaning maximum happiness |
| 15 | `scl15_litigation` | VECTOR | 0.371 | 风险与质量 | 0 | — | — | — | UNUSABLE | Score from 0 to 1 indicating legal activity or controversy around a stock; 1 means more legal activity |
| 16 | `scl15_longshort` | VECTOR | 0.371 | 情绪与新闻 | 0 | — | — | — | UNUSABLE | Score from -1 to 1 indicating net buying versus shorting/selling sentiment, where positive implies more buying |
| 17 | `scl15_longshortforecast` | VECTOR | 0.371 | 其他 | 0 | — | — | — | UNUSABLE | Forecasts of buying net of forecasts of shorting/selling scaled from -1 to 1 |
| 18 | `scl15_lovehate` | VECTOR | 0.371 | 风险与质量 | 0 | — | — | — | UNUSABLE | Score denoting love, net of references to hate towards a stock, scaled from -1 to 1 |
| 19 | `scl15_managementchange` | VECTOR | 0.371 | 风险与质量 | 0 | — | — | — | UNUSABLE | Score from -1 to 1 capturing stability of a company's management; 1 implies maximum change and thus less stability |
| 20 | `scl15_managementtrust` | VECTOR | 0.371 | 风险与质量 | 0 | — | — | — | UNUSABLE | Score from -1 to 1 reflecting trust in a company's management; -1 indicates minimum trust, potentially due to unethical behavior |
| 21 | `scl15_mergers` | VECTOR | 0.371 | 风险与质量 | 0 | — | — | — | UNUSABLE | Score from 0 to 1 denoting merger and acquisition activity; 1 means the company is most likely undergoing a merger or acquisition |
| 22 | `scl15_optimism` | VECTOR | 0.371 | 其他 | 0 | — | — | — | UNUSABLE | Degree of optimism about the stock’s future growth, from -1 (maximum pessimism) to +1 (maximum optimism) |
| 23 | `scl15_price_score` | VECTOR | 0.371 | 盈利与财务 | 0 | — | — | — | UNUSABLE | Forecasts of asset price rises net of references to price drops, scaled from -1 to 1 |
| 24 | `scl15_pricedirection` | VECTOR | 0.371 | 价量与波动 | 0 | — | — | — | UNUSABLE | A score ranging from -1 to 1 giving the direction of price movement; positive values indicate upward moves, with 1 denoting maximum upward c |
| 25 | `scl15_risk_score` | VECTOR | 0.371 | 情绪与新闻 | 0 | — | — | — | UNUSABLE | Bubble risk indicator for the stock, scaled -1 to 1 based on social and emotional signals; higher positive suggests elevated bubble risk |
| 26 | `scl15_sentiment` | VECTOR | 0.371 | 情绪与新闻 | 0 | — | — | — | UNUSABLE | Net aggregate sentiment about the stock scaled from -1 (negative) to +1 (positive) |
| 27 | `scl15_stress` | VECTOR | 0.371 | 价量与波动 | 0 | — | — | — | UNUSABLE | Apprehension regarding the stock price, scaled 0 to 1, with 1 indicating maximum stress |
| 28 | `scl15_timeurgency` | VECTOR | 0.371 | 其他 | 0 | — | — | — | UNUSABLE | Urgency and timeliness net of delays scaled from -1 to 1; 1 indicates maximum timeliness and better growth prospects |
| 29 | `scl15_trust` | VECTOR | 0.371 | 其他 | 0 | — | — | — | UNUSABLE | Trustworthiness of the stock scaled from -1 to 1; 1 indicates maximum trust and minimal corruption concerns |
| 30 | `scl15_uncertainty` | VECTOR | 0.371 | 其他 | 0 | — | — | — | UNUSABLE | Confusion or uncertainty about the stock’s movement, scaled 0 to 1, with 1 indicating maximum uncertainty |
| 31 | `scl15_violence` | VECTOR | 0.371 | 其他 | 0 | — | — | — | UNUSABLE | Intensity of violent or highly entropic reactions related to the stock, scaled 0 to 1, with 1 indicating maximum intensity |
| 32 | `scl15_volatility` | VECTOR | 0.371 | 价量与波动 | 0 | — | — | — | UNUSABLE | Volatility in market prices or business conditions on a 0 to 1 scale |
| 33 | `scl15_d1_buzz` | VECTOR | 0.299 | 情绪与新闻 | 0 | — | — | — | UNUSABLE | A 0 to 1 score representing how much a particular stock is talked about. 0 indicates that other scores would also be N/A. |
| 34 | `scl15_d1_sentiment` | VECTOR | 0.295 | 情绪与新闻 | 0 | — | — | — | UNUSABLE | A score scaled between -1 to 1 expressing net sentiment on stock. |
| 35 | `scl15_d1_emotionvsfact` | VECTOR | 0.294 | 情绪与新闻 | 0 | — | — | — | UNUSABLE | This score denotes net emotional sentiment on a stock in the range of -1 to 1 |
| 36 | `scl15_d1_conflict` | VECTOR | 0.278 | 风险与质量 | 0 | — | — | — | UNUSABLE | This score denotes disagreement and net of agreement and conciliation, ranging from -1 to 1 |
| 37 | `scl15_d1_stress` | VECTOR | 0.269 | 价量与波动 | 0 | — | — | — | UNUSABLE | 0 to 1 score that denotes an apprehension on a stock price. 1 means maximum apprehension. |
| 38 | `scl15_d1_timeurgency` | VECTOR | 0.269 | 风险与质量 | 0 | — | — | — | UNUSABLE | A score ranging from -1 to 1 denoting urgency and timeliness, net of references to tardiness and delays, indicating future growth prospects  |
| 39 | `scl15_d1_optimism` | VECTOR | 0.268 | 风险与质量 | 0 | — | — | — | UNUSABLE | A score ranging from -1 to 1 expressing optimism to future growth of stock. -1 means maximum pessimism or minimum optimism towards a stock. |
| 40 | `scl15_d1_longshort` | VECTOR | 0.267 | 风险与质量 | 0 | — | — | — | UNUSABLE | A score denoting buying, net of references to shorting/selling, scaled in the range of -1 to 1 |
| 41 | `scl15_d1_risk_score` | VECTOR | 0.266 | 情绪与新闻 | 0 | — | — | — | UNUSABLE | A score ranging from -1 to 1 indicating bubble risk on a stock, considering speculative bubbles using social media and emotional expectation |
| 42 | `scl15_d1_volatility` | VECTOR | 0.264 | 价量与波动 | 0 | — | — | — | UNUSABLE | 0 to 1 score indicating volatility in market prices or business conditions. |
| 43 | `scl15_d1_pricedirection` | VECTOR | 0.263 | 价量与波动 | 0 | — | — | — | UNUSABLE | A score ranging from -1 to 1 giving the direction of price movement. Upward is +ve. Maximum directional change upwards is denoted by 1. |
| 44 | `scl15_d1_fundamentalstrength` | VECTOR | 0.259 | 持仓与资金流 | 0 | — | — | — | UNUSABLE | This score denotes positivity about accounting fundamentals, net of references to negativity about accounting fundamentals, in range of -1 t |
| 45 | `scl15_d1_trust` | VECTOR | 0.255 | 风险与质量 | 0 | — | — | — | UNUSABLE | A score ranging from -1 to 1 indicating trustworthiness of a stock as opposed to corruption practices for the underlying. 1 indicates maximu |

## 六、本地回测证据

本地库无该数据集的回测记录。

> 说明：`backtest_results` 只收录已持久化的波次（当前 EUR 共 1157 行）；本次会话的直接派发未写库，故此处为空**不代表未做尽**，实测结论见配套战役档案。

## 七、判死记录（sealed dead_end）

无针对本数据集的 `dead_end` 记录。

