# analyst_consensus（目标价一致预期族）字段画像与回测（USA / TOP3000 / D1，2026-10-20）

> 命名：`_usa-<字段前缀>-field-profile-<asOf>.md`｜本集前缀 **analyst**（数据集 `analyst_consensus`）
> 三段式：**字段画像 → 适用模板 → 回测结果及指标**，末尾判读。
> 本页覆盖**目标价（targetprice_annual12_tribes）10 字段**这一被实测过的子族；数据集另有 EPS/营收等族，不在本页范围。
> **全字段清单（300 VECTOR + 10 MATRIX，含覆盖/uc/aC/可用性档位）→**
> [`_usa-analyst-consensus-field-inventory-20261020.md`](_usa-analyst-consensus-field-inventory-20261020.md)。

## 0. 路由与元数据

| 项 | 值 |
|---|---|
| dataset id | `analyst_consensus`（平台 `get_datafields` 实测，2026-10-20） |
| 字段类型 | 全部 **MATRIX** |
| 本子族覆盖 | **0.9592**（10/10 字段同一覆盖） |
| 塔 / 状态 | USA/D1 ANALYST（已点亮）；PV 分类同时出现在部分 alpha（multiplier 1.1–1.2） |
| 拥挤度 | 目标价族 aC 1–28、uc 1–20（远低于 revision/surprise 族） |

## 1. 字段画像

### 1.1 目标价一致预期 10 字段（平台实测）

| 字段 | 含义 | 覆盖 | uc / aC |
|---|---|---:|---|
| `mean_estimate_targetprice_annual12_tribes` | 目标价一致预期均值（原始币种） | 0.9592 | 20 / 28 |
| `median_estimate_targetprice_annual12_tribes` | 目标价中位数（原始） | 0.9592 | — |
| `min_estimate_targetprice_annual12_tribes` | 最低目标价 | 0.9592 | 1 / 1 |
| `max_estimate_targetprice_annual12_tribes` | 最高目标价 | 0.9592 | 4 / 9 |
| `mean_estimate_fxadj_targetprice_annual12_tribes` | 均值（汇率/拆股调整后） | 0.9592 | 16 / 22 |
| `median_estimate_fxadj_targetprice_annual12_tribes` | 中位数（调整后） | 0.9592 | 3 / 4 |
| `min_estimate_fxadj_targetprice_annual12_tribes` | 最低（调整后） | 0.9592 | 1 / 2 |
| `max_estimate_fxadj_targetprice_annual12_tribes` | 最高（调整后） | 0.9592 | 6 / 6 |
| `stddev_estimate_fxadj_targetprice_annual12_tribes` | 分析师间标准差（分歧度） | 0.9592 | 12 / 18 |
| `estimate_count_current_period_targetprice_annual12_tribes` | 参与一致预期的分析师人数 | 0.9592 | 11 / 15 |

### 1.2 分布与更新

- 目标价是**价格量纲**（非无量纲比率）；跨股票直接比较会被股价/市值放大 ⇒ 必须用 `ts_zscore`（对自身历史）或组内 `group_rank`，**不要用原始水平做横截面**。
- 汇率调整族（`*_fxadj_*`）与原始族同覆盖，但 `mean` 与 `median` 的差只有在**同一口径**下才有意义（原始对原始、调整对调整）。
- 更新频率：随分析师报告（日频有变动、但多数股票稀疏）⇒ 天然低换手。
- 可构造的**无量纲形状量**：`(mean−median)/stddev`（偏度）、`(max−min)/mean`（相对极差）、`stddev/mean`（变异系数）、`(mean−min)/(max−mean)`（上下不对称）。

## 2. 适用模板

### 2.1 已交付族 A：**离散度 × 共识偏斜方向**（queue 验证）

```
quantile(group_rank(ts_mean(if_else(greater(mean_estimate_targetprice_annual12_tribes,
                                         median_estimate_targetprice_annual12_tribes),
                                   stddev_estimate_fxadj_targetprice_annual12_tribes,
                                   reverse(stddev_estimate_fxadj_targetprice_annual12_tribes)),
                          20), subindustry), sigma=1.0)
```
设置：USA/TOP3000/D1，decay **500**，neutralization **STATISTICAL**，trunc 0.08。
机制：共识右偏（均值>中位数）时做多分歧度，左偏时做空分歧度 —— **分歧的方向由共识偏斜决定**。

### 2.2 已交付族 B：**目标价一致预期的时序位置**（queue 验证）

```
group_rank(ts_zscore(mean_estimate_targetprice_annual12_tribes, 175), subindustry)
```
设置：同区，neutralization **STATISTICAL**。
机制：一致预期相对自身 175 日历史的位置 ⇒ 目标价的修正趋势（不是绝对价位）。

### 2.3 本轮新机制批 25：四种正交读数（同一 ATOM 数据集）

通用壳：`quantile(group_rank(hump(ts_backfill(winsorize(SIGNAL, std=4), 252), hump=0.01), subindustry))`
设置：USA/TOP3000/D1，decay **20**，neutralization **REVERSION_AND_MOMENTUM**，trunc 0.08。

| # | 机制 | SIGNAL |
|---:|---|---|
| 1 | 目标价修正（3 月） | `ts_av_diff(mean_estimate_fxadj_targetprice_annual12_tribes, 63)` |
| 2 | 覆盖人数变化 | `ts_av_diff(estimate_count_current_period_targetprice_annual12_tribes, 63)` |
| 3 | 共识偏度 | `ts_zscore(subtract(mean_fxadj, median_fxadj), 252)` |
| 4 | 相对极差 | `ts_zscore(subtract(max_fxadj, min_fxadj), 252)` |
| 5 | 分歧变化 | `ts_av_diff(stddev_fxadj, 63)` |
| 6 | 分歧水平 | `ts_zscore(stddev_fxadj, 252)` |
| 7 | 覆盖人数水平 | `ts_zscore(estimate_count_current_period, 252)` |
| 8 | 变异系数 | `ts_zscore(divide(stddev_fxadj, mean_fxadj), 252)` |

### 2.4 批 27：中性化 / 分组轴定向 A/B（2×8）

批 26 归因（§3.3）证明 backfill / window / winsor / decay 不是 F 的杠杆 ⇒ 唯一未测的两把杠杆是
**中性化**与 **分组轴**。设计成两个平行 multisim，**信号完全相同、只有设置不同**：

- 27a：`STATISTICAL`，decay 20（族 A/B 已验证 STATISTICAL 能同时抬 S 与 F）；
- 27b：`CROWDING`，decay 20（交付 `kqJLawqP` 用的中性化）。

| # | SIGNAL（同 §2.3 壳） | 测什么 |
|---:|---|---|
| 1 | `ts_av_diff(estimate_count_current_period_targetprice_annual12_tribes, 63)` | 基线（批 25 近失机制）× 新中性化 |
| 2 | 同 #1 窗口 **126** | 2Y 最优变体（批 26 `Vkd3KLrJ` 2Y1.91）× 新中性化 |
| 3 | `ts_av_diff(vec_avg(average_analyst_projection_noshareout_qtr), 63)` | 未测族：预测均值水平漂移（cov 0.8924） |
| 4 | `ts_av_diff(vec_avg(analyst_estimate_count_noshareout_qtr), 63)` | 未测族：人数广度的另一口径（cov 0.8924） |
| 5 | `ts_av_diff(vec_avg(average_surprise_fx_adjusted_qtr), 63)` | 未测族：fxadj 意外（cov 0.5357 ⇒ backfill **504**） |
| 6 | `ts_av_diff(vec_avg(average_forecast_actual_value_noshareout_qtr), 63)` | 未测族：预测+实际混合均值漂移（cov 0.8924） |
| 7 | `ts_av_diff(vec_avg(avg_net_income_3mth_prior), 63)` | 未测机制：**滞后修订**（3 个月前的共识在过去 63 日的变化，cov 0.9121） |
| 8 | 同 #1 但 `group_rank(..., market)`（27a）/ `industry`（27b） | **分组轴**杠杆（批 25/26 全为 subindustry） |

判据（先写死）：若某设置下 #1/#2 的 F 仍 <1.0 且 S 无 +8% 提升 ⇒ REVERSION_AND_MOMENTUM 之外的两把中性化也无效，
count 机制判定为**结构性差 F**，不再磨参；#3–#7 中任一条 S≥1.58/F≥1.0/2Y≥1.58/SUB≥0.75 即进相关性实测。

**实际结局（批 27，§3.4）**：判据的前半段不成立 —— `CROWDING × industry` 下 count Δ63 达 S1.73/F1.03/2Y1.83/SUB0.92，
**F 不再缺**；constraint 从「F 差 0.08」翻转成「TO 0.90% 差 0.1pp」。故不走「判死」，走批 28 的换手修复。

### 2.5 批 28：count breadth 的换手修复（单机制、7 个破 LOW_TURNOVER 杠杆 + 1 对照）

锁定信号与设置：`estimate_count_current_period_targetprice_annual12_tribes` Δ63、`group_rank(..., industry)`、
`CROWDING`、trunc 0.08、其余壳不变。目标只有一个：**TO 0.90% → ≥1.0%**，同时 S/F/2Y/SUB 不得退化到闸外。

| # | 变更 | 预期机制 |
|---:|---|---|
| 1 | `hump=0.005`（decay 20） | 收窄死区 ⇒ 提高换手（首选，最小改动） |
| 2 | 去 `hump`（decay 20） | 无死区 ⇒ 换手最大，风险是 S 抖动 |
| 3 | decay **10**（hump 0.01） | 缩短平滑记忆 ⇒ 提高换手 |
| 4 | decay **5**（hump 0.01） | 同上更强 |
| 5 | `hump=0.005` + decay **10** | 两杠杆叠加 |
| 6 | 去 `hump` + decay **10** | 极值 |
| 7 | Δ63 → **Δ42**（hump 0.01, decay 20） | 更短记忆 ⇒ 换手 + 信号略快 |
| 8 | 去 `quantile`（只留 `group_rank`） | 权重形态杠杆（对照，判断 TO 是否由 quantile 归一化压住） |

判据（写死）：**TO ≥ 1.0% 且 S≥1.58 / F≥1.0 / 2Y≥1.58 / SUB≥0.75** 即视为通过，跑 `check_correlation(refresh=True)`；
若 7 个杠杆全都无法在保 S/F/2Y 的前提下把 TO 抬过 1%，则 count 机制判定为**结构性低换手**（数据更新频率决定的，
不是壳参数问题），封存并转 EPS fxadj / actual_* 报表族，不再磨。

**实际结局（批 28，§3.5）**：8 个杠杆全部失败，判据触发 ⇒ **count breadth 封存为结构性低换手**。
根因不是壳没调对，而是 TO 与 S 沿 decay/hump 轴**单调对立**：任何把 TO 抬到 1% 以上的变体都同时丢掉 ≥0.23 S。
死区/hump 本身就是 alpha 的来源（去 hump 后 2Y 直接变负）。

### 2.6 机制模板矩阵（**不封顶 8 个**；8 只是 multisim 单批容量）

> 纪律（2026-10-20 用户纠正后固化）：**经济机制模板必须按字段族的经济含义充分展开，不得把「8 条一批」
> 误当成「8 个机制」。** 每批 ≤10 条是平台容量；机制清单是**待办矩阵**，做完一批就补下一批，
> 直到每个字段族的每种经济读数都有实测结论（交付 / 判死 / 待测三态）。下面的矩阵是本集的机制台账。

