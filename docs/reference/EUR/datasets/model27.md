# model27 — EUR 字段画像

> 自动生成于 2026-10-20 17:55　|　[← 返回索引](README.md)

## 一、数据集元信息

| 项 | 值 |
|---|---|
| 数据集 ID | `model27` |
| 名称 | Credit Risk Model |
| 类别 | MODEL |
| 数据字段数(平台) | 14 |
| 覆盖率 | 0.8931 |
| 平台已有 alpha | 20 |
| valueScore | 2.0 |
| 金字塔倍率 | 1.3 |
| 数据类型 | — |
| delay | 1 |
| 状态 | — |

## 二、数据集描述（平台原文）

> ⚠️ 平台目录描述存在**错配**（已实测：insiders1 / imbalance5 的描述指向无关数据集）。以「五、全字段明细」的真实字段语义为准。

This dataset provides a comprehensive mapping between Bloomberg Identifiers (BBID) and Reuters Instrument Codes (RIC), facilitating cross-platform security identification and integration. It is essential for data normalization, enabling users to link and reconcile securities across Bloomberg and Reuters data sources. While not directly predictive of price movements, the dataset is crucial for ensuring accurate data alignment in multi-source quantitative research, portfolio management, and trading systems, thereby supporting robust analytics and operational efficiency.

## 三、字段画像汇总

| 维度 | 结果 |
|---|---|
| 字段总数 | **14** |
| 类型分布 | MATRIX×14 |
| 平均覆盖率 | **0.893** |
| 覆盖率区间 | 0.78 ~ 1.00 |
| 更新频率（推断） | 快照（按库表更新，需实测） |
| 可用性评级 | 良（覆盖 70–90%，sub/robust 需关注） |

**覆盖率分档**

| 档 | 字段数 | 占比 |
|---|---:|---:|
| 高 (≥0.90) | 8 | 57.1% |
| 中 (0.70–0.90) | 6 | 42.9% |
| 低 (0.50–0.70) | 0 | 0.0% |
| 稀疏 (<0.50) | 0 | 0.0% |

**历史实测分布（field_profile_perf）**

| 判定 | 字段数 | 占比 |
|---|---:|---:|
| UNTESTED | 14 | 100.0% |

- 该数据集全部字段**尚未实测**（UNTESTED）⇒ 优先做尽

## 四、语义维度地图（自动归类）

| 语义族 | 字段数 | 平均覆盖 | 代表字段 |
|---|---:|---:|---|
| 宏观与行业 | 8 | 0.87 | star_ccr_country_rank、star_ccr_region_rank、star_ccr_sector_rank |
| 风险与质量 | 4 | 0.88 | mdl27_index_rating、star_ccr_global_rank、annual_default_probability_percent |
| 修正与预期 | 2 | 0.98 | star_ccr_implied_rating、star_ccr_combined_pd |

## 五、全字段明细

> 按 `best_sharpe` 降序（未测者置后）。`判定` 来自 `field_profile_perf`：ALIVE=历史测出过 S≥闸线（**不代表可提交**）；UNTESTED=未测；UNUSABLE/DEAD/AXIS_ONLY=已证否或仅可作轴。

| # | 字段名 | 类型 | 覆盖 | 语义族 | 测次 | best_S | best_2Y | best_sub | 判定 | 描述 |
|---:|---|---|---:|---|---:|---:|---:|---:|---|---|
| 1 | `mdl27_index_rating` | MATRIX | 1.000 | 风险与质量 | 0 | — | — | — | UNTESTED | Credit risk rating |
| 2 | `star_ccr_implied_rating` | MATRIX | 1.000 | 修正与预期 | 0 | — | — | — | UNTESTED | Agency-equivalent credit rating implied by the estimated forward 1-year default probability |
| 3 | `star_ccr_combined_pd` | MATRIX | 0.969 | 修正与预期 | 0 | — | — | — | UNTESTED | Estimated 1-year probability of default (0–1) from the StarMine Combined Credit Risk model |
| 4 | `star_ccr_country_rank` | MATRIX | 0.969 | 宏观与行业 | 0 | — | — | — | UNTESTED | Country-level percentile rank (1–100) of the 1-year default probability; higher = safer/lower PD |
| 5 | `star_ccr_global_rank` | MATRIX | 0.969 | 风险与质量 | 0 | — | — | — | UNTESTED | Global percentile rank (1–100) of the 1-year default probability; higher = safer/lower PD |
| 6 | `star_ccr_region_rank` | MATRIX | 0.969 | 宏观与行业 | 0 | — | — | — | UNTESTED | Regional percentile rank (1–100) of the 1-year default probability; higher = safer/lower PD |
| 7 | `star_ccr_sector_rank` | MATRIX | 0.967 | 宏观与行业 | 0 | — | — | — | UNTESTED | Sector-level percentile rank (1–100) of the 1-year default probability; higher = safer/lower PD |
| 8 | `star_ccr_industry_rank` | MATRIX | 0.962 | 宏观与行业 | 0 | — | — | — | UNTESTED | Industry-level percentile rank (1–100) of the 1-year default probability; higher = safer/lower PD |
| 9 | `annual_default_probability_percent` | MATRIX | 0.784 | 风险与质量 | 0 | — | — | — | UNTESTED | 1-year probability of default from CCR expressed as a percentage (0–100) |
| 10 | `country_relative_default_percentile` | MATRIX | 0.784 | 宏观与行业 | 0 | — | — | — | UNTESTED | Country-level 1–100 percentile rank of the 1-year default probability; higher is safer |
| 11 | `global_relative_default_percentile` | MATRIX | 0.784 | 风险与质量 | 0 | — | — | — | UNTESTED | Global percentile rank (1–100) of the 1-year PD; higher means safer or lower PD |
| 12 | `region_relative_default_percentile` | MATRIX | 0.784 | 宏观与行业 | 0 | — | — | — | UNTESTED | Regional percentile rank (1–100) of the 1-year PD; higher means safer or lower PD |
| 13 | `sector_relative_default_percentile` | MATRIX | 0.783 | 宏观与行业 | 0 | — | — | — | UNTESTED | Sector-level 1–100 percentile rank of the 1-year default probability; higher is safer |
| 14 | `industry_relative_default_percentile` | MATRIX | 0.779 | 宏观与行业 | 0 | — | — | — | UNTESTED | Industry-level 1–100 percentile rank of the 1-year default probability; higher is safer |

## 六、本地回测证据

本地库无该数据集的回测记录。

> 说明：`backtest_results` 只收录已持久化的波次（当前 EUR 共 1157 行）；本次会话的直接派发未写库，故此处为空**不代表未做尽**，实测结论见配套战役档案。

## 七、判死记录（sealed dead_end）

无针对本数据集的 `dead_end` 记录。

