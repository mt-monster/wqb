# USA analyst category 挖掘报告 — 2026-10-03/04

> 指令：在 USA 标准流程内，**优先聚焦 ANALYST category** 持续挖掘可提交 REGULAR alpha。
> 方法：S0 白地测绘（25 个 analyst 数据集 × 三重交集）→ Mode B 逐集深挖（analyst82 / analyst49 / analyst69）→ 结构空间穷举（ratio / 分组轴 / 窗口 / 常数 / 事件时间）。
> 统一设置：USA / TOP3000 / delay 1 / decay 30 / STATISTICAL / truncation 0.08 / nanHandling ON。

---

## 1. 结论（一句话）

**analyst category 的单表达式 S 天花板 ≈ 1.2，低于 1.58 闸线**（缺口约 0.4）。
但其**信息结构天然过 SUB**（ratio / rank / 事件时间类构造全部 SUB PASS，与高 S 族相反）⇒
**analyst 家族的价值在「低相关 + 天然过 SUB」的组合腿属性，而非单信号强度** ⇒ 应走 SuperAlpha 组腿或跨集 Mode B 组合。

> 四集验证的 S 天花板：analyst49 **0.74** < analyst69 **0.98** < analyst82 **1.19** < AFS-divide **1.62**（但 F 缺 0.17）—— 全部 < 1.58 闸。

唯一例外：AFS（analyst_factor_signals）的 `divide` 族达到 S=1.62 且三闸齐过，仅差 F 0.17 ⇒ 见 §2、§4。

---

## 2. AFS（analyst_factor_signals）—— 唯一「三闸齐过」候选

### 2.1 冠军候选 `LLZqw9W9`
```
group_rank(trade_when(rank(ts_backfill(est_revision_magnitude_profit,22)) > 0.5,
  divide(ts_zscore(ts_backfill(est_revision_magnitude_profit,33),126),
         add(ts_zscore(ts_backfill(est_revision_magnitude_eps,33),126), 1.0)), -1), market)
```
| 指标 | 值 | 闸线 | 判定 |
|---|---|---|---|
| Sharpe | **1.62** | ≥1.58 | ✅ |
| Fitness | 0.83 | ≥1.0 | ❌ 差 0.17 |
| SUB_UNIVERSE | **0.77** | ≥0.571×S | ✅ PASS |
| 2Y Sharpe | **2.26** | ≥1.58 | ✅ PASS |

**唯一缺口 = Fitness 0.83（需 1.0）。** 这是全场最接近可提交的 analyst 候选。

### 2.2 ★★ AFS 二律背反（铁律）
| 结构族 | S 天花 | SUB |
|---|---|---|
| `divide(predict, add(eps, C))` | **1.62**（C=1.0） | ✅ PASS |
| `multiply(rank, rank)` | **1.93** | ❌ 全灭 |

**两族交集为空** ⇒ AFS 单表达式无解。

### 2.3 ★★★ 分母常数旋钮（V 批）
`divide` 分母 `add(z, C)` 的常数 **C 从 0.5→1.0** 同时松开三闸：S 1.47→1.62、SUB 0.75→0.77、2Y 1.50→2.26。
机理：常数把分母推离 0（符号翻转敏感区），稳定横截面排序、降低极端值占比。

### 2.4 ★ 第二重二律背反（z 窗）
| z 窗 | S | F | SUB |
|---|---|---|---|
| 66 | 1.69 | 0.87 | ❌ 0.55 |
| **126** | **1.62** | 0.83 | ✅ **0.77** |
| 252 | 1.27 | 0.58 | ❌ 0.25 |

**z 窗=126 恰是 SUB 唯一通过点，同时是 S/F 最低点** ⇒ divide 族内部也救不出 F。

### 2.5 AFS 全部「三闸齐过」候选（均仅差 F）
| 变体 | S | F | SUB | 2Y |
|---|---|---|---|---|
| V1-1 (`LLZqw9W9`) | 1.62 | 0.83 | ✅0.77 | ✅2.26 |
| V4-2 (axis=sector) | 1.60 | 0.81 | ✅0.76 | ✅2.30 |
| V5-1 (arg=0) | 1.63 | 0.83 | ✅0.77 | ✅2.34 |

---

## 3. analyst82 —— 「信号-不确定度比」`predict/madp`（最强构造）

`madp` = 模型预测值的平均绝对偏差（分析师模型分歧度 = 不确定度代理）。
构造 `divide(ts_zscore(predict, W), add(ts_zscore(madp, W), C))`：

