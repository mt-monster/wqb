# USA 区域数据集扫描 + 字段画像（S0/S1）

> 日期：2026-10-14　战役：`tracking/USA/campaign_20261014/`
> 方法：`score_datasets.py --campaign-dir tracking/USA --stage all`（S0 唯一权威，禁手写 filter）
> 字段：`get_datafields` 平台实时值（禁本地表；类型 MATRIX/VECTOR 以平台 `type` 字段为准）

## 0. 点塔现状（`get_pyramid_alphas`，本季度）

USA/D1：**model=4、analyst=1、earnings=1**，其余 13 塔全 0。
USA/D0：全 0（USA 走 D1）。

⇒ **可挖塔 = 未点亮塔**，且优先选 `pyramidMultiplier` 高者。

| 塔 | 本季 | multiplier | 本轮是否投 |
|---|---:|---:|---|
| model | 4（已点亮） | 1.0 | ✗ 已点亮，排除 |
| analyst | 1（已点亮） | 1.4 | ✗ 已点亮，排除 |
| earnings | 1（已点亮） | 1.4 | ✗ 已点亮，排除 |
| **option** | **0** | **1.3** | ✓ 投 |
| **macro** | **0** | 1.1 | ✓ 投 |
| **shortinterest** | **0** | 1.1 | ✓ 投 |
| **insiders** | **0** | 1.1 | ✓ 投 |
| **socialmedia** | **0** | 1.0 | ✓ 投 |
| **institutions** | **0** | 1.0 | ✓ 投（次优先）|
| **risk** | **0** | 1.1 | ✓ 投（次优先）|
| imbalance | 0 | 1.0 | 观察（仅 1 个数据集 imbalance5）|
| pv / fundamental / news / sentiment | 0 | — | 历史判死较多，本轮不投 |

## 1. S0 结果总览

`datasets=286　alive_ranked=93（tier1=40 / tier2=53 / floor_band=3）　dead_skipped=0　mode=general　method=quantile`

**信号分榜 top20**（战略排序，非点塔排序）：
`mmp_nlp_sentiment(1.0798) / predictive_starmine(1.0701) / model264(1.0691) / option_horizon_decomp(1.0691) / techindi_model(1.0686) / analyst_revision_horizons(1.0654) / continuation_score(1.0589) / other460(1.058) / pattern_scores(1.0554) / model354(1.0536) / multifactor_return_pred(1.0534) / tech_chart_model(1.0492) / model10(1.0439) / analyst15(1.0438) / chart_cnn_alpha(1.0438) / other596(1.0428) / other455(1.0362) / chart_return_model(1.0347) / global_seasonal_model(1.034) / pv98(1.0332)`

**点塔视角 top10**（非 model + 低拥挤加分）：
`finnews_nlp_scores(other) / other580(other) / ai_news_scores(other) / earningscall_embed(other) / nlp_news_scores(other) / pv63(pv) / order_book_imbalance(other) / dl_volume_pred(pv) / us_equity_news(other) / other546(other)`

⚠ **两个榜单严重背离** ⇒ 传统「按 score 排序取白名单」会全部落到 model 塔（已点亮）⇒ **本轮以点塔视角 + 未点亮塔 × 低拥挤为准，不按 signal score 排序**。

## 2. 入选数据集（4 个，均在未点亮塔）

### ★ A. `insider_agg_matrix`（insiders 塔，mult 1.1）— 本轮第一优先

| 项 | 值 |
|---|---|
| coverage | 0.7716 |
| fieldCount | 17（**全部 MATRIX**，无 VECTOR 坑） |
| userCount / alphaCount | 79 / 122（**极低拥挤**） |
| valueScore | 4.0（最高档）|

**字段画像（17 个全 MATRIX，cov 均 0.7716）**

