# DEU 字段画像 · 全面分析总结

> **一句话**：把 DEU 的 **22494 个字段**逐个判定为 9 类，使「筛字段」从"每字段一条回测"变成"一条 SQL"。
> 数据源：`data/wqb.db::field_profile_deu` ｜ 工具：`tools/fields/field_profile_deu.py`

---

# 一 一页速览

| 指标 | 值 |
|---|---|
| 字段总数 | **22494** |
| 数据集数 | **178** |
| 已测字段（`n_tests>0`） | **392** |
| 有单信号记录的字段 | **386** |
| 本地 DEU 回测行 | **1930**（其中 348 条由本轮从平台回填） |
| **真正过线（ALIVE）** | **1** |
| 接近（WEAK） | 26 |
| 已判死（DEAD 各型） | **365** |
| 结构性不可用（UNUSABLE） | **17460** |

**⇒ DEU 的可用面已被压缩到：1 颗过线 + 26 个接近 + 3252 个待探。**

---

# 二 画像是什么

## 2.1 表结构

| 列 | 含义 |
|---|---|
| `region` / `dataset` / `category` / `field` | 定位 |
| `ftype` | MATRIX / VECTOR / GROUP / SYMBOL |
| `coverage` | 覆盖率（0~1） |
| `family` | 命名族（去数字与期限后缀） |
| `n_tests` / `n_sg` | 总测试次数 / **单信号记录数** |
| `to_med` / `to_min` / `to_max` | 换手中位数 / 最小 / 最大 |
| `best_s` / `best_2y` / `best_sub` / `best_f` | 全部记录的最好值 |
| **`best_s_sg` / `best_2y_sg` / `best_sub_sg`** | **单信号记录**的最好值（已剔多腿污染） |
| `best_2y_when_s_hi` | S 最高那条的 2Y（诊断「2Y有S无」） |
| **`verdict`** | **9 类判定** |

## 2.2 九类 verdict 与判据

| verdict | 判据 | 含义 | 依据 |
|---|---|---|---|
| **`UNUSABLE`** | `coverage < 0.6` | 覆盖率太低，**永久剔除** | — |
| **`AXIS_ONLY`** | `ftype == GROUP` | 只能作 `group_neutralize` 的轴 | — |
| **`UNTESTED`** | `n_tests == 0` 且通过上面两关 | **真正待探** | — |
| **`ALIVE`** | 单信号 S ≥ **1.58** | **过闸线** | 平台 RA 阈值 |
| **`WEAK`** | 单信号 S ≥ **1.10** | 有信号但不够强 | — |
| `DEAD` | 已测但 S < 1.10 | 无信号 | — |
| **`DEAD_STATIC`** | `to_med < 0.03` | **静态属性，任何骨架都无用** | 11→30 字段实证 |
| **`DEAD_TURNOVER`** | `to_med > 0.70` | **被 `HIGH_TURNOVER` 闸直接拒** | 19 字段实证 |
| **`DEAD_COUNT`** | 名字含 `num/count` 且 2Y≥1.3 且 S≤0.7 | **「2Y 有 S 无」判死形态** | 4/4 命中 |

## 2.3 怎么建（可复现）

```bash
# ① 从平台回填（破解了列表接口的嵌套结构）
python tools/data-repair/backfill_deu_from_platform.py --region DEU --stage IS
# ② 建画像
python tools/fields/field_profile_deu.py --build --region DEU
# ③ 查询
python tools/fields/field_profile_deu.py --query --region DEU --verdict WEAK
```

**★ 回填的关键（`/users/self/alphas` 列表接口）**：
```
alpha["regular"]["code"]       ← 表达式（顶层无 code）
alpha["is"]                    ← IS 指标
alpha["is"]["checks"]          ← 是 list；2Y/sub 要从 checks[].value 取
alpha["classifications"]       ← 平台官方合规标记（DATA_USAGE:SINGLE_DATA_SET）
```

---

# 三 DEU 全景

## 3.1 verdict 分布

| verdict | 数量 | 占比 |
|---|---:|---:|
| **`UNUSABLE`** | **17460** | **77.6%** |
| **`UNTESTED`** | **3252** | **14.5%** |
| **`AXIS_ONLY`** | **1390** | **6.2%** |
| `DEAD` | 312 | 1.39% |
| `DEAD_STATIC` | 30 | 0.13% |
| **`WEAK`** | **26** | 0.12% |
| `DEAD_TURNOVER` | 19 | 0.08% |
| `DEAD_COUNT` | 4 | 0.02% |
| **`ALIVE`** | **1** | **0.004%** |

