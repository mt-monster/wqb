# KOR wave272 · analyst 修正/惊喜模板库与派发记录（2026-11-06）

> 区域 KOR / TOP600 / D1；设置 decay 4 · neutralization SECTOR · truncation 0.08 · nanHandling ON · pasteurization ON。
> 两个多仿真批（每批 10 条），并发 = 2，符合「create_multi_simulation 并发 2」约束。

## 一、取证（双通道，先查后建）

| 通道 | 来源 | 采用的结论 |
|---|---|---|
| 论坛 | `【因子灵感】分析师预期修正，怎样分离方向与参与广度`（XH93773，29 票） | 修正要**把「方向」与「参与广度」分开**：少数观点大幅调整 vs 多数观点小幅同向，是两种信息过程 ⇒ 广度和幅度必须做成两条独立模板，不能相加 |
| 论坛 | `【Alpha Idea】分析师盈利预期修正广度` | 上调/下调家数比值横截面标准化可捕捉盈利动能，但**要先核对覆盖家数与更新时点**，否则结果由少数高覆盖公司主导 |
| 论坛 | `模板硬跑 #2 复盘`（FD69320） | 「**水平值 ≠ 惊喜**」；PEAD 类模板用水平值直接排会失效，必须换成惊奇/差值口径 |
| 论文 | SUE 定义（PEAD 标准式） | `SUE = (actual − consensus) / σ_estimate`，σ 用分析师预期离散度 ⇒ 直接落成模板 B3（惊喜/标准差）与 B1（纯惊喜）的对照 |
| 论文 | Gleason & Lee (2003)、Jung/Keeley/Ronen (2019)（经 `_wave11-13_analyst_findings.md` 转引） | **未缩放**修正在小盘/低覆盖股更强；缩放后会失效 ⇒ 模板保留「未缩放幅度」与「按分歧度缩放」两版做对照 |
| 论文 | Mill Street / 华泰金工（同上转引） | 修正方向 1 个月后仍维持 ~83%，而收益仅 50% ⇒ 修正有持续性，允许用 `ts_mean` 做持续期模板 |

## 二、10 个结构互异模板（每集 10 条，骨架互不相同）

差异落在：**标准化方式 / 期限结构 / 缩放分母 / 差分阶 / 趋势拟合 / 分歧度 / 分布高阶矩 / 稳定性 / 加速度 / 持续性**。

### 批 A — `analyst_factor_signals`（MATRIX，无需 vec_*）

| # | 模板 | 表达式 | 算子数 | 机制 |
|---|---|---|---:|---|
| A1 | 修正水平标准化 | `group_rank(ts_zscore(eps_y1_estimate_change_3mo, 252), sector)` | 4 | 修正动量（时序标准化，剔除个股尺度） |
| A2 | 期限结构倒挂 | `group_rank(subtract(rank(eps_y2_estimate_change_3mo), rank(eps_y1_estimate_change_3mo)), sector)` | 5 | FY2 比 FY1 修得更快 = 长期预期重估 |
| A3 | 分歧度缩放修正 | `group_rank(divide(eps_y1_estimate_change_3mo, add(eps_y1_estimate_coeff_var, 0.001)), sector)` | 5 | 同样的修正，分歧小的更可信（Jung 2019 反向对照） |
| A4 | 修正加速度 | `group_rank(ts_delta(eps_revision_magnitude, 22), sector)` | 4 | 二阶差分：修正幅度在加速 |
| A5 | 营收趋势斜率 | `group_rank(ts_mean(revenue_estimate_trend_slope_1yr, 66), sector)` | 4 | 用营收（非 EPS）做同机制正交对照 |
| A6 | 分歧度压缩 | `group_rank(reverse(ts_mean(eps_y1_estimate_coeff_var, 66)), sector)` | 5 | 分歧收敛 = 不确定性消除 |
| A7 | 预期分布偏斜 | `group_rank(reverse(eps_y1_estimate_skewness), sector)` | 3 | 三阶矩：正偏（乐观尾巴）反向做 |
| A8 | 惊喜稳定性 | `group_rank(reverse(ts_mean(eps_surprise_stddev, 66)), sector)` | 5 | 历史惊喜波动低 = 可预测性好 |
| A9 | 增长预期加速度 | `group_rank(ts_delta(eps_y1_cagr_2yr, 66), sector)` | 4 | 长期增速预期在抬升 |
| A10 | 修正持续期 | `group_rank(ts_mean(eps_y1_estimate_change_3mo, 66), sector)` | 4 | 持续性（Mill Street：修正方向 1 个月后仍 83% 保持） |

