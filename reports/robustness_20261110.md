# 稳健性审计 — DEU 第三席候选（2026-11-10）

**口径依据**：`Claude/skills/brain-alpha-robustness/SKILL.md` Phase C 判定表（2026-04-22 论坛共识台账 + 本文表）。
**关键口径修正（本轮）**：此前审计用的 CV 口径有双重错误 —— ①用了**样本 sd（÷(n-1)）**；②把 **0.60（REJECT 线）当成了「超线即死」线**。
skill 规定：
- `Recent-3yr CV_Sharpe = 最近 3 个年度 Sharpe 的 std / mean`，**默认总体 sd（÷n）**
  （证据：zq3eb7No 审计报告 —— 总体 0.387 判 PASS、样本 0.474 仅为参考带）
- 三档：**<0.40 PASS / 0.40–0.60 CONDITIONAL / ≥0.60 REJECT**
- **CV 永不单独构成 REJECT**（LLMzYrZe 被 REJECT 的真正原因是「近三年均值 1.570 < 1.58」主判未达）

---

# 稳健性审计 — E569ZE7L（2026-11-10 09:0x）★ 第三席代表

**口径：Recent-3yr（2021/2022/2023，skill 判定表主判）**

表达式 `-group_rank(ts_target_tvr_decay(multiply(rank(ts_delta(ts_backfill(vec_avg(shrt3_bar), 132), 264)), rank(ts_delta(ts_backfill(vec_avg(shrt3_bar), 132), 132))), target_tvr=0.03), subindustry)`
DEU/TOP500/D1/decay4/FAST/trunc0.08/nanON，10 ops

| 年 | Sharpe | Fitness | longCount | margin | 备注 |
|---|---:|---:|---:|---:|---|
| 2014 | 1.72 | 1.23 | 158 | 10.19bp | |
| 2015 | 2.23 | 1.86 | 169 | 14.32bp | |
| 2016 | 0.62 | 0.26 | 182 | 3.65bp | 低年 |
| 2017 | 2.40 | 1.90 | 200 | 14.17bp | |
| 2018 | 1.83 | 1.38 | 198 | 12.17bp | |
| 2019 | 0.37 | 0.12 | 206 | 2.46bp | 全史低点（单年离群） |
| 2020 | 2.34 | 2.05 | 223 | 18.14bp | |
| **2021** | **0.55** | 0.22 | 285 | 4.24bp | **近3年最低** |
| **2022** | **2.64** | 2.57 | 299 | 22.53bp | |
| **2023** | **1.88** | 1.44 | 277 | 13.80bp | 末年 |

## Phase C 判定表逐项

| 检查项 | 实测 | 档 | 依据 |
|---|---|---|---|
| **Recent-3yr Sharpe（主判定）** | 0.55 / 2.64 / 1.88，**均值 1.690 ≥ 1.58**，每年 > 0.3 | **PASS** | 三年合计 5.07 > 4.74；无负年 |
| **Recent-3yr CV_Sharpe** | 总体 sd 口径 **0.5111**（样本 sd 参考 0.6260） | **CONDITIONAL** | 落在 0.40–0.60 带 |
| 衰减比 | 1.88 / 1.658 = **1.134** ≥ 0.50 | PASS | 末年**高于**全期均值，无末段衰减 |
| 平年（仅最近 3 年） | 0（最低 0.55） | PASS | |
| Recent-3yr max/min | 2.64 / 0.55 = **4.80** | **CONDITIONAL** | 落在 3–5 带（2021 单年拉大分母） |
| 全历史早年疲软 | 10y CV 0.507、max/min 4.42 | 仅软标记 | skill 明文「**绝不**据此 REJECT」 |
| Sub-universe | 0.86（限 0.75×√(500/500)×1.68 = 1.26） | PASS | 平台 LOW_SUB_UNIVERSE_SHARPE = PASS |
| 算子数 | 10 | 仅软标记 | REGULAR 不因算子数 REJECT（>5 提示过拟合风险） |
| Margin @ turnover | 2023: 13.80bp @ TO 10.67% | PASS | ≥5bp；TO 全史 9.3–10.6% 极稳 |
| Top-5 个股集中度 | 未取得逐股分解 | — | 仅软标记 |
| 经济可解释性 | 一句话可写：「借券需求评级加速上升 = 做空/对冲需求拥挤 ⇒ 后续反转，做空借券需求抬升股」 | PASS | 外部文献：Lou & Polk 2018 comomentum；short-interest skew 拥挤预警 |
| WebDataScope failed count | Failed RA = 0，PPA = 0，pending 无 | PASS | `get_alpha_details` is.checks.fail = [] |

