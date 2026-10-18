# GBR × analyst（组合分支）

> 回到 [GBR 区域流程](../SKILL.md) · [GBR profile（证据与历史）](../../wq-brain-ra-pipeline/references/regions/GBR.md) · 实时生效画像：`$WQ_PY -m wqb.profiles explain --region GBR --category analyst`

<!-- profiles:cell-panel:start -->
**状态**：active（跟区域入场 active）　**分组**：Analyst　**类别卡**：analyst

**涉及数据集**：analyst44、analyst47、analyst48、analyst7、analyst9、analyst93、analyst_consensus

### 回测设置（进仿真的值）

| 设置 | 值 | 来源 |
|---|---|---|
| instrumentType | EQUITY | 区域 settings.json |
| region | GBR | 区域 settings.json |
| universe | TOP700 | 区域 settings.json |
| delay | 1 | 区域 settings.json |
| neutralization | SUBINDUSTRY | 区域 settings.json |
| decay | 4 | 区域 settings.json |
| truncation | 0.08 | 区域 settings.json |
| maxTrade | ON | 区域 settings.json |
| pasteurization | ON | 区域 settings.json |
| unitHandling | VERIFY | 区域 settings.json |
| nanHandling | ON | 区域 settings.json |
| language | FASTEXPR | 区域 settings.json |
| visualization | false | 区域 settings.json |
| startDate | 2014-01-01 | 区域 settings.json |
| endDate | 2023-12-31 | 区域 settings.json |

### 阈值

- Mode B 主闸 sharpe / fitness：1.25 / 0.8（default；下限锁生效，实时值看 explain）
- 其余阈值跟区域 thresholds.json（本组合无覆盖）

### 证据（2026-10-04 只读汇总）

| 回测 | RA 全过 | prod 已测 | 其中低于上限 | 判死 | 胜绩 |
|---|---|---|---|---|---|
| 63 | 0 | 0 | 0 | 5 | 0 |

主要数据集（回测数）：analyst7（36）、analyst93（24）、analyst_consensus（3）

### S1 字段理解

- 分清 actual_*（已实现、事后）与 mean_estimate_* / flash（预测、前瞻）：IND analyst_consensus 前 16 条全灭的真因是用了 actual（DEC-77）
- VECTOR 先 vec_avg / vec_count 聚合；JPN 下 vec_* 外再套 ts_* 会报错
- 窗口（类别卡，均在白名单内）：monthly 22/66；quarterly 66/252

### S2 生成

- **类别通用原语**（类别卡，跨区）：
  - revision surprise: change in FY1/FY2 vs the stale level
  - dispersion: disagreement across estimates, not the consensus mean
  - breadth vs magnitude: how many estimates moved, not how far the mean moved
  - horizon gap: FY2 minus FY1 as a growth-expectation residual
  - rating momentum: upgrade/downgrade frequency vs historical baseline
  - target price gap: current price vs consensus target (upside/downside)
  - estimate acceleration: second derivative of estimate revisions
- **跨区结论**（USA/GLB/HKG/KOR/EUR/DEU/GBR；negative）：flash / pretax 一致预期动量族只在 IND 有效，别的区 ／S／ 都在 1.07 以下（证据：waves probe_flash_eps_20260919 / probe_pretax_20260919：USA ≤0.09、GLB ≤0.08、HKG 0.64、KOR ≤1.07、EUR ≤0.96、DEU ≤0.72、GBR ≤0.54） <!-- lint:const-ok 证据原文 -->
- **跨区结论**（KOR/USA/DEU；negative）：分析师主信号族普遍撞 prod 墙（证据：KOR analyst10/16/44/consensus（RULES §G）；USA-ANALYST44-BREADTH-DEAD-EP-PRODWALL（E/P z prod 0.93）；DEU analyst93 prod 饱和） <!-- lint:const-ok 证据原文 -->
- **禁止**（类别卡）：禁止使用裸 rank(estimate)（必须 ts_delta 或 group_zscore）
- **禁止**（全局锁定）：禁止两条独立信号腿相加：加权（0.4×A + 0.6×B）、等权 add(rank(A), rank(B))、中缀 + 都算；第二个数据集只以条件（trade_when / if_else）、分组（group_rank / bucket）或残差（regression_neut / vector_neut）入场
- **禁止**（全局锁定）：禁止 ts_event_* 系列（平台没有）与幽灵算子；字段名逐一经 get_datafields 验证

