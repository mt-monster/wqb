# EUR 挖掘经验总结（2026-10-27 ~ 10-28 会话）

> 只记**可复用判据**，不记流水账。证据见 `.workbuddy/memory/2026-10-28.md` 与各 alpha id。

## 一、破闸的核心认知（本轮最大收获）

### 1. ★ sub 闸是**比率闸**，不是绝对值闸 —— 高 S 是双刃剑
- EUR `LOW_SUB_UNIVERSE_SHARPE` = **0.52–0.53 × S**（三例逐位吻合：1.07/2.05、1.12/2.15、1.17/2.25）。
- ⇒ 抬 S 会同步抬 sub 闸。**sub/S < 0.52 的信号，S 再高也过不去**。
- ⇒ 选型口径改为"**找 sub/S 比例最高的结构**"，而不是"追最高 S"。

### 2. ★★ universe 错 ≠ 信号死（本轮唯一真突破）
同一表达式 `signed_power(rank(ts_backfill(vec_avg(projected_excess_return),22)),p)`：

| universe | S | F | TO | sub/限 | rob | 2Y |
|---|---|---|---|---|---|---|
| TOP2500 | 2.04 | 1.52 | 0.052 | 1.03/1.06 ✗ | — | 1.72 |
| **TOPCS1600** | **2.05** | **1.62** | **0.041** | **1.10 过** | **0.83 过** | **1.69** |

⇒ **换 universe 一次解决 sub 与 2Y，且 S/F 同升**。在放弃某个信号前，先做 universe 双向夹逼（TOP2500 ↔ TOPCS1600 ↔ TOP1200）。
（注：TOPCS1600 本就是 EUR 区域缺省档，此前用 TOP2500 是偏离 profile。）

### 3. ★ `vector_neut(x, rank(cap))` 在本区是 2Y 杀手
两种 universe、所有幂次下都一致：2Y **1.59 → 1.00 / 1.72 → 1.01**。
⇒ 它确实能修 sub（1.06 过闸），但代价是 2Y 归零 ⇒ **修 sub 禁用此法**；与 MEMORY §4"vector_neut 对水平量 +0.32"不矛盾——这里的输入是 `rank()` 后的有界变量，非原始水平量。

## 二、杠杆表（EUR 实测，勿跨族外推）

| 杠杆 | Δprod | ΔS | Δ2Y | 备注 |
|---|---|---|---|---|
| 幂次 0.5→1.0 | **−0.0335** | 压 | — | 上限 2.1（2.4⇒F 0.96 FAIL） |
| `group_neutralize(·, bucket(rank(cap),0,1,0.05))` | **−0.0253** | 抬 | — | 20 桶甜点；5 桶⇒F 0.98 FAIL；前置 `IS_LADDER≥2.02` |
| 幂次↓（1.8→1.2） | — | — | **+0.15**（1.52→1.67） | 单调；与 prod 方向相反 |
| `vector_neut(rank(cap))` | — | 微降 | **−0.7 崩** | 禁用 |
| 混第二腿 | — | 抬 | **−0.5 崩**（1.69→1.06/1.12） | 本区**加腿一律压 2Y** |
| `group_neutralize(·,subindustry)` | — | +0.07 | +0.07（1.69→1.76） | 最优分组轴（本区 subindustry > industry > market） |

## 三、判死清单（本轮新增，勿重投）

| 对象 | 死因 | 证据 |
|---|---|---|
| **EUR 残差动量**（`rank(-ts_regression(ts_zscore(returns,252), ts_zscore(ts_delay(F,21),252),252,0))`） | 不跨区 | 6 变体 S≤1.40 / F≤0.55 / 2Y ≈0（IND 上同类结构 prod 0.47–0.68） |
| **fundamental28**（1605 原始科目） | **cov 恒 0.50** | 最好 S1.57/F0.83/2Y2.08，但 sub 0.52 vs 限 0.82 ⇒ 覆盖率不足必死于 sub 闸 |
| **global_seasonal_model** | 事件预测反向噪声 | TOPCS1600 上 6 条全负 S（−0.15~−0.58）；翻符号仅 +0.35 |
| **ai_equity_alpha 其余字段** | 无料 | financial_statement_volatility 1.38 / accounting_forensics 0.20 / earnings_growth 0.36 / analyst_sentiment 0.55 / opacity 混入负 |

⇒ **数据集准入门槛新增一条：cov < 0.85 不进候选池**（低 cov 对 sub 闸是确定性死因，与既有"低 cov 腿致整批 ERROR"同源）。

### 3.1 ★★★ 未点亮塔（news/sentiment）在本区结构性无信号（44 条表达式实证）

