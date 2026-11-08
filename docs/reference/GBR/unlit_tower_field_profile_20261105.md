# GBR 未点亮塔 · 字段画像与机制地图（2026-11-05 复核）

> 口径：`GBR / TOP700 / D1 / EQUITY`。
> 数据来源：本轮 `get_datasets(category=…)` + `get_datafields(dataset_id=…)` 实读（2026-11-05），
> 与 `docs/reference/GBR/unlit_tower_field_profile_20261031.md`（下称"10-31 报告"）交叉核对。
> 本文件只写**可执行事实**；判死结论以引用处的实测为准。

---

## 0. 本轮结论（先看这 6 条）

1. **未点亮 9 塔、17 个候选数据集，今天复核无新增**。有实际覆盖的仍只有 9 个数据集；`earnings6` / `earnings_sent_matrix` / `option1` / `macro27` / `socialmedia12` / `socialmedia5` / `risk68` / `risk71` / `risk72` / `insiders12` / `imbalance5` 在 GBR/TOP700 的**字段级 coverage 全为 0**（`earnings6` 今天逐字段复核仍 18/18 = 0.0）。
2. **唯一未被 10-31 报告实测的候选是 `insiders1`**（9 个 VECTOR 字段，cov 0.5937，无买卖方向字段）。本轮纳入 Wave 1 之后的结构轴波次。
3. **历史产出率**（DB `get_mining_yield(strict=False, S≥1.25/F≥1.0)`）：`shortinterest3` 80 次回测 / 1 次达标；`institutions6` 115 / 0；`insider_agg_matrix` 37 / 0；`fund_holdings_panel` 40 / 0。⇒ **近闸池不能靠"重跑历史"，只能靠新机制 + 新几何**。
4. **本区未点亮塔的最强已验证设置档**（从平台 alpha 详情反读，不是猜）：
   `decay=15 / neutralization=FAST / truncation=0.05 / nanHandling=ON / maxTrade=OFF`。
   代表：`leA23Jae`（DTC22，S1.72）、`WjOd7edQ`（institutions6 sellers，S0.95）、`qMLdnQXE`（risk60 fee，S0.40）。
   区域 `settings.json` 的 `SUBINDUSTRY + decay4 + trunc0.08` 是**已点亮塔的赢家档**，不是未点亮塔的最优档；
   两档必须做 A/B，不能混读（见 §5）。
5. **PV/MODEL/OTHER 组腿红线**：`shortinterest3 ÷ volume`（ADV）这类表达式会同时点亮 PV 塔，属于"PV+非 PV"组腿，
   全战役**最多 5 条**。本轮优先用 `risk88.alternative_market_cap_usd`（RISK，cov 1.0）与
   `current_enterprise_value`（FUNDAMENTAL，非 PV/MODEL/OTHER）做分母，把 PV 配额留给 DTC 系列。
6. **近 10 年数据**：IS 窗口固定 `2014-01-01 ~ 2023-12-31`（区域 settings）。任何候选在进入近闸池前，
   必须用 `get_alpha_yearly_stats` 逐年核 `longCount>0 && shortCount>0 && pnl>0`；缺年即剔除（§6）。

---

## 1. 数据集覆盖总表（2026-11-05 实读）

