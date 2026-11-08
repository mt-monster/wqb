# 稳健性归因报告 · 2026-11-05（EUR 1YNjqknX）

## 候选
- 1YNjqknX · EUR/TOP2500/FAST/decay1/trunc0.04/maxTrade OFF
- 表达式：trade_when(greater(group_count(imb5_score, market), 40), add(group_scale(imb5_score, subindustry), group_rank(buy_sell_ratio_all_250d_filled, subindustry)), -1)（6 算子）
- 指标：S 3.37 / F 1.84 / 2Y 2.37 / sub 1.87 / TO 20.39% / margin 5.96bp / lc 1404；CONCENTRATED_WEIGHT PASS、submit_verdict UNVERIFIABLE(failed_ra=0)、self 0.2246、prod 0.67、check_correlation.all_passed=true

## Phase B 归因
- 逐年（get_alpha_yearly_stats）：2014-2023 逐年 longCount 1331-1481、pnl 全非零、Sharpe 1.22-6.27、drawdown 0.46%-1.59%、margin 2.43-9.26bp。
- 近 3 个 IS 年 Sharpe = [1.22, 2.45, 2.26]，均值 1.98 ≥ 2Y 线 1.58 且逐年全正；CV 0.274 < 0.40；衰减比 0.671 ≥ 0.50；max/min 2.01 ≤ 3；近 3 年平年 0。
- get_alpha_pnl：累计 PnL 曲线自 2014 单调上行，investability-constrained PnL 同向；无单季 >2× 全期平均的回撤。
- performance_comparison：对 EQUITY:EUR:1:POWER_POOL 池 before S3.17/F2.01 → after S3.84/F2.43，边际贡献为正。
- compute_mutual_correlation：族内与 pwd5MzVg 0.9971、qML0enMK 0.8878 ⇒ 族内只交 1 颗，避免 self 互锁。

## Phase C 判定
- WebDataScope failed count = 0（CW 转 PASS）且 RA 名单无 PENDING ⇒ 继续。
- Recent-3yr Sharpe / CV / 衰减比 / 平年 / max-min / Sub-universe / Margin@TO / 集中度 / 经济可解释性全部 PASS。
- verdict = PASS（3 条软标记：早年强近年弱厂字形、margin 贴 5bp 线且逐年下滑、6 算子）。
- 台账：ledger key robustness_1YNjqknX = PASS（已 readback 确认）。

## 收益归因与失效风险预估（CLAUDE.md 要求）
- 收益来源：imb5_score 有界评分经 group_scale 保幅（S 1.69→4.03 暴赢来源）+ 买卖比 group_rank 等权辅助腿；trade_when(group_count>40) 只在覆盖充足日持仓，消除 group_scale 保幅导致的集中度（破 CW）。
- 失效风险：① 厂字形衰减 S 6.27→2.26、margin 8.8→4.3bp 同向，OS 可能继续走低；② 族内高度同源，只交 1 颗；③ prod 0.67 距 0.70 仅 0.03；④ 门控依赖 group_count 阈值 40 的覆盖稳定性。
- 结论：PASS，建议按用户授权提交 1YNjqknX 单颗（不连交同族件）。

---

## 候选 LLM5eAMn · EUR/TOP2500/FAST/decay1/trunc0.04/maxTrade OFF（imb5 族，2026-11-05 补审）

- 表达式：add(group_scale(ts_backfill(imb5_score, 250), subindustry), group_rank(ts_backfill(buy_sell_ratio_all_250d_filled, 250), subindustry))（4 算子）
- 指标：S 3.48 / F 1.95 / 2Y 2.48 / sub 1.91 / TO 19.77% / margin 6.30bp；CONCENTRATED_WEIGHT PASS、submit_verdict UNVERIFIABLE(failed_ra=0)、self 0.2322、prod 0.6652、check_correlation.all_passed=true
- 与 1YNjqknX 同族（mutual 0.9699）、同塔位（EUR/D1/IMBALANCE+OTHER），族内只交 1 颗。

### Phase B 归因
- 逐年（get_alpha_yearly_stats）：2014-2023 逐年 longCount 1334-1497、pnl 全非零、Sharpe 1.44-6.36、drawdown 0.45%-1.68%、逐年全覆盖无空窗。
- 近 3 个 IS 年 Sharpe = [1.44, 2.21, 2.76]，均值 2.137 ≥ 2Y 线 1.58 且逐年全正；CV = 0.31 < 0.40；衰减比 = 2.76/3.48 = 0.793 ≥ 0.50；max/min = 1.917 ≤ 3；近 3 年平年 0。
- get_alpha_pnl：累计 PnL 自 2014 单调上行，investability-constrained PnL 同向；无单季 >2× 全期平均回撤。
- performance_comparison：EQUITY:EUR:1:POWER_POOL 池 before S3.17/F2.01 → after pnl 5,429,173，边际贡献为正。
- check_correlation：prod 0.6652（<0.70）、self 0.2322（<0.70）、all_passed=true。