| # | 经济机制 | 字段构造（同一数据集内） | 模板/算子 | 状态 |
|---:|---|---|---|---|
| M01 | 收入增长漂移 | `actual_revenue_value_quarterly16` | Δ63/Δ126 + 通用壳 | ❌ 判弱（CROWDING 下 S1.25，§3.6）；RAM×Δ63 复测 `zqrRjbLX` S1.36/F0.89/2Y1.56/SUB0.46（差 2Y 0.02 但 SUB 缺口）⇒ **只给一次测量口径复测**（批 33 M52，§3.13） |
| M02 | 净利润增长漂移 | `actual_netprofit_value_quarterly16` | Δ63/Δ126 + 通用壳 | ❌ 判弱（S1.27/2Y0.44，§3.6）；同上 |
| M03 | EBIT 增长漂移 | `actual_ebit_value_quarterly16_2` | Δ63/Δ126 + 通用壳 | ❌ 判死（S1.03，§3.6） |
| M04 | EPS 增长漂移 | `actual_eps_value_quarterly16` | Δ63/Δ126 + 通用壳 | ❌ 判死（S0.92，§3.6） |
| M05 | 资本开支扩张 | `actual_capex_value_quarterly16` | Δ63（反向）+ 通用壳 | ❌ 判死（S0.49，§3.6） |
| M06 | 自由现金流增长 | `actual_fcf_value_quarterly16` | Δ63 + 通用壳 | ❌ 判死（S0.70，§3.6） |
| M07 | 去杠杆 | `actual_netdebt_value_quarterly16` | Δ63（反向）+ 通用壳 | ❌ 判死（S0.49，§3.6） |
| M08 | ROE 趋势 | `actual_value_roe_quarterly16` | Δ63 + 通用壳 | ❌ 判死（S0.70，§3.6） |
| M09 | 净利率趋势 | netprofit / revenue | 比率水平 + Δ63 | ❌ 判弱（S1.49/2Y1.11/**SUB −0.16**，§3.7） |
| M10 | 毛利率/EBIT 率趋势 | EBIT / revenue | 比率 + Δ63 | ❌ 判弱（2Y1.98 但 **SUB −0.22**，小盘反向不可救，§3.7） |
| M11 | 现金流转化质量 | FCF / netprofit | 比率 + Δ63 | 待测 |
| M12 | 应计质量（反向） | (netprofit − FCF) / total_assets | 水平 + Δ63（反向） | 待测 |
| M13 | 杠杆率趋势 | netdebt / (netdebt + tangbookvalue) | 比率 + Δ63 | 待测 |
| M14 | 资本开支强度 | capex / revenue | 比率 + Δ63（反向） | 待测 |
| M15 | 资产周转率趋势 | revenue / total_assets | 比率 + Δ63 | 待测 |
| M16 | ROA 趋势 | netprofit / total_assets | 比率 + Δ63 | 待测 |
| M17 | 股本稀释（反向） | `actual_sharesoutstanding_value_annual12` | Δ252（反向） | 待测（年度口径 ⇒ 低换手风险） |
| M18 | 有形账面价值增长 | `actual_tangbookvalue_value_annual12_tribes` | Δ252 | 待测 |
| M19 | 总资产扩张 | `actual_total_assets_value_annual12` | Δ252 | 待测 |
| M20 | EPS 与净利背离（稀释效应） | EPS 增速 − 净利增速 | 二者差 + Δ63 | 待测 |
| M21 | 目标价隐含盈利倍数 | targetprice / actual EPS | 水平/Δ63 | 待测 |
| M22 | 目标价时序位置 | mean targetprice | `ts_rank/ts_zscore` | ✅ 已交付 #6 |
| M23 | 共识偏斜 × 分歧 | mean−median × stddev | trade_when/条件 | ✅ 已交付 #5 |
| M24 | 覆盖广度 | estimate_count | Δ63 + CROWDING | ❌ 封存（§3.5，结构性低换手） |
| M25 | 预测修正速度 | targetprice mean | Δ63 | ❌ 判弱（批 25/26） |
| M26 | 分歧度/形状量 | stddev/skew/range | z252 | ❌ 判死（批 25） |
| M27 | 财报意外 | surprise 族 | Δ63 / ts_sum | ❌ 判死（批 26/27 ×2 中性化） |
| M28 | 预测+实际合并均值漂移 | `mean_forecast_actual_combined_fxadj_eps_annual12` | Δ63/Δ126 + 通用壳 | **本集最强机制，已交付**：`e76xgXkM` = `ts_zscore(Δ63,252)` + RAM/industry **S1.89/F1.12/2Y1.76/SUB1.05/TO3.29%，RA 全过，prod 0.5532 / self 0.4553**（§3.9）；门控版 `78on0e78` S2.19/F1.48/2Y2.46/SUB1.05 但 prod 0.7214 挂起 |
| M29 | 应计距离（利润−现金） | (netprofit − cfo)/total_assets（annual12）或 (netprofit − fcf)/total_assets（短窗） | 比率 + Δ63/Δ252（反向） | **封存（批 31，§3.12）**：`78onQ6m5` 1.21/0.78/1.31、`KPmE6rQk` 1.33/0.88/1.33；**SUB 0.87/0.76 反而全过** ⇒ 高低流动性配比没问题，是原始收益强度不足（高质量低收益），不是可交付信号 |
| M30 | 财务质量复合（ROE × 现金销售比） | ROE × cfo/revenue | 乘积 + 秩 | **封存（批 31）**：`wp9E1bP2` 1.13/0.73/1.35/SUB0.73；水平型质量信号在 RAM 下收益强度不足 |
| M31 | 财报发布窗口门控 | 质量/修正信号 × `forecast_actual_flag_*` | `trade_when` | **封存（含误读更正）**：字段为三值 `0 backfilled / 1 consensus forecast / 2 actual report`。批 31 `flag>0.5`（= 1+2，cov 0.9779）`LL5d6Z3a` S1.67/F1.07/2Y1.49/SUB0.64 **低于全样本**；`flag≤0.5`（= backfill-only）`O0Jxk8gp` S−0.83 ⇒ **backfill 行信号反转**，不是「预测/已报 regime 相反」。M31 封存，§3.13 M50 已取消 |
| M32 | 存货占用（反向） | `actual_inventory_value_fxadj_annual12` / revenue | 比率 + Δ252（反向） | **封存（批 31）**：`JjPvmQr2` S0.65/F0.31，CW 0.294（limit 0.1，2014-01-07）；覆盖率 0.5966 的结构性缺口已实测确认 |
| M33 | 合并总资产修正动量 | `mean_forecast_actual_combined_fxadj_total_assets_annual12`（0.8937） | Δ63 + 通用壳 | 待测（批 31 备选；资产负债表扩张预期） |
| M34 | 流动资产强度 | `actual_currentassets_value_fxadj_annual12`（0.7212）/ revenue | 比率 + Δ63 | 待测（批 31 备选） |
| M35 | 预期修正**加速度** | 合并 EPS/营收序列 | `ts_av_diff(ts_av_diff(x,63),63)` 或 `ts_delta(ts_av_diff(x,63),63)` | **差测量口径（批 31）**：`Grge6O7P` S1.75/F0.99/2Y1.58/SUB0.40 ⇒ F 差 0.01、SUB 缺口；按 30c 方法论给一次 `ts_zscore(·,252)` 复测（批 33 M51），仍 SUB<0.43×S 则封存 |
| M36 | 预期水平时序位置（EPS） | `mean_forecast_actual_combined_fxadj_eps_annual12` | `ts_rank`/`ts_zscore` 长窗 | 待测（M22 同族不同字段；self-corr 风险需与 #1/#6 实测） |
| M37 | 修正广度（多口径同向） | EPS + 营收 + EBIT 合并序列的修正方向 | 三方向计数/秩平均 | 待测但**风险高**：三字段合成易触发「禁混信号」红线，仅在与用户确认后可测 |
| M38 | 修正**持续性**（节奏） | 合并 EPS 的 Δ5 | `ts_product(Δ5, 5)`：连续 5 日同向修正的强度（论坛移植，§3.10） | **量纲失配**（`A1Q7Yojg` S−1.41/SUB−0.60，被 hump 归零）；30d 用 `ts_product(ts_zscore(Δ5,252),5)` 复测 |
| M39 | 修正**阈值门控**（节奏） | 合并 EPS 的 Δ22 | `trade_when(abs(ts_zscore(Δ22,66))>1.5, Δ22, 0)`：只在修正幅度 >1.5σ 时持仓 | **已测** `78on0e78` S2.19/F1.48/2Y2.46/SUB1.05（全场最强）；prod 0.7214 超线 0.0214、直方图 [0.7,0.8) n=1 ⇒ 挂起 |
| M40 | **同行相对**修正 | 合并 EPS 的 Δ63 | `group_zscore(Δ63, industry)` 先做行业内相对化再进壳 | **已测** `ZYmKqOPQ` 1.87/1.20/1.45/SUB0.88：SUB 过、2Y 差 0.13 ⇒ 正交备胎 |
| M41 | 修正**慢版本** | 合并 EPS 的 Δ63 | `ts_mean(Δ63, 22)` 或 `ts_mean(clean,120)` | **已测** `1Yjz1rYm` 1.88/1.17/1.21/0.62：2Y 塌，平滑牺牲近年记忆 |

优先级：M09–M16 是**比率型机制**（同一数据集两个字段相除，不是混信号）；M18–M20 是年度口径慢变量
（先解决 TO 下限问题再投入）；M21 用目标价与实际 EPS 构造隐含倍数。每条机制先测一个代表性字段，
有信号才展开算子替换（`ts_rank` / `ts_zscore` / `ts_av_diff` / 长窗微分），**无信号不扫参**。

### 2.7 论坛 / 外部证据（可复用结论）

| 来源 | 结论 | 对本集的用法 |
|---|---|---|
| [利润和现金流的距离：应计质量的一种观察](https://support.worldquantbrain.com/hc/en-us/community/posts/43808003274007)（28 票，2026-09-28） | 用**净利润、经营现金流、总资产构造尺度统一的差异**，避免只看金额大小；该差异不是舞弊判据，适合做风险筛查 | M29：`(netprofit − cfo)/assets` 或 quarterly16 代理 `(netprofit − fcf)/revenue`，**反向**使用 |
| [华泰单因子测试之财务质量因子](https://support.worldquantbrain.com/hc/en-us/community/posts/19140285170199)（14 票，2023-11-17） | ① 财务质量因子数据滞后、单独用一般；② **现金流/收入 × ROE 相乘**可放大信号；③ 按市值分组中性化更好；④ 效果集中在**年报发布窗口**（3–4 月），与动量/择时结合才显著 | M30 乘法复合；M31 用 `forecast_actual_flag_*` 做财报窗口门控；分组轴用 industry/market（本集无市值字段，`market` 是豁免分组） |
| [【Alpha Idea】分析师修正当成节奏，而不是评分](https://support.worldquantbrain.com/hc/en-us/community/posts/43878933562391)（GZ47187，2026-09-30） | ① **不要追单次修正，要等连续同向修正**（`ts_product(clean,5)` 在 analyst16 上 S2.95/F3.05）；② 只在修正幅度 >1.5σ 时交易（`trade_when` + `ts_zscore`）；③ 同行相对修正（`group_zscore`）；④ 慢版本 `ts_mean(clean,120)` 的 margin 最高（0.01183）、TO 仅 2.45% | M38–M41（§3.10）。⚠ 帖中字段是**修正分量**（可正可负），本集是 **EPS 水平值（恒正）** ⇒ `ts_product` 必须改对**差分**做，且字段一律不照搬（破 ATOM） |

⚠ 两条都是**论坛经验，不是本区实测**：先按上面的最小机制各测 1 条，有信号再展开；
不得直接照搬帖中 `mdl175_*` 字段（跨数据集，破 ATOM）。

## 3. 回测结果及指标

### 3.1 族 A / 族 B（submit_ready 队列，全部闸 + prod/self 实测）

| 族 | alpha | S | F | 2Y | SUB | TO | prod | self | 判定 |
|---|---|---:|---:|---:|---:|---:|---:|---:|---|
| A | `pw5RbrYX` | 2.07 | 1.21 | 1.67 | 0.90 | 3.75% | ~~0.5857~~ **0.9000** | 0.3495 | ❌ **prod 墙**（2026-10-21 refresh 实测） |
| A | `RR6bv6rz` | 2.04 | 1.20 | 1.71 | 0.89 | 3.82% | 0.5919 | 0.3566 | 同族（窗口 10） |
| A | `rKeOaLvo` | 2.04 | 1.20 | 1.71 | 0.89 | 3.83% | 0.5932 | 0.3567 | 同族（decay 512） |
| A | `leKKGb9l` | 2.04 | 1.19 | 1.66 | 0.92 | 3.78% | ~~0.5896~~ **0.9014** | 0.3547 | ❌ **prod 墙**（2026-10-21 refresh 实测） |
| B | `KPrGMEe1` | 1.94 | 1.24 | 1.71 | 1.04 | 5.94% | **0.6593** | 0.4277 | 可提交（余量 0.041） |
| B | `KPrGp2G8` | 1.93 | 1.23 | 1.72 | 1.01 | 6.00% | 0.6649 | 0.4268 | 同族 |
| B | `rKe2woad` | 1.92 | 1.21 | 1.73 | 0.98 | 6.04% | 0.6697 | 0.4253 | 同族 |

⇒ **族 A 与族 B 只有一族的代表可计入交付**（族内近重复），当前各取 1 颗。

> ⚠ **2026-10-22 更正（本表 prod 列已过期，勿按原判定提交）**：`pw5RbrYX` / `leKKGb9l` 的
> 0.5857 / 0.5896 是 2026-10-17 的**入库值**，2026-10-21 `check_correlation(refresh=True)` 复测已是
> **0.9000 / 0.9014**，2026-10-22 复测一致 ⇒ 两只均为 **D0-P `dead_end`（≥0.75）**，不是「可提交」。
> 同族 `RR6bv6rz` / `rKeOaLvo`、族 B `KPrGMEe1` / `KPrGp2G8` / `rKe2woad` 的入库值同样未刷新，
> 进入交付表前必须逐只 `refresh=True` 复测。漂移机制与全族读数见
> [`_usa-analyst-consensus-fa-overlay-field-profile-20261021.md`](_usa-analyst-consensus-fa-overlay-field-profile-20261021.md) §9.6。

### 3.2 批 25（新机制，multisim `4xGNrAgXc4DrbUTSwac8pcp`，8/8 COMPLETE）

设置：USA / TOP3000 / D1 / **REVERSION_AND_MOMENTUM** / **decay 20** / trunc 0.08。

| # | alpha | 机制 | S | F | 2Y | SUB | TO | 判定 |
|---:|---|---|---:|---:|---:|---:|---:|---|
| 1 | `88vegpLa` | Δ63 目标价均值 | 1.44 | 0.81 | 1.32 | 0.59 | 3.67% | 四闸不过 |
| 2 | **`pwvKQN7x`** | **Δ63 覆盖人数** | **1.65** | **0.92** | **1.71** | **0.92** | 3.31% | **只差 F 0.08** |
| 3 | `78ongzd5` | z252(均值−中位) | 1.35 | 0.67 | 0.43 | −0.04 | 3.67% | 四闸不过 |
| 4 | `O0JxKGpv` | z252(最大−最小) | 1.00 | 0.41 | 0.22 | −0.41 | 3.33% | 四闸不过 |
| 5 | `RRA10mpd` | Δ63 分歧度 | 1.29 | 0.60 | 0.59 | −0.01 | 3.07% | 四闸不过 |
| 6 | `P0MOjGpx` | z252(分歧度) | 1.09 | 0.47 | 0.40 | −0.05 | 3.30% | 四闸不过 |
| 7 | `leM3JWVn` | z252(覆盖人数) | 1.15 | 0.52 | 0.22 | 0.57 | 3.50% | 三闸不过 |
| 8 | `akVEX1nv` | z252(变异系数) | 0.91 | 0.35 | 0.08 | −0.19 | 3.19% | 四闸不过 |

**归因（不扫参）**：

1. **目标价的"形状量"在本集全灭**：偏度/极差/分歧度/变异系数四种形状读数 2Y 0.08–0.59、SUB ≤ 0，
   与 2026-10-19 analyst_factor_signals 的结论一致 —— **形状类读数只在 FY1 EPS 上成立，目标价上没有截面信息**。
   注意这与族 A（`pw5RbrYX`）不矛盾：族 A 是「**用**分歧度做权重、由偏斜定方向」，
   不是「**把**分歧度当信号」，机制不同。
2. **目标价水平修正（Δ63）也不够**：S 1.44 / 2Y 1.32 —— 水平修正在本集需要更长记忆（族 B 用 ts_zscore 175 才过），
   短窗修正只留下噪声。
3. **唯一新机制 = 覆盖人数变化（analyst breadth）**：`pwvKQN7x` S1.65/F0.92/2Y1.71/SUB0.92，
   与族 A/B 的机制正交（广度 ≠ 水平 ≠ 分歧），且 `estimate_count_current_period` 字段本身 uc11/ac15 不算拥挤。
   缺的只是 F：TO 3.31% < 0.125 ⇒ `F = S·√(returns/0.125)`，returns 3.86% 要补到 4.59%（+19%）或 S 到 1.80。
   ⇒ 下一批只做**定向一轮**（换 neutralization / decay / backfill 三杠杆），不做同族窗扫。

### 3.3 批 26（定向一轮：壳参数 + 未测族，multisim `2jHWibb9k4R19NU16M34NGz6`，8/8 COMPLETE）

设置同批 25（USA/TOP3000/D1/REVERSION_AND_MOMENTUM/decay 20/trunc 0.08，区间 2014-01-01→2023-12-31）。
通用壳同 §2.3；`*_surprise_*` 为 VECTOR，先 `vec_avg` 聚合。

| # | alpha | 变量 | S | F | 2Y | SUB | TO | returns | 判定 |
|---:|---|---|---:|---:|---:|---:|---:|---:|---|
| 1 | `ZYmKk9V3` | count Δ63 + backfill **504** | 1.65 | 0.92 | 1.71 | 0.92 | 3.31% | 3.86% | 仍差 F 0.08 |
| 2 | `qME6ep2O` | count Δ63 + winsor **std=3** | 1.66 | 0.92 | 1.71 | 0.93 | 3.31% | 3.88% | 仍差 F 0.08 |
| 3 | `Vkd3KLrJ` | count **Δ126** | 1.67 | 0.93 | **1.91** | 0.87 | 3.28% | 3.88% | 仍差 F 0.07 |
| 4 | `MP0L9nEk` | count Δ63 + ts_mean 5 | 1.62 | 0.89 | 1.68 | 0.93 | 3.28% | 3.79% | 更差 |
| 5 | `78ongr5v` | surprise(noshareout) Δ63 | 1.45 | 0.83 | 0.98 | 0.65 | 4.53% | 4.11% | 三闸不过 |
| 6 | `omogQXd5` | surprise(noshareout) ts_sum 63 | 0.38 | 0.09 | 1.16 | −0.12 | 2.60% | 0.68% | 死 |
| 7 | `gJW9752M` | surprise(depamort) Δ63 | 1.17 | 0.65 | 0.96 | 0.63 | 5.04% | 3.86% | 三闸不过 |
| 8 | `leM3JYm5` | EPS fxadj 合并均值 Δ63（重壳） | 1.74 | 0.99 | 1.48 | 0.49 | 3.25% | 4.06% | 三闸不过 |

**归因（写死，不再重复验证）**：

1. **backfill / winsor / 平滑 / 窗口都不是 F 的杠杆**：count 四个变体 S 1.62–1.67、returns 3.79–3.88%、F 0.89–0.93，
   极差 < 0.04。这是因为 TO≈3.3% < 12.5% ⇒ `F = S·√(returns/0.125)` 与 TO/decay 无关；
   `backfill(504)`、`winsor std=3`、`ts_mean5` 只动这三者之外的细节 ⇒ 结构上提不了 F。
   **要过 F1.0 只剩两条路：把 S 提到 1.80（+8%）或 returns 提到 4.59%（+19%），二者都只能来自中性化或换信号轴。**
2. **surprise 族（财报意外）在本集判弱**：noshareout Δ63 S1.45/2Y0.98、depamort Δ63 S1.17/2Y0.96、
   ts_sum63 S0.38。意外值本身是**事件级脉冲**，`ts_av_diff(63)` 把它摊平成缓慢漂移，方向信息被稀释；
   继续在同族换窗口属于盲扫，**排除**。
3. **EPS fxadj 合并均值 Δ63（`leM3JYm5`）是唯一 S、F 双达标（1.74 / 0.99）的新机制**，
   但 SUB 0.49（需 0.75）、2Y 1.48（需 1.58）双缺口 ⇒ 与 count 族互补而非替代；
   优先级低于 count（count 只差 F 一项）。
4. **结论：REVERSION_AND_MOMENTUM + decay 20 已榨干**。批 27 只换**中性化 / 分组轴**这两把杠杆
   （STATISTICAL / CROWDING；group = subindustry / industry / market），并补测未测的 projection / count(qtr) /
   surprise(fxadj) / prior-consensus 四个族，不再动 backfill/window/winsor。

### 3.4 批 27（2×8 A/B：中性化 × 分组轴，两 multisim 均 8/8 COMPLETE）

两个 multisim 信号完全相同、只有设置不同：
27a `1JXW0i8Y24NKcrDpUyaz0Wg` = **STATISTICAL** decay 20；27b `1lC5Yl3jA4Eo8O5txSxg8Uw` = **CROWDING** decay 20。
其余（USA/TOP3000/D1/trunc 0.08/2014-01-01→2023-12-31）同批 25。

| # | 信号 | 27a STATISTICAL（alpha）S/F/2Y/SUB/TO | 27b CROWDING（alpha）S/F/2Y/SUB/TO |
|---:|---|---|---|
| 1 | count Δ63, subind | `RRA1Z07b` 1.38/**0.60**/1.45/0.67/**3.00%** | `LL5dbxa1` 1.62/0.93/1.60/0.92/**0.90%** |
| 2 | count Δ126, subind | `KPmEYx7p` 1.50/0.69/1.70/0.76/3.07% | `omogwe5E` 1.68/0.97/**1.86**/0.89/0.89% |
| 3 | projection_noshareout Δ63 | `JjPv0Rxj` 1.29/0.55/0.68/0.20/3.25% | `RRA1ZLQz` 1.37/0.78/0.70/0.46/0.95% |
| 4 | estimate_count_noshareout Δ63 | `npA8kwKw` **1.55**/0.75/0.89/0.68/3.47% | `1YjzV5bR` 1.35/0.82/0.97/0.67/0.98% |
| 5 | surprise_fxadj Δ63（bf504） | `d5KR8eOj` 1.03/0.41/0.84/0.18/3.65% | `Vkd3wojA` 0.61/0.28/−0.21/0.27/1.41% |
| 6 | forecast_actual_noshareout Δ63 | `WjLVwKPZ` 1.27/0.54/0.21/0.29/3.28% | `6XAePbv7` 1.31/0.73/0.36/0.68/1.07% |
| 7 | avg_net_income_3mth_prior Δ63 | `npA8kwdw` 0.73/0.25/1.55/0.23/3.62% | `MP0LlAo9` 1.09/0.66/1.40/0.43/1.08% |
| 8 | count Δ63, group=**market**(a)/**industry**(b) | `d5KR8ebj` 1.52/0.76/1.26/0.60/3.54% | **`kqJZk52L` 1.73/1.03/1.83/0.92/0.90%** |

**归因（写死）**：

1. **中性化是 count 机制的生死开关，且方向与 targetprice 族相反**：STATISTICAL 把 count 压到 S1.38–1.52 / F0.60–0.76，
   CROWDING 把它拉到 S1.62–1.73 / F0.93–1.03。族 A/B（targetprice）在 STATISTICAL 下最好，是因为它们是**价格量纲**、
   需按统计风险因子剥离；coverage breadth 是**计数型广度**，真正的共同暴露是拥挤度本身 ⇒ CROWDING 才是对应剥离轴。
2. **中性化同时决定换手量级**：同一表达式 subindustry 分组，RAM（批 25）TO 3.31% → CROWDING TO 0.90%。
   即 CROWDING 把持仓变化对齐到共同的拥挤因子后，个股间相对变化被大幅吸收。这是**换手塌陷的机制解释**，
   不是壳参数问题 ⇒ 修复必须动「死区 / decay / 窗口」这些允许持仓更快更新的杠杆（批 28）。
3. **分组轴只在 CROWDING 下加分**：industry 比 market 高 +0.21 S（1.73 vs 1.52）、+0.57 SUB（0.92 vs 0.60）；
   在 STATISTICAL 下 market 反而更高（1.52 vs 1.38）。**分组轴与中性化必须成对解读，不能单列结论。**
4. **四个新字段族全部不够闸**：projection 1.37/1.29、estimate_count_noshareout 1.35/1.55（2Y 0.89）、
   forecast_actual 1.31/1.27（2Y 0.36）、avg_net_income_3mth_prior 1.09/0.73。其中 `npA8kwKw`（S1.55）
   在 CROWDING 下反而降到 1.35 ⇒ 不是设置问题，是字段无截面信息。**surprise 族两次中性化复证判死**（0.61/1.03）。
   ⇒ 「人数广度」的真信号只有 `estimate_count_current_period_targetprice_annual12_tribes` 这一个口径。
5. **批 27 预注册判据需修正**：原判据「F 仍 <1.0 ⇒ count 结构性差 F」被 `kqJZk52L`（F1.03）证伪；
   真实约束是 **TO 结构性偏低**（0.90% vs 1% 下限）。count 机制保留，走 §2.5 批 28 定向修复。
   ⚠ 注意：`kqJZk52L` 的 `checks.fail` 只有 LOW_TURNOVER；S/F/2Y/SUB 全 PASS，PPA 也仅因 TO 未过。

### 3.5 批 28（count breadth 换手修复：8 个杠杆，两 multisim）

28a = decay 20（4 条）；28b = decay 10（`35DHKSgTV4zabWxqDuE0hJR`，4 条，children
`3qjeYRdN` / `YPxgw0Xw` / `zqrRwmX8` / `QPY9rVmp`）。信号与设置锁定同 §2.5
（`estimate_count_current_period_targetprice_annual12_tribes` Δ63、`group_rank(..., industry)`、CROWDING、trunc 0.08）。

| # | 变更 | alpha | S | F | 2Y | SUB | TO | 判定 |
|---:|---|---|---:|---:|---:|---:|---:|---|
| 1 | hump 0.005，decay 20 | — | 1.51 | 0.85 | — | — | **1.05%** | TO 过，S/F 崩 |
| 2 | 去 hump，decay 20 | — | 1.08 | 0.56 | −0.27 | — | **4.83%** | 死（死区在承担 alpha） |
| 3 | hump 0.01，decay **10** | `3qjeYRdN` | 1.50 | 0.87 | 1.64 | 0.79 | **1.01%** | TO 过，S/F 不过 |
| 4 | hump 0.005，decay **10** | `YPxgw0Xw` | 1.39 | 0.76 | 1.90 | 0.66 | 1.15% | S/F/SUB 不过 |
| 5 | 去 hump，decay **10** | `zqrRwmX8` | 1.12 | 0.56 | −0.20 | 0.55 | 5.75% | 死 |
| 6 | Δ42，hump 0.01，decay 20 | — | 1.64 | 0.96 | 1.50 | — | 0.93% | 三闸不过 |
| 7 | Δ42，hump 0.01，decay 10 | `QPY9rVmp` | 1.44 | 0.86 | 1.57 | 0.83 | **1.04%** | TO 过，S/F/2Y 不过 |
| 8 | 去 `quantile`，decay 20 | — | 1.53 | 0.85 | 1.54 | — | 0.82% | 更差 |

（decay 5 未发：decay 20→10 已使 S 单调掉 0.23，继续降只会更差；按「不盲扫」跳过。）

**归因（写死，count 机制到此为止）**：

1. **TO 与 S 沿 decay/hump 轴单调对立，没有中间带**：保 S 的配置 TO 0.82–0.93%；TO 过 1% 的配置
   S 1.39–1.64（全部 <1.58）、F 0.76–0.96。最好的折中 `3qjeYRdN`（TO1.01/S1.50/F0.87）仍差 S 0.08、F 0.13。
2. **死区/hump 不是可拆的壳参数，它本身就是 alpha**：去 hump 后 TO 冲到 4.83–5.75%，但 2Y 翻负（−0.20/−0.27）。
   即该字段的信号是**年度口径覆盖人数的慢漂移**，收益来自「只交易稳定变化、忽略抖动」；
   把死区拆掉等于把信号换成噪声。
3. **判据触发 ⇒ count breadth 封存为结构性低换手**（数据更新频率决定，不是壳参数问题）。
   `kqJZk52L`（S1.73/F1.03/2Y1.83/SUB0.92，仅 TO0.90%）作为**未交付最优**留档，不再投仿真。
   count(qtr) 口径已在批 27 复测（`1YjzV5bR` S1.35）⇒ 同族无替代字段，**整族排除**。

### 3.6 批 29（actual_* 已报值增长漂移，8 机制；multisim `43vPrredU59MbhnJ0e95hTj`，8/8 COMPLETE）

设置：CROWDING / decay 10 / industry / trunc 0.08；壳 = `ts_zscore(ts_av_diff(vec_avg(F), 126), 504)`
→ winsor std4 → backfill 252 → hump 0.01 → group_rank(industry) → quantile。

| # | 机制 | 字段 | alpha | S | F | 2Y | SUB | TO |
|---:|---|---|---|---:|---:|---:|---:|---:|
| 1 | 收入增长 | `actual_revenue_value_quarterly16` | `YPxgwEQM` | 1.25 | 0.75 | 1.20 | 0.44 | 1.07% |
| 2 | 净利增长 | `actual_netprofit_value_quarterly16` | `qME6kYg2` | 1.27 | 0.71 | 0.44 | 0.21 | 1.07% |
| 3 | EBIT 增长 | `actual_ebit_value_quarterly16_2` | `xA1dw2ng` | 1.03 | 0.56 | 1.10 | 0.09 | 1.15% |
| 4 | EPS 增长 | `actual_eps_value_quarterly16` | `RRA1Zlrd` | 0.92 | 0.45 | 0.45 | 0.27 | 1.12% |
| 5 | 资本开支扩张（反） | `actual_capex_value_quarterly16` | `6XAePoEG` | 0.49 | 0.20 | 0.50 | 0.29 | 1.13% |
| 6 | FCF 增长 | `actual_fcf_value_quarterly16` | `N1eRWJOE` | 0.70 | 0.36 | 0.73 | 0.63 | 1.02% |
| 7 | 去杠杆（反） | `actual_netdebt_value_quarterly16` | `A1Q7JrwY` | 0.49 | 0.20 | 1.23 | 0.28 | 1.04% |
| 8 | ROE 趋势 | `actual_value_roe_quarterly16` | `3qjeYk7X` | 0.70 | 0.38 | 0.63 | 0.27 | **0.94%** |

**归因（写死）**：

1. **8 个已报值增长机制全不够闸**，最好的收入也只有 S1.25/2Y1.20；净利 2Y0.44、EPS 2Y0.45。
   即「已报财务值的同比/环比漂移」在本集**没有截面信息**（与批 25 形状量、批 26 surprise 的结论同向：
   本集的有效信息集中在**预期侧**，不在已报侧）。
2. **CROWDING 再次把 TO 压到 1.0% 一线**（0.94–1.15%），与批 27/28 的换手塌陷一致 ⇒ 对**季度更新**的已报值，
   CROWDING 几乎必然踩 LOW_TURNOVER 下限。判弱**不能全归给字段**：本批壳（Δ126+zscore504）与中性化同时偏慢。
   ⇒ M01/M02 若要复测，只换 STATISTICAL × Δ63 一条轴（不重扫 8 个字段）；M03–M08 判死（S≤1.03 且 2Y≤1.10）。
3. **报表族的第一条强判据**：预期侧合并序列（批 30）若同样无信号，则 actual_* 整族封存；
   若合并序列有效，则后续只在合并序列上构造比率，不再回到已报值。

### 3.7 批 30a（预期+实际合并序列 × 6 机制；multisim `2K2t0R2Bp5dC9Q01bqgETyTg`，8/8 COMPLETE）

设置：STATISTICAL / decay 20 / trunc 0.08；壳 = `quantile(group_rank(hump(ts_backfill(winsorize(ts_av_diff(<SIGNAL>, W), std=4), 252), hump=0.01), <G>))`。
#3 是「复测壳」：与已交付的 `leM3JYm5`（RAM/decay20/subindustry）**只差窗口与中性化**，用作可比的对照。

| # | 机制 | 字段 / 构造 | 变体 | alpha | S | F | 2Y | SUB | TO |
|---:|---|---|---|---|---:|---:|---:|---:|---:|
| 1 | M28 合并 EPS 修正 | `mean_forecast_actual_combined_fxadj_eps_annual12` | Δ63 / industry | `gJW9ql5O` | 1.73 | 0.89 | 1.43 | 0.59 | 3.38% |
| 2 | 同上 | 同上 | Δ63 / market | `leM36nY7` | 1.73 | 0.92 | 1.31 | 0.59 | 3.62% |
| 3 | 同上 | 同上 | Δ126 / industry | `wp9EwdAl` | **1.82** | **0.97** | 1.01 | **0.69** | 3.47% |
| 4 | 合并营收修正 | `mean_forecast_actual_combined_fxadj_revenue_annual12_tribes` | Δ63 / industry | `akVE208x` | 1.33 | 0.59 | 0.63 | 0.41 | 3.28% |
| 5 | 合并 EBIT 修正 | `mean_forecast_actual_fxadj_ebit_annual12` | Δ63 / industry | `LL5dbvw2` | 1.56 | 0.75 | 1.37 | 0.25 | 3.23% |
| 6 | 合并 FCF 修正 | `mean_forecast_actual_combined_fxadj_fcf_annual12` | Δ63 / industry | `ZYmKw8vY` | 1.22 | 0.53 | **1.77** | 0.66 | 3.62% |
| 7 | M09 净利率漂移 | `actual_netprofit_value_quarterly16 / actual_revenue_value_quarterly16` | Δ63 / industry | `WjLVwZ2k` | 1.49 | 0.75 | 1.11 | **−0.16** | 3.76% |
| 8 | M10 EBIT 率漂移 | `actual_ebit_value_quarterly16_2 / actual_revenue_value_quarterly16` | Δ63 / industry | `pwvKJ2e6` | 1.47 | 0.73 | **1.98** | **−0.22** | 3.73% |

**归因（写死）**：

1. **M28 合并序列是全批最强机制**：S 1.73–1.82，显著高于已报值族（批 29，S≤1.27）与比率类（S 1.47–1.49）。
   与批 29 的结论同向：**本集的有效信息在预期侧；「预期+实际」合并序列优于纯已报值**。
   缺口是三闸同时贴边：F 0.89–0.97（差 0.03–0.11）、2Y 1.01–1.43（差 0.15–0.57）、SUB 0.59–0.69（差 0.06–0.16）。
2. **窗口方向是「S/SUB 升、2Y 崩」**：Δ63→Δ126 时 S 1.73→1.82、F 0.89→0.97、SUB 0.59→0.69，
   但 **2Y 1.43→1.01**。⇒ 2Y 缺口不是「信号太慢」，更像**近年有效记忆在缩短**；Δ42/Δ22 方向与之相反，仍值得实测（批 30b）。
3. **分组轴不是主杠杆**：industry 与 market 的 S/F/SUB 同形（1.73 / 0.89–0.92 / 0.59），
   2Y market 反而更差（1.31 vs 1.43）⇒ 与 count 在 `industry` 下 F 翻盘（批 27）不同，此处换分组不改命运。
4. **比率类的 SUB 转负**（M09 −0.16 / M10 −0.22）：净利率、EBIT 率的漂移在 TOP3000 子宇宙**反向**。
   EBIT 率 2Y 1.98 是唯一亮点，但 SUB 为负属结构性危险（小盘反向），**M09/M10 判弱**，不再磨。
5. **F 判据第二次复证**：TO 3.2–3.8% < 12.5% ⇒ `F = S·√(returns/0.125)`。
   Δ126 之所以 F 最高（0.97），是 S（1.82）与 returns（3.55%）同时更高，**不是窗口改变了 F 的机制**。
   ⇒ 要 F≥1.0 且 2Y≥1.58，必须找**同时**抬高收益幅度与近年稳定性的设置，磨 decay 无效。
6. **FCF 是唯一 2Y 过闸的（1.77）**，但 S 1.22 / F 0.53 ⇒ 「只在近年有效」，不可交付；
   留作 M31（财报窗口门控）的动机证据。

**批 30b 预注册判据（写死）**：

- 通过线：**S≥1.58 且 F≥1.0 且 2Y≥1.58 且 SUB≥0.75 且 TO≥1%** ⇒ 立即 `check_correlation(refresh=True)`。
- 只测 9 个杠杆（3 个 multisim 并行，中性化为批次级设置）：Δ42 / Δ22（短记忆）、subindustry / sector（分组轴）、
  反号（判断 2Y 是否由方向造成）、RAM × industry / market（中性化轴，批 30a #3 的另一半）、
  CROWDING × industry Δ63 / Δ126（中性化轴 + 换手风险观测）。
- 若 9 条全败、且无一条同时达到「F≥0.95 且 2Y≥1.45」⇒ **M28 判 F×2Y 双缺口，封存**，转 M29–M32（应计距离 / 财务质量复合 / 财报窗口门控 / 存货占用）。

### 3.8 批 31 预注册（M29–M32 + 机制补测；仅在 30b 判据触发时执行）

设置：STATISTICAL / decay 20 / industry / trunc 0.08；壳同 §3.7（`winsor std4 → backfill 252 → hump 0.01 → group_rank(industry) → quantile`），
除特别注明外信号直接替换 `SIGNAL`。**每条的字段全部来自 `analyst_consensus`，满足 ATOM 单数据集约束。**

| # | 机制 | SIGNAL 核心 | 方向 |
|---:|---|---|---|
| 1 | M29 应计距离（年度） | `ts_av_diff((vec_avg(actual_netprofit_value_annual12) − vec_avg(actual_cfo_value_annual12)) / vec_avg(actual_total_assets_value_annual12), 252)` | 反向（应计高 = 质量差） |
| 2 | M29b 应计距离（季度代理） | `ts_av_diff((vec_avg(actual_netprofit_value_quarterly16) − vec_avg(actual_fcf_value_quarterly16)) / vec_avg(actual_revenue_value_quarterly16), 63)` | 反向 |
| 3 | M30 财务质量复合 | `vec_avg(actual_value_roe_quarterly16) * vec_avg(actual_cfo_value_annual12) / vec_avg(actual_revenue_value_quarterly16)`（**水平**，不取 Δ） | 正向 |
| 4 | M31a 窗口门控（flag 高） | `trade_when(vec_avg(forecast_actual_flag_eps_annual12_3) > 0.5, <M28 Δ63 内层>, -1)` | 正向（flag 语义两种都测） |
| 5 | M31b 窗口门控（flag 低） | `trade_when(vec_avg(forecast_actual_flag_eps_annual12_3) <= 0.5, <M28 Δ63 内层>, -1)` | 正向 |
| 6 | M32 存货占用 | `ts_av_diff(vec_avg(actual_inventory_value_fxadj_annual12) / vec_avg(actual_revenue_value_quarterly16), 252)` | 反向（存货占比升 = 需求弱） |
| 7 | M35 预期修正加速度 | `ts_av_diff(ts_av_diff(vec_avg(mean_forecast_actual_combined_fxadj_eps_annual12), 63), 63)` | 正向 |
| 8 | M01 复测（补批 29 缺口） | `ts_av_diff(vec_avg(actual_revenue_value_quarterly16), 63)` | 正向（STATISTICAL 下复测，非 CROWDING） |

判据（写死）：任一 S≥1.58 / F≥1.0 / 2Y≥1.58 / SUB≥0.75 / TO≥1% ⇒ 相关性实测；
**若 8 条全灭 ⇒ actual_* 与比率族整体封存，analyst_consensus 无计可施，转 other685「Enhanced Financial Indicators」并在交付日志写明原因。**
注意 M32 覆盖率仅 0.5966，若出现 `CONCENTRATED_WEIGHT` 先判 backfill 不足而非机制无效。

**完整表达式清单（可直接发批；壳 = `quantile(group_rank(hump(ts_backfill(winsorize(<SIG>, std=4), 252), hump=0.01), industry))`）**：

| # | SIG |
|---:|---|
| 1 | `-1 * ts_av_diff((vec_avg(actual_netprofit_value_annual12) - vec_avg(actual_cfo_value_annual12)) / vec_avg(actual_total_assets_value_annual12), 252)` |
| 2 | `-1 * ts_av_diff((vec_avg(actual_netprofit_value_quarterly16) - vec_avg(actual_fcf_value_quarterly16)) / vec_avg(actual_revenue_value_quarterly16), 63)` |
| 3 | `vec_avg(actual_value_roe_quarterly16) * vec_avg(actual_cfo_value_annual12) / vec_avg(actual_revenue_value_quarterly16)` |
| 4 | `trade_when(vec_avg(forecast_actual_flag_eps_annual12_3) > 0.5, ts_av_diff(vec_avg(mean_forecast_actual_combined_fxadj_eps_annual12), 63), -1)` |
| 5 | `trade_when(vec_avg(forecast_actual_flag_eps_annual12_3) <= 0.5, ts_av_diff(vec_avg(mean_forecast_actual_combined_fxadj_eps_annual12), 63), -1)` |
| 6 | `-1 * ts_av_diff(ts_backfill(vec_avg(actual_inventory_value_fxadj_annual12), 252) / ts_backfill(vec_avg(actual_revenue_value_quarterly16), 252), 252)` |
| 7 | `ts_av_diff(ts_av_diff(vec_avg(mean_forecast_actual_combined_fxadj_eps_annual12), 63), 63)` |
| 8 | `ts_av_diff(vec_avg(actual_revenue_value_quarterly16), 63)` |

⚠ 批 31 的 3/4/5/6 依赖低覆盖字段（cfo 0.7956 / inventory 0.5966 / currentassets 0.7212），
发批时若整批出现大面积 NaN，先补内层 `ts_backfill` 而不是判机制死。

**实际发批（2026-10-20，multisim `2AGL5Ueiz4izbzhL1tpW3cK`，8 条；设置改用 REVERSION_AND_MOMENTUM/decay20/industry/trunc0.08）**：
与预注册的三处偏差必须按实际读：
1. **中性化改 RAM**：30b/30c 已证明 F×2Y 由 RAM 解决（STATISTICAL 下两闸皆缺），故本批统一在 RAM 下测新机制。
2. **字段替换（预注册时凭记忆写错名，均按 `get_datafields` 实测纠正）**：
   `actual_fcf_value_quarterly16` → `actual_fcf_value_annual12`（cov 0.8491）、
   `actual_value_roe_quarterly16` → `actual_roe_value_annual12`（cov 0.7372）、
   存货分母 `actual_revenue_value_quarterly16` → `actual_revenue_value_annual12`（cov 0.7617，与年度存货同尺度）。
   M29b 因此变为「(年度净利 − 年度 FCF)/年度总资产 的 Δ63」= **同分子族的短窗变体**，与 #1 是窗口对照而非独立机制。
3. **`trade_when` 退出条件用 `0` 不用 `-1`**：0 = 永不退出（保持前值），与 30c #5 实测可用的写法一致；
   `-1` 在 FASTEXPR 里是恒真的退出条件，会把信号整条赋 NaN（量纲风险，未实测不冒）。
4. 预检 `preflight_expressions` 报 `valid=false, unknown_fields=["std"]` 是 `winsorize(std=4)` 命名参数的已知误报，
   10 个真实字段全部 `fields_checked` 通过。

### 3.9 批 30b（M28 九杠杆：窗口 / 分组 / 中性化 / 方向；3 multisim 全 COMPLETE）

设置：trunc 0.08 固定；三批分别为 STATISTICAL/decay20（5 条）、RAM/decay20（2 条）、CROWDING/decay10（2 条）。
壳同 §3.7，只动杠杆本身。**九条中没有一条同时过 F≥1.0 ∧ 2Y≥1.58 ∧ SUB≥0.75**，但出现了第一个 O0JxqoNq 这样的 prod-可过候选。

> ⚠ 工程注记（2026-10-20 批 31 发批时踩到）：本档案里的「**RAM**」是 **REVERSION_AND_MOMENTUM** 的简称，
> MCP `create_multi_simulation` 的 `neutralization` 合法值里**没有** `RAM`（会报 Unknown neutralization），
> 必须传全名。同理 `winsorize(..., std=4)` 在 `preflight_expressions` 里会被误报
> `unknown_fields=["std"]`（命名参数被当成字段），属已知误报，字段面真实校验看 `fields_checked`。

| # | 杠杆 | 中性化/decay | 分组 | 窗口 | alpha | S | F | 2Y | SUB | TO |
|---:|---|---|---|---|---|---|---:|---:|---:|---:|---:|
| 1 | 短记忆 | STATISTICAL/20 | industry | Δ42 | `QPY9qEeX` | 1.73 | 0.88 | **1.64** | 0.63 | 3.37% |
| 2 | 极短记忆 | STATISTICAL/20 | industry | Δ22 | `LL5dqke6` | 1.33 | 0.59 | 0.80 | 0.29 | — |
| 3 | 细分行业 | STATISTICAL/20 | subindustry | Δ63 | `Vkd3qOnG` | 1.51 | 0.70 | 1.18 | 0.47 | — |
| 4 | 行业组 | STATISTICAL/20 | sector | Δ63 | `WjLVn9kO` | 1.78 | 0.95 | 1.47 | 0.58 | — |
| 5 | 反号对照 | STATISTICAL/20 | industry | Δ63 | `kqJZbQR6` | 0.82 | 0.29 | 0.44 | 0.13 | — |
| 6 | **RAM** | **RAM/20** | industry | Δ63 | **`O0JxqoNq`** | **1.92** | **1.22** | **1.81** | 0.65 | 3.55% |
| 7 | RAM + 全市场 | RAM/20 | market | Δ63 | `MP0Lqka6` | 1.66 | 1.12 | 1.83 | 0.59 | 3.90% |
| 8 | CROWDING | CROWDING/10 | industry | Δ63 | `omogA3LJ` | 1.76 | 1.10 | 1.37 | 0.50 | 1.18% |
| 9 | CROWDING + 长窗 | CROWDING/10 | industry | Δ126 | `rKdPEJe1` | 1.81 | 1.17 | 1.09 | 0.60 | 1.18% |

**归因（写死）**：

1. **RAM 是决定性中性化，F×2Y 两闸其实可解**：同一构造 Δ63/industry，STATISTICAL 下 1.73/0.89/1.43（#30a-1），
   RAM 下 **1.92/1.22/1.81**（#6）—— S、F、2Y 同时抬升，且 TO 只从 3.38% → 3.55%。
   同族 `leM3JYm5`（RAM/subindustry）1.74/0.99/1.48 说明增益来自**中性化本身**，不是 subindustry 分组。
   ⇒ 30a 结论「三闸同时贴边」应修正为：**F 与 2Y 由中性化轴解决，SUB 不是**。
2. **SUB 是唯一残余缺口，且是结构性的**：`O0JxqoNq` SUB 0.65 / limit 0.83（lim = 0.43×S）。
   本机制九条的 SUB/S 比值 0.22–0.36，全部低于破闸所需的 0.43；分组轴（market 0.355 / sector 0.326 /
   subindustry 0.311）与中性化轴（CROWDING 0.284–0.331）都不能把它推到 0.43。
   ⇒ 读数：**该字段的修正信号在高流动性子宇宙上系统性偏弱**（小盘分析师覆盖少、修正弹性大）。
3. **反号判死**：#5 反号后 0.82/0.29/0.44/0.13 ⇒ 原方向正确，2Y 缺口不是「方向做反」造成的。
4. **短记忆与长记忆互补**：Δ42 在 STATISTICAL 下 2Y 1.64 已过闸但 F 0.88（#1）；Δ126 在 30a 下 F 0.97 但 2Y 1.01。
   ⇒ 在 RAM 下测 Δ42/Δ84 是同时拿两头的唯一机会（批 30c）。
5. **CROWDING 不适合本机制**：TO 被压到 1.18%（贴 1% 下限），2Y 还从 1.81 掉到 1.37/1.09。
   本机制原生换手就不高，再压只会牺牲近年稳定性。
6. **★ prod 实测（本族首次，关键）**：`O0JxqoNq` **prod 0.682 / self 0.535，均通过**（阈值 0.7，
   prod 侧 max 0.682、分布 [0.6,0.7) 仅 328 个历史 alpha）。⇒ **本族没有结构性 prod 墙**，
   与 `institutions18`（prod 0.94）和 count breadth（prod 0.94）形成鲜明对比。修 SUB 有真实交付价值。

**批 30c 预注册（在飞，multisim `3ivjgW6pJ4WUcJ3189FWp99z`，8 条）**：

设置 RAM/decay20/trunc0.08/industry，基线 = `O0JxqoNq`。八个 SUB 杠杆：

| # | 杠杆 | SIGNAL 变体 |
|---:|---|---|
| 1 | 内层强平滑 | 同基线但 `hump=0.05`（0.01 → 0.05） |
| 2 | 20 日平滑 | `ts_mean(ts_av_diff(vec_avg(F),63), 22)` |
| 3 | 中短窗 | `ts_av_diff(vec_avg(F), 42)` |
| 4 | 中长窗 | `ts_av_diff(vec_avg(F), 84)` |
| 5 | 阈值门控（论坛移植） | `trade_when(abs(ts_zscore(ts_av_diff(vec_avg(F),22),66)) > 1.5, ts_av_diff(vec_avg(F),22), 0)` |
| 6 | 持续性（论坛移植） | `ts_product(ts_av_diff(vec_avg(F), 5), 5)` |
| 7 | 同行相对（论坛移植） | `group_zscore(ts_av_diff(vec_avg(F), 63), industry)` 作为内层 |
| 8 | 历史标准化 | `ts_zscore(ts_av_diff(vec_avg(F), 63), 252)` |

判据（写死）：SUB ≥ 0.78 且 S≥1.58 / F≥1.0 / 2Y≥1.58 / TO≥1% 全保持 ⇒ 相关性复核后入交付候选；
**若八条中 SUB/S 最高仍 < 0.40 ⇒ M28 判 SUB 结构性缺口，封存**，转 §3.8 批 31（M29–M32）。
M38–M41 四条论坛节奏结构同时在此批完成首测。

⚠ **两个已知的读数量纲风险（发批后才发现，收批时必须先排除再归因）**：
1. **C6 `ts_product(Δ5,5)` 会被 hump 归零**：Δ5 量级约 0.01–0.1，5 次乘积约 1e-10，绝对值小于壳内 `hump=0.01`
   ⇒ 整条信号被抹成 0。若 C6 的 S≈0/持仓数≈0，判**量纲失配而非机制无效**，30d 用
   `ts_product(ts_zscore(Δ5,252),5)` 补测。
2. **C5 门控后 93% 的值为 0**：`|z|>1.5` 约覆盖 7% 观测，横截面大部分为 0、排名居中，
   实际是「只在极端修正日持仓」。若 TO 低于 1%，应改 `trade_when(..., 信号, -1)`（保持前值、不平仓）而不是判死。

**30d 预案（仅当 30c 的 SUB/S < 0.40 但出现 ≥0.36 的改善时启用）**：Δ5（跨战役证据：Institutions 扫描 §9.3
的 14 族 42 条中 Δ5 是 SUB 最高 0.89 的唯一族）+ `ts_product(ts_zscore(Δ5,252),5)` +
`ts_mean(clean,120)` 慢版（论坛帖 TO 2.45% / margin 0.01183）。三条即可，不再扩批。

**批 30c 收批（8/8 COMPLETE；两条 RA 全闸 PASS，本战役首次）**：

| # | 杠杆 | alpha | S | F | 2Y | SUB | limit | SUB/S | TO | RA |
|---:|---|---|---:|---:|---:|---:|---:|---:|---:|---|
| 1 | hump 0.05 | `npA8YL1l` | 2.01 | 1.29 | 1.72 | 0.70 | 0.87 | 0.348 | 3.53% | SUB fail |
| 2 | ts_mean 22 | `1Yjz1rYm` | 1.88 | 1.17 | 1.21 | 0.62 | 0.81 | 0.330 | 3.55% | SUB+2Y fail |
| 3 | Δ42 | `WjLVnvjP` | 1.84 | 1.15 | **2.01** | 0.66 | 0.80 | 0.359 | 3.58% | SUB fail |
| 4 | Δ84 | `kqJZbzqO` | 1.99 | 1.29 | 1.72 | 0.73 | 0.86 | 0.367 | 3.59% | SUB fail |
| 5 | **zscore 门控** | **`78on0e78`** | **2.19** | **1.48** | **2.46** | **1.05** | 0.94 | **0.479** | 3.61% | **fail=[] 全过** |
| 6 | ts_product 持续 | `A1Q7Yojg` | −1.41 | −0.84 | −2.19 | −0.60 | — | — | 3.83% | 量纲失配 |
| 7 | group_zscore 同行 | `ZYmKqOPQ` | 1.87 | 1.20 | 1.45 | **0.88** | 通过 | 0.471 | 3.65% | 2Y fail（差 0.13） |
| 8 | **ts_zscore 历史标准化** | **`e76xgXkM`** | **1.89** | **1.12** | **1.76** | **1.05** | 通过 | **0.556** | 3.29% | **fail=[] 全过** |

**归因（写死）**：

1. **★ SUB 缺口的真正解是「测量口径」，不是窗口/平滑/分组**：同一 Δ63 构造，
   基线 `O0JxqoNq` SUB 0.65（SUB/S 0.339）→ `ts_zscore(Δ63,252)` 后 **SUB 1.05（SUB/S 0.556）**，
   同时 S 1.92→1.89、F 1.22→1.12、2Y 1.81→1.76 仅微降。
   ⇒ 与 Institutions 档案 §10.4 同一条方法论**第二次复证**：把修正幅度按**自身历史波动**归一后，
   高波动小盘股的信号被压回与大盘同一量纲，SUB 闸（子宇宙相对强度）随即通过。
2. **门控版本是全场最强读数**：`78on0e78` S2.19/F1.48/2Y2.46/SUB1.05，全部远超闸线
   （trade_when 只在 |z(Δ22,66)|>1.5 的极端修正日更新，TO 仍 3.61%）。但 **prod 0.7214 未过**（超 0.0214）。
   直方图 `[0.7,0.8)` 桶 **n=1**、`[0.6,0.7)` 桶 344 ⇒ 按 `wq-window-valley-break-prod-wall`「n≥1 必死」，
   该门控形态**族级不可救**；不磨参数，**挂起（非 dead_end 以外的新构造）**。
3. **e76xgXkM 已验证交付（第 7 颗）**：prod **0.5532** / self **0.4553**（top: `akVnvzX5` 0.4553、
   `omoK1A5m` 0.4340），双端点均 < 0.7；字段 = 合并 EPS 的 Δ63 历史标准化，RAM/decay20/industry/trunc0.08。
4. **窗口轴在 RAM 下也救不了 SUB**：Δ42 SUB/S 0.359（2Y 2.01）、Δ84 0.367（最接近但未过）、
   hump0.05 0.348、ts_mean22 0.330 ⇒ 四条全部 <0.43。窗口只移动 S/2Y 的平衡点，不改变高低流动性两段的相对强度。
5. **group_zscore 同行相对化能过 SUB（0.88，SUB/S 0.471），但 2Y 1.45 差 0.13**：
   行业内去均值削掉了近年最有效的「行业整体修正」成分 ⇒ 与 `e76xgXkM` 可作**正交备胎**，
   但当前不达三闸，不进入交付。
6. **ts_product 判量纲失配（非机制无效）**：S−1.41/F−0.84/2Y−2.19/SUB−0.60，符号整体反转 +
   幅度异常，与发批前的预测（5 次乘积 ≈1e-10 被 hump=0.01 归零）一致。30d 必须用
   `ts_product(ts_zscore(Δ5,252),5)` 复测；**不得据此判 M38 机制无效**。

### 3.10 论坛帖《分析师修正当成节奏，而不是评分》的三条可移植结构（M38–M41）

来源：[【Alpha Idea】分析师修正当成节奏，而不是评分](https://support.worldquantbrain.com/hc/en-us/community/posts/43878933562391)（GZ47187，2026-09-30）。
原帖在 **analyst16** 上的实测：`ts_product(clean,5)` = S2.95/F3.05/TO17.85%/margin 0.002144；
`trade_when(abs(ts_zscore(ts_av_diff(clean,22),66))>1.5, …, 0)`；`group_zscore(…, industry)`；
`ts_mean(clean,120)` 慢版本 = S1.75/F1.88/TO2.45%/margin 0.01183（USA/TOP3000/decay3/RAM/trunc0.08）。

**移植纪律**：帖中 `clean = winsorize(ts_backfill(vec_avg(field),120), std=4)` 且字段是**修正分量**（可正可负）；
本集的 `mean_forecast_actual_combined_fxadj_eps_annual12` 是**EPS 水平值（恒正）**，
⇒ **不能照搬 `ts_product(clean,5)`**（正数乘积退化为水平乘积，无「连续同向」含义），必须改为对**差分**做乘积
（`ts_product(ts_av_diff(…,5),5)`）。字段不照搬（破 ATOM），只移植算子结构。

### 3.11 批 32 预注册（M42–M49：M28 修正机制换财务行项目；仅在批 31 不足 3 颗时执行）

**问题**：M28（合并预期序列 Δ63 按自身 252 日波动标准化）已在 EPS 上交付（`e76xgXkM`），
但交付目标还需 3 颗，且 EPS 一个字段无法证明该机制是**普遍的分析师修正漂移**还是偶然。
本批把同一测量口径（`ts_zscore(Δ63,252)`）横移到 8 个**经济含义不同**的财务行项目，
每条只引用一个字段（ATOM 合规），并为每条写下**独立的方向假说**——这不是扫参：
先行项目不同 ⇒ 信息集不同 ⇒ 若同时出现多颗过闸，它们的截面相关也应显著低于同字段变体。

设置：REVERSION_AND_MOMENTUM / decay 20 / industry / trunc 0.08（与 30c/31 完全一致，只换字段）。
壳：`quantile(group_rank(hump(ts_backfill(winsorize(<SIG>, std=4), 252), hump=0.01), industry))`，
`<SIG> = ts_zscore(ts_av_diff(vec_avg(F), 63), 252)`。

| # | 机制 | 字段 F（coverage，`get_datafields` 实测） | 方向假说 |
|---:|---|---|---|
| 1 | M42 营收修正（top-line demand） | `mean_forecast_actual_combined_fxadj_revenue_annual12`（0.9751） | 正：收入预期上修 = 需求趋势改善，且比 EPS 少受成本/一次性项污染 |
| 2 | M43 EBIT 修正（operating profitability） | `mean_forecast_actual_combined_fxadj_ebit_annual12_2`（0.9632） | 正：经营利润率上修 = 定价权/成本效率改善 |
| 3 | M44 税前利润修正（broad profit） | `mean_forecast_actual_combined_pretax_annual12`（0.9665） | 正：比净利更少受税率与一次性项干扰 |
| 4 | M45 报告净利修正（bottom line） | `mean_forecast_actual_combined_fxadj_reportednet_annual12_2`（0.9589） | 正；与 M44 的差 = 税率/非经营项信息 |
| 5 | M46 CFO 修正（cash reality） | `mean_forecast_actual_combined_fxadj_cfo_annual12`（0.7956） | 正：现金流上修比利润上修更难过应计操纵，信号更干净 |
| 6 | M47 ROE 修正（capital efficiency） | `mean_forecast_actual_combined_roe_annual12_tribes`（0.8592） | 正：单位资本盈利能力改善，天然跨公司可比 |
| 7 | M48 EBITDA 修正（operating cash earnings） | `mean_forecast_actual_combined_ebitda_annual12`（0.8636） | 正；与 M43 的差 = D&A 政策信息 |
| 8 | M49 Capex 修正（overinvestment） | `mean_forecast_actual_combined_capex_annual12_2`（0.8334） | **负**：Titman/Wei/Xie (2004) 过度投资假说——资本开支预期上修预示自由现金流恶化与后续低回报 |

判据（写死）：
- **单条**：S≥1.58 / F≥1.0 / 2Y≥1.58 / SUB≥0.75 / TO≥1% 全过 ⇒ 立即 `check_correlation(refresh=True)`；
  prod 与 self 均 <0.7 ⇒ 入交付候选。任一相关端点超线 ⇒ 按 `wq-window-valley-break-prod-wall` 直方图判族级命运，不磨参数。 <!-- from config.prod_corr_max -->
- **批级**：8 条全灭且 S 无一条 ≥1.2 ⇒ 判「分析师修正漂移只存在于 EPS/盈利口径，不横移财务行项目」，
  M42–M49 封存，analyst_consensus 的交付潜力见底；若完成 3 颗仍不足 10，则按交付日志 §2 转 other685。
- **覆盖率注意**：M46（0.7956）/ M49（0.8334）低于 0.9，若出现 `CONCENTRATED_WEIGHT` 先补内层 backfill，不判机制死。
- **自相关预算**：本批与 `e76xgXkM` 同壳同机制，若某条 self 落在 0.6–0.7，先看是否**行项目重叠**导致
  （净利/税前/EBITDA 很可能共享分析师现金流预期），不要直接用 hump/decay 硬压（`wq-prod-lever-self-lock-guard`）。

**完整表达式清单（可直接发批）**：

| # | 完整表达式 |
|---:|---|
| 1 | `quantile(group_rank(hump(ts_backfill(winsorize(ts_zscore(ts_av_diff(vec_avg(mean_forecast_actual_combined_fxadj_revenue_annual12), 63), 252), std=4), 252), hump=0.01), industry))` |
| 2 | `quantile(group_rank(hump(ts_backfill(winsorize(ts_zscore(ts_av_diff(vec_avg(mean_forecast_actual_combined_fxadj_ebit_annual12_2), 63), 252), std=4), 252), hump=0.01), industry))` |
| 3 | `quantile(group_rank(hump(ts_backfill(winsorize(ts_zscore(ts_av_diff(vec_avg(mean_forecast_actual_combined_pretax_annual12), 63), 252), std=4), 252), hump=0.01), industry))` |
| 4 | `quantile(group_rank(hump(ts_backfill(winsorize(ts_zscore(ts_av_diff(vec_avg(mean_forecast_actual_combined_fxadj_reportednet_annual12_2), 63), 252), std=4), 252), hump=0.01), industry))` |
| 5 | `quantile(group_rank(hump(ts_backfill(winsorize(ts_zscore(ts_av_diff(vec_avg(mean_forecast_actual_combined_fxadj_cfo_annual12), 63), 252), std=4), 252), hump=0.01), industry))` |
| 6 | `quantile(group_rank(hump(ts_backfill(winsorize(ts_zscore(ts_av_diff(vec_avg(mean_forecast_actual_combined_roe_annual12_tribes), 63), 252), std=4), 252), hump=0.01), industry))` |
| 7 | `quantile(group_rank(hump(ts_backfill(winsorize(ts_zscore(ts_av_diff(vec_avg(mean_forecast_actual_combined_ebitda_annual12), 63), 252), std=4), 252), hump=0.01), industry))` |
| 8 | `-1 * quantile(group_rank(hump(ts_backfill(winsorize(ts_zscore(ts_av_diff(vec_avg(mean_forecast_actual_combined_capex_annual12_2), 63), 252), std=4), 252), hump=0.01), industry))` |

⚠ 方向说明：#8 的负号放在**壳外**（与批 30b 的 `O0JxqoNq` 反号处理一致），保证分位与分组仍在原始修正方向上计算，
再整体翻转持仓；不要把 `-1 *` 塞进 `ts_av_diff` 里（会改变 `winsorize` 前的符号分布，等价但难读）。

**实际发批（2026-10-20，multisim `142IJ74Ro4nUaYk1ajMGdOZp`，8 条）**：
设置与预注册一致（REVERSION_AND_MOMENTUM/decay20/industry/trunc0.08）；
`preflight_expressions` 的 8 个真实字段全部 `fields_checked` 通过，仅报 `unknown_fields=["std"]`（已知误报）。

### 3.12 批 31 收批（8/8 COMPLETE；0 条三闸全过，actual_*/比率族判封存）

