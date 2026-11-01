# USA / insider_trx_matrix 字段画像（S1 级 · 2026-10-30）

> 数据集元数据：**insider_trx_matrix** / 16 字段 / cov 0.7704 / **userCount 274 / alphaCount 仅 1** / valueScore 4.0 / pyramidMultiplier 1.7
> 区域 USA / D1 ｜ category = **OTHER** ｜ 塔位：USA/D1/OTHER（mult 1.4）
> **本画像结论：这是 USA 唯一一个「既有强候选、又被几乎完全忽略」的数据集 —— alphaCount=1 意味着几乎没人用过 ⇒ prod 天然低。**

---

## 1. 为什么它此前被漏掉

历史台账里**只把 `insider_trx_matrix` 归到「insiders 语义」**，从未按 **OTHER 塔（mult 1.4，本季计数 1/3）** 来挖。
实际塔位以平台 `pyramids.list` 为准：`vROPEJ8w` / `1Yj08nb6` 的 `pyramids.list = [{"name":"USA/D1/OTHER","multiplier":1.4}]` ⇒ **属 OTHER 塔，不属 INSIDERS 塔**。

⇒ **「数据集 category」不等于「塔位」**。分类是平台元数据字段，塔位是 alpha 级别的属性（`pyramid_short` / `pyramids.list`）。选靶时必须两者都查。

---

## 2. 已验证候选（全部 fRA 0 / checks.fail 为空）

| alpha | 表达式 | 设置 | S | F | 2Y | SUB | TO | margin | prod | self |
|---|---|---|---|---|---|---|---|---|---|---|
| **vROPEJ8w** | `ts_zscore(ts_sum(mean_buy_transaction_count, 63), 252)` | TOP2000 / decay5 / SUBINDUSTRY | **2.08** | **1.74** | **3.49** | 1.31 | 10.52% | 16.65bp | **0.5517 ✅** | **−0.073** |
| **O0Jgd7Y7** | `ts_zscore(ts_sum(total_buy_transaction_count, 42), 252)` | — | **2.27** | **2.03** | **3.09** | 1.22 | 13.0% | — | **0.5655 ✅** | 0.0 |
| **vROPEJ8w** 同族 | `ts_zscore(ts_sum(mean_top_buy_transaction_count, 63), 252)` | — | 1.61 | 1.39 | 2.75 | 1.00 | 11.2% | — | **0.6163 ✅** | −0.036 |
| **1Yj08nb6** | `ts_zscore(ts_sum(total_buy_transaction_count, 63), 504)` | — | 1.58 | 1.20 | 2.29 | 0.94 | 10.01% | 14.45bp | **0.5796 ✅** | — |
| **XgRM3Yra** | `ts_zscore(ts_sum(total_buy_transaction_count, 126), 252)` | — | 1.66 | 1.19 | 2.27 | 0.97 | 8.69% | 14.86bp | 0.5803 ✅ | — |
| **88vXxaqv** | `ts_zscore(ts_sum(total_buy_transaction_count, 63), 504)` | — | 1.99 | 1.66 | 2.04 | 0.89 | 9.5% | — | 0.6811 ✅ | — |

**共同骨架**：`ts_zscore(ts_sum(<内部人买入笔数字段>, <63/126/252>), <252/504>)`
⇒ **「内部人买入笔数的时序累计 + 截面标准化」是一个强机制族**。

**经济含义**：内部人买入是知情交易的经典代理（信息优势假说）。本族的三层结构：
- `ts_sum(·, 63)` —— 季度累计（覆盖财报/交易公告周期内的累计买入强度）；
- `ts_zscore(·, 252)` —— 截面标准化（消除「内部人交易活跃度」的规模偏误：大盘公司内部人交易绝对数天然更高）；
- 组合窗 `63/126/252` 与标准化窗 `252/504` 的错位制造了**时间尺度上互不相关**的多个变体 ⇒ **天然低 prod 相关的分散源**。

---

## 3. 为什么它同时过所有闸

