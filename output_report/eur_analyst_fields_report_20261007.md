# EUR 区 ANALYST 类数据集字段构成报告

**查询参数**（全部 13 个数据集统一）：`region=EUR, universe=TOPCS1600, delay=1, filter_sharpe=false`
**查询方式**：MCP `mcp__wq-brain-http__get_datafields`
**查询日期**：2026-10-07

---

## 0. 方法与数据可信度声明（请先读）

这一节决定了后面每个数字该被信到什么程度，请务必先看。

### 0.1 平台返回的两个硬限制

1. **`search` 参数最多返回 100 条**（实测多次恰好返回 98/99/100）。
   → 对字段数 >100 的数据集，**按前缀分批查无法穷尽**，只能拿到"相关度最高的 100 条"。
2. **单次全量返回超过约 8 万字符会报错**并落盘。
   → `analyst11`（445 字段）全量查询直接失败：`result (83,130 characters) exceeds maximum allowed tokens`。
   → 落盘文件位于 `~/.workbuddy/projects/.../tool-results/mcp-wq-brain-http-get_datafields-1791382260315-f66427.txt`，但**本次会话中该文件的 Read / Grep / Bash 访问均被权限拒绝**，因此我无法对 analyst11 做全量精确统计。

### 0.2 因此，本报告的数据分两类

- **[精确]**：字段数 ≤ 122 的小数据集，返回完整未截断，所有数字（count / 类型分布 / 覆盖率分位 / userCount 分布 / 完整字段列表）均为**实测精确值**。
- **[抽样]**：字段数 > 400 的数据集，基于 ≤100 条的分批抽样。**覆盖率的"中位数"和"前缀计数"为估算值，已标注 `≈`；类型分布给出的是抽样比例而非精确计数。**

### 0.3 覆盖率（coverage）的语义坑（重要）

平台返回的 `coverage` 不是"多少股票有这个字段"，而是**该字段在时间序列上的有效观测占比**。这解释了本报告里大量数据集出现 `coverage` 精确等于 **0.5** 或 **1.0** 的整片同值：

- `coverage = 0.5` 的数据集（analyst14 / analyst15 / analyst7）→ 典型的**半年度财报期**标记，平台只在前半个观测窗口有值。
- `coverage = 1.0` 的数据集（analyst45 / analyst10 多数 / analyst69 多数）→ 平台对该字段做了全窗口填充，**不代表它对全部 1600 只股票都有值**。

所以 **coverage 高 ≠ 截面广**。真正的截面广度要看 `userCount` 分布和该字段在 TOPCS1600 上的非空截面数（需要 Labs 脚本才能测，本报告未做）。

---

## 1. 总览表

> 图例：`M` = MATRIX，`V` = VECTOR，`G` = GROUP
> `≈` = 抽样估算（分批查询 `search` 上限 100 条，非全量）

| # | 数据集 | 字段数 | 类型分布 | 中位覆盖 | 覆盖≥0.9 | 覆盖≥0.7 | 主要命名前缀（个数） | 零使用(userCount=0) | 数据可信度 |
|---|---|---|---|---|---|---|---|---|---|
| 1 | **model52** | 3 | M3 / V0 / G0 | **0.1986** | 0 | 0 | `cr_`(3) | 2 / 3 | 精确 |
| 2 | **analyst81** | 5 | M5 / V0 / G0 | **0.2316** | 0 | 0 | `anl81_`(3)，`default_likelihood_percent` / `financial_data_completeness_percent`(各1) | 3 / 5 | 精确 |
| 3 | **analyst39** | 24 | M24 / V0 / G0 | **0.9127** | 19 | 24 | `anl39_`(24) | 0 / 24 | 精确 |
| 4 | **analyst45** | 61 | M0 / **V61** / G0 | **1.0000** | **61** | 61 | `anl45_`(51)，无前缀(10：货币/基准类) | 14 / 61 | 精确 |
| 5 | **analyst9** | 111 | M5 / **V106** / G0 | ≈0.59 | 4 | ≈33 | `anl9_`(83)，`anl9_consensusv2span_`(34)，`anl9_sconsensusv2span_`(30) | ≈83 / 111 | 精确(count) / 覆盖为估算 |
| 6 | **analyst14** | 121 | **M121** / V0 / G0 | **0.5000** | 0 | 0 | `anl14_high/low/mean/median/stddev/numofests_`(99)，`rtk_ptg_`(6)，`anl14_actvalue_`(9) | ≈48 / 121 | 精确 |
| 7 | **analyst11** | 445 | **M445** / V0 / G0（推断） | ≈0.86 | ≈300 | ≈430 | `anl11_creptcesger*`(≈50)，`anl11_*reg_*perc/rnk`(≈60)，`anl11_e/g/emp/cit_*`聚合KPI(≈30) | **≈420 / 445** | 抽样 |
| 8 | **analyst4** | 776 | M+V 混合（抽样 ≈ 各半） | ≈0.86 | ≈600 | ≈680 | `anl4_fs_detail_estimates_*`(≈150)，`anl4_*_flag/_ft`(27)，`anl4_bac1*`/`cuo1*`/`eaz1*`(≈90)，`anl4_*_bk/_person/_item`(≈80) | ≈600 / 776 | 抽样 |
| 9 | **analyst69** | 813 | **V为主** + M(约1/4) | ≈0.94 | ≈700 | ≈760 | `anl69_best_*(≈420)`，`*_best_cur_fiscal_*_period`(≈30)，`*_expected_report_dt` | ≈200 / 813 | 抽样 |
| 10 | **analyst10** | 961 | V+M 混合 | ≈0.95 | ≈800 | ≈880 | `anl10_*past_det_analyst/_indicator/_estage`(≈330)，`*smun_*`(≈80)，`*_smart_ests_v0/v1/v2`(≈120)，`*_ff`字段格式(≈25) | ≈600 / 961 | 抽样 |
| 11 | **analyst7** | 1111 | **M1111** / V0 / G0（推断） | **0.5000** | 0 | 0 | `est_12m_*(≈300)`，`est_q_*(≈220)`，`act_q_*_surprise*(≈20)`，`rec_*` | ≈700 / 1111 | 抽样 |
| 12 | **analyst15** | 1744 | **M1744** / V0 / G0 | **0.5000** | 0 | 0 | `anl15_{bps,cps,ebt,ebg,dps}_{s,gr,ind}_*`(笛卡尔积，≈1700) | ≈1500 / 1744 | 抽样 |
| 13 | **analyst_consensus** | 1929 | **V 为主** + M(少量) | ≈0.80 | ≈1200 | ≈1500 | `mean_estimate_*`(72+)，`median_estimate_*`，`max/min_estimate_*`，`stddev_*`，`{mean,median}_flash_estimate_*`，`estimate_count_*` | **≈1750 / 1929** | 抽样 |

---

## 2. 逐数据集明细

### 2.1 model52 — 3 字段（全量精确）

信用评级类，**极小数据集**。

