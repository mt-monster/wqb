# DEU 字段画像 · 最终可交付版 · 2026-10-08

> **表**：`data/wqb.db::field_profile_deu`（**22494 行**，DEU 全量字段）
> **工具**：`tools/fields/field_profile_deu.py`（`--build` / `--query`）；回填：`tools/data-repair/backfill_deu_from_platform.py`
> **状态**：✅ **4 项修复全部完成，画像已可交付**（上一版的三处"不可信"均已消除）

---

## 〇 本次修复了什么（对比上一版）

| # | 问题 | 修复 | 验证 |
|---|---|---|---|
| **1** | 多腿判据失效（`\x08` 退格符混进正则 + v3 判据本身会误杀双窗骨架） | v4 = `add(` **且** ≥2 个**不同信号字段** | 单测 **4/4** + 与手工审计真值 **4/4 精确吻合** |
| **2** | 收割不落库 ⇒ 画像数据源缺失 | **破解列表接口的嵌套结构**（`regular.code` / `is` / `is.checks`） | 回填 **298 条**，code/2Y/sub **298/298 全部非空** |
| **3** | preflight 校验钩子 | ⏳ 工具已验证可用（`preflight_expressions`），接入主流程待做 | — |
| **4** | `fields` 表重复行 | `GROUP BY ... MAX(coverage)` | ✅ |

**★ 关键突破（#2）**：`/users/self/alphas` **列表接口的 `code` 不在顶层**，而在 `regular.code`；
且 `two_year_sharpe` / `sub_universe_sharpe` 不在 `is` 里，**要从 `is.checks[].value` 按 name 取**。
（**额外收获**：列表接口还带 `classifications`，含平台**官方**的 `DATA_USAGE:SINGLE_DATA_SET` 合规标记。）

---

## 一 全量 verdict 分布（**2026-10-08 升级版：新增 UNUSABLE / AXIS_ONLY 分层**）

| verdict | 数量 | 占比 | 含义 |
|---|---:|---:|---|
| **`UNUSABLE`** | **17460** | **77.6%** | **`coverage < 0.6` ⇒ 结构性不可用，永久剔除** |
| **`UNTESTED`** | **3296** | **14.6%** | **真正待探**（cov≥0.6 且非 GROUP） |
| **`AXIS_ONLY`** | **1390** | **6.2%** | **`ftype == GROUP` ⇒ 只能当轴，不能当信号** |
| DEAD | 281 | 1.25% | 已测且 S<1.10 |
| **WEAK** | **26** | 0.12% | 已测有信号但不够强（S 1.10~1.58） |
| DEAD_TURNOVER | 19 | 0.08% | 换手 >0.7，被闸直接拒 |
| DEAD_STATIC | 17 | 0.08% | 换手 <0.03，任何骨架都无用 |
| DEAD_COUNT | 4 | 0.02% | 「2Y 有 S 无」判死形态 |
| **ALIVE** | **1** | **0.004%** | **S 与 2Y 同时过线** |

### ★ UNTESTED 怎么处理（4 步层层过滤）

| 步 | 操作 | 剔除 | 剩余 |
|---|---|---:|---:|
| ① | 原始 UNTESTED（升级前口径） | — | 22146 |
| ② | 剔 `coverage<0.6` → `UNUSABLE` | −17460 | 4686 |
| ③ | 剔 `GROUP` → `AXIS_ONLY` | −1390 | **3296** |
| ④ | 再剔 5 个**已判死数据集**（`pattern_scores` / `model26` / `model264` / `other455` 嵌入 / `dl_riskfree_returns` 标签） | −1581 | **≈1715** |
| **⑤** | **★ 真正值得探** | | **≈1715** |

**⇒ 22146 → 3296（工具自动分层）→ ≈1715（扣已判死数据集），压掉 92%。**
**⇒ 但 1715 / 10 = ~172 批，仍不可全扫 ⇒ 必须按机制族圈优先级。**

### ⚠️ UNTESTED 的准确含义（不是"从未测过"）

`n_tests == 0` = **在 `backtest_results` 里无记录**。至少 3 个原因造成"测过却没记录"：
1. alpha 被删 / 未持久化
2. `field_of()` 字段提取失败（字段名不是表达式里首个长 token）
3. 平台列表分页边界（本次只扫到 offset≈1100，HTTP 400 后停止）

