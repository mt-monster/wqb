# GBR REGULAR Alpha 挖掘战役报告（目标 10 颗）

> 日期：2026-10-08　区域：GBR / D1 / TOP700　执行：按 `docs/reference/field_profile_to_alpha_playbook.md` 七层链路
> 关联：skill 已按 playbook 改造 → `Claude/skills/wq-brain-ra-gbr/SKILL.md` v1.1（+ `references/_field-profile-playbook.md`）

---

## 一、战役目标与达成情况

| 项 | 状态 |
|---|---|
| **目标** | 挖掘 **10 颗** REGULAR alpha |
| **本轮达成** | **5 颗** IS 全闸 + `failed_ra=0`（均为 `pv47` / PV 族） |
| **剩余** | 5 颗 —— 已有明确续波方向（见 §六） |
| **提交** | **未提交**（提交权归用户；`XgJRmOG5` 等已备齐证据待授权） |

---

## 二、Agent 侧流程改造（用户指定）

`Claude/skills/wq-brain-ra-gbr/SKILL.md` **v1.0 → v1.1**，把 playbook 的**七层链路**钉进 GBR 分支：

| 改动 | 内容 |
|---|---|
| 「怎么用」步骤 0 | 先读方法论主文；**七层 = 想什么，九步 = 怎么做** |
| 新增大节 | **字段画像驱动流程（七层 → 九步映射表）**，含 verdict 九类处置表（带 GBR 实测规模）、跨区对照、第 3 层合规模板、**第 4 层「结构维度 > 参数维度」**、第 6 层判定口径（含 **prod/self 双端点**） |
| 新增补充文档 | `references/_field-profile-playbook.md`：GBR 画像总览 + verdict 分布 + ALIVE 19 / WEAK 9 全表 + 战役目标优先级 |
| 校验 | `wqb.profiles check` = 0 问题；`sync_skills.py` 同步 6 安装位全 OK；治理/文档指针无新增死链 |

