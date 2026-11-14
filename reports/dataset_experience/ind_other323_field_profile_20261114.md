# IND / other323 全字段静态画像 · 2026-11-14

> 人工撰写审计 → `reports/dataset_experience/`。**100% 字段覆盖，不抽样**：MCP `get_datafields` 实读 `count=11 / platform_count=11 / complete=True`。事实源（机器读）= `tracking/IND/reference/ind_other323_fields.json`。

- category=OTHER｜当季塔=4（已亮）｜覆盖率=0.9996｜字段=11｜类型分布={'VECTOR': 11, 'V_UNTESTED': 11}

## 0. 取数口径与三条须知

1. **工具坑（本轮实测）**：`get_datafields(max_fields=null)` 显式传参会触发 `max_fields_cap`，每集只返 1 条且 `complete=false`。正确用法 = **不传 `max_fields`**（dataset-scoped 缺省不限量）或传 ≥ `platform_count` 的整数；同时必须 `filter_sharpe=False`，否则按 OS/IS Sharpe<0 过滤字段 = 隐性抽样。
2. `coverage` 不可信：GBR 2026-11-09 实测与探针 `longCount+shortCount` 有偏差；VECTOR 字段的 coverage 是**历史累计覆盖**，非任意时点覆盖（IND `news29` 判死即因 8/8 空持仓）。本表对 VECTOR 一律在「分布特征」列标稀疏风险。
3. MCP 返回**不含** `updateCount` / 更新频率 / 分布形态；IND 不在离线体检包七区（ASI/CHN/EUR/GLB/JPN/KOR/USA）且本机 `tracking/mining/field_inspect_ind_*.json` 零命中。故「更新频率」「分布特征」列由字段语义 + DB `field_profile_full.freq_hint` 静态推定，逐条标 `[inferred]`；**在线六法最小仿真集只对入选主信号字段做**，不对 185 字段逐字段跑（Q2 口径）。

## 1. 机制风险（选集证据修订）

已亮塔 4/3（lit_category_but_unoccupied）；⚠ MCP 实读 11 字段全是 VECTOR 股本/票面/手数/标识符静态数据 → 几无横截面收益信息 → 标 WEAK_MECHANISM，仅作分组轴/条件腿候选，配额上限 2 条。

## 2. 全字段画像（8 列，11 字段无空行）

