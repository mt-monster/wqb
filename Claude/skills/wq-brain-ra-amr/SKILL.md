---
name: wq-brain-ra-amr
description: "在 AMR 区挖 REGULAR alpha、调 AMR 的回测设置或阈值、查 AMR 某类数据集（区域 × 类别组合）的配方与禁区时使用：AMR 的区域分支流程与回测把控面板。通用九步走 wq-brain-ra-pipeline，判提交与提交走 worldquant-submit-alpha。"
layer: L-RA-R
allowed-tools:
  - Read
  - Bash
  - mcp__wqb-db__*
  - mcp__wq-brain-http__*
version: "1.0"
last_verified: 2026-10-05
---

# AMR 区域挖掘流程（RA 区域分支）

## 职责边界

- **本 skill 负责**：AMR 的区域分支——入场状态、回测把控（区域与「区域 × 类别」组合的回测设置 / 阈值 / Mode B 主闸，每个值可查来源）、S1 / S2 / S4 / S5 的 AMR 差异步骤、组合分支文件索引。
- **本 skill 不做**：九步通用正文（→ [`wq-brain-ra-pipeline`](../wq-brain-ra-pipeline/SKILL.md)）；选区（→ `brain-next-move-analysis`）；判提交与提交（`submit_verdict` 只否决，提交走 `worldquant-submit-alpha` 且必须用户确认）；不改其它区域的控制文件。
- **上游 / 下游**：上游 = 用户点名 AMR，或 `wq-brain-ra-pipeline` 步 1 路由到本区；下游 = `wq-brain-ra-pipeline` 各步、`wq-brain-campaign-toolkit` 引擎、`wq-brain-alpha-optimization-v1`（S4 改进）。

## 怎么用

1. **入场**：看下面「区域控制面板」的入场状态。`frozen` 只走 profile 写明的后门；`probe-only` 只许探针批。
2. **每次回测前**按数据集取生效画像（回测设置、阈值、Mode B 主闸、生成与改进要点，每项带来源）：

   ```bash
   $WQ_PY -m wqb.profiles explain --region AMR --dataset <dataset>
   ```

   `workflow_batch_track` 会把该组合的回测覆盖以 `--set` 钉住；直接用 MCP 发仿真（`create_multi_simulation` / `create_simulation`）时，按 explain 输出逐项传设置，不要依赖工具缺省（各入口缺省不同，换档等于换信号）。
3. **走九步**：按 `wq-brain-ra-pipeline` 执行；步 3 / 4 / 7 / 8 先读对应组合的分支文件（下表最后一列）。
4. **步 9 回写之后**刷新组合证据并重渲本 skill：

   ```bash
   $WQ_PY -m wqb.profiles sync-cells --region AMR --apply
   $WQ_PY -m wqb.profiles render --region AMR --apply
   ```

<!-- region-scaffold:nav:start -->
| 目录 | 装什么 | 入口 |
|---|---|---|
| **SKILL.md** | 职责边界 + 怎么用 + 生成块（区域控制面板 / 组合分支 / 流程差异） | 本文 |
| [`rules/`](rules/README.md) | **AMR 独有规则与纪律**（六步覆盖、改控制、闸门与提交纪律） | [rules/README.md](rules/README.md) |
| [`config/`](config/README.md) | **配置视图**（真身在 `tracking/AMR/config/`）：三表分工、区域默认档、覆盖落差 | [config/README.md](config/README.md) |
| [`references/`](references/) | **实证**：`<类别>.md` 组合分支卡（render 生成）+ `_` 前缀专题（战役 / 手册 / 快照） | [references/](references/) |
| [`scripts/`](scripts/README.md) | 本 skill 级脚本（区域探针脚本家 = `tracking/AMR/scripts/`） | [scripts/README.md](scripts/README.md) |

细则不写在 SKILL.md：规则 → `rules/`，实证 → `references/`，配置 → `config/`，脚本 → `scripts/`。
<!-- region-scaffold:nav:end -->

