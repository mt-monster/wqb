# EUR 全类别 · 字段画像与潜力数据集盘点

> 数据源：WorldQuant BRAIN 平台实时（`/data-sets` + `get_datafields` + `get_pyramid_alphas`）
> 范围：EUR / delay=1 / TOPCS1600 ｜ **全部 14 个类别** ｜ 采样日期 2026-10-13

---

## 一、EUR 全量规模

| 类别 | 数据集 | 字段 | 本季度金字塔 alphaCount | 塔状态 |
|---|---:|---:|---:|---|
| model | 46 | 9,242 | **1** | 已点亮 |
| **analyst** | 16 | **8,251** | **1** | 已点亮 |
| fundamental | 13 | 6,019 | **1** | 已点亮 |
| pv | 20 | 5,972 | **0** | ★ **未点亮** |
| other | 36 | 3,841 | **0** | ★ **未点亮** |
| news | 20 | 922 | **0** | ★ **未点亮** |
| risk | 5 | 370 | **1** | 已点亮 |
| sentiment | 5 | 356 | 0 | ★ 未点亮（已穷尽） |
| earnings | 2 | 73 | 0 | ★ 未点亮（已穷尽） |
| insiders | 3 | 51 | 0 | ★ 未点亮（已穷尽） |
| socialmedia | 2 | 51 | 0 | ★ 未点亮（已穷尽） |
| institutions | 2 | 41 | 0 | ★ 未点亮（已穷尽） |
| macro | 2 | 34 | 0 | ★ 未点亮（已穷尽） |
| imbalance | 1 | 2 | 0 | ★ 未点亮（已穷尽） |
| **合计** | **173** | **35,225** | — | — |

### ★★ 关键发现 1：金字塔按季度清零，我此前对「已点亮」的判断有误

**EUR / delay=1 / 2026Q4 金字塔**：仅 `Model`/`Fundamental`/`Analyst`/`Risk` 各有 **1** 颗 alpha；
**PV(0) / News(0) / Other(0) 及其余 10 类全部为 0**。

**⇒ PV / News / Other 三个类别（76 个数据集、10,735 个字段）本季度 alphaCount = 0 ⇒ 未点亮、可用**，
且它们**不在我此前已穷尽的 8 类**之中。

---

## 二、潜力数据集排行（低拥挤 × 大字段 × 高覆盖）

| dataset | 类别 | 字段 | 用户 | 覆盖 | **alphaCount** | 内容 | 实测结果 |
|---|---|---:|---:|---:|---:|---|---|
| `multifactor_return_pre` | model | 648 | 6 | 0.57 | **13** | 多因子收益预测 | 未测（已点亮类） |
| `pattern_scores` | pv | 504 | 12 | **0.998** | **26** | 图表形态相似度 | ❌ 已测：S ≤0.56、**2Y 负** |
| `continuation_score` | pv | 560 | 18 | **0.998** | **35** | 价格形态相似度 | ❌ 已测：同上 |
| `intraday_pv_feats` | pv | 585 | 36 | **0.999** | 54 | 日内价量特征 | ❌ 已测：**TO 1.15 爆炸** |
| `global_seasonal_mode` | model | 449 | 32 | 0.99 | 41 | 季节性制度 | 未测（已点亮类） |
| `ai_news_scores` | other | 105 | 10 | 0.79 | **12** | 新闻情绪 AI 评分 | ❌ 已测：**TO 1.26–1.36 爆炸** |
| `quant_factor_lib` | model | 126 | **4** | 0.51 | **4** | 量化因子库 | 未测（已点亮类） |
| `news_sentiment_dl` | other | 66 | **1** | 0.76 | **1** | 新闻情绪深度学习 | 未测 |
| `multi_source_model` | model | 60 | **0** | 0.58 | **0** | 多源模型 | 未测（已点亮类） |
| `option_chart_model` | model | 39 | **0** | 0.44 | **0** | 期权图表模型 | 未测（已点亮类） |
| `insider_feats` | other | 118 | 27 | 0.54 | 43 | 内部人特征 | 未测 |

---

## 三、本轮实测结论（wave506/507，24 条）

