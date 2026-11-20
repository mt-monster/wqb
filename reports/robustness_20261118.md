# 稳健性审计报告 2026-11-18

## GrmPOz05（DEU/TOP500/D1，00:18）

> 提交链①②③+robustness 闸门员审计。候选来自零配额收割（S0_TOWER_SCAN_20261117.md §9.1 收割件 №4）。
> 判定：**REJECT**（1 项硬 REJECT：等权混腿结构；4 项软标记不阻断、逐项落盘）。

## B.0 WebDataScope 门（硬前置，平台实读）

`get_alpha_details("GrmPOz05")`：`ra.failed_ra_count=0`、`failed_ppa_count=0`、`ra_failed=false`；
`checks.fail=[]`、`checks.warning` 仅 `MATCHES_COMPETITION`（AQP202611）与 `MATCHES_THEMES`
（GLB/D1 Power Pool Nov'26 ×1.0 / USA/D1 turnover 15..30% ×2.0，均非 counted item）；
`checks.pass` 9 项含 `LOW_SUB_UNIVERSE_SHARPE`、`IS_LADDER_SHARPE`、`CLUSTER_TEST`、`MATCHES_PYRAMID`。
⇒ Failed = 0 且无名单内 PENDING，B.0 通过。

## B.1–B.5 归因（平台实读）

- 表达式（平台 code 原文）：`signed_power(group_zscore(add(add(add(add(multiply(group_rank(ts_delta(ts_mean(vec_avg(insd1_holdings),66),66),sector),group_rank(ts_mean(divide(significant_value_1,…(4 项 significant_value 求和)…,66),sector)),multiply(group_rank(ts_ir(vec_avg(insd1_holdings),66),sector),group_rank(divide(1,add(days_from_last_change(vec_avg(insd1_holdings)),1)),sector))),…(significant_value 腿重复)…),group_rank(ts_ir(vec_avg(insd1_holdings),66),sector)),group_rank(divide(est_12m_ebi_raised_1wk,add(est_12m_ebi_num,1)),sector)),sector),1.3)`
- 配置：DEU / TOP500 / D1 / decay 0 / SUBINDUSTRY / trunc 0.08 / nanHandling ON / 2014-01-01→2023-12-31。
- IS：S 1.79 / F 1.41 / TO 14.09% / 2Y 2.66 / sub 1.02 / margin 12.40bp（12.4bp @ TO 14.09%）/
  DD 6.35% / invest_S 1.55 / risk_neutralized 1.12 / status UNSUBMITTED / stage IS。
- 塔位：`pyramids.effective=2`，list = `DEU/D1/INSIDERS ×1.6` + `DEU/D1/ANALYST ×1.8`；
  `ra.pyramid_short = "insiders/analyst"`。本批同族 5 件互相关 0.83–0.97（S0 2026-11-16
  `compute_mutual_correlation`），五条只能交一颗。

### 逐年归因（get_alpha_yearly_stats，2014–2023 十年全有记录）

| 年 | 2014 | 2015 | 2016 | 2017 | 2018 | 2019 | 2020 | 2021 | 2022 | 2023 |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| Sharpe | 1.60 | 2.10 | 1.30 | 1.52 | 1.86 | 2.22 | 1.51 | **0.62** | 2.30 | 3.05 |
| longCount | 98 | 101 | 103 | 112 | 114 | 121 | 134 | 168 | 168 | 149 |
| shortCount | 119 | 125 | 129 | 144 | 146 | 157 | 178 | 217 | 223 | 199 |
| pnl | 0.72M | 1.16M | 0.82M | 0.72M | 0.97M | 0.99M | 0.76M | 0.29M | 1.13M | 1.45M |

- **③近十年逐年闸（本闸门员的专项核对）：10/10 年 `longCount>0 && shortCount>0 && pnl>0` 全过**。
  十年完整无空窗（无「数据不满十年被全期指标掩盖」情形）。
- 2021 年 S 0.62、pnl 29.4 万为十年最弱年，但为正且非近 3 年窗口内，按口径记软标记（早年疲软类）。
- 近 3 年（2021/2022/2023）：S = 0.62 / 2.30 / 3.05，均值 1.99 ≥ 1.58（用户 2Y 线）；
  但 2021 S 0.62 > 0.3 计正年，0 个平年；主判定 PASS。
