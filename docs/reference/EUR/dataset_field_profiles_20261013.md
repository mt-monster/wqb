# EUR 未点亮类别 · 数据集字段画像盘点

> 数据源：WorldQuant BRAIN 平台实时（`get_datafields` / `/data-sets`）
> 范围：EUR / delay=1 / TOPCS1600 ｜ 8 个未点亮类别 ｜ **33 个数据集**
> 采样日期：2026-10-13

---

## 一、总览

| 类别 | 数据集数 | 字段合计 | MATRIX | VECTOR | 零竞争字段(≤3 user) |
|---|---:|---:|---:|---:|---:|
| Analyst | 16 | 2,487 | 1,943 | 544 | 1,929 |
| Sentiment | 5 | 337 | 233 | 104 | 202 |
| Social Media | 2 | 49 | 2 | 47 | 32 |
| Insiders | 3 | 51 | 34 | 17 | 17 |
| Institutions | 2 | 41 | 11 | 30 | 29 |
| Macro | 2 | 34 | 1 | 33 | 20 |
| Earnings | 2 | 62 | 7 | 55 | 6 |
| Imbalance | 1 | 2 | 2 | 0 | 0 |
| **合计** | **33** | **3,063** | **2,233** | **830** | **2,235** |

**⇒ 2,235 个字段（占 73%）处于零竞争状态**（user ≤ 3）；但真正能过闸的只有 1 个数据集。

---

## 二、逐数据集字段画像

### 2.1 Analyst（16 个）

| 数据集 | 字段 | 类型分布 | 零竞争 | 最大覆盖 | 平台用户 | **alphaCount** | 判定 |
|---|---:|---|---:|---:|---:|---:|---|
| ★**`analyst_factor_signals`** | 108 | MAT 108 | **104** | 0.94 | 36 | **58** | ★**胜出** |
| `analyst69` | 297 | MAT 50 / **VEC 247** | 115 | 1.00 | 1626 | **14,111** | ❌ 结构矛盾 |
| `analyst4` | 264 | MAT 130 / VEC 134 | 226 | 1.00 | 812 | 3,031 | ❌ TO 过低 |
| `analyst10` | 294 | MAT 255 / VEC 39 | 220 | 1.00 | 601 | 1,399 | ❌ S ≤0.76 |
| `analyst15` | 297 | MAT 297 | 280 | 0.50 | 340 | 898 | ❌ S 0.17 |
| `analyst7` | 299 | MAT 299 | 261 | 0.50 | 677 | 3,081 | ❌ S 0.10 |
| `analyst11` | 287 | MAT 287 | 284 | 0.91 | 95 | 147 | ❌ breadth 无信号 |
| `analyst_consensus` | 300 | MAT 3 / VEC 297 | 299 | 0.95 | 42 | 76 | ❌ breadth ≤0.21 |
| `analyst45` | 44 | **VEC 44** | 31 | 1.00 | 147 | 242 | ❌ S 0.36 |
| `analyst39` | 24 | MAT 24 | 2 | 0.92 | 263 | 541 | ❌ S 0.19 |
| `analyst14` | 113 | MAT 113 | 92 | 0.50 | 158 | 267 | ❌ 2Y 负 |
| `analyst9` | 101 | MAT 5 / VEC 96 | 93 | 1.00 | 47 | 76 | ❌ S 0.45 |
| `analyst40` | 16 | MAT 14 / VEC 2 | 16 | 0.36 | 10 | 12 | ❌ TO 爆炸 1.5–1.6 |
| `analyst_base_ref` | 17 | MAT 7 / VEC 10 | 17 | 0.98 | 5 | 6 | ❌ 2Y −0.58 |
| `analyst81` | 5 | MAT 5 | 5 | 0.25 | 5 | 5 | 跳过（cov 0.25） |
| `model52` | 3 | MAT 3 | 3 | 0.20 | 1 | 2 | 跳过（cov 0.20） |

**关键字段族**：`analyst_factor_signals` 的 `*_revision_magnitude` / `*_estimate_coeff_var`（分歧度）/
`*_4wk_chg`（修正变化）/ `*_numest`（广度）——**唯一命中的原语组合**。

### 2.2 Sentiment（5 个）

| 数据集 | 字段 | 类型分布 | 零竞争 | 最大覆盖 | 平台用户 | **alphaCount** | 判定 |
|---|---:|---|---:|---:|---:|---:|---|
| ⚠**`sentiment27`** | 30 | **VEC 30** | 12 | 1.00 | 402 | 1,153 | ⚠ **S 1.33（近线）** |
| `sentiment7` | 24 | VEC 24 | 16 | 0.50 | 49 | 65 | ❌ S 0.43（Wikipedia 浏览量） |
| `other553` | 66 | MAT 33 / VEC 33 | 47 | 0.97 | 171 | 318 | ❌ ≈0（财报电话文本） |
| `sentiment26` | 17 | VEC 17 | 0 | 1.00 | 236 | 461 | ❌ 与 27 同源、竞争高 |
| `sentiment21` | 200 | MAT 200 | 127 | 1.00 | 315 | 681 | 跳过（全 MATRIX + 高竞争） |

