# USA 未点亮塔挖掘 · 实证配方与判死清单（campaign_20261014）

> 证据日期 **2026-10-14**。回测 **16 波 / 64 条**，全部 USA/TOP3000/D1。
> 原始台账 `tracking/USA/campaign_20261014/02_wave_ledger.md`；字段画像 `01_S0_S1_dataset_field_profile.md`；逐波结论 `03_skill_findings.md`。
> 纪律：本轮**零自动提交**；所有结论以平台回测读数为准，元数据仅作先验。

## 0. 适用范围

本篇只记 **USA × 未点亮塔（shortinterest / insiders / option / macro / socialmedia）** 的实证，
供后续 USA 战役直接取用。通用九步走 `wq-brain-ra-pipeline`。

---

## 1. ★★★ 入场：白名单不能用 signal-score 排序

`get_pyramid_alphas`（本季度）USA/D1 只有 **model=4 / analyst=1 / earnings=1** 亮着，其余 13 塔全 0。

`score_datasets.py` 的 signal-score top20 **全部是 model 族**（`model264` / `model10` / `model354` /
`multifactor_return_pred` / `predictive_starmine` / `techindi_model` / `chart_cnn_alpha` …）。

⇒ **按 score 排序取白名单 = 往已点亮塔堆料。**
⇒ 正确筛法 = **未点亮塔 × 低 `alphaCount`**，本轮据此选出 4 个数据集（见 `01_S0_S1_*.md`）。

---

## 2. ★★★★ 纪律一：`reverse` 必须与原方向成对发批

**实测**：`short_interest_pred.predicted_change` 原方向 **S = −1.48 / 2Y = −3.16**（|S| 已近闸线）。

| 阶段 | S | 2Y | TO |
|---|---:|---:|---:|
| 原方向（decay 5） | **−1.48** | −3.16 | 0.677 |
| `+reverse`（decay 20） | +1.11 | 3.13 | 0.346 |
| `+reverse`（decay 5） | **+1.78** | 4.23 | 0.677 |
| `+reverse` + `ts_av_diff`（decay 5） | **+2.13** | 4.20 | 0.662 |

**判据**：`|S| ≥ 1.0` 且 S 为负 ⇒ **先 `reverse` 再判死**。
**为什么**：高 `alphaCount` 字段往往意味着别人已发现**正向**口径；反向才是白空间。
**成本**：一条腿一次回测；漏掉可能整族误判死。

---

## 3. ★★★★ 纪律二：`ts_av_diff` 优于 `ts_zscore(ts_backfill(...))`

同一字段 / 同设置 / 同轴，只换时序算子：

| 结构 | decay 5 | decay 10 | decay 20 |
|---|---:|---:|---:|
| `ts_zscore(ts_backfill(reverse(F),252),252)` | 1.78 | 1.52 | 1.11 |
| **`ts_av_diff(reverse(F),252)`** | **2.07** | **1.64** | **1.26** |

⇒ 全 decay 档稳定 **+16~20%**。
**机制**：`ts_zscore` 除以 `ts_std_dev`，把「低波动股的微小偏离」与「高波动股的同幅偏离」压成同值；
`ts_av_diff` 只减均值、**不除波动** ⇒ 保留幅度信息。

⚠ **前提：字段须是慢变量**（本族 cov 0.9987 满覆盖、日更预测变动）。
**事件型字段禁试**（同 `ts_mean` 抹掉频率信息的道理）。

---

## 4. ★★★★ 纪律三：decay 是 S↔F 权衡旋钮（USA 方向 = 越小 S 越高）

| decay | 63 | 20 | 10 | **5** | 3 |
|---|---:|---:|---:|---:|---:|
| b3 S | 0.70 | 1.11 | 1.52 | **1.78** | — |
| av_diff S | — | 1.26 | 1.88 | **2.13** | 2.15 |
| av_diff TO | — | 0.334 | 0.473 | 0.662 | **0.823 ❌** |
| av_diff F | — | 0.39 | 0.55 | 0.54 | 0.49 ❌ |

- **decay↓ ⇒ S↑**（单调），与 USA SUPER 实证「decay↓压 prod」（d100→d50：prod 0.8495→0.6881）**同向**。
- ★ **decay 3 撞 `HIGH_TURNOVER`（0.823 > 0.70）⇒ decay 5 是本族甜点**。
- ★ **decay 不改善 fitness**（F 恒 0.39–0.55）⇒ **decay 是纯 S 杠杆，不是 F 杠杆**
  （与 USA `analyst_consensus` TP 族「decay 六指标同向改善」相反 ⇒ **逐族实测**）。

---

## 5. ★★★ 纪律四：`2Y ≥ 2.0` 且 `TO > 0.5` 的「强 2Y」是假强

`short_interest_surprise_ratio` 原方向 **2Y = 4.03**（全批最高），但 **TO = 0.761 > 0.70 闸**。
加 `reverse` 后 **S ≈ 0.07** ⇒ 信号不存在，2Y 是高换手噪声。

**判据**：任何 `2Y ≥ 2.0` 的候选**先看 TO**；`TO > 0.5` ⇒ 不算突破。

---

## 6. ★★★ 纪律五：判毒字段看 `longCount`，不看 `coverage`

`insider_agg_matrix.directional_indicator_2` 元数据 **coverage 0.7716**，
实测 **longCount=0 / shortCount=0 / TO=0.0 / S=0.00** ⇒ **USA 无有效截面值**。

⇒ **唯一可靠判据 = 回测 `longCount`/`shortCount` 为 0**。
⇒ `insider_agg_matrix.directional_*` 全族（5 字段）按高风险处理。

---

## 7. 胜出配方（当前唯一，`failed_ra_count=1`）

```
group_rank(ts_av_diff(reverse(short_interest_predicted_change), 504), industry)
USA / TOP3000 / D1 / STATISTICAL / decay 5 / truncation 0.04 / nanHandling ON / maxTrade OFF
```

| alpha | S | F | 2Y | SUB | TO | returns | inv_S | 剩余闸 |
|---|---:|---:|---:|---:|---:|---:|---:|---|
| **`N1ewm5Jw`** | **2.13** | 0.54 | 4.20 | **1.52** | 0.662 | 0.0424 | 1.85 | `LOW_FITNESS` |
| `A1QWZ6AX`（decay3） | 2.15 | 0.49 | 4.33 | 1.55 | **0.823 ❌** | 0.0419 | 1.88 | `LOW_FITNESS`+`HIGH_TURNOVER` |
| `akVYYbQ6`（轴 market） | 2.04 | 0.52 | **4.39** | **1.54** | 0.664 | 0.0424 | 1.74 | `LOW_FITNESS` |
| `XgRrrVXz`（decay10） | 1.88 | **0.55** | 3.92 | 1.26 | 0.473 | 0.0405 | 1.52 | `LOW_FITNESS` |
| `9qEvvj81`（b3） | 1.78 | 0.41 | 4.23 | 1.28 | 0.677 | 0.0363 | 1.43 | `LOW_FITNESS` |

全部 **`ppa_failed=false`**、`MATCHES_PYRAMID` **PASS**（`pyramids.list = [USA/D1/SHORTINTEREST, mult 1.1]`）
⇒ 一旦过 `LOW_FITNESS` 即可点亮 **shortinterest 塔**（本季 0 颗）。