**结论：CONDITIONAL**（主判 PASS + CV 与 max/min 两项落 CONDITIONAL 带）

**soft_flags**：
1. Recent-3yr CV 0.511（总体 sd）落 0.40–0.60 带 —— 根因是 **2021 年德国借券市场几无波动**（借券评级变化信号信息量不足），2022 极端反弹；8 个窗口变体在 2021 年全部退化（0.18~0.55）⇒ **数据环境特性，非选样问题**
2. Recent-3yr max/min 4.80（同一根因：2021 的 0.55 拉大分母）
3. 算子数 10（>5 软标记；PPA 硬上限 ≤8 仅约束 PPA 通道，本件走 REGULAR）
4. 全史 max/min 4.42（2019 年 0.37 拉低分母）

**平台闸**：S1.68 / F1.21 / 2Y2.27 / TO0.1128 / sub0.86 / failed_ra=0 / prod0.5444 / self0.5444 / ΔSharpe+0.06（不稀释）
**正交性**：与 1YNMAA8M 互相关 **0.1227**；与全部 17 件 OS REGULAR 全部 < 0.7（19/19 完整独立集）
**覆盖**：2014–2023 每年均有数据，longCount 158→299 单调上升，**无空窗**
**金字塔**：DEU/D1/SHORTINTEREST（单塔 ATOM，不占两塔组合配额）

---

# 稳健性审计 — 9qxnNkeq（2026-11-10 09:0x）★ 族内次优，降级为备选

表达式 `-group_rank(ts_target_tvr_decay(multiply(rank(ts_delta(ts_backfill(vec_avg(shrt3_bar), 132), 264)), rank(ts_delta(ts_backfill(vec_avg(shrt3_bar), 132), 88))), target_tvr=0.03), subindustry)`

| 年 | Sharpe | Fitness | longCount |
|---|---:|---:|---:|
| 2014 | 1.05 | 0.58 | 159 |
| 2015 | 2.26 | 1.86 | 169 |
| 2016 | 0.09 | 0.01 | 182 |
| 2017 | 2.38 | 1.87 | 200 |
| 2018 | 1.62 | 1.13 | 198 |
| 2019 | 0.60 | 0.24 | 205 |
| 2020 | 2.54 | 2.27 | 223 |
| **2021** | **0.50** | 0.19 | 284 |
| **2022** | **3.00** | 3.11 | 299 |
| **2023** | **2.35** | 2.01 | 277 |

| 检查项 | 实测 | 档 |
|---|---|---|
| Recent-3yr Sharpe（主判） | 0.50 / 3.00 / 2.35，均值 1.950 ≥ 1.58，每年 > 0.3 | PASS |
| Recent-3yr CV_Sharpe | 总体 sd **0.5431**（样本参考 0.6652） | CONDITIONAL |
| 衰减比 | 2.35 / 1.639 = 1.434 | PASS |
| 平年 | 0 | PASS |
| **Recent-3yr max/min** | 3.00 / 0.50 = **6.00 > 5** | **REJECT** |
| 2016 年 | S 0.09（< 0.3）| 全史软标记 |

**结论：REJECT（Recent-3yr max/min = 6.00 > 5）**

