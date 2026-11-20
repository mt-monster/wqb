# FIELD 档案：institutions6（DEU / TOP500 / D1）· 2026-11-16

> S1 字段档案（平台实读版）。全部字段/覆盖读数来自平台 MCP 实返，本地仅作先验与历史回测引用；本地画像含幽灵字段，一律不以之为准。

## 0. 读数来源

| 来源 | 内容 | 证据 |
|---|---|---|
| `get_datafields(dataset_id="institutions6", region="DEU", delay=1, universe="TOP500")` | **11 字段全量**，`count=11 / platform_count=11 / complete=true / pages_fetched=1`，每字段 `type=MATRIX, coverage=1.0`；`sharpe_filter_applied=false, sharpe_filter_removed=0` | 本轮平台实读（2026-11-16） |
| `get_datafields(..., data_type="VECTOR")` | count=0, platform_count=0 | 同上 |
| `get_datafields(..., data_type="GROUP")` | count=0, platform_count=0 | 同上 |
| `get_datasets(region=DEU, delay=0, universe=TOP500, search="institutions6")` | count=0 → **D0 无此数据集** | 同上 |
| `get_datasets(region=DEU, delay=1, universe=TOP500, search="institutions6")` | 数据集级：coverage 1.0, fieldCount 11, userCount 145, alphaCount 309, valueScore 3.0, pyramidMultiplier 1.6（**仅作上下文，不用数据集级 coverage 判可用性**） | 同上 |
| `get_alpha_details("QPvrZxPM")` / `("om6rrVKn")` | DEU institutions6 两条历史 alpha 的平台实读：settings/metrics/checks/ra/pyramids | 本轮平台实读 |
| `mcp__wqb-db__get_field_catalog(DEU, institutions6)` | 本地目录 11 字段与平台 11 同名同 coverage，但 userCount 陈旧（如 aggregate_share_count_all_owners 本地 8 vs 平台 14） | 本地 DB 只读 |
| `mcp__wqb-db__query_field_profile(region=USA/EUR, dataset=institutions6)` | 本地先验：USA 含 11 个 `inst6_*` 幽灵名；EUR 11 字段带 verdict（DEAD/DEAD_STATIC/UNTESTED） | 本地 DB 只读 |
| `data/wqb.db`（只读 sqlite，脚本 `logs/_tmp_inst6_deu_read.py`） | DEU institutions6 回测 18 行（wave `s2_institutions6_probe_r63_d1` ×8 + wave 92 ×10）+ 25 条表达式记录 | 本地 DB 只读 |
| `tracking/mining/field_coverage_DEU_d1_TOP500.json` | 数据集级快照（fetched_at=2026-08-10）：valueScore 6.0 / pyramidMultiplier 1.9 —— 与平台现值（3.0 / 1.6）漂移，仅作陈旧佐证 | 文件 |
| `docs/reference/GBR/unlit_tower_field_profile_20261105.md:289` | repo 先验：institutions6 为**季频**数据；`ts_mean(...,66)` 平滑反而伤（0.95→0.86） | 文件引用 |
| `docs/experience/03_region_dataset.md:310,318` | USA ATOM 先验：institutions6 3 探针 best S 0.07 / 2Y −0.15「持股计数族全灭」；判据 B（max S<1.58 出局） | 文件引用 |
| `tracking/DEU/config/cells.json:220-225` | DEU 判死标记 `DEU-INSTITUTIONS6-DEAD`：`text:""`、`bound:"inferred"` → **无实质判死记录**（AGENTS.md §7.6：判死标记不得单独作依据） | 文件引用 |

## 1. 平台实返回字段（11，全 MATRIX，coverage 全 1.0）

