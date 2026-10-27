# option_chart_model — EUR 字段画像

> 自动生成于 2026-10-20 17:55　|　[← 返回索引](README.md)

## 一、数据集元信息

| 项 | 值 |
|---|---|
| 数据集 ID | `option_chart_model` |
| 名称 | Option Chart Image Return Prediction |
| 类别 | MODEL |
| 数据字段数(平台) | 39 |
| 覆盖率 | 0.4352 |
| 平台已有 alpha | 0 |
| valueScore | 6.0 |
| 金字塔倍率 | 1.3 |
| 数据类型 | — |
| delay | 1 |
| 状态 | — |

## 二、数据集描述（平台原文）

> ⚠️ 平台目录描述存在**错配**（已实测：insiders1 / imbalance5 的描述指向无关数据集）。以「五、全字段明细」的真实字段语义为准。

This dataset consists of 2D financial chart images generated from historical option market data, including implied volatility curves and OHLC price charts, for individual stocks. Using these images, a convolutional neural network (CNN) model is trained to predict future single-stock returns, both as raw values and as quantile rankings relative to peers. The dataset provides model outputs such as predicted returns, quantile labels, and associated confidence probabilities for multiple forecast horizons. By leveraging visual patterns in option data, the dataset enables systematic, cross-sectional return predictions and can help identify stocks with favorable risk-reward profiles, making it a valuable tool for quantitative trading and investment strategies focused on price movement forecasting

## 三、字段画像汇总

| 维度 | 结果 |
|---|---|
| 字段总数 | **39** |
| 类型分布 | MATRIX×39 |
| 平均覆盖率 | **0.435** |
| 覆盖率区间 | 0.44 ~ 0.44 |
| 更新频率（推断） | 快照（按库表更新，需实测） |
| 可用性评级 | 低（覆盖 <50%，仅作条件/分组或放弃） |

**覆盖率分档**

| 档 | 字段数 | 占比 |
|---|---:|---:|
| 高 (≥0.90) | 0 | 0.0% |
| 中 (0.70–0.90) | 0 | 0.0% |
| 低 (0.50–0.70) | 0 | 0.0% |
| 稀疏 (<0.50) | 39 | 100.0% |

**历史实测分布（field_profile_perf）**

| 判定 | 字段数 | 占比 |
|---|---:|---:|
| UNUSABLE | 39 | 100.0% |

- 无带 `n_tests>0` 的有效实测记录；但历史判定已存在（UNTESTED 0 / UNUSABLE 39 等）。⚠ 历史判定可能**过时**（如 analyst7 的旧判死已作废），做尽前须重跑。

## 四、语义维度地图（自动归类）

| 语义族 | 字段数 | 平均覆盖 | 代表字段 |
|---|---:|---:|---|
| 价量与波动 | 26 | 0.44 | option_call_iv_level_0、option_call_iv_level_1、option_call_iv_level_10 |
| 其他 | 13 | 0.44 | put_call_parity_metric_0、put_call_parity_metric_1、put_call_parity_metric_10 |

## 五、全字段明细

> 按 `best_sharpe` 降序（未测者置后）。`判定` 来自 `field_profile_perf`：ALIVE=历史测出过 S≥闸线（**不代表可提交**）；UNTESTED=未测；UNUSABLE/DEAD/AXIS_ONLY=已证否或仅可作轴。