**这是本轮口径修正带来的第二个结论**：此前我把 9qxnNkeq 当作族代表（因 CV 0.665 < E569ZE7L 的 0.626），
那是样本 sd 口径下的排序。按 skill 真实口径，**E569ZE7L 的 max/min = 4.80（CONDITIONAL）优于
9qxnNkeq 的 6.00（REJECT）** ⇒ 族代表应为 **E569ZE7L**，9qxnNkeq 降为备选（不提交）。

---

# 稳健性审计 — 1YNMAA8M（2026-11-10 09:1x，口径复核）

表达式 `multiply(multiply(group_rank(ts_mean(mean_estimate_change_pct_f12m_earnings_7d_4, 10), sector), group_rank(ts_mean(netprofit_y1_estimate_change_3mo, 50), sector)), group_rank(ts_sum(anl15_dps_gr_12_m_3m_chg, 22), sector))`
DEU/TOP500/D1/decay4/SUBINDUSTRY/trunc0.08/nanOFF，9 ops

| 年 | Sharpe | Fitness | longCount |
|---|---:|---:|---:|
| 2014 | 1.65 | 1.31 | 76 |
| 2015 | 1.59 | 1.32 | 81 |
| 2016 | 1.56 | 1.28 | 88 |
| 2017 | 1.01 | 0.63 | 97 |
| 2018 | 1.06 | 0.78 | 102 |
| 2019 | 2.06 | 1.96 | 103 |
| 2020 | 0.78 | 0.54 | 122 |
| **2021** | **2.96** | 3.54 | 140 |
| **2022** | **2.19** | 2.34 | 150 |
| **2023** | **1.25** | 0.97 | 129 |

| 检查项 | 实测 | 档 |
|---|---|---|
| Recent-3yr Sharpe（主判） | 2.96 / 2.19 / 1.25，均值 **2.133** ≥ 1.58，每年 > 0.3 | PASS |
| **Recent-3yr CV_Sharpe** | 总体 sd **0.3278**（样本参考 0.4014）| **PASS**（<0.40）|
| 衰减比 | 1.25 / 1.762 = 0.776 ≥ 0.50 | PASS（末段有降但未破线）|
| 平年 | 0 | PASS |
| Recent-3yr max/min | 2.96 / 1.25 = **2.37 ≤ 3** | PASS |
| 全历史早年疲软 | 10y CV 0.356、max/min 2.37 | 仅软标记 |
| Sub-universe | 1.01 | PASS |
| 算子数 | 9 | 仅软标记 |
| Margin @ turnover | 2023: 12.13bp @ TO 13.37% | PASS |
| 经济可解释性 | 一句话可写 | PASS |
| WebDataScope failed | 0 | PASS |

**结论：PASS（全部检查项 PASS，无 CONDITIONAL 项）**

**平台闸**：S1.58 / F1.36 / 2Y2.13 / TO0.1337 / sub1.01 / failed_ra=0 / prod0.6951（refresh 复测稳定）/ self0.6946 / ΔSharpe+0.43
**正交性**：与 17 件 OS REGULAR 全部 < 0.7（18/18 独立集）
**覆盖**：2014–2023 每年均有数据，longCount 76→150

---

# 口径修正总结（本轮最重要产出）

| 项 | 此前（本轮我的错误用法） | skill 权威口径 | 影响 |
|---|---|---|---|
| CV 的 sd | 样本 sd（÷(n-1)） | **总体 sd（÷n）**，样本 sd 仅作参考带 | E569ZE7L：0.626 → **0.511**（降一档） |
| CV 的阈值语义 | ≥0.60 即 REJECT（当作生死线） | 0.60 是 REJECT 线，**0.40–0.60 是 CONDITIONAL 带** | E569ZE7L：REJECT → **CONDITIONAL** |
| CV 能否单独 REJECT | 认为可以 | **永不单独 REJECT**（skill 明文） | 判定从「生死」变「带 soft_flag」 |
| 族代表排序 | 按样本 sd CV 排 ⇒ 选 9qxnNkeq | 按 max/min ⇒ **E569ZE7L**（4.80）优于 9qxnNkeq（6.00 REJECT） | 换代表 |

