# 稳健性闸逐候选报告（append-only，每日一份）

> 阈值与三态定义见 skill `brain-alpha-robustness` Phase C；本文件只记事实与判定，不改阈值。
> 台账事实源：`ledger_kv` 键 `robustness_<alpha_id>`（本文件是给人读的审计痕迹）。

---

## E5RGoOX1 — USA / TOP3000 / D1 / STATISTICAL / decay 250

- 表达式：`group_rank(ts_zscore(mean_estimate_targetprice_annual12_tribes,175),subindustry)`
- 来源：`submit_ready` 队列 READY（`added_at=2026-10-08`，`verified_at=2026-10-23T05:46:59`）
- 顶层指标：S **1.81** / F 1.09 / TO 0.0619 / RET 4.50% / DD 8.62% / 2Y 1.65 / SUB 0.86 / margin 14.55 bp
- 平台 checks：`failed_ra_count = 0`；warning = `CLUSTER_TEST 0.52 (limit 1.58)` / `MATCHES_THEMES` / `OSMOSIS_ALLOCATION`
- 相关性（队列值，375 h 前）：prod 0.6869 / self 0.4163
- 塔：`USA/D1/ANALYST` × 1.2

### 逐年（`get_alpha_yearly_stats`）

| 年 | 2014 | 2015 | 2016 | 2017 | 2018 | 2019 | 2020 | 2021 | 2022 | 2023 |
|---|---|---|---|---|---|---|---|---|---|---|
| Sharpe | 3.73 | 4.80 | 2.58 | 2.26 | 2.20 | 1.47 | **-1.68** | 2.08 | 2.69 | **0.39** |
| Returns | 6.3% | 9.6% | 4.5% | 4.3% | 4.9% | 3.2% | -5.3% | 7.7% | 7.9% | 1.0% |

### Phase C 判定

| 检查项 | 实测 | 判定 |
|---|---|---|
| WebDataScope failed count | 0，无 PENDING | PASS |
| Recent-3yr Sharpe（2021–2023 均值） | 1.72 ≥ 1.58，且三年均 > 0.3 | PASS |
| Recent-3yr CV_Sharpe | 0.57 | CONDITIONAL（0.40–0.60） |
| **衰减比** = 2023 / 全期 | **0.39 / 1.81 = 0.215** | **REJECT（< 0.30）** |
| 平年（近 3 年） | 0 | PASS |
| Recent-3yr max/min | 2.69 / 0.39 = 6.9 | **REJECT（> 5）** |
| 全历史早年疲软 | 2020 整年 -1.68（窗口外） | 软标记 |
| Sub-universe | 0.86，平台 `LOW_SUB_UNIVERSE_SHARPE` PASS | PASS |
| 算子数 | 3（`group_rank`/`ts_zscore`/字段） | PASS |
| Margin @ turnover | 14.55 bp @ 6.2% | PASS |
| 经济可解释性 | 分析师目标价修正（12 个月）的横截面动量 | PASS |

**结论：REJECT。** 硬标记两条：衰减比 0.215（2023 年 Sharpe 仅 0.39，收益 1.0%）、近 3 年
max/min 6.9。全期 1.81 由 2014–2018（S 2.2–4.8）撑起，2019 起单调走弱，2020 整年负收益。
这是分析师修正族被拥挤后的典型衰减形态，不是单年噪声——2023 的弱是连续第 5 年下行的一环。

处置：台账写 `REJECT`，`submit_verdict` 将 BLOCKED（`ROBUSTNESS_REJECT`）。不进提交队列。
若用户要求保留，唯一合规入口是用户明确指令放宽「衰减比」并留痕 `soft_flags`；不自行放宽。

---

## YPx89bQJ — USA / TOP2000 / D1 / STATISTICAL / decay 0（ai_equity_alpha · 波 99c）

