# KOR pv30 字段理解与特征工程建议（S1/S2 合规补充文档）

数据集：pv30（KOR/TOP600/delay1，GROUP 615 + MATRIX 75，PV 类）。
PCA 结构集：`pca_industry_grouping_method{2,3}_{2,10,50}clusters`（聚类行业分组，GROUP 型）
+ `principal_component_{N}_{all513|top1200_xjp_513}`（主成分，MATRIX 型）。

## 字段分类与理解

- **分组字段（group/bucket 角色）**：`pca_industry_grouping_*` 为数据驱动的行业聚类标签，
  不直接做信号，只作 `group_*` 算子的分组维度或 `bucket` 自定义分组。
- **主成分字段（主信号）**：`principal_component_11_all513`、
  `principal_component_9_top1200_xjp_513` 等，横截面标准化的市场结构分量。
- **事件语义**：个股聚类归属变化（`days_from_last_change`）= 结构漂移事件，
  归属稳定的票信号更可信 → 事件门控天然适配。

## 特征工程建议

1. **结构漂移衰减**：`days_from_last_change(grouping)` 越大 = 归属越稳，权重越高。
2. **主成分动量**：`ts_delta(pc_11, 5)` 短期结构变化方向。
3. **组内相对**：`group_rank(rank(pc_11), pca_industry_grouping_method2_10clusters)`
   ——聚类簇内相对强弱（数据驱动行业中性）。
4. **双成分协同**：`ts_corr(pc_11, pc_9, 22)` 结构分量联动。
5. **尾部结构**：`ts_kurtosis(ts_delta(pc_11,5), 66)` 负向，结构突变风险规避。
6. **事件门控**：归属变化 <5 日（刚漂移）时持仓，其余观望。
7. **预处理**：GROUP 字段只进分组/条件位，不进数值运算；主成分直接 `rank`。

来源：brain-makeSomeGem（s2_nested）+ 本文档；候选池来源=skill。
