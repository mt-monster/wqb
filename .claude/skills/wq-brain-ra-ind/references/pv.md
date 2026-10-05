# IND × pv（组合分支）

> 回到 [IND 区域流程](../SKILL.md) · [IND profile（证据与历史）](../../wq-brain-ra-pipeline/references/regions/IND.md) · 实时生效画像：`$WQ_PY -m wqb.profiles explain --region IND --category pv`

<!-- profiles:cell-panel:start -->
**状态**：probe（跟区域入场 probe-only）　**分组**：PV　**类别卡**：pv

**涉及数据集**：intraday_pv_feats、pv103、pv106、pv30、pv70

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
| 143 | 47 | 29 | 10 | 8 | 2 |

主要数据集（回测数）：intraday_pv_feats（80）、pv103（52）、pv106（11）

### S1 字段理解

- 各区可用性差异大：先查本区有没有 pv1（JPN TOP1600 没有，close / adv20 / returns 不可用）
- intraday_pv_feats 目录字段 ≠ 平台可用字段：先单字段探针再成批
- 窗口（类别卡，均在白名单内）：daily 1/5/22；monthly 66

### S2 生成

- **用**：intraday_pv_feats 日内价量相关反转只作被门控的主腿：裸用 prod 0.79–0.92（IND profile）
- **用**：成本分布形状族（pv106 transaction_cost 的 max / median 尾部脆弱度）有胜绩 Wj7YP5JN；该 win 是加权写法，新候选须换合规结构复现同一机制
- **避**：pv103 尾盘反转：外部孪生在首测 1 小时内把 prod 顶到 1.0
- **避**：pv47 特质反转拥挤族（prod 0.78–0.99）
- **避**：pv106 spread / slippage / liquidity-shock 族（IND-PV106-LIQUIDITY-SHOCK-DEAD）
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

1. [组合] trade_when 慢开关：用季 / 月频慢变量把宇宙切掉约一半（进 >0.5 出 <0.4 的滞回带），如税前利润预期修正 rank<0.5、机构持股比例 rank>0.5（证据：ZYbqREW1 S 3.20 / prod 0.54；levk5JYN S 3.34 / prod 0.55（IND profile 组腿配方）） <!-- lint:const-ok 证据原文 -->
2. [全局] 判「无解 / 天花板」前先扫等价算子替换：signed_power → quantile、ts_scale → quantile / normalize。数值路径不同，一次动多个闸（含 prod，要读全部闸）（KOR/GLB 复现：KOR other466 signed_power→quantile：2Y 1.51→1.56、prod 0.6544→0.6397；GLB quantile 替 ts_scale：S +0.20、F +0.06、prod 0.475→0.565（DEC-72）） <!-- lint:const-ok 证据原文 -->
   - 注意：效应量逐区实测，禁外推；quantile 只收 1 个参数
3. [全局] 强但撞 prod 墙的快信号：用一个经济子集门控（trade_when 进 >0.5 出 <0.4 的慢变量，或 rank(cap)>0.2 ∩ 子集）只在子集里持仓（GLB/ASI/IND 复现：GLB-DL20D-SUBSET-GATE-FAMILY-20260921（prod 0.82→0.60–0.67）；ASI LLNgdpw2 / 88jaV5lv；IND ZYbqREW1 / levk5JYN（prod 0.54–0.55）） <!-- lint:const-ok 证据原文 -->
   - 前提：未门控的基础信号 IS sharpe 不低于 2.5、fitness 不低于 1.5（GLB 2026-09-27 铁律：门控只修 prod / robust，不造强度）；慢信号门控后换手会升，只用于快信号
- **不要用**：group_rank(主腿, bucket(慢变量))：只重排、不减持仓，prod 0.79–0.83（w198 / w199） <!-- lint:const-ok 证据原文 -->
- **不要用**：快变量门控（情绪 5 日比值、期权成交量 z、新闻计数）：换手 0.46–0.65、robust 掉到 0.5–0.9（w198 / w199） <!-- lint:const-ok 证据原文 -->
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
| IND-INTRADAYPV-PRICEVOLUME-CORR-REVERSAL-PRODWALL | intraday_pv_feats intraday price-volume correlation reversal | IND pv tower: intraday reversal families (last-hour, price-volume corr) are all prod-blocked; only non-reversal intraday | intraday_pv_feats | payload | <!-- lint:const-ok 证据原文 -->
| IND-IPVF-MICROSTRUCTURE-DEAD | intraday_pv_feats microstructure | 日内微结构字段族（盘口价差/深度/日内价格行为/量价相关）在 IND TOP500 SECTOR 无 alpha 转化力：cov 0.987 高覆盖不保证预测力；alphaCount 0-67 零竞争也不能作为信号存在性的证据；此类族判死不 | intraday_pv_feats | inferred | <!-- lint:const-ok 证据原文 -->
| IND-PV103-LASTHOUR-REVERSAL-PROD-TWIN | pv103 last-hour (14:30->close) return reversal |  | pv103 | payload | <!-- lint:const-ok 证据原文 -->
| IND-PV103-PV47-ROBUST-DEAD-WALL | pv103 session friction + pv47 idiosyncratic vol | IND pv103 会话摩擦信号 + pv47 特质波动率组合不再投入。Wj7YP5JN 的 robust 1.03 无法通过换 pv106 字段（transaction_cost_percentile_25/10、group_buy/se | pv103 | inferred | <!-- lint:const-ok 证据原文 -->
| IND-PV106-LIQUIDITY-SHOCK-DEAD | pv106 spread/slippage self-normalised change (liquidity shoc | pv106 in IND only as a cost/condition leg (transaction_cost_maximum/median already used by ACTIVE Wj7YP5JN); the robust- | pv106 | payload | <!-- lint:const-ok 证据原文 -->
| IND-PV70-DEAD | pv70 relationship | Avoid pv70 in IND; relationship data VECTOR fields yield zero signal after aggregation | pv70 | inferred | <!-- lint:const-ok 证据原文 -->
| IND-PV70-REGION-MISMATCH | pv70 | 用数据集前先核对 region 覆盖：pv70 字段描述含 'APAC ex-Japan, ex-China' 即 IND 无数据；get_datafields 返回 coverage 1.0 但那是 ASI 区域覆盖，非 IND | pv70 | inferred | <!-- lint:const-ok 证据原文 -->
| pv106 | slippage_transaction_cost | pv106 in IND/TOP500/D1 - do not probe further | pv106 | inferred | <!-- lint:const-ok 证据原文 -->

### 胜绩

| 条目 | 机制 | 设置与骨架 | 数据集 | 归属 |
|---|---|---|---|---|
| IND-PV106-COST-FRAGILITY-WIN | transaction_cost fragility ratio + spread deterioration reve |  | pv106 | payload | <!-- lint:const-ok 证据原文 -->
| IND-PV30-PCA-GROUPING-AXIS-LEVER | pv30 statistical industry classification as group axis |  | pv30 | inferred | <!-- lint:const-ok 证据原文 -->
<!-- profiles:cell-panel:end -->

## 补充说明（手写）

<!-- profiles:manual:start -->
<!-- profiles:manual:end -->
