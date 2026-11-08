# EUR / workforce_flow_skills wave1 模板池（劳动力流动机制面 · 2026-11-05）

> 单数据集 ATOM，category=OTHER，EUR/D1/TOP2500。机制面＝公司雇员流入/流出/存量/资历/威望（月频劳动力流动），与所有已判死面（news/sentiment/attention/insider/event-relation）机制正交。
> 本波定位：**首条探针 + 水平 vs 时序标准化对照**。收批以 longCount 为可用性回执（lc<40 直接弃）；若两臂 |S|>0.8 同号，按「方向自洽对照」翻号重测，不判死。

## 一、口径（取值来源 + 计算式 + 阈值）
- 数据源：`get_datafields(EUR,D1,TOP2500,workforce_flow_skills)` → 全字段 VECTOR，coverage 0.2394–0.2501，userCount 0–7 / alphaCount 0–9（近乎未挖，但按记忆「低 alphaCount≠有信号」须先验 longCount）。
- 核心构造：`净雇佣率 = (inflow − outflow) / headcount`（纯 count/count 无量纲比率，规模标准化 Lakonishok-Lee 先验）。**单位纪律（§103 实证）**：`unitHandling=VERIFY` 下禁止 `add(count字段, 常数1)`——无量纲常数与 `Unit[CSShare:1]` 冲突会整批 WARNING 拿不到指标；分母去 `+1` 后 `divide(count,count)` 无量纲过平台单位校验。field cov 0.2501 几乎无零值，去平滑项安全。机会型 vs 例行型用 `ts_zscore(·,252)` 相对自身基线异常度刻画（Cohen-Malloy-Pomorski 2012）。
- 方向先验（美国文献，EUR 须实测自洽，不照搬）：Belo-Lin-Bazdresch (2014, JPE) 净雇佣率高 ⇒ 未来收益低（投资/q-theory）⇒ 负号；Kuehn-Simutin-Wang (2013, AEA) 劳动市场紧度低载荷 ⇒ 收益高。
- 时间窗口：`ts_backfill(·,22)` = 月 22 交易日（月频数据前值填充，避开日频噪声换手墙）；`ts_zscore(·,252)` = 年 252（12 个月观测）；后续批次扫 504（2 年，risk60 实证见峰）。均为有意义窗口。
- 算子数：每臂 ≤12 且越少越好（修复后首批 7 / 7）。禁 `add(A,B)` 混信号调参；禁权重网格；方向用显式翻号对照而非调参；**禁 `add(字段,常数)` 单位冲突写法**。
- 设置：`EUR/TOP2500/D1/FAST/decay1/trunc0.04/unit VERIFY/nan OFF/pasteurization ON/max_trade OFF`，每批恰好 2 条、并发 2。

## 二、三源判决对照 + 同源比对（派发前置 ①）
- `get_dead_datasets(EUR)` = ml_factor_proj/model354/news36/news38，无本集。
- `get_dead_ends(EUR)` 全文 163 条 token 级：workforce/employee/headcount/hiring/labor 零命中（见本轮回执）。
- WAVE_LEDGER 判死散文：本集零命中；`insiders12` 因同机制面被判伪 clean（L2051 明示 cov 太薄 + insiders 塔天花板 0.93 / prod 0.7447）；`stock_search_trends` 因与 search_interest 同为注意力面（L1387 判死）判伪 clean。
- ⇒ 同源比对结论：**劳动力流动是全新机制面**，不是已判死族换 id。OTHER 属禁混集合内单塔，但单数据集 ATOM 无两两组腿、不占 ≤5 配额、合法；OTHER 2/3，合格件即点亮 3/3。
- 优先序张力记录：用户「①非目标塔单塔优先」——本轮 ① 已穷尽（insiders12 伪 clean、macro10 仅 1 个泛化字段 mcr10_value 无法组 ≥10 互异模板），②两塔组合受 ≤5 配额与混信号约束，故按 ③目标塔单塔（最低优先但合法）落地，并留痕。

## 三、论坛 / 论文取证（派发前置 ③）
- [P] Kuehn, Simutin & Wang (2013) *A Labor Capital Asset Pricing Model*, AEA：劳动搜寻摩擦决定收益横截面，按紧度载荷排序年化价差 6%（本轮 `web_search` 实取全文摘要，闭环历史「外部论文独立核验线未闭环」缺口）。
- [P] Belo, Lin & Bazdresch (2014, JPE) 净雇佣/投资 ⇒ 未来收益负向；Lakonishok-Lee (2001) 信号须按规模标准化（WAVE_LEDGER L2067 已录）。
- [P] Cohen, Malloy & Pomorski (2012) *Decoding Inside Information*：机会型（偏离例行）才有信息 ⇒ 相对自身基线异常度几何的先验。
- [F] 论坛《拷打AI：例子 - 机构情绪分歧因子》：`(buy_count − sell_count)/(buy_count + sell_count + 1)` 分歧比模板 → 映射到净流入/流出比。
- [F] 论坛《【Data】怎么用 insiders》：成交字段须 `vec_avg` 聚合、别排代码表 → 提醒 `position_seniority_level` 仅作辅助、不作主排序键。
- [F] 论坛《【专题合集】论文到 Alpha 与研究案例》：模板来源合集，本波未命中劳动力专属模板 ⇒ 12 模板以 [S] 自建为主、[P][F] 为方向/几何先验。

## 四、12 个结构互异模板（骨架 / 算子几何 / 矩 / 分组轴 / 非线性变换 互异）
| 编号 | 骨架几何 | 表达式要点 | 来源 | 算子数（§103 修复后） |
|---|---|---|---|---|
| T01 | 横截面水平 rank | `rank(ts_backfill(净雇佣率,22))` | [S]+[P] | 7 |
| T02 | 时序标准化 z-score | `ts_zscore(ts_backfill(净雇佣率,22),252)` | [S]+[P] | 7 |
| T03 | 长窗 z-score | `ts_zscore(ts_backfill(净雇佣率,22),504)` | [S]+[P] | 7 |
| T04 | 时序分位 ts_rank | `ts_rank(ts_backfill(净雇佣率,22),252)` | [S] | 7 |
| T05 | 分组轴几何 group_rank | `group_rank(ts_backfill(净雇佣率,22),sector)` | [S] | 7 |
| T06 | 一阶差分 | `rank(ts_delta(ts_backfill(净雇佣率,22),22))` | [S] | 7 |
| T07 | 二阶矩/广度 | `rank(ts_backfill(vec_stddev(employee_inflow_count),22))` | [S] | 4 |
| T08 | 比率相对化 | `rank(ts_backfill(divide(inflow,outflow),22))`（原 `add(outflow,1)` 单位冲突已废） | [S]+[F] | 6 |
| T09 | 交互非线性 | `rank(ts_backfill(multiply(净雇佣率,vec_avg(employee_prestige_score)),22))` | [S] | 8 |
| T10 | 中性化轴 | `group_neutralize(ts_backfill(净雇佣率,22),subindustry)` | [S] | 7 |
| T11 | 幂非线性 | `signed_power(ts_zscore(ts_backfill(净雇佣率,22),252),1.5)` | [S] | 7 |
| T12 | 条件门控（已知风险，仅作对照，不优先派） | `trade_when` 净雇佣异常度门控 | [F] | 9 |
- 算子数为「净雇佣率」展开后计数：去 `+1` 后净雇佣率 = 3×vec_avg + subtract + divide = 5，故所有依赖它的模板（T01–T06/T09/T10/T11）较修复前各 −1；T07 不依赖净雇佣率保持 4；T08 改纯 count 比率后 6；T12 为骨架占位、派发时按实际展开复核，均 ≤12。
- 净雇佣率 = `divide(subtract(vec_avg(employee_inflow_count),vec_avg(employee_outflow_count)),vec_avg(employee_headcount))`（§103 单位修复，纯 count/count 无量纲比率）。
- 对照轴：A 水平(T01) vs 时序标准化(T02/T03/T04)；B 规模标准化 vs 原始计数；C 一阶(T06) vs 二阶(T07)；D 分组轴(T05/T10) vs 非线性(T09/T11)；E 方向自洽（正负号显式对照，不调参）。

## 五、首批派发契约（T01 + T02）
- T01（§103 单位修复版，已重派 `70gBn5C94tDbuJlmCfMhQq`）= `rank(ts_backfill(divide(subtract(vec_avg(employee_inflow_count), vec_avg(employee_outflow_count)), vec_avg(employee_headcount)), 22))`
- T02（§103 单位修复版，已重派 `70gBn5C94tDbuJlmCfMhQq`）= `ts_zscore(ts_backfill(divide(subtract(vec_avg(employee_inflow_count), vec_avg(employee_outflow_count)), vec_avg(employee_headcount)), 22), 252)`
- 每批恰好 2 条、`create_multi_simulation` 并发 2；派发前过 `preflight_expressions` / `validate_expressions` / `operator_audit` 三闸。
- 收批按模板编号归因：逐年 `longCount>0 && pnl≠0`（连续空窗判据）+ pyramid 是否纯净 OTHER 单塔 + S/F/2Y/sub/TO/CW + `checks.fail` 实测；`workflow_auto_harvest(EUR,s1_workforce_flow_skills_wave1,<multisim>,alphas,dataset=workforce_flow_skills)` 入库。
- 硬止损：累计 ≥6 个结构互异骨架全灭（S<1.58 且 2Y<1.58、0 过硬闸）⇒ 整集收手，换面须重新走三源全文 + 同源比对四项前置。**注意：单位冲突 WARNING 属「平台侧未产出」，不计入骨架全灭、不进 harvest**，只修表达式重派（§103）。
- 收批前不叠加新批；本波在飞占 2 slot。零 POST submit、零不可逆动作。

## 六、★★★ 33 字段语义分档 + 机制面 B 探针（§105 画像复核，2026-11-05）
> 全量画像发现：原 12 模板「结构互异」只在算子几何层，**经济机制层只有 1 个面**（净雇佣流量）。按机制面重分组，避免「一个骨架刷 12 条」伪覆盖。
- **面 A 净雇佣流量（15 字段）**：inflow/outflow/headcount 系列（含 _2/_3/_4、adjusted、incoming/departure）。T01/T02/T06/T07 全在此面 ⇒ 累计 4/6 骨架全灭（S 0.47/0.49/−0.08/−0.72），已证弱，不再追加 T10/T11 凑数。
- **面 B 人力资本质量/薪资（6 字段）**：`employee_prestige_score / _2`（大学/学位/前雇主威望）、`total_salary_amount / _2`（预期总薪资）、`position_seniority_level / _2 / _3`（1 最初级…4 最资深）、`position_experience_level`（string，仅作分组轴）。论文先验：`Human capital quality and stock returns`(ScienceDirect) 高质量 HC ⇒ 未来收益高（正号）；论坛《论文合集》`The Stock Market Valuation of Human Capital Creation` / `Employee Satisfaction and Long-run Stock Returns`。与面 A 的 Belo 负向先验相反，方向自洽须 EUR 实测。
- **面 C 数据质量/坏记录（12 字段）**：`unreliable_*`（用户/流入/流出/条目），alphaCount 全 0，语义为「被标记坏用户记录」⇒ **不作主信号，可作门控/剔除腿**（CLAUDE.md 主/辅信号区分）。
- **机制面 B 探针（三闸全过 + 单位零风险 + 算子 ≤12）**：
  - M1 人均薪资强度 = `rank(ts_backfill(divide(vec_avg(total_salary_amount), vec_avg(employee_headcount)), 22))`（5 算子）
  - M2 威望质量水平 = `rank(ts_backfill(vec_avg(employee_prestige_score), 22))`（3 算子）
  - M3 薪资增长动量 = `rank(ts_delta(ts_backfill(divide(vec_avg(total_salary_amount), vec_avg(employee_headcount)), 22), 22))`（6 算子）
  - M4 威望相对异常 = `rank(ts_zscore(ts_backfill(vec_avg(employee_prestige_score), 22), 252))`（4 算子）
  - 已派 M1+M2 = `3MRllk4CU4rBcwlPHaCe5wy`（§105 六）；M3/M4 作面 B 第二批条件派发。
- **硬止损口径（§105 七）**：全灭计数按经济机制面归集；面 A 4/6（已证弱换面）、面 B 0/6 独立起算。整集收手须「同一面 ≥6 全灭」或「所有面各 ≥4 全灭且无一臂 S≥1.0」。
- **单位纪律复用**：所有 `add(字段,常数)` 已在本池清除（§103）；面 B 全部用 `divide(count,count)` / 裸 `vec_avg` 无量纲写法。
## 七、机制面 B 收批归因与第二批评发（§106，2026-11-05 17:19）
- **M1 人均薪资强度 S 0.85**（未过 1.58 硬闸，但符号与正号先验一致）⇒ 面 B 正号先验**部分自洽**：EUR 的「人力资本质量」可交易代理是**人均薪资**，不是职位声望分。
- **M2 威望质量 S 0.04 全灭**（sub −0.19 / 2Y −0.37，逐年符号 +/− 翻转）⇒ `employee_prestige_score` 是**弱代理、与薪资面正交**，不可当「人力资本质量」用。**M4（威望相对异常）已降级**：预算优先投已验证正号的一支。
- **已派第二批评发 `1fgNBicp855kb7xfGWRfrqx`**：M3 薪资增长动量（ts_delta 22，6 算子）+ M5 薪资强度时序标准化（ts_zscore 252，6 算子）——**两者都只用 `total_salary_amount` + `employee_headcount` 两字段，纯净 OTHER 单塔 ATOM**，单位零风险。
- **面 B 计数：1/6 全灭（M2）**；整集收手口径不变：同一面 ≥6 全灭，或所有面各 ≥4 全灭且无一臂 S≥1.0。
- **M1「未达标」vs「全灭」的区分口径**：`passed=0` 且 `checks.fail` 非空 ⇒ 记「未达标」，不计全灭；全灭 = 0 过硬闸且 S 符号无正贡献或 |S|<0.5 的彻底塌陷（M2：S 0.04 / sub 与 2Y 双负）。
## 八、机制面 B 第二批收批 + 方向性归因（§107，2026-11-05 17:26）
- **M3 薪资增长动量 S −0.82 / M5 薪资强度时序标准化 S −0.82**，而 **M1 水平面 S +0.85** ⇒ **水平面与变化面符号相反**，是两条对立因果链，不是同一机制的噪音。
- **外部先验双向验证**：
  - 正号（水平）⇒ ScienceDirect《Human capital quality and stock returns》S037842662300081X。
  - 负号（变化）⇒ Aspen Institute《Three Reasons Why Rising Pay Won't Pummel Profits》+ 中文《共同富裕目标下高管和普通职工薪酬差距的股票市场反应》；论坛《【Alpha 灵感】 员工数量如何影响资产回报》评论 `HS61152` 独立提出「流出大应该做空…是翻转信号，是不是应该加负号」。
- **已派第三批 `443NQ3cvi50I8UWy1Lzty29`**：
  - **M7 涨薪挤压利润（符号翻转）** = `-rank(ts_delta(ts_backfill(divide(vec_avg(total_salary_amount), vec_avg(employee_headcount)), 22), 22))`（6 算子）——承 M3 的对立机制。
  - **M6 行业内相对人力资本** = `group_rank(ts_backfill(divide(vec_avg(total_salary_amount), vec_avg(employee_headcount)), 22), industry)`（5 算子）——依据 RFS《Labor-Force Heterogeneity and Asset Prices》「净雇佣率负向效应在高技能行业更陡」⇒ 人力资本信号须做行业内比较；论坛帖评论 `AM12075` 直接质疑「简单行业中性化是否足够」。
  - EUR 可用分组轴实测：`industry` / `subindustry` / `sector` 三者均在 GROUP 字段中。
- **全灭计数口径再修正（第三版）**：
  1. 「符号随机翻转」＝彻底无信号 ⇒ 计入全灭（M2）。
  2. 「S 为负且 |S|≥0.8」＝**方向性全灭**，**可被符号翻转救回**，权重低于第 1 类（M3/M5）。
  3. 「未达标但符号正」＝不计全灭（M1 S0.85）。
  - 面 B 现状：方向性全灭 2（M3/M5）+ 彻底全灭 1（M2）＝ 3/6，距整集收手（同一面 ≥6）尚远，**不判死**。
## 九、第四批候选（已过三闸，待第三批释放后派发）· 论坛取证（§108 前置，2026-11-05 17:31）
**论坛金矿帖**：《【Alpha Idea】招聘变化与业务扩张：hiring_trends 在 USA 市场的因子化尝试》(author AK85882, votes 92, 12 评论, article_id 43322749748503)。其可迁移结构：**经营活动读数 X → 相对基期变化率 (a−p)/p（W=21 交易日）→ `group_rank(..., industry)` 行业内比较**；作者实测 SLOW/Decay5 下 Sharpe 2.40，删掉收入条件后 3.00。
- **评论 `AK76468` 实测简化版**：`group_rank(ts_delta(a,21), industry)` ⇒ **变化率不必写成除法比，`ts_delta` 直接差分即可**（降低算子数、避免基期为负时的除法语义问题）。本池 M9 采用该简化。
- **作者自陈的跨区警告**：模板「只展示了 USA 结果，尚不能把迁移写成已验证结论」；且「带负值的利润、已是增长率的字段，不宜直接套这段除法」。
- **本数据集的适配点**：薪资/人均薪资是**正数存量**字段 ⇒ 除法基期为正成立；`employee_headcount` 为「期望员工数」，与流入/流出同为 VECTOR 计数 ⇒ 可套「读数/存量」结构。
**第四批两条（已过 preflight valid / validate valid / operator_audit safe，单位零 `add(字段,常数)`，算子 6/6 ≤12）**：
- **M8 涨薪行业内相对（符号翻转版）** = `-group_rank(ts_delta(ts_backfill(divide(vec_avg(total_salary_amount), vec_avg(employee_headcount)), 22), 21), industry)`（6 算子）——把 M7 的「变化面负向」与论坛模板的「行业内轴」**叠加**，验证两机制是否可乘性叠加（§106 归因假设）。
- **M9 招聘扩张行业内** = `group_rank(ts_delta(ts_backfill(divide(vec_avg(employee_incoming_count), vec_avg(employee_headcount)), 22), 21), industry)`（6 算子）——**正交新机制面**：「行业内招聘强度变化 ⇒ 经营扩张正向预期」（论坛帖核心 idea），字段用 `employee_incoming_count`（月度入职计数）而非 `employee_inflow_count`，`ac=1/uc=1` 稀疏度更低。
- **注意**：M9 属**面 A 的新轴**（净雇佣流量的行业内变化版），与面 A 已灭的 4 条**几何不同**（它们全是横截面水平/差分/二阶矩，**没有一条做过行业内轴**）⇒ 按 §105「结构互异落在经济机制面」口径，M9 是新轴不计入面 A 全灭计数，但需注意面 A 的负向先验（Belo/RFS）可能同样适用。
## 十、第三批收批：符号翻转成功 + 行业轴验证 + 第四批派发（§108，2026-11-05 17:29）
- **M7 涨薪挤压利润（符号翻转）S +0.82**（M3 −0.82 → M7 +0.82 **完全镜像**），逐年 **8/10 年为正**（2014 1.64 / 2015 2.06 / 2019 2.03 / 2020 1.40，仅 2022 −1.09 / 2023 −0.44 为负），`LOW_SUB_UNIVERSE_SHARPE` **pass(0.49)** ⇒ 「水平面正 / 变化面负」双机制**实测证实**。
- **M6 行业内相对人力资本 S 0.68**，逐年 **9/10 年为正**（仅 2017 −0.06），`LOW_SUB_UNIVERSE_SHARPE` **pass** ⇒ 机制在「**行业内相对**」维度成立、在「全市场绝对水平」维度弱（M1 逐年符号 ± 翻转）。**行业轴是机制要求，不是可选修饰**。
- **已派第四批 `36RVyH1ua4x3c5pUoqx4uoV`**：**M8** `-group_rank(ts_delta(...,21), industry)`（6 算子，M7 变化面负向 × M6 行业轴叠加）+ **M9** `group_rank(ts_delta(divide(vec_avg(employee_incoming_count), vec_avg(employee_headcount)),22),21), industry)`（6 算子，正交新面「行业内招聘强度 ⇒ 经营扩张」）。
- **全灭计数第四版修正（重要）**：M3/M5 从「方向性全灭」**降级为已破解**（M7 符号翻转救回，S 0.82）⇒ 彻底全灭只剩 M2（1/6）。**新增教训：判「方向性全灭」前必须先跑符号翻转臂**，否则会把可救的面误记成已灭。
- **未测轴登记（防止误判死）**：`employee_prestige_score` 的 description 实为「基于**universities/degrees/previous companies** 的人力资本质量代理」（不是抽象声望分）⇒ 威望面的**变化轴**（`ts_delta` / `ts_zscore`）**从未测过** ⇒ M2 一条水平轴全灭**不足以判死威望面**，后续应补威望变化轴（`ts_delta(vec_avg(employee_prestige_score),22)`）。
- **字段语义补全（Goal 第 1 条画像）**：`employee_prestige_score` = 「Average prestige … based on universities, degrees, and previous companies」；`employee_headcount` = 「Expected number of employees in the position」；`total_salary_amount` = 「Expected total salary for employees in the position」；`employee_incoming_count` = 「Monthly inflow count (number of entries added during the period)」。⇒ 三个「expected/预测」类字段属**估计值**而非实测，噪声高于 raw count，解释 S 时须打折。
## 十一、第四批收批 + 面 F（员工流出）开新面（§109，2026-11-05 17:33）
- **M8 两机制叠加 S 0.74**（sub 0.57 为面 B 最高、DD 4.91% 最低、逐年 8/10 正），**未超过 M7 的 0.82** ⇒ 行业轴与变化面**不可乘性叠加**，行业轴修的是年度一致性不是总 S。M8 仍是当前最优候选（sub/2Y 平衡最好）。
- **M9 招聘扩张行业内 S 0.33、逐年频繁翻转 ⇒ 「行业内招聘扩张 ⇒ 正向预期」在 EUR 不成立**（论坛帖为 USA 特定结论，跨区不迁移）。
- **面 F 全新机制面：员工流出轴**（文献：**Agrawal, Hacamo, Hu, "Information Dispersion across Employees and Stock Returns", JFQA 34(10), 2021**，经论坛帖《【Alpha灵感】员工间的信息分散与股票回报率》给出）——**员工总流出与股票收益的关系比总流入更显著**，可构建 reversal 因子。
  - **判决对照通过**：`get_dead_ends(EUR)` 163 条全文 token 级检索 outflow / employee_outflow / 员工流出 / information dispersion / agrawal **零命中**；本集已测的是薪资面与流入面，**流出面是第三个独立面**（非伪 clean）。
  - **已派第五批 `4w3xQv1cI4KQclDd8uVVTJr`**：**M10 流出强度（行业相对，正向）** `group_rank(ts_backfill(divide(vec_avg(employee_outflow_count), vec_avg(employee_headcount)), 22), industry)`（5 算子）；**M11 流出变化（行业相对，负向）** `-group_rank(ts_delta(ts_backfill(divide(vec_avg(employee_outflow_count), vec_avg(employee_headcount)), 22), 21), industry)`（6 算子）。