### Phase C 判定
- WebDataScope failed count = 0（checks.fail=[]、仅 MATCHES_THEMES warning）且 RA 名单无 PENDING ⇒ 继续。
- Recent-3yr Sharpe / CV / 衰减比 / 平年 / max-min / Sub-universe（LOW_SUB_UNIVERSE_SHARPE PASS）/ Margin@TO（6.30bp ≥5bp @ TO<40%）/ 集中度 / 经济可解释性全部 PASS。
- verdict = **PASS**。软标记：① 早年强近年弱厂字形（S 6.36→2.76，仅软标记不 REJECT）；② 4 算子（REGULAR 软标记）；③ prod 0.6652 距 0.70 仅 0.035；④ 族内与 1YNjqknX 同源 0.9699，两件只交 1 颗。
- 收益归因：ts_backfill(imb5_score,250) 补齐稀疏缺失日（破 CW 形态杠杆）+ group_scale 保幅主信号 + 买卖比 group_rank 等权辅助。失效风险：厂字形衰减、族内同源、prod 贴线。

---

## 候选 ZYQmolVx · EUR/TOP2500/FAST/decay1/trunc0.04/maxTrade OFF（est_12m_ebt 族，2026-11-05 新审）

- 表达式：trade_when(less(group_rank(rsk68_beta,subindustry),0.6),vector_neut(group_neutralize(group_scale(signed_power(group_zscore(divide(est_12m_ebt_raisednum_4wks,add(est_12m_ebt_raisednum_4wks,est_12m_ebt_lowerednum_4wks)),subindustry),2.05),sector),market),ts_mean(vec_avg(oth553_est_estvalue),66)),-1)（12 算子）
- 指标：S 2.48 / F 1.19 / 2Y 2.15 / sub 1.29 / TO 22.72% / margin 4.59bp / lc 1314；checks.fail=[]、CONCENTRATED_WEIGHT 明确在 PASS 列表、submit_verdict UNVERIFIABLE(failed_ra=0)、self 0.4169、prod 0.5276、check_correlation.all_passed=true
- 塔位：EUR/D1/RISK 1.0 + ANALYST 1.3 + SENTIMENT 1.4（正是要补的 RISK 2/3 塔，三腿全在禁混集合外）。族内 ZYQmolVx↔kqNJKmp8 0.9998 ⇒ 只交 1 颗。

### Phase B 归因
- 逐年（get_alpha_yearly_stats）：2014-2023 逐年 longCount 1314-1516、pnl 全非零、Sharpe 0.80-4.55（10 年逐年全为正、无负年）、drawdown 0.56%-2.96%，总 pnl 5,376,597；近十年全覆盖无空窗。
- 近 3 个 IS 年 Sharpe = [1.44, 1.86, 1.67]，均值 1.657 ≥ 2Y 线 1.58（贴线 +0.077）且逐年全正（每年 >0.3，无平年）；CV = 0.129 < 0.40；衰减比 = 1.67/2.48 = 0.673 ≥ 0.50；max/min = 1.292 ≤ 3。
- get_alpha_pnl：累计 PnL 自 2014 单调上行，investability-constrained PnL 同向；无单季 >2× 全期平均回撤。
- performance_comparison：**平台瞬时故障**（`failed after 6 attempts`），本项本轮未取得读数，如实标注；按 Phase B 该项为软标记来源、非硬闸，不影响下方 Phase C 硬项判定，不编造数值。
- check_correlation：prod 0.5276（改持仓后真测，比原式 zq3Yrb3G 0.5635 更低）、self 0.4169、all_passed=true。

### Phase C 判定
- WebDataScope failed count = 0（checks.fail=[]、仅 MATCHES_THEMES warning）且 RA 名单无 PENDING ⇒ 继续。
- Recent-3yr Sharpe 1.657 贴线但过线、CV 0.129 / 衰减比 0.673 / 平年 0 / max-min 1.292 / Sub-universe（LOW_SUB_UNIVERSE_SHARPE PASS，sub/S 0.5202 ≥ 0.517）/ 集中度 全 PASS。
- Margin@TO：4.59bp @ TO 22.72% —— 噪声拟合 REJECT 条件是「<3bp @ >60% TVR」两条件都不满足，记软标记不 REJECT。
- 算子数 12（REGULAR 仅软标记，>5 提示过拟合风险；PPA 硬上限 ≤8 不适用 REGULAR）。
- 经济可解释性：分析师上调/下调盈利预期家数比（预期修正动量，市场反应不足）经低 beta 门控（rsk68_beta），再对 oth553 估值做 vector_neut 正交剥离估值暴露 —— 一句话可写，PASS。
- verdict = **PASS**。软标记：① Recent-3yr 1.657 贴 2Y 线（+0.077）；② margin 4.59bp 略低于 5bp 论坛经验线但 TO<40% 不构成噪声拟合；③ 12 算子偏多；④ 2016 单年 Sharpe 0.80 为全史最弱（属全历史早年，按 RB-10 绝不 REJECT）；⑤ performance_comparison 本轮平台故障未取到。
- 收益归因：主信号 = 预期修正广度的横截面 z-score（group_zscore over subindustry）+ signed_power(2.05) 压幅（破 sub 相对闸的关键）；辅助 = 低 beta 门控 + 估值正交；group_neutralize(market) 与 B腿 rank(ts_mean(vec_avg(oth553),66)) 为承重墙（删任一 S/F/CW/TO 全崩，见 WAVE_LEDGER §79.1）。失效风险：Recent-3yr 贴线、幂次甜点窄（p∈[2.05,2.10]，p≥2.2 则 2Y 破闸）、族内同源。