- 表达式：`ts_decay_linear(group_rank(ts_zscore(ts_backfill(subtract(vec_avg(predicted_earnings_surprise_2), vec_avg(predicted_earnings_surprise_3)), 252), 252), subindustry), 5)`
- 来源：波 99c（multisim `3MggBxa524Uya6UjIrSUc1X`）SUB 单闸修复批的 subindustry 臂
- 顶层指标：S **2.19** / F 1.16 / TO 0.1569 / RET 4.39% / DD 2.92% / 2Y 1.91 / SUB 1.24（limit 1.19）/ margin **5.6 bp** / longCount 1032 / shortCount 1047
- `is.checks`：failed 0（`failed_ra_count=0`、`failed_ppa_count=0`）；warning = CLUSTER_TEST 1.04（limit 1.58）、MATCHES_THEMES、OSMOSIS_ALLOCATION；pending = SELF_CORRELATION / DATA_DIVERSITY / PROD_CORRELATION / REGULAR_SUBMISSION / POWER_POOL_CORRELATION / MATCHES_THEMES
- pyramid：`USA/D1/MODEL` × 1.3

### WebDataScope / 体检

| 检查项 | 实测 | 判定 |
|---|---|---|
| Failed RA | 0，无 PENDING | PASS |
| 字段体检 | 波 99 起同壳（`vec_avg` 包 VECTOR），99c 未触型别混用 | PASS |

### 逐年（`get_alpha_yearly_stats`）

| 年 | 2014 | 2015 | 2016 | 2017 | 2018 | 2019 | 2020 | 2021 | 2022 | 2023 |
|---|---|---|---|---|---|---|---|---|---|---|
| Sharpe | 3.06 | 3.19 | 2.05 | 2.61 | 2.98 | 2.78 | 1.34 | 1.49 | 2.96 | 0.91 |

### Phase C 判定

| 检查项 | 实测 | 判定 |
|---|---|---|
| Recent-3yr Sharpe（2021–2023 均值） | **1.79** ≥ 1.58，且三年均 > 0.3 | PASS |
| Recent-3yr CV_Sharpe | 0.48（0.40–0.60） | CONDITIONAL |
| 衰减比 = 2023 / 全期 | 0.91 / 2.19 = **0.416**（0.30–0.50） | CONDITIONAL |
| 平年（近 3 年） | 0 | PASS |
| Recent-3yr max/min | 2.96 / 0.91 = **3.25**（3–5） | CONDITIONAL |
| 全历史早年疲软 | 无（最早 2014 起即 3.06） | PASS |
| Sub-universe | 1.24 vs limit 1.19 | PASS（余量 0.05） |
| 算子数 | 7 个调用点（≤8） | 软标记（>5） |
| Margin @ turnover | **5.6 bp** @ 15.69% TVR | PASS（≥5 bp，余量薄） |
| Top-5 个股集中度 | 无逐股 PnL，未评估 | 未测 |
| 经济可解释性 | 「同一模型两代对每股盈利意外的预测分歧 → 分析师预期修正未充分定价」 | PASS |

### 风险与相关性（`check_correlation(refresh=True)`）

| 端口 | 实测 | 判定 |
|---|---|---|
| PROD `max` | **0.6803**（limit 0.7；直方图 [0.6,0.7) 桶 n=1，即该条即本人） | PASS（余量仅 0.020） |
| SELF `max` | 0.2812（对 `O08EjLVp`） | PASS |

### 回撤日历（`get_alpha_pnl`，2494 个交易日）

- 全期最大回撤 291,712（2020-07-29），占期末累计 PnL 4,386,566 的 6.6%
- 季度内最大回撤均值 73,627；**超 2 倍均值的季度 3 个**：2020Q2（182,621，当季 −128,328）、2021Q2（181,906，当季 −35,373）、2023Q3（168,128，当季 −103,027）
- 年度 PnL 全为正（10/10），最弱 2023（186,818）

**结论：CONDITIONAL（无硬标记）。** 三条软标记都落在 CONDITIONAL 档（CV 0.48 / 衰减比 0.416 / max-min 3.25），
没有触发任何 REJECT 条件；但 2023 年 S 0.91、收益显著衰减，且 prod 0.6803 距 0.70 仅 0.020、
margin 5.6 bp 偏薄。处置：进 `submit_ready` 候选，**提交前需用户确认**；
若用户要求先修衰减，优先候选是 `group_zscore` 之外的平滑轴（99c 已证 `ts_mean(22)` 与 `group_zscore` 均崩），
故修复空间有限，不建议为抬 2023 而破坏当前全闸状态。

