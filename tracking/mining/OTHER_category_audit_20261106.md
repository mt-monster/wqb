# OTHER category 全景审计（EUR 36 个 + USA 56 个数据集）· 2026-11-06

> 本文件原为 `tracking/EUR/eur_other_other455_competitor_net_20261106.md`，因内容已扩展到跨区 OTHER 面而重命名。

> 起因：用户两次追问「判死用的模板是不是不充分」「不考虑 PPA，只考虑 REGULAR/ATOM，查论坛或外部论文，看这个 category 下还有哪些模板没测过」。
> 本文件同时回答两件事：① OTHER category 的模板覆盖表（已测 / 未测 / 出处）；② 唯一未测数据集 other455 的画像与首波派发。

## 一、other571 结案（4/4 全灭）

| alpha | 模板 | S | TO | 2Y | failed |
|---|---|---:|---:|---:|---:|
| `d5W9xbn2` | R03 关注度水平 | 0.02 | — | −0.03 | — |
| `E56mwpq0` | R04 渠道分歧 | 0.00 | — | 0.85 | — |
| `Xg9NpVGx` | R02 异常关注度 views7d/views84d | **−0.27** | 77.53% | −0.53 | 5 |
| `2rAG7908` | R05 零售 vs 机构 7dmobile/7ddesktop | −0.01 | 57.07% | 0.26 | 4 |

4 个结构互异骨架最强 |S| = 0.27，全部 REJECT。**other571 封盘**（命中例外判据：骨架最强 S<1.5）。
机制侧另一条硬伤：字段描述原文标明 **14 天滞后**（over the trailing 14-day window ending 14 days ago），注意力溢价本身是 1-2 周半衰期现象，滞后 14 天正好把信号窗口吃掉。

## 二、other455 字段画像

- 平台 `platform_count = 1500`，但 **`offset` 参数被平台忽略**：offset 0/200/400/…/1400 全部返回同一批前 200 字段（`pagination_truncated: true`、`truncated_reason: max_fields_cap`）。以下结论只针对**可见并可预校验的那 200 个**。
- 类型：**GROUP 161 / MATRIX 39**（前 200 中）。cov 0.9705。aC 极低（多数 0–4）⇒ 机制几乎无人开采。
- 命名网格：`oth455_competitor_n2v_p{10|50}_q{50|200}_w{1..5}_{kmeans|pca_fact1..3}_cluster_{5|10|20}`
  - `_cluster_{5|10|20}` = GROUP（簇标签，5/10/20 三档粒度）
  - `_value` = MATRIX（仅 `pca_fact1..3` 有，连续潜轴坐标）
- 语义：node2vec（p = return parameter、q = in-out parameter、w = 嵌入窗口版本）在**竞品关系图**上学出每只股票的潜在向量 → KMeans 得簇标签、PCA 得 3 个主成分坐标。D1 滞后。
- **关键性质**：PCA 轴的方向与旋转是任意的 ⇒ **符号必须实测**，不能按字段名推方向（与既有「符号一律按实测」纪律一致）。

## 三、OTHER category 模板覆盖表

「已测」= 本 campaign 在 EUR/OTHER（techindi_model / news_sentiment_dl / news_sentiment_nlp / ai_news_scores / other571）实盘跑过的结构。