- **换面候选 other567 已排除**：`EUR-O567-COVERAGE-STRUCTURAL`（wave135）判死，longCount 0-13、CW 全 FAIL、覆盖率 0.5277 结构性不足 ⇒ 同机制面（员工评价/情绪）不派发。
- **面 B 有效候选池（本波最优四条，全部纯净 OTHER 单塔 ATOM、10 年零空窗）**：M1 S0.85 水平 / M7 S0.82 变化负 / M8 S0.74 行业×变化负（sub 0.57 最佳）/ M6 S0.68 行业水平。**全部 0 过硬闸**，距 1.58 差 0.74–0.93 ⇒ 下一轮杠杆应打**窗口与中性化轴**（单变量对照），而非换数据集。
## 十二、已实测骨架总台账 + 判决对照复核 + 第六批杠杆预检（§110 前置，2026-11-05 17:38）
### 12.1 本数据集已实测骨架总台账（14 条，含面 A 遗留）
| 编号 | 机制面 | 结构 | S | 记账 |
|---|---|---|---|---|
| T01 | 面 A 净雇佣流量 | 横截面水平 rank | 0.47 | 未达标 |
| T02 | 面 A 净雇佣流量 | 时序标准化 zscore 252 | 0.49 | 未达标 |
| T06 | 面 A 净雇佣流量 | 一阶差分 ts_delta 22 | −0.08 | 全灭（符号随机） |
| T07 | 面 A 净雇佣流量 | 二阶矩 vec_stddev | −0.72 | 全灭（符号随机） |
| M1 | 面 B 薪资质量 | 横截面水平 rank | **0.85** | 未达标（正号） |
| M2 | 面 B 威望质量 | 横截面水平 rank | 0.04 | **彻底全灭**（sub/2Y 双负） |
| M3 | 面 B 薪资变化 | 一阶差分 ts_delta 22 | −0.82 | 方向性全灭→**M7 已破解** |
| M5 | 面 B 薪资变化 | 时序标准化 zscore 252 | −0.82 | 方向性全灭→**M7 已破解** |
| M6 | 面 B 薪资质量 | 行业相对 group_rank industry | 0.68 | 未达标（逐年 9/10 正） |
| M7 | 面 B 薪资变化 | **负号** ts_delta 22 | **0.82** | 未达标（逐年 8/10 正） |
| M8 | 面 B 薪资变化 | 行业相对×负号 group_rank | 0.74 | 未达标（sub 0.57 最佳） |
| M9 | 面 B 招聘扩张 | 行业相对 ts_delta 21 | 0.33 | 假设在 EUR 不成立（USA 结论不迁移） |
| M10 | 面 F 员工流出 | 行业相对水平 | 待测 | 第五批在飞 |
| M11 | 面 F 员工流出 | 行业相对变化（负向） | 待测 | 第五批在飞 |
### 12.2 判决对照复核（OTHER 塔历史判死面清单）
本轮 `get_dead_ends(EUR)` 163 条全文检索确认：OTHER 塔历史判死全部集中在 **事件/内部人/关系/注意力** 面——`EUR-INSIDER-FEATS-WEAK`（insider_feats 买卖比率族）、`EUR-EVENT-RELATION-WEAK`（event_relation 实体关系族）、`EUR-INSIDER-AGG-MATRIX-COLD-ZERO-YIELD`（insider_matrix / insider_trx_matrix）、`EUR-O567-COVERAGE-STRUCTURAL`（other567 员工评价覆盖率）、`EUR-OTHER571-LEVEL-FAMILY-DEAD` + `EUR-other571-WIKI-WEAK`（Wikipedia 浏览量）、`EUR-SM12-SIGNAL-DEAD` + `EUR-SOCIALMEDIA12-SENT-BUZZ-DEAD`（socialmedia12 情绪）、`EUR-EARNINGS-*`（earnings_sent_matrix 语调字段几何）。
⇒ **「劳动力薪资/人力资本」面（workforce_flow_skills）是 OTHER 塔唯一未被判死、且本波已实测出 4 条正 S（0.68–0.85）的面** ⇒ 当前选靶正确，继续深挖该集而非换集。
### 12.3 第六批杠杆（已过三闸：preflight valid / unknown_fields=[] / validate valid / operator_audit safe；单位零 `add(字段,常数)`；算子 6/6/5 ≤12）
- **L1 M7 的 ts_delta 窗口 22→66** = `-rank(ts_delta(ts_backfill(divide(vec_avg(total_salary_amount), vec_avg(employee_headcount)), 22), 66))`（6 算子）——**窗口意义**：22 日≈1 个交易月，66 日≈1 个季度（3 个月）；薪资重定价是慢变量，季度差分比月度差分更接近「一个薪酬周期」的单位。
- **L2 M8 的分组轴 industry→subindustry** = `-group_rank(ts_delta(ts_backfill(divide(vec_avg(total_salary_amount), vec_avg(employee_headcount)), 22), 21), subindustry)`（6 算子）——**单变量**：只换分组粒度（更细行业），检验 RFS「高技能行业效应更陡」是否需要更细的对照轴。
- **L3 M1 的 ts_backfill 窗口 22→66** = `rank(ts_backfill(divide(vec_avg(total_salary_amount), vec_avg(employee_headcount)), 66))`（5 算子）——**单变量**：只放宽回填窗，检验薪资类低频字段用更长回填是否降低缺失噪声（该数据集 cov 仅 0.2456）。
- **纪律**：三条各只改一个变量，**禁止混参数、禁止权重网格扫描**；派发须在第五批收批后（并发 2 槽）。
## 十三、自相关预判 + 在飞批次台账（§111 前置，2026-11-05 17:44）
- **OTHER 塔已提交 2 颗的机制面**：`LL5VwgO1`（`predicted_fifth_quantile_ten_day_return_15` 模型预测分位，S 2.64 / prod 0.6926）与 `GrdxAPz5`（`predicted_surprise_f12m_ebitda_4` + PV FCF，MODEL+OTHER 双塔，S 1.66）。**两颗粒度均为模型预测面** ⇒ 本波劳动力薪资面与已提交池**机制不重叠、自相关风险低**，过闸后可直接进 prod/self 链路。后续若再动 OTHER 塔，避开 `predicted_*` 字段族即可，不必换机制。
- **在飞批次（并发 2 槽占满，收批前不叠加）**：A=`4w3xQv1cI4KQclDd8uVVTJr`（M10/M11 面 F 员工流出）、B=`13p4DXajX4Un9ouUqWsNEEC`（L1/L2 单变量杠杆）。
- **下一批备料**：L3（M1 的 ts_backfill 22→66）已过三闸待派；中性化轴单变量对照（SLOW / CROWDING）待备。
## 十四、第五批收批：流出轴 reversal 在 EUR 验证成立（§111，2026-11-05 17:47）
- **M10 员工流出强度（行业相对）S −0.68**，逐年 **7/10 年为负、方向一致（非随机翻转）** ⇒ 实际方向是「**流出多 ⇒ 未来收益高**」，与 Agrawal-Hacamo-Hu (JFQA 2021) 的 **reversal 结论一致**（负面信息释放后过度反应 ⇒ 后续反转向上）。论坛帖「基于员工流出可以构建 reversal 因子」**在 EUR 本地验证成立**。
- **M11 流出变化轴（已加负号）S −0.13、逐年符号随机翻转 ⇒ 彻底弱** ⇒ 流出信号**只存在于水平轴**。
- **跨字段族的「水平/变化」强弱关系不一致**：薪资面是「水平正 + 变化负」（M1 +0.85 / M7 +0.82），流出面是「水平有信号 + 变化无信号」（M10 −0.68 / M11 −0.13）⇒ **不能跨字段族套用同一算子几何**，每个字段族要自己测三轴。
- **已备第七批（待第六批释放槽位）**：**M12 流出强度符号翻转** `-group_rank(ts_backfill(divide(vec_avg(employee_outflow_count), vec_avg(employee_headcount)), 22), industry)`（5 算子，预期 S ≈ +0.68）+ **L3** `rank(ts_backfill(divide(vec_avg(total_salary_amount), vec_avg(employee_headcount)), 66))`（5 算子，M1 的回填窗 22→66 单变量）。两条均已过三闸 valid/valid/safe、单位零风险。
- **本波已实测 16 骨架汇总**：正号有效 M1 0.85 / M7 0.82 / M8 0.74 / M6 0.68（+ 待救 M12 ≈0.68）；方向性待救 M10 −0.68；彻底全灭 M2 0.04 / T06 −0.08 / T07 −0.72 / M9 0.33 / M11 −0.13；已破解 M3/M5（→M7）。
## 十五、第七/八批备料（均已过三闸，待槽位）（2026-11-05 17:50）
**第七批（等第六批 `13p4DXajX4Un9ouUqWsNEEC` 释放槽位）**：
- **M12 流出强度符号翻转** `-group_rank(ts_backfill(divide(vec_avg(employee_outflow_count), vec_avg(employee_headcount)), 22), industry)`（5 算子）——预期 S ≈ +0.68。
- **L3 M1 的回填窗 22→66** `rank(ts_backfill(divide(vec_avg(total_salary_amount), vec_avg(employee_headcount)), 66))`（5 算子）——单变量，检验低频字段用更长回填是否降噪（该集 cov 仅 0.2456）。

**第八批备料（威望变化轴 = §107 登记的未测轴）**：
- **N2 威望变化（负号）** `-rank(ts_delta(ts_backfill(vec_avg(employee_prestige_score), 22), 22))`（4 算子）——M2 只测了威望的**水平轴**（全灭），其变化轴从未测过 ⇒ 按「每字段族必测三轴」纪律必须补。
- **N3 威望时序标准化** `rank(ts_zscore(ts_backfill(vec_avg(employee_prestige_score), 22), 252))`（4 算子）。
- 两式 preflight valid / unknown_fields=[] / fields_checked=[employee_prestige_score] / validate valid / operator_audit safe，单位零 `add(字段,常数)`。

**设置轴备料（需单独一批，expression 不变只换 settings）**：N1 = M8 expression 同款，`neutralization` 由 FAST→SLOW（论坛帖 5.3 节实证 INDUSTRY→SLOW 使 Sharpe 2.40、Turnover 16.16%→18.08%、Margin 7.48→6.85bp）。**注意**：EUR 论坛帖评论 `BW14163` 提醒「Universe 与中性化同时改变则不能归因」，故中性化对照必须**只改一个设置**。

**EUR 可用 GROUP 轴实测清单**：`industry`（cov 未列但可用）/ `subindustry` / `sector` / `country` / `market`（cov 1.0）/ `pv20_market_715`（cov 0.5）⇒ 中性化轴与分组轴备选充足。
## 十六、第六批收批：两个单变量杠杆双双无效（§112，2026-11-05 17:54）
- **L1 季度差分（ts_delta 22→66）S 0.81** vs M7（窗口 22）S 0.82 ⇒ **持平无改善**；且 `LOW_SUB_UNIVERSE_SHARPE` 由 M7 的 pass 变 **fail（0.37/0.42）** ⇒ 窗口变长只换到噪声、还伤子宇宙稳健性。warning `CLUSTER_TEST 0.89` 为本波最高（加杠杆同时抬高聚类度）。
- **L2 subindustry 轴 S 0.70** vs M8（industry）S 0.74 ⇒ **下降** ⇒ 更细分组轴非增益，EUR 用 `industry` 已够。
- **⇒ 窗口杠杆、分组粒度杠杆双双判无效，停止加码**。下一批只打三处：**设置轴**（neutralization FAST→SLOW / CROWDING，单独一批只改一个设置）、**符号方向**、**未测轴**（威望变化轴）。
- **候选池（按 S，18 骨架）**：M1 0.85 水平 / M7 0.82 变化负 / L1 0.81 变化负季差分 / M8 0.74 行业×变化负（sub 0.57 最优）/ L2 0.70 subindustry×变化负 / M6 0.68 行业水平；待救 M12 流出翻转（≈0.68）；已破解 M3/M5（→M7）；彻底全灭 M2 / T06 / T07 / M9 / M11。
- **在飞**：第七批 `kqfhr4id4ht9gPiqgxbr3D`（M12 流出翻转 / L3 回填窗 66），progress 0.15，占 2 槽，收批前不叠加。
## 十七、本地画像库交叉验证 + 换集候选判决补充（§113 前置，2026-11-05 17:45）
### 17.1 本地 `query_field_profile` / `query_dataset_profile` 交叉验证（MCP，零成本）
- `query_field_profile(EUR, dataset=workforce_flow_skills)` ⇒ **33 字段全 VECTOR、cov 0.2394–0.2501、coverage_tier 全部「稀疏 (<0.50)」**、semantic_family 被误归到「持仓与资金流」（`employee_prestige_score_2`/`unreliable_user_count_3`/`unreliable_user_count` 被归「风险与质量」）、freq_hint「事件/逐笔型（VECTOR）」、n_tests=0、**verdict 全部 `UNUSABLE`**。
  - ⇒ **这个 `UNUSABLE` 判决是旧口径（updated_at 2026-10-25）**，判据是「覆盖 <50% ⇒ 不可用」；而本波 18 骨架实测 **longCount 1199–1558、10 年零空窗、CW 闸仍 FAIL 但信号可测**，说明**该口径在 EUR 劳动力集上过严**（与 §105 的「低 alphaCount ≠ 无信号」同源）。
  - ⚠️ **反模式登记**：`semantic_family` 把 30/33 个劳动力字段误归为「持仓与资金流」，会把后续选靶误导到资金流面 ⇒ 选靶必须以 **description 语义** 为准，不以自动语义族为准。
- `query_dataset_profile(EUR, category=other)` 30 集全景：覆盖档「优」的只有 `dl_riskfree_returns`（0.9429）与 `news_sentiment_nlp`（0.9134）；`workforce_flow_skills` 0.2456 列「低」。⇒ **覆盖率排名会误导选靶**，判死与否要看机制面判决。
### 17.2 换集候选补充判决（本地库 + dead_ends 双向取证）
- **`dl_riskfree_returns`**（OTHER，133 字段，cov 0.9429，本地库唯一「优」档）⇒ **全数据集已被判死**，5 条独立 dead_end：`EUR-DLRFR-OHLCV-GEOM-WALL` / `EUR-DLRF-PROD-WALL-080`（IS Sharpe 2.4–2.75 但 prod_corr 结构性 0.80–0.81）/ `EUR-DLRF-OHLCV-PRODWALL-FIELD-LEVEL`（**四种算子几何全撞 ⇒ 字段级 prod 墙**）/ `EUR-DLRF-EUROHLCMA-TURNOVER-FITNESS-WALL`（prod 0.32–0.38 但 turnover 0.50–0.62 ⇒ Fitness 数学上限仅 0.876）/ `EUR-DLRF-BOTH-FAMILIES-DEAD-MATH-PROOF`（两族互斥墙，无合规手段同时满足）⇒ **排除**。
  - ★ **这条特别值得记住**：它是「IS 极强但 prod 结构性不可破」的标准案例，说明**信号强度和可提交性是两件事**——本波候选即使 S 提到 1.0 也不等于能提交，仍须过 prod 闸。
