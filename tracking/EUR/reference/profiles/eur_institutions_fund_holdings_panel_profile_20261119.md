# EUR / D1 / TOP2500 — institutions · fund_holdings_panel 全字段画像（2026-11-19）

> 范围：EUR region、delay 1、universe TOP2500。
> 口径：**全字段探测，禁止抽样**——字段全表 = 平台 `get_datafields(filter_sharpe=false)` 返回的全量 30 字段（`complete=true`，`platform_count=30`，`returned=30`）。
> 数据源：`mcp__wq-brain-http__get_datafields`，2026-11-19 实拉。原始目录 `tracking/EUR/reference/eur_fund_holdings_panel_fields.json`。

## 1. 数据集概览

| 项 | 值 |
|---|---|
| dataset id | `fund_holdings_panel` |
| 名称 | Global Institutional Fund Holdings |
| category | institutions（EUR/D1 塔位 **0/3**，完全未点亮） |
| 字段数 | 30（**全部 VECTOR**） |
| 平台覆盖率 | 0.8805 |
| userCount / alphaCount | 403 / 922 |
| pyramidMultiplier | 1.1 |

**★ 结构性事实：30 = 15 个基读数 × 2 套口径**

每个基字段都有一对：`<name>` 与 `<name>_active`。两者语义相同、口径不同（`_active` 覆盖率低 5–7pp，通常 aC 更低=更冷门）：

| 口径 | 覆盖率区间 | 字段数 |
|---|---|---:|
| 基字段（无后缀） | 0.9083 – 0.9183 | 15 |
| `_active` 变体 | 0.8430 – 0.8570 | 15 |

⇒ **有效独立信息只有 15 个基读数**，另 15 个是同源变体。ATOM 挖掘时每对只能取一席（同族互相关极高）。

**⚠ 覆盖率漂移记录**：2026-11-16 本地缓存里同一数据集基字段 coverage 记为 **1.0**、`boundary_transaction_total` 的 aC 为 171；本次实拉为 **0.9083**、aC 77。
口径差异来自 universe 不同（旧缓存非 TOP2500）。**本档案以本次 TOP2500 实拉为准**，旧缓存不得引用。

## 2. 字段全表

> 本节是分母：逐字段列出真实 id，无通配、无「同构孪生」省略。