multisim `2AGL5Ueiz4izbzhL1tpW3cK`；RAM/decay20/industry/trunc0.08。

| # | 机制 | alpha | S | F | 2Y | SUB | limit | TO | RA 结论 |
|---:|---|---|---:|---:|---:|---:|---:|---:|---|
| 1 | M29 应计距离（Δ252，反号） | `78onQ6m5` | 1.21 | 0.78 | 1.31 | **0.87** | 0.52 | 4.38% | S/F/2Y fail；SUB pass |
| 2 | M29b 应计距离（Δ63，反号） | `KPmE6rQk` | 1.33 | 0.88 | 1.33 | **0.76** | 0.61 | 4.39% | S/F/2Y fail；SUB pass |
| 3 | M30 质量复合（水平） | `wp9E1bP2` | 1.13 | 0.73 | 1.35 | 0.73 | — | 5.14% | S/F/2Y fail |
| 4 | M31a flag>0.5 门控 M28 | `LL5d6Z3a` | 1.67 | 1.07 | 1.49 | 0.64 | 0.72 | 5.31% | 2Y+SUB fail（最接近） |
| 5 | M31b flag≤0.5 门控 M28 | `O0Jxk8gp` | −0.83 | −0.46 | −0.31 | −0.40 | — | 6.58% | 全灭；**符号整体反转** |
| 6 | M32 存货占用 | `JjPvmQr2` | 0.65 | 0.31 | 1.00 | 0.32 | — | 4.76% | CW 0.294 + S/F/2Y fail（低覆盖已验证） |
| 7 | M35 修正加速度 | `Grge6O7P` | **1.75** | 0.99 | **1.58** | 0.40 | 0.76 | 3.28% | F 差 0.01、SUB 缺口 |
| 8 | M01 收入增长（actual_*） | `zqrRjbLX` | 1.36 | 0.89 | 1.56 | 0.46 | 0.59 | 5.04% | S/F/2Y(差 0.02)/SUB fail |

