---
name: wq-brain-ra-mea
description: "在 MEA 区挖 REGULAR alpha、调 MEA 的回测设置或阈值、查 MEA 某类数据集（区域 × 类别组合）的配方与禁区时使用：MEA 的区域分支流程与回测把控面板。通用九步走 wq-brain-ra-pipeline，判提交与提交走 worldquant-submit-alpha。"
layer: L-RA-R
allowed-tools:
  - Read
  - Bash
  - mcp__wqb-db__*
  - mcp__wq-brain-http__*
version: "1.0"
last_verified: 2026-10-05
---

# MEA 区域挖掘流程（RA 区域分支）

## 职责边界

- **本 skill 负责**：MEA 的区域分支——入场状态、回测把控（区域与「区域 × 类别」组合的回测设置 / 阈值 / Mode B 主闸，每个值可查来源）、S1 / S2 / S4 / S5 的 MEA 差异步骤、组合分支文件索引。
- **本 skill 不做**：九步通用正文（→ [`wq-brain-ra-pipeline`](../wq-brain-ra-pipeline/SKILL.md)）；选区（→ `brain-next-move-analysis`）；判提交与提交（`submit_verdict` 只否决，提交走 `worldquant-submit-alpha` 且必须用户确认）；不改其它区域的控制文件。
- **上游 / 下游**：上游 = 用户点名 MEA，或 `wq-brain-ra-pipeline` 步 1 路由到本区；下游 = `wq-brain-ra-pipeline` 各步、`wq-brain-campaign-toolkit` 引擎、`wq-brain-alpha-optimization-v1`（S4 改进）。

## 怎么用

1. **入场**：看下面「区域控制面板」的入场状态。`frozen` 只走 profile 写明的后门；`probe-only` 只许探针批。
2. **每次回测前**按数据集取生效画像（回测设置、阈值、Mode B 主闸、生成与改进要点，每项带来源）：

   ```bash
   $WQ_PY -m wqb.profiles explain --region MEA --dataset <dataset>
   ```

   `workflow_batch_track` 会把该组合的回测覆盖以 `--set` 钉住；直接用 MCP 发仿真（`create_multi_simulation` / `create_simulation`）时，按 explain 输出逐项传设置，不要依赖工具缺省（各入口缺省不同，换档等于换信号）。
3. **走九步**：按 `wq-brain-ra-pipeline` 执行；步 3 / 4 / 7 / 8 先读对应组合的分支文件（下表最后一列）。
4. **步 9 回写之后**刷新组合证据并重渲本 skill：

   ```bash
   $WQ_PY -m wqb.profiles sync-cells --region MEA --apply
   $WQ_PY -m wqb.profiles render --region MEA --apply
   ```

## 区域控制面板

<!-- profiles:region-panel:start -->
**入场状态**：`frozen`　TOP400 全区判死：9 数据集全 exhausted，入口即拒，仅留用户强制的 probe-only 后门

| 回测设置 | 值 | 来源 |
|---|---|---|
| instrumentType | EQUITY | settings.json |
| region | MEA | settings.json |
| universe | TOP400 | settings.json |
| delay | 1 | settings.json |
| neutralization | SECTOR | settings.json |
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
| near.sharpe_min | 1.2 | thresholds.json |
| diversity.signal_floor.max_sharpe_floor | 1.2 | thresholds.json |

**循环与闸门（profile front-matter）**
- 每波探针位上限：1
- 快判死：frozen 态不适用；probe-only 后门单波 8 探针上限
- 停止条件：默认停止：全区 exhausted
- 闸门特化（文档级）：cw_gate=FAIL——代码尚未读取（闸 7 恒 WARN，CW 在步 7 人工判），按此执行由 agent 负责

**平台事实**
- 宇宙跨多个国家（config.REGION_COUNTRY_SCOPE）：country 轴中性化 / 分组有意义
<!-- profiles:region-panel:end -->

## 组合分支（区域 × 类别）

<!-- profiles:cells-index:start -->
| 类别 | 分组 | 状态 | 回测覆盖 | 阈值覆盖 | 回测 / RA 全过 | prod 已测（低于上限） | 判死 / 胜绩 | 分支文件 |
|---|---|---|---|---|---|---|---|---|
| analyst | Analyst | archived | — | — | 76 / 13 | 49（16） | 1 / 5 | [references/analyst.md](references/analyst.md) |
| fundamental | Fundamental | archived | — | — | 25 / 1 | 6（1） | 8 / 2 | [references/fundamental.md](references/fundamental.md) |
| earnings | Earnings | archived | — | — | 10 / 1 | 0（0） | 1 / 0 | [references/earnings.md](references/earnings.md) |
| pv | PV | archived | — | — | 8 / 0 | 2（0） | 5 / 0 | [references/pv.md](references/pv.md) |
| model | MODEL | archived | — | — | 0 / 0 | 4（4） | 3 / 0 | [references/model.md](references/model.md) |

说明：另有 379 条回测行没写数据集，无法归到组合；7 条判死 / 胜绩连类别也推断不出；证据于 2026-10-04 只读汇总。
<!-- profiles:cells-index:end -->

## 本区流程差异（相对九步骨架）

<!-- profiles:manual:start -->
- **入场即拒**：9 个数据集全部 exhausted。唯一后门：用户明确要求继续时，只探白名单外新上线的数据集，单波 8 探针，一波结束无论成败回到 frozen，事先说明配额成本。
- **SuperAlpha**：MEA 的 SUPER 通道已关闭（POST /simulations 带 region=MEA 返回 400），既有 2 颗是存量。
- 死路记录保留，作 HKG / TWN 等小宇宙区的跨区语料。
（来源：MEA profile）
<!-- profiles:manual:end -->

## 改控制

- **区域级**：`tracking/MEA/config/settings.json`（仿真设置）、`tracking/MEA/config/thresholds.json`（阈值）。
- **组合级**：`tracking/MEA/config/cells.json`——只写覆盖值，每个覆盖在同级 `_evidence` 写证据（波号 / alpha id / 日期）；没有证据的覆盖校验不通过。改完先校验再重渲：

  ```bash
  $WQ_PY -m wqb.profiles check --region MEA
  $WQ_PY -m wqb.profiles render --region MEA --apply
  ```

- **锁定项**（任何层都不能放宽）：禁混信号、Mode B 主闸下限、决策表 D0-P、平台线、窗口白名单、点塔按平台类别、提交前用户确认、truncation 不作扫描维度——全文见 `$WQ_PY -m wqb.profiles explain` 末尾。
- **证据与历史**：[MEA profile](../wq-brain-ra-pipeline/references/regions/MEA.md)（入场裁决、红绿榜、证据附录）。
