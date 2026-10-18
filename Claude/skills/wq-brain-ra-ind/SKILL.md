---
name: wq-brain-ra-ind
description: "在 IND 区挖 REGULAR alpha、调 IND 的回测设置或阈值、查 IND 某类数据集（区域 × 类别组合）的配方与禁区时使用：IND 的区域分支流程与回测把控面板。通用九步走 wq-brain-ra-pipeline，判提交与提交走 worldquant-submit-alpha。"
layer: L-RA-R
allowed-tools:
  - Read
  - Bash
  - mcp__wqb-db__*
  - mcp__wq-brain-http__*
version: "1.0"
last_verified: 2026-10-10
---

# IND 区域挖掘流程（RA 区域分支）

## 职责边界

- **本 skill 负责**：IND 的区域分支——入场状态、回测把控（区域与「区域 × 类别」组合的回测设置 / 阈值 / Mode B 主闸，每个值可查来源）、S1 / S2 / S4 / S5 的 IND 差异步骤、组合分支文件索引。
- **本 skill 不做**：九步通用正文（→ [`wq-brain-ra-pipeline`](../wq-brain-ra-pipeline/SKILL.md)）；选区（→ `brain-next-move-analysis`）；判提交与提交（`submit_verdict` 只否决，提交走 `worldquant-submit-alpha` 且必须用户确认）；不改其它区域的控制文件。
- **上游 / 下游**：上游 = 用户点名 IND，或 `wq-brain-ra-pipeline` 步 1 路由到本区；下游 = `wq-brain-ra-pipeline` 各步、`wq-brain-campaign-toolkit` 引擎、`wq-brain-alpha-optimization-v1`（S4 改进）。

## 怎么用

1. **入场**：看下面「区域控制面板」的入场状态。`frozen` 只走 profile 写明的后门；`probe-only` 只许探针批。
2. **每次回测前**按数据集取生效画像（回测设置、阈值、Mode B 主闸、生成与改进要点，每项带来源）：

   ```bash
   $WQ_PY -m wqb.profiles explain --region IND --dataset <dataset>
   ```

   `workflow_batch_track` 会把该组合的回测覆盖以 `--set` 钉住；直接用 MCP 发仿真（`create_multi_simulation` / `create_simulation`）时，按 explain 输出逐项传设置，不要依赖工具缺省（各入口缺省不同，换档等于换信号）。
3. **走九步**：按 `wq-brain-ra-pipeline` 执行；步 3 / 4 / 7 / 8 先读对应组合的分支文件（下表最后一列）。
4. **步 9 回写之后**刷新组合证据并重渲本 skill：

   ```bash
   $WQ_PY -m wqb.profiles sync-cells --region IND --apply
   $WQ_PY -m wqb.profiles render --region IND --apply
   ```

<!-- region-scaffold:nav:start -->
| 目录 | 装什么 | 入口 |
|---|---|---|
| **SKILL.md** | 职责边界 + 怎么用 + 生成块（区域控制面板 / 组合分支 / 流程差异） | 本文 |
| [`rules/`](rules/README.md) | **IND 独有规则与纪律**（六步覆盖、改控制、闸门与提交纪律） | [rules/README.md](rules/README.md) |
| [`config/`](config/README.md) | **配置视图**（真身在 `tracking/IND/config/`）：三表分工、区域默认档、覆盖落差 | [config/README.md](config/README.md) |
| [`references/`](references/) | **实证**：`<类别>.md` 组合分支卡（render 生成）+ `_` 前缀专题（战役 / 手册 / 快照） | [references/](references/) |
| [`scripts/`](scripts/README.md) | 本 skill 级脚本（区域探针脚本家 = `tracking/IND/scripts/`） | [scripts/README.md](scripts/README.md) |

细则不写在 SKILL.md：规则 → `rules/`，实证 → `references/`，配置 → `config/`，脚本 → `scripts/`。
<!-- region-scaffold:nav:end -->

## 区域控制面板

