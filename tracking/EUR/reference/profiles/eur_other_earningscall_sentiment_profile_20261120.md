# EUR / earningscall_sentiment 全字段画像（2026-11-20）

> 平台实查 `get_datafields(dataset_id=earningscall_sentiment, region=EUR, universe=TOP2500, delay=1)`：**MATRIX 121（平台声明）+ VECTOR 23（complete=True）= 144 字段**。
> 命名规则 `eur_<category>_<dataset>_profile_<YYYYMMDD>.md`；数据集 category=other，但语料是 earnings call transcript，投 **socialmedia 塔（0/3，唯一全零塔）**，multiplier 1.5，valueScore 6.0，aC 1306，cov 0.5115。
> 字段全为 2025-11-01 onboard 的新代（Euro universe 上架时间短）。

## 1. 字段结构总览（144 字段 = 5 维度 × 4 节 × 3 极性 + 元数据）

### 维度结构（5 经济主题 × 4 电话会节段 × {positive,negative,neutral} 概率 + polarity + count）
| 维度（axis） | 说明 | aC 头部字段 |
|---|---|---|
| profitability | 盈利能力 | presentation 极性 aC160（最高）、summary aC55、answer aC40 |
| assetutilization | 资产利用 | answer aC78、summary aC32 |
| leverage | 杠杆 | presentation aC57、summary aC13 |
| cashflow | 现金流 | summary aC25、answer aC22 |
| valuation | 估值 | presentation aC23、summary aC15 |

### 节段（section）结构
- **presentation**：管理层陈述（aC 最高，拥挤度最高，均值回归风险）
- **answer**：Q&A 回答段（aC 次之，信息量最高——分析师追问后管理层表态）
- **question**：Q&A 提问段（aC 最低 1–11，极冷门）
- **summary**：全文汇总（aC 中等）

### 元数据
- `answer_chunk_count`：电话会 Answers 段语义块总数（aC 94，事件规模代理）
- `chunk_relevance_z0/z1/z2_flag`（VECTOR）：块相关性门槛标记

### VECTOR（23 个，须 vec_* 降维）
- `{axis}_sentiment_polarity` × 5：块级有符号净极性（−1~+1）
- `{axis}_{positive,negative,neutral}_score` × 15：块级概率
- `chunk_relevance_z*_flag` × 3



## 字段全表（144 字段实测读数，来源 get_datafields 2026-11-20）

