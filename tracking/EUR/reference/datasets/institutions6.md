# institutions6 · EUR / TOPCS1600 / D1 字段画像

> 类型 MATRIX · 11 字段 · cov 0.93–1.0 · category = **institutions**（×1.1，未点亮塔）
> 采集：2026-11-06 · αC 最高 24（卖出家数）

## 0. 字段

| 字段 | αC | 语义 |
|---|---|---|
| `count_institutional_sellers_security` | 24 | 卖出机构家数 |
| `count_institutional_buyers_security` | 21 | 买入机构家数 |
| `quantity_institutional_shares_acquired` | 18 | 买入股数 |
| `aggregate_share_count_institutions` | 13 | 机构持股总量 |
| `market_value_institutional_shares_acquired` | 12 | 买入金额 |
| `quantity_institutional_shares_disposed` | 11 | 卖出股数 |
| 其余 holders/value 存量 | ≤7 | 存量轴 |

## 1. 机制

JMZ(2003) 买卖不对称迁移：机构买入家数/股数应有信息，卖出多为再平衡。套用 insider 战役最优骨架（88d zscore 栈 × SLOW_AND_FAST）。注意：本集是季报低频 MATRIX，窗口 ≥66。

## 2. 实测

**第一批（已终态,multisim `2SFPlRcuQ4HsaFuco979gCh`,88d zscore 栈 × SLOW_AND_FAST）——弱信号**：

| 字段 | alpha id | S | F | 2Y | sub | robust |
|---|---|---|---|---|---|---|
| 买入家数 | `d5W3x1ov` | **0.45** | 0.13 | −0.53 | 0.46 | 0.43 |
| 买入股数 | `0mYN7r5k` | 0.01 | 0 | 0.10 | 0.22 | 0.11 |
| 卖出家数 | `78Lvw6lL` | 0.36 | 0.10 | −0.37 | 0.31 | 0.21 |
| reverse 卖出家数 | `9qxdwWke` | −0.36 | −0.10 | 0.37 | −0.31 | −0.21 |

**归因**：买卖不对称方向微弱存在（买入 0.45 > 卖出 0.36），但强度远不够；股数读数归零（规模噪声主导）。与 insider 成功骨架同构却弱一个数量级——机构持仓是季频披露、信息半衰期与内部人日频申报不同。下一步试：① 密度模板（ts_rank 自身基线）；② 净买入（buy−sell）；③ 换 FAST / 更长窗口 252。

**第二批密度/净买入（已终态,multisim `3c3sLz2Om55d8I15sMK2KPg`,FAST/decay15）**：

| 变体 | alpha id | S | F | 2Y |
|---|---|---|---|---|
| −ts_rank(buyers,66/252) | `kqNW015K` | **−0.88** | −0.42 | 0.05 |
| 净买入家数 zscore 栈 | `RREl82Xo` | 0.21 | 0.05 | −0.56 |
| −ts_rank(净买入,66/252) | `omEJl3Qm` | −0.89 | −0.37 | −0.99 |
| 买入家数 252d zscore | `1YNlda66` | 0.34 | 0.12 | 1.41 |

**关键发现**：`−ts_rank(buyers)` S=−0.88 ⇒ 正向 `ts_rank(buyers)` 预期 ≈+0.88——机构买入家数异常高 → 后续超额（「聪明钱跟随」，与新闻密度「高→反转」方向相反）。已提交正向密度版（multisim `VCUD0g4n4jNc3wiufRvgoe`）。

**正向密度结果（已终态）**：

| 变体 | alpha id | S | F | 2Y | sub | robust |
|---|---|---|---|---|---|---|
| buyers 66/252 | `kqNW0vzd` | 0.88 | 0.42 | −0.05 | 0.53 | 0.50 |
| buyers 88/252 | `1YNldOrX` | **0.95** | 0.47 | 0.04 | 0.52 | 0.50 |
| 净买入 66/252 | `YP1E08RR` | 0.89 | 0.37 | 0.99 | 0.67 | 0.12 |
| 股数 acquired 66/252 | `A1VrPrRg` | 0.52 | 0.15 | **1.64** | 0.59 | 0.49 |

**归因**：正向密度最高 0.95，方向确认但强度不足（差 1.7×）；2Y 在该字段族普遍低（~0）——机构买入家数的 alpha 集中在早段年份。**institutions6 初判：首探针 + 密度两波 8 条，最大 |S|=0.95，距闸 1.7×,转出该集**,按快判死规则还差 0 条探针即可触发（新集 8 探针无 |S|≥0.5——已 8 条且仅 1 条 ≥0.5 压线）,先并行测试另一个 institutions 集（fund_holdings_panel）再定。