| # | field id | type | cov | userCount | alphaCount | description 摘要 |
|---|---|---|---|---|---|---|
| 1 | aggregate_equity_value_all_owners | MATRIX | 1.0 | 18 | 20 | 全体持有人（父子去重）持有市值合计 |
| 2 | aggregate_equity_value_institutions | MATRIX | 1.0 | 22 | 26 | 报告期末机构持有市值合计 |
| 3 | aggregate_share_count_all_owners | MATRIX | 1.0 | 14 | 21 | 全体持有人（父子去重）持股数合计 |
| 4 | aggregate_share_count_institutions | MATRIX | 1.0 | 17 | 22 | 报告期末机构持股数合计 |
| 5 | count_institutional_buyers_security | MATRIX | 1.0 | 44 | 63 | 报告期内买入机构家数 |
| 6 | count_institutional_holders_security | MATRIX | 1.0 | 19 | 31 | 报告期末持股>0 的机构家数 |
| 7 | count_institutional_sellers_security | MATRIX | 1.0 | 38 | 54 | 报告期内卖出机构家数 |
| 8 | market_value_institutional_shares_acquired | MATRIX | 1.0 | 54 | 88 | 报告期内机构买入金额 |
| 9 | market_value_institutional_shares_disposed | MATRIX | 1.0 | 23 | 39 | 报告期内机构卖出金额 |
| 10 | quantity_institutional_shares_acquired | MATRIX | 1.0 | 49 | 67 | 报告期内机构买入股数 |
| 11 | quantity_institutional_shares_disposed | MATRIX | 1.0 | 27 | 39 | 报告期内机构卖出股数 |

（平台实读原文即以上 11 条；无第 12 字段。`filter_sharpe` 默认开启但 `sharpe_filter_applied=false`，说明 11 条全数通过/无需过滤。）

## 2. 语义维度（按 description 归纳，字段名不作语义依据）

| 维度 | 代表字段 | 经济含义 |
|---|---|---|
| 机构持股存量（市值/股数） | aggregate_equity_value_institutions / aggregate_share_count_institutions | 机构净持仓水平；慢变量（报告期末快照） |
| 全体持有人存量（分母口径） | aggregate_equity_value_all_owners / aggregate_share_count_all_owners | 提供「机构渗透率」分子/分母与市值/总股本代理（all owners ≈ 全股本，父子去重） |
| 报告期机构买入流量 | market_value / quantity_institutional_shares_acquired | 机构增持强度（金额/股数两口径） |
| 报告期机构卖出流量 | market_value / quantity_institutional_shares_disposed | 机构减持与抛压 |
| 机构参与广度（家数） | count_institutional_buyers/sellers/holders_security | 买入/卖出/持有的机构家数 → 共识、羊群与覆盖宽度 |

## 3. 类型与降维要求（typeNotes）

- **11/11 全 MATRIX 标量**：无 VECTOR（data_type 过滤实读 0）、无 GROUP（0）、无 EVENT（0）。
  ⇒ **无需 vec_avg/vec_max 降维**；EVENT 类型不存在，**无 ts_event_* 探针对象**（单条探针要求 N/A）。
- **D0 不可用**：DEU/TOP500 delay=0 下 `get_datasets` 与 `get_datafields` 均返回 0 → 本数据集仅 D1 配置。
- **更新频率**：`get_datafields` 不返回该字段。repo 先验标「季频」（`docs/reference/GBR/unlit_tower_field_profile_20261105.md:289`，GBR 实测平滑窗 66d 反而伤）；本地 `field_profile.freq_hint` =「快照（按库表更新，需实测）」为静态推定。DEU 实测 TO 仅 1.5–10.3%（18 条）与季频台阶数据形态一致 —— **均为推断，平台未直接返回频率**。
- **构造约束（0 值膨胀）**：buyers/sellers 家数为「报告期内发生交易」计数，**合法 0 值**普遍（该季无机构买/卖）；设计必须用 `count_institutional_holders_security` 或存量字段作分母，避免 0/0 与 rank 稳定性问题。DEU 实测支持：分母用 holders 的表达式（QPvrZxPM）是 18 条里唯一 SUB 过闸者（SUB 0.53）。
- **无可构造轴**：无逐机构向量 ⇒ **无法构造机构集中度 / HHI / 持有人分散度类信号**（GBR 在 shortinterest3 上用 vec_stddev/vec_avg 的那类轴在此集不存在）。

