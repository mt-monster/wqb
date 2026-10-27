# other327 — EUR 字段画像

> 自动生成于 2026-10-20 17:55　|　[← 返回索引](README.md)

## 一、数据集元信息

| 项 | 值 |
|---|---|
| 数据集 ID | `other327` |
| 名称 | Sensitivity to Interest Rates Model |
| 类别 | OTHER |
| 数据字段数(平台) | 3 |
| 覆盖率 | 0.5158 |
| 平台已有 alpha | 28 |
| valueScore | 4.0 |
| 金字塔倍率 | 1.5 |
| 数据类型 | — |
| delay | 1 |
| 状态 | — |

## 二、数据集描述（平台原文）

> ⚠️ 平台目录描述存在**错配**（已实测：insiders1 / imbalance5 的描述指向无关数据集）。以「五、全字段明细」的真实字段语义为准。

This dataset provides a machine learning-based model that quantifies the sensitivity of individual stocks to changes in interest rates, using elastic net regression. It includes metrics such as sensitivity to parallel shifts (level) and twists (slope) of the yield curve, derived from principal component analysis of global interest rate data. Covering over 11,000 stocks across 45 countries, the dataset enables investors to assess how monetary policy changes and yield curve movements may impact stock returns. By incorporating these sensitivity measures into portfolio construction and risk management, users can better predict price movements during periods of interest rate volatility and optimize exposure to macroeconomic factors.

## 三、字段画像汇总

| 维度 | 结果 |
|---|---|
| 字段总数 | **3** |
| 类型分布 | MATRIX×3 |
| 平均覆盖率 | **0.516** |
| 覆盖率区间 | 0.50 ~ 0.52 |
| 更新频率（推断） | 快照（按库表更新，需实测） |
| 可用性评级 | 中（覆盖 50–70%，截面偏窄） |

**覆盖率分档**

| 档 | 字段数 | 占比 |
|---|---:|---:|
| 高 (≥0.90) | 0 | 0.0% |
| 中 (0.70–0.90) | 0 | 0.0% |
| 低 (0.50–0.70) | 3 | 100.0% |
| 稀疏 (<0.50) | 0 | 0.0% |

**历史实测分布（field_profile_perf）**

| 判定 | 字段数 | 占比 |
|---|---:|---:|
| UNUSABLE | 3 | 100.0% |

- 无带 `n_tests>0` 的有效实测记录；但历史判定已存在（UNTESTED 0 / UNUSABLE 3 等）。⚠ 历史判定可能**过时**（如 analyst7 的旧判死已作废），做尽前须重跑。

## 四、语义维度地图（自动归类）

| 语义族 | 字段数 | 平均覆盖 | 代表字段 |
|---|---:|---:|---|
| 宏观与行业 | 2 | 0.52 | oth327_sirc_lev、oth327_sirc_sl |
| 其他 | 1 | 0.50 | oth327_mktcap |

## 五、全字段明细

> 按 `best_sharpe` 降序（未测者置后）。`判定` 来自 `field_profile_perf`：ALIVE=历史测出过 S≥闸线（**不代表可提交**）；UNTESTED=未测；UNUSABLE/DEAD/AXIS_ONLY=已证否或仅可作轴。

| # | 字段名 | 类型 | 覆盖 | 语义族 | 测次 | best_S | best_2Y | best_sub | 判定 | 描述 |
|---:|---|---|---:|---|---:|---:|---:|---:|---|---|
| 1 | `oth327_sirc_lev` | MATRIX | 0.522 | 宏观与行业 | 0 | — | — | — | UNUSABLE | Numeric value quantifying the stock's sensitivity to parallel (level) shifts in the US Treasury yield curve |
| 2 | `oth327_sirc_sl` | MATRIX | 0.522 | 宏观与行业 | 0 | — | — | — | UNUSABLE | Numeric value quantifying the stock's sensitivity to slope (twist/steepening/flattening) changes in the US Treasury yield curve |
| 3 | `oth327_mktcap` | MATRIX | 0.503 | 其他 | 0 | — | — | — | UNUSABLE | Market capitalization of the company, typically measured in US Dollars; represents the total market value of the company’s outstanding share |

## 六、本地回测证据

本地库无该数据集的回测记录。

> 说明：`backtest_results` 只收录已持久化的波次（当前 EUR 共 1157 行）；本次会话的直接派发未写库，故此处为空**不代表未做尽**，实测结论见配套战役档案。

## 七、判死记录（sealed dead_end）

无针对本数据集的 `dead_end` 记录。