## 区域控制面板

<!-- profiles:region-panel:start -->
**入场状态**：`active`　AMR（美洲）持续自我挖掘：TOP600 小宇宙 delay1，SUBINDUSTRY 跟 win，绿榜 analyst/insiders/pv 主攻 + Other/PV/Risk/ShortInterest 未点亮塔，8 探针快判死

| 回测设置 | 值 | 来源 |
|---|---|---|
| instrumentType | EQUITY | settings.json |
| region | AMR | settings.json |
| universe | TOP600 | settings.json |
| delay | 1 | settings.json |
| neutralization | SUBINDUSTRY | settings.json |
| decay | 4 | settings.json |
| truncation | 0.08 | settings.json |
| pasteurization | ON | settings.json |
| unitHandling | VERIFY | settings.json |
| nanHandling | OFF | settings.json |
| maxTrade | OFF | settings.json |
| language | FASTEXPR | settings.json |
| visualization | false | settings.json |
| startDate | 2013-01-01 | settings.json |
| endDate | 2023-12-31 | settings.json |

| 阈值 | 值 | 来源 |
|---|---|---|
| Mode B 主闸（sharpe / fitness） | 1.25 / 0.8 | default（实时值含区域台账，看 explain） |
| review.sharpe_min | 1.58 | thresholds.json |
| review.fitness_min | 1.0 | thresholds.json |
| review.turnover_min | 0.01 | thresholds.json |
| review.turnover_max | 0.7 | thresholds.json |
| review.two_year_sharpe_min | 1.0 | thresholds.json |
| near.sharpe_min | 1.0 | thresholds.json |
| diversity.signal_floor.max_sharpe_floor | 0.5 | thresholds.json |

**循环与闸门（profile front-matter）**
- 每波探针位上限：8
- 快判死：新数据集只给 8 条探针预算，无 ／S／≥0.5 即写 dead_end 回写，不扩批、不换设置重试
- 停止条件：白名单被 dead_end 全覆盖
- 停止条件：连续 3 波全 FAIL 且无新 dead_end
- 停止条件：连续 3 波 gate 通过率=0
- 闸门特化（文档级）：cw_gate=FAIL、longcount_min=80、longcount_verdict=FAIL、prod_corr_early_warn=0.7——代码尚未读取（闸 7 恒 WARN，CW 在步 7 人工判），按此执行由 agent 负责

**平台事实**
- 宇宙跨多个国家（config.REGION_COUNTRY_SCOPE）：country 轴中性化 / 分组有意义
<!-- profiles:region-panel:end -->

## 组合分支（区域 × 类别）

<!-- profiles:cells-index:start -->
| 类别 | 分组 | 状态 | 回测覆盖 | 阈值覆盖 | 回测 / RA 全过 | prod 已测（低于上限） | 判死 / 胜绩 | 分支文件 |
|---|---|---|---|---|---|---|---|---|
| analyst | Analyst | active | — | — | 80 / 0 | 0（0） | 1 / 0 | [references/analyst.md](references/analyst.md) |
| pv | PV | active | — | — | 24 / 0 | 0（0） | 1 / 0 | [references/pv.md](references/pv.md) |

说明：证据于 2026-10-04 只读汇总。
<!-- profiles:cells-index:end -->

## 六步纵深骨架（本区覆盖）

> 通用方法见 [六步纵深骨架 · 通用主文档](../wq-brain-ra-pipeline/references/_six-step-core.md)。
> 本节只写 **AMR 的 override**：主 skills 未覆盖的本区平台事实、实测杠杆、已死轴、工程坑。
> **覆盖主 skills 同名条目；铁律与锁定项不可放宽。** 无实证处标「待实测」。

### ① 六法体检 · 本区覆盖

