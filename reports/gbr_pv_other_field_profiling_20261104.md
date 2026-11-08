# GBR PV / OTHER 双塔字段画像与机制地图

> 生成：2026-11-04 · 区域 GBR / TOP700 / delay 1 / decay 4 / truncation 0.08 / CROWDING
> 数据来源：`get_pyramid_alphas` `get_pyramid_multipliers` `get_datasets` `get_datafields`（全部走 MCP，无临时直连）

---

## 0. 结论先行（这一节改写了整个战役的方向）

### 0.1 塔位数学：「点亮」的判据是每塔 3 颗 alpha

`get_pyramid_alphas(region=GBR, delay=1)` 实测 D1 塔位：

| 塔 | 已有 | 距点亮 | 可达性 |
|---|---:|---:|---|
| fundamental | 3 | **已点亮** | — |
| model | 5 | **已点亮** | — |
| news | 3 | **已点亮** | — |
| analyst | 3 | **已点亮** | — |
| **pv** | **2** | **差 1 颗** | ★★★★★ |
| **other** | **1** | **差 2 颗** | ★★★★★ |
| institutions / insiders / earnings / sentiment / risk / option / socialmedia / imbalance / macro / shortinterest | 0 | 各差 3 颗 | ★（实测天花板 0.15–1.13） |

**这是本次战役最重要的发现**：前 25 波（约 176 臂）全部投在「0 颗、需从零点 3 颗」的塔上，
而真正的近场是 **pv（差 1）与 other（差 2）**。前 25 波从未系统挖过这两个塔。

### 0.2 已有 3 颗全闸候选正好落在这两个塔上

| alpha | 金字塔归属（`ra.pyramid_short` 实测） | S | F | TO | 2Y | self |
|---|---|---:|---:|---:|---:|---:|
| Xg9b5ZX0 | **pv/other** | 2.07 | 1.07 | 27.2% | 2.09 | 0.213 |
| zq38KdX1 | **other** | 2.33 | 1.44 | 23.2% | 1.61 | 0.229 |
| YP1bGkGq | **other** | 1.91 | 1.03 | 25.0% | 2.20 | 0.235 |

- 三颗两两互相关（`compute_mutual_correlation` 本地实测）：Xg9b5ZX0↔zq38KdX1 **0.2331**、Xg9b5ZX0↔YP1bGkGq **0.4681**、zq38KdX1↔YP1bGkGq **0.1566** ➜ 全部 < 0.70，**可同时提交互不蚕食**。
- 若三颗全提交：**pv 2→3（点亮）**、**other 1→4（点亮）** ➜ **一次动作点亮两个塔**。
- 阻塞项：prod 相关性（平台单 in-flight 槽被僵尸 holder 占用）+ 用户明确授权。本轮无任何提交动作。

---

## 1. 覆盖是第一筛选器

`get_datafields` 返回的 `coverage` 在 GBR/TOP700 下的可用分布（本批 24 个数据集抽样）：

| coverage | 数据集 |
|---|---|
| **0.4878** | other545（Linked Firms Momentum） |
| **0.3440** | other699（Individual Investor Transactions） |
| **0.3319** | pv109（Bond Yield Data） |
| **0.2175 / 0.2105** | other384（NLP on conference conversation） |
| **0.2028 / 0.1649 / 0.1645** | order_book_imbalance |
| **0.1568** | euro_equity_imbalance |
| **0.0000（平台报 0）** | pv173、pv106、pv71、pv13、other571、other128、other567、other425、other315、other566、other696、event_ml_signals、continuation_score、intraday_pv_feats |

⚠ **cov=0.0 不等于无数据**：本项目已多次证实平台 coverage 列不可信（earnings6 / sentiment27 / insiders12 / institutions25 / socialmedia12 全报 0.0，但逐年 longCount 显示多数满覆盖）。
**cov=0.0 一律只作为「需要实测」标记，不作判死依据**；真判据是 `get_alpha_yearly_stats` 逐年 `longCount>0 && pnl≠0`。

