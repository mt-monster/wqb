# EUR D1 融资依赖 Mode B1：未实现概念补齐

## 字段
仅 total_financing_cash_flow / operating_cashflow / assets_total_2，均为 S1 已确认 MATRIX，users分别1/4/7，全部冷门。

## 特征
本文件补齐已预先定义但未正确生成的两个 Mode B1 概念，不依据第248波收益重新调参。基线2rwj1kWY S1.42 F.85，prod .7879。字段诊断显示经营现金流正年度均值仅348/1256，需分离现金消耗与现金生成。253等非标准窗口、权重混合和自动改信号方向均禁止。

## 建议
精确绑定下面原式，经 GEM 生成；若生成的式子丢失符号或条件，直接拒绝。标准回填252，不更改EUR/D1/TOPCS1600/SUBINDUSTRY/decay4设置。研究机制来源见前轮融资概念文档。

**Dataset**: fundamental23
**Region**: EUR
**Delay**: 1

**Concept**: Financing dependence conditional on positive operating cash
**Mechanism**: Among firms with positive operating cash, prefer lower external financing relative to that internally generated cash. Firms consuming operating cash carry no raw signal.
**Fields**: total_financing_cash_flow, operating_cashflow.
**Implementation Example**: `if_else(greater(ts_backfill({operating_cashflow},252),0),-rank(divide(ts_backfill({total_financing_cash_flow},252),abs(ts_backfill({operating_cashflow},252)))),0)`

**Concept**: Net financing relative to the asset base
**Mechanism**: Prefer lower financing cash raised per unit of existing total assets. This avoids the operating-cash denominator and measures capital expansion intensity rather than its absolute size.
**Fields**: total_financing_cash_flow, assets_total_2.
**Implementation Example**: `subtract(0,rank(divide(ts_backfill({total_financing_cash_flow},252),ts_backfill({assets_total_2},252))))`
