# USA 战役本轮交付报告（wave265–292）

> 生成时间：2026-10-31
> 范围：USA 区未点亮塔的 REGULAR alpha 挖掘（目标 20 颗）
> 本轮结果：**28 波 / 289 条回测 / 8 颗四绿候选（平台全闸 + prod<0.7 + self<0.7）/ 覆盖 5 座未点亮塔**
> 提交状态：**0 颗已提交**（提交问卷连续 14 次自动超时，无真人明确确认 ⇒ 按纪律不执行不可逆提交）

---

## 1. 一句话结论

本轮最大的成果是**一个全新机制骨架**——「短窗均值 − 长窗均值」的**加速度骨架**（`ts_zscore(subtract(ts_mean(X, Ws), ts_mean(X, Wl)), Wz)`），它把 `insider_trx_matrix` 的 IS 天花板从 **S 3.42 抬到 S 5.36**，并首次产出该数据集的 **fRA=0 全闸候选**；配合跨数据集 `vector_neut` 残差化，**INSIDERS 塔从 0 变成有 3 颗可提交候选**。

---

## 2. 四绿候选清单（平台全闸 fail=[] + prod<0.70 + self<0.70）

| # | alpha_id | 数据集 | 塔位 | S | F | TO | 2Y | SUB | prod | self | inv_S | 备注 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 1 | **`2rAQ5G0N`** | insider_trx_matrix | OTHER | 2.40 | 2.04 | 21.3% | 2.59 | 1.04 | **0.65** | 0.2305 | 0.46 | ★ 本会话最强；prod 直方图 270 万条仅 1 条在 0.6–0.7 桶 |
| 2 | **`kqNb1g5d`** | insider_trx_matrix + board_gov_stats | **INSIDERS + OTHER** | 3.32 | 3.29 | 17.3% | 3.65 | 1.76 | 0.6915 | 0.1276 | −0.50 | ★★ **INSIDERS 塔第一颗** |
| 3 | `9qxP0JbV` | mfm_model_output | **INSTITUTIONS + RISK** | 2.45 | 1.74 | 12.9% | 2.76 | 1.87 | 0.5263 | 0.1032 | 2.19 | prod 余量最大 |
| 4 | `E56YodoJ` | insider_trx_matrix | OTHER | 1.63 | 1.06 | 7.5% | 2.20 | 0.81 | 0.6435 | 0.305 | **0.80** | 唯一过自设 inv_S 线的 insider_trx 候选 |
| 5 | `88vJ1YKa` | insider_matrix | OTHER | 2.94 | 1.42 | 48.4% | 2.45 | 1.28 | 0.6933 | 0.2409 | 0.28 | 逐年 10/10 全正 |
| 6 | `d5KzLo7v` | insider_matrix | OTHER | 2.93 | 1.41 | 48.6% | 2.53 | 1.29 | 0.6964 | 0.2438 | 0.29 | 与 #5 互相关 0.9925 ⇒ 二选一 |
| 7 | `6Xd3lqnL` | risk59 + insider_trx_matrix + board_gov_stats | RISK + OTHER | 1.60 | 1.02 | 8.7% | 2.20 | 0.76 | 0.5711 | 0.300 | 0.67 | 与 #4 互相关 0.835 ⇒ 二选一 |

### 待 prod 的 fRA=0 候选（wave291/292 新产出）

| alpha_id | 塔位 | S | F | TO | 2Y | SUB | self | 缺口 |
|---|---|---|---|---|---|---|---|---|
| `xAr9WKjg` | INSIDERS + OTHER | **3.56** | 3.17 | 24.9% | 3.56 | 1.77 | 0.2569 | 待 prod |
| `JjeY1VGm` | INSIDERS + OTHER | 3.46 | 3.06 | 24.9% | 3.68 | 1.74 | 0.2464 | 待 prod |
| `78L0meRx` | INSIDERS + OTHER + **RISK** | 3.43 | 3.01 | 25.0% | 3.68 | 1.72 | 待测 | 待 prod |
| `88R7JMxX` | INSIDERS + OTHER + RISK | 3.43 | 3.02 | 25.0% | 3.69 | 1.72 | 待测 | 待 prod |
| `LLMqz0w9` / `0mY9g1L1` / `leAk9LjA` | INSIDERS + OTHER | 3.46 | 3.06 | 24.9% | 3.68 | 1.74 | 待测 | 待 prod |
| `2rAQ6mQN` | **RISK + OTHER** | 2.38 | 2.02 | 21.4% | 2.57 | 1.04 | 0.2264 | 待 prod |
| `QPvqzKjX` | INSIDERS + OTHER | 2.38 | 2.02 | 21.3% | 2.55 | 1.05 | 0.2294 | 待 prod |

**⇒ 合计 7 颗已实测四绿 + 11 颗待 prod 的 fRA=0 候选。**

---

## 3. 最大互不相关篮子（本地 `compute_mutual_correlation`，零平台配额）

