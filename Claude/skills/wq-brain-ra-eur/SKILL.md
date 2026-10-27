---
name: wq-brain-ra-eur
description: "在 EUR 区挖 REGULAR alpha、调 EUR 的回测设置或阈值、查 EUR 某类数据集（区域 × 类别组合）的配方与禁区时使用：EUR 的区域分支流程与回测把控面板。通用九步走 wq-brain-ra-pipeline，判提交与提交走 worldquant-submit-alpha。"
layer: L-RA-R
allowed-tools:
  - Read
  - Bash
  - mcp__wqb-db__*
  - mcp__wq-brain-http__*
version: "1.0"
last_verified: 2026-10-20
---

# EUR 区域挖掘流程（RA 区域分支）

## 职责边界

- **本 skill 负责**：EUR 的区域分支——入场状态、回测把控（区域与「区域 × 类别」组合的回测设置 / 阈值 / Mode B 主闸，每个值可查来源）、S1 / S2 / S4 / S5 的 EUR 差异步骤、组合分支文件索引。
- **本 skill 不做**：九步通用正文（→ [`wq-brain-ra-pipeline`](../wq-brain-ra-pipeline/SKILL.md)）；选区（→ `brain-next-move-analysis`）；判提交与提交（`submit_verdict` 只否决，提交走 `worldquant-submit-alpha` 且必须用户确认）；不改其它区域的控制文件。
- **上游 / 下游**：上游 = 用户点名 EUR，或 `wq-brain-ra-pipeline` 步 1 路由到本区；下游 = `wq-brain-ra-pipeline` 各步、`wq-brain-campaign-toolkit` 引擎、`wq-brain-alpha-optimization-v1`（S4 改进）。

## 怎么用

1. **入场**：看下面「区域控制面板」的入场状态。`frozen` 只走 profile 写明的后门；`full-coverage` 数据集必须做尽（见「全量覆盖操作纪律」）。
2. **每次回测前**按数据集取生效画像（回测设置、阈值、Mode B 主闸、生成与改进要点，每项带来源）：

   ```bash
   $WQ_PY -m wqb.profiles explain --region EUR --dataset <dataset>
   ```

   `workflow_batch_track` 会把该组合的回测覆盖以 `--set` 钉住；直接用 MCP 发仿真（`create_multi_simulation` / `create_simulation`）时，按 explain 输出逐项传设置，不要依赖工具缺省（各入口缺省不同，换档等于换信号）。
3. **走九步**：按 `wq-brain-ra-pipeline` 执行；步 3 / 4 / 7 / 8 先读对应组合的分支文件（下表最后一列）。
4. **步 9 回写之后**刷新组合证据并重渲本 skill：

   ```bash
   $WQ_PY -m wqb.profiles sync-cells --region EUR --apply
   $WQ_PY -m wqb.profiles render --region EUR --apply
   ```

<!-- region-scaffold:nav:start -->
| 目录 | 装什么 | 入口 |
|---|---|---|
| **SKILL.md** | 职责边界 + 怎么用 + 生成块（区域控制面板 / 组合分支 / 流程差异） | 本文 |
| [`rules/`](rules/README.md) | **EUR 独有规则与纪律**（六步覆盖、改控制、闸门与提交纪律） | [rules/README.md](rules/README.md) |
| [`config/`](config/README.md) | **配置视图**（真身在 `tracking/EUR/config/`）：三表分工、区域默认档、覆盖落差 | [config/README.md](config/README.md) |
| [`references/`](references/) | **实证**：`<类别>.md` 组合分支卡（render 生成）+ `_` 前缀专题（战役 / 手册 / 快照） | [references/](references/) |
| [`scripts/`](scripts/README.md) | 本 skill 级脚本（区域探针脚本家 = `tracking/EUR/scripts/`） | [scripts/README.md](scripts/README.md) |

细则不写在 SKILL.md：规则 → `rules/`，实证 → `references/`，配置 → `config/`，脚本 → `scripts/`。
<!-- region-scaffold:nav:end -->

## 区域控制面板

<!-- profiles:region-panel:start -->
**入场状态**：`full-coverage`　⛔ 2026-10-20 起废止探针式派发，数据集必须做尽（字段全量覆盖 / 模板族 ≥3 / 边界算子档穷举）；2026-10-02 的『结构性穷尽』只在探针式派发口径下成立，重开前必须重跑全量覆盖闸。已验证机制两条：① analyst7 四件套修订 surprise（14 颗 RA 全过 / 6 个 metric 族，TOP2500 + FAST + decay 40–80，最大互不相关团 7）；② 慢 MODEL 残差 × 快 PV（加权写法已被闸 5 禁止，只许条件 / 分组 / 残差三式，SUBINDUSTRY + decay4）