| 字段 | 类型 | cov | uC | aC | 节段 | 说明 |
|---|---|---:|---:|---:|---|---|
| `count_negative_assetutilization_presentation` | MATRIX | 0.5115 |  |  | presentation | count of negative chunks on assetutilization |
| `count_negative_assetutilization_question` | MATRIX | 0.5115 |  |  | question | count of negative chunks on assetutilization |
| `count_negative_assetutilization_answer` | MATRIX | 0.5115 |  |  | answer | count of negative chunks on assetutilization |
| `count_negative_assetutilization_summary` | MATRIX | 0.5115 |  |  | summary | count of negative chunks on assetutilization |
| `count_negative_cashflow_presentation` | MATRIX | 0.5115 |  |  | presentation | count of negative chunks on cashflow |
| `count_negative_cashflow_question` | MATRIX | 0.5115 |  |  | question | count of negative chunks on cashflow |
| `count_negative_cashflow_answer` | MATRIX | 0.5115 |  |  | answer | count of negative chunks on cashflow |
| `count_negative_cashflow_summary` | MATRIX | 0.5115 |  |  | summary | count of negative chunks on cashflow |
| `count_negative_leverage_presentation` | MATRIX | 0.5115 |  |  | presentation | count of negative chunks on leverage |
| `count_negative_leverage_question` | MATRIX | 0.5115 |  |  | question | count of negative chunks on leverage |
| `count_negative_leverage_answer` | MATRIX | 0.5115 |  |  | answer | count of negative chunks on leverage |
| `count_negative_leverage_summary` | MATRIX | 0.5115 |  |  | summary | count of negative chunks on leverage |
| `count_negative_profitability_presentation` | MATRIX | 0.5115 |  |  | presentation | count of negative chunks on profitability |
| `count_negative_profitability_question` | MATRIX | 0.5115 |  |  | question | count of negative chunks on profitability |
| `count_negative_profitability_answer` | MATRIX | 0.5115 |  |  | answer | count of negative chunks on profitability |
| `count_negative_profitability_summary` | MATRIX | 0.5115 |  |  | summary | count of negative chunks on profitability |
| `count_negative_valuation_presentation` | MATRIX | 0.5115 |  |  | presentation | count of negative chunks on valuation |
| `count_negative_valuation_question` | MATRIX | 0.5115 |  |  | question | count of negative chunks on valuation |
| `count_negative_valuation_answer` | MATRIX | 0.5115 |  |  | answer | count of negative chunks on valuation |
| `count_negative_valuation_summary` | MATRIX | 0.5115 |  |  | summary | count of negative chunks on valuation |
| `count_neutral_assetutilization_presentation` | MATRIX | 0.5115 |  |  | presentation | count of neutral chunks on assetutilization |
| `count_neutral_assetutilization_question` | MATRIX | 0.5115 |  |  | question | count of neutral chunks on assetutilization |
| `count_neutral_assetutilization_answer` | MATRIX | 0.5115 |  |  | answer | count of neutral chunks on assetutilization |
| `count_neutral_assetutilization_summary` | MATRIX | 0.5115 |  |  | summary | count of neutral chunks on assetutilization |
| `count_neutral_cashflow_presentation` | MATRIX | 0.5115 |  |  | presentation | count of neutral chunks on cashflow |
| `count_neutral_cashflow_question` | MATRIX | 0.5115 |  |  | question | count of neutral chunks on cashflow |
| `count_neutral_cashflow_answer` | MATRIX | 0.5115 |  |  | answer | count of neutral chunks on cashflow |
| `count_neutral_cashflow_summary` | MATRIX | 0.5115 |  |  | summary | count of neutral chunks on cashflow |
| `count_neutral_leverage_presentation` | MATRIX | 0.5115 |  |  | presentation | count of neutral chunks on leverage |
| `count_neutral_leverage_question` | MATRIX | 0.5115 |  |  | question | count of neutral chunks on leverage |
| `count_neutral_leverage_answer` | MATRIX | 0.5115 |  |  | answer | count of neutral chunks on leverage |
| `count_neutral_leverage_summary` | MATRIX | 0.5115 |  |  | summary | count of neutral chunks on leverage |
| `count_neutral_profitability_presentation` | MATRIX | 0.5115 |  |  | presentation | count of neutral chunks on profitability |
| `count_neutral_profitability_question` | MATRIX | 0.5115 |  |  | question | count of neutral chunks on profitability |
| `count_neutral_profitability_answer` | MATRIX | 0.5115 |  |  | answer | count of neutral chunks on profitability |
| `count_neutral_profitability_summary` | MATRIX | 0.5115 |  |  | summary | count of neutral chunks on profitability |
| `count_neutral_valuation_presentation` | MATRIX | 0.5115 |  |  | presentation | count of neutral chunks on valuation |
| `count_neutral_valuation_question` | MATRIX | 0.5115 |  |  | question | count of neutral chunks on valuation |
| `count_neutral_valuation_answer` | MATRIX | 0.5115 |  |  | answer | count of neutral chunks on valuation |
| `count_neutral_valuation_summary` | MATRIX | 0.5115 |  |  | summary | count of neutral chunks on valuation |
| `count_positive_assetutilization_presentation` | MATRIX | 0.5115 |  |  | presentation | count of positive chunks on assetutilization |
| `count_positive_assetutilization_question` | MATRIX | 0.5115 |  |  | question | count of positive chunks on assetutilization |
| `count_positive_assetutilization_answer` | MATRIX | 0.5115 |  |  | answer | count of positive chunks on assetutilization |
| `count_positive_assetutilization_summary` | MATRIX | 0.5115 |  |  | summary | count of positive chunks on assetutilization |
| `count_positive_cashflow_presentation` | MATRIX | 0.5115 |  |  | presentation | count of positive chunks on cashflow |
| `count_positive_cashflow_question` | MATRIX | 0.5115 |  |  | question | count of positive chunks on cashflow |
| `count_positive_cashflow_answer` | MATRIX | 0.5115 |  |  | answer | count of positive chunks on cashflow |
| `count_positive_cashflow_summary` | MATRIX | 0.5115 |  |  | summary | count of positive chunks on cashflow |
| `count_positive_leverage_presentation` | MATRIX | 0.5115 |  |  | presentation | count of positive chunks on leverage |
| `count_positive_leverage_question` | MATRIX | 0.5115 |  |  | question | count of positive chunks on leverage |
| `count_positive_leverage_answer` | MATRIX | 0.5115 |  |  | answer | count of positive chunks on leverage |
| `count_positive_leverage_summary` | MATRIX | 0.5115 |  |  | summary | count of positive chunks on leverage |
| `count_positive_profitability_presentation` | MATRIX | 0.5115 |  |  | presentation | count of positive chunks on profitability |
| `count_positive_profitability_question` | MATRIX | 0.5115 |  |  | question | count of positive chunks on profitability |
| `count_positive_profitability_answer` | MATRIX | 0.5115 |  |  | answer | count of positive chunks on profitability |
| `count_positive_profitability_summary` | MATRIX | 0.5115 |  |  | summary | count of positive chunks on profitability |
| `count_positive_valuation_presentation` | MATRIX | 0.5115 |  |  | presentation | count of positive chunks on valuation |
| `count_positive_valuation_question` | MATRIX | 0.5115 |  |  | question | count of positive chunks on valuation |
| `count_positive_valuation_answer` | MATRIX | 0.5115 |  |  | answer | count of positive chunks on valuation |
| `count_positive_valuation_summary` | MATRIX | 0.5115 |  |  | summary | count of positive chunks on valuation |
| `mean_negative_assetutilization_presentation` | MATRIX | 0.5113 |  |  | presentation | mean negative prob on assetutilization |
| `mean_negative_assetutilization_question` | MATRIX | 0.5018 |  |  | question | mean negative prob on assetutilization |
| `mean_negative_assetutilization_answer` | MATRIX | 0.5018 |  |  | answer | mean negative prob on assetutilization |
| `mean_negative_assetutilization_summary` | MATRIX | 0.5115 |  |  | summary | mean negative prob on assetutilization |
| `mean_negative_cashflow_presentation` | MATRIX | 0.5113 |  |  | presentation | mean negative prob on cashflow |
| `mean_negative_cashflow_question` | MATRIX | 0.5018 |  |  | question | mean negative prob on cashflow |
| `mean_negative_cashflow_answer` | MATRIX | 0.5018 |  |  | answer | mean negative prob on cashflow |
| `mean_negative_cashflow_summary` | MATRIX | 0.5115 |  |  | summary | mean negative prob on cashflow |
| `mean_negative_leverage_presentation` | MATRIX | 0.5113 |  |  | presentation | mean negative prob on leverage |
| `mean_negative_leverage_question` | MATRIX | 0.5018 |  |  | question | mean negative prob on leverage |
| `mean_negative_leverage_answer` | MATRIX | 0.5018 |  |  | answer | mean negative prob on leverage |
| `mean_negative_leverage_summary` | MATRIX | 0.5115 |  |  | summary | mean negative prob on leverage |
| `mean_negative_profitability_presentation` | MATRIX | 0.5113 |  |  | presentation | mean negative prob on profitability |
| `mean_negative_profitability_question` | MATRIX | 0.5018 |  |  | question | mean negative prob on profitability |
| `mean_negative_profitability_answer` | MATRIX | 0.5018 |  |  | answer | mean negative prob on profitability |
| `mean_negative_profitability_summary` | MATRIX | 0.5115 |  |  | summary | mean negative prob on profitability |
| `mean_negative_valuation_presentation` | MATRIX | 0.5113 |  |  | presentation | mean negative prob on valuation |
| `mean_negative_valuation_question` | MATRIX | 0.5018 |  |  | question | mean negative prob on valuation |
| `mean_negative_valuation_answer` | MATRIX | 0.5018 |  |  | answer | mean negative prob on valuation |
| `mean_negative_valuation_summary` | MATRIX | 0.5115 |  |  | summary | mean negative prob on valuation |
| `mean_neutral_assetutilization_presentation` | MATRIX | 0.5113 |  |  | presentation | mean neutral prob on assetutilization |
| `mean_neutral_assetutilization_question` | MATRIX | 0.5018 |  |  | question | mean neutral prob on assetutilization |
| `mean_neutral_assetutilization_answer` | MATRIX | 0.5018 |  |  | answer | mean neutral prob on assetutilization |
| `mean_neutral_assetutilization_summary` | MATRIX | 0.5115 |  |  | summary | mean neutral prob on assetutilization |
| `mean_neutral_cashflow_presentation` | MATRIX | 0.5113 |  |  | presentation | mean neutral prob on cashflow |
| `mean_neutral_cashflow_question` | MATRIX | 0.5018 |  |  | question | mean neutral prob on cashflow |
| `mean_neutral_cashflow_answer` | MATRIX | 0.5018 |  |  | answer | mean neutral prob on cashflow |
| `mean_neutral_cashflow_summary` | MATRIX | 0.5115 |  |  | summary | mean neutral prob on cashflow |
| `mean_neutral_leverage_presentation` | MATRIX | 0.5113 |  |  | presentation | mean neutral prob on leverage |
| `mean_neutral_leverage_question` | MATRIX | 0.5018 |  |  | question | mean neutral prob on leverage |
| `mean_neutral_leverage_answer` | MATRIX | 0.5018 |  |  | answer | mean neutral prob on leverage |
| `mean_neutral_leverage_summary` | MATRIX | 0.5115 |  |  | summary | mean neutral prob on leverage |
| `mean_neutral_profitability_presentation` | MATRIX | 0.5113 |  |  | presentation | mean neutral prob on profitability |
| `mean_neutral_profitability_question` | MATRIX | 0.5018 |  |  | question | mean neutral prob on profitability |
| `mean_neutral_profitability_answer` | MATRIX | 0.5018 |  |  | answer | mean neutral prob on profitability |
| `mean_neutral_profitability_summary` | MATRIX | 0.5115 |  |  | summary | mean neutral prob on profitability |
| `mean_neutral_valuation_presentation` | MATRIX | 0.5113 |  |  | presentation | mean neutral prob on valuation |
| `mean_neutral_valuation_question` | MATRIX | 0.5018 |  |  | question | mean neutral prob on valuation |
| `mean_neutral_valuation_answer` | MATRIX | 0.5018 |  |  | answer | mean neutral prob on valuation |
| `mean_neutral_valuation_summary` | MATRIX | 0.5115 |  |  | summary | mean neutral prob on valuation |
| `mean_positive_assetutilization_presentation` | MATRIX | 0.5113 |  |  | presentation | mean positive prob on assetutilization |
| `mean_positive_assetutilization_question` | MATRIX | 0.5018 |  |  | question | mean positive prob on assetutilization |
| `mean_positive_assetutilization_answer` | MATRIX | 0.5018 |  |  | answer | mean positive prob on assetutilization |
| `mean_positive_assetutilization_summary` | MATRIX | 0.5115 |  |  | summary | mean positive prob on assetutilization |
| `mean_positive_cashflow_presentation` | MATRIX | 0.5113 |  |  | presentation | mean positive prob on cashflow |
| `mean_positive_cashflow_question` | MATRIX | 0.5018 |  |  | question | mean positive prob on cashflow |
| `mean_positive_cashflow_answer` | MATRIX | 0.5018 |  |  | answer | mean positive prob on cashflow |
| `mean_positive_cashflow_summary` | MATRIX | 0.5115 |  |  | summary | mean positive prob on cashflow |
| `mean_positive_leverage_presentation` | MATRIX | 0.5113 |  |  | presentation | mean positive prob on leverage |
| `mean_positive_leverage_question` | MATRIX | 0.5018 |  |  | question | mean positive prob on leverage |
| `mean_positive_leverage_answer` | MATRIX | 0.5018 |  |  | answer | mean positive prob on leverage |
| `mean_positive_leverage_summary` | MATRIX | 0.5115 |  |  | summary | mean positive prob on leverage |
| `mean_positive_profitability_presentation` | MATRIX | 0.5113 |  |  | presentation | mean positive prob on profitability |
| `mean_positive_profitability_question` | MATRIX | 0.5018 |  |  | question | mean positive prob on profitability |
| `mean_positive_profitability_answer` | MATRIX | 0.5018 |  |  | answer | mean positive prob on profitability |
| `mean_positive_profitability_summary` | MATRIX | 0.5115 |  |  | summary | mean positive prob on profitability |
| `mean_positive_valuation_presentation` | MATRIX | 0.5113 |  |  | presentation | mean positive prob on valuation |
| `mean_positive_valuation_question` | MATRIX | 0.5018 |  |  | question | mean positive prob on valuation |
| `mean_positive_valuation_answer` | MATRIX | 0.5018 |  |  | answer | mean positive prob on valuation |
| `mean_positive_valuation_summary` | MATRIX | 0.5115 |  |  | summary | mean positive prob on valuation |
| `mean_polarity_assetutilization_presentation` | MATRIX | 0.5113 |  |  | presentation | signed polarity on assetutilization |
| `mean_polarity_assetutilization_question` | MATRIX | 0.5018 |  |  | question | signed polarity on assetutilization |
| `mean_polarity_assetutilization_answer` | MATRIX | 0.5018 |  |  | answer | signed polarity on assetutilization |
| `mean_polarity_assetutilization_summary` | MATRIX | 0.5115 |  |  | summary | signed polarity on assetutilization |
| `mean_polarity_cashflow_presentation` | MATRIX | 0.5113 |  |  | presentation | signed polarity on cashflow |
| `mean_polarity_cashflow_question` | MATRIX | 0.5018 |  |  | question | signed polarity on cashflow |
| `mean_polarity_cashflow_answer` | MATRIX | 0.5018 |  |  | answer | signed polarity on cashflow |
| `mean_polarity_cashflow_summary` | MATRIX | 0.5115 |  |  | summary | signed polarity on cashflow |
| `mean_polarity_leverage_presentation` | MATRIX | 0.5113 |  |  | presentation | signed polarity on leverage |
| `mean_polarity_leverage_question` | MATRIX | 0.5018 |  |  | question | signed polarity on leverage |
| `mean_polarity_leverage_answer` | MATRIX | 0.5018 |  |  | answer | signed polarity on leverage |
| `mean_polarity_leverage_summary` | MATRIX | 0.5115 |  |  | summary | signed polarity on leverage |
| `mean_polarity_profitability_presentation` | MATRIX | 0.5113 |  |  | presentation | signed polarity on profitability |
| `mean_polarity_profitability_question` | MATRIX | 0.5018 |  |  | question | signed polarity on profitability |
| `mean_polarity_profitability_answer` | MATRIX | 0.5018 |  |  | answer | signed polarity on profitability |
| `mean_polarity_profitability_summary` | MATRIX | 0.5115 |  |  | summary | signed polarity on profitability |
| `mean_polarity_valuation_presentation` | MATRIX | 0.5113 |  |  | presentation | signed polarity on valuation |
| `mean_polarity_valuation_question` | MATRIX | 0.5018 |  |  | question | signed polarity on valuation |
| `mean_polarity_valuation_answer` | MATRIX | 0.5018 |  |  | answer | signed polarity on valuation |
| `mean_polarity_valuation_summary` | MATRIX | 0.5115 |  |  | summary | signed polarity on valuation |
| `answer_chunk_count` | MATRIX | 0.5115 | 66 | 94 | answers | Answers 段语义块总数 |
| `assetutilization_sentiment_polarity` | VECTOR | 0.5115 |  |  | chunk | 块级有符号净极性 −1~+1 |
| `cashflow_sentiment_polarity` | VECTOR | 0.5115 |  |  | chunk | 块级有符号净极性 −1~+1 |
| `leverage_sentiment_polarity` | VECTOR | 0.5115 |  |  | chunk | 块级有符号净极性 −1~+1 |
| `profitability_sentiment_polarity` | VECTOR | 0.5115 |  |  | chunk | 块级有符号净极性 −1~+1 |
| `valuation_sentiment_polarity` | VECTOR | 0.5115 |  |  | chunk | 块级有符号净极性 −1~+1 |
| `assetutilization_positive_score` | VECTOR | 0.5115 |  |  | chunk | 块级 positive 概率 |
| `assetutilization_negative_score` | VECTOR | 0.5115 |  |  | chunk | 块级 negative 概率 |
| `assetutilization_neutral_score` | VECTOR | 0.5115 |  |  | chunk | 块级 neutral 概率 |
| `cashflow_positive_score` | VECTOR | 0.5115 |  |  | chunk | 块级 positive 概率 |
| `cashflow_negative_score` | VECTOR | 0.5115 |  |  | chunk | 块级 negative 概率 |
| `cashflow_neutral_score` | VECTOR | 0.5115 |  |  | chunk | 块级 neutral 概率 |
| `leverage_positive_score` | VECTOR | 0.5115 |  |  | chunk | 块级 positive 概率 |
| `leverage_negative_score` | VECTOR | 0.5115 |  |  | chunk | 块级 negative 概率 |
| `leverage_neutral_score` | VECTOR | 0.5115 |  |  | chunk | 块级 neutral 概率 |
| `profitability_positive_score` | VECTOR | 0.5115 |  |  | chunk | 块级 positive 概率 |
| `profitability_negative_score` | VECTOR | 0.5115 |  |  | chunk | 块级 negative 概率 |
| `profitability_neutral_score` | VECTOR | 0.5115 |  |  | chunk | 块级 neutral 概率 |
| `valuation_positive_score` | VECTOR | 0.5115 |  |  | chunk | 块级 positive 概率 |
| `valuation_negative_score` | VECTOR | 0.5115 |  |  | chunk | 块级 negative 概率 |
| `valuation_neutral_score` | VECTOR | 0.5115 |  |  | chunk | 块级 neutral 概率 |
| `chunk_relevance_z0_flag` | VECTOR | 0.5115 |  |  | chunk | 块相关性门槛 flag |
| `chunk_relevance_z1_flag` | VECTOR | 0.5115 |  |  | chunk | 块相关性门槛 flag |
| `chunk_relevance_z2_flag` | VECTOR | 0.5115 |  |  | chunk | 块相关性门槛 flag |