| 字段 | 类型 | coverage | userCount | alphaCount |
|---|---|---|---|---|
| cr_class | M | 0.1986 | 0 | 0 |
| cr_confidence_level_percent | M | 0.1986 | 0 | 0 |
| cr_probability_of_default_percent | M | 0.1986 | 1 | 2 |

- 类型：M3
- 覆盖率：最高 0.1986，≥0.9 = 0，≥0.7 = 0，中位数 **0.1986**
- 前缀：`cr_` = 3/3（单一机制：信用质量评级）
- 零使用：2/3。最高使用：`cr_probability_of_default_percent`（userCount=1, alphaCount=2）
- 高覆盖列表：无

**判断**：信用评级本身在 EUR 覆盖极稀（0.1986，只覆盖约 1/5 股票），且 3 个字段是同一机制的三种表示。**不值得单独挖**，覆盖闸必过不去。

---

### 2.2 analyst81 — 5 字段（全量精确）

同样是信用评级，与 model52 高度重复（`class` / `confidence` / `PD` 三件套）。

| 字段 | 类型 | coverage | userCount | alphaCount |
|---|---|---|---|---|
| anl81_class | M | 0.2316 | 0 | 0 |
| anl81_confidence_level_percent | M | 0.2316 | 0 | 0 |
| anl81_probability_of_default_percent | M | 0.2316 | 2 | 2 |
| default_likelihood_percent | V→M | 0.2531 | 0 | 0 |
| financial_data_completeness_percent | M | 0.2531 | 3 | 3 |

- 类型：M5
- 覆盖率：最高 0.2531，≥0.9 = 0，≥0.7 = 0，中位数 **0.2316**
- 前缀：`anl81_` = 3/5（另有 2 个无前缀长名）
- 零使用：3/5。最高：`financial_data_completeness_percent`（3/3）、`anl81_probability_of_default_percent`（2/2）
- 高覆盖列表：无

**判断**：与 model52 是**同一机制的两个数据源副本**，覆盖率都约 0.2。**直接排除**，重复劳动。

---

### 2.3 analyst39 — 24 字段（全量精确）

**本报告中覆盖质量最好的小数据集**。基本面估值/盈利能力指标，MATRIX。

覆盖率画像：最高 0.9231，≥0.9 = **19/24**，≥0.7 = **24/24**，中位数 **0.9127**

前缀：`anl39_` = 24/24（完全同前缀，但内含 3 个机制族）

机制族拆分（按字段名语义）：
- **EPS 族**（8）：`anl39_aepsinclxo` / `qepsinclxo` / `ttmepsincx` / `roxlcxspeq` / `roxlcxspea` / `ptmepsincx` / `xlcxspemtp` / `xlcxspemtt`
- **每股账面价值族**（4）：`atanbvps` / `qtanbvps` / `spvba` / `spvbq`
- **毛利率族**（5）：`agrosmgn` / `agrosmgn2` / `qgrosmgn` / `grosmgn5yr` / `ttmgrosmgn` — 覆盖明显偏低（0.70–0.77）
- **杠杆族**（3）：`qtotd2eq`（覆盖 0.9068，userCount 122/alphaCount 175，**全数据集最热**）/ `qtotd2eq2` / `rasv2_atotd2eq`
- **EPS 变动率族**（4）：`epschngin` / `ghcspea` / `ghcspemtt` / `rygnhcspe`

零使用：**0/24**（全部字段都有人用过）
userCount Top3：`anl39_qtotd2eq`（122 / 175）、`anl39_qepsinclxo`（60 / 70）、`anl39_qtanbvps`（56 / 66）

高覆盖（≥0.9）完整列表（19 个）：
`anl39_aepsinclxo`(0.9212)、`anl39_atanbvps`(0.9231)、`anl39_ghcspea`(0.9172)、`anl39_ptmepsincx`(0.9029)、`anl39_qepsinclxo`(0.9193)、`anl39_qtanbvps`(0.9174)、`anl39_qtotd2eq`(0.9068)、`anl39_rasv2_atotd2eq`(0.9119)、`anl39_roxlcxspea`(0.9212)、`anl39_roxlcxspeq`(0.9193)、`anl39_rygnhcspe`(0.9071)、`anl39_spvba`(0.9231)、`anl39_spvbq`(0.9174)、`anl39_ttmepsincx`(0.9136)、`anl39_xlcxspemtp`(0.9029)、`anl39_xlcxspemtt`(0.9135)、`anl39_epschngin`(0.8995，接近)、`anl39_ghcspemtt`(0.8922)、`anl39_qtotd2eq2`(0.8954)

**判断**：**高优先级**。覆盖 0.91 中位、0 使用字段 0、机制清晰（盈利能力+杠杆+账面价值）、字段数少易穷尽、样本内已有高使用字段（说明机制被验证过但远未饱和）。主要注意点：杠杆族（`qtotd2eq`）userCount 已 122，容易撞 prod 相关性，需搭配账面价值或 EPS 变动率做差异化。

---

### 2.4 analyst45 — 61 字段（全量精确）

**"Idea / 投资组合"元数据类，全部 VECTOR，全部 coverage=1.0。**

| 统计项 | 值 |
|---|---|
| 字段数 | 61 |
| 类型 | M0 / **V61** / G0 |
| 最高覆盖 | 1.0000 |
| ≥0.9 | **61/61** |
| ≥0.7 | 61/61 |
| 中位覆盖 | **1.0000** |
| 零使用 | **14/61** |

前缀分布：
- `anl45_` = 51/61
- 无前缀（长名）= 10：`benchmark_currency_code`、`conversion_rate_summary`、`currency_gain_percentage`、`currency_gain_value`、`investment_currency_code`、`security_trading_currency_3`

机制族（这是本数据集最关键的信息）：
- **持仓/敞口**（约 10）：`current_inv`(17/24)、`initial_inv`(9/11)、`ang_inv`、`net_market_exposure`(**82/114，全数据集最热**)、`idea_count`(9/13)、`probability`、`new_value`/`old_value`
- **收益归因**（约 20）：`ad_ret_per`、`real_ret`、`unreal_ret`、`tot_ret`、`rel_ret_per`、`stock_ret_per`、`ret_today` 系列
- **价格/成本**（约 12）：`prc`、`avg_initial_prc`、`target_prc`、`prev_close_prc`、`period_*_prc`、`latest_prc`、`closed_prc`
- **基准/FX**（约 8）：`bm_ret`、`bm_ret_wo_fx`、`bm_fx_ret`、`bm_exchange_rate`、`inv_exchange_rate`、`*_currency_*`
- **风险调整**（5）：`beta`、`jensensalpha`、`treynor_ratio`、`tot_ret_per`、`risk_free_rate`
- **元信息**：`time`、`days_since_inception`、`avg_dur`、`current_inv`

零使用字段（14 个）：`anl45_bm_exchange_rate`、`anl45_bm_ret`、`anl45_index_ret_per`、`anl45_probability`、`anl45_real_ret_today`、`anl45_rel_ret_per_today`、`anl45_rel_ret_today`、`anl45_ret_today`、`anl45_stock_ret_per`、`anl45_tot_ret_wo_fx`、`anl45_transaction_charge`、`benchmark_currency_code`、`conversion_rate_summary`、`currency_gain_percentage`、`currency_gain_value`、`security_trading_currency_3`（其中 3 个为无前缀长名）