| 回测设置 | 值 | 来源 |
|---|---|---|
| instrumentType | EQUITY | settings.json |
| region | EUR | settings.json |
| universe | TOPCS1600 | settings.json |
| delay | 1 | settings.json |
| neutralization | SUBINDUSTRY | settings.json |
| decay | 4 | settings.json |
| truncation | 0.08 | settings.json |
| maxTrade | ON | settings.json |
| pasteurization | ON | settings.json |
| unitHandling | VERIFY | settings.json |
| nanHandling | ON | settings.json |
| language | FASTEXPR | settings.json |
| visualization | false | settings.json |
| startDate | 2014-01-01 | settings.json |
| endDate | 2023-12-31 | settings.json |

| 阈值 | 值 | 来源 |
|---|---|---|
| Mode B 主闸（sharpe / fitness） | 1.25 / 0.8 | default（实时值含区域台账，看 explain） |
| review.sharpe_min | 1.58 | thresholds.json |
| review.fitness_min | 1.0 | thresholds.json |
| review.turnover_min | 0.05 | thresholds.json |
| review.turnover_max | 0.3 | thresholds.json |
| review.two_year_sharpe_min | 1.6 | thresholds.json |
| review.rn_sharpe_min | 1.0 | thresholds.json |
| near.sharpe_min | 1.2 | thresholds.json |
| diversity.signal_floor.max_sharpe_floor | 0.5 | thresholds.json |

**循环与闸门（profile front-matter）**
- ⛔ 每波派发走**全量覆盖**：字段覆盖率 ≥ 100%、模板族 ≥ 3、边界算子档穷举（详见「全量覆盖操作纪律」）。
- 快判死：缺省（决策表 D15：新数据集 8 探针无 ／S／≥0.5 即判死）仅适用于单字段级——数据集级判死必须先通过三道覆盖闸，任何一闸未过都不允许判死该数据集
- 停止条件：白名单被 dead_end 全覆盖
- 停止条件：EUR/D1 结构性穷尽（2026-10-02 历史结论，2026-10-20 起冻结）——升 active 须出现 returns ≥ 0.05 且 prod 直方图不是密墙的新信号源，或全量覆盖闸三闸均过但候选 ／S／ 全 <0.5
- 闸门特化（文档级）：cw_gate=WARN——代码尚未读取（闸 7 恒 WARN，CW 在步 7 人工判），按此执行由 agent 负责

**平台事实**
- 宇宙跨多个国家（config.REGION_COUNTRY_SCOPE）：country 轴中性化 / 分组有意义
<!-- profiles:region-panel:end -->

## 组合分支（区域 × 类别）

<!-- profiles:cells-index:start -->
| 类别 | 分组 | 状态 | 回测覆盖 | 阈值覆盖 | 回测 / RA 全过 | prod 已测（低于上限） | 判死 / 胜绩 | 分支文件 |
|---|---|---|---|---|---|---|---|---|
| model | MODEL | active | — | — | 156 / 3 | 4（4） | 67 / 3 | [references/model.md](references/model.md) |
| other | Other | active | — | — | 119 / 0 | 19（1） | 20 / 0 | [references/other.md](references/other.md) |
| pv | PV | active | — | — | 108 / 10 | 0（0） | 12 / 0 | [references/pv.md](references/pv.md) |
| analyst | Analyst | active | — | — | 74 / 0 | 0（0） | 8 / 0 | [references/analyst.md](references/analyst.md) |
| news | News-Sentiment | active | — | — | 46 / 0 | 0（0） | 16 / 0 | [references/news.md](references/news.md) |
| fundamental | Fundamental | active | — | — | 41 / 2 | 6（0） | 7 / 0 | [references/fundamental.md](references/fundamental.md) |
| risk | Risk | active | — | — | 40 / 0 | 2（0） | 3 / 1 | [references/risk.md](references/risk.md) |
| institutions | Institutions | active | — | — | 22 / 0 | 0（0） | 3 / 0 | [references/institutions.md](references/institutions.md) |
| sentiment | News-Sentiment | active | — | — | 11 / 0 | 0（0） | 3 / 0 | [references/sentiment.md](references/sentiment.md) |
| insiders | Insider | active | — | — | 9 / 0 | 0（0） | 1 / 2 | [references/insiders.md](references/insiders.md) |
| earnings | Earnings | active | — | — | 4 / 0 | 0（0） | 1 / 0 | [references/earnings.md](references/earnings.md) |
| macro | Other | active | — | — | 0 / 0 | 0（0） | 0 / 0 | [references/macro.md](references/macro.md) |

