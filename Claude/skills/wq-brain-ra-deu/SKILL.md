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
last_verified: 2026-10-08
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
**入场状态**：`probe-only`　全域 16 类 0 alpha 的处女地（统一 1.9× 倍率、PPA 点塔无竞争）。★ 2026-10-08 更正：sub_universe 不是固定墙 —— limit≈0.47×IS_sharpe 是**比值闸**，S 高了自动过；实测已出现 sub=0.74/0.75/1.00。真瓶颈是**合规字段稀缺**（单信号过线仅 1 个字段）

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
- 快判死：新数据集 8 探针无 ／S／≥0.5 即判死；sub_universe 未过则不再加变体（墙是结构性的，调参无解）
- 停止条件：白名单被 dead_end 全覆盖
- 闸门特化（文档级）：cw_gate=WARN——代码尚未读取（闸 7 恒 WARN，CW 在步 7 人工判），按此执行由 agent 负责

**平台事实**
- 宇宙是单一国家（config.REGION_COUNTRY_SCOPE）：country 轴中性化 / 分组等于全市场，别用
<!-- profiles:region-panel:end -->

## 组合分支（区域 × 类别）

<!-- profiles:cells-index:start -->
| 类别 | 分组 | 状态 | 回测覆盖 | 阈值覆盖 | 回测 / RA 全过 | prod 已测（低于上限） | 判死 / 胜绩 | 分支文件 |
|---|---|---|---|---|---|---|---|---|
| model | MODEL | probe | — | — | 528 / 65 | 0（0） | 5 / 2 | [references/model.md](references/model.md) |
| other | Other | probe | — | — | 401 / 47 | 50（6） | 8 / 1 | [references/other.md](references/other.md) |
| analyst | Analyst | probe | — | — | 284 / 0 | 0（0） | 4 / 0 | [references/analyst.md](references/analyst.md) |
| institutions | Institutions | probe | — | — | 102 / 0 | 0（0） | 5 / 0 | [references/institutions.md](references/institutions.md) |
| insiders | Insider | probe | — | — | 69 / 1 | 0（0） | 1 / 1 | [references/insiders.md](references/insiders.md) |
| shortinterest | ShortInterest | probe | — | — | 59 / 25 | 0（0） | 1 / 1 | [references/shortinterest.md](references/shortinterest.md) |
| sentiment | News-Sentiment | probe | — | — | 39 / 12 | 0（0） | 0 / 0 | [references/sentiment.md](references/sentiment.md) |
| news | News-Sentiment | probe | — | — | 24 / 0 | 0（0） | 3 / 0 | [references/news.md](references/news.md) |
| pv | PV | probe | — | — | 24 / 0 | 0（0） | 3 / 0 | [references/pv.md](references/pv.md) |
| fundamental | Fundamental | probe | — | — | 22 / 3 | 0（0） | 2 / 0 | [references/fundamental.md](references/fundamental.md) |
| risk | Risk | probe | — | — | 22 / 11 | 0（0） | 1 / 0 | [references/risk.md](references/risk.md) |

说明：另有 8 条回测行没写数据集，无法归到组合；11 条判死 / 胜绩连类别也推断不出；证据于 2026-10-04 只读汇总。
<!-- profiles:cells-index:end -->

## 本区流程差异（相对九步骨架）

<!-- profiles:manual:start -->
### ★★ 开批前判断（2026-10-08 重审后版）

**⓪ 先查字段画像，再决定开不开批**（[references/field-profile.md](references/_field-profile.md)）

```bash
$WQ_PY tools/fields/field_profile.py --query --region DEU --verdict UNTESTED --limit 40
# 多区域：--build --region EUR / --all-regions / --list（各区间不串号）
```
- `to_med < 0.03` ⇒ **静态属性，任何骨架都无用**（`DEAD_STATIC`，已 30 字段实证）
- `to_med > 0.70` ⇒ **被 `HIGH_TURNOVER` 闸直接拒**（`DEAD_TURNOVER`，已 19 字段实证）
- **未测字段可用「同族外推」**：`count_institutional_*` 全 0.015~0.020｜`mdl28_*_rank` 0.024~0.028｜`star_sr_*` 0.022 ⇒ 整族免探
- **判死不必探**：`DEAD_STATIC` / `DEAD_TURNOVER` / `DEAD_COUNT`（名字含 `num/count` 且 2Y≥1.3 且 S≤0.7）三类**开批前就能定论**

**① 校验字段名与类型（零成本，MCP）**：`preflight_expressions(alpha_expressions=[...], region="DEU", universe="TOP500", delay=1)`
→ 看 `unknown_fields` 是否为空；它还会提示 VECTOR 字段需 `vec_*`。**跳过这步的代价是整批 CANCELLED（10 条全废）。**

**② 校验算子元数**：`op_arity.ensure_safe_for_dispatch(exprs)`。**同上，跳过即整批废。**
（`group_mean(x, weight, group)` 是**三参** —— 曾因写成两参整批 CANCELLED。）

