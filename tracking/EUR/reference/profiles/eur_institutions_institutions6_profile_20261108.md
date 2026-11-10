# EUR × institutions6 字段画像（2026-11-08）

> 平台目录：11/11 字段全量拉取（complete=true，MCP get_datafields，TOPCS1600/D1）
> **2026-11-09 复核（goal eur15）**：MCP 重拉 complete=true，11 字段 cov 不变；数据集级 aC 99→106（+7/6h，拥挤上升）；塔位仍 INSTITUTIONS 0/3 未点亮。analyst7 载体因 ANALYST 塔点亮（10颗）禁用于新波，小腿载体改 insider_agg_matrix/news18。见 s0_institutions_scan_20261109.md。
> 塔位：INSTITUTIONS(×1.1，本季 0/3 未点亮)；字段级拥挤度：全字段 userCount 3–17 / alphaCount 1–24（极冷门）

## 一、字段清单与六维画像

| # | 字段 | 类型 | cov | 更新频率 | 分布特征 | 可用性 | 潜在适用性 |
|---|---|---|---|---|---|---|---|
| 1 | count_institutional_buyers_security | MATRIX | 0.9976 | 季频（监管申报期） | 计数型右偏；差分后近似对称 | uC15/aC22 冷门 | **小腿首选**：(B−S)/H 买卖广度（leAXvaLn 实证 2Y+0.78） |
| 2 | count_institutional_sellers_security | MATRIX | 0.9976 | 季频 | 同上 | uC17/aC24 | 同 #1 分母腿 |
| 3 | count_institutional_holders_security | MATRIX | 0.9976 | 季频 | 存量水平，慢变 | uC6/aC7 | 同 #1 分母；亦可做门控（IND levk5JYN rank>0.5 先例） |
| 4 | market_value_institutional_shares_acquired | MATRIX | 0.9976 | 季频 | 金额右偏重尾 | uC10/aC12 | 金额流向小腿（历史"金额深度取负 S0.75"半有效） |
| 5 | market_value_institutional_shares_disposed | MATRIX | 0.9307 | 季频 | 同上 | uC3/aC4 | 同 #4 对冲腿 |
| 6 | quantity_institutional_shares_acquired | MATRIX | 0.9976 | 季频 | 股数右偏（拆股敏感） | uC13/aC18 | 股数流向小腿（"股数口径"历史有 2 条回测） |
| 7 | quantity_institutional_shares_disposed | MATRIX | 0.999 | 季频 | 同上 | uC8/aC11 | 同 #6 对冲腿 |
| 8 | aggregate_equity_value_all_owners | MATRIX | 0.9976 | 季频 | 水平量，慢变 | uC6/aC6 | 仅分母（机构渗透率 INST/ALL） |
| 9 | aggregate_equity_value_institutions | MATRIX | 0.9976 | 季频 | 同上 | uC7/aC8 | 机构渗透率分子 |
| 10 | aggregate_share_count_all_owners | MATRIX | 0.9976 | 季频 | 同上 | uC7/aC8 | 同 #8 股数口径 |
| 11 | aggregate_share_count_institutions | MATRIX | 0.9976 | 季频 | 同上 | uC13/aC16 | 同 #9 股数口径 |

## 二、机制分组与模板映射（10 模板，覆盖全部 11 字段）

- **G1 买卖广度**（#1,2,3）：T1 净广度比 (B−S)/H（已验证小腿）；T8 买入占比 B/(B+S)；T5 广度动量 ts_delta((B−S)/H,66)
- **G2 金额流向**（#4,5）：T2 金额净流向 rank(MVA−MVD)；T7 金额失衡率 (MVA−MVD)/AEV_INST
- **G3 股数流向**（#6,7）：T3 股数净流向 rank(QA−QD)；T9 金额-股数分歧 subtract(rank(MV净流), rank(Q净流))
- **G4 持仓水平**（#8,9,10,11）：T4 机构渗透率 AEV_INST/AEV_ALL；T6 户均规模 AEV_INST/H；T10 慢门控 trade_when(rank(渗透率)>0.5, CORE, -1)

## 三、EUR 历史实证（判死边界）

- **ATOM 主信号判死**（EUR-INST6-INSTITUTIONS-TOWER-EXHAUSTED / EUR-INSTITUTIONS6-COLD-ZERO-YIELD）：22 条 × FAST/SUBIND 两档最好 S 0.56；广度版 S 0.86 但 2Y −0.30（机制存在但近期断档）；boundary_total/ts_mean(holding_value,55) 形态 TO 爆到 1.13。
- **小腿形态可用**：leAXvaLn（ebi 修订广度载体 × 1.2×[(B−S)/H 广度 rank − 0.5]）S1.78/F1.06/2Y2.10/sub1.12/failed_ra=0，pyramids [INSTITUTIONS×1.1, ANALYST×1.3]，UNSUBMITTED。
- **IND 先例**：levk5JYN 机构持股比例 rank>0.5 门控，prod 0.55。

## 四、结论

1. institutions6 主信号禁做（已判死，覆盖判死豁免不适用——cov 0.9976 达标，是信号层死）。
2. 唯一用途：组合小腿（点亮 INSTITUTIONS 塔）+ 慢门控。小腿配方 = `multiply(1.2, subtract(group_rank(ts_backfill(<读数>,120), subindustry), 0.5))`。
3. 全字段覆盖计划：G1-G4 十模板按波次派发，2 臂/批，ANALYST+INSTITUTIONS 组合配额内交付 ≤3 颗。
