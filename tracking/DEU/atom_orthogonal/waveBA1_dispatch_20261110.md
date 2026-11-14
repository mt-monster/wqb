# Wave BA1 dispatch — 判死撤判重开第一波：risk60 + risk88（2026-11-10）

> 触发：用户指令「判死的太快了」⇒ 六维审计（DEATH_AUDIT_20261110.md）将 risk60/risk88 撤判。
> risk60 在波 N 仅 ~5 条无 backfill 简单读数 + 判据 MH 先验封死；本波按 MI 教训全部 ts_backfill(vec_avg()) 转面板重测。

设置：DEU/TOP500/D1/decay4/SUBINDUSTRY/trunc0.08/nanON/maxTradeOFF（全战役统一档）
字段事实（get_datafields 实测）：rsk60_crowding/lending_fee_bid_rate/rsk60_last/rsk60_offer 均 VECTOR cov0.835；risk88 alternative_market_cap_usd MATRIX cov1.0；risk68/71/72 全字段 cov=0（数据层排除，死因标签已更正）。

| # | 模板 | 表达式 | 算子 |
|---|---|---|---:|
| B1 | crowding 水平 | group_rank(ts_mean(ts_backfill(vec_avg(rsk60_crowding),132),22), subindustry) | 4 |
| B2 | crowding 流量（做空活动变化） | group_rank(ts_delta(ts_backfill(vec_avg(rsk60_crowding),132),22), subindustry) | 4 |
| B3 | 借出费率水平 | group_rank(ts_mean(ts_backfill(vec_avg(rsk60_offer),132),66), subindustry) | 4 |
| B4 | 费差（offer−bid，借贷供需张力） | group_rank(ts_mean(subtract(ts_backfill(vec_avg(rsk60_offer),132), ts_backfill(vec_avg(lending_fee_bid_rate),132)),66), subindustry) | 7 |
| B5 | 费率动量 | group_rank(ts_delta(ts_backfill(vec_avg(rsk60_offer),132),66), subindustry) | 4 |
| B6 | 费率信噪比 | group_rank(ts_ir(ts_backfill(vec_avg(lending_fee_bid_rate),132),252), subindustry) | 4 |
| B7 | 费率波动（不确定性溢价，反向） | multiply(-1, group_rank(ts_std_dev(ts_backfill(vec_avg(rsk60_offer),132),252), subindustry)) | 5 |
| B8 | 拥挤×费率交互 | group_rank(ts_mean(multiply(ts_backfill(vec_avg(rsk60_crowding),132), ts_backfill(vec_avg(rsk60_offer),132)),22), subindustry) | 7 |
| B9 | 第二分组轴（industry） | group_rank(ts_mean(ts_backfill(vec_avg(rsk60_crowding),132),66), industry) | 4 |
| B10 | risk88 市值反转 | multiply(-1, group_rank(ts_backfill(alternative_market_cap_usd,66), subindustry)) | 4 |

派发状态：首派 12 条被拒（上限 10）→ 10 条二派 429（AN 占槽）→ 后台退避重试 cache/_watchBA1_retry.ps1，成功后 sim id 落 cache/_out_BA1_dispatch_ok.json。
顺延 BA1b：ts_rank 非线性 1 条 + risk88 industry 轴 1 条。
机制先验：借券费率面在 shortinterest3 族 S1.64-1.85（2023 脆弱已知）；risk60 的 crowding 是带符号流量读数，与 shrt3_bar（需求评级）不同信息面——若出货须与 E569ZE7L 查互相关。

---

## BA1 收割（sim 2N0fo53az4Cu9721ZzTUIA8，10/10 COMPLETE，0 error，约 7 分钟）

金字塔命中 DEU/D1/RISK（x1.5）；CW 全过。

| # | 模板 | alpha | S(raw) | 翻转后 |
|---|---|---|---:|---:|
| B1 | crowding level sub | 78Yk8PRZ | -0.29 | +0.29 |
| B2 | crowding delta22 | ZYaRYVv8 | -0.25 | +0.25 |
| B3 | 借出费率水平 | MP6jPvv9 | **-0.55** | **+0.55** |
| B4 | 费差 offer−bid | qM7KM22j | **-0.49** | **+0.49** |
| B5 | 费率动量 delta66 | 1YWqY33R | -0.24 | +0.24 |
| B6 | 费率 IR 252 | gJaYJNlK | +0.12 | — |
| B7 | 负费率波动 252 | npa1pGja | +0.41 | — |
| B8 | 拥挤 x 费率交互 | RReJRxgj | -0.16 | +0.16 |
| B9 | crowding level industry | KPgKPA18 | -0.11 | +0.11 |
| B10 | risk88 市值反转 | GrmqrjRQ | -0.11 | — |

归因（判据 MG）：费率/拥挤面 7 条中 6 条同号（负）⇒ 方向一致非噪声——高借券费股未来收益更差，与 shortinterest3 借券需求机制同向。翻转后探针天花板 +0.55（B3）/+0.49（B4）。B7（负费率波动）+0.41 留观察。

处置：按新闸「探针不产生判死」，risk60 升级 BA2 十模板池（shortinterest3 冠军骨架 tvr_decay 双窗 x 翻转，判据 MX：判死只在当时骨架下成立）；risk88 补 delta/ts_rank 两维凑单字段族三维自测。