说明：另有 20 条回测行没写数据集，无法归到组合；3 条判死 / 胜绩连类别也推断不出；证据于 2026-10-04 只读汇总。
<!-- profiles:cells-index:end -->

## 六步纵深骨架（本区覆盖）

> 通用方法见 [六步纵深骨架 · 通用主文档](../wq-brain-ra-pipeline/references/_six-step-core.md)。
> 本节只写 **EUR 的 override**：主 skills 未覆盖的本区平台事实、实测杠杆、已死轴、工程坑。
> **覆盖主 skills 同名条目；铁律与锁定项不可放宽。** 无实证处标「待实测」。

### ① 六法体检 · 本区覆盖

- **回测设置以 `settings.json` 为准**：`TOPCS1600` / `SUBINDUSTRY` / `decay 4` / `maxTrade ON` / `nanHandling ON`。
  ⚠ 历史台账里还有 `TOP2500` / `COUNTRY` / `decay 6` 的记录，**别混用**（换档否证：TOP2500 2.19 → TO…）。
- **待实测**：离线体检包退化范围、不可用算子。

### ② 组装 · 本区覆盖

- **⛔ 全量覆盖闸前置**：派批前必须过 `tools/full_coverage_gate.py --gate-mode enforce`（字段/模板族/边界算子三闸），任一未过不允许送回测。
- **禁止探针式派批**：8–10 槽位必须覆盖该数据集 ≥60% 字段（配合闸 1）且 ≥3 模板族（配合闸 2），不是"双结构 × 4 字段"的稀疏派发。
- **待实测**：本区组装禁区（新信号源优先）。

### ③ 归因 · 本区覆盖

- **结构性穷尽判据（2026-10-20 起冻结）**：库存 47/47 族 prod 都不低于上限、7 战役全 exhausted 的结论**只在探针式派发口径下成立**。2026-10-20 起改用全量覆盖闸，任何判死必须**三闸全过**才允许。
- **待实测**：本区逐年 S 分布（历史 win 机制 = 慢 MODEL 残差）。

### ④ 破闸杠杆 · 本区覆盖

- **未点亮塔路径数学上封闭**：`Fitness 上限 ≈ Sharpe × sqrt(returns / 0.125)`，而 **EUR 数据集 returns 普遍 < 0.03** ⇒ 不要只在同一金字塔里换字段。
- **★ 闸线（本区实测）**：`LOW_SHARPE` 1.58｜`LOW_FITNESS` 1.0｜`LOW_TURNOVER` 0.01｜`HIGH_TURNOVER` 0.7｜`LOW_2Y_SHARPE` 1.58｜`LOW_SUB_UNIVERSE_SHARPE` = **0.53×S（比率闸）**｜`LOW_ROBUST_UNIVERSE_SHARPE` 0.7。
- **★ 高 S 是双刃剑**：sub 是比率闸 ⇒ `sub/S < 0.53` 时任何 S 都过不了 ⇒ **选「刚好过主闸」的 S，不追最高 S**。

### ⑤ 算子穷举 · 本区覆盖

- **⛔ 边界算子白名单**：表达式里出现的每个算子，其参数必须落在 [references/_boundary-ops-eur.md](references/_boundary-ops-eur.md) 列出的合法档内；不在此表内的档需要**先补一次实测**、把档加进本表后再用。
- **近闸候选必须穷举 min_coverage 档**：cheap gate 已过但 RA 至少 1 项 FAIL 的候选，其表达式中每个算子的档位必须已试完边界清单里的 min_coverage 档（如 signed_power ≥3 档、ts_mean ≥2 档）。
- **机器可读版本**：`tracking/EUR/reference/boundary_ops_eur.json`（含 `poison_structures` 禁用结构清单）。
- **判定入口**：`tools/full_coverage_gate.py --near-gate`。

### ⑥ 终验 · 本区覆盖