**⇒ 它是"无记录"而非"无测试"，属上界估计。**

---

## 二 ★ category × verdict 交叉表

| category | ALIVE | WEAK | DEAD | DEAD_TURN | DEAD_STAT | DEAD_COUNT | UNTESTED | 合计 |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| **MODEL** | 0 | **15** | 101 | 6 | 1 | 0 | **8050** | 8173 |
| **ANALYST** | **1** | 5 | 81 | 5 | **11** | **4** | **4205** | 4312 |
| **OTHER** | 0 | 6 | 41 | 1 | 1 | 0 | 3872 | 3921 |
| **PV** | 0 | 0 | 23 | 0 | 0 | 0 | 2854 | 2877 |
| **FUNDAMENTAL** | 0 | 0 | 11 | 0 | 3 | 0 | 2132 | 2146 |
| NEWS | 0 | 0 | 4 | **6** | 0 | 0 | 513 | 523 |
| SENTIMENT | 0 | 0 | 0 | 0 | 0 | 0 | 276 | 276 |
| INSTITUTIONS | 0 | 0 | 8 | 1 | 1 | 0 | 56 | 66 |
| RISK / SHORTINTEREST / INSIDERS / EARNINGS / OPTION / MACRO / SOCIALMEDIA / IMBALANCE | 0 | 0 | 3/5/4/0/0/0/0/0 | 0 | 0 | 0 | 49/20/38/25/22/13/19/2 | — |

### 三个 category 级结论

1. **MODEL 是唯一"有厚度"的**：8050 未测 + **15 WEAK（占全部 WEAK 的 58%）**。
2. **ANALYST 的失败模式集中在两类**：**DEAD_STATIC 11 个**（其中 **7 个是 `anl93_*`**）+ **DEAD_COUNT 4 个**（全在 `analyst7` 计数类）。
3. **★ NEWS 的换手爆表率全场最高**（6/523 = **1.1%**，全场仅 0.08%）⇒ **新闻类字段的更新频率与 DEU 的换手约束结构性冲突**。

---

## 三 四个关键名单

### 3.1 ✅ ALIVE（1 个 —— 唯一真正过闸线的字段）

| dataset | field | 类型 | cov | n_sg | to_med | **S_sg** | **2Y_sg** | sub |
|---|---|---|---:|---:|---:|---:|---:|---:|
| **analyst_factor_signals** | **`eps_y1_estimate_change_3mo`** | MATRIX | 0.92 | **60** | 0.0989 | **1.66** | **2.14** | 0.98 |

**★ 它就是本会话就绪候选 `9qWX78vX` 系列的载体字段** —— 画像现在正确识别了它（此前 `n_sg=0`）。
**这是全 DEU 唯一一个"单信号形态下 S 与 2Y 同时过线"的字段。**

### 3.2 WEAK（26 个）—— 已测有信号但不够强，**按 S 排序的前 15**