| # | field | type | coverage | userCount | alphaCount | 更新频率 | 分布特征 | 可用性 | 潜在 alpha 适用性 |
|---:|---|---|---:|---:|---:|---|---|---|---|
| 1 | `actual_shares_outstanding` | VECTOR | 0.9996 | n/a [inferred] | n/a [inferred] | 事件/逐笔型（VECTOR） (DB field_profile_full) | point_mass / 稀疏事件型（VECTOR 需 vec_* 折叠，任意时点有值股票数可能远小于 coverage） [inferred] | 待测（无历史回测，首探判定）；VECTOR：最内层必须 vec_avg/vec_sum 折叠，否则平台 400 | FE 步0：先做类型与覆盖探针，再定机制 |
| 2 | `oth323_esod` | VECTOR | 0.9996 | n/a [inferred] | n/a [inferred] | 事件/逐笔型（VECTOR） (DB field_profile_full) | point_mass / 稀疏事件型（VECTOR 需 vec_* 折叠，任意时点有值股票数可能远小于 coverage） [inferred] | 待测（无历史回测，首探判定）；VECTOR：最内层必须 vec_avg/vec_sum 折叠，否则平台 400 | FE 步0：先做类型与覆盖探针，再定机制 |
| 3 | `oth323_esor` | VECTOR | 0.9996 | n/a [inferred] | n/a [inferred] | 事件/逐笔型（VECTOR） (DB field_profile_full) | point_mass / 稀疏事件型（VECTOR 需 vec_* 折叠，任意时点有值股票数可能远小于 coverage） [inferred] | 待测（无历史回测，首探判定）；VECTOR：最内层必须 vec_avg/vec_sum 折叠，否则平台 400 | FE 步0：先做类型与覆盖探针，再定机制 |
| 4 | `oth323_ibc` | VECTOR | 0.9996 | n/a [inferred] | n/a [inferred] | 事件/逐笔型（VECTOR） (DB field_profile_full) | point_mass / 稀疏事件型（VECTOR 需 vec_* 折叠，任意时点有值股票数可能远小于 coverage） [inferred] | 待测（无历史回测，首探判定）；VECTOR：最内层必须 vec_avg/vec_sum 折叠，否则平台 400 | 不适用：元数据/标识符，无经济锚 → FE 步3 剔除 |
| 5 | `oth323_ibs` | VECTOR | 0.9996 | n/a [inferred] | n/a [inferred] | 事件/逐笔型（VECTOR） (DB field_profile_full) | point_mass / 稀疏事件型（VECTOR 需 vec_* 折叠，任意时点有值股票数可能远小于 coverage） [inferred] | 待测（无历史回测，首探判定）；VECTOR：最内层必须 vec_avg/vec_sum 折叠，否则平台 400 | 不适用：元数据/标识符，无经济锚 → FE 步3 剔除 |
| 6 | `oth323_par_amt` | VECTOR | 0.9996 | n/a [inferred] | n/a [inferred] | 事件/逐笔型（VECTOR） (DB field_profile_full) | point_mass / 稀疏事件型（VECTOR 需 vec_* 折叠，任意时点有值股票数可能远小于 coverage） [inferred] | 待测（无历史回测，首探判定）；VECTOR：最内层必须 vec_avg/vec_sum 折叠，否则平台 400 | 不适用：元数据/标识符，无经济锚 → FE 步3 剔除 |
| 7 | `oth323_pxrls` | VECTOR | 0.9996 | n/a [inferred] | n/a [inferred] | 事件/逐笔型（VECTOR） (DB field_profile_full) | point_mass / 稀疏事件型（VECTOR 需 vec_* 折叠，任意时点有值股票数可能远小于 coverage） [inferred] | 待测（无历史回测，首探判定）；VECTOR：最内层必须 vec_avg/vec_sum 折叠，否则平台 400 | 不适用：元数据/标识符，无经济锚 → FE 步3 剔除 |
| 8 | `oth323_pxtls` | VECTOR | 0.9996 | n/a [inferred] | n/a [inferred] | 事件/逐笔型（VECTOR） (DB field_profile_full) | point_mass / 稀疏事件型（VECTOR 需 vec_* 折叠，任意时点有值股票数可能远小于 coverage） [inferred] | 待测（无历史回测，首探判定）；VECTOR：最内层必须 vec_avg/vec_sum 折叠，否则平台 400 | 不适用：元数据/标识符，无经济锚 → FE 步3 剔除 |
| 9 | `par_value_amount` | VECTOR | 0.9996 | n/a [inferred] | n/a [inferred] | 事件/逐笔型（VECTOR） (DB field_profile_full) | point_mass / 稀疏事件型（VECTOR 需 vec_* 折叠，任意时点有值股票数可能远小于 coverage） [inferred] | 待测（无历史回测，首探判定）；VECTOR：最内层必须 vec_avg/vec_sum 折叠，否则平台 400 | FE 步2：仅作 group_* 分组轴；机制=分组中性化（非主信号） |
| 10 | `round_lot_size_value` | VECTOR | 0.9996 | n/a [inferred] | n/a [inferred] | 事件/逐笔型（VECTOR） (DB field_profile_full) | point_mass / 稀疏事件型（VECTOR 需 vec_* 折叠，任意时点有值股票数可能远小于 coverage） [inferred] | 待测（无历史回测，首探判定）；VECTOR：最内层必须 vec_avg/vec_sum 折叠，否则平台 400 | FE 步0：先做类型与覆盖探针，再定机制 |
| 11 | `trade_lot_size_value` | VECTOR | 0.9996 | n/a [inferred] | n/a [inferred] | 事件/逐笔型（VECTOR） (DB field_profile_full) | point_mass / 稀疏事件型（VECTOR 需 vec_* 折叠，任意时点有值股票数可能远小于 coverage） [inferred] | 待测（无历史回测，首探判定）；VECTOR：最内层必须 vec_avg/vec_sum 折叠，否则平台 400 | FE 步2 预处理：rank/ts_zscore 去量纲；机制=波动/反转（禁裸水平相加） |

## 3. 判死字段通道（不生成表达式）

共 5 / 11 字段进黑名单：`oth323_ibc`, `oth323_ibs`, `oth323_par_amt`, `oth323_pxrls`, `oth323_pxtls`


## 4. 主信号候选（交 FE 步 2）

共 0 字段：无；需先做在线六法最小集探针


## 5. 在线六法补测清单（仅主信号字段）

一批 6 条：`x`｜`x!=0`｜`ts_std_dev(x,N)!=0` N=5/22/66｜`abs(x)>1`；扩展 ≤8 条：`abs>X` X=10/100、`ts_mean(x,252)>X`、`zscore>k`。
设置 `Neutralization=None / Decay=0 / Test Period=P0Y0M0D`，读 `longCount/shortCount`；VECTOR 先 `vec_avg`。
工具 = `mcp__wq-brain-http__create_multi_simulation`（2–10 条，连坐语义），发批前 `preflight_expressions`。