<!-- profiles:region-panel:start -->
**入场状态**：`probe-only`　TOP500：可提交空间已于 2026-10-03 系统扫描穷尽（20 批 / ~170 表达式 / 14+ 族；8 颗 IS 全闸候选 prod 全部 0.7161–0.8261，被 1–3 颗钉子钉在 0.70 之上）——只许探针；历史有效面是长窗结构（2Y 强，评审加 2Y 权重）

| 回测设置 | 值 | 来源 |
|---|---|---|
| instrumentType | EQUITY | settings.json |
| region | IND | settings.json |
| universe | TOP500 | settings.json |
| delay | 1 | settings.json |
| neutralization | STATISTICAL | settings.json |
| decay | 4 | settings.json |
| truncation | 0.08 | settings.json |
| pasteurization | ON | settings.json |
| testPeriod | P0Y0M0D | settings.json |
| unitHandling | VERIFY | settings.json |
| nanHandling | OFF | settings.json |
| maxTrade | OFF | settings.json |
| language | FASTEXPR | settings.json |
| visualization | false | settings.json |

| 阈值 | 值 | 来源 |
|---|---|---|
| Mode B 主闸（sharpe / fitness） | 1.5 / 1.0 | thresholds_override:IND（实时值含区域台账，看 explain） |
| review.sharpe_min | 1.58 | thresholds.json |
| review.fitness_min | 1.0 | thresholds.json |
| review.turnover_min | 0.01 | thresholds.json |
| review.turnover_max | 0.7 | thresholds.json |
| review.two_year_sharpe_min | 1.0 | thresholds.json |
| near.sharpe_min | 1.0 | thresholds.json |
| diversity.signal_floor.max_sharpe_floor | 1.2 | thresholds.json |

**循环与闸门（profile front-matter）**
- 每波探针位上限：1
- 快判死：缺省（决策表 D15：新数据集 8 探针无 ／S／≥0.5 即判死）；本区无额外规则
- 停止条件：白名单被 dead_end 全覆盖
- 停止条件：已知 14+ 族全部 IS 死或撞 prod 钉子（2026-10-03 扫描穷尽）——升 active 须出现新的信息维度（不在 prod book 里）
- 闸门特化（文档级）：cw_gate=WARN、judge_two_year_sharpe_weight=high——代码尚未读取（闸 7 恒 WARN，CW 在步 7 人工判），按此执行由 agent 负责

**平台事实**
- 宇宙是单一国家（config.REGION_COUNTRY_SCOPE）：country 轴中性化 / 分组等于全市场，别用
<!-- profiles:region-panel:end -->

## 组合分支（区域 × 类别）

<!-- profiles:cells-index:start -->
| 类别 | 分组 | 状态 | 回测覆盖 | 阈值覆盖 | 回测 / RA 全过 | prod 已测（低于上限） | 判死 / 胜绩 | 分支文件 |
|---|---|---|---|---|---|---|---|---|
| model | MODEL | probe | — | — | 168 / 25 | 12（9） | 12 / 5 | [references/model.md](references/model.md) |
| pv | PV | probe | — | — | 143 / 47 | 29（10） | 8 / 2 | [references/pv.md](references/pv.md) |
| analyst | Analyst | probe | — | — | 114 / 7 | 18（10） | 5 / 3 | [references/analyst.md](references/analyst.md) |
| sentiment | News-Sentiment | probe | — | — | 95 / 0 | 0（0） | 1 / 0 | [references/sentiment.md](references/sentiment.md) |
| institutions | Institutions | probe | — | — | 47 / 0 | 0（0） | 3 / 0 | [references/institutions.md](references/institutions.md) |
| news | News-Sentiment | probe | — | — | 42 / 0 | 0（0） | 3 / 0 | [references/news.md](references/news.md) |
| earnings | Earnings | probe | — | — | 36 / 0 | 0（0） | 4 / 0 | [references/earnings.md](references/earnings.md) |
| option | Option | probe | — | — | 36 / 0 | 0（0） | 1 / 0 | [references/option.md](references/option.md) |
| risk | Risk | probe | — | — | 8 / 8 | 2（2） | 3 / 0 | [references/risk.md](references/risk.md) |
| shortinterest | ShortInterest | probe | — | — | 7 / 0 | 0（0） | 1 / 0 | [references/shortinterest.md](references/shortinterest.md) |
| insiders | Insider | probe | — | — | 6 / 0 | 0（0） | 2 / 0 | [references/insiders.md](references/insiders.md) |
| fundamental | Fundamental | probe | — | — | 0 / 0 | 1（1） | 9 / 2 | [references/fundamental.md](references/fundamental.md) |
| other | Other | probe | — | — | 0 / 0 | 92（19） | 9 / 0 | [references/other.md](references/other.md) |