| 塔 | 数据集 | dataset cov | 字段数 | 字段级 cov 范围 | 类型 | 判定 |
|---|---|---|---:|---|---|---|
| shortinterest | **shortinterest3** | 0.849 | 25 | 0.8217–0.8719 | VECTOR | ✅ 主力 |
| risk | **risk60** | 0.6694 | 5 | 0.6694 | VECTOR | ✅ 可用 |
| risk | **risk88** | 1.0 | 1 | 1.0 | MATRIX | ✅ 仅分母 |
| institutions | **institutions6** | 1.0 | 11 | 1.0 | MATRIX | ✅ 可用 |
| institutions | fund_holdings_panel | 0.9099 | 18 | — | — | ❌ 10-31 已判死（真 F 墙） |
| institutions | institutions1 / institutions4 / institutions25 | 0.31 / 0.39 / 0.0 | 7 / 6 / 24 | — | — | ❌ 10-31 全排除 |
| insiders | **insider_agg_matrix** | 0.6175 | 34 | 0.5935–1.0 | MATRIX | ⚠️ 有值但历史最好 S0.51 |
| insiders | **insiders1** | 0.5937 | 9 | 0.5937 | VECTOR | ⚠️ **本轮唯一未测** |
| insiders | insiders12 | 0.0 | 7 | 0.0 | — | ❌ 无覆盖 |
| sentiment | **sentiment27** | 0.8003 | 18 | 0.7976–0.814 | VECTOR/SYMBOL | ❌ 10-31 全族判死 |
| sentiment | **sentiment7** | 0.5784 | 3 | 0.5766–0.5819 | VECTOR | ❌ 10-31 判死（2Y −0.19） |
| sentiment | **sentiment33** | 0.3218 | 255 | 0.3218 | VECTOR | ❌ 10-31 判死（净语调为负） |
| option | option1 | 0.0 | 22 | 0.0 | — | ❌ 无覆盖 |
| earnings | earnings6 | 0.0 | 18 | **0.0（今天逐字段复核）** | VECTOR | ❌ 无覆盖 |
| earnings | earnings_sent_matrix | 0.0 | 7 | 0.0 | — | ❌ 无覆盖 |
| macro | macro27 | 0.0 | 13 | 0.0 | — | ❌ 无覆盖 |
| socialmedia | socialmedia39 | 0.4948 | 1 | 0.4948 | VECTOR | ❌ 字段是非数值 ticker 列表 |
| socialmedia | socialmedia12 / socialmedia5 | 0.0 | 6 / 13 | 0.0 | — | ❌ 无覆盖 |
| imbalance | imbalance5 | 0.0 | 2 | 0.0 | MATRIX | ❌ 无覆盖（`imb5_score` 是 0–1 复合分，但 GBR 无值） |

---

## 2. 字段级画像（只列进入本轮模板库的 7 个集）

### 2.1 shortinterest3（25 VECTOR，三套变体）

三套变体：**裸名 / `_main` / `_p5_d1`**；`_p5_d1` 覆盖率最高（0.8719）且 alphaCount 最大 ⇒ 本轮统一用 `_p5_d1`。

| 语义族 | 字段 | cov | 说明 |
|---|---|---:|---|
| 借券存量 | `loaned_share_count_p5_d1` | 0.8719 | 出借股数（做空筹码存量） |
| 借券市值 | `loaned_market_value_usd_p5_d1` | 0.8719 | 出借市值 USD |
| 借贷笔数 | `transaction_count_p5_d1` | 0.8719 | 借贷成交笔数（市场活跃度/机构参与） |
| 借贷久期 | `average_loan_duration_days_p5_d1` | 0.8719 | 借贷加权平均年龄（空头顽固度） |
| 费率水平 | `mean_loan_rate_p5_d1` | 0.8719 | 加权平均借券费率 |
| 费率尾部 | `max_loan_rate_p5_d1` / `min_loan_rate_p5_d1` | 0.8719 | dealer 价差/急迫借款人 |
| 费率不确定性 | `loan_rate_volatility_p5_d1` | 0.8719 | 费率标准差 |
| 需求评级 | `shrt3_bar` | 0.8669 | 1–10 预计算借券需求评级 |

**可构造的高阶量**（不引入第二数据集）：
`loan_count / loaned_share_count`（单笔规模）、`loaned_value / transaction_count`（单笔金额）、
`max_fee − mean_fee`（尾部价差）、`fee_vol / mean_fee`（费率 CoV）、
`duration × fee`（久期×成本交互）。

### 2.2 institutions6（11 MATRIX，cov 1.0）

| 语义族 | 字段 | 说明 |
|---|---|---|
| 家数（广度） | `count_institutional_sellers_security` / `count_institutional_buyers_security` / `count_institutional_holders_security` | 报告期卖出/买入/持有的机构家数 |
| 金额流 | `market_value_institutional_shares_disposed` / `..._acquired` | 卖出/买入金额 |
| 股数流 | `quantity_institutional_shares_disposed` / `..._acquired` | 卖出/买入股数 |
| 存量 | `aggregate_equity_value_institutions` / `aggregate_share_count_institutions` | 机构持有总市值/总股数 |
| 全所有者存量 | `aggregate_equity_value_all_owners` / `aggregate_share_count_all_owners` | 用于算机构持股占比 |

