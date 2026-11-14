# IND / model77 全字段静态画像 · 2026-11-14

> 人工撰写审计 → `reports/dataset_experience/`。**100% 字段覆盖，不抽样**：MCP `get_datafields` 实读 `count=23 / platform_count=23 / complete=True`。事实源（机器读）= `tracking/IND/reference/ind_model77_fields.json`。

- category=MODEL｜当季塔=3（已亮）｜覆盖率=0.4001｜字段=23｜类型分布={'MATRIX': 23, 'V_UNUSABLE': 23}

## 0. 取数口径与三条须知

1. **工具坑（本轮实测）**：`get_datafields(max_fields=null)` 显式传参会触发 `max_fields_cap`，每集只返 1 条且 `complete=false`。正确用法 = **不传 `max_fields`**（dataset-scoped 缺省不限量）或传 ≥ `platform_count` 的整数；同时必须 `filter_sharpe=False`，否则按 OS/IS Sharpe<0 过滤字段 = 隐性抽样。
2. `coverage` 不可信：GBR 2026-11-09 实测与探针 `longCount+shortCount` 有偏差；VECTOR 字段的 coverage 是**历史累计覆盖**，非任意时点覆盖（IND `news29` 判死即因 8/8 空持仓）。本表对 VECTOR 一律在「分布特征」列标稀疏风险。
3. MCP 返回**不含** `updateCount` / 更新频率 / 分布形态；IND 不在离线体检包七区（ASI/CHN/EUR/GLB/JPN/KOR/USA）且本机 `tracking/mining/field_inspect_ind_*.json` 零命中。故「更新频率」「分布特征」列由字段语义 + DB `field_profile_full.freq_hint` 静态推定，逐条标 `[inferred]`；**在线六法最小仿真集只对入选主信号字段做**，不对 185 字段逐字段跑（Q2 口径）。

## 1. 机制风险（选集证据修订）

已亮塔 3/3（lit_category_but_unoccupied）；⚠ MCP 实读 23 字段全是 ESG/治理评分、cov **0.4001**（DB 画像 0.8495 为旧版本，已作废）→ 与 IND 已判死的治理评分类（fundamental1 / other567 / other128）同型 → 标 WEAK_MECHANISM，配额上限 2 条。

## 2. 全字段画像（8 列，23 字段无空行）

