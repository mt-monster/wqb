# EUR × fund_holdings_panel · W3 救援波模板池（2026-11-09，论坛取证后）

> 触发：W1-B 全量复核 best |S| 0.47 + TO 爆炸 6/10，原判死程序已启动；**判死前论坛取证发现活读数**（seal 取证闸的正面价值）。
> 论坛证据：41049370096663（SZ83096，22赞，EUR/TOP2500 四轮 75+ 表达式）+ 41049450679191（验证改进篇）。
> 核心发现：stable_boundary_trade_count_21d = 唯一活字段（持久性仓位变化=机构信息优势）；holder_account_total 最毒（−0.88，与 W1-B1 互证）。
> 论坛最佳：ts_decay_linear(group_zscore(vec_avg(stable_boundary_trade_count_21d),sector),20) S0.93/2Y2.28/F0.48。
> 设置：EUR/**TOP2500**（论坛原档，复现优先）/D1/SUBINDUSTRY/decay4/trunc0.08/maxTrade OFF/nan ON。
> 边界档：ts_decay_linear 20/60 与 ts_mean 20 已凭论坛实证补录 boundary_ops_eur.json（2026-11-09）。
> 覆盖口径：W1-B 已过 30/30 全量覆盖闸；本波为 S4 救援（单读数深化），不再要求批内全字段覆盖。

| ID | 骨架 | 论坛对应 | 来源 |
|---|---|---|---|
| R1 | ts_decay_linear(group_zscore(vec_avg(sb21d),sector),20) | 最佳 S0.93/2Y2.28 | forum 41049370096663 |
| R2 | group_zscore(ts_decay_linear(vec_avg(sb21d),20),sector) | S0.93/2Y2.27（先时序后截面对照） | forum |
| R3 | ts_decay_linear(group_zscore(vec_avg(sb21d),sector),60) | S0.91/**2Y2.44**（2Y 最强） | forum |
| R4 | ts_mean(group_zscore(vec_avg(sb21d),sector),20) | S0.91/2Y2.27 | forum |
| R5 | R1 换 industry 轴 | 分组轴 sweep | self（EUR 多轴纪律） |
| R6 | R1 换 country 轴 | 分组轴 sweep | self（EUR 跨国事实） |
| R7 | rank(R1) | 截面整形 | self（ATOM 战役包装栈经验） |
| R8 | ts_decay_linear(group_scale(group_zscore(vec_avg(sb21d),sector),industry),20) | prod 杠杆 −0.057 预置 | eur skill ④ group_scale 首选 |
| R9 | R1 换 _active 字段 | 主动账户口径对照 | self（W1 字段对设计） |
| R10 | signed_power(R1,1.5) | S 抬升杠杆 | eur 边界档 1.5 |

备用杠杆（W4 视结果）：STATISTICAL 中性化 + decay6（论坛 XD81759「小而稳」TWN FHP TO 0.078 实测）；TOPCS1600 对照档；持仓价值类 ts_rank+rank / 集中度类 −rank+ts_mean（论坛模板库）。