## 4. 字段级覆盖实读（coverageNotes 的字段层）

- **平台字段级 coverage：11/11 = 1.0**，`complete=true`、`platform_count=11` —— 无平台级宽度塌缩字段。
- **宽度塌缩（结构性，非平台读数）**：count 类字段的 0 值膨胀与季频台阶（见 §3）；无工具能在字段面读到日度非零比例（IND 档案同口径确认：`reports/dataset_experience/ind_institutions6_field_profile_20261114.md:11` 记「MCP 返回不含 updateCount/更新频率/分布形态」）。
- **跨区宽度先验（EUR，非 DEU）**：EUR 画像中 `market_value_institutional_shares_disposed` coverage=0.9307 为全集最低（其余 0.997–0.9976）→ 卖出金额字段是历史上最薄的一根，DEU 实读仍为 1.0。
- **本地目录陈旧**：DEU catalog 11 字段与平台同名同 coverage，但 userCount 落后（例：aggregate_share_count_all_owners 本地 8 → 平台 14）；`field_coverage_DEU_d1_TOP500.json`（2026-08-10）valueScore 6.0/pyramid 1.9 vs 平台现值 3.0/1.6 —— 一律以平台为准。
- **幽灵字段**：DEU 无平台级幽灵（11=11）；本地 **USA** 画像含 11 个 `inst6_*` 旧名（见 §7）不在平台返回集内。

## 5. DEU 本地先验（18 条已测，机器读数，`logs/_tmp_inst6_deu_read.py` + get_alpha_details）

- **wave `s2_institutions6_probe_r63_d1`（2026-09-13，8 条裸探针）**：`rank(buyers)` S0.36/2Y0.86；`rank(mv_acq−mv_dis)` S0.31/2Y1.01；`rank(qty_acq−qty_dis)` S0.31/2Y1.21；`rank(count_holders)` S0.36/2Y0.91；`rank(ts_delta(holders,66))` S0.33/2Y0.19；`rank(buyers−sellers)` S−0.18 等。全 FAIL（LOW_SHARPE/LOW_FITNESS/LOW_2Y）。
- **wave 92（2026-10-30，10 条结构式）**：最佳 `group_neutralize(ts_zscore((buyers−sellers)/holders, 252), subindustry)` **S 0.71 / F 0.40 / 2Y 0.58 / SUB 0.53 / TO 8.4%**（alpha QPvrZxPM，平台实读）；`group_rank(ts_rank((qty_acq−qty_dis)/share_inst, 252), subindustry)` S 0.21 但 **2Y 1.79**；其余 S −0.44 ~ 0.36。
- **平台验证设置**（QPvrZxPM / om6rrVKn 实读）：DEU/TOP500/D1、decay=4、neutralization=SUBINDUSTRY、truncation=0.08、pasteurization ON、nanHandling OFF、maxTrade OFF、2014-01-01~2023-12-31 FULL；RA 失败 3–4 项；pyramid `DEU/D1/INSTITUTIONS` ×1.6。
- **配置覆盖缺口（D6）**：`expressions.settings_json` 只存 `{"template": "..."}` 标签，其余 16 条的 neutralization/decay 本地不可考 ⇒ **平台验证配置只有 1 套（SUBINDUSTRY/decay4/trunc0.08）**，D6「≥2 套配置」未满足，需补测 INDUSTRY/SECTOR/MARKET 中性化与 decay∈{0,10}。
- **判死标记无效**：`DEU-INSTITUTIONS6-DEAD` 为 `text:""` + `bound:"inferred"`（`tracking/DEU/config/cells.json:220-225`），无六维判死档案；AGENTS.md §7.6 判死标记不得单独作为依据。**信号层弱是真**（18 条 max S 0.71，全闸 FAIL），但「DEU 判死」不成立，字段面应继续可设计。
- 跨区对照：USA ATOM 3 探针 max S 0.07（`docs/experience/03_region_dataset.md:310`）；EUR 5 字段已测全 DEAD/DEAD_STATIC（aggregate_equity_value_institutions best_2y 0.47；count_buyers best_s −0.67）；GBR institutions6 上限 ≈0.94（`docs/reference/GBR/unlit_tower_field_profile_20261105.md:289` 段）。**DEU 未测出 1.0+ 信号，但三区上限也都在 1.58 闸下**。