### 本批落盘动作
- 台账：upsert robustness_LLM5eAMn = PASS、robustness_ZYQmolVx = PASS（1YNjqknX 已是 PASS，不覆写）。
- 提交状态：三颗仍 UNSUBMITTED；submit_verdict=UNVERIFIABLE 非 SUBMITTABLE；workflow_submit_alpha 的 robustness_audited 是 fail-closed，本批落台账后该前置已满足。真闸仍是用户明确授权后的 confirm_submit=True。本批零提交、零不可逆动作。


---

## 候选 O0AJ3NEd · EUR/TOP2500/FAST/decay1/trunc0.04/maxTrade OFF（est_12m_ebt 族，删 RISK 门版，2026-11-05 新审）

- 表达式：vector_neut(group_neutralize(group_scale(signed_power(group_zscore(divide(est_12m_ebt_raisednum_4wks,add(est_12m_ebt_raisednum_4wks,est_12m_ebt_lowerednum_4wks)),subindustry),2.05),sector),market),ts_mean(vec_avg(oth553_est_estvalue),66))（9 算子）
- 族内关系：为 ZYQmolVx 的逐算子消融 A2（删 `trade_when(less(group_rank(rsk68_beta,subindustry),0.6),·,-1)`）；与基线互测 0.6884（<0.70，独立席位）。同批 A3 `gJeW2bpO`（6 算子，再删 sentiment 腿）与其互测 0.9746，二者同席位，只交 1 颗。
- 指标：S 2.91 / F 1.36 / 2Y 2.60 / sub 1.58（限 1.51）/ TO 28.65% / margin 4.36bp / drawdown 3.49% / lc 1405·sc 1411 / pnl 6,443,539；checks.fail=[]、CONCENTRATED_WEIGHT 在 PASS 列表、RA/PPA failed=0、pyramids.effective=2（ANALYST 1.3 + SENTIMENT 1.4）。
- 相关性：prod **0.6557**（`check_correlation` 权威缓存，all_passed=true，min -0.469，0.6–0.7 桶仅 2 颗）、self **0.4460**。

### Phase B 归因
- 逐年（get_alpha_yearly_stats，2014–2023 共 10 年）：pnl 913565 / 855876 / 383689 / 889489 / 852183 / 582662 / 198592 / 466637 / 746381 / 554411，**10 年全为正、零负年、无空仓年、无 late_start**；单年最大贡献 **14.2%**（2014），无单年依赖；逐年 Sharpe 0.71–5.16（中位 3.17）；逐年 drawdown ≤ 2.84%。
- 近 3 个 IS 年 Sharpe = [1.95, 2.77, 2.41]，均值 **2.377** ≥ 2Y 线 1.58（+0.797）；CV = **0.173** < 0.40；衰减比 = 2.377/2.91 = **0.817** ≥ 0.50；max/min = **1.421** ≤ 3。
- Sub-universe：LOW_SUB_UNIVERSE_SHARPE 1.58 vs 限 1.51，sub/S = **0.543** ≥ 0.517（基线为 0.5202，删门后余量从 +0.003 拓宽到 +0.026）。
- Margin@TO：**4.36bp @ TO 28.65%** —— 噪声拟合 REJECT 条件「<3bp 且 >60% TVR」两条件均不满足，仅记软标记。
- `performance_comparison`：本项不在官方 9 项提交测试内，且对已提交后恒 400；本轮不作归因依据。

### Phase C 判定
- WebDataScope failed RA/PPA = **0**、checks.fail=[]、无 PENDING 红线项 ⇒ 继续。
- 全部硬项通过（近 3 年 Sharpe / CV / 衰减比 / 平年 0 / max-min / sub / 集中度 / margin@TO）⇒ **PASS**。
- 软标记：① 2020 年 S 0.71 / F 0.19（唯一弱年，仍为正）；② margin 4.36bp 偏薄（但未触发 REJECT 阈值）；③ prod 0.6557 属「薄过」，距 0.70 仅 0.044，**提交前应以 48h 内缓存为限，禁再 refresh 抬高占用**。
