# MEA Wave 1 挖掘追踪

## 批次状态

| 批次 | 数据集 | 表达式数 | 状态 | Multisim ID |
|------|--------|----------|------|-------------|
| B1 | fundamental6 (v1) | 8 | ERROR - VECTOR字段未用vec_* | 3OvCs7dij4Rbc0ocINNUXvL |
| B2 | earnings3 + analyst7 (v1) | 8 | ERROR/CANCELLED | 3S1E9gjr4gpaAwbLQfMYBi |
| B3 | fundamental6 (v2) | 8 | COMPLETE - IS指标差 | 3AXOpV15q4UD9Tx1boN5zdt2 |
| B4 | analyst7 (v2) | 8 | CANCELLED | ssQKv1Yz51Vb96R4eZOLbC |
| B5 | earnings3 (v2) | 6 | COMPLETE - IS指标差 | - |
| 09A | analyst7+volume | 8 | COMPLETE - 5 near, 0 candidate | 2WeVBY1nK4ERb8wlMWJTjYZ |
| 10A | fundamental6 (v3) | 8 | SUBMIT_FAIL | - |
| 11A | model25 | 8 | RUNNING | 1FDxQH8an4QAaIy16AOJbWj1 |
| 12A | pv1 | 8 | RUNNING | 3O6R405VU4Mt9T7PM7mMrVZ |

## 目标
- 点亮 fundamental 金字塔 (当前: 0)
- 点亮 earnings 金字塔 (当前: 0)
- 找到3个不同数据集、不同风格、prod_corr<0.7的alpha

## 关键发现
1. MEA 区域所有数据字段都是 VECTOR 类型，必须使用 vec_* 聚合
2. 已有2个 analyst7 alpha 通过IS检查但 prod_corr>0.8
3. fundamental6 简单比率策略在 MEA 不工作
4. earnings3 只有4个字段，信号有限
5. model25 是 MATRIX 类型字段，可直接使用

## 下一步
1. 等待 11A (model25) 和 12A (pv1) 结果
2. 分析通过廉价闸的alpha
3. 对达标alpha进行robust测试
4. 计算alpha间相关性
