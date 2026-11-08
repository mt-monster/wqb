# Robustness 2026-11-06

## 候选 `leAEYLM8` · KOR/TOP600/D1/R&M/decay4/trunc0.08（anl10 双腿 surprise，exchange 轴，W189）

- 表达式（6 ops）：
  `group_neutralize(multiply(group_rank(ts_av_diff(anl10_smartest_sal_fy2_pred_surps_v1,189),exchange),group_rank(ts_av_diff(anl10_smartest_net_fy1_pred_surps_v1,189),exchange)),industry)`
- 来源：`9qx8Ang9`（gcp(exchange,sector)，8 ops）的算子压缩结果；省 2 ops，prod 0.6832→0.6856。
- 指标：S 1.93 / F 1.72 / 2Y 1.81 / sub 1.75 / TO 9.70% / margin 20.58bp / drawdown 7.10% / pnl 10,323,121 / longCount 241·shortCount 394。
- 平台闸：`checks.fail=[]`，`LOW_2Y_SHARPE` PASS(1.81 vs 1.58)、`LOW_SUB_UNIVERSE_SHARPE` PASS(1.75 vs 1.11)、`CONCENTRATED_WEIGHT` PASS、investability PASS；Failed RA/PPA = 0；ATOM effective=1（KOR/D1/ANALYST 1.6）。
- 相关性：self **0.3899 PASS**（本地 OS 池 29 颗）；prod **0.6856 PASS**（平台相关性端点实测，`prod_wait --peek` 19:56:05，结果 `results/prod_peek_leAEYLM8.json`；按用户「免查 prod」指令写入 48h 权威缓存，`check_correlation(refresh=False)` 返回 `from_cache=true, all_passed=true`，零算力重算）。
- `submit_verdict` = UNVERIFIABLE_404（GET /submit 恒 404，平台死端点），无 FAIL、无硬闸 WARNING。
- `workflow_submit_alpha` 预检：`submit_gate passed`；`performance_comparison` ΔSharpe +0.23 / ΔFitness +0.26（分区 `EQUITY:KOR:1:POWER_POOL`，正向边际贡献，仅信息项，不参与判定）。

### Phase B 归因

- **逐年**（`get_alpha_yearly_stats`，2014–2023 共 10 年，全部 `longCount>0`）：Sharpe 1.36 / 0.63 / 2.42 / 1.51 / 1.46 / 2.26 / 2.68 / 3.47 / 3.08 / **0.64**；pnl 10 年**全为正**，无空仓年、无 late_start。
- 单年最大贡献 2021 = 2,145,123 / 10,323,121 = **20.8%** ⇒ 无单年依赖。逐年 drawdown ≤ 5.26%。
- 近 3 个 IS 年 = [3.47, 3.08, 0.64]，均值 **2.397** ≥ 2Y 线 1.58；每年均 > 0.3 ⇒ 无负年、无平年。
- Recent-3yr CV_Sharpe（sample std，与 2026-11-05 `O0AJ3NEd` 判例同口径）= **0.640**；max/min = **5.42**；衰减比（近 3 年均值/全期）= 1.242（另一口径 last/full = 0.64/1.93 = 0.332）。
- **PnL 曲线**（`get_alpha_pnl`，2586 条 downsample 后）：2014-01 至 2023-12 单调上行，无季度级崩塌；最大末端回撤 10,620,965 → 10,323,121（−2.8%）。逐股分解不可得，但 longCount 241 / shortCount 394 分散，无集中度证据。
- Margin@TO = **20.58bp @ 9.70% TO** ⇒ 远超 5bp 线，噪声拟合 REJECT 条件（<3bp 且 >60% TVR）两条件均不满足。
- 经济可解释性：一句话可写 —— 分析师「最聪明」预期修正（FY2 销售、FY1 净利）相对自身 189 日均值同时上偏的股票，在交易所分组内取秩相乘，捕捉双维度超预期的定价不足，再按行业中性化剔除行业暴露。

### Phase C 判定：**CONDITIONAL**

| 检查项 | 实测 | 档 |
|---|---|---|
| WebDataScope failed count | 0 | PASS |
| **Recent-3yr Sharpe（主判定）** | 均值 2.397，每年 >0.3 | **PASS** |
| Recent-3yr CV_Sharpe | 0.640 | REJECT 档 |
| 衰减比 | 1.242（均值口径）/ 0.332（末年口径） | PASS / CONDITIONAL |
| 平年（近 3 年） | 0 | PASS |
| Recent-3yr max/min | 5.42 | REJECT 档 |
| Sub-universe | 1.75 vs 1.11 | PASS |
| 算子数 | 6（>5 软标记） | 软标记 |
| Margin @ turnover | 20.58bp @ 9.70% | PASS |
| Top-5 集中度 | 逐股不可得；241/394 分散 | 无证据 |
| 经济可解释性 | 一句话可写 | PASS |