---

## 2. PV 全 16 数据集（按平台 alphaCount 升序 = 竞争度升序）

| dataset | alphaCount | valueScore | 字段数 | 用户数 | D1倍率 | 名称 |
|---|---:|---:|---:|---:|---:|---|
| pv113 | 2 | 6.0 | 1 | 2 | 1.4 | Economic MacroIndicator Data |
| pv17 | 3 | 5.0 | 1 | 3 | 1.4 | Intermediate Cluster Groups |
| pv71 | 4 | 6.0 | 8 | 3 | 1.4 | Europe Relation Dataset |
| pv173 | 19 | 5.0 | 81 | 13 | 1.4 | Corporate Bond Pricing Data |
| pv109 | 32 | 5.0 | 26 | 15 | 1.4 | Bond Yield Data |
| pv106 | 43 | 4.0 | 8 | 25 | 1.4 | Microstructure Spread Data |
| pv13 | 44 | 5.0 | 28 | 29 | 1.4 | Relationship Data for Equity |
| pv29 | 73 | 4.0 | 50 | 53 | 1.4 | Derived Industry Classification |
| pv103 | 170 | 3.0 | 8 | 101 | 1.4 | Interval and MOO&MOC Statistics |
| pv30 | 400 | 4.0 | 240 | 159 | 1.4 | Alternate Industry Classification |
| intraday_pv_feats | 690 | 3.0 | 585 | 326 | 1.4 | Daily Intraday Price Volume Features |
| pv20 | 717 | 3.0 | 675 | 360 | 1.4 | Daily Spot and Cross Rate Data |
| continuation_score | 778 | 4.0 | 560 | 326 | 1.4 | Price Chart Continuation Pattern Similarity |
| pv47 | 779 | 1.0 | 2 | 320 | 1.4 | Specific Return Dataset |
| pattern_scores | 1841 | 3.0 | 504 | 772 | 1.4 | Chart Pattern Similarity Scores |
| pv1 | 56109 | 1.0 | 23 | 3516 | 1.4 | Price Volume Data for Equity |

**选品原则**：pv1 / pattern_scores / pv47 已饱和或已知 prod 拥挤（pv47 在本项目实测 7 条近似件 prod 0.7993–0.8737，整族封盘）；
pv113 / pv17 只有 1 个字段，撑不起 10–15 算子骨架；
**真正的 PV 候选带是 pv173 / pv109 / pv106 / pv13 / pv71 这 5 个（alphaCount 4–44，valueScore 4.0–6.0）**。

---

## 3. OTHER 全 41 数据集（alphaCount 升序）