| # | 模板族 | 结构 | 已测? | 出处 / 备注 |
|---|---|---|---|---|
| 1 | 水平 level | `rank(x)` | ✅ techindi 硬标签、ai_news A1、other571 R03 | 基线 |
| 2 | 上下侧累积 | `rank((P4+P3)-(P1+P0))` | ✅ techindi T02 | 本 campaign 最强 S3.53 |
| 3 | 尾部净上行 | `rank(P4-P0)` | ✅ techindi T01 | |
| 4 | 相对信心比 | 概率/频数比 | ✅ techindi T03 | |
| 5 | 稳定性加权 IR | 方向/自身波动 | ✅ techindi T08 | |
| 6 | 对数概率 | `rank(log(1+p))` | ✅ techindi T09 | |
| 7 | 两极分化度（二阶非方向） | `rank(P4+P0)` | ✅ techindi T04 | S 掉到 0.55 |
| 8 | 区间宽度（分歧度） | `upper-lower` | ✅ ai_news A2 | |
| 9 | 区间内位置 | `(avg-lower)/(upper-lower)` | ✅ ai_news A3 | |
| 10 | 跨版本分歧 | `x_2 - x_5` | ✅ ai_news A4 | 全零：跨版本为常数 |
| 11 | 短长窗比（异常度） | `views7d/views84d` | ✅ other571 R02 | |
| 12 | 渠道/来源分歧 | mobile/desktop、跨源分歧 | ✅ other571 R05 / news_dl W03/W04 | |
| 13 | 行业内相对 | `group_rank(x, industry)` | ✅ techindi 变体5 | sub/S 最差 0.4701 |
| 14 | **自定义网络簇分组** | `group_rank(x, GROUP簇字段)` / `group_neutralize` | ❌ **未测** | BigQuant QIML：用 Node2Vec 新闻共现簇替代 GICS 行业分类构建动态分类体系 |
| 15 | **潜空间位移（一阶差分）** | `ts_delta(value,63)` / `ts_zscore(value,504)` | ❌ **未测** | 嵌入坐标漂移 = 竞争结构迁移速度；本轮首次派发 |
| 16 | **跨潜轴分歧** | `rank(fact1)-rank(fact2)` | ❌ **未测** | 两个主成分轴上的相对位置差；本轮首次派发 |
| 17 | **跨窗/模型版本分歧** | `rank(w1)-rank(w5)` | ❌ 未测 | 嵌入版本间分歧 = 模型不确定性代理 |
| 18 | **簇跳变事件化** | `ts_delta(cluster,252)` 非零 | ❌ 未测 | 纯事件型，与所有 value 类构造正交；GROUP 的第二种用法 |
| 19 | **簇稳定性** | `ts_std_dev(cluster,252)` | ❌ 未测 | 网络重组频率 |
| 20 | **对价量正交化（残差化）** | `group_rank(x,簇)-rank(momentum)` | ❌ 未测 | 全 campaign 从未对 alt-data 做 momentum/vol 残差化 |
| 21 | **时序粘性/自相关** | 信号符号的 ts_mean、自相关 | ❌ 未测 | 持续性作为独立维度 |
| 22 | **注意力×情绪交互** | other571 views × ai_news sentiment | ❌ 未测 | 两者同属 OTHER ⇒ 单塔合规；但两者单独判弱，优先级低 |
| 23 | 条件化门控 | `if_else(状态, sign+, sign-)` | ✅ 部分 | 本 campaign 反复证明门控 + 长窗不可叠加 |
| 24 | 非线性 signed_power / log1p | — | ✅ | 实证：指数只移动 prod↔sub 前沿，不破墙 |

**结论**：OTHER category 真正**结构上没测过**的是 #14–#21 这 8 族。其中 #14（用网络簇替代行业做分组轴）、#18/#19（GROUP 标签本身当信号）是 other455 独有的能力，无法在别的数据集上复现。

**外部检索来源**（web_search 实检索）：
- A Robust Cross-Sectional Attention Premium: Evidence from Wikipedia Pageviews in the Russell 1000 Universe —— 注意力溢价的截面存在性（但 other571 因 14 天滞后 + 4 骨架全灭已封盘）。
- The Wikipedia effect: Analyzing investor attention for strategic investment decisions（Economics Letters, Pyun Chaehyun）—— 同上。
- Learning Embedded Representation of the Stock Correlation Matrix using Graph Machine Learning（arXiv q-fin.CP）—— 图嵌入表征股票相关矩阵的标准做法，对应 other455 的 node2vec → PCA 流程。
- QIML Insight：基于多源特征及机器学习的股票聚类模型（BigQuant）—— **直接用 Node2Vec 新闻共现簇替代 GICS 行业分类**，是 #14「网络簇当分组轴」的直接方法论依据。
- Stock Ranking Prediction Using List-Wise Approach and Node Embedding Technique（IEEE）—— 节点嵌入用于排序预测。

论坛侧：本轮 `search_forum_posts` 因账号级 compute 预算被占未取到新帖，不伪称已取。前序轮次已取的三条（软信息优于硬信息 / 概率提供方向、概率稳定性决定权重 / 概率类字段需分位平滑化）仍是 OTHER 概率族的主依据。

## 四、本轮派发（other455 首波，2 批 4 条）

设置：EUR / TOPCS1600 / D1 / decay 8 / SUBINDUSTRY / trunc 0.08 / VERIFY / nan ON / pasteurization ON / maxTrade OFF。
预检：`valid:true`、`unknown_fields:[]`、`unknown_soft:[]`，字段名逐字命中 catalog（fields_checked 3 个）。

| 批 | mid | 模板 | 表达式 | 算子 |
|---|---|---|---|---|
| A | `4kbbYv5wY5hJbB9KaipLC4B` | #1 水平基线 | `rank(oth455_competitor_n2v_p10_q200_w1_pca_fact1_value)` | 2 |
| A | 同上 | #15 潜空间位移 | `rank(ts_delta(<同字段>,63))` | 3 |
| B | `tEn8V8Qq5ju9sDXa9eGOKd` | #14 网络簇内相对 | `group_rank(<同字段>, oth455_competitor_n2v_p10_q200_w1_kmeans_cluster_10)` | 2 |
| B | 同上 | #16 跨潜轴分歧 | `subtract(rank(fact1),rank(fact2))` | 3 |

