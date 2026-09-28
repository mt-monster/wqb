# EUR D1 fundamental17：盈利口径纠错与直接对照

## 输入与动机

用户要求对新增对照带来的Sharpe提升继续探查。wave251中N1aeg3pp（标准化净利润/资产）S1.18/F.80/2Y.43，88jvaGR7（标准化净利润减报告利润，再除资产）S.58/F.23/2Y.08。2026-09-24平台详情新复核发现后者有UNITS警告：subtract第二输入为Unit[]，第一输入为Unit[TSPrice:1]。这使旧配对不能用于干净的会计调整归因。

本波是一次测量纠错与缺失对照补齐，最多2条新回测。不是根据S1.18发参数增强波；Mode B资格线保持S≥1.25且F≥.8。已有N1aeg3pp作为冻结的历史水平对照，设置完全相同，不重复回测。若新式还有单位警告，本波只记“测量尚未解决”，不能当作经济机制失败或成功。

## 已有证据

N1aeg3pp逐年Sharpe（2014–2023）：2.17、1.92、1.49、-1.01、3.71、2.22、-1.00、2.74、-.08、1.42。7/10年正值，近3年含负年；RN Sharpe=.53，相比原始1.18仍明显偏弱。多空数量摘要473/531与旧差额式相同，尚不能证明逐日覆盖掩码相同。TVR1.13%低于战役5%下限。以上说明研究线索值得留存，但还没有增强或提交资格。

文献中的毛利润/资产是独立的盈利能力测度，不能把此处净利润直接称为毛利润，也不能援引论文证明本平台字段有效：[Novy-Marx, The Other Side of Value](https://www.nber.org/papers/w15940)。本波不扩展到毛利润、新窗口或新中性化。

## 字段

- annual_normalized_net_income_common：年度标准化普通股净利润，MATRIX，coverage .7495，users1，原式中无单位警告。
- annual_net_income_available_common：年度普通股可得报告净利润，MATRIX，coverage .7495，users3。与旧fnd17_aniac有相同文字定义；是否适合相减须以本波平台UNITS检查验证，不能仅凭名称断言等价。
- fnd17_ata：年度总资产，MATRIX，coverage .7509，users5，统一分母。

三个字段均来自fundamental17。冷门字段预算100%；EUR/TOPCS1600/D1/SUBINDUSTRY/decay4/truncation.08，252日回填与2014–2023 IS范围冻结；保留既有完整体检包缺失的metadata-only声明。

## 特征与建议

预注册两个问题。A：报告利润水平与标准化利润水平的区别能否解释原先观察到的差距？B：在平台认可的同单位字段上，原会计调整差额机制是否仍弱？这两个问题都有现存证据缺口，不用更多窗口寻找高点。

**Dataset**: fundamental17
**Region**: EUR
**Delay**: 1

**Concept**: Reported earnings to assets matched measurement control
**Mechanism**: Measure reported annual earnings available to common relative to the same annual assets used by the frozen normalized-earnings baseline. This isolates the accounting earnings definition while holding lookback, ranking, universe and simulation settings fixed. The field alias is selected for its documented meaning, not past performance.
**Fields**: annual_net_income_available_common, fnd17_ata.
**Implementation Example**: `rank(divide(ts_backfill({annual_net_income_available_common},252),ts_backfill({fnd17_ata},252)))`

**Concept**: Accounting adjustment spread measurement repair
**Mechanism**: Retest the original normalized-minus-reported earnings spread using the same-family reported-income alias. It is a measurement repair, not a new economic direction. Platform unit compatibility is required before interpreting its performance; any remaining unit warning invalidates the comparison.
**Fields**: annual_normalized_net_income_common, annual_net_income_available_common, fnd17_ata.
**Implementation Example**: `rank(divide(subtract(ts_backfill({annual_normalized_net_income_common},252),ts_backfill({annual_net_income_available_common},252)),ts_backfill({fnd17_ata},252)))`

## 事先定义的后续决策

1. 先查UNITS与覆盖，再看全期/2Y/RN/逐年证据；存在测量问题时不按Sharpe排名决定胜负。
2. 报告与标准化水平相近：保留盈利能力共同线索，降低“剔除一次性项目带来独立收益”的优先级。
3. 修正后的差额仍弱：关闭本轮差额结构；不据此封禁利润水平、整个字段或数据集。
4. 新候选同时达到Mode B资格才进入机制优化；否则本轮到此，不加窗口、不翻号、不通过放宽阈值造合格结果。研究线索保留在research_leads_w251，与near/ready分开。

## wave252 实测结果

计划2条、选中2条、门禁2条通过、回测2条COMPLETE、0错误；两条均无平台UNITS警告。S3批次`11q7eX96y4Kv9x7CboI5Cup`，S4任务`campaign_EUR_S4_20260924_230711`成功；没有正式提交Alpha。

| 对照 | Alpha | Sharpe | Fitness | 2Y | RN Sharpe | 换手率 |
|---|---|---:|---:|---:|---:|---:|
| 标准化利润/资产（已有） | N1aeg3pp | 1.18 | .80 | .43 | .53 | 1.13% |
| 报告利润/资产（新增） | QPbYaMlK | 1.13 | .75 | .47 | .52 | 1.12% |
| 修正差额/资产（新增） | 6XjAw7Y7 | -.50 | -.17 | -.64 | -.59 | 1.33% |

这次续查解决了原差额式的单位警告，并补齐直接盈利水平对照。标准化与报告利润的结果相近，不支持把先前的提升归因于“剔除一次性项目”；差额式在本设置下仍弱。无单位警告不证明覆盖完全相同，.05的Sharpe差异未检验显著性。

两条新式均未达到Mode B资格，完整合格0。按事先规则关闭本次测量复验，保留盈利水平线索及RN/近期衰减问题；下一步先寻找新诊断证据，不消耗预算重复扩窗口、翻号或调参。`research_leads_w251`记录完成结果，`s6_verdict_252`与真实波次结果已回写，字段经验已刷新。

工程验收同时发现按数据集关联波次会串入旧Alpha，已修复为真实backtest_results的region/wave/alpha_id关联。新回归覆盖相同数据集跨波、空波、跨区与重复行；实时MCP查询252仅返回上述2条新结果。全量1402 passed / 10 skipped，JUnit零失败、零错误（45.58秒）。
