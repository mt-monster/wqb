# EUR D1 fundamental17：四个配对基线对照

wave251主计划保留8个预先定义假设，加4个对照；12是本次问题清单长度，不是通用选波上限。
对照与主假设保持字段、252回填、分组轴及信号方向一致，只替换被检验的变化/差额部分，避免将窗口或中性化变化误当机制增益。原48个自动包装变体保持可追溯，未回测不写dead_end。

**Dataset**: fundamental17
**Region**: EUR
**Delay**: 1

**Concept**: Labor productivity level control
**Expected Exposure**: Labor productivity level.
**Mechanism**: Baseline for annual change in net income per employee. Hold 252-day backfill and subindustry grouping constant; test whether annual change adds value beyond the level. High values preferred.
**Fields**: ttm_net_income_per_employee.
**Implementation Example**: `group_rank(ts_backfill({ttm_net_income_per_employee},252),subindustry)`

**Concept**: Receivables turnover level control
**Expected Exposure**: Working capital efficiency level.
**Mechanism**: Baseline for rising receivables turnover. Keep 252-day backfill and industry grouping; compare current level with annual change. Higher turnover preferred, subject to industry business model differences.
**Fields**: fnd17_ttmrecturn.
**Implementation Example**: `group_rank(ts_backfill({fnd17_ttmrecturn},252),industry)`

**Concept**: Recurring expense burden level control
**Expected Exposure**: Low operating expense intensity.
**Mechanism**: Baseline for falling SGA-to-sales. Keep negative direction, industry grouping and 252-day backfill. Test whether low expense intensity already explains the change signal. Never flip to high expense direction.
**Fields**: fnd17_ttmsga2rev.
**Implementation Example**: `reverse(group_rank(ts_backfill({fnd17_ttmsga2rev},252),industry))`

**Concept**: Normalized earnings return on assets control
**Expected Exposure**: Recurring profitability level.
**Mechanism**: Baseline for normalized-minus-reported earnings scaled by assets. Hold annual normalized income, total assets, 252-day backfill and cross-sectional rank constant. Remove only the reported-income subtraction to test whether the gap adds value beyond recurring profitability.
**Fields**: annual_normalized_net_income_common, fnd17_ata.
**Implementation Example**: `rank(divide(ts_backfill({annual_normalized_net_income_common},252),ts_backfill({fnd17_ata},252)))`

这些是待检验假设。统一沿用EUR/TOPCS1600/D1/decay4/SUBINDUSTRY设置；对照优于或劣于主假设均需联合检查逐年、RN指标及相关性，不能依据单次Sharpe差值认定机制有效。