---

## 波 100（ai_equity_alpha · 未测族分歧腿，TOP2000 / D1 / STATISTICAL / decay 0）

波次 `4abGpEr4iqb1ldIsZY3CD`，10 臂全部收批（`harvest_multisim_results`：upserted 10，wave 100 暂定 PASS）。
统一壳：`ts_decay_linear(group_rank(ts_zscore(ts_backfill(subtract(vec_avg(<A>), vec_avg(<B>)), 252), 252), subindustry), 5)`
——同字段不同 vintage 的**分歧腿**（本质 = 模型版本修正速率），非混信号。

四臂 `failed_ra_count == 0` 进稳健链。年度 Sharpe 与 Phase C 计算如下（近 3 年 = 2021/2022/2023）：

| alpha | 字段对 | 年度 Sharpe（2014→2023） | 近 3 年均值 | CV | 衰减比 | max/min | margin | 2Y | SUB / limit |
|---|---|---|---|---|---|---|---|---|---|
| `npAmlRr8` | accounting_forensics_factor − _6 | 2.86 2.99 3.93 2.89 3.49 1.82 1.95 3.61 1.53 2.54 | **2.56** | 0.332 | 0.988 | 2.36 | 6.48 bp | 2.00 | 1.75 / 1.40 |
| `QPYOAk6w` | intrinsic_valuation_estimate_3 − _91 | 2.52 4.22 4.15 1.42 0.61 2.11 2.29 2.74 1.65 2.30 | **2.23** | 0.201 | 0.987 | 1.66 | 4.38 bp | 1.94 | 1.58 / 1.28 |
| `58jr102k` | financing_structure_analysis_3 − _4 | 1.90 3.33 4.32 2.50 0.45 1.12 2.69 2.55 1.42 2.78 | **2.25** | 0.264 | 1.23 | 1.96 | 6.96 bp | 2.06 | 1.41 / 1.24 |
| `N1eLGm2e` | balance_sheet_trend_metric_7 − _51 | 3.31 3.18 3.11 2.01 0.32 1.57 2.89 2.85 2.46 1.84 | **2.38** | 0.175 | 0.80 | 1.55 | 5.70 bp | 2.14 | 1.28 / 1.26 |

**Phase C 四臂全过**（近 3 年均值 ≥ 1.58、CV < 0.40、衰减比 ≥ 0.50、max-min ≤ 3、平年 0）。
全历史弱年仅 2018（0.61 / 0.61 / 0.45 / 0.32），按近窗制度只记软标记，不据此 REJECT。

### prod / self 终判（`check_correlation(refresh=True)`）

| alpha | PROD max | 判定 | SELF max | 判定 |
|---|---|---|---|---|
| `npAmlRr8` | **0.7946** | FAIL（≥0.75 ⇒ D0-P dead_end） | —（prod 已死不探） | — |
| `QPYOAk6w` | **0.7761** | FAIL（≥0.75 ⇒ D0-P dead_end） | — | — |
| `58jr102k` | **0.6818** | PASS（余量 0.018；直方图 [0.6,0.7) n=12） | **0.2329**（对 `O08EjLVp`） | PASS |
| `N1eLGm2e` | **0.7663** | FAIL（≥0.75 ⇒ D0-P dead_end） | — | — |

### 回撤日历（2494 个交易日，`recordsets/pnl`）

- `npAmlRr8`：maxDD 230,400（2023-12-27，占期末 3.8%）；季度 DD 超 2× 均值 3 个（2023Q4 3.0× / 2022Q4 2.5× / 2022Q2 2.5×）；年度 PnL 10/10 为正
- `QPYOAk6w`：maxDD 190,294（2018-10-16，3.9%）；超 2× 均值 2 个（2021Q2 2.3× / 2020Q3 2.1×）；年度 PnL 10/10 为正
- `58jr102k`：maxDD 179,903（2018-11-15，4.1%）；超 2× 均值 3 个（2022Q4 2.3× / 2021Q2 2.3× / 2019Q3 2.0×）；年度 PnL 10/10 为正
- `N1eLGm2e`：maxDD 229,667（2018-10-01，5.0%）；超 2× 均值 4 个（2023Q2 2.6× / 2018Q3 2.4× / 2020Q3 2.3× / 2022Q4 2.1×）；年度 PnL 10/10 为正