## 2. 六维画像

- **类型**：MATRIX 121（count/mean 双族）+ VECTOR 23（polarity/概率/flag）——MATRIX 直接可用，VECTOR 须 vec_avg/vec_sum。
- **覆盖率**：全族 cov 0.5115（presentation/summary/count 族）与 0.5018/0.476（answer/question 的 mean 族）——**约一半宇宙有值**，事件型（电话会日才有值）。
- **更新频率**：季频事件（电话会），日频面板稀疏 ⇒ 须 `ts_backfill(...,66~120)` 补齐后用时序相对化。
- **分布特征**：count 族 = 非负整数（0~几百），mean 族 = 有界 [−1,1] 极性或 [0,1] 概率 ⇒ **有界读数 → `ts_zscore(ts_backfill(F,66),252)` 是已验证有效形态**（earnings_sent_matrix 同构）。
- **可用性**：aC 1–160 全族低拥挤（相对 analyst4 的 109400），question 段字段 aC≤11 极冷门；2025-11 新 onboard ⇒ prod 友好窗口期。
- **适用性**：主信号 = mean_polarity_{axis}_{summary,answer}（有界极性）；辅助 = count_{pos,neg}_{axis}_summary（净差数）；门控 = answer_chunk_count（事件规模）；VECTOR polarity 可作交叉验证腿。

