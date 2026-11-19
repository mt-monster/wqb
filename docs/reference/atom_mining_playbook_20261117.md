# ATOM 挖掘 playbook（2026-11-17 建立，源：外部文章 + 本仓实测交叉核验）

> 性质：**速查 / SOP**。原文：<https://mp.weixin.qq.com/s/1nhN8rmGF-gFvHSSHr2Y6A>
> （2026-11-17 访问时被微信「环境异常」验证页拦截；本文以仓库既有交叉核验稿为底稿，
> 并对「低换手 0.85 折扣」一条补了平台判别件 `YP1ZvjWA`）。本文只保留**经本仓数据核验**的部分，
> 并把「被本仓数据否掉 / 未复现」与「我们还不具备的能力」单列。**外部模板在入批前仍须过本仓静态闸与证据闸，且只作假设**。

## 一、直接可用（与本仓实测一致）

| 结论 | 本仓对应物 |
|---|---|
| ATOM = 全表达式只用**同一数据集**字段；仅豁免 6 个分组字段 `country / exchange / market / sector / industry / subindustry` | `atom-pyramid-rules`（隐形破 ATOM 清单同源） |
| **隐式破 ATOM 的三种写法**：① `convert()` / `inst_pnl()`（底层调 pv1 价量）；② 用 `cap / close / returns / vwap` 做 `bucket()`；③ `vector_neut(x, cap)` / `vector_neut(x, returns)` | 同上；**本文新增可操作替代**：用**主数据集自带的**市值字段造桶（例：`model26` 的 `mdl26_market_cap_u`），或干脆改用 Settings 里的中性化，不要在表达式里造桶 |
| ATOM 免 IS-Ladder，只查 2Y —— 单集件载体是 `LOW_2Y_SHARPE`，多数据集件走 `IS_LADDER_SHARPE(year=2)` | 平台回读结构一致（`effective=1` → LOW_2Y；`effective=2` → IS_LADDER） |
| **混 ≥3 个类别 ⇒ 金字塔计 0**；多类别混用时**倍率按最低的那个算（木桶短板）** | 与「跨 ≥3 塔不计点塔」「trio 内部禁混」同源；本文补上了倍率侧的机制解释 |
| 单字段 ATOM 能把「每 alpha 平均不同字段数」压到 1 | 与我们「一族一席 / 单腿」经验方向一致 |

## 二、✗ 不要照抄（本仓已否 / 未见）

### ✗1 「2Y 阈值 = 1.59」→ 实测是 **1.58**

- 平台 checks 实读：`gJaR5gov` 的 `LOW_SHARPE` 与 `LOW_2Y_SHARPE` 两条都打印 `limit = 1.58`；`RREALzx0` 报 `value 1.43 / limit 1.58`。
- 以 **`checks.fail` 的 limit 实读**为准，不用外部文章的数字。

### ✗2 「Turnover < 30% ⇒ 阈值 ×0.85（即 2Y 只需 1.35）」→ **本仓实测未见；按 1.58 执行**

- **判别件（2026-11-17 平台实读）`YP1ZvjWA`**：USA / TOP3000 / D1，**ATOM**
  （`group_rank(reverse(ts_decay_linear(ts_backfill(discount_store_retail_score,22),66)), sector)`，
  仅一个数据集 + 豁免 `sector`），TO **17.7%**（<30%）、2Y **1.57**。
  平台 `checks.warning` 里 `LOW_2Y_SHARPE`：`value=1.57`、`limit=1.58`、`ra_failed=true`。
  **若 ×0.85 成立，PASS 阈值应是 1.343，1.57 应 PASS 而不是 warning。**
- **前版引用的 `gJaR5gov` 不能作反例**：TO 5.39%、2Y **1.08** —— 1.08 同时低于 1.58 与 1.343，
  无法区分。`RREALzx0` 本地只有 `ra_failed_checks`、无原始 checks，也分不清 FAIL/WARNING。
- **ladder 载体同样未见折扣**：`WjP07oJN`（TO 25.6%、2Y 1.57）、`vRk6QNga`（TO 12.1%、2Y 1.57）、
  `rKjRj8qj`（TO 3.2%、2Y 1.57）均走 `IS_LADDER_SHARPE`，`limit=1.58`，判 fail/warning。
- **结论（scope：USA/TOP3000/D1 的 ATOM 判别件 + DEU/MEA 的 ladder 件）**：本仓**按无折扣执行**，
  近闸线用 **1.58**；不要用 1.34 当近闸线，否则会把 2Y 1.36–1.57 的件误当达标。