- **CV_Sharpe 口径歧义如实披露**：近 3 年 std/mean，总体口径 0.51（软标记带 0.40–0.60），
  样本口径（n−1）0.63（≥0.60 REJECT 带）。仓内无单一权威实现：skill 只写「std/mean」；
  2026-11-16 报告两份先例互斥（`Jj85OR7e` 0.162 恰为总体口径、`wponnkmd` 0.419 最接近样本口径）。
  本报告按主读数取总体口径（与 Jj85OR7e 先例及用户清单「CV 0.40–0.60 软标记」一致），
  样本口径读数一并落盘交用户裁量；此项不影响 REJECT 结论（REJECT 由混腿硬闸独立成立）。
- 衰减比 = 3.05 / 1.79 = 1.704 ≥ 0.50，PASS（末端无衰减）。
- max/min（近 3 年）= 3.05 / 0.62 = 4.92，落在 3–5 带 = CONDITIONAL 软标记（未超 5）。
- Top-5 个股集中度：无逐股 PnL 不可得；平台 `CONCENTRATED_WEIGHT` PASS 代证。
- 经济可解释性（一句话）：「内部人持仓动量与集中度信噪比、机构显著交易占比、分析师上调占比四腿行业内排名
  加权聚合——复合结构，方向可读但因混腿结构不合规」。

### ④⑤相关性（本闸不做，只登记待查项）

- 本地快照（`get_alpha_corr_metrics(DEU)`）：`prod_correlation=0.4923`（source=platform_sync，
  corr_checked_at 2026-11-17T08:07:01，age 15.72h，非 stale）；`self_correlation=0.3136`（同源同戳）。
  与 ask 给的 check_correlation prod=0.4923 一致。**④⑤判定与终验归相关性员**（本闸不回源、不下结论）。

## Phase C 反过拟合闸

| 检查项 | 实测 | 判定 |
|---|---|---|
| WebDataScope failed count | Failed RA=0 / PPA=0，无名单内 PENDING | **PASS** |
| Recent-3yr Sharpe（主判定） | 0.62/2.30/3.05 均值 1.99 ≥ 1.58；每年 > 0.3 | **PASS** |
| Recent-3yr CV_Sharpe | 总体口径 0.51（0.40–0.60 带）；样本口径 0.63（≥0.60）；口径仓内无单源（见上） | **软标记（歧义披露）** |
| 衰减比 | 3.05/1.79 = 1.704 ≥ 0.50 | **PASS** |
| 平年（近 3 年） | 0 | **PASS** |
| Recent-3yr max/min | 4.92（3–5 带） | **软标记** |
| 全历史早年疲软 | 2021 S 0.62（十年最弱，正年非平年，非近 3 年） | **软标记（绝不 REJECT）** |
| Sub-universe | `LOW_SUB_UNIVERSE_SHARPE` 平台 PASS，sub 1.02 | **PASS** |
| 算子数 | distinct 算子 11（signed_power/group_zscore/add/multiply/group_rank/ts_delta/ts_mean/divide/ts_ir/days_from_last_change/rank 系），> 5 | **软标记**（REGULAR 不据此 REJECT） |
| Margin @ turnover | 12.40bp @ TO 14.09%（≥5bp） | **PASS** |
| Top-5 个股集中度 | 逐股 PnL 不可得；`CONCENTRATED_WEIGHT` PASS 代证 | 不可得（平台代证） |
| **混腿结构（AGENTS.md §7.7 混腿禁令 / methodology_rules `mixed_signal_leg_ban_v1`）** | 闸5 检测器 `_find_equal_weight_leg_add` 复跑（本闸 2026-11-18 00:18，`logs/_tmp_grm_addgate.py`）：**4 命中、全部 same_dataset=false、block=true**；与 S0_TOWER_SCAN_20261117.md §16.6 复核表（`logs/_tmp_s0_add_gate.py` 4 命中）一致 | **硬 REJECT** |

## 结论

**REJECT**（`submit_verdict` fail-closed：读到 REJECT 即 BLOCKED，reason_code `ROBUSTNESS_REJECT`）。

