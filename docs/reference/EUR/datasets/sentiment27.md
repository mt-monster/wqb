# sentiment27 — EUR 字段画像

> 自动生成于 2026-10-20 17:55　|　[← 返回索引](README.md)

## 一、数据集元信息

| 项 | 值 |
|---|---|
| 数据集 ID | `sentiment27` |
| 名称 | Website Popularity Rankings |
| 类别 | SENTIMENT |
| 数据字段数(平台) | 30 |
| 覆盖率 | 0.9427 |
| 平台已有 alpha | 1154 |
| valueScore | 2.0 |
| 金字塔倍率 | 1.4 |
| 数据类型 | — |
| delay | 1 |
| 状态 | — |

## 二、数据集描述（平台原文）

> ⚠️ 平台目录描述存在**错配**（已实测：insiders1 / imbalance5 的描述指向无关数据集）。以「五、全字段明细」的真实字段语义为准。

This dataset provides a robust, research-oriented ranking of the most popular websites worldwide, designed to be resistant to manipulation and volatility. It aggregates and harmonizes data from multiple sources, including DNS traffic, browser extensions, and web crawls, to produce a stable and reproducible list of top domains. The dataset includes detailed metrics such as relative popularity, ranking intervals, domain counts, and statistical measures like skewness and kurtosis. By mapping domains to standardized identifiers, it enables aggregation and analysis at various levels. This dataset is valuable for predicting price movements by identifying trends in web traffic, shifts in user behavior, and the emergence of influential domains, which can signal changes in market sentiment, consume

## 三、字段画像汇总

| 维度 | 结果 |
|---|---|
| 字段总数 | **30** |
| 类型分布 | VECTOR×30 |
| 平均覆盖率 | **0.943** |
| 覆盖率区间 | 0.75 ~ 1.00 |
| 更新频率（推断） | 事件/逐笔型（VECTOR） |
| 可用性评级 | 优（覆盖 ≥90%，可直接做尽） |

**覆盖率分档**

| 档 | 字段数 | 占比 |
|---|---:|---:|
| 高 (≥0.90) | 26 | 86.7% |
| 中 (0.70–0.90) | 4 | 13.3% |
| 低 (0.50–0.70) | 0 | 0.0% |
| 稀疏 (<0.50) | 0 | 0.0% |

**历史实测分布（field_profile_perf）**

| 判定 | 字段数 | 占比 |
|---|---:|---:|
| UNTESTED | 30 | 100.0% |

- 该数据集全部字段**尚未实测**（UNTESTED）⇒ 优先做尽

## 四、语义维度地图（自动归类）

| 语义族 | 字段数 | 平均覆盖 | 代表字段 |
|---|---:|---:|---|
| 风险与质量 | 17 | 0.92 | snt27_avgranking、snt27_top50pctranking、snt27_top50pctrankingavg |
| 其他 | 4 | 0.98 | snt27_relpopularity08、snt27_relpopularity1、snt27_totaldomains |
| 宏观与行业 | 3 | 0.97 | snt27_dltcc、snt27_totalcountrydomains、snl27_totalcountrydomains |
| 搜索与替代数据 | 3 | 0.97 | snt27_website、snt27_wq_pit、snl27_wq_pit |
| 情绪与新闻 | 2 | 0.91 | snl27_relpopularity08、snl27_relpopularity1 |
| 元数据与非信号 | 1 | 1.00 | snt27_new_atlas_domain |

## 五、全字段明细

> 按 `best_sharpe` 降序（未测者置后）。`判定` 来自 `field_profile_perf`：ALIVE=历史测出过 S≥闸线（**不代表可提交**）；UNTESTED=未测；UNUSABLE/DEAD/AXIS_ONLY=已证否或仅可作轴。