**经济含义**：做空意愿（模型预测的空头仓位变动）**上升 → 未来收益上升**（挤空 / 空头回补）。
`ts_av_diff` 取「当前值 − 自身均值」⇒ 捕捉**空头预期的异常偏离**，而非空头水平。

---

## 8. `LOW_FITNESS` 破闸：先算公式，再谈修法

### ★★★★★ 精确公式（12 点回归，最大误差 1.8%）

```
fitness = S × √( returns / max(TO, 0.125) )
```

**存在硬下限 `max(TO, 0.125)`** —— 这是本轮最有价值的发现。
⚠ 旧记忆里的 `F ≈ 2.813 × S × √returns`（「不吃 turnover」）**是错的**，必须废弃。

| alpha | S | returns | TO | F_pred | F_act | 误差 |
|---|---:|---:|---:|---:|---:|---:|
| `N1ewm5Jw` | 2.13 | 0.0424 | 0.662 | 0.539 | 0.54 | 0.2% |
| `XgRrrVXz` | 1.88 | 0.0405 | 0.473 | 0.550 | 0.55 | 0.0% |
| `N1ew9nqL` | 1.59 | 0.0789 | 0.670 | 0.546 | 0.55 | 0.8% |
| `e76pkZ9M` | 1.11 | 0.0283 | 0.346 | 0.317 | 0.32 | 0.8% |
| `Vkd91baM` | 0.47 | 0.0132 | **0.067** | 0.153 | 0.15 | 1.8% |
| `78oAW7E5` | 0.82 | 0.0162 | **0.066** | 0.295 | 0.30 | 1.6% |

⚠ 最后两行 **TO < 0.125**：若不设下限，公式会**高估 23–39%**（Vkd91baM 预测 0.209 vs 实际 0.15）
⇒ **0.125 下限确实存在**，且意味着 **TO 降到 0.125 以下对 fitness 再无增益**。

### ★ 由此得到破闸的**充要条件**

要 `F ≥ 1.0`：`returns / max(TO, 0.125) ≥ 1/S²`

| 起点 | S | returns | TO | 需 TO ≤ | 需降幅 |
|---|---:|---:|---:|---:|---:|
| `N1ewm5Jw` | 2.13 | 0.0424 | 0.662 | **0.192** | −71% |
| `XgRrrVXz` | 1.88 | 0.0405 | 0.473 | **0.143** | −70% |
| `vROq32rz`（TOP2000） | 1.47 | 0.0576 | 0.481 | **0.124** | −74% |

⇒ 三条路只需命中一条：① TO ≤ 0.19；② returns ≥ 0.11；③ S ≥ 4.0（不现实）。

### ★★ 论坛破闸手法实测：全部失败，但排除了 4 类路径

论坛高赞帖（《降低换手率的方法》《store+死区降低换手率》《高换手率因子优化经验分享》）
的核心手法都是**强制降换手**。本族逐一实测：

| 手法 | TO | S | F | 判定 |
|---|---:|---:|---:|---|
| `ts_target_tvr_decay(target_tvr=0.10)` | **0.090**（低于下限！） | 0.71 | 0.25 | ❌ **TO 达标但 S 崩 67%** |
| `ts_target_tvr_decay(target_tvr=0.05)` | 0.065 | 0.29 | 0.07 | ❌ 更差 |
| `hump(hump=0.001)` | 0.207 | 0.76 | 0.19 | ❌ TO −69% / S −64% |
| `ts_target_tvr_hump(target_tvr=0.10)` | **0.031** | **−0.21** | −0.03 | ❌ **信号完全杀死** |
| `ts_decay_linear`（早期已测） | 0.076 | 0.54 | 0.20 | ❌ 零和 |

⇒ ★★ **决定性结论：降 TO 在本族是「等比降 S」，不是免费午餐。**
`ts_target_tvr_decay` 把 TO 精确压到 **0.090（已低于 0.125 下限，分母已达理论最优）**，
但 S 从 2.13 → 0.71（−67%），F 反而 0.54 → 0.25。
⇒ **即使 TO = 0.125（分母最优），本族 returns 0.0424 只能给出 F = 0.71×√(0.0424/0.125) = 0.41 < 1.0。**
⇒ 必须抬 returns，而抬 returns 只能靠 universe（TOP2000 已把 returns 从 0.0424 抬到 **0.0789，+86%**），
但 TOP2000 又把 S 压到 1.59 ⇒ **两端仍卡 F ≈ 0.55**。

### ⇒ 最终裁决：`short_interest_pred.predicted_change` 属**数据集层 fitness 天花板 ≈ 0.55**

与 `macro38`（fit 0.82）、`continuation_score`（F 0.42）、`si3×obim`（margin 0–0.6bp）同类。
该数据集 10 个字段只有此 1 条有信号（`surprise_*` 四字段 / `predicted_value` / `prior_*` 全部实测判死）
⇒ **无第二条腿 ⇒ 需换数据集。**

### 附：论坛确认的通用认知（本轮实测一致）

- 《开发高换手率的Alpha因子》：「**最常见的错误是直接以换手率为目标，而不是去捕捉短周期的信息来源。高换手应该是一个想法的结果，而不是想法本身**」
  ——与本族「TO 0.66 是 `reverse` + 日更预测变动的**固有成本**、不可事后剥离」完全吻合。
- 新腿 `E5V73M6L`（`ts_quantile`）**S 1.95 / 2Y 4.53 / SUB 1.32 / ppa_failed=false**，
  但 fitness 0.47 低于冠军且**与冠军同腿**（互冲）⇒ 不构成第二条腿。
- `ts_ir`（S −0.20）不可用；`bucket` 喂 `group_rank` 会报
  `Incompatible unit ... expected "Unit[]", found "Unit[Group:1]"` ⇒ **`bucket` 产物是 GROUP unit，只能当分组轴**。

### 破闸工具的可用性速查（本轮实测签名）

| 算子 | 可用签名 | 备注 |
|---|---|---|
| `ts_target_tvr_decay` | `(x, lambda_min=0, lambda_max=1, target_tvr=0.10)` | 四个参数**必须具名** |
| `ts_target_tvr_hump` | `(x, target_tvr=0.10)` | **无** `hump=` 参数（加了报 SYNTAX） |
| `hump` | `(x, hump=0.001)` | 第 2 参**必须具名**，否则 toolkit 静态闸拦 |
| `ts_step` | `(x)` | 只收 1 参，无窗口 |
## 9. 判死清单（本轮实测，勿重试）

