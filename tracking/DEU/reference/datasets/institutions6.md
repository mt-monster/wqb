# institutions6 字段画像（DEU / TOP500 / D1）

> 建档 2026-11-23。数据源 `mcp__wq-brain-http__get_datafields(region=DEU, universe=TOP500, delay=1, dataset_id="institutions6", filter_sharpe=false)`；
> 平台实返 `count=11 / platform_count=11 / complete=true / pages_fetched=1`。归档路径规则：`tracking/<REGION>/reference/datasets/<dataset_id>.md`。

## 0. 数据集级

| 项 | 值 |
|---|---|
| name | Institutions and Beneficial Stake Ownership |
| category | institutions（DEU/D1 塔 `INSTITUTIONS`，×1.6；当前 1/3） |
| coverage（集级） | 1.0 |
| fieldCount | 11（全 MATRIX） |
| userCount / alphaCount | 145 / 309 |
| valueScore | 3.0 |
| 更新频率 | 季频（报告期快照；repo 先验 + DEU 实测 TO 1.5–10.3% 一致，平台未直接返回频率） |
| 十年跨度 | ✅ `1YWaRlJm`（2026-11-17 实读）2014–2023 逐年 LC/SC>0；本批继承该口径 |

## 1. 字段全表（11/11，逐字段实测）

| # | field id | type | coverage | userCount | alphaCount | 语义 |
|---|---|---|---:|---:|---:|---|
| 1 | `aggregate_equity_value_all_owners` | MATRIX | 1.0 | 18 | 20 | 全体持有人（父子去重）持有市值合计 |
| 2 | `aggregate_equity_value_institutions` | MATRIX | 1.0 | 22 | 28 | 报告期末机构持有市值合计 |
| 3 | `aggregate_share_count_all_owners` | MATRIX | 1.0 | 16 | 23 | 全体持有人持股数合计（≈总股本代理） |
| 4 | `aggregate_share_count_institutions` | MATRIX | 1.0 | 19 | 24 | 报告期末机构持股数合计 |
| 5 | `count_institutional_buyers_security` | MATRIX | 1.0 | 46 | 65 | 报告期内买入机构家数 |
| 6 | `count_institutional_holders_security` | MATRIX | 1.0 | 22 | 34 | 报告期末持股>0 的机构家数 |
| 7 | `count_institutional_sellers_security` | MATRIX | 1.0 | 38 | 54 | 报告期内卖出机构家数 |
| 8 | `market_value_institutional_shares_acquired` | MATRIX | 1.0 | 57 | 93 | 报告期内机构买入金额 |
| 9 | `market_value_institutional_shares_disposed` | MATRIX | 1.0 | 25 | 43 | 报告期内机构卖出金额 |
| 10 | `quantity_institutional_shares_acquired` | MATRIX | 1.0 | 50 | 69 | 报告期内机构买入股数 |
| 11 | `quantity_institutional_shares_disposed` | MATRIX | 1.0 | 28 | 40 | 报告期内机构卖出股数 |

类型纪律：**11/11 全 MATRIX**，**不得**包 `vec_avg`（会静默失败/None）；无 VECTOR/GROUP/EVENT；D0（delay=0）无此数据集。

### 实测读数表（平台 `get_datafields` 逐字段实读）

| field | type | coverage | userCount | alphaCount |
|---|---|---|---:|---:|
| `aggregate_equity_value_all_owners` | MATRIX | 1.0 | 18 | 20 |
| `aggregate_equity_value_institutions` | MATRIX | 1.0 | 22 | 28 |
| `aggregate_share_count_all_owners` | MATRIX | 1.0 | 16 | 23 |
| `aggregate_share_count_institutions` | MATRIX | 1.0 | 19 | 24 |
| `count_institutional_buyers_security` | MATRIX | 1.0 | 46 | 65 |
| `count_institutional_holders_security` | MATRIX | 1.0 | 22 | 34 |
| `count_institutional_sellers_security` | MATRIX | 1.0 | 38 | 54 |
| `market_value_institutional_shares_acquired` | MATRIX | 1.0 | 57 | 93 |
| `market_value_institutional_shares_disposed` | MATRIX | 1.0 | 25 | 43 |
| `quantity_institutional_shares_acquired` | MATRIX | 1.0 | 50 | 69 |
| `quantity_institutional_shares_disposed` | MATRIX | 1.0 | 28 | 40 |

## 2. 机制聚类（5 条，全部字段覆盖）