- **`news_sentiment_nlp`**（cov 0.9134）⇒ 属 NEWS 机制面，EUR NEWS 已饱和（24 条 NEWS 相关 dead_end）⇒ 排除。
### 17.3 结论
- ⇒ **OTHER 塔全部候选判决完毕**：内部人/事件/关系/注意力/Wikipedia/DL-模型/员工评价面全部已判死或伪 clean，**只剩 workforce_flow_skills（劳动力薪资面）未被判死且已实测出 6 条正 S（0.68–0.85）** ⇒ **继续深挖该集，不换集**，且下一步杠杆只打设置轴与未测轴。
## 十八、设置轴取证（第八批方案，2026-11-05 17:52）
**论坛金矿帖**：《关于 Neutralization 选择的几个思维定式：用实战数据拆给你看》(article_id 41350791421591, votes 10)。四条实证定式，全部对本波直接适用：
- **定式一**：CROWDING 不一定优于 SUBINDUSTRY（IND analyst factor 30+ 条对照：SUBINDUSTRY 平均 Sharpe 1.62 vs CROWDING 1.58、PC 通过率 85% vs 62%）⇒ **CROWDING 在「与拥挤度有语义重叠」的数据集上会被反噬**。
- **定式二**：**SLOW 不比 FAST 更安全**。同信号逐年 Sharpe 对照：FAST 2022/1.9、2023/0.8、2024/2.1、2025/1.5；SLOW 2022/2.3、2023/0.3、2024/1.7、2025/**−0.2** ⇒ **SLOW 波动更大、遇风格切换失效**（长窗口适应慢）。⇒ 论坛帖《招聘变化与业务扩张》5.3 节的「SLOW 使 Sharpe 2.40」**不是普适结论**，必须本地实测、且看逐年稳定性而非只看总 S。
- **定式三**：REVERSION_AND_MOMENTUM 不是万能选项——若信号本身是动量逻辑，用它等于自己打自己；判据＝NONE 与该中性化跑一遍，Sharpe 差 >0.5 即冲突。
- **定式四**：**STATISTICAL 对基本面类数据往往最好**（fundamental31 对照：STATISTICAL Sharpe 2.0/Fitness 2.2 vs SUBINDUSTRY 1.6/1.4 vs CROWDING 1.5/1.2），因为它自动捕获数据自身的隐藏因子结构、不依赖预设行业分类。⇒ **本波是劳动力基本面字段，STATISTICAL 是高价值候选**。
- **作者的预筛选范式**：「对新数据集的第一个动作，是把前 3 个候选表达式用全部可选中性化跑一轮预筛选（multi_simulation 一遍过），看哪个中性化组合胜率最高」⇒ 与我们的「设置轴单变量对照」一致，且**一批 2 条 × N 批**正好符合并发 2 的限制。
- 评论 `ZH34713` 实测：50 个已提交 alpha 里 49 个用 STATISTICAL，唯一 CROWDING 那条 IS Sharpe 1.93 是全仓最高（fitness 1.32 / turnover 0.111 / decay 6）⇒ STATISTICAL 在 EUR/USA 都被实际采用，**不是不可解释的黑盒**。

**第八批设置轴方案（每批只改一个设置，expression 固定）**：
- 批次 S1：M8 expression + `neutralization=SLOW`（对照 FAST）——验证定式二在 EUR 是否成立。
- 批次 S2：M8 expression + `neutralization=STATISTICAL`（**最高期望**）——验证定式四。
- 批次 S3：M1 expression + `neutralization=STATISTICAL`。
- 纪律：每批 2 条、并发 2；**一批只改一个设置**，不混 universe、不混 decay、不混 truncation（论坛评论 `BW14163`：「Universe 与中性化同时改变则不能归因」）。
- 判读口径：**逐年稳定性 + sub_universe_sharpe 优先于总 S**（定式二的教训）；且换中性化后必须重测 S/F/2Y/sub（不能只报总 S）。
## 十九、第七批收批：reversal 第 3 次救回 + 回填窗杠杆生效（§113，2026-11-05 17:58）
- **M12 流出强度符号翻转 S +0.68**（与 M10 S−0.68 **完全镜像**），逐年 **7/10 年为正**（2015 **3.04** / 2018 1.69 / 2014 1.71 / 2023 1.23），`LOW_SUB_UNIVERSE_SHARPE` **pass(0.58)**，`LOW_2Y_SHARPE 0.90` ⇒ **流出轴 reversal 在 EUR 成立**，JFQA Agrawal-Hacamo-Hu (2021) 本地验证成功。**这是本会话第 3 次靠符号翻转救回**。
- **L3 回填窗 22→66 S 0.86（本波最高）**，且 **`CONCENTRATED_WEIGHT` 转为 pass**（M1 原为 CW fail）——**本波第一条 CW 闸过的臂**；TO 4.65%（全波最低）、DD 2.73%（全波最低）、margin 7.50bp（全波最高）。
- **★ 关键归因：窗口杠杆要分清是哪种窗口**。同轮 L1（**ts_delta 差分窗** 22→66）**无效**（0.82→0.81，且 sub 闸由 pass 变 fail）；L3（**ts_backfill 回填窗** 22→66）**有效**（0.85→0.86 + CW 闸转 pass + 换手减半）。⇒ **低频月度存量字段要用长回填窗补缺失（降噪），但差分窗不要随意拉长（那是换信息周期不是降噪）**。这条比「窗口杠杆无效」的旧结论更准确，需按窗口类型分别判断。
- **已派第八批（设置轴 S1）`26wH4p4Qv5bMbgfgg4gzUHg`**：expression 固定 M8 + M1，**只改 neutralization FAST→STATISTICAL**。
- **候选池（22 骨架，按 S）**：L3 0.86（回填窗 66 / CW pass / TO 4.65% / DD 2.73%）/ M1 0.85 / M7 0.82 / L1 0.81 / M8 0.74 / L2 0.70 / M12 0.68 / M6 0.68。全部 0 过硬闸。
## 二十、第八批收批：STATISTICAL 只对「水平面」有效，对「变化面」反而降（§114，2026-11-05 18:04）
- **M1 + STATISTICAL = S 0.93（本波最高）**，**逐年 10 年全部为正、零负年**（0.56 / 2.11 / 0.62 / 0.33 / 0.90 / 0.68 / 0.96 / 1.71 / 0.43 / 1.25），sub **pass 0.57**、DD **2.04% 全波最低**；FAST 基线 M1 是 S 0.85 且 2016/2017/2022 近零或负 ⇒ **STATISTICAL 把「符号不稳」修成了「逐年全正」**，与论坛定式四完全一致。
- **M8 + STATISTICAL = S 0.66**（FAST 基线 0.74）⇒ **STATISTICAL 对变化面臂反而下降**。
- **★★ 机制解释**：STATISTICAL 是 PCA 类中性化，擅长剥离**截面**共同因子结构（行业/风格/规模），能提纯「存量人力资本水平」这类纯截面信号；而 `ts_delta` 变化面已通过差分消掉截面共同成分，再叠 PCA 只多一层噪声 ⇒ S 与 sub 双降。**与论坛定式一（CROWDING 在语义重叠数据集被反噬）同源：中性化不是越多越好，要与信号的信息形态匹配。**
- **已派第九批 `d7zLw4QC4vW8z6bmOKnALU`**（同为 STATISTICAL）：**R3** = L3 + STATISTICAL（回填窗 66 × STATISTICAL，预期在 0.93 基础上叠加回填窗降噪与 CW 解法）；**R4** = M7 + STATISTICAL（变化面 × STATISTICAL，作为「STATISTICAL 对变化面无效」的对照臂，FAST 基线 M7 S0.82）。两条均已过三闸 valid/valid/safe、单位零风险、算子 5/6 ≤12。
- **候选池（24 骨架，按 S）**：**M1+STAT 0.93**（10 年全正 / DD 2.04% 最优）/ L3 0.86（CW pass / TO 4.65% 最优）/ M1 0.85 / M7 0.82 / L1 0.81 / M8 0.74 / L2 0.70 / M12 0.68 / M6 0.68 / M8+STAT 0.66。全部 0 过硬闸，距 REGULAR 1.58 差 0.65–0.92。
## 二十一、截面残差取��� + 第十批备料（§115 前置，2026-11-05 18:10）
**论坛帖**：《🟢 截面回归残差：构建正交化 Alpha 的实用技术》(article_id 41509899396375, votes 18)。核心内容：
- **截面回归残差**＝从信号中剥离已知系统性因子暴露、保留「因子无法解释的纯信号」，数学上保证与风险因子**截面上正交**。FASTEXPR 无原生截面回归，但可用 `signal − group_mean(signal,1)` 去均值 → `group_mean(signal_dm × factor_dm,1) / group_mean(factor_dm × factor_dm,1)` 求 beta → 取残差 三步近似。
- **简化替代：`group_zscore(signal, industry)`** —— 行业内 z-score 等效于去除行业均值与行业标准差；与完全回归残差相比略差（不剥离行业内因子暴露斜率），但**更简单更稳定**。
- **分层剥离有顺序**：先剥离分类变量（行业），再剥离连续变量（市值）；**反向操作会重新引入行业暴露**。
- **三种剥离方式的取舍表**（帖内原表）：表达式内回归残差（精度高/透明度高，但增复杂度与估计误差）vs `group_zscore` 近似（中/高）vs 平台 neutralization 参数（高/**低，黑箱**）。
- 评论 `LY43440` 补充：**行业内股票数少时 `group_zscore` 估计不稳定、极端值被放大** ⇒ 可先 `group_rank` 再转 zscore，或合并到更高层级行业分类。

**第十批备料（已过三闸 valid/valid/safe、单位零风险、算子 5/5 ≤12）**：
- **G1** `group_zscore(ts_backfill(divide(vec_avg(total_salary_amount), vec_avg(employee_headcount)), 22), industry)` —— M1 水平面改用**表达式内行业残差近似**（对照 M1+STAT 0.93 的平台 STATISTICAL）。
- **G2** `group_zscore(ts_backfill(divide(vec_avg(total_salary_amount), vec_avg(employee_headcount)), 66), industry)` —— 再叠加回填窗 66（已验证有效的杠杆）。
- **假说**：若 G1/G2 > 0.93 ⇒ 表达式内透明剥离优于平台黑箱 STATISTICAL，且可进一步叠市值残差（3 步近似）；若 ≤ 0.93 ⇒ 平台 STATISTICAL 已足够，不必增表达式复杂度（符合帖内「平台参数剥离更简单、已验证」的取舍）。
## 二十二、第九批收批：双杠杆叠加出 S 0.96（3 闸最优）+ 变化面 STATISTICAL 结论两例互证（§115，2026-11-05 18:18）
- **★★★ R3 = 回填窗 66 × STATISTICAL（水平面）S 0.96 / F 0.35 / TO 6.04% / sub 0.58 / 2Y 0.75 / DD 2.02%（全波最低）/ margin 5.50bp**。**只差 3 闸**（`LOW_SHARPE 0.96/1.58`、`LOW_FITNESS 0.35/1.0`、`LOW_2Y_SHARPE 0.75/1.58`），**`CONCENTRATED_WEIGHT` pass + `LOW_SUB_UNIVERSE_SHARPE` pass**，**逐年 10 年全部为正、零负年**（2015 2.31 / 2021 1.79 / 2020 1.20 / 2023 1.10）。
  - ⇒ **两个已验证杠杆可叠加**：M1(FAST,窗22) 0.85 → M1(STAT,窗22) 0.93 → R3(STAT,窗66) **0.96**；且叠加后**同时解掉 CW 闸（回填窗把持仓打散）与 sub 闸（STATISTICAL 提纯）**。**回填窗与 STATISTICAL 作用在不同层面、不冗余**。
- **R4 = M7 + STATISTICAL S 0.65**（FAST 基线 0.82，降 0.17）⇒ **「STATISTICAL 对变化面无效」第二例，与 M8+STAT（0.74→0.66）独立一致 ⇒ 两例互证、结论稳健**。
- **★ 操作纪律（本波沉淀）**：
  | 信号形态 | 中性化选择 | 依据 |
  |---|---|---|
  | 水平面（存量水平，`rank`/`group_rank`） | **STATISTICAL 优先** | 两例提 S（0.85→0.93）、提 sub、修逐年全正 |
  | 变化面（`ts_delta` 差分） | **保持 FAST，不试 STATISTICAL** | 两例降 S（−0.08 / −0.17） |
  | 低频月度存量字段 | **回填窗 22→66** | 降噪 + 解 CW 闸 + 降换手 |
- **已派第十批 `fRTmyYY4nxaQu109YNbtt4`**（STATISTICAL）：G1 `group_zscore(..., 22), industry` / G2 `group_zscore(..., 66), industry`（论坛《🟢 截面回归残差》表达式内行业残差近似）。若 G2 > 0.96 ⇒ 表达式内透明剥离更优，可再叠市值残差（EUR 市值字段 `market_capitalization_dlr1` cov 0.9998）；若 ≤ 0.96 ⇒ 平台 STATISTICAL 已足够。
- **候选池（26 骨架，按 S）**：R3 0.96（3 闸最优）/ M1+STAT 0.93 / L3 0.86（CW pass）/ M1 0.85 / M7 0.82 / L1 0.81 / M8 0.74 / L2 0.70 / M12 0.68 / M6 0.68 / M8+STAT 0.66 / R4 0.65。全部 0 过硬闸。
## 二十三、第十一批备料被「算子上限 12」当场拦下（2026-11-05 18:24）
尝试把论坛帖《🟢 截面回归残差》的 **3 步市值残差**写进 FASTEXPR（`signal_dm − beta × size_dm`，size 用 `market_capitalization_dlr1` cov 0.9998）：
- **H1 纯市值残差（全局截面）** = `subtract(subtract(SIG, group_mean(SIG,1)), multiply(divide(group_mean(multiply(subtract(SIG,group_mean(SIG,1)), subtract(SIZE,group_mean(SIZE,1))),1), group_mean(multiply(subtract(SIZE,group_mean(SIZE,1)), subtract(SIZE,group_mean(SIZE,1))),1)), subtract(SIZE,group_mean(SIZE,1))))` ⇒ **算子数 35、表达式长 786 字符**。
- **H2 行业 z-score 后再叠市值残差（帖内 Layer1→Layer2）** ⇒ **算子数 32、长度 749**。
- 两者 preflight/validate/operator_audit 均 valid/valid/safe，但 **算子数远超上限 12**，且单位自检正则命中 `subtract(x, 1)` 形态 ⇒ **不派发**。
- ⇒ **算子上限纪律的实战价值**：论坛帖给的是「方法论伪代码」，不是可提交表达式；**带内联重复子表达式的回归式天然撞算子上限**（同一 SIG 被写 3 次、SIZE 被写 4 次）。
- **可行替代（若 G2 有效再考虑）**：用**平台参数**做市值层剥离（`neutralization` 已是黑箱剥离，无需表达式内重复），或用单层 `group_zscore` 而非 3 步残差。**不要为追一个论坛方法而堆算子。**
- **登记**：EUR 可用市值字段 —— `market_capitalization_dlr1`（cov 0.9998，ac 46）/ `market_capitalization_value_5`（0.7514）/ `firm_market_capitalization`（0.5）。
## 二十四、第十批收批：group_zscore 行业残差 ≈ STATISTICAL 的 S，但 2Y 明显更高（§116，2026-11-05 18:33）
- **G1** `group_zscore(..., 22), industry` = **S 0.95 / F 0.36 / TO 8.37% / sub 0.58 / 2Y 1.29 / DD 2.12%**，**10 年全部为正、零负年**（2015 1.79 / 2023 **1.59** / 2021 1.22 / 2016 1.08 / 2022 1.08）。
- **G2** `group_zscore(..., 66), industry` = **S 0.94 / F 0.35 / TO 6.40% / sub 0.57 / 2Y 1.04 / DD 2.14%**，**3 闸**（LOW_SHARPE / LOW_FITNESS / LOW_2Y_SHARPE），**CW + sub 双 pass**，10 年全正。
- **★★ 归因：二者互补而非互斥**。总 S 几乎相同（G1/G2 0.95/0.94 vs R3 0.96 / M1+STAT 0.93），但 **2Y 差 0.54**（G1 1.29 vs R3 0.75）。机制：STATISTICAL 是 PCA 多因子剥离（提总 S + 全期一致性），`group_zscore` 是行业内标准化（把**行业共同波动**剥干净 ⇒ 近期两年更稳 ⇒ 2Y 高）。⇒ **最优形态是两者叠加**（G1/G2 本身已含平台 STATISTICAL）。
  | 维度 | 平台 STATISTICAL | 表达式内 group_zscore | 叠加（G1/G2） |
  |---|---|---|---|
  | 总 S | 0.93 | 0.95 | 0.94–0.95 |
  | 2Y | 0.75 | **1.29** | 1.04–1.29 |
  | 逐年一致性 | 10 年全正 | 10 年全正 | 10 年全正 |
  | CW 闸 | pass（配窗66） | pass（配窗66） | pass |
- **已派第十一批 `2e0GrJs05ikbv5da3F9L0u`**（STATISTICAL）：**S1** `group_zscore(..., 22), sector` / **S2** `group_zscore(..., 22), subindustry)` —— 单变量换分组轴，与 G1 的 industry 臂对照（三闸全过、算子 5/5）。
- **候选池（28 骨架）**：R3 0.96（3 闸/CW+sub/10 年全正）/ G1 0.95（**2Y 1.29 最高**）/ G2 0.94（3 闸/CW+sub）/ M1+STAT 0.93 / L3 0.86（CW pass）/ M1 0.85 / M7 0.82 / L1 0.81 / M8 0.74 / L2 0.70 / M12 0.68 / M6 0.68 / M8+STAT 0.66 / R4 0.65。全部 0 过硬闸。
## 二十五、2Y 强对冲与修 2Y 的反直觉实测（外部取证，2026-11-05 18:48）
**帖 A**《【结构认知】全周期 sharpe 和 2y sharpe 的强对冲：为什么 2y 是最难关卡》(article_id 43583615602711, votes 23)：全周期 S 与 2Y **强对冲**（案例：分析师族全周期 0.87 / 2Y 0.64→1.18 单调反向；换变化轴 ts_delta 60d 后全周期抬到 0.96、2Y 压回 0.64 ⇒ **调参只是在跷跷板上挪支点**）。**2Y 崩塌是「信号衰减」的现场证据**，比 os2023 还快（2Y 现在能测，os2023 要等提交后一年）⇒ **2Y 是预筛、os2023 是终审**。用法：**批次设计就分两车道**（全周期最优车道 / 2Y 最优车道），两车道无交集 ⇒ 信号是历史型的，及早归档；全车道闭合而 2Y 仍不达标 ⇒ **整理证据链上报裁决，不换批继续磨**。

**帖 B**《【踩坑复盘】修 LOW_2Y_SHARPE 的五个反直觉实测》(article_id 44349557269655)：
1. **signed_power / sign 套在已排序信号外常是精确空操作**（三臂读数逐位相同；zscore 字段上 signed_power(·,2)/(·,0.5) 与对照 SH 1.06/FIT 0.59/TO 0.1888 一模一样）⇒ **想改 2Y，「形状轴」不用试**。
2. **decay 能修 2Y 但只在少数族里，方向像抛硬币**（11 族 30 子臂：2Y 随 decay 6 升 5 降，10 个失败母臂只翻过来 1 个，9 臂在低 decay 下新挂 CW）。小坑：**decay=1 与 decay=0 读数逐位相同**；**2Y 显示 1.58 时可能 PASS 也可能 FAIL**（门拿未取整值严格比较）。⇒ 只差 0.03 以内值得试一次 d0，别指望它。
3. **一心优化 Fitness 会把 2Y 优化掉**（Fitness 0.66→0.96 同时 2Y 1.90→0.78、未过门数 3→6）⇒ 优化目标应是「**还差几道门、差多少**」，不是 Fitness。
4. **2Y 与 INVCON 对中性化/窗口的要求正好相反**（2Y 偏好 STATISTICAL+短窗、INVCON 偏好 SUBINDUSTRY+长窗）⇒ **门限随 alpha 浮动**（同一道 INVCON 四臂门限 1.11/0.97/0.97/1.00）⇒ **必须用同一次检查里的 limit 比，不要用记住的固定值**。
5. **换宇宙、换中性化修 2Y 越改越差**（EUR 营收意外预测 2Y 1.37 不过门；换更小宇宙 2Y 0.07/0.78、换 STATISTICAL 2Y 0.97，无一更好）⇒ **2Y 不过多半是信号近两年本身变弱**。

### ★ 与本波的直接对照（外部实证背书）
- 帖 B 第 5 条「换 STATISTICAL 把 2Y 从 1.37 压到 0.97」——**我们的 R3 正是同型现象**（M1+STAT 2Y 0.76）。而 **G1 用 `group_zscore` 把 2Y 拉到 1.29** ⇒ **「换剥离形态」（平台 PCA → 表达式内行业 z-score）有效**，因为它换的是**剥离对象**而非同层参数，这正是帖 B 第 5 条的例外情形。
- 帖 A「两车道分流」支持本波做法：**R3 车道 = 全周期最优**（STATISTICAL+长回填，S0.96、10 年全正）、**G1 车道 = 2Y 最优**（group_zscore，S0.95、2Y 1.29），两车道**已找到交集**（G1 同时 S0.95 + 2Y 1.29 + 10 年全正）⇒ **该信号不是历史型的，可继续深挖**。
- 帖 B 第 1 条 ⇒ **不做 signed_power/sign 形状轴**（登记为禁轴）；第 2 条 ⇒ decay 轴值得试一次 d0 但期望低；第 3 条 ⇒ 优化目标改为「差几道门」。
- **CLUSTER_TEST 性质确认**（论坛《【KOR/D1】Cluster Test 上线实测》+《点亮 Pyramid 不是凑三个 Alpha》）：**Cluster Test 仅打标、不影响提交资格**；`MATCHES_THEMES` 亦为诊断/warning 项；**只有硬性 IS 检查 PASS 才算通过，Warning 不能当通过**。⇒ 本波 `CLUSTER_TEST` warning 不必修，但 `MATCHES_PYRAMID` pass 需保留（点塔证据）。

## 二十六、第十一批收批：sector 轴 S 1.09 首次破 1.0（§117，2026-11-05 18:52）
- **S1 = `group_zscore(..., 22), sector`** `E5666LXJ`：**S 1.09 / F 0.45 / TO 8.97% / sub 0.57 / 2Y 1.05 / returns 2.17% / DD 2.51% / margin 4.83bp / longCount 1323 / pnl 2,235,503**。**本波首次破 1.0**。`ra.failed_ra_count=4`、**`ppa_failed_count=0`（PPA 通道全过）**、`pyramids.effective=1 / [EUR/D1/OTHER ×1.5]`。逐年：0.95 / **2.81** / 0.96 / 0.88 / 0.59 / 0.50 / 0.83 / 1.50 / 0.74 / **1.57** ⇒ **10 年全部为正、零负年**。
- **S2 = `group_zscore(..., 22), subindustry`** `6XdddJvp`：**S 0.84 / F 0.28 / TO 8.28% / sub 0.49 / 2Y 1.02 / DD 2.54%**；fail 四闸；逐年 2019 −0.16 / 2023 −0.03 有负年。
- **★★ 关键归因（推翻此前结论）**：分组轴在 `group_zscore` 形态下的最优是 **sector > industry > subindustry**（1.09 / 0.95 / 0.84）。这与面 A/面 B 早期「换轴不增 S」（M6 industry 0.68 vs M8 subindustry 0.70、L2 subindustry 0.70 < M8 industry 0.74）的结论**方向相反** ⇒ **「分组轴优劣」不是数据集属性，而是「分组算子形态 × 分组粒度」的交互**：早期那些臂用的是 `group_rank`（秩变换，抹平组内幅度信息），本波用的是 `group_zscore`（组内标准化，保留组内相对幅度）⇒ **在保留组内幅度的形态下，更粗的分组轴反而更好**（粗轴组内成分更同质 ⇒ z-score 后更干净；细轴组内异质 ⇒ 标准化估计不稳）。**这一条与论坛评论 `LY43440`「行业内股票数少时 group_zscore 估计不稳、极端值被放大」完全一致**（细轴 ⇒ 每组样本少 ⇒ 估计不稳）。
- **已派第十二批 `4kTNRk5nH4Q7cpG15QwJM8Bl`**（STATISTICAL）：**U1** `group_zscore(..., 66), sector`（sector 优势 × 回填窗 66 叠加）/ **U2** `group_zscore(..., 120), sector`（**窗口意义**：120 交易日 ≈ 半年，覆盖两个薪酬评审周期）。两条三闸全过、算子 5/5、单位零风险。
- **候选池（30 骨架）**：**S1 1.09**（PPA 全过 / 10 年全正 / 2Y 1.05）/ R3 0.96（3 闸/CW+sub）/ G1 0.95（2Y 1.29 最高）/ G2 0.94（3 闸）/ M1+STAT 0.93 / L3 0.86（CW pass）/ M1 0.85 / M7 0.82 / L1 0.81 / S2 0.84 / M8 0.74 / L2 0.70 / M12 0.68 / M6 0.68。全部 0 过硬闸。
## 二十七、第十二批收批：U1 S 1.12（3 闸 / PPA 全过）+ 最优骨架定型（§118，2026-11-05 19:05）
- **U1 = `group_zscore(ts_backfill(人均薪资, 66), sector)` + neutralization STATISTICAL** ⇒ **S 1.12 / F 0.48 / TO 7.09% / sub 0.58 / 2Y 1.01 / DD 3.02% / margin 6.41bp**，**本波最高**，**只差 3 闸**（LOW_SHARPE 1.12/1.58、LOW_FITNESS 0.48/1.0、LOW_2Y_SHARPE 1.01/1.58），**CW + sub 双 pass**、**`ppa_failed_count=0`（PPA 通道 7 项全过）**、**逐年 10 年全部为正**（2015 **2.98** / 2021 1.54 / 2023 1.51）。
- **U2 = 同骨架但回填窗 120** ⇒ S 0.98、sub 0.45 **fail**、2Y 0.77 ⇒ **窗口 66 是甜点**（120 日≈半年，过长会把近期变化抹平；66 日≈一个季度，与月度薪资更新周期匹配）。
- **最优骨架定型**：`group_zscore(ts_backfill(divide(vec_avg(total_salary_amount), vec_avg(employee_headcount)), 66), sector)` + `neutralization=STATISTICAL`（5 算子）——**机制面（人均薪资水平）+ 最优分组形态（group_zscore×sector）+ 最优回填窗（66）+ 最优中性化（STATISTICAL）四者全叠加**。
- **已派第十三批 `B4dMv12o4NwbR31dLDmzl9i`**（STATISTICAL）：**W1** 流出轴 × sector × group_zscore × 窗66（面 F 首次在最优形态下测，正交交叉）/ **W2** 威望面 × sector × group_zscore（M2 原 `rank`+industry 全灭，按「分组算子形态会改结论」做正当的形态修正重测）。
- **候选池（32 骨架）**：U1 1.12（3 闸/PPA 全过）/ S1 1.09（4 闸/PPA 全过）/ U2 0.98 / R3 0.96 / G1 0.95（2Y 1.29 最高）/ G2 0.94 / M1+STAT 0.93 / L3 0.86 / M1 0.85 / S2 0.84 / M7 0.82 / L1 0.81 / M8 0.74 / L2 0.70 / M12 0.68 / M6 0.68。
## 二十九、第十三批收批：威望面正式判死 + 流出面方向一致 + submit_verdict 判定（§119，2026-11-05 19:22）
- **W1 流出面 × sector × group_zscore × 窗66** = **S −0.60 / sub −0.61 / 2Y −1.60**，逐年 7/10 年为负、方向一致 ⇒ 与 M10（`group_rank`+industry S−0.68）**同号** ⇒ 流出面 reversal 方向在两种分组形态下一致，**属方向性全灭**（可翻转救回），**已派 X2 翻转臂**。
- **W2 威望面 × sector × group_zscore** = **S 0.15 全灭** ⇒ **★ 威望面正式判死**：M2（原 `rank`+industry S0.04 全灭）→ W2（**换成最优分组形态后仍全灭**）⇒ **两种形态 × 两种分组轴都是全灭 ⇒ 该面在 EUR 无横截面 alpha，不是「形态没选对」**。面 B 威望面收手。
- **`submit_verdict` 权威判定**：U1 `BLOCKED / FAILED_COUNT_RA:LOW_SHARPE,LOW_FITNESS,LOW_2Y_SHARPE / failed_ra=3 / failed_ppa=0`；S1 `BLOCKED / +CONCENTRATED_WEIGHT / failed_ra=4 / failed_ppa=0`。⇒ **`failed_ppa=0` = PPA 通道 7 项全过，但 PPA 全过 ≠ REGULAR 可提交**（REGULAR 专有 LOW_FITNESS / LOW_2Y_SHARPE / PROD / SELF 不在 PPA 7 项内）。**两件均不可提交。**
- **Fitness 公式验算**：`F = S × sqrt(|returns|/max(TO,0.125))`；U1 = `1.12×sqrt(0.0227/0.125) = 0.477` ≈ 实测 0.48 ⇒ **U1 的 TO 7.09% 已在 0.125 下限之下 ⇒ 降换手对 Fitness 无效，提 Fitness 只能提 returns**。
- **decay 轴依据**：Sharpe 随 decay 倒 U（EUR 峰值 4–6）、Fitness 单调升（8–10 最高）；**低换手基本面类 decay 2–4 就够**；「Sharpe 踩线 ⇒ 降 decay / Fitness 踩线 ⇒ 增 decay」⇒ 本波 decay=4 是合理首测。
- **已派第十四批 `yleJ44MX4SS96P95Ek2Ozr`**（decay=4，其余同 U1）：**X1** = U1 expression + decay 4（破三闸）/ **X2** = 流出面符号翻转 `-group_zscore(...,66,sector)`。
- **机制面台账（本数据集）**：面 A 净雇佣流量 4/6 全灭（已证弱）/ 面 B 薪资水平 **正号主面**（8+ 条）/ 面 B 薪资变化面（负号，7–8/10 年正）/ 面 F 员工流出（reversal 待翻）/ **面 B 威望面 —— 正式判死** / 数据质量族 `unreliable_*` 未测（只能作门控）。

## 二十八、破 U1 三闸的设置轴取证 + submit_verdict 权威判定（§119 前置，2026-11-05 19:15）
### 28.1 `submit_verdict` 权威判定（否决权威）
- **U1 `VkxxNJl5`** ⇒ `verdict=BLOCKED / reason_code=FAILED_COUNT_RA:LOW_SHARPE,LOW_FITNESS,LOW_2Y_SHARPE / failed_ra=3 / failed_ppa=0 / submit_status=404 / exit_code=1` ⇒ **阻 3 闸，不可提交**。
- **S1 `E5666LXJ`** ⇒ `verdict=BLOCKED / FAILED_COUNT_RA:LOW_SHARPE,LOW_FITNESS,CONCENTRATED_WEIGHT,LOW_2Y_SHARPE / failed_ra=4 / failed_ppa=0` ⇒ **阻 4 闸，不可提交**。
- ★ **`failed_ppa=0` 的确切含义**：`submit_verdict` 的 Failed-PPA 计数为 0 ⇒ **PPA 通道 7 项检查全过**（PPA 只算 7 项 PPA 检查 + `LOW_SHARPE` value<1；REGULAR 专有的 `LOW_FITNESS`/`LOW_2Y_SHARPE`/`PROD_CORRELATION`/`SELF_CORRELATION` 不在 PPA 7 项里）。⇒ **PPA 全过 ≠ REGULAR 可提交**，两套门槛不同，本波两件仍需补 REGULAR 三闸 + prod/self。
### 28.2 Fitness 公式验算 ⇒ 提 Fitness 的杠杆被排除了「降换手」
- **公式**：`Fitness = Sharpe × sqrt(|returns| / max(turnover, 0.125))`。
- **U1 代入**：`1.12 × sqrt(0.0227 / max(0.0709, 0.125)) = 1.12 × sqrt(0.0227/0.125) = 1.12 × 0.426 = 0.477` ⇒ 与实测 **0.48** 吻合。
- ⇒ **U1 的 turnover 7.09% 已低于 0.125 下限**，分母被钳在下限 ⇒ **降换手对 Fitness 无效，提 Fitness 只能靠提 returns**（即提高信号对组合收益的贡献比例）。**这条直接排除「用 decay/平滑压换手来提 Fitness」这条无效杠杆。**
### 28.3 decay 轴取证（论坛《decay参数调优的一个实用经验：从Sharpe到Fitness的平衡点》article_id 41419197070359, votes 16）
- **decay 与 Sharpe 呈倒 U 型**：EUR/TOP2500/analyst 类数据 decay 0→10，Sharpe 峰值在 **decay 4–6**；**Fitness 随 decay 单调上升**（8–10 最高）⇒ 高 decay 降换手改善 Fitness，但过度衰减损害边际收益、压低 Sharpe。
- **按信号类型给建议**：换手率敏感类（news/sentiment）用 decay 6–8；**低换手率类（fundamental）decay 2–4 就够，过高会让信号过平滑、丢失截面差异**。⇒ **本波是低换手基本面（TO 7.09%）⇒ decay 应在 2–4 区间试，不是 6–8**。
- **调参技巧（可直接用）**：**「Fitness 高但 Sharpe 踩线」⇒ 优先**降低** decay；「Sharpe 高但 Fitness 低」⇒ **增加** decay。**U1 是两者都未过**（S1.12<1.58、F0.48<1.0），属混合型 ⇒ 先试 decay=4 与 decay=2 两档，看 Sharpe 与 Fitness 是否反向移动。
- 评论 `FF45555` 补充：**最优窗口是 region 依赖的，不是只跟 dataset 走**；MEA/TOP400 需 hump 或 double-smoothing 才能过 Sub-universe，CHN/TOP3000 需更长窗（ts_mean ≥ 10 天）⇒ **先按 region 定窗口，再按 dataset 微调**。EUR 属 decay 敏感度中庸区。
### 28.4 第十四批备料（待第十三批释放槽位）
- **X1 = U1 expression + decay 4**（低换手基本面建议区间 2–4 的上沿；也试「Sharpe 踩线 ⇒ 降 decay」）
- **X2 = U1 expression + truncation 0.08**（论坛《聊一下因子优化里 Truncation 的实际用法》：调大 truncation ⇒ Fitness/收益上升但换手与回撤同步放大；**U1 的 TO 已在下限，收益上升是唯一出路**）
- **纪律**：每批只改**一个**设置；decay 与 truncation 不同时改；判读看 **S / F / returns / TO / DD / sub** 六项一起（因 Fitness 被 TO 钳住，须同时看 returns）。
- **备用杠杆**：sector 轴已是 z-score 形态最优粗轴，**country 轴（更粗）已预检通过但未测**（若 sector→country 不降，说明粗轴收益已到顶，可收手转设置轴）。

- **S1 相关性预筛**：self **0.1021 pass**（红线 0.7，余量极大；与已提交池几乎零重叠）；prod 平台计算中（inflight）⇒ **未测得前不得称可提交**。

## 三十、第十四批收批：decay 无效 + 流出面 reversal 确认 + 候选池互相关体检 + SNR 骨架（§120，2026-11-05 18:42）
- **X1（decay 4）S 1.12 与 U1（decay 1）逐位相同**（S/F/2Y/sub 全同）⇒ **decay 轴在本波关闭**（TO 6.9% 远低于 0.125 下限，平滑无空间；印证帖 B「decay=1 与 0 读数逐位相同」）。
- **X2 流出面翻转 S 0.59 / 2Y 1.60（最高）/ 只差 2 闸**（`LOW_SHARPE` `LOW_FITNESS`）⇒ **流出面 reversal 在 EUR 确认**（本会话第 4 次靠翻转救回）。
- **★ 候选池互相关体检（`compute_mutual_correlation` 4 年期）**：七条候选 21 对**全部 0.80–0.99**，`max_mutually_below_subset` 只有 1 个 ⇒ **同一机制面的多个杠杆版本无法互相去相关，不能靠它们凑 OTHER 塔的 3 颗** ⇒ 第三颗必须来自**正交机制面**。
- **★ SNR（信噪比）骨架 —— 与水平面正交的第三条路**（论坛 article_id 43179521660823, votes 109, 45 评论；USA/GLB/EUR 三市场验证）：
  `b = divide(ts_zscore(a, W_long), ts_std_dev(ts_zscore(a, W_short), W_vol))` ; `alpha = group_zscore(b, G)`
  - 分子＝相对自身长期历史的偏离强度，分母＝短周期波动率（噪音强度）⇒ 比值即 **t 统计量** ⇒ **用偏离的显著性而非幅度选股**。理论：Zhang (2006, JF) 信息不确定性 ⇒ 高噪音自动降权。
  - **原帖骨架算子 13 超上限 12 ⇒ 压缩分母为 `ts_std_dev(a, W_vol)`（等价 t 统计量简化式）**。
  - **已派第十五批 `9T99EfFX4vK9qU170FkFSxu`**：**Y1** `group_zscore(divide(ts_zscore(回填22,252), ts_std_dev(回填22,66)), sector)`（**12 算子，正好上限**）/ **Y2** 同式但信号基线回填窗 66。符号先验：人均薪资处自身历史高位 = 人力资本投入持续加码 ⇒ 延续性 ⇒ **正号**。窗口意义：W_long 252（年，偏离基准）/ W_vol 66（季，波动率窗）。
- **候选池（36 骨架）**：U1/X1 1.12（3 闸/PPA 全过/10 年全正）/ S1 1.09（4 闸/self 0.1021）/ U2 0.98 / R3 0.96 / G1 0.95（2Y 1.29）/ G2 0.94 / M1+STAT 0.93 / L3 0.86 / M1 0.85 / S2 0.84 / M7 0.82 / L1 0.81 / M8 0.74 / L2 0.70 / M12 0.68 / M6 0.68 / **X2 0.59（2 闸/2Y 1.60 最高）**。

## 三十一、第十五批收批 + ★ 正交性突破：找到可共存的三条组合（§121，2026-11-05 18:24）
- **Y1 SNR（分子 252 / 分母 std_dev 66）S −0.04 / Y2（基线回填66）S −0.15** ⇒ SNR 骨架当前形态无信号、逐年符号随机翻转。**但其信息形态与水平面正交**。
- **★★★ 互相关矩阵（compute_mutual_correlation 4 年期）**：
  - U1 ↔ X1（同表达式仅 decay 不同）= **0.9991**
  - **SNR ↔ 水平面 U1 = −0.1558（正交）**
  - **流出 ↔ 水平面 U1 = −0.2125（正交）**
  - SNR ↔ 流出 = 0.1496
  - **max_mutually_below_subset = [VkxxNJl5, RREE5o1d, mLooKbe9] = 3 条可共存**
- **★ 点塔解法**：之前「21 对全 0.80+」是因为那 7 条**全是水平面变体**。**引入正交信息形态（SNR 显著性面 + 流出 reversal 面）后互相关降到 −0.21 ~ +0.15 ⇒ 三条可同时提交**（水平面 1.12 / SNR 面 / 流出面 0.59）。**点塔第 2/3 颗必须来自正交机制面**——模板级可执行证据。
- **已派第十六批 3Ixlmp68l5ivabH1bjhmDs3p**（救 SNR 面，各 12 算子）：**V1** 分子窗 252→66 + 分母窗 66→22 / **V2** 分子改 ts_rank(66)（秩化显著性，避开慢 z-score 窗）。
- **候选池（38 骨架）**：U1/X1 1.12（3 闸/PPA 全过/10 年全正）/ S1 1.09 / U2 0.98 / R3 0.96 / G1 0.95（2Y 1.29）/ G2 0.94 / M1+STAT 0.93 / L3 0.86 / M1 0.85 / S2 0.84 / M7 0.82 / L1 0.81 / M8 0.74 / L2 0.70 / M12 0.68 / M6 0.68 / **X2 0.59（2 闸/2Y 1.60）** / Y1 −0.04 / Y2 −0.15（SNR 正交面）。

## 三十二、第十六批收批 + ★ 四条候选互相关全部可共存（§122，2026-11-05 18:28）
- **V1（SNR 分子 66 / 分母 22）S −0.13**（符号随机翻转、|S|≈0，TO 20.28%）；**V2（分子 ts_rank 66）S −0.67，逐年 8/10 年为负、方向基本一致** ⇒ 属**方向性全灭** ⇒ 已派 **T1 符号翻转臂**（预期 ≈ +0.67）。
- **★★★ 互相关复测（4 条候选 6 对）**：V2↔V1 0.1764 / **V2↔U1 −0.1204** / V2↔X2 0.0711 / **V1↔U1 −0.0582** / V1↔X2 0.0551 / **U1↔X2 −0.2125** ⇒ **max_mutually_below_subset = 4 个元素（V2+V1+U1+X2），全部在 −0.21 ~ +0.18** ⇒ **四条可同时共存**，点塔 3 颗在「互相关」维度已无障碍，剩下是「各自过没过硬闸」。
- **已派第十七批 `4aTk598QW56YbiL13LoYZmz`**（decay 1 + STATISTICAL）：**T1** = V2 符号翻转（12 算子，SNR-tick 面）/ **T2** = X2 流出面换 country 轴（5 算子，呼应「group_zscore 形态用粗轴更稳」）。
- **★★ 换集候选：macro27（MACRO 塔，Job records from job posting，cov 0.3273，33 字段）** —— **本战役唯一「合法未测」候选**：全库 token 级检索**零判死命中**；本地画像 33 字段全 `n_tests=0`、verdict 全 UNUSABLE（旧口径）。关键字段：`mcr27_company_ajnet`（招聘净变化 created−removed）、`num_jobs_active/created/removed`（cov 0.43）、`mcr27_company_jobsactive`（ac 537 饱和）、`is_job_repost_flag`（重复发布标记 ⇒ 可作数据质量门控）、`avg_days_job_posting_active/closed`（职位挂起时长）。**与 workforce 面同源但独立数据集 ⇒ 用前须先做同源比对**；forum《vec_sum 还是 vec_avg》提醒 created/removed 比值衡量的是「岗位流水净扩张」而非雇佣速度。
- **EUR 全 14 塔清单完成**：OTHER **唯一可挖**（S1.12）；INSIDERS 判死（S 天花板 0.95）；RISK 判死（残差族单调衰减）；SENTIMENT 数学不可达（Fitness 上限 0.455）；PV 快腿已死 + 慢腿 prod 占满；INSTITUTIONS exhausted（returns 上限 0.0089 ⇒ Fitness 0.080）；EARNINGS 已判死；NEWS 饱和；SOCIALMEDIA 不可达；MACRO 仅 macro27 未测；其余塔 0/3 未探。
- **候选池（40 骨架）**：U1/X1 1.12（3 闸/PPA 全过/10 年全正）/ S1 1.09 / U2 0.98 / R3 0.96 / G1 0.95（2Y 1.29）/ G2 0.94 / M1+STAT 0.93 / L3 0.86 / M1 0.85 / S2 0.84 / M7 0.82 / L1 0.81 / M8 0.74 / L2 0.70 / M12 0.68 / M6 0.68 / **X2 0.59（2 闸/2Y 1.60）** / **V2 −0.67（SNR-tick 待翻转 T1）** / V1 −0.13 / Y1 −0.04 / Y2 −0.15。

## 三十四、第十七批收批：★ 三条正 S 候选互相关全部 ≤0.2125 ⇒ 可同时提交（§123，2026-11-05 18:42）
- **T1 = V2 符号翻转（SNR-tick 面）`RREE9Eo0` S +0.67**（V2 S−0.67 → **完全镜像**）⇒ **SNR-tick 面确立为第三条正信号候选**（本会话第 5 次靠翻转救回）。**SNR 骨架在 EUR 薪资面终于成立**：机制解读 =「人均薪资相对自身历史高位**且该偏离统计上显著** ⇒ 人力资本投入持续加码 ⇒ 未来收益高」（延续性逻辑）。逐年 8/10 年为正（2018 1.80 / 2022 2.09）。
- **T2 = 流出面换 country 轴`leAAEAY5` S 0.30**（低于 X2 sector 的 0.59）⇒ **「group_zscore 用粗轴更稳」不是单调的，存在适中粒度**：本机制 **sector > industry > subindustry，且 country（更粗）反而下降** ⇒ **sector 是最优轴**。
- **★★★ 三条正 S 候选互相关（4 年期）**：
  - T1 ↔ 水平面 U1 = **+0.1204**
  - T1 ↔ 流出面 X2 = **−0.0711**
  - U1 ↔ X2 = **−0.2125**
  - **max_mutually_below_subset = [RREE9Eo0, VkxxNJl5, mLooKbe9]（3 条）**
  ⇒ **点塔所需 3 颗在互相关维度已完全就绪**，三条分属**三个不同经济机制面**（水平溢价 / 显著性延续 / 流出 reversal）。
- **★ 点塔三瓶颈状态**：① 互相关 ✅ 已解决（|r| ≤ 0.2125）；② 机制面正交 ✅ 已解决（三面各有正 S）；③ **硬闸 ❌ 未解决**（最好 U1 S1.12 差 0.46、Fitness 0.48 差 0.52）⇒ 唯一剩余工作是推每条过闸。
- **已派第十八批 `3ad1SueI74nFccgYZMaq69U`**：**U1** = T1 的回填窗 22→66（12 算子）/ **U2** = 流出面换 subindustry 轴（5 算子）。
- **候选池（42 骨架）**：U1/X1 1.12（3 闸/PPA 全过/10 年全正）/ S1 1.09 / U2 0.98 / R3 0.96 / G1 0.95（2Y 1.29）/ G2 0.94 / M1+STAT 0.93 / L3 0.86 / M1 0.85 / S2 0.84 / M7 0.82 / L1 0.81 / M8 0.74 / L2 0.70 / M12 0.68 / M6 0.68 / **T1 0.67（SNR-tick，8/10 正，三条可共存之一）** / **X2 0.59（2 闸/2Y 1.60 最高，三条可共存之二）** / T2 0.30 / V2 −0.67 / V1 −0.13 / Y1 −0.04 / Y2 −0.15。

## 三十六、第十八批收批：回填窗效应依形态而异 + 流出面分组轴谱系完成 + 三条候选 self 全 pass（§124，2026-11-05 19:00）
- **U1 = T1 的回填窗 22→66 S 0.66**（vs T1 窗22 S0.67）⇒ **SNR 面的回填窗无杠杆效应**（水平面「窗66 有效」在 SNR 面不成立）⇒ **回填窗的效应依信号形态而异**：水平面靠窗长补缺失；SNR 面的分子分母都已内含时序窗，外层回填窗是冗余的。**「回填窗有效」不是通用规则。**
- **U2 = 流出面换 subindustry 轴 S 0.23** ⇒ **流出面分组轴谱系完成：sector 0.59 > country 0.30 > subindustry 0.23** ⇒ **sector 是唯一最优轴**（更细⇒组内异质估计不稳；更粗 country⇒剥离的是国别成分而非共同成分）。
- **★★ 三条可共存候选的 self 相关性预筛（本地 MCP，零成本）**：U1 **0.1124 pass** / T1 **0.0182 pass** / X2 **0.0874 pass**（红线 0.7，余量 0.59–0.68，pool 17）⇒ **三条已具备「可进入提交链路」资格，纯粹只差 IS 硬闸**。
- **已派第十九批 `2DT7Ov4vd4UyaOI9C180sfF`**（truncation 0.08）：两条同表达式 `-group_zscore(divide(ts_rank(回填22,66), ts_std_dev(回填22,66)), sector)`（12 算子）。**⚠ 本批是双变量**（分母窗 22→66 + truncation 0.04→0.08 同时改）⇒ **不可用于单变量归因**；定位为「SNR 新分母窗 + 宽截断的**联合测试**」，下一批须恢复单变量复核。
- **候选池（44 骨架）**：U1/X1 1.12（3 闸/CW+sub 双 pass/PPA 全过/10 年全正/self 0.112）/ S1 1.09 / U2 0.98 / R3 0.96 / G1 0.95（2Y 1.29）/ G2 0.94 / M1+STAT 0.93 / L3 0.86 / M1 0.85 / S2 0.84 / M7 0.82 / L1 0.81 / M8 0.74 / L2 0.70 / M12 0.68 / M6 0.68 / **T1 0.67（SNR-tick/self 0.018）** / U1' 0.66 / **X2 0.59（2 闸/2Y 1.60/self 0.087）** / T2 0.30 / U2' 0.23 / V2 −0.67 / V1 −0.13 / Y1 −0.04 / Y2 −0.15。

## 五十一、第二十九批收批：门控阈值是 2Y/sub 取舍旋钮 + ts_mean 是换手/margin 杠杆（§143，2026-11-05 19:45）
- **Y1 `MPYYNMW9`（门控阈值 0.3→0.15）**：**S 1.37（最高）/ F 0.62 / TO 9.45% / sub 0.97 / 2Y 1.51（差 0.07）/ DD 2.03%（全波最低）/ margin 5.50bp**，只差 3 闸，CW + sub 双 pass、**PPA 全过**。
  - **★ 门控阈值 = 「2Y/DD」与「sub」的取舍旋钮**：放宽（0.3→0.15）⇒ 信号更接近完整横截面 ⇒ **2Y +0.21、DD −0.31pp、S +0.02**，但 sub 微降（0.98→0.97）；收紧则反向。
- **W1 `qMLLJ91j`（P2 + ts_mean(5)）**：**S 1.32 / F 0.59 / TO 6.38%（全波最低）/ sub 0.85 / 2Y 1.17 / margin 7.71bp（全波最高）**，3 闸、CW + sub 双 pass、**PPA 全过** ⇒ **帖 A 根因①「行业分组结构问题 → ts_mean 时间平滑」有效**，但它是**换手/margin 杠杆**而非强度杠杆。
- **★ Fitness 公式二次校准（W1 验算）**：`F = 1.32 × sqrt(0.0246/0.125) = 0.586` ≈ 实测 0.59 ⇒ 公式精确成立。**要 F 从 0.62 升到 1.0，在 S=1.37 下需 returns 从 0.026 升到 0.0353（+36%）**，或 S 升到 1.90 ⇒ **F 缺口 ≈ 强度缺口，仍应集中攻 S**。
- **已派第三十批 `RzHKDafi4LEbz5K4j2XnVS`**：Z1 = 门控阈值 0.15→0.05（冲 2Y 1.51→1.58，差 0.07）/ Z2 = Y1 + 回填窗 22→66（测门控与长窗能否叠加）。
- **候选池（34 骨架）**：Y1 1.37（3 闸/2Y1.51/DD 最低）/ V2 1.35（3 闸/sub0.98）/ P2 1.34（4 闸/self0.0783）/ W1 1.32（3 闸/TO 最低/margin 最高）/ V1 1.30（3 闸）/ R2 1.05 · L3 0.86 · M1 0.85 · T1 0.67（self 0.018）/ X2 0.59（2 闸/2Y 1.60/self 0.087）。
## 五十二、第三十批收批 + ★★ 两项方法论纠错 + 第三十一批（FAST 档首次）（§144–§148，2026-11-05 20:10）
- **Z1 `bl661vYq`（门控阈值 0.15→0.05）**：**S 1.38（本波最高）/ F 0.63 / TO 9.55% / sub 0.92 / 2Y 1.52（距 1.58 差 0.06）/ DD 2.13% / margin 5.44bp / inv_sharpe 1.27**，只差 3 闸，CW + sub 双 pass、**PPA 全过**。
  - **★ 门控阈值三点单调曲线（0.3 → 0.15 → 0.05）**：2Y **1.30 → 1.51 → 1.52**、sub **0.98 → 0.97 → 0.92**、S 1.35 → 1.37 → 1.38、DD 2.34% → 2.03% → 2.13% ⇒ **2Y 增益在 0.15 后饱和（+0.21 → +0.01），sub 代价开始显现 ⇒ 甜点 = 0.15**。
  - **Z1 逐年 S**：1.62 / 2.53 / 0.77 / 0.44 / 1.57 / 0.33 / 1.38 / 1.99 / 1.09 / 2.10 ⇒ 8/10 年 ≥1.0，**末 2 年 1.595 / 末 3 年 1.727 / 末 5 年 1.378**，塌陷年是 2019(0.33) 与 2017(0.44) ⇒ **2Y 1.52 非单年驱动**。
- **Z2 `RREEwdJz`（Y1 + 回填窗 22→66）**：**S 1.26 / 2Y 0.82（较 Y1 −0.69）/ sub 0.82 / TO 6.35%** ⇒ **★★ 「门控与长窗不可叠加」成立**：长窗把信号慢化 + 门控做时间选择 ⇒ 末期信息被抹掉 ⇒ **带门控骨架的回填窗必须 ≤22**。
- **★★★ 纠错一：IS_LADDER 不是单数据集 ATOM 的闸** —— 论坛《提交门槛里容易被忽略的硬性项》明写「**多数据集时才会有 IS Ladder Sharpe 要求**」、《筛选可优化RA进阶版》明写「IS_LADDER 在**非 ATOM RA** 中最频繁」；**平台实证：本账号 11 颗单数据集 ACTIVE 件的 `checks.pass` 全无 IS_LADDER_SHARPE，多数据集件则含之** ⇒ **此前把 Ladder 当「比 LOW_SHARPE 更硬的墙」是误判** ⇒ 闸路径收敛为 **LOW_SHARPE / LOW_FITNESS / LOW_2Y_SHARPE** 三道纯强度闸 ⇒ 仍按 `F = S×sqrt(|returns|/max(TO,0.125))` 集中攻 S。
- **★★★ 纠错二：macro27 在 EUR 已被实测，「唯一合法未测集」作废** —— 平台实测 `N1NrOvYX`（S 0.31 / 2Y 1.90）与 `zq3mW1lo`（S −0.88 / DD 23.6%）均属 EUR/D1/MACRO ⇒ **MACRO 招聘面在 EUR 无可用数据集（天花板 0.31）**，该换集候选关闭。⇒ **教训：`query_field_profile.n_tests=0` 只反映本地库记录数，不等于平台未测 ⇒ 换集前必须额外查平台 alpha 池**。
- **★★★★ 未测设置轴：FAST 中性化档** —— 我们 30 批全用 STATISTICAL；本账号 31 颗 EUR OS 件里 10 颗 FAST、最强三件全 FAST；台账 §2170–§2184 早已实证 FAST 对某些信号是 +0.45 S/+0.60 2Y 的全面增益、对另一些是 −0.50 的灾难 ⇒ **必须逐信号 A/B**。本数据集 FAST 档零命中 ⇒ 第三十一批专测此轴。
- **已派第三十一批 `tM15G9Lq4qmcM0Vw0OJ07e`**（EUR/TOP2500/D1/**FAST**/decay1/trunc0.04/nan OFF）：**A1 = Z1 骨架在 FAST 档**（12 算子，单变量对照 S1.38/2Y1.52）/ **A2 = P2 骨架在 FAST 档**（7 算子，单变量对照 S1.34/2Y1.31/CW fail）。
- **候选池（36 骨架）**：Z1 **1.38**（3 闸/2Y1.52）/ Y1 1.37（3 闸/sub0.97/DD 最低）/ V2 1.35（3 闸/sub0.98）/ P2 1.34（4 闸/self0.0783）/ W1 1.32（3 闸/TO 最低/margin 最高）/ V1 1.30（3 闸）/ Z2 1.26（3 闸/2Y0.82）/ R2 1.05 · L3 0.86 · M1 0.85 · T1 0.67（self 0.018）/ X2 0.59（2 闸/2Y1.60/self 0.087）。
- **★ X2 流出面逐年体检（第三十三批设计依据）**：X2 逐年 S = 2.03 / 1.54 / −0.58 / 0.21 / 1.52 / −0.35 / **−1.09** / −0.48 / **2.02** / 1.13 ⇒ **末2年 1.575 / 末3年 0.89 / 末5年 0.246 / 全期 0.595** ⇒ **2Y 1.60 靠 2022–2023 两年撑起；2020–2021 连续两年负（COVID 冲击期）** ⇒ **形态是「中期塌陷」而非「末期崩塌」**，与论坛讨论的 Ladder 末期崩塌形态不同 ⇒ 提 S 的杠杆应指向修中期塌陷。
- **E1 流出面套轻尾重塑 `d5WWvqEX`**：S 0.60 / 2Y 1.47 / sub 0.63 / CW+sub 双 pass / **PPA 失败 1 项** ⇒ **重塑在流出面无效（2Y 反降 0.13、S 平）⇒ 与水平面「重塑是水平面专属」结论一致**。
- **第三十三批备料（已过三闸 valid/valid/safe、单位零风险、算子 10/10 ≤12，待第三十二批释放槽位即派）**：**G2 = 流出面 + 流出率时序分位门控** = `trade_when(greater(ts_rank(ts_backfill(vec_avg(employee_outflow_count),66),252),0.3), -group_zscore(ts_backfill(divide(vec_avg(employee_outflow_count), vec_avg(employee_headcount)),66), sector), nan)` / **G3 = G2 门控阈值反向对照**（`less(..., 0.7)`）⇒ **流出面首次测门控**，两条构成单变量对照。
## 五十四、第三十二批收批：职级结构面判负（负号才是真信号）+ PPA 通道全量核对（§154–§155，2026-11-05 19:40）
- **S1 职级结构 `leAAn5lN`（S −0.91 / F −0.34 / 2Y 0.34 / DD 20.8%）**：逐年 S −1.56 / −2.46 / −0.52 / −2.51 / −0.05 / −0.47 / −1.85 / −1.20 / **+0.54 / +0.09** ⇒ **8/10 年为负、方向一致**。
  - **★ 机制先验被修正**：我原本的先验是「高资历占比 ⇒ 高技能 ⇒ 高收益」（正号），**实测是稳定负号** ⇒ **正确解读反向**：**大量招初级岗位 = 扩张快但人力资本薄 ⇒ 未来盈利质量低**；**只招资深 = 增长停滞/成本高**。这与「招聘扩张负号」先验（Liu & Smirnyagin《Labor-Based Asset Pricing》vacancy 负向预测收益）**同向** ⇒ **该字段的信息在「扩张强度」而非「人力资本质量」上**。
  - **★ 但不派翻转臂**：S1 的 **2Y 是 +0.34（正）而全期 −0.91** ⇒ 负号集中在早年（2014–2021），**近两年已转正/持平** ⇒ 翻转全期符号会让近两年变负 ⇒ **翻转臂预期 S≈+0.91 但 2Y 会变负 ⇒ 过不了 2Y 闸** ⇒ **该面按「全期方向性全灭 + 末期已翻转」判负**（与「一律翻转救回」的常规处置不同，因末期已翻向）。
