# EUR × analyst（组合分支）

> 回到 [EUR 区域流程](../SKILL.md) · [EUR profile（证据与历史）](../../wq-brain-ra-pipeline/references/regions/EUR.md) · 实时生效画像：`$WQ_PY -m wqb.profiles explain --region EUR --category analyst`

<!-- profiles:cell-panel:start -->
**状态**：probe（跟区域入场 probe-only）　**分组**：Analyst　**类别卡**：analyst

**涉及数据集**：analyst10、analyst11、analyst39、analyst45、analyst9、analyst_consensus、analyst_factor_signals

### 回测设置（进仿真的值）

| 设置 | 值 | 来源 |
|---|---|---|
| instrumentType | EQUITY | 区域 settings.json |
| region | EUR | 区域 settings.json |
| universe | TOPCS1600 | 区域 settings.json |
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
| 74 | 0 | 0 | 0 | 8 | 0 |

主要数据集（回测数）：analyst9（27）、analyst45（14）、analyst_factor_signals（9）、analyst_consensus（8）、analyst11（8）、analyst10（8）

### S1 字段理解

- 分清 actual_*（已实现、事后）与 mean_estimate_* / flash（预测、前瞻）：IND analyst_consensus 前 16 条全灭的真因是用了 actual（DEC-77）
- VECTOR 先 vec_avg / vec_count 聚合；JPN 下 vec_* 外再套 ts_* 会报错
- 窗口（类别卡，均在白名单内）：monthly 22/66；quarterly 66/252

### S2 生成

