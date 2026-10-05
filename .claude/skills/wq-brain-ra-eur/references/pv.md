# EUR × pv（组合分支）

> 回到 [EUR 区域流程](../SKILL.md) · [EUR profile（证据与历史）](../../wq-brain-ra-pipeline/references/regions/EUR.md) · 实时生效画像：`$WQ_PY -m wqb.profiles explain --region EUR --category pv`

<!-- profiles:cell-panel:start -->
**状态**：probe（跟区域入场 probe-only）　**分组**：PV　**类别卡**：pv

**涉及数据集**：continuation_score、intraday_pv_feats、pattern_scores、pv106、pv37

### 回测设置（进仿真的值）

| 设置 | 值 | 来源 |
|---|---|---|
| instrumentType | EQUITY | 区域 settings.json |
| region | EUR | 区域 settings.json |
| universe | TOPCS1600 | 区域 settings.json |
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
| 108 | 10 | 0 | 0 | 12 | 0 |

主要数据集（回测数）：continuation_score（81）、pv106（11）、pattern_scores（8）、pv37（8）

### S1 字段理解

- 各区可用性差异大：先查本区有没有 pv1（JPN TOP1600 没有，close / adv20 / returns 不可用）
- intraday_pv_feats 目录字段 ≠ 平台可用字段：先单字段探针再成批
- 窗口（类别卡，均在白名单内）：daily 1/5/22；monthly 66

### S2 生成

- **类别通用原语**（类别卡，跨区）：
  - continuation vs reversal: short-horizon pattern vs longer mean
  - intraday vs overnight: session-specific pressure
  - volume-conditioned return: price move that happened on unusual volume
  - fast+slow interaction must be ONE coherent signal (ratio / ts_corr / conditional), never a weighted sum of two legs
  - volatility regime: high-vol vs low-vol period signal divergence
  - liquidity shock: volume spike vs historical average (ts_zscore of volume)
  - price efficiency: bid-ask spread or price impact proxy
- **跨区结论**（IND/GLB/ASI；negative）：日内价量相关反转 / 尾盘反转 IS 很强，但裸用 prod 0.79–0.99；只有加门控才可能破墙（见全局杠杆 subset_gate）（证据：IND intraday_pv_feats prod 0.79–0.92、pv103 外部孪生 1.0（IND profile）；GLB / ASI 门控模板（2026-09-21 实证）） <!-- lint:const-ok 证据原文 -->
- **跨区结论**（JPN/IND/GBR/USA；negative）：日内微观结构的非反转机制普遍弱（max ／S／ 约 1.0，或撞 fitness 墙）（证据：JPN w8 16 条 max／S／ 1.02；USA-IPV-CORR-PRECLOSE-FITNESS-WALL-20260921；GBR-INTRADAY-MICRO-WEAK；IND 未点亮塔实证） <!-- lint:const-ok 证据原文 -->
- **跨区结论**（KOR/GBR/DEU/AMR；negative）：图表形态族（pattern_scores / continuation_score / chart_cnn）（证据：KOR 三连死（chart_cnn 1.51 → continuation 0.34 → pattern_scores 0.49）；GBR-SIMPLE-STRUCTURE-DEAD；DEU-PATTERN_SCORES-PROBE-DEAD-20261002；AMR 红榜） <!-- lint:const-ok 证据原文 -->
- **禁止**（类别卡）：禁止使用加权混合（0.4*rank(A) + 0.6*rank(B) / add(multiply(0.4,A),multiply(0.6,B))）
- **禁止**（类别卡）：禁止使用 ts_entropy / ts_skewness（幽灵算子）
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

- 资格判定：`$WQ_PY tools/mode_b_qualify.py evaluate --region EUR --sharpe <S> --fitness <F> --two-year-sharpe <2Y>`（喂全指标，旁路 A–E 才会生效）
- 提交链：`submit_verdict` 只否决；prod 与 self 双端点实测（`check_correlation(refresh=True)`）；用户明确确认后才 `workflow_submit_alpha(confirm_submit=True)`——见 `worldquant-submit-alpha`

### 判死记录（不要重试；「归属」= payload 绑定 / 由条目名推断 / 关键词推断）