- **数据集级判死唯一合法路径**：三道覆盖闸全过 + 全波次 |S|<0.5 ⇒ 该数据集可入 dead_end。任一闸未过 = 未做尽、**不允许**判死。
- **判死前必查**：`tools/full_coverage_gate.py --candidates <last_wave>.json --gate-mode enforce --campaign-dir tracking/EUR --json` 输出 `ok=true` 才允许提交 `seal_dead_end`。
- **升档条件**：出现 returns 达 0.05 且 prod 直方图不是密墙的新信号源，**或**三闸全过但候选 |S| 全 <0.5。

## 本区流程差异（相对九步骨架）

<!-- profiles:manual:start -->
- **入场**：2026-10-20 起 **full-coverage**（废止探针式派发）——数据集必须做尽：字段 100% 覆盖、模板族 ≥3、边界算子档穷举。历史 2026-10-02 判定的"结构性穷尽"（47/47 族 prod 都不低于上限、7 个战役全 exhausted）**只在探针式派发口径下成立**，本区升 active 须重跑全量覆盖闸。
- **S0 选集**：未点亮塔路径数学上封闭（Fitness 上限约为 Sharpe × sqrt(returns / 0.125)，EUR 数据集 returns 普遍低于 0.03）；不要只在同一金字塔里换字段。
- **S3 回测**：设置以 settings.json 为准（TOPCS1600 / SUBINDUSTRY / decay 4 / maxTrade ON / nanHandling ON）；历史台账里还有 TOP2500 / COUNTRY / decay 6 的记录，别混用。换档否证：TOP2500 2.19 → TOP1200 0.33 → TOP400 0.50。
- **S3 例外（已验证配方自带设置）**：`analyst7` 修订族 ATOM 必须 **TOP2500 / FAST / decay 40–80 / nanHandling ON / maxTrade ON**（与区域缺省不同）。`explain` 只回区域缺省，直发 MCP 要逐项显式传，否则跑的是另一条信号。一个 `create_multi_simulation` 只带一个 settings 块，参数名只认 snake_case——派发后读回一个子项断言 `nanHandling` / `maxTrade` 为 ON。完整配方见 [references/_atom-revision-playbook.md](references/_atom-revision-playbook.md)。
- **S4 改进**：prod 墙不是单一路径。① **残差化**（见 [EUR × fundamental](references/fundamental.md)：换维度、替换优于叠加、hump 档位；换分母在 EUR 是毒药）；② **同数据集换 metric 族**（analyst7 用 6 族出 14 颗，是最快的席位扩张）；③ **2Y/CV 修复用制度门控** `trade_when(abs(ts_zscore(<单字段水平值>, 66)) > 1.0, CORE, 0)`（`Grge2lN3` Recent-3yr CV 由 .436 降到 .366；计数门控反向）；④ decay / 平滑按形态分档（幅度 d40、广度 d80 + `ts_mean(·,5)`）。
- **S5 提交**：prod 与 self 双端点都取 max；**同族 p 变体互相关 0.97–0.99 ⇒ 每族只 1 席**，hump / decay 这类只改时序的变体全部作废（self 会爆）；「14 颗全过 ≠ 14 颗可同时提交」，analyst7 的最大互不相关团 = 7。
- **analyst 类别旧判死作废**：`analyst7` 不是 0.10 死集（旧记 299 字段是分页截断，真实 1111）；「Analyst 只能出 1 颗」「要凑 RA 腿必须离开 analyst」只对 `analyst_factor_signals` 旧结构成立。见 [references/analyst.md](references/analyst.md) 顶部覆盖说明。
（来源：EUR profile）

### ★★★★★ 数据集普查表（先读这个，跳开已判死族）

**EUR 共 173 个数据集 / 14 类**（未点亮 93 / 已测 ≈25 / 未测 60）。
全量清单 + 逐数据集判死速查（死因七分类）+ 未测集排序 见 [references/_dataset-inventory.md](references/_dataset-inventory.md)。

**组合候选清单（combo-candidate-inventory）**：EUR 版「正交骨架 × 加权饱和卫星」配方实证（含账本机制占用图、qfl 骨架、`subtract(骨架, w×rank(卫星))` 配方与 `w=0.5` 甜点） 见 [references/_combo-candidate-inventory.md](references/_combo-candidate-inventory.md)。
⇒ 开波前先读它，30 秒排除已判死族；**任何「穷尽」声明前必须重跑全量枚举**（曾经误记 21/33 个）。

### ★★★★★ 全量覆盖操作纪律（2026-10-20 定稿，废止探针式派发）

