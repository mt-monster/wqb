# DEU 全字段画像 + 分析 · 2026-10-07

> **表**：`data/wqb.db::field_profile_deu`（**22494 行**，DEU 全量字段）
> **工具**：`tools/fields/field_profile_deu.py`（`--build` / `--query`）
> ⚠️ **可靠性声明见 §5** —— 本画像的 `ALIVE`/`WEAK` 列表**尚未可信**（多腿污染未清干净）。

---

## 一 画像表结构

| 列 | 含义 |
|---|---|
| `region` / `dataset` / `category` / `field` | 定位 |
| `ftype` | MATRIX / VECTOR / GROUP / SYMBOL |
| `coverage` | 覆盖率（归一化到 0~1） |
| `family` | 命名族（去数字与期限后缀） |
| `n_tests` | 已测次数（来自 `backtest_results`） |
| `to_med` / `to_min` / `to_max` | 换手中位数 / 最小 / 最大 |
| `best_s` / `best_2y` / `best_sub` / `best_f` | 全部记录的最好值 |
| **`best_s_sg` / `best_2y_sg` / `best_sub_sg` / `n_sg`** | **单信号记录**的最好值（⚠️ 见 §5） |
| `best_2y_when_s_hi` | S 最高那条的 2Y（诊断「2Y有S无」） |
| `verdict` | 判定 |

**verdict 规则**（每条都有实测依据）：
```
ALIVE          best_s_sg ≥ 1.58
WEAK           best_s_sg ≥ 1.10
DEAD_STATIC    to_med < 0.03                          11 字段实证
DEAD_TURNOVER  to_med > 0.70                          167 字段实证
DEAD_COUNT     名字含 num/count 且 2Y≥1.3 且 S≤0.7    5 次独立出现
DEAD / UNTESTED
```

---

## 二 全量 verdict 分布

| verdict | 数量 | 占比 |
|---|---:|---:|
| **UNTESTED** | **22180** | **98.6%** |
| DEAD | 248 | 1.1% |
| **WEAK** | **20** | 0.09% |
| DEAD_TURNOVER | 19 | 0.08% |
| ALIVE | 15 ⚠️ | 0.07% |
| DEAD_STATIC | 11 | 0.05% |
| DEAD_COUNT | 1 | 0.004% |

---

## 三 ★ category × verdict 交叉表（本报告最有信息量的一张）

| category | ALIVE⚠️ | WEAK | DEAD | DEAD_TURN | DEAD_STAT | DEAD_COUNT | UNTESTED | 合计 |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| **MODEL** | 10 | **12** | 87 | 6 | 1 | 0 | **8057** | 8173 |
| **ANALYST** | 0 | 3 | 68 | 5 | 6 | 1 | **4229** | 4312 |
| **OTHER** | 3 | 4 | 40 | 1 | 1 | 0 | **3872** | 3921 |
| **PV** | 0 | 0 | 21 | 0 | 0 | 0 | **2856** | 2877 |
| **FUNDAMENTAL** | 0 | 0 | 11 | 0 | 2 | 0 | **2133** | 2146 |
| NEWS | 0 | 0 | 4 | **6** | 0 | 0 | 513 | 523 |
| SENTIMENT | 0 | 0 | 0 | 0 | 0 | 0 | 276 | 276 |
| INSIDERS | 1 | 0 | 3 | 0 | 0 | 0 | 38 | 42 |
| **INSTITUTIONS** | 0 | 1 | 7 | 1 | 1 | 0 | **56** | 66 |
| RISK | 0 | 0 | 3 | 0 | 0 | 0 | 49 | 52 |
| EARNINGS | 0 | 0 | 0 | 0 | 0 | 0 | 25 | 25 |
| SHORTINTEREST | 1 | 0 | 4 | 0 | 0 | 0 | 20 | 25 |
| OPTION / MACRO / SOCIALMEDIA / IMBALANCE | 0 | 0 | 0 | 0 | 0 | 0 | 22 / 13 / 19 / 2 | — |

