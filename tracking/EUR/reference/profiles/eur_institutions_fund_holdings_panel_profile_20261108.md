# EUR × fund_holdings_panel 字段画像（2026-11-08）

> 平台目录：30/30 字段全量拉取（complete=true，全部 VECTOR，需 vec_* 聚合）
> **2026-11-09 复核（goal eur15）**：MCP 重拉 complete=true，30 字段 cov 不变（base 0.908–0.918 / _active 0.843–0.857）；25 字段 aC=0。⚠ 历史 ATOM 判死仅覆盖 5/30 字段，覆盖闸未过⇒判死程序不合法，W1 补全量探测后重判。见 s0_institutions_scan_20261109.md。
> **2026-11-09 W1-B 收批 + 论坛改判**：全量复核 best |S| 0.47（B10 权重conviction比）+ TO 爆炸 6/10（比率/散度读数 × 季频跳变）；历史最强 ts_delta(HHI,252) 重算后 −0.07。**但判死前论坛取证发现活读数**：stable_boundary_trade_count_21d 水平 z+decay（论坛 41049370096663，EUR/TOP2500 S0.93/2Y2.28）⇒ 判死中止，W3 救援波在飞。旧结论「ATOM 通道判死（returns 封顶）」仅适用于比率/散度读数族，水平 z+decay 族待 W3 裁决。holder_account_total 最毒（论坛 −0.88 / W1-B1 互证）。
> **2026-11-09 W3 收批：机制复活实锤**——论坛读数重算后 S1.06/2Y1.92；**_active 口径 GrWjbP7G S1.45/2Y2.30/sub1.23/ret5.42% 近闸**；ts_mean 几何控 TO 12.6%（O0AdNOgJ）。判死条目已改范围（仅比率/散度族死）。W5 杂交波（_active×ts_mean）在飞。本集从「判死」改档「近闸主力候选」。
> 塔位：INSTITUTIONS(×1.1)；拥挤度：userCount 0–6 / alphaCount 0–10（几乎无人使用）

## 一、字段族分组

| 族 | 字段（含 _active 变体） | cov | 语义 | 适用性 |
|---|---|---|---|---|
| F1 边界交易 | boundary_transaction_total(+_active)、boundary_transaction_usd_value(+_active)、stable_boundary_trade_count_21d(+_active) | 0.843–0.908 | 新建仓/清仓事件计数（21d 稳健版更耐噪） | 事件型门控；TO 风险高（季频跳变） |
| F2 集中度 | herfindahl_index_holdings(+_active)、herfindahl_index_transactions(+_active) | 0.843–0.918 | HHI 持仓/交易集中度 | **历史最好方向 ts_delta(herfindahl_index_holdings,252) S0.80–0.81**；F 数学封顶 |
| F3 账户广度 | holder_account_total(+_active)、transaction_account_total(+_active) | 0.843–0.918 | 持有/交易账户数 | 广度读数，可做小腿 |
| F4 信念持仓 | top_weighted_account_number(+_active)、top_weighted_transaction_number(+_active) | 0.843–0.918 | 前列为 conviction holding 的账户/交易数 | 聪明钱广度，小腿备选 |
| F5 持仓水平 | security_holding_usd_value(+_active)、security_transaction_usd_value(+_active)、mean_security_weight(+_active) | 0.843–0.918 | 持仓金额/权重水平 | 慢变量，仅分母/门控 |
| F6 分布得分 | holding_value_distribution_score(+_active)、transaction_value_distribution_score(+_active) | 0.843–0.908 | 拥挤度自定义指标 0–1 | 门控条件（拥挤>阈值时降杠杆） |
| F7 大单 | large_trade_count_50bps(+_active) | 0.843–0.908 | >0.5%AUM 交易数 | 机构大单注意力，小腿备选 |

## 二、EUR 历史实证

- **ATOM 判死（F 数学封顶）**：EUR-FHP-INSTITUTIONS-WEAK。有效方向 ts_delta(herfindahl_index_holdings, 252)（机构持仓集中度变化）S 0.80–0.81（幂次 3.0 仅 +0.01）；反推 returns 仅 2.33% ⇒ S=1.58 时 F 上限 = 1.58×sqrt(0.0233/0.125) = 0.68 < 1.0 ⇒ **数学上不可能过 F 闸**。
- 30 VECTOR 字段须 vec_avg/vec_sum 聚合后使用；TO 爆炸风险（季频申报跳变）。

## 三、结论

1. ATOM 通道判死（returns 封顶，结构性不可修复——杠杆清单已扫过幂次/换手两档）。
2. 本战役仅作 INSTITUTIONS 小腿备选（G3 账户广度 vec_avg(holder_account_total) / G4 信念持仓 vec_sum(top_weighted_account_number)）与慢门控（F6 拥挤度条件）。不投主信号槽。
3. 覆盖率豁免不适用（cov ≥0.84）；判死类型 = returns 不足（F 闸）。
