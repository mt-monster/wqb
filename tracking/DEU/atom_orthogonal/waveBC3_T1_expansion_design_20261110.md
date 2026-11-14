# Wave BC3 设计 — T1 现金利润率三维扩展（水平/稳定性/斜率），待 BD1/BC2 腾槽

> 动机：T1（S1.15/2Y0.43）的 2Y 需组合腿救（BC2 在飞），但 **S 缺口 0.43 还有单数据集强化空间**。
> 核心洞察：**现金流稳定性（低波动=高质量）与 T1 的水平面正交**，且 vol 面在 DEU 已被多次验证（news18 N4 0.57、earningscall T6、BA3b vol 族）。

## 十条臂（全部单数据集 fundamental6，纯 ATOM 路线）

| # | 表达式 | 维度 | 机制 |
|---|---|---|---|
| E1 | group_rank(divide(fnd6_oancfy, fnd6_revty), sector) | 水平 | **T1 基线（S1.15 已有）**，对照锚 |
| E2 | -group_rank(ts_std_dev(divide(ts_backfill(fnd6_oancfy,66), ts_backfill(fnd6_revty,66)), 252), sector) | 稳定性 | 现金流利润率低波动=盈利质量高（Novy-Marx 质量） |
| E3 | group_rank(ts_zscore(divide(ts_backfill(fnd6_oancfy,66), ts_backfill(fnd6_revty,66)), 504), sector) | 水平异常 | 自身基线 zscore（其他47 T2 验证过的几何） |
| E4 | group_rank(ts_delta(divide(ts_backfill(fnd6_oancfy,66), ts_backfill(fnd6_revty,66)), 252), sector) | 斜率 | 现金利润率变化（改善趋势） |
| E5 | group_rank(divide(fnd6_oancfy, add(fnd6_cptnewq_atq, 1)), subindustry) | 水平换分母 | 现金资产回报率（换分母避覆盖偏差） |
| E6 | group_rank(divide(fnd6_oancfy, fnd6_newa2_sale), subindustry) | 水平换分母 | 现金销售率 |
| E7 | -group_rank(multiply(ts_std_dev(divide(ts_backfill(fnd6_oancfy,66), ts_backfill(fnd6_revty,66)), 252), -1), industry) | 稳定性换轴 | 同 E2 换 industry 轴 |
| E8 | group_rank(ts_ir(divide(ts_backfill(fnd6_oancfy,66), ts_backfill(fnd6_revty,66)), 252), subindustry) | 信噪比 | 现金流利润率的信息比率 |
| E9 | group_rank(ts_target_tvr_decay(divide(ts_backfill(fnd6_oancfy,132), ts_backfill(fnd6_revty,132)), target_tvr=0.03), sector) | 水平+治理 | T1 加 tvr_decay（BC2 B5 的变体轴） |
| E10 | group_rank(ts_rank(divide(ts_backfill(fnd6_oancfy,66), ts_backfill(fnd6_revty,66)), 252), sector) | 非线性 | 现金利润率的 52 周分位（非线性保序） |

算子数全部 ≤8；窗口白名单 66/252/504（月/年/两年）。

## 出口

- 若任一臂 S ≥ 1.4 且 2Y ≥ 0.8 ⇒ 与 BC2 的组合腿二次组合或直接破闸。
- 若全部 S < 1.2 ⇒ T1 的 1.15 就是该机制的极限，DEU 上限确证。

## 前置

- 待 BD1/BC2 收割后派发（并发 2 + AN 僵尸）。
- 全部字段已在 fundamental6_fields.csv 核实存在（oancfy/revty/cptnewq_atq/newa2_sale）。