- 硬 REJECT 项 1 条：**等权混腿**。表达式本质是 4 处 `add(独立信号腿A, 独立信号腿B)`（insd1_holdings 动量腿 /
  significant_value 显著交易腿 / est_12m_ebi 分析师腿跨数据集相加）。`mixed_signal_leg_ban_v1` 明文
  「仍然无条件禁止 add(独立信号腿A,独立信号腿B)」，且「门禁通过 ≠ 合规：闸是兜底不是许可证」；
  S0 扫描已据同一证据把 7 条收割件全部移出可提交池、注明「待用户裁定」，本闸复跑同读数。
  **唯一合规方向 = Mode B 换字段组合/换几何/换分组轴，或单信号结构化；不得靠扫描混权修复。**
- 软标记 4 项（不阻断、逐项落盘）：CV_Sharpe 口径歧义（0.51 总体 / 0.63 样本）、max/min 4.92（3–5 带）、
  2021 早年疲软、算子 11 > 5。
- ②RA 闸与塔位：failed_ra=0 平台实读通过；塔位 `DEU/D1/INSIDERS + DEU/D1/ANALYST`（effective 2，
  乘积 2.88），提交会给 insiders 塔与 analyst 塔各 +1 —— 但混腿 REJECT 成立时这些塔位收益不可兑现。
- ③近十年：10/10 年三条件全过，无异常年（2021 最弱年如实标注，正年）。
- ①台账排除：insiders1 台账命中 379 行（多区死/判死档案），但 §7.5「判死标记不得单独作为依据」
  且 DEU 实测线（_effective-levers.md）为 provisional 未判死 —— 本候选不因此排除；排除它的实证是混腿硬闸。
- provenance 修正：ask 称候选出自波 `rt-insiders-w4`，但 `get_wave_result(DEU, rt-insiders-w4)` 20 臂名单
  （批1 批2，expressions id 109942-109951 / 110378-110387）均不含 GrmPOz05；实际出处为
  BE145/BE146（2026-11-12）→ S0_TOWER_SCAN_20261117.md 收割池 §9.1/§16.6。

---

## `Jj8pgxJm`（USA / D1 / SHORTINTEREST）— 提交前稳健性审计

**审计时间**：2026-11-18 02:1x ｜ **触发**：用户 02:11「提交 Jj8pgxJm」⇒ 按 `brain-alpha-robustness` Phase B/C 走完整闸
**表达式（变量抽取版，调用点 9 / distinct 6）**：
```
a = subtract(divide(shrt43_edgxshvol_svol, shrt43_edgxshvol_totalvolume),
             divide(add(shrt43_batsshvol_svol, shrt43_byxxshvol_svol),
                    add(shrt43_batsshvol_totalvolume, shrt43_byxxshvol_totalvolume)));
ts_target_tvr_decay(group_zscore(add(a, ts_mean(a, 121)), subindustry), target_tvr=0.1)
```
**设置**：USA / TOP3000 / D1 / decay 0 / STATISTICAL / trunc 0.08 / pasteurization ON / nanHandling ON / unitHandling VERIFY

### B.0 WebDataScope failed-count（硬前置）
`get_alpha_details` → `ra.failed_ra_count = 0`、`failed_ppa_count = 0`、`ra_failed = false`；
`checks.fail = []`，8 项全 PASS（LOW_SHARPE / LOW_FITNESS / LOW_TURNOVER / HIGH_TURNOVER / CONCENTRATED_WEIGHT / LOW_SUB_UNIVERSE_SHARPE / LOW_2Y_SHARPE / MATCHES_PYRAMID）。
⇒ **Failed = 0**，进入 B.1–B.5。