| 数据集 / 族 | 死因 | 代表 alpha |
|---|---|---|
| `board_gov_stats`（治理水平值全族） | S 0.11 / −0.16，2Y ≤ 0.46 | `omop8VM2` / `pwvXY8Ab` |
| `insider_agg_matrix.significant_value_*` | b3 骨架 S 0.74（水平值 + `ts_zscore` 无效） | `3qjbQg8X` |
| `insider_agg_matrix.directional_indicator_2` | **longCount=0 毒字段** | `N1ewxkYE` |
| **`option3` 全族** | **天花板 0.88**（8 条 4 变体穷尽：`ts_rank` / `ts_delta` / `ts_zscore66` / `ts_sum` / `ts_av_diff` / `subtract` / OTM 比率 / bucket 轴） | `A1QWjxNX`（S 0.88） |
| `short_interest_pred.surprise_{ratio,value,amount}` + `prior_surprise_ratio` | S ≤ 0.17 且 2Y 多负；原 2Y 4.03 是 TO 0.761 假强 | `d5KXpkVv` / `88vob5da` / `JjPwqMKx` / `XgRrmAJm` |
| `short_interest_pred.prior_predicted_change` | S −0.32 | `YPxrrLgo` |
| `short_interest_pred.predicted_value`（作主信号） | S 0.82–1.13，2Y 0.36–1.32 | `rKd33pPj` / `mLY33w52` / `QPYJkm1X` |
| `macro63`（3 个二元成分 flag） | 只能当 group 轴，不能作信号 | — |

**⇒ `option3` 的判死把 `option.md` 的结论推进一层**：原文说「option 塔 surface-level IV 全关，只剩 volume/OI 可用」，
本轮实测 **volume/OI 也只到 0.88** ⇒ **USA option 塔整体无可提交信号**。

---

## 10. 工程坑（两道闸对同一写法判断相反）

| 写法 | `preflight_expressions` | toolkit 静态闸 | 结论 |
|---|---|---|---|
| `winsorize(x, 3)` | 报 `unknown_fields: ["std"]`（把 std 当字段名解析） | `[SYNTAX] Invalid number of inputs : 2, should be exactly 1` | ❌ **两侧都拦，本轮无法使用** |
| `winsorize(x, std=3)` | `unknown_fields: ["std"]` | — | ❌ |
| `if_else(…, industry)`（4 参） | 未拦 | `[SYNTAX] 函数 if_else 最多接受 3 个参数` | ⇒ **`group_rank` 必须包在 `if_else` 外层** |

⇒ **发批前必须同时过 `preflight_expressions` 与 toolkit 静态闸，两者互补不可互替。**
⇒ 替代方案：用 `ts_av_diff` 系算子（本轮已证明更优），不必依赖 `winsorize`。
---

## 10. ★★★★★ 反向工程 39 颗 USA ACTIVE：fitness 公式全量确证 + 选集硬筛标准

### 公式在 39 颗 ACTIVE 上验证：平均误差 **0.2%**、最大 **0.8%**

```
fitness = S × √( returns / max(TO, 0.125) )
```

### ★★★ 决定性统计：**29/39 颗 ACTIVE 的 TO < 0.125**（fitness 分母下限之下）

| 典型 ACTIVE | S | TO | returns | F | 数据集 |
|---|---:|---:|---:|---:|---|
| `KPrGMXZ8` | 1.95 | **0.059** | 0.0520 | 1.26 | analyst_consensus（季频预测） |
| `omWMO06n` | 2.50 | **0.089** | 0.0463 | 1.52 | earnings_sent_matrix |
| `d51A3nqY` | 2.45 | **0.095** | 0.0451 | 1.47 | ai_equity_alpha |
| `xAdL5vmN` | 4.51 | **0.061** | 0.1049 | 4.13 | ai_equity_alpha |

⇒ **USA 过 fitness 闸的压倒性路径是「低换手慢信号」，不是「高 returns」。**
⇒ ⚠ **日更字段在 USA 过不了 fitness 闸**：本轮 `short_interest_pred.predicted_change`（日更）TO 0.662，
在 39 颗 ACTIVE 里属异常高换手（仅 3 颗 TO>0.45）⇒ **先天劣势**。

### ★★★ 由此得到的**选集硬筛**（开波前必问，写入 S0）

| 筛项 | 判据 |
|---|---|
| **① 字段更新频率** | **必须能支撑 TO<0.125**：季频/月频慢变量 ✅；**日更快变量直接跳过**（已实测：`predicted_change` / 全部社媒 / 全部 option 价 / T4 模板都救不回） |
| **② coverage 不是否决项** | cov < 0.65 **反而是优势**：cov 低 ⇒ 只有大公司有数据 ⇒ **换手天然低**。`workforce_flow_skills` cov 仅 **0.5754** 却过了 fitness 闸 |
| ③ 低拥挤 | `alphaCount` 低（prod 干净区） |
| ④ 未点亮塔 | 排除 model / analyst / earnings（本季已亮） |

### ★★★ 换集判据的修正（本轮血泪）

**「元数据好看」≠「能过 fitness」**：`twitter_sentiment_l2` 画像全优（95 MATRIX / cov 0.82–1.0 / αC 0–40 /
机制正交），实测 **TO 0.48–1.06 全部破 `HIGH_TURNOVER`，S ≤ 0.79** ⇒ **注意力型社媒字段在 USA 是高频事件型**，
与 sentiment21/22 判死同因。**筛掉它的唯一正确理由是 TO，不是拥挤度。**

---

## 11. ★★★★★ 第二腿突破：`workforce_flow_skills`（other 塔 mult **1.4** 全平台最高）

### 胜出表达式（首个过 `LOW_FITNESS` 的未点亮塔候选）

```text
group_rank(ts_zscore(ts_backfill(divide(vec_sum(employee_inflow_count),
            add(vec_sum(employee_outflow_count), 1)), 252), 252), industry)
USA / TOP3000 / D1 / STATISTICAL / decay 10 / truncation 0.08 / nanHandling ON / maxTrade OFF
```

| alpha | S | F | 2Y | SUB | TO | returns | inv_S | inv_F | 失败闸 |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---|
| **`rKd3Lro9`** | **2.22** | **1.28 ✓** | 0.93 ❌ | **1.00 ✓** | **0.0606** | 0.0418 | 2.07 | 1.16 | **仅 `LOW_2Y_SHARPE`** |
| `vROq9bZa`（bf126/z252） | 2.20 | 1.27 ✓ | 0.92 | 0.99 ✓ | 0.061 | 0.0414 | 2.05 | 1.14 | 仅 2Y |
| `P0MW6bPM`（bf504/z504） | 2.17 | 1.24 ✓ | 0.73 | 0.90 | 0.059 | 0.0405 | 2.04 | 1.12 | SUB+2Y |

`failed_ra_count=1`｜`ppa_failed=false`｜`MATCHES_PYRAMID` PASS｜
`pyramids.list = [USA/D1/OTHER, **multiplier 1.4**]` ⇒ **过闸即点亮 other 塔**。

**机制**：**净招聘流入/流出比**（inflow/(outflow+1)）= 劳动力扩张强度。
学术支撑：企业招聘是**先行指标**，净扩张预示盈利改善与股价上修
（labour reallocation / 无形资本积累，Haltiwanger–Bartik 假设）。

### 本数据集三条结论

1. **比率形态 >> 水平值**：净招聘比 S **2.22** vs `ts_av_diff(vec_avg(inflow))` S **1.00**（**2.2 倍**）。
2. **窗口修不了 2Y**：bf/z 三档 126/252/504 ⇒ 2Y 0.92/0.93/0.73，**无单调关系**
   ⇒ **2Y 是数据期属性，不是参数问题**。
