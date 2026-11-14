# Wave BA5 dispatch — fund_holdings_panel 12 模板池首派（2026-11-10 19:4x，PTC 恢复后）

> 背景：pv29 字段自测否决（50 字段全是统计行业簇标签，只能当分组轴，不能做单数据集信号）。
> 转向 11-03 已设计但从未派发的 fund_holdings_panel 模板池（institutions 塔位 1，差 2 点亮；18 VECTOR cov 0.88-0.93）。
> 取证：Lou 2012 流量价格压力 / Shive-Yun 2013 抢跑 / Miller 1977+Diether 2002 分歧论 / Swedroe smart money 反方 + 论坛 13F 时滞帖。

| # | alpha 表达式 | 机制 |
|---|---|---|
| F1 | -group_rank(ts_mean(ts_backfill(vec_sum(boundary_transaction_total),132),22), subindustry) | 事件活动反向（Miller 分歧论） |
| F2 | group_rank(divide(bf(vec_sum(stable_boundary_trade_count_21d)), add(bf(vec_sum(boundary_transaction_total)),1)), subindustry) | 稳定边界占比（conviction 共识） |
| F3 | group_rank(ts_mean(bf(vec_avg(herfindahl_index_transactions)),22), subindustry) | 集中度正向（知情交易） |
| F4 | 同 F3 取负 | 集中度反向对照（流动性冲击） |
| F5 | group_rank(ts_mean(divide(bf(vec_avg(HHI_active)), add(bf(vec_avg(HHI_total)),0.0001)),22), subindustry) | active/total 主动基金净差 |
| F6 | group_rank(ts_delta(ts_mean(bf(vec_sum(transaction_account_total)),22),22), subindustry) | 参与广度变化（共识扩散） |
| F7 | group_rank(divide(bf(vec_sum(large_trade_count_50bps)), add(bf(vec_sum(transaction_account_total)),1)), subindustry) | 大单占比（conviction 强度） |
| F8 | group_rank(multiply(rank(ts_mean(bf(vec_avg(HHI)),22)), rank(ts_mean(bf(vec_sum(boundary_total)),22))), subindustry) | 集中 x 活动交互 |
| F9 | -group_rank(ts_mean(bf(vec_sum(boundary_transaction_usd_value)),22), industry) | 价值事件反向 x 第二分组轴 |
| F10 | group_rank(ts_delta(divide(bf(vec_sum(security_transaction_usd_value)), add(bf(vec_sum(transaction_account_total)),1)),66), subindustry) | 单笔规模漂移 |

全部 ≤10 算子；设置 DEU/TOP500/D1/decay4/SUBINDUSTRY/trunc0.08/nanON。留待后续：T11 双塔门控（institutions6 净流方向腿）、T12 双集中度净额。
收割后按口径：逐年 longCount > 0 检查（近十年覆盖），max|S| ≥1.2 进逐闸破墙，否则按新闸记证据。
---

## BA5 收割（sim 46JbfOnj4XdcyoUc4gpkL，10/10 COMPLETE，0 error）

| # | 模板 | alpha | S | 2Y | sub | lc | TO |
|---|---|---|---:|---:|---:|---:|---:|
| F1 | 事件活动反向（Miller 分歧论） | MP6jkq8z | **-0.54** | -1.26 | -0.26 | 153 | 0.079 |
| **F2** | **稳定边界占比（conviction 共识）** | **xAvKR9mb** | **0.65** | **1.77** | 0.33 | 134 | **0.467** |
| F3 | 集中度正向（知情交易） | leaLrkQO | -0.27 | -0.64 | -0.23 | 142 | 0.049 |
| F4 | 集中度反向对照 | zqdvOQPO | 0.27 | 0.64 | 0.23 | 151 | 0.049 |
| F5 | active/total 净差 | VkNvOq25 | 0.07 | 0.93 | -0.31 | 141 | 0.093 |
| F6 | 参与广度变化 | kqaxQbnl | 0.43 | -0.69 | 0.45 | 144 | 0.135 |
| F7 | 大单占比（conviction 强度） | zqdvOQ5O | 0.23 | 0.98 | -0.06 | 131 | 0.376 |
| F8 | 集中 x 活动交互 | xAvKR9eb | 0.30 | 0.64 | 0.32 | 144 | 0.095 |
| F9 | 价值事件反向 x industry | d5a2dgnv | -0.31 | 0.02 | -0.18 | 153 | 0.132 |
| F10 | 单笔规模漂移 | VkNvOqOV | -0.39 | -0.45 | -0.06 | 151 | 0.545 |

**归因**：
1. **F2（稳定边界占比）族冠**：S0.65 / 2Y1.77 / lc134，但 **TO 0.467 逼近 0.7 硬闸**（margin 被压）——单臂不可作组合腿。
2. **F1 事件活动反向为负（-0.54/-1.26）** ⇒ Miller 分歧论「高活动=高估→反向」在 DEU 不成立；反读即「活动高→收益好」。
3. **F3/F4 严格对称（±0.27）** ⇒ 集中度字段无方向信息（纯噪声面）。
4. 方向面（F5/F8 弱正、F7 TO0.376）全不足；F10 规模漂移 TO0.545 过高。

**判定**：族天花板 **0.65** 距 1.58 差 0.93；D6 第二配置未测但缺口过大，配置救不了 ⇒ **fund_holdings_panel 信号层弱（PROVISIONAL，1 波 10 臂全测）**，不判死、不追投。
证据链：本波 10 臂 = institutions 塔第 2 个数据集的完整实测（institutions6 已二次判死），institutions 塔内无剩余强信号面。