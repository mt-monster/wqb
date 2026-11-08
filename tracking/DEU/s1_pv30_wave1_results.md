# pv30 波 1 收官归因（2026-11-03）

设置：DEU/TOP500/D1/SUBINDUSTRY/decay4/trunc 0.08，全臂 returns × factor{1,2,3}_group*_top800_513 分组轴。

## 全臂结果（11 臂）

| # | 表达式（缩写） | alpha | S | F | TO | 状态 |
|---|---|---|---|---|---|---|
| 1 | rank(ts_mean(r,252)) @f2g50 | P0oOMkQq | 0.79 | 0.57 | 0.075 | REVERSION 警告 |
| 2 | -rank(ts_mean(r,22)) @f2g2 | MPYL0JMk | 0.13 | 0.03 | 0.186 | REVERSION 警告 |
| 3 | gneut(ts_mean(r,252)) @f1g10 | npv860Od | 0.68 | 0.53 | 0.067 | REVERSION 警告 |
| 4 | rank×rank 双分组乘积 | 78LnGOKv | 0.77 | 0.57 | 0.067 | REVERSION 警告 |
| 5 | -gzscore(ts_std_dev(r,66)) @f2g20 | vR1vpJGd | 0.12 | 0.04 | 0.059 | 完成 |
| 6 | trade_when(低波动门控, rank(ts_mean(r,252))) | O0AxM5z7 | 0.72 | 0.48 | 0.067 | 完成 |
| 7 | -gzscore(ts_kurtosis(r,66)) @f1g10 | P0oOYpWx | 0.73 | 0.09 | 0.085 | 完成 |
| 8 | rank(ts_delta(ts_mean(r,252),22)) @f2g10 | wpQE2Rxp | -0.09 | -0.02 | 0.195 | 完成 |
| 9 | gstd_dev(ts_mean(r,252)) @f1g10 | MPYLe7go | -0.06 | -0.01 | 0.082 | REVERSION 警告 |
| 10 | gneut(rank(ts_mean(r,252)) @f2g20) @f1g20 | npv8e76z | 0.74 | 0.52 | 0.075 | REVERSION 警告 |
| 11 | trade_when(not_equal(f2g20,f1g20), rank(ts_mean(r,252)) @f2g20) | — | — | — | — | ERROR 量纲 |

## 归因与判死

1. **族判死**：10 个可测臂 |S|<=0.79 全部离 DEU 闸（1.58）一个数量级；因子分组轴（factor1/2/3_group*）× returns 动量/矩族在 DEU/TOP500 无信号。
2. **双重否决**：多数臂还挂平台 REVERSION_COMPONENT 警告（「未来可能不收反转成分」）——即便有信号，提交前景也存疑。
3. **T11 结构缺陷教训**：`not_equal` 直接比较两个 Group 量纲字段报 Incompatible unit（Unit[Group:1] vs Unit[]）——分组字段不能当数值比较；想做「跨分组不一致」条件需先把分组映射成数值（如 group_rank 包裹后比较），本次不再补发。
4. 运维注记：本波 6 条 REVERSION 臂的 CSV 行原本全是 WARNING 盲区假 TIMEOUT（runner 轮询不认 WARNING 终态），已按 lookINTO 回收 alpha + Python 复刻指纹补行（探针 b33b455b 校验过）。
