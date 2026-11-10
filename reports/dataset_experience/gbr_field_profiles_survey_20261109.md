# GBR（TOP700 / D1）字段画像存档 · 2026-11-09

> 取数口径：`get_datasets(region="GBR", delay=1, universe="TOP700")` 得 **177 个数据集**；
> `get_datafields(region="GBR", dataset_id=…, universe="TOP700", delay=1)` 逐集实读。
> 命名规则：`<region小写>_<dataset或主题>_<campain|survey>_<YYYYMMDD>.md`（历史沿用 `campain` 拼写，勿改）。
> 本文是**跨 category 的字段画像总表**；单集深挖结论仍在各自的 `gbr_<dataset>_campain.md`。

## 0. 读这张表前必须知道的三件事

1. **`coverage` 字段不可信**：平台给的 `coverage: 0` 既可能是「无数据」，也可能是「未登记」。
   实测反例：`imbalance5` `coverage 0` 却是本轮核心腿（`leAgQPO5` S 2.16）；`option1` `coverage 0` 实际有完整 IV 曲面（见 option.md）；
   `macro27` `coverage 0` 实测 S 1.45。**⇒ 判可用性要看「跑一条探针的 longCount/shortCount」，不是看 coverage。**
2. **VECTOR 字段必须先折叠**（`vec_avg` / `vec_sum` / `vec_count`），且折叠语义决定量纲：
   股数/金额用 `vec_sum`，比率/评分用 `vec_avg`。`add(计数,1)` 兜底会触发 `unit_handling=VERIFY` 整条 FAIL。
3. **更新频率不写在元数据里**，只能从字段名与时序行为反推：13F 类=季度、EPS/电话会议=季度事件、
   新闻/社媒/借贷=日频、基本面科目=季度累积、风险残差=日频。

## 1. 逐 category 画像

| category | 数据集数 | cov>0 数 | 本轮是否可出信号 | 形态特征 |
|---|---:|---:|---|---|
| **pv** | 16 | 16 | 是（分母/价格类，但属禁混集合） | MATRIX 日频 |
| **model** | 46 | 46 | 边际（`mdl28` 作主腿 S1.62 过闸） | MATRIX 日频，含大量排名/评分 |
| **other** | 41 | 41 | 少数（techindi 族强、另类数据全灭） | 混合，1500 字段级大集 |
| **analyst** | 19 | 8 | **是**（广度/修正两个方向都出过闸） | VECTOR 为主，事件+快照 |
| **news** | 18 | 6 | **是（但已饱和）** | VECTOR，事件型，多分类器情绪 |
| **fundamental** | 12 | 3 | **是**（`fnd6/cap` 唯一量产线） | MATRIX 季度科目 |
| **risk** | 5 | 2 | 边际（残差收益作主腿弱） | MATRIX 日频残差 |
| **institutions** | 5 | 4 | **待定**（`inst25` 新通道，弱短腿下 S1.19） | VECTOR 季度/日频 |
| **insiders** | 3 | 2 | **是**（方向/净买入两形态过闸） | MATRIX/VECTOR 事件型 |
| **sentiment** | 3 | 3 | 否（单字段最弱） | VECTOR 文本分数 |
| **socialmedia** | 3 | 1 | 否（S 0.23、TO 1.15） | VECTOR 帖子级 |
| **shortinterest** | 1 | 1 | **是（短腿之王）** | VECTOR 日频借贷 |
| **earnings** | 2 | 0 | **是**（EPS 意外 S1.74 过闸） | VECTOR 事件型 |
| **macro** | 1 | 0 | 边际（S1.45/F0.66/2Y3.62） | VECTOR 招聘流量 |
| **option** | 1 | 0 | 否（S 天花板 1.40） | VECTOR IV 曲面 |
| **imbalance** | 1 | 0 | **是**（已入篮） | VECTOR 订单失衡 |

## 2. 关键字段级明细（本轮实读）