说明：另有 83 条回测行没写数据集，无法归到组合；9 条判死 / 胜绩连类别也推断不出；证据于 2026-10-04 只读汇总。
<!-- profiles:cells-index:end -->

## 六步纵深骨架（本区覆盖）

> 通用方法见 [六步纵深骨架 · 通用主文档](../wq-brain-ra-pipeline/references/_six-step-core.md)。
> 本节只写 **IND 的 override**：主 skills 未覆盖的本区平台事实、实测杠杆、已死轴、工程坑。
> **覆盖主 skills 同名条目；铁律与锁定项不可放宽。** 无实证处标「待实测」。

### ① 六法体检 · 本区覆盖

- **平台档位**：`TOP500`。
- **待实测**：离线体检包退化范围、在线体检档、不可用算子。

### ② 组装 · 本区覆盖

- **沿用主 skills**。
- **待实测**：本区组装禁区。

### ③ 归因 · 本区覆盖

- **★ prod 全景**：8 颗 IS 全闸候选的 prod **全在 0.7161–0.8261**（单颗钉子型）⇒ 归因读数应重点看 prod 直方图而非强度。
- **历史有效面**是长窗结构（2Y 强）。

### ④ 破闸杠杆 · 本区覆盖

- **已点亮塔不开战役**，只作组腿辅助；**塔计数按自然季度清零**，现查 `tools/campaign_intel.py` 的 pyramid 子命令。
- **待实测**：本区各闸最优杠杆（按决策表 D0-P 处置）。

### ⑤ 算子穷举 · 本区覆盖

- **★ 字段画像基线（本区实证库）**：[references/_field-profile.md](references/_field-profile.md)。按「① 字段画像 → ② 适用模板 → ③ 回测结果及指标」三节组织，覆盖 analyst_base_ref / model68 / model207 / earnings3 / news_sentiment_nlp / pv70 / fundamental1 七集 + 全区 14 334 字段的 verdict 总览。
- **★ 画像权威源 = `data/wqb.db::field_profile_ind`**（工具 `tools/fields/field_profile.py`，DEU/GBR 同款）。全区 14 334 字段中 **ALIVE 仅 54 / WEAK 15（合计 0.5%）**，其余 UNTESTED 10 770 / UNUSABLE 2 785。**判死前必查此视图**——指纹（cov/类型/aCnt）只够预筛。
- **★ 修正（2026-10-18）**：`earnings3` 的 `ern3_pre_interval`（S **4.49** / F 3.25 / TO 0.337 / n=19）与 `ern3_next_interval`（S **3.03** / F 1.91 / TO 0.209 / n=15）是本区**画像 ALIVE** 字段。此前把该集当「日期类毒药」整集判死是**误判** ⇒ **日期类必须区分 timestamp（死）与 interval（活）**。当前唯一达标 ATOM 仍是 `zqrj0bzK`；`ern3_pre_interval` 是下一个待验候选（瓶颈在 prod/robust/2Y，S/F/TO 已过）。
- **本区算子实测**：`ts_decay_exp_window` **IND 不可用**（发批前必核 `get_operators`）；`ts_max_diff` / `ts_av_diff` 可用但 mm 结构在本区**信号毁灭**（S −0.31~0.01）⇒ 勿用。
- **待实测**：本区其余算子实证。

### ⑥ 终验 · 本区覆盖

- **★ 升档条件**：出现不在 prod book 里的新信息维度，且单仿真探针 IS 层 |S| 达 0.5；
  升档前先按 D0-P 的诊断前置看 prod 直方图。
