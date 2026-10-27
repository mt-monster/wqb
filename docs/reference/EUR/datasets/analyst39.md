# analyst39 — EUR 字段画像

> 自动生成于 2026-10-20 17:55　|　[← 返回索引](README.md)

## 一、数据集元信息

| 项 | 值 |
|---|---|
| 数据集 ID | `analyst39` |
| 名称 | Analyst estimates & financial ratios |
| 类别 | ANALYST |
| 数据字段数(平台) | 24 |
| 覆盖率 | 0.8755 |
| 平台已有 alpha | 546 |
| valueScore | 2.0 |
| 金字塔倍率 | 1.3 |
| 数据类型 | MATRIX |
| delay | 1 |
| 状态 | scanned |

## 二、数据集描述（平台原文）

> ⚠️ 平台目录描述存在**错配**（已实测：insiders1 / imbalance5 的描述指向无关数据集）。以「五、全字段明细」的真实字段语义为准。

This dataset contains detailed point-in-time company financials, standardized ratios, earnings estimates, consensus recommendations, and business intelligence for global equities. It includes annual and interim financial statements, key ratios (such as ROE, ROA, debt-to-equity, margins), analyst estimates, and consensus ratings, as well as company reference data and officer information. The breadth and depth of financial metrics, combined with historical and restated data, allow for robust factor modeling, backtesting, and cross-sectional analysis. Researchers can use this dataset to identify value, growth, quality, and momentum signals, assess earnings surprises, and construct predictive models for price movements based on fundamental drivers and analyst sentiment.

## 三、字段画像汇总

| 维度 | 结果 |
|---|---|
| 字段总数 | **24** |
| 类型分布 | MATRIX×24 |
| 平均覆盖率 | **0.876** |
| 覆盖率区间 | 0.70 ~ 0.92 |
| 更新频率（推断） | 快照（按库表更新，需实测） |
| 可用性评级 | 良（覆盖 70–90%，sub/robust 需关注） |

**覆盖率分档**

| 档 | 字段数 | 占比 |
|---|---:|---:|
| 高 (≥0.90) | 16 | 66.7% |
| 中 (0.70–0.90) | 8 | 33.3% |
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
| 其他 | 12 | 0.91 | anl39_atanbvps、anl39_aepsinclxo、anl39_roxlcxspea |
| 盈利与财务 | 12 | 0.84 | anl39_spvba、anl39_spvbq、anl39_rasv2_atotd2eq |

## 五、全字段明细

> 按 `best_sharpe` 降序（未测者置后）。`判定` 来自 `field_profile_perf`：ALIVE=历史测出过 S≥闸线（**不代表可提交**）；UNTESTED=未测；UNUSABLE/DEAD/AXIS_ONLY=已证否或仅可作轴。

