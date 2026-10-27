# insiders1 — EUR 字段画像

> 自动生成于 2026-10-20 17:55　|　[← 返回索引](README.md)

## 一、数据集元信息

| 项 | 值 |
|---|---|
| 数据集 ID | `insiders1` |
| 名称 | Global Insider Trading Data |
| 类别 | INSIDERS |
| 数据字段数(平台) | 9 |
| 覆盖率 | 0.5512 |
| 平台已有 alpha | 393 |
| valueScore | 2.0 |
| 金字塔倍率 | 1.1 |
| 数据类型 | — |
| delay | 1 |
| 状态 | — |

## 二、数据集描述（平台原文）

> ⚠️ 平台目录描述存在**错配**（已实测：insiders1 / imbalance5 的描述指向无关数据集）。以「五、全字段明细」的真实字段语义为准。

This dataset provides a comprehensive mapping between Reuters Instrument Codes (RIC) and Bloomberg Identifiers (BBID), serving as a cross-reference for security identifiers across two major financial data platforms. It is essential for researchers, portfolio managers, and quantitative analysts who need to integrate or reconcile data from both Refinitiv and Bloomberg sources. By enabling accurate and efficient linkage of securities across systems, this mapping facilitates robust multi-source data analysis, backtesting, and model development, ultimately supporting more reliable and timely investment decision-making and price prediction workflows.

## 三、字段画像汇总

| 维度 | 结果 |
|---|---|
| 字段总数 | **9** |
| 类型分布 | VECTOR×9 |
| 平均覆盖率 | **0.551** |
| 覆盖率区间 | 0.55 ~ 0.55 |
| 更新频率（推断） | 事件/逐笔型（VECTOR） |
| 可用性评级 | 中（覆盖 50–70%，截面偏窄） |

**覆盖率分档**

| 档 | 字段数 | 占比 |
|---|---:|---:|
| 高 (≥0.90) | 0 | 0.0% |
| 中 (0.70–0.90) | 0 | 0.0% |
| 低 (0.50–0.70) | 9 | 100.0% |
| 稀疏 (<0.50) | 0 | 0.0% |

**历史实测分布（field_profile_perf）**

| 判定 | 字段数 | 占比 |
|---|---:|---:|
| UNUSABLE | 9 | 100.0% |

- 无带 `n_tests>0` 的有效实测记录；但历史判定已存在（UNTESTED 0 / UNUSABLE 9 等）。⚠ 历史判定可能**过时**（如 analyst7 的旧判死已作废），做尽前须重跑。

## 四、语义维度地图（自动归类）

| 语义族 | 字段数 | 平均覆盖 | 代表字段 |
|---|---:|---:|---|
| 价量与波动 | 4 | 0.55 | insd1_price、insd1_shares、insd1_tradesignificance |
| 宏观与行业 | 2 | 0.55 | insd1_value、transaction_currency_code |
| 元数据与非信号 | 1 | 0.55 | insd1_gvkey |
| 盈利与财务 | 1 | 0.55 | insd1_holdings |
| 其他 | 1 | 0.55 | insd1_valueeur |

## 五、全字段明细

> 按 `best_sharpe` 降序（未测者置后）。`判定` 来自 `field_profile_perf`：ALIVE=历史测出过 S≥闸线（**不代表可提交**）；UNTESTED=未测；UNUSABLE/DEAD/AXIS_ONLY=已证否或仅可作轴。

| # | 字段名 | 类型 | 覆盖 | 语义族 | 测次 | best_S | best_2Y | best_sub | 判定 | 描述 |
|---:|---|---|---:|---|---:|---:|---:|---:|---|---|
| 1 | `insd1_gvkey` | VECTOR | 0.551 | 元数据与非信号 | 0 | — | — | — | UNUSABLE | Compustat Global Company Identifier (Global Value Key) for the issuer |
| 2 | `insd1_holdings` | VECTOR | 0.551 | 盈利与财务 | 0 | — | — | — | UNUSABLE | Total equity share holdings of the insider after the transaction |
| 3 | `insd1_price` | VECTOR | 0.551 | 价量与波动 | 0 | — | — | — | UNUSABLE | Transaction price per share; if a range was reported, this is the minimum price |
| 4 | `insd1_shares` | VECTOR | 0.551 | 价量与波动 | 0 | — | — | — | UNUSABLE | Number of shares (or units) traded in the transaction |
| 5 | `insd1_tradesignificance` | VECTOR | 0.551 | 价量与波动 | 0 | — | — | — | UNUSABLE | Significance score of the trade (1 = low significance, 3 = high significance) |
| 6 | `insd1_value` | VECTOR | 0.551 | 宏观与行业 | 0 | — | — | — | UNUSABLE | Total value of the transaction in original currency |
| 7 | `insd1_valueeur` | VECTOR | 0.551 | 其他 | 0 | — | — | — | UNUSABLE | Total value of the transaction in Euro |
| 8 | `max_trade_price` | VECTOR | 0.551 | 价量与波动 | 0 | — | — | — | UNUSABLE | Maximum transaction price per share when a price range was reported |
| 9 | `transaction_currency_code` | VECTOR | 0.551 | 宏观与行业 | 0 | — | — | — | UNUSABLE | Three-letter ISO currency code of the transaction’s currency |

## 六、本地回测证据

本地库无该数据集的回测记录。

> 说明：`backtest_results` 只收录已持久化的波次（当前 EUR 共 1157 行）；本次会话的直接派发未写库，故此处为空**不代表未做尽**，实测结论见配套战役档案。

## 七、判死记录（sealed dead_end）

无针对本数据集的 `dead_end` 记录。

