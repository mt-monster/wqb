# sentiment7 — EUR 字段画像

> 自动生成于 2026-10-20 17:55　|　[← 返回索引](README.md)

## 一、数据集元信息

| 项 | 值 |
|---|---|
| 数据集 ID | `sentiment7` |
| 名称 | Webpage Views  Data |
| 类别 | SENTIMENT |
| 数据字段数(平台) | 24 |
| 覆盖率 | 0.0625 |
| 平台已有 alpha | 65 |
| valueScore | 2.0 |
| 金字塔倍率 | 1.4 |
| 数据类型 | VECTOR |
| delay | 1 |
| 状态 | scanned |

## 二、数据集描述（平台原文）

> ⚠️ 平台目录描述存在**错配**（已实测：insiders1 / imbalance5 的描述指向无关数据集）。以「五、全字段明细」的真实字段语义为准。

This dataset tracks daily Wikipedia page views for a global universe of companies, including both parent entities and their subsidiaries. By aggregating user interest across multiple languages and linking subsidiary activity to parent companies, it provides a unique measure of public attention and sentiment. Spikes or changes in page views can signal increased market interest, news events, or shifts in company visibility, which may precede trading activity or price movements. The dataset is especially useful for generating alternative sentiment signals and for event-driven trading strategies, as it captures real-time shifts in public focus that are not reflected in traditional financial data.

## 三、字段画像汇总

| 维度 | 结果 |
|---|---|
| 字段总数 | **24** |
| 类型分布 | VECTOR×24 |
| 平均覆盖率 | **0.062** |
| 覆盖率区间 | 0.00 ~ 0.50 |
| 更新频率（推断） | 事件/逐笔型（VECTOR） |
| 可用性评级 | 低（覆盖 <50%，仅作条件/分组或放弃） |

**覆盖率分档**

| 档 | 字段数 | 占比 |
|---|---:|---:|
| 高 (≥0.90) | 0 | 0.0% |
| 中 (0.70–0.90) | 0 | 0.0% |
| 低 (0.50–0.70) | 3 | 12.5% |
| 稀疏 (<0.50) | 21 | 87.5% |

**历史实测分布（field_profile_perf）**

| 判定 | 字段数 | 占比 |
|---|---:|---:|
| UNUSABLE | 23 | 95.8% |
| DEAD | 1 | 4.2% |

- 已实测字段：**1** 个（4%），best_sharpe 最高 **0.24**，中位 0.24

## 四、语义维度地图（自动归类）

| 语义族 | 字段数 | 平均覆盖 | 代表字段 |
|---|---:|---:|---|
| 元数据与非信号 | 11 | 0.05 | snt7_timestamp、snt7_all_languagescompany_name_146、snt7_all_languagesexchange_138 |
| 其他 | 6 | 0.17 | snt7_all_languages_views、snt7_views、snt7_all_languagesaccess_type_139 |
| 交易与微观结构 | 3 | 0.00 | snt7_all_languagesticker_142、snt7_all_languagestimestamp_143、snt7ticker_109 |
| 宏观与行业 | 2 | 0.00 | snt7_all_languagescountry_147、snt7country_112 |
| 搜索与替代数据 | 2 | 0.00 | snt7_all_languageswebsite_144、snt7website_113 |

## 五、全字段明细

> 按 `best_sharpe` 降序（未测者置后）。`判定` 来自 `field_profile_perf`：ALIVE=历史测出过 S≥闸线（**不代表可提交**）；UNTESTED=未测；UNUSABLE/DEAD/AXIS_ONLY=已证否或仅可作轴。