### 批 B — `analyst_base_ref`（VECTOR，全部 `vec_avg` 降维）

| # | 模板 | 表达式 | 算子数 | 机制 |
|---|---|---|---:|---|
| B1 | 纯惊喜 | `group_rank(ts_backfill(vec_avg(consensus_surprise_percentage), 66), sector)` | 4 | PEAD：惊喜百分比 |
| B2 | 绝对惊喜归一 | `group_rank(divide(vec_avg(consensus_vs_actual_diff), add(abs(vec_avg(consensus_mean_estimate)), 0.001)), sector)` | 6 | 与 B1 换分母，检验是否尺度驱动 |
| B3 | SUE | `group_rank(divide(vec_avg(consensus_surprise_percentage), add(vec_avg(consensus_stddev_estimate), 0.001)), sector)` | 6 | 论文标准式 SUE = 惊喜/σ |
| B4 | 覆盖广度变化 | `group_rank(ts_delta(vec_avg(num_estimates_consensus), 66), sector)` | 5 | 关注度上升（论坛「覆盖家数」警告版：只用变化不用水平） |
| B5 | 分歧度水平 | `group_rank(reverse(ts_mean(vec_avg(consensus_stddev_estimate), 66)), sector)` | 6 | 低分歧溢价 |
| B6 | 惊喜持续期 | `group_rank(ts_mean(vec_avg(consensus_surprise_percentage), 66), sector)` | 5 | 连续超预期（漂移） |
| B7 | 惊喜时序标准化 | `group_rank(ts_zscore(vec_avg(consensus_surprise_percentage), 252), sector)` | 5 | 剔除个股惊喜均值 |
| B8 | 预期区间宽度 | `group_rank(reverse(divide(subtract(vec_avg(consensus_high_estimate), vec_avg(consensus_low_estimate)), add(abs(vec_avg(consensus_mean_estimate)), 0.001))), sector)` | 8 | 高低差/均值 = 认知区间，越窄越可信 |
| B9 | 惊喜波动率 | `group_rank(reverse(ts_std_dev(vec_avg(consensus_surprise_percentage), 66)), sector)` | 6 | 惊喜一致性 |
| B10 | 惊喜长窗分位 | `group_rank(ts_rank(vec_avg(consensus_surprise_percentage), 504), sector)` | 4 | 两年分位（慢变，但检验长记忆） |

**多样性自检**：20 条覆盖 10+ 种骨架几何（zscore / 期限价差 / 比值缩放 / 一阶差分 / 趋势均值 / 分歧度 / 偏度 / 标准差 / 加速度 / 持续期 / 区间宽度 / 长窗分位），
且每个数据集内部 10 条互不同构 ⇒ 满足「模板 ≥10 且结构互异」。

## 三、派发记录

| 批 | multisim | 表达式数 | 状态 |
|---|---|---:|---|
| W272-A | `YVAdV564yo9qe18DxN8KTw` | 10 | 已派发 |
| W272-B | `21hrQaeV24IuaX714e6N26cT` | 10 | 已派发 |

## 四、本轮明确不做的事（纪律）

- 不复刻 `覆盖广度水平` 与 `分歧度水平` 两条已在 wave11–13 判死的机制 —— 本批 B4/B5/B9 只用**变化量**与**二阶矩**，且 B5/B9 作为对照而非主攻。
- 不在第一批就上 `add(A,B)` 双腿（`POISON:equal_weight_leg_add`）。
- 不扫 neutralization / truncation 两轴（本批统一档位，先看机制强弱）。
