---
name: wq-brain-ra-twn
description: "在 TWN 区挖 REGULAR alpha、调 TWN 的回测设置或阈值、查 TWN 某类数据集（区域 × 类别组合）的配方与禁区时使用：TWN 的区域分支流程与回测把控面板。通用九步走 wq-brain-ra-pipeline，判提交与提交走 worldquant-submit-alpha。"
layer: L-RA-R
allowed-tools:
  - Read
  - Bash
  - mcp__wqb-db__*
  - mcp__wq-brain-http__*
version: "1.0"
last_verified: 2026-10-08
---

# TWN 区域挖掘流程（RA 区域分支）

## 职责边界

- **本 skill 负责**：TWN 的区域分支——入场状态、回测把控（区域与「区域 × 类别」组合的回测设置 / 阈值 / Mode B 主闸，每个值可查来源）、S1 / S2 / S4 / S5 的 TWN 差异步骤、组合分支文件索引。
- **本 skill 不做**：九步通用正文（→ [`wq-brain-ra-pipeline`](../wq-brain-ra-pipeline/SKILL.md)）；选区（→ `brain-next-move-analysis`）；判提交与提交（`submit_verdict` 只否决，提交走 `worldquant-submit-alpha` 且必须用户确认）；不改其它区域的控制文件。
- **上游 / 下游**：上游 = 用户点名 TWN，或 `wq-brain-ra-pipeline` 步 1 路由到本区；下游 = `wq-brain-ra-pipeline` 各步、`wq-brain-campaign-toolkit` 引擎、`wq-brain-alpha-optimization-v1`（S4 改进）。

## 怎么用

1. **入场**：看下面「区域控制面板」的入场状态。`frozen` 只走 profile 写明的后门；`probe-only` 只许探针批。
2. **每次回测前**按数据集取生效画像（回测设置、阈值、Mode B 主闸、生成与改进要点，每项带来源）：

   ```bash
   $WQ_PY -m wqb.profiles explain --region TWN --dataset <dataset>
   ```

   `workflow_batch_track` 会把该组合的回测覆盖以 `--set` 钉住；直接用 MCP 发仿真（`create_multi_simulation` / `create_simulation`）时，按 explain 输出逐项传设置，不要依赖工具缺省（各入口缺省不同，换档等于换信号）。
3. **走九步**：按 `wq-brain-ra-pipeline` 执行；步 3 / 4 / 7 / 8 先读对应组合的分支文件（下表最后一列）。
4. **步 9 回写之后**刷新组合证据并重渲本 skill：

   ```bash
   $WQ_PY -m wqb.profiles sync-cells --region TWN --apply
   $WQ_PY -m wqb.profiles render --region TWN --apply
   ```

## 区域控制面板

<!-- profiles:region-panel:start -->
**入场状态**：`probe-only`　小宇宙类 KOR：继承严闸 + 先实测档位，半导体权重股结构注意集中度

> 本区没有战役目录（`tracking/TWN/config/` 缺 settings.json）：开新区前先补 settings.json / thresholds.json，见 INDEX「开新区检查表」。 <!-- lint:counterexample: 本区尚未初始化：这些配置文件是「开新区前需补」的前置清单，引用待创建路径属有意提及 -->

| 阈值 | 值 | 来源 |
|---|---|---|
| Mode B 主闸（sharpe / fitness） | 1.25 / 0.8 | default（实时值含区域台账，看 explain） |

**循环与闸门（profile front-matter）**
- 每波探针位上限：2
- 快判死：新数据集 8 探针无 ／S／≥0.5 即判死（类 KOR 小宇宙纪律）
- 停止条件：白名单被 dead_end 全覆盖
- 闸门特化（文档级）：cw_gate=FAIL、longcount_verdict=FAIL——代码尚未读取（闸 7 恒 WARN，CW 在步 7 人工判），按此执行由 agent 负责

**平台事实**
- 宇宙是单一国家（config.REGION_COUNTRY_SCOPE）：country 轴中性化 / 分组等于全市场，别用
<!-- profiles:region-panel:end -->

## 组合分支（区域 × 类别）

<!-- profiles:cells-index:start -->
本区还没有组合文件（`tracking/TWN/config/cells.json` 不存在或为空）：所有类别跟区域缺省。有回测证据后跑 `$WQ_PY -m wqb.profiles sync-cells --region TWN --apply`。 <!-- lint:counterexample: 本区尚未初始化：这些配置文件是「开新区前需补」的前置清单，引用待创建路径属有意提及 -->
<!-- profiles:cells-index:end -->

## 本区流程差异（相对九步骨架）

<!-- profiles:manual:start -->
- **开新区前置**：tracking/TWN/config 不存在——先补 settings.json / thresholds.json；档位必须实测（config.REGIONS 写 TOP1000 / TOP500，campaign_intel 的兜底写 TOP500，都未实测）。
- **S2 / S3**：半导体权重极高，行业集中度天然大——每个新信号族首波做 STATISTICAL 与 SUBINDUSTRY 对照（各占半槽），定下来再回写。
- **S4**：小宇宙严闸同 KOR（文档级）。
（来源：TWN profile）
<!-- profiles:manual:end -->

## 改控制

- **区域级**：`tracking/TWN/config/settings.json`（仿真设置）、`tracking/TWN/config/thresholds.json`（阈值）。 <!-- lint:counterexample: 本区尚未初始化：这些配置文件是「开新区前需补」的前置清单，引用待创建路径属有意提及 -->
- **组合级**：`tracking/TWN/config/cells.json`——只写覆盖值，每个覆盖在同级 `_evidence` 写证据（波号 / alpha id / 日期）；没有证据的覆盖校验不通过。改完先校验再重渲： <!-- lint:counterexample: 本区尚未初始化：这些配置文件是「开新区前需补」的前置清单，引用待创建路径属有意提及 -->

  ```bash
  $WQ_PY -m wqb.profiles check --region TWN
  $WQ_PY -m wqb.profiles render --region TWN --apply
  ```

- **锁定项**（任何层都不能放宽）：禁混信号、Mode B 主闸下限、决策表 D0-P、平台线、窗口白名单、点塔按平台类别、提交前用户确认、truncation 不作扫描维度——全文见 `$WQ_PY -m wqb.profiles explain` 末尾。
- **证据与历史**：[TWN profile](../wq-brain-ra-pipeline/references/regions/TWN.md)（入场裁决、红绿榜、证据附录）。