| 字段 | 类型 | 覆盖率 | userCount | alphaCount | 语义族 | 形态 | 模板方向 |
|---|---|---:|---:|---:|---|---|---|
| `boundary_transaction_total` | VECTOR | 0.9083 | 55 | 77 | 建仓/清仓事件 | count_flow | 流量÷存量：ts_sum(·,63)/ts_mean(holder_account_total,63) |
| `boundary_transaction_total_active` | VECTOR | 0.843 | 47 | 65 | 建仓/清仓事件（_active 变体） | count_flow | 流量÷存量：ts_sum(·,63)/ts_mean(holder_account_total,63) |
| `boundary_transaction_usd_value` | VECTOR | 0.9083 | 15 | 18 | 建仓/清仓金额 | level_amount | 金额需 rank/log 压缩后时序化 |
| `boundary_transaction_usd_value_active` | VECTOR | 0.843 | 12 | 14 | 建仓/清仓金额（_active 变体） | level_amount | 金额需 rank/log 压缩后时序化 |
| `herfindahl_index_holdings` | VECTOR | 0.9183 | 77 | 105 | 持仓集中度 HHI | bounded_dense | 有界 0–1，ts_zscore 直接可用 |
| `herfindahl_index_holdings_active` | VECTOR | 0.857 | 51 | 67 | 持仓集中度 HHI（_active 变体） | bounded_dense | 有界 0–1，ts_zscore 直接可用 |
| `herfindahl_index_transactions` | VECTOR | 0.9083 | 9 | 11 | 交易集中度 HHI | bounded_dense | 有界 0–1，ts_zscore 直接可用 |
| `herfindahl_index_transactions_active` | VECTOR | 0.843 | 8 | 9 | 交易集中度 HHI（_active 变体） | bounded_dense | 有界 0–1，ts_zscore 直接可用 |
| `holder_account_total` | VECTOR | 0.9183 | 83 | 126 | 持有人数（存量） | level_amount | 存量分母；可作 breadth 水平或流量分母 |
| `holder_account_total_active` | VECTOR | 0.857 | 22 | 26 | 持有人数（存量）（_active 变体） | level_amount | 存量分母；可作 breadth 水平或流量分母 |
| `holding_value_distribution_score` | VECTOR | 0.9183 | 58 | 80 | 持仓价值分布（拥挤度） | bounded_dense | 有界拥挤度指标 |
| `holding_value_distribution_score_active` | VECTOR | 0.857 | 44 | 53 | 持仓价值分布（拥挤度）（_active 变体） | bounded_dense | 有界拥挤度指标 |
| `large_trade_count_50bps` | VECTOR | 0.9083 | 6 | 8 | 大额交易计数 | count_flow | 稀疏计数，需长窗求和 |
| `large_trade_count_50bps_active` | VECTOR | 0.843 | 7 | 7 | 大额交易计数（_active 变体） | count_flow | 稀疏计数，需长窗求和 |
| `mean_security_weight` | VECTOR | 0.9183 | 5 | 6 | 平均持仓权重 | bounded_dense | 占 AUM 比例，有界 |
| `mean_security_weight_active` | VECTOR | 0.857 | 4 | 5 | 平均持仓权重（_active 变体） | bounded_dense | 占 AUM 比例，有界 |
| `security_holding_usd_value` | VECTOR | 0.9183 | 67 | 105 | 持仓市值（存量） | level_amount | 金额存量，需压缩 |
| `security_holding_usd_value_active` | VECTOR | 0.857 | 33 | 45 | 持仓市值（存量）（_active 变体） | level_amount | 金额存量，需压缩 |
| `security_transaction_usd_value` | VECTOR | 0.9083 | 32 | 45 | 交易市值（流量） | level_amount | 金额流量 |
| `security_transaction_usd_value_active` | VECTOR | 0.843 | 6 | 7 | 交易市值（流量）（_active 变体） | level_amount | 金额流量 |
| `stable_boundary_trade_count_21d` | VECTOR | 0.9083 | 64 | 100 | 稳定建仓计数（21日无反复） | count_flow | 高质量事件计数，首选读数 |
| `stable_boundary_trade_count_21d_active` | VECTOR | 0.843 | 68 | 99 | 稳定建仓计数（21日无反复）（_active 变体） | count_flow | 高质量事件计数，首选读数 |
| `top_weighted_account_number` | VECTOR | 0.9183 | 10 | 11 | 重仓账户数（conviction） | count_flow | 信念持仓账户数 |
| `top_weighted_account_number_active` | VECTOR | 0.857 | 15 | 16 | 重仓账户数（conviction）（_active 变体） | count_flow | 信念持仓账户数 |
| `top_weighted_transaction_number` | VECTOR | 0.9083 | 7 | 7 | 重仓交易数 | count_flow | 信念持仓上的交易 |
| `top_weighted_transaction_number_active` | VECTOR | 0.843 | 1 | 0 | 重仓交易数（_active 变体） | count_flow | 信念持仓上的交易 |
| `transaction_account_total` | VECTOR | 0.9083 | 16 | 24 | 交易账户数 | count_flow | 参与账户广度 |
| `transaction_account_total_active` | VECTOR | 0.843 | 8 | 9 | 交易账户数（_active 变体） | count_flow | 参与账户广度 |
| `transaction_value_distribution_score` | VECTOR | 0.9083 | 16 | 16 | 交易价值分布 | bounded_dense | 有界 0–1 |
| `transaction_value_distribution_score_active` | VECTOR | 0.843 | 12 | 12 | 交易价值分布（_active 变体） | bounded_dense | 有界 0–1 |

## 3. 逐字段画像（更新频率 / 分布形态 / 可用性）

