# GLB / D1 十塔点塔矩阵（Q4 2026-10-01 ~ 12-31）

> 生成：2026-10-02（v3，区域口径修正版）
> 目标：**点亮 10 座塔** = GLB/D1 的 13 个 category 中，≥10 个各达 **3 颗 ACTIVE REGULAR**
> 权威源：平台 `get_pyramid_alphas` / `get_mining_yield`；库 `s1_triage_glb` + `registry_empirical` + `backtest_results(按 region 过滤)`

---

## 0. 关键事实（全部平台/库内核验）

| 项 | 值 | 来源 |
|---|---|---|
| **GLB/D1 Q4（当前）塔计数** | **0/13 全为 0** | `get_pyramid_alphas` |
| GLB/D1 Q3 塔计数 | pv:5, other:3（2 塔曾点亮） | `get_pyramid_alphas(start=2026-07-01)` |
| 已有 ACTIVE REGULAR | **10 颗，全 Q3 提交 → Q4 记 0** | `alphas` 表 |
| 已有 10 颗归属 | `dl_riskfree_returns`×6 + `_unknown`×4 → 落 **OTHER** 塔 | 表关联 |
| **prod 墙（头号约束）** | `prod_wall_ratio` **81%**（prod_blocked 81 / prod_clean 19） | `get_mining_yield GLB` |
| 挖矿转化 | 8325 expr → 2154 bt → 168 pass → ra_clean 157 → **prod_clean 仅 19** | 同上 |
| 判死账 | **40 个数据集** 判死，覆盖 **11/13** category | `registry_empirical` dead_end |
| TRI 闸 | `block=true` 118 集 / `block=false` 仅 **28 集** | `s1_triage_glb` |
| S1 幸存（可开波） | **17 个** | `s1_triage_glb.survivors` |
| 配额 | REGULAR 4/ET 日；ET 2026-10-01 已用 5/4 → **12:00 GMT+8 重置** | `quota_status.py` |

**根因**：金字塔按季度重置，Q4 从 10-01 起算；已有 10 颗全落 Q3 → 对 Q4 贡献 0。本季须新提 30 颗。

---

## 1. ★★★ 区域口径修正（v3 最重要的更正）

**v2 曾误把「跨区回测」当成「已在 GLB 测过」。按 `backtest_results.region` 过滤后真相如下：**

