# DEU 未点亮塔挖掘战役 · 设计底稿（2026-10-29）

对象：DEU / TOP500 / D1，未点亮塔 11 类（pv, news, earnings, insiders, sentiment, socialmedia, risk, shortinterest, macro, option, imbalance）。
机器数据源：`data/wqb.db` 的 `field_profile_deu`（22,494 字段，14,494 已测）、`backtest_results`、平台投影（2026-10-28 `get_pyramid_multipliers`）。
本文只记录**已验证事实 + 设计取舍**，结论性战绩另见复盘报告。

> **交付口径（2026-10-29 晚更新，逐条可复核）**：本战役累计交付 **67 颗 regular alpha**（全部 DEU/TOP500/D1、IS 2014-01-01–2023-12-31 满十年）：
> 首批 20（§7.1 = wave A 的 18 条 + risk60 覆盖位 2 条）+ 第二批 **39**（§7.14，wave `s2_unlit_tower_b_20261029`）+ 近闸定向 **8**（§7.15，wave `s4_shorti_lvl_flip_20261029`）。
> **ATOM 65/67 = 97%**：两条例外 `j2Ym1PL9`/`RREWdlXe` 是「借券门 + 分析师修正」的两数据集组合，
> 平台 `checks` 里也确带 `IS_LADDER_SHARPE`（ATOM 硬判据是「有 `LOW_2Y_SHARPE` 且无 `IS_LADDER_SHARPE`」）。
> **67 颗里独立信号核 62 个**（只读实测、按 `reverse(f) ≡ −f` 归一：1 颗精确重复 `npv016jE ≡ ZYQLOx60`
> + 4 组同核反向镜像，见 §7.15 去重一节）—— 按 alpha ID 计 67 颗、超目标 7 颗；按独立信号核计 62 个、超目标 2 个。
> **未新增点亮塔**，也未新增近闸候选（借券单信号上限 S≈1.06，闸 1.58）。

## 1. 塔位现状（平台实测）

已点亮 5 类：institutions 1、model 1、other 2、analyst 1、fundamental 1。
未点亮 11 类：pv、news、earnings、insiders、sentiment、socialmedia、risk、shortinterest、macro、option、imbalance。
DEU 无 news 类金字塔 multiplier 记录外的可用数据集极少（news18/news20 字段以 VECTOR 事件文为主，覆盖率 0.69–0.98，单信号 S 最大 0.48）。

## 2. 字段画像（`field_profile_deu` 实测，按 category）

| category | 字段数 | 已测 | 单信号 S≥1 | 单信号最高 S | 最高 2Y | 判读 |
|---|---:|---:|---:|---:|---:|---|
| MODEL | 8173 | 197 | 33 | 1.71 | 1.91 | 唯一有稳定单信号的地盘（estimate/surprise/score），但已被 book 占满 |
| ANALYST | 4312 | 123 | 17 | 1.70 | 2.14 | 第二强，estimate_change 系可作强腿 |
| OTHER | 3921 | 44 | 8 | 1.45 | 1.23 | dl_riskfree 系，多为概率/分位标签 |
| INSTITUTIONS | 66 | 20 | 1 | 1.06 | 1.78 | 只有 fund_holdings_panel 一个信号点 |
| FUNDAMENTAL | 2146 | 13 | 1 | 1.02 | 1.00 | 基本静态 |
| PV | 2877 | 23 | 0 | 0.78 | 1.06 | 单信号全灭；intraday_pv_feats 覆盖率 0.0 不可用 |
| INSIDERS | 42 | 4 | 0 | 0.75 | 1.06 | directional_indicator 是唯一活点（cov 1.0） |
| SHORTINTEREST | 25 | 13 | 0 | 0.73 | 1.28 | mean_loan_rate_main 最好（cov 0.687，S 0.73 / 2Y 1.28） |
| NEWS | 523 | 10 | 0 | 0.48 | 0.76 | 事件文本 VECTOR，全部 DEAD/DEAD_TURNOVER |
| RISK | 52 | 3 | 0 | 0.29 | 1.28 | lending_fee_bid_rate 有 2Y 无 S；rsk60_crowding 近似；risk72 覆盖率 0.0 |
| EARNINGS | 25 | 0 | 0 | — | — | **两集均 cov 0.0**（earnings6 18 字段 / earnings_sent_matrix 7 字段）⇒ DEU/TOP500/D1 无数据 |
| SENTIMENT | 276 | 0 | 0 | — | — | sentiment27（cov 0.90，但**只有 2019–2023**）/ sentiment7（10 年）/ sentiment33（cov 0.32）；本战役已否（§7.3、§7.11） |
| MACRO | 13 | 0 | 0 | — | — | macro27 = 招聘岗位数（VECTOR），**cov 0.0** ⇒ 不可用 |
| OPTION | 22 | 0 | 0 | — | — | option1 = delta surface / VI / moneyness（VECTOR），**cov 0.0** ⇒ 不可用 |
| IMBALANCE | 2 | 0 | 0 | — | — | imbalance5 = imb5_score / imb5_mktcap，**cov 0.0** ⇒ 不可用 |
| SOCIALMEDIA | 19 | 0 | 0 | — | — | socialmedia12 **cov 0.0** ⇒ 不可用（39/5 未在画像面内） |

**§2 修正（2026-10-29 复核，`field_profile_deu` 实测）**：初版把这 6 类写成「未测」是**错的**——
`earnings6` / `earnings_sent_matrix` / `macro27` / `option1` / `imbalance5` / `socialmedia12` / `risk72`
在 DEU/TOP500/D1 的**字段覆盖率全为 0.0**（`n_cov_pos=0`、`n_tests=0`，共 151 个字段无一条有数据）。
所以它们不是「还没挖」，是**这个宇宙取不到数**：未点亮塔里真正可挖的只有
SHORTINTEREST / SENTIMENT / NEWS / INSIDERS / RISK(risk60) 五族，本战役在**category / 高覆盖数据集层**已全部覆盖
（逐数据集分母见 §7.13；三个低覆盖 VECTOR 集仍属未测，不在「已覆盖」里）。

**核心判读**：未点亮塔的单信号上限全部 < 1.0（除 insiders 0.75 / shortinterest 0.73），
按 DEU skill 的判活标准（S≥1.58 且 2Y≥1.58 才算全闸候选）**单腿不可直接过闸**；
必须走「未点亮塔腿 × 强腿」或「未点亮塔内部多字段合成」，且强腿只能用 ANALYST / INSTITUTIONS / FUNDAMENTAL
（MODEL / OTHER / PV 受第 5 条组腿配额约束）。

**§2 的第二个维度：时间跨度（用户第 4 条，2026-10-29 补测）**。`cov` 只说明**当前**覆盖，不说明**历史跨度**。
用 `get_alpha_yearly_stats` 逐年代理实测（明细与处置见 §7.11）：

| 数据集 | 实际有持仓年份 | 跨度 | 合规 |
|---|---|---:|---|
| risk（`risk60.lending_fee_bid_rate`） | 2014–2023 | 10 | ✅ |
| SHORTINTEREST（shortinterest3） | 2014–2023 | 10 | ✅ |
| INSIDERS（directional_indicator） | 2014–2023 | 10 | ✅ |
| SENTIMENT（sentiment7 / snt7_views） | 2014–2023 | 10 | ✅ |
| SENTIMENT（sentiment27 / snl27_relpopularity1） | 2019–2023 | 5 | ✗ |
| INSTITUTIONS（institutions1） | 2018–2023 | 6 | ✗ |

⇒ 交付中所有 sentiment27 名额已剔除、institutions1 不再作为挖掘输入（双重出局：账户占用 + 跨度不足）。

### 2.1 数据集清单：逐个 category 的 MCP 平台实测（2026-10-29）

**方法**：`mcp__wq_brain_http__get_datasets(region='DEU', delay=1, universe='TOP500', category=<每个 category>)`，
**16 次按类调用**；覆盖率对账用 `mcp__wqb_db__get_field_catalog` / `get_mining_yield`，分母用 `field_profile_deu`。

| category | 平台集数 | cov>0 | 已回测 | 判死 | 未测(cov>0) | 判读 / 缺口 |
|---|---:|---:|---:|---:|---:|---|
| ANALYST | 18 | 8 | 7 | 3 | 2 | `analyst83`（345 字段全 VECTOR，cov 0.34）未测；`analyst48` cov 0.79 已判死 |
| MODEL | 49 (平台 45) | 22 | 10 | 3 | 12 | 最大余量面：`model26` 548 / `model109` 544 / `multifactor_return_pred` 648，但属已点亮塔 + 第 5 条配额 |
| OTHER | 42 (平台 41) | 12 | 8 | 7 | 5 | `insider_matrix` 33 字段 cov 0.55 未测（与 insiders 塔同源，注意性质重叠） |
| FUNDAMENTAL | 13 (平台 12) | 4 | 2 | 1 | 2 | `fundamental31` 48 字段 cov 0.40 / `fundamental45` 12 字段 cov 0.27 未测 |
| PV | 16 | 4 | 2 | 1 | 3 | `pv29` cov 1.0（50 字段）、`pv30` 285 字段（已判死）、`pv109` 26 字段（VECTOR） |
| NEWS | 17 | 6 | 4 | 1 | 2 | `news38` 3 字段 cov 0.60 未测；`news50` 8 探针判死 |
| RISK | 5 | 2 | 1 | 2 | 1 | 只有 `risk60` 可用（借券费率）；`risk88` 单字段判死；risk68/71/72 cov 0 |
| INSTITUTIONS | 5 | 4 | 3 | 0 | 1 | `institutions4` 6 字段全 VECTOR cov 0.34 未测 |
| SENTIMENT | 3 | 3 | 2 | 0 | 1 | `sentiment33` 255 字段 cov 0.32 未测；sentiment27 只有 2019–2023 已否 |
| INSIDERS | 2 | 2 | 2 | 0 | 0 | 已覆盖（`insiders1` 的行记在类别名键 `insiders` 上，台账瑕疵见 §7.13 C.3） |
| SHORTINTEREST | 1 | 1 | 1 | 0 | 0 | 唯一集 `shortinterest3` 已深挖（25 字段，9 个进过表达式） |
| SOCIALMEDIA | 2 | 1 | 0 | 0 | 1 | `socialmedia39` 1 字段 cov 0.27 未测；`socialmedia12` cov 0 |
| EARNINGS | 2 | 0 | 0 | 0 | 0 | 两集 cov 全 0 ⇒ DEU/TOP500/D1 取不到数 |
| MACRO | 1 | 0 | 0 | 0 | 0 | `macro27` cov 0 |
| OPTION | 1 | 0 | 0 | 1 | 0 | `option1` cov 0（22 字段 VECTOR 无数据） |
| IMBALANCE | 1 | 0 | 0 | 0 | 0 | `imbalance5` cov 0 |
| **合计** | **178（平台 172）** | **69** | **41** | **19** | **31** | 69 有覆盖 = **38 已回测 + 31 未测**；另有 3 个 cov=0 的集留下过历史探针回测行 ⇒ 已回测 41 |

**四条对账结论**：

1. **平台面 ⊆ 数据库面，且平台面少 6 个**：`fundamental31`、`model193`(98)、`model219`(1172)、`model230`(670)、
   `multi_horizon_alpha`(147)、`ml_factor_proj`(333) 只在画像里、平台按 region 标签不返回。前五个除
   `fundamental31` 外 cov 全 0；`fundamental31` 是真实可测缺口（48 字段 cov 0.40）。
2. **覆盖率逐项一致**：平台 `coverage` 与 `field_profile_deu` 的平均覆盖在 16 个 category 上**逐个吻合**
   （如 news104 0.963 / shortinterest3 0.7105 / risk60 0.835 / pv29 1.0），说明画像没有虚报。
3. **不分类的单次调用会截断**：同一组参数不带 `category` 只返回 **92** 集，按类分 16 次调用合计 **172** 集
   ⇒ 「平台数据集清单」必须**按 category 逐类枚举**，或直接用画像分母。§7.13 里「不能当分母」的判断由此得到确证。
4. **「挖完」的口径**：有覆盖的 69 集里 41 个已回测、19 个已判死、31 个未测（其中 5 个已判死重复计入判死面）。
   未测的 31 个里 **26 个是真实未测**，剩下 5 个是已判死（risk88 / other532 / analyst48 / news50 / model262）。
   这 26 个中，**未点亮塔目标面内只有 3 个**（`sentiment33` / `news38` / `socialmedia39`，全是低覆盖 VECTOR），
   其余 23 个属已点亮塔（MODEL/OTHER/PV/ANALYST/FUNDAMENTAL/INSTITUTIONS），按塔位策略不作主数据集。

## 3. 规则 5 组腿矩阵（硬约束）

- 禁止：PV/MODEL/OTHER 内部任意两两（PV+PV、PV+MODEL、MODEL+OTHER…）。
- 允许且**不计数**：未点亮塔之间、或与 ANALYST / INSTITUTIONS / FUNDAMENTAL 组腿。
- 允许但**全战役 ≤5 颗**：PV/MODEL/OTHER 之一 与 其它 category 组腿（如 MODEL+SHORTINTEREST、PV+OPTION）。
- 因此：现有 13 颗 IS 全过候选（全部是 MODEL+shortinterest/sentiment/risk）合计只能取 5 颗，
  且实测 prod 已 0.75–0.90（库内 stale 值），先按 0 颗可用处理；主力必须走 ANALYST 强腿。

## 4. 机制模板（论坛 + 外部论文取证）

> 本节是**设计稿**（7 条，按可查性排序）；**实际回测与判读见 §4.1** —— 最终落地 11 类独立机制（保守口径 10 类），另 4 类设计成型但被 DEU 数据挡住。

1. **借券成本 / 供给约束**（JFE 2005 *Short interest, institutional ownership, and stock returns*；JAE *Supply shortage*；Pearson *Anomalies and Their Short-Sale Costs*）
   - 机制：借券费率是卖空成本，费率高处 = 供给稀缺 + 看空拥挤；费率变化比水平更接近「供给边际」。
   - 落地：`-rank(ts_rank(vec_avg(mean_loan_rate_main), 60))`、`ts_delta(mean_loan_rate_main)`、`loan_rate_volatility` 作 squeeze 过滤。
2. **交易所做空量占比**（论坛 2025-10-12「基于 short interest 数据的跨交易所组合案例」）
   - 机制：`short volume / volume` 的 ts_rank，decay 250 压 turnover；多子交易所按成交量加权合成。
   - DEU 的 shortinterest3 无子交易所 short volume 字段，迁移其**结构**（ts_rank + 大 decay），不迁字段名。
3. **HV−IV 价差**（Goyal & Saretto, *Cross-Section of Option Returns and Volatility*；论坛 2025-11-05「期权隐含波动率价差因子」）
   - 机制：IV 相对 HV 的系统性偏离会均值回归；论坛变体用 `group_zscore(IV_put − IV_call, market)` 取极端做空。
   - 落地：DEU option1 只有单边 VI，改用 `ts_std_dev(returns,60) − vec_avg(opt1_p_deltasurface_d1_vi)`（PV+OPTION，占 5 配额）。
4. **招聘岗位增长**（macro27）
   - 机制：公司岗位数净增 = 扩张代理，与分析师修正正交；VECTOR 需 vec 聚合。
5. **内部人信念强度**（DEU 论坛实证模板，可迁移到未点亮 insiders 塔；论坛帖 43178926004887，JX84394，2026-09-02，69 赞）
   - 已提交实证 `xAjEkeOq`（DEU/TOP500/D1，institutions1 单数据集）：S 1.68 / F 1.34 / 2Y 2.40 / turnover 7.4% / margin 21.5bp / prod 0.52 / self 0.11 / ra=0。
   - 骨架：`ratio = 流量字段 / (存量字段 + ε)` → `ts_sum(ratio, 66)`（66=季度申报周期）→ `group_rank(·, industry)` → `winsorize(·, std=2)` → `tail(·, 0.25, 0.75, 0.5)`。
   - **核心机制（帖 §2.2 实测）**：稀疏事件数据 + `nanHandling=ON` 会把「当日无申报」填成 0；这些股票过 `ts_sum` 后仍为 0，在 `rank` 里形成**每天占横截面 72%–80% 的并列块**，且并列值落在 rank 中段（≈0.4）→ 组合把它当「中等信念」交易，`LOW_SUB_UNIVERSE_SHARPE` 被稀释到 0.45–0.70。`tail` 把中段统一置 0.5（中性化后权重归零），实测 **+0.24 Sharpe / +0.58 subU**；且 q 在 0.20–0.30 是平台（0.10 与 ≥0.35 才崩），属结构修正而非调参。
   - **反面铁律**：事件型数据必须 `ts_sum`，不能 `ts_mean`——`ts_mean` 的分母是「非 NaN 天数」，会把「一个季度申报几次」这个频率信息除掉（本例 1.44 → 0.73）。
   - DEU 落地字段：`institutions1` 属**已点亮** institutions 塔；未点亮 INSIDERS 塔有两个同构数据源 —— `insiders1`（VECTOR：`insd1_valueeur` / `insd1_holdings` / `insd1_shares` / `insd1_price` / `insd1_tradesignificance`，cov 0.534）与 `insider_agg_matrix`（MATRIX：total/avg buy/sell shares、`directional_indicator`，cov 0.534）。
   - 文献：Jeng-Metrick-Zeckhauser (2003, REStat) 买入有超额、卖出几乎无；Lakonishok-Lee (2001, RFS) 必须按规模标准化；Cohen-Malloy-Pomorski (2012, JF) 机会型 vs 例行。
6. **网络关注度**（sentiment27）
   - 机制：snl27_relpopularity / totaldomains = 散户关注度，关注度变化率做反转（attention fade）。
7. **借券费率的时序不确定性**（论坛 2026-09-20 `JX84394`「同一个排序，方差版能提交、标准差版被拦」64 赞，已提交 ASI alpha `npK8Vx1M` S 1.89 / F 1.54 / 2Y 1.63 / subU 1.66 / prod 0.6648；ERR 2018 *Short-Selling Risk* JF 73(2)；D'Avolio 2002 JFE 66；Cohen-Diether-Malloy 2007 JF 62）
   - 机制：空头怕的不是费率**高低**，而是费率**突然变贵 / 券被召回**；时序不确定性高 ⇒ 套利者系统性少做空 ⇒ 高估得不到纠正 ⇒ 未来收益更低。
   - 关键口径：要的是**同一只票跨日**的方差；厂商字段 `loan_rate_volatility_*` 是**同一天不同合约之间**的截面离散度，是另一个矩，**不能直接当它用**。
   - 模板：`reverse(group_zscore(ts_covariance(x, x, 22), exchange))`，x = `vec_avg(mean_loan_rate_main)`；`nanHandling=ON`（无成交日填 0，"从有费率到无费率"被记成一次召回跳变）。窗口 22 = 一个交易月（ERR 用月度波动），不是扫出来的。
   - 同帖三个**必须一起复现的反例**：① CV = std/mean 归一化把信号抹平（0.61）；② `ts_delta` 安慰剂 0.09 ⇒ 信号不是"费率在涨"；③ `ts_std_dev` 与 `ts_covariance(x,x)` 截面排序相同但**权重形状不同**，ASI 上 std 版被 robust 0.9 比例闸拦（1.70 < 1.78）而方差版过。
   - DEU 适配风险：`exchange` 在 DEU/TOP500 可能只有单一交易所（XETRA），`group_zscore(·, exchange)` 会退化成全局 z-score ⇒ 必须同时跑 `industry` 分组作对照，才能判定"分组"这一层在 DEU 是否有信息。

### 4.1 模板台账：11 类独立机制（保守口径 10 类，≥10 达标；2026-10-29 复核）

**口径**：一个「模板」= 一条**能独立陈述的经济机制** + 一个**独立的数据来源**。同一机制换窗口 / 换分组轴 / 换归一化口径 / 换算子形态 / 换中性化，算该模板的**对照实验**，不另计一类。按此口径本战役实际回测 **12 行 / 11 类独立机制**（#2 是同机制归一化对照，不计类）；若再把 #8/#9 两个「新闻分歧矩」合并成一类，仍有 **10 类** —— 两种口径都 ≥ 用户要求的 10。另有 4 类设计成型但被数据挡住的模板。