| 闸 | 为什么天然过 |
|---|---|
| `LOW_SHARPE` | 内部人信号本身强（学术证据充分） |
| `LOW_FITNESS` | TO 8.7%–13%（不在地板区）⇒ `F = S·sqrt(R/TO)` 分子分母都健康 |
| `LOW_TURNOVER` / `HIGH_TURNOVER` | TO 10% 上下，两头都不触线 |
| `CONCENTRATED_WEIGHT` | 标准化后权重分散 |
| `LOW_SUB_UNIVERSE_SHARPE` | 内部人交易在大盘股上更密集 ⇒ **天然偏向流动性好的股票 ⇒ SUB 高**（与 risk59 联动性骨架的 SUB 硬伤正好相反） |
| `LOW_2Y_SHARPE` | 2Y 2.0–3.5，稳过 |

⇒ **这是本项目至今唯一「一个数据集就同时提供 4–6 颗全闸候选」的地方。**

---

## 4. 注意事项

1. **持仓数偏窄**：`vROPEJ8w` longCount 346 / shortCount 639（合计 985 只），虽然 TOP2000 宇宙合规，但**实际持仓只有宇宙的一半** ⇒ 内部人数据在小票上缺失 ⇒ 这正是它 SUB 高的原因。
2. **investability 偏低**：`vROPEJ8w` inv_S 0.17 / inv_ratio 0.0817；`1Yj08nb6` inv_S −0.03；`XgRM3Yra` inv_S −0.10。⚠️ 项目自设 0.70 线（非平台闸）—— 若要提交这批需先裁定是否豁免。
3. **不要与 `insiders1` / `insiders3` 混为一谈**：`insiders1`（45f）无买卖方向维度且 GBR 已实测全灭；`insiders3`（61f，aCnt 38109）极拥挤。`insider_trx_matrix` 是独立数据集。
4. **塔位纪律**：属 OTHER 塔 ⇒ 与 PV / MODEL / OTHER 的禁混规则无关（单塔），但**不能与 PV 塔的 alpha 组成同一个 alpha**（字段混用才会触发）。

---

## 5. 三波实测的完整机制地图（wave273–275，共 30 条回测）

### 5.1 窗口轴 —— 存在内点最优，**两个窗都要短**

组合窗（mean_buy_transaction_count，标准化窗 252）：

| 组合窗 | S | F | 2Y | SUB | TO | CW | 结论 |
|---|---:|---:|---:|---:|---:|---|---|
| **1** | **5.29** | 4.99 | **5.89** | 2.83 | **56.46%** | **0.1563 ❌** | 信号最强但不可交易 |
| 5 | 2.91 | 2.40 | 3.87 | 1.36 | 34.25% | **0.1523 ❌** | CW FAIL + SUB 闸 |
| 11 | 2.57 | 2.19 | 4.00 | 1.22 | 23.78% | — | SUB 差 10% |
| **22** | 2.47 | 2.18 | 3.49 | **1.33** | 17.51% | ✅ | **全闸通过（kqNb7XY6）** |
| 63 | 2.08 | 1.74 | 3.49 | 1.31 | 10.52% | ✅ | 全闸通过（vROPEJ8w） |
| 126 | 1.57 | 1.09 | 2.08 | 0.95 | 8.65% | ✅ | fRA 1（QPY8rqRg） |
| 252 | 1.49 | 1.01 | 0.99 | 1.12 | 7.25% | ✅ | 2Y 不足 |

标准化窗（组合窗 22）：z126（S2.95/F2.71/SUB1.47）> z252（2.47/2.18/1.33）> z504（1.84/1.51/0.99）。

⇒ **组合窗与标准化窗都该短**：要的是「相对近期的异常买入强度」，不是「相对一年的位置」。
⇒ **与 risk59 的「长窗更优」完全相反** —— 窗口方向由机制的时间衰减速度决定，不是通用偏好。

### 5.2 有效机制（4 条）

| 机制 | 最优表达式 | S | F | 2Y | SUB | fRA |
|---|---|---:|---:|---:|---:|---:|
| ① 纯买入（mean 口径） | `ts_zscore(ts_sum(mean_buy_transaction_count, 22), 252)` | 2.47 | 2.18 | 3.49 | 1.33 | **0** |
| ② 纯买入（total 口径） | `ts_zscore(ts_sum(total_buy_transaction_count, 22), 252)` | 2.35 | 2.03 | 3.30 | 1.32 | **0** |
| ③ 强度 × 纯净度相乘 | `multiply(zscore(mean_buy_22), zscore(buy22/(sell22+1)))` | **3.28** | **3.15** | **4.46** | 1.66 | 2（差 CW 3% + SUB 5%） |
| ④ 买卖比 | `ts_zscore(divide(ts_sum(total_buy_transaction_count, 63), add(ts_sum(total_sell_transaction_count, 63), 1)), 252)` | 1.44 | 1.02 | 2.42 | 0.71 | 2 |