| 字段 | userCount | alphaCount | 语义 |
|---|---:|---:|---|
| `directional_indicator_2` | 11 | 13 | 内部人活动**整体方向偏置** |
| `directional_significant_value_1..4` | 3–13 | 4–15 | 方向显著交易的第 1–4 大值 |
| `significant_value_1..4` | 6–26 | 8–34 | **最显著交易**第 1–4 大值 |
| `top_directional_significant_value_1..4` | 1–7 | 2–8 | 「top」口径方向显著交易 |
| `top_significant_value_1..4` | 3–5 | 3–9 | 「top」口径显著交易 |

**机制假设**：内部人交易**强度-梯度**（`_1` 最大 → `_4` 最小）比单一时点值信息更全；`directional_*` 编码方向（买/卖符号），`_2` 的 overall bias 是**净方向×强度合成**。
**学术支撑**：Seyhun (1986) 内部人交易超额收益、Lakonishok & Lee (1976) 内部人买入信号的显著正向预测力；「显著交易排序（rank of significance）」是经典构造。
**★ 与历史判死的区别**：`insider_matrix`（VECTOR 稀疏事件双墙）与 `insider_feats`（buy/sell ratio 无独立信号）判死，但**本集是 MATRIX + 预聚合 + alphaCount 个位数** ⇒ 结构与拥挤度都不同，不是同一个雷。

### ★ B. `option3`（option 塔，mult **1.3** 最高）— 第二优先

| 项 | 值 |
|---|---|
| coverage | 0.8801（vol/OI 0.88–0.95；put 侧 0.726） |
| fieldCount | 20（全部 MATRIX） |
| userCount / alphaCount | 277 / 469（**低拥挤**，对比 option8=196422） |
| valueScore | 3.0 |

**字段画像（20 个 MATRIX，三族 × ATM/ITM/OTM 三档）**

| 族 | 字段 | cov | 最低 userCount |
|---|---|---|---:|
| **open interest** | `opt3_openinte{call,put}{atm,itm,otm}` | 0.726–0.949 | 5（`opt3_openinteputotm`）|
| **implied vol** | `opt3_vol{call,put}{atm,itm,otma,otmb}` | 0.949 | 22 |
| **volume** | `opt3_volume{call,put}{atm,itm,otm}` | 0.726–0.949 | 11 |

**★ 关键情报**：`references/option.md` 明确「option 塔 USA：**surface-level IV 信号全线关闭；只剩 volume/OI 类 option 数据集可用**」⇒ 本集正是 volume/OI 族，且 **IV 族已被 option40 判死不必再投**。
**论坛支撑**：
- 《The Information Content of Option Demand》(Research Paper 71) → **期权需求的信息含量**（O/S volume ratio）；
- 《The option to stock volume ratio and future returns》→ 期权成交量 / 股票成交量比率；
- 《Individual Option Volatility Smirk》→ `group_neutralize(alpha, bucket(rank(volume), range="0,1,0.1"))` 的**成交量分桶**做法（可作分组轴）。
**探针设计**：`divide(put OI, call OI)` 与 `divide(call OTM volume, put OTM volume)`——**比率形态**（合规：不触「禁混信号」加法闸）。

### ★ C. `board_gov_stats`（insiders 塔，mult 1.1）— 第三优先

| 项 | 值 |
|---|---|
| coverage | 0.9482（多数字段）|
| fieldCount | 46（全部 MATRIX） |
| userCount / alphaCount | 220 / 444（低拥挤）|
| valueScore | 3.0 |

**字段画像（46 个，按机制分 6 组）**

