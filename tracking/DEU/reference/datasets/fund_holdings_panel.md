# fund_holdings_panel 字段画像（DEU / TOP500 / D1）

> 建档 2026-11-23。数据源 `mcp__wq-brain-http__get_datafields(region=DEU, universe=TOP500, delay=1, dataset_id="fund_holdings_panel", filter_sharpe=false)`；
> 平台实返 `count=18 / platform_count=18 / complete=true`。归档：`tracking/DEU/reference/datasets/fund_holdings_panel.md`。

## 0. 数据集级

| 项 | 值 |
|---|---|
| name | Global Institutional Fund Holdings（账户级基金持仓/交易，日频） |
| category | institutions（`INSTITUTIONS`，×1.6） |
| coverage（集级） | 0.9019 |
| fieldCount | 18（全 VECTOR ⇒ 必须 `vec_avg` 降维） |
| userCount / alphaCount | 72 / 130 |
| valueScore | 4.0 |
| 十年跨度 | ⚠ 未取；EUR 先验为 **2015–2023 共 9 年**（数据层排除线）⇒ 本区启用前须用 `get_alpha_yearly_stats` 逐年核 2014–2023 |

## 1. 字段全表（18/18）

| # | field id | coverage | alphaCount | 语义 |
|---|---|---:|---:|---|
| 1 | `boundary_transaction_total` | 0.9278 | 29 | 全基金账户当日边界交易数（新建仓/清仓） |
| 2 | `boundary_transaction_total_active` | 0.876 | 8 | 同上（活跃口径） |
| 3 | `boundary_transaction_usd_value` | 0.9278 | 4 | 边界交易美元总额 |
| 4 | `boundary_transaction_usd_value_active` | 0.876 | 5 | 同上（活跃口径） |
| 5 | `herfindahl_index_transactions` | 0.9278 | 6 | 交易额在账户间集中度 HHI（0–1） |
| 6 | `herfindahl_index_transactions_active` | 0.876 | 0 | 同上（活跃口径） |
| 7 | `large_trade_count_50bps` | 0.9278 | 7 | 超过基金 AUM 0.5% 的大单笔数 |
| 8 | `large_trade_count_50bps_active` | 0.876 | 0 | 同上（活跃口径） |
| 9 | `security_transaction_usd_value` | 0.9278 | 10 | 证券成交美元总额 |
| 10 | `security_transaction_usd_value_active` | 0.876 | 3 | 同上（活跃口径） |
| 11 | `stable_boundary_trade_count_21d` | 0.9278 | 45 | **持久**边界交易数（账户 21 交易日内未在同证券做过边界交易） |
| 12 | `stable_boundary_trade_count_21d_active` | 0.876 | 28 | 同上（活跃口径） |
| 13 | `top_weighted_transaction_number` | 0.9278 | 2 | 信念持仓证券的交易笔数（conviction） |
| 14 | `top_weighted_transaction_number_active` | 0.876 | 2 | 同上（活跃口径） |
| 15 | `transaction_account_total` | 0.9278 | 11 | 当日交易该证券的不同账户数 |
| 16 | `transaction_account_total_active` | 0.876 | 5 | 同上（活跃口径） |
| 17 | `transaction_value_distribution_score` | 0.9278 | 5 | 交易额账户分布集中度 0–1 |
| 18 | `transaction_value_distribution_score_active` | 0.876 | 3 | 同上（活跃口径） |

### 实测读数表（平台 `get_datafields` 逐字段实读）

| field | type | coverage | alphaCount |
|---|---|---|---:|
| `boundary_transaction_total` | VECTOR | 0.9278 | 29 |
| `boundary_transaction_total_active` | VECTOR | 0.876 | 8 |
| `boundary_transaction_usd_value` | VECTOR | 0.9278 | 4 |
| `boundary_transaction_usd_value_active` | VECTOR | 0.876 | 5 |
| `herfindahl_index_transactions` | VECTOR | 0.9278 | 6 |
| `herfindahl_index_transactions_active` | VECTOR | 0.876 | 0 |
| `large_trade_count_50bps` | VECTOR | 0.9278 | 7 |
| `large_trade_count_50bps_active` | VECTOR | 0.876 | 0 |
| `security_transaction_usd_value` | VECTOR | 0.9278 | 10 |
| `security_transaction_usd_value_active` | VECTOR | 0.876 | 3 |
| `stable_boundary_trade_count_21d` | VECTOR | 0.9278 | 45 |
| `stable_boundary_trade_count_21d_active` | VECTOR | 0.876 | 28 |
| `top_weighted_transaction_number` | VECTOR | 0.9278 | 2 |
| `top_weighted_transaction_number_active` | VECTOR | 0.876 | 2 |
| `transaction_account_total` | VECTOR | 0.9278 | 11 |
| `transaction_account_total_active` | VECTOR | 0.876 | 5 |
| `transaction_value_distribution_score` | VECTOR | 0.9278 | 5 |
| `transaction_value_distribution_score_active` | VECTOR | 0.876 | 3 |

## 2. 机制聚类（3 条）

| 机制 | 字段 | 含义 |
|---|---|---|
| F1 持久信念流 | `stable_boundary_trade_count_21d`、`top_weighted_transaction_number`、`large_trade_count_50bps` | 只统计「持久/大额/信念」边界交易（比总边界流更接近 smart money） |
| F2 交易集中度 | `herfindahl_index_transactions`、`transaction_value_distribution_score`、`transaction_account_total` | 当日交易集中在少数账户（集中度越高 = 少数机构主导） |
| F3 交易强度/规模 | `boundary_transaction_total`、`boundary_transaction_usd_value`、`security_transaction_usd_value` | 边界交易规模与总交易额 |

## 3. 历史与可用性

- 本地 `get_mining_yield`（2026-11-17 前）：**94 backtested / 0 ra_clean**（conv 0.743）；`DEU-FHP-ALLGATE-CLOSED` / `DEU-FHP-SCEILING-DEAD` 为旧档研究级结论（无六维判死档案）。
- 2026-11-21 5 层 53 臂梯度终态（`gradient-mandatory-and-imb5-2layer-20261121`）：**天花板 S0.70**（距 S 闸 0.88）；L4 `group_scale` +0.21 / L5 decay8 +0.17；数据窗口 2015–2023。
- ⇒ 本区**不优先**：十年跨度风险 + 单一 ATOM 强度 0.70。若启用，只作「F1 持久信念流 × 搭档腿」的跨集组合，且必须先验 2014 年持仓。

## 4. 类型/禁用

- 全 VECTOR：必须 `vec_avg`（或 `vec_max`）；`*_active` 是子集口径，不得与全集混算。
- 数据自 2015 起（EUR 先验）⇒ **2014 零持仓 = 用户十年硬约束排除**，启用前必须 `get_alpha_yearly_stats`。