| 波 | 数据集 | 类 | 结构 | 条数 | 最好 S | TO | 2Y |
|---|---|---|---|---|---|---|---|
| E1/E2 | `news73` | news | 情绪分 5 字段 × {幂次/分组/平滑/极性合成} × {decay 4, 40} | 16 | **0.58** | 0.065→0.032 | ≤1.13 |
| F1/F2 | `sentiment21` | sentiment | 5 个聚合统计 × {subindustry, country 轴} | 14 | **0.36** | 0.09 | ≤0.39 |
| G | `news17` | news | 5 个文本分类器 + 相关性权重 | 8 | **0.44** | 0.08 | ≤0.70 |

**★ 三条硬结论**：
1. **TO 不是 NEWS 族死因**（decay 4 下 TO 仅 0.065–0.096）。decay 40 把 TO 压 −45% 而 **S 不动** ⇒ 是"无信号"而非"成本吃掉"。
   ⇒ 修正旧归纳：NEWS 有**两种死法** —— `news20/54` 的 TO 爆炸型，与 `news73` 的无信号型。
2. **分组轴杠杆不跨族**：`country` 轴在财务类是 +0.19，在情绪上是 **0.30→0.36（噪音级）**。
3. **`group_zscore` 会产生结构伪影**：`sub_universe_sharpe` 普遍高于 S（例：S 0.30 / sub 0.76），因未中心化导致多空失衡 ⇒ 不可把 sub 高当信号强。

⇒ EUR 未点亮类（news / sentiment / earnings / institutions / macro / imbalance / socialmedia）**已无可用信号源**：
- `earnings6` 66 字段全为元数据（日期/公司名/电话/交易所/ticker）；
- `institutions6`（2Y −0.30）、`fund_holdings_panel`（returns 2.33%）、`macro27`（returns 2.27%）、`imbalance5`（returns 2.66%）、`socialmedia15`（TO 1.23–1.33）历史已判死。
- 合计：本区历史 46 条 news 回测 + 11 条 sentiment 回测 + 本轮 44 条 = **0 条全闸**。

### 3.2 ★ MODEL 塔 `ai_equity_alpha` 判死（prod 实测）

`kqNr8pKK` prod **0.8052 ✗**。直方图 0.7+ 仅 **24 颗**（0.6–0.7 有 2,663 颗）⇒ **宽分布长尾墙（A 型）**，不是可绕开的单点对手（B 型）。
三颗同机制（同字段换幂次/中性化）⇒ 同 prod，全废。MODEL 塔本季已 3 颗，该源已被占位。


## 四、工程纪律（踩坑后固化）

1. **prod/self 只准走 MCP**（`check_correlation`）；**禁止**临时 Python 直连。
2. **提交回测/状态/收割只准走 MCP**（`submit_batch`/`batch_status`/`harvest_multisim_alphas`）。
3. **平台饱和时别原地重试 prod**：`check_correlation` 的 pending 会占 300s 本机 inflight 窗口，连试只会越试越慢；抢到槽后要给它 5–10 分钟静默期。
4. **`harvest_multisim_alphas` 需 `/simulations/<id>` 前缀**，裸 id 返 404。
5. **multisim 生子仿真在拥堵时可达 5–12 分钟**，`batch_status` 的 `child_count=0` 不代表失败。
6. **预检必做**：`preflight_expressions` 会自动补 `vec_*`（本区大量数据集是 VECTOR 型，裸字段秒拒且一条错整批 CANCELLED）。

## 五、当前可用资产

| alpha | 塔 | S | F | sub | rob | 2Y | 状态 |
|---|---|---|---|---|---|---|---|
| `A1VZLX3e` | MODEL | 1.99 | 1.44 | 1.11 | 0.97 | 1.76 | IS/RA 全过，**prod 未测** |
| `kqNr8pKK` | MODEL | 2.05 | 1.62 | 1.10 | 0.83 | 1.69 | 同上，cluster 1.57⚠ |
| `Xg9Qv121` | MODEL | 2.04 | 1.59 | 1.09 | 0.83 | 1.62 | 同上 |
| `6XAe27eL` | analyst | 1.74 | 1.10 | 0.96 | — | 1.62 | prod 0.4857 / self 0.447 ✅ |
| `Grge2lN3` | analyst | 1.79 | 1.15 | 0.94 | — | 2.02 | prod 0.5893 / self 0.5386 ✅ |
| `rKd5lAo8` | fundamental | 1.64 | 1.14 | 1.07 | — | 1.78 | prod 0.6747 / self 0.5054 ✅ |

前 3 颗同机制（同字段换幂次/中性化）⇒ 预计只出 1 席。