## 3. 机制假设（论文锚）

- *Earnings conference calls and stock returns: The incremental informativeness of textual tone*（JBF 2012）：电话会文本语调**增量**于盈利惊喜，预测收益；
- *Conference Call Tone and Stock Returns*（AJFS 2017）：负语调 → 低收益（弱市场效率）；
- 模板先验：polarity 正向（语调好→多）；count 净差（positive−negative）正向。

## 4. 段1 实测 12 臂（TOP2500×INDUSTRY×decay4×nanHandling ON）

| 臂型 | 最优 | S 范围 | 2Y 范围 | TO |
|---|---|---|---|---|
| 5 极性 summary（profit/au/cf/lev/val） | O0WJnn9q（assetutilization）S0.51 | 0.24–0.51 | 0.88–1.38 | 4.4% |
| 2 极性 presentation（profit/cf） | A1xQnn3W S0.42 | 0.42 | 1.38 | 4.4% |
| 3 极性 answer/valuation（au/cf） | xAv1eexw S0.37 | 0.20–0.37 | 1.03–1.15 | 4.3% |
| 4 count 净差（profit/cf/au/lev） | 1YWjoNKz S0.44 | 0.30–0.44 | 1.04–1.38 | 4.5% |

**段1 全 REJECT**（S 闸 1.58），但三特征与 socialmedia15 根本不同：
1. **全正 S**（无方向悖论，取反必负——论坛文本语调先验方向被 EUR 实证确认）；
2. **TO 4.4% 极低**（事件稀疏+backfill 后近恒定）⇒ F 分母走 0.125 地板，**F≈S×2.83**，F 闸实际等价 S≥0.71 上下——但 S 只有 0.5 量级；
3. **sub 0.54–0.85 全正**（rank 未哑变量化——cov 0.51 的事件数远高于 socialmedia15 的 cov 0.37 且分布更均匀）。