## 6. 模板骨架（8 个，不同经济机制；换机制不是换窗口）

> 符号方向为经济机制预期，**全部需实测判向**（季频数据的符号常与日频直觉相反，DEU 66d 渗透率漂移实测 −0.44 即一例）。配置起点沿用已验证套 SUBINDUSTRY/decay4/trunc0.08，D6 补测轴见 §5。

| # | 机制（经济含义） | 骨架（FASTEXPR） | 预期符号 | 已测状态（DEU） |
|---|---|---|---|---|
| T1 | **机构净买入强度**：知情交易/需求压力（季频聚合口径对照臂） | `group_neutralize(ts_zscore(divide(subtract(quantity_institutional_shares_acquired, quantity_institutional_shares_disposed), ts_mean(aggregate_share_count_institutions, 252)), 126), subindustry)` | + | 机制已测（S≤0.21 @126d 无均值分母）；此变体仅调聚合口径，预期无增益，作对照 |
| T2 | **参与广度共识**：(买入家数−卖出家数)/持有家数 = 多机构同向信息聚合 | `group_rank(ts_rank(divide(subtract(count_institutional_buyers_security, count_institutional_sellers_security), count_institutional_holders_security), 126), subindustry)` | + | 机制已测 = DEU 最强（S 0.71 @ts_zscore252）；变体改 ts_rank 稳健化，上限预期仍 <1.0 |
| T3 | **机构持股水平（neglected-firm 溢价）**：inst/all-owners 股数占比的截面低位 | `-group_rank(divide(aggregate_share_count_institutions, aggregate_share_count_all_owners), subindustry)` | −（机构低配→被忽视溢价） | **水平态未测**（DEU 只测过其 66d 差分，S −0.44；EUR 水平态 DEAD_STATIC） |
| T4 | **机构化趋势漂移**：渗透率 4 季差分（长窗机构化=稳定资金流入） | `group_rank(ts_delta(divide(aggregate_share_count_institutions, aggregate_share_count_all_owners), 252), subindustry)` | +（但 66d 版实测 −0.44，长窗方向需实测） | 短窗已测（S −0.44），**252d 未测** |
| T5 | **机构成交择时价差**：隐含买入均价/卖出均价（mv/qty 比）——机构追高则未来承压 | `ts_zscore(divide(divide(market_value_institutional_shares_acquired, quantity_institutional_shares_acquired), divide(market_value_institutional_shares_disposed, quantity_institutional_shares_disposed)), 252)` | −（买价高于卖价=追涨，反转） | **未测**；需处理 0 股数分母（建议 ts_backfill + nanHandling ON 探针期） |
| T6 | **广度-规模分歧**：多机构小单（广度驱动）与少数大单（规模驱动）的符号背离 | `subtract(group_rank(divide(subtract(count_institutional_buyers_security, count_institutional_sellers_security), count_institutional_holders_security), subindustry), group_rank(divide(subtract(market_value_institutional_shares_acquired, market_value_institutional_shares_disposed), aggregate_equity_value_institutions), subindustry))` | +（广度高于规模时做多） | **未测** |
| T7 | **机构基础换手折价**：年度买卖总额/持股基数的倒数（高 churn=短线资金主导） | `-group_rank(divide(add(quantity_institutional_shares_acquired, quantity_institutional_shares_disposed), ts_mean(aggregate_share_count_institutions, 252)), subindustry)` | − | 市值口径 66d 版已测（S 0.15）；**股数口径+252d 未测** |
| T8 | **羊群拥挤反转**：净广度进入自身历史极值分位时反向（条件反转机制） | `trade_when(ts_zscore(divide(subtract(count_institutional_buyers_security, count_institutional_sellers_security), count_institutional_holders_security), 126) > 1.5, -rank(ts_zscore(divide(subtract(count_institutional_buyers_security, count_institutional_sellers_security), count_institutional_holders_security), 126)), 0)` | −（极值拥挤后反转） | **未测**（DEU 仅 mcp-20261029 留过 ts_quantile/signed_power 形态，无结果入库） |

