# pv1 — EUR 字段画像

> 自动生成于 2026-10-20 17:55　|　[← 返回索引](README.md)

## 一、数据集元信息

| 项 | 值 |
|---|---|
| 数据集 ID | `pv1` |
| 名称 | Price Volume Data for Equity |
| 类别 | PV |
| 数据字段数(平台) | 24 |
| 覆盖率 | 1.0 |
| 平台已有 alpha | 44048 |
| valueScore | 1.0 |
| 金字塔倍率 | 1.1 |
| 数据类型 | — |
| delay | 1 |
| 状态 | — |

## 二、数据集描述（平台原文）

> ⚠️ 平台目录描述存在**错配**（已实测：insiders1 / imbalance5 的描述指向无关数据集）。以「五、全字段明细」的真实字段语义为准。

The dataset contains financial data related to equities, including metrics such as prices (open, high, low, close), trading volumes, market capitalization, returns, dividends, splits, and other key indicators that provide insights into stock performance and market activity.

## 三、字段画像汇总

| 维度 | 结果 |
|---|---|
| 字段总数 | **24** |
| 类型分布 | MATRIX×13　GROUP×7　SYMBOL×4 |
| 平均覆盖率 | **1.000** |
| 覆盖率区间 | 1.00 ~ 1.00 |
| 更新频率（推断） | 快照（按库表更新，需实测） |
| 可用性评级 | 优（覆盖 ≥90%，可直接做尽） |

**覆盖率分档**

| 档 | 字段数 | 占比 |
|---|---:|---:|
| 高 (≥0.90) | 24 | 100.0% |
| 中 (0.70–0.90) | 0 | 0.0% |
| 低 (0.50–0.70) | 0 | 0.0% |
| 稀疏 (<0.50) | 0 | 0.0% |

**历史实测分布（field_profile_perf）**

| 判定 | 字段数 | 占比 |
|---|---:|---:|
| UNTESTED | 17 | 70.8% |
| AXIS_ONLY | 7 | 29.2% |

- 无带 `n_tests>0` 的有效实测记录；但历史判定已存在（UNTESTED 17 / UNUSABLE 0 等）。⚠ 历史判定可能**过时**（如 analyst7 的旧判死已作废），做尽前须重跑。

## 四、语义维度地图（自动归类）

| 语义族 | 字段数 | 平均覆盖 | 代表字段 |
|---|---:|---:|---|
| 价量与波动 | 8 | 1.00 | adv20、close、high |
| 其他 | 5 | 1.00 | cap、exchange、market |
| 宏观与行业 | 5 | 1.00 | country、currency、industry |
| 元数据与非信号 | 3 | 1.00 | cusip、isin、sedol |
| 盈利与财务 | 2 | 1.00 | adjfactor、dividend |
| 交易与微观结构 | 1 | 1.00 | ticker |

## 五、全字段明细

> 按 `best_sharpe` 降序（未测者置后）。`判定` 来自 `field_profile_perf`：ALIVE=历史测出过 S≥闸线（**不代表可提交**）；UNTESTED=未测；UNUSABLE/DEAD/AXIS_ONLY=已证否或仅可作轴。

