# EUR / institutions 塔收口报告（2026-11-20）

> 塔位 EUR/D1 **INSTITUTIONS 0/3**（未点亮）｜数据集：`fund_holdings_panel`（30 字段全 VECTOR，cov 0.88）+ `institutions6`（11 字段，cov 0.99）
> 结论：**两集 ATOM 均卡 prod 墙；门控/换经济逻辑/组 regular 三形态全灭 ⇒ PROVISIONAL（信息源级）**

## 1. 本轮 31 臂（全部收割入库，wave=mcp-20261120）

| 批次 | 臂数 | 内容 | 最优 |
|---|---:|---|---|
| 段1 事件门控矩阵 | 8 | `trade_when(<presence 字段> > 0, zq378ELo核, -1)` × 8 门控字段 | RReAPWkn S1.51/F0.93/2Y2.44 |
| 段2 换经济逻辑 | 8 | conviction 广度 / HHI / 分布分 / 平均权重 / 大单 / 差分 / 比值 | wpo9vx16 S0.33 |
| 段3 组 regular 三形态 | 8 | residual(vector_neut) ×4 / ratio(divide) ×2 / gating ×1 / 简化核 ×1 | j2aeMx2E S0.70 |
| 探针 | 7 | 纯 MATRIX 臂（修复 vec_* / UNITS 后） | 已并入上列 |

## 2. 关键判据

### 2.1 门控（presence）在本族**无效**——与 earningscall 相反

| 臂 | S | F | 2Y | prod |
|---|---:|---:|---:|---:|
| zq378ELo（**无门控基线**） | **1.64** | **1.05** | **2.61** | **0.8887** |
| RReAPWkn（`transaction_account_total > 0` 门控） | 1.51 | 0.93 | 2.44 | 0.8548 |

**8 个门控臂无一超过无门控基线**；prod 只降 0.034（0.8887→0.8548），远不够 0.19 的缺口。

> ★ **重要边界修正**：`trade_when(presence>0, …)` 只对**低覆盖事件型**数据集有效
> （earningscall_sentiment cov 0.51 → S 0.51 抬到 1.76）；本族 cov 0.84–0.92（连续日频）
> ⇒ 门控只做减法（砍掉无事件日的信息），**必然降 S**。**门控前先看 coverage**：cov<0.6 值得试，cov>0.8 基本无效。

### 2.2 该面板只有一个经济逻辑有信号

「换经济逻辑」8 臂（conviction 广度 / HHI / 交易分布分 / 持仓分布分 / 平均权重 / 大单 / 差分 / 比值）**全灭**（S ≤ 0.33），
而 `stable_boundary_trade_count_21d_active`（21 日内无前次边界交易的账户所做的边界交易 = **新意度**）单独就 S1.64。
⇒ 机制定位精确：**只有「机构新意建仓/清仓的持续性」有定价信息**，其余持仓/交易广度读数全是噪声。

### 2.3 组 regular 三形态全灭（residual / ratio / gating）

| 形态 | 臂 | 最优 S |
|---|---:|---:|
| residual（`vector_neut` 两集互残差） | 4 | 0.48 |
| ratio（两集比值） | 2 | 0.28 |
| gating（持仓面板门控买家比例） | 1 | 0.70 |
| 简化核（去 winsorize/neutralize） | 1 | 0.46 |

**归因**：institutions6（买家比例）与 fund_holdings_panel（持仓变动）**同属「机构活动」信息源、信号高度同源**
⇒ 正交后残差无信息、比值无差异。**同源两集组腿无效**（这是本轮最有价值的否定结论，
因为它同时解释了为何「同塔两集 ATOM 各自 prod 都高」——它们其实是同一个因子的两个读数）。

### 2.4 ATOM 已有最优件（除 prod 外全闸）

`zq378ELo` = `ts_mean(group_zscore(vec_avg(stable_boundary_trade_count_21d_active), country), 22)`，
TOP2500×SUBINDUSTRY×decay4：**S1.64 / F1.05 / 2Y2.61 / sub1.17 / TO12% / DD1.9%**，
`risk_neutralized_sharpe` 有值（标准档），`pyramids.list` = EUR/D1/INSTITUTIONS（mult 1.1）——
**唯一卡 prod 0.8887**（生产池里「机构持仓变动」因子已饱和）。

## 3. 判定

| 维度 | 结论 |
|---|---|
| ATOM | institutions6 标准档 S1.35（FAST 风险线 S2.22 不算）→ prod 0.8257 墙；fund_holdings_panel S1.64 → prod 0.8887 墙 |
| 门控 | 8 臂全灭（S↓、prod 仅降 0.034）⇒ 本族不适用 |
| 换经济逻辑 | 8 臂全灭 ⇒ 只有「新意度」一个逻辑有信号 |
| 组 regular（residual/ratio/gating） | 8 臂全灭 ⇒ 两集同源，组腿无效 |
| **最终** | **PROVISIONAL（信息源级 prod 墙）**。institutions 塔在本区靠 ATOM 与组腿两条路均已闭合；未提交任何 alpha |

## 4. 沉淀

1. **presence 门控的适用条件**（今日新增判据）：cov < 0.6 的事件型 → 门控是强杠杆；
   cov > 0.8 的连续型 → 门控必降 S，无效。
2. **同源两集组腿无效**（residual/ratio/gating 三形态全灭）：组腿前先问「两集是不是同一个信息源的两种读数」。
3. **prod 墙的量级感**：0.8887（机构持仓变动）vs 0.8257（机构买家比例）——都是「机构活动」因子的经典实现；
   降 prod 需要**换信息源**（如把持仓数据当辅助腿配非机构信息源），而不是在本源内换实现。
