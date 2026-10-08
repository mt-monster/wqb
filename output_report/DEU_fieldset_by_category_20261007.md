# DEU 各 Category 的字段集分析 · 2026-10-07

> 结构：**Category → 字段集（族）**。每个字段集给出：命名模式 / 字段数 / 载体数据集 / 类型 / 实测状态与天花板。
> 状态标记：✅ 有产出｜❌ 已判死｜⚠️ 部分有效或被误判｜❓ **未测**｜🚫 不能当信号

---

# 一 category = `model`（9 个数据集，~1250 高覆盖）

| # | 字段集（命名模式） | 字段数 | 载体 | 状态 | 天花板 / 说明 |
|---|---|---:|---|---|---|
| M-1 | **`mean_estimate_change_pct_<指标>_<期>_<窗>`**（预期变化率） | ~20 | `predictive_starmine` | ✅ | **`_f12m_earnings_14d_4` S1.75 / 2Y2.07 → `58gkLAkk` 已提交** |
| M-2 | `predicted_surprise_*`（预测意外） | ~20 | `predictive_starmine` | ❌ | 单信号最高 S0.86 |
| M-3 | `mdl264_*_class`（分类分数） | 380 | `model264` | ❌ | 单信号 S0.74；历史高分全多腿 |
| M-4 | `mdl25_eq_*`（因子值） | 108 | `model25` | ❌ | 单信号 S1.18 |
| M-5 | `mdl26_*`（模型因子） | 398 | `model26` | ❌ | W94 十机制全崩 |
| M-6 | `mdl238_*_rank` / `{country,industry}_relative_*_rank` / `global_{change,institutional,peer,screening}_*`（投资偏好排位） | 22 | `model238` | ❌ | **S1.33 / sub0.54**（候选为真但不够强） |
| M-7 | `mdl250_{lmt_close,lmt_open,malta,maltahc}_eq_sector`（行业相对价值） | 4 | `model250` | ❌ | S1.33 / **2Y −0.38** |
| M-8 | **`mdl216_arm*{score,rank}`**（ARM 分析师修正模型，**VECTOR**） | 45 | `model216` | ⚠️ | 历史单信号 **S1.45**；**我此前白测**（未 `vec_avg` 包装） |
| M-9 | **`mdl28_sm_structural_credit_structural_*`**（Merton 结构化信用） | 25 | `model28` | ❓ | **`distance_to_default` / `asset_drift_pct` / `asset_volatility_pct` / `leverage`** |
| M-10 | **`credit_risk_*_score` + `default_risk_*_percentile` + `star_sr_*`**（信用分） | 20 | `model36` | ❓ | `coverage/growth/leverage/liquidity/profitability_score` |
| M-11 | **`annualized_pd_<期限>_jc7`**（违约概率期限结构） | 22 | `model53` | ❓ | 1m→10y 十条期限曲线 |
| M-12 | `star_new_eps_*`（智能预期 / 意外预测 / 分析师数） | 10 | `model30` | ❓ | — |
| M-13 | `{closing_price,two_fifty_day_total_return,five_day_total_return}_dlr2` | 42 | `analyst_earnings_ibes` | ❌ | 单信号 S0.95 |
| M-14 | `days_since_last_report_3`（财报时点） | 1 | `predictive_starmine` | ❌ | S0.30 |
| M-15 | `mdl106_*` | 8 | `model106` | 🚫 | 历史换手 0.80 爆表 |

**⇒ model 的可用面：M-1（已产 1 颗）× M-9/10/11（67 字段信用风险，未测）× M-8（45 VECTOR，最可能翻案）**

---

# 二 category = `analyst`（6 个数据集，~650 高覆盖）