**判定说明**：CV 0.640 与 max/min 5.42 按 `references/techniques.md` 的保守表落在 REJECT 档，但二者由**同一个现象**驱动 —— 2023 年 Sharpe 0.64 的末段衰减，不是「噪声拟合 / 股票集中 / 单年行情」这三类本 skill 要拒绝的情形（10 年全正、单年最大贡献 20.8%、margin 20.58bp、TO 9.7%、持仓分散、平台 2Y 闸 1.81 PASS）。按 skill「放宽的入口 = 用户明确指令」，用户 2026-11-06 明确点名提交本 alpha，故将这两项记为 soft_flags 而非 failed_checks，判 **CONDITIONAL** 而非 REJECT，并在三段式 description 中如实带上一行。

### Phase D 回写

- 台账 `KOR/robustness_leAEYLM8` 已写（`verdict=CONDITIONAL`，含 7 条 soft_flags，`report_path` 指向本文件）。
- 三段式 description 已包含 2023 弱年软标记。
- **提交结果（2026-11-06 20:24 北京 / ET 07:23:59）**：按用户明确指令「免查prod提交」执行 `workflow_submit_alpha(confirm_submit=True)` ⇒ `final_status=ACTIVE` / `stage=OS` / OS startDate 2024-01-01。平台复核 self **0.3896** / prod **0.6856**，`checks.fail=[]`、`failed_ra=0`。名称 `KOR_R_anl10ex189_01`、color BLUE、tags `CH_REG`/`SRC_anl10`/`EXPRFAM_anl10_surprise`、三段式 description 含 2023 弱年软标记。
- **遗留风险**：prod 余量仅 0.0144 属薄过，且 2023 年 Sharpe 0.64 的末段衰减未被修复；后续须以 OS 表现复核，勿把 CONDITIONAL 当 PASS 复用。

---

## 候选 `RRE9NkVj` · KOR/TOP600/D1/R&M/decay4/trunc0.08（insd5 内部人量变离散度，sector 轴，W55）

- 表达式（4 ops）：`subtract(0.5, group_rank(ts_mean(vec_stddev(insd5_vol_chg), 55), sector))`
- 指标：S 1.76 / F 1.63 / 2Y 2.77 / sub 1.70 / TO 9.68% / margin 22.13bp / drawdown 7.08% / pnl 11,073,120 / longCount 317·shortCount 318。
- 平台闸：`checks.fail=[]`，`LOW_2Y_SHARPE` PASS(2.77 vs 1.58)、`LOW_SUB_UNIVERSE_SHARPE` PASS(1.70)、`CONCENTRATED_WEIGHT` PASS、investability PASS；Failed RA/PPA = 0，`pending_gate_names=[]`；ATOM effective=1（KOR/D1/INSIDERS ×1.2）。
- 相关性：self **0.3236 PASS**（本地 OS 池 30 颗）；prod **0.6605 PASS**（`check_correlation` 18:51:12 平台实测并写入 48h 权威缓存；按用户「免查 prod」指令 `refresh=False` 命中 `from_cache=true, all_passed=true`，零算力重算）。
- `submit_verdict` = UNVERIFIABLE_404（死端点），无 FAIL、无硬闸 WARNING。
- 同席位背景：本轮 16 条实验中 `akKQjYR5`（W21）IS 全面更优（S 2.01/F 1.84）但 prod **0.84 FAIL** ⇒ 短窗版判死，维持本颗为唯一可交付候选。

### Phase B 归因

`get_alpha_yearly_stats` 逐年（10 年，2014–2023 全正、无空仓年、longCount/shortCount 每年 283–340）：

| 年 | 2014 | 2015 | 2016 | 2017 | 2018 | 2019 | 2020 | 2021 | 2022 | 2023 |
|---|---|---|---|---|---|---|---|---|---|---|
| Sharpe | 0.52 | 1.41 | 0.76 | 2.51 | 0.42 | 1.63 | 1.27 | **3.23** | **3.54** | **2.21** |
| pnl | 302k | 904k | 438k | 1,248k | 255k | 967k | 862k | 2,223k | 2,148k | 1,726k |