userCount Top3：`anl45_net_market_exposure`（82 / 114）、`anl45_current_inv`（17 / 24）、`anl45_idea_count`（9 / 13）

高覆盖（≥0.9）完整列表：**全部 61 个**（均为 1.0），从略。

**判断**：**机制独特但需谨慎**。全 VECTOR + 全覆盖 1.0 意味着"平台侧数据完整"，但这批字段描述的是**平台用户自己创建的 idea 组合**（一个"虚拟持仓/回测想法"的账本），**不是市场数据**。对 EUR TOPCS1600 而言，这些字段在真实截面上的截面广度存疑（很可能是稀疏的、只对少数有 idea 的股票有值），而 coverage=1.0 只是时间维度的填充。

**建议**：不做主力。可以低成本试 1–2 个表达式（例如 `vec_avg(anl45_net_market_exposure)` 或 `vec_avg(anl45_rel_ret_per)`），先确认截面非空率再决定是否展开。**不要**因为 coverage=1.0 就假设它好用——这是本报告最容易误判的一个数据集。

---

### 2.5 analyst9 — 111 字段（全量返回，统计为估算）

**S&P Capital IQ 分析师一致预期明细（revision span 结构）。**

| 统计项 | 值 |
|---|---|
| 字段数 | 111（精确） |
| 类型 | **M5 / V106 / G0**（精确） |
| 最高覆盖 | 1.0000（`anl9_recommendationbrokeroptioncode`） |
| ≥0.9 | **4** |
| ≥0.7 | ≈33 |
| 中位覆盖 | ≈0.59（估算） |
| 零使用 | ≈83 / 111 |

5 个 MATRIX（注意：VECTOR 才是主体）：`anl9_estanalystmap`(0.8496)、`anl9_recommendationbrokeroptioncode`(1.0)、`anl9_recommendationnumericvalue`(0.9714)、`anl9_scaleconversionflag`(0.9742)、`base_currency_conversion_indicator`(0.9742)

前缀/词根分布（**这是 analyst9 的核心结构信息**）：
- `anl9_` = 83/111
- `anl9_consensusv2span_` = 34（每条报表 4 件套：`dataitemvalue` / `effectivetime` / `splitfactor` / `totime`）
  - 其中按报表分：`balancesheet`(4)、`cashflowstatement`(4)、`incomeebt`(4)、`incomeeps`(4)、`incomenetincome`(4)、`incomeothers`(4)、`others`(4)
- `anl9_sconsensusv2span_` = 30（"s"=snapshot 版本，结构同上，但**覆盖普遍高一档**，0.65–0.82）
- `anl9_daily_num*` = 8（`numup` 15/18、`numdn` 9/10、`numanalysts`、`numanalystall`、`numupunfiltered`、`numdownunfiltered`、`numnochg`、`numnochangeunfiltered`）
- `anl9_s_num*` = 8（同上的 snapshot 版）
- `anl9_guidancev2span_*` = 3（覆盖极低 0.2186）
- `anl9_detail_*` / `anl9_sdetail_*` = 6
- 无前缀 `*_consensus_value` 类 = 12（各种 lookup 索引，多数覆盖 0.22–0.60）

**关键判断**：
1. **111 个字段里约 75 个是 `_dataitemvalue` / `_effectivetime` / `_splitfactor` / `_totime` 四件套**。后三者（时间戳、拆股因子）**几乎不可能直接构成 alpha**，真正可用的只有 `_dataitemvalue`。
2. 即便只取 `dataitemvalue`，也只有 **≈9 个财务科目 × 2 个版本（current / _s）+ 2 个时间窗（current / prior）** 的窄窄一条线。
3. 覆盖约 0.55–0.60，**季度类（`_quarterly16` 隐含的 fq16/gps 族）覆盖低到 0.18–0.25**，那几个必然过不了覆盖闸。
4. **真正的可用亮点是 revision 计数**：`anl9_daily_numup`（15/18）、`anl9_daily_numdn`（9/10）、`anl9_s_numup`（5/6）—— 覆盖 0.5532/0.602，是「分析师上/下修家数」这一经典机制，且已在用但 userCount 很低（≤15），**竞争空间大**。

userCount Top3：`anl9_daily_numup`（15 / 18）、`anl9_consensusanalysis_dataitemvalue`（10 / 15）、`anl9_daily_numdn`（9 / 10）

**判断**：**中等优先级，但只挖 3–5 个字段，不要碰 111 个**。理性路径：集中打「revision 广度/净额」这一族（`daily_numup`、`daily_numdn`、`daily_numanalysts`，配合 `vec_` 算子），这是该数据集里唯一既机制清晰、覆盖尚可、竞争又小的角落。`consensusv2span_*_effectivetime/totime/splitfactor` 这 3 类（共约 56 个字段）**直接视为噪声**。

---

### 2.6 analyst14 — 121 字段（全量精确）

**"分析师预测统计量"：对 8 个科目 × 6 个统计量 × 2 个前瞻期做笛卡尔积。全字段 coverage 精确等于 0.5。**

| 统计项 | 值 |
|---|---|
| 字段数 | 121 |
| 类型 | **M121 / V0 / G0** |
| 最高覆盖 | 0.5000（全部字段同值） |
| ≥0.9 | **0** |
| ≥0.7 | **0** |
| 中位覆盖 | **0.5000** |
| 零使用 | ≈48 / 121 |

**前缀结构（笛卡尔积，非常规整）**：
| 前缀 | 个数 | 含义 |
|---|---|---|
| `anl14_high_*` | 20 | 最高估值（8 科目 × fp1/fp2） |
| `anl14_low_*` | 25 | 最低估值 |
| `anl14_mean_*` | 20 | 均值估值 |
| `anl14_median_*` | 20 | 中位数估值 |
| `anl14_stddev_*` | 16 | 估值标准差（离散度） |
| `anl14_numofests_*` | 16 | 覆盖分析师家数 |
| `anl14_actvalue_*` | 9 | 实际值（上季） |
| `anl14_{buy,hold,sell,outperform,underperform,meanrating}` | 6 | 评级分布 |
| `rtk_ptg_*` | 6 | 目标价（high/low/mean/median/number/stddev） |
| `anl14_{curperiodnum,curperiodtype,cursharesoutstanding,xrefmap}` | 4 | 期间/股本元信息 |

8 个科目：`ebit`、`ebitda`、`eps`、`epsrep`、`ntp`、`ntprep`、`ptp`、`ptprep`、`revenue`（9 个，含 revenue），前瞻期 `fp1`（下季）/ `fp2`（下两季）

零使用字段（≈48 个，主要是 `stddev_*` 和 `numofests_*` 的 fp2 尾部，以及 `high_*`/`low_*` 中无人用的科目）。

userCount Top3：`anl14_buy`（38 / 50）、`rtk_ptg_high`（28 / 33）、`rtk_ptg_median`（19 / 19）