补充（非骨架）：季频披露节奏 ⇒ 探针期建议 `ts_backfill(field, 252)` 前向填充兜底 + 平滑窗 ≥66d；T5/T6 的 0 分母用 holders/存量分母或 +1 平滑规避。`aggregate_share_count_all_owners` ≈ 总股本代理（全部持有人父子去重），DEU 先例 zq3wKxvG 已按此口径使用。

## 7. blockedFields（不可用/幽灵字段）

- **DEU 平台无幽灵**：11 平台字段全部可用（coverage 1.0）。以下为**本地 USA 画像**中的幽灵旧名（2026-10-25 入库，不在 2026-11-16 平台返回集内，任何表达式引用即平台 404/未知字段）：
  - inst6_value_held_by_institutions
  - inst6_value_held_by_owners
  - inst6_total_shares_held_by_institutions
  - inst6_total_share_held_by_owners
  - inst6_num_of_institutional_holders
  - inst6_num_of_institutional_buyers
  - inst6_num_of_institutional_sellers
  - inst6_num_of_institutional_shares_bought
  - inst6_num_of_institutional_shares_sold
  - inst6_value_of_institutional_shares_bought
  - inst6_value_of_institutional_shares_sold
- **配置层不可用**：D0 全集不存在（DEU/TOP500 delay=0 返回 0）；VECTOR/GROUP/EVENT 类型在本集不存在（集中度/HHI 轴不可构造）。

## 8. 模板验证（本轮实跑，非推断）

| 闸 | 命令/调用 | 结果 |
|---|---|---|
| 字段名（平台） | `mcp__wq-brain-http__validate_expressions(alpha_expressions=<§6 全部 8 条>, region="DEU", universe="TOP500", delay=1)` | `valid=true`, `unknown_fields=[]`, `fields_checked=10`；⚠ 带警告 `market_value_institutional_shares_acquired: get_datafields(offset=0): failed after 6 attempts` → 该次查名不完整，`platform_field_count=9` 是查名抖动，**不是**平台只有 9 个字段（§1 全量拉取为 11）；字段真实性以 §1 的 `complete=true` 全量为准 |
| 算子元数 | `python -X utf8 logs/_tmp_inst6_opcheck.py`（`wqb.expression.op_arity.check_expressions`） | `[arity] 8/8 PASS（签名表 101 个算子）`，`ok=True errors=0` |
| 历史回测读数 | `python -X utf8 logs/_tmp_inst6_deu_read.py`（`data/wqb.db` 只读） | 18 行，max sharpe 0.71，TO 0.0155–0.1033，waves={92:10, s2_institutions6_probe_r63_d1:8} |

**未跑（如实说明）**：8 条骨架**未做仿真**（本轮是 S1 字段档案，不是回测波次），故 §6 的符号方向全部只是机制预期，无一条有实测证据；`ts_backfill` 是否必要、T5 的 0 股数分母在 DEU 的实际 NaN 率，均需探针波实测。