设计逻辑：A 批回答「PCA 潜轴有没有任何截面信号」（#1）与「潜轴在动还是静止」（#15）；B 批直接测本次唯一全新结构杠杆 #14（网络簇替代行业），并用 #16 检验三根潜轴是否携带互异信息。4 条分属 4 个结构，杜绝同骨架刷参。

## 五、未派发模板的后续队列

1. #17 跨窗分歧（w1 - w5，两个嵌入版本）；
2. #18 簇跳变事件化（`ts_delta(kmeans_cluster_10,252)`，含 20 簇细粒度版）；
3. #19 簇稳定性（`ts_std_dev(cluster_20,252)`）；
4. #20 对 momentum 残差化；
5. #21 信号粘性；
6. 粒度轴：cluster_5 vs 10 vs 20、q50 vs q200、p10 vs p50 —— 仅当 #14 出正 S 后启用。

## 六、退出条件

- 若 #1/#15 的 |S| 均 < 0.5 且 #14 未显著超过 #1，则 other455 判为无信号集，与 other571 一同结案，EUR/OTHER 停在 2/3。
- 若 #14 明显优于 #1（簇内相对 > 全样本相对），则「竞品网络簇」这个分组轴本身有价值，按第五节粒度轴铺开。
## 七、★重大纠错：EUR/OTHER 实际有 36 个数据集，此前只覆盖了 7 个

`get_datasets(region=EUR, universe=TOPCS1600, delay=1)` 返回 **173 个数据集**，其中 `category=OTHER` 有 **36 个**。此前基于本地缓存 `tracking/mining/field_coverage_EUR_d1_TOP1200.json` 只列了 7 个 —— **缓存不完整，导致「EUR/OTHER 面已基本穷尽」的判断是错的**。

36 个 OTHER 数据集全表（fields / alphaCount / coverage / users）：

| 数据集 | 名称 | 字段 | aC | cov | 状态 |
|---|---|---:|---:|---:|---|
| techindi_model | DL Technical Indicator Returns | 798 | 2453 | 0.9999 | 封盘（11 变体 prod 0.7276–0.8562） |
| **other567** | **Employee Review Data** | **224** | **84** | **0.4665** | **本轮开波（§九）** |
| other455 | Relationship enhanced with AI/ML | 1500 | 301 | 0.9599 | 本轮 4 骨架已测（§八） |
| other571 | Wikipedia Viewing Data | 30 | 61 | 0.7585 | 封盘（4/4 全灭） |
| news_sentiment_dl | DL News Sentiment Signals | 66 | 2 | 0.7558 | 封盘 |
| news_sentiment_nlp | News Sentiment Signal Features | 23 | 7 | 0.9134 | 连带封盘 |
| ai_news_scores | AI News Sentiment Scores | 105 | 13 | 0.7924 | 封盘 |
| search_interest | Rapid Search Interest Signals | 5 | 8 | 0.7815 | 弃（字段太少） |
| **other545** | **Linked Firms Momentum Data** | **4** | **14** | **0.5424** | **未测·高优先（Cohen-Frazzini 经济关联动量）** |
| **other315** | **Equity Swap Data** | 32 | 109 | 0.5191 | 未测 |
| **other546** | **Institutional Network Analysis** | 13 | 13 | 0.3810 | 未测 |
| **other699** | **Individual Investor Transactions** | 7 | 246 | 0.2732 | 未测（散户流，cov 偏低） |
| **acquisition_model** | **Corporate Acquisition Likelihood** | 15 | 14 | 0.7484 | 未测·高优先（并购概率，cov 最好） |
| **other128** | Global Executive Performance Factors | 18 | 20 | 0.4607 | 未测 |
| **event_sentiment_signals** | Corporate Event Sentiment Signals | 26 | 23 | 0.3567 | 未测 |
| **other250** | details data | 12 | 22 | 0.4899 | 未测 |
| **other296** | Corporate Earnings Call Sentiment | 19 | 56 | 0.5649 | 未测 |
| **other635** | Thomson Reuters News Analytics | 6 | 15 | 0.6216 | 未测 |
| **other384** | NLP on conference conversation | 66 | 42 | 0.2803 | 未测（cov 低） |
| **stock_cluster_dl** | DL Stock Clusters | 5 | 1 | 0.4563 | 未测（与 other455 同源机制） |
| **stock_search_trends** | US Stock Search Trend Matrix | 6 | 2 | 0.5401 | 未测 |
| **equity_forum_data** | International Equity Forum Activity | 8 | 0 | 0.4060 | 未测（aC=0 全新鲜） |
| **event_relation** | Text-Based Event Relationship | 12 | 3 | 0.5769 | 未测 |
| **workforce_flow_skills** | Workforce Flow and Skills | 33 | 0 | 0.2456 | 未测（aC=0 但 cov 低） |
| insider_feats / insider_matrix / insider_trx_matrix | 内部人三套 | 118/33/33 | 56/86/44 | 0.54/0.61/0.61 | 未测（与 INSIDERS 塔可能重叠） |
| earningscall_sentiment | Multi Aspect Earnings Call Sentiment | 167 | **4803** | 0.5061 | 饱和（aC 4803） |
| euro_equity_imbalance | European Equity Trading Imbalance | 31 | 142 | 0.3089 | cov 低 |
| order_book_imbalance | Order Book Imbalance | 256 | 2 | 0.2122 | cov 极低 |
| equity_conc_metrics | Equity Market Concentration | 18 | 1 | 0.1965 | cov 极低 |
| dl_riskfree_returns | DL Risk Free Returns | 133 | 187 | 0.9429 | 非 alpha（利率腿） |
| other327 / other424 / other436 | 利率敏感 / 两套股息模型 | 3/3/3 | 28/176/72 | 0.52/0.69/0.45 | 字段太少 |