### institutions
| 数据集 | 字段数 | 类型 | 实读内容 | 可用性 |
|---|---:|---|---|---|
| `institutions25` | 20 | VECTOR | **做空经理行为**：`inst25_crowding`/`concentration`/`position_change`/`security_cover_count`/`security_short_count`/`security_trade_count_1wk·1mo·3mo·1yr`/`activity`/`manager_count`/`age` | ★新通道，与 shortinterest3 不同源 |
| `institutions4` | 6 | VECTOR | 机构持仓 `current/previous` × {`market_value`, `shares`} + `percent_of_portfolio`/`percent_of_shares_outstanding` | 纯 ATOM S −0.37；仅作组合腿 |
| `institutions6` | 11 | VECTOR | 13F 机构持仓广度 | 3 载体 18 条最高 S 0.62 ⇒ 判死（TOP700 横截面无离散度） |
| `institutions1` | 7 | VECTOR | 内部人申报（`inst1_holdings` 描述含 "held by the insider"） | 判死 |
| `fund_holdings_panel` | 18 | VECTOR | 基金持仓面板 | 判死（F 墙） |

### insiders
| 数据集 | 字段数 | 类型 | 可用字段 | 实测 |
|---|---:|---|---|---|
| `insider_agg_matrix` | 34 | MATRIX | `directional_indicator`（cov 1.0，方向偏置）/ `directional_indicator_2` / `avg|total` × {`buy`, `sell`, `top_buy`, `top_sell`, `secondary_*`} _shares / `significant_value_1..4` / `directional_significant_value_1..4` | ★`directional_indicator` 主腿 S1.76 过闸；净买入比率 S1.82 过闸 |
| `insiders1` | 9 | — | — | 判死 |
| `insiders12` | 7 | VECTOR | 未开采 | 待测 |

### shortinterest3（25 字段，cov 0.849，VECTOR 日频）
`loaned_share_count_main`（**最强短腿**）· `loan_rate_volatility_{main,p5_d1}` · `average_loan_duration_days_{main,p5_d1}` ·
`transaction_count_{main,p5_d1}` · `loaned_market_value_usd_*` · `mean|max|min_loan_rate_*` · `shrt3_bar`（借券需求评级）。
实测：只有 `loaned_share_count_main` 与 `average_loan_duration_days_main` 作短腿能过闸；其余 3 个短腿全灭。

### earnings / macro / option（三个 `coverage 0` 但有数据的集）
| 数据集 | 可用字段 | 实测 |
|---|---|---|
| `earnings6` | `ern6_actual_eps` vs `ern6_estimated_eps`（同量纲相减=SUE）· `ern6_1q..4q` · `ern6_next_ed` · `preliminary_eps_range_*` | ★S1.74/F1.10/2Y2.78 **过闸** |
| `earnings_sent_matrix` | `sentiment_weighting_method1/2` · `positive|negative_sentiment_probability_3` · `likelihood_of_neutral_tone` | 语气几何全灭（S 0.16 / −1.08） |
| `macro27` | `mcr27_company_jobscreated/jobsremoved/jobsactive` · `num_jobs_*` · `avg_days_job_posting_*` · `is_job_repost_flag` | 净招聘 S1.45/F0.66/2Y3.62（差 F） |
| `option1` | `opt1_p_deltasurface_d1_vi`（IV 曲面）· `_delta` · `opt1_vp_deltasurface_d1_period` · `opt1_raw_deltasurface_d1_moneyness` · `opt1_price_*` | 纯 0.44 / 加短腿 1.39–1.40 |

### news（18 集；本轮实读 17/18/20/50/104/38）
- **news17**（48 字段，cov 0.837）：`nws17_multiple_comp_event_sentiment_score` 已入篮（`rKRPAWv9`）。
- **news18**（70，cov 0.819）：`event_sentiment_score` · `event_relevance_score` · `days_since_similar_event`（**事件新颖度**）·
  `nws18_ghc_lna`（新闻中的评级变动）· `multi_entity_*` 多实体标签。
- **news20**（46，cov 0.745）：`nws20_multiple_comp_{event_sentiment_score, nip, qmb, ber, ssc, rp_story_event_count}`。
  实测情绪 S1.84 但 F0.71；**事件条数（关注度）S0.62 判死**。