**核心口径**：一旦锁定某数据集，必须**枚举其全部字段语义维度 × 全部模板族**才算测完。**不允许"跑 10 条就换集"**。数据集级判死必须**先通过三道覆盖闸**：

| 闸 | 语义 | 判据 | 工具 |
|---|---|---|---|
| **1. 字段全量覆盖闸** | 数据集内每个字段至少出现在 1 条候选表达式里 | `coverage ≥ 1.0`（100%） | `tools/full_coverage_gate.py` |
| **2. 模板族全量闸** | 本数据集至少试跑 ≥3 个模板族 | `--min-families ≥ 3`（默认 3） | 同上 |
| **3. 边界算子穷举闸** | 表达式里每个算子的参数落在合法档；近闸候选已试完 min_coverage 档 | 见 [references/_boundary-ops-eur.md](references/_boundary-ops-eur.md) + `tracking/EUR/reference/boundary_ops_eur.json` | 同上 |

**开波顺序（不可跳步）**：

1. **反向检索**：查 `data/wqb.db::backtest_results` 里本 region 全部 RA 全过的 alpha，按 dataset 聚类、按 2Y≥1.58 排序，只从"已证明能出货"的集出发做尽（详见 MEMORY §0）。
2. **拉字段清单**：`tracking/EUR/reference/eur_<dataset>_fields.json` 或 MCP `get_datafields`；**无字段目录不允许派批**。
3. **画语义维度地图**：按经济机制（事件驱动 / 基本面 / 情绪 / 分析师 / 价量）分组，按 `alphaCount` 升序排。
4. **过覆盖闸**：`python tools/full_coverage_gate.py --region EUR --dataset <ds> --candidates <cand>.json --gate-mode enforce --campaign-dir tracking/EUR`；三闸全过才允许送 `wave_gate.py` 走回测。
5. **回测近闸候选**（cheap gate 过但 RA 未全过）必须启用 `--near-gate`：边界算子需已试完 min_coverage 档，否则 FAIL。
6. **判死条件**（**唯一合法**）：三闸全过 + 全波次 |S|<0.5 ⇒ 该数据集可入 dead_end；三闸任一未过 = 未做尽、不允许判死。

**⛔ 违规反例（禁做）**：
- 只跑 3-5 条表达式就换数据集 ⇒ 违反闸 1。
- 只用一种模板族（如只跑 `signed_power + group_rank`）⇒ 违反闸 2。
- 只测 `decay=4` 一档、只测 `signed_power 2.5` 一档 ⇒ 违反闸 3。
- 近闸候选未穷举 signed_power 全部档就换方向 ⇒ 违反闸 3 near_gate 分支。

**参考文件**：
- 边界算子清单（人可读）：[references/_boundary-ops-eur.md](references/_boundary-ops-eur.md)
- 边界算子配置（机器读）：`tracking/EUR/reference/boundary_ops_eur.json`
- 闸门脚本：`tools/full_coverage_gate.py`
- 已归档的探针 SOP（历史留档，**不再适用**）：`attic/probe_sop_retired_20261020/_probe-sop.md`

**EUR 设置档（平台权威 `get_platform_setting_options`）**：universe = `TOPCS1600`｜`TOP2500`｜`TOP1200`｜`TOP800`｜`TOP400`（实测 **TOPCS1600 最优**）；中性化 12 档（实测 **SUBINDUSTRY 最优**）；multi-sim **2–10 条**。
<!-- profiles:manual:end -->

## 改控制

- **区域级**：`tracking/EUR/config/settings.json`（仿真设置）、`tracking/EUR/config/thresholds.json`（阈值）。
- **组合级**：`tracking/EUR/config/cells.json`——只写覆盖值，每个覆盖在同级 `_evidence` 写证据（波号 / alpha id / 日期）；没有证据的覆盖校验不通过。改完先校验再重渲：

  ```bash
  $WQ_PY -m wqb.profiles check --region EUR
  $WQ_PY -m wqb.profiles render --region EUR --apply
  ```

- **锁定项**（任何层都不能放宽）：禁混信号、Mode B 主闸下限、决策表 D0-P、平台线、窗口白名单、点塔按平台类别、提交前用户确认、truncation 不作扫描维度——全文见 `$WQ_PY -m wqb.profiles explain` 末尾。
- **证据与历史**：[EUR profile](../wq-brain-ra-pipeline/references/regions/EUR.md)（入场裁决、红绿榜、证据附录）。