**关键实证（10-31）**：`-rank(ts_rank(sellers,504))` = S0.95；`+buyers` = −0.14；`+holders` 全期 −0.19 / 2Y −1.23；
`-(sellers−buyers)` = 0.64 ⇒ **卖家家数是最强拥挤维度，做减法会掉信号**。本轮在此基础上加"家数/持有人基数"比率。

### 2.3 risk60（5 VECTOR，cov 0.6694）

`rsk60_offer`（空头借券费率）、`lending_fee_bid_rate`（多头出借费率）、`rsk60_last`（最新费率）、
`rsk60_crowding`（带符号日度做空活动：正=加空/拥挤）、`rsk60_datatime`（时间戳，非信号）。

**本轮新增**：`rsk60_crowding` 在 10-31 报告里**没有被单独测过**（只测了费率水平/偏离/波动），是最大的未测面。

### 2.4 risk88（1 MATRIX，cov 1.0）

`alternative_market_cap_usd` = 市值（USD）。**只作分母**：可把"借券存量/机构持股/内部人交易"变成比率，
同时点亮 RISK 塔，且不占 PV 配额。

### 2.5 insider_agg_matrix（34 MATRIX）

- 全体董事：`total_buy_shares` / `total_sell_shares` / `avg_buy_shares` / `avg_sell_shares`
- 直接交易（secondary）：`total_secondary_buy_shares` / `total_secondary_sell_shares`
- 高管（top）：`total_top_buy_shares` / `total_top_sell_shares`
- 显著交易：`significant_value_1..4`、`top_significant_value_1..4`、`directional_significant_value_1..4`
- 预计算方向：`directional_indicator` / `directional_indicator_2`（cov 1.0）
- 覆盖：大部分 0.5937 / 0.5935；`directional_indicator*` = 1.0。

**本轮新增机制**：仓位变化比（`total_sell / total_buy`、`(buy−sell)/(buy+sell)`）、
显著交易集中度（`significant_value_1 / significant_value_4`）、高管 vs 董事分层。

### 2.6 insiders1（9 VECTOR，cov 0.5937，本轮唯一未测）

`insd1_holdings`（交易后持股）、`insd1_shares`（交易股数）、`insd1_price`、`insd1_value` / `insd1_valueeur`、
`insd1_tradesignificance`（1–3 重要性）、`insd1_gvkey`、`max_trade_price`、`transaction_currency_code`。
**没有买卖方向字段** ⇒ 方向只能从 `holdings` 变化推断；本轮以"交易强度/持仓换手"为主：
`insd1_shares / insd1_holdings`（仓位变动比）、`insd1_valueeur / insd1_holdings`（金额强度）、
`ts_delta(vec_avg(insd1_holdings), 66)`（持仓变化）。

### 2.7 sentiment27（18，cov 0.7976–0.814）

可用数值字段：`snl27_relpopularity1` / `snl27_relpopularity08`（相对关注度）、`snl27_avgranking` / `snl27_topranking`（排名，越低越热）、
`snl27_top50pctrankingavg` / `snl27_top75pctrankingavg`（分位内平均排名）、`snl27_skewness` / `snl27_kurtosis`（域名排名分布形态）、
`snl27_totaldomains` / `snl27_totalcountrydomains`（域名数/国家域名数）、`snt27_rank`。
**10-31 已判死**：水平/差分/长窗百分位全无信号；本轮不再投，只保留 `kurtosis/skewness` 作为"新机制"控制组（1 条）。

### 2.8 sentiment7（3，cov 0.577）

`snt7_views` / `snt7_all_languages_views`（Wikipedia 浏览量）、`snt7_timestamp`（非信号）。
10-31 判死（水平 S0.49 / 2Y −0.19）。本轮只测"浏览量 ÷ 自身 252 日均值"与"多语言占比"，作为控制组（2 条）。

---

## 3. 机制地图（文献 + 论坛 + 本区实证）

> 读法：**机制 → 方向 → GBR 是否成立**。GBR 未点亮塔的符号多次与美股文献相反（10-31 §9.2），
> 所以每条机制都配"方向控制组"，不默认取负。

### 3.1 SHORTINTEREST（shortinterest3）

