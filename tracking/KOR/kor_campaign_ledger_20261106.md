# KOR 开区战役台账（2026-11-06 起）

> 区域档：KOR / TOP600 / D1 / decay 4 / STATISTICAL / trunc 0.08 / unit VERIFY / nan ON / pasteurization ON / maxTrade OFF
> 门槛实测锚点：`LLZ6wZO2` S 1.99 时 `checks.fail=[]` 且 `LOW_SHARPE` 在 pass 列表 ⇒ **KOR LOW_SHARPE limit ≤ 1.99**（与 EUR/GBR 的 1.58 同档假设，待一条失败件读出确切 limit）。

---

## §1 `institutions6` 迁移失败（wave1 2/2 全灭）

批 `11DL9l5tM4DK8Tf1cvex170r`，两条 2/2 COMPLETE、0 error。

| alpha | 模板 | S | F | TO | 2Y | sub | fRA |
|---|---|---:|---:|---:|---:|---:|---:|
| `qML5kxVv` | T1 = IND `E5VNe67L`(S 3.20) 原款：`rank(-ts_regression(ts_zscore(returns,252), ts_zscore(ts_delay(divide(qty_disposed, add(qty_acq,qty_disposed)),21),252), 252, rettype=0))` | 2.05 | 0.79 | **80.03%** | **−0.56** | 1.36 | 4 |
| `mLoK2mQx` | T2 = IND `KPmvEYeE`(S 3.07) 原款：`rank(-ts_regression(ts_zscore(returns,252), ts_zscore(quantity_institutional_shares_disposed,252), 252, rettype=0))` | 2.06 | 0.80 | **79.95%** | **−0.61** | 1.31 | 4 |

### 判决：KOR × `institutions6` 判死，不再投第二代

**关键归因**：同一套表达式在 IND 是 TO 22.5–25.0% / 2Y 2.36–3.00，在 KOR 变成 TO 80% / 2Y −0.6。
⇒ 差异不在骨架，在**字段的时间序列粒度**：KOR 的 `quantity_institutional_shares_acquired/disposed` 是逐日大幅突变的（申赎事件稀疏 + 大量 0/NaN 交替），
`ts_regression` 对二阶噪声极其敏感，相关系数日间翻转 ⇒ 持仓天天翻仓 ⇒ TO 80%。

**这不是「该加平滑」的问题，是字段不适配回归骨架**。两条 2Y 为负说明近两年效应反向，即使压住 TO 也过不了 `LOW_2Y_SHARPE`。
**封盘理由**：TO 与 2Y 双杀，且两周前效应反向 ⇒ 机制在 KOR 不成立。

---

## §2 `news79`（RavenPack）模板池 —— 10 个结构互异模板

**数据集画像**（`get_datafields` 实读，KOR/TOP600/D1）：全部 **VECTOR**，须 `vec_avg()` 包裹后做算术。
cov 0.73–0.92（远高于 metadata `coverage` 不可信区）。已确认存在且有经济含义的字段：

| 字段 | cov | aC | 含义 |
|---|---:|---:|---|
| `nws79_composite_sentiment_score` | 0.869 | 13 | 文档综合情绪 −1..+1（2 位小数） = 论坛所称 `ssc` |
| `nws79_document_sentiment_confidence` | 0.869 | 10 | 情绪置信度 0..1 |
| `nws79_credit_sentiment` | 0.729 | 74 | 事件对企业**信用度**的影响 −1..+1 |
| `nws79_earnings_release_sentiment` | 0.869 | 17 | 财报类新闻情绪 = 基本面新闻 |
| `nws79_earnings_tone_sentiment` | 0.869 | 35 | 财报评价语调 |
| `nws79_analyst_ratings_sentiment` | 0.869 | 28 | 分析师评级变动情绪 −1/0/+1 |
| `nws79_corporate_actions_sentiment` | 0.869 | 7 | 公司行为类新闻情绪 |
| `nws79_commentary_sentiment` | 0.869 | 10 | 短评类情绪 |
| `nws79_document_sentiment` | 0.869 | 33 | 文档整体情绪 |
| `nws79_entity_detection_distance` | 0.869 | 35 | 实体被检出距离（0=直接）⇒ **relevance 反向代理** |
| `nws79_document_type_189` | 0.92 | 9 | 文档类型（>600 类）⇒ 基本面新闻过滤器 |