### 逐年诊断（O0WJnn9q，assetutilization summary）
- **2014 S1.35 / 2023 S2.39 两端强**，2019 S1.37 / 2020 S0.98 中段强；
- **2015–2017 连续 3 年负**（−0.26/−0.44/−0.24）：弱年不是数据缺失（longCount 694–809 全年>0）而是**regime 段**（低波动牛市，语调-收益关系钝化）；
- 2023 S2.39 说明**近端信号在增强**（NLP 新代字段），2Y 1.24–1.38 与 2023 强年一致。

### 段2 形态验证（8 臂全 FAIL，工程坑）
- `vec_avg({axis}_sentiment_polarity)` 等 5 臂：**VECTOR 字段裸用**（未 vec_*）被平台拒——子代理横切时未走 preflight 修复路径；
- `vec_sum(subtract(count_...))`：MATRIX 字段被 vec_sum 包裹也 FAIL（vec_* 只吃 VECTOR）；
- `divide(subtract(...), add(answer_chunk_count,1))` + `mean_polarity_profitability_answer` 短窗（66,66）2 臂重试在队列（排队 25+ 分钟）。

## 5. 初步判定（PROVISIONAL）

- **方向确认**（全正）、**覆盖非缺陷**（sub 全正）、**近端增强**（2023 S2.39）——**该集与 socialmedia15 有质的区别，不是哑变量结构**；
- 真瓶颈 = **S 绝对水平太低**（0.5 量级 vs 闸 1.58）。TO 4.4% 极低 ⇒ F≈2.83×S，若 S 能到 0.56+ F 即过 1.58（不对，F 闸是 1.0，S≥0.354 即过 F；S 闸 1.58 才是墙）；
- 段2 定向方向：**正负语调差分**（mean_positive − mean_negative 同轴）、**question 段冷门字段**（aC≤11）、**answer/presentation 分节对比**（信息增量假说的直接实现）、**事件门控**（trade_when(answer_chunk_count>0, ...)）。