| # | 模板（机制） | 取证来源 | 代表 alpha / 表达式 | S / 2Y | 判读 |
|---|---|---|---|---|---|
| 1 | 借券费率**水平**（供给稀缺 + 看空拥挤） | JFE 2005 *Short interest, institutional ownership, and stock returns*；JAE *Supply shortage*；Pearson *Anomalies and Their Short-Sale Costs*；论坛 43607257389207（29 赞） | `JjeK5YPO` `-rank(ts_backfill(vec_avg(mean_loan_rate_main),252))` | 0.82 / **1.65** | 不死（TO 19.4% 偏高、IS 弱），该模板的强形态见 #3 / #4 |
| 2 | 借券费率**自身历史位置**（时序归一化） | 同 #1 的归一化对照（自设，**不计类**） | `A1VKOpMw` `ts_rank(·,250)` / `rKRXrqv9` `ts_zscore(·,250)` | 0.67 / 0.30；0.74 / 0.24 | 被水平版**支配** ⇒ 「费率高低」这一层不该做时序归一化 |
| 3 | 借券费率**时序方差**（borrow risk，怕的不是贵是突变） | 论坛 43624312881943（64 赞，ASI 已提交 `npK8Vx1M`）；ERR 2018 *Short-Selling Risk* JF 73(2)；D'Avolio 2002 JFE 66(2-3) | `1YN5X1qJ` `-group_zscore(ts_mean(ts_covariance(vec_avg(min_loan_rate_main),vec_avg(min_loan_rate_main),5),15),densify(industry))` | 1.32 / **1.86** | 最强 2Y；`gJezQX6K` 1.36/2.00 但 CW 不过 |
| 4 | 跨交易商费率**截面离散度**（同一天不同合约的分歧 = special 与 general 的分裂） | 论坛 43607257389207（special vs general collateral；费率+补库天数=拥挤）；自设 `vec_range` | `JjeLN31l` `-group_zscore(ts_mean(vec_range(min_loan_rate_main),15),densify(industry))` | 1.30 / 1.74（margin 34.8bp） | 唯一非 PASS 项 = LOW_SHARPE（差 0.28） |
| 5 | 借券门控 × **分析师修正主信号**（单主信号 + 风险过滤，非加权混腿） | SOP 8 问（分析师修正 × 供给约束） | `j2Ym1PL9` `trade_when(rank(ts_backfill(vec_avg(mean_loan_rate_main),252))<0.7, rank(ts_mean(eps_y1_estimate_change_3mo,22)), -1)`；`RREWdlXe` 换 netprofit 口径 | **1.57 / 1.13**；1.52 / 1.25 | **全战役唯一近闸**（缺口 0.01） |
| 6 | 内部人**流量 / 存量**（信念强度骨架，`ts_sum` 不能 `ts_mean`） | 论坛 43178926004887（69 赞，JX84394）；Jeng-Metrick-Zeckhauser 2003 REStat；Lakonishok-Lee 2001 RFS；Cohen-Malloy-Pomorski 2012 JF | `1YNEnwXQ` `tail(winsorize(group_rank(ts_sum(divide(vec_sum(insd1_valueeur),add(vec_sum(insd1_holdings),0.0001)),66),industry),std=2),0.25,0.75,0.5)` | 0.13 / 0.30 | 死（DEU insiders1 cov 0.534，事件稀疏） |
| 7 | 内部人**方向 / 买压**（方向指示 + 买盘股数） | 论坛 43152032301591（43 赞，「被自己对照组证伪」的反例帖） | `N1N95XaX` `rank(ts_mean(directional_indicator,22))`；`KPJaw7NN` `tail(winsorize(group_rank(ts_sum(total_buy_shares,66),industry),std=2),…)` | -0.23 / -0.83；0.34 / 0.49 | 死（与论坛帖结论同向：买压本身不构成信号） |
| 8 | 新闻情绪**不对称**（bull/bear 概率差） | 论坛 18 票分歧度模板；SOP 8 问 | `9qxQE9Jr` `rank(ts_mean(vec_avg(nws104_prob_pos) - vec_avg(nws104_prob_neg), 5))` | -0.22 / -0.33 | 死（方向反了也只是 0.22 / 0.33，镜像口径同死） |
| 9 | 新闻情绪**离散度**（同日观点分歧，不是方向） | 同 #8 族的正交口径（自设） | `O0AvAEJY` `rank(ts_mean(vec_stddev(nws104_sentiment), 5))` | 0.74 / 0.62 | 弱，未过任何闸（本族最好） |
| 10 | 新闻**新颖度门控**（旧闻重发不算信息） | SOP 8 问 | `wpQVQe72` `trade_when(rank(vec_avg(nws104_novelty))>0.7, -rank(ts_mean(vec_avg(nws104_sentiment),5)), -1)` | -0.24 / 0.22 | 死（门控把样本切窄，主信号本身也弱） |
| 11 | **新闻-收益 R1**（信息反应强度） | 论坛 93 票 R1 模板 | `bl63xzW6` `rank(ts_corr(vec_avg(nws17_multiple_comp_nip), returns, 22))`；镜像 `9qxQGMaq` | 0.41 / -0.32；-0.41 / 0.32 | 死（**唯一用到 PV 字段 `returns` 的模板**，PV×NEWS 计入规则 5 配额） |
| 12 | 网络**关注度反转**（attention fade） | sentiment27 数据字典；SOP 8 问 | `88R1aAwz` `-rank(ts_backfill(vec_avg(snt7_views),22))`；`qMLqmKxv` `-rank(ts_delta(vec_avg(snl27_relpopularity1),5))` | -0.07 / -0.61；-0.08 / 1.45 | 死（`qMLqmKxv` 的 2Y 1.45 只覆盖 2019–2023，违反「近十年有数据」） |

**同机制变体（不另计一类）**：

- 借券**期限**门控 `MPYmGPno` `trade_when(rank(ts_backfill(vec_avg(average_loan_duration_days_main),252))>0.5, rank(ts_backfill(vec_avg(mean_loan_rate_main),252)), 0)`：-0.66 / -2.22 —— #5 结构换字段的**反向安慰剂**，同时证明「门控有效」不是结构本身带来的。
- risk60 **跨厂商**同机制迁移（同一「费率方差」机制换到 risk60 的 `lending_fee_bid_rate`，与 #3 的 shortinterest3 `min_loan_rate_main` 互为供应商口径对照）：`leAZ9GPA` `reverse(group_zscore(ts_std_dev(vec_avg(lending_fee_bid_rate),22),industry))` 0.49 / 1.69、`WjOm0z2G` 同式换 `ts_covariance` 0.34 / 1.63 —— 2Y 同量级、IS 更弱，说明「方差」这一层可迁移，但 shortinterest3 的字段质量更好。
- §6 W1-K~T 的**算子形态**展开：`s2_si3_vecdisp_d1` 下 `vec_range` `JjeLN31l` 1.30 / 1.74、`vec_stddev` `A1VdNLmQ` 1.27 / 1.78、`vec_count` 0.21（死）—— #4 的聚合算子阶梯。

**设计成型但被数据挡住的 4 类**（不算「未挖」，算「这条路在 DEU 无输入」）：

| 模板 | 取证 | 挡住的原因 |
|---|---|---|
| 交易所做空量占比 | 论坛 2025-10-12「基于 short interest 数据的跨交易所组合案例」 | DEU shortinterest3 无子交易所 short volume 字段，只能迁结构不能迁字段 |
| HV − IV 价差 | Goyal & Saretto *Cross-Section of Option Returns and Volatility*；论坛 2025-11-05 | option1 覆盖率 0.00 |
| 招聘岗位增长 | macro27 | macro27 覆盖率 0.00 |
| 需求评级 / 利用率 | 论坛 34407581314583（87 赞，EUR 三因子） | `shrt3_utilizationpercent_units` **DEU 不存在**；`shrt3_bar`（1–10 需求评级，cov 0.653）仅历史 W326 测过 S 0.85，且用的是**当时允许、现已禁的 OTHER 聚类分组轴**，按当前规则重跑需新开一波 |

**取证结构（诚实口径）**：

- **12 行里 4 行产出了有用东西**（#1 的 2Y 1.65 谱系、#3 的 1.86、#4 的 1.74、#5 的近闸 1.57），其余判死或偏弱 —— 与「先模板探信号、再定向精修」的原意一致：模板层的任务是把死路**便宜地**排掉。
- **外部取证的真实比例**：**论文 4 类**（#1、#3、#4、#6；#2 继承 #1 的文献）+ **论坛帖 5 类**（#3、#6、#7、#8、#11），两者重叠 #3、#6 ⇒ **7 类有外部锚点、4 类（#5、#9、#10、#12）来自 SOP 8 问与数据字典**（#2 为对照）。最硬的三条是 ERR 2018 的「借券风险 ≠ 借券成本」、Jeng 2003 的「内部人买入有超额、卖出几乎无」、D'Avolio 2002 的「借券市场分割（special vs general collateral）」。
- **论坛实读清单（本会话）**：3 篇正文 —— 43624312881943（64 赞，方差 vs 标准差）、34407581314583（87 赞，EUR short interest 三因子与需求评级）、43607257389207（29 赞，费率 + 补库天数 = 拥挤）；另检索命中 2 篇未改变结论的帖（43152032301591 内部人买压反例 43 赞、35238443276567 小盘内部人新闻情绪）。#8（18 票分歧度）与 #11（93 票 R1）的取证帖来自本战役前期检索，不在本次实读清单内。
- **缺口要说清**：DEU 自己的 `forum_recon` 台账只有 **4 条记录 / 1 个唯一问题**（「DEU shortinterest3 有无解法」），论坛取证主要来自**跨区同机制帖**（ASI/EUR/HKG），不是 DEU 专属经验。这是本战役的**研究深度缺口，不是数量缺口**；下一步若要补，应针对 `shrt3_bar` 与 `insiders` 两个具体问题各做一次波级取证。

**结论**：模板 **11 类独立机制**（把两个新闻分歧矩并成一类的保守口径 = 10 类）**≥ 10**，多样性覆盖 **5 个信号族** —— 借券供给（#1–#4，水平 / 时序方差 / 截面离散）、内部人（#6–#7，强度 / 方向）、新闻（#8–#11，不对称 / 离散度 / 新颖度门控 / 收益相关）、关注度（#12）、分析师修正（#5，作主信号被借券门控）；每类都配了对照实验（同字段换窗口、换轴、换归一化、换算子形态）—— 数量与多样性要求均已满足，无需为凑数再开波。

## 5. 波次设计（并发 2，create_multi_simulation 每批 2 条）

原设计里的 W1-C/W1-D（option1 / macro27 / imbalance5 / earnings）因覆盖率读 0.00 已降级；
W2 里的 `add(rank(A), rank(B))` 形态**全部取消** —— 它属于用户明令禁止的「两条独立信号加权相加」，
后续需要组腿时改为 `trade_when` 单主信号 + 风险过滤（不加权、不扫描权重）。实际执行序列：

| 批 | 表达式 | 塔 | 规则5 | 状态 |
|---|---|---|---|---|
| P1 | `rank(ts_mean(directional_indicator,22))`；`-rank(ts_delta(vec_avg(snl27_relpopularity1),5))` | insiders / sentiment | 0 配额 | ✅ N1N95XaX / qMLqmKxv 全灭 |
| P2 | `-rank(ts_backfill(vec_avg(mean_loan_rate_main),252))`；`-rank(ts_backfill(vec_avg(lending_fee_bid_rate),252))` | shortinterest / risk | 0 配额 | ✅ JjeK5YPO（2Y 1.65/subU 0.85）/ 78L9K0o2 |
| P3 | 论坛信念骨架 ×2（insiders1 金额比 / agg_matrix 买盘股数） | insiders | 0 配额 | ✅ 1YNEnwXQ / KPJaw7NN 全灭 |
| P4 | 同字段归一化对照：`ts_rank(·,250)`；`ts_zscore(·,250)` | shortinterest | 0 配额 | ✅ A1VKOpMw / rKRXrqv9（均劣于水平版） |
| P5 | `-rank(ts_backfill(vec_avg(snl27_relpopularity1),22))`；`-rank(ts_backfill(vec_avg(snt7_views),22))` | sentiment ×2 | 0 配额 | 🔄 在飞 |
| P6 | `reverse(group_zscore(ts_covariance(vec_avg(mean_loan_rate_main),vec_avg(mean_loan_rate_main),22),exchange))`；同式换 `ts_std_dev` | shortinterest | 0 配额 | 待发（**nanHandling=ON**，论坛方差模板） |
| P7 | 同方差式换 `industry` 分组；换窗口 66 | shortinterest | 0 配额 | 待发（分组/窗口归因） |
| P8 | **水平主腿精修**：`-rank(ts_backfill(vec_avg(mean_loan_rate_p5_d1),22))`（covered 0.783）；`-rank(ts_backfill(vec_avg(mean_loan_rate_main),22))`（backfill 22 vs 252 对照） | shortinterest | 0 配额 | 待发（**唯一有 2Y 1.65 的谱系**，nanHandling=OFF） |
| P9 | **W1-E 结论落地**：`reverse(group_zscore(ts_std_dev(vec_avg(mean_loan_rate_main),22), industry))`；`reverse(group_zscore(ts_covariance(vec_avg(mean_loan_rate_p5_d1),vec_avg(mean_loan_rate_p5_d1),22), industry))`（nanHandling=ON，与 P8 分开发批） | shortinterest | 0 配额 | 待发（industry 轴已验证把 CW 0.473→pass、DD 58%→20.6%） |
| P10 | `trade_when(rank(ts_backfill(vec_avg(mean_loan_rate_main),252))<0.7, rank(ts_mean(eps_y1_estimate_change_3mo,22)), -1)`；同式换 `netprofit_y1_estimate_change_3mo` | analyst × shortinterest | 0 配额（ANALYST×未点亮塔不计数） | 待发（**唯一可能过 S 1.58 的组腿路径**；单主信号 + 风险过滤，非加权混合） |
| P11（备选） | `-rank(ts_backfill(vec_avg(rsk60_offer),22))`（cov 0.835，跨厂商）；`-rank(ts_backfill(vec_avg(shrt3_bar),22))`（需求评级 1–10） | risk / shortinterest | 0 配额 | 备选（仅当 P8–P10 有落空时顶上凑数） |

判读口径（DEU skill）：S≥1.58 且 2Y≥1.0（阈值两档）→ 近闸；S 1.0–1.58 → 不死，升窗口/轴；两侧 <0.5 → 该机制判死。
每批完成后做**归因对比**：同字段换窗口（5/22）、换聚合（vec_avg/vec_sum）、换中性化（SUBINDUSTRY/INDUSTRY）各留一条对照。

## 6. 首波实测与波次修订（2026-10-29）

**W1-A 实测（2/2 完成，均 DEAD）**

| alpha | 表达式 | S | 2Y | turnover | 判读 |
|---|---|---:|---:|---:|---|
| N1N95XaX | `rank(ts_mean(directional_indicator,22))` | -0.23 | -0.83 | 0.310 | longCount 35、CONCENTRATED_WEIGHT 0.181>0.1 |
| qMLqmKxv | `-rank(ts_delta(vec_avg(snl27_relpopularity1),5))` | -0.08 | 1.45 | 0.313 | subU -0.40、ra_failed 5 |

归因：两条都踩了论坛模板的两个坑 —— 对稀疏事件数据用 `ts_mean`/`ts_delta`（吃掉事件频率、保留 0 原子），
且没有 `tail` 掐掉 nanHandling 造出的并列中段。turnover 0.31 与 longCount 35 正是「全横截面被同一个中段值交易」的指纹。
**结论：单信号 + 均值类算子 = 结构性死亡，不是窗口/参数问题。**

**W1-A′（论坛骨架重打 INSIDERS，未点亮塔，0 配额）** —— 两条均过 `validate_expressions`（3/3 字段存在）

1. `tail(winsorize(group_rank(ts_sum(divide(vec_sum(insd1_valueeur), add(vec_sum(insd1_holdings), 0.0001)), 66), industry), std=2), lower=0.25, upper=0.75, newval=0.5)`
2. `tail(winsorize(group_rank(ts_sum(total_buy_shares, 66), industry), std=2), lower=0.25, upper=0.75, newval=0.5)`

对照设计：1 是「金额口径 × 自身持仓」，2 是「股数口径 × 无分母（靠 group_rank 做截面标准化）」；
同骨架换分子/分母即构成归因对比，符合帖 §5.4「用量纲变化检验信号来源」。

**W1-A′ 实测（2/2 完成，未点亮塔 INSIDERS 仍不点亮）**

| alpha | 表达式 | S | F | 2Y | subU | turnover | long/short | ra_failed |
|---|---|---:|---:|---:|---:|---:|---|---|
| 1YNEnwXQ | insd1_valueeur / insd1_holdings（金额/持仓比） | 0.13 | 0.04 | 0.30 | 0.02 | 0.075 | 43/42 | 5（含 CW 0.194） |
| KPJaw7NN | `ts_sum(total_buy_shares,66)`（买盘股数） | 0.34 | 0.15 | 0.49 | **0.62** | 0.073 | 48/66 | 3（S/F/2Y） |

归因三条：
1. **骨架迁移成功、机制迁移失败**。turnover 从 W1-A 的 0.31 降到 0.073，longCount 从 35 升到 43–48，
   说明 `ts_sum + group_rank + winsorize + tail` 确实修掉了「并列中段被整段交易」的结构病（W1-A 的死因），
   但信号本身在 DEU 内部人数据上没有横截面区分力 —— 是**字段/sample 问题，不是形态问题**。
2. **买卖口径不对称**：买盘股数（KPJaw7NN）的 subU 0.62 明显优于金额/持仓比（1YNEnwXQ）的 0.02，
   与 Jeng-Metrick-Zeckhauser(2003)「内部人买入信号强于卖出」一致；但 2Y 0.49 说明它不是稳定慢变量，
   2022–2023 贡献了主要收益，属于**阶段性事件行情**而非可复现机制。
3. **样本天花板**：MAC 2016 / MiFID II 后 DEU 申报才密集，有效账本约 6 年（见下条年限提示），
   在 TOP500 上每条再被 `tail` 掐掉 50% 横截面 → 实际下注样本过薄，S 的抽样误差远大于 0.13 这个数本身。

**结论：INSIDERS 从「主攻机制」降级为「已记录负结果」**；除非后续改用「卖出侧 masked 信号 + 与
ANALYST 强腿组腿」的形态，否则不再单独投配额。塔位状态：DEU/D1/INSIDERS 仍 0/3。

**数据年限提示（交付时必须显式说明）**：DEU 内部人有效申报样本自 2018 起（欧盟 MAR 2016、MiFID II 2018），
2014–2017 覆盖极薄；论坛母版也是 2018–2023 六个交易年账本。若 W1-A′ 过闸，需标注「有效账本 6 年」，
不能声称满足「近十年全段有数据」。

**W1-B 实测（2/2 完成）**

| alpha | 表达式 | S | F | 2Y | subU | turnover | 判读 |
|---|---|---:|---:|---:|---:|---:|---|
| JjeK5YPO | `-rank(ts_backfill(vec_avg(mean_loan_rate_main),252))` | 0.82 | 0.45 | **1.65** | **0.85** | 0.194 | 只卡 LOW_SHARPE/LOW_FITNESS，**2Y 与 subU 已过**——未点亮塔里唯一「双副闸已过」的单信号 |
| 78L9K0o2 | `-rank(ts_backfill(vec_avg(lending_fee_bid_rate),252))` | 0.83 | 0.60 | 1.15 | 0.30 | 0.067 | 4 项 fail，subU 0.30 远低于 0.39 线 |

归因：两者都是「借券成本水平」的同一机制（借贷供给），差异来自字段口径——`mean_loan_rate_main` 的横截面
离散度更高（longCount 101 vs 119、margin 6.1bp vs 19.4bp），因此 subU 与 2Y 显著更好。
**结论：shortinterest 机制在 DEU 未点亮塔里是最强的一条（S 0.82 距 1.58 仍有 1.9 倍差距，单信号无法过闸），
必须靠 ANALYST 强腿抬 S/F；risk 的 lending_fee 只能作备选。**

**W1-B′ 实测（同字段水平 vs 自身历史归一，干净归因对照）**

| alpha | 归一方式 | S | F | 2Y | subU | turnover | long/short | ra_failed |
|---|---|---:|---:|---:|---:|---:|---|---|
| JjeK5YPO | 无（横截面 rank，基准） | **0.82** | **0.45** | **1.65** | 0.85 | **0.194** | 101/98 | S/F |
| A1VKOpMw | `ts_rank(·,250)` | 0.67 | 0.26 | 0.30 | 0.81 | 0.326 | 83/83 | S/F/CW/2Y |
| rKRXrqv9 | `ts_zscore(·,250)` | 0.74 | 0.32 | 0.24 | **1.00** | 0.294 | 83/83 | S/F/CW/2Y |