| # | 字段名 | 类型 | 覆盖 | 语义族 | 测次 | best_S | best_2Y | best_sub | 判定 | 描述 |
|---:|---|---|---:|---|---:|---:|---:|---:|---|---|
| 1 | `anl39_atanbvps` | MATRIX | 0.923 | 其他 | 0 | — | — | — | UNTESTED | Book value (tangible) per share - most recent fiscal year |
| 2 | `anl39_spvba` | MATRIX | 0.923 | 盈利与财务 | 0 | — | — | — | UNTESTED | Book value (Common Equity) per share - most recent fiscal year |
| 3 | `anl39_aepsinclxo` | MATRIX | 0.921 | 其他 | 0 | — | — | — | UNTESTED | EPS including extraordinary items - most recent fiscal year |
| 4 | `anl39_roxlcxspea` | MATRIX | 0.921 | 其他 | 0 | — | — | — | UNTESTED | EPS excluding extraordinary items - most recent fiscal year |
| 5 | `anl39_qepsinclxo` | MATRIX | 0.919 | 其他 | 0 | — | — | — | UNTESTED | EPS including extraordinary items - most recent quarter |
| 6 | `anl39_roxlcxspeq` | MATRIX | 0.919 | 其他 | 0 | — | — | — | UNTESTED | EPS excluding extraordinary items - most recent quarter |
| 7 | `anl39_qtanbvps` | MATRIX | 0.917 | 其他 | 0 | — | — | — | UNTESTED | Book value (tangible) per share - most recent quarter |
| 8 | `anl39_spvbq` | MATRIX | 0.917 | 盈利与财务 | 0 | — | — | — | UNTESTED | Book value (Common Equity) per share - most recent quarter |
| 9 | `anl39_ghcspea` | MATRIX | 0.917 | 其他 | 0 | — | — | — | UNTESTED | EPS Change % - year over year |
| 10 | `anl39_ttmepsincx` | MATRIX | 0.914 | 其他 | 0 | — | — | — | UNTESTED | EPS including extraordinary items - trailing 12 month |
| 11 | `anl39_xlcxspemtt` | MATRIX | 0.913 | 其他 | 0 | — | — | — | UNTESTED | EPS excluding extraordinary items - trailing 12 month |
| 12 | `anl39_rasv2_atotd2eq` | MATRIX | 0.912 | 盈利与财务 | 0 | — | — | — | UNTESTED | Total debt to total equity ratio for the most recent fiscal year |
| 13 | `anl39_rygnhcspe` | MATRIX | 0.907 | 其他 | 0 | — | — | — | UNTESTED | EPS Change % - most recent quarter 1 year ago |
| 14 | `anl39_qtotd2eq` | MATRIX | 0.907 | 盈利与财务 | 0 | — | — | — | UNTESTED | Total debt to total equity ratio for the most recent quarter |
| 15 | `anl39_ptmepsincx` | MATRIX | 0.903 | 盈利与财务 | 0 | — | — | — | UNTESTED | Earnings per share including extraordinary items for the prior trailing 12-month period |
| 16 | `anl39_xlcxspemtp` | MATRIX | 0.903 | 盈利与财务 | 0 | — | — | — | UNTESTED | Earnings per share excluding extraordinary items for the prior trailing 12-month period |
| 17 | `anl39_epschngin` | MATRIX | 0.899 | 其他 | 0 | — | — | — | UNTESTED | EPS Change % - prior quarter |
| 18 | `anl39_qtotd2eq2` | MATRIX | 0.895 | 盈利与财务 | 0 | — | — | — | UNTESTED | Total debt/total equity - most recent quarter, 1 year ago |
| 19 | `anl39_ghcspemtt` | MATRIX | 0.892 | 其他 | 0 | — | — | — | UNTESTED | Percent change in EPS, trailing 12 months versus the prior trailing 12 months |
| 20 | `anl39_agrosmgn` | MATRIX | 0.769 | 盈利与财务 | 0 | — | — | — | UNTESTED | Gross Margin - 1st historical fiscal year |
| 21 | `anl39_agrosmgn2` | MATRIX | 0.768 | 盈利与财务 | 0 | — | — | — | UNTESTED | Gross Margin - 2nd historical fiscal year |
| 22 | `anl39_qgrosmgn` | MATRIX | 0.725 | 盈利与财务 | 0 | — | — | — | UNTESTED | Gross Margin - most recent quarter |
| 23 | `anl39_ttmgrosmgn` | MATRIX | 0.724 | 盈利与财务 | 0 | — | — | — | UNTESTED | Gross Margin - trailing 12 month |
| 24 | `anl39_grosmgn5yr` | MATRIX | 0.702 | 盈利与财务 | 0 | — | — | — | UNTESTED | Gross Margin 5-year average |

## 六、本地回测证据

本地库无该数据集的回测记录。

> 说明：`backtest_results` 只收录已持久化的波次（当前 EUR 共 1157 行）；本次会话的直接派发未写库，故此处为空**不代表未做尽**，实测结论见配套战役档案。

## 七、判死记录（sealed dead_end）

- `EUR-ANL39-EPS-GM-BOOK-WEAK`（2026-08-25）family=analyst39 EPS/margin/book residual x v_rev/wedge：{"best": {"alpha": "6Xlwe9bP", "fitness": 0.41, "sharpe": 0.88}, "reason": "Wave62 seven analyst39 slows (YoY EPS/FY-Q EPS/ex-XO/GM/book/TTM/prior-Q change) x v_rev/wedge. Max S0.88. Differentiated but far from cheap gate. Do not Mode A leftover overlapping GM/book fields.", "rule": "Do not reuse analyst39 EPS/margin/book residuals as 0.30 slow legs with v_rev/falling_wedge.", "wave": 62}
- `EUR-ANALYST39-FAST-RECIPE-DEAD`（2026-10-19）family=analyst39：{"acceleration_leg": "ts_delta(anl39_ghcspemtt, 60) → S 0.09（全批最差）⇒ 「变动」再取变动在 EUR 是纯噪声。", "batch": "1e3zWtfA64HqcFSOP51tcOH", "best": {"alpha": "9qE7arG1", "failed_ra": 3, "field": "anl39_rygnhcspe", "fitness": 0.73, "sharpe": 1.21, "sub": 0.44, "sub_limit": 0.63, "two_year_sharpe": 1.8}, "coverage": 0.8755, "dataset": "analyst39", "date": "2026-10-19", "decision_table": "D15", "family": "analyst3

