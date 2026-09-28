# EUR D1 other460：财务趋势概率的方向信息探针

## S-PRE / S0 选择依据

最新wave253已闭环，完整合格仍0。实时其他候选复核后：analyst69已有13998个Alpha且主体字段较拥挤；earnings6无MATRIX返回，需另核类型。other460为MODEL类别（名称前缀other不改变平台类别），EUR/TOPCS1600/D1覆盖1、1393字段、users66、alphaCount121；S0 score1.11、tier1、hard_excluded=false。无匹配的other460死路，源候选池此前为空。

model264样本字段与other460的目标和描述高度相似，本轮不把二者当独立数据来源并行试同一机制。S0点塔候选的优先级不等同字段质量或预计收益；估算座位数也不能证明能挖出10个Alpha。旧胜绩中PV×MODEL及加权混合不采用。

## S1 字段分类与元数据

S1任务`campaign_EUR_S1_20260924_235909`于2026-09-25 00:00完成：1393/1393 MATRIX、全部userCount≤9，描述均有值。MCP初次返回300字段只是切片，以下使用完整目录和逐字段含义。

| 字段 | 角色 | 方向描述 | coverage | users / Alpha数 |
|---|---|---|---:|---:|
| oth460_sopi_l3 | 主信号 | 经营利润趋势上升概率 | 1 | 0 / 0 |
| oth460_sopi_l1 | 反向状态 | 经营利润趋势下降概率 | 1 | 0 / 0 |
| oth460_1l_dlts | 主信号 | 总债务趋势下降概率 | 1 | 1 / 1 |
| oth460_3l_dlts | 反向状态 | 总债务趋势上升概率 | 1 | 0 / 0 |
| oth460_fincf_l1 | 主信号 | 融资活动净现金流趋势下降概率 | 1 | 0 / 0 |
| oth460_fincf_l3 | 反向状态 | 融资活动净现金流趋势上升概率 | 1 | 0 / 0 |
| oth460_es_sale_ntm_r1m_l3 | 主信号 | NTM收入预期1月修正的趋势上升概率 | 1 | 1 / 1 |
| oth460_es_sale_ntm_r1m_l1 | 反向状态 | 同一目标的趋势下降概率 | 1 | 0 / 0 |

8个输入均冷门；不使用PV、标签class编号或其它数据集。数据分布包未找到，coverage1只是元数据，非实测每日有效性。全部设置固定EUR/TOPCS1600/D1/SUBINDUSTRY/decay4/truncation.08，FULL 2014–2023。

## 特征工程建议：黑盒模型的八问边界

1. 不变量：同一目标的升/降概率标签明确；三状态和是否恒为1未实测，因此不借该等式省略输入或推断独立性。
2. 变化：模型预测的方向不等于已实现财务变化；更新频率与预测跨度未明，不臆设季度回填或年差。
3. 异常：检查回测的持仓数量、集中度和单位警告；100%目录覆盖可能掩盖默认值或常数。
4. 组合：只做同一目标相反状态概率之差，检验相对置信信息；不作不同目标的概率加权平均。
5. 结构：MODEL信号只从本集取得，四个经济问题分别验证；目标之间实际相关性须由结果检验。
6. 累积：初探不添加时间平滑；模型内部历史长度未知，避免又人为叠一层窗口。
7. 相对位置：主假设与对照都在subindustry内group_rank，统一行业参照，防行业间概率校准差异主导；同设置仍须检查实际持仓口径。
8. 不确定性：预测期限、校准、历史训练/PIT未由元数据证明。若质量初筛达标，再查相关性、逐年、RN、稳健性和文档证据；不把低users当低Prod保证。

## 事先锁定的四组假设与对照

四个主假设保持方向，四个单侧控制用于判断相反状态信息是否增加价值。8不是固定开波数量，而是4个问题各自需要2项实验。原始融资需求问题参考fundamental23已测经验，但这里预测的是未来现金流方向，不能冒充旧胜绩复现或已验证增强。

**Dataset**: other460
**Region**: EUR
**Delay**: 1

**Concept**: H1 Forecast operating profitability improvement
**Mechanism**: Companies with a higher model probability of rising operating income than falling operating income may exhibit gradual fundamental repricing. Compare the signed directional balance with the same-target up-probability control. This is a forecast direction, not realized profit growth. Expected Exposure: forward operating profitability.
**Fields**: oth460_sopi_l3, oth460_sopi_l1.
**Implementation Example**: `group_rank(subtract({oth460_sopi_l3},{oth460_sopi_l1}),subindustry)`

**Concept**: H1 matched one-sided probability control
**Mechanism**: Keep the same target, preferred direction, industry grouping and simulation settings; remove only the opposite-state probability. This baseline diagnoses whether directional subtraction adds information. It is not an extra optimized signal. Expected Exposure: forward operating profitability.
**Fields**: oth460_sopi_l3.
**Implementation Example**: `group_rank({oth460_sopi_l3},subindustry)`

**Concept**: H2 Forecast balance sheet deleveraging
**Mechanism**: A higher probability of falling rather than rising total debt may proxy lower future financing risk. The sign is preregistered; it does not assert that every debt reduction is beneficial. Compare against the same-target down-probability control. Expected Exposure: balance sheet debt reduction.
**Fields**: oth460_1l_dlts, oth460_3l_dlts.
**Implementation Example**: `group_rank(subtract({oth460_1l_dlts},{oth460_3l_dlts}),subindustry)`