| # | 字段名 | 类型 | 覆盖 | 语义族 | 测次 | best_S | best_2Y | best_sub | 判定 | 描述 |
|---:|---|---|---:|---|---:|---:|---:|---:|---|---|
| 1 | `snt27_avgranking` | VECTOR | 1.000 | 风险与质量 | 0 | — | — | — | UNTESTED | Average of rankings |
| 2 | `snt27_dltcc` | VECTOR | 1.000 | 宏观与行业 | 0 | — | — | — | UNTESTED | Country code TLD |
| 3 | `snt27_new_atlas_domain` | VECTOR | 1.000 | 元数据与非信号 | 0 | — | — | — | UNTESTED | Cleaned domain name |
| 4 | `snt27_relpopularity08` | VECTOR | 1.000 | 其他 | 0 | — | — | — | UNTESTED | Relative popularity calculated with alpha=0.8 |
| 5 | `snt27_relpopularity1` | VECTOR | 1.000 | 其他 | 0 | — | — | — | UNTESTED | Relative popularity calculated with alpha=1 |
| 6 | `snt27_top50pctranking` | VECTOR | 1.000 | 风险与质量 | 0 | — | — | — | UNTESTED | The top 50% percentile ranking |
| 7 | `snt27_top50pctrankingavg` | VECTOR | 1.000 | 风险与质量 | 0 | — | — | — | UNTESTED | The average ranking of the top 50% percentile |
| 8 | `snt27_top75pctranking` | VECTOR | 1.000 | 风险与质量 | 0 | — | — | — | UNTESTED | The top 75% percentile ranking |
| 9 | `snt27_top75pctrankingavg` | VECTOR | 1.000 | 风险与质量 | 0 | — | — | — | UNTESTED | The average ranking of the top 75% percentile |
| 10 | `snt27_topranking` | VECTOR | 1.000 | 风险与质量 | 0 | — | — | — | UNTESTED | The top ranking |
| 11 | `snt27_totalcountrydomains` | VECTOR | 1.000 | 宏观与行业 | 0 | — | — | — | UNTESTED | Total number of country-code TLDs |
| 12 | `snt27_totaldomains` | VECTOR | 1.000 | 其他 | 0 | — | — | — | UNTESTED | Total number of sub-domains |
| 13 | `snt27_website` | VECTOR | 1.000 | 搜索与替代数据 | 0 | — | — | — | UNTESTED | name of the website |
| 14 | `snt27_wq_pit` | VECTOR | 1.000 | 搜索与替代数据 | 0 | — | — | — | UNTESTED | For ongoing data it is wq_append_time, for history data it simulated from PIT simulation field in the MCD input settings. MCD builder can di |
| 15 | `snt27_rank` | VECTOR | 0.927 | 风险与质量 | 0 | — | — | — | UNTESTED | Daily popularity rank of the domain in Tranco, 1 = most popular |
| 16 | `snl27_avgranking` | VECTOR | 0.914 | 风险与质量 | 0 | — | — | — | UNTESTED | Arithmetic mean of the Tranco ranks across all domains mapped to the issuer on that date; lower values indicate higher overall popularity |
| 17 | `snl27_relpopularity08` | VECTOR | 0.914 | 情绪与新闻 | 0 | — | — | — | UNTESTED | Composite relative popularity score computed with alpha=0.8; higher values indicate broader attention across the issuer’s domains |
| 18 | `snl27_relpopularity1` | VECTOR | 0.914 | 情绪与新闻 | 0 | — | — | — | UNTESTED | Composite relative popularity score computed with alpha=1; higher values indicate broader attention across the issuer’s domains |
| 19 | `snl27_top50pctranking` | VECTOR | 0.914 | 风险与质量 | 0 | — | — | — | UNTESTED | 50th-percentile (median) rank cutoff of the issuer’s domain rank distribution; lower is better |
| 20 | `snl27_top50pctrankingavg` | VECTOR | 0.914 | 风险与质量 | 0 | — | — | — | UNTESTED | Average rank within the top 50% (best half) of the issuer’s domain rank distribution |
| 21 | `snl27_top75pctranking` | VECTOR | 0.914 | 风险与质量 | 0 | — | — | — | UNTESTED | 75th-percentile rank cutoff of the issuer’s domain rank distribution; lower is better |
| 22 | `snl27_top75pctrankingavg` | VECTOR | 0.914 | 风险与质量 | 0 | — | — | — | UNTESTED | Average rank within the top 75% of the issuer’s domain rank distribution |
| 23 | `snl27_topranking` | VECTOR | 0.914 | 风险与质量 | 0 | — | — | — | UNTESTED | Best (lowest) rank among the issuer’s domains on that date |
| 24 | `snl27_totalcountrydomains` | VECTOR | 0.914 | 宏观与行业 | 0 | — | — | — | UNTESTED | Number of domains associated with the issuer that have a country-code TLD (ccTLD) or regional identifier |
| 25 | `snl27_totaldomains` | VECTOR | 0.914 | 其他 | 0 | — | — | — | UNTESTED | Total number of distinct domains associated with the issuer on that date (de-duplicated count) |
| 26 | `snl27_wq_pit` | VECTOR | 0.914 | 搜索与替代数据 | 0 | — | — | — | UNTESTED | Internal PIT alignment marker (wq_append_time for ongoing data or simulated for historical), used for point-in-time decoding/stitching; not  |
| 27 | `snt27_kurtosis` | VECTOR | 0.897 | 风险与质量 | 0 | — | — | — | UNTESTED | Kurtosis of ranking |
| 28 | `snt27_skewness` | VECTOR | 0.897 | 风险与质量 | 0 | — | — | — | UNTESTED | Skewness of ranking |
| 29 | `snl27_kurtosis` | VECTOR | 0.754 | 风险与质量 | 0 | — | — | — | UNTESTED | Excess kurtosis of the issuer’s domain rank distribution, indicating tail heaviness/extremes |
| 30 | `snl27_skewness` | VECTOR | 0.754 | 风险与质量 | 0 | — | — | — | UNTESTED | Skewness of the issuer’s domain rank distribution, indicating asymmetry/concentration |

## 六、本地回测证据

本地库无该数据集的回测记录。

> 说明：`backtest_results` 只收录已持久化的波次（当前 EUR 共 1157 行）；本次会话的直接派发未写库，故此处为空**不代表未做尽**，实测结论见配套战役档案。

## 七、判死记录（sealed dead_end）

无针对本数据集的 `dead_end` 记录。