**纠错结论**：EUR/OTHER 的可用面不是 7 个数据集而是 36 个，扣除已判死 5 个、饱和/非 alpha/字段过少 6 个，**仍有约 20 个从未测过**。「穷尽所有 category」这条 Goal 要求远未达成。
下一步优先序：`other567`（本轮已开波）→ `acquisition_model`（cov 0.7484，15f）→ `other545`（经济关联动量）→ `other315` / `other546` / `other128` / `event_sentiment_signals` / `other250` / `other296`。

**方法论沉淀**：本地 `field_coverage_*.json` 缓存只覆盖「曾查询过」的数据集，**不能作为「该 category 有几个数据集」的判据**。任何「本面已穷尽」的结论，必须先跑一次 `get_datasets` 取平台全表再比对。此条应回写进开波 SOP。

## 八、other455 四骨架实测（首波结果）

| alpha | 模板 | S | TO | 2Y | sub | fail |
|---|---|---:|---:|---:|---:|---:|
| `MPYgQ9v8` | #1 水平基线 `rank(value)` | −0.32 | 0.80% | −1.61 | −0.38 | 6 |
| **`wpQNlX7l`** | **#15 潜空间位移 `rank(ts_delta(v,63))`** | **+0.57** | 1.36% | **1.82** | 0.42 | 3 |
| `E56mE7A1` | #14 网络簇内相对 `group_rank(v,cluster_10)` | −0.44 | 3.39% | −0.88 | −0.92 | 5 |
| `1YNGd956` | #16 跨潜轴分歧 `rank(f1)−rank(f2)` | −0.23 | 0.79% | −1.26 | −0.21 | 6 |

读法：
- 唯一正向的是 **#15 潜空间位移**（S 0.57 / 2Y 1.82）：嵌入坐标的变化率比坐标水平更有信息，方向符合「网络位置迁移」直觉，但量级 0.57 离 1.58 差 1.0。
- **#14 网络簇分组比全样本更差**（−0.44 vs −0.32）⇒「竞品网络簇」没有比行业分类提供额外截面结构。这是本轮最想验证的新杠杆，结果否定。
- 换手 0.8–3.4%（极低）：信号是慢变量，不存在换手闸问题，纯粹是信号太弱。
- 剩余 2 个未测骨架（#18 簇跳变事件化 / #19 簇稳定性）留作判死的第 5、6 个结构，仅在需严格判死时补测。

## 九、other567（Employee Review Data）画像与派发

- **224 字段全 VECTOR**，cov 主评分族 **0.5277**、标识族 0.625、`delta` 族 0.3433。aC 极低（avg_overall / avg_pay / avg_senior_mgmt 均 0）。
- 四个子族：① 无前缀 `avg_*_score`（10 维度：overall / culture / career / CEO / D&I / pay / recommend / senior mgmt / work-life / business outlook）+ 13 个 `*_sentiment_score` 文本情绪 + `*_rating`；② `oth567_individual*` 逐条评论级；③ `oth567_trend*` 趋势级；④ `oth567_delta*` 变化级（同时含招聘岗位增量 `deltajob_category` / `deltaatlas_month`）。
- **VECTOR 必须包 `vec_avg`**（裸用报 does not support event inputs，本 campaign 已验证）。
- 机制出处（web_search 实检索，标题+期刊确认）：
  - Green, Huang, Wen, Zhou (2019) **Crowdsourced employer reviews and stock returns**, *Journal of Financial Economics* vol.134 —— 众包雇员评论评分正向预测截面收益，直接对应本数据集原始字段。
  - Edmans (2011) **Does the stock market fully value intangibles? Employee satisfaction and equity prices**, JFE —— 市场对这类无形资产定价不足。
- 派发（EUR / TOPCS1600 / D1 / decay 8 / SUBINDUSTRY / trunc 0.08 / VERIFY / nan ON / pasteurization ON / maxTrade OFF；预检三项全空、5 个字段逐字命中）：