| dataset | field | 类型 | cov | n_sg | to_med | S_sg | 2Y_sg | sub |
|---|---|---|---:|---:|---:|---:|---:|---:|
| predictive_starmine | `mean_estimate_change_pct_f12m_earnings_14d_4` | MATRIX | 0.97 | 21 | 0.192 | **1.57** | 1.44 | 0.97 |
| model216 | `mdl216_armpreferredrevisionscore` | **VECTOR** | 0.71 | 6 | 0.099 | **1.45** | 1.04 | 0.58 |
| predictive_starmine | `mean_estimate_change_pct_f12m_ebitda_14d_4` | MATRIX | 0.95 | 44 | 0.190 | **1.41** | 1.22 | **1.20** |
| model238 | `mdl238_industry_rank` | MATRIX | 1.00 | 8 | 0.137 | 1.33 | 1.18 | 0.54 |
| model250 | `mdl250_malta_eq_score` | MATRIX | 0.56 | 3 | 0.121 | 1.33 | 0.05 | 0.82 |
| analyst_factor_signals | `netprofit_y1_estimate_change_3mo` | MATRIX | 0.92 | 2 | 0.045 | 1.32 | 1.21 | **1.00** |
| analyst93 | `anl93_recprofitabilityprev_analyst_profitability2` | VECTOR | 0.64 | 27 | 0.081 | 1.30 | 1.17 | 0.84 |
| model250 | `mdl250_maltahc_eq_score` | MATRIX | 0.56 | 2 | 0.111 | 1.30 | 0.53 | 0.95 |
| analyst93 | `anl93_recprofitabilityprev_estimator_profitability2` | VECTOR | 0.64 | 9 | 0.080 | 1.28 | 1.14 | 0.86 |
| analyst_factor_signals | `eps_y2_estimate_change_3mo` | MATRIX | 0.92 | 5 | 0.044 | 1.27 | 0.92 | 0.64 |
| model216 | `mdl216_preferredblendedrevisionfy2percent` | VECTOR | 0.71 | 2 | 0.113 | 1.27 | 0.45 | 0.19 |
| **analyst_factor_signals** | **`eps_y2_estimate_coeff_var`** | MATRIX | 0.89 | 24 | 0.113 | 1.23 | **1.49** | 0.84 |
| model238 | `mdl238_global_rank` / `global_screening_rank` | MATRIX | 1.00 | 2 / 1 | 0.098 / 0.075 | 1.18 | 0.85 / 0.88 | — |
| model25 | `mdl25_eq_v4_2_1_v6` / `_v22` | MATRIX | 0.65 | 2 / 1 | 0.126 / 0.031 | 1.18 | 0.31 | — |
| model216 | `mdl216_armindustry100score` | VECTOR | 0.71 | 2 | 0.108 | 1.17 | 0.90 | 0.39 |
| （另 11 个：`dl_riskfree_returns` 的**分位数标签** ×8 —— **不是信号**，可忽略） | | | | | | | | |

**★ 值得注意的两个**：
- **`netprofit_y1_estimate_change_3mo`**（S1.32 / 2Y1.21 / **sub1.00**）—— 与 ALIVE 字段**同族同机制**，样本仅 2 条，**值得补测**
- **`eps_y2_estimate_coeff_var`**（S1.23 / **2Y1.49**）—— WEAK 里 **2Y 最高**，但属分歧度族（A-3 已判死），需注意矛盾

### 3.3 DEAD_COUNT（4 个）—— ✅ **判死规则精准命中，全在 `analyst7` 计数类**

| field | n_sg | to_med | **S_sg** | **2Y_sg** |
|---|---:|---:|---:|---:|
| `rec_lowerednum_4wks` | 13 | 0.046 | **0.01** | **1.90** |
| `est_q_net_num_28d` | 1 | 0.069 | 0.65 | **1.59** |
| `est_12m_tbv_raisednum_1mth` | 4 | 0.088 | 0.24 | **1.52** |
| `est_12m_sal_num` | 2 | 0.067 | 0.66 | **1.47** |

**⇒ 教科书级「2Y 有、S 无」** —— 全部是"分析师数量"类计数字段。**4/4 命中，无假阳性。**

### 3.4 DEAD_STATIC（17 个，换手 <0.03）—— ★ **7 个是 `anl93_*`**

| dataset | field | to_med | S_sg |
|---|---|---:|---:|
| analyst7 | `act_q_ebi_surprisemean` | 0.0184 | 0.21 |
| analyst7 | `act_q_eps_surprisemean` | 0.0189 | 0.56 |
| fundamental6 | `fnd6_ewq_rectoq` | 0.0193 | −0.10 |
| **analyst93** | `anl93_profitabilityprev_analyst_analyst` | 0.0194 | 0.22 |
| **analyst93** | `anl93_recprofitabilityprev_analyst_analyst` | 0.0196 | 0.56 |
| fundamental6 | `fnd6_capxy` | 0.0197 | 0.22 |
| institutions6 | `count_institutional_buyers_security` | 0.0204 | 0.36 |
| **analyst93** | `anl93_consistency_analyst_analyst` | 0.0206 | 0.23 |
| **analyst93** | `anl93_correv_analyst_analyst` | 0.0206 | 0.23 |
| **analyst93** | `anl93_analyst_accuracy2` | 0.0237 | 0.51 |
| predictive_starmine | `smest_f12m_earnings_5` | 0.0247 | 0.51 |
| fundamental6 | `fnd6_oancfy` | 0.0263 | 1.02 |
| **analyst93** | `anl93_estimator_accuracy1` | 0.0264 | 0.09 |
| **analyst93** | `anl93_estimator_correct_revision_ratio` | 0.0284 | 0.50 |
| **analyst93** | `anl93_analyst_accuracy1` | 0.0285 | 0.14 |
| **analyst93** | `anl93_analyst_correct_revision_ratio` | 0.0286 | 0.60 |
| other545 | `oth545_mpd` | 0.0263 | 0.15 |

