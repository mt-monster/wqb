# EUR × other（组合分支）

> 回到 [EUR 区域流程](../SKILL.md) · [EUR profile（证据与历史）](../../wq-brain-ra-pipeline/references/regions/EUR.md) · 实时生效画像：`$WQ_PY -m wqb.profiles explain --region EUR --category other`

<!-- profiles:cell-panel:start -->
**状态**：probe（跟区域入场 probe-only）　**分组**：Other　**类别卡**：other

**涉及数据集**：acquisition_model、ai_news_scores、dl_riskfree_returns、event_relation、insider_feats、insider_matrix、insider_trx_matrix、ml_factor_proj、news_sentiment_dl、news_sentiment_nlp、other128、other455、other567、other571、predictive_starmine,pattern_scores

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
| 119 | 0 | 19 | 1 | 20 | 0 |

主要数据集（回测数）：other128（22）、insider_trx_matrix（15）、news_sentiment_nlp（12）、insider_feats（10）、news_sentiment_dl（9）、other571（9）、ai_news_scores（8）、insider_matrix（8）

### S1 字段理解

- 数据集名会骗人：必读字段 description；稀疏高 valueScore 是陷阱
- 窗口（类别卡，均在白名单内）：daily 5/22；quarterly 66/252

### S2 生成

