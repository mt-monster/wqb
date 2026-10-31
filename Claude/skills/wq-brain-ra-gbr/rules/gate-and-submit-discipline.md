# GBR 提交前闸门纪律（gate-and-submit-discipline）

> **as_of**：2026-10-31 ｜ 手写区，SKILL.md / `references/<category>.md` 重渲不会覆盖它。
> **定位**：GBR 独有 + 本轮实证的**提交前五道闸**执行顺序。通用九步在 `../../wq-brain-ra-pipeline/SKILL.md`。
> **证据源**：`docs/reference/gbr_submit_execution_pack_20261031.md`（21 条提交组）· `docs/reference/GBR/field_mechanism_map_20261031.md`（字段通道地图）· `docs/reference/template_library_gbr_news_strong_geometry.md`（十模板波 / 五轮收割归因）。

---

## 0. 一句话

**候选「看起来全绿」不等于可提交。** 本区 21 条提交组里，台账标全闸、prod 实测 < 0.7、self < 0.7 的候选里，仍有 **5 条被拦下**（3 条数据不满十年 / 1 条挂 robust 闸 / 1 条近重跑）。**五道闸必须按序全跑。**

---

## 1. 五道闸（顺序不可换）

| # | 闸 | 工具 | 成本 | 漏掉会怎样 |
|---|---|---|---|---|
| **1** | **台账排除** | `grep -r "<dataset_id>" docs reports Claude/skills` → 读「已证伪 / 判死 / 失败边界」章节，把已测骨架当**排除表** | 零 | 直接踩已证伪形态（本轮：F 腿用水平毛利率 ⇒ 10 模板全灭） |
| **2** | **RA 闸 + 塔位** | `batch_get_alpha_metrics`（平台权威 `failed_ra_count`）+ `get_alpha_details`（`checks.fail` / `pyramids.list`） | 零配额 | 本地 `alphas.failed_ra_count` 是**旧快照**（本轮某条本地记 0、平台实读 3 闸） |
| **3** | **近十年** | `get_alpha_yearly_stats` 逐年核 `longCount>0` 且 `shortCount>0` 且 `pnl>0` | 只读 | **数据不满十年**的 alpha 全期指标很漂亮（本轮 3 条：S 1.66–2.45 / prod < 0.55） |
| **4** | **self-corr** | `check_self_correlation`（对**本区** OS 池） | 本地计算 | 5 条「神候选」（S 4.73 / 4.64 / 2.90 / 2.00 / 1.92）会被误当高质量提交并全部撞墙 |
| **5** | **篮内互相关 + 配额** | `compute_mutual_correlation` + 塔位组合计数 | 本地计算 | 同族只能取 1–2 条；PV+FUND 会超「单组合 ≤3」 |

**顺序理由**：② 先于 ③（否则把数据不满十年的当优质候选）；④ 先于 ⑤（重跑项会污染最大团计算）。

---

## 2. 第 2 闸的两个细则

### 2.1 `checks.fail` 是唯一判闸依据

- `get_alpha_details` 的 `checks` 段给 `fail` / `warning` / `pass` / `pending` 四个**名字数组**，**不附 limit 数值**（limit 只在 fail 条目的 `value`/`limit` 里）⇒ 想反推线（如 `LOW_SUB_UNIVERSE_SHARPE = 0.478 × S`）只能去读**曾经 fail 过**的同 check 条目。
- **`IS_LADDER_SHARPE` 带 `"year": N`** 时会出现在 `fail` **或** `warning` 里 ⇒ **warning 也计入 `failed_ra_count`**，不能只看 `fail` 名单长度。
- `failed_ra_count` 只是**计数**，不告诉你挂在哪 ⇒ 必须逐项读 `checks.fail`。

### 2.2 `LOW_ROBUST_UNIVERSE_SHARPE` 是**分区下发**的

| 区 | universe | `checks.pass` 里是否出现 robust 闸 |
|---|---|---|
| **GBR** | TOP700 | **从不出现**（平台不下发 ⇒ 不可能挂） |
| EUR | TOPCS1600 | 出现 |
| IND | TOP500 | 出现 |

⇒ **跨区候选必须逐条读 `checks.fail`**，不能拿 GBR 的闸清单去套。本轮实测：`mLjnnzKE`（IND）本地全绿，平台实读 `LOW_ROBUST_UNIVERSE_SHARPE 0.82 < 1.0` ⇒ 不可提交。

---