3. ⚠ **修正 §3 的适用范围**：`ts_av_diff` / `ts_rank` 在本集**反而弱**（S 0.69–1.00）
   ⇒ **「`ts_av_diff` 优于 `ts_zscore`」是 `short_interest` 特定，不是普适定律** ⇒ 逐数据集实测。

### 互补腿（组合腿救援素材）

| 机制 | 表达式 | S | F | 2Y | SUB | TO |
|---|---|---:|---:|---:|---:|---:|
| **量**扩张 | 净招聘比 | **2.22** | 1.28 ✓ | 0.93 | 1.00 ✓ | 0.061 |
| **价**扩张 | 薪资/招聘比 | 1.70 | 0.86 | **1.44** | 0.39 | 0.052 |
| **价**扩张（vec_sum） | 薪资/招聘比 | 1.42 | 0.66 | **1.54** | 0.20 | 0.059 |

⇒ 两条腿的 S 与 2Y **反向互补**（强 S/弱 2Y vs 弱 S/强 2Y）
⇒ 这是**组合腿救援的理想场景**（属两种经济机制，不是 add 混信号）。

---

## 12. 工程坑：preflight 的 `auto_fix_vector` 会产出双层包裹

| 写法 | `preflight` 输出 | 平台结果 |
|---|---|---|
| `vec_avg(divide(A, add(B,1)))`（A/B 为 VECTOR） | 自动改成 `vec_avg(vec_sum(A))` = **双层归约** | ❌ **整批 4 条全 ERROR** |
| 同上 | `validate_expressions` 返回 **valid=true** | ⇒ **valid ≠ 可派发** |
| ✅ 正确：`divide(vec_sum(A), add(vec_sum(B), 1))` | 单层 | ✅ 4/4 COMPLETE |

⇒ **VECTOR 比率必须手写单层聚合**；`fixed_expressions` 要**逐字读**，
不要信 `any_changed=true` 就发批（本轮浪费 1 批 4 条）。

---

## 13. ★★★★★ `SECTOR` 中性化 = USA fitness/margin 杠杆（本轮最高价值发现之一）

同一条表达式（净招聘比）**只换 `neutralization`**：

| neut | S | **F** | 2Y | SUB | **TO** | **returns** | **margin** |
|---|---:|---:|---:|---:|---:|---:|---:|
| STATISTICAL | 2.22 | 1.28 | 0.93 | 1.00 | 0.0606 | 0.0418 | 13.8bp |
| **SECTOR** | 1.73 | **1.34** | **1.05** | 1.21 | **0.0379** | **0.0750** | **39.6bp** |
| SECTOR + `quantile` | 1.75 | **★1.41** | **1.10** | 1.21 | **0.0317** | **0.0810** | **51.2bp** |
| SECTOR + 轴 market | 1.71 | 1.35 | 1.07 | 1.09 | 0.0362 | 0.0782 | 43.2bp |
| SECTOR + 轴 subindustry | 1.72 | 1.29 | 1.05 | 1.13 | 0.0398 | 0.0706 | 35.5bp |

⇒ ★★ **`SECTOR` 让 S 降 22% 但 returns 涨 79%、TO 降 37% ⇒ fitness 反升、margin 涨 2.7 倍。**
机制：`SECTOR` 剥掉行业共性后剩下的是**行业内相对信号**，持仓更稳 ⇒ 每单位权重收益更高。

⇒ ★★ **两轴分工，不是替代关系（修正本文 §10 与旧记忆的「USA 一律用 STATISTICAL」）**：

| 中性化轴 | 作用 | 证据 |
|---|---|---|
| **STATISTICAL** | **prod 杠杆** | `omWMO06n` prod 0.6948 PASS |
| **SECTOR** | **fitness / margin / SUB 杠杆** | 本节 F 1.28→1.41、margin 13.8→51.2bp |

⇒ **`quantile` 在慢信号低换手族是增益算子**（F 1.34→1.41、TO 再降、margin +29%）
——与「`signed_power` 被 `quantile` 抵消」不是一回事（那是幂次 vs 分位归一化）⇒ **按算子语义分类，不按名字类推**。

---

## 14. `workforce_flow_skills` 的 2Y 是数据期硬顶（穷尽 20+ 变体）

| 变体 | 2Y |
|---|---:|
| STATISTICAL bf252 | 0.93 |
| SECTOR bf252 | 1.05 |
| SECTOR + `quantile` | 1.10–1.13 |
| SECTOR + `quantile` + TOP2000 | 1.03 |
| **SECTOR + `quantile` + 减法净差比 `(in−out)/(in+out)`** | **★1.17** |

已穷尽：neut 5 档 × universe 2 档 × decay 2 档 × 窗口 6 组 × `quantile` × 轴 3 档 × 骨架 3 种 × 比率形态 3 种。

⇒ **2Y 封顶 ≈1.17，缺口 0.41。机制判定**：净招聘流量的近两年（2022–23）受后疫情用工正常化压制，
净流入率横截面 dispersion 收缩 ⇒ 全期 S 1.75 由 2014–21 早期样本贡献。
⇒ **数据期结构问题，算子/设置救不回。**

### ★ 但三个确定收益（不因 2Y 失败而作废）

1. **`SECTOR` 中性化 = USA fitness/margin 杠杆**（见 §13）。
2. **`quantile` 在慢信号低换手族是增益算子**。
3. **对称化比率 `(in−out)/(in+out)` 优于除法比 `in/(out+1)`**：
   2Y 1.17 vs 1.05、S 1.62 vs 1.73、F 1.20 vs 1.16、**SUB 1.38 vs 1.21**
   ⇒ 分母不随「分母趋零」而爆 ⇒ **低换手族优先用对称化比率**。

⇒ **裁决：判「机制成立、闸差一口」**，`failed_ra_count=1` 且唯一缺口是数据期 2Y ⇒ 留档不提交。
⇒ **下一腿**：`hiring_trends`（other 塔同族，cov 0.4987，`j2rrpVzO` 已证明 **TO 0.163 / F 1.78** 可过 fitness）
的其余字段。

### 最优候选留档

| alpha | 表达式 | S | F | 2Y | SUB | TO | returns | margin |
|---|---|---:|---:|---:|---:|---:|---:|---:|
| `bl8kNqRm` | `quantile(group_rank(ts_zscore(ts_backfill(divide(vec_sum(employee_inflow_count), add(vec_sum(employee_outflow_count),1)),252),252), industry))` @ TOP3000/SECTOR/d10 | 1.75 | **1.41** | 1.10 | 1.21 | 0.0317 | 0.0810 | **51.2bp** |
| `kqJ7QW9O` | 同上但 `divide(subtract(in,out), add(in,out))` @ TOP2000/SECTOR/d5 | 1.62 | 1.20 | **1.17** | **1.38** | 0.0383 | 0.0682 | 35.6bp |

---

## 15. 第三腿 `hiring_trends` 判死 + ★ USA 合法 universe 已变更

3 字段（全 VECTOR，cov 0.4998）：`aggregate_open_positions_count`（**已被 `j2rrpVzO` 占一腿**）/
`fresh_open_positions_count` / `rolling_84d_new_positions_sum`。