- **说明**：★★★ 【MATRIX ⇒ TO 崩」的适用边界修正】此前基于 f72/f17（年度/季度财报）得出「MATRIX ⇒ TO 崩 0.017–0.029」；但 **analyst_factor_signals（108 字段全 MATRIX，日频分析师修正）实测 TO 可达 0.087**（'eps_q1_estimate_change_1mo' S0.71/TO0.087）。⇒ ★ **规则应表述为：TO 崩的是「低频更新字段」（年度/季度财报），而非所有 MATRIX**；**日频事件型 MATRIX（分析师修正/预估值）TO 正常** ⇒ 选集时看**更新频率**而非仅看 type。⚠ 但仍需逐字段实测：同数据集内 'eps_estimate_volatility_adj_3yr' TO 仅 0.0272（慢变量）、'eps_actual_q1_yoy_growth' TO 0.0253 ⇒ **快变量（change/revision/surprise）TO 合格，慢变量（level/volatility/CAGR）TO 崩**。
- **说明**：★★★★ 【EUR Analyst 首个全闸门通过配方】（2026-10-13，wave472–485，13 波 104 条实证）： **数据集 = 'analyst_factor_signals'**（108 字段全 MATRIX、104 个 user≤3；**日频分析师修正 ⇒ TO 正常**，推翻「MATRIX ⇒ TO 崩」的过度泛化）。 **达标表达式**：'ts_target_tvr_decay(signed_power(group_rank(divide(eps_revision_magnitude, ts_mean(eps_y1_estimate_coeff_var, 55)), industry), 1.8), lambda_min=0, lambda_max=1, target_tvr=0.18)' ⇒ alpha 'ZYAJZL93'：**S1.67 / F1.04 / TO0.1047 / 2Y1.81 / margin9.27bp / PROD0.6617 / SELF0.2278，FAIL 0 WARNING 1（仅信息性），all_passed=True**。 **四层杠杆（按增益排序）**： ① ★★★**「修正幅度 ÷ 分歧度」原语**（'revision_magnitude / coeff_var'）= 0.71→**1.32**（S +0.61）—— 对应 S2 类别原语的 revision surprise ÷ dispersion； ② ★★**分组轴 'industry'**（vs sector 1.32 / market 1.29 / c5 0.96）； ③ ★★**'target_tvr' = S 与 2Y 的同步杠杆**（0.06→0.10 使 S1.43→1.58、2Y1.34→1.53；0.12 后饱和）； ④ ★★★**分母 'ts_mean' 平滑（窗 55）= 三重杠杆**：提 2Y（1.55→**1.81**）、降 prod（0.7064→**0.6617**）、保 S —— 机制：平滑分歧度 ⇒ 分母稳定 ⇒ 持仓集中 ⇒ 小宇宙改善 + 与存量 alpha 相似度下降。 **幂次**：'signed_power' 1.6–1.8 最优（1.8 给 F≥1.0，1.45–1.55 给 2Y 更高）。 ⚠ **失效项**：'revenue_*' / 'netprofit_*' 版本（同结构下 S 仅 1.13/1.07）；跨指标 multiply；'eps_y2_estimate_coeff_var' 分母（S1.45）；horizon gap（y2−y1 consensus，S −0.75 需翻转）；TOP2500（S 崩到 1.34–1.40）；decay=4（S 1.47）⇒ **TOPCS1600+SUBINDUSTRY+decay1+maxTradeOFF 是必要条件**。
- **说明**：★★★★★ 【EUR Analyst 战役终局定论】（2026-10-13，wave472–492，**21 波 168 条实证**）： **结论：Analyst 类别可提交 regular alpha = 1 颗**（不是 10 颗）。 **唯一达标形态**：'ts_target_tvr_decay(signed_power(group_rank(divide(eps_revision_magnitude, ts_mean(eps_y1_estimate_coeff_var, 55)), industry), 3.0), lambda_min=0, lambda_max=1, target_tvr=0.18)' ⇒ alpha **'O083qZQp'**：S1.71 / F1.09 / TO0.1123 / 2Y1.78 / margin9.02bp / **PROD 0.6170** / verdict FAIL 0。 **为何只能是 1 颗（互相关实测）**：同族 4 颗达标候选 'get_mutual_correlation' = **0.9757–0.9993**，'max_mutually_below_subset_size=1' ⇒ 提交 1 颗后其余全部触发 self-corr ⇒ **一条腿只出 1 颗**。 **六层杠杆（增益排序，全部实证）**： ① ★★★'eps_revision_magnitude ÷ 分歧度' 原语（0.71→1.32）； ② ★★轴 = 'industry'（industry 1.38 > sector 1.32 > market 1.29 > c5 0.96）； ③ ★★★'target_tvr' = S 与 2Y 同步杠杆（0.06→0.18；0.22 后饱和）； ④ ★★★分母 'ts_mean' 平滑（窗 **55**；窗88 亦达标，窗44/33 使 2Y 崩）； ⑤ ★★★**'signed_power' 幂次 = S/F 提升器 + prod 降低器**（1.8→3.0：S1.67→1.71、F1.04→1.09、**prod0.6617→0.6170**）； ⑥ 窗 55 是 prod 的关键（窗44 prod 0.7064 > 0.7 ⇒ 失败）。 ⚠ **判死清单**：'revenue_*'/'netprofit_*' 版本（S≤1.49）；'eps_y2_coeff_var' 分母（1.45）；'change_3mo' 分子（0.91）；'consensus_value' 分子（负）；期限差（−0.97）；'cagr_*' 分子（≤0.51）；'asymmetry'/'volatility' 分母（≤0.42）；跨指标 multiply（0.11）；'analyst_consensus' breadth（≤0.21）；'analyst45'（0.36）；'analyst9/10' 共识水平（≤0.76）；sector/market/subindustry 轴（2Y ≤1.50）。 → **要凑够 10 颗须离开 Analyst 类别**（Analyst 内唯一有效结构已穷尽）。
- **说明**：★★★★★ 【EUR × analyst 数据集【全量 16 个】最终覆盖表】（2026-10-13 收官） ／ 数据集 ／ 规模 ／ 最佳 S ／ 判定 ／ ／---／---／---:／---／ ／ ★**'analyst_factor_signals'** ／ 108 MATRIX ／ **1.71** ／ ★**胜出**（'786pLKnb' 全闸门+prod/self 过） ／ ／ 'analyst69' ／ 297（**247 VECTOR**, cov 1.0） ／ 1.48 ／ ❌ **结构性矛盾**：alpha 依赖高频换手（TO 0.29）；压制换手后 S→0.75 且 2Y 转负 ／ ／ 'analyst4' ／ 264（134 VECTOR, cov 0.965） ／ 0.65 ／ ❌ TO 仅 0.020（低于下限）+ 2Y 0.05 ／ ／ 'analyst45' ／ 61 VECTOR ／ 0.36 ／ ❌ ／ ／ 'analyst14' ／ 113 MATRIX ／ 0.48 ／ ❌ 2Y 负 ／ ／ 'analyst15' ／ 297 MATRIX（含多窗修正变化 '*_gr_12_m_{1m,3m,6m}_chg'） ／ 0.17 ／ ❌ ／ ／ 'analyst39' ／ 24 MATRIX ／ 0.19 ／ ❌ ／ ／ 'analyst40' ／ 16（董事变动） ／ 0.20 ／ ❌ **TO 1.50–1.63 爆炸** ／ ／ 'analyst7' ／ 299 MATRIX（actual 值） ／ 0.10 ／ ❌ ／ ／ 'analyst9' ／ 111 VECTOR ／ 0.45 ／ ❌ ／ ／ 'analyst10' ／ 961（39 VECTOR 多为元数据） ／ ≤0.76 ／ ❌ ／ ／ 'analyst11'/'analyst_consensus' ／ 445/1929 ／ ≤0.21 ／ ❌（breadth 无信号） ／ ／ 'analyst_base_ref' ／ 17（股数/价格参考） ／ 0.36 ／ ❌ 2Y −0.58 ／ ／ 'model52'（列在 analyst 类） ／ 3（违约概率 PD） ／ −0.17 ／ ❌ cov 0.199 过低 ／ ／ 'analyst81' ／ 5 ／ — ／ 跳过（cov 0.25 < 0.35） ／ ⇒ ★★ **analyst 类别 16 个数据集全部探过，唯一可提交结构 = 'eps_revision_magnitude ÷ 分歧度'**。
- **说明**：★★★★★★ 【EUR × analyst 收官补充：RA 通道被 PPA 占腿封闭】（2026-10-17，波 568–577，10 波 ≈100 条） ① **塔态权威**：EUR/D1 analyst 塔 = 1（'786pLKnb'，**PPA 通道**）⇒ 按项目口径该塔实际无 RA 产出。 ② ★★★★★ **唯一有效原语的 IS 甜点窗谱**（'eps_revision_magnitude ÷ ts_mean(eps_y1_estimate_coeff_var, W)' + tvr0.18 + p3.0 @ industry）： ／ 窗 W ／ S ／ 2Y ／ prod ／ 判定 ／ ／---:／---:／---:／---:／---／ ／ 55 ／ 1.71 ／ 1.78 ／ 0.6170 ／ = '786pLKnb'（PPA ACTIVE） ／ ／ **60** ／ **1.75** ／ **1.74** ／ **0.9920** ／ ★ IS 全过（'0mj9nM36'/'58j39lpM' failed_ra=0）但**同腿**（互相关 0.994） ／ ／ 66 ／ 1.66 ／ 1.50 ／ 0.9818 ／ 2Y 差 0.08 + 同腿 ／ ／ 77 ／ 1.58 ／ 1.48 ／ — ／ 双差 ／ ／ 88 ／ 1.52 ／ 1.20 ／ — ／ 双差 ／ ⇒ ★★★ **全部窗变体与 786pLKnb 互相关 ≥0.98 ⇒ 'revision_magnitude ÷ dispersion' 族对 RA 通道封闭**（PPA 在 prod 池）。 ③ **'eps_y1_estimate_change_3mo' = 最强单字段（S 1.90/F 1.33）但 2Y 硬顶 ~0.93**： tvr/ts_mean 平滑/换 sector·market 轴/换分母(skewness·asymmetry)/ts_delta 加速度/TOP2500宇宙 **全部无效**（2Y 0.28–0.93）⇒ 快信号结构性缺 2Y。 ④ **'analyst10'（294 字段）判死 = 噪声型**：原始 revise 值 TO 1.40–1.75 爆炸；ts_mean(22) 平滑后 TO 修复但 S 塌到 0.03–0.70、2Y 转负（平滑即杀）。 breadth（innovate_increase−decrease）、Margin Scissor（cpxrevise−ebirevise）、pred_surps、smun 归一化**全灭**。 ⑤ **'analyst_consensus'（300 字段）无预测值字段**（只有 actual_value + estimate_count + flag）⇒ vec_avg 动量/vec_stddev 分歧度/count 动量全灭（S ≤0.88）。 ⑥ **残差化（IND 2026-10-16 新结构）在 EUR analyst 不适用**：decay126 下 S 0.51–1.65 但 2Y 全 DEAD（0.37–1.08）—— EUR analyst 信号本就「残差状」。 ⑦ **算子替换杠杆无效**：'group_zscore' 替 'signed_power(group_rank)' ⇒ S 1.75→1.12；'quantile/normalize/ts_scale' 批两次整批 ERROR（平台瞬态，毒表达式未隔离，但该杠杆已被 group_zscore 结果否证）。 ⑧ **门控杠杆无效**：trade_when(高分歧度) ⇒ S 1.35；trade_when(正修正) ⇒ S 1.05（虽 2Y 1.89）。 ⑨ surprise(SUE)/trend_slope/zscore/trailing_4q 族 S ≤0.88 全灭。 ⇒ ★ **EUR analyst 类别 = prod 墙内的结构性穷尽；要凑 RA 腿必须离开 analyst 原语族**（换类别或跨区复用已验证结构）。
- **说明**：★★★★★ 【EUR × analyst 换腿降 prod 专项：五级全试，全面封死】（2026-10-17，波 580–582） **问题**：'0mj9nM36'（IS 全闸过）prod 0.9920（与 PPA 的 786pLKnb 互相关 0.994）——换腿能否降 prod？ **答案：不能。五级换腿实测**： ① **参数级**（幂次 6.0 / INDUSTRY 中性化档 / lambda_max=0.5）：互相关地板 **0.92–0.94**（幂次6 = 0.9362、INDUSTRY = 0.9349），prod 地板 **0.9231** ⇒ 离 0.7 差 0.22，无接近者。 ② **输入级**（change_3mo/q1/revenue/netprofit 包 cv 分母，6 变体）：S 全塌 **0.74–1.13** ⇒ **「修正÷分歧度」的强度是 'eps_revision_magnitude' 字段特有**（Street revision 缩放构造），非结构通用。 ③ **门控级**（trade_when 跨度量门控 ×6）：S 全塌 **0.49–1.50** ⇒ 信号强度需全暴露。 ④ **universe 级**（TOP1200/TOP800）：S **0.57–0.82** ⇒ analyst 覆盖集中于大市值，小宇宙丢覆盖。 ⑤ **decay 级**（decay 4）：S 1.58/1.59 但 **F 0.97** 差 0.03；且同序 ⇒ prod 仍 ~0.99。 ⇒ ★★★★★ **根论「强度-占用」锁死**：prod 0.99 与 S 1.75 **同源**（同为该原语在 TOPCS1600 上的排序之结果）。保序变换保强度但保高相关；改序变换降相关但丢强度。⇒ **换腿不能降 prod；要出 RA 腿必须换原语/换数据集/换区域**。 ★ **附带最优发现**：winner 原语 @ **INDUSTRY** 中性化（'LL56W0Q9'）= S 1.78/F 1.17/**2Y 1.89**/robust 1.23/failed_ra=0 —— **全场最优 IS 配置**；区域 settings 的 SUBINDUSTRY 并非该原语最优档（**历史从未扫过 neutralization 设置档，只扫过 group_rank 轴**）。prod 0.9231 仍同腿，但 prod 墙松解时优先提交此版。
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
- **禁止**（全局锁定）：禁止两条独立信号腿相加：加权（0.4×A + 0.6×B）、等权 add(rank(A), rank(B))、中缀 + 都算；第二个数据集只以条件（trade_when / if_else）、分组（group_rank / bucket）或残差（ts_regression / group_neutralize）入场（原举例 regression_neut / vector_neut 均已被平台移除，2026-10-10 op-lint 实测）
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