| # | 字段集（命名模式） | 字段数 | 载体 | 状态 | 天花板 / 说明 |
|---|---|---:|---|---|---|
| A-1 | **`<指标>_y{1,2}_estimate_change_3mo`**（预期变化率） | 8 | `analyst_factor_signals` | ✅ | **`eps_y1_...` S1.65 / F1.47 / 0失败 → `9qWX78vV` 就绪（塔 DEU/D1/ANALYST）** |
| A-2 | `*_revision_magnitude`（修正幅度） | 3 | 同上 | ❌ | S0.78 |
| A-3 | **`*_{skewness, asymmetry, coeff_var}`**（分歧度，**最大类**） | 17 | 同上 | ❌ | **≈0（有研报依据仍全灭）** |
| A-4 | `*_consensus_value`（共识水平） | 6 | 同上 | ❌ | <0 |
| A-5 | `*_cagr_{2,3,4}yr`（增长） | 9 | 同上 | ❌ | S0.31 |
| A-6 | `*_trend_slope_1yr`（趋势） | 3 | 同上 | ❌ | S0.22 |
| A-7 | `*_raisednum` / `*_lowerednum`（修正广度，44 组配对） | ~88 | `analyst7` | ❌ | S0.68（形态合规但无信号） |
| A-8 | **`est_12m_<指标>_{num, num_28d, raised, lowered, raised_1wk}`**（计数 / 事件） | ~330 | `analyst7` | ❌ | **2Y有S无**（2Y 1.59~1.67 / S 0.53~0.65） |
| A-9 | `anl93_{accuracy,consistency,correv,estimator}_*`（**分析师技能元数据**，VECTOR） | ~60 | `analyst93` | ❌ | S≤0.43，**换手 0.019~0.029（静态）** |
| A-10 | **`anl93_recprofitabilityprev_*_profitability2`**（覆盖持续性，**VECTOR**） | ~28 | `analyst93` | ⚠️ | **换手 0.0795 正常、历史单信号 S1.30** ⇒ **活的族，需按轴深/窗长扫描** |
| A-11 | `anl44_2_{eps,roe,bps,tbvps}_value`（VECTOR 价值） | 48 | `analyst44` | 🚫 | 换手 **1.64** 爆表 |
| A-12 | `anl9_consensusv2span_*` / `anl9_{s_numup,daily_numup}` | 20 | `analyst9` | 🚫 | 换手 **0.73~1.47** 爆表 |
| A-13 | `anl48_bulk_*` / `anl48_index_bulk_*`（索引元数据，VECTOR） | 7 | `analyst48` | ❓ | 疑似无信号 |
| A-14 | `anl47_indicator` | 1 | `analyst47` | ❓ | — |

**⇒ analyst 的可用面：A-1（已产 1 颗）× A-10（活的族，未深挖）**

---

# 三 category = `fundamental`（2 个数据集，39 高覆盖）

| # | 字段集（命名模式） | 字段数 | 载体 | 状态 | 天花板 / 说明 |
|---|---|---:|---|---|---|
| F-1 | **`fnd6_<科目>` 原始财报科目**（总资产 / 净利 / 营收 / 权益 / 税 / 利息 / **经营现金流**） | 38 | `fundamental6` | ❌ | 7 机制 × 70 条全部不过，**最高 S1.03** |
| F-2 | `fnd6_adesinda_curcd` / `idesindq_curcd`（ISO 货币码） | 2 | 同上 | 🚫 | 纯标签 |
| F-3 | `fundamental22`（1 字段） | 1 | `fundamental22` | ❓ | — |

**★ F-1 内部的子机制**：内部比率 0.37｜**价值收益率 0.89（最强）**｜规模化改善 0.60｜PEAD 事件门控 1.03（CW 互斥）｜回归残差 0.33｜变化构造 0.46。

---

# 四 category = `pv`（3 个可用数据集，734 高覆盖）

| # | 字段集（命名模式） | 字段数 | 载体 | 状态 | 天花板 / 说明 |
|---|---|---:|---|---|---|
| P-1 | **`<形态名>_<统计量>_simscore_lookback{60,120}`**（技术形态相似度） | 504 | `pattern_scores` | ❌ | 40 条全灭，**最高 S0.46**；换手 0.14~0.29（快信号） |
| P-2 | `factor<n>_group<n>_top<n>_<ver>`（分组） | 180 | `pv30` | 🚫 | GROUP，**只能当轴** |
| P-3 | `sta1_*`（分组） | 50 | `pv29` | 🚫 | GROUP，**只能当轴** |
| P-4 | 元字段 `close` / `vwap` / `volume` / `adv20` / `returns` / `cap` / `sharesout`… | 23 | `pv1` | 🚫 | **可作分母 / 轴；单独作信号 prod 必高**（平台 sector 3749 / industry 3251 alphas） |

**⇒ PV 在 DEU 无可用信号面。**

---

# 五 category = `news`（5 个数据集，212 高覆盖）

| # | 字段集（命名模式） | 字段数 | 载体 | 状态 | 说明 |
|---|---|---:|---|---|---|
| N-1 | **`nws{17,18,20}_{acb,bam,bee,ber}`**（事件元数据族，**VECTOR**） | ~60 | news17/18/20 | ❓ | 全未测 |
| N-2 | **`{nws17,news18,news20}_multiple_*`**（多实体事件，**VECTOR**） | 57 | 同上 | ❓ | 未测 |
| N-3 | **`event_sentiment_score`** / `event_relevance` / **`event_similarity_days`** | ~15 | news17/18/20/50 | ❓ | **情绪 + 相关性 + 相似事件距今天数** |
| N-4 | **`mws50_*`**（含 `ens` 集成分 / `ens_elapsed`，**VECTOR**） | 37 | news50 | ❓ | 未测 |
| N-5 | `analyst_recommendation_change{,_score}` | 2 | news17/18 | ❓ | 未测 |
| N-6 | `stable_boundary_trade_count_21d{,_active}` | 2 | news18 | ❌ | 单信号 S1.06 / 0.89 |
| N-7 | `boundary_transaction_total{,_active}` | 2 | news18 | ❌ | S0.90；换手 0.46 |