## 6. 段3 突破：事件门控 + 定向优化（2026-11-20 晚，38 臂）

### 6.1 ★ 核心机制发现：**事件门控把 S 从 0.51 抬到 1.44**

段1/段2 的无门控骨架（`group_rank(ts_zscore(ts_backfill(mean_polarity_*, 66), 252), industry)`）全族 S 只有 0.20–0.51。
加 `trade_when(answer_chunk_count > 0, <骨架>, -1)` 后：

| 形态 | alpha | S | F | 2Y | TO | sub |
|---|---|---:|---:|---:|---:|---:|
| 门控 + zscore 252 | A1xQloVX | 1.44 | 0.75 | **2.17** | 3.78% | 1.22 |
| 门控 + zscore 504 | rK7d5REo | **1.58** | 0.89 | 2.26 | 3.69% | 1.20 |
| 门控 + zscore 756 + trunc0.02 | **omaoLaJl** | **1.76** | **1.05** | 2.25 | 3.62% | 1.36 |

**逐年诊断（门控版 A1xQloVX）**：2014–2023 **10 年全正**（1.57/1.02/1.52/0.21/1.44/0.92/1.36/1.75/2.19/2.21）——
无门控版的 2015–17 连续负年（regime 段）被门控彻底抹平。
**机制解释**：电话会语调只在**事件日**有信息；门控 = 只在事件发生时持仓，非事件日空仓（TO 降到 3.6–4.4%）。
⇒ **稀疏事件型数据集必须用 presence 门控，否则信号被大面积 NaN 摊薄**（与 socialmedia15 的 buzz 门控线索独立复现，两族不同集同结论）。