| # | field | type | coverage | userCount | alphaCount | 更新频率 | 分布特征 | 可用性 | 潜在 alpha 适用性 |
|---:|---|---|---:|---:|---:|---|---|---|---|
| 1 | `board_compensation_policy_score` | MATRIX | 0.4001 | n/a [inferred] | n/a [inferred] | 快照（按库表更新，需实测） (DB field_profile_full) | 有界 [0,1] 或 [-1,1] 的评分类，concentrated/ceiling [inferred] | 不可用（判死/元数据字段）；cov<0.5 → 必须 ts_backfill/group_backfill 或在线补判；进 S1 黑名单，不生成表达式 | 不适用：FE 步2：ts_delta 或 ts_zscore 转变化率；机制=持股结构变化（禁净买入族） → 排除 |
| 2 | `board_functionality_score` | MATRIX | 0.4001 | n/a [inferred] | n/a [inferred] | 快照（按库表更新，需实测） (DB field_profile_full) | 有界 [0,1] 或 [-1,1] 的评分类，concentrated/ceiling [inferred] | 不可用（判死/元数据字段）；cov<0.5 → 必须 ts_backfill/group_backfill 或在线补判；进 S1 黑名单，不生成表达式 | 不适用：FE 步2：仅作 group_* 分组轴；机制=分组中性化（非主信号） → 排除 |
| 3 | `board_structure_governance_score` | MATRIX | 0.4001 | n/a [inferred] | n/a [inferred] | 快照（按库表更新，需实测） (DB field_profile_full) | 有界 [0,1] 或 [-1,1] 的评分类，concentrated/ceiling [inferred] | 不可用（判死/元数据字段）；cov<0.5 → 必须 ts_backfill/group_backfill 或在线补判；进 S1 黑名单，不生成表达式 | 不适用：FE 步2：仅作 group_* 分组轴；机制=分组中性化（非主信号） → 排除 |
| 4 | `corporate_governance_score` | MATRIX | 0.4001 | n/a [inferred] | n/a [inferred] | 快照（按库表更新，需实测） (DB field_profile_full) | 有界 [0,1] 或 [-1,1] 的评分类，concentrated/ceiling [inferred] | 不可用（判死/元数据字段）；cov<0.5 → 必须 ts_backfill/group_backfill 或在线补判；进 S1 黑名单，不生成表达式 | 不适用：FE 步2：ts_delta(66) 或 divide 标准化；机制=事件时钟/PEAD（禁日历裸排序） → 排除 |
| 5 | `customer_product_responsibility_score` | MATRIX | 0.4001 | n/a [inferred] | n/a [inferred] | 快照（按库表更新，需实测） (DB field_profile_full) | 有界 [0,1] 或 [-1,1] 的评分类，concentrated/ceiling [inferred] | 不可用（判死/元数据字段）；cov<0.5 → 必须 ts_backfill/group_backfill 或在线补判；进 S1 黑名单，不生成表达式 | 不适用：FE 步2：rank/winsorize；机制=评分型需 group_neutralize 但 IND robust 墙高风险 → 排除 |
| 6 | `economic_market_performance_score` | MATRIX | 0.4001 | n/a [inferred] | n/a [inferred] | 快照（按库表更新，需实测） (DB field_profile_full) | 有界 [0,1] 或 [-1,1] 的评分类，concentrated/ceiling [inferred] | 不可用（判死/元数据字段）；cov<0.5 → 必须 ts_backfill/group_backfill 或在线补判；进 S1 黑名单，不生成表达式 | 不适用：FE 步2：ts_delta 或 ts_zscore 转变化率；机制=持股结构变化（禁净买入族） → 排除 |
| 7 | `economic_product_sustainability_score` | MATRIX | 0.4001 | n/a [inferred] | n/a [inferred] | 快照（按库表更新，需实测） (DB field_profile_full) | 有界 [0,1] 或 [-1,1] 的评分类，concentrated/ceiling [inferred] | 不可用（判死/元数据字段）；cov<0.5 → 必须 ts_backfill/group_backfill 或在线补判；进 S1 黑名单，不生成表达式 | 不适用：FE 步2：rank/winsorize；机制=评分型需 group_neutralize 但 IND robust 墙高风险 → 排除 |
| 8 | `economic_resource_circularity_score` | MATRIX | 0.4001 | n/a [inferred] | n/a [inferred] | 快照（按库表更新，需实测） (DB field_profile_full) | 有界 [0,1] 或 [-1,1] 的评分类，concentrated/ceiling [inferred] | 不可用（判死/元数据字段）；cov<0.5 → 必须 ts_backfill/group_backfill 或在线补判；进 S1 黑名单，不生成表达式 | 不适用：FE 步2：ts_delta 或 ts_zscore 转变化率；机制=持股结构变化（禁净买入族） → 排除 |
| 9 | `economic_score_asset4` | MATRIX | 0.4001 | n/a [inferred] | n/a [inferred] | 快照（按库表更新，需实测） (DB field_profile_full) | 有界 [0,1] 或 [-1,1] 的评分类，concentrated/ceiling [inferred] | 不可用（判死/元数据字段）；cov<0.5 → 必须 ts_backfill/group_backfill 或在线补判；进 S1 黑名单，不生成表达式 | 不适用：FE 步2：ts_delta(66) 或 divide 标准化；机制=事件时钟/PEAD（禁日历裸排序） → 排除 |
| 10 | `environmental_emissions_reduction_score` | MATRIX | 0.4001 | n/a [inferred] | n/a [inferred] | 快照（按库表更新，需实测） (DB field_profile_full) | 有界 [0,1] 或 [-1,1] 的评分类，concentrated/ceiling [inferred] | 不可用（判死/元数据字段）；cov<0.5 → 必须 ts_backfill/group_backfill 或在线补判；进 S1 黑名单，不生成表达式 | 不适用：FE 步2：rank/winsorize；机制=评分型需 group_neutralize 但 IND robust 墙高风险 → 排除 |
| 11 | `environmental_policy_initiative_score` | MATRIX | 0.4001 | n/a [inferred] | n/a [inferred] | 快照（按库表更新，需实测） (DB field_profile_full) | 有界 [0,1] 或 [-1,1] 的评分类，concentrated/ceiling [inferred] | 不可用（判死/元数据字段）；cov<0.5 → 必须 ts_backfill/group_backfill 或在线补判；进 S1 黑名单，不生成表达式 | 不适用：FE 步2：仅作 group_* 分组轴；机制=分组中性化（非主信号） → 排除 |
| 12 | `environmental_resource_reduction_score` | MATRIX | 0.4001 | n/a [inferred] | n/a [inferred] | 快照（按库表更新，需实测） (DB field_profile_full) | 有界 [0,1] 或 [-1,1] 的评分类，concentrated/ceiling [inferred] | 不可用（判死/元数据字段）；cov<0.5 → 必须 ts_backfill/group_backfill 或在线补判；进 S1 黑名单，不生成表达式 | 不适用：FE 步2：rank/winsorize；机制=评分型需 group_neutralize 但 IND robust 墙高风险 → 排除 |
| 13 | `environmental_score_asset4` | MATRIX | 0.4001 | n/a [inferred] | n/a [inferred] | 快照（按库表更新，需实测） (DB field_profile_full) | 有界 [0,1] 或 [-1,1] 的评分类，concentrated/ceiling [inferred] | 不可用（判死/元数据字段）；cov<0.5 → 必须 ts_backfill/group_backfill 或在线补判；进 S1 黑名单，不生成表达式 | 不适用：FE 步2：ts_delta(66) 或 divide 标准化；机制=事件时钟/PEAD（禁日历裸排序） → 排除 |
| 14 | `governance_integrity_vision_score` | MATRIX | 0.4001 | n/a [inferred] | n/a [inferred] | 快照（按库表更新，需实测） (DB field_profile_full) | 有界 [0,1] 或 [-1,1] 的评分类，concentrated/ceiling [inferred] | 不可用（判死/元数据字段）；cov<0.5 → 必须 ts_backfill/group_backfill 或在线补判；进 S1 黑名单，不生成表达式 | 不适用：FE 步2：仅作 group_* 分组轴；机制=分组中性化（非主信号） → 排除 |
| 15 | `investor_relations_score_asset4` | MATRIX | 0.4001 | n/a [inferred] | n/a [inferred] | 快照（按库表更新，需实测） (DB field_profile_full) | 有界 [0,1] 或 [-1,1] 的评分类，concentrated/ceiling [inferred] | 不可用（判死/元数据字段）；cov<0.5 → 必须 ts_backfill/group_backfill 或在线补判；进 S1 黑名单，不生成表达式 | 不适用：FE 步2：ts_delta(66) 或 divide 标准化；机制=事件时钟/PEAD（禁日历裸排序） → 排除 |
| 16 | `shareholder_rights_score` | MATRIX | 0.4001 | n/a [inferred] | n/a [inferred] | 快照（按库表更新，需实测） (DB field_profile_full) | 有界 [0,1] 或 [-1,1] 的评分类，concentrated/ceiling [inferred] | 不可用（判死/元数据字段）；cov<0.5 → 必须 ts_backfill/group_backfill 或在线补判；进 S1 黑名单，不生成表达式 | 不适用：FE 步2：仅作 group_* 分组轴；机制=分组中性化（非主信号） → 排除 |
| 17 | `social_community_score` | MATRIX | 0.4001 | n/a [inferred] | n/a [inferred] | 快照（按库表更新，需实测） (DB field_profile_full) | 有界 [0,1] 或 [-1,1] 的评分类，concentrated/ceiling [inferred] | 不可用（判死/元数据字段）；cov<0.5 → 必须 ts_backfill/group_backfill 或在线补判；进 S1 黑名单，不生成表达式 | 不适用：FE 步2：rank/winsorize；机制=评分型需 group_neutralize 但 IND robust 墙高风险 → 排除 |
| 18 | `social_human_rights_score` | MATRIX | 0.4001 | n/a [inferred] | n/a [inferred] | 快照（按库表更新，需实测） (DB field_profile_full) | 有界 [0,1] 或 [-1,1] 的评分类，concentrated/ceiling [inferred] | 不可用（判死/元数据字段）；cov<0.5 → 必须 ts_backfill/group_backfill 或在线补判；进 S1 黑名单，不生成表达式 | 不适用：FE 步2：rank/winsorize；机制=评分型需 group_neutralize 但 IND robust 墙高风险 → 排除 |
| 19 | `social_score_asset4` | MATRIX | 0.4001 | n/a [inferred] | n/a [inferred] | 快照（按库表更新，需实测） (DB field_profile_full) | 有界 [0,1] 或 [-1,1] 的评分类，concentrated/ceiling [inferred] | 不可用（判死/元数据字段）；cov<0.5 → 必须 ts_backfill/group_backfill 或在线补判；进 S1 黑名单，不生成表达式 | 不适用：FE 步2：ts_delta(66) 或 divide 标准化；机制=事件时钟/PEAD（禁日历裸排序） → 排除 |
| 20 | `workforce_diversity_opportunity_score` | MATRIX | 0.4001 | n/a [inferred] | n/a [inferred] | 快照（按库表更新，需实测） (DB field_profile_full) | 有界 [0,1] 或 [-1,1] 的评分类，concentrated/ceiling [inferred] | 不可用（判死/元数据字段）；cov<0.5 → 必须 ts_backfill/group_backfill 或在线补判；进 S1 黑名单，不生成表达式 | 不适用：FE 步2：rank/winsorize；机制=评分型需 group_neutralize 但 IND robust 墙高风险 → 排除 |
| 21 | `workforce_equity_score` | MATRIX | 0.4001 | n/a [inferred] | n/a [inferred] | 快照（按库表更新，需实测） (DB field_profile_full) | 有界 [0,1] 或 [-1,1] 的评分类，concentrated/ceiling [inferred] | 不可用（判死/元数据字段）；cov<0.5 → 必须 ts_backfill/group_backfill 或在线补判；进 S1 黑名单，不生成表达式 | 不适用：FE 步2：ts_delta(66) 或 divide 标准化；机制=事件时钟/PEAD（禁日历裸排序） → 排除 |
| 22 | `workforce_training_development_score` | MATRIX | 0.4001 | n/a [inferred] | n/a [inferred] | 快照（按库表更新，需实测） (DB field_profile_full) | 有界 [0,1] 或 [-1,1] 的评分类，concentrated/ceiling [inferred] | 不可用（判死/元数据字段）；cov<0.5 → 必须 ts_backfill/group_backfill 或在线补判；进 S1 黑名单，不生成表达式 | 不适用：FE 步2：rank/winsorize；机制=评分型需 group_neutralize 但 IND robust 墙高风险 → 排除 |
| 23 | `workplace_health_safety_score` | MATRIX | 0.4001 | n/a [inferred] | n/a [inferred] | 快照（按库表更新，需实测） (DB field_profile_full) | 有界 [0,1] 或 [-1,1] 的评分类，concentrated/ceiling [inferred] | 不可用（判死/元数据字段）；cov<0.5 → 必须 ts_backfill/group_backfill 或在线补判；进 S1 黑名单，不生成表达式 | 不适用：FE 步2：rank/winsorize；机制=评分型需 group_neutralize 但 IND robust 墙高风险 → 排除 |