| 机制 | 文献/论坛来源 | 方向先验 | GBR 实证 |
|---|---|---|---|
| 借券存量水平（short interest level） | Boehmer-Jones-Zhang (2008) | 高 SI ⇒ 跑输 | ✅ S1.53（`Xg9Ln5ox`） |
| days-to-cover（SI ÷ ADV） | 同上；论坛"高 SI + 正新闻/超卖" | 高 DTC ⇒ 跑输 | ✅ S1.72（`leA23Jae`，但 prod 0.7445） |
| 借券费率水平 | Engelberg-Reed-Ringgenberg (2018) | 高费率 ⇒ 跑输 | ❌ 反向（S −0.20） |
| 借券费率变化 | 同上（该文核心：变化 > 水平） | 费率上升 ⇒ 跑输 | ❌ 变化形式 S −0.42 |
| 借券需求评级 `shrt3_bar` | 数据集自带 | 高评级 ⇒ 跑输 | ❌ S0.17 |
| 借贷笔数水平 | 论坛 3 SI factors / 市场活跃度 | 高活跃 ⇒ 拥挤 ⇒ 跑输 | ✅ 部分（S1.35 `qMLdNGgV`） |
| 借贷久期（空头年龄） | 自建（顽固空头） | 久期长 ⇒ 跑输 | ⏳ 本轮 Wave 1 |
| 单笔规模（股数/笔数） | 自建（机构 vs 散户做空） | 机构大单 ⇒ 信息 ⇒ 跑输 | ⏳ 本轮 Wave 1 |
| dealer 价差（max−mean） | 自建（急迫借款人） | 价差大 ⇒ 压力 ⇒ 跑输 | ⏳ 本轮 Wave 1 |
| 费率 CoV | 自建（借贷市场不确定性） | 高 CoV ⇒ 压力 | ⏳ 本轮 Wave 1 |

### 3.2 INSTITUTIONS（institutions6）

| 机制 | 来源 | 方向先验 | GBR 实证 |
|---|---|---|---|
| 卖家家数（breadth） | 10-31 实证 / 论坛"机构情绪分歧" | 家数多 ⇒ 拥挤 ⇒ 跑输 | ✅ S0.95 |
| 净广度 `(buyers−sellers)/(1+holders)` | 论坛模板（FX25214 / ZL35633） | 净卖出 ⇒ 跑输 | ⏳ 本轮 Wave 1 |
| 卖买金额比 `disposed/acquired` | 自建（金额口径） | 卖压 ⇒ 跑输 | ⏳ 本轮 Wave 1 |
| 持仓周转 `disposed / aggregate_equity_value_institutions` | 自建（流量/存量） | 高换手 ⇒ 跑输 | ⏳ 本轮 Wave 1 |
| 机构持股占比 | 论坛 / category card | 占比高 ⇒ 拥挤 | ❌ 10-31 S−0.20（占比被价格内生化） |

### 3.3 INSIDERS（insider_agg_matrix / insiders1）

| 机制 | 来源 | 方向先验 | GBR 实证 |
|---|---|---|---|
| 买卖比 `sell/buy` | Lakonishok-Lee (2001) / 论坛 | 净卖出 ⇒ 跑输 | ✅ 部分 S0.51（`9qxKRKNe`） |
| 仓位变化比（shares/holdings） | 论坛 DEU 帖「动了多少仓位比多少钱重要」 | 减持比例大 ⇒ 跑输 | ⏳ insiders1 未测 |
| 显著交易集中度 | 数据集自带 `significant_value_*` | 集中大额卖出 ⇒ 跑输 | ⏳ 本轮 |
| 高管 vs 董事分层 | Cohen-Malloy-Pomorski (2012) | 高管交易更有信息 | ⏳ 本轮 |
| 交易方向预计算 `directional_indicator` | 数据集自带 | 方向未知 | ⏳ 做符号控制组 |

### 3.4 RISK（risk60 / risk88）

| 机制 | 来源 | 方向先验 | GBR 实证 |
|---|---|---|---|
| 借券费率水平 | 10-31 | 高费率 ⇒ 跑输 | ❌ S0.40（加 backfill 后） |
| 借券费率波动 | 10-31 | 高波动 ⇒ 压力 | ⚠️ S0.78（2Y 1.34） |
| 做空拥挤度 `rsk60_crowding` | 自建（本区未测） | 加空 ⇒ 跑输 | ⏳ 本轮 |
| dealer 价差 `offer−bid` | 自建（做市商压力） | 价差大 ⇒ 压力 | ⏳ 本轮 |
| 市值分母 | 10-31 §13.3 | 只作分母 | ⏳ 本轮 |