| 组 | 代表字段 | cov | 语义 |
|---|---|---|---|
| **董事会/管理层离职率** | `board_departure_rate_{1y_board, 3m/6m_management}`、`management_departure_rate_*`、`personnel_departure_rate_*` | 0.877–0.923 | **turnover 异象**（高流失⇒治理差） |
| **董事会/管理层加入率** | `board_join_rate_*`、`management_join_rate_*`、`personnel_join_rate_*` | 0.877–0.923 | 净变化的方向腿 |
| **独立性/结构** | `independent_director_ratio`、`board_member_count_2`、`total_personnel_count`、`management_team_size` | 0.941–0.948 | 治理质量代理 |
| **网络连接** | `aggregate_external_connections`、`board_external_connection_count`、`unique_external_company_{board,management,union}`、`{board,management}_external_connection_count` | 0.941–0.948 | 董事会网络 busy-ness |
| **任期** | `ceo_tenure_days`、`chairman_tenure_days`、`{max,median,min}_chief_officer_tenure_days` | 0.933–0.936 | 管理层稳定性 |
| **其他治理** | `ceo_chairman_duality_flag`、`multiple_ceo_indicator`、`doctorate_share_*`、`male_ratio_*`、`surname_concentration_*`、`ceo_gender_flag` | 0.595–0.948 | 治理质量/多样性 |

**机制假设**：① **turnover 异象**（Bhagat, Shleifer & Vishny 2003「Governance and Business Performance」— 高管理层流失与低绩效相关）；② `departure_rate − join_rate` = **净流失**（结构化减法，非混信号）；③ 任期天数 = 稳定性代理。
**★ 注意 `surname_concentration_management` cov=0.5948 < 0.65 硬地板** ⇒ 不用。

### ★ D. `short_interest_pred`（shortinterest 塔，mult 1.1）— 第四优先

| 项 | 值 |
|---|---|
| coverage | **0.9987（近乎满覆盖）** |
| fieldCount | 10（全部 MATRIX） |
| userCount / alphaCount | 172 / 369（低拥挤） |
| valueScore | 3.0 |

**字段画像（10 个，`prior_*` 前一期 / 裸当期，`surprise` 系列为预测意外）**

| 字段 | userCount | alphaCount | 语义 |
|---|---:|---:|---|
| `short_interest_predicted_change` | 97 | 197 | 当期**预测变动**（最拥挤） |
| `short_interest_surprise_ratio` | 36 | 56 | **实际/预测比**＝意外幅度（比率，已归一） |
| `short_interest_surprise_value` | 17 | 20 | 实际 − 预测（绝对差） |
| `short_interest_surprise_amount` | 9 | 14 | 意外金额 |
| `short_interest_predicted_value` | 16 | 23 | 当期预测水平 |
| `prior_short_interest_surprise_ratio` | 15 | 28 | 前一期意外比 |
| `prior_short_interest_surprise_{value,amount}` | 9–10 | 11–12 | 前一期意外 |
| `prior_short_interest_predicted_{change,value}` | 14–26 | 17–31 | 前一期预测 |

**机制假设**：这是**做空情绪的「预期 vs 实际」分解**，不是水平值。`surprise_ratio` 是纯比率形态（合规且已归一），经济含义 = **空头拥挤度意外变化** ⇒ 经典「挤空（short squeeze）」前兆。
**论坛支撑**：《基于 short interest 数据的跨交易所组合案例》明确「根据 short volume to volume ratio 构建因子，`ts_rank`」。
**★ 与历史判死的区别**：`shortinterest3`（securities lending，prod **0.957** 结构性墙）与 `shortinterest29`（rank 弱）判死；本集是**平台自带预测模型的 surprise 分解**（cov 0.9987），机制与拥挤度都不同。

## 3. 本轮不投的数据集（附理由）

