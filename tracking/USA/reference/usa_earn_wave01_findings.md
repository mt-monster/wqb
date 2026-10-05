# USA EARNINGS/INSTITUTIONS 塔首轮挖掘发现（2026-10-01）

## 目标与背景
- 用户指令：转向 USA 挖掘，目标累积 10 颗可提交 REGULAR alpha。
- USA D1 ACTIVE 塔状态（平台实测）：FUNDAMENTAL 5 / MODEL 4 / PV 3 / OTHER 3 已亮；
  **EARNINGS 2（差 1 颗）/ INSTITUTIONS 1（差 2 颗）**；其余 11 塔全 0。
- 首轮选定 EARNINGS + INSTITUTIONS 塔（点亮性价比最高）。

## 回测结果（USA / TOP3000 / D1 / decay5 / SUBINDUSTRY / trunc0.08）

### 骨架有效性对比（同一信号，不同骨架）
信号 = `subtract(prob_quantile_5_bucket_4_20day_return, prob_quantile_5_bucket_0_20day_return)`（earnings_chart_dl 5分位20天顶-底概率差）

| 骨架 | 候选 | S | F | 2Y | 结论 |
|---|---|---|---|---|---|
| `ts_decay_linear(signed_power(subtract(group_rank(X, subindustry), 0.5), 5), 90)` | a5 | **1.46** | **1.17** | 2.18 | ★最优 |
| `ts_decay_linear(signed_power(subtract(group_rank(X, subindustry), 0.5), 5), 90)`（4分位10天） | a7 | **1.46** | **1.17** | 2.19 | ★最优 |
| `ts_decay_linear(...subindustry...)`（同骨架） | a2 | 1.38 | 1.06 | 2.03 | 优 |
| `signed_power(ts_rank(group_rank(X, market), 504), 0.5)` | a1 | 0.51 | 0.11 | -0.43 | ✗失效 |
| `signed_power(ts_rank(group_rank(X, market), 504), 0.5)` | a4/a6 | 0.34/0.46 | — | ✗ | ✗失效 |
| `group_rank(ts_zscore(ts_backfill(X,252), 252), industry)` | a3 | 0.58 | 0.13 | -0.26 | ✗失效 |
| 连续回归预测 `quantile_1_assignment_*` | a8/a9/a10 | 0.10/1.01/0.15 | — | — | 弱/不稳 |

### ★★★ 核心结论：USA 骨架与 KOR 相反
- **USA 有效骨架 = `ts_decay_linear(signed_power(subtract(group_rank(X, subindustry), 0.5), PW), DEC)`**（subindustry 内归一化 + signed_power 压尾 + 长 decay）。
- **USA 失效骨架 = `signed_power(ts_rank(group_rank(X, market), 504), 0.5)`**（market 级 ts_rank）——
  而后者在 **KOR 是王牌骨架**（zq87zzqO/wpZkk1Mp/A1NXddRw 全用它）。
- **机理**：USA 是成熟大市场，横截面预期收益的 alpha 更多来自**子行业内相对定位**（同行比较），
  market 级排名被行业 beta 噪声淹没；KOR 市场小、行业结构弱，market 级排名更有效。
- **迁移警示**：KOR 的 win skeleton 不可直接搬到 USA（反之亦然）。

### INSTITUTIONS 塔（fund_holdings_panel，全 VECTOR）
| 候选 | 信号 | S | F | 2Y |
|---|---|---|---|---|
| inst_a2 | `boundary_transaction_usd_value_active`（边界交易额）| **1.28** | **1.08** | 2.06 |
| inst_a1 | `herfindahl_index_holdings_active`（持仓集中度 HHI）| 0.25 | 0.06 | 0.25 |

→ 同骨架（subindustry）有效；**边界交易额** 比 **持仓集中度** 更有信号。

### 跨集价差（已声明）表现
| 候选 | 组合 | S | F |
|---|---|---|---|
| earn_b2 | earnings_chart_dl × fund_holdings_panel | 0.74 | 0.46 |
| ern03_a1 | earnings6 实际-预期 EPS 价差 | -0.98 | -0.51 |
| ern03_a3 | 同上 ts_zscore 版 | 0.44 | 0.17 |

→ **跨集价差首轮偏弱**（<1.0）；earnings6 实际vs预期 EPS 价差**方向可能相反**（-0.98 提示反向更强）。

## 距提交门槛的差距
- 门槛：S ≥ 1.58 ∧ F ≥ 1.0 ∧ 2Y ≥ 1.58 ∧ SUB ≥ 0.571×S。
- **最强 a5/a7：S=1.46（差 0.12）F=1.17 ✓ 2Y=2.18 ✓ SUB=0.81**。
  - SUB 比值要求 0.571×1.58=0.90；当前 0.81 → **SUB 是提升后需同步关注的卡点**。
  - 换手仅 0.06 → 有提升空间（缩短 decay 提高响应可换 Sharpe）。

## 提升批（up01，22 条，已启动）
围绕 a5/a7 骨架扫参：
- group 轴：subindustry / industry / sector
- signed_power 指数：0.35 / 0.4 / 0.5 / 0.6 / 0.7
- decay：66 / 90 / 120 / 150 / 252
期望：把 S 从 1.46 推到 ≥1.58 且 SUB 同步 ≥0.90。
