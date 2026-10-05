# GBR × model（组合分支）

> 回到 [GBR 区域流程](../SKILL.md) · [GBR profile（证据与历史）](../../wq-brain-ra-pipeline/references/regions/GBR.md) · 实时生效画像：`$WQ_PY -m wqb.profiles explain --region GBR --category model`

<!-- profiles:cell-panel:start -->
**状态**：active（跟区域入场 active）　**分组**：MODEL　**类别卡**：model

**涉及数据集**：analyst_earnings_ibes、model106、model109、model109_vector、model109_x_fundamental17、model110、model144、model238、model25、model25+model38+behavior、model250、model262、model264、model28、model307、model313、model36、model38_components、model38_ev_ebitda_region、model38_star_val …

### 回测设置（进仿真的值）

| 设置 | 值 | 来源 |
|---|---|---|
| instrumentType | EQUITY | 区域 settings.json |
| region | GBR | 区域 settings.json |
| universe | TOP700 | 区域 settings.json |
| delay | 1 | 区域 settings.json |
| neutralization | SUBINDUSTRY | 区域 settings.json |
| decay | 4 | 区域 settings.json |
| truncation | 0.08 | 区域 settings.json |
| maxTrade | ON | 区域 settings.json |
| pasteurization | ON | 区域 settings.json |
| unitHandling | VERIFY | 区域 settings.json |
| nanHandling | ON | 区域 settings.json |
| language | FASTEXPR | 区域 settings.json |
| visualization | false | 区域 settings.json |
| startDate | 2014-01-01 | 区域 settings.json |
| endDate | 2023-12-31 | 区域 settings.json |

### 阈值

- Mode B 主闸 sharpe / fitness：1.25 / 0.8（default；下限锁生效，实时值看 explain）
- 其余阈值跟区域 thresholds.json（本组合无覆盖）

### 证据（2026-10-04 只读汇总）

| 回测 | RA 全过 | prod 已测 | 其中低于上限 | 判死 | 胜绩 |
|---|---|---|---|---|---|
| 283 | 23 | 18 | 9 | 13 | 1 |

主要数据集（回测数）：predictive_starmine（74）、model250（23）、model25（23）、model36（22）、model106（18）、model28（18）、model307（12）、model109（11）

### S1 字段理解

- 分清分数水平与分位 / 概率标签：标签类在 GBR 2Y 崩（GBR-DLRISKFREE-LABEL-DEAD）
- 看字段 description 判断是不是别人做好的成品因子；成品因子的热门字段 prod 墙最硬
- 窗口（类别卡，均在白名单内）：level 22/66/252；change 5/22

### S2 生成

- **避**：PROD 饱和族：starmine 四向价值、delta66 双时序差分、other455×model264（GBR profile，只许机制换腿）
- **说明**：STATISTICAL 中性化（GBR 首次采样）让 8 / 8 孪生全面提升：S +0.1~0.45、2Y +0.4~0.8；以后 GBR 波次把它当 A / B 对照轨（Claude 记忆 gbr 2026-09-15）——这是对照证据，没有改缺省档
- **说明**：model250 ML 复合 1.28 / 1.00、rn 0.87，但生命周期晚（年度 2.87→约 0.9）且 prod 0.764；model238 排名类天花板 0.68，只作复合从腿
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

- 资格判定：`$WQ_PY tools/mode_b_qualify.py evaluate --region GBR --sharpe <S> --fitness <F> --two-year-sharpe <2Y>`（喂全指标，旁路 A–E 才会生效）
- 提交链：`submit_verdict` 只否决；prod 与 self 双端点实测（`check_correlation(refresh=True)`）；用户明确确认后才 `workflow_submit_alpha(confirm_submit=True)`——见 `worldquant-submit-alpha`

### 判死记录（不要重试；「归属」= payload 绑定 / 由条目名推断 / 关键词推断）