**归因（写死，作为 actual_* / 比率族封存依据）**：

1. **应计距离是「高质量低收益」结构，不是可交付信号**：两条 SUB 通过（0.87 / 0.76，SUB/S 0.72 / 0.57），
   但 S 只有 1.21 / 1.33、F 0.78 / 0.88、2Y 1.31 / 1.33。⇒ 该族的高低流动性配比正确、**原始收益强度不足**；
   与 M28（S 高、SUB 低）恰好互补但方向相反。**不可以用 add 拼接**（禁混信号），也不值得再调壳——
   窗口 252→63 只把 S 从 1.21 抬到 1.33，离 1.58 仍差 0.25。
2. **flag 门控不是 regime 分割，而是「剔除 backfill 行」**（2026-10-20 实测字段描述更正）：
   平台原文 `Flag for FA overlay status/provenance (0 backfilled, 1 consensus forecast, 2 actual report)`
   ⇒ **三值 0/1/2**，不是 0/1。因此 `flag > 0.5` 同时含预测(1) 与实际(2)，覆盖率 0.9779，**接近全样本**；
   `flag ≤ 0.5` 只含 backfill(0) 的约 2.2% 稀疏子样本。更正后的读数：
   - `LL5d6Z3a`（flag>0.5）S1.67/F1.07/2Y1.49/SUB0.64 ≈ 全样本去 backfill，**比全样本 `e76xgXkM`（1.89/1.12/1.76/1.05）更差**
     ⇒ 该门控不是杠杆，只是一次质量略降的样本裁剪；
   - `O0Jxk8gp`（flag≤0.5，backfill-only）S−0.83 ⇒ **backfill 行的修正信号方向反转**（陈旧/合成值导致），
     这是一条数据质量事实，**不能解释为「已报窗口反转」**。
   ⇒ 原来设想的「预测 vs 已报」regime 对照并未被实测支持；正确的对照只能是 `flag == 1` vs `flag == 2`，
   且即便要做也不值得再烧配额（见下方用户指令）。**M31 封存（误读已纠正，不再进入 regime-aware）。**