**流程改进（写入 Agent Memory）**：任何稳健性判定前，**先读 `brain-alpha-robustness/SKILL.md` Phase C 的判定表**，
不要凭印象记阈值 —— 判定表是事实源，且阈值分三档（PASS/CONDITIONAL/REJECT），
CONDITIONAL 的规范动作是「repair 一轮后重跑」，不是「判死」，也不是「自动放行」。

---

# 0mY1QPEv（EUR TOP2500 d1 CROWDING）· 2026-11-10 12:10 审计

`group_rank(subtract(group_rank(subtract(probability_fifth_quantile_ten_day_bucket_four_15,probability_fifth_quantile_ten_day_bucket_zero_15),subindustry),group_rank(vec_avg(snt26_avgranking),subindustry)),subindustry)`

## B.0 资格门
Failed RA = 0 / Failed PPA = 0 ⇒ 无名单内 PENDING，继续。

## B.1 顶层
6 算子；S 3.76 / F 2.32 / TO 23.84% / returns 9.07% / margin 7.61bp / DD 1.64%；longCount 1417、shortCount 1399（双侧均衡）；平台 checks 9 PASS / 0 FAIL / 2 WARNING（MATCHES_COMPETITION、MATCHES_THEMES 属信息项）。

## B.2 逐年（10 个完整 IS 年，long/short 每年均 >0，无空窗）
| 年 | 2014 | 2015 | 2016 | 2017 | 2018 | 2019 | 2020 | 2021 | 2022 | 2023 |
|---|---|---|---|---|---|---|---|---|---|---|
| Sharpe | 4.09 | 4.82 | 6.07 | 3.74 | 5.16 | 3.02 | 4.18 | 3.72 | **1.36** | 3.00 |
| Return | 10.5% | 14.5% | 13.5% | 6.0% | 9.3% | 6.3% | 13.9% | 7.5% | 4.1% | 5.5% |

## B.3 Recent-3yr 判定（Phase C 表）
| 项 | 读数 | 判 |
|---|---|---|
| Recent-3yr Sharpe（主判定） | 2021 3.72 / 2022 1.36 / 2023 3.00，均值 **2.69** ≥ 1.58，三年全正 | **PASS** |
| Recent-3yr CV_Sharpe | 总体 sd 0.988 / 2.693 = **0.367**（< 0.40） | **PASS** |
| 衰减比 | 3.00 / 3.76 = **0.798**（≥ 0.50） | **PASS** |
| 平年（\|S\|<0.3） | 0 个（最低 1.36） | **PASS** |
| Recent-3yr max/min | 3.72 / 1.36 = **2.74**（≤ 3） | **PASS** |
| Sub-universe | 平台 PASS：2.14 vs 1.95 | **PASS** |
| Margin @ turnover | 7.61 bp @ 23.8% TVR（≥ 5 bp） | **PASS** |
| 算子数 | 6（> 5） | 软标记 |
| 回撤日历 | 季均 0.333%，最高 2022Q3 **0.722% = 2.17×** 均值 | 软标记（> 2×） |
| 经济可解释性 | 分析师盈利预测分布右移（上修）＋ 网页关注度抬升，二者同向 = 预期修正未被充分定价 ⇒ 做多 | **PASS** |

## B.4 相关性
prod **0.6339**（`prod_peek` 2026-11-10 11:30，已入权威表）；self **0.0886**（本地池 17 颗，最近 kqJOQgnk 0.0886）。均远低于 0.70。

## C. 判定
**PASS**（带软标记）。软标记：① 算子数 6；② 2022Q2–Q3 季度回撤达全期均值的 1.9–2.2 倍，对应 2022 年 Sharpe 1.36 —— 属"单年偏弱"而非结构失效（该年仍为正、且次年回到 3.00）。