- 边界：这是 1 个 ATOM 判别件 + 3 个 ladder 件；其它区域/其它闸**未测**，不要外推成
  「平台没有这条规则」。若某区确要使用 1.343，必须先用该区 1.34–1.58 区间的 ATOM 件实测确认。

## 三、⚠ 未核实（方向可信，落地前必须实测）

### ⚠1 [Power Pool + ATOM] 不占纯 PP 每日 1 个配额

- 文中称：同时满足 Power Pool 与 ATOM（双标签）时不占「纯 PP 每天 1 个」限额，走 regular 的每日 4 个额度。
- **未在本仓验证**（我们的 `submit_verdict` / `get_daily_and_quarterly_payment` 侧没有这条判据）。
- 若要利用：先在 PPA 提交层用一条 ATOM 件实测当日配额计数，再决定是否把它当策略前提。

### ⚠2 Genius 六维 Tie-Breaker：avg distinct fields 低 + total distinct fields 高

- 战略含义（这是全文对我们最有用的判断）：**用「单字段 ATOM」扫新字段，同时压低平均值、抬高总量**。
- 与我们的「收割优先于重挖」「单腿优先」兼容：小批量单字段扫描 > 大批量多腿模板。
- 未核实「六维具体权重」，但不影响方向。

### ⚠3 ★ 选字段按 `dateCreated` 降序 + `alphaCount` 升序（**我们工具链缺这个能力**）

- 文章的核心洞察：**老数据集里 `alphaCount == 0` 的字段多半是死字段**（全平台几万人犁过，仍是 0 说明数据缺失或无信号）；
  真正白空间是**最近 1–3 个月新 onboard、coverage ≥ 0.8、倍率 ≥1.2x** 的字段，再叠 `alphaCount` 升序。
- **本仓现状（实读）**：MCP `get_datafields` 返回体只有 `id / type / coverage / userCount / alphaCount / description`
  —— **不含 `dateCreated`**。实测 `get_datafields(dataset_id="insiders1")` 8 条全部没有该字段。
  `dateCreated` 只在 alpha 侧用过（`world-quant-brain-mcp/brain_mixin_simulation.py:827` 的 `dateCreated>` 过滤、
  `tools/probe/probe_sa_candidates.py:279` 的排序），**datafields 侧零使用**。
- ✅ **已补齐（2026-11-17）**：根因不是平台不返回，而是 `mcp_core._slim_datafields` 把它裁掉了
  （原始 payload 实测含 `dateCreated` / `pyramidMultiplier` / `dateCoverage`）。现在：
  - `_slim_datafields` 透传 `dateCreated` 与 `pyramidMultiplier`；
  - `get_datafields` 新增 `sort_by`（`dateCreated` / `alphaCount` / `userCount` / `coverage` / `pyramidMultiplier`）、
    `sort_order`（`asc`/`desc`，缺省按字段给合理方向：dateCreated→desc、alphaCount/userCount→asc、coverage/倍率→desc）、
    `min_coverage`（本地过滤）；
  - 排序**全在本地做**（字段已全量拉取），不额外打平台；返回体回显 `sorted_by` / `sort_order` / `min_coverage` /
    `returned` / `ordering_scope`；`count` 仍是平台总数。
  - 守卫：`world-quant-brain-mcp/tests/test_datafields_ordering.py`（8 例）。
  - ⚠ 用法纪律：**缺失值恒排最后**（不因升降序翻转）；`sort_by` 传非法值会返回 `{"error": ...}` 而不是静默忽略。
- 标准用法（找蓝海字段）：`get_datafields(region, dataset_id, universe, sort_by="dateCreated", min_coverage=0.8)`
  → 取头部 = 最新 onboard 且覆盖达标；再看 `alphaCount` 挑最冷门的。
- ⚠ **运行中的 MCP 服务需重启才暴露新参数**：代码虽已改，但当前常驻 `wq-brain-http` 进程的工具 schema
  仍是旧签名（实测 `get_datafields` schema 无 `sort_by` / `sort_order` / `min_coverage`）。
  未重启前 MCP 调用只能用旧参数；重启后再按上面的标准用法。改 `world-quant-brain-mcp/` 后需重启是
  `AGENTS.md` §3 的既有纪律。

### ⚠4 文中 4 条单字段 ATOM 模板（只作候选，不许直接抄）