### 3.5 SENTIMENT（sentiment27 / sentiment7 / sentiment33）

10-31 已三集全判死。本轮只保留 3 条控制组（`kurtosis` / `views÷252日均值` / `多语言占比`），
用于验证"死因是字段还是几何"，不再投入主预算。

---

## 4. 模板库（本轮可执行骨架）

> 所有表达式默认 `ts_backfill(...,120)`；外层统一 `-rank(ts_rank(...,504))` 作为**基几何**，
> 让 Wave 1 的差异只来自"分子机制"。结构轴（分组/平滑/门控）放 Wave 2，避免一次动两个自由度。

### 4.1 shortinterest3（8 条，Wave 1A）

| # | 机制 | 表达式骨架 | 塔 |
|---|---|---|---|
| S1 | 借券存量水平（基线） | `-rank(ts_rank(ts_backfill(vec_sum(loaned_share_count_p5_d1),120),504))` | SI |
| S2 | 存量/市值（SIR） | `-rank(ts_rank(ts_backfill(divide(vec_sum(loaned_share_count_p5_d1),alternative_market_cap_usd),120),504))` | SI+RISK |
| S3 | 借券市值/市值 | `-rank(ts_rank(ts_backfill(divide(vec_sum(loaned_market_value_usd_p5_d1),alternative_market_cap_usd),120),504))` | SI+RISK |
| S4 | 单笔股数（股数/笔数） | `-rank(ts_rank(ts_backfill(divide(vec_sum(transaction_count_p5_d1),add(vec_sum(loaned_share_count_p5_d1),1)),120),504))` | SI |
| S5 | 单笔金额（市值/笔数） | `-rank(ts_rank(ts_backfill(divide(vec_sum(loaned_market_value_usd_p5_d1),add(vec_sum(transaction_count_p5_d1),1)),120),504))` | SI |
| S6 | dealer 价差（max−mean） | `-rank(ts_rank(ts_backfill(subtract(vec_avg(max_loan_rate_p5_d1),vec_avg(mean_loan_rate_p5_d1)),120),504))` | SI |
| S7 | 费率 CoV | `-rank(ts_rank(ts_backfill(divide(vec_avg(loan_rate_volatility_p5_d1),add(vec_avg(mean_loan_rate_p5_d1),0.0001)),120),504))` | SI |
| S8 | 借贷久期 | `-rank(ts_rank(ts_backfill(vec_avg(average_loan_duration_days_p5_d1),120),504))` | SI |

### 4.2 institutions6（8 条，Wave 1B）

| # | 机制 | 表达式骨架 | 塔 |
|---|---|---|---|
| I1 | 卖家家数（基线） | `-rank(ts_rank(count_institutional_sellers_security,504))` | INST |
| I2 | 总活动家数 | `-rank(ts_rank(add(sellers,buyers),504))` | INST |
| I3 | 卖家/持有人 | `-rank(ts_rank(divide(sellers,add(holders,1)),504))` | INST |
| I4 | 卖家/买家 | `-rank(ts_rank(divide(sellers,add(buyers,1)),504))` | INST |
| I5 | 金额卖买比 | `-rank(ts_rank(divide(disposed_value,add(acquired_value,1)),504))` | INST |
| I6 | 持仓周转（金额） | `-rank(ts_rank(divide(disposed_value,add(aggregate_equity_value_institutions,1)),504))` | INST |
| I7 | 持仓周转（股数） | `-rank(ts_rank(divide(disposed_qty,add(aggregate_share_count_institutions,1)),504))` | INST |
| I8 | 家数周转 | `-rank(ts_rank(divide(add(buyers,sellers),add(holders,1)),504))` | INST |

### 4.3 Wave 2+ 待派发（结构轴 / 机制替换）

- **结构轴**：`group_rank(x, subindustry/sector)`、`ts_mean(x,66)` 平滑、`ts_decay_linear`、`signed_power`、`trade_when` 门控。
- **机制替换**：risk60 `rsk60_crowding`、`offer−bid`；insider 仓位变化比/显著交易；insiders1 持仓换手。
- **分母替换**：`current_enterprise_value`（FUNDAMENTAL）、`alternative_market_cap_usd`（RISK）——避开 PV 配额。
- **PV 配额**：`÷ ts_mean(volume,22)` 的 DTC 系列最多 5 条，且仅在 Wave 3 之后使用。