归因：**借券费率的 alpha 在「横截面水平」里，不在「自身历史偏离」里**。两种自身历史归一都把 2Y 从 1.65 打到
0.24–0.30（−82%），turnover 反而从 0.19 升到 0.29–0.33，并且新出现 CONCENTRATED_WEIGHT（longCount 101→83）。
机制解释：横截面水平刻画的是「谁难借、谁被看空」的**结构性分层**，这种分层在 2014–2023 全段稳定、天然分散；
自身历史归一把它变成「某只票比平时更难借」的**择时信号**，只剩下少数跳变样本承担收益，2Y 段尤其空。
这与 §4 第 1 条论文口径一致：供给约束是**水平型**约束，不是动量型信号。
**结论：shortinterest 主腿定型为水平式 `-rank(ts_backfill(vec_avg(mean_loan_rate_main),252))`，不再做归一化调参；
后续只走「换机制腿」而非「改形态」。**

覆盖率数据纠正：`option1` / `macro27` / `imbalance5` / `earnings6` 在 DEU 的字段覆盖率读数为 0.00
（`UNKNOWN_COVERAGE` 哨兵或确为 0），原 W1-C/W1-D 计划用这三类做单信号探针**成本高收益低**，降级为最后备选；
SENTIMENT 侧改用有实测覆盖的 `sentiment27`（0.90）与 `sentiment7`（Wikipedia 浏览，0.74）。

**W1-C 实测（关注度水平，跨两个独立代理复现）**

| alpha | 表达式 | S | F | 2Y | subU | turnover | 判读 |
|---|---|---:|---:|---:|---:|---:|---|
| npvVZ0jl | `-rank(ts_backfill(vec_avg(snl27_relpopularity1),22))` | -0.60 | -0.37 | -1.73 | -0.40 | **0.0175** | 符号与 Barber-Huang-Odean-Schwarz 相反 |
| 88R1aAwz | `-rank(ts_backfill(vec_avg(snt7_views),22))` | -0.07 | -0.01 | -0.61 | 0.44 | 0.098 | 无信号 |

归因（三条，都是可复用的负结论）：
1. **符号反了，而且不是巧合**：`-rank(注意力)` 得 -0.60，意味着**高关注度在 DEU 预示更高收益**。
   美股「散户关注度 → 未来 20 日 -4.7%」在 DEU 不成立，更接近「关注度 = 质量/大盘代理」。
   若要做，应改 `+rank`，但那会与 momentum/quality 家族高度同源，撞 prod 墙的概率高。
2. **turnover 1.75% 是判决书**：关注度水平几乎不换手 ⇒ 它是**慢 beta 暴露**，不是可交易的 alpha；
   即使符号翻正，S 也只有 0.60，且 2Y -1.73 说明近两年完全反向。
3. **换代理不复现**：Wikipedia 浏览量（完全独立的数据源）S -0.07，说明不是 snl27 的厂商问题，
   是「DEU 上没有 attention→reversal 这条机制」。
**结论：SENTIMENT 塔的关注度方向判死（两个独立代理 + 一个变化率版本 qMLqmKxv 三连否）；塔位仍 0/3。**

**W1-D 实测（论坛「费率时序方差」模板在 DEU 的复现，nanHandling=ON）**

| alpha | 表达式 | S | F | 2Y | subU | turnover | margin | drawdown | long/short | ra_failed |
|---|---|---:|---:|---:|---:|---:|---:|---:|---|---|
| 78L9aY2O | `reverse(group_zscore(ts_covariance(x,x,22),exchange))` | 0.67 | 0.69 | 0.25 | 0.35 | 0.108 | 24.5bp | **58.2%** | 109/63 | S/F/**CW 0.473**/2Y |
| 3qoLa02O | `reverse(group_zscore(ts_std_dev(x,22),exchange))` | 0.88 | 0.81 | 0.64 | 0.59 | 0.086 | 24.8bp | 40.8% | 102/70 | S/F/**CW 0.156**/2Y |

归因（三条）：
1. **ASI 的「方差 vs 标准差」结论在 DEU 反转**：ASI 上方差版过 robust、std 版被拦；DEU 上 **std 全面优于方差**
   （S 0.88 vs 0.67、2Y 0.64 vs 0.25、DD 40.8% vs 58.2%、CW 0.156 vs 0.473）。机制解释：DEU/TOP500 只有 500 只票、
   借券市场参与者少，方差把尾部权重推满 truncation 后，**多空腿失衡**（109/63、102/70），集中度直接爆掉；
   ASI 的 MINVOL1M 有 2000+ 票，尾部还有分散空间。**同一模板的可迁移性取决于 universe 宽度，不是区域。**
2. **nanHandling=ON 的代价**：margin 从水平版的 6.1bp 抬到 24.5–24.8bp（说明"召回跳变"确实带来了信息），
   但 drawdown 从 13.7% 恶化到 40.8–58.2%。无成交日填 0 在 TOP500 这种薄市场上制造了大量假跳变。
3. **2Y 一致崩塌**（0.25 / 0.64 vs 水平版 1.65）：三条 shortinterest 变体（归一化、方差、std）**全部**在近两年失效，
   只有**水平式**在 2022–2023 还有 1.65。这是本战役最强的单条证据：**DEU 的借券 alpha 只能是慢变量水平型**。
**结论（后被 W1-E 修正为「分组轴错、不是机制死」）：shortinterest 主腿仍是 JjeK5YPO 水平式。**

**W1-E 实测（分组轴 / 窗口归因 —— 本战役最关键的一次对照）**

| alpha | 变化 | S | F | 2Y | subU | turnover | margin | drawdown | CW | ra_failed |
|---|---|---:|---:|---:|---:|---:|---:|---:|---|---|
| 78L9aY2O | 方差 @ `exchange`，W22 | 0.67 | 0.69 | 0.25 | 0.35 | 0.108 | 24.5bp | 58.2% | **0.473 挂** | 4 |
| **wpQg5xZp** | 方差 @ **`industry`**，W22 | **0.95** | 0.75 | **1.10** | 0.62 | 0.089 | 17.7bp | **20.6%** | **过** | 3 |
| akKvNZbv | 方差 @ `exchange`，**W66** | 0.81 | 0.89 | 0.37 | 0.51 | 0.055 | 54.0bp | 54.6% | 0.378 挂 | 4 |

归因（这是整轮里最有迁移价值的一条）：
1. **DEU 的 `exchange` 轴是退化的**（XETRA 单交易所），`group_zscore(·,exchange)` 实际等于全局 z-score，
   于是权重被少数费率跳变最猛的票吃满 truncation → CW 0.473、DD 58%。换成 `industry` 后同一表达式
   **CW 转安、DD 从 58% 降到 20.6%、2Y 从 0.25 抬到 1.10**，S 也升到 0.95。论坛在 ASI 上强调「必须用制度边界
   exchange、industry 会 FAIL」，**这条在 DEU 正好相反**：单交易所市场里 industry 才是有效分组轴。
2. **窗口 22 是自然尺度**：W66 把 margin 抬到 54bp 但 2Y 掉到 0.37、CW 0.378 挂 —— 与论坛「22 天 = 一个月、
   66 天全面衰减」的结论一致，**不是扫出来的，是机制半衰期**。
3. 修正上一条结论：方差/波动机制**没死**，死的是分组轴选择。当前 shortinterest 最强形态有两条并列：
   水平式 JjeK5YPO（S 0.82 / 2Y **1.65** / subU **0.85**）与方差-industry wpQg5xZp（S **0.95** / 2Y 1.10 / DD 20.6%）。

**W1-F 实测（水平式的 backfill 窗口 / 字段口径对照，nanHandling=OFF）**

| alpha | 表达式 | 覆盖率 | S | F | 2Y | subU | turnover | margin | drawdown | long/short | ra_failed |
|---|---|---|---:|---:|---:|---:|---:|---:|---:|---|---|
| JjeK5YPO | `mean_loan_rate_main` backfill **252** | 0.687 | **0.82** | **0.45** | **1.65** | **0.85** | 0.194 | 6.06bp | 13.7% | 101/98 | S/F |
| 9qx09por | `mean_loan_rate_main` backfill **22** | 0.687 | 0.76 | 0.39 | 1.25 | 0.74 | 0.216 | 5.37bp | 13.8% | 88/85 | S/F/2Y |
| 1YNEopE6 | `mean_loan_rate_p5_d1` backfill 22 | **0.783** | 0.68 | 0.31 | 1.26 | 0.50 | 0.222 | 4.14bp | 11.7% | 114/111 | S/F/2Y |

归因：
1. **窗口方向已被两个独立对照夹住**：252 优于 22（S 0.82 vs 0.76、2Y 1.65 vs 1.25、subU 0.85 vs 0.74、turnover 更低），
   与 W1-B′「自身历史归一（250 日窗）杀 2Y」并不矛盾——**长窗是平滑输入，不是把信号变成择时**
   （`ts_backfill(·,252)` 只做前向填充，度量仍是横截面水平；`ts_rank(·,250)` 才把水平改成时序分位）。
   因此 252 定为最终参数，不再往上/往下扫。
2. **高覆盖率字段反而更弱**：`_p5_d1` 口径覆盖率 0.783（vs main 0.687）却在全部维度更差（S −17%、2Y −24%、subU −41%、margin −32%）。
   说明这条机制的瓶颈不是样本宽度，而是**费率口径的信息密度**——`_p5_d1` 混入了更多低信息档的合约。
   **结论：覆盖率不是本族的约束条件，不要为提高覆盖换字段。**
3. 三条水平式（252 main / 22 main / 22 p5_d1）全部 CW 通过、DD ≤ 13.8%，说明水平式的风险结构稳定；
   它们的共同短板仍是 S/F（0.68–0.82 vs 1.58/1.0）→ **单信号不可能过闸，必须靠 ANALYST 强腿（P10）**。

**W1-G 实测（方差机制 2×2 完整析因：算子 × 分组轴，外加字段口径）**

| alpha | 算子 | 分组轴 | 字段 | S | F | 2Y | subU | turnover | margin | DD | CW |
|---|---|---|---|---:|---:|---:|---:|---:|---:|---:|---|
| 78L9aY2O | variance | exchange | main | 0.67 | 0.69 | 0.25 | 0.35 | 0.108 | 24.5bp | 58.2% | 0.473 挂 |
| 3qoLa02O | std | exchange | main | 0.88 | 0.81 | 0.64 | 0.59 | 0.086 | 24.8bp | 40.8% | 0.156 挂 |
| wpQg5xZp | variance | **industry** | main | 0.95 | 0.75 | 1.10 | 0.62 | 0.089 | 17.7bp | 20.6% | **过** |
| **gJepxE2m** | **std** | **industry** | main | **0.98** | **0.76** | **1.30** | 0.54 | 0.084 | 18.1bp | 20.1% | **过** |
| wpQgLMr2 | variance | **industry** | **p5_d1** | 0.93 | 0.69 | **1.30** | 0.63 | 0.088 | 15.6bp | **17.8%** | **过** |

析因结论（2×2 把 W1-D/W1-E 混在一起的两个因子彻底拆开）：
1. **分组轴是主效应，且远大于算子选择**：exchange→industry 在方差上把 2Y 从 0.25 抬到 1.10（+0.85）、
   DD 58%→20.6%（−38pt）、CW 0.473→过；在 std 上把 2Y 从 0.64 抬到 1.30（+0.66）、DD 40.8%→20.1%（−21pt）、CW 0.156→过。
   **同一个表达式只换分组轴就从"三闸挂"变"只挂 S/F 两闸"，这是本战役最大的一步增益。**
2. **算子在 DEU 上 std 微弱优于 variance**（exchange 0.88 vs 0.67；industry 0.98 vs 0.95；2Y 1.30 vs 1.10），
   与 ASI 论坛「方差版过 robust、std 版被拦」**相反**，但差异幅度（ΔS ≈ 0.03–0.21）小于分组轴（ΔS ≈ 0.28–0.30）。
   机制：TOP500 只有 500 票，方差版把尾部权重推得更极端 ⇒ long/short 失衡更大（144/81 vs 102/70），
   在窄 universe 上方差的高阶矩优势反而变成集中度代价。
3. **字段口径的作用依赖几何，W1-F 的结论需要按形态分开读**：水平式里 `p5_d1` 明显更弱（1YNEopE6 全面差于 main），
   但方差式里 `p5_d1` **≥ main**（wpQgLMr2 2Y 1.30 vs wpQg5xZp 1.10、DD 17.8% vs 20.6%、subU 0.63 vs 0.62）。
   机制解释站得住：**方差是从整条合约面板估出来的二阶量，合约越多估计越稳（要广度）；
   水平式取的是单条代表性费率，越"干净"的口径信息密度越高（要纯度）**。⇒ 选字段必须跟着几何走，不能全局定一条"好字段"。
4. 五条方差/波动候选的共同短板仍是 S 0.93–0.98 / F 0.69–0.76（需 1.58 / 1.0），
   2Y 最好 1.30 也差 0.28 到线。**shortinterest 单信号天花板 ≈ S 1.0，靠它自己到不了闸**——
   这也把 P10 的角色定死了：ANALYST 不是"锦上添花"，是过闸的必要条件。

**W1-H 实测（ANALYST 主腿 + 借券费风险过滤 —— 本战役唯一近闸候选）**

| alpha | 主信号（ANALYST） | S | F | 2Y | subU | turnover | margin | DD | long/short | 闸状态 |
|---|---|---:|---:|---:|---:|---:|---:|---:|---|---|
| **j2Ym1PL9** | `eps_y1_estimate_change_3mo` W22 | **1.57** | **1.33** | 1.13 | **0.95** | **0.0333** | **53.8bp** | **10.1%** | 124/120 | **fail=[]**；LOW_SHARPE 1.57/1.58、IS_LADDER 1.13/1.58 均为 WARNING |
| RREWdlXe | `netprofit_y1_estimate_change_3mo` W22 | 1.52 | 1.27 | **1.25** | 0.83 | 0.0340 | 51.6bp | 11.8% | 124/120 | 同上 + CLUSTER 0.91 WARNING |

归因（为什么这两条比单信号强一个量级，以及它合规在哪）：
1. **结构是「单主信号 + 风险过滤」，不是加权混腿**：`trade_when(借券费率 rank < 0.7, ANALYST 修正 rank, -1)`——
   主信号只有 ANALYST 修正一条，借券费率只做**可否交易的门**（裁掉最难借的 30% 股票），
   没有 `add()`、没有乘权重、没有扫描 0.4/0.6。这是用户明令禁止项之外唯一合规的组合形态。
2. **门的作用方向是"去掉拥挤空头"**：裁掉高费率段后 turnover 从 0.194 掉到 0.033（−83%）、
   margin 从 6.1bp 抬到 53.8bp（×8.8）、DD 从 13.7% 降到 10.1%、S 从 0.82 抬到 1.57。
   机制解释：高借券费=已被大量做空+难借，这类票上分析师修正信号最容易被挤空（short squeeze）反向打爆；
   把它们排除后，修正信号在"借券成本正常"的票上稳定兑现。
3. **塔位双计**：pyramid effective = 2（SHORTINTEREST ×1.3 + ANALYST ×1.8）。这不只是凑数——
   它同时给两个塔加分，是本战役唯一的多塔贡献候选。
4. **两条都只差临门一脚**：`checks.fail = []`（没有任何硬 FAIL），
   差的是 LOW_SHARPE（1.57 vs 1.58，**差 0.01**）与 IS_LADDER（2Y 1.13 vs 1.58）。
   eps 版 S 更高、netprofit 版 2Y 更高（1.25）——**两个字段在 S 与 2Y 上互补**，这是下一步改进的入口。

**W1-I 定向改进设计（近闸候选，干净对照，一次只动一个因子）**

| alpha | 相对 j2Ym1PL9 的唯一变化 | 目的 |
|---|---|---|
| 待测 A | ANALYST 腿 `rank(·)` → `group_rank(·, industry)` | 只换分组轴：抑制行业级修正潮，看 2Y 抬升 |
| 待测 B | ANALYST 腿平滑 `ts_mean(·,22)` → `ts_mean(·,66)` | 只换窗口：慢化修正信号，直接针对 IS_LADDER（2Y 1.13） |

（两条都为「改算子几何/改窗口」，不含任何权重或腿数变化；A、B 若各自有效，下一轮再合并成一条。）

**W1-I′ 实测（第一轮：分组轴 / 窗口，两条都退化）**

| alpha | 相对 j2Ym1PL9 的唯一变化 | S | F | 2Y | subU | turnover | DD | margin | CLUSTER |
|---|---|---:|---:|---:|---:|---:|---:|---:|---:|
| j2Ym1PL9 | 基准（全局 rank，W22） | **1.57** | **1.33** | **1.13** | **0.95** | 0.0333 | 10.1% | 53.8bp | 0.67 |
| d5WLQmE2 | `rank` → `group_rank(·, industry)` | 1.52 | 1.22 | 1.00 | 0.74 | 0.0407 | 9.3% | 39.4bp | 0.94 |
| E56JKbg0 | 平滑窗口 22 → 66 | 1.39 | 1.10 | 1.04 | 0.77 | 0.0255 | 13.3% | 61.0bp | 0.77 |

归因（两条都是可复用的负结论）：
1. **`industry` 分组在分析师修正腿上是有害的，与借券方差那条正好相反**：S −0.05、2Y −0.13、subU −0.21、
   CLUSTER 从 0.67 恶化到 0.94。机制：修正信号的收益里有一块是**行业级修正潮（板块轮动）**，
   `group_rank` 把行业内部排序之外的信息抹掉，再叠加 SUBINDUSTRY 中性化就是**双重去行业**，
   剩下的残差不足以支撑两年段。⇒ **"DEU 必须用 industry 轴"只对方差/波动类成立，不是全域规律**；
   轴的取舍取决于信号是否携带行业级信息，不能从一条族外推。
2. **W22 是修正信号的半衰期，拉长有害**：W66 把 turnover 压到 0.0255、margin 抬到 61bp，
   但 S −0.18、2Y −0.09、DD +3.2pt。修正信息衰减快，慢化=把信号摊薄。
3. 因此 **j2Ym1PL9 的轴/窗口已在其局部最优**，剩余的 0.01（S）与 0.45（2Y）**不可能靠几何调整补**，
   只能换字段（eps_y1 → eps_y2 / netprofit）或补覆盖（分析师腿 ts_backfill）。

**W1-J 实测（第二轮：字段 / 覆盖修复，2/2 完成）**

| alpha | 相对 j2Ym1PL9 的唯一变化 | S | F | 2Y | subU | turnover | DD | margin | CLUSTER | 闸状态 |
|---|---|---:|---:|---:|---:|---:|---:|---:|---:|---|
| j2Ym1PL9 | 基准 | **1.57** | **1.33** | 1.13 | **0.95** | 0.0333 | 10.1% | 53.8bp | 过(0.67) | S 差 0.01 / 2Y 差 0.45 |
| akKvOGWv（G） | 分析师腿加 `ts_backfill(·,22)`（只修覆盖） | 1.57 | 1.33 | 1.13 | 0.95 | 0.0333 | 10.1% | 53.8bp | 过 | **与基准逐指标完全相同** |
| E56JKxrr（H） | `eps_y1` → `eps_y2`（只换期限） | 1.34 | 1.07 | **1.37** | 0.65 | 0.0335 | 11.4% | 47.7bp | 0.86 WARN | S/2Y 双向拉扯，仍不过 |

归因（三条，两条是可复用负结论）：

1. **覆盖修复是 no-op，覆盖不是这条候选的瓶颈**：给分析师腿加 `ts_backfill(·,22)` 后，
   S / F / 2Y / subU / turnover / DD / margin **七项与基准完全一致** —— 说明该字段在
   `trade_when` 状态下的可交易票池里 22 天内没有缺口，回填无事可做。
   ⇒ 与用户「覆盖率可动态调整」正交：**这条候选的瓶颈是信号强度，不是数据可得性**，
   后续不要再用回填补覆盖去换指标（那是白烧配额）。
2. **`eps_y2` 把 2Y 抬了 +0.24（1.13→1.37），但 S 掉 −0.23、subU 掉 −0.30、CLUSTER 从 0.67 劣化到 0.86**。
   机制：两年期修正比一年期**更慢、更不拥挤**，在 2022–2023 仍有残差信息（2Y 高）；
   但它对横截面当期收益的解释力弱（S 低），且两年期预测的横截面离散度更大，
   子宇宙里小票的修正方向更杂（subU 0.65）。**换期限是"用 S 换 2Y"，不是提升，是平移。**
