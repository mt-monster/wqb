# DEU 数据集 → 字段层归类分析 · 2026-10-07

> 把「未测潜力池」的字段逐一展开归类，结果暴露了一个**结构性事实**和 **6 个全新机制族**。

---

## ★★ 结构性事实：未测池**绝大多数是 VECTOR 型**

| 数据集 | 高覆盖 | 类型构成 | 说明 |
|---|---:|---|---|
| `model216` | 45 | **VECTOR ×45** | 全 VECTOR |
| `news18` | 70 | **VECTOR ×64** + SYMBOL ×6 | 几乎全 VECTOR |
| `news17` | 48 | **VECTOR ×48** | 全 VECTOR |
| `news20` | 46 | **VECTOR ×46** | 全 VECTOR |
| `news50` | 37 | **VECTOR ×37** | 全 VECTOR |
| `shortinterest3` | 25 | **VECTOR ×25** | 全 VECTOR |
| `fund_holdings_panel` | 18 | **VECTOR ×18** | 全 VECTOR |
| `sentiment27` | 18 | **VECTOR ×14** + SYMBOL ×4 | — |
| `other250` | 12 | **VECTOR ×12** | 全 VECTOR |
| `other47` | 9 | **VECTOR ×9** | 全 VECTOR |
| `analyst48` | 7 | **VECTOR ×7** | 全 VECTOR |
| `risk60` | 5 | **VECTOR ×5** | 全 VECTOR |

**⇒ 未测的 ~330 个高覆盖字段里，绝大多数是 VECTOR。**

**这意味着两件事：**

1. **它们全部必须经 `vec_*` 聚合才能用** —— 这也解释了为什么这些池的历史高分我从未复现（我一直没做对包装）。
2. **`vec_*` 的选择本身就是一个"逐字段机制搜索"** —— 我实测过：
   - `vec_max`（最乐观/最大值）= **0.43**
   - `vec_avg`（均值）= 0.35
   - `vec_range` / `vec_count` = 负
   ⇒ **同一字段换聚合算子，结果差 0.1~0.5。这是与"轴层数"同级的一个新搜索维度。**

---

## 一 六个全新机制族（从未碰过）

### ① ★★★ 信用 / 违约风险（**model28 + model36 + model53，共 67 个字段**）

| 数据集 | 字段族 | 代表 |
|---|---|---|
| **`model28`**（25） | `mdl28_sm_structural_credit_structural_*` | **`distance_to_default`**、`leverage`、`asset_drift_pct`、`asset_volatility_pct`、`{country,global,industry}_rank` |
| **`model36`**（20） | `credit_risk_*_score_d1`（5）+ `default_risk_*_percentile_d1`（5）+ `star_sr_*`（10） | `coverage_score`、`growth_score`、`leverage_score`、`liquidity_score`、`profitability_score` |
| **`model53`**（22） | `annualized_pd_*_jc7`（10）+ `mdl53_ms*`（10） | **`annualized_pd_{1_month,3_month,6_month,1_year,2_year,…,10_year}_jc7`** |

**★ 机制经济含义**：**Merton 结构化违约模型**（资产漂移 / 资产波动率 / 违约距离）+ 违约概率期限结构。
**这与已有的全部机制都不同** —— 它刻画的是**"公司离违约有多远"**，是信用风险维度。
**⇒ 67 个字段，零测试，机制全新。这是 C 类里最大的一块。**

### ② ★★ 新闻事件 / 情绪（**news17 + news18 + news20 + news50 + news104 = 212 个字段**）

| 数据集 | 字段族 | 代表 |
|---|---|---|
| `news17`（48） | `nws17_*` + `nws17_multiple_*`（23） | `event_sentiment_score`、`event_relevance`、`event_similarity_days`、`analyst_recommendation_change_score` |
| `news18`（70） | `multi_entity_*`（13）+ `nws18_multiple_*`（12） | 同上 + `company_story_headline`、`event_start/end_time_utc` |
| `news20`（46） | 同构（`nws20_*`） | 同上 |
| `news50`（37） | `mws50_*` | `ens`（集成分）、`enc_elapsed` |
| `news104`（11） | — | — |

**★ 机制**：事件情绪 + 事件相关性 + **`event_similarity_days`（相似事件距今几天）** + `analyst_recommendation_change`。
**★ 论坛明确指出：这类另类数据"未被大量 Alpha 使用" ⇒ prod 相关性墙压力小。**

### ③ ★★ 零售关注度 / 人气榜（**sentiment27，18 个字段**）

`snl27_*`：`relpopularity`（相对人气）、`top50pctranking`、`avgranking`、`kurtosis`、`skewness`、`top{pct}pctrankingavg`
**★ 机制**：**零售投资者注意力 / 社交媒体人气排名** —— 经典的 **attention-driven buying** 异象载体。

### ④ ★★ 数字营销 / 电商（**other47 + other250，共 21 个字段**）—— **最"另类"的一族**

| 数据集 | 字段 | 含义 |
|---|---|---|
| **`other47`**（9） | `paid_search_{budget_estimate,terms_count,visitors}`、`organic_{cost,keywords,traffic}`、`rank` | **付费/自然搜索流量与广告投放** —— 公司获客强度的代理 |
| **`other250`**（12） | `product_price_{lower,upper}_bound`、`item_display_price`、`average_star_score`、`item_rating`、`item_review_count`、`price_range_{min,max}` | **商品价格带 + 评分/评论数** —— 电商需求与定价力 |

**★ 机制**：**获客 / 需求侧的另类高频代理**（搜索流量、商品评价）。这类数据的**独特性最高**，与所有既有 alpha 的机制都不同。