**★★ 77.6% 的字段是"结构性不可用"（cov<0.6）—— 这是最重要的一条：近 8 成字段从来就不该被考虑。**

## 3.2 category × verdict 交叉表

| category | ALIVE | WEAK | DEAD | DEAD_TURN | DEAD_STAT | DEAD_COUNT | UNTESTED | UNUSABLE | 合计 |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| **MODEL** | 0 | **15** | 101 | 6 | 1 | 0 | 1552 | 6498 | 8173 |
| **ANALYST** | **1** | 5 | 81 | 5 | **11** | **4** | 550 | 3655 | 4312 |
| **OTHER** | 0 | 6 | 41 | 1 | 1 | 0 | 366 | 3506 | 3921 |
| **PV** | 0 | 0 | 23 | 0 | 0 | 0 | 527 | 2093 | 2877 |
| **FUNDAMENTAL** | 0 | 0 | 11 | 0 | 3 | 0 | 36 | 2096 | 2146 |
| NEWS | 0 | 0 | 4 | **6** | 0 | 0 | 202 | 311 | 523 |
| SENTIMENT | 0 | 0 | 0 | 0 | 0 | 0 | 21 | 255 | 276 |
| INSTITUTIONS | 0 | 0 | 8 | 1 | 1 | 0 | 19 | 37 | 66 |
| 其余 8 个 category | 0 | 0 | — | — | — | — | ~50 | ~165 | — |

### 三条 category 级结论

1. **MODEL 是唯一"有厚度"的**：15 WEAK（占全部 WEAK 的 **58%**）。
2. **ANALYST 的失败高度集中**：`DEAD_STATIC` 11 个（**其中 7 个是 `anl93_*`**）+ `DEAD_COUNT` 4 个（**全在 `analyst7` 计数类**）+ 唯一的 ALIVE。
3. **★ NEWS 的换手爆表率全场最高**（6/523 = **1.1%**，全场仅 0.08%）⇒ **新闻类字段的更新频率与 DEU 换手约束结构性冲突**。

---

# 四 五个关键名单

## 4.1 ✅ ALIVE（1 个）

| dataset | field | 类型 | cov | n_sg | to_med | **S_sg** | **2Y_sg** | sub |
|---|---|---|---:|---:|---:|---:|---:|---:|
| `analyst_factor_signals` | **`eps_y1_estimate_change_3mo`** | MATRIX | 0.92 | **60** | 0.0989 | **1.66** | **2.14** | 0.98 |

**全 DEU 22494 个字段中唯一一个「单信号形态下 S 与 2Y 同时过线」的字段。**

## 4.2 WEAK（26 个，前 12 按 S 排）

| dataset | field | 类型 | S_sg | 2Y_sg | sub |
|---|---|---|---:|---:|---:|
| predictive_starmine | `mean_estimate_change_pct_f12m_earnings_14d_4` | MATRIX | **1.57** | 1.44 | 0.97 |
| model216 | `mdl216_armpreferredrevisionscore` | VECTOR | **1.45** | 1.04 | 0.58 |
| predictive_starmine | `mean_estimate_change_pct_f12m_ebitda_14d_4` | MATRIX | **1.41** | 1.22 | **1.20** |
| model238 | `mdl238_industry_rank` | MATRIX | 1.33 | 1.18 | 0.54 |
| model250 | `mdl250_malta_eq_score` | MATRIX | 1.33 | 0.05 | 0.82 |
| analyst_factor_signals | `netprofit_y1_estimate_change_3mo` | MATRIX | 1.32 | 1.21 | **1.00** |
| analyst93 | `anl93_recprofitabilityprev_analyst_profitability2` | VECTOR | 1.30 | 1.17 | 0.84 |
| analyst_factor_signals | `eps_y2_estimate_coeff_var` | MATRIX | 1.23 | **1.49** | 0.84 |
| model216 | `mdl216_preferredblendedrevisionfy2percent` | VECTOR | 1.27 | 0.45 | 0.19 |
| model238 | `mdl238_global_rank` / `global_screening_rank` | MATRIX | 1.18 | 0.85 / 0.88 | — |
| model25 | `mdl25_eq_v4_2_1_v6` / `_v22` | MATRIX | 1.18 | 0.31 | — |
| （另 14 个，含 `dl_riskfree_returns` 分位数标签 ×8 —— **不是信号**） | | | | | |

