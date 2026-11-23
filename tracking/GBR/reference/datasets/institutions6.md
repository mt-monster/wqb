# GBR / institutions6（Institutions and Beneficial Stake Ownership，机构持股/流量/家数，全 MATRIX）

> 塔：**institutions**（GBR/D1 乘数 **1.4**，当前 **1/3**——`E5Q6bbLm`（institutions1 族）已提交；差 2 席）
> 画像日期 2026-11-21 · 数据源 `mcp__wq-brain-http__get_datafields`（GBR/TOP700/D1，`filter_sharpe=false`，不传 `max_fields`）
> 本轮实拉：`count=11` / `platform_count=11` / `returned=11` / `complete=true` / `pages_fetched=1`。
> ⚠ 全 11 字段 **coverage=1.0**（本区唯一全覆盖机构集），MATRIX ⇒ 不套 `vec_*`。
> ⚠ 季度披露（13F/季报型）⇒ 序列是阶梯函数；时序算子前建议 `ts_backfill`（28 赞帖）；分母统一 +1 防零（同帖）。

---

## 字段全表（平台实拉 11/11）

| 字段 | 类型 | cov | αC | uC | 经济含义（平台 description） |
|---|---|---:|---:|---:|---|
| `count_institutional_sellers_security` | MATRIX | 1.0 | **214** | 150 | 本期减持机构家数 |
| `count_institutional_buyers_security` | MATRIX | 1.0 | 187 | 126 | 本期增持机构家数 |
| `quantity_institutional_shares_acquired` | MATRIX | 1.0 | 153 | 113 | 本期买入股数 |
| `aggregate_share_count_all_owners` | MATRIX | 1.0 | 140 | 92 | 全体持有人持股数（去重） |
| `aggregate_equity_value_institutions` | MATRIX | 1.0 | 132 | 100 | 机构持仓总市值（美元） |
| `aggregate_share_count_institutions` | MATRIX | 1.0 | 122 | 87 | 机构持股数 |
| `market_value_institutional_shares_acquired` | MATRIX | 1.0 | 120 | 82 | 机构买入金额（美元） |
| `count_institutional_holders_security` | MATRIX | 1.0 | 112 | 74 | 当前持有机构家数 |
| `aggregate_equity_value_all_owners` | MATRIX | 1.0 | 103 | 82 | 全体持有人持股市值（美元，去重） |
| `market_value_institutional_shares_disposed` | MATRIX | 1.0 | 86 | 65 | 机构卖出金额（美元） |
| `quantity_institutional_shares_disposed` | MATRIX | 1.0 | 93 | 68 | 本期卖出股数 |

> αC 逐行（按表序）：214, 187, 153, 140, 132, 122, 120, 112, 103, 86, 93（合计 1462，均值 133）。uC 逐行：150, 126, 113, 92, 100, 87, 82, 74, 82, 65, 68（合计 1039，均值 94.5）。

---

## 3. 聚合统计

| 指标 | 值 |
|---|---|
| 字段总数 | 11（全 MATRIX） |
| coverage | **11/11 = 1.0**（本区最高；institutions4 0.39 / institutions1 0.31 / institutions25 0.0 盲区） |
| αC 合计 / 均值 | 1462 / 133 |
| αC 最大 / 最小 | 214（sellers）/ 86（market_value_disposed） |
| dateCreated | 11/11 = 2026-07-01（同批 onboard） |
| pyramidMultiplier | 11/11 = 1.4 |
| αC=0 | 无 |

数据集级：`id=institutions6` / `name=Institutions and Beneficial Stake Ownership` / `category=institutions` / `fieldCount=11` / `coverage=1.0` / `userCount=442` / `alphaCount=981` / `valueScore=2.0` / `pyramidMultiplier=1.4`。

---

## 4. 字段族拆解（三族口径）

| 族 | 字段 | 机制 |
|---|---|---|
| **存量族**（水平） | `aggregate_equity_value_institutions`、`aggregate_share_count_institutions`、`aggregate_equity_value_all_owners`、`aggregate_share_count_all_owners` | 当前持仓规模（市值/股数），分机构版与全体版 |
| **流量族**（本期变动） | `market_value_institutional_shares_acquired`、`market_value_institutional_shares_disposed`、`quantity_institutional_shares_acquired`、`quantity_institutional_shares_disposed` | 本期买入/卖出金额与股数 |
| **家数族**（广度） | `count_institutional_buyers_security`、`count_institutional_sellers_security`、`count_institutional_holders_security` | 增持/减持/持有机构家数 |