| 字段 | 更新频率 | 分布形态 | 可用性判定 |
|---|---|---|---|
| `boundary_transaction_total` | 日频（事件计数） | 非负整数，零膨胀 | 流量族：ts_sum 长窗 / 流量÷存量 |
| `boundary_transaction_total_active` | 日频（事件计数） | 非负整数，零膨胀 | 流量族：ts_sum 长窗 / 流量÷存量；_active 口径，与基字段同源只取一 |
| `boundary_transaction_usd_value` | 日频（金额/存量快照） | 右偏重尾，量纲跨股票不可比 | 需先 rank/log 压缩再时序化 |
| `boundary_transaction_usd_value_active` | 日频（金额/存量快照） | 右偏重尾，量纲跨股票不可比 | 需先 rank/log 压缩再时序化；_active 口径，与基字段同源只取一 |
| `herfindahl_index_holdings` | 日频（持仓快照） | 有界 [0,1]，稠密，连续 | **首选**：有界稠密 → ts_zscore 稳定有效 |
| `herfindahl_index_holdings_active` | 日频（持仓快照） | 有界 [0,1]，稠密，连续 | **首选**：有界稠密 → ts_zscore 稳定有效；_active 口径，与基字段同源只取一 |
| `herfindahl_index_transactions` | 日频（持仓快照） | 有界 [0,1]，稠密，连续 | **首选**：有界稠密 → ts_zscore 稳定有效 |
| `herfindahl_index_transactions_active` | 日频（持仓快照） | 有界 [0,1]，稠密，连续 | **首选**：有界稠密 → ts_zscore 稳定有效；_active 口径，与基字段同源只取一 |
| `holder_account_total` | 日频（金额/存量快照） | 右偏重尾，量纲跨股票不可比 | 需先 rank/log 压缩再时序化 |
| `holder_account_total_active` | 日频（金额/存量快照） | 右偏重尾，量纲跨股票不可比 | 需先 rank/log 压缩再时序化；_active 口径，与基字段同源只取一 |
| `holding_value_distribution_score` | 日频（持仓快照） | 有界 [0,1]，稠密，连续 | **首选**：有界稠密 → ts_zscore 稳定有效 |
| `holding_value_distribution_score_active` | 日频（持仓快照） | 有界 [0,1]，稠密，连续 | **首选**：有界稠密 → ts_zscore 稳定有效；_active 口径，与基字段同源只取一 |
| `large_trade_count_50bps` | 日频（事件计数） | 非负整数，零膨胀 | 流量族：ts_sum 长窗 / 流量÷存量 |
| `large_trade_count_50bps_active` | 日频（事件计数） | 非负整数，零膨胀 | 流量族：ts_sum 长窗 / 流量÷存量；_active 口径，与基字段同源只取一 |
| `mean_security_weight` | 日频（持仓快照） | 有界 [0,1]，稠密，连续 | **首选**：有界稠密 → ts_zscore 稳定有效 |
| `mean_security_weight_active` | 日频（持仓快照） | 有界 [0,1]，稠密，连续 | **首选**：有界稠密 → ts_zscore 稳定有效；_active 口径，与基字段同源只取一 |
| `security_holding_usd_value` | 日频（金额/存量快照） | 右偏重尾，量纲跨股票不可比 | 需先 rank/log 压缩再时序化 |
| `security_holding_usd_value_active` | 日频（金额/存量快照） | 右偏重尾，量纲跨股票不可比 | 需先 rank/log 压缩再时序化；_active 口径，与基字段同源只取一 |
| `security_transaction_usd_value` | 日频（金额/存量快照） | 右偏重尾，量纲跨股票不可比 | 需先 rank/log 压缩再时序化 |
| `security_transaction_usd_value_active` | 日频（金额/存量快照） | 右偏重尾，量纲跨股票不可比 | 需先 rank/log 压缩再时序化；_active 口径，与基字段同源只取一 |
| `stable_boundary_trade_count_21d` | 日频（事件计数） | 非负整数，零膨胀 | 流量族：ts_sum 长窗 / 流量÷存量 |
| `stable_boundary_trade_count_21d_active` | 日频（事件计数） | 非负整数，零膨胀 | 流量族：ts_sum 长窗 / 流量÷存量；_active 口径，与基字段同源只取一 |
| `top_weighted_account_number` | 日频（事件计数） | 非负整数，零膨胀 | 流量族：ts_sum 长窗 / 流量÷存量 |
| `top_weighted_account_number_active` | 日频（事件计数） | 非负整数，零膨胀 | 流量族：ts_sum 长窗 / 流量÷存量；_active 口径，与基字段同源只取一 |
| `top_weighted_transaction_number` | 日频（事件计数） | 非负整数，零膨胀 | 流量族：ts_sum 长窗 / 流量÷存量 |
| `top_weighted_transaction_number_active` | 日频（事件计数） | 非负整数，零膨胀 | 流量族：ts_sum 长窗 / 流量÷存量；_active 口径，与基字段同源只取一 |
| `transaction_account_total` | 日频（事件计数） | 非负整数，零膨胀 | 流量族：ts_sum 长窗 / 流量÷存量 |
| `transaction_account_total_active` | 日频（事件计数） | 非负整数，零膨胀 | 流量族：ts_sum 长窗 / 流量÷存量；_active 口径，与基字段同源只取一 |
| `transaction_value_distribution_score` | 日频（持仓快照） | 有界 [0,1]，稠密，连续 | **首选**：有界稠密 → ts_zscore 稳定有效 |
| `transaction_value_distribution_score_active` | 日频（持仓快照） | 有界 [0,1]，稠密，连续 | **首选**：有界稠密 → ts_zscore 稳定有效；_active 口径，与基字段同源只取一 |

## 4. 形态聚类（决定算子族，本档案核心）