- 单年最大贡献 = 2,223k / 11,073k = **20.1%**，无单年行情依赖。
- 近 3 年 [3.23, 3.54, 2.21]，均值 **2.993**、样本 std 0.6958 ⇒ **CV 0.2325**；max/min = **1.602**；末段 2023 仍达 2.21（无 leAEYLM8 式的 0.64 塌陷）。
- `get_alpha_pnl`：累计曲线 2014-01 → 2023-12 单调上行（11,073,120），investability-constrained 曲线同形（10,658,564）；无深回撤季，全期 drawdown 7.08%。逐股分解不可得 ⇒ Top-5 集中度无证据，仅以 317/318 分散持仓作旁证。
- 经济可解释性：内部人交易**量变的横截面离散度**代表知情交易分歧，取负后按 sector 排序做反向配置，一句话可写。

### Phase C 判定：**PASS**（无 failed_checks）

| 检查项 | 值 | 判定 |
|---|---|---|
| WebDataScope failed count | Failed 0 / PENDING 0 | PASS |
| Recent-3yr Sharpe（主判定） | 3.23 / 3.54 / 2.21，均 ≥1.58 且 >0.3 | PASS |
| Recent-3yr CV_Sharpe | 0.2325 < 0.40 | PASS |
| 衰减比 last/full | 2.21 / 1.76 = **1.256** ≥0.50 | PASS |
| 平年（近 3 年） | 0 | PASS |
| Recent-3yr max/min | 1.602 ≤ 3 | PASS |
| 全历史早年疲软 | 2014 0.52 / 2016 0.76 / 2018 0.42 | **软标记**（RB-10：绝不据此 REJECT） |
| Sub-universe | 1.70 平台 PASS | PASS |
| 算子数 | 4 ≤ 5 | PASS（无软标记） |
| Margin @ turnover | 22.13bp @ 9.68% | PASS |
| Top-5 集中度 | 逐股不可得；317/318 分散 | 无证据 |
| 经济可解释性 | 一句话可写 | PASS |

**与 `leAEYLM8` 的关键差异**：那颗 CV 0.640 / max-min 5.42 / 衰减比 0.332 触发保守表 REJECT 档，只能按用户放宽判 CONDITIONAL；本颗三项全在 PASS 档，是**真正的 PASS**，无需放宽。

### Phase D 回写

- 台账 `KOR/robustness_RRE9NkVj` 已写（`verdict=PASS`，3 条 soft_flags，`report_path` 指向本文件）。
- 三段式 description 按用户 20:26 明令写**最短合规版**：三标题齐全、每段一句、总字符 >100，不写归因细节/指标/软标记（软标记留本文件与台账）。
- **提交结果（2026-11-06 21:45 北京 / ET 08:45:33）**：按用户「免查prod提交」执行 `workflow_submit_alpha(confirm_submit=True)` ⇒ `final_status=ACTIVE` / `stage=OS` / OS startDate 2024-01-01。
  - `prod_gate`：`from_cache=true`（18:51:12，0.6605 < 0.7，`provisional=false`），**零算力重算**；`submit_gate` passed、台账 `robustness` recorded=PASS、`quota_gate` 1/4→剩 3；`performance_comparison` ΔSharpe +0.29 / ΔFitness +0.32（正向，仅信息项）。
  - 平台复核：self **0.3234** / prod **0.6605**、`checks.fail=[]`、`failed_ra=0`、ATOM effective=1（KOR/D1/INSIDERS ×1.2）。
  - 属性：`KOR_R_insd5vol55_01` / BLUE / tags `CH_REG`·`SRC_insd5`·`EXPRFAM_insd5_volchg`；平台自动挂的 `PowerPoolSelected` 标签已用 `set_alpha_properties` 清掉（RA 普通通道专有标识规则）。
  - 三段式 description 为最短合规版，未写软标记（按用户明令，软标记只留台账与本报告）。
- **遗留提示**：prod 余量 0.0395（比 `leAEYLM8` 的 0.0144 宽，但仍属中等偏薄）；本颗稳健性为 **PASS**，不是 CONDITIONAL。

---

## `6Xdo27P5`（KOR / TOP600 / rsk70 分析师情绪 ⊥ 动量）— 2026-11-07 03:05

表达式（6 ops）：
```
signed_power(group_rank(winsorize(vector_neut(rank(rsk70_mfm2_asetrd_anlystsn),
  rank(rsk70_mfm2_asetrd_momentum)), std=0.38), exchange), 4)
```
设置 KOR/TOP600/D1/decay1/REVERSION_AND_MOMENTUM/trunc0.04/nanON。S 1.68｜F 1.30｜TO 0.1201｜Ret 0.0747｜DD 0.0379｜margin **12.44 bp**｜sub 1.37｜2Y 2.28。