TOP2000 / SECTOR / decay 3：`omopKp62`（T4 `rolling_84d`）**S 1.27 / F 0.85 / TO 0.135 / SUB 0.92 / 2Y 0.70**、
`vROqLqra`（T4 窗 252）S 1.15 / F 0.83 / **2Y 1.16**、`leMqVq8N`（b3+`quantile`）S 1.03 / F 0.72 / TO 0.047
⇒ **均未过 3 闸** ⇒ 判死。

⇒ ★ **未测字段均弱于已占用的 `aggregate_open_positions_count`**（该字段 S 2.19/F 1.78）
⇒ 该集有效信号集中在「总职位数」单字段，另两个是其子集/增量口径，**信息量重叠**。

### ★★★ USA 合法 universe 已变更（影响历史复现）

平台报错原文：
```
universe 'ILLIQUID_MINVOL1M' not valid for region 'USA'.
Valid: ['TOP3000', 'TOP2000', 'TOP1000', 'TOP500', 'TOP200', 'TOPSP500']
```

⇒ ★★ **历史 ACTIVE `j2rrpVzO` 用的正是 `ILLIQUID_MINVOL1M`**
⇒ **存量 alpha 能跑 ≠ 现在能复现**；其低换手（TO 0.163）可能来自该宇宙的大市值偏好，而非字段本身慢
⇒ **不可把它的 fitness 当作该数据集在 TOP3000 下可复现的证据**（修正本文 §10 的选集推论）。

⇒ **TOP2000 是杠杆不是主信号**（本轮两腿独立验证）：
`rolling_84d` TOP3000（S 1.18 / TO 0.079）→ TOP2000（**S 1.27 / TO 0.135**）；
`short_interest` TOP3000（returns 0.0424）→ TOP2000（**returns 0.0789，+86%**）。

---

## 16. ★★★ 本战役最终裁决（3 腿 / 26 波 / 104 条）

| 腿 | 数据集 | 塔 / mult | 最优 | 裁决 |
|---|---|---|---|---|
| 1 | `short_interest_pred` | shortinterest / 1.1 | `N1ewm5Jw` S2.13 / **F0.54** / TO0.662 | ❌ **日更字段 ⇒ TO 结构性出局** |
| 2 | `twitter_sentiment_l2` | socialmedia / 1.0 | S 0.79 / TO 0.48–1.06 | ❌ 高频事件型，`HIGH_TURNOVER` 破闸 |
| 3a | **`workforce_flow_skills`** | **other / 1.4（最高）** | **`bl8kNqRm` S1.75 / F1.41✓ / TO0.032 / 2Y1.10** | ★ **过 4 闸，仅差 2Y（族内硬顶 1.17）** |
| 3b | `hiring_trends` | other / 1.4 | `omopKp62` S1.27 / F0.85 | ❌ 3 闸 |

**唯一实质成果**：`bl8kNqRm`（净招聘流入/流出比，other 塔 mult 1.4）
`failed_ra_count=1`｜**SHARPE/FITNESS/SUB_UNIVERSE/MATCHES_PYRAMID 四闸 PASS**｜`ppa_failed=false`｜
margin **51.2bp**｜TO **0.0317**｜risk_neutralized_S 2.14 ｜**距全闸只差 `LOW_2Y_SHARPE` 0.41**。

### 方法论净收获（跨区可迁移，已全部写入本 skill）

1. **fitness 精确公式 + 0.125 硬下限**（39 颗 ACTIVE 验证，误差 0.2%）。
2. **选集硬筛：先问字段更新频率能否支撑 TO<0.125；日更字段直接跳过**；**cov<0.65 反是优势**。
3. **`SECTOR` = fitness/margin 杠杆**（F 1.28→1.41、margin 13.8→51.2bp）；`STATISTICAL` = prod 杠杆。**两轴分工**。
4. **`quantile` 在慢信号低换手族是增益算子**（不是幂次替代）。
5. **对称化比率 `(a−b)/(a+b)` 优于 `a/(b+1)`**（2Y 1.17 vs 1.05、SUB 1.38 vs 1.21）。
6. **比率形态 >> 水平值**（净招聘比 S2.22 vs 单腿 S1.00，2.2 倍）。
7. **`ts_av_diff` 更优是数据集特定，非普适**（本集反而弱）⇒ 逐数据集实测。
8. **TOP2000 是杠杆不是主信号**（两腿独立验证：抬 returns / 压 TO）。
9. **`ILLIQUID_MINVOL1M` 对 USA 已失效** ⇒ 存量 ACTIVE 设置未必可复现。
10. **槽位饥饿表现为 progress 停在 0.1/0.15** ⇒ 改一个设置维度另起一批，**勿空等、勿原样重发**（原样重发会自相关互冲）。
11. **preflight `auto_fix_vector` 会产出双层 `vec_*` 包裹导致整批 ERROR**；`validate_expressions` 的 valid ≠ 可派发。

---

## 17. 第四腿 `institutions18` 判死 —— ★ 硬筛完全奏效，但解决不了强度

选集严格按 §10 硬筛：**季频**（⇒ TO 天然低）× institutions 塔本季 0 颗 × cov 1.0 MATRIX。
17 字段含两组天然配对（`cur_holding`/`pre_holding`、`cur_mv`/`vm_erp`）⇒ 用**对称化变化率** `(cur−pre)/(cur+pre)`。

| 表达式 | S | F | 2Y | SUB | TO | 失败闸 |
|---|---:|---:|---:|---:|---:|---|
| `fundownershipv2` **市值**变化率 | 0.92 | 0.62 | **1.27** | 0.64 | **0.066** | S/F/2Y |
| `fundownershipv2` **持股数**变化率 | 0.90 | 0.60 | 1.25 | 0.55 | 0.066 | S/F/2Y |
| `instownership` 持股数变化率 | 0.31 | 0.16 | −0.06 | 0.23 | 0.037 | S/F/2Y |
| `fundownershipv2_pct_held` 水平 | **−0.41** | −0.17 | 1.05 | −0.34 | 0.143 | S/F/SUB/2Y |
| `lionshares_insider_num` | 0.67 | 0.37 | 0.72 | 0.74 | 0.086 | S/F/2Y |

⇒ ★★ **硬筛完全奏效**：季频 ⇒ **TO 0.037–0.143**（vs `short_interest` 日更腿的 0.662）
⇒ **「日更字段直接跳过」这条硬筛被独立验证**。
⇒ ❌ **但信号强度不足**（S ≤ 0.92，距 1.58 差 1.7×）⇒ 判死，与 `references/institutions.md`
（「56 条回测 / 6 条 RA 全过但 prod 全挂」）一致。
⇒ ★ `pct_held` 水平值 **S −0.41（反向）** ⇒ 机构持股**比例**本身是反向信号（过度机构化 ⇒ 收益低），
但 TO 0.143 偏高、S 绝对值太小，不值得挖。
⇒ ★ **`instownership_*`（cov 0.7879）全族弱于 `fundownershipv2_*`（cov 1.0）** ⇒ 覆盖率高的口径更可靠。

---

## 18. ★★★ 四腿总结论（本战役最浓缩的一条）

> **硬筛（月频/季频）解决了 fitness / TO 问题，但解决不了信号强度问题。**