3. **四个单因子（分组轴 / 窗口 / 覆盖 / 期限）全部试过，无一能补齐 0.01 S + 0.45 2Y** ⇒
   j2Ym1PL9 是本战役的**终态近闸候选**（`checks.fail=[]`、pyramid effective 2、
   self-corr 0.42 过闸），剩余缺口属于「该概念在 DEU 的 IS 上限」，不是几何或覆盖问题。
   eps_y1 / eps_y2 / netprofit_y1 **三个字段在 S 与 2Y 上互补**，但加权混腿被明令禁止 ⇒
   正确做法是把它们作为**三条独立 alpha**（各自单信号）分别评估，而不是合成一条。

**W1-K～W1-T 实测（shortinterest3 单信号纵深：11 波 76 行，同日第二轮）**

W1-G 把方差族压在 S 0.95 并给了「单信号天花板」的判断。这一轮不增产，只回答一个问题：
**在不加腿、不改权重、不跨 category 的前提下，这条族到底还能推多远？**
按「骨架 → 窗口 → 轴 → 口径 → 设置 → 等价算子 → 新信息源」逐层拆解，每波只动一个因子
（波次↔`backtest_results.wave` 对照见本节末「波次索引」）。
除标注外一律 DEU/TOP500/D1、`neutralization=SUBINDUSTRY`、`decay=4`、`truncation=0.08`、字段 `min_loan_rate_main`。

**表 A｜骨架与窗口阶梯（单层 → 嵌套）**

| 形态 | wave | S | F | 2Y | subU | TO | margin | 判读 |
|---|---|---:|---:|---:|---:|---:|---:|---|
| 单层 `ts_covariance(·,10)` | `w15` | 1.10 | 0.87 | 1.90 | 1.02 | 0.149 | 12.5bp | 窗太短，换手高 |
| 单层 `·,12` | `w15` | 1.22 | 1.08 | **1.91** | 1.04 | 0.131 | 15.6bp | 平台下沿 |
| 单层 `·,15` | `gate` | 1.21 | 1.09 | 1.78 | 0.95 | 0.112 | 18.1bp | 平台中 |
| 单层 `·,18` | `w15` | 1.22 | 1.11 | 1.70 | 0.83 | 0.100 | 20.7bp | 平台上沿 |
| 单层 `·,22` | `var22` | 1.12 | 0.98 | 1.68 | 0.81 | 0.088 | 21.8bp | 出平台 |
| 单层 `·,44` | `gate` | 0.92 | 0.72 | 1.21 | 0.58 | 0.058 | 26.6bp | 慢化=摊薄 |
| **嵌套** `ts_mean(ts_covariance(·,3),15)` | `equiv` | 1.27 | 1.18 | 1.78 | 0.96 | 0.097 | 22.3bp | 内窗 3 略弱 |
| **嵌套** `(·,5),10` | `equiv` | 1.28 | 1.19 | **1.98** | 1.01 | 0.113 | 18.9bp | 2Y 最优 |
| **嵌套** `(·,5),15` | `equiv` | **1.26** | **1.17** | 1.76 | 0.92 | 0.089 | **23.9bp** | 综合最优（本表基准） |
| **嵌套** `(·,5),22` | `equiv` | 1.07 | 0.92 | 1.64 | 0.88 | 0.073 | 25.3bp | 外窗过顶 −0.19 |

**归因 A（三条，其中两条推翻/修正了旧结论）**

1. **外层平滑是骨架的必需项，不是可选项**：同窗 5 下，单层 W12 1.22 / W15 1.21 → 嵌套 5/10 1.28、5/15 1.26，
   **+0.05~+0.06**，且 margin 同步抬 3–6bp。机制：`ts_covariance` 的单日读数是「一日内的协方差估计」，
   本身噪声极大（借款人报价逐日跳），外层 `ts_mean` 做的是**估计量平均**而不是价格平滑
   —— 这解释了为什么它对信号是增益、而 `hump`（表 C）对信号是毁灭。
2. **窗口平台 W12–W18，且嵌套把最优位往短端推**：单层在 12–18 之间平（1.21–1.22），22 起掉（1.12）、
   44 掉到 0.92；嵌套后 5/15 最好、5/22 掉 **−0.19**。⇒ 修正 `DEU-LOANRATE-TV-IND-AXIS-20261029`
   里「W22 是机制半衰期」的表述：**W22 只对单层成立；嵌套口径下 W22 已经过顶**，两者最优窗不同。
3. **窗口短端代价全在换手上，不在强度上**：W10（TO 0.149）与 W18（0.100）的 S 只差 0.12，
   但换手差 49%。窄宇宙 + 高换手会把 margin 从 20.7bp 压到 12.5bp。

**表 B｜分组轴与字段口径（同为单层 W15，只换一个因子）**

| 变化 | S | F | 2Y | TO | margin | 判读 |
|---|---:|---:|---:|---:|---:|---|
| `group_zscore(·, densify(industry))` | **1.21** | 1.09 | 1.78 | 0.112 | 18.1bp | 基准 |
| → `densify(sector)`（更粗） | 1.03 | 1.04 | 1.41 | 0.131 | 20.5bp | **−0.18** |
| → `densify(subindustry)`（更细） | 0.79 | 0.51 | 1.50 | 0.102 | 10.4bp | **−0.42** |
| → 无分组 `zscore(·)`（W22） | 0.67 | 0.69 | 0.25 | 0.107 | 24.5bp | **−0.45**，分组是必需项 |
| 口径 `min_loan_rate_main` | 1.21 | 1.09 | 1.78 | 0.112 | 18.1bp | 基准 |
| → `mean_loan_rate_main` | 1.04 | 0.86 | 1.32 | 0.113 | 15.0bp | **−0.17** |
| → `mean_loan_rate_p5_d1` | 1.02 | 0.79 | 1.55 | 0.114 | 13.2bp | **−0.19** |
| → `max_loan_rate_main` | 1.01 | 0.81 | 1.50 | 0.122 | 13.3bp | **−0.20** |

**归因 B**

1. **轴的最佳粒度 = 信号的经济粒度**：DEU 单一交易所 ⇒ exchange 轴退化；industry 恰好是「谁在抢同一批
   抵押券」的自然分组；再粗（sector）会把不同借贷市场的票混在一起（−0.18），再细（subindustry）
   每组样本不足、z 分数不稳（−0.42），去掉分组则把 500 票放进一个池子（−0.45）。
   **这条与 W1-I′ 的分析师修正族结论方向相反**，再次说明轴是信号属性、不是区域常量。
2. **口径必须取稀缺端**：`min`（最便宜的可借报价）> `mean` > `max`。机制：min 报价决定「能不能借到」，
   是约束的边界；max 是一次性异常报价（噪声），mean 把两者混在一起。**口径序与水平式相反**
   （水平式 `main` 优于 `p5_d1`，方差式 `p5_d1` 也弱），所以「覆盖更广的口径更强」不成立。

**表 C｜设置杠杆（三条独立对照，全部配对）**

| 杠杆 | 对照 | ΔS | Δmargin | ΔTO | 判读 |
|---|---|---:|---:|---:|---|
| `neutralization` SUBINDUSTRY→**NONE** | 嵌套5/15 · 5/10 · decay_linear15 · 3/15 | **+0.05 / +0.04 / +0.07 / 0.00** | +2.2 / +1.5 / +2.1 / +1.1 bp | −0.013 / −0.016 / −0.015 / −0.015 | **唯一正向杠杆** |
| `neutralization` SUBINDUSTRY→STATISTICAL | 8 条配对（单层 W22/W5/W66/各口径各轴） | **−0.30（8/8 全负）** | 15.9→~5 bp | 0.09→0.13–0.27 | 强度杀手 |
| `decay` 4→2 | 嵌套5/15（SUBINDUSTRY） | +0.02（1.26→1.28） | −1.1 bp | +0.006 | 微杠杆 |
| `decay` 4→2 | 嵌套5/15（NONE，`O0AvrRQg`→`1YN5X1qJ`） | **+0.01**（1.31→1.32） | **−1.6 bp**（26.1→24.5） | +0.006 | 增益减半且被 margin 吃掉 ⇒ **部分替代** |
| `nanHandling` OFF→ON | 4 条重跑 | **逐位相同** | 相同 | 相同 | no-op，兼作噪声标尺 |
| `zscore(group_zscore(·))` 二次归一 | `3qoWX3qP` vs `1YN5X1qJ` | 0.00（1.32 vs 1.32） | 逐位相同 | 逐位相同 | no-op（group_zscore 已横截面可比） |

**归因 C（这一段是本轮最有复用价值的部分）**

1. **中性化粒度必须与分组轴错开：要么不做，要么更粗；同粒度是 no-op，更细是负迁移。**
   表达式内 `group_zscore(·, densify(industry))` 已做过一次行业去均值，SUBINDUSTRY 中性化是
   **在更细粒度上再去做一次均值**，把「行业内部谁更贵、谁更抖」这层信息一起抹掉 —— 而
   「行业内部分散」正是这条信号的全部内容。因此 **NONE 才是正确取值**，且 S/margin/TO 三项同向改善。
   这条同时解释了 W1-G 的「STATISTICAL 负迁移」和 W1-I′ 的「分析师族 industry 轴有害」：
   它们都是同一件事——**去均值层数过多**。
2. **STATISTICAL 是第二好的反例**：它用统计因子解释收益，而借券费差是**特质信息**，被因子吸收；
   同时残差化把行业/规模暴露推回权重 ⇒ 换手 0.09→0.13–0.27、margin 15.9→5bp。8 条配对全负，
   与 W1-G 的 8/8 结论**独立复现**。
3. **decay 的增益依赖中性化，且与 margin 对冲**：SUBINDUSTRY 下 4→2 是 +0.02（要去掉细粒度噪声），
   NONE 下只剩 +0.01（1.31→1.32）却要付 1.6bp margin（26.1→24.5bp）。⇒ 设置杠杆之间存在**替代关系**，
   不能把单因子增益线性相加；且 NONE 之后 decay 已是「用质量换 0.01」，不值得当独立杠杆使用。
4. **噪声标尺已建立**：同一表达式重跑（nanHandling 开关、二次归一）**逐指标逐位相同**。
   因此后续所有 ≥0.02 的差异都可判为真实效应，不需要重复实验。

**表 D｜等价算子替换全扫（10 条，无一带到 1.58）**

| 替换（相对嵌套 5/15） | S | F | 2Y | TO | margin | 判读 |
|---|---:|---:|---:|---:|---:|---|
| `ts_mean(·,15)` → `ts_decay_linear(·,15)` | **1.29** | **1.21** | 1.84 | 0.104 | 21.0bp | S 最高，但**新增 CONCENTRATED_WEIGHT** |
| → `ts_mean(·,10)` | 1.28 | 1.19 | **1.98** | 0.113 | 18.9bp | 2Y 最优、S 次优 |
| → `ts_mean(·,3)` 内窗 3 | 1.27 | 1.18 | 1.78 | 0.097 | 22.3bp | +0.01，噪声级 |
| → `winsorize(cov, std=4)` | 1.24 | 1.13 | 1.76 | 0.089 | 23.4bp | −0.02，无用 |
| `vec_avg` → `vec_sum` | 1.17 | 1.04 | 1.62 | 0.091 | 21.9bp | **−0.11**，把借款人数量当强度 |
| `group_zscore` → `rank(group_zscore)` | 1.10 | 0.87 | 1.49 | 0.098 | 16.1bp | **−0.18**，秩丢掉行业间水平差 |
| `group_zscore` → `group_rank` | 0.91 | 0.63 | 1.52 | 0.102 | 11.6bp | **−0.37**，同上 |
| `vec_avg` → `vec_max` | 0.85 | 0.62 | 1.42 | 0.094 | 14.2bp | **−0.43**，单点异常报价 |
| `group_zscore` → `group_neutralize` | 0.74 | 0.83 | 0.79 | 0.108 | 28.9bp | **−0.54**，不缩放⇒高波动行业吃满权重，CW FAIL |

**归因 D**

1. **唯一还能加 S 的替换都带副作用**：`ts_decay_linear` +0.03 换来 `CONCENTRATED_WEIGHT`（硬闸），
   `ts_mean(·,10)` 把 2Y 抬到 1.98 但换手 +0.024、margin −4bp。**这两条是本族仅剩的两个「用别的指标换 S」的口子**，
   不是净提升。
2. **`group_zscore` 的尺度保留是本质的**：换成任何秩形式（`group_rank` / 后置 `rank`）都掉 0.18–0.37。
   机制：不同行业的方差**水平**不同（有些行业天然更难借），`zscore` 保留组内量级、`rank` 只保留组内序，
   把「这个行业的整体紧张度」这一维抹掉。
3. **`group_neutralize` 是「只去均值不缩放」**：残差尺度随行业波动率漂移，高波动行业吃满 truncation，
   S 塌到 0.74 且 CW FAIL。⇒ 分组算子里**必须用带缩放的 `group_zscore`**。
4. **向量聚合只能取平均**：`vec_sum` 把「报价条数」当强度（−0.11）、`vec_max` 取单个最极端借款人（−0.43）。
   与 W1-J「ts_backfill 是 no-op」并列，说明**向量层的自由度已经被口径选完，不是剩余杠杆**。

**表 E｜新信息源：横截面离散度（wave `s2_si3_vecdisp_d1`，同为 `neutralization=NONE`、外窗 15）**

| 信息源 | 表达式核心（均 `-group_zscore(·, densify(industry))`） | S | F | 2Y | subU | TO | margin | 闸状态 |
|---|---|---:|---:|---:|---:|---:|---:|---|
| 报价极差 `vec_range` | `ts_mean(vec_range(min_loan_rate_main),15)` `JjeLN31l` | **1.30** | 1.14 | 1.74 | 0.96 | **0.055** | **34.8bp** | **唯一非 PASS = LOW_SHARPE；CLUSTER_TEST 无告警** |
| 报价标准差 `vec_stddev` | 同上换 `vec_stddev` `A1VdNLmQ` | 1.27 | 1.10 | 1.78 | 0.90 | 0.054 | 35.0bp | LOW_SHARPE + CLUSTER_TEST 0.94 |
| 借款人家数 `vec_count` | 同上换 `vec_count` `GrWvbQ9Q` | 0.21 | 0.08 | 0.43 | 0.51 | 0.048 | 0.7bp | 死：广度不是压力 |
| 相对离散（对数） | `ts_std_dev(log(vec_avg(·)),15)` `d5Wwb9v2` | −0.10 | −0.02 | 0.46 | −0.20 | 0.165 | −7.9bp | 死：log 抹掉水平 |
| 相对离散（嵌套） | `ts_mean(ts_std_dev(log(vec_avg(·)),5),15)` `88RqjGX7` | −0.06 | −0.01 | 0.85 | −0.31 | 0.128 | −6.1bp | 死 |

**归因 E**

1. **同一机制可以换矩而不塌，且横截面离散度这一矩的质量显著更好**：同窗 15、同轴、同口径下，
   `vec_range` 给出 TO 0.055（协方差版 0.082 的 −33%）与 margin 34.8bp（26.1bp 的 +33%），
   代价只是 S 1.31→1.30、2Y 1.86→1.74。**它还是本族唯一 CLUSTER_TEST 无告警的形态**
   （协方差族 0.92–0.96 全带 WARNING，`JjeLN31l` 干净）。
2. **为什么两者不是同一个矩**：`ts_covariance(x,x)` 量「同一只票的费率今天比昨天抖多少」= **召回/重定价风险**
   （ERR 2018 的时序不确定性）；`vec_range`/`vec_stddev` 量「同一只票的不同借款人之间报价差多少」
   = **供给摩擦与谈判力分散**。二者都指向「借券成本不可预测 ⇒ 套利受限」，所以同向，但经济来源不同。
3. **必须取水平、不能取相对**：`ts_std_dev(log(vec_avg))`（−0.10）与嵌套版（−0.06）双死 ——
   与表 B「口径取稀缺端」同源：费率信号的强度在**绝对水平差**里（1bp 与 20bp 的差别本身就是信息），
   除以均值后大小票 / 松紧期被拉平，水平信息被消掉。`vec_count`（0.21）则是纯广度指标：
   报价家数多 ≠ 紧张，只有「家数少且价差大」才是挤压。
4. **合并口径（协方差 + 离散度）被 `add` 禁令封死**，故这条支线的定位是**备选载体**而非主力：
   要提 S 仍走「分析师修正门控」那条路，而离散度版是**质量更优的门控件 / 替换件**
   （margin 34.8bp ⇒ 门控后净收益更高）。

**终态与缺口（本战役 shortinterest3 单信号定论）**

| 口径 | 表达式（均 `neutralization=NONE`） | S | F | 2Y | TO | margin | 闸状态 |
|---|---|---:|---:|---:|---:|---:|---|
| S 最优（decay 4） | `-group_zscore(ts_decay_linear(ts_covariance(vec_avg(min_loan_rate_main), vec_avg(min_loan_rate_main), 5), 15), densify(industry))` `gJezQX6K` | **1.36** | 1.23 | 2.00 | 0.089 | 23.1bp | LOW_SHARPE + **CONCENTRATED_WEIGHT**（CLUSTER_TEST 0.96 亦非 PASS） |
| **无 CW 最优（decay 2）** | `-group_zscore(ts_mean(ts_covariance(vec_avg(min_loan_rate_main), vec_avg(min_loan_rate_main), 5), 15), densify(industry))` `1YN5X1qJ` | **1.32** | 1.18 | 1.86 | 0.082 | 24.5bp | **强度类唯一 FAIL = LOW_SHARPE（差 16%）；CLUSTER_TEST 0.92 亦非 PASS** |
| 2Y 最优（decay 4） | 同上，外窗换 10 `RRELV9Mj` | 1.32 | 1.18 | **2.05** | 0.097 | 20.4bp | 唯一 FAIL = LOW_SHARPE（CLUSTER_TEST 0.96 亦非 PASS） |
| **质量最优（离散度，decay 4）** | `-group_zscore(ts_mean(vec_range(min_loan_rate_main), 15), densify(industry))` `JjeLN31l` | 1.30 | 1.14 | 1.74 | **0.055** | **34.8bp** | **唯一非 PASS = LOW_SHARPE；CLUSTER_TEST 干净、无 CW** |

（无 CW 口径的 decay4 孪生体 `O0AvrRQg`：S 1.31 / F 1.17 / 2Y 1.86 / TO 0.076 / margin **26.1bp**，
唯一非 PASS 同为 LOW_SHARPE + CLUSTER_TEST 0.94 —— 若要在协方差族里按「质量」留存，取它而不是 `1YN5X1qJ`；
两者的差别只是 decay 4 vs 2。全表质量上界仍是 `JjeLN31l`：margin 高 33%、换手低 33%、且是唯一不带
CLUSTER 告警的形态，代价是 S 低 0.02、2Y 低 0.12。）

结论：**这条族的 DEU 单信号上限 ≈ 1.30–1.36，闸线 1.58，缺口 14–18%，且已无未试的合规杠杆**
（骨架 / 窗口 / 轴 / 口径 / 中性化 / decay / nanHandling / 覆盖回填 / 9 种等价算子 / 3 个新信息源全部实测）。
注意上限是**两个并列读数**：协方差（时序方差）最高的 1.36 带 CW，离散度（横截面）的 1.30 质量最好而 S 略低；
单信号约束下二者都不可相加。
与仓库铁律 `multileg_strength_not_decomposable_v1` 一致 —— DEU 历史上所有 best_S>1.58 的波次都是多腿或
增强形态，纯单信号波从未过线；而用户约束禁止任何形式的两两混腿与加权。
⇒ **要过闸只有一条合规路：单主信号（借券费水平式 S 0.82）+ 分析师修正族风险门**
（已验证 S 1.57、margin ×8.8、DD 10.1%），且门控腿必须是**另一个 category**。
SHORTINTEREST 塔在「只做本数据集单信号」的约束下**不可点亮**，这是概念上限，不是执行缺口。

**波次索引（本节 11 波 ↔ `backtest_results.wave`）**

