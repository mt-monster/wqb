# S0 · KOR 全类别数据集扫描与选定（2026-11-15）

> 判据优先级：① 金字塔未点亮（平台 `get_pyramid_alphas` 实读，2026-11-15）；
> ② 类别内存在 `failed_ra_count=0` 的现成件（本地库 + 平台 `batch_get_alpha_metrics` 复验）；
> ③ 该信息源在 OS 池中的占比（决定 prod 是否还有白空间）。
> ⚠ 本文件的「本地 N 条」**只是 evidence channel 之一**：MCP 直连仿真不写 `expressions` 表，
> 所以 `local=0` ≠ 没挖过（AGENTS §8.11 ⑦ 的盲区纪律）。

## 1. 点亮态（平台实读，2026-11-15）

| 塔 | 已点亮 | 乘数 | 本轮可用性 |
|---|---|---|---|
| analyst | 4 | 1.6 | ⛔ 已点亮 |
| fundamental | 3 | 1.6 | ⛔ 已点亮（满） |
| model | 3 | 1.6 | ⛔ 已点亮（满） |
| risk | 3 | 1.3 | ⛔ 已点亮（2026-11-06 时还是 0，10 天内点亮；路线图 §0 已过期） |
| shortinterest | 4 | 1.4 | ⛔ 已点亮 |
| **pv** | **2** | 1.4 | ✅ 差 1 颗点亮 |
| **insiders** | **1** | 1.2 | ✅ 主攻 |
| **other** | 1 | 1.6 | ✅ 旁证 |
| earnings / macro / imbalance / socialmedia / news / sentiment / institutions | 0 | 1.0–1.6 | ⛔ 见 §3 逐类判决 |

## 2. Institutions（用户指定类别）—— 判决：结构性不可达

| 数据集 | 字段 | cov | 本地回测 | max S | 结论 |
|---|---:|---:|---:|---:|---|
| `institutions6` | 11（全 MATRIX） | 0.9996 | 8 | **0.60** | 上一轮 110 次模拟最强件 `MPYee1r6` S 0.97；2Y 1.42 |
| `fund_holdings_panel` | 30（12 MATRIX + 18 VECTOR） | 0.8093 | 10 | **0.56** | 账户级数据 2015 起 ⇒ 2014 空年，**不满足「近十年有数据」** |

**唯一 S≥1.58 的构型**（`qML5kxVv`，`ts_regression` 残差动量，S 2.05）被三闸同杀：
`LOW_FITNESS 0.79/1.0`、`HIGH_TURNOVER 80.03%/70%`、`IS_LADDER_SHARPE −0.56/1.58`。
⇒ **换集**（用户 2026-11-15 批准「确实无计可施时更换并说明原因」）。

## 3. 其余未点亮类别逐类判决（依据 = 本地实测 + `reference/unlit_towers_roadmap_20261030.md` §3 波次台账）

| 类别 | 活数据集 | 判决 | 依据 |
|---|---|---|---|
| news | news7/18/20/31/46/50/85/79 … | ⛔ 塔关闭（wave 211） | 五条轴（方向/计数/强度/结构/幅度）全落在 S 0.25–0.67，十年覆盖全 PASS ⇒ 死因是「新闻信息在 D1 已定价」 |
| sentiment | other553 / sentiment23/26/27 / news_sentiment_transfer | ⛔ 塔关闭（wave 189/192/216） | 覆盖判死（2019 起）+ 机制判死（max\|S\| 0.28/0.20） |
| macro | macro63 | ⛔ 无截面 | 单字段 WTIDJH 成分状态，KOR `longCount` 十年全 0 |
| socialmedia | socialmedia39 / other100 | ⛔ 无信号面 | 仅「邻居票 ID 列表」连接键 |
| earnings | earnings3 | ⛔ 强度天花板 0.95 | wave 186/209/210 三几何实测，calendar-distance 单字段上限 ≈0.95 |
| imbalance | imbalance5 | ⛔ 2Y 结构性不可达 | 3 种形态 S 1.08–1.09 全卡 2Y≈0.17 |
| **insiders** | insiders5 / insiders1 | ✅ **主攻 insiders5** | 见 §4 |
| **pv** | pv30/pv37/pv13/intraday_pv_feats… | ✅ 补 1 颗 | 差 1 颗点亮；`ZYQ116ln` 全闸 + prod 0.698 |
| **other** | oth475 / oth496 / oth695 / dl_riskfree_returns | ✅ 旁证 | 各有全闸件；`oth475` 出口额是 OS 池未覆盖的信息源 |

## 4. 选定：insiders5（主）+ pv / other（补）

**insiders5 依据**：

1. **全字段画像已在库**：`reference/datasets/insiders5.md`（53/53 字段，全 VECTOR，按 description 分 5 族：
   交易流量 / 交易时点 / 持仓快照 / **库藏股** / 标识属性）。
2. **现成全闸件充足**：本地 103 条回测 ⇒ **56 条过 S/2Y/TO 三闸** ⇒ 平台复验 **15 条 `failed_ra_count=0`**。
3. **prod 仍有白空间**：OS 池 49 条里 **insd5 只占 1 条**（`RRE9NkVj`，`−ts_mean(vec_stddev(vol_chg),55)` 族）。
   ⇒ 同族**其余件 prod 0.84–0.97 全撞墙**（重复件陷阱），但**换子族**仍可过：
   实测 `78LpqZYQ`（分析师惊奇 − 内部人分歧度）**prod 0.697 通过**。
4. **未挖子族**：库藏股（`insd5_trsy_*`，cov 0.8728）、去重缺口（`source_real_ratio / source_ratio`）——
   两族**从未在任何区域进过候选池**，是本轮第 1 波的两条新机制。

**pv 依据**：`ZYQ116ln` = `subtract(0.5, group_rank(ts_mean(corr_bid_price_with_bid_size,22), industry))`，
S 1.86 / F 1.10 / TO 22.05% / 2Y 1.80 / `failed_ra_count=0` / **prod 0.698**；PV 塔 2/3，出一颗即点亮。

**other 依据**：`oth475_export_value`（出口额）与 OS 池的进口额（`oth695`）、涨跌停（`oth496`）不同源，
但 `rKRLLzRa` 实测 **prod 0.8284（撞墙）** ⇒ 只作旁证，不入 A 档。

## 5. 禁区（本轮不投）

死数据集 16 个（含 **institutions6**、news79、sentiment21、acquisition_model…）+ 战役级判死
（**fund_holdings_panel**、other455、ai_equity_alpha…）。详见 `reference/unlit_towers_roadmap_20261030.md` §4。
