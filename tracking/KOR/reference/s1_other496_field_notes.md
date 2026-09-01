# KOR other496 字段理解与特征工程建议（S1/S2 合规补充文档）

数据集：other496（KOR/TOP600/delay1，MATRIX 78 + VECTOR 26，判定 CAUTION→PROBE 复核）。
混合集：`oth496_returns*` 区间累计收益族 + `oth496_ard_*`/`oth496_a2_ard_*` 财报资产负债族。

## 字段分类与理解

- **收益族（主信号）**：`returns20/returns60/returns250`（累计收益，原向）与
  `returns20_t/returns60_t/returns250_t`（_t 变换版本）。多窗口动量/反转原料。
- **财报族（辅助信号）**：`ard_tot_assets`（总资产）、`ard_total_shareholders_equity`（股东权益）、
  `a2_ard_cash_and_cash_equivalents`（现金）。低频季度更新 → 66 日回填。
- **字段角色**：收益族 = 主信号；财报族 = 辅助/条件字段（可做 bucket 分组或 if_else 条件），
  禁止 add(A,B) 裸混——财报族只进条件腿或分母腿。

## 特征工程建议

1. **长短动量差**：`returns250_t − returns20_t`，长牛短弱时做多（趋势确认）。
2. **短期反转**：`10 − returns250` 反向（均值回归腿，注意方向待回测定夺）。
3. **账面杠杆条件**：`equity/assets` 与动量的 `ts_corr(…,22)` 捕捉财务质量×动量协同。
4. **事件门控**：放量（volume>20 日均）时持有长短动量差——主信号=动量差，事件=量能确认。
5. **财务漂移**：`ts_av_diff(cash/assets, 252)` 现金占比年漂移（质量改善）。
6. **预处理**：收益族 10 日回填（短窗快照）；财报族 66 日回填；MATRIX 集禁用 vec_*。

来源：brain-makeSomeGem（s2_nested）+ 本文档；候选池来源=skill。
