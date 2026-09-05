# other571 Feature Engineering Analysis Report

**Dataset**: other571
**Region**: EUR
**Delay**: 1


- **Dataset**: `other571`
- **Category**: `other`
- **Region**: `EUR`
- **Delay**: `1`
- **Universe**: `TOP2500`
- **Fields Analyzed**: 30
- **Generated**: 2026-09-04T02:31:36.629993

---

## Executive Summary

本数据集提供 30 个字段（MATRIX 30 / VECTOR 0 / GROUP 0），覆盖 `other` 类信号。以下为自动生成的特征工程思路，供 S2 GEM 阶段绑定字段池。

## 字段画像（Field Inventory）

| Field ID | Type | Coverage | Field Type | Operator Adaptation | Description |
|---|---|---|---|---|---|
| `oth571_views14d` | MATRIX | 78% | 连续数值型 | ts_mean/ts_delta/rank/ts_zscore/ts_corr/ts_regression；禁 ts_std_dev/ts_max_diff | Total Wikipedia company page views in the USA module over the trailing 14-day window ending 14 days ago (inclusive; modu |
| `oth571_views1y` | MATRIX | 70% | 连续数值型 | ts_mean/ts_delta/rank/ts_zscore/ts_corr/ts_regression；禁 ts_std_dev/ts_max_diff | Total Wikipedia company page views in the USA module over the trailing 365-day window (366 in leap years) ending 364 day |
| `oth571_views1yafternoon` | MATRIX | 70% | 连续数值型 | ts_mean/ts_delta/rank/ts_zscore/ts_corr/ts_regression；禁 ts_std_dev/ts_max_diff | Wikipedia company page views in the USA module from 12:00 to 17:59 on the day 364 days ago (module timezone) |
| `oth571_views1ydesktop` | MATRIX | 70% | 连续数值型 | ts_mean/ts_delta/rank/ts_zscore/ts_corr/ts_regression；禁 ts_std_dev/ts_max_diff | Total Wikipedia company page views in the USA module via desktop devices on the day 364 days ago (desktop web; module ti |
| `oth571_views1yevening` | MATRIX | 70% | 连续数值型 | ts_mean/ts_delta/rank/ts_zscore/ts_corr/ts_regression；禁 ts_std_dev/ts_max_diff | Wikipedia company page views in the USA module from 18:00 to 23:59 on the day 364 days ago (module timezone) |
| `oth571_views1ymobile` | MATRIX | 70% | 连续数值型 | ts_mean/ts_delta/rank/ts_zscore/ts_corr/ts_regression；禁 ts_std_dev/ts_max_diff | Total Wikipedia company page views in the USA module via mobile devices on the day 364 days ago (mobile web and apps; mo |
| `oth571_views1ymorning` | MATRIX | 70% | 连续数值型 | ts_mean/ts_delta/rank/ts_zscore/ts_corr/ts_regression；禁 ts_std_dev/ts_max_diff | Wikipedia company page views in the USA module from 06:00 to 11:59 on the day 364 days ago (module timezone) |
| `oth571_views1ynight` | MATRIX | 70% | 连续数值型 | ts_mean/ts_delta/rank/ts_zscore/ts_corr/ts_regression；禁 ts_std_dev/ts_max_diff | Wikipedia company page views in the USA module from 00:00 to 05:59 on the day 364 days ago (module timezone) |
| `oth571_views28d` | MATRIX | 78% | 连续数值型 | ts_mean/ts_delta/rank/ts_zscore/ts_corr/ts_regression；禁 ts_std_dev/ts_max_diff | Total Wikipedia company page views in the USA module over the trailing 28-day window ending 28 days ago (inclusive; modu |
| `oth571_views28dafternoon` | MATRIX | 78% | 连续数值型 | ts_mean/ts_delta/rank/ts_zscore/ts_corr/ts_regression；禁 ts_std_dev/ts_max_diff | Wikipedia company page views in the USA module from 12:00 to 17:59 on the day 28 days ago (module timezone) |
| `oth571_views28ddesktop` | MATRIX | 78% | 连续数值型 | ts_mean/ts_delta/rank/ts_zscore/ts_corr/ts_regression；禁 ts_std_dev/ts_max_diff | Total Wikipedia company page views in the USA module via desktop devices on the day 28 days ago (desktop web; module tim |
| `oth571_views28devening` | MATRIX | 78% | 连续数值型 | ts_mean/ts_delta/rank/ts_zscore/ts_corr/ts_regression；禁 ts_std_dev/ts_max_diff | Wikipedia company page views in the USA module from 18:00 to 23:59 on the day 28 days ago (module timezone) |
| `oth571_views28dmobile` | MATRIX | 78% | 连续数值型 | ts_mean/ts_delta/rank/ts_zscore/ts_corr/ts_regression；禁 ts_std_dev/ts_max_diff | Total Wikipedia company page views in the USA module via mobile devices on the day 28 days ago (mobile web and apps; mod |
| `oth571_views28dmorning` | MATRIX | 78% | 连续数值型 | ts_mean/ts_delta/rank/ts_zscore/ts_corr/ts_regression；禁 ts_std_dev/ts_max_diff | Wikipedia company page views in the USA module from 06:00 to 11:59 on the day 28 days ago (module timezone) |
| `oth571_views28dnight` | MATRIX | 78% | 连续数值型 | ts_mean/ts_delta/rank/ts_zscore/ts_corr/ts_regression；禁 ts_std_dev/ts_max_diff | Wikipedia company page views in the USA module from 00:00 to 05:59 on the day 28 days ago (module timezone) |
| `oth571_views7d` | MATRIX | 78% | 连续数值型 | ts_mean/ts_delta/rank/ts_zscore/ts_corr/ts_regression；禁 ts_std_dev/ts_max_diff | Total Wikipedia page views over the past 7 natural days. |
| `oth571_views7dafternoon` | MATRIX | 78% | 连续数值型 | ts_mean/ts_delta/rank/ts_zscore/ts_corr/ts_regression；禁 ts_std_dev/ts_max_diff | Wikipedia company page views in the USA module from 12:00 to 17:59 on the day 7 days ago (module timezone) |
| `oth571_views7ddesktop` | MATRIX | 78% | 连续数值型 | ts_mean/ts_delta/rank/ts_zscore/ts_corr/ts_regression；禁 ts_std_dev/ts_max_diff | Wikipedia page views from desktop devices over the past 7 natural days. |
| `oth571_views7devening` | MATRIX | 78% | 连续数值型 | ts_mean/ts_delta/rank/ts_zscore/ts_corr/ts_regression；禁 ts_std_dev/ts_max_diff | Wikipedia company page views in the USA module from 18:00 to 23:59 on the day 7 days ago (module timezone) |
| `oth571_views7dmobile` | MATRIX | 78% | 连续数值型 | ts_mean/ts_delta/rank/ts_zscore/ts_corr/ts_regression；禁 ts_std_dev/ts_max_diff | Wikipedia page views from mobile devices over the past 7 natural days. |
| `oth571_views7dmorning` | MATRIX | 78% | 连续数值型 | ts_mean/ts_delta/rank/ts_zscore/ts_corr/ts_regression；禁 ts_std_dev/ts_max_diff | Wikipedia company page views in the USA module from 06:00 to 11:59 on the day 7 days ago (module timezone) |
| `oth571_views7dnight` | MATRIX | 78% | 连续数值型 | ts_mean/ts_delta/rank/ts_zscore/ts_corr/ts_regression；禁 ts_std_dev/ts_max_diff | Wikipedia company page views in the USA module from 00:00 to 05:59 on the day 7 days ago (module timezone) |
| `oth571_views84d` | MATRIX | 76% | 连续数值型 | ts_mean/ts_delta/rank/ts_zscore/ts_corr/ts_regression；禁 ts_std_dev/ts_max_diff | Total Wikipedia company page views in the USA module over the trailing 84-day window ending 84 days ago (inclusive; modu |
| `oth571_viewstoday` | MATRIX | 77% | 连续数值型 | ts_mean/ts_delta/rank/ts_zscore/ts_corr/ts_regression；禁 ts_std_dev/ts_max_diff | Total Wikipedia company page views in the USA module today (calendar day; module timezone) |
| `oth571_viewstodayafternoon` | MATRIX | 77% | 连续数值型 | ts_mean/ts_delta/rank/ts_zscore/ts_corr/ts_regression；禁 ts_std_dev/ts_max_diff | Wikipedia company page views in the USA module from 12:00 to 17:59 today (module timezone) |
| `oth571_viewstodaydesktop` | MATRIX | 77% | 连续数值型 | ts_mean/ts_delta/rank/ts_zscore/ts_corr/ts_regression；禁 ts_std_dev/ts_max_diff | Total Wikipedia company page views in the USA module via desktop devices today (desktop web; module timezone) |
| `oth571_viewstodayevening` | MATRIX | 77% | 连续数值型 | ts_mean/ts_delta/rank/ts_zscore/ts_corr/ts_regression；禁 ts_std_dev/ts_max_diff | Wikipedia company page views in the USA module from 18:00 to 23:59 today (module timezone) |
| `oth571_viewstodaymobile` | MATRIX | 77% | 连续数值型 | ts_mean/ts_delta/rank/ts_zscore/ts_corr/ts_regression；禁 ts_std_dev/ts_max_diff | Total Wikipedia company page views in the USA module via mobile devices today (mobile web and apps; module timezone) |
| `oth571_viewstodaymorning` | MATRIX | 77% | 连续数值型 | ts_mean/ts_delta/rank/ts_zscore/ts_corr/ts_regression；禁 ts_std_dev/ts_max_diff | Wikipedia company page views in the USA module from 06:00 to 11:59 today (module timezone) |
| `oth571_viewstodaynight` | MATRIX | 77% | 连续数值型 | ts_mean/ts_delta/rank/ts_zscore/ts_corr/ts_regression；禁 ts_std_dev/ts_max_diff | Wikipedia company page views in the USA module from 00:00 to 05:59 today (module timezone) |

## 字段-算子适配表（Field-Operator Adaptation）

| Field Type | Valid Operators | Forbidden Operators | Example |
|---|---|---|---|
| 连续数值型 | `ts_mean/ts_delta/rank/ts_zscore/ts_corr/ts_regression` | `ts_std_dev`（波动率无预测力）、`ts_max_diff`（加速脉冲失效） | `rank(ts_mean(surprise, 22))` |
| 分类型（quantile_label/rank） | `rank/group_rank/ts_backfill` | `ts_mean`（分类平均无意义）、`ts_zscore`（非连续分布） | `rank(ts_backfill(quantile_label, 66))` |
| 概率型（prob_class） | `rank/subtract/if_else` | `ts_mean`（概率平均稀释信号）、`ts_delta`（概率变化噪声大） | `rank(prob_class1) - rank(prob_class0)` |
| 计数型（count/usd） | `ts_sum/trade_when/ts_backfill` | `ts_delta`（计数变化=已反应）、`ts_max_diff`（加速脉冲失效） | `trade_when(count > 0, rank(x), NaN)` |
| 比率型（to_price/ratio） | `rank/group_zscore/group_neutralize` | `ts_mean`（比率平均无意义）、`ts_delta`（比率变化噪声） | `group_zscore(ratio, industry)` |
| VECTOR 型 | `vec_avg/vec_sum/vec_stddev/vec_range` + `ts_mean/ts_delta/rank` | 直接用 `ts_mean`（必须先聚合） | `rank(ts_mean(vec_avg(sentiment), 22))` |

## 字段解构（Field Deconstruction）

### `oth571_views7d`（MATRIX）
- **测什么**：Total Wikipedia page views over the past 7 natural days.
- **覆盖率**：0.7806
- **字段名语义**：`oth571_views7d` 的命名前缀用于字段族聚类（S1 前缀扫描）

### `oth571_views7dafternoon`（MATRIX）
- **测什么**：Wikipedia company page views in the USA module from 12:00 to 17:59 on the day 7 days ago (module timezone)
- **覆盖率**：0.7806
- **字段名语义**：`oth571_views7dafternoon` 的命名前缀用于字段族聚类（S1 前缀扫描）

### `oth571_views7ddesktop`（MATRIX）
- **测什么**：Wikipedia page views from desktop devices over the past 7 natural days.
- **覆盖率**：0.7806
- **字段名语义**：`oth571_views7ddesktop` 的命名前缀用于字段族聚类（S1 前缀扫描）

### `oth571_views7devening`（MATRIX）
- **测什么**：Wikipedia company page views in the USA module from 18:00 to 23:59 on the day 7 days ago (module timezone)
- **覆盖率**：0.7806
- **字段名语义**：`oth571_views7devening` 的命名前缀用于字段族聚类（S1 前缀扫描）

### `oth571_views7dmobile`（MATRIX）
- **测什么**：Wikipedia page views from mobile devices over the past 7 natural days.
- **覆盖率**：0.7806
- **字段名语义**：`oth571_views7dmobile` 的命名前缀用于字段族聚类（S1 前缀扫描）

### `oth571_views7dmorning`（MATRIX）
- **测什么**：Wikipedia company page views in the USA module from 06:00 to 11:59 on the day 7 days ago (module timezone)
- **覆盖率**：0.7806
- **字段名语义**：`oth571_views7dmorning` 的命名前缀用于字段族聚类（S1 前缀扫描）

### `oth571_views7dnight`（MATRIX）
- **测什么**：Wikipedia company page views in the USA module from 00:00 to 05:59 on the day 7 days ago (module timezone)
- **覆盖率**：0.7806
- **字段名语义**：`oth571_views7dnight` 的命名前缀用于字段族聚类（S1 前缀扫描）

### `oth571_views14d`（MATRIX）
- **测什么**：Total Wikipedia company page views in the USA module over the trailing 14-day window ending 14 days ago (inclusive; module timezone)
- **覆盖率**：0.7791
- **字段名语义**：`oth571_views14d` 的命名前缀用于字段族聚类（S1 前缀扫描）

## 预处理决策（Preprocessing）

- group_zscore / group_rank：MATRIX 字段截面中性化（cross-sectional）

## 特征概念（8 问框架，模板化）

### Q1 稳定性/不变量
- **使用字段**：`oth571_views7d`, `oth571_views7dafternoon`
- **建议**：ts_mean / ts_std_dev 度量字段的长期水平与稳定性

### Q2 变化
- **使用字段**：`oth571_views7d`, `oth571_views7dafternoon`
- **建议**：ts_delta / ts_scale 捕捉变化率与动量

### Q3 异常
- **使用字段**：`oth571_views7d`, `oth571_views7dafternoon`
- **建议**：zscore / ts_rank 识别截面与时间序列上的离群

### Q4 交互
- **使用字段**：`oth571_views7d`, `oth571_views7dafternoon`
- **建议**：两字段 add/multiply 合成新含义，注意先各自中性化

### Q5 结构
- **使用字段**：`oth571_views7d`, `oth571_views7dafternoon`
- **建议**：字段占比 / 比例关系（如 components 型字段）

### Q6 累积
- **使用字段**：`oth571_views7d`, `oth571_views7dafternoon`
- **建议**：ts_sum / ts_decay_linear 累积与衰减记忆

### Q7 相对
- **使用字段**：`oth571_views7d`, `oth571_views7dafternoon`
- **建议**：rank / group_rank 相对定位与归一化

### Q8 本质
- **使用字段**：`oth571_views7d`, `oth571_views7dafternoon`
- **建议**：第一性原理直取原始字段，剥离过拟合包装

## GEM 兼容模板（Concept Blocks）

> 以下 Concept 块供 S2 `brain-makeSomeGem` 直接消费（`--ideas-file` 注入）。
> 占位符 `{field_id}` 为字段白名单中的真实字段 id，run_pipeline 可解析绑定。

**Concept**: oth571_views7d 长期水平稳定（Q1）
- **Mechanism**: ts_mean 度量字段长期水平，rank 截面归一化
- **Fields Used**: `oth571_views7d`, `oth571_views7dafternoon`
- **Implementation Example**: `rank(ts_mean({oth571_views7d}, 66))`
- **Direction**: High → long

**Concept**: oth571_views7d 变化动量（Q2）
- **Mechanism**: ts_delta 捕捉 21 日变化率，rank 截面归一化
- **Fields Used**: `oth571_views7d`, `oth571_views7dafternoon`
- **Implementation Example**: `rank(ts_delta({oth571_views7d}, 21))`
- **Direction**: High → long

**Concept**: oth571_views7d 截面离群（Q3）
- **Mechanism**: zscore 识别截面离群，rank 归一化
- **Fields Used**: `oth571_views7d`, `oth571_views7dafternoon`
- **Implementation Example**: `rank(zscore({oth571_views7d}))`
- **Direction**: High → long

**Concept**: oth571_views7d × oth571_views7dafternoon 交互（Q4）
- **Mechanism**: 两字段各自 ts_zscore 中性化后 multiply 合成
- **Fields Used**: `oth571_views7d`, `oth571_views7dafternoon`
- **Implementation Example**: `rank(multiply(ts_zscore({oth571_views7d}, 66), ts_zscore({oth571_views7dafternoon}, 66)))`
- **Direction**: High → long

**Concept**: oth571_views7d 结构占比（Q5）
- **Mechanism**: divide 构造比例关系，rank 截面归一化
- **Fields Used**: `oth571_views7d`, `oth571_views7dafternoon`
- **Implementation Example**: `rank(divide({oth571_views7d}, {oth571_views7dafternoon}))`
- **Direction**: High → long

**Concept**: oth571_views7d 累积衰减（Q6）
- **Mechanism**: ts_decay_linear 累积记忆衰减，rank 归一化
- **Fields Used**: `oth571_views7d`, `oth571_views7dafternoon`
- **Implementation Example**: `rank(ts_decay_linear({oth571_views7d}, 21))`
- **Direction**: High → long

**Concept**: oth571_views7d 截面相对定位（Q7）
- **Mechanism**: ts_backfill 稀疏回填 + group_rank 行业内相对定位
- **Fields Used**: `oth571_views7d`, `oth571_views7dafternoon`
- **Implementation Example**: `group_rank(ts_backfill({oth571_views7d}, 66), industry)`
- **Direction**: High → long

**Concept**: oth571_views7d 本质直取（Q8）
- **Mechanism**: 第一性原理直取原始字段，rank 截面归一化
- **Fields Used**: `oth571_views7d`, `oth571_views7dafternoon`
- **Implementation Example**: `rank({oth571_views7d})`
- **Direction**: High → long

## 字段白名单（Field Whitelist）

```
oth571_views14d
oth571_views1y
oth571_views1yafternoon
oth571_views1ydesktop
oth571_views1yevening
oth571_views1ymobile
oth571_views1ymorning
oth571_views1ynight
oth571_views28d
oth571_views28dafternoon
oth571_views28ddesktop
oth571_views28devening
oth571_views28dmobile
oth571_views28dmorning
oth571_views28dnight
oth571_views7d
oth571_views7dafternoon
oth571_views7ddesktop
oth571_views7devening
oth571_views7dmobile
oth571_views7dmorning
oth571_views7dnight
oth571_views84d
oth571_viewstoday
oth571_viewstodayafternoon
oth571_viewstodaydesktop
oth571_viewstodayevening
oth571_viewstodaymobile
oth571_viewstodaymorning
oth571_viewstodaynight
```

*Report generated: 2026-09-04T02:31:36.629993*