| 机制 | 字段 | 经济含义 | 文献锚 |
|---|---|---|---|
| M1 参与广度共识 | buyers − sellers，分母 holders | 多家机构同向买入 = 共识/羊群宽度 | Chen-Hong-Stein (2002) breadth of ownership；SSRN 1663723 |
| M2 净买入强度（金额口径） | market_value acq − dis，分母 aggregate_equity_value_institutions | 机构净流入占持仓市值比例 | 13F flow 文献；SSRN 3439729 |
| M3 机构渗透率水平 | share_count_institutions / share_count_all_owners | 机构化程度（neglected-firm 溢价） | Institutional ownership & long-term returns (2003) |
| M4 渗透率趋势 | ts_delta(M3, 252) | 机构化漂移/稳定资金流入 | Ownership breadth & stock returns (2010) |
| M5 换手/短线资金占比 | (qty acq + qty dis) / ts_mean(share_institutions,252) | 高 churn = 短线资金主导 | Short-term institutional trades: smart money or overconfidence (2011) |

## 3. 模板族（结构与方向）

| 族 | 骨架 | 预期符号 | 状态 |
|---|---|---|---|
| H 水平 | `group_rank(divide(share_inst, share_all), sector)` | −（低配溢价） | 2026-11-23 本批测 |
| D 差分 | `group_rank(ts_delta(divide(share_inst, share_all), 252), sector)` | + | 本批测 |
| B 广度 | `group_rank(ts_mean(divide(buyers−sellers, holders), 66), sector)` | + | 历史 best S0.71（QPvrZxPM, ts_zscore252）；本批变体测 |
| F 净流 | `group_rank(ts_mean(divide(mv_acq−mv_dis, eq_value_inst), 66), sector)` | + | 本批测 |
| T 换手 | `−group_rank(ts_mean(divide(qty_acq+qty_dis, ts_mean(share_inst,252)), 66), sector)` | − | 本批测 |
| C 条件反转 | `trade_when(ts_zscore(B,126)>1.5, −rank(ts_zscore(B,126)), 0)` | − | 未测（候选） |
| G 门控 | `trade_when(渗透率高, 主信号, −1)` | 视主信号 | 未测（候选） |
| X 组合 | 本集多腿 `add(B,F,H)`（同集 add 合法） | + | 本批测 |

## 4. 历史读数（只读，非本批）

- 2026-09-13 裸探针 8 条：`rank(buyers)` S0.36/2Y0.86；`rank(mv_acq−mv_dis)` S0.31/2Y1.01；`rank(qty_acq−qty_dis)` S0.31/2Y1.21；全 FAIL。
- 2026-10-30 结构式 10 条：最佳 `QPvrZxPM` `group_neutralize(ts_zscore((buyers−sellers)/holders,252), subindustry)` **S0.71/F0.40/2Y0.58/SUB0.53/TO8.4%**；其余 −0.44~0.36。
- 2026-11-17 配对形 `1YWaRlJm`（bucket-only 第二数据集）S0.82/sub0.21/4 项 RA fail ⇒ 只作分组轴，不可作主信号。
- ⇒ 本集 ATOM 单信号天花板约 0.7–0.8（PROVISIONAL，D1/D6 未穷尽）；跨集搭档（gating/grouping/residual/ratio 或本报告口径的 2-category 组合）是唯一可能到 1.58 的路径。

## 5. 本批设计（2026-11-23）

- 台账：`tracking/DEU/institutions_atom/`（本批新建）；设置 DEU/TOP500/D1、decay0、SUBINDUSTRY、trunc0.08、nanHandling ON、2014–2023。
- 批次 1（10 臂）：insd1 核心 × 5 条 institutions 腿 + 纯本集 3 腿 + 本集×MODEL 搭档 + QPvrZxPM 参考。
- ⚠ 首轮 2026-11-23 10 臂（`2XZ4cr6kG4Gvb6816RTO7bEq`）平台排队 >25min 无 children；并行补发 2 臂探针（`1bxvWXcrP4QBcxTxkOYKmfJ`）。读数待收。
- ⚠ 2026-11-23 实读：insd1_holdings 族已被 2026-11-21 提交母件占位（prod 0.90–0.91），本批含 insd1 核心的 5 臂预计仅作结构参考、不可交付；可交付面看 pure-inst / inst×MODEL / significant_value×inst。

## 6. blockedFields / 禁用

- 无幽灵字段：平台 11 = 本地 11 同名同 coverage（local userCount 旧）。
- 0 值膨胀：buyers/sellers 家数在「该季无交易」时为合法 0，分母必须用 `count_institutional_holders_security` 或存量字段，避免 0/0。
- 无法构造集中度/HHI（无逐机构向量）。