3. **M35 加速度差的是测量口径，不是机制**：S1.75 / 2Y1.58（两闸过）、F 0.99（差 0.01）、
   SUB 0.40（差 0.36）。与 30c 的教训一致：加速度量级未按自身波动归一，子宇宙相对强度被高波动股稀释。
   ⇒ 用 `ts_zscore(加速度, 252)` 复测一次；**若仍 SUB<0.43×S 则封存 M35**。
4. **M01 收入增长在 actual_* 口径下同样缺测量口径**：S1.36 / 2Y1.56（差 0.02）/ SUB 0.46。
   该条本来就没套 `ts_zscore`（预注册写于 30c 结论之前）⇒ 用同一测量口径复测一次是**有依据的诊断**，
   不是扫参。
5. **存货占比确认低覆盖结构性**：CW 0.294（limit 0.1）出现在 2014-01-07，与覆盖率 0.5966 一致；
   即使 backfill 也救不回 S0.65。M32 封存。
6. **封存判定**：按 §3.8 预注册「8 条全灭 ⇒ actual_* 与比率族整体封存」——
   **M29 / M29b / M30 / M32 封存**（合计 4 条，全部 S<1.4 且无 F≥1.0）；
   M31（门控）并入 regime-aware 新构造（M50）继续；M35 / M01 各给一次测量口径复测（M51 / M52）。
   **analyst_consensus 尚未见底**：三条存活线索都用本集字段，不需要换数据集。