| 批 | mid | 模板 | 表达式 |
|---|---|---|---|
| E | `2MKtv87T958XbkNDDoAOVHz` | 满意度水平 | `rank(vec_avg(avg_overall_company_score))` |
| E | 同上 | 满意度变化 | `rank(ts_delta(vec_avg(avg_overall_company_score), 63))` |
| F | `3MszTqXa53Tazh79us2JAW` | 文化-薪酬错配 | `subtract(rank(vec_avg(avg_culture_values_score)), rank(vec_avg(avg_pay_and_benefits_score)))` |
| F | 同上 | 文本与评分背离 | `subtract(rank(vec_avg(workplace_culture_sentiment)), rank(vec_avg(culture_values_rating)))` |

后队列（other567 第 2 波，凑满 ≥10 模板）：recommend−overall 缺口、CEO 认可相对整体、trend 族 vs avg 族分歧、helpful/unhelpful 比、`employment_duration_years` 任期、`remote_work` 结构分、`oth567_delta*` 招聘岗位增量（labor demand nowcasting）、前员工 vs 在职员工评分差、多维度内部离散度、评分加速度（二阶差分）。
### E 批实测（other567）

| alpha | 模板 | S | TO | 2Y | sub | fail |
|---|---|---:|---:|---:|---:|---:|
| `MPYgQb2n` | 满意度水平 `rank(vec_avg(avg_overall_company_score))` | −0.26 | 9.29% | 0.63 | −0.12 | 5 |
| `bl6xqNgZ` | 满意度变化 `rank(ts_delta(...,63))` | 0.46 | 0.69% | −0.69 | 0.69 | 6 |

两条 |S| ≤ 0.46。F 批（文化-薪酬错配 / 文本与评分背离）仍在飞。初步读法：雇员满意度**水平**在 EUR 无截面预测力（marginal S −0.26），变化量 0.46 也不足；cov 0.5277 意味着近一半股票没有评论覆盖，这是先验短板。

## 十、acquisition_model（并购概率模型）画像与派发

- **15 字段全 VECTOR，cov 0.7484**（本面已测数据集中覆盖最好），aC ≤ 6，全部是 1–100 的百分位秩。
- 两类信息：① **目标概率**，五个同行集版本 `{global|region|industry|sector|country}_percentile_acquisition_likelihood`；② **模型分量**，五个维度 × 两个范围 `{global|region}_{company_size|credit_quality|fundamental_factor|text_factor|valuation}_percentile_rank`。
- 经济机制：并购目标概率 → 被收购溢价预期。学术脉络：Palepu (1986) 的 takeover target 预测模型是该族鼻祖；近年 ML 版直接输出 target likelihood。分量里 **text_factor** 是新闻/文本驱动的"并购传闻强度"，与其余四个基本面分量在信息源上完全正交。
- 模板库（≥10，结构互异）：
  1. 目标概率水平（global 版）—— 基线；
  2. 文本因子单独（text only）—— 纯传闻强度；
  3. 估值因子单独（valuation only）—— 便宜才有吸引力；
  4. **同行相对超额**（sector 版 − global 版）—— 去掉全市场共同成分后剩"本行业特有的被收购体质"；
  5. **文本 vs 基本面背离**（text − fundamental）—— 有传闻但基本面不支撑；
  6. 五个同行集百分位的**离散度**（横跨 country/industry/region/sector/global 的一致性）—— 一致性高 = 无歧义目标；
  7. **概率变化**（`ts_delta` 126）—— 概率上修；
  8. **信用质量调节**（credit_quality 与概率的交互）—— 高杠杆/低信用更容易成为目标；
  9. **规模 × 概率交互**（小市值 + 高概率 = 经典 LBO 标的）；
  10. **估值-基本面双低组合**（value trap 型目标）；
  11. 概率的**时序 z 分数**（相对自身两年位置）；
  12. **概率与自身波动之比**（IR 化）。
- 本轮派发（EUR / TOPCS1600 / D1 / decay 8 / SUBINDUSTRY / trunc 0.08 / VERIFY / nan ON / pasteurization ON / maxTrade OFF；预检三项全空、4 字段逐字命中）：

| 批 | mid | 模板 | 表达式 |
|---|---|---|---|
| G | `4jC5esggD5dVa4l1uVcCaQr` | #1 目标概率水平 | `rank(vec_avg(global_percentile_acquisition_likelihood))` |
| G | 同上 | #2 文本因子单独 | `rank(vec_avg(global_text_factor_percentile_rank))` |
| H | `1V7NLqaQU5g0avzr8Ddzg3q` | #4 同行相对超额 | `subtract(rank(vec_avg(sector_percentile_acquisition_likelihood)), rank(vec_avg(global_percentile_acquisition_likelihood)))` |
| H | 同上 | #5 文本 vs 基本面背离 | `subtract(rank(vec_avg(global_text_factor_percentile_rank)), rank(vec_avg(global_fundamental_factor_percentile_rank)))` |
## 十一、EUR/OTHER 本轮全部结果与判决