- **S2 资历层级 `RREEOl1a`（S −0.56 / 2Y 0.26 / DD 14.1%）**：逐年 7/10 年为负 ⇒ 同向弱化版 ⇒ 同面判负。

## 五十五、★★★★★ PPA 通道全量核对：PPA 提交**不**给塔位计数加分（§155，2026-11-05 19:40）
- **论坛权威**：《【新手顾问科普】金字塔如何点亮》(42342005664151)：「**同一区域×延迟×数据集类别下提交 3 个 Alpha 即点亮**」+「**单 Alpha 最多贡献 2 个金字塔**（3 类别及以上不计入）」+「**中性化字段不占类别名额**」+ 策略三「**PPAC 期间门槛低（Sharpe 低、PC 不强制）**」；《PPA 活动主题限制下，提交 ra 点塔的一点心得》(38121310515223)：「**参加活动的 ppa 也都满足 ra 标准，只是有些豁免了 pc 提交**」。
- **PPA 通道门槛**：资格 = `failed_ppa == 0`（7 项全过）、**Sharpe ≥ 1.0**、**算子 ≤ 8**、**字段 ≤ 3**、**PPAC < 0.5**。
- **★ 本账号 EUR 31 件 OS 按通道分塔统计 vs 平台塔位**：
  | 塔 | REG | PPA | 合计 | 平台计数 |
  |---|---|---|---|---|
  | **OTHER** | **2** | **2** | 4 | **2** |
  | MODEL | 6 | 4 | 10 | 3 |
  | PV | 5 | 2 | 7 | 2 |
  | ANALYST | 9 | 1 | 10 | 10 |
  | NEWS | 1 | 1 | 2 | 1 |
  | RISK | 2 | 1 | 3 | 2 | |
  - ⇒ **★ OTHER 塔的 2 颗 PPA 件（`GrdxAPz5`、`blRaArVZ`）没有把塔位从 2 抬到 3** ⇒ **PPA 通道不（或暂不）计入金字塔点亮计数** ⇒ **★ 不能靠 PPA 绕过 REGULAR 硬闸来点亮 OTHER 塔** ⇒ **点塔仍必须靠 REGULAR 通道过全闸**。