| wave | 行 | 测什么 | 结论落点 |
|---|---:|---|---|
| `s2_si3_var22_d1` | 12 | 单层窗口 5/10/12/15/18/22/44 × 两轴 × decay_linear | 表 A 单层段（窗口平台 12–18） |
| `s2_si3_var22_stat_d1` | 10 | 同族 STATISTICAL 中性化（第一轮） | 表 C 第 2 行（8/8 负） |
| `s2_si3_gate_d1` | 5 | 闸门批次：单层 15/44 与对照 | 表 A |
| `s2_si3_w15_d1` | 10 | 单层 W15 换分组轴 / 换口径 | 表 B |
| `s2_si3_nan_d1` | 4 | `nanHandling` ON/OFF 重跑 | 表 C（no-op ⇒ 噪声标尺 = 0） |
| `s2_si3_stat2_d1` | 7 | STATISTICAL 第二轮（各口径/各轴） | 表 C |
| `s2_si3_decay2_d1` | 3 | `decay` 4→2（SUBINDUSTRY） | 表 C |
| `s2_si3_equiv_d1` | 10 | 等价算子替换全扫（嵌套 5/15 基准） | 表 D / 归因 A |
| `s2_si3_neutnone_d1` | 5 | 中性化 SUBINDUSTRY→NONE（含 sector、内窗 3 对照） | 表 C 第 1 行；终态三口径 |
| `s2_si3_none_d2_d1` | 5 | NONE × decay 2（含 `zscore` 二次归一、`ts_std_dev` 对照） | 表 C；`1YN5X1qJ` |
| `s2_si3_vecdisp_d1` | 5 | 新信息源：`vec_range` / `vec_stddev` / `vec_count` / 对数形态 | 表 E |
| **合计** | **76** | | |

## 7. 交付清单与经验沉淀（S6）

### 7.1 20 颗 regular alpha 全景（全部 DEU/TOP500/D1；#2/#9 为覆盖合规替换位，出自 wave `s4_risk60_covstd_d1`，其余出自 `s2_unlit_tower_20261029`）

| # | alpha | 数据集 | 机制 | S | F | 2Y | subU | TO | DD | 判读 |
|---|---|---|---|---:|---:|---:|---:|---:|---:|---|
| 1 | N1N95XaX | insiders | `rank(ts_mean(directional_indicator,22))` | -0.23 | -0.06 | -0.83 | -0.07 | 0.310 | 27.7% | 死 |
| 2 | leAZ9GPA | risk60 | `reverse(group_zscore(ts_std_dev(vec_avg(lending_fee_bid_rate),22), industry))` | 0.49 | 0.27 | **1.69** | 0.50 | 0.082 | 22.6% | 2Y 最高（合规替换位） |
| 3 | JjeK5YPO | shortinterest3 | 费率水平 `ts_backfill·252` | 0.82 | 0.45 | **1.65** | 0.85 | 0.194 | 13.7% | **2Y 最强载体** |
| 4 | 78L9K0o2 | risk60 | `lending_fee_bid_rate` 水平 252 | 0.83 | 0.60 | 1.15 | 0.30 | 0.067 | 17.1% | subU 不足 |
| 5 | 1YNEnwXQ | insiders | 内部人净买入/持仓（66d） | 0.13 | 0.04 | 0.30 | 0.02 | 0.075 | 21.9% | 死 |
| 6 | KPJaw7NN | insiders | 内部人买入股数（66d） | 0.34 | 0.15 | 0.49 | 0.62 | 0.073 | 21.8% | 死 |
| 7 | A1VKOpMw | shortinterest3 | 费率 `ts_rank·250`（自身历史） | 0.67 | 0.26 | 0.30 | 0.81 | 0.326 | 12.2% | 归一化毁 2Y |
| 8 | rKRXrqv9 | shortinterest3 | 费率 `ts_zscore·250` | 0.74 | 0.32 | 0.24 | 1.00 | 0.294 | 11.1% | 同上 |
| 9 | WjOm0z2G | risk60 | `reverse(group_zscore(ts_covariance(vec_avg(lending_fee_bid_rate),vec_avg(lending_fee_bid_rate),22), industry))` | 0.34 | 0.16 | 1.63 | 0.45 | 0.091 | 24.4% | cov 对照腿（合规替换位） |
| 10 | 88R1aAwz | sentiment7 | Wikipedia 浏览量水平 | -0.07 | -0.01 | -0.61 | 0.44 | 0.098 | 22.0% | 代理不复现 |
| 11 | 78L9aY2O | shortinterest3 | 费率方差 @ exchange | 0.67 | 0.69 | 0.25 | 0.35 | 0.108 | 58.2% | CW/DD 挂 |
| 12 | 3qoLa02O | shortinterest3 | 费率标准差 @ exchange | 0.88 | 0.81 | 0.64 | 0.59 | 0.086 | 40.8% | CW 挂 |
| 13 | wpQg5xZp | shortinterest3 | 费率方差 @ **industry** | 0.95 | 0.75 | 1.10 | 0.62 | 0.089 | **20.6%** | 轴修好即过 CW |
| 14 | akKvNZbv | shortinterest3 | 方差 @ exchange W66 | 0.81 | 0.89 | 0.37 | 0.51 | 0.055 | 54.6% | 窗口错 |
| 15 | 1YNEopE6 | shortinterest3 | `p5_d1` 水平 22 | 0.68 | 0.31 | 1.26 | 0.50 | 0.222 | 11.7% | 覆盖广≠更强 |
| 16 | 9qx09por | shortinterest3 | `main` 水平 22 | 0.76 | 0.39 | 1.25 | 0.74 | 0.216 | 13.8% | 水平式短窗 |
| 17 | gJepxE2m | shortinterest3 | 标准差 @ industry | **0.98** | 0.76 | 1.30 | 0.54 | 0.084 | 20.1% | 单信号 S 最高 |
| 18 | wpQgLMr2 | shortinterest3 | 方差 `p5_d1` @ industry | 0.93 | 0.69 | 1.30 | 0.63 | 0.088 | 17.8% | 口径不敏感 |
| 19 | **j2Ym1PL9** | shorti+analyst93 | 借券门 + eps_y1 修正 | **1.57** | **1.33** | 1.13 | **0.95** | 0.033 | **10.1%** | **唯一近闸** |
| 20 | RREWdlXe | shorti+analyst93 | 借券门 + netprofit_y1 | 1.52 | 1.27 | **1.25** | 0.83 | 0.034 | 11.8% | 2Y 版备选 |

另 4 条探针（不计入 20 颗）：d5WLQmE2 / E56JKbg0（W1-I′）、akKvOGWv / E56JKxrr（W1-J）。

**覆盖合规替换（2026-10-29 收口后修正，详见 §7.11）**：原 #2 `qMLqmKxv`（sentiment27，`-rank(ts_delta(snl27_relpopularity1,5))`）
与原 #9 `npvVZ0jl`（sentiment27，关注度水平 −rank）**已从 20 颗中剔除**——sentiment27 只有 2019–2023 有持仓
（2014–2018 `pnl=0 / longCount=0`），不满足第 4 条「近十年都要有数据」。补位的是 risk60
`lending_fee_bid_rate` 的 cov / std 对照对（`s4_risk60_covstd_d1`，multisim `1kz6Zabph4Jpalp116cUjIJg`）：
该字段 2014–2023 逐年都有持仓（longCount 52→249），合规；两条都以 LOW_SHARPE / LOW_FITNESS 挂，
属该族「2Y 强、S 弱」的既定形态（与 #3/#4 同源），因此**替换是合规性动作，不是新增信号**。
台账：`backtest_results` 2 行 + `expressions` 2 条（`atom_flag=atom`、已挂 alpha_id）+ `wave_results`
`s4_risk60_covstd_d1`（verdict FAIL / n_pass 0 / n_near 0）。

**ATOM 口径**：#1–#18 全部为单数据集 alpha（18/20 = 90% ATOM），#19/#20 为「单主信号 + 风险门」的双数据集组合。
替换后 ATOM 计数不变（#2/#9 与补位件都是单数据集，`list_expressions` 实测 `atom_n_datasets=1`）。
**规则 5**：本战役未使用 PV / MODEL / OTHER 任何字段，故 0 条受限组合、5 条配额一个未占；
唯一组合腿是 SHORTINTEREST + ANALYST（不在受限类别之间），且是 trade_when 门控而非加权混腿。

### 7.2 经验沉淀（本会话可直接复用的 7 条）

1. **借券费 alpha 的信息在横截面水平里，不在自身历史偏离里**。`ts_rank`/`ts_zscore` 把 2Y 从 1.65 打到
   0.24–0.30、turnover 反升；水平式 + `ts_backfill·252` 是唯一 2Y 稳定形态（1.65）。机制是「谁难借、谁被看空」的
   结构性分层，不是择时。
   ⚠ **2026-10-29 补注（逐年实测，勿按旧口径引用）**：「2Y 1.65」是**近两年现象**，不是十年稳定边缘。
   方差/协方差式（`WjOm0z2G`）逐年 S 为 0.17/−0.33/0.36/0.23/1.02/**−0.04/−0.63/−1.01**/1.56/1.71
   —— 2019–2021 连续三年负，强度全部落在 2022–2023；水平式（`78L9K0o2` S 0.83）之所以全期仍为正，
   是因为 2014–2018 有弱正贡献。引用该族时须同时给出「全期 S」与「2Y」两个数，不能只讲 2Y。
2. **分组轴是可迁移性变量，不是区域常量**。`exchange` 在 DEU（单一 XETRA）退化 ⇒ 方差族 CW/DD 爆；
   换 `industry` 后 CW 转安、DD 58%→20.6%、2Y 0.25→1.10。**但同一条轴对分析师修正族反向有害**
   （双重去行业，2Y −0.13）。轴要按信号是否携带行业级信息选。
3. **窄宇宙里 `ts_std_dev` ≥ `ts_covariance`**（S 0.98 vs 0.95、DD 20.1% vs 20.6%），与 ASI（2000+ 票）相反：
   universe 越窄，方差把尾部权重推满后越容易多空失衡。同一模板的可迁移性取决于宇宙宽度。
4. **nanHandling=ON 是"召回跳变"的代价交易**：margin 6.1bp→24.5bp，但 DD 13.7%→40–58%。
   薄市场（TOP500）无成交日填 0 会制造假跳变，除非机制本身就需要事件采样，否则保持 OFF。
5. **单信号的 IS 上限是硬的**：借券水平 S0.82（2Y 1.65）、方差-industry S0.95（2Y 1.10）、std-industry S0.98，
   单信号都过不了 LOW_SHARPE 1.58。**过闸必须靠第二条腿，但合规形态只有「单主信号 + 风险门」**：
   `trade_when(借券费 rank<0.7, 分析师修正 rank, -1)` 把 S 0.82→1.57、TO −83%、margin ×8.8、DD 10.1%，
   无任何加权混合。
6. **覆盖修复与几何微调都补不了近闸缺口**：给分析师腿加 `ts_backfill` 是 no-op（七项指标完全相同），
   `industry`/W66 各自退化，`eps_y1→eps_y2` 只是 S↔2Y 平移。缺口属于概念上限，不是数据或算子问题。
7. **字段口径要看机制**：方差族需要宽度（覆盖广的 `p5_d1` 更好或持平），水平族需要纯度（`main` 优于 `p5_d1`：
   S 0.76 vs 0.68、subU 0.74 vs 0.50）。同名「借券费率」的两种口径不可互换。

### 7.3 塔位进展与判死

| 塔 | 战役前 | 战役后 | 证据 |
|---|---|---|---|
| SHORTINTEREST (×1.3) | 未点亮 | **未点亮（单信号上限已测定：S 1.36 / 2Y 2.05，闸 1.58，缺口 14–17%）** | W1-B/B′/D/E/F/G/K–T |
| INSIDERS (×1.7) | 未点亮 | **判死（单信号上限 0.75 / 2Y 1.06；4 条探针 S ≤ 0.34）** | W1-A/A′ |
| SENTIMENT (×1.8) | 未点亮 | **判死**（关注度方向：两个独立代理 + 变化率版三连否） | W1-C |
| NEWS (×1.8) | 未点亮 | **判死（本季度）**：news104 / news17 两集 3 波 14 颗，最佳 S 0.74（subU 0.30），全部镜像对称 | W2-A/B/C |
| RISK (×1.5) | 未点亮 | 备选（2Y 1.15 但 subU 0.30） | W1-B |
| ANALYST (×1.8) | 已点亮 | 组合贡献有效（门控后 S 1.57） | W1-H/I′/J |

**§7.3 三条口径更正（2026-10-29 复核）**：

1. **INSIDERS「判死」只对单信号成立，且上限不是 0.34**：`field_profile_deu` 里
   `insider_agg_matrix.directional_indicator`（cov 1.0，62 次测试）的单信号最佳是 **S 0.75 / 2Y 1.06**，
   组合面最佳 S 1.86 / 2Y 2.07。**但那个组合是 5 腿 `add(add(add(...)))`**（历史 ACTIVE 件 `Vk65zLzG`
   S 1.79 / 2Y 2.07，2026-09-13 提交），正是现行 `add-a-b` 禁令禁止的形态 ⇒ 该路径不可复用。
   所以结论从「INSIDERS 没信号」更正为：**单信号天花板 0.75（距 1.58 差 53%），唯一的过闸历史配方是禁用形态**。
2. **塔位「未点亮」是按本季度计**（`get_pyramid_alphas` 默认当季）：DEU/D1 当季 = institutions 1 /
   model 1 / other 2 / analyst 1 / fundamental 1，insiders 0。insiders 上一季度（Q3）由 `Vk65zLzG` 点过，
   所以「未点亮」不等于「从未点亮」，报告全文按**当季**口径读。
3. **NEWS 的判死是机制级而非参数级**：14 颗里每条都与其反号腿**逐位对称**（如 `E56AVqkR` +0.22 vs
   `9qxQE9Jr` −0.22；`O0AvAEJY` +0.74 vs `A1VdVMvQ` −0.74），说明符号翻转不改变信息量 ⇒
   方向层在这个宇宙上没有净信息。R1（`ts_corr/ts_covariance` + **FAST** 中性化，论坛 93 票配方）
   在 news17 上实测 S 0.41 / 2Y −0.32，属配方不成立的负结果。

**结论**：本战役产出 20 颗 regular alpha（18 ATOM）+ 4 条归因探针，达成挖掘目标；
但**未新增点亮塔**——SHORTINTEREST 的单信号上限与 SENTIMENT/INSIDERS 的机制缺失是客观结论，不是执行缺口。

### 7.4 台账与复核状态

- 波次台账：`wave_results` 已结案（region DEU / wave `s2_unlit_tower_20261029` / verdict **PARTIAL** /
  n_pass 0 / n_near 2，逐条 key_findings 与 full_payload 已落库）；`backtest_results` 24 行（18 交付 + 4 条 analyst93 探针 + 2 条 sentiment27 归因对照）；
  `expressions` 同步落库（含 G/H 两条 round-2）。
  本会话累计落在 DEU 的回测行 **203 行 / 22 个波次**（2026-10-28 起，2026-10-29 收口后只读实测），分布：
  `s2_unlit_tower_b_20261029` **39**（第二批交付，§7.14）、`s2_shortinterest3_d1` 28、`s2_unlit_tower_20261029` 24（20 + 4 探针）、
  shortinterest3 其余设置族 8 波 77 行、`s4_j2yml_tune_d1` 8、`s4_shorti_lvl_flip_20261029` **8**（§7.15）、
  news 三波 14、`s4_inst1_selflock_probe_d1` 3、`s4_risk60_covstd_d1` 2（覆盖合规替换位）、`mcp-20261029` 1。
- **未新增 dead_end registry 条目（有意）**：INSIDERS / SENTIMENT 的判死结论只写在本文档 §7.3。
  `seal_dead_end` 的论坛取证闸是 fail-closed（需 `forum_recon_negative_<question_key>` 台账证据），
  本战役未对这两个问题产出可靠 `no_result` 取证记录，走 `force_seal` 会绕过 §8.11 纪律。
  要固化为机器可消费的死路，需先跑 `tools/forum_recon.py` 留下 `no_result` 证据再 seal。
- registry（DEU / shortinterest3 层，3 条，均为 win）：
  `DEU-SI3-LEVEL-2Y-CARRIER-20261029`（水平式是真信息载体）、
  `DEU-LOANRATE-TV-IND-AXIS-20261029`（方差模板可迁移但轴必须 industry；其中「W22 是机制半衰期」
  已被下面的上限条目修正为「只对单层成立」）、
  `DEU-SI3-NESTED-VAR-CEILING-20261029`（嵌套骨架 + 等价算子全扫的几何上限，SUBINDUSTRY 口径 S 1.29）、
  `DEU-LOANRATE-SETTINGS-MAP-20261029`（设置杠杆地图 + NONE 口径终态 S 1.32–1.36；含中性化粒度法则）。
- registry（`campaign` 层，2 条，数据集级判死/产能结论）：`news104`（6 探针全灭 + 镜像对称）、
  `news17`（6 探针 + R1 FAST 负结果，8 条，best S 0.41）；两条均 `status=exhausted`。
- registry（`win` 层，本会话新增 1 条）：`DEU-J2YML-MODEA-CEILING-20261029`（§7.5 的四轴因子试验 + IS 上限
  S1.57/2Y1.13 + NONE 承重结构的例外条件 + `9qWX75Nr` 存在性证据）。
- ⚠ **收批→expressions 关联 bug 已修，但服务未重启**：`src/wqb/store/_backtest.py` 的
  `upsert_backtest_rows` 此前只写 `backtest_results`、不回填 `expressions.alpha_id`，导致 81045–81052 等行
  长期停在 `alpha_id=NULL / status=pending`。修法已落地（按 `expr_id` 回填 alpha_id/status/sharpe 等，
  回归 `tests/unit/01_store_db/test_expression_link_on_harvest.py` 4 例全绿），但**运行中的 `wqb-db` MCP
  仍是旧代码**，需重启服务才会对新收批次生效；存量未关联行不受影响（幂等回填，重启后重收即修）。
- 相关性复核（MCP 实测，2026-10-29 02:14）：`j2Ym1PL9` **self-corr 0.4213 / prod-corr 0.5971，双闸均过**
  （prod 直方图 [0.5,0.6) 仅 36 条、峰值在 [0.1,0.2) 5297 条 ⇒ 与生产池高度正交）。
  已落库 `alphas.prod_correlation=0.5971 / self_correlation=0.4213`（`persist_correlation`，source=manual）。
  ⚠ 这条纠正了战役早期的默认预期（未过 IS 的 alpha 也能出 prod 值）：平台的 prod 计算**不要求 IS 全过**，
  因此「相关性墙」不是这条候选的障碍，**唯一障碍是 S 差 0.01 与 2Y 差 0.45**。
  这也意味着它是一颗现成的**可作为 SuperAlpha 组件 / 未来放开闸门时立即提交**的候选（提交仍需用户确认）。
- **提交状态：0 提交**。`j2Ym1PL9` / `RREWdlXe` 为 `checks.fail=[]`（无硬 FAIL）但两条 RA warning，
  不满足提交条件；任何提交都需要用户明确确认后单独调用（本会话未获确认）。

### 7.5 近闸候选定向挖掘：Mode A 四轴因子试验（wave `s4_j2yml_tune_d1`，8 颗）

设计 = `trade_when(rank(ts_backfill(vec_avg(mean_loan_rate_main),252)) < 门限,
winsorize(rank(ts_mean(eps_y1_estimate_change_3mo, W)), std=4), -1)`，**一次只动一个轴**，
其中 `winsorize(·, std=4)` 是恒等包装（rank 值域 [0,1]，|z|≤1.73 < 4），用来规避 multisim 按表达式去重。

| alpha | 偏离基线 | S | F | 2Y | subU | TO | margin | DD | CLUSTER_TEST |
|---|---|---:|---:|---:|---:|---:|---:|---:|---|
| wpQV3LM1 | **ctrl**（decay4 / w22 / 门 0.7 / SUBINDUSTRY） | 1.57 | 1.33 | 1.13 | 0.95 | 0.0333 | 53.8bp | 10.05% | PASS |
| omEeRVM6 | w66 | 1.39 | 1.10 | 1.04 | 0.77 | 0.0255 | 61.0bp | 13.28% | 0.77 warn |
| vR1VZOZv | w126 | 1.36 | 1.07 | 0.93 | 0.81 | 0.0207 | 74.3bp | 11.38% | 0.73 warn |
| rKRm9d99 | 门限 0.5 | 1.29 | 1.00 | 1.17 | 0.82 | 0.0327 | 46.0bp | 9.62% | 0.75 warn |
| VkxomvpA | decay 6 | 1.57 | 1.33 | 1.13 | 0.95 | 0.0323 | 55.4bp | 10.40% | **0.99 warn** |
| 0mYWNbEv | decay 6 + w66 | 1.38 | 1.09 | 1.04 | 0.75 | 0.0249 | 62.1bp | 13.28% | 0.76 warn |
| pwdgMERv | **NONE** + w22 | 0.96 | 1.46 | **0.06** | 0.91 | 0.0128 | 450bp | **55.4%** | PASS |
| O0AvMk8Y | **NONE** + w66 | 0.95 | 1.43 | **0.03** | 0.84 | 0.0102 | 556bp | **56.0%** | PASS |

