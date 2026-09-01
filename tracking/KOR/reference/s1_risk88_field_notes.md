# KOR risk88 字段理解与特征工程建议（S1/S2 合规补充文档）

数据集：risk88（KOR/TOP600/delay1，MATRIX，cov≈0.97）。风险模型因子载荷集：
`rsk88_mfm_ase1_*` 为 Barra 风格风险模型的日频载荷与特异性收益。

## 字段分类与理解

- **风格载荷族（ri_*）**：`ri_value`（价值）、`ri_growth`（成长）、`ri_momentum`（动量）、
  `ri_volatility`（波动）、`ri_beta`（市场 beta）、`ri_leverage`（杠杆）、
  `ri_divyield`（股息率）、`ri_size`（线性规模）、`ri_nonlsize`（非线性规模）。
  均为标准化载荷，横截面可比；低频缓变 → 预处理统一 `ts_backfill(...,66)`，低换手。
- **特异性收益族**：`dsrt`（剥离风格/行业后的个股特异性日收益，信息量最高的主信号）、
  `srisk`（特异性风险水平）、`ri_value` 配合可做单位风险缩放。

## 特征工程建议

1. **主信号**：`dsrt` 的 21 日均值 = 干净残差动量；除以 `srisk` 得单位风险残差动量。
2. **风格楔（wedge）**：`ri_beta − ri_volatility` 捕捉特异风险溢出（彩票溢价做空腿）。
3. **交叉排序**：`rank(ri_value) + rank(ri_growth)` 交集 = GARP 低拥挤区。
4. **事件门控**：`dsrt` 短期变化 >0 时才持有价值载荷（trade_when 骨架）。
5. **尾部结构**：`ts_kurtosis(ts_delta(dsrt))` 厚尾度负向，规避尾部风险。
6. **窗口纪律**：仅用 5/21/22/66 标准窗口；载荷水平用 66 日回填，变化量用 5/21 日。

## 预处理决策（入库口径）

- 低覆盖风险低（cov 0.97）无需强 backfill，但载荷更新慢，统一 66 日回填防 NaN 毒化。
- 载荷直接横截面 `rank`；比率类 `divide(x, add(y,0.001))` 防除零。
- 预期暴露标签：lowvol / value / momentum / quality / growth / size 各占一槽，防同暴露堆叠。

来源：brain-makeSomeGem（s2_nested）+ 本文档；候选池来源=skill。