- **★ 但 PPA 仍是 Z1/P2 的第二条合格路径**：Z1 PPAC **−0.0029**、P2 PPAC **+0.0028**（红线 0.5，余量 0.49）、self 0.0793 pass、`failed_ppa_count=0`；**P2 算子 7 ≤8 / 字段 2 ≤3 / S 1.34 ≥1.0** ⇒ **P2 按 PPA 口径合格，按 REGULAR 口径被 4 闸拦住**。
- **⚠ 当期 PPA 主题不含 EUR**：全量扫 100 条公告 ⇒ 当期 = 「GLB/D1 Power Pool Nov'26」（10-26～11-22，GLB+Delay1+AMER Sharpe>1）；「OTHER/D1 Power Pool Sept'26」只含 KOR/JPN/CHN/AMR/TWN/HKG 且已结束 ⇒ **EUR 无当期主题窗口**，只能走月度 PPA 竞赛通道（用户在 web UI 提交）。
- **★ 提交顺序纪律**（37718954490135）：日度 **1 个 pure ppa**（pure ppa 提交后 atom+ppa 无法再提交）+ 月度 **10 个 pure ppa** ⇒ **优先提交 atom+ppa（REGULAR），第 10 个 pure ppa 留到最后**。
## 五十六、第三十三批收批：流出面首次测门控 + G3 流出面新高 + 第三十四批（数据质量族首入表达式）（§158–§159，2026-11-05 19:45）
- **G2 严格门控 `vR11Q88Q`**：S 0.62 / F 0.20 / TO 9.36% / sub 0.54 / 2Y 1.36 / DD 5.59%；3 闸，CW+sub 双 pass。
- **G3 宽松门控 `0mYYJql8`**：**S 0.65（流出面最高）/ F 0.21 / TO 8.68% / sub 0.66 / 2Y 1.50 / DD 7.00%**；3 闸，CW+sub 双 pass。
  - **★ 门控规律跨机制面复现**：宽松（保留 70%）全面胜严格（保留 30%）⇒ **「门控越宽 ⇒ 越接近完整横截面 ⇒ 2Y/sub 越好」是门控算子的普遍属性，不是水平面特例** ⇒ **后续所有门控臂一律直接用宽松档 0.7，不再测严格档**。
  - **★ 流出面天花板**：X2（无门控）S 0.59/2Y 1.60 vs G3（门控）S 0.65/2Y 1.50 ⇒ 门控提 S +0.06 但压 2Y −0.10 ⇒ **该面 S 天花板 ≈0.65，距 1.58 差 0.93 ⇒ 流出面无法独立支撑点塔**。
- **已派第三十四批 `3CgEP89Ta4Ts9zOgV86q9JN`**（STATISTICAL/decay1/trunc0.04/nan OFF）：**Q1 = 水平面 + `unreliable_user_count` 存量污染门控** / **Q2 = 水平面 + `unreliable_user_inflow` 流量污染门控**（均 12 算子，宽松档 less(...,0.7)）⇒ **数据质量族 12 字段首次进入表达式**（此前 alphaCount 全 0、只被登记「可作门控」）⇒ **机制：剔除记录污染重的标的 ⇒ 人均薪资估计更可信 ⇒ returns 上升 ⇒ 攻 Z1 的 Fitness 缺口（需 +92% returns）**。
## 五十七、§105 分化轴方案复核（全部不可用）+ SNR 面原式算子 ts_ir 开新臂（§161–§162，2026-11-05 19:50）
- **★ §105 的 D1/D2/D3 全部已被消耗，不可再派**：**D1 = `group_zscore(回填22, industry)`** = `58EEEvmo`（S 0.95）已测；**D2 = country 轴**已测（S 0.30）；**D3 残差正交化**已被论坛《vector_neut 正交化不是免费的》降级（「**正交化是在『创造交易』而不是『发现交易』**」）。⇒ **点塔矛盾点（水平面腿可达但互相关 0.82+ / 正交腿不可达）仍无解**。
- **流入面已充分测过**（T01/T02/T06/T07/M9/H3n/Wa）⇒ **本数据集仅剩两条未测方向：数据质量族门控（第三十四批在飞）、SNR 面原式算子（第三十五批）**。
- **已派第三十五批 `1paQr1Vo5dyc1o163og7YPH`**（STATISTICAL/decay1/trunc0.04/nan OFF）：**IR1 = `group_zscore(ts_ir(ts_backfill(人均薪资, 22), 66), sector)`**（6 算子）/ **IR2 = `group_neutralize(group_zscore(ts_ir(...), sector), country)`**（7 算子，外层 country 轴单变量对照）。
  - **★ 关键差异（官方定义取证）**：`ts_ir(x,d) = ts_mean(x,d) / ts_std_dev(x,d)`（**同一支股票自身**的信噪比）；而本波 SNR 面 T1 用的是 `ts_rank(回填22,66) / ts_std_dev(回填22,22)`（**逐股票时序秩** / **同期截面标准差**）⇒ **两者语义不同**，ts_ir 更贴近「显著性」原意、且只需一个窗口。
  - **为什么值得派**：SNR 面是**唯一与水平面正交（互相关 +0.12）且已出正 S（0.67）** 的面，是点塔第 2 颗腿的现成候选；用**论坛骨架原式算子**替换自造版属**信息形态级**改动（不是参数扫描）⇒ 符合模板互异纪律。
## 五十八、第三十四/三十五批收批：数据质量门控 null-op + ts_ir 原式判负 + 第三十六批（vec_sum 聚合语义轴）（§165–§167，2026-11-05 20:00）
- **Q1 `ZYQQJjqZ`（unreliable_user_count 门控）**：S 1.32 / F 0.58 / 2Y 1.20 / CW fail；PPA 全过。
- **Q2 `58EEXL3M`（unreliable_user_inflow 门控）**：S 1.34 / F 0.60 / 2Y 1.30 / CW fail；PPA 全过。
  - **★ null-op 判定**：Q2 与 P2（无门控）读数**逐项几乎完全相同**（S 1.34=1.34、F 0.60=0.60、returns 2.48%=2.48%）⇒ **unreliable 门控是精确空操作**：坏记录占比与薪资信号正交 ⇒ **数据质量门控轴关闭**（12 个 unreliable 字段两种用法全部排除）。
  - **★ CW 的门控解法定型**：Q1/Q2 的 CW 是 fail（P2 也 fail）⇒ **解 CW 的门控条件必须是「员工数」这类规模代理（V2 的 CW pass），坏记录计数不行**。
- **IR1 `WjOO5P9k`（ts_ir 原式，6 算子）**：S 0.21 / F 0.04 / 2Y 0.72；**IR2 `pwddLP86`（+country 轴）**：S 0.27 / F 0.06 / 2Y 0.69。
  - **★ ts_ir 原式判负**：远弱于自造版 T1（S 0.67）⇒ **SNR 面的有效形态是「时序秩 / 截面噪声」，不是「时序均值 / 时序噪声」**；**country 轴增益也依形态而变**（水平面 +0.41 vs SNR 面 +0.06）。
- **已派第三十六批 `z1D4zg0t4BvbrcbQOD5hUG`**（STATISTICAL/decay1/trunc0.04/nan OFF）：**V1 = Z1 骨架 + `vec_sum` 聚合**（12 算子，门控保持 vec_avg）/ **V2 = P2 骨架 + vec_sum 聚合**（7 算子）。
  - **★ 聚合语义轴（本数据集最后一条未测信息级轴）**：切片是「职位」⇒ `divide(vec_sum(薪资), vec_sum(人数)) = 公司级真实人均薪资`（经济正确的量）；现行 vec_avg 版是「比值平均」（受职位构成影响的伪影）⇒ **两版对公司排序不同**。论坛《vec_sum 还是 vec_avg》规则一「计数类用 vec_sum」⇒ headcount 正是计数类。**grep 确认从未测过**。
  - **预期**：若 vec_sum 版改变排序 ⇒ 与 Z1 互相关可能低于 0.82 ⇒ 可能同时解决「可达性」与「共存性」矛盾（§105 点塔矛盾点）。