- 资格判定：`$WQ_PY tools/mode_b_qualify.py evaluate --region EUR --sharpe <S> --fitness <F> --two-year-sharpe <2Y>`（喂全指标，旁路 A–E 才会生效）
- 提交链：`submit_verdict` 只否决；prod 与 self 双端点实测（`check_correlation(refresh=True)`）；用户明确确认后才 `workflow_submit_alpha(confirm_submit=True)`——见 `worldquant-submit-alpha`

### 判死记录（不要重试；「归属」= payload 绑定 / 由条目名推断 / 关键词推断）

| 条目 | 族 | 下次怎么办 / 说明 | 数据集 | 归属 |
|---|---|---|---|---|
| EUR-ANALYST-FACTOR-SIGNALS-WEAK | analyst_factor_signals 分析师因子信号族（EPS/revenue revision magnitu | wave243 9 探针全灭 best ／sharpe／=0.31 → 达 fast_kill 判死线。ANALYST 塔候选出局。今日 7 集回测探针全灭（max／S／ 0.16-0.91），与 2026-09-22 零竞争轴证伪结论互证 | analyst_factor_signals | inferred | <!-- lint:const-ok 证据原文 -->
| EUR-ANALYST10-PREDICTED-SURPRISE-DEAD | analyst10 performance-weighted estimates (predicted surprise | EUR analyst tower: predicted-surprise family closed | analyst10 | payload | <!-- lint:const-ok 证据原文 -->
| EUR-ANALYST9-COLD-ZERO-YIELD | 一致预期修正标准化劾量 / 预期陈旧度 / 修正广度 | 本区该集不再投槽位；同机制（一致预期修正）在其他 analyst 集要进先跑 1-2 条 prod-first + 强度探针 | analyst9 | payload | <!-- lint:const-ok 证据原文 -->
| EUR-ANL11-ESG-SLOWVAR-LONGCOUNT | analyst11 ESG 评分体系（三支柱 + 行业排名 + 改善动量） | Leave analyst11（ESG）在 EUR。analyst 塔（1.3x）完全 exhausted：analyst_consensus（CW=0.5 全灭）+ analyst45 + analyst11（longCount 3-52 | analyst11 | payload | <!-- lint:const-ok 证据原文 -->
| EUR-ANL39-EPS-GM-BOOK-WEAK | analyst39 EPS/margin/book residual x v_rev/wedge | Do not reuse analyst39 EPS/margin/book residuals as 0.30 slow legs with v_rev/falling_wedge. | analyst39 | inferred | <!-- lint:const-ok 证据原文 -->
| EUR-ANL45-TRADE-IDEAS-WEAK | analyst45 VECTOR trade-idea residual x v_rev/wedge | Do not reuse analyst45 trade-idea vec_avg residuals as 0.30 slow legs with v_rev/falling_wedge. | analyst45 | inferred | <!-- lint:const-ok 证据原文 -->
| EUR-CONSENSUS-SURPRISE-TP-WEAK | analyst_consensus surprise/estimate/target x v_rev/wedge | Do not reuse analyst_consensus surprise/target residuals as 0.30 slow legs with v_rev/falling_wedge. Prefer GEM concept  | analyst_consensus | inferred | <!-- lint:const-ok 证据原文 -->
| EUR-analyst45-RET-WEAK | analyst45 return/benchmark fields | Leave analyst45 return/benchmark fields in EUR. Do not retry ts_mean/ts_delta/ts_decay_linear on anl45_*_ret fields or i | analyst45 | payload | <!-- lint:const-ok 证据原文 -->
<!-- profiles:cell-panel:end -->

## 补充说明（手写）

<!-- profiles:manual:start -->
<!-- profiles:manual:end -->
