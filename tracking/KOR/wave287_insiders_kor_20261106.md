# KOR × insiders 波次记录（wave287 · 2026-11-06）

> 目标：KOR / TOP600 / D1，ATOM（单数据集）REGULAR alpha。本波按用户目标切换至 **Insiders** 类别。
> 类别参考页：`Claude/skills/wq-brain-ra-kor/references/insiders.md`

## 1. 数据集全集（`get_datasets`，category=insiders）

| 数据集 | aC | uC | cov | 字段数 | 判死记录 |
|---|---:|---:|---:|---:|---|
| `insiders1` | 549 | 202 | 0.3526 | 9 | 无（**几乎未被挖掘**） |
| `insiders5` | 5027 | 820 | 0.8918 | 53 | `KOR-INSIDERS5-CEILING-20260909`（族 insider_x_pv_x_analyst，S 天花板 1.05） |

⚠ 类别只有 **2 个**数据集（不同于 analyst 的 17 个）。

## 2. 字段画像（全部 VECTOR 类型 ⇒ 必须先 `vec_*` 降维再进任何标量算子）

### insiders1（9 字段 / cov 0.353）
| 字段 | aC | 说明 |
|---|---:|---|
| `insd1_gvkey` | 178 | 公司标识 |
| `insd1_shares` | 112 | 交易股数 |
| `insd1_value` | 107 | 交易金额（原币） |
| `insd1_holdings` | 57 | 交易后持股 |
| `insd1_price` / `insd1_valueeur` | 45 / 45 | 交易价 / 欧元金额 |
| `insd1_tradesignificance` | 40 | 交易重要性评分 1–3 |
| `transaction_currency_code` | 15 | 币种 |
| `max_trade_price` | 5 | 价格区间上限 |

**结构性缺陷**：无「买卖方向」字段、无「变动量」字段 ⇒ 只能表达金额/股数的**规模与离散度**，方向只能靠取负反推。

### insiders5（53 字段 / cov 0.732–1.000）
核心可用（含符号方向）：
| 字段 | aC | 说明 |
|---|---:|---|
| `insd5_ghc_tr` | 220 | **持股比例变动（有符号）** ← 核心 |
| `insd5_fa_tr` / `insd5_fb_tr` | 132 / 76 | 交易后 / 前持股比例 |
| `insd5_vol_chg` | 126 | 股数变动（有符号） |
| `insd5_vol_af` / `insd5_vol_bf` | 75 / 95 | 交易后 / 前持股数 |
| `insd5_trd_amt` | 85 | 交易金额（KRW） |
| `insd5_ratio` / `real_ratio` / `source_ratio` | 122 / 205 / 413 | 去重持股比例族 |
| `insd5_officer` | 49 | 是否高管 |

高占用（拥挤，慎用）：`insd5_source_data`(744)、`insd5_source_real_data`(625)、`insd5_rpst_grp_typ`(590)、`insd5_tnc`(478)。

## 3. 回测设置（按类别卡）
`STATISTICAL`（卡片值）→ 实测改为 `REVERSION_AND_MOMENTUM` 更优；decay **4** / trunc **0.08** / **nanHandling OFF** / maxTrade OFF。

## 4. 第一轮：10 个结构互异模板 × STATISTICAL（`QVcai8c44IDa0Djwc14ihM` / `1VhA3g1bh4KobwKb4YbOQ8v`）

模板维度 = 字段 × 降维算子 × 时序算子 × 分组轴：