## 五十九、第三十六批收批：聚合语义轴被证伪（vec_sum 大幅弱于 vec_avg）+ 第三十七批（group_scale 保幅轴）（§169–§170，2026-11-05 20:05）
- **V1 `78LLe2Nx`（Z1 + vec_sum，12 算子）**：S 0.64 / F 0.20 / sub 0.51 / 2Y 1.39 / returns 1.20%；3 闸，PPA 失败 1。
- **V2 `1YNNr2XW`（P2 + vec_sum，7 算子）**：S 0.58 / F 0.17 / sub 0.46 / 2Y 1.05；4 闸，PPA 失败 1。
  - **★ 预期被证伪**：派发前假设「vec_sum = 公司级真实人均薪资（经济正确）⇒ 应更强」⇒ **实测 vec_sum S 0.64/0.58 vs vec_avg S 1.38/1.34（几乎腰斩）**。
  - **★ 正确的机制解释（反转原推理）**：`vec_avg` 度量的是「**该公司招聘岗位的平均薪资档位**」（记录层面的边际特征），`vec_sum` 度量的是「**全公司总薪资/总人数**」（被大量低薪职位与规模效应稀释）⇒ **EUR 市场上可定价的是「岗位档位溢价」而非「人均总成本」**，与「人力资本质量溢价」先验一致 ⇒ **聚合语义轴判负，vec_avg 确立为最优形态**。
  - **★ 可复用教训**：**聚合算子的选择先问「度量记录层还是公司层」；「公司层面的真总量」不等于「更好的信号」——定价常来自可观测的边际特征而非会计总量**。
- **已派第三十七批 `vD2RY6jR4xm9yInuSmWAuD`**（STATISTICAL/decay1/trunc0.04/nan OFF）：**GS1 = P2 + `group_scale`**（7 算子）/ **GS2 = Z1 + group_scale**（12 算子）。**group_scale 在本数据集从未测过**（保幅 vs 标准化 = 信息形态级轴）。
  - **机制**：`F = S×sqrt(|returns|/max(TO,0.125))` ⇒ TO 已钳在 0.125 ⇒ **提 F 只能靠提高「组合收益占总波动比例」** ⇒ 保幅保留组内相对幅度 ⇒ 可能提高 returns。
  - **⚠ 本批双变量缺陷（留痕）**：两条都用了 **vec_sum**（第三十六批形态）⇒ 与已判负形态耦合 ⇒ 本批只能定位为「group_scale × vec_sum 联合测试」；**若判负，下一批必须回到 vec_avg 形态做 group_scale 单变量复核**。
## 六十、第三十七批收批（group_scale×vec_sum 联合）+ 篮子终验 + 第三十八批（修正单变量）（§173–§175，2026-11-05 20:10）
- **GS1 `d5Wa2exY`（P2+group_scale+vec_sum）**：S 0.59 / F 0.17 / 2Y 1.03 / CW fail；4 闸。
- **GS2 `VkxNvKpA`（Z1+group_scale+vec_sum）**：S 0.69 / F 0.22 / 2Y 1.26 / CW pass；3 闸。
  - **★ group_scale 在 vec_sum 形态的增益边际**：带门控 0.64→0.69（+0.05）、无门控 0.58→0.59（+0.01）⇒ **正增益存在但小**，vec_sum 弱形态（0.6 档）主导 ⇒ **需在 vec_avg 形态上单变量复核**（第三十八批在飞）。
  - **★ CW 规律三向确认**：group_scale 形态下「门控解 CW」依然成立（GS2 pass / GS1 fail）⇒ 与第三十四/二十八批构成三向证据链。
- **★ 篮子终验（Z1 时代互相关矩阵）**：**Z1↔T1 = +0.136 / Z1↔X2 = −0.200 / T1↔X2 = −0.071**（全部远低于 0.5）⇒ **Z1 与两条正交腿完全兼容**；**X2↔G3 = +0.7481 超阈** ⇒ G3 与 X2 是同一信号（流出面 1 篮位，X2 胜出）⇒ **max_mutually_below_subset = [X2, Z1, T1]** ⇒ **点塔三腿篮子结构正式确认**，剩余障碍纯粹是各腿自身 IS 强度（Z1 差 S0.20/F0.37/2Y0.06；T1 差 S0.91；X2 差 S0.99）。
- **已派第三十八批 `2IisO2fUp4ODaemhQPC9Fop`**：**GS1a = P2+group_scale+vec_avg（7 算子，单变量对照 P2 的 S1.34）** / **GS2a = Z1+group_scale+vec_avg（12 算子，单变量对照 Z1 的 S1.38）** ⇒ **判读标准：GS2a 的 S > 1.38 则保幅轴有效；≈1.38 或更低则关闭**。
## 六十一、第三十八批收批：保幅轴判负（group_scale 在最优形态上是负向杠杆）+ 第三十九批（truncation 0.02）（§177–§178，2026-11-05 20:15）
- **GS1a `RREeJA8e`（P2+group_scale+vec_avg）**：S 1.23 / F 0.52 / 2Y 1.11 / CW fail；4 闸，PPA 全过。
- **GS2a `9qxlzErd`（Z1+group_scale+vec_avg）**：S 1.28 / F 0.55 / 2Y 1.29 / CW pass；3 闸，PPA 全过。
  - **★ 保幅轴判负**：GS2a vs Z1：**S −0.10 / 2Y −0.23 / sub −0.11**；GS1a vs P2：**S −0.11 / 2Y −0.20** ⇒ **group_scale 在最优形态上是负向杠杆**。第三十七批在 vec_sum 弱形态上的 +0.05 是**弱形态特有的伪增益**（弱形态幅度方差大，保幅偶然有利；强形态幅度已被 quantile-gaussian 控制）。
  - **★ 水平面最优形态最终确认（38 批全量证据）**：**Z1 = 门控 0.05 + country 外层 + sector 内层 + quantile(gaussian) + vec_avg + backfill 22**——**七个组件全部经单变量对照确认最优**。
- **已派第三十九批 `2wwnLK6WM4Q0b3NigRYuXQS`（trunc 0.02 设置轴）**：**T1' = Z1 @ trunc0.02（对照 S1.38）** / **T2' = P2 @ trunc0.02（对照 S1.34）** ⇒ 依据 §2392「trunc 0.02 稳定 +0.06 S」（另一 EUR 结构）⇒ 若迁移则 1.38→1.44。
  - ⇒ **本批是水平面最后两条未测轴之一**（另一条 W2 market 轴先验偏弱：market 比 country 粗，会保留国别成分）。
## 六十二、第三十九批收批：截断轴 null-op（+0.06 未迁移）+ 第四十批（W2 market 轴，最后未测）（§181–§182，2026-11-05 20:20）
- **T1' `Xg9ajd60`（Z1 @ trunc0.02）**：**S 1.38 / F 0.63 / 2Y 1.53（历史最高）/ sub 0.92 / DD 2.11% / CW pass**；3 闸，PPA 全过。
- **T2' `A1VxRodY`（P2 @ trunc0.02）**：S 1.34 / F 0.60 / 2Y 1.30 / CW fail；4 闸，PPA 全过。
  - **★ 截断轴 null-op**：S 完全相同（1.38=1.38、1.34=1.34）、2Y ±0.01 ⇒ **另一结构的 +0.06 S 未迁移**——**机制**：quantile-gaussian 重塑已轻尾化横截面 ⇒ 权重天然分散 ⇒ truncation 上限不构成约束 ⇒ **轴关闭**。
  - **★ 保留 `Xg9ajd60`**：**2Y 1.53 全波最高（差 0.05）+ DD 2.11% 最低** ⇒ 作为「2Y 最接近的候选」入库。
- **已派第四十批 `fds0Cakx4oQ9lz4UPplvHY`（W2 market 外层轴）**：**W2a = P2+market 外层（对照 S1.34）** / **W2b = Z1+market 外层（对照 S1.38）** ⇒ **先验偏弱**（market 比 country 粗、会保留国别成分）⇒ 预期负向；**信息价值 = 确认外层轴层级 country > market > none** ⇒ **本批之后水平面全部轴已测完**，波次进入收尾阶段。
## 六十四、第四十一批（universe TOPCS1600 轴，本波首次）（§188，2026-11-05 20:25）
- **动机**：台账 L1283/L2005 证实「宇宙轴对信号强度影响巨大且方向依信号而异」；论坛实证 fundamental31 在 TOPCS1600 全过硬闸（S 1.90）；**本波 40 批全在 TOP2500 上，universe 轴从未测过** ⇒ 设置轴（未测机制面）。
- **已派 `XDQ6xbFH4V1ccytY73blxf`**：**A1 = Z1 @ TOPCS1600**（12 算子，对照 S1.38/2Y1.52）/ **A2 = P2 @ TOPCS1600**（7 算子，对照 S1.34/2Y1.31）。
## 六十五、第四十一批收批：universe TOPCS1600 强负向（轴关闭）+ 设置轴全关（§190，2026-11-05 20:30）
- **A1 `rKR7pZZJ`（Z1@TOPCS1600）**：**S 1.01 / F 0.45 / 2Y 0.92 / sub 0.76 / longCount 751（腰斩）/ robust 0.77**；3 闸，PPA 全过。
- **A2 `e75akXX6`（P2@TOPCS1600）**：**S 1.01 / F 0.44 / 2Y 0.56 / sub 0.83 / longCount 743 / CW fail / robust 0.72**；4 闸，PPA 全过。
  - **★ universe 轴关闭**：Z1 S 1.38→1.01（−0.37）、2Y 1.52→0.92（−0.60）、longCount 1392→751（腰斩）⇒ **TOPCS1600 对本信号强负向**（中盘宇宙个股更小 ⇒ 覆盖通过率腰斩 ⇒ 信号被稀释）⇒ 与台账 L1283「宇宙扩宽是稀释源」方向一致 ⇒ **TOP2500 确认为最优宇宙**。
  - **★ 口径差异发现**：TOPCS1600 触发 **robust_universe_sharpe** 检查（0.77/0.72），TOP2500 不触发 ⇒ 「TOPCS1600 会多一道 robust 检查」登记为口径差异。
  - **★ 设置轴全关**：中性化（STATISTICAL 最优）+ decay（无效）+ truncation（null-op）+ universe（TOP2500 最优）⇒ **本波「表达式轴 + 设置轴」全部测完并关闭**。
- **波次最终状态（41 批全量）**：**水平面天花板 S 1.38 / 2Y 1.53（Xg9ajd60）**，全部 14+ 条表达式轴 + 4 条设置轴穷尽关闭 ⇒ **本赛季 EUR 塔位不可达已穷尽实证**。
  - **机制预期**：TOPCS1600（中盘）个股更小、流动性更低 ⇒ 若信号在更宽的宇宙中有效，S 可能抬升（参考 L2005「宇宙单调律」1.93>1.56）；反之若稀释，S 会降（L1283 方向）。**该轴是真正的单变量设置轴**，与本波已关的所有表达式轴正交。
## 六十三、第四十批收批 + ★★★★★ 波次收尾总结（40 批 capstone）（§185–§186，2026-11-05 20:20）
- **W2a `GrWmroWP`（P2+market 外层）**：S 1.05 / F 0.41 / 2Y 1.17 / CW fail；4 闸，PPA 全过。
- **W2b `vR1ARm1z`（Z1+market 外层+门控）**：S 1.09 / F 0.43 / 2Y 1.40 / CW pass；3 闸，PPA 全过。
  - **★ 外层轴层级最终确认**：**country (1.38) > market (1.09) > none (0.93)**——两臂同向 −0.29 互证 ⇒ market 保留国别薪资结构噪声。
- **★★★★★ 波次收尾总结（40 批全量）**：
  - **天花板**：S 1.38（Z1/Xg9ajd60）/ 2Y 1.53（Xg9ajd60）/ F 0.63 ⇒ **距三道硬闸差 0.20 / 0.37 / 0.05**。
  - **14+ 条轴全部关闭**（详见台账 §186 ③）⇒ **水平面 7 组件经穷尽式单变量对照确认最优**。
  - **篮子 [X2, Z1, T1]** 互相关全达标，但正交腿强度差 0.91-0.99 不可达。
  - **PPA 候选 P2** 全达标（算子 7 / 字段 2 / S 1.34 / PPAC 0.0028），提交须用户 web UI。
  - **EUR 战役空间**：14 塔判决完毕，其它塔全判死 ⇒ **本赛季 EUR 无法再点亮任何塔** ⇒ 战役贡献 = 穷尽性文档 + 最优候选保留 + PPA 候选。
  - **最终候选池（按保留价值）**：Z1 `bl661vYq`（S1.38/2Y1.52）/ Xg9ajd60 `Xg9ajd60`（S1.38/2Y1.53/DD2.11% 最低）/ Y1 `MPYYNMW9`（S1.37/sub0.97）/ P2 `vR11bq0v`（PPA 全达标）/ T1 `RREE9Eo0`（正交腿）/ X2 `mLooKbe9`（正交腿/2Y1.60）。
## 五十三、第三十一批收批：FAST 档两条独立对照互证负向 + 设置轴关闭 + 第三十二批（职级结构新面）（§150–§151，2026-11-05 20:35）
- **A1 `RREEOZXz`（Z1 骨架 @ FAST，12 算子）**：**S 1.09 / F 0.50 / TO 8.64% / sub 0.68 / 2Y 0.78 / DD 3.26% / margin 6.04bp**；3 闸，CW + sub 双 pass、**PPA 全过**。
- **A2 `VkxxrwnA`（P2 骨架 @ FAST，7 算子）**：**S 1.13 / F 0.52 / TO 7.32% / sub 0.69 / 2Y 0.65 / DD 3.08% / margin 7.17bp**；4 闸（含 CW fail），sub pass、**PPA 全过**。
- **★ 单变量对照（只换中性化档）**：
  | 骨架 | STATISTICAL 档 | FAST 档 | ΔS | Δ2Y |
  |---|---|---|---|---|
  | Z1（带门控） | S 1.38 / 2Y 1.52 / sub 0.92 | S **1.09** / 2Y **0.78** / sub 0.68 | **−0.29** | **−0.74** |
  | P2（无门控） | S 1.34 / 2Y 1.31 / CW fail | S **1.13** / 2Y **0.65** / CW fail | **−0.21** | **−0.66** |
  ⇒ **两条独立对照同向 ⇒ FAST 档在本数据集全面负向 ⇒ 中性化档轴关闭**（对照台账 §2183「FAST 对 imbalance +0.45、对另一些 −0.50」⇒ **「必须逐信号 A/B」再获实证**）。
  - **机制**：本信号已是「行业内相对水平」（`group_zscore` 做过行业剥离）+ 门控选股 ⇒ **FAST 这类 PCA 快速中性化会叠加去相关、削弱有效截面差异**；与论坛《修 LOW_2Y_SHARPE 五个反直觉实测》第 5 条「换宇宙、换中性化修 2Y 越改越差」同型。
- **★ Fitness 缺口硬算（Z1 实测代入）**：`F = S×sqrt(|returns|/max(TO,0.125)) = 1.38×sqrt(0.026/0.125) = 0.629` ≈ 实测 0.63 ⇒ 公式精确。**要 F≥1.0**：S 抬到 1.58 需 returns ≥ **0.0501（+92%）**；S 停在 1.38 需 returns ≥ **0.0656（+152%）** ⇒ **returns 须接近翻倍，与 S 同源 ⇒ 只能靠换机制面，不是调参能解**。
- **已派第三十二批 `2LEHAX3ad5hlbJOoq6ee4D8`**（STATISTICAL/decay1/trunc0.04/nan OFF）：**S1 = `group_zscore(ts_backfill(vec_avg(position_seniority_level), 22), sector)`**（3 算子，职级结构面，alphaCount=1 从未作主信号）/ **S2 = `group_zscore(ts_backfill(vec_avg(position_experience_level), 22), sector)`**（3 算子，同族第二切片可用性探针）。
  - **机制含义**：薪资水平是人力资本的「价格」，**资历结构是「技能的形状」**（公司招聘组合的层级中位数高 ⇒ 高技能占比高 ⇒ 不可替代/议价能力强 ⇒ 未来收益高）⇒ 与水平面**正交**，若成立即为点塔第 2 颗正交腿。
- **候选池（38 骨架）**：Z1 **1.38**（3 闸/2Y1.52）/ Y1 1.37（3 闸/sub0.97）/ V2 1.35（3 闸/sub0.98）/ P2 1.34（4 闸/self0.0783）/ W1 1.32（3 闸/TO 最低）/ V1 1.30（3 闸）/ Z2 1.26（3 闸/2Y0.82）/ A2@FAST 1.13 / A1@FAST 1.09 · R2 1.05 · L3 0.86 · M1 0.85 · T1 0.67（self 0.018）/ X2 0.59（2 闸/2Y1.60/self 0.087）。


## 五十、第二十八批收批：V1 窗66 解 CW + V2 质量门控解 sub（§142，2026-11-05 19:35）
- **V1 `xArroVVn`（P2 + 窗66）**：**S 1.30 / F 0.57 / TO 6.46%（全波最低）/ sub 0.84 / 2Y 1.10 / margin 7.54bp（全波最高）/ DD 2.49%** —— **只差 3 闸**，**`CONCENTRATED_WEIGHT` pass（★CW 转过）**、**PPA 全过**。⇒ **CW 闸在窗 66 下转过**（窗22 时 fail）⇒ 印证「要 CW pass 用长回填窗」。
- **V2 `KPJJpvvg`（P2 + 员工数时序分位质量门控，12 算子）**：**S 1.35（本波最高）/ F 0.61 / sub 0.98（★逼近 1.0）/ 2Y 1.30 / TO 9.32% / DD 2.34%** —— 只差 3 闸，CW pass、**PPA 全过**。⇒ **论坛《E/P 价值因子的质量门控》在我们数据集上复现成功**：sub 0.88→0.98。
- **★ 门控的定位（重要）**：**门控是「从持仓构成上做减法」的杠杆（提 sub、降 PC），不是提 S 的杠杆**（S 1.34→1.35 基本中性）⇒ **提 S 仍要靠「外层 country 中性化 + 轻尾重塑 + 窗 66」**；**两者互补可同时用**。
- **算子上限拦截**：原计划 Y2（门控 + 双轴中性化 + 重塑 + ts_mean 双平滑）**13 算子超限 ⇒ 整批未派发** ⇒ **门控(5)+双轴中性化+重塑 已占满 12，再加任何平滑层即超限**。
- **已派第二十九批 `2kmrFFgeW4Fub40fJ1v3bNP`**：Y1 = V2 骨架 + 门控阈值 0.3→0.15（12 算子，放宽门控冲 sub 1.0）/ W1 = P2 骨架 + ts_mean(5) 平滑（8 算子，帖 A 根因①）。
- **候选池（32 骨架）**：V2 1.35（3 闸/sub0.98）/ V1 1.30（3 闸/TO 最低）/ P2 1.34（4 闸/self 0.0783）/ U1 1.12 · R2 1.05 · L3 0.86 · M1 0.85 · T1 0.67（self 0.018）/ X2 0.59（2 闸/2Y 1.60/self 0.087）。


## 四十九、P2 相关性里程碑 + CW 墙剩余两条解法（§141 前置，2026-11-05 19:20）
- **P2 `vR11bq0v`（本波首个过 near 线 1.2 的候选，S1.34）相关性预筛**：self **0.0783 pass**（红线 0.7，余量 0.62，pool 17，与已提交池几乎零重叠）；prod **两次调用均 120s 超时**（账号级单并发被占，未重复触发，留待下轮重查）；`submit_verdict` ⇒ **BLOCKED / FAILED_COUNT_RA:LOW_SHARPE,LOW_FITNESS,CONCENTRATED_WEIGHT,LOW_2Y_SHARPE / failed_ra=4 / failed_ppa=0 / submit_status=404**。
  - ⇒ **★ 瓶颈收敛**：**CW 闸是 P2 仅剩的「结构性」阻塞**（另三道 LOW_SHARPE/LOW_FITNESS/LOW_2Y_SHARPE 属「强度不足」类，可由提 S 顺带改善）；**self 已过、PPA 通道全过、塔位纯净 OTHER** ⇒ **障碍纯粹在 IS 强度**。
- **CW 墙剩余两条未试解法（帖 A 根因三分类未覆盖项；三闸 valid/valid/safe、单位零风险、算子 8/7 ≤12）**：
  - **W1 = 加 ts_mean 时间平滑（day=5）**（帖 A 根因①「行业分组结构问题 → ts_mean 时间平滑」，day<5 依帖 C）—— 本波尚未试过。
  - **W2 = 外层中性化轴 country→market**（EUR 有 `market` 组，cov 1.0）—— 若 country 仍残留国别噪声，market 轴可能进一步纯化。
- 在飞批次：第二十八批 `1upcIN3TN58W9eyHLMbXsBZ`（V1 = P2 + 窗66 冲 S；V2 = P2 + 员工数时序分位质量门控，论坛 EUR 本区实证可同时修 Sub/Ladder/PC）。


## 四十八、论坛结论与我们的实测并置：「结构多样化」而非「参数扫描」是降低自相关的最便宜杠杆（§141 前置，2026-11-05 19:20）
**论坛**《同一组字段的两套骨架:时序型与截面型结构,是降低自相关最便宜的杠杆》—— 核心原文：「当你想围绕一组字段做多个 alpha 时，**最容易犯的错是用『参数扫描』代替『结构多样化』：同样的表达式换换窗口、换换 decay，出来的变体互相之间的自相关高得吓人**。更有效的做法是**保持字段不变、结构换掉**（时序型 vs 截面型）。