| # | 字段名 | 类型 | 覆盖 | 语义族 | 测次 | best_S | best_2Y | best_sub | 判定 | 描述 |
|---:|---|---|---:|---|---:|---:|---:|---:|---|---|
| 1 | `snt7_all_languages_views` | VECTOR | 0.500 | 其他 | 4 | 0.24 | 0.66 | 0.16 | DEAD | Number of views for the company’s Wikipedia page |
| 2 | `snt7_timestamp` | VECTOR | 0.500 | 元数据与非信号 | 0 | — | — | — | UNUSABLE | Content date for which the data were recorded (YYYYMMDD) |
| 3 | `snt7_views` | VECTOR | 0.500 | 其他 | 0 | — | — | — | UNUSABLE | Daily Wikipedia page view count for the specified project and access type |
| 4 | `snt7_all_languagesaccess_type_139` | VECTOR | 0.000 | 其他 | 0 | — | — | — | UNUSABLE | The stock exchange where the company is listed across all languages |
| 5 | `snt7_all_languagescompany_name_146` | VECTOR | 0.000 | 元数据与非信号 | 0 | — | — | — | UNUSABLE | Company name |
| 6 | `snt7_all_languagescountry_147` | VECTOR | 0.000 | 宏观与行业 | 0 | — | — | — | UNUSABLE | ISO Alpha 2 codes for countries in which the companies are incorporated |
| 7 | `snt7_all_languagesexchange_138` | VECTOR | 0.000 | 元数据与非信号 | 0 | — | — | — | UNUSABLE | Exchange code |
| 8 | `snt7_all_languagesisin_145` | VECTOR | 0.000 | 元数据与非信号 | 0 | — | — | — | UNUSABLE | ISIN for the company |
| 9 | `snt7_all_languagesproject_141` | VECTOR | 0.000 | 其他 | 0 | — | — | — | UNUSABLE | The type of access used to view Wikipedia for subsidiaries in the D0 module |
| 10 | `snt7_all_languagesticker_142` | VECTOR | 0.000 | 交易与微观结构 | 0 | — | — | — | UNUSABLE | The timestamp for a data record related to subsidiaries |
| 11 | `snt7_all_languagestimestamp_143` | VECTOR | 0.000 | 交易与微观结构 | 0 | — | — | — | UNUSABLE | The ticker symbol for the company in the D1 module |
| 12 | `snt7_all_languagesviews_148` | VECTOR | 0.000 | 其他 | 0 | — | — | — | UNUSABLE | The name of the company in the D1 module |
| 13 | `snt7_all_languageswebsite_144` | VECTOR | 0.000 | 搜索与替代数据 | 0 | — | — | — | UNUSABLE | The number of views for the Wikipedia pages of subsidiaries in the D0 module |
| 14 | `snt7_company_url_110` | VECTOR | 0.000 | 元数据与非信号 | 0 | — | — | — | UNUSABLE | Company wikipage name |
| 15 | `snt7access_type_104` | VECTOR | 0.000 | 元数据与非信号 | 0 | — | — | — | UNUSABLE | The ISIN for a company across all languages |
| 16 | `snt7company_name_106` | VECTOR | 0.000 | 元数据与非信号 | 0 | — | — | — | UNUSABLE | Company name |
| 17 | `snt7country_112` | VECTOR | 0.000 | 宏观与行业 | 0 | — | — | — | UNUSABLE | ISO Alpha 2 codes for countries in which the companies are incorporated |
| 18 | `snt7exchange_108` | VECTOR | 0.000 | 元数据与非信号 | 0 | — | — | — | UNUSABLE | Exchange code |
| 19 | `snt7isin_103` | VECTOR | 0.000 | 元数据与非信号 | 0 | — | — | — | UNUSABLE | ISIN for the company |
| 20 | `snt7project_105` | VECTOR | 0.000 | 其他 | 0 | — | — | — | UNUSABLE | The specific Wikimedia project (eg, "en.wikipedia") for which data is retrieved |
| 21 | `snt7ticker_109` | VECTOR | 0.000 | 交易与微观结构 | 0 | — | — | — | UNUSABLE | The date of data extraction across all languages |
| 22 | `snt7timestamp_111` | VECTOR | 0.000 | 元数据与非信号 | 0 | — | — | — | UNUSABLE | The type of access used to view Wikipedia in the D1 module |
| 23 | `snt7views_107` | VECTOR | 0.000 | 元数据与非信号 | 0 | — | — | — | UNUSABLE | The ISIN for a company in the D1 module |
| 24 | `snt7website_113` | VECTOR | 0.000 | 搜索与替代数据 | 0 | — | — | — | UNUSABLE | The timestamp for a data record related to subsidiaries in the D0 module |

## 六、本地回测证据

- 本地累计回测 **4** 条；其中 `ra_failed_checks` 为空的 **0** 条（⚠ 空不等于过关，2Y 为 NULL 者需复检）

| alpha | S | F | 2Y | sub | TO | RA失败数 | wave | 表达式（截断） |
|---|---:|---:|---:|---:|---:|---|---:|---|
| `58z3JKXz` | 0.24 | 0.06 | 0.66 | 0.16 | 0.06 | ["LOW_SHARPE | 210 | `rank(ts_delta(ts_mean(ts_backfill(vec_sum(snt7_all_languages_views), 5), 22), 66))` |
| `xA39v7Zw` | 0.06 | 0.01 | — | -0.07 | 0.07 | ["LOW_SHARPE | 210 | `group_rank(multiply(-1, ts_zscore(ts_backfill(vec_sum(snt7_all_languages_views), 5), 66)),` |
| `2rwQ5VgY` | -0.10 | -0.02 | 0.39 | -0.02 | 0.10 | ["LOW_SHARPE | 210 | `rank(multiply(-1, divide(ts_backfill(vec_sum(snt7_all_languages_views), 5), ts_mean(ts_bac` |
| `WjbnlrZP` | -0.15 | -0.03 | 0.50 | 0.00 | 0.11 | ["LOW_SHARPE | 210 | `rank(multiply(-1, ts_zscore(ts_backfill(vec_sum(snt7_all_languages_views), 5), 66)))` |

## 七、判死记录（sealed dead_end）

- `EUR-SNT26-ATTENTION-FITNESS-CEILING`（None）family=sentiment26 网站流行度/投资者注意力族：{"dataset": "sentiment26", "evidence": {"LL9d1JO9": "注意力水平 relpopularity08：S0.90/F0.45/2Y1.75 PASS/TVR0.0929/returns0.0319/longCount1061，仅 2 项 FAIL", "N1QRr0YE": "注意力广度动量 totaldomains：S0.09 无信号", "ZY0Kn563": "top10% 集中度：S-0.84（镜像后 +0.84 仍不达线）"}, "math_proof": "turnover 0.0929 已低于公式下限 0.125，分母钉死 → Fitness_upper = Sharpe_max * sqrt(returns_max/0.125) = 0.90*0.505 = 0.455，实测 0.45 已贴天花板。即使 Sharpe 达 1.
- `EUR-SENTIMENT7-WIKI-ATTENTION-DEAD`（2026-09-19）family=sentiment7 Wikipedia page-view attention (shock reversal / ratio / cap-decile / 66d trend)：{"id": "EUR-SENTIMENT7-WIKI-ATTENTION-DEAD", "dataset": "sentiment7", "wave": 210, "universe": "TOPCS1600", "evidence": "4 probes /S/<=0.24; only 2 usable fields, coverage 0.5", "verdict": "no signal; EUR sentiment tower stays unlit", "rule": "EUR: wiki attention closed"}