| dataset | alphaCount | valueScore | 字段数 | 用户数 | 名称 |
|---|---:|---:|---:|---:|---|
| other635 | 2 | 6.0 | 3 | 2 | Thomson Reuters News Analytics Equities |
| other546 | 3 | 7.0 | 22 | 3 | Institutional Network Analysis Dataset |
| other571 | 3 | 7.0 | 23 | 3 | Wikipedia Viewing Data |
| workforce_flow_skills | 3 | 6.0 | 10 | 3 | Global Workforce Flow and Skills Analytics |
| other327 | 4 | 6.0 | 3 | 3 | Sensitivity to Interest Rates Model |
| other384 | 6 | 7.0 | 66 | 5 | NLP on conference conversation |
| euro_equity_imbalance | 7 | 7.0 | 4 | 6 | European Equity Trading Imbalance Indicators |
| other250 | 8 | 7.0 | 12 | 4 | details data |
| other567 | 11 | 7.0 | 48 | 9 | Employee Review Data |
| search_interest | 11 | 6.0 | 7 | 9 | Rapid Search Interest Signals |
| event_relation | 12 | 6.0 | 12 | 4 | Text-Based Event Relationship Analysis |
| other128 | 12 | 7.0 | 14 | 4 | Global Executive Performance Factors |
| other699 | 14 | 6.0 | 7 | 13 | Individual Investor Transactions Data |
| other323 | 15 | 6.0 | 7 | 11 | Global Equity Premarket Data |
| news_sentiment_nlp | 18 | 6.0 | 23 | 12 | News Sentiment Signal Features |
| other296 | 19 | 6.0 | 10 | 14 | Corporate Earnings Call Sentiment Data |
| stock_cluster_dl | 19 | 6.0 | 5 | 11 | Deep Learning Stock Clusters |
| stock_search_trends | 19 | 6.0 | 12 | 15 | US Stock Search Trend Matrix |
| other315 | 22 | 6.0 | 21 | 12 | Equity Swap Data |
| other436 | 23 | 5.0 | 3 | 17 | Dividend model |
| other734 | 23 | 6.0 | 7 | 9 | Search Engine Data |
| other425 | 26 | 6.0 | 13 | 8 | Supply Chain Data |
| other545 | 26 | 6.0 | 4 | 18 | Linked Firms Momentum Data |
| other47 | 33 | 5.0 | 18 | 22 | Web Intelligence Data |
| other696 | 39 | 6.0 | 220 | 25 | Hybrid NLP Model |
| other424 | 45 | 5.0 | 3 | 35 | Dividend prediction model |
| other169 | 47 | 6.0 | 22 | 30 | CDS dataset |
| earningscall_sentiment | 56 | 6.0 | 167 | 38 | Multi Aspect Earnings Call Sentiment |
| other78 | 87 | 6.0 | 112 | 50 | Earnings and conference call data |
| order_book_imbalance | 96 | 6.0 | 240 | 60 | Order Book Liquidity and Imbalance Analytics |
| other566 | 109 | 5.0 | 112 | 78 | Image-Based Financial Prediction Dataset |
| ai_news_scores | 114 | 5.0 | 105 | 68 | AI News Sentiment Scores |
| event_ml_signals | 117 | 7.0 | 104 | 12 | Machine Learning Company Event Signals |
| event_sentiment_signals | 117 | 6.0 | 52 | 55 | Corporate Event Sentiment Signals |
| insider_trx_matrix | 215 | 5.0 | 33 | 124 | Global Insider Transaction Aggregates |
| other335 | 281 | 3.0 | 10 | 166 | Multi-Region Dividend Alpha Model Dataset |
| other455 | 412 | 5.0 | 1500 | 169 | Relationship enhanced with AI/ML |
| insider_matrix | 553 | 4.0 | 33 | 293 | Aggregated Insider Transaction Matrix |
| dl_riskfree_returns | 983 | 3.0 | 133 | 470 | Deep Learning Risk Free Returns |
| acquisition_model | 1596 | 2.0 | 15 | 511 | Corporate Acquisition Likelihood Model |
| techindi_model | 26992 | 2.0 | 399 | 1883 | Deep Learning Technical Indicator Returns |

**关键读法**：
1. `techindi_model` 的 category 是 **other**（不是 model）——本项目已出货的 3 颗全闸候选全部属于 OTHER 塔。它是 OTHER 塔唯一被验证过的矿脉，但 alphaCount 26992 极度拥挤。
2. `event_ml_signals`（valueScore **7.0**、alphaCount 117、用户数仅 12）名字是「ML 信号」但字段实际是**二元事件旗标**（`dividend_increase_event`/`corporate_guidance_raised_event`…），是事件计数与事件时间门控的原料，不是预测值。
3. `insider_trx_matrix` / `insider_matrix` 在 **other** 塔而不是 insiders 塔——想做 insiders 塔时不能用它们。
4. `euro_equity_imbalance` 是少数明确标 **European** 的数据集，GBR 区域适配性最好。

---

## 4. 深画像（按 coverage 优先，共 8 个数据集）

### 4.1 ★★★★★ other545 — Linked Firms Momentum（cov **0.4878**，全批最高）
4 个 VECTOR 字段，全会话覆盖最好的一批：