**★ 与本波独立实测完全一致（互相印证）**：
- 我们 §130 实测：**6 条候选里 4 条是同一条水平面的参数变体**（rank / quantile-gaussian / quantile-uniform × 回填窗 22 / 66），两两互相关 **0.822–0.9865** ⇒ **参数扫描确实产生「高自相关变体」**，论坛结论在我们的数据上独立复现。
- 我们的解法与论坛一致：**改结构（换信息形态）而不是改参数** ⇒ 由此得到 SNR-tick 面（+0.1209）、流出 reversal 面（−0.0711 ~ −0.26）、SNR 显著性面等正交腿；**max_mutually_below_subset 从 1 升到 3**。

**门控备料（已过三闸 valid/valid/safe，单位零风险，各 10 算子 ≤12）**：
- **G1 = 水平面 D1（industry 轴·未整形·5 算子）+ 员工数时序分位质量门控** = `trade_when(greater(ts_rank(ts_backfill(vec_avg(employee_headcount), 66), 252), 0.3), group_zscore(ts_backfill(人均薪资, 22), industry), nan)`（10 算子）。
- **G2 = 流出面 X2（sector 轴·5 算子）+ 流出率时序分位质量门控** = `trade_when(greater(ts_rank(ts_backfill(vec_avg(employee_outflow_count), 66), 252), 0.3), -group_zscore(ts_backfill(流出率, 66), sector), nan)`（10 算子）—— 门控条件与信号腿同字段族但语义相反（低流出=基本面稳定）。
- ★ **门控必须套在简单骨架上**（D1g 6 算子 + 门控 = 11 可行；再叠条件就超 12）；且**门控是「从持仓子集入手」的思路，不是「再叠一层算子」**（与 winsorize/truncation 机制不同故不冗余）。


## 四十七、2Y / Ladder / PC 的 EUR 本区实证修复路径（§140 前置，2026-11-05 19:10）
**帖**《E/P 价值因子的质量门控：把 PC 从 0.70 压到 0.51 的实战记录（EUR/TOP2500/D1）》(article_id 43778032162199) —— **与我们的困境同型**：
- **起点症状**：纯 E/P（季度EPS/价格，subindustry 组内 zscore）IS Sharpe 1.94–1.96 / Fitness 1.30，**但 Sub-universe Sharpe 恒卡 0.96（limit 1.01）、IS Ladder 2Y 段只有 1.56（limit 1.58）、Prod Correlation 压在 0.6986–0.7004 临界线**。
- **试过但无效**：winsorize std / 窗口 / 中性化（COUNTRY/CROWDING/R&M）/ truncation / 两字段相乘 —— **均无法同时修复**。
- **★ 突破口（唯一有效解）**：「加一道『留存收益质量门控』：**`trade_when(greater(ts_rank(ts_backfill(retained_earnings,66),252),0.3), 原信号, nan)`**。逻辑上，留存收益是公司盈利累积的代理，门控**只保留『便宜且基本面扎实』的股票，从持仓构成上剔除低质量标的，而不是在权重层面做文章**。
- **★ 效果**：**PC 从 0.70 降到 0.5063、Sub-universe 升到 1.07、IS Ladder 3Y 到 2.21，全部 PASS**；同结构 4 个变体（回填 66/126/252、有无 winsorize）均全 PASS，PC 0.506–0.513。**「这条路径一个模拟都没多花」**（因为它在已有候选上直接加门控，而非重新扫参）。
- **★ 要点（可迁移）**：「**当 PC 高的根源是信号本身拥挤时，先想『该从哪个持仓子集入手』，而不是继续叠正交化算子**」。

### 对本波的映射（已预检，算子 ≤12）
- **Q1** = `trade_when(greater(ts_rank(ts_backfill(vec_avg(employee_headcount), 66), 252), 0.3), D1g, nan)`（**11 算子**）—— 用**员工数（规模/扩张代理）**的时序分位做质量门控，保留「扩张中」的公司。
- **Q2 变体（门控条件用薪资自身的时序分位）** = 13 算子 ⇒ **超上限，不派**；压缩版（门控用未整形序列）仍 13 ⇒ **内联重复是根因**。
- ⇒ **结论**：**「质量门控 + 轻尾重塑水平面」在算子上限 12 下不可共存**（D1g 骨架本身已 6 算子，门控再叠 ts_rank + ts_backfill 必然超限）⇒ 若要试门控，**必须用未整形的基准信号**（如 D1 = `group_zscore(ts_backfill(人均薪资,22), industry)`，5 算子 ⇒ 门控后约 10 算子）。
**★ 执行纪律**：门控类表达式**优先套在最简单的骨架上**（少算子），别套在最精巧的骨架上；且**门控是「从持仓子集入手」的思路，不是「再叠一层算子」**。


## 四十六、联合可行性闸账单 + 点塔矛盾点定位 + 分化轴方案（§133，2026-11-05 19:05）
### 46.1 联合可行性闸账单（TO 被钳 0.125 ⇒ 提 F 靠 returns，returns 与 S 同源）
| 腿 | gap_S | gap_F | gap_2Y | 闸数 | CW | returns 需增 | 增到位则 S 估到 | 可否同过 S+F |
|---|---|---|---|---|---|---|---|---|
| U1 rank·窗66 | 0.46 | 0.52 | 0.44 | 3 | pass | **2.15×** | 1.64 | **✅** |
| R2 重塑·窗22 | 0.53 | 0.59 | 0.41 | 4 | FAIL | **2.68×** | 1.72 | **✅** |
| Z2g 重塑·窗66 | 0.54 | 0.60 | 0.56 | 3 | pass | **2.69×** | 1.71 | **✅** |
| T1 SNR-tick | 0.91 | 0.79 | 0.61 | 4 | FAIL | 4.08× | 1.35 | ❌ 差 0.23 |
| X2 流出 reversal | 0.99 | 0.81 | 已过 | 2 | pass | 4.01× | 1.18 | ❌ 差 0.40 |

### 46.2 ★ 点塔矛盾点与解法
**矛盾**：三条水平面腿最容易推过闸（returns 只需增 2.15–2.69×），但**互相关 0.82–0.9865 无法共存**；正交的 T1/X2 需 returns 增 4.0× 以上、S 只估到 1.18–1.35 ⇒ **短期内不可达**。⇒ **三条腿不能都来自水平面**，必须有一条「S 够强 + 与水平面低相关」的中间态。

**解法：改变「与谁比」来分化同一条水平面**（分组轴 = 横截面对照基准，不同基准 ⇒ 不同经济含义 ⇒ 可能低相关）。三条已过三闸 valid/valid/safe、算子 5/5/12 ≤12：
- **D1** = `group_zscore(ts_backfill(人均薪资, 22), industry)` —— 相对**同行业**（而非 sector）。
- **D2** = `group_zscore(ts_backfill(人均薪资, 22), country)` —— 相对**本国**。
- **D3** = `group_zscore(subtract(group_zscore(人均薪资,22), industry), group_zscore(人均薪资,22), country)), sector)`（12 算子）—— **行业内相对 − 本国相对 的差**：显式剥离「国别薪资结构」后剩行业特异成分，**理论上是真正的正交化构造**，应与两条水平面腿都低相关。

★ **分化的经济含义**：D1 问「这公司在同行里薪资算高吗」（同行竞争视角）· D2 问「这公司在本国算高薪吗」（国别劳动力市场定价视角）· D3 问「剔除国别差异后，公司在行业内的相对位置」（纯行业特异成分）。三条是**三个不同的经济问题**，而非同一问题的参数变体。


## 四十五、macro27 官方用法帖取证（article_id 43615287467799, votes 31）—— 官方模板与执行面教训（2026-11-05 20:30）
**帖子**：《【Data】怎么用 macro：全市场同一个数，不要拿去 rank》—— 讲 macro 分类的「三条路」：**广播序列（体制）/ 招工（公司级）/ 持仓与进指（事件）**。

### 45.1 招工路（macro27）—— **官方推荐模板（本可直接使用）**
- 官方帖原话：「**macro27 是网上招聘。VECTOR，要先 vec_avg**」；「官方帖：招工增加相对同行，当作公司在扩张」。
- **★ 常见错法**：「`rank(vec_avg(mcr27_company_jobsactive))` —— **大公司岗位多，这是规模，不是扩张**」。
- **★ 官方建议模板**：「**比净增（新发减撤贴），或相对同桶/同行。岗位挂很久可能是招不到人或冻结编制**」：
  `j = vec_avg(company_jobs_created_count); r = vec_avg(company_jobs_removed_count); group_zscore(ts_backfill(j - r, 20), densify(industry))`
- **字段使用统计**（2026-09-19）：created_count 5 条 / removed_count 2 条 / 在岗天数 5 条 / **company_ajnet 1 条** / 中性化后 jobsactive_n 0 条 ⇒ **净增字段几乎没人用 ⇒ 是低竞争区**。
- **帖给论文**：**SSRN 3703948 / SSRN 3342669**（macro27 相关的两篇工作论文，待取全文核方向）。

### 45.2 ★ 执行面教训（评论 `JR57542` / `ZH41150`，对换集派发同样适用）
- **体制变量当开关用，不当因子输入**：「宏观序列是会被重述的，今天看到的上季度值和当时实况可能不同，**直接对序列做差分会把『新闻』和『重述』搅在一起**」⇒ 偏爱修订稳定的变换（方向/档位而非精确值）。
- **体制翻转需迟滞**：「当体制指标在零附近震荡时，全书会跟着来回翻，换手被体制噪声而不是信号驱动」⇒ **给翻转加迟滞（变化幅度超过一个带才认翻），或把体制量化成几个离散档位**。
- **公司级字段与广播序列要分开处理**：「公司级的招聘净增数据倒是可以做同行相对值，比如**除以行业内均值再 rank**，这类公司级字段和广播序列**正确用法完全不同**」。
- **分类标签不能替你做研究**：「**macro38 技术评分混进 macro 类这个发现很关键，按 category 找字段之前先验证语义，别让分类标签替你做研究**」⇒ 与本项目「semantic_family 自动归类会错、必须读 description」同源。

### 45.3 对本波的影响
- **H3 备料（流入/流出比）方向正确但需修正**：帖内官方做法是 **created − removed 的差分**（净增）而不是**流入/流出之比**（比值在 removed=0 时会爆，且量纲上不是「扩张强度」而是「相对存量比」）；⇒ **H3 改为官方差分式**：`group_zscore(ts_backfill(vec_avg(created) - vec_avg(removed), 20), densify(industry))` 的 workforce 等价版。
- ⚠ **单位纪律**：官方式是 `j - r`（两个 count 相减 ⇒ 量纲一致，安全）；**不要写成比值**再乘常数。
- ★ macro27 属 **MACRO 塔（0/3，差 3 颗）** ⇒ 即使跑出好信号也**不点亮 OTHER**；它的价值是**提供一个与 workforce 面正交的「招聘面」机制腿**（流入 vs 流出 vs 薪资水平三者信息形态不同），可作为点塔第三/四腿的候选来源。


## 四十四、新机制面备料（受 §130 约束：不再在水平面加参数臂）（2026-11-05 20:20）
**派发约束（来自 §130 互相关矩阵）**：水平面已被 R2/Z2g/U1/R1 占满（两两 0.82–0.9865）⇒ **下一批只派「换机制面」的臂**。三条备料（已过三闸 valid/valid/safe、单位零风险、算子 4–5 ≤12）：
| 编号 | 新机制面 | 表达式 | 算子 | 预期 |
|---|---|---|---|---|
| **H1** | **去分组的纯时序形态** | `ts_rank(ts_backfill(人均薪资, 66), 252)` | 5 | **与 group_zscore 族信息形态不同 ⇒ 预期相关显著低于 0.82**；「薪资相对自身 252 日常态的位置」本身是独立机制 |
| **H2** | **流出腿的新形状（去分组）** | `-ts_rank(ts_backfill(流出率, 66), 252)` | 5 | 流出腿的时序形态，与水平面正交；若 S 显著可为点塔第三腿提供比 X2 更强的替代 |
| **H3** | **招聘净扩张（流入/流出之比）** | `group_zscore(divide(vec_avg(employee_incoming_count), vec_avg(employee_outflow_count)), sector)` | 4 | **全新机制面**：净招聘强度（招聘扩张 vs 收缩），与已测的「流出率」「薪资水平」都不同；论坛《招聘变化与业务扩张》核心 idea 的直接实现 |

**H3 的机制依据与注意事项**：论坛《【Alpha Idea】招聘变化与业务扩张：hiring_trends 在 USA 市场的因子化尝试》(article_id 43322749748503) 的核心结构就是「招聘读数 → 相对基期变化率 → 行业内比较」；本波 H3 用**流入/流出之比**度量「招聘净扩张强度」，与 M9（`incoming/headcount` 行业相对，S0.33 已证在 EUR 不成立）**信息形态不同**（比值 vs 水平），仍值得独立测一次。⚠ **单位纪律**：`divide(count, count)` 是无量纲比率，**不触发** VERIFY 量纲冲突（与 `add(字段,常数)` 不同）。


## 四十三、六条候选完整互相关矩阵：水平面这一腿只有 1 个名额（§130，2026-11-05 20:12）
**6 条候选 15 对互相关（4 年期）**：
| 对 | 相关 |
|---|---|
| **R2 ↔ Z2g**（同骨架，窗 22 vs 66） | **0.9865** |
| Z2g ↔ R1（uniform driver） | 0.9792 |
| R2 ↔ R1 | 0.9662 |
| R2 ↔ U1（rank 版） | 0.8681 |
| Z2g ↔ U1 | 0.8616 |
| U1 ↔ R1 | 0.8220 |
| R2 ↔ T1（SNR-tick） | +0.1209 |
| Z2g ↔ T1 | +0.1237 |
| U1 ↔ T1 | +0.1204 |
| R1 ↔ T1 | +0.1280 |
| **R2 ↔ X2（流出 reversal）** | **−0.2520** |
| Z2g ↔ X2 | −0.2600 |
| U1 ↔ X2 | −0.2125 |
| R1 ↔ X2 | −0.2579 |
| T1 ↔ X2 | −0.0711 |

⇒ **max_mutually_below_subset = [RREEKQne(R2), RREE9Eo0(T1), mLooKbe9(X2)]（3 条）**，是唯一可共存组合。
⇒ **★ 结构性结论**：6 条候选里 **4 条是同一条腿的变体**（水平面：rank/quantile-gaussian/uniform × 窗 22/66 ⇒ 两两 0.82–0.9865）⇒ **「水平溢价」腿只能取 1 条入篮**；另外两条腿必须来自 **SNR 显著性面（T1）** 与 **流出 reversal 面（X2）**。⇒ **三条腿的名额是稀缺资源，挖掘预算应按「机制面」而非按「参数」分配**。
⇒ **派发约束**：**不要再在水平面加参数臂**（窗口/driver/sigma/轴的任何组合都落在 0.82+ 相关区、浪费槽位）；只派「① 流出面加杠杆（E1 在飞）② 新机制面（去分组的时序形态 G2 / macro27 招聘面）」。


## 四十二、闸缺口账单更新（含 U1 完整数据）+ 降相关备料（§130 前置，2026-11-05 20:05）
### 42.1 闸缺口账单（重算，含 U1 完整指标）
| 腿 | S | 差 1.58 | F | 差 1.0 | 2Y | 差 1.58 | 闸数 | 公式验算 | TO 钳下限 | S→1.58 需 returns | 倍数 |
|---|---|---|---|---|---|---|---|---|---|---|---|
| **U1** rank·窗66 | **1.12** | **0.46** | 0.48 | 0.52 | 1.14 | 0.44 | 3 | 0.4835 | 是 | 0.0501 | **2.15×** |
| Z2g 重塑·窗66 | 1.04 | 0.54 | 0.40 | 0.60 | 1.02 | 0.56 | 3 | 0.4012 | 是 | 0.0501 | 2.69× |
| R2 重塑·窗22 | 1.05 | 0.53 | 0.41 | 0.59 | **1.17** | **0.41** | 4 | 0.4061 | 是 | 0.0501 | 2.68× |
| T1 SNR-tick | 0.67 | 0.91 | 0.21 | 0.79 | 0.97 | 0.61 | 4 | 0.2099 | 否 | 0.0645 | 4.08× |
| X2 流出 reversal | 0.59 | 0.99 | 0.19 | 0.81 | **1.60** | **已过** | **2** | 0.1866 | 是 | 0.0501 | 4.01× |

**★ 杠杆排序（闸数少优先，再看综合缺口）**：X2（2 闸，缺口 1.80）→ **U1（3 闸，综合 1.42 最小）** → Z2g（3 闸，1.70）→ R2（4 闸，1.53）→ T1（4 闸，2.31）。
⇒ **U1 综合缺口最小（1.42）且 S 最高（1.12）**，但它与 Z2g 互相关 **0.8616** ⇒ **二者只能取其一**；**取 U1 则点塔第三腿须另找，取 Z2g 则 U1 出局**。R2（重塑·窗22）与 Z2g（重塑·窗66）是**同骨架不同回填窗**，其互相关须实测（预计仍 >0.5）⇒ **它们是同一腿的两个窗口变体，不是两条腿**。

### 42.2 降相关备料（已过三闸 valid/valid/safe、算子 5/5/6 ≤12）
目标：**造一条「S 接近 U1/Z2g 但与它们相关低」的臂**，作为点塔第三/第四条腿。手段 = 改**形状**（而非参数）：
- **G1** = `group_zscore(ts_backfill(人均薪资, 66), subindustry)`（5 算子）—— 换分组轴（group_zscore 形态已知 subindustry 弱，但 rank 形态下未测）。
- **G2** = `ts_rank(ts_backfill(人均薪资, 66), 252)`（5 算子）—— **去分组、纯时序化**：与 group_zscore 系列的信息形态不同 ⇒ 预期相关显著更低。
- **G3** = `group_zscore(winsorize(ts_backfill(人均薪资, 66), std=3), sector)`（6 算子）—— 轻度整形（winsorize vs quantile 的对比）。

★ **注意**：帖 B 已实证 winsorize 对 ts_delta 长尾无效，但**这里不是给 ts_delta 用**（是给存量水平用），故仍值得测一次作为形状对照。


