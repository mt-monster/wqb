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
last_verified: 2026-10-20
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

## 本区结构导航（四目录）

<!-- region-scaffold:nav:start -->
| 目录 | 装什么 | 入口 |
|---|---|---|
| **本文件 SKILL.md** | 职责边界 + 怎么用 + 生成块（区域控制面板 / 组合分支 / 流程差异） | 本文 |
| [`rules/`](rules/README.md) | **USA 独有规则与纪律**：六步覆盖详解、改控制纪律、闸门与提交纪律 | [rules/README.md](rules/README.md) |
| [`config/`](config/README.md) | **配置视图**（真身在 `tracking/USA/config/`）：三表分工、区域默认档、本区覆盖落差 | [config/README.md](config/README.md) |
| [`references/`](references/analyst.md) | **实证**：`<类别>.md` 组合分支卡（render 生成）+ `_` 前缀专题（战役 / 手册 / 快照） | [references/](references/) |
| [`scripts/`](scripts/README.md) | 本 skill 级脚本（当前为空；区域探针脚本家 = `tracking/USA/scripts/`） | [scripts/README.md](scripts/README.md) |

细则不写在 SKILL.md：规则 → `rules/`，实证 → `references/`，配置 → `config/`，脚本 → `scripts/`。
<!-- region-scaffold:nav:end -->

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
| analyst | Analyst | active | neutralization=REVERSION_AND_MOMENTUM、decay=20 | — | 19 / 0 | 1（0） | 2 / 0 | [references/analyst.md](references/analyst.md) |
| insiders | Insider | active | — | — | 8 / 0 | 0（0） | 1 / 0 | [references/insiders.md](references/insiders.md) |
| news | News-Sentiment | active | — | — | 0 / 0 | 0（0） | 1 / 0 | [references/news.md](references/news.md) |
| sentiment | News-Sentiment | active | — | — | 0 / 0 | 0（0） | 1 / 0 | [references/sentiment.md](references/sentiment.md) |

说明：另有 99 条回测行没写数据集，无法归到组合；8 条判死 / 胜绩连类别也推断不出；证据于 2026-10-04 只读汇总。
<!-- profiles:cells-index:end -->

## 六步纵深骨架（本区覆盖）

> 通用方法见 [六步骨架 · 通用主文档](../wq-brain-ra-pipeline/references/_six-step-core.md)。
> **USA 的 override 细则（① 六法体检 / ② 组装 / ③ 归因 / ④ 破闸杠杆 / ⑤ 算子穷举 / ⑥ 终验 + 改控制纪律）已下沉**
> → **[rules/six-step-usa-override.md](rules/six-step-usa-override.md)**（as_of 2026-10-18）。
> 要点：最深最饱和市场（value/quality/book 必死，book/value 145 颗同族 ACTIVE）；扩批前先查 prod-first；
> delay 0 探针单独成批；破 prod 靠换 neutralization 不是磨算子；`ts_av_diff` > `ts_zscore(ts_backfill())`；
> `reverse` 必须与原方向成对发批；`winsorize` 必须具名 `std=`（preflight 误报 ≠ 不可用）。
## 本区流程差异（相对九步骨架）

<!-- profiles:manual:start -->
- **S0 / S2**：最深最饱和的市场——经典 value / quality / book 及其线性变体必死（book/value 单族 145 颗同族 ACTIVE）；priors 硬排除饱和族，生成后命中饱和族的在选波阶段剔除。
- **S3 回测**：扩批之前先按族查 prod-first；delay 0 探针单独成批，不与 delay 1 混批。
- **S4 改进**：同族出现 prod 达 0.6 → 只按决策表 D0-P 处置（0.60–0.70 当天进步 8；达 0.75 或踩线尝试失败判 dead_end 并换正交概念），禁止同族磨参数。修复保持 TOP3000；换 universe 要在 key_findings 写清 TOP3000 下失败的原因与要回答的诊断问题。
- **Mode B**：原来的 1.0 / 0.6 降门已被下限锁作废；单腿偏弱的组腿起点候选走旁路 A–E。
（来源：USA profile）
<!-- profiles:manual:end -->