**命中的字段**：`snl27_skewness`（域名排名偏度）、`snl27_relpopularity1/08`、`snl27_totaldomains`、
`snl27_totalcountrydomains` —— **双对比 `(A÷td)×(B÷tcd)` @ sector** 是本类别最优结构。

### 2.3 其余 5 类别（12 个）

| 类别 | 数据集 | 字段 | 类型分布 | 零竞争 | 最大覆盖 | 平台用户 | alphaCount | 判定 |
|---|---|---:|---|---:|---:|---:|---:|---|
| Insiders | `insiders1` | 9 | VEC 9 | 0 | 0.55 | 190 | 393 | ❌ TO 爆炸 1.5–1.6 |
| Insiders | `insider_agg_matrix` | 34 | MAT 34 | 14 | 0.61 | 72 | 149 | ❌ TO 爆炸 1.43 |
| Insiders | `insiders12` | 8 | VEC 8 | 3 | 0.26 | 113 | 201 | 跳过（cov 0.26） |
| Institutions | `fund_holdings_panel` | 30 | **VEC 30** | 28 | 0.92 | 19 | 34 | ❌ returns 2.33% |
| Institutions | `institutions6` | 11 | MAT 11 | 1 | 1.00 | 43 | 90 | ❌ 全 MATRIX |
| Macro | `macro27` | 33 | VEC 33 | 20 | 0.43 | 190 | 472 | ❌ returns 2.27% |
| Macro | `macro10` | 1 | MAT 1 | 0 | 1.00 | 73 | 121 | ❌ 2Y −1.56 |
| Earnings | `earnings6` | 55 | VEC 55 | 5 | 1.00 | 576 | 1,617 | ❌ 字段全 NaN |
| Earnings | `earnings_sent_matrix` | 7 | MAT 7 | 1 | 0.51 | 44 | 59 | ❌ TO 爆炸 1.61 |
| Social Media | `socialmedia15` | 45 | **VEC 45** | 32 | 0.37 | 67 | 122 | ❌ TO 爆炸 1.23–1.33 |
| Social Media | `socialmedia12` | 4 | MAT 2 / VEC 2 | 0 | 0.85 | 361 | 1,072 | 跳过（竞争高） |
| Imbalance | `imbalance5` | 2 | MAT 2 | 0 | 0.55 | 914 | 2,841 | ❌ 2Y ≈0 + returns 2.66% |

---

## 三、★ 从画像中读出的四条规律

### 规律 1：**alphaCount 是最强的负向指标**

| 数据集 | alphaCount | 结果 |
|---|---:|---|
| ★`analyst_factor_signals` | **58** | ★ **胜出** |
| `sentiment27` | 1,153 | ⚠ 近线（S 1.33） |
| `analyst7` / `analyst4` | 3,081 / 3,031 | ❌ |
| `imbalance5` | 2,841 | ❌ |
| `analyst69` | **14,111** | ❌ |

**⇒ 平台 alphaCount（该数据集被全平台挖掘的次数）越高，剩余空间越小。**
胜出数据集的 alphaCount 仅 58，而失败的普遍在数千至上万。

> ⚠ 注意与「字段级 userCount」区分：`analyst69` 虽有很多 `userCount ≤ 3` 的字段（说明**这些具体字段**少人用），
> 但**数据集整体**已被挖 1.4 万次 ⇒ 信号空间已被占领。

### 规律 2：字段类型不是判据，**更新频率**才是

| 类型 | 覆盖 | 结果 |
|---|---|---|
| MATRIX（年度/季度财报，低频） | 2,233 | 多数 TO 崩或 returns 不足 |
| **MATRIX（分析师修正，日频）** | — | ★ **胜出**（`analyst_factor_signals`） |
| VECTOR（稀疏事件，如内部人交易/情绪评分） | 830 | **TO 爆炸**（`vec_avg` 归约后个股间跳变） |
| VECTOR（稠密日频，如 sentiment27 域名指标） | — | ⚠ 近线（S 1.33） |

**⇒ 判据应表述为「信号的动态特征」**：稠密 + 日频 = 可用；稀疏事件型 = TO 爆炸；低频 = returns 不足。

### 规律 3：零竞争字段 ≠ 有信号

2,235 个字段（73%）零竞争，但只有 1 个数据集产出可提交 alpha。
**⇒ 零竞争只说明「别人不用」，不说明「有预测力」**（`analyst69` 有 115 个零竞争字段却全军覆没）。

### 规律 4：高覆盖 ≠ 可用

覆盖 1.00 的数据集里，`analyst45`(0.36)、`analyst69`(结构矛盾)、`sentiment26`(竞争高)、
`earnings6`(空信号)、`imbalance5`(2Y≈0)、`sentiment21`(全 MATRIX) 全部失败。
**⇒ 覆盖率只是必要条件（≥0.35），不是充分条件。**

---

## 四、可提交产出（唯一）