## 3. 判死字段通道（不生成表达式）

共 23 / 23 字段进黑名单：`board_compensation_policy_score`, `board_functionality_score`, `board_structure_governance_score`, `corporate_governance_score`, `customer_product_responsibility_score`, `economic_market_performance_score`, `economic_product_sustainability_score`, `economic_resource_circularity_score`, `economic_score_asset4`, `environmental_emissions_reduction_score`, `environmental_policy_initiative_score`, `environmental_resource_reduction_score`, `environmental_score_asset4`, `governance_integrity_vision_score`, `investor_relations_score_asset4`, `shareholder_rights_score`, `social_community_score`, `social_human_rights_score`, `social_score_asset4`, `workforce_diversity_opportunity_score`, `workforce_equity_score`, `workforce_training_development_score`, `workplace_health_safety_score`


## 4. 主信号候选（交 FE 步 2）

共 0 字段：无；需先做在线六法最小集探针


## 5. 在线六法补测清单（仅主信号字段）

一批 6 条：`x`｜`x!=0`｜`ts_std_dev(x,N)!=0` N=5/22/66｜`abs(x)>1`；扩展 ≤8 条：`abs>X` X=10/100、`ts_mean(x,252)>X`、`zscore>k`。
设置 `Neutralization=None / Decay=0 / Test Period=P0Y0M0D`，读 `longCount/shortCount`；VECTOR 先 `vec_avg`。
工具 = `mcp__wq-brain-http__create_multi_simulation`（2–10 条，连坐语义），发批前 `preflight_expressions`。
