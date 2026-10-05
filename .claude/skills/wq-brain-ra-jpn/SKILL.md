---
name: wq-brain-ra-jpn
description: "在 JPN 区挖 REGULAR alpha、调 JPN 的回测设置或阈值、查 JPN 某类数据集（区域 × 类别组合）的配方与禁区时使用：JPN 的区域分支流程与回测把控面板。通用九步走 wq-brain-ra-pipeline，判提交与提交走 worldquant-submit-alpha。"
layer: L-RA-R
allowed-tools:
  - Read
  - Bash
  - mcp__wqb-db__*
  - mcp__wq-brain-http__*
version: "1.0"
last_verified: 2026-10-05
---

# JPN 区域挖掘流程（RA 区域分支）

## 职责边界

- **本 skill 负责**：JPN 的区域分支——入场状态、回测把控（区域与「区域 × 类别」组合的回测设置 / 阈值 / Mode B 主闸，每个值可查来源）、S1 / S2 / S4 / S5 的 JPN 差异步骤、组合分支文件索引。
- **本 skill 不做**：九步通用正文（→ [`wq-brain-ra-pipeline`](../wq-brain-ra-pipeline/SKILL.md)）；选区（→ `brain-next-move-analysis`）；判提交与提交（`submit_verdict` 只否决，提交走 `worldquant-submit-alpha` 且必须用户确认）；不改其它区域的控制文件。
- **上游 / 下游**：上游 = 用户点名 JPN，或 `wq-brain-ra-pipeline` 步 1 路由到本区；下游 = `wq-brain-ra-pipeline` 各步、`wq-brain-campaign-toolkit` 引擎、`wq-brain-alpha-optimization-v1`（S4 改进）。

## 怎么用

1. **入场**：看下面「区域控制面板」的入场状态。`frozen` 只走 profile 写明的后门；`probe-only` 只许探针批。
2. **每次回测前**按数据集取生效画像（回测设置、阈值、Mode B 主闸、生成与改进要点，每项带来源）：

   ```bash
   $WQ_PY -m wqb.profiles explain --region JPN --dataset <dataset>
   ```

   `workflow_batch_track` 会把该组合的回测覆盖以 `--set` 钉住；直接用 MCP 发仿真（`create_multi_simulation` / `create_simulation`）时，按 explain 输出逐项传设置，不要依赖工具缺省（各入口缺省不同，换档等于换信号）。
3. **走九步**：按 `wq-brain-ra-pipeline` 执行；步 3 / 4 / 7 / 8 先读对应组合的分支文件（下表最后一列）。
4. **步 9 回写之后**刷新组合证据并重渲本 skill：

   ```bash
   $WQ_PY -m wqb.profiles sync-cells --region JPN --apply
   $WQ_PY -m wqb.profiles render --region JPN --apply
   ```

## 区域控制面板

<!-- profiles:region-panel:start -->
**入场状态**：`active`　2026-09-15 首度开挖：平台实测 universe 仅 TOP1600/TOP1200；D1 共 7 塔全 0 亮；白名单 10 集（pyramid_view 战略榜重建，6 塔覆盖）

| 回测设置 | 值 | 来源 |
|---|---|---|
| instrumentType | EQUITY | settings.json |
| region | JPN | settings.json |
| universe | TOP1600 | settings.json |
| delay | 1 | settings.json |
| neutralization | MARKET | settings.json |
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
- 每波探针位上限：5
- 快判死：新数据集 8 探针无 ／S／≥0.5 即判死回写，不扩批不换设置重试
- 停止条件：白名单被 dead_end 全覆盖
- 停止条件：连续 3 波全 FAIL 且无新 dead_end
- 闸门特化（文档级）：cw_gate=FAIL——代码尚未读取（闸 7 恒 WARN，CW 在步 7 人工判），按此执行由 agent 负责

**平台事实**
- 宇宙是单一国家（config.REGION_COUNTRY_SCOPE）：country 轴中性化 / 分组等于全市场，别用
- 平台不支持的分组字段：sector, subindustry, industry（闸 2b 拦，platform_constraints.json）
- 本区不可用的基础字段：close, open, high, low, volume, returns, vwap, cap, sharesout, adv20 …（platform_constraints.json）
- VECTOR 字段聚合后不能再套 ts_* 算子（platform_constraints.json region_vector_ts_forbidden）
<!-- profiles:region-panel:end -->

## 组合分支（区域 × 类别）

<!-- profiles:cells-index:start -->
| 类别 | 分组 | 状态 | 回测覆盖 | 阈值覆盖 | 回测 / RA 全过 | prod 已测（低于上限） | 判死 / 胜绩 | 分支文件 |
|---|---|---|---|---|---|---|---|---|
| model | MODEL | active | — | — | 120 / 0 | 0（0） | 1 / 0 | [references/model.md](references/model.md) |
| pv | PV | active | — | — | 16 / 0 | 0（0） | 1 / 0 | [references/pv.md](references/pv.md) |

说明：另有 92 条回测行没写数据集，无法归到组合；证据于 2026-10-04 只读汇总。
<!-- profiles:cells-index:end -->

## 本区流程差异（相对九步骨架）

<!-- profiles:manual:start -->
- **平台硬事实**：universe 只有 TOP1600 / TOP1200；SUBINDUSTRY / SECTOR 中性化执行必 ERROR（用 MARKET / STATISTICAL / NONE）；没有 pv1（close / adv20 / returns 不可用）；VECTOR 聚合后再套 ts_* 报错；sector / subindustry / industry 分组字段非法。
- **S0 选集**：放宽档（coverage 0.6 / alphaCount 1500 / fieldCount 10）必须带补偿三件套：users 达 50 的字段只做方向验证；10–49 进池、提交前必实测；0–9 优先，且冷门字段占批次预算一半以上。
- **S2 生成**：辅助腿只以条件 / 分组 / 残差三式入场，任何加权 / 等权相加都不行（profile 步 4 旧文的主辅配比已于 2026-10-05 更正）。
- **S3 回测**：新数据集 8 探针无 |S| 达 0.5 即判死回写；delay 切换单独成批。体检包缺口时按 S1 字段画像把关 5 条预处理规则。
（来源：JPN profile）
<!-- profiles:manual:end -->

## 改控制

- **区域级**：`tracking/JPN/config/settings.json`（仿真设置）、`tracking/JPN/config/thresholds.json`（阈值）。
- **组合级**：`tracking/JPN/config/cells.json`——只写覆盖值，每个覆盖在同级 `_evidence` 写证据（波号 / alpha id / 日期）；没有证据的覆盖校验不通过。改完先校验再重渲：

  ```bash
  $WQ_PY -m wqb.profiles check --region JPN
  $WQ_PY -m wqb.profiles render --region JPN --apply
  ```

- **锁定项**（任何层都不能放宽）：禁混信号、Mode B 主闸下限、决策表 D0-P、平台线、窗口白名单、点塔按平台类别、提交前用户确认、truncation 不作扫描维度——全文见 `$WQ_PY -m wqb.profiles explain` 末尾。
- **证据与历史**：[JPN profile](../wq-brain-ra-pipeline/references/regions/JPN.md)（入场裁决、红绿榜、证据附录）。