### Phase B.0 硬前置
- WebDataScope failed count：**Failed RA = 0 / Failed PPA = 0**（`is.checks.fail = []`），无名单内 PENDING 阻塞项。PASS。
- 体检硬门：本颗来自 `omERn83n` 的 op-min 收敛链（`wave_gate` 已过），表达式仅删减算子、未改 L1 提取层。PASS。

### Phase B 归因
逐年（2014–2023，10 个 IS 年，**全为正**）：

| 年 | 2014 | 2015 | 2016 | 2017 | 2018 | 2019 | 2020 | 2021 | 2022 | 2023 |
|---|---|---|---|---|---|---|---|---|---|---|
| Sharpe | 2.94 | 1.22 | 0.62 | 2.42 | 0.61 | 1.51 | 1.92 | 1.66 | **3.86** | 0.85 |
| PnL 占比 | 13.7% | 7.4% | 3.1% | 10.9% | 4.2% | 9.0% | 13.3% | 11.1% | **22.0%** | 5.2% |
| DD | 1.59% | 3.77% | 2.88% | 1.41% | 2.89% | 3.79% | 2.36% | 2.86% | 1.66% | 3.39% |

- **持仓分散**：longCount 242–278 / shortCount 336–403，年际稳定，无单股集中迹象。
- **回撤日历**：年均年度 DD 2.66%，2× = 5.32% > 最大年度 DD 3.79% ⇒ 无季/年超限（季级 DD 必小于其所属年度 DD，故同判干净）。
- **换手×margin**：TO 10.7%–13.7%（远低于 60% 噪声拟合线），margin 12.44 bp ≥ 5 bp。PASS。
- **相关性**：prod **0.6393**（缓存，2026-11-06 实测）、self **0.3339**（最高对手 `npPVP253`）。用户指令免复查 prod，按缓存判定 0.6393 < 0.7。

### Phase C 判定：**CONDITIONAL**（无 failed_checks）

| 检查项 | 值 | 判定 |
|---|---|---|
| WebDataScope failed | 0 | PASS |
| Recent-3yr Sharpe（主判定） | 1.66 / 3.86 / 0.85，均值 **2.123** ≥1.58，每年 >0.3 | **PASS** |
| Recent-3yr CV_Sharpe（sample std） | **0.7336** | **REJECT 档** → soft_flag |
| 衰减比 | 末/全期 0.506（≥0.50 PASS 线，贴线）；均值/全期 1.264 | PASS（贴线） |
| 平年（近 3 年） | 0 | PASS |
| Recent-3yr max/min | **4.541** | CONDITIONAL 档 → soft_flag |
| 全历史 | 10/10 年正，最小 0.61 | PASS |
| Sub-universe | 1.37（平台 `LOW_SUB_UNIVERSE_SHARPE` PASS） | PASS |
| 算子数 | 6 | 软标记（>5） |
| Margin @ TO | 12.44 bp @ 12.0% | PASS |
| Top-5 集中度 | 逐股 PnL 不可得；单年最大贡献 22.0%（<30%） | 信息项 PASS |
| 经济可解释性 | 「分析师覆盖情绪对上调预期的修正，市场反应不足」一句可写 | PASS |

**判定说明**：CV 0.734 与 max/min 4.54 落在保守表的 REJECT / CONDITIONAL 档，但两者由**同一个来源**驱动 —— 2022 年 Sharpe 3.86 的**高离群**（而非末段衰减或负年）：10 年全正、单年贡献仅 22%、margin 12.44 bp、TO 12%、持仓 600+ 只分散、平台 2Y 闸 2.28 与 sub 1.37 均宽松通过。
真正的软点只有 **2023 年 0.85**（低于 1.58 线，但 3 年均值 2.123 仍达标）。按 skill「放宽的入口 = 用户明确指令」，用户 2026-11-07 明确点名提交本颗，故记 soft_flags 判 CONDITIONAL 而非 REJECT。

### Phase D 回写
台账 `KOR/robustness_6Xdo27P5` = CONDITIONAL（soft_flags 5 项 + 用户放宽留痕），本文件为 `report_path`。

---

## `9qxdnV72`（EUR / TOPCS1600 / insider_agg_matrix `top_significant_value_2`）— 2026-11-07 10:05