| 形态 | 基读数字段数 | 含 _active 合计 | 对应算子族 | 代表字段 |
|---|---:|---:|---|---|
| count_flow | 6 | 12 | `ts_sum(F,63)` 长窗累加；或 流量÷存量 归一 | `boundary_transaction_total`、`boundary_transaction_total_active`、`large_trade_count_50bps` |
| bounded_dense | 5 | 10 | `ts_zscore(ts_backfill(F,60),250)` / `ts_quantile` | `herfindahl_index_holdings`、`herfindahl_index_holdings_active`、`herfindahl_index_transactions` |
| level_amount | 4 | 8 | `rank(F)` 或 `log` 压缩后再 `ts_delta`/`ts_zscore` | `boundary_transaction_usd_value`、`boundary_transaction_usd_value_active`、`holder_account_total` |

## 5. VECTOR 处理契约

```
vec_avg(<field>)   # 均值：本集全部字段的唯一自然口径
vec_sum(<field>)   # 计数/金额族可用
```
- 30 字段**全部 VECTOR**，裸写字段名会整批语法失败，必须 `vec_*` 包裹。
- 覆盖率 0.843–0.918 意味着非持仓日为空，`ts_backfill` 是必需前置。

## 6. 可用性分层

| 层级 | 判定 | 字段 |
|---|---|---|
| L1 首选 | 有界稠密，算子族明确 | `herfindahl_index_holdings`、`herfindahl_index_transactions`、`holding_value_distribution_score`、`mean_security_weight`、`transaction_value_distribution_score` |
| L2 流量族 | 计数，需长窗或归一 | `stable_boundary_trade_count_21d`、`boundary_transaction_total`、`large_trade_count_50bps`、`top_weighted_account_number`、`top_weighted_transaction_number`、`transaction_account_total` |
| L3 量纲族 | 金额/存量，需压缩 | `security_holding_usd_value`、`security_transaction_usd_value`、`boundary_transaction_usd_value`、`holder_account_total` |
| L4 同源变体 | `_active` 口径，每对只取一 | 全部 15 个 `*_active` |

## 7. 字段 → 候选模板白名单（静态先验，需实证裁决）

> ⚠ 这是准入先验，不是实证结论。按经验库纪律，落回测前须逐字段做六法实证裁决。
> 已内置本轮 earnings 20 臂的证伪结论：`ts_target_tvr_decay` 在低换手慢信号上零贡献；事件门控只适合短周期读数；轴加宽摧毁 sub；`group_rank(rank(x))` 是空操作；winsorize 在尾部驱动字段上负向。

| 形态 | 白名单模板 | 排除模板 | 依据 |
|---|---|---|---|
| bounded_dense | `group_rank(ts_zscore(ts_backfill(vec_avg(F),60),250), subindustry)` | 裸水平；`winsorize`；`group_rank(rank(x))` | 有界稠密读数 z-score 稳定（sent_matrix 实证 S1.90–1.93） |
| count_flow | `group_rank(ts_sum(vec_avg(F),63), subindustry)`；或 `divide(ts_sum(流量,63), ts_mean(存量,63))` | 裸计数；短窗 | 计数零膨胀，需累加；流量÷存量是 insiders1 已验证核心（DEU 70赞专帖） |
| level_amount | `group_rank(ts_delta(divide(vec_avg(F), add(abs(vec_avg(存量分母)),1)),63), subindustry)` | 裸金额跨股票 rank | 金额右偏重尾，先归一后差分 |

## 8. 已知实测读数（本地库，2026-11-19 只读查询）

见 §9 —— 本集在 EUR 的历史战果为**ATOM F-数学判死**（returns 2.33%），但那次探测存在「30 字段只探 5 个代表」的历史违例，结论不可直接沿用。

## 9. 结论与下一步

1. **可挖面**：15 个基读数，L1 有界稠密 5 个（首选）、L2 流量 6 个、L3 量纲 4 个。
2. **ATOM 合规**：单数据集，`pyramids.effective` 将为 1；VECTOR 必须 `vec_*`。
3. **历史包袱**：旧档案判「ATOM F-数学判死（returns 2.33%）」，但该结论基于抽样探测（30 字段只测 5 个），按用户 2026-11-17 硬约束不得作为判死依据 —— **必须重测**。
4. **下一步**：按 §7 白名单对 L1 的 5 个有界稠密字段各出 1–2 臂，首轮消融「形态→算子族」这一维。

---

配套闸：`python tools/gates/field_profile_completeness_gate.py --profile tracking/EUR/reference/profiles/eur_institutions_fund_holdings_panel_profile_20261119.md`