| 变体 | 字段 / 窗口 / 轴 | S | F | SUB | 2Y |
|---|---|---|---|---|---|
| **Z4-2** | oprq_q1, z126, **industry** | **1.19** | 0.53 | ✅0.65 | ✅2.92 |
| Z1-1 | oprq_q1, **z252**, market | 1.16 | 0.49 | ✅0.73 | ✅2.55 |
| Z3-1/2 | oprq_q1, z126, C=0.5/2.0 | 1.10 | 0.47 | ✅0.56/0.57 | ✅2.77 |
| W1-4 | oprq_q1, z126, market | 1.10 | 0.47 | ✅0.56 | ✅2.77 |
| Z4-1 | axis=sector | 1.07 | 0.45 | ✅0.52 | ✅2.70 |
| X3-2 | ebtq_q1, z126 | 1.06 | 0.44 | ✅0.46 | ✅2.05 |
| W1-2 | netq_q1, z126 | 0.97 | 0.38 | ✅0.42 | ✅2.09 |
| Z1-2 | oprq_q1, z66 | 0.86 | 0.32 | ❌0.35 | ✅2.58 |
| W1-5 / X1-5 | nety_y1, z126 | 0.76/0.83 | 0.27/0.29 | ✅0.42/0.41 | 1.61/1.46 |

**旋钮排序**：基础量质量（oprq > ebtq > netq > salq > epsq）> 分组轴（industry > market > sector）> z 窗（126 ≈ 252 > 66）> 常数 C（无杠杆）。
**死的**：离散度压缩 `-ts_delta(madp)`（S≈0）、跨期斜率 `Q2-Q1 predict`（S 负）、rank 乘积（S≈0）、去 zscore（S 0.47）。
**结论**：**S 天花板 1.19**，缺口 0.39，**单表达式无法过闸**。

**3.1 放大尝试（P 批，均未突破 1.19）**
| 变体 | 构造 | S | F | SUB | 2Y |
|---|---|---|---|---|---|
| P6-1 | signed_power(ratio, 0.5) | 1.19 | 0.53 | ✅0.65 | ✅2.92 |
| P3-1 | rank(ratio) × rank(momentum) | 1.13 | 0.47 | ❌0.48 | ✅2.49 |
| P2-2 | revision_momentum / madp | 1.03 | 0.42 | ❌0.44 | ✅2.32 |
| P4-1 | ratio z504 | 0.99 | 0.39 | ✅0.59 | ✅2.14 |
| P2-1 | revision_momentum / madp | 0.97 | 0.39 | ✅0.50 | ✅2.28 |

`multiply(rank,rank)` 破 SUB（P3-1）；`signed_power` 对 group_rank 输出无效（P6-1 ≡ Z4-2）。

---

## 4. analyst49（Value Line 数据，极低拥挤 alphaCount 0–10）

| 变体 | 字段 | S | SUB | 2Y |
|---|---|---|---|---|
| A49-1-4 | technicalrank（反转） | 0.74 | ✅0.45 | ❌1.07 |
| A49-3-1 / A49-6-3 | earningspredictabilityindex | 0.70 | ✅0.32 | ✅1.62 |
| A49-2-1 | timelinessrank（zscore） | 0.61 | ✅0.40 | ❌0.88 |
| A49-1-2 | performancerank（反转） | 0.51 | ✅0.41 | ❌1.01 |

全部 **S≤0.74**，但 SUB 天然 PASS。Value Line 自带 rank（1-5，低=好）信息量弱。

---

## 5. AFS `LLZqw9W9` Fitness 救援（H 批，8 变体全灭）

平台 `get_alpha_details(LLZqw9W9)` 实证：**fail = 无**；warning = **LOW_FITNESS 0.83（需 1.0）**；SUB/2Y/SHARPE 全 PASS。pyramid = USA/D1/ANALYST ×1.2。

| 变体 | 改动 | S | F | SUB | 2Y |
|---|---|---|---|---|---|
| F-1（=基线） | — | 1.62 | **0.83** | ✅0.77 | ✅2.26 |
| F-2 | signed_power(·,1.5) | 1.62 | 0.83 | ✅0.77 | ✅2.29 |
| F-5 | 门控 0.5→0.3 | 1.62 | 0.83 | ❌0.50 | ✅1.75 |
| F-8 | axis=industry | 1.58 | 0.79 | ✅0.76 | ✅2.15 |
| F-7 | 分母换 profit | 1.41 | 0.67 | ✅0.66 | ✅1.99 |
| F-6 | 分子 ts_sum | 1.38 | 0.65 | ✅0.66 | ✅1.94 |
| F-3 | 全窗 252 | 1.27 | 0.58 | ❌0.25 | ✅1.88 |
| F-4 | **去 trade_when 门控** | 1.30 | 0.61 | ❌0.44 | ❌1.50 |

**结论**：① **F 锁定 ≤0.83**，任何结构/设置变体都无法提升；② **`trade_when` 门控是必需件**（去掉则 S/F/SUB/2Y 齐崩）；③ 分母换同族 profit 反而降 S ⇒ eps 分母是唯一生产力源；④ turnover 0.0479 远低于 0.125 地板 ⇒ Fitness 被 `Sharpe×sqrt(returns)` 锁死。
⇒ **`LLZqw9W9` 是 AFS 终局产物：3 闸齐过、仅差 F，转 SuperAlpha / 跨集组合。**

