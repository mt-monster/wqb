# BE13 波派发记录（2026-11-11）

**目的**：篮子 7 件已被「4 纯 analyst 预估族 + 3 借券族」占满；news/earnings/institutions/sentiment/risk/option/macro/imbalance/workforce 零覆盖 ⇒ 相关性空白。
本波用**已验证骨架**（`group_zscore(add(A, B), market)` + `sector` 内层 + `ts_backfill 132`）只替换**第一腿**为新数据集，找与篮子低相关的新成员。

**multisim**：`3afxPLfG84lea2KV3oo4IVk`（10 臂）
**设置**：DEU / TOP500 / D1 / decay4 / SUBINDUSTRY / truncation 0.08 / pasteurization ON / unit VERIFY / nan ON
**算子数**：每臂 11 个（≤12 上限）

| 臂 | 第一腿 × 第二腿 | 机制 | 塔组合 |
|---|---|---|---|
| A1 | lending_fee_bid_rate Δ220 × I7 内部人持股 | 证券借贷费 = 做空需求直接观测（新数据集） | SHORT/LENDING × INSIDERS |
| A2 | lending_fee_bid_rate Δ220 × shrt3_bar Δ132 | 双做空需求面（新×旧） | SHORT × SHORT |
| A3 | loan_rate_volatility Δ220 × I7 | 借券利率波动（挤兑风险） | SHORT/LENDING × INSIDERS |
| A4 | loaned_market_value_usd Δ220 × shrt3_bar Δ220 | 借出市值（空头存量） | SHORT × SHORT |
| A5 | opt1_p_deltasurface_d1_vi Δ66 × I7 | 期权隐含波动变化（OPTION 塔 0） | OPTION × INSIDERS |
| A6 | opt1_p_deltasurface_d1_vi Δ66 × shrt3_bar Δ220 | 期权 IV × 做空需求 | OPTION × SHORT |
| A7 | rsk60_crowding Δ66 × I7 | 风险拥挤度（RISK 塔 0） | RISK × INSIDERS |
| A8 | inst25_concentration Δ66 × shrt3_bar Δ220 | 机构集中度（INSTITUTIONS） | INSTITUTIONS × SHORT |
| A9 | nws20_multiple_comp_event_sentiment_score Δ66 × I7 | 新闻事件情绪（NEWS 塔 0） | NEWS × INSIDERS |
| A10 | rsk60_crowding Δ66 × opt1_p_deltasurface_d1_vi Δ66 | 纯新族配对（RISK×OPTION） | RISK × OPTION |

## 设计依据

1. **I7 第二腿**（`group_rank(ts_rank(ts_backfill(vec_avg(insd1_holdings),132),252),sector)`）是 qM7KxkQV 的已验证冠军第二腿 —— 换成新第一腿后，与 qM7KxkQV 共享的只有一半信号，预期互相关 0.4-0.6（<0.7 阈值）。
2. **shrt3 第二腿**用于构造「新族 × 做空需求」交叉，避开 I7 共享导致的族内高相关。
3. **禁混合规**：所有配对避开 {PV, MODEL, OTHER, FUNDAMENTAL} 集合内两两；NEWS/RISK/OPTION/INSTITUTIONS/INSIDERS/SHORTINTEREST 两两皆在集合外或单腿在集合内。
   - ⚠ lending_* 与 loaned_* 的数据集 category 尚未确证；若为 OTHER，则 A2/A4（与 shrt3 配对）为 集合内×集合外，占用 ≤5 配额（当前已用 2/5）。
4. **符号取法**：做空需求/拥挤度/IV 上升全部取负（bearish）；机构集中度、新闻正面情绪取正。若某臂出现 |S| 高但为负，下一波直接翻号。

## 待验证

- 10 臂是否 COMPLETE；ERROR 臂提示字段名无效（lending_*/opt1_*/rsk60_*/inst25_*/nws20_* 需按平台实际名核对）。
- 出货臂需过：S≥1.58 / F≥1.0 / 2Y≥1.58 / sub≥0.474×S / TO≤0.7 / 与 7 件篮子全对 <0.7。