| 字段 | 含义 | alphaCount |
|---|---|---:|
| oth545_mktcap | 公司市值（USD） | 4 |
| oth545_mpd | 动态价格动量得分（machine-learned price momentum） | 2 |
| oth545_pln_omen | NLP 派生的**网络动量**得分（文本挖掘关联） | 13 |
| oth545_score | NEMO 2.0 复合得分（七个网络动量信号聚合） | 8 |

**机制**：供应链/关联公司的动量溢出（spillover momentum）。经济学依据：Cohen & Frazzini (2008)「Economic Links and Predictable Returns」——通过经济关联传播的动量。
**优点**：4 个字段全是**模型输出连续值**（符合「预测类取数铁律：取连续形态，不用离散分位标签」）；cov 0.49 是 TOP700 里约 340 只，覆盖率足够撑 sub-universe 闸。
**风险**：动量族在 GBR 已有点亮件（pv 塔 2 颗含价格量衍生），prod 相关性需实测；`oth545_mpd` 与 `oth545_score` 之间可能高度相关，不可当两条独立腿。

### 4.2 ★★★★ other699 — Individual Investor Transactions（cov **0.3440**）
7 个 VECTOR 字段，全部围绕**散户逐笔成交**：

| 字段 | 含义 |
|---|---|
| oth699_sharestraded | 本次交易股数（**带符号**：正=买、负=卖；已复权） |
| oth699_newnumofshares | 交易后持仓股数（复权） |
| oth699_prevnumofshares | 交易前持仓股数（复权） |
| oth699_priortransactionnumber | 该用户历史交易笔数 |
| oth699_priordistincttradingdays | 该用户历史有交易的不同交易日数 |
| oth699_aggsplitfactor | 拆股调整因子 |
| oth699_executiontimestamp | 事件记录时间戳 |

**机制**：散户净买入强度 / 持仓变动比例。**这是 DEU 已验证模板（`divide(vec_sum(value), add(vec_sum(holdings), 0.0001))`）在散户维度的同构移植**——用比值不用差值、分母加 ε。
**注意**：DEU 那个 institutions1 模板搬到 GBR 后实测 S = **−0.13 / 2Y −0.64**（W22a），机制先验正确 ≠ 区域内可用，必须实测。

### 4.3 ★★★★ pv109 — Bond Yield Data（cov **0.3319**，PV 塔）
26 个 VECTOR 字段，债券价格/收益率/票息/期限结构：

- 收益率族：`ask_side_yield_to_maturity`、`bid_side_yield_to_maturity`、`midpoint_yield_to_maturity`、`ask_side_conversion_yield`、`bid_side_conversion_yield`、`midpoint_conversion_yield`
- 价格族：`last_traded_price`、`highest_bid_price`、`lowest_ask_price`、`midpoint_trade_price`、`initial_issue_price`、`redemption_value_amount`
- 结构族：`bond_coupon_rate`、`current_coupon_rate`、`coupon_payment_frequency`、`bond_maturity_structure`、`coupon_type_description`、`interest_day_count_basis`、`pv109_maturity`
- 规模/流动性族：`pv109_amt_issued`、`pv109_amt_outstanding`、`face_value_amount`、`total_traded_volume`、`minimum_bond_denomination`、`minimum_trade_increment`
- 日期族：`pv109_announce_dt`

**机制**：债券市场对股票的前瞻性。信用利差扩大 → 股票后续跑输（credit-equity lead-lag）。
**注意**：`bid_side_yield_to_maturity` 与 `ask_side_yield_to_maturity` 之差就是**债券买卖价差**，是流动性代理；`midpoint_yield_to_maturity` 的时序 z-score 是信用风险变化代理。

### 4.4 ★★★ other384 — NLP on conference conversation（cov 0.2175，66 个 VECTOR）
财报电话会文本结构特征，分为 **presentation（宣讲）** 与 **QA（问答）** 两段，各有三套命名（`oth384_*` / `presentation_*` / `qa_*`）：

