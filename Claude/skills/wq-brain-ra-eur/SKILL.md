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

1. **入场**：看下面「区域控制面板」的入场状态。`frozen` 只走 profile 写明的后门；`probe-only` 只许探针批。
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
**入场状态**：`probe-only`　2026-10-02 起 probe-only：EUR/D1 被项目自身实证判为结构性穷尽（库存 47/47 族 prod ≥ 0.70、7 个战役全 exhausted、23 条高 Sharpe 未测簇核实后可提交新增 = 0）；历史 win 机制 = 慢 MODEL 残差 × 快 PV（0.4/0.6 加权写法已被闸 5 禁止，只许条件 / 分组 / 残差三式），SUBINDUSTRY + decay4

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
- 每波探针位上限：1
- 快判死：缺省（决策表 D15：新数据集 8 探针无 ／S／≥0.5 即判死）；本区无额外规则
- 停止条件：白名单被 dead_end 全覆盖
- 停止条件：EUR/D1 结构性穷尽（2026-10-02）——升 active 须出现 returns ≥ 0.05 且 prod 直方图不是密墙的新信号源
- 闸门特化（文档级）：cw_gate=WARN——代码尚未读取（闸 7 恒 WARN，CW 在步 7 人工判），按此执行由 agent 负责

**平台事实**
- 宇宙跨多个国家（config.REGION_COUNTRY_SCOPE）：country 轴中性化 / 分组有意义
<!-- profiles:region-panel:end -->

## 组合分支（区域 × 类别）

<!-- profiles:cells-index:start -->
| 类别 | 分组 | 状态 | 回测覆盖 | 阈值覆盖 | 回测 / RA 全过 | prod 已测（低于上限） | 判死 / 胜绩 | 分支文件 |
|---|---|---|---|---|---|---|---|---|
| model | MODEL | probe | — | — | 156 / 3 | 4（4） | 67 / 3 | [references/model.md](references/model.md) |
| other | Other | probe | — | — | 119 / 0 | 19（1） | 20 / 0 | [references/other.md](references/other.md) |
| pv | PV | probe | — | — | 108 / 10 | 0（0） | 12 / 0 | [references/pv.md](references/pv.md) |
| analyst | Analyst | probe | — | — | 74 / 0 | 0（0） | 8 / 0 | [references/analyst.md](references/analyst.md) |
| news | News-Sentiment | probe | — | — | 46 / 0 | 0（0） | 16 / 0 | [references/news.md](references/news.md) |
| fundamental | Fundamental | probe | — | — | 41 / 2 | 6（0） | 7 / 0 | [references/fundamental.md](references/fundamental.md) |
| risk | Risk | probe | — | — | 40 / 0 | 2（0） | 3 / 1 | [references/risk.md](references/risk.md) |
| institutions | Institutions | probe | — | — | 22 / 0 | 0（0） | 3 / 0 | [references/institutions.md](references/institutions.md) |
| sentiment | News-Sentiment | probe | — | — | 11 / 0 | 0（0） | 3 / 0 | [references/sentiment.md](references/sentiment.md) |
| insiders | Insider | probe | — | — | 9 / 0 | 0（0） | 1 / 2 | [references/insiders.md](references/insiders.md) |
| earnings | Earnings | probe | — | — | 4 / 0 | 0（0） | 1 / 0 | [references/earnings.md](references/earnings.md) |
| macro | Other | probe | — | — | 0 / 0 | 0（0） | 0 / 0 | [references/macro.md](references/macro.md) |

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

- **沿用主 skills**。
- **待实测**：本区组装禁区（本区已判结构性穷尽，新信号源优先）。

### ③ 归因 · 本区覆盖

- **结构性穷尽判据**：库存 **47 / 47 族 prod 都不低于上限**、7 个战役全 exhausted ⇒ 归因读数多指向「prod 密墙」而非强度不足。
- **待实测**：本区逐年 S 分布（历史 win 机制 = 慢 MODEL 残差）。

### ④ 破闸杠杆 · 本区覆盖

- **未点亮塔路径数学上封闭**：`Fitness 上限 ≈ Sharpe × sqrt(returns / 0.125)`，而 **EUR 数据集 returns 普遍 < 0.03** ⇒ 不要只在同一金字塔里换字段。
- **★ 闸线（本区实测）**：`LOW_SHARPE` 1.58｜`LOW_FITNESS` 1.0｜`LOW_TURNOVER` 0.01｜`HIGH_TURNOVER` 0.7｜`LOW_2Y_SHARPE` 1.58｜`LOW_SUB_UNIVERSE_SHARPE` = **0.53×S（比率闸）**｜`LOW_ROBUST_UNIVERSE_SHARPE` 0.7。
- **★ 高 S 是双刃剑**：sub 是比率闸 ⇒ `sub/S < 0.53` 时任何 S 都过不了 ⇒ **选「刚好过主闸」的 S，不追最高 S**。