### B.1–B.5 归因
| 项 | 读数 |
|---|---|
| 顶层指标 | S **1.90** ｜ F **1.06** ｜ TO **11.21%** ｜ R **3.88%** ｜ DD **2.41%** ｜ margin **6.92 bp** ｜ 持仓 1591L/1534S |
| 2Y / sub-universe | **2.12** ｜ **0.83**（平台 `LOW_SUB_UNIVERSE_SHARPE` PASS） |
| 逐年 S（2014→2023） | 5.23 / 1.68 / **0.10** / **0.47** / 3.78 / 1.26 / 1.74 / **1.07** / **1.31** / 2.81 |
| 逐年 PnL（万元） | 91.0 / 36.1 / 2.0 / 8.5 / 76.8 / 25.5 / 40.5 / 23.8 / 25.0 / 56.3（合计 385.3 万） |
| 回撤日历 | 降采样曲线（2494 点）无单季异常回撤；全期 DD 2.41%，单季谷底最深约 0.3% 量级 |
| 换手 × margin | 11.21% × 6.92 bp ⇒ 不触发「>60% TVR 且 <3bp」噪声拟合线 |
| Top-5 个股集中度 | **不可得**（`get_alpha_pnl` 只返回日度累计 PnL，无逐股分解）⇒ 记为未测 |
| prod correlation | **0.6339**（<0.7，余量 0.066）｜ `check_correlation` both |
| self correlation | **0.1758**（pool 142，首位 `9WkpwQq` 0.1758）｜余量 0.524 |

### Phase C 反过拟合闸（年度项只算最近 3 个 IS 年）
| 检查项 | 数值 | 判定 |
|---|---|---|
| WebDataScope failed count | 0，无名单内 PENDING | **PASS** |
| Recent-3yr Sharpe（主判定） | 2Y **2.12 ≥ 1.58**；近三年 1.07 / 1.31 / 2.81 均 >0.3 | **PASS** |
| Recent-3yr CV_Sharpe | mean 1.730、pop sd 0.770 ⇒ **0.445**（sample sd 口径 0.545） | **CONDITIONAL（0.40–0.60 带）** |
| 衰减比（末年/全期） | 2.81 / 1.90 = **1.48** | **PASS** |
| 平年（近 3 年 \|S\|<0.3） | 0 个 | **PASS** |
| Recent-3yr max/min | 2.81 / 1.07 = **2.63** | **PASS（≤3）** |
| 全历史早年疲软 | 2016 S 0.10 / 2017 S 0.47 / 2019 1.26 | 近窗制下**只记软标记，绝不据此 REJECT** |
| Sub-universe | 平台 PASS（0.83） | **PASS** |
| 算子数 | distinct **6**（调用 9） | 软标记（REGULAR 不因算子数 REJECT） |
| Margin @ turnover | 6.92 bp @ 11.21% TVR | **PASS（≥5bp）** |
| Top-5 集中度 | 数据不可得 | 未测 |
| 经济可解释性 | 「EDGX 场所的空头成交占比相对 BATS+BYX 的偏离，度量空头在单一场所的集中度；要求当前偏离与 121 日中期偏离同向才给满仓，滤掉单日噪声造成的假挤压」 | **PASS（一句话）** |

### 判定
**硬 REJECT 项：0。判定 = CONDITIONAL**（唯一 CONDITIONAL 项为 Recent-3yr CV_Sharpe 0.445 落在 0.40–0.60 带）。

**软标记**：`CV_Sharpe(近3年)=0.445` ｜ `ops_distinct=6 (>5)` ｜ `全历史早年疲软 2016 S0.10 / 2017 S0.47`

**处置说明**：`submit_verdict` 对 CONDITIONAL 为 fail-open（不改判、只提示先 repair）；本次由用户 **02:11 明确点名叫停提交**，视为「用户明确指令」通道留痕，未做 CV 修复轮换（修复需改窗口/降波动，会改变已定型的 PnL）。

---

## wpolZRO6（DEU/TOP500/D1，12:47）—— VkNOJYnM 的 3 腿合规等价重写

> 背景：VkNOJYnM（4 腿 stack 结构闸硬拦）→ 1YWnZ9rK（5 腿同拦）→ 数学等价重写两步：① 分配律合并 leg2+gri = gri×(2−st)（数学无损）；② 4 参 add 分母改链式两参（纯分母算术，非信号腿，闸文本扫描误计的规避）。两步均**逐位复现**原件指标（S 2.03/F 1.73/2Y 2.25/TO 0.1226/margin 14.79bp/DD 0.0503 全同）。混腿闸实测：kind=three_leg 放行，三问已答（insiders 双面 + analyst 修正确认）。

### B.0 WebDataScope 门
failed_ra_count=0 / failed_ppa_count=0 / checks.fail=[] / pass 9 项含 IS_LADDER_SHARPE、MATCHES_PYRAMID ⇒ 通过。

