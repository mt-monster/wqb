# model307 — EUR 字段画像

> 自动生成于 2026-10-20 17:55　|　[← 返回索引](README.md)

## 一、数据集元信息

| 项 | 值 |
|---|---|
| 数据集 ID | `model307` |
| 名称 | Global Sales Allocation Model Data |
| 类别 | MODEL |
| 数据字段数(平台) | 15 |
| 覆盖率 | 0.625 |
| 平台已有 alpha | 3 |
| valueScore | 4.0 |
| 金字塔倍率 | 1.3 |
| 数据类型 | — |
| delay | 1 |
| 状态 | — |

## 二、数据集描述（平台原文）

> ⚠️ 平台目录描述存在**错配**（已实测：insiders1 / imbalance5 的描述指向无关数据集）。以「五、全字段明细」的真实字段语义为准。

This dataset provides a comprehensive mapping between Reuters Instrument Codes (RIC) and Bloomberg Identifiers (BBID), enabling seamless cross-referencing of securities across two major financial data platforms. By linking these unique identifiers, the dataset facilitates accurate integration of market data, trading information, and analytics from both Bloomberg and Refinitiv sources. This is particularly useful for portfolio managers, analysts, and trading systems that require consistent security identification for aggregation, reconciliation, and analysis. While not directly predictive of price movements, the dataset is essential for ensuring data integrity and enabling robust multi-source financial research and modeling.

## 三、字段画像汇总

| 维度 | 结果 |
|---|---|
| 字段总数 | **15** |
| 类型分布 | VECTOR×15 |
| 平均覆盖率 | **0.625** |
| 覆盖率区间 | 0.61 ~ 0.67 |
| 更新频率（推断） | 事件/逐笔型（VECTOR） |
| 可用性评级 | 中（覆盖 50–70%，截面偏窄） |

**覆盖率分档**

| 档 | 字段数 | 占比 |
|---|---:|---:|
| 高 (≥0.90) | 0 | 0.0% |
| 中 (0.70–0.90) | 0 | 0.0% |
| 低 (0.50–0.70) | 15 | 100.0% |
| 稀疏 (<0.50) | 0 | 0.0% |

**历史实测分布（field_profile_perf）**

| 判定 | 字段数 | 占比 |
|---|---:|---:|
| UNTESTED | 15 | 100.0% |

- 该数据集全部字段**尚未实测**（UNTESTED）⇒ 优先做尽

## 四、语义维度地图（自动归类）

| 语义族 | 字段数 | 平均覆盖 | 代表字段 |
|---|---:|---:|---|
| 盈利与财务 | 7 | 0.61 | canada_sales_fraction、mdl307_sales_pct_emea、mdl307_sales_pct_eu |
| 元数据与非信号 | 5 | 0.63 | mdl307_atlas_unit_name、mdl307_cusip、australia_nz_sales_ratio |
| 宏观与行业 | 2 | 0.67 | mdl307_country、mdl307_sector |
| 其他 | 1 | 0.61 | mdl307_sales_pct_gb |

## 五、全字段明细

> 按 `best_sharpe` 降序（未测者置后）。`判定` 来自 `field_profile_perf`：ALIVE=历史测出过 S≥闸线（**不代表可提交**）；UNTESTED=未测；UNUSABLE/DEAD/AXIS_ONLY=已证否或仅可作轴。

| # | 字段名 | 类型 | 覆盖 | 语义族 | 测次 | best_S | best_2Y | best_sub | 判定 | 描述 |
|---:|---|---|---:|---|---:|---:|---:|---:|---|---|
| 1 | `mdl307_atlas_unit_name` | VECTOR | 0.667 | 元数据与非信号 | 0 | — | — | — | UNTESTED | Atlas unit name |
| 2 | `mdl307_country` | VECTOR | 0.667 | 宏观与行业 | 0 | — | — | — | UNTESTED | Country Code |
| 3 | `mdl307_cusip` | VECTOR | 0.667 | 元数据与非信号 | 0 | — | — | — | UNTESTED | Point in Time CUSIP |
| 4 | `mdl307_sector` | VECTOR | 0.667 | 宏观与行业 | 0 | — | — | — | UNTESTED | Sector |
| 5 | `australia_nz_sales_ratio` | VECTOR | 0.610 | 元数据与非信号 | 0 | — | — | — | UNTESTED | Fraction of total company sales attributed to Australia and New Zealand at the reporting date |
| 6 | `canada_sales_fraction` | VECTOR | 0.610 | 盈利与财务 | 0 | — | — | — | UNTESTED | Fraction of the company’s total sales revenue allocated to Canada as a proportion (0 to 1) |
| 7 | `mdl307_sales_pct_axj` | VECTOR | 0.610 | 元数据与非信号 | 0 | — | — | — | UNTESTED | Fraction of total company sales attributed to Asia excluding Japan at the reporting date |
| 8 | `mdl307_sales_pct_cnax` | VECTOR | 0.610 | 元数据与非信号 | 0 | — | — | — | UNTESTED | Fraction of total company sales attributed to Mainland China (excluding Hong Kong and Macau) at the reporting date |
| 9 | `mdl307_sales_pct_emea` | VECTOR | 0.610 | 盈利与财务 | 0 | — | — | — | UNTESTED | Fraction of the company's total sales revenue allocated to Europe, Middle East, and Africa (EMEA) region, as a decimal proportion |
| 10 | `mdl307_sales_pct_eu` | VECTOR | 0.610 | 盈利与财务 | 0 | — | — | — | UNTESTED | Fraction of company sales allocated to the European Union excluding Great Britain as a proportion of total revenue |
| 11 | `mdl307_sales_pct_gb` | VECTOR | 0.610 | 其他 | 0 | — | — | — | UNTESTED | Fraction of the company's total sales allocated to Great Britain (UK) for the given period, expressed as a number between 0 and 1 |
| 12 | `mdl307_sales_pct_jp` | VECTOR | 0.610 | 盈利与财务 | 0 | — | — | — | UNTESTED | Fraction of the company’s total sales revenue allocated to Japan as a proportion (0 to 1) |
| 13 | `mdl307_sales_pct_latam` | VECTOR | 0.610 | 盈利与财务 | 0 | — | — | — | UNTESTED | Fraction of the company's total sales revenue allocated to the Latin America and Caribbean region, as a decimal proportion |
| 14 | `mdl307_sales_pct_unclassified` | VECTOR | 0.610 | 盈利与财务 | 0 | — | — | — | UNTESTED | Fraction of the company’s total sales revenue that is unallocated or not classified to any defined geographic region as a proportion (0 to 1 |
| 15 | `mdl307_sales_pct_us` | VECTOR | 0.610 | 盈利与财务 | 0 | — | — | — | UNTESTED | Fraction of the company’s total sales revenue allocated to the United States as a proportion (0 to 1) |

## 六、本地回测证据

本地库无该数据集的回测记录。

> 说明：`backtest_results` 只收录已持久化的波次（当前 EUR 共 1157 行）；本次会话的直接派发未写库，故此处为空**不代表未做尽**，实测结论见配套战役档案。

## 七、判死记录（sealed dead_end）

无针对本数据集的 `dead_end` 记录。