```python
signed_power(group_rank(divide(eps_revision_magnitude,
                                ts_mean(eps_y1_estimate_coeff_var, 55)), industry), 3.0)
```
| 项 | 值 |
|---|---|
| **alpha id** | `786pLKnb` |
| 数据集 | `analyst_factor_signals`（alphaCount **58**，全表最低之一） |
| 算子数 | **4** |
| S / F / TO | 1.71 / 1.09 / 0.1124 |
| 2Y / margin | 1.78 / 9.02bp |
| PROD / SELF | **0.6171 / 0.1752** |
| verdict | **FAIL 0**（唯一 WARNING 为信息性 MATCHES_THEMES） |

**近线候选**：`sentiment27`（S 1.29 / F 0.87 / 2Y 1.61 / returns 5.68%）—— 唯一瓶颈是 S 距 1.58 差 0.25。

---

## 五、选集的四条硬筛（由本画像导出，建议前置执行）

```
1. 全量枚举该类别数据集（/data-sets?category=X，不带 limit）
2. 记录 alphaCount —— 优先测 alphaCount 低的数据集（< 200 为佳）
3. 每个数据集 1-8 条探针，反算 returns = max(TO, 0.125) × (F/S)²
4. 四条硬筛（任一不过即弃）：
   · returns ≥ 5%（否则 F 闸数学上不可过）
   · TO ∈ [0.05, 0.3]（<0.05 触发 LOW_TURNOVER；>0.3 逼近上限）
   · 2Y 非负且 ≥ 0.5（recency 结构性保障）
   · |S| ≥ 0.5（否则无信号）
```

---

## 六、Analyst 字段级覆盖度（用户质询后补测）

### 6.1 全量清点

| 项 | 数量 | 占比 |
|---|---:|---:|
| Analyst 字段总数 | **2,469** | 100% |
| 元数据（id/flag/code/时间戳/货币） | 315 | 13% |
| **值类字段** | **2,154** | **87%** |
| 值类中「低竞争(user≤3) 且 cov≥0.5」 | **1,473** | 60% |
| **本战役实际引用过的字段** | **≈100** | **≈4%** |

### 6.2 值类语义家族分布

| 家族 | 字段数 | 已测数据集数 | 结果 |
|---|---:|---:|---|
| `level`（共识/实际水平） | 942 | 6 | 部分有信号（`eps_y1_consensus_value`），但不够 |
| `other`（未归类） | 540 | — | — |
| `revision`（修正变化） | 276 | 4 | ★ **唯一命中族**（`eps_revision_magnitude`） |
| `dispersion`（分歧度） | 262 | 3 | ★ 作为**分母**命中（`eps_y1_estimate_coeff_var`） |
| `breadth`（覆盖广度） | 116 | 3 | ❌ 全部无信号 |
| `growth`（CAGR/趋势） | 18 | 1 | ❌ |

### 6.3 最大盲区（本次补测）

| 数据集 | 低竞争&cov≥0.5 值类字段 | 本次补测 | 结果 |
|---|---:|---|---|
| `analyst11` | **263**（此前 **0** 使用） | E/G Score、`cit*regsubsecrnk` 排名、44 个 ESG/治理 score | ❌ 全灭（S ≤ −0.11） |
| `analyst7` | **261** | **`act_q_*_surprisemean/std/num`**（盈余惊喜族 —— 胜出配方的直接同构） | ❌ 全灭（**TO 0.009–0.029 过低**，季度数据） |
| `analyst15` | 280 | 多窗修正变化（上轮已测） | ❌ |
| `analyst10` | 135（此前 0 使用） | 多为 anntime/analyst-ID/estage **元数据** | 判定不可用 |

### 6.4 字段级覆盖度的结论

| 层级 | 覆盖率 | 状态 |
|---|---|---|
| **数据集级** | **33 / 33 = 100%** | ✅ 完成 |
| **语义家族级** | **6 / 6 = 100%** | ✅ 每族已在 ≥1 个数据集上测过 |
| **数据集 × 家族组合** | ≈35 / 96 ≈ **36%** | ⚠ 部分 |
| **单字段级** | ≈100 / 2,469 ≈ **4%** | ❌ 未完成 |

**★ 关键判断**：本战役的失败**不是字段选择问题，而是结构性的** ——
- `analyst7` 的 surprise÷surprise-std（配方同构）失败原因是**季度数据 ⇒ TO 0.029**（与字段无关）
- `analyst11` 的评分族失败原因是**评分本身无预测力**（与字段无关）
- 其余数据集失败于 returns < 5% / TO 越界 / 2Y 负（均为**数据集级属性**）

**⇒ 继续做单字段级穷举（剩余 96%）的边际收益低**：同一数据集内的同族字段（如 `act_q_{bps,cps,cpx,dsh,dps,ebi,ebs,ebt}_surprisemean`）共享同一动态特性，
TO / returns / 2Y 的判死结论会同向复现（本次 8 条探针已验证该同族性）。

**⇒ 真正未被排除的方向是「跨数据集的字段组合」与「新语义家族」**，而非单数据集内的字段穷举。