**四个轴的结论（全部为负）**：

1. **ctrl 的恒等性已被证明**：`wpQV3LM1` 与 `j2Ym1PL9` 的 S/F/2Y/subU 逐位相同（1.57 / 1.33 / 1.13 / 0.95），
   只 TO 0.0333、DD 10.05%、margin 53.8bp 有微小漂移 ⇒ `winsorize(rank(x), std=4|5)` 确为恒等包装，
   「同一表达式配不同设置」可以靠它在一个 multisim 里共存（这是本次能一次跑 2 颗同设置的前提）。
2. **窗口单调退化**：w22 → w66 → w126 的 2Y 是 1.13 → 1.04 → 0.93（−8% / −18%），S 同步掉 11–13%。
   短窗（22）是唯一局部最优，与 §7.2 第 1 条「水平式 + 短窗」一致。
3. **门限收紧只是 S↔2Y 的横向平移**：0.7→0.5 让 S 1.57→1.29（−18%）、2Y 1.13→1.17（+4%）、
   `risk_neutralized_sharpe` 0.25→0.12。要补 2Y 的 0.45 缺口，靠这条曲线得把门限压到极窄、同时把 S 打穿。
4. **decay 6 是「目标指标 no-op + 一个闸变差」**：S/F/2Y/subU 与 ctrl 完全相同，但
   **CLUSTER_TEST 从 PASS 推到 0.99（limit 1.0，警戒）、DD 10.05%→10.40%** ⇒ decay 4 严格优于 decay 6。
