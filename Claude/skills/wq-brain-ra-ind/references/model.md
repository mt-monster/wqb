# IND × model（组合分支）

> 回到 [IND 区域流程](../SKILL.md) · [IND profile（证据与历史）](../../wq-brain-ra-pipeline/references/regions/IND.md) · 实时生效画像：`$WQ_PY -m wqb.profiles explain --region IND --category model`

<!-- profiles:cell-panel:start -->
**状态**：probe（跟区域入场 probe-only）　**分组**：MODEL　**类别卡**：model

**备注**：behavioral_signals（平台类别 MODEL）是 IND 唯一能过 IS 闸的族；但 8 颗 IS 全闸候选 prod 全在 0.7161–0.8261（单颗钉子型）

**涉及数据集**：behavioral_signals、global_seasonal_model、mdl135、model、model135、model138、model144、model16、model170、model192、model216、model238、model238_anlrev、model252、model262、model28、model29、model32、model36、predictive_starmine

### 回测设置（进仿真的值）

| 设置 | 值 | 来源 |
|---|---|---|
| instrumentType | EQUITY | 区域 settings.json |
| region | IND | 区域 settings.json |
| universe | TOP500 | 区域 settings.json |
| delay | 1 | 区域 settings.json |
| neutralization | STATISTICAL | 区域 settings.json |
| decay | 4 | 区域 settings.json |
| truncation | 0.08 | 区域 settings.json |
| pasteurization | ON | 区域 settings.json |
| testPeriod | P0Y0M0D | 区域 settings.json |
| unitHandling | VERIFY | 区域 settings.json |
| nanHandling | OFF | 区域 settings.json |
| maxTrade | OFF | 区域 settings.json |
| language | FASTEXPR | 区域 settings.json |
| visualization | false | 区域 settings.json |

### 阈值

- Mode B 主闸 sharpe / fitness：1.5 / 1.0（thresholds_override:IND；下限锁生效，实时值看 explain）
- 其余阈值跟区域 thresholds.json（本组合无覆盖）

### 证据（2026-10-04 只读汇总）

| 回测 | RA 全过 | prod 已测 | 其中低于上限 | 判死 | 胜绩 |
|---|---|---|---|---|---|
| 168 | 25 | 12 | 9 | 12 | 5 |

主要数据集（回测数）：model135（62）、model252（31）、model32（29）、model36（14）、model16（10）、model144（10）、model238_anlrev（9）、global_seasonal_model（3）

### S1 字段理解

- 分清分数水平与分位 / 概率标签：标签类在 GBR 2Y 崩（GBR-DLRISKFREE-LABEL-DEAD）
- 看字段 description 判断是不是别人做好的成品因子；成品因子的热门字段 prod 墙最硬
- 窗口（类别卡，均在白名单内）：level 22/66/252；change 5/22

### S2 生成

