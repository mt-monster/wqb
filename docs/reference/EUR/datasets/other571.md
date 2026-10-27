# other571 — EUR 字段画像

> 自动生成于 2026-10-20 17:55　|　[← 返回索引](README.md)

## 一、数据集元信息

| 项 | 值 |
|---|---|
| 数据集 ID | `other571` |
| 名称 | Wikipedia Viewing Data |
| 类别 | OTHER |
| 数据字段数(平台) | 30 |
| 覆盖率 | 0.7585 |
| 平台已有 alpha | 61 |
| valueScore | 4.0 |
| 金字塔倍率 | 1.5 |
| 数据类型 | MATRIX |
| delay | 1 |
| 状态 | scanned |

## 二、数据集描述（平台原文）

> ⚠️ 平台目录描述存在**错配**（已实测：insiders1 / imbalance5 的描述指向无关数据集）。以「五、全字段明细」的真实字段语义为准。

This dataset tracks daily Wikipedia pageviews for companies across a global universe, capturing user interest and information-seeking behavior. By aggregating and transforming raw pageview data into structured fields, it enables researchers to analyze trends in public attention, which can serve as a proxy for retail investor sentiment or information demand. The use of natural days (including weekends and holidays) ensures comprehensive coverage and more robust time series analysis. Spikes or sustained increases in pageviews may precede or coincide with significant price movements, making this dataset valuable for predicting market activity, especially around news events or periods of heightened public interest.

## 三、字段画像汇总

| 维度 | 结果 |
|---|---|
| 字段总数 | **30** |
| 类型分布 | MATRIX×30 |
| 平均覆盖率 | **0.758** |
| 覆盖率区间 | 0.70 ~ 0.78 |
| 更新频率（推断） | 日频 |
| 可用性评级 | 良（覆盖 70–90%，sub/robust 需关注） |

**覆盖率分档**

| 档 | 字段数 | 占比 |
|---|---:|---:|
| 高 (≥0.90) | 0 | 0.0% |
| 中 (0.70–0.90) | 30 | 100.0% |
| 低 (0.50–0.70) | 0 | 0.0% |
| 稀疏 (<0.50) | 0 | 0.0% |

**历史实测分布（field_profile_perf）**

| 判定 | 字段数 | 占比 |
|---|---:|---:|
| UNTESTED | 25 | 83.3% |
| DEAD | 4 | 13.3% |
| DEAD_STATIC | 1 | 3.3% |

- 已实测字段：**5** 个（17%），best_sharpe 最高 **0.58**，中位 -0.22

## 四、语义维度地图（自动归类）

| 语义族 | 字段数 | 平均覆盖 | 代表字段 |
|---|---:|---:|---|
| 其他 | 24 | 0.76 | oth571_views7d、oth571_views7dafternoon、oth571_views7ddesktop |
| 搜索与替代数据 | 6 | 0.75 | oth571_views28ddesktop、oth571_views28dmobile、oth571_viewstodaydesktop |

## 五、全字段明细

> 按 `best_sharpe` 降序（未测者置后）。`判定` 来自 `field_profile_perf`：ALIVE=历史测出过 S≥闸线（**不代表可提交**）；UNTESTED=未测；UNUSABLE/DEAD/AXIS_ONLY=已证否或仅可作轴。