### other567 F 批 + acquisition_model G/H 批实测

| alpha | 数据集 | 模板 | S | TO | 2Y | sub | fail |
|---|---|---|---:|---:|---:|---:|---:|
| `KPJV9Nll` | other567 | 文化−薪酬错配 | 0.40 | 9.29% | 0.95 | 0.26 | 5 |
| `WjOYGb1Q` | other567 | 文本 − 评分背离 | 0.08 | **146.65%** | 1.02 | −0.26 | 7 |
| `N1NKrQlp` | acquisition_model | 目标概率水平 | **−0.76** | 1.95% | −0.85 | −0.48 | 5 |
| `qML5lWJO` | acquisition_model | 文本因子单独 | −0.60 | 3.37% | −0.53 | −0.36 | 5 |
| `mLoKbmOX` | acquisition_model | 同行相对超额（sector−global） | −0.02 | 3.74% | −0.29 | 0.09 | 4 |
| `RRE58bXb` | acquisition_model | 文本 vs 基本面背离 | 0.24 | 3.04% | 0.35 | 0.27 | 4 |

读法：
- **acquisition_model 是本轮最强信号源**：目标概率水平 S −0.76 / 2Y −0.85，方向一致（反向：高并购概率 → 跑输），且换手仅 1.95%。但 |S| 0.76 离 1.58 差一倍，且反向的 `−likelihood` 本质上是「大市值+高质量」暴露，prod 相关性风险高。
- **同行相对超额（sector−global）≈ 0**（−0.02）⇒ 该信号的截面信息**全部来自全球水平成分**，peer 相对化不增加信息。这是很有价值的负结果：说明它不是「行业内的被收购体质」，而是「整体便宜/绩差」。
- 文本因子单独 −0.60，与「文本 vs 基本面背离」+0.24 方向相反 ⇒ 文本因子更像「绩差代理」而非独立传闻信号。
- **other567 全面偏弱**：4 个结构（水平 −0.26 / 变化 0.46 / 文化-薪酬错配 0.40 / 文本-评分背离 0.08），最强 |S| 0.46。文本-评分背离的换手 **146.65%** 是致命伤（VECTOR 文本情绪逐日全推倒）。

### EUR/OTHER 累计判决表（本轮结束状态）

| 数据集 | 骨架数 | 最强 \|S\| | 判决 |
|---|---:|---:|---|
| techindi_model | 11 | 3.53 | **封盘**（prod 0.7276–0.8562 窄带） |
| news_sentiment_dl | 4 | 0.28 | **封盘**（+TO 160–175%） |
| news_sentiment_nlp | — | — | 连带封盘 |
| ai_news_scores | 4 | 0.33 | **封盘**（+TO 140–151%） |
| other571 | 4 | 0.27 | **封盘** |
| other455 | 4 | 0.57 | 弱·暂停（余 #18/#19 两骨架未测） |
| other567 | 4 | 0.46 | 弱·暂停 |
| acquisition_model | 4 | 0.76 | 弱·暂停（唯一有经济意义方向） |
| 其余 20 个（other545/other315/other546/other128/event_sentiment_signals/other250/other296/other635/equity_forum_data/stock_search_trends/stock_cluster_dl/workforce_flow_skills…） | 0 | — | **未测** |

**决策：EUR/OTHER 停止深度挖掘，转广度扫描。** 理由：本面已测的 7 个数据集里 5 个彻底判死、3 个最强 |S| ≤ 0.76；单数据集平均要花 4–11 个骨架才能确认弱，而本面还有 20 个数据集从未碰过。**广度扫描的期望产出高于继续在弱数据集上加骨架**。

## 十二、转 USA/OTHER 广度扫描（塔位 2/3，只差 1 颗）

USA 平台实取 **286 个数据集，OTHER 类 56 个**（此前只测过 4 个）。设 TOP2000/D1/decay 0/STATISTICAL/trunc 0.08/VERIFY/nan ON/pasteurization ON/maxTrade OFF。

### 首个目标：other699（TipRanks 个人投资者交易，19 字段全 VECTOR，cov 0.9855）

- 字段：`oth699_sharestraded`（带符号股数，正买负卖）、`oth699_newnumofshares` / `prevnumofshares`（交易前后持股）、`oth699_priordistincttradingdays` / `priortransactionnumber`（交易者经验）、`oth699_usertype_24`（Basic/Premium/Ultimate 订阅档 = 散户内部的信息层级）、`oth699_action_14`（加自选 / 开仓 / 等 6 类动作）、标识族（country / platform / splitfactor / 时间戳）。
- 机制出处：Barber & Odean 的散户劣势系列 + Boehmer/Jones/Zhang 的 retail order imbalance（散户净买入在短周期反向预测收益）+ Kelley & Tetlock (2013) 关于众包意见的「群体智慧 vs 羊群」。
- 派发（预检三项全空、3 字段逐字命中）：

