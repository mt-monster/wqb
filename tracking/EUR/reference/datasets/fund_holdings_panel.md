# fund_holdings_panel · EUR / TOPCS1600 / D1 字段画像

> 类型 VECTOR · 30 字段 · cov 0.84–0.92 · category = **institutions**（×1.1，未点亮塔）
> 采集：2026-11-06 · αC 合计 42（最高 `security_holding_usd_value` αC=10）

## 0. 字段目录（语义族）

| 族 | 字段（基版/active 双写,取基版） | 经济含义 |
|---|---|---|
| **边界交易**（新建仓/清仓） | `boundary_transaction_total` / `_usd_value` / `stable_boundary_trade_count_21d` | **新建仓=买入信念最强**（主动决策）,清仓=退出;stable_21d 过滤频繁进出 |
| **拥挤/集中度** | `herfindahl_index_holdings` / `_transactions` / `holding_value_distribution_score` / `transaction_value_distribution_score` | HHI 拥挤度——可做反向或门控 |
| **广度** | `holder_account_total` / `transaction_account_total` | 持有/交易账户数=机构关注度 |
| ** conviction** | `top_weighted_account_number` / `top_weighted_transaction_number` | 重仓持有/交易账户数——机构 conviction 代理 |
| **规模** | `security_holding_usd_value` / `security_transaction_usd_value` / `mean_security_weight` | 存量/流量/权重 |
| **大单** | `large_trade_count_50bps` | 超基金 AUM 0.5% 的大额交易笔数 |

## 1. 五问

| # | 问 | 答 |
|---|---|---|
| 1 | 时间 | 日频基金持仓流——比 institutions6 的季报更精细,**事件流量** |
| 2 | 相对性 | 家数/HHI 天然规模无关;USD 值需标准化 |
| 3 | 被定价谁 | 新建仓（boundary）与 conviction（top_weighted）是「聪明钱主动决策」;清仓反向 |
| 4 | 拥挤 | αC≤10,低竞争 |
| 5 | 事件 | 日频连续,`ts_rank` 自身基线 + 截面 rank 双测 |

## 2. 第一批探针

1. `ts_rank(ts_mean(boundary_transaction_total, 66), 252)` 正向（新建仓异常高→跟随）
2. `ts_rank(ts_mean(stable_boundary_trade_count_21d, 66), 252)`（更 durable 的新建仓）
3. `ts_rank(ts_mean(top_weighted_account_number, 66), 252)`（conviction 持有）
4. `reverse(...herfindahl_index_holdings...)`（拥挤反转）
5. `ts_rank(ts_mean(holder_account_total, 66), 252)`（机构关注度）

@ FAST / decay 15 / TOPCS1600（机构字段吃窄宇宙——institutions6 实测）

## 3. 实测

**第一批（已终态,multisim `32UNtU69s4w8c1e1nYPSULm`）——全噪声,快判死归档**：

| 变体 | alpha id | S | F | 2Y |
|---|---|---|---|---|
| boundary_total | `leA5WrW7` | −0.12 | −0.02 | −0.37 |
| stable_boundary 21d | `9qxdpJpe` | −0.12（与上逐位相同——字段冗余） | | |
| top_weighted_account | `WjOoA97k` | −0.20 | −0.06 | 0.35 |
| reverse HHI | `pwdMN8j6` | **0.48** | 0.15 | −0.30 |
| holder_account_total | `A1VrGkle` | −0.20（与 top_weighted 逐位相同） | | |

**归因**：本集是日更连续面板（非稀疏事件）,`vec_count` 退化为 0/1,密度模板不适用;boundary/conviction 家数族无截面信息。HHI 反向（集中度异常低→跑赢）是唯一读数但 0.48 <0.5 判死线。**快判死归档（5 探针,max |S|=0.48）,不再投入。**