| 条目 | 族 | 下次怎么办 / 说明 | 数据集 | 归属 |
|---|---|---|---|---|
| GBR-DEBT-X-FUND17-CROSS-CEILING | debt_x_fundamental17_cross_dataset | debt×fundamental 跨数据集组合不再生成新变体；GBR 挖掘停止（B1 同轴 6 波 FAIL） | model109_x_fundamental17 | payload | <!-- lint:const-ok 证据原文 -->
| GBR-M28-REVERSE-CEILING | credit_reverse |  | model28 | payload | <!-- lint:const-ok 证据原文 -->
| GBR-MDL106-CEILING | model106_rank | model106 排名类结构不作为主导腿；仅允许复合结构从腿（软判死，走 priors 提示不设 L3 硬拦截） | model106 | inferred | <!-- lint:const-ok 证据原文 -->
| GBR-MDL238-RANK-CEILING | model238_rank | model238 排名类结构不作为主导腿；仅允许作为复合结构从腿（软判死，走 priors 提示不设 L3 硬拦截） | model238 | inferred | <!-- lint:const-ok 证据原文 -->
| GBR-MIRROR-ACCEL-SIGNAL-20260925 | analyst_earnings_ibes_return_acceleration_mirror | 镜像收益加速度族按 D4 判死（fitness 0.56<0.8）；机制发现已记录，仅在 D4 资格线经用户明确放宽或平台闸变化后方可重访 | analyst_earnings_ibes | payload | <!-- lint:const-ok 证据原文 -->
| GBR-MODEL109-DEBT-CEILING | model109_debt_dynamics | model109 debt 动态族不再生成新变体（含几何/中性化/门控/窗口）；GBR model 域 B1 停止闸触发 | model109 | payload | <!-- lint:const-ok 证据原文 -->
| GBR-MODEL109-VECTOR-CEILING | model109_vector_forecast | model109 VECTOR 字段族不再生成新变体；GBR model109 域全判死（MATRIX+VECTOR） | model109_vector | payload | <!-- lint:const-ok 证据原文 -->
| GBR-MODEL110-DEAD | model110_composite | model110 不再生成任何结构（quality/analyst_sentiment/alternative/tree/score/value/price_momentum_reversal 全灭）；GBR model 域判死 | model110 | payload | <!-- lint:const-ok 证据原文 -->
| GBR-MODEL144-DEAD | model144_starperformer | model144 不再生成任何结构（predict/score 组合全灭）；GBR StarPerformer 域判死 | model144 | payload | <!-- lint:const-ok 证据原文 -->
| GBR-MODEL250-LIFECYCLE-PRODSAT | model250_ml_composite | model250 composite/sub-signal variants not to be generated for RA in GBR; coverage 0.49 (longCount ~170 under SUBINDUSTR | model250 | payload | <!-- lint:const-ok 证据原文 -->
| GBR-MODEL53-DEAD | model53 | 不生成 model53 表达式 | model53 | inferred | <!-- lint:const-ok 证据原文 -->
| M36-CEILING | model36 star_sr 信用质量域 | same-family-ceiling | model36 | inferred | <!-- lint:const-ok 证据原文 -->
| MODEL307-HOME-BIAS | sales_pct_home_bias | TO 结构性超闸 + IS 天花板 0.61，35 条结构无路径可过全闸 | model307 | payload | <!-- lint:const-ok 证据原文 -->

### 胜绩

| 条目 | 机制 | 设置与骨架 | 数据集 | 归属 |
|---|---|---|---|---|
| GBR-ASYM-GATE-MIRROR-WIN-KPNgQApj | analyst_earnings_ibes_mirror_acceleration |  | analyst_earnings_ibes | inferred | <!-- lint:const-ok 证据原文 -->
<!-- profiles:cell-panel:end -->

## 补充说明（手写）

<!-- profiles:manual:start -->
<!-- profiles:manual:end -->
