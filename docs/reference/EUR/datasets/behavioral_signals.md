# behavioral_signals — EUR 字段画像

> 自动生成于 2026-10-20 17:55　|　[← 返回索引](README.md)

## 一、数据集元信息

| 项 | 值 |
|---|---|
| 数据集 ID | `behavioral_signals` |
| 名称 | Behavioral Finance Signal Factors |
| 类别 | MODEL |
| 数据字段数(平台) | 7 |
| 覆盖率 | 0.557 |
| 平台已有 alpha | 1 |
| valueScore | 4.0 |
| 金字塔倍率 | 1.3 |
| 数据类型 | — |
| delay | 1 |
| 状态 | — |

## 二、数据集描述（平台原文）

> ⚠️ 平台目录描述存在**错配**（已实测：insiders1 / imbalance5 的描述指向无关数据集）。以「五、全字段明细」的真实字段语义为准。

This dataset provides a suite of behavioral finance-based signals designed to capture investor extrapolation bias in equity markets. It includes six key factors: three that analyze the shape and curvature of price paths, and three that identify salient patterns such as streaks in returns, extreme daily movements, and visually prominent trends. By quantifying how investors may irrationally project recent performance into the future, these signals serve as contrarian indicators and can help forecast short-term reversals and momentum effects. The dataset is valuable for predictive modeling, risk assessment, and portfolio construction, offering insights into market inefficiencies driven by psychological biases and aiding in the identification of potential mispricings and alpha opportunities.

## 三、字段画像汇总

| 维度 | 结果 |
|---|---|
| 字段总数 | **7** |
| 类型分布 | VECTOR×7 |
| 平均覆盖率 | **0.557** |
| 覆盖率区间 | 0.56 ~ 0.56 |
| 更新频率（推断） | 事件/逐笔型（VECTOR） |
| 可用性评级 | 中（覆盖 50–70%，截面偏窄） |

**覆盖率分档**

| 档 | 字段数 | 占比 |
|---|---:|---:|
| 高 (≥0.90) | 0 | 0.0% |
| 中 (0.70–0.90) | 0 | 0.0% |
| 低 (0.50–0.70) | 7 | 100.0% |
| 稀疏 (<0.50) | 0 | 0.0% |

**历史实测分布（field_profile_perf）**

| 判定 | 字段数 | 占比 |
|---|---:|---:|
| UNUSABLE | 7 | 100.0% |

- 无带 `n_tests>0` 的有效实测记录；但历史判定已存在（UNTESTED 0 / UNUSABLE 7 等）。⚠ 历史判定可能**过时**（如 analyst7 的旧判死已作废），做尽前须重跑。

## 四、语义维度地图（自动归类）

| 语义族 | 字段数 | 平均覆盖 | 代表字段 |
|---|---:|---:|---|
| 价量与波动 | 6 | 0.56 | chronological_return_sequence_correlation、consecutive_return_streak_length、extreme_daily_return_indicator |
| 盈利与财务 | 1 | 0.56 | total_equity_market_value_usd |

## 五、全字段明细

> 按 `best_sharpe` 降序（未测者置后）。`判定` 来自 `field_profile_perf`：ALIVE=历史测出过 S≥闸线（**不代表可提交**）；UNTESTED=未测；UNUSABLE/DEAD/AXIS_ONLY=已证否或仅可作轴。

| # | 字段名 | 类型 | 覆盖 | 语义族 | 测次 | best_S | best_2Y | best_sub | 判定 | 描述 |
|---:|---|---|---:|---|---:|---:|---:|---:|---|---|
| 1 | `chronological_return_sequence_correlation` | VECTOR | 0.557 | 价量与波动 | 0 | — | — | — | UNUSABLE | Chronological Return Ordering; correlation of daily return magnitude with their sequence, capturing recency bias in return patterns |
| 2 | `consecutive_return_streak_length` | VECTOR | 0.557 | 价量与波动 | 0 | — | — | — | UNUSABLE | Streak in Returns; length and direction (+/-) of most recent consecutive up or down daily returns, reflecting momentum/reversal tendency |
| 3 | `extreme_daily_return_indicator` | VECTOR | 0.557 | 价量与波动 | 0 | — | — | — | UNUSABLE | Degree of Return Extremeness; measures how extreme the most extreme daily positive and negative returns are, normalized by recent volatility |
| 4 | `price_path_curvature_measure` | VECTOR | 0.557 | 价量与波动 | 0 | — | — | — | UNUSABLE | Price-Path Convexity; measures the curvature (convexity/concavity) of recent price path, indicating price path shapes that may predict rever |
| 5 | `salience_weighted_return_score` | VECTOR | 0.557 | 价量与波动 | 0 | — | — | — | UNUSABLE | Salience Theory Value; measures the impact of standout past daily returns by comparing salience-weighted returns to equal-weighted returns,  |
| 6 | `total_equity_market_value_usd` | VECTOR | 0.557 | 盈利与财务 | 0 | — | — | — | UNUSABLE | Market capitalization of the company in US dollars on the factor computation date |
| 7 | `visual_price_path_shape_score` | VECTOR | 0.557 | 价量与波动 | 0 | — | — | — | UNUSABLE | Visual Shape Score; measures the fraction of the price path above or below the straight line between start and end prices, capturing path co |

## 六、本地回测证据

本地库无该数据集的回测记录。

> 说明：`backtest_results` 只收录已持久化的波次（当前 EUR 共 1157 行）；本次会话的直接派发未写库，故此处为空**不代表未做尽**，实测结论见配套战役档案。

## 七、判死记录（sealed dead_end）

无针对本数据集的 `dead_end` 记录。