**★ 类型构成**：MATRIX **22** + VECTOR **5** ⇒ **WEAK 池以 MATRIX 为主**。

## 4.3 ✅ DEAD_COUNT（4 个）—— 判死规则**精准命中 4/4**

| field | n_sg | to_med | **S_sg** | **2Y_sg** |
|---|---:|---:|---:|---:|
| `rec_lowerednum_4wks` | 13 | 0.046 | **0.01** | **1.90** |
| `est_q_net_num_28d` | 1 | 0.069 | 0.65 | **1.59** |
| `est_12m_tbv_raisednum_1mth` | 4 | 0.088 | 0.24 | **1.52** |
| `est_12m_sal_num` | 2 | 0.067 | 0.66 | **1.47** |

**全部是"分析师数量"类计数字段** ⇒ 教科书级「2Y 有、S 无」。**无假阳性。**

## 4.4 DEAD_STATIC（30 个）—— ★ **其中 7 个是 `anl93_*`**

**换手全部 < 0.03**，代表性样本：
```
aggregate_share_count_institutions    0.0146   ← 机构家数
count_institutional_holders_security  0.0151
count_institutional_sellers_security  0.0165
act_q_ebi_surprisemean                0.0184
count_institutional_buyers_security   0.0204
anl93_analyst_accuracy2               0.0237
anl93_analyst_correct_revision_ratio  0.0286
mdl28_..._industry_rank / _global_rank 0.0277 / 0.0245
star_sr_profitability_d1              0.0229
```
**⇒ 「机构家数 / 信用排名 / 信用分 / 分析师技能」这一整类字段都是静态结构属性，不是时变信号。**

## 4.5 DEAD_TURNOVER（19 个，换手 >0.7）

| category | 数量 |
|---|---:|
| **news** | **6** |
| model | 6（`mdl106_*`） |
| analyst | 5（`anl44_2_*` / `anl9_*`） |
| other / institutions | 1 / 1 |

---

# 五 从画像得出的六条结构性结论

### ① 77.6% 的字段结构性不可用

`UNUSABLE 17460` —— 覆盖率 <0.6。**这是最大的一条：近 8 成字段从来就不该被考虑。**

### ② 全 DEU 只有 1 个字段真正过线

`eps_y1_estimate_change_3mo`。**且它属于「已标准化的预期变化率」这一唯一有效机制。**

### ③ 换手是最强的"前置筛子"（30 + 19 = 49 个字段）

- `to_med < 0.03` ⇒ 静态属性（**30 个**）—— 任何骨架都无用
- `to_med > 0.70` ⇒ 被换手闸直接拒（**19 个**）

**⇒ 换手分布**：342 个已测字段，中位 **0.1178**；偏离这个区间两端的都要警惕。

### ④ VECTOR 池的类型决定处理方式

未测池里 VECTOR 占多数（`model216` 全 VECTOR、`news` 大量 VECTOR、`shortinterest3`/`risk60` 全 VECTOR）
⇒ **必须先 `vec_*` 聚合**，且**聚合算子是搜索维度**（实测 `vec_max` 0.43 > `vec_avg` 0.35）。

### ⑤ 5 个全新机制族**全部否证**

| 族 | 最好 S | 死因 |
|---|---:|---|
| 机构资金流（`institutions6`） | 0.82 | **换手 0.014~0.020（静态）** |
| 信用/违约风险（`model28/36`） | **1.08** | 核心字段换手 0.022~0.028（静态） |
| 违约概率期限结构（`model53`） | **0.31** | 期限斜率假设不成立 |
| ARM216（VECTOR） | 0.93 | 我的框架不如历史框架（1.45） |
| 借券/拥挤（`shortinterest3`/`risk60`） | **全负** | 甚至反向 |

### ⑥ NEWS 的换手爆表率是结构性的

6/523 = 1.1%（全场 0.08%）⇒ **新闻类字段的更新频率与 DEU 的换手约束冲突**。

---

# 六 怎么用画像（可执行流程）

## 6.1 ★ 发批前的零成本前置检查（三步）

