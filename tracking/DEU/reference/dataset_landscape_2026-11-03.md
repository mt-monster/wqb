# DEU 数据集全景（2026-11-03 get_datasets 实拉，172 集 / 16 category，TOP500/D1）

挖矿优先级口径 = **高覆盖 × 低拥挤（alphaCount 低）**；单塔 alpha 优先非目标塔 category（用户优先序：非目标塔单塔 > 非目标塔×目标塔 > 目标塔单塔）。

## 值得排队的矿位（高 cov 低 ac）

| 数据集 | category | cov | ac/uc | 字段数 | 备注 |
|---|---|---|---|---|---|
| analyst48 Dividend estimation | analyst | 0.79 | **7/4** | 7 | 极低拥挤，几乎无人挖 |
| model53 Creditworthiness Risk | model(trio) | 0.91 | **9/9** | 22 | 低拥挤但 trio 内禁混，只能单塔 |
| other250 details data | other(trio) | 0.61 | **2/2** | 12 | valueScore 7，全库最冷 |
| risk88 Multi-Factor Risk | risk | **1.0** | 64/39 | 1 | 单字段集 |
| institutions6 Stake Ownership | institutions | **1.0** | 270/127 | 11 | 非目标塔满覆盖 |
| pv29 Derived Industry | pv(trio) | **1.0** | 66/44 | 50 | 分组轴素材 |
| pattern_scores Chart Pattern | pv(trio) | 0.99 | 266/158 | 504 | 大字段面 |
| model36 SmartRatios / model28 Structural Credit | model(trio) | 0.85/0.81 | 58/53 | 20/25 | 中拥挤 |
| fund_holdings_panel | institutions | 0.90 | 102/58 | 18 | 机构持仓 |
| sentiment27 Website Popularity | sentiment | 0.90 | 324/129 | 18 | sentiment7 的 POPULARITY_PROXY 源 |
| news20 Web Sources Sentiment | news | 0.77 | **33/27** | 46 | 低拥挤 news 位 |
| analyst93 Europe Estimate Daily | analyst | 0.64 | 193/116 | 100 | DEU 本土向 |
| insider_agg_matrix | insiders | 0.56 | 170/89 | 34 | 与 insider_matrix 的取舍待用户裁定 |

## 字段画像补录（2026-11-03 06:4x get_datafields）

- **risk88**（risk 塔）：单字段 `alternative_market_cap_usd`（MATRIX，市值 USD，定位=加权/归一化辅助）cov 1.0 / ac 70/42。**机制面薄：辅助/归一化角色，非信号源**——不做单挖矿位，留作他波的归一化素材（引用它点亮 risk 塔，非 PV）。
- **news20 Web Sources Sentiment**（news 塔，46 VECTOR）：与 news17 **同构字段族**（acb/bee/ber/bam/qep/qmb/ssc/nip 分类器 + event_relevance / event_similarity_days 新颖度 + rp_story_event_count/index 密度），双簇：裸 `nws20_*` cov 0.639 / `nws20_multiple_comp_*` **cov 0.919**。拥挤度极低（多数字段 ac 0-2）。
  ⇒ **头号矿位**。news17 波2 全灭的机制（密度/新颖度/分类器分歧/relevance 加权）按「机制×数据集」二维律**必须在 news20 重开**，不许跨集封杀；字段近重复对（裸簇 vs multiple_comp 簇）可做同机制净额。模板池设计时引用 news17/news104 台账的论坛+论文取证（relevance+novelty 过滤、情绪概率差）。

- **analyst48 Dividend estimation**（analyst 塔，7 VECTOR，cov 0.788 / ac 7/4）：**降级——机制面薄**。7 字段全是**指数级记录**而非个股级：`bbpdiip`（指数预期股息，唯一准信号）/ `bulk_count_index_members`（指数成分数）/ `bulk_idivisor`（指数除数）/ `bulk_indx_typ`（指数类型码）/ `index_bulk_ibc`（Bloomberg ID）/ `index_bulk_nfields`（记录字段数）/ `index_bulk_return_code`（返回码）。同指数成员取值相同 ⇒ 横截面方差≈指数归属签名（市值/流动性因子的重复映射）；除 bbpdiip 外全是元数据。**不单挖**，与 risk88 同待遇；「极低拥挤」实为无人问津的镜像。
- **institutions6 Stake Ownership**（institutions 塔，11 MATRIX，cov 1.0 / ac 270/127）：**头号非目标塔矿位**。个股级三大字段族——① 持仓水平：aggregate_equity_value/share_count × all_owners/institutions（4）② 买卖广度：count_institutional_buyers/sellers/holders（3）③ 交易流量：market_value/quantity × acquired/disposed（4）。机制面：机构净流比率（smart money, Chen-Jegadeesh-Wermers）、买卖广度失衡、机构渗透率变化（inst/all_owners 同集内比率，量纲安全）、拥挤度反转（holders 高=拥挤→反向）、流量/存量速度。注意 institutions1 判死**不跨集封杀**（机制×数据集二维律）。逐字段 ac 19-85 中度拥挤，字段级净额/比率结构有差异化空间。待做：论坛+论文取证后开波（模板池 ≥10）。