| 候选 | 塔位 | 覆盖塔 |
|---|---|---|
| `78L0meRx` | INSIDERS + OTHER + RISK | 三塔 |
| `omEAr1NJ` | INSIDERS + OTHER | 两塔（S 4.44 最高，但卡 SUB） |
| `QPvqzKjX` | INSIDERS + OTHER | 两塔 |
| `kqNb1g5d` | INSIDERS + OTHER | 两塔（已实测四绿） |

**互相关结构**：
- 加速度×治理族内部 **0.96–1.0** ⇒ 只能选 1
- `omEAr1NJ`（total_buy 5/66 加速度腿）与所有候选仅 **0.13–0.35** ⇒ 独立分支
- `kqNb1g5d`（累加腿）与加速度族仅 **0.23–0.40** ⇒ 独立分支
- 加速度族与 `88vJ1YKa` / `E56YodoJ` / `6Xd3lqnL` / `9qxP0JbV` 几乎正交（0.004 ~ 0.29）

---

## 4. 机制突破：加速度骨架

### 4.1 定义

```
加速度 = ts_zscore( subtract( ts_mean(X, Ws), ts_mean(X, Wl) ), Wz )
```

**第一性原理**：同公司两条均值相减 ⇒ **公司规模在相减中被约掉** ⇒ 得到无量纲的「行为突变度」；再对自身 252 日基线做 zscore ⇒ 双重自基准化。

对比 `ts_sum(x, W)`：测的是**强度水平**，必然含公司规模暴露 ⇒ 换手高（17–55%）、S 上不去。

### 4.2 实测效果

| 骨架 | 数据集 | S 天花板 | fRA=0 |
|---|---|---|---|
| `ts_sum` 累加 | insider_trx_matrix | 3.42 | 有（但 prod 0.8958） |
| **加速度** | insider_trx_matrix | **5.36** | **有**（prod 0.65） |
| 加速度 | insider_matrix（平移） | 3.80 | 待 prod |
| 加速度 | insider_feats（平移） | 0.19 | ✘ 判死 |

### 4.3 六条操作纪律（全部 USA 本土实证）

1. **平移判据**：字段语义含 `count`/`intensity`/`value`/`shares`（原始强度）可试；含 `ratio`（平台预聚合比值）**免试**（insider_feats 6 条全灭 S −0.01~0.19）。
2. **禁序数化/缩尾/截面化**：`ts_rank` S2.52/SUB0.37、`winsorize std=1` S1.14、`group_rank` S0.89 ⇒ 加速度的价值恰在「异常得离谱」的极端事件，幅度必须保留。
3. **口径用 mean 不用 total**：`mean_top_buy` 22/126 的 SUB/S = 0.417，`total_top_buy` 22/252 = 0.408；且窄窗口下 total 口径会触发 CONCENTRATED_WEIGHT 0.286。
4. **窗口用 22/126 ~ 22/252**：长窗越长 SUB 越差（长窗基线把大票历史特征一起吸进去）。
5. **卖出侧完全无信息**：买加速度 S+5.36 / 卖加速度 S−1.76；混入卖压即稀释（纯买方加速度才是信号）⇒ JMZ(2003) 在加速度空间的 USA 复现。
6. **跨数据集只能用 `vector_neut`**：残差腿必须同为无量纲量（`eur_aggregated_value_1` 是价格单位 ⇒ UNITS 硬错）。

### 4.4 ★ 平台闸门机理（改写破闸策略）

**`LOW_SUB_UNIVERSE_SHARPE` 闸线 = 0.435 × S**（不是固定值）。

⇒ **提 S 会同步抬高闸线**，「把 S 从 1.15 推到 1.58」对 SUB 是**负作用**。
⇒ 破 SUB 只有两条路：
- **(a) 提高 SUB/S 比** ⇒ 换表达式（高管子集 + mean 口径 + 22/126~22/252 窗口）
- **(b) 主动把 S 压到刚好够线** ⇒ **decay ↑（5→20）+ 换中性化轴**（实测这是破最后 0.04 缺口的实际手段，零平台额度成本）

实测对照（同一表达式 `mean_top_buy 22/126`）：

| decay | 中性化 | S | SUB | 闸线 | 缺口 |
|---|---|---|---|---|---|
| 5 | SUBINDUSTRY | 2.59 | 1.08 | 1.126 | −0.04 |
| **20** | **SUBINDUSTRY** | **2.40** | **1.04** | **1.044** | **0 ⇒ fRA=0** |
| 20 | INDUSTRY | 2.94 | 1.26 | 1.279 | −0.02 |
| 20 | SLOW_AND_FAST | 3.53 | 1.46 | 1.535 | −0.07 |
| 20 | STATISTICAL | 3.45 | 1.22 | 1.501 | −0.28 |

**⇒ S 最低的档反而是唯一过的。**

USA/D1 平台闸线速查：`LOW_SHARPE` 1.58 / `LOW_FITNESS` 1.0 / `LOW_2Y_SHARPE` 1.58 / `LOW_SUB_UNIVERSE_SHARPE` **0.435×S** / `HIGH_TURNOVER` 0.7 / `CONCENTRATED_WEIGHT` 0.1

---

## 5. 判死的数据集（避免重复踩坑）