## 3. 第 3 闸的细则（本区特有）

**判「近十年有数据」只看三列，逐年核**：`longCount > 0` 且 `shortCount > 0` 且 `pnl > 0`。

- **不看平台 `coverage`**：本轮 3 条被剔全部是 coverage 正常但**逐年零持仓**——
  `omWVZ7lm`（EUR）2014–2019 六年 0、`9qxP0JbV`（USA）2014–2018 五年 0 ⇒ 对应数据集在那些年份**没有数据**。
- 逐年 S 允许为负吗？**不允许**（本轮 `pwv9eM76` IND 2015 年 S −0.26、pnl 为负 ⇒ 剔）。
- 本地库**没有逐年表**（`alphas`/`backtest_results` 都没有 year 列）⇒ 只能走 `get_alpha_yearly_stats`。

---

## 4. 第 4 闸的细则：self-corr 判据分两层

| 区间 | 含义 | 动作 |
|---|---|---|
| **> 0.7** | **提交红线**，超了不可提交（不管指标多好） | **剔** |
| **≥ 0.99** | 「是重跑还是同族变体」的**分类阈值** | 判剔的理由（重跑 vs 同骨架换参数） |
| 0.7 – 0.99 | 同族不同参数/结构 | 剔（同样不可提交） |

**两条实战判例**：
- `rKe5L9q3` vs 已提交 `gJZQZkZe` = **0.9933** ⇒ 近重跑（只差一层 `last_diff_value`）。
- `zqbYwOmV` vs `gJZQZkZe` = **0.9411** ⇒ **同骨架只差平滑窗 100→120** ⇒ 不是重跑，但照样超线。
  ⇒ **0.99 门槛过严**；真正决定能不能提交的是 **0.7**。

**OS 池按区隔离**（实测 `pool_size` / `full_os_pool_size`）：GBR 18–21 · EUR 10–15 · IND 52–60 · USA 135–140。
⇒ **池小的区 self 门槛天然更松**（EUR 只有 12 条 OS ⇒ 跨区补量时 EUR 更容易过）。

---

## 5. 第 5 闸的细则：配额核算（按区独立）

| 规则 | 口径 | 本轮实证 |
|---|---|---|
| **trio 内部禁混** | `PV` / `MODEL` / `OTHER` 三者之间**不得两两组腿**（含 `PV+PV`、两个 MODEL 集互组） | 本轮 21 条**零违规** |
| **单两塔组合 ≤ 3** | 同一「数据集组合」的候选 ≤ 3 | GBR 的 PV+FUND **恰好 3 条卡线**（`rKRkL9QE` / `WjOkLGWx` / `leAJn9e2`） |
| **trio×非trio ≤ 5** | 含 trio 字段的非单塔组合总量 ≤ 5 | GBR 3 · EUR 1 · IND 1 · USA 0 |
| **单塔不吃配额** | 纯 FUNDAMENTAL / MODEL / ANALYST / NEWS / INSTITUTIONS / SHORTINTEREST 单塔 | ✓ |

**★ 塔位杠杆（最重要的一条）**：
- `current_enterprise_value` 是 **`fundamental17` 集内**字段（描述含市值但**归属 fundamental**）
  ⇒ `divide(<科目>, current_enterprise_value)` = **纯 FUNDAMENTAL 单塔**，不碰 PV 的 `cap`、**不吃任何 trio 配额**。
- 分母用 `cap`（PV 集内）⇒ 变 **PV+FUND 双塔**，吃上述配额。
- ⇒ **要单塔就选集内市场量当分母**。

---

## 6. 收割纪律（本轮最大增量）

**★ 「prod 未知」多半是检索盲区，不是平台阻塞。**

本区曾把 `check_correlation` 试到超时（3 轮 × 241s、每轮 180+ 次轮询全空响应）后判「平台侧 prod 队列不推进」——
**其实本地 `alphas.prod_correlation` 早存着平台实测值**。

```sql
SELECT alpha_id, region_id, universe, dataset_id, sharpe, fitness, two_year_sharpe,
       sub_universe_sharpe, prod_correlation, self_correlation, turnover, status, expression
FROM alphas
WHERE stage = 'IS'
  AND prod_correlation IS NOT NULL AND prod_correlation < 0.7  -- 见 config.PRODCORR_CEILING
  AND (status IS NULL OR status NOT IN ('ACTIVE','SUPERSEDED'));
```