- **fund_holdings_panel**（institutions 塔，18 VECTOR，cov 0.88-0.93 / ac 2-41）：**基金账户级交易微结构，机制面厚**。四字段族——① 边界交易（新建仓/清仓=conviction 事件）：boundary_transaction_total/usd_value×(all/active)（4）② 交易集中度：herfindahl_index_transactions、transaction_value_distribution_score×(all/active)（4，共识 vs 单账户幕后）③ conviction 规模：large_trade_count_50bps（>0.5% AUM 大单）、top_weighted_transaction_number（conviction 持仓交易）④ 稳定边界交易 stable_boundary_trade_count_21d（21 天非重复边界交易=持久 conviction，ac 41/24 最拥挤）+ transaction_account_total 参与广度。**active vs total 天然对照变体**（主动基金信号 vs 全账户含被动噪声）。与 institutions6 同塔互补（持仓水平 vs 交易事件）；低拥挤字段多（ac 0-10）。VECTOR 聚合用 vec_sum/vec_avg。
- **sentiment27 Website Popularity**（sentiment 塔，15 VECTOR + 3 SYMBOL 元数据，cov 0.90-0.91）：Tranco 域名排名分布统计——avgranking / relpopularity08 / relpopularity1（alpha 参数对照变体）/ skewness / kurtosis / top50/75pctranking(avg) / topranking / totaldomains / totalcountrydomains + snt27_rank 单域日排名。机制=**注意力驱动错价**（Lou 2013 一线；rank 变化=注意力冲击，分布形状=注意力集中度，域名数增长=数字足迹扩张）。是 sentiment7 POPULARITY_PROXY 的源头数据集；拥挤度中高（relpopularity08 ac 58），差异化空间在分布形状（skew/kurt）与 rank 变化矩。SYMBOL 字段（时间戳元数据）不可作数值位。

## 字段画像补录 2（2026-11-03 07:1x，earnings 塔首次画像）

- **earnings6 International Findings Data**（earnings 塔，18 VECTOR，cov 0.0 / uc 44 / ac 112）：**EPS surprise 机制核心对在集内**——`ern6_actual_eps`（实际 non-GAAP 摊薄 EPS，ac 22）↔ `ern6_estimated_eps`（Estimize 加权预期，ac 25）⇒ **SUE/earnings surprise = Bernard-Thomas (1989) PEAD 经典信号**，同机制净额合成合规（同量纲 EPS↔EPS）。事件日期族（ern6_1q/2q/3q/4q 各季财报日、next_ed、conferencecalltime、board_of_directors_meeting）= **财报事件窗口素材**（公告前后漂移 = PEAD 时序结构，DellaVigna-Pollet 2009 周内效应可查）。元数据族（*_fiscal_year、wqreceivetimestamp、x_dividend）不作数值位。**在册提醒**：ern6 EPS 族是 leading-gap 5 族之一（2019 才起，2014-2018 空窗），裁定卡入篮不卡挖掘。

- **earnings_sent_matrix Global Earnings Call Sentiment Matrix**（earnings 塔，7 MATRIX，cov 0.0 / uc 67 / ac 131）：财报电话会 NLP 情绪三概率分布（`positive/negative/likelihood_of_neutral_sentiment`，三者和=1）+ argmax 标签 `overall_sentiment_score`（-1/0/1，低信息）+ 聚合语气分 `sentiment_weighting_method1/2`（天然对照变体）+ `intraday_delay_indicator`（时滞码，元数据）。**机制面**：情绪净差（pos−neg，news104「情绪概率差」配方同构）、分歧度（1−max 或三概率熵）、method1↔method2 同量纲净额、情绪转折（ts_delta 概率）。**⚠️ cov 0.0 待逐年核验**——字段是 intraday transcript slice（仅财报日附近有值，平时 NaN），稀疏性会让 cov 统计失真（other250 前例：cov 0.61 但逐年 10/10 满；反向也可能）；**连续多年空窗才排除**，须探针+get_alpha_yearly_stats 逐年验证（等槽）。若 DEU 真无数据，「极低拥挤」同样是无人问津镜像（analyst48 教训）。