### 三点读法

1. **MODEL 是唯一"有厚度"的 category**：8057 未测 + 12 WEAK + 10 ALIVE ⇒ **它贡献了全部 WEAK 的 60%**。
2. **PV（2856）/ FUNDAMENTAL（2133）几乎全未测，但已测部分 0 产出** ⇒ 与我的战役结论一致（PV 与基本面在 DEU 无信号）。
3. **NEWS 有 6 个 DEAD_TURNOVER（换手爆表）** ⇒ 新闻类字段更新太快，**换手闸先杀**。这是一个 category 级的结构性障碍。

---

## 四 三个关键名单

### 4.1 WEAK（20 个）—— 已测有信号但不够强

| dataset | field | 类型 | cov | n | to_med | S_sg | 2Y_sg | sub |
|---|---|---|---:|---:|---:|---:|---:|---:|
| predictive_starmine | `mean_estimate_change_pct_f12m_ebitda_14d_4` | MATRIX | 0.95 | 15 | 0.217 | **1.39** | 1.21 | — |
| model216 | `mdl216_armpreferredrevisionscore` | VECTOR | 0.82 | 19 | 0.094 | **1.45** | 0.84 | — |
| analyst93 | `anl93_recprofitabilityprev_analyst_profitability2` | VECTOR | 0.64 | 25 | 0.080 | **1.30** | 1.17 | 0.84 |
| analyst93 | `anl93_recprofitabilityprev_estimator_profitability2` | VECTOR | 0.64 | 7 | 0.080 | 1.28 | 1.09 | 0.86 |
| analyst_factor_signals | `eps_y2_estimate_coeff_var` | MATRIX | 0.89 | 23 | — | **1.23** | **1.49** | 0.84 |
| model250 | `mdl250_malta_eq_score` / `maltahc_eq_score` | MATRIX | 0.56 | 2 / 1 | 0.107 / 0.083 | 1.31 / 1.30 | 0.05 / 0.53 | — |
| model25 | `mdl25_eq_v4_2_1_v6` / `_v22` | MATRIX | 0.65 | 7 / 1 | 0.127 / 0.031 | 1.18 | 0.31 | — |
| model238 | `mdl238_industry_rank` / `global_screening_rank` / `global_rank` | MATRIX | 1.00 | 17 / 1 / 1 | 0.138 / 0.075 / 0.113 | 1.27 / 1.18 / 1.17 | 0.97 / 0.88 / 0.85 | — |
| model216 | `mdl216_armindustry100score` | VECTOR | 0.71 | 1 | 0.088 | 1.17 | 0.40 | — |
| predictive_starmine | `..._f12m_earnings_30d_5` / `..._fy1_earnings_30d_4` | MATRIX | 0.97 | 14 / 7 | 0.199 / 0.183 | 1.23 / 1.18 | 0.81 / 0.33 | — |
| dl_riskfree_returns | 分位数标签 ×6 | MATRIX | 1.00 | — | — | 1.12~1.45 | — | — |

**★ 排除项**：`dl_riskfree_returns` 的 6~8 条是**分位数分桶标签，不是信号**（记忆已明确）。

### 4.2 DEAD_STATIC（11 个，换手 <0.03，任何骨架都无用）

`act_q_ebi_surprisemean`(0.0184)｜`anl93_recprofitabilityprev_analyst_analyst`(0.0185)｜`act_q_eps_surprisemean`(0.0189)｜
`fnd6_ewq_rectoq`(0.0193)｜`fnd6_capxy`(0.0197)｜`count_institutional_buyers_security`(0.0204)｜
`anl93_analyst_accuracy2`(0.0237)｜`smest_f12m_earnings_5`(0.0247)｜`oth545_mpd`(0.0263)｜
`anl93_estimator_correct_revision_ratio`(0.0284)｜`anl93_analyst_correct_revision_ratio`(0.0286)