**★ 论坛指出：新闻类另类数据"未被大量 Alpha 使用" ⇒ prod 相关性墙压力小。**

---

# 六 category = `sentiment`（2 个数据集，21 高覆盖）

| # | 字段集（命名模式） | 字段数 | 载体 | 状态 | 说明 |
|---|---|---:|---|---|---|
| S-1 | **`snl27_{avgranking, relpopularity<n>, top<n>pctranking{,avg}, kurtosis, skewness}`**（零售关注度/人气排名，**VECTOR**） | 14 | `sentiment27` | ❓ | **attention-driven buying 的载体** |
| S-2 | `aggregate_{collection_timestamp,reference_date}` / `ranking_reference_date` | 4 | 同上 | 🚫 | SYMBOL，时间戳 |
| S-3 | `sentiment7`（3 字段） | 3 | `sentiment7` | ❓ | — |

---

# 七 category = `shortinterest`（1 个数据集，25 高覆盖）

| # | 字段集（命名模式） | 字段数 | 载体 | 状态 | 说明 |
|---|---|---:|---|---|---|
| SI-1 | **`{average,max,mean,min}_loan{_duration_days,_rate,*}`**（借券期限/费率，**VECTOR**） | 12 | `shortinterest3` | ❌ | `mean_loan_rate_main` 历史 2.02 **全多腿**，单信号仅 0.73 |
| SI-2 | **`loan_rate_volatility{,_main,_p5_d1}`**（费率波动） | 3 | 同上 | ❓ | **未单独测** |
| SI-3 | **`loaned_market_value_usd` / `loaned_share_count`**（借出市值/股数） | 6 | 同上 | ❓ | 未测 |
| SI-4 | `transaction_count*`（借券笔数） | 3 | 同上 | ❓ | 未测 |
| SI-5 | `directional_indicator*` | 2 | `shortinterest3`/`insider_agg_matrix` | ❌ | 历史 1.86 **全多腿**，0 条单信号 |

**★ 注**：SI-1 有 3 个后缀版本（裸 / `_main` / `_p5_d1`，cov 0.668/0.687/0.783）—— **同字段三形态，可作对照**。

---

# 八 category = `institutions`（2 个数据集，29 高覆盖）

| # | 字段集（命名模式） | 字段数 | 载体 | 状态 | 说明 |
|---|---|---:|---|---|---|
| I-1 | **`count_institutional_{buyers,holders,sellers}_security`**（机构家数） | 3 | `institutions6` | ❓ | **MATRIX cov=1** ⇒ 无需 `vec_*` |
| I-2 | **`market_value_institutional_shares_{acquired,disposed}` / `quantity_institutional_shares_*`**（增减持） | 4 | 同上 | ❓ | MATRIX cov=1 |
| I-3 | **`aggregate_{equity_value,share_count}_{all_owners,institutions}`**（总持股） | 4 | 同上 | ❓ | MATRIX cov=1 |
| I-4 | **`boundary_transaction_{total,usd_value}{,_active}`**（基金交易边界，**VECTOR**） | 4 | `fund_holdings_panel` | ❓ | cov 0.88~0.93 最高 |
| I-5 | **`herfindahl_index_transactions{,_active}`**（持仓集中度） | 2 | 同上 | ❓ | 未测 |
| I-6 | **`large_trade_count_50bps{,_active}`**（大额交易） | 2 | 同上 | ❓ | 未测 |
| I-7 | `security_transaction_usd_value*` / `top_weighted_*` / `stable_boundary_*` / `transaction_{account,value}_*` | 8 | 同上 | ❓ | 未测 |

**★★ I-1~I-3 是全 DEU 唯一的「未测 + MATRIX + cov=1」字段集** ⇒ **最快上手**。

---

# 九 category = `other`（4 个可用数据集，1589 高覆盖）