### 组内互相关（`compute_mutual_correlation`，4 年日收益，含 `YPx89bQJ`）

`YPx89bQJ` 与四条分歧腿全部低相关（0.07 / 0.07 / −0.03 / 0.19）；分歧腿彼此 0.39–0.67，
最大对 `N1eLGm2e`×`j2eoJRMO` 0.6817。**阈值 0.5 下的最大互相容子集 = 4 条**
（`YPx89bQJ`, `npAmlRr8`, `58jr102k`, `j2eoJRMO`）——与 prod 结论方向一致：这一族只能出极少数代表。

### 结论

- **`58jr102k`：PASS**（Phase C 全过 + prod 0.6818 + self 0.2329）→ 第 7 颗可提交候选，进 `submit_ready`；**提交需用户明确确认**。
- **`npAmlRr8` / `QPYOAk6w` / `N1eLGm2e`：REJECT（prod 家族性饱和 0.766–0.795）**。
  三臂 IS 全闸 + 稳健闸都过得漂亮，卡点不在信号质量而在**持仓与生产池重叠**；
  按 D0-P 记 dead_end，不再为这组字段对换平滑轴（换 `hump`/`decay` 只改时序、不改持仓，只会把 self 推高）。
- 家族结论：`ai_equity_alpha` 的 vintage-disagreement 壳在 TOP2000/STATISTICAL 下 prod 呈**双峰**——
  `financing_structure_analysis_3−4`（0.68）与其余字段对（0.77–0.79）分属两簇。后续同壳新字段对**先探 prod 再投稳健链**，
  避免把配额烧在必死臂上。

---

## `zqrgna91`（USA/TOP2000/D1 · `ai_equity_alpha` · `buzz_intensity_score_2 − buzz_intensity_score_11`）

- 表达式：`signed_power(ts_decay_linear(group_rank(ts_zscore(ts_backfill(subtract(vec_avg(buzz_intensity_score_2), vec_avg(buzz_intensity_score_11)), 252), 252), market), 5), 0.8)`
- 设置：USA / TOP2000 / D1 / decay 0 / STATISTICAL / trunc 0.08 / **nanHandling ON**；`nanHandling` 不显式传 ON 时该 VECTOR 族会塌陷（画像 §12 铁律）。
- 平台指标：S **2.67** / F **1.66** / 2Y **1.68** / SUB **1.47** / TVR **15.8%** / MDD 2.19% / margin **7.74 bp**；`failed_ra_count = 0`。
- 相关性（`check_correlation(refresh=True)`）：PROD max **0.6877**（PASS，余量 0.0123）；SELF max **0.2866**（pool 3 / OS pool 6，PASS）。

### 逐年 Sharpe（IS 2014–2023）

| 2014 | 2015 | 2016 | 2017 | 2018 | 2019 | 2020 | 2021 | 2022 | 2023 |
|---|---|---|---|---|---|---|---|---|---|
| 3.71 | 3.59 | 4.21 | 1.68 | 2.02 | 3.53 | 2.64 | 3.11 | 1.81 | 1.64 |

年度 PnL 10/10 为正；逐年 fitness 2014–2021 ≥1.87，2022 0.98 / 2023 0.77。

### Phase C 判定（近 3 年口径：2021–2023）