### S4 改进（按顺序试：组合 → 类别卡 → 全局）

1. [全局] 判「无解 / 天花板」前先扫等价算子替换：signed_power → quantile、ts_scale → quantile / normalize。数值路径不同，一次动多个闸（含 prod，要读全部闸）（KOR/GLB 复现：KOR other466 signed_power→quantile：2Y 1.51→1.56、prod 0.6544→0.6397；GLB quantile 替 ts_scale：S +0.20、F +0.06、prod 0.475→0.565（DEC-72）） <!-- lint:const-ok 证据原文 -->
   - 注意：效应量逐区实测，禁外推；quantile 只收 1 个参数
2. [全局] 强但撞 prod 墙的快信号：用一个经济子集门控（trade_when 进 >0.5 出 <0.4 的慢变量，或 rank(cap)>0.2 ∩ 子集）只在子集里持仓（GLB/ASI/IND 复现：GLB-DL20D-SUBSET-GATE-FAMILY-20260921（prod 0.82→0.60–0.67）；ASI LLNgdpw2 / 88jaV5lv；IND ZYbqREW1 / levk5JYN（prod 0.54–0.55）） <!-- lint:const-ok 证据原文 -->
   - 前提：未门控的基础信号 IS sharpe 不低于 2.5、fitness 不低于 1.5（GLB 2026-09-27 铁律：门控只修 prod / robust，不造强度）；慢信号门控后换手会升，只用于快信号
- 提醒：prod 与 self 两个端点都取 max、都过线才可提；不改持仓的降 prod 杠杆（hump、加大 decay）会把 self 推爆（EUR wave274） <!-- lint:const-ok 证据原文 -->
- 提醒：设置是强度闸：nanHandling / maxTrade / decay / 中性化换档等于换信号，跨档结果不可比（IND 行为族 S 2.19→0.46） <!-- lint:const-ok 证据原文 -->
- 提醒：decay 匹配信号速度：快信号上 decay 越大越差；decay 0 与 1 逐位相同，只留一个 <!-- lint:const-ok 证据原文 -->
- 提醒：prod 墙先看直方图分单颗钉子 / 密墙 / 可破三型，再决定换分母、换设置档或分组轴（决策表 D0-P 诊断前置） <!-- lint:const-ok 证据原文 -->

### S5 提交前

- 资格判定：`$WQ_PY tools/mode_b_qualify.py evaluate --region GBR --sharpe <S> --fitness <F> --two-year-sharpe <2Y>`（喂全指标，旁路 A–E 才会生效）
- 提交链：`submit_verdict` 只否决；prod 与 self 双端点实测（`check_correlation(refresh=True)`）；用户明确确认后才 `workflow_submit_alpha(confirm_submit=True)`——见 `worldquant-submit-alpha`

### 判死记录（不要重试；「归属」= payload 绑定 / 由条目名推断 / 关键词推断）

| 条目 | 族 | 下次怎么办 / 说明 | 数据集 | 归属 |
|---|---|---|---|---|
| GBR-ANALYST7-REVISION-DECAYED | analyst7_revision_momentum | analyst7 revision-momentum 家族 (est_12m_ebt/net/sal/pre + est_q_* raised/lowerednum) 不再生成新变体——整个家族在 GBR 已拥挤化衰减；dispersion | analyst7 | payload | <!-- lint:const-ok 证据原文 -->
| GBR-ANALYST9-DEAD | analyst9 | 不生成 analyst9 表达式 | analyst9 | inferred | <!-- lint:const-ok 证据原文 -->
| GBR-ANL44-EPS-REVISION-CEILING | analyst44_eps_sales_revision | analyst44 anl44_2_*预期修正族不再生成新变体；与analyst7 est_*族合并为GBR分析师域判死 | analyst44 | inferred | <!-- lint:const-ok 证据原文 -->
| GBR-ANL47-SENTIMENT-TSQUANTILE-PINNACLE | analyst47_rawsentiment_tsquantile_signedpower | 本轮不再生成rawsentiment ts_quantile族新变体；收手非判死，顶点族列为GBR最强资产（D4过线+prod干净） | analyst47 | inferred | <!-- lint:const-ok 证据原文 -->
| GBR-ANL48-BBPDIIP-CEILING | analyst48_bbpdiip_level_momentum | analyst48 anl48_bbpdiip族不再生成新变体；GBR analyst域第三条判死（analyst7/44/48） | analyst48 | inferred | <!-- lint:const-ok 证据原文 -->
<!-- profiles:cell-panel:end -->