## 四十一、闸缺口账单 + 下一批杠杆优先级（§128 前置，2026-11-05 19:58）
### 41.1 Fitness 公式验算（三条腿全部吻合 ⇒ 可用于派发前估算）
公式 **`Fitness = S × sqrt(|returns| / max(TO, 0.125))** ⇒ Z2g 计算 0.4012 vs 实测 0.40；T1 0.2099 vs 0.21；X2 0.1866 vs 0.19 ⇒ **可靠**。

| 腿 | S | 差 1.58 | F | 差 1.0 | 2Y | 差 1.58 | 闸数 | TO 被钳下限? | S→1.58 时所需 returns | 倍数 |
|---|---|---|---|---|---|---|---|---|---|---|
| Z2g | 1.04 | **0.54** | 0.40 | 0.60 | 1.02 | 0.56 | 3 | 是(6.27%) | 0.0501 | **2.69×** |
| T1 | 0.67 | 0.91 | 0.21 | 0.79 | 0.97 | 0.61 | 4 | 否(16.1%) | 0.0645 | 4.08× |
| X2 | 0.59 | 0.99 | 0.19 | 0.81 | **1.60 已过** | **−0.02 已过** | **2** | 是(9.64%) | 0.0501 | 4.01× |

**★ 核心结论**：三腿 TO 均被钳在 0.125 下限附近 ⇒ **提 Fitness 只能靠提 returns**，而 **returns 与 S 同源** ⇒ **「把 S 推过 1.58」与「让 F 过 1.0」是同一个动作**；且 **S 到 1.58 后 returns 只需增 2.7–4.1×**（与 S 提升同量级）⇒ **不是不可逾越**。**⇒ 下一轮全部预算集中在「提 S」，不要为 Fitness 单独找杠杆。**（修正此前「Fitness 缺口大需单独攻」的判断。）
### 41.2 下一批杠杆优先级（六条全部 operator_audit safe、单位零风险、算子 ≤12，已预检）
| 优先 | id | 表达式要点 | 算子 | 理由 |
|---|---|---|---|---|
| **1** | **E1** | `-group_zscore(ts_backfill(quantile(流出率, driver="gaussian"), 66), sector)` | 6 | **★ 流出面套轻尾重塑：X2 只差 2 闸（LOW_SHARPE+LOW_FITNESS）、2Y 1.60 已过 ⇒ 提 S 的边际收益最大** |
| 2 | A1 | `group_zscore(ts_quantile(回填22, 66, driver="gaussian"), sector)` | 6 | 水平面换 ts_quantile（rank 的分布整形版） |
| 2 | F1 | `-group_zscore(divide(ts_quantile(回填22,66,driver="gaussian"), ts_std_dev(回填22,22)), sector)` | 12 | **唯一能一次引用带整形的 SNR 路径**（绕开算子墙） |
| 3 | B1 | Z2g 骨架只换 sigma=0.5 | 6 | 参数单变量（论坛 cauchy 解法同款 sigma） |
| 3 | C1 | Z2g 骨架回填窗 66→22 | 6 | 参数单变量（测回填窗在重塑形态下是否仍有效） |
| 4 | D1 | Z2g 骨架 + truncation 0.02 | 6 | 收窄截断对照（论坛预期负向，仅作对照） |

**派发纪律**：每批 2 条、并发 2、每条只改一个变量；**先派 E1 + A1**（收益最高的两条）；收批后按闸缺口账单更新候选池。


## 四十、第二十二批备料 + 一个结构性不可达结论（2026-11-05 19:50）
### 40.1 ★ 结构性不可达：「重塑 + SNR 叠加」在算子上限 12 下不可达
想把两条已验证路径叠加（Z2g 的轻尾重塑 + T1 的 SNR 分子），但 **FASTEXPR 无 let/变量绑定 ⇒ 同一底层信号必须内联重复书写**：
- **P1 原版** = `-group_zscore(divide(ts_rank(ts_backfill(quantile(RAW, driver="gaussian"),22),66), ts_std_dev(ts_backfill(quantile(RAW, driver="gaussian"),22),22)), sector)` ⇒ **14 算子 / 284 字符**（RAW 内联 2 次、quantile 写 2 次）。
- **P1 压缩版**（分母改用原始序列 std_dev）⇒ **13 算子**。
- **P1b**（分子 ts_zscore 替代 ts_rank）⇒ **13 算子**。
- **P1d**（分子侧改用 winsorize 替代 quantile）⇒ **13 算子**。
⇒ **四种写法全部 ≥13，均超上限 12** ⇒ **该路径结构性不可达，不是「还没试够」**。
★ **通用教训**：**任何需要「同一子表达式内联两次以上」的组合，在算子上限 12 下基本不可达** ⇒ 设计模板时应先数「子表达式被写了几次」：写 1 次的组合（水平面 + quantile）可行；写 2 次的组合（SNR + 重塑）超限。⇒ **优先选「单次引用 + 轻量整形」的算子链**，把重塑放在唯一可放的位置。

### 40.2 第二十二批备料（已过 operator_audit safe、单位零风险、算子 6/6 ≤12）
- **P2** = `group_zscore(ts_backfill(quantile(RAW, driver="gaussian", sigma=0.5), 66), sector)`（6 算子）—— Z2g 骨架**只换 sigma 0.5**（论坛 cauchy 解法用的 sigma 值），测轻尾 driver 下 sigma 是否仍有作用。
- **P3 = ts_quantile 路径**（已预检 operator_audit safe、算子 12/6）：
  - **S1** = `-group_zscore(divide(ts_quantile(ts_backfill(RAW,22), 66, driver="gaussian"), ts_std_dev(ts_backfill(RAW,22),22)), sector)`（12 算子）—— SNR 分子由 ts_rank 换 ts_quantile（分布整形版）。
  - **S2** = `group_zscore(ts_quantile(ts_backfill(RAW,22), 66, driver="gaussian"), sector)`（6 算子）—— 水平面由 rank 换 ts_quantile。
  - ★ 价值：这是**唯一能在不内联重复的前提下用到分布整形的 SNR 路径**（ts_quantile 自带整形、只需一次引用）⇒ 若 S1/S2 有效，即可在 SNR 面引入轻尾整形而绕开算子墙。

### 40.3 Z2g 与 U1 的互补性（决定点塔的三条腿怎么选）
| 指标 | U1 (rank 版) | Z2g (轻尾重塑版) |
|---|---|---|
| Sharpe | **1.12** | 1.04 |
| Turnover | 8.79% | **6.27%（全波最低）** |
| Drawdown | 2.32% | **1.86%（全波最低）** |
| margin | 3.96bp | **5.94bp（全波最高）** |
| CW / sub 闸 | 双 pass | 双 pass |
| PPA | 全过 | **全过** |
| 闸数 | 3 | 3 |
⇒ 总 S 差 0.08，但风险画像 Z2g 全面更优 ⇒ **两者是互补的两条腿，不是同一信号的两个版本**（待互相关验证）。


## 三十九、平台算子官方定义取证（get_operators，103 个算子）（§126 前置，2026-11-05 19:40）
**`quantile`（Cross Sectional）**：定义 `quantile(x, driver = gaussian, sigma = 1.0)` —— 「Ranks and shifts a vector of Alpha values, then applies a chosen statistical distribution (**gaussian, cauchy, or uniform**) to reduce outliers」。⇒ **driver 的三个合法值由平台官方定义确认：gaussian / cauchy / uniform，默认 gaussian** ⇒ 我们用的 `driver="gaussian" / `driver="uniform" **语法完全合法**，`preflight`/`validate` 的 unknown_fields 属**平台字段检查器把 driver 字符串当字段名的缺陷**（论坛多帖实证该语法可跑）⇒ 以 operator_audit safe + 实跑为准。
**`ts_quantile`（Time Series）**：定义 `ts_quantile(x, d, driver="gaussian")` —— 「Calculates the **ts_rank** of the input and **transforms it using the inverse cumulative distribution function (quantile function) of a specified probability distribution**」⇒ **它是 ts_rank 的分布整形版：保留排序 + 把秩映射到指定分布**（帖 B《ts_quantile居然可以降低pc！！》的路径）。
**`winsorize`（Cross Sectional）**：定义 `winsorize(x, std=4)` —— 「limits values … within a specified number of standard deviations from the mean, reducing the impact of extreme outliers. **Note: recommended…**」（官方描述含推荐用法说明，可进一步读 /operators/winsorize 文档）。
**其它相关算子**：`ts_std_dev(x, d)`、 `ts_rank(x, d, constant = 0)`。

**⇒ 三条可直接比较的分布整形路线（按「是否保留幅度信息」排序）**：
1. `quantile(x, driver=gaussian)` —— 横截面秩 + 轻尾分布，**保留排序与中间结构**（帖 B：轻尾后 truncation 杠杆复活）。
2. `ts_quantile(x, d, driver=gaussian)` —— 时序秩 + 轻尾分布整形，**可替代 ts_rank** 塞进 SNR 分子（S1 备料）。
3. `rank(x)` —— 纯秩，**丢掉幅度信息**（帖 B 评论 FF45555 不推荐作首选）。

**已备料（operator_audit safe、单位零风险、算子 12/6 ≤12；preflight/validate 的 driver 误报照旧留痕）**：
- **S1** = `-group_zscore(divide(ts_quantile(回填22, 66, driver="gaussian"), ts_std_dev(回填22, 22)), sector)`（12 算子）—— SNR 分子由 ts_rank 换 ts_quantile。
- **S2** = `group_zscore(ts_quantile(回填22, 66, driver="gaussian"), sector)`（6 算子）—— 水平面由 rank 换 ts_quantile。


## 三十八、SNR 模板的两篇后续讨论：0/0 区间的结构坑 + 真信号判别设计（§125 前置，2026-11-05 19:25）
**帖 D**《【方法笔记】比值型 Alpha 的 0/0 区间：divide(ts_zscore, ts_std_dev) 的一个结构性坑与组内分母收缩修法》(article_id 43525418528535, votes 21) —— 直接续 SNR 原帖：
- **问题**：`b = divide(ts_zscore(a,W_long), ts_std_dev(ts_zscore(a,W_short),W_vol))` 形式上像 t 统计量但**严格说不成立**——分子已把 a 除以自己的滚动标准差，分母又是「短窗 z-score 的滚动波动」，**两者对同一序列做同类运算、并不独立**。对 `ts_backfill` 后的**阶梯状季频序列**（我们的薪资字段正是月度更新 ⇒ 正是阶梯状），财报跳跃后窗口滚动，**分子分母会同向衰减**：序列趋稳时 `ts_zscore`→0、其滚动波动也→0 ⇒ 出现 **0/0 区间**，此区间比值由数值精度而非信号决定 ⇒ **产生与「显著性」语义相反的伪尖峰，且恰好集中在「长期不动」的稳健公司上**——不是 winsorize 能处理的那类横截面极端值。
- **修法（把鉴别与治理合一）：分母组内收缩** `denom' = (1−λ)·denom + λ·group_mean(denom, G)`，λ 取 0.3~0.5。双重效果：① 给近零分母一个**组内先验下限**，0/0 区间被结构化抑制（**比收紧 truncation 更对症——truncation 截分子端，管不到分母端**）；② 组内公共部分恰是「低波动/信息不确定性」异象的代理（Zhang 2006 信息不确定性、Ang et al. 2006 低波动异象），剥离后剩余才是**个股特异性噪音**。
- **判别实验**：换成分母收缩后重跑 IS ⇒ 若 Sharpe 仍在，说明信号确实来自「显著性」；若明显衰减，说明原收益有相当部分**借了低波异象的光**。

**帖 E**《【检验设计】把参数当实验变量：窗口-系数面如何区分"真信号"与"标签贴牌」(article_id 43525464033303, votes 21) —— 同系列续篇：
- **核心**：比值型模板的可信度取决于**分母窗口选在哪**（分母决定收益来自「显著性」还是「稳健公司标签」）；**单点调参很容易在某个窗口组合上刷出高点却无法说明真假** ⇒ 要**把参数当实验变量**：固定 W_long，扫描 (W_short, W_vol) ∈ {5,22,66,126} × {22,66,126,252} 网格。
- **三种可识别曲面形态**：① Sharpe 对 W_short 单调、对 W_vol 不敏感 ⇒ **分母只在给「短期噪音标签」贴牌，收益吃「近零分母 = 稳健公司」的低波异象边**（形态一 = 伪信号）；② **峰值在中等窗口非端点** ⇒ 存在「噪音估计采样误差 ↔ 滞后」的真实权衡 = **显著性代理在起作用**（形态二 = 真信号）；③ 整面平坦 ⇒ 比值结构对参数不敏感。
- **delay 0/1 对照**：同表达式在 delay 0 与 delay 1 各跑一次，比较 Sharpe 差的方向与幅度；delay 0 显著更高而 delay 1 塌掉 ⇒ 信号主体是「公告日当天的信息反应」。**窗口曲面 + delay 差两种对照组合 = 对「真显著性」的一票否决制检验**。

**★ 我们已有的初步判别（无需新批次，用已实测臂反推）**：
- T1/V2 = `divide(ts_rank(回填22,66), ts_std_dev(回填22,22))` ⇒ S +0.67 / −0.67（**分母 W_vol=22**）。
- Y1 = `divide(ts_zscore(回填22,252), ts_std_dev(ts_zscore(回填22,66),66))` ⇒ S −0.04（**分母内层带 zscore + W_vol=66**）。
- U1' = T1 的回填窗改 66 ⇒ S 0.66（几乎不变）。
⇒ **分母结构与窗口的变动对 SNR 面结果影响巨大（0.67 → −0.04）** ⇒ 倾向帖 E 的**形态二（真显著性）**而非形态一（低波标签借光）；但仍需网格扫描与分母收缩对照才能定论。

**已备料（下一批，每条单变量；预检 valid/valid/safe，算子 12/12，单位零风险）**：
- **C1 = W_vol 22→66** = `-group_zscore(divide(ts_rank(回填22,66), ts_std_dev(回填22,66)), sector)` —— **只改分母噪声窗**。
- **C2 = W_long 66→22** = `-group_zscore(divide(ts_rank(回填22,22), ts_std_dev(回填22,22)), sector)` —— **只改分子偏离窗**。
- **★ 分母组内收缩臂（帖 D 修法）**：
`denom' = (1−λ)·denom + λ·group_mean(denom, sector)` —— FASTEXPR 无 let 绑定 ⇒ 需把 denom 内联两次，**算子数会超 12 上限**，须先做等价压缩设计（见 §129 备料）。


## 三十七、CONCENTRATED_WEIGHT 阻塞的解法取证（论坛三帖，含可直接迁移的分布重塑法）（§125 前置，2026-11-05 19:10）
**我们的现状**：U1/X1（水平面）与 T1（SNR-tick 面）都卡 `CONCENTRATED_WEIGHT`（U1 是 3 闸之一，T1 是 4 闸之一）⇒ **CW 闸是当前点塔的最后一道结构障碍**。论坛三帖给出成套解法：

**帖 1**《【经验分享】MEA地区CONCENTRATED_WEIGHT 阻塞解决记录》(article_id 41625344232343, votes 60, 7 评论) —— 完整排查记录：
- **无效方案 1：`ts_backfill`** —— 「只填有限天数的缺口，新上市或断档超过 lookback 的股票仍无完整历史，delta 依然 NaN，覆盖度没有本质改善」。
- **无效方案 2：`group_count`** —— 「是截面函数，不能跨日期统计；且若把 sector 覆盖差的保留、覆盖好的丢弃，持仓反而更集中（long 从 150 降到 101）」。
- **无效方案 3：`winsorize`** —— 「裁剪的是 raw 值的极端值，但 ts_delta 算的是同比变化；两个 winsorize 后的值相减仍可以很大（去年 100 到今年 200 = 变化 100%）」。
- **有效方案：`quantile(x, driver="cauchy", sigma=0.5)`** —— 「**不试图增加覆盖度，而是直接重塑分布**：先排秩丢掉原始数值，再用 Cauchy 逆函数把 [0,1] 秩映射回完全受控的分布，无论输入分布长什么样，输出都是同一个 Cauchy 分布」。实测 baseline(winsorize) CW FAIL S1.88/F1.86 → **quantile+ts_delta CW PASS S2.30/F2.41**。
- **★ 顺序至关重要**：「`quantile` 放 `ts_delta` **前面**效果更好 —— 先重塑分布再算变化」：`ts_delta(quantile(EPS,cauchy),252)` → S2.30，而 `quantile(ts_delta(EPS,252),cauchy)` → S2.06（也能过，但信号损失大）。
- **根因三分类（可复用的判据）**：① 行业分组结构问题（group_rank 小行业）→ `ts_mean` 时间平滑；② **信号值分布极端问题（ts_delta 长尾）→ `quantile` 分布重塑，比 winsorize 彻底得多**；③ 覆盖度不足问题（ts_delta 窗口期缺失）→ 增加覆盖度的思路（backfill/group_count）都有限。

**帖 2**《【实证】CW 墙的物理学：cauchy 重尾才是 Crowding 的主因，换轻尾 driver 才能把 truncation 杠杆救回来》(votes 23) —— **进一步收敛解法**：cauchy 是**超重尾**分布，尾部权重天然把横截面质量推向极端 ⇒ 这才是 CW 的来源；**换成 gaussian/uniform 轻尾 driver 后，truncation 杠杆直接复活**（「cw4 里压不动 cauchy 超重尾的 trunc，在 gaussian 轻尾下 0.05 就够」）。⇒ **轻尾 driver（gaussian/uniform）比 cauchy 更适合解 CW 墙**。

**帖 3**《Weight concentrated问题的一些解决方法》(article_id 35141695661975, votes 20) —— 四条方案清单：① 调 Truncation；② `ts_backfill` / `group_backfill`；③ `ts_mean(alpha, day)`（day 一般 <5）；④ `trade_when(group_count(alpha,market)>40, alpha, -1)`。

**评论 `FF45555` 的两条补充**：① **`quantile(cauchy)` 与 `rank` 的细微差别** —— 两者都能解 CW，但 `rank` 把分布压成均匀、**丢掉幅度信息**；`quantile(cauchy)` 只压缩两端胖尾、**保留原本排序和中间结构**，幅度信息对信号重要时 cauchy 更保真。② **前置检查**：「**别等提交才看 CW —— IS 里就有 CONCENTRATED_WEIGHT 这项，早期瞄一眼，如果 borderline 直接上分布重塑，而不是先折腾 ts_backfill/group_count**」。

**★ 对本波的直接应用（备料）**：
- **Z2** = `group_zscore(ts_backfill(quantile(人均薪资, driver="gaussian"), 66), sector)`（6 算子）—— 水平面 U1 的**轻尾 driver 重塑**（若 gaussian 不可用则试 uniform）；目的是让 truncation 杠杆复活 + 保住幅度信息。
- **Z1** = SNR-tick 面套 quantile 重塑（原帖骨架 14 算子超上限 ⇒ **必须把重塑结果复用**，FASTEXPR 无 let 绑定 ⇒ 只能对底层信号重塑一次，代价是重复书写，故算子数偏高；备选：先重塑再 SNR 会超算子上限 ⇒ **优先在水平面用 Z2**）。
- **平台校验注意**：`preflight_expressions` 与 `validate_expressions` 对 `driver="gaussian"` / `driver="uniform"` / `driver="cauchy"` **一律误报 unknown_fields**（把 driver 字符串当字段名；论坛两帖均用该语法且实际可跑）⇒ **该误报不构成拒绝理由，以 operator_audit safe + 实跑结果为准**（本项目纪律：三闸须过，但遇到已知工具缺陷须留痕而非直接弃用）。



## 三十五、macro27 三个正交面备料齐备（岗位存量 / 净扩张 / 招聘时长）（§124 前置，2026-11-05 18:50）
**论坛补充取证**：《和AI学点手搓小知识-vec操作符解析》(votes 48, 22 评论) —— 同样以 macro27 为教材，补充机制提示：「**要『招到有多快』，更接近时长字段（岗很快消失）**」⇒ 岗位挂起时长 = **招聘难度的直接度量**，是与「薪资水平」「岗位存量/净扩张」完全正交的第三个经济机制面。
**已备料（三闸 valid/valid/safe、单位零风险、算子 2–3）**：
| 编号 | 机制面 | 表达式 | 算子 |
|---|---|---|---|
| N1 | 岗位**存量**的月度变化 | `group_rank(ts_delta(vec_sum(num_jobs_active), 22), industry)` | 3 |
| N2 | 招聘**净扩张**（created−removed） | `group_rank(vec_sum(mcr27_company_ajnet), industry)` | 2 |
| **D1** | **招聘时长（开放中岗位挂起天数）** | `group_rank(vec_avg(avg_days_job_posting_active), industry)` | 2 |
| **D2** | **招聘时长（已关闭岗位挂起天数）** | `group_rank(vec_avg(avg_days_job_posting_closed), industry)` | 2 |
- **时长面必须用 `vec_avg`**（帖内规则二）：「10 个岗各挂 5 天，sum 出来 50，不等于 50 天难招」⇒ D1/D2 用 vec_avg 正确。
- **机制含义（可写进 alpha description）**：D1 岗位长期挂着 = **岗位难招/技能稀缺**（需求强但供给不足）⇒ 可能是**高技能、高议价能力**公司；D2 已关闭岗位曾挂很久 = **招聘失败或撤岗**（负面信息）。两者方向相反，是**同一字段族的两个对立面**。
- **同源定位**：macro27 三面（岗位存量/净扩张/时长）**全部与 workforce 薪资面正交** ⇒ 若派发，归因须标注为「**招聘面**」，不可与 workforce 的「薪资面」混算。



## 三十三、macro27（MACRO 塔唯一合法未测集）方法论取证 + 备料（§123 前置，2026-11-05 18:37）
**论坛帖**：《vec_sum 还是 vec_avg：拿到 VECTOR 字段，先回答这个问题再写表达式》(article_id 43444585257879, votes 15)。**直接以 macro27（招聘）为教材**，给出 VECTOR 字段的完整处理规则：
- **切片认知先行**：macro27 一条记录带 `mcr27_zip`、`mcr27_country` ⇒ 切片是「地点/岗位」**不是「公司一天一个值」**；不先压掉这叠记录，表达式直接废（类型链没接上，不是字段坏了）。
- **规则一：计数类用 `vec_sum`，别用 `vec_avg`**。`num_jobs_active` 是「在招岗位条数」，你要的是公司级「一共挂了多少岗」——「开 20 个点各招 1 人 vs 开 2 个点各招 1 人，avg 一样、sum 差 10 倍」；`vec_max` 更歪（只留最忙的一个 zip，把全国扩张整个丢掉）。
- **规则二：时长类才轮到 `vec_avg`**（`mean_days_job_active` 是「岗挂了多久」，求和没有经济含义）。
- **规则三：别看到字段名带 company 就当 MATRIX 用** —— `mcr27_company_jobsactive` 语义是公司级计数但类型仍是 VECTOR，照样要先 `vec_*`。
- **规则四：稀疏字段做除法要防除零**（`num_jobs_removed` 某天全 0 会炸回测）⇒ **但本项目单位纪律禁 `add(字段,常数)`（unitHandling=VERIFY 下量纲冲突）**，改用纯差分或无量纲比率。
- **规则五：流与存量是两个不同的 alpha**：`num_jobs_active` 是库存；`num_jobs_created/removed` 是流。created 比 removed 大是扩张，但 **removed ≠ 招到了人**（可能录用/撤岗/过期）⇒ 那个比值衡量的是「**岗位流水的净扩张**」不是雇佣速度；`ts_delta(vec_sum(num_jobs_active), 22)` 是「库存一个月变了多少」，与 created−removed 在理想记账下接近，**实际两路常对不齐 ⇒ 恰好说明流与存是两个不同的 alpha**。
- **规则六：截面比较用 `group_rank(..., densify(industry))`** —— 「招聘是行业现象，零售旺季大家一起招；比『相对同行多招还是少招』才有信息，绝对岗数基本是市值和行业的代理变量」。
**已备料（预检 valid/valid/safe，单位零风险，算子 2–3）**：
- **N1** = `group_rank(ts_delta(vec_sum(num_jobs_active), 22), industry)`（3 算子）—— 岗位**存量**的月度变化，行业内相对。
- **N2** = `group_rank(vec_sum(mcr27_company_ajnet), industry)`（2 算子）—— 招聘**净扩张**（created−removed）水平，行业内相对。
- **同源纪律**：macro27 与 workforce_flow_skills 同源（都是招聘/职位数据）⇒ 派发前须核「N1/N2 的机制面是否已被 workforce 面覆盖」——workforce 已测的是**薪资水平/薪资变化/员工流出**，macro27 是**岗位存量/岗位净扩张**，机制面不同 ⇒ 可派，但归因中须明确区分为「招聘面」而非「薪资面」。
























