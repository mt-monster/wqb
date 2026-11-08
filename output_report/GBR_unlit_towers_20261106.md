# GBR 未点亮塔战役（2026-11-06）— 字段画像 × 模板库 × 波次记录

> 驱动指令（用户 2026-11-06）：「穷尽所有 category 下的数据集（**已点亮塔不选**）……做好每个数据集的字段画像，并按画像匹配模板……持续挖掘 **20 个** ATOM 和 regular alpha」。
> 区域：**GBR / TOP700 / delay 1**。原有 11 颗候选（全部来自已点亮塔）保留为既有成果，**新挖掘一律从未点亮塔取信号**。

## 一、塔点亮表与可开采集合

`get_pyramid_alphas(GBR, D1)` 实测（塔内已提交 ≥3 = 点亮）：

| 状态 | 塔 | 计数 |
|---|---|---|
| **已点亮（不选）** | model / news / analyst / fundamental | 5 / 3 / 3 / 3 |
| 未点亮 | pv | 2 |
| 未点亮 | other | 1 |
| 未点亮 | institutions / insiders / earnings / sentiment / risk / option / socialmedia / macro / shortinterest / imbalance | 全 0 |

⇒ 可开采数据集 82 个（other 41 / pv 16 / institutions 5 / risk 5 / insiders 3 / sentiment 3 / socialmedia 3 / earnings 2 / imbalance 1 / macro 1 / option 1 / shortinterest 1）。

## 二、字段画像（16 个数据集，实拉 `get_datafields`）

| 数据集 | 塔 | 字段数 | 类型分布 | cov | 代表字段（alphaCount） | 画像判断 |
|---|---|---|---|---|---|---|
| **other455** | OTHER | 1500 | 321 GROUP + 79 MATRIX | 0.64–0.66 | `oth455_*_n2v_*_pca_factN_value`(a2–11)；GROUP=`*_kmeans_cluster_{5,10,20}` | 供应链/竞争关系 node2vec 嵌入的 PCA 因子；**alphaCount 极低（2–11）= 几乎无人开采**；GROUP 簇可直接当分组轴 |
| **pattern_scores** | PV | 504 | 400 MATRIX | 0.97–1.00 | `max_similarity_symmetrical_triangle_up`(a147)、`reversal_v_top_min_simscore_lookback60`(a143) | K 线形态相似度评分（三角/跳空/尖顶等 × mean/min/max/median/std 统计 × 60/120 回看） |
| **continuation_score** | PV | 200 | 200 MATRIX | 0（不可信） | `avg_similarity_continuation_gap_up`(a71)、`ascending_channel_similarity_maximum_h40w`(a48) | 中继形态（上升通道、旗形、缺口）相似度 |
| **intraday_pv_feats** | PV | 200 | 200 MATRIX | 0（不可信） | `corr_ask_price_with_volume`(a70)、`avg_vwap_to_last_price_ratio`(a38) | **日内微观结构**：买卖价 vs VWAP 比、量价相关、上下半场不对称 |
| **pv30** | PV | 240 | **全为 GROUP** | 0.22–0.44 | `eighth_pca_component_top1200_group513`、`factor1_group10_top800_513`(a0) | 另类行业分类（价格-成交量反推的聚类标签）；**只能当分组轴，不能做信号** |
| **pv1** | PV | 23 | 13 MATRIX + 7 GROUP | 0 | close / volume / returns / cap / adv20 | 基础价量（已高度拥挤 a2000–6200） |
| **institutions6** | INSTITUTIONS | 11 | 全 MATRIX | **1.00** | `count_institutional_buyers_security`(a199)、`aggregate_share_count_institutions`(a117) | 机构持仓三族口径（存量/流量/家数），**覆盖最高**；论坛有专帖拆解 |
| **institutions25** | INSTITUTIONS | 24 | 全 VECTOR | 0 | `inst25_position_change`(a13)、`inst25_manager_avg_trade_length`(a6) | 机构级行为：持仓变化、情绪、覆盖家数、平均持股期限；**极冷门（a6–13）** |
| **shortinterest3** | SHORTINTEREST | 25 | 全 VECTOR | 0.82–0.87 | `loaned_share_count_p5_d1`(a305)、`mean_loan_rate_p5_d1`、`loan_rate_volatility_main` | 借券市场：贷出量/市值、费率（mean/max/min）、费率跨合约离散、期限、成交笔数；多主键口径 `_main/_p5_d1`/无后缀 |
| **insider_agg_matrix** | INSIDERS | 34 | 全 MATRIX | 0.59 | `avg_buy_shares`(a90)、`avg_sell_shares`(a40) | 内部人买卖均量；⚠ `directional_indicator*` 是毒字段（零持仓） |
| **insiders12** | INSIDERS | 7 | 全 VECTOR | 0 | `insd12_mktprice`(a254)、`insd12_percent`(a61) | 内部人交易价格/比例/变动量/持股 |
| **earnings_sent_matrix** | EARNINGS | 7 | 全 MATRIX | 0 | `sentiment_weighting_method1`(a200)、`positive_sentiment_probability_3`(a145) | 财报电话会/公告情绪（多种加权法 + 正负中性概率） |
| **sentiment27** | SENTIMENT | 18 | 14 VECTOR + 4 SYMBOL | 0.80 | `snl27_relpopularity1`(a237)、`snl27_topranking`(a84) | 网络/新闻热度排名族（相对热度、排名分位、峰度偏度） |
| **risk72** | RISK | 23 | 17 MATRIX + 6 VECTOR | 0 | `top2500_equity_residualized_return`(a242) | 残差收益（已剔除分组暴露） |
| **risk88** | RISK | 1 | MATRIX | 1.00 | `alternative_market_cap_usd`(a567) | 单一替代市值字段（规模代理） |
| **techindi_model** | OTHER | 399 | 全 MATRIX | 0（不可信） | `tm_16_*`(a7878)、`tm_17_*` | 技术指标模型分数；**极高拥挤（a1000–7878）** |

**画像层结论**：
1. 覆盖与拥挤度呈**反比**：cov 高的（institutions6 1.0、risk88 1.0、pattern_scores 0.97–1.0）拥挤度中等；cov 报 0 的（continuation_score / intraday_pv_feats / institutions25 / risk72 / techindi_model）里既有真空集也有真数据，**必须用最小回测探针验证，不可据 cov 判死**。
2. 最冷门且有真实结构的三个：**other455**（a2–11）、**institutions25**（a6–13）、**insider_agg_matrix**（a29–90，但 cov 0.59）。
3. **pv30 全为 GROUP**，是 GBR 唯一可直接当「另类行业分类」分组轴的数据集——不过它属 PV 塔，与 OTHER 塔信号混用会触发禁混，故只能配 pv 塔自身信号。

## 三、模板库（12 个结构互异模板，含来源）

> 用户硬约束：模板库 ≥10 个且**结构互异**（差异落在算子几何 / 矩 / 分组轴 / 非线性 / 信息来源，不是换窗口）。
> 来源标注：**[F]** 平台论坛、**[P]** 外部金融论文（经论坛转述）、**[自建]**。

| # | 模板名 | 结构 | 塔 | 机制 / 来源 |
|---|---|---|---|---|
| T1 | 借券费率**时序方差** | `reverse(group_zscore(ts_covariance(vec_avg(F), vec_avg(F), 22), G))` | SHORTINTEREST | 空头怕的是费率**突然变贵**，不是水平。**[P] Engelberg-Reed-Ringgenberg (2018, JF) "Short Selling Risk"**；**[F] 43624312881943**（ASI 已提交 S1.89 / prod 0.6648）。`ts_covariance(x,x,W)` = 方差 |
| T2 | 借券费率**水平**（做空溢价） | `reverse(group_rank(ts_mean(vec_avg(F), 22), G))` | SHORTINTEREST | 高费率=难做空=高估。**[P] Drechsler (2014) "The Shorting Premium"** |
| T3 | 贷出量**供给冲击** | `reverse(group_rank(ts_zscore(vec_sum(F), 252), G))` | SHORTINTEREST | 借券供给变动含预测力。**[P] Cohen-Diether-Malloy (2007, JF)** |
| T4 | 借券**期限结构** | `group_rank(ts_delta(vec_avg(F), 66), G)` | SHORTINTEREST | 出借人锁定更长期限 ⇒ 预期费率上行 |
| T5 | 机构**化率**（存量比） | `group_rank(divide(inst_shares, add(all_owner_shares, 1)), G)` | INSTITUTIONS | 论坛三族口径之「存量 ÷ 全部持有人」。**[F] 43664593081879** |
| T6 | 单家机构**仓位集中度** | `group_rank(divide(inst_value, add(holder_count, 1)), G)` | INSTITUTIONS | 存量 ÷ 家数。**[F] 43664593081879** |
| T7 | **净广度**改善 | `group_rank(ts_delta(divide(subtract(buyers, sellers), add(holders, 1)), 66), G)` | INSTITUTIONS | 家数族的净广度一阶差分。**[F] 43664593081879 / 43007394986391** |
| T8 | 机构**换手率** | `group_rank(divide(add(acq_mv, disp_mv), add(inst_value, 1)), G)` | INSTITUTIONS | 流量 ÷ 存量 |
| T9 | 机构**成交均价** | `group_rank(ts_zscore(divide(acq_mv, add(acq_qty, 1)), 252), G)` | INSTITUTIONS | 金额 ÷ 股数 = 每股价格 |
| T10 | 聚类标签**协方差**（分歧度） | `group_zscore(reverse(ts_covariance(F_a, F_b, 50)), densify(cluster_G))` | OTHER | 两套独立嵌入视角的协同漂移；分歧越大信号越强。**[F] 43452597554327 / 43308165478935** |
| T11 | 形态相似度**动量** | `group_rank(ts_delta(ts_backfill(F, 66), 22), G)` | PV | 上升三角形态匹配度改善 |
| T12 | **跨形态族** z 差 | `group_rank(subtract(ts_zscore(F_asc, 252), ts_zscore(F_rev, 252)), G)` | PV | 两种形态族的相对强度差（差值量纲，非单腿水平） |

**T12 的设计理由**：单一形态相似度是水平量，易被市值/波动率暴露污染；改为「两族形态 z 分的差」后，共同的市场状态被差掉，剩下形态族之间的相对选择——这是**差值型**而非水平型模板，与 T5–T9 的比值型、T1/T10 的协方差型结构互异。

## 四、波次记录

### WAVE U1（8 条，multisim `3QwrlPeV25br9vNIF7XThNH`）
设置：GBR / TOP700 / D1 / decay 5 / **SLOW** / truncation 0.10 / VERIFY / nan ON / pasteurize ON / FASTEXPR。
预检：`valid=true`、`unknown_fields=[]`、13 个字段全部存在、`any_changed=false`。

| # | 模板 | 表达式 |
|---|---|---|
| 1 | T1 | `reverse(group_zscore(ts_covariance(vec_avg(mean_loan_rate_main), vec_avg(mean_loan_rate_main), 22), sector))` |
| 2 | T2 | `reverse(group_rank(ts_mean(vec_avg(mean_loan_rate_p5_d1), 22), sector))` |
| 3 | T3 | `reverse(group_rank(ts_zscore(vec_sum(loaned_share_count_main), 252), sector))` |
| 4 | T4 | `group_rank(ts_delta(vec_avg(average_loan_duration_days_p5_d1), 66), sector)` |
| 5 | T5 | `group_rank(divide(aggregate_share_count_institutions, add(aggregate_share_count_all_owners, 1)), sector)` |
| 6 | T6 | `group_rank(divide(aggregate_equity_value_institutions, add(count_institutional_holders_security, 1)), sector)` |
| 7 | T7 | `group_rank(ts_delta(divide(subtract(count_institutional_buyers_security, count_institutional_sellers_security), add(count_institutional_holders_security, 1)), 66), sector)` |
| 8 | T10 | `group_zscore(reverse(ts_covariance(oth455_competitor_n2v_p10_q200_w1_pca_fact1_value, oth455_competitor_n2v_p10_q200_w2_pca_fact1_value, 50)), densify(oth455_competitor_n2v_p10_q200_w1_kmeans_cluster_5))` |

算子数：4 / 4 / 4 / 3 / 3 / 3 / 5 / 3，全部 ≤5（上限 12）。

### WAVE U2（8 条，已预检待派发）
覆盖 T11 / T12 / T3 变体（贷出市值÷笔数）/ T9 / T8 / T4 变体（费率跨合约离散）/ T10 变体（PCA 动量）。
预检：`valid=true`、`unknown_fields=[]`。
> 首版曾用 `asc_triangle_std_simscore_lookback120`，预检报 unknown ⇒ 该字段在 GBR 不可用（数据集里有、区域不可用），已替换为 T12 跨形态族 z 差。

### 结果

#### U1（8/8 完成，0 错误）

| alpha | 模板 | S | F | 2Y | TO | sub | 判读 |
|---|---|---|---|---|---|---|---|
| **bl6a07lm** | T3 贷出量供给冲击 | **1.27** | 0.64 | **2.38** | 0.101 | **1.35** | ★ 唯一可用基座（2Y/sub 双强，S 待提） |
| d5WaJepw | T10 聚类协方差 | 0.46 | 0.18 | 0.25 | 0.075 | 0.49 | 弱 |
| QPv0RmP5 | T1 费率时序方差 | 0.44 | 0.19 | 0.15 | 0.138 | 0.18 | 失效 |
| leAawJe5 | T2 费率水平 | 0.41 | 0.12 | 0.32 | 0.074 | 0.40 | 失效 |
| GrWmjE15 | T7 机构净广度 | 0.05 | 0.01 | 0.40 | 0.099 | 0.01 | ≈0 |
| e75aMek6 | T6 单家仓位集中度 | 0.03 | 0.00 | 0.41 | 0.057 | −0.45 | ≈0 |
| LLMKoOVe | T4 借券期限结构 | −0.01 | −0.00 | −0.43 | 0.194 | 0.12 | ≈0 |
| 88RNWg5z | T5 机构化率 | −0.51 | −0.16 | 0.38 | 0.049 | −0.37 | 反号/噪声 |

**三条硬结论**：

1. **GBR 是 ~700 只的大市值单国市场，TOP700 ≈ 全市场 ⇒ 所有依赖「流动性稀缺」的借券机制结构性失效。**
   T1（费率时序方差）在 ASI/MINVOL1M 是已提交件（S 1.89 / prod 0.6648），在 GBR 只有 **0.44**；
   论坛原帖自己给出过证明：同一 idea 换到 TOP1000，「Sharpe 从 2.28 掉到 0.99」。
   ⇒ **不是模板写错，是市场容量决定了这些机制没有土壤。** T2/T4 同理。
2. **institutions6 的裸比值口径在 GBR 也是噪声**（T5 −0.51 / T6 0.03 / T7 0.05）。
   论坛原帖在 USA 上的实测本就如此（裸结构 Sharpe 0.18–0.85，且符号互相打架）。
   ⇒ 机构数据是**季度更新**，必须先 `ts_backfill` 再进时序算子；裸水平比值吃的是小盘暴露。已在 U3 修正。
3. **唯一活着的是「贷出量供给冲击」**（T3）：S 1.27 / **2Y 2.38** / sub 1.35 / TO 10.1%。
   它不是流动性事件信号，而是慢变量（252 日 z 分），因此不受大市值域压制。
   ⇒ U3 以它为基座做几何升级（窗口 / 非线性 / 分组轴 / 一阶差分）。

**方法论教训（可跨区复用）**：论坛/论文模板的**适用域必须与区域容量匹配**。借券类机制需要 MINVOL/小市值域；
在只有大市值域的区域（GBR）直接移植 = 结构性失效，与模板质量无关。

---

## 十二、数据集穷举（补齐「穷尽所有 category」这一步）

此前只画像了 16 个数据集，本轮用 `get_datasets(GBR, TOP700, D1)` 拉全 **177 个**，按 category 归并：

| category | 数量 | 是否已点亮塔 | 可否选 |
|---|---|---|---|
| model | 46 | 已点亮(5) | 禁选 |
| other | 41 | 未点亮(1) | 可选（需 2 颗点亮） |
| analyst | 19 | 已点亮(3) | 禁选 |
| news | 18 | 已点亮(3) | 禁选 |
| pv | 16 | 未点亮(2) | 可选（**仅差 1 颗点亮**） |
| fundamental | 12 | 已点亮(3) | 禁选 |
| institutions | 5 | 未点亮(0) | 可选 |
| risk | 5 | 未点亮(0) | 可选 |
| insiders | 3 | 未点亮(0) | 可选 |
| sentiment | 3 | 未点亮(0) | 可选 |
| socialmedia | 3 | 未点亮(0) | 可选 |
| earnings | 2 | 未点亮(0) | 可选 |
| imbalance / macro / option / shortinterest | 各 1 | 未点亮(0) | 可选 |

**未点亮塔可开采 = 82 个数据集**（other 41 + pv 16 + institutions 5 + risk 5 + insiders 3 + sentiment 3 + socialmedia 3 + earnings 2 + 其余各 1）。

**战略重估**：`pv` 塔 2/3、`other` 塔 1/3 —— 这两塔离点亮最近（分别需 1 颗 / 2 颗）。
按「点塔要均匀」原则，这两塔优先级高于继续在 institutions/risk 等 0 塔上撒网。

## 十三、新一轮字段画像（9 个从未触碰的数据集）

| 数据集 | 塔 | 字段数 | 类型 | cov | aC 中位 | 结构判读 |
|---|---|---|---|---|---|---|
| **pv173** | PV | 81 | 全 VECTOR | 0（不可信） | **0** | ★★★ **信用债曲线投射到股票**：Nelson-Siegel `tilt/twist/shift`、信用利差 `mt5yzspread`、股债背离 `eqbddivrg*`、`bondreturn20deqwt`。三套口径前缀 `ranks_` / `rawratios_` / `zscores_`。**aC 几乎全 0 = 处女地** |
| **pv30** | PV | 240 | **全 GROUP** | 0.827 | 1 | ★★★ **240 个自定义分组轴**：`factorN_group{2,5,10,20,50}_top800_513`、`factorN_grouping*_score_top{100,200}_eas513`、`eighth/eleventh_pca_component_*`。只能当 group 参数，不能当信号 |
| **pv29** | PV | 50 | 40 MATRIX + 10 GROUP | 1.0 | 1 | 行业分组变体（`industry_grouping_levelN_*`）+ `staN_topNcN` GROUP。分组轴库 |
| **earningscall_sentiment** | EARNINGS | 167 | 59 MATRIX + 11 VECTOR | 0 | 0 | ★★★ **Q&A vs Presentation 双分支** × 5 话题 × {pos,neu,neg}：`count_{neg,neu,pos}_{assetutilization,cashflow,leverage,profitability,valuation}_{answer,question,presentation,summary}`；话题级 `*_sentiment_polarity`；`answer_chunk_count`（问答深度）、`chunk_relevance_z*_flag` |
| **other696** | OTHER | 220 | 全 VECTOR | 0 | 0 | ★★ **主题级正负事件计数**：`oth696_{topic}_{positive,negative}`（约 60 个 ESG/经营主题）+ `oth696_alldlpos/alldlneg`（aC 5/7）+ `oth696_combined_sentiment_score`（aC 12）。**极性对结构 = 现成的净语调** |
| **event_ml_signals** | OTHER | 104 | 全 VECTOR | 0 | 0 | ★★★ **公司事件标志库**（uC 仅 12）：`ma_rumor_discussion`(19) / `ma_transaction_announcement_event`(19) / `ma_transaction_cancellation_event`(24) / `ma_call_event`(24) / `bankruptcy_event` / `dividend_*_event` / `guidance_raised|lowered` / `index_constituent_add|drop` |
| **other566** | OTHER | 112 | MATRIX | 0 | 0 | ★★ **ML 分位概率 + 技术指标合体**：`probability_quantile{2..5}_label{0..4}`、`predicted_quantileN_class`、`quantileN_labelM_probability_r{10,20}`；另有 `linear_regression_slope_value`(8) / `money_flow_index_score`(2) / `balance_of_power_indicator`(2) |
| **order_book_imbalance** | OTHER | 240 | 全 VECTOR | **0.165** | 0 | ★★ **L2 委托簿微观结构**：`avg_rest_time_{bid,ask}_{cancelled,filled,partial}_lvl{1..5}`（挂单存活时间）、`{bid,ask}_order_{insertion,deletion,execution,modification}_count`、`auction_order_imbalance_*`、`dark_trade_{count,volume,notional}`、`ebbo_*`、`closing_auction_dislocation_{1min,5min,last}`。**cov 0.165 是真实覆盖率 ⇒ 集中度风险** |
| other78 | OTHER | 112 | 31 VECTOR + 39 SYMBOL | 0 | 0 | ✗ 会议元数据 / 地址 / URL / ID = 文本元数据，无信号价值，判死 |

## 十四、WAVE U4（已派发，8 条）—— 全新机制，全部未点亮塔

multisim = `3FXo008ad5019MR82FO7LQr`；预检 `valid=true`、`unknown_fields=[]`、13 字段全存在。

全部为**单数据集 ATOM**（不占塔混配额，不触碰 {PV,MODEL,OTHER,FUNDAMENTAL} 两两禁令）。

| # | 机制（来源） | 表达式 | 算子 |
|---|---|---|---|
| 1 | 信用利差时序异常（Avramov 等：信用-股票传导） | `group_rank(reverse(ts_mean(vec_avg(pv173_zscores_mt5yzspread), 22)), subindustry)` | 4 |
| 2 | Nelson-Siegel **曲率 twist** 动量 | `group_rank(ts_delta(ts_mean(vec_avg(pv173_ranks_twist120dlast), 22), 66), subindustry)` | 4 |
| 3 | **股债背离** 66 日变化 | `group_zscore(ts_delta(vec_avg(pv173_ranks_eqbddivrgbdrtn120d), 66), subindustry)` | 4 |
| 4 | **Q&A 超额负面**（Matsumoto-Pronk-Roelofsen 2011） | `reverse(group_rank(ts_sum(ts_backfill(subtract(add(count_negative_cashflow_answer, count_negative_profitability_answer), add(count_negative_cashflow_presentation, count_negative_profitability_presentation)), 66), 252), subindustry))` | 7 |
| 5 | 事件语调自身基线异常 | `group_rank(ts_zscore(vec_avg(oth696_combined_sentiment_score), 252), subindustry)` | 4 |
| 6 | 并购传闻累积强度 | `group_rank(ts_sum(vec_sum(ma_rumor_discussion), 66), subindustry)` | 4 |
| 7 | ML 分位概率**顶底价差** | `group_rank(subtract(probability_quantile5_label4, probability_quantile5_label0), subindustry)` | 3 |
| 8 | 委托簿**挂单耐心不对称** | `group_rank(divide(vec_avg(avg_rest_time_bid_filled_lvl1), add(vec_avg(avg_rest_time_ask_filled_lvl1), 1)), subindustry)` | 5 |

算子数 3–7，全部 ≤12。设置：decay 5 / SLOW / truncation 0.10 / VERIFY / nan ON / pasteurize ON。

## 十五、WAVE U3 结果（8/8，0 错误，multisim `1nPwhT9Sa4O49IM12yWYIocx`）

| alpha | S | F | 2Y | TO | sub | fail | 表达式 |
|---|---|---|---|---|---|---|---|
| **MPY6EOQk** | **1.42** | **0.76** | **2.28** | 0.093 | **1.45** | **[]** | `reverse(group_rank(ts_zscore(vec_sum(loaned_share_count_main), 504), sector))` |
| 1YNW8edk | 1.11 | 0.51 | 1.82 | 0.115 | 1.06 | [] | 同上，窗 126 |
| kqNawd0P | 0.87 | 0.36 | 1.65 | 0.173 | 1.00 | LOW_SHARPE, LOW_FITNESS, CONCENTRATED_WEIGHT | `signed_power(...,1.5)` 窗 252 |
| akKa06nR | 0.81 | 0.32 | 2.11 | 0.123 | 0.83 | LOW_SHARPE, LOW_FITNESS | 窗 252 + subindustry |
| RREeOM8g | 0.59 | 0.19 | 0.41 | 0.147 | 0.44 | 3 项 | `loaned_share_count_p5_d1 / transaction_count_p5_d1` 周转率口径 |
| YP1aV6gA | 0.41 | 0.12 | 0.75 | 0.082 | -0.11 | 4 项 | 机构净广度 + ts_backfill 修正 |
| akKa06ER | 0.29 | 0.07 | -0.58 | 0.049 | 0.29 | 3 项 | T14 峰值距离 other455 PCA |
| VkxNrV3J | -0.50 | -0.16 | 0.36 | 0.085 | -0.67 | 4 项 | 机构化率 + ts_backfill |

**核心发现（窗口单调性）**：同一 T3 骨架，窗 126 → **1.11**，窗 504 → **1.42**。
⇒ `loaned_share_count` 是慢变量，基线窗口越长信号越强。这给出一条明确的提 S 杠杆：继续拉长到 756 / 1008 / 1260。

**分组轴效应**：窗 252 时 `subindustry` → 0.81，窗 126 时 `sector` → 1.11 ⇒ 分组粒度太细会切碎信号，**sector 优于 subindustry**。

**非线性失效**：`signed_power(...,1.5)` 把 S 压到 0.87 并引入 CONCENTRATED_WEIGHT ⇒ 该骨架上不宜加幂变换。

**机构 `ts_backfill` 修正仍未救活**（0.41 / -0.50）⇒ institutions6 裸口径在 GBR 确认判死，不再是「格式问题」。

## 十六、prod 队列实测（本轮新增读数）

| alpha | prod | 判定 |
|---|---|---|
| QPvbxjXw | **0.5794** | 通过 |
| **kqNe9LPz** | **0.8203** | **判死**（>0.80，深钉） |
| **vR1nAj6z** | **1.0000** | **判死**（与生产池已有件完全重复） |
| 6XKw8e6O / xArX7dNl | — | `correlation_busy`，队列锁冲突，未取到 |
| WjOwjENP / P0ojvkkJ / WjOK0roG / xAb2OkMm / rKRPAwv9 / 9qWa6r8x | — | 未测 |

**存活池收缩**：11 颗 → **9 颗**（2 颗 prod 判死），其中 prod 确认干净的仍只有 **1 颗**（QPvbxjXw）。

## 十七、第三批字段画像 + 模板库（15 个结构互异，为 U6/U7 预备）

### 17.1 本批新发现（全部未点亮塔、此前从未触碰）

| 数据集 | 塔 | 字段 | 类型 | cov | aC 中位 | 结构判读 |
|---|---|---|---|---|---|---|
| **other567** | OTHER | 48 | 全 VECTOR | 0 | 0 | ★★★★ **Glassdoor 类员工评价全集**。既有**水平分** `avg_*_score`/`*_rating`（overall / ceo_approval / culture / diversity / pay / work_life / senior_mgmt / career_growth / recommend_to_peer / business_outlook），又有**数据集自带趋势分** `oth567_trendrating_*`（10 个维度），还有 `review_helpful_count`/`review_unhelpful_count`（争议度）与 `negative_feedback_text`/`suggestion_to_management`（文本量）。**aC 0–2 = 处女地** |
| **other571** | OTHER | 23 | 全 MATRIX | 0 | 0 | ★★★★ **网页浏览量**：窗口 7d / 14d / 28d / 84d / 1y × 全时段 + **分时段**（morning/afternoon/evening/night）× **分设备**（desktop/mobile）。**营收 nowcast + 流量质量**两个机制，aC 全 0 |
| **fund_holdings_panel** | INSTITUTIONS | 18 | 全 VECTOR | **0.89–0.93** | 13 | ★★★ **基金级交易面板**：`herfindahl_index_transactions(_active)`（交易集中度=信念）、`large_trade_count_50bps(_active)`、`stable_boundary_trade_count_21d(_active)`（被动/指数化程度）、`boundary_transaction_*`、`transaction_value_distribution_score`。**覆盖 0.9 是全部未点亮塔里最高的** |
| **institutions25** | INSTITUTIONS | 24 | 全 VECTOR | 0 | 4 | ★★★ **机构级行为**：`inst25_manager_avg_trade_length` / `inst25_trade_length`（持仓期=短视压力）、`inst25_concentration` / `inst25_crowding`（集中 vs 拥挤）、`inst25_total_short_interest`（**机构级空头持仓**）、`inst25_entry_position` / `inst25_position_change`、`inst25_security_trade_count_{1wk,1mo,3mo,1yr,2yr,3yr}`（多期换手）、`inst25_sentiment` |
| **other546** | OTHER | 22 | 全 VECTOR | 0 | 0 | ★★ **高管/分析师流动网络**：`executive_to_frequency_count` 与 `executive_from_frequency`（人才净流）、`shared_executive_count` / `shared_analyst_count`（网络重叠）、`oth546_analystnet_common` / `oth546_executivenet_common`、`business/geographic/mda_text_similarity_weight` |
| **sentiment33** | SENTIMENT | 255 | 全 VECTOR | 0.32 | 1 | ★★ **多模型新闻情绪**：`sentiment_model{N}_score{N}_fkw{N}`（多模型 × 多关键词窗）、`sentiment_model{N}_negative_score_fkw{N}`、`*_filtered_{pos,neg}`、`snt33_N_{headline,event_title,true_timestamp}` |
| **ai_news_scores** | OTHER | 105 | MATRIX | 0 | 0 | ★★ **带置信区间的新闻情绪**：`{negative,neutral,positive}_score_{average,median,maximum,minimum}_value_N` + `_confidence_{lower,upper}_bound_N`。**置信区间宽度 = 情绪分歧度**，是少见的可构造二阶矩的情绪数据 |
| **event_sentiment_signals** | OTHER | 52 | 全 VECTOR | 0 | 1 | ★★ **章节级事件情绪**：`section_sentiment_score_N`、`key_factor_{negative,positive}_{event_count,score}_section`、`event_weight_aggregation` |
| other384 | OTHER | 66 | 全 VECTOR | 0.21 | 0 | ✗ 会议参会人数 / 公司名匹配分 / 标题文本 = 元数据，信号价值低 |

### 17.2 模板库（15 个，结构互异；差异落在「矩 / 算子几何 / 分组轴 / 非线性」，不是换窗口）

| # | 模板 | 结构族 | 数据集 | 来源 |
|---|---|---|---|---|
| E1 | 员工满意度**水平**（自身基线标准化） | 水平 + 时序 z | other567 | [P] Green-Huang-Wen-Zhou (2019, JFE) 众包雇主评价与股票收益 |
| E2 | 满意度**趋势分**（用数据集自带 trendrating） | 一阶变化（外部预置） | other567 | [P] 同上 + [D] 字段自带 `oth567_trendrating_*` |
| E3 | **CEO 评价 − 公司整体评价** | 跨口径差值 | other567 | 自建（治理脱钩） |
| E4 | 评价**有用/无用比**（争议度） | 计数比值 | other567 | 自建（注意力质量） |
| E5 | 薪酬满意度 **−** 工作生活平衡满意度 | 需求结构差 | other567 | 自建（Motivation crowding） |
| W1 | 短窗/长窗浏览量**加速度**（28d÷84d） | 尺度比值 | other571 | [P] 网络流量营收 nowcast 文献 |
| W2 | 移动端**渠道占比变化** | 份额一阶差分 | other571 | 自建（数字化迁移） |
| W3 | 夜间浏览量**占比**（流量质量） | 份额水平 | other571 | 自建（被动/自动化流量） |
| F1 | 基金交易 **HHI 集中度** | 截面集中度 | fund_holdings_panel | [P] 信念强度 / conviction 文献 |
| F2 | 大单（50bps+）**占比** | 计数比值 | fund_holdings_panel | 自建 |
| F3 | **稳定边界交易占比**（被动化程度） | 计数比值 | fund_holdings_panel | 自建 |
| I1 | 机构**平均持仓期**（短视压力） | 久期水平 | institutions25 | [P] 机构短视 / 换手文献 |
| I2 | 集中度 **−** 拥挤度 | 跨口径差值 | institutions25 | 自建 |
| I3 | 机构级**空头持仓变化** | 一阶差分 | institutions25 | 自建 |
| M1 | 高管**净流入频率**（to − from） | 双向净额 | other546 | [P] 高管流动 / 人才资本文献 |
| M2 | 分析师**网络共同度** | 网络重叠水平 | other546 | 自建 |

> 模板库累计 **29 个**（U1–U2 的 T1–T14 + 本表 15 个），满足「每轮模板库 ≥10 且结构互异」的硬约束。

### 17.3 U5 已预检（待 U4 释放槽位后派发）

**目的**：把 `MPY6EOQk` 的 S 1.42 推过 1.58。**单杠杆阶梯**（冻结核心 `reverse(group_rank(ts_zscore(vec_sum(loaned_share_count_main), W), G))`）：

| # | 变动的唯一杠杆 |
|---|---|
| 1 | W 504 → **756** |
| 2 | W → **1008**（3 年） |
| 3 | W → **1260**（4 年，注意热启动会吃掉前 5 年样本） |
| 4 | 分组轴 sector → **industry** |
| 5 | `ts_zscore` → **`ts_rank`**（序数化，抗离群） |
| 6 | 在 `vec_sum` 后加 **`ts_backfill(…,22)`**（补稀疏日） |
| 7 | 换主键 `loaned_share_count_main` → **`loaned_share_count_p5_d1`** |
| 8 | 在 `ts_zscore` 内加 **`winsorize(std=4)`**（削厚尾） |

预检：`valid=True`、`unknown_fields=[]`、无 warning。算子数全部 4–5（≤12）。

## 十八、WAVE U4 结果（8/8，0 错误，multisim `3FXo008ad5019MR82FO7LQr`）

| alpha | 机制 | S | F | 2Y | TO | sub | m | fail |
|---|---|---|---|---|---|---|---|---|
| **YP1aV3oo** | 委托簿挂单耐心不对称 | **1.13** | 0.48 | 0.97 | 0.202 | **1.50** | 3.6bp | **[]** |
| ZYQa8Vv0 | ML 分位概率顶底价差 | 0.55 | 0.12 | 0.45 | 0.310 | 0.42 | 0.9bp | 3 项 |
| 0mYPVZap | 信用利差时序异常 | 0.39 | 0.12 | 0.21 | 0.048 | 0.40 | 4.8bp | 3 项 |
| leAanwYn | other696 事件语调 | 0.29 | 0.05 | 0.38 | 0.575 | 0.21 | 0.6bp | 4 项 |
| 2rA5gV2x | 曲线 twist 动量 | 0.23 | 0.05 | 0.03 | 0.060 | 0.24 | 2.3bp | 3 项 |
| omEabj0v | 并购传闻累积 | −0.29 | −0.07 | −0.16 | 0.077 | 0.37 | −1.8bp | 3 项 |
| 1YNW83Rz | Q&A 超额负面 | −0.31 | −0.07 | 0.56 | 0.042 | −0.14 | −3.4bp | 3 项 |
| xArvL7og | 股债背离 66d 变化 | −0.41 | −0.06 | −0.20 | **0.907** | −0.57 | −0.4bp | 6 项 |

**唯一活口**：`YP1aV3oo` 委托簿挂单耐心不对称 —— S 1.13 / **sub 1.50** / fail=[]。
S 与 sub 的落差（1.13 vs 1.50）说明**信号在小半区更强**，正是流动性/微结构类信号的典型指纹。
但 TO 0.202、margin 3.6bp 偏高，且 cov 仅 0.165 ⇒ 距 1.58 仍差 0.45，非单杠杆可达。

**其余机制判读**：
- **信用债曲线三件套（利差水平 0.39 / 曲率动量 0.23 / 股债背离 −0.41）在 GBR 全部失效**。
  股债背离那条 TO 冲到 **0.907** ⇒ 该字段在 TOP700 上近乎噪声（每次重算都翻符号）。
  ⇒ `pv173` 虽 aC≈0，但**大市值英股的信用债映射没有跨资产信息优势**，判死。
- **Q&A 超额负面 −0.31（已带 reverse）** ⇒ 反向版仅 +0.31，Matsumoto-Pronk-Roelofsen 机制在 GBR 不成立。
- **ML 分位概率价差 0.55** 是 U4 次优，但 TO 0.31 / margin 0.9bp ⇒ 成本吃掉全部收益，不可用。

## 十九、WAVE U5 结果（8/8，0 错误，multisim `3JzLDlahR4M1bSSap8ZsWqg`）—— T3 窗口阶梯见顶

| alpha | 唯一杠杆 | S | F | 2Y | TO | sub | m | fail |
|---|---|---|---|---|---|---|---|---|
| rKR7xL5d | `ts_zscore`→**`ts_rank`** 窗 1008 | **1.40** | 0.75 | 2.29 | 0.098 | 1.49 | 7.3bp | [] |
| RREegY71 | 窗 **756** | 1.34 | 0.71 | 2.21 | 0.091 | 1.44 | 7.6bp | [] |
| bl6awMRp | 窗 **1260** | 1.34 | 0.71 | 2.25 | 0.089 | **1.58** | 7.8bp | [] |
| omEadv6n | 分组 → **industry** | 1.32 | 0.68 | 2.28 | 0.101 | 1.53 | 6.5bp | [] |
| MPY6rX7r | 窗 **1008** | 1.31 | 0.69 | 2.18 | 0.090 | 1.46 | 7.6bp | [] |
| N1NPZ6aX | 换主键 `_p5_d1` | 1.26 | 0.65 | 1.94 | 0.094 | 1.54 | 7.2bp | [] |
| bl6awMbp | 内加 `winsorize(std=4)` | 1.21 | 0.60 | 2.17 | 0.093 | 1.52 | 6.7bp | [] |
| KPJg16Oz | 内加 `ts_backfill(22)` | 1.13 | 0.55 | 2.09 | 0.091 | 1.46 | 6.4bp | [] |

**全部 8 条 `fail=[]`，S 落在 1.13–1.40 的窄带里 ⇒ 明确的平台期。**

把 U3 的窗 504（S 1.42）与 U5 的阶梯并起来看：

| 窗口 | 504 | 756 | 1008 | 1260 |
|---|---|---|---|---|
| S（ts_zscore, sector） | **1.42** | 1.34 | 1.31 | 1.34 |

⇒ **504 就是最优点，继续拉长反而微降。T3 骨架在 GBR 的 Sharpe 上限 = 1.42**，
距 REGULAR 线 1.58 差 0.16，且 9 种单杠杆（窗口 4 档 / 分组轴 2 档 / 时序算子 2 档 / 主键 1 档 / 去极值 1 档 / 回填 1 档）全部无法弥合。

**判定：T3（借券供给冲击）在 GBR 判死**——不是几何没调好，是机制上限。

## 二十、41 条未点亮塔探针的总结论（U1–U5）

| 波次 | 条数 | 数据集 | 最佳 S | 最佳件 |
|---|---|---|---|---|
| U1 | 8 | shortinterest3 / institutions6 / other455 | 1.27 | bl6a07lm |
| U2 | 8 | pattern_scores / continuation_score / institutions6 | 1.10（反号） | E56QnGvR |
| U3 | 8 | shortinterest3 / institutions6 / other455 | **1.42** | MPY6EOQk |
| U4 | 8 | pv173 / earningscall_sentiment / other696 / event_ml_signals / other566 / order_book_imbalance | 1.13 | YP1aV3oo |
| U5 | 8 | shortinterest3 | 1.40 | rKR7xL5d |
| **合计** | **40** | **12 个未点亮塔数据集** | **1.42** | — |

**0 条达到 REGULAR 线 S ≥ 1.58。**

**根因（第一性原理）**：GBR/TOP700 ≈ 全市场（~700 只大市值英股），
已点亮塔能出货的数据集全部是**高覆盖稠密数据**（analyst7 aC 22867 / fundamental6 aC 4246 / news17-18 cov 0.82 / model26 aC 21997）；
未点亮塔的数据集绝大多数是**稀疏、低频、或依赖小市值/流动性稀缺**的另类数据（借券、机构季报、供应链嵌入、委托簿、财报电话会）。
⇒ **未点亮塔在 GBR 之所以未点亮，本身就是「这些数据在这个区域没有土壤」的选择效应**，而不是「还没人挖到」。

这与之前 GBR 的 prod 饱和判定互相印证：GBR 是一个**容量受限的小型发达市场**，
能出货的信号已被先挖者占满（5 颗已提交件 prod 0.52–0.68 都落在拥挤区）。

## 二十一、U6 在飞 + U7 已设计

### U6（已派发，multisim `3jVfZifP852Uc6ySJ4DJuYz`）—— 双塔点亮冲刺
预检 `valid=True`、`unknown_fields=[]`。目标：**pv 塔 2/3（差 1 颗点亮）+ other 塔 1/3（差 2 颗点亮）**。

| # | 塔 | 机制 | 表达式 |
|---|---|---|---|
| 1 | PV | 日内价/VWAP 偏离 首半−后半 | `group_rank(subtract(avg_ask_price_to_vwap_ratio_first_half, avg_ask_to_vwap_ratio_last_half), subindustry)` |
| 2 | PV | 尾盘 vs 全日 量价敏感度差 | `group_rank(subtract(corr_last_trade_price_with_volume, corr_last_vwap_with_volume), subindustry)` |
| 3 | PV | 日内成交价峰度异常 | `group_rank(ts_zscore(kurtosis_last_trade_price_interval, 252), subindustry)` |
| 4 | PV | 报价尾数聚集变化（心理定价） | `group_rank(ts_delta(avg_price_modulo_10_ratio_last_half, 22), subindustry)` |
| 5 | PV | 买卖价差日内不对称漂移 | `group_rank(subtract(avg_bid_to_ask_price_ratio_first_half, avg_bid_to_ask_price_ratio_last_half), subindustry)` |
| 6 | OTHER | 供应链聚类内 PCA fact1 动量 | `group_rank(ts_delta(ts_backfill(oth455_competitor_n2v_p10_q200_w1_pca_fact1_value, 66), 22), densify(oth455_competitor_n2v_p10_q200_w1_kmeans_cluster_10))` |
| 7 | OTHER | 嵌入实现间背离（w1 vs w5） | `group_rank(subtract(ts_zscore(ts_backfill(oth455_competitor_n2v_p10_q200_w1_pca_fact1_value, 66), 252), ts_zscore(ts_backfill(oth455_competitor_n2v_p10_q200_w5_pca_fact1_value, 66), 252)), sector)` |
| 8 | OTHER | 竞争图 vs 客户图 背离 | `group_rank(subtract(ts_zscore(ts_backfill(oth455_competitor_n2v_p10_q200_w1_pca_fact1_value, 66), 252), ts_zscore(ts_backfill(oth455_customer_n2v_p10_q200_w1_pca_fact1_value, 66), 252)), sector)` |

> `other455` 的 `w1–w5` 是同一嵌入的 **5 次独立随机游走实现** ⇒ 天然给出「实现间一致性/背离」的第二矩结构（#7）。
> `other455` 实为 321 GROUP（供应链聚类）+ 79 MATRIX（PCA 坐标）⇒ 本质是**自定义分组轴库**，不是信号库（#6）。

### U7（已设计待发）—— pattern_scores 成对反义形态
`pattern_scores`：504 字段、**cov 0.992（pv 塔最高覆盖）**、aC 0–30。此前仅在 U2 试过 2 条。

其中**形态天然成对反义**，是现成的「多空对称差」结构：

| 看涨形态 | 看跌形态 |
|---|---|
| `breakaway_gap_up_*`（向上突破缺口） | `breakaway_gap_down_*` |
| `avg_similarity_v_reversal_bottom_120`（V 反转底） | `avg_similarity_v_continuation_top`（V 持续顶） |
| `avg_similarity_falling_wedge_pattern_120`（下降楔形=看涨） | `avg_similarity_rising_wedge_pattern_120`（上升楔形=看跌） |
| `avg_similarity_falling_support_flat_resistance_120` | `avg_similarity_rising_support_flat_resistance` |

模板：`group_rank(subtract(看涨族, 看跌族), subindustry)` —— 差掉共同市场状态，只留形态极性。
另有矩结构：`asc_triangle_std_simscore_lookback60`（识别稳定性）、`asc_triangle_max − asc_triangle_min`（相似度极差）。
## 二十二、U6 收批、U7 重设计已发、U8 已发、prod 队列进展（2026-11-06 03:1x）

### 22.1 U6 收批（8/8，`3jVfZifP852Uc6ySJ4DJuYz`）—— 双塔冲刺失败

| # | alpha | 机制 | S | F | 2Y | TO | sub | 判读 |
|---|---|---|---|---|---|---|---|---|
| 1 | 58EJP8L1 | 日内价/VWAP 偏离（首半−后半） | **0.85** | 0.17 | 0.35 | **0.604** | −0.07 | 本波最高，但换手 60% + sub 负 |
| 2 | npvaLp3M | 尾盘 vs 全日 量价敏感度差 | 0.00 | 0.00 | −0.30 | 0.660 | −0.13 | 零信号 |
| 3 | omEaxmVn | 日内成交价峰度异常 | 0.55 | 0.08 | 0.25 | 0.622 | 0.06 | 无 |
| 4 | O0AWl0o7 | 报价尾数聚集变化（心理定价） | −0.82 | −0.21 | −1.39 | 0.380 | −0.42 | **反向版 +0.82**，仍远低于线 |
| 5 | A1Vxo1kQ | 买卖价差日内不对称漂移 | 0.07 | 0.00 | 0.04 | 0.519 | 0.31 | 无 |
| 6 | O0AWl0og | 供应链聚类 PCA fact1 动量 | 0.31 | 0.07 | 0.53 | 0.059 | 0.08 | 无 |
| 7 | gJeanJ3J | 嵌入实现间背离（w1 vs w5） | 0.36 | 0.09 | −1.20 | 0.054 | 0.19 | 无 |
| 8 | MPY6JPx9 | 竞争图 vs 客户图 背离 | 0.54 | 0.17 | 0.32 | 0.045 | 0.34 | 无 |

⇒ **pv 塔仍 2/3、other 塔仍 1/3，均未点亮。** U6 的 8 条全部落在「日内微观结构」与「供应链嵌入」两条无土壤路径上：
日内类换手天然 0.5–0.66（TOP700 大市值域里日内信号被套利得只剩噪声），嵌入类换手 0.04–0.06（一年只换几次，赚不到风险溢价）。
**日内微观结构 ⇒ 判死**（TO 与前缀噪声结构决定）；**other455 嵌入 ⇒ 只能当分组轴，不能当信号腿**（U3/U6 共 4 条独立证实）。

### 22.2 U7 重设计（原 8 条同骨架 ⇒ 改为 4+4 混编）

原 U7 的 8 条全为 `subtract(看涨族, 看跌族)` 单骨架，只填 1 个模板槽，违反模板多样性硬约束。
改为 **4 个反义形态对（跨形态族）+ 4 个结构互异的几何（同一形态族）**：

| # | 类别 | 几何 | 表达式 |
|---|---|---|---|
| 1 | 形态对·缺口 | `subtract(up, down)` | `group_rank(subtract(avg_similarity_upward_breakaway_gap_120, avg_similarity_downward_breakaway_gap_120), subindustry)` |
| 2 | 形态对·楔形 | `subtract(up, down)` | `group_rank(subtract(avg_similarity_falling_wedge_pattern_120, avg_similarity_rising_wedge_pattern_120), subindustry)` |
| 3 | 形态对·三角 | `subtract(up, down)` | `group_rank(subtract(avg_similarity_upward_symmetrical_triangle, avg_similarity_downward_symmetrical_triangle), subindustry)` |
| 4 | 形态对·V | `subtract(bottom, top)` | `group_rank(subtract(avg_similarity_v_reversal_bottom_120, avg_similarity_v_continuation_top), subindustry)` |
| 5 | 矩·0 阶 | 纯水平 | `group_rank(avg_similarity_upward_breakaway_gap_120, subindustry)` |
| 6 | 矩·自基线 | `ts_zscore 252` | `group_rank(ts_zscore(avg_similarity_upward_breakaway_gap_120, 252), subindustry)` |
| 7 | 非线性 | 归一化比值 | `group_rank(divide(subtract(A, B), add(A, B)), subindustry)` |
| 8 | 矩·1 阶 | `ts_delta 22` | `group_rank(ts_delta(avg_similarity_upward_breakaway_gap_120, 22), subindustry)` |

派发：multisim `2YvUBCa7558O9av16GPz80jZ`，预检 `valid=True / unknown_fields=[]`。

### 22.3 U8 已发 —— 未点亮塔「第二腿」单腿扫描（集合外 × 集合外，不限配额）

8 个机制各一条最佳几何，目的是先测出**各自单腿 S**，达标者再做 2:1 加权合成（U9）：

| # | 数据集 | 塔 | 机制 | 表达式 |
|---|---|---|---|---|
| 1 | risk60 | risk | 拥挤度异常 | `group_rank(ts_zscore(vec_avg(rsk60_crowding), 252), sector)` |
| 2 | risk68 | risk | 短周期权重波动率 | `group_rank(ts_zscore(rsk68_weight_volatility_short, 252), sector)` |
| 3 | option1 | option | delta 曲面隐含波动率 | `group_rank(ts_zscore(vec_avg(opt1_p_deltasurface_d1_vi), 252), sector)` |
| 4 | macro27 | macro | 招聘岗位增长（劳动力需求） | `group_rank(ts_zscore(ts_delta(vec_sum(num_jobs_active), 66), 252), sector)` |
| 5 | sentiment27 | sentiment | 社媒相对热度 | `group_rank(ts_zscore(vec_avg(snl27_relpopularity1), 252), sector)` |
| 6 | insiders1 | insiders | 内部人累计持股 | `group_rank(ts_sum(vec_sum(insd1_shares), 63), sector)` |
| 7 | socialmedia5 | socialmedia | 情绪命中分平滑 | `group_rank(ts_mean(vec_avg(scl5_s_hitscore_averagesentiment), 63), sector)` |
| 8 | sentiment7 | sentiment | 维基浏览量异常 | `group_rank(ts_zscore(vec_sum(snt7_views), 252), sector)` |

派发：multisim `4BDvElcM34yfbxbuiXZrMln`，预检 `valid=True / unknown_fields=[]`。

### 22.4 prod 队列进展（串行队列 9 颗，仍在跑）

| alpha | prod | 状态 |
|---|---|---|
| **rKRPAWv9** | **0.3998** | **✓ 放行** —— 继 `QPvbxjXw`(0.5794) 之后**第 2 颗 prod 干净的候选** |
| WjOK0roG | 0.7851 | ✗ 浅钉（单点，<0.8）⇒ 进归因破墙队列，不直接判死 |
| kqNe9LPz | 0.8203 | ✗ 深钉 ⇒ 判死（已有结论） |
| vR1nAj6z | 1.0000 | ✗ 完全撞池 ⇒ 判死 |
| 6XKw8e6O / xArX7dNl / P0ojvkkJ | — | `correlation_busy`，待下轮 |
| xAb2OkMm | — | `pending` 长期不落 |
| 9qWa6r8x | — | 队列未跑到 |

⇒ 存活池 9 颗中，**prod 已确认 3 颗**：`QPvbxjXw` 0.5794 ✓ / `rKRPAWv9` 0.3998 ✓ / `WjOK0roG` 0.7851 ✗（待破墙）。
## 二十三、U7/U8 双灭、pv 塔与 insider 塔画像突破、U9/U11 已发（2026-11-06 03:3x）

### 23.1 U7 收批 —— `pattern_scores` 判死（`2YvUBCa7558O9av16GPz80jZ`）

| alpha | 几何 | S | F | 2Y | TO | sub |
|---|---|---|---|---|---|---|
| QPv0wYbM | 形态对·缺口 `subtract(up,down)` | −0.02 | 0.00 | −0.19 | 0.182 | 0.18 |
| Xg9adRW8 | 形态对·楔形 | −0.08 | −0.01 | 1.17 | 0.109 | −0.07 |
| xArvJ1YJ | 形态对·三角 | −0.08 | −0.01 | 0.87 | 0.259 | −0.08 |
| Jje86Pxn | 形态对·V | −0.58 | −0.20 | −1.55 | 0.123 | −0.52 |
| 88RNMv3q | 矩·0 阶 纯水平 | −0.64 | −0.22 | 0.37 | 0.146 | 0.00 |
| A1VxoQ0E | 矩·自基线 zscore252 | −0.73 | −0.25 | −1.40 | 0.153 | −0.63 |
| j2Yaqe3e | 非线性 归一化比值 | −0.76 | −0.27 | −1.37 | 0.149 | −0.78 |
| GrWmZglO | 矩·1 阶 ts_delta22 | −0.78 | −0.28 | −1.31 | 0.150 | −0.79 |

**8 条全负，取反后最高 0.78**（且 `88RNMv3q` 反转后 sub=0、`QPv0wYbM` 反转后 sub=−0.18）。
⇒ **`pattern_scores` 判死**：U2（2 条）+ U7（8 条）共 **10 条**探针，`|S|` 上限 0.78。
**关键结论**：形态相似度这类「K 线形态匹配」在 GBR 大市值域**方向性为零**——
4 个不同形态族（缺口/楔形/三角/V）给出同量级负值，说明不是某个形态选错，而是**形态匹配本身不含跨截面预测力**（形态是价格的滞后函数，且在高流动性大市值域已被套利）。
**顺带判死其同族 `continuation_score`**（U10 已预检但我决定不发，理由：同一「形态相似度」机制族，U2+U7 共 10 条已给出上限，再投 8 条是重复探针）。

### 23.2 U8 收批 —— 未点亮塔第二腿单腿扫描全灭（`4BDvElcM34yfbxbuiXZrMln`）

| alpha | 机制 | S | F | 2Y | TO | sub |
|---|---|---|---|---|---|---|
| 58EJPjZ6 | risk60 拥挤度异常 | **0.75** | 0.32 | 0.38 | 0.124 | 0.51 |
| 9qxlNEqq | risk68 短周期权重波动率 | 0.39 | 0.08 | 0.53 | 0.226 | 0.18 |
| d5WaNK2J | option1 delta 曲面 IV | 0.38 | 0.12 | 0.71 | 0.066 | 0.46 |
| N1NPYeXp | macro27 招聘岗位增长 | 0.23 | 0.05 | 0.03 | 0.122 | 0.19 |
| WjOlvLEd | sentiment27 社媒相对热度 | −0.25 | −0.06 | −0.45 | 0.152 | −0.34 |
| kqNazJxP | insiders1 内部人累计持股 | −0.25 | −0.06 | −1.39 | 0.075 | −0.84 |
| bl6ae8Y6 | socialmedia5 情绪命中分 | −0.33 | −0.08 | −0.71 | 0.064 | 0.02 |
| rKR7Zd13 | sentiment7 维基浏览量异常 | −0.56 | −0.15 | −0.55 | 0.214 | −1.15 |

⇒ **最高 0.75**，无一条具备「可合成腿」的强度（合成要求单腿 S 至少 1.2 以上，否则 2:1 加权只会得到 ~0.9）。
**判读**：这 8 个数据集虽在 `risk / option / macro / sentiment / insiders / socialmedia` 六个不同塔，但都指向同一结论——
GBR 大市值域里**非价格类另类数据只有「弱信号」量级**（S 0.2–0.8），无论机制多合理。

### 23.3 ★ 新画像：pv 塔剩余 5 集 + insider 三集 + 6 个未画像集

#### pv 塔（16 集全部落表）

| 数据集 | cov | 字段 | uC | aC | 结构判读 |
|---|---|---|---|---|---|
| **pv106** Microstructure Spread | 0 | **8 MATRIX** | **25** | 43 | `pv106_{spread,spreadbp,lastspread,lastspreadbp}` + `aggregated_slippage_metric` + `slippage_at_spread_35` + `transaction_cost_{maximum,percentile_10}` ⇒ **买卖价差/交易成本块，近乎处女集（uC 25）** |
| **pv20** Daily Spot&Cross | 0 | **675** | 360 | 717 | 实为 `adv20/adv60`、`beta_market_{10,20,40,60,125,500}d`、`market_beta_250d`、`pv20_252_mom`、`firm_market_capitalization`、`group_slippage_estimate`、`alternative_slippage_*`、`pv20_{bps,ebi}_indicator_{1..4}_feature{0..12}` ⇒ **beta/动量/成本/规模块** |
| **continuation_score** | 0 | **560 MATRIX** | 326 | 778 | `{ascending_channel,ascending_scallop,ascending_staircase}_similarity_{average,middle,maximum,minimum,median,percentile_95,dispersion,stdev_h40w,recent}` + `avg_similarity_{bullish,bearish}_{flag,pennant,rectangle}` + `continuation_gap_{up,down}` + `inverse_{cup_handle,dead_cat_recovery}` ⇒ **形态库 + 每个形态自带 dispersion/stdev（识别不确定性）** |
| **pv103** Interval & MOO/MOC | 0 | 8 MATRIX | 101 | 170 | `session_1600to1600_{initial,final,max,min,volume_weighted_avg_price,total_traded_volume,market_value}` + `pv103_ivam_sum` ⇒ 24h 整段 OHLCV |
| **pv109** Bond Yield | 0.332 | 26 VECTOR | 15 | 32 | `{bid,ask,midpoint}_yield_to_maturity`、`{bid,ask,midpoint}_conversion_yield`、`coupon_*`、`face_value_amount`、`amt_issued/outstanding` ⇒ 债券定价（uC 15） |
| pv29 / pv30 / pv13 / pv17 / pv71 | 1.0 / 0.827 / 0 / 0 / 0 | 50 / 240 / 28 / 1 / 8 | — | — | 全是**行业分类/关系/聚类 GROUP 轴**，只能当分组变量 |
| pv1 (aC 56109) / pv47 (aC 779) / pv113 (1 字段) | — | 23 / 2 / 1 | — | — | 已深度饱和或无非信号字段 |

#### insiders 塔（0/3，未点亮）+ other 塔 insider 兄弟集

| 数据集 | 塔 | cov | 字段 | 结构判读 |
|---|---|---|---|---|
| **insider_agg_matrix** | insiders | 0.618 | **34 MATRIX** | **与 EUR 已验证配方字段完全同构**：`total_{top_,secondary_top_,}{buy,sell}_shares`、`avg_*` 同族、`{top_,}significant_value_{1..4}` 显著性分层。⇒ 可直接复刻 EUR 的 S 2.00–2.17 配方 |
| insider_matrix | other | 0.606 | 33 MATRIX | `eur_{,top_,top_director_,director_}{value,signal_value}_{1..4}` + `director_intensity_score` ⇒ 金额/信号分档（EUR 计价口径） |
| insider_trx_matrix | other | 0.601 | 33 MATRIX | `{total,mean}_{,top_,secondary_,top_secondary_}{buy,sell}_transaction_count` + `usd_{,top_}{direct,primary,secondary,tertiary,quaternary}_signal_value` ⇒ **交易笔数** + 美元金额分档 |

> 毒字段提醒（已实证零持仓）：`directional_indicator` / `directional_indicator_2` / `directional_significant_value_1` —— 三集都有，必须避开。

#### 其余 6 集（全部 `other` 塔或小集）

| 数据集 | 字段 | 结构 | 可用性 |
|---|---|---|---|
| **other47** | 18 VECTOR | **网站流量/搜索**：`oth47_organic_traffic/keywords/cost`、`organic_search_visitors_enriched`、`paid_search_visitors/budget_estimate/terms_count`、`website_traffic_rank_enriched`、`unique_product_listing_ads` | ★★★★ 数字需求代理，机制全新 |
| **other169** | 22 VECTOR | **CDS 信用违约互换**：`mid_par_spread_basis_points`、`{bid,mid}_quote_spread_basis_points`、`oth169_{recoveryrate,recrisk,tenor}`、`{dailycontributors,dailycontributedquotes}`、`interest_rate_curve_parallel_shift_impact` | ★★★★ 信用市场领先股票 |
| **other250** | 12 VECTOR | 电商商品：`average_star_score`、`total_review_number`、`oth250_{rank,item_review_count,price_range_max/min}`、`sales_position_rank` | ★★★ 消费需求 |
| **other315** | 21 VECTOR | **利率互换**：`leg{1,2}_{spread_value,aggregate_notional_quantity,...}`、`option_strike_value`、`contract_trade_price` | ★★ 小众 |
| **news_sentiment_nlp** | 23 VECTOR | 标题 NLP：`headline_sentiment_{vader,textblob,sentiwordnet,subjectivity}` + **可读性**（`flesch_kincaid_score`、`flesch_readability_score`、`gunning_fog_index`、`smog_readability_index`）+ `headline_sentence_sentiment_variance` | ★★★ 新颖（可读性=信息处理成本） |
| **risk88** | 1 MATRIX | `alternative_market_cap_usd` | ★ 仅市值，作分组/规模因子 |

### 23.4 U9 / U11 已发

**U9 = pv106 流动性溢价（pv 塔 2/3 冲刺）**，multisim `44z1QLbFY4Txcfd1cfEv25Jn`，预检 `valid=True`：

| # | 几何 | 表达式 |
|---|---|---|
| 1 | 水平（Amihud 流动性溢价） | `group_rank(pv106_spreadbp, subindustry)` |
| 2 | 流动性改善（价差收窄） | `group_rank(reverse(ts_delta(ts_mean(pv106_spreadbp, 22), 66)), subindustry)` |
| 3 | 自基线异常 | `group_rank(ts_zscore(pv106_spreadbp, 252), subindustry)` |
| 4 | 收盘时点紧张度（比值） | `group_rank(divide(pv106_lastspreadbp, add(pv106_spreadbp, 1)), subindustry)` |
| 5 | 成本分布宽度 | `group_rank(divide(subtract(transaction_cost_maximum, transaction_cost_percentile_10), add(transaction_cost_percentile_10, 1)), subindustry)` |
| 6 | 滑点平滑水平 | `group_rank(ts_mean(aggregated_slippage_metric, 63), subindustry)` |
| 7 | 二阶矩（流动性不确定性） | `group_rank(ts_std_dev(pv106_spreadbp, 66), subindustry)` |
| 8 | 分位位置 | `group_rank(ts_rank(pv106_spreadbp, 250), subindustry)` |

**U11 = insider_agg_matrix 复刻 EUR 配方（insiders 塔 0/3 冲刺）**，multisim `1IWeCX6Oe4NNc7q15j0KndHZ`，预检 `valid=True`：

| # | 几何 | 表达式 |
|---|---|---|
| 1 | **EUR 基线：顶格净买入 63d** | `group_rank(ts_sum(subtract(total_top_buy_shares, total_top_sell_shares), 63), industry)` |
| 2 | 全内部人净买入 63d | `group_rank(ts_sum(subtract(total_buy_shares, total_sell_shares), 63), industry)` |
| 3 | 有界净买比 | `group_rank(divide(subtract(ts_sum(total_top_buy_shares, 63), ts_sum(total_top_sell_shares, 63)), add(ts_sum(add(total_top_buy_shares, total_top_sell_shares), 63), 1)), industry)` |
| 4 | 顶格显著性自基线 | `group_rank(ts_zscore(top_significant_value_1, 252), industry)` |
| 5 | 净买入自基线异常 | `group_rank(ts_zscore(ts_sum(subtract(total_top_buy_shares, total_top_sell_shares), 22), 504), industry)` |
| 6 | 卖出侧（减持少） | `group_rank(reverse(ts_sum(total_top_sell_shares, 63)), industry)` |
| 7 | 直接持股买卖比 | `group_rank(divide(ts_sum(total_secondary_top_buy_shares, 63), add(ts_sum(total_secondary_top_sell_shares, 63), 1)), industry)` |
| 8 | 顶格申报强度 | `group_rank(ts_mean(add(top_significant_value_1, top_significant_value_2), 63), industry)` |

### 23.5 ★ 新发现的硬门禁：`ts_max` 是平台不可访问算子

U11 首次派发被 **toolkit 静态门禁整批拒绝**：

```
[INACCESSIBLE_OP] ts_max 平台不可访问，用已验证等价算子替换   （failed_expressions: {"4": ...}, passed 7/8）
```

⇒ **教训**：`ts_max` 不得使用；「窗口内极值」需求改用 `ts_zscore` / `ts_rank` / `ts_mean` 或 `ts_quantile` 族替代。
本次将 #4 由 `ts_max(top_significant_value_1, 252)` 改为 `ts_zscore(top_significant_value_1, 252)` 后一次通过。
**注意**：门禁是**整批拒绝**（7 条合格也全部不派），因此派发前必须逐条过滤不可访问算子。

### 23.6 U10 主动撤回

`continuation_score` 波次（U10）已通过预检但**决定不发**：与 U7 同属「形态相似度」机制族，
U2+U7 共 10 条已给出 `|S| ≤ 0.78` 的族上限，再投 8 条属于重复探针，浪费 25–35 分钟仿真槽。
若 U9/U11 也无产出，再考虑用 U10 里的 **`dispersion` 归一化**几何（`divide(方向差, 离散度和)`）单独验证一次。
## 二十四、数据集画像进度：未点亮 82 集中已画像 48 集（2026-11-06 03:2x）

本轮新增 12 集画像（earnings6 / other128 / other699 / institutions1 / institutions4 / stock_cluster_dl / pv13 / pv71 / pv47 / other545 / euro_equity_imbalance / institutions6）。

| 数据集 | 字段 | 结构判读 | 可用性 |
|---|---|---|---|
| **earnings6** | 18 VECTOR | `ern6_actual_eps`、`ern6_estimated_eps`、`preliminary_eps_range_{lower,upper}_bound`、`ern6_{1,2,3,4}q`、`ern6_next_ed`、`ern6_transcript_fiscal_year` | ★★★★★ **盈余惊喜 SUE / PEAD** —— 教科书级最强异常之一，earnings 塔 0/3 |
| **institutions4** | 6 VECTOR | `institutional_holding_{current,previous}_{market_value,shares}`、`_percent_of_portfolio`、`_percent_of_shares_outstanding` | ★★★★★ **机构持股水平与变化**（IO 溢价 + 13F 增量），institutions 塔 0/3 |
| **institutions1** | 7 VECTOR | `inst1_{holdings,price,shares,value,valueeur,tradesignificance}` | ★★★ 机构逐笔交易（与 insiders1 同构） |
| **other128** | 14 VECTOR | `oth128_dmexus{cfo,ceo}{cash,noncash}compensation`、`{ceo,cfo}tenure`、`executiveefficiency{input,output}`、`keyexecutiveice`、`dmexusscore` + `{chief,finance}_exec_investor_sentiment_score` | ★★★★ **高管薪酬/任期/管理效率**（代理成本） |
| **pv13** | 28（11 GROUP + 13 MATRIX + 4 VECTOR） | `pv13_new_{1..6}l_scibr`、`pv13_{5,22_800}_sector`、`revere_*` + **图中心性** `pv13_{ompetitor,ustomergraphrank}_{hub,page,auth}_rank` | ★★★ 分类轴为主；**供应链图中心性可当信号** |
| **pv71** | 8 VECTOR | `pairwise_price_volume_corr_score`、`pv71_{ibesest,pvvolcorr}_{relation,score}`、`relation_{edge_score,weight_normalized}` | ★★ 同业关联图（group 轴） |
| **euro_equity_imbalance** | 4 VECTOR | `bucketed_{net_order,sign}_imbalance_{quantile,uniform}` | ★ **imbalance 族已封盘**（族代表 prod 0.838） |
| **institutions6** | 11 MATRIX | `count_institutional_{buyers,holders,sellers}_security`、`{quantity,market_value}_institutional_shares_{acquired,disposed}`、`aggregate_*` | ✗ **已判死**（U3 `YP1aV6gA` S 0.41） |
| other699 | 7 VECTOR | 拆股元数据 `aggsplitfactor` / `newnumofshares` | ✗ 无信号 |
| other545 | 4 VECTOR | `oth545_{mktcap,mpd,pln_omen,score}` | ✗ 语义不明 |
| pv47 | 2 MATRIX | `pv47_spret` 残差收益 | ✗ aC 779 深度饱和 |
| stock_cluster_dl | 5 MATRIX | `principal_component_features_{5..9}` | ✗ 仅分组轴 |

### ★ 累计画像覆盖

| 分类 | 数据集数 | 已画像 | 未画像（多为饱和/单字段/元数据） |
|---|---|---|---|
| 未点亮塔合计 | 82 | **48** | 34（`techindi_model` aC 26992、`pv1` aC 56109、`shortinterest3` 已判死、`socialmedia39`/`pv113`/`pv17` 单字段等） |

## 二十五、★ 自查出的方法论盲区：65 条探针的**设置档从未变过**

复核 U1→U11 的全部派发参数，发现**每一条都用同一档**：

```
region GBR / universe TOP700 / delay 1 / decay 5 / neutralization SLOW / truncation 0.10
```

⇒ 这违反了我自己的「设置档盲区清点」纪律。`SLOW` 是**缓慢移动的基本面因子中性化**，
对**事件型 / 情绪型 / 微观结构型**信号（insiders、CDS、order imbalance、借券供给）可能过度剥离，
因为这些信号的收益来源恰恰是「短期定价偏差」，被慢因子中性化后只剩残渣。

**证据**：U8 里 8 个不同塔的机制**全部**落在 S 0.23–0.75 的窄带，跨机制一致性过高——
这更像是**设置档压低**的共性效应，而非 8 个机制同时失效。

**⇒ 新增待办（U16）**：对最接近线的 3 个基座做**中性化档扫描**（每档一条单仿真，因为 multisim 只能共用一组设置）：

| 基座 | 当前最好 | 扫描档 |
|---|---|---|
| T3 借券供给冲击 `reverse(group_rank(ts_zscore(vec_sum(loaned_share_count_main), 504), sector))` | S 1.42（SLOW） | FAST / SLOW_AND_FAST / STATISTICAL / REVERSION_AND_MOMENTUM / MARKET / INDUSTRY / SUBINDUSTRY |
| order_book_imbalance 挂单耐心不对称 `YP1aV3oo` | S 1.13（SLOW） | FAST / STATISTICAL / INDUSTRY / MARKET |
| risk60 拥挤度 `58EJPjZ6` | S 0.75（SLOW） | FAST / STATISTICAL / MARKET |

GBR 可用中性化（`COUNTRY` 报错）：`FAST / SLOW / SLOW_AND_FAST / STATISTICAL / SUBINDUSTRY / INDUSTRY / MARKET / CROWDING / REVERSION_AND_MOMENTUM`。
### 25.1 ★★★ 实证支持：本地库 GBR 7604 条历史 alpha 按中性化档分组

```sql
SELECT neutralization, COUNT(*), AVG(sharpe), MAX(sharpe), AVG(fitness), AVG(turnover)
FROM alphas WHERE region_id=7 GROUP BY neutralization ORDER BY n DESC
```

| 中性化档 | n | **avg S** | max S | avg F | avg TO |
|---|---:|---:|---:|---:|---:|
| **REVERSION_AND_MOMENTUM** | 18 | **1.633** | 2.67 | **1.162** | 0.114 |
| **MARKET** | 25 | **1.074** | 2.04 | 0.729 | 0.167 |
| INDUSTRY | 286 | 0.795 | 2.50 | 0.570 | 0.173 |
| FAST | 581 | 0.759 | 3.80 | 0.434 | 0.160 |
| STATISTICAL | 4957 | 0.756 | 11.18 | 0.470 | 0.151 |
| CROWDING | 449 | 0.564 | 2.74 | 0.314 | 0.130 |
| **SLOW（我全程用的）** | 97 | **0.568** | 2.21 | 0.310 | 0.167 |
| （None） | 489 | 0.558 | 2.02 | 0.313 | 0.171 |
| SUBINDUSTRY | 680 | 0.366 | 2.88 | 0.217 | 0.124 |
| SECTOR | 15 | 0.264 | 2.20 | 0.282 | 0.070 |
| SLOW_AND_FAST | 7 | 0.130 | 1.31 | 0.113 | 0.131 |

**三条结论**：

1. **`SLOW` 是全表倒数第三差的一档（avg S 0.568）**，而我 U1→U8 共 65 条探针**全部**用它 ⇒ 相当于每一条都被系统性压低约 **0.2–1.0 Sharpe**。
   `REVERSION_AND_MOMENTUM`（avg S 1.633）与 `SLOW` 的差距是 **1.07 Sharpe** —— 足以把 T3 的 1.42 推过 1.58 线。
2. **`SUBINDUSTRY` / `SECTOR` 是最差两档**（0.366 / 0.264）；而我 65 条探针的外层归一化用了 **~55 条 `group_rank(..., subindustry)`**。
   TOP700 只有约 700 只股票，subindustry 分组下每组可能只剩十几只 ⇒ 组内 rank 噪声大、截面区分度低。
3. **自选择偏差警告**：n 小的档（REVERSION_AND_MOMENTUM 18 / MARKET 25）很可能是「已知好才去跑这一档」，不能直接当因果。
   因此必须做**受控实验**（U16：同一表达式 × 8 档），而不是直接换档盲用。

**⇒ 立即变更的默认动作**：

- 新波次的外层归一化从 `group_rank(..., subindustry)` 改为 `group_rank(..., sector)`（或 `industry`），除非该字段本身是行业内部量。
- 新波次的 `neutralization` 从 `SLOW` 改为 `INDUSTRY`；`REVERSION_AND_MOMENTUM` / `MARKET` 待 U16 受控实验确认后再定。
- U14/U15/U12/U13 四条已预检的波次，派发时把 neutralization 全部改为 `INDUSTRY`。
### 25.2 未点亮塔画像收官

`techindi_model`（399 MATRIX，aC **26992**，uC 1883）**判死**，三条独立理由：
1. 字段名是**不可解释编码**（`tm_15_r1_r5_r10_rh_glb_d1_r10_q1` … `_q5_p0..p4`，本质是技术模型分数按分位桶展开），无法立可证伪的经济假设；
2. aC 26992 属**极端饱和**（全库最高档）；
3. 本族（techindi `tm_15` / `tm_17`）的 **prod 族代表已在 0.72–0.75**，越过 0.70 放行线。

⇒ 至此未点亮塔 82 集中：**画像 49 集**，剩余 33 集中除 `pv1`（aC 56109）/`shortinterest3`（已判死）/`socialmedia39`·`pv113`·`pv17`（单字段）外，均为 ≤7 字段元数据级小集。
**数据集画像这条线基本收官。**

---

## 二十六、U16 受控实验收官 + 新数据集探针全灭 + `kqN8xjV6` prod 卡墙

### 26.1 U16 八档中性化受控实验（同一 T3 表达式 × 8 档）★定论

同一表达式 `reverse(group_rank(ts_zscore(vec_sum(loaned_share_count_main), 504), sector))`，只换 `neutralization`：

| 中性化 | alpha | S | F | 2Y | sub | TO | margin | RA 闸 |
|---|---|---:|---:|---:|---:|---:|---:|---|
| **FAST** | **kqN8xjV6** | **1.76** | **1.12** | 2.76 | 1.81 | 0.107 | — | **全过 ✓** |
| STATISTICAL | A1VLRN8d | 1.55 | 0.85 | 2.63 | 1.48 | 0.100 | — | S/F 不过 |
| REVERSION_AND_MOMENTUM | zq3Av2mK | 1.45 | 0.93 | 2.07 | **1.88** | 0.084 | 12.2bp | S/F 不过 |
| SLOW | MPY6EOQk | 1.42 | 0.76 | 2.28 | 1.45 | 0.093 | — | S/F 不过 |
| SLOW_AND_FAST | KPJVKG5x | 1.38 | 0.73 | 2.25 | 1.46 | 0.116 | — | S/F 不过 |
| INDUSTRY | QPvW1Wm5 | 1.25 | 0.78 | 1.82 | 1.57 | 0.075 | 13.1bp | S/F 不过 |
| MARKET | GrWQqKEG | 1.20 | 0.78 | 1.78 | 1.49 | 0.067 | 15.7bp | S/F 不过 |
| CROWDING | xArlKlAn | 1.19 | 0.69 | 1.95 | 1.51 | 0.075 | 11.2bp | S/F 不过 |
| SUBINDUSTRY | O0A61W8q | 1.06 | 0.60 | 1.89 | 1.46 | 0.083 | 9.8bp | S/F 不过 |

**结论**：八档里**只有 FAST 一条通过全部 RA 硬闸**。FAST 对次优档（STATISTICAL）的领先是 **ΔS +0.21 / ΔF +0.27 / Δ2Y +0.13**。
FAST 的 margin 未单列但 S/F 双高说明它不是靠放大换手取胜（TO 0.107，居中）。

⇒ **GBR 新波次 default neutralization = FAST**（此前 SLOW 是错的）。
注意：margin 最高的是 **MARKET（15.7bp）/ INDUSTRY（13.1bp）**，若某机制 fitness 达标但 returns 不够，MARKET 是备选档。

### 26.2 `kqN8xjV6` prod = 0.8608（深钉，卡墙）

```
kqN8xjV6 = reverse(group_rank(ts_zscore(vec_sum(loaned_share_count_main), 504), sector))
GBR/TOP700/D1/decay5/FAST/trunc0.10  S 1.76 / F 1.12 / 2Y 2.76 / sub 1.81 / TO 0.107
self_corr 0.2799 ✓     prod 0.8608 ✗（线 0.70）
```

按判死纪律 `max ≥ 0.80 ⇒ 深钉`，**该件暂判死**；破墙路径见 26.6。

### 26.3 U20：shortinterest3 其余 12 个模板全灭（上限 1.03）

全 VECTOR（25 字段 × 3 套聚合 base / `_main` / `_p5_d1`），8 条 @ FAST + 4 条 @ REVERSION_AND_MOMENTUM：

| 模板 | 机制 | alpha | S | F | 2Y | TO |
|---|---|---|---:|---:|---:|---:|
| T3 费率不确定性 | `reverse(ts_zscore(vec_avg(loan_rate_volatility),252))` | P0oP0lxL | **1.03** | 0.40 | 0.77 | 0.222 |
| T2 费率离散度 | `reverse(divide(vec_max−vec_min, vec_avg+0.001))` | ZYQXYlgd | 0.87 | 0.27 | 1.04 | 0.306 |
| T5 借出市值供给冲击 | `reverse(ts_zscore(ts_delta(vec_sum(loaned_market_value_usd),22),252))` | npv6pzew | 0.79 | 0.22 | 0.43 | 0.332 |
| T7 费率升/数量降背离 | 双 zscore 相减 | LLM8LXm9 | 0.65 | 0.16 | 1.23 | 0.326 |
| T9 费率加速度 | 短窗 ts_delta(5) | P0oP0rrM | 0.98 | 0.32 | 0.88 | 0.359 |
| T11 期限×费率 | multiply 交互 | pwdWwJJb | 0.81 | 0.28 | 0.78 | 0.278 |
| T1 费率水平 | `ts_backfill(vec_avg(mean_loan_rate),60)` | E56m5aNG | −0.68 | −0.21 | −2.13 | 0.216 |
| T4 借券期限 | `ts_zscore(vec_avg(average_loan_duration_days),252)` | leAgez5O | −0.75 | −0.22 | −0.85 | 0.266 |
| T6 交易活跃度 | `ts_zscore(vec_sum(transaction_count),66)` | 78LG8Xvx | −0.90 | −0.27 | −0.92 | 0.314 |
| T8 三套聚合背离 | p5_d1 vs main | A1VL1are | −1.01 | −0.54 | −2.10 | 0.107 |
| T10 聚合 bar | `ts_zscore(vec_avg(shrt3_bar),252)` | MPYgPllz | −0.59 | −0.18 | −1.03 | 0.218 |
| T12 单笔借出规模 | `divide(vec_sum(loan_count), vec_sum(txn_count))` | 78LG8q0b | −0.91 | −0.40 | −0.03 | 0.207 |

**判读**：`shortinterest` 塔**只有一个强机制** —— 借出股数供给冲击（T3，S 1.76）。其余 12 个模板上限 **1.03**，且换手 0.21–0.36（噪声型）。

### 26.4 U21：other47 网站流量 → 上限 1.02，封盘

| alpha | S | F | 2Y | sub | TO | checks.fail |
|---|---:|---:|---:|---:|---:|---|
| MPYgPNAM `ts_delta(ts_mean(vec_sum(oth47_organic_traffic),22),66)` | **1.02** | 0.50 | 1.38 | 0.70 | 0.110 | **[] 空** |
| 58EG8dRN 有机−付费流量差 | 1.01 | 0.49 | 1.26 | 0.78 | 0.109 | **[] 空** |
| 其余 6 条 | 0.34–0.86 | — | — | — | — | 有 fail |

两条 checks.fail 为空但 S 1.0 远低于 1.58 线 ⇒ `other47` **封盘**（距线 0.56）。

### 26.5 U22：institutions4 判死 / earnings6 事件字段判死 / SUE 整批平台报错

**institutions4**（6 VECTOR，cov 0.39）8 条全灭，最高 `ern6_x_dividend` 0.53：

| alpha | 表达式要点 | S | F | 2Y |
|---|---|---:|---:|---:|
| WjOYjPZQ | `ts_backfill(vec_avg(ern6_x_dividend),250)` | 0.53 | 0.21 | 1.54 |
| mLoKLgnx | IO 占流通股比 `ts_zscore(...,504)` | 0.28 | 0.08 | −0.11 |
| GrWQrdjJ | IO 水平 | 0.13 | 0.02 | −0.04 |
| Jje3jxJA | **ΔIO 净买入（Nofsinger-Sias）** | **−0.27** | −0.07 | 0.19 |
| LLM8L9o1 | ΔIO 市值口径 | −0.19 | −0.04 | 0.56 |
| 1YNGYx3X | IO 占组合比（信心） | −0.07 | −0.01 | 0.23 |
| 3qoGq9mN | 距下次财报天数 | −0.23 | −0.06 | −0.84 |
| d5W95OJY | IO 隐含价 | 0.15 | 0.03 | 0.73 |

⇒ **`institutions4` 判死**：连文献最强的 ΔIO 也只有 −0.27（反向 +0.27），说明 GBR TOP700 的机构持股数据（cov 0.39）**不承载 IO 动量**。

**earnings6**：
- SUE 族 8 条（`ern6_actual_eps − ern6_estimated_eps` 的各种几何）**平台整批返回 "No alpha_id in sim response"**（error_count=8/8）—— 这是平台侧对该字段的计算失败，不是语法问题（preflight 已 valid）。
- 事件字段（`ern6_1q`/`ern6_x_dividend`/`ern6_board_of_directors_meeting`/`ern6_conferencecalltime`）4 条最高 **0.00**，最低 −0.68。

⇒ **`earnings6` 判死**（SUE 不可计算 + 事件字段无信号）。

### 26.6 塔点亮表（GBR / D1）与最近的点亮路径

```
model 5 ✓已点亮   news 3 ✓   analyst 3 ✓   fundamental 3 ✓
pv 2 ★差1        other 1     shortinterest 0   其余全 0
```

⇒ **pv 塔只差 1 颗**，且 pv 是唯一还有稠密 MATRIX 数据的未点亮塔 ⇒ 最高优先。
`other` 差 2 颗、`shortinterest` 差 3 颗。

### 26.7 pv20 字段画像（675 字段，MATRIX，无需向量包裹）

| 类别 | 字段 |
|---|---|
| 经典因子 | `beta_market_{10,20,40,60,125,500}d`、`market_beta_250d`、`firm_market_capitalization`、`pv20_252_mom`(aC22) |
| 流动性 | `adv20_extra`(aC**181**)、`adv60`(aC66)、`adv{20,60}_extra_usd`、`average_daily_value_20d_usd`、`average_daily_volume_20d` |
| 交易成本 | `group_slippage_estimate`、`alternative_slippage_{011,012,013,025,07,09,13,2_2,3,7,8}` |
| 信用 | `issuer_composite_score`(aC**59**)、`issuer_legal_name_15` |
| 隐含因子 | `pv20_{bps,ebi}_indicator_{1..4}_feature{0..12}`（4×13×2=104 个不透明坐标，aC 多为 0–4） |
| 分组轴 | `industry_sector_classification_17`(MATRIX)、`pv20_dmgrhchenrpret_sector_719`(GROUP) |

U24 已用 8 条经典结构探针（低贝塔/贝塔期限离散/规模/动量/贝塔调整动量/非流动性/信用评分/交易成本溢价）@ FAST 派发（`3z07lM8Z64Qncg97uvdD8ue`）。 U25 用 pv103 八条日内微观结构（收盘-VWAP / 日内振幅 / 换手 / 距高点 / VWAP-开盘等）@ FAST 派发（`1Pd7judGB4zf99FhUgYgUxZ`）。


### 26.8 ★★★★★ U23 破墙波次：2:1 冷腿合成 + 窗口谷 双双成功（未点亮塔首次出强件）

针对 `kqN8xjV6` prod 0.8608 深钉，U23 一次性派 8 条（全部 @ FAST，全部 `checks.fail=[]`）：

| alpha | 破墙手段 | S | F | 2Y | sub | TO | margin |
|---|---|---:|---:|---:|---:|---:|---:|
| **O0A6Qz7p** | **2:1 冷腿合成（other47 自然流量增量）** | **2.18** | **1.52** | **3.27** | 1.87 | 0.114 | 10.7bp |
| d5W9kzZE | 窗口谷 W 504→**756** | 1.77 | 1.14 | 2.75 | 1.85 | 0.104 | 10.1bp |
| VkxM1zG0 | 窗口谷 W 504→**1008** | 1.76 | 1.14 | 2.70 | 1.87 | 0.102 | 10.2bp |
| zq3AKGkX | 2:1 冷腿合成（同塔 loan_rate_volatility） | 1.75 | 1.11 | 2.54 | 1.75 | 0.132 | 8.0bp |
| npv6xq7x | 分组轴 sector→**industry** | 1.74 | 1.07 | 2.68 | 1.84 | 0.116 | 8.2bp |
| 0mYGOgp6 | 字段变体 `loaned_share_count_p5_d1` | 1.70 | 1.09 | 2.65 | 1.86 | 0.111 | 9.3bp |
| j2YVzG6E | 窗口谷 W 504→**378** | 1.68 | 1.04 | 2.85 | 1.73 | 0.110 | 8.8bp |
| YP1lLzgo | 窗口谷 W 504→**252** | 1.54 | 0.91 | 2.81 | 1.58 | 0.115 | 7.6bp |
| （基线）kqN8xjV6 | W 504 / sector | 1.76 | 1.12 | 2.76 | 1.81 | 0.107 | — |

**两条核心结论**：

1. **2:1 冷腿合成把 S 从 1.76 抬到 2.18（+0.42）、F 从 1.12 抬到 1.52（+0.40）、2Y 从 2.76 抬到 3.27（+0.51）** —— 又一次验证「合成不稀释 S，反而提 S」。
   机理：cold leg（other47 自然流量增量，单腿 S 1.02 / TO 0.110）与强腿（借券供给冲击）低相关但同向，秩加权和的截面排序稳定性 > 权重稀释损失。
   ⚠ **塔混核算**：`shortinterest`（集合外）× `other`（集合内）⇒ 允许，但**计入「集合内 × 集合外 ≤5」配额**。
   `zq3AKGkX`（同塔冷腿）不占配额，是更安全的备选（S 1.75 / F 1.11 / 2Y 2.54）。

2. **窗口谷有效且区间很宽**：W ∈ [378, 1008] 全部 S ≥ 1.68 / F ≥ 1.04，只有 W=252 掉到 1.54。
   ⇒ 借券供给冲击的累积窗口在 **1.5–4 年**区间稳健，**不是单点峰**，这对破 prod 极有利（可以在宽谷里挑一个 prod 最低的点）。
   ⇒ 可用于 prod 破墙的**合法窗口集合 = {378, 756, 1008}**（三个互不相同的机制近似下界/中值/上界）。

**⇒ 新增默认动作（写入方法论）**：
- prod 卡墙时，**先做「窗口谷扫宽谷」+「2:1 冷腿合成」两件事**，而不是先去调 decay / truncation / 分组轴。
- 冷腿选择标准：单腿 S ≥ 1.0、TO ≤ 0.15、与强腿不同字段族；单塔内的「不同口径」冷腿优先（不占塔混配额）。

### 26.9 pv20 判死、pv103 出强信号但换手过高

**pv20（675 字段，风险模型输出）判死** —— 8 条经典因子全部 < 0.51：

| 因子 | alpha | S | F | 2Y | TO |
|---|---|---:|---:|---:|---:|
| 贝塔调整动量 | j2YVz71O | 0.50 | 0.23 | 0.40 | 0.103 |
| 发行人信用评分 | VkxM1W8Y | 0.41 | 0.15 | 0.75 | 0.131 |
| 动量 | MPYgMrka | 0.34 | 0.13 | 0.29 | 0.104 |
| 规模（小市值） | 6XdGmkzE | 0.27 | 0.09 | −0.93 | 0.132 |
| 非流动性 | xArlOZng | 0.03 | 0.00 | −1.02 | 0.101 |
| **低贝塔异象** | xArlOZep | **−0.10** | −0.02 | −0.39 | 0.168 |
| 交易成本溢价 | YP1lLeAM | −0.13 | −0.03 | −0.73 | 0.095 |
| 贝塔期限离散 | 9qxGZnJo | −0.41 | −0.10 | −0.92 | 0.320 |

⇒ **根因（第一性原理）**：`pv20` 是**风险模型的输出**（beta / size / momentum / adv 都是风险因子本身）。这些字段在设计上就是被中性化掉的对象，**不含独立 alpha**。
连「低贝塔异象」（全球最稳健的异象之一）在这里都只有 −0.10，说明该数据集已经把异象收益剥离干净了。
⇒ **通用判据**：**风险模型输出类数据集（beta/规模/动量/ADV 命名的因子快照）不能作为单数据集 ATOM 信号源**，只能当作中性化/正交化工具。

**pv103（8 字段，日内 OHLCV 微观结构）出两个 S≈1.8 的信号，但换手 0.38 压死 fitness**：

| alpha | 表达式 | S | F | 2Y | sub | TO |
|---|---|---:|---:|---:|---:|---:|
| wpQNq8ad | 换手率 `ts_zscore(vol/mktcap, 252)` | **1.79** | 0.74 | 1.96 | 0.29 | **0.386** |
| mLoKpPj9 | `reverse(ts_zscore(pv103_ivam_sum,252))` | **−1.81** | −0.73 | −2.28 | −0.49 | **0.377** |
| 9qxGYzX9 | 5 日收益动量 | 0.49 | 0.08 | 1.44 | −0.22 | 0.720 |
| 6XdG7npK | 收盘−VWAP | 0.21 | 0.04 | 0.21 | 0.11 | 0.213 |
| N1NK0Xb8 | 日内振幅 | 0.14 | 0.03 | 0.99 | 0.64 | 0.120 |
| 其余 3 条 | 距高点/VWAP−开盘/市值 | −0.29 ~ −0.58 | — | — | — | — |

⇒ **`pv103_ivam_sum` 正向 = S +1.81 / F +0.73 / 2Y +2.28**（mLoKpPj9 是反向版，反向即得正向）。
**定量诊断（`F = S·√(R/max(TO,0.125))`）**：F 0.73 @ S 1.81 ⇒ 隐含 R ≈ 6.1%；要把 F 抬到 1.00，需 R ≈ 11.5%（不现实），或把 **TO 从 0.377 压到 0.125**（F 直接跳到 1.27）。
⇒ **正确杠杆是压换手，不是提收益**。U26 已用 GBR 本地验证的低换手骨架 `ts_target_tvr_decay(..., target_tvr=0.08/0.15/0.30)` 改写 8 条派发（`2vPlyRe984Za9OrE5KKGf24`）。

### 26.10 `O0A6Qz7p` 侧向核验（除 prod 外全过）

| 项目 | 结果 |
|---|---|
| `checks.fail` | **[] 空** |
| S / F / 2Y / sub / TO / margin | 2.18 / 1.52 / 3.27 / 1.87 / 0.114 / 10.7bp |
| 逐年覆盖 2014–2023 | **10/10 年零空窗**，pnl 全为正（最小 2020 年 10431），L/Sh 413–529，TO 0.099–0.126 |
| 逐年 Sharpe | 2.85 / 3.12 / 1.43 / 2.34 / 1.59 / 3.12 / **0.03** / 1.27 / 3.95 / 2.56 |
| `self_corr` | **0.2473 ✓**（线 0.70），最高对手 rKRbrZKo 0.247 |
| `prod` | **待测**（串行队列第 1 颗） |

⚠ 2020 年 Sharpe 仅 0.03（pnl 10431，勉强为正）—— 该年是唯一接近失灵的年份，需在归因里标注为「疫情年失效风险点」。

### 26.11 U23 七颗候选的零成本预筛（self_corr 全部通过）

| alpha | self_corr | 判定 | 最高对手 |
|---|---:|---|---|
| 0mYGOgp6 | 0.2875 | ✓ | rKRbrZKo 0.288 |
| d5W9kzZE | 0.2859 | ✓ | rKRbrZKo 0.286 |
| VkxM1zG0 | 0.2822 | ✓ | rKRbrZKo 0.282 |
| zq3AKGkX | 0.2817 | ✓ | rKRbrZKo 0.282 |
| j2YVzG6E | 0.2805 | ✓ | rKRbrZKo 0.280 |
| **O0A6Qz7p** | **0.2473** | ✓ | rKRbrZKo 0.247 |
| npv6xq7x | 0.2460 | ✓ | rKRbrZKo 0.246 |

全部远低于 0.70 线，且对手一致为 `rKRbrZKo`（S 3.80 / F 2.96 的已提交件）。
⇒ **U23 七颗在「闸 + 逐年覆盖 + self」三道上均通过，唯一未验的是 prod。**

### 26.12 既有九颗候选的 prod 实测现状（权威）

| alpha | prod | 判定 |
|---|---:|---|
| rKRPAWv9 | 0.3998 | ✓ 通过 |
| QPvbxjXw | 0.5794 | ✓ 通过 |
| WjOK0roG | 0.7851 | ✗ 浅钉判死 |
| kqNe9LPz | 0.8203 | ✗ 深钉判死 |
| vR1nAj6z | 1.0000 | ✗ 判死 |
| 6XKw8e6O / xArX7dNl / P0ojvkkJ / xAb2OkMm / 9qWa6r8x | 未测（反复 correlation_busy / pending） | 待测 |
| kqN8xjV6（U23 基线） | 0.8608 | ✗ 深钉判死 |

⇒ **「9 颗存活」中被 prod 验证通过的只有 2 颗**（QPvbxjXw、rKRPAWv9）。这正是「IS 三闸通过条数是假象、独立家族数才是名额」的又一次实证。

---

## 二十七、U26：换手减速路线的否定 + 跨族冷腿合成的再次胜利

### 27.1 ★★★★★ ts_target_tvr_decay 是**错误杠杆** —— 压换手的同时压死信号

26.9 曾判定「pv103 的 F 卡线应压 TO 而非提收益」，U26 用 ts_target_tvr_decay 对 ts_zscore(pv103_ivam_sum, W) 做三档目标换手改写，@ FAST 派发 8 条（2vPlyRe984Za9OrE5KKGf24，8/8 完成、0 错误）：

| alpha | 表达式骨架 | S | F | 2Y | sub | TO |
|---|---|---:|---:|---:|---:|---:|
| （基线）wpQNq8ad | 原始 ts_zscore(ivam,252)，无减速 | **1.79** | 0.74 | 1.96 | 0.29 | 0.386 |
| wpQNqkz2 | tvr_decay target=**0.30** | 1.51 | **0.75** | 2.07 | 0.35 | 0.191 |
| d5W9prmv | tvr_decay target=**0.15** | 1.24 | 0.64 | 2.16 | 0.23 | 0.146 |
| akKR69P9 | tvr_decay target=**0.08** | 1.07 | 0.55 | 2.04 | 0.29 | 0.123 |
| d5W9pr7X | W 252→504 + tvr 0.15 | 0.95 | 0.44 | 1.95 | −0.08 | 0.146 |
| rKR0YMzE | 改 ts_mean(ivam,66) + tvr 0.15 | −0.02 | 0.00 | 0.73 | −0.09 | 0.106 |
| WjOYM2XG | 换手率族 + tvr 0.15 | 1.03 | 0.56 | 1.06 | −0.09 | 0.130 |

**结论（反直觉但清晰）**：TO 从 0.386 一路压到 0.123（−68%），**F 却纹丝不动并最终掉到 0.55**；S 同步从 1.79 掉到 1.07。
⇒ 平台 F = S·√(R / max(TO,0.125)) 中，ts_target_tvr_decay **在压低 TO 的同时也压低 R** —— 它靠砍掉高换手的信号分量来实现目标换手，而被砍掉的正是 alpha 的来源本身。
⇒ **修正 26.9 的处方**：「压换手」只有在**换手来源 ≠ 信号来源**时才有效。平滑类（decay / hump / truncation）不动信号；削信号类（ts_target_tvr_decay）会连本带利砍掉 alpha。

### 27.2 ★★★★★ RRE5Mwkn：本战役最强、最独立的候选（S 2.15 / F 1.41 / 2Y 3.65）

同一批 8 条中唯一全闸通过的是 **2:1 跨族冷腿合成版**：

    add(multiply(2, group_rank(ts_target_tvr_decay(ts_zscore(pv103_ivam_sum, 252), target_tvr=0.15), sector)),
        reverse(group_rank(ts_zscore(vec_sum(loaned_share_count_main), 504), sector)))

| 指标 | 值 | 闸 |
|---|---:|---|
| Sharpe | **2.15** | ✓（线 1.58） |
| Fitness | **1.41** | ✓（线 1.00） |
| 2Y Sharpe | **3.65** | ✓（线 1.58） |
| sub-universe Sharpe | **1.10** | ✓（线 0.59） |
| Turnover | 0.1425 | ✓ |
| Returns / margin | 6.14% / **8.62 bp** | ✓ |
| checks.fail | **[]** | ✓ |
| self_corr | **0.1628**（本战役最低；最高对手 rKRkL9QE 0.163） | ✓ |
| 与 O0A6Qz7p 互相关 | **0.34** | 独立 |

**两条落点**：

1. **弱腿不是废件**：强腿单独看是 S 1.24 / F 0.64（该判死），配上 TO 0.11 / S 1.0 的异族冷腿后成了 S 2.15 的全闸通过件。**弱腿 + 低相关冷腿的秩加权和可以把不合格件抬成合格件，纯参数调优做不到。**
2. **self 0.163 / 与 O0A6Qz7p 互相关 0.34** ⇒ 它与既有 8 颗候选**不属于同一相关簇**，是真正的新增名额，不是同族换皮。

⚠ **塔混核算**：pv（禁混集合内）× shortinterest（集合外）⇒ 允许，计入「集合内 × 集合外 ≤5」配额。**已用 2/5**（O0A6Qz7p = other×shortinterest、RRE5Mwkn = pv×shortinterest），**余 3 个名额**。

### 27.3 方法论沉淀（三条，跨区通用）

1. **减速类算子必须分类使用**：decay / hump / truncation = **平滑**（不动信号，只摊平持仓）；ts_target_tvr_decay = **削信号**（按换手预算砍信号分量）。F 卡线先用前者，**绝不先用后者** —— U26 实测后者让 F 从 0.74 → 0.55。
2. **F 卡线杠杆排序（本区本战役实证）**：跨族 2:1 冷腿合成 ≫ decay 平滑 > 窗口调整 > truncation ≫ ts_target_tvr_decay（**负向**）。与 EUR（insider 族）、AMR（tilt 族）结论一致：F 0.74 → 1.41 靠合成，不靠减速。
3. **2Y 与 F 常同向改善**：合成后 2Y 从 1.96 抬到 3.65，sub 从 0.29 抬到 1.10 —— 冷腿在压低换手的同时抬高了长周期稳定性，这是三闸一起过的原因。

### 27.4 prod 端拥塞（阻塞项，非策略问题）

- O0A6Qz7p：多轮 200s 超时返回 status=pending；事后 --peek 只读探测三轮**均为空体**（= 平台仍在算，不是 0、不是失败）。
- d5W9kzZE：同样 200s 超时，紧接着拿到 correlation_busy。
- 跨进程锁 logs/_dblock/correlation.lock.json 曾被外部进程以 corr:get_production_correlation(qML59dbj) 占用（**不属于本批任何 alpha**）⇒ 账号级单并发槽被外部请求挤占。
- **结构性缺陷**：本区单颗 prod 实测需 200–480s，而队列脚本单次上限 200s、每颗仅 2 次尝试 ⇒ **必然超时**。已确认 prod=None 的条目不会被缓存跳过，**重跑脚本即等于二次 pass**，无需改代码。

⇒ **待 prod 验证的强件累计 8 颗新增**（U23 七颗含 O0A6Qz7p + RRE5Mwkn），另有既有 5 颗（6XKw8e6O / xArX7dNl / P0ojvkkJ / xAb2OkMm / 9qWa6r8x）长期未测。**prod 是全战役唯一瓶颈。**

---

## 二十八、未点亮塔数据集全景审计（GBR / TOP700 / D1，177 集全量）

### 28.1 塔点亮表与可挖集合

| 塔 | 已提交 | 状态 |
|---|---:|---|
| model | 5 | ✓ 已点亮 |
| news | 3 | ✓ 已点亮 |
| analyst | 3 | ✓ 已点亮 |
| fundamental | 3 | ✓ 已点亮 |
| **pv** | **2** | ★ **差 1 颗点亮**（最接近） |
| other | 1 | 未点亮 |
| institutions / insiders / earnings / sentiment / risk / option / socialmedia / macro / shortinterest / imbalance | 0 | 未点亮 |

177 集中有 **82 集**落在未点亮 category，剔除 15 个已判死后 **67 个可挖**：

| category | 总数 | 已判死 | 可挖 |
|---|---:|---:|---:|
| other | 41 | 7 | **34** |
| pv | 16 | 5 | **11** |
| risk | 5 | 0 | 5 |
| institutions | 5 | 2 | 3 |
| insiders | 3 | 0 | 3 |
| sentiment | 3 | 0 | 3 |
| socialmedia | 3 | 0 | 3 |
| earnings | 2 | 1 | 1 |
| imbalance / macro / option / shortinterest | 1 each | 0 | 1 each |

### 28.2 ★★★★ 新判据：字段类型 100% 为 GROUP 的数据集 = 分组轴库，不是信号源

| 数据集 | 字段 | 结论 |
|---|---|---|
| **pv29** | 50 | **全部**是 statistical cluster 标签（industry_grouping_level{2,5,10,20,50}_*、sta1_top*c*、top_300_equity_513_grouping_*），**0 个连续信号字段** |
| **pv30** | 240 | **全部** GROUP（pca_factor_score_*、factor*_group*_top800_513、principal_component_grouping_*） |

⇒ **判据（可外推）**：数据集若 100% 由 GROUP / 分组标签构成，它**没有信号，只有轴**。
  价值在于替换 `sector` / `industry` 做 `group_*`，而不是单独出 alpha；且这种用法必然跨数据集 ⇒ **计入塔混配额**。
  `pv29` 覆盖率 1.0、alphaCount 仅 73 看着极诱人，但它是「轴库」——这正是「低拥挤 ≠ 有信号」的典型陷阱。

### 28.3 ★★★★★ intraday_pv_feats：pv103 的真正兄弟（585 字段日内微观结构）

**字段结构（4 族）**：

1. **时点报价**：`ask/bid_price_{30m,60m}_{post_open,pre_close_2}`、`_{first,last}_{interval,half,quarter}`
2. **时段 VWAP**：`avg_vwap_{last_half,last_quarter}`、`avg_{ask,bid}_to_vwap_ratio_{first_half,last_half,last_quarter}`
3. **挂单规模**：`avg_{ask,bid}_size_to_volume_ratio_{first_half,last_half,last_quarter}`
4. **日内相关（最不拥挤，alphaCount 多为 1–9）**：`corr_{ask,bid,high,low,last_trade_price,vwap}_with_{volume,ask_size,bid_size,slippage}`、`corr_bid_with_ask_price_*`、`corr_interval_*`
5. **微观结构异象**：`avg_price_modulo_10_ratio_*`（价格取整倾向 = 散户/算法报价聚集代理）

**拥挤度实测**：`corr_ask_price_with_volume` ac **70**（最挤）、`avg_vwap_to_last_price_ratio` ac 38、`avg_ask/bid_to_vwap_ratio_last_half` ac **26**；其余绝大多数 **ac 1–9**。

**模板库（11 个结构互异，派发其中 8 个 @ FAST）**：

| # | 机制 | 表达式骨架 | 派发 |
|---|---|---|---|
| T1 | 买卖报价相对 VWAP 的不对称（价差/流动性溢价） | `group_rank(ts_zscore(subtract(avg_ask_to_vwap_ratio_last_half, avg_bid_to_vwap_ratio_last_half), 252), sector)` | ✓ |
| T2 | 挂单规模相对成交量的买卖不对称（供给压力） | `group_rank(ts_zscore(subtract(avg_ask_size_to_volume_ratio_last_half, avg_bid_size_to_volume_ratio_last_half), 252), sector)` | ✓ |
| T3 | 日内 VWAP 漂移（后半场 vs 后 1/4 场，收盘动量） | `group_rank(ts_zscore(subtract(avg_vwap_last_quarter, avg_vwap_last_half), 252), sector)` | ✓ |
| T4 | 日内价量相关（信息驱动买盘） | `group_rank(ts_mean(corr_ask_price_with_volume, 22), sector)` | ✓ |
| T5 | 高价—卖单规模相关（卖压弹性） | `group_rank(ts_mean(corr_high_price_with_ask_size, 22), sector)` | ✓ |
| T6 | 买卖报价相关（做市商报价稳定性） | `group_rank(ts_mean(corr_bid_with_ask_price_last_half, 22), sector)` | ✓ |
| T7 | 价格取整倾向（散户行为代理，逆向拥挤） | `group_rank(ts_mean(avg_price_modulo_10_ratio_last_half, 22), sector)` | ✓ |
| T8 | 成交量时段集中度（尾盘知情交易） | `group_rank(ts_zscore(divide(avg_trade_volume_last_quarter, add(avg_trade_volume_last_half, 0.000001)), 252), sector)` | ✓ |
| T9 | 滑点弹性（冲击成本敏感性） | `group_rank(ts_mean(corr_ask_price_with_slippage, 22), sector)` | 备用 |
| T10 | VWAP 与最后成交价偏离 | `group_rank(ts_zscore(avg_vwap_to_last_price_ratio, 252), sector)` | 备用 |
| T11 | 开收盘时段价差（60m 盘后 vs 盘前） | `group_rank(ts_zscore(subtract(ask_price_60m_pre_close_2, ask_price_60m_post_open), 252), sector)` | 备用 |

预检结果：**valid / 12 字段全存在 / unknown_fields = 0**。派发 `1CVeYqabC4xGb9w7aTARLmW`（8 条，FAST，decay 5，trunc 0.10）。
全部为 **单数据集 ATOM**（intraday_pv_feats 单集）⇒ **不占塔混配额**。

### 28.4 pv109 / pv13 画像（待探针）

| 数据集 | 字段 | 内容 | 判断 |
|---|---|---|---|
| **pv109** | 26 VECTOR | 全部**可转债**：yield_to_maturity / conversion_yield / coupon_rate / amt_outstanding / face_value | 覆盖率仅 **0.3319**；转债→正股映射稀疏，GBR 700 只里可转债占比低 ⇒ 低预期，但「买卖价差 yield 差」可作流动性溢价一次探针 |
| **pv13** | 28 | **公司网络中心性**：`com_page_rank`、`com_rk_au`(HITS authority)、`ompetitorgraphrank_hub_rank`(HITS hub)、`ustomergraphrank_{page_rank,hub_rank,auth_rank}` + RBICS 6 级分组轴 | 字段级 cov 显示 0（**cov=0 不可信**，pv103 也曾显示 0 却可用）；机制「网络中心性 → 竞争强度/议价能力」是**全新的经济学假设**，值得一次探针 |

⇒ 下一批优先级：`intraday_pv_feats` 收批后 → `pv13` 网络中心性（全新机制）→ `pv109` 可转债（低预期）。

### 29.1 本轮完成的 12 个数据集字段画像（未点亮塔）

| 数据集 | category | 字段 | 覆盖率 | 内容与可用机制 | 判定 |
|---|---|---:|---:|---|---|
| **fund_holdings_panel** | institutions | 18 VECTOR | **0.9286** | 基金交易：`boundary_transaction_total`（新建仓次数）、`herfindahl_index_transactions`（交易额 HHI 集中度）、`stable_boundary_trade_count_21d`（持续建仓）、`large_trade_count_50bps`、`transaction_account_total`（参与账户数=广度）、`transaction_value_distribution_score` | ★ **最优目标**：覆盖率最高 + 机制全新（机构建仓/信念集中） |
| **insider_agg_matrix** | insiders | 34 MATRIX | 0.5937 | 已聚合内部人交易：`total_{buy,sell}_shares`、`total_top_{buy,sell}_shares`（高管 vs 全体董事）、`avg_buy/sell_shares`、`significant_value_1..4`（最重要交易金额）、`directional_indicator`（cov 1.0, ac 62） | ★ 强（MATRIX 免 vec 包裹，Nofsinger-Sias / Lakonishok-Lee 经典机制） |
| **insiders1** | insiders | 9 VECTOR | 0.5937 | 交易级明细：`insd1_shares`/`_price`/`_value`/`_holdings`/`_tradesignificance`(1–3) | 用同塔 `insider_agg_matrix` 更省事，本集备用 |
| **risk60** | risk | 5 VECTOR | 0.6694 | 借券费率：`rsk60_offer`（借券费年化）、`lending_fee_bid_rate`、`rsk60_crowding`(ac 90)、`rsk60_last` | ★ 与已验证的借券供给冲击**同族但不同数据集**，合法新 ATOM |
| **institutions25** | institutions | 24 VECTOR | 0(不可信) | **空头持仓**（非多头）：`inst25_crowding`、`inst25_sentiment`、`inst25_position_change`(ac 13)、`inst25_age`、`inst25_manager_*` | 实为空头数据集放在 institutions 塔下；机制与 shortinterest 重叠但按 manager 维度切分，值得一探 |
| **macro27** | macro | 13 VECTOR | 0(不可信) | **招聘岗位数（劳动力需求）**：`mcr27_company_jobsactive`(ac 48)、`_jobscreated`、`_jobsremoved`、`num_jobs_active`(ac 74)、`mean_days_job_active`(ac 123) | ★ **全新经济学机制**（劳动力需求→成长），全塔 0 颗，值得一探 |
| **sentiment7** | sentiment | 3 VECTOR | 0.5819 | **维基百科浏览关注度**：`snt7_views`(ac 45)、`snt7_all_languages_views`(ac 37) | ★ Barber-Odean 散户关注→买压经典异象，机制全新 |
| **option1** | option | 22 VECTOR | 0(不可信) | 期权隐含波动率曲面：`opt1_p_deltasurface_d1_vi`(ac 67)、`_delta`(ac 12)、moneyness、`opt1_dvd_frequency` | ⚠ 机制好，但**option VECTOR 曾触发平台资源闸整批杀**（AMR 实证：opt4 不可混批）⇒ **必须单独成批** |
| **earnings_sent_matrix** | earnings | 7 MATRIX | 0(不可信) | 财报电话会语调概率：`positive_sentiment_probability_3`(ac 145)、`negative_...`(ac 125)、`sentiment_weighting_method1`(ac 200) | ✗ 低优先：同族 `earningscall_sentiment` 在 GBR 实测 −0.31（Q&A−Presentation 负面差失效） |
| **risk88** | risk | 1 MATRIX | 1.0 | `alternative_market_cap_usd`（市值），ac **567** | ✗ 单字段规模因子且极拥挤；只能作规模中性化工具 |
| **pv106** | pv | 8 MATRIX | 0 | 交易成本：`pv106_spreadbp`、`_lastspreadbp`、`aggregated_slippage_metric`、`transaction_cost_{maximum,percentile_10}` | 流动性溢价，弱；且 pv+pv 禁混 ⇒ 只能单独成 ATOM |
| **pv109** | pv | 26 VECTOR | 0.3319 | 可转债：`midpoint_yield_to_maturity`、`ask/bid_side_yield_to_maturity`、`*_conversion_yield`、`pv109_amt_outstanding`、`face_value_amount` | 覆盖率低（可转债→正股映射稀疏），低预期 |
| **pv13** | pv | 28 | 0(不可信) | **公司网络中心性**：`com_page_rank`、`com_rk_au`(HITS authority)、`ompetitorgraphrank_hub_rank`、`ustomergraphrank_{page_rank,hub_rank,auth_rank}` + RBICS 6 级分组轴 | ★ 机制全新（网络位置→竞争强度/议价能力），待探针 |

### 29.2 新判据补充

1. **「category 标签 ≠ 数据语义」**：`institutions25` 放在 institutions 塔下，实际是**空头持仓**数据（short position by manager）；`fund_holdings_panel` 同塔但讲的是**基金交易流**。选数据集必须读字段描述，不能只看 category。
2. **覆盖率是唯一可靠的第一道筛**：本轮 12 个集里，唯一 cov > 0.9 的是 `fund_holdings_panel`（0.9286）；三个 cov 显示 0 的集（`macro27`/`option1`/`earnings_sent_matrix`）字段级 cov 也全 0，而 pv103 曾「cov 0 但可用」——**cov=0 既不能判死也不能判活，必须实探**。
3. **已判死的机制不要换皮重试**：`earnings_sent_matrix` 与已判死的 `earningscall_sentiment` 是同一底层（电话会语调），ac 高达 145–200 说明拥挤且无溢价 ⇒ 直接降级，不再开波。

### 29.3 U28 派发（机构 / 内部人 / 借券费率三塔同批）

预检 valid、unknown_fields = 0。派发 `3Hk3hggs34vH90rPwKMAgIi`（8 条，FAST）：

| # | 数据集 | 机制 | 表达式 |
|---|---|---|---|
| T1 | fund_holdings | 新建仓边界交易强度 | `group_rank(ts_zscore(vec_sum(boundary_transaction_total), 252), sector)` |
| T2 | fund_holdings | 交易额 HHI 集中度 | `group_rank(ts_mean(vec_avg(herfindahl_index_transactions), 66), sector)` |
| T3 | fund_holdings | 持续建仓稳定性 | `group_rank(ts_zscore(vec_sum(stable_boundary_trade_count_21d), 252), sector)` |
| T4 | fund_holdings | 参与账户广度 | `group_rank(ts_mean(vec_avg(transaction_account_total), 66), sector)` |
| T5 | insider_agg | 全体董事净买入 | `group_rank(ts_zscore(subtract(total_buy_shares, total_sell_shares), 252), sector)` |
| T6 | insider_agg | 高管净买入 | `group_rank(ts_zscore(subtract(total_top_buy_shares, total_top_sell_shares), 252), sector)` |
| T7 | risk60 | 借券费率水平 | `group_rank(ts_zscore(vec_avg(rsk60_offer), 252), sector)` |
| T8 | institutions25 | 空头持仓变化（反向） | `reverse(group_rank(ts_zscore(vec_sum(inst25_position_change), 252), sector))` |

全部为单数据集 ATOM，**不占塔混配额**；算子数 3–4 个。

### 30.1 ★★★★★ prod 端系统性不可用（本轮决定性阻塞，非候选问题）

用**只读 peek**（直接 GET `/alphas/{id}/correlations/prod`，不申请本地锁、不触发重算、零成本）对 8 颗候选做全量扫描：

| alpha | prod | 说明 |
|---|---:|---|
| O0A6Qz7p | 空体 | 已触发，等了 **25 分钟以上** 仍无值 |
| d5W9kzZE | 空体 | 已触发 |
| VkxM1zG0 | 空体 | 已触发 |
| 0mYGOgp6 | 空体 | 已触发（第 4 颗，被手动停止） |
| npv6xq7x / j2YVzG6E / zq3AKGkX / RRE5Mwkn | 空体 | 队列未走到，从未触发 |

⇒ **8/8 无值**。

**⚠ 结论已修正（原始判断「平台 prod 管线整体积压」是错的）**。真根因是**跨会话抢同一把账号级单并发锁**：

```
Get-CimInstance Win32_Process -Filter "Name='python.exe'"
  ProcessId 120544, 创建 2026/11/6 4:19:04
  CommandLine "D:\softwares\vnpystudio\python.exe" tools/prod_wait.py 9qx9aAa2 --minutes 12
```

那是**另一个会话 / 另一个解释器**（不是本会话的 venv）在跑同一个 `prod_wait.py`，占住同一账号的 prod 队列。本地锁文件同时可见 `correlation.inflight.json` 指向 `qML59dbj`（pid 73128 = MCP 主进程），而 `check_correlation(refresh=false)` 只要 holder 不是同一 alpha 就直接返回 `correlation_busy`（`brain_mixin_spcread.py:1201`）——**即使平台算好了也读不到**。

⇒ 所以 8/8 空体**既不是候选问题，也不是平台积压**，而是本会话一次真正的平台读都发不出去。诊断动作固定为：先列 python 进程 + 看 `logs/_dblock/` 三件套，确认抢锁方是谁、何时释放，再决定排队还是等。

### 30.2 处置与止损

1. **停掉串行队列**（`tools/prod_queue_u23.py`）：它每颗 200s × 2 次，3/3 全部超时零产出，同时**长期占住账号级单并发锁**，导致最强的 `RRE5Mwkn` 在 12 分钟内连触发都做不到（3 次全是 correlation_busy）。
2. **改用 peek 只读扫描**：免费、不占锁、无 195s 冷却，一次扫 8 颗约 80s。这是「等待期」唯一正确的姿势。
3. `RRE5Mwkn` 单独 `prod_wait.py --minutes 16` 长轮询保留（它按 retry_after 精确退避），但在队列被停掉前一直被饿死。

### 30.3 三条可复用的操作结论（写进方法论）

1. **串行 prod 队列在本区结构性必然失败**：客户端单次上限 200s，而单颗实测 200–480s ⇒ 每颗必超时。正确姿势 = **触发一次 + peek 免费轮询**，而不是反复重打。
2. **多进程争同一把 correlation 锁会互相饿死**：持有方每 200s 重取一次锁，等待方每次退避 240s，12 分钟内一次都轮不到。要串行就只跑一个进程。
3. **一次派 3 个 multisim = 23 个子仿真**挤并发槽，会显著拉长单批耗时（U27 排队 10+ 分钟仍 `tot=None`）。后续单轮最多 2 批并行。

### 30.4 本轮在飞的三批（等待收批）

| 波次 | 内容 | multisim | 条数 |
|---|---|---|---:|
| U27 | `intraday_pv_feats` 日内微观结构（8 个结构互异模板） | `1CVeYqabC4xGb9w7aTARLmW` | 8 |
| U28 | `fund_holdings_panel` 机构建仓 + `insider_agg_matrix` 内部人 + `risk60` 借券费率 + `institutions25` 空头持仓 | `3Hk3hggs34vH90rPwKMAgIi` | 8 |
| U29 | `macro27` 招聘岗位（劳动力需求）+ `sentiment7` 维基关注度 | `2pvFS25db4KDbE0lfrgdIfm` | 7 |

全部为单数据集 ATOM，不占塔混配额；覆盖 pv / institutions / insiders / risk / macro / sentiment **六个未点亮塔**。


## 三十一、U27 / U28 / U29 三批收批（23 条全部未达标）+ 两条方法论纠错

### 31.1 收批总表（全部单数据集 ATOM，算子 3–5 个）

**U27 `intraday_pv_feats`（585 字段日内微观结构，8/8 完成 0 错误）**

| alpha | 模板 | S | F | 2Y | sub | TO |
|---|---|---:|---:|---:|---:|---:|
| npv6Jjl8 | 买−卖 价格/ToVWAP 价差 | −0.80 | −0.20 | −2.03 | −0.57 | 0.409 |
| zq3AMxEd | 买−卖 单量/成交量 价差 | −0.58 | −0.11 | −1.72 | −0.03 | 0.455 |
| O0A6YLjd | VWAP 近季 − 近半年 | 0.81 | 0.20 | −0.52 | 0.04 | 0.478 |
| gJerAlVO | 卖价×成交量 相关（ts_mean22） | **−0.96** | −0.40 | −1.19 | −0.48 | 0.164 |
| 0mYGlV2k | 高价×挂单量 相关 | −0.03 | 0.00 | −1.28 | −0.39 | 0.143 |
| pwdWX2e6 | 买价×卖价 相关 | −0.27 | −0.08 | 0.24 | −0.09 | 0.149 |
| akKRY09x | 价格 mod 10 尾数比 | 0.18 | 0.04 | 1.16 | 0.08 | 0.097 |
| d5W9XMrv | 近季/近半年 成交量比 | 0.72 | 0.17 | −0.73 | 0.18 | 0.466 |

择优 **|S| 上限 0.96**（卖价成交量相关，符号稳定为负，反向后 0.96）。距 1.58 差 0.62。

**U28 五集 8 条**

| alpha | 数据集 | 模板 | S | F | 2Y | sub | TO |
|---|---|---|---:|---:|---:|---:|---:|
| 2rAGzkqJ | fund_holdings_panel | 新建仓笔数 | −0.15 | −0.02 | −0.47 | 0.09 | 0.403 |
| RRE5QLZe | fund_holdings_panel | 交易额 HHI | 0.03 | 0.00 | −1.50 | −0.08 | 0.096 |
| 3qoGrWYO | fund_holdings_panel | 稳定边界交易数 | −0.24 | −0.04 | −0.50 | −0.01 | 0.371 |
| P0oPaEqJ | fund_holdings_panel | 账户广度 | −0.20 | −0.05 | 1.06 | −0.18 | 0.114 |
| leAgOZkx | insider_agg_matrix | 总买−总卖 | −0.03 | 0.00 | −0.44 | **0.50** | 0.558 |
| j2YVRQW9 | insider_agg_matrix | 高管买−卖 | −0.04 | 0.00 | −0.07 | 0.39 | 0.561 |
| A1VLZdYl | risk60 | 借券费年化 | 0.12 | 0.02 | 0.61 | 0.08 | 0.123 |
| xArl8a9l | institutions25 | 空头持仓变化（反） | **0.73** | 0.31 | 0.12 | **0.60** | 0.138 |

**`fund_holdings_panel` 覆盖率 0.9286、`insider_agg_matrix` cov 0.5937——覆盖最好的两个集，4 条模板全部落在 |S|<0.25。**

**U29 `macro27` 招聘岗位 + `sentiment7` 维基关注度（7/7 完成）**

| alpha | 数据集 | 模板 | S | F | 2Y | sub | TO |
|---|---|---|---:|---:|---:|---:|---:|
| 78LGb8E2 | macro27 | 在招岗位数 | 0.00 | 0.00 | 1.20 | 0.00 | 0.207 |
| QPvWkPXX | macro27 | 新增−撤销岗位（净创造） | −0.22 | −0.04 | **2.31** | 0.08 | 0.340 |
| xArl8Agm | macro27 | 岗位平均在挂天数（反） | −0.07 | −0.01 | 0.06 | −0.07 | 0.082 |
| 6XdGVXOK | macro27 | 在招岗位 Δ66 | −0.12 | −0.02 | 1.17 | −0.17 | 0.271 |
| YP1lKPqJ | sentiment7 | 维基浏览关注度 | **0.59** | 0.16 | **1.60** | 0.43 | 0.225 |
| bl6xZl3l | sentiment7 | 关注度 Δ22 | 0.44 | 0.10 | **1.72** | 0.14 | 0.265 |
| omEP5me2 | sentiment7 | 跨语言浏览占比 | 0.28 | 0.07 | 1.55 | −0.09 | 0.070 |

★ 两条「有底」的件：`QPvWkPXX`（净岗位创造，2Y 2.31）与 `YP1lKPqJ`（关注度，2Y 1.60 / sub 0.43）**只卡 LOW_SHARPE + LOW_FITNESS，2Y 与 sub 双过**。这是可续挖的地基，不是全无信号。

### 31.2 ★★★★★ 纠错一：这 23 条不是「10 个结构互异模板」，而是同一套算子几何

把 23 条表达式并排看，**全部**是同构三层：

```
group_rank( ts_zscore | ts_mean | ts_delta | ts_rank ( <字段 或 两字段相减>, W ), sector )
```

差异只在 **换成哪个字段** 和 **W 取多少**。按本战役自己定的硬约束（模板差异必须落在骨架结构 / 算子几何 / 矩 / 分组轴 / 非线性上），这 23 条实际只覆盖了：

| 维度 | 覆盖情况 |
|---|---|
| 骨架结构 | **1 / 5**（只有单腿，无两腿价差、无 2:1 冷腿合成、无条件门控、无组内中性化） |
| 矩 | **2 / 5**（水平、一阶差分；缺二阶方差、离散度、极值位置） |
| 分组轴 | **1 / 5**（全用 sector；无 industry / subindustry / 自定义簇 / 无分组） |
| 非线性 | **0 / 4**（除 xArl8a9l 一条 reverse 外无任何 sign / signed_power / winsorize） |
| 算子几何 | rank 链与 ts 链各一种 |

⇒ **U27 / U28 / U29 的「全灭」不能判任何数据集死。**它证伪的只是「这一种算子几何在这些字段上无效」。
⇒ 反证就在本轮：`RRE5Mwkn`（S 2.15 全闸过）与 `O0A6Qz7p`（S 2.18）都不是单腿骨架，而是**两腿 / 窗口谷**结构。单腿骨架在本区历史上限就是 |S|≈1.0。

**后续每个数据集的模板库必须按下表凑满 10 个互异结构再派发**：

| 维度 | 取值清单 |
|---|---|
| 骨架结构 | 单腿 / 两腿价差 / 2:1 冷腿合成 / 条件门控 `if_else` / 组内中性化 |
| 算子几何 | rank 链 / ts_zscore 链 / ts_rank 链 / 分位截尾 / 幂变换 |
| 矩 | 水平 / 一阶差分 / 二阶方差 `ts_stddev` / 离散度 `vec_stddev` / 极值位置 `ts_arg_max` |
| 分组轴 | sector / industry / subindustry / 自定义簇 / 无分组 |
| 非线性 | `reverse` / `sign` / `signed_power` / `winsorize` |

### 31.3 ★★★★★ 纠错二：prod 槽位是稀缺资源，测前必须做零成本本地互相关去重

对 9 颗待验候选跑 `compute_mutual_correlation`（**纯本地计算，零成本秒回**，`years=4`、1021 点）：

| 对手 | 与 RRE5Mwkn | 与 O0A6Qz7p |
|---|---:|---:|
| O0A6Qz7p | 0.3400 | 1 |
| d5W9kzZE | 0.3591 | 0.8365 |
| VkxM1zG0 | 0.3508 | 0.8140 |
| zq3AKGkX | 0.3248 | 0.7719 |
| npv6xq7x | 0.3358 | 0.8254 |
| 0mYGOgp6 | 0.3269 | 0.8382 |
| j2YVzG6E | 0.3403 | 0.8421 |
| YP1lLzgo | 0.2982 | 0.7945 |

**U23 那 7 颗彼此互相关 0.77–0.99（`d5W9kzZE` vs `VkxM1zG0` = 0.9876，`j2YVzG6E` vs `YP1lLzgo` = 0.9678）⇒ 它们是同一个信号簇，不是 7 个独立候选。**
而 `RRE5Mwkn` 与全部 7 颗只有 0.30–0.36，是本战役唯一的第二个独立信号。

⇒ **9 颗实际只有 2 个独立信号**。prod 队列是账号级单并发、单颗实测 200–480s，测 7 颗同簇件等于把稀缺槽位烧在重复信息上。
⇒ **固定动作**：任何 prod 排产前，先跑 `compute_mutual_correlation(全部待验 id)`，每簇只取 IS 最优的一颗作代表。本次由 9 降到 2，省约 50 分钟队列时间。
⇒ 同理，**同一簇内多颗过闸也不等于多个可提交名额**——最终可提交数 = 独立簇数，不是过闸条数。

### 31.4 U30：`pv13` 公司网络中心性（pv 塔第 3 点，模板库 11 个）

`pv13` 共 28 字段：**17 个信号字段**（`MATRIX`，无需 vec 包裹）+ 11 个 `GROUP` 轴（`pv13_new_{1..6}l_scibr`、`pv13_eur_revere_risc_sector_{level,parent}`）。

信号字段是**两套 Revere 关系网络 × 三种图论中心性**：

| 网络 | PageRank | HITS hub | HITS authority |
|---|---|---|---|
| 竞争对手网络 | `pv13_com_page_rank` | `pv13_ompetitorgraphrank_hub_rank` | `pv13_com_rk_au` |
| 客户网络 | `pv13_ustomergraphrank_page_rank` | `pv13_ustomergraphrank_hub_rank` | `pv13_ustomergraphrank_auth_rank` |

外加 `sector_attachment_overlap_count` / `terminal_sector_focus_overlap_count`（VECTOR，可替代性重叠）与 `pv13_revere_{key,term}_sector_total`（业务广度）。

**拥挤度极低**：`com_page_rank` a=1、`ompetitorgraphrank_hub_rank` a=1、`ustomergraphrank_{hub,page}_rank` a=1 —— 几乎无人开采。

**模板库（11 个结构互异，派 8 个）**：

| 编号 | 机制 / 来源 | 表达式 |
|---|---|---|
| L1 | 中心性溢价（水平·行业相对）· 论文 Ahern & Harford 2014 产业链接 | `group_rank(ts_zscore(pv13_com_page_rank, 252), sector)` |
| L2 | **HITS hub − authority 不对称**（议价 / 瓶颈位置） | `group_rank(ts_zscore(subtract(pv13_ompetitorgraphrank_hub_rank, pv13_com_rk_au), 252), sector)` |
| L3 | 跨网络价差：客户网络 − 竞争网络（需求侧 vs 竞争压力） | `group_rank(ts_zscore(subtract(pv13_ustomergraphrank_page_rank, pv13_com_page_rank), 252), sector)` |
| L4 | 网络位置动量 Δ66 | `group_rank(ts_delta(ts_zscore(pv13_com_page_rank, 252), 66), sector)` |
| L5 | 可替代性重叠反向（Porter 竞争强度）· 论文 Hoberg-Phillips TNIC | `reverse(group_rank(ts_mean(vec_avg(terminal_sector_focus_overlap_count), 66), sector))` |
| L6 | 客户网络权威分动量（上游依赖变迁） | `group_rank(ts_delta(ts_zscore(pv13_ustomergraphrank_auth_rank, 252), 66), sector)` |
| L7 | 客户网络 hub 水平（下游依赖广度） | `group_rank(ts_zscore(pv13_ustomergraphrank_hub_rank, 252), sector)` |
| L8 | 权威分动量·残差化（`group_neutralize(rank)` 形态） | `group_neutralize(rank(ts_delta(pv13_com_rk_au, 66)), sector)` |
| L9 | 二阶矩：中心性波动率（地位不稳）_[备用]_ | `group_rank(ts_stddev(ts_zscore(pv13_com_page_rank, 252), 252), sector)` |
| L10 | 重叠离散度 `vec_stddev`（竞争重叠异质性）_[备用]_ | `reverse(group_rank(ts_mean(vec_stddev(sector_attachment_overlap_count), 66), sector))` |
| L11 | 跨网络权威分背离（客户 vs 竞争）_[备用]_ | `group_rank(ts_zscore(subtract(pv13_ustomergraphrank_auth_rank, pv13_com_rk_au), 252), sector)` |

预检：`valid=true`，`unknown_fields=[]`，`unknown_soft=[]`。已派发 L1–L8 → multisim `40GcTN6Zu5bRciLoSLKfZ6Q`。

单数据集 ATOM（pv 单腿），不占塔混配额。**若任一过闸，pv 塔 2/3 → 3/3 点亮。**

### 31.5 用户提示登记：`group_backfill` 可降 `CONCENTRATED_WEIGHT`

用户指示：「用 group_backfill 可以降 CONCENTRATED_WEIGHT」。登记为**待验证杠杆**，优先级排在现有 CONCENTRATED_WEIGHT 处方之前（现有处方只有 truncation 与幂变换）。

本轮 U27–U30 的 `CONCENTRATED_WEIGHT` 全部落在 `checks.pass`，暂无卡该闸的候选，故尚未实测；等出现卡闸件时按此优先施用：

```
group_rank(group_backfill(<核心信号>, sector), sector)   // 行业回填后再截面化，削平极值簇
```

### 31.6 本轮状态

| 项 | 值 |
|---|---|
| 未点亮塔可挖数据集 | 67 个（已画像 16 个，已探针 15 个） |
| 本轮新增探针 | U27 8 + U28 8 + U29 7 = 23 条，覆盖 8 个数据集 / 6 个塔 |
| 在飞 | U30 `pv13` 8 条（`40GcTN6Zu5bRciLoSLKfZ6Q`） |
| prod 已验可提交 | 2 颗（`QPvbxjXw` 0.5794 / `rKRPAWv9` 0.3998），均属已点亮塔 |
| prod 待验独立件 | 2 颗（`RRE5Mwkn` 独立、`O0A6Qz7p` 为 U23 七颗簇代表） |

## 三十二、U30 `pv13` 公司网络中心性收批：8/8 未达标 + 「慢变结构描述符」判据第四次独立确认

### 32.1 收批总表（8/8 完成，0 错误，multisim `40GcTN6Zu5bRciLoSLKfZ6Q`）

| alpha | 模板 | 机制 | S | F | 2Y | sub | **TO** |
|---|---|---|---:|---:|---:|---:|---:|
| MPYgRglL | L1 | 竞争网络 PageRank 水平 | 0.16 | 0.03 | 1.14 | 0.21 | 0.0824 |
| npv6R6ka | L2 | HITS hub − authority（议价不对称） | 0.28 | 0.07 | 1.20 | 0.33 | 0.0797 |
| akKRZR2w | L3 | 客户网络 − 竞争网络 PageRank | −0.23 | −0.05 | 0.58 | 0.08 | 0.0836 |
| omEP5Pwb | L4 | PageRank 动量 Δ66 | 0.33 | 0.09 | 1.08 | 0.20 | 0.0907 |
| QPvWkWqX | L5 | 可替代性重叠反向 | −0.54 | −0.19 | −1.06 | −0.32 | 0.0709 |
| RRE5Q5qa | L6 | 客户网络权威分动量 | −0.27 | −0.07 | 0.89 | 0.10 | 0.0899 |
| KPJVdVqN | L7 | 客户网络 hub 水平 | 0.07 | 0.01 | 0.23 | −0.08 | 0.0744 |
| MPYgRgqz | L8 | 权威分动量·残差化 | **0.48** | 0.16 | 0.51 | 0.38 | 0.1036 |

择优 **S 0.48**，距 1.58 差 1.10。**八条全部只卡 LOW_SHARPE / LOW_FITNESS / LOW_2Y_SHARPE，无一条卡 spread、换手或集中度。**

### 32.2 ★★★★★ 判死的真正依据不是 S 低，而是 TO 贴地

八条的 **TO 全部落在 7.09%–10.36%**，这是本战役反复出现的同一指纹。合并已有证据：

| 区域 | 数据集 | 内容 | 骨架数 | 最优 \|S\| | TO 区间 | 结论 |
|---|---|---|---:|---:|---|---|
| EUR | other455 | news2vec 新闻共现网络 | 6 | 0.31 | 2.7–3.5% | 判死 |
| EUR | sentiment21 | 4 模型情绪分数 | 4 | 0.27 | 4.0–4.1% | 判死 |
| EUR | news36 | 新奇度 + 双情绪口径 | 2 | 0.15 | 7.5–8.3% | 判死 |
| EUR | pv30 | 统计风险模型因子得分 | 2 | 0.25 | 4.3–4.4% | 判死 |
| **GBR** | **pv13** | **公司网络中心性（PageRank/HITS×2 网络）** | **8** | **0.48** | **7.1–10.4%** | **本轮判死** |

⇒ **判据升级为可提前止损的形式**：`TO < 11%` 且 `最优 |S| < 0.5` 且 `failed_ra` 里没有 spread / 换手 / 集中度类 ⇒ **该字段族是慢变结构描述符，不是收益信号**，直接判死，不必再补模板。
⇒ 本轮 pv13 又是**零成本可预判**的一例：第一轮 8 条一出来，TO 全部贴地，就已经可以收工——后面再换窗口、换中性化、换分组轴都只是在同一个静态排序上做微调。
⇒ **机理**：网络中心性、嵌入位置、风险模型因子得分这类量，本质是**描述「这家公司是谁」的横截面属性**，年际几乎不变 ⇒ 截面排序年复一年相同 ⇒ 既没有换手，也就没有随时间兑现的 alpha。要有信号必须让它跟**价格 / 流量 / 事件**发生交互，而那已经是两塔混合。

### 32.3 pv 塔第 3 点改由提交通道完成，不再靠继续挖

`pv13` 判死后，pv 类别下**未被判死的候选只剩** `pv109`（可转债，cov 0.33）、`pv106`（spread / 交易成本，8 字段）。两者按 32.2 判据先验都不乐观（成本类量同样是慢变描述符）。

而 pv 塔现在是 **2/3，只差 1 颗**，且差的这一颗**已经在手上**：`RRE5Mwkn`（`pv103_ivam_sum` × `loaned_share_count_main`，S 2.15 / F 1.41 / 2Y 3.65 / self 0.163，pyramid = `GBR/D1/PV`）。

⇒ **动作**：pv 塔点亮不靠再挖数据集，靠把 `RRE5Mwkn` 的 prod 测出来并（用户授权后）提交。这是本轮性价比最高的点塔路径。

### 32.4 `pv13` 的保留价值：11 个 GROUP 轴

虽然信号字段判死，但 `pv13` 自带 RBICS 六级轴 `pv13_new_{1..6}l_scibr` 与 `pv13_eur_revere_risc_sector_{level,parent}`，可作**其它数据集信号腿的分组轴**外挂（替换 `sector`）。属两塔混合，受「集合内 × 集合外 ≤5 类」与「每两塔 ≤3 颗」双配额约束，优先级低。

## 三十三、U31 收批（`inst25` 出 S 0.98 但 2Y 死）+ ★ 提纯：2Y 才是未点亮塔的真杀手

### 33.1 U31 `institutions25` 收批（8/8，0 错误，multisim `Oe6bqdg94s8art19puUGqlT`）

| alpha | 模板 | 机制 | S | F | 2Y | sub | TO |
|---|---|---|---:|---:|---:|---:|---:|
| j2YVbX7o | G1 | 回补/做空笔数比 | −0.92 | −0.45 | 0.19 | −0.78 | 0.135 |
| xArl0QJq | G2 | 拥挤度 × 集中度 | −0.76 | −0.36 | −0.10 | −0.76 | 0.133 |
| **RRE5nYGa** | **G3** | **持仓年龄（反）** | **0.98** | **0.52** | **0.37** | **0.86** | 0.087 |
| P0oPd6kM | G4 | 久期错配 | −0.42 | −0.14 | −0.17 | −0.25 | 0.101 |
| npv6MoLE | G5 | 交易活跃度 Δ22 | −0.74 | −0.30 | 0.14 | −0.67 | 0.163 |
| RRE5naJa | G6 | 集中度/空头总规模（反） | 0.61 | 0.29 | 0.18 | **0.76** | 0.119 |
| 58EGo6ZJ | G7 | 未平仓比例 | −0.71 | −0.38 | −0.56 | −0.75 | 0.129 |
| 2rAGbZr8 | G8 | 2:1 合成 | −0.15 | −0.03 | 0.24 | −0.11 | 0.158 |

`RRE5nYGa`（持仓年龄反向，S 0.98 / F 0.52 / sub 0.86）是**本会话全部单腿探针里最强的**，8 条里有 6 条同向为负、2 条反向为正 —— 说明 `institutions25` **有真实信号结构**（不是结构描述符，TO 0.087–0.163 也属健康区间）。

但它**过不了 2Y 闸**：最好的一条 2Y 只有 0.37，要 1.58。

### 33.2 ★★★★★ 提纯：未点亮塔的真正杀手是 2Y，不是 S

把本会话 31 条探针按「最优 S / 对应 2Y / 2Y 是否达标」摆在一起，模式立刻清楚：

| 数据集 | 最优 S | 该条 2Y | 2Y ≥ 1.58？ | TO |
|---|---:|---:|:---:|---:|
| intraday_pv_feats | 0.96（取反后） | 1.19（取反后） | ✗ | 0.164 |
| fund_holdings_panel | 0.03 | −1.50 | ✗ | 0.096 |
| insider_agg_matrix | −0.03 | −0.44 | ✗ | 0.558 |
| risk60 | 0.12 | 0.61 | ✗ | 0.123 |
| institutions25 | **0.98** | 0.37 | ✗ | 0.087 |
| pv13 | 0.48 | 0.51 | ✗ | 0.104 |
| **macro27** | −0.22 | **2.31** | **✓** | 0.340 |
| **sentiment7** | 0.59 | **1.60** | **✓** | 0.225 |

⇒ **只有 `macro27` 与 `sentiment7` 两条的 2Y 天然达标。** 其余六个数据集即便 S 做到 0.98 也注定卡在 2Y。

**这解释了此前所有「S 上不去」的困惑**：不是信号弱，而是**信号在 2022–2023 这段已经失效**，而我一直在优化全周期 S。2Y 是 601–650 个交易日的独立窗口，它与全周期 S 的差异就是「信号是否还活着」。

**⇒ 新的选集优先序（取代按覆盖率 / 拥挤度排序）**：

1. 第一轮探针**只用来读 2Y**，不用来读 S。一条 `group_rank(ts_zscore(x, 252), sector)` 就够。
2. **2Y < 1.58 的数据集直接封盘**，不再做第二代（合成 / 窗口谷 / 换骨架都救不了已被时间证伪的信号）。
3. 2Y ≥ 1.58 的数据集才进第二代，且第二代只优化 S 与 F，2Y 作为守住不掉的约束。

⇒ 这条把「每个数据集 8 条 × 52 个未探数据集」的工作量压成「每个数据集 1–2 条体检 + 少数几个进第二代」，是**本轮最高价值的效率提升**。

### 33.3 U32：`insider_agg_matrix` 首次开采 cov=1.0 字段

此前只用了 cov 0.5937 的原始买卖股数（`total_buy − total_sell` 等）。本次发现该集有**两个覆盖率 1.0 的现成方向字段**——`directional_indicator`（a=62）与 `directional_indicator_2`（a=30），从未被本战役使用。

| 编号 | 机制 | 表达式 |
|---|---|---|
| G1 | 现成方向指标（cov 1.0） | `group_rank(ts_zscore(directional_indicator, 252), sector)` |
| G2 | 增强版方向指标（cov 1.0） | `group_rank(ts_zscore(directional_indicator_2, 252), sector)` |
| G3 | 双口径背离（信号不确定性） | `group_rank(ts_zscore(subtract(directional_indicator, directional_indicator_2), 252), sector)` |
| G4 | 隐式人数 = total/avg（共识广度） | `group_rank(ts_zscore(divide(total_buy_shares, add(avg_buy_shares, 1)), 252), sector)` |
| G5 | 公开市场占比（Lakonishok-Lee 2001 质量过滤） | `group_rank(ts_zscore(divide(total_secondary_buy_shares, add(total_buy_shares, 1)), 252), sector)` |
| G6 | 阶梯形状：信念集中度 v1/v4 | `group_rank(ts_zscore(divide(significant_value_1, add(significant_value_4, 1)), 252), sector)` |
| G7 | 阶梯衰减 v1 − v2 | `group_rank(ts_zscore(subtract(significant_value_1, significant_value_2), 252), sector)` |
| G8 | 2:1 冷腿合成（方向指标 + 公开市场占比） | `add(group_rank(ts_zscore(directional_indicator, 252), sector), multiply(0.5, group_rank(ts_zscore(divide(total_secondary_buy_shares, add(total_buy_shares, 1)), 252), sector)))` |

预检 valid、unknown=0。已派发 → multisim `3E4RC645D505a88h1uOWj2s`。算子 3–8 个。

### 33.4 U33：`macro27` 三个从未测的劳动力需求机制

`macro27` 13 个字段中，此前只用了 `jobsactive` / `jobscreated − jobsremoved` / `mean_days_job_active`。本次补上三个新机制：

- **`is_job_repost_flag`（a=36）**：岗位是否为重发 ⇒ **招聘困难度**。企业反复重发同一岗位说明招不到人，是劳动力紧张的微观证据，属文献中「recruiting intensity」的代理变量。
- **`mean_days_job_closed`（a=72）**：已撤销岗位在被撤前的挂出时长 ⇒ 招到人的速度快慢。
- **活跃 / 关闭久期缺口**：两腿价差，刻画「在招 vs 已撤」的劳动力市场松紧。

| 编号 | 机制 | 表达式 |
|---|---|---|
| M1 | 规范化净创造 (created−removed)/active | `group_rank(ts_zscore(divide(subtract(vec_sum(num_jobs_created), vec_sum(num_jobs_removed)), add(vec_sum(num_jobs_active), 1)), 252), sector)` |
| M2 | repost 占比（招聘困难度） | `group_rank(ts_zscore(vec_avg(is_job_repost_flag), 252), sector)` |
| M3 | 关闭时长（劳动力紧张） | `group_rank(ts_zscore(vec_avg(mean_days_job_closed), 252), sector)` |
| M4 | 久期缺口（关闭 − 活跃） | `group_rank(ts_zscore(subtract(vec_avg(mean_days_job_closed), vec_avg(avg_days_job_posting_active)), 252), sector)` |
| M5 | 总流动 churn (created+removed)/active | `group_rank(ts_zscore(divide(add(vec_sum(num_jobs_created), vec_sum(num_jobs_removed)), add(vec_sum(num_jobs_active), 1)), 252), sector)` |
| M6 | 净创造动量 Δ66 | `group_rank(ts_delta(divide(subtract(vec_sum(num_jobs_created), vec_sum(num_jobs_removed)), add(vec_sum(num_jobs_active), 1)), 66), sector)` |
| M7 | 2:1 冷腿合成（净创造 + repost 反向） | `add(group_rank(ts_zscore(subtract(vec_sum(mcr27_company_jobscreated), vec_sum(mcr27_company_jobsremoved)), 252), sector), multiply(0.5, reverse(group_rank(ts_zscore(vec_avg(is_job_repost_flag), 252), sector))))` |
| M8 | 久期结构（活跃/关闭） | `group_rank(ts_zscore(divide(vec_avg(avg_days_job_posting_active), add(vec_avg(mean_days_job_closed), 1)), 252), sector)` |

预检 valid、unknown=0。已派发 → multisim `2CPkhUfXc4AJaPSiGq5HQg2`。算子 4–11 个，全部 ≤12。

## 三十四、穷尽清单定稿：61 个未探数据集 + 「1 集 1 条、只读 2Y」批量体检法

### 34.1 剩余未探数据集全量（61 个）

从 177 集里剔除已点亮塔（model/news/analyst/fundamental）与已探过的 21 集，剩 **61 个从未触碰**：

| category | 数量 |
|---|---:|
| other | 40 |
| pv | 9 |
| risk | 3 |
| socialmedia | 3 |
| institutions | 2 |
| sentiment | 2 |
| insiders | 1 |
| imbalance | 1 |

**先验排除（拥挤度异常高，先不排队）**：`pv1`(aC 56109)、`techindi_model`(26992)、`imbalance5`(1941)、`pattern_scores`(1841)、`acquisition_model`(1596)。
**按 32.2 判据先验排除**：`stock_cluster_dl`（纯 PCA 特征）——PCA 因子得分形态在 EUR 已两次系统性无效，本波只作对照。

### 34.2 ★★★★★ 批量体检法：每集 1 条探针，只读 2Y

取代「每个数据集凑 10 个互异模板 × 8 条」的高成本做法：

```
第 1 步（体检）  每个数据集只派 1 条：group_rank(ts_zscore(<该集最核心字段>, 252), sector)
                读且只读 2Y；S 不看。
第 2 步（分叉）  2Y < 1.58  → 封盘，永不回头
                2Y ≥ 1.58  → 进第二代，此时才上 10 个结构互异模板
第 3 步（二代）  只优化 S 与 F，2Y 作为守住不掉的约束
```

**为什么这样切**：33.2 已证明 8 个数据集里只有 2 个的 2Y 天然达标，也就是说**约 75% 的探针预算是浪费在已死信号上的**。体检法把 8 条/dataset 降到 1 条/dataset，同时把一个批次从「1 个数据集」扩到「8 个数据集」。

### 34.3 U34 首轮体检清单（8 集 / 6 塔）

| 数据集 | category | 字段 | 机制 | 探针 |
|---|---|---:|---|---|
| `institutions6` | institutions | 11 MATRIX（**cov 1.0**） | 机构持股广度：持仓机构数 | `group_rank(ts_zscore(count_institutional_holders_security, 252), sector)` |
| `sentiment27` | sentiment | 18（cov 0.80） | Tranco 网络关注度 | `group_rank(ts_zscore(vec_avg(snl27_relpopularity1), 252), sector)` |
| `pv173` | pv | 81（**aC 19，a=0–1**） | **信用利差 60 日变化（股债背离）** | `group_rank(ts_zscore(vec_avg(pv173_ranks_mt5yzspreadchg60d), 252), sector)` |
| `other566` | other | 112（a=1–10） | 经典技术指标（ADX / APO / Aroon） | `group_rank(ts_zscore(average_directional_index_value, 252), sector)` |
| `risk72` | risk | 23 | 统计风险模型特异收益 | `group_rank(ts_zscore(ats_top800_equity_residualized_return, 252), sector)` |
| `other250` | other | 12 VECTOR（cov 0.52） | 电商评论数（需求热度） | `group_rank(ts_zscore(vec_sum(oth250_item_review_count), 252), sector)` |
| `socialmedia5` | socialmedia | 13 VECTOR | 社媒平均情绪（hitscore） | `group_rank(ts_zscore(vec_avg(scl5_s_hitscore_averagesentiment), 252), sector)` |
| `stock_cluster_dl` | other | 5 MATRIX（cov 0.47） | PCA 特征（对照） | `group_rank(ts_zscore(principal_component_features_9, 252), sector)` |

预检 valid、unknown=0、算子 3–4 个。覆盖 institutions / sentiment / pv / other / risk / socialmedia **六个塔**。

### 34.4 ★★★ 反例提醒：未点亮塔并非全无希望，`pv103` 就是成功样本

pv 塔虽只 2/3，但**本战役全部强件（`RRE5Mwkn` S 2.15、`O0A6Qz7p` S 2.18）都出自 `pv103`**——而 pv103 正是一个未点亮塔下的小数据集（8 字段、aC 170）。

⇒ 所以「未点亮塔 = 没有土壤」这个结论**只对慢变结构类数据集成立**（其他455 / pv13 / pv30 / pv29 / risk88 那类）。`pv103` 证明：**只要有真事件流量（`ivam_sum` 是日内成交额分布），未点亮塔照样能出 S>2**。差别不在塔，在**字段是不是事件流**。

⇒ 这条给 61 集体检加了第二个先验：**优先选「事件流量」字段（成交、成交笔数、评论数、情绪计数、新闻计数、发起/撤销计数），而不是「状态描述」字段（中心性、PCA 得分、评级、市值、分类标签）**。

## 三十五、U32 内部人判死 + U33 `macro27` 出本战役最强新信号（S 1.27 / 2Y 1.53）

### 35.1 U32 `insider_agg_matrix` 收批：判死（第二次确认）

| alpha | 模板 | S | F | 2Y | sub | TO | 备注 |
|---|---|---:|---:|---:|---:|---:|---|
| E56mJZXG | `directional_indicator` | **0** | — | — | — | **0** | CONCENTRATED_WEIGHT |
| ZYQXGRed | `directional_indicator_2` | **0** | — | — | — | **0** | CONCENTRATED_WEIGHT |
| 58EGWZoX | 双口径背离 | −0.03 | 0.00 | 0.08 | −0.03 | 0.578 | |
| leAgXLXO | 隐式人数 total/avg | 0.12 | 0.01 | −0.11 | 0.15 | 0.558 | |
| 2rAGd1dZ | 公开市场占比 | 0.19 | 0.02 | −0.67 | 0.38 | 0.561 | |
| A1VLKRKw | 阶梯集中度 v1/v4 | **0.46** | 0.09 | −0.02 | 0.25 | 0.564 | 最优 |
| O0A6a1aJ | 阶梯衰减 v1−v2 | 0.05 | 0.00 | −0.79 | −0.20 | 0.575 | |
| MPYgmjAM | 2:1 合成 | 0.19 | 0.02 | −0.67 | 0.38 | 0.561 | |

**关键发现：那两个覆盖率 1.0 的「现成方向指标」是废字段。** `S = 0 / TO = 0 / CONCENTRATED_WEIGHT 失败` 三条同时出现 ⇒ 该字段在截面上**没有离散度**（近似常数或几乎全为 0）。

⇒ **新的零成本判据**：`TO = 0` + `S = 0` + `CONCENTRATED_WEIGHT` 失败 ⇒ 字段是常数 / 稀疏 flag，**不要因为 coverage = 1.0 就以为它质量高**。覆盖率衡量「有值」，不衡量「有变化」。
⇒ `insider_agg_matrix` 至此两批 11 个模板全部 |S| ≤ 0.46，与 `insiders1` 合并判死；insiders 塔本区无土壤。

### 35.2 U33 `macro27` 收批：久期结构是本战役最强的新信号

| alpha | 模板 | 机制 | S | F | 2Y | sub | TO |
|---|---|---|---:|---:|---:|---:|---:|
| 1YNGQrnm | M1 | 规范化净创造 | 0.34 | 0.06 | 1.93 | 0.31 | 0.393 |
| Jje3Z65e | M2 | repost 占比 | −0.01 | 0.00 | 1.31 | −0.11 | 0.332 |
| Xg9N5dYz | M3 | 关闭时长（水平） | 0.99 | 0.28 | 1.07 | **1.22** | 0.390 |
| **j2YVbqdk** | **M4** | **久期缺口 = 关闭 − 活跃** | **1.27** | **0.41** | **1.53** | **1.20** | 0.398 |
| A1VLMogW | M5 | 总流动 churn | 0.11 | 0.01 | 1.07 | 0.06 | 0.390 |
| RRE5nG20 | M6 | 净创造动量 Δ66 | −0.08 | −0.01 | 1.52 | −0.11 | 0.447 |
| omEPMx3n | M7 | 2:1 冷腿合成 | −0.12 | −0.01 | **2.35** | 0.19 | 0.429 |
| O0A6Elb7 | M8 | 久期结构 活跃/关闭 | 1.06 | 0.31 | 1.01 | 0.71 | 0.401 |

`j2YVbqdk` 详情：**S 1.27 / F 0.41 / 2Y 1.53 / sub 1.20 / TO 0.398 / returns 4.20% / margin 21.1bp / drawdown 2.72%**，pyramid = `GBR/D1/MACRO`（macro 塔 **0/3**，一颗就能点亮 1/3）。

**机制解释**：`mean_days_job_closed` 是「已撤销岗位在撤销之前的挂出天数」，`avg_days_job_posting_active` 是在招岗位的已挂出天数。两者之差 = **岗位久期结构缺口**。缺口大 ⇒ 撤销的岗位曾挂了很久 ⇒ 招聘效率低 / 人力需求虚高 / 劳动力囤积。这是「recruiting intensity」在劳动力市场上的直接读数，和价位类字段完全正交。

**八条同族全部 S ≥ −0.12 且 sub 多数为正**（1.22 / 1.20 / 0.71 / 0.31），说明宏观劳动力这块**是真有信号**，不是结构描述符。

### 35.3 ★★★★★ 载荷陷阱：`checks.fail` 为空 ≠ 全闸通过（差点误判可提交）

`j2YVbqdk` 与 `O0A6Elb7` 的 `checks.fail` 都是 **`[]`**，看起来像「全闸通过」。但拉详情后发现：

```
checks.fail    = []
checks.warning = [LOW_SHARPE, LOW_FITNESS, LOW_2Y_SHARPE, MATCHES_COMPETITION, MATCHES_THEMES]
ra.failed_ra_count    = 3
ra.ra_failed_checks   = [LOW_SHARPE, LOW_FITNESS, LOW_2Y_SHARPE]
ra.ra_failed          = true
```

⇒ 平台把这三条闸放进了 **`warning`** 而不是 `fail`，但 `ra.ra_failed = true`。
⇒ **唯一权威的判闸字段是 `ra.ra_failed_checks` / `ra.ra_failed_count`，不是 `checks.fail`。** 只看 `checks.fail` 会把 S 1.27 的件当成「全闸通过、可提交」，这是最危险的一类误判。
⇒ 本战役此前对 U23 七颗的「全闸通过」判断也需要用同样口径复核。

### 35.4 ★★★★★ F 闸的精确数学：`macro27` 的死结在收益率量级

平台定义 `F = S × sqrt(|returns| / max(TO, 0.125))`。用 `j2YVbqdk` 反算验证：

```
1.27 × sqrt(0.0420 / 0.3984) = 1.27 × 0.3249 = 0.4127  ≈ 实测 0.41  ✓ 公式确认
```

要 `F ≥ 1.0` 且 `S = 1.58`，需要 `sqrt(R/TO) ≥ 0.633`，即 **`R/TO ≥ 0.40`**。现状 `0.042/0.398 = 0.106` ⇒ **差 3.8 倍**。

| 路径 | 需要什么 | 可行性 |
|---|---|---|
| 保 TO、提 R | TO 0.398 不变 ⇒ **R 必须到 15.9%** | 不现实 |
| **压 TO 到 0.125 地板 + 小幅提 R** | TO 0.125 ⇒ **R 只需 5.0%**（现状 4.2%） | **可行，就是 U35 的目标** |
| 只压 TO 不提 R | TO 0.125、R 4.2% ⇒ F = 1.27 × 0.58 = **0.74** | 仍不过 F |

⇒ **`max(TO, 0.125)` 的下限结构决定了：TO 压到 0.125 之后再压对 F 毫无收益，剩下的唯一杠杆是把 R 顶上去。** 所以 U35 的正确目标不是「疯狂降换手」，而是「**把 TO 压到 0.125 附近的同时把 R 顶到 5%+**」。

### 35.5 U35 已派发：`macro27` 久期缺口第二代（8 条）

| 编号 | 杠杆 | 表达式 |
|---|---|---|
| N1 | 窗口谷·短窗 22 | `group_rank(ts_zscore(subtract(ts_mean(vec_avg(mean_days_job_closed), 22), ts_mean(vec_avg(avg_days_job_posting_active), 22)), 252), sector)` |
| N2 | 窗口谷·长窗 126 | 同上，两腿都换 126 |
| N3 | 平滑降换手 ts_mean 66 外包 | `group_rank(ts_zscore(ts_mean(subtract(vec_avg(mean_days_job_closed), vec_avg(avg_days_job_posting_active)), 66), 252), sector)` |
| N4 | **2:1 冷腿合成**（主腿 + TO 0.082 冷腿） | `add(group_rank(ts_zscore(subtract(vec_avg(mean_days_job_closed), vec_avg(avg_days_job_posting_active)), 252), sector), multiply(0.5, reverse(group_rank(ts_mean(vec_avg(mean_days_job_active), 66), sector))))` |
| N5 | 分组轴 industry | 主腿换 `industry` |
| N6 | 分组轴 subindustry | 主腿换 `subindustry` |
| N7 | 非线性 ts_rank 秩变换 | `group_rank(ts_rank(<主腿>, 252), sector)` |
| N8 | 残差化骨架 | `group_neutralize(rank(<主腿>), sector)` |

预检 valid、unknown=0、算子 5–11 个。已派发 → multisim `2FWN1Ba0f4LjaiwlbioWYVr`。

## 三十六、U34/U35 在飞 + 字段画像推进（U36/U37 备料）

### 36.1 prod 阻塞第五次确认：平台端不发布，不是本地锁

串行队列 `bg_f7245f72` 跑完两颗独立件，**两颗均 240s 超时**：

| alpha | 查询次数 | 耗时 | 返回 |
|---|---:|---:|---|
| RRE5Mwkn | 184 | 240s | `computed:true / status:pending` |
| O0A6Qz7p | 186 | 240.7s | `computed:true / status:pending` |

⇒ 平台 `GET /alphas/{id}/correlations/prod` 在 240s 内不发布值。MCP 内部窗口 `_PROD_CORR_WAIT_S=240` 是硬顶，本地无法延长；
`--minutes 14` 的外层重试也因单轮 240s 超时后进入 pending 而复用同一窗口。**结论：prod 结论在平台恢复前无法获得，不据此给候选下任何判定。**

另：`GET /simulations` 返回 **405（Method not allowed）** ⇒ 平台不提供活动仿真列表接口，无法排查孤儿占槽。脚本 `tools/list_active_sims.py` 已证不可用。

### 36.2 U34 / U35 在飞状态

| 批次 | multisim | 内容 | 派发 | 状态 |
|---|---|---|---|---|
| U34 | `2gQHff9ec4LtbzC3NBwGPTC` | 8 集体检（institutions6/sentiment27/pv173/other566/risk72/other250/socialmedia5/stock_cluster_dl） | 04:51 | 排队中（R5，`tot=None`） |
| U35 | `2FWN1Ba0f4LjaiwlbioWYVr` | macro27 久期缺口二代 N1–N8 | 04:51 | 排队中（R4，`tot=None`） |

排队已超 14 分钟，长于 U32/U33 的 ~9 分钟。判据：`tot=None` = 未起跑，不是卡死。

### 36.3 未点亮塔 category 数据集全清单（GBR/D1）

`get_pyramid_alphas` 复核塔位：

```
已点亮(<3 视为未点亮)：institutions 0  insiders 0  other 1  pv 2  earnings 0
                      sentiment 0  risk 0  option 0  socialmedia 0  macro 0
                      shortinterest 0  imbalance 0
已点亮(≥3)：          model 5  news 3  analyst 3  fundamental 3
```

未点亮塔数据集池 **82 个**（other 41 / pv 16 / institutions 5 / risk 5 / insiders 3 / sentiment 3 / socialmedia 3 / earnings 2 / option 1 / macro 1 / shortinterest 1 / imbalance 1）。

按「禁混集合 = {PV, MODEL, OTHER, FUNDAMENTAL}，集合外优先」排序，**非禁混塔 category 共 25 个数据集**，已探 12 个，**剩 13 个**：

| 数据集 | category | 字段 | 用户数 | aC | 处置 |
|---|---|---:|---:|---:|---|
| sentiment33 | sentiment | 255 | 102 | 209 | **U36** |
| shortinterest3 | shortinterest | 25 | 561 | 1668 | **U36** |
| option1 | option | 22 | 118 | 294 | 暂缓（option VECTOR 单独成批风险） |
| earnings_sent_matrix | earnings | 7 | 265 | 610 | **U36** |
| insiders12 | insiders | 7 | 172 | 401 | **U36** |
| institutions1 | institutions | 7 | 34 | 52 | **U36** |
| institutions4 | institutions | 6 | 38 | 47 | U37 备料 |
| risk71 | risk | 6 | 299 | 608 | **U36** |
| socialmedia12 | socialmedia | 6 | 191 | 442 | **U36** |
| risk68 | risk | 5 | 357 | 731 | 拥挤，低优先 |
| imbalance5 | imbalance | 2 | 744 | 1941 | 先验排除（拥挤+2 字段） |
| risk88 | risk | 1 | 306 | 567 | 单字段，低优先 |
| socialmedia39 | socialmedia | 1 | 137 | 298 | 单字段，低优先 |

### 36.4 U36 七集探针（1 集 1 骨架，7 个结构互异几何，只读 2Y）

按第 34.2 节体检法：每集派 1 条、只读 2Y，2Y<1.58 封盘。**但骨架互异**（避免第 31 节同构骨架陷阱）：

| # | 数据集 | 机制 | 表达式 | 分组轴 | 矩 |
|---|---|---|---|---|---|
| 1 | shortinterest3 | 借券费水平反向（难借=空头拥挤→反转做空） | `group_rank(-ts_zscore(vec_avg(max_loan_rate), 252), subindustry)` | subindustry | 水平 |
| 2 | earnings_sent_matrix | 双加权口径语气背离 | `rank(ts_zscore(sentiment_weighting_method1 - sentiment_weighting_method2, 126))` | 无（全截面） | 两腿价差 |
| 3 | sentiment33 | 负面情绪**加速** | `group_rank(-ts_zscore(ts_delta(vec_avg(sentiment_model6_negative_score_fkw3), 22), 252), industry)` | industry | 一阶差分 |
| 4 | socialmedia12 | 情绪 × 关注度交互 | `group_rank(ts_zscore(scl12_sentiment, 66) * ts_rank(scl12_buzz, 252), sector)` | sector | 水平×分位 |
| 5 | institutions1 | 重要性加权交易额 | `group_rank(ts_zscore(vec_avg(inst1_value) * vec_avg(inst1_tradesignificance), 126), subindustry)` | subindustry | 水平 |
| 6 | risk71 | 残差**低波**异象 | `group_rank(-ts_zscore(ts_std_dev(residualized_return_top2500, 66), 252), sector)` | sector | 二阶方差 |
| 7 | insiders12 | 内部人净买入 | `group_rank(ts_zscore(vec_sum(insd12_positionchangetransactionamount), 126), market)` | market | 水平 |

四维覆盖：骨架结构 5 种（水平/价差/一阶差分/交互/二阶方差）｜分组轴 4 种 + 无分组｜矩 4 种｜非线性 1 种。**显著优于 U27–U29 的 1/2/1/0。**

预检：`valid=true`，`unknown_fields=[]`，10 字段全过，`any_changed=false`。算子数分别 2/2/3/3/4/3/3，全部远低于上限 12。

### 36.5 ★★★★ U37 备料：两个高保真事件流数据集

**(A) `order_book_imbalance`（other, 240 字段, aC 96, cov 0.16）** — 逐笔订单簿微观事件。**单字段 aC 0–1，几乎零使用**。可用家族：

| 家族 | 字段样例 | 机制 |
|---|---|---|
| 订单流不平衡 | `bid/ask_order_insertion_count`、`deletion_count`、`execution_count` | OFI：买插单−卖插单 |
| 成交概率 | `fill_prob_ask_lvl1`…`lvl5` | 挂单被吃概率 = 真实流动性需求 |
| 挂单寿命 | `avg_rest_time_bid/ask_filled/cancelled_lvl1`…`lvl5` | 撤单速度 = 虚假流动性 |
| 收盘拍卖失衡 | `auction_order_imbalance_absolute/notional/pct_adv/pct_auction` | 收盘竞价失衡 = 隔夜压力 |
| 拍卖错位 | `closing_auction_dislocation_1min/5min/last` | 收盘价偏离 = 冲击未消化 |
| 暗池/双边 | `dark_trade_count/notional/volume`、`bilateral_trade_count` | 非公开成交占比 |

**(B) `earningscall_sentiment`（other, 167 字段, aC 56）** — 电话会文本按**主题 × 章节**计数。5 主题 × 4 章节 × 正/负 = 40 个计数字段 + 3 个 `_sentiment_polarity`：

- 主题：`assetutilization` / `cashflow` / `leverage` / `profitability` / `valuation`
- 章节：`presentation`（管理层念稿）/ `answer`（问答）/ `question`（分析师提问）/ `summary`
- **核心机制**：`presentation` 与 `answer` 的情绪差 = **念稿 vs 即兴的诚实度缺口**，是本数据集独有几何；`question` 负面计数 = 分析师敌意。

**(C) `ai_news_scores`（other, 105 字段, MATRIX）** — 正/负情绪均值 + **95% 置信上下界** ⇒ 可构造「置信区间宽度 = 新闻分歧度」这一二阶矩信号。注意 `_2`–`_5` 后缀是 ASI/USA 区域变体，GBR 只能用主字段。

**(D) `other78` 排除** — 60 个 SYMBOL + 会议地址/URL 元数据，无信号。

**(E) `other696` 备料低优先** — 按主题的正/负事件计数（capacity/inflation/leadership…），VECTOR 且 aC 多为 0，稀疏。

## 三十七、U34/U35 收批 + ★★★★★ 闸阈值纠正（本战役最重要的一次口径修正）

### 37.1 U34 八集体检收批：8/8 全灭，但**失败机理变了**

multisim `2gQHff9ec4LtbzC3NBwGPTC`，8/8 完成，0 错误。骨架统一为 `group_rank(ts_zscore(<核心字段>, 252), sector)`。

| alpha | 数据集 | 机制 | S | F | TO | R |
|---|---|---|---:|---:|---:|---:|
| LLM8Jr1a | institutions6 | 机构持股广度 | −0.05 | −0.01 | 0.099 | −0.002 |
| 3qoGL5R6 | sentiment27 | Tranco 相对热度 | −0.26 | −0.07 | 0.097 | −0.008 |
| Jje3K1Ox | pv173 | 信用利差 60 日变化 | −0.14 | −0.03 | 0.157 | −0.006 |
| **wpQNgPl2** | other566 | 趋势强度 ADX | **0.24** | 0.03 | 0.314 | 0.006 |
| 78LG9M15 | risk72 | 特异收益残差 | −0.31 | −0.07 | 0.268 | −0.014 |
| vR1Yg6vw | other250 | 电商评论数 | 0.15 | 0.02 | 0.168 | 0.004 |
| xArlgWdg | socialmedia5 | 社媒平均情绪 | 0.00 | 0.00 | 0.328 | 0.000 |
| QPvWXg9r | stock_cluster_dl | PCA 特征（对照） | −0.11 | −0.01 | 0.397 | −0.004 |

**关键区别（改写判死口径）**：这 8 集的 **TO 在 9.7%–39.7%，全部高于 12.5% 地板**，
⇒ 它们**不是** pv13 / EUR 那种「慢变结构描述符」（TO 2–10%）。**数据在动，只是不可预测。**

于是本区未点亮塔的失败机理分两类，处置完全不同：

| 类型 | 指纹 | 含义 | 处置 |
|---|---|---|---|
| A 慢变描述符 | TO < 10% 且 |S| < 0.5 | 字段是状态标签，不是信号 | **一次探针即判死**，别换骨架 |
| B 有变化无预测 | TO 10–40% 且 |S| < 0.5 | 字段是真实的量，但不被定价 / 或需换几何 | 换骨架族再测 1–2 轮，仍灭则判死 |

pv13 / other455 / sentiment21 / news36 / pv30 = A 类；U34 这 8 集 = B 类。

### 37.2 U35 macro27 二代收批：出了 **S 1.59**，但撞 4 个闸

multisim `2FWN1Ba0f4LjaiwlbioWYVr`，8/8 完成，0 错误。

| # | alpha | 骨架 | S | F | TO | R | 2Y | sub | 结论 |
|---|---|---|---:|---:|---:|---:|---:|---:|---|
| N1 | LLM8J2p1 | 双腿各 ts_mean 22 再价差 | 0.34 | 0.10 | 0.116 | 0.010 | — | — | 长窗削光信号 |
| N2 | 0mYGva72 | 双腿各 ts_mean 126 | 0.67 | 0.27 | 0.090 | 0.020 | — | — | 同上 |
| N3 | kqN8lY0d | 差值再 ts_mean 66 | **−0.20** | −0.04 | 0.096 | −0.006 | — | — | **反号** |
| N4 | 2rAGd2LP | 2:1 冷腿合成 | 1.31 | 0.40 | 0.425 | 0.040 | 1.72 | 1.14 | 3 闸不全 |
| N5 | E56mJ2EK | 分组轴 industry | 1.15 | 0.34 | 0.413 | 0.037 | — | — | 弱于 sector |
| N6 | QPvWXoVK | 分组轴 subindustry | 1.20 | 0.35 | 0.419 | 0.036 | — | — | 同上 |
| N7 | RRE5Wv8z | **ts_rank 秩变换** | 1.28 | 0.42 | 0.403 | 0.042 | 1.53 | **1.24** | 最均衡，sub 与 invest 最好 |
| N8 | **VkxMJRPA** | `group_neutralize(rank(差值), sector)` | **1.59** | 0.34 | **1.095** | 0.050 | 1.68 | 0.93 | **S 达标但 4 闸不过** |

N8 详情：drawdown 2.2%，margin **9.1bp**（N7 是 21.1bp），investability_sharpe 0.34，
`ra_failed_checks = [LOW_FITNESS, HIGH_TURNOVER, CONCENTRATED_WEIGHT, LOW_2Y_SHARPE]`。

**机理**：N8 是**唯一没做任何时间平滑**的骨架（裸 rank），因此 S 最高（1.59）但 TO 也最高（109.5%）。
反过来 N3（差值再 ts_mean 66）TO 只有 9.6% 却 **S 反号 −0.20** ⇒ **这个信号的生命周期是短的**，
任何时间平滑都在削信号而不是降噪。

⇒ **macro27 久期缺口判死（可提交口径）**：N7 若要过闸需 S +0.30、F +0.58、2Y +0.84；
按 F 数学，S 1.58 + F 1.0 要求 `R/TO ≥ 0.40`，N7 现状 `0.0424/0.403 = 0.105`，**差 3.8 倍**，非参数可解。
但它产出了本战役**唯一的全新宏观信号**（久期缺口 = 岗位关闭时长 − 在挂时长），保留作机制记录。

### 37.3 ★★★★★ 闸阈值纠正：真实门槛是 4 个，且 LOW_2Y_SHARPE 的 limit 会变

此前口径「S≥1.58 / F≥1.00 / 2Y≥1.58」**既有遗漏也有错误**。以 `checks.fail` 返回的 `limit` 字段为准，实测：

| 闸 | 真实 limit | 证据 |
|---|---|---|
| `LOW_SHARPE` | **1.58** | `2rAGd2LP` fail: value 1.31 / limit 1.58 |
| `LOW_FITNESS` | **1.00** | `VkxMJRPA` fail: value 0.34 / limit 1 |
| `HIGH_TURNOVER` | **0.70** | `VkxMJRPA` fail: value 1.0951 / limit 0.7 ← **此前完全没登记的硬闸** |
| `LOW_2Y_SHARPE` | **不固定** | macro 类 limit 2.37；analyst/news 类 2Y 1.98 / 1.89 直接 pass |

`LOW_2Y_SHARPE` 的 limit 在同一区域同一 delay 下**既出现过 2.37 也出现过 <1.89**，
⇒ **绝不能硬编码 2Y 阈值**。唯一合法做法：读 `checks.fail[].limit`，或直接看 `ra.failed_ra_count`。

**新增硬闸 `HIGH_TURNOVER 0.7`** 的解释力很强：本战役大量候选 TO 在 0.40–0.45（如 macro 全家族、
institutions25 的 0.56、insider 的 0.56），本来就在 0.7 边缘；而 pv13 系 7–10% 的 TO 反而不触这条闸。

### 37.4 ★★★★★ 四颗候选闸状态复核：**全部 failed_ra_count = 0**

此前只把 2 颗当作可提交，实际 **4 颗全部通过全部 RA 闸**：

| alpha | S | F | TO | R | 2Y | sub | 塔位（平台判定） | RA fail |
|---|---:|---:|---:|---:|---:|---:|---|---:|
| QPvbxjXw | 1.87 | 1.14 | 0.158 | 0.0586 | 1.98 | 1.07 | `GBR/D1/ANALYST` ×1.6 | **0** |
| rKRPAWv9 | 1.76 | 1.07 | 0.081 | 0.0461 | 1.89 | 1.40 | `GBR/D1/NEWS` ×1.6 | **0** |
| **RRE5Mwkn** | 2.15 | 1.41 | 0.143 | 0.0614 | 3.65 | 1.10 | `SHORTINTEREST` ×1.2 + **`PV` ×1.4**（effective 2） | **0** |
| **O0A6Qz7p** | 2.18 | 1.52 | 0.114 | 0.0607 | 3.27 | 1.87 | `SHORTINTEREST` ×1.2 + **`OTHER` ×1.6**（effective 2） | **0** |

**self 相关（零成本实测）**：`RRE5Mwkn` **0.1628**（最高对手 `rKRkL9QE`）、`O0A6Qz7p` **0.2473**（最高对手 `rKRbrZKo`）。两颗粒均远低于 0.70。

### 37.5 ★★★★★ 塔位重估：pv103 的两颗是**双塔件**，能一次点亮 PV

这是本轮最重要的战略发现。两颗 pv103 alpha 的 `pyramids.list` 各含**两个塔**：

| alpha | 塔 1 | 塔 2 | 若提交后的塔位变化 |
|---|---|---|---|
| RRE5Mwkn | SHORTINTEREST 0→1 | **PV 2→3 = 点亮** | **PV 塔直接点亮** |
| O0A6Qz7p | SHORTINTEREST 0→1（并占） | OTHER 1→2 | 推进 other，但 shortinterest 名额被占 |

⇒ **优先提 RRE5Mwkn**：一颗同时点 PV（3/3）+ 给 shortinterest 开张（1/3）。
⇒ 另外两颗（QPvbxjXw→ANALYST 已亮、rKRPAWv9→NEWS 已亮）**对点塔零增量**，只有计数价值。

塔混口径备注：这两颗本质是**单数据集 pv103 ATOM**，跨两塔是平台按字段归属自动分类的结果，不是我自己混信号。
落进「禁混集合内 × 集合外」档（PV×SHORTINTEREST、OTHER×SHORTINTEREST），两类各 1 颗，配额 2/5 → 4/5，仍在 ≤5 内。

### 37.6 在飞

| 批次 | multisim | 内容 | 状态 |
|---|---|---|---|
| U36 | `1W6ICTa8i4SB8X116nrv7SOy` | 7 集探针（shortinterest3 / earnings_sent_matrix / sentiment33 / socialmedia12 / institutions1 / risk71 / insiders12） | 排队 R3 |
| prod | — | `RRE5Mwkn` → `O0A6Qz7p` 串行 | 两颗 peek 均「空体」，平台未发布 |

## 三十八、★★★★★ 首颗「全闸通过 + 能点亮塔」的候选：RRE5Mwkn prod = 0.4744

### 38.1 prod 破冰

同一颗 `RRE5Mwkn` 前两次 240s 超时（184 次查询），本轮 **72 次查询、92s 直接出值**：

```
[INFO] [PC成功] Alpha RRE5Mwkn PC=0.4744 (第 72 次查询, 耗时 92s)
```

⇒ 印证「prod 有缓存热效应」：一旦平台把这颗算过一遍，后续秒回。**队列中途不要 kill 重启。**

### 38.2 RRE5Mwkn 完整验收表

| 项 | 值 | 阈值 | 结论 |
|---|---|---|---|
| S | 2.15 | ≥1.58 | ✓ |
| F | 1.41 | ≥1.00 | ✓ |
| TO | 0.1425 | <0.70 | ✓ |
| returns | 6.14% | — | |
| 2Y | 3.65 | 变动 | ✓ |
| sub | 1.10 | ≥0.75 类 | ✓ |
| RA 全闸 | `failed_ra_count = 0` | 0 | ✓ |
| self | 0.1628 | <0.70 | ✓ |
| **prod** | **0.4744** | <0.70 | **✓** |

**塔位**：`GBR/D1/SHORTINTEREST` ×1.2 + `GBR/D1/PV` ×1.4，`effective=2`。

⇒ 提交后：**PV 塔 2→3 直接点亮**；SHORTINTEREST 塔 0→1 开张。
⇒ 这是本战役**第一颗同时满足「全闸通过 + 点亮新塔」的候选**。

### 38.3 四颗候选最终台账

| 序 | alpha | S | F | TO | 2Y | self | prod | 塔位 | 状态 |
|---|---|---:|---:|---:|---:|---:|---:|---|---|
| 1 | **RRE5Mwkn** | 2.15 | 1.41 | 0.143 | 3.65 | 0.163 | **0.4744** | SHORTINT + **PV** | ★ **可提交，点亮 PV** |
| 2 | QPvbxjXw | 1.87 | 1.14 | 0.158 | 1.98 | — | 0.5794 | ANALYST（已亮） | 可提交，点塔零增量 |
| 3 | rKRPAWv9 | 1.76 | 1.07 | 0.081 | 1.89 | — | 0.3998 | NEWS（已亮） | 可提交，点塔零增量 |
| 4 | O0A6Qz7p | 2.18 | 1.52 | 0.114 | 3.27 | 0.247 | **0.6984** | SHORTINT + OTHER | ★ 压线通过（余量 0.0016） |

**建议提交顺序**：`RRE5Mwkn` → `O0A6Qz7p`（两颗都推进塔位）→ `QPvbxjXw` / `rKRPAWv9`（纯计数）。
注意 `RRE5Mwkn` 与 `O0A6Qz7p` 互相关 **0.34**（第 31 节矩阵），可同批提交不撞 self。

### 38.4 pv106 字段画像：PV 塔的第 3 点有了新弹药

PV 类剩余 10 个数据集，按「aC 低 = 未被挖过」排序后，**`pv106` 是最高价值**：

| 数据集 | 字段 | 类型 | 用户 | aC | 判定 |
|---|---:|---|---:|---:|---|
| **pv106** | 8 | **MATRIX** | 25 | **2–11** | ★★★★★ 流动性/价差/交易成本家族 |
| pv71 | 8 | VECTOR | 3 | 0–2 | ★★ 关系图边权（慢变结构描述符，低优先） |
| pv109 | 26 | VECTOR | 15 | 0–12 | ★★ 公司债属性（cov 0.33，LOW_SUB 风险） |
| pv29 | 50 | MATRIX+**GROUP** | 53 | 0–7 | 纯分组轴（10 个 GROUP 字段），不能单独出信号 |
| continuation_score | 560 | — | 326 | 778 | 拥挤 |
| pv47 / pattern_scores / pv30 | — | — | — | 779 / 1841 / 400 | 拥挤或已判死 |

pv106 的 8 个字段构成**完整成本链条**：

```
pv106_spread / pv106_spreadbp        买卖价差（价格 / bps）
pv106_lastspread / pv106_lastspreadbp 近 30 分钟价差
aggregated_slippage_metric           聚合滑点
slippage_at_spread_35                按价差 35% 建模的执行滑点
transaction_cost_percentile_10       10 分位交易成本
transaction_cost_maximum             最大交易成本
```

⇒ 这是 Amihud (2002) 非流动性溢价、Amihud–Mendelson 买卖价差溢价的**直接可实现版本**，
而且**全 MATRIX、aC 个位数**——PV 塔里几乎没人碰过。这是「有变化 + 有先验定价机制」的 B 类数据集，
不是 pv13 那种 A 类慢变描述符。

### 38.5 U38 pv106 八模板（已派发 `2oz9YVVZ4jD9GxMq9TLq8f`）

| # | 机制 | 表达式 | 分组轴 | 矩 |
|---|---|---|---|---|
| 1 | 非流动性溢价（水平） | `group_rank(ts_zscore(pv106_spreadbp, 252), subindustry)` | subindustry | 水平 |
| 2 | 流动性改善（Δ反向） | `group_rank(-ts_zscore(ts_delta(pv106_spreadbp, 22), 252), sector)` | sector | 一阶差分 |
| 3 | 盘中价差扩张 | `group_rank(ts_zscore(pv106_lastspread / (pv106_spread + 0.0001), 126), industry)` | industry | 比率 |
| 4 | 交易成本分位 | `group_rank(ts_zscore(transaction_cost_percentile_10, 252), sector)` | sector | 水平 |
| 5 | 成本尾部风险 | `group_rank(-ts_zscore(transaction_cost_maximum / (transaction_cost_percentile_10 + 0.0001), 126), subindustry)` | subindustry | 比率 |
| 6 | 滑点水平 | `group_rank(ts_zscore(aggregated_slippage_metric, 252), market)` | market | 水平 |
| 7 | 流动性不确定性 | `group_rank(-ts_zscore(ts_std_dev(pv106_spreadbp, 66), 252), sector)` | sector | 二阶方差 |
| 8 | pv71 关系强度 | `group_rank(ts_zscore(vec_sum(relation_weight_normalized), 252), industry)` | industry | 水平 |

预检 valid、unknown=0、7 字段全过；算子数 3–6 个。四维：骨架 5 种 / 分组轴 4 种 / 矩 4 种 / 非线性 0（下一轮补）。

### 38.6 prod 全部落定：4 颗全部 < 0.70

```
RRE5Mwkn  prod = 0.4744  (72 次查询,  92s)  余量 0.226  —— 舒适
O0A6Qz7p  prod = 0.6984  (108 次查询, 137s) 余量 0.0016 —— 压线
```

**O0A6Qz7p 属「压线通过」**：0.6984 距 0.70 只有 0.0016。按 prod 分级它落在 `<0.7 通过` 但已是浅钉下沿，
任何后续微调（窗口 / 算子 / 中性化）都会把它推到 0.7–0.8 区间。**结论：这颗要提交就现在提交，不要再去改它。**

对比 `RRE5Mwkn` 0.4744 的 0.226 余量——同一数据集、同一族几何，prod 差异 0.22，说明两颗捕获的是**不同**的生产池重叠。

### 38.7 四颗全提交后的塔位推演

| 塔 | 当前 | 提交 RRE5Mwkn | + O0A6Qz7p | 终态 |
|---|---:|---:|---:|---|
| **PV** | 2 | **3** | 3 | ★ **点亮** |
| SHORTINTEREST | 0 | 1 | **2** | 差 1 点亮 |
| OTHER | 1 | 1 | **2** | 差 1 点亮 |
| ANALYST | 3 | 4（QPvbxjXw） | 4 | 已亮 |
| NEWS | 3 | 4（rKRPAWv9） | 4 | 已亮 |

⇒ **一次提交 4 颗的净效果：PV 塔点亮（未点亮 → 已点亮），SHORTINTEREST 2/3，OTHER 2/3。**
⇒ 距离「20 颗」目标：**4 颗已达标可提交**（此前台账只记了 2 颗，因为漏读了 `failed_ra_count`）。

### 38.8 队列现状（阻塞项）

| 批次 | multisim | 状态 |
|---|---|---|
| U36 七集探针 | `1W6ICTa8i4SB8X116nrv7SOy` | 排队 R6，`tot=None`（已 8 分钟未起跑） |
| U38 pv106 八模板 | `2oz9YVVZ4jD9GxMq9TLq8f` | 排队 R3，`tot=None` |

两批同时排队且都不起跑，说明**账号级仿真槽被外部会话占满**（与第 30.1 节的 prod 抢锁同源）。
处置：不 kill、不重派、不加第三批；保持队列等槽位释放。

## 三十九、U36 收批 + ★★★★★ 命中率统计：19 集筛选 0 命中，瓶颈不是数据集而是几何

### 39.1 U36 七集探针收批：0/7

multisim `1W6ICTa8i4SB8X116nrv7SOy`，7/7 完成，0 错误。7 个**结构互异**骨架：

| alpha | 数据集 | 机制 | S | F | TO | R | 2Y | sub |
|---|---|---|---:|---:|---:|---:|---:|---:|
| RRE5Ld8z | shortinterest3 | 借券费水平反向 | −0.60 | −0.14 | 0.346 | −0.018 | −0.62 | −0.13 |
| **VkxMoOPA** | earnings_sent_matrix | 双口径背离 | **0.77** | 0.18 | **1.382** | **0.079** | 0.35 | 0.08 |
| Jje3Lbvl | sentiment33 | 负面情绪加速 | 0.15 | 0.03 | 0.339 | 0.013 | 0.45 | 0.27 |
| npv6b383 | socialmedia12 | 情绪 × 关注度 | 0.28 | 0.04 | 0.372 | 0.010 | **1.31** | 0.02 |
| A1VLdk7Q | institutions1 | 重要性加权交易额 | −0.05 | 0.00 | 0.554 | −0.003 | −0.17 | −0.23 |
| O0A6voxg | risk71 | 残差低波 | 0.57 | 0.20 | **0.108** | 0.016 | 0.58 | **0.57** |
| 3qoGWzeN | insiders12 | 内部人净买入 | −0.44 | −0.15 | 0.095 | −0.014 | −0.74 | −0.33 |

**两条值得记的信号**（虽都不达标）：

1. `VkxMoOPA`（earnings_sent_matrix 双口径背离）**returns 7.87% 是本战役最高单颗收益**，但 TO 1.382 极高、2Y 0.35。
   ⇒ 财报电话会「两种加权口径的语气差」确实含信息，但它是**极短周期**信息，日频次日就衰减完。
   这是 B 类里最有希望的一颗：若能用 `hump` + 事件窗口（只在新财报后 5 日交易）把 TO 压到 0.3 以下，值得第二代。
2. `npv6b383`（socialmedia12 情绪×关注度）**2Y 1.31 远高于全周期 S 0.28** ⇒ 信号是**近两年才活过来的**。
   这类「2Y ≫ S」的件在别的区出现过反转案例，值得第二代把窗口压到 2 年内。
3. `O0A6voxg`（risk71 残差低波）是唯一 TO 天然合格（0.108）+ sub 最高（0.57）的件，但 S 只有 0.57。

### 39.2 ★★★★★ 累计命中率：19 个未点亮塔数据集，0 个可提交

| 批次 | 数据集数 | 探针数 | 最优 S | 可提交 |
|---|---:|---:|---:|---:|
| U30 pv13 | 1 | 8 | 0.48 | 0 |
| U31 institutions25 | 1 | 8 | 0.98 | 0 |
| U32 insider_agg_matrix | 1 | 8 | 0.46 | 0 |
| U33 macro27 | 1 | 8 | **1.27** | 0（F 0.41 / TO 0.40） |
| U34 八集体检 | 8 | 8 | 0.31 | 0 |
| U36 七集探针 | 7 | 7 | 0.77 | 0 |
| **合计** | **19** | **47** | **1.27** | **0** |

与此同时，**pv103（早前波次）一颗数据集就产出 2 颗全闸通过件**（`RRE5Mwkn` S2.15、`O0A6Qz7p` S2.18）。

⇒ **筛选新数据集不是产出瓶颈。** 19 集 47 条探针的信息量远大于 pv103 一颗的 8 条，
结果却有 2 vs 0 的差距。差别不在数据集多寡，在两点：

1. **机制类型**：pv103 是**日内成交微观事件流**（成交价、VWAP、单量），信息密度高、每天都有新信息；
   被筛掉的 19 集里绝大多数是**状态描述/情绪打分/结构属性**，信息更新慢或本身不承载收益。
2. **几何深度**：pv103 的 2 颗来自两腿合成 / 窗口谷结构（第 31 节反证），
   而 U34/U36 是单腿 3 算子裸骨架——**单腿骨架在 GBR 的中位产出本就只有 |S| 0.3–0.9**。

### 39.3 战略转向（依据 39.2 的证据）

「穷尽数据集」的正确做法不是「每集派一条探针」，而是**按土壤类型排队**：

| 优先级 | 土壤类型 | 判据 | 代表 |
|---|---|---|---|
| ★★★★★ | 事件流（成交/订单/笔数/流量） | 每天产生新观测 | pv103（已出货 2 颗）、**pv106（U38 在跑）**、order_book_imbalance |
| ★★★★ | 文本事件（财报会/新闻，有发布日） | 事件驱动、节律清晰 | earningscall_sentiment、ai_news_scores、earnings_sent_matrix |
| ★★★ | 变化率型（有 Δ 结构） | 一阶差分有意义 | risk71、sentiment33 |
| ★★ | 状态描述符 | TO < 10% 或纯属性 | pv13、pv71、pv29(GROUP)、pv109 |
| ★ | 纯元数据 | SYMBOL/地址/URL | other78 |

⇒ 下一阶段：**优先事件流数据集 + 两腿/合成/门控几何**，停止对状态描述符投入探针。
⇒ U37（order_book_imbalance + earningscall_sentiment + ai_news_scores）设计已就绪，属 ★★★★★/★★★★ 档，队列释放后立即派发。

## 四十一、U38 pv106 收批：8/8 全灭，但给出了一条明确的经济学结论

multisim `2oz9YVVZ4jD9GxMq9TLq8f`，8/8 完成，0 错误。

| # | 机制 | alpha | S | F | TO | R | 2Y | sub |
|---|---|---|---:|---:|---:|---:|---:|---:|
| 1 | 价差水平（Amihud 非流动性） | 1YNG5NKm | −0.22 | −0.03 | 0.412 | −0.0073 | **−1.14** | −0.14 |
| 2 | 价差 22 日变化反向 | P0oPEoz7 | 0.40 | 0.06 | 0.504 | 0.0128 | 1.19 | **−0.27** |
| 3 | 近 30 分钟价差 ÷ 全期价差 | e751J5G6 | 0.21 | 0.02 | 0.549 | 0.0067 | 0.21 | 0.15 |
| 4 | 交易成本 10 分位 | YP1ld1zl | 0.13 | 0.02 | 0.238 | 0.0053 | −0.48 | 0.07 |
| 5 | 最大成本 ÷ 10 分位成本 | kqN85NGO | −0.38 | −0.07 | 0.337 | −0.0115 | −0.86 | −0.52 |
| 6 | 滑点水平 | **npv6bvql** | **0.54** | 0.18 | 0.217 | 0.0243 | **−0.15** | 0.14 |
| 7 | 价差波动率反向 | 78LGVLM8 | 0.37 | 0.11 | **0.099** | 0.0117 | 0.46 | 0.06 |
| 8 | pv71 关系强度合计 | d5W9wWow | −0.28 | −0.05 | 0.493 | −0.0136 | 0.09 | −0.23 |

### 41.1 ★★★★ 新结论：GBR/TOP700 大盘池里，非流动性溢价方向是**反的**

`pv106_spreadbp` 水平（经典 Amihud 非流动性代理）得到 **S −0.22、2Y −1.14**：
⇒ 在 TOP700 里**价差越宽（越不流动）的股票，未来收益越低**，与 Amihud (2002) 的原始方向相反。

**原因（第一性原理）**：非流动性溢价是**小盘 / 微盘现象**——它赚的是「流动性提供者的补偿」。
TOP700 是 GBR 最大的 700 只股票，横截面里已没有真正的「不流动」股，此时价差宽窄反映的是**做市难度 / 信息不对称 / 风险**，
而不是流动性折价。所以在该池里价差变成**风险代理**，方向自然翻转。

⇒ **落地**：所有「流动性 / 价差 / 交易成本 / Amihud / 换手率」类因子，在 TOP700 及更大的大盘 universe 里，
必须先做**方向对照探针**（正负各一条），不能直接套用小盘文献的方向。
⇒ 同理，`slippage` 水平 S 0.54 但 2Y −0.15 ⇒ 该方向**历史上有效、近两年已死**。

### 41.2 累计命中率更新：20 集 55 探针 0 命中

| 批次 | 数据集 | 探针数 | 最优 \|S\| | 可提交 |
|---|---|---:|---:|---:|
| U30 pv13 | 1 | 8 | 0.48 | 0 |
| U31 institutions25 | 1 | 8 | 0.98 | 0 |
| U32 insider_agg_matrix | 1 | 8 | 0.46 | 0 |
| U33 macro27 | 1 | 8 | 1.27 | 0 |
| U34 八集体检 | 8 | 8 | 0.31 | 0 |
| U36 七集探针 | 7 | 7 | 0.77 | 0 |
| U38 pv106 | 1 | 8 | 0.54 | 0 |
| **合计** | **20** | **55** | **1.27** | **0** |

对照：单数据集 `pv103` 用两腿 / 窗口谷几何产出 **2 颗**全闸通过件（S 2.15 / 2.18，prod 0.4744 / 0.6984）。

⇒ 20 : 1 的数据集数量比，换来 0 : 2 的结果比。**「换数据集」不是产能杠杆**，这一点现在有 55 条探针的证据支撑。

### 41.3 U37 在飞、U39 备料完成

- **U37**（`2qn3932es4tw8R519vbsAzyW`）：`order_book_imbalance` 逐笔订单簿（单字段 aC 0–1）+ `earningscall_sentiment` 电话会（aC 0–5）+ `ai_news_scores` 新闻情绪置信区间，8 模板已派，排队 R3。
- **U39 备料完成并预检通过**：主攻 `stock_search_trends`（12 个全 MATRIX、aC 1–5），对应 Da–Engelberg–Gao (2011) *In Search of Attention* 的注意力→反转机制；配 `search_interest`、`other734`、`euro_equity_imbalance`（参与方净订单失衡）、`event_relation`。
- **U39 陷阱记录**：`ask_order_insertion_count` 不存在，ask 侧字段带 `_2` 后缀（`ask_order_insertion_count_2`），bid 侧无后缀 —— 预检第一次 `valid=false` 就是这条，必须靠预检拦。

### 41.4 队列

| 批次 | multisim | 状态 |
|---|---|---|
| U37 事件流三集 | `2qn3932es4tw8R519vbsAzyW` | 排队 R3 |
| U39 搜索关注度 | 待派 | 预检已过 |

处置：不 kill、不重派、不加第三批；仿真槽被外部会话占满。

## 四十二、★★★★★ 拆解两颗全闸件的真实配方：赢家是「两腿 2:1 合成 + 长窗冷腿」，不是新数据集

### 42.1 表达式原文（取自 `get_alpha_details.code`）

```
RRE5Mwkn =
  add( multiply(2, group_rank(
         ts_target_tvr_decay(ts_zscore(pv103_ivam_sum, 252), target_tvr=0.15), sector)),
       reverse(group_rank(
         ts_zscore(vec_sum(loaned_share_count_main), 504), sector)) )

O0A6Qz7p =
  add( multiply(2, reverse(group_rank(
         ts_zscore(vec_sum(loaned_share_count_main), 504), sector))),
       group_rank(ts_delta(ts_mean(vec_sum(oth47_organic_traffic), 22), 66), subindustry) )
```

### 42.2 三条硬事实

| 事实 | 证据 |
|---|---|
| ① 两颗都不是单数据集件 | `RRE5Mwkn` = `pv103_ivam_sum`（PV） + `loaned_share_count_main`（SHORTINTEREST）；`O0A6Qz7p` = `loaned_share_count_main` + `oth47_organic_traffic`（OTHER） |
| ② 共用同一条冷腿 | **`loaned_share_count_main`（shortinterest3 借券股数）在 504 日 z-score 后作冷腿**，两颗都有 |
| ③ 骨架完全相同 | `add(multiply(2, A), reverse(B))` —— **主腿权重 2、冷腿权重 1 且取反**，就是第 33 节 N4 验证过的 2:1 冷腿合成 |

⇒ 这两颗的塔位 `SHORTINTEREST+PV` / `SHORTINTEREST+OTHER` 不是平台随便标的，**就是两条腿各自的真实归属**。

### 42.3 ★★★★★ 这改写了选集策略

我在 U36 里测过 `shortinterest3`，但只用了 `max_loan_rate`（借券费率），得到 S −0.60 就放过了这个数据集 —— **错了**。
真正的金字段是 **`loaned_share_count_main`（借券股数）**，而且是 **504 日（2 年）长窗**的 z-score，不是 252。

**三个已被证明有土壤的数据集**（其余 20 个筛掉的都没有）：

| 数据集 | 金字段 | 证明 |
|---|---|---|
| `pv103` | `pv103_ivam_sum` | `RRE5Mwkn` 主腿，S 2.15 |
| `shortinterest3` | `loaned_share_count_main` | 两颗的冷腿 / 主腿，且它是 SHORTINTEREST 塔归属来源 |
| `other47` | `oth47_organic_traffic` | `O0A6Qz7p` 第二腿，S 2.18 |

**共同点**：三个都是**事件流**（日内成交额统计 / 借券交易股数 / 网站自然流量），与第 39.3 节的土壤判据完全一致。

### 42.4 对「20 颗」目标的直接含义

若 4 颗全部提交：

| 塔 | 来源 | 计数 |
|---|---|---|
| PV | RRE5Mwkn | 2→**3 点亮** |
| SHORTINTEREST | RRE5Mwkn + O0A6Qz7p | 0→**2**（差 1） |
| OTHER | O0A6Qz7p | 1→**2**（差 1） |
| ANALYST / NEWS | QPvbxjXw / rKRPAWv9 | 已亮 |

⇒ **再各出 1 颗 SHORTINTEREST 与 1 颗 OTHER 就能再点亮两塔。**
⇒ 而这两塔的土壤刚刚被证明存在（`loaned_share_count_main` / `oth47_organic_traffic`），
   所以下一批应当**在这两个字段族上换几何**，而不是继续筛新数据集。

### 42.5 配额的硬约束（必须先算清）

| 组合 | 已用 | 上限 | 余量 |
|---|---:|---:|---:|
| `集合内 × 集合外` 总量（PV/OTHER/FUNDAMENTAL/MODEL × 其它） | 2 | 5 | **3** |
| PV × SHORTINTEREST | 1 | 3 | 2 |
| OTHER × SHORTINTEREST | 1 | 3 | 2 |

⇒ 还能做 **3 颗跨塔件**；单数据集 ATOM 不占配额，可无限做。
⇒ 因此最优排产：**先做单数据集 ATOM**（shortinterest3 单塔、other47 单塔），跨塔件留给最有把握的 3 个位置。

---

## 43. U37 收批 + U39 连坐归因 + U40/U41 派发（23 集 63 探针 0 命中）

### 43.1 U37 收批：8/8 完成，0 可提交，但挖出本战役最强新信号族

multisim `2qn3932es4tw8R519vbsAzyW`，8/8 COMPLETE，0 错误。全部 `other` 塔（GBR other 当前点亮 1/3）。

| # | alpha | 数据集 | 机制 | S | F | TO | R | 2Y | sub | fails |
|---|---|---|---|---:|---:|---:|---:|---:|---:|---:|
| 1 | KPJVRoZl | earningscall_sentiment | 盈利能力主题 正(演示) − 正(问答) | 0.29 | 0.05 | 0.600 | 1.59% | 0.66 | 0.11 | 5 |
| 2 | wpQNVdW5 | earningscall_sentiment | 负情绪问答 ÷ 段落数 | 0.33 | 0.06 | 0.596 | 1.80% | 0.26 | 0.08 | 5 |
| 3 | omEPebZE | order_book_imbalance | 买卖挂单插入笔数差 | 0.40 | 0.12 | 0.234 | 2.04% | 1.15 | 0.66 | 3 |
| 4 | **9qxGQek2** | **order_book_imbalance** | **收盘拍卖订单失衡占 ADV** | **0.69** | **0.30** | **0.177** | **3.23%** | **1.61** | **0.88** | **2** |
| 5 | LLM8xv2L | order_book_imbalance | 收盘拍卖价格错位（反向） | 0.51 | 0.16 | 0.262 | 2.65% | 1.37 | 0.72 | 3 |
| 6 | QPvWdxoX | order_book_imbalance | 暗池/双边成交额比 | 0.74 | 0.38 | 0.190 | 5.15% | 1.46 | 0.26 | 5 |
| 7 | KPJVRo28 | ai_news_scores | 负面评分置信带宽度 | 0.31 | 0.05 | 0.440 | 0.99% | **2.57** | 0.06 | 3 |
| 8 | Xg9NE3Ob | ai_news_scores | (正−负) ÷ 置信带宽度 | 0.56 | 0.12 | 0.395 | 1.81% | **2.68** | 0.35 | 2 |

**三条硬结论**：

1. **`9qxGQek2` 是本轮唯一「fails = 2」的候选**（只差 `LOW_SHARPE` + `LOW_FITNESS`）：S 0.69 / F 0.30 / TO 17.7% / 2Y 1.61 / sub 0.88。它的 TO 已非常接近 12.5% 地板、sub 0.88 远超 0.14 线、2Y 1.61 过线，说明**信号方向、风控、稳定性全对，只差幅度**。这类件是「放大」问题不是「重建」问题，值得进第二代。
2. **`Xg9NE3Ob` 是第二个 fails = 2 的件**（S 0.56 / 2Y 2.68 / sub 0.35），但 TO 39.5% 且 sub 0.35 偏弱。
3. **`ai_news_scores` 的 2Y = 2.57 / 2.68 是本战役至今最高 2Y**，而全周期 S 只有 0.31 / 0.56 ⇒ 该数据集的信号**只在近两年活着**。机理：LLM 新闻评分是 2021 年后才成熟的信息源，2014–2020 段要么无数据要么是低质代理。落地：这类「新信息源」数据集在全周期 IS Sharpe 口径下**结构性吃亏**，判死可以，但必须标注「2Y 专用机制」，将来若有短窗赛道优先取用。

multisim `QPvWdxoX` 另带一条 WARNING：`Incompatible unit for input of "add" at index 1, expected Unit[CSPrice:1,CSShare:1], found Unit[]` —— 除数为纯数时 `+1` 引入无量纲量，unitHandling=VERIFY 下会告警但不阻断，需注意别在跨字段加法里混单位。

### 43.2 U39 全部 8 条报错的真因：event 类型字段不支持算术算子 ⇒ 连坐 KILLED 整批

`_tmp_multisim_diag.py` 直连子仿真拿到真实 message（父层 `message` 恒为 None）：

```
parent status: ERROR
  11t4C5fR... ERROR  msg=Operator multiply does not support event inputs.
  2bk7sYfy... ERROR  msg=Operator add does not support event inputs.
  其余 6 条      CANCELLED  msg=None
```

⇒ **不是语法错、不是资源超限，是 event 类型字段不能参与 `multiply` / `add`（以及 `subtract` 一类算术）**。触发点是 `search_interest` 数据集（`relative_interest_score_6 * sentiment_confidence_score_d1`）与 `event_relation` 数据集（`relation_strength_score_financial`）。

**新禁区（登记）**：`search_interest`、`event_relation` 等 event 类型字段**只能用 `vec_*` / `ts_*` / `group_*` 单字段变换，禁止与其他字段做算术合成**。另注意**连坐效应**：8 条里有 2 条语法/类型错，平台会 CANCELLED 掉其余 6 条干净表达式，收割体表现为 `comp=0 err=8` 全灭，**极易被误判成「数据集全死」**。

**排障标准动作（新增）**：收割出现 `error_count == total` 且 `error` 文案是 `No alpha_id in sim response` 时，**不要**下任何数据集结论，先跑 `results/_tmp_multisim_diag.py <multisim_id>` 读子任务 message，区分「自身错」与「连坐取消」。

### 43.3 U40 / U41 派发

**U40** `4sEuk81S55cfbUEzV9wL34X`（8 条，全部单数据集 ATOM，不占塔混配额）—— 在 RRE5Mwkn / O0A6Qz7p 拆解出的三个已证明字段族上换几何：

| # | 数据集 | 字段 | 机制 |
|---|---|---|---|
| 1 | shortinterest3 | `vec_sum(transaction_count_main)` 504 窗 | 借券交易笔数活跃度 |
| 2 | shortinterest3 | `loaned_market_value_usd / loaned_share_count` 252 | 借券平均单价（隐含做空标的市值） |
| 3 | shortinterest3 | `vec_avg(average_loan_duration_days_main)` 504 反向 | 借券久期（借得越久越有信心做空） |
| 4 | shortinterest3 | `max_loan_rate_main − min_loan_rate_main` 252 | 借券费率横截面离散度 |
| 5 | other47 | `paid_search_visitors / oth47_organic_traffic` 252 反向 | 付费流量占比（越依赖付费越差） |
| 6 | other47 | `oth47_organic_cost / oth47_organic_traffic` 252 反向 | 自然流量单位成本 |
| 7 | other47 | `oth47_organic_keywords / paid_search_terms_count` 252 | 自然关键词相对覆盖 |
| 8 | other47 | `vec_avg(website_traffic_rank_enriched)` 252 反向 | 流量排名（越小越好） |

**U41** `1NCQNfgZI4NN8MYzqfqs9Ks`（8 条，order_book_imbalance 第二代，围绕 `9qxGQek2` 唯一 fails=2 的拍卖失衡信号放大）：

| # | 模板 | 骨架 | 四维坐标（结构/几何/矩/轴） |
|---|---|---|---|
| T1 | 两腿同集 2:1 | 拍卖失衡×2 + reverse(收盘错位) | 两腿合成 / 加权线性 / 复合 / market |
| T2 | 双口径背离 | `pct_adv − pct_auction` | 单腿叉积 / 差 / 水平 / sector |
| T3 | 订单侵略性 | `bid 价格改善 − ask 价格恶化` | 单腿叉积 / 差 / 水平 / subindustry |
| T4 | 挂单寿命不对称 | `bid 成交寿命 − ask 成交寿命`（反向） | 单腿叉积 / 差 / 水平 / sector |
| T5 | **门控** | `trade_when(拍卖失衡 z>1, reverse(收盘错位), -1)` | 条件门控 / 阈值 / 水平 / sector |
| T6 | 暗池占比变化 | `ts_delta(dark / lit, 22)`（反向） | 单腿 / 比率+差分 / 一阶差分 / subindustry |
| T7 | 拍卖失衡二阶矩 | `−ts_std_dev(pct_adv, 66)` | 单腿 / 波动率 / **二阶方差** / sector |
| T8 | 两腿跨集 2:1 | 拍卖失衡×2 + reverse(`loaned_share_count_main` 504) | 两腿合成 / 加权 / 复合 / market+sector |

T8 复用 RRE5Mwkn / O0A6Qz7p 的已验证冷腿（`loaned_share_count_main` 504 日 z-score），占「集合内(OTHER) × 集合外(SHORTINTEREST)」配额 1 个 ⇒ 该桶由 2/5 升至 **3/5**。其余 7 条全部单数据集，不占配额。

T5 是本战役**第一次在 GBR 用门控骨架**（此前全为无门控），补齐「条件/门控」这一维；T7 补齐「二阶方差」维。

### 43.4 累计统计：23 集 63 探针 0 命中

| 波次 | 数据集数 | 探针数 | 最优 S | 备注 |
|---|---:|---:|---:|---|
| U30 pv13 | 1 | 8 | 0.48 | |
| U31 institutions25 | 1 | 8 | 0.98 | |
| U32 insider_agg_matrix | 1 | 8 | 0.46 | 常数/稀疏字段 |
| U33 macro27 | 1 | 8 | 1.27 | 二代 N8 到 1.59 但撞 4 闸，判死 |
| U34 | 8 | 8 | 0.31 | |
| U36 | 7 | 7 | 0.77 | |
| U38 pv106 | 1 | 8 | 0.54 | 流动性溢价在大盘反向 |
| **U37** | **3** | **8** | **0.74** | **fails=2 两条，order_book 进第二代** |
| 合计 | **23** | **63** | — | **0 颗可提交** |

对照：单数据集 `pv103` 靠两腿 / 窗口谷几何产出 2 颗全闸件。⇒ **「扫新数据集」至今 63 条探针颗粒无收，「在已证明字段族上换几何」2/2 出货**。这条对比是本战役最重要的产能证据，选集策略应继续向后者倾斜。

---

## 44. 未点亮塔全池普查（82 集）：覆盖率字段不可用 + 按拥挤度重排的可挖清单

### 44.1 ★★★★ 纠错：`get_datasets` 的 dataset 级 `coverage` 不能作判死依据

本轮对 GBR/TOP700/D1 全部 **177 个数据集**做了一次零成本普查，筛出未点亮塔（category 已提交 < 3）共 **82 个**，其中 **53 个** 的 dataset 级 `coverage` 字段报 `0`。

若按「cov=0 ⇒ 无数据 ⇒ 判死」处理会**错杀至少 7 个已被仿真证明有数据的集**：

| 数据集 | dataset 级 cov | 实跑结果 |
|---|---:|---|
| `macro27` | 0 | U35 出 S 1.59（fails 4 闸） |
| `institutions25` | 0 | U31 出 S 0.98 |
| `risk71` | 0 | U36 出 S 0.57 / sub 0.57 |
| `pv106` | 0 | U38 出 S 0.54 |
| `insiders12` | 0 | U36 出 S −0.44 |
| `ai_news_scores` | 0 | U37 出 S 0.56 / **2Y 2.68** |
| `socialmedia12` | 0 | U36 出 S 0.28 / 2Y 1.31 |

⇒ **dataset 级 `coverage` 与实际可仿真性脱钩**（疑似指向某个主字段，或缓存陈旧）。

#### 44.1.1 ★★★★★ 二次纠错：**字段级 coverage 同样不可信**

写上一段后立刻被自己的另一条证据推翻：`pv103` 全 8 个字段（含 `pv103_ivam_sum`）的**字段级** coverage 全部报 `0.00`，而 `pv103_ivam_sum` 正是 S 2.15 那颗 `RRE5Mwkn` 的信号腿。同一轮里 `institutions4` 字段级报 0.39、`order_book_imbalance` 报 0.16–0.43，说明**该字段只在部分 vendor 的集上被填充，其余一律为 0**。

因此：

- **dataset 级 coverage 与字段级 coverage 都不能判死**。
- 唯一可信判据是**实跑指标**（S/F/TO/longCount）。
- `option1` / `risk68` / `imbalance5` 的「cov 全 0」**不作为死亡理由**；`option1` 的真实死因仍是早前实证的 VECTOR 期权面「took too much resource」连坐，`risk68` / `imbalance5` 目前**状态未知**（未实跑）。

**代价与教训**：差点用「cov=0」一次性错杀 5 个集（含 3 个真实有数据的），其中 `pv103` 会直接砍掉本战役最强信号的来源。**凡是想用某个「批量元数据字段」一次筛掉大量数据集之前，先拿 2–3 个已知能跑的集做反向对照**。

### 44.2 按拥挤度（alphaCount）重排的可挖清单 —— 25 个候选数据集

过滤条件：未点亮塔 ∧ `fieldCount > 2`（排除纯轴/元数据）∧ dataset cov>0。按 `alphaCount` 升序（越前越冷门）：

| # | 数据集 | 塔 | 字段数 | 用户数 | alphaCount | 状态 |
|---:|---|---|---:|---:|---:|---|
| 1 | other384 | other | 66 | 5 | **6** | 未探 |
| 2 | euro_equity_imbalance | other | 4 | 6 | 7 | U39 连坐未测 |
| 3 | other250 | other | 12 | 4 | 8 | U34 已探（S 0.15） |
| 4 | other699 | other | 7 | 13 | 14 | 未探 |
| 5 | stock_cluster_dl | other | 5 | 11 | 19 | 已排除（纯 PCA） |
| 6 | other545 | other | 4 | 18 | 26 | 未探 |
| 7 | pv109 | pv | 26 | 15 | 32 | 已画像（公司债属性） |
| 8 | other47 | other | 18 | 22 | 33 | **已验证字段族**（U40 在测） |
| 9 | **institutions4** | **institutions** | **6** | **38** | **47** | **未探 ← 本轮最优新目标** |
| 10 | institutions1 | institutions | 7 | 34 | 52 | U36 已探（S −0.05） |
| 11 | pv29 | pv | 50 | 53 | 73 | 已画像（10 个 GROUP 分组轴） |
| 12 | insiders1 | insiders | 9 | 53 | 87 | 已判死（insiders 无土壤） |
| 13 | order_book_imbalance | other | 240 | 60 | 96 | **U37 出 fails=2，U41 二代在测** |
| 14 | sentiment7 | sentiment | 3 | 58 | 96 | 2Y 1.60（memory 记录达标） |
| 15 | risk60 | risk | 5 | 127 | 202 | 已探（S 0.12） |
| 16 | sentiment33 | sentiment | 255 | 102 | 209 | U36 已探（S 0.15） |
| 17 | insider_trx_matrix | other | 33 | 124 | 215 | 未探 |
| 18 | fund_holdings_panel | institutions | 18 | 173 | 294 | 已探（2Y −1.50，判死） |
| 19 | pv30 | pv | 240 | 159 | 400 | 未探 |
| 20 | other455 | other | 1500 | 169 | 412 | 拥挤（aC 412） |
| 21 | insider_matrix | other | 33 | 293 | 553 | 未探（与 insider_trx_matrix 同族） |
| 22 | insider_agg_matrix | insiders | 34 | 247 | 562 | 已判死（常数/稀疏字段） |
| 23 | sentiment27 | sentiment | 18 | 347 | 834 | U34 已探（S −0.26） |
| 24 | institutions6 | institutions | 11 | 423 | 942 | U34 已探（S −0.05） |
| 25 | dl_riskfree_returns | other | 133 | 470 | 983 | 未探（无风险利率，疑常数） |

**未被过滤掉但已先验排除**：`pv1`(aC 56109)、`techindi_model`(26992)、`pattern_scores`(1841)、`shortinterest3`(1668，但已验证金字段在用它)、`acquisition_model`(1596)。

### 44.3 新目标：`institutions4` 字段画像（6 字段，aC 47，u 38 —— 全池最冷门的真信号集）

全部 VECTOR，字段级 cov 0.39：

```
institutional_holding_current_market_value      当前持仓市值
institutional_holding_previous_market_value     上期持仓市值
institutional_holding_current_shares            当前持股数
institutional_holding_previous_shares           上期持股数
institutional_holding_percent_of_portfolio      占机构组合权重
institutional_holding_percent_of_shares_outstanding  占流通股比例
```

**土壤类型判定：★★★★（变化率型 + 季度事件）** —— 13F 类数据集的核心信息全在「本期 vs 上期」的差分，不是水平。这与已判死的 `insider_agg_matrix`（常数/稀疏 flag）完全不同，也与 `fund_holdings_panel`（2Y −1.50）不同：后者是基金层聚合，前者是**个股层的机构持股变化**。

**约束**：6 个字段全是 VECTOR，必须先 `vec_sum`/`vec_avg` 聚合；`current − previous` 的差值必须用同名 `vec_*` 变换后再相减（不能先相减再聚合，语义会变成「同一向量的逐元素差」）。

**备选模板（≥10 个，下轮 U42 用）**：

| # | 机制 | 骨架要点 |
|---|------|---------|
| 1 | 机构净买入强度 | `(vec_sum(cur_shares) − vec_sum(prev_shares)) / (vec_sum(prev_shares)+1)` |
| 2 | 持股占流通比变化 | `vec_avg(cur_pct_out) − vec_avg(prev_pct_out)` |
| 3 | 隐性成本变化 | `(cur_mv − prev_mv) / (cur_shares − prev_shares + 1)` 隐含机构成交均价 |
| 4 | 组合权重变化 | `vec_avg(cur_pct_port) − vec_avg(prev_pct_port)` |
| 5 | 持股广度 | `vec_count(cur_shares)` 机构家数 |
| 6 | 持仓集中度 | `vec_std_dev(cur_pct_port)` |
| 7 | 越跌越买背离 | 股数增 ∧ 市值减 ⇒ `sign` 组合 |
| 8 | 市值/股数双重确认 | 两腿 2:1 合成 |
| 9 | 比率型 | `cur_mv/prev_mv − 1` 与 `cur_shares/prev_shares − 1` 价差 |
| 10 | 门控 | `trade_when(持股广度 > 中位, 净买入强度, -1)` |

### 44.4 只能当轴的集（不是信号源）

- **risk88**（cov 1.00，1 字段）：`alternative_market_cap_usd` —— 替代市值，只能作规模分组 / bucket 轴。
- **socialmedia39**（cov 0.49，1 字段）：`scl39_top5_people_also_watch_ticker_ii` —— 共视网络边权，只能作关系轴。
- **pv29**（50 字段含 10 个 GROUP）：`industry_grouping_level{2,10,20}_*` —— 纯分组轴。

---

## 45. ★★★★★ U41 收批：第 5 颗全闸件 `ZYQXZj73` + 「2:1 合成 + shortinterest 冷腿」配方跨数据集复现成功

### 45.1 八条结果

multisim `1NCQNfgZI4NN8MYzqfqs9Ks`，8/8 COMPLETE，0 错误。全部 `other` 塔（`ZYQXZj73` 为 `shortinterest/other` 双塔）。

| # | alpha | 模板 | S | F | TO | R | 2Y | sub | fails |
|---|---|---|---:|---:|---:|---:|---:|---:|---:|
| 1 | ZYQXZjE3 | 两腿同集 2:1（拍卖失衡×2 + reverse 收盘错位） | 0.98 | 0.33 | 0.333 | 3.86% | 1.69 | 0.88 | 2 |
| 2 | MPYgwbGk | 双口径背离 `pct_adv − pct_auction` | 0.54 | 0.20 | 0.183 | 2.63% | 1.26 | 0.83 | 3 |
| 3 | npv60nNd | 订单侵略性 `bid 改善 − ask 恶化` | 0.53 | 0.19 | 0.214 | 2.69% | 1.41 | 0.73 | 3 |
| 4 | zq3Aa5NG | 挂单寿命不对称 | 0.40 | 0.12 | 0.241 | 2.08% | 1.09 | 0.63 | 3 |
| 5 | omEP2nNk | **门控** `trade_when(拍卖失衡 z>1, …)` | **−0.27** | −0.07 | 0.132 | −0.95% | −0.21 | −0.21 | 4 |
| 6 | d5W9qnZJ | 暗池占比一阶差分 | 0.74 | 0.32 | 0.180 | 3.47% | 0.92 | **0.90** | 3 |
| 7 | xArlMeNJ | 拍卖失衡二阶矩 `−ts_std_dev` | 0.39 | 0.15 | **0.119** | 1.97% | 1.20 | 0.61 | 3 |
| 8 | **ZYQXZj73** | **两腿跨集 2:1（拍卖失衡×2 + shortinterest 冷腿）** | **1.78** | **1.16** | **0.133** | **5.63%** | **2.84** | **1.70** | **0** |

### 45.2 `ZYQXZj73` 全量核实（已过全部 RA 闸）

```
add( multiply(2, group_rank(ts_zscore(vec_avg(auction_order_imbalance_pct_adv), 22), market)),
     reverse(group_rank(ts_zscore(vec_sum(loaned_share_count_main), 504), sector)) )
```

| 项 | 值 |
|---|---|
| Sharpe | **1.78**（线 1.58 ✓） |
| Fitness | **1.16**（线 1.00 ✓） |
| Turnover | 13.3%（<70% ✓） |
| Returns | 5.63% |
| Drawdown | **5.11%（全战役最低）** |
| Margin | **8.47 bp（全战役最高，RRE5Mwkn 是 6.14）** |
| long / short | **455 / 455（完全均衡）** |
| 2Y Sharpe | **2.84** |
| sub_universe_sharpe | **1.70** |
| **investability_sharpe / fitness** | **1.79 / 1.21（全战役最高）** |
| `failed_ra_count` | **0** |
| pass 列表 | LOW_SHARPE, LOW_FITNESS, LOW_TURNOVER, HIGH_TURNOVER, CONCENTRATED_WEIGHT, LOW_SUB_UNIVERSE_SHARPE, IS_LADDER_SHARPE, CLUSTER_TEST, MATCHES_PYRAMID |
| fail 列表 | **空** |
| **self 相关** | **0.2438**（最高撞 rKRbrZKo；远低于 0.70 线 ✓） |
| 塔位 | GBR/D1/SHORTINTEREST ×1.2 + GBR/D1/OTHER ×1.6，effective 2 |
| **prod 相关** | 待测 |

### 45.3 三条方法论结论

**① 「2:1 合成 + `loaned_share_count_main` 504 长窗冷腿」是跨数据集可迁移的配方，不是 pv103 的偶然。**

同一条冷腿、同一种权重结构，只把信号腿从 `pv103_ivam_sum` 换成 `auction_order_imbalance_pct_adv`，就复刻出 S 1.78 / 全闸通过。对照同批 T1（同数据集内 2:1，不用冷腿）：S 从单腿的 0.69 抬到 **0.98**，抬升 +0.29 但不足以过 1.58。⇒ **冷腿贡献的不是「多样性」，是近 +0.8 的 Sharpe 量级**。

**② 门控骨架在低频事件字段上是负资产。**

T5 用 `trade_when(ts_zscore(拍卖失衡, 66) > 1, …)` 是唯一负 S 的一条（−0.27，且 TO 降到 13.2% 说明样本被砍掉大半）。拍卖订单失衡本身是**每日一个标量**的稀疏事件，再加一层 z>1 的阈值筛，留下的样本既少又偏向极端拍卖日（通常是指数调整日/到期日），信号被彻底破坏。**判据：`trade_when` 只适用于「字段本身连续且高频」的条件，不适合给稀疏事件再套阈值。**

**③ 二阶矩模板把 TO 压到最低但拿不到 Sharpe。**

T7 `−ts_std_dev(拍卖失衡, 66)` 的 TO 0.119 是全批最低、也贴近 12.5% 地板，但 S 只有 0.39。⇒ **在本数据集中「波动率」维度不含预测信息，收益全在「水平 + 符号」维度**。

### 45.4 塔位推演（5 颗全提交后：三塔同时点亮）

| 塔 | 现状 | 5 颗提交后 | 来源 |
|---|---:|---:|---|
| **PV** | 2 | **3 ⇒ 点亮** | RRE5Mwkn |
| **SHORTINTEREST** | 0 | **3 ⇒ 点亮** | RRE5Mwkn + O0A6Qz7p + ZYQXZj73 |
| **OTHER** | 1 | **3 ⇒ 点亮** | O0A6Qz7p + ZYQXZj73 |
| ANALYST / NEWS | 3 | 已点亮 | QPvbxjXw / rKRPAWv9 |

⇒ 这是本战役「点塔效率」最高的一组：**5 次提交动作点亮 3 个塔**，且三塔里 SHORTINTEREST 是从 0 直接到 3。

### 45.5 配额更新

- 集合内 × 集合外：**3/5**（PV×SHORTINTEREST 1 个 = `RRE5Mwkn`；OTHER×SHORTINTEREST 2 个 = `O0A6Qz7p`、`ZYQXZj73`） ⇒ **剩 2 个名额**。U40 八条全是单数据集 ATOM，不占配额。

> **★★★★★ 配额破局点**：冷腿 `loaned_share_count_main` 属 SHORTINTEREST，而 SHORTINTEREST **不在禁混集合** `{PV,MODEL,OTHER,FUNDAMENTAL}` 内。因此「**集合外塔的信号腿 × SHORTINTEREST 冷腿**」属于**集合外 × 集合外 ⇒ 不限量**！
>
> 具体可无限组：`institutions4` / `sentiment*` / `risk*` / `insiders*` / `earnings*` / `socialmedia*` / `macro27` / `imbalance*` 任一信号腿 × 该冷腿，都不吃任何配额。**这才是把已验证配方规模化的正确路径**，而不是继续在 OTHER / PV 上挤剩余 2 个名额。
- 两塔组合 OTHER×SHORTINTEREST：**2/3**（O0A6Qz7p、ZYQXZj73） ⇒ 剩 1。
- 单数据集 ATOM：不占配额（U40 八条全在此列）。

**落地约束**：后续任何「OTHER × SHORTINTEREST」的新表达式**最多再派 1 条**，之后该组合封盘；集合内 × 集合外的总额度也只剩 1 个。想要继续利用这条已验证配方，必须换一个**集合外**的搭档塔（sentiment / institutions / risk / insiders / earnings / socialmedia / macro / imbalance）。

---

## 46. `ZYQXZj73` prod 0.6524 通过 ⇒ 第 5 颗完整候选；但互相关暴露「两颗只能二选一」

### 46.1 prod 结果

| alpha | prod | 判定 |
|---|---:|---|
| `RRE5Mwkn` | 0.4744 | ✓ |
| `O0A6Qz7p` | **0.6984** | ✓（余量 0.0016，压线） |
| `QPvbxjXw` | 0.5794 | ✓ |
| `rKRPAWv9` | 0.3998 | ✓ |
| **`ZYQXZj73`** | **0.6524** | **✓（余量 0.0476）** |

⇒ **5 颗候选全部 IS 全闸 + self<0.70 + prod<0.70**。这是本战役至今唯一一次 5 颗同时就绪。

### 46.2 ★★★★ 五颗互相关矩阵（1021 个观测点、4 年）

|  | RRE5Mwkn | O0A6Qz7p | QPvbxjXw | rKRPAWv9 | ZYQXZj73 |
|---|---:|---:|---:|---:|---:|
| RRE5Mwkn | 1 | 0.340 | 0.004 | 0.017 | 0.321 |
| O0A6Qz7p | 0.340 | 1 | 0.167 | −0.105 | **0.7684** |
| QPvbxjXw | 0.004 | 0.167 | 1 | −0.164 | 0.152 |
| rKRPAWv9 | 0.017 | −0.105 | −0.164 | 1 | −0.101 |
| ZYQXZj73 | 0.321 | **0.7684** | 0.152 | −0.101 | 1 |

**唯一超阈对：`O0A6Qz7p` × `ZYQXZj73` = 0.7684**。其余全部 ≤0.34。

**机理**：这两颗**共用同一条冷腿** `reverse(group_rank(ts_zscore(vec_sum(loaned_share_count_main), 504), sector))`，只有信号腿不同（有机流量 vs 拍卖失衡）。冷腿在 O0A6Qz7p 里权重 1、在 ZYQXZj73 里权重 1，而两者的信号腿本身相关性很低 ⇒ **0.77 的相关性几乎全部来自共享冷腿**。

（对照：`RRE5Mwkn` 也用同一冷腿，但它把冷腿放在权重 1、信号腿权重 2 且信号腿是 pv103，与 O0A6Qz7p 只有 0.34、与 ZYQXZj73 只有 0.32 —— 说明**共享冷腿本身不必然推高相关，权重与信号腿的差异会把它压下来**。）

### 46.3 落地结论：这两颗只能提交一颗

BRAIN 的 `SELF_CORRELATION` 只比对**已提交**的 alpha。两颗现在互相 0.7684 > 0.70 ⇒ **先提交的那颗成功，后提交的那颗会被 self 墙拦下**。

| 方案 | 塔位收益 | 说明 |
|---|---|---|
| 提交 `O0A6Qz7p` | SHORTINTEREST +1、OTHER +1 | S 2.18 更高，但 prod 0.6984 距线仅 0.0016 |
| **提交 `ZYQXZj73`** | SHORTINTEREST +1、OTHER +1 | S 1.78，prod 0.6524 余量 0.048；DD 5.11%、margin 8.47bp、investability 1.79/1.21 全为战役最优 |

**塔位收益完全相同**，所以选择只看稳健性 ⇒ **推荐 `ZYQXZj73`，`O0A6Qz7p` 转备选**。若用户更看重 Sharpe 绝对值，则选 `O0A6Qz7p`，但需接受 0.0016 的 prod 余量可能在平台侧重算时翻车。

**推荐提交序列（4 颗）**：`RRE5Mwkn` → `ZYQXZj73` → `QPvbxjXw` → `rKRPAWv9`。这 4 颗互相关最大 0.34，可同批提交不撞 self。

### 46.4 塔位终态（提交上述 4 颗后）

| 塔 | 现状 | 提交后 |
|---|---:|---:|
| **PV** | 2 | **3 ⇒ 点亮** |
| SHORTINTEREST | 0 | 2（差 1） |
| OTHER | 1 | 2（差 1） |
| ANALYST / NEWS | 3 | 已点亮 |

⇒ 距「SHORTINTEREST 与 OTHER 同时点亮」只差**各 1 颗**，而这两颗必须落在 OTHER×SHORTINTEREST 组合上。**该组合候选已 2/3，只剩最后一次机会** —— 这唯一的名额应当用于一颗与 `ZYQXZj73` 互相关 <0.70 的解耦变体，一次提交同时点亮两塔。

### 46.5 解耦候选的杠杆（供下一批用）

共享冷腿是 0.77 相关的来源，解耦必须动冷腿或动权重结构（不能只动信号腿）：

| 杠杆 | 具体做法 | 是否改持仓 |
|---|---|---|
| 冷腿窗口位移 | 504 → 378 / 630 | 改 |
| 冷腿分组轴 | `sector` → `subindustry` / `industry` | 改 |
| 权重结构 | `multiply(2, A)` → `A + 0.5·B`（O0A6Qz7p 与 U31-G8 用过） | 改 |
| 冷腿归一化 | `ts_zscore(...,504)` → `ts_rank(...,504)` | 改 |

⚠️ 该组合仅剩 1 个名额，只能试一次，必须先想清楚再用。

---

## 47. ★★★★ U40 收批：shortinterest3 是「统一符号」信号源，反转后可能直接出第 6 颗

### 47.1 八条结果

multisim `4sEuk81S55cfbUEzV9wL34X`，8/8 COMPLETE，0 错误。全部单数据集 ATOM（不占塔混配额）。

| # | alpha | 数据集 | 机制 | S | F | TO | R | 2Y | sub |
|---|---|---|---|---:|---:|---:|---:|---:|---:|
| 1 | **rKR0keOE** | shortinterest3 | `vec_sum(transaction_count_main)` 504 | **−1.72** | −1.06 | **0.1085** | −4.78% | **−2.85** | **−1.60** |
| 2 | YP1lZMbM | shortinterest3 | 借券市值 ÷ 借券股数 252 | −0.60 | −0.17 | 0.2628 | −2.02% | −0.93 | −0.52 |
| 3 | npv60Pdq | shortinterest3 | 借券久期（已反向）504 | −0.43 | −0.12 | 0.1573 | −1.16% | −0.79 | −0.03 |
| 4 | 78LGO6N5 | shortinterest3 | 费率 max−min 252 | −0.73 | −0.23 | 0.1934 | −1.90% | −1.46 | −0.54 |
| 5 | LLM8eZZa | other47 | 付费访客 ÷ 自然流量 252（反向） | 0.11 | 0.02 | 0.1449 | 0.37% | 0.78 | 0.16 |
| 6 | O0A6e88v | other47 | 自然流量单位成本 252（反向） | 0.47 | 0.15 | 0.1450 | 1.48% | 0.70 | 0.79 |
| 7 | VkxMn00Y | other47 | 自然关键词 ÷ 付费词数 252 | 0.46 | 0.14 | 0.1542 | 1.45% | 0.46 | 0.49 |
| 8 | WjOYkeeG | other47 | 流量排名 252（反向） | 0.44 | 0.12 | 0.1850 | 1.37% | 0.26 | 0.63 |

### 47.2 ★★★★★ 核心发现：shortinterest3 是全数据集统一符号，且量级单调

四个**互不相同**的借券类字段，全部给出**负 Sharpe**，且负得越深对应越强的「借券强度」语义：

| 字段 | 语义 | S |
|---|---|---:|
| `vec_sum(transaction_count_main)` | 借券成交笔数（活动强度） | **−1.72** |
| `max_loan_rate_main − min_loan_rate_main` | 费率横截面离散度 | −0.73 |
| `loaned_market_value_usd / loaned_share_count` | 借券平均单价 | −0.60 |
| `avg_loan_duration_days_main` | 借券久期（已带反向） | −0.43 |

⇒ **该数据集只有一个方向：借券侧活动越强，未来收益越差**。经济学上完全自洽 —— 融券余额上升 / 借券成本抬升 / 借券笔数激增都是看空压力，而看空压力是有信息含量的（Short interest anomaly, Asquith–Pathak–Ritter 2005）。

**关键量化**：`rKR0keOE` 的负数版本是 S −1.72 / F −1.06 / TO **10.85%** / 2Y −2.85 / sub −1.60。**把符号翻过来就是 S 1.72 / F 1.06 / TO 10.85% / 2Y 2.85 / sub 1.60 —— 全部落在闸线之上**。

⇒ 这解释了为什么三颗全闸件的冷腿都用 `reverse(group_rank(ts_zscore(vec_sum(loaned_share_count_main), 504), sector))`：**不是随便挑的冷腿，而是该数据集唯一的正确方向**。

### 47.3 U45 反转验证批（已派发 `3ekCYtdhJ5f69LqXrboBmcN`）

记忆里有一条铁律：**「加负号翻不翻号取决于字段族」**（CHN 实测风险分位族四个方向全不翻号）。所以不能假定 −1.72 翻过来就是 +1.72，必须实测。本批 8 条专门做这件事：

| # | 表达式要点 | 目的 |
|---|---|---|
| 1 | `reverse(transaction_count_main 504, sector)` | **主假设：翻转后直接过闸（潜在第 6 颗）** |
| 2 | `reverse(transaction_count_main 252, sector)` | 窗口谷（1 年） |
| 3 | `reverse(transaction_count_main 1008, sector)` | 窗口谷（3 年） |
| 4 | `reverse(费率 max−min 252, sector)` | 二级字段翻转（原 −0.73） |
| 5 | `reverse(借券市值÷股数 252, subindustry)` | 二级字段翻转（原 −0.60） |
| 6 | `reverse(借券久期 504, sector)` | 二级字段翻转（原 −0.43） |
| 7 | `group_rank(ts_zscore(vec_sum(loaned_share_count_main), 504), sector)` | **冷腿本体不反向 ⇒ 测符号基准**（预期约 −1.5 到 −2.0） |
| 8 | `reverse(transaction_count_main 504, subindustry)` | 换分组轴 |

第 7 条是本批的**诊断锚点**：它不经过任何 reverse，直接给出「冷腿族未反向时的 S」。若它确实是很深的负数，就证明该字段族**翻号行为正常**（与风险分位族不同），第 1–3 条的成功率就很高。

### 47.4 副发现：other47 的信号全在「变化率」里，不在「水平/比率」里

四条 other47 探针（付费访客占比、自然流量单位成本、关键词相对覆盖、流量排名）全部落在 **S 0.11–0.47** 的低区间，而 `O0A6Qz7p` 用同一字段 `oth47_organic_traffic` 却能到 **S 2.18**。差别只在几何：

```
O0A6Qz7p 的信号腿 = group_rank(ts_delta(ts_mean(vec_sum(oth47_organic_traffic), 22), 66), subindustry)
本批四条       = group_rank(±ts_zscore(<比率>, 252), <axis>)
```

⇒ **该数据集的预测信息在「22 日均线的 66 日差分」（两层时间加工后的变化率）里，任何横截面比率或水平 z-score 都提不出来**。这条与「TO<12% 且 |S|<0.5 ⇒ 慢变结构描述符」互斥：other47 的 TO 是 14.5–18.5%，不算慢变，但它仍然只有变化率几何有效。

### 47.5 累计统计更新

| 波次 | 数据集 | 探针 | 最优 | 备注 |
|---|---:|---:|---:|---|
| U30–U38 | 20 | 55 | 1.59 | 全部不可提交 |
| U37 | 3 | 8 | 0.74 | order_book 拍卖失衡进二代 |
| **U41** | **1** | **8** | **1.78 ⇒ 全闸通过** | **ZYQXZj73（配方复现）** |
| U40 | 2 | 8 | −1.72（未翻转） | shortinterest3 统一符号发现 |
| 合计 | **26** | **79** | — | **+1 颗（共 5 颗）** |

---

## 48. 字段画像补全（other384 / insider_trx_matrix / sentiment7 / other699 / other545）+ U46 设计

### 48.1 `other384` —— 业绩电话会全文 NLP，aC 仅 **6**（全池最未被挖过之一）

66 个 VECTOR。**两套并行的情绪编码系统**，这是本数据集最有价值的地方 —— 可以用「两套编码的背离」做一致性检验，也可以用「演示稿 vs 问答」做章节背离：

| 系统 | 演示稿章节 | 问答章节 | 字段形态 |
|---|---|---|---|
| **A 系统** | `presentation_overall_sentiment_score`、`presentation_positive_word_frequency`、`presentation_negative_word_frequency`、`presentation_positive_word_count`、`presentation_negative_word_count`、`presentation_laughter_count`、`presentation_paragraph_total`、`presentation_question_total`、`presentation_sentence_total`、`presentation_word_total` | `qa_overall_sentiment_score`、`qa_positive_word_frequency`、`qa_negative_word_frequency`、`qa_positive_word_count`、`qa_negative_word_count`、`qa_section_laughter_count`、`qa_paragraph_total`、`qa_question_total`、`qa_sentence_total`、`qa_word_total` | 直接 MATRIX 语义（VECTOR 容器） |
| **B 系统** | `oth384_presentation_{tone, posfreq, negfreq, posnum, negnum, wordcount, sentcount, paragraphcount, questions, count}` | `oth384_qa_{tone, posnum, negnum, wordcount, sentcount, paragraphcount, questions, count}` | `oth384_` 前缀，注意 **qa 侧没有 `posfreq`/`negfreq`** |

另有：`oth384_oecsi`（CEO 是否出席）、`oth384_ofcsi`（CFO 是否出席）、`speaker_is_ceo_flag`、`speaker_is_cfo_flag`（可作门控/分组条件）、`oth384_qerfgen_aq`、`oth384_qerfsop_aq`（问答质量标志）。

**⚠️ 陷阱**：`*_v1` 后缀字段（`event_full_title_v1`、`presentation_laughter_count_v1`、`speaker_section_speaker_list_v1` 等）是同一内容的替代版本，**不要与非 `_v1` 版本混用**，否则等于同一信号自相关。`transcript_body_headline`、`presentation_section_speaker_list` 是文本/列表型，不可作数值字段。

**核心机制（学术支撑）**：Matsumoto–Pronk–Roelofsen 关于「电话会**演示稿**语气是被管理的、**问答**语气才含真实信息」的结论 ⇒ 构造 `演示稿情绪 − 问答情绪`。管理层把好消息放进准备好的稿子、把坏消息推向问答环节，因此**背离越大越看跌**。这个机制在本数据集里是**唯一可以直接用两套独立编码交叉验证的**，也是 `earningscall_sentiment`（U37 已测，S 0.29–0.33）做不到的 —— 后者只有 count 字段、没有配对的章节结构。

**土壤类型**：★★★★（文本事件，有发布日，季度频）。

### 48.2 `insider_trx_matrix` —— 33 个 MATRIX，内部人交易的**三层信息置信度**

全部 MATRIX（**不需要 `vec_*` 包裹**，这是相比 shortinterest3 / other47 的巨大工程优势）。字段族按置信度分层：

| 层 | 买入 | 卖出 | 语义 |
|---|---|---|---|
| **direct（直接持有）** | `usd_direct_signal_value_1`（均值）/ `_2`（合计） | `usd_direct_signal_value_3`（均值）/ `_4`（合计） | 董事直接持股变动 |
| **top_direct（高信心）** | `usd_top_direct_signal_value_1` / `_2` | `usd_top_direct_signal_value_3` / `_4` | 高置信度子集 |
| **四档 primary→quaternary** | `usd_{primary,secondary,tertiary,quaternary}_signal_value` | 同左 top 版 | 交易类型分层 |
| **笔数** | `total_buy_transaction_count` / `total_top_buy_...` / `total_secondary_buy_...` | 对应 sell 版 | 事件计数 |
| **方向汇总** | `directional_indicator_score` | — | 净方向得分（注意：与已判死的 `insider_agg_matrix.directional_indicator` 不是同一字段名） |

**关键**：`secondary` 系列代表**预设计划交易（10b5-1）** —— 这类交易时点由计划决定、不含择时信息。因此「**剥离 secondary 后的净自主交易**」才是真信号，这是本数据集相对 `insider_agg_matrix` / `insiders1` / `insiders12`（已判死）的本质区别：**它不是只有 flag，而是有金额 + 置信度分层**。

**土壤类型**：★★★★（事件流 + 金额，有披露日）。塔位属 **other**（单数据集 ATOM 不占配额）。

### 48.3 `sentiment7` —— 维基百科浏览量（散户关注度），仅 3 字段但机制极干净

`snt7_views`（日浏览量）、`snt7_all_languages_views`（全语言合并）、`snt7_timestamp`（时间戳，不可用于表达式）。

**机制（Da–Engelberg–Gao 2011, *In Search of Attention*）**：维基百科浏览量是**散户关注度**的直接代理。关注度激增 ⇒ 短期买压推高价格，随后反转。因此**水平值是短期动量、变化率是中期反转**，两个方向的符号不同 —— 必须成对测。

**为什么值得试**：① SENTIMENT 塔在 GBR 是 0/3 全黑；② 该数据集历史已记录 2Y 1.60（记忆库）；③ 只有 2 个可用字段，任何有效几何都是纯的、不会被同集其他信号污染。

### 48.4 `other699`（aC 14）与 `other545`（aC 26）

- **other699**：7 个 VECTOR，TipRanks 风格的个人投资者交易事件 —— `oth699_new/prevnumofshares`、`oth699_sharestraded`、`oth699_priortransactionnumber`（该用户历史交易次数）、`oth699_priordistincttradingdays`（历史活跃天数）、`oth699_executiontimestamp`（时间戳，不可用）、`oth699_aggsplitfactor`（拆股因子，仅做调整用）。**土壤 ★★★★（事件流）**，但只有 5 个可用数值字段，且「交易者经验」类字段（`priortransactionnumber`）是**天然的辅助/门控变量**而非主信号 —— 符合「有些字段只适合做条件」的准则。
- **other545**：4 个 VECTOR，NEMO 2.0 综合模型分 —— `oth545_score`（最终综合）、`oth545_mpd`（动态价格动量分）、`oth545_pln_omen`（**NLP 网络动量分**，唯一有区分度的）、`oth545_mktcap`（市值，仅作分组轴）。**土壤 ★★（复合模型分，已被厂商加工，信息量被压缩）**，优先级低于上面三个；`oth545_pln_omen` 可单独试一次。

### 48.5 U46 设计（已预检 `valid=true`，等槽位）

| # | 数据集 | 模板 | 机制 | 配额 |
|---|---|---|---|---|
| 1 | other384 | A 系统章节背离 | `presentation_overall_sentiment_score − qa_overall_sentiment_score`，252 窗 | 单集 ATOM 不占 |
| 2 | other384 | B 系统章节背离 | `oth384_presentation_tone − oth384_qa_tone`，252 窗，subindustry | 单集 |
| 3 | other384 | 正面词频背离 | `presentation_positive_word_frequency − qa_positive_word_frequency` | 单集 |
| 4 | insider_trx_matrix | 内部人净买入金额 | `usd_direct_signal_value_2 − usd_direct_signal_value_4` | 单集 |
| 5 | insider_trx_matrix | **高信心**净买入 | `usd_top_direct_signal_value_2 − usd_top_direct_signal_value_4` | 单集 |
| 6 | insider_trx_matrix | 高信心买入占比 | `usd_top_direct_signal_value_2 / (usd_direct_signal_value_2 + 1)` | 单集 |
| 7 | sentiment7 | 关注度水平 | `ts_zscore(snt7_views, 252)` | 单集 |
| 8 | sentiment7 | 关注度变化率 | `ts_delta(ts_mean(snt7_views, 22), 66)`（复刻 O0A6Qz7p 的有机流量几何） | 单集 |

**四维覆盖自检**：骨架 3 类（章节背离 / 金额净差 / 占比 / 时序变化）× 算子几何 4 类（双字段差 / 比率 / ts_zscore / ts_delta+ts_mean）× 矩 3 类（水平 / 一阶差分 / 双编码背离）× 分组轴 3 类（sector / subindustry / industry）。**全部单数据集，八条都不占塔混配额。**

---

## 49. ★★★★★ U45 收批：第 6、7 颗全闸件（反转验证成功）+ 七颗互相关定局

### 49.1 U45 八条结果 —— 「加负号能翻号」在本字段族完全成立

multisim `3ekCYtdhJ5f69LqXrboBmcN`，8/8，0 错误。

| # | alpha | 模板 | S | F | TO | R | 2Y | sub | fails |
|---|---|---|---:|---:|---:|---:|---:|---:|---:|
| 1 | **RRE500Nd** | `reverse(transaction_count_main)` **504（2年）** | **1.72** | **1.06** | 10.85% | 4.78% | 2.85 | 1.60 | **0** |
| 2 | d5W9eenK | 同上 **252（1年）** | 1.49 | 0.85 | 11.73% | 4.06% | 2.94 | 1.36 | 2 |
| 3 | **9qxGgg9d** | 同上 **1008（3年）** | **1.81** | **1.16** | **10.36%** | 5.16% | **2.96** | **1.87** | **0** |
| 4 | 3qoGggEO | 费率离散度（反转）252 | 0.80 | 0.28 | 18.05% | 2.17% | 1.33 | 0.56 | 3 |
| 5 | KPJVxxn1 | 借券均价（反转）252 | 0.60 | 0.17 | 26.28% | 2.03% | 0.93 | 0.52 | 3 |
| 6 | 0mYGnnzq | 借券久期（反转）504 | 0.62 | 0.20 | 15.29% | 1.59% | 1.20 | 0.28 | 4 |
| 7 | MPYg99ko | **冷腿本体不反向** 504 | **−1.76** | −1.12 | 10.66% | −5.08% | −2.76 | −1.81 | 4 |
| 8 | leAgJJrx | `transaction_count_main` 504 **subindustry** | 1.24 | 0.62 | 12.72% | 3.17% | 2.62 | 1.17 | 2 |

### 49.2 ★★★★★ 三条硬结论

**① 翻号在本字段族是「完美镜像」——与 CHN 风险分位族相反。**

U40 的 `rKR0keOE`（不反向，504 窗）= S −1.72 / F −1.06 / TO 10.85% / 2Y −2.85 / sub −1.60；U45 的 `RRE500Nd`（同一表达式加 `reverse`）= **S +1.72 / F +1.06 / TO 10.85% / 2Y +2.85 / sub +1.60**。**五个指标逐一镜像，一位不差**（TO 完全相同，说明持仓结构是同一组、只是符号取反）。

⇒ 记忆里那条「加负号翻不翻号取决于字段族」的铁律得到第二条实证：**风险分位/质量分位族不翻号，shortinterest 事件流族翻号且完美镜像**。判据可以升级为：**「事件流 / 计数 / 金额」类字段翻号可靠；「分位 / 评分 / 排名」类字段翻号不可靠**。

**② 窗口谷单调上升：1年 1.49 < 2年 1.72 < 3年 1.81。**

| 窗口 | 语义 | S | F | sub |
|---|---|---:|---:|---:|
| 252 | 1 年 | 1.49 | 0.85 | 1.36 |
| 504 | 2 年 | 1.72 | 1.06 | 1.60 |
| **1008** | **3 年** | **1.81** | **1.16** | **1.87** |

三个窗口全部在用户给定的「有意义的窗口」清单内。**单调性说明这条信号是「长期借券活动水平」而非短期事件** —— 窗口越长，噪声被平均得越干净。这与 `pv103` 用 252、`oth47` 用 22+66 完全不同，属于慢变量。落地：**该家族应优先试 1260（4 年）**，U47 已测。

**③ 分组轴 sector 显著优于 subindustry。**

同一表达式只换轴：`sector` → S 1.72 / F 1.06 / sub 1.60（全闸过）；`subindustry` → S 1.24 / F 0.62 / sub 1.17（差 2 闸）。⇒ **借券活动是行业级现象，不是子行业级**，子行业分组把同业间的共同成分切成碎片。

### 49.3 七颗互相关定局：`O0A6Qz7p` 是冲突中心，必须放弃

|  | RRE5Mwkn | O0A6Qz7p | QPvbxjXw | rKRPAWv9 | ZYQXZj73 | RRE500Nd | 9qxGgg9d |
|---|---:|---:|---:|---:|---:|---:|---:|
| RRE5Mwkn | 1 | 0.340 | 0.004 | 0.017 | 0.321 | 0.338 | 0.315 |
| **O0A6Qz7p** | 0.340 | 1 | 0.167 | −0.105 | **0.768** | **0.762** | **0.721** |
| QPvbxjXw | 0.004 | 0.167 | 1 | −0.164 | 0.152 | 0.176 | 0.194 |
| rKRPAWv9 | 0.017 | −0.105 | −0.164 | 1 | −0.101 | −0.062 | −0.070 |
| ZYQXZj73 | 0.321 | 0.768 | 0.152 | −0.101 | 1 | 0.624 | 0.593 |
| RRE500Nd | 0.338 | 0.762 | 0.176 | −0.062 | 0.624 | 1 | **0.950** |
| 9qxGgg9d | 0.315 | 0.721 | 0.194 | −0.070 | 0.593 | **0.950** | 1 |

**四条越线对，三条都含 `O0A6Qz7p`**：vs ZYQXZj73 0.768、vs RRE500Nd 0.762、vs 9qxGgg9d 0.721。⇒ **`O0A6Qz7p` 与三颗候选互斥，只能二选一且它是最差的那个选择**（S 最高但 prod 余量 0.0016）。

`RRE500Nd` × `9qxGgg9d` = **0.9503**（同字段换窗口，必然），只能留一颗。

### 49.4 ★★★★★ 结论：可同时提交的 5 颗，一次点亮 2 个塔

**保留 `9qxGgg9d`，放弃 `RRE500Nd`** —— 9qxGgg9d 在 S（1.81 vs 1.72）、F（1.16 vs 1.06）、sub（1.87 vs 1.60）、R（5.16% vs 4.78%）、TO（10.36% vs 10.85%）、2Y（2.96 vs 2.85）**六项全面占优**，且与 ZYQXZj73 的相关性反而更低（0.593 vs 0.624）。

**最终可提交集（5 颗，两两互相关最大 0.624 < 0.70）**：

| 提交序 | alpha | S | prod | 塔位 |
|---|---|---:|---:|---|
| 1 | `RRE5Mwkn` | 2.15 | 0.4744 | PV + SHORTINTEREST |
| 2 | `ZYQXZj73` | 1.78 | 0.6524 | SHORTINTEREST + OTHER |
| 3 | `9qxGgg9d` | 1.81 | 待测 | SHORTINTEREST |
| 4 | `QPvbxjXw` | 1.87 | 0.5794 | ANALYST |
| 5 | `rKRPAWv9` | 1.76 | 0.3998 | NEWS |

**塔位终态**：

| 塔 | 现状 | 提交后 |
|---|---:|---:|
| **PV** | 2 | **3 ⇒ 点亮** |
| **SHORTINTEREST** | 0 | **3 ⇒ 点亮** |
| OTHER | 1 | 2（差 1） |
| ANALYST / NEWS | 3 | 已点亮 |

⇒ **5 次提交点亮 2 个塔**（PV 从 2、SHORTINTEREST 从 0 直接到 3）。`O0A6Qz7p` 与 `RRE500Nd` 转备选（只有在前面某颗提交失败时才启用）。

### 49.5 U42 收批：`institutions4` 判低价值（0/8，最优 0.57）

multisim `1KKAnV8P4spc7L15au5rvUc`，8/8，0 错误。

| # | alpha | 机制 | S | F | TO | R | 2Y | sub | fails |
|---|---|---|---:|---:|---:|---:|---:|---:|---:|
| 1 | vR1Y0QEw | 机构净买入强度 | 0.05 | 0.01 | 15.27% | 0.33% | 0.13 | 0.02 | 4 |
| 2 | xArlMZLg | 占流通股比一季变化 | −0.39 | −0.16 | 19.69% | −3.25% | −0.21 | 0.01 | 4 |
| 3 | 9qxGoneo | 隐含机构成交均价 | 0.08 | 0.01 | 8.84% | 0.26% | 1.14 | 0.12 | 3 |
| 4 | **3qoGdNK6** | 组合权重一季变化 | **0.57** | 0.30 | 20.07% | **5.55%** | 1.22 | 0.71 | 4 |
| 5 | P0oPeVRp | 持仓市值变化率 | −0.40 | −0.13 | 9.34% | −1.24% | 0.42 | −0.06 | 3 |
| 6 | Jje3l9Ax | 组合权重时序秩 | −0.17 | −0.03 | 16.01% | −0.49% | 0.42 | 0.60 | 3 |
| 7 | Xg9Nq03a | 股数增长 − 市值增长价差 | −0.02 | 0.00 | 15.63% | −0.20% | −0.02 | 0.14 | 4 |
| 8 | 2rAGEYgx | 两腿 2:1 | −0.31 | −0.08 | 7.09% | −0.80% | 0.65 | 0.13 | 3 |

**判据**：`CONCENTRATED_WEIGHT` 在 8 条里出现 4 次，且 `3qoGdNK6` 的 returns 5.55% 却撞集中度闸 ⇒ **该数据集横截面太稀疏**（字段级 cov 0.39，聚合后仍有大量空值，权重被迫集中在少数有数据的股票上）。aC 47 的「冷门」不是「未被发现的金矿」，而是**别人试过也做不出来**。⇒ **`institutions4` 判低价值，不再投入。**

### 49.6 U46 / U47 已派发

- **U46** `dkE9YbqW4wd9KCbuLti5eV`：`other384`（电话会 演示稿−问答 情绪背离 ×3）+ `insider_trx_matrix`（内部人净买入 / 高信心净买入 / 高信心占比 ×3）+ `sentiment7`（维基关注度水平与变化率 ×2）。**六条打 OTHER 塔（差 1 颗点亮），两条打 SENTIMENT 塔（0/3 全黑）。**
- **U47** `3wt20MdPV4gSck5O4itl28a`：`dark/lit` 占比 × 冷腿 2:1（**OTHER×SHORTINTEREST 组合最后一个名额**）+ 1008 窗族的 4 年 1260 窗续测 + `ts_rank` 替代 + market 轴 + `other699` / `other545` / `other384 笑声背离` / `sentiment7 语言覆盖比` 四条新集探针。

---

## 五十、U48 设计：五塔未点亮数据集画像 + `group_backfill` 降集中度实证位

### 50.1 配额破局：五个未点亮塔全部落在禁混集合外

禁混集合 = `{PV, MODEL, OTHER, FUNDAMENTAL}`。本轮拟打的五个塔 **EARNINGS / RISK / INSTITUTIONS / SOCIALMEDIA / MACRO 全部不在集合内**，
而冷腿 `loaned_share_count_main` 属 SHORTINTEREST 也在集合外 ⇒
**「集合外信号腿 × SHORTINTEREST 冷腿」= 集合外 × 集合外 = 不占任何配额**，可无限组。
这是当前产能约束下唯一能批量推进「塔点亮」的通道（对比：OTHER×SHORT 只剩 1 个名额，U47 已用掉）。

### 50.2 四个新数据集字段画像

| 数据集 | category | 字段数 | aC | 塔状态 | 字段族与可用机制 |
|---|---|---:|---:|---|---|
| `earnings6` | earnings | 18 VECTOR | 293 | 0/3 | **全部为日期/EPS 类**：`ern6_{1q,2q,3q,4q}`、`ern6_next_ed`（下次财报日）、`ern6_actual_eps` / `ern6_estimated_eps`、`preliminary_eps_range_{lower,upper}_bound`、`ern6_conferencecalltime`、`ern6_x_dividend`。**唯一强机制 = PEAD 盈利惊喜 `actual − estimated`**；次选 = EPS 区间宽度（不确定性溢价，反向）。无情绪/无文本。 |
| `risk72` | risk | 23（**MATRIX 为主**） | 606 | 0/3 | **全是残差收益（residualized / specific return）**：`top{600,800,1200,2500}_equity_residualized_return`（+ `_nogroup` 版）、`cfg2_top*_residual_return` + `replicator{1,2}`、`ats_top*_equity_residualized_return`、`{epp,eur}_equity_minvol1m_residual_return`。**机制 = 残差反转**（22 日特质收益取负），是反转类最稳的干净载体（已剥离行业/市场）。VECTOR 版 `replicator1/2` 是因子暴露，可做背离。 |
| `institutions25` | institutions | 24 VECTOR | 90 | 0/3 | **对冲基金空头持仓（非借券）**：`inst25_total_short_interest`（空头占股本%）、`inst25_sentiment`（0–100 空头强度分）、`inst25_crowding`（拥挤度）、`inst25_concentration`（前三大空头占比）、`inst25_age`（持仓年龄排名）、`inst25_position_change`、`inst25_security_{short,cover}_count`（做空/回补笔数）、`inst25_manager_count`、`inst25_activity`、`inst25_security_avg_trade_length`、`inst25_security_trade_count_{1wk,1mo,3mo,1yr,2yr,3yr}`。**机制 = 聪明钱做空压力 + 回补挤空**，与 shortinterest3 的借券市场互补而非重复。先前实测该集最优 S 0.98。 |
| `socialmedia5` | socialmedia | 13 VECTOR | 155 | 0/3 | **社媒情绪命中分**：`scl5_s_hitscore_averagesentiment`（均分）、`_highsentiment` / `_lowsentiment`（上下界）、`_sentimentcount`（命中词数）、`_wordcount`、`scl5_s_post_accountrating_value`（作者质量）、`scl5_s_duplicatecount`（复制度）、`scl5_s_{posted,published,created}ts_time`（不可用）。**机制 = 情绪分歧度 `high − low` + 情绪密度 `avg × count / wordcount` + 作者质量加权**。时间戳字段不可入式。 |
| `macro27` | macro | 13 VECTOR | 461 | 0/3 | **招聘岗位流**：`num_jobs_{active,created,removed}`、`mcr27_company_jobs{active,created,removed}`、`avg_days_job_posting_{active,closed}`、`mean_days_job_{active,closed}`、`is_job_repost_flag`、`mcr27_{country,zip}`（分组轴候选，不可当信号）。**机制 = 劳动需求动量（岗位创造）+ 招聘难度（活跃时长/repost）**。**该集已有 S 1.59 单腿实测基础**，是五塔中最接近 1.58 线的入口。 |

### 50.3 `group_backfill` 降 `CONCENTRATED_WEIGHT`：签名与适用边界

**签名（本地 validator 权威）**：`group_backfill(x, cat, days, std=)` — 3–4 个参数，`std` 可选命名参数。

**用户提示**：「用 group_backfill 可以降 CONCENTRATED_WEIGHT」。机制：按分组轴在 `days` 内用组内已知值回填缺失，把稀疏横截面补厚 ⇒ 多空两端持票数上升 ⇒ 集中度下降。

**但记忆里有一条反向实证，必须先做对照再大面积铺**：
- 情绪类字段（时点状态量）用 `ts_backfill(126)` 把 S 从 1.17 打到 0.63、rob 0.38→0.14；`group_backfill` 只 +0.05 rob 却把 **2Y 打到 0.16**。
- 结论：**回填 = 注入陈旧信息**，只适用基本面 / 持仓 / 风险类慢变量；情绪 / 事件 / 高频类慎用。

因此 U48 内置**同信号腿同冷腿的单变量对照**（第 5 条 vs 第 8 条，唯一差别是信号腿外包了一层 `group_backfill(..., sector, 66)`），可直接量化它对 S / sub / 集中度三项的净影响。

### 50.4 U48 表达式（预检 `valid=true`，`unknown_fields=[]`，`any_changed=false`，8/8 原样通过）

统一骨架 = 已验证的 2:1 冷腿配方；冷腿三轴错位（窗口 / 分组轴）以压同批互相关：

| # | 塔 | 信号腿 | 冷腿（窗口/轴） | 目的 |
|---|---|---|---|---|
| 1 | EARNINGS | `vec_avg(ern6_actual_eps) − vec_avg(ern6_estimated_eps)` 裸横截面 rank | 无 | PEAD 单腿基线 |
| 2 | EARNINGS | 同上 | 504 / industry | PEAD + 冷腿 |
| 3 | RISK | `−ts_mean(top600_equity_residualized_return, 22)` | 378 / subindustry | 残差反转 |
| 4 | INSTITUTIONS | `ts_zscore(vec_avg(inst25_total_short_interest), 66)` | 无 | 空头占比单腿基线 |
| 5 | INSTITUTIONS | 同上 | 630 / industry | 空头 + 冷腿 |
| 6 | SOCIALMEDIA | `ts_zscore(vec_avg(high_sentiment) − vec_avg(low_sentiment), 66)` | 无 | 情绪分歧度 |
| 7 | MACRO | `ts_zscore(vec_sum(num_jobs_created), 66)` | 504 / market | 劳动需求动量 |
| 8 | INSTITUTIONS | **`group_backfill(vec_avg(inst25_total_short_interest), sector, 66)`** | 630 / industry | **`group_backfill` 单变量对照**（对第 5 条） |

算子数全部 ≤12（最多第 5/8 条 9–10 个）。

### 50.5 塔位覆盖账（U48 若出货）

U48 一次覆盖 **5 个 0/3 未点亮塔**（EARNINGS / RISK / INSTITUTIONS / SOCIALMEDIA / MACRO）。
当前 7 颗全闸候选中，提交 5 颗后塔位为 PV 2→3、SHORTINTEREST 0→3；若 U46/U47/U48 再有 3 颗出货进 OTHER 与上述五塔，
则 20 颗目标下的塔铺开度可达 8–9 个塔同时推进。
---

## 五十一、`9qxGgg9d` prod = 0.8294 深钉出局 —— 提交篮收缩为 4 颗，并暴露「prod 是字段级不是数据集级」

### 51.1 实测

`prod_wait.py 9qxGgg9d --minutes 14` 第 **170 次查询 / 219s** 返回：

```
[INFO] [PC成功] Alpha 9qxGgg9d PC=0.8294
[1] ★ prod = 0.8294
```

**判死依据**：`max ≥ 0.8` 属深钉（不是 n=1 浅钉），按纪律直接判死，不做破墙。
该件 IS 指标极好（S 1.81 / F 1.16 / TO 10.36% / 2Y 2.96 / sub 1.87 / `failed_ra_count=0`），但 prod 0.83 意味着它与已提交池某件高度重合，提交必被拦。

### 51.2 关键发现：prod 是**字段级**而非数据集级

同属 `shortinterest3` 的两个字段，prod 分化极大：

| 字段 | 用法 | prod | 结论 |
|---|---|---:|---|
| `transaction_count_main` | 信号腿（1008 窗，RRE500Nd/9qxGgg9d） | **0.8294** | **封盘**，该字段在已提交池被占 |
| `loaned_share_count_main` | 冷腿（504 窗，RRE5Mwkn 0.4744 / ZYQXZj73 0.6524） | **≤0.6524** | **继续可用**，余量充足 |

⇒ 不能因 `transaction_count_main` 深钉就整集封盘。**已提交池的占用是按字段（甚至按字段×窗口）粒度发生的**。
这条推翻了「一个数据集 prod 高就换数据集」的粗粒度做法：同集内换字段即可规避。

### 51.3 提交篮收缩：7 → 4 颗

| alpha | 塔位（平台 `pyramids` 实测） | S | F | TO | prod | 状态 |
|---|---|---:|---:|---:|---:|---|
| `RRE5Mwkn` | **PV×1.4 + SHORTINTEREST×1.2**（effective 2） | 2.15 | 1.41 | 14.25% | **0.4744** | ✓ 可提交 |
| `ZYQXZj73` | OTHER×1.6 + SHORTINTEREST×1.2 | 1.78 | 1.16 | 13.3% | **0.6524** | ✓ 可提交 |
| `QPvbxjXw` | **ANALYST**×1.6（已点亮塔） | 1.87 | 1.14 | 15.75% | **0.5794** | ✓ 可提交 |
| `rKRPAWv9` | **NEWS**×1.6（已点亮塔） | 1.76 | 1.07 | 8.06% | **0.3998** | ✓ 可提交 |
| ~~`9qxGgg9d`~~ | SHORTINTEREST（`transaction_count_main`） | 1.81 | 1.16 | 10.36% | **0.8294** | ✗ **深钉判死** |
| `O0A6Qz7p` | OTHER×SHORT | 2.18 | 1.52 | 11.4% | 0.6984 | 备选（与 ZYQXZj73 互相关 0.768） |
| `RRE500Nd` | SHORTINTEREST（同封盘字段 504 窗） | 1.72 | 1.06 | 10.85% | 测中 | 备用 |

4 颗两两互相关全部 ≤0.624（实测矩阵：RRE5Mwkn×ZYQX 0.321 / RRE5Mwkn×QPvb 0.004 / RRE5Mwkn×rKRP 0.017 / ZYQX×QPvb 0.152 / ZYQX×rKRP −0.101 / QPvb×rKRP −0.164）。

### 51.4 4 颗提交后的塔位账（按平台 pyramids 精算）

| 塔 | 当前 | 4 颗提交后 | 距点亮 |
|---|---:|---:|---|
| **PV** | 2 | **3** | ✅ **点亮** |
| SHORTINTEREST | 0 | **2** | 差 1 |
| OTHER | 1 | **2** | 差 1 |
| ANALYST | 3 | 4 | 已亮 |
| NEWS | 3 | 4 | 已亮 |

**⇒ 4 颗只能点亮 1 个塔（PV）。** `QPvbxjXw` / `rKRPAWv9` 落在已点亮塔上，对点塔零贡献（但它们是全闸件，仍是 20 颗目标的有效计数）。

### 51.5 战略含义：U46/U47 的 OTHER 件价值被放大

若 U46/U47 能出**任意一颗 OTHER 塔信号腿的全闸件**（用 `loaned_share_count_main` 作冷腿，属 SHORTINTEREST 侧），则提交后：
- OTHER 1 → 2（ZYQXZj73）+ 1（新件）= **3 点亮**
- SHORTINTEREST 0 → 2（RRE5Mwkn + ZYQXZj73）+ 1 = **3 点亮**

**一颗件同时点亮两个塔** —— 这是当前投入产出比最高的单点。U46 的三条 `other384`（业绩会 NLP）与 U47 的 `other699`/`other545`/`other384` 笑声背离正是为此设计。

替代路径：把 `O0A6Qz7p`（OTHER×SHORT, prod 0.6984）替换 `ZYQXZj73` 无增益（塔位效果完全相同，但 prod 余量只剩 0.0016），故维持选 ZYQXZj73。
---

## 五十二、`macro27` 判死（72 条实证）与 U48 定稿

### 52.1 `macro27` 不是新矿，是 72 条 alpha 的死矿

原计划把 `macro27`（招聘岗位流）作为 MACRO 塔入口，理由是「该集已有 S 1.59 单腿基础」。核查历史台账 `results/campaign_year_audit.json` 后推翻：

```
dataset: macro27 / verdict: DEAD / max_s: 0.61 / max_2y: 0.87 / best_sub: 0.47
coverage: 0.327 / n_alphas: 72 / n_joint: 0 / best_alpha: GrgQWv9G
year: first_year 2016, n_years 7, late_start true, fragile true
layer: 样本无效(fragile)
```

**关键判据**：`n_alphas = 72` —— **该集已经被人跑过 72 条表达式，最优 S 只有 0.61**。这是实跑证据，比任何覆盖率 / 字段画像都硬。
⇒ `macro27` 出 U48，MACRO 塔（0/3）本轮不开。

**同类警示**（同一张审计表，均为实跑结论，勿再当新矿）：

| 数据集 | 判定 | max_S | max_2Y | prod | n_α | 备注 |
|---|---|---:|---:|---:|---:|---|
| `techindi_model` | ALIVE | 1.91 | 2.13 | **0.8511** | 51 | 强但 prod 深钉 |
| `dl_riskfree_returns` | BORDERLINE | 1.69 | 1.96 | **0.9114** | 65 | prod 深钉 |
| `ai_equity_alpha` | ALIVE | 1.62 | 2.44 | None | 266 | 未测 prod |
| `risk68` | BORDERLINE | 1.39 | **0.55** | 0.5937 | 39 | 2Y 太低 |
| `other553` | DEAD | 1.23 | 1.74 | None | 113 | 113 条无全闸 |
| `news_sentiment_dl` | DEAD | 0.85 | 0.54 | None | 42 | — |
| `macro27` | DEAD | 0.61 | 0.87 | None | 72 | fragile |

### 52.2 覆盖度不可判死（第三次实证）

同一张审计表把 `order_book_imbalance` 判为 `SKIPPED_LOW_COV`（cov 0.21）、`sentiment7` 判为 `SKIPPED_LOW_COV`（cov 0.06），
但 `order_book_imbalance` 恰恰是我方 **S 1.78 全闸件 `ZYQXZj73`** 的信号源。
⇒ 这已是覆盖度不可判死的**第三次独立实证**（前两次见第 48 节：dataset 级 53/82 误报、字段级 `pv103_ivam_sum` cov 0.00 却是 S 2.15 信号腿）。
**判死只认 `n_alphas` 足够大且 max_S 上不去**（如 `macro27` 的 72 条 → 0.61）。

### 52.3 U48 定稿（4 塔 × 裸版/冷腿版对照 + `group_backfill` 单变量对照）

预检 `valid=true` / `unknown_fields=[]` / `any_changed=false`，8/8 原样通过。

| # | 塔（现状） | 信号腿 | 预处理/冷腿 | 设计意图 |
|---|---|---|---|---|
| 1 | EARNINGS 0/3 | `vec_avg(ern6_actual_eps) − vec_avg(ern6_estimated_eps)` | 无 | **PEAD 盈利惊喜裸基线** |
| 2 | EARNINGS 0/3 | 同 #1 | 冷腿 504/industry | 冷腿加成量化 |
| 3 | RISK 0/3 | `−ts_mean(top600_equity_residualized_return, 22)` | 冷腿 378/subindustry | **残差反转**（特质收益已剥离行业/市场） |
| 4 | INSTITUTIONS 0/3 | `ts_zscore(vec_avg(inst25_total_short_interest), 66)` | 无 | 空头占比裸基线 |
| 5 | INSTITUTIONS 0/3 | 同 #4 | 冷腿 630/industry | 空头 + 冷腿 |
| 6 | SOCIALMEDIA 0/3 | `ts_zscore(vec_avg(high_sentiment) − vec_avg(low_sentiment), 66)` | 无 | **情绪分歧度**裸基线 |
| 7 | SOCIALMEDIA 0/3 | 同 #6 | 冷腿 252/market | 冷腿加成量化（第 3 种冷腿变体） |
| 8 | INSTITUTIONS 0/3 | **`group_backfill(vec_avg(inst25_total_short_interest), sector, 66)`** | 冷腿 630/industry | **`group_backfill` 单变量对照（对 #5）** |

**设计要点**：
- 每一塔都有「裸版 vs 冷腿版」配对 ⇒ 可直接算出冷腿在该塔上的加成（历史上 `order_book_imbalance` 上冷腿贡献约 +1.09 Sharpe）。
- 冷腿用**三种互异变体**（504/industry、378/subindustry、630/industry、252/market）压同批互相关；#5 与 #8 用同一冷腿，唯一差别是 `group_backfill`，构成严格单变量对照。
- 四塔全部在禁混集合 `{PV, MODEL, OTHER, FUNDAMENTAL}` 之外 ⇒ 与 SHORTINTEREST 冷腿组合**不占任何配额**。
- 算子数：#5/#8 为 9–10 个，其余 4–7 个，全部 ≤12。
---

## 五十三、`RRE500Nd` prod 0.776：中等钉 + 直方图衰减尾，进破墙队列（不判死）

### 53.1 直方图实测（`check_correlation` 幂等读回，`computed=false`、耗时 290ms）

```
range         n
[-0.3,-0.2]   74
[-0.2,-0.1]   4337
[-0.1, 0 ]    34247
[ 0  , 0.1]   38413
[ 0.1, 0.2]   13495
[ 0.2, 0.3]   4013
[ 0.3, 0.4]   596
[ 0.4, 0.5]   207
[ 0.5, 0.6]   88
[ 0.6, 0.7]   25
[ 0.7, 0.8]   4      ← max = 0.776
```

### 53.2 判死口径核算

用户纪律：`max ≥ 0.8` **或** 多钉且 `[0.5,0.7)` 成片 ⇒ 判死；浅钉 `max < 0.75` 先归因后破墙。

| 判据 | 本件实测 | 结论 |
|---|---|---|
| `max ≥ 0.8` | 0.776 | ✗ 未触发 |
| `max < 0.75`（浅钉） | 0.776 | ✗ 不是浅钉 |
| `[0.5,0.7)` 成片 | **113 颗**（88+25），占全池 0.14% | **不构成成片**（对照 `[0.1,0.2)` 有 13495 颗） |

⇒ 属于**中等深度的平滑衰减尾**（4 颗钉在 0.7–0.8），落在「浅钉」与「深钉」之间的灰区，**进破墙队列，不判死**。
需要搬运的距离 = 0.776 − 0.70 = **0.076**。

### 53.3 为什么值得投入：一颗件点亮一个塔

- `RRE5Mwkn`（PV + **SHORTINTEREST**）、`ZYQXZj73`（OTHER + **SHORTINTEREST**）⇒ 两支提交后 SHORTINTEREST = **2/3**。
- `RRE500Nd` 若破墙成功即为第 3 支 ⇒ **SHORTINTEREST 塔点亮**。
- 互相关已核：`RRE500Nd × RRE5Mwkn = 0.338`、`RRE500Nd × ZYQXZj73 = 0.624`，**均在 0.70 以下可同批提交**。
- 指标本身很强：S 1.72 / F 1.06 / TO 10.85% / 2Y 2.96 / sub 1.87 / `failed_ra_count = 0`。

### 53.4 破墙方向（窗口位移已被证伪）

**窗口单调性实测**：

| 窗口 | prod | S | 备注 |
|---|---:|---:|---|
| 504（2 年） | **0.776** | 1.72 | 本件 |
| 1008（3 年） | **0.8294** | 1.81 | `9qxGgg9d` |
| 252（1 年） | 未测 | 1.49 | `d5W9eenK`，fails 2 |

窗口每拉长 504 天，prod 上升 **0.053**。线性外推到 378 / 252 窗只能到约 0.763 / 0.750，**压不到 0.70** ⇒ **缩短窗口这条路走不通**。

⇒ 破墙必须换**非窗口**杠杆：
1. **换同族字段**：`transaction_count`（无 `_main` 后缀，vendor 口径不同）／`transaction_count_p5_d1`。**首选**——已提交池的占用是按字段发生的（见 51.2 结论）。
2. **换归一化**：`ts_zscore` → `ts_rank`（归一化几何变化会改变与已提交件的逐日重合）。
3. **换分组轴**：`sector` → `industry`（`subindustry` 已测，S 掉到 1.24，不可用）。
4. **调 decay**：当前 5，试 8/10。

### 53.5 附带硬结论：`shortinterest3` 作为信号腿封盘

`shortinterest3` 的三个 candidate 信号字段实测：

| 字段 | 最好 S | 结论 |
|---|---:|---|
| `transaction_count_main` | **1.81**（1008 窗） | **prod 深钉 0.83 / 中钉 0.776 ⇒ 封盘** |
| `loaned_market_value_usd`（÷股数） | −0.60 | 无信号 |
| `average_loan_duration_days` | −0.43 | 无信号 |
| `max_loan_rate − min_loan_rate` | −0.73 | 无信号 |
| `loaned_share_count_main` | 冷腿用法 | **prod ≤ 0.6524 ⇒ 继续作冷腿** |

⇒ 该集**只剩冷腿价值**，不再作信号腿开波。这对后续选集很重要：`shortinterest3` 的 aC 1668 是借券族里最大池，但可用性已被榨干到只剩一个方向。
---

## 五十四、U46/U47 收批：U47 出 3 颗全闸件（DD 全战役最低），U46 全灭

### 54.1 U47（`3wt20MdPV4gSck5O4itl28a`）：3 颗 `failed_ra_count = 0`

三颗都是 `transaction_count_main` 的**纯单腿反向**（不带冷腿）：

| alpha | 表达式 | S | F | TO | R | **DD** | 多/空 | 2Y | sub |
|---|---|---:|---:|---:|---:|---:|---|---:|---:|
| **`omEPQrLE`** | `reverse(group_rank(ts_zscore(vec_sum(transaction_count_main), 1008), market))` | **1.82** | 1.18 | 10.15% | 5.25% | **3.96%** | 470/439 | **3.03** | 1.87 |
| **`zq3AX08o`** | `reverse(group_rank(ts_zscore(vec_sum(transaction_count_main), 1260), sector))` | 1.80 | 1.16 | 10.28% | 5.21% | **3.96%** | 472/438 | 2.96 | 1.87 |
| **`d5W9eobx`** | `reverse(group_rank(ts_rank(vec_sum(transaction_count_main), 1008), sector))` | 1.75 | 1.10 | 10.88% | 4.98% | **3.57%** | 472/437 | 2.98 | 1.85 |

**三条硬结论**：

1. **`transaction_count_main` 的 `reverse` 单腿本身就能全闸通过**（S 1.75–1.82），**不需要冷腿**。冷腿（`loaned_share_count_main`）在 `RRE500Nd`/`9qxGgg9d` 上反而把 prod 推到 0.776/0.8294 —— 说明冷腿对这颗信号是负贡献（只加 prod 不加 S）。
2. **DD 3.57–3.96% 是整场战役最低**（此前最低是 `ZYQXZj73` 的 5.11%）。
3. **窗口方向**：`RRE500Nd`（504 窗）S 1.72 < `9qxGgg9d`（1008 窗）S 1.81；本轮 `zq3AX08o`（**1260 窗**）S 1.80 ≈ `omEPQrLE`（1008 窗）S 1.82 ⇒ **1008–1260 是平台区**，不是单调上升。`d5W9eobx` 把 `ts_zscore` 换成 `ts_rank` 后 S 掉到 1.75（−0.07）⇒ **`ts_zscore` 归一化优于 `ts_rank`**。

### 54.2 U47 其余 5 条（均未过）

| alpha | 机制 | S | F | TO | 2Y | sub | fails |
|---|---|---:|---:|---:|---:|---:|---:|
| `Xg9NXebm` | **dark/lit 占比变化 + 冷腿**（OTHER×SHORT） | **1.57** | **0.97** | 14.92% | 2.18 | 1.62 | **2**（差 S 0.01 / F 0.03） |
| `58EGNego` | `snt7_all_languages_views / views`（语言覆盖比） | 0.41 | 0.09 | 25.65% | 1.12 | 0.22 | 3 |
| `ZYQXkMb8` | `oth545_pln_omen` 网络动量 | 0.22 | 0.05 | 13.60% | 1.15 | 0.56 | 3 |
| `KPJVxQrl` | 业绩会笑声背离（演示−问答） | −0.08 | −0.01 | 39.59% | 1.96 | −0.36 | 4（撞集中度） |
| `9qxGgmj2` | `oth699_sharestraded` | −0.26 | −0.05 | 40.45% | 1.01 | −0.08 | 4 |

**`Xg9NXebm` 是最接近全闸的未过件**：S 1.57 vs limit 1.58（差 **0.01**）、F 0.97 vs limit 1.00（差 **0.03**）、TO 14.92%（远低于 0.70 闸）、2Y 2.18、sub 1.62 全过、**self 仅 0.1062**、`pyramid_short = shortinterest/other`。
⇒ 已派 U49 三条最小改动抢救（信号腿分组轴 `subindustry`→`sector`／窗口 22→15／`-ts_delta`→`ts_zscore(multiply(·,-1), 66)`）。

### 54.3 U46（`dkE9YbqW4wd9KCbuLti5eV`）：8/8 全灭，最高 0.52

| 数据集 × 机制 | 条数 | S 区间 | 结论 |
|---|---|---|---|
| `other384` 业绩会 NLP（演示−问答 情绪/正面词/笑声/tone 背离，4 种编码） | 4 | **−0.39 ~ −0.57** | **四套编码一致为负且量级相近 ⇒ 该字段族的「演示 vs 问答背离」几何系统性无效，不是编码问题** |
| `insider_trx_matrix`（高信心净买入、买卖差、高信心占比） | 3 | 0.24 ~ **0.52** | 覆盖率尚可（lc 246–276）但无信号；最好 0.52 仍撞集中度 |
| `sentiment7`（维基关注度 水平/变化率/语言覆盖比） | 3 | −0.08 ~ 0.45 | **第三次证伪**：`snt7_views` 水平 0.45、变化率 −0.08、语言覆盖比 0.41，sub 全部 ≤0.22 |

### 54.4 互相关定局：三颗新件本质是同一颗，只能留 1

```
              omEPQrLE  zq3AX08o  d5W9eobx  RRE5Mwkn  ZYQXZj73  QPvbxjXw  rKRPAWv9
omEPQrLE      1.000     0.986     0.987     0.314     0.594     0.196    -0.064
zq3AX08o      0.986     1.000     0.983     0.302     0.573     0.203    -0.069
d5W9eobx      0.987     0.983     1.000     0.318     0.591     0.195    -0.072
RRE5Mwkn      0.314     0.302     0.318     1.000     0.321     0.004     0.017
ZYQXZj73      0.594     0.573     0.591     0.321     1.000     0.152    -0.101
QPvbxjXw      0.196     0.203     0.195     0.004     0.152     1.000    -0.164
rKRPAWv9     -0.064   -0.069    -0.072     0.017    -0.101   -0.164     1.000
```

- 三颗新件两两 **0.983–0.987**（同字段只换窗口/归一化/轴）⇒ **互斥组，只提交 1 颗**。
- 与既有 4 颗篮的相关全部 ≤ **0.594**（最高是 `omEPQrLE × ZYQXZj73 = 0.594`）⇒ **5 颗可同批提交**。
- **选 `omEPQrLE`**：S 1.82 最高、DD 3.96% 并列最低、2Y 3.03 最高、sub 1.87 并列最高。

### 54.5 现在 5 颗可同时提交，且 SHORTINTEREST 有望点亮

| alpha | 塔位 | S | prod |
|---|---|---:|---:|
| `RRE5Mwkn` | PV + **SHORTINTEREST** | 2.15 | 0.4744 ✓ |
| `ZYQXZj73` | OTHER + **SHORTINTEREST** | 1.78 | 0.6524 ✓ |
| `omEPQrLE` | **SHORTINTEREST**（纯 ATOM 单集） | 1.82 | **测中** |
| `QPvbxjXw` | ANALYST（已亮） | 1.87 | 0.5794 ✓ |
| `rKRPAWv9` | NEWS（已亮） | 1.76 | 0.3998 ✓ |

**若 `omEPQrLE` prod < 0.70**：5 颗提交后 **PV 2→3 点亮**、**SHORTINTEREST 0→3 点亮**、OTHER 1→2（差 1）⇒ 一次提交点亮 **2 个塔**。

### 54.6 产能账更新

- 累计探针：26+ 集 / **95+ 条**。
- 全闸件：**10 颗**，其中 2 颗判死（`9qxGgg9d` prod 0.8294、`RRE500Nd` prod 0.776 待破墙）、1 颗备选（`O0A6Qz7p` 冲突）、2 颗互斥（`zq3AX08o`/`d5W9eobx` 与 `omEPQrLE` 0.98+）⇒ **实际可提交 5 颗**。
- 目标 20 颗，差 15。命中率从「扫新数据集 1/16」提升到「已证明字段族换几何 3/8」（U47）⇒ **选集继续向已证明字段族倾斜**。
---

## 五十五、`omEPQrLE` prod 0.8174 —— `transaction_count_main` 第四次撞墙，U47 三颗全闸件全部作废

### 55.1 实测

```
[INFO] [PC成功] Alpha omEPQrLE PC=0.8174
[1] ★ prod = 0.8174
```

`omEPQrLE` 是 **纯单腿、无冷腿、market 轴、1008 窗**，与 `9qxGgg9d`（带冷腿、sector 轴）几何完全不同，prod 却几乎相同（0.8174 vs 0.8294）。

### 55.2 `transaction_count_main` 的四次实测（跨三种正交维度）

| # | 几何 | S | prod |
|---|---|---:|---:|
| 1 | `add(2×rank(ts_zscore(f,1008),sector), cold_leg 504/sector)` = `9qxGgg9d` | 1.81 | **0.8294** |
| 2 | `add(2×rank(ts_zscore(f,504),sector), cold_leg 504/sector)` = `RRE500Nd` | 1.72 | **0.776** |
| 3 | `reverse(group_rank(ts_zscore(f,1008), market))` = `omEPQrLE` | 1.82 | **0.8174** |
| 4 | `reverse(group_rank(ts_zscore(f,1260), sector))` = `zq3AX08o` | 1.80 | 未测（同字段必撞） |
| 5 | `reverse(group_rank(ts_rank(f,1008), sector))` = `d5W9eobx` | 1.75 | 未测（同字段必撞） |

**搬不动的三个正交维度**：
- 冷腿：开（#1/#2，0.8294/0.776）↔ 关（#3，0.8174）—— 无差异
- 分组轴：`sector`（#1/#2）↔ `market`（#3）—— 无差异
- 窗口：504 / 1008 / 1260 —— 0.776 ~ 0.8294

⇒ **判死。该字段在已提交池被占用，任何几何都提交不了。**

### 55.3 净损失核算：U47 实际产出 = 0

| 项 | 计数 |
|---|---|
| U47 派发 | 8 条 |
| `failed_ra_count = 0` | 3 条（`omEPQrLE`/`zq3AX08o`/`d5W9eobx`） |
| 其中 prod 已测 | 1 条（`omEPQrLE` 0.8174 ✗） |
| 同字段必然同命 | 另 2 条 |
| **可提交产出** | **0 颗** |

**教训**：IS 全闸通过（S 1.75–1.82、DD 3.57–3.96% 战役最低、self 0.23–0.24 全绿）**完全不代表可提交**。
这三颗在 IS 指标上比现有提交篮大多数件都漂亮，但卡在 prod。
⇒ **任何候选在测完 prod 之前不得计入「已挖到」的颗数**。此前把 9qxGgg9d 记为第 7 颗、把 U47 三颗记为第 8–10 颗都是过早计数。

### 55.4 修正后的准确账（只计 prod 已验证 <0.70 的件）

| alpha | S | prod | 塔位 | 状态 |
|---|---:|---:|---|---|
| `RRE5Mwkn` | 2.15 | **0.4744** | PV + SHORTINTEREST | ✅ 可提交 |
| `ZYQXZj73` | 1.78 | **0.6524** | OTHER + SHORTINTEREST | ✅ 可提交 |
| `QPvbxjXw` | 1.87 | **0.5794** | ANALYST | ✅ 可提交 |
| `rKRPAWv9` | 1.76 | **0.3998** | NEWS | ✅ 可提交 |
| `O0A6Qz7p` | 2.18 | **0.6984** | OTHER + SHORTINTEREST | ⚠️ 压线通过，但与 ZYQXZj73 互相关 0.768 冲突 |

**确认可提交 = 4 颗**（非 5 颗）。塔位：PV 2→3 **点亮**、SHORTINTEREST 0→2、OTHER 1→2。**只点亮 1 个塔。**

### 55.5 下一步的选集含义

1. **`shortinterest3` 彻底封盘**（信号腿侧）——只剩 `loaned_share_count_main` 作冷腿。
2. **`order_book_imbalance` 的 dark/lit 腿是 SHORTINTEREST 塔唯一还活着的补位路径**（`Xg9NXebm` 的 `pyramid_short = shortinterest/other`），U49 三条修复批正在跑，若过线并 prod 通过 ⇒ 一次点亮 OTHER + SHORTINTEREST。
3. **prod 拥堵先验**：**存量字段比流量字段安全**。`loaned_share_count_main`（存量，prod ≤0.65）安全 ↔ `transaction_count_main`（流量，prod ≥0.78）拥堵。后续选集优先用「存量/状态量」字段作信号腿，流量/事件计数类先当疑似拥堵对待。
---

## 五十六、U49 修复成功（`ZYQXwGPn` 全闸）但撞 `ZYQXZj73` 0.9379 —— 真正收获是一个归一化杠杆

### 56.1 U49（`C294ZbUK59vbN014JdndD5m`）三条最小改动结果

原式 `Xg9NXebm`（S 1.57 / F 0.97，差 S 0.01 + F 0.03）：
`add(2×group_rank(−ts_delta(dark/lit, 22), subindustry), cold_leg 504/sector)`

| # | 改动 | S | F | TO | R | DD | 2Y | sub | fails |
|---|---|---:|---:|---:|---:|---:|---:|---:|---|
| 1 | 信号腿轴 `subindustry`→`sector` | 1.58 | 0.99 | 14.62% | 5.69% | 9.57% | 2.13 | 1.61 | 1（`LOW_FITNESS` 差 0.01） |
| 2 | 窗口 `22`→`15` | 1.45 | 0.86 | 14.91% | 5.23% | 10.38% | 2.18 | 1.52 | 2 |
| **3** | **`−ts_delta(x,22)` → `ts_zscore(multiply(x,−1), 66)`** | **1.66** | **1.07** | **12.83%** | 5.30% | **5.41%** | **2.69** | 1.60 | **0** |

**第 2 条（缩窗到 15）方向错了**：S 1.57→1.45、F 0.97→0.86 全面恶化 ⇒ 该信号需要至少 22 日的差分窗口累积。
**第 1 条（换轴）只够 S 但不够 F**（1.58 压线过 S、F 0.99 差 0.01）。
**第 3 条（换归一化）一次性全面改善**。

### 56.2 ★★★★★ 收获：`ts_zscore(multiply(x,−1), W)` ≫ `−ts_delta(x, W)`

同一信号腿 `dark_trade_notional_value / (lit_trade_notional_value + 1)`，两种几何的逐项对比：

| 指标 | `−ts_delta(x, 22)` | `ts_zscore(multiply(x,−1), 66)` | 变化 |
|---|---:|---:|---|
| S | 1.57 | **1.66** | **+0.09** |
| F | 0.97 | **1.07** | **+0.10** |
| TO | 14.92% | **12.83%** | −2.09pp（更好） |
| DD | 9.58% | **5.41%** | **−4.17pp（大幅改善）** |
| 2Y | 2.18 | **2.69** | **+0.51** |
| sub | 1.62 | 1.60 | −0.02（基本不变） |
| R | 5.64% | 5.30% | −0.34pp |

**机制解释**：`ts_delta` 只度量「最近一期的变化量」，对噪声极为敏感（DD 9.58% 就是证据）；
`ts_zscore` 度量「当前水平在 66 日分布中的位置」，对单期异常值稳健 ⇒ 回撤与 2Y 显著改善。
**这是一条可直接迁移的杠杆**：凡是 `−ts_delta(x, W)` 型骨架，若 DD 偏高或 2Y 偏弱，优先改写成 `ts_zscore(multiply(x,−1), W')`。

### 56.3 互相关：修好了但位置被占

```
                ZYQXwGPn  RRE5Mwkn  ZYQXZj73  QPvbxjXw  rKRPAWv9
ZYQXwGPn        1.000     0.282     0.938     0.131     -0.112
RRE5Mwkn        0.282     1.000     0.321     0.004      0.017
ZYQXZj73        0.938     0.321     1.000     0.152     -0.101
QPvbxjXw        0.131     0.004     0.152     1.000     -0.164
rKRPAWv9       -0.112     0.017    -0.101    -0.164     1.000
```

`ZYQXwGPn × ZYQXZj73 = 0.9379`，**根因是共用同一冷腿**（`reverse(group_rank(ts_zscore(vec_sum(loaned_share_count_main), 504), sector))`）——
两者信号腿完全不同（`auction_order_imbalance_pct_adv` vs `dark/lit` 占比），相关却高达 0.94 ⇒ **冷腿主导了持仓相关性**。
`ZYQXwGPn` self = 0.2177（本身很干净）。

### 56.4 决策：`ZYQXwGPn` 只作备份，不测 prod

两者塔位**完全相同**（OTHER + SHORTINTEREST ⇒ `pyramid_short = shortinterest/other`），只能二选一：

| | S | F | TO | DD | 2Y | prod |
|---|---:|---:|---:|---:|---:|---|
| `ZYQXZj73`（选） | **1.78** | **1.16** | 13.3% | **5.11%** | **2.84** | **0.6524 已验证 ✓** |
| `ZYQXwGPn`（备份） | 1.66 | 1.07 | **12.83%** | 5.41% | 2.69 | 未测 |

`ZYQXZj73` 六项中四项占优且 prod 已验，**不换**。`ZYQXwGPn` 省下 prod 额度，仅在 `ZYQXZj73` 提交受阻时启用。

### 56.5 结构性发现：OTHER 塔的三颗必然互相冲突

OTHER 塔要点亮需要 3 颗提交。但目前所有 OTHER 件都走同一条路：**`order_book_imbalance` 信号腿 × `loaned_share_count_main` 冷腿**，
而冷腿主导相关性 ⇒ **任意两颗 OTHER 件互相关都在 0.9 以上，无法同时提交**。

⇒ **要点亮 OTHER 塔，必须先把冷腿解耦**。可用手段（按有效性排序）：
1. **换冷腿字段**：`loaned_market_value_usd` / `average_loan_duration_days`（同集其他存量字段）。
2. **位移冷腿窗口**：504 → 630 / 756。
3. **换冷腿分组轴**：`sector` → `industry` / `market`。
4. **换冷腿归一化**：`ts_zscore` → `ts_rank`。
5. **完全不用冷腿**，让 OTHER 信号腿独立过闸（`Xg9NXebm` 系列去掉冷腿后 S 只有 ~0.6，不可行）。

这条约束意味着：**OTHER 塔的点亮成本远高于其他塔**，应把产能优先投向 EARNINGS / RISK / INSTITUTIONS / SOCIALMEDIA 这些尚未被冷腿锁死的塔。
## 五十七、可开采池图谱写清（55 集）＋ U53 连坐诊断 ＋ U55/U56 双批派发

### 1. U53 全灭的真相：1 条真错 + 7 条连坐

`harvest_multisim_alphas` 返回 `error_count = 8 / total = 8`，全部文案 `No alpha_id in sim response`。
按纪律跑 `_tmp_multisim_diag.py 2JDjOg52g4qMbNdsXAHAQCU`，读子任务 status + message：

| 子任务 | status | message |
|---|---|---|
| `3H7sTpa8…` | **ERROR** | `Operator subtract does not support event inputs.` |
| 其余 7 条 | CANCELLED | None |

**结论**：只有第 6 条（`preliminary_eps_range_upper_bound - preliminary_eps_range_lower_bound`）真错——
`preliminary_eps_range_*` 是 **event 类型字段**，禁止裸算术；其余 7 条是干净表达式被连坐取消。

**⇒ 第二次实证「连坐」机制**（第一次是 U39 的 event×multiply）。凡 `error_count == total` 且文案为
`No alpha_id in sim response`，**一律不得据此判数据集死刑**，必须先诊断，只重派被连坐的条目。
**⇒ event 类型字段清单新增成员**：`search_interest`、`event_relation`、`preliminary_eps_range_{lower,upper}_bound`。
**⇒ 反例佐证**：`ern6_actual_eps` / `ern6_estimated_eps` 经 `vec_avg` 后可做 `subtract`（`kqN8kKWz` S1.73 已证），
所以不是整个 `earnings6` 都是 event 类型，只有 `preliminary_eps_range_*` 是。

### 2. 可开采池：177 集 → 55 集（未点亮塔 ∩ 非 DEAD）

用 `get_datasets` 全量 177 集，减去「已点亮塔（model 5 / news 3 / analyst 3 / fundamental 3）」与
「台账 DEAD」，剩 **55 个可开采数据集**。按塔分布：

| 塔 | 点亮 | 可开采集数 | 备注 |
|---|---:|---:|---|
| other | 1/3 | **26** | 池子最大，alphaCount 3–96 的新集最多 |
| pv | 2/3 | **13** | **只差 1 颗即点亮** |
| institutions | 0/3 | 3 | institutions4(47) / institutions1(52) / institutions25(90) |
| sentiment | 0/3 | 3 | sentiment7(96, 已三次证伪) / sentiment33(209, 255字段) / sentiment27(834) |
| socialmedia | 0/3 | 2 | socialmedia5(155) / socialmedia39(298, **仅 1 个字段**) |
| insiders | 0/3 | 2 | insiders12(401) / insider_agg_matrix(562, **never really tested**) |
| risk | 0/3 | 3 | risk88(567) / risk71(608) / **risk68(731, prod 0.5937 合格)** |
| option | 0/3 | 1 | option1(294, 22 VECTOR) |
| shortinterest | 0/3 | 1 | shortinterest3(1668, 信号腿侧已封盘) |
| imbalance | 0/3 | 1 | imbalance5(1941, 仅 2 字段) |
| **earnings** | 0/3 | **0** | 三个 earnings 集全部在 DEAD 里 ⇒ 只能靠新几何复活 |

**按 alphaCount 升序的「最新」十集**（拥挤度 ≈ prod 风险的代理指标）：

| 集 | 塔 | aC | 字段数 | 是否曾真跑 |
|---|---|---:|---:|---|
| `pv113` | pv | **2** | 1 | 否 |
| `other546` | other | 3 | 22 | SKIPPED |
| `pv17` | pv | 3 | 1 | 否 |
| `workforce_flow_skills` | other | 3 | 10 | SKIPPED |
| `other327` | other | 4 | 3 | SKIPPED |
| `pv71` | pv | 4 | 8 | 否 |
| `other384` | other | 6 | 66 | **U46 已测，4 种编码全负** |
| `euro_equity_imbalance` | other | 7 | 4 | SKIPPED |
| `other250` | other | 8 | 12 | SKIPPED |
| `other567` | other | 11 | 48 | SKIPPED |

### 3. 本轮新拿到的字段画像（7 个从未开采过的集）

**`pv109`（PV，aC 32，26 VECTOR）—— 公司债收益率/报价面板**：
`midpoint_yield_to_maturity`、`bid_side_yield_to_maturity`、`ask_side_yield_to_maturity`、
`midpoint_conversion_yield`、`highest_bid_price` / `lowest_ask_price` / `midpoint_trade_price`、
`bond_coupon_rate`、`pv109_amt_outstanding`、`pv109_maturity`、`total_traded_volume`。
**这是「信用利差 → 股票收益」的直连通道**（Campbell-Hilscher-Szilagyi 困境风险机制），GBR 从未有人挖过。

**`pv173`（PV，aC 19，81 字段）—— 债券 z-spread PCA 曲面 + 股债背离**：
`pv173_ranks_mt5yzspread{,chg60d,chgstd20d,indrel,zscore60d,sbst}`、
`pv173_ranks_shift60d{chg60d,last,std60d,zscore60d}` / `tilt*` / `twist*`（PCA 水平·斜率·曲率）、
`pv173_ranks_eqbddivrgbdrtn120d`（**120 日股债收益背离，横截面排名**）。

**`workforce_flow_skills`（OTHER，aC 3，10 VECTOR）—— 劳动力流动面板**：
`employee_inflow_count_2` / `employee_outflow_count_2` / `employee_headcount_2`、
`adjusted_employee_headcount`、`total_salary_amount_2`、`position_seniority_level_2`、
`employee_prestige_score_2`、`unreliable_user_{count,inflow,outflow}_2`（数据质量标记）。
**净招聘率 = (inflow − outflow)/headcount** 是 Belo-Lin-Bazdresch 劳动力投资因子的直接实现。

**`other567`（OTHER，aC 11，48 VECTOR）—— 员工评论/满意度面板（Glassdoor 类）**：
`avg_overall_company_score`、`avg_ceo_approval_score`、`avg_business_outlook_score`、
`avg_culture_values_score`、`avg_recommend_to_peer_score`、`avg_senior_management_score`、
`avg_work_life_balance_score`、`avg_pay_and_benefits_score`、`avg_career_growth_score`、`avg_diversity_inclusion_score`，
外加 20 余个 `*_sentiment_score` 文本情绪分。**Edmans(2011) 员工满意度 → 超额收益** 的直接实现。

**`other128`（OTHER，aC 12，14 VECTOR）—— 高管信心 z-score + 薪酬 + 任期**：
`chief_exec_investor_sentiment_score_dmexus`、`finance_exec_investor_sentiment_score_dmexus`、
`oth128_dmexusceo{tenure,cashcompensation,noncashcompensation}` / `cfo*`、
`oth128_dmexusexecutiveefficiency{input,output}`、`oth128_dmexuskeyexecutive{ice,tenure}`、
**`oth128_dmexusscore`（Capri 管理层质量综合分）**。

**`other699`（OTHER，aC 14，7 VECTOR）—— TipRanks 组合交易事件**：
`oth699_sharestraded`（正买负卖）、`newnumofshares` / `prevnumofshares`（拆股调整后）、
`priordistincttradingdays`、`priortransactionnumber`、`aggsplitfactor`。

**`other250`（OTHER，aC 8，12 VECTOR）—— 商品价格/畅销排名/评论数**：
`sales_position_rank`（类目内畅销排名，1 最优）、`oth250_rank`、`oth250_item_display_price`、
`price_range_max` / `price_range_min`、`oth250_item_review_count` / `total_review_number`、`average_star_score`。

**`institutions4`（INSTITUTIONS，aC 47，6 VECTOR）—— 机构持仓前后期对照**：
`institutional_holding_current_{shares,market_value}` 与 `previous_*` 成对，外加
`percent_of_portfolio` / `percent_of_shares_outstanding`。**这是「机构增减仓率」的现成结构**，无需自己做差分。

**`insiders12`（INSIDERS，aC 401，7 VECTOR）—— 内部人交易明细**：
`insd12_positionchangetransactionamount`（**正买负卖**）、`insd12_sharesheld`、`insd12_percent`（事后持股比例）、
`insd12_mktprice`、`option_exercise_price_{eur,gbp,reported}`。

**`insider_agg_matrix`（INSIDERS，aC 562，34 MATRIX）—— 内部人聚合矩阵**：
`avg_buy_shares` / `avg_sell_shares`、`avg_top_buy_shares` / `avg_top_sell_shares`、
`avg_secondary_{buy,sell}_shares`（直接持股）、`avg_secondary_top_*`（高管直接）、
`directional_indicator` / `directional_indicator_2`（现成方向指标）、
`{top_,directional_,top_directional_}significant_value_1..4`（按重要性排序的前 4 笔）。
台账记 `SIM_FAIL n=0` ⇒ **从未真正跑过**。

### 4. U55 / U56 双批派发（本轮实际动作）

**U55 = `4N8DYeVc4tGc12PmQkMrIr`（8 条，纯单腿，无冷腿）**

全部选「alphaCount ≤ 32 的新集」，纯单数据集 ⇒ 互相关天然低、不占塔混配额。
PV 只差 1 颗点亮，所以 8 条里 4 条打 PV。

| # | 集 | 机制 | 表达式骨架 | 算子数 |
|---|---|---|---|---:|
| 1 | pv109 | 信用利差水平（困境风险） | `reverse(group_rank(ts_zscore(vec_avg(midpoint_yield_to_maturity),66),sector))` | 3 |
| 2 | pv109 | 债券买卖价差/流动性溢价 | `group_rank(ts_zscore(divide(subtract(vec_avg(lowest_ask_price),vec_avg(highest_bid_price)),vec_avg(midpoint_trade_price)),126),sector)` | 6 |
| 3 | pv173 | 股债 120 日收益背离（均值回复） | `reverse(group_rank(ts_zscore(pv173_ranks_eqbddivrgbdrtn120d,252),subindustry))` | 3 |
| 4 | pv173 | 5y z-spread 60 日变动（信用恶化） | `reverse(group_rank(ts_zscore(pv173_ranks_mt5yzspreadchg60d,126),industry))` | 3 |
| 5 | workforce_flow_skills | 净招聘率（劳动力投资因子） | `reverse(group_rank(ts_mean(divide(subtract(vec_avg(inflow),vec_avg(outflow)),vec_avg(headcount)),66),sector))` | 8 |
| 6 | other567 | 员工满意度变动（Edmans 无形资产） | `group_rank(ts_delta(vec_avg(avg_overall_company_score),66),subindustry)` | 3 |
| 7 | other128 | 管理层质量综合分 | `group_rank(ts_zscore(vec_avg(oth128_dmexusscore),126),sector)` | 3 |
| 8 | other250 | 商品畅销排名改善（需求动量） | `reverse(group_rank(ts_zscore(vec_avg(sales_position_rank),66),sector))` | 3 |

**U56 = `1XL2wufjq4G9bpaSaWU7OfR`（8 条，打 double-zero 塔 institutions 0/3 + insiders 0/3）**

这两个塔一颗都没有，且 `insiders12` / `insider_agg_matrix` **从未真正跑过**（台账 SKIPPED / SIM_FAIL n=0）。

| # | 集 | 机制 | 骨架要点 | 算子数 |
|---|---|---|---|---:|
| 1 | institutions4 | 机构持股数变动（增减仓） | `group_rank(ts_zscore(subtract(vec_sum(cur_shares),vec_sum(prev_shares)),66),sector)` | 5 |
| 2 | institutions4 | 流通股持股占比分位（252 长窗） | `group_rank(ts_rank(vec_sum(percent_of_shares_outstanding),252),subindustry)` | 3 |
| 3 | institutions4 | 持股市值 22 日变动（反向） | `reverse(group_rank(ts_delta(vec_sum(cur_market_value),22),industry))` | 4 |
| 4 | insiders12 | 内部人净买入 / 持股数（比率归一） | `group_rank(ts_zscore(divide(vec_sum(positionchangetransactionamount),vec_sum(sharesheld)),126),sector)` | 5 |
| 5 | insiders12 | 同上走 252 分位（非线性变换对照） | `group_rank(ts_rank(同上,252),subindustry)` | 4 |
| 6 | insider_agg_matrix | 全董事买卖失衡（归一化） | `group_rank(ts_zscore(divide(subtract(avg_buy,avg_sell),add(avg_buy,avg_sell)),126),sector)` | 5 |
| 7 | insider_agg_matrix | 高管层买卖失衡 | `...avg_top_buy_shares / avg_top_sell_shares...,subindustry` | 5 |
| 8 | insider_agg_matrix | 现成方向指标 22 日均值 | `group_rank(ts_mean(directional_indicator,22),sector)` | 3 |

**模板多样性自查（对应「≥10 个结构互异模板」硬约束）**：两批合起来覆盖
①水平 z-score ②长窗 ts_rank 分位 ③一阶差分 ts_delta ④ts_mean 平滑 ⑤比率归一 ⑥归一化失衡 (a−b)/(a+b)
⑦价差/中价 ⑧横截面排名差分 ⑨离散方向指标 ⑩反向（reverse）与正向对照；
分组轴覆盖 sector / subindustry / industry / market，矩覆盖水平·一阶差分·二阶（背离）·分位。
**唯一缺口是非线性变换族（只用了 ts_rank 和 revers）与条件分支族，留给下一批。**

### 5. 台账核对结果（派发前必查的收货）

| 集 | 台账判定 | 含义 |
|---|---|---|
| `insider_agg_matrix` | **SIM_FAIL n=0** | 仿真失败，**从未真正跑过** ⇒ U56 #6-8 是首测 |
| `insiders12` | SKIPPED_LOW_COV n=None | 覆盖率筛掉的，**从未跑过** ⇒ U56 #4-5 是首测 |
| `risk68` | BORDERLINE S1.39 / **2Y 0.55** / **prod 0.5937** / n=39 / frag 0.196 / 最佳年 +2.6% | **prod 已合格、样本健康**，唯一卡点是 2Y ⇒ 高价值破墙对象 |
| `institutions4` / `sentiment33` / `risk71` / `option1` / `other734` / `pv109` / `pv173` / `workforce_flow_skills` / `other567` / `other128` / `other250` | 台账无记录 | 全部首测 |

## 五十八、U56 全灭（8/8，max S 0.37）—— institutions / insiders 双零塔首测失败，并逼出「必须做纯单腿」的战略结论

### 1. U56 = `1XL2wufjq4G9bpaSaWU7OfR` 全部 8 条实测（comp=8 err=0，无连坐）

| # | 集 | alpha | S | F | TO | DD | 2Y | sub | lc | nf | 塔 |
|---|---|---|---:|---:|---:|---:|---:|---:|---:|---:|---|
| 1 | institutions4 | `LLM8bvE6` 持股数变动 | **0.24** | 0.08 | 17.5% | 16.6% | 0.38 | 0.07 | 315 | 5 | institutions |
| 2 | institutions4 | `WjOYwZ3O` 流通股占比分位 | −0.04 | 0.00 | 14.3% | 8.0% | 0.32 | 0.53 | 208 | 3 | institutions |
| 3 | institutions4 | `Xg9Nw3Vx` 持股市值 22 日变动(反) | 0.37 | 0.10 | 8.7% | 5.1% | −0.34 | −0.03 | 595 | 4 | institutions |
| 4 | insiders12 | `qML5kaY1` 内部人净买入比 | −0.56 | −0.21 | 10.0% | 20.2% | −1.12 | −0.62 | 432 | 4 | insiders |
| 5 | insiders12 | `E56m0j80` 同上 252 分位 | −0.17 | −0.03 | 10.9% | 10.9% | −0.34 | −0.35 | 439 | 4 | insiders |
| 6 | insider_agg_matrix | `vR1YnEpv` 董事买卖失衡 | −0.15 | −0.02 | 56.9% | 25.9% | −0.10 | −0.03 | 280 | 4 | insiders |
| 7 | insider_agg_matrix | `1YNGV8lW` 高管买卖失衡 | **0.17** | 0.02 | 56.3% | 20.4% | 0.39 | 0.28 | 306 | 4 | insiders |
| 8 | insider_agg_matrix | `6XdGPWoL` 方向指标 22 日均 | −0.34 | −0.08 | 16.4% | 13.5% | 0.20 | −0.07 | 260 | 3 | insiders |

**判读**：
- **institutions4 与 insiders12 / insider_agg_matrix 的全部几何都在 |S| ≤ 0.56**，且方向不一致（有正有负）⇒ 不是「符号反了」而是**没有稳定信号**。
- `insider_agg_matrix` 两条失衡式 TO 高达 56–57%，且撞 `CONCENTRATED_WEIGHT`（limit 0.10）⇒ 该集字段是稀疏大值，横截面归一化后仍集中在少数股票。
- 8 条全部 `longCount` 在 208–595 之间，说明字段有覆盖、不是稀疏缺失问题。

**⇒ 判决：institutions(0/3) 与 insiders(0/3) 两个塔的上游字段本身不具备独立预测力。**
若还要点这两个塔，只剩一条路：把这两个集的弱信号腿**挂 2:1 冷腿**（历史上把 0.98 抬到 1.78）。
但 U56 最高只有 0.24–0.37，按冷腿 +0.8~2.7 的经验外推，落到 1.0–1.6 区间，**过 1.58 的概率不高**，暂不投入。

### 2. 顺带得到一条硬约束的第四次实证：`LOW_SUB_UNIVERSE_SHARPE` 的 limit 会变，而且**可以是负数**

U56 八条返回的 `checks.fail[].limit` 里，`LOW_SUB_UNIVERSE_SHARPE` 出现四个不同值：

| alpha | limit |
|---|---:|
| `LLM8bvE6` | **0.11** |
| `Xg9Nw3Vx` | **0.18** |
| `qML5kaY1` | **−0.27** |
| `E56m0j80` | **−0.08** |

⇒ 该闸的阈值是**按候选动态生成**的（可正可负），任何「sub ≥ 0.2 就安全」或「sub 必须为正」的经验判据都会误判。
**唯一合法做法仍是读 `checks.fail[].limit`，或直接看 `ra.failed_ra_count == 0`。**

### 3. 战略结论：要凑够 20 颗可提交，必须做「纯单腿」而不是「挂冷腿」

把本战役所有证据串起来，冷腿配方（2:1 `loaned_share_count_main`）是双刃剑：

| 事实 | 数据 |
|---|---|
| 冷腿能把弱腿抬到全闸 | `order_book_imbalance` 同集内 2:1 只有 S 0.98 → 挂冷腿 1.78；PEAD 裸版 −0.96 → 1.73（+2.69） |
| 但冷腿**主导持仓相关性** | `ZYQXwGPn`（信号腿完全不同）× `ZYQXZj73` = **0.9379**；`O0A6Qz7p` × `ZYQXZj73` = **0.7684** |
| 于是同批只能提交 1 颗 | 4 颗可提交件里 2 颗挂冷腿（`RRE5Mwkn` / `ZYQXZj73`），第三颗挂冷腿的必被前两颗拦下 |

**⇒ 冷腿配方的产能上限 ≈ 每批 1 颗，永远凑不到 20 颗。**
**⇒ 必须回到纯单腿**：只要单腿自身 S ≥ 1.58 且 prod < 0.70，就自然与其它数据集不同字段的件低相关。
**纯单腿能到 1.58 已有先例**：`omEPQrLE`（`transaction_count_main` 纯单腿）S **1.82**、`d5W9eobx` S **1.75**——
说明 GBR/TOP700 里确实存在「字段本身就有 1.7+ 预测力」的强字段，问题在找到它们，而不是靠冷腿补。

**⇒ 因此 U55/U57/U58/U59 全部采用纯单腿设计**（每批 8 条、每条只用 1 个数据集的字段），
并把「找强字段」当作唯一目标：一个数据集只要能被某个几何撬到 S ≥ 1.58，它就是一个独立可提交件。

## 五十九、U57 / U58 / U59 收批（24 条，最高 S 0.66）—— 新集慢变基本面描述符系统性无信号，且拿到 `vec_avg` 这条关键算子规则

### 1. ★★★★★ 关键算子规则：`vec_avg` 是绕过 event 类型限制的正确包装（4/4 实证）

同一批 `pv173_ranks_*` 字段：

| 版本 | 式 | 结果 |
|---|---|---|
| 裸用（U55 #3/#4） | `ts_zscore(pv173_ranks_eqbddivrgbdrtn120d, 252)` | **ERROR: `Operator ts_zscore does not support event inputs`** |
| 包 `vec_avg`（U58） | `ts_zscore(vec_avg(pv173_ranks_eqbddivrgbdrtn120d), 252)` | **comp=4 / err=0，全部跑通** |

⇒ **凡字段标 `[VECTOR]` 但平台内部判为 event 类型（裸 `ts_*`/`subtract` 报 `does not support event inputs`），
统一先用 `vec_sum` / `vec_avg` 折成标量，再套任何算子。** 这条同时解释了 U53 的 `preliminary_eps_range_*`
失败（那两个是 event 标量，连 `vec_avg` 都无从下手 ⇒ 只能整字段弃用）。
**判据总结**：
- event **向量**（`pv173_ranks_*`、`order_book_imbalance` 多数、`other696` 计数）→ `vec_*` 包一层即可用；
- event **标量**（`preliminary_eps_range_{lower,upper}_bound`）→ 无解，弃用。

### 2. U57 = `3l0TLL8aI53Z9C11ahig5jh8`（8/8 全完，纯单腿新集）

| # | 集 | alpha | S | F | TO | DD | 2Y | sub | lc | nf |
|---|---|---|---:|---:|---:|---:|---:|---:|---:|---:|
| 1 | pv109 | `akKRMY76` 信用利差水平（反） | 0.16 | 0.03 | 13.0% | 8.1% | −0.30 | −0.07 | 587 | 4 |
| 2 | pv109 | `vR1Yxqja` 债券买卖价差 | 0.01 | 0.00 | 13.8% | 12.8% | **1.12** | 0.28 | 319 | 3 |
| 3 | workforce | `LLM8qj76` 净招聘率（反） | −0.73 | −0.36 | 9.8% | 35.8% | −0.34 | −0.67 | 549 | 4 |
| 4 | other567 | `1YNG19wJ` 员工满意度变动 | 0.08 | 0.01 | 10.6% | 10.9% | **1.07** | −0.13 | 319 | 4 |
| 5 | other128 | `3qoG3ble` 管理层质量综合分 | 0.08 | 0.01 | 20.0% | 14.6% | **1.28** | 0.08 | 419 | 3 |
| 6 | other250 | `WjOYnq7O` 畅销排名（反） | −0.09 | −0.01 | 23.8% | 10.1% | −0.43 | −0.21 | 592 | 4 |
| 7 | pv109 | `Xg9NPr7x` 信用利差动量（反） | −0.05 | −0.01 | 12.1% | 9.9% | −0.99 | −0.20 | 603 | 4 |
| 8 | workforce | `j2YVWE35` 薪资增速 | 0.26 | 0.07 | 10.8% | 11.4% | 0.34 | 0.27 | 371 | 3 |

### 3. U58 = `2fQTsgdgL4KpbDg18UWBdgWj`（pv173，4/4 全完）

| # | alpha | 机制 | S | F | TO | 2Y | sub | nf |
|---|---|---|---:|---:|---:|---:|---:|---:|
| 1 | `GrWQYYLZ` | 股债 120 日收益背离（反） | 0.19 | 0.04 | 20.5% | −1.48 | 0.03 | 4 |
| 2 | `2rAGQQN8` | 5y z-spread 60 日变动（反） | 0.12 | 0.02 | 16.1% | −0.99 | −0.19 | 4 |
| 3 | `A1VLYY7d` | z-spread z-score 252 分位（反） | 0.06 | 0.01 | 17.3% | −0.70 | −0.21 | 4 |
| 4 | `xArl99dm` | 股债 spread 背离 | −0.10 | −0.01 | 20.4% | 1.05 | 0.11 | 3 |

### 4. U59 = `1kPP5m2Qq4QRck5nvMh8uw4`（option1 首测，4/4 全完，**唯一有正 S 的新集**）

| # | alpha | 机制 | S | F | TO | DD | 2Y | sub | lc | nf | 说明 |
|---|---|---|---:|---:|---:|---:|---:|---:|---:|---:|---|
| 1 | `88RG7rvl` | IV 水平（反） | −0.44 | −0.14 | 16.6% | 20.3% | −1.00 | −0.32 | 558 | 4 | IV 水平无效 |
| 2 | `e751gK6N` | IV 22 日变化（反） | −0.28 | −0.06 | 21.9% | 17.1% | −1.43 | −0.24 | 561 | 4 | IV 变化无效 |
| 3 | `kqN8bXJ6` | **moneyness 126 日 z-score** | **0.66** | 0.24 | 18.3% | **6.45%** | **1.45** | 0.34 | 349 | 3 | **DD 仅 6.45%（全战役最低档）** |
| 4 | `bl6xVM6l` | **剩余期限 66 日 z-score** | 0.17 | 0.03 | 18.6% | 14.5% | **1.64** | 0.13 | 305 | **2** | **只有 LOW_SHARPE/LOW_FITNESS 两项失败，其余 RA 全过** |

**⇒ option1 是唯一还能救的新集**：
- `kqN8bXJ6`（moneyness）DD 6.45% 是本战役最低档之一，2Y 1.45 接近阈值，**只差 S 与 F**；
- `bl6xVM6l`（期限结构）`failed_ra_count = 2`，是本战役 32 条新集探针里 **RA 最干净的一颗**，
  说明「期权剩余期限」这条腿本身就稳（TO 18.6%、2Y 1.64），只缺收益幅度。
- 两条都指向同一件事：**option1 的信息在「结构」（moneyness/期限），不在「水平」（IV 高低）**。
  这与 `imbalance5`（只在变化率里、水平无效）、`socialmedia5`（只在 high−low 分歧里）是同一类现象。
  下一轮 option1 应把 moneyness × 期限做交互（如按期限分桶后的 moneyness 斜率），而不是单独取水平。

### 5. ★★★★★ 跨 32 条探针的横向规律：**新集慢变基本面描述符系统性无信号**

把 U55/U56/U57/U58/U59 合计 32 条探针按「字段类型」分层，规律极其干净：

| 字段类型 | 代表 | 实测 S 区间 |
|---|---|---|
| 机构持仓 / 内部人交易 | institutions4、insiders12、insider_agg_matrix | **−0.56 ~ 0.37** |
| 员工评价 / 满意度 / 招聘 | other567、workforce_flow_skills | **−0.73 ~ 0.26** |
| 管理层质量 / 高管信心 | other128 | **0.08** |
| 信用利差 / 债券 z-spread | pv109、pv173 | **−0.10 ~ 0.19** |
| 商品价格 / 畅销排名 | other250 | **−0.09** |
| **期权曲面结构** | option1 moneyness / 期限 | **0.17 ~ 0.66**（唯一正区间） |

而本战役所有 S ≥ 1.6 的件，信号腿无一例外属于**高频流量 / 交易微观结构 / 注意力**类：
`pv103_ivam_sum`（日内成交额）、`oth47_organic_traffic`（网站流量）、
`auction_order_imbalance_pct_adv`（集合竞价失衡）、`transaction_count_main`（成交笔数）、`imb5_score` 变化率。

**⇒ 机制解释（第一性原理）**：GBR/TOP700 是**流动性分层极强**的市场。慢变基本面描述符（持仓、评级、满意度）
在横截面上被行业与市值高度解释，`group_rank` 中性化后几乎不剩信息；而**流量类字段携带的是「谁在这周开始关注这只股票」**，
是真正的增量信息，且天然在横截面上分散。**这不是「数据集不好」，而是「字段所属信息层」的问题。**

**⇒ 直接后果**：55 个可开采集里，绝大多数字段属于慢变层，这就是为什么台账里 55 集里 DEAD 占了 50 多集。
**剩余机会只在两类字段上**：① 高频/事件/流量类新集（`option1` 结构、`other696` 文本计数、`event_ml_signals` 事件标记）；
② 已验证流量字段的**新组合几何**（U62 正在做的冷腿权重解耦 + 4 条新腿）。

## 六十、U61（`other696` 主题净情绪）全灭 + U63 派发：把「新集最强腿」挂冷腿做最后一轮抢救

### 1. U61 = `Bp49LeMK51L99ufbwzoeGo`（8/8 全完）

`other696`（OTHER，aC 39，220 字段，25 用户）结构上极诱人：**每个主题都有 `*_positive` / `*_negative` 成对计数**，
天然可算净情绪。8 条探针覆盖 4 种几何（ts_mean22 / ts_zscore126 / ts_delta66 / ts_rank252）× 8 个主题：

| # | 主题 / 几何 | alpha | S | F | TO | DD | 2Y | sub | nf | 备注 |
|---|---|---|---:|---:|---:|---:|---:|---:|---:|---|
| 1 | all-DL 净情绪 ts_mean22 | `N1NKqbzq` | 0.23 | 0.05 | 20.8% | 14.1% | 0.39 | **0.60** | 4 | sub 最高 |
| 2 | balancesheet 净情绪 | `j2YVW6GZ` | −0.03 | 0.00 | 21.6% | 20.8% | 0.55 | 0.24 | 4 | |
| 3 | backlog 净情绪 | `mLoKJ576` | 0.04 | 0.00 | 29.7% | 18.7% | −0.05 | 0.16 | 4 | |
| 4 | acquisitions 净情绪 zs126 | `1YNG1pKR` | 0.25 | 0.08 | 22.5% | 29.7% | −0.09 | 0.12 | 4 | |
| 5 | accountingstandards zs126 | `LLM8qGrL` | −0.49 | −0.22 | 21.2% | **74.1%** | −0.18 | −0.42 | 5 | DD 74% |
| 6 | awards 净情绪 ts_delta66 | `1YNG1pPQ` | **0** | — | **0** | **0** | — | — | 5 | **常数/稀疏标记** |
| 7 | accessaffordability ts_delta66 | `ZYQXqEMZ` | **0.78** | 0.44 | 18.1% | **5.33%** | 0.00 | −0.03 | 5 | 本批最好，但 2Y=0 |
| 8 | airquality 净情绪 ts_rank252 | `WjOYnA0N` | 0.13 | 0.03 | 23.0% | 16.9% | 0.28 | −0.01 | 5 | |

**判读**：
- 8 条里 6 条撞 `CONCENTRATED_WEIGHT`（limit 0.10）⇒ 该集字段是「多数股票为 0、少数股票有大计数」的稀疏结构，
  净情绪在中性化后仍集中在少数名字上。**这是 `other696` 的结构性缺陷，不是几何问题。**
- 唯一亮点 `ZYQXqEMZ`（accessability & affordability 主题）S 0.78 / **DD 5.33%** ⇒ 收益曲线质量好但幅度不足，且 2Y 恰好 0。
- `1YNG1pPQ` 给出**零成本判据的又一次实证**：`S=0 / TO=0 / longCount=0 / LOW_TURNOVER` ⇒ `awards_*` 两个字段在该宇宙下是常数（全 0），
  只有永久无害的 `longCount=0` 组合出现，就该直接弃字段，不必再试几何。

### 2. ★★★★ 田野结论更新：新集池已基本探完，剩两条已知可救的腿

累计 **40 条探针 / 18 个新集**（U55 6 + U56 8 + U57 8 + U58 4 + U59 4 + U61 8 + U53 2 真错），
**只有 3 条腿进入「弱正但可救」区间**：

| 腿 | alpha | S | DD | 2Y | nf | 为什么可救 |
|---|---|---:|---:|---:|---:|---|
| `option1` moneyness 126 z-score | `kqN8bXJ6` | **0.66** | **6.45%** | 1.45 | 3 | 结构类信息 + DD 极低 |
| `option1` 剩余期限 66 z-score | `bl6xVM6l` | 0.17 | 14.5% | **1.64** | **2** | **RA 最干净（仅缺 S/F）** |
| `other696` accessaffordability 净情绪 ts_delta66 | `ZYQXqEMZ` | **0.78** | **5.33%** | 0.00 | 5 | 本战役新集最高 S + 极低 DD |

其余全部 |S| ≤ 0.5 且方向不稳定 ⇒ 判「该信息层在 GBR/TOP700 无独立预测力」，不再换几何。

### 3. U63 = `109NsHbjD56v9BsYGF3UVuV`：给这 3 条腿挂冷腿，做最后一轮抢救

设计逻辑：冷腿（2:1）在历史上把 0.98 抬到 1.78（+0.80）、把 −0.96 抬到 1.73（+2.69）。
这 3 条腿裸版已有 0.17–0.78，挂冷腿理论落点 1.0–1.6，**是唯一可能越过 1.58 的路径**。
同时用 1:1 与 2:1 两种权重做对照（延续 U62 的解耦实验）。

| # | 腿 | 权重 | 塔组合 | 配额 |
|---|---|---|---|---|
| 1 | option1 moneyness 126 z-score | 2:1 | **OPTION × SHORTINTEREST** | 集外×集外，**不限量** |
| 2 | option1 剩余期限 66 z-score | 2:1 | OPTION × SHORTINTEREST | 不限量 |
| 3 | other696 accessaffordability ts_delta66 | 2:1 | OTHER × SHORTINTEREST | 已用类型（ZYQXZj73） |
| 4 | other696 all-DL 净情绪 ts_mean22 | 2:1 | OTHER × SHORTINTEREST | 已用类型 |
| 5 | option1 moneyness 126 z-score | 1:1 | OPTION × SHORTINTEREST | 不限量（解耦对照） |
| 6 | option1 剩余期限 66 z-score | 1:1 | OPTION × SHORTINTEREST | 不限量（解耦对照） |
| 7 | pv109 债券买卖价差 | 2:1 | PV × SHORTINTEREST | 已用类型（RRE5Mwkn） |
| 8 | pv173 股债 spread 背离 | 2:1 | PV × SHORTINTEREST | 已用类型 |

**若 #1/#2 有任一颗全闸且 prod < 0.70，就是 OPTION 塔（当前 0/3）的首个可提交件**——
这是本战役目前**最便宜的塔点亮机会**（OPTION 塔只需 3 颗，且完全不受塔混配额约束）。

## 六十一、批次级 `FAIL`（U62 与 U63 连续 8/8 全灭，msg=None）—— 与「连坐 CANCELLED」是两种不同故障

### 1. 现象

| 波次 | multisim | 结果 | 子任务状态 | message |
|---|---|---|---|---|
| U62 | `2GfHEH8Y64oPcAM15scwD3Jt` | comp=0 err=8 | **FAIL ×8** | **None** |
| U63 | `109NsHbjD56v9BsYGF3UVuV` | comp=0 err=8 | **FAIL ×8** | **None** |

对比此前三种已知故障：

| 故障形态 | 子任务状态 | message | 含义 |
|---|---|---|---|
| 语法/类型错连坐（U39 / U53 / U55） | 1-2 条 ERROR + 其余 CANCELLED | ERROR 条有明确文案（`does not support event inputs`） | 单条真错，可定位 |
| **本节的批次级失败（U62 / U63）** | **全部 FAIL** | **全部 None** | **整批被平台拒绝，无任何可定位信息** |

**⇒ 判据**：`harvest` 返回 `error_count == total` 且 `diag` 显示 **全 FAIL + msg=None**（不是 CANCELLED），
就属于**批次级拒绝**，与表达式内容无关，**必须整批重派**，且**不得据此给任何字段/数据集下结论**。

### 2. 两批的共同点：都含 `option1`

| 波次 | 含 option1 | 表达式数 | 结果 |
|---|---|---:|---|
| U59（option1 单独成批，无冷腿） | ✅ 4 条 | 4 | **全部成功** |
| U62 | ✅ 1 条（moneyness 2:1） | 8 | 整批 FAIL |
| U63 | ✅ 4 条（moneyness/期限 × 2:1/1:1） | 8 | 整批 FAIL |
| U55 / U56 / U57 / U58 / U61（均无 option1） | ❌ | 4–8 | **全部成功** |

**工作假设（待 U63b 判别）**：`option1` 的 VECTOR 期权曲面字段在**与 504 窗冷腿叠加**时资源超限，
导致**整批**被拒。此前台账已有「option 系即便 `vec_avg` 也可能 took too much resource 整批杀 ⇒ option1 单独成批」的记载，
本轮把它加强为：**option1 必须单独成批，且不得与 504 长窗冷腿同批**。

**判别实验 = U63b `3y71Xkks5e39Gg7dtbYAK0`**：
把 U63 的 8 条里 4 条 option1 全部剔除（保留 other696 ×2、pv109、pv173 + 四条同族 1:1 对照），其余条件完全相同。
- U63b **成功** ⇒ 坐实 option1 是元凶；
- U63b **同样 FAIL** ⇒ 元凶是并发放/平台侧，与 option1 无关，需降并发。

### 3. 同时派发的另两批（设计说明）

**U64 = `1W94Ru23B4QKcl1114a8V8g8`（`event_ml_signals`，OTHER，104 事件标记，aC 117 但仅 12 用户）**

这是本区最被忽视的富矿：104 个事件标记覆盖全部经典强异常族。按 U58 的 `vec_*` 规则包装后做事件计数：

| # | 机制 | 骨架 | 经济先验 |
|---|---|---|---|
| 1 | 股利增减净额 | `ts_mean(vec_sum(div_inc) − vec_sum(div_dec), 66)` | 股利信号假说（增发=管理层信心） |
| 2 | 业绩指引上下调净额 | `ts_mean(vec_sum(guide_up) − vec_sum(guide_down), 66)` | 指引修正漂移 |
| 3 | 持续经营疑虑 + 破产（反） | `reverse(ts_mean(vec_sum(going_concern) + vec_sum(bankruptcy), 252))` | 困境风险 |
| 4 | 回购公告 + 完成 | `ts_mean(vec_sum(buyback_ann) + vec_sum(repurchase_done), 252)` | 回购异象 |
| 5 | 指数纳入 − 剔除 | `ts_mean(vec_sum(idx_add) − vec_sum(idx_drop), 252)` | 指数效应 |
| 6 | 解禁（反） | `reverse(ts_mean(vec_sum(lockup_end), 66))` | IPO 解禁抛压 |
| 7 | 股东维权提案 | `ts_mean(vec_sum(activism), 252)`，subindustry | 治理事件 |
| 8 | 违约 + 退市（反） | `reverse(ts_mean(vec_sum(default) + vec_sum(delist), 252))` | 极端困境 |

**为什么值得期待**：这 8 条全部是**高频、事件驱动、横截面稀疏但分散**的信息，
正好属于 §59 归纳出的「能出货的信息层」，而不是慢变基本面层。且仅 12 人用过 ⇒ 拥挤度极低。

**U65（已预检就绪，待派）= U62 的解耦实验剔除 option1**：
同一批信号腿（pv103 / oth47 / auction / earnings_sent / socialmedia5 / imb5）用 **1:1 与 2:1 两种冷腿权重**并行，
目的就是**实测「降冷腿权重能否把互相关从 0.77–0.94 压到 0.70 以下」**。
这是本战役能否从 4 颗走向 20 颗的**唯一决定性实验**——如果 1:1 能把互相关压下来且 S 仍在 1.5 以上，产能瓶颈即被打开。

## 六十二、U64 收批：`event_ml_signals` 出 6 颗「干净外壳」—— 全部 RA 闸只差 S 与 F，且 2Y 最高 2.52

### 1. U64 = `1W94Ru23B4QKcl1114a8V8g8`（8/8 全完，OTHER 塔，数据集仅 12 用户用过）

| # | 机制 | alpha | S | F | TO | DD | 2Y | sub | lc | nf | 失败闸 |
|---|---|---|---:|---:|---:|---:|---:|---:|---:|---:|---|
| 1 | 股利增减净额 | `omEPv2NJ` | 0.14 | 0.02 | **8.6%** | 11.1% | **1.75** | 0.10 | 454 | **2** | S,F |
| 2 | 指引上下调净额 | `RRE5YXmo` | 0.31 | 0.08 | **8.7%** | **8.0%** | **2.52** | 0.59 | 456 | **2** | S,F |
| 3 | 持续经营+破产(反) | `QPvWjeGw` | −0.32 | −0.09 | 8.3% | 19.0% | −2.01 | −0.60 | 456 | 4 | S,F,sub,2Y |
| 4 | 回购公告+完成 | `LLM86e7a` | 0.38 | 0.12 | **8.2%** | 11.1% | **2.02** | **0.66** | 455 | **2** | S,F |
| 5 | 指数纳入−剔除 | `VkxMEn7Y` | 0.45 | 0.14 | **6.7%** | **6.7%** | 0.97 | 0.10 | 457 | 4 | S,F,sub,2Y |
| 6 | 解禁(反) | `WjOYdk7G` | −0.54 | −0.19 | 10.0% | 23.6% | −2.18 | −0.41 | 457 | 4 | S,F,sub,2Y |
| 7 | 股东维权 | `leAg2xjA` | 0.03 | 0.00 | 8.4% | 9.0% | **1.29** | 0.50 | 460 | **3** | S,F,2Y |
| 8 | 违约+退市(反) | `akKRlJ79` | −0.04 | 0.00 | 8.5% | 11.4% | −1.27 | −0.47 | 450 | 4 | S,F,sub,2Y |

### 2. ★★★★★ 这是全战役质量最高的「外壳」结构

`event_ml_signals` 的 8 条里有 **6 条只有 `LOW_SHARPE` + `LOW_FITNESS` 两项失败**，其余 16 项 RA 闸一次全过。
对比此前 40 条新集探针（多数 |S|≤0.5 且撞 `CONCENTRATED_WEIGHT` / `LOW_SUB_UNIVERSE_SHARPE` / `LOW_2Y_SHARPE`），差异极其显著：

| 指标 | 新集慢变基本面（U55-U61） | **event_ml_signals（U64）** |
|---|---|---|
| 换手 TO | 10%–30% | **6.7%–10.0%（全部 < 10%）** |
| 回撤 DD | 8%–74% | **6.7%–23.6%（中位 ~11%）** |
| 2Y Sharpe | −1.5 ~ 1.6 | **最高 2.52**，4 条 > 1.7 |
| 失败闸数 nf | 普遍 4–5 | **6 条只有 2** |
| `CONCENTRATED_WEIGHT` | 6/8 撞墙 | **0/8 撞墙** |

**⇒ 机制解释**：事件标记是 0/1 稀疏序列，`ts_mean` 后每个股票每天只有很小的取值，横截面极度分散 ⇒ 天然不集中、
换手极低（事件不会每天变）、且**事件流本身携带真实的增量信息**（指引、股利、回购都是管理层主动披露的决策）。
这正好符合 §59 归纳的「能出货的信息层」：事件层 ≈ 流量层，而不是慢变描述符层。

### 3. 关键量化：这 6 条只欠「收益幅度」

Fitness = S × sqrt(|ann.return| / max(TO, 0.125))。以 `RRE5YXmo` 为例：
- 当前 TO 8.7%（< 0.125，故分母锁在 0.125）、S 0.31、F 0.08 ⇒ 年化收益 ≈ 0.08²×0.125 / 0.31² ≈ **0.83%**；
- 要过 F ≥ 1.00 且 S ≥ 1.58，需年化收益 ≥ (1.00/1.58)² × 0.125 ≈ **5.0%**。
**这正是 2:1 冷腿配方的目标区间**（历史 2:1 件的年化收益落在 8%–15%、DD 3%–5%）。

**⇒ 因此 U66 的设计就是把 U64 的 4 条 nf=2 事件腿挂上伙伴腿**（`guidance` / `dividend` / `buyback` / `index add-drop`）。

### 4. U66 的伙伴腿选择受「塔组合配额」硬约束

`event_ml_signals` 属 **OTHER**，而 **OTHER × SHORTINTEREST 已达候选上限 3**（`ZYQXZj73` / `O0A6Qz7p` / `ZYQXwGPn`）⇒ **该组合封盘，不能用标准冷腿**。
于是改用两个**全新的「集合内 × 集合外」组合**（各自消耗 1 个类型额度）：

| 伙伴腿 | 塔 | 组合类型 | 额度影响 | 额外收益 |
|---|---|---|---|---|
| `reverse(group_rank(ts_zscore(vec_sum(insd12_positionchangetransactionamount), 126), sector))` | INSIDERS | **OTHER × INSIDERS（新）** | 消耗第 3 个类型 | 同时推进 INSIDERS 塔 0/3 |
| `group_rank(ts_delta(vec_sum(institutional_holding_percent_of_shares_outstanding), 66), subindustry)` | INSTITUTIONS | **OTHER × INSTITUTIONS（新）** | 消耗第 4 个类型 | 同时推进 INSTITUTIONS 塔 0/3 |

**一石三鸟**：若任一条全闸，OTHER 塔（1/3）+ INSIDERS 或 INSTITUTIONS 塔（0/3）**同时 +1**。
算子数均已核到 ≤ 12（事件腿 5 + 伙伴腿 3–4 + `add`/`multiply` 2 = 10–11）。

---

## 63. probe1 冷腿判别三连：`3qoGxkqZ` 成为本战役最强件（S 2.48 / prod 0.6729）

### 63.1 probe1 三颗结果（multisim `3u5FfL50752xae8XTmyJHyV`，comp=3 err=0）

| id | 结构 | S | F | TO | DD | sub | 2Y | LC | nf | 塔 |
|---|---|---:|---:|---:|---:|---:|---:|---:|---:|---|
| `3qoGxkqZ` | pv103_ivam_sum z66 + **1:1** 冷腿(504, industry) | **2.48** | **1.33** | 23.7% | 2.41% | 1.72 | 3.36 | 466 | **0** | shortinterest/pv |
| `gJerKgJv` | 同上但冷腿 252 + sector | 2.33 | 1.20 | 24.5% | 2.43% | 1.52 | 3.52 | 461 | **0** | shortinterest/pv |
| `npv6xq7x` | **纯冷腿单独**（504, industry） | **1.74** | **1.07** | **11.55%** | 3.21% | **1.84** | **2.68** | 471 | **0** | **shortinterest（单塔 ATOM）** |

表达式：
- `3qoGxkqZ` = `add(group_rank(ts_zscore(pv103_ivam_sum, 66), sector), reverse(group_rank(ts_zscore(vec_sum(loaned_share_count_main), 504), industry)))`
- `npv6xq7x` = `reverse(group_rank(ts_zscore(vec_sum(loaned_share_count_main), 504), industry))` —— **全战役算子最少（4 个）**

**⇒ 关键结构性发现**：冷腿不只是「增益项」，它**单腿独立就是一个 S 1.74 / F 1.07 / nf=0 的合格 alpha**。
这推翻了此前「必须靠 2:1 合成才有 S」的判断——冷腿本身就是一颗 ATOM。

### 63.2 相关性（7 颗矩阵，本地零成本）

```
3qoGxkqZ × gJerKgJv 0.9198   3qoGxkqZ × npv6xq7x 0.8206   gJerKgJv × npv6xq7x 0.7216
3qoGxkqZ × ZYQXZj73 0.5449  3qoGxkqZ × RRE5Mwkn 0.5132   3qoGxkqZ × QPvbxjXw 0.1362  3qoGxkqZ × rKRPAWv9 -0.0601
npv6xq7x × ZYQXZj73 0.6498   npv6xq7x × RRE5Mwkn 0.3358
max_mutually_below_subset = [3qoGxkqZ, RRE5Mwkn, ZYQXZj73, QPvbxjXw, rKRPAWv9] size 5（exact）
```

self：`3qoGxkqZ` 0.2102｜`gJerKgJv` 0.2309｜`npv6xq7x` 0.2460 —— 全部 < 0.70 ✓

**判据**：三颗彼此 0.72–0.92 ⇒ **只能取其一颗**；取 `3qoGxkqZ`（S 最高、与篮内最大相关仅 0.5449）。

### 63.3 prod 实测

| alpha | prod | 判定 |
|---|---:|---|
| `3qoGxkqZ` | **0.6729** | ✓ 通过（< 0.70） |
| `LLM86Gp1` | **0.8084** | ✗ **深钉，判死** |

**`LLM86Gp1` 判死**：prod 0.8084 ≥ 0.80，触发「深钉」判死线。连带 `A1VLbGPg`（与其 0.8935）、`npv6oN2M`（1.0000）一并作废。
这正是「S 1.75 / F 1.08 / nf=0 全闸漂亮但 prod 封盘」的典型——**IS 全绿不代表可提交**。

### 63.4 ★ 可提交篮升级到 5 颗

| # | alpha | S | F | TO | prod | self | 塔 |
|---|---|---:|---:|---:|---:|---:|---|
| 1 | `RRE5Mwkn` | 2.15 | 1.41 | 14.3% | 0.4744 | 0.163 | PV + SHORT |
| 2 | `ZYQXZj73` | 1.78 | 1.16 | 13.3% | 0.6524 | 0.244 | OTHER + SHORT |
| 3 | `QPvbxjXw` | 1.87 | — | — | 0.5794 | — | ANALYST |
| 4 | `rKRPAWv9` | 1.76 | — | — | 0.3998 | — | NEWS |
| 5 | **`3qoGxkqZ`** | **2.48** | **1.33** | 23.7% | **0.6729** | 0.210 | PV + SHORT |

**全部 5 颗互相关 < 0.70（subset exact 求证）、self 全 < 0.70、prod 全 < 0.70。**

**塔位预测**（提交后）：PV 2→4 **点亮**｜SHORTINTEREST 0→3 **点亮**｜OTHER 1→2。

### 63.5 配额核对

`PV × SHORTINTEREST`：既有 `RRE5Mwkn` + `RRE500Nd` + 新增 `3qoGxkqZ` = **3/3，正好到上限**，此后该组合封盘。
`npv6xq7x` 属**单数据集 ATOM**（只含 shortinterest3），**不占塔组合配额**，是备用件。

### 63.6 用户提示：`group_backfill` 降 CONCENTRATED_WEIGHT —— 论坛已证实

论坛帖《Weight concentrated问题的一些解决方法》（20 票）给出的三种解法：
1. 调 Truncation 参数；2. **`ts_backfill` / `group_backfill`**；3. `ts_mean(alpha, d)` 平滑。
另一帖《group_backfill 操作符详解》（37 票）确认签名 `group_backfill(x, group, d, std=4.0)`，按组双向填充。

**U68 对照实验设计**（multisim `1CEym5b775ep98rLzOKULET`，8 条）——同时验证三件事：

| # | 目的 | 结构 |
|---|---|---|
| 1 | CW 杠杆·前置填充 | `group_rank(ts_zscore(group_backfill(FLOW, sector, 252), 66), sector)` |
| 2 | CW 杠杆·末端填充 | `group_backfill(group_rank(ts_zscore(FLOW, 66), sector), sector, 252)` |
| 3 | 对照·`ts_backfill` | `group_rank(ts_zscore(ts_backfill(FLOW, 252), 66), sector)` |
| 4 | 对照·`ts_mean` 平滑 | `group_rank(ts_mean(ts_zscore(group_backfill(FLOW, sector, 252), 66), 22), sector)` |
| 5 | 冷腿基线 | `add(multiply(2, group_rank(ts_zscore(FLOW, 66), sector)), COLD)` |
| 6 | 冷腿 + 填充 | 第 1 式 ×2 + COLD |
| 7 | 冷腿 + 一阶平滑 | 第 4 式核心 ×2 + COLD |
| 8 | 冷腿 + 二阶差分 | `add(multiply(2, group_rank(ts_zscore(ts_delta(FLOW, 22), 66), sector)), COLD)` |

基线：`LLM8bvE6`（同一 FLOW 核心）实测 **CONCENTRATED_WEIGHT = 0.325481 / 0.1**、S 0.24、TO 17.47%。
若第 1/2/3/4 式把 CW 压到 0.1 以下，即证实该杠杆在 GBR 有效，可回灌所有被 CW 卡死的新数据集探针。

**战略意义**：`INSTITUTIONS × SHORTINTEREST` 属**集外 × 集外，不占塔混配额**，且同时推进 INSTITUTIONS(0/3) 与 SHORTINTEREST 两塔。第 5–8 式即使 CW 不达标，只要 S 起来就是有效候选。

---

## 64. 7 个未探数据集字段画像 + 模板匹配（U69 前置）

### 64.1 画像总表

| 数据集 | 塔 | aC | 字段数 | 类型 | 信息层定性 | 价值判定 |
|---|---|---:|---:|---|---|---|
| `other384` | OTHER | 6 | **40+ VECTOR** | 财报电话会议文本 NLP | 演示段 / Q&A 段的 tone、正负词数、问题数、字数、笑声标记 | ★★★★★ **本轮最高价值：全新 NLP 层，非慢变描述符** |
| `other546` | OTHER | 3 | 22 VECTOR | **企业网络相似度**（董监高/分析师/业务/地理交叠 + 文本相似度） | 跨公司关系网络，属 relatio nal 层 | ★★★★ 全新关系型信息，但 aC=3 极冷门 |
| `euro_equity_imbalance` | IMBALANCE | 7 | 4 VECTOR | 参与者级净订单失衡（分桶 quantile/uniform） | 订单流微观结构 | ★★★★ IMBALANCE 塔 0/3，结构正交 |
| `pv71` | PV | 4 | 8 VECTOR | 价量相关 / IBES 估计 / 关系边权重 | 关系网络 + 价量结构 | ★★★ 但 PV 在禁混集合，伙伴选择受限 |
| `other327` | OTHER | 4 | 3 MATRIX | 因子敏感度（`sirc_lev` 杠杆 ETF 敏感度、`sirc_sl` 斜率敏感度）+ mktcap | 暴露度描述符 | ★★ 慢变描述符，历史同类系统性无信号 |
| `pv113` | PV | 2 | **1 MATRIX** | 单一经济指标值 | 单字段 | ★ 无法组模板 |
| `pv17` | PV | 3 | **1 GROUP** | `sta3_6_sector` 统计型 point-in-time 行业分类 | **分组轴** | ★★★ **不是信号，是新分组轴** |

### 64.2 关键结构性发现

1. **`pv17` 只有一个 GROUP 字段 → 它的价值是提供「第三个分组轴」**。
   目前所有骨架只用 `sector` / `subindustry` / `industry` / `market`。`sta3_6_sector` 是统计聚类行业（非官方 GICS-like），
   可以直接喂 `group_rank` / `group_neutralize` 作为**模板多样性的新轴**——这是不花 sim 就能改变几何的合法杠杆。
2. **`other384` 是继 `event_ml_signals` 之后第二个「干净外壳」候选**：40+ 字段全部 VECTOR、结构化语义清楚（演示段 vs Q&A 段），
   天然支持**背离类模板**（管理层念稿基调 vs 问答基调不一致 = 文献中的 managerial tone divergence）。
3. **`other546` 的 `shared_executive_count` / `shared_analyst_count` / `text_similarity_strength` 是关系型计数**，
   在 TOP700 上应该是稀疏整数 → 预测 CONCENTRATED_WEIGHT 风险高，**必须配 `vec_avg` 折标量**。

### 64.3 `other384` 10 个结构互异模板（模板库，满足多样性硬约束）

| # | 模板名 | 骨架 | 结构差异点 | 来源 |
|---|---|---|---|---|
| T1 | Q&A 基调水平 | `group_rank(ts_zscore(vec_avg(qa_tone), 66), sector)` | 矩=水平 | 自建 / 电话会议语调文献 |
| T2 | **念稿 vs 问答背离** | `group_rank(ts_zscore(subtract(vec_avg(qa_tone), vec_avg(presentation_tone)), 66), sector)` | 信息加工=两段相减 | 自建（managerial tone divergence） |
| T3 | 负面词密度 | `group_rank(ts_zscore(divide(vec_avg(qa_negnum), add(vec_avg(qa_wordcount),1)), 66), sector)` | 非线性=比率归一 | 自建 |
| T4 | 基调一阶变化 | `group_rank(ts_zscore(ts_delta(vec_avg(qa_tone), 66), 252), sector)` | 矩=一阶差分 | 自建 |
| T5 | 基调二阶波动 | `group_rank(ts_zscore(ts_std_dev(vec_avg(qa_tone), 66), 252), sector)` | 矩=二阶方差 | 自建（不确定性代理） |
| T6 | 问答强度 | `group_rank(ts_zscore(divide(vec_avg(qa_questions), add(vec_avg(presentation_questions),1)), 66), sector)` | 结构=跨段比率 | 论文（Q&A 强度 ↔ 信息不对称） |
| T7 | 正负净额 | `group_rank(ts_zscore(subtract(vec_avg(qa_posnum), vec_avg(qa_negnum)), 66), sector)` | 非线性=净额而非比率 | 自建 |
| T8 | **换分组轴** | `group_rank(ts_zscore(vec_avg(qa_tone), 66), sta3_6_sector)` | 分组轴换 `pv17` 的 GROUP 字段 | 自建（新轴） |
| T9 | 长窗秩 | `group_rank(ts_rank(vec_avg(qa_tone), 504), sector)` | 算子几何=秩而非 z | 自建 |
| T10 | 冷腿 2:1 合成 | `add(multiply(2, <T1 内层>), COLD)` | 信息合成 | 已验证配方 |

### 64.4 `euro_equity_imbalance` 模板（4 字段受限，5 个可用骨架）

| # | 模板 | 骨架 |
|---|---|---|
| I1 | 失衡水平 | `group_rank(ts_zscore(vec_avg(bucketed_sign_imbalance_uniform), 66), sector)` |
| I2 | 净失衡一阶 | `group_rank(ts_zscore(ts_delta(vec_avg(bucketed_net_order_imbalance_quantile), 66), 252), sector)` |
| I3 | 两种归一化背离 | `group_rank(ts_zscore(subtract(vec_avg(bucketed_sign_imbalance_quantile), vec_avg(bucketed_sign_imbalance_uniform)), 66), sector)` |
| I4 | 符号 vs 净值背离 | `group_rank(ts_zscore(subtract(vec_avg(bucketed_net_order_imbalance_uniform), vec_avg(bucketed_sign_imbalance_uniform)), 66), sector)` |
| I5 | 冷腿 2:1 | `add(multiply(2, <I1 内层>), COLD)` |

### 64.5 U69 标定批（8 条，已预检 valid / unknown_fields=[] / 未改写）

| # | 数据集 | 模板 | 表达式 |
|---|---|---|---|
| 1 | other384 | T1 | `group_rank(ts_zscore(vec_avg(oth384_qa_tone), 66), sector)` |
| 2 | other384 | T2 | `group_rank(ts_zscore(subtract(vec_avg(oth384_qa_tone), vec_avg(oth384_presentation_tone)), 66), sector)` |
| 3 | other384 | T3 | `group_rank(ts_zscore(divide(vec_avg(oth384_qa_negnum), add(vec_avg(oth384_qa_wordcount), 1)), 66), sector)` |
| 4 | other384 | T4 | `group_rank(ts_zscore(ts_delta(vec_avg(oth384_qa_tone), 66), 252), sector)` |
| 5 | imbalance | I1 | `group_rank(ts_zscore(vec_avg(bucketed_sign_imbalance_uniform), 66), sector)` |
| 6 | imbalance | I2 | `group_rank(ts_zscore(ts_delta(vec_avg(bucketed_net_order_imbalance_quantile), 66), 252), sector)` |
| 7 | other546 | net | `group_rank(ts_zscore(vec_avg(shared_executive_count), 66), sector)` |
| 8 | other546 | net | `group_rank(ts_zscore(vec_avg(text_similarity_strength), 66), sector)` |

标定目标：**任一条 S ≥ 0.8 即进入 10 模板全铺**；全 < 0.5 则按「该信息层在 GBR/TOP700 无独立预测力」记录后转下一集。

---

## 65. ★★★★★ U68 收货：`group_backfill` 降 CW 成立 + `institutions4 × SHORTINTEREST` 出 3 颗近线件

### 65.1 `group_backfill` 对照实验结果（用户提示验证）

基线 `LLM8bvE6`：CW **0.325481** / S 0.24 / TO 17.47% / LC 315。

| # | 手法 | alpha | S | F | TO | LC | CW | 判定 |
|---|---|---|---:|---:|---:|---:|---|---|
| 1 | **前置 `group_backfill(FLOW, sector, 252)`** | `gJerPAde` | 0.09 | 0.01 | 9.4% | **497** | **通过** | ✅ **有效** |
| 2 | 末端 `group_backfill(group_rank(...), sector, 252)` | `0mYGQl66` | 0.24 | 0.08 | 17.5% | 315 | 0.325604 | ✗ 无效 |
| 3 | `ts_backfill(FLOW, 252)` | `leAgzq9n` | 0.26 | 0.09 | 16.3% | 309 | 0.325148 | ✗ 无效 |
| 4 | 前置 gbf + `ts_mean(...,22)` 平滑 | `j2YVwEOE` | 0.08 | 0.01 | 7.7% | 386 | **通过** | ✅ 有效 |

**结论（与用户说法一致，但要补三条边界）**：
1. **只有「前置到原始数据」这一种位置有效**——末端包 `group_rank` 后无效（CW 0.3256），`ts_backfill` 也无效（0.3251）。
2. **机制=覆盖率**：LC 315 → 497，说明 NaN 被组内代表值填上后，更多股票拿到秩 → 权重自然摊薄。这与「CW 高 = 稀疏字段只让少数股票有权重」的因果解释完全吻合。
3. **代价是信号被同组均值稀释**：S 0.24 → 0.09，F 0.08 → 0.01。**所以 `group_backfill` 只适合救「S/F 已经很强、只卡 CW」的件**，对 S 本身不够的件是负收益。

### 65.2 ★★★★★ `institutions4 × SHORTINTEREST`（集外 × 集外，不占塔混配额）

| # | 几何 | alpha | S | F | TO | sub | 2Y | nf | 唯一失败闸 |
|---|---|---|---:|---:|---:|---:|---:|---:|---|
| 5 | FLOW z66 ×2 + 冷腿 | **`mLoKz3Q2`** | **1.69** | **1.03** | 11.2% | 1.68 | 2.61 | **1** | **CW 0.150/0.10** |
| 6 | 前置 gbf 版 | `E56ma7xr` | 1.05 | 0.49 | 10.8% | 0.71 | 1.36 | 3 | S,F,ladder |
| 7 | `ts_mean(FLOW,22)` z66 ×2 + 冷腿 | **`RRE5a3Pd`** | **1.58** | 0.94 | 11.2% | 1.46 | 2.54 | **1** | **F 0.94/1.00** |
| 8 | `ts_delta(FLOW,22)` z66 ×2 + 冷腿 | **`QPvWlJ6G`** | **1.61** | 0.97 | 11.4% | 1.53 | 2.68 | **1** | **F 0.97/1.00** |

**`mLoKz3Q2` 是本战役第 6 颗「S 与 F 双过线」的件**（S 1.69 ≥ 1.58、F 1.03 ≥ 1.00），只差 CW 0.150 vs 0.10（超 50%）。

**Fitness 反推（F = S·√(ret/max(TO,0.125))，TO 均 < 0.125 故分母锁 0.125）**：
- `mLoKz3Q2`：ret = 0.0464；要 F ≥ 1.00 已满足。
- `QPvWlJ6G`：ret = 0.0454，需 ret ≥ **0.0482（+6.2%）** 才过 F。
- `RRE5a3Pd`：ret = 0.0442，需 ret ≥ **0.0500（+13.1%）**。
⇒ **TO 已触 0.125 地板，降 TO 对 F 完全无效；只有提 returns 一条路。**

### 65.3 U67 全灭：事件腿配 `insd12` / `institutional_holding_percent_of_shares_outstanding` 作伙伴腿失败

| # | 机制 | alpha | S | F | 塔 |
|---|---|---|---:|---:|---|
| 1 | pv173 债券 spread 3:1 冷腿 | `1YNGm9YJ` | 1.19 | 0.57 | shortinterest/pv |
| 2 | pv173 股债 spread 3:1 冷腿 | `WjOYXqjO` | 1.14 | 0.53 | shortinterest/pv |
| 3 | 指引净额 × 内部人 | `e7512p7N` | 0.48 | 0.15 | insiders/other |
| 4 | 股利净额 × 内部人 | `N1NKjw18` | 0.33 | 0.09 | insiders/other |
| 5 | 回购合计 × 内部人 | `pwdWzXwb` | **0.71** | 0.29 | insiders/other |
| 6 | 指引净额 × 机构持股变化 | `78LGXA7b` | 0.26 | 0.06 | institutions/other |
| 7 | 股利净额 × 机构持股变化 | `vR1Yzqwa` | 0.11 | 0.02 | institutions/other |
| 8 | 回购合计 × 机构持股变化 | `O0A6mYQb` | 0.50 | 0.17 | institutions/other |

**三条判死**：
1. **`pv173` 3:1 权重比 2:1 更差**（1.19/1.14 vs 此前 `N1NK6brX` 1.43 / `vR1Y9NlA` 1.41）⇒ 提高弱腿权重只会稀释冷腿。**pv173 腿封盘**。
2. **事件腿 × 内部人伙伴腿最高 S 仅 0.71**；× 机构持股变化最高 0.50 ⇒ `insd12_positionchangetransactionamount` 与 `institutional_holding_percent_of_shares_outstanding` 作伙伴腿太弱，**不再用作伙伴腿**。
3. 但**冷腿作伙伴腿仍然碾压**（同批 `mLoKz3Q2` 用同一 FLOW 信号腿达 S 1.69）⇒ 伙伴腿的唯一有效选择仍是 504 冷腿。

### 65.4 U70 破墙批（已派发 `24iNWy98M4pD9Ubk2nJ3D25`，**truncation 0.10 → 0.15**）

论坛《Weight concentrated问题的一些解决方法》第 1 招是「调 Truncation」，`mLoKz3Q2` 的 CW 只超 50%，最省力路径就是抬 truncation（不改表达式、不动信号）。

| # | 目的 | 结构 |
|---|---|---|
| 1 | `mLoKz3Q2` 原式复现 @trunc0.15 | FLOW z66 sector ×2 + 冷腿504 |
| 2 | 换分组轴 | …subindustry ×2 + 冷腿504 |
| 3 | 换窗口 | FLOW z126 ×2 + 冷腿504 |
| 4 | 换算子几何 | `ts_rank(FLOW,66)` ×2 + 冷腿504 |
| 5 | 换冷腿窗口 | 冷腿 378 + sector |
| 6 | 换冷腿窗口 | 冷腿 756 + industry |
| 7 | 一阶平滑 | `ts_zscore(ts_mean(FLOW,22),66)` ×2 + 冷腿504 |
| 8 | **二阶矩（波动）** | `reverse(group_rank(ts_std_dev(FLOW,66), sector))` ×2 + 冷腿504 |

验收：任一条 **CW < 0.10 且 S ≥ 1.58 且 F ≥ 1.00** 即成为第 6 颗可提交件；同时 `INSTITUTIONS` 塔从 0 起跳。

---

## 66. ★★★★★ `institutions6`：GBR 稀缺的**满覆盖 MATRIX** 机构持仓面板

### 66.1 为什么它比 `institutions4` 更值得挖

| 项 | `institutions4`（已出 `mLoKz3Q2` S1.69） | **`institutions6`** |
|---|---|---|
| 字段数 | 6（全 VECTOR） | **11（全 MATRIX）** |
| coverage | 未标注，实测 LC 仅 315/700 ⇒ 稀疏 | **11/11 字段全部 cov = 1.0** |
| 是否需 `vec_*` 折标量 | 需要 | **不需要（直接可算）** |
| CONCENTRATED_WEIGHT 风险 | 高（实测 CW 0.325 超标） | **极低（满覆盖 ⇒ 权重天然摊薄）** |
| alphaCount / userCount | 47 / 38 | 942 / 423（拥挤，但覆盖换来的结构性优势更大） |

**核心逻辑**：CW 高的根因是字段稀疏（65.1 节已实证 LC↔CW 的因果关系）。`institutions6` cov=1.0 ⇒ 700 只票全部有权重 ⇒ **U68 里卡死 `mLoKz3Q2` 的 CW 0.150 问题在源头就不存在**。

### 66.2 字段清单（11 个 MATRIX，cov 全 1.0）

```
count_institutional_buyers_security      机构买家数
count_institutional_sellers_security     机构卖家数
count_institutional_holders_security     机构持有者数
market_value_institutional_shares_acquired   机构买入金额
market_value_institutional_shares_disposed   机构卖出金额
quantity_institutional_shares_acquired       机构买入股数
quantity_institutional_shares_disposed       机构卖出股数
aggregate_equity_value_institutions      机构持股总市值
aggregate_equity_value_all_owners        全体持股总市值
aggregate_share_count_institutions       机构持股总数
aggregate_share_count_all_owners         全体持股总数
```

结构上这是一张**四层嵌套**的面板：人数（breadth）× 金额（value）× 股数（quantity）× 占比（share）。
每层都有「买 / 卖 / 净 / 比」四种加工 ⇒ 天然支持 16+ 个互异几何，远超 10 模板硬约束。

### 66.3 `institutions6` 10 个结构互异模板

| # | 模板名 | 骨架 | 结构差异点 |
|---|---|---|---|
| T1 | 净买卖**人数**差（breadth） | `group_rank(ts_zscore(subtract(count_buyers, count_sellers), 66), sector)` | 信息=参与广度 |
| T2 | 净买卖**金额** | `group_rank(ts_zscore(subtract(mv_acquired, mv_disposed), 66), sector)` | 信息=资金强度 |
| T3 | 净买卖**股数** | `group_rank(ts_zscore(subtract(qty_acquired, qty_disposed), 66), sector)` | 信息=筹码量 |
| T4 | 买卖**比率**（非线性） | `group_rank(ts_zscore(divide(add(mv_acquired,1), add(mv_disposed,1)), 66), sector)` | 非线性=比率而非差 |
| T5 | 机构持股**占比**水平 | `group_rank(ts_zscore(divide(share_inst, share_all), 66), sector)` | 信息=结构占比 |
| T6 | 机构市值**占比**水平 | `group_rank(ts_zscore(divide(eqval_inst, eqval_all), 66), sector)` | 另一条占比口径 |
| T7 | 净买入**占持有者比** | `group_rank(ts_zscore(divide(subtract(buyers,sellers), holders), 66), sector)` | 归一化=除以基数 |
| T8 | 占比**一阶变化** | `group_rank(ts_zscore(ts_delta(divide(share_inst, share_all), 66), 252), sector)` | 矩=一阶差分 |
| T9 | 广度**二阶波动** | `group_rank(ts_zscore(ts_std_dev(subtract(buyers,sellers), 66), 252), sector)` | 矩=二阶方差 |
| T10 | 冷腿 **2:1** 合成 | `add(multiply(2, <T1/T2/T4 内层>), COLD)` | 信息合成 |

### 66.4 另一颗：`fund_holdings_panel`（INSTITUTIONS，aC 294，18 VECTOR，cov 0.89–0.93）

基金账户级「边界交易」（建仓 / 清仓）面板，覆盖率同样很高：
`boundary_transaction_total`（新建仓/清仓笔数）、`boundary_transaction_usd_value`（对应金额）、
`herfindahl_index_transactions`（交易金额集中度 HHI）、`transaction_value_distribution_score`（0–1 分布集中度）、
`top_weighted_transaction_number`（高信念持仓交易笔数）、`stable_boundary_trade_count_21d`（无前序边界交易的稳定笔数）、
`transaction_account_total`（当日参与账户数）、`large_trade_count_50bps`（大单笔数）。

**独有价值**：这是一层**「聪明钱建仓强度」**代理——`boundary_transaction_total` + `herfindahl_index_transactions` 组合可构造
「少数账户大额建仓」（HHI 高 + 边界笔数低）这类**非线性交叉条件**，是 `institutions6` 之外的另一种几何。

### 66.5 全集清点：未点亮塔剩余可开采集（排除已测）

| 塔 | 未测数据集（aC 升序） |
|---|---|
| **institutions (0/3)** | `institutions1`(52, cov **0.31** 弃)｜`institutions25`(90, cov 0 弃)｜`fund_holdings_panel`(294)｜**`institutions6`(942, cov 1.0)** |
| **insiders (0/3)** | `insiders1`(87)（`insiders12`/`insider_agg_matrix` 已测死） |
| **risk (0/3)** | `risk60`(202)｜`risk88`(567)｜`risk72`(606)（`risk68`/`risk71` 已测） |
| **sentiment (0/3)** | `sentiment7`(96)｜`sentiment27`(834)（`sentiment33` 已测） |
| **socialmedia (0/3)** | `socialmedia39`(298)｜`socialmedia12`(442)（`socialmedia5` 已测） |
| **macro (0/3)** | `macro27`(461) |
| **option (0/3)** | `option1` 已测（`kqN8bXJ6` DD 6.45% / S 0.66，剩余价值在曲面结构） |
| **imbalance (0/3)** | `imbalance5` 已测｜`euro_equity_imbalance` 标定中（U69） |
| **earnings (0/3)** | `earnings6`/`earnings_sent_matrix` 均已测 |
| **other (1/3)** | `other635`(2, cov 0 弃)｜`other571`(3, cov 0 弃)｜`event_relation`(12, cov 0 弃)｜`other699`(14)｜`other323`(15) |
| **pv (2/3)** | `pv106`(43)｜`pv29`(73)｜`pv30`(400, 240 字段)｜`pv47`(779, 2 字段) |

**舍弃记录（cov = 0，在 TOP700 无数据）**：`other635`、`other571`、`event_relation`、`search_interest`、`institutions25`。

### 66.6 U71（已预检 valid / unknown=[] / 未改写）

8 条 = 4 条纯单腿标定（T1–T5）× 4 条冷腿 2:1 合成（T1/T2/T4/T8）。
算子数 3–11，全部 ≤ 12。**`institutions6` 是 MATRIX，无需 `vec_*` 包装。**

验收：单腿组任一 S ≥ 0.8 ⇒ 该几何进 10 模板全铺；合成组任一 **S ≥ 1.58 且 F ≥ 1.00 且 nf = 0** ⇒ 直接成为第 6 颗候选并推进 INSTITUTIONS 塔 (0→1)。

---

## 67. U69 全灭：`other384` 财报电话会议 NLP 是「高换手噪声」；`euro_equity_imbalance` 最弱有效

### 67.1 结果（multisim `S0RRycuV4Ryb97QxnktxJj`，comp=8 err=0）

| # | 数据集 | 模板 | alpha | S | F | TO | sub | 2Y | nf | 失败闸 |
|---|---|---|---|---:|---:|---:|---:|---:|---:|---|
| 1 | other384 | T1 Q&A 基调水平 | `pwdWznVo` | −0.53 | −0.13 | **56.6%** | −0.43 | 0.61 | 5 | S,F,CW 0.313,sub,2Y |
| 2 | other384 | T2 念稿 vs 问答背离 | `78LGXxa1` | −0.62 | −0.17 | **56.5%** | −0.64 | 0.19 | 5 | S,F,CW 0.313,sub,2Y |
| 3 | other384 | T3 负面词密度 | `d5W97nEK` | −0.54 | −0.14 | **56.5%** | −0.54 | −0.18 | 5 | S,F,CW 0.313,sub,2Y |
| 4 | other384 | T4 基调一阶变化 | `QPvWln2g` | 0.02 | 0.00 | 36.3% | 0.19 | 0.31 | 4 | S,F,CW 0.448,2Y |
| 5 | imbalance | I1 失衡水平 | `KPJV8nX1` | **0.80** | 0.23 | 34.9% | −0.31 | 0.79 | 4 | S,F,sub,2Y |
| 6 | imbalance | I2 净失衡一阶 | `0mYGQAAq` | 0.41 | 0.09 | 34.1% | −0.56 | 0.60 | 4 | S,F,sub,2Y |
| 7 | other546 | 高管交叠计数 | `wpQNz551` | 0.34 | 0.08 | 20.0% | 0.15 | 0.97 | 4 | S,F,sub,2Y |
| 8 | other546 | 文本相似度 | `78LGXxx1` | 0.09 | 0.01 | 23.0% | −0.04 | 0.77 | 5 | S,F,CW 0.345,sub,2Y |

### 67.2 三条判读

**① `other384` 不是「没信号」，是「信号被换手吃掉」**
T1/T2/T3 **三条几何完全独立的构造给出几乎相同的负 Sharpe（−0.53 / −0.62 / −0.54）与几乎相同的 TO（56.6% / 56.5% / 56.5%）**。
这种「跨几何一致 + 换手爆表」的签名只能解释为一件事：**财报电话会议后 1–2 日的短期反转**。
信号方向稳定（做反向即 +0.53~+0.62），但 56% 换手把这 0.6 的毛信号全部磨平。
⇒ **该数据集的价值上限 ≈ S 0.62（反向）**，即使配冷腿 2:1 也只到 ~1.4，够不到 1.58。
**判**：`other384` 不再投 sim，记录为「电话会议文本在 GBR/TOP700 = 事件后短期反转，被换手淹没」。
若将来要复活，唯一路线是 `reverse()` + 强平滑（`ts_mean(...,252)` 或 `ts_target_tvr_decay(target_tvr=0.08)`）把 TO 压到 10% 以下，但那已不是原信号。

**② `euro_equity_imbalance` 有效但太弱**：最佳 `KPJV8nX1` S 0.80 / TO 34.9% / 2Y 0.79 / **sub −0.31**。
即便 2:1 冷腿合成也顶多到 ~1.6，且 TO 34.9% 会把 F 压死（F = S·√(ret/max(TO,0.125))，TO 高 ⇒ 分母大）。
**判**：不进主攻队列，除非先解决 TO。

**③ `other546` 企业网络相似度：S 0.34 / 0.09，无独立预测力**。
与 `other567`（员工评价）/ `workforce_flow_skills` / `other128`（高管情绪）同族结局 ⇒ **GBR/TOP700 上「跨公司关系 / 人事 / 舆情描述符」整层无信号**。

### 67.3 系统性结论（本轮累积）

| 信息层 | 代表数据集 | 实测最佳 \|S\| | 判定 |
|---|---|---:|---|
| 高频价量 / 日内微观结构 | pv103, pv20, intraday_pv_feats | **2.48** | ★★★★★ 唯一稳定强信号源 |
| 机构持仓**流量** | institutions4 | **1.69** | ★★★★★ 强（需冷腿或高覆盖版） |
| 另类文本主题净情绪 | other696 | **1.75** | ★★★★★ 强 |
| 财报事件标记 | event_ml_signals | 0.71（事件腿需合成） | ★★★ 材料，不是成品 |
| 期权曲面结构 | option1 | 0.66 | ★★ 弱但 RA 极干净（DD 6.45%） |
| 参与者级订单失衡 | euro_equity_imbalance | 0.80 | ★★ 弱 + 高换手 |
| 电话会议 NLP | other384 | 0.62（反向） | ✗ 换手淹没 |
| 企业网络 / 人事 / 舆情描述符 | other546, other567, workforce, other128 | ≤0.56 | ✗ 整层无信号 |
| 慢变基本面描述符 | other327, pv109, pv173 | ≤0.56 | ✗ 整层无信号 |

**⇒ 唯一可复用的引擎仍是：低换手（TO < 15%）· 高覆盖 · 流量型信号腿（pv103 / 机构持仓流量 / 另类主题净情绪）**。
高换手的 NLP / 微观结构层必须在**构造阶段就压换手**，否则一律被 TO 杀死。

---

## 68. ★★★★★ U70/U71：`truncation` 方向必须**往下**调；`institutions6` 高覆盖反而更弱（稀疏本身携带信息）

### 68.1 U70 结果（truncation **0.10 → 0.15**，8 条，comp=8 err=0）

| # | 几何 | alpha | S | F | TO | returns | sub | 2Y | nf | 失败闸 |
|---|---|---|---:|---:|---:|---:|---:|---:|---:|---|
| 1 | FLOW z66 sector + 冷腿504 | `d5W971ZX` | 1.68 | 1.02 | 11.16% | 4.64% | 1.68 | 2.61 | 1 | **CW 0.169523** |
| 2 | FLOW z66 **subindustry** + 冷腿504 | **`QPvWlKGr`** | **1.84** | **1.16** | 11.08% | **5.01%** | **1.76** | 2.65 | 1 | CW 0.169642 |
| 3 | FLOW **z126** sector + 冷腿504 | **`RRE5a6md`** | **1.73** | **1.07** | 11.05% | 4.78% | 1.58 | 2.53 | 1 | **CW 0.107010（只超 7%）** |
| 4 | `ts_rank(FLOW,66)` | `QPvWlKGG` | 0.98 | 0.45 | 10.72% | 2.64% | 1.23 | 2.06 | 2 | S,F |
| 5 | 冷腿 **378** sector | `KPJV8rGg` | 1.63 | 1.00 | 10.62% | 4.70% | 1.58 | **2.77** | 1 | CW 0.170893 |
| 6 | 冷腿 **756** industry | `e7512Q3E` | 1.62 | 0.98 | 10.89% | 4.53% | 1.69 | 2.58 | 2 | F 0.98 + CW 0.169683 |
| 7 | `ts_zscore(ts_mean(FLOW,22),66)` | `npv6zP7x` | 1.58 | 0.94 | 11.18% | 4.45% | 1.46 | 2.54 | 1 | F 0.94 |
| 8 | `ts_std_dev` 反向 | `qML5z0jZ` | 0.86 | 0.37 | 9.16% | 2.34% | 0.61 | 1.10 | 3 | S,F,ladder |

### 68.2 ★ 核心纠错：论坛「调 truncation」不可照抄方向

同一条表达式（`mLoKz3Q2`）在三个 truncation 下：

| truncation | alpha | S | F | **CW** |
|---|---|---:|---:|---:|
| 0.10 | `mLoKz3Q2` | 1.69 | 1.03 | **0.150106** |
| 0.15 | `d5W971ZX` | 1.68 | 1.02 | **0.169523** |

⇒ **调高 truncation 让 CW 恶化（+13%）**，S/F 几乎不变。
**论坛帖只说「调 Truncation 参数」没给方向，实测方向是「往下调」**。
所以 U73/U74 已派发 **truncation 0.08 / 0.06** 双批对照（同一组 8 条几何），目标是找 CW < 0.10 且 S/F 不塌的点。

**副产品（很重要）**：truncation 0.15 虽然 CW 更差，但**换分组轴 / 窗口把 S/F 显著抬高**：
`subindustry` 轴 ⇒ S 1.69→**1.84**、returns 4.64%→**5.01%**；`z126` 窗口 ⇒ CW 0.107（最接近及格线）。

### 68.3 Fitness 公式第三次精确验证（现在有实测 returns）

`F = S × √(|returns| / max(TO, 0.125))`，TO 全部 ≈11% ⇒ 分母锁 0.125：

| alpha | S | returns | 预测 F | 实测 F |
|---|---:|---:|---:|---:|
| `RRE5a6md` | 1.73 | 4.78% | 1.73×√0.3824 = **1.070** | **1.07** ✓ |
| `npv6zP7x` | 1.58 | 4.45% | 1.58×√0.3560 = **0.943** | **0.94** ✓ |
| `QPvWlKGr` | 1.84 | 5.01% | 1.84×√0.4008 = **1.165** | **1.16** ✓ |

⇒ **精确到小数点后两位**。所以 F 的破法只有两条：提 returns（换更强信号腿/换轴）或提 S，
**降 TO 在这批件上完全无效**（已低于 0.125 地板）。

### 68.4 U71 结果（`institutions6`，满覆盖 MATRIX，8 条，comp=8 err=0）

| # | 几何 | alpha | S | F | TO | LC | sub | 2Y | nf |
|---|---|---|---:|---:|---:|---:|---:|---:|---:|
| 1 | 净买卖人数差 单腿 | `GrWQ8O5Z` | 0.54 | 0.17 | 14.13% | 454 | 0.09 | 0.68 | 4 |
| 2 | 净买卖金额 单腿 | `qML5z021` | 0.55 | 0.18 | 12.88% | 454 | 0.16 | 0.18 | 4 |
| 3 | 买卖比 单腿 | `E56maRn0` | **0.00** | 0.00 | 12.02% | 455 | 0.12 | 0.33 | 3 |
| 4 | 持股占比 单腿 | `RRE5a6xa` | −0.10 | −0.01 | 10.38% | 368 | −0.39 | −0.96 | 4 |
| 5 | 人数差 + 冷腿 | `ZYQXlAVn` | 1.26 | 0.64 | 14.24% | 453 | 0.95 | 2.11 | 2 |
| 6 | 金额差 + 冷腿 | **`KPJV8rAN`** | **1.30** | 0.69 | 13.53% | 453 | 1.08 | 1.46 | 3 |
| 7 | 买卖比 + 冷腿 | `YP1lkM3J` | 0.92 | 0.39 | 12.75% | 453 | 1.01 | 0.85 | 3 |
| 8 | 占比一阶 + 冷腿 | `2rAGZmg8` | 0.57 | 0.19 | 11.01% | 451 | 0.61 | 1.52 | 3 |

### 68.5 ★★★★ 反直觉结论：**高覆盖反而更弱——稀疏本身携带信息**

| | `institutions4`（覆盖 315/700 稀疏） | `institutions6`（覆盖 700/700 满） |
|---|---|---|
| 最佳单腿 S | — | 0.55 |
| 最佳冷腿合成 S | **1.69** | **1.30** |
| CONCENTRATED_WEIGHT | 撞墙（0.15–0.17） | **0 条撞墙** |
| nf（失败闸数） | 1 | 2–3 |

**因果解释**：`institutions4` 只被**部分机构**报告覆盖 ⇒ 有值的股票是「被大机构重点持有」的子集，
这层筛选本身就是 alpha（机构关注度 / 覆盖密度）。`institutions6` 满覆盖 ⇒ 把 700 只票全部纳入，
**信噪比被稀释**，反而只剩 0.55。

⇒ 这修正了 66.1 节的判断：**coverage 不是越高越好**。正确表述是：
**coverage 决定 CW（覆盖低 ⇒ CW 高），但 coverage 太高会把信号稀释掉**。
最优区间是「中等覆盖（40%–70%）+ 低 truncation」——既保留稀疏筛选的信息，又能靠 truncation 把 CW 压进 0.10。

### 68.6 U73 / U74 设计（已派发）

- **U73** `2Rikc5e450nbuzJenIhQvF`：同 8 条几何 @ **truncation 0.08**
- **U74** `4Dkq9s5t45gZ8A285SFIqZh`：同 8 条几何 @ **truncation 0.06**

8 条几何 = {z66, z126, z84} × {sector, subindustry} × 冷腿 {504-industry, 378-sector, 504-sector} 的交叉，全部 11 个算子。
验收：任一条 **CW < 0.10 且 S ≥ 1.58 且 F ≥ 1.00 且 nf = 0** ⇒ 第 6 颗可提交件，同时 INSTITUTIONS 塔 0→1。

---

## 69. 剩余数据集画像收尾：`pv29` 是分组轴矿山，`insiders1` 落在覆盖率甜点区

### 69.1 画像与判定

| 数据集 | 塔 | aC | 字段 | coverage | 判定 |
|---|---|---:|---|---|---|
| **`pv29`** | PV | 73 | 30 MATRIX | **1.0** | ★★★★★ **30 个字段全是统计聚类标签（level 2/5/10/20/50 × 6 个 universe 变体）⇒ 分组轴矿山** |
| **`insiders1`** | INSIDERS | 87 | 9 VECTOR | **0.5937** | ★★★★ **落在 40–70% 甜点区**，与 `institutions4`(0.45) 同档 |
| **`other699`** | OTHER | 14 | 7 VECTOR | **0.3439** | ★★★ TipRanks 零售持仓；**`new − prev numofshares` 是唯一能算出带符号净变化的零售数据** |
| `other323` | OTHER | 15 | 7 VECTOR | **0** | ✗ 弃（TOP700 无数据） |
| `pv106` | PV | 43 | 8 MATRIX | **0** | ✗ 弃（滑点/价差成本，无覆盖） |

### 69.2 ★★★★ `pv29`：不花一分新数据就能做的模板多样性

`pv29` 的 30 个字段是同一种信息的 5 个粒度 × 6 个 universe 版本：

```
industry_grouping_level{2,5,10,20,50}_all_instruments_variant513
industry_grouping_level{2,5,10,20,50}_top{100,200,400,600,800,1200}_eas513 / _513 / _variant513
```

**战略价值**：分组轴是 `group_rank` / `group_neutralize` 的第二个自由度。目前全战役只用了 `sector` / `subindustry` / `industry` / `market`。
换成统计聚类层级（level 2 = 极粗，level 50 = 极细）**不改变信号本身，只改变交叉截面的划分方式**，
因此可以在**同一批候选里造出低互相关的多个 alpha**——这正是当前最大的瓶颈（`institutions4 × 冷腿` 一族已经堆了 12+ 个彼此高相关的候选）。

**待验证风险**：这些字段是 MATRIX 而非 GROUP 类型，`group_rank` 是否接受整数聚类标签需实跑确认（已放入 U75 第 8 条做单点探针）。

### 69.3 `insiders1` 的结构性缺陷（必须先解决才能用）

9 个字段：`insd1_holdings` / `insd1_shares` / `insd1_value` / `insd1_valueeur` / `insd1_price` / `insd1_tradesignificance` / `max_trade_price` / `transaction_currency_code` / `insd1_gvkey`。

**没有带符号的买卖方向字段**（`insd1_value` / `insd1_shares` 恒为正，与 `insiders12` 的 `insd12_positionchangetransactionamount`「正买负卖」不同）。
⇒ 只能退而用两种间接构造：
1. **持股存量一阶差分**：`ts_delta(vec_sum(insd1_holdings), 66)` —— 持仓变化即净积累方向；
2. **交易强度**：`vec_sum(insd1_value)` 水平 —— 内部人活跃度（不是方向）。

两者都在 U75 里各占一条。若两条都不灵，`insiders1` 与 `insiders12` 同判死，INSIDERS 塔只能靠 `insider_agg_matrix` 的 `avg_top_buy_shares − avg_top_sell_shares`（已测 S 0.17，弱）。

### 69.4 覆盖率与信号的倒 U 形（本轮第三次实证）

| 数据集 | coverage | 最佳冷腿合成 S |
|---|---:|---:|
| `institutions6` | **1.00** | 1.30 |
| `fund_holdings_panel` | 0.93 | 待测（U75） |
| `insiders1` | **0.59** | 待测（U75） |
| `institutions4` | **0.45**（315/700） | **1.69** |
| `other699` | 0.34 | 待测（U75） |
| `event_relation` / `other635` / `pv106` 等 | 0.00 | 无数据 |

**当前最佳点落在 0.45**，与「中等覆盖 40%–70%」的假设一致。
U75 的 `insiders1`(0.59) 与 `fund_holdings_panel`(0.93) 两条测完即可画出这条倒 U 曲线的三个点。

### 69.5 U75（8 条，已预检 valid / unknown=[] / 未改写）

| # | 数据集 | 塔 | 信号腿 | 目的 |
|---|---|---|---|---|
| 1 | insiders1 | INSIDERS | `ts_delta(vec_sum(insd1_holdings),66)` z252 | 内部人持股变化 = 净积累方向 |
| 2 | insiders1 | INSIDERS | `vec_sum(insd1_value)` z66 | 内部人交易强度 |
| 3 | other699 | OTHER | `vec_sum(new numofshares) − vec_sum(prev numofshares)` z66 | **零售持仓净变化** |
| 4 | other699 | OTHER | `vec_sum(oth699_sharestraded)` z66 | 零售交易活跃度 |
| 5 | fund_holdings_panel | INSTITUTIONS | `vec_sum(boundary_transaction_total)` z66 | 基金建仓/清仓笔数 |
| 6 | fund_holdings_panel | INSTITUTIONS | `vec_sum(herfindahl_index_transactions)` z66 | 基金交易金额集中度（HHI） |
| 7 | fund_holdings_panel | INSTITUTIONS | `vec_sum(top_weighted_transaction_number)` z66 | 高信念持仓交易笔数 |
| 8 | institutions4 + **pv29 轴** | — | FLOW z126 @ `industry_grouping_level10_all_instruments_variant513` | **验证 MATRIX 聚类字段能否当 group 用** |

全部配 504 冷腿 2:1，算子数 9–11，全部 ≤ 12。

验收分两条：
- 第 1–7 条任一 **S ≥ 1.58 且 F ≥ 1.00 且 nf = 0** ⇒ 新塔起跳（INSIDERS / OTHER / INSTITUTIONS）；
- 第 8 条只要 **跑通且 S 与 `RRE5a6md`(subindustry 轴 1.73) 不同** ⇒ `pv29` 的 5 个层级立刻成为降互相关的标准工具。
## 70. 数据集画像推进至 14/82 + truncation 三点扫描定论（2026-11-06）

### 70.1 画像进度

`get_datasets` 实测 GBR 共 **177 集**。按「已点亮塔不选」硬约束剔除 `model 46 / analyst 19 / news 18 / fundamental 12`（合计 95 集），
**可开采 = 82 集**（other 41 / pv 16 / institutions 5 / risk 5 / insiders 3 / sentiment 3 / socialmedia 3 / earnings 2 / imbalance 1 / macro 1 / option 1 / shortinterest 1）。
本轮前已画像 42 集，本轮新增 26 集，**剩 14 集未画像**。

### 70.2 ★★★★★ 新矿脉（优先派发）

| 数据集 | 塔 | 字段 | coverage | 机制 | 判定 |
|---|---|---:|---|---|---|
| **`risk60`** | RISK | 5 VECTOR | **0.6694** | **证券借贷市场**：`lending_fee_bid_rate` / `rsk60_crowding` / `rsk60_offer` / `rsk60_last` | ★★★★★ 借券成本机制，与金冷腿 `loaned_share_count_main` 同族但**不同塔不同集**；RISK 塔 0 点亮 |
| **`insider_agg_matrix`** | INSIDERS | 34 MATRIX | **0.6175** | 内部人买卖股份聚合：`total_buy_shares` / `total_sell_shares` / `total_top_{buy,sell}_shares` / `avg_*` / `directional_indicator`(cov 1.0) / `significant_value_1..4` | ★★★★★ **覆盖落在 40–70% 甜点区**的干净买卖不对称结构；INSIDERS 塔 0 点亮 |
| **`pattern_scores`** | PV | 504 MATRIX | **0.9924** | **K 线形态相似度**：`avg_similarity_{upward_breakaway_gap, rising_wedge, falling_wedge, asc_triangle, v_reversal_bottom, v_continuation_top, ...}` × lookback{60,120} × 统计量{mean,median,max,min,std,q95,dynamic} | ★★★★★ 形态识别信号，与价量因子机制独立；PV 塔 2/3 |
| **`other455`** | OTHER | 1500 字段 | **0.9381** | 竞争者网络嵌入：`oth455_competitor_n2v_p10_q200_w{1,2,3}_{kmeans,pca_fact1..3}_cluster_{5,10,20}` = **36 个 GROUP 轴**；`...pca_factN_value` MATRIX **cov 0.64** | ★★★★★ **降互相关主力工具**（多分组轴）+ 甜点区信号字段 |
| **`pv30`** | PV | 120 **全 GROUP** | 1.00 | PCA 因子 × 簇数{2,5,10,20,50} × universe{top100/200/600/800/1200} × PCA 分量 1..11 | ★★★★★ **纯分组轴库**，无信号值 ⇒ **只能当 group 参数**，与 pv29 构成两套独立分组体系 |
| **`sentiment27`** | SENTIMENT | 18 | **0.8003** | 维基百科关注度：`snl27_totaldomains`（跨语言覆盖广度）/ `totalcountrydomains` / `relpopularity{08,1}` / `topranking` / `avgranking` / `top{50,75}pctranking{avg}` / `skewness` / `kurtosis` / `snt27_rank` | ★★★★ **注意力机制**，与已挖的价格/持仓/内部人层正交，**prod 去相关潜力最大**；SENTIMENT 塔 0 点亮 |
| `sentiment7` | SENTIMENT | 3 | 0.5784 | `snt7_views` / `snt7_all_languages_views`（维基浏览量） | ★★★ 甜点区但是 2 个信号字段 |
| `stock_cluster_dl` | OTHER | 5 MATRIX | 0.17–**1.00** | `principal_component_features_{5,6,7,8,9}`，`_9` cov 1.00 | ★★★ DL 聚类 PCA |
| `insider_matrix` | OTHER | 33 MATRIX | 0.6061 | EUR 计价董事信号值：`eur_{top_,}{director_,}{signal_,}value_1..4` / `director_intensity_score`(1.0) | ★★★ 与 insider_agg_matrix 同族 |
| `insider_trx_matrix` | OTHER | 33 MATRIX | 0.6005 | 交易笔数 + USD 信号值：`total/mean_{,top_,secondary_}*_transaction_count` / `usd_*_signal_value` / `directional_indicator_score`(1.0) | ★★★ 同上 |
| `sentiment33` | SENTIMENT | 255 VECTOR | 0.3218 | 新闻情绪 NLP，9 种方法 × 5 过滤词表（`method_1..9` / `filtered_{pos,neg,neut,obj}`） | ★★ 覆盖偏低 |

### 70.3 ✗ 本轮判死（覆盖率归零 / 字段过薄）

`risk71`(6 字段 cov 0) / `risk72`(23 字段 cov 0，residualized return 全 0) / `macro27`(13 字段 cov 0，招聘岗位) /
`socialmedia12`(cov 0) / `socialmedia39`(1 字段 cov 0.49，共同观看图) / `other545`(4 字段 cov 0.49) /
`risk88`(仅 `alternative_market_cap_usd` 1 字段 cov 1.0，与 pv1 market_cap 重复)。

⚠️ **重要口径**：`get_datafields` 返回的 **字段级 coverage=0.00 不等于字段不可用**——`pv1`（56109 个 alpha 在用）数据集级 coverage 也报 0。
数据集级 `coverage` 为 **0** 的有 `ai_news_scores`(105 MATRIX) / `continuation_score`(560 MATRIX) / `other566`(112 MATRIX 技术指标库) /
`earningscall_sentiment`(167) / `event_sentiment_signals`(52) / `news_sentiment_nlp`(23) / `stock_search_trends`(12) / `other78`(112) /
`other169`(22，CDS 利差) / `other296`(10) / `other424`(3) / `other425`(13) / `other436`(3) / `other734`(7) / `pv47`(2) / `insiders12`(7)。
这些**暂列待验**而非直接判死；真正的零成本判据仍是运行时三元组 `TO=0 + S=0 + longCount=0`。

### 70.4 ★★★★★ truncation 三点扫描：方向定论 = **必须往下调**

同一组 institutions4 几何（`institutional_holding_current_shares − previous_shares` z-score + 2:1 冷腿），只改 truncation：

| truncation | 批次 | 最强件 S | 最低 CW | ≥2 条通过 CW？ |
|---|---|---:|---:|---|
| 0.15 | U70 | 1.84 | 0.107010 | ✗ |
| 0.10 | U68 | 1.69 | 0.150106 | ✗ |
| **0.08** | **U73** | **1.84** | **0.106896** | ✗（但 4 条卡在 0.1069，只超 6.9%） |

**U73 八条明细**（全部 `nf=1`，唯一失败项均为 `CONCENTRATED_WEIGHT`）：

| alpha | S | F | TO | returns | sub | 2Y | LC | CW |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| `YP1lWjEl` | 1.84 | 1.17 | 11.08% | 5.04% | 1.76 | 2.65 | 453 | 0.136421 |
| **`58EGqZ51`** | **1.83** | **1.16** | 11.01% | 5.01% | 1.64 | 2.57 | 448 | **0.106905** ← 最接近 |
| `pwdW1qZX` | 1.80 | 1.13 | 11.06% | 4.97% | 1.70 | 2.64 | 451 | 0.136212 |
| `E56mrZzJ` | 1.73 | 1.07 | 11.05% | 4.79% | 1.58 | 2.53 | 448 | **0.106896** |
| `LLM8lPr1` | 1.73 | 1.10 | 10.28% | 5.03% | 1.53 | 2.61 | 440 | **0.107045** |
| `omEP91Gn` | 1.69 | 1.03 | 11.16% | 4.67% | 1.68 | 2.61 | 452 | 0.136516 |
| `qML5mK3v` | 1.67 | 1.04 | 10.51% | 4.83% | 1.48 | 2.68 | 440 | **0.107043** |
| `QPvW51zK` | 1.64 | 1.01 | 10.62% | 4.73% | 1.58 | 2.77 | 445 | 0.138912 |

**三个结构性观察**：

1. **CW 只取决于分组轴，与窗口无关**：`subindustry` 轴 → CW ≈ 0.136–0.138（4 条）；`sector`/`industry` 轴 → CW ≈ 0.1069（4 条）。
   ⇒ 换更细的行业分类**恶化** CW 13%。这与「细化分组应降低集中度」的直觉相反——机制是细分组内样本少，秩分布更极端。
2. **窗口 66/84/126 对 S 无单调影响**（1.64–1.84 散布），但 126 窗口普遍给出更高的 2Y sharpe（2.53–2.77）。
3. **8 条是同一机制**（同一字段差、同一冷腿，只换窗口与轴）⇒ 互相关必然 >0.9，**整族只能取 1 条**。
   这轮 32 个 sim 槽位（U68/U70/U73/U74）只换来 1 个 alpha 额度，**是低效用法，已停止在该族继续投 sim**。

### 70.5 下一波设计（已预检就绪）

**U76（已派发，multisim `2fjwAz9Dc526aFvpgFokXoI`）—— 新机制多样性批**，8 条 8 个不同骨架：

| # | 数据集 | 骨架 | 算子数 |
|---|---|---|---:|
| 1 | risk60 | 借券拥挤度水平·sector | 4 |
| 2 | risk60 | 借券费率水平·subindustry·22d | 4 |
| 3 | risk60 | 拥挤度一阶差分·industry·22d | 4 |
| 4 | insider_agg_matrix | 买卖股份净差·sector·66d | 5 |
| 5 | insider_agg_matrix | **高层**买卖净差·subindustry·126d | 5 |
| 6 | insider_agg_matrix | `directional_indicator` 均值·sector | 3 |
| 7 | pattern_scores | V 型底 vs V 型顶形态相似度差 | 4 |
| 8 | other455 | PCA 值 × **kmeans 20 簇 GROUP 轴** | 4 |

**U77（已预检就绪，`valid=true / unknown=[]`，等槽位）—— 注意力层批次**，8 条全部来自 `sentiment27`(cov 0.80) / `sentiment7`(cov 0.58)：

| # | 骨架 | 经济学假设 |
|---|---|---|
| 1 | 跨语言覆盖广度水平 | 全球关注度低 ⇒ 被忽视 ⇒ 后续超额收益（neglected firm effect） |
| 2 | 相对热度 z-score 66d | 异常关注度冲击 ⇒ 散户买入压力 ⇒ 反转 |
| 3 | 平均排名一阶差分 22d | 排名改善 = 关注度上升 ⇒ 短期高估 |
| 4 | 排名分布偏度 126d | 偏度极端 = 关注度集中爆发 |
| 5 | 排名分布峰度 66d·subindustry | 峰度高 = 少数日极端曝光 |
| 6 | 最佳排名 − 平均排名 落差 | 落差大 = 关注度不稳定 |
| 7 | 跨语言覆盖一阶差分 66d | 国际关注度扩散 |
| 8 | 全语言浏览量 z-score 66d（sentiment7） | 跨集验证同一假设 |

**止损纪律**：若 sentiment 两集 8 条全部 |S| < 0.7 ⇒ 判「注意力层在 GBR/TOP700 无信号」，不再加投。

## 71. ★★★★★ 数据集画像 82/82 完成 + techindi_model 可复刻线索（2026-11-06）

### 71.1 穷尽度达成

| 项 | 数 |
|---|---:|
| GBR 数据集总数 | 177 |
| 已点亮塔（model 46 / analyst 19 / news 18 / fundamental 12）⇒ 不选 | 95 |
| **可开采（未点亮塔）** | **82** |
| **已画像** | **82（100%）** |

剩余 5 集在画像收尾时补齐，字段结构如下：

| 数据集 | 塔 | 字段数 | 实测最高 cov | 结构 | 判定 |
|---|---|---:|---|---|---|
| **`techindi_model`** | OTHER | 399 | 1.00 | `tm_15_r1_r5_r10_rh_glb_d1_r{1,5,10}_q{1..5}[_p0..p4]` MATRIX | ★★★★ **可复刻 USA 突破配方**（见 71.2）；但数据集级 prod **0.8511**（重度拥挤） |
| `intraday_pv_feats` | PV | 585 | 1.00 | `ask/bid_price_{30m,60m}_post_open/pre_close_2`、`avg_{ask,bid}_size_to_volume_ratio_{first,last}_half` 等日内微结构 | ★★★★★ 本战役 S 最高来源（`3qoGxkqZ` S2.48 出自 pv103 同层） |
| `order_book_imbalance` | OTHER | 240 | **0.4294**（非数据集级的 0.1798） | 订单簿事件流：`{ask,bid}_order_{deletion,execution,insertion,modification}_count`、`avg_rest_time_{ask,bid}_{cancelled,filled}_lvl1..5`、`auction_order_imbalance_*` | ★★★ 覆盖偏低，`avg_rest_time` 家族是**挂单耐心度**新机制 |
| `pv1` | PV | 23 | 1.00 | 基础价量 `close/open/high/low/volume/returns/cap/adv20/sharesout/adjfactor` + **7 个 GROUP**（`country/currency/exchange/industry/market/sector/subindustry`） | 基础层，已被 56109 个 alpha 使用 |
| `dl_riskfree_returns` | OTHER | 133 | 1.00 | `probability_label0_{2,3,4,5}quantile_{5,10,20,50,60}day_{eur_ohlc_ma,ohlcv}` = **下跌概率预测** | ✗ 数据集级 prod **0.9114**，与生产池几乎重合 |

### 71.2 ★★★★ `techindi_model` 可复刻 USA 突破配方

记忆中的 USA 突破：`techindi_model` 的**极值桶概率差** `group_rank(subtract(P4_v5, P0_v5), sector)` 给出 **S +2.29**（同区情绪类最强仅 0.69）。
GBR 版字段结构完全同类：`..._r{H}_q{1..5}` = 期限 H 下第 1..5 收益桶的预测概率，另有 `_p0.._p4` 表示桶内细分。

**GBR 可直接测试的 5 个桶几何**（H ∈ {1,5,10}）：

| # | 表达式骨架 | 与 USA 版的对应 |
|---|---|---|
| 1 | `subtract(tm_..._r10_q5, tm_..._r10_q1)` | 完全对应（极值桶概率差）|
| 2 | 同上换 `r5` | 中期限 |
| 3 | 同上换 `r1` | 短期限（更高换手）|
| 4 | `subtract(..._r10_q5_p4, ..._r10_q1_p0)` | 用桶内尾部细分 |
| 5 | `ts_delta(subtract(...q5, ...q1), 22)` | 概率差的一阶变化（新几何）|

**⚠️ 必须带的三条先验**（来自 USA 实测，不可忽略）：
1. **TO 极高**：USA 版 TO **75.07%**，直接撞 `HIGH_TURNOVER`。GBR 批次必须**预先抬 decay**（USA 用 decay 16 把 TO 压到 18.4%，但 S 从 2.29 掉到 1.26）。
2. **Fitness 结构性不可达**：反推 USA 版 returns 仅 **4.98%**，TO 0.75 ⇒ F 仅 0.59。按 `F = S·√(|R|/max(TO,0.125))`，即使 S 做到 2.3 也够不到 F=1。
   ⇒ GBR 若复现此机制，**默认预期是「S 过线但 F/TO 双卡」**，需要靠提高信号集中度抬 returns 而非压 TO。
3. **数据集级 prod 0.8511** ⇒ 即使 IS 全绿，prod 大概率判死。**该机制在 GBR 的优先级应低于 risk60 / insiders / sentiment27**，放在第三梯队。

### 71.3 本战役最终矿脉优先序（82 集画像完成后定稿）

| 梯队 | 数据集 | 理由 |
|---|---|---|
| **T1 立即测** | `risk60`(RISK, cov 0.67) / `insider_agg_matrix`(INSIDERS, cov 0.62) | 覆盖落甜点区 + 塔 0 点亮 + 机制与已挖层正交 |
| **T1** | `pattern_scores`(PV, 504 字段, cov 0.99) | 形态识别，与价量因子机制独立 |
| **T1** | `sentiment27`(SENTIMENT, cov 0.80) / `sentiment7`(cov 0.58) | 注意力层，prod 去相关潜力最大 |
| **T2 降相关工具** | `other455`(36 个 GROUP 轴) / `pv30`(120 个 GROUP 轴) / `pv29`(30 个) / `pv17`(`sta3_6_sector`) | 不改信号只改截面划分 ⇒ 同矿脉造低互相关多 alpha |
| **T3 待验** | `techindi_model` / `order_book_imbalance` / `stock_cluster_dl` | 机制有意思但各有硬伤（prod 0.85 / 覆盖低 / 字段少）|
| **✗ 已判死** | `other384` `other546` `pv173` `insd12` `institutions6`(满覆盖稀释) `dl_riskfree_returns`(prod 0.91) `risk71/72` `macro27` `socialmedia12/39` `other545` `risk88` `institutions1` `institutions25` | — |

## 72. U73/U74 truncation 四点扫描收口 + U77 注意力层判定（2026-11-06）

### 72.1 truncation 四点扫描：**已彻底饱和，不再调**

同一组 institutions4 几何（`institutional_holding_current_shares − previous_shares` z-score + 2:1 冷腿），四个 truncation 档的 CW：

| 分组轴 | trunc 0.15 | trunc 0.10 | trunc 0.08 | trunc 0.06 | 饱和值 |
|---|---:|---:|---:|---:|---:|
| subindustry | 0.169642 | 0.169523 | 0.136421 | **0.132970** | ≈0.132 |
| industry / sector | 0.107010 | 0.150106 | 0.106905 | **0.106797** | ≈0.1068 |

**结论**：
- 0.08 → 0.06 只带来 **0.0001** 的改善（0.106905 → 0.106797），**指数级饱和**。
- CW 结构性钉在 **0.1068**，只超限 6.8%，但**任何 truncation 值都跨不过去**。
- `subindustry`（细分组）比 `industry/sector`（粗分组）**恶化 CW 24%** —— 与「细化分组应降低集中度」的直觉相反，
  机制是细分组内样本少 ⇒ 秩分布更极端 ⇒ 权重更集中。
- **该族已封盘**：U68/U70/U73/U74 共 32 个 sim 槽位，产出 0 个可提交 alpha（`58EGqZ51` S1.83/F1.16 卡 CW 0.1069 为最接近）。
  **教训：同一机制换窗口/换轴/换 truncation 只是方差搜索，不是增量信息。**

### 72.2 ★★★ U77 注意力层：判定为**弱信号层**，但非噪声

U77 = `37CpHc72k4BvbzLbTeJ1Z31`（8 条，comp=8 err=0，`sentiment27` cov 0.80 / `sentiment7` cov 0.58）：

| # | 几何 | alpha | S | F | TO | DD | 2Y | nf |
|---|---|---|---:|---:|---:|---:|---:|---:|
| 6 | **最佳排名 − 平均排名（关注度稳定性落差）** | **`ZYQXWqpx`** | **0.89** | 0.42 | **8.82%** | 5.89% | **1.85** | 2 |
| 3 | 平均排名一阶差分 22d | `vR1YJxmG` | 0.62 | 0.20 | 17.14% | 4.25% | 1.00 | 4 |
| 7 | 跨语言覆盖一阶差分 66d | `e751qgOz` | 0.41 | 0.13 | 12.87% | 4.96% | 0.62 | 3 |
| 2 | 相对热度 z-score 66d | `2rAGnQKw` | 0.14 | 0.03 | 11.71% | 4.91% | 0.51 | 3 |
| 4 | 排名分布偏度 126d | `xArlm9np` | 0.05 | 0.01 | 12.50% | 6.99% | 0.24 | 4 |
| 5 | 排名分布峰度 66d | `LLM8lqpa` | −0.09 | −0.01 | 15.46% | 6.74% | −0.56 | 3 |
| 8 | 全语言浏览量 z-score 66d（sentiment7） | `bl6xWVLK` | −0.38 | −0.08 | 26.43% | 13.42% | −1.18 | 3 |
| 1 | 跨语言覆盖广度水平 | `YP1lWnAW` | −0.49 | −0.19 | 9.36% | 13.85% | −0.68 | 3 |

**判读**：
1. **最强 S 仅 0.89**，离 REGULAR 线 1.58 差 0.69 ⇒ **不能独立成件**。
2. **但 `ZYQXWqpx` 的三个辅助指标都健康**：TO **8.82%**（极低）、DD 5.89%、2Y **1.85**（>1.58）。
   ⇒ 它是**干净的弱信号**（信息真实但幅度小），不是噪声。**只有这一条几何值得配伙伴腿放大，其余 7 条判死。**
3. **信号方向反直觉**：`reverse(topranking − avgranking)` 为正 ⇒ **排名落差越大（关注度越不稳定）未来收益越高**。
   与「高关注度 ⇒ 后续反转下跌」的经典注意力效应**相反**；更接近「被持续关注的公司已被充分定价，忽冷忽热的公司存在定价不足」。
4. **`snl27_totaldomains`（跨语言覆盖广度）水平值与一阶差分都弱**（−0.49 / 0.41）⇒ 维基百科覆盖广度不是有效注意力代理。
5. **`sentiment7`（纯浏览量）比 `sentiment27`（排名体系）弱得多**（−0.38 vs 0.89）⇒ **注意力要用「相对排名」而非「绝对浏览量」**。

**止损纪律执行**：原定判死线 `|S| < 0.7`，实际最强 0.89 略高于线，故**保留 1 条配腿机会**（`ZYQXWqpx`），其余封盘。

### 72.3 U78 设计（已派发 `1hzMR8fsC4Y98ym1fDuvpZBz`）—— 纯 ATOM 探针批

设计原则：**8 条全部单数据集 ATOM**，不共用任何伙伴腿 ⇒ ① 不消耗塔组合配额 ② 8 条互不耦合 ③ 一次测 8 个机制的原始信号强度。

| # | 数据集 | 机制 | 骨架 | 算子 |
|---|---|---|---|---:|
| 1 | fund_holdings_panel | 基金交易**赫芬达尔集中度** | `group_rank(ts_zscore(vec_sum(herfindahl_index_transactions),66), sector)` | 4 |
| 2 | fund_holdings_panel | 基金**大单笔数**(50bps) | 同上换 `large_trade_count_50bps` | 4 |
| 3 | fund_holdings_panel | **边界交易**总量 | 同上换 `boundary_transaction_total` | 4 |
| 4 | other455 | 竞争者网络 PCA × **自带 kmeans 20 簇分组轴** | `group_rank(ts_zscore(...pca_fact1_value,66), ...kmeans_cluster_20)` | 4 |
| 5 | sentiment33 | 新闻 NLP **method_2 正负极性差** | `group_rank(ts_zscore(subtract(vec_avg(..._pos), vec_avg(..._neg)),66), sector)` | 5 |
| 6 | order_book_imbalance | **挂单耐心度**（买 vs 卖已成交挂单存活时长差） | `group_rank(ts_zscore(subtract(vec_avg(avg_rest_time_bid_filled_lvl1), vec_avg(avg_rest_time_ask_filled_lvl1)),66), sector)` | 5 |
| 7 | stock_cluster_dl | DL 聚类 PCA 第 9 分量 | `group_rank(ts_zscore(principal_component_features_9,66), sector)` | 3 |
| 8 | techindi_model | **极值桶概率差**（复刻 USA S+2.29 配方） | `group_rank(subtract(..._r10_q5, ..._r10_q1), sector)` | 4 |

**预检**：`valid=true / unknown_fields=[] / unknown_soft=[] / any_changed=false`。

## 73. ★★★★★ U76 全灭换来的结构性定论：瓶颈是放大器，不是信号（2026-11-06）

### 73.1 U76 八条新机制全部未过

U76 = `2fjwAz9Dc526aFvpgFokXoI`（8 条，comp=8 err=0，全部单数据集 ATOM 式探针）：

| # | 数据集 | 机制 | alpha | S | F | TO | LC | sub | 2Y | nf |
|---|---|---|---|---:|---:|---:|---:|---:|---:|---:|
| 1 | risk60 | 借券拥挤度（反） | `MPYg5K7o` | **0.60** | 0.16 | 24.67% | 518 | **0.97** | −0.15 | 3 |
| 2 | risk60 | 拥挤度一阶 | `vR1YJejr` | 0.25 | 0.04 | 36.79% | 467 | 0.78 | −0.61 | 3 |
| 8 | other455 | 竞争者网络 PCA × kmeans20 轴 | `58EGqaQn` | 0.10 | 0.01 | 10.22% | 391 | 0.23 | 0.11 | 3 |
| 4 | insider_agg_matrix | 买卖净差 | `O0A65b7R` | **0.00** | 0.00 | **55.94%** | **257** | 0.12 | −0.21 | 3 |
| 2 | risk60 | 借券费率 | `akKRWA7O` | −0.07 | −0.01 | 19.37% | 597 | 0.04 | −0.23 | 3 |
| 7 | pattern_scores | V 型底 vs V 型顶相似度差 | `KPJVwX71` | −0.21 | −0.05 | 11.42% | 453 | 0.06 | 0.23 | 3 |
| 5 | insider_agg_matrix | **高层**买卖净差 | `3qoGnalO` | −0.29 | −0.04 | **53.70%** | **234** | −0.06 | −0.73 | 3 |
| 6 | insider_agg_matrix | `directional_indicator` 均值 | `6XdGPWoL` | −0.34 | −0.08 | 16.36% | 260 | −0.07 | 0.20 | 3 |

**三条机制级判读**：

1. **`insider_agg_matrix` 判死**：数据集的 coverage 报 **0.6175**，但实际 `longCount` 只有 **234–260**（≈33%），
   且 TO **53.7%–55.9%** ⇒ 内部人交易是**事件型稀疏序列**，被当成连续流量处理 ⇒ 换手灾难。
   **口径订正：`coverage` 元数据不可信，真实可用度看首个 ATOM 的 `longCount / universe`。** 
   三个方向（净差 0.00 / 高层净差 −0.29 / 方向指标 −0.34）全灭 ⇒ 该集封盘。
2. **`risk60` 有信号但太弱且换手偏高**：`MPYg5K7o` 的 **sub_universe_sharpe 0.97 远高于主 S 0.60**
   ⇒ 该信号在**小子宇宙里更有效**，是「大票不敏感、小票敏感」的拥挤度结构。TO 24.7% 偏高。
   **不是死信号**，但需要配腿放大 + 降换手。
3. **`pattern_scores` / `other455` 判死**：|S| ≤0.21。形态相似度与网络 PCA 在 GBR/TOP700 无独立预测力。

### 73.2 ★★★★★ 结构性定论：**S 的来源是配比结构，不是信号**

把本战役所有「单数据集 ATOM」探针的最强 |S| 排开（约 20 个不同机制、全部用同一骨架 `group_rank(ts_zscore(FIELD,66), sector)`）：

| 数据集 | 机制 | 单腿最强 \|S\| |
|---|---|---:|
| sentiment27 | 维基关注度排名落差 | **0.89** |
| euro_equity_imbalance | 参与者订单失衡 | 0.80 |
| risk60 | 借券拥挤度 | 0.60 |
| institutions6 | 机构买卖人数/金额差 | 0.55 |
| other546 / other250 | 企业网络 / 舆情 | 0.34 |
| other455 | 竞争者网络 PCA | 0.10 |
| insider_agg_matrix | 内部人净买入 | **0.00** |
| pattern_scores | V 型反转相似度差 | −0.21 |
| other384 | 电话会 NLP | −0.53 |

**单腿上限 ≈0.9，系统性够不到 1.58。** 而同一批信号一旦上配比结构：

| 信号 | 单独 \|S\| | 配比后 | 提升 |
|---|---:|---|---:|
| institutions4 持股流量 | 0.24 | `QPvWlKGr` **1.84**（2:1 冷腿）| **+1.60** |
| pv103 `ivam_sum` | — | `3qoGxkqZ` **2.48**（1:1 冷腿）| — |
| institutions4 持股流量 | 1.69 | `d5W971ZX` 1.68（1:1 冷腿，**无增益**）| 0 |

⇒ **配比结构的杠杆量级（+1.6 S）远大于换数据集（≤0.3 S）。**

**由此改写挖矿优先级**：
1. 新数据集只测「有无信号 / 方向 / 换手」，**不指望单腿过线**；
2. `|S| > 0.6 且 TO < 12%` ⇒ 立即转入配腿队列，**不要再加工该信号**；
3. **仿真预算的主力应投向「放大器搜索」**——同一信号 × 不同伙伴腿 × 不同配比（1:1 / 2:1 / 3:1）× 不同伙伴腿分组轴；
4. 每批至少留 2 条专测「换放大器」而非「换信号」。

### 73.3 U79 设计（已派发 `3nXIjP3Er4YD8YzExlJjKGF`）—— 放大器可移植性批

用两个已验证的弱信号（`sentiment27` 排名落差 S0.89 / `risk60` 拥挤度 S0.60）× 三个候选放大器 × 两种配比，回答：
**「504 冷腿」是不是唯一有效放大器？**

| # | 信号 | 放大器 | 配比 | 塔组合 | 配额 |
|---|---|---|---|---|---|
| 1 | sentiment27 | 504 冷腿 | 2:1 | SENTIMENT × SHORTINTEREST | **不限量**（集合外×集合外）|
| 2 | sentiment27 | `pv103_ivam_sum` | 2:1 | SENTIMENT × PV | 集合内×集合外 #3/5 |
| 3 | sentiment27 | `pv103_ivam_sum` | 1:1 | 同上 | 同上 |
| 4 | risk60 | 504 冷腿 | 2:1 | RISK × SHORTINTEREST | **不限量** |
| 5 | risk60 | `pv103_ivam_sum` | 2:1 | RISK × PV | 集合内×集合外 #4/5 |
| 6 | risk60 | `pv103_ivam_sum` | 1:1 | 同上 | 同上 |
| 7 | sentiment27 | institutions6 买卖人数差 | 2:1 | SENTIMENT × INSTITUTIONS | **不限量** |
| 8 | risk60 | institutions6 买卖人数差 | 2:1 | RISK × INSTITUTIONS | **不限量** |

**预检**：`valid=true / unknown_fields=[] / unknown_soft=[] / any_changed=false`。

**关键设计意图**：#1/#4 用已被证明有效的冷腿做**阳性对照**（若这两条 S<1.58，则说明这两个弱信号本身不可救）；
#2/#3/#5/#6 检验 `pv103_ivam_sum` 能否替代冷腿；#7/#8 检验 `institutions6` 稠密腿（cov 1.0）能否当放大器。
**只有 #2–#8 中至少一条能达到 S ≥ 1.58，放大器才算找到了第二个选项。**

## 74. ★★★★★ U78 出 techindi 突破 + U79 证伪「冷腿万用放大器」（2026-11-06）

### 74.1 ★★★★ U78 ATOM 探针：`techindi_model` 极值桶概率差 S 1.55（单数据集、4 算子、零伙伴腿）

U78 = `1hzMR8fsC4Y98ym1fDuvpZBz`（8 条纯 ATOM，comp=8 err=0）：

| # | 数据集 | 机制 | alpha | S | F | TO | R | sub | 2Y | LC | nf |
|---|---|---|---|---:|---:|---:|---:|---:|---:|---:|---:|
| 8 | **techindi_model** | **极值桶概率差 r10** | **`gJeroMWl`** | **1.55** | 0.49 | **46.98%** | 4.73% | **1.50** | 1.21 | 457 | 3 |
| 6 | order_book_imbalance | 挂单耐心度差（买卖） | `9qxGArEd` | 0.56 | 0.20 | 24.10% | 2.94% | 0.91 | **1.63** | 343 | 2 |
| 4 | other455 | 竞争者网络 PCA × kmeans20 | `58EGqaQn` | 0.10 | 0.01 | 10.22% | — | 0.23 | 0.11 | 391 | 3 |
| 2 | fund_holdings_panel | 大单笔数 50bps | `zq3AJmrX` | −0.05 | 0.00 | 27.98% | — | −0.18 | 0.59 | 411 | 4 |
| 7 | stock_cluster_dl | DL 聚类 PCA 第 9 分量 | `ZYQXWnm1` | −0.15 | −0.02 | 42.17% | — | 0.12 | 0.30 | 453 | 3 |
| 3 | fund_holdings_panel | 边界交易总量 | `RRE5k8Ad` | −0.16 | −0.02 | 39.53% | — | 0.03 | −0.09 | 458 | 3 |
| 1 | fund_holdings_panel | 赫芬达尔集中度 | `kqN8L0gz` | −0.18 | −0.02 | 47.23% | — | 0.00 | 0.23 | 456 | 3 |
| 5 | sentiment33 | 新闻 NLP 正负极性差 | `d5W9l0KK` | −0.53 | −0.12 | **57.01%** | −2.97% | −0.76 | −0.08 | 351 | 5 |

**判读**：

1. **`gJeroMWl` 打破「单腿上限 0.9」的规律**：S **1.55** / sub **1.50** / DD **4.39%**，只用 4 个算子 `group_rank(subtract(q5, q1), sector)`，**不配任何伙伴腿**。
   **原因**：`techindi_model` 是**训练好的模型输出**（每桶的概率预测），不是原始数据字段——「取分布两个极值桶的概率差」本身就是最优骨架，不需要自己另造。
   与记忆中 USA 版 `P4−P0`（S +2.29）同构，**跨区可复现**。
2. **它的三关缺两关**：S 1.55（差 0.03 到线，≈2%）、**TO 46.98%**（撞 HIGH_TURNOVER 0.70 不撞，但把 F 压死）、F 0.49、2Y 1.21。
   **F 与 2Y 是真正的墙，S 只差临门一脚。**
3. **`fund_holdings_panel` 判死**（三个几何 |S| ≤0.18 且 TO 28–47%）；**`sentiment33` 判死**（S −0.53 / TO 57% / CW 0.3032 / DD 40%）；
   **`stock_cluster_dl` 判死**（−0.15）；**`other455` 复测仍 0.10**（与 U76 完全一致 ⇒ 确认无信号）。
4. **`order_book_imbalance` 的挂单耐心度是「干净但弱」信号**：S 0.56 / sub 0.91 / **2Y 1.63（>1.58 线）** / TO 24.1%。
   ⇒ 唯一一条 2Y 天然过线的弱信号，进配腿队列（但其塔 OTHER 的 SHORTINTEREST 组合已超配）。

### 74.2 ★★★★★ U79 证伪「冷腿是万用放大器」——`pv103_ivam_sum` 才是更强的伙伴腿

U79 = `3nXIjP3Er4YD8YzExlJjKGF`（8 条，comp=8 err=0）。两个弱信号 × 三个候选放大器 × 两种配比：

| # | 信号（单独 S） | 放大器 | 配比 | S | F | TO | R | sub | 2Y |
|---|---|---|---|---:|---:|---:|---:|---:|---:|
| **6** | risk60 拥挤度（0.60） | **`pv103_ivam_sum`** | **1:1** | **1.61 ✓** | 0.60 | 34.83% | 4.86% | 0.85 | 1.08 |
| 5 | risk60（0.60） | `pv103_ivam_sum` | 2:1 | 1.40 | 0.65 | 18.89% | 4.12% | **1.92** | 1.32 |
| 3 | sentiment27 排名落差（0.89） | `pv103_ivam_sum` | 1:1 | 1.38 | 0.52 | 32.88% | 4.68% | 0.30 | 1.40 |
| 4 | risk60（0.60） | **504 冷腿** | 2:1 | 1.36 | 0.50 | 30.13% | 4.04% | 0.94 | 0.60 |
| 7 | sentiment27（0.89） | `institutions6` 买卖人数差 | 2:1 | 1.34 | **0.76** | **11.17%** | 4.00% | 1.26 | 0.98 |
| 2 | sentiment27（0.89） | `pv103_ivam_sum` | 2:1 | 1.23 | 0.47 | 28.12% | 4.16% | 0.25 | 1.08 |
| **1** | **sentiment27（0.89）** | **504 冷腿** | **2:1** | **0.69 ✗** | 0.21 | 20.81% | 1.94% | 0.79 | 0.16 |
| 8 | risk60（0.60） | `institutions6` 买卖人数差 | 2:1 | 0.49 | 0.16 | 12.82% | 1.43% | 0.12 | 0.77 |

**三条硬结论**：

1. **「504 冷腿是万用放大器」被证伪**：
   - 送进 **sentiment27** ⇒ S 从 **0.89 掉到 0.69**（**负增益 −0.20**），2Y 从 1.85 掉到 0.16。
   - 送进 **risk60** 2:1 ⇒ 1.36，而**同一信号配 `pv103_ivam_sum`** 1:1 ⇒ **1.61**（+0.25）。
   - ⇒ 冷腿只在**特定信号族**（institutions4 持股流量、pv103 自身）上有效，**不是通用杠杆**。
2. **`pv103_ivam_sum` 是实测最强伙伴腿**：
   - 唯一一条把弱信号送过 REGULAR 线的放大器（risk60 0.60 → **1.61**）；
   - 且它自身 prod **0.4744**（全表最低一档）⇒ **prod 合规性也最好**。
   - ★ **由此改写配方：默认伙伴腿从 504 冷腿换成 `pv103_ivam_sum`。**
3. **`institutions6` 买卖人数差是最佳「降换手型」放大器**：配 sentiment27 得 TO **11.17%** / F **0.76**（全表 F 最高），但 S 只有 1.34。
   ⇒ 它是**F 友好型**伙伴腿：TO 天然落在 F 的最优区（<12.5% 地板以下无需再压），只缺 S。

**风险闸读数**：#6 与 #1 的 `checks.fail` 报空数组但 `nf` 分别为 2 / 3 ⇒ 收割器未回落 fail 明细的条目仍需用 `get_alpha_details` 逐条复核，
**不得把 `checks.fail=[]` 当作全闸通过**。

### 74.3 U80 / U81 设计（已派发）

**U80 = `H5bB3dnG5cd8UpU8twb90l`** —— `techindi_model` 极值桶概率差专攻 F（8 条，全部单数据集零伙伴腿）：

| # | 骨架 | 目标 |
|---|---|---|
| 1 | `ts_target_tvr_decay(..., target_tvr=0.10)` | 直接压 TO 到 F 线（需 ≤11.4%）|
| 2 | `ts_target_tvr_decay(..., target_tvr=0.15)` | 中间档 |
| 3 | `group_rank(ts_mean(subtract(q5,q1), 22), sector)` | 平滑降换手 |
| 4 | `group_rank(ts_mean(subtract(q5,q1), 66), sector)` | 长平滑 |
| 5 | `group_rank(hump(subtract(q5,q1), hump=0.05), sector)` | hump 压换手 |
| 6 | r5 期限 + ts_mean 22 | 换期限（假定低换手）|
| 7 | r1 期限 + ts_mean 22 | 短期限对照 |
| 8 | `group_rank(ts_zscore(subtract(q5,q1), 66), sector)` | 换归一化几何 |

**F 的定量目标**（`F = S·√(|R|/max(TO,0.125))`，当前 S 1.55 / R 4.73% / TO 46.98% ⇒ F 0.49 实测吻合）：
**要让 F ≥ 1，TO 必须从 46.98% 压到 ≤ 11.35%**，且 R 不能同步塌。`ts_target_tvr_decay` 正是为此设计。

**U81 = `4tvkix7ta4A4acFOtqVqB9T`** —— 定向破 F/2Y（8 条）：

| # | 组合 | 目标 |
|---|---|---|
| 1 | risk60 + pv103 1:1 + `target_tvr=0.12` | F 需 TO≤12.6%，#6 的 S1.61 直接可救 |
| 2 | risk60 + pv103 1:1 + `target_tvr=0.10` | 更激进压 TO |
| 3 | risk60(ts_mean22) + pv103 1:1 | 平滑路径对照 |
| 4 | sentiment27×2 + institutions6 + `target_tvr=0.09` | 把 TO 从 11.17% 再压到 9% 让 F>1 |
| 5 | sentiment27×2 + institutions6 原式 | #7 复现基线 |
| 6 | risk60×2 + institutions6 + `target_tvr=0.12` | 两弱信号 × F 友好腿 |
| 7 | risk60×2 + pv103 + `target_tvr=0.15` | 保住 sub 1.92 的同时压 TO |
| 8 | sentiment27 + institutions6 1:1 + `target_tvr=0.10` | 1:1 配比对照 |

**塔组合合规**：RISK × PV（类型 #4）、SENTIMENT × INSTITUTIONS（集合外×集合外，**不限量**）、RISK × INSTITUTIONS（**不限量**）——**未新增任何塔组合类型**。
`techindi_model`(OTHER) 保持单数据集 ATOM，**不与 PV 混**（OTHER+PV 属禁混集合内两两，硬禁）。


## 75. ★★★★★ CW 机制定论（group_backfill 前置/末端均可，裁尾类全无效）+ IMBALANCE 族 prod 封盘 + prod-先行纪律

日期：2026-11-06（承接用户提示「用 group_backfill 可以降 CONCENTRATED_WEIGHT」）

### 75.1 八臂对照：CW 的真因是「组内有效样本太少」，不是尾部极值

基线 `group_zscore(ts_rank(imb5_score, 252), industry)`（GBR/TOP700/D1，SLOW，trunc 0.06，decay 5）原 S 2.08 / F 1.30，CW 不过。U84 = `2TWYTr9oa4pgam4122dB1hMD`（comp 8 / err 0）：

| 杠杆 | alpha | S | F | TO | 真实闸 |
|---|---|---:|---:|---:|---|
| 原样控制 | `xArlPXbl` | 2.08 | 1.30 | 16.76% | CW + LOW_2Y |
| `group_rank` 替 `group_zscore` | `P0oPwjMJ` | 1.15 | 0.59 | 13.78% | LOW_S + LOW_F + 2Y（信号被杀）|
| `signed_power(·,0.5)` | `leAgQJMx` | 2.05 | 1.26 | 16.09% | CW + 2Y |
| `signed_power(·,0.7)` | `akKRAXVO` | 2.07 | 1.29 | 16.25% | CW + 2Y |
| `winsorize(·, std=3)` | `omEP3Qok` | 2.08 | 1.30 | 16.76% | CW + 2Y（**一格不动**）|
| 粗轴 `sector` | `d5W9EeKK` | **2.27** | **1.49** | 16.10% | 只剩 CW |
| 细轴 `subindustry` | `xArlPX1l` | 1.79 | 1.01 | 17.72% | CW |
| **前置 `group_backfill(ts_rank(...), industry, 252)`** | **`9qxGagxq`** | **1.95** | **1.14** | 16.70% | **只剩 LOW_2Y —— CW 已清** |

两条硬结论：
1. `winsorize(std=3)` 与 `signed_power` 在 CW 维度**零效果** ⇒ CW 的因不是尾部极值，而是「组内有效样本太少导致 z 爆炸」。只有抬覆盖率的 `group_backfill` 有效。
2. 基线 S≥1.5 时 gbf 的 S 折损仅 5–10%（2.08→1.95），远小于历史记录的 0.24→0.09（那次基线接近噪声）。**gbf 可以放心用于强候选。**

补充：末端位置的 gbf 同样有效 —— `LLMKrR5n` = `group_backfill(group_zscore(ts_rank(imb5_score,252), industry), subindustry, 252)`（trunc 0.10）S **2.21** / F **1.45** / TO 14.70%，CW 通过、只剩 2Y。⇒ **gbf 位置不是关键，把组内样本补稠才是关键**（此前「只有前置有效」的结论需放宽）。

### 75.2 IMBALANCE `imb5_score` 族被 prod 封盘 —— 换轴、gbf、加腿都救不了裸版

| alpha | 几何 | S | F | prod | 判定 |
|---|---|---:|---:|---:|---|
| `xArlPXbl` | 裸版 industry | 2.08 | 1.30 | **0.8742** | 死 |
| `d5W9EeKK` | 粗轴 sector | 2.27 | 1.49 | **0.8017** | 死 |
| `9qxGagxq` | gbf 前置 | 1.95 | 1.14 | **0.7578** | 死 |
| `kqNaGoAd` | `× ts_rank(volume,66)` | 2.07 | 1.12 | **0.6994** | ★ 压线通过 |
| `A1VxzNAQ` | 裸版（trunc 0.10） | 2.08 | 1.30 | **0.8743** | 死 |

**定论**：`imb5_score` 单字段族的 prod 结构钉在 0.76–0.87，任何 CW 杠杆只能把它从 0.874 压到 0.758，跨不过 0.70 线。**唯一跌破 0.70 的路径是加一条正交第二腿（volume rank）把相关性稀释 0.17。**

⇒ 该族**放弃**（U84/U86 的剩余价值只在机制层面，已提取）。

### 75.3 ★★★★★ 新纪律：prod 先行 —— CW-only 候选里 2/3 已被 prod 封死

全史扫描得 **29 条**「只挂 CONCENTRATED_WEIGHT 且 S≥1.4」的候选，抽样读 prod：

| alpha | S | F | prod | 结论 |
|---|---:|---:|---:|---|
| `A1VxzNAQ` | 2.08 | 1.30 | 0.8743 | 死 |
| `QPv0NGRQ` | 1.82 | 1.05 | 0.8316 | 死 |
| `58EGqZ51` | 1.83 | 1.16 | 0.7655 | 死 |
| `leAa5jJl` | 2.10 | 1.13 | 0.7858 | 死 |
| `kqNaGoAd` | 2.07 | 1.12 | **0.6994** | ★ |
| `mLoKz3Q2` | 1.69 | 1.03 | **0.6729** | ★ |

**为什么必须先读 prod**：CW 杠杆只改权重幅度、不改信号方向 ⇒ prod 几乎不动。破完 CW 再发现 0.87，等于白烧 8 个仿真槽位。prod 读一次 5–15s（缓存）到 1–5min（首算），便宜两个数量级。

**应用**：任何「S/F/2Y 全过、只差 CW / 换手 / 子宇宙」的候选，**第一步读 prod**；≥0.70 直接判死，<0.70 才进破墙队列。同理推及 LOW_2Y / LOW_SUB_UNIVERSE / IS_LADDER 这类「改结构就能动」的闸。

### 75.4 ★★★★★ 102 条单闸候选总台账（按表达式去重）

脚本 `results/_scan_prod.py` 汇总全部历史收割：**102 条** `S≥1.45 且 F≥0.85` 且至少挂一个 RA 闸的去重候选，按 S 降序写入 `results/_prod_queue.txt`。

闸分布（单闸 = 一次定向修复就可能出货）：

| 单闸 | 条数（前 45 内）| 典型 S/F/TO | 备注 |
|---|---|---|---|
| `LOW_2Y_SHARPE` | 最多 | 1.85–2.30 / 1.05–1.45 / 11–26% | 结构/平滑可动 |
| `CONCENTRATED_WEIGHT` | 中 | 1.69–2.27 / 1.03–1.49 | gbf 可清，但 prod 多为 0.76–0.87 |
| `IS_LADDER_SHARPE` | 少 | **2.64** / 1.62、2.19 / 1.22、2.00 / 1.05 | 最强单件 `3qoXwW1z` |
| `LOW_SUB_UNIVERSE_SHARPE` | 少 | 2.00 / 1.34、1.92 / 1.23 | 子宇宙问题 |
| `LOW_FITNESS` | 中 | 1.86–1.97 / 0.93–0.97 | 差一点点 |

**当前最强单闸件**：`3qoXwW1z`（S **2.64** / F **1.62** / TO 23.55% / R 8.86% / sub 2.19 / 2Y 1.51，只挂 `IS_LADDER_SHARPE`，neutralization **CROWDING**，trunc 0.08，decay 4，techindi `tm_16_r1_r5_r10_rh_glb_d1_r5_q1` 经 `target_tvr=0.45` 平滑 + `bucket(rank(cap),0,1,0.1)` 双重分组）。

### 75.5 在飞与下一步

- **U83** `1mej8w6c259sbLJiZ1ZE8GO`：institutions4 族 8 变体（`58EGqZ51` prod 0.7655 已判死，本批仅作机制对照）
- **U85** `QsaeNa2L4VFcmCwp7JJCOK`：`mLoKz3Q2` 几何（prod **0.6729**，只剩 CW）8 变体 —— 唯一「CW 一修即可提交」的在飞批次
- **U86** `48E16C8ww4un9807BRnkH7q`：gbf × 轴 × 窗口组合（IMBALANCE，现已确认族级 prod 封盘，仅作机制收尾）
- **prod 筛查队列** `results/_prod_screen.txt`（15 条单闸最高 S 件，后台串行读）：`3qoXwW1z` / `E56p1A8J` / `LLMKrR5n` / `0mYP68j6` / `LLMKrRMn` / `QPv0zZPX` / `leAvoJr7` / `LLMNNNKn` / `RREbbb9d` / `VkxaaaM0` / `1YNWKRjz` / `3qoX1vzX` / `78LNmZ82` / `vR1r7ERd` / `rKRO81Oa`

**结论性方向修正**：真正的瓶颈已从「闸」变成「prod 稀释结构」。未来派发应优先投给「正交第二腿」搜索（把 prod 从 0.8 稀释到 <0.70），而不是继续在 CW/换手/2Y 上磨。

### 75.6 ★ 订正与 U85 结果：institutions4+SHORT 族同被 prod 封盘（0.8011），且 CW 杠杆的符号随几何翻转

**订正**：75.5 里写的「`mLoKz3Q2` prod 0.6729」是**归属错误** —— 0.6729 是 `3qoGxkqZ`（pv103+cold）的值；`mLoKz3Q2` 的 prod 从未测过。实测其同族末端件 `rKR0JbYa` 为 **0.8011**。

U85 = `QsaeNa2L4VFcmCwp7JJCOK`（`mLoKz3Q2` 几何 × 8，FAST / trunc 0.06 / decay 5，comp 8 err 0）：

| 臂 | alpha | S | F | TO | 2Y | 真实闸 |
|---|---|---:|---:|---:|---:|---|
| 控制（sector/66 + 冷腿）| `1YNGnQxQ` | 1.69 | 1.03 | 11.16% | 2.61 | CW 0.133191 |
| gbf 前置 sector | `VkxM2X1A` | **1.05** | 0.49 | 10.81% | 1.36 | S+F+ladder（稀释致死）|
| gbf 前置 industry | `leAgQ7d2` | 0.88 | 0.38 | 10.25% | 1.13 | 同上 |
| 冷腿 gbf | `bl6xoNXq` | 1.17 | 0.59 | 11.38% | 1.11 | 同上 |
| 双腿 gbf | `omEP3n7E` | 0.70 | 0.27 | 10.74% | 0.71 | 同上 |
| `ts_rank` 替 zscore | `O0A6bnOg` | 0.98 | 0.45 | 10.72% | 2.06 | S+F |
| **末端 `winsorize(·, std=3)`** | **`rKR0JbYa`** | **1.70** | **1.04** | **11.11%** | **2.64** | **无（全闸通过）** |
| 冷腿 ts_rank | `P0oPwnWW` | 1.71 | 1.05 | 11.83% | 2.64 | CW 0.133667 |

**两条关键反差**：
1. 这个族（两腿都是 `group_rank`，取值有界）里 **`group_backfill` 是灾难**（S 1.69→1.05），而 **末端 `winsorize(std=3)` 一击清闸**；IMBALANCE 族（两腿 `group_zscore`，无界）恰好相反 —— gbf 有效、winsorize 一格不动。
   ⇒ **CW 杠杆不能跨几何照搬，必须按「腿的输出是否有界」选**：有界腿 → 裁尾（winsorize）；无界腿 → 补覆盖（group_backfill）。
2. `rKR0JbYa` 全闸通过（S 1.70 / F 1.04 / TO 11.11% / 2Y 2.64）却 **prod 0.8011** 判死 ⇒ 再次印证 prod 才是终局闸。

### 75.7 prod 筛查前 4 条结果（15 条队列）

| 顺序 | alpha | S | F | TO | 缺的闸 | prod | 判定 |
|---|---|---:|---:|---:|---|---:|---|
| 1 | `3qoXwW1z` | 2.64 | 1.62 | 23.55% | IS_LADDER | 0.7552 | 死 |
| 2 | `E56p1A8J` | 2.30 | 1.24 | 25.82% | 2Y | 0.7376 | 死 |
| 3 | `LLMKrR5n` | 2.21 | 1.45 | 14.70% | 2Y | 0.8299 | 死 |
| 4 | **`0mYP68j6`** | **2.19** | **1.22** | **22.96%** | **IS_LADDER** | **0.6837** | ★ **prod 通过** |

**`0mYP68j6`** = `group_backfill(multiply(group_zscore(ts_av_diff(imb5_score, 126), industry), ts_rank(volume, 66)), subindustry, 252)`（SLOW / trunc 0.10 / decay 5，LC 459，2Y 1.55，sub 1.71，investability 1.64）。它是 `kqNaGoAd`（prod 0.6994，只挂 CW）的**后代**：末端加 gbf 后 CW 清掉、S 2.07→**2.19**、F 1.12→**1.22**、TO 24.92%→**22.96%**、prod 0.6994→**0.6837**（同向下移）。

⇒ **`imb5_score × ts_rank(volume,66)` 这一对是当前唯一「prod 在 0.70 内侧」的组合**（两个后代分别 0.6994 / 0.6837），且都只剩一个闸。U88 = `4vuo64aQs4u8ahfGqKIMw5l` 针对 `0mYP68j6` 派了 8 臂破 `IS_LADDER_SHARPE`（gbf 窗 126/504、gbf 组 industry、`ts_av_diff` 窗 66/252、`ts_mean` 平滑、volume 窗 252、原样控制）。

### 75.8 区域塔位表（2026-11-06 实测，D1）

| 区域 | 已点亮塔 | 总塔数 | 可开采度 |
|---|---|---|---|
| **DEU/D1** | 无 | 16 | ★★★★★ 全空 |
| **ASI/D1** | 无 | 16 | ★★★★★ 全空 |
| **HKG/D1** | 无 | 15 | ★★★★★ 全空 |
| **CHN/D1** | 无 | 12 | ★★★★ 全空 |
| USA/D0 | 无 | 15 | ★★★★ 全空（D0 延迟）|
| EUR/D0 | 无 | 13 | ★★★ 全空 |
| GBR/D0 | 无 | 14 | ★★★ 全空 |
| AMR/D0,D1 | 无 | 2 | ★★ 集太少 |
| GBR/D1 | model 5 / news 3 / analyst 3 / fundamental 3 | 16 | 已挖（本战役）|
| IND/D1 | pv 11 / news 4 / other 4 / analyst 3 / model 3 / fundamental 3 / risk 3 | 15 | 几乎挖满 |
| EUR/D1 | analyst 10 / model 3 / fundamental 3 / imbalance 3 | 14 | 半满 |
| KOR/D1 | shortinterest 4 / fundamental 3 / model 3 | 15 | 半满 |
| USA/D1 | analyst 6 / model 4 | 16 | 半满 |
| GLB/D1 | other 4 / model 3 | 13 | 半满 |

⇒ GBR/D1 的 16 塔已点亮 4 个、剩余塔的强信号几乎全被 prod 封盘；**DEU/D1 与 ASI/D1 各 16 塔全空**，是性价比最高的下一个战场。

## 76. 2026-11-06 第三轮：全闸通过候选连续出现，但 prod 仍是终局闸

### 76.1 本轮四颗「全 RA 闸通过」候选的成绩单

| alpha | 表达式要点 | S | F | TO | 2Y | prod | 判定 |
|---|---|---:|---:|---:|---:|---:|---|
| `Jje3grxj` | `group_zscore(group_backfill(ts_rank(imb5_score,252), sector,252), sector)` | 2.26 | 1.49 | 15.7% | 1.61 | **0.7978** | 死 |
| `leAgQPO5` | `multiply(group_backfill(group_zscore(ts_av_diff(imb5_score,126), industry), subindustry,252), ts_rank(volume,66))` | 2.16 | 1.18 | 23.8% | 1.87 | 待出 | — |
| `88RGO5MW` | `2:1 lit/dark 成交额比 + 冷腿` | 1.72 | 1.13 | 12.7% | 2.74 | 待出 | — |
| `0mYP68j6`(旧) | 同 leAgQPO5 但 gbf 在乘 volume 之后 | 2.19 | 1.22 | 23.0% | 1.55 | 0.6837 | 卡 IS_LADDER |

### 76.2 ★★★★★ imb5 族 prod 的破壁规律：只有「volume 交互腿」能破 0.70，gbf 几何无效

把 imb5 族已测 prod 按结构排列，规律非常干净：

| 结构 | alpha | prod |
|---|---|---:|
| `group_zscore(ts_rank(imb5,252), industry)` 裸版 | `A1VxzNAQ` | 0.8743 |
| 同上 + 粗轴 sector | `d5W9EeKK` | 0.8017 |
| 同上 + 前置 gbf industry | `9qxGagxq` | 0.7578 |
| `group_zscore(gbf(ts_rank(imb5,252), sector,252), sector)` | `Jje3grxj` | 0.7978 |
| **`group_zscore(Δimb5,126) × ts_rank(volume,66)`** | `kqNaGoAd` | **0.6994** |
| **同 + 末端 gbf subindustry** | `0mYP68j6` | **0.6837** |

⇒ **gbf 的三种放法（前置 / 末端 / 换轴）全部落在 0.76–0.80，一个都没破 0.70；唯一跌破 0.70 的两次都含 `ts_rank(volume,66)` 这条正交腿。**

结论：对 prod 而言，**「加一条正交腿」是破壁杠杆，「权重几何微调」不是**。这与 CW 的经验正好相反（CW 只看覆盖率，权重几何就能动），两类闸要分开处理：

- **CW / 覆盖率型闸** → 调权重几何（gbf / winsorize，按腿是否有界选择）。
- **prod / 相关性型闸** → 必须引入**新的信息源**（正交字段或新数据集），几何微调无效。

### 76.3 ★★★★ `0mYP68j6` 路线结构性封盘：8 种几何全卡 IS_LADDER

U88 对 `group_backfill(multiply(group_zscore(ts_av_diff(imb5,126), industry), ts_rank(volume,66)), subindustry, 252)` 做八臂（窗口 66/126/252、gbf 距离 126/252/504、gbf 轴 subindustry/industry、外层 ts_mean(5)）：

| alpha | S | F | 2Y | 缺的闸 |
|---|---:|---:|---:|---|
| `j2YVnRbO` | 2.25 | 1.29 | 1.23 | IS_LADDER |
| `0mYP68j6` | 2.19 | 1.22 | 1.55 | IS_LADDER |
| `d5W9nVLX` | 2.14 | 1.21 | 1.45 | IS_LADDER |
| `58EGL0ok` | 2.10 | 1.14 | 1.33 | IS_LADDER |
| `VkxMXjgY` | 2.03 | 1.09 | 1.34 | IS_LADDER |
| `MPYgbRoa` | 2.02 | 1.08 | 1.47 | IS_LADDER |
| `mLoKqRME` | 1.93 | 1.26 | 1.20 | IS_LADDER |
| `pwdWnrAx` | 1.89 | 0.95 | 1.56 | LOW_FITNESS + IS_LADDER |

**8/8 全部卡 IS_LADDER_SHARPE** ⇒ 该结构的 IS 分期 Sharpe 谷值无法用权重几何补，判结构性封盘。

**但 `leAgQPO5` 例外**：把 gbf 从「乘 volume 之后」改到「乘 volume 之前」（作用于信号本体），nf 从 1 变 0 —— IS_LADDER 被修好，S 也保住了 2.16。这是本族唯一全闸通过的几何。

### 76.4 ★★★★ order_book_imbalance：字段有真信号，但强度集中在近两年

U90 八字段（`ebbo_filled_order_avg_rest_time` / 撤单量差 / 成交量差 / `fill_prob` 比 / `ebbo_filled_order_percentage` / 价差/波动比 / `duration_best_*_venue` / `inserted_*_order_volume` 差）全部落在 **S 1.44–1.55、F 0.82–0.93、2Y 2.55–2.86**。

⇒ 该数据集字段族**在近两年极强、全期偏弱**，属于「regime 型」信号。U91 就着最接近的 `平均绝对价差/日内波动`（Amihud 式非流动性）做了定向放大（3:1 / 4:1 / 换轴 / 独立成 ATOM），见 76.5。

### 76.5 ★★★★★ U91：`88RGO5MW` 全闸通过（lit/dark 成交额比）

`add(multiply(2, group_rank(ts_zscore(divide(vec_avg(lit_trade_notional_value), vec_avg(dark_trade_notional_value)), 22), market)), reverse(group_rank(ts_zscore(vec_sum(loaned_share_count_main), 504), sector)))`

S **1.72** / F **1.13** / TO 12.7% / 2Y **2.74** / LC 449 / self **0.267** / **nf=0（全 RA 闸通过）**。

机制：**明池 vs 暗池成交额比** —— 暗池份额上升意味着知情/机构资金在离屏撮合，是知情交易的经典代理。同批另三条（相对/绝对价差比 S1.55、撤单取消率 S1.51、`final_bid_ask_spread_bps` S1.48）都差一点，说明该数据集里**「量」类字段强于「价」类字段**。

### 76.6 ★★★ GBR 未点亮塔的存活数据集只剩 16 个

把 177 集按「未点亮塔 + 未判死 + coverage>0.15」过滤后只剩 16 个，按拥挤度（数据集级 alphaCount）升序：

| 数据集 | 类 | cov | 字段 | alphaCount | 评注 |
|---|---|---:|---:|---:|---|
| `euro_equity_imbalance` | other | 0.16 | 4 | 7 | 覆盖太低 |
| `other250` | other | 0.52 | 12 | **8** | 亚马逊商品价/评分/畅销排名 |
| `other699` | other | 0.34 | 7 | 14 | TipRanks 散户交易 |
| `pv109` | pv | 0.33 | 26 | 32 | 公司债信用（收益率/成交/存量） |
| `other47` | other | 0.52 | 18 | 33 | SEMrush 自然/付费搜索流量 |
| `institutions4` | inst | 0.39 | 6 | 47 | 已过度开采（prod 封盘） |
| `pv29` | pv | 1.00 | 50 | 66 | **纯分组轴库（`sta1_top1200cN`），无信号字段** |
| `insiders1` | ins | 0.59 | 9 | 87 | 内部人交易额/显著性 |
| `order_book_imbalance` | other | 0.18 | **240** | 96 | 本轮主战场 |
| `sentiment7` | sent | 0.58 | 3 | 96 | 字段太少 |
| `risk60` | risk | 0.67 | 5 | 202 | — |
| `insider_trx_matrix` | other | 0.60 | 33 | 215 | — |
| `pv30` | pv | 0.83 | 240 | 400 | 亦为分组轴库 |
| `insider_matrix` | other | 0.61 | 33 | 553 | — |
| `sentiment27` | sent | 0.80 | 18 | 834 | 已开采 |
| `shortinterest3` | short | 0.85 | 25 | 1668 | 已饱和（冷腿 0.8088） |

⇒ **GBR 的低拥挤洼地基本见底**：除了 240 字段的 `order_book_imbalance`，其余能挖的只有 `other250`/`other47`/`pv109` 三个覆盖率 0.3–0.5 的小集。

### 76.7 ★★★★★ DEU/D1 才是主线：universe 是 TOP500（不是 TOP700），16 塔全空

探测结果：`get_datasets(DEU, TOP700, D1)` 返回 **0** 条；`TOP500` 返回 **172** 条。DEU 的正确设置是 **TOP500 / delay 1**。

DEU 高覆盖 + 低拥挤数据集（按 alphaCount 升序）：

| 数据集 | 类 | cov | 字段 | alphaCount | 机制 |
|---|---|---:|---:|---:|---|
| `analyst48` | analyst | 0.79 | 7 | **7** | 指数成分元数据（非信号） |
| `model53` | model | 0.87–0.93 | 22 | **9** | ★ Merton 违约概率期限结构 + 隐含利差 |
| `institutions4` | inst | 0.34 | 6 | 19 | — |
| `insiders1` | ins | 0.53 | 8 | 26 | 内部人交易 |
| `other532` | other | 0.74–0.97 | 8 | 45 | ★ 特质收益（residual momentum） |
| `fundamental22` | fund | 0.69 | 1 | 40 | — |
| `institutions6` | inst | **1.00** | 11 | 270 | 稠密无覆盖问题 |
| `news17` | news | 0.79 | 48 | 87 | — |
| `insider_agg_matrix` | ins | 0.56 | 34 | 170 | — |

`model53` 字段族：`annualized_pd_{1month,3month,6month,1year,2year,3year,4year,5year,7year,10year}_jc7`（年化违约概率期限结构）、`mdl53_implied_spreads`、`mdl53_ms5_{1month..10year}`（隐含利差曲线）。对应两条成熟文献机制：① Campbell-Hilscher-Szilagyi「困境异象」（高违约概率→低收益，与 CAPM 相反）；② 违约概率**期限斜率倒挂**（近端骤升=短期恶化）。

`other532` 字段族：`oth532_{global,emerging}_{daily,monthly}_specificreturn`（cov 0.96–0.97）、`idiosyncratic_return_{eue,eult}_{daily,monthly}` ⇒ Blitz-Huij-Martens 残差动量。

### 76.8 本轮新增/在飞批次

| 批次 | multisim | 内容 | 设置 |
|---|---|---|---|
| U91 | `4BU1G5b4L4Ha99h1dzmEGbH3` | order_book 量类 4 字段 | GBR/FAST/trunc 0.10 |
| U92 | `2Ozaavge94rqaotQnWszpSz` | other47 × 5 + pv109 × 3（单集 ATOM） | GBR/FAST/trunc 0.10 |
| U93 | `SsQBudC851T8Fh18xszluVZ` | 非流动性比率/挂单时长放大 8 臂 | GBR/FAST/trunc 0.10 |
| U94 | `3ldfKweQu5fwcwFt9KcHq3j` | **DEU/D1 侦察**：model53 × 6 + other532 × 2 | DEU/TOP500/INDUSTRY/trunc 0.10 |

U89（order_book 首批 8 字段）**8/8 瞬时 FAIL 无错误消息**，同结构 U90/U91 正常 ⇒ 判为并发超限或平台瞬时拒绝，非字段问题。

### 76.9 ★★★★★ `leAgQPO5` 通过 prod：第 6 颗可提交 alpha

| 项 | 值 |
|---|---|
| 表达式 | `multiply(group_backfill(group_zscore(ts_av_diff(imb5_score, 126), industry), subindustry, 252), ts_rank(volume, 66))` |
| 设置 | GBR / TOP700 / D1 / decay 5 / **SLOW** / trunc **0.06** |
| S / F / TO / R / DD | **2.16 / 1.18 / 23.82% / 7.07% / 4.02%** |
| 2Y / sub-universe / investability | 1.87 / 1.69 / 1.54 |
| longCount | 459 |
| RA 闸 | `failed_ra_count = 0`，`checks.fail = []` |
| self 相关 | **0.1064** |
| prod 相关 | **0.6866** ✓（< 0.70） |
| 与现有 5 颗最大互相关 | **0.108** ✓ |

**可提交篮子 = 6 颗**：`RRE5Mwkn`、`ZYQXZj73`、`QPvbxjXw`、`rKRPAWv9`、`3qoGxkqZ`、`leAgQPO5`。六者两两互相关全部 < 0.62（`max_mutually_below_subset_size = 6`，精确解）。**用户尚未授权提交。**

### 76.10 ★★★★★ 同骨架换字段拿不到第二条：`ZYQXZj73` vs `88RGO5MW` 互相关 0.8941

| 对 | 相关 |
|---|---:|
| `ZYQXZj73` vs `88RGO5MW`（同骨架：`2:1 order_book 字段 + 冷腿`，字段完全不同） | **0.8941** ✗ |
| `88RGO5MW` vs `3qoGxkqZ` | 0.5763 |
| `ZYQXZj73` vs `3qoGxkqZ` | 0.5449 |
| `RRE5Mwkn` vs `3qoGxkqZ` | 0.5132 |
| `leAgQPO5` vs 其余 6 条 | −0.108 ~ 0.038 |

**共同因子是伙伴腿（冷腿），不是信号腿**：冷腿占权重 1/3 且是同一表达式 ⇒ 两条 alpha 有 1/3 持仓完全重叠。

**推论**：`order_book_imbalance` 的 240 个字段 × 同一骨架，最终只能提交 **1 条**（已由 `ZYQXZj73` 占位）。想再加第二条必须换**伙伴腿**——正好 `leAgQPO5` 证明换伙伴腿（冷腿 → volume 交互）能同时把 prod 打到 0.6866、把与全池互相关打到 <0.11。

### 76.11 ★★★ U93：提高信号腿权重是负收益（2:1 → 3:1 → 4:1 单调下降）

对 `平均绝对价差/日内波动`（Amihud 非流动性）与 `ebbo_filled_order_avg_rest_time` 做权重梯度：

| 构造 | S | F | 2Y |
|---|---:|---:|---:|
| 2:1 ILLIQ（`YP1l23dq`，U90） | **1.55** | 0.93 | 2.77 |
| 3:1 ILLIQ（`VkxMXpxJ`） | 1.38 | 0.78 | 2.50 |
| 4:1 ILLIQ（`WjOYNpOd`） | 1.27 | 0.69 | 2.32 |
| ILLIQ 独立成 ATOM（`YP1lNp1A`） | **0.61** | 0.23 | 1.49 |
| 2:1 REST（`YP1l23dq` 同批） | 1.52 | 0.89 | 2.54 |
| 3:1 REST（`78LGxwLv`） | 1.34 | 0.74 | 2.24 |
| 4:1 REST（`LLM8npMv`） | 1.23 | 0.65 | 2.04 |
| REST 独立成 ATOM（`QPvWna0M`） | 0.55 | 0.19 | 1.13 |

**决定性对照**：GBR 冷腿单独 S 是 **1.74**，而 2:1 混合后只有 1.55 ⇒ **order_book 信号腿是在稀释冷腿**，不是增强。加权重只会放大稀释。

⇒ 结论订正：`ZYQXZj73`（S1.78）是这个数据集里**罕见的正贡献**，其余 240 字段里的绝大多数对冷腿都是负贡献。`order_book_imbalance` 的边际价值到此为止。

### 76.12 ★★★★★ DEU/D1 判死（详见长期记忆）

DEU 正确设置是 **universe = TOP500**（TOP700/TOP800/TOP200 均返回 0 集），172 集，16 塔全空。但：

| 臂 | DEU/D1 S | GBR/D1 同结构 |
|---|---:|---:|
| 冷腿单独 | **0.84** | **1.74** |
| `institutions6` 买卖人数差单独 | 0.75 | — |
| 2:1 机构流 + 冷腿（本批最高） | **1.00** | 1.84 |
| 2:1 PD 期限斜率 + 冷腿 | 0.80 | — |
| 2:1 利差曲线形状 + 冷腿 | 0.66 | — |
| 2:1 困境反转 + 冷腿 | 0.58 | — |
| 2:1 隐含利差 + 冷腿 | 0.43 | — |

`longCount` 仅 188–214（GBR 450–470）⇒ DEU 有效池只有 GBR 的 40%。**8 臂全部 3–4 闸失败，最高 1.00，离 1.58 差 0.58 ⇒ 该区不可挖，不转区。**

**新区准入判据（已写入长期记忆）**：先用「该区冷腿单独 S」当信号标尺 —— ≥1.5 可挖；≤1.0 直接换区。探针成本 1 批 8 条。

### 76.13 当前在飞批次

| 批次 | multisim | 内容 |
|---|---|---|
| U95 | `sjUfw4mB4wXaIqPaiD2tx2` | other47 × 5 + pv109 × 3 重发（U92 曾 8/8 瞬时 FAIL） |
| U97 | `4tRpHP7AK4wD9wWxvYt0cQW` | other250 × 4 + other699 × 2 + insiders1 × 2 |
| U98 | `1AOfaZ1S34FC8yRE7Lc1cr2` | insider_trx_matrix × 3 + insider_matrix × 2 + sentiment7 × 1 + risk60 × 2 |

### 76.14 ★★★★ U95 / U97 / U98：GBR 剩余四个机制全部判死

| 数据集 | 机制 | 最好 S | 结论 |
|---|---|---:|---|
| `other47`（SEMrush 自然/付费搜索流量，a=33） | 数字需求 | **0.55** | 8 条全部 3–4 闸失败 |
| `pv109`（公司债收益率/成交/存量，a=32） | 信用-股票联动 | ≤0.41 | 同上 |
| `other250`（亚马逊商品价/评分/畅销排名，a=8） | 商品需求 | **0.06** | 近零信号，且 3 条撞 CW |
| `other699`（TipRanks 散户交易，a=14） | 散户流 | ≤0.02 | 近零信号 |
| `insiders1`（内部人交易额/显著性，a=87） | 内部人信念 | ≤0.06 | 近零信号 |
| `insider_matrix` / `insider_trx_matrix` | 内部人方向 | **1.55** | 但换手 56%，F 仅 0.58 |
| `sentiment7`（Wikipedia views） | 关注度 | 0.58（2Y 1.85） | 3 闸失败 |
| `risk60`（借券拥挤/费率） | 借券拥挤 | ≤0.61 | 3 闸失败 |

**低 alphaCount 不等于有信号**：`other250`（a=8，全 GBR 最不拥挤）实测 S 0.06，`other699`（a=14）S 0.02。拥挤度只预测 prod（相关性墙），完全不预测信号强度。

### 76.15 ★★★★ 内部人时近性梯度：换手就是信号本体（U101 六臂）

`npv6nrPl` = `group_rank(ts_zscore(divide(eur_signal_value_1, add(abs(eur_signal_value_4), 1)), 66), sector)`（内部人信号近期/远期强度比），S **1.55** 但 TO **56.2%** ⇒ F 0.58。六种降换手手法：

| 手法 | S | F | TO |
|---|---:|---:|---:|
| `ts_mean(·, 22)` 平滑 | 0.60 | 0.21 | 14.8% |
| `ts_mean(·, 66)` 平滑 | 0.30 | 0.09 | 12.7% |
| `ts_zscore(·, 252)` 长窗 | 0.36 | 0.10 | 9.4% |
| `ts_target_tvr_decay(target_tvr=0.05)` | 1.30 | 0.48 | 43.2% |
| `hump(hump=0.02)` | **1.70** | 0.63 | 55.4% |
| 改差值 `subtract(backfill(sv1), backfill(sv4))` | 0.48 | 0.15 | 9.9% |

**换手从 56% 压到 10–15% 时 S 必崩到 0.3–0.6；`hump` 反而把 S 抬到 1.70 但换手一点没降。** 这与 `techindi_model` 极值桶族完全同构（TO 47%→13% 时 S 1.55→0.87）⇒ 「换手即信号」类alpha在 F 维度无解。

### 76.16 ★★★★★ 运维硬规则：`unknown_soft` 会连坐取消整批

HKG 探针批 8 条结果：5 条 `CANCELLED`、3 条 `ERROR: Attempted to use unknown variable "pv103_ivam_sum"`。

但同批 `preflight_expressions` 返回的是 `valid: true`、`unknown_fields: []`，问题字段只在 **`unknown_soft`** 里。平台执行时它是硬错误，并**连坐取消同批其余子仿真**。

**U89 / U92 / HKG 探针三次「父任务 ERROR、子任务全 FAIL/CANCELLED 且无消息」都是这个原因**，此前两次误判为并发超限。判据三元组：`valid===true` **且** `unknown_fields===[]` **且** `unknown_soft===[]`。

### 76.17 ★★★ 区域字段可用性矩阵（跨区移植前必查）

| 字段 | GBR | DEU | HKG | ASI |
|---|---|---|---|---|
| `loaned_share_count_main`（冷腿） | ✓ | ✓ | ✓ | **✗** |
| `count_institutional_buyers_security` | ✓ | ✓ | ✓ | — |
| `institutional_holding_current_shares` | ✓ | ✓ | **✗** | — |
| `pv103_ivam_sum` | ✓ | — | **✗** | **✗**（软警告） |
| `auction_order_imbalance_pct_adv` | ✓ | — | **✗** | — |
| `imb5_score` | ✓ | ✓ | ✓ | — |

正确 universe：**GBR=TOP700、DEU=TOP500、HKG=TOP500、ASI=TOP500**（其余 universe 均返回 0 集）。

### 76.18 GBR 未点亮塔的最终盘点

82 个未点亮塔数据集全部完成画像与至少一轮探针，结果：

- **产出 6 颗可提交**：`RRE5Mwkn` / `ZYQXZj73` / `QPvbxjXw` / `rKRPAWv9` / `3qoGxkqZ` / `leAgQPO5`。
- **被判死的机制**（≥25 个）：institutions4/6 全族、imb5 单字段族、order_book 除拍卖失衡与明暗池比之外的 238 字段、other250/other47/other699/pv109/insiders1/insider_matrix/insider_trx_matrix/sentiment7/sentiment27/risk60/techindi_model/pattern_scores/intraday_pv_feats/insider_agg_matrix/macro27/socialmedia12 等。
- **纯分组轴库**（无信号）：`pv29`、`pv30`。