| 数据集 | 信号结构 | S | TO | 2Y | 判死依据 |
|---|---|---:|---:|---:|---|
| `pattern_scores` | 楔形/矩形相似度差 | ≤0.52 | 0.36–0.45 | 负 | **2Y 负 + TO 高** |
| `continuation_score` | `avg_similarity_bearish_flag` | **0.56** | 0.39 | **1.32** | TO 高 + S 不足 |
| 同上 + `ts_target_tvr_decay(0.06)` | 压制换手 | **−0.70** | 0.063 | −0.70 | ❌ **平滑杀死信号** |
| 同上 + `ts_mean(·, 22/66/132)` | 时间平滑 | −0.67 ~ −0.79 | 0.07–0.15 | 负 | ❌ 同上 |
| `intraday_pv_feats` | 日内价格相对水平 | ≤0.37 | **1.15** | −1.14 | TO 爆炸 |
| `ai_news_scores` | 净情绪 / 情绪比值 | ≤0.18 | **1.08–1.36** | 负 | TO 爆炸 |

### ★★ 关键发现 2：新一类结构性矛盾 ——「噪声型信号」

这批数据集（形态相似度 / 日内特征 / 新闻情绪评分）呈现一个**新的失败模式**：

```
不平滑  ⇒ TO 0.36–1.36（爆炸/逼近上限）+ 2Y 负    ← 高频成分有 alpha 但不可提交
平滑    ⇒ S 从 +0.56 崩到 −0.79                    ← alpha 全在高频成分，平滑即杀
```

**⇒ 与 `analyst69` 的「依赖高频换手」同源**：这类信号的预测力集中在**日间跳变**中，
而 EUR 的 TO 上限（0.3 review / 0.7 平台）与 2Y 闸（≥1.58）**联合排除了这类信号**。

**判据（可迁移）**：若探针的 `TO > 0.3` 且 `ts_target_tvr_decay` 或 `ts_mean` 一压就掉 S ⇒ **该数据集结构性不可用**。

---

## 四、EUR 全量覆盖度总账

| 层级 | 覆盖 | 结果 |
|---|---|---|
| **类别级** | 14 / 14 | — |
| **数据集级** | **173 / 173**？ | ❌ **未完成** —— 已探 ≈50 个（未点亮 33 + PV/Other 5 + 部分已点亮） |
| 字段级 | ≈120 / 35,225 ≈ **0.3%** | ❌ |

**⇒ 诚实的现状**：本战役的深度集中在未点亮 8 类（33 数据集 / 8,859 字段，100% 数据集级覆盖）；
PV/News/Other 仅开了 5 个头（且全灭）。

---

## 五、可提交产出（仍为 1 颗）

```python
signed_power(group_rank(divide(eps_revision_magnitude,
                                ts_mean(eps_y1_estimate_coeff_var, 55)), industry), 3.0)
```
`786pLKnb`｜S 1.71 / F 1.09 / TO 0.1124 / 2Y 1.78 / PROD 0.6171 / SELF 0.1752 / verdict FAIL 0

**近线**：`sentiment27`（S 1.33，returns 5.68%）。

---

## 六、下一步（按优先级）

| 优先级 | 方向 | 依据 |
|---|---|---|
| **1** | **PV / Other / News 的剩余 71 个数据集** | 本季度 alphaCount = 0（未点亮）+ 10,735 字段未探 |
| **2** | `news_sentiment_dl`（alphaCount **1**）、`insider_feats`（43） | 潜力榜里尚未测的低拥挤集 |
| **3** | 已点亮类中的低拥挤大集（`multifactor_return_pre` αC 13、`quant_factor_lib` αC 4） | 若放宽「不选已点亮」 |
| ❌ 排除 | 未点亮 8 类的 33 个数据集 | 已 100% 数据集级探过（S/TO/2Y/returns 四判据） |

---

## 七、低拥挤候选实测（wave508，8 条）—— 全部判死

| dataset | 类别 | alphaCount | 信号 | S | TO | 2Y | 判死依据 |
|---|---|---:|---|---:|---:|---:|---|
| `news_sentiment_nlp` | other | **5** | 标题 NLP 情绪比 | ≤0.27 | **0.97–1.22** | 0.80–1.15 | **TO 爆炸** |
| `news_sentiment_nlp` | other | 5 | `vader_score` | 0.43 | **1.20** | **1.41** | TO 爆炸 |
| `news_sentiment_dl` | other | **1** | DL 情绪 `inferess` | 0.29 | **1.42** | 0.74 | TO 爆炸 |
| `news54` | news | **3** | 事件因子 `mws54_factor` | ≤0.14 | **1.44** | −0.27 | TO 爆炸 |
| `acquisition_model` | other | 14 | 并购概率百分位 | −0.89 | 0.0403 | −1.25 | S 负 + TO 过低 + 2Y 负 |