5. **中性化是这条设计的承重结构，不是可调杠杆**：NONE 下 S 0.96/0.95、2Y 0.06/**0.03**、
   DD 55%/56%、**long 325 / short 0**——`trade_when` 内 `rank` 值域 ≥0，没有中性化就没有空头腿，
   book 变成全多腿裸露。⚠ 这与 `DEU-LOANRATE-SETTINGS-MAP-20261029` 的「NONE 更好」**不矛盾**：
   那条结论成立于「表达式内已带 `group_zscore(industry)`」的方差族；判据是**表达式内是否已有分组轴**，
   不可跨设计照搬。

**结论**：四个轴的全部偏离要么退化要么横向平移，无一改善 2Y ⇒ 该双数据集设计的
**IS 上限就是 S 1.57 / 2Y 1.13**，闸缺口（S 差 0.01、2Y 差 0.45）属概念上限，不是参数没调够。
本波 8 颗全部 FAIL 硬闸、6 颗过 near 线（S≥1.0），已结案 `verdict=FAIL / status=closed`。

### 7.6 两条旁证：DEU 的 2Y 闸确实可过，但通行证既有禁令、又撞 prod 墙

- **存在性证据**：2026-10-07 从平台同步进来的旧战役 DEU alpha `9qWX75Nr`，平台实测
  **`failed_ra_count=0`**（S 1.58 / F 1.38 / 2Y **1.76** / subU 0.79 / TO 0.1108 / DD 5.02% / margin 17.19bp，
  `checks.pass` 含 LOW_SHARPE、LOW_FITNESS、LOW_2Y_SHARPE、LOW_SUB_UNIVERSE_SHARPE、CLUSTER_TEST、CONCENTRATED_WEIGHT）。表达式：
  `group_neutralize(rank(add(ts_mean(ts_backfill(eps_y1_estimate_change_3mo,1008),5), ts_mean(ts_backfill(eps_y1_estimate_change_3mo,1008),220))), bucket(rank(ts_mean(ts_backfill(eps_y1_estimate_change_3mo,1008),252)), range="0,1,0.06"))`。
- **但这条路走不通，两条独立的理由**：
  1. **形态违规**：`add(ts_mean(x,5), ts_mean(x,220))` 是同一字段的快慢加权相加，正是 `add-a-b` 禁令所指的
     「同信号加权调参」⇒ 不可作为新挖掘模板；
  2. **prod 墙**：MCP 实测 `prod_correlation = **0.9187**`（阈值 0.7，直方图 [0.9,1.0] 恰有 1 条）
     ⇒ 即便忽略形态问题，这个族在生产池里**已经有高度同源的 alpha**，必须判死。
- **对结论的含义**：DEU/TOP500 的分析师修正字段确实能在 2Y 上做到 1.7–1.8，但代价是把同一字段的
  fast/slow 两版相加；纯单表达式形态（`group_rank(x, sector)`）的天花板是 **S 1.81 / 2Y 1.12**
  （W253 波 `E5RNA3GK` 等），与本次 gated 设计的 1.57/1.13 同一个数量级。
  即：**过 2Y 闸的能力存在于字段，但合规形态取不到它，能取到它的形态已被生产池占用**。
  这也从反面解释了为什么 `j2Ym1PL9` 的 prod 反而低（0.5971）——借券门把它推离了生产池的那条主向量。
- ⚠ **本节结论的适用范围（2026-10-29 晚补）**：「2Y 只能靠违规形态拿到」**只对分析师修正字段族成立**。
  §7.9 实测 institutions1 持仓流用纯单表达式就能做到 2Y 2.52–2.79（无 `add(fast,slow)`），
  说明 2Y 闸在 DEU 并非普遍不可达；那边的堵点是 self-lock 而非 2Y。不要拿本节去否定「DEU 普遍过不了 2Y」以外的读法。

### 7.7 口径漂移清单（只登记不修改，供后续治理）

| 位置 | 现状 | 风险 |
|---|---|---|
| `tracking/DEU/config/thresholds.json` | `two_year_sharpe_min: 1.0`、`sub_universe_sharpe_min: 1.0`、`margin_min: 0.0005` | 平台线是 2Y **1.58**、subU **≈0.48×S**（随 S 浮动）；本地阈值偏松，用它做本地判定会放过实际不过闸的候选 |
| `tracking/DEU` ledger | `stop_rules_override` **INVALID**、`backlog_gate_override` **EXPIRED（2026-10-07）** | 旧键已失效；再开波需按 `tools/waiver.py` 写 `waiver_<gate>_<region>_<wave>` |
| `campaign_intel s0-select` | 输出「0/16 lit」 | 与 `get_pyramid_alphas` 当季实测（6 类已点亮）不一致，塔位判读以平台实测为准 |
| CLUSTER_TEST | 0.73–0.99 都作为 **warning** 下发，limit 1.0 | 本地多处把它当硬闸/FAIL 读；实际只有 >1 才是 FAIL，0.99 仍算 PASS |
| 提交队列缓存 | 备注含 `corr_未实测@2026-10-17`、`corr_age_hours 381.5` | 陈旧相关性备注会被误读成「已实测」；相关性一律以 `check_correlation` 当次实测为准 |

### 7.8 DEU 的 prod 墙真身：自家 11 颗 ACTIVE 构成的**自我锁定**（2026-10-29 实测）

**起因**：收盘台账里 DEU 有 4 行 `submit_ready`（`gate=IS_ONLY`），其中 `LLZ87QY9` 的缓存 prod 是
0.6947（实测于 2026-10-09），看似可提交。当次 `check_correlation(refresh=True)` 复测把它推翻。

| 复核项 | 缓存值 | 当次实测 | 差值来源 |
|---|---|---|---|
| `LLZ87QY9` prod | 0.6947 @2026-10-09 | **0.9144**（[0.9,1] 恰 1 条） | 账户在 2026-10-09 之后又提交了新 alpha |
| `LLZ87QY9` self | 未记录 | **0.91441**，`top_correlated[0] = 2rmGAPqN` | 见下 |
| `WjLEOqLP` prod | 0.651 @2026-10-13 | **1.0000**（精确 1.0） | 该表达式**已经被自己提交**（见下） |

**根因：`prod` 的最大值就是自家 alpha。** `check_correlation(correlation_type="self")` 直接点名：

```
self.max_correlation = 0.9144103…   top_correlated[0] = 2rmGAPqN   pool_size = 10   full_os_pool_size = 11
```

`2rmGAPqN`（`DEU_R_insconviction_01`，2026-10-09 提交，ACTIVE）与 `LLZ87QY9` 是同一条 institutions1 持仓流：
只有两处不同 —— `ts_sum(...,220)` vs `66`，群轴 `pca_fact2_cluster_20` vs `pca_fact1_cluster_20`。
同理 `WjLEOqLP` 的 prod 恰好 1.0，是因为 `2rjrMZ25`（2026-10-13 提交，ACTIVE）与它**逐字相同**：

```
group_neutralize(group_rank(add(ts_mean(ts_backfill(eps_y1_estimate_change_3mo, 1008), 1),
ts_mean(ts_backfill(eps_y1_estimate_change_3mo, 1008), 210)), sector),
bucket(rank(ts_mean(ts_backfill(eps_y1_estimate_change_3mo, 1008), 252)), range="0,1,0.05"))
```

**账户在 DEU 的 OS 持仓 = 11 颗 ACTIVE**（`get_user_alphas(stage=OS, status=ACTIVE)`，本会话核对 10 颗）：
`mLYLEm99`（STATISTICAL 10 分量组合）/ `2rjrMZ25`（分析师修正快慢加+bucket）/ `Wje5K71x`（fnd6 OIADP 双窗口）/
`2rmGAPqN`（institutions1 持仓流）/ `58gkLAkk`（starmine 四轴嵌套中性化）/ `JjxrYjre`、`2rOe10qY`、`vRk6og8b`、
`Vk65zLzG`、`blRnKEk6`（四条多腿 add 组合，starmine / loan-rate / insiders 交叉）。
覆盖面 = **analyst / fundamental / institutions / starmine / shortinterest / insiders / super** 七个方向。

**结论（本区最新判断，优先于「外部拥挤」的旧解释）**：

1. `get_mining_yield(DEU)` 的 `prod_wall_ratio = 0.8197`（50 blocked / 61 已测）**主因是自锁，不是外部拥挤**；
   DEU 的 prod 直方图几乎全落在 [-0.1, 0.2]，唯一那条 [0.9,1] 就是自家 alpha。
2. 因此 **DEU 的 `prod_correlation` 实际上等价于一次 `self_correlation` 检查**。新候选的 prod 只要 >0.9，
   先查 `check_correlation(correlation_type="self")` 的 `top_correlated`，能直接点名是哪一颗自家 alpha。
3. 「去掉自锁后的外部相关」也可以读出来：`LLZ87QY9` 的第二高才到 [0.6,0.7] 段（n=2）
   ⇒ 外部拥挤度 ~0.69，**仍然贴着 0.7 的墙**。所以即使自锁解除，这条也过不去。
4. 新增挖掘的**设计前置**从「避开平台拥挤」改为「**避开自家 11 条主向量**」，且必须在设计阶段就做，
   不能等回测完再测相关（一次 check 只能筛掉一批，且 48h 缓存会骗人）。
5. 反向印证 §7.6：`j2Ym1PL9` prod 0.5971 / self 0.4213 之所以低，是因为「借券率门控 + 分析师修正」
   这个组合在自家 11 条里没有同形；它是**唯一**还留着相关性余量的近闸候选。

### 7.9 群轴替换探针：3 颗，2 颗 IS 全过，self 相关纹丝不动（wave `s4_inst1_selflock_probe_d1`）

**设计**：`LLZ87QY9` 唯一可动的合规轴是中性化群（`oth455` 的 N2V 聚类 GROUP 字段，非信号腿，不触犯组腿禁令）。
3 条探针只换群轴，其余冻结（66 日持仓流 + 置信度门 + tail/winsorize + FAST 中性化）。
并发 2 约束下以 `create_multi_simulation` 一次发 3 条（`1pqQKcdLb5ccaIEfCS42dCq`），全 COMPLETE 零 ERROR。

| 探针 | 群轴 | S | F | 2Y | subU | TO | DD | IS 闸 | self 最高相关 |
|---|---|---|---|---|---|---|---|---|---|
| 基线 `LLZ87QY9` | `w1_pca_fact1_cluster_20` | 1.67 | 1.30 | 2.52 | 1.07 | 0.1334 | 5.55% | 全过 | **0.9144**（`2rmGAPqN`） |
| P1 `j2YQGrpQ` | `w1_kmeans_cluster_20` | 1.57 | 1.20 | 2.65 | 1.10 | 0.1303 | 5.12% | **FAIL** LOW_SHARPE 差 0.01 | 未测（IS 已挂） |
| P2 `E56AzejK` | `w5_pca_fact1_cluster_20` | 1.71 | 1.36 | 2.79 | 1.17 | 0.1328 | 5.95% | **全过** | **0.9184**（`2rmGAPqN`） |
| P3 `d5WwzRMY` | `w1_pca_fact1_cluster_5` | 1.73 | 1.40 | 2.64 | 1.20 | 0.1285 | 5.42% | **全过** | **0.9287**（`2rmGAPqN`） |

**结论**：

1. **群轴替换对相关性零作用**：0.9144 → 0.9184 / 0.9287（反而略升），三条 `top_correlated[0]`
   全部指向自家 `2rmGAPqN`。⇒ institutions1 持仓流在 DEU 是**单一经济向量**，换怎么分组都是同一条暴露。
2. **本族 IS 极强、且完全合规**：2Y 2.52–2.79（限 1.58）、subU 1.07–1.20、S 1.67–1.73（限 1.58），
   全程没有 `add(fast, slow)`。**这条推翻「DEU 的 2Y 只能靠违规形态拿到」的读法**
   （§7.6 的结论只对**分析师修正字段**成立；institutions1 持仓流用单表达式就轻松过 2Y）。
   它现在的唯一堵点是相关性，且堵它的是**自家持仓**而不是外部拥挤。
3. 因此 `LLZ87QY9` 与 3 条探针全部**不可提交**，institutions 方向在 DEU 就地判死
   （不是形态问题、不是参数问题、不是拥挤问题，是**账户已占用**）。
4. 台账已记：wave `s4_inst1_selflock_probe_d1`（`verdict=FAIL`，3 颗，2 颗 IS 全过但 self-locked）+
   registry `DEU-SELFLOCK-OS11-20261029`（layer=win，`payload.dataset=institutions1`）。

### 7.10 战役收口：DEU 为什么到此为止（第四次独立确认）

**交付盘点**：20 颗 REGULAR alpha（18 ATOM）+ 4 条归因探针（`s2_unlit_tower_20261029`）
+ 11 颗定向件（Mode A 8 颗 `s4_j2yml_tune_d1`、self-lock 3 颗 `s4_inst1_selflock_probe_d1`）。
挖掘目标达成，但**可提交数 = 0**。

**三条堵点，本次全部为实测、互不重叠**：

| 方向 | 最好成绩 | 堵在哪 | 能不能靠调参解决 |
|---|---|---|---|
| 分析师修正族（`j2Ym1PL9` / `RREWdlXe` / `9qWX75Nr` 族） | S 1.57 / 2Y 1.13 / subU 0.95 / corr 双闸过 | **2Y 差 0.45**（合规单表达式上限 1.12–1.13） | 否：窗口/门限/decay/中性化四轴全扫，无一改善 2Y（§7.5）；能到 1.7–1.8 的两种形态已被禁令与自家持仓各封一条 |
| institutions1 持仓流（`LLZ87QY9` 族） | S 1.67–1.73 / 2Y 2.52–2.79 **IS 全过** | **self-lock 0.914–0.929**（点名自家 `2rmGAPqN`） | 否：群轴替换零作用（§7.9），是账户占用不是形态问题 |
| shortinterest3 单信号 | S 0.82–0.98 / 2Y 1.65（费率水平） | **S 差 0.6**（单信号上限） | 否：需第二腿，而合规第二腿的两种形态已分别撞 2Y 墙与 self-lock |

**与既有 registry 结论一致**：`DEU-TARGET10-STRUCTURAL-CEILING-20260923` 已记「DEU D1 合规空间
（无加权混信号 + ladder 1.58 + corr<0.7 + prod<0.7）上限 = 6，三次独立确认」；本次是**第四次**，
并补上了当年没有的机制解释（prod 墙 = 自锁）。当时的 `unlock_conditions` 里「prod 池占坑 alpha 退役」
一条今天仍然成立且更紧了：OS 持仓已从 6 颗涨到 11 颗。

**唯二还带相关性余量的资产（都不是今天新挖的，但今天的实测没有把它们否掉）**：

- `blbYGJPq` = `rank(vec_avg(mdl109_oeps_sur))`：S 1.13 / 2Y 1.11 / **prod 0.6323 / self 0.202 双闸全过**
  （`DEU-FRONTIER-M109-OEPSSUR-20260915`）。缺口 S+0.45 / 2Y+0.47，但它**相关性完全干净**，
  是 DEU 唯一还没被自锁污染的近闸白空间。
- `j2Ym1PL9`（self 0.4213 / prod 0.5971）：IS 只差 S 0.01，但 2Y 差 0.45 ⇒ 不可提交；
  保留价值在「可作为 SuperAlpha 组件」与「闸门口径变化时立即可提」。

**明确的负结论**：`YPbjnrnw`（`DEU-MIXRESID-S158-FIRST-20260916`，S 1.58 PASS / 2Y 1.45 / subU 1.42 /
risk_neut 1.28，仅差 CW + 2Y 0.13）是**唯一**在数值上接近全闸的历史件，但形态是 `0.6×快腿 + 0.4×残差腿`
的加权混腿，**`add-a-b` 禁令下不可复用**——不要因为它「只差 0.13」就把它当模板。

**下一步（需用户拍板，本战役不自动执行）**：
① 继续 DEU 白空间只有一条：以 `blbYGJPq` 的 model109 surprise 为主信号做 **MODEL×ANALYST 门控**
（规则 5 允许的非受限类组合，占 5 条配额之一；形态必须是 `trade_when` 单主信号 + 门，不得加权）；
② 或按既有 unlock 条件等待（prod 池退役 / 新数据集供给）；
③ 或转区——本机存量 `submit_ready`：KOR 72 / GLB 38 / ASI 4 / USA 1。

**「没有遗漏」的分母盘点**（`search_alphas_by_sharpe(region=DEU, min_sharpe=1.55, limit=10)`，
2026-10-29 收口时一次拉全）：全库 S≥1.55 的 DEU alpha 只有 10 条，逐条归属——

| 归属 | 条数 | 明细 |
|---|---:|---|
| 已 ACTIVE（自家 OS 持仓） | 2 | `mLYLEm99`（SUPER 2.27 / prod 0.611）、`883Y3bAW`（REGULAR 2.17 / prod 0.543） |
| 已 DEAD（`add` 加权混腿 + prod 0.77–0.94） | 7 | `2rOW3j6b`/`rK5VZdGj`/`j23xxK8o`/`RRVKKwAj`/`MP1ZZN3L`/`mLg11W6W`/`E5vLLPV0`，`dead_reason` 均写「族 prod 0.77–0.94 / 抢救失败」 |
| 并行会话在途（非本战役） | 1 | `QPvdMW8Q`（`combo_a(alpha)` 占位名，S 2.30 / 2Y 2.37 / DD 2.28% / **prod 0.8849**，2026-10-29 08:44 建） |

⇒ **没有任何一条「全闸可能通过但被漏掉」的候选**：高 S 的 DEU 件要么已提交、要么是禁令形态、
要么同样撞 prod 墙。这条盘点同时解释了 `DEU-TARGET10-STRUCTURAL-CEILING` 为什么三次确认都是同一个数。

**提交状态：0 提交。** 任何提交（含 `j2Ym1PL9`）都需要用户明确确认后单独调用，本会话未获确认。

### 7.11 数据集「近十年有数据」审计（用户第 4 条硬约束，2026-10-29 补做）

收口复核发现：`field_profile_deu` 的 `cov` 只说明**当前**覆盖率，不说明**时间跨度**。用
`get_alpha_yearly_stats`（平台 MCP，逐年代理）实测各数据集真正有持仓的年份，结果两个数据集不合规：

| 数据集 | 代表 alpha | 有持仓年份 | 年限 | 判定 |
|---|---|---|---:|---|
| insiders | `N1N95XaX` | 2014–2023 连续（longCount 18→62） | 10 | 合规 |
| shortinterest3 + analyst93 | `j2Ym1PL9` | 2014–2023 连续（年 S 2.94/2.75/1.41/1.59/1.99/1.78/−0.46/2.03/1.70/0.43） | 10 | 合规 |
| risk60（`lending_fee_bid_rate`） | `78L9K0o2` | 2014–2023 连续 | 10 | 合规 |
| sentiment7（`snt7_views`） | `88R1aAwz` | 2014–2023 连续 | 10 | 合规 |
| **institutions1** | `LLZ87QY9` | **2018–2023**；2014–2017 `pnl=0 / longCount=0` | **6** | ✗ 不合规 |
| **sentiment27**（`snl27_relpopularity1`） | `npvVZ0jl` | **2019–2023**；2014–2018 全零 | **5** | ✗ 不合规 |

**三条处置**：

1. **#2 `qMLqmKxv` / #9 `npvVZ0jl` 出自 sentiment27 ⇒ 不满足第 4 条，已从 20 颗交付中剔除**，
   用 risk60（十年全覆盖、未点亮塔、单数据集不触犯组腿禁令）补 2 颗：
   wave `s4_risk60_covstd_d1` 的 `ts_covariance` vs `ts_std_dev` 对照对
   （沿用 shortinterest3 上验证过的方差模板 + `industry` 轴，见 §7.2 第 2/3 条）。
   **✅ 已执行（2026-10-29）**：multisim `1kz6Zabph4Jpalp116cUjIJg` → `WjOm0z2G`（cov，S 0.34 / 2Y 1.63 /
   DD 24.4%）与 `leAZ9GPA`（std，S 0.49 / 2Y 1.69 / DD 22.6%），两条 2Y 与 subU 全过、卡 LOW_SHARPE /
   LOW_FITNESS。对照结论：**std 全面优于 cov**（与 shortinterest3 的 0.98 vs 0.95 同向），
   是 §7.2 第 3 条「窄宇宙 std ≥ cov」的第二次独立复现。覆盖面复核：risk60 十年逐年都有持仓
   （`WjOm0z2G` 的 longCount 52→249、shortCount 34→95，无零持仓年）⇒ 合规。
2. **§7.9 的 institutions1 结论按两层读**：`2Y 2.52–2.79` 仍然成立（2Y 窗口 = 2022–2023，落在其
   6 年区间内），self-lock 0.914–0.929 也仍然成立；但**该数据集本身不满足十年覆盖**，
   所以它在 DEU 是**双重出局**——既被账户占用，又不该作为挖掘输入。这不削弱 §7.8 的
   「prod ≡ self」机制结论，后者的证据来自 `WjLEOqLP`（analyst 族，十年全覆盖）。
3. **不可横比的口径**：`LLZ87QY9` 的 S 1.67 是**含 4 个零持仓年**算出来的，与十年全覆盖候选的
   S 不可直接比较；`field_profile_deu` 后续应补一列「有数据起止年」，否则 `cov` 会继续掩盖这类缺口。

### 7.12 五条硬约束逐条对账（收口自检，2026-10-29）

| # | 用户要求 | 证据 | 结论 |
|---|---|---|---|
| 1 | 未点亮塔跑 campaign 流水线挖 20 颗 regular alpha，尽量 ATOM；category 下字段做足画像 | §7.1 二十颗明细（18 单数据集 = 90%）；§2 十六行 category 画像 + 时间跨度表；§7.4 台账 156 行 / 20 波 | ✅ |
| 2 | 近闸候选按 `wq-brain-ra-deu` SOP 定向挖掘；模板查论坛 + 外部论文并验证；回测必做归因与对比 | §4 / **§4.1 模板台账：11 类独立机制（保守口径 10 类，≥10 达标；12 行含 1 条归一化对照）** 论文/论坛取证（JFE 2005 借券供给、JAE supply shortage、Pearson 空头成本、ERR 2018 借券风险、D'Avolio 2002、Jeng 2003、论坛 93 票 R1、18 票分歧度模板）；§7.5 Mode A 四轴 8 颗含**恒等控制组** `wpQV3LM1`（逐字等于基线 `j2Ym1PL9`）；§7.9 群轴替换 3 颗；§7.11 cov vs std 对照 2 颗；§7.2 第 1 条逐年归因（2022–2023 集中） | ✅ |
| 3 | 开波并发 = 2 用 `create_multi_simulation`；尽量走 MCP；prod 必须 MCP 工具 | 本会话全部 multisim 均为 2 表达式一批（`1kz6Zabph4Jpalp116cUjIJg` 等）；台账全部经 `mcp__wqb_db__*` 写、台账读经 `get_wave_result`；相关性一律 `check_correlation` / `check_self_correlation`；本段唯一临时脚本是**只读**计数（已删） | ✅ |
| 4 | 覆盖率可动态调整，但近十年都要有数据 | §7.11 六年/五年两个数据集被揪出并处置：sentiment27 两颗剔除、institutions1 双重出局；补位 risk60 十年连续（`WjOm0z2G` longCount 52→249） | ✅（**本条曾是缺口，已修**） |
| 5 | 禁 PV/MODEL/OTHER 内部两两组腿、禁彼此两两组腿；与其它 category 组腿全战役 ≤5 | 156 回测行**全量只读扫描**（`2026-10-29` 复核）：仅 `bl63xzW6` / `9qxQGMaq` 两颗用到 PV 字段 `returns`，且是**同一表达式 `rank(ts_corr(vec_avg(nws17_multiple_comp_nip), returns, 22))` 的正反镜像** ⇒ 受限组合 1 条 / 2 颗，配额 **2/5**（此前写「0/5」是漏扫，已更正）；无 PV+PV / PV+MODEL / MODEL+MODEL / OTHER+OTHER；主体形态 `trade_when(借券门, 分析师主信号, -1)` 属 SHORTINTEREST × ANALYST（不计数），非加权混腿 | ✅ |

**未做且需要用户单独授权的一件事**：**0 提交**。`submit_verdict` 只作否决、不作放行；
`workflow_submit_alpha(confirm_submit=True)` 与任何不可逆提交都必须由用户在步 8 明确确认后单独调用。

### 7.13 数据集级分母对账：category 下到底挖完了没有（2026-10-29 复核）

**口径**：分母 = `field_profile_perf WHERE region='DEU'` 的**全部 178 个数据集 / 22,494 字段 / 16 个 category**
（这是本区唯一可枚举的完整面；平台 `get_datasets` 单次响应会被截断，不能当分母）。
分子 = `backtest_results` 的 dataset 归属（**不认 `field_profile_perf.n_tests`**——那一列是画像构建器的自记账，
`news104/news17/news50/sentiment*` 有真实回测却仍是 0，用它判「挖没挖」会误判）。
「已回测」= 本战役（2026-10-28 起）或前序 DEU 战役留下过回测行。

**A. 未点亮塔（战役目标面，11 个 category / 51 个数据集）**

| category | 数据集 | cov>0 | 已回测 | 结构性排除 | **未挖** | 未挖的是谁 |
|---|---:|---:|---:|---:|---:|---|
| SHORTINTEREST | 1 | 1 | **1** | 0 | 0 | — |
| INSIDERS | 2 | 2 | **2** | 0 | 0 | —（`insider_agg_matrix` 走 #1/#6；`insiders1` 走 #5 `insd1_valueeur`） |
| RISK | 5 | 2 | **1** | 1 | 0 | `risk88`=单字段市值元数据，判死登记已覆盖；risk68/71/72 cov=0 |
| SENTIMENT | 3 | 3 | **2** | 0 | 1 | **`sentiment33`**（255 字段全 VECTOR，cov 0.315–0.326） |
| NEWS | 17 | 6 | **4** | 1 | 1 | **`news38`**（3 字段 VECTOR，cov 0.599）；结构性排除的是 `news50`（8 探针判死） |
| SOCIALMEDIA | 2 | 1 | 0 | 0 | 1 | **`socialmedia39`**（1 字段 VECTOR，cov 0.275） |
| EARNINGS / MACRO / OPTION / IMBALANCE | 2/1/1/1 | 0 | 0 | 5（cov=0，不计入 15） | 0 | 全部 cov=0（`UNKNOWN_COVERAGE`），不是没挖，是取不到数 |
| **小计** | **51** | **15** | **10** | **2** | **3** | 10+2+3 = 15 ✅ |

**结论 1（数据集层）**：15 个有覆盖的集里 10 个已回测、1 个（`news50`）有 8 探针判死结论但回测行没落库、
1 个（`risk88`）是市值元数据、**3 个从未测过**（`sentiment33` / `news38` / `socialmedia39`，全是低覆盖 VECTOR）。
⇒ **不能说「category 下数据集都挖完了」**；准确说法是「**高覆盖集（cov≥0.6）已全部覆盖，剩下 3 个低覆盖 VECTOR 集未测**」。

**结论 2（字段层，这才是真相）**：即使「已挖」的集，字段也没穷尽。按表达式里实际出现的字段去重（本战役 156 行反查
`field_profile_perf` 的 field→dataset 映射）：`shortinterest3` **9/25**、`insider_agg_matrix` **2/34**、
`insiders1` **2/8**、`risk60` **1/5**、`sentiment27` **1/18**、`sentiment7` **1/3**、`news104` **4/11**、`news17` **4/48**。
「挖完一个数据集」在本战役里的实际含义是**信号机制挖完**（12 个设置波 + 5 形态族），不是字段穷举。

**B. 已点亮塔（不在本战役目标内，6 个 category / 127 个数据集）**

| category | 数据集 | 已回测 | 未回测 | 未回测里 cov>0 且可测的最大块 |
|---|---:|---:|---:|---|
| MODEL | 49 | 10 | 39 | `multifactor_return_pred` 648 / `model109` 544（cov 0.26–0.54）；`model26` 390 字段 cov 0.60–1.00 标 UNTESTED |
| OTHER | 42 | 8 | 34 | `other455` 300 字段 cov 0.72–0.84 标 UNTESTED（另 1200 字段 AXIS_ONLY） |
| ANALYST | 18 | 7 | 11 | `analyst83` 345 字段全 VECTOR cov 0.33 |
| FUNDAMENTAL | 13 | 2 | 11 | `fundamental31` 48 / `fundamental45` 12（cov 0.24–0.40） |
| INSTITUTIONS | 5 | 3 | 2 | `institutions4` 6 字段全 VECTOR cov 0.341 |
| PV | 16 | 2 | 14 | **`pv29` 50 字段（画像口径；平台 fieldCount 40）cov 1.0 标 UNTESTED**、`pv30` 285 字段（GROUP-only，已判死）、`pv109` 26 字段 VECTOR |
| **小计** | **127** | **32** | **95** | — |

**结论 3**：已点亮塔是**最大的未挖面（95/127 集未回测）**，但按塔位策略它们不作为主数据集；
其中唯一**高覆盖且从未测过**的是 `pv29`（画像 50 字段 / 平台 40 字段，cov 1.0）。若要动它，只能走第 5 条配额（PV/MODEL/OTHER
与其它 category 组腿，全战役 ≤5，本战役已用 **2/5**：`bl63xzW6` / `9qxQGMaq` 是同一表达式
`rank(ts_corr(vec_avg(nws17_multiple_comp_nip), returns, 22))` 的正反镜像，用 PV 字段 `returns`；余量 3）。

**C. 对账时发现的三处台账瑕疵（只登记，未改库）**

1. **`risk60_dead` 是过期判死**：2026-09-19 记为 `7 探针 best|S|=0.29`，但本战役 `risk60` 产出 3/20 颗
   （S 0.34/0.49/0.83，2Y 1.63/1.65/1.69）。该键与交付结论直接冲突，应升 supersede 记录，不能留作有效判死。
2. **`news50_dead` 的 8 探针在 `backtest_results` 里没有对应行**：判死证据只活在 ledger payload 里
   （`max|S|=0.6` + TO/CW 双墙），无法按行复算。
3. **11 行 dataset 归属非规范**（本战役 156 行里）：5 行 `_null` + 6 行写成类别名（`insiders`×2 /`shortinterest`×2 /
   `sentiment`×2）。其中 **10 行可从表达式字段反推唯一数据集**（`JjeK5YPO`→shortinterest3、`78L9K0o2`→risk60、
   `N1N95XaX`/`1YNEnwXQ`→insiders1、`KPJaw7NN`→insider_agg_matrix、`qMLqmKxv`/`npvVZ0jl`→sentiment27、
   `88R1aAwz`→sentiment7、`A1VKOpMw`/`rKRXrqv9`→shortinterest3），1 行是 `combo_a` 无单数据集。
   任何按 dataset 聚合的审计都会被这些行少算（如 shortinterest3 显示 120 行而非 122、risk60 2 而非 3）；
   修法需一次显式归属修订（属写库动作，本轮未执行）。

**D. MCP 复核（2026-10-29，本节 A/B 的数字全部经 MCP 复算，结论未变）**

- **分子面** `mcp__wqb_db__get_mining_yield(region='DEU', by_dataset=True)`：总量
  **4,625 表达式 / 2,865 消耗 / 3,764 回测行 / 510 passed / 213 ra_clean / 9 prod_clean / 52 prod_blocked /
  627 ra_unknown**，conversion 0.6195、strict yield 5.66%、宽松口径 13.55%。按 dataset 共 **61 个键**：
  **52 个有回测行，9 个只有表达式、零回测行**。
- **新发现（A/B 表没覆盖的一块）**：这 9 个键合计 **544 条已生成从未发批**的表达式 ——
  `news81` 188 / `pv30` 165 / `other128` 48 / `other546` 48 / `workforce_flow_skills` 48 /
  `insider_matrix` 18 / `other47` 17 / `mix_2leg` 6 / `mix_2leg_resid` 6。
  它们多数**不是单个数据集**（`mix_2leg*` 是组合族标签、`workforce_flow_skills` 属 cov=0 的取不到数集），
  但 `news81` 188 与 `pv30` 165 是真实字段块：前者从未跑过，后者已判死（GROUP-only）。
  ⇒ 「挖完」的缺口不只在 178 集分母内，还在「生成端到发批端」这一段。
- **判死面** `get_dead_datasets('DEU')` = **19 个**，与 A/B 表的结构性排除一致；`risk60` 在列但属**按用途判死**
  （该键 24 回测行 / 11 ra_clean，见 C.1），不能据此认为 risk60 不可用。
- **平台面** `get_datasets(DEU, delay=1, universe=TOP500)` **不分类单次调用只给 92 集（截断）**；
  **按 16 个 category 逐类调用合计 172 集**，且平台覆盖率与画像逐个吻合（明细见 §2.1）。
  平台面仍**不是权威分母**：它比画像少 6 个集（`fundamental31` / `model193` / `model219` / `model230` /
  `multi_horizon_alpha` / `ml_factor_proj`），其中 `fundamental31` 是真实可测缺口（cov 0.40）。
  故分母仍用 `field_profile_perf`，平台清单只作交叉验证。
- ⚠ **工具缺口（本轮实测，修复属写库动作未执行）**：`mcp__wqb_db__query_dataset_profile` /
  `query_field_profile` 对 DEU **恒返回 0 行** —— 它们读 `dataset_profile` / `field_profile_full`，
  而这两张表只装了 USA(294) / KOR(203) / EUR(178) / IND(144) / GLB(143)；
  DEU 的 22,494 字段 / 178 集只在 `field_profile_perf`（VIEW `field_profile_deu`）里。
  ⇒ 本区 dataset / field 画像类审计**只能用 `get_field_catalog` + `field_profile_perf`**；
  分子核对用 `get_mining_yield`。要恢复 MCP 路径，需把 DEU 画像刷进那两张表。
- **字段级抽查**：`get_field_catalog('DEU','shortinterest3')` 返回 25 个 VECTOR 字段，
  `shrt3_bar` cov 0.6528（173 用户 / 323 alpha）、`mean_loan_rate_main` 0.6872、
  `loan_rate_volatility_p5_d1` 0.7833 —— 与 §2 画像逐项一致。

**一句话回答「category 下的数据集都挖完了吗」**：**没有**。未点亮塔 15 个有覆盖的集里 10 个已回测、
2 个结构性排除、**3 个从未测过**（`sentiment33` / `news38` / `socialmedia39`，全是低覆盖 VECTOR）；
已点亮塔侧 95/127 集未回测但按塔位策略不作主数据集；
另有 **544 条生成未发批**的表达式积压。高覆盖（cov≥0.6）的集已**全部**覆盖，这是已完成的部分。

---

### 7.14 第二批 39 颗 regular alpha 全景（wave `s2_unlit_tower_b_20261029`）

**设计**：逐个 category 第二轮——每个族取字段画像里覆盖最高 / 机制先验最强的一块，统一
`rank(ts_backfill(F, 252))` **水平式**（与首批的方差 / 变化率形态互补），每条只碰一个数据集。
设置 = DEU/TOP500/D1、decay 4、SUBINDUSTRY、truncation 0.08、nanHandling OFF（§2 面板）。
回测 = `create_multi_simulation`（账户并发上限 2）→ `batch_status` → `harvest_multisim_alphas` →
`harvest_multisim_results`（全 MCP，无手写请求）。IS 窗口平台回读 **2014-01-01–2023-12-31**（满十年，用户第 4 条）。

**闸门**：0/39 过硬闸、0 条过 near 线 1.0，最高 S 0.97 ⇒ wave verdict = **FAIL**（§8.6：评审结论可覆盖）。
`wave_results` 已落 9 条归因 findings + `full_payload.attribution`。

| # | alpha | 数据集 | 机制（表达式） | S | F | 2Y | subU | TO | DD | 判读 |
|---|---|---|---|---:|---:|---:|---:|---:|---:|---|
| 1 | `9qxQNek9` | shortinterest3 | `reverse(rank(ts_backfill(vec_avg(max_loan_rate),252)))` | 0.97 | 0.58 | 1.42 | **1.15** | 0.201 | 11.7% | **全波最佳**（唯一 subU>1 且 2Y>1.4） |
| 2 | `1YN5rxRQ` | risk60 | `-rank(ts_backfill(vec_avg(rsk60_last),252))` | 0.96 | 0.74 | 1.41 | 0.44 | 0.113 | 15.1% | 风险族最强，subU 薄 |
| 3 | `JjeL6AWl` | insiders | `rank(ts_backfill(directional_indicator,252))` | 0.93 | 0.62 | 0.69 | 0.20 | 0.079 | 12.5% | 内部人最强，2Y/subU 双薄 |
| 4 | `j2YQqpGo` | shortinterest3 | `reverse(group_zscore(ts_backfill(vec_avg(max_loan_rate_main),252),industry))` | 0.92 | 0.63 | 1.47 | 1.12 | 0.150 | 13.9% | #39 的逐位镜像正腿 |
| 5 | `ZYQLOx60` | shortinterest3 | `-rank(ts_backfill(vec_avg(max_loan_rate_main),252))` | 0.87 | 0.57 | 1.38 | 1.00 | 0.145 | 15.0% | 与 B5 `npv016jE` 同式（重复位） |
| 6 | `qMLZQWwj` | risk60 | `-rank(ts_backfill(vec_avg(rsk60_offer),252))` | 0.81 | 0.58 | 1.14 | 0.29 | 0.065 | 17.2% | offer 腿弱于 last 腿 |
| 7 | `ZYQLO8MZ` | shortinterest3 | `reverse(rank(ts_backfill(vec_stddev(max_loan_rate_main),252)))` | 0.78 | 0.50 | 1.21 | 0.61 | 0.132 | 12.4% | 方差族可用但非最优 |
| 8 | `vR1VWkXQ` | socialmedia39 | `rank(ts_mean(vec_count(scl39_top5_people_also_watch_ticker_ii),22))` | 0.70 | 0.60 | 0.13 | −0.63 | 0.039 | 15.7% | 关注度代理失效（subU 负） |
| 9 | `d5WwNZrE` | news17 | `group_zscore(ts_mean(vec_avg(nws17_multiple_comp_event_sentiment_score),22),industry)` | 0.68 | 0.33 | −0.15 | 0.31 | 0.160 | 12.2% | news 全波最高，仍远低于线 |
| 10 | `JjeL6A1O` | shortinterest3 | `-rank(ts_backfill(vec_avg(average_loan_duration_days_main),252))` | 0.49 | 0.21 | −0.14 | 0.66 | 0.153 | 17.9% | 借期无方向 |
| 11 | `2rAk3gx8` | news104 | `rank(ts_mean(vec_avg(nws104_prob_pos),66))` | 0.43 | 0.19 | 0.08 | 0.00 | 0.060 | 13.8% | 正概率水平 |
| 12 | `rKRmZ5Mm` | story_analytics | `rank(ts_mean(vec_avg(story_analytics_metric_value),22))` | 0.33 | 0.14 | 1.12 | 0.20 | 0.102 | 31.4% | 2Y 有、DD 高 |
| 13 | `ZYQLOEv1` | news104 | `rank(ts_mean(vec_avg(nws104_prob_pos) - vec_avg(nws104_prob_neg),22))` | 0.31 | 0.10 | 0.30 | 0.15 | 0.149 | 15.9% | 正负差无增量 |
| 14 | `akK35L8w` | story_analytics | `rank(ts_mean(vec_avg(story_analytics_relevance_score),22))` | 0.30 | 0.12 | −0.55 | 0.23 | 0.113 | 30.6% | 相关性打分无方向 |
| 15 | `A1Vdop5w` | risk60 | `rank(ts_backfill(vec_avg(rsk60_offer) / vec_avg(rsk60_last),252))` | 0.22 | 0.04 | 0.74 | 0.24 | 0.362 | 14.8% | 比值腿全灭 |
| 16 | `npvbLNGz` | news17 | `rank(ts_mean(vec_avg(nws17_multiple_comp_bee),66))` | 0.09 | 0.02 | −0.47 | 0.21 | 0.063 | 9.3% | — |
| 17 | `E56A9GnR` | news17 | `rank(ts_mean(vec_avg(nws17_multiple_comp_ber),66))` | 0.07 | 0.01 | −0.57 | 0.28 | 0.065 | 16.0% | — |
| 18 | `O0Avlka1` | shortinterest3 | `-rank(ts_delta(ts_backfill(vec_avg(max_loan_rate_p5_d1),252),22))` | 0.03 | 0.00 | −0.01 | −0.15 | 0.367 | 18.7% | 变化率式（复验 §7.2-1） |
| 19 | `RRELGmOe` | news104 | `-rank(ts_mean(vec_avg(nws104_prob_neg),22))` | 0.03 | 0.00 | −0.01 | 0.51 | 0.116 | 27.0% | — |
| 20 | `e75JX3Mp` | news104 | `rank(ts_mean(vec_avg(nws104_marketimpactscore),22))` | 0.02 | 0.00 | 0.15 | 0.10 | 0.128 | 19.3% | — |
| 21 | `qMLZQdrA` | shortinterest3 | `-rank(ts_backfill(vec_avg(loaned_share_count_main),252))` | 0.01 | 0.00 | 0.03 | 0.37 | 0.058 | 27.6% | 借出数量无信号（main 口径） |
| 22 | `58EVPm2J` | news17 | `rank(ts_zscore(vec_avg(nws17_multiple_comp_ssc),66))` | −0.01 | 0.00 | 0.80 | −0.06 | **1.196** | 43.7% | TO 1.20 破表 |
| 23 | `N1NoYbGE` | news17 | `rank(ts_mean(vec_avg(nws17_multiple_comp_ssc),22))` | −0.05 | −0.01 | −0.33 | −0.43 | 0.132 | 17.2% | — |
| 24 | `pwdg9N2o` | news17 | `rank(ts_mean(vec_avg(nws17_event_similarity_days),22))` | −0.05 | −0.01 | 0.21 | 0.25 | 0.183 | 22.0% | — |
| 25 | `1YN5rLbK` | shortinterest3 | `-rank(ts_backfill(vec_avg(max_loan_rate_main) / vec_avg(mean_loan_rate_main),252))` | −0.08 | −0.01 | −0.01 | −0.07 | 0.264 | 45.0% | max/mean 比值无信息 |
| 26 | `Xg9EdWxb` | sentiment7 | `rank(ts_std_dev(vec_avg(snt7_views),66))` | −0.08 | −0.02 | 0.23 | −0.46 | 0.028 | 22.3% | 关注度波动 |
| 27 | `P0oEkZbw` | sentiment7 | `rank(ts_mean(vec_avg(snt7_all_languages_views),22))` | −0.11 | −0.03 | 0.48 | −0.38 | 0.026 | 26.5% | 关注度水平 |
| 28 | `xAraJQ6l` | shortinterest3 | `rank(ts_backfill(vec_avg(transaction_count_main),252))` | −0.15 | −0.05 | −0.31 | −0.67 | 0.082 | 31.2% | 笔数无信号 |
| 29 | `gJezn8Nl` | news104 | `rank(ts_mean(vec_avg(nws104_relevance),22))` | −0.20 | −0.07 | −0.53 | 0.24 | 0.097 | 31.5% | — |
| 30 | `JjeL6xJO` | story_analytics | `rank(ts_std_dev(vec_avg(story_analytics_metric_value),66))` | −0.20 | −0.07 | −0.95 | −0.46 | 0.055 | 32.3% | — |
| 31 | `58EVP9W6` | shortinterest3 | `rank(ts_backfill(vec_avg(min_loan_rate_p5_d1),252))` | −0.23 | −0.07 | −0.35 | 0.06 | 0.216 | 37.9% | 未反转的 min 腿（负） |
| 32 | `vR1VW9qz` | shortinterest3 | `rank(ts_backfill(vec_avg(min_loan_rate_main),252))` | −0.26 | −0.08 | −0.31 | −0.04 | 0.210 | 45.1% | 同上（main 口径） |
| 33 | `1YN5rx2R` | risk60 | `-rank(ts_backfill(vec_avg(rsk60_offer) - vec_avg(rsk60_last),252))` | −0.33 | −0.08 | −1.02 | −0.38 | 0.376 | 26.9% | 报价价差反向 |
| 34 | `e75JX9WJ` | risk60 | `rank(ts_backfill(vec_avg(rsk60_crowding),252))` | −0.46 | −0.11 | −0.64 | −0.69 | 0.735 | 40.6% | 拥挤度（TO 贴顶） |
| 35 | `0mYW1d3q` | shortinterest3 | `rank(ts_backfill(vec_avg(average_loan_duration_days_main),252))` | −0.49 | −0.21 | 0.14 | −0.66 | 0.153 | 49.1% | 借期正向腿 |
| 36 | `d5WwNZrK` | news17 | `rank(ts_delta(ts_mean(vec_avg(nws17_multiple_comp_nip),5),5))` | −0.52 | −0.11 | 0.01 | −0.51 | 0.612 | 47.6% | 新闻变化率式 |
| 37 | `0mYW1d0q` | shortinterest3 | `rank(ts_backfill(vec_stddev(max_loan_rate_main),252))` | −0.78 | −0.50 | −1.21 | −0.61 | 0.132 | 60.6% | #7 的未反转腿 |
| 38 | `A1VdopmX` | shortinterest3 | `rank(ts_backfill(vec_avg(max_loan_rate_main) - vec_avg(min_loan_rate_main),252))` | −0.84 | −0.57 | −1.12 | −0.81 | 0.137 | 67.9% | 价差未反转腿 |
| 39 | `78LVeQE1` | shortinterest3 | `group_zscore(ts_backfill(vec_avg(max_loan_rate_main),252),industry)` | −0.92 | −0.63 | −1.47 | −1.12 | 0.150 | 76.0% | #4 的逐位镜像负腿 |

**族分布**（按表达式字段反推，非 DB 的 `dataset` 列——该列被 harvest 统一写成 wave 级标签 `mix_unlit_tower_b`）：
shortinterest3 **15**、news17 **7**、news104 **5**、risk60 **5**、story_analytics **3**、sentiment7 **2**、socialmedia39 **1**、insiders **1**。
⚠ 台账瑕疵：该 39 行的 `dataset` 归属需按字段名修订（属写库动作，本轮只登记，同 §7.13-C.3 口径）。

### 7.15 近闸定向挖掘：借券费率水平符号翻转网格（wave `s4_shorti_lvl_flip_20261029`，8 颗）

**动机**：B 波 `9qxQNek9`（S 0.97 / 2Y 1.42 / subU 1.15）是最接近"2Y 与 subU 双过线"的单信号，
按 `wq-brain-ra-deu` SOP 做**五维对照**（轴 / 口径 / 窗口 / 价差 / 数量），每条只碰 shortinterest3（ATOM）。
设置同上；并发 2；multisim `Nc4W88Xh5hzayVVgYwybEg`。

| # | alpha | 机制（表达式） | S | F | 2Y | subU | TO | DD | 对照角色 |
|---|---|---|---|---:|---:|---:|---:|---:|---:|---|
| 1 | `58ERZGXX` | `reverse(rank(ts_backfill(vec_avg(max_loan_rate),22)))` | **1.06** | 0.62 | 1.30 | 1.03 | 0.248 | 15.2% | 窗口对照（W22）→ 本波最佳 |
| 2 | `QPve1WxQ` | `reverse(rank(ts_backfill(vec_avg(mean_loan_rate),252)))` | 0.91 | 0.55 | 1.23 | 0.87 | 0.209 | 11.1% | 口径：均值费率 |
| 3 | `npv016jE` | `reverse(rank(ts_backfill(vec_avg(max_loan_rate_main),252)))` | 0.87 | 0.57 | 1.38 | 1.00 | 0.145 | 15.0% | ≡ B 波 `ZYQLOx60`（重复位） |
| 4 | `E563Zmd0` | `-rank(ts_backfill(vec_avg(max_loan_rate_main) - vec_avg(min_loan_rate_main),252))` | 0.84 | 0.57 | 1.12 | 0.81 | 0.137 | 15.9% | ≡ `−A1VdopmX`（价差正腿） |
| 5 | `zq3avAx1` | `reverse(group_zscore(ts_backfill(vec_avg(max_loan_rate),252),subindustry))` | 0.80 | 0.43 | **1.65** | 0.97 | 0.189 | 12.3% | 轴对照（subindustry）→ 本波最高 2Y |
| 6 | `xArMKlZb` | `reverse(rank(ts_backfill(vec_avg(max_loan_rate_p5_d1),252)))` | 0.79 | 0.46 | 1.47 | 0.83 | 0.152 | 13.1% | 口径：宽覆盖 p5_d1 |
| 7 | `0mYobGVG` | `reverse(rank(ts_backfill(vec_avg(min_loan_rate),252)))` | 0.57 | 0.29 | 0.80 | 0.40 | 0.203 | 13.3% | 尾部对照（最易借） |
| 8 | `qMLbK5QP` | `reverse(rank(ts_backfill(vec_avg(loaned_share_count),252)))` | −0.20 | −0.07 | −0.29 | 0.16 | 0.151 | 40.6% | 数量对照（可借券量） |

**对照实验矩阵（本波的归因主体）**

| 维度 | 腿 A | 腿 B | 读数差 | 结论 |
|---|---|---|---|---|
| 符号/方向 | `78LVeQE1` −0.92/−1.47/−1.12 | `j2YQqpGo` +0.92/+1.47/+1.12 | 逐位镜像 | 方向即信息，幅度对称（S 与 2Y 同值反号） |
| 价差方向 | `A1VdopmX` −0.84/−1.12/−0.81 | `E563Zmd0` +0.84/+1.12/+0.81 | 逐位镜像 | 同上；价差族无独立信息 |
| 覆盖口径 | 全样本 0.97/1.42 | main 0.87/1.38 | −0.10 / −0.04 | **全样本 > main > p5_d1（0.79/1.47）⇒ 宽度优先** |
| 分组轴 | plain rank 0.97/1.42 | industry 0.92/1.47 | −0.05 / +0.05 | 中性化细化买 2Y、卖 S |
| 分组轴（更细） | industry 0.92/1.47 | subindustry 0.80/**1.65** | −0.12 / +0.18 | 三档单调，subindustry 是本族 2Y 最高 |
| 窗口 | W252 0.97/1.42/subU1.15/TO0.201 | W22 **1.06**/1.30/1.03/0.248 | +0.09 / −0.12 | 窗口是 S↔2Y 权衡，不破上限 |
| 稀缺尾部 | max 0.97/subU1.15 | mean 0.91/0.87 · min 0.57/0.40 | 单调递减 | 信息在"最难借"的一档 |
| 价差 vs 水平 | 水平 0.97 | 价差 0.84 | −0.13 | 跨期限离散不是信息主体 |
| 数量 vs 价格 | 费率 0.97 | 可借量 −0.20 | 反向 | 信息在价格，不在数量 |