```bash
# ① 看该 category 的待探字段（含换手！）
python tools/fields/field_profile_deu.py --query --region DEU --verdict UNTESTED --limit 40
#    看 to_med 列 —— 已测字段若 <0.03 直接跳过（静态属性）
# ② 校验字段名与类型（零成本，避免整批 CANCELLED）
#    MCP: preflight_expressions(alpha_expressions=[...], region, universe, delay)
# ③ 检查算子元数
#    wqb.expression.op_arity.ensure_safe_for_dispatch(exprs)
```

**★ 这三步都是零成本的，我在实践中至少各踩过一次坑才固化下来。**

## 6.2 处理待探字段的 4 步过滤

| 步 | 操作 | 剔除 | 剩余 |
|---|---|---:|---:|
| ① | 原始 UNTESTED（升级前口径） | — | 22146 |
| ② | 剔 `coverage<0.6` → `UNUSABLE` | −17460 | 4686 |
| ③ | 剔 `GROUP` → `AXIS_ONLY` | −1390 | **3252** |
| ④ | 再剔已判死数据集（`pattern_scores`/`model26`/`model264`/`other455` 嵌入/`dl_riskfree` 标签） | ~−1500 | **≈1700** |

**⇒ 22146 → 3252（工具自动）→ ≈1700，压掉 92%。**

## 6.3 ★ 但 1700 仍不可全扫（1700/10 = 170 批）⇒ 按机制族圈优先级

**首选顺序**（已部分验证）：
1. **26 个 WEAK 池**（尤其 `netprofit_y1_estimate_change_3mo`：与 ALIVE 同族、**sub 1.00**、但只有 2 条样本）
2. `predictive_starmine` 的 536 未测（唯一产出过 alpha 的数据集）
3. `analyst7` 的 395（**但需剔除计数类**）
4. `model25` 的 100

---

# 七 产物清单

| 产物 | 路径 | 用途 |
|---|---|---|
| **画像工具** | `tools/fields/field_profile_deu.py` | `--build` / `--query`（9 类 verdict） |
| **平台回填** | `tools/data-repair/backfill_deu_from_platform.py` | 平台 alpha → 本地 `backtest_results` |
| **特征→骨架框架** | `docs/reference/field_characteristic_to_mechanism.md` | 8 特征维度 → 11 机制骨架（依据分级 A/B/C/D） |
| **机制×字段搭配** | `docs/reference/mechanism_field_pairing.md` | 机制总表 + 字段分类 + 轴层数判据 |
| **逐数据集分析** | `output_report/DEU_dataset_by_dataset_analysis_20261007.md` | 178 数据集分 4 类 |
| **字段集总账** | `output_report/DEU_fieldset_by_category_20261007.md` | 10 category × 71 字段集 |
| **换手体检** | `output_report/DEU_turnover_healthcheck_20261007.md` | 换手边界判据 |
| **本总结** | `output_report/DEU_field_profile_summary_20261008.md` | ← 你正在看 |

---

# 八 局限与保留口径（必须知道）

| 局限 | 说明 |
|---|---|
| **`UNTESTED` ≠ "从未测过"** | 只覆盖"平台上仍存在的 IS alpha"（348 条）。"测过但 alpha 被删/未持久化/字段提取失败"都会误判为 UNTESTED |
| **回填只做了 `DEU / stage=IS`** | OS stage、其他区未做 |
| **平台分页边界** | 只扫到 `offset≈1100`（HTTP 400 停止），可能有遗漏 |
| **`field_of()` 提取** | 取表达式里首个非算子长 token；若字段名不是首个 token 会归错 |
| **画像不判断"机制对不对"** | 它只说"这个字段有没有信号"，不说"配什么机制最好" ⇒ 仍需配合 `field_characteristic_to_mechanism.md` |

---

# 九 一句话总结

> **DEU 的可用面已经画清楚了：22494 个字段 → 1 个过线 + 26 个接近 + 3252 个待探 + 365 个判死 + 17460 个结构性不可用。**
>
> **唯一有效的机制是「已标准化的预期变化率」，唯一有效的框架是「双窗 1/210 + 单桶轴」。**
> **画像的价值不在于"多测了几批"，而在于把"该不该测这个字段"从回测降级成一条 SQL。**
>
> **★ 而它最实用的一列是 `to_med`（换手）—— `<0.03` 或 `>0.70` 的字段，连测都不用测。**