### 3.13 批 33 预注册（M50 regime 双边 + M51/M52 测量口径复测）—— **❌ 已取消（2026-10-20 用户指令）**

> **取消原因（用户原话）**：「已点亮塔的数据集先不回测」。平台实测 USA/D1 金字塔
> `analyst = 5`（2026-10-20 `get_pyramid_alphas`），analyst 塔已点亮 ⇒ `analyst_consensus`
> 停止新增回测。本节保留为「若塔位重置/换区时的待测清单」，**不再执行**。
> 同批按更正后的 flag 三值语义重写：`flag == 1` = 预测、`flag == 2` = 实际报告、`0` = backfill；
> 原 M50「预测 vs 已报」设计建立在 0/1 误读上，未实测即作废。

**动机**：批 31 的发现经更正后是「backfill 行信号反转」而非「预测/已报 regime 相反」；
另两条（M35 加速度、M01 收入增长）只差测量口径。三条都来自同一数据集的**已验证字段**，
不是换数据集，也不是把两条信号相加。

设置：REVERSION_AND_MOMENTUM / decay 20 / industry / trunc 0.08（与 30c/31 完全一致）。
壳：`quantile(group_rank(hump(ts_backfill(winsorize(<SIG>, std=4), 252), hump=0.01), industry))`。