### ⑤ 算子穷举 · 本区覆盖

- **待实测**：本区算子实证。

### ⑥ 终验 · 本区覆盖

- **待实测**：本区 prod 分布（已知 47/47 族 ≥ 上限，属密墙）。
- **升档条件**：出现 returns 达 0.05 且 prod 直方图不是密墙的新信号源。

## 本区流程差异（相对九步骨架）

<!-- profiles:manual:start -->
- **入场**：2026-10-02 起 probe-only——库存 47 / 47 族 prod 都不低于上限、7 个战役全 exhausted。升 active 须出现 returns 达 0.05 且 prod 直方图不是密墙的新信号源。
- **S0 选集**：未点亮塔路径数学上封闭（Fitness 上限约为 Sharpe × sqrt(returns / 0.125)，EUR 数据集 returns 普遍低于 0.03）；不要只在同一金字塔里换字段。
- **S3 回测**：设置以 settings.json 为准（TOPCS1600 / SUBINDUSTRY / decay 4 / maxTrade ON / nanHandling ON）；历史台账里还有 TOP2500 / COUNTRY / decay 6 的记录，别混用。换档否证：TOP2500 2.19 → TOP1200 0.33 → TOP400 0.50。
- **S4 改进**：破 prod 墙只有残差化一条路，见 [EUR × fundamental](references/fundamental.md)（换维度、替换优于叠加、hump 档位；换分母在 EUR 是毒药）。
- **S5 提交**：prod 与 self 双端点都取 max；同族已有提交时，hump / decay 这类只改时序的变体全部作废（self 会爆）。
（来源：EUR profile）

### ★★★★★ 数据集普查表（先读这个，跳开已判死族）

**EUR 共 173 个数据集 / 14 类**（未点亮 93 / 已测 ≈25 / 未测 60）。
全量清单 + 逐数据集判死速查（死因七分类）+ 未测集排序 见 [references/_dataset-inventory.md](references/_dataset-inventory.md)。

**组合候选清单（combo-candidate-inventory）**：EUR 版「正交骨架 × 加权饱和卫星」配方实证（含账本机制占用图、qfl 骨架、`subtract(骨架, w×rank(卫星))` 配方与 `w=0.5` 甜点） 见 [references/_combo-candidate-inventory.md](references/_combo-candidate-inventory.md)。
⇒ 开波前先读它，30 秒排除已判死族；**任何「穷尽」声明前必须重跑全量枚举**（曾经误记 21/33 个）。

### ★★★★★ 探针派发 SOP（2026-10-13 定稿，全文见 [references/_probe-sop.md](references/_probe-sop.md)）

**8–10 槽 = 2 个已验证结构 × 3–4 跨族字段 + 2 机动（`vec_max` / `reverse`）**。读数三分法（EUR 口径）：

| 双结构最好读数 | 动作 |
|---|---|
| S ≥ 1.58 且 2Y ≥ 1.58 且 F ≥ 1.0 | 全闸验证 → PnL 互相关去重（一条腿 1 颗） |
| S 1.0–1.58 或 F 0.6–1.0（returns ≥ 3.5%） | **不判死**——「结构没找对」信号带；升级幂次 / 轴 / `ts_mean` 分母 / tvr |
| **反算 returns < 3.5%** | **判死**（F 闸数学封顶）：`returns = max(TO,0.125)×(F/S)²`，过闸需 **`S ≥ sqrt(0.125/returns)`** |
| 双结构 S < 0.5 | 判死；同族字段免测 |

**EUR 失败模式预筛（开波前即可定论）**：① news/sentiment/事件 VECTOR ⇒ **TO 爆炸**（`news20` cov 0.963 亦爆）；② 噪声型 ⇒ **平滑即杀**；③ 低频 MATRIX / 事件计数 ⇒ **returns 不足**；④ **S > 4 且 TO 打满 = 数据伪影**（非发现）。

**反例驱动的五条铁律**：① 新数据集首派前**逐字段核对平台实时名**（`oth553_rec_poscnt` 不存在 ⇒ 整批 ERROR）；② 宣称「穷尽」前**全量枚举**（`/data-sets` 不带 `limit`，带 `limit=100` 会 400）；③ **双结构保底**（只测一个会错杀字段）；④ 出闸后先算 **PnL 互相关**再决定投哪颗（Analyst 同族 4 颗 0.976–0.999 ⇒ 只出 1 颗）；⑤ **复现赢家必须拉它自己的 settings**（区域缺省 `decay 4` 使 Analyst 腿 F 1.09→0.97 掉闸）。

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
