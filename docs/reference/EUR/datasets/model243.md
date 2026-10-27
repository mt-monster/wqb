# model243 — EUR 字段画像

> 自动生成于 2026-10-20 17:55　|　[← 返回索引](README.md)

## 一、数据集元信息

| 项 | 值 |
|---|---|
| 数据集 ID | `model243` |
| 名称 | Combined Alpha Model |
| 类别 | MODEL |
| 数据字段数(平台) | 4 |
| 覆盖率 | 0.7494 |
| 平台已有 alpha | 202 |
| valueScore | 2.0 |
| 金字塔倍率 | 1.3 |
| 数据类型 | — |
| delay | 1 |
| 状态 | — |

## 二、数据集描述（平台原文）

> ⚠️ 平台目录描述存在**错配**（已实测：insiders1 / imbalance5 的描述指向无关数据集）。以「五、全字段明细」的真实字段语义为准。

This dataset provides quantitative scores and ranks for equities based on a static, region-optimized combination of multiple alpha models, including analyst revisions, price momentum, relative and intrinsic valuation, earnings quality, institutional holdings, insider activity, and short interest. Each security is ranked within its region, country, sector, and industry, enabling cross-sectional analysis and factor diversification. The dataset includes historical scores, mapping files for identifier cross-referencing, and supports backtesting and portfolio construction. By aggregating diverse predictive signals, it helps investors identify bullish and bearish opportunities, optimize long-short strategies, and improve the robustness of price movement forecasts across global markets.

## 三、字段画像汇总

| 维度 | 结果 |
|---|---|
| 字段总数 | **4** |
| 类型分布 | VECTOR×4 |
| 平均覆盖率 | **0.749** |
| 覆盖率区间 | 0.75 ~ 0.75 |
| 更新频率（推断） | 事件/逐笔型（VECTOR） |
| 可用性评级 | 良（覆盖 70–90%，sub/robust 需关注） |

**覆盖率分档**

| 档 | 字段数 | 占比 |
|---|---:|---:|
| 高 (≥0.90) | 0 | 0.0% |
| 中 (0.70–0.90) | 4 | 100.0% |
| 低 (0.50–0.70) | 0 | 0.0% |
| 稀疏 (<0.50) | 0 | 0.0% |

**历史实测分布（field_profile_perf）**

| 判定 | 字段数 | 占比 |
|---|---:|---:|
| UNTESTED | 4 | 100.0% |

- 该数据集全部字段**尚未实测**（UNTESTED）⇒ 优先做尽

## 四、语义维度地图（自动归类）

| 语义族 | 字段数 | 平均覆盖 | 代表字段 |
|---|---:|---:|---|
| 宏观与行业 | 4 | 0.75 | mdl243_country_rank、mdl243_industry_rank、mdl243_region_rank |

## 五、全字段明细

> 按 `best_sharpe` 降序（未测者置后）。`判定` 来自 `field_profile_perf`：ALIVE=历史测出过 S≥闸线（**不代表可提交**）；UNTESTED=未测；UNUSABLE/DEAD/AXIS_ONLY=已证否或仅可作轴。

| # | 字段名 | 类型 | 覆盖 | 语义族 | 测次 | best_S | best_2Y | best_sub | 判定 | 描述 |
|---:|---|---|---:|---|---:|---:|---:|---:|---|---|
| 1 | `mdl243_country_rank` | VECTOR | 0.749 | 宏观与行业 | 0 | — | — | — | UNTESTED | Combined Alpha Model Country Rank. A 1-100 rank, relative to other firms in the same country, representing the StarMine Combined Alpha Model |
| 2 | `mdl243_industry_rank` | VECTOR | 0.749 | 宏观与行业 | 0 | — | — | — | UNTESTED | Combined Alpha Model Industry Rank. A 1-100 rank, relative to other firms in the same region and TRBC industry group. There are approximatel |
| 3 | `mdl243_region_rank` | VECTOR | 0.749 | 宏观与行业 | 0 | — | — | — | UNTESTED | Combined Alpha Model Region Rank; A 1-100 rank, relative to other firms in the same region, representing the StarMine Combined Alpha Model s |
| 4 | `mdl243_sector_rank` | VECTOR | 0.749 | 宏观与行业 | 0 | — | — | — | UNTESTED | Combined Alpha Model Sector Rank. A 1-100 rank, relative to other firms in the same region and TRBC economic sector. There are ten TRBC econ |

## 六、本地回测证据

本地库无该数据集的回测记录。

> 说明：`backtest_results` 只收录已持久化的波次（当前 EUR 共 1157 行）；本次会话的直接派发未写库，故此处为空**不代表未做尽**，实测结论见配套战役档案。

## 七、判死记录（sealed dead_end）

无针对本数据集的 `dead_end` 记录。