- 情绪：`presentation_overall_sentiment_score`、`qa_overall_sentiment_score`、`oth384_presentation_tone`、`oth384_qa_tone`
- 词频：`presentation_positive_word_frequency`、`presentation_negative_word_frequency`、`qa_positive_word_frequency`、`qa_negative_word_frequency`、`oth384_qerfsop_aq`、`oth384_qerfgen_aq`
- 结构：`presentation_paragraph_total`、`qa_paragraph_total`、`presentation_sentence_total`、`qa_sentence_total`、`presentation_word_total`、`qa_word_total`、`qa_question_total`
- 参与者：`speaker_is_ceo_flag`、`speaker_is_cfo_flag`、`oth384_oecsi`、`oth384_ofcsi`、`conference_analyst_attendees`
- 行为：`presentation_laughter_count`、`qa_section_laughter_count`

**机制**：Loughran & McDonald (2011) 财报电话会语调；「**QA 段 vs 宣讲段的情绪差**」是最经典的高信息量构造（管理层在问答段被迫更坦诚）。
**优点**：`qa_sentiment − presentation_sentiment` 这种**段间差**是天然的正交构造，不是「情绪水平」的变体。
**风险**：全部 VECTOR(event)，且是季频事件稀疏数据 → 需 `ts_backfill(·, 80)` 填季报空档，**严禁当日频均线**。

### 4.5 ★★★ order_book_imbalance（cov 0.1649–0.2028，240 个 VECTOR，OTHER 塔）
限价订单簿全量微观结构。字段族：

- 收盘集合竞价：`auction_order_imbalance_absolute`、`auction_order_imbalance_notional`、`auction_order_imbalance_pct_adv`（占 ADV 比例，最可直接比较）、`auction_order_imbalance_pct_auction`
- 订单事件计数：`ask_order_deletion_count`、`bid_order_deletion_count`、`ask_order_insertion_count_2`、`bid_order_insertion_count`、`ask_order_execution_count`、`bid_order_execution_count`、`ask_order_modification_count`、`bid_order_modification_count`
- 订单量：`ask_order_volume_deleted`、`ask_order_volume_executed`、`bid_order_volume_after_modification`、`ask_order_volume_before_modification`
- 挂单存活时间：`avg_rest_time_{ask,bid}_{cancelled,filled,partial}_lvl{1..5}`（侧 × 结局 × 深度，30 个字段）

**机制**：订单流不平衡（OFI）是文献中最强的短周期预测量（Cont, Kukanov & Stoikov 2014）。
**两个独立可用的构造**：
1. **收盘竞价失衡** `auction_order_imbalance_pct_adv` —— 收盘压力，日频、cov 0.20 最好；
2. **撤单压力** `divide(deletion_count, insertion_count)` —— 流动性脆弱度，是**比值**不是水平。
**风险**：cov 0.16–0.20 意味着 TOP700 里仅 110–140 只有数据 → CONCENTRATED_WEIGHT 与 sub-universe 闸风险高。

### 4.6 ★★★ euro_equity_imbalance（cov 0.1568，4 个 VECTOR）
`bucketed_net_order_imbalance_{quantile,uniform}`、`bucketed_sign_imbalance_{quantile,uniform}` —— 按参与者分桶的净订单失衡符号。
**机制**：机构 vs 散户订单失衡（参与者级）。**GBR 是欧洲区，这是唯一明确标注 European 的失衡数据集**。
**风险**：只有 4 个字段，且 quantile/uniform 两个变体高度同源，实际只能算 1–2 条独立腿。

### 4.7 ★★★★ pv106 — Microstructure Spread Data（8 个 **MATRIX**，PV 塔）
全批**唯一纯 MATRIX 的 PV 候选**，无 VECTOR 算子协议负担：

