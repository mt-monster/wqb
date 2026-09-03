# S1 字段理解：fundamental86（KOR/TOP600/D1）

- 数据集类型：MATRIX，10 字段，coverage=1.0，alphaCount 低
- 主题：综合评分类基本面（fundamental/earnings/average score，1-10 十分位）

## 字段/特征/建议

- 特征：评分类字段（非原始财务比率），慢变；核心 3 字段：fnd86_average_score / fnd86_fundamental_score / fnd86_earnings_score；其余为元数据（companyname/country/exchange）不可用
- 建议：正向质量动量为主；252 标准窗口做动量与平滑；sector 组内相对化；小批量探针验证（慢变族判死风险）
- 风险提示：与 KOR-FUNDAMENTAL89-ACCRUALS-DEAD 同属慢变基本面族；评分类可能不同但需实证；评分 1-10 离散度低，rank 后区分度有限

## 初始信号

1. 基本面评分横截面排序（fnd86_fundamental_score，正向）
2. 盈利评分横截面排序（fnd86_earnings_score，正向）

## 进阶信号

- 评分年度动量：ts_delta(fundamental_score, 252)
- 盈利-基本面评分差（earnings_score − fundamental_score）
- 持续高质量平滑：ts_mean(average_score, 252)
- sector 组内相对：group_zscore(average_score, sector)

## 预处理决策

- 评分已是序数尺度，rank() 包裹防离散平台
- MATRIX 连续，无需 ts_backfill/trade_when
- 窗口仅用 252（慢变语义）
