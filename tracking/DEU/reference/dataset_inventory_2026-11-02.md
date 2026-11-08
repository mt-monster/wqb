# DEU/TOP500/D1 数据集全量台账（2026-11-02 平台实拉）

**172 个数据集 / 14 category**（get_datasets 实拉）。选集纪律：塔混禁令（trio=PV/MODEL/OTHER 互禁、trio×非trio ≤5 已满）+ 单塔优先非目标塔 category + 交叉 mining_yield + 覆盖口径（连续多年空窗才排除）。

## category 分布与关键集

| category | 数量 | 关键集（ac=alphaCount） |
|---|---|---|
| model | 46 | model38 Growth Valuation 6105 / model25 Earnings Quality 1946 / predictive_starmine 1143 / model26 Analyst Revisions 908 / model216 629 |
| other | 42 | techindi_model 4055 / dl_riskfree_returns 922 / other455 Rel-Enhanced AI 219 / order_book_imbalance 104 / other335 Dividend Model 99 |
| analyst | 18 | analyst7 Broker Estimates 3993 / analyst_factor_signals 1575 / analyst15 649 / analyst69 515 / analyst_consensus 413 |
| pv | 16 | pv1 12639 / intraday_pv_feats 510 / pv20 619 / pattern_scores 266 / pv30 287 / pv29 66 |
| news | 16 | news81 223 / news18 Ravenpack 137 / news104 100 / news17 87 |
| fundamental | 12 | fundamental17 1742 / fundamental6 1028 / fundamental72 275 / fundamental89 412 / fundamental86 172 / fundamental90 153 |
| risk | 5 | risk60 证券借出 395 / risk68 Forecast 169 |
| institutions | 5 | institutions6 270 / fund_holdings_panel 102 |
| sentiment | 3 | sentiment27 网站人气 324 / sentiment7 94 |
| insiders | 2 | insider_agg_matrix 170 / insiders1 26 |
| earnings | 2 | earnings_sent_matrix 127 / earnings6 108 |
| socialmedia | 2 | socialmedia39 137 / socialmedia12 130 |
| shortinterest | 1 | shortinterest3 864 |
| macro | 1 | macro27 招聘岗位 149 |
| imbalance | 1 | imbalance5 油价韧性 138 |
| option | 1 | option1 波动率曲面 72 |

## 字段画像记录

### other425 Supply Chain Data —— ✗ 判死（2026-11-02）
12 字段全 VECTOR 通用价量字段（daily_closing_price_2 / daily_trading_volume / market_value_total_2 …），cov=0 / ac=0。**名称与内容错位**：DEU 未暴露供应链关系内容，空壳集不可用。教训：ac=0 的集先拉字段再动心。

### macro27 Job records from job posting —— ✓ 可用（2026-11-02）
13 字段全 VECTOR（须 vec_* 包裹）。机制=**劳动需求**：
- 流量计数族：`num_jobs_created`(ac12) / `num_jobs_active`(ac28) / `num_jobs_removed`(ac10) + 公司级 `mcr27_company_jobs*`——**计数/流量类，必须 ts_rank(·,252) 去规模混淆**（大公司天然岗位多）。
- 时长水平族：`mean_days_job_active`(ac42) / `mean_days_job_closed`(ac64) / `avg_days_job_posting_*`——水平即信号，禁时序归一化。
- 事件旗标：`is_job_repost_flag`(ac28)——重复挂牌=需求走弱信号。
经济学机制：招聘加速=扩张预期（正向）；挂牌删除激增=收缩（负向）；repost 率升=需求疲软。