| 检查 | 读数 | 判定 |
|---|---|---|
| Recent-3yr 均值 Sharpe | **2.187**（≥1.58） | PASS |
| 近 3 年逐年 > 0.3 | 3.11 / 1.81 / 1.64 | PASS（0 平年） |
| CV_Sharpe（近 3 年） | **0.300**（<0.40） | PASS |
| 衰减比 last/full | 1.64 / 2.67 = **0.614**（≥0.50） | PASS |
| max/min（近 3 年） | 3.11 / 1.64 = **1.90**（≤3） | PASS |
| Sub-universe | 平台 `LOW_SUB_UNIVERSE_SHARPE` PASS（1.47 vs limit 1.34） | PASS |
| Margin @ turnover | 7.74 bp @ TVR 15.8% | PASS |
| 经济可解释性 | 同一「关注度强度」指标两个 vintage 的分歧 = 市场关注度的**增量修正**，做多关注度被低估者、做空被高估者 | PASS |
| 算子数 | 7（软标记线 >5） | 软标记 |

### 回撤日历（2494 个交易日，`recordsets/pnl`）

- 全期 maxDD **219,423**（占 book **1.10%**）；40 个季度平均 qDD 74,241。
- 超出 2× 均值的季度 2 个：**2021Q2（2.23×，0.83%）**、**2020Q3（2.23×，0.83%）** —— 绝对幅度极小，记软标记。
- 年度 PnL 单调递增（2014 662k → 2023 6,118k），无年度亏损。
- Top-5 个股集中度：平台未提供逐股 PnL 分解，**未计算**（技能允许「逐股 PnL 可得时」才查）。

### 判定

**PASS**（软标记：21Q2/20Q3 季度回撤 2.23×；2017/2023 年度 Sharpe 贴线 1.68/1.64；算子 7 个；平台 `CLUSTER_TEST` warning 1.29）。
prod 余量仅 0.0123，属该族 prod 高位簇（直方图 [0.6,0.7) 内），**提交顺序放在余量更大的候选之后**。
台账 `robustness_zqrgna91` 已写 PASS；**提交需用户明确确认**。

## `j2eoKKEj`（USA/TOP2000/D1 · `ai_equity_alpha` · `earnings_per_share_growth_metric_2 − _3`）

- 表达式：`signed_power(ts_decay_linear(group_rank(ts_zscore(ts_backfill(subtract(vec_avg(earnings_per_share_growth_metric_2), vec_avg(earnings_per_share_growth_metric_3)), 252), 252), market), 5), 0.8)`
- 设置：USA / TOP2000 / D1 / decay 0 / STATISTICAL / trunc 0.08 / **nanHandling ON**；`nanHandling` 不显式传 ON 时该 VECTOR 族会塌陷（画像 §12 铁律）。
- 平台指标：S **2.58** / F **1.63** / 2Y **2.17** / SUB **1.38**（limit 1.36）/ TVR **17.57%** / MDD 3.16% / margin **7.96 bp**；`failed_ra_count = 0`。
- 相关性（`check_correlation(refresh=True)`）：PROD max **0.6434**（PASS，余量 **0.0566**，为全部候选中最宽）/ SELF max **0.2751**（对 `O08EjLVp`；pool 3 / OS pool 6，PASS）。

### 逐年 Sharpe（IS 2014–2023）

| 2014 | 2015 | 2016 | 2017 | 2018 | 2019 | 2020 | 2021 | 2022 | 2023 |
|---|---|---|---|---|---|---|---|---|---|
| 2.91 | 3.98 | 3.26 | 2.75 | 5.02 | **0.62** | 2.91 | 1.95 | 2.86 | 1.47 |

### Phase C 反过拟合闸（近窗制度：最近 3 个 IS 年）

| 检查项 | 读数 | 判定 |
|---|---|---|
| Recent-3yr 均值 Sharpe（2021–2023） | **2.093** ≥ 1.58 | PASS |
| 近 3 年每年为正（>0.3） | 1.95 / 2.86 / 1.47 | PASS |
| Recent-3yr CV_Sharpe | **0.275** < 0.40 | PASS |
| 衰减比（2023 / 全期） | **0.570** ≥ 0.50 | PASS |
| Recent-3yr max/min | **1.95** ≤ 3 | PASS |
| 平年数（\|S\|<0.3） | 0 | PASS |
| 全历史早年疲软 | 2019 S **0.62**（10 年中唯一 <1） | 软标记，**不据此 REJECT** |
| Margin @ turnover | 7.96 bp @ 17.57% TVR | PASS |
| 算子数 | 7（vec_avg×2 计 2） | 软标记（>5） |
| 经济可解释性 | 「EPS 增长模型两代版本的增速分歧 = 增长预期修正速率」一句话可写 | PASS |