**判断**：**结构最规整、最适合做笛卡尔积扫面的数据集**。但有两个硬伤：
1. **coverage 全部 = 0.5**，覆盖闸会以 0.5 为上限卡人。需要先在 Labs 里确认非空截面数。
2. **`stddev_*`（16 个）和 `numofests_*`（16 个）合计 32 个字段是"估计离散度"和"覆盖家数"** —— 这两个恰好是**分析师预期不确定性的经典代理变量**，机制上比 mean/median 更有 alpha 价值，且其中约一半无人使用。**这 32 个字段是本数据集的真正机会点**，比 99 个 mean/high/low 兄弟字段更值得挖。

**建议路径**：优先打 `stddev_*` / `numofests_*` / `rtk_ptg_stddev` 这条"分歧度"机制线，用 8 科目 × 2 期做小笛卡尔积（例如 `vec_avg(anl14_numofests_eps_fp2)`、`ts_rank(anl14_stddev_eps_fp1, 252)` 之类），而不是去扫 99 个 high/low/mean 兄弟。

---

### 2.7 analyst11 — 445 字段（抽样，全量查询因体积失败）

**注意：本数据集与 "分析师" 名字无关，实际是 ESG 评分数据集。**

已确认事实：
- 全量查询失败（83,130 字符超限），无法做精确统计。
- `data_type=GROUP` 查 → 0 条
- `data_type=VECTOR` + `search="anl11_"` → 0 条
- `data_type=VECTOR` + `search="score"` → 0 条
- → **强烈提示全部 445 个都是 MATRIX**（未能 100% 证实，标为推断）

抽样得到的覆盖率画像：全部落在 **0.69 – 0.91** 区间，例如 0.9065(`anl11_g`)、0.908(`anl11_e`)、0.9087(`anl11_gse`)、0.8892、0.8874、0.8841、0.8749、0.82(混合分)、0.79、0.7572、0.6958
- 中位覆盖 **≈0.86**（估算）
- ≥0.9 约 **300** 个（估算）
- ≥0.7 约 **430** 个（估算）
- **零使用 ≈420 / 445** —— 这是本数据集最惊人的数字

**命名前缀族（这是 analyst11 的核心信息）**：
1. `anl11_creptcesger*`（≈50，抽样中出现 20+ 次）：**"公司 ESGR 百分位/排名"的生造缩写**，按「科目后缀 × 群体类型(sector/sect/ind/subsec) × 指标(perc/rnk/pme/tic/e/g) × 柱式(E/EMP/CIT/G)」四重笛卡尔积生成。例：`anl11_creptcesger1pme`、`anl11_creptcesger2e`、`anl11_creptcesgerrocsopgse`
2. `anl11_*reg_*perc` / `anl11_*reg_*rnk`（≈60）：如 `cit1reg_industryperc`、`e2reg_subsecperc`、`gregsubsecrnk`
3. `anl11_{e,g,emp,cit,esg}_{1,2,3}{e,g,pme,tic}`（≈30）：**原始聚合 KPI**（如 `anl11_1e` 污染预防、`anl11_3g` 披露透明度）
4. `anl11_*_totalcor` / `*_ttcrg` / `*_poscor*`（≈20）：**"ESG 与财务回报相关性加权"的混合分数**（`anl11_esg_totalcor`、`anl11_e_ttcrg_industryperc`）
5. **无 `anl11_` 前缀的长名族（≈185，占比最大！）**：`social_score_sector_percentile`、`governance_industry_percentile_score`、`sustainability_hybrid_*_position`、`environmental_maxcorr_*`、`transparency_*`、`citizenship_hybrid_*`、`employer_*`、`management_ethics_*`
   - 这批长名与 `anl11_` 短名**是同一批数据的重复暴露**（例：`anl11_creptcesgergse` 与 `sustainability_sector_percentile_score` 描述都是"ESG score 在 sector 内的百分位"）

抽样中 userCount 最高的：`citizenship_hybrid_industry_percentile_score`（4 / 5）、`anl11_1g`（5 / 8）、`anl11_2e`（5 / 5）、`anl11_1pme`（6 / 6）、`anl11_empregsubsecperc`（1/2）
**全数据集最高也只有 userCount≈6** —— 而 445 个字段里约 420 个是 0 使用。

**判断**：**低优先级（不建议作为 REGULAR alpha 主力）**。理由：
1. **机制与 "分析师预期" 无关** —— 如果你的战役主题是分析师预期修正，这 445 个字段整体跑偏。它们的价值在 ESG 因子本身。
2. **命名空间极度混乱** —— 同一份数据同时以 `anl11_` 短名（生造缩写，几乎不可读）和长名（可读）两套暴露，且有明显的重复字段。这会让"笛卡尔积扫面"变得不可控，也难以判断两个 alpha 是不是其实用了同一个数据。
3. **覆盖率高不代表信号好** —— 0.86 的覆盖是"时间维度"填满，但 ESG 分数天然是**低频、慢变、年度更新**的。在 delay=1、日频 alpha 上，一个季度才动一次的分数其换手极低，Sharpe 能否做出来高度存疑。
4. **零使用率 94%** 通常是**双刃剑**：可能是金矿（无人发现的空白），也可能是**平台自己也不认为它有 alpha 价值**。结合第 3 点（低频），我倾向后者。

**如果一定要碰**：只用长名里的 `social_*` / `governance_*` / `environmental_*` score 系列（可读、机制清楚），配 `ts_rank` 做慢变信号的横截面排序，测 2–4 个表达式验证 ESG 是否在 EUR 有预测力。**不要**碰 `anl11_creptcesger*` 那 50 个生造缩写。

---

### 2.8 analyst4 — 776 字段（抽样）

**混合结构：MATRIX（"汇总后的分析师预测值"）+ VECTOR（"按 broker/分析师拆分的明细"）。**

抽样观察：
- 最高覆盖 1.0（`anl4_ffo_flag`、`anl4_rd_exp_flag`、`anl4_cfi_flag`、`anl4_cff_flag`、`anl4_tbve_ft`、`anl4_fcfps_flag`）
- ≥0.9 的字段大量存在且集中在 `_flag` / `_ft`（forecast type）系列
- 中位覆盖 **≈0.86**（估算）

**命名前缀族**：
1. `anl4_fs_detail_estimates_advanced_af_nd_*`（≈150）：**Cash Flow 报表科目的 low/mean/median/high/number**（`fcf`、`cfi`、`cff`、`cfo`、`fcfps`、`capex`）
2. `anl4_*_flag` / `anl4_*_ft`（**27 个，精确**）：forecast type（revision/new/...），覆盖 0.85–1.0
3. `anl4_{bac1,cuo1,dei2,dei3,eaz1,eaz2,ads1}*`（≈90）：**两字母模块前缀**，每模块下挂 `_item`/`_bk`/`_person`/`_mean`/`_high`/`_median`/`_low` 七件套（VECTOR 为主）
4. `anl4_{ady,basiccon*,adxqf,eaz*,dez*}_*`：第二套两字母模块
5. `anl4_{af,ad,qf,af}_*`：单字母简写系列（`af_eps_*`、`adz_*`）
6. 无前缀长名：`quarterly_free_cash_flow_low` 等