| 字段 | 含义 | alphaCount |
|---|---|---:|
| pv106_spreadbp | 买卖价差（bp，以中间价/VWAP 归一） | 11 |
| pv106_lastspreadbp | 最近 30 分钟买卖价差（bp） | 5 |
| pv106_spread | 最优买价与最优卖价之差（计价货币） | 3 |
| pv106_lastspread | 最近 30 分钟买卖价差（计价货币） | 9 |
| aggregated_slippage_metric | 跨多笔/多场所的综合滑点 | 4 |
| slippage_at_spread_35 | 执行量为 ADV 35% 的滑点估计 | 6 |
| transaction_cost_maximum | 最大估计交易成本 | 2 |
| transaction_cost_percentile_10 | 交易成本 10 分位 | 4 |

**机制**：Amihud (2002) 非流动性溢价 —— 高价差股票要求更高预期收益；反向用法是**价差扩大 = 流动性恶化 = 短期跑输**。
**为什么优先**：MATRIX 类型、无 VECTOR 连坐风险、alphaCount 全 ≤11（极低竞争）、字段语义全是「成本」类，与 pv1 的价格量动量天然正交。

### 4.8 ★★★ pv173 — Corporate Bond Pricing Data（81 个 VECTOR，PV 塔）
同一批 ~27 个底层指标各有三套口径：`pv173_rawratios_*`（原始值）、`pv173_zscores_*`（z-score）、`pv173_ranks_*`（横截面 rank）。

底层指标族：
- **股债背离**：`eqbddivrgbdrtn120d`（120 日股票收益 vs 发行人债券收益背离）、`eqbddivrgsprd5y120d`（股票 vs 5 年 z-spread 变动背离）、`eqbddivrgsprd5y120dsbst`
- **信用利差**：`mt5yzspread`、`mt5yzspreadchg60d`、`mt5yzspreadzscore60d`、`mt5yzspreadchgstd20d`、`mt5yzspreadindrel`（行业相对）
- **债券曲线 PCA**：`shift`（水平）、`tilt`（斜率）、`twist`（曲率），各有 `chg60d`/`zscore60d`/`std60d`/`ema60d` 变体
- **期限结构**：`reltermspreadtransfema120d`
- **债券收益**：`bondreturn20deqwt`

**机制**：股债背离均值回归（同一发行人的股票与债券对同一信用信息反应速度不同）。
**风险**：平台 cov 报 0.0，且描述中大量写「Cross-sectional rank (ASI, D0)」/「(USA, D0)」，**区域来源可能不是欧洲** → GBR 覆盖必须实测。

---

## 5. 机制 → 字段 → 模板 映射表（本批设计依据）

| # | 机制 | 数据集 | 字段 | 模板骨架 | 状态 |
|---|---|---|---|---|---|
| M1 | 关联公司动量溢出 | other545 | `vec_avg(oth545_score)` | `ts_decay_linear(ts_zscore(ts_rank(ts_backfill(·,500),126),252),5)` | W24-1 在跑 |
| M2 | 散户净买强度（比值） | other699 | `divide(vec_sum(sharestraded), add(vec_sum(newnumofshares),1))` | `rank(ts_backfill(·,500))` | W24-2 在跑 |
| M3 | 收盘集合竞价失衡 | order_book_imbalance | `vec_avg(auction_order_imbalance_pct_adv)` | `ts_mean(ts_zscore(ts_rank(ts_backfill(·,500),22),252),5)` | W24-3 在跑 |
| M4 | 参与者净订单失衡 | euro_equity_imbalance | `vec_avg(bucketed_net_order_imbalance_quantile)` | `ts_mean(ts_zscore(ts_backfill(·,500),252),5)` | W24-4 在跑 |
| M5 | 非流动性溢价（价差） | pv106 | `pv106_spreadbp` | `ts_decay_linear(ts_zscore(ts_rank(ts_backfill(·,500),252),504),5)` | W24-5 在跑 |
| M6 | 交易成本恶化（变化率） | pv106 | `aggregated_slippage_metric` | `ts_mean(ts_delta(ts_zscore(group_zscore(ts_backfill(·,500),subindustry),252),5),22)` | W24-6 在跑 |
| M7 | 信用风险前瞻（收益率） | pv109 | `vec_avg(midpoint_yield_to_maturity)` | 同 M5 | W24-7 在跑 |
| M8 | 股债背离回归 | pv173 | `vec_avg(pv173_zscores_eqbddivrgbdrtn120d)` | `ts_mean(ts_zscore(ts_backfill(·,500),252),5)` | W24-8 在跑 |
| M9 | QA vs 宣讲情绪差 | other384 | `qa_overall_sentiment_score − presentation_overall_sentiment_score` | 待设计 | 未派发 |
| M10 | 撤单压力（流动性脆弱度） | order_book_imbalance | `divide(vec_sum(bid_order_deletion_count), add(vec_sum(bid_order_insertion_count),1))` | 待设计 | 未派发 |
| M11 | 指引上调 vs 下调事件广度 | event_ml_signals | `ts_sum(vec_sum(corporate_guidance_raised_event),66) − ts_sum(vec_sum(corporate_guidance_lowered_event),66)` | 待设计 | 未派发 |
| M12 | 分析师覆盖密度（网络度） | other546 | `vec_avg(analyst_coverage_count)` | 待设计 | 未派发 |