### PnL 与回撤归因（`recordsets/pnl`，2494 个交易日）

- 全期 maxDD **315,891**（1.58% book），发生在 **2020-04-03**；终值 PnL 7,003,966。
- 季度回撤：40 季均值 98,790；超 2× 均值 2 季 —— **2023Q4** 276,304（1.38% book，2.80×）、**2021Q2** 214,738（1.07%，2.17×）。
- 季度回撤 top5：2023Q4 / 2021Q2 / 2022Q2 / 2020Q3 / 2021Q1（均 ≤1.38% book，无单季结构性塌陷）。
- 年度 PnL **10/10 为正**：575k / 901k / 675k / 531k / 1,073k / 142k / 977k / 772k / 952k / 406k。
- Top-5 个股集中度：平台未提供逐股 PnL，未计算（非 PASS 依据）。

### 判定

**PASS**。近 3 年三项硬指标（均值 / CV / 衰减比）全部过线，无 REJECT 项。软标记见台账 `soft_flags`：
2019 为全历史弱年（近窗制度下只留痕）、2023Q4 与 2021Q2 单季回撤偏大但绝对幅度 <1.4% book、2023 年内衰减、CLUSTER_TEST 1.34、SUB 余量 0.02。

台账 `robustness_j2eoKKEj` 已写 PASS；**提交需用户明确确认**。

---

## `N1eLE1de` — ai_equity 信用风险模型两代评分分歧（第 10 颗，2026-10-23 复核）

- 数据集 / 塔：`ai_equity_alpha`（dataset_id 294，MODEL）/ `USA/D1/MODEL`（×1.3）
- 核心字段：`credit_risk_model_score_5` − `credit_risk_model_score_7`（两代信用风险模型评分分歧 = 信用基本面重估速率）
- 表达式：`ts_decay_linear(group_rank(ts_zscore(ts_backfill(subtract(vec_avg(credit_risk_model_score_5), vec_avg(credit_risk_model_score_7)), 252), 252), subindustry), 5)`
- 设置：USA / TOP2000 / D1 / decay 0 / STATISTICAL / trunc 0.08 / VERIFY / **nanHandling ON**；2014-01-01→2023-12-31。
- 平台指标：S **2.63** / F **1.54** / 2Y **2.07** / SUB **1.66**（limit 1.24，比值 0.631 远高于 0.527 门槛）/ TVR **14.09%** / RET 4.86% / ret-drawdown 2.41% / margin **6.89 bp** / long 1032 · short 1048。
- RA 闸：`failed_ra_count = 0`；warning 仅 CLUSTER_TEST 1.07（limit 1.58）、MATCHES_THEMES、OSMOSIS_ALLOCATION。
- 相关性（`check_correlation(refresh=True)`）：PROD max **0.6916**（PASS，余量 **0.0084** —— 全部候选最薄）/ SELF max **0.2753**（对 `O08EjLVp`；pool 3 / OS pool 6）。

### 逐年 Sharpe（IS 2014–2023）

| 2014 | 2015 | 2016 | 2017 | 2018 | 2019 | 2020 | 2021 | 2022 | 2023 |
|---|---|---|---|---|---|---|---|---|---|
| 4.26 | 3.12 | 3.44 | 1.92 | 1.86 | 1.07 | 4.29 | 2.50 | 2.83 | 1.07 |

### Phase C 反过拟合闸（近窗制度：最近 3 个 IS 年）

