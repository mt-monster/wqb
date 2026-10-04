---
name: wq-brain-ra-usa
description: "在 USA 区挖 REGULAR alpha、调 USA 的回测设置或阈值、查 USA 某类数据集（区域 × 类别组合）的配方与禁区时使用：USA 的区域分支流程与回测把控面板。通用九步走 wq-brain-ra-pipeline，判提交与提交走 worldquant-submit-alpha。"
layer: L-RA-R
allowed-tools:
  - Read
  - Bash
  - mcp__wqb-db__*
  - mcp__wq-brain-http__*
version: "1.0"
last_verified: 2026-10-05
---

# USA 区域挖掘流程（RA 区域分支）

## 职责边界

- **本 skill 负责**：USA 的区域分支——入场状态、回测把控（区域与「区域 × 类别」组合的回测设置 / 阈值 / Mode B 主闸，每个值可查来源）、S1 / S2 / S4 / S5 的 USA 差异步骤、组合分支文件索引。
- **本 skill 不做**：九步通用正文（→ [`wq-brain-ra-pipeline`](../wq-brain-ra-pipeline/SKILL.md)）；选区（→ `brain-next-move-analysis`）；判提交与提交（`submit_verdict` 只否决，提交走 `worldquant-submit-alpha` 且必须用户确认）；不改其它区域的控制文件。
- **上游 / 下游**：上游 = 用户点名 USA，或 `wq-brain-ra-pipeline` 步 1 路由到本区；下游 = `wq-brain-ra-pipeline` 各步、`wq-brain-campaign-toolkit` 引擎、`wq-brain-alpha-optimization-v1`（S4 改进）。

## 怎么用

1. **入场**：看下面「区域控制面板」的入场状态。`frozen` 只走 profile 写明的后门；`probe-only` 只许探针批。
2. **每次回测前**按数据集取生效画像（回测设置、阈值、Mode B 主闸、生成与改进要点，每项带来源）：

   ```bash
   $WQ_PY -m wqb.profiles explain --region USA --dataset <dataset>
   ```

   `workflow_batch_track` 会把该组合的回测覆盖以 `--set` 钉住；直接用 MCP 发仿真（`create_multi_simulation` / `create_simulation`）时，按 explain 输出逐项传设置，不要依赖工具缺省（各入口缺省不同，换档等于换信号）。
3. **走九步**：按 `wq-brain-ra-pipeline` 执行；步 3 / 4 / 7 / 8 先读对应组合的分支文件（下表最后一列）。
4. **步 9 回写之后**刷新组合证据并重渲本 skill：

   ```bash
   $WQ_PY -m wqb.profiles sync-cells --region USA --apply
   $WQ_PY -m wqb.profiles render --region USA --apply
   ```

## 区域控制面板

<!-- profiles:region-panel:start -->
**入场状态**：`active`　最深最饱和市场：value/quality 种子全死，靠 option/analyst 新集 + 强制正交

| 回测设置 | 值 | 来源 |
|---|---|---|
| instrumentType | EQUITY | settings.json |
| region | USA | settings.json |
| universe | TOP3000 | settings.json |
| delay | 1 | settings.json |
| neutralization | SUBINDUSTRY | settings.json |
| decay | 5 | settings.json |
| truncation | 0.08 | settings.json |
| maxTrade | OFF | settings.json |
| pasteurization | ON | settings.json |
| unitHandling | VERIFY | settings.json |
| nanHandling | ON | settings.json |
| language | FASTEXPR | settings.json |
| visualization | false | settings.json |
| startDate | 2013-01-01 | settings.json |
| endDate | 2023-12-31 | settings.json |

| 阈值 | 值 | 来源 |
|---|---|---|
| Mode B 主闸（sharpe / fitness） | 1.25 / 0.8 | default（实时值含区域台账，看 explain） |
| review.sharpe_min | 1.25 | thresholds.json |
| review.fitness_min | 1.0 | thresholds.json |
| review.turnover_min | 0.05 | thresholds.json |
| review.turnover_max | 0.3 | thresholds.json |
| review.two_year_sharpe_min | 1.6 | thresholds.json |
| near.sharpe_min | 1.0 | thresholds.json |
| diversity.signal_floor.max_sharpe_floor | 0.9 | thresholds.json |