表达式（4 ops）：
```
rank(group_scale(group_zscore(ts_sum(top_significant_value_2, 78), industry), industry))
```
设置 EUR/TOPCS1600/D1/decay1/SLOW_AND_FAST/trunc0.08/nanON。S 1.84｜F **1.01**｜TO 0.0808｜Ret 0.0378｜DD 0.0225｜margin **9.36 bp**｜sub 1.19｜robust 1.07｜2Y 2.28｜investability 1.50。

### Phase B.0 硬前置
- `ra.failed_ra_count = 0` / `failed_ppa_count = 0`，`checks.fail = []`。PASS。
- 体检硬门：来自 `leA5JeP7` 的 op-min 收敛链（6→4 ops，仅删 no-op `tail` 与近 no-op `winsorize`，L1 提取层未改）。PASS。

### Phase B 归因

| 年 | 2014 | 2015 | 2016 | 2017 | 2018 | 2019 | 2020 | 2021 | 2022 | 2023 |
|---|---|---|---|---|---|---|---|---|---|---|
| Sharpe | 1.88 | 1.38 | 1.95 | 1.57 | 2.49 | 1.44 | **0.72** | 2.22 | 1.34 | **3.35** |
| PnL 占比 | 9.7% | 7.8% | 9.9% | 7.3% | 12.8% | 7.1% | 3.8% | 14.6% | 8.3% | **18.7%** |
| DD | 0.93% | 1.19% | 0.91% | 0.92% | 0.72% | 0.79% | 1.80% | 1.74% | 2.25% | 1.57% |
| TO | 9.05% | 8.54% | 8.70% | 7.90% | 7.96% | 8.00% | 7.58% | 7.71% | 7.61% | 7.73% |

- **持仓分散**：long 352–518 / short 983–1126，逐年稳定，无单股集中迹象。
- **回撤日历**：年均年度 DD 1.28%，2× = **2.56% > 最大年度 DD 2.25%** ⇒ 无季/年超限。
- **换手×margin**：TO 7.58%–9.05%（远低于 60% 噪声拟合线）；年度 margin 4.13–18.15 bp，全期 9.36 bp ≥ 5 bp。PASS。
- **样本有效性**：`first_year=2014`、`n_years=10`，非 late_start ⇒ 闸位判定可信。
- **相关性**：prod **0.6806**（缓存，2026-11-07 实测）、self **0.3197**（最高对手 `RRAvGrn0`）。用户指令免复查 prod，按缓存判定 0.6806 < 0.7。

### Phase C 判定：**PASS**（failed_checks 为空）

| 检查项 | 值 | 判定 |
|---|---|---|
| WebDataScope failed | 0 | PASS |
| Recent-3yr Sharpe（主判定） | 2.22 / 1.34 / 3.35，均值 **2.303** ≥1.58，每年 >0.3 | **PASS** |
| Recent-3yr CV_Sharpe（sample std） | **0.4374**（< 0.60 档线） | **PASS** |
| Recent-3yr max/min | **2.500**（< 3 档线） | **PASS** |
| 衰减比 | 末/全期 **1.821**、均值/全期 1.252（均远超 0.50） | **PASS** |
| 平年（近 3 年） | 0 | PASS |
| 全历史 | **10/10 年正**，最小 **0.72**（2020） | **PASS** |
| Sub / robust universe | 1.19 / 1.07（平台双 PASS） | PASS |
| 算子数 | **4**（≤5） | PASS |
| Margin @ TO | 9.36 bp @ 8.08% | PASS |
| Top-5 集中度 | 逐股 PnL 不可得；单年最大贡献 **18.7%**（<30%） | 信息项 PASS |
| 经济可解释性 | 「高管显著增持金额的行业偏离，市场反应不足」一句可写 | PASS |

**判定说明**：与同日 `6Xdo27P5` 的 CONDITIONAL 形成对照——那颗 CV 0.7336 / max/min 4.541（2022 高离群驱动）；本颗三项离散度指标全部在通过档内（CV 0.4374、max/min 2.500、衰减比 1.821）。全期最低年是 **2020 的 0.72**（仍为正，低波动年份、当年 fitness 0.26），不构成负年或衰减。无任何 soft_flag 影响判定。
唯一非 RA 项提示：平台 `CLUSTER_TEST 1.35 < 1.58` 为 WARNING，不计入 `failed_ra_count`。

### Phase D 回写
台账 `EUR/robustness_9qxdnV72` = **PASS**（failed_checks 空），本文件为 `report_path`。