### earnings 塔覆盖核验定案（2026-11-03 07:2x，探针 + get_alpha_yearly_stats 逐年）

| 集 | 探针 alpha | 2014-2018 | 2019-2023 | 判定 |
|---|---|---|---|---|
| earnings6 | `58Ek1eYk`（ern6_actual_eps） | **五年彻底空窗**（pnl=0/lc=0/TO=0 全零） | pnl/TO 有数 | **leading-gap 第 6 族**（2019 起，前段五年空窗）；暂行口径=保留标注、卡入篮不卡挖掘（★待用户裁定） |
| earnings_sent_matrix | `MPYLnZVa`（positive_sentiment_probability_3） | **逐年有数**（pnl −1.06M~−0.43M，TO 0.35-0.58） | 逐年有数（pnl +1.79M~+2.37M，TO 0.56-1.22） | **满 10 年 ✓ 合规矿位**——cov 0.0 确系 intraday slice 稀疏性统计失真，覆盖闸通过，earnings 塔点亮 |

- 判据执行：longCount=0 且 pnl=0 才算空窗（ern_sent 的 lc 多为 0 但 pnl/TO 非零 = 有交易，longCount 是年末快照口径非覆盖判据）；连续多年空窗才排除。
- **earnings_sent_matrix 开波资格确认**：情绪三概率分布（POS+NTR+NEG=1）机制面可开正式波（模板池 ≥10），可与 institutions6/fundholdings 并列为 earnings 塔首个矿位。ern6 EPS 族（SUE/PEAD）等 leading-gap 裁定后再定入篮资格。

## category 汇总（count / 平均 cov / 总 ac）

- model(trio) 45 / 0.30 / 14086 —— 最大类，trio 禁混约束主战场
- other(trio) 41 / 0.16 / 6010
- news 17 / 0.28 / 802 —— 在挖（news104/news17）
- analyst 18 / 0.27 / 8038
- pv(trio) 16 / 0.20 / 14664
- fundamental 12 / 0.12 / 4028；risk 5 / 0.37 / 688；institutions 5 / 0.49 / 430
- sentiment 3 / 0.66 / 463；insiders 2 / 0.55 / 196；earnings 2 / 0 / 235；socialmedia 2 / 0.14 / 267
- macro 1 / 0 / 149；imbalance 1 / 0 / 138；option 1 / 0 / 72；shortinterest 1 / 0.71 / 864

## 字段画像补录 3（2026-11-03 07:5x，MACRO/SOCIALMEDIA 三集）

- **macro27 Job records from job posting**（macro 塔，13 VECTOR，cov 0.0 / ac 165 / uc 78）：**招聘动态=劳动力需求机制面厚**——① 招聘净流：`mcr27_company_jobscreated`/`jobsremoved`（同机制净额=招聘扩张/收缩）② 填岗速度：`mean_days_job_closed`/`avg_days_job_posting_closed`（岗位撤下快=需求强/快速填岗）③ 重招率 `is_job_repost_flag`（重发=招聘困难/需求持续）④ 存量 `num_jobs_active`/`jobsactive`。宏观机制=公司招聘需求→增长预期（Campbell et al. labor demand 一线）；**LABOR DEMAND 动态面优先**（与 sentiment27 同教训：水平面弱）。元数据 mcr27_country/zip 不作数值位。**cov 0.0 待逐年核验**（探针在飞）。ac 165 中拥挤。
- **socialmedia12 Sentiment Data for Equity（PulsePick 供应商）**（socialmedia 塔，18 MIXED，cov 0.0 / ac 138 / uc 65）：真情绪面=`scl12_buzz`（相对情绪量）/`scl12_sentiment`/`sentiment_score`——**正是研报热度反转帖（HH77144）对口字段**（ts_decay_linear(abs(buzz),5) 骨架 + 热度-价格背离四象限，美股验证过 DEU 未测）。⚠️ 避雷：`sentiment_{open,close,high,low}_price` 是价格复制品（与 PV 语义重叠、与内建 close 高相关）；`backtest_hit_ratio`/`sentiment_significance`/`sentiment_expected_price_change` 是**供应商回测质量元数据，前瞻（look-ahead）风险高，禁作信号腿**；`entity_*` 是慢变量画像（employee_count/revenue 可作分组/条件）。cov 0.0 待逐年核验（探针在飞）。
- **socialmedia39 Investor views**（socialmedia 塔，1 VECTOR，cov 0.27 / ac 145）：**判弱降级**——唯一字段 `scl39_top5_people_also_watch_ticker_ii` 是共视邻居 ticker ID 列表（非数值，join 用），FASTEXPR 内最多 vec_count 数邻居个数（1-5 截断桶），机制天花板极低。不单挖。


