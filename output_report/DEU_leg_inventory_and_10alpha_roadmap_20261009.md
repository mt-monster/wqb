# DEU 腿占用清单与「10 颗 alpha」路线图（2026-10-09）

## 一、本账户现状（平台实读 `/users/self/alphas`）

**总 ACTIVE/SUBMITTED = 98 颗**，区域分布：

| 区域 | 已提交 | 相对空间 |
|---|---|---|
| KOR | 15 | 中 |
| IND | 14 | 低（分析师/价量族拥挤）|
| GBR | 12 | 中 |
| GLB | 12 | 中 |
| **DEU** | **8** | **低（分析师族极拥挤）** |
| USA | 8 | 中 |
| ASI | 6 | **高** |
| HKG | 4 | **高** |
| EUR | 3 | **高** |

## 二、DEU 已占用的 8 条腿（新 alpha 必须避开）

| alpha_id | 提交日 | 涉及字段 | 塔/中性化 |
|---|---|---|---|
| `2rmGAPqN` | 10-09 | `inst1_valueeur` / `inst1_holdings` / `inst1_tradesignificance` | INSTITUTIONS+OTHER / FAST |
| `58gkLAkk` | 10-07 | `mean_estimate_change_pct_f12m_earnings_14d_4` | SUBINDUSTRY |
| `JjxrYjre` | 09-14 | `mean_buy_transaction_count` + earnings_14d_4 + ebitda_90d_3 | SUBINDUSTRY |
| `2rOe10qY` | 09-14 | earnings_14d_4 + ebitda_90d_3 + `predicted_surprise_f12m_ebitda_4` | SUBINDUSTRY |
| `vRk6og8b` | 09-13 | earnings_14d_4 + ebitda_14d_4 + `mean_loan_rate_main` | SUBINDUSTRY |
| `Vk65zLzG` | 09-13 | **`directional_indicator`** + ebitda_14d_4 + ebitda_90d_3 | SUBINDUSTRY |
| `883Y3bAW` | 09-13 | `closing_price_dlr2` + earnings_14d_4 + ebitda_14d_4 | SUBINDUSTRY |
| `blRnKEk6` | 09-13 | earnings_14d_4 + ebitda_90d_3 + `mean_loan_rate_main` | SUBINDUSTRY |

**⇒ 三条硬结论**：
1. **分析师修正族（`mean_estimate_change_pct_*`）已被我们自己的 6 颗占据** ⇒ DEU 该族已饱和，任何变体 self 必高。
2. ★ **`directional_indicator` 已被 `Vk65zLzG` 用过** ⇒ 修正 W248 判断：该字段**不是白空间**
   （平台 `alphaCount=39` 含我们自己的）。**但 `directional_significant_value_1/2/3` 的 `alphaCount=0` 仍是真白空间**（我们也没用过）。
3. **DEU 剩余可用方向**：`insider_agg_matrix` 中**从未被我们碰过**的字段（买入类/显著性类/高管类）。

## 三、「10 颗 REGULAR」路线图

### 硬约束
- **REGULAR 配额 = 4 颗 / ET 日**（全账户）⇒ 10 颗需 **≥3 个 ET 日**
- 每颗须过：IS 9 项硬闸 + prod<0.7 + self<0.7 + 稳健性闸（skill 内部）
- **self 自锁**：同结构变体必被拦 ⇒ 10 颗必须是 **10 条不同的腿**

### 分配建议（按区域空间 + 我们的配方可迁移性）

| 批 | 区域 | 数据集/信号族 | 计划颗数 | 依据 |
|---|---|---|---|---|
| ~~A~~ | ~~DEU~~ | ~~`insider_agg_matrix`~~ | ~~2~~ | ❌ **判死**（W248–W252：DEU 最好 S0.69、EUR 最好 S0.57；高频日更不匹配 D1）|
| B | EUR | 内部人 / 分析师修正 / 价量（3 颗已提交 ⇒ 空间大）| 3 | 空间最大 |
| C | ASI | 内部人 / 短息 / 新闻情绪 | 2 | 6 颗已提交，空间大 |
| D | HKG | 内部人 / 卖空（`shrt55_*`）| 2 | 4 颗已提交，空间最大 |
| E | USA / GLB | 待定 | 1 | 补齐 |

**⇒ 关键依赖**：把本次已验证的「破闸配方」迁移到新区域：
```
signal  = <流量字段> / (<存量字段> + ε)          # 信念强度
mask    = if_else(and(买入侧判定, 显著性门槛), 1, 0)   # 只取机会型买入
accum   = ts_sum(mask, <长窗 176~220>)              # 长窗 = 三维同向改善
ranked  = winsorize(group_rank(accum, <图谱簇轴>), std=2)
alpha   = tail(ranked, lower=0.25, upper=0.75, newval=0.5)
```
⚠ **不可跨区类比**（R1 铁律）⇒ 每个区域**必须在本地重测全链**（字段存在性、类型、settings 档位、稀疏/稠密、图谱轴可用性）。