| # | 结构 | alpha | S | 2Y |
|---|---|---|---:|---:|
| T1 | `ts_sum(vec_sum(ghc_tr),66)` sector | qMLOdZL1 | **-0.41** | -0.68 |
| T2 | `ts_mean(vec_avg(ghc_tr),66)` sector | O0ARkvAb | -0.41 | -0.94 |
| T3 | `ts_rank(ts_sum(vec_sum(ghc_tr),22),250)` sector | E56NbA6G | -0.67 | -0.09 |
| T4 | `ts_sum(vec_count(ghc_tr),66)` sector | 3qo1xWoP | -0.70 | -1.19 |
| T5 | `ts_mean(vec_sum(vol_af),66)` industry | gJeXKze0 | **-1.07** | -2.35 |
| T6 | `vol_af/vol_bf` 比率 | WjO3dmOZ | -0.30 | -0.94 |
| T7 | `ts_sum(vec_max(ghc_tr),66)` sector | YP18mda6 | -0.70 | -1.28 |
| T8 | `ts_mean(vec_stddev(ghc_tr),66)` sector | kqNvX5al | **-1.16** | -1.49 |
| T9 | `ts_sum(vec_sum(trd_amt),66)` sector | JjeoYJl2 | -0.81 | -0.82 |
| T10 | 金额集中度 max/sum | qMLOvJeZ | -0.46 | -0.19 |
| T11 | 分组轴 market | xArV9pXn | -0.50 | -0.87 |
| T12 | 外包裹 group_neutralize(industry) | vR1ZxXar | -0.19 | -0.55 |
| T13 | `ts_av_diff(ghc_tr,250)` | 9qx8bOgd | -0.20 | -0.90（**TO 1.43**） |
| T14 | `ts_zscore(ghc_tr,250)` | gJeXwV7l | -0.13 | -1.14（**TO 1.44**） |
| T15 | `insd1_value` 66 sector | MPYdqNlo | **-1.08** | -0.79 |
| T16 | `insd1_tradesignificance` | pwdxoeJo | 0.01 | -0.02（无信息） |

### ★ 归因（关键）
1. **16 条里 15 条为负** ⇒ 不是某条骨架写错，是**方向系统性相反**：KOR 内部人净增持（持股比例上升）反向预示跑输，净减持反而已被定价。
2. 全部 16 条同时 fail `LOW_INVESTABILITY_CONSTRAINED_SHARPE` ⇒ 在 STATISTICAL 档下该族不可投资。
3. `ts_av_diff`/`ts_zscore` 在 `ghc_tr` 上 **TO 爆到 1.43** ⇒ 这两个算子在本族直接判死。

## 5. 第二轮：取负 + 中性化 A/B（`2RxTqD3Yv4CwbCkJQocQcIq` / `PHtDv6Wi4P6bGvfa5oeOCG`）

按类别卡 D6 写法 `subtract(0.5, group_rank(X, g))`（取负放在 rank 之后、保持零均值），中性化改 `REVERSION_AND_MOMENTUM`。

| 结构 | alpha | S | F | TO | 2Y | R |
|---|---|---:|---:|---:|---:|---:|
| **T8' 离散度 66 sector** | **e75N2JJ6** | **1.41** | **1.21** | .0875 | **1.86** | .0915 |
| T15' `insd1_value` 66 sector | xArVzaMw | 1.39 | 1.20 | .0991 | 1.18 | .0933 |
| T6' vol_af/vol_bf 比率 | rKR9zmmJ | 0.51 | 0.23 | .0794 | 1.33 | .0244 |
| T9' 金额 66 | GrWX8vv5 | 0.52 | 0.23 | .0741 | 0.54 | .0246 |
| T1' 净变动 66 | leAEzZX5 | 0.20 | 0.06 | .0798 | 0.96 | .0102 |
| T8'' 离散度 **250** | KPJv86Az | 0.85 | 0.55 | .0613 | 0.83 | .0517 |
| T15'' insd1_value **250** | A1VeabpQ | 1.10 | 0.76 | .0578 | 1.25 | .0592 |
| T1'' 净变动 250 | E56NabnK | 0.64 | 0.31 | .0545 | 0.98 | .0299 |

### ★ 归因
1. **取负是决定性杠杆**：同一批结构由 -1.16/-1.08 翻到 +1.41/+1.39。
2. **中性化 A/B**：同一表达式同一取负，STATISTICAL → R&M 让 T8 从 1.16 抬到 **1.41（+0.25）**，且 investability 闸从 fail 转为不报错。
3. **机制胜出的是「分歧度」不是「水平」**：`vec_stddev`（1.41）远强于 `vec_sum`（0.20）；「动了多少仓位」的内部**一致性**才是定价信息 —— 与论坛「动了多少仓位比动了多少钱重要」一致，但更进一步：**仓位的分歧度 > 仓位变化量**。
4. **66 天窗口是谷底**：250/132 天版本全部掉到 0.64–1.10。
5. T8' 只 fail `LOW_SHARPE`（1.41 < 1.58），其余闸全过 ⇒ 距提交线差 **0.17**。

## 6. 待办
- 第三轮：窗口 44/55/88/99、分组轴 industry/subindustry、`vec_range` 替 `vec_stddev`、其它字段离散度（trd_amt/vol_chg/ratio/insd1_value）。
- 目标：把 T8' 从 S1.41 推到 ≥1.58 且 2Y ≥1.58，再过 prod/self。