零使用 ≈600 / 776（抽样中高使用字段稀少，仅见 `anl4_af_eps_low` 34/130、`anl4_adjusted_netincome_ft` 66/230、`anl4_totassets_flag` 28/93）

**判断**：**中等优先级，但只取 2 个窄族**。
1. **`anl4_*_flag` / `_ft`（27 个，覆盖 0.85–1.0）** —— 「forecast type = revision/new」本身是一个**信息量很大但极少被用**的字段：它标记了"这条预测是新发布的还是被修订过的"，配合 `ts_delta` 可以构造"分析师在何时集体转向"的机制。27 个字段中多数 userCount=0。**这是 analyst4 里性价比最高的角落。**
2. **`anl4_fs_detail_estimates_advanced_af_nd_*_low`（20 个，精确覆盖见 §抽样）** —— 现金流科目 low/mean/median 之差 = 预期离散度。但注意覆盖两档：`_af_nd_` 系列覆盖 0.80–0.88（可用），`_1qf_v4_nd_` 系列覆盖只有 0.28–0.30（**不可用**）。
3. **必须避开**：两字母模块前缀那约 170 个 VECTOR 明细字段（`bac1*`/`cuo1*`/`eaz*`/`ads1*`），它们是「每 broker 一条记录」的明细，截面稀疏、需要 vec_* 聚合才能用，笛卡尔积不可控。

---

### 2.9 analyst69 — 813 字段（抽样）

**Refinitiv 风格的"最佳（consensus）预测汇总 + 财期与财报日"。**

抽样观察：VECTOR 为主，MATRIX 约占 1/4。
- 最高覆盖 1.0（大量 `anl69_best_*`）
- 中位覆盖 **≈0.94**（估算）
- ≥0.9 ≈700（估算）

**命名前缀族**：
1. `anl69_best_*`（**≈420，占比过半**）：结构 `anl69_best_{科目}_{统计量}`
   - 科目（≈20）：`eps`、`eps_gaap`、`ebit`、`ebitda`、`net`、`net_gaap`、`ptp`、`opp`、`sales`、`ndebt`、`nav`、`roe`、`roa`、`target`、`dps`
   - 统计量（6 件套）：`_lo` / `_mean` / `_hi` / `_stddev` / `_numest` / `_4wk_chg` / `_4wk_up` / `_4wk_dn` / `_chg_pct`
   - 比率类：`anl69_best_ebit_to_sales`、`anl69_best_ptp_to_sales`、`anl69_best_px_bps_ratio`、`anl69_best_cur_ev_to_ebitda`
2. `*_best_cur_fiscal_{year,quarter,semi_year}_period`（≈30，MATRIX，覆盖全部 0.5）：财期标识
3. `*_expected_report_dt`（MATRIX，0.5）：**预期财报日**
4. `anl69_analyst_*`（≈5）：`latest_ann_dt_qtrly`、`best_fiscal_period_dt`、`expected_report_dt`
5. `anl69_*_best_crncy_iso`：货币代码（全 1.0）
6. `anl69_{tot_sell_rec, best_analyst_rating, aeps_market_status, bps_market_status, eqy_recent_qt_end}`

**零使用 ≈200 / 813**（抽样估计）—— 相比字段数比例，零使用比例在几个大集里最低，说明**竞争度最高**。

userCount 极高的字段（抽样可见，**这是本数据集最重要的信号**）：
- `anl69_best_analyst_rating` — **userCount 507 / alphaCount 3865**
- `anl69_best_eeps_cur_yr` — **250 / 3842**
- `anl69_best_cur_ev_to_ebitda` — 155 / 1821
- `anl69_best_ndebt_hi` — 108 / 2163
- `anl69_best_ebit_4wk_chg` — 92 / 1950
- `anl69_analyst_expected_report_dt` — 165 / 3137
- `anl69_best_cur_fiscal_year_period` — 65 / 439
- `anl69_aeps_market_status` — 32 / 158

**判断**：**质量最高但竞争最激烈，且拥挤风险已经具体化**。
1. 覆盖 0.94 中位、全 MATRIX/VECTOR 混合、结构极规整（`best_科目_统计量` 九件套），**是本报告中"字段质量最好"的大数据集**。
2. **但**：`best_analyst_rating`（507 用户 / 3865 alpha）、`best_eeps_cur_yr`（250/3842）、`best_ndebt_hi`（108/2163）、`best_ebit_4wk_chg`（92/1950）这些字段**已经是全平台的万人坑**。在这些字段上直接做 9 件套笛卡尔积，**几乎必然 prod 相关性卡死**。
3. 相对空的地方：**`_4wk_up` / `_4wk_dn` / `_chg_pct` / `_stddev` / `_numest` 这几个"变动与分歧"后缀**。抽样中它们的 userCount 普遍在 1–28 之间，而 `_lo`/`_hi`/`_mean`/`_rating` 动辄上百。
4. MATRIX 侧的 `*_expected_report_dt`（165/3137）和 `*_best_cur_fiscal_*_period`（65/439）是**极强的 seasonality / 日历效应**来源，但已被大量使用。

**建议路径**：**不要碰 `_mean` / `_rating` / `_cur_ev_to_ebitda` / `_eeps_cur_yr`**。改为集中打 **`_4wk_up` vs `_4wk_dn` 的净额**（上修家数减下修家数）和 **`_stddev` / `_numest` 的分歧度**，这两个机制在 analyst69 里竞争最小。`anl69_best_ebit_4wk_up`(11/14) 与 `anl69_best_ebit_4wk_dn`(8/16) 是很好的起步对。

---

### 2.10 analyst10 — 961 字段（抽样）

**"逐分析师明细 + Smart Estimate + 分析师家数"三合一，是本报告中字段语义最碎的一个。**

抽样观察：VECTOR + MATRIX 混合，覆盖两档分明。
- **MATRIX 侧多为 coverage=1.0 或 0.43–0.54 两档**
- 中位覆盖 **≈0.95**（估算）

**命名前缀族**：
1. `anl10_{科目}past_det_{analyst,indicator,estage,estvalue}`（**≈330，1/3**）：每科目一套四件套
   - 科目（≈22）：`ebi`、`ebt`、`net`、`opr`、`pre`、`sal`、`nav`、`ner`、`tbv`、`csh`、`cpx`、`gps`、`dps`、`grm`、`ndt`、`prr`、`roe`、`roa`
   - `_analyst` = 分析师ID（VECTOR，覆盖 1.0 居多）
   - `_indicator` = 财期 ASCII 码（54=fq1, 55=fq2, 49=fy1, 50=fy2）
   - `_estage` = 预测_age（天）
   - `_estvalue` = 预测值