**★ 乘性破例**：同族信号相乘在本项目此前（risk59 / option3）全部是坏形式；此处**首次有效** ——
前提是两个信号**不同族**（强度 vs 纯净度），而非同一骨架换参数。

### 5.3 判死机制（勿重派）

| 机制 | 实测 | 结论 |
|---|---|---|
| 卖出侧单独 | j2YWvnmE S −0.13 / vR1x85gz S −0.24 | 无正向信号（但作分母强） |
| 净差（买 − 卖） | QPvqMnXG S 0.50 / rKREYbX8 S 0.33 | 弱于买卖比与纯买入 |
| 平台方向分 `directional_indicator_score` | 58E3xLVn S −0.18 | 官方聚合版无信息量 |
| **全部 16 个 `usd_*` 美元金额字段** | \|S\| ≤ 0.50；`usd_top_direct_signal_value_2` CW 0.1064 ❌ | **笔数 > 金额**（金额受单笔大额噪声支配） |
| top（高置信度）口径 × 22 窗 | j2YWbPXW S1.60 + CW 0.1042 ❌ / LLMqAm69 S1.45 | **top 口径整体无效** |
| top 口径买卖比 | vR1xq9bv S1.06 | 同上 |
| `vector_neut` 残差化 | Xg9PrLA5 S0.20（归零）/ 2rAQ0RoZ S1.21 | 稀释主腿，只适合做低相关变体 |
| 一阶差（增量变化） | ZYQqedlY S2.21 / SUB1.02 | 存量强度优于增量变化 |

### 5.4 当前全闸候选（OTHER 塔，checks.fail 完全为空）

| alpha | 表达式 | S | F | 2Y | SUB | prod | self |
|---|---|---:|---:|---:|---:|---|---|
| **kqNb7XY6** | `ts_zscore(ts_sum(mean_buy_transaction_count, 22), 252)` | 2.47 | 2.18 | 3.49 | 1.33 | **0.6569 ✅** | **0.018 ✅** |
| **58E3oA3X** | `ts_zscore(ts_sum(total_buy_transaction_count, 22), 252)` | 2.35 | 2.03 | 3.30 | 1.32 | 未测 | — |
| **bl6V5rVM** | `ts_zscore(ts_sum(mean_buy_transaction_count, 22), 504)` | 1.84 | 1.51 | 2.73 | 0.99 | 未测 | — |
| vROPEJ8w | `ts_zscore(ts_sum(mean_buy_transaction_count, 63), 252)` | 2.08 | 1.74 | 3.49 | 1.31 | 0.5517 ✅ | −0.073 ✅ |
| O0Jgd7Y7 | `ts_zscore(ts_sum(total_buy_transaction_count, 42), 252)` | 2.27 | 2.03 | 3.09 | 1.22 | 0.5655 ✅ | 0.0 |
| LL53QVvn | `ts_zscore(ts_sum(mean_top_buy_transaction_count, 63), 252)` | 1.61 | 1.39 | 2.75 | 1.00 | 0.6163 ✅ | −0.036 |
| 1Yj08nb6 | `ts_zscore(ts_sum(total_buy_transaction_count, 63), 504)` | 1.58 | 1.20 | 2.29 | 0.94 | 0.5796 ✅ | — |
| XgRM3Yra | `ts_zscore(ts_sum(total_buy_transaction_count, 126), 252)` | 1.66 | 1.19 | 2.27 | 0.97 | 0.5803 ✅ | — |

**近全闸**：xAr9029b（S2.95/F2.71，SUB 差 6%）/ kqJAXbp8（S1.55，LOW_SHARPE 差 1.9%）/ A1VYMrbe（S3.28，CW 差 3% + SUB 差 5%）。

---

## 6. 第五波（wave277）新增：★ 「指标强度与 prod 负相关」——提交候选排序的第一原则

### 6.1 实测对照（全部 USA/TOP3000 或 TOP2000 / D1）