- **平台档位**：universe 只有 `TOP600`、delay 只 `1`；中性化 **7 选**（**没有 CROWDING / FAST / SLOW**），`SUBINDUSTRY` 跟 win。
- **待实测**：离线体检包在本区的退化范围、在线体检设置档（当前无记录）。
- **不可用算子**：本区未见记录 ⇒ 沿用主 skills，发批前按「新算子小批验存在性」自检。

### ② 组装 · 本区覆盖

- **已验证形状**：事件类用 `trade_when` / `if_else` / `ts_arg_max` / `days_from_last_change`。
- **观察名单**：`longCount` 低于 80 的 VECTOR 字段进观察（profile 要求 FAIL，代码闸 7 仍 WARN）。
- **S0 选集**：红榜 chart_patterns / news_sentiment / ai_ml / credit_risk / glb_emotion；绿榜 analyst / insiders / pv；MODEL 数据集不作主数据集。

### ③ 归因 · 本区覆盖

- **沿用主 skills**（本区归因实证尚无记录）。
- **待实测**：本区归因常见误判（先跑 `get_alpha_yearly_stats` + `get_alpha_pnl` 建立基线）。

### ④ 破闸杠杆 · 本区覆盖

- **中性化**：只有 7 档（无 CROWDING / FAST / SLOW）⇒ **主 skills 的「逐族重扫全档」在本区即这 7 档**；`SUBINDUSTRY` 跟 win。
- **待实测**：各闸最优杠杆与数值 —— **禁止照搬别区**（KOR 的 CROWDING×decay12 在本区不适用，本区无 CROWDING）。

### ⑤ 算子穷举 · 本区覆盖

- **待实测**：本区有效 / 有害算子清单（先用小批验存在性，再逐族记）。

### ⑥ 终验 · 本区覆盖

- **快判死**：新数据集 8 探针无 ／S／≥0.5 即判死回写，不扩批。
- **待实测**：本区 prod 直方图分布（密墙 / 白空间）。

## 本区流程差异（相对九步骨架）

<!-- profiles:manual:start -->
- **档位**：universe 只有 TOP600、delay 只 1；中性化 7 选（没有 CROWDING / FAST / SLOW），SUBINDUSTRY 跟 win。
- **S0 选集**：红榜 chart_patterns / news_sentiment / ai_ml / credit_risk / glb_emotion；绿榜 analyst / insiders / pv；MODEL 数据集不作主数据集。跨区死路只认 registry 的族级 dead_end。
- **S1 / S2**：longCount 低于 80 的 VECTOR 字段进观察名单（profile 要求 FAIL，代码闸 7 仍 WARN）；事件类用 trade_when / if_else / ts_arg_max / days_from_last_change 等已验证形状。
- **S3 / S4**：8 探针快判死；CW 超过 0.5 判死不回炉（profile 要求）。
- **停止闸**：本次任务新挖 20 个可提交 alpha（用户 2026-09-28 战役令）。
（来源：AMR profile）
<!-- profiles:manual:end -->

## 改控制

- **区域级**：`tracking/AMR/config/settings.json`（仿真设置）、`tracking/AMR/config/thresholds.json`（阈值）。
- **组合级**：`tracking/AMR/config/cells.json`——只写覆盖值，每个覆盖在同级 `_evidence` 写证据（波号 / alpha id / 日期）；没有证据的覆盖校验不通过。改完先校验再重渲：

  ```bash
  $WQ_PY -m wqb.profiles check --region AMR
  $WQ_PY -m wqb.profiles render --region AMR --apply
  ```

- **锁定项**（任何层都不能放宽）：禁混信号、Mode B 主闸下限、决策表 D0-P、平台线、窗口白名单、点塔按平台类别、提交前用户确认、truncation 不作扫描维度——全文见 `$WQ_PY -m wqb.profiles explain` 末尾。
- **证据与历史**：[AMR profile](../wq-brain-ra-pipeline/references/regions/AMR.md)（入场裁决、红绿榜、证据附录）。