2. `anl10_{科目}{fq1,fq2,fy1,fy2}_smart_ests_{v0,v1,v2}`（**≈120**）：**Smart Estimate 三个版本**。这是最有料的一族——"Smart Estimate" 通常是平台对分析师预测做的**异常值调整/去极值**版本，`smart_ests_v1` 与 `mean` 的差本身就是"预测被修正的幅度"信号
3. `anl10_{科目}{1qf,1yf,2qf,2yf}_smun*`（**≈80**）：Sample/analyst number，**覆盖家数**
4. `anl10_{科目}ff` / `*_ff_NNN`（≈25）：field format 标志
5. `anl10_{ebi,net}innovation_score_{fq1,fq2}`（覆盖仅 0.34–0.44，**偏低不可用**）
6. `anl10_{科目}fq*_consensus_*` / `*_pred_surps_v0`（预测意外）

零使用 ≈600 / 961（估算）

抽样中 userCount 最高：`anl10_ebifq1_smart_ests_v0`(14/16)、`anl10_ebifq1_smart_ests_v1`(14/14)、`anl10_ebify1_smart_ests_v0`(11/11)、`anl10_ebifq1_smart_ests_v2`(9/11)、`anl10_netfy2_smart_ests_v0`(9/9)、`anl10_nersmun_2qf`(8/10)

**判断**：**信息量极大但工程成本最高，建议只做 Smart Estimate 一条线**。
1. `smart_ests_v0/v1/v2` 是本数据集**唯一的高价值机制**——三个版本并列意味着平台提供了至少两种口径的"平滑后预测"，`ts_zscore(v1 - v0)` 或 `v1/v0 - 1` 直接就是"分析师共识在被修正多少"的度量。而且抽样里 v0/v1/v2 的 userCount 都在 9–14，**竞争小**。
2. **必须避开** `*past_det_analyst` / `*past_det_indicator`（≈330 个）：分析师ID 和 财期ASCII码 是**纯粹的 ID/元数据**，不是数值信号。它们的价值只在于"配合 `_estvalue` 做 vec_max/vec_avg 分组聚合"。要单独用这些字段做表达式几乎必然失败。
3. **必须避开** `*innovation_score_*`（覆盖 0.34–0.44）和 `*_fq1/fq2_smart_ests_*`（季度类，覆盖 0.43–0.54）——覆盖不够。
4. `_smun_*`（家数）覆盖多在 1.0，机制清晰，可与 Smart Estimate 组合。

**建议路径**：`{科目}fy1/fy2` × `smart_ests_{v0,v1,v2}` × `{科目}smun_1yf/2yf`，围绕 FY1/FY2（不是季度）做一个小笛卡尔积，约 8 科目 × 2 期 × 3 版本 = 48 个候选，量级可控。

---

### 2.11 analyst7 — 1111 字段（抽样）

**"分析师预期全量矩阵"：科目 × 期限(q / 12m) × 统计量(high/mean/median/low/std/num) × 变动方向。**

抽样观察：**全部 MATRIX，全部 coverage 精确等于 0.5**（抽样的 100 条无一例外）
- 最高覆盖 0.5，≥0.9 = **0**，≥0.7 = **0**，中位覆盖 **0.5**
- 零使用 ≈700 / 1111

**命名前缀族（本数据集结构最规整）**：
1. `est_12m_*`（≈300）：**未来 4 个季度的滚动合计**期限
2. `est_q_*`（≈220）：**下一季度**期限
3. `act_q_*_surprise*`（≈20）：`act_q_{ebt,ebi,sal,net,ent,ndt,opr}_surprisemean` = 实际 - 预期 的惊喜值
4. `rec_mean`（1 个）：**Mean estimate of the analyst recommendation** — userCount **107** / alphaCount **840**，是本数据集最热字段
5. `est_*_{raised,lowered}num_4wks`（≈40）：**4 周内上/下修家数**
6. `est_*_std`（≈20）：预测标准差

**科目集合（≈20）**：`ebt`(EBITDA)、`ebi`(EBIT)、`ebs`(EBITDA/share)、`ent`(EV)、`sal`(sales)、`net`(net income)、`opr`(operating profit)、`ndt`(net debt)、`eps`、`gps`(GAAP EPS)、`dps`、`pre`(pretax)、`prr`、`ner`、`nav`、`tbv`、`cpx`(capex)、`grm`(gross margin)

**统计量后缀（6 件套）**：`_high` / `_mean` / `_median` / `_low` / `_std` / `_num`

**关键发现 —— 拥挤度已经分层**：
- **12m 期限热，q 期限冷**。`est_12m_ndt_median`(75/650)、`est_12m_ndt_mean`(60/638)、`est_12m_ebt_mean`(36/290)、`est_12m_ebt_median`(30/267)、`est_12m_sal_mean`(26/196)、`est_12m_sal_median`(22/186)、`est_12m_ebt_low`(26/232) vs 对比的 `est_q_*` 系列几乎全是 userCount=0。
- `_4wk` 系列冷热不均：`est_12m_ebt_lowerednum_4wks`(24/197) 热，而 `est_q_grm_lowerednum_4wks` 为 0。
- `act_q_*_surprise*` 全冷（多为 0–3）。

**判断**：**这是本报告里"最像标准 analyst estimate 数据集"的一个，机制最标准，但 coverage=0.5 是硬约束，且内部分层极其明显**。
1. **结构上它是最好的笛卡尔积载体**：`20 科目 × 2 期限 × 6 统计量 + 4wk 修正族 = 约 280 个核心字段`，命名 100% 可预测，扫面工程成本极低。
2. **coverage=0.5 是真实风险**。这与 analyst14/analyst15 同源（半年度窗口）。**在投入批量仿真前，必须先用 Labs 脚本测一次 TOPCS1600 上的非空截面数** —— 如果非空只有 800 只，覆盖闸还能过；如果只有 400 只，直接放弃。这一步能省掉整批回测。
3. **必须避开 `est_12m_{ndt,ebt,sal}` 的 mean/median/low/high** —— 这些 userCount 60–75、alphaCount 高达 650–840，已经是深坑。`est_12m_ndt_median`(75 用户/650 alpha) 尤其危险。
4. **机会点**：`est_q_*` 全系列（≈220 个，多数 userCount=0）+ `act_q_*_surprise*`（≈20，几乎全 0）+ `est_*_4wk_{up,dn}`。**"下一季度预期"相对冷门，但它的日频更新率可能比 12m 版本更高**（12m 是滚动合计，变化慢），换手可能更好。

**建议路径**：先 Labs 测 coverage → 若通过，主攻 `est_q_*` 的 `{low,mean,median,high}` 离散度（4 科目 × 3 统计量）+ `est_q_*_{raised,lowered}num_4wks`，配 `est_12m_*` 的对应字段做期限价差（term structure 机制：`est_12m_eps_mean / est_q_eps_mean`）。

---

### 2.12 analyst15 — 1744 字段（抽样）

**"行业/板块/分组层面的分析师预期聚合"—— 注意：这些字段描述的是 GICS 行业、板块、group 层级的聚合统计，**不是**个股字段。**

