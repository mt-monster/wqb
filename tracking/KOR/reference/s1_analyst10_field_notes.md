# S1 字段理解：analyst10（KOR/TOP600/D1）

- 数据集类型：640 字段（475 MATRIX + 165 VECTOR），38 前缀簇
- 主题：WorldQuant 专有 SmartEstimates 体系——模型预测盈余惊喜（pred_surps）、稳定化估计值（smart_ests）、覆盖分析师数（nums）、销售/预税修订比率（salrevise/prerevise）、历史估计明细（det/past VECTOR 族）
- **定位差异化**：revise_value 族已判死（wave 97-99，天花板 S=0.67 + CW 墙）；本波主攻 smartest pred_surps 族（users 1-4 冷门，PEAD 机制），与 wave 143 EPS 修订动量（prod 墙 0.83）机制不同——预测惊喜是模型前瞻信号，非历史修订聚合

## 字段/特征/建议

- **主选 pred_surps 族（MATRIX，cov 0.83-0.96，users 1-4）**：net_fy1_pred_surps_v1（cov 0.96）、sal_fy1_pred_surps_v1（0.96）、pre_fy1_pred_surps_v1（0.95）、ebi_fy1_pred_surps_v0/v1（0.95）、gps_fy1_pred_surps_v1（0.94）、ndt_fy1_pred_surps_v1（0.85）、sal_fy2_pred_surps_v1（0.83）、dps_fy1_pred_surps_v2（0.83）
- **辅助 nums 族（覆盖广度）**：pre_fq1_nums（0.97）、gps_fq1_nums（0.96）、bps_fq1_nums（0.93）、nav_fq2_nums（0.89）——冷门股溢价（负向）或作 bucket/if_else 门控
- 次选 salrevise_ratio_to_close_fy1_7862（cov 0.68 users=2，销售修订非 EPS）
- 禁用：historical_estimate_currency_*（货币代码分类值）；anl10_det/*past VECTOR 明细族（estimate 快照元数据非信号）；revise_value 族（判死）；anl10_analyst_innovation_*（wave97-99 判死长名族）

## 初始信号

1. 预测盈余惊喜动量（PEAD）：pred_surps 高 → 分析师共识将上修 → 公告后漂移（正向）
2. 多口径惊喜一致性：net/sal/ebi/pre 同向验证（2 字段 rank 组合）
3. 覆盖广度冷门溢价：nums 低 → 关注不足 → 正向（neglected firm）

## 进阶信号

- industry 组内相对化（wave 143 验证 +0.10S）
- ts_decay_linear(5/22) 平滑（惊喜信号衰减快，短窗优先）
- v0 vs v1（raw vs stabilized）对照定版本
- nums 作 bucket 分组变量：按覆盖广度分桶后组内排惊喜
- if_else 覆盖门控：nums 太低时惊喜不可靠 → 置 0

## 预处理决策

- MATRIX 直接用（无需 vec_avg）；cov≥0.83 无需 ts_backfill；salrevise cov 0.68 边缘仍免（>0.4）
- pred_surps 已标准化但偏态可能 → rank 强制；nums 计数 → rank 强制
- 窗口纪律：1/5/22/66 标准窗