**循环与闸门（profile front-matter）**
- 每波探针位上限：1
- 快判死：缺省（决策表 D15：新数据集 8 探针无 ／S／≥0.5 即判死）；本区无额外规则
- 停止条件：白名单被 dead_end 全覆盖
- 闸门特化（文档级）：cw_gate=WARN——代码尚未读取（闸 7 恒 WARN，CW 在步 7 人工判），按此执行由 agent 负责

**平台事实**
- 宇宙是单一国家（config.REGION_COUNTRY_SCOPE）：country 轴中性化 / 分组等于全市场，别用
<!-- profiles:region-panel:end -->

## 组合分支（区域 × 类别）

<!-- profiles:cells-index:start -->
| 类别 | 分组 | 状态 | 回测覆盖 | 阈值覆盖 | 回测 / RA 全过 | prod 已测（低于上限） | 判死 / 胜绩 | 分支文件 |
|---|---|---|---|---|---|---|---|---|
| model | MODEL | active | — | — | 557 / 1 | 4（4） | 12 / 0 | [references/model.md](references/model.md) |
| other | Other | active | — | — | 211 / 2 | 15（4） | 9 / 0 | [references/other.md](references/other.md) |
| pv | PV | active | — | — | 154 / 1 | 2（1） | 3 / 0 | [references/pv.md](references/pv.md) |
| shortinterest | ShortInterest | active | — | — | 78 / 0 | 0（0） | 1 / 1 | [references/shortinterest.md](references/shortinterest.md) |
| institutions | Institutions | active | — | — | 56 / 6 | 1（0） | 0 / 0 | [references/institutions.md](references/institutions.md) |
| option | Option | active | — | — | 25 / 0 | 0（0） | 4 / 0 | [references/option.md](references/option.md) |
| analyst | Analyst | active | — | — | 19 / 0 | 1（0） | 2 / 0 | [references/analyst.md](references/analyst.md) |
| insiders | Insider | active | — | — | 8 / 0 | 0（0） | 1 / 0 | [references/insiders.md](references/insiders.md) |
| news | News-Sentiment | active | — | — | 0 / 0 | 0（0） | 1 / 0 | [references/news.md](references/news.md) |
| sentiment | News-Sentiment | active | — | — | 0 / 0 | 0（0） | 1 / 0 | [references/sentiment.md](references/sentiment.md) |

说明：另有 99 条回测行没写数据集，无法归到组合；8 条判死 / 胜绩连类别也推断不出；证据于 2026-10-04 只读汇总。
<!-- profiles:cells-index:end -->

## 本区流程差异（相对九步骨架）

<!-- profiles:manual:start -->
- **S0 / S2**：最深最饱和的市场——经典 value / quality / book 及其线性变体必死（book/value 单族 145 颗同族 ACTIVE）；priors 硬排除饱和族，生成后命中饱和族的在选波阶段剔除。
- **S3 回测**：扩批之前先按族查 prod-first；delay 0 探针单独成批，不与 delay 1 混批。
- **S4 改进**：同族出现 prod 达 0.6 → 只按决策表 D0-P 处置（0.60–0.70 当天进步 8；达 0.75 或踩线尝试失败判 dead_end 并换正交概念），禁止同族磨参数。修复保持 TOP3000；换 universe 要在 key_findings 写清 TOP3000 下失败的原因与要回答的诊断问题。
- **Mode B**：原来的 1.0 / 0.6 降门已被下限锁作废；单腿偏弱的组腿起点候选走旁路 A–E。
（来源：USA profile）
<!-- profiles:manual:end -->

## 改控制

- **区域级**：`tracking/USA/config/settings.json`（仿真设置）、`tracking/USA/config/thresholds.json`（阈值）。
- **组合级**：`tracking/USA/config/cells.json`——只写覆盖值，每个覆盖在同级 `_evidence` 写证据（波号 / alpha id / 日期）；没有证据的覆盖校验不通过。改完先校验再重渲：

  ```bash
  $WQ_PY -m wqb.profiles check --region USA
  $WQ_PY -m wqb.profiles render --region USA --apply
  ```

- **锁定项**（任何层都不能放宽）：禁混信号、Mode B 主闸下限、决策表 D0-P、平台线、窗口白名单、点塔按平台类别、提交前用户确认、truncation 不作扫描维度——全文见 `$WQ_PY -m wqb.profiles explain` 末尾。
- **证据与历史**：[USA profile](../wq-brain-ra-pipeline/references/regions/USA.md)（入场裁决、红绿榜、证据附录）。
