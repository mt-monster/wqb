# EUR D1 fundamental17：质量变化与经营效率八机制首探

> 2026-09-24 22:14修订：下列8条仍是主假设；实际wave251增加[四个配对基线](eur_d1_20260924_fundamental17_controls.md)，形成8＋4实验清单。以DB `selection_w251`所列12个身份为执行要求，替代原“必须8条”。12也不是通用上限。48个自动变体只是本轮延后，未回测不代表已判死。

## 字段与范围

2026-09-24 S1扫描523个MATRIX字段。使用真实平台描述，覆盖率约0.60–0.75，以下所用字段users均≤9。`fnd17_ata`与热门资产别名可能同源，低users不能证明独立性；按经济角色选取且不重复同义字段。完整WebDataScope形状包缺失，覆盖仅为元数据，未知分布不宣称体检通过。252日回填用于财报值持续有效，不假设每天更新；长回填可能带来陈旧信息，后续强候选须验证。

范围EUR/TOPCS1600/D1/SUBINDUSTRY/decay4/truncation.08，沿用区域设置。8个独立预定概念各1条，另加4个预定对照；100%冷门字段预算，分组轴industry/subindustry，窗口66/252。不得扩为字段笛卡尔积、不得修改信号方向、不得注入其他骨架。禁止PV×MODEL、加权混合及add混信号。实际选择必须覆盖DB实验清单的每个身份；任何缺失先修生成或明确报告，不静默缩波。

## 特征工程建议

按字段经济角色构建经营效率变化、财报质量差额和资产扩张节制三个方向；使用252日回填维持财报值，横截面rank减轻量纲与离群值影响。年度变化与水平对照保持相同分组、回填和方向；归一化盈利差额用同一年度资产缩放。配对比较后再决定是否做窗口敏感性，不能把未测的自动包装当作已失败机制。

## 先验与可证伪边界

继承本会话 fundamental23 的教训：冷门不保证低Prod，盈利暴露剥离可提高IS但独立性待证；本轮用经营质量变化检验不同于融资依赖的收益来源。news46/50弱结构不复用。读取当前DB priors的wins/dead_ends，但其中任何加权混合旧配方均不得使用。