| # | 机制 | SIG（已按 flag 三值语义更正） | 方向/预期 |
|---:|---|---|---|
| 1 | ~~M50 regime 双边~~（作废，仅存档） | `trade_when(vec_avg(forecast_actual_flag_eps_annual12_3) == 1, ts_av_diff(vec_avg(mean_forecast_actual_combined_fxadj_eps_annual12), 63), trade_when(vec_avg(forecast_actual_flag_eps_annual12_3) == 2, -1 * ts_av_diff(vec_avg(mean_forecast_actual_combined_fxadj_eps_annual12), 63), 0))` | 正向=预测(1)、反向=实际(2)、backfill(0) 不交易；**未实测** |
| 2 | M50b regime 双边（Δ22） | 同上但内层 Δ22 | 短窗对照；**未实测** |
| 3 | M51 加速度 + 测量口径 | `ts_zscore(ts_av_diff(ts_av_diff(vec_avg(mean_forecast_actual_combined_fxadj_eps_annual12), 63), 63), 252)` | 正向 |
| 4 | M52 收入增长 + 测量口径 | `ts_zscore(ts_av_diff(vec_avg(actual_revenue_value_quarterly16), 63), 252)` | 正向 |
| 5 | M53 应计距离 + 测量口径 | `-1 * ts_zscore(ts_av_diff((vec_avg(actual_netprofit_value_annual12) - vec_avg(actual_cfo_value_annual12)) / vec_avg(actual_total_assets_value_annual12), 252), 252)` | 反向；SUB 已过、只测能否把 S 从 1.21 抬向 1.58 |
| 6 | M54 应计距离 × 收入增长 | `trade_when(ts_av_diff(vec_avg(actual_revenue_value_quarterly16), 63) > 0, -1 * ts_av_diff((vec_avg(actual_netprofit_value_annual12) - vec_avg(actual_cfo_value_annual12)) / vec_avg(actual_total_assets_value_annual12), 252), 0)` | 反向：只在收入扩张公司里做空高应计（**条件门控，不是相加**） |
| 7 | M55 质量×修正 条件 | `trade_when(vec_avg(actual_roe_value_annual12) > 0, ts_zscore(ts_av_diff(vec_avg(mean_forecast_actual_combined_fxadj_eps_annual12), 63), 252), 0)` | 正向：只在盈利公司里交易修正 |
| 8 | M50c regime 双边 + Δ84 | 同 #1 内层 Δ84 | 慢窗对照；**未实测** |

