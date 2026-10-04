---
name: wq-brain-ra-deu
description: "在 DEU 区挖 REGULAR alpha、调 DEU 的回测设置或阈值、查 DEU 某类数据集（区域 × 类别组合）的配方与禁区时使用：DEU 的区域分支流程与回测把控面板。通用九步走 wq-brain-ra-pipeline，判提交与提交走 worldquant-submit-alpha。"
layer: L-RA-R
allowed-tools:
  - Read
  - Bash
  - mcp__wqb-db__*
  - mcp__wq-brain-http__*
version: "1.0"
last_verified: 2026-10-05
---

# DEU 区域挖掘流程（RA 区域分支）

## 职责边界

- **本 skill 负责**：DEU 的区域分支——入场状态、回测把控（区域与「区域 × 类别」组合的回测设置 / 阈值 / Mode B 主闸，每个值可查来源）、S1 / S2 / S4 / S5 的 DEU 差异步骤、组合分支文件索引。
- **本 skill 不做**：九步通用正文（→ [`wq-brain-ra-pipeline`](../wq-brain-ra-pipeline/SKILL.md)）；选区（→ `brain-next-move-analysis`）；判提交与提交（`submit_verdict` 只否决，提交走 `worldquant-submit-alpha` 且必须用户确认）；不改其它区域的控制文件。
- **上游 / 下游**：上游 = 用户点名 DEU，或 `wq-brain-ra-pipeline` 步 1 路由到本区；下游 = `wq-brain-ra-pipeline` 各步、`wq-brain-campaign-toolkit` 引擎、`wq-brain-alpha-optimization-v1`（S4 改进）。

## 怎么用

1. **入场**：看下面「区域控制面板」的入场状态。`frozen` 只走 profile 写明的后门；`probe-only` 只许探针批。
2. **每次回测前**按数据集取生效画像（回测设置、阈值、Mode B 主闸、生成与改进要点，每项带来源）：

   ```bash
   $WQ_PY -m wqb.profiles explain --region DEU --dataset <dataset>
   ```

   `workflow_batch_track` 会把该组合的回测覆盖以 `--set` 钉住；直接用 MCP 发仿真（`create_multi_simulation` / `create_simulation`）时，按 explain 输出逐项传设置，不要依赖工具缺省（各入口缺省不同，换档等于换信号）。
3. **走九步**：按 `wq-brain-ra-pipeline` 执行；步 3 / 4 / 7 / 8 先读对应组合的分支文件（下表最后一列）。
4. **步 9 回写之后**刷新组合证据并重渲本 skill：

   ```bash
   $WQ_PY -m wqb.profiles sync-cells --region DEU --apply
   $WQ_PY -m wqb.profiles render --region DEU --apply
   ```

## 区域控制面板

<!-- profiles:region-panel:start -->
**入场状态**：`active`　零竞争高倍率区（统一 1.9×、D1 全域 16 类塔本季全空）但**合规形态天花板 0.69 vs ladder 1.58 = 2.3× 落差**才是真墙——历史 6 颗 ACTIVE 的 S1.68~2.17 全靠 4~5 腿 add 相加（铁律 §0 违规族）取得，无 win recipe 可继承

| 回测设置 | 值 | 来源 |
|---|---|---|
| instrumentType | EQUITY | settings.json |
| region | DEU | settings.json |
| universe | TOP500 | settings.json |
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
| Mode B 主闸（sharpe / fitness） | 1.25 / 0.8 | thresholds_override:DEU（实时值含区域台账，看 explain） |
| review.sharpe_min | 1.58 | thresholds.json |
| review.fitness_min | 1.0 | thresholds.json |
| review.turnover_min | 0.01 | thresholds.json |
| review.turnover_max | 0.7 | thresholds.json |
| review.two_year_sharpe_min | 1.0 | thresholds.json |
| near.sharpe_min | 1.0 | thresholds.json |
| diversity.signal_floor.max_sharpe_floor | 0.5 | thresholds.json |

**循环与闸门（profile front-matter）**
- 每波探针位上限：1
- 快判死：新数据集 8 探针无 ／S／≥0.5 即判死。**注意：sub_universe 不再作为探针早停依据**——该闸是 IS sharpe 的线性函数（limit≈0.47×S），S≳1.7 时自动过；历史「实测 0.30」来自 S≈0.6 的低分批被误读为墙（见正文『伪墙更正’）
- 停止条件：白名单被 dead_end 全覆盖
- 停止条件：合规形态天花板（~0.69）距 ladder 1.58 无可行路径
- 闸门特化（文档级）：cw_gate=WARN——代码尚未读取（闸 7 恒 WARN，CW 在步 7 人工判），按此执行由 agent 负责