### B.2 逐年（get_alpha_yearly_stats，与原件同 PnL 流逐位一致）
2014-2023：1.55/2.92/1.40/1.87/2.76/2.45/1.73/1.16/2.43/2.06。**近 3 年 1.16/2.43/2.06 全正**（≥0.3 线全过）；
衰减比 2.06/2.03=1.01；近 3 年 CV=0.28（<0.40 PASS）；近 3 年 max/min=2.43/1.16=2.09（≤3 PASS）；平年 0。
软标记：2021 年 S 1.16 为十年最低（仍 >1.0），早年 2014/2016 偏弱——全历史信息项，不判。

### B.3 换手 × margin
TO 12.26%（<60% 线）、margin 14.79bp（>5bp 线）⇒ PASS。全期 DD 5.03%。

### B.4/B.5 相关性与池边际
- prod = **0.4489**（平台实测直返，直方图 [0.4,0.5)=2，远离 0.7 红线）⇒ PASS
- self = **0.3032**（本地池 20）⇒ PASS
- 池边际（performance_comparison）：ΔS +0.08 / ΔF +0.07 / ΔRet −0.04pp / ΔTO −0.06pp / ΔDD −0.08pp ⇒ **pass_offset**（成本同降补偿收益微降，方案 D v2 放行）

### Phase C 判定：**PASS**
- 硬标记 0；软标记 3：① 2021 单年 S 1.16 偏弱（近 3 年判定线下不阻断）② 早年 2014/2016 <1.6（全历史信息项）③ 2021 fitness 0.74（同年同因）。
- 经济可解释性（一句话）：内部人持仓动量强且信息新鲜（IR×days_from_last_change 反向）、重大交易金额集中度高、分析师净上调三类信号同向确认 → 看多。

### 塔与六维（与 VkNOJYnM 相同，同一 PnL 流）
- 塔：DEU/D1 insiders 1→2 + analyst 6→7（无新点亮，短板倍率 1.6x）；两件互相关 0.5982，提交本件后 VkNOJYnM/1YWnZ9rK 全族 self 封死（孪生效应），属预期代价。
- 六维：T1 +0.0143（4.6074→4.6217）、T2 +0.0136（软成本）；T3 +1（days_from_last_change 新算子）、T4 +6（significant_value_1–4 + est_12m_ebi_raised/lowerednum_4wks 新字段，硬收益全清单最强）；T5/T6 n/a。

---

## 2r5Lm3Jx（DEU/TOP500/D1，15:1x）—— 最终压缩版：中缀算术 + 去 group_zscore

> 演进链：VkNOJYnM(4腿 stack 拦) → wpolZRO6(链式 3 腿, distinct 10) → 1YWdZoxR(中缀, distinct 6) → **2r5Lm3Jx(中缀+去 group_zscore, distinct 5)**。用户两问驱动：①「六维里算子调用数多少，还能优化吗」②「add/subtract 合并、multiply/divide 数学简化？」——判定：算术链中缀化后每链计 1 次调用且**平台不再把算术算子计入 distinct**（genius_tiebreak 实测 5 个 distinct = 纯函数算子）；乘/除是交互项/比值语义不可去；group_zscore 与设置层 SUBINDUSTRY 中性化冗余，实测去除无损（S 不变）。

### 指标对比（vs 原件 VkNOJYnM）
S 2.03(同) / F 1.72(−0.01) / 2Y 2.23(−0.02) / TO 12.03%(−0.23pp) / margin 15.0bp(+0.2) / DD 5.44%(+0.41pp) / invest_S 1.82(+0.03)。均在线内。

### B.0 / B.2 / B.3
failed_ra=0 / failed_ppa=0 / checks.fail=[] ⇒ B.0 过。逐年 1.79/2.91/1.20/1.96/2.76/2.40/1.70/1.16/2.40/2.07：近 3 年全正、衰减比 1.02、CV 0.28、max/min 2.07 ⇒ 全 PASS。TO 12.0% × margin 15.0bp ⇒ PASS。