- **说明**：★★★★★ 【EUR × other 数据集实测】（2026-10-13，波 508–523，约 60 条） ／ 数据集 ／ 规模 ／ 最佳 ／ S ／ F ／ TO ／ **returns** ／ 判死依据 ／ ／---／---／---／---:／---:／---:／---:／---／ ／ ★'insider_feats'（内部人买卖比） ／ 118 MATRIX cov .916 αC 43 ／ 'top5_buy_tx_count_250d' / 双窗 add ／ **1.11** ／ 0.60 ／ 0.023 ／ **3.68%** ／ ❌ **returns 天花板 3.9% ⇒ 需 S≥1.84** ／ ／ ★'dl_riskfree_returns'（ML 前瞻收益概率） ／ 133 MATRIX cov **1.000** αC 167 ／ 2quantile **60day** 概率差 ／ **1.40** ／ 0.71 ／ 0.10–0.22 ／ **3.8%** ／ ❌ **returns 天花板 3.8% ⇒ 需 S≥1.82** ／ ／ 'news_sentiment_dl'(αC1)/'news_sentiment_nlp'(αC5)/'acquisition_model' ／ — ／ 情绪/并购概率 ／ ≤0.43 ／ — ／ **0.97–1.45** ／ — ／ ❌ TO 爆炸 ／ ⇒ ★★★ **两者均为 F 闸数学封顶**（F_max@S1.58 = 0.87/0.88 < 1.0）。 **'dl_riskfree_returns' 细节**：horizon 是关键（60d S 1.37 >> 20d 0.29 >> 5d 0.55）；分位越细越差（2q>3q>4q>5q）； 修订类结构（ts_delta / 跨 horizon 差 / rank 差 / 乘 / 除）**全部失败（S≤0.87）**⇒ 该模型信号是「水平」非「变化」。 **'insider_feats' 细节**：buy-only 计数 > buy/sell ratio（验证 JMZ 2003）；250d margin 32bp vs 60d 8.8bp； 'ts_ir'/'ts_std_dev' 分母结构**灾难**（S→0）；'ts_delta' 混合可提 TO（0.023→0.056）而不杀 S。
- **说明**：★★★★★★ 【EUR × other 本轮第二批深挖】（2026-10-14，波 529–536，≈60 条） ① **'techindi_model'（300 MATRIX，cov **1.000**，αC 2072）= 多分位×多 horizon 的**预测收益率模型** （'predicted_{first..fifth}_quantile_{one,five,ten}_day_return_{V}'，V=13/131/14/141/15/16/17）。 ★ **IS 极强**：8/8 探针 S ≥1.5；最优 'QPYZ5ePX' = 'signed_power(group_rank(ts_mean(predicted_fifth_quantile_ten_day_return_15,2), industry), 3.0)' ⇒ **S 3.49 / F 1.53 / TO 0.5422 / 2Y 1.90 / ROBUST 0.87 / sub 1.88**，**returns 反算 10.1%**（EUR 本会话最高）。 ★ **判死 = prod 墙**：6 条实测 prod 0.7213–0.7685，'prod_bucket_scan' 的 **n[0.7,0.8) = 3–4 ⇒ DEAD（单钉子卡死）**。 ⇒ **几何改造确能降 prod**（0.7514→0.7213，用 'ts_zscore(·,252)'）**但同步把 sub/S 压到 0.463** ⇒ sub 失败 ⇒ **无解**。 ② **'stock_search_trends'（Google Trends，αC **2**）/ 'other571'（Wikipedia 浏览，αC 61）双双判死**： 注意力类 TO 0.41–0.98 爆炸（Trends）/ S ≤0.44 且 2Y 1.53 但 S 0.24（Wikipedia，2Y 有 S 无）。 ③ ★★★★★ **两条新闸门铁律（EUR 实测）**： 'LOW_SUB_UNIVERSE_SHARPE' 闸线 = **0.53 × S**（786pLKnb S1.71→0.91；leMpQ5E2 S3.78→2.0） 'LOW_ROBUST_UNIVERSE_SHARPE' 闸线 = **0.7 固定** ⇒ **高 S 是双刃剑**：sub 是**比率闸**，若 'sub/S < 0.53' 则任何 S 都过不了；'ts_zscore' 是最强 S 放大器但压 sub/S。 ④ ★ **降 TO 算子谱**（该数据集实证）：'ts_mean(P,2)' ✅保 robust（TO 0.79→0.542，robust 不变）； 'decay=2' 设置 ✅（TO→0.585，robust 0.86→0.80）；'ts_decay_linear(P,3)' ✅（TO 0.506，robust 0.75）； ❌ 'ts_mean(P,5)' / 'tvr_decay' / 'hump' **均摧毁 robust**（0.87→0.45/0.53/0.55）；'hump' 档位过陡无甜区。 ⑤ ⚠ 'quantile(P, driver=gaussian)' 被 'group_rank' 包裹时是 **no-op**；horizon 期限差完全无效（S ≤0.22）。
- **说明**：★★★★★★★ 【EUR × other 重大突破：双窗秩乘积破 prod 墙】(2026-10-14, wave539–542) **达标候选 #2 = 'e76kv2xE'**（techindi_model, other 未点亮）： 'signed_power(group_rank(multiply(rank(ts_mean(predicted_fifth_quantile_ten_day_return_15,2)), rank(ts_mean(predicted_fifth_quantile_ten_day_return_15,252))), industry), 3.0)' ⇒ S 2.60 / F 1.23 / TO 0.3834 / SUB 1.67 / ROBUST 0.93 / 2Y 1.94 / **returns 8.54%** / **PROD 0.6916** / SELF −0.0149 / Failed RA=0。 ⇒ 与 Analyst 腿 '786pLKnb' 互相关 **0.0907** ⇒ 两条独立腿。 ★★★★★ **通用结构「双窗秩乘积」**：'multiply(rank(ts_mean(F,W_short)), rank(ts_mean(F,W_long)))' —— 相对朴素 'group_rank(ts_mean(F,2))'：**prod 0.7514→0.6916（跨线）+ TO 0.542→0.383 + robust 0.87→0.93 + sub比率 0.539→0.642**（一石四鸟）。 ⚠ **非普适**：sentiment27(1.33→1.14) / dl_riskfree(1.40→1.20) / insider_feats(1.11→1.08,TO 0.032) 均降 S ⇒ 逐数据集实测。 ⚠ **该数据集同族只出 1 颗**：'RRAjKw2b'(prod 0.6824)/'zqrK0nPO'(0.6911) 也过线，但三者互相关 0.81–0.87 ⇒ 同腿。 ⚠ **'pv13' 图网络特征（客户 PageRank / 竞争者 HITS）判死**：近静态 TO 0.012–0.086、S ≤0.13； 且 'pv13_new_*l_scibr' 是 **GROUP 类型**（不能当信号）⇒ 整批 CANCELLED（字段类型坑再现）。
- **说明**：★★★★★★ 【EUR × other 续推收官（wave543–546）】三个假设的证伪/修正： ① **「预测型数据必胜」修正为「只有直接预测收益率的模型有效」**： ✅ 'techindi_model'（预测收益率分位 S 3.41）/ 'dl_riskfree_returns'（收益率概率 S 1.40）； ❌ 'other545' **NEMO 2.0 综合模型评分**（7 子模型聚合 + 价格动量 + NLP 网络动量）**S 仅 0.05–0.63、2Y 全死** ② **双窗秩乘积非普适**：在 'pv1'（经典价量，αC 43728）上 S 反降、2Y 转负；'news18' TO 0.73–0.94 爆炸。 ③ ★ **网络/嵌入型数据集一律近静态**：'pv13'（客户 PageRank/竞争者 HITS）TO 0.012–0.086； 'other455'（竞争者 node2vec → PCA factor）TO **0.010–0.012** ⇒ **S ≤0.12 全灭** ⇒ 与「状态量/评级」同类，**开波前可预筛**。 ⇒ 本会话 EUR 未点亮空间最终产出 = **2 条独立腿**：'786pLKnb'(Analyst) + 'e76kv2xE'(Other/techindi_model)，互相关 0.0907。
- **说明**：★★★★★★ 【EUR 数据集全量普查 + 本轮新铁律（2026-10-14）】 ① **平台权威枚举：EUR 共 173 个数据集 / 14 类**（未点亮 10 类 = 93 个：other36/news20/pv20/sentiment5/insiders3/earnings2/institutions2/macro2/socialmedia2/imbalance1）；已点亮 4 类（model46/fundamental13/analyst16/risk5）。 ⇒ 普查表 + 逐数据集判死速查（死因七分类）见 'references/_dataset-inventory.md'。 ② ★★★ **'earningscall_sentiment'（财报电话会语调，152 字段/137 MATRIX-计数）判死**： 'vec_avg' 后 **TO 1.07–1.57 爆炸**、S ≤0.21 ⇒ 与 news/sentiment 事件 VECTOR 同族。 ⚠ 类型坑：'{topic}_*_score'/'*_polarity'=**VECTOR**（需 vec_avg），'count_*'/'mean_polarity_*'=**MATRIX** ⇒ 混用整批 CANCELLED； 且 'count_negative_cashflow_answer' **不存在**（只有 positive/neutral）。 ③ ★★ **'pv173'（91 VECTOR 全 '*_unit_name'）/'other384'（cov≥0.5=0）/'investor_activity'（cov≥0.5=0）判死**：元数据/低覆盖。 ④ ★★★ 未测集（60 个）以 **news 事件族群（TO 爆炸）+ PV 拥挤族（αC 585–885）+ 微型/低覆盖集** 为主 ⇒ **唯剩的机制性机会 = 'pv29'/'pv30' 的「统计聚类 GROUP 轴」**（GROUP 字段只能当 'group_*' 的第 2 参，不能当信号）。
- **类别通用原语**（类别卡，跨区）：
  - name the priced risk first; the operator is secondary
  - 先按字段 description 判断经济含义，再套对应类别卡的思路（例：KOR other466 是财务比率 → fundamental；IND other532 是 Barra 特质收益 → 残差反转）
