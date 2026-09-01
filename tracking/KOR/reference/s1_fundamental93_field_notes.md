# S1 字段理解：fundamental93（KOR/TOP600/D1）

- 数据集类型：MATRIX，46 字段，覆盖 0.59–0.91，竞争度低（大多数字段 users≤8，prod_corr 风险低）
- 主题：递延税项 / 税务应计（tax accruals）盈余质量族

## 字段家族

| 家族 | 字段 | 语义 |
|---|---|---|
| accruals LTM 统计 | accruals_d1_{current_t,dts,max,mean,min,length} | 应计比率当期 t 值 / LTM 窗口波动与极值 |
| tax_accruals 比率 | tax_accruals_{11,12,13,21,22,23,31,41,51} | (税费−实缴现金税)/分母，衡量应计激进度 |
| deferred_tax_expense | expense_{11,12,21,22,31,41,51} | 递延税费用比率族 |
| deferred_tax_liability | liability_{11..51} 9 个 | 递延税负债比率族 |
| expense/liability LTM 统计 | expense_d1_*、liability_d1_* | 同上统计变体 |
| asset growth | *_asset_change 3 个 | 总资产 YoY 变化（资产增长异象载体） |

## 初始信号（经典异象）

1. **应计异象（Sloan 1996）**：高应计 → 未来收益更低，方向为负
2. **资产增长异象（Cooper et al）**：资产扩张快 → 未来收益更低，方向为负
3. **税簿差异**：递延税费用/负债高企 = 盈余质量红旗
4. **税务应计激进度**：(税费−实缴税) 高 = 激进应计管理

## 进阶信号

- current_t 与 LTM mean 的缺口 → 均值回归
- accruals_d1_dts（应计波动率）：不稳定 → 负预期收益
- tax_accruals 水平持续性：ts_mean(252) 平滑
- sector 组内相对化（group_zscore / group_rank）

## 预处理决策

- current_t 已是 z-score，仅加 rank() 防厚尾
- 比率字段（_11/_12 等）偏态 → rank() 强制
- MATRIX 连续字段，无需 ts_backfill / trade_when
- 窗口用 252/504（与 LTM 语义一致的标准窗口）
- 主方向先试负向（应计/增长异象），正向作对照

## 字段/特征/建议（摘要）

- 特征：全部为 MATRIX 连续比率/统计量，无事件稀疏性；LTM 窗口统计已由数据商预计算（current_t/dts/max/mean/min/length）
- 建议：优先 current_t 类 t 值字段（已标准化）+ 负方向；比率字段一律 rank；252/504 标准窗口平滑；sector 组内相对化做差异化腿；避开 length 类元字段（信息量低）
- 风险提示：税相关比率跨行业可比性弱，优先 group_zscore(sector) 或 rank 后使用；cov<0.65 的字段（_41/_51 系）不作主力

## 主候选字段

fnd93_accruals_d1_current_t / fnd93_tax_accruals_11 / fnd93_tax_accruals_31 /
fnd93_expense_d1_current_t / fnd93_liability_d1_current_t /
fnd93_accrualsratio_d1_asset_change / fnd93_deferred_tax_expense_11 /
fnd93_deferred_tax_liability_13
