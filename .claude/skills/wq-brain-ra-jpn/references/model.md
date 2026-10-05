# JPN × model（组合分支）

> 回到 [JPN 区域流程](../SKILL.md) · [JPN profile（证据与历史）](../../wq-brain-ra-pipeline/references/regions/JPN.md) · 实时生效画像：`$WQ_PY -m wqb.profiles explain --region JPN --category model`

<!-- profiles:cell-panel:start -->
**状态**：active（跟区域入场 active）　**分组**：MODEL　**类别卡**：model

**涉及数据集**：analyst_revision_horizons、global_seasonal_model、multi_source_model

### 回测设置（进仿真的值）

| 设置 | 值 | 来源 |
|---|---|---|
| instrumentType | EQUITY | 区域 settings.json |
| region | JPN | 区域 settings.json |
| universe | TOP1600 | 区域 settings.json |
| delay | 1 | 区域 settings.json |
| neutralization | MARKET | 区域 settings.json |
| decay | 4 | 区域 settings.json |
| truncation | 0.08 | 区域 settings.json |
| pasteurization | ON | 区域 settings.json |
| unitHandling | VERIFY | 区域 settings.json |
| nanHandling | OFF | 区域 settings.json |
| maxTrade | OFF | 区域 settings.json |
| language | FASTEXPR | 区域 settings.json |
| visualization | false | 区域 settings.json |
| startDate | 2013-01-01 | 区域 settings.json |
| endDate | 2023-12-31 | 区域 settings.json |

### 阈值

- Mode B 主闸 sharpe / fitness：1.25 / 0.8（default；下限锁生效，实时值看 explain）
- 其余阈值跟区域 thresholds.json（本组合无覆盖）

### 证据（2026-10-04 只读汇总）

| 回测 | RA 全过 | prod 已测 | 其中低于上限 | 判死 | 胜绩 |
|---|---|---|---|---|---|
| 120 | 0 | 0 | 0 | 1 | 0 |

主要数据集（回测数）：analyst_revision_horizons（61）、global_seasonal_model（43）、multi_source_model（16）

### S1 字段理解

- 分清分数水平与分位 / 概率标签：标签类在 GBR 2Y 崩（GBR-DLRISKFREE-LABEL-DEAD）
- 看字段 description 判断是不是别人做好的成品因子；成品因子的热门字段 prod 墙最硬
- 窗口（类别卡，均在白名单内）：level 22/66/252；change 5/22

### S2 生成

- **说明**：JPN/TOP1600 没有 pv1；VECTOR 字段外面不能再套 ts_*（只能 rank(vec_avg(f)) 级）；SUBINDUSTRY / SECTOR 中性化不可用（用 MARKET / STATISTICAL / NONE）——区域硬事实，见 JPN profile
- **类别通用原语**（类别卡，跨区）：
  - industry residual: group_zscore so the factor is not the sector bet
  - quality minus yield: a slow fundamental residual, not the raw score
  - invert only when the economic story is crowding or mean-reversion
  - never ship a lone rank(model_score) as a concept
  - model disagreement: ensemble variance across model outputs
  - regime conditional: model signal only in specific market regimes
- **跨区结论**（GLB/USA/EUR；negative）：成品模型分数的热门字段在多区撞 prod 墙（users 高的字段 prod 必超上限）（证据：GLB techindi_model predicted_first_quantile 系 qMNZX1o1 prod 0.7686（GLB profile）；USA mdl177 / book-value 145 颗同族 ACTIVE；EUR×model 62 条判死） <!-- lint:const-ok 证据原文 -->
- **禁止**（类别卡）：禁止使用裸 rank(model_score)（必须 group_neutralize 或 industry residual）
- **禁止**（全局锁定）：禁止两条独立信号腿相加：加权（0.4×A + 0.6×B）、等权 add(rank(A), rank(B))、中缀 + 都算；第二个数据集只以条件（trade_when / if_else）、分组（group_rank / bucket）或残差（regression_neut / vector_neut）入场
- **禁止**（全局锁定）：禁止 ts_event_* 系列（平台没有）与幽灵算子；字段名逐一经 get_datafields 验证

### S4 改进（按顺序试：组合 → 类别卡 → 全局）

1. [全局] 判「无解 / 天花板」前先扫等价算子替换：signed_power → quantile、ts_scale → quantile / normalize。数值路径不同，一次动多个闸（含 prod，要读全部闸）（KOR/GLB 复现：KOR other466 signed_power→quantile：2Y 1.51→1.56、prod 0.6544→0.6397；GLB quantile 替 ts_scale：S +0.20、F +0.06、prod 0.475→0.565（DEC-72）） <!-- lint:const-ok 证据原文 -->
   - 注意：效应量逐区实测，禁外推；quantile 只收 1 个参数
2. [全局] 强但撞 prod 墙的快信号：用一个经济子集门控（trade_when 进 >0.5 出 <0.4 的慢变量，或 rank(cap)>0.2 ∩ 子集）只在子集里持仓（GLB/ASI/IND 复现：GLB-DL20D-SUBSET-GATE-FAMILY-20260921（prod 0.82→0.60–0.67）；ASI LLNgdpw2 / 88jaV5lv；IND ZYbqREW1 / levk5JYN（prod 0.54–0.55）） <!-- lint:const-ok 证据原文 -->
   - 前提：未门控的基础信号 IS sharpe 不低于 2.5、fitness 不低于 1.5（GLB 2026-09-27 铁律：门控只修 prod / robust，不造强度）；慢信号门控后换手会升，只用于快信号
- 提醒：prod 与 self 两个端点都取 max、都过线才可提；不改持仓的降 prod 杠杆（hump、加大 decay）会把 self 推爆（EUR wave274） <!-- lint:const-ok 证据原文 -->
- 提醒：设置是强度闸：nanHandling / maxTrade / decay / 中性化换档等于换信号，跨档结果不可比（IND 行为族 S 2.19→0.46） <!-- lint:const-ok 证据原文 -->
- 提醒：decay 匹配信号速度：快信号上 decay 越大越差；decay 0 与 1 逐位相同，只留一个 <!-- lint:const-ok 证据原文 -->
- 提醒：prod 墙先看直方图分单颗钉子 / 密墙 / 可破三型，再决定换分母、换设置档或分组轴（决策表 D0-P 诊断前置） <!-- lint:const-ok 证据原文 -->

### S5 提交前

- 资格判定：`$WQ_PY tools/mode_b_qualify.py evaluate --region JPN --sharpe <S> --fitness <F> --two-year-sharpe <2Y>`（喂全指标，旁路 A–E 才会生效）
- 提交链：`submit_verdict` 只否决；prod 与 self 双端点实测（`check_correlation(refresh=True)`）；用户明确确认后才 `workflow_submit_alpha(confirm_submit=True)`——见 `worldquant-submit-alpha`

### 判死记录（不要重试；「归属」= payload 绑定 / 由条目名推断 / 关键词推断）

| 条目 | 族 | 下次怎么办 / 说明 | 数据集 | 归属 |
|---|---|---|---|---|
| JPN-MULTI-SOURCE-MODEL-QUANTILE-DEAD | multi_source_model quantile/confidence predictions | JPN/TOP1600/D1 不再用 multi_source_model 单集做主信号；剩余 1211 条 GEM 池不再消化 | multi_source_model | payload | <!-- lint:const-ok 证据原文 -->
<!-- profiles:cell-panel:end -->

## 补充说明（手写）

<!-- profiles:manual:start -->
<!-- profiles:manual:end -->
