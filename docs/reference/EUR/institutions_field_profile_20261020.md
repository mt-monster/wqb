# EUR × Institutions 类别 — 字段画像与回测档案

> 日期：2026-10-20 ｜ 设置：TOPCS1600 / SUBINDUSTRY / decay4 / trunc0.08 / maxTrade ON / nanHandling ON
> 纪律：full-coverage，三道覆盖闸全过（institutions6: 11/11 字段·3 族；fund_holdings_panel: 30/30 字段·4 族）

## 一、数据集全量清单（平台 EUR/TOPCS1600）

| ID | 名称 | 字段 | 覆盖 | 已有alpha | valueScore | 金字塔倍率 |
|---|---|---:|---:|---:|---:|---:|
| fund_holdings_panel | Global Institutional Fund Holdings（账户级） | 30 | 0.881 | **35** | 2.0 | 1.1 |
| institutions6 | Institutions and Beneficial Stake Ownership（13F） | 11 | 0.992 | 94 | 2.0 | 1.1 |

**合计 41 字段全部实测覆盖**

## 二、字段画像

### 2.1 institutions6（11 MATRIX，cov 0.93–1.00）
| 维度 | 字段 | 经济含义 | 实测 |
|---|---|---|---|
| **F1 买入侧** | quantity_institutional_shares_acquired / market_value_institutional_shares_acquired / count_institutional_buyers_security | 机构买入股数/金额/买家数 | 净价差 S 0.15–0.46 |
| **F2 卖出侧** | quantity_institutional_shares_disposed / market_value_institutional_shares_disposed / count_institutional_sellers_security | 机构卖出股数/金额/卖家数 | 同上 |
| **F3 持股水平** | aggregate_share_count_{all_owners,institutions} / aggregate_equity_value_{all_owners,institutions} | 持股总量/市值 | 冠军栈 S −0.04~0.62 |
| **F4 持有广度** | count_institutional_holders_security | 持有机构数 | S 0.62（该集最佳） |

- **更新频率**：季频（13F），TO 仅 0.014–0.057
- **可用性**：cov 0.93–1.00（最佳覆盖）
- **实测结论**：**净买入广度（Griffin-Xu 经典信号）在 EUR 无效**（S 0.46，2Y −0.36）；13F 流已被充分套利

### 2.2 fund_holdings_panel（30 VECTOR 事件型，cov 0.84–0.92）
| 维度 | 字段 | 经济含义 | 实测 |
|---|---|---|---|
| **V1 持仓水平** | security_holding_usd_value / mean_security_weight / holder_account_total | 持仓市值 / 平均权重 / 持有账户数 | `vec_sum` S 0.62（该集最佳） |
| **V2 集中度** | herfindahl_index_holdings / holding_value_distribution_score | HHI / 分布集中度 | S −0.34~0.56 |
| **V3 交易流** | security_transaction_usd_value / transaction_value_distribution_score | 交易额 / 分布 | `vec_sum` S 0.59–0.62 |
| **V4 新开仓** | boundary_transaction_{usd_value,total} / stable_boundary_trade_count_21d | 建仓交易额/笔数/稳定账户建仓 | S 0.31–0.60 |
| **V5 大单与conviction** | large_trade_count_50bps / top_weighted_account_number / top_weighted_transaction_number | 大单 / 高权重账户 | S 0.32–0.59 |
| **V6 _active 变体** | 上述 15 字段的 _active 版（剔被动） | 主动型基金口径 | 与基础版同向 |

- **更新频率**：日频持仓快照，但账户持仓变动缓慢 ⇒ 有效 TO 0.01–0.19
- **事件型约束**：VECTOR 事件字段**不支持事件层算术**（同 insiders 发现），须先 `vec_*` 聚合

## 三、适用模板与实测

| 模板 | 骨架 | 适用 | 实测最佳 |
|---|---|---|---|
| 净价差（同源） | `subtract(rank(bf(A,66)), rank(bf(B,66)))` | institutions6 买卖配对 | S 0.46 |
| 买入强度比 | `divide(acquired, add(disposed, 1e-4))` | institutions6 | S −0.07 |
| 冠军栈 | `signed_power(ts_zscore(bf(F,66),126),1.5)` | 水平类字段 | S ≤0.62 |
| **向量聚合** | `vec_sum(F)` / `vec_avg(F)` | fund_holdings 全部 | **S 0.62（最佳）** |
| 比率 | `divide(vec_sum(A), add(vec_sum(B),1e-4))` | 占比/换手 | S −0.20~0.44 |
| **size 正交化** | `vector_neut(vec_sum(X), vec_sum(holding_usd_value))` | 剥 size | **S 0.11（证否）** |

## 四、回测台账（关键行）

| wave | 表达式 | S | F | TO | 2Y | sub | 判定 |
|---|---|---:|---:|---:|---:|---:|---|
| w750 | `vec_sum` 类 institutions6 持股水平 | −0.04~0.62 | ≤0.29 | 0.01–0.06 | −1.07~1.05 | −0.10~0.51 | 弱 |
| w750 | 净买入广度（buyers−sellers） | 0.46 | 0.19 | 0.028 | **−0.36** | 0.33 | 弱 |
| w751 | `vec_sum(security_holding_usd_value)` | **0.62** | 0.48 | 0.013 | 1.21 | 0.31 | 该类别最佳 |
| w751 | `vec_sum(top_weighted_account_number)`（conviction 账户） | 0.55 | 0.35 | 0.016 | **1.33** | 0.25 | 次佳 |
| w751 | `vec_sum(security_transaction_usd_value)` | 0.59 | 0.45 | 0.013 | 1.13 | 0.33 | 弱 |
| w751 | `vec_sum(boundary_transaction_usd_value)`（新开仓） | 0.55 | 0.33 | 0.136 | 1.03 | 0.28 | 弱 |
| **w752** | **`vector_neut(conviction账户, 持仓额)`** | **0.11** | 0.02 | 0.022 | 1.30 | 0.15 | ★ 证否 |
| **w752** | **`vector_neut(交易额, 持仓额)`** | **0.10** | 0.02 | 0.184 | 0.16 | 0.45 | ★ 证否 |
| w752 | conviction 账户占比 | 0.44 | 0.21 | 0.020 | 1.30 | 0.11 | 弱 |

## 五、★ 归因（决定性命中）

**size 正交化实验是决定性证据**：
- `vec_sum(top_weighted_account_number)`：S **0.55** → size 正交后 **0.11**（降 −0.44）
- `vec_sum(security_transaction_usd_value)`：S **0.59** → size 正交后 **0.10**（降 −0.49）

⇒ **institutions 信号本质是 size（市值）代理**：
- 持仓额、conviction 账户数、交易额都与市值强相关
- **2Y（1.2–1.33）> 全样本（0.55–0.62）** 的形态 = size 因子近两年强势的表现，不是 alpha 变强
- 剥掉 size 后信号归零 ⇒ 无独立信息

**institutions6（13F 流）**：净买入广度等经典信号 2Y 为负（−0.36~−1.07）⇒ 季频 13F 流已被充分套利。

## 六、结论
**EUR institutions 类别（2 数据集 / 41 字段全量覆盖）无过闸候选**：最佳 S 0.62（闸 1.58），且机制层证明其为 size 代理（正交后归零）。判死证据链完整。

## 七、存档索引
- 字段全集：`tracking/EUR/reference/{institutions6,fund_holdings_panel}_fields.json`
- 覆盖阀候选：`tracking/EUR/candidates/{institutions6,fund_holdings_panel}.json`
