# EUR × fund_holdings_panel · W1 模板池（goal eur15，2026-11-09）

> 设置（profiles explain 生效档）：EUR/TOPCS1600/D1/SUBINDUSTRY/decay4/trunc0.08/maxTrade OFF/pasteurization ON/unit VERIFY/nan ON/FASTEXPR
> 字段全集：30/30（MCP 2026-11-09 complete=true，全 VECTOR 需 vec_*）；本池 12 模板（10 派发 + 2 备用），5 结构族，字段覆盖 100%
> 核心设计：base=全部基金账户，_active=主动管理账户 ⇒ **passive = base − active**（指数/被动账户行为），active−base 差分=主动超额行为。25 个 aC=0 白地字段全部入表达式。
> 历史判死程序缺陷：旧探针仅覆盖 5/30 字段（覆盖闸未过）⇒ 本波补全量后才允许重判。

## 模板清单

| ID | 族 | 骨架要点 | 字段（base/active 对） | 来源 | 状态 |
|---|---|---|---|---|---|
| F1 | passive_boundary_density | (边界交易数_all − 边界交易数_active)/持有账户数 = 被动账户换仓密度 | boundary_transaction_total ×2, holder_account_total | self + paper LSV(1992) 交易冲击 | 派发 B1 |
| F2 | active_boundary_turnover | 主动边界交易USD净差 / 被动持仓USD = 主动-driven 换手强度 | boundary_transaction_usd_value ×2, security_holding_usd_value ×2 | self | 派发 B2 |
| F3 | passive_hhi_delta | 被动持仓 HHI 年度变化 ts_delta252（历史最强方向 S0.80 的主动/被动分解） | herfindahl_index_holdings ×2 | eur 历史最好方向 + self 分解 | 派发 B3 |
| F4 | trade_hhi_active_spread | 交易 HHI 主动−全体散度（主动交易集中度溢价） | herfindahl_index_transactions ×2 | self + paper Sias(2004) 羊群 | 派发 B4 |
| F5 | passive_conviction_share | 被动信念账户数 / 主动持有账户数 = 被动 conviction 结构 | top_weighted_account_number ×2, holder_account_total_active | self | 派发 B5 |
| F6 | passive_conviction_trade_intensity | 被动信念交易数 / 被动交易账户数 | top_weighted_transaction_number ×2, transaction_account_total ×2 | self | 派发 B6 |
| F7 | passive_crowding_divergence_z | 被动持仓拥挤 z252 − 被动交易拥挤 z252 = 持有者/交易者拥挤背离 | holding_value_distribution_score ×2, transaction_value_distribution_score ×2 | self + paper Sias(2004) | 派发 B7 |
| F8 | stable_boundary_persistence | 被动稳定边界交易数 / 交易USD = 持续换仓强度（21周无 prior 的稳健版） | stable_boundary_trade_count_21d ×2, security_transaction_usd_value | eur 历史 T9 持续性 + self | 派发 B8 |
| F9 | passive_large_trade_attention | 被动大单数/主动交易USD 的 66d 均值 = 大单注意力 | large_trade_count_50bps ×2, security_transaction_usd_value_active | eur 历史 T10 大单 + self | 派发 B9 |
| F10 | weight_conviction_ratio | 全体平均权重 / 主动平均权重 = 被动超配程度 | mean_security_weight ×2 | self | 派发 B10 |
| F11 | hhi_level_z | ts_zscore(vec_avg(HHI_holdings),252) 集中度水平 z | herfindahl_index_holdings | eur 历史 | 备用（S4） |
| F12 | boundary_usd_momentum | ts_delta(vec_avg(边界USD),66) 事件金额动量 | boundary_transaction_usd_value | self | 备用（S4） |

## 字段覆盖：30/30（每字段恰出现在 1 条派发表达式）
B1: btt,btt_a,hat | B2: btuv,btuv_a,shuv,shuv_a | B3: hih,hih_a | B4: hit,hit_a | B5: twan,twan_a,hat_a | B6: twtn,twtn_a,tat,tat_a | B7: hvds,hvds_a,tvds,tvds_a | B8: sbtc21,sbtc21_a,stuv | B9: ltc50,ltc50_a,stuv_a | B10: msw,msw_a

## 纪律核对
- 算子数 ≤12：B1=6,B2=8,B3=5,B4=4,B5=6,B6=8,B7=9,B8=6,B9=7,B10=4 ✓
- VECTOR 全部经 vec_sum（计数）/vec_avg（分值/金额）聚合 ✓（否则 does not support event inputs）
- 边界档：ts_delta 252 / ts_zscore 252 / ts_mean 66 ✓
- TO 风险预案：季频申报跳变可能 TO 爆（insiders1 前科）；若 TO>0.7 按类别判据弃该读数，S4 上 ts_mean 平滑/ts_backfill
- 禁混：单数据集 ATOM ✓；B7 的 subtract 是同机制（拥挤）两读数背离，非独立信号混加 ✓