| # | 字段名 | 类型 | 覆盖 | 语义族 | 测次 | best_S | best_2Y | best_sub | 判定 | 描述 |
|---:|---|---|---:|---|---:|---:|---:|---:|---|---|
| 1 | `oth571_views7d` | MATRIX | 0.781 | 其他 | 4 | 0.58 | 1.26 | — | DEAD | Total Wikipedia page views over the past 7 natural days. |
| 2 | `oth571_views7dafternoon` | MATRIX | 0.781 | 其他 | 2 | -0.20 | 1.27 | — | DEAD | Wikipedia company page views in the USA module from 12:00 to 17:59 on the day 7 days ago (module timezone) |
| 3 | `oth571_views7ddesktop` | MATRIX | 0.781 | 其他 | 1 | -0.22 | 1.17 | — | DEAD_STATIC | Wikipedia page views from desktop devices over the past 7 natural days. |
| 4 | `oth571_views28d` | MATRIX | 0.776 | 其他 | 1 | -0.24 | 1.09 | — | DEAD | Total Wikipedia company page views in the USA module over the trailing 28-day window ending 28 days ago (inclusive; modu |
| 5 | `oth571_views1y` | MATRIX | 0.701 | 其他 | 1 | -0.25 | 1.01 | — | DEAD | Total Wikipedia company page views in the USA module over the trailing 365-day window (366 in leap years) ending 364 day |
| 6 | `oth571_views7devening` | MATRIX | 0.781 | 其他 | 0 | — | — | — | UNTESTED | Wikipedia company page views in the USA module from 18:00 to 23:59 on the day 7 days ago (module timezone) |
| 7 | `oth571_views7dmobile` | MATRIX | 0.781 | 其他 | 0 | — | — | — | UNTESTED | Wikipedia page views from mobile devices over the past 7 natural days. |
| 8 | `oth571_views7dmorning` | MATRIX | 0.781 | 其他 | 0 | — | — | — | UNTESTED | Wikipedia company page views in the USA module from 06:00 to 11:59 on the day 7 days ago (module timezone) |
| 9 | `oth571_views7dnight` | MATRIX | 0.781 | 其他 | 0 | — | — | — | UNTESTED | Wikipedia company page views in the USA module from 00:00 to 05:59 on the day 7 days ago (module timezone) |
| 10 | `oth571_views14d` | MATRIX | 0.779 | 其他 | 0 | — | — | — | UNTESTED | Total Wikipedia company page views in the USA module over the trailing 14-day window ending 14 days ago (inclusive; modu |
| 11 | `oth571_views28dafternoon` | MATRIX | 0.776 | 其他 | 0 | — | — | — | UNTESTED | Wikipedia company page views in the USA module from 12:00 to 17:59 on the day 28 days ago (module timezone) |
| 12 | `oth571_views28ddesktop` | MATRIX | 0.776 | 搜索与替代数据 | 0 | — | — | — | UNTESTED | Total Wikipedia company page views in the USA module via desktop devices on the day 28 days ago (desktop web; module tim |
| 13 | `oth571_views28devening` | MATRIX | 0.776 | 其他 | 0 | — | — | — | UNTESTED | Wikipedia company page views in the USA module from 18:00 to 23:59 on the day 28 days ago (module timezone) |
| 14 | `oth571_views28dmobile` | MATRIX | 0.776 | 搜索与替代数据 | 0 | — | — | — | UNTESTED | Total Wikipedia company page views in the USA module via mobile devices on the day 28 days ago (mobile web and apps; mod |
| 15 | `oth571_views28dmorning` | MATRIX | 0.776 | 其他 | 0 | — | — | — | UNTESTED | Wikipedia company page views in the USA module from 06:00 to 11:59 on the day 28 days ago (module timezone) |
| 16 | `oth571_views28dnight` | MATRIX | 0.776 | 其他 | 0 | — | — | — | UNTESTED | Wikipedia company page views in the USA module from 00:00 to 05:59 on the day 28 days ago (module timezone) |
| 17 | `oth571_viewstoday` | MATRIX | 0.773 | 其他 | 0 | — | — | — | UNTESTED | Total Wikipedia company page views in the USA module today (calendar day; module timezone) |
| 18 | `oth571_viewstodayafternoon` | MATRIX | 0.773 | 其他 | 0 | — | — | — | UNTESTED | Wikipedia company page views in the USA module from 12:00 to 17:59 today (module timezone) |
| 19 | `oth571_viewstodaydesktop` | MATRIX | 0.773 | 搜索与替代数据 | 0 | — | — | — | UNTESTED | Total Wikipedia company page views in the USA module via desktop devices today (desktop web; module timezone) |
| 20 | `oth571_viewstodayevening` | MATRIX | 0.773 | 其他 | 0 | — | — | — | UNTESTED | Wikipedia company page views in the USA module from 18:00 to 23:59 today (module timezone) |
| 21 | `oth571_viewstodaymobile` | MATRIX | 0.773 | 搜索与替代数据 | 0 | — | — | — | UNTESTED | Total Wikipedia company page views in the USA module via mobile devices today (mobile web and apps; module timezone) |
| 22 | `oth571_viewstodaymorning` | MATRIX | 0.773 | 其他 | 0 | — | — | — | UNTESTED | Wikipedia company page views in the USA module from 06:00 to 11:59 today (module timezone) |
| 23 | `oth571_viewstodaynight` | MATRIX | 0.773 | 其他 | 0 | — | — | — | UNTESTED | Wikipedia company page views in the USA module from 00:00 to 05:59 today (module timezone) |
| 24 | `oth571_views84d` | MATRIX | 0.763 | 其他 | 0 | — | — | — | UNTESTED | Total Wikipedia company page views in the USA module over the trailing 84-day window ending 84 days ago (inclusive; modu |
| 25 | `oth571_views1yafternoon` | MATRIX | 0.701 | 其他 | 0 | — | — | — | UNTESTED | Wikipedia company page views in the USA module from 12:00 to 17:59 on the day 364 days ago (module timezone) |
| 26 | `oth571_views1ydesktop` | MATRIX | 0.701 | 搜索与替代数据 | 0 | — | — | — | UNTESTED | Total Wikipedia company page views in the USA module via desktop devices on the day 364 days ago (desktop web; module ti |
| 27 | `oth571_views1yevening` | MATRIX | 0.701 | 其他 | 0 | — | — | — | UNTESTED | Wikipedia company page views in the USA module from 18:00 to 23:59 on the day 364 days ago (module timezone) |
| 28 | `oth571_views1ymobile` | MATRIX | 0.701 | 搜索与替代数据 | 0 | — | — | — | UNTESTED | Total Wikipedia company page views in the USA module via mobile devices on the day 364 days ago (mobile web and apps; mo |
| 29 | `oth571_views1ymorning` | MATRIX | 0.701 | 其他 | 0 | — | — | — | UNTESTED | Wikipedia company page views in the USA module from 06:00 to 11:59 on the day 364 days ago (module timezone) |
| 30 | `oth571_views1ynight` | MATRIX | 0.701 | 其他 | 0 | — | — | — | UNTESTED | Wikipedia company page views in the USA module from 00:00 to 05:59 on the day 364 days ago (module timezone) |

## 六、本地回测证据

- 本地累计回测 **9** 条；其中 `ra_failed_checks` 为空的 **9** 条（⚠ 空不等于过关，2Y 为 NULL 者需复检）

| alpha | S | F | 2Y | sub | TO | RA失败数 | wave | 表达式（截断） |
|---|---:|---:|---:|---:|---:|---|---:|---|
| `JjxZzqje` | 0.58 | 0.09 | -0.61 | — | 0.67 | 0 | 119 | `if_else(ts_delta(oth571_views7d, 5) > 0, rank(oth571_views7d), rank(reverse(oth571_views7d` |
| `9qVLMYZV` | -0.19 | -0.05 | 1.26 | — | 0.06 | 0 | 119 | `rank(zscore(oth571_views7d))` |
| `QP3LNwkp` | -0.20 | -0.05 | 1.27 | — | 0.08 | 0 | 119 | `rank(zscore(oth571_views7dafternoon))` |
| `om6MG7m5` | -0.22 | -0.06 | 1.21 | — | 0.02 | 0 | 119 | `rank(ts_decay_linear(oth571_views7d, 21))` |
| `N1QvJYvq` | -0.22 | -0.06 | 1.17 | — | 0.01 | 0 | 119 | `rank(ts_mean(oth571_views7ddesktop, 66))` |
| `zqY1GZKK` | -0.23 | -0.07 | 1.13 | — | 0.01 | 0 | 119 | `rank(ts_mean(oth571_views7d, 66))` |
| `gJQEG6JM` | -0.24 | -0.07 | 1.20 | — | 0.02 | 0 | 119 | `rank(ts_decay_linear(oth571_views7dafternoon, 21))` |
| `9qVLMYZK` | -0.24 | -0.07 | 1.09 | — | 0.06 | 0 | 119 | `trade_when(ts_count_nans(oth571_views28d, 22) < 5, rank(oth571_views28d), NaN)` |
| `npKMq9pl` | -0.25 | -0.07 | 1.01 | — | 0.07 | 0 | 119 | `group_zscore(oth571_views1y, industry)` |

## 七、判死记录（sealed dead_end）

- `EUR-other571-WIKI-WEAK`（2026-09-04）family=other571 Wikipedia page views：{"best_2y": 1.27, "best_alpha": "JjxZzqje", "best_fitness": 0.09, "best_sharpe": 0.58, "dataset": "other571", "evidence": "wave119 9 条全灭：Wikipedia 浏览量在 EUR TOP2500 整体弱信号，最强 S0.58/F0.09/2Y-0.61 远低于 Mode B 线；if_else 唯一正信号但强度不足；ts_decay_linear/ts_mean/zscore 全负", "id": "EUR-other571-WIKI-WEAK", "reason": "other571 Wikipedia 浏览量在 EUR D1 无正向预测力；9 条中 8 条负，1 条 S0.58 弱；if_else 条件逻辑唯一正信号但强度不足", "region": "