## 字段画像补录 5（2026-11-03 09:1x 冷集扫描 · 172 集全清单落 _mcp_reads/ds_all_result.txt）
- **institutions25 Fund Short Selling Data**（INSTITUTIONS 塔·非trio，ac 7/uc 7，全 VECTOR，cov 0.0 待逐年探针）：inst25_crowding 拥挤度 0-100（轧空挤压机制）、inst25_age 空头持仓年龄排名（知情深度）、inst25_concentration 前三大空头占流通股%（集中度）、inst25_activity 活跃度、inst25_entry_position 建仓仓量、inst25_is_open、inst25_manager_avg_trade_length。**双机制先验**：拥挤高→挤压→正收益 vs 持仓老/集中→知情→负收益。与 si3 借券费率互补（成本面 vs 行为面）。**下一矿脉首选**。
- **other699 Individual Investor Transactions**（OTHER·trio，ac 5/uc 5，VECTOR，cov 0.506 真覆盖）：oth699_sharestraded（正买负卖）、prev/newnumofshares、priortransactionnumber、priordistincttradingdays。散户净买卖流（Barber-Odean 过度自信→负预测先验）。timestamp/splitfactor 等元数据字段非信号。
- 冷集池余量（ac≤10 待挖）：other425 Supply Chain(ac 0)、model27 Credit Risk、model141/other327 利率敏感度、model313 Intangible Asset、other567 Employee Review、other546 Institutional Network、other323 Premarket；search_interest 属注意力族（DEU 已证弱）后选。
## 字段画像补录 6（2026-11-03 10:1x · analyst46 + oth699 探针方向）

### analyst46 Analyst Investment insight Data（ANALYST 塔 · uc 2 冷集 · MATRIX 型无 event 陷阱）
- anl46_indicator：区域横截面 1-10 多空排名分（核心信号腿；分析师情绪主变量）。
- anl46_sentiment：复合情绪分（decay+贡献者技能+财报临近度+想法量方向）（核心信号腿）。
- anl46_experts：贡献者历史绩效加权（辅助腿：可信度条件/分组）｜anl46_alphadecay：想法新鲜度（辅助腿：新旧条件化）。
- **⚠️ anl46_performancepercentile = 禁信号**：「Indicator 信号过去 12 个月回测预测价格表现百分位」= 供应商信号质量元数据（backtest_hit_ratio 同族 look-ahead），只可作慢变量画像，禁入表达式。
- 机制先验：分析师情绪/revision 因子（earnings momentum 邻域）；experts 加权 = StarMine SmartEstimate 同款逻辑。开波前需论坛+论文两读。

### other699 探针方向信号（2/6 落，2026-11-03 10:1x）
- P1 净买流正向 S 0.24（ZYQE5KR0）/ P2 反向 −0.24（0mYplMb6）——**严格对称，KST 方向（散户净买正向）成立但水平面弱**。
- 待 P3 活跃笔数 / P4 比值结构（KOR 金帖无量纲化主臂）/ P5 经验腿 / P6 净持仓变化流。

## 字段画像补录 4（2026-11-03 08:2x，option/imbalance/shortinterest 三 category 首查）

- **option1 Options Volatility Surfaces**（option 塔，22 VECTOR，ac 75 / uc 32）：**IV 曲面机制面厚但算子受限**。核心=曲面坐标族 `opt1_p_deltasurface_d1_vi`（各 delta/moneyness/period 点的隐含波动率，ac 19 最热但整体冷）+ 坐标轴（deltasurface_d1_delta/moneyness、vp_deltasurface_d1_period 到期天数）+ raw 版本（raw_deltasurface_d1_vi）。经典机制=Bali-Hovakimyan IV skew（崩盘恐惧溢价）/ 期限结构 / IV 动量。**⚠️ 算子事实：vec_skewness 与 vec_std_dev 不在平台算子名单（vec_sum/avg/count 在）**——BW14163 EUR 帖的 vec_skewness 配方在 DEU 不可照抄，**IV skew 机制被阻断**，只剩 IV 水平/动量/raw-cleaned 差。避雷：opt1_price_*/opt1_volume=价格复制品；dvd/split 元数据；data_quality/isenabled=条件腿。VECTOR=曲面多点，vec_avg 聚合。**cov 0.0 须逐年核验**（探针 optsi3probe_20261103 在飞）。逐字段 ac 0-19 极冷。