### 模板来源留痕

| 来源 | 内容 |
|---|---|
| 论坛帖 `42659817284375`（WL27618，31 票，《新闻情绪因子：别再用裸 sentiment 了》） | 套路一 relevance 加权；套路二 新颖度过滤（`event_similarity_days × sentiment`）；套路三 情绪动量用变化类字段（`ghc_lna`）配 `ts_decay_linear`/`ts_target_tvr_decay`；进阶：多公司聚合族 + Story Attention Dilution + Entity-Story Deviation |
| 论坛帖 `18641983716503`（ML13205，《The Momentum of News》） | 论文 Wang/Zhang/Zhu (2018), SSRN 3267337：`a=ts_mean(sentiment,5)` → `group_rank(a, subindustry)`，`trade_when(vec_avg(relevance)>0.1, ...)`；年化 7.45% 风险调整超额 |
| 论坛帖 `34321840027799`（SP74109，《基本面新闻情绪反转因子》） | 中泰证券《寻找另类Alpha因子系列之一》+ 财通证券《在下跌中寻找惊喜》：① 用**综合**情绪分（css）不用单事件分（ess）；② 基本面三类等权合成 `earnings + revenue + dividends`；③ **`ts_arg_min(X, 240)` 定位情绪底部**，实测 d=240 远强于 30/60/180；④ `trade_when(ts_corr(close,volume,5)>0.5)` 做噪声过滤 |

### 10 个结构互异模板（差异落在骨架 / 算子几何 / 矩 / 分组轴 / 非线性）

| # | 模板名 | 骨架 | 算子数 | 机制来源 | 状态 |
|---|---|---|---:|---|---|
| N1 | 置信度加权水平惊奇 | `group_rank(ts_zscore(multiply(vec_avg(css), vec_avg(conf)), 252), sector)` | 5 | 自建（`ts_zscore`=SUE 式标准化惊奇） | **已派 wave2** |
| N2 | 信贷情绪慢变水平 | `group_rank(ts_rank(vec_avg(credit), 504), sector)` | 3 | 自建（信用质量漂移，慢变量用长窗分位） | **已派 wave2** |
| N3 | Relevance 加权情绪 | `group_rank(ts_mean(divide(vec_avg(css), add(vec_avg(distance), 1)), 22), sector)` | 6 | 论坛 `42659817284375` 套路一 | **已派 wave3** |
| N4 | 情绪底部定位 | `group_rank(ts_arg_min(vec_avg(earnings_rel), 240), sector)` | 3 | 论坛 `34321840027799` + 中泰/财通研报（d=240 实证最优） | **已派 wave3** |
| N5 | 情绪动量 5 日 + relevance 门控 | `group_rank(ts_mean(vec_avg(css), 5), sector)`（门控版需 `trade_when`，算子超 12 待压缩） | 3 | 论文 Wang/Zhang/Zhu 2018 + 论坛 `18641983716503` | 待派 |
| N6 | 基本面新闻三合一 | `group_rank(ts_mean(add(add(vec_avg(earnings_rel), vec_avg(corp_act)), vec_avg(analyst_ratings)), 66), sector)` | 7 | 论坛 `34321840027799` 的 css 三合一 | 待派 |
| N7 | 情绪分歧度（二阶矩） | `group_rank(reverse(ts_std_dev(vec_avg(css), 66)), sector)` | 6 | 自建（不确定性折价） | 待派 |
| N8 | 情绪-价格背离 | `group_rank(reverse(ts_corr(vec_avg(css), close, 66)), sector)` | 6 | 论坛《情绪数据中用 ts_covariance 构建 alpha 模板》 | 待派 |
| N9 | 文档 vs 财报语调偏离 | `group_rank(subtract(ts_mean(vec_avg(doc_sent),66), ts_mean(vec_avg(earnings_tone),66)), sector)` | 7 | 论坛 `42659817284375` Entity-Story Deviation | 待派 |
| N10 | 情绪加速度（二阶差分） | `group_rank(ts_delta(ts_mean(vec_avg(css), 22), 22), sector)` | 5 | 自建 | 待派 |
| N11 | 分析师评级变动情绪 | `group_rank(ts_zscore(vec_avg(analyst_ratings), 252), sector)` | 5 | 自建（评级修订面，与 N6 不同维度） | 待派 |

