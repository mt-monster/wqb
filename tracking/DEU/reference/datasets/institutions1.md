# institutions1 字段画像（DEU / TOP500 / D1）

> 建档 2026-11-23。数据源 `mcp__wq-brain-http__get_datafields(region=DEU, universe=TOP500, delay=1, dataset_id="institutions1", filter_sharpe=false)`；
> 平台实返 `count=7 / platform_count=7 / complete=true`。归档：`tracking/DEU/reference/datasets/institutions1.md`。

## 0. 数据集级

| 项 | 值 |
|---|---|
| name | Insider Trading for Europe（30+ 欧洲国家内部人交易；平台 category=institutions） |
| category | institutions（`INSTITUTIONS`，×1.6） |
| coverage（集级） | 0.2289（字段级同 0.2289） |
| fieldCount | 7（全 VECTOR） |
| userCount / alphaCount | 24 / 37 |
| valueScore | 5.0 |
| 十年跨度 | ❌ `E56AzejK` 2014–2017 LC/SC/pnl 全 0（2026-11-17 实读）⇒ 用户十年硬约束排除 |

## 1. 字段全表（7/7）

| # | field id | type | coverage | alphaCount | 语义 |
|---|---|---|---:|---:|---|
| 1 | `inst1_holdings` | VECTOR | 0.2289 | 19 | 交易后内部人持有股数/权益单位 |
| 2 | `inst1_price` | VECTOR | 0.2289 | 1 | 成交价（区间取最低） |
| 3 | `inst1_shares` | VECTOR | 0.2289 | 2 | 交易股数/权益单位 |
| 4 | `inst1_tradesignificance` | VECTOR | 0.2289 | 7 | 交易重要性 1–3（3=高） |
| 5 | `inst1_value` | VECTOR | 0.2289 | 3 | 交易金额（原币） |
| 6 | `inst1_valueeur` | VECTOR | 0.2289 | 19 | 交易金额（欧元） |
| 7 | `transaction_currency_code_2` | VECTOR | 0.2289 | 0 | 币种 ISO 三字母（元数据，不可作信号） |

### 实测读数表（平台 `get_datafields` 逐字段实读）

| field | type | coverage | alphaCount |
|---|---|---|---:|
| `inst1_holdings` | VECTOR | 0.2289 | 19 |
| `inst1_price` | VECTOR | 0.2289 | 1 |
| `inst1_shares` | VECTOR | 0.2289 | 2 |
| `inst1_tradesignificance` | VECTOR | 0.2289 | 7 |
| `inst1_value` | VECTOR | 0.2289 | 3 |
| `inst1_valueeur` | VECTOR | 0.2289 | 19 |
| `transaction_currency_code_2` | VECTOR | 0.2289 | 0 |

## 2. 结论

- **不投**：十年跨度只 2019–2023（2014–2017 全零），且 2026-09-23 探针判弱（DEU-INSTITUTIONS1-PROBE-DEAD-20260923：欧洲内部人事件流在 TOP500/D1 方向为负、实测 0.32–0.44）。
- 与 `insiders1` / `insider_agg_matrix`（INSIDERS 塔）不同数据集；本集计入 `INSTITUTIONS` 塔但不满足十年线。