## 四、当前阻塞

**平台回测队列严重拥堵**：W248（8 条）+ 2 条隔离探针共 10 条 sim，发出 10+ 分钟仍 `0/0 terminal`。
两轮 W248 均 8/8 `FAIL`+`alpha=None`+无细节 ⇒ 判为**占槽**（今日已40+批）。
**⇒ 等队列缓解后**：① 先读 ON/OFF 探针确认 settings；② 重发 `cache/w248_g1.txt`（表达式已存）。


---

## 五、路线修订（2026-10-10 00:05）

### ❌ 已判死
- **`insider_agg_matrix` 双区判死**（30 条证据，见 `RULES.md` Q42）⇒ 路线图 A 批取消。

### ✅ 仍可用
- **EUR（3 颗已提交，空间最大）**：`insider_agg_matrix` 已死 ⇒ 转 **EUR 的 MODEL(49 数据集) / OTHER(38) / PV(21) / NEWS(20) / ANALYST(16)** 族
  - EUR 合法 universe：TOP2500 / TOP1200 / TOP800 / TOP400 / TOPCS1600
  - **EUR 有 1200 个图谱簇轴** ⇒ 核心杠杆可用
- **HKG（4 颗）**：合法 universe TOP800 / TOP500
- **ASI（6 颗）**：MINVOL1M / MINVOL10M / TOP500
- **JPN（0 颗已提交！）**：TOP1600 / TOP1200 —— **完全处女区，空间最大**
- **AMR（0 颗已提交！）**：TOP600 —— 同样处女
- **CHN（0 颗已提交！）**：TOP2000U —— 但 CHN 有专属规则，谨慎

★ **新发现两个完全未提交的区域：JPN 与 AMR** —— 按 R2（一条腿只出 1 颗），处女区是最容易出 alpha 的地方。

### 现实的进度评估
- 目标 10 颗；**当前已提交本战役 1 颗**（`2rmGAPqN`）
- **配额 4 颗/ET 日** ⇒ 10 颗需 ≥3 个 ET 日
- 每颗需过 IS 9 闸 + prod<0.7 + self<0.7 + 稳健性闸 ⇒ **不是简单重复，每颗都是一条新腿**
- **建议路线**：优先 **JPN / AMR 处女区**（无 self 历史包袱）→ 其次 EUR/HKG


---

## 六、路线修订 v2（2026-10-10 04:00）—— **锁死 DEU**

**用户明令**：「永远不要考虑换 region，锁定 DEU 挖掘」⇒ 已写入 `MEMORY.md` 铁律区。
**v1 路线图里的 JPN / AMR / EUR / HKG / ASI 分配全部作废。**

### DEU 现实盘点（本战役累计）

| 腿 | 状态 |
|---|---|
| 分析师修正族（`mean_estimate_change_pct_*`）| 6 颗已提交 ⇒ **饱和** |
| `institutions1` + 伙伴图谱簇 | 1 颗已提交（`2rmGAPqN`）⇒ **自锁** |
| `directional_indicator` | 被 `Vk65zLzG` 占 |
| `insider_agg_matrix` | **双区判死**（DEU 最好 S0.69）|
| `eps_y1_estimate_change_3mo`（新 ALIVE）| **S1.82 / fit1.62**，唯一卡 2Y 1.12（7 类杠杆全败）|
| `analyst_factor_signals` 其它字段 | 均不如上者（最高 S1.41）|
| `model26` / `pattern_scores` / `analyst7` 代表字段 | **两轮（有/无 rank）均败 ⇒ 初步判死**（样本仅 7 字段）|

### 剩余可用方向（DEU 内）
1. **★ 未测 MATRIX 池系统性开采**（11738 字段）—— 但需**先按描述筛出有机制假设的字段**，避免盲扫
   - 优先数据集：`predictive_starmine`(502, cov0.97)、`model264`(354, 1.0)、`other455`(300 非轴字段)
2. **攻 2Y 墙的候选**（`eps_y1_estimate_change_3mo` S1.82）—— 剩未试：换 universe（DEU 仅 TOP500，
   **不可**）、`trade_when` 状态门控（历史 8 次实证均降 S）
3. **新数据集族**：`pattern_scores` 里**非相似度类**字段（如 `_quantile95_` × 其它形态名）

### 现实评估
DEU 已有 8 颗 ACTIVE + 6 颗分析师族饱和 ⇒ **在 DEU 内挖新 alpha 的难度显著高于处女区**，
但按用户指令**锁定不换区**，因此后续策略 = **深挖未测 MATRIX 池** + **啃 2Y 墙**。