### 6.2 ★ CONCENTRATED_WEIGHT 0.5 的根因与解法

- **现象**：窄门控（`answer_chunk_count > 0`）全部臂 CW=0.5（限 0.1，超 5 倍）；truncation 0.08→0.02 **完全无效**（不是权重上限问题）。
- **根因**：门控只在电话会当日生效 ⇒ 任一交易日只有极少数股票持仓（longCount 798/shortCount 811 是年均值，
  但日度上集中在事件股）⇒ 单股权重集中。
- **解法（用户 2026-11-20 提示 group_backfill 解 CW，实测验证）**：
  - **宽门控**（`ts_sum(answer_chunk_count, 22) > 0` = 22 天内有事件即持仓）⇒ **CW 直接 PASS**（E5QVpQN0），
    代价 S 1.58→1.53；
  - **group_backfill 填 NaN**（`group_backfill(answer_chunk_count, subindustry, 5)` / 对 polarity 字段填）⇒
    把事件面按组扩散，同样放宽持仓面。

### 6.3 窗口/轴效应（门控内层）

| 轴 | 最优 | Δ |
|---|---|---|
| zscore 窗 | 756 > 504 > 252 | S +0.32（1.44→1.76） |
| backfill 窗 | 252 ≈ 66 | S +0.09 |
| 分组轴 | industry > sector > subindustry | subindustry 明显更差（S1.07） |
| 宇宙 | TOP2500 > TOPCS1600 | ΔS 0.2–0.4 |
| 语调轴 | profitability > assetutilization > cashflow > leverage | presentation 段（aC160）< summary 段 |
| count 净差 | 与 polarity 同向但更弱 | S 0.42 vs 0.45 |

### 6.4 塔位与合规

- `pyramids.list` = **EUR/D1/OTHER（mult 1.5）**——该集平台 category=other，**OTHER 塔已点亮**。
- **合规判定：表达式只用 earningscall_sentiment 单数据集字段 + 豁免分组轴 = 纯 ATOM** ⇒
  符合用户 2026-11-20 指令「已点亮塔不再持续投入，**除非 ATOM** 和作辅助腿组 regular alpha」。
- **当前最优候选 omaoLaJl**：S1.76 / F1.05 / 2Y2.25 / sub1.36 / TO3.62% / DD2.83% / invest1.37，
  **只余 CONCENTRATED_WEIGHT 一闸**（0.5 vs 0.1）；prod 待平台计算（两次查询均 pending/inflight）。