**论坛模板（AK85882《招聘变化与业务扩张：hiring_trends 在 USA 的因子化尝试》2026-09-08，92 赞）**：
- 骨架：`signal = group_rank(if_else(p>0, (a-p)/p, NaN), industry)`，a=`vec_avg(aggregate_open_positions_count)`、p=`ts_delay(a,21)`。评论区简化等价式：`group_rank(ts_delta(vec_avg(字段),21), industry)`。
- 实测刻度：初版「新职位占比」margin 仅 2.96bp；改 21 日相对变化+收入条件→S 1.57；**公式不动只把 INDUSTRY 换 SLOW → S 2.40 / F 1.41 过 Ladder**（GrdogzX3）；**删掉收入条件反而更好**（单信号合规也满足）。
- 关键细节：VECTOR 用 vec_avg（同日多条报告值）；`vec_count>0` 判空；基期>0 保护除法；设置 INDUSTRY→**SLOW**、Decay 5、Trunc 0.01；**有效观察集中在 2019-2023（前段空窗，与 leading-gap 问题同型——DEU macro27 发波前必查逐年覆盖）**。
- **方向先验分层（论文+论坛并不矛盾）**：Liu (2019)《Labor-Based Asset Pricing》（SSRN 3081364）——职位空缺**水平**负向预测收益（水平族做负向：`subtract(0, ts_rank(vec_avg(字段),252))`）；论坛——招聘**变化率/加速度**正向（变化族做正向：`group_rank(ts_delta(vec_avg(字段),22), …)`）。水平与变化是两个矩，别混方向。
- 迁移到 DEU/macro27：字段换成 `num_jobs_active`/`mcr27_company_jobsactive`（水平）、`num_jobs_created/removed`（流量）；21→22 窗（白名单）；变化率自带去规模混淆（不用再 ts_rank），水平族才走 ts_rank。单塔 MACRO 合规（trio×非trio 配额已满，禁加 PV 腿）。

### sentiment27 Website Popularity Rankings（ac=324）—— ✓ 可用（2026-11-02 画像）
18 字段（15 VECTOR + 3 SYMBOL 日期元数据不可用）。Tranco 域名人气排名族：
- 主排名：`snt27_rank`（ac28，**1=最流行，语义反号**）/ `snl27_avgranking`(18) / `snl27_topranking`(18)——**水平排名型（有界），直接 rank 不需要 ts_rank**；方向先验按注意力文献（Da-Engelberg-Gao）：高人气/高注意力→短期买压后反转偏负，待实测。
- 相对人气分：`snl27_relpopularity08/1`（ac58/53）——composite 分数。
- 分布矩族：`snl27_skewness`(66) / `snl27_kurtosis`(47) / top50/top75 分位秩——**矩/分位类结构，适合做辅助腿或 bucket**。
- 计数族：`snl27_totaldomains`(35) / `snl27_totalcountrydomains`(13)——**规模混淆，须 ts_rank(·,252)**（大公司域名多）。

### earnings_sent_matrix Global Earnings Call Sentiment Matrix（ac=127）—— ✓ 可用（2026-11-02 画像）
7 个 MATRIX 字段（无 vec_*）：`positive_sentiment_probability_3`(ac76) / `negative_sentiment_probability_3`(27) / `likelihood_of_neutral_tone`(31) / `sentiment_weighting_method1/2`(38/15) / `overall_sentiment_score`(10，argmax 分类标签) / `intraday_delay_indicator`(4)。
- 概率/语气分 [0,1] **有界水平型**，直接 rank/group_rank；**财报电话=事件型（快）**：价值在事件后短窗，禁 ts_mean 拉长窗（本项目 insider 实证同型）。
- 机制：tone 超预期=管理层信心（正向）；负面语气激增=风险（负向）；可做事件门控（call 日附近 trade_when）。
- 事件型数据**逐年覆盖必查**（财报电话数据 2014 年前后可能稀疏）。

### other47 SEMrush 网站流量（ac 极低）—— ★ 下一矿脉首选（2026-11-03 02:1x 画像+取证）

**18 字段全 VECTOR（须 vec_* 包裹），两簇**：base 簇 cov 0.6516（oth47_organic_traffic/keywords/cost、paid_search_*、PLA 族、oth47_rank）+ `_enriched` 簇 cov 0.5023（同机制富化版）。**拥挤度全场最低**：alphaCount 0–6（仅 oth47_organic_traffic 47），相对 analyst7 的 5823 是真空地带。