## 补充说明（手写）

<!-- profiles:manual:start -->

### ★ 2026-10-13 · GBR 类别选择实证（「未点亮塔 × ALIVE 密度」双条件）

用户指令：不换 region、**已点亮塔不选**、优选有潜力、不频繁换数据集。据此建立唯一可执行的选区判据：

| category | 当季塔计数（`get_pyramid_alphas`） | ALIVE 字段数（`field_profile --query --verdict ALIVE`） | 判决 |
|---|---:|---:|---|
| MODEL | 5（**≥3 = 已点亮**） | 26 | **排除**（用户规则） |
| **ANALYST** | **2** | **20** | ✅ **本回选定** |
| OTHER | 1 | 3 | 备选 |
| PV | 1 | 3 | 备选 |
| 其余 10 类 | 0 | **0** | 无 ALIVE，不进白名单 |

> GBR 的类别选择**只剩一个真判据**：ALIVE 字段落在哪一类。塔计数与 ALIVE 分布**互相独立**——MODEL 已点亮却 ALIVE 最多；ANALYST 未点亮而 ALIVE 第二多。
> ALIVE / WEAK 全表已落盘 `cache/_gbr_alive.txt` / `cache/_gbr_weak.txt`（52 / 48 条，2026-10-13 快照）。

### ★ 2026-10-13 · GBR analyst 数据集实测全景

| 数据集 | 字段 | GBR 回测记录 | 最好 S | 状态 |
|---|---:|---:|---:|---|
| `analyst7` | 502 | 36（本地库）+ 平台大量 | 2.13（单信号） | breadth/pre 族**已判死**（拥挤化衰减） |
| `analyst47` | 5 | **46** | **1.95** | 单族（ts_quantile+signed_power），**F 硬顶** |
| `analyst9` | 51（VECTOR） | **0** | 单信号 1.69 / 2Y 1.19 | 处女池（2Y 隐患） |
| `analyst69` | 292 | 0 | 1.11（WEAK） | cov≈0 |
| `analyst93` | 100（VECTOR） | 24 | **0.80** | **类型 D**：2Y 1.65~1.84 但 S 差 2× |
| `analyst_factor_signals` | **96** | 25 | 0.71 | 93/96 未测（本塔最大未测 MATRIX 池） |
| `analyst_earnings_ibes` | 42 | — | 2.07 | **归 MODEL 类**，不进本塔 |

### ★★ 同一字段「骨架族决定成败」差异可达 7×（本回最硬的新证据）

同一 `anl47_indicator`（cov 1.00，单信号 S 1.78）：
- `winsorize(signed_power(ts_quantile(anl47_rawsentiment,504),0.3), std=2.0)` → **S 1.95 / F 0.96 / 2Y 1.75 / sub 1.30**
- GBR house 骨架（`group_rank(ts_target_tvr_decay(winsorize(rank(X)),…), sector)`）→ **S 0.0 ~ 0.28**（波 `gbr_anl47_wa`，8 条，6 族）

⇒ **house 骨架不可当默认器**。「DEAD 判定实为『在该骨架下不行』」在本回再次被证实。
⇒ **纪律**：对「单信号强但 family 窄」的字段，先补扫 `ts_quantile` + `signed_power` 这类**非线性压缩族**，再谈判死。

### ★ analyst47 顶点族是「类型 C（差一闸）」，不是判死

`GBR-ANL47-SENTIMENT-TSQUANTILE-PINNACLE` 的判死理由写的是「D4 过线 ⇒ 最强资产 ⇒ 收手」。**该前提与平台 RA 口径不符**：D4 是本地资格门（S≥1.25 / F≥0.8），而平台 RA 的 `LOW_FITNESS` 线是 1.0 ⇒ **F 0.96 = FAIL**。46 条全史里 40+ 条是同一 family 的包装变体，全部卡在 F 0.76~0.96。
⇒ 该条目应从「收手」改判为 **类型 C（差 F 0.04）**，按「近似项（差一闸）必须挂已证修复器复测」纪律**保留复访权**。

### ★ analyst93 = 类型 D（2Y 稳 S 弱）实证

`group_rank(vec_avg(anl93_analyst_consistency), sector)` → S 0.75~0.80 / **2Y 1.65~1.84**（> 闸 1.58）。
⇒ 2Y 不是瓶颈、**IS 是瓶颈**；S 缺口 2× ⇒ 高风险保留项，只能换量纲复访。