## 7. ★★★★ 第四轮：窗口谷命中全过候选（`MHUEXgpc4j5cJiOjuiR09c` / `4sPcnf9qK4n6bsRD980xHvl`）

### 窗口谱（ghc_tr 离散度，R&M / d4 / trunc 0.08 / nanH OFF，sector 分组）
| W | alpha | S | F | TO | 2Y | failed_ra |
|---|---|---:|---:|---:|---:|---|
| 44 | rKR9J1m8 | 1.50 | 1.37 | .1109 | 2.22 | LOW_SHARPE |
| **55** | **kqNv1xRk** | **1.62** | **1.50** | .0981 | **2.23** | **（空，全过）** |
| 66 | e75N2JJ6 | 1.41 | 1.21 | .0875 | 1.86 | LOW_SHARPE |
| 88 | A1VegR6l | 1.06 | 0.79 | .0786 | 1.15 | 3 项 |
| 99 | QPvO21mM | 1.07 | 0.80 | .0761 | 1.02 | 3 项 |
| 250 | KPJv86Az | 0.85 | 0.55 | .0613 | 0.83 | 2 项 |

### 同批其它结构
| 结构 | alpha | S | 2Y |
|---|---|---:|---:|
| `vec_stddev(vol_chg)` 66 sector | e75N2MPg | 1.47 | **2.23** |
| `vec_stddev(fa_tr)` 66 sector | qMLOz2JE | 1.37 | 1.72 |
| `ts_sum` 替 `ts_mean`（ghc 66） | xArVz7op | 1.33 | 1.88 |
| 分组轴 market（ghc 66） | P0oxlLmE | 1.28 | 1.99 |
| 分组轴 industry（ghc 66） | MPYdKj9k | 1.51 | 1.54 |
| 分组轴 subindustry（ghc 66） | mLodrPe1 | 0.95 | 0.55 |
| 外包裹 group_neutralize(industry) | 3qo1aMYZ | 1.41 | 1.45 |
| `vec_range` 替 `vec_stddev` | leAEQL6l | 1.30 | 1.59 |
| `vec_stddev(ratio)` | akKePm8x | -0.31 | -0.56 |

## 8. ★★★★★ 交付候选 #2：`kqNv1xRk`
```
subtract(0.5, group_rank(ts_mean(vec_stddev(insd5_ghc_tr), 55), sector))
```
数据集 `insiders5`（ATOM，单数据集）· KOR/TOP600/D1 · R&M · decay 4 · trunc 0.08 · nanH OFF · maxTrade OFF

| 闸 | 实测 | 线 | 判定 |
|---|---:|---:|---|
| S | **1.62** | 1.58 | ✅ |
| 2Y | **2.23** | 1.58 | ✅ |
| F | **1.50** | 1.0 | ✅ |
| self | **0.3639** | 0.70 | ✅ |
| failed_ra | **0** | 0 | ✅ |
| 逐年 | 2014–2023 全部 longCount 285–327、pnl 全非零 | 近十年 | ✅ |
| prod | submit_gate 通过、hard_gate_warns=[] | 0.70 | ✅（数值未单独取到：`check_correlation` 连续 120s 超时） |

`submit_gate`：passed=true / blocked=false / failed_ra=0 / hard_gate_warns=[]；边际贡献 **ΔSharpe +0.26**（非稀释）。**未提交，等用户授权。**

### ★ 归因（本波最重要结论）
1. **方向反转是本族的第一性事实**：KOR 内部人净增持 → 后续跑输。必须 `subtract(0.5, group_rank(...))`。
2. **「仓位变动的分歧度」> 「仓位变动量」**：`vec_stddev(ghc_tr)` 1.62 vs `vec_sum(ghc_tr)` 0.20。含义：内部人**是否一致**地增减持才是定价信息，增减持的总量早已被套利。
3. **55 天是窗口谷**（44 1.50 / **55 1.62** / 66 1.41 / 88 1.06）—— 注意 55 为非标准窗口，峰值窄，需在后续波次用 50/58/60 复核稳健性。
4. **分组轴 sector 最优**（industry 1.51 但 2Y 掉到 1.54；subindustry 0.95 崩）。
5. **2Y 普遍极高（1.9–2.23）** ⇒ 该机制近两年特别强，全样本 S 是短板，正对应窗口谷的选择性。
