# GLB × other（组合分支）

> 回到 [GLB 区域流程](../SKILL.md) · [GLB profile（证据与历史）](../../wq-brain-ra-pipeline/references/regions/GLB.md) · 实时生效画像：`$WQ_PY -m wqb.profiles explain --region GLB --category other`

<!-- profiles:cell-panel:start -->
**状态**：active（跟区域入场 active）　**分组**：Other　**类别卡**：other

**备注**：GLB 两条出货机制之一（dl_riskfree_returns 平台类别 OTHER）

**涉及数据集**：ai_news_scores、dl_riskfree_returns、other296、other315、other455、other699、techindi_model

### 回测设置（进仿真的值）

| 设置 | 值 | 来源 |
|---|---|---|
| instrumentType | EQUITY | 区域 settings.json |
| region | GLB | 区域 settings.json |
| universe | TOPDIV3000 | 区域 settings.json |
| delay | 1 | 区域 settings.json |
| neutralization | STATISTICAL | 区域 settings.json |
| decay | 2 | 区域 settings.json |
| truncation | 0.08 | 区域 settings.json |
| pasteurization | ON | 区域 settings.json |
| unitHandling | VERIFY | 区域 settings.json |
| nanHandling | OFF | 区域 settings.json |
| maxTrade | OFF | 区域 settings.json |
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
| 440 | 79 | 48 | 9 | 7 | 2 |

主要数据集（回测数）：dl_riskfree_returns（375）、ai_news_scores（34）、other296（8）、techindi_model（8）、other315（8）、other699（7）

### S1 字段理解

- 数据集名会骗人：必读字段 description；稀疏高 valueScore 是陷阱
- 窗口（类别卡，均在白名单内）：daily 5/22；quarterly 66/252

### S2 生成

- **用**：dl_riskfree_returns 20 日 CNN（single_bucket_20day_return_estimate_ohlcv_img_2）× 一个经济子集门控：未门控 prod 0.77–0.84（38 个变体），门控后 0.60–0.67
- **避**：techindi_model predicted_first_quantile 系：热门字段 prod 必超上限（qMNZX1o1 0.7686），已判穷尽
- **避**：single_bucket_20day_return_estimate_ohlcv_img_2 / single_bucket_60day 已被 prod 饱和闸拦
- **说明**：门控模板只修 prod / robust、不造强度：未门控基础信号 IS sharpe 不低于 2.5、fitness 不低于 1.5 才值得花槽位（GLB 2026-09-27 铁律）
- **类别通用原语**（类别卡，跨区）：
  - name the priced risk first; the operator is secondary
  - 先按字段 description 判断经济含义，再套对应类别卡的思路（例：KOR other466 是财务比率 → fundamental；IND other532 是 Barra 特质收益 → 残差反转）
- **跨区结论**（KOR/EUR/DEU/GBR；negative）：other455 网络嵌入（n2v）族（证据：KOR RULES §G；EUR-W253-OTHER455-CUSTOMER-NETWORK-RETURNS；DEU-OTH455-PURECOMP-SUBUNIVERSE-WALL-20260923；GBR 红榜） <!-- lint:const-ok 证据原文 -->
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

- 资格判定：`$WQ_PY tools/mode_b_qualify.py evaluate --region GLB --sharpe <S> --fitness <F> --two-year-sharpe <2Y>`（喂全指标，旁路 A–E 才会生效）
- 提交链：`submit_verdict` 只否决；prod 与 self 双端点实测（`check_correlation(refresh=True)`）；用户明确确认后才 `workflow_submit_alpha(confirm_submit=True)`——见 `worldquant-submit-alpha`

### 判死记录（不要重试；「归属」= payload 绑定 / 由条目名推断 / 关键词推断）

| 条目 | 族 | 下次怎么办 / 说明 | 数据集 | 归属 |
|---|---|---|---|---|
| GLB-AINEWS-TS-DELTA-STRENGTH-WALL | ai_news_scores 情绪变化率族（ts_delta 净情绪） |  | ai_news_scores | payload | <!-- lint:const-ok 证据原文 -->
| GLB-DLRF-CNN-ESTIMATE-PROD-WALL | dl_riskfree_returns OHLCV 图像 CNN 市场中性收益预测（single_bucket_{5,2 |  | dl_riskfree_returns | payload | <!-- lint:const-ok 证据原文 -->
| GLB-DLRF-NEWGEM-139-PROD-WALL-20260925 | dl_riskfree_returns 全族新 GEM 139 条回测（single_bucket/probabilit | GLB dl_riskfree 新 GEM 路线封死；不再投任何同族变体 | dl_riskfree_returns | payload | <!-- lint:const-ok 证据原文 -->
| GLB-MODELTOWER-DLCHART-COLDVARIANTS-FASTKILL | DL 图像预测族冷门变体（techindi_model 分位概率/预测、tech_chart_model 连续预测、ch |  | techindi_model | payload | <!-- lint:const-ok 证据原文 -->
| GLB-OTH315-EQUITY-SWAP-NOISE-20260927 | other315 OTC 权益互换报备（互换成交价 vs 现价基差、名义额存量与增速、成交笔数、合成杠杆强度、名义额/流 |  | other315 | payload | <!-- lint:const-ok 证据原文 -->
| GLB-OTH699-RETAIL-FLOW-FASTKILL |  |  | other699 | payload | <!-- lint:const-ok 证据原文 -->
| GLB-W03-OTHER455-NO-SIGNAL | other455 competitor_n2v_pca 族 |  | other455 | payload | <!-- lint:const-ok 证据原文 -->

### 胜绩

| 条目 | 机制 | 设置与骨架 | 数据集 | 归属 |
|---|---|---|---|---|
| GLB-AINEWS-TS-DELTA-DECORRELATION-WIN | 情绪水平信号 prod 饱和 → 变化率正交化方法论 |  | ai_news_scores | payload | <!-- lint:const-ok 证据原文 -->
| GLB-DL20D-SUBSET-GATE-FAMILY-20260921 | dl_riskfree_returns 20d 回归预测 × 经济子域门控（可复制的 prod 破墙模板） |  | dl_riskfree_returns | inferred | <!-- lint:const-ok 证据原文 -->
<!-- profiles:cell-panel:end -->

## 补充说明（手写）

<!-- profiles:manual:start -->
<!-- profiles:manual:end -->