| 检查项 | 读数 | 判定 |
|---|---|---|
| Recent-3yr 均值 Sharpe（2021–2023） | **2.133** ≥ 1.58 | PASS |
| 近 3 年每年为正（>0.3） | 2.50 / 2.83 / 1.07 | PASS |
| Recent-3yr CV_Sharpe | **0.358** < 0.40 | PASS |
| 衰减比（2023 / 全期） | **0.407**（1.07 / 2.63），落 0.30–0.50 | **CONDITIONAL** |
| Recent-3yr max/min | **2.65** ≤ 3 | PASS |
| 平年数（\|S\|<0.3） | 0 | PASS |
| 全历史疲软 | 2019 与 2023 同为 1.07（非单调衰减，是双年周期性） | 软标记 |
| Margin @ turnover | 6.89 bp @ 14.09% TVR | PASS |
| 算子数 | 7（vec_avg×2 计 2） | 软标记（>5） |
| 经济可解释性 | 「两代信用风险模型对同一主体的评分分歧 = 信用重估速率」一句话可写 | PASS |

### PnL 与回撤归因（`recordsets/pnl`，2494 个交易日）

- 全期终值 PnL **4,831,044**；maxDD **240,731（1.20% book）**，发生在 **2022-10-24**。
- 季度回撤：40 季均值 67,706；超 2× 均值 4 季 —— 2021Q3 182,204（0.91%）、2022Q4 149,141（0.75%）、2019Q3 145,482（0.73%）、2023Q1 138,507（0.69%），**绝对幅度全部 <1% book**。
- 年度 PnL **10/10 为正**：676k / 494k / 536k / 285k / 314k / 184k / 953k / 577k / 624k / 188k。
- Top-5 个股集中度：平台未提供逐股 PnL，未计算（非 PASS 依据）。

### 判定

**CONDITIONAL**（唯一条件项 = 衰减比 0.407）。其余硬指标全过，无 REJECT 项。

**归因（不当作字段对失效，也不当作可忽略）**：2023 年 S 1.07 与 2019 年 1.07 完全同值，且中间三年
（2020 4.29 / 2021 2.50 / 2022 2.83）强劲 ⇒ 形态是**双年周期性弱势**而非单调衰减。同数据集另两条分歧腿
（`YPx89bQJ` 2023 S 0.91、`j2eoKKEj` 2023 S 1.47）2023 年同样显著弱于前两年 ⇒ 判为
**MODEL 数据集在 2023 年的制度性弱势**（模型版本更新节奏变慢 ⇒ 分歧信号衰减），不是本字段对特有的崩塌。

**两条风险须在用户确认前交代**：① PROD 0.6916 距 0.70 仅 **0.0084**，是全部 10 颗里余量最薄的，且 prod 只向上漂——
本轮虽过闸，后续平台池变化即可能翻越；② 衰减比 0.407 ⇒ 若按纪律先 repair 再重审，可试的轴是
**加 `signed_power(...,0.8)` 外包裹 + 分组轴 `subindustry`→`market`**（wave 102 已验证该组合在 EPS 增长腿把
SUB 比值从 0.493 抬到 0.535，同时对持仓有实质改变、可重测 prod），代价是必须重测 prod 与 self。

台账 `robustness_N1eLE1de` 已写 CONDITIONAL；**提交需用户明确确认**。

---

## `0mjk2ZQv` — institutions6 机构持有家数残差反转（IND 10 颗配套，2026-10-23 复核）

- 数据集 / 塔：`institutions6` / `IND/D1/INSTITUTIONS`（×1.0；另匹配 `IND/D1/PV` ×1.1）
- 核心字段：`returns` × `count_institutional_holders_security`（机构持有家数的时序 Z 分数）
- 表达式：`rank(-ts_regression(ts_zscore(returns, 252), ts_zscore(count_institutional_holders_security, 252), 252, rettype=0))`
- 设置：IND / TOP500 / D1 / STATISTICAL / decay 126 / trunc 0.08 / nanHandling OFF / maxTrade OFF / unitHandling VERIFY / pasteurization ON / P0Y0M0D / FULL；2014-01-01→2023-12-31
- 平台指标：S **2.87** / F **2.14** / 2Y **2.08**（IS_LADDER limit 2.02）/ SUB **1.36**（limit 0.85，余量 0.51）/ ROBUST **1.55**（limit 1.0）/ CLUSTER **2.11**（limit 1.0）/ TVR **24.03%** / RET 13.37% / DD **4.04%** / margin **11.12 bp** / invest_S **2.25**（invest_S/S **0.7840**，≥ 0.70）
- RA 闸：`failed_ra_count = 0`；/check 0 FAIL / 4 WARNING（MATCHES_THEMES、OSMOSIS_ALLOCATION、PPA 描述长/格式两条，均非 REGULAR 硬闸），SELF / PROD / DATA_DIVERSITY / REGULAR_SUBMISSION / POWER_POOL 全部 PASS
- 相关性（`check_correlation(refresh=True)`）：PROD max **0.5925**（PASS，余量 **0.1075**；直方图 [0.5,0.6) n=8，无 ≥0.6）/ SELF max **0.2663**（对 `RR7v9gV0`；pool 49 / OS pool 54，5 颗 PPA 按平台口径排除；/check 视角 0.2608）

