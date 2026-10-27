# risk68 — EUR 字段画像

> 自动生成于 2026-10-20 17:55　|　[← 返回索引](README.md)

## 一、数据集元信息

| 项 | 值 |
|---|---|
| 数据集 ID | `risk68` |
| 名称 | Forecast Data |
| 类别 | RISK |
| 数据字段数(平台) | 5 |
| 覆盖率 | 1.0 |
| 平台已有 alpha | 193 |
| valueScore | 1.0 |
| 金字塔倍率 | 1.0 |
| 数据类型 | — |
| delay | 1 |
| 状态 | — |

## 二、数据集描述（平台原文）

> ⚠️ 平台目录描述存在**错配**（已实测：insiders1 / imbalance5 的描述指向无关数据集）。以「五、全字段明细」的真实字段语义为准。

This dataset delivers full order book and top of book tick-level statistics for global markets, including bid and ask levels, sizes, order updates, trade prices, volumes, and interval-based metrics. It aggregates and computes advanced measures such as average distances from mid, size distributions, and volatility at various intervals. By analyzing these detailed order book dynamics and trade flows, users can detect liquidity imbalances, order flow trends, and microstructure effects, which are instrumental in forecasting short-term price movements and understanding market behavior at a granular level.

## 三、字段画像汇总

| 维度 | 结果 |
|---|---|
| 字段总数 | **5** |
| 类型分布 | MATRIX×5 |
| 平均覆盖率 | **1.000** |
| 覆盖率区间 | 1.00 ~ 1.00 |
| 更新频率（推断） | 日频 |
| 可用性评级 | 优（覆盖 ≥90%，可直接做尽） |

**覆盖率分档**

| 档 | 字段数 | 占比 |
|---|---:|---:|
| 高 (≥0.90) | 5 | 100.0% |
| 中 (0.70–0.90) | 0 | 0.0% |
| 低 (0.50–0.70) | 0 | 0.0% |
| 稀疏 (<0.50) | 0 | 0.0% |

**历史实测分布（field_profile_perf）**

| 判定 | 字段数 | 占比 |
|---|---:|---:|
| UNTESTED | 5 | 100.0% |

- 该数据集全部字段**尚未实测**（UNTESTED）⇒ 优先做尽

## 四、语义维度地图（自动归类）

| 语义族 | 字段数 | 平均覆盖 | 代表字段 |
|---|---:|---:|---|
| 修正与预期 | 2 | 1.00 | rsk68_beta、rsk68_weight_volatility_short |
| 价量与波动 | 2 | 1.00 | rsk68_weight_dadv、rsk68_weight_edadv |
| 盈利与财务 | 1 | 1.00 | rsk68_residual_return |

## 五、全字段明细

> 按 `best_sharpe` 降序（未测者置后）。`判定` 来自 `field_profile_perf`：ALIVE=历史测出过 S≥闸线（**不代表可提交**）；UNTESTED=未测；UNUSABLE/DEAD/AXIS_ONLY=已证否或仅可作轴。

| # | 字段名 | 类型 | 覆盖 | 语义族 | 测次 | best_S | best_2Y | best_sub | 判定 | 描述 |
|---:|---|---|---:|---|---:|---:|---:|---:|---|---|
| 1 | `rsk68_beta` | MATRIX | 1.000 | 修正与预期 | 0 | — | — | — | UNTESTED | Unitless stock beta for a European asset relative to the regional liquidity-weighted market_return, typically estimated over a long rolling  |
| 2 | `rsk68_residual_return` | MATRIX | 1.000 | 盈利与财务 | 0 | — | — | — | UNTESTED | Idiosyncratic 1-day return for a European asset unexplained by the market factor, computed as actual return minus beta times market_return,  |
| 3 | `rsk68_weight_dadv` | MATRIX | 1.000 | 价量与波动 | 0 | — | — | — | UNTESTED | Simple moving average dollar average daily trading volume for European instruments, used as a liquidity weight (dollar units) |
| 4 | `rsk68_weight_edadv` | MATRIX | 1.000 | 价量与波动 | 0 | — | — | — | UNTESTED | Exponentially decayed dollar average daily trading volume for European instruments, used as a liquidity weight (dollar units) |
| 5 | `rsk68_weight_volatility_short` | MATRIX | 1.000 | 修正与预期 | 0 | — | — | — | UNTESTED | Short-term volatility estimate for European instruments, expressed in decimal terms |

## 六、本地回测证据

本地库无该数据集的回测记录。

> 说明：`backtest_results` 只收录已持久化的波次（当前 EUR 共 1157 行）；本次会话的直接派发未写库，故此处为空**不代表未做尽**，实测结论见配套战役档案。

## 七、判死记录（sealed dead_end）

- `EUR-RISK72-RESIDUAL-RETURN-WEAK`（2026-09-23T18:17:24）family=risk72 equity_residualized_return 残差族（cfg2/ecs/ats × top1200/top2500 残差价差）：{"family": "risk72 equity_residualized_return 残差族（cfg2/ecs/ats × top1200/top2500 残差价差）", "reason": "wave230 8 探针全灭：best sharpe 0.91 / fitness 0.48，2Y 1.65 但 LOW_ROBUST_UNIVERSE_SHARPE；未达 Mode B 资格线 1.25（D4）→ 判死。2 条 group_cartesian_product/group_count 单位错误被自动隔离。RISK 塔剩余候选：risk68(fields=5 仅条件腿)/risk62(crowded 10665) 均不进白名单。", "source": "registry_dead_end", "salvage": {"alpha_ids": [], "count": 0, "s

