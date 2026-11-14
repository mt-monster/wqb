# Wave AY dispatch — DEU D0 探针（delay=0 新矿脉首波）2026-11-10 16:10

sim_id: 1eVz5dRo53iaQO88TwXKfr（try 1 无 429）

背景：checkpoint 探明 DEU 支持 delay=0（TOP500），DEU/D0 金字塔全塔 0 颗未点亮，70 数据集可用。
goal 约束解释：「不得更换 region/固定 deu」—— D0 仍是 DEU 分区，goal 文本未限定 delay；「数据集全面扫描」指 DEU 全部数据集。
按此解释开探针；若用户裁定 delay0 越界，损失仅 1 条探针波配额。

探针 10 条（每数据集 1-2 字段，level + 反向借券费率）：
| # | dataset | field | 结构 |
|---|---|---|---|
| 1 | model216 | mdl216_preferredblendedrevisionfy1percent (uc15) | level sub |
| 2 | model216 | mdl216_armglobalcombinationscore (uc7) | level ind |
| 3 | analyst44 | anl44_eps_value / anl44_eps_prevalue | 修正比率 sub |
| 4 | analyst44 | latest_quarter_end_bps (uc16, MATRIX) | level ind |
| 5 | analyst44 | anl44_roe_value / prevalue | 修正比率 sub |
| 6 | fund_holdings_panel | stable_boundary_trade_count_21d_active (uc8) | level sub |
| 7 | fund_holdings_panel | boundary_transaction_total_active | delta66 ind |
| 8 | sentiment7 | snt7_views | level sub（D0 注意力对照） |
| 9 | shortinterest3 | shrt3_bar 反向 | level sub（self 风险对照 xArzm3Mn） |
| 10 | risk60 | lending_fee_bid_rate 反向 | level sub（借费 D0） |

设置：DEU/TOP500/**delay0**/decay4/SUBINDUSTRY/trunc0.08/nanON。preflight valid=true unknown=[]。
AN 仍卡 0.1。
---

## Wave AY 判决（DEU D0 探针首波，sim 1eVz5dRo53iaQO88TwXKfr，10/10 COMPLETE）

| # | dataset | 模板 | alpha | S | 2Y | sub | 判定 |
|---|---|---|---|---:|---:|---:|---|
| 1 | model216 | blend revision FY1 | O0AldwGY | 0.90 | -0.68 | 0.70 | 活（旧强新弱） |
| 2 | shortinterest3 | −shrt3_bar D0 | kqNzpkV6 | 0.85 | 1.82 | 0.57 | ★活（新强，**self=0.0**） |
| 3 | model216 | ARM combo | P0okLrGw | 0.80 | -0.90 | 0.62 | 活（旧强） |
| 4 | fund_holdings_panel | stable boundary 21d | N1NYEW78 | 0.73 | 1.75 | 0.63 | ★活（新强） |
| 5 | fund_holdings_panel | boundary delta | d5WNJ8Og | 0.50 | 1.07 | 0.80 | 边缘（TO 0.42 高） |
| 6 | risk60 | −lending fee | vR1W7nra | 0.42 | 0.63 | 0.20 | 弱 |
| 7 | analyst44 | EPS 修正比率 | npvLGkNa | 0.41 | -0.47 | 0.04 | 弱 |
| 8 | sentiment7 | snt7_views | 6Xd56PrK | 0.40 | 0.64 | -0.31 | 弱（与 D1 一致） |
| 9 | analyst44 | qend_bps | O0Aldw7Y | -0.14 | — | — | 死 |
| 10 | analyst44 | ROE 修正比率 | rKRZa6jo | -0.17 | — | — | 死 |

### D0 关键发现
1. **D0 分区去相关实锤**：shrt3_bar D0 探针对 OS 池（全 D1）self-corr = **0.0** —— D0 与 D1 PnL 几乎正交，D1 已提交件不阻断 D0 同数据集新席位。
2. **D1 判死不传导确认**：fund_holdings_panel D1 死（S≤0.37），D0 的 boundary transaction 流字段活（0.73/2Y1.75）—— 同 id 不同 delay 是不同信号。
3. shrt3 借券反转机制在 D0 复现（0.85/2Y1.82）—— 机制跨 delay 稳健。
4. model216 修订动量族活但旧强新弱（2Y -0.68/-0.90）—— 需要新强几何（delta/quantile）改造。
5. analyst44 修正比率探针弱 —— 319 字段只测了 3 个读数面，暂不判死，列后备。
---

## Wave AZ dispatch（D0 深探第 2 波，sim 28LP8Hd9t4hmawXw6KxU8BP）2026-11-10 16:25
聚焦 AY 三活族的变化/quantile 几何（新强优先）：shrt3 D0 ×3（delta66 / quantile-IR(delta) / tvr_decay 双窗）、fhp ×4（stable bnd delta / large trade / herfindahl 反向 / value score）、m216 ×3（quantile-IR / ARM delta / zscore504）。设置同 AY（delay0）。preflight valid=true。
---

## Wave AZ 判决（D0 深探第 2 波，sim 28LP8Hd9t4hmawXw6KxU8BP，10/10 COMPLETE）

| # | 模板 | alpha | S | F | 2Y | TO | lc | sub |
|---|---|---|---:|---:|---:|---:|---:|---:|
| AZ3 | shrt3 tvr_decay 双窗 | e75XMGaM | **1.62** | **1.25** | **1.81** | 0.034 | 168 | 0.61 |
| AZ10 | m216 zscore504 | npvLGqe3 | 0.68 | 0.34 | -0.80 | 0.037 | 138 | 0.44 |
| AZ4 | fhp stable delta | j2YqkGVQ | 0.58 | 0.16 | 1.09 | 0.415 | 155 | 0.92 |
| AZ8 | m216 quantile-IR | 9qxN5M82 | 0.53 | 0.24 | -0.29 | 0.083 | 136 | 0.53 |
| AZ5 | fhp large trade | rKRZaG0d | 0.51 | 0.26 | 1.51 | 0.059 | 137 | 0.56 |
| AZ9 | m216 ARM delta | 58EPK5Ao | 0.44 | 0.18 | -0.04 | 0.082 | 130 | 1.14 |
| AZ6 | fhp −herfindahl | wpQ07G3x | 0.14 | — | — | — | 153 | — |
| AZ7 | fhp value score | vR1W7GZd | -0.09 | — | — | — | 145 | — |
| AZ2 | shrt3 quantile-IR | rKRZaG7d | -0.61 | — | — | — | 124 | — |
| AZ1 | shrt3 delta66 | RREGxze0 | -0.93 | — | — | — | 137 | — |

**AZ3 = D0 借券反转四闸通过候选**（S1.62≥1.58 / F1.25 / 2Y1.81 / TO0.034，probe self=0.0）。

## ★★ D0 方向冻结（用户指令 2026-11-10「先不考虑D0,记住没有」）
- 本波 AZ 为冻结前最后一波（派发时已在飞，不可撤，收割仅为落账止损）；
- AZ3 候选**落账备查但不追投**（不跑 prod/self 终验、不做稳健性、不提交）；
- 已存 User Memory：任何区域开波只走 delay=1，未来开采 D0 必须先获用户明确指令；
- D0 全部工作（AY/AZ 两波 20 条）到此为止。
