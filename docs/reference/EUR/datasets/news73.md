# news73 — EUR 字段画像

> 自动生成于 2026-10-20 17:55　|　[← 返回索引](README.md)

## 一、数据集元信息

| 项 | 值 |
|---|---|
| 数据集 ID | `news73` |
| 名称 | Story by Story Sentiment |
| 类别 | NEWS |
| 数据字段数(平台) | 22 |
| 覆盖率 | 0.813 |
| 平台已有 alpha | 32 |
| valueScore | 2.0 |
| 金字塔倍率 | 1.3 |
| 数据类型 | VECTOR |
| delay | 1 |
| 状态 | scanned |

## 二、数据集描述（平台原文）

> ⚠️ 平台目录描述存在**错配**（已实测：insiders1 / imbalance5 的描述指向无关数据集）。以「五、全字段明细」的真实字段语义为准。

This dataset provides sentiment analysis at the individual news story level, offering granular sentiment scores such as positivity, negativity, fear, financial up/down, hype, volatility, certainty, and uncertainty for each news article. The data is available intraday, daily, and hourly, and covers thousands of securities across major global regions. By tracking sentiment shifts in real time and at high frequency, this dataset enables users to detect market-moving news, gauge investor mood, and anticipate price movements based on the tone and content of news coverage. The detailed entity-level sentiment and volume metrics further enhance predictive modeling for short-term and event-driven trading strategies.

## 三、字段画像汇总

| 维度 | 结果 |
|---|---|
| 字段总数 | **22** |
| 类型分布 | VECTOR×22 |
| 平均覆盖率 | **0.813** |
| 覆盖率区间 | 0.81 ~ 0.81 |
| 更新频率（推断） | 事件/逐笔型（VECTOR） |
| 可用性评级 | 良（覆盖 70–90%，sub/robust 需关注） |

**覆盖率分档**

| 档 | 字段数 | 占比 |
|---|---:|---:|
| 高 (≥0.90) | 0 | 0.0% |
| 中 (0.70–0.90) | 22 | 100.0% |
| 低 (0.50–0.70) | 0 | 0.0% |
| 稀疏 (<0.50) | 0 | 0.0% |

**历史实测分布（field_profile_perf）**

| 判定 | 字段数 | 占比 |
|---|---:|---:|
| UNTESTED | 18 | 81.8% |
| DEAD | 4 | 18.2% |

- 已实测字段：**4** 个（18%），best_sharpe 最高 **0.50**，中位 0.24

## 四、语义维度地图（自动归类）

| 语义族 | 字段数 | 平均覆盖 | 代表字段 |
|---|---:|---:|---|
| 情绪与新闻 | 16 | 0.81 | nws73_globalsent_negativescore、nws73_globalsent_positivescore、nws73_entitiessent_negativepartscr |
| 修正与预期 | 2 | 0.81 | nws73_globalsent_finupscore、nws73_entitiessent_finuppartscr |
| 价量与波动 | 2 | 0.81 | nws73_entitiessent_finvolatilepartscr、nws73_globalsent_finvolatilescore |
| 搜索与替代数据 | 1 | 0.81 | nws73_entitiescounter |
| 风险与质量 | 1 | 0.81 | nws73_entitiessent_finhypepartscr |

## 五、全字段明细

> 按 `best_sharpe` 降序（未测者置后）。`判定` 来自 `field_profile_perf`：ALIVE=历史测出过 S≥闸线（**不代表可提交**）；UNTESTED=未测；UNUSABLE/DEAD/AXIS_ONLY=已证否或仅可作轴。