**平台事实**
- 宇宙是单一国家（config.REGION_COUNTRY_SCOPE）：country 轴中性化 / 分组等于全市场，别用
<!-- profiles:region-panel:end -->

## 组合分支（区域 × 类别）

<!-- profiles:cells-index:start -->
| 类别 | 分组 | 状态 | 回测覆盖 | 阈值覆盖 | 回测 / RA 全过 | prod 已测（低于上限） | 判死 / 胜绩 | 分支文件 |
|---|---|---|---|---|---|---|---|---|
| model | MODEL | active | — | — | 528 / 65 | 0（0） | 5 / 2 | [references/model.md](references/model.md) |
| other | Other | active | — | — | 401 / 47 | 50（6） | 8 / 1 | [references/other.md](references/other.md) |
| analyst | Analyst | active | — | — | 284 / 0 | 0（0） | 4 / 0 | [references/analyst.md](references/analyst.md) |
| institutions | Institutions | active | — | — | 102 / 0 | 0（0） | 5 / 0 | [references/institutions.md](references/institutions.md) |
| insiders | Insider | active | — | — | 69 / 1 | 0（0） | 1 / 1 | [references/insiders.md](references/insiders.md) |
| shortinterest | ShortInterest | active | — | — | 59 / 25 | 0（0） | 1 / 1 | [references/shortinterest.md](references/shortinterest.md) |
| sentiment | News-Sentiment | active | — | — | 39 / 12 | 0（0） | 0 / 0 | [references/sentiment.md](references/sentiment.md) |
| news | News-Sentiment | active | — | — | 24 / 0 | 0（0） | 3 / 0 | [references/news.md](references/news.md) |
| pv | PV | active | — | — | 24 / 0 | 0（0） | 3 / 0 | [references/pv.md](references/pv.md) |
| fundamental | Fundamental | active | — | — | 22 / 3 | 0（0） | 2 / 0 | [references/fundamental.md](references/fundamental.md) |
| risk | Risk | active | — | — | 22 / 11 | 0（0） | 1 / 0 | [references/risk.md](references/risk.md) |

说明：另有 8 条回测行没写数据集，无法归到组合；11 条判死 / 胜绩连类别也推断不出；证据于 2026-10-04 只读汇总。
<!-- profiles:cells-index:end -->

## 本区流程差异（相对九步骨架）

<!-- profiles:manual:start -->
- **真墙**：合规单信号形态天花板约 0.69（other545），离 ladder 线差约 2.3 倍；历史 6 颗 ACTIVE 全靠 4~5 腿 add 相加——那是被禁形态，没有可继承的配方。开波前先回答：怎样在合规单信号形态下把 S 推到 1.7 以上。
- **S0 选集**：锁白名单前交叉核历史（expressions 状态、ledger 判词、probe 波的回测行，「回测 0 行」不等于没测过）；GROUP 类数据集（pv29 / pv30）只能当分组轴，不进信号白名单。
- **S1 字段**：字段扫描要产出 TOP500 上的 longCount。
- **S4 改进**：sub_universe 是比值闸（limit 约等于 0.47 × IS sharpe），S 高了自动过；低分批的实测值不能外推成墙。体检包只有 1 个，体检硬门对本区基本不生效。
（来源：DEU profile）
<!-- profiles:manual:end -->

## 改控制

- **区域级**：`tracking/DEU/config/settings.json`（仿真设置）、`tracking/DEU/config/thresholds.json`（阈值）。
- **组合级**：`tracking/DEU/config/cells.json`——只写覆盖值，每个覆盖在同级 `_evidence` 写证据（波号 / alpha id / 日期）；没有证据的覆盖校验不通过。改完先校验再重渲：

  ```bash
  $WQ_PY -m wqb.profiles check --region DEU
  $WQ_PY -m wqb.profiles render --region DEU --apply
  ```

- **锁定项**（任何层都不能放宽）：禁混信号、Mode B 主闸下限、决策表 D0-P、平台线、窗口白名单、点塔按平台类别、提交前用户确认、truncation 不作扫描维度——全文见 `$WQ_PY -m wqb.profiles explain` 末尾。
- **证据与历史**：[DEU profile](../wq-brain-ra-pipeline/references/regions/DEU.md)（入场裁决、红绿榜、证据附录）。