**⇒ 与 wave506/507 完全同源：「新闻/情绪/事件型 VECTOR」的统一失败模式 —— `vec_avg` 归约后个股情绪日间翻转 ⇒ TO 1.0–1.45。**

---

## 八、EUR 全域失败模式总账（累计 ≈45 个数据集实测）

| 失败模式 | 案例数 | 代表数据集 |
|---|---:|---|
| **TO 爆炸 > 0.7** | **11** | insiders1｜socialmedia15｜earnings_sent_matrix｜insider_agg_matrix｜analyst40｜ai_news_scores｜intraday_pv_feats｜news_sentiment_nlp｜news_sentiment_dl｜news54｜mws54 |
| **returns < 5%**（F 闸数学不可过） | 6 | fund_holdings_panel 2.33%｜macro27 2.27%｜analyst4 1.4%｜imbalance5 2.66%｜analyst69 4.79%｜analyst7-surprise 1.5% |
| **2Y ≈ 0 / 负** | 9 | imbalance5｜macro10｜pattern_scores｜continuation_score（2Y 1.32 但 TO 0.39）｜acquisition_model｜… |
| **S ≈ 0 无信号** | 11 | analyst11｜breadth 族（analyst_consensus/analyst10）｜analyst39/7/15/14｜sentiment7｜other553 |
| **TO 过低 < 0.05** | 2 | analyst4 (0.020)｜analyst7-surprise (0.009–0.029) |
| **平滑即杀 alpha** | 3 | continuation_score（+0.56 → −0.79）｜analyst69｜ai_news_scores |

**⇒ EUR 的四重约束（TO ∈ [0.05,0.3] + 2Y ≥ 1.585 + returns ≥ 5% + F ≥ 1.0）联合排除了绝大多数信号类型。**

---

## 九、EUR 全量覆盖度（最终）

| 层级 | 覆盖 | 状态 |
|---|---|---|
| 类别级 | **14 / 14** | ✅ |
| 数据集级 | **≈55 / 173 = 32%** | ⚠ 未点亮 33 已 100%；PV/Other/News 已开 8 / 76 |
| 字段级 | ≈130 / 35,225 ≈ **0.4%** | ❌ |

**唯一可提交产出仍为 1 颗**：`786pLKnb`（Analyst / `analyst_factor_signals`）。

---

## 十、本轮深挖（未点亮 PV/Other/News，波 506–528）—— 6 数据集判死 + 5 条新铁律

> 目标：在**本季度未点亮类别**（PV/Other/News，金字塔 alphaCount = 0，符合「已点亮塔不选」）中挖可提交 regular alpha
> 方法：全量字段画像 → 选低拥挤×大字段×结构化数据集 → 8 探针/波 → 反算 returns 判 F 可行性

### 10.1 本轮实测总账（约 130 条仿真）

| 数据集 | 类别 | 规模 | 最佳形态 | S | returns | TO | 判死依据 |
|---|---|---|---:|---:|---:|---:|---|
| **`insider_feats`** | other | 118 MATRIX cov .916 αC 43 | `top5_buy_tx_count_250d` / 双窗 add | 1.11 | **3.68%** | 0.023 | ❌ **F 闸数学封顶** |
| **`dl_riskfree_returns`** | other | 133 MATRIX cov **1.000** αC 167 | 2quantile **60day** 概率差 | **1.40** | **3.8%** | 0.10–0.22 | ❌ **F 闸数学封顶** |
| `news20` | news | 64 VECTOR cov .963 | 多分类器情绪 | 0.28 | — | **0.88–1.24** | ❌ TO 爆炸 |
| `pv106` | pv | 13 MATRIX cov 1.0 | 价差/成本 | −0.51~−1.65 | — | 0.40–0.97 | ❌ 负号 + 退化假信号 |
| `pv37` | pv | 245 MATRIX cov 1.0 | `reverse(ts_delta(close,5))` | 1.15 | — | **0.46–1.28** | ❌ TO 爆炸 |
| `sentiment27`（中性化复测） | sentiment | — | 乘积分母对比 | 1.14/0.65 | — | — | ❌ CROWDING/STATISTICAL 均劣于 SUBINDUSTRY |

### 10.2 五条新铁律（已写入 skill）