- **shortinterest3 Securities Lending Files**（shortinterest 塔，25 VECTOR，**cov 0.65-0.78 实测好**，ac 918 / uc 329）：**做空约束机制面厚且完全可表达**。三族×三变体（base/_main/_p5_d1 天然对照）：① 借券成本：mean/max/min_loan_rate + loan_rate_volatility（利率高=约束强，D'Avolio/Asquith 做空约束→负收益，Boehmer-Jones-Zhang 2010 做空需求预测横截面）② 借贷量：loaned_market_value_usd/share_count ③ 期限/广度：average_loan_duration_days（持仓持久度=conviction）、transaction_count + `shrt3_bar` 借券需求评级 1-10（ac 341 最热）。**冷字段差异化空间**：average_loan_duration_days ac 9 / min_loan_rate ac 9 / loan_rate_volatility ac 8 / loaned_market_value_usd ac 13。候选机制：利率水平与变化、max−min 利差（同族净额）、期限持久度、需求评级动态。探针在飞后开正式波（论坛+论文取证 + 模板池 ≥10）。

- **imbalance5 Oil Price Resilience Scores**（imbalance 塔，2 字段，ac 144）：**判弱降级**——2 字段油价格韧性评分，机制面薄，DEU 个股横截面映射弱。不单挖。

### 算子事实（跨区通用）
`vec_skewness` / `vec_std_dev` **不在** get_operators 103 名单——外部帖（BW14163 EUR）的 vec_skewness 配方照抄前必须换算；矩统计只剩 vec_sum/vec_avg/vec_count。ts_skewness 同样不在（既有记忆）。

## 覆盖口径提醒（用户口径：连续多年空窗才排除）

cov=0.0 的集（earnings6/earnings_sent_matrix/macro27/option1/imbalance5/risk71/72 等）**不能按 cov 直接排除**——须逐年 longCount 核验后再判。earnings_sent_matrix（财报电话会情绪矩阵，ac 127）若逐年有数，是 earnings 塔的现成矿位。
## 补录 7：news29 / other425 字段画像（2026-11-04 MCP get_datafields）
- **news29 Significant Developments（news 塔·16 字段全 VECTOR）**：可用数值面=vec_count 事件计数（注意力密度）/ nws29_significance(1=High,2=Med,3=Low 均码) / nws29_frontpage(0/1 头条旗标)；topic1-3 分类码须 overlay 解码暂不用；文本字段无数值面。全字段 cov=0.0（事件型常态，覆盖以逐年 longCount/pnl 判）。两读金帖（78赞密度反转模板+107赞SNR）→ 模板池 12 臂落 s1_news29_wave1_template_pool.md，探针 6 臂双预检全过待派发。
- **other425 Supply Chain（other 塔·12 字段）**：**判死**——字段全为价格/股本/汇率复制件（close/open/volume/dividend/shares_outstanding/split_ratio），无任何供应链专属字段，无独立机制面且与 PV 内建语义重叠。

## 补录 8：workforce_flow_skills / other546 / other327 画像（2026-11-03 冷候选巡检）
- **workforce_flow_skills（other 塔·10 字段全 VECTOR·月频）**：真·劳动力流量面——employee_inflow/outflow_count（月度雇入/离职）、employee_headcount、position_seniority_level(1-4)、employee_prestige_score、total_salary_amount。**禁信号腿**：unreliable_user_count/inflow/outflow（数据质量元数据）。机制=招聘/流失净流量（比值结构 divide(inflow,outflow) 符合比值纪律）→ 企业扩张/收缩；文献先验=劳动力调整不对称 + 招聘帖因子。**下一波首选**（不在封盘族、单数据集可成表达式）。
- **other546 Institutional Network Analysis（other 塔·12 字段全 VECTOR）**：**成对网络数据**（primary×peer 公司对）——business/geographic/MD&A 文本相似度权重、executive 律动频次、共享分析师/共享高管数。vec 聚合后=个股的网络连通度面（linked-firm 信息扩散机制，Cohen-Frazzini-Malloy 供应链信息扩散先验）。复杂度高，次选。
- **other327 Rate Sensitivity（other 塔·仅 3 字段 MATRIX）**：oth327_sirc_lev/sl（利率水平/斜率敏感度）+ mktcap（PV 复制件弃）。**搁置**——可用面仅 2 字段，静态 beta 无 regime 腿不成 alpha，且搭 macro 腿=trio×非trio 配额已满禁混。
