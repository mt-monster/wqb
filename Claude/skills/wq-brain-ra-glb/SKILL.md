---
name: wq-brain-ra-glb
description: "在 GLB 区挖 REGULAR alpha、调 GLB 的回测设置或阈值、查 GLB 某类数据集（区域 × 类别组合）的配方与禁区时使用：GLB 的区域分支流程与回测把控面板。通用九步走 wq-brain-ra-pipeline，判提交与提交走 worldquant-submit-alpha。"
layer: L-RA-R
allowed-tools:
  - Read
  - Bash
  - mcp__wqb-db__*
  - mcp__wq-brain-http__*
version: "1.0"
last_verified: 2026-10-27
---

# GLB 区域挖掘流程（RA 区域分支）

## 职责边界

- **本 skill 负责**：GLB 的区域分支——入场状态、回测把控（区域与「区域 × 类别」组合的回测设置 / 阈值 / Mode B 主闸，每个值可查来源）、S1 / S2 / S4 / S5 的 GLB 差异步骤、组合分支文件索引。
- **本 skill 不做**：九步通用正文（→ [`wq-brain-ra-pipeline`](../wq-brain-ra-pipeline/SKILL.md)）；选区（→ `brain-next-move-analysis`）；判提交与提交（`submit_verdict` 只否决，提交走 `worldquant-submit-alpha` 且必须用户确认）；不改其它区域的控制文件。
- **上游 / 下游**：上游 = 用户点名 GLB，或 `wq-brain-ra-pipeline` 步 1 路由到本区；下游 = `wq-brain-ra-pipeline` 各步、`wq-brain-campaign-toolkit` 引擎、`wq-brain-alpha-optimization-v1`（S4 改进）。

## 怎么用

1. **入场**：看下面「区域控制面板」的入场状态。`frozen` 只走 profile 写明的后门；`probe-only` 只许探针批。
2. **每次回测前**按数据集取生效画像（回测设置、阈值、Mode B 主闸、生成与改进要点，每项带来源）：

   ```bash
   $WQ_PY -m wqb.profiles explain --region GLB --dataset <dataset>
   ```

   `workflow_batch_track` 会把该组合的回测覆盖以 `--set` 钉住；直接用 MCP 发仿真（`create_multi_simulation` / `create_simulation`）时，按 explain 输出逐项传设置，不要依赖工具缺省（各入口缺省不同，换档等于换信号）。
3. **走九步**：按 `wq-brain-ra-pipeline` 执行；步 3 / 4 / 7 / 8 先读对应组合的分支文件（下表最后一列）。
4. **步 9 回写之后**刷新组合证据并重渲本 skill：

   ```bash
   $WQ_PY -m wqb.profiles sync-cells --region GLB --apply
   $WQ_PY -m wqb.profiles render --region GLB --apply
   ```

<!-- region-scaffold:nav:start -->
| 目录 | 装什么 | 入口 |
|---|---|---|
| **SKILL.md** | 职责边界 + 怎么用 + 生成块（区域控制面板 / 组合分支 / 流程差异） | 本文 |
| [`rules/`](rules/README.md) | **GLB 独有规则与纪律**（六步覆盖、改控制、闸门与提交纪律） | [rules/README.md](rules/README.md) |
| [`config/`](config/README.md) | **配置视图**（真身在 `tracking/GLB/config/`）：三表分工、区域默认档、覆盖落差 | [config/README.md](config/README.md) |
| [`references/`](references/) | **实证**：`<类别>.md` 组合分支卡（render 生成）+ `_` 前缀专题（战役 / 手册 / 快照） | [references/](references/) |
| [`scripts/`](scripts/README.md) | 本 skill 级脚本（区域探针脚本家 = `tracking/GLB/scripts/`） | [scripts/README.md](scripts/README.md) |

细则不写在 SKILL.md：规则 → `rules/`，实证 → `references/`，配置 → `config/`，脚本 → `scripts/`。
<!-- region-scaffold:nav:end -->

## 区域控制面板

<!-- profiles:region-panel:start -->
**入场状态**：`active`　跨区铁律发源地：emotion 死路 + anl15 精确表达式封禁，铁律必读升强制

| 回测设置 | 值 | 来源 |
|---|---|---|
| instrumentType | EQUITY | settings.json |
| region | GLB | settings.json |
| universe | TOPDIV3000 | settings.json |
| delay | 1 | settings.json |
| neutralization | STATISTICAL | settings.json |
| decay | 2 | settings.json |
| truncation | 0.08 | settings.json |
| pasteurization | ON | settings.json |
| unitHandling | VERIFY | settings.json |
| nanHandling | OFF | settings.json |
| maxTrade | OFF | settings.json |
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
- 闸门特化（文档级）：cw_gate=WARN——代码尚未读取（闸 7 恒 WARN，CW 在步 7 人工判），按此执行由 agent 负责

**平台事实**
- 宇宙跨多个国家（config.REGION_COUNTRY_SCOPE）：country 轴中性化 / 分组有意义
<!-- profiles:region-panel:end -->

## 组合分支（区域 × 类别）