| # | 字段名 | 类型 | 覆盖 | 语义族 | 测次 | best_S | best_2Y | best_sub | 判定 | 描述 |
|---:|---|---|---:|---|---:|---:|---:|---:|---|---|
| 1 | `nws73_globalsent_negativescore` | VECTOR | 0.813 | 情绪与新闻 | 1 | 0.50 | -0.14 | — | DEAD | Story-level negative sentiment score indicating overall negativity of the article |
| 2 | `nws73_globalsent_finupscore` | VECTOR | 0.813 | 修正与预期 | 1 | 0.24 | 0.68 | — | DEAD | Story-level financial “up/upgrade” sentiment score indicating positive directional financial tone |
| 3 | `nws73_globalsent_positivescore` | VECTOR | 0.813 | 情绪与新闻 | 1 | -0.10 | 0.47 | — | DEAD | Story-level positive sentiment score indicating overall positivity of the article |
| 4 | `nws73_entitiessent_negativepartscr` | VECTOR | 0.813 | 情绪与新闻 | 1 | -0.40 | -0.65 | — | DEAD | List of per-entity negative partial sentiment scores, ordered to entitiesCounter_str |
| 5 | `nws73_djnindustry` | VECTOR | 0.813 | 情绪与新闻 | 0 | — | — | — | UNTESTED | Dow Jones news industry tag(s) |
| 6 | `nws73_djnsubject` | VECTOR | 0.813 | 情绪与新闻 | 0 | — | — | — | UNTESTED | Dow Jones news subject tag(s) |
| 7 | `nws73_entitiescounter` | VECTOR | 0.813 | 搜索与替代数据 | 0 | — | — | — | UNTESTED | Dictionary of recognized financial entities in the story mapped to their mention counts |
| 8 | `nws73_entitiessent_certaintypartscr` | VECTOR | 0.813 | 情绪与新闻 | 0 | — | — | — | UNTESTED | List of per-entity certainty partial sentiment scores, ordered to entitiesCounter_str |
| 9 | `nws73_entitiessent_fearpartscr` | VECTOR | 0.813 | 情绪与新闻 | 0 | — | — | — | UNTESTED | List of per-entity fear partial sentiment scores, ordered to entitiesCounter_str |
| 10 | `nws73_entitiessent_findownpartscr` | VECTOR | 0.813 | 情绪与新闻 | 0 | — | — | — | UNTESTED | List of per-entity financial down/negative directional partial sentiment scores, ordered to entitiesCounter_str |
| 11 | `nws73_entitiessent_finhypepartscr` | VECTOR | 0.813 | 风险与质量 | 0 | — | — | — | UNTESTED | Per-entity Financial Hype partial score vector, aligned with entitiesCounter_str |
| 12 | `nws73_entitiessent_finuppartscr` | VECTOR | 0.813 | 修正与预期 | 0 | — | — | — | UNTESTED | List of per-entity financial up/upgrade partial sentiment scores, ordered to entitiesCounter_str |
| 13 | `nws73_entitiessent_finvolatilepartscr` | VECTOR | 0.813 | 价量与波动 | 0 | — | — | — | UNTESTED | List of per-entity financial volatility partial sentiment scores, ordered to entitiesCounter_str |
| 14 | `nws73_entitiessent_positivepartscr` | VECTOR | 0.813 | 情绪与新闻 | 0 | — | — | — | UNTESTED | List of per-entity positive partial sentiment scores, ordered to entitiesCounter_str |
| 15 | `nws73_entitiessent_uncertaintypartscr` | VECTOR | 0.813 | 情绪与新闻 | 0 | — | — | — | UNTESTED | List of per-entity uncertainty partial sentiment scores, ordered to entitiesCounter_str |
| 16 | `nws73_globalsent_certaintyscore` | VECTOR | 0.813 | 情绪与新闻 | 0 | — | — | — | UNTESTED | Global Certainty score at the article level |
| 17 | `nws73_globalsent_fearscore` | VECTOR | 0.813 | 情绪与新闻 | 0 | — | — | — | UNTESTED | Document-level fear sentiment score |
| 18 | `nws73_globalsent_findownscore` | VECTOR | 0.813 | 情绪与新闻 | 0 | — | — | — | UNTESTED | Global Financial Down score at the article level |
| 19 | `nws73_globalsent_finhypescore` | VECTOR | 0.813 | 情绪与新闻 | 0 | — | — | — | UNTESTED | Global Financial Hype score at the article level (Acuity) |
| 20 | `nws73_globalsent_finvolatilescore` | VECTOR | 0.813 | 价量与波动 | 0 | — | — | — | UNTESTED | Story-level financial volatility sentiment score indicating emphasis on volatility |
| 21 | `nws73_globalsent_uncertaintyscore` | VECTOR | 0.813 | 情绪与新闻 | 0 | — | — | — | UNTESTED | Global Uncertainty score at the article level |
| 22 | `nws73_headlines` | VECTOR | 0.813 | 情绪与新闻 | 0 | — | — | — | UNTESTED | Primary headline text of the story |