- **用**：behavioral_signals streak / recency 的秩化形，方向 = 动量 / 外推（反向全负 S）（IND profile 2026-10-03）
- **避**：model77 / model170 质量分与估值缺口、mdl68、mdl313、global_seasonal 事件旗标：IS 层就死（S 0.07–1.22）
- **说明**：group_rank 是行为族成立的条件：换 group_neutralize / group_zscore 保幅度 S 掉到 0.39–1.33；SUBINDUSTRY 中性化使 S 腰斩 2.36→1.28
- **说明**：decay 匹配信号速度：mean-5 水平形 decay 1 最优、decay 20 全灭；raw 窗口 1 需 decay 8
- **说明**：设置是强度闸：同表达式 decay 8 下 nanHandling=OFF 换成 ON、或 maxTrade=OFF 换成 ON，S 2.19→0.46——跟本区 settings.json
- **已验证骨架**（证据见每行注释；照抄前先按本组合当前 prod 复核）：

  ```text
  group_rank(ts_mean(vec_avg(recency), 5), industry)
  group_rank(vec_avg(streak), industry)
  ```

  - group_rank(ts_mean(vec_avg(recency), 5), industry)… ← decay 1，prod 0.7161（IND profile；recency 指 behavioral_signals 的 recency 字段）
  - group_rank(vec_avg(streak), industry)… ← decay 8，2Y 1.71（IND profile）
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
- **不要用**：事件门控（future_event_update_flag 等）：2Y 能提到 2.44，但 prod 不降（0.7544）（IND profile 2026-10-03） <!-- lint:const-ok 证据原文 -->
- **不要用**：改窗口 / 分组轴 / decay：9 种构造都被 1–3 颗钉子钉在上限之上；7 个分组轴 prod 0.74–0.83（IND profile（单颗钉子型 prod 墙）） <!-- lint:const-ok 证据原文 -->
- 提醒：prod 与 self 两个端点都取 max、都过线才可提；不改持仓的降 prod 杠杆（hump、加大 decay）会把 self 推爆（EUR wave274） <!-- lint:const-ok 证据原文 -->
- 提醒：设置是强度闸：nanHandling / maxTrade / decay / 中性化换档等于换信号，跨档结果不可比（IND 行为族 S 2.19→0.46） <!-- lint:const-ok 证据原文 -->
- 提醒：decay 匹配信号速度：快信号上 decay 越大越差；decay 0 与 1 逐位相同，只留一个 <!-- lint:const-ok 证据原文 -->
- 提醒：prod 墙先看直方图分单颗钉子 / 密墙 / 可破三型，再决定换分母、换设置档或分组轴（决策表 D0-P 诊断前置） <!-- lint:const-ok 证据原文 -->

### S5 提交前

- 资格判定：`$WQ_PY tools/mode_b_qualify.py evaluate --region IND --sharpe <S> --fitness <F> --two-year-sharpe <2Y>`（喂全指标，旁路 A–E 才会生效）
- 提交链：`submit_verdict` 只否决；prod 与 self 双端点实测（`check_correlation(refresh=True)`）；用户明确确认后才 `workflow_submit_alpha(confirm_submit=True)`——见 `worldquant-submit-alpha`

### 判死记录（不要重试；「归属」= payload 绑定 / 由条目名推断 / 关键词推断）

| 条目 | 族 | 下次怎么办 / 说明 | 数据集 | 归属 |
|---|---|---|---|---|
| IND-EBITDA-SURPRISE-ROBUST-WALL | model29 EBITDA SmartEstimate surprise | IND区域model29 EBITDA surprise信号族robust结构性死墙（0.32-0.49），S/F/2Y都有梯度但robust不可达，不再展开同族变体 | model29 | inferred | <!-- lint:const-ok 证据原文 -->
| IND-MDL135-PROD-WALL-FINAL | model135 oscillation reversal icc/isr/willimsr | mdl135震荡反转族本战役封存：族内变体禁止再提交(自相食)也禁止再生成同骨架新变体；该族唯一可提交名额已被d5jJebLv占用 | mdl135 | inferred | <!-- lint:const-ok 证据原文 -->
| IND-MDL138-DEVIATION-ROBUST-WALL | model138 |  | model138 | inferred | <!-- lint:const-ok 证据原文 -->
| IND-MDL262-IMPLIED-VALUATION-DEAD | model262 DNN implied valuation | IND区域model262 DNN隐含估值比率信号族不可用，sub_universe+robust双崩，不再展开 | model262 | inferred | <!-- lint:const-ok 证据原文 -->
| IND-MODEL-SCORE-DEAD | 模型分数族 | IND 区域模型分数族不可用，EVENT 字段聚合后信号衰减严重 | model | inferred | <!-- lint:const-ok 证据原文 -->
| IND-MODEL170-VALUATION-DEAD | model170 implied valuation | skip model170 valuation family; proceed to analyst_base_ref consensus surprise | model170 | inferred | <!-- lint:const-ok 证据原文 -->
| IND-MODEL192-CDS-DEAD | model192 cds | IND 区域回避信用风险/CDS/破产预测类信号，该方向为反向指标 | model192 | inferred | <!-- lint:const-ok 证据原文 -->
| IND-MODEL216-ROBUST-WALL | model216 ARM | 单信息源模型分数字段族（如 model216 综合评分）在 IND robust universe 结构性失效：组合/窗口/双窗均无法抬 robust；裸 rank 最高但也不到 1.0；同时与已有 win 相关 0.66+ 预示 prod | model216 | inferred | <!-- lint:const-ok 证据原文 -->
| IND-MODEL238-PROD-SATURATED | model238 SmartHoldings | 模型分数字段族在 IND prod 池结构性饱和，四重形态实测：内部组合破 robust 不破 prod（0.85 地板）、跨族反腿压 prod 不保 S、强 S 反腿不压 prod、残差差分模板破 prod 墙但剥信号（prod 0.20 | model238 | inferred | <!-- lint:const-ok 证据原文 -->
| IND-PREDICTED-SURPRISE-ROBUST-WALL | predictive_starmine predicted_surprise | IND区域predicted_surprise信号族robust结构性死墙（0.20-0.62），S可过但robust不可达，不再展开同族变体 | predictive_starmine | inferred | <!-- lint:const-ok 证据原文 -->
| IND-STARMINE-GROWTH-DEAD | predictive_starmine SmartEstimate growth | IND区域predictive_starmine SmartEstimate growth字段族（盈利增长/收入增长/市场隐含CAGR）不可用，robust墙0.20以下恒定 | predictive_starmine | inferred | <!-- lint:const-ok 证据原文 -->
| IND-STARMINE-VALUATION-DEAD | predictive_starmine valuation | IND区域predictive_starmine估值类字段（EP yield/forward PE/Price-to-IV/PE比率）不可单用，robust墙0.37-0.69恒定 | predictive_starmine | inferred | <!-- lint:const-ok 证据原文 -->

