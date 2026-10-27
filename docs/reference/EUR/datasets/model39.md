# model39 — EUR 字段画像

> 自动生成于 2026-10-20 17:55　|　[← 返回索引](README.md)

## 一、数据集元信息

| 项 | 值 |
|---|---|
| 数据集 ID | `model39` |
| 名称 | Valuation Momentum Data |
| 类别 | MODEL |
| 数据字段数(平台) | 24 |
| 覆盖率 | 0.8044 |
| 平台已有 alpha | 472 |
| valueScore | 1.0 |
| 金字塔倍率 | 1.3 |
| 数据类型 | — |
| delay | 1 |
| 状态 | — |

## 二、数据集描述（平台原文）

> ⚠️ 平台目录描述存在**错配**（已实测：insiders1 / imbalance5 的描述指向无关数据集）。以「五、全字段明细」的真实字段语义为准。

This dataset integrates two advanced quantitative models: an earnings quality model that ranks stocks based on the sustainability and reliability of their reported earnings, and an analyst revisions model that tracks changes in analyst sentiment and estimate revisions. The earnings quality component uses a multi-factor approach, considering accruals, cash flow, operating efficiency, and exclusions to assess the likelihood that a company's earnings will persist. The analyst revisions component evaluates the direction and magnitude of recent analyst estimate changes, which have historically been strong predictors of future price movements. By combining these perspectives, the dataset provides percentile rankings (1-100) for stocks globally, enabling investors to identify companies with both 

## 三、字段画像汇总

| 维度 | 结果 |
|---|---|
| 字段总数 | **24** |
| 类型分布 | MATRIX×24 |
| 平均覆盖率 | **0.804** |
| 覆盖率区间 | 0.77 ~ 0.86 |
| 更新频率（推断） | 快照（按库表更新，需实测） |
| 可用性评级 | 良（覆盖 70–90%，sub/robust 需关注） |

**覆盖率分档**

| 档 | 字段数 | 占比 |
|---|---:|---:|
| 高 (≥0.90) | 0 | 0.0% |
| 中 (0.70–0.90) | 24 | 100.0% |
| 低 (0.50–0.70) | 0 | 0.0% |
| 稀疏 (<0.50) | 0 | 0.0% |

**历史实测分布（field_profile_perf）**

| 判定 | 字段数 | 占比 |
|---|---:|---:|
| UNTESTED | 24 | 100.0% |

- 该数据集全部字段**尚未实测**（UNTESTED）⇒ 优先做尽

## 四、语义维度地图（自动归类）

| 语义族 | 字段数 | 平均覆盖 | 代表字段 |
|---|---:|---:|---|
| 价量与波动 | 20 | 0.79 | mdl39_d1_price_mo_industry_component、mdl39_d1_price_mo_short_term_component、mdl39_d1_price_mo_mid_term_component |
| 宏观与行业 | 3 | 0.85 | mdl39_d1_val_mo_region_rank、mdl39_d1_val_mo_sector_rank、mdl39_d1_val_mo_industry_rank |
| 风险与质量 | 1 | 0.85 | mdl39_d1_val_mo_global_rank |

## 五、全字段明细

> 按 `best_sharpe` 降序（未测者置后）。`判定` 来自 `field_profile_perf`：ALIVE=历史测出过 S≥闸线（**不代表可提交**）；UNTESTED=未测；UNUSABLE/DEAD/AXIS_ONLY=已证否或仅可作轴。