| alpha | 表达式要点 | S | F | TO | SUB | 2Y | prod | 结论 |
|---|---|---:|---:|---:|---:|---:|---|---|
| **vROPEJ8w** | mean_buy 63 窗 z252（裸） | 2.08 | 1.74 | 10.52% | 1.31 | 3.49 | **0.5517 ✅** | prod 最优 |
| O0Jgd7Y7 | total_buy 42 窗 z252（裸） | 2.27 | 2.03 | 13.0% | 1.22 | 3.09 | **0.5655 ✅** | |
| LL53QVvn | mean_top_buy 63 窗 z252（裸） | 1.61 | 1.39 | 11.2% | 1.00 | 2.75 | **0.6163 ✅** | |
| kqNb7XY6 | mean_buy 22 窗 z252（裸） | 2.47 | 2.18 | 17.51% | 1.33 | 3.49 | **0.6569 ✅** | 指标强、prod 贴线 |
| 58E3oA3X | total_buy 22 窗 z252（裸） | 2.35 | 2.03 | 17.69% | 1.32 | 3.30 | **0.6715 ✅** | |
| **3qo3Wv5O** | base 22 窗 **+ group_neutralize** | **3.42** | **3.06** | 20.26% | 1.59 | 3.96 | **0.8958 ❌** | **指标最强但 prod 撞墙** |
| **E56YodoJ** | **买入 − secondary 卖出（差值）126 窗** | 1.63 | 1.06 | **7.47%** | 0.81 | 2.20 | **0.6435 ✅** | **inv_S 0.80（四绿）** |

### 6.2 三条硬结论

1. **「指标最强」与「prod 最优」反向**。prod 池里已有「教科书化的内部人买入因子」（SUE / 内部人交易强度），它天然就在 TO 10–20% / S 2 上下。越往指标极致走（短窗 + group_neutralize + 精细几何）越贴近它 ⇒ prod 越高。
   ⇒ **提交候选排序以 prod 升序为第一原则，S/F 只在 prod 都达标后用于挑最优。**
2. **压 prod 的五条偏离轴**（wave277 全部验证）：
   - 更长的组合窗（63 → 126 → 252 → 504）
   - 更粗的口径（total / mean / top，而非细分 secondary）
   - 更少的几何加工（裸 `ts_zscore` 而非 `group_neutralize`）
   - 换宇宙 / 换中性化（设置层也是偏离轴）
   - 用**差值**（买 − 卖）而非**比值**（买 / 卖）—— 差值避免分母趋零的爆炸，指标更稳且 investability 更高（E56YodoJ inv_S 0.80 vs 买卖比 −0.10）
3. **乘性两族组合只在两信号同号且都有正信息时有效**：买入 × 买卖比 ⇒ S3.28（wave273）；买入强度 × **卖出**（反向信号）⇒ S −0.33（wave277）符号翻转。**乘进一个反向信号会翻转整个 alpha。**

### 6.3 ★ 本会话唯一「四绿」候选

**E56YodoJ** = `ts_zscore(subtract(ts_sum(total_buy_transaction_count, 126), ts_sum(total_secondary_sell_transaction_count, 126)), 252)`
（USA/TOP3000/decay 5/REVERSION_AND_MOMENTUM/trunc 0.08）

| 项 | 值 |
|---|---|
| S / F | 1.63 / 1.06 |
| 2Y / SUB | **2.20** / 0.81 |
| TO / R / DD | **7.47%**（全族最低）/ 5.24% / 7.09%（全族最低） |
| margin | 14.03bp |
| investability_sharpe / fitness | **0.80** / 0.36 ← **唯一过项目自设 0.70 线** |
| risk_neutralized_sharpe | 1.42 |
| failed_ra_count / failed_ppa_count | **0 / 0**（checks.fail 完全为空） |
| prod / self | **0.6435 ✅** / **0.305 ✅** |

---

## 7. 待办

- [ ] 补齐 `58E3oA3X` / `bl6V5rVM` / `xAr9029b` / `A1VYMrbe` 的 prod 与 self-corr
- [ ] 裁定 investability 自设 0.70 线是否豁免（本数据集 30 条实测 inv_S 全在 −0.51 ~ +0.16）
- [x] 挖本数据集未测字段：卖出笔数（SELL 侧）、买卖比、交易金额（而非笔数）—— wave273–275 已全部完成
- [ ] 该数据集 alphaCount=1 ⇒ **低相关红利尚未折旧，应优先用掉**
- [ ] 剩余未测：`mean_secondary_buy_transaction_count`（uCnt 39）、`total_secondary_sell_transaction_count`（uCnt 7）、`mean_top_secondary_sell_transaction_count`（uCnt 10）

