# IND / institutions6 全字段静态画像 · 2026-11-14

> 人工撰写审计 → `reports/dataset_experience/`。**100% 字段覆盖，不抽样**：MCP `get_datafields` 实读 `count=11 / platform_count=11 / complete=True`。事实源（机器读）= `tracking/IND/reference/ind_institutions6_fields.json`。

- category=INSTITUTIONS｜当季塔=1（未亮）｜覆盖率=0.9920｜字段=11｜类型分布={'MATRIX': 11, 'V_ALIVE': 11}

## 0. 取数口径与三条须知

1. **工具坑（本轮实测）**：`get_datafields(max_fields=null)` 显式传参会触发 `max_fields_cap`，每集只返 1 条且 `complete=false`。正确用法 = **不传 `max_fields`**（dataset-scoped 缺省不限量）或传 ≥ `platform_count` 的整数；同时必须 `filter_sharpe=False`，否则按 OS/IS Sharpe<0 过滤字段 = 隐性抽样。
2. `coverage` 不可信：GBR 2026-11-09 实测与探针 `longCount+shortCount` 有偏差；VECTOR 字段的 coverage 是**历史累计覆盖**，非任意时点覆盖（IND `news29` 判死即因 8/8 空持仓）。本表对 VECTOR 一律在「分布特征」列标稀疏风险。
3. MCP 返回**不含** `updateCount` / 更新频率 / 分布形态；IND 不在离线体检包七区（ASI/CHN/EUR/GLB/JPN/KOR/USA）且本机 `tracking/mining/field_inspect_ind_*.json` 零命中。故「更新频率」「分布特征」列由字段语义 + DB `field_profile_full.freq_hint` 静态推定，逐条标 `[inferred]`；**在线六法最小仿真集只对入选主信号字段做**，不对 185 字段逐字段跑（Q2 口径）。

## 1. 机制风险（选集证据修订）

未亮塔 1/3；ACTIVE/OS 未占用；11 字段全 ALIVE。族锁：机构净买入（IND-W149-INST6-NETBUY-WEAK-DEAD）。

## 2. 全字段画像（8 列，11 字段无空行）