| S1 幸存集 | GLB 本区回测 | 其他区回测（不算数） |
|---|---|---|
| **model38** | **729 条，maxS 2.08** | — |
| analyst69 | **0** | JPN:16/maxS1.41 |
| analyst11 | **0** | AMR:64/0.83; ASI:6/0.27; EUR:8/0.43 |
| analyst_earnings_ibes | **0** | DEU:115/**2.17**; GBR:3/1.7 |
| global_seasonal_model | **0** | ASI/EUR/IND/JPN（最高 1.24） |
| other335 | **0** | GBR:15/1.13 |
| macro27 | **0** | GBR:11/0.49 |
| model110 | **0** | GBR:5/0.75 |
| other432 / model31 / model239 / model243 / pv13 / pv53 / earnings7 / other551 / ai_factor_transfer | **0** | — |

**⇒ 结论：17 个幸存集中，16 个在 GLB 本区从未测过 → 全部是真正的新领土。** 判死账只覆盖旧数据集；S1 幸存集是 2026-09-30 triage 新筛出的、GLB 上的白空间。

---

## 2. 13 category 可行性（判死账 × TRI 闸 × GLB 本区实测 三重交叉）

`✗ 判死` = 塔下已知数据集全判死；`○` = 有 GLB 未测幸存集。

| # | category | mult | GLB 未测幸存集 | 判定 |
|---|---|---|---|---|
| 1 | **analyst** | **1.4** | analyst69(779f)、analyst11(235f) | **○ 主战场**（GLB 零回测 + 最高乘数） |
| 2 | **model** | 1.3 | model110、model31、model239、model243、global_seasonal_model、analyst_earnings_ibes、ai_factor_transfer、**model38**(已测,2.08) | **○ 候选最多** |
| 3 | **other** | 1.3 | other335、other432 | **○**（Q3 已亮 3 颗，新机制仍可） |
| 4 | **macro** | 1.1 | macro27、other551(→MACRO) | **○ 窄路** |
| 5 | **earnings** | 1.1 | earnings7（唯一） | **△** |
| 6 | **pv** | 1.0 | pv13、pv53 | **△**（Q3 已亮，乘数最低） |
| 7 | **fundamental** | **1.4** | —（f17/23/28/44 判死；f31/6/72 TRI block=true） | **✗ 判死**（需人工豁免） |
| 8 | **news** | 1.3 | —（news17/23/31/52/73 判死；news20 TRI block=true） | **✗ 判死**（需人工豁免） |
| 9 | **risk** | 1.0 | —（risk60/68/70 判死；risk66 仅 2 字段） | **✗ 判死** |
| 10 | **sentiment** | **1.4** | —（snt21/22/26 + other553 判死） | **✗ 判死** |
| 11 | **institutions** | 1.1 | —（institutions6 判死；inst18 TRI block=true） | **✗ 判死**（需人工豁免） |
| 12 | **insiders** | 1.1 | —（GLB 仅 insider_agg_matrix，已判死且无第二集） | **✗ 判死（不可行）** |
| 13 | **socialmedia** | 1.1 | socialmedia12（TRI block=false，「仅条件腿」） | **△ 极窄** |

**⇒ TRI 通过且未判死 = 6 座塔**（analyst / model / other / macro / earnings / pv）。

---

## 3. 用户决策：守 GLB + 判死复审 4 探针

**判死复审的诚实评估**（原设想已被推翻）：

| 原设想 | 核验 | 结果 |
|---|---|---|
| sentiment21 未开波 | ❌ **已开波** `ws2_snt21_probe_d1` 8 条 maxS 1.05 ra=0 → 判死 | 失效 |
| fundamental 事件型变化率 | f17 已全族判死；f31/f6/f72 TRI block=true | 需人工豁免 |
| news 首次覆盖 | news17/23/31/52/73 判死；news20 TRI block=true | 需人工豁免 |
| risk70 冷门因子 | ❌ 已开波 maxS 2.16 ra=1 判死；risk66 仅 2 字段 | 失效 |

**⇒ 判死复审后实际可新增的塔 = 最多 3 座**（fundamental / news / institutions，均需 `--skip-triage-gate` 人工放行）。
**⇒ 现实上限 ≈ 9 塔**（6 主 + 3 复审）；10 塔需 4 座靠豁免，命中率低。

---

## 4. 最终执行方案

### 第一梯队（6 座可行塔，无需豁免）

| 塔 | mult | 首波数据集 | 骨架方向 | prod 规避 |
|---|---|---|---|---|
| **analyst** | 1.4 | **analyst69(779f) / analyst11(235f)** | GLB 零回测 → 走**修正速率/惊喜**（非水平非共识） | 避 consensus/targetprice 水平族 |
| **model** | 1.3 | **model110 / model31 / model239 / model243** | 换机制轴（model38 已测机制不再投变体） | — |
| **other** | 1.3 | other335(5f) / other432(345f) | 单信号结构化（拒绝 add 混腿） | dl_riskfree 族一律不碰 |
| **macro** | 1.1 | macro27(33f) / other551 | 宏观-个股传导（非回归残差） | macro_equity_signals 残差族已判死 |
| **earnings** | 1.1 | earnings7(8f) | 事件后漂移（非日历临近） | 避 earnings3 日历族 |
| **pv** | 1.0 | pv13(56f) / pv53(9f) | 与 intraday_pv_feats 已点 3 座正交 | pv98/pv106 判死 |

### 第二梯队（判死复审，需 `--skip-triage-gate`）

| 塔 | 数据集 | 探针机制轴 |
|---|---|---|
| fundamental | fundamental72(896f) | 季度公布日事件型 + **非变化率/ratio 的全新机制轴** |
| news | news20(24f) | **首次覆盖/事件起始**（非计数非语调） |
| institutions | institutions18(6f) | 基金持仓**变动率**（非水平）；跨区强 USA:6 |
| socialmedia | socialmedia12 | 仅作条件腿（buzz/sentiment 门控） |

**不可行**：`insiders`（GLB 仅一个集）、`risk`、`sentiment`。

---

## 5. 执行顺序

**Phase 1（6 主塔）**：analyst → model → other → macro → earnings → pv，每塔 3 颗。
**Phase 2（3-4 复审塔）**：fundamental72 → news20 → institutions18 → socialmedia12。
**Phase 3**：攒批等配额 → 提交 → `get_pyramid_alphas` 复核。

每波：S1 triage → S2 GEM → S5 wave_gate → S6 回测 → S6 台账回写（步9）。
**组合形态铁律**：本批严禁 `add(rank(A),rank(B))` 类加权混腿（analyst_earnings_ibes 在 DEU 的 2.17 即是此违规形态，不可照搬）——必须单信号结构化（`ts_scale` / `group_rank` 差值 / 门控 / trade_when）。