---

## 5. 归因与对照实验设计

**Wave 1 的控制变量**：同一外层 `-rank(ts_rank(ts_backfill(·,120),504))`、同一设置
（FAST/decay15/trunc0.05/nanHandling ON/maxTrade OFF）、同一 universe/date；**只换分子**。
⇒ 读数差异可直接归因到"机制"而非"几何/参数"。

**Wave 2 的 A/B**：取 Wave 1 的 S≥1.0 候选，复制成 3 组：
- A：基几何（不变）；
- B：`group_rank(·, subindustry)` 替换外层 `rank`；
- C：`ts_mean(·,66)` 平滑 + 基几何。
三组同设置、同分子 ⇒ 归因到"结构维度"。

**设置 A/B**（只对 Wave 1 的 top2 执行，4 条）：
- `SUBINDUSTRY / decay4 / trunc0.08`（区域默认档）
- `FAST / decay15 / trunc0.05`（未点亮塔实证档）
用于回答"10-31 的赢家档是否仍是今天的最优档"。

**判读口径**（近闸池，非提交）：
- 入池：`S ≥ 1.2`，或 `S ≥ 1.0` 且机制清晰（有符号一致性/对照组成立）；
- 记录 `F / TO / 2Y / SUB / longCount / shortCount`；
- 同族变体用 `compute_mutual_correlation` 去重，避免把同一 PnL 的克隆算成多颗。

---

## 6. 近 10 年数据校验（硬性）

IS 窗口 = `2014-01-01 ~ 2023-12-31`。候选入池前逐条 `get_alpha_yearly_stats(alpha_id)`：
- 2014–2023 **每一年**都要 `longCount > 0 && shortCount > 0 && pnl > 0`；
- 任一年缺失/单边 ⇒ 该候选标注 `data_gap_<year>`，不进近闸池（可留作机制证据）。

> 理由：GBR 多次出现"全期指标漂亮但某些年份零持仓"的候选（AGENTS.md §7.5 第 3 闸）。

---

## 7. 本轮已派发

| 波次 | 数据集 | 条数 | 设置 | 状态 |
|---|---|---:|---|---|
| `s2_unlit_w1_d1` | shortinterest3 | 8 | FAST/decay15/trunc0.05/nanHandling ON/maxTrade OFF | 已派发（2 并发 multisim） |
| `s2_unlit_w1_d1` | institutions6 | 8 | 同上 | 已派发 |

并发纪律：**2 个 multisim 同时在飞**（`WQB_GLOBAL_SLOTS` 现行 cap=2），每批 ≤8 条（GBR multi-sim 上限 8）。

---

## 8. 本轮结果（2026-11-05 收口）

> 完整波次明细、31 条近闸池、机制归因与未完成项见
> [`output_report/GBR_unlit_campaign_20261105.md`](../../../output_report/GBR_unlit_campaign_20261105.md)。

- **9 批 / 72 条新回测**：W1A SI、W1B INST、W2 RISK、W3–W5 SI 结构轴/分母/平滑、W6 INST 结构轴、W7 insiders1、W8 insider_agg_matrix。
- **RA 全闸新增 4 条**（10 年数据全过）：
  `O0AA03E1` S1.73/F1.10（纯 SI 平滑存量）、`qMLL8lPV` S1.72/F1.09（纯 SI `_main` 平滑）、
  `QPvj9m0K` S1.71/F1.06（DTC126，历史复现）、`gJee6MRK` S1.58/F1.05（SI+FUND EV 分母平滑）。
- **近闸池 31 条**（S≥1.0，含 5 条 10-31 历史）；其中 S≥1.2 共 24 条。
  **实际独立机制族约 7 个**：存量/市值/笔数水平、market cap 分母、EV 分母、ADV/sharesout 分母、分组轴、集中度 CoV。
- **★ 新结构杠杆**：`ts_mean(ts_rank(x,504), 22)` 在日频稀疏字段上 **+0.14~+0.24 S、+0.11~+0.20 F、−1.6pp TO**；
  `ts_mean(...,66)` 对季频 institutions6 反而伤（0.95→0.86）⇒ **平滑窗匹配更新频率**。