| # | field | type | coverage | userCount | alphaCount | 更新频率 | 分布特征 | 可用性 | 潜在 alpha 适用性 |
|---:|---|---|---:|---:|---:|---|---|---|---|
| 1 | `aggregate_equity_value_all_owners` | MATRIX | 0.992 | n/a [inferred] | n/a [inferred] | 快照（按库表更新，需实测） (DB field_profile_full) | 强右偏、跨公司量纲差数个数量级（须 rank/ts_zscore 去量纲） [inferred] | 可用（历史有 ALIVE 实证） | FE 步2：ts_delta(66) 或 divide 标准化；机制=事件时钟/PEAD（禁日历裸排序） |
| 2 | `aggregate_equity_value_institutions` | MATRIX | 0.992 | n/a [inferred] | n/a [inferred] | 快照（按库表更新，需实测） (DB field_profile_full) | 强右偏、跨公司量纲差数个数量级（须 rank/ts_zscore 去量纲） [inferred] | 可用（历史有 ALIVE 实证） | FE 步2：ts_delta(66) 或 divide 标准化；机制=事件时钟/PEAD（禁日历裸排序） |
| 3 | `aggregate_share_count_all_owners` | MATRIX | 0.992 | n/a [inferred] | n/a [inferred] | 快照（按库表更新，需实测） (DB field_profile_full) | 强右偏、跨公司量纲差数个数量级（须 rank/ts_zscore 去量纲） [inferred] | 可用（历史有 ALIVE 实证） | FE 步0：先做类型与覆盖探针，再定机制 |
| 4 | `aggregate_share_count_institutions` | MATRIX | 0.992 | n/a [inferred] | n/a [inferred] | 快照（按库表更新，需实测） (DB field_profile_full) | 强右偏、跨公司量纲差数个数量级（须 rank/ts_zscore 去量纲） [inferred] | 可用（历史有 ALIVE 实证） | FE 步2：ts_delta 或 ts_zscore 转变化率；机制=持股结构变化（禁净买入族） |
| 5 | `count_institutional_buyers_security` | MATRIX | 0.992 | n/a [inferred] | n/a [inferred] | 快照（按库表更新，需实测） (DB field_profile_full) | 强右偏、跨公司量纲差数个数量级（须 rank/ts_zscore 去量纲） [inferred] | 可用（历史有 ALIVE 实证） | FE 步2：ts_delta 或 ts_zscore 转变化率；机制=持股结构变化（禁净买入族） |
| 6 | `count_institutional_holders_security` | MATRIX | 0.992 | n/a [inferred] | n/a [inferred] | 快照（按库表更新，需实测） (DB field_profile_full) | 强右偏、跨公司量纲差数个数量级（须 rank/ts_zscore 去量纲） [inferred] | 可用（历史有 ALIVE 实证） | FE 步2：ts_delta 或 ts_zscore 转变化率；机制=持股结构变化（禁净买入族） |
| 7 | `count_institutional_sellers_security` | MATRIX | 0.992 | n/a [inferred] | n/a [inferred] | 快照（按库表更新，需实测） (DB field_profile_full) | 强右偏、跨公司量纲差数个数量级（须 rank/ts_zscore 去量纲） [inferred] | 可用（历史有 ALIVE 实证） | FE 步2：ts_delta 或 ts_zscore 转变化率；机制=持股结构变化（禁净买入族） |
| 8 | `market_value_institutional_shares_acquired` | MATRIX | 0.992 | n/a [inferred] | n/a [inferred] | 快照（按库表更新，需实测） (DB field_profile_full) | 强右偏、跨公司量纲差数个数量级（须 rank/ts_zscore 去量纲） [inferred] | 可用（历史有 ALIVE 实证） | FE 步2：ts_delta 或 ts_zscore 转变化率；机制=持股结构变化（禁净买入族） |
| 9 | `market_value_institutional_shares_disposed` | MATRIX | 0.9915 | n/a [inferred] | n/a [inferred] | 快照（按库表更新，需实测） (DB field_profile_full) | 强右偏、跨公司量纲差数个数量级（须 rank/ts_zscore 去量纲） [inferred] | 可用（历史有 ALIVE 实证） | FE 步2：ts_delta 或 ts_zscore 转变化率；机制=持股结构变化（禁净买入族） |
| 10 | `quantity_institutional_shares_acquired` | MATRIX | 0.992 | n/a [inferred] | n/a [inferred] | 快照（按库表更新，需实测） (DB field_profile_full) | 强右偏、跨公司量纲差数个数量级（须 rank/ts_zscore 去量纲） [inferred] | 可用（历史有 ALIVE 实证） | FE 步2：ts_delta 或 ts_zscore 转变化率；机制=持股结构变化（禁净买入族） |
| 11 | `quantity_institutional_shares_disposed` | MATRIX | 0.992 | n/a [inferred] | n/a [inferred] | 快照（按库表更新，需实测） (DB field_profile_full) | 强右偏、跨公司量纲差数个数量级（须 rank/ts_zscore 去量纲） [inferred] | 可用（历史有 ALIVE 实证） | FE 步2：ts_delta 或 ts_zscore 转变化率；机制=持股结构变化（禁净买入族） |

## 3. 判死字段通道（不生成表达式）

共 0 / 11 字段进黑名单：无


## 4. 主信号候选（交 FE 步 2）

共 11 字段：`aggregate_equity_value_all_owners` (bestS=2.76, 2Y=2.41), `aggregate_equity_value_institutions` (bestS=2.9, 2Y=3.18), `aggregate_share_count_all_owners` (bestS=2.53, 2Y=2.79), `aggregate_share_count_institutions` (bestS=3.45, 2Y=2.94), `count_institutional_buyers_security` (bestS=3.23, 2Y=2.5), `count_institutional_holders_security` (bestS=3.18, 2Y=2.3), `count_institutional_sellers_security` (bestS=3.1, 2Y=2.87), `market_value_institutional_shares_acquired` (bestS=2.92, 2Y=2.66), `market_value_institutional_shares_disposed` (bestS=2.81, 2Y=2.98), `quantity_institutional_shares_acquired` (bestS=3.19, 2Y=3.04), `quantity_institutional_shares_disposed` (bestS=3.2, 2Y=3.29)


## 5. 在线六法补测清单（仅主信号字段）

一批 6 条：`x`｜`x!=0`｜`ts_std_dev(x,N)!=0` N=5/22/66｜`abs(x)>1`；扩展 ≤8 条：`abs>X` X=10/100、`ts_mean(x,252)>X`、`zscore>k`。
设置 `Neutralization=None / Decay=0 / Test Period=P0Y0M0D`，读 `longCount/shortCount`；VECTOR 先 `vec_avg`。
工具 = `mcp__wq-brain-http__create_multi_simulation`（2–10 条，连坐语义），发批前 `preflight_expressions`。