<!-- profiles:cells-index:start -->
| 类别 | 分组 | 状态 | 回测覆盖 | 阈值覆盖 | 回测 / RA 全过 | prod 已测（低于上限） | 判死 / 胜绩 | 分支文件 |
|---|---|---|---|---|---|---|---|---|
| model | MODEL | active | — | — | 857 / 1 | 1（0） | 6 / 0 | [references/model.md](references/model.md) |
| pv | PV | active | — | — | 753 / 68 | 43（11） | 9 / 2 | [references/pv.md](references/pv.md) |
| other | Other | active | — | — | 440 / 79 | 48（9） | 7 / 2 | [references/other.md](references/other.md) |
| fundamental | Fundamental | active | — | — | 70 / 0 | 0（0） | 4 / 0 | [references/fundamental.md](references/fundamental.md) |
| analyst | Analyst | active | — | — | 54 / 0 | 0（0） | 2 / 0 | [references/analyst.md](references/analyst.md) |
| news | News-Sentiment | active | — | — | 44 / 0 | 0（0） | 4 / 0 | [references/news.md](references/news.md) |
| risk | Risk | active | — | — | 41 / 13 | 10（0） | 3 / 0 | [references/risk.md](references/risk.md) |
| sentiment | News-Sentiment | active | — | — | 16 / 0 | 0（0） | 2 / 0 | [references/sentiment.md](references/sentiment.md) |
| earnings | Earnings | active | — | — | 8 / 0 | 0（0） | 1 / 0 | [references/earnings.md](references/earnings.md) |
| institutions | Institutions | active | — | — | 8 / 0 | 0（0） | 1 / 0 | [references/institutions.md](references/institutions.md) |
| insiders | Insider | active | — | — | 7 / 0 | 0（0） | 1 / 0 | [references/insiders.md](references/insiders.md) |
| macro | Other | active | — | — | 4 / 0 | 0（0） | 1 / 0 | [references/macro.md](references/macro.md) |

说明：另有 74 条回测行没写数据集，无法归到组合；1 条判死 / 胜绩连类别也推断不出；证据于 2026-10-04 只读汇总。
<!-- profiles:cells-index:end -->

## 六步纵深骨架（本区覆盖）

> 通用方法见 [六步纵深骨架 · 通用主文档](../wq-brain-ra-pipeline/references/_six-step-core.md)。
> 本节只写 **GLB 的 override**：主 skills 未覆盖的本区平台事实、实测杠杆、已死轴、工程坑。
> **覆盖主 skills 同名条目；铁律与锁定项不可放宽。** 无实证处标「待实测」。

### ① 六法体检 · 本区覆盖

- **入场**：active，但**已挖穿** —— 41 个判死族覆盖所有类别，获胜字段本身已被 prod 饱和闸拦。
  ⇒ **不要再开 atom 主信号**；转区或做 SuperAlpha。
- **待实测**：离线体检包退化范围、不可用算子。

### ② 组装 · 本区覆盖

- **两条铁律**：`emotion` 系**全排除**；`anl15` 按**精确表达式（sha1）封禁**，不按前缀通配。
- **出货机制**见 [GLB × pv](references/pv.md)（尾盘反转）与 [GLB × other](references/other.md)（dl 20 日 CNN × 子集门控）。

### ③ 归因 · 本区覆盖

- **沿用主 skills**。
- **待实测**：本区逐年 S 分布（本区已挖穿，新机制优先）。

### ④ 破闸杠杆 · 本区覆盖

- **跨区组合**的新信号族**首波 delay 1**，次波可探 delay 0 对照，**设置差异单独成批**。
- **待实测**：本区各闸最优杠杆。

### ⑤ 算子穷举 · 本区覆盖

- **子集门控只修 prod / robust、不造强度** —— 未门控基础信号 IS sharpe 不低于 2.5、fitness 不低于 1.0。

### ⑥ 终验 · 本区覆盖

- **待实测**：本区 prod 分布（已知饱和）。

## 本区流程差异（相对九步骨架）

<!-- profiles:manual:start -->
- **入场**：active，但已挖穿——41 个判死族覆盖所有类别，获胜字段本身已被 prod 饱和闸拦。不要再开 atom 主信号；转区或做 SuperAlpha（Claude 记忆 2026-09-27）。
- **S1 / S2**：emotion 系全排除；anl15 按精确表达式（sha1）封禁，不按前缀通配。两条出货机制见 [GLB × pv](references/pv.md)（尾盘反转）与 [GLB × other](references/other.md)（dl 20 日 CNN × 子集门控）。
- **S3 回测**：跨区组合的新信号族首波 delay 1，次波可探 delay 0 对照，设置差异单独成批。
- **S4 改进**：子集门控只修 prod / robust、不造强度——未门控基础信号 IS sharpe 不低于 2.5、fitness 不低于 1.5 才值得花槽位。
- **S9 回写**：每条判死都评估是否跨区普适；是就写成 GLOBAL 的 cross_region 条目，其他区步 1 自动读到。
（来源：GLB profile）
<!-- profiles:manual:end -->

## 改控制

- **区域级**：`tracking/GLB/config/settings.json`（仿真设置）、`tracking/GLB/config/thresholds.json`（阈值）。
- **组合级**：`tracking/GLB/config/cells.json`——只写覆盖值，每个覆盖在同级 `_evidence` 写证据（波号 / alpha id / 日期）；没有证据的覆盖校验不通过。改完先校验再重渲：

  ```bash
  $WQ_PY -m wqb.profiles check --region GLB
  $WQ_PY -m wqb.profiles render --region GLB --apply
  ```

- **锁定项**（任何层都不能放宽）：禁混信号、Mode B 主闸下限、决策表 D0-P、平台线、窗口白名单、点塔按平台类别、提交前用户确认、truncation 不作扫描维度——全文见 `$WQ_PY -m wqb.profiles explain` 末尾。
- **证据与历史**：[GLB profile](../wq-brain-ra-pipeline/references/regions/GLB.md)（入场裁决、红绿榜、证据附录）。
