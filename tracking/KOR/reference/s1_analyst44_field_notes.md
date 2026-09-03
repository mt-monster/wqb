# S1 字段理解：analyst44（KOR/TOP600/D1）

- 数据集类型：540 字段（VECTOR 374 / MATRIX 166），EPS 修订族 coverage=1.0
- 主题：分析师一致预期修订（EPS/DPS/sales/net_debt 4 周修订幅度与方向计数）

## 字段/特征/建议

- 特征：4 周滚动修订快照（事件流但近每日更新）；修订幅度字段带符号、计数字段非负偏态；EPS 修订族极冷门（3 字段 users=0）
- 建议：主信号 = eps_estimate_4wk_change / eps_gaap_estimate_4wk_change（users=0）；辅助 = up/down count 做 breadth、dps_4wk_chg 做股息腿；ts_backfill 补洞；22 日持续性；sector 组内相对化
- 风险提示：anl44_second_*/anl44_2_* 两大族覆盖低（0.53-0.67）禁用；analyst 类 KOR 已有 win 但同族饱和，本集未试；consensus 修订动量为经典异象，KOR 方向需实证

## 初始信号

1. EPS 4 周修订幅度（eps_estimate_4wk_change，正向：上调→漂移）
2. GAAP EPS 4 周修订（eps_gaap_estimate_4wk_change，正向）
3. 股息修订（anl44_best_dps_4wk_chg，正向）

## 进阶信号

- 修订宽度：up_count − down_count
- 持续性：ts_mean(vec_avg(change), 22)
- sector 组内相对：group_rank(rank(change), sector)
- 事件门控：trade_when 门控修订发生日

## 预处理决策

- VECTOR 滚动快照 → vec_avg 聚合
- 日间无更新 → ts_backfill 补洞
- 计数偏态 → rank 强制；幅度字段有符号 → rank 后直接用方向
