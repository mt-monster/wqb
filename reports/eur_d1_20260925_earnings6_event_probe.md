# EUR D1 earnings6 实际业绩与预告精度研究（wave255）

**Dataset**: earnings6
**Region**: EUR
**Delay**: 1


## S-PRE与S0证据

2026-09-25，DB最新wave254已closed/FAIL；本任务57条已完成、0/10合格。本轮先复查135条死路，未找到earnings6精确历史实验。名似盈利预测的analyst_earnings_ibes实际主要为event-masked OHLCV，已有wave125弱结果，排除其同型重试。

earnings6实时EUR/TOPCS1600/D1数据集coverage=.8203，66字段，alphaCount1608、userCount572。S0评分.6598、auto_tier=excluded、hard_excluded=false，属于全数据集拥挤软先验。拟仅对四个真实数字字段开4条有界机制/对照实验；需将覆盖写入s0_whitelist，不改提交阈值。EPS主字段71/54用户，只验证方向和幅度，不作饱和腿参数打磨；预告上下界8/5用户，占唯一输入及实验预算50%。继承旧win的“相对预期的盈利信息”研究问题，替换为实际业绩事件与预告区间，禁止照抄旧PV×MODEL或加权配方。

## S1数据画像

S1任务campaign_EUR_S1_20260925_002431完成66个VECTOR扫描。仅使用以下四个数值字段，其他日期、链接、币种和类别标签不得数值rank。

| 字段 | 含义 | coverage | users / alphaCount | 角色 |
|---|---|---:|---:|---|
| ern6_actual_eps | 已报告非GAAP稀释EPS，缺稀释时基本EPS | .5258 | 71 / 91 | 已实现结果 |
| ern6_estimated_eps | 平台称最近已完成期间的Estimize加权EPS预估 | .5258 | 54 / 75 | 预期基线 |
| preliminary_eps_range_lower_bound | 已公布初步EPS或区间下界 | .5258 | 8 / 8 | 区间边界 |
| preliminary_eps_range_upper_bound | 区间上界；点估计时同下界 | .5258 | 5 / 5 | 区间边界 |

已存在field_inspect_eur_earnings6包，但source为“wqb.db fields (degraded: coverage-only)”，分布偏度、峰度、频率均未知。不可称为完整画像。低覆盖采用vec_avg后计算同日联合量，再ts_backfill(...,22)作最多约一个交易月的持有；不分别回填两个输入后相减，以减少错配旧记录。nanHandling仍为平台现有ON，实际支持集合须复查；回填不能保证覆盖、同期、币种或PIT正确。

### 特征设计的八个问题

1. 数值是什么：EPS及预告区间，不是价格、回报或类别编码。
2. 什么在变：本轮不追逐任意差分，先度量同事件的预期偏差和预告宽度。
3. 什么异常：接近零的预估分母会夸大传统百分比惊喜；使用双方绝对值最大值归一化。
4. 什么组合：每式只组合两项同维度EPS；无跨源权重混合。
5. 什么结构：实际值与预估需同会计期/币种；预告上下界需同一事件。当前平台目录未证明这些逐条匹配。
6. 什么累积：22仅为预先规定的短期事件持有上限，不推断为供应商更新频率。
7. 什么相对：在subindustry内比较归一化惊喜或宽度；共同字段与设置的sign对照检验“幅度”是否增量有效。
8. 什么本质：检验盈利信息与精度的有限问题，不能把EPS金额高、用户少、覆盖高直接当收益来源。

## 外部一手资料与限制