| 腿 | 字段频率 | TO | S | 结论 |
|---|---|---:|---:|---|
| `short_interest_pred` | **日更** | 0.662 | **2.13** | 强度够，**fitness 结构性不可达** |
| `institutions18` | 季频 ✅ | 0.066 | 0.92 | **fitness 没问题**，强度不够 |
| `workforce_flow_skills` | **月频 ✅** | **0.032** | **1.75** | ★ **两者同时满足 ⇒ 唯一成果** |

⇒ **选集必须同时满足两个条件，缺一不可**：
1. **频率够慢**（⇒ `F = S×√(returns/max(TO,0.125))` 的分母达标）；
2. **是「流量/变化率」而非「存量/水平值」**（`workforce_flow_skills` 的净流入比 vs
   `institutions18` 的持仓变化率 —— 后者是**季频存量差分**，噪声被季频平滑吃掉 ⇒ S 仅 0.92）。

⇒ ★ **可操作的判据**：季频**存量**（持仓量、持股数、库存量）的差分在 USA 噪声太大；
**月频流量**（招聘流入流出、订单流、授信额度变化）才有横截面预测力。

---

## 19. `workforce_flow_skills` 算子穷尽：2Y 硬顶 = 数据期结构

对净招聘比 `(in−out)/(in+out)`，穷尽了 10 个时序算子（窗 126/252/504 × 各算子）：

| 算子 | S | F | 2Y | SUB | TO |
|---|---:|---:|---:|---:|---:|
| `ts_std_dev(·,126)` | 1.62 | 1.21 | **1.48** | 0.95 | 0.013 |
| `ts_av_diff(std_dev(·,126),252)` | 1.68 | 1.29 | 1.37 | 1.07 | 0.017 |
| `ts_delta(std_dev(·,126),22)` | 1.69 | 1.32 | 1.11 | 1.18 | 0.033 |
| `ts_kurtosis(·,126)` | 1.63 | 1.27 | 1.26 | 1.02 | 0.022 |
| `ts_arg_max(·,126)` | 1.56 | 1.17 | 1.33 | 0.82 | 0.025 |
| `ts_rank(·,504)` | 1.36 | 0.79 | 0.79 | 0.82 | 0.142 |
| `tail(·,0.2,0.8,0)` | 1.57 | 1.22 | 1.13 | 1.12 | 0.018 |
| `ts_scale(·,252)` | 1.65 | 1.27 | 1.31 | 1.07 | 0.019 |
| `reverse(ts_corr(in,out,126))` | 1.52 | 1.17 | 1.23 | **1.24** | 0.019 |
| `ts_regression(·,126,1)` | **0.00** | — | — | — | — |

⇒ ★★ **10 个算子穷尽后 2Y 全卡 1.11–1.48，无一例外** ⇒ **本族 2Y 硬顶 ≈1.48，缺口 0.10**，
确证是「后疫情用工正常化」的数据期结构问题 ⇒ **算子/设置不可救** ⇒ 存档不提交。

**★ `ts_corr` 揭示第二条腿**（节奏/混乱度 vs 水平值的量）：
`LL5jMGPM` 正向 S **−1.63** ⇒ `0mjlPdvK` 反向 S **+1.52 / F 1.17 / SUB 1.24 / TO 0.019 / 2Y 1.23**，
机制 = 「流入/流出高度相关（同开同关）的公司未来收益更差」⇒ 反向做多「进出平稳」。
**与净招聘比属两个正交机制**（`ts_corr` 与 `divide` 的乘积相关性 0.84 < 0.7）⇒ 合法的同数据集双腿。

**★ 毒算子**：`ts_regression` 在本集**全零持仓**（S=0、TO=0、longCount=0）⇒ **该集字段不兼容此算子，勿再试**。

### 候选池（全过 SHARPE/FITNESS/SUB/TO/CW/MATCHES_PYRAMID 六闸，仅差 2Y）

| alpha | 表达式 | S | F | 2Y | SUB | TO | margin |
|---|---|---:|---:|---:|---:|---:|---:|
| **`d5KXbPov`** | `quantile(group_rank(ts_std_dev(divide(subtract(vec_sum(in),vec_sum(out)),add(vec_sum(in),vec_sum(out))),126), sector))` | 1.62 | 1.21 | **1.48** | 0.95 | 0.013 | 109bp |
| `akVYVjo2` | 同上，`ts_delta(std_dev,22)` | **1.69** | **1.32** | 1.11 | 1.18 | 0.033 | 47bp |
| `RRA3Ajd1` | 同上，`ts_av_diff(std_dev,252)` | 1.68 | 1.29 | 1.37 | 1.07 | 0.017 | 87bp |
| `WjLqL1Nx` | 同上，`ts_kurtosis` | 1.63 | 1.27 | 1.26 | 1.02 | 0.022 | 68bp |
| `JjPweGjE` | 同上，`ts_scale` | 1.65 | 1.27 | 1.31 | 1.07 | 0.019 | 77bp |

全部 `ppa_failed=false`、`pyramids=[USA/D1/OTHER, mult 1.4]`。
⇒ **数据期结构问题解除（2Y 稳定 >1.58）或换「月频流量 + 机制不同」的数据集前，不再重复试算子**。

---

## 20. 终局：算子穷尽后 2Y 硬顶确证为数据期结构（战役收口）

### `submit_verdict` 实证（冠军 `d5KXbPov`）

```
verdict = BLOCKED   reason_code = SIM_FAIL:LOW_2Y_SHARPE
value = 1.48   limit = 1.58   缺口 = 0.10
其余全部 PASS：SHARPE / FITNESS / LOW_SUB_UNIVERSE_SHARPE / LOW_TURNOVER / HIGH_TURNOVER /
              CONCENTRATED_WEIGHT / MATCHES_PYRAMID ；ppa_failed = false
```

### 2Y 杠杆穷尽清单（全部实测，全部无效）

| 维度 | 范围 | 2Y 峰值 |
|---|---|---:|
| 时序算子（10 个） | `ts_std_dev`/`ts_av_diff`/`ts_delta`/`ts_kurtosis`/`ts_arg_max`/`ts_rank`/`tail`/`ts_scale`/`ts_corr`/`ts_regression` | 1.11–**1.48** |
| 窗口 | 63 / 126 / 189 / 252 / 504 | 1.07–1.48 |
| 中性化轴 | STATISTICAL / SECTOR / INDUSTRY / SUBINDUSTRY / MARKET | 1.05–1.48 |
| universe | TOP3000 / TOP2000 | TOP2000 **全差**（2Y 1.07–1.32 vs TOP3000 1.48）|
| delay | 1 / **0** | **delay 0 报「unknown variable employee_inflow_count」** |
| truncation | 0.08 / 0.04 | 无差 |

⇒ ★★ **该族 2Y 硬顶 ≈1.48，缺口 0.10，属数据期结构问题（后疫情用工正常化 ⇒ 近两年净流入率横截面收缩）**。
⇒ **判定：机制成立、闸差一口（仅 2Y），存档不提交。** 不再重复试算子。

### ★★★ 终局三条新结论（跨区可迁移）

1. **算子穷尽后 2Y 不动 = 数据期问题的铁证**：2Y 由「近 2 年样本表现」决定，与算子/窗口/中性化无关。
   若某族 2Y 全卡同一水平 ⇒ **先判定数据期结构，再决定要不要换集**（不要盲目继续扫算子）。