| # | 字段名 | 类型 | 覆盖 | 语义族 | 测次 | best_S | best_2Y | best_sub | 判定 | 描述 |
|---:|---|---|---:|---|---:|---:|---:|---:|---|---|
| 1 | `mdl39_d1_price_mo_industry_component` | MATRIX | 0.857 | 价量与波动 | 0 | — | — | — | UNTESTED | Global 1-100 ranking of the Industry Price Momentum Component of the Price Mo model |
| 2 | `mdl39_d1_val_mo_global_rank` | MATRIX | 0.854 | 风险与质量 | 0 | — | — | — | UNTESTED | Global-relative 1-100 ranking of the Val-Mo model |
| 3 | `mdl39_d1_val_mo_region_rank` | MATRIX | 0.854 | 宏观与行业 | 0 | — | — | — | UNTESTED | Region-relative 1-100 ranking of the Val-Mo model |
| 4 | `mdl39_d1_val_mo_sector_rank` | MATRIX | 0.854 | 宏观与行业 | 0 | — | — | — | UNTESTED | Sector-relative 1-100 ranking of the Val-Mo model |
| 5 | `mdl39_d1_price_mo_short_term_component` | MATRIX | 0.852 | 价量与波动 | 0 | — | — | — | UNTESTED | Global 1-100 ranking of the Short-Term Price Momentum Component of the Price Mo model |
| 6 | `mdl39_d1_price_mo_mid_term_component` | MATRIX | 0.848 | 价量与波动 | 0 | — | — | — | UNTESTED | Global 1-100 ranking of the Mid-Term Price Momentum Component of the Price Mo model |
| 7 | `mdl39_d1_val_mo_industry_rank` | MATRIX | 0.847 | 宏观与行业 | 0 | — | — | — | UNTESTED | Industry-relative 1-100 ranking of the Val-Mo model |
| 8 | `mdl39_d1_price_mo_long_term_component` | MATRIX | 0.832 | 价量与波动 | 0 | — | — | — | UNTESTED | Global 1-100 ranking of the Long-Term Price Momentum Component of the Price Mo model |
| 9 | `mdl39_d1_price_mo_global_rank` | MATRIX | 0.832 | 价量与波动 | 0 | — | — | — | UNTESTED | Global-relative 1-100 ranking of the Price Mo model |
| 10 | `mdl39_d1_price_mo_region_rank` | MATRIX | 0.832 | 价量与波动 | 0 | — | — | — | UNTESTED | Region-relative 1-100 ranking of the Price Mo model |
| 11 | `short_term_price_momentum_score_2` | MATRIX | 0.782 | 价量与波动 | 0 | — | — | — | UNTESTED | A percentile rank reflecting only the short term aspect of the Price Momentum Model; scores of 100 indicate the highest rated stocks and 1 t |
| 12 | `industry_price_momentum_score_2` | MATRIX | 0.782 | 价量与波动 | 0 | — | — | — | UNTESTED | A percentile rank reflecting only the industry aspect of the Price Momentum Model; scores of 100 indicate the highest rated stocks and 1 the |
| 13 | `mid_term_price_momentum_score_2` | MATRIX | 0.781 | 价量与波动 | 0 | — | — | — | UNTESTED | A percentile rank reflecting only the mid term aspect of the Price Momentum Model; scores of 100 indicate the highest rated stocks and 1 the |
| 14 | `global_value_momentum_rank` | MATRIX | 0.777 | 价量与波动 | 0 | — | — | — | UNTESTED | The current global 1-100 percentile rank of the security based on the Value-Momentum Model |
| 15 | `global_value_momentum_rank_float` | MATRIX | 0.777 | 价量与波动 | 0 | — | — | — | UNTESTED | Float (non-integer) value of the global 1-100 percentile rank for the Value-Momentum Model |
| 16 | `region_value_momentum_rank` | MATRIX | 0.777 | 价量与波动 | 0 | — | — | — | UNTESTED | The current regional 1-100 percentile rank of the security based on the Value-Momentum Model |
| 17 | `region_value_momentum_rank_float` | MATRIX | 0.777 | 价量与波动 | 0 | — | — | — | UNTESTED | Float (non-integer) value of the regional 1-100 percentile rank for the Value-Momentum Model |
| 18 | `sector_value_momentum_rank` | MATRIX | 0.777 | 价量与波动 | 0 | — | — | — | UNTESTED | The current sector 1-100 percentile rank of the security based on the Value-Momentum Model |
| 19 | `sector_value_momentum_rank_float` | MATRIX | 0.777 | 价量与波动 | 0 | — | — | — | UNTESTED | Float (non-integer) value of the sector 1-100 percentile rank for the Value-Momentum Model |
| 20 | `industry_value_momentum_rank` | MATRIX | 0.768 | 价量与波动 | 0 | — | — | — | UNTESTED | The current industry 1-100 percentile rank of the security based on the Value-Momentum Model |
| 21 | `industry_value_momentum_rank_float` | MATRIX | 0.768 | 价量与波动 | 0 | — | — | — | UNTESTED | Float (non-integer) value of the industry 1-100 percentile rank for the Value-Momentum Model |
| 22 | `long_term_price_momentum_score_2` | MATRIX | 0.767 | 价量与波动 | 0 | — | — | — | UNTESTED | A percentile rank reflecting only the long term aspect of the Price Momentum Model; scores of 100 indicate the highest rated stocks and 1 th |
| 23 | `global_price_momentum_percentile_2` | MATRIX | 0.767 | 价量与波动 | 0 | — | — | — | UNTESTED | The current global 1-100 percentile rank of the security based on the Price Momentum Model |
| 24 | `regional_price_momentum_percentile_2` | MATRIX | 0.767 | 价量与波动 | 0 | — | — | — | UNTESTED | The current regional 1-100 percentile rank of the security based on the Price Momentum Model |

## 六、本地回测证据

本地库无该数据集的回测记录。

> 说明：`backtest_results` 只收录已持久化的波次（当前 EUR 共 1157 行）；本次会话的直接派发未写库，故此处为空**不代表未做尽**，实测结论见配套战役档案。

## 七、判死记录（sealed dead_end）

无针对本数据集的 `dead_end` 记录。