- **线索**：[IND × other](references/other.md) 的 `other532` 特质收益反转（`gJZwVXVm` S 3.66）可能正是这样的新维度 —— **先测 prod，再由人决定是否改 entry_verdict**。

## 本区流程差异（相对九步骨架）

<!-- profiles:manual:start -->
- **入场**：2026-10-03 起 probe-only——20 批、约 170 条表达式、14+ 族系统扫描；8 颗 IS 全闸候选的 prod 全在 0.7161–0.8261（单颗钉子型）。只许探针批。
  - **⚠ 2026-10-17 修正：「可提交空间已穷尽」结论被推翻。** 新增族 = **残差化**（`rank(-ts_regression(ts_zscore(returns,252), ts_zscore(<F>,252), 252, rettype=0))` + **decay 126**），属 2026-10-03 扫描里**没有的信息维度**，实测在 IND 直接过 prod 墙：institutions6（13F 季频）**10/10 RA 全过**（S 2.65–3.12 / TO 0.24–0.26 / robust 1.14–1.97 / prod 0.59–0.67）；analyst 族 11/18 全过（S 1.94–3.04）；PV 残差 `vRO9nG3w` S 2.90 / 2Y 3.14 / robust 1.78 / prod 0.6695。
  - ⇒ **「只许探针批」的限制对残差化族不适用**（它已用 24+ 条仿真证明能过全闸）。`entry_verdict` 是否升 `active` 属**用户决策**，agent 不得自行改；在用户表态前，残差化族可按完整波形（每波 ≤10 条）推进。
- **升档条件**：出现不在 prod book 里的新信息维度，且单仿真探针 IS 层 |S| 达 0.5；升档前先按决策表 D0-P 的诊断前置看 prod 直方图。注意 [IND × other](references/other.md) 的 other532 特质收益反转（gJZwVXVm S 3.66）可能正是这样的新维度——先测 prod，再由人决定是否改 entry_verdict。
- **S0 选集**：已点亮塔不开战役，只作组腿辅助；塔计数按自然季度清零，现查 tools/campaign_intel.py 的 pyramid 子命令。
  - **★ 选集优先级 = 「经济锚 > 覆盖率 > 拥挤度」，禁止按 aCnt 排序开炮（2026-10-18 实证）**：三个全库最低拥挤集（`analyst_base_ref` aCnt 0–73｜`news_sentiment_nlp` 2–9｜`pv70` 0–3）**实测全部 0 达标** ⇒ **低 aCnt ≠ 有信号**（低拥挤只解决 prod，解决不了强度）。IND 的 ATOM 瓶颈是 **S 连 1.58 都够不到**（强度不足），不是 prod 拥挤。
  - **★ IND 无收益锚字段 8 类（换集前必查）**：盈利惊喜(0.05–0.60/TO1.20 爆)｜动量(0.25–1.09/2Y 塌)｜内部人(−0.05–0.45/画像 DEAD_STATIC)｜新闻情绪(−0.48–0.33/TO1.5 爆)｜分歧度区间(0.10–0.50)｜`chg_pct`(TO0.82 爆)｜关系图 `pv70`｜薪酬 `fundamental1`（画像 UNUSABLE×118）。**注意：`earnings3` 不在此列**（见 S1 字段的修正条）。完整画像/模板/指标见 **[字段画像基线](references/_field-profile.md)**。
  - **★ IND 唯一有效机制三要素（缺一不可）**：①连续慢变量（预期每日微调，非财报阶跃）②有经济锚（PEAD）③TO 适中（`ts_delta(F,66)` ⇒ 0.10）。仅 `anl44_eps_best_eeps_cur_yr` 系满足。
  - **★ IND 区 11 塔已全亮**（2026-10-18 实测：ANALYST×9/1.4｜EARNINGS×2/1.1｜FUNDAMENTAL×3/1.2｜IMBALANCE×1/1.0｜INSTITUTIONS×3/1.0｜MACRO×2/1.0｜MODEL×10/1.2｜NEWS×6/1.3｜OTHER×6/1.3｜PV×17/1.1｜RISK×5/1.0）⇒ **本区选类别纪律已无区分度**，ATOM 价值只在 alpha 收益 ×  multiplier。⚠ **塔归属不能读未提交 alpha 的 `pyramids` 字段**（UNSUBMITTED 时为 null）⇒ 靠「数据集类别」推算。
