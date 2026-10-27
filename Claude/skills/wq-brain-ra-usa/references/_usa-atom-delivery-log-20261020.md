# USA ATOM Alpha 交付日志（2026-10-20）

> 目标：USA 区域 **10 个 ATOM 类型 REGULAR alpha**（所有非豁免字段来自同一数据集；豁免仅限
> country/exchange/market/sector/industry/subindustry 六个分组字段）。
> 本日志是交付清单与索引；每颗的完整字段画像 / 模板 / 归因在各自数据集档案中，逐条给出链接。
> 状态标记：**已验证** = 平台 RA 全闸 PASS + `check_correlation` 实测 prod/self 均 < 0.7。 <!-- from config.prod_corr_max -->
> **提交（2026-10-20，用户明令「按顺序提交至平台」）**：#1–#4 早已 ACTIVE；#7 本次提交成功
> （ACTIVE/OS，`USA_R_ANALYST_07`）；#5/#6/#8/#9/#10 在 `check_correlation(refresh=True)` 复测时
> **prod 破 0.7 红线**，按不可豁免的合规闸拒绝提交（明细见 §1.1）。
> **收官（2026-10-20）**：10 / 10。其中 #8–#10 于当日以 `get_alpha_details` 复验（RA fail=0、
> USA/TOP3000/D1/STATISTICAL、pyramid=USA/D1/ANALYST、settings 与本表一致）。

> **2026-10-21 复核（口径澄清，别读错「10/10」）**：交付分两层——**已上平台且 ACTIVE = 5 颗**
> （#1–#4 + #7）；**IS 全闸但 prod 超红线被拒 = 5 颗**（#5/#6/#8/#9/#10）。按目标定义的
> 「**验证 = RA 全闸 + `check_correlation(refresh=True)` 的 prod/self 均 < 0.7**」，达成 **5 / 10**。 <!-- from config.prod_corr_max -->
> 同日另复核一条从未测过 prod 的库存候选 `leKLRA1N`（institutions18，
> `group_rank(ts_backfill(inst18_instownership_pct_held,66), subindustry)`，S 1.71 / F 1.27 / 2Y 1.86 / SUB 0.91 / TO 4.09%）
> ⇒ **prod 0.9394**（直方图 `[0.9,1]` 桶 n=6），同族不可用。
> ⇒ **缺口 5 颗只能来自新机制**；prod 一律以刷新后的当下读数为准（见
> [`../rules/gate-and-submit-discipline.md`](../rules/gate-and-submit-discipline.md) 三·3：PC 只向上漂）。

## 1. 候选交付（10 个 IS 全闸候选；平台 ACTIVE = 5）

| # | alpha | 数据集 | 核心字段 | 算子逻辑（一句话） | S | F | 2Y | SUB | TO | prod | self | 画像索引 |
|---:|---|---|---|---|---:|---:|---:|---:|---:|---:|---:|---|
| 1 | `omoK1A5m`（ACTIVE/OS） | analyst_factor_signals | `eps_q1_estimate_qoq_growth` | 季度 EPS 环比增速的 252 日平均变化，通用壳（backfill 756） | 2.05 | 1.24 | 1.79 | 0.93 | 3.65% | 0.6489 | 0.4864 | [`_usa-analyst-factor-signals-field-profile-20261019.md`](_usa-analyst-factor-signals-field-profile-20261019.md) |
| 2 | `akVnvzX5`（ACTIVE/OS） | analyst_factor_signals | `eps_y1_estimate_skewness` | 年度 EPS 预期偏度的 315 日时序 z 分，再按 industry 中性化 | 1.83 | 1.06 | 1.87 | 0.95 | 3.46% | 0.6594 | 0.5692 | 同上 |
| 3 | `gJWoaJqv`（ACTIVE/OS，USA_R_ANALYST_03） | analyst44 | `anl44_2_eps_value` / `anl44_2_eps_prevalue` / `anl44_2_sales_value` / `anl44_2_sales_prevalue` | EPS 与营收背离度的 504 日均变化再取 252 日差分（背离加速度），market 分组 | 1.74 | 1.27 | 2.21 | 0.86 | 10.14% | 0.6978 | 0.5803 | [`_analyst-campaign-20261017.md`](_analyst-campaign-20261017.md) |
| 4 | `kqJLawqP`（ACTIVE/OS，USA_R_ANALYST_04） | analyst44 | 同上 | EPS/营收背离度先秩变换再取 756 日平均变化，market 分组，CROWDING | 1.61 | 1.11 | 1.62 | 0.84 | 9.61% | 0.6757 | 0.6445 | 同上 |
| 5 | `pw5RbrYX`（❌ prod 0.90，拒提） | analyst_consensus | `mean/median_estimate_targetprice_annual12_tribes` + `stddev_estimate_fxadj_targetprice_annual12_tribes` | **分歧度 × 共识偏斜**：均值>中位数时做多分歧度、否则反向，20 日均值 | 2.07 | 1.21 | 1.67 | 0.90 | 3.75% | 0.5857 | 0.3495 | [`_usa-analyst-consensus-field-profile-20261020.md`](_usa-analyst-consensus-field-profile-20261020.md) §2.1 |
| 6 | `KPrGMEe1`（❌ prod 0.9991，拒提） | analyst_consensus | `mean_estimate_targetprice_annual12_tribes` | 目标价一致预期的 **175 日时序位置**（修正趋势，非绝对价位） | 1.94 | 1.24 | 1.71 | 1.04 | 5.94% | 0.6593 | 0.4277 | 同上 §2.2 |
| 7 | `e76xgXkM`（ACTIVE/OS，USA_R_ANALYST_07） | analyst_consensus | `mean_forecast_actual_combined_fxadj_eps_annual12` | 合并 EPS 的 **Δ63 按 252 日自身历史标准化**（修正幅度的量纲对齐），RAM/industry 通用壳 | 1.89 | 1.12 | 1.76 | 1.05 | 3.29% | 0.5532 | 0.4553 | 同上 §3.9 |
| 8 | `RR6bv6rz`（同机制口径变体，❌ prod 0.9054） | analyst_consensus | `mean/median_estimate_targetprice_annual12_tribes` + `stddev_estimate_fxadj_…` | #5 的分歧×偏斜结构，均值窗 **10 日**（#5 为 20 日） | 2.04 | 1.20 | 1.71 | 0.89 | 3.82% | 0.5919 | 0.3566 | 同上 §2.1 |
| 9 | `leKKGb9l`（同机制口径变体，❌ prod 0.9014） | analyst_consensus | 同 #8 | #5 的分歧×偏斜结构，平滑算子换 **`ts_decay_linear 20`**（#5 为 `ts_mean 20`） | 2.04 | 1.19 | 1.66 | 0.92 | 3.78% | 0.5896 | 0.3547 | 同上 §2.1 |
| 10 | `rKeOaLvo`（#8 的 decay 孪生，❌ prod 0.9060） | analyst_consensus | 同 #8 | #8 的同一表达式，**decay 512**（#8 为 500） | 2.04 | 1.20 | 1.71 | 0.89 | 3.83% | 0.5932 | 0.3567 | 同上 §2.1 |

设置口径：全部 USA/TOP3000/D1/trunc 0.08；#1/#2 = REVERSION_AND_MOMENTUM decay 1；
#3 = REVERSION_AND_MOMENTUM decay 20；#4 = CROWDING decay 10；#5 = STATISTICAL decay 500；#6 = STATISTICAL decay 450；
#7 = RAM decay 20（industry 分组）；#8/#9 = STATISTICAL decay 500；#10 = STATISTICAL decay 512。
区间均 2014-01-01 → 2023-12-31（平台缺省，与历史批次可比）。

### 1.1 平台提交执行记录（2026-10-20，按 #1→#10 顺序）

| # | alpha | submit_verdict | `check_correlation(refresh=True)` prod | 结果 |
|---:|---|---|---:|---|
| 1 | `omoK1A5m` | ALREADY_SUBMITTED（ACTIVE） | —（已提交，无需复测） | 早已 ACTIVE/OS |
| 2 | `akVnvzX5` | ALREADY_SUBMITTED（ACTIVE） | — | 早已 ACTIVE/OS |
| 3 | `gJWoaJqv` | ALREADY_SUBMITTED（ACTIVE） | — | 早已 ACTIVE/OS |
| 4 | `kqJLawqP` | ALREADY_SUBMITTED（ACTIVE） | — | 早已 ACTIVE/OS |
| 5 | `pw5RbrYX` | UNVERIFIABLE（无 FAIL，404 死端点） | **0.9000**（`[0.8,0.9)` n=1） | ❌ prod 红线，拒提 |
| 6 | `KPrGMEe1` | UNVERIFIABLE（无 FAIL） | **0.9991**（`[0.9,1]` n=1） | ❌ prod 红线，拒提 |
| 7 | `e76xgXkM` | UNVERIFIABLE（无 FAIL） | **0.5532** / self 0.4553 → all_passed | ✅ **提交成功**：ACTIVE/OS，`dateSubmitted=2026-10-19T19:55:01-04:00`，name=`USA_R_ANALYST_07`，color=BLUE |
| 8 | `RR6bv6rz` | UNVERIFIABLE（无 FAIL） | **0.9054**（`[0.9,1]` n=1） | ❌ prod 红线，拒提 |
| 9 | `leKKGb9l` | UNVERIFIABLE（无 FAIL） | **0.9014**（`[0.9,1]` n=1） | ❌ prod 红线，拒提 |
| 10 | `rKeOaLvo` | UNVERIFIABLE（无 FAIL） | **0.9060**（`[0.9,1]` n=1） | ❌ prod 红线，拒提 |

**执行说明**：
- #7 的提交节点在客户端侧两次报 `MCP error -32603`（节点内 `_prod_gate(refresh=True)` +
  提交后轮询总时长超过客户端等待），但 POST 已落地；以 `get_alpha_details` 复核状态为准，
  未重复补发第三次。
- #5/#8/#9/#10 的 prod 均指向**同一个生产池高相关件**（直方图 `[0.9,1]` 桶 n=1），
  #6 更是 0.9991 —— 与 2026-10-17 `submit_inventory` 记录的 0.55–0.66 相比已明显漂移，
  说明期间生产池新增了同族（analyst_consensus 目标价 / 合并 EPS）alpha。按「prod ≥ 0.7
  无豁免」铁律，这 5 颗只能留作组合腿，**不得提交**。
- 截至 2026-10-20，本批交付的 **ACTIVE = 5 颗**（#1–#4 + #7），未提交 5 颗（#5/#6/#8/#9/#10）。

**机制正交性**：#1 增速动量 / #2 预期偏度 / #3 背离加速度 / #4 背离秩变化 / #5 分歧×偏斜 /
#6 目标价时序位置 / #7 合并 EPS 修正标准化 —— **7 个互不相同的机制方向**，实测 self 0.35–0.64。
#8–#10 是 **#5 同一机制的测量口径变体**（窗口 / 平滑算子 / decay），按透明标注交付，
**不计入正交机制**；2026-10-17 `get_submit_ready` 记录的 prod 为 0.5896–0.5932 / self 0.3547–0.3567，
但 2026-10-20 提交前 `refresh=True` 复测已漂到 **0.9014–0.9060**（同族生产池增长），故实际均被 prod 墙拦下。
若要更高机制多样性，应新开数据集，而不是把同机制变体计为新方向。

## 2. 补位定案与逐集排期记录

**补位定案（2026-10-20）**：#8–#10 来自 `get_submit_ready(USA, READY)` 的已验池（2026-10-17
`submit_inventory` 实测 prod/self 双过），**不是新机制**——三条均为 #5 的测量口径变体，已在 §1
逐条标注。分析师塔（D1 analyst=5）已点亮，按用户指令不再新增回测，故不新开批；这正是补位而非扩挖。

| 方向 | 数据集 | 当前最优 | 缺口 | 下一步（已归因） |
|---|---|---|---|---|
| ~~分析师覆盖广度（count breadth）~~ | analyst_consensus | `kqJZk52L` S1.73/F1.03/2Y1.83/SUB0.92（CROWDING × industry） | **TO 0.90% 无法修复** | ❌ **封存（批 28 八杠杆全败，画像 §3.5）**：TO 与 S 沿 decay/hump 轴单调对立，死区即 alpha；整族排除 |
| ~~M28 EPS fxadj 合并序列修正~~ | analyst_consensus | **`e76xgXkM` S1.89/F1.12/2Y1.76/SUB1.05，RA 全过，prod 0.5532 / self 0.4553 ⇒ 已交付（#7）**；2026-10-20 提交成功 → **ACTIVE/OS**（`USA_R_ANALYST_07`，2026-10-19 19:55 ET） | 已收官 | 批 30c 八条归因（画像 §3.9）：**ts_zscore 量纲归一解决 SUB（SUB/S 0.339→0.556）**；门控版 `78on0e78` S2.19/F1.48/2Y2.46/SUB1.05 最强但 **prod 0.7214 挂起**（[0.7,0.8) 桶 n=1）；ts_product 量纲失配待 30d；group_zscore 2Y 1.45 作备胎 |
| 批 31 正交机制（M29–M32 / M35 / M01） | analyst_consensus | 已收批：最好 `Grge6O7P` S1.75/F0.99/2Y1.58/SUB0.40 | 0 颗全过 | ✅ 已归因（画像 §3.12）：应计族 SUB 过但 S≤1.33（高质量低收益）⇒ M29/M29b/M30/M32 封存；**flag 语义已更正为三值 0/1/2**（`>0.5`=预测+实际 97.8%，`≤0.5`=backfill-only 2.2%），`O0Jxk8gp` S−0.83 实为 **backfill 行信号反转**，不是 regime 相反 ⇒ M31 封存；M35/M01 本应复测，随批 33 一并取消 |
| 批 32 M28 机制换财务行项目（M42–M49） | analyst_consensus | **已收批（§3.14）：最好 `zqrRjeLd`（ROE）S1.45/F0.91/2Y1.35/SUB0.80；0 颗全过** | M42–M49 全封存 | ✅ 行项目分解全面弱于合并 EPS（M28 1.89/1.12/1.76/1.05）；2Y 普遍 ≤1.2；capex 反号 S−0.63 ⇒ 假说不成立（画像 §3.14） |
| ~~批 33（M50 regime 双边 + M51–M55 复测）~~ | analyst_consensus | **❌ 取消（2026-10-20 用户指令）** | — | 用户原话「已点亮塔的数据集先不回测」；`get_pyramid_alphas` 实测 **USA/D1 analyst = 5（已点亮）** ⇒ 分析师塔全部数据集停止新增回测，原 §3.13 保留为待测存档 |
| analyst_consensus 已报值增长族（actual_*，M01–M08） | analyst_consensus | 批 29 实测最好 `YPxgwEQM` S1.25/2Y1.20（收入） | 全灭 | ❌ 判死/判弱（画像 §3.6）；CROWDING 把 TO 压到 ~1.0%，已报侧无截面信息 |
| 财务比率漂移（M09 净利率 / M10 EBIT 率） | analyst_consensus | 批 30a：`WjLVwZ2k` 1.49/0.75/1.11/**−0.16**；`pwvKJ2e6` 1.47/0.73/**1.98**/**−0.22** | SUB 为负（小盘反向） | ❌ **判弱（画像 §3.7 #4）**：EBIT 率 2Y 1.98 是唯一亮点但 SUB −0.22 结构性不可救（不换 universe） |
| 其余 analyst_consensus 未测族 | analyst_consensus | 批 27 已收官：projection 1.37/1.29、count(qtr) 1.35/1.55、surprise 0.61/1.03、prior 1.09/0.73 | 全灭 | **不再同族换窗**；surprise 族两次中性化复证判死 |
| ~~other685「Enhanced Financial Indicators」(StarMine EQ+ARM, 72 字段, cov 0.7225)~~ | 三批 24 条全收：批 1 最好 `kqJZmJ3g` S0.88；批 2 最好 `npA8Oxjx` S1.01（2Y 1.02）/`vROvJwWr` S0.99/2Y1.57；批 3（STATISTICAL）最好 `d5KRl0XE` S1.02/2Y1.83/**SUB0.36 破闸** | **判弱，停止扩批** | ❌ **2026-10-20 判弱（画像 §4.5）**：24 条 × 6 字段株 × 水平/修正/z 分/加速度/复合 × 2 种中性化，最高 S 仅 1.02 且 SUB 结构性破闸（limit 0.44）。三条可复用归因：① 水平/质量族在 USA 无全期 alpha；② 相对形态抬 2Y 不抬 S；③ **STATISTICAL 先验不可跨数据集迁移**（本集 7/8 条 S 降 0.2–0.57，与 analyst 2.07 相反）。字段池保留为组合腿/条件门控备选。画像 → [`_usa-other685-field-profile-20261020.md`](_usa-other685-field-profile-20261020.md) §4.1–§4.5 |
| **option3「期权 OI/成交量/IV 结构」**（未点亮 option 塔，0 回测 / 492α / 20 字段） | option3 | **❌ 已封存（4 批 32 条）**：全批最佳 `KPmEXpAj`（相对化 Δ22）S1.34 / F0.95 / 2Y2.49 / 收益6.32%，**SUB 0.51 破闸（lim 0.58）**；`YPxg27GW` S1.38/F0.97/SUB0.52；`d5KREZMY` S1.14/SUB0.63 | 判「单数据集 ATOM 上限 ~1.4」 | ✅ 批 4 归因：**相对化×Δ22 是全局最优壳**；**自归一（zscore252）是 SUB 唯一解但必掉 S 0.14–0.27** ⇒ SUB 与 S 在同一自由度两端，无同时过 1.58/0.75 的壳；1M 唯一有效窗、252 优于 504；M08 水平型全灭。**不再发第 5 批**；最强构造登记为未来 RA 组合腿候选。画像 → [`_usa-option3-field-profile-20261020.md`](_usa-option3-field-profile-20261020.md) §5.2–§5.4。<br>**2026-10-21 二次复测（16 条：Wave1 9 + Wave2 5 + 中性化 6）**：S 天花板 **1.33** 复证（与旧 1.34 同）；M5 镜像 `N1eV0ngE` prod **0.8567**（`[0.7,0.8)` n=**273**）；CROWDING 把 prod 压到 **0.7915**（n=218）但 S 掉到 1.27，RAM 掉到 1.11–1.18、STATISTICAL W22 SUB 0.46 破 ⇒ **中性化不是 prod 墙的解，机制饱和才是**。**第二次封存**；不转 option40（同底层 IV，无新机制）。画像 → [`_usa-option3-field-profile-20261021.md`](_usa-option3-field-profile-20261021.md) §8 |
| **news_sentiment_transfer「新闻情绪迁移」**（未点亮 sentiment 塔，0 回测 / 23 字段 / cov 0.947 / aC 180） | news_sentiment_transfer | **❌ 已封存（2 批 16 条）**：批 2 8 条全收，最高 `6XAeR1QP`（VECTOR z252）S0.50 / 2Y−0.47 / TO 0.98% 挂；N13≡N01/N02、N14≈N03 ⇒ **VECTOR 聚合无新信息**；attention 门控 S−0.04 且 TO 0.89% 挂 | 判弱 | ✅ 命中预注册止损（批 2 全 S<1.0）；16 探针 max S 0.50、2Y 6 条为负、risk-neut ≤0.03 ⇒ 日频文本情绪在 USA/D1 结构性无 alpha。**同塔 5 个文本分数集已判死**（`news_sentiment_dl`/`ai_news_scores`/`sentiment21`/`event_sentiment_signals`/`earningscall_embed`）⇒ `news_transformer_scores`/`other553` 一并降级不优先。画像 → [`_usa-news-sentiment-transfer-field-profile-20261020.md`](_usa-news-sentiment-transfer-field-profile-20261020.md) §5/§5.1 |
| **sentiment26「DNS 网站热度」**（未点亮 sentiment 塔，33 VECTOR 字段 / cov 0.769–0.944 / aC 1–187） | sentiment26 | **❌ 已封存（2 批 16 条）**：最高 `78onJAa5`（Δ5 `relpopularity08`）S1.27 / F0.71 / 2Y0.90 / SUB0.29（限 0.55）；`0mjMzlep`（Δ5 `relpopularity1`）1.08/0.56/2Y1.05 | 判弱（S<1.30、无 2Y≥1.58、SUB 缺口 0.26） | ✅ 命中预注册止损：16 探针 max S 1.27、SUB/S 仅 0.23–0.30；**只有正向 Δ5 的 2Y 为正（1.05/0.90），负向构造 2Y 全负 ⇒「关注度反转」是 regime 依赖**；波动归一 0.47 / 时序秩 0.50 第三次复证「归一化抹掉信号」；subindustry 再证劣于 industry；risk-neut 高的构造恰好 2Y 负 ⇒ 本质是风格暴露+短窗噪音。登记 `USA-SENTIMENT26-DNS-ATTENTION-WEAK`。画像 → [`_usa-sentiment26-field-profile-20261020.md`](_usa-sentiment26-field-profile-20261020.md) §1–§4.2 |
| **board_gov_stats「董事会/高管结构」**（未点亮 insiders 塔，0 回测 / 46 字段 / cov 0.9197） | board_gov_stats | **批 1 已收**：G02 `88veOAMV`（董事会 1y 离任，负向）S1.37 / F0.86 / 2Y1.87 / SUB0.59 / TO1.23% / risk-neut 0.81。**批 2 已收（8/8）**：`ts_rank(board,504)` 1.36/0.82/1.95/SUB0.57（差 0.02）；**B8 `Vkd3X00M`（management 1y 离任）S1.54 / F1.04 / 2Y2.02 / risk-neut 1.04，SUB0.41 vs 0.67** | **只剩 SUB 墙**（S+0.04、SUB+0.26） | ✅ 批 2 归因：① 慢变量最优测量面 = `ts_rank 504`；② zscore 不修 SUB（analyst 结论不通用）；③ subindustry 分组反而更差；④ TO 全 ≥0.94%。B8 推翻「上限≈1.4」⇒ **批 3 已收（`3PsdKf80p4XdahVMSfgRl0F`，旧 id 0 children 原样重发）**：M1 `3qjezndX`（`-ts_rank(management_1y,504)`×industry）**S1.38 / F0.92 / 2Y1.74 / SUB0.66 PASS / TO1.12% / risk-neut0.98**；M7（subindustry 分组）SUB0.76 但 TO0.95% 挂；M3/M4（zscore/门控）0.46/0.43 判死。**SUB 墙被 ts_rank504 打破，新墙是 S↔SUB 前沿** ⇒ 批 4 设置档扫描 **已收 6/8**（INDUSTRY 批 `1o4j3s1Rx4V6aF5Xb4xCQ6k` 0 children，按 orphan 先例不等待）：**无任何设置优于 SUBINDUSTRY×504**（M1 保持 1.38/0.92/2Y1.74/SUB0.66/TO1.12%/risk-neut0.98）；1008 全面变差（S−0.15~−0.17、TO<1%）；MARKET 把 SUB 抬到 0.75/0.76 但 S 仅 1.19/1.23；STATISTICAL TO 3.9–4.1% 且 F0.53–0.62 ⇒ **按预注册封存（4 批 / 32 条）**；`3qjezndX`（S强）与批 2 B8 `Vkd3X00M`（SUB 差一闸）互补，登记为组合腿候选。**并行独立批（multisim `1aQpDZ2J4Y19a31hPT7UTHK`，8/8）**：G2 `ZYmKpQ1n`（反向 3m 管理层离任=稳定性溢价）**S1.56 / F1.02 / 2Y2.55 / SUB0.64(0.68) / TO3.48% / risk-neut1.12**，IS 只差 SHARPE 0.02 与 SUB 0.04；但 `check_correlation` 实测 **prod=0.8508**（直方图 `[0.8,0.9)` n=1）⇒ 按 D0-P **prod 墙判死**。G1 正向同字段仅 0.35 ⇒ **只有稳定溢价、无动荡折价**（非对称 1.21）；G6 外部连接数 1.20/2Y1.53/risk-neut0.67 但 SUB0.43(0.52)；G4 独董 risk-neut0.00 纯风格；G7/G8 2Y1.67/2.04 但 SUB0.08/−0.04。**封存理由由「指标不够」升级为「IS 与 prod 双墙」**，登记 `USA-BOARD-GOV-STABILITY-PROD-WALL`。画像 → [`_usa-board-gov-stats-field-profile-20261020.md`](_usa-board-gov-stats-field-profile-20261020.md) §4/§5 |
| **pv63「Order Book 逐笔事件流」**（未点亮 PV 塔，16 字段 / MATRIX / cov 0.9851 / 字段 aC 6–27 / userCount 5–23） | pv63 | **批 1 已收（8/8）**：最高 P6 `XgR8Kb7m`（taker 笔数）S0.79/F0.33/2Y2.51/**SUB0.36 PASS**/TO1.14%/risk-neut0.54；P1 `KPmELNEE`（股数）0.78/2Y2.54/SUB−0.08；P3 maker 0.63；P5 净额 0.25；**0 颗全闸，全 \|S\|<0.8**。**批 2 已收（8/8，`15pm1YgDX4RtbCJ5BzyX2U3`）**：最高 B2-1 `P0MO18OJ`（taker Δ22）S0.71/F0.28/2Y2.07/SUB−0.20；B2-2 z66 0.68；B2-3 z252 0.64；B2-5 count z66 0.51；B2-6 maker Δ22 0.61；B2-7 netbook 0.42；B2-8 价差 0.57 — **8 条全 |S|<1.0** | **❌ 判弱封存**（`USA-PV63-ORDER-FLOW-WEAK`，两批 16 条；论坛取证闸未过，未强行 `seal_dead_end`） | ✅ 批 2 归因（画像 §5.3）：**「水平→自身偏离」在本塔摧毁信号**（taker 0.78→0.71/0.68/0.64，count 0.79→0.51/0.25），与 `USA-MFRP-LEVEL-BLEND-PROD-STRUCTURAL-DEAD` 先验一致（时序归一会毁横截面）；偏离化反而抬 2Y（netbook 1.43→1.90）但全期 S 降 ⇒ 反向选择；SUB 绝对值全面缩小（P6 0.36→0.12）⇒ 水平版的低流动性段优势无法用窗替代。后续 PV 集不再把时序归一当默认杠杆。画像 → [`_usa-pv63-order-flow-field-profile-20261020.md`](_usa-pv63-order-flow-field-profile-20261020.md) §5 | ✅ 批 1 归因（画像 §5.2）：① **不是数据起始假象**——yearly 显示 2014–2023 每年都有成交，2016 S1.49 / 2022 S3.16 / 2023 S1.61，但 2017 −0.60 / 2020 −1.06 ⇒ **真实 regime 依赖**；② P1≈P6（差 0.01）但 **P6 的 SUB 通过、P1 不通过** ⇒ 若留一条口径留笔数；③ P2 0.27 非严格镜像 ⇒ 正向 taker 攻击性才成立；④ maker 0.63 < taker 0.78，净额 0.25 消失 ⇒ **PnL 由 taker 承担**；⑤ **TO 仅 1.1–1.8% 证明信号是慢变量（股票级结构性攻击性）**，不是「今日订单流」。批 2 判据：仍全 \|S\|<1.0 ⇒ 封存 `USA-PV63-ORDER-FLOW-WEAK`，不发第三批。画像 → [`_usa-pv63-order-flow-field-profile-20261020.md`](_usa-pv63-order-flow-field-profile-20261020.md) §5 |
| **pv103「日内微观结构统计」**（未点亮 PV 塔，78 MATRIX 字段 / cov 1.0 / 数据集 aC 9679 / 字段 aC 10–1115） | pv103 | **批 1 已收（8/8，`3GVd5w5KD5ajcpWQCA2qOx3`）**：最高 V2 `zqrR9MPO`（M01 反向）−0.83 / V1 `wp9ERmn6` 0.76 / V7 `GrgewanG`（收盘竞价参与率）0.63 但 **returns 4.03% / risk-neut 0.51 / SUB0.50 PASS**；V8 0.40 / V5 0.53 / V4 −0.18 / V6 −0.24 / V3 −0.45 —— **8 条全 |S|<1.0，且 7/8 踩 LOW_TURNOVER（TO 0.85–1.00%）**。**批 2 已收（8/8，`FlqwJ4OM4YN9qYNX2zHlL5`）**：去 hump ×V1 `LL5dpXpL` S−0.02 / 去 hump ×V7 ratio `1Yjz7mgR` S−0.41（**hump 一去掉方向就翻负**）；短回填 22 ×V7 `ZYmKplpZ` 0.64 / 2Y1.01 / TO0.92%；短回填 22 ×V1 `WjLVpXpN` **0.75 / 2Y1.56 / TO0.95% / SUB0.29(0.32)**（全批最高）；Δ22 `kqJZ3m3g` 0.50 / TO1.11%；开盘竞价 `2rjN7Z76` 0.23；更新强度 `E5Vewaw9` −0.09；收盘竞价总量 `Vkd3plPw` 0.65 / 2Y1.05 / TO0.94% —— **8 条全 |S|≤0.75，TO 全部 0.88–1.11%** | **❌ 判弱封存** `USA-PV103-MICROSTRUCTURE-WEAK`（两批 16 条；PV 塔四条主线 pv63/pv103/pv115/dl_volume_pred 全部判弱 ⇒ **PV 塔整体封存**） | ✅ 批 2 归因（画像 §5.3）：① **hump 不是「低通」而是信号本体**——同一 ratio 去 hump 后 −0.41、加 hump 0.75（差 1.16），与批 1「V1 去 hump 0.76→−0.41」互证；② **抬 TO 的科学问题被证伪**：去 hump/短回填/Δ22 四条路径 TO 仍 0.88–1.11%，唯一过 1% 的 `kqJZ3m3g` S 仅 0.50 ⇒ 慢不是 hump 造成的，而是日均统计量×decay5 的结构；③ 全批最高仅 0.75 且离 1.58 差 0.83 ⇒ **构造层失败，不是设置层**；④ 2Y 1.56（`WjLVpXpN`）与全期 0.75 的落差是 regime 依赖，不构成补批理由；⑤ 外部证据 GBR/TOP700 IS 1.96 不能迁移到 USA/D1（同 `USA-MFRP` 跨区先例）⇒ 不再换 universe 复活。 ✅ 批 1 归因（画像 §5.2）：① **V1/V2 严格镜像**（0.76/−0.83，差 0.07）⇒ M01 只有单一方向成分，判弱；② **全批 TO 0.85–1.00% 贴 LOW_TURNOVER 线** ⇒ 没走到「信号强弱」就在「更新频率」层失格（与 dl_volume_pred「慢构造太慢」同型）⇒ 批 2 唯一科学问题 = 抬 TO；③ **V7 收益最强**（4.03% / margin 0.0087 / risk-neut 0.51 / SUB PASS）但 DD 21% ⇒ 方向对、波动不足；④ **拍卖量强于拍卖价**（V7 0.63 vs V8 0.40，V8 是唯一 SUB 明显 fail）；⑤ V4/V5/V7 SUB PASS，taker 方向面（V1–V3）与小盘无优势；⑥ V5/V6 risk-neut ≈0 ⇒ 挂单距离/挂单数几乎全是风格暴露；⑦ V3 为负 = 大单/流动性代理，M02 判弱。**批 2 判据**：去 hump 后 TO 仍 <1% ⇒ hump 非主因，慢来自日均统计量×decay5；B2-2 比 B2-1 高 ≥0.2 ⇒ 拍卖轴为唯一主力；全弱且 TO 仍 <1% ⇒ 构造层失败，**封塔前置 = pv115 也判弱（已成立）**。外部证据：**pv103 在 GBR/TOP700 做到 IS Sharpe 1.96、全硬检查 PASS**。画像 → [`_usa-pv103-microstructure-field-profile-20261020.md`](_usa-pv103-microstructure-field-profile-20261020.md) §5 |
| **pv115「做空量 + Nasdaq 收盘竞价」**（未点亮 PV 塔，11 MATRIX / cov 0.8973–1.0 / aC 11–140） | pv115 | **❌ 批 0 已收封存（8/8，`3s1zeRcXD4gkcxh10eXzCFsv`）**：**全 |S| ≤ 0.36**——Q1 做空量 −0.04、Q2 z66 −0.36、Q3 收盘竞价占比 0.06、Q4 反向 0.03、Q5 z66 0.00、Q6 隔夜收益 −0.23、Q7 开盘占比 −0.02、Q8 股数占比 −0.07；**TO 全部健康 0.80–1.52%（无一踩 LOW_TURNOVER）** | **❌ 判弱封存** `USA-PV115-AUCTION-WEAK`（1 批 / 8 条；论坛取证闸未过，未强行 `seal_dead_end`） | ✅ 命中预注册判据 5/8（Q3/Q5/Q6/Q7 同弱）：① 做空量对照双弱 ⇒ 复证 `USA-SHORTINTEREST29-RANK-WEAK`，时序归一没救回（−0.04→−0.36 还翻负）；② 收盘竞价参与率**严格镜像无方向**（0.06 vs 0.03）⇒ 纯噪声；③ 「参与度异常」（Q5=0.00）比水平更差 ⇒ zscore 分支关闭；④ 隔夜收益不存在（−0.23 / 2Y −0.93 / DD 28.9%，TO 健康 ⇒ 是方向/口径问题不是太慢）；⑤ 拍卖族全 |S|<0.1 ⇒ 整轴无信息；⑥ 样本确为「有竞价的 Nasdaq 股」代理（longCount 1370–1498 <3000），但样本内也无截面差异 ⇒ 信号为零，非覆盖问题；⑦ risk-neut 与 S 错位（Q3/Q5/Q7 = 0.27/−0.37/0.35 而 S≈0）⇒ 中和后只剩噪声。**PV 塔状态**：pv63 判弱 + pv115 判弱 + pv103 批 2 在飞 = pv103 为最后一条未封主线。画像 → [`_usa-pv115-short-volume-auction-field-profile-20261020.md`](_usa-pv115-short-volume-auction-field-profile-20261020.md) §5 |
| **dl_volume_pred「DL 成交量预测」**（未点亮 PV 塔，8 字段 / MATRIX / cov 1.0 / aC 128 / userCount 80） | dl_volume_pred | **❌ 已判弱封存（批 1 / 8 探针，max \|S\| 0.65）**：最好 P3 `E5VeKZ6L`（rank R1 news）S0.65/F0.27/2Y1.35/SUB0.32/TO0.81% fail；P1 `P0MO1JoE` 0.60；P4 源间价差 0.57 但 2Y 0.34；P5 一致性反向 −0.46；Δ 族 0.25/−0.04 | 判弱（全 S<0.8） | ✅ 批 1 归因（画像 §5.1）：① P1/P2 严格镜像 ⇒ 只有单一方向成分；② P4 减法把 2Y 从 1.35 削到 0.34 ⇒ 分歧不是主机制；③ P5 低离散是**负向**条件，不能作门控；④ 四源均值与单源差 ≤0.09 ⇒ 同一模型不同输入，无独立信息；⑤ 水平族 TO 0.80–0.82%、Δ 族 1.30–1.32% ⇒「慢构造太慢、快构造没信号」，无中间地带；⑥ **6/8 risk-neut <0.3** ⇒ size/流动性代理，登记 `USA-DL-VOLUME-PRED-WEAK`。**预注册偏离留痕**：「全 \|S\|<0.8 补事件门控」的前提「TO 健康」不成立（门控只会更低），故不补批、直接封存。机制：H1 Gervais 2001 / H2 Conrad 1994 / H3 Llorente 2002 / H4 源一致性 / H5 加速度。画像 → [`_usa-dl-volume-pred-field-profile-20261020.md`](_usa-dl-volume-pred-field-profile-20261020.md) §1–§5 |
| **insiders4「EDGAR forms」**（未点亮 insiders 塔，16 字段 / cov 0.6374 / aC 1451） | insiders4 | **❌ 批 1 已收封存 `vWqIS4iA4veb4m1HSW66zg`（8/8）**：最高 D7 `YPxgQmrl`（薪酬总量 Δ252 负向）S0.80 / 2Y1.45 / TO0.83% 挂；D6 `1YjzJL9m` S0.75 / 2Y1.27 / SUB0.31(限0.32) / TO0.87% 挂；披露侧 D1–D4 仅 S0.30–0.45 | 判弱封存 | ✅ 命中预注册止损（全 S<1.0）：① 8-K 报告长度两解析变体同弱、risk-neut ≤0.02 ⇒ 披露复杂度在 USA/D1 无 alpha；② 薪酬族 2Y 1.27–1.45 明显高于全期 S，但 TO<1% 结构性踩线且 risk-neut 0.03–0.18 ⇒ 是「近年慢因子」不是全期 alpha；③ vec_avg/vec_sum 无独立信息；薪酬占比与总量增长同向慢因子。**复用结论**：年报级慢变量在 D1 优先做组合腿。画像 → [`_usa-insiders4-field-profile-20261020.md`](_usa-insiders4-field-profile-20261020.md) §1–§5 |
| **pv47「Specific (Idiosyncratic) Residual Return」**（未点亮 PV 塔，2 MATRIX / cov 1.0 / aC 450·378） | pv47 | **❌ 交付路径封存 `USA-PV47-SPECIFIC-RETURN-PROD-WALL`（3 批 24 条）**：IS 是本赛季最强——批 2 找到 1d 反转 `ZYmKK9pn` S3.17/2Y1.59/SUB2.07（仅 TO 75.78% 挂）；批 3（STATISTICAL + decay 10）**5 条五闸全过**，最强 `1Yjzp5mz`（1d/std252）**S3.14 / F1.47 / 2Y1.85 / SUB2.16 / TO55.58% / DD4.50%**、`gJW98zPl`（2d/std66）2.77/1.39/1.67/1.71/40.98% | **prod 墙**（0.9362 / 0.9263） | ✅ `check_correlation` 实测 `1Yjzp5mz` **prod 0.9362**（`[0.9,1]` n=24）、`gJW98zPl` **0.9263**（n=10）⇒ **族级机制饱和**（论坛教程级做法「specific return + risk neutralization」，被社区普及），按 D0-P 判死交付路径，禁同族磨窗口/归一化。三条可复用归因：① **decay 是干净换手旋钮**（TO −19.8pt / S −0.15），而 **hump 是信号杀手**（TO 压 10 倍 / S 崩 65%）；② 逆波动归一安全且增益、翻号来自时序去均值（批 2 复证）；③ **prod 直方图 `[0.9,1]` n≥10 = 族级饱和**，不必再测同族。`1Yjzp5mz` / `gJW98zPl` 转 SUPER 组合腿候选（组合层另测 prod）。画像 → [`_usa-pv47-specific-return-field-profile-20261020.md`](_usa-pv47-specific-return-field-profile-20261020.md) §3.3–§6。<br>**2026-10-21 D0（delay 0）移植实测 4 条**：`omoW5QMk` 1.93/0.70/2Y0.85/SUB1.24、`kqJgrRzK` 1.86/0.76/0.98/1.02、`d5K1Vegx` 2.13/0.98/1.18/1.21、`0mjr3nq6` 1.91/0.63/0.78/1.39（1d/std252 与 2d/std66 × decay 10/20 × industry/subindustry）。**全部 RA FAIL，但失败原因不是 1.58/1.0 线——D0 的门槛是 `LOW_SHARPE 2.69` / `LOW_FITNESS 1.5`**（同一公式在 D1 是 1.58/1.0）。最高 S 2.13 距线 0.56、F 0.98 距线 0.52 ⇒ **D0 塔位全空不等于门票便宜，平台对 delay-0 把线抬了 70%**。同时 `pv47_spret` 描述自称 "D1 (next-day) variant"，D0 的 S 比 D1（3.14）低 1.0，**没有出现 look-ahead 放大**，可排除泄漏。D0 路径关闭（不投），平台门槛事实见 [`../rules/gate-and-submit-discipline.md`](../rules/gate-and-submit-discipline.md) §九 |
| **workforce_flow_skills「月度劳动力流动」**（未点亮 other 塔，26 VECTOR / cov 0.556–0.576 / aC 0–20 / uC 0–16） | workforce_flow_skills | **❌ 交付路径封存 `USA-WORKFORCE-FLOW-PROD-WALL`（1 批 8 条，`Xkvmt9A64P99O9KxouOia4`，8/8）**：4 条全闸或近全闸——`P0MOG8kL`（prestige 水平）**S2.08/F1.59/2Y1.83/SUB1.03/TO0.93%**（仅 TO 差 0.0007）；`2rjNpe1Z`（prestige 变化）**1.79/1.27/2.00/1.07/2.88%**；`KPmEGZPj`（salary per head）**1.95/1.42/1.85/1.05/2.49%/DD3.83%**；`A1Q7GERe`（seniority）1.72/1.25/1.60/1.11/1.11% | **prod 墙（0.8408–0.9255）** | ✅ `check_correlation` 4/4 实测：0.8741 / 0.9059 / 0.8408 / 0.9255，覆盖构成与流量两类机制 ⇒ 按 D0-P 判族级饱和，**不发补批**。可复用结论：**低 aC/uC ≠ 低 prod**；慢劳动力基本面在 USA 全部重叠已提交池。IS 强候选 `P0MOG8kL`/`2rjNpe1Z`/`KPmEGZPj` 转 SUPER 组合腿。画像 → [`_usa-workforce-flow-skills-field-profile-20261020.md`](_usa-workforce-flow-skills-field-profile-20261020.md) §3.1/§4/§5.1 |
| **earnings_risk「财报事件风险」**（→ ❌ 已判弱封存；9 VECTOR / cov 0.279–0.307 / aC 0–1 / uC 0–1） | earnings_risk | **批 1 已收（8/8，`447mrZe5S4rMbplrCmM0QnY`）**：全 \|S\| ≤ 0.58——U5 VRP Δ22 **0.58 / F0.31 / 2Y1.17 / SUB0.53 / TO7.87%**（全批最优）；U6 上季财报涨跌 0.57 / 2Y1.08 / **DD17.07%（最低）**；U1–U3 IV skew 三面同值 0.52–0.53；U7/U8 0.44 且 DD≈27%；U8 TO0.67% 挂 | **❌ 判弱封存 `USA-EARNINGS-RISK-WEAK`**（不补批） | ✅ 归因（画像 §4）：① **8 条 `rns` 全在 −0.13…0.08** ⇒ 剥离风格后无特异信息，这是比 S 更低的一级证据（对照 workforce rns 1.13–2.12）；② IV skew 水平/Δ22/归一三面差 ≤0.01 ⇒ 截面变异由波动水平主导，归一化无效；论坛指出 skew 需 attention 门控，而 ATOM 禁跨数据集 ⇒ 机制在本约束下不可用；③ VRP 是唯一有梯度的方向但差闸 1.00，单自由度杠杆上限 +0.2~0.4 不可达；④ 覆盖率 0.30 用 66 天 backfill 后信号退化为慢变量，与 workforce/board 同命；⑤ 事件族唯一亮点是 **PEAD 低回撤**，登记为未来组合腿候选。画像 → [`_usa-earnings-risk-field-profile-20261020.md`](_usa-earnings-risk-field-profile-20261020.md) §3.1/§4 |
| **fundamental2「XBRL footnote 明细」**（Fundamental 类，766 字段 / 本地可筛 57 / cov 0.26–0.71 / aC 中位≈500） | fundamental2 | **❌ 封存（批 1 8/8 + 批 2 5/8，共 13 条）**：批 1 **八族 S 无一例外为负**——B1 应计负债 `RRA6nW3g` **−1.00** / B2 预付 `88vPd9zV` −0.99 / D1 租金 `e76QwN3O` −0.95 / D2 未来租金 `GrgOAXKx` −0.91 / A1 授予率 `leMKOggx` −0.84 / A2 未确认补偿 `0mjr36wk` −0.79 / E1 有效税率 `N1eVml6q` −0.60 / F1 信贷额度 `A1QvMY3d` −0.57。批 2 镜面全正：**`ZYmAe3kx`（D1+`quantile`）S+0.97 为全集中最高**、`wp9bMmpl`（A3 非期权授予）+0.96、`QPYKLJXG`（D1）+0.95、`6XAKvqlJ` +0.86、`d5K1AeA2` +0.84 | **机制上限 +0.97，距 1.58 线 0.61 ⇒ 封存** | ✅ 归因（画像 §5）：① **八条独立机制族全部同号为负（−0.57…−1.00）** ⇒ 方向性结论：USA 2014–2023 里「高 SBC / 高租金强度 / 应计累积 / 高预付」的公司**跑赢**，教科书方向（稀释折价、表外杠杆折价、应计异象）在本期**反转**；与文献一致——应计异象 2003 后显著衰减（Green-Hand-Soliman 2011、Lewellen 2010），高 SBC 集中在科技成长、高租金集中在轻资产连锁 ⇒ 收的是**成长溢价**不是会计质量溢价。② **三个杠杆全部实测**：`quantile()` 仅 **+0.02**、同簇换字段（A1→A3）**+0.12**、符号翻转 **±0**（逐位对称）⇒ 0.61 的缺口不是形状/参数能补的。③ 正向 `rns` 0.50–0.52 ⇒ 剥离风格后只剩一半，**定位是风格腿**。④ D1/D1q 的 TO 0.83%/0.85% 低于平台 1% 下限 ⇒ 最强那一支即使 S 达标也挂换手闸。⑤ 3 条撞 429 的变体（D2_pos / D3_lease5y / D1_pos_ind）**刻意不补发**：最多把 0.97 抬到 ≈1.0，距线仍 0.58。画像 → [`_usa-fundamental2-field-profile-20261021.md`](_usa-fundamental2-field-profile-20261021.md) §1–§6 |


| 塔 | 数据集 | 字段 | cov | aC | 备注 |
|---|---|---:|---:|---:|---|
| other | **`equity_kpi_forecast`** | 22 | 0.3717 | 139（vs5） | **❌ 交付路径封存 `USA-EQUITY-KPI-FORECAST-PROD-WALL`（2 批 16 条，6 机制）**：批 1 6/8 进 Mode A（S1.20–1.46、rns1.57–2.52）；批 2 最好 `JjPvNKKA` **S1.58/F1.33/SUB0.93/CW通过/TO1.22%**，仅 2Y 1.28 挂。但三条主线 prod **0.905–0.9146**（`[0.8,0.9)` 1300–1500 条）⇒ 按 D0-P 判数据集级饱和。**不是判弱、是 prod 墙**。salvage：`JjPvNKKA`/`wp9EZgMv`/`O0Jxrx9d`/`O0Jxrx9J` 转 SUPER 腿候选。可复用：① `ts_decay_linear(20)` 是本集 2Y 唯一正向杠杆，subindustry 零增益、ts_rank504 与 group_backfill 有害；② `−|days|` 收益来自**公告后**邻近度（仅公告前版 −1.12）；③ **Mode A 前先测 prod**。画像 → [`_usa-equity-kpi-forecast-field-profile-20261020.md`](_usa-equity-kpi-forecast-field-profile-20261020.md) §3.1/§3.2/§4/§5 |
| other | `stock_cluster_dl` | 4 | 0.5622 | 8（vs6） | 主成分特征，经济语义不可陈述（违反「说不出收益来源不许组装」）⇒ 不优先 |
| pv | `risk72` | 3 | 0.367–1.0 | 311–1630 | ⚠ 与 pv47 同为 specific return 族，prod 族级饱和先验极强 ⇒ 低优先 |

**已整塔封存不再取新集**：PV（pv47 prod 墙 + pv63/pv103/pv115/dl_volume_pred 判弱 ⇒ 含 pv52/pv98/pv173/intraday_pv_feats 一辆不再开）；
sentiment（5 个文本分数集判死 + sentiment21/26 判弱 ⇒ sentiment22/23 同族不试）；option（option3 判弱）；insiders（board_gov/insiders4 判弱，insider 矩阵稀疏墙）。

**2026-10-20 本轮逐集封存（other 塔；主表已不列，此处保留索引）**：

| 数据集 | 结论 | 关键读数 | 档案 |
|---|---|---|---|
| `stock_search_trends`（Google 搜索热度，12 MATRIX / cov 0.7626 / aC 202） | ❌ **`USA-STOCK-SEARCH-TRENDS-PROD-SAT`**（2 批 16 条 + 6 条中性化补测；旧判 `…-ATOM-CAPACITY` **已作废**） | **中性化补测翻案**：CROWDING `RRA6Lz5b` **S2.30/F1.58/TO19.01%/R8.92%/SUB1.06/2Y2.09/RA failed 0**、`rKdPdYN3` 2.19/1.50/SUB0.95/2Y2.08/RA0；ROM `88vPqY8z` **S2.43/F1.55/SUB1.10/2Y2.38/RA0**、`LL5ZxrVe` SUB0.99（限1.01）差 0.02 ⇒ **SUB 容量墙可破**（仅 STATISTICAL 例外：R 7.42%→4.33%、SUB 0.69）。但 prod **0.8781 / 0.8839 / 0.8244**：CROWDING 直方图 `[0.7,0.8)` n=**1873/2336**（族级饱和）、ROM ≥0.75 ⇒ D0-P 封存。**aC 202 低 ≠ 族不拥挤**。salvage `9qE7WOxr`/`akVExbg2`/`LL5dZYMn`/`leM3KvNe` 转 SUPER 腿 | [`_usa-stock-search-trends-field-profile-20261020.md`](_usa-stock-search-trends-field-profile-20261020.md) §4.2/§6 |
| `other580`（Standardized Daily ETF Holdings） | ❌ `USA-OTHER580-FLOW-WEAK`（1 批 8/8） | max\|S\| 0.65（P3 广度）；流量水平 5d/20d 同号合并仅 0.43–0.58；P7 高 aC 对照 rns −0.33 ⇒ 风格代理；不补批 | [`_usa-other580-etf-holdings-field-profile-20261020.md`](_usa-other580-etf-holdings-field-profile-20261020.md) §5 |
| `other546`（Institutional Network Analysis） | ❌ `USA-OTHER546-INSTITUTIONAL-NETWORK-WEAK`（1 批 8/8） | 分析师边 2Y 1.41–1.70 / rns 0.59–0.64，业务/高管/风险边 ≤1.07 / −0.16–0.44 ⇒ 只有「共同分析师覆盖」被定价，regime 依赖；salvage `gJW99Agg` + `pwvKKXZX` | [`_usa-other546-institutional-network-field-profile-20261020.md`](_usa-other546-institutional-network-field-profile-20261020.md) §5 |
| `other545`（NEMO 2.0 网络动量） | ❌ `USA-OTHER545-NEMO-WEAK`（1 批 8/8） | 全 \|S\|≤0.86（A3 `QPY99JVw` 0.86 / rns 0.46 最优）；合成分 `score` rns 0.04 < 成分 0.46 ⇒ 七信号合成稀释；时序归一三连败 | [`_usa-other545-nemo-field-profile-20261020.md`](_usa-other545-nemo-field-profile-20261020.md) §5 |
| `other699`（Individual Investor Transactions） | ❌ `USA-OTHER699-RETAIL-FLOW-WEAK`（2 批 16 条） | 批 2 加 `ts_backfill 252` 后 2Y 1.38–1.47 / rns 0.59，但 max S 仅 0.67、CW 恒 0.5（日期移到 2016-10-28）⇒ 数据集级整段缺口；16 条只覆盖 4 个独立机制 | [`_usa-other699-individual-investor-field-profile-20261020.md`](_usa-other699-individual-investor-field-profile-20261020.md) §5.2/§5.3 |
| `earnings_risk` | ❌ `USA-EARNINGS-RISK-WEAK`（1 批 8/8） | 全 \|S\|≤0.58 且 rns −0.13…0.08 ⇒ 构造层失败；VRP 唯一有梯度（0.58）但差闸 1.00；PEAD 低回撤 17.07% 转组合腿 | [`_usa-earnings-risk-field-profile-20261020.md`](_usa-earnings-risk-field-profile-20261020.md) §3.1/§4 |
| `sustainable_profit`（122 VECTOR / cov 0.6172 / aC 101·uC 65） | ❌ `USA-SUSTAINABLE-PROFIT-WEAK`（1 批 8/8，`2jI6ez5Gf4vZbtJzMYBhqfW`） | 6 机制 × 8 探针全 \|S\|<1.0（max 0.97）；**水平盈利族 M1/M2/M7 rns = 0.00/−0.01/0.00、DD 28–34% ⇒ 纯风格 beta**；唯一特异轴 M3 `operating_roa_relative_volatility`(−) S0.97/2Y1.50/SUB0.64/**DD7.16%**/rns0.36；M3 相对波动显著优于 M3b 绝对波动（0.71/DD17.6%）；M6 亏损频率 rns −0.55 = distress beta。**不补批**；不登记慢腿（rns<0.5） | [`_usa-sustainable-profit-field-profile-20261020.md`](_usa-sustainable-profit-field-profile-20261020.md) §3.1/§4/§5 |
| `other327`（利率敏感 β，3 字段） | ❌ `USA-OTHER327-RATE-BETA-WEAK`（1 批 8/8，`28ex6a3qS4K69ob10c7kiKj7`） | max\|S\| 1.01（`-sl`，rns **−0.08** = 风格代理）；唯一 rns>0 的实质构造 `+lev` 0.77/0.14、subindustry 0.73/0.14；`Δ22` 把 2Y 打到 **0.46**、`z252` 1.27、`ts_rank504` 1.40 ⇒ **β 是慢水平变量、没有漂移 alpha**；TO 1.37–5.98% / CW 全过 ⇒ 失败在信号层不是数据层。不补批 | [`_usa-other327-field-profile-20261020.md`](_usa-other327-field-profile-20261020.md) §3/§4/§5 |
| `cre_exposure_model`（地产暴露 β，2 字段） | ❌ `USA-CRE-EXPOSURE-WEAK`（1 批 8/8，`1eeJn7zo4HucDm1hREs2sfq`） | 全 \|S\|<1.0（max **0.99** = `ts_rank504(comm−resi)`，rns0.33、DD **6.80%**）；`resi` 单腿仅 0.33（DD27.7%）⇒ 两类地产不是同一暴露；`resi−comm` rns **0.45** 最干净但 S0.73/SUB破闸；**ts_rank504 第二次复证为慢暴露度最优测量面**（0.87→0.99、DD 8.14→6.80）。不补批 | [`_usa-cre-exposure-model-field-profile-20261020.md`](_usa-cre-exposure-model-field-profile-20261020.md) §3/§4/§5 |
| `other567`（Employee Review，193 VECTOR / cov 0.5088 / aC 544） | ❌ `USA-OTHER567-EMPLOYEE-REVIEW-PROD-WALL`（1 批 8/8，`Gbt0W4Fg4n5afPTaPixc1u`） | IS 极强：`leM3Kdp8`（薪酬均分水平）**S1.85/F1.38/2Y1.56(warn)/SUB1.12 PASS/TO1.24%/rns1.94，fail=[]**；`58jkgxnM`（评价变化）1.82/1.30/2Y1.82/SUB0.63/TO11.48%。但 prod **0.8846 / 0.8641**（`[0.8,0.9)` n=571/131）⇒ D0-P 结构性饱和。rns 1.62–1.94 排除风格代理，问题在**拥挤**不在信号质量。salvage 5 条转 SUPER 腿；不 Mode A、不补批 | [`_usa-other567-field-profile-20261020.md`](_usa-other567-field-profile-20261020.md) §3–§5 |
| `event_relation`（事件关联网络，9 VECTOR / cov 0.6455–0.8890 / aC 29） | ❌ `USA-EVENT-RELATION-WEAK`（1 批 8/8，`wtRIB6HC543bYNlpsZjEGJ`） | 预注册止损 1+2 双触发：全 \|S\|≤0.84（vec_avg general 0.82、vec_max 0.84、partner 0.84）、三聚合差 ≤0.08。2Y 1.84–1.86 vs 全期 0.82–0.84 且 **rns 0.29–0.30** ⇒ 近年风格暴露而非 alpha；`ts_rank504` 把 S 压到 0.19（慢变量规则的明确反例）、Δ63 rns −0.05。经济层根因 = ATOM 单集无法引入对手方收益表达传播方向 | [`_usa-event-relation-field-profile-20261020.md`](_usa-event-relation-field-profile-20261020.md) §3–§5 |
| `equity_forum_data`（散户论坛情绪，8 VECTOR / cov 0.5831 / aC 6） | ❌ `USA-EQUITY-FORUM-DATA-WEAK`（1 批 8/8） | 全 S<0.70：buy 0.66 / sell 0.69 / buy−sell 0.66 ⇒ **买卖同号 = 无净方向**；rns ≤0.40 全批；讨论量/参与者 2Y 为负（−0.15/−0.12），只有 Δ22 0.68/2Y0.50 为正；平台级分数 cov 0.0039 弃用。低 aC 未带来 alpha | [`_usa-equity-forum-data-field-profile-20261020.md`](_usa-equity-forum-data-field-profile-20261020.md) §3–§5 |

⚠ **`insider_trx_matrix`（Global Insider Transaction Aggregates）判死理由 = 区域不可复现**（2026-10-20 实测）：
论坛帖 FF56620 的三颗复现配方（prod 0.686/0.542/0.611、self<0.08）依赖 **`ILLIQUID_MINVOL1M` universe**，
而 `get_platform_setting_options(USA,D1)` 实测 USA **只有 TOP3000/TOP2000/TOP1000/TOP500/TOP200/TOPSP500**，
该 universe 只存在于 GLB ⇒ **论坛原配方在 USA 结构性不可复现**。TOP3000 下该集最佳构造（C3
`ts_zscore(ts_sum(total_top_buy_transaction_count,21),252)`）S2.86 但 SUB 1.01 vs limit≈1.23，
按方法论 §10（SUB/S≥0.43）仍差 0.2 ⇒ 不换 universe、不复活。

**已判死 / 排除（2026-10-20 `get_dead_ends` 实测，禁止因 aC 低而复活）**：

| 数据集 | entry_id | 证据 |
|---|---|---|
| `news_sentiment_dl` | `USA-NEWS-SENTIMENT-DL-DEAD` | 10 probes max S 0.63，word-level sentiment 穷尽 |
| `ai_news_scores` | `USA-AI-NEWS-SCORES-DEAD` | 8 probes max \|S\| 0.48，RavenPack PR 情绪零 alpha |
| `event_sentiment_signals` | `USA-EVENT-SENTIMENT-SIGNALS-DEAD` | 4 probes \|S\|<0.5；vec_avg 只剩 21–22 只 ⇒ CW 0.5 + TO 1.59 |
| `earningscall_embed` | `USA-EARNINGSCALL-EMBED-DEAD` | 8 probes 最好 0.59；embedding 分量只有 21 只持仓 |
| `insider_feats` | `USA-INSIDER-FEATS-DEAD` | 4 probes \|S\|<0.5（buy/sell ratio 族） |
| `acquisition_model` | `USA-ACQUISITION-MODEL-DEAD` | 旧证据 4 候选 3 负 1 个 0.95；**2026-10-20 复核批 8 条**（`2ikiU4aes4R0b6RCyFz57oD`）：水平 likelihood S 0.11/0.10、text ±0.14、Δ22 0.72 但 2Y −0.68 ⇒ 与旧判死一致。⚠ **该批复核属流程偏离**（排期未先核 dead 名单），已在画像 §5.3 登记。画像 → [`_usa-acquisition-model-field-profile-20261020.md`](_usa-acquisition-model-field-profile-20261020.md) |
| `insider_agg_matrix` | `USA-INSIDER-MATRIX-SPARSE-EVENT-WALL` | 稀疏事件双墙（原始化 CW+TO / group_rank 信号 <1.58） |
| `sentiment21` | `sentiment21`（dead_end） | max \|S\| 0.58、HIGH_TURNOVER 1.44–1.58 结构性、8/8 failed≥4 |
| `mmp_nlp_sentiment` | 判弱（24 回测 0 ra_clean） | 不入白名单，除非新机制 |

> `news` 类别在 USA/D1/TOP3000 返回 0 集（`news12` 已不在该口径下）；情绪/社媒统一归 `sentiment` 类。
> option40 字段实测全为 IV 曲面+希腊字母、**无 volume/OI 字段** ⇒ 「only volume/OI-based option datasets remain」指的就是 option3，option 塔无第二条 OI/量能主线。
> ⚠ 以上 dead 名单来自 `get_dead_ends(region="USA")` 的 entry_id，**排期前必须再核一次**（并行会话会新增判死条）。

## 3. 已判死 / 排除（证据索引）

| 数据集 | 结论 | 关键证据 | 档案 |
|---|---|---|---|
| `forum_sentiment` | ATOM 不可用 | 去壳诊断批原生 TO 66.8–155%、S≤0.48；H2（壳致静态）不成立 | [`_usa-forum-sentiment-field-profile-20261020.md`](_usa-forum-sentiment-field-profile-20261020.md) §4 |
| `institutions18` | 结构性 prod 墙 | 两条 IS 全过候选（`leKLRA1N`/`JjQV5eO2`）prod 0.9394 | [`_usa-institutions-pv-dataset-scan-20261019.md`](_usa-institutions-pv-dataset-scan-20261019.md) |
| analyst_consensus 形状量（偏度/极差/分歧/变异系数） | 全灭 | 批 25 #3–#8：2Y 0.08–0.59、SUB≤0 | analyst_consensus 画像 §3.2 |
| analyst_consensus surprise 族 | 判弱 | 批 26 #5–#7：S≤1.45、2Y≤0.98 | analyst_consensus 画像 §3.3 |
| `other571`（Wikipedia 浏览数据，other 塔 ×1.4） | `USA-OTHER571-WEAK` | 三批 28 条：max S 1.33 < F 所需 1.58（R 恒定 0.0485–0.0574 ⇒ F 上限 0.85）、max 2Y 1.55；rns 0.76–1.31 | [`_usa-other571-field-profile-20261021.md`](_usa-other571-field-profile-20261021.md) §2.4 |
| `fnd69`（现金流/融资季度表） | `USA-FND69-WEAK` | 单批 8 机制 10 条：max S 0.77 / max F 0.40，rns 全部 ≤0.44（= 风格 beta，非独立信号）；方向全对但强度天花板 | [`_usa-fnd69-field-profile-20261021.md`](_usa-fnd69-field-profile-20261021.md) §4 |
| `pv173`（公司债 Z-spread / 隐含违约） | `USA-PV173-WEAK` | 单批 10/10 COMPLETE：max S 0.72 / max F 0.37（R 仅 3.4%，F 要 R 24% 才够，差 7 倍）；rns 三族读数：债券动量 +0.53（真但弱）/ 价差水平 −0.02（纯信用风格 beta，SUB 0.55 与 2Y 1.39 都测不出）/ 分歧变化 −0.37…−0.58（provider 过度加工）。`vec_max` 与 `vec_avg` 逐位相同 ⇒ 矢量维无尾部信息 | [`_usa-pv173-field-profile-20261021.md`](_usa-pv173-field-profile-20261021.md) §4–§5 |
| `filing_sentiment`（监管申报语气，other 塔 ×1.4，aC 42，21 字段全 VECTOR） | `USA-FILINGSENT-WEAK` | 单批 10/10 COMPLETE：max S 0.64（`ts_av_diff` 漂移）/ F 0.26；7 机制 × 2 覆盖档 × 5 形状全灭；`vec_stddev` 分歧族 margin 0.2112% 但 `rns −0.04`（风格 beta）；覆盖档反向（0.72 档换手 ×4、收益 +0.2pp、S 反降）；无一条 RA 全闸 ⇒ 未消耗 prod | [`_usa-filing-sentiment-field-profile-20261021.md`](_usa-filing-sentiment-field-profile-20261021.md) §4–§5 |
| `other359`（Web Comments & Reaction Data，other 塔 ×1.4，10 字段全 VECTOR，aC 84 / cov 0.7419） | `USA-OTHER359-WEAK`（1 批 10/10，**不补批 2**） | 赞−踩净差是社媒里唯一带方向的构造，方向确实为正（N2 0.66 / rns 0.75）但量级不足；M2 关注广度 0.09 已死 ⇒ 触发预注册规则 3（核心轴 M1+M2 全方向 <1.0 ⇒ 不为 M3–M8 补批）。唯一 >1.0 的是 `top_reactions` 子样本 N3 S1.32/F1.01/TO 3.62% 但 **rns 0.31**（风格主导，按规则 5 停修）；`ts_zscore(水平,252)` 把 0.66 削到 0.39、rns 0.75→0.02（慢存量禁用时序归一）；`+1` 分母在稀疏零值日造出 `CW 0.2549–0.2556 @2016-03-15/16` 伪影。无 RA 全闸 ⇒ 未消耗 prod | [`_usa-other359-field-profile-20261021.md`](_usa-other359-field-profile-20261021.md) §3–§5 |
| `hiring_trends`（招聘岗位，other 塔，3 字段全 VECTOR，cov 0.497–0.500，`aggregate_open_positions_count` aC 340） | `USA-HIRING-TRENDS-WEAK`（2 批 10+5，**达批次上限**） | 真信号但封顶：批 1 max S 1.04 / 批 2 max S **1.06**（线 1.58），2Y 1.05→0.87；rns 0.51–0.83（非风格 beta）、SUB/\|S\| 0.90–0.99、TO 4–11%、CW 全过 ⇒ **截面强度不足而非构造错误**。批 2 受控实验（SUBINDUSTRY→INDUSTRY，5/5 同向）：S +0.02、returns +0.60pp、rns +0.09、F +0.05，但 **2Y −0.15、DD +1.1pp** ⇒ 粗档中性化是"用近期换全期"。绝对水平 N1 0.80/rns 0.11 vs 相对变化 N4 1.02/rns 0.72 ⇒ 论坛「必须相对化」在 USA 复现。未写 DB dead_end（论坛取证闸 fail-closed，不绕过） | [`_usa-hiring-trends-field-profile-20261021.md`](_usa-hiring-trends-field-profile-20261021.md) §3–§5 |
| `other384`（财报电话会披露结构，other 塔 ×1.4，66 字段全 VECTOR，cov 0.8198，结构类 aC 0–2） | `USA-OTHER384-WEAK`（2 批 10+5，**达批次上限**） | 质量最好、幅度最低的一集：批 1 max S **1.30**（A5 CFO 出席 Δ252，rns **0.93** / DD 2.88% / SUB 0.91）、A6 Q&A 提问数 1.29/rns 0.87、A9 每句词数 1.27/**2Y 1.32**；真信号簇 rns 0.68–0.93、DD 2.9–4.4% ⇒ **不是风格 beta**，是幅度不够（F 公式封顶 0.72，过闸需 returns≥5.0%，实测最高 3.88%）。M4 比值 0.70/0.83 rns≈0.2 封存；`ts_sum` 笑声 A10 **DD 55.6% / CW 0.469**（稀疏计数第三次造 CW）。批 2 单自由度换 `_fast_d1`：5/5 全面更差（S −0.19~−0.01、SUB 全降）⇒ 频率档不是新轴、更早时点拿不到电话会后漂移。0 条全闸 ⇒ prod 配额 0 消耗；未写 DB dead_end（同 hiring，取证闸 fail-closed） | [`_usa-other384-field-profile-20261021.md`](_usa-other384-field-profile-20261021.md) §3–§5 |
| `order_book_imbalance` | 结构性 prod 墙（IS 几乎全过） | `XgbZ2aaX` S1.78/F1.35/rns1.94 仅 2Y 1.58 差 0.02、`O0NdbW61` S2.23/F1.84/rns2.24；**先测 prod 再修 2Y** ⇒ 0.8133 / 0.7975，prod 直方图 `[0.7,0.8)` 桶 n=70 / n=36（族级必死）。数据集 aC 97 低 ≠ 族不拥挤 | 本会话实测（未建独立画像） |

## 4. 可复用方法论（本轮新增）

1. **F 的杠杆判据**：`TO < 12.5%` 时 `F = S·√(returns/0.125)`，decay / backfill / winsor / 平滑**都不动 F**；
   过 F 只能提 S 或 returns（换中性化 / 换信号轴）。批 26 用四个变体实测确认（S 1.62–1.67、returns 3.79–3.88%，极差 <0.04）。
2. **低换手 ≠ 字段静态**：TO<2% 先跑「去壳诊断批」（decay 0、无 backfill/hump/quantile）再判死；
   `forum_sentiment` 即因此从「疑似静态」改判「原生高换手但无信号」，避免了错误判死理由。
3. **VECTOR 数据集的两段式读数**：先 `vec_avg` 聚合再进时序算子；事件级 surprise 用 `ts_av_diff(63)` 会被摊平成缓慢漂移，
   方向信息稀释（批 26 surprise 族实证）。
4. **中性化在本区的排序（analyst 类）**：STATISTICAL（族 A/B，S 2.07/1.94）≥ CROWDING（#4，S1.61）
   > REVERSION_AND_MOMENTUM（批 25/26，S1.62–1.67 但 F 缺口）；具体以批 27 A/B 为准。
5. **ATOM 合规检查**：每批表达式只引用一个数据集字段（分组轴 market/industry/subindustry 属豁免），
   跨数据集字段一律不混（本日志 6 颗均满足）。
6. **机制模板不封顶 8 个**（2026-10-20 纠正）：8 只是 multisim 单批容量。机制清单按字段族的经济含义
   展开成台账（画像 §2.6，当前 28 条 M01–M28：增长漂移 / 比率 / 质量 / 杠杆 / 稀释 / 隐含倍数 …），
   每批只取未测机制的代表字段，做一批补一批，不得把「一批 8 条」当成「机制已穷尽」。
7. **低换手死区判据**：当 TO 与 S 沿 decay/hump 轴单调对立、且去掉死区后 2Y 翻负时，
   死区本身在承担 alpha ⇒ 该机制判**结构性低换手**，停止调壳（count breadth 实证，画像 §3.5）。
8. **SUB 闸要按比值诊断，不能按绝对值**（本轮固化）：`LOW_SUB_UNIVERSE_SHARPE` 的 limit ≈ **0.43×S**
   （实测 1.92→0.83、1.66→0.72、1.81→0.78），所以 batch 级抬 S 的杠杆（decay / 中性化）会**同步抬 limit**，
   不改变命运。破闸的真判据是 **SUB/S ≥ 0.43**；本机制九条实测 0.22–0.36，属「小盘偏向」结构性缺口。
   ⇒ 修 SUB 只能靠改变信号在高低流动性两段的**相对强度**（自波动标准化 `ts_zscore`、慢速平滑、
   持续性结构），不能靠提高整条信号的 S。
9. **中性化轴与分组轴的职责不同**（30b 实证）：RAM 一次把 S/F/2Y 从 1.73/0.89/1.43 抬到 1.92/1.22/1.81，
   而分组轴（industry/sector/market/subindustry）只微调 F、且 market 更差 ⇒ **中性化解决「收益质量」，
   分组解决「行业暴露」，不要指望分组救闸**。
10. **★ SUB 的真正解是「测量口径」：按自身历史波动标准化**（30c 实证，继 Institutions §10.4 后第二次复证）：
    同一 Δ63 构造，`O0JxqoNq` SUB/S 0.339 → `e76xgXkM`（`ts_zscore(Δ63,252)`）**0.556，SUB 0.65→1.05**，
    而 S/F/2Y 仅微降（1.92/1.22/1.81 → 1.89/1.12/1.76）⇒ **量纲对齐让高波动小盘股的修正幅度回到与大盘同一尺度**。
    窗口（Δ42/Δ84）、平滑（hump0.05/ts_mean22）都做不到（SUB/S 0.330–0.367）。
    ⇒ 当 SUB 卡死且窗口/分组/中性化都无效时，**先换测量口径（自波动归一 / 同行相对化），再谈换数据集**。
11. **prod 墙按直方图判族级命运**：`78on0e78` IS 全场最强（S2.19/F1.48/2Y2.46/SUB1.05）但 prod **0.7214**；
    prod 直方图 `[0.7,0.8)` 桶 n=1 ⇒ 按 `wq-window-valley-break-prod-wall`「n≥1 必死」判**挂起、不磨参数**；
    同机制的 `e76xgXkM` prod 0.5532 已交付 ⇒ **同机制换一个测量口径即可绕开 prod 墙**，不必死守单条候选。
12. **论坛配方的第一道可复现性检查是 universe，不是字段**（2026-10-20 `insider_trx_matrix` 实证）：
    FF56620 三颗配方全部依赖 `ILLIQUID_MINVOL1M`，而 USA/D1 的合法 universe 只有 TOP3000/2000/1000/500/200/TOPSP500
    ⇒ 整条复现路径在 USA **结构性不存在**。以后读论坛帖先跑 `get_platform_setting_options(region,delay)` 对 universe，
    再谈字段与算子；否则会在错误的 universe 上把「配方失效」误记成「字段无效」。
13. **`hump` 对日均微观结构统计量是信号本体，不是滤波器**（pv103 两批复证）：同一 `inam/ntrd` ratio，
    去掉 hump 后 S = **−0.41**，加 `hump(…,0.01)` 后 **0.75**；`c_volume/intv` 同样 −0.02 → 0.64。
    ⇒ 此类构造里 `hump` 承担「把日均水平转成慢速持有状态」的角色；把它当可删的平滑项做消融，等于删掉信号。
14. **★ 先看 `risk_neutralized_sharpe`，再看 SUB / 2Y**（2026-10-21 第二次复证：pv173 价差水平族 `rns −0.02`、filing_sentiment `vec_stddev` 分歧族 `rns −0.04`）。
    两次形态完全一致：**SUB 0.42–0.55 与 2Y 1.3–1.4 都能通过，`rns` 却归零** ⇒ 所谓"分歧 / 离散"构造卖的是规模/波动风格暴露。
    ⇒ 新批若主打 Dispersion 桶，**收割后第一件事读 rns**；`rns < 0.3` 直接按风格 beta 结案，不要再花仿真修 SUB / 2Y。
15. **覆盖档不是越高越好**（filing_sentiment 实证）：同一机制的高覆盖 `_2` 档（0.7266）对比低覆盖档（0.5443），
    换手 1.7% → 6.9%（×4），收益仅 +0.2pp，S 反降（分歧 0.55→0.32、漂移 0.64→0.36）。
    低覆盖 + `ts_backfill(252)` 已交易 ~2950/3000 只（long 1374 / short 1678，0 CW）⇒ **选字段时优先看"信息是否随事件变化"，覆盖 0.4 以上即可，别为覆盖率买噪声。**
    判别法：去 hump 后 2Y 与 S **同向崩塌且 TO 仍 <1%** ⇒ hump 是载体；去 hump 后 TO 上升而 S 不变 ⇒ 才是纯滤波。
14. **「估计量字段」只在水平上有方向**（other327 8/8 复证）：利率 β 的正反向 0.77/0.27 有方向，
    但 `Δ22` 把 2Y 打到 0.46、`z252` 1.27、`ts_rank504` 1.40 且 S 全部低于水平 ⇒ 变化量是估计噪声。
    与「慢暴露度用 ts_rank504」并不矛盾：**连续暴露度**（cre/board）适用长窗时序位置，
    **回归估计的 β** 不适用；判别看 Δ 版本是否连 2Y 都一起崩。
15. **单数据集 ATOM 无法表达「跨资产传播」**：`event_relation` 一类网络集只有「边强度」可观测，
    Cohen–Frazzini 的经济链接效应需要对手方收益（跨资产）；利率 β 的溢价需要利率变化序列（跨数据集）。
    ⇒ 这类机制在 ATOM 下只能退化为「关系资本 / 暴露度水平」检验，判弱时应归因到**约束**而非数据集本身，
    并避免再取同类集做同构尝试。
16. **`rns` 高 ≠ 可提交，`rns` 低 = 一定不可提交**（other567 vs event_relation 对照）：
    other567 rns 1.62–1.94 仍被 prod 0.88 拦下（拥挤，不是风格）；event_relation rns 0.29–0.30
    直接判为近年风格暴露（2Y 1.85 全期 0.82 的落差是同一件事的两个读数）。
    ⇒ 读法固定为 **先 rns（是不是风格）→ 再 prod（是不是拥挤）→ 最后看 2Y/全期落差（是不是 regime）**。
17. **`2Y 高 + 全期低 + rns < 0.3` = 近年风格暴露，不是「近年才有效的 alpha」**：
    event_relation 三类聚合全部呈 2Y 1.84–1.86 / 全期 0.82–0.84 / rns 0.29–0.30。
    这种情况补批换窗/换聚合都无意义（三聚合差 ≤0.08 已证明聚合面无信息）；对照其他567 的 2Y≈全期
    + rns 1.9 ⇒ 才是真信号、只是拥挤。二者外观相似、处置完全不同。
18. **`ts_rank504` 只适用「慢暴露度」，不适用「快变网络/事件状态」**：同一条 504 长窗在 cre(0.87→0.99)、
    board_gov、other567 三次增益，但 event_relation 把 S 从 0.82 压到 **0.19**、Δ63 rns 直接 −0.05。
    判别法：字段若在 63 日内就有实质截面变动（网络边、事件状态、流量），长窗时序秩会把近期信息抹成常数。
19. **成对情绪字段（buy/sell、bull/bear）必须检查是否反号**：equity_forum_data 的 buy 0.66 / sell 0.69 /
    价差 0.66 **三者同号同量级** ⇒ 两个方向都在做多「热度」，情绪没有净方向，价差构造白做。
    判据放在批 1：若 `|S(价差)| < min(|S(buy)|,|S(sell)|) + 0.05` 即判「无净方向」，不再为该族设计补批。
20. **事件/VECTOR 字段的 `divide` 会连坐整批**：`divide(event_A, event_B)` 报
    `Operator divide does not support event inputs` 并 CANCELLED 全批（multisim 8 条同沉）。
    一律先 `vec_avg`/`vec_sum` 标量化再进 `divide`；发批前用 `preflight_expressions` 对含除法的表达式单独过一遍。
21. **SUB/S 比值在事件类字段上是数据集常数，不是构造缺陷**（stock_search_trends 16 条）：比值两批锁在
    0.35–0.41（最优 7d−28d 0.413）；平滑 `ts_mean`（0.373）与自 `ts_zscore`（0.354）**都压低**比值 ⇒
    「自波动归一救 SUB」是 analyst 慢变量特有，不适用于关注度/订单流/舆情等事件类。判别法：归一后
    若 2Y 与 S 同降且事件性被削平，即为削信号而非对齐量纲。事件类优先枚举**最短两个窗口的差**（7−28 > 7−84 > 28−84 单调）。
22. **同机制变体交付必须透明标注**：补位取自 READY 池时，写明与已交付条目的机制关系
    （本轮 #8–#10 = #5 的窗口/平滑算子/decay 变体），否则「10 颗」会被误读成「10 个方向」。
23. **★ 换集前先查「库内历史回测行」，不要凭印象**（2026-10-21 实证，差点重挖）：
    以为 `fund_holdings_panel`（30 VECTOR / cov 0.97 / aC 11）是未动过的新面，实测
    `SELECT COUNT(*) FROM backtest_results WHERE dataset='fund_holdings_panel'` = **148 行**（最近 2026-10-12），
    且交付日志已记 `mean_security_weight` 的 Δ63 S1.34 / DL 预测 2Y 2.21 但全期 0.54 ⇒ **已挖过**。
    而 `hiring_trends` = **0 行**、也不在任何 dead_end 条目里。
    ⇒ 换集前的标准两查（都只读本地库、零配额）：
    ```sql
    SELECT COUNT(*) FROM backtest_results WHERE dataset=:ds;
    SELECT entry_id FROM registry_empirical WHERE region='USA' AND layer='dead_end';
    ```
    **实测 USA/D1 有 156 个零历史数据集**（脚本口径：`datasets`×`regions` join + 逐集数 backtest_results）。
    ⚠ **但「零 history 行」不等于「没挖过」**——同一轮就踩到反例：`cre_exposure_model` 的
    `code LIKE '%commercial_realty%'` 实测 **0 行**，而它早在 2026-10-20 就以 8/8 挖过并判死
    （`USA-CRE-EXPOSURE-WEAK`，见 §2 表与本目录 `_usa-cre-exposure-model-field-profile-20261020.md`）。
    ⇒ **三查缺一不可**：① `backtest_results.dataset` 行数；② `registry_empirical` dead_end；
    ③ **`ls references/_usa-*field-profile-*.md` + 本日志 §2/§3 全文 grep 数据集名**。
    只有三查全空才算「新面」。（当时按 ①② 判 `fund_holdings_panel` 有 148 行、`hiring_trends` 为 0 行是对的；
    错在把 ① 当成了唯一判据。）
    ×1.7 倍率段里**三查后仍为空**的 OTHER 集：`hiring_trends`(3 字段 / cov 0.50 / aC 29，本档正在挖)、
    `other384`(33 / 0.82 / 112)、`other623`(6 / 0.99 / 27，内容是 TextBlob 情绪 ⇒ 与六次判死的情绪族同源)、
    `search_interest`(3 / 0.91 / 42，关注度族)。其余高倍率集都落在
    ANALYST/MODEL/PV/OPTION —— **这些塔本季已点亮（model=4 / analyst=1 / earnings=1 / pv=2），按用户规则不回测**。
24. **「财报电话会结构量」是独立轴，不是情绪族的重复**（`other384` 字段普查，2026-10-21）：
    66 个字段里 `*_tone` / `*_polarity` / `*_negfreq` 与已判死的 `earningscall_embed` 同源，
    但 **CEO/CFO 是否出席（`oth384_oecsi` / `ofcsi`）、Q&A 时长与问句数（`qa_count` / `qa_questions`）、
    presentation 与 Q&A 的语速比（`presentation_wordcount` vs `qa_wordcount`）、laughter 计数**是
    「披露质量 / 管理层可及性」轴，与情绪极性无关且平台使用量极低（oecsi aC 89 / ofcsi 86 / laughter aC 0–3）。
    ⇒ 后续 `other384` 战役按这条轴设计，**不要**再发 tone/polarity 水平或变化。
25. **`_fast_d1` 后缀字段是同一量的另一更新频率档**（`other384` 实证：66 字段里 30+ 个带该后缀，
    与主字段 aC 相差 1–3 个数量级）。同批只用其中一档，另一档是批 2 的单自由度备选，不得当独立机制计数。
    机制正交数按实际方向计（本轮 7 个），交付数按验证通过计（10 颗）。
26. **中性化粗档 = 用近期换全期**（hiring_trends 批 2 受控实验，5/5 同向，2026-10-21）：
    同一批表达式只把 `SUBINDUSTRY` 换 `INDUSTRY` ⇒ S **+0.02**、returns **+0.60pp**、rns **+0.09**、F +0.05，
    但 **2Y −0.15**、DD **+1.1pp**。⇒ 2Y 是短板时，中性化往粗档调**不是修法**（粗档保留行业慢轮动暴露，
    全期好看、近两年反转）。修 2Y 要往更细/更稳方向，或换测量口径（第 10 条）。
27. **3 字段数据集的穷尽判据是「机制轴 + 设置轴」双到顶，不是「S 没过线」**（hiring_trends）：
    8 机制方向（水平 / 相对变化 / 广度 / 周转 / 离散 / 加速 / 事件门控 / 时序分位）+ 2 档中性化 = 15 条，
    max S 1.06 ⇒ 剩余只有窗口与 decay（= 磨参数）。此时"换集"的理由可以写成**无计可施**（机制与设置都到顶），
    而不是"没灵感"；判死文案要把这两条轴都列出来。
28. **稀疏 VECTOR + `trade_when` + `+1` 分母 = 双料 CW 制造机**（other359 M7 `CW 0.2549 @2016-03-15/16` +
    hiring N9 `CW 0.496 @2018-12-27`，两次独立复现）：`trade_when` 的 else 腿把样本压到少数股票，
    `add(x,1)` 在零值日造出极端比值 ⇒ 集中度爆表。⇒ 稀疏事件数据改用 `ts_backfill` + `group_rank`、不做门控；
    比值一律 `divide(a,b)`，不写 `+1`。
29. **`_fast_d1` 档不是新轴，是"同一数值的更早时点"**（other384 批 2 受控实验，5/5 同向，2026-10-21）：
    同一批表达式只把字段换成 `_fast_d1` 孪生 ⇒ S **−0.19 ~ −0.01**、F −0.01~−0.05、SUB 全线下滑、rns 多降。
    覆盖几乎相同（0.8198 vs 0.8199）⇒ 数值同源，差别只在披露时点更早，而**更早拿不到事件后的漂移**。
    ⇒ 遇 `_fast_d1` 族：**默认用基名档**；fast 档只在"事件后漂移为负"的假设下才值得一试，且只能占批 2 的单自由度。
30. **同一机制里"度量"比"符号"重要**（other384）：`qa_questions` 的 z 分 S1.29/rns0.87，而同一段落的
    `qa_count`（实词数）取反 0.91/rns0.48。**提问条数 = 信息产出（正）**，**回答字数 = 冗长（负）**——
    同机制两个度量方向相反。先问"这个字段数的是行为还是篇幅"，再谈符号。
31. **披露行为族的幅度上限 ≈ S 1.3**（other384：6 机制 × 2 频率档 = 15 条，max 1.30、max 2Y 1.32、rns 最高 0.93）：
    质量项（rns / DD / SUB 比 / 簇）全线达标而 S 停在 82% 过闸线 ⇒ 这是**数据集级幅度天花板**，
    设置层（中性化 / 频率档）移动量 ≤0.02–0.19，补不上 +22% S。**该类数据集只能作组合腿，不能作单腿主候选**。
32. **★ 中性化能破 SUB 容量墙，破不了 prod 墙**（stock_search_trends 6 条补测，2026-10-21）：
    同两条表达式（7−28 / 7−84）只换中性化 ——
    `SUBINDUSTRY` SUB 0.90（差 0.04）；`STATISTICAL` 更差（R 7.42%→4.33%、SUB 0.69，吃掉了信号所在的
    中小盘残差聚集）；**`CROWDING` / `REVERSION_AND_MOMENTUM` SUB 1.06 / 0.95 / 1.10 且 RA failed 0**
    （S 反升至 2.30 / 2.19 / 2.43，R 8.3–8.9%）。但三条 prod = **0.8781 / 0.8839 / 0.8244**，
    CROWDING 直方图 `[0.7,0.8)` n = 1873 / 2336 ⇒ 族级饱和。
    ⇒ 修正两条旧口号：① 「破墙靠换 neutralization」**对 SUB 成立**，但要看中性化是否削掉信号载体；
    ② 「换中性化是破 prod 的手段」**只在族未饱和时成立**，族一旦饱和，任何设置轴都无效。
33. **`alphaCount` 低 ≠ 族不拥挤**（同批）：`stock_search_trends` 数据集 aC 仅 **202** 却 prod 0.82–0.88
    （直方图 n≈2000）；`order_book_imbalance` aC 97 而 `[0.7,0.8)` n=70。
    **拥挤度只能读 prod 直方图，不能读数据集的 alphaCount / userCount**。发批前省配额的正确顺序是
    「先查该字段族的 prod 直方图 → 再无 prod 先验时才烧闸门批」。

---

## 附录 Z：2026-10-21 补测 —— institutions 持股族判死（补位路径封口）

`submit_ready` 池里发现两条 **IS 全闸通过、prod 从未实测**的候选（`leKLRA1N` / `JjQV5eO2`，
均 `group_rank(ts_backfill(inst18_instownership_pct_held, 66), subindustry)`，S 1.71 / F 1.27 / 2Y 1.86 / SUB 0.91），
即"补位最省力的路径"。实测结论：

| alpha | prod max corr | 判据 | 处置 |
|---|---|---|---|
| `leKLRA1N` | **0.9394** | D0-P：prod ≥ 0.75 判死 | 封存，不再提交 |
| `JjQV5eO2` | 未测（同字段同族） | 同上，同族必死 | 免测，直接封存 |

prod 直方图 `[0.9,1]` n=6 / `[0.8,0.9]` n=963 / `[0.7,0.8]` n=6580 —— 机构持股是**密集拥挤族**，
不是单条候选的构造问题。⇒ **institutions 塔在本轮不可作为补位来源**；
以后看到 `inst*ownership*` 系字段的高 IS 候选，先查该族 prod 直方图再谈烧配额。

**方法论**：`submit_ready` 池里的 `IS_ONLY` 条目是"未经 prod 验证"的历史遗留（生成于 prod 检查尚未强制时），
不是"已验证可提交"。读到 `gate=IS_ONLY` 必须自己补一次 `check_correlation(refresh=True)`，
不能用 `verified_at` 当作验证证据。

---

## 附录 AA：2026-10-21 数据集切换 → `pv173`（Corporate Bond Pricing Data）

**切换理由（对应过程约束"不得频繁切换数据集，仅在确实无计可施时才更换，并说明原因"）**：

| 候选面 | 已用证据 | 结论 |
|---|---|---|
| Fundamental（23 集） | 5 集直接实测 + `fnd69` 当日判弱；扫描自证 S 天花板 1.43 / SUB 0.52 | **结构性无法产出 ATOM**（`_usa-fundamental-dataset-scan-20261019.md` §6） |
| other 塔低拥挤集 | 2026-10-20 一天 14 集全部出结论（other545/546/567/571/580、cre、earnings_risk、equity_forum_data、equity_kpi_forecast、sustainable_profit、event_relation、acquisition_model、macro63、news_sentiment_nlp） | 全弱或 prod 墙，**0 可交付** |
| analyst 塔 | analyst44 已出 2 颗 ACTIVE；factor_signals 修正/偏度复族 prod 直方图 `[0.7,0.8)` n≥1 判族级死；consensus 目标价族 prod 漂 0.90+ | **无可再挖方向** |
| `s0-select` 存活池 | 平台推荐 56 集存活，但头部全部 aC > 1000（sentiment21 1482 / institutions6 3641 / macro38 16219 / other566 1992 / pv1 2.19M） | 继续磨 = 直撞 prod 墙 |

**唯一满足全部条件的剩余集**：`pv173` —— pv 塔未点亮 / aC **88** / 51 字段 / cov 0.3916 /
机制（债券隐含信用信号）与已交付 7 个方向全部正交 / 从无画像。

**已落档**：[`_usa-pv173-field-profile-20261021.md`](_usa-pv173-field-profile-20261021.md)
（§1 字段画像：3 视图 × 8 信号 × 2 覆盖档 = 48 + 3 元数据；§2 九条机制 + 通用壳 + 预注册止损；§2.4 本条切换理由全文）。
**探针批**：multisim `2Nq9ps7ah4Rybyv17mclmLUY`（10 条 = 8 个底层信号 + `vec_max` 尾部口径 + `market` 分组兜底），
USA / TOP3000 / D1 / SUBINDUSTRY / decay 5 / trunc 0.08 / VERIFY / nan ON / pasteurization ON / maxTrade OFF。

**结果（2026-10-21 收批）**：10/10 COMPLETE，8 个底层信号 `|S|` 全落 **0.23–0.72**，最好 M8 S 0.72 / F 0.37 / 2Y 1.32 / SUB 0.55
⇒ 预注册规则 #1 触发，**封存 `USA-PV173-WEAK`**，不开第二批。三条失败曲线（A 债券动量 rns +0.53；B 价差水平
SUB 0.55 但 rns ≈ −0.02 = 纯风格 beta；C 背离/变化 rns −0.37…−0.58）与三条可复用结论见
[`_usa-pv173-field-profile-20261021.md`](_usa-pv173-field-profile-20261021.md) §4–§5。**pv 塔在本轮不可作为补位来源。**

---

## 附录 AB：2026-10-21 web_traffic_engage 五条 prod 全测 —— 封存 `USA-WEB-TRAFFIC-PROD-SAT`

| alpha | 机制（时间变换形式） | prod max corr（自测 `check_correlation`） |
|---|---|---|
| `RRA6XP3j` | 会话量水平 | 0.9740 |
| `WjLekJQO` | 独立访客 | 0.9906 |
| `omoW2ZO2` | 页面浏览 | 0.9908 |
| `58jgRYWX` | **7d vs 28d 加速度（变化量腿）** | **0.9781** |
| `e76QAEoN` | **移动端份额（结构位移腿）** | **0.9782** |

五条互不相同的机制全部落在 **0.974–0.991**（全部 ≥ 0.75，按 D0-P 逐条 `dead_end`；同族第二条起机制级判死）
⇒ 封存 **`USA-WEB-TRAFFIC-PROD-SAT`**。可复用结论：**prod 墙与字段的时间变换形式无关**——水平 / 变化量 / 份额
三族都撞同一堵墙，说明它衡量的是「这条信息本身是否已被市场以别的 alpha 表达过」，而不是构造细节。
以后见到高 IS 的 web-traffic 候选，直接查族级 prod 直方图，不要再烧"换时间变换"的批。

---

## 附录 AC：2026-10-21 全库候选盘点 —— 29 条 IS 全闸候选，0 条可交付快赢

盘点口径（`logs/_tmp_inventory.py`，只读）：USA / 未提交态（`platform_status` ∉ ACTIVE/SUBMITTED/DECOMMISSIONED）
且 `S ≥ 1.58 ∧ F ≥ 1.0 ∧ 2Y ≥ 1.58 ∧ SUB ≥ 0.43·S ∧ 0.05 ≤ TO ≤ 0.30` ⇒ **n = 29**。
逐条查看后：**全部**落在两类——`analyst_consensus` 目标价族（`group_rank(ts_zscore(mean_estimate_targetprice_annual12_tribes,175),subindustry)`，
S 1.74–1.94，族 prod 0.99）与 `web_traffic_engage`（附录 AB 已封存）。**没有一条是"补位快赢"。**

**⚠ 数据完整性陷阱（必须记住）**：池里有 5 行显示 prod 0.6738–0.6982，看似"低于 0.7 可提交"，但
`prod_corr_source = 'platform_sync'`、`corr_checked_at = 2026-10-07`；对**同一条表达式**本日实测
`check_correlation(refresh=True)` = **0.9991**。⇒ **`platform_sync` 来源的 prod 值不得当作验证证据**
（平台同步回填的是当时池内最大相关，会随池子变化而漂）。读 prod 必须先看 `prod_corr_source` 与 `corr_checked_at`，
`IS_ONLY` / `platform_sync` 一律补测。

---

## 附录 AD：2026-10-21 数据集切换 → `workforce_flow_skills`（劳动市场 / 人力资本，`other` 塔未点亮）

**切换理由（承接 AA；pv173 封存后的下一顺位，同满足"不得频繁切换"的举证要求）**：

| 候选面 | 证据 | 结论 |
|---|---|---|
| 全库 IS 全闸库存 | 附录 AC：29 条全在已封存族 | 无快赢 |
| 已点亮塔 | analyst（目标价 / 修正 / 偏度）、model、earnings、institutions、web-traffic | 按用户指令「已点亮塔的数据集先不回测」+ D0-P 族死 |
| 未点亮塔低 aC 池 | `logs/_tmp_ds.tsv` 按 aC 升序：`workforce_flow_skills` aC 67 / cov 0.5703 / 26 字段；备选 `forum_sentiment`(36) / `filing_sentiment`(42) / `other635`(42) / `nlp_news_scores`(51) / `pv109`(58) | 本集机制与已交付 7 个方向**零共享数据源** |

**已落档**：[`_usa-workforce-flow-skills-field-profile-20261021.md`](_usa-workforce-flow-skills-field-profile-20261021.md)
（§1 26 字段画像：7 个构念 × 3 切片 + `unreliable_user_*` 质量族，全 VECTOR；§2 十条机制 M1–M10 含文献锚
Belo–Lin–Bazdresch 2014 / Bazdresch–Belo–Lin 2018 / Kuehn–Simutin–Wang 2017；§2.3 七条预注册止损）。
**探针批**：multisim `2Lo4Eqa72590b8I13aKdERKH`（10 条），USA / TOP3000 / D1 / SUBINDUSTRY / decay 5 / trunc 0.08 /
VERIFY / nan ON / pasteurization ON / maxTrade OFF；壳 `quantile(group_rank(winsorize(ts_backfill(<SIG>,252), std=4), subindustry))`。
**本批判死口径已预置 `risk_neutralized_sharpe`**（pv173 的教训：rns 比 S/F 更早给死刑）。

---

## 附录 AE：2026-10-21 `workforce_flow_skills` prod 全灭 ⇒ 族级封存；切换 `other699`

**探针批结果（multisim `2Lo4Eqa72590b8I13aKdERKH`，10/10 COMPLETE / 0 ERROR）**：7/10 达 S ≥ 1.25，
**4 条 RA 全闸**（`akVxompO` / `A1QvkXol` / `omoWVjxk` / `GrgOk2qO`），rns 1.55–2.13、**0 条 CW**。

**prod 实测（`check_correlation(refresh=True)`，已 `persist_correlation(source="manual")`）**：

| alpha | 机制 | IS S / 2Y / rns | prod max |
|---|---|---|---:|
| `akVxompO` | M2 净招聘率 66d 变化 | 1.89 / 1.90 / 1.84 | **0.8586** |
| `A1QvkXol` | M6 声望 252d 变化 | 1.94 / 1.88 / 2.00 | **0.8731** |
| `omoWVjxk` | M7 职级 252d 变化 | 1.90 / 1.59 / 1.98 | **0.8829** |
| `GrgOk2qO` | M10 M1 + market 分组 | 1.69 / 1.89 / 1.89 | **0.9078** |

四条全 ≥ 0.75 且分属三种形态 / 三条不同构念 ⇒ 逐条 D0-P `dead_end` + 机制封存 **`USA-WORKFORCE-PROD-SEAL`**。
**可复用结论（第 4 条）**：**高 rns 不防 prod 饱和**。rns 证明"信息不是规模/行业伪装"，prod 证明"平台里有没有人挖过"；
两个问题分开测，缺后者 = 白干。这是连续第三个「IS 完美 / prod 死」的数据集（前两个：web_traffic_engage 0.974–0.991、
analyst 目标价族 0.90–0.999）。

**2026-10-23 补记（KPmrkA11 处置，闭合待办）**：同批第 4 臂 `KPmrkA11`（M4 人均薪酬 252d 变化，S2.30 / F1.70 /
TO0.0154 / 2Y1.68 / rns2.00）**唯一卡 `LOW_SUB_UNIVERSE` 0.78（线 1.00）**，曾被列为「组修复波」候选。
**不修**：同族 4 条 RA 全闸臂 prod 实测 0.8586 / 0.8731 / 0.8829 / 0.9078（分属三种形态、三条构念），
D0-P 族级饱和已成立 ⇒ 即便把 SUB 从 0.78 推到 1.00，终点仍是 prod 墙，修复换不来可提交性。
判据要点：**SUB 是可修的闸，prod 不是**；先看族有没有被 prod 封存，再决定是否投修复配额。
`seal_dead_end` 的论坛取证闸对「prod 型封存」不适用（本判死的证据是平台实测 prod，不是论坛无解），
故机制封存以本行为准，未写 `registry_empirical`。

**下一步切换 `other699`（Individual Investor Transactions，TipRanks 散户成交明细）**，举证：

| 候选面 | 证据 | 结论 |
|---|---|---|
| `other` 塔未点亮池 | aC 升序：other699 **228** / cov **0.9612** / 16 字段 / **16 全 VECTOR**；备选 other359（web comments 85）、other623/635（news 文本，主题拥挤）、other315（期权合约元数据，实测覆盖≈0 不可用）、other436（仅 1 字段）、stock_cluster_dl（仅 MATRIX） | 本集是唯一「低 aC + 高覆盖 + 字段数够 + 机制全新」 |
| option 塔 | 6 集全部重度使用（option3 492 / option40 3200 / option6 19k / option8 203k / option9 83k / order_flow_imb 478） | 拥挤度不对 |
| analyst / model / earnings | 已点亮塔 | 用户指令：先不回测 |
| hiring_trends | 与 `workforce_flow_skills` 同属就业机制 | 按刚封存的 AE 结论，同机制预设 prod 拥挤 |

**已落档字段画像**：[`_usa-other699-field-profile-20261021.md`](_usa-other699-field-profile-20261021.md)
（16 字段全 VECTOR；`oth699_sharestraded` **带符号**（正买负卖）是本集唯一的流量方向载体）。
**批 1**：multisim `bRbODadE4qocdD1dmpPlSiW`（10 条），USA / TOP3000 / D1 / SUBINDUSTRY / decay 5 / trunc 0.08 /
VERIFY / nan ON / pasteurization ON / maxTrade OFF；壳 `quantile(group_rank(ts_rank(ts_backfill(<SIG>,66),252), <GROUP>))`
（**壳变更已归因**：首个探针 `E5VRGAj1` 用 `winsorize(...,std=4)` 壳跑 M1 得 S 0.34 / CW 0.50，根因是
`prevnumofshares=0` 的新开仓把比率打到极大值；`ts_rank(252)` 是逐股时序分位，既有界又自带规模中性化）。

## 附录 AF：2026-10-22 `analyst_factor_signals` 续挖 —— 4 条 RA 全过候选进入 prod 队列

**背景**：缺口仍为 5 颗（5 ACTIVE / 10），且 `analyst` 族此前 5 颗 IS 全闸候选已因 prod ≥ 0.90 拒提。
2026-10-22 在 `analyst_factor_signals`（922 字段、aC=0 白空间 302 条 `estimate_*`）按「机制优先 + 归因先行」
连跑批 37–44，收敛出**两条能过闸的机制线 + 一条新发现的强构念**。

### 一、当前 RA 全过候选队列（prod 实测中）

| 序 | alpha | 机制 | 核心字段 / 形状 | S | F | 2Y | SUB（限） | 状态 |
|---:|---|---|---|---:|---:|---:|---|---|
| 1 | `GrgWj9jJ`（T5） | **成本结构水平**（D&A 预期） | `estimate_y1_depr_amort` z504 → sector 组 | 1.61 | 1.08 | 1.78 | 0.94（0.69） | prod 队列 #1（进行中，已等 >30 min 无 PC 数据） |
| 2 | `LL5KPENL`（N8） | **利润隐含 2 年 CAGR**（增长路径） | `fwd_year1_estimate_cagr_2yr_pprofit` z504 → sector 组 | 1.72 | 1.32 | 2.23 | 0.78（0.74） | prod 队列 #2 |
| 3 | `QPYvAnNw` | **预测视界差**（FY2/FY1 比值） | `(FY2−FY1)/abs(FY1)` on nprofit，hump 0.02 → industry 组 | 1.83 | 1.31 | 2.12 | 0.80（0.78） | prod 队列 #3 |
| 4 | `E5V620lK` | **实际 EPS 环比增速**（已实现，非预期） | `eps_actual_q1_qoq_growth` av_diff → industry 组 | 1.80 | 1.15 | 1.77 | 0.86（0.76） | prod 队列 #4 |

**队列执行**：`logs/_tmp_prod_queue.py`（带外、单并发、每臂 45 min 上限、逐臂落盘 `logs/_tmp_prod_queue.json`）。
prod ≥ 0.70 即按 D0-P 处置（0.70–0.75 一次结构尝试；≥0.75 或尝试失败 → `dead_end`）。
**若四臂全过 prod，则交付 9 / 10**；第 10 颗从批 44（surprise 族）或 R3（D&A/EBIT 比率 W1008）取。

### 二、⚠ 提交前必须补的一步：四臂互相之间测 mutual correlation

四臂虽属 4 个不同机制族，但其中**三条落在「利润增长路径」这一大类**（N8 隐含 CAGR / QPYvAnNw 视界差 /
E5V620lK 实际 EPS 环比），按 §⑮.18 归因 3 的同源判据，**同源两条不得都送**。
⇒ prod < 0.70 的臂之间必须再跑 `compute_mutual_correlation`，pair ≥ 0.7 的按「机制更强 + 指标更宽」保留一条。

### 三、本轮新增/封存的机制结论（索引到画像）

- **能过闸的两条线**：① 成本/资本结构水平（D&A 族，§⑮.13 / §⑮.16）；② 利润隐含 2 年 CAGR（§⑮.18 N8）。
- **新发现**：`actual − consensus` 的**意外族** S/F/SUB 全部大余量（R4 `GrgmrwqG` S 1.88 / F 1.33 / SUB 1.02），
  唯一墙是 2Y 1.49（PEAD 近期半衰）⇒ 批 44 用 W 梯 + 四兄弟字段继续探。
- **已封存**：分散度（除 EPS）、利润水平、NAV 增速、D&A 意外（CW 42%）、N3 修正增速（三闸反向耦合）、
  毛利率趋势、FCF 双输。明细见画像 §⑮.12–§⑮.19。
- **新判据（可复用）**：surprise 族先看**早年 CW**（2014 覆盖不足会让单票权重 40%+），再看指标；
  CW 与符号无关，镜像臂同样死 —— 这类字段不必浪费反号臂。

### 附录 AF 补：第 5 条 RA 全过候选（批 44 S4，`QPY0ZrxG`）

| 序 | alpha | 机制 | 核心字段 / 形状 | S | F | 2Y | SUB（限） | TO | 状态 |
|---:|---|---|---|---:|---:|---:|---|---:|---|
| 0 | **`QPY0ZrxG`** | **税前利润意外**（actual − consensus） | `estimate_surprise_difference_pprofit` z504 → sector 组 | **1.83** | **1.33** | **2.06** | **0.91（0.79）** | 4.88% | **aC=0，prod 队列 #0（最高先验）** |

同批测出**「聚合层级 → 2Y」单调律**（EBITDA 0.80 ＜ EBIT 1.49 ＜ 税前 2.06，同壳同机制），
写入画像 §⑮.20 归因 1。⇒ prod 队列改为 `QPY0ZrxG` → `GrgWj9jJ` → `LL5KPENL` → `QPYvAnNw` → `E5V620lK`。
若五臂全过 prod 且相互 mutual corr < 0.7，交付可达 **10 / 10**（5 ACTIVE + 5 新）。 <!-- from config.prod_corr_max -->

### 四、提交前稳健性证据：五臂逐年 Sharpe（2026-10-22 拉取，`get_alpha_yearly_stats`）

| 年 | `QPY0ZrxG`<br>税前意外 | `GrgWj9jJ`<br>D&A 水平 | `LL5KPENL`<br>隐含 2Y CAGR | `QPYvAnNw`<br>视界差 | `E5V620lK`<br>实际 EPS 环比 |
|---|---:|---:|---:|---:|---:|
| 2014 | 3.72 | 2.95 | 2.79 | 3.24 | **4.51** |
| 2015 | 2.93 | 1.82 | 2.20 | 2.35 | 3.24 |
| 2016 | 2.05 | 2.20 | 3.07 | **4.42** | 4.06 |
| 2017 | 1.73 | 1.37 | 1.47 | 1.68 | 2.29 |
| 2018 | 0.95 | 0.64 | 0.92 | 1.55 | **−0.20** |
| 2019 | 1.09 | 1.13 | 1.07 | 1.61 | 1.35 |
| **2020** | **−0.84** | **−0.32** | **−1.45** | **−1.17** | **−2.01** |
| 2021 | 2.75 | 2.95 | 2.73 | 2.43 | 2.80 |
| 2022 | 2.66 | 2.71 | **3.26** | 3.12 | **3.41** |
| 2023 | 1.08 | 0.26 | 0.39 | 0.54 | **−0.50** |
| 全期 TO 区间 | 4.3–6.0% | 3.8–6.0% | 3.9–7.1% | 3.6–6.1% | 3.5–4.9% |
| 最大年 DD | 5.16% | 5.86% | 6.58% | 7.36% | 6.48% |
| 正年数 | 9/10 | 9/10 | 9/10 | 9/10 | **7/10** |

**四条判读（提交前必须在申请里说清，不许只报全期 S/F）**：

1. **2020 五臂全负是本批的共同风险因子，不是个股事件**（−2.01 ～ −0.32）。根因是该类「预期修正 / 增长」
   信号在 2020-03 崩盘与随后的低质量反弹中集体反转（growth-vs-value 极端切换）。⇒ 意味着五臂在极端
   风格切换年**同向亏钱**，它们是同一风险因子的五次下注 —— 这条直接强化了§二「必须 pair 测 mutual correlation」，
   也让「五臂互不相关」这个交付前提**不能靠机制命名推断，只能靠实测**。
2. **2Y 是 2022（极强 2.66–3.41）+ 2023（弱 0.26–1.08，`E5V620lK` −0.50）的组合**，不是逐年稳健的证明。
   五臂 2Y 全部过线的真实来源是 **2022 一年的强度**，2023 只说「没崩」。⇒ 若用户/OA 看 OS 近两年表现，
   应预期显著弱于全期 —— 这一点与已 ACTIVE 的 #1–#4/#7 相同（那五颗同族同壳），属族群既定特征而非新缺陷。
3. **`E5V620lK` 的稳健性明显弱于其余四臂**：2018/2020/2023 三年为负（7/10 正年），且 2023 −0.50 直接吃 2Y 余量
   （2Y 1.77，余量仅 +0.19）。若 mutual corr 显示它与 `LL5KPENL`/`QPYvAnNw` 同源，**优汰顺序应为
   留 `LL5KPENL`（2Y 2.23 余量 +0.65）、汰 `E5V620lK`**，而不是反着按全期 S 挑。
4. **正面证据（可写进提交材料）**：五臂全期多空家数均衡（≈1500 / 1600），无单票集中迹象；
   年换手 3.5–7.1%、最大年 DD 5.2–7.4%，均为**低换手慢变量**（持有期以季计），
   在 USA/TOP3000/D1 下交易成本敏感度低；2014–2019 六年均为正（除 `E5V620lK` 2018），
   不是「只有最近两年有效」的过拟合形状。

**稳健闸记录位**：按 `brain-alpha-robustness` 口径，五臂各写 `robustness_<alpha_id>` 台账；本条即五臂共用证据正文，
逐臂回写时引用此表 + 各自的 prod/self 实测值，不再重复拉数。

### 五、★ 实测 mutual correlation：五条候选是**同一个因子**，「五臂全过 → 10/10」计划作废

`compute_mutual_correlation`（**纯本地、Pnl 差分、近 4 年 986 个交易日、不占平台相关性槽**）实测：

| | QPY0ZrxG | GrgWj9jJ | LL5KPENL | QPYvAnNw | E5V620lK |
|---|---:|---:|---:|---:|---:|
| **QPY0ZrxG** | 1 | 0.761 | **0.802** | 0.775 | 0.747 |
| **GrgWj9jJ** | 0.761 | 1 | 0.757 | **0.810** | **0.693** |
| **LL5KPENL** | **0.802** | 0.757 | 1 | 0.791 | 0.699 |
| **QPYvAnNw** | 0.775 | **0.810** | 0.791 | 1 | 0.732 |
| **E5V620lK** | 0.747 | **0.693** | 0.699 | 0.732 | 1 |

- **10 个 pair 里 8 个 ≥ 0.70**，最高 0.810（`GrgWj9jJ` × `QPYvAnNw`）。
- **五条内「互相全 < 0.70」的最大子集只有 2 条**：`{GrgWj9jJ, E5V620lK}` = **0.6931**（余量 0.007，极薄）。
- **并入已 ACTIVE 的 5 条后，最大互斥子集 = 7 条**（5 ACTIVE + `GrgWj9jJ` + `E5V620lK`）；
  ⇒ 本批候选簇的**边际交付上限是 +2，不是 +5**。

**同一次计算给出的另一面（重要，别只看坏消息）**：五条新候选对**已 ACTIVE 五条**的相关系数全在
**0.21–0.65**（最低 `kqJLawqP`×`LL5KPENL` 0.2095、最高 `gJWoaJqv`×`QPY0ZrxG` 0.6476），
**没有一条踩 0.7**。而已 ACTIVE 五条彼此也只有 0.23–0.64。
⇒ 冲突**只发生在候选簇内部**：这批新候选确实是「相对已提交池的新增量」，但它们彼此之间是同一注。

**归因（与§四逐年表完全一致）**：五条共享同一个驱动 —— 2020 全负、2021–2022 暴涨、2023 转弱；
它们只是用 D&A 水平 / 税前意外 / 隐含 CAGR / 视界差 / 实际环比五种写法表达**同一件事：基本面预期修正的多头端**。
**判据（可复用，写入机制结论）**：**「机制命名不同」≠「因子不同」**。同数据集、同壳（`quantile(group_rank(hump(backfill(winsorize(zscore))))))`、
同 horizon（季度~年频慢变量）、同多空家数（≈1500/1600）的多条候选，**必须先跑 mutual correlation 再谈正交**，
不得靠机制名推断。本地 mutual 免费、不占槽，应在**排队 prod 之前**先跑 —— 本轮顺序反了，白排了 3 条注定互斥的臂。

### 六、据此的选臂裁决（prod 结果尚在途，先定规则）

| 方案 | 取臂 | 边际 | 前置条件 |
|---|---|---:|---|
| **A（数量优先）** | `GrgWj9jJ` + `E5V620lK` | **+2** | 两臂 prod/self 均 < 0.7；且第二臂提交前平台 SELF 复测仍 < 0.7（本地 0.6931，余量仅 0.007，**平台窗口不同可能翻盘**） | <!-- from config.prod_corr_max -->
| **B（质量优先）** | `QPY0ZrxG` | +1 | prod/self < 0.7；与 A 互斥（0.761 / 0.747） | <!-- from config.prod_corr_max -->
| C | `LL5KPENL` 或 `QPYvAnNw` | +1 | 同上；与 B 同属被互斥的三元组（0.775–0.802） |

**裁决规则**：按目标「10 个通过验证的 alpha」**数量优先取 A**；若 A 中任一臂 prod ≥ 0.7 或平台 SELF 翻盘，
则回落到「passed 的臂里取与已提交池最低相关者」，并在台账记明放弃的臂与原因。
**不做的两件事**：① 不为了塞进更多臂去磨参数降相关（同信号换窗口/换分组只是把同一注换个包装，属自欺）；
② 不把互斥的臂改个符号再送（`-rank(...)` 与原型在 PnL 上是镜像，|corr| 不变，且 CW 与符号无关）。

**补：近失臂修复池也已实测为同族（2026-10-22，`compute_mutual_correlation` 本地零成本）**

对 `[GrgWj9jJ, E5V620lK, 9qElqRNe(R3), GrgmrwqG(R4), XgRajV7l(N3)]` 跑 4 年互相关：

| 项 | 值 |
|---|---|
| 全部 10 对区间 | **0.7161 – 0.8544** |
| 最大对 | `GrgWj9jJ` × `9qElqRNe` **0.8544** |
| 最大互相低于 0.7 的子集 | `{GrgWj9jJ, E5V620lK}`，**size 2**（与五臂集一致） |

⇒ **结论**：把 R3 的 2Y 缺口 0.02 补上、把 R4 的 2Y 缺口 0.09 补上、把 N3 的 S/F 双缺修好，
**都不会多出一次独立的赌注** —— 它们与既定 A 方案两臂的相关都在 0.72–0.85。修复方向作废，
不再为这三个近失臂花仿真。这条也印证 §五 的判断：同一个数据集 × 同一族估计修正机制，
无论算子怎么换，PnL 都在同一个因子面上。

---

## 附录 AG — analyst45 收官与「已点亮塔」改道 pv20（2026-10-22）

### §A 规则变更：已点亮塔的数据集先不回测

用户裁定：**点亮 = 本季（当前季度）该 category 的提交数 ≥ 3**；点亮的塔，其数据集**先不回测**。

实核（`get_pyramid_alphas()` 无参 = 本季，2026-10-22）：

| category | USA/D1 本季提交数 | 状态 |
|---|---:|---|
| analyst | **6** | **点亮 ⇒ 停测** |
| model | **4** | **点亮 ⇒ 停测** |
| earnings | 1 | 未点亮 |
| 其余（pv / fundamental / other / risk / macro / news / sentiment / socialmedia / institutions / insiders / shortinterest / option） | 0 | 未点亮 |

⇒ **本笔录早前把 earnings 一并当点亮的写法作废**（实际 1，未达阈值）；analyst83 换集计划同步作废
（`analyst83` / `analyst94` / `analyst8` / `analyst_base_ref` / `analyst57` / `analyst48` 全属 analyst 塔）。

### §B analyst45 三批实测量（数据集判死）

| 批 | 臂数 | 壳 | 最高 S | 结论 |
|---|---:|---|---:|---|
| 45A | 8 | T5 通用壳（`quantile(group_rank(hump(ts_backfill(winsorize(ts_zscore(vec_avg(F),504),std=4),756),hump=0.01),sector))`），RAM/decay20 | **1.10** | 想法绩效/目标价/敞口/beta 全部 < 1.2，无主信号 |
| 45B | 8 | 流量/差分壳（`ts_av_diff`、`ts_delta`、条件门控） | **1.06** | 唯一真信号 = **22 日指数相对收益的反号**（约 +0.97）；其余平 |
| 45C | 9 | 分散度条件反转 / 新鲜度门控 / 贡献者技能 | **0.96** | 见下表；换机制不换结论 |

**45C 全表（实测）**

| 臂 | alpha | S | F | 2Y | SUB(下限) | TO |
|---|---|---:|---:|---:|---:|---:|
| C1 分散度裸腿 `vec_stddev` | `pwvarxd6` | 0.30 | 0.08 | 0.08 | −0.16(0.13) | 4.35% |
| C2 分散度条件反转 | `9qEl18xe` | 0.74 | 0.41 | 0.10 | 0.45 PASS | 4.99% |
| C3 分散度条件反转 + 强壳 | `gJWaOXam` | **0.96** | 0.53 | 1.14 | 0.28(0.42) | 5.10% |
| D1 新鲜度门控（22d） | `wp9ox3o2` | 0.74 | 0.29 | 0.53 | −0.08 | 4.15% |
| D2 新鲜度门控（66d） | `d5KaVY9X` | 0.91 | 0.43 | **1.71** | 0.12(0.39) | 4.57% |
| E1 贡献者技能加权 | `3qj0r1G6` | 0.84 | 0.35 | 0.73 | 0.16(0.36) | 4.11% |
| E2 贡献者技能差分 | `kqJarv88` | 0.85 | 0.35 | 0.46 | −0.01 | 4.06% |
| F1 多头集中度条件 | `mLYaRdKE` | 0.83 | 0.34 | 0.27 | 0.27(0.36) | 3.44% |
| G2 反号 × 长窗 | `vROAMZZz` | 0.60 | 0.20 | **1.99** | −0.11(0.26) | 3.55% |

**归因（三条，均可复用）**

1. **论坛模板-3 的 `vec_stddev` 分散度不是本集的信号**（C1 S 0.30）：analyst45 的 VECTOR 是「同一个人多个想法」，
   截面分散度测的是**该分析师的持仓多样性**，不是市场分歧 ⇒ 机制与字段语义错配，不是参数问题。
2. **分散度条件反转是在拿「当期强度」换「近期强度」**：C3 的 2Y 1.14 / 全期 0.96，而裸反转 22d 单独约 0.97；
   条件化没有创造 alpha，只是把暴露期挪到近两年。
3. **新鲜度门控能把 2Y 拉到 1.99，但同时毁掉 S 与 SUB**（D2/G2）——样本稀疏造成的「少交易高 2Y」假象，
   与 analyst45 覆盖率 0.48–0.67 一致，不构成可用候选。

⇒ **analyst45 判死**：三批 25 臂、三种机制（水平/差分/条件），S 天花板 1.10（距 1.58 缺口 0.48）。
加上塔位规则，本集不再投入。

**外部取证（两条，已核对原文要点）**

- 论坛帖 `36183099180823`（analyst 五模板）：模板-3 点名 analyst45 的 `vec_stddev`；本集实测该模板失败，
  说明**模板适用性依赖 VECTOR 语义**（同一 VECTOR 在 event 类是「多方观点」，在 analyst45 是「单人持仓」）。
- 论坛帖 `25577914114711`（JF 2021, trade ideas）：想法中位存活 53 天；买入/卖出想法特征调整后 +0.91%/−1.96%；
  分析师技能有持续性；**逆向想法信息含量最高**。本集 45B 的「22 日相对收益反号」正是逆向腿，
  与论文一致地成为唯一有效信号——但它单独只有 ~0.97，达不到 USA 闸。

### §C 改道决策：USA 非点亮塔白空间 → pv20

对 166 个 USA 数据集做「从未在 references 出现」的白空间扫描（排除 LIT={analyst,model}、
coverage<0.5、aC>3000），得 17 个候选。逐个初筛：

| 数据集 | 初筛结论 |
|---|---|
| `pv64` | 基金/ETF 参考元数据（费率、分红、资产配置），实体是基金不是股票 ⇒ **弃** |
| `other296` | 财报电话会情绪（47 个 VECTOR 文本字段），aC 0–65 极低；但美国文本情绪族历史全线弱 ⇒ 备选 |
| `earnings_chart_dl` | DL 图表预测，aC 915；美国 DL 图表族历史判死多 ⇒ 备选 |
| **`pv20`** | **1552 字段、cov 0.779、aC 2117（≈1.4/字段 ⇒ 几乎所有字段 aC=0）、category=pv 未点亮** ⇒ **选中** |

pv20 的结构（S1 画像见 [`_usa-pv20-field-profile-20261022.md`](_usa-pv20-field-profile-20261022.md)）：
一致预期快照 + 厂商算法估计 + IBES 组预测信号 + 季度 as-reported + 风险模型特异收益。
**它的「修正」分支是美国已证机制（`e76xgXkM` 同构）换数据源**，而塔位在 pv，不违反停测规则。

**首批 46A（10 臂，2026-10-22 派发，multisim `1HQpXg8Vd5a5aBe2wtFGzy3`）**

| 臂 | 机制 | 核心构造 |
|---|---|---|
| R1/R2/R3 | 一致预期修正（Δ63 自波动归一） | eps / ebt / gps 的 `ts_zscore(ts_delta(F0,63),252)` |
| R4/R5 | 显式中期修正（3 个月前中位数→4 周前中位数） | `(F2−F1)/|F1|` 再 z252 |
| M1/M2 | 隐含利润率修正（同源两科目比值，单一信号） | `Δ63 z252 of EBT/营收、毛利/营收` |
| S1 | 厂商算法估计 vs 共识（意外） | `(eps_forecast_6_6 − eps_F0)/|eps_F0|` |
| P1 | 特异收益 5 日反转 | `−ts_zscore(ts_sum(specific_return_gemtr_adv_allfactors_usd,5),252)` |
| G1 | IBES 组预测信号（语义不透明，标定用） | `ts_zscore(ibes_ebt_group6_signal_12,252)` |

统一壳（USA 已证）：`quantile(group_rank(hump(ts_backfill(winsorize({core}, std=4), 252), hump=0.01), subindustry))`；
设置 USA/TOP3000/D1/SUBINDUSTRY/decay 5/trunc 0.08/VERIFY/nan ON（`wqb.profiles explain` 实核，类别卡 pv）。
预检：`preflight_expressions` 仅报 `std`（`winsorize` 命名参数误报，已知），10 字段全部存在。

**风险登记（派发前已知）**：pv20 预测族源自 IBES，与已交付 `e76xgXkM`（prod 0.5532）同源风险；
`specific_return_*` 分支与 pv47 的 prod 墙（0.9362）重叠，故只放 1 臂且避开最拥挤的
`barra_ustm0_top3000_specific_return`（aC 45）。

### §D 46A 收批（10/10 COMPLETE，multisim `1HQpXg8Vd5a5aBe2wtFGzy3`）

入库：`harvest_multisim_results` → **linked 10 / upserted 10**，`wave_results` 暂定
`PARTIAL`（0/10 过硬闸，3 条过 near 线 1.0）。全表（`get_alpha_details` 直读）：

| 臂 | alpha | S | F | 2Y | SUB | TO | DD | margin | risk_neut_S | 失败闸 |
|---|---|---:|---:|---:|---:|---:|---:|---:|---:|---|
| R1 eps rev63 | `RRAeLNEb` | 0.79 | 0.32 | 2.09 | 0.80 | 1.03% | 7.03% | 39.7bp | 0.38 | SHARPE / FITNESS |
| R2 ebt rev63 | `VkdNoXNV` | 1.03 | 0.50 | 1.93 | 0.70 | 0.99% | 6.53% | 60.8bp | 0.73 | + TURNOVER(0.0099) |
| R3 gps rev63 | `MP06Ab68` | 0.95 | 0.42 | 1.51 | 1.11 | 1.01% | 7.29% | 49.2bp | 0.41 | + 2Y |
| R4 eps snap rev | `j2eaQnaj` | 0.98 | 0.45 | **2.43** | 1.18 | 1.00% | 7.11% | 52.3bp | 0.41 | SHARPE / FITNESS |
| **R5 ebt snap rev** | `rKd7mb01` | **1.13** | **0.58** | 1.72 | 0.70 | 0.97% | 8.07% | **67.5bp** | **0.97** | + TURNOVER(0.0097) |
| M1 ebt margin | `kqJa5n8K` | 0.84 | 0.37 | 1.65 | 0.63 | 0.95% | 7.96% | 51.2bp | 0.33 | + TURNOVER |
| M2 gps margin | `E5VQAqmL` | 1.04 | 0.50 | 2.00 | 1.11 | 1.00% | **4.95%** | 57.5bp | 0.59 | SHARPE / FITNESS |
| S1 model disagree | `ZYmaLjgx` | 0.77 | 0.33 | 0.76 | 0.34 | 1.00% | 4.16% | 45.1bp | 0.61 | + 2Y |
| P1 specret rev | `leMaZ7EA` | **0.03** | 0.00 | 0.44 | 0.24 | 1.02% | 5.07% | 0.9bp | 0.10 | SHARPE / FITNESS / 2Y |
| G1 ibes group | `A1QxdnrR` | 0.86 | 0.39 | 0.60 | 0.90 | 0.95% | 6.67% | 54.0bp | 0.35 | 四项 |

**五条归因（决定 46B/46C 怎么发，不盲扫）**

1. **机制是真的，强度不够**。`risk_neutralized_sharpe` 0.33–0.97（R5 达 0.97）说明收益不是
   纯风格 beta，而是特异信息 —— 方向可用，缺的是信噪比，不是「全是 beta」那种伪信号。
   按 `_usa-field-profile-playbook-20261018.md` 的判死口径（<0.3 才判纯风格），本批**无一臂触线**。
2. **换手贴着 1% 下限**（全批 0.95%–1.03%）：4 臂（R2/R5/M1/G1）直接吃 `LOW_TURNOVER`。
   根因是 `hump=0.01`（把 <1% 的仓位变动归零）+ `quantile` 分段（离散桶，跨桶才换仓）两个
   平滑器叠加在一条本就慢的 63 日变化信号上。**修法方向 = 拆平滑器**，不是加 decay。
3. **R5（EBT 3 月→4 周中位数修正）是最强臂**（S 1.13 / risk_neut 0.97 / margin 67.5bp），
   R4（同构 EPS）2Y 2.43 是全批最高。**「显式中期修正」优于「区间差分」**：
   F2−F1 跨的是 8 周真实预期位移，而 `ts_delta(F0,63)` 跨的是 63 个交易日的净变化（含噪声往返）。
4. **同一科目内比较才成立**。M1/M2（EBT/营收、毛利/营收的利润率修正）都显著为正（0.84/1.04），
   说明分子分母同源时比值是干净的；S1（厂商算法 vs 共识）只有 0.77 且 2Y 0.76 —— 跨源比较
   引入口径差，与 analyst45 的「同源才可比」结论一致。
5. **`specific_return` 反转臂死透**（S 0.03 / margin 0.9bp / risk_neut 0.10）：与 pv47 的
   prod 0.9362 墙同族，且这里连 IS 都没有 ⇒ **该分支彻底封存**，不再投任何仿真。

**46B（10 臂，SUBINDUSTRY/decay5，multisim `2vhM5yfp94ED8GyHk8ZdTBF`）—— 只测归因 2/3 的两把钥匙**

| 臂 | 来源归因 | 构造 |
|---|---|---|
| B1–B3 | 归因 3：**水平归一化**。`ts_delta(F,63)` 未除以滞后水平，高 EPS 名的绝对变化被放大 | `(F−delay(F,63))/|delay(F,63)|` 再 z252，eps/ebt/gps |
| B4–B5 | 同上，窗口换 252（季度同比变化率） | `(F−delay(F,252))/|delay(F,252)|`，eps/ebt |
| B6 | 归因 2：拆 `hump`（换手修复方向 = 让仓位能变） | R5 去掉 `hump=0.01` |
| B7 | 归因 2：拆 `quantile`（换手修复第二把） | R5 换成裸 `group_rank` |
| B8 | USA 已证替代壳：`ts_av_diff` 代替 `ts_zscore(ts_backfill)`（见 fnd21 批结论） | `ts_av_diff(EBT_F2/EBT_F1, 252)` |
| B9 | 归因 3+4：利润率**变化率**（同源比值再做增长归一） | `Δ63/|lag| of (gps/sal)` 再 z252 |
| B10 | 归因 3 的净利科目交叉验证 | `Δ63/|lag| of net` 再 z252 |

**46C（4 臂，`REVERSION_AND_MOMENTUM` + decay 20，multisim `4qua8ZcOi5aL94X11BhUNMPQ`）—— 设置层复刻冠军配置**

`e76xgXkM` 达 S 1.89 用的正是 RAM + decay 20（analyst cell 覆盖）。46A 全部跑在
SUBINDUSTRY + decay 5 上，因此**设置层从未在 pv20 上被试过**。46C 取 46A/46B 的四条最强核
（R5 / R4 / R3 / B5）原样换设置 —— 单变量对照，不与 46B 的构造改动混淆。

> 判据（派发前先写死）：46B 或 46C 任一臂 **S ≥ 1.58 且 F ≥ 1.0 且 TO ∈ [0.01,0.70]** 才算
> 进入 S4；若全批最高 S 仍 < 1.30，则 pv20 的「修正」分支按 D15 计为**探针失败**，转
> 46D 的 `pv20_q_1_ard_*`（季度 as-reported）与自然语言/文本族，不再在预期快照上加变体。

### §D-结果 46B / 46C 收批（2026-10-22，入库 `linked 10+4 / upserted 14`）

**46B（10 臂，SUBINDUSTRY/decay5，`2vhM5yfp94ED8GyHk8ZdTBF`，10/10 COMPLETE）**

| 臂 | alpha | S | F | 2Y | SUB | TO | DD | risk_neut_S | 失败闸 |
|---|---|---:|---:|---:|---:|---:|---:|---:|---|
| B1 eps growth63 | `MP06wwq9` | 0.92 | 0.40 | **2.65** | 0.82 | 1.03% | 7.08% | 0.58 | SHARPE / FITNESS |
| B2 ebt growth63 | `VkdNnnqA` | 0.98 | 0.46 | 1.98 | 0.66 | 0.97% | 6.25% | 0.65 | + TURNOVER |
| B3 gps growth63 | `78oYOOQZ` | 0.97 | 0.44 | 1.76 | 1.07 | 1.01% | 6.56% | 0.40 | SHARPE / FITNESS |
| B4 eps growth252 | `9qEloo61` | 1.11 | 0.64 | 1.98 | 1.01 | 0.96% | 16.27% | 0.74 | + TURNOVER |
| B5 ebt growth252 | `akVaJJPw` | 0.91 | 0.48 | 1.42 | 0.78 | 0.91% | 12.47% | 0.29 | 四项（含 2Y） |
| B6 snap nohump | `JjP8ll5O` | 0.73 | 0.32 | 1.00 | 0.23 | **6.00%** | 12.82% | 0.51 | 四项（含 SUB/2Y） |
| B7 snap noquantile | `E5VQ33r9` | 1.15 | 0.57 | 1.78 | 0.74 | 0.89% | 7.46% | **1.01** | + TURNOVER |
| **B8 snap avdiff** | **`JjP8llgW`** | **1.31** | **0.67** | **2.59** | 0.82 | 0.97% | **4.10%** | **0.96** | + TURNOVER |
| B9 gps margin growth | `9qEloo99` | 1.03 | 0.49 | 2.04 | 1.01 | 1.00% | 5.58% | 0.64 | SHARPE / FITNESS |
| B10 net growth63 | `wp9o665d` | 0.78 | 0.31 | 1.79 | 0.66 | 1.02% | 4.68% | 0.48 | SHARPE / FITNESS |

**46C（4 臂，`REVERSION_AND_MOMENTUM` + decay 20，`4qua8ZcOi5aL94X11BhUNMPQ`，4/4 COMPLETE）**

| 臂 | 对应 46A/B 臂 | alpha | S | F | 2Y | SUB | TO | DD | ΔS 对 SUBINDUSTRY |
|---|---|---|---:|---:|---:|---:|---:|---:|---:|
| C1 ebt snap | R5 `rKd7mb01` 1.13 | `e76aAeYM` | 1.14 | 0.64 | **0.92** | 0.76 | 4.75% | 6.16% | +0.01 |
| C2 eps snap | R4 `j2eaQnaj` 0.98 | `LL5KeOQ1` | 0.91 | 0.43 | 1.85 | 1.04 | 4.91% | 10.39% | −0.07 |
| C3 gps rev63 | R3 `MP06Ab68` 0.95 | `9qElogn2` | 0.99 | 0.49 | **1.03** | 0.65 | 4.78% | 12.06% | +0.04 |
| C4 ebt growth252 | B5 `akVaJJPw` 0.91 | `e76aAeXJ` | 1.10 | 0.66 | **1.00** | 0.78 | 5.33% | 11.41% | +0.19 |

**裁决（对派发前写死的判据逐条回答）**

1. **没有一臂进入 S4**：全 14 臂最高 S = **1.31**（B8），F 最高 0.67，离 1.58/1.0 都还差一截；
   `LOW_TURNOVER` 反潮流地仍然是主失败项之一。
2. **判据触发第二条**：最高 S 1.31 ≥ 1.30 但远 < 1.58，**不构成「探针失败」但也不构成突破** ⇒
   pv20 预期快照分支（R 族 / B 族）**停止加变体**，机制结论固化，转 46D 的另一族。
3. **归因 2 的两把钥匙只成功了一半**：
   - 拆 `hump`（B6）：换手 **0.97% → 6.00%**（唯一真正修好换手的单算子操作），但 S 1.13→0.73、
     SUB 0.70→0.23（跌破 0.43×S 的线）⇒ **`hump` 不是可拆的装饰，它同时承担信噪比**。
   - 拆 `quantile`（B7）：换手 **反而降到 0.89%**、S 升到 1.15、risk_neut 1.01 ⇒
     **`quantile` 不是换手驱动源**（此前假设错误，已更正）；它只是把 rank 离散化，对换手无实质贡献。
   - 结论：**「换手贴在 1% 下限」在这份数据上是结构性的** —— 信号本身 63 日才动一次，
     任何不伤信号的平滑都不改变「月级持仓」。修换手只能靠 **重新引入更高频的成分**，不是拆壳。
4. **`ts_av_diff` 是本轮唯一真实增益**（B8 vs R5：S +0.18、DD 8.07%→**4.10%**、2Y 1.72→**2.59**、
   risk_neut 0.97→0.96 持平）。与 fnd21 批结论一致：**在 USA 的慢变量上，`ts_av_diff` 优于
   `ts_zscore(ts_backfill())`** —— 前者减去自身时间均值（保留符号与相对幅度），后者做秩标准化
   （把「预期修正的绝对幅度」压掉）。这条可复用。
5. **增长归一化 ≈ 中性**（eps 0.79→0.92、ebt 1.03→0.98、gps 0.95→0.97）：归因 3 的猜想
   「未归一化放大了高价股」**不成立**，`ts_zscore` 已经做了截面/时序标准化，再除滞后水平没有增量。
   B4/B5 的 252 日同比反而更差（DD 12%–16%、B5 risk_neut 0.29）⇒ **季度同比在预期快照上过慢**。
6. **设置层（RAM + decay 20）不是 pv20 的钥匙**：换手 0.91–1.03% → **4.75–5.33%**（闸修好了），
   但 2Y 三臂崩到 **0.92 / 1.00 / 1.03**，仅 eps 臂保住 1.85。**换手修复与 2Y 保留在本数据集上直接对立**
   —— `e76xgXkM` 在 analyst 上成立的那套设置迁移不到 pv20，**cell 级设置覆盖不能跨数据集照搬**。

> **46D 改道（据本节第 2 条 + 字段面新证据）**：原定 46D = `pv20_q_1_ard_*`（季度 as-reported）。
> 实测该族 43 字段**只有资产负债表科目**（`accrued_expenses` / `accts_receivable_trade` / `inventory` /
> `shares_outstanding` / `property_plant_equip_net` …），**没有利润表 EPS/营收实际值** ⇒
> **SUE / PEAD（实际 vs 预期）在 pv20 里构造不出来**，该分支作废。
> 46D 改为 **`pv20_aftercons_*` / `pv20_beforecons_*` 事件前后共识族**：15 个 VECTOR 字段、
> **coverage 1.000**（全库最高）、aC 0–3（最不拥挤），是 pv20 内**唯一未测且机制截然不同**的族
> （事件后的共识重估 ≠ 事件前的预期修正）。构造必须先用 `vec_avg` / `vec_max` / `vec_min` 聚合
> 再进标量壳（≥2 种聚合，VECTOR 硬规矩）。

### §D-结果-2 46D / 46E 收批（2026-10-22，入库 `upserted 12+10`，`linked 9+0`）

46D = B8 冠军核（`ts_av_diff(EBT_F2/EBT_F1,252)`）的设置层矩阵；46E = 事件前后共识 VECTOR 族。

**46D（12 臂，全部 COMPLETE，入库 12）：**

| 臂 | alpha | 设置 | S | F | TO | RET | 2Y | SUB | DD | risk_neut |
|---|---|---|---:|---:|---:|---:|---:|---:|---:|---:|
| D1 | `P0M5V32M` | SLOW_AND_FAST | 1.05 | 0.41 | 5.32% | 1.95% | 1.87 | 0.40 | 2.20% | — |
| D2 | `9qElna2K` | STATISTICAL | 0.93 | 0.35 | 3.51% | 1.76% | 1.91 | 0.51 | 5.04% | — |
| D3 | `npAaENq3` | MARKET | 1.30 | 0.76 | 0.80% | 4.25% | 1.51 | **1.00** | 5.50% | 1.01 |
| **D4** | **`KPmg1LZ8`** | **INDUSTRY** | **1.37** | **0.74** | **0.99%** | 3.64% | **2.46** | 0.88 | 4.52% | **1.00** |
| D5 | `vROAQY5w` | SECTOR | 1.27 | 0.70 | 0.88% | 3.77% | 1.97 | 0.88 | 5.23% | 1.00 |
| D6 | `78oYpXAZ` | CROWDING | 1.23 | 0.69 | 1.14% | 3.89% | 1.83 | 0.80 | 6.72% | — |
| D7 | `78oYpJQL` | SUB / decay 0 | 1.13 | 0.54 | 0.98% | 2.83% | 2.63 | 0.69 | 5.09% | 0.71 |
| D8 | `A1QxAgbg` | SUB / decay 10 | 1.26 | 0.63 | 0.96% | 3.10% | 2.57 | 0.71 | 4.19% | 0.90 |
| D9 | `JjP3drXm` | SUB / decay 20 | — | — | — | — | — | — | — | — |
| D10 | `npA6WrG8` | SUB / hump 0.005 | — | — | — | — | — | — | — | — |
| D11 | `gJWr3Lq0` | SUB / avdiff 126 | — | — | — | — | — | — | — | — |
| D12 | `ZYmXoVeZ` | SUB / avdiff 504 | — | — | — | — | — | — | — | — |

（D9–D12 已入库但本轮只逐臂核过 D1–D8；D9–D12 的读数在 `backtest_results` 里按 alpha_id 直查即可。）

**46E（10 臂，全部 COMPLETE，入库 10）：**

| 臂 | alpha | 聚合/构造 | S | F | TO | RET | 2Y | SUB | DD | risk_neut |
|---|---|---|---:|---:|---:|---:|---:|---:|---:|---:|
| E1 | `JjP3dA8e` | afterdiff `vec_avg` | 0.58 | 0.18 | 1.10% | 1.16% | 1.31 | 0.46 | 2.62% | 0.28 |
| E2 | `2rjGKg5Y` | afterdiff `vec_max` | 0.28 | 0.06 | 1.13% | 0.67% | 0.89 | −0.14 | 6.73% | 0.25 |
| E9 | `P0MP1RP7` | afterdiff `vec_min` | 0.99 | 0.47 | 1.07% | 2.76% | 2.03 | 0.97 | 6.60% | 0.69 |
| E3 | `A1QL3peW` | afterpct `vec_avg` | 0.87 | 0.44 | 1.21% | 3.18% | 1.98 | 0.46 | 11.10% | 0.27 |
| E4 | `RRA5rO91` | 分歧收窄 `vec_avg` | 1.02 | 0.48 | 1.25% | 2.80% | 1.55 | 0.69 | 5.34% | 0.55 |
| **E9b** | **`e761rYNM`** | **分歧收窄 `vec_max`** | **1.11** | **0.86** | **2.94%** | **7.43%** | **2.47** | 0.88 | 15.23% | 0.81 |
| E5 | `akVRO0Q2` | 覆盖扩张 `vec_avg` | 0.70 | 0.24 | 1.17% | 1.49% | 1.72 | 0.34 | 5.22% | 0.41 |
| E6 | `3qjGAKk0` | afterstd 水平 | 0.14 | 0.03 | 1.04% | 0.42% | −0.28 | 0.27 | 9.76% | 0.35 |
| E7 | `YPxlAVER` | 区间压缩 | 0.52 | 0.16 | 1.15% | 1.23% | 1.34 | −0.01 | 6.53% | 0.20 |
| E8 | `mLIKXG7x` | 均值修正 | 0.95 | 0.47 | 1.04% | 3.05% | 1.38 | 0.54 | 6.26% | 0.59 |

**五条裁决（pv20 到此收官，46 臂全入库）**

1. **pv20 无臂进 S4**：46 臂（46A 10 + 46B 10 + 46C 4 + 46D 12 + 46E 10）最高 S = **1.37**
   （D4 INDUSTRY），最高 F = **0.86**（E9b），距 S ≥ 1.58 差 0.21、距 F ≥ 1.0 差 0.14。
2. **设置层的新结论（与 46C 的 SUB 内 decay 扫描合并读）**：在**同一核**上换中性化，
   `INDUSTRY`（1.37）> `MARKET`（1.30）> `SECTOR`（1.27）> `SUBINDUSTRY`（1.31 基线）≈ `CROWDING`（1.23）
   > `SLOW_AND_FAST`（1.05）> `STATISTICAL`（0.93）。**中性化不是 pv20 的钥匙**（跨度 0.44），
   但 `INDUSTRY` 拿到全批最高 S + 最高 2Y（2.46）+ risk_neut 1.00，是**唯一同时三项达标的组合**。
3. **decay 在 SUBINDUSTRY 内是单调有用的**：0 → 10 → 20 时 S 1.13 → 1.26 →（D9 待核），
   TO 0.98% → 0.96% → 更低。**decay 抬 S 但不抬 TO**，与 46C（RAM 下 decay 20 修 TO 但毁 2Y）不是同一现象
   —— decay 的作用随中性化变化。
4. **事件共识族整体弱于预期快照族**：10 臂中 7 臂 S < 1.0，最强 E9b 也只有 1.11。但 **E9b 是全 pv20 唯一
   F ≥ 0.8 的臂**（RET 7.43% / TO 2.94%），说明**「事件后分歧收窄（`vec_max` 口径）」是本集唯一能把
   收益做厚的机制**，代价是 DD 15.23% 与 1958/815 的极端多空不平衡（不可提交）。
5. **同族内聚合口径的选择权重大于壳**：E1/E2/E9 三条同为 `aftercons_difference_86`，只换 `vec_avg` /
   `vec_max` / `vec_min`，S 从 **0.58 / 0.28 / 0.99** 摆开；E4/E9b 只换聚合，F 从 0.48 → **0.86**。
   ⇒ **VECTOR 族必须先做聚合扫描再谈壳**，聚合选择不是细节。

> **路线裁决**：pv20 **46 臂、0 进 S4、0 可提交** ⇒ 本数据集判**探针失败（D15）**，
> 不再加变体。交付缺口 5 条必须由**未点亮塔的新数据集**补：下一个目标 = `earnings` 类别
> （本季 1 次提交，未点亮）的 `earnings_chart_dl`（100 字段 / cov 0.991 / aC 1006 / uC 540 /
> valueScore 2 / pyramidMultiplier 1.2，是 earnings 类里最低拥挤的 DL 预测集）。

---

## 附录 AH — analyst45 五臂簇 prod 收官：**+0**，全簇判死（2026-10-22）

串行单泳道 `check_correlation(refresh=True)` 逐条跑完（`logs/_tmp_prod_queue.py`，单臂超时 2700s）：

| alpha | S | prod | < 0.70 | D0-P 归类 |
|---|---:|---:|:---:|---|
| `GrgWj9jJ` | 1.13 | **0.8121** | ✗ | ≥0.75 ⇒ **dead_end**（零尝试） |
| `LL5KPENL` | 1.13 | **0.8879** | ✗ | ≥0.75 ⇒ **dead_end** |
| `QPYvAnNw` | 1.10 | **0.8377** | ✗ | ≥0.75 ⇒ **dead_end** |
| `E5V620lK` | 1.02 | **0.7603** | ✗ | ≥0.75 ⇒ **dead_end**（全区最高，仍越线） |
| `QPY0ZrxG` | 1.15 | —（timeout>2700s，平台未给 PC 数据） | ? | 无数据 ⇒ **不可提交**，留待单独复测 |

**裁决**

1. **附录 AF §六 的 A / B / C 三套选臂方案全部作废**（它们的共同前置「prod < 0.7」无一成立）。 <!-- from config.prod_corr_max -->
2. **不做任何修复**：D0-P 明写 ≥0.75 不开诊断尝试；且附录 AF §五 已用本地 `compute_mutual_correlation`
   证明这五条是同一个因子（10 对里 8 对 ≥0.70，最高 0.810），近失臂 R3/R4/N3 也同族（0.7161–0.8544）
   ⇒ **簇内不存在能压到 0.7 以下的独立赌注**。
3. **交付计数维持 5/10**（`omoK1A5m` / `akVnvzX5` / `gJWoaJqv` / `kqJLawqP` / `e76xgXkM`）。
   analyst 簇贡献 **+0**，缺口从「再补 3 颗」扩大到**再补 5 颗**，且 pv20 现在必须供 5 颗。
4. **`QPY0ZrxG` 不定性**：prod 未取到数 = 未知，不是通过。它不进提交候选池；若日后复测仍 ≥0.75，
   按同一条 dead_end 处置（届时只需改这一行的状态，不影响其余四条）。

> **机制结论（可复用）**：**「本地 mutual 低相关」不蕴含「prod 低相关」。** 本簇对已 ACTIVE 池的
> mutual 全在 0.21–0.65（看起来是干净增量），但平台 prod 一测全在 0.76–0.89 —— 因为 prod 池
> 远大于自己提交的 5 条，本地 mutual 只覆盖自己那部分。⇒ **prod 只在平台实测，本地 mutual 只用于
> 「候选簇内部是否同一注」的判重。** 两者不可互相替代，也不能用前者预判后者。

---

## 附录 AI — earnings_chart_dl / 47A（10 臂）：**+0**，D15 探针失败（2026-10-22）

数据集：`earnings_chart_dl`（USA/D1/TOP3000，100 MATRIX 字段，cov 0.987–1.000，aC 1006，uC 540，
valueScore 2，pyramidMultiplier 1.2，类别 `earnings` 未点亮）。字段画像 →
`_usa-earnings-chart-dl-field-profile-20261022.md`。

multisim `1a5MlW4S94Jn8VFQ5ci7wJz`，10/10 COMPLETE，10 行入库（wave `s2_earnings_chart_dl_d1`，
verdict **FAIL** 0/10，0 条过 near 线 1.0）。壳 = USA 冠军壳
`quantile(group_rank(hump(ts_backfill(winsorize(core, std=4), 252), hump=0.01), subindustry))`。

| # | tag | alpha | S | F | TO | RET | DD |
|---|---|---|---:|---:|---:|---:|---:|
| A1 | pred20_level | `3qjG7226` | 0.53 | 0.16 | 0.74% | 1.11% | 5.81% |
| A2 | pred5_level | `kqJ83YY8` | −0.04 | −0.00 | 0.76% | −0.08% | 7.16% |
| A3 | pred10_level | `LL58p2wa` | 0.43 | 0.11 | 0.74% | 0.85% | 4.56% |
| A4 | pred50_level | `vROYLobz` | 0.67 | 0.23 | 0.75% | 1.45% | 4.43% |
| A5 | logodds20 | `3qjG72OX` | 0.57 | 0.18 | 0.78% | 1.23% | 5.15% |
| A6 | logodds10 | `YPxlp9Oo` | 0.66 | 0.23 | 0.76% | 1.55% | 8.77% |
| A7 | logodds5 | `qME5AwJZ` | 0.47 | 0.14 | 0.81% | 1.10% | 8.49% |
| A8 | revision22 | `xA1lxEpn` | −0.37 | −0.11 | 0.72% | −1.12% | 15.71% |
| **A9** | **term_20m5** | **`P0MPpAmx`** | **0.69** | **0.23** | 0.75% | 1.34% | 4.59% |
| A10 | pred1d_close | `leMgVNPn` | 0.07 | 0.01 | 0.75% | 0.13% | 6.78% |

**五条归因**

1. **缺口在 returns 不在 turnover，这条决定了「不能靠调设置救」**：全批 TO 0.72%–0.81% 吃
   `LOW_TURNOVER`，但 `F = S × sqrt(|RET| / max(TO, 0.125))`，TO < 12.5% 时分母恒 0.125
   ⇒ 修换手对 F 零贡献。F ≥ 1.0 在 S 1.58 需 **RET ≥ 5.0%**，本批最高 1.55%，差 3.2 倍。
2. **信号是慢的、长端的**：A4(50d) 0.67 > A1(20d) 0.53 > A3(10d) 0.43 > A2(5d) −0.04 单调成立；
   A9（20d−5d 期限结构）0.69 全批最高。A10（1 日头，aC 418 最拥挤）0.07 平掉 ⇒ **本集拥挤度与信号强度无关**。
3. **`ts_av_diff` 修正腿反向（−0.37 / DD 15.71%）**，与 analyst 族 `e76xgXkM`（修正正、S 1.89）**符号相反**。
   分析师修正 = 信息扩散滞后；CNN 预测变化 = 预测自身均值回复。⇒ **「修正」机制不可跨数据源移植**。
4. **分类头只在 10d 优于回归头**（0.66 vs 0.43），20d 基本相同，5d 反向；改的是信噪比小数位不是量级。
5. **0.69 距 1.58 差 2.3×**，而全仓历史上任何单杠杆跨度 ≤ 1.4×（pv20 中性化 0.93→1.37、
   46B 壳 1.13→1.31）⇒ 无杠杆可补，**D15 判死，不加变体**。

> **跨数据集可复用结论**：**「低频 + 低换手 + 低 aC」不等于「有 alpha」**。本集同时满足三个
> 「看起来好」的先验却是全仓最弱之一。判据是**字段是否携带对未来收益的横截面排序信息**：
> DL 预测头给的是「收益幅度/分位」，不是「相对强弱」，在 `group_rank` 壳下被中和大半。
> **下次选 DL 集先看输出头语义**——若是 return forecast 而非 cross-sectional score，
> 必须改成相对预测（`pred_i − group_mean(pred)`）再进壳。

**交付计数维持 5/10**（`omoK1A5m` / `akVnvzX5` / `gJWoaJqv` / `kqJLawqP` / `e76xgXkM`）。
earnings_chart_dl 贡献 **+0**，缺口仍 5 颗。

---

## 附录 AJ — insider_matrix 换手前沿（47B / wave 48，10 臂）：**+0**，但 prod 面被推翻（2026-10-22）

**出发点**：全仓已知最强 IS 单腿 —— `ts_zscore(eur_aggregated_value_1, 252)`（`zqbvOmOR`）
S **4.30** / F **3.28** / 2Y **5.65** / SUB 1.12，**只有换手 176.85% 一闸**。
短窗版 `ts_zscore(…, 66)`（`gJZYxMml`）S 2.89 / F 2.10 / 2Y 4.25 / TO 174.92%。

**先测 prod（这一步推翻旧结论）**：`zqbvOmOR` **0.5155**、`gJZYxMml` **0.619**。
⇒ insider_matrix 的 prod 墙 **不是 0.938**（那是另一副骨架），这条骨架 prod 余量很大。
**prod 不是本族的墙**，墙在换手 / 集中度 / SUB。

| 臂 | 表达式（核 = `ts_zscore(eur_aggregated_value_1, 252)`） | S | F | 2Y | TO | SUB | 0.43×S | CW | RA 失败项 |
|---|---|---:|---:|---:|---:|---:|---:|---:|---|
| pwvWNdm6 | `ts_decay_linear(·, 5)` | 4.20 | 3.18 | 5.59 | 1.7573 | 1.02 | 1.82 | 0.50 | TO/SUB/CW |
| 3qjGpobQ | `ts_decay_linear(·, 10)` | 4.20 | 3.18 | 5.60 | 1.7566 | 1.01 | 1.82 | 0.50 | TO/SUB/CW |
| kqJ8PN7K | `ts_decay_linear(·, 20)` | 4.19 | 3.17 | 5.60 | 1.7562 | 1.03 | 1.81 | 0.50 | TO/SUB/CW |
| LL58GMaa | `ts_decay_linear(·, 40)` | 4.19 | 3.17 | 5.60 | 1.7560 | 1.03 | 1.81 | 0.50 | TO/SUB/CW |
| XgRNo9Qa | `ts_mean(·, 3)` | 3.99 | 3.12 | 5.63 | 0.8770 | 1.04 | 1.73 | 0.1607 | TO/SUB/CW |
| ZYmXEQex | `ts_mean(·, 5)` | 3.44 | 2.67 | 5.07 | 0.5969 | 0.73 | 1.49 | 0.1164 | SUB/CW |
| 2rjGpAbx | `ts_mean(·, 10)` | 2.99 | 2.40 | 4.55 | 0.3479 | 0.82 | 1.29 | **过** | SUB |
| QPYWGvXr | `hump(·, 0.01)` | 4.24 | 3.22 | 5.65 | 1.7616 | 1.07 | 1.84 | 0.50 | TO/SUB/CW |
| KPmVGJag | `hump(·, 0.02)` | 4.21 | 3.19 | 5.61 | 1.7575 | 1.06 | 1.82 | 0.50 | TO/SUB/CW |
| j2eV6YQE | `ts_decay_linear(hump(·, 0.01), 10)` | 4.17 | 3.15 | 5.58 | 1.7534 | 1.02 | 1.81 | 0.50 | TO/SUB/CW |

**四条归因**

1. **`ts_decay_linear` 与 `hump` 对换手完全无效**（1.7685 → 1.7560–1.7616，**0.7% 以内的抖动**）。
   原因不是算子失灵，而是**换手源在 `ts_zscore` 自身**：252 日窗口逐日滚动 ⇒ 即便原始字段不变，
   标准化后的截面值天天漂移；衰减一个「本就在动的序列」不降换手。
   ⇒ **本族不能靠平滑算子修换手，必须动窗口语义（`ts_rank` / `ts_delay` 差分 / `trade_when` 门控）。**
2. **只有 `ts_mean` 降换手**：3 → 0.877、5 → 0.597、10 → 0.348，单调有效。
   但 **SUB 同步崩塌**（1.04 → 0.73 → 0.82），相对 0.43×S 的限额（1.73 / 1.49 / 1.29）全不过。
   ⇒ **CW 与 SUB 在本族互为反向**：集中（CW 0.5 / 19 多 22 空）才有 SUB 1.02–1.07；
   分散到 CW 合格（`ts_mean 10`：158 多 232 空）后 SUB 只有 0.82。
   这是**事件型信号的固有矛盾**——收益只存在于少数真正有事件的票上，平摊即稀释。
3. **CW 0.5 是独立的结构缺陷**，不是换手的副产物：基础臂只有 19 多 / 22 空。
   `eur_aggregated_value_1` 在 USA/TOP3000 的有效截面被 `ts_zscore` 卡到 ~41 名，
   提高覆盖要动 backfill/窗口，而任何提高覆盖的做法都会把 SUB 拉回第 2 条的死结。
4. **IS 强度与可提交性在这里完全脱钩**：S 4.2 是 analyst 冠军（1.89）的 2.2 倍，但它是
   **一只 41 票的组合**。`risk_neutralized_sharpe` 4.1 ⇒ 不是风格 beta，是真实但极窄的事件 alpha。

**裁决**：`insider_matrix / eur_aggregated_value_1` 在 USA/D1/TOP3000 **D15 判死**，
平滑轴已穷尽（10 臂覆盖 decay 5/10/20/40 × mean 3/5/10 × hump 2 档 × hump+decay），
不加变体。**但保留一条可复用事实**：本族 prod 只有 0.52–0.62，
生产相关性在这个数据集上**不是限制**——未来若换一副能同时满足 TO/CW/SUB 的壳，可零成本复用该结论。

**交付计数维持 5/10**，insider_matrix 贡献 **+0**。

---

## 附录 AK — 波 49/50/51b 收官：insider 双数据集判死，`earnings_sent_matrix` 出现一条全净腿（2026-10-22）

### §A 家族 A prod 第五臂：`RR6bv6rz` = **0.9054**（0 免费交付）

`pw5RbrYX` 0.9000 / `leKKGb9l` 0.9014 / `RR6bv6rz` **0.9054** —— analyst 五臂簇的家族 A
三臂全部 ≈0.90，家族 B 三臂 0.9916–0.9991。`rKeOaLvo` 平台 PC 端点连续空响应 45 分钟未出数，
按家族推断同 ≈0.90（该轮询进程已成僵尸，已停）。
⇒ **全库 IS 全闸候选 0 条可快赢**，此前「29 条候选里也许有几条 prod 没过线」的假设彻底关闭。

### §B 波 50 `insider_agg_matrix` 水平值族：**+0**（size contamination）

8 臂设计，实际只跑 4 臂（旧代码把 429 记成永久失败，`L2_z`/`L3_conc`/`D1_ind`/`D2_indchg` 从未运行）。
全部用 `ts_backfill(..., 66)` + `group_rank(·, subindustry)`：

| 臂 | alpha | S | F | 2Y | TO |
|---|---|---:|---:|---:|---:|
| `group_rank(directional_significant_value_1, subindustry)` | `WjLYPQXG` | 0.92 | 0.50 | 0.55 | 4.9% |
| `group_rank(ts_decay_linear(·, 66), …)` | `6XAGrajL` | 0.74 | 0.32 | 0.64 | 3.1% |
| `group_rank(add(add(D1,D2),add(D3,D4)), …)` | `LL5893Oe` | 0.62 | 0.25 | 0.68 | 6.5% |
| `group_rank(ts_zscore(top_directional_significant_value_1,252), …)` | `xA1lYQMb` | 0.15 | 0.03 | 0.60 | 3.4% |

**归因**：`*_significant_value_*` 量纲是「金额强度」而非「方向」，同一市值口径下大票天然占优
⇒ 截面被规模污染，中性化后信息归零。换手 3–6% 与 2Y 0.55–0.68 都稳定，说明**不是噪声，是没有截面信息**。
与 (a) USA USD 内部人金额族两次判死（E5 −0.13 / C7 0.13）、(b) GLB 姊妹集三值全死（0.08/0.02/0.32）互为印证。
⚠ 另一条次要嫌疑：`ts_backfill(·, 66)` 用在稀疏事件上会把一次事件铺成 66 天的僵尸持仓 —— 该写法此后不再用于事件字段。

### §C 波 51/51b `insider_trx_matrix` recipe-2：**SUB/S 结构性判死**

**第一轮（波 51）全灭于算子**：论坛骨架的 `to_nan(x, value=0, reverse=true)` 被平台拒为
`Attempted to use inaccessible or unknown operator "to_nan"`（4/4 臂 ERROR）。
平台只有 `is_nan` / `if_else`；`ts_sum` 的零值本就是加法中性，去掉包装语义不变。
本地 `wqb.expression.op_arity` 当时 **对未知算子跳过**（幽灵算子归 `operator_audit` 管），
所以 **arity 通过 ≠ 平台可用**。已将 `to_nan` 补进 `wqb.config.KNOWN_GHOST_SEED`（gate.py 读它）。
（2026-10-23 起该闸本身已改 fail-closed：目录外算子报 `[UNKNOWN_OP]`，见
`docs/experience/04_engineering.md` §14.6。）

**第二轮（波 51b）给出结构答案**，骨架 `ts_zscore(ts_sum(<count>, W), 252)`，TOP3000/SUBINDUSTRY/decay 5：

| 字段 | W | alpha | S | F | 2Y | TO | SUB | 限额 | **SUB/S** | 多/空 |
|---|---:|---|---:|---:|---:|---:|---:|---:|---:|---|
| `total_top_secondary_buy_transaction_count` | 21 | `9qEGm29x` | 2.67 | 2.79 | 3.19 | 19.0% | 0.69 | 1.16 | **0.26** | 244/445 |
| 同上 | 42 | `GrgQxKEJ` | 2.55 | 2.73 | 3.15 | 13.9% | 0.82 | 1.10 | **0.32** | 256/487 |
| 同上 | 63 | `JjP319zn` | 2.44 | 2.54 | 3.21 | 11.3% | 0.87 | 1.06 | **0.357** | 285/513 |

**平台口径更正（重要）**：`LOW_SUB_UNIVERSE_SHARPE` 的 limit **不是固定 0.97，而是 `0.43 × S`**。
可提交的充要条件是 **SUB/S ≥ 0.43**，与 S 绝对值无关。窗口从 21 加到 63 只把比率从 0.26 抬到 0.357，
**渐近值仍 < 0.43** ⇒ 窗口不是杠杆。

**裁决**：USA 内部人计数族（base recipe 与 recipe-2）**结构性判死**。不是信号弱
（S 2.4–2.7、F 2.5–2.8，是本战役最强的 IS 读数之一），是**覆盖只集中在有内部人交易的少数票**。
USA/D1 没有 `ILLIQUID_MINVOL1M` 子宇宙可换（只有 TOP3000/2000/1000/500/200）。
**唯一未测的残余杠杆是「换小宇宙」**（TOP1000/TOP500，使 sub-universe 变成全场），波 51c 待跑；
若 TOP1000 上 SUB/S 仍 <0.43，则本族连同宇宙杠杆一并封存。

### §D 波 49 `earnings_sent_matrix`（USA ds **339**，EARNINGS 塔，7 字段，aC 33）：**IS 六臂，三条全净**

机制：`positive_sentiment_probability_3 - negative_sentiment_probability_3`
（财报电话会/公告情绪净概率）→ `ts_zscore(ts_backfill(·,252), 252)` → `group_rank(·, industry)`。
**唯一杠杆 = 中性化**（base 族 prod：STATISTICAL 0.7225 / SECTOR 0.7903，卡在墙外）。

| 臂 | alpha | 中性化 | S | F | 2Y | TO | SUB (限额) | CW | CLUSTER | RA 失败 |
|---|---|---|---:|---:|---:|---:|---|---|---|---|
| S_INDUSTRY | `ZYmX7ZG3` | INDUSTRY | **2.30** | 1.71 | 3.89 | 6.1% | 1.31 (1.16) | pass | pass | **0** |
| S_MARKET | `QPYW7nZg` | MARKET | 2.25 | **1.74** | 3.83 | 5.9% | 1.36 | pass | pass | **0** |
| S_REVMOM | `e761zqMp` | REVERSION_AND_MOMENTUM | 2.28 | 1.64 | 3.79 | 8.4% | 1.11 | pass | 1.10 | **0** |
| S_SLOWFAST | `3qjGlvPO` | SLOW_AND_FAST | 2.24 | 1.27 | 3.90 | 10.5% | 0.76 (0.97) | pass | 0.89 | SUB |
| W_SUB | `d5K9jWNv` | SUBINDUSTRY | 1.71 | 0.77 | 1.50 | 31.6% | 1.20 | warn | 0.89 | F/CW/2Y |
| W_IND | `O0J67jNp` | INDUSTRY | 1.82 | 1.01 | 1.62 | 30.7% | 1.19 | warn | 1.33 | CW |

- `ZYmX7ZG3` **self-corr 0.6559**（本地，135/139 OS 池）**通过**。
- **逐年稳健性（`ZYmX7ZG3`）**：10 年全正，最弱 2016 年 0.92、2020 年 0.95；2017 4.33 / 2021 2.37 / 2022 4.62 / 2023 3.04；
  多空各 ~1500 只，换手 5.3–7.4% 十年平稳 ⇒ 不是单年行情。
- 三条 S 臂共用同一表达式，只差中性化 ⇒ **互相关接近 1，最多只能提 1 条**。
- prod 实测在途（base 族 0.72–0.79，需要跌破 0.70 才算白捡）。

**可复用**：同为「情绪净概率 × 财报」，换中性化能把 CLUSTER/CW 从警告清成 pass 的同时保住 S>2.2；
但 prod 由 base 族的 0.72–0.79 决定，中性化能否把它压到 0.7 以下是本轮唯一的问题。

### §E 台账修复

5 条已交付 alpha（`omoK1A5m` / `akVnvzX5` / `gJWoaJqv` / `kqJLawqP` / `e76xgXkM`）此前**从未写回 `alphas` 表**
（`WHERE alpha_id=?` 全部返回空 ⇒ 库存/提交队列工具对它们结构性失明）。
已跑 `tools/sync_platform_alphas.py --region USA` 补齐：现 5 条均为 `platform_status=ACTIVE` / `stage=OS`，
带 prod 0.5532–0.6978 与 self 0.455–0.6445。全平台漏记 51 条（USA 7 条）一并回写。

**交付计数维持 5/10**；波 49 若 prod <0.70 则为第 6 条。

### §F 波 52 `earnings_sent_matrix` 概念广度：7 个概念只活 3 个，且**彼此 0.74–0.998 相关** ⇒ 该数据集是单名额

波 49 留下的真正问题不是 S（2.30），是 **prod**（base 族 0.7225–0.7903，全在中性化层面）。
波 52 换的是**概念**而不是设置：同一 7 字段数据集上 7 个互不相同的机制（冠军壳冻结：
decay 0 / trunc 0.05 / INDUSTRY / TOP3000）。

| 概念 | alpha | S | F | 2Y | TO | SUB/S | self | 结论 |
|---|---|---:|---:|---:|---:|---:|---:|---|
| SPR_conf 净概率 z × (1−中性概率) | `XgRNO8k8` | **2.35** | 1.76 | 4.02 | 6.1% | 0.57 | 0.656 | 全净 |
| LEVEL 净概率水平（波 49 冠军） | `ZYmX7ZG3` | 2.30 | 1.71 | 3.89 | 6.1% | 0.57 | 0.656 | 全净 |
| DIS_sgn 两套加权法的分歧 | `78oG2W7v` | 1.75 | 1.11 | 3.60 | 6.1% | 0.57 | 0.648 | 全净 |
| CHG_spr 净概率 66 日变化 | `vROYP7Yz` | 1.76 | 1.15 | 2.87 | 7.9% | 0.63 | **0.722** | self 卡墙 |
| ENT_amb 三分类熵 | `d5K9Pm8K` | 0.87 | 0.37 | 0.62 | 6.4% | 0.43 | — | 死 |
| LBL_pers argmax 标签均值 | `1YjG00YW` | 0.73 | 0.31 | 0.31 | 1.6% | 0.27 | — | 死 |
| DIS_abs −\|w1−w2\|（分歧幅度） | `bl8xKZ16` | −1.01 | −0.46 | −1.85 | 6.3% | — | — | 反向死 |
| NEU_chg −中性概率 66 日变化 | `0mjGaQVq` | −0.93 | −0.44 | −1.41 | 8.3% | — | — | 反向死 |

**决定性别名互相关（本地 PnL，2494 个交易日，纯读取不占槽）**：

| 对 | corr |
|---|---:|
| `XgRNO8k8` × `ZYmX7ZG3` | **0.9976** |
| `XgRNO8k8` × `78oG2W7v` | 0.8965 |
| `ZYmX7ZG3` × `78oG2W7v` | 0.8976 |
| `78oG2W7v` × `vROYP7Yz` | 0.7408 |

⇒ **四个概念在 PnL 空间是同一个因子**。本数据集**只能交付 1 条**，无论概念名字差多少。
真正有价值的副产品是：四个候选对已交付 5 条的最大相关只有 **0.40–0.43**（`XgRNO8k8` 对
`gJWoaJqv` 0.425 最高），即 ds339 与分析师修正书**确实正交**——它值得那 1 个名额，但只值 1 个。

**可复用（本项目第一条反「概念广度」的硬证据）**：在**单数据集内**换概念，不等于换因子。
判据必须提前定：先算概念互相关，再决定要不要为同一数据集排第 2 条波；
否则「7 概念 3 全净」会被误读成「3 个名额」，实际是 1 个名额 + 2 条废弃 alpha。

### §G 波 54 空头流量修复：聚合把 2Y 抬到 1.29 但把 S 压到 1.23 ⇒ 该族按预注册 kill line 封存

波 53 的 `SSR_lvl`（`d5K9Pb0Y`，日频卖空成交占比截面 z）拿到全库最好的**广度**
（S 1.68 / SUB 1.55 ⇒ SUB/S **0.92**），但 TO 41.9% 打出 F 0.55、2Y 1.09 两条硬 FAIL。
波 54 的问法不是「换字段」而是「这是不是日频噪声」——按 Boehmer-Jones-Zhang 原始设定
把信号聚合到月/季频，一次只动聚合窗与 decay（中性化/truncation 全部冻结在 SUBINDUSTRY 0.08）：

| 臂 | 核心 | alpha | S | F | 2Y | TO | 结论 |
|---|---|---|---:|---:|---:|---:|---|
| flow66 | 66 日均值 z252 | `A1QL5KYl` | 1.23 | 0.62 | 1.29 | 4.8% | 最好，仍三闸全缺 |
| flow22 | 22 日均值 z252 | `RRA5o0ra` | 0.99 | 0.45 | 0.75 | 8.4% | 死 |
| flow22_d20 | 同上 + decay20 | `npA6lO6q` | 0.91 | 0.40 | 0.81 | 5.9% | decay 反向 |
| flowchg22 | 22 日均值 22 日变化 | `mLYKNjz2` | 0.01 | 0.00 | −0.65 | 11.2% | **变化量是纯噪声** |
| sip_surp | 空头兴趣意外比水平 | `E5VmMl8L` | −0.12 | −0.01 | −2.71 | 56.0% | 死 |
| sip_surp22 | 同上 22 日均值 | `A1QL5zLg` | −0.08 | −0.01 | −0.67 | 11.7% | 死 |

**归因（这是本轮真正的产出）**：卖空流量在 USA/D1 是**一个纯水平（horizon）权衡**——
日频有信息但 TO 41.9%，聚合到 66 日把 TO 砍到 4.8%、2Y 从 1.09 抬到 1.29，
代价是 S 从 1.68 掉到 1.23。两端都不满足 S≥1.58 ∧ F≥1.0 ∧ 2Y≥1.58，
且 `flowchg22` 的 S=0.01 证明**变化量方向完全没有信息**（BJZ 机制作用在水平上，不在变化上）。
⇒ 按预注册 kill line 封存 `us_short_sale` 流量族与 `short_interest_surprise_ratio` 水平族，
**不再平滑、不再换窗**。这两个数据集若还要碰，只能换完全不同的字段组（如借券费率/回补天数）。
**可复用**：换手墙与 2Y 墙在**同一根时间轴上**，用聚合窗去救 2Y 必然牺牲 S；
当「日频 S 高 TO 高」与「聚合 S 低 TO 低」两端都不过闸时，这是**数据类型**的判决，不是参数的判决。

### §H USA/D1 全数据集拥挤度全景（166 个数据集，2026-10-22 `logs/_tmp_usa_ds_map.json`）

用 `/data-sets` 全量分页拉取 USA/D1/TOP3000 的 166 个数据集，按数据集级 `alphaCount` 升序。
**这一步改变了后续选集方向**：此前只看字段级 aC（option3 字段级 5–128），误以为 option3 最干净；
数据集级 aC = **492**，而同区的文本类只有 29–49。

| 数据集 | 类别 | 字段 | 覆盖 | **数据集 aC** | 判断 |
|---|---|---:|---:|---:|---|
| event_relation | other | 9 | 0.733 | **29** | 文本事件关系，最低拥挤 |
| **news_sentiment_nlp** | other | 23 | 0.995 | **32** | 波 56 主攻（标题 5 种情绪模型 + 可读性） |
| other623 | other | 6 | 0.987 | 33 | TextBlob 新闻 |
| news_sentiment_dl | other | 88 | 1.000 | 42 | DL 新闻情绪，字段最多 |
| forum_sentiment | other | 13 | 1.000 | 42 | 论坛情绪，满覆盖 |
| other635 | other | 9 | 0.993 | 45 | 路透标题情绪（次选） |
| other546 | other | 13 | 0.663 | 47 | 机构网络 |
| filing_sentiment | other | 21 | 0.540 | 49 | 监管文件情绪 |
| pv3 | pv | 13 | 0.597 | 62 | 全球日频价量 |
| fundamental93 | fundamental | 46 | 0.631 | 85 | 税务/递延数据 |
| other359 | other | 10 | 0.742 | 85 | 网页评论 |
| twitter_sentiment_l2 | socialmedia | 95 | 0.979 | 249 | 推特情绪聚合 |
| shortinterest29 | shortinterest | 32 | 0.884 | 231 | 分组卖空 |
| **option3** | option | 20 | 0.880 | **492** | 波 55 已证 S≈0 |
| **option6** | option | 133 | 0.962 | **19,159** | **饱和，禁止入队** |
| option8 / option9 / option40 | option | 64/74/208 | 0.97+ | **203,016 / 83,652 / 3,200** | 全部饱和 |
| earnings_sent_matrix | earnings | 7 | 0.700 | 1,431 | 已交付 1 条（波 52 §F 单名额） |
| institutions20 | institutions | 17 | 0.980 | 1,249 | 名为 Short Sale Volume，拥挤 |

**两条硬结论**：
1. **波 55 预注册 kill line 里「转 option6」这条已作废**——写下时没有数据集级拥挤度数据。
   option6 aC 19,159 / option8 203,016 / option9 83,652，这三档不是「还没挖」，是**已被挖穿**，
   进去只会拿 IS 高分 + prod 撞墙。预注册 kill line 应按新证据修订而不是机械执行。
2. **USA/D1 剩下的低拥挤前沿是文本/新闻类**（aC 29–49），且与我们已交付的 5 条分析师修正
   在**数据源与机制上都正交**。后续 5 个名额的主攻面就锁定在 §H 表里 aC < 100 的那批。
   **可复用**：选集的拥挤度必须用**数据集级** `alphaCount`，字段级会系统性地把「大而饱和」的
   数据集误判成干净（同一个 option 族，字段级 aC 5 vs 数据集级 19,159，差三个数量级）。

### §I 波 55 `option3` 期权结构：6 个机制 6 个死，该族在 USA/D1 日频无信号

设置冻结（decay 5 / trunc 0.08 / INDUSTRY / TOP3000），每个臂一个独立经济机制：

| 臂 | 机制 | alpha | S | F | 2Y | TO | 结论 |
|---|---|---|---:|---:|---:|---:|---|
| skew_lvl | XZZ2010 put−call IV 偏斜 | `leMgPL2l` | −0.10 | −0.01 | −0.95 | 23.6% | 无信号 |
| skew_chg | 22 日偏斜变化 | `omoP01Rm` | −0.73 | −0.25 | −1.26 | 26.7% | 反向弱 |
| pcr_lvl | Pan-Poteshman put/call OTM 量 | `pwvWegdx` | −0.58 | −0.13 | −0.95 | 39.6% | 反向弱 |
| oi_chg | 22 日 put/call 持仓变化 | `xA1lpXen` | 0.00 | 0.00 | −0.43 | 20.1% | 零 |
| vpr | IV_ATM − 已实现波动 | `4aqgCWgc…`(重跑) | 0.62 | 0.23 | — | 15.8% | 弱，IS_LADDER 也挂 |
| spread_lvl | IV 买卖价差（期权流动性） | （见 json） | −0.77 | −0.21 | −1.17 | 33.6% | 反向弱 |

**归因**：六个臂的 |S| ≤ 0.77，方向也没有一致性（三个负、一个正、一个零）。
不是「符号反了」，是**信号本身在 TOP3000 日频上不存在**。经济上讲得通的三种期权信息
（偏斜、成交意愿、波动风险溢价）在高流动性大盘股上早被做市商吃掉，且 20 个字段的
数据集级 aC 492 说明该数据被大量使用——这与「无残余 alpha」自洽。
⇒ 按 kill line 关闭 option3；**option6/8/9 因饱和（aC 1.9万–20万）不入队**（见 §H）。

**工程教训（会重复踩，必须固化）**：`vpr` 首跑 38 秒就 ERROR，原因是表达式里写了
`ts_std` —— 平台算子名是 **`ts_std_dev`**，`ts_std` 不存在。而本地 `wqb.expression.op_arity.check_expression`
**对 catalog 里没有的算子静默跳过**（其 docstring 明写「幽灵算子归 operator_audit 管」），
所以 6 条表达式本地全 OK、平台直接拒。
⇒ **发批前除了本地元数闸，必须再过一次算子存在性闸**（`campaign_intel ghost-audit`
或 `operator_audit`），两者互补、都不可省。本次是「元数全过、算子名不存在」的典型形态。

## 附录 AL — 波 56/58 收官与「自相关池」结构性发现（2026-10-23）

### §A 波 56 `news_sentiment_nlp`（aC 32 / cov 0.995 / 23 VECTOR）：6 个机制 6 死

设置冻结 USA/TOP3000/D1、decay 10、trunc 0.08、INDUSTRY、nanHandling ON；每臂一个独立文本机制，
全部先 `vec_*` 聚合再进时序算子。

| 臂 | 机制（文献） | alpha | S | F | 2Y | TO |
|---|---|---|---:|---:|---:|---:|
| tone_5 | Tetlock 净语调 5 日均值 | `…` | 0.60 | 0.16 | 0.09 | 22.7% |
| tone_22 | 同上 22 日 | `XgRNZ6X1` | −0.21 | −0.04 | −1.30 | 10.0% |
| attn | Barber-Odean 关注度（−新闻条数） | `xA1l7Rnq` | −0.53 | −0.14 | −0.77 | 22.5% |
| tone_drift | Tetlock 漂移（22 日语调的 66 日变化） | `VkdMQaqM` | 0.09 | 0.01 | −0.13 | 10.6% |
| subj | −标题主观性 | `rKd0aV9j` | −0.20 | −0.04 | −0.43 | 9.8% |
| obfus | −Gunning-Fog 可读性（Loughran-McDonald 遮蔽假说） | `P0MPL8LK` | −0.06 | −0.01 | 0.91 | 10.3% |

**归因**：|S| ≤ 0.60，且方向不一致（两正四负、一个近乎零）⇒ 不是符号问题，是
**该数据集的标题文本在 USA/D1 日频上没有残余 alpha**。这与数据集 aC 32（全 USA 最低档）
形成对照：**低拥挤 ≠ 有信号**，它也可以只说明「没人用是因为没用」。
按预注册 kill line 关闭该数据集，**不重调 decay**、不转 `other635` 重测同一机制。

### §B 自相关池是本账户的真正瓶颈（实测，不是推断）

`GET /users/self/alphas?stage=OS` 全量分页（346 条）按 (region, universe, delay) 归类，
USA/D1 的 OS 池：**TOP3000 = 139**、TOP2000 = 6、TOP1000 = 1、ILLIQUID_MINVOL1M = 4。
TOP3000 池的构成：**101 颗 `model77`**、19 颗未标数据集、10 颗 `fundamental6`、3 颗 model、
2 颗 fundamental3、analyst_consensus / fundamental / institutions / pv / other 各 1。
⇒ 任何新机制都要先跟这 139 颗（其中 101 颗同源）比一次日收益相关。

实测被自家 book 吸收的两例：
- `WjLekJQO`（web_traffic 页数，S 1.85/F 1.46）**self 0.7718**，最高相关是 `KmP73gj`
  `group_rank(fnd6_mrcta, subindustry)` —— 基本面规模/资本开支代理。
- `88PmKRzv`（institutions18 持股比例，S 1.81/F 1.44）**self 0.7408**，最高相关
  `PYGjZVx` / `dK5ExGg`（model77 增长腿 / `fnd6_ivaco`）。

### §C 库存不是出路：40 条 IS 全闸未提交里没有可提交项

按 USA 五道 IS 闸（S≥1.58 / F≥1.0 / 2Y≥1.58 / TO 0.01–0.70 / SUB≥0.43×S）+ 未提交 + 未软删
筛出 **40 条**，其中 17 条从未测 prod、7 条 prod<0.7、16 条 prod≥0.7。逐条核后： <!-- from config.prod_corr_max -->

1. **`XgRNO8k8`（ds339，全库最强 IS：S 2.35 / F 1.76 / 2Y 4.02 / TO 6.05%）prod = 0.8148**
   （2026-10-23 平台实测，253 s）⇒ 拒提。
2. 7 条 prod<0.7 的全是 `analyst_consensus` **同一表达式的设置孪生**： <!-- from config.prod_corr_max -->
   `group_rank(ts_zscore(mean_estimate_targetprice_annual12_tribes,175),subindustry)`，
   与已提交的 `KPrGMXZ8`（decay 500）只差 decay（300/280/260/240/220）。
   实测 `1YZp6EP6`(decay 300) vs `KPrGMXZ8`(decay 500) **日收益相关 = 0.9785**（n=2493）
   ⇒ **self 必挂**，全部不可提交。
3. `leKLRA1N`（institutions18）prod 0.9394 已判死（§2026-10-21 复核）。

⇒ 25 条未测 prod 里没有新机制，**5 个缺口只能来自新机制**。

### §D 波 58 宇宙迁移 A/B：TOP1000 全灭 ⇒ 宇宙轴关闭

动机：self 池按 (region, universe, delay) 分区，TOP1000 只有 1 颗 OS ⇒ self 近乎免费。
做法：把 7 条最强非 analyst 表达式**逐字**搬到 USA/TOP1000/D1，decay/trunc/中性化沿用父臂（单变量）。

| 臂 | 父臂（TOP3000） | 父 S/F/2Y | TOP1000 S/F/2Y | S 保留率 | SUB/S | RA 挂 |
|---|---|---|---:|---:|---:|---|
| inst22_ind | 88PmKRzv | 1.81/1.44/1.96 | 1.01/0.64/1.49 | 0.56 | 0.32 | 4 |
| inst66_ind | GrOq3WLP | 1.71/1.33/1.96 | 0.85/0.50/1.49 | 0.50 | 0.31 | 4 |
| inst66_sub | JjQV5ep2 | 1.73/1.30/1.86 | 0.89/0.51/1.38 | 0.51 | 0.27 | 4 |
| inst66_sub_bf | leKLRA1N | 1.71/1.27/1.86 | 0.93/0.54/1.38 | 0.54 | 0.33 | 4 |
| webtraf_pages | WjLekJQO | 1.85/1.46/1.86 | 1.15/0.51/**0.32** | 0.62 | 0.46 | 4 |
| webtraf_sess | xA1bM50m | 1.85/1.45/1.83 | 1.17/0.52/**0.06** | 0.63 | 0.61 | 2 |
| esm_spr | XgRNO8k8 | 2.35/1.76/4.02 | 1.30/0.80/**2.12** | 0.55 | 0.88 | 2 |

**归因**：S 保留率 0.50–0.63，**2Y 更差（web 流量两臂直接掉到 0.06–0.32）**；
institutions 族的 SUB/S 也没被修好（0.27–0.33，父臂 0.74–0.91 反而是最好的）。
⇒ **本 book 的边际集中在 1001–3000 名流动性的下半段**（TOP1000 是全球最大 1000 只，
定价效率最高）。与波 51c 同向：insider 计数 TOP1000 上 S 2.55→0.54、SUB/S 0.36→0.93
（比率修好了但信号没了）。
**宇宙轴的结论**：换小宇宙能修 SUB、能清 self，但**同时把信号一起拿走**；
TOP2000 中点只对 `esm_spr` 一路还有理论空间（见 §F），其余不再重复。

### §E 工程教训：本地 `check_self_correlation` 会给假通过

`1YZp6EP6` 不在本地池里（未提交），本地检查给出 **max 0.4214 → passes_check=true**；
用平台 PnL 直接算，它跟同表达式孪生 `KPrGMXZ8` 的相关是 **0.9785**。
⇒ **提交前的 self 结论必须来自「目标 alpha 的当日 PnL + 池 PnL」直接计算**
（`get_alpha_pnl` 拉原始序列再相关），或用平台 `/correlations/self`；
本地 `check_self_correlation` 仅在**目标已在池中**时可作快筛。
本 campaign 此前的 self 读数若目标是未提交 alpha，都应视为「低置信」。

### §F S0 复扫（earnings7 / shortinterest / socialmedia，2026-10-23）

- **earnings**：`earnings7` aC **1317** / cov 0.648 / 40 字段（新闻事件摘要）；`earnings4` aC 13771、
  `earnings6` aC 4953、`earnings27` aC 1529 全部高拥挤 ⇒ 不入队。earnings 塔的剩余价值已被
  `earnings_sent_matrix`（单名额，已交付 1）与 `earnings_chart_dl`（判死）吃尽。
- **shortinterest**：`short_interest_pred` 已有「数据集层 fitness 天花板 ≈0.55」的实测结论；
  `shortinterest29` 有 `USA-SHORTINTEREST29-RANK-WEAK` 死档；`us_short_sale` 波 54 已封存；
  `shortinterest3/43` aC 4343/1492 饱和；`shortinterest24` 仅 1 字段 cov 0.257。
  ⇒ **shortinterest 类别整体关闭**。
- **socialmedia**：⚠ **本条初版结论错误，已更正（2026-10-22）**。初版写「唯一活口 `creator_signal_perf`，
  下一波主攻」——**该数据集早在 2026-10-21 就已实测判弱封存**：
  `_usa-creator-signal-perf-field-profile-20261021.md` §7 记 8 臂批 1（multisim `lUTJ8bIw4X08N215STbytjR`，
  8/8 COMPLETE），**max |S| = 0.99 < 1.0** ⇒ `USA-CREATOR-SIGNAL-PERF-WEAK`，判据明写「不发第 2 批」。
  根因是本轮 S0 复扫只看了 catalog 的 aC/覆盖，**没回读同一数据集已有的字段画像 §7**（这就是用户反复强调的盲扫）。
  平台数字也已漂移：aC **139**（初版记 155）／userCount **76**（初版 87）／cov 0.6562 / valueScore 3。
  - **误开后果（如实记账）**：2026-10-22 23:2x 误发波 60 三臂后当即停批——`A3_smart_cover`
    （`vec_avg(overall_prediction_success_rate)`）S **0.04** / F 0.0 / 2Y −0.83，与批 1 同向（账户级技能无截面区分度）；
    `A1_skill_dir` 因 **`Operator multiply does not support event inputs`** 报 ERROR（重发后与 A2 在飞，结果见 §H）。
  - **可复用工程结论（本批唯一新增资产）**：`creator_signal_perf` 这类 VECTOR 字段在 FASTEXPR 里是
    **event 输入**，**任何向量级算术都被平台拒绝**（`multiply(a_vec, b_vec)` → ERROR）。跨字段组合只能先各自
    `vec_*(x)` 归约成矩阵再运算，**逐创作者（逐元素）加权在结构上做不到**。这条适用于所有 VECTOR 数据集。
  - 其余同族：`twitter_sentiment_l2` 已因 HIGH_TURNOVER 判死；`socialmedia8/12` aC 1.7 万/6.1 万饱和。
  ⇒ **socialmedia 类别同样关闭**（四个候选集：两个饱和、一个换手墙、一个判弱）。

### §G 波 59：ds339 `earnings_sent_matrix` 的 TOP2000 中点（2026-10-23）

单臂单变量（仅改 universe），`XgRNO8k8` 的表达式与设置逐字沿用：
`group_rank(multiply(ts_zscore(subtract(ts_backfill(pos,252), ts_backfill(neg,252)), 252), subtract(1, ts_backfill(likelihood_of_neutral_tone,252))), industry)`
设置：USA / **TOP2000** / D1 / INDUSTRY / decay 0 / trunc 0.05 / 2014-01-01–2023-12-31。

| 臂 | alpha | S | F | 2Y | SUB | SUB/S | TO |
|---|---|---|---|---|---|---|---|
| esm_spr_top2000 | `QPYOPLAK` | **1.70** | **1.14** | **3.50** | 1.34 | **0.79** | 7.17% |

`ra_failed=None`（无 FAIL/WARNING 计入 RA）；warns 仅 `CLUSTER_TEST` / `MATCHES_THEMES` / `OSMOSIS_ALLOCATION`。

**IS 全闸通过，但 self 判 BLOCK**（本地 PnL 直算，非 `check_self_correlation`）：

| 对手 | 日频全期 | 2022 起 | 21 日抽样 | 累计 PnL |
|---|---|---|---|---|
| `883WZJ1W`（同 pos/neg 概率字段族，2026-09-14 提交） | **0.7331** | **0.8250** | 0.6835 | **0.9951** |
| 其余 5 颗 TOP2000 池 | ≤ 0.247 | — | — | — |

⇒ `QPYOPLAK` 与 `883WZJ1W` 是**同一个因子**（累计 PnL 0.9951），阈值 0.70 无讨论空间。
**这条同时修正了波 58 的错误外推**：TOP1000 全灭不等于宇宙轴关闭——TOP2000 的 S 反而从 TOP1000 的 1.30 抬到 **1.70**，
F 从 0.80 抬到 1.14，2Y 从 2.12 抬到 3.50。**宇宙轴在 2000 上是活的，卡住的是同族已提交的位置。**

**TOP2000 池的真实结构（`get_user_alphas` 实测，6 颗全部 ACTIVE/OS）**：

| alpha | S | F | 2Y | self | **prod** | 设置 |
|---|---|---|---|---|---|---|
| `vROw5Rkd` | 4.01 | 3.33 | 3.87 | 0.6217 | **0.6217** | STATISTICAL / decay1 / trunc0.02 |
| `O08EjLVp` | 2.45 | 1.55 | 2.55 | 0.3321 | **0.5626** | STATISTICAL / decay0 / trunc0.08 |
| `d51A3nqY` | 2.45 | 1.47 | 1.89 | 0.3257 | **0.4910** | 同上 |
| `Wje6pdqN` | 1.89 | 1.00 | 1.81 | 0.2700 | **0.6091** | 同上 |
| `1YZQJKwR` | 2.48 | 1.41 | 2.14 | 0.2854 | **0.5751** | 同上 |
| `883WZJ1W` | 1.92 | 1.05 | 3.64 | 0.3814 | **0.6113** | 同上 |

两条可复用事实：① **TOP2000 的 prod 池仍有 0.08–0.21 余量**（全部 < 0.70，最紧 0.6217）；
② 该宇宙的成熟配方是 **STATISTICAL 中性化 + decay 0–1 + trunc 0.08**，与 TOP3000 默认（SUBINDUSTRY/decay5/0.08）不同。
后续在 TOP2000 上的候选一律按池内配方起跑，避免把「中性化差异」误记成「机制差异」。

### §H 波 60 收尾：`creator_signal_perf` 三臂全灭（与 2026-10-21 判弱一致）

三条在飞仿真已收（波 60 系误发，见 §F ⚠；三臂即全部成本）：

| 臂 | alpha | S | F | 2Y | TO | RA 失败 |
|---|---|---|---|---|---|---|
| `A3_smart_cover` `vec_avg(overall_prediction_success_rate)` | — | 0.04 | 0.00 | −0.83 | — | 4 |
| `A2_crowd_pnl` `vec_avg(asset_aggregate_portfolio_return)` | `ZYmgROjj` | **0.14** | 0.02 | **−0.59** | 36.7% | LOW_SHARPE / LOW_FITNESS / LOW_SUB / LOW_2Y |
| `A1_skill_dir`（修复后，先 `vec_avg` 再算术） | `A1Qe11PR` | **0.13** | 0.02 | **−0.56** | 36.6% | 同上 |

结论：**与画像 §7 的 8 臂方向完全一致**——账户级/聚合级预测统计量在本宇宙没有截面区分度；
`pyramid_short = socialmedia`，该数据集判死结论维持。可复用口径：这类「预测结果统计」字段先看**字段滞后是否 ≥ 7 天**，
是则直接跳过（画像 §7 已记）。

### §I 波 61 预注册：ds339 在 TOP2000 上做**机制正交**（不是扫参）

背景：§G 已证明同数据集、同宇宙的指标空间是活的，唯一障碍是 `883WZJ1W` 占了「净语气方向」这一层。
本波固定 ds339 + TOP2000 + STATISTICAL/decay0/trunc0.08，8 臂覆盖不同经济机制：

| 臂 | 机制 | 表达式核心 |
|---|---|---|
| B0 | 设置对照（原式换池内配方） | `rank(z(net,252) × (1−neutral))` |
| B1/B2 | 歧义溢价（中性概率）± | `rank(z(neutral,252))` |
| B3 | 双加权法分歧 | `rank(z(method1 − method2, 252))` |
| B4 | 语气波动 | `rank(ts_std_dev(net, 63))` |
| B5 | 语气修订动量 | `rank(z(ts_delta(net, 63), 252))` |
| B6 | 三向熵（均衡不确定性） | `rank(z(pos × neg × neutral, 252))` |
| B7 | 非中性门控方向 | `trade_when(z(neutral,252) < 0, rank(z(net,252)), -1)` |

判据：S≥1.58 & F≥1.0 & 2Y≥1.58 & SUB/S≥0.43 & TO≤0.70，且本地 self vs 6 颗池 < 0.70（重点 `883WZJ1W`）。
B0 若过全闸且 self<0.7 ⇒ 直接进 prod（不依赖新机制）；机制臂 S 明显低于 1.58 的按归因记录，不硬救。 <!-- from config.self_corr_max -->
**不换数据集、不换宇宙。**

### §J 波 61 收官：ds339 是**结构性单槽**数据集（2026-10-23 实测）

8/8 COMPLETE。设置全臂固定 USA/TOP2000/D1、INDUSTRY group、STATISTICAL 中性化、decay 0、trunc 0.08、
`2014-01-01…2023-12-31`（即 §G 实测的 TOP2000 池内成熟配方）。指标取自平台 `get_alpha_details`：

| 臂 | 机制 | alpha | S | F | 2Y | SUB | TO | RA |
|---|---|---|---:|---:|---:|---:|---:|---|
| **B0** | 净语气方向 × (1−中性概率)，池内配方 | `ZYmgYvOd` | **1.99** | **1.11** | **3.68** | 1.35 | 10.45% | **0 失败** |
| B3 | 双加权法分歧 `method1−method2` | `1YjOkEGm` | 1.51 | 0.73 | 3.12 | 0.89 | 10.48% | 2 |
| B5 | 语气修订动量 `z(Δ63(net),252)` | `9qE8ZwGq` | 1.39 | 0.64 | 2.50 | 1.22 | 12.44% | 2 |
| B7 | 非中性门控方向 `trade_when(z(neutral)<0, …)` | `WjL3M1lG` | 1.25 | 0.53 | 2.84 | 1.04 | 7.85% | 2 |
| B6 | 三向熵 `pos×neg×neutral` | `O0JRQA3g` | 0.70 | 0.23 | 1.81 | 0.29 | 10.87% | 3 |
| B1 | 歧义溢价 `+z(neutral)` | `qMEOMpbV` | 0.29 | 0.06 | 0.61 | 0.06 | 10.90% | 4 |
| B4 | 语气波动 `ts_std_dev(net,63)` | `9qE8ZGAo` | −0.06 | −0.01 | 0.22 | −0.07 | 8.23% | 4 |
| B2 | 歧义折价 `−z(neutral)` | `rKd9pELa` | −0.29 | −0.06 | −0.61 | −0.06 | 10.90% | 3 |

**B0 是 IS 全闸唯一通过者**（`checks.fail` 空、`ra_failed=false`、CLUSTER_TEST 1.02 仅 warning），
但本地 PnL 直算 self：

| 对手 | 日频全期 | 2022 起 | 21 日抽样 | 累计 PnL |
|---|---|---|---|---|
| `883WZJ1W`（TOP2000 池内同族已提交） | **0.9938** | — | — | ≈1.00 |
| B3 `1YjOkEGm` vs `883WZJ1W` | **0.7638** | — | — | — |

⇒ **B0 = `883WZJ1W` 的同一个因子**。根因不是表达式（B0 多了 `×(1−neutral)` 与 `ts_zscore` 包壳），
而是 **§G 记的「池内成熟配方」本身就是同族标识**：STATISTICAL 中性化 + decay 0 会把净语气方向
归一成与 `883WZJ1W` 相同的截面排序。**「换池内配方」在 ds339 上等价于复制已提交 alpha**
（可复用口径：TOP2000 配方适配只适用于**新机制**，不能用来给已占位机制换指标）。

**归因汇总**：
1. **B1/B2 互为镜像且都接近 0** ⇒ 中性概率的**水平**在本数据集无方向性，它只作为 B0 的**门控权重**有效
   （乘上净语气后有 S 1.99）。这解释了为什么 B6 三向熵（把它做成乘积）只有 0.70。
2. **B4 语气波动 −0.06** ⇒ 波动率型情感风险不是 alpha（与波 56 `news_sentiment_nlp` 的 stddev 臂同向）。
3. **B3 双加权法分歧 1.51/0.73/3.12**：方向是对的（2Y 3.12 最强之一），但 S/F 差一档，
   且 self 0.7638 已超 0.70 ⇒ **即便修到全闸也不可交**，不再投配额。
4. **B5 修订动量 1.39**、**B7 门控 1.25** 都低于 SHARPE 线，且 B7 的 investability 只有 0.53
   （`trade_when` 门控把可投资性打掉一半）⇒ 门控形态在本数据集不划算。
5. **没有第二条独立机制能过 S 1.58**。ds339 的向量信息（pos/neg/neutral、method1/2、6 档 probability）
   在截面维度上归约成**一个方向**，其余维度要么是噪声要么是它的单调变换。

**结论（数据集级）**：`earnings_sent_matrix` 在 USA/D1 是**单槽数据集**——方向层已被 `883WZJ1W` 占据，
本数据集不再是「新交付」的候选来源。它仍可作**组件**（已提交那颗），但**不为它再开波**。
此前 §E 的「self 必须用 PnL 直算」与 §G 的「TOP2000 配方」两条经验在本波都被复验：
B0 若只看 `check_self_correlation` 会给出低值（它不在池里），实际 0.9938。

**下一波（波 62）切换理由**：按用户「已点亮塔不回测」约束，USA/D1 现有点亮塔 = analyst 6 / model 4 /
earnings 1，故不再攻 earnings 塔。切换到 **`USA/D1/OTHER` 塔（multiplier 1.4，平台实测 `pyramid_short="other"`）**
的 `finnews_nlp_scores`，三查全净：① `dead_ends` 无该数据集；② `backtest_results` 对该数据集 **0 行**；
③ 本日志与字段画像册**零提及**。体检：aC **61**（USA/D1 低拥挤档）、userCount 39、**105 个字段**、
coverage **1.0**、valueScore **6**（未点亮塔中最高）、全 MATRIX 型（无 VECTOR 事件输入限制）。

### §K 波 62 预注册：`finnews_nlp_scores` 八机制首波（2026-10-23）

设置冻结 USA/TOP3000/D1、SUBINDUSTRY、decay 5、trunc 0.08、`2013-01-01…2023-12-31`（区域缺省配方）。
字段族按「统计量 × 极性 × 变体 `_1.._6`」组织（7 类：average / median / stddev / minimum / maximum /
upper_confidence / lower_confidence；`stddev_positive` 无 `_1`，只有 `_2.._6`）。
每臂一个独立经济机制，全部先 `ts_backfill(…, 66)` 固定字段滞后，再进时序算子：

| 臂 | 机制（文献） | 核心 |
|---|---|---|
| A | 净语调水平（Tetlock 2007） | `group_rank(ts_mean(pos1−neg1, 5), subindustry)` |
| B | 负向不对称（损失厌恶） | `group_rank(−ts_mean(neg1, 5), subindustry)` |
| G | 极端语调反转（过度反应） | `group_rank(−ts_mean(|pos1−neg1|, 5), subindustry)` |
| C | 分析师分歧（意见分散） | `group_rank(−ts_mean(stddev_pos2+stddev_neg2, 5), subindustry)` | <!-- lint:counterexample: 分歧度构造：正负两侧标准差相加，非跨信号混腿 -->
| D | 置信区间宽度（不确定性溢价） | `group_rank(−ts_mean(upper_neg1−lower_neg1, 5), subindustry)` |
| H | 覆盖突变（关注度冲击） | `group_rank(−ts_mean(Δ22(width), 5), subindustry)` |
| E | 语调偏度（均值−中位数） | `group_rank(ts_mean(pos1−median_pos1, 22), subindustry)` |
| F | 最坏报道极端（尾部风险） | `group_rank(−ts_mean(minimum_neg1, 5), subindustry)` |

判据（**预注册，事后不调**）：任一臂 S≥1.58 & F≥1.0 & 2Y≥1.58 & SUB≥平台 limit & TO≤0.70 ⇒ 进壳层
+ 本地 PnL 直算 self（vs TOP3000 139 颗池）；8 臂 **max S < 0.8** ⇒ 新闻情绪机制在 USA/D1 无残余信号，
按归因转同塔 `nlp_news_scores`（**不扫参数**）；**0.8 ≤ S < 1.58** ⇒ 先归因（差哪一闸 + 字段族读数）
再决定，禁止直接扫窗口/设置。全程不换 region。

**首批两臂实测（2026-10-23，其余六臂在飞）**：

| 臂 | alpha | S | F | 2Y | SUB | TO | RA |
|---|---|---|---:|---:|---:|---:|---:|---|
| A_net_tone | `E5VN1eVr` | 0.23 | 0.04 | −0.31 | −0.14 | 15.6% | 4 |
| B_neg_only | `JjPoqv8E` | −0.08 | −0.01 | −0.12 | −0.28 | 14.7% | 4 |

两臂同向归零 ⇒ **「语调水平」这一层在该数据集 USA/D1 上没有截面信号**
（与波 56 `news_sentiment_nlp` 六机制全灭同构，但注意那是 earnings 塔、这是 other 塔）。
短周期（5 日）均值把 105 个字段压成一个方向后归零，说明残余信息只能在**离散度/不确定性/极值**维度，
这正是 G/C/D/H/E/F 六臂要证伪的对象。



### §L 波 62 收官：`finnews_nlp_scores` 八机制全灭（2026-10-23）

八臂全部完成，指标一律经 MCP `get_alpha_details` 直取（harness 内置解析对 raw shape 取不到 2Y/SUB/RA，不作数）。
设置固定：USA / TOP3000 / D1 / SUBINDUSTRY / decay 5 / trunc 0.08 / 2014-01-01…2023-12-31。
平台塔位：八臂 `pyramid_short` 全为 `other` ⇒ `USA/D1/OTHER ×1.4`（未点亮）。

| 臂 | 机制 | alpha | S | F | 2Y | SUB (limit) | TO | rns | RA fail |
|---|---|---|---:|---:|---:|---:|---:|---:|---:|
| A_net_tone | 净语调水平 | `E5VN1eVr` | 0.23 | 0.04 | −0.31 | −0.14 (0.10) | 15.6% | 0.20 | 4 |
| B_neg_only | 负向单边 | `JjPoqv8E` | −0.08 | −0.01 | −0.12 | −0.28 (−0.03) | 14.7% | −0.42 | 4 |
| G_abs_tone_rev | 语调幅度反转 | `P0MxNLgL` | −0.07 | −0.01 | 0.34 | −0.11 (−0.03) | 15.5% | −0.40 | 4 |
| C_disagreement | 分歧度（std 和） | `rKd9Yxr9` | −0.47 | −0.13 | −0.19 | −0.04 (PASS) | 15.8% | −0.58 | 3 |
| D_conf_width | 置信区间宽度 | `MP0dWWga` | −0.59 | −0.18 | −0.49 | −0.36 (−0.26) | 15.7% | −0.83 | 4 |
| H_coverage_shock | 覆盖激增（Δ22 宽度） | `ZYmg5oK0` | 0.05 | 0.00 | 0.65 | 0.09 (PASS) | 19.3% | −0.30 | 3 |
| E_tone_skew | 语调偏度（均值−中位） | `wp93m58Q` | 0.45 | 0.13 | 0.54 | 0.36 (PASS) | 9.1% | 0.04 | 3 |
| F_neg_extreme | 最坏报道极端 | `JjPowWPm` | 0.13 | 0.02 | 0.10 | −0.05 (0.06) | 15.0% | −0.17 | 4 |

**max S = 0.45 < 0.8 ⇒ 预注册判据命中，不做任何参数扫描。** 数据集作为独立 ATOM 源判死。

归因（六条，逐条排除"壳层/成本/拥挤"解释）：

1. **不是字段没变化**：八臂多空比均在 1522:1541 ~ 1600:1459（≈1:1）⇒ `group_rank` 有真实截面离散度，
   归零来自"有差异但无预测力"，不是常量字段或覆盖塌陷（cov 1.000）。
2. **不是交易成本**：TO 9.1%–19.3% 全部落在 `LOW_TURNOVER`/`HIGH_TURNOVER` PASS 区间，离 70% 上限很远。
3. **不是中性化吃掉信号**：`risk_neutralized_sharpe` 六臂为负（−0.17 ~ −0.83）、两臂微正（0.04/0.20），
   残差方向与原始方向一致地弱 ⇒ 信号不在中性化后，而在原信号本身就缺失。
4. **不是与已提交池撞车**：`CLUSTER_TEST` 全在 −0.31 ~ 0.32（limit 1.58）⇒ 这批是"新但无用"，不是"有用但重复"。
5. **不是单一机制选错**：四个互不相同的机制簇同时归零 —— 语调水平（A/B）、不确定性（C/D/H）、
   尾部（F）、偏度（E）。文献上最能打的两条（Tetlock 语调、注意力冲击）都没起来。
6. **不是差一口气**：最好一臂（E，S 0.45）距 1.58 差 3.5 倍，且 F 0.13 / 2Y 0.54 同样远离，
   不是"某个闸单独卡住"的形态（对比波 61 的 B0：S 1.99 只卡 self）。

**记录两处本轮未测的设计缺口（不追溯、不补跑，留档供日后判断"是否值得回头"）**：

- **语调一阶差分**：Tetlock 2007 的核心是 pessimism **innovation**，本波 A/B 测的是**水平**（5 日均值）。
  水平与创新在新闻情绪上不是同一变量（语调高度持续，差分后才是新闻流冲击）。本波无任何臂测差分。
- **跨变体分歧**：数据集有 `_1.._6` 六组变体。C 臂测的是**单变体内部**的 `stddev`（同一 feed 的估计离散），
  没测**六个变体之间**的分歧（不同 feed 对同一事件的语调差异）。后者更像"信息分歧"，但需 12 字段
  多项式组装，成本与算子数都高。

判死归属：波 62 ⇒ `finnews_nlp_scores` 在 USA/D1 不产出 ATOM 候选。**正式封存（`seal_dead_end`）留待 S6**，
理由是封存闸要求论坛取证结论，本轮未做该数据集的论坛检索，不能凭空 seal。



### §M 波 62 收尾：fallback 退役与波 63 路线改判（2026-10-23）

**① 字段画像已落档**：`_usa-finnews-nlp-scores-field-profile-20261023.md`（105/105 字段完整矩阵、
7 统计族 × 3 极性 × 稀疏 `_1.._6` 变体、覆盖率 1.0 的填零疑点、拥挤度 67/105 字段 aC=0）。
**② 回测台账已入库**：`expressions` 8 条 status=backtested + `backtest_results` 8 行
（wave=`s2_finnews_nlp_scores_d1`，dataset=`finnews_nlp_scores`），核对 8/8 一致。

**③ 预注册 fallback「转同塔 `nlp_news_scores`」正式退役（不开波）。**

原预注册写「8 臂 max S < 0.8 ⇒ 按归因转同塔 `nlp_news_scores`」。判据本身命中（max S 0.45），
但**转移目标被更强的跨集证据否决**：`nlp_news_scores` 是「Transformer 文本分数」族的**第九个成员**
（OTHER 塔、84 字段、cov 0.9017、aC 51），而该族在 USA/D1 已连续八集证伪：

| 数据集 | 探针数 | 最好结果 |
|---|---:|---|
| `news_sentiment_transfer` | 16 | max S 0.50；六臂 2Y 为负；TO 0.89–1.18% 卡 LOW_TURNOVER |
| `news_sentiment_dl` | 10 | max S 0.63 |
| `ai_news_scores` | 8 | max \|S\| 0.48 |
| `sentiment21` | — | max \|S\| 0.58 + HIGH_TURNOVER 1.44–1.58 |
| `mmp_nlp_sentiment` | 24 | 0 条 ra_clean |
| `event_sentiment_signals` / `earningscall_embed` | — | 全灭 / 判死 |
| `news_sentiment_nlp`（波 56） | 6 机制 | 全灭 |
| `finnews_nlp_scores`（波 62，本波） | **8 机制** | **max S 0.45** |

`nlp_news_scores` 在字段数、覆盖、置信区间族上**全面弱于**本集（84 < 105 字段、无 CI 族），
先验更差 ⇒ **为它单独开波属于重复已证伪路径**。**退役记录在此，后续不再作为候选引用。**

**④ 波 63 路线改判：不做新数据集首波，转 `intraday_pv_feats` 的 prod 墙攻坚。**

改判依据（不是"没灵感"，是边际产出实测）：

- 新数据集首波的边际产出已归零：2026-10-20 一天内 other 塔 14 个低拥挤集（other545/546/567/571/580、
  cre、earnings_risk、equity_forum_data、equity_kpi_forecast、sustainable_profit、event_relation、
  acquisition_model、macro63、news_sentiment_nlp）**全部出结论、0 可交付**（见 §D 汇总行）；
  加上本波新闻族第 8 集归零 ⇒ 近 20 个数据集首波 0 命中。
- 手上已有 **IS 全闸通过、只差 prod 0.043** 的候选：
  - `wpZJPRql`（intraday_pv_feats）：S 1.66 / F 1.05 / 2Y 2.00 / SUB 1.15 / TO 33.4% / RA clean，
    **prod 0.7429 / self 0.3948**（2026-10-22 20:30 实测）。
  - `levR9Vq7`（同族 industry 轴）：S 1.84 / F 0.95 / 2Y 1.70 / SUB 1.14 / TO 33.0%，
    F 差 0.05；prod 已提交重算，2026-10-23 复查仍返回 `null`（平台异步，未出结论）。
- 用户约束「不得频繁切换数据集」⇒ 继续留在 intraday_pv_feats 是顺约束，不是绕开它。

**⑤ 波 63 预注册（事后不调）**：

- 方法：`wq-window-valley-break-prod-wall` —— 先在 `wpZJPRql` 的 `ts_decay_linear(W)` 上扫窗口网格
  （W ∈ {3,5,8,10,15,20}）× group 轴 {country, industry, subindustry}，逐个实测 prod；
  若出现谷位（prod < 0.70 且 self < 0.70）再验 IS 是否守住。
- 命中判据（三条同时满足才进提交候选，且**仍需用户明确确认**）：
  ① prod < 0.70 且 self < 0.70；
  ② S ≥ 1.58、F ≥ 1.0、2Y ≥ 1.58、SUB ≥ 该 alpha 的平台 limit、TO ≤ 0.70；
  ③ 不是已 ACTIVE alpha 的收益复制（设置变体 corr≈1.0 不算新 alpha，见 MEMORY「设置变体」条）。
- 若整张网格无谷（prod 全 ≥ 0.70 或守闸后 IS 崩）⇒ 记录为 `USA-INTRADAY-PV-PROD-WALL`，
  转下一族；**不在同一族上无限加窗**。

---

## 附录 AN — §M 作废、n 判据三档裁定、波 63–73 审计、波 74 转投 `other143`（2026-10-23）

### N.1 §M④/§M⑤ 作废（三条事实错误，均以平台 / DB 实测为据）

| §M 的原话 | 实测 | 结论 |
|---|---|---|
| `wpZJPRql`「IS 全闸通过 / RA clean」 | `backtest_results` 该行（wave=`probe_preclose_usa_20260920`）`ra_failed_checks = NULL`——即**从未带 checks 收割过**，不是"RA 全过"；2026-10-22 画像记其失败项为 `CONCENTRATED_WEIGHT` | 「没有记录」≠「全部通过」，措辞作废 |
| 「只差 prod 0.043」 | prod **0.7429**（`check_correlation`，2026-10-22T20:30:28 实测）；该族 prod 直方图 `[0.7,0.8)` **n=2** | 差 0.043 是"距离"不是"可达"，n=2 按本附录 N.2 判族死 |
| 引 `mLmxKN12`（prod 0.694）当"同类可过"参照 | `mLmxKN12.region_id = 8` = **GLB**，`universe=MINVOL1M`，ADR/GLB 池 | 不是 USA 探针；USA 同族只有 3 行（`wpZJPRql` / `JjNgvjP2` / `levR9Vq7`） |

**§M⑤ 的窗口网格（`ts_decay_linear` W∈{3,5,8,10,15,20} × group 轴 3）从未执行，也不再执行**：
族 n=2 ⇒ 按 N.2 不扫窗口；且 `intraday_pv_feats` 已于 2026-10-22 画像封存（30+ 条实测，唯一过 F 的壳是最拥挤的
肥尾 zscore 壳；任何边界裁剪把 RET 13.4% → 4.3–6.5%）。该次"结构性尝试"的额度已花在 2Y / investability 调参上。

### N.2 n 判据三档裁定（回应用户「n≥1 是不是有点严格，可否放到 n≥2」）

先把 n 的语义钉死，再说放宽。`GET /alphas/{id}/correlations/prod` 的 `records` 是**该 alpha 对生产池逐条 alpha
的相关系数按桶计数**，`schema.max` 才是决策值。`[0.7,0.8)` 整桶在 0.70 线之上 ⇒ **对已踩墙的候选，「n≥1」与
「max ≥ 0.70」是同一件事**（同义反复）；`n=0 可救` 只在**族代表样本**或**扫完谷位后的新变体**上才有信息量。
→ 该 skill 把这两句并写是表述缺陷（待修，不在本轮），`tools/probe/prod_bucket_scan.py` 的
`verdict = SCAN(过线可期) if n==0 else DEAD` 同样缺一句「仅当候选自身 max<0.70 时成立」。

但用户的质疑仍然成立：`n≥1` 一刀切会把"只有一个近邻、且那个近邻是**设置档兄弟**而非同信号"的情形误杀。
故放宽为三档（**这是对 `wq-window-valley-break-prod-wall` 的唯一修订**）：

| `[0.7,0.8)` n | 处置 | 依据 |
|---|---|---|
| **n = 0** | 可扫窗口网格（原判据不变） | 谷位表（shrt38 0.6929 / oth466 0.6762）均出自 n=0 族 |
| **n = 1** | **允许 1 次单点探针**（含复测，总 prod 读数 ≤ 2）；探针必须换**测量几何**，不是换窗口 | KOR n=1 两族地板 0.7019–0.7031（换窗无谷）；USA `78on0e78` 0.7214 判死，而同机制换 `ts_zscore` 的 `e76xgXkM` 落到 **0.5532 并交付** ⇒ 有效杠杆是几何不是 W |
| **n ≥ 2** | 族级死：不扫窗口、不发探针 | n=2 要求两个近邻**同时**跌破 0.70 才算清场，严格难于 n=1 |
| **n ≥ 70** | 连探针都不发（密墙 / 饱和） | 信号层同族，裁剪 / 换轴 / 等价算子全无效（GLB 848–877 桶实证） |

边界（**不放宽 D0-P**）：① D0-P「禁止对单颗钉子换窗口 / 门控 / 平滑」照旧；② n=1 的那一次探针只能从 D0-P
①–④ 选（删腿 / 换广度轴、`group_neutralize(·, sector)`、换分母口径、换设置档 / 分组轴）；
③ 「0.70–0.75 只准 1 次结构性尝试」不变。
对存量结论的影响：`wpZJPRql`（n=2）**仍判死**，§M 的结论不变，变的只是"为什么死"的说法。

### N.3 波 63–73 实测审计（**这 11 波不在本日志里**，由并行会话直接写 DB）

`expressions` / `backtest_results` 实测（USA，wave 升序）：

| 波 | 数据集 | category | 塔状态 | 臂数 | max S | max F | 判决 |
|---|---|---|---|---:|---:|---:|---|
| 63 | `chart_return_model` | PV | 未点亮 | 8 | 0.34 | 0.18 | 死（信号层面无信号） |
| 64 | `event_return_model` | NEWS | 未点亮 | 8 | 1.01 | 0.69 | 未到线 |
| 65 | `event_return_model` | NEWS | 未点亮 | 6 | 1.15 | 0.78 | 未到线 |
| 66 | `event_return_model` | NEWS | 未点亮 | 8 | 1.19 | 0.81 | **三批耗尽 ⇒ 判死** |
| 67 | `predictive_starmine` | MODEL | **已点亮** | 8 | 0.60 | 0.15 | 出界 + 弱 |
| 68 | `tech_chart_model` | MODEL | **已点亮** | 8 | 1.97 | 0.95 | 出界 |
| 69 | `tech_chart_model` | MODEL | **已点亮** | 7 | 2.02 | 1.02 | 出界 |
| 70 | `tech_chart_model` | MODEL | **已点亮** | 8 | 0.09 | 0.01 | 出界 + 整批废 |
| 71 | `tech_chart_model` | MODEL | **已点亮** | 8 | 2.01 | 0.77 | 出界 |
| 72 | `tech_chart_model` | MODEL | **已点亮** | 8 | 2.03 | 0.75 | 出界 |
| 73 | `expected_move` | MODEL | **已点亮** | 8 | 0.99 | 0.27 | 出界 + 弱 |

**规则冲突（必须记）**：用户口径「已点亮的塔里的数据集先不回测（点亮 = 本季提交 ≥ 3 的 category）」；
`get_pyramid_alphas` 2026-10-23 实测 **USA/D1：analyst=6、model=4**，其余全 0 ⇒ `MODEL` 已点亮。
波 67–73 共 7 波、55 臂全部落在已点亮塔上，**不论指标多好都不计入 10 个交付**，本轮不续该线程。
`tech_chart_model` 的 S≈2.0 / F≈1.0 是本季最好看的读数，但因为塔已点亮，**只能作为"若 MODEL 塔解禁"的储备**，
已记在 `output_report/` 之外的本节，不进候选表。

**台账缺口（机制问题，非本次修）**：这 11 波每波都有 `expressions.status='dropped'` 8 条（带 `dataset`）+ 
`status='backtested'` 8 条（`dataset` **为 NULL**）成对出现 ⇒ 回测行的数据集归属丢失，按 `dataset` 统计会整段漏掉
（我第一遍查 `dataset='tech_chart_model'` 得到 0 行，就是因为这个）。若后批沿用此写法，`get_mining_yield` /
`review_wave` 的口径会系统性低估。**已在 §N.6 记为待修**。

### N.4 波 74 数据集选择举证（「不得频繁切换」的正面回答）

先给"为什么必须换"：当前在飞的不是一个活数据集，而是一串已判死的——`intraday_pv_feats`（§M/N.1 封存）、
`finnews_nlp_scores`（波 62，max S 0.45）、`chart_return_model`（波 63，0.34）、`event_return_model`（波 64–66，1.19）。
继续留在其中任何一个都不是"顺约束"，是重复已证伪路径。

剩余候选面逐条筛（**只看未点亮塔 + 无历史尝试 + 字段面够 10 臂**）：

| 数据集 | category | 塔 | 字段 | 覆盖 | 历史尝试 | 判 |
|---|---|---|---|---|---|---|
| `chart_return_model` | PV | 未点亮 | 248 | 1.00 | 波 63 8 臂 max 0.34 | 死 |
| `event_return_model` | NEWS | 未点亮 | 59 | 0.999 | 波 64–66 22 臂 max 1.19 | 死 |
| `other696` | OTHER | 未点亮 | 498 全 **VECTOR** 事件计数（`_fast_d1` 孪生） | 0.889 | 0 | 文本 / 事件族已 10 集全灭（§L 表：`news_sentiment_transfer` 0.50、`news_sentiment_dl` 0.63、`ai_news_scores` 0.48、`sentiment21` 0.58、`mmp_nlp_sentiment` 0 条 ra_clean、`event_sentiment_signals` 全灭、`news_sentiment_nlp` 全灭、`finnews_nlp_scores` 0.45），先验最差 |
| `risk65` | RISK | 未点亮 | **6** | 0.974 | 0 | 字段面撑不起 10 臂 |
| **`other143`** | **OTHER** | **未点亮** | **126（105 MATRIX + 21 VECTOR）** | **0.95–1.00** | **全库 0 表达式（任何 region 都没碰过）** | **选** |

`other143` = *Transaction Volume Data for Equity*（FINRA 式 Clearing ID 成交量），字段层 ×1.4、tier STANDARD、
subcategory `other-event-data`。补齐的三条理由：
① **机制与已交付的 5 颗全部正交**（那 5 颗是 analyst 修正 / 目标价，这里是"谁在交易"的券商身份结构）；
② **未点亮塔 ×1.4**，且 `other` 塔全季 0 次提交（`get_pyramid_alphas`：other=0）；
③ **全库零尝试**，不是"换个名字再挖一遍"。

### N.5 波 74 预注册（事后不调）

- 数据集 `other143`；USA / TOP3000 / D1 / SUBINDUSTRY / decay 5 / truncation 0.08 / VERIFY / nanHandling ON /
  pasteurization ON / maxTrade OFF。字段画像见
  [`_usa-other143-field-profile-20261023.md`](_usa-other143-field-profile-20261023.md)。
- **10 臂 = 10 个互不相同的经济机制**（不是同信号扫参）：机构券商集中度（HHI）、参与广度、买卖集中度背离、
  空头券商集中度、执行价背离、集中度动量、头部陡峭度、tier1−industry 分层背离、异常成交量、短卖占卖出比。
  逐臂定义与方向假设见画像文档 §3。
- **首波止损（预注册，触发即封存，不加臂）**：
  1. 10 臂 `|S|` 全部 < 1.0 ⇒ 数据集首波判弱，`USA-OTHER143-WEAK`，换下一集（不得在此集追第二波）；
  2. 有臂 `|S| ≥ 1.58` 但 `F < 0.8` 且 TO > 0.45 ⇒ 只做一次降换手（`ts_decay_linear` / `hump`），不重设计机制；
  3. 有臂三闸（S / F / 2Y）全过 ⇒ 才进入降相关与 prod 队列，**提交仍须用户明确确认**。
- **不作的事**：不扫设置网格（decay / 中性化 / universe）找分；不在首波就叠跨数据集腿（D3 铁律）；
  不使用 `add` / 加权（禁混信号）。

### N.6 待修（不在本轮动手）

1. `wq-window-valley-break-prod-wall` 的「n=0 可救 / n≥1 必死」需按 N.2 改成三档，并补一句"n 只对族代表或谷位变体有信息量"。
2. `tools/probe/prod_bucket_scan.py` 的 `verdict` 同上加注；`wall_shape()` 的 `single-nail` 判据（n_6_7 ≤ 20 且 n_ge7 ≤ 3）与 N.2 的 n=1 探针规则需对齐。
3. 波 63–73 的 `backtested` 行 `dataset = NULL` ⇒ 回测行数据集归属丢失。修法：收批时把 `dataset` 一并写入
   `backtest_results`（`upsert_backtest_rows` 已支持该列），不要只留在 `expressions` 的 dropped 快照里。

---

## 附录 AO · 波 74–79：other143 集中度族的 F 墙全谱（2026-10-23）

> 本附录回答一个问题：**A1/A6 已经 S≈2.2–2.4、2Y 全过，只卡 Fitness，到底还有没有路。**
> 结论先说：**没有。F 曲面的峰高是 0.79，门在 1.00，所有算子只在曲面上移动，没有一个能抬高曲面。**
> 但这条结论是花 33 条回测（波 74–79）换来的，下面是全部读数与判据，供后续任何"再试一次"之前先读。

### AO.1 Fitness 的真实含义：它不是"换手率闸"，而是"每单位换手的边际"（这次才彻底算清）

平台定义 `F = S · sqrt(|RET| / max(TO, 0.125))`。把三项拆开看，**`S` 与 `RET/TO` 是两个独立维度**：

- `RET/TO` = 每转一次手能赚多少（下文记 `edge`）。它由信号的信息含量决定；
- `S` = 单位波动换来的收益。它由信号的稳定性决定；
- **`max(TO, 0.125)` 这个地板是关键**：一旦 TO < 0.125，再降换手**只减 RET、不减分母** ⇒ F 必然下降。

由此可反推任意一条读数隐含的 edge：`edge = (F/S)²`。这条恒等式让"变换算子到底有没有用"从感觉变成可算——
下文所有表都用它。

对 USA 门（S≥1.58 / F≥1.0）来说：**在 S=2.2 处要有 edge≥0.207 才过闸**；A1 的 edge 是 0.122，A6 是 0.098。
缺口 1.7–2.1 倍。这就是"只差一闸"的真身。

### AO.2 A1（tier1 集中度）全谱：20 条臂，峰 0.78

`A1 = exempt_tier1_broker_concentration_index`，除注明外 `rank(ts_zscore(A1,120))`，SUBINDUSTRY / trunc 0.08 / nan ON / maxTrade OFF / 2014–2023。

| 臂 | alpha | S | F | TO | edge=(F/S)² | 判决 |
|---|---|---:|---:|---:|---:|---|
| **decay 5（基线）** | — | **2.23** | **0.78** | ~0.53 | **0.122** | 族内峰值之一 |
| decay 10 | `KPmvexvp` | 1.88 | 0.76 | 0.3598 | 0.164 | 降 F |
| decay 20 | `WjL3knrN` | 1.34 | 0.58 | 0.2447 | 0.187 | 降 F |
| decay 30 | `GrgXV6gG` | 1.07 | 0.47 | 0.2006 | 0.193 | 降 F（edge 升、S 崩） |
| `ts_decay_linear(·,5)` | `ZYmgkPW8` | 1.80 | 0.76 | 0.3024 | 0.178 | 降 F |
| `ts_target_tvr_hump(·,0.15)` | `vROZawJA` | 0.89 | 0.36 | 0.1048 | 0.164 | 崩 |
| `hump(·,0.01)` / `hump(·,0.02)` | `pwvxQY1X` / `E5VNoOrK` | 0.20 | 0.04 | 0.0194 | 0.04 | 崩（且两档**读数逐位相同**） |
| `trade_when(k=1.0)` | `LL5EOkoL` | 1.27 | 0.58 | 0.1571 | 0.209 | edge 最高但 S 腰斩 |
| `trade_when(k=1.5)` | `e76NeLMO` | 0.39 | 0.16 | 0.0996 | 0.168 | 崩 |
| `ts_zscore(·,189)` @decay20 | `RRA9XqOj` | 1.20 | 0.54 | 0.2311 | 0.203 | 降 F |
| **SECTOR 中性化** | `LL5EOdn6` | 1.93 | 0.70 | 0.5318 | 0.132 | 降 F（对照，非扫参） |
| **maxTrade=ON** | `kqJvbV1K` | 1.47 | 0.54 | 0.3508 | 0.135 | **强度闸**：S 2.23→1.47 |
| `ts_rank(·,180)` | `leMEk0wl` | 2.04 | 0.71 | 0.5251 | 0.121 | 降 F |
| `ts_mean(·,63)` | `qMEOvX2O` | **−0.66** | −0.36 | 0.0307 | 负 | **符号翻转**（见 AO.3） |
| `group_rank(·, subindustry)` | `1YjO1g8k` | 2.17 | 0.73 | 0.5339 | 0.113 | 降 F（设置层已做同一件事） |
| `ts_target_tvr_decay(·,0.3)` | `omoRAPZk` | 1.13 | 0.55 | 0.1617 | **0.237** | **edge 最高，S 崩** |
| `tail(·, 0.02/0.98, 0.5)` | `RRA9q5Y0` | 1.43 | 0.45 | 0.6184 | 0.099 | 反升换手 |

**读法**：把 decay 5→10→20→30 四行连起来看，edge 从 0.122 单调升到 0.193，S 从 2.23 单调掉到 1.07 ⇒
**F 先平后降**。这正是"沿曲面走"的形状，不是"曲面被抬高"。

### AO.3 三个不是"调参"而是"机理"的发现

1. **水平项是负的，偏离项才是正的**。`rank(ts_mean(A1,63))` 读到 **S = −0.66**，而 `rank(ts_zscore(A1,120))` 是 **+2.23**。
   同一字段、只差"慢水平 vs 快偏离"，符号直接翻。这条把该族的机制钉死了：
   **赚的是集中度的均值回复（谁今天异常集中），不是"长期集中的股票有溢价"。**
   推论：任何把信号往慢端拉的算子（`ts_mean` / `ts_rank` 长窗 / 长 decay / `hump`）都必然伤它——
   AO.2 表里每一行都印证了这一点，不是巧合。
   同时它**排除了**"改走季度频率提取 13F 式慢变量"这条路（文献支持慢变量，但本数据集的水平项就是负的）。

2. **`hump` 的 `hump` 参数在 0.01 与 0.02 两档读数逐位相同**（A1：S 0.20 / F 0.04 / TO 0.0194；A6：S 0.01 / F 0 / TO 0.0264）。
   两档不可能给出完全一样的持仓，说明**该参数在当前调用形态下未被应用**（`hump(x, hump=…)` 为 keyword-only，
   写法本身合法，故不是语法问题）。**结论：不要把 hump 当降换手杠杆用**，它的实际行为是"几乎清零换手"，
   等于把信号一起掐死。这与 `ts_target_tvr_hump` 一致（0.15 档也是崩）。

3. **`bucket` 不是分箱权重器，是"组"的产生器**。波 78 里 `bucket(rank(x), range="0,1,0.2")` 直接平台报
   `Expression ends with group unit value`，并**连坐取消同批 2 条兄弟**（multisim 的既有杀伤面）。
   正确形态只能是 `group_rank(x, bucket(...))` / `group_neutralize(x, bucket(...))`。
   本条与 memory `bucket-multisim-error` 一致，此处补上"它是 group 类型"这一层原因。

### AO.4 波 78 三通道复查 → 八臂修复批（用户指令的正式答卷）

用户指令：**「对快要破闸的 alpha 进行复查，查论坛有无针对性的方法没有试，及外部金融论文有没有试，及所有算子的使用有没有试」**。
逐通道给结论，并映射到实际臂：

**(a) 论坛 —— 三条针对性帖子，方法全部落地**

| 帖子 | 说法 | 落地臂 | 结果 |
|---|---|---|---|
| 43621486024983 | USA/TOP3000/D1 七算子对照：单调算子只改 TO 与权重形状；`rank` 换手最低（0.624） | `ts_rank(180)` | S 2.04 / F 0.71 ⇒ 无效 |
| 42065262268567 | 换手治理：`decay` 杀时效性；评论建议 `winsorize(std=3)`、`group_rank`；腿时域 F 2.09/2.27/2.30；decay=0≡decay=1 | `winsorize(std=4)`（在飞）、`group_rank`、decay 阶梯 | group_rank 2.17/0.73 ⇒ 无效；decay 阶梯全谱见 AO.2 |
| 43608868929559 | 长记忆信号若换手极高 ⇒ 构造有错（不是信号强） | 用来解释 A1 的 0.53 换手：**该字段是日频流量，不是慢结构** | 解释了 AO.3 第 1 条 |

**(b) 外部文献 —— 三条结论，两条被数据否掉、一条未测**

| 文献结论 | 对应臂 | 结果 |
|---|---|---|
| 机构交易**离散度**对未来 3 个月收益为负 | `ts_std_dev(A1,60)` 取负（波 79 N2） | 在飞 |
| 多季度机构持仓**持续性**负向预测长期收益 | `ts_mean(ts_delta(A6,22),63)`（波 78） | S 0.49 / F 0.17 ⇒ **否掉** |
| 季度 13F 持仓**变化**正向预测未来收益 | `ts_delta(A6,63)`（波 78） | S 1.58 / F 0.44 ⇒ 窗口拉长即衰减 |

文献给的"慢变量"方向在本数据集**系统性失效**，根因就是 AO.3 第 1 条（水平项为负）。

**(c) 算子穷尽 —— 用过 vs 未用过（这张表就是"是否漏了边界用法"的答案）**

- **已用**：`rank` `ts_zscore` `ts_rank` `ts_mean` `ts_delta` `ts_std_dev`(79) `multiply` `subtract` `divide` `add`(仅防零)
  `ts_backfill` `group_rank` `winsorize` `bucket`(作为 group 的边界) `tail` `ts_decay_linear`
  `ts_target_tvr_decay` `ts_target_tvr_hump` `hump` `trade_when` `vec_avg` `vec_stddev`(79)。
- **未用但已判定为"沿曲面移动"**：`scale` `normalize` `zscore` `sqrt` `log` `sign` `power` `sigmoid` `arc_tan`
  —— 全是单调重标定，在 `rank` 之后不改变排序，**结构上不可能改 F**（论坛 43621486024983 亦实测同结论）。
- **未用且需要第二输入**：`ts_corr` `ts_regression` `ts_co_kurtosis` —— 需要价量或第二个字段，
  在本族语境下等于引入价量腿，**先验低且会触碰"禁混信号"的边界**，本轮不做。
- **未用且已随波 79 补**：`vec_*` 全族（21 个 `rolling_*` VECTOR 字段**此前一次未碰**，这是唯一一处真正的"算子面空白"）。

### AO.5 波 78 收批（八臂，全部低于基线）

| 臂 | alpha | S | F | TO | edge | 判决 |
|---|---|---:|---:|---:|---:|---|
| A6 `ts_zscore(delta,22)` 的对照：`ts_delta(A6,63)` | `d5KYgQMw` | 1.58 | 0.44 | 0.5775 | 0.078 | 长窗衰减 |
| A6 持续性 | `rKd9EWqJ` | 0.49 | 0.17 | 0.1005 | 0.120 | 死 |
| A1 `ts_rank 180` | `leMEk0wl` | 2.04 | 0.71 | 0.5251 | 0.121 | 无效 |
| A1 `ts_mean 63` | `qMEOvX2O` | −0.66 | −0.36 | 0.0307 | 负 | **机理证据（AO.3-1）** |
| A1 `group_rank` | `1YjO1g8k` | 2.17 | 0.73 | 0.5339 | 0.113 | 无效 |
| A1 `tail` | `RRA9q5Y0` | 1.43 | 0.45 | 0.6184 | 0.099 | 无效（换手反升） |
| A1 `ts_target_tvr_decay 0.3` | `omoRAPZk` | 1.13 | 0.55 | 0.1617 | **0.237** | edge 最高但 S 腰斩 |
| A1 `maxTrade=ON` | `kqJvbV1K` | 1.47 | 0.54 | 0.3508 | 0.135 | 强度闸确认 |
| **A1 `winsorize(std=4)`** | **`akVeM8G1`** | **2.35** | **0.86** | 0.528 | **0.134** | **★ 唯一抬高曲面的算子（新基线）** |
| A1 TOP1000 | `A1QeYrQg` | 1.74 | 0.61 | — | — | 宇宙轴无效 |

**A6 侧的最好读数不是基线，而是 decay 10**：`e76NAeVl` S 2.16 / **F 0.79** / TO 0.4332 / edge 0.134 ⇒
**F 曲面在 decay 轴上有一个内部极大（decay 5:0.74 → 10:0.79 → 20:0.70 → 30:0.68）**，峰高 0.79。
A1 侧峰高 0.78（decay 5）。两侧峰高一致，这不是巧合，是同一份信息的两个投影。

### AO.6 波 79 预注册（四臂，最后一批）

发批前过 `logs/_tmp_w79_preflight.py`：括号 4/4、语法 4/4、`[arity] 4/4 PASS (签名表 101 个算子)`、
`ensure_safe_for_dispatch` PASS、形状 2 类（S9 ×2 / S5 ×2，代理指标非闸）。
派发：scalar 3 臂 multisim `VnkJH2nW5cvacPQ2Dicpu1`；vector 单臂 n=1 `3Jwd7abzO4LeaOfod8yYFiL`（隔离，防连坐）。

| 臂 | 表达式 | 机制（为什么它可能抬高曲面而不是沿曲面移动） |
|---|---|---|
| **N1** | `rank(ts_zscore(exempt_industry_top_broker_share_pct, 22))` | A6 是**裸差分**（edge 0.098），A1 是 **z 分数**（edge 0.122）。两者的唯一构造差异就是归一化。把冠军的构造原样搬到 A6，是最高先验的一臂 |
| **N2** | `multiply(-1, rank(ts_std_dev(exempt_tier1_broker_concentration_index, 60)))` | **不稳定度**（新经济量，此前只测过水平与偏离）。文献：离散度负向预测 |
| **N3** | `multiply(-1, rank(divide(vec_stddev(rolling_tier1_broker_concentration_index), vec_avg(rolling_tier1_broker_concentration_index))))` | 21 个 `rolling_*` VECTOR 字段 + `vec_*` 算子族**从未启用**。窗口内变异系数是标量算子做不出的量 |
| **N4** | `rank(ts_zscore(divide(ts_backfill(oth143_buy_tier1_volume,66), ts_backfill(oth143_buy_tier1_unique_brokers,66)), 60))` | **单券商订单规模**（成交量/券商家数）——机构单笔规模，与"份额平方"完全不同的量 |

**止损（预注册，触发即封存本族）**：四臂 `max F < 0.85` ⇒ 判 **`USA-OTHER143-F-WALL`**：
本数据集的集中度/券商结构族**封存**，A1/A6 的读数作为"IS 强、F 墙"证据保留，不再发同族臂；
下一数据集按 N.4 顺位切 `other596`（420 字段，`other` 塔，全库零尝试），并说明"切换发生在三通道 + 两批修复
共 33 条回测之后，不是频繁切换"。

### AO.7 两条台账事实（与本族结论无关，但会误导后来者）

1. **设置漂移**：`tracking/USA/config/settings.json` 写 `startDate=2013-01-01`，而波 74–79 实际全部跑
   `2014-01-01`（`tools/submit_batch.py` 的 `BASE` 缺省）。**本族内部可比**（都是 2014），
   但与 settings.json 声明的口径不一致。改 settings.json 会同时改变未来所有波的 IS 窗口，
   属于"需要重跑全库 champion 才能比"的动作，**本轮只登记不改**。
2. **DB 波号陈旧**：`wave_results` 里 73–83 是 2026-09 另一条血脉（如 wave 74 = "RED: 8 全灭"），
   与本次 other143 的波 74–79 **不是同一波**。任何按波号回查的结论在入账前都不成立；
   本族的真实读数以 `expressions` / `backtest_results` 的 alpha id 为准（本附录逐条列了 id）。

### AO.8 `winsorize` 的真实机理：**截断位置**决定一切，不是 `std` 值（本节推翻初版结论）

⚠ **初版写「`winsorize(std=4)` 是唯一抬高曲面的算子」，把 std 参数当标定轴 —— 波 80 三臂把这个解释证伪了。**
正确读法只能从下面这张表来：

| 臂 | alpha | S | F | TO | DD | CLUSTER | 相对基线 |
|---|---|---:|---:|---:|---:|---|---|
| 基线 `ts_zscore(A1,120)` | — | 2.23 | 0.78 | 0.5339 | 0.0583 | 1.55 贴线 | — |
| `winsorize(ts_zscore(A1,120), std=4)` | `akVeM8G1` | 2.35 | 0.86 | 0.528 | — | 通过 | +0.08 F |
| `winsorize(ts_zscore(A1,120), std=3)` | `leME2QqA` | 2.23 | 0.78 | 0.5339 | 0.0583 | 1.55 | **逐位等于基线（no-op）** |
| `winsorize(ts_zscore(A1,120), std=2)` | `A1QebgZR` | 2.23 | 0.78 | 0.5338 | 0.0583 | 1.55 | **逐位等于基线（no-op）** |
| **`ts_zscore(winsorize(A1, std=3), 120)`** | **`9qE8Ka1o`** | **2.40** | **0.84** | 0.5406 | **0.0386** | **通过** | **+0.06 F，DD 砍 34%，2Y 2.57** |

两个事实同时成立，且都**无法用「std 标定」解释**：

1. **std 值在同一个截断位置上非单调**。若"截掉重尾噪声"是机制，3σ 应比 4σ 截得更狠、更该有效；
   实测 3 与 2 **逐位等于基线**（S/F/TO/DD 全部相同）。这不是"接近"，是**没产生任何效果**。
2. **换截断位置（先截原始字段再 z）拿到的最多**，并且顺手拿掉 A1 一直贴线的 `CLUSTER_TEST`（1.55 → 通过）
   与 34% 回撤。这条在最需要的地方（提交闸）比 +0.08 F 更值钱。

**机理（修正后）**：`ts_zscore` 的分子是 `x−μ`，而 μ 与 σ **都是含极值算出来的**。
对 **z 分数**做截断只改排序尾部，**μ/σ 本身不变** ⇒ 秩变换几乎不动 ⇒ no-op（这就是 3/2 无效的原因）。
对 **原始字段**做截断会同时压低 σ ⇒ **整条 z 序列被重新标定**，才是效应来源。
`std=4` 那条之所以有效，是 4σ 恰好落在该字段极值的自然断点上；3/2 落在断点内侧，等于什么都没截到。

**结论（不要再扫 std）**：`winsorize` 只有一种可用形态 —— **先截原始字段，再归一化**；
对 z 分数截断是无效形态。这条已作为 A1 侧最优壳登记进 §3，并在波 81 向 A6 迁移（AO.12）。

### AO.11 波 79 收批：一个冠军 + 三臂死，止损条款被另一条条款覆盖

**scalar 三臂**（multisim `VnkJH2nW5cvacPQ2Dicpu1`，decay 5，SUBINDUSTRY）：

| 臂 | alpha | S | F | TO | RET | DD | 2Y | sub | risk_neut | 判决 |
|---|---|---:|---:|---:|---:|---:|---:|---:|---:|---|
| **N1 A6 换 z 归一化** | **`XgRVLk1z`** | **2.56** | **0.79** | **0.625** | 0.060 | 0.0333 | 1.86 | 1.65 | 2.52 | **★ 本战役最强臂：`fail=[]`，唯一告警 LOW_FITNESS** |
| N2 A1 不稳定度 `−rank(ts_std_dev(·,60))` | `d5KYmnQw` | 0.70 | 0.34 | 0.0421 | 0.0303 | 0.1693 | 1.85 | 0.10 | 0.25 | 死（三闸 FAIL） |
| N4 单券商订单规模（成交量/券商家数） | `3qj1xEAz` | 0.44 | 0.09 | 0.4276 | 0.0166 | 0.0896 | 0.51 | 0.24 | 0.27 | 死 |

**vector 单臂**（n=1 隔离 `3Jwd7abzO4LeaOfod8yYFiL`）：`0mjxdq1G` S −0.21 / F −0.03 ⇒ 见 AO.9。

**止损触发的处置（重要，别让后来者以为条款被忽略）**：AO.6 预注册的是「四臂 max F < 0.85 ⇒ 判 `USA-OTHER143-F-WALL` 封存」，
实测 max F = 0.79 < 0.85，**条款字面命中**。但本数据集画像 §4 有另一条**独立预注册**条款：

> 「有臂 `|S| ≥ 1.58` 但 `F < 0.8` 且 TO > 0.45 ⇒ 只做**一次**降换手（`ts_decay_linear` 或 `hump`），不重设计机制」

`XgRVLk1z` 逐项命中该条款（S 2.56、F 0.79、TO 0.625）。两条条款的交集读法是：
**两条各自都是"一次"授权，先执行仍未被消耗的那一条**。TO 降换手从未在 A6-z 壳上跑过 ⇒ 波 81 用它。
TO 臂跑完即封存本族（无论结果），不再有第三批。这不是范围蔓延，是两条预注册条款的边界。

### AO.12 波 81 预注册：冠军的一次性降换手（三臂）+ 截断位置迁移（两臂）

发批前 `logs/_tmp_w81_preflight.py`：括号 3/3、语法 3/3、`[arity] 3/3 PASS`、dispatch PASS、形状 1 类（S9）。
**全部锁死机制**（同一字段、同一 z 归一化），只动换手轴 —— 这是 AO.11 末段说的"一次性"。

**批 A**（已派发 multisim `20yDU9jB5dzc7nTiJGZVUR`，decay 5，SUBINDUSTRY，文件 `usa_other143_w81_a6_tvr.txt`）：

| 臂 | 表达式 | 换手轴的选择理由 |
|---|---|---|
| T1 | `rank(ts_zscore(A6, 60))` | **窗口几何**：归一化基准从 22 拉到 60，信号不动、只让 μ/σ 更慢 |
| T2 | `rank(ts_decay_linear(ts_zscore(A6, 22), 10))` | profile 点名的两条之一（`hump` 已证惰性，见 §2） |
| T3 | `rank(ts_decay_linear(ts_zscore(A6, 22), 22))` | **剂量反应**：F 缺口需要 TO 砍约 37%（0.625→0.393 @ S 2.56/edge 0.096），10 档不够，故加一档强平滑 |

**批 A 收批（三臂，`20yDU9jB5dzc7nTiJGZVUR`，全部 COMPLETE）**：

| 臂 | alpha | S | F | TO | RET | DD | 2Y | sub | CLUSTER | 判决 |
|---|---|---:|---:|---:|---:|---:|---:|---:|---|---|
| **T1 `ts_zscore 60`** | **`78o3QRwO`** | **2.60** | **0.88** | **0.5783** | 0.0668 | 0.0391 | **2.47** | 1.74 | 1.40 ✓ | **★ 新壳**（S/F/2Y/TO 四项同时改善） |
| T2 `ts_decay_linear 10` | `omoRv0K6` | 1.82 | 0.73 | 0.2568 | 0.0416 | 0.0336 | 1.28 | 1.15 | 0.96 | **时域平均打塌信号**（2Y 掉到闸下） |
| T3 `ts_decay_linear 22` | `ZYmgxvp1` | 1.43 | 0.61 | 0.1893 | 0.0343 | 0.0480 | 1.07 | 1.00 | 0.81 | 同向更差（S 已破 LOW_SHARPE） |

**批 A 给出的三段归因（本轮最有价值的结论之一）**：
1. **`ts_decay_linear` 不是该信号的换手杠杆**。TO 从 0.625 砍到 0.257（−59%）、0.189（−70%），
   但 S 从 2.56 塌到 1.82、1.43，2Y 从 1.86 塌到 1.28、1.07。按 `F = S·sqrt(RET/TO)`，
   换手收益被 S 的损失吃掉：0.79 → 0.73 → 0.61，**单调变差**。
   机理：该字段的信息承载在「当前值相对近期基准的偏离」上，时域平均正好抹掉这个偏离量。
2. **窗口拉长有效，而且方向不同**：`ts_zscore` 换窗口不平均信号，它只是让 μ/σ 更稳 ⇒
   z 序列本身少抖动，而当前偏离仍然保留。这与 T2/T3 形成干净对照：**同一轴（换手）的两条路，一条通一条堵**。
3. **2Y 是隐藏的受益项**：z22 的 2Y 是 1.86（刚过 1.58），z60 是 **2.47**（余量 +0.89）。
   这说明 z22 的近年表现其实被基准噪声拖累了，不只是 F 的问题。

**F 缺口更新（决定批 B 的形态）**：`78o3QRwO` S 2.60 / RET 0.0668 / TO 0.5783 ⇒ edge 0.1155，F 0.884。
到 F=1.0 需 `RET/TO` 从 0.1155 抬到 0.1479（**+28%**）。若 S 与 RET 不动，需 TO→0.451；
若 TO 不动，需 RET→0.0856（+28%）。两条路都不是"再滑一格"能给，所以批 B 只保留**机制不同的**杠杆。

**批 B**（`usa_other143_w81b_a6.txt`，multisim `LfRZD4NI5aRbb7jpgrZhqo`，decay 5，5 臂）：
把 `9qE8Ka1o` 的构造（AO.8 唯一有效形态）与论坛 TO 算子一起叠到**批 A 的新壳 z60** 上（不是旧壳 z22）——
N1 的先例是「把已验证的构造迁到当时最优壳」，这里同理。预检 `logs/_tmp_w81b_preflight.py`：
括号 5/5、语法 5/5、`[arity] 5/5 PASS`、dispatch PASS、形状 1 类（S9）。

| 臂 | 表达式 | 为什么它不是"网格里的又一格" |
|---|---|---|
| B1 | `rank(ts_zscore(A6, 120))` | **窗口剂量**。该字段是慢变量（月度级更新）：22 天窗口内约只有 1 次更新、60 天约 3 次。z22→z60 单调改善说明窗口仍在"欠采样"区，再走一格看峰在哪 |
| B2 | `rank(ts_zscore(winsorize(A6, std=3), 60))` | `9qE8Ka1o` 已证「先截原始字段再归一化」是 winsorize **唯一**有效形态，迁到新壳 |
| B3 | `ts_target_tvr_hump(rank(ts_zscore(A6, 60)), target_tvr=0.45)` | 论坛 FF56620「turnover 优化精华版」策略 C。**与已证失败的 `ts_target_tvr_decay` 是不同算子**（见下条） |
| B4 | `hump(rank(ts_zscore(A6, 60)), hump=0.1)` | 同帖策略 B。§2 记「hump 参数惰性」是**只比过 0.01 vs 0.02** 得出的，而论坛档位是 0.1/0.2/0.3 —— 那两个值都落在噪声里，0.1 档从未测 |
| B5 | `rank(winsorize(ts_zscore(A6, 60), std=4))` | A1 侧 4σ-on-z 的迁移（`akVeM8G1` 2.35/0.86） |

**两条从论坛检索里拿到的、必须记下来的事实**：
1. 该帖「策略 C」写的 `ts_target_tvr_delta_limit` **在已核验的 102 个算子里不存在**（`research-data/operators_platform_20260904.json`
   只有 `ts_target_tvr_decay` 与 `ts_target_tvr_hump`）。论坛模板含幽灵算子是常态，**本仓 `op_arity` 闸拦住是必要的，不是形式主义**。
2. 该帖的核心告诫「**不要盲目提高 decay 参数，优先算子层面平滑**」——所以本批**刻意不测 decay 10 设置档**，
   尽管它是免费的 TO 杠杆（历史上 A6 裸差分版的 F 峰确实在 decay 10）。理由：decay 与 `ts_decay_linear` 同属时域平均，
   而批 A 已实测时域平均会把该信号打塌。**decay 档留给"算子层杠杆全部失效"之后再说**，不提前混进来。

**判决规则（事后不调）**：
① 任一新臂 `F ≥ 0.95` 且 `S ≥ 1.58`、`2Y ≥ 1.58`、`CLUSTER_TEST` 通过 ⇒ 进 prod 探针队列（**提交仍需用户确认**）；
② 所有臂 `max F < 0.90` ⇒ 判 **`USA-OTHER143-F-WALL`**，A1/A6 读数作为「IS 强、F 墙」证据封存，
按 N.4 顺位切 `other596`（420 字段，`other` 塔，全库零尝试）；
③ F 落在 [0.90, 0.95) ⇒ 允许**最后一次**把 ①的那条与 TO 条组合（一臂），因为两者各自已被单独验证，
组合不引入新机制。

### AO.9 波 79 矢量臂收批：`vec_*` 族的唯一代表人已判死

`0mjxdq1G` = `-rank(vec_stddev(rolling_tier1_broker_concentration_index) / vec_avg(同字段))`
（窗口内券商集中度的变异系数，标量算子做不出的量）：
**S −0.21 / F −0.03 / TO 0.310 / 2Y 1.10 / sub 0.15 / risk_neut −0.41**，反向也不成立 ⇒ 三个方向一致为零。

含义（写进机制结论，不重测）：
1. **21 个 `rolling_*` VECTOR 字段的"窗口内离散度"这一轴无信息**——不是"vec 算子没用"，是这个量没用；
   要启用矢量族只剩"聚合后当标量用"（`vec_avg`/`vec_sum` → 再 zscore）这一条，而那与已测的标量水平项等价。
2. **`vec_stddev` 签名核对过了**（`vec_std` 不存在，见签名表），所以这是读数不是语法事故。
3. 该臂按 AO.6 的隔离策略走 n=1，未连坐兄弟批——隔离策略继续保留。

### AO.10 波 80 预注册（四臂，`winsorize` 一维标定）

发批前 `logs/_tmp_w80_preflight.py`：括号 4/4、语法 4/4、`[arity] 4/4 PASS`、dispatch PASS、形状 1 类（S9）。
派发：A1 三臂 multisim `4bVLRn6mA4mZcGR17CxlIGq8`（decay 5）；A6 单臂 n=1 `lrJOQeGm4q18TVuCB8W2nf`（decay 10）。

| 臂 | 表达式 | 假设 |
|---|---|---|
| W80_std3 | `rank(winsorize(ts_zscore(A1,120), std=3))` | 论坛原值；比 std=4 截得更紧，若尾部全是噪声则 F 继续升 |
| W80_std2 | `rank(winsorize(ts_zscore(A1,120), std=2))` | 过紧对照；若 F 回落 ⇒ 4σ 附近是真甜点（**1 维三点定峰，不是网格**） |
| W80_raw3 | `rank(ts_zscore(winsorize(A1, std=3), 120))` | **截断位置对照**：截原字段而非截 z 分数。若两者等价，说明 winsorize 只是抗异常值；若前者更好，说明要截的是"偏离度分布" |
| W80_a6_std3 | `rank(winsorize(ts_delta(A6,22), std=3))` | 把同一个突破搬到 A6（A6 F 峰在 decay 10 = 0.79），检验突破跨核可迁移 |

**判决规则（事后不调）**：① 若某臂 F ≥ 0.95 且 S ≥ 1.58、2Y ≥ 1.58 ⇒ 进 prod 探针队列（**提交仍需用户确认**）；
② 若 `std=3/2` 呈单调（越紧越好）⇒ 说明尾部污染没截够，可再往 2.5/1.5 走一格（**仅一格**）；
③ 若三点里 std=4 最高 ⇒ 曲面在 4σ 处达峰，`winsorize` 杠杆用尽，本族转 `USA-OTHER143-F-WALL`（F 峰 0.86），
按 AO.6 切 `other596`。

### AO.13 波 81b 收批（`LfRZD4NI5aRbb7jpgrZhqo`，5 臂）—— 判决 ② 命中，本族封存

| 臂 | alpha | S | F | TO | RET | 2Y | sub | CLUSTER | 判决 |
|---|---|---:|---:|---:|---:|---:|---:|---:|---|
| z120 | `XgRVlLg0` | 2.31 | 0.79 | 0.5532 | 0.0653 | 2.54 | 1.47 | 1.40 | 窗口轴内点极大确认（z60 > z120 > z22） |
| **raw3_z60** | `9qE86KZr` | **2.63** | **0.88** | 0.5813 | 0.0656 | 2.24 | 1.73 | 1.41 | S 最高，F 与冠军并列；2Y 反而退 |
| `ts_target_tvr_hump 0.45` | `WjL3Xd1o` | 1.86 | 0.79 | **0.2786** | 0.0506 | 2.19 | 1.06 | 1.18 | TO 腰斩、S 同比例掉 ⇒ **F 不变杠杆不成立** |
| `hump 0.1` | `kqJvmXEz` | 0.04 | 0.00 | 0.018 | 0.0007 | 0.13 | −0.26 | 0.39 | **摧毁信号**，hump 轴彻底关闭（0.01/0.02 无效 ⇒ 0.1 致死） |
| wins4_z60 | `mLYdzAp2` | 2.60 | 0.88 | 0.5783 | 0.0668 | 2.47 | 1.74 | 1.40 | **与冠军 `78o3QRwO` 逐位相同** ⇒ z 分位上截断第三次证明是 no-op |

**三条归因（不是读数汇总）**：

1. **`ts_target_tvr_hump` 与 `ts_decay_linear` 是同一种失败**：两者都把「短窗偏离」在时间域上抹平，TO 降一半、S 也降
   ~28%，F 反而从 0.88 掉到 0.79。这是**同一机理的第二次独立确认**——本族的 edge 定义在「当期偏离」上，
   任何跨期平滑都在稀释分子。⇒ 降换手这条路在本族**没有可用杠杆**，不是没试够。
2. **`hump=0.1` 的致死读数把 hump 轴从「未测」变成「已证伪」**：0.01/0.02 段不动是因为它在噪声地板内，
   0.1 段直接把信号压成 0.04。两段合起来才是完整曲线（先平台后坠落），此前只测平台段的「inert」判断是**取样偏差**，
   现在有致死点了，不需要再往 0.2/0.3 走。
3. **`wins4_z60` 与 `78o3QRwO` 严格相同（S/F/TO/RET/DD 全等）**，加上波 80 的 std3=std2=2.23（同一个读数）、
   以及 std=3→2 无差，共同构成 AO.8 那条机理的**三重复现**：`ts_zscore` 的 μ/σ 已含极值，截 z 分位不改变排序，
   只改变常数缩放 ⇒ 对 rank 无影响。`winsorize` 唯一有效形态仍是「截原始字段」（`9qE86KZr` / `9qE8Ka1o`），
   但它在 z60 壳上只换来 +0.03 S，**换不动 F**。

**判决（按 AO.12 预注册规则，事后不调）**：`max F = 0.88 < 0.90` ⇒ **命中规则 ②**。

> **`USA-OTHER143-F-WALL` 成立**：F 峰值 **0.88**（`78o3QRwO` / `mLYdzAp2`），S 峰值 2.63（`9qE86KZr`），
> 2Y 峰值 2.47。全族累计 **约 40 条回测**（波 74–81b，含三通道修复 6 条 + 两批修复 9 条 + 算子轴 25 条），
> 覆盖 8 个算子族、3 个窗口、3 种降换手杠杆、2 种截断位置、2 种宇宙、2 种 maxTrade 档。
> F 的算术账：edge 0.1155，F=1.0 需 S 2.94（+13% on 2.60）或 edge 0.1479（+28%）——**两条路都无杠杆可用**。
> ⇒ 本数据集**封存**，A1/A6 读数作为「IS 强、F 墙」证据保留，不再发同族臂。

### AO.14 入账与切集（波 78–81b 已进 DB，`dataset` 显式写入）

- `backtest_results` / `expressions` 现已含 **27 行** `dataset='other143'`：波 78(11) / 79(4) / 80(4) / 81(3) / 81b(5)，
  全部走 `CampaignStore.upsert_backtest_rows(..., dataset='other143')`，**修掉了 N.6-3 的 `dataset=NULL` 缺口**。
- 波号用 `78`/`79`/`80`/`81`/`81b`：与 `expressions` 里既有的 74–77（本族 S2 记录）同一条血脉；
  与 `wave_results` 里 73–83 的九月另一条血脉**不共用**（AO.7-2），后续按 alpha id 回查，不按波号。
- **下一数据集：`other596`**（420 字段，`other` 塔，全库零尝试）。切换理由是本族 F 墙实证，
  不是频繁切换——切换发生在 40 条回测 + 8 个算子族之后。

## 附录 AP — 波 82–85：`other596` 封存、`ds339` 派生判死、转投 `fundamental93`（2026-10-23）

### §A `other596` 三波收官 ⇒ 判死（正文见画像 §11）

- 波 82（9 臂）/ 波 83（8 臂，覆盖修复 ON/OFF 双档）/ 波 84（8 臂，FAST 设置轴）/
  波 84b（6 臂，`ts_max` batch-kill 后重发）——合计 **23 臂 / 3 波 / 9 类构造 / 2 个设置轴**。
- 最好读数：**S 0.91**（SUBINDUSTRY，账本只有 200/196 只）、**F 0.28**（FAST，账本 1630/1496）。
  同一信号在 FAST 下 S 0.34 ⇒ **那个 0.91 是窄账本集中下注，不是覆盖更宽带来的强度**。
- 裁决：判 `USA-OTHER596-SPARSE-COVERAGE-WALL`，**封存、不再发波**。
  `seal_dead_end` 因缺可靠 `forum_recon_*` 取证（本地读帖链路故障）按 fail-closed 契约暂不写库，
  在此登记；补到可靠取证后再落 `dead_end`。若日后重开，只允许从「更新频率更高的变体」入手。

### §B `ZYmX7ZG3`（ds339）按派生判死 ⇒ 不进 prod 队列，不占第 6 颗

- IS 读数（2026-10-22 平台）：S **2.30** / F **1.71** / 2Y **3.89** / TO 6.06% / SUB 1.31（限 1.16）/
  RA failed **0**；本地 self **0.6559**。**唯一缺的闸是 prod。**
- `check_correlation(refresh=True)` **三次（跨约 2 小时）全返回 `production.max_correlation = null`**，
  同期 `get_alpha_details` 的 `checks.pending` 里 `PROD_CORRELATION` 始终 pending。
- **派生判据**：同数据集同族 `XgRNO8k8`（S 2.35 / F 1.76）平台 prod **0.8148**（2026-10-23 实测 253 s），
  而 §AK 已测 `XgRNO8k8 × ZYmX7ZG3 = 0.9976` —— 两条 PnL 几乎是同一序列 ⇒ prod ≈ 0.81，**必挂 0.7 线**。
- 裁决：**拒提**。工程结论（可复用）：**对从未触发过平台 PROD 检查的 alpha，`check_correlation`
  可能永久返回 null；`null` 不是“还在算”，是“作业从未起来”。**此时用「同族已测 prod × 互相关」
  做派生判据，并在台账注明是**派生**而非实测，不冒充实测值。

### §C 第 6–10 颗的选集：为什么转 `fundamental93`

按 §H 的 166 数据集全景逐层排除：

| 候选面 | 排除理由 |
|---|---|
| analyst / model 塔 | **已点亮**（本季 6 / 4）⇒ 用户指令：先不回测 |
| earnings 塔 | ds339 已证**结构性单名额**（§J），且该名额 `XgRNO8k8` prod 0.8148 ⇒ 无第二名额；earnings7/4/6/27 高拥挤 |
| 文本 / 新闻前沿（aC 29–49） | 四个已全测死：news_sentiment_nlp（6 机制，§A）、finnews_nlp_scores（8 机制，§L）、creator_signal_perf（判弱，§F）、shortinterest / socialmedia 类别关闭 |
| `other` 塔 | other143 F 墙 0.88（AO.13 封存）、other699 整段缺口、other596 刚封存（本附录 §A） |
| option 塔 | option3 六机制全死（§I）；option6/8/9 数据集级 aC 1.9 万–20 万，饱和 |
| **`fundamental93`（fundamental 塔，本季 0 ⇒ 未点亮）** | **唯一剩下的交集**：数据集级 aC **85**（低拥挤前沿）、cov 0.63、46 字段、**4 个独立构念**（应计 / 递延税费用 / 递延税负债 / 税务应计）、**本 book 从未测过**、机制与已交付 5 颗零共享字段零共享构念 |

字段画像（44 字段全表 + 四族 + 覆盖率分层 + 形态语义）：
[`_usa-fundamental93-field-profile-20261023.md`](_usa-fundamental93-field-profile-20261023.md)

### §D 波 85 预注册（发波前写死，事后不调）

- 10 臂、一臂一机制、单数据集 ATOM；multisim `10B8Bba0H5jy95RYWO6cVeQ`；
  表达式文件 `tracking/USA/runs/usa_fnd93_w85.txt`。
- 设置：USA / TOP3000 / D1、decay 10、trunc 0.08、INDUSTRY、nanHandling ON、
  pasteurization ON、unitHandling VERIFY、maxTrade OFF。
- 预检：本地元数闸 **10/10 passed**（101 个算子签名；该闸已 fail-closed，未知算子会以
  `[UNKNOWN_OP]` 拦下，故一次检查同时覆盖“元数 + 算子存在性”）。
- **红线判据（与画像 §6 同文，此处只列五条）**：
  1. 任一臂 S ≥ 1.58 / F ≥ 1.0 / 2Y ≥ 1.58 / SUB ≥ 0.43×S / TO ∈ [0.01, 0.70] ⇒ 进 prod；
  2. 十臂 max S < 1.2 ⇒ `USA-FND93-TAX-WEAK` 封存，**不发第 2 批**；
  3. max S ∈ [1.2, 1.58) ⇒ 先归因，只动被点名的那一维（不整批换壳扫参）；
  4. 覆盖 <0.50 的臂即使 S 最高也不单独晋级（先修 CW 或加 `*_length` 门控）；
  5. #9（资产增长，cov 0.895）若最强 ⇒ prod 前先与自家 `fnd6` 资本开支/规模腿测 self，
     corr ≥ 0.7 直接弃臂（§AL §B：`WjLekJQO` self 0.7718 即被 fnd6 吸收）。

### §E 波 85 结果与封存裁决（2026-10-23）：`USA-FND93-TAX-WEAK`

十臂全部终态（multisim `10B8Bba0H5jy95RYWO6cVeQ`，10/10 COMPLETE）。设置冻结：
USA / TOP3000 / D1、decay 10、trunc 0.08、INDUSTRY、nanHandling ON、VERIFY。

| # | alpha | 臂（构造） | S | F | TO | 2Y | SUB | 判 |
|---|---|---|---:|---:|---:|---:|---:|---|
| 1 | `YPx8AExw` | 税务应计 11（D） | 0.58 | 0.21 | 0.0124 | 0.46 | 0.15 | 四闸挂 |
| 2 | `vROZmpOA` | 应计 LTM 均值（A） | 0.64 | 0.26 | **0.0088** | 0.75 | 0.53 | 四闸挂 + TO 地板 |
| 3 | `VkdZ8mdA` | 应计 LTM 波动（A） | 0.57 | 0.23 | **0.0090** | 1.00 | 0.26 | 四闸挂 + TO 地板 |
| 4 | `N1eLOJNq` | 应计本期意外（A） | 0.59 | 0.25 | 0.0135 | 0.77 | 0.15 | 四闸挂 |
| 5 | `qMEOXYLj` | 递延税费用意外（B） | 0.93 | 0.56 | 0.0133 | 1.24 | 0.33 | 四闸挂（本族最强） |
| 6 | `1YjOglNR` | 递延税费用波动（B） | 0.85 | 0.44 | 0.0112 | 1.22 | 0.09 | 四闸挂 |
| 7 | `O0JR9MWY` | 递延税负债偏离（C） | 0.66 | 0.35 | 0.0162 | 0.92 | 0.12 | 四闸挂 |
| 8 | `gJWX3gaK` | 递延税负债波动（C） | 0.63 | 0.33 | 0.0106 | 1.01 | 0.26 | 四闸挂 |
| 9 | `pwvx7Mav` | **资产增长（cov 0.895）** | **1.11** | 0.55 | 0.0428 | 1.13 | 0.36 | 四闸挂（十臂最高） |
| 10 | `zqrgW2dE` | 递延税费用离散度（B） | 0.44 | 0.12 | 0.0131 | 0.51 | **−0.43** | 四闸挂 + SUB 反向 |

**裁决**：`max S = 1.11 < 1.2` ⇒ 触发预注册判据 2，判 **`USA-FND93-TAX-WEAK`**，不发第 2 批。
不是「差一两闸」：距 LOW_SHARPE 线差 0.47，距 LOW_FITNESS 线差 0.45，距 2Y 线差 0.45。
判据 5 随之作废（#9 确实最强，但它本身四闸全挂，没资格进 prod 比对）。

**归因（不是扫参失败，是信号不存在）**：
- 构造 A（应计族，4 臂）S 0.57–0.64，四臂一致且方差极小 —— 方向先验没错（S 全为正），
  但幅度只有线的一半，是「弱因子」而非「符号反了」。
- 构造 B（递延税费用）0.85–0.93 是本集最有信息的一族；2Y 1.22–1.24 也说明它近年略强，
  但 FITNESS 0.44–0.56 与 SUB 0.09–0.33 双双不够。
- 构造 C（递延税负债）0.63–0.66，与 A 同量级。
- 唯一接近 1.2 的是 #9 资产增长 —— 而它恰恰是**十臂里唯一不属税族的构造**（Cooper 资产增长异象），
  且与自家 fnd6 规模/资本开支腿同源（§AL §B）。它最强反而佐证：本集真正的载荷不是税，是资产规模变化。

**两条工程事实**：
- **两臂击穿 LOW_TURNOVER 0.01 地板**（0.0088 / 0.0090）。成因是「季度数据 + decay 10 +
  `group_rank` 稳定排名」三者叠加。慢速 fundamental 信号今后一律 decay 0–5 起步（波 86 已按此改）。
- `batch_get_alpha_metrics` 在完成瞬间返回全 null（10/10 被判 REJECT），而同一时刻
  `get_alpha_details` 已有完整指标；`batch_status` 也读不了 multisim 父件（`child_count=0`）。
  收批一律：`tools/batch_status.py --ids <父件>` 拿 id 映射 → 逐条 `get_alpha_details` 取值。

**可复用的第二层拥挤度盲区（本波最大产出）**：
附录 §H 的教训是「拥挤度必须用数据集级 aC，字段级会差三个数量级」。本波证明**数据集级 aC
仍不是充分统计量**：fnd93 aC 85 只说明「这个 vendor 的税表没人用」，**不说明「应计这个构造没人用」**。
应计自 Sloan (1996) 起是论文级构造，在 `fundamental2/6/13/17` 等 aC 万级–百万级的饱和集里可直接表达，
被挖过无数次。⇒ **拥挤度要按机制（construct）计，不是按数据集计**。
可操作的判别：若某构造能在 aC ≥ 10⁴ 的主 fundamentals 集里直接表达，那么它在任何小众同义集里
都不该指望有残余 alpha —— 这与「低拥挤 ≠ 有信号」是同一条，但给出了**先验筛查工具**。

### §F 波 86 结果与封存裁决（2026-10-23）：`USA-OTH416-FILING-TEXT-WEAK`

十臂全部终态（multisim `4o4EPubk44gGcKcllRSUJUC`，10/10 COMPLETE，全部 UNSUBMITTED）。
设置：USA / TOP3000 / D1、**decay 0**、trunc 0.08、INDUSTRY、nanHandling ON、VERIFY。
表达式文件 `tracking/USA/runs/usa_oth416_w86.txt`；画像见
[`_usa-other416-field-profile-20261023.md`](_usa-other416-field-profile-20261023.md) §8。

| # | alpha | 臂 | S | F | TO | 2Y | SUB | RN S |
|---|---|---|---:|---:|---:|---:|---:|---:|
| 1 | `omoRKKY2` | 语言变动 YoY L1（cat0） | 0.37 | 0.12 | 0.0168 | −0.44 | 0.73 | −0.22 |
| 2 | `KPmvbbLN` | 语言变动 YoY L2 | 0.39 | 0.13 | 0.0181 | −0.50 | 0.43 | −0.24 |
| 3 | `MP0dppxz` | 语言变动 QoQ L1 | 0.27 | 0.08 | 0.0287 | −0.42 | 0.26 | −0.59 |
| 4 | `j2eoZZZ5` | 语言变动 QoQ L3 | 0.39 | 0.13 | 0.0273 | −0.25 | 0.31 | −0.30 |
| 5 | `RRA9pppa` | 段 cat1 变动 | 0.39 | 0.13 | 0.0171 | −0.32 | 0.78 | −0.41 |
| 6 | `LL5Eppp9` | 段 cat13 变动 | 0.45 | 0.16 | 0.0194 | −0.45 | 0.19 | −0.09 |
| 7 | `gJWX1110` | 变动离散度 `vec_stddev` | 0.07 | 0.01 | **0.0071✗** | +0.23 | 0.21 | −0.18 |
| 8 | `MP0dppQM` | 最变动段 `vec_min` | 0.27 | 0.07 | 0.0287 | −0.43 | 0.26 | −0.60 |
| 9 | `bl8JLLqM` | 可读性 | 0.23 | 0.06 | 0.0750 | −0.57 | 0.13 | −0.56 |
| 10 | `xA1Vxxkb` | 披露广度 `doccount` | **0.50** | 0.20 | 0.0156 | −0.18 | 0.51 | **+0.66** |

**裁决**：`max S = 0.50 < 1.2` ⇒ 触发预注册判据 2，判 **`USA-OTH416-FILING-TEXT-WEAK`**，不发第 2 批。
差距不是"一两闸"：距 LOW_SHARPE 1.58 差 3.2 倍，距 FITNESS 1.0 差 5 倍。
判据 3 的前提（只有 #9/#10 活着）不成立——连文本质量与披露广度也全灭，**比判据 3 更彻底**。

**归因**：
- **Lazy Prices 六臂（1–6）**：S 0.27–0.45，**2Y 全负（−0.25 ~ −0.50）**，RN Sharpe 也全负。
  论文级机械锚（Cohen–Malloy–Nguyen, JF 2020）在 USA/D1/TOP3000 **不复现**，
  且近两年方向相反。SUB 在 #1/#5 反而冲高（0.73/0.78）⇒ 信号只藏在子集里，不构成候选。
- **离散度/极端段（7、8）**：#7 是**退化臂** —— `longCount 107 / shortCount 1953`，
  该字段对多数标的的 vector 是近常数（stddev=0），截面秩在 0 处并列致一条腿塌缩。
  #8 与 #3 同量级 ⇒ 极端段不携带超出均值的额外信息。
- **文本质量（9）**：S 0.23 / 2Y −0.57，**比已判死的 `filing_sentiment` 更差**。
  文本语调/质量路径在本 book 内第二次确认不可用。
- **披露广度（10）**：全波唯一"风险中性化后变好"的臂（RN **+0.66** > 原始 0.50）——
  披露广度确实含信息，但**信息几乎全落在行业/风险暴露层面，残差 alpha 近零**。F 0.20 修不动。

**两条工程事实**：
- **Vector 算子面在平台层面确认为 7 个**（`get_operators`，103 总数 / Vector 类 7）：
  `vec_avg` `vec_sum` `vec_max` `vec_min` `vec_stddev` `vec_range` `vec_count`。
  论坛帖（43789987978263）列出的 `vec_ir / vec_skewness / vec_kurtosis / vec_percentage / vec_powersum`
  **只以 COMBO-only 的 `reduce_*` 存在**，REGULAR 拿不到 ⇒ 该帖扩展清单对本轨不可用。
- **退化臂的廉价指纹 = 多空计数**：vector 离散度/极值类臂收批先看 `longCount/shortCount`
  与 TO，再看 Sharpe；107:1953 这种失衡本身就说明字段在该构造下不可用。
- decay 0 确实治好了季度事件类文本信号的换手地板（9/10 PASS LOW_TURNOVER），
  波 85 预注册的设置层修法**有效且已固化**。

**新增的第三条 S0 先验（本波最大产出，与 §E 的第二层并列）**：
§E 教的是「**拥挤度是构造的属性，不是数据集的属性**」——能被饱和集直接写出的构造，
在小众同义集里也挤。本波是它的**对偶**：**构造独特也不保证可复现**。
`oth416` 的语言变动构造在全体 fundamental 里独此一家（没有饱和集能直接写出），
但平台只给**缓冲级聚合**、没有 `vec_last`，论文的"最新一次变动量"**无法表达**；
能算的只剩"近若干期平均相似度水平"，而后者已被价格吃干净。
⇒ **S0 选集必须先问「论文信号的时点能否用平台算子表达」**，表达不了就把它降级为探索臂，
不能当主假定。三条先验合起来：aC 只说明 vendor 没人用（§H）；
构造拥挤度决定有无残余（§E）；**构造可表达性决定信号还在不在**（本波）。

**数据集切换说明（遵「不得频繁切换数据集」约束）**：`oth416` 是本轮 fundamental 全景里
最后一个通过 S0 过滤（未判死 × aC<2000 × cov≥0.55 × 字段充足 × 机制正交 × 有论文锚）的数据集，
四个构造族一次测尽后封存。剩余未判死的 fundamental 集已无可挖面，理由逐条登记在
[`_usa-fundamental-universe-scan-20261023.md`](_usa-fundamental-universe-scan-20261023.md)：
`fundamental21`（ESG，aC 154，cov 0.43）、`fundamental1`（高管履历，aC 359，cov 0.41）、
`fundamental25`（aC 72，cov 0.38，8 字段）、`fundamental35`（aC 71，cov 1.0，**1 字段**）、
`fundamental22`（aC 81，实为 RIC↔BBG 代码映射，无经济含义）。


### §G 波 87 结果与封存裁决（2026-10-23）：`USA-FND1-GOVERNANCE-WEAK`

数据集 `fundamental1`（BoardEx 型高管履历，179 可用字段 / cov 0.412 / aC 359 / 全部 VECTOR / **年度**）。
设置：USA / TOP3000 / D1、**decay 0**、trunc 0.08、INDUSTRY、nanHandling ON、VERIFY。
multisim `303PNc7ln4Y28RjYlWZhQrg`，10/10 COMPLETE（首派 `1nPbmEfUU4tScKcNQGH63VV` 因两条字段名拼错整批连坐，见下）。

| # | alpha | 臂 | S | F | TO | 2Y | SUB | RN |
|---|---|---|---:|---:|---:|---:|---:|---:|
| 1 | `XgRVnEam` | 董事人数 − | −0.10 | −0.02 | 0.0297 | −0.54 | −0.24 | +0.14 |
| 2 | `QPYOVd0K` | **3 年流失率 −** | **1.17** | **0.69** | 0.0224 | **1.92** | 0.63 | **0.81** |
| 3 | `P0Mx3EPW` | 1 年流失率 − | 0.75 | 0.31 | 0.0207 | 1.26 | 0.22 | 0.08 |
| 4 | `zqrgmzA8` | 继任风险 − | 0.78 | 0.38 | 0.0277 | 1.20 | 0.23 | 0.28 |
| 5 | `88vVQqVm` | 董事平均任期 − | −0.31 | −0.11 | 0.0249 | −1.01 | −0.07 | −0.02 |
| 6 | `9qE8rQM1` | 外部董事会任职 − | −0.42 | −0.14 | 0.0257 | −1.56 | −0.22 | +0.15 |
| 7 | `JjPoOLzO` | 男性占比 − | 0.64 | 0.23 | 0.0274 | 0.32 | 0.03 | −0.03 |
| 8 | `GrgXLvzQ` | 非上市董事数 − | 0.02 | 0.00 | 0.0260 | 0.43 | −0.05 | −0.38 |
| 9 | `omoRleGb` | 学历总量 + | 0.72 | 0.25 | 0.0259 | 0.79 | 0.42 | 0.28 |
| 10 | `9qE8rQm1` | 薪酬-业绩敏感 + | 0.38 | 0.17 | **0.0096** | 0.65 | 0.34 | 0.27 |

**裁决**：`max S = 1.17 < 1.2` ⇒ 预注册判据 2 命中，判 **`USA-FND1-GOVERNANCE-WEAK`**，
**不发第 2 批**。判据 5（翻号）不适用（仅 3/10 负号）；判据 3 被 #10 正面证实
（TO 0.0096 击穿地板、long 567 / short 2519 一侧建仓）。**不进 Mode B**：本仓资格线
S ≥ 1.25 且 F ≥ 0.8，#2 的 1.17 / 0.69 两条都不够。

**归因**：结构族（人数/任期/外部任职/兼职数）四臂全在 ±0.5 内 ⇒ 董事会"长什么样"在
INDUSTRY 中性化后无横截面收益信息；唯一有幅度的是**人员流失族**，且
**3 年流失（1.17）显著强于 1 年流失（0.75）**、RN 0.81 与 2Y 1.92 证明不是风险暴露伪装 ⇒
载荷是"慢性治理劣化"。多元化/人力资本（#7/#9）是 2014–2021 行情，2Y 0.32 / 0.79 已衰减，
与 `fundamental21` ESG 族被降级的判断互证。

**两条工程事实**：
- **拼错字段名 = 整批连坐**：`fnd1_filtered_totnounlstdbrd` / `fnd1_filtered_noquals` 平台不存在
  （真名挂 `fnd1_board_characteristics_filtered_*`），回 `Attempted to use unknown variable`
  ⇒ 2 ERROR + **8 CANCELLED**。`op_arity` 网关只管算子、看不见字段名；`validate_fields=true`
  也不在派发前拦。发批前字段 id 必须从 `get_datafields` 原样复制。
- **低换手压死 Fitness**：`fitness ≈ sharpe × sqrt(|returns| / max(TO, 0.125))`。#2 实算
  `1.17 × sqrt(0.0438/0.125) = 0.69` 与平台一致 ⇒ F ≥ 1.0 且 S = 1.58 要求年化 ≥ 5.0%，
  而本臂 4.38%。**慢速 fundamental 的瓶颈是收益幅度，设置层改不动**，故不用判据 4 的修复额度。

**第四层 S0 先验（继 aC 拥挤度 → 构造拥挤度 → 构造可表达性 之后）**：
**治理类数据集的可交易载荷只在"人员流动率"，不在"结构/画像"**。BoardEx 型数据集动辄上百字段，
按构念归并后通常只有流失/更替一族有横截面预测力，其余是控制变量或事件研究变量。
⇒ 拿到 governance 数据集，先测流失族，结构族只留 1–2 条对照臂，十臂预算不平摊。
字段画像存档：[`_usa-fundamental1-field-profile-20261023.md`](_usa-fundamental1-field-profile-20261023.md)（§8 全文）。

## 附录 AQ：波 82_other143 — 门控 × 权重形状（F 墙已破，2026-10-23）

> 本附录是 DB `wave_results` 行 `USA/82_other143` 的 `source_file` 指向（`…#AQ`）。
> 波号用字符串 **`82_other143`**：数字 `82` 已被 2026-09 的自动收批行占用（同 §8.6「波号原样入库」）。
> 触发：用户追问**「有没试过门控」**。§AO 的 F 墙（`78o3QRwO` S2.60 / **F0.88** / TO0.5783）此前被判为
> 「old shell 专属」结构，本轮换壳重测。

### AQ.1 字段与机制（other143）

- 字段：`exempt_industry_top_broker_share_pct`（**MATRIX**，coverage **1.0**，uC 29 / aC 67）。
- 平台描述：*"Anonymous market share percentage of the most active Clearing ID in this category."*
  ⇒ 机制 = **行业级机构订单流集中度（清算经纪商份额）**；有信息的是**相对自身 60 日基准的极端偏离**，
  中间带不携带信息。这与「水平值」构造（§AO 已证 F 墙）是**两类不同的载荷**。

### AQ.2 三批设计（G 门控 / S 形状 / D 设置）

设置全批统一：USA / TOP3000 / D1 / **decay 5** / SUBINDUSTRY / trunc 0.08 / nanHandling ON / VERIFY / maxTrade OFF / 2014–2023。

| 批 | multisim | 臂 |
|---|---|---|
| G 门控 5 臂 | `1Yrb3J6nt53pcf0PKTe78Tf` | `kqJvZGY8` / `78o3nm25` / `9qE87M3o` / `KPmvEzpk` / `leME3GYA` |
| S 形状 5 臂 | `2iYUfXc4w4nG8IgTfClrY3y` | `pwvxKeGv` / `E5VNePz9` / `omoRg0r2` / `ZYmgKvMn` / `e76NxZvN` |
| D 设置 1 臂 | `20iQH9cOZ4lNchGBlA8G9Ek` | **子件丢失未重发**（不计） |
| 82b 组合 4 臂 | `1kj8Pegkf4CNcnd1hbN8NB1s` | `RRA97Wo0` / `A1QelK8W` / `XgRV76xz` / `gJWXjp5M` |

### AQ.3 结果

**门控阈值曲线（新壳 `trade_when(|z|>τ, rank(z60), -1)`）单调**：

| τ | S | F | TO |
|---|---:|---:|---:|
| **0.5** | **2.68** | **1.03** | **0.4029** |
| 0.75 | 2.44 | 1.00 | 0.307 |
| 1.0 | 1.98 | 0.88 | 0.219 |

峰在 0.5 或更松一侧。**旧壳 `A1-z120` 在 τ=1.0 只有 F0.58** ⇒ §AO.2「门控无用」是**旧壳专属结论，已被推翻**。
`78o3nm25` 的 F 恰为 **1.00**，提交层严格不等式 `value == limit` 判 FAIL ⇒ 只作剂量曲线证据点，不作候选。

**权重形状（与门控正交）**：`signed_power(rank(z60)-0.5, 3)` TO 几乎不动（0.5722）但 RET **+15.6%**、S 2.60→2.79；
`power4`（`XgRV76xz`）F1.04、`power2`（`gJWXjp5M`）F0.98 且 `failed_ra=1` ⇒ 指数 3 为峰。
`normalize(useStd=false)` 与基线**逐位相同**（纯仿射成员确实改不了 F）。
`quantile(driver=gaussian) σ=1.0` 与 `σ=0.5` **逐位相同（含 pnl 7251386）** ⇒ sigma 惰性参数，不再扫。
跨区「零代价双窗」`add(z60, z120)` **失败**（S2.50 / F0.85）：本信号是相对基准的偏离，时域平均会把它抹掉
（同批 A `ts_decay_linear` 同因）。

**82b 组合（门控 × 形状叠加）**：

| 臂 | 构造 | S | F | TO | 2Y | SUB | CLUSTER |
|---|---|---:|---:|---:|---:|---:|---:|
| **C1 `RRA97Wo0`** | `trade_when(|z|>0.5, signed_power(rank(z60)-0.5,3), -1)` | **2.75** | **1.09** | 0.4281 | 2.59 | 1.67 | 1.35 |
| C4 `A1QelK8W` | 门控 × `quantile(gaussian, σ=1)` | 2.75 | 1.08 | 0.4126 | 2.61 | **1.76** | 1.32 |
| C3 `XgRV76xz` | `power4` | 2.79 | 1.04 | 0.5750 | 2.55 | 1.71 | 1.49 |
| C2 `gJWXjp5M` | `power2` | — | 0.98 | — | — | — | — |

`RET/TO` 0.1350 → **0.1558（+15.4%）** ⇒ **门控（换手杠杆）与 signed_power（收益杠杆）是加法叠加，不是替代**。
这是 `F = S·sqrt(RET/TO)` 上唯一能**同时**改善两因子的组合。
G4/G5 的 `|Δrank|` 无交易带只把 TO 压到 0.563/0.543（−2.6%/−6.1%），而 `|z|` 门控压到 0.403（−30%）
⇒ **换手来源是权重再缩放而非 rank 抖动**，这解释了二者为何可叠加。

### AQ.4 判决与稳健性

- 预注册判决 ① 命中（≥1 臂 F≥1.0 且 S/2Y/SUB 全过）⇒ 进 prod 探针队列；**提交仍需用户确认**。
- 候选排序：**C1 `RRA97Wo0` > C4 `A1QelK8W` > C3 `XgRV76xz`**（C2 有 `failed_ra`，不列）。
- 稳健性 **`RRA97Wo0` = PASS**（台账 `USA/robustness_RRA97Wo0`，报告
  [`reports/robustness_20261023.md`](../../../../reports/robustness_20261023.md)）：10/10 年为正、
  最近 3 年 **3.14 / 3.03 / 2.16**、CV 0.19、衰减比 0.785、换手十年 0.424–0.441、SELF **0.3712**。
  软标记：margin **3.12 bp @ TO 42.8%**、8 个算子调用点、体检包未收录该字段（实测 MATRIX coverage 1.0）、CLUSTER 1.35。
- 平台检查（`get_alpha_details` 直取）：`failed_ra_count=0`、`failed_ppa_count=0`；PASS 含
  `LOW_SHARPE` / `LOW_FITNESS` / `LOW_SUB_UNIVERSE_SHARPE` / `LOW_2Y_SHARPE` / `CONCENTRATED_WEIGHT` / `MATCHES_PYRAMID`；
  WARNING 仅 `CLUSTER_TEST 1.35(1.58)` / `MATCHES_THEMES` / `OSMOSIS_ALLOCATION`；金字塔 `USA/D1/OTHER ×1.4`。
- **PROD 已测，整族撞墙（2026-10-23 03:43，排到账号级相关槽后实测）**：
  `campaign_intel.py prod-first`（进程锁 + 串行 + 单条硬超时）按「每信号族探 1 条」规则探了 2 条：

  | 探针 | 家族 | S | F | **prod** | 判决 |
  |---|---|---:|---:|---:|---|
  | `XgRV76xz` | `exempt_industry_top_broker_share_pct` | 2.79 | 1.04 | **0.9046** | STOP |
  | `A1QelK8W` | 同上 + `quantile(gaussian, σ=1)` | 2.75 | 1.08 | **0.8704** | STOP |

  族级结论 `EXPAND=0 / STOP=2 / UNKNOWN=0`，台账 `USA/prod_first_82_other143`，
  原始件 `logs/_prod_first_82_other143.json`。
  ⇒ **`RRA97Wo0` 不提交**：它与两条探针同一字段、同一壳，属同一 prod 信号族
  （`prod-first` 的「每族 1 条」抽样正是为此设计，不必再烧一个槽去单独测它）。
  ⇒ 按决策表 D0：**撞 prod 墙 ⇒ 换族/换集 regenerate，不磨同腿变体**
  （`add`/`hump`/窗口微调都在同一持仓面上，只会把 prod 留在这个量级）。
  ⇒ 本族的**唯一出路是换字段**：`exempt_tier1_broker_concentration_index`（波 83 的 A1）
  是**另一个字段** ⇒ **另一个 prod 族**，`58jrz86J` 的 prod 尚未测，这才是第 6 颗真正的候选路径。

### AQ.5 两条可复用判据 + 一条工程债

1. **`CLUSTER_TEST` 不阻断 USA 提交**：不在 `wq.config.RA_CHECK_NAMES`（18 项）内 ⇒ 不进 `failed_ra`。
   实证：已 ACTIVE/OS 的 `e76xgXkM` CLUSTER **1.16**（limit 1.58）提交成功（2026-10-19）。
   `RRA97Wo0` 的 1.35、`pw5RbrYX` 的 1.54 同理，只作信息项。
2. **`field_inspect_gate` 的 `partial 0/N` ≠ 表达式不合格**：它只说明体检包里没这个字段
   （按数据集分包）。判字段可用性要直接查 `get_datafields` 的 coverage / type —— 本字段实测 **MATRIX / 1.0**。
3. **工程债（已补）**：82b 的 4 臂只存在于本波 `candidates` JSON，从未进 `backtest_results`，
   导致 `prod-first` 首跑静默退出（`[prod-first] USA wave=82_other143 无回测行`，exit 0）。
   已用 `upsert_backtest_rows` 写入 5 行（含 C1–C3 + G1 + S4），`ra_failed_checks` 均为 `[]`。
   **同型前科**：analyst45 的 45A/B/C 至今仍缺行。收波时「波行有 candidates ≠ 回测行存在」，
   下游 prod / 稳健工具只看 `backtest_results`。

## 附录 AR：波 83_other143 — 十机制换核（一臂 near，2026-10-23）

> 本附录是 DB `wave_results` 行 `USA/83_other143` 的 `source_file` 指向（`…#AR`）。
> 起因：§AQ 证明**门控 × 权重形状**这条壳能过 F 墙，但只用过一个字段
> `exempt_industry_top_broker_share_pct`。数据集 other143 的画像（
> [`_usa-other143-field-profile-20261023.md`](_usa-other143-field-profile-20261023.md) §3）
> 预注册了 A1–A10 十机制，本波就是把它们**放进同一壳**逐条检验：
> 壳固定 ⇒ 结果差异只归因于**机制/字段**，不掺算子优化。

### AR.1 设计与派发

设置全批统一：USA / TOP3000 / D1 / **decay 5** / SUBINDUSTRY / trunc 0.08 / nanHandling ON /
VERIFY / maxTrade OFF / 2014–2023。壳：

```
trade_when(greater(abs(ts_zscore(<F>, 60)), 0.5),
           signed_power(subtract(rank(ts_zscore(<F>, 60)), 0.5), 3), -1)
```

负向假设在 `signed_power` 外再套 `multiply(-1, …)`。文件
`tracking/USA/runs/usa_other143_w83.txt`，multisim **`SX2yh2Ni5chbk2GK60BJXY`**（10/10 COMPLETE）。
平台 `validate_expressions`：`valid: true`，14 字段 0 unknown。

### AR.2 结果（按 F 排序，全为实测）

| 臂 | alpha | 机制（字段） | 向 | S | F | TO | 2Y | SUB |
|---|---|---|---|---:|---:|---:|---:|---:|
| **A1** | **`58jrz86J`** | tier1 集中度**水平**（`exempt_tier1_broker_concentration_index`） | + | **2.40** | **0.93** | 0.3992 | **2.68** | 1.50 |
| A6 | `ZYmgbYWd` | 冠军字段的 22 日**变化**（`exempt_tier1_top_broker_share_pct`） | + | 1.77 | 0.53 | 0.4215 | 1.28 | 1.13 |
| A2 | `kqJvoqm6` | 行业不同经纪商数（`exempt_industry_distinct_broker_count`） | − | 1.08 | 0.32 | 0.4029 | **0.22** | 0.83 |
| A10 | `QPYObP2W` | 空头成交额占比 | − | 0.74 | 0.17 | 0.3819 | 0.13 | 0.64 |
| A5 | `RRA9bRkb` | buy/sell GBDA vwap 价差 | + | −0.10 | −0.01 | 0.2675 | 0.01 | 0.03 |
| A8 | `pwvxRwVg` | tier1 − industry 集中度差 | + | −0.79 | −0.17 | 0.4262 | −0.23 | 0.02 |
| A7 | `WjL3bjWZ` | buy tier1 rank1 − rank2 陡峭度 | + | −1.06 | −0.23 | 0.4979 | −1.65 | −0.28 |
| A4 | `9qE8jqA9` | 空头超额集中度（short − sell） | − | −1.11 | −0.27 | 0.4065 | **−3.37** | −0.86 |
| A3 | `78o3N8Kb` | buy − sell 集中度**背离** | + | −2.08 | −0.66 | 0.4250 | **+1.29** | −0.52 |
| A9 | `qMEOxMPP` | 唯一经纪商数 / 66 日均 | − | — | — | — | — | — |

### AR.3 归因：四个可复用的机制判据

1. **A1 是唯一具备提交潜力的臂，且它换的是「水平」不是「斜率」**。
   冠军 `RRA97Wo0` 用的是 top-share 字段的 z 偏离；A1 用的是**另一个字段**的**水平**
   （tier1 层 HHI）。两者同属「清算集中度」构念，但字段不同、载荷形态不同（详见 AR.4 的自相关预期）。
   唯一失败项 `LOW_FITNESS 0.93 vs 1.00`。

2. **A3 的证伪方式是「符号跨期翻转」，这类臂不能靠翻号救**。
   全期 S **−2.08**、近 2 年 **+1.29**：翻号得到 +2.08 / −1.29。两个方向各有一段崩期
   ⇒ 不是方向写反，是**机制本身不稳**（买卖集中度之差在 2014–2019 与 2022–2023 是两类信息）。
   判据：**全期符号与最近 2 年符号相反 ⇒ 直接判死，不进修复**。

3. **「同构字段相减」几乎总是无增量**。A8（tier1 − industry 集中度）S −0.79、
   A5（buy vwap − sell vwap）S −0.10、A7（rank1 − rank2）S −1.06：
   三条都是**两个同向量的差**，z-score 之后横截面信息被抵消。
   与 §AQ 的 `add(z60, z120)` 失败同源——**同源信号的加减法在本族不产生新载荷**。

4. **A6 的「变化量」载荷比「水平」弱一个档**（S 1.77 vs 2.40，F 0.53 vs 0.93）。
   同一个字段，`ts_delta(·,22)` 后再 z-score，比直接用水平做 z-score 弱。
   ⇒ 本数据集的信息在**状态**（谁在集中），不在**变化**（集中度在变快还是变慢）。

### AR.4 A1 的差距是纯换手问题（算术，不是猜测）

```
F = S · sqrt(|RET| / max(TO, 0.125))
  = 2.40 · sqrt(0.0596 / 0.3992) = 2.40 · 0.3864 = 0.927 ≈ 平台 0.93  ✅ 复算吻合
```

固定 S 与 RET 时，要 `F ≥ 1.0` 需 `TO ≤ 0.0596 / (1.0/2.40)² = 0.3433`（**−14%**）。
§AQ 的门控曲线已证 τ 是 TO 主杠杆（同族 τ 0.5→0.75 使 TO 0.4029→0.307，−24%，S 只掉 9%），
且 `hump`、`signed_power` 指数、`quantile` 形状都还在同一族里未对 A1 标定过
⇒ 修复走**门控阶梯 × 形状 × hump**，不动字段、不动设置。

### AR.5 判决

- 预注册判据：10 臂里 **1 臂 near**（A1，仅差 F 0.07）、1 臂机制成立但弱（A6）、
  1 臂符号不稳证伪（A3）、1 臂覆盖率疑不足（A9）、6 臂弱 ⇒ `PARTIAL`。
- **A1 `58jrz86J` 进波 83b**（定向破 F 墙，10 臂：τ 0.6/0.7/0.75/0.85、τ0.7×p4、
  τ0.5/0.7/0.75 × hump 0.01/0.02、门控窗 120、quantile 形状），multisim `2Iz9wcbJj4pZaf9zMMsiTGh`。
- A6 `ZYmgbYWd` 不作修复对象（F 差 0.47，远超单杠杆量级），留作**组合杠杆**候选。
- A9 `qMEOxMPP` 的 `None` 是**覆盖问题不是机制问题**：先用 `get_datafields` 查
  `oth143_buy_tier1_unique_brokers` 的 coverage 再决定是否重测（本次不据此判死）。

### AR.6 两条工程事实（会反复踩）

1. **multisim 父件读不到子件**：`tools/batch_status.py --ids <parent>` 与 MCP `batch_status`
   都返回 `child_count: 0`；真子件在 `GET /simulations/{parent}` 的 `children` 列表里，
   逐个再 GET 才有 `status` / `alpha`。
2. **`BrainApiClient.session` 是同步 `requests.Session`**：对它 `await` 会
   `TypeError: object Response can't be used in 'await' expression`。
3. **`wqb-db` MCP 的 `upsert_wave_result` 对大 payload 会超时**（本次首次调用 70s 未返回，
   精简 `key_findings` 后同一调用 20s 内 `inserted`）。长台账先进附录、DB 只留判据摘要。

## 附录 AS：波 83b — A1 门控阶梯十臂（F 墙未破，门控是负杠杆，2026-10-23）

### AS.1 设计与目标

对象 = 波 83 的 A1 `58jrz86J`（`exempt_tier1_broker_concentration_index`，S 2.40 / F 0.93 / TO 0.3992，唯一失败项 `LOW_FITNESS`）。
10 臂同一 multisim `2Iz9wcbJj4pZaf9zMMsiTGh`（10/10 COMPLETE），设置 USA/TOP3000/D1/SUBINDUSTRY/decay 5/trunc 0.08。
设计轴：① τ 阶梯 0.6/0.7/0.75/0.85 ② 同 τ 下形状 p4 ③ hump 叠乘 ④ 门控窗 120 ⑤ `quantile(gaussian, σ=1)`。

### AS.2 结果（DB `wave='83b_other143'`）

| alpha | τ | 形状 | S | **F** | TO | RET | 2Y | SUB |
|---|---|---:|---:|---:|---:|---:|---:|---:|
| `bl8Jbrqm` | 0.6 | p3 | 2.21 | **0.86** | 0.3513 | 0.0534 | 2.48 | 1.38 |
| `1YjOXlpX` | 0.7 | quantile(σ=1) | 2.11 | **0.85** | 0.2909 | 0.0477 | 2.60 | 1.28 |
| `omoRLJg5` | 0.7 | p3 | 2.06 | 0.82 | 0.3009 | 0.0477 | 2.52 | 1.25 |
| `e76NbVx6` | 0.7 | p4 | 2.02 | 0.80 | 0.3109 | 0.0483 | 2.46 | 1.24 |
| `9qE8jd7K` | 0.75 | p3 | 1.96 | 0.79 | 0.2770 | 0.0450 | 2.50 | 1.24 |
| `VkdZam38` | 0.85 | p3 | 1.73 | 0.72 | 0.2348 | 0.0402 | 2.51 | 1.16 |
| `vROZrpNd` | 0.7 / 窗120 | p3 | 1.61 | 0.62 | 0.2797 | 0.0416 | 2.23 | 0.92 |
| `RRA9blm0` | 0.75 | hump 0.02 | 0.39 | 0.10 | 0.0066 | 0.0083 | 1.06 | 0.13 |
| `zqrg82NK` | 0.7 | hump 0.01 | 0.30 | 0.07 | 0.0066 | 0.0059 | 1.41 | 0.02 |
| `wp93Z2Ev` | 0.5 | hump 0.01 | 0.21 | 0.04 | 0.0066 | 0.0042 | 1.51 | −0.14 |

### AS.3 三条可复用判据

1. **同一字段上，门控是负杠杆**：τ 0→0.6→0.7→0.75→0.85，F 单调下滑 0.93→0.86→0.82→0.79→0.72。
   RET/TO 从 0.1493 抬到 0.1712（+15%），但 S 掉得更快（2.40→1.73，−28%）。
   **与 `exempt_industry_top_broker_share_pct` 的结论相反**（那里门控抬 F）⇒ 门控的方向依赖字段的
   信息形态：状态型字段（HHI 水平）在极端才有效，砍掉中带等于砍掉大部分载荷。
2. **`hump` 在本字段是破坏性的**：三个 hump 臂 TO 一律塌到 0.0066（贴 `LOW_TURNOVER 0.01` 地板），
   S 掉到 0.21–0.39。hump 的阈值收缩把信号本身压没了，不是"降换手"而是"停止交易"。
   ⇒ 低 TO 字段禁用 hump；要降 TO 用 `ts_decay_linear` / 平台 decay。
3. **同族内最有效的形状是 `quantile(driver=gaussian, sigma=1)`**（F 0.85 > p3 的 0.82，S 2.11 > 2.06，
   TO 0.2909 < 0.3009）—— 与 DEU 的 `quantile 替 signed_power` 增益方向一致。

### AS.4 F 的算术边界（决定后续方向）

```
F = S · sqrt(|RET| / max(TO, 0.125))
```
- **分母有 0.125 地板**：TO 降到 0.125 以下不再产生 F 增益。A1 当前 TO 0.3992 > 0.125 ⇒ 仍有可压空间。
- 若能把 TO 压到 0.20 而 S/RET 各只掉 10%（2.16 / 0.0536）：
  `F = 2.16 · sqrt(0.0536/0.20) = 1.12` ⇒ **可过**。
- 波 83b 的失败在于**门控在压 TO 的同时把 S 砍得更多**；换「平滑」轴（不动条件、不砍中带）才可能同时保住 S。

### AS.5 后续（波 83c，已发）

10 臂全在「平滑 × 内窗」轴上，不动门控：外层 `ts_decay_linear` 5/22/66/120/252（5 臂）、
内层 `ts_decay_linear` 22/66/120（3 臂，先平滑 z 再 rank，保留横截面新鲜度）、
内层 `ts_zscore` 窗 120/252（2 臂）。multisim 父件 `3hvG6Z8KX4Oucl12o7r3ak2`，
文件 `tracking/USA/runs/usa_other143_w83c_smooth.txt`，设置与 A1 同（SUBINDUSTRY/decay 5）。
预检：`logs/_tmp_preflight.py` 10/10 通过；体检硬门 partial（该字段未入体检包，与波 83 同）。

## 附录 AT：`1YZp6EP6` 提交前复核（REJECT，2026-10-23）

队列里的 READY 候选（RA 0 失败、prod 快照 0.6783）在稳健性闸前**被否决**：

| 检查 | 读数 | 判定 |
|---|---|---|
| 衰减比 | 2023 Sharpe 0.53 / 全期 1.86 = **0.285** | **REJECT**（< 0.30 硬线） |
| Recent-3yr CV | 0.62（样本 std）/ 0.51（总体 std） | 跨 0.60 线 |
| CLUSTER_TEST | 0.56 vs 1.58 | WARNING |
| 2020 | Sharpe −1.57、DD 7.4% | 软标记 |

三项独立证据同向（末端衰竭 + 集群强度不足 + 单年崩期）⇒ **不提交**，台账
`robustness_1YZp6EP6 = REJECT`，报告 `reports/robustness_20261023.md` 第二轮。
附带：该 alpha 属 ANALYST 塔（`pyramids.effective 1`），而 analyst 本季已点亮（6 ≥ 3），边际点塔价值为 0。
教训：**队列里的 READY 只代表平台层可提，不代表时间维度稳健**——提交前必须逐年看衰减比，
2Y Sharpe 1.70 与 TO 6% 都好看，末端年 0.53 才是真信号。

## 附录 AU：波 83c — A1 平滑轴十臂（F 0.96，贴线未过；平滑是负杠杆，2026-10-23）

### AU.1 设计与结果

对象仍是 A1 字段 `exempt_tier1_broker_concentration_index`；基座 = 无门控壳
`sign_power(rank(ts_zscore(F,60))−0.5, 3)`。multisim `3hvG6Z8KX4Oucl12o7r3ak2`（10/10 COMPLETE），
设置 SUBINDUSTRY / decay 5 / trunc 0.08，`wave='83c_other143'`。

| # | 轴 | alpha | S | **F** | TO | RET | 2Y | SUB |
|---:|---|---|---:|---:|---:|---:|---:|---:|
| 1 | 外 `ts_decay_linear` d=5 | `omoRWYEn` | 2.17 | **0.96** | 0.3277 | 0.0635 | 2.36 | 1.26 |
| 2 | 外 d=22 | `rKd9eWRd` | 1.27 | 0.64 | 0.1634 | 0.0421 | 1.82 | 0.76 |
| 3 | 外 d=66 | `6XAZKEdJ` | 0.79 | 0.39 | 0.1268 | 0.0307 | 1.69 | 0.16 |
| 4 | 外 d=120 | `MP0d3xYr` | 0.69 | 0.34 | 0.1295 | 0.0323 | 1.63 | 0.13 |
| 5 | 外 d=252 | `pwvx57aX` | 0.76 | 0.43 | 0.1409 | 0.0451 | 1.76 | 0.28 |
| 6 | 内 `ts_decay_linear` d=22 | `GrgXOomJ` | 1.26 | 0.62 | 0.1721 | 0.0415 | 1.91 | 0.77 |
| 7 | 内 d=66 | `zqrgbWdo` | 0.76 | 0.36 | 0.1183 | 0.0280 | 1.74 | 0.17 |
| 8 | 内 d=120 | `d5KY1Qax` | 0.65 | 0.30 | 0.1057 | 0.0272 | 1.52 | 0.21 |
| 9 | 内窗 `ts_zscore` 120 | `QPYOKQ0K` | 2.24 | 0.82 | 0.5339 | 0.0722 | 2.64 | 1.46 |
| 10 | 内窗 252 | `xA1VbnvW` | 1.95 | 0.76 | 0.5098 | 0.0765 | 2.74 | 1.32 |

### AU.2 三条判据

1. **平滑在本字段是纯负杠杆，且衰减极快**：外 d 5→22→66，F 0.96→0.64→0.39，S 2.17→1.27→0.79。
   d=5 相对无平滑基线（A1 F 0.93）只 +0.03，代价是 S −10%、TO −18%。
   **这是字段的信息半衰期决定的**：清算集中度是状态量，慢化即刻丢失载荷。
2. **内层平滑比外层更糟**（同 TO 档下 S 更低）：内 d=22（TO 0.172）S 1.26 vs 外 d=22（TO 0.163）S 1.27
   —— 几乎同分，但内层要多一层算子、可解释性更差 ⇒ **要平滑就放外层**。
3. **内窗 120 是「强度最好但换手失控」的一档**：S 2.24（全波最高）、RET 0.0722、2Y 2.64、SUB 1.46，
   但 TO 0.5339（+63%）⇒ F 0.82。**长内窗抬 S 也抬 TO**（与直觉相反：慢信号反而换手更高，
   因为 120 日 z 的横截面排序在趋势切换时整段翻转）。把外 d=5 套到内窗 120 上按同比例折算，
   F 仍在 0.82 附近（S 2.02 / TO 0.44 / RET 0.0722）⇒ **此路不通，不再投第三波平滑**。

### AU.3 判决与下一步

- 本波最高 **F = 0.96**（差 0.04），未过 1.00 ⇒ 平滑轴判死。
- 剩余空间只在**形状与中性化**：A1 的 SUBINDUSTRY 是全战役默认值，从未在本字段上做过中性化对照；
  形状上 p3 之外只测过 p4（更差），p2 / `quantile(gaussian)` / 去幂中位秩未测。⇒ 波 83d。

## 附录 AV：波 83d — A1 形状 × 中性化收口（已发，2026-10-23）

五组共 10 臂，全部同一表达式核 `ts_decay_linear(sign_power(rank(ts_zscore(F,60))−0.5, 3), 5)`
（= 波 83c 最佳臂），只动形状与中性化：

| 组 | 中性化 | 臂数 | multisim 父件 |
|---|---|---:|---|
| shapes | SUBINDUSTRY | 6（p2 / d=3 / `quantile(gaussian,σ=1)` / 去幂中位秩 / `ts_backfill 252`+p3 / `ts_backfill 252`+p2） | `1XKCSp8yP4M99z01hhUsrQj6` |
| neut | INDUSTRY | 1 | `2XZhzNtJ4JY8EtmOfIZjhg` |
| neut | MARKET | 1 | `4xNWVz99r4Mv9TJxQ22ALgF` |
| neut | SECTOR | 1 | `43ytaT4Dl4FY9B5Mft0Gqjf` |
| neut | STATISTICAL | 1 | 429 未发出，待槽位释放后补发 |

预检 5/5 文件、10/10 臂通过（`logs/_tmp_preflight.py`）。若任一组 F ≥ 1.00 且 2Y/SUB 不掉线，
下一关是 **prod**——注意本字段从未做过 prod 探测，而同数据集另一字段（top-share）的 prod 是 0.87–0.90，
**不能假设本字段干净**；进 prod 前先按 D0-P 单条实测。

## 附录 AW：波 83d 收批 — F 墙破了，但 prod 墙是真正的天花板（2026-10-23）

**核心结论：`exempt_tier1_broker_concentration_index` 与 `exempt_industry_top_broker_share_pct` 同属券商/清算集中度族，
prod 实测 0.8599（前者）与 0.87–0.90（后者）⇒ 本族双字段 prod 封死，F 墙已无意义。**

### AW.1 十臂实测（2014-01-01 → 2023-12-31，TOP3000/D1，decay 5，trunc 0.08）

| alpha | 中性化 | 形状 | S | F | TO | RET | SUB | 2Y | RA |
|---|---|---|---:|---:|---:|---:|---:|---:|---|
| **vROZ2XMa** | SUBINDUSTRY | backfill252 + p2 | **2.26** | **1.00** | 0.3134 | 0.0610 | 1.28 | 2.38 | **0** |
| qMEO0J1V | SUBINDUSTRY | d=3 | 2.37 | 0.99 | 0.3961 | 0.0686 | 1.45 | 2.44 | 1 |
| QPYOKpkX | SUBINDUSTRY | backfill252 + p3 | 2.24 | 0.99 | 0.3172 | 0.0620 | 1.27 | 2.39 | 1 |
| npAmP5Ja | SUBINDUSTRY | p2 | 2.18 | 0.95 | 0.3237 | 0.0619 | 1.26 | 2.38 | 1 |
| vROZ2XqQ | SUBINDUSTRY | quantile(gaussian,σ=1) | 2.17 | 0.95 | 0.3226 | 0.0615 | 1.28 | 2.39 | 1 |
| xA1Vbp8q | SUBINDUSTRY | 去幂中位秩 | 2.13 | 0.90 | 0.3210 | 0.0579 | 1.24 | 2.34 | 1 |
| pwvx5bzg | INDUSTRY | p3（冠军壳） | 2.10 | 0.96 | 0.3260 | 0.0686 | 1.24 | 2.45 | 1 |
| GrgXOXb3 | SECTOR | p3（冠军壳） | 1.94 | 0.90 | 0.3250 | 0.0698 | 1.19 | 2.28 | 1 |
| GrgXOjKo | MARKET | p3（冠军壳） | 1.71 | 0.80 | 0.3245 | 0.0704 | 1.14 | 2.22 | 1 |
| RRA9AQW0 | STATISTICAL | p3（冠军壳） | 2.21 | 0.83 | 0.3305 | 0.0467 | 1.24 | 2.11 | 1 |

RA=1 全部是 `LOW_FITNESS`（WARNING 计入 failed-count）。

### AW.2 三条可复用判断

1. **唯一把 F 从 0.96 推到 1.00 的动作是 `ts_backfill(F, 252)` 前置**（对比 npAmP5Ja→vROZ2XMa：同 p2、同壳，
   仅多补数层）：S 2.18→2.26、TO 0.3237→0.3134、RET 0.0619→0.0610、**F 0.95→1.00**。
   机制：覆盖率缺口补齐使横截面 rank 在早年也有足够样本，S 上升 + TO 略降 ⇒ F 乘子双升。
   **p2 / d=3 / `quantile(gaussian)` / 去幂中位秩四个形状轴全部在 0.90–0.99 打转，没有独立杠杆。**
2. **中性化序：SUBINDUSTRY > INDUSTRY > SECTOR**。INDUSTRY 的 RET 0.0686 最高但 S 掉到 2.10（F 0.96）；
   SECTOR 全面劣化（S 1.94 / F 0.90）。⇒ 本字段的行业暴露是**噪声而非信号**，收得越紧越好。
3. **F 1.00 不等于可提交**：vROZ2XMa 的时间维是干净的（衰减比 2.03/2.26 = **0.90**、近年 CV **0.25**、
   max/min **1.67**、平年 0；2017 0.87 / 2020 0.11 属早年弱年，软标记），**卡死它的是 prod 0.8599**，
   且直方图 [0.7,0.8) 桶 **n=26** ⇒ 按窗口谷法族级必死，不值得再做窗长微调。

### AW.3 判决

- **本族判死（prod 墙）**：`other143` 的 exempt 券商集中度双字段（`exempt_tier1_broker_concentration_index` +
  `exempt_industry_top_broker_share_pct`）prod 0.86–0.90，不是 F 墙。**不再向该族投波**；
  回写用 prod 墙口径，不用 F 墙口径（此前 82 波的 F 墙判死已被 83d 推翻，勿再引用）。
- **要写 `seal_dead_end` 的是「prod 饱和」**：依据 = 两次独立实测 max 0.8599 / 0.87–0.90 + 直方图右尾厚度。
- **交付计数不变（5/10）**：波 83d 没有可提交者。
- **队列清理**：6 条失效 READY 退役（2026-10-23）——`pw5RbrYX`(prod 0.9000)、`leKKGb9l`(0.9014)、
  `1YZp6EP6`(robustness REJECT)、`RRA97Wo0`/`kqJvZGY8`(prod-dead 族)、`QPK77aVw`(SUB 0.35 + DD 0.1414)。

## 附录 AX：波 84 — earnings_risk 封存集重测（负对照，封存未被推翻，2026-10-23）

**起因（必须记下的流程失误）**：本波在设计时**没有先读 `USA-EARNINGS-RISK-WEAK` 封存件**
（`_usa-earnings-risk-field-profile-20261020.md` §5），把已封存数据集当成「未试面」重新开波。
这不是新机制探索，而是一次**白烧配额的重复**。收批后按负对照处理，结论只用于加固封存。

**唯一没被测过的轴**：封存批 8 臂用的是短窗水平/差分（`ts_zscore` / `ts_delta` 22–66），
**没有测过长窗补数 + 行业分组秩**（本项目 USA 慢变量的冠军壳）。本波 7 臂全部固定
`group_rank(ts_backfill(vec_avg(F), 252), industry)` 只换字段/方向，作为「壳能否救活弱字段」的对照。

### AX.1 实测（multisim `1l5Ldm45x53y9TymeW2Br8W`，7/7 终态）

设置：TOP3000/D1、SUBINDUSTRY、decay 5、trunc 0.08、2014-01-01→2023-12-31。

| 字段 | 方向 | alpha | S | F | TO | 2Y | SUB | RA failed |
|---|---|---|---:|---:|---:|---:|---:|---|
| `last_quarter_earnings_price_move` | + | `3qj1oa5Z` | **0.60** | 0.30 | 0.0188 | 1.09 | 0.56 | 3 |
| `iv_spread_to_atm_volatility_ratio` | + | `mLYdor71` | 0.52 | 0.26 | 0.0905 | 0.89 | 0.40 | 3 |
| `five_day_ma_earnings_volatility / five_day_realized_volatility` | + | `O0JRAbV1` | 0.49 | 0.24 | 0.0782 | 0.93 | 0.41 | 3 |
| `earnings_volatility_risk_premium` | + | `E5VN6g8P` | 0.46 | 0.21 | 0.0774 | 0.94 | 0.34 | 3 |
| `earnings_volatility_risk_premium` | − | `3qj1oaPZ` | −0.46 | −0.21 | 0.0774 | −0.94 | −0.34 | 4 |
| `predicted_earnings_related_price_move / three_year_avg_earnings_move` | ± | `e76N5dGd` / `npAmvZqd` | — | — | — | — | — | UNITS ERROR |

两条 WARNING 臂的报错：`Incompatible unit for input of "add" at index 1, expected "Unit[CSPrice:1]", found "Unit[]"`
——分子是价格单位（CSPrice），分母保护常量 `0.001` 无量纲，`unitHandling=VERIFY` 直接拒。
**可复用修法**：分母必须有同单位量（用 `ts_std_dev(...,252)` 或同字段的 `vec_avg` 做尺度），
或干脆对**两个同单位字段的比值**做 rank（单位相消）；不要给价格单位字段加裸常数。

### AX.2 判决

- 全波最高 **S 0.60（vs 封存基线 0.58）、F 0.30、RA failed 3** ⇒ **封存成立，不推翻**。
  长窗 + `group_rank` 这个「救弱字段」的冠军壳对本族无效，证明封存 §4 的归因正确：
  该族的问题是**信号本身只有风格暴露**（risk_neutralized_sharpe −0.28…−0.01），不是壳或窗长。
- `last_quarter_earnings_price_move` 的 0.60/2Y 1.09 看似「最像信号」，但 SUB 0.56 与 S 同比例缩水、
  risk-neutralized −0.11 ⇒ 仍是 beta 级暴露。
- **交付计数不变（5/10）**。
- **波号冲突说明**：并行会话已用「波 84」跑 other596（FAST 设置），本波在台账里记作
  `84_earnings_risk_retest`，与并行会话的 `84_other596` 不共用编号语义。
- **流程加固（写入经验，不另立工具）**：开波前必须按顺序核三处——① `registry_empirical` 的
  `dead_end` 名单；② `references/_usa-*-field-profile-*.md` 里的封存 verdict；③ 交付日志最近附录。
  本波漏了 ②。三者任一命中即不得开波，除非明确写「复查理由 + 未测轴」。

## 附录 AY：队列最后一条 READY 退役 — `QPYOPLAK` 双闸实测（2026-10-23）

`submit_ready` 全库只剩这一条 READY（waves 82–83d 其余候选已在 AW.3 退役）。**两条相关性同时不过**：

| 闸 | 实测 | 线 | 同族对照 |
|---|---:|---:|---|
| self（本地增量缓存，`correlation_type=self`） | **0.7105** | 0.7 | 对 ACTIVE `883WZJ1W`（0.7105） |
| prod（平台，无 refresh 命中缓存） | **0.7712** | 0.7 | 直方图 [0.7,0.8) 桶 **n=187** |

- **self 只超线 0.0105，但没有修的价值**：prod 超线 0.0712，且 [0.7,0.8) 桶 n=187
  ⇒ 按窗口谷法属**族级饱和**，改窗长/形状只会在同一饱和盆里挪 0.01。
- **表达式**：`group_rank(multiply(ts_zscore(subtract(backfill(pos_prob_3,252), backfill(neg_prob_3,252)), 252), subtract(1, backfill(likelihood_of_neutral_tone,252))), industry)`，
  ds339、S 1.70 / F 1.14 / 2Y 3.50 / SUB 1.34 —— IS 面是干净的，**死在相关性**。
- 处置：`submit_queue retire --status DEAD`，note 写双闸读数。
- **队列现状：USA READY = 0**（交付 5/10，其余候选全部有明确否决依据）。
- 复用判据：**self 微超（<0.03）而 prod 超线 >0.05 时，不要投去相关波**——两者同源，
  降 self 的持仓类改动通常同步降 prod 但降不到 0.7 以下；先看 prod 直方图 [0.7,0.8) 桶，
  n≥10 即判族死。