理论背景：[Novy-Marx盈利能力研究](https://www.nber.org/papers/w15940)及[Quality minus junk原论文](https://link.springer.com/article/10.1007/s11142-018-9470-2)把盈利、成长与安全性作为质量研究方向。下列具体字段、方向和欧股可预测性均是本战役待检验假设，不是论文已验证结果；不照搬其合成权重。至少三条为≤4算子，避免为多样性而无经济含义地堆算子。

**Dataset**: fundamental17
**Region**: EUR
**Delay**: 1

**Concept**: Receivables collection efficiency improvement
**Expected Exposure**: Working capital quality independent of financing flow.
**Mechanism**: Rising trailing-year receivables turnover over one year may indicate better collection rather than accounting sales growth; compare within industry to reduce payment-term differences. fnd17_ttmrecturn is receivables turnover for trailing twelve months, users0, coverage.6533.
**Fields**: fnd17_ttmrecturn.
**Implementation Example**: `group_rank(ts_delta(ts_backfill({fnd17_ttmrecturn},252),252),industry)`

**Concept**: Declining recurring operating expense burden
**Expected Exposure**: Operating cost efficiency change.
**Mechanism**: A fall in TTM selling/general/administrative expense over sales may reveal scalable operations. Reverse the annual change; lower cost is preferred. fnd17_ttmsga2rev users0, coverage.6117. Do not replace direction with a generic wrapper.
**Fields**: fnd17_ttmsga2rev.
**Implementation Example**: `reverse(group_rank(ts_delta(ts_backfill({fnd17_ttmsga2rev},252),252),industry))`

**Concept**: Current gross margin exceeding established annual level
**Expected Exposure**: Profitability improvement, subject to seasonality.
**Mechanism**: The latest quarterly gross margin above the most recent historical annual margin tests emerging pricing or production efficiency. Quarter versus year is not seasonally matched; a failure should close this specific contrast. fnd17_qgrosmgn users5 coverage.6031; fnd17_agrosmgn users1 coverage.6380.
**Fields**: fnd17_qgrosmgn, fnd17_agrosmgn.
**Implementation Example**: `group_rank(subtract(ts_backfill({fnd17_qgrosmgn},252),ts_backfill({fnd17_agrosmgn},252)),subindustry)`

**Concept**: Normalized earnings obscured by transitory charges
**Expected Exposure**: Earnings normalization versus headline accounting results.
**Mechanism**: Normalized common net income minus reported common net income, scaled by total assets, tests whether one-time charges obscure recurring earnings. This is not cash-flow accrual measurement. annual_normalized_net_income_common users1 coverage.7495; fnd17_aniac users1 coverage.7495; fnd17_ata users5 coverage.7509. Keep fiscal periods and shareholder scope aligned.
**Fields**: annual_normalized_net_income_common, fnd17_aniac, fnd17_ata.
**Implementation Example**: `rank(divide(subtract(ts_backfill({annual_normalized_net_income_common},252),ts_backfill({fnd17_aniac},252)),ts_backfill({fnd17_ata},252)))`

**Concept**: Fiscal net margin progression
**Expected Exposure**: Realized annual profitability growth.
**Mechanism**: Compare first versus second historical fiscal-year net margin directly, avoiding a trading-day delta that can miss annual publication timing. fnd17_tcpngmpna users0 coverage.7464; fnd17_a2netmrgn users7 coverage.7451.
**Fields**: fnd17_tcpngmpna, fnd17_a2netmrgn.
**Implementation Example**: `group_rank(subtract(ts_backfill({fnd17_tcpngmpna},252),ts_backfill({fnd17_a2netmrgn},252)),industry)`

**Concept**: Improving earnings productivity per employee
**Expected Exposure**: Labor productivity change.
**Mechanism**: Annual increase in TTM net income per employee tests efficiency improvements rather than a stable high-margin industry level. Employee reporting may be stale; compare within subindustry. ttm_net_income_per_employee users0 coverage.6813.
**Fields**: ttm_net_income_per_employee.
**Implementation Example**: `group_rank(ts_delta(ts_backfill({ttm_net_income_per_employee},252),252),subindustry)`

**Concept**: Gross margin retained after SG&A burden
**Expected Exposure**: Operating margin quality.
**Mechanism**: TTM gross margin minus TTM SG&A/sales estimates operating spread before other charges. Ratios share sales denominator and period; it is an accounting difference, not a weighted blend. Compare within industry. fnd17_8_ttmgrosmgn users1 coverage.6326; fnd17_ttmsga2rev users0 coverage.6117. Verify platform unit consistency at gate.
**Fields**: fnd17_8_ttmgrosmgn, fnd17_ttmsga2rev.
**Implementation Example**: `group_rank(subtract(ts_backfill({fnd17_8_ttmgrosmgn},252),ts_backfill({fnd17_ttmsga2rev},252)),industry)`

**Concept**: Conservative asset expansion
**Expected Exposure**: Investment discipline.
**Mechanism**: Lower reported annual total-asset growth may identify disciplined investment. Use a 66-day mean to smooth reporting transitions; this is one diagnostic benchmark, not a window search. fnd17_atachg users1 coverage.7484.
**Fields**: fnd17_atachg.
**Implementation Example**: `reverse(group_rank(ts_mean(ts_backfill({fnd17_atachg},252),66),subindustry))`

## 波后决策

仅同条Sharpe≥1.25且Fitness≥.8进入Mode B。弱结果记录具体搭配/结构/设置边界，不判死整个数据集。强代表先测Prod/Self再扩展同族；RN指标不足不靠同义字段或参数网格掩饰。8条以内首探是一项预算有界实验，七槽上限仍由账户仲裁器执行；不足独立通过门禁的机制时不硬凑槽位。