### 逐年 Sharpe（IS 2014–2023）

| 2014 | 2015 | 2016 | 2017 | 2018 | 2019 | 2020 | 2021 | 2022 | 2023 |
|---|---|---|---|---|---|---|---|---|---|
| 5.72 | 1.42 | 3.19 | 2.83 | 3.11 | 3.85 | 2.50 | 2.31 | 2.10 | 1.82 |

### Phase C 反过拟合闸（近窗制度：最近 3 个 IS 年）

| 检查项 | 读数 | 判定 |
|---|---|---|
| Recent-3yr 均值 Sharpe（2021–2023） | **2.077** ≥ 1.58 | PASS |
| 近 3 年每年为正（>0.3） | 2.31 / 2.10 / 1.82 | PASS |
| Recent-3yr CV_Sharpe | **0.097** < 0.40 | PASS |
| 衰减比（2023 / 全期） | **0.634**（1.82 / 2.87）≥ 0.50 | PASS |
| Recent-3yr max/min | **1.269** ≤ 3 | PASS |
| 平年数（\|S\|<0.3） | 0 | PASS |
| 全历史疲软 | 全历史 CV **0.403**（仅略高于 0.40）、max/min **4.03**（2014 5.72 / 2015 1.42） | 软标记，**不据此 REJECT** |
| Margin @ turnover | 11.12 bp @ 24.03% TVR | PASS |
| 算子数 | 4（`rank` + `-` + `ts_regression` + `ts_zscore`×2） | PASS（≤5） |
| 经济可解释性 | 「机构持有家数的时序偏离，剥离与收益共动的慢趋势后，短期反转」一句话可写 | PASS |

### PnL 与回撤归因

- 全期 maxDD **4.04% book**（与 2015 年回撤同值）；年度回撤均值 2.19%，2015 为 **1.84×** 均值（低于 2× 阈值）；平台仅给年度回撤，无单季数据显示结构性塌陷。
- 年度 PnL **10/10 为正**：2,820k / 717k / 1,563k / 1,234k / 1,562k / 1,690k / 1,294k / 1,082k / 1,077k / 790k。
- Top-5 个股集中度：平台只提供聚合 PnL（`recordsets/pnl`），未提供逐股 PnL，未计算（非 PASS 依据）。
- 组合前后对比（`performance_comparison`，IND/D1/POWER_POOL）：before S **4.12** / after S **4.79**，returns 10.94% → 11.54%，tvn 16.09% → 18.07%，双侧均为正、无负边际。

### 判定

**PASS**。近 3 年三项硬指标（均值 / CV / 衰减比）全部过线，无 REJECT 项。软标记见台账 `soft_flags`：
全历史 CV 0.403（仅略高于 0.40）、全历史 max/min 4.03（2014 早期强势年抬高）、2015 年回撤 4.04%（1.84× 年度均值，<2×）、
Top-5 集中度不可得（聚合 PnL）。近 5 年不是单调衰减（2019 3.85 → 2023 1.82），衰减比 0.634 仍在安全区，经济机制单句可写。

台账 `robustness_0mjk2ZQv` 已写 PASS；本轮用户已明确确认提交 `0mjk2ZQv`。