2. **`delay=0` 不可用 = 慢数据集的固有约束**：`workforce_flow_skills` 报「unknown variable employee_inflow_count」
   ⇒ **只到 delay 1** ⇒ **无法靠更鲜数据提 2Y**（慢信号的 2Y 只能靠时间流逝自然修复）。
3. **`ts_corr` 与净招聘比正交（0.84 < 0.7）⇒ 合法的同数据集双腿**（量 vs 节奏）：
   `LL5jMGPM` 正向 S −1.63 ⇒ `0mjlPdvK` 反向 **S +1.52 / F 1.17 / SUB 1.24 / TO 0.019**。

### 战报总览（最终）

| 腿 | 数据集 | 塔/mult | 最优 | 结论 |
|---|---|---|---|---|
| 1 | `short_interest_pred` | shortinterest/1.1 | S2.13 / F0.54 | ❌ 日更 ⇒ fitness 结构性不可达 |
| 2 | `twitter_sentiment_l2` | socialmedia/1.0 | S0.79 / TO0.48–1.06 | ❌ 高频事件型，HIGH_TURNOVER |
| 3a | **`workforce_flow_skills`** | **other/1.4** | **`d5KXbPov` S1.62/F1.21/SUB0.95/2Y1.48** | ★ **六闸 PASS，仅差 2Y** |
| 3b | `hiring_trends` | other/1.4 | S1.27 / F0.85 | ❌ 3 闸 |
| 4 | `institutions18` | institutions/1.0 | S0.92 / F0.62 | ❌ 强度不足 |

**累计**：34 波 / 128 条回测 / 6 数据集 / 11 个新结论沉淀进 skill。

---

## 21. 第五腿 `macro27`（macro 塔，招聘数据）判死 —— 同机制、信号更弱

| 表达式 | S | F | 2Y | SUB | TO |
|---|---:|---:|---:|---:|---|
| `A1QWrqqW` jobsremoved/(jobscreated+1) | 0.74 | 0.42 | 0.88 | 0.25 | 0.081 |
| `xA162XXw` (removed−created)/(removed+created) | 0.65 | 0.35 | 0.69 | 0.26 | 0.094 |
| `omopJQQn` std_dev(net ratio,126) | 0.92 | 0.52 | 0.29 | 0.58 | 0.016 |
| `xA162XXN` reverse(jobsactive) | 0.53 | 0.25 | 0.60 | 0.20 | 0.040 |

⇒ **判死**：同「招聘流量」机制但 **S ≤ 0.92**（比 `workforce_flow_skills` 的 1.75 弱近一半）。

### ★★ 关键判据（新）：**同一机制、不同数据集、不同更新频率 ⇒ 优先更新频率更高的**

`workforce_flow_skills` 是**日频流量**（inflow/outflow 每天都有值）；
`macro27` 是**周频抓取**（`since the prior scrape` ⇒ 一周一更新）
⇒ **数据更新频率越低，横截面信号越钝** ⇒ workforce 日更 > macro27 周更。

⇒ ★ **`reverse(jobsactive)` S 0.53（正向）**：「在招岗位越少越好」是弱信号 ⇒
「在招岗位数」**不是**好信号（与 `hiring_trends` 的 `aggregate_open_positions_count` 判死一致）。

---

## 22. ★★★ 收官：未点亮塔月频流量集已全部穷尽（战役最终裁决）

### 最后 3 个候选的画像评估（不用回测就能判）

| 数据集 | 塔 | 画像 | 不投理由 |
|---|---|---|---|
| `macro63` | macro/1.1 | 3 字段全是二元指数成分 flag | **只能当分组轴，不能当信号**（连续 alpha 需要连续字段） |
| `other551` | macro/1.1 | 33 字段全是**日频** beta/R²/resret（αC 30–748） | **日更字段 ⇒ fitness 结构性不可达**（与 short_interest 腿同因）|
| `mfm_model_output` | risk/1.1 | 117 字段**日频**行业暴露 + 行业 flag | **日更字段**（同 short_interest 腿）+ 行业 flag 不能当信号 |

### ★★★ 终局判据（本战役最重要的一条，跨区可迁移）

> **「月频流量 + 非存量 + 低拥挤 + 未点亮」四条件同时满足的数据集已全部穷尽。**

`workforce_flow_skills` 是**唯一命中的**（净招聘比，other 塔 mult 1.4 最高档），
且已算子穷尽到 **2Y 数据期硬顶 ≈1.48**（缺口 0.10）。

⇒ **下一步必须换主题，不是换数据集**——招聘流量主题在 USA 已穷尽；
任何想继续在 USA 挖的方向都必须找到**月频流量 + 机制不同**的新数据集（按 §10 硬筛）。

### 战役总账（最终）

| 腿 | 数据集 | 塔/mult | 最优 | 结论 |
|---|---|---|---|---|
| 1 | `short_interest_pred` | shortinterest/1.1 | S2.13 / F0.54 | ❌ 日更 ⇒ fitness 结构性不可达 |
| 2 | `twitter_sentiment_l2` | socialmedia/1.0 | S0.79 / TO0.48–1.06 | ❌ 高频事件型，HIGH_TURNOVER |
| 3a | **`workforce_flow_skills`** | **other/1.4** | **`d5KXbPov` S1.62/F1.21/SUB0.95/2Y1.48** | ★ **六闸 PASS，仅差 2Y** |
| 3b | `hiring_trends` | other/1.4 | S1.27 / F0.85 | ❌ 3 闸 |
| 4 | `institutions18` | institutions/1.0 | S0.92 / F0.62 | ❌ 强度不足 |
| 5 | `macro27` | macro/1.1 | S0.92 / F0.52 | ❌ 同机制、信号更钝 |

**累计**：38 波 / 140 条回测 / 8 数据集 / 14 条新结论沉淀进 skill。全程零自动提交。

---

## 23. ★★★★★ 论坛破 `LOW_2Y_SHARPE` 方法：全部实测 + 适用边界（本战役最重要补充）

### 论坛查到的方法与本族实测结果

| 论坛方法 | 来源（票数） | 本族实测 | 判定 |
|---|---|---|---|
| **neutralization 换 RAM** | LC69991 / SY54221 / ZZ47696 | S 1.62→**1.69**、F→**1.27**、margin 109→202bp，**2Y 1.48→1.33** | ⚠ 抬 S/F/margin，**降 2Y** |
| **neutralization 换 CROWDING** | 同上（论坛 2Y 记录 2.17） | S 1.57、**margin 794bp（7.3×）**、**2Y 1.34** | ⚠ **margin 之王，2Y 不动** |
| **内层 `group_neutralize(industry)`** | ZZ47696（GLB 2Y 1.15→2.04） | `kqJ7GQdg` 2Y 1.28 / `3qjb5eg0` 2Y 1.24 | ❌ 不如裸版 |
| **`rank_by_side`** | 70 票专帖（ladder 0.28→2.44） | 未测 | ⚪ **本账号疑似无权限**（论坛多人提及未解锁）|
| 拉长 `ts_backfill` 窗 | PY82964（2Y 0.65→0.78） | bf126/252/504 全扫 | ❌ 本族无效 |
| `tail` + `rank_by_side` 组合 | XW23690 | 未测 | ⚪ 依赖 `rank_by_side` |