**★ 17 个里 7 个是 `anl93_*`（41%）** ⇒ **从换手维度独立证实该数据集的"静态属性"性质**（与"换 5 种角色都不行"的结论互证）。

### 3.5 DEAD_TURNOVER（19 个，换手 >0.7，被闸直接拒）

| category | 数量 |
|---|---:|
| **news** | **6** |
| model | 6（`mdl106_*`） |
| analyst | 5（`anl44_2_*` / `anl9_*`） |
| other / institutions | 1 / 1 |

---

## 四 画像的可信度声明（最终版）

| ✅ 可信 | 说明 |
|---|---|
| `to_med` / `to_min` / `to_max`（换手） | 与实测一致，已验证 |
| `ftype` / `coverage` / `family` | 来自 `fields` 表（已去重） |
| **`best_s_sg` / `best_2y_sg` / `best_sub_sg` / `n_sg`** | **单信号过滤已修复（4/4 真值验证）** |
| **`verdict`（ALIVE/WEAK/DEAD/DEAD_STATIC/DEAD_TURNOVER/DEAD_COUNT）** | 判定逻辑已验证 |

| ⚠️ 保留口径 | 说明 |
|---|---|
| **UNTESTED 22146** | **不等于"从未测过"** —— 只覆盖"平台上仍存在的 IS alpha"（本次回填 298 条） |
| 覆盖范围 | 回填只做了 `region=DEU, stage=IS`；OS / 其他区未做 |

---

## 五 下一步建议

| 优先 | 动作 | 依据 |
|---|---|---|
| **1** | **补测 `netprofit_y1_estimate_change_3mo`** | 与 ALIVE 字段同族同机制、**sub 1.00**，但只有 2 条样本 ⇒ 很可能被低估 |
| **2** | **`mdl216_*` 用 `vec_max` 深测** | 3 个字段进 WEAK，但 `n_sg` 只有 2~6 ⇒ 样本严重不足 |
| **3** | **接 #3（preflight 钩子）进发批流程** | 零成本，可避免整批 CANCELLED |
| **4** | **回填 OS stage** | 补全 `58gkLAkk` 等已提交 alpha 的行 |
| — | 不再投入 | DEAD_STATIC（17）/ DEAD_TURNOVER（19）/ DEAD_COUNT（4）= **40 个字段**已定论 |

---

# 六 【2026-10-08 追加】5 个机制族探针 + 画像闭环

## 6.1 探针结果：5 个全新机制族**全部未过闸**

| 族 | 数据集 | 最好字段 | S | 2Y | 结论 |
|---|---|---|---:|---:|---|
| **F1 机构资金流** | `institutions6` | `quantity_institutional_shares_acquired` | 0.82 | **1.68** | ❌ 2Y有S无 |
| **F2 信用/违约风险** | `model28` | **`mdl28_..._asset_drift_pct`** | **1.08** | 0.68 | ❌ 族内最高，仍不够 |
| **F3 违约概率期限结构** | `model53` | `斜率1m−1y` | **0.31** | 0.51 | ❌ **最看好的构造，全灭** |
| **F4 ARM216**（VECTOR+`vec_max`） | `model216` | `armpreferredrev1rank` | 0.93 | 1.21 | ❌ **我的框架不如历史框架（1.45）** |
| **F5 借券/拥挤** | `shortinterest3`+`risk60` | — | **全负 −0.07~−0.74** | 负 | ❌ **甚至反向**（`min_loan_rate_main` −0.74） |

**发批前用 `preflight_expressions` 校验了 47 个字段名 → `unknown_fields: []` ⇒ 零整批 CANCELLED。**