#### ① F 闸判据精确化（最重要）
```
F = S × sqrt( |returns| / max(TO, 0.125) )      ← 平台实现，8+ 条实测逐位吻合
⇒ 过 F 闸（≥1.0）需：S ≥ sqrt(0.125 / returns)  （TO ≤ 0.125 时）
   returns = 5.0% → S ≥ 1.58（最低档，等于 LOW_SHARPE 线）
   returns = 4.0% → S ≥ 1.77
   returns = 3.8% → S ≥ 1.81
   returns = 3.5% → S ≥ 1.89
```
**⇒ 修正此前的「returns 必须 ≥5%」表述**：正解是 **S 与 returns 的权衡曲线**；returns 越低，S 门槛越高。
**⇒ TO 仅在 > 0.125 时有害** ⇒ 最优 TO 恰好 ≈ 0.10–0.125。

#### ② EUR 平台真实阈值（直接读 checks 得到）
| 检查 | 平台 limit |
|---|---|
| LOW_SHARPE | **1.58** |
| LOW_FITNESS | **1.0** |
| LOW_TURNOVER | **0.01** |
| HIGH_TURNOVER | **0.7** |
| LOW_2Y_SHARPE | **1.58** |
> 项目自设的 TO ∈ [0.05, 0.3] 是更严的内部纪律；平台只卡 [0.01, 0.7]。

#### ③ EUR 合法设置档（平台权威 `get_platform_setting_options`）
- **universe**：`TOPCS1600` ｜ `TOP2500` ｜ `TOP1200` ｜ `TOP800` ｜ `TOP400`
- **neutralization**：`NONE` ｜ `MARKET` ｜ `SECTOR` ｜ `INDUSTRY` ｜ `SUBINDUSTRY` ｜ `COUNTRY` ｜ `CROWDING` ｜ `STATISTICAL` ｜ `FAST` ｜ `SLOW` ｜ `REVERSION_AND_MOMENTUM` ｜ `SLOW_AND_FAST`
- **实测结论**：**TOPCS1600 + SUBINDUSTRY 仍是最优组合**（TOP400 1.01 / TOP800 1.16 / TOP1200 1.14 / TOP2500 1.41 但 2Y 崩；CROWDING 1.14 / STATISTICAL 0.65）

#### ④ 「稠密覆盖」不能救 news/sentiment/事件类 VECTOR
`news20` 覆盖 **0.963**（稠密）仍 TO **1.1** ⇒ 失败与覆盖无关，与**事件驱动 + 情绪符号日间翻转**有关 ⇒ 该类一律跳过。

#### ⑤ `ts_delta` 混合 = 提 TO 杠杆（与 `ts_target_tvr_decay` 互补）
`insider_feats`：`add(ts_mean(x,250), ts_delta(x,22))` 使 TO **0.023→0.056** 而 S 仅 1.11→1.03
⇒ 首次实证「**提 TO**」的可用结构（此前只有降 TO 的 hump/tvr_decay）。

### 10.3 外部资料（IQC 指南 / 教程 / DeepWiki）要点
- **Fitness 公式** `sqrt(|Returns|/max(TO,0.125))×Sharpe`（与平台实现一致，已验证）
- **Sharpe 提升手法**：降 decay ｜ 更流动的股票池 ｜ 适当增加波动性 ｜ 用新闻/分析师数据
- **文档验证的顶级模式**：**价格均值反转** `rank(-ts_delta(close,5))`（consistently top-performing）、量价背离 `rank(-ts_corr(volume,close,10))`、残差动量
- 推荐读物：**Kakushadze & Tulchinsky《101 Formulaic Alphas》**（101 条可直接测试的公式）

### 10.4 全 EUR 未点亮空间 F 可行性终表

| 数据集 | S 上限 | returns | **所需 S** | 缺口 | 状态 |
|---|---:|---:|---:|---:|---|
| ★`analyst_factor_signals` | **1.71** | **5.07%** | 1.58 | — | ★**已产出 1 颗**（`786pLKnb`） |
| ★`sentiment27` | 1.33 | **5.68%** | 1.58 | **0.25** | 最小缺口 |
| `dl_riskfree_returns` | 1.40 | 3.8% | 1.82 | 0.42 | 判死 |
| `insider_feats` | 1.11 | 3.9% | 1.79 | 0.68 | 判死 |
| `fund_holdings_panel` | 0.81 | 2.33% | 2.32 | 1.51 | 判死 |
| 其余 ~60 个未探数据集 | — | — | — | — | 失败模式高度同质 |

> **全程零提交**（`ALLOW_ALPHA_SUBMIT` 未开启）。