**★ 11 个里 4 个是 `anl93_*`** ⇒ 从换手维度独立证实该数据集的"静态属性"性质。

### 4.3 DEAD_TURNOVER（19 个，换手 >0.70，被闸直接拒）

按 category：**NEWS 6 个**（`nws17/20/50_event_sentiment` 等）｜PV 0｜MODEL 6 个（`mdl106_*`）｜ANALYST 5 个（`anl44_2_*`、`anl9_*`）｜INSTITUTIONS 1｜OTHER 1

**★ category 级结论**：**NEWS 的换手爆表率最高**（6/523 = 1.1%，而全场 19/22494 = 0.08%）⇒ **新闻类字段的更新频率与 DEU 的换手约束结构性冲突**。

---

## 五 ⚠️ 可靠性声明（**必读**）

### 5.1 ALIVE 列表**不可信** —— 多腿污染未清干净

**证据**：画像显示 `mdl264_amihud_class` 的 `best_s_sg = 1.94`，但我在 **MODEL 审计**里**手工逐条核对**过：
> 它的**单信号**记录最好只有 **S0.74**；S1.94 来自 4~5 腿的 `add(...)` 组合。

**⇒ 15 个 ALIVE 里大部分可能是多腿污染的产物，与 WEAK 名单的可信度不同。**

**根因**：`is_multileg` 判据改了两次仍未对：
- 旧版「≥2 个 `rank(`」→ 假阳性（误杀合法单信号）
- 现版「`add(` + ≥2 个不同信号字段」→ **假阴性**（漏掉某些多腿形态）

**⇒ 正确判据应是**：解析 `add(` 的**参数树**，数它直接组合了几个"信号子表达式"（而不是数字段 token）。

### 5.2 UNTESTED 22180 **虚高**

**证据**：`backtest_results` 里只存了 **3 条**含 `eps_y1_estimate_change_3mo` 的记录（形态还是老 wave 的），
而我本轮**实测该字段 30+ 次**（含 `9qWX78vX` 系列）。

**⇒ 收割路径不落 `backtest_results`** ⇒ 画像只反映"历史上被某工具落库过的记录"，**不是"我测过的全部"**。

**⇒ 这解释了为什么回填后画像数字一位没变**（W166 的结果没有落库）。

### 5.3 结论：画像目前的价值定位

| 能信 | 不能信 |
|---|---|
| ✅ **换手**（`to_med`）—— 来自实测记录，直接反映字段的时间变化性 | ❌ ALIVE / WEAK（多腿污染） |
| ✅ **类型**（`ftype`）、**覆盖**（`coverage`）—— 来自 `fields` 表 | ❌ UNTESTED（虚高，且含平台上已不存在的名字） |
| ✅ **DEAD_STATIC / DEAD_TURNOVER**（只看换手，与 S 无关） | ❌ `best_s` / `best_2y`（含多腿） |

**⇒ 当前可靠的用法**：用 `to_med` 做**换手边界筛查**（这一条与实测一致、已验证），其余判定待修。

---

## 六 修复清单（下一步）

| # | 问题 | 修法 |
|---|---|---|
| 1 | 多腿假阴性 | 解析 `add(` 参数树，数"信号子表达式"个数（而非字段 token 数） |
| 2 | 收割不落库 | 在收割脚本里加 `upsert_backtest_rows`（平台有 `mcp__wqb-db__upsert_backtest_rows`） |
| 3 | 本地字段名可能平台已无 | `--build` 后对候选做一次 `preflight_expressions` 校验（零成本） |
| 4 | 字段表有重复行（同一字段多个 cov 快照） | `--build` 时按 `field_name` 去重取最大 cov |

**★ 修完这 4 条，画像才算可交付。** 目前它是一份**结构正确、但判定值需修正**的半成品。