| 批 | mid | 模板 | 表达式 |
|---|---|---|---|
| I | `16ngFt68Q4v59xg9qaLqWLE` | 散户净买入水平 | `rank(vec_avg(oth699_sharestraded))` |
| I | 同上 | 异常散户买入（相对自身两年） | `rank(ts_zscore(vec_avg(oth699_sharestraded), 252))` |
| J | `48SjRT1IB4Coc0rijcBrRgG` | 仓位归一化净买入 | `rank(divide(vec_avg(oth699_sharestraded), vec_avg(oth699_newnumofshares)))` |
| J | 同上 | 交易者活跃度（关注度代理） | `rank(vec_avg(oth699_priordistincttradingdays))` |

后续队列（other699 第 2 波）：`newnumofshares − prevnumofshares`（仓位增量）、`usertype` 档位加权（Premium 用户的方向是否更聪明）、加自选 vs 实际开仓的分歧、`priortransactionnumber` 分组的散户老手方向、按 country/platform 分组的地域散户差异。

### USA/OTHER 其他未测高覆盖候选（排队）

`other596`(420f, aC347, cov0.9796) ｜ `other580`(403f, aC219, cov0.9119) ｜ `nlp_news_scores`(84f, aC68, cov0.9017) ｜ `us_equity_news`(8f, aC171, cov0.9627) ｜ `other623`(6f, aC38, cov0.9866) ｜ `forum_sentiment`(13f, aC51, cov1.0) ｜ `other546`(13f, aC50, cov0.663) ｜ `other359`(10f, aC87, cov0.7419) ｜ `filing_sentiment`(21f, aC51, cov0.5396) ｜ `earningscall_embed`(515f, aC182, cov0.7596)。
### other699 首波结果（I/J 批，decay 0）

| alpha | 模板 | S | TO | 2Y | sub | fail |
|---|---|---:|---:|---:|---:|---:|
| **`xArlkWqw`** | 散户净买入水平 `rank(vec_avg(sharestraded))` | **1.02** | **138.64%** | 1.11 | 0.63 | 5 |
| `LLM81rW1` | 异常散户买入 `rank(ts_zscore(vec_avg(sharestraded),252))` | 0.57 | 101.95% | 1.29 | 0.31 | 5 |
| `VkxMPeqA` | 仓位归一化 `rank(divide(vec_avg(sharestraded), vec_avg(newnumofshares)))` | 0.68 | 145.68% | 0.69 | 0.68 | 5 |
| `MPYgQVX9` | 交易者活跃度 `rank(vec_avg(priordistincttradingdays))` | −0.13 | 135.65% | 1.14 | −0.35 | 6 |

读法：
- **这是本 campaign 在 OTHER category 上第一个 S>1.0 的新信号**（techni_model 之外）。散户净买入方向为正（S 1.02），与 Barber-Odean 的「散户买入后跑输」**符号相反** —— 按「符号一律按实测」纪律照实记录，不按论文先验翻号。
- 四个骨架 S 单调：1.02（水平）> 0.68（仓位归一）> 0.57（异常 z）> −0.13（交易者活跃度）⇒ 信息集中在**净买入的方向/规模**，不在交易者属性。
- **换手 100–146% 是本批唯一致命项**（HIGH_TURNOVER），decay 0 是主因。S 1.02 虽未达 1.58，但比 EUR/OTHER 除 techindi 外所有数据集都强。

### other699 第二波（decay 8 平滑族）

设置改为 USA / TOP2000 / D1 / **decay 8** / STATISTICAL / trunc 0.08（单一杠杆：用 decay 平滑换手；模板同步换成平滑族）。

| 批 | mid | 模板 | 表达式 |
|---|---|---|---|
| K | `3bbwo87x24K5bWRR60ATE3n` | 平滑散户流（22 日） | `rank(ts_mean(vec_avg(oth699_sharestraded), 22))` |
| K | 同上 | 向量信息比（单位无关） | `rank(divide(vec_avg(oth699_sharestraded), vec_stddev(oth699_sharestraded)))` |

若 K 批能把换手压到 70% 以下且 S 保持 ≥1.2，则按「平滑 + 分组中性化 + 长窗」三轮推进到 1.58；若 S 随平滑大幅衰减，则说明散户流是短周期反转信号，长平滑无解，需要换「事件密度」（`priortransactionnumber` 分桶）而非时间平滑。

### 同批探查的两个 USA/OTHER 机制（未派发）