- **news50**（37，cov 0.691）：多分类器情绪 + `mws50_g_ens`（全局事件新颖度 0–100）+ `mws50_vea`（91 日事件量）。
- **news104**（11，cov 0.970）/ **news38**（3，cov 0.599）：旧轮判死。

### analyst（19 集；cov>0 的 8 集）
| 数据集 | 字段 | 实测 |
|---|---:|---|
| `analyst9` | 51 | 广度比率 (`numup−numdn)/numanalysts 主腿 S2.09–2.15 过闸 |
| `analyst93` | 100 | 分析师**技能元信息**：`anl93_estimator_relative_accuracy1/2` · `correct_revision_ratio` · `correct_forecast_times1/2` · `consistency`。实测 `correct_revision_ratio` 主腿 S 不足 |
| `analyst48` | 7 | **指数成分元数据**（`anl48_bbpdiip` 指数点股息、`bulk_count_index_members`、`bulk_idivisor`）⇒ 非个股信号 |
| `analyst_consensus` | 1772 | 实际财务值向量（`actual_bvps/capex/cfo/cogs/dividend/ebit/ebitda/ebt/eps_reported` × `annual12/quarterly16` × `fxadj`）⇒ 本质是基本面，量纲为 VECTOR 年度序列 |
| `analyst7` / `analyst47` | 502 / 5 | 旧轮封顶（1.35 / 判死） |

### risk
`risk88`：单字段 `alternative_market_cap_usd`（cov 1.0）⇒ **通用合规分母**（RISK 类，与 FUNDAMENTAL/INSTITUTIONS 组腿不受 trio 约束）。
`risk71` / `risk72`：`*_residual_return` / `residualized_return_top2500` / `cfg2_top{600,800,1200}_replicator{1,2}` ⇒ 日频特质收益。
实测 22 日特质反转在 GOLD2 形态 S 0.60 判死。`risk60` / `risk68` 未测。

### sentiment / socialmedia
- `sentiment27`（18，cov 0.800）未测；`sentiment33`（255，cov 0.322）文档级文本分数；`sentiment7`（3）旧判死。
- `socialmedia5`（13）：`scl5_s_hitscore_{average,high,low}sentiment` / `_sentimentcount` / `_wordcount` / `post_accountrating_value`；
  实测平均情绪纯 ATOM S0.23 且 **TO 1.15**（帖子级高频）。
- `socialmedia39`（1）：`scl39_top5_people_also_watch_ticker_ii` = **共视邻居 ticker 的 instrument ID 向量 ⇒ 非数值，不可直接做信号**。
- `socialmedia12`（6）未测。

### fundamental
`fundamental6`（197，cov 0.497）= 唯一量产线，`divide(fnd6_<科目>, cap)` 跨量纲族出 13 条 S≥1.58。
`fundamental86`（7）= **现成多因子十分位合成**：`fnd86_{average,earnings,fundamental,insider_trading,price_momentum,relative_valuation,risk}_score`（1–10 decile）。实测纯/加短腿 S 0.84 不足。
`fundamental45`（12）= 电话会议语言（LDA/readability/sentiment change）判死。
`fundamental22`（1）= ESG 单字段（S 0.68 判死）。

### imbalance5（2 字段，cov 0）
`imb5_score`（订单失衡评分，已入篮 `leAgQPO5`）+ 另一字段。VECTOR 日频。

## 3. 判死的字段通道（不要重试）

电话会议语言（`analyst83` / `fundamental45` / `other384` 合计 16 条 0 达标）· 另类数据（`other545`/`other47`/`other250`/`other455` 6 探针 S 0.08–0.36）·
`model106` 分析师评级（TO 0.80 爆表）· 13F 多头广度（`institutions6` 18 条最高 0.62）· 评级/星级类慢变信号 ·
文本情绪纯几何（`sentiment` / `earnings_sent_matrix` 语气面）· 社交帖子级情绪（TO 爆表）。
