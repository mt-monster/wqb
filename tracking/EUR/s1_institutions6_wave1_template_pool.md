# EUR × institutions6 · W1 模板池（goal eur15，2026-11-09）

> 设置（profiles explain 生效档，逐项显式传）：EUR/TOPCS1600/D1/SUBINDUSTRY/decay4/trunc0.08/maxTrade OFF/pasteurization ON/unit VERIFY/nan ON/FASTEXPR
> 字段全集：11/11（MCP 2026-11-09 complete=true）；本池 12 模板（10 派发 + 2 备用），8 结构族，字段覆盖 100%
> 来源标注：forum=论坛帖 / paper=金融论文 / self=自建 / eur=本区历史实证

## 模板清单

| ID | 族 | 骨架要点 | 字段 | 来源 | 状态 |
|---|---|---|---|---|---|
| T1 | flow_breadth_z | (B−S)/H 季频回填120→时序z66→截面rank（已验证小腿读数作 ATOM 复核） | B,S,H | eur leAXvaLn + paper Bennett-Sias-Starks(2003) | 派发 A1 |
| T2 | penetration_delta_value | 金额机构化率 AEV_INST/AEV_ALL 的季度变化 ts_delta 66 | AEV_INST,AEV_ALL | paper Gompers-Metrick(2001) | 派发 A2 |
| T3 | netflow_intensity_value | 净买入金额 / 机构持仓市值（流量强度） | MVA,MVD,AEV_INST | paper Bennett-Sias-Starks(2003) | 派发 A3 |
| T4 | execution_price_premium | (MVA/QA)/(MVD/QD) 机构买入均价 vs 卖出均价 = 付溢价买入 | MVA,QA,MVD,QD | forum 43664593081879（金额÷股数=成交均价）延伸 | 派发 A4 |
| T5 | conviction_per_holder_z | 户均仓位 AEV_INST/H 的时序 z252（信念强度） | AEV_INST,H | forum 43664593081879（存量÷家数） | 派发 A5 |
| T6 | buyer_share_momentum | 买家占比 B/(B+S) 的季度动量 ts_delta 66 | B,S | paper Bennett-Sias-Starks(2003) 变化可预测 | 派发 A6 |
| T7 | penetration_delta_shares | 股数机构化率 ASC_INST/ASC_ALL 年度变化 ts_delta 252 | ASC_INST,ASC_ALL | forum 43664593081879（机构化率股数口径） | 派发 A7 |
| T8 | country_relative_breadth | (B−S)/H 的 country 组内 z（EUR 跨国事实；死档注记 country 轴 2Y 1.89 值得复用） | B,S,H | eur 死档注记 + forum 43497507223191（IND 广度） | 派发 A8 |
| T9 | institutional_turnover | (MVA+MVD)/AEV_INST 机构换手率 | MVA,MVD,AEV_INST | forum 43664593081879（流量÷存量） | 派发 A9 |
| T10 | execution_price_level | MVA/QA 机构买入均价水平（USA 裸结构最强族 S0.85，中性化后复核） | MVA,QA | forum 43664593081879 | 派发 A10 |
| T11 | breadth_ratio_forum | B/(S+1) 广度比（分母+1 平滑） | B,S | forum 43664593081879 | 备用（S4 杠杆） |
| T12 | slow_gate_hysteresis | trade_when(rank(机构化率)>0.5, CORE, -1) 慢开关 | AEV_INST,AEV_ALL | eur 类别卡（季频慢变量适合门控） | 备用（W2 组合用） |

## 字段覆盖矩阵（11/11）

B: T1,T6,T8,T11 | S: T1,T6,T8,T11 | H: T1,T5,T8 | MVA: T3,T4,T9,T10 | MVD: T3,T4,T9 | QA: T4,T10 | QD: T4 | AEV_ALL: T2,T12 | AEV_INST: T2,T3,T5,T9,T12 | ASC_ALL: T7 | ASC_INST: T7

## 纪律核对
- 算子数 ≤12：A1=5,A2=3,A3=3,A4=5,A5=3,A6=4,A7=3,A8=3,A9=3,A10=2 ✓
- 边界档：ts_backfill 120 ✓（2026-11-08 补录档）/ ts_zscore 66,252 ✓ / ts_delta 66,252（类别卡季度窗）✓ / group_zscore country ✓（group_rank 无 country 档，故用 group_zscore）
- 禁混：单数据集 ATOM，无跨集腿 ✓；无 add(A,B) 混信号（A6/A9 的 add 是同族计数/金额合成，单一读数）✓
- 论坛提示采纳：季频先 ts_backfill（T1）；金额与股数不直接相减（T4 用比值）✓；裸水平吃小盘暴露→SUBINDUSTRY 中性化 ✓