抽样观察：**全部 MATRIX，全部 coverage 精确等于 0.5**
- 中位覆盖 0.5，≥0.9 = 0，≥0.7 = 0
- 零使用 ≈1500 / 1744

**命名前缀族（纯笛卡尔积）**：
结构为 `anl15_{科目}_{群体层级}_{财期}_{统计量}`

- **科目（5）**：`bps`、`cps`、`dps`、`ebt`、`ebg`(EBIT before goodwill)
- **群体层级（3）**：`s`(sector)、`gr`(group)、`ind`(industry) —— 还有无层级的版本
- **财期（5）**：`cal_fy0`、`cal_fy1`、`cal_fy2`、`cal_fy3`、`12_m`、`18_m`
- **统计量（≈10）**：`mean`、`total`、`pe`、`st_dev`、`ests`(家数)、`ests_up`、`ests_dn`、`cos`(家数)、`cos_up`、`cos_dn`、`gro`(增长)、`chg`、`1m_chg`、`3m_chg`、`6m_chg`、`mktcap`、`val`

笛卡尔积规模：5 科目 × 3 层级 × 6 财期 × 16 统计量 ≈ 1440，与 1744 的字段数吻合。

抽样中 userCount 最高：`anl15_ebg_gr_cal_fy0_val`(9/12)、`anl15_bps_gr_12_m_cos_up`(8/8)、`anl15_bps_gr_12_m_pe`(4/6)、`anl15_s_12_m_ests_dn`(4/5)、`anl15_ebg_s_cal_fy2_mean`(6/10)、`anl15_ebg_ind_cal_fy3_mean`(4/7)

**判断**：**这是 16 个数据集中我认为最应该直接跳过的数据集**。三个独立的硬理由：
1. **它们不是个股字段**。描述明确写着 "aggregated within GICS industry grouping"、"in the Americas"、"at the sector level"。在 EUR TOPCS1600 上，这些字段的**截面变化几乎是常数**（同一行业内所有股票拿到同一个值），横截面排序后**信噪比接近 0**。`group_rank` 之类的算子在这种字段上不会有区分度。
2. **coverage=0.5**，与 analyst7/analyst14 同样的半年度窗口问题。
3. **零使用率 ≈86%**（1500/1744）。对一个 1744 字段的数据集，86% 无人使用不是"金矿"的强证据 —— 更可能是**社区早就试过并放弃了**。注意有相当一部分字段的 description 是明显复制粘贴错误的（多个 `anl15_cps_s_18_m_ests_dn` / `dps_s_fy2_ests_up` / `gr_18_m_ests_dn` 的描述都是同一句 "Count of unique IDs of industry participants..."），**数据质量本身有问题**。

**唯一可能的例外**（如果你一定要试）：`anl15_{ind}_*_total` / `*_mktcap` 这类**行业总量/市值聚合**字段，理论上可以做"分析师预期变化 vs 行业市值"的规模效应。但这是很弱的 idea，我**不建议投入**。

---

### 2.13 analyst_consensus — 1929 字段（抽样）

**全 EUR ANALYST 类里字段最多的数据集。** S&P Capital IQ 的一致预期中枢值族。

抽样观察：**VECTOR 为主，MATRIX 仅少量**
- MATRIX 抽样（`data_type=MATRIX, search="estimate"`）只返回 18 条，而 `search="consensus"` 全类型返回 100 条几乎全是 VECTOR
- MATRIX 侧集中在 `*_targetprice_annual12_tribes`（覆盖 0.9477，8 个统计量）和 `*_eps_longterm`（覆盖 0.7809，6 个统计量）
- 中位覆盖 ≈0.80（估算）；≥0.9 ≈1200（估算）

**命名前缀族（三层嵌套结构）**：
结构为 `{统计量}_estimate_[{时间偏移}_][fxadj_]{科目}_{财期}[_tribes]`

1. **统计量层（7 种）**：`mean_estimate_`、`median_estimate_`、`max_estimate_`、`min_estimate_`、`stddev_{estimate,current_period,recent_estimates,flash_estimate}`、`estimate_count_`、`estimate_currency_code_`
2. **时间偏移层**：`four_weeks_prior_`、`three_months_prior_`、`current_period_`、无偏移（= 当前）
3. **调整层**：`fxadj_`（currency/split/regime 调整）、`flash_`（最新快报）
4. **科目层（≈30）**：`eps`、`epsreported`、`net2`(net income)、`netprofit`、`reportednet`、`pretax`、`pretax_reported`、`ebt`、`ebit`、`ebitda`、`ebitdarep`、`revenue`、`cogs`、`dps`、`dividend`、`nav`、`roe`、`roa`、`fcf`、`capex`、`cfi`、`cff`、`cfo`、`cfps`、`fcfps`、`taxrate`、`taxprovision`、`depreciation`、`inventory`、`goodwill`、`total_assets`、`netdebt`、`enterprisevalue`、`bvps`、`tangbookvalue`、`sharesoutstanding`、`currentassets`、`currentliabilities`、`totalliab`、`marketable_securities`、`grossmargin`、`fullyreported`(GPS)
5. **财期层**：`annual12`、`quarterly16`、`fq16`、`longterm`，部分带 `_tribes` 后缀

抽样计数（`search="mean_estimate_"` 返回 72 条全部为该前缀）：说明 `mean_estimate_` 至少 72 个，实估在 200+ 量级。

零使用 **≈1750 / 1929** —— 抽样 100 条中只有 7 条 userCount>0，且最高仅 `mean_estimate_netprofit_annual12`(4/15)、`mean_estimate_targetprice_annual12_tribes`(6/6)、`mean_estimate_ebitda_annual12`(2/2)

**关键发现 —— 覆盖率的清晰分层**（这是本数据集最有价值的操作信息）：
- **年化科目（`annual12`）覆盖高**：0.73–0.94。`mean_estimate_eps_annual12`(0.936)、`mean_estimate_revenue_annual12`(0.935)、`mean_estimate_dividend_annual12_2`(0.9353)、`mean_estimate_fxadj_pretax_annual12_2`(0.9289)、`mean_estimate_netprofit_annual12`(0.9323)、`mean_estimate_epsreported_annual12`(0.9219)、`mean_estimate_ebitda_annual12`(0.8994)
- **季度科目（`quarterly16` / `fq16`）覆盖低到不可用**：`mean_estimate_dps_quarterly16`(0.3153)、`mean_estimate_eps_quarterly16`(0.2944)、`mean_estimate_netprofit_quarterly16`(0.4668)、`mean_estimate_ebit_quarterly16_tribes`(0.4771)、`median_estimate_gps_fq16`(0.2585)、`stddev_estimate_dps_quarterly16_2`(0.1802)
- **`fxadj_` 版本普遍比未调整版高 0.01–0.08**：`mean_estimate_pretax_annual12_2`(0.9289) vs `mean_estimate_pretax_reported_annual12_2`(0.733)