判据（写死）：任一 S≥1.58 / F≥1.0 / 2Y≥1.58 / SUB≥0.75 / TO≥1% **且其余三闸 fail 数 = 0** ⇒ 相关性实测；
若 M50 三窗全部达不到 SUB≥0.75，则 regime-aware 路线封存，**analyst_consensus 的修正族到此为尽**，
按交付日志 §2 转 other685。M51/M52 若在测量口径后 S 仍 <1.4，判该机制收益强度不足、封存。

### 3.14 批 32 收批（M42–M49 财务行项目修正；8/8 COMPLETE，0 颗全过）+ 用户指令收口

multisim `142IJ74Ro4nUaYk1ajMGdOZp`；RAM / decay 20 / industry / trunc 0.08；壳 = 通用壳，
SIG = `ts_zscore(ts_av_diff(vec_avg(F), 63), 252)`（#8 反号在壳外）。

| # | 行项目字段（cov） | alpha | S | F | 2Y | SUB | TO | RA 结论 |
|---:|---|---|---:|---:|---:|---:|---:|---|
| 1 | fxadj_revenue_annual12（0.7528） | `akVElGGx` | 0.99 | 0.45 | −0.10 | 0.41 | 5.19% | 4 fail（含 2Y、SUB） |
| 2 | fxadj_ebit_annual12_2（0.7453） | `LL5d6332` | 1.12 | 0.53 | 1.21 | **0.71** | 4.82% | S/F/2Y fail；SUB pass |
| 3 | pretax_annual12（0.7528） | `ZYmKxN1Y` | 0.80 | 0.33 | 1.00 | 0.36 | 4.96% | S/F/2Y fail |
| 4 | fxadj_reportednet_annual12_2（0.7510） | `0mjMd5ak` | 0.80 | 0.33 | 1.39 | −0.02 | 4.89% | 4 fail（SUB 为负） |
| 5 | fxadj_cfo_annual12（0.7363） | `pwvKE3p6` | 0.87 | 0.46 | 0.81 | 0.50 | 3.94% | S/F/2Y fail |
| 6 | roe_annual12_tribes（0.7300） | `zqrRjeLd` | **1.45** | **0.91** | 1.35 | **0.80** | 4.13% | S/F/2Y fail；**本批最强** |
| 7 | ebitda_annual12（0.7564） | `xA1dQ5Ep` | 0.91 | 0.45 | 0.00 | 0.17 | 3.78% | 4 fail（2Y=0） |
| 8 | −capex_annual12_2（0.7905） | `RRA1YPon` | −0.63 | −0.29 | −1.01 | −0.36 | 4.94% | 反号失败 ⇒ Titman 过度投资假说不成立 |

**归因（写死）**：

1. **分解财务行项目不增益，M28 已是该族的聚合上限**：最强单腿 ROE `zqrRjeLd` 1.45/0.91/1.35/0.80，
   仍低于合并 EPS `e76xgXkM` 1.89/1.12/1.76/1.05。行项目修正的信息被 EPS 汇总时已充分吸收，
   拆分后每条只剩部分信号 + 更多噪声 ⇒ **M42–M49 全部封存**，不再做行项目排列组合。
2. **2Y 普遍缺失是结构性的**：除 EBIT（1.21）与 reportednet（1.39）外，其余行项目 2Y ≤ 1.00，
   EBITDA 甚至为 0 ⇒ 年度行项目的分析师修正缺乏跨年持续性，不适合做长期衰减的慢信号。
3. **Capex 反号失败**：反向（做空高 capex 增长）S −0.63，正向也仅约 +0.63 ⇒ 在 USA/D1/TOP3000
   capex 扩张既不是可靠的负面也不是正面信号（与 Titman/Wei/Xie 的过度投资假说在本口径不兼容）。
4. **收口**：`analyst_consensus` 修正族最终只交付 1 颗（#7 `e76xgXkM`）；M01/M35 的测量口径复测
   （原 §3.13 M51/M52）随批 33 一并取消。**该数据集除已交付机制外不再新增回测。**
5. **用户指令（2026-10-20）**：「已点亮塔的数据集先不回测」。`get_pyramid_alphas` 实测
   USA/D1 `analyst = 5`（model = 4、earnings = 1 亦亮）⇒ analyst 塔已点亮，
   `analyst_consensus` / `analyst44` / `analyst_factor_signals` 全部停止新增回测。
   **后续只从未点亮塔（pv / other / shortinterest / institutions / option / insiders / news / sentiment …）选数据集。**