| 数据集 | 塔 | 不投理由 |
|---|---|---|
| `option8` / `option40` / `option6` / `option9` | option | option.md：surface-level IV 全线关闭；option8 prod 0.83–0.91 九颗死；option40 max S 1.12 |
| `insiders1` / `insider_matrix` / `insider_feats` | insiders | 历史判死（prod / 稀疏事件双墙 / 无独立信号）|
| `shortinterest3` | shortinterest | prod 0.957 结构性墙，永久封存 |
| `shortinterest29` | shortinterest | rank 弱（`USA-SHORTINTEREST29-RANK-WEAK`）|
| `socialmedia12` / `socialmedia8` | socialmedia | alphaCount 60341 / 16947，极度拥挤；sentiment 族跨区死路 |
| `creator_signal_perf` | socialmedia | **全部 VECTOR（102 个）** + cov 0.60–0.65 贴着硬地板 ⇒ 需 vec_* 归约且覆盖不足，本轮降级 |
| `insiders3` / `insiders4` | insiders | alphaCount 37210 / 1450，拥挤 |
| `institutions6` | institutions | 96 条配置矩阵已数学穷尽，天花板 S 1.03 |
| `macro38` | macro | fitness/margin 双结构性墙（fit 0.82 / margin 0.62bp）|
| `risk70` / `risk62` | risk | alphaCount 106478 / 24028，极度拥挤 |
| `dl_riskfree_returns` | risk | 本轮早前实证天花板 1.40 < 所需 1.81 |
| `twitter_sentiment_l2` | socialmedia | 95 字段 MATRIX/cov 0.82–1.0/alphaCount 0–40 **画像极好**，但情绪族 USA prod 0.80–0.96 饱和 ⇒ **列为第二轮备选**（`market_relevance_score_*` 是「市场相关度」而非情绪分，机制上更接近 attention 而非 sentiment ⇒ 值得单独试）|

## 4. 骨架选择（USA 已验证 b3 型）

```
group_rank(ts_zscore(ts_backfill(F, 252), 252), industry)
```

**证据**：`omWMO06n`（S 2.50 / F 1.52 / 2Y 4.22 / prod **0.6948 PASS** / self 0.3908）用的就是这个骨架 + `STATISTICAL` 中性化 + `decay=0`。
`references/model.md`：b3 型「SUB 与 S 同高，无比值闸压力」⇒ USA 最稳。
**★ 中性化纪律**：USA 实测 **SUBINDUSTRY 是最差 prod 轴**（avg 0.685 最高）；压 prod 用 **STATISTICAL / SECTOR** ⇒ 本轮统一走 `STATISTICAL`（注意：`config/settings.json` 默认值仍是 SUBINDUSTRY，属已知不一致，以实测为准）。

## 5. 首波探针（8 条，2026-10-14 已派发）

| # | 表达式 | 数据集 |
|---|---|---|
| 1 | `group_rank(ts_zscore(ts_backfill(significant_value_1, 252), 252), industry)` | insider_agg_matrix |
| 2 | `group_rank(ts_zscore(ts_backfill(directional_indicator_2, 252), 252), industry)` | insider_agg_matrix |
| 3 | `group_rank(ts_zscore(ts_backfill(divide(opt3_openinteputatm, opt3_openintecallatm), 252), 252), industry)` | option3 |
| 4 | `group_rank(ts_zscore(ts_backfill(divide(opt3_volumecallotm, opt3_volumeputotm), 252), 252), industry)` | option3 |
| 5 | `group_rank(ts_zscore(ts_backfill(board_departure_rate_1y_board, 252), 252), industry)` | board_gov_stats |
| 6 | `group_rank(ts_zscore(ts_backfill(independent_director_ratio, 252), 252), industry)` | board_gov_stats |
| 7 | `group_rank(ts_zscore(ts_backfill(short_interest_surprise_ratio, 252), 252), industry)` | short_interest_pred |
| 8 | `group_rank(ts_zscore(ts_backfill(short_interest_predicted_change, 252), 252), industry)` | short_interest_pred |

设置：USA / TOP3000 / D1 / **STATISTICAL** / decay 5 / trunc 0.08 / nanHandling ON / maxTrade OFF / pasteurization ON / unitHandling VERIFY
multi-sim：`2TWTRR4EO4TTaRtl6Ce50VG`（1–4）、`4hbWAcP34CU9uDf0ZTLBox`（5–8）
preflight：`valid=true, unknown_fields=[], vector_fields=[]`（8 字段全部平台实时校验通过）