**算子数**：M1–M8 全部落在 [10,15]（骨架 5 + CORE 5/6/7）。M9–M12 设计时必须先数算子。

---

## 6. 覆盖与类型陷阱清单（本批实测）

1. **cov=0.0 不可信**：pv173 / pv106 / pv71 / pv13 / other571 / other128 / other567 / other425 / other315 / other566 / other696 / event_ml_signals / continuation_score / intraday_pv_feats 全报 0.0，但 pv106 的 8 个 MATRIX 字段明显是日频常规数据。判死只认 `get_alpha_yearly_stats` 逐年 longCount。
2. **VECTOR(event) 合法第一跳只有** `vec_avg/vec_sum/vec_max/vec_min/vec_count/vec_stddev/vec_range`、`reduce_*`、`kth_element(F,d,k=1)`（k 必须具名）。必须先聚合再套任何标量算子。
3. **MATRIX 优先**：pv106（8 个 MATRIX）与 other571（23 个 MATRIX）无 VECTOR 协议负担，设计成本最低；VECTOR 数据集要多一层聚合。
4. **GROUP 字段可当分组轴**：pv13 自带 `pv13_22_800_sector`、`pv13_5_sector`、`pv13_eur_revere_risc_sector_level` —— 但注意 `pv13_22_800_sector` 绑定 top800 universe，与 TOP700 不匹配时会出现「静默卡 progress 0.15」（已在本项目 pv29/pv5 上实测过该故障）。
5. **季频事件必须 `ts_backfill(·,80)`**：earnings6 / other384 / event_ml_signals 属此类，**严禁 `ts_mean(EPS,252)`** 这类日频平滑（等价于把台阶抹平）。
6. **塔位归属由字段决定，不由「我以为」决定**：`cap` 属 PV（用 `bucket(rank(cap),…)` 会把 risk 件变成 risk/pv）；`insider_*_matrix` 属 OTHER 不属 insiders；`techindi_model` 属 OTHER 不属 model。

---

## 7. 下一步

- W24 8 臂（M1–M8）在跑，两个 4 臂 multisim：`rfMWCeC5a9csscYwnGY3A`（OTHER）/ `42POwEf3k4tG9eteTeC6Q9z`（PV）。
- 收批后做归因：按 **M1–M8 机制编号**归因，而不是按单条 alpha 归因；同一机制出一颗即封。
- M9–M12 作为第二波（模板互异），确保 OTHER/PV 两塔各有 ≥10 个结构互异的模板可用。
- 优先解锁：3 颗全闸候选（Xg9b5ZX0 / zq38KdX1 / YP1bGkGq）的 prod 判决 → 用户授权 → 一次性点亮 pv + other 两塔。