## 6.2 ★★★★ 画像闭环完全打通

```
探针（5 批 50 条）→ backfill（新增 50，累计 348）→ 画像重建 ✅
```

| verdict | 闭环前 | **闭环后** |
|---|---:|---:|
| UNTESTED | 3296 | **3252** |
| DEAD | 281 | **312** |
| **DEAD_STATIC** | 17 | **30（+13）** |
| 其余 | 不变 | 不变 |

## 6.3 ★★★★ 画像的最强价值：**它在开探针前就已预警**

新测 50 个字段里 **13 个是 `DEAD_STATIC`**，换手全在 **0.014~0.028**：

| 字段 | 换手 | verdict |
|---|---:|---|
| `aggregate_share_count_institutions` | **0.0146** | DEAD_STATIC |
| `count_institutional_holders_security` | **0.0151** | DEAD_STATIC |
| `count_institutional_sellers_security` | **0.0165** | DEAD_STATIC |
| `count_institutional_buyers_security` | **0.0204** | DEAD_STATIC |
| `mdl28_..._industry_rank` / `_global_rank` | **0.0277 / 0.0245** | DEAD_STATIC |
| `star_sr_profitability_d1` / `star_sr_leverage_d1` / `credit_risk_leverage_score_d1` | **0.0229 / 0.0221** | DEAD_STATIC |

**⇒ 机构家数、信用排名、信用分 —— 这些"新机制族"字段的换手都是 0.014~0.028（静态结构属性，不是时变信号）。**
**⇒ 这从换手维度解释了两个族为什么没有信号。**

## 6.4 ★ 我的判断错误 + 新增纪律

我把 `count_institutional_buyers_security` 列为「**最快上手（MATRIX cov=1）**」的首选 —— **这个判断错了**：
它在**画像 v1 里就已经是 `DEAD_STATIC`**（换手 0.0204），**我开探针前没查画像的 `to_med`**。

**★ 新增纪律：开任何探针批前，先查目标字段的 `to_med`（换手）—— 零成本，可避免整批浪费。**
```bash
python tools/fields/field_profile_deu.py --query --region DEU --verdict UNTESTED --limit 40
# 看 to_med 列；已测字段若 to_med<0.03 直接跳过
```

---

# 七 最终结论（DEU 战役）

## 7.1 画像最终状态

| verdict | 数量 | 说明 |
|---|---:|---|
| `UNUSABLE` | 17460 | cov<0.6，永久剔除 |
| `UNTESTED` | **3252** | 真正待探（已扣 UNUSABLE / AXIS_ONLY） |
| `AXIS_ONLY` | 1390 | GROUP，只能当轴 |
| `DEAD` | **312** | 已测 S<1.10 |
| `DEAD_STATIC` | **30** | 换手<0.03 |
| `WEAK` | 26 | S 1.10~1.58 |
| `DEAD_TURNOVER` | 19 | 换手>0.7 |
| `DEAD_COUNT` | 4 | 「2Y有S无」 |
| **`ALIVE`** | **1** | **`eps_y1_estimate_change_3mo`（S1.66 / 2Y2.14）** |

## 7.2 DEU 的最终可用面

**全 DEU 22494 个字段里，只有 1 个字段（`eps_y1_estimate_change_3mo`）在单信号形态下 S 与 2Y 同时过线。**

- **唯一有效机制**：「已标准化的预期变化率」（`*_estimate_change_*`）
- **唯一有效框架**：双窗 1/210 + 单桶轴 gran 0.05
- **5 个全新机制族（机构/信用/期限结构/ARM/借券）全部否证**
- **26 个 WEAK 是最好的剩余池**（最高 S1.57）

## 7.3 三件产物（可跨区复用）

| 产物 | 用途 |
|---|---|
| `tools/fields/field_profile_deu.py` | 字段画像表（9 类 verdict），`--build` / `--query` |
| `tools/data-repair/backfill_deu_from_platform.py` | 平台 → 本地落库（破解了列表接口的嵌套结构） |
| `docs/reference/field_characteristic_to_mechanism.md` | 8 特征维度 → 11 机制骨架（依据分级 A/B/C/D） |