## 改控制

- 区域级 `tracking/USA/config/settings.json`（仿真设置 + `_spre` 步 1 产物）、`thresholds.json`（审查阈值）；
  组合级 `cells.json`（只写覆盖值，每个覆盖须同级 `_evidence`，无证据校验不通过）。
- 改完先校验再重渲：`$WQ_PY -m wqb.profiles check --region USA` → `render --region USA --apply`。
- 三表分工与**本区覆盖落差（cells 零覆盖 ⇒ explain 与实测不一致）** → [config/README.md](config/README.md)；
  纪律细则 → [rules/six-step-usa-override.md](rules/six-step-usa-override.md)「改控制纪律」。
- 锁定项（任何层都不能放宽）：禁混信号、Mode B 主闸下限、决策表 D0-P、平台线、窗口白名单、点塔按平台类别、
  提交前用户确认、truncation 不作扫描维度——全文见 `$WQ_PY -m wqb.profiles explain` 末尾。
- 证据与历史：[USA profile](../wq-brain-ra-pipeline/references/regions/USA.md)（入场裁决、红绿榜、证据附录）。
## ★ 未点亮塔实证速查（指针）

2026-10-14 起 16 波 / 64 条的未点亮塔横跨 6 数据集实证（字段画像 / 纪律表 / 判死清单 / 最优候选 `N1ewm5Jw`）
已全部下沉 → **[references/_unlit-tower-campaign-20261014.md](references/_unlit-tower-campaign-20261014.md)**。

**逐字段档案**（挖过的每个字段族的类型/覆盖/αC/机制/读数/判死）→
**[references/_usa-field-profile-playbook-20261018.md](references/_usa-field-profile-playbook-20261018.md)**
（含 `risk_neutralized_sharpe` 判死口径：<0.3 = 纯风格 beta，别花仿真）。

**Fundamental 战役档案（2026-10-19）**：类别级扫描 →
[`references/_usa-fundamental-dataset-scan-20261019.md`](references/_usa-fundamental-dataset-scan-20261019.md)；
单集档案按**字段八问**组织（命名 = `_usa-<字段前缀>-field-profile-<asOf>.md`）：
[`fnd67`](references/_usa-fnd67-field-profile-20261019.md)、[`fnd93`](references/_usa-fnd93-field-profile-20261019.md)。

**ShortInterest 类别扫描（2026-10-19）** →
[`references/_usa-shortinterest-dataset-scan-20261019.md`](references/_usa-shortinterest-dataset-scan-20261019.md)
（6 集全景 + 三族字段八问 + 判死依据：日频做空量=噪声、借券方向对但 S 上限 1.07/SUB 缺口 0.3）。

**Institutions / PV 扫描（2026-10-19 战役二）** →
[`references/_usa-institutions-pv-dataset-scan-20261019.md`](references/_usa-institutions-pv-dataset-scan-20261019.md)
（20 条实测：机构 `mean_security_weight` Δ63 S1.34/DD 2.45%；DL 图表预测 2Y 2.21 但全期 S 0.54；概率价差为负）。

- 本季 USA/D1 只有 **model=4 / analyst=1 / earnings=1** 亮着；`score_datasets.py` 的 signal-score top20 **全是 model 族**
  ⇒ **白名单只能用「未点亮塔 × 低 alphaCount」筛，按 score 排序等于往已点亮塔堆料**。
- Analyst 战役（2026-10-17/18，15 波 / 60 条，交付 2 颗 ACTIVE）的字段画像 × 模板 × 指标
  → **[references/_usa-mining-playbook-20261018.md](references/_usa-mining-playbook-20261018.md)**；
  破 prod 墙的旋钮与提交纪律 → **[rules/gate-and-submit-discipline.md](rules/gate-and-submit-discipline.md)**。