### 毒药字段（analyst9 VECTOR 内，勿当信号）

`*_splitfactor` / `*_totime` / `*_effectivetime` / `*_estimatetime` / `*_isexcluded` / `*_isnmflag` / `*_parentflag` / `*_consensus_*_value`（lookup 索引）= 元数据/码。

### ★★ 复现记录前必须从平台取设置（本回踩坑实录）

按区域缺省（decay 4 + SUBINDUSTRY）重跑 `winsorize(signed_power(ts_quantile(anl47_rawsentiment,504),0.3), std=2.0)`，只得 **S 1.34 / TO 0.262**，与记录 **S 1.95 / TO 0.190** 相差极大。
根因：记录的真实设置是 **decay 2 + STATISTICAL**（`get_alpha_details(zqbrK3k8).settings`）。
⇒ **纪律：复现某条历史 alpha 前，先用 `get_alpha_details` 拉其 `settings`；区域缺省 ≠ 该记录的设置。** 本地 `backtest_results.payload_json` 可能为空。

### ★★★ analyst47 ＝ LOW_FITNESS 硬墙（F 族不变量，本回最重要否证）

**全参数空间扫描（80 条仿真）后结论：F 恒定在 0.96~0.97，S↔TO 严格同向 ⇒ 无法过 `LOW_FITNESS ≥ 1.0`（差 0.03~0.04）。** <!-- from config.thresholds.json：LOW_FITNESS 线 -->

| 维度 | 扫过 | 最好结果 |
|---|---|---|
| `signed_power` 指数 | 0.15 / 0.2 / 0.25 / 0.3 / 0.35 / 0.5 | 0.2~0.3 最优（S 1.95~1.97）|
| `winsorize` std | 1.5 / 2 / 3 / 4 / 6 / 10 / 不加 | **3.0 最优（S 1.97 F 0.97）**，4+ 饱和 |
| `ts_quantile` 窗 | 300 / 400 / 504 / 650 | 504 最优 |
| sim `decay` | 2 / 4 / 8 | **8 ⇒ TO 0.152（−20%）但 S 1.60（−19%）** |
| 中性化 | STATISTICAL / SUBINDUSTRY / FAST / REVERSION_AND_MOMENTUM | STATISTICAL 最优；**R&M ⇒ S 1.38** |
| nanHandling·maxTrade | ON·ON / OFF·OFF | ON·ON 最优；**OFF ⇒ TO 0.277、F 0.78** |
| 残差化×平滑修复器 | `ts_mean(group_neutralize(X,sector),100/66)` | **S 0.26~0.28（灾难）** |

**机制**：F = S × √(returns / max(TO, 0.125))；本族里 S 与 1/√TO 严格同向 ⇒ 乘积不变。**F 是该族的经济不变量，不是结构问题**。
⇒ 判死形态新增一类：**「F 墙（不变量型）」**——与形态 A「prod 墙」、B「2Y 塌」并列：IS 三闸（S/F/2Y/sub）中**只剩 F 差 ≤0.05 且全参数空间扫不上去**。

### 2026-10-13 派发台账（11 波 88 条；每波 8 条，全部过五道发批闸 + 骨架审计）