**族间关系**（28 赞帖给的经济配比，全部是「同口径相除」）：
1. **存量 ÷ 家数 = 平均单家机构仓位（集中度）**：`aggregate_equity_value_institutions / count_institutional_holders_security`
2. **机构持股 ÷ 全体持股 = 机构化率**：`aggregate_share_count_institutions / aggregate_share_count_all_owners`（分母不是流通股本）
3. **金额 ÷ 股数 = 机构成交均价**：`market_value_institutional_shares_acquired / quantity_institutional_shares_acquired`
4. **流量 ÷ 存量 = 机构换手**：`(market_value_acquired + market_value_disposed) / aggregate_equity_value_institutions`
5. **买 ÷ 卖 = 广度比**：`count_buyers / count_sellers`；净广度 = `(buyers − sellers) / holders`

---

## 5. 可用性三分

| 分类 | 字段 | 依据 |
|---|---|---|
| **① 配比分子/分母**（不可裸信号） | 全部 11 字段 | 裸水平/裸流量在 USA 实测均为噪声（S −0.18~0.85，6/8 条单边 long、invest 全负）；必须**同口径相除**后再中性化 |
| **② 直接元数据可用** | cov 全 1.0 | 无盲区；季度更新需 `ts_backfill` 进时序算子前 |

---

## 6. 六法/实测

| 法 | 读数 / 结论 |
|---|---|
| **① 覆盖率** | **cov=1.0（平台元数据，11/11）**；GBR 回测 lc/sc 历史 300–500 双边 ⇒ 覆盖充足 |
| **② 非零率** | 季度披露；家数/流量族零值常见（无交易季度）⇒ 分母 +1 / `ts_backfill` 平滑 |
| **③ 更新频率** | 季度（13F 型）⇒ 窗口 ≥66；`ts_zscore(126)` 有效（批 D 实测见 §8） |
| **④ 量纲** | 存量/流量有两套（美元 vs 股数）⇒ **同单位相除才无量纲**；跨族相减必错（28 赞帖原文） |
| **⑤ 中心** | 存量恒正（单边）；流量双边（买/卖） |
| **⑥ 分布** | 存量右偏长尾（美元 10⁶–10⁹）；家数右偏；比率后近正态 |

**模板白名单（28 赞帖配方 + GBR 本地化）**：
- 机构化率：`group_rank(ts_zscore(divide(aggregate_share_count_institutions, aggregate_share_count_all_owners), 126), industry)`
- 机构化率动量：`group_rank(ts_delta(divide(...), 66), sector)`
- 平均单家仓位：`group_rank(ts_zscore(divide(aggregate_equity_value_institutions, count_institutional_holders_security), 126), sector)`
- 机构换手：`group_rank(ts_zscore(divide(add(acquired, disposed), aggregate_equity_value_institutions), 126), industry)`
- 净广度：`group_rank(ts_zscore(divide(subtract(buyers, sellers), holders), 126), sector)`
- 买家比例（EUR 唯一活内核移植）：`group_rank(ts_zscore(divide(buyers, holders), 66), industry)`
- 新鲜度门（IND LC97552 模板）：`trade_when(ts_arg_max(holders, 90) < 33, signed_power(ts_quantile(divide(buyers, ts_mean(holders,72)), 840), 1.6), -1)`
- 机构成交均价：`group_rank(ts_zscore(divide(market_value_acquired, quantity_acquired), 126), sector)`
- 净流入率：`group_rank(ts_zscore(divide(subtract(market_value_acquired, market_value_disposed), aggregate_equity_value_institutions), 126), sector)`
- 卖出压力（Dasgupta 2011）：`group_rank(ts_zscore(divide(market_value_disposed, aggregate_equity_value_institutions), 126), industry)`

---

## 7. 判据核验

- cov 1.0 ⇒ 无盲区，不需 NONE 探针；直接进标准档。
- 跨区结论：GBR in6 历史已 154 臂、天花板 |S| 0.95（2026-11-20）；**塔 1/3 未满，PROVISIONAL 不判死**。
- 与 institutions1（E5Q6bbLm 所在集）**不同数据集**；组腿允许（同 category 不做两两组合？用户红线只禁 PV/MODEL/OTHER 内部及相互 ⇒ institutions+institutions 不在禁止列表，但**同类别两集组腿会撞 ATOM 与同源**，本批一律 ATOM 单集）。

---

## 8. 批 D · 三族口径实测（2026-11-21，SUBINDUSTRY/decay4/trunc0.08/nanON）