⇒ **本区一次返回 31 条**（全库 180 条：EUR 29 / USA 30 / IND 59 / GBR 31）。
⇒ **零仿真配额**地把候选池从 14 条扩到 34 条，再跨区到 **21 条五道闸全过**。

**配套纪律**：
1. 本地 prod 是**筛选器不是终验**（平台 prod 池 2–3 天可从 0.58 漂到 0.98）⇒ 提交前仍须 `check_correlation(refresh=True)` 当场终验。
2. `prod_corr_source` 字段区分 `platform_sync`（权威）/ `manual` / `triage_local` ⇒ 按 source 分层读，别把本地估算当平台值。
3. **★ prod 墙是族属性**：同一字段族的 prod 命中率一致 ⇒ **选族优先，选几何次要**。本区已验证通道见 `field_mechanism_map_20261031.md` §2。

---

## 7. 提交链与执行顺序

1. **先提 GBR 15 条**（点 3 塔：PV 1→4 / FUNDAMENTAL 0→4 / NEWS 0→5），产出最快。
2. 逐条当场观察平台 prod 判定；**撞墙的当场从 47 条合格替补池**（`results/backup_screen_20261031.json`）按「族不同 + 塔位合规」顶上。撞 prod **非破坏性**（平台拒收、alpha 保持未提交、不消耗塔位与配额）。
3. 再提 EUR 2 → IND 1 → USA 3。
4. 每条：`check_correlation(refresh=True)` → `set_alpha_properties`（name/tags/descriptions 见 `gbr_submit_execution_pack_20261031.md`）→ `workflow_submit_alpha(confirm_submit=True)`（**须用户确认后执行，不可逆**）。
5. **提交动作必须用户明确确认**；问卷超时自动选中**不算**确认。
6. 命名/标签规范：`<REGION>_R_<family>_<NN>`（禁含 PROD 数值）；tags = `CH_<通道>` + `SRC_<数据集>` + `EXPRFAM_<族>`（≤5）。

---

## 8. 本区已知数据面边界（避免重复踩）

| category | GBR 状态 | 关键依据 |
|---|---|---|
| **NEWS** | ✅ 可点亮（5 轴，最多 5 条） | `news17` / `news18`；`news104` `news20` `news38` `news50` 判死；**强几何才有货** |
| **FUNDAMENTAL** | ✅ 可点亮（`fundamental6` + `fundamental17` 两通道） | 其余 10 个集 cov 0；`fundamental45` cov 0.27 |
| **PV** | ✅ 可点亮 | `pattern_scores`（`MPY96E7o`）· `pv47`（**prod 族级封盘**）· `pv29`（簇标签）· `pv30` |
| **SHORTINTEREST** | ⚠ 仅 1 条（`akK2vpWW`） | `shortinterest3` 1 活字段、无兄弟集 |
| **INSTITUTIONS** | ❌ 结构性不可达 | `fund_holdings_panel` 24 探针 · `institutions6` 天花板 0.56 · `institutions4` 是标识符映射 · `institutions25` cov 0 · **`institutions1` 本轮 4 探针全灭** |
| **INSIDERS** | ❌ | `insiders1` / `insider_agg_matrix` 15 探针全灭（TO 0.016–0.06 近静态） |
| **EARNINGS** | ❌ | `earnings6` / `earnings_sent_matrix` cov 全 0 |
| **SENTIMENT** | ❌ | `sentiment7` 覆盖不足致 SUB 结构性失败 · `sentiment33` `sentiment27` `sentiment21` |
| **ANALYST** | ⚠ 已点亮 3–4 条 | `analyst7` 的 **est_breadth 形式存活**（`gJZQZkZe` ACTIVE）、**pre/revision 形式衰减**；`analyst9` `analyst47` `analyst_factor_signals` `analyst93` 判死 |
| **MODEL** | ⚠ 已点亮 5 条 | `mdl28` / `model109` / `predictive_starmine` 通道可加固 |
| **RISK / MACRO / OPTION / SOCIALMEDIA / IMBALANCE / OTHER** | ❌ / 已点亮 | `risk88` `risk60` `macro27` `option_chart_model` `socialmedia39` `imbalance5` `other455` `dl_riskfree` 均判死 |

> ⚠ **判死标记一律不得单独作为依据**：本轮实测 `registry_empirical.family_dead_datasets` 把 `fundamental17` / `news17` / `news18` / `fundamental6` / `shortinterest3` 全列为死集，**而这些集本轮仍在出货全闸候选**。以平台实测为准。