### B.4 / B.5
- prod = **0.4396** PASS（直方图 [0.4,0.5)=2，比原件 0.4489 更低）
- self = **0.3010** PASS（本地池 20）
- 池边际：ΔS +0.08 / ΔF +0.07 / ΔTO −0.07pp / ΔDD −0.08pp ⇒ pass_offset

### Phase C：**PASS**（软标记：2021 S 1.16 偏弱、2016 S 1.20 早年疲软——均为全历史信息项不判）

### 混腿闸
中缀写法令文本扫描 fail-open（kind=none）；结构上仍是 insiders 双面 + analyst 三腿语义，三问已在预检主动留痕。

### 六维（genius_tiebreak 实测）
distinct 算子 **5**（days_from_last_change/group_rank/ts_ir/ts_mean/vec_avg）：T1 +0.0010（几乎中性）、T2 +0.0136；T3 +1（days_from_last_change 新算子）、T4 +6（significant_value_1–4 + est_12m_ebi 双字段）；T5/T6 n/a。**六维软成本为全家族最低**（T1 增量 0.0010 vs VkNOJYnM 0.0143）。

---

## zqdRJWL8 战役收官件稳健性审计（DEU / D1 / SENTIMENT，2026-11-18 20:30）

候选族：`vRAvXvZb` / `2r5NxxxJ` / `KPgEpQWg` / `VkN3zO15`（PnL 逐位相同 3,970,317）＋ `VkN3el3M`（3,968,xxx，多 `winsorize`）。
归因数据取自 `get_alpha_yearly_stats`（IS 2014–2023，数据自 2019 起）、`get_alpha_pnl`、`get_alpha_details`、`check_correlation`、`performance_comparison`。

### Phase B/C 逐项

| 检查项 | 实测 | 判定 |
|---|---|---|
| WebDataScope failed | `failed_ra=0` / `failed_ppa=0`，`checks.fail=[]`，pending 仅 SELF/PROD/DATA_DIVERSITY/REGULAR_SUBMISSION | PASS |
| Recent-3yr Sharpe（主判定） | 2021 **1.35** / 2022 **1.24** / 2023 **3.67**，均值 **2.087** ≥ 1.58，三年全 >0.3 | PASS |
| **Recent-3yr CV_Sharpe** | **0.537**（0.40–0.60 带） | **CONDITIONAL** |
| 衰减比 | 3.67 / 1.63 = **2.25**（≥0.50） | PASS |
| 平年（<0.3） | **0** 个 | PASS |
| max/min Sharpe 比 | 3.67/1.24 = **2.96**（≤3） | PASS |
| 分年回撤 | 3.51 / 4.61 / 2.61 / 3.65 / 1.77 %，最大 4.61% < 2×均值 6.46% | PASS |
| Sub-universe | `LOW_SUB_UNIVERSE_SHARPE` PASS（sub S 1.12） | PASS |
| Margin @ turnover | **7.88 bp** @ 20.24% | PASS |
| 算子数（distinct） | `vRAvXvZb` **8** / `2r5NxxxJ` 7 / `VkN3zO15` 6 | 软标记 |
| 经济可解释性 | 一句话可写：「每域名摊薄后的关注度尾部集中度——单位域名上的分歧越高，后续超额越强」 | PASS |
| 池边际贡献 | DEU/D1 池 PnL 10,315,653 → 10,267,524（**−0.47%**），但 Sharpe 3.66 → **3.69** | 软标记（负 PnL / 正 Sharpe，稀释型分散） |
| 相关性 | self **0.2407**（池 21，top `d5a2aO7v`）／prod **0.5614**（直方图 `[0.6,0.7)`=0、`[0.7,0.8)`=0） | PASS |

### 结论

**`CONDITIONAL`**（唯一实质软标记＝近 3 年 CV 0.537，成因是 2023 年 Sharpe 3.67 单年尖峰，占全期 PnL **42.5%**）。
该尖峰是**整个族的共性**（`VkN3el3M` CV 0.507 同带），改参数无法消除——只能换信息机制才能改变年度分布。
硬闸全过、无 FAIL、无 REJECT 项，故 `submit_verdict` 不拦（fail-open），软标记须在提交前的三段式 description 中如实带上。

台账：`robustness_vRAvXvZb`、`robustness_2r5NxxxJ`（均 CONDITIONAL）。