[WSH官方字段说明（2022版）](https://www.wallstreethorizon.com/upload/WSHEclassesandfieldsforIBAPI2022-11-16.pdf)把prelim_from/to解释为初步EPS区间，点估计时上下界相同；其中estimated_eps供应商为Zacks，且只在公告昨日/今日提供。它与当前BRAIN的Estimize描述不同，说明数据版本/供应商口径存在未解差异；不得把官方旧文档当作当前BRAIN字段的完整证明。

[英国PEAD研究](https://papers.ssrn.com/sol3/papers.cfm?abstract_id=249959)报告英国市场多种盈利惊喜定义存在公告后漂移；这是历史机制依据，不是本轮EUR收益保证。[盈利波动与PEAD研究](https://papers.ssrn.com/sol3/papers.cfm?abstract_id=1573556)讨论盈利稳定性与漂移，本轮把“预告区间精度”作为待证伪推论，并不等同论文的历史盈利波动指标。

## 已评审实验（2个问题×2个对照维度）

**Concept**: H1 Bounded realized EPS surprise
**Mechanism**: Realized non-GAAP EPS above the estimate for the last completed period may have a delayed price response. Normalize their difference by the larger absolute magnitude to avoid using a tiny estimate alone as denominator. Aggregate both current vectors before forming the contrast, then hold only a maximum of 22 trading days. The estimate source and fiscal/currency alignment must remain explicitly unverified; do not infer predictive efficacy merely from a beat. Expected Exposure: realized earnings surprise.
**Fields**: ern6_actual_eps, ern6_estimated_eps.
**Implementation Example**: `group_rank(ts_backfill(divide(subtract(vec_avg({ern6_actual_eps}),vec_avg({ern6_estimated_eps})),max(abs(vec_avg({ern6_actual_eps})),abs(vec_avg({ern6_estimated_eps})))),22),subindustry)`

**Concept**: H1 matched direction-only surprise control
**Mechanism**: Use exactly the same normalized surprise, vector aggregation, missingness path, 22-day hold and group as H1; retain only its sign before the hold. This tests whether surprise magnitude adds anything to beat-versus-miss direction; no extra time-window search. Expected Exposure: realized earnings surprise.
**Fields**: ern6_actual_eps, ern6_estimated_eps.
**Implementation Example**: `group_rank(ts_backfill(sign(divide(subtract(vec_avg({ern6_actual_eps}),vec_avg({ern6_estimated_eps})),max(abs(vec_avg({ern6_actual_eps})),abs(vec_avg({ern6_estimated_eps}))))),22),subindustry)`

**Concept**: H2 Narrow preliminary EPS range as information precision
**Mechanism**: The company-reported preliminary EPS range may contain information about earnings uncertainty. A narrower range relative to its own EPS magnitude is hypothesized to be favorable. This is a precision hypothesis, not a claim that the range predicts future EPS or that a scalar class label is a quantity. Normalize current upper-minus-lower by their larger absolute magnitude, then hold for at most 22 trading days and favor narrower ranges within subindustry. Expected Exposure: preliminary earnings information precision.
**Fields**: preliminary_eps_range_upper_bound, preliminary_eps_range_lower_bound.
**Implementation Example**: `reverse(group_rank(ts_backfill(divide(subtract(vec_avg({preliminary_eps_range_upper_bound}),vec_avg({preliminary_eps_range_lower_bound})),max(abs(vec_avg({preliminary_eps_range_upper_bound})),abs(vec_avg({preliminary_eps_range_lower_bound})))),22),subindustry))`

**Concept**: H2 matched point-versus-range control
**Mechanism**: Retain only the sign of H2 normalized range width, preserving its denominator, missingness, hold, group and direction. This isolates whether magnitude of range width adds information beyond a point estimate versus a nonzero range. Negative widths are data-quality questions, not a favorable fabricated certainty signal. Expected Exposure: preliminary earnings information precision.
**Fields**: preliminary_eps_range_upper_bound, preliminary_eps_range_lower_bound.
**Implementation Example**: `reverse(group_rank(ts_backfill(sign(divide(subtract(vec_avg({preliminary_eps_range_upper_bound}),vec_avg({preliminary_eps_range_lower_bound})),max(abs(vec_avg({preliminary_eps_range_upper_bound})),abs(vec_avg({preliminary_eps_range_lower_bound}))))),22),subindustry))`

## 后续建议、预算与停止条件

四条共享EUR/TOPCS1600/D1/SUBINDUSTRY/decay4，每字段最多出现两次，保留max-field-repeat3。VECTOR聚合、量纲归一化、有限回填及匹配sign对照增加必要算子，不为凑结构多样性换壳；事先记录小批多样性例外，字段/类型/语法/毒模式/体检门仍检查。

两式对照使用同一归一化内核再取sign，以尽量维持零分母和缺失路径一致。两边同时为0时比值未定义，不把0/0自动解释为无惊喜；取决于平台运算规则的支持变化需在结果中保留。负的预告宽度若出现须当数据问题，不能解释成高精度收益。

同一条S≥1.25且F≥.8才取得Mode B资格；未达不发窗口、反号或组合增强。平台单位/类型异常先判测量未决；仅有具体可修缺陷及独立新证据才考虑一次事先限定的复验。没有正证据时关闭本轮四式，记录精确失败边界，不判死整个66字段数据集。生产相关性、每日样本匹配、PIT和样本外表现均须另证。

## S2与S3执行记录

GEM任务gem_1790267341_eeb8da成功，四条原式与预定文档逐一匹配。DB来源52505–52508，selection_w255按身份全部选入目标52509–52512；没有自动补齐或未测变体。来源source列为空，实际来源以GEM任务与原式/身份匹配证明。

独立preflight六项通过。workflow S2干跑先执行区域零成本门禁，再按其命令使用权威build_wave脚本执行；此前workflow包装有300秒等待问题，不重复触发同一故障。wave_gate语法与字段/类型/毒模式4/4通过，已事先登记批级多样性例外。体检工具虽显示ok，原始画像只有覆盖率，不能据此声称分布或事件对齐已通过。

发批前台账同步通过。S3任务batch_track_EUR_255_20260925_003350，实际multisim为1lGIt0g9d5aFbIsqjGy3xkH，4条同批。启动时文档内容检查提示缺少“特征/建议”关键词，随后规范章节标题；实验内容和表达式未变，未重复回测。此处仅记录启动，完成数与性能须待真实结果核验。