---

## 6. analyst69（Fundamental Analyst Estimates，646 字段 / cov 0.93 / ac 12250，白地）

**★ 核心：事件时间信号 `expected_report_dt`（预期财报日期）**
`group_rank(multiply(-1, ts_delta(ts_backfill(<X>_expected_report_dt,22),22)), market)`（X∈{aeps,bps,cps,analyst}，四字段同源 ⇒ 结果逐位相同）：

| 变体 | 字段 | S | F | SUB | 2Y |
|---|---|---|---|---|---|
| **A69-E-1** | 平滑事件时间 `ts_mean(-ts_delta(dt,5),22)` | **0.98** | 0.43 | ✅0.70 | ✅2.13 |
| A69-A-1/2/3/4 | `-ts_delta(expected_report_dt,22)` | 0.91 | 0.41 | ✅**0.78** | ✅2.37 |
| A69-C-1/3 | `dps_new`/`ebit` 变体 EPS 修订 | 0.82 | 0.33 | ✅0.59 | ❌1.15 |
| A69-C-2 | `dps_new` EPS nxt_yr 修订 | 0.66 | 0.24 | ✅0.63 | ❌1.22 |
| A69-B-1/3 | EPS 增长价差 `nxt−cur` | 0.15 | 0.03 | ✅0.58 | ✅1.97 |
| A69-D-1 | 股息 `dvd_sh_last` 修订 | 0.60 | 0.21 | ✅0.29 | ✅1.70 |

**机制**：预期财报日**前移/后移**的时序变化 = 事件公告节奏信号，与估计水平正交；**A69-A 的 SUB 0.78 是全场 analyst 信号最高**。
⇒ **analyst69 单表达式 S 天花板 0.98**（EPS 增长价差、股息估计均弱）。

---

## 7. biasfree_analyst（bias-adjusted forecasts，54 字段）

| 变体 | 字段 | S | SUB |
|---|---|---|---|
| BF-U5-2 | num_upward_fundamental_revisions (z126) | 1.09 | ❌0.29 |
| BF-U3-2 | stddev/mean price target | 1.06 | ❌0.12 |
| BF-U1-2 | ts_delta(median_bias_adjusted_estimate,66) | 0.87 | ❌0.12 |

全 **SUB FAIL**，与 analyst82 ratio 系相反（biasfree 系过不了 SUB）。

---

## 8. analyst category 白地地图（25 个数据集）

- **已测 / 弱**：`analyst82`（S 天花 1.19）、`analyst49`（0.74）、`analyst69`（0.98）、`biasfree_analyst`（SUB 全灭）、`analyst_base_ref`（28 字段）。
- **已判死**：`analyst44`、`analyst_consensus`、`analyst_earnings_ibes`、`analyst_factor_signals`（AFS 除 divide 族）。
- **真白地（未测）**：`model211`（488 字段 / ac 18240，analyst82 拥挤孪生）、`analyst16`（实时估计 / ac 12353）、`analyst83`·`news87`（电话会议文本 / ac 722·2513）、`analyst35`（ESG / ac 544）、`analyst48`（分红估计 / ac 471）、`analyst45`（ac 266）。

---

## 9. 下一步（按价值排序）

1. **救援 `LLZqw9W9`**：三闸齐过仅差 F 0.17 ⇒ 走 brain-alpha-repair / SuperAlpha 组腿 / 设置迁移。
2. **analyst69 深挖**（进行中）：`expected_report_dt`（事件时间，ac≈0）、`best_eeps_nxt_yr−cur_yr`（前瞻增速）、`best_eps_4wk_chg`（修订）、`best_roe`/`best_target_price` 等经典修订/评级信号。
3. **cross-dataset Mode B 组合腿**：analyst82 ratio 系（低 S 高 SUB） × AFS divide 系（高 S）互补。
4. **SuperAlpha**：以天然过 SUB 的 analyst 腿 + 高 S 腿组 SA。

---

## 10. 工程纪律（本轮教训）

- **并发 >7 触发 auth 429**：同时 3 个探针进程（各 conc 4）⇒ 认证撞 429 整批崩。**纪律：最多 2 个探针进程，总 conc ≤ 7**。
- `rank(x,-1)` 非法（只收 1 参）→ 用 `subtract(1, rank(x))`。
- `trade_when(cond,x)` 只给 2 参非法（必须 3 参）→ `trade_when(cond,x,-1)`。
- `tmp_probe_conc.py` 已移至 `attic/tracking_reference_20261004/scripts/`。
- 本地 `wqb.db` 的 `fields` 表对 analyst82/49 无数据 ⇒ **字段以平台 `get_datafields` 为准**（本地 catalog ≠ 平台）。