**Concept**: H2 matched one-sided probability control
**Mechanism**: Keep the same target, preferred direction, industry grouping and simulation settings; remove only the opposite-state probability. This baseline diagnoses whether directional subtraction adds information. It is not an extra optimized signal. Expected Exposure: balance sheet debt reduction.
**Fields**: oth460_1l_dlts.
**Implementation Example**: `group_rank({oth460_1l_dlts},subindustry)`

**Concept**: H3 Forecast decline in net financing inflows
**Mechanism**: Forecast declines in financing cash flow may reflect less need for external capital or greater net repayments. This carries forward a financing-demand question from fundamental23 using an independent forward forecast input, not the old cash-flow/assets expression. Economic ambiguity remains: falling flow can also mean distress, so no sign search after failure. Expected Exposure: external financing dependence.
**Fields**: oth460_fincf_l1, oth460_fincf_l3.
**Implementation Example**: `group_rank(subtract({oth460_fincf_l1},{oth460_fincf_l3}),subindustry)`

**Concept**: H3 matched one-sided probability control
**Mechanism**: Keep the same target, preferred direction, industry grouping and simulation settings; remove only the opposite-state probability. This baseline diagnoses whether directional subtraction adds information. It is not an extra optimized signal. Expected Exposure: external financing dependence.
**Fields**: oth460_fincf_l1.
**Implementation Example**: `group_rank({oth460_fincf_l1},subindustry)`

**Concept**: H4 Forecast improvement in revenue estimate revisions
**Mechanism**: A higher probability that the direction of next-twelve-month revenue revisions improves rather than worsens may capture gradual incorporation of changes in expectations. The 1M text is part of the model target label, not an added expression lookback or a verified prediction horizon. Expected Exposure: forward analyst revenue revisions.
**Fields**: oth460_es_sale_ntm_r1m_l3, oth460_es_sale_ntm_r1m_l1.
**Implementation Example**: `group_rank(subtract({oth460_es_sale_ntm_r1m_l3},{oth460_es_sale_ntm_r1m_l1}),subindustry)`

**Concept**: H4 matched one-sided probability control
**Mechanism**: Keep the same target, preferred direction, industry grouping and simulation settings; remove only the opposite-state probability. This baseline diagnoses whether directional subtraction adds information. It is not an extra optimized signal. Expected Exposure: forward analyst revenue revisions.
**Fields**: oth460_es_sale_ntm_r1m_l3.
**Implementation Example**: `group_rank({oth460_es_sale_ntm_r1m_l3},subindustry)`

## 预算、门禁与停止规则

预算8条，全部经GEM并按selection_w254的原式身份选入；自动窗口/包装变体留在延后审计，不自动补入。所有字段最大出现2次，保留默认max-field-repeat3。统一同一结构用于匹配检验，因此批级结构多样性事先登记探针例外；语法、字段、类型、毒模式、区域门禁照常。

同一候选须达到S≥1.25且F≥.8才允许Mode B。若不达，关闭这8个已测结构并保存证据；不自动反号或扫窗口。若主假设与对照持仓口径不一致，暂停增量归因；只有独立测量证据且仍有研究价值时才安排有界纠错。Mode B达标也不等于提交通过，必须继续完整验证。

## S2与S3执行证据

GEM任务`gem_1790265912_2da053`于00:06完成，56条真实入库。`selection_w254`核验8条原式身份，另外48条为4字段各12种自动时间窗口/包装，保留延后审计；不代表数据集全部机会已覆盖。选波独立预检6/6、门禁8/8，默认字段重复上限3保持。匹配实验采用已登记的批级多样性例外，缺分布包使用显式warn。

00:10发批前台账同步检查PASS，任务`batch_track_EUR_254_20260925_001024`模拟批`2bn6JB5X64wD9XUtNXf5ziY`，8条进入S3；结果待核实。未正式提交Alpha。

## S3、S4与S6结果（00:17更新）

8/8 COMPLETE且入库，0执行错误。逐ID MCP核查确认原式、EUR/D1与固定设置一致；S4 `campaign_EUR_S4_20260925_001414`成功。结果如下，括号为配对单侧基线：

| 机制 | 主假设Alpha | 对照Alpha | S | F | 2Y | RN S |
|---|---|---|---:|---:|---:|---:|
| 经营利润概率差 | `9qjEWPP2` | `akbVx2X2` | -.50（-.50） | -.17（-.17） | -.63（-.62） | -.16（-.16） |
| 债务概率差 | `JjNPQ0Yl` | `E5pVR0om` | -.37（-.36） | -.11（-.11） | -.44（-.44） | -.24（-.24） |
| 融资现金流概率差 | `akbVx2M1` | `P02MgrrW` | -.45（-.39） | -.15（-.12） | -.91（-.89） | -.34（-.24） |
| 收入修正概率差 | `vRrO2nxQ` | `npdAPkk3` | .05（.07） | .01（.01） | -.07（-.10） | .06（.06） |

八条没有UNITS警告；持仓总数均1498，尚未证明每日掩码相同。每条仍4–5个RA失败，2Y均负，Prod/Self未核实。prod-first因所有|S|<1而跳过昂贵查询。观察不到支持概率差扩展的收益证据；相近结果不能直接证明两式相关性为1，也没有进行差异显著性检验。

0个Mode B资格，0个完整合格Regular。`s6_verdict_254`、`research_leads_w254`与精确八式范围的registry已回写，wave_result保留真实批次和设置并标记closed/FAIL。S6 `campaign_EUR_S6_20260925_001633`已生成[字段经验](dataset_experience/eur_other460_campain.md)。未測48变体保留审计，研究线索预算0；下一预算回到独立机制，不机械反号或换窗口。