### ⑤ ★★ 证券借贷 / 做空（**shortinterest3 + risk60，共 30 个字段**）

| 数据集 | 字段族 | 代表 |
|---|---|---|
| `shortinterest3`（25） | `loan_rate*`（3）、`loaned_{market_value_usd,share_count}`（3）、`{average,max,mean,min}_loan*`（12）、`transaction_count_*`（3） | 借券费率、借出股数、借券交易笔数 |
| `risk60`（5） | `lending_fee_bid_rate`、`rsk60_crowding`、`rsk60_offer` | 融券费率、**拥挤度** |

**★ 机制**：**做空压力 / 借券市场紧张度**（fee 高 = 做空需求强）+ **拥挤度**。
**★ 注**：`mean_loan_rate_main` / `directional_indicator` 的历史高分全是多腿组合（我验证过）。

### ⑥ ★★ 机构资金流（**institutions6 + fund_holdings_panel，共 29 个字段**）

| 数据集 | 字段族 | 代表 |
|---|---|---|
| `institutions6`（11，**MATRIX** cov=1） | `count_institutional_{buyers,holders,sellers}_security`、`market_value_institutional_shares_{acquired,disposed}`、`aggregate_{equity_value,share_count}_{all_owners,institutions}` | **买/卖/持有机构家数** + 增减持市值 |
| `fund_holdings_panel`（18，VECTOR cov 0.88~0.93） | `boundary_transaction_*`（4）、`herfindahl_index_transactions`、`large_trade_count_50bps`、`{top_weighted,stable_boundary,transaction_*}` | 基金交易边界/大额交易/集中度 |

**★ 机制**：**机构被动/主动资金流 + 持仓集中度**（Herfindahl）。
**★ 亮点**：`institutions6` 是 **MATRIX 型**（不需 `vec_*`）且 **cov=1.0** ⇒ **最容易上手的未测池**。

### ⑦ 分析师预期综合分（**model216，45 个全 VECTOR**）

`mdl216_arm{country,global,industry,region}{1,5,100}{rank,score}`、`arm{estimate,preferred,revenue,secondary}revision{component,combination}{rank,score}`、
`armrecommendation{n}rank`
**★ 机制**：ARM（Analyst Revision Model）的**地区/行业相对排位 + 多组件组合分**。
**★ 历史单信号最好 S1.45** —— 但**是 VECTOR，我此前从未用 `vec_avg` 包装测过**。

### ⑧ 其他小池

| 数据集 | 字段 | 机制 |
|---|---|---|
| `other532`（8，MATRIX） | `idiosyncratic_return_{eue,eult}_{daily,monthly}`、`oth532_{emerging,global}_{daily,monthly}_specificreturn` | **特质收益（残差动量）** |
| `model250`（4） | `mdl250_{lmt_close,lmt_open,malta,maltahc}_eq_sector` | 行业相对价值分（刚测 S1.33） |
| `model238`（22） | `mdl238_*_rank` + `{country,industry}_relative_investment_rank`、`global_{change,institutional,peer,screening}_*` | 投资偏好排位（刚测 S1.33） |
| `model30`（10） | `star_new_eps_{analyst_number,smart_estimate,surprise_prediction}_{fq1,fq2,fy1,fy2,12m}` | 智能预期 + 意外预测 |
| `insider_agg_matrix`（2） | `directional_indicator`、`directional_indicator_2` | **内部人方向指标** |
| `analyst47`（1） | `anl47_indicator` | — |
| `analyst48`（7，VECTOR） | `anl48_bulk_*`、`anl48_index_bulk_*` | 索引/批量元数据（疑似无信号） |
| `analyst9`（20） | — | 历史换手 1.36~1.47（**爆表，不可用**） |

---

## 三 结论：优先级（按「机制新颖度 × 字段数 × 上手难度」）

| 优先 | 目标 | 字段 | 类型 | 为什么排这个位置 |
|---|---|---|---|---|
| **1** | **`institutions6`** | 11 | **MATRIX** cov=1 | **唯一 MATRIX + cov=1 的未测池** ⇒ 无需 `vec_*`，最快上手 |
| **2** | **`model28` + `model36` + `model53`** | **67** | MATRIX | **信用/违约风险 = 最大的全新机制族** |
| **3** | **`model216`** | 45 | VECTOR | 历史 S1.45，**只是此前包装错了** ⇒ 最可能翻案 |
| **4** | **`shortinterest3` + `risk60`** | 30 | VECTOR | 做空/借券（M18），有历史高分线索 |
| **5** | **`news17/18/20/50`** | 201 | VECTOR | 全新机制 + **prod 墙压力小** |
| **6** | **`other47` + `other250`** | 21 | VECTOR | **最另类**（搜索流量/电商），独特性最高 |
| **7** | **`sentiment27`** | 18 | VECTOR | 零售注意力 |
| **8** | `fund_holdings_panel` | 18 | VECTOR | 机构交易 |
| **9** | `other532`（特质收益）/ `model250/238`（已测）/ `model30` / `insider_agg_matrix` | ~45 | MATRIX | 小池 |

**★ VECTOR 池的额外搜索维度**：每个字段要先搜 **`vec_*` 聚合算子**（`vec_max` 已验证优于 `vec_avg`），再搜轴深与窗长。

**★ 每开一池的标准流程**：
```
1. get_datafields 拉清单（含 type）→ 按上面这张机制表归类
2. 换手边界筛（TO<0.03 剔除 / >0.7 剔除）
3. VECTOR ⇒ 先搜 vec_* 聚合算子（7 选 1，1 批）
4. 轻框架探针 1 批 → 有无信号
5. 有信号 ⇒ 轴深扫描 + 窗长扫描（找该字段的最优框架）
6. 推进过闸
```