| 波 | sim | 目标 / 设置 | 最好结果 |
|---|---|---|---|
| `gbr_anl47_wa` | `19Vf2D9mp5639nI26jcnU2h` | analyst47 house 骨架（6 族）· SUBINDUSTRY/decay4 | **S 0.0~0.28 全弱** ⇒ house 骨架不适用 |
| `gbr_afs_w2` | `Igz7yP54HObmxHDVhnJLr` | analyst_factor_signals 未测池 · 同上 | **S 0.09~1.0 全弱** ⇒ 该池连 IS 都不行 |
| `gbr_anl9_w3` | `1tAPfXXd4OL9YM1fuAbH88x` | analyst9 VECTOR 处女池 · 同上 | **S −0.25~0.50 全弱** ⇒ 处女池确无信号 |
| `gbr_anl47_wd_sub` | `1NftHvaXa4Zsa62puBc3Tm0` | analyst47 参数扫 · SUBINDUSTRY/decay4 | S ≤1.38（设置错，作废）|
| `gbr_anl47_wd_fast` | `ZKkwm4TP4uU9CNvnppVxi5` | 同上 · FAST/decay4 | S ≤1.55（同上）|
| **`gbr_anl47_we`** | `33QquXdID4lWc6RpMKvjaQH` | **analyst47 参数扫 · STATISTICAL/decay2（正确设置）** | **基线复现 1.95/0.96；`zqrvbdYX`（std=3.0）S 1.97 F 0.97** |
| `gbr_anl47_wf_d8` | `35uCeua9459Mbds2KCNIbUf` | 同上但 decay 8 | S 1.60 / TO 0.152 / F 0.80 |
| `gbr_anl47_wg_rm` | `3JxjAh4gw5c6a6XuFJBnf9O` | 同上但 REVERSION_AND_MOMENTUM | S 1.38 / F 0.68 |
| `gbr_anl47_wh_nanoff` | `4nbH145L74Jdbq350Y7UCgJ` | 同上但 nanHandling/maxTrade OFF、trunc 0.1 | S 1.93 / TO 0.277 / F 0.78 |
| `gbr_anl47_ws` | `1P1f7UcFC4Zbc481gbsrX53R` | std/指数/窗细扫（STATISTICAL/decay2）| **S 1.96~1.97 / F 全 0.97（饱和）** |
| `gbr_techindi_wx` | `4Eezixdjs4i8bgb9vkbIlcX` | OTHER×techindi_model 未采 ALIVE（CROWDING/decay2）| 见 other.md |

⇒ **ANALYST 五个数据集本轮全部判死**：`analyst7`（breadth族拥挤）+ `analyst47`（**F 墙**）+ `analyst9`（处女池无信号）+ `analyst_factor_signals`（IS 弱）+ `analyst93`（S 弱）。
⇒ GBR 未点亮塔里 ANALYST 已无路；按用户「无计可施才换」纪律，下一步只剩 OTHER（techindi_model）。

### ★★★ 2026-10-14 · analyst7 的 ALIVE 是画像伪影（重要方法论实证）

**背景**：画像 ALIVE 全表显示 analyst7 有一批 **2Y 极高**的字段（全区最高）：
| 字段 | S_sg | 2Y_sg | n_tests |
|---|---:|---:|---:|
| `est_12m_pre_low`（最低税前利润预期） | 1.90 | **2.72** | 134 |
| `est_12m_pre_mean` | 1.66 | **2.15** | 39 |
| `est_12m_pre_raisednum_1mth` | **2.13** | **2.10** | 9 |
| `est_12m_pre_raised_1wk` | 1.99 | **2.08** | 14 |
| `est_12m_pre_raisednum_4wks` | 1.96 | **2.05** | 76 |

（2Y ≥ 2.02 意味着可直通严档 ⇒ 理论上是最优先攻击目标。）

**实测：该 ALIVE 不可复现。**
1. **`est_12m_pre_low` 在 GBR `backtest_results` 中 0 行**（`LIKE '%est_12m_pre_low%'`），n_tests=134 无出处。
2. 本地仅有的 3 条 `pre_*` 行全是 SUE 型构造，最高 **S 0.67**：
   `winsorize(divide(ts_delta(est_12m_pre_mean_4wks_ago,22), add(est_12m_pre_std_3mth_ago,0.01)), std=4)`
3. **三组构造实测全部 ≤0.37**（`group_rank(..., sector)` @ CROWDING/decay2）：
   | 构造族 | 代表 | 最好 S | TO |
   |---|---|---:|---:|
   | 水平量/时序分位 | `ts_mean(est_12m_pre_low,22)` / `ts_rank(pre_mean,252)` | **0.02 / 0.18** | 0.019 / 0.048（**近静态**）|
   | 比率/离散度 | `divide(pre_std,pre_mean)` / 广度比 / 偏斜 / 区间宽 | **−0.17 ~ 0.37** | 0.023~0.077 |
   | SUE 型（修正/离散度标准化）| `divide(ts_delta(pre_mean,22), add(pre_std,0.01))` | 见 P3 | — |

**★ 铁律（已写入 [_probe-sop.md](_probe-sop.md) 第 0 步第 6 条）**：
**`ALIVE`/`WEAK` verdict 必须先在本地 `backtest_results`（region=该区）找到对应行才可采信；`COUNT=0` ⇒ 视为 UNTESTED，按探针规格重测。** 否则会把画像伪影当机会，白烧整批。
另：**判死一个「计数/广度族」数据集前，必须把「比率/离散度/标准化」形态各测一次**——mechanism 族 ≠ 原始字段族。

<!-- profiles:manual:end -->