- **判死复核**：institutions6 上限 0.94、risk60 上限 0.80（crowding 符号镜像成立但弱）、
  insiders1 上限 0.76、insider_agg_matrix 上限 0.73；sentiment 三集沿用 10-31 全灭。
  ⇒ **未点亮塔可产面收敛为 shortinterest3 单集**；该塔要 3 条独立轴才点亮，本轮仍只有 1 条 ⇒ **0 座新塔**。
- **prod/self 未测**：`check_correlation` / `check_self_correlation` 连续 3 次在 MCP 客户端 30s 上限超时；
  按 10-31 教训「prod 未测 = 未定」，不得把 4 条全闸当成可提。

### 8.1 2026-11-05 追加：shortinterest3 全字段补测（W9–W13）

**数据集全集**：GBR `shortinterest` 类别只有 `shortinterest3`（25 字段，cov .849）；相关「做空/借券」集还有
`risk60`（5 字段，cov .6694，已测）、`institutions25`（Fund Short Selling，24 字段，**字段级 cov 全 0**）、
`model239`（Short Selling Model，29 字段，**字段级 cov 全 0**）。⇒ 数据集级无遗漏。

**25 字段全测结果**：
- 借券存量 / 借券市值 / 借贷笔数 → 两条独立腿（S1.35–1.97，全闸）；
- 久期、mean/max/min 费率、费率波动、max−min 价差、`shrt3_bar` → **全弱（−0.66 ~ 0.58）**；
- 集中度/分散度（`vec_stddev/vec_avg`）→ 第三条轴（S1.23–1.34，near-gate），**但 2015/2017/2020 负 pnl，不过 10 年闸**。

**★ 新结构突破（可迁移）**：
1. **`transaction_count` 族是独立第二腿**：`-group_rank(vec_avg(transaction_count_main), subindustry)` 无 mask 即 **S1.86/F1.26**；
   加 `if_else(rank(ts_mean(...,5))>0.9, nan, ...)` 极端笔数掩码后 **S1.97/F1.35**（`vR11n3xQ`）。
   它与存量腿互相关仅 **0.2022**，族内 0.88–0.96。
2. **`ts_decay_linear(ts_rank(x,504),22)` 与 `ts_mean(...,22)` 等效**（存量腿 S1.70/F1.07 vs 1.73/1.10），
   平滑窗 22 优于 66（1.57）与 120（1.38）。
3. **`vec_ir` / `vec_kurtosis` / `vec_skewness` 平台不可用**（W12 全批 `unknown operator`）；
   `vec_stddev` / `vec_avg` / `vec_max` / `vec_sum` 可用。
4. **10 年闸是第三腿的硬墙**：CoV 三条最好 S1.32–1.34，但 2015/2017/2020 三年负 pnl；
   在「近十年每年 pnl>0」约束下，SHORTINTEREST 塔仍只有 2 条可用的独立全闸腿（需 3 条才点亮）。
5. **regime 门控修不动第三腿**（W14，8 条）：用同数据集内的市场 SI 水平 / 交易活跃度 / 分散度趋势 /
   费率水平做 `if_else` 门控，最好 `WjOONrZd` S1.50/F0.93 但 **2Y0.98**；其余 1.03–1.46。
   ⇒ **第三腿封盘**；SHORTINTEREST 塔在现行约束下不可点亮。
6. **算子变换（W15，论坛/ideas 取证）**：
   - `signed_power(x,0.5)` 对 txn÷ADV 近闸有效：1.62/0.97 → **`pwdd7Za6` 1.69/1.04/2Y2.49/RA0 全闸（10 年过）**；
   - `ts_target_tvr_decay(0.05)` 对 loan count 等价于平滑：**`KPJJLQVj` 1.71/1.08/RA0 全闸**；
   - 对 CoV：`signed_power`/`quantile` 把 1.34 推到 **1.45**，仍 near-gate（10 年问题未解）；
   - **verifier 算子表不含 `ts_quantile` / `ts_max_diff` / `ts_decay_linear`**（报「表达式不完整」）；
     `tools_sim.py` 的 `failed_expressions` 键是 **1-based**（`str(i+1)`），排查别按 0-based 读错位。