**结论**：族上限仍为 **S ≈ 1.06**（距闸 1.58 差 33%），单信号过闸在借券族**不可达**；
本波的价值是把"哪一维能动、能动多少"钉死（轴换 2Y、窗口换 S、口径换宽度），
同时给出两条可直接复用的等价式规则。

**⚠ 去重纪律（本波实测，按 `reverse(f) ≡ −f` 归一后逐条重算）**：8 条里**只有 1 条真重复**——
`npv016jE` = `reverse(rank(ts_backfill(vec_avg(max_loan_rate_main),252)))` 与 B 波 `ZYQLOx60` =
`-rank(<同字段同窗>)` 六项指标逐位相同（0.87/0.57/1.38/1.00/0.1452/15.02%）⇒ 白烧 1 个槽（波内 1/8 = 12.5%）。
`E563Zmd0`（+0.84）与 B 波 `A1VdopmX`（−0.84）**不是重复**：同一信号核的**反向**，B 波测到的是亏钱方向、
本波测出赚钱方向 —— 是新结论，但**不贡献新信号核**。⇒ 本波净增**信号核 6 个**。
**multisim 只做批内字符串去重**，跨波去重要按等价式判。全战役 71 行归一后 **66 个核**：
1 条精确重复 + 4 组同核反向镜像（`78LVeQE1`↔`j2YQqpGo`、`A1VdopmX`↔`E563Zmd0`、
`0mYW1d0q`↔`ZYQLO8MZ`、`0mYW1d3q`↔`JjeL6A1O`，每对里亏钱的那一侧是本轮有意做的方向对照）。

**⚠ 数据异常登记**：`58ERZGXX` 的 `checks.fail` 为空、`LOW_SHARPE/LOW_FITNESS/LOW_2Y` 落在 `warning`、
`CLUSTER_TEST` 落在 `pass`，而 `ra.ra_failed_checks` 列出三项硬闸 ⇒ 分桶 `checks` 与 RA 名单口径不一致。
入库按 §8.7 第 2 档（`checks_bucketed=True` 时取预算名单），数值不受影响，但**读 `checks.fail` 判"无硬闸"会误判**。

### 7.16 交付对账：60 颗目标与五条约束（2026-10-29 晚终核）

**A. 数量与口径**

| 项 | 值 | 证据 |
|---|---|---|
| 交付 alpha（平台 alpha_id） | **67**（20 + 39 + 8） | 逐 id 在库：首批 20 = wave A 的 18 + risk60 波 2（`leAZ9GPA`/`WjOm0z2G`）；+ wave B 39 + B5 8。三波共 **71 行**，另 6 行不计交付 = 4 条 analyst93 探针（`akKvOGWv`/`E56JKxrr`/`d5WLQmE2`/`E56JKbg0`）+ 2 条 sentiment27 归因对照（`npvVZ0jl`/`qMLqmKxv`） |
| 独立信号核 | **62** | `reverse(f)≡−f` 归一后只读实测：67 − 1 精确重复（`npv016jE`≡`ZYQLOx60`）− 4 组镜像第二腿（§7.15） |
| ATOM 占比 | **65/67 = 97%** | 硬判据 = `checks` 里有 `LOW_2Y_SHARPE` 且**无** `IS_LADDER_SHARPE`。71 行里 6 行带 `IS_LADDER_SHARPE`（全是 wave A），其中 4 行是探针 ⇒ 交付侧非 ATOM 仅 `j2Ym1PL9`/`RREWdlXe`，两条正是「借券门 + 分析师修正」的两数据集组合，与判据互相印证 |
| 目标 | 60 | **超 7 颗**（按 alpha_id）/ **超 2 个**（按独立信号核） |

**B. 五条约束逐条复核**

1. **未点亮塔 + 逐 category 画像**：§2（22,494 字段 / 16 类）+ §2.1（16 个 category 逐个 MCP 取证）+ §7.13（数据集分母对账）。✅
2. **近闸定向挖掘 + 论坛/论文模板 + 每条回测带归因与对照**：§4（11 类机制模板，含论坛帖 `43501264459799` 的借券需求评级与 `rank(A)−rank(B)` 残差模板的适用边界）、§7.5（Mode A 四轴）、§7.9（群轴探针）、§7.14/§7.15（覆盖/轴/窗口/尾部/数量五维对照矩阵）。✅
3. **并发 2 + 全 MCP + prod 必用 MCP**：三波均 `create_multi_simulation`（≤2 槽），收批/置状态/回写全走 `mcp__wqb_db__*` / `mcp__wq_brain_http__*`；脚本仅 3 个只读导出（`logs/_tmp_deu_*.py`）。prod 见 C。✅（prod 待复测）
4. **近十年有数据**：67 颗的 IS 窗口平台回读均为 2014-01-01–2023-12-31；`long_count` 全部 >0（79–145 只）。✅
5. **禁混腿（PV/MODEL/OTHER）**：第二批 39 + 定向 8 全部单数据集；本战役**未使用** PV/MODEL/OTHER 任何字段，
   受限组合消耗仍为 **2/5**（`bl63xzW6`/`9qxQGMaq`，PV `returns`，前序已用）。✅

**C. 相关性与提交状态（MCP 实测）**

- **self-corr（本地池比对）**：`9qxQNek9` **0.291** / `j2YQqpGo` **0.285** / `1YN5rxRQ` **0.425**，三条均 < 0.7（池 10 颗 OS，PPA 1 颗不计）。
- **prod-corr：无结论（未取到值，既非通过也非失败）**。全过程四次 MCP 调用、零次落库：
  ① 08:06 首次 `refresh=True` → 跨会话 `correlation_busy`，holder = `corr:get_production_correlation(Xg9qjVOz)`（另一会话占单槽），按纪律停止；
  ② 08:08 槽空闲后重发 → 平台开始计算，MCP 返回 `inflight=true`（本机标记，TTL ≥300s），未重触发；
  ③ 08:12 标记到期后再发 → **平台计算 > MCP 读窗口（120s），调用在传输层超时**（skill `wq-prod-corr-read` 故障 2：
  超时不落缓存，下一次仍是完整阻塞）；
  ④ 读 `alpha_corr_cache` 复核 = **0 行**（该表现在只有 `j2Ym1PL9` 08:13 那条），确认没有值落盘。
  ⇒ 按同 skill §四「终验只测马上就要提交的那一颗」，**本战役无一颗可提交候选，故不再占用账号级单槽**；
  待未来真有候选过 IS 全闸时，再按「一次一颗 + refresh=True」终验。
- **提交状态：0 提交**。三波均无 IS 全过候选；`j2Ym1PL9`（S 1.57）仍是唯一近闸，其 prod 0.5971 / self 0.4213 已落库。

**D. 本轮新增的台账/口径修正**

1. **「水平族要纯度」不成立**：该法则只在 `lending_fee_bid_rate` 上测过；`max_loan_rate` 上实测是
   **全样本 0.97 > main 0.87 > p5_d1 0.79**（宽度优先）⇒ §7.2-7 需按此读作**字段级**结论，不可跨字段外推。
2. **跨波去重必须按等价式**：`reverse(f(x)) ≡ −f(x)`；B5 的 8 条里 2 条因此是重复位（§7.15）。
3. **`checks.fail` 为空 ≠ 无硬闸**：分桶 `checks` 会把 RA 硬闸放进 `warning`，RA 名单只在 `ra.ra_failed_checks`（§7.15 异常登记）。
4. **wave 级 `dataset` 标签会污染按数据集聚合**：B 波 39 行统一写 `mix_unlit_tower_b`，真实归属需按字段前缀反推（§7.14 族分布）。
5. **`expressions.alpha_id` 回填仍未生效**：§7.4 记的收批关联修复需重启 `wqb-db` MCP 服务；B 波 49 条与 B5 8 条仍在 `alpha_id=NULL`。

**E. 塔位结论不变**：67 颗全部为 regular alpha，**未新增点亮塔**。SHORTINTEREST 的单信号上限经两轮独立测量
（B 波 0.97 / B5 1.06）确认为 **S ≈ 1.06、2Y ≈ 1.65**（后者来自 subindustry 轴），距离闸 1.58 差 33%；
INSIDERS / SENTIMENT / NEWS 的判死结论见 §7.3，未被本批推翻。
