# EUR / pv106（买卖价差与交易成本）全字段画像（2026-11-20）

> 平台实查 `get_datafields(dataset_id=pv106, region=EUR, universe=TOP2500, delay=1)`：**15/15 字段，complete=True**（全部 MATRIX）。
> 类别 pv ⇒ EUR/D1/**PV 塔 2/3（差 1 席）**；mult 1.1；**cov 1.0（全覆盖 ⇒ 历史长）**；**aC 8–102（冷门）**；2022-09 老代 + 2025-11 新代。
> 命名规则 `eur_<category>_<dataset>_profile_<YYYYMMDD>.md`。**PV 类按用户红线不得两两组腿 ⇒ 本集只能单集 ATOM。**

## 1. 字段结构总览（4 语义族）

| 语义族 | 字段数 | 说明 |
|---|---:|---|
| 价差（bp 归一） | 2 | `pv106_spreadbp` / `pv106_lastspreadbp`——**最干净的流动性度量** |
| 价差（绝对币值） | 3 | `pv106_spread` / `pv106_lastspread` / `bid_ask_price_gap` / `price_difference_bid_ask` |
| 交易成本 | 5 | 中位数/10/25 分位/最大/估计——含规模效应（与市值相关） |
| 滑点 | 4 | `aggregated_slippage_metric` / `average_spread_slippage` / `slippage_at_spread_35` / `slippage_commission_2025` |

## 字段全表（15 字段逐字段平台读数，cov 均 1.0）

| 字段 | 类型 | cov | uC | aC | 语义族 | 说明 |
|---|---|---:|---:|---:|---|---|
| `pv106_lastspreadbp` | MATRIX | 0.65 | 102 | 102 | 价差bp(30分) | 最近 30 分钟买卖价差（bp） |
| `pv106_spreadbp` | MATRIX | 0.71 | 95 | 95 | 价差bp | 买卖价差（bp，按 mid/VWAP 归一） |
| `pv106_lastspread` | MATRIX | 0.47 | 68 | 68 | 价差(币) | 最近 30 分钟买卖价差均值（计价货币） |
| `pv106_spread` | MATRIX | 0.39 | 65 | 65 | 价差(币) | 最优买价与最优卖价之差（计价货币） |
| `bid_ask_price_gap` | MATRIX | 0.32 | 48 | 48 | 价差(币) | 最优买卖价差 |
| `aggregated_slippage_metric` | MATRIX | 0.25 | 30 | 30 | 滑点 | 跨多笔交易/多场所的综合滑点 |
| `transaction_cost_percentile_25` | MATRIX | 0.2 | 29 | 29 | 交易成本 | 交易成本 25 分位 |
| `transaction_cost_median` | MATRIX | 0.23 | 26 | 26 | 交易成本 | 交易成本中位数 |
| `transaction_cost_percentile_10` | MATRIX | 0.17 | 24 | 24 | 交易成本 | 交易成本 10 分位 |
| `average_spread_slippage` | MATRIX | 0.19 | 20 | 20 | 滑点 | 归因于跨价差的滑点部分 |
| `price_difference_bid_ask` | MATRIX | 0.16 | 19 | 19 | 价差 | 买卖价差（描述缺失） |
| `transaction_cost_estimate` | MATRIX | 0.14 | 18 | 18 | 交易成本 | 交易成本估计 |
| `slippage_at_spread_35` | MATRIX | 0.13 | 13 | 13 | 滑点 | 按 35% 日均量下单的建模滑点 |
| `slippage_commission_2025` | MATRIX | 0.13 | 13 | 13 | 滑点 | 2025 年滑点+佣金 |
| `transaction_cost_maximum` | MATRIX | 0.08 | 8 | 8 | 交易成本 | 交易成本最大值 |

## 2. 六维画像

- **类型**：15/15 全 MATRIX（无需 vec_* 降维）。
- **覆盖率**：**cov 1.0（全覆盖）** ⇒ 数据从起点即有 ⇒ **历史长度无虞**（与 macro27/investor_activity 的数据层短板相反）。
- **更新频率**：日频（盘后快照 + 30 分钟窗口）。
- **分布特征**：价差 bp 为右偏正值（小盘股价差大）；交易成本类含规模成分（与市值/成交额相关）⇒ **须与规模中性化搭配或用 bp 归一口径**。
- **可用性**：**aC 8–102（冷门）**（对照 pv1 的 44048）⇒ prod 友好候选；信息源 = 微观结构执行成本，**与生产池的价量/分析师/情绪因子重叠度低**。
- **适用性**：主信号 = **`pv106_spreadbp`（bp 归一价差）**；辅助 = 30 分钟价差（盘中流动性冲击）；排除 = 绝对币值与交易成本绝对水平（含规模成分）。

## 3. 机制假设（三路证据后）

- **论文**（12 篇/7 作者，多样闸 PASS）：*Illiquidity and Stock Returns: Cross-section and Time-series Effects*（Amihud, RFS 2002）、
  *Illiquidity and Stock Returns II*（RFS 2020）、*Sell-Order Illiquidity and the Cross-Section of Expected Stock Returns*（2012）、
  *Illiquidity and the Cross-Section of International Stock Returns*（2020）
  ⇒ **流动性溢价**：横截面上高非流动性（高买卖价差）⇒ 预期收益更高（Amihud 溢价），且时序上非流动性冲击与负收益相关。
- **论坛**：本会话未取该集专帖（aC 低）。
- **两支机制**：
  ① **流动性溢价（横截面）**：bp 价差高 ⇒ 流动性差 ⇒ 要求更高回报 ⇒ 后续收益高（正向）；
  ② **流动性冲击（时序）**：价差**变宽** ⇒ 交易成本急升 ⇒ 未来收益下行（负向动量）⇒ 价差变化的负号方向。

## 4. TemplatePlan（每字段族一行）

| 字段族 | 合法模板 | 排除 | 依据 |
|---|---|---|---|
| 价差 bp | `group_rank(ts_zscore(ts_backfill(pv106_spreadbp,22),252),industry)`（正向 + **反向**各一） | 裸 rank | 论文① |
| 30 分钟价差 bp | `pv106_lastspreadbp` 同构；`ts_delta` 取变化（动量方向） | 裸 rank | 论文② |
| 交易成本 | 只用**分位/中位数**字段，且须 `group_neutralize` 掉规模 | 绝对水平（规模代理） | 论文① |
| 滑点 | `aggregated_slippage_metric` / `slippage_at_spread_35`（执行成本与容量） | 裸 rank | 机制② |

## 5. 探针计划（8 臂，preflight 全过）

价差 bp 水平 2（含反向）+ 30 分钟价差 1 + 交易成本 1 + 滑点 2 + 价差变化 1 + 滑点@35% 1。
**判据**：cov 1.0 ⇒ 非稀疏型 ⇒ **presence 门控不适用**（按「cov<0.6 才试门控」判据）；
内核为**右偏正值** ⇒ 外层 `group_rank` 与 `group_zscore` 都试（后者可能降 prod）。
