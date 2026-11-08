# s1_fund_holdings_panel_wave1 模板池（DEU / TOP500 / D1 / SUBINDUSTRY）

数据集：fund_holdings_panel（institutions 塔，18 VECTOR，cov 0.88-0.93）。**单塔合法**；与 institutions6 同塔组合也合法（同 category 不算塔混，不占 trio×非trio 配额）。

## 一、关键设计约束（face-value 实证）

- **boundary_transaction_* 把「新建仓 + 完全清仓」合并计数，无方向**：纯本集臂的方向先验只能靠分歧论/反转论，或以 institutions6 净流为方向腿（第二数据集只能以条件/门控入场）。
- active vs total 是天然对照变体（主动基金信号 vs 含被动噪声）。
- VECTOR 数值位必须 vec_sum/vec_avg 聚合；「笔数」族用 vec_sum，「分数/HHI」族用 vec_avg。

## 二、论坛+论文取证（2026-11-03）

- 论坛：institutions18 金帖（已全文读，见 institutions6 台账）+ IVA/MFM/CNI 三分法 + **「13F 披露时滞下的思考」新帖**（公告后漂移效应：抄作业/再平衡资金在公告密集周制造可预测漂移）。
- 论文：**Lou (2012 RFS) 流量价格压力**（资金流制造可预测价格压力=流量字段方向先验）；**Shive & Yun (2013 JFE)** 基金交易被抢跑（集中度字段意义）；**Diether-Malloy-Scherbina (2002) / Miller (1977) 分歧论**（高交易活动=高分歧→高估→反向）；Swedroe「smart money 效应不存在」=反方对照；「Mutual fund alpha as predictor」=conviction 交易先验。
- 开放问题臂 ≥3：方向不可分（T1 Miller 反向 vs T3 知情集中正向的对照）、active-total 差异（T5）、smart money 反方（T9 反向对照）。

## 三、模板池（12 结构互异；照抄臂 0（本集无可照抄配方，金帖机制照抄计入 institutions6 波））

| # | 骨架 | 机制/方向先验 | 来源 |
|---|---|---|---|
| T1 | −rank(ts_mean(vec_sum(boundary_transaction_total), 22)) 事件活动反向 | Miller 分歧论：高活动=高分歧→高估 | Miller 1977/Diether 2002 |
| T2 | rank(divide(vec_sum(stable_boundary_trade_count_21d), vec_sum(boundary_transaction_total))) 稳定边界占比 | 持久 conviction 共识→正 | 数据集自带去噪定义 |
| T3 | +rank(ts_mean(vec_avg(herfindahl_index_transactions), 22)) 集中度正向 | 单账户集中=知情交易 | Shive-Yun 2013 |
| T4 | −rank(同 T3) 集中度反向对照 | 集中=流动性冲击→反向 | 开放问题对照臂 |
| T5 | rank(subtract(vec_avg(..._active), vec_avg(..._total))) active−total 差 | 主动基金知情度净差 | 文献主动vs被动 |
| T6 | rank(ts_delta(ts_mean(vec_sum(transaction_account_total), 22), 22)) 参与广度变化 | 共识扩散 | CHS2002 广度迁移 |
| T7 | rank(divide(vec_sum(large_trade_count_50bps), vec_sum(transaction_account_total))) 大单占比 | conviction 规模强度 | conviction 交易文献 |
| T8 | multiply(集中度 rank, 事件活动 rank) 集中×活动交互 | 知情活动共振 | Shive-Yun × Miller |
| T9 | −rank(ts_mean(vec_sum(boundary_transaction_usd_value), 22)) 价值事件反向 | smart money 反方（Swedroe） | Swedroe 反方臂 |
| T10 | rank(平均单笔规模变化: divide(usd_value, count) 的 ts_delta) | 单笔规模漂移=交易意图变化 | 自建 |
| T11 | trade_when(conviction 门控, institutions6 净流反转, -1) 双集门控 | 方向腿=inst6 净流，事件腿=本集 conviction | Lou 2012+金帖A（同塔合法） |
| T12 | rank(subtract(vec_avg(herfindahl_index_transactions), vec_avg(transaction_value_distribution_score))) 双集中度净额 | 同机制两度量差=稳健集中度 | 自建（同机制净额合规） |

## 四、硬闸提醒

- 量纲：同族 add/subtract 后 divide；vec 函数按语义选 sum/avg；T10 的 divide(usd, count)=USD/笔 新量纲，再做 ts_delta 后 rank，不与他量纲 add。
- T11 塔混核对：institutions6+fund_holdings_panel = institutions 单塔 ✓；门控形态用极值剔除/条件触发（阈值型会吃 S，参考 EUR 实证用 trade_when 形态）。
- 稀疏性：boundary/transaction 字段是「当日计数」型，逐日有值（cov 0.93）非季度步进，可用 ts_mean 平滑后差分；但事件日可能尖峰，ts_sum 窗口兜底。
- 派发前双预检 + get_operators 精确名单核对（trade_when 签名按论坛帖 trade_when(x, h, expires) 语义与 news20 M4 已验证形态一致）。

## 五、执行状态

- 排队：① 重试池补发（snt7 8 + oth250 2）② institutions6_wave1（就绪）③ 本波（设计完成，待落表达式+双预检）。