- **`other580`（ETF 持仓变动，403f / aC219 / cov 0.91–1.0）**：字段如 `change_average`（20 日 ETF 持股绝对变动的等权均值）、`change_count`（参与变动的 ETF 数量 = 广度）、`change_skewness`、`change_log`/`change_sqrt`/`change_squared`（非线性变换已是**独立字段**，用它们不花算子）、`average_predicted_holding_change_20d`（**预测值**）。机制是 ETF 申赎/再平衡引发的价格压力，与新闻情绪完全正交，是 next 优先目标。
- **`other596`（新闻情绪多期限 + 置信区间，420f / aC347 / cov 0.9795–1.0）**：`oth596_{2|3|4}{pos|neg|neut}_conf_low/conf_up` + `_dts`（标准差）。结构与已判死的 `ai_news_scores`（区间宽度 / 区间内位置都试过，|S|≤0.33、换手 140–151%）高度同源，**优先级放低**。
## 十三、other699 换手弹性实测（Y/Z 批）与两条新收批

### other699 同一模板 × decay 三档（唯一杠杆 = decay）

| decay | alpha | S | TO | 2Y | sub | fail |
|---:|---|---:|---:|---:|---:|---:|
| 0 | `xArlkWqw` | 1.02 | 138.64% | 1.11 | 0.63 | 5 |
| 2 | `gJer9mbe` | 1.02 | 123.04% | 0.98 | 0.53 | 6 |
| 4 | `YP1lgnzv` | 1.01 | 112.49% | 0.60 | 0.46 | 6 |
| 8（+22d 均值） | `GrWQeqn0` | −0.52 | 12.61% | 0.11 | −0.50 | 4 |

**decay 对散户流几乎无效**：0→2→4 只把换手从 138.6% 压到 112.5%（−26 点），S 纹丝不动（1.02/1.02/1.01）。一旦上时序平滑（`ts_mean` 5 日 → S 0.16 / TO 44.7%；`ts_decay_linear` 10 → S −0.01 / TO 71.2%；`ts_mean` 22 + decay 8 → S −0.52），**信号立刻归零**。
⇒ 结论：散户净买入是**日频短周期信号**，本数据集内没有任何设置在「换手 ≤70%」约束下还能保住 S。它与换手闸结构性冲突，**other699 判为不可提交**（虽然它是本面唯一 S>1.0 的新信号）。

### 同一波收批：窗口谷 `buy_sell_ratio` 族（EUR/TOP2500/decay8/SLOW_AND_FAST）

| alpha | 模板 | S | F | TO | 2Y | sub | sub/S | 闸 |
|---|---|---:|---:|---:|---:|---:|---:|---:|
| **`A1VLR6Yd`** | `group_neutralize(rank(ts_backfill(buy_sell_ratio_top20_60d_filled,250)),industry)` | **2.09** | **1.12** | **4.61%** | **2.05** | **1.39** | 0.665 | **0（全过）** |
| `j2YV5LW5` | 同上但 `top5_20d` | 1.54 | 0.81 | 7.85% | 1.92 | 0.40 | 0.260 | 3 |

- `A1VLR6Yd`：**ra.failed_ra_checks 为空、checks.fail 为空**，塔 `EUR/D1/OTHER`（multiplier 1.5），4 算子。这是 EUR/OTHER 的**第 3 颗可提交件 —— 一交即点亮该塔**。
- `j2YV5LW5` 三条不过：LOW_SHARPE 1.54<1.58、LOW_FITNESS 0.81<1、LOW_SUB_UNIVERSE_SHARPE 0.40<0.80。注意 limit 0.80 ≈ 0.5303×1.54=0.817，**再次印证 sub 闸是比值而非固定阈值**。
- 归因：同一族字段，窗口从 `top5_20d` 换到 `top20_60d`，S 1.54→2.09、sub 0.40→1.39 —— **换窗口是这一族唯一有效的杠杆**，与「窗口谷」方法论一致。
- 未知项：平台 by-alpha API 只返回 id/code/type/status/stage/settings/metrics/ra/checks/pyramids，**不返回 dataset 归属**；`buy_sell_ratio_*_filled` 不在 `euro_equity_imbalance`（31 字段已核）里，具体 dataset id 本轮未定位。

### EUR/SOCIALMEDIA 快几何判死

| alpha | 表达式 | S | 闸 |
|---|---|---:|---:|
| `P0o5kO6q` | `ts_decay_linear(group_rank(ts_mean(ts_backfill(scl12_sentiment,22),5),industry),10)` | −0.26 | 4 |
| `leAao32l` | `-group_rank(ts_zscore(ts_backfill(scl12_buzz,22),252),industry)` | 0.26 | 3 |

EUR/TOP2500/INDUSTRY/trunc 0.01，塔 `EUR/D1/SOCIALMEDIA`（multiplier 1.2）。情绪水平与 buzz 反转两个快几何骨架天花板 |S| 0.26 ⇒ `scl12` 快几何判死。