- **S1 字段**：分清 actual（已实现）与 estimate（预测）；IND 的 HIGH_TURNOVER 线 0.40 比它区严，平台还额外要求 robust universe Sharpe。
  - **★ 判死前必查 `field_profile_ind`，指纹只够预筛**：`pv70`（关系图近静态）与 `fundamental1`（UNUSABLE×118）靠画像直接跳过是可靠的；但 **`earnings3` 被指纹误杀**——`*_reptime`（timestamp）确实死，而 **`*_interval`（间隔天数）是 ALIVE**（`ern3_pre_interval` S 4.49）。⇒ 预筛用 cov/类型/aCnt，**终判必须查画像**。画像/模板/指标见 **[字段画像基线](references/_field-profile.md)**。
  - **日期类必须区分 timestamp 与 interval**：`*_reptime` / `*_lastupdate`（时间戳）无收益锚；`*_interval`（间隔天数）是连续数值变量，有事件时钟锚，可投。
  - **§ 事件型字段必须 `ts_delta` 包装**：财报日阶跃类（`reported_actual_value` / `chg_pct`）裸水平 TO 1.2–1.5 爆表；日频新闻必须 `ts_mean(22)`（代价是 S 掉到 0.33）。
- **S3 回测**：设置跟 settings.json（STATISTICAL；nanHandling、maxTrade 都是 OFF——两项都是强度闸）；窗口 / decay 按信号速度定：行为族 decay 1（水平形）或 8（raw），长窗结构族才用大 decay。需要设置全显式时用 tools/ind_sim_submit.py。
- **S4 改进**：评审加 2Y 维度——IS 在 1.0–1.25 之间但 2Y 达 1.5 的候选不降格、不判死，进 Mode A 收敛（2Y 强只免误杀，不免闸）。
- **S5 提交**：向用户汇报时 IS 与 2Y 两列并列，禁止只报 IS。
- **★ 单塔归属法则（2026-10-10）**：`MATCHES_PYRAMID` 的匹配塔数 = 表达式**全部字段（含门控字段）的数据集类别并集** ⇒ 造单塔候选时**门控字段必须与信号字段同类别**（`cap` / `returns` 属 PV，用它们门控会把 other 信号污染成 PV+OTHER 双塔）。IND/D1 已点亮 = model / pv（analyst、risk 各差 2 颗）；可用未点亮塔 11 个：other / macro / fundamental / option / sentiment / news / earnings / insiders / imbalance / institutions / shortinterest。
- **未点亮塔入口（2026-10-10）**：IND 的 `macro` 类别只有 1 个数据集 `macro63`（Index Reconstitution Data），只有 1 个字段 `mcr63_membership`（MATRIX，WisdomTree WTIDJH 成分状态）。
  - **⚠ 实测结论：IND 的 macro 塔当前不可达。** 该字段在 IND/TOP500/delay1 下**全域恒为 0**（23 条表达式 × 4 种设置档 STATISTICAL/NONE × nanHandling ON/OFF × 8+ 算子族，全部空仓；铁证 = `if_else(greater(x,0.5),1,-1)` 得 long 0 / short 502，无 NaN）。
  - 同一字段在 **ASI/MINVOL1M 有真实持仓**（raw S=0.49）⇒ **不是字段坏，是 IND 侧数据缺口**（IND `dateCreated=2025-10-01`，疑似未覆盖 IS 期）⇒ 标记「数据未落地」，平台更新后复测。证据见 `tracking/IND/candidates/IND_macro63_ledger.md`。
  - **★★★ 2026-10-17 修正：恒 0 字段的正确用法 = 「挂塔器」，macro 塔已实证可达。** 它不产生信号（恒 0），但 `add(<腿>, mcr63_membership)` 能让**信号逐位不变**、只把 `MATCHES_PYRAMID` 的类别并集从 1 类改成 2 类（eff=2），从而把该 alpha 记到 macro 塔上。
    - **硬约束 ①**：腿用到的**数据集类别数必须 ≤1**（挂 macro 后 =2）。≥3 类别 ⇒ `effective` 归零、塔位全废。
    - **硬约束 ②**：含 `returns` 的腿若还含别的集字段（如 institutions6）已是 2 类别，**不能再挂**。⇒ 正解是**同类别残差腿**：`returns` 与 `volume`/`adv20`/`ts_std_dev(returns,20)` 同属 **PV** 类，所以「PV 残差」是天然单类别腿。
    - **实测**：`add(rank(-ts_regression(ts_zscore(returns,252), ts_zscore(ts_std_dev(returns,20),252),252,rettype=0)), mcr63_membership)` = `vRO9nG3w`，**S 2.90 / 2Y 3.14 / robust 1.78 / self 0.2838 / prod 0.6695 / 塔归 macro+pv eff=2 / 十年全正 / RA failed=0**。
    - **对照验证**：两组 add-zero 对照逐位相同（`KPm6xeGx`≡`mLYeO51`、`omovwGMv`≡`rKdL6GgE`）⇒ **信号零增益是设计预期，不是 bug**。
    - **代价**：multiplier 由 1.1 降为 1.0（双塔分摊），且属**蹭塔位合规灰区** ⇒ **只在「某塔只差 1 颗就点亮」时用，且用前须让用户知情**。当前 IND macro=2/3，正差 1 颗。
  - ⇒ 要打「未点亮塔」，优先用**有数据**的：other(20 数据集) / news(22) / fundamental(12)…；只有「差 1 颗」时才动恒 0 字段。
  - **「混塔」实测（wave163 → wave234 修正）**：把该字段当 `bucket` 分组轴 ⇒ 与纯 PV 版**逐位相同**（恒 0 ⇒ 单组 ⇒ 退化）；把它 `add` 挂进**单类别**腿 ⇒ 塔归属确为 **[MACRO, PV] eff=2**，信号零增益（结果就是原腿本身），但 multiplier **1.1 → 1.0**。⚠ wave163 当时判「不建议」是在「想赚 multiplier」的目标下；**若目标是「点亮差 1 颗的塔」，结论相反 —— 可用**（见上条硬约束）。加第三类会让 effective 归零（论坛+实测双证）。
  - **字段有无数据的标准诊断法（论坛背书）**：`if_else(greater(x,0.5),1,-1)`（或 `f==0?1:0`）+ **neutralization=NONE** + decay0，看 **`longCount/shortCount`**——若 long=0/short=全宇宙 ⇒ 字段在本 universe 恒为常数。⚠ **别只看总 sharpe**：全空头退化组合会给出 S=−1.10 的**假信号**。配套算子：`to_nan(x, value=0)`（0→NaN）、`last_diff_value(x,d)`（上一档水位）、`days_from_last_change(x)`（从未变化时返 NaN）。
（来源：IND profile；塔法则与 macro 入口见 [other 分支经验](references/other.md)）
<!-- profiles:manual:end -->

## 改控制

- **区域级**：`tracking/IND/config/settings.json`（仿真设置）、`tracking/IND/config/thresholds.json`（阈值）。
- **组合级**：`tracking/IND/config/cells.json`——只写覆盖值，每个覆盖在同级 `_evidence` 写证据（波号 / alpha id / 日期）；没有证据的覆盖校验不通过。改完先校验再重渲：

  ```bash
  $WQ_PY -m wqb.profiles check --region IND
  $WQ_PY -m wqb.profiles render --region IND --apply
  ```

- **锁定项**（任何层都不能放宽）：禁混信号、Mode B 主闸下限、决策表 D0-P、平台线、窗口白名单、点塔按平台类别、提交前用户确认、truncation 不作扫描维度——全文见 `$WQ_PY -m wqb.profiles explain` 末尾。
- **证据与历史**：[IND profile](../wq-brain-ra-pipeline/references/regions/IND.md)（入场裁决、红绿榜、证据附录）。