**机制分箱（8 问初判）**：
- **需求/增长代理**：`organic_search_traffic`（自然搜索访问量）+ `organic_search_terms`（关键词广度）——公司产品需求的高频数字足迹；水平型（横截面属性，禁 ts 自归一）+ **变化型**（ts_delta 增速=需求加速度，Berkeley「数字足迹预测营收」先验）。
- **营销投入代理**：`paid_search_budget` / `paid_search_visitors` / `product_listing_ad_terms`——付费投放=获客努力；投放收缩=需求走弱（条件/事件腿）。
- **注意力/知名度**：`oth47_rank` / `website_traffic_rank`（1=更流行，语义反号同 sentiment27 陷阱）。
- **健康度比率（同机制净额合成合规）**：organic/paid 比=自然流量占比（对营销开支的依赖度）、terms/visitors=流量效率。
- `_enriched` 与 base 同机制**双份投递**：先用 base 簇（cov 高 0.15），enriched 留作稳健性对照，不混计席位。

**取证（2026-11-03）**：
1. **论文锚①「Firm Websites and the Risk of Firm」**（[NTU Scholars](https://scholars.lib.ntu.edu.tw/entities/publication/eb2d206b-8010-46f3-b474-dd861a9d036a)，4122 家美股）：网站流量高→信息不对称低→**权益成本/波动/分析师分歧全降** ⇒ 水平型方向先验：**流量高→预期收益低（负向）**。
2. **论文锚② Berkeley Haas × Stanford GSB「Digital Footprints」**（[Haas News](https://newsroom.haas.berkeley.edu/companies-website-traffic-proves-powerful-predictor-of-financial-performance-and-stock-returns)，The Accounting Review）：网站流量**变化**预测营收与股票收益 ⇒ 变化型方向先验：**流量加速→正向**。
3. **论坛**：存在对口帖《【Alpha Idea】维基百科关注度的"突压"信号(sent)在德国DEU市场的因子化尝试》（DEU 注意力突压结构）+《德国市场的"报喜藏忧"效应 0.85→1.60 全记录》（DEU 事件结构参考）——开波设计模板时读全文（跳转链为 marshaled 参数，帖 ID 待解析）。
4. **与 sentiment27 的关系**：同属「注意力」大类但载体不同（域名流量 vs 域名排名/人气）——**开波前必跑互相关防 self 撞**（QPveY7Kg 已占 sentiment 席）。

**开波前置清单**：①逐年覆盖必查（SEMrush 面板 2015-16 前可能空窗，leading-gap 口径待裁）②模板 ≥10 互异 ③两道预检 ④方向先验：水平负向 / 变化正向，先探针后定。

## 策略注记
- 低拥挤未挖集（ac<5）多为壳/小集：event_ml_signals 4 / event_relation 1 / other327 1 / other546 1 / model16 1 / other425 0——**逐个先拉字段验真再投**。
- trio 塔集（pv/model/other）占大头；非目标塔 category（analyst/news/sentiment/earnings/institutions/insiders/macro/shortinterest/risk）是单塔 alpha 的优先矿（平台重算后旧判死结论失真）。

## news 族覆盖补测（2026-11-03 get_datasets 实拉，覆盖口径参考）

| 数据集 | cov | 字段数 | ac | 备注 |
|---|---|---|---|---|
| news104 Archive News | **0.963** | 11 | 100 | 覆盖全场最高，未挖 |
| news18 Ravenpack | 0.805 | 70 | 137 | 未挖 |
| news17 PR Edition | 0.791 | 48 | 87 | GBR ACTIVE 塔腿 vec_count×similarity 机制源 |
| news20 Web Sources Sentiment | 0.773 | 46 | 33 | GBR W10 判死只限 GBR |
| news50 Web News Analytics | 0.764 | 37 | 42 | DEU 已收口（情绪机制弱，最高 0.59） |
| news38 News Analytic Model | 0.599 | 3 | 26 | 码表漂移，降级门控源 |
| sentiment7 Webpage Views | 0.742 | 3 | 94 | 注意力型，EUR 同型先验 |
| socialmedia39 Investor views | 0.275 | 1 | 137 | 低覆盖高拥挤 |

注意：coverage=0.0 的集（news3/7/21/23/29/31/52/54/73/76 等）按覆盖口径**不能直接排除**——数据集级 cov=0 可能是平台未度量，排除前仍须逐年 longCount 核验（连续多年空窗才判死）。