| # | 字段名 | 类型 | 覆盖 | 语义族 | 测次 | best_S | best_2Y | best_sub | 判定 | 描述 |
|---:|---|---|---:|---|---:|---:|---:|---:|---|---|
| 1 | `option_call_iv_level_0` | MATRIX | 0.435 | 价量与波动 | 0 | — | — | — | UNUSABLE | Implied volatility value for call options at the 0th reference point. |
| 2 | `option_call_iv_level_1` | MATRIX | 0.435 | 价量与波动 | 0 | — | — | — | UNUSABLE | Implied volatility value for call options at the 1st reference point. |
| 3 | `option_call_iv_level_10` | MATRIX | 0.435 | 价量与波动 | 0 | — | — | — | UNUSABLE | Implied volatility value for call options at the 10th reference point. |
| 4 | `option_call_iv_level_11` | MATRIX | 0.435 | 价量与波动 | 0 | — | — | — | UNUSABLE | Implied volatility value for call options at the 11th reference point. |
| 5 | `option_call_iv_level_12` | MATRIX | 0.435 | 价量与波动 | 0 | — | — | — | UNUSABLE | Implied volatility value for call options at the 12th reference point. |
| 6 | `option_call_iv_level_2` | MATRIX | 0.435 | 价量与波动 | 0 | — | — | — | UNUSABLE | Implied volatility value for call options at the 2nd reference point. |
| 7 | `option_call_iv_level_3` | MATRIX | 0.435 | 价量与波动 | 0 | — | — | — | UNUSABLE | Implied volatility value for call options at the 3rd reference point. |
| 8 | `option_call_iv_level_4` | MATRIX | 0.435 | 价量与波动 | 0 | — | — | — | UNUSABLE | Implied volatility value for call options at the 4th reference point. |
| 9 | `option_call_iv_level_5` | MATRIX | 0.435 | 价量与波动 | 0 | — | — | — | UNUSABLE | Implied volatility value for call options at the 5th reference point. |
| 10 | `option_call_iv_level_6` | MATRIX | 0.435 | 价量与波动 | 0 | — | — | — | UNUSABLE | Implied volatility value for call options at the 6th reference point. |
| 11 | `option_call_iv_level_7` | MATRIX | 0.435 | 价量与波动 | 0 | — | — | — | UNUSABLE | Implied volatility value for call options at the 7th reference point. |
| 12 | `option_call_iv_level_8` | MATRIX | 0.435 | 价量与波动 | 0 | — | — | — | UNUSABLE | Implied volatility value for call options at the 8th reference point. |
| 13 | `option_call_iv_level_9` | MATRIX | 0.435 | 价量与波动 | 0 | — | — | — | UNUSABLE | Implied volatility value for call options at the 9th reference point. |
| 14 | `option_put_iv_level_0` | MATRIX | 0.435 | 价量与波动 | 0 | — | — | — | UNUSABLE | Implied volatility value for put options at the 0th reference point. |
| 15 | `option_put_iv_level_1` | MATRIX | 0.435 | 价量与波动 | 0 | — | — | — | UNUSABLE | Implied volatility value for put options at the 1st reference point. |
| 16 | `option_put_iv_level_10` | MATRIX | 0.435 | 价量与波动 | 0 | — | — | — | UNUSABLE | Implied volatility value for put options at the 10th reference point. |
| 17 | `option_put_iv_level_11` | MATRIX | 0.435 | 价量与波动 | 0 | — | — | — | UNUSABLE | Implied volatility value for put options at the 11th reference point. |
| 18 | `option_put_iv_level_12` | MATRIX | 0.435 | 价量与波动 | 0 | — | — | — | UNUSABLE | Implied volatility value for put options at the 12th reference point. |
| 19 | `option_put_iv_level_2` | MATRIX | 0.435 | 价量与波动 | 0 | — | — | — | UNUSABLE | Implied volatility value for put options at the 2nd reference point. |
| 20 | `option_put_iv_level_3` | MATRIX | 0.435 | 价量与波动 | 0 | — | — | — | UNUSABLE | Implied volatility value for put options at the 3rd reference point. |
| 21 | `option_put_iv_level_4` | MATRIX | 0.435 | 价量与波动 | 0 | — | — | — | UNUSABLE | Implied volatility value for put options at the 4th reference point. |
| 22 | `option_put_iv_level_5` | MATRIX | 0.435 | 价量与波动 | 0 | — | — | — | UNUSABLE | Implied volatility value for put options at the 5th reference point. |
| 23 | `option_put_iv_level_6` | MATRIX | 0.435 | 价量与波动 | 0 | — | — | — | UNUSABLE | Implied volatility value for put options at the 6th reference point. |
| 24 | `option_put_iv_level_7` | MATRIX | 0.435 | 价量与波动 | 0 | — | — | — | UNUSABLE | Implied volatility value for put options at the 7th reference point. |
| 25 | `option_put_iv_level_8` | MATRIX | 0.435 | 价量与波动 | 0 | — | — | — | UNUSABLE | Implied volatility value for put options at the 8th reference point. |
| 26 | `option_put_iv_level_9` | MATRIX | 0.435 | 价量与波动 | 0 | — | — | — | UNUSABLE | Implied volatility value for put options at the 9th reference point. |
| 27 | `put_call_parity_metric_0` | MATRIX | 0.435 | 其他 | 0 | — | — | — | UNUSABLE | Put-call parity calculation at the 0th reference point. |
| 28 | `put_call_parity_metric_1` | MATRIX | 0.435 | 其他 | 0 | — | — | — | UNUSABLE | Put-call parity calculation at the 1st reference point. |
| 29 | `put_call_parity_metric_10` | MATRIX | 0.435 | 其他 | 0 | — | — | — | UNUSABLE | Put-call parity calculation at the 10th reference point. |
| 30 | `put_call_parity_metric_11` | MATRIX | 0.435 | 其他 | 0 | — | — | — | UNUSABLE | Put-call parity calculation at the 11th reference point. |
| 31 | `put_call_parity_metric_12` | MATRIX | 0.435 | 其他 | 0 | — | — | — | UNUSABLE | Put-call parity calculation at the 12th reference point. |
| 32 | `put_call_parity_metric_2` | MATRIX | 0.435 | 其他 | 0 | — | — | — | UNUSABLE | Put-call parity calculation at the 2nd reference point. |
| 33 | `put_call_parity_metric_3` | MATRIX | 0.435 | 其他 | 0 | — | — | — | UNUSABLE | Put-call parity calculation at the 3rd reference point. |
| 34 | `put_call_parity_metric_4` | MATRIX | 0.435 | 其他 | 0 | — | — | — | UNUSABLE | Put-call parity calculation at the 4th reference point. |
| 35 | `put_call_parity_metric_5` | MATRIX | 0.435 | 其他 | 0 | — | — | — | UNUSABLE | Put-call parity calculation at the 5th reference point. |
| 36 | `put_call_parity_metric_6` | MATRIX | 0.435 | 其他 | 0 | — | — | — | UNUSABLE | Put-call parity calculation at the 6th reference point. |
| 37 | `put_call_parity_metric_7` | MATRIX | 0.435 | 其他 | 0 | — | — | — | UNUSABLE | Put-call parity calculation at the 7th reference point. |
| 38 | `put_call_parity_metric_8` | MATRIX | 0.435 | 其他 | 0 | — | — | — | UNUSABLE | Put-call parity calculation at the 8th reference point. |
| 39 | `put_call_parity_metric_9` | MATRIX | 0.435 | 其他 | 0 | — | — | — | UNUSABLE | Put-call parity calculation at the 9th reference point. |

## 六、本地回测证据

本地库无该数据集的回测记录。

> 说明：`backtest_results` 只收录已持久化的波次（当前 EUR 共 1157 行）；本次会话的直接派发未写库，故此处为空**不代表未做尽**，实测结论见配套战役档案。

## 七、判死记录（sealed dead_end）

无针对本数据集的 `dead_end` 记录。