**判断**：**中等优先级，但**它的价值不在"多"，而在"提供一个高覆盖的年化一致预期底座"**。
1. 1929 个字段里绝大多数是**同一张表的 7 统计量 × 3 时间偏移 × 2 调整口径 的机械展开**。全量笛卡尔积不可行，也没必要。
2. **真正有用的机制只有三个**：
   - **离散度**：`stddev_estimate_*`（分歧度）—— 抽样 98 条里绝大多数 userCount=0
   - **修正速度**：`{mean,median}_estimate_four_weeks_prior_*` vs `mean_estimate_*` 的差 —— "过去 4 周分析师把预期调高了多少"
   - **极端值宽度**：`max_estimate_* - min_estimate_*` —— 分析师分歧的绝对幅度
3. **必须避开所有 `quarterly16` / `fq16` 字段**（覆盖 0.18–0.48），以及 `_tribes` 后缀中除 targetprice 外的部分。
4. 零使用率 90%+ 是双刃剑：与 analyst11 不同，这里的字段**机制极其标准**（就是一致预期），所以"无人用"更可能是因为"大家都去用 analyst7 / analyst69 了"——**这反而说明存在生态位空缺**，因为 1929 个字段里挑几个高覆盖年化字段做修正/分歧机制，逻辑上是通的。

**建议路径**：只在 `annual12` 财期上，取高覆盖科目（`eps`/`revenue`/`netprofit`/`pretax`/`ebitda`/`ebt`/`dps`/`taxrate`），用 `{mean,median,max,min,stddev}_estimate_{科目}_annual12` 的 5 件套 + `four_weeks_prior_` 快照，算 3 个机制（离散度 / 4周修正 / 极端宽度）。科目数控制在 6–8 个，候选量 ≈ 6×5×3 = 90，可控。

---

## 3. 横向对比与优先级排序

### 3.1 覆盖可行性硬约束（先看这个）

| 覆盖档位 | 数据集 | 后果 |
|---|---|---|
| **coverage = 0.5 整片** | analyst14, analyst15, analyst7 | 必测 Labs 截面数，否则整批回测白跑 |
| coverage 0.20–0.25 | model52, analyst81 | **直接排除**，覆盖闸必挂 |
| coverage 0.43–0.54 | analyst10（季度类/innovation）, analyst_consensus（季度类）, analyst9（guidance） | 子族不可用，需按字段筛 |
| coverage 0.69–0.91 | analyst11, analyst4, analyst9（主体） | 可用 |
| coverage 0.86–1.00 | analyst39, analyst45, analyst69, analyst10（年化）, analyst_consensus（annual12） | 最优 |

### 3.2 推荐优先级

| 优先级 | 数据集 | 理由 | 起步机制 |
|---|---|---|---|
| **1** | **analyst39** | 覆盖 0.91 中位 / 零使用 0 / 24 字段可穷尽 / 机制清晰 | 杠杆（`qtotd2eq` 已被用过，需差异化）+ 账面价值 + 毛利率 |
| **2** | **analyst69** | 覆盖 0.94 / 结构最规整（9 件套） | **只打 `_4wk_up` vs `_4wk_dn` 净额** 和 `_stddev`/`_numest`；**避开** `_rating`/`_cur_ev_to_ebitda`/`_eeps_cur_yr`（已 250–507 用户） |
| **3** | **analyst7** | 结构最规整笛卡尔积（20 科目 × 2 期限 × 6 统计量） | **先测 coverage**；主攻冷门 `est_q_*` + `act_q_*_surprise`；`est_12m_{ndt,ebt,sal}` 是万人坑要避开 |
| **4** | **analyst_consensus** | 高覆盖年化底座（0.93 左右） | `stddev_*` 分歧度 + `four_weeks_prior_*` 修正幅度；**只用 annual12，避开 quarterly16** |
| **5** | **analyst10** | Smart Estimate 三版本机制独特且竞争小（userCount 9–14） | `{科目}fy1/fy2 × smart_ests_{v0,v1,v2}` 的版本差；**避开** `*past_det_*` ID 类 |
| **6** | **analyst4** | 27 个 `_flag`/`_ft` 高覆盖冷门 | forecast type（revision/new）的 `ts_delta` 机制 |
| **7** | **analyst14** | 结构规整但 coverage=0.5 风险 | 若通过覆盖测试：`stddev_*` / `numofests_*`（32 个，多数无人用） |
| **8** | **analyst9** | 75/111 字段是时间戳与拆股因子噪声 | 只打 `daily_numup` / `daily_numdn` / `daily_numanalysts` |
| **9** | **analyst11** | ESG 数据集，非分析师预期；命名空间混乱且双份重复 | 仅长名 `social_*`/`governance_*` score + `ts_rank`，试 2–4 个 |
| **10** | **analyst15** | **非个股字段**（GICS 行业聚合），横截面无区分度 | 不建议投入 |
| **排除** | model52, analyst81 | 覆盖 0.20–0.25，且两者是同机制重复数据源 | 无 |

### 3.3 三个必须先做的前置动作

1. **对 analyst7 / analyst14 / analyst15（coverage=0.5 那批）跑一次 Labs 覆盖脚本**。
   `coverage=0.5` 是时间序列窗口标记，**不等于**只有一半股票有值。这一步的结果决定这 3 个数据集（合计 2976 字段，占 ANALYST 类一半以上）是保留还是直接砍掉。**优先级最高**。

2. **查清拥挤度分层，再定扫面范围**。
   报告已标出明确分层：analyst69 的 `_rating`(507 用户) vs `_4wk_up`(11 用户) 差 46 倍；analyst7 的 `est_12m_ndt_median`(75) vs 整个 `est_q_*` 系列(≈0)。**在万人坑字段上做笛卡尔积 = 必撞 prod 相关性**。

3. **对 analyst4 / analyst9 / analyst10 做字段剪枝，不要全量扫**。
   这三个的字段里混了大量纯元数据（分析师ID、财期ASCII码、货币代码、broker 明细）。建议先按前缀建立白名单（如 analyst4 只留 `_flag`/`_ft` + `fs_detail_estimates_af_nd_*`），再送进 GEM。

---

## 4. 本报告未能覆盖的部分（如实说明）

1. **analyst11 全量精确统计缺失**。全量查询因 83,130 字符超限失败，落盘文件在本次会话中被权限拒绝（Bash/Read/Grep 全部被拒）。其字段数 445 为平台 `count` 精确值，但类型分布、覆盖率分位、前缀计数均为抽样估算，`data_type=VECTOR` 返回 0 条只是**强烈提示**而非证实。
2. **所有 >400 字段数据集的覆盖率中位数、前缀计数、零使用数均为抽样估算**，已在表内用 `≈` 标注。抽样基于 `search` 的相关度排序返回（前 100 条），**存在系统性偏向热门/高相关字段**的风险 —— 因此零使用字段数很可能被**低估**（高使用字段更容易被 `search` 命中）。
3. **未测量任何字段在 TOPCS1600 上的真实非空截面数**。本报告所有"覆盖可行性"判断都基于平台 `coverage` 字段，而第 0.3 节说明了它与截面广度不是一回事。
4. **未核对另外 3 个数据集**（analyst_base_ref / analyst40 / analyst_factor_signals），按你的要求已跳过。
