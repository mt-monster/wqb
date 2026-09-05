---
last_verified: 2026-08-25
name: brain-nextMove-analysis
description: "为 WorldQuant BRAIN 顾问生成综合日报。 覆盖平台更新、比赛进展、alpha 表现（IS/OS）、金字塔分析与可执行建议。 当用户要求\"日报\"、\"早报\"、\"状态检查\"或 \"daily report\"、\"morning update\" 时使用。"
layer: L0
allowed-tools:
  - Read
  - Bash
  - mcp__wq-brain-http__*
  - mcp__wqb-db__*
---







# BRAIN 日报工作流

该工作流为 WorldQuant BRAIN 顾问生成结构化日报。
详细的逐步流程与预期输出见 [reference.md](reference.md)。

## 定位声明（L0 并行情报层）

本 skill 属 **L0 并行情报层**：产出日报/金字塔分析/可执行建议，供决策参考；**非流水线前置、不产出 campaign 配置**。流水线前置查表由 `wq-brain-campaign-matrix`（S-PRE）负责，S0 体检白名单由 `wq-brain-ppa-mining §1.0`（toolkit `score_datasets.py` 权威执行）产出。

## 0. 执行摘要
总结下述分析中发现的关键洞察、机会与风险。

## 1. 平台更新
- **消息**：检查 `mcp__wq-brain-http__get_messages` 获取公告。
- **排行榜**：检查 `mcp__wq-brain-http__get_leaderboard` 获取排名变化。
- **多样性**：检查 `mcp__wq-brain-http__value_factor_trendScore` 获取多样性趋势。

## 2. 比赛进展
- **进行中的比赛**：`mcp__wq-brain-http__get_user_competitions`。
- **规则**：`mcp__wq-brain-http__get_competition_details` 与 `mcp__wq-brain-http__get_competition_agreement`。*关键：务必核对协议中的 universe/delay 约束。*
- **行动项**：推荐符合具体比赛规则的 alpha。

## 3. 未来事件
- **事件**：`mcp__wq-brain-http__get_events`（筛选即将发生的事件）。

## 4. 研究与建议
- **策略**：基于 alpha 表现与金字塔缺口，建议下一步行动。

## 5. Alpha 进展（IS/OS）
- **样本内（IS）**：`get_user_alphas(stage="IS")`。
- **样本外（OS）**：`get_user_alphas(stage="OS")`。
- **表现**：分析 Sharpe、PnL、Fitness（`mcp__wq-brain-http__get_alpha_details`、`mcp__wq-brain-http__get_alpha_yearly_stats`）。
- **优化**：提出改进建议（例如，利用 `mcp__wq-brain-http__get_pyramid_multipliers` 进行思路打磨或金字塔定向）。

## 5.5 区域饱和度检测（2026-08-25 落地）
**可选并行情报层**：本段查询失败不阻塞日报其余部分（失败时标注"区域饱和度：数据不可用"并跳过）。

对全部区域（USA/EUR/KOR/IND/ASI/GBR/HKG/GLB/CHN/TWN；MEA 为 frozen，仅报告冻结状态不做饱和度计算）执行：

- **PROD 饱和度**：`mcp__wqb-db__search_alphas_by_sharpe(region, min_sharpe=1.58)` 统计已达标 alpha 数。若 ≥10 且风格同质（同族/同算子家族集中）→ 标记 `prod_saturation: likely`，建议转向正交方向或减少该区域配额投入。
- **战役 exhaustion**：`mcp__wqb-db__get_campaigns(region)` 统计 `exhausted / in_progress / untried` 分布。若数据集全部 exhausted → 建议冻结转区（参照 MEA 先例）。
- **开战役候选**：`untried` 数据集数量 >0 的 probe-only 区域（ASI/GBR/HKG/CHN/TWN）→ 列为"建议开战役"候选。

**输出区域状态表**：

| region | 达标数 | exhausted 占比 | 建议动作 |
|---|---|---|---|
| USA | n | x% | 继续 / 正交 / 开战役 / 冻结 |

**联动区域 profile**：转区建议以 `wq-brain-ra-pipeline/references/regions/<REGION>.md` 的 `entry_verdict`（active/probe-only/frozen）为基准——active 区域默认"继续"，触饱和或 exhaustion 才升级为"正交/冻结"；probe-only 区域默认不开战役，有 untried 数据集才列候选；frozen 区域仅报状态。