| # | 字段集（命名模式） | 字段数 | 载体 | 状态 | 说明 |
|---|---|---:|---|---|---|
| O-1 | **`oth455_<关系族>_*_cluster_{5,10,20,50}`**（关系聚类，GROUP） | 1200 | `other455` | 🚫 | **只能当轴**（我们一直在用） |
| O-2 | **`oth455_<关系族>_{n2v,roam}_*_pca_fact<n>_value`**（关系图节点嵌入，MATRIX） | 300 | 同上 | ❌ | 作信号全灭；**换手 0.012（静态结构特征）** |
| O-3 | **`oth47_{organic,paid_search}_*`**（搜索流量 / 广告投放，**VECTOR**） | 9 | `other47` | ❓ | **最另类**：`organic_{cost,keywords,traffic}` / `paid_search_{budget_estimate,terms_count,visitors}` |
| O-4 | **`oth250_*` / `product_price_*` / `average_star_score` / `item_{rating,review_count}`**（电商价格与评价，**VECTOR**） | 12 | `other250` | ❓ | 商品价格带 + 评分/评论数 |
| O-5 | **`idiosyncratic_return_*` / `oth532_{emerging,global}_*_specificreturn`**（特质收益） | 8 | `other532` | ❓ | 残差动量 |
| O-6 | `oth250_rank` / `oth47_rank` | 2 | 同上 | ❓ | 排位 |
| O-7 | `dl_riskfree_returns`（分位数桶标签） | 57 | — | 🚫 | **实为标签，非信号** |
| O-8 | `insider_matrix` / `insider_trx_matrix`（各 1） | 2 | — | ❓ | — |
| O-9 | `stock_cluster_dl`（1） | 1 | — | ❓ | — |

---

# 十 category = `insiders` / `risk`（小池）

| # | 字段集 | 字段数 | 载体 | 状态 |
|---|---|---:|---|---|
| IN-1 | `directional_indicator{,_2}` | 2 | `insider_agg_matrix` | ❌（历史全多腿） |
| R-1 | **`rsk60_{crowding, offer, last, datatime}`** | 4 | `risk60` | ❓ |
| R-2 | **`lending_fee_bid_rate`**（融券费率，**VECTOR**） | 1 | `risk60` | ❓ |
| R-3 | `risk88`（1） | 1 | `risk88` | ❓ |

---

# 十一 汇总：字段集总账

| category | 字段集总数 | ✅ 有产出 | ❌ 判死 | ⚠️ 待深挖 | ❓ 未测 | 🚫 不可用 |
|---|---:|---:|---:|---:|---:|---:|
| `model` | 15 | **1** | 8 | 1 | **4** | 1 |
| `analyst` | 14 | **1** | 10 | 1 | 1 | 2 |
| `fundamental` | 3 | 0 | 1 | 0 | 1 | 1 |
| `pv` | 4 | 0 | 1 | 0 | 0 | 3 |
| `news` | 7 | 0 | 2 | 0 | **5** | 0 |
| `sentiment` | 3 | 0 | 0 | 0 | **2** | 1 |
| `shortinterest` | 5 | 0 | 2 | 0 | **3** | 0 |
| `institutions` | 7 | 0 | 0 | 0 | **7** | 0 |
| `other` | 9 | 0 | 1 | 0 | **5** | 3 |
| `insiders`/`risk` | 4 | 0 | 1 | 0 | **3** | 0 |
| **合计** | **71** | **2** | **26** | **2** | **31** | **11** |

**⇒ 71 个字段集里：2 个有产出、26 个判死、2 个待深挖、31 个未测、11 个不可用。**

---

# 十二 未测字段集的优先级（31 个里挑最优）

| 优先 | 字段集 | category | 字段 | 类型 | 理由 |
|---|---|---|---|---|---|
| **1** | **I-1~I-3 机构家数 / 增减持 / 总持股** | institutions | 11 | **MATRIX cov=1** | 全 DEU 唯一「未测+MATRIX+cov=1」 |
| **2** | **M-9/10/11 信用 / 违约风险** | model | **67** | MATRIX | **最大全新机制族**（Merton 结构模型） |
| **3** | **M-8 `mdl216_arm*`** | model | 45 | VECTOR | 历史单信号 **S1.45**，**包装错了** ⇒ 最可能翻案 |
| **4** | **SI-2~SI-4 借券费率波动 / 借出量 / 笔数** | shortinterest | 12 | VECTOR | 做空压力，且有"同字段三形态"可对照 |
| **5** | **N-3 事件情绪 / 相关性 / 相似天数** | news | ~15 | VECTOR | 全新机制，prod 墙压力小 |
| **6** | **O-3/O-4 搜索流量 / 电商评价** | other | 21 | VECTOR | **最另类**，独特性最高 |
| **7** | **S-1 零售关注度** | sentiment | 14 | VECTOR | attention 异象 |
| **8** | **A-10 `recprofitabilityprev_*_profitability2`** | analyst | ~28 | VECTOR | **已确认是活的族**（换手正常、历史 S1.30） |
| **9** | I-4~I-7 基金交易 / 集中度 | institutions | 18 | VECTOR | — |
| **10** | O-5 特质收益 / R-1~R-3 拥挤度 / M-12 | 多 | ~17 | MATRIX | 小池 |

**★ VECTOR 字段集的额外步骤**：先搜 `vec_*` 聚合算子（7 选 1），再搜轴深与窗长。