| 条目 | 族 | 下次怎么办 / 说明 | 数据集 | 归属 |
|---|---|---|---|---|
| EUR-CONTINUATION-COMPOSITE-WEAK | continuation_score chart-similarity composites | After composite round (bull-bear subtract, group_rank, ts_av_diff, ts_corr) max ／sharpe／ 0.44. Not worth another probe r | continuation_score | payload | <!-- lint:const-ok 证据原文 -->
| EUR-INTRADAY-PV-W126-128-NEAR-MISS | intraday_pv_feats 事件门控 × 成交量厚尾分位 | Leave intraday_pv_feats 的下列已试机制：挂单深度倾斜(group_zscore)、宽价差买盘偏离(if_else)、量价确认度(ts_corr/ts_covariance)、VWAP 积压、报价厚尾不对称、T-KB- | intraday_pv_feats | payload | <!-- lint:const-ok 证据原文 -->
| EUR-PATTERN-BREAKAWAY-RESID-WEAK | pattern_scores breakaway residual alone | Breakaway-gap residual/invert max S0.71 F0.29. PV pyramid but weak as standalone. Wj71Q12o used gap as 0.60 mix with FCF | pattern_scores | payload | <!-- lint:const-ok 证据原文 -->
| EUR-PV-RISING-WEDGE-TRIANGLE-CONT-FAST-WEAK | pattern_scores rising_wedge / symmetrical_triangle / continu | Do not use rising_wedge, symmetrical_triangle, or continuation_falling_wedge as the 0.40/0.30 fast pair replacing v_rev/ | pattern_scores | inferred | <!-- lint:const-ok 证据原文 -->
| EUR-STAR-PV-ASCT-TREND-WEAK | pattern_scores asc_triangle / support-resistance / trendline | unused PV families weak vs common_gap_up winner | pattern_scores | payload | <!-- lint:const-ok 证据原文 -->
| EUR-UNTESTED-CHANNEL-FIRSTPROBE-DEAD | EUR 未测数据集通道（pv106 PV价差 / model50 MODEL估值） | EUR 未测通道亦穷尽：新赛季（Q4）不改变 returns 天花板与 prod 池，故本区不再投槽位；如需继续须先出现全新数据集（非新赛季）或 prod 池实质衰减，否则转 IND/KOR。 | pv106 | inferred | <!-- lint:const-ok 证据原文 -->
| EUR-W169-FASTPV-SPREAD-REVERSED-DEAD | continuation_score/intraday_pv_feats 快腿 - predicted_surprise | EUR D1 快腿 PV 族(continuation_score/intraday_pv) 禁止作正向 rank 腿；其信号方向为反转，若用必须取负(-rank)且与慢腿同向叠加而非价差。intraday_pv corr 字段高换手(>0 | intraday_pv_feats | inferred | <!-- lint:const-ok 证据原文 -->
| EUR-W170-FASTPV-NEGATED-WEAK-DEAD | predicted_surprise 慢 - continuation_score 快(取负同向) 价差 | EUR 快腿 PV 族(continuation_score/intraday_pv_feats) 判死：正向价差方向反(wave169)、取负同向强度不足(wave170)，两向都过不了 1.58。与 wave166 实证一致(纯信号族  | continuation_score | inferred | <!-- lint:const-ok 证据原文 -->
| EUR-pattern_scores-BREAKAWAY-GAP-WEAK | EUR-pattern_scores-BREAKAWAY-GAP-WEAK | breakaway_gap 字段族信号弱，8 条全灭，最高 Sharpe 0.03 | pattern_scores | payload | <!-- lint:const-ok 证据原文 -->
| EUR-pattern_scores-wave83-skeleton-fail |  |  | pattern_scores | payload | <!-- lint:const-ok 证据原文 -->
| EUR-shortinterest6-PATTERN-FAST-LEG-PROD | shortinterest6 × pattern_scores fast leg variants | star_hold 家族与任何 pattern_scores 快腿组合 prod_corr 必超 0.7（wave110 0.74-0.77），换快腿字段无法破墙；shortinterest6 在 EUR 区域 IS 天花板 1.24-1. | pattern_scores | inferred | <!-- lint:const-ok 证据原文 -->
| EUR-shortinterest6-PATTERN-MIX-PROD | shortinterest6 × pattern_scores win mix | star_hold 家族与 pattern_scores 快腿组合 prod_corr 0.74-0.77 超 0.7 硬闸，无法提交 | pattern_scores | inferred | <!-- lint:const-ok 证据原文 -->
<!-- profiles:cell-panel:end -->

## 补充说明（手写）

<!-- profiles:manual:start -->
<!-- profiles:manual:end -->
