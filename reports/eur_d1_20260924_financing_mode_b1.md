# EUR D1 fundamental23：融资依赖的 Mode B 第一轮

## 字段
全为 EUR TOPCS1600 D1 实查 MATRIX。total_financing_cash_flow（coverage .9323，users1）、operating_cashflow（.7555，users4）、assets_total_2（.9361，users7）、investment_cash_expenditures（.7439，users0）、fnd23_debt_issuance（.8347，users1）、accrued_cash_equivalents（.8672，users5）。仅使用精确字段，不展开名称相似字段。

## 特征
基线 2rwj1kWY：S1.42/F.85/2Y2.20，PROD .7879，已满足 Mode B 资格但不可提交。三个风险：绝对经营现金流分母混合正负状态；融资现金流可能只是投资/规模代理；2017与2020负收益。以下6个可证伪假设，各仅改变1–2个经济概念。不改变仿真设置，不做窗口/权重网格，不使用价格或MODEL。

## 建议
仅生成下面6个 Implementation Example；不生成孤字段模板扩展。252日为年度比较和财务缺失回填，当前无完整原始分布包，不能假称完成形状体检。另行跑两个核心字段的六项诊断，用其结果决定是否保留零分母/低覆盖敏感项。优先测试结构能否降低生产相关性，不按研究假说预判达标。

研究依据：[Liquidity Management with Decreasing-returns-to-scale and Secured Credit Line](https://arxiv.org/abs/1411.7670)讨论现金受限企业的外部融资、抵押与投资决策。下面信号是由该机制推导的待检验假设，该论文没有证明这些表达式在EUR有效。

**Dataset**: fundamental23
**Region**: EUR
**Delay**: 1

**Concept**: Financing dependence among cash-generating firms
**Mechanism**: Restrict the financing dependence comparison to firms with positive operating cash flow. Zero positions for non-generating firms remove the absolute-denominator conflation of operating strength and distress.
**Fields**: total_financing_cash_flow, operating_cashflow.
**Implementation Example**: `if_else(greater(ts_backfill({operating_cashflow},252),0),reverse(rank(divide(ts_backfill({total_financing_cash_flow},252),abs(ts_backfill({operating_cashflow},252))))),0)`

**Concept**: Deterioration of financing dependence
**Mechanism**: A year-on-year rise in external financing relative to operating cash reveals deteriorating self-funding capacity. Change replaces persistent level exposure.
**Fields**: total_financing_cash_flow, operating_cashflow.
**Implementation Example**: `reverse(rank(ts_delta(divide(ts_backfill({total_financing_cash_flow},252),abs(ts_backfill({operating_cashflow},252))),252)))`

**Concept**: Financing intensity relative to the asset base
**Mechanism**: External financing scaled by total assets measures net capital raised per unit of capital employed, without the near-zero operating cash denominator.
**Fields**: total_financing_cash_flow, assets_total_2.
**Implementation Example**: `reverse(rank(divide(ts_backfill({total_financing_cash_flow},252),ts_backfill({assets_total_2},252))))`

**Concept**: External funding relative to productive investment
**Mechanism**: Financing cash relative to fixed-asset purchases measures reliance on external funds for productive deployment. A large ratio may identify financing disconnected from productive investment; the absolute investment denominator accommodates provider sign conventions.
**Fields**: total_financing_cash_flow, investment_cash_expenditures.
**Implementation Example**: `reverse(rank(divide(ts_backfill({total_financing_cash_flow},252),abs(ts_backfill({investment_cash_expenditures},252)))))`

**Concept**: Debt issuance dependence
**Mechanism**: Isolate gross debt issuance relative to operating cash to distinguish leverage expansion from aggregate financing flows that also contain shareholder payouts.
**Fields**: fnd23_debt_issuance, operating_cashflow.
**Implementation Example**: `reverse(rank(divide(ts_backfill({fnd23_debt_issuance},252),abs(ts_backfill({operating_cashflow},252)))))`

**Concept**: Financing dependence within cash-buffer peer groups
**Mechanism**: Compare financing dependence only among firms with similar cash-to-asset buffers. This removes liquidity-buffer exposure rather than blending two signals.
**Fields**: total_financing_cash_flow, operating_cashflow, accrued_cash_equivalents, assets_total_2.
**Implementation Example**: `group_neutralize(reverse(rank(divide(ts_backfill({total_financing_cash_flow},252),abs(ts_backfill({operating_cashflow},252))))),bucket(rank(divide(ts_backfill({accrued_cash_equivalents},252),ts_backfill({assets_total_2},252))),range="0,1,0.2"))`