### 胜绩

| 条目 | 机制 | 设置与骨架 | 数据集 | 归属 |
|---|---|---|---|---|
| IND-BEHAVIORAL-SIGNALS-BREAKTHROUGH | behavioral_signals 行为金融信号在 IND TOP500 有效，5/8 alpha Sharpe >  | chronological_return_sequence_correlation + STATISTICAL 中性化 + decay=4，但 Turnover 59.75% 过高（>40% 硬闸），需降低 Turnover | behavioral_signals | inferred | <!-- lint:const-ok 证据原文 -->
| IND-MDL135-OSC-REVERSAL-WIN | model135 震荡反转族首探即引爆：3日RSI反转S=3.44(F2.11/2Y3.14/robust1.54)，d | 配方=-rank(ts_backfill(vec_avg(震荡指标),66))，decay=6，STATISTICAL；适用字段 d3_isr/d5_isr/d01_icc/d01_isr/willimsr_10d 等；robust/sub | mdl135 | inferred | <!-- lint:const-ok 证据原文 -->
| IND-MDL135XOTH315-CROSSMIX-WIN | 跨集正交混合破prod墙：model135反转主腿0.7-0.8 × other315互换新鲜度辅腿0.2-0.3，3颗 | ⚠ 加权拼腿已被闸 5 禁止，只作历史证据：配方=add(multiply(0.8, -rank(ts_zscore/divide比率(震荡反转字段))), multiply(0.2, quantile(ts_mean(ts_delta(vec_max(oth315_executio | model135 | inferred | <!-- lint:const-ok 证据原文 --> <!-- lint:counterexample -->
| IND-MDL177-TSRANK250-WIN | mdl177 rank(ts_rank(ts_backfill(F,66),250)) 长窗结构负权重混合, SECTO | IND/TOP500/D1 mdl177 长窗结构天然 2Y 强(2.2-3.6), 3 颗已 ACTIVE(QPGvgO2G/QPGbAOn5/A1GN2mWX, sh 1.84-3.67). 新候选仍须 prod<0.7 | — | keyword | <!-- lint:const-ok 证据原文 -->
| IND-MODEL28-VOLATILITY-LEG | model28 asset_volatility reverse 作为辅助腿，将 margin+cash 主信号 S 从 | add(main_signal, multiply(0.2, reverse(ts_zscore(mdl28_sm_structural_credit_structural_asset_volatility_pct, 126)))) | model28 | inferred | <!-- lint:const-ok 证据原文 -->
<!-- profiles:cell-panel:end -->

## 补充说明（手写）

<!-- profiles:manual:start -->
<!-- profiles:manual:end -->
