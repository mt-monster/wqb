# insiders12 — EUR 字段画像

> 自动生成于 2026-10-20 17:55　|　[← 返回索引](README.md)

## 一、数据集元信息

| 项 | 值 |
|---|---|
| 数据集 ID | `insiders12` |
| 名称 | UK Insider Transaction Data |
| 类别 | INSIDERS |
| 数据字段数(平台) | 8 |
| 覆盖率 | 0.2008 |
| 平台已有 alpha | 201 |
| valueScore | 2.0 |
| 金字塔倍率 | 1.1 |
| 数据类型 | — |
| delay | 1 |
| 状态 | — |

## 二、数据集描述（平台原文）

> ⚠️ 平台目录描述存在**错配**（已实测：insiders1 / imbalance5 的描述指向无关数据集）。以「五、全字段明细」的真实字段语义为准。

This dataset provides a comprehensive mapping between Bloomberg IDs (BBID) and Reuters Instrument Codes (RIC), enabling seamless cross-referencing of securities across two major financial data platforms. By linking these identifiers, the dataset facilitates data integration, aggregation, and validation for quantitative research, portfolio management, and trading systems. Accurate mapping ensures that price, volume, and corporate action data from different sources can be reliably combined, reducing errors and improving the quality of analytics. While not directly predictive, this dataset is essential for constructing robust multi-source datasets that underpin price movement prediction models.

## 三、字段画像汇总

| 维度 | 结果 |
|---|---|
| 字段总数 | **8** |
| 类型分布 | VECTOR×8 |
| 平均覆盖率 | **0.201** |
| 覆盖率区间 | 0.19 ~ 0.26 |
| 更新频率（推断） | 事件/逐笔型（VECTOR） |
| 可用性评级 | 低（覆盖 <50%，仅作条件/分组或放弃） |

**覆盖率分档**

| 档 | 字段数 | 占比 |
|---|---:|---:|
| 高 (≥0.90) | 0 | 0.0% |
| 中 (0.70–0.90) | 0 | 0.0% |
| 低 (0.50–0.70) | 0 | 0.0% |
| 稀疏 (<0.50) | 8 | 100.0% |

**历史实测分布（field_profile_perf）**

| 判定 | 字段数 | 占比 |
|---|---:|---:|
| UNUSABLE | 8 | 100.0% |

- 无带 `n_tests>0` 的有效实测记录；但历史判定已存在（UNTESTED 0 / UNUSABLE 8 等）。⚠ 历史判定可能**过时**（如 analyst7 的旧判死已作废），做尽前须重跑。

## 四、语义维度地图（自动归类）

| 语义族 | 字段数 | 平均覆盖 | 代表字段 |
|---|---:|---:|---|
| 价量与波动 | 4 | 0.19 | insd12_mktprice、option_exercise_price_eur、option_exercise_price_gbp |
| 持仓与资金流 | 3 | 0.19 | insd12_percent、insd12_positionchangetransactionamount、insd12_sharesheld |
| 元数据与非信号 | 1 | 0.26 | insd12_transactioncode |

## 五、全字段明细

> 按 `best_sharpe` 降序（未测者置后）。`判定` 来自 `field_profile_perf`：ALIVE=历史测出过 S≥闸线（**不代表可提交**）；UNTESTED=未测；UNUSABLE/DEAD/AXIS_ONLY=已证否或仅可作轴。

| # | 字段名 | 类型 | 覆盖 | 语义族 | 测次 | best_S | best_2Y | best_sub | 判定 | 描述 |
|---:|---|---|---:|---|---:|---:|---:|---:|---|---|
| 1 | `insd12_transactioncode` | VECTOR | 0.259 | 元数据与非信号 | 0 | — | — | — | UNUSABLE | A code representing the type or nature of the transaction. |
| 2 | `insd12_mktprice` | VECTOR | 0.193 | 价量与波动 | 0 | — | — | — | UNUSABLE | Market price per share/security at the transaction date, as reported, unadjusted for corporate actions |
| 3 | `insd12_percent` | VECTOR | 0.193 | 持仓与资金流 | 0 | — | — | — | UNUSABLE | Post-event insider ownership percentage, as directly reported; may be a bound depending on GLTPercent |
| 4 | `insd12_positionchangetransactionamount` | VECTOR | 0.193 | 持仓与资金流 | 0 | — | — | — | UNUSABLE | Number of shares bought (+) or sold (-) in the transaction |
| 5 | `insd12_sharesheld` | VECTOR | 0.193 | 持仓与资金流 | 0 | — | — | — | UNUSABLE | Number of shares held by the insider after the transaction as officially reported |
| 6 | `option_exercise_price_eur` | VECTOR | 0.193 | 价量与波动 | 0 | — | — | — | UNUSABLE | Exercise price for derivatives or options in EUR, as disclosed in the transaction |
| 7 | `option_exercise_price_gbp` | VECTOR | 0.193 | 价量与波动 | 0 | — | — | — | UNUSABLE | Exercise price of derivatives or options in GBP, as disclosed in the transaction |
| 8 | `option_exercise_price_reported` | VECTOR | 0.193 | 价量与波动 | 0 | — | — | — | UNUSABLE | Price at which the option/derivative was exercised at the time of the trade; currency varies by context |

## 六、本地回测证据

本地库无该数据集的回测记录。

> 说明：`backtest_results` 只收录已持久化的波次（当前 EUR 共 1157 行）；本次会话的直接派发未写库，故此处为空**不代表未做尽**，实测结论见配套战役档案。

## 七、判死记录（sealed dead_end）

无针对本数据集的 `dead_end` 记录。