| # | 字段名 | 类型 | 覆盖 | 语义族 | 测次 | best_S | best_2Y | best_sub | 判定 | 描述 |
|---:|---|---|---:|---|---:|---:|---:|---:|---|---|
| 1 | `adjfactor` | MATRIX | 1.000 | 盈利与财务 | 0 | — | — | — | UNTESTED | Adjustment factor applied to historical prices and dividends to account for splits and other corporate actions |
| 2 | `adv20` | MATRIX | 1.000 | 价量与波动 | 0 | — | — | — | UNTESTED | Average daily volume in past 20 days |
| 3 | `cap` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | Daily market capitalization (in millions) |
| 4 | `close` | MATRIX | 1.000 | 价量与波动 | 0 | — | — | — | UNTESTED | Daily close price |
| 5 | `country` | GROUP | 1.000 | 宏观与行业 | 0 | — | — | — | AXIS_ONLY | Country grouping |
| 6 | `currency` | GROUP | 1.000 | 宏观与行业 | 0 | — | — | — | AXIS_ONLY | Currency |
| 7 | `cusip` | SYMBOL | 1.000 | 元数据与非信号 | 0 | — | — | — | UNTESTED | CUSIP Value |
| 8 | `dividend` | MATRIX | 1.000 | 盈利与财务 | 0 | — | — | — | UNTESTED | Dividend |
| 9 | `exchange` | GROUP | 1.000 | 其他 | 0 | — | — | — | AXIS_ONLY | Exchange grouping |
| 10 | `high` | MATRIX | 1.000 | 价量与波动 | 0 | — | — | — | UNTESTED | Daily high price |
| 11 | `industry` | GROUP | 1.000 | 宏观与行业 | 0 | — | — | — | AXIS_ONLY | Industry grouping |
| 12 | `isin` | SYMBOL | 1.000 | 元数据与非信号 | 0 | — | — | — | UNTESTED | ISIN Value |
| 13 | `low` | MATRIX | 1.000 | 价量与波动 | 0 | — | — | — | UNTESTED | Daily low price |
| 14 | `market` | GROUP | 1.000 | 其他 | 0 | — | — | — | AXIS_ONLY | Market grouping |
| 15 | `open` | MATRIX | 1.000 | 价量与波动 | 0 | — | — | — | UNTESTED | Daily open price |
| 16 | `returns` | MATRIX | 1.000 | 价量与波动 | 0 | — | — | — | UNTESTED | Daily returns |
| 17 | `sector` | GROUP | 1.000 | 宏观与行业 | 0 | — | — | — | AXIS_ONLY | Sector grouping |
| 18 | `sedol` | SYMBOL | 1.000 | 元数据与非信号 | 0 | — | — | — | UNTESTED | Sedol |
| 19 | `sharesout` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | Daily outstanding shares (in millions) |
| 20 | `split` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | Stock split ratio |
| 21 | `subindustry` | GROUP | 1.000 | 宏观与行业 | 0 | — | — | — | AXIS_ONLY | Subindustry grouping |
| 22 | `ticker` | SYMBOL | 1.000 | 交易与微观结构 | 0 | — | — | — | UNTESTED | Ticker |
| 23 | `volume` | MATRIX | 1.000 | 价量与波动 | 0 | — | — | — | UNTESTED | Daily volume |
| 24 | `vwap` | MATRIX | 1.000 | 价量与波动 | 0 | — | — | — | UNTESTED | Daily volume weighted average price |

## 六、本地回测证据

本地库无该数据集的回测记录。

> 说明：`backtest_results` 只收录已持久化的波次（当前 EUR 共 1157 行）；本次会话的直接派发未写库，故此处为空**不代表未做尽**，实测结论见配套战役档案。

## 七、判死记录（sealed dead_end）

- `EUR-UNTESTED-CHANNEL-FIRSTPROBE-DEAD`（2026-10-02）family=EUR 未测数据集通道（pv106 PV价差 / model50 MODEL估值）：{"id": "EUR-UNTESTED-CHANNEL-FIRSTPROBE-DEAD", "family": "EUR 未测数据集通道（pv106 PV价差 / model50 MODEL估值）", "reason": "2026-10-02 实测：经 S0-tier ∩ TRI ∩ 未测 ∩ 非判死 四重筛选后，EUR 仅剩 pv106 与 model50 两个真空白候选。首波 pv106 11 式 max/S/=0.70、model50 23 式 max/S/=0.80（骨架含 group_rank/group_zscore/ts_zscore/价差对/门控），全 LOW_SHARPE+LOW_FITNESS，candidates=0。与 eur_unlit_tower_strategic_closure 的 Fitness_upper=Sharpe×sqrt(returns/0.