- **跨区结论**（KOR/EUR/DEU/GBR；negative）：other455 网络嵌入（n2v）族（证据：KOR RULES §G；EUR-W253-OTHER455-CUSTOMER-NETWORK-RETURNS；DEU-OTH455-PURECOMP-SUBUNIVERSE-WALL-20260923；GBR 红榜） <!-- lint:const-ok 证据原文 -->
- **禁止**（全局锁定）：禁止两条独立信号腿相加：加权（0.4×A + 0.6×B）、等权 add(rank(A), rank(B))、中缀 + 都算；第二个数据集只以条件（trade_when / if_else）、分组（group_rank / bucket）或残差（ts_regression / group_neutralize）入场（原举例 regression_neut / vector_neut 均已被平台移除，2026-10-10 op-lint 实测）
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
| EUR-ACQUISITION-MODEL-COLD-ZERO-YIELD | mna_target_likelihood_percentile (acquisition_model 全 15 字段  | wave218 8 探针全灭 max／sharpe／=0.16（best 2y 1.46 但 IS 无强度），达 EUR profile fast_kill 线（新集 8 探针无 ／S／>=0.5 即判死）。字段全冷门（users<=4）理 | acquisition_model | inferred | <!-- lint:const-ok 证据原文 -->
| EUR-AINEWS-POS-INTENSITY-WEAK |  | Leave ai_news_scores 全部字段族在 EUR。新闻情绪类信号在 EUR D1 普遍无预测力。 | ai_news_scores | payload | <!-- lint:const-ok 证据原文 -->
| EUR-DLRF-BOTH-FAMILIES-DEAD-MATH-PROOF | dl_riskfree_returns 全数据集（ohlcv 通用族 + eur_ohlc_ma 专用族） | Leave dl_riskfree_returns 全数据集在 EUR（含 ohlcv 与 eur_ohlc_ma 两族、133 字段）。后续如遇同类型 DL 分位数预测数据集，先用 Fitness 墙预筛判据评估，再决定是否开波。 | dl_riskfree_returns | payload | <!-- lint:const-ok 证据原文 -->
| EUR-DLRF-EUROHLCMA-TURNOVER-FITNESS-WALL | dl_riskfree_returns eur_ohlc_ma EUR 专用模型族 × 跨期分位数差 | Leave dl_riskfree_returns 的 eur_ohlc_ma 族跨期分位数差在 EUR：prod 极低但 Fitness 墙结构性不可破（turnover 源于数据更新频率，非表达式可修）。不再试 label 对/期限对/ | dl_riskfree_returns | payload | <!-- lint:const-ok 证据原文 -->
| EUR-DLRF-OHLCV-PRODWALL-FIELD-LEVEL | dl_riskfree_returns ohlcv 通用模型字段族 × 四种算子几何 | Leave dl_riskfree_returns 的 *_ohlcv 通用模型字段族在 EUR：IS 强但 prod 墙字段级不可破，任何算子几何变换无效。转向 *_eur_ohlc_ma EUR 专用字段族（prod 低但 IS 弱，需 | dl_riskfree_returns | payload | <!-- lint:const-ok 证据原文 -->
| EUR-DLRF-PROD-WALL-080 |  | Leave dl_riskfree_returns 的 quantile_label_1bucket/probability_label 分位数概率族在 EUR。信号强但 prod 墙结构性不可破。如需复用，仅在多区域组合中作为低权重稀释腿 | dl_riskfree_returns | payload | <!-- lint:const-ok 证据原文 -->
| EUR-DLRFR-OHLCV-GEOM-WALL | dl_riskfree_returns |  | dl_riskfree_returns | payload | <!-- lint:const-ok 证据原文 -->
| EUR-EVENT-RELATION-WEAK | event_relation 实体关系强度族（relation_strength_rank/score × merger | wave233 8 探针全灭 max／sharpe／=0.43 < 0.5 → 达 EUR fast_kill 判死线。字段全冷门（users<=1）理论 prod≈0，纯信号缺席。OTHER 塔已连续三集判死（acquisition_mo | event_relation | inferred | <!-- lint:const-ok 证据原文 -->
| EUR-INSIDER-FEATS-WEAK | insider_feats 内部人买卖比率族（buy/sell ratio × tx count × lookback） | wave238 10 探针全灭 best ／sharpe／=0.47 < 0.5 → 达 fast_kill 判死线。此前 w232 多样性闸（flow 单 exposure）+ 字段名拼接幻觉 + 低覆盖无 backfill 三轮门禁墙已 | insider_feats | inferred | <!-- lint:const-ok 证据原文 -->
| EUR-MLFP-0ALPHA-OPS-WEAK | ml_factor_proj 0-alpha coverage/rating/CCC/capex | Leave this ml_factor_proj ops/coverage family. Do not replay Wave9 EPS/price/FCF ranks. Next: predictive_starmine high-c | ml_factor_proj | payload | <!-- lint:const-ok 证据原文 -->
| EUR-NSNLP-SPARSE-TWO-WALLS |  | Leave news_sentiment_nlp 全部字段族在 EUR。稀疏事件流的 CW+turnover 双墙是结构性问题，不是信号问题。 | news_sentiment_nlp | payload | <!-- lint:const-ok 证据原文 -->
| EUR-O567-COVERAGE-STRUCTURAL |  | Leave other567 在 EUR。员工评价数据在 EUR 市场覆盖率不足，无法形成有效横截面分散。 | other567 | payload | <!-- lint:const-ok 证据原文 -->
| EUR-STAR-ARM-LEFTOVER-WEAK | starmine ARM preferred/revenue/score-change/region-global as | weaker than surprise x common_gap_up | predictive_starmine,pattern_scores | payload | <!-- lint:const-ok 证据原文 -->
| EUR-STAR-GAP-FACTOR-NEUT-WEAK | predictive_starmine surprise x common_gap_up factor neutrali | factor neutralization kills F vs SUBINDUSTRY, does not produce RN>1 | predictive_starmine,pattern_scores | payload | <!-- lint:const-ok 证据原文 -->
| EUR-W253-OTHER455-CUSTOMER-NETWORK-RETURNS | other455 customer network monthly returns seed1 k5 |  | other455 | payload | <!-- lint:const-ok 证据原文 -->
| EUR-ai_news_scores-ADVANCED-NEG | ai_news_scores advanced stats |  | ai_news_scores | payload | <!-- lint:const-ok 证据原文 -->
| EUR-insider_trx_matrix-WEAK-DRIFT | insider |  | insider_trx_matrix | payload | <!-- lint:const-ok 证据原文 -->
| EUR-news_sentiment_dl-SENTIMENT-WEAK | news_sentiment_dl sentiment word stats | Leave news_sentiment_dl sentiment word stats and text complexity in EUR. Do not retry ts_mean/ts_std_dev/ts_delta on pos | news_sentiment_dl | payload | <!-- lint:const-ok 证据原文 -->
| EUR-news_sentiment_nlp-STRUCTURE-DEAD | news_sentiment_structure |  | news_sentiment_nlp | payload | <!-- lint:const-ok 证据原文 -->
| EUR-other571-WIKI-WEAK | other571 Wikipedia page views | Leave other571 Wikipedia page views in EUR. Do not retry ts_mean/ts_delta/ts_decay_linear/zscore on oth571_views* fields | other571 | payload | <!-- lint:const-ok 证据原文 -->
<!-- profiles:cell-panel:end -->

## 补充说明（手写）

<!-- profiles:manual:start -->
<!-- profiles:manual:end -->