### ★★★★★ 关键诊断：论坛修法**指征不符**，不是配方无效

论坛修法 1 的机制：**「纯风险因子中性化（STATISTICAL/FAST/SLOW）在近两年与信号高度重叠，
把有效收益一起中性化掉了」**。论坛实测表（GLB）：

| neutralization | Sharpe | Fitness | margin(bp) | 2Y |
|---|---:|---:|---:|---:|
| STATISTICAL | 3.04 | 0.86 | 1.58 | 1.15 ❌ |
| FAST | 2.37 | 0.65 | 1.52 | 1.30 ❌ |
| SLOW | 2.75 | 0.76 | 1.52 | 0.96 ❌ |
| SLOW_AND_FAST | 2.38 | 0.58 | 1.19 | 0.72 ❌ |
| **REVERSION_AND_MOMENTUM** | 3.05 | 1.05 | 2.37 | **2.04 ✓** |
| **CROWDING** | 3.13 | 1.17 | 2.79 | **2.17 ✓** |

⇒ ★ **该机制的前提是「高换手线」**（GLB 那条线 turnover 0.6+）。
**本族 TO = 0.013–0.018（比 GLB 低 40 倍）⇒ 低换手线根本不存在「风险因子吃掉收益」的问题**
⇒ 换任何 neutralization 都无效，**2Y 是数据期结构问题**。

### ★★★★ 升级后的通用判据（比论坛原文更严格，跨区可迁移）

> **「全期 Sharpe 正常、只挂 `LOW_2Y_SHARPE`」的处置分流**：
> - **高换手线（TO > 0.2）** ⇒ 第一杠杆 = **neutralization 换 `REVERSION_AND_MOMENTUM` 或 `CROWDING`**
>   （论坛实测 2Y 1.15/1.30/0.96/0.72 → 2.04/2.17，成本 1 条 simulation）；
>   第二杠杆 = **内层 `group_neutralize`**（粒度必须**严格细于**外层 setting，否则 P²=P 退化为恒等）。
> - **低换手线（TO < 0.05）** ⇒ 换 neutralization **无效**（已实测 RAM/CROWDING 均降 2Y），
>   **不要浪费时间**，直接判定为数据期结构问题。
>
> **margin↔Sharpe 取舍表**（论坛拟合，误差 <1%）：
> `Fitness = Sharpe × √(505 × margin)`，`margin = returns/(turnover × 505)`
> ⇒ **等价于本skill 的 `F = S×√(returns/max(TO,0.125))`**（505 = 252 日年化常数）⇒ 两套公式互证。
> margin 掉 10% 需 Sharpe 涨 >5.4%；掉 20% 需 >11.8%；掉 35% 需 >24%。
> **margin 基本只由 setting 决定**（本族实测：CROWDING 让 margin 109→794bp = 7.3 倍）。

### ★ 本战役定案

最优候选仍是 `d5KXbPov`（STATISTICAL）**2Y 1.48**；
`akVYwEJ5`（CROWDING）作为 **「2Y 数据期修复后的高价值储备」**（margin 794bp，收益能力最强）。
**⇒ 存档不提交**（`failed_ra_count=1`，唯一缺口 `LOW_2Y_SHARPE`）。

---

## 24. ★★★★★ 破 2Y 闸的最终答案：`winsorize` / `normalize` 外包（+ 与 `tail` 的分工）

### 核心结论：`winsorize(x, std=N)` 是 USA 低换手族的 **2Y 杠杆**

| 外层处理 | S | F | 2Y | SUB | TO | margin | 失败闸 |
|---|---:|---:|---:|---:|---:|---:|---|
| 无（`d5KXbPov`） | 1.62 | 1.21 | 1.48 | 0.95 | 0.013 | 109bp | 2Y |
| **`winsorize(·,std=3)`**（`rKdgpaPd`） | **1.85** | 1.06 | **1.63 ✓** | 0.70 | 0.045 | 18bp | SUB |
| **`tail(0.2,0.8,0)`+`winsorize(std=3)`**（`qMEr926K`） | **2.17** | **1.28** | 1.11 | **0.98 ✓** | 0.049 | 18bp | 2Y |
| `normalize(·)` | 1.82 | 1.04 | **1.65 ✓** | 0.68 | 0.043 | 19bp | SUB |

**机制**：`winsorize` 把极端值压到统一量纲 ⇒ 抑制「少数极端公司主导近期收益」
（本族 = 2022-23 科技业裁员潮）⇒ **2Y 1.48 → 1.63/1.65 突破**。
这正是论坛 70 票帖 `rank_by_side` 的「降低单股极端贡献」机制 ——
**`rank_by_side` 本账号无权限 ⇒ `winsorize`/`normalize` 是等效替代，实测同样奏效**。

### ★★★★ `winsorize` vs `tail` 的分工（本族实证，与论坛说法相反）

| 算子 | 作用闸 | 机制 |
|---|---|---|
| **`winsorize(std=N)`** | **2Y ↑**（1.48→1.63），SUB ↓（0.95→0.70） | 压极端值，**保留全分布** |
| **`tail(lower,upper,newval)`** | **S/SUB ↑↑**（1.85→2.17 / 0.70→0.98），2Y ↓（1.63→1.11） | **去掉中段噪声**，只信极值 |

⇒ **两者反向**：`tail` 强化「只信极值」，`winsorize` 强化「信全分布」。
⇒ ⚠ **论坛 XW23690「`tail`+`winsorize` 组合 margin 损失更小」不适用于低换手慢信号族** ——
本族实测该组合 2Y 掉到 1.11 ⇒ **论坛组合法逐族实测，不可外推**。

### ★★★★ 修正两条错误铁律（重要）

1. **「2Y 是数据期结构问题、算子不可救」→ 错**。
   判 2Y 死前**必须先试极值压缩类算子**：`winsorize(std=N)` / `normalize()` / `tail(...)`。
2. **「`winsorize` 两道闸都拦」→ 错**。
   平台完整支持 `winsorize(x, std=4)`（定义见 `get_operators`），toolkit 静态闸**接受具名形式**；
   只有 `preflight_expressions` 会误报 `unknown_fields:["std"]`（把 `std` 当字段名解析）
   ⇒ **preflight 误报 ≠ 不可用，以 toolkit 静态闸 + 平台为准**。

### USA workforce 族的机制性权衡墙（最终裁决）

`2Y` 与 `S/SUB` 由外层处理的两端分别把持：
- `winsorize` 端：S 1.85 / F 1.06 / 2Y 1.63 ✓ / **SUB 0.70 ❌**
- `tail` 端：S 2.17 / F 1.28 / 2Y 1.11 ❌ / **SUB 0.98 ✓**

⇒ **两端都不全过** ⇒ 判「机制成立、两闸各差一口」，**存档不提交**。
⇒ **若后续要破**：需在**表达式内层**（而非外层）引入第三个维度 ——
例如 `group_rank` 换成按 `bucket(rank(volatility))` 分组的 `group_neutralize`，
或用 `ts_corr` 腿（本族另一条正交腿，SUB 1.24）与波动率腿做 **Mode B 组合腿**（合规，非 add）。