**③ 每波探针位上限 1**（数值见上方 panels 生成块）；结论输出走 `submit_verdict`，提交必须用户确认。
**⚠️ 这条只有文档、没有代码闸**（`grep -n "probe_limit|probe_slot" src/ tools/` 无命中）⇒ 靠 agent 自觉；建议后续落成 ledger 计数 + 发批前检查。

### ★★★ 四条判词的修正（2026-10-08 实证推翻 / 补充）

**① `sub_universe` 不是固定墙（推翻生成面板的「实测仅 0.30」）**

生成面板写「sub_universe 结构性墙（limit≈0.47×sharpe，DEU 需 0.8，**实测仅 0.30**）」。
**本轮实测反证**：W170 一批内出现 **`sub=0.74` / `0.75` / `1.00`** 三个样本。
**⇒ `limit ≈ 0.47 × IS sharpe` 是比值闸；「0.30」来自 S≈0.6 的低分批被误读。S 高了自动过 —— 低分批实测值不能外推成墙。**

**② `model26` 不能整体判死 —— 按「字段族」判，不按数据集判**

旧判词：「`model26`（398 未测但历史全崩）⇒ 不建议投入」。**该判词只对 `mdl26_*`（模型因子）成立。**
**本轮实测**：`model26` 的 **`avg_estimate_change_pct_*` 族**（唯一有效机制的载体）——
`avg_estimate_change_pct_year1_earnings_90d` → **S1.27 / 2Y1.33 / sub0.75 ⇒ 进 WEAK**。
**⇒ `mdl26_*` 不建议；`avg_estimate_change_pct_*` 值得探。** 此原则适用于一切「数据集判死」：**必须落到字段族粒度。**

**③ 「同一机制跨数据集迁移」有效**

机制（已标准化预期变化率）从 `predictive_starmine` / `analyst_factor_signals` **迁到 `model26` 仍成立**。
**⇒ 迁移的是「机制」，不是「字段名」也不是「数据集」。**
对照：`avg_change_analyst_recommendation_*`（**推荐变化 = 不同机制**）S **−0.33 / −0.37** ⇒ 对照组证明机制判别有效。

**④ 画像 `n_sg ≤ 3` 的字段，其 S/2Y 只能当「下界」**

`netprofit_y1_estimate_change_3mo` 样本 2→3 时：S 1.32→**1.33**、2Y 1.21→**1.39**。
**⇒ 低样本 WEAK 字段值得先补测一轮再判死活。**

### ★★ 真墙判断已修正（本条推翻旧文）

**旧判断**：「合规单信号形态天花板约 0.69，离 ladder 1.58 差 2.3 倍；历史 6 颗 ACTIVE 全靠 4~5 腿 add（被禁形态）⇒ 无可行路径」。

**新事实（2026-10-08 实测）**：**合规单信号形态能过线，且已产出 2 颗** ——
- `58gkLAkk`（MODEL，S1.75 / 2Y2.07）**已提交 ACTIVE**
- `9qWX78vX`（ANALYST，S1.65 / F1.47 / **0 失败**）就绪

**⇒ 真正的墙不是「形态天花板」，而是「字段稀缺」**：全 DEU **22494 个字段里只有 1 个**（`eps_y1_estimate_change_3mo`）在单信号形态下 S 与 2Y 同时过线。
**⇒ 开波前该问的不是"怎么把 S 推上去"，而是"还有没有第二个字段配得上这个机制"。**

| 项 | 结论 |
|---|---|
| 唯一有效机制 | **「已标准化的预期变化率」**（`*_estimate_change_*`、`mean_estimate_change_pct_*`） |
| 唯一有效框架 | **双窗 1/210 + 单桶轴** `bucket(rank(ts_mean(bf,252)), "0,1,0.05")` |
| 已否证的 11 个机制骨架 | 仅 S1/S2 为 A 级（实测正）；其余 7 个 B 级（实测负）、2 个曾写错 → `docs/reference/field_characteristic_to_mechanism.md` |

### 本区流程差异（相对九步骨架）

- **S0 选集**：锁白名单前交叉核历史（expressions 状态、ledger 判词、probe 波的回测行，「回测 0 行」不等于没测过）；
  **GROUP 类数据集（pv29 / pv30 / other455 的 `*_cluster_*`）只能当分组轴**，不进信号白名单（画像 `AXIS_ONLY` 1390 个）。
  **★ 覆盖率 <0.6 的字段直接剔除** —— 占全量 **77.6%**（`UNUSABLE` 17460 个）。
- **S1 字段**：字段扫描要产出 TOP500 上的 longCount。**VECTOR 类数据集须 `vec_*` 聚合，且聚合算子是搜索维度**（实测 `vec_max` 0.43 > `vec_avg` 0.35）；`model216` / `news*` / `shortinterest3` / `risk60` 全为 VECTOR。
- **S4 改进**：sub_universe 是比值闸（limit 约等于 0.47 × IS sharpe），S 高了自动过；低分批的实测值不能外推成墙。体检包只有 1 个，体检硬门对本区基本不生效。
- **★ 开销纪律**：发批前必做上面 ⓪①② 三步（全部零成本）；单批上限 10 条；**开新数据集先跑 1 批探针，不直接扫全池**。

（来源：DEU profile + 2026-10-08 画像战役）
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