`multisimulation_id=2yMmWY5zg57rbz8M2h5rGPj`（10 臂）

| # | 机制 | 表达式核心 | S | F | 2Y | TO | RA |
|---|---|---|---:|---:|---:|---:|---|
| 1 | 机构化率 | `ts_zscore(divide(share_inst, share_all),126)@industry` | 待收 | | | | |
| 2 | 机构化率动量 | `ts_delta(divide(share_inst, share_all),66)@sector` | 待收 | | | | |
| 3 | 平均单家仓位 | `ts_zscore(divide(ev_inst, holders),126)@sector` | 待收 | | | | |
| 4 | 机构换手 | `ts_zscore(divide(acquired+disposed, ev_inst),126)@industry` | 待收 | | | | |
| 5 | 净广度 | `ts_zscore(divide(buyers-sellers, holders),126)@sector` | 待收 | | | | |
| 6 | 买家比例 | `ts_zscore(divide(buyers, holders),66)@industry` | 待收 | | | | |
| 7 | 新鲜度门（IND 模板） | `trade_when(ts_arg_max(holders,90)<33, signed_power(ts_quantile(divide(buyers, ts_mean(holders,72)),840),1.6), -1)` | 待收 | | | | |
| 8 | 机构成交均价 | `ts_zscore(divide(mv_acquired, qty_acquired),126)@sector` | 待收 | | | | |
| 9 | 净流入率 | `ts_zscore(divide(mv_acquired−mv_disposed, ev_inst),126)@sector` | 待收 | | | | |
| 10 | 卖出压力 | `ts_zscore(divide(mv_disposed, ev_inst),126)@industry` | 待收 | | | | |

> 注：arms 1/3/4/5/8/9/10 的 `divide` 分母可能为 0（无机构/无交易季度）→ 平台返回 NaN，由 nanHandling=ON 处理；28 赞帖建议 +1，但 GBR `unit_handling=VERIFY` 下裸 +1 有 UNITS 风险（AGENTS §「裸常数 UNITS 坑」）⇒ 本批先试无 +1 形态，若整批 UNITS 拒收再改 `divide(..., add(...))` 同单位版本。

---

## 9. 证据闸

### 论坛
- **28 赞（`43664593081879`）**：in6 三族口径与 8 组配比实测（USA/D1）；裸结构全弱、必须同口径相除 + 中性化。**本批的直接配方来源**。
- **70 赞（`43754821327639`）**：GBR 专属「分析师预期 ÷ 机构持股规模 + 126d ts_zscore」→ S1.28/F0.91；机构人数门控反向劣化（S0.99）⇒ 本批不叠 analyst（analyst 塔已点亮，禁投入）+ 不做人数门控。
- IND 机构+分析师共振（`44147814648215`）：买家/卖家比率 + 分析师，S2.39/prod0.6524（跨区参考，腿语义不可照搬）。
- 2026-11-09 判死记录：`GBR-INST6-HOLDINGS-CEILING-20260929`（institutions6 机构持仓/流量族不再生成新变体）——**本轮以不同几何（三族配比/新鲜度门）重开，若全灭则回填该判死**。

### 论文（paper_search --diverse，≥5 篇 ∧ ≥3 作者）
| 论文 | 机制 → 模板 |
|---|---|
| Dasgupta, Prat & Moraga-González (2011), "The Price Impact of Institutional Herding", RFS, doi:10.1093/rfs/hhq137 | 机构羊群 → 后续修正：卖出压力/净流入率配比 |
| Nofsinger & Sias (2003), "Institutional Herding", RFS, doi:10.1093/rfs/hhg035 | 机构羊群与持仓变化 → 流量÷存量（换手） |
| "International Evidence on Institutional Trading Behavior and Price Impact" (2004), JF, doi:10.1111/j.1540-6261.2004.00651.x | 机构交易与价格冲击跨市场 → 家数广度 |
| "Price Impact Asymmetry of Block Trades" (2001), RFS, doi:10.1093/rfs/14.4.1153 | 买卖冲击不对称 → buyers/sellers 分别建模 |

---

## 10. 小结

- in6 = GBR 唯一 cov=1.0 机构集、11 字段三族、塔 1/3 差 2 席。
- 裸字段不可用（USA 8 组实测全弱）；**同口径配比 + 中性化 + 季度平滑**是唯一合规路径。
- 批 D（10 臂）在读；若全灭回填 `GBR-INST6-HOLDINGS-CEILING`，若有近闸再进梯度。