```
① group_rank(ts_mean(F,20) / ts_mean(F,120), subindustry)     // 长短均值比（边际变化）
② group_neutralize(ts_zscore(F,60), subindustry)              // 时序标准化 + 组内中性
③ ts_decay_linear(-ts_rank(F,252), 10)                        // 一年期分位反转（低换手）
④ group_rank(ts_delta(F,20) / ts_std_dev(F,60), sector)       // 差分÷自身波动（单字段 SNR）
```
- ②④ 与我们既有杠杆重叠（zscore 量级形态、SNR 腿）；①③ 是新的。
- **入批前必须**：过 `gate.py`（含幽灵算子/量纲/窗口）、过本仓证据闸、区内小批符号指纹校验（跨区不外推）。

## 三bis、KOR 负面校准（2026-11-17，文章方法实测）

**结论：`dateCreated` 法能找到真蓝海字段，但「新字段 ⇒ 简单模板即可过检」在 KOR 未复现。**

- 选集：`fund_holdings_panel`（KOR institutions 塔 0/3 未亮）全 30 字段 `dateCreated=2026-03-01`、
  coverage 0.66–0.96、aC 0–35、倍率 1.4 —— 完美命中文章的「新 onboard + 高覆盖 + 低 aC」白空间签名。
  对照 `institutions6`（2025-10-01，aC 59–259）明显拥挤。
- 实测：文章四套单字段模板 × 10 字段（SLOW/d2，批次 `2vE76b28m50scGmHFkMIbsV`）**10/10 REJECT**。
  ① 5 条 MATRIX 持仓/集中度水平族 S −0.51…−0.01（cov 0.95，非覆盖闸，纯信号不存在）；
  ② 5 条 VECTOR 逐日交易事件族 3 条 TO 0.96–1.20 爆换手、2 条 2Y≈0.69 但全期 S 为负（符号跨期不稳）。
- **可复用教训**：`dateCreated` 是**选字段的必要筛**（排除 aC==0 死字段），不是**过闸的充分条件**；
  文章模板在 USA dense 字段上成立，在 KOR institutions 这类**机构持仓低频水平 / 逐日事件计数**上不成立。
  模板 1/4 的除法对逐日事件计数尤其敏感（TO 爆表），须先回到「字段的时间结构」（水平/差分/事件）
  再选模板，别照抄。详见 `tracking/KOR/campaign_20261117_news_regular/README.md` §4 W4 归因。

## 四、行动清单

1. **立即纠正口径**：任何近闸判断里删掉「低换手 0.85 折扣」；2Y 阈值一律以 `checks` 实读为准（DEU = 1.58）。
2. **工具已补齐**（2026-11-17）：`get_datafields` 已支持 `sort_by=dateCreated|alphaCount|coverage|pyramidMultiplier`
   + `min_coverage`；**运行中的 MCP 服务需重启**才暴露新参数（未重启前 schema 仍是旧三参）。
3. **策略**：新数据集进场时优先「单字段 × 4 模板」小批扫描（Genius 维度 + 倍率 + prod 低相关三重优势），
   而不是一上来就多腿组合；单字段立住之后再谈加腿。
4. **纪律不变**：`atom-pyramid-rules` 的隐形破 ATOM 清单、`AGENTS.md` §7.6 的六维判死闸、跨区不外推，全部优先于本文。
5. **政策优先**：ATOM 优先 / 穷尽举证后才 regular 跨集 / 跨集只许 gating·grouping·residual·ratio /
   `add` 等权混腿仍禁 —— 见 `AGENTS.md` §7.7 与 `methodology_rules.json::atom_first_regular_fallback_v1`。
   本文只补充字段选择与模板，不改变政策。

## 五、证据索引

- **2Y 折扣判别件（决定性）**：`YP1ZvjWA`（USA/TOP3000/D1，ATOM 单数据集，TO 17.7%、2Y 1.57；
  `checks.warning.LOW_2Y_SHARPE = {value:1.57, limit:1.58}`，`ra_failed=true`）—— 若 ×0.85 成立，
  1.57 应过 1.343；实际仍是 warning ⇒ 本仓按 **1.58** 执行。
- **ladder 载体对照**：`WjP07oJN`（TO 25.6%、2Y 1.57）、`vRk6QNga`（TO 12.1%、2Y 1.57）、
  `rKjRj8qj`（TO 3.2%、2Y 1.57），均 `IS_LADDER_SHARPE limit=1.58` 判 fail/warning。