## 六、本地回测证据

- 本地累计回测 **4** 条；其中 `ra_failed_checks` 为空的 **0** 条（⚠ 空不等于过关，2Y 为 NULL 者需复检）

| alpha | S | F | 2Y | sub | TO | RA失败数 | wave | 表达式（截断） |
|---|---:|---:|---:|---:|---:|---|---:|---|
| `vRkjbRV3` | 0.50 | 0.16 | -0.14 | — | 0.30 | ["LOW_SHARPE | s2_news73_d1 | `ts_zscore(ts_delta(vec_avg(nws73_globalsent_negativescore), 5), 252)` |
| `rK5jwKXJ` | 0.24 | 0.04 | 0.68 | — | 0.27 | ["LOW_SHARPE | s2_news73_d1 | `group_rank(subtract(vec_avg(nws73_globalsent_finupscore), vec_avg(nws73_globalsent_findown` |
| `blRjglEm` | -0.10 | -0.01 | 0.47 | — | 0.28 | ["LOW_SHARPE | s2_news73_d1 | `rank(subtract(vec_avg(nws73_globalsent_positivescore), vec_avg(nws73_globalsent_negativesc` |
| `e79zP7R6` | -0.40 | -0.11 | -0.65 | — | 0.24 | ["LOW_SHARPE | s2_news73_d1 | `rank(reverse(multiply(vec_avg(nws73_entitiessent_negativepartscr), vec_count(nws73_entitie` |

## 七、判死记录（sealed dead_end）

- `EUR-predictive_starmine-NEWS-MIX-WEAK`（2026-09-04）family=predictive_starmine × news73 sentiment mix：{"best_2y": 1.26, "best_alpha": "9qVLwrOK", "best_fitness": 0.52, "best_sharpe": 1.21, "dataset": "predictive_starmine × news73", "evidence": "wave113 11 条全灭：MODEL×NEWS 配方（surprise 慢腿 × nws73 情绪快腿）整体弱信号，最强候选 S1.21/F0.52/2Y1.26 未达 Mode B 资格线；news73 字段在 EUR TOP2500 覆盖不足或信号弱", "id": "EUR-predictive_starmine-NEWS-MIX-WEAK", "reason": "MODEL×NEWS 跨集混合弱信号：surprise 与 news73 sentiment 相关性不足，组合后 IS 衰减；11 条
- `EUR-news_sentiment_dl-SENTIMENT-WEAK`（2026-09-04）family=news_sentiment_dl sentiment word stats：{"best_2y": 1.36, "best_alpha": "zqY1knoO", "best_fitness": 0.04, "best_sharpe": 0.21, "dataset": "news_sentiment_dl", "evidence": "wave114 9 条全灭：情绪词统计（mean/max/min positive/negative sentiment）在 EUR TOP2500 整体弱信号，最强 S0.38/F0.07/2Y0.63 远低于 Mode B 线；text_complexity 交互项全负；ts_std_dev/ts_delta 快腿全负", "id": "EUR-news_sentiment_dl-SENTIMENT-WEAK", "reason": "news_sentiment_dl 情绪词统计与文本复杂度在 EUR D1 无正向预测力；p