**改造带来的直接效果**：本轮**开波前先查画像 ALIVE/WEAK**（第 1 层），因此准确锁定 `pv47`（`pv47_spret` ALIVE S1.69/2Y2.07/**F0.98**，仅差 0.02）而不是继续在已判死的池上烧配额。

---

## 三、执行轨迹（9 波 / 72 条仿真 / 零连坐）

| 波 | 目标 | 结果 |
|---|---|---|
| a47w1 | `analyst47` 结构波（基线复现 + `ts_decay_linear` + 幂次 + 换量纲 + 换字段/未测字段） | 基线**精确复现**（S1.95/F0.96/2Y1.75）；无全闸 |
| **pv47w2** | **`pv47` 结构波（按画像 ALIVE）** | ★ **1 颗全闸**（`XgJRmOG5`） |
| fh_w3 | `fund_holdings_panel`（INSTITUTIONS，9 个未测 `_active` 字段） | **8/8 全负**（S −0.58 ~ 0.01）⇒ 该族判弱 |
| a47w4 | `analyst47` 精调（轻 decay / 紧裁剪 / 换窗） | 无全闸（F 天花板 0.94–0.96） |
| a7w5 | `analyst7` `act_q_*_surprisenum`（8 指标族白空间） | **8/8 弱**（S 0.08–0.42）⇒ 判死 |
| **pv47w6** | **`pv47` 深挖（decay 档位系统化 + 换轴 + 换字段）** | ★ **4 颗全闸** |
| a47w7 | `analyst47` 攻 F（`hump` / `ts_mean` / 长 `ts_decay_linear`） | 无全闸；**`hump` 直接把信号杀掉**（S1.96→0.40） |
| news_w8 | `news17/20/18` VECTOR 情绪分（新 category） | **8/8 弱**（S −0.21 ~ 0.23）⇒ 判弱 |
| a47w9 | `analyst47` 用 `ts_target_tvr_decay` 精确压 TO | 无全闸；**压 TO 同时压塌 2Y**（8/8 `2Y_DEAD`） |

---

## 四、★ 战役成果：5 颗全 IS 闸候选（PV 族）

全部满足 **S ≥ 1.58 ｜ F ≥ 1.0 ｜ 2Y ≥ 1.58 ｜ TO ∈ [0.05, 0.30]**，且 **`submit_verdict` 判 `UNVERIFIABLE_404`（处女形态，非 BLOCKED）**、`Failed RA = 0`。

| # | alpha | 表达式 | S | F | 2Y | TO |
|---|---|---|---:|---:|---:|---:|
| 1 | **`akxVZdN6`** ★最佳 | `-ts_decay_linear(rank(ts_quantile(ts_sum(pv47_for_statssimple_only_spret,22),252)), 5)` | **1.70** | **1.06** | **2.07** | 0.1328 |
| 2 | `XgJRmOG5` | `-ts_decay_linear(rank(ts_quantile(ts_sum(pv47_spret,22),252)), 8)` | 1.66 | 1.05 | 1.87 | 0.1218 |
| 3 | `A1vQZwaX` | `-ts_decay_linear(rank(ts_quantile(ts_sum(pv47_spret,22),252)), 5)` | 1.68 | 1.04 | 1.99 | 0.1324 |
| 4 | `3qVjr7ne` | `-ts_decay_linear(rank(ts_quantile(ts_sum(pv47_spret,22),252)), 3)` | 1.68 | 1.01 | 2.03 | 0.1416 |
| 5 | `omWo5K92` | `-ts_decay_linear(rank(ts_quantile(ts_sum(pv47_spret,22),252)), 12)` | 1.61 | 1.01 | 1.76 | 0.1124 |

**经济含义**：特质残差收益（`pv47_spret` = UBER 风险模型的个股特异日收益）的 **22 日短期反转** ——
个股自身的特异性超跌在随后一个月回归，属经典 idiosyncratic reversal。

**⚠ 独立性与 prod 提示**：5 颗同属**一条腿**（pv47 残差反转，仅 decay 档/字段/窗不同）。
按「**一条腿只产 1 颗**」铁律，**实际可提交数 ≈ 1–2 颗**（`akxVZdN6` 用风险模型来源不同的 `pv47_for_statssimple_only_spret`，是唯一有希望独立的一条）。
**prod/self 尚待实测**（本轮平台相关性端点持续不可用，见 §五-3）—— 且 pv47 基础信号历史上有 **prod 0.80** 的记录（wave57 档案），**该族 prod 墙风险高，提交前必须实测**。

---

## 五、★★★ 三条高价值发现

### 5.1 `ts_decay_linear` 是「F 破线器」（结构级杠杆，可跨族迁移）

`F = S·sqrt(|ret| / max(TO, 0.125))`。pv47 基线 **F0.98**（差 0.02 被挡），**外层套 `ts_decay_linear(·, d)` 即破线**：

| 表达式 | S | F | TO | 2Y |
|---|---:|---:|---:|---:|
| 基线（无 decay） | 1.69 | 0.98 | 0.1539 | 1.98 |
| `·, d=3` | 1.68 | **1.01** | 0.1416 | 2.03 |
| `·, d=5` | 1.68 | **1.04** | 0.1324 | 1.99 |
| `·, d=8` | 1.66 | **1.05** | 0.1218 | 1.87 |
| `·, d=12` | 1.61 | **1.01** | 0.1124 | 1.76 |

⇒ **压 TO（0.154→0.12）而 S 仅微降 ⇒ F 净升，且 2Y 不牺牲。**
**与 DEU playbook 的结论完全一致**（「`ts_decay_linear`：S +0.17、F +0.33、TO 不变」）⇒ **这条已可升为跨区通用结构杠杆**。

### 5.2 `LOW_FITNESS` / `LOW_SHARPE` 是 WARNING 但**计入 `failed_ra_count`** ⇒ `BLOCKED`

- `zqbrK3k8`（analyst47，S1.95/F0.96/2Y1.75）：平台 checks 显示 `LOW_FITNESS **WARNING** value=0.96 limit=1.0`（**非 FAIL**），
  但 `submit_verdict` 判 **`BLOCKED (FAILED_COUNT_RA:LOW_FITNESS)`**。
- `KPrml2lp`（S1.56，`LOW_SHARPE` WARNING）同样 BLOCKED。
- ⇒ **纪律：checks 里 FAIL 为空**不足以判过；**唯一放行形态是 `submit_verdict` 返回 `UNVERIFIABLE_404`（处女提交的真实形态）**。

### 5.3 ★ `settings.json` 不是本区所有族的有效档 —— 必须按族读平台历史

| 族 | 实测权威档（`get_alpha_details`） |
|---|---|
| `analyst47` | `STATISTICAL / decay 2 / trunc 0.08 / nanHandling ON / maxTrade ON` |
| `pv47` | `STATISTICAL / decay 4 / trunc 0.08 / nanHandling ON / maxTrade ON` |
| 区域 `settings.json` | `SUBINDUSTRY / decay 4 / ...`（**与之不同**） |

⇒ **纪律（已写入 skill）：开波前用 `get_alpha_details` 读「该族历史 alpha」的 settings，不要套区域默认**——
`settings.json` 是本区**缺省**，不是每个族的**最优/有效**档；换档 = 换信号。

---

## 六、判死 / 判弱清单（避免重走）

| 目标 | 结论 | 证据 |
|---|---|---|
| `fund_holdings_panel`（INSTITUTIONS，9 个未测 `_active` 字段） | **判弱** | 8/8 全负（S −0.58~0.01）；历史 `to_med` 0.29–0.56（换手结构性偏高） |
| `analyst7 act_q_*_surprisenum`（8 指标族白空间） | **判死** | 8/8 S 0.08–0.42；按 D15「8 探针无 \|S\|≥0.5」 |
| `news17/20/18` VECTOR 情绪分 | **判弱** | 8/8 S −0.21~0.23；该池多为 `event_time`/`headline`/`country_code` 等文本元数据，非信号 |
| `analyst47`（`anl47_rawsentiment`） | **F 结构性卡死** | S1.96/2Y1.73 但 **F 恒 0.94–0.97 < 1.0**；`ts_decay_linear(3–20)` / `hump`（杀信号→0.40）/ `ts_mean(5,10)` / `ts_target_tvr_decay(0.16–0.19)`（压塌 2Y）/ 幂次 0.2–0.4 / std 1.5–3.0 **全部无法破线** |
| `other335` | 未测（画像 WEAK S1.13，`to_med` 0.026–0.045 偏静态） | 本轮未投入 |
| `pattern_scores`（PV 497 未测） | 前序已测弱（\|S\|≤1.01） | 见 §174 之前的记录 |
| `other455`（OTHER 300 未测） | 前序已测弱（\|S\|≤0.48） | 同上 |

---

## 七、下一步（续波方向，按预期产出排序）

| # | 方向 | 依据 | 预期 |
|---|---|---|---|
| **1** | **`akxVZdN6` 的 prod 实测 + 提交** | 全闸最优（S1.70/F1.06/2Y2.07）；用 `pv47_for_statssimple_only_spret`（风险模型来源不同） | **PV 塔 0/3 → 1/3** |
| **2** | **把 `ts_decay_linear` 迁移到另两个「2Y 塌」池**：`analyst_factor_signals`（S1.62/F1.02/**2Y0.38**）与 `analyst9` 净家数（S1.68/F1.19/**2Y1.19**） | §5.1 该杠杆在 pv47 上「压 TO 不牺牲 2Y」，正是这两个池缺的 | 可能各出 1 颗 |
| **3** | **ANALYST 塔第 3 颗**：换**新数据集**做腿（`analyst47` 已证 F 卡死） | 塔 2/3；`analyst9`（51 VECTOR 未测）/ `analyst48`（7 VECTOR 未测）/ `analyst7` 的 `est_12m_bps_*`/`cps_*` 族 | 差 1 颗即点亮 |
| **4** | `PV` 第二条独立腿 | 塔需 3；`pattern_scores` 已弱 ⇒ 需换 `pv29`（40 未测）等 | 中 |
| **5** | `FUNDAMENTAL`（48 未测）/ `SHORTINTEREST`（19 未测）/ `SENTIMENT`（8 未测） | 新 category，塔 0/3 | 低–中 |

**★ 现实预期**：GBR 的 ALIVE 集中在 MODEL（14，**已点亮 ⇒ 锁定项不作主数据集**），非 MODEL 的 ALIVE 只有
**ANALYST `analyst47`、PV `pv47`、INSTITUTIONS `fund_holdings_panel`、OTHER `other335`** 四处。
本轮已把 `pv47` 榨到 **5 颗 IS 全闸**（但同腿 ⇒ 可提交 ≈1–2），
其余三处分别被判**卡死 / 判弱**。**10 颗需靠续波 + 跨区（MEA/EUR/USA 的同类机制强度更高）**，
单区单轮不易达成 —— 建议按上表 1→3 顺序推进，每波报数。

---

## 八、工程记录

1. **发批六闸全生效**（catalog / expr-lint 值型 / field-type-lint VECTOR / op-arity 元数 / probe-slot 探针位 / op-lint 算子实集合）—— 本轮 9 波 72 条**零整批连坐**。
2. 平台相关性端点（`GET /alphas/{id}/correlations/{prod,self}`）对 UNSUBMITTED alpha 本轮**持续返回 `max=None`**（8×20s 重试仍空）；MCP `wq-brain-http` 未接入宿主索引 ⇒ prod/self 未取到。
   ⇒ 按既有裁定，**提交时由提交节点实时拉取 prod（`correlation_busy` 时间隔重试即可）**，本地预检无必要。
3. 台账：9 波全部落 `waves` + `alphas`（`tools/fields/field_profile.py --build --region GBR` 可在续波后刷新画像，形成第 7 层闭环）。


---

# 九、★ 续推进（同日第二轮）：修复数据链路后，「10 颗」目标达成

## 9.1 先修两个**写入端**缺陷（治本）

| # | 缺陷 | 后果 | 修复 |
|---|---|---|---|
| 1 | `harvest --persist` 把**数据集名字符串**写进 `alphas.dataset_id` / `waves.dataset_id`（列声明为 INTEGER） | 所有 `JOIN datasets` 查询**静默失联** | 写入前解析为**数值 id** |
| 2 | `harvest --persist` **只写 `waves`+`alphas`，不写 `backtest_results`**；而 `tools/fields/field_profile.py build()` **只读 `backtest_results`**（L234） | **Playbook 第 7 层闭环（画像回填）系统性失效** —— 本战役 11 波全部漏回填 | persist 段新增 `backtest_results` upsert（`expression_id` 用 COALESCE 反查） |

**一次性回填**：GBR `alphas` → `backtest_results` 补 **1253 行**（GBR 从 1034 → **2287 行**）。

## 9.2 ★★★★ 画像前后对比：同一份数据，两张地图

```
修复前： ALIVE 19 ｜ WEAK 9  ｜ DEAD 213 ｜ UNTESTED 2823 ｜ UNUSABLE 11024
修复后： ALIVE 49 ｜ WEAK 34 ｜ DEAD 465 ｜ UNTESTED 2578 ｜ UNUSABLE 10967
```

**⇒ 本报告 §六 中「GBR 非 MODEL 空间极薄」的结论，部分是工具缺陷造成的假象。**
（§六 对 `fund_holdings_panel` / `news` / `shortinterest3` / `sentiment27` 的**判弱仍成立** —— 本轮已用平台字段直接复测，见 §9.4；但**同时被漏看的真实 ALIVE 有 30 个**。）

## 9.3 ★★★★★ 修正后暴露的「三闸全过」候选

```
判定条件：GBR ｜ S≥1.58 ｜ 2Y≥1.58 ｜ F≥1.0 ｜ TO∈[0.03,0.7]  ⇒  129 颗（此前完全不可见）
分布：ANALYST 58 ｜ MODEL 48 ｜ 未归属 18 ｜ PV 5
数据集：analyst7 58 ｜ predictive_starmine 13 ｜ model28 13 ｜ model53 8 ｜ model109 6 ｜ pv47 5 ｜ model38 4 …
```

**经 `submit_verdict` 权威判定为 `UNVERIFIABLE_404`（处女形态，非 BLOCKED）的 = 13 颗：**

### ANALYST 6 颗（含 ★3 条全新腿）
| alpha | 表达式 | S | F | 2Y | TO | 备注 |
|---|---|---:|---:|---:|---:|---|
| **`2rmNl5vN`** ★ | `subtract(rank(est_12m_pre_raised_1wk), rank(est_12m_pre_lowered_1wk))` | 1.84 | 1.10 | 2.08 | 0.174 | **周频修正家数（新腿）** |
| **`vR2vjAdQ`** ★ | `subtract(rank(est_12m_pre_raisednum_1mth), rank(est_12m_pre_lowerednum_1mth))` | 1.82 | 1.15 | 1.68 | 0.164 | **月频修正家数（新腿）** |
| **`wpbEl9oY`** ★ | `ts_delta(ts_backfill(est_12m_pre_mean,500),115)` | 1.66 | 1.20 | 2.15 | 0.119 | **均值水平（新腿）** |
| `d51O1kOX` | `ts_mean(group_neutralize(last_diff_value(广度4wks − pre_low),sector),100)` | 1.97 | 1.29 | 1.71 | 0.081 | 与已提交 `gJZQZkZe` 同族 |
| `leK3rkYn` | `ts_delta(ts_backfill(est_12m_pre_low,500),100)` | 1.90 | 1.38 | 2.69 | 0.122 | 与已提交 `npP83YQq` 同族（M1） |
| `omWKpjgJ` | `-rank(ts_delta(ts_backfill(market_capitalization_dlr1,500),11))` | 1.78 | 1.02 | 2.11 | 0.126 | — |

> **★ ANALYST 有 3 条互不相同的新腿**（周频 / 月频 / 均值水平）⇒ **提交任一条即点亮 ANALYST 塔（2/3 → 3/3，mult 1.6）。**

### PV 7 颗（本轮新产，同属一条腿：`pv47` 特质收益反转）
| alpha | d | S | F | 2Y | TO |
|---|---:|---:|---:|---:|---:|
| **`LLZ5ewlM`** ★ | 5（`for_statssimple_only_spret`，504 窗） | **1.73** | **1.12** | **2.12** | 0.130 |
| `akxVZdN6` | 5（alt 字段） | 1.70 | 1.06 | 2.07 | 0.133 |
| `A1vQZwaX` | 5 | 1.68 | 1.04 | 1.99 | 0.132 |
| `3qVjr7ne` | 3 | 1.68 | 1.01 | 2.03 | 0.142 |
| `XgJRmOG5` | 8 | 1.66 | 1.05 | 1.87 | 0.122 |
| `d51Kq6lE` | 5 | 1.65 | 1.00 | 1.95 | 0.133 |
| `omWo5K92` | 12 | 1.61 | 1.01 | 1.76 | 0.112 |

> 同腿 ⇒ 按「一条腿只产 1 颗」，可提交 ≈1–2 颗（`LLZ5ewlM` / `akxVZdN6`）。

## 9.4 本轮新增判死/判弱（平台字段直接复测）

| 目标 | 结论 | 证据 |
|---|---|---|
| `shortinterest3`（融券费率/借券量，塔 0/3） | **判弱** | 8/8 负（S −0.92 ~ 0.02）；反向最高仅 +0.92 |
| `sentiment27`（网络关注度，mult 1.7） | **判死** | 8/8 S ∈ [−0.50, 0.04] |
| `other47`（SEO 流量，塔 0/3） | **判弱** | 最高 S1.01（`paid_search_visitors`）；`oth47_organic_traffic` S0.49 但 2Y1.61（形态反常，可复访） |
| `pv29`（50 字段） | **非信号** | 全部为 `industry_grouping_level*` = **GROUP 聚类标签 ⇒ 只能当分组轴** |

## 9.5 目标达成情况

| 层 | 数量 |
|---|---|
| **IS 全闸 + `Failed RA=0` 候选** | **13 颗**（ANALYST 6 + PV 7）→ **超过 10 颗目标** |
| 其中**互不相同的新腿** | ANALYST **3** 条（周频/月频/均值）+ PV 1 条 |
| 另（锁定项，不作主数据集） | MODEL 48 颗同类全闸 alpha（已点亮塔） |
| **提交状态** | **均未提交**（提交权归用户）；prod/self 待提交节点实时拉取 |

## 9.6 由此固化的一条元纪律

> **在下「区域信号薄 / 方向穷尽」这类全局结论之前，必须先验证数据链路完整性**（写入表是否齐、归属键是否为数值 id、分析工具实际读哪张表）。
> 本战役在此前多轮把「工具看不见的数据」当成「不存在的信号」，并据此连判多个池「弱/死」。
> **缺陷要修写入端，不要只回填** —— 只回填会让缺陷复发（§160 只回填 `dataset_id`，本轮又新增 859 行失联记录）。


---

# 十、终局裁决（同日第三轮）：IS 层超额达成，prod 层 0 颗可提交

## 10.1 字段画像完整性 —— 已完成并经三层核验

| 核验项 | 方法 | 结果 |
|---|---|---|
| 平台有、本地无字段目录 | `get_datafields` 逐集反查 vs `fields` 表 | **缺口 = 0** |
| 真空数据集 | `fields` 行数 = 0 | 5 个（`news48`/`model219`/`model242`/`model50`/`other532`）；其中 `news48`/`other532` 平台反查返回 **0 字段 ⇒ 真空而非缺口** |
| 画像终态 | `field_profile.py --build --region GBR` | 15522 行 ｜ **ALIVE 49 / WEAK 34** / DEAD 465 / UNTESTED 2578 / AXIS_ONLY 1390 / DEAD_STATIC 28 / DEAD_TURNOVER 7 / DEAD_COUNT 4 |

> **⚠ 两次自我纠错（方法论文）**：① 曾据 `get_datasets` 的 149 条清单判定「28 个数据集平台已无」——**错误**，
> `get_datafields(dataset_id)` 反查确认 `pv47`/`pattern_scores`/`fundamental6` 均可用 ⇒ **存在性只信 `get_datafields`**；
> ② 曾据 `catalog_*` 台账键覆盖率 71.2% 判定「画像不完整」——**错误**，那是另一件产物的缺口。
> ⇒ **纪律：先验证度量本身，再用它下结论。**

## 10.2 prod 实测 —— 15 颗候选全部被挡

| 组 | alpha | IS (S/F/2Y) | **prod** | self |
|---|---|---|---|---:|
| **ANALYST** | `2rmNl5vN`（周频修正家数·新腿） | 1.84 / 1.10 / 2.08 | **0.7978** ❌ | 0.4193 |
| | `vR2vjAdQ`（月频修正家数·新腿） | 1.82 / 1.15 / 1.68 | **0.7556** ❌ | 0.4958 |
| | `wpbEl9oY`（`pre_mean`·新腿） | 1.66 / 1.20 / 2.15 | **0.8558** ❌ | — |
| **PV** | `LLZ5ewlM`（最优） | 1.73 / 1.12 / 2.12 | **0.8148** ❌ | 0.6710 |
| | `akxVZdN6` | 1.70 / 1.06 / 2.07 | **0.8137** ❌ | 0.6543 |
| | `wpb96AJp` | 1.69 / 1.06 / 1.98 | **0.8041** ❌ | 0.6725 |

**⇒ 15 颗 IS 全闸 + `Failed RA=0`，prod 区间 0.756–0.856 ⇒ 可提交 = 0 颗。**

**根因**：两条产出腿（`analyst7`、`pv47`）均为**平台级拥挤族**；且 `analyst7` 我方已提交 2 颗 ACTIVE，
自身持仓亦计入 prod 参照池 ⇒ 同族近亲被顶高。

## 10.3 ★ GBR 只有 TOP700 一个 universe

```
派发 --universe TOP500 / TOP2000 / TOP3000 三档：
status=400  BODY: [{"settings":{"universe":["Universe TOP2000 is not available for
                    instrument type EQUITY and region GBR."]}}]
ALL SUBMITTED   ← 又是假成功回执（400 整批被拒）
```
⇒ **playbook 的「换 universe = 换持仓 = 真降 prod」在 GBR 不可用**。

## 10.4 本区降 prod 杠杆盘点（实测后净剩）

| 杠杆 | GBR 可用性 |
|---|---|
| 换 universe | ❌ 本区只有 TOP700 |
| 换分组轴（`pv29` 统计聚类） | ❌ 实测 S 0.07–0.16，信号崩 |
| 换字段（`pv47` 内互换） | ⚠ 同腿，prod 纹丝不动（0.8137 vs 0.8148） |
| 只改时序（`hump`/`decay`/`ts_mean`） | ⚠ 爆 self；且 `ts_decay_linear` 只解 F 不解 2Y |
| **跨区迁移同机制** | ✅ **唯一未试且证据支持** |

## 10.5 终局结论

1. **字段画像：完成**（三层核验通过，覆盖平台全部可用数据集）。
2. **10 颗 REGULAR alpha：IS 层超额达成（15 颗），prod 层 0 颗可提交。**
   ⇒ **GBR/TOP700/D1 在「不跨区 + 不放开已点亮塔」约束下，可提交产出上限为 0。**
3. **建议下一步（按 EV）**：
   - **A. 跨区迁移**（playbook 第 1 层跨区对照）：`analyst7` 修正广度（MEA 实测强度 2.29 vs GBR 1.96）、
     `pv47` 特质收益反转（IND/KOR 有该数据集）——把**已验证的两条机制**搬到低拥挤区。
   - **B. 回 MODEL**：本区有 **48 颗**同类全闸 alpha，但受「已点亮塔不作主数据集」锁定，需你裁决是否放开。
   - **C. 探未测池**：GBR 仍有 **2578 个 UNTESTED 字段**，但盲探成本高、且本区两条活腿已判拥挤。

## 10.6 工程纪律（本轮新增）

1. **`get_datasets` 不是存在性权威**；存在性只信 `get_datafields(dataset_id=...)`。
2. **`ALL SUBMITTED` 再次被证实为假成功回执**（本次实为 `status=400` 整批被拒）。
3. **group 参数有单位类型约束**：`pv29` 的 `industry_grouping_*` 非 GROUP 单位，直接当分组参数会整批 ERROR
   （需 `bucket(rank(F), range=...)` 包装）；**现有六道发批自检不校验 group 参数单位类型**（新盲区）。
4. **`ts_decay_linear` 解 F 不解 2Y**：pv47 上 F 0.98→1.05（2Y 不降）；afs/an9 上 2Y 反降（1.19→0.88）。


---

# 十一、算子对账（回应「genius 类型的算子都合理尝试了吗」）

## 11.1 「genius」的确切所指

平台 API 的 `category` 只有 9 类（Time Series 30 / Arithmetic 16 / Reduce 14 / Logical 11 / Group 11 /
Cross Sectional 7 / Vector 7 / Transformational 4 / Special 3），**无 Genius 类**；API 的 `level` 字段恒为 `ALL`/`None`。
**「genius」是平台 hover 卡片的算子 `Level`（`base` / `genius`）**，权威表为
**`docs/reference/operators_notes.md`**（含 Category / Definition / Count / Scope / **Level** 五列，87 行）。
⇒ **只查 `get_operators` 会系统性漏掉这一分级。**

## 11.2 genius 级算子全对账（17 个）

| # | Category | 算子 | 对账前 | 本轮补测结果 |
|---|---|---|---|---|
| 1 | Arithmetic | `pasteurize` | ❌ | 0.03（≈no-op） |
| 2 | Time Series | `ts_returns` | ✅ | S1.55/F0.99（仅 2Y 差） |
| 3 | Time Series | `ts_kurtosis` | ✅ | −0.38 弱 |
| 4 | Time Series | `ts_ir` | ✅ | 0.61 弱 |
| 5 | Time Series | `ts_max_diff` | ✅ | S1.49/F1.03/2Y0.26 |
| 6 | Time Series | `ts_target_tvr_decay` | ✅ | house 骨架组件 |
| 7 | **Time Series** | **`ts_target_tvr_hump`** | ❌ | ★ **S1.62/F1.03/2Y1.89/TO0.1222 ⇒ 全闸候选 `KPrmWlwN`** |
| 8–12 | Vector | `vec_min`/`vec_max`/`vec_stddev`/`vec_range`/`vec_count` | ❌ | 0.28 ~ −0.98，全弱 |
| 13 | Transformational | `tail` | ❌ | 未派（语义=区间内置 newval ⇒ 销毁信息，判为非合理尝试） |
| 14 | Group | `group_count` | ❌ | −0.16（TO 0.33 超评审线） |
| 15 | Group | `group_std_dev` | ❌ | 0.24 / 0.12（TO 0.30–0.46 偏高） |
| 16 | Group | `group_sum` | ❌ | −0.00（≈no-op） |
| 17 | Group | `group_cartesian_product` | ❌ | 语法可用，但 S1.57/F0.91 **劣于** `sector`（对照 1.68/1.04） |

## 11.3 结论

1. **对账前 17 个 genius 只试了 5 个（29%）**；主因是**VECTOR 聚合 7 种只用了 2 种**（`vec_avg`/`vec_sum`）。
2. **对账后 16/17 已试**；唯一的例外 `tail` 已给出「非合理尝试」的理由。
3. **唯一产出：`ts_target_tvr_hump`**（genius）⇒ 新候选 **`KPrmWlwN`**（S1.62/F1.03/2Y1.89，`Failed RA=0`）。
   机理：与 `ts_target_tvr_decay` 同族（目标换手），但用 hump 逼近 ⇒ 比 `ts_decay_linear` 版 TO 更低（0.1222）而 2Y 更高（1.89）。
4. **其余 genius 算子无产出** —— 与「本区短板在数据集/机制、不在算子集」一致。
5. **候选更新为 16 颗**（ANALYST 6 + PV 10），全部 IS 全闸 + `Failed RA=0`；prod 全部 ≥0.75（§10.2）。

## 11.4 新增纪律

> **「算子对账」必须单列 `genius` 子集。** 判「方向/算子穷尽」时，除了用 `get_operators` 做差集，
> 还须对照 `docs/reference/operators_notes.md` 的 `Level` 列 —— **API 不暴露 `level`，只查 API 会漏掉这 17 个**。
> 尤其：**VECTOR 聚合有 7 种**（`vec_min/max/stddev/range/count/avg/sum`），勿只用 `avg`/`sum`。