- **不可用作判别的前版读数**：`gJaR5gov`（TO 5.39%、2Y 1.08，低于 1.58 与 1.343，无法区分）、
  `RREALzx0`（本地只有 `ra_failed_checks`、无原始 checks，分不清 FAIL/WARNING）。
- `get_datafields` 排序/过滤实现：`world-quant-brain-mcp/tools_data.py::_order_fields`（2026-11-17）；
  `_slim_datafields` 透传 `dateCreated`/`pyramidMultiplier`；守卫 `test_datafields_ordering.py`。
- datafields 返回体实测：`get_datafields(dataset_id="insiders1", region="DEU", universe="TOP500", delay=1)` → 8 条，无 `dateCreated`。
- ATOM 定义与隐形破清单：`atom-pyramid-rules` 记忆条目；`tracking/DEU/atom_orthogonal/ATOM_OFFICIAL_DEFINITION_AND_GATE5_REVISION_20261112.md`。
- 单腿/一族一席：`Claude/skills/wq-brain-ra-deu/references/_effective-levers.md`。

## 三ter、DEU 全分母校准（2026-11-18，55 集 / ≈3,900 字段实读）

**结论：`dateCreated` 选字段法在 DEU 结构性失效——全区分母上零区分度。**

- 分母 = DEU/TOP500/D1 的 **11 个未点亮塔类别**（insiders 2 / institutions 5 / sentiment 3 / news 17 /
  option 1 / pv 16 / earnings 2 / macro 1 / risk 5 / socialmedia 2 / imbalance 1）= **55 个数据集**。
- 实读结果：**55/55 数据集、全部字段 `dateCreated` = 2026-07-01**，早于/晚于该日者 **0 条**
  （user 追问「只扫 6 个候选集吗」后由两个只读子代理补全；首轮 6 集 = 目标塔分母 2 + 备选集 4，属口径错误）。
- ⇒ 该区字段是一次性整批导入，**「近 1–3 月新 onboard」这一白空间签名在 DEU 不存在**；
  「老 + `alphaCount==0` ⇒ 死字段」也随之失效（aC==0 占 60.3%，绝大多数是 timestamp / flag / metadata）。
- **补扫带出的真白空间是「覆盖 × 使用」**：`pattern_scores` 504 字段 cov ≥ 0.9647（aC 最大 36）、
  `pv29` 50 字段全 cov ≥ 0.8、`fund_holdings_panel`（DEU）18 字段全 ≥ 0.8、`news104` 11 字段 cov 0.963。
- **13 个数据集挂牌但零覆盖**：news21 / news23 / news29 / news3 / news31 / news52 / news54 / news7 / news73 /
  news76 / news81、earnings6、earnings_sent_matrix（数据集级与字段级 cov 同为 0.0）。
  ⚠ **不要把 cov=0 当死集**（2026-11-18 用户纠正）：对这 13 集派 23 条探针臂，**23/23 全部跑出真实 PnL**
  （TO 0.07–1.69、drawdown 与 returns 均非零）⇒ coverage=0 是元数据/展示层问题，**不等于无数据**。
  最好的三条：`news7` `ts_delta(earnings_news_mention_count,22)` S 0.71 / F 0.43 / **TO 0.068** / 2Y 0.97
  （invest_S −0.51，容量待查）；`news21` `ts_zscore(subtract(nws21_pos_sc,nws21_neg_sc),60)` S 0.61 / 2Y **1.17** / TO 0.87；
  `news21` `ts_zscore(nws21_pos_sc,60)` S 0.49 / 2Y 0.84。earnings 两集也各有非零读数（S 0.08 / 0.30）。
  ⇒ 「零覆盖 ⇒ 排除」的捷径作废，**判死前至少跑一条探针臂**（与 AGENTS §7.6 判死纪律同源）。
- ⚠ 方法限制：`continuation_score`(560) / `intraday_pv_feats`(585) / `pv20`(681) / `pattern_scores`(504) / `pv30`(285)
  五个大数据集单次响应超 50 KB，改用 `sort_by=dateCreated` 的 asc/desc 双端探针证明「单值」；
  这三处 `alphaCount==0` 计数**不可精确读**，已标不可读，未估算。
- **口径教训**：任何「本区全部数据集 / 没有白空间」的措辞，必须先拿平台 `/data-sets` 按
  (region, universe, delay, category) 的全表分母，再逐集实读——与 AGENTS §8.11 同源。