**多样性自检**：11 个模板，维度覆盖 水平(N1/N2/N11) / 动量(N5/N10) / 底部定位(N4) / 分歧(N7) / 共动(N8) / 偏离(N9) / 加权(N3) / 合成(N6)，
骨架落在 `ts_zscore` / `ts_rank` / `ts_mean` / `ts_arg_min` / `ts_std_dev` / `ts_corr` / `ts_delta` / `subtract` 八种不同算子几何上 ⇒ 满足 ≥10 且结构互异。

---

## §2b news79 三波 4 模板全部结案 → **判死**

| alpha | 模板 | S | F | TO | 2Y | sub | fRA | preScreen |
|---|---|---:|---:|---:|---:|---:|---:|---|
| `1YNG1kRJ` | N1 置信度加权水平惊奇（`ts_zscore(multiply(css,conf),252)`） | 0.60 | 0.16 | **41.37%** | 1.28 | 0.68 | 4 | REJECT |
| `E56mYOMG` | N2 信贷情绪慢变水平（`ts_rank(credit,504)`） | 0.11 | 0.01 | **43.26%** | 0.57 | 0.18 | 4 | REJECT |
| `E56m0nO0` | N3 Relevance 加权（`ts_mean(css/(1+distance),22)`） | 0.77 | 0.39 | 11.66% | 0.39 | 0.98 | 3 | REJECT |
| `d5W98Jkj` | N4 情绪底部定位（`ts_arg_min(earnings_rel,240)`） | 0.48 | 0.19 | 8.09% | −0.95 | 0.30 | 3 | REJECT |

### 判决理由（三条独立证据）

1. **四个结构互异模板**（水平二阶矩标准化 / 长窗分位 / relevance 加权 / 底部定位），算子几何覆盖 `ts_zscore`/`ts_rank`/`ts_mean`+`divide`/`ts_arg_min`，**最大 |S| 仅 0.77**，距 KOR 门槛 ~1.58 差 0.81。
2. **TO 谱系两档同时出现，各对应一种死法**：
   - N1/N2 的 TO **41–43%** ⇒ 落「高频刷新噪声描述符」档（与 HKG `news_sentiment_transfer` 42–50% / `other553` 45–47% **同一档位**）⇒ 日频聚合的新闻情绪在日频上就是噪声。
   - N3/N4 的 TO **8–12%** ⇒ 落「常规有效区」，**说明字段有真实信号、只是太弱**，不是骨架选错。
3. **与 HKG 交叉印证**：新闻情绪族在两个区域都死在「TO 41–50% + |S|<0.8」或「TO 健康但 |S|<0.8」。
   ⇒ 这是**新闻情绪类字段在本平台 KR/HK 小盘宇宙的普遍属性**，不是 KOR 特有的。

### 处置

**KOR · news79 判死，不投第二代。** 剩余 N5–N11 不再派发（同一字段、同一刷新率，换骨架救不了）。
KOR 战役剩余可动资产只有 `LLZ6wZO2`（OTHER ATOM，S 1.99 / self 0.676 / prod 0.6762）。
⇒ **KOR 降为副战场**；KOR 的 47 个零塔数据集里，NEWS / INSTITUTIONS 两面已证死，
后续若回 KOR，应改攻 **RISK（`risk88` 64 字段 / cov 0.973）** 或 **EARNINGS / INSIDERS**，且必须先做低 TO 构造（避免 40%+ 刷新率档）。

---

## §3 塔位影响

KOR 塔位现状（`get_pyramid_alphas`）：已点亮 shortinterest(4)/fundamental(3)/model(3)；
**未点亮 12 档**：analyst(2)/pv(2)/other(1) + earnings/imbalance/insiders/institutions/macro/news/socialmedia/risk/sentiment(0)。
`news79` 属 **NEWS**，是 KOR 的 0 塔 ⇒ 出货即点亮；且它是**单数据集 ATOM，不占塔混配额**。