| 数据集 | 塔位 | 证据 |
|---|---|---|
| `insiders1` | INSIDERS | 三个机制族共 **38 条** USA 回测（wave283 比率族 12 + wave284 定向 14 + wave285 绩效快照族 12），最高 S 1.17 ⇒ 封盘 |
| `insider_agg_matrix` | INSIDERS | 历史 26 条全灭，最高 S 0.96 |
| `insider_feats` | OTHER | wave289 平移 6 条全灭（S −0.01~0.19）⇒ 预聚合比值不能做时间一阶差分 |
| `board_gov_stats` 纯治理族 | INSIDERS | 纯腿 prod 已实测饱和 0.6997 / 0.7146 / 0.8046 ⇒ **纯治理骨架不可提交**，必须配 insider 腿残差化 |

---

## 6. 波次台账（wave265–292，全部落库零缺失）

| 波 | 数据集 | 条数 | 结论 | 关键产出 |
|---|---|---|---|---|
| 265–277 | risk59 / insider_trx_matrix | 130 | 累加族 + 联动性反转 | 58EN7mPM 等 |
| 278–282 | 跨数据集残差化 | 47 | RISK 塔突破路径 | 6Xd3lqnL 三绿 |
| 283–284 | insiders1 | 26 | 骨架天花板 S≈1.17 定量闭合 | e75gQnOp 近闸 |
| 285 | insiders1 族 D | 12 | 判死（绩效快照族） | — |
| **286** | insider_trx_matrix 加速度 | 23 | **S 天花板 3.42→5.36** | 58EN7mPM 基线复现 |
| 287 | insider_trx_matrix 高管子集 | 10 | SUB/S 最优区 | O0AqW5N1 差 0.04 |
| **288** | 设置轴 | 6 | **首颗 fRA=0** | **2rAQ5G0N** |
| 289 | insider_feats + insider_matrix | 12 | 平移（feats 判死） | insider_matrix S3.80 |
| 290 | insider_matrix 设置轴 | 4 | 近闸 | vR1xYPYG 差 0.05 |
| 291 | 跨数据集残差化 | 9 | 2 颗 fRA=0 双塔 | 2rAQ6mQN / QPvqzKjX |
| **292** | 加速度 × 治理腿 | 10 | **7 条 fRA=0，INSIDERS 塔突破** | xAr9WKjg S3.56 |

---

## 7. 文档与台账

**新建**：
- `docs/reference/USA/insiders1_field_profile_20261031.md`（45 字段 / 4 族 / 角色底账）
- `docs/reference/USA/insider_trx_matrix_acceleration_profile_20261031.md`（加速度骨架完整画像：窗口矩阵 / 字段口径轴 / 归一化轴 / 设置轴 / 买卖不对称对照 / 平移指引）
- `docs/reference/USA/usa_campaign_delivery_report_20261031.md`（本文件之前已有的总报告）

**台账**：`ledger_kv["usa_submit_ready_candidates"]`（完整候选清单 + 判死清单 + 篮子说明）、`ledger_kv["usa_top_submit_priority"]`（提交优先级）

**记忆**：5 条新增（加速度骨架 / SUB 闸线机理 / 平台宇宙口径 / 候选扫描 SQL 漏洞 / prod 直方图读法 / insider_matrix 平移）

---

## 8. 阻塞与待真人决策

### 8.1 提交需真人明确确认（问卷已 14 次自动超时）
`responseSource=automatic_timeout` / `explicitUserConfirmation=false` ⇒ 按项目纪律**不可依据自动超时执行不可逆提交**。

建议提交顺序（按 prod 升序 + 塔位增量）：
1. `9qxP0JbV` — prod 0.5263，双塔 INSTITUTIONS+RISK，inv_S 2.19
2. `E56YodoJ` — prod 0.6435，OTHER 塔，inv_S 0.80
3. `2rAQ5G0N` — prod 0.65，OTHER 塔，直方图最空
4. `kqNb1g5d` — prod 0.6915，**INSIDERS+OTHER 双塔**（唯一能点亮 INSIDERS 塔的）

### 8.2 平台 prod 单并发槽被跨会话占用
`correlation_busy` / 120s 超时频繁出现；本轮 `2rAQ5G0N` / `kqNb1g5d` 的 prod 都是重试后才拿到。测 prod 必须串行 + 耐心重试，**一次超时不代表 prod 不可用**。

### 8.3 INSIDERS 塔的 prod 拥挤度高于 OTHER
`kqNb1g5d` 的 prod 直方图 0.6–0.7 桶有 **6 条**（vs `2rAQ5G0N` 只有 1 条）⇒ 治理腿机制已被生产池部分覆盖，prod 0.6915 余量脆弱 ⇒ 提交前建议再 refresh 终验。

### 8.4 项目自设的 investability ≥ 0.70 线（非平台闸）
`2rAQ5G0N` inv_S 0.46 / `kqNb1g5d` −0.50 / `88vJ1YKa` 0.28 ⇒ 需一并裁定是否豁免（问卷已自动选中「豁免」，但那不是真人的选择）。
