# institutions6 Feature Engineering Analysis Report

**Dataset**: institutions6
**Region**: GBR
**Delay**: 1


- **Dataset**: `institutions6`
- **Category**: `INSTITUTIONS`
- **Region**: `GBR`
- **Delay**: `1`
- **Universe**: `TOP700`
- **Fields Analyzed**: 11
- **Generated**: 2026-09-12T03:15:00.000000

---

## Executive Summary

本数据集提供 11 个字段（MATRIX 11 / VECTOR 0 / GROUP 0），覆盖 `INSTITUTIONS` 类信号。以下为自动生成的特征工程思路，供 S2 GEM 阶段绑定字段池。

## 字段画像（Field Inventory）

| Field ID | Type | Coverage | Field Type | Operator Adaptation | Description |
|---|---|---|---|---|---|
| `aggregate_equity_value_all_owners` | MATRIX | 100% | 连续数值型 | ts_mean/ts_delta/rank/ts_zscore/ts_corr/ts_regression；禁 ts_std_dev/ts_max_diff | Aggregate dollar value of shares of the security held by all owners, with duplication between child and parent owners re |
| `aggregate_equity_value_institutions` | MATRIX | 100% | 连续数值型 | ts_mean/ts_delta/rank/ts_zscore/ts_corr/ts_regression；禁 ts_std_dev/ts_max_diff | Aggregate dollar value of shares of the security currently held by all institutional investors at the reporting date |
| `aggregate_share_count_all_owners` | MATRIX | 100% | 计数型 | ts_sum/trade_when/ts_backfill；禁 ts_delta/ts_max_diff | Aggregate number of shares of the security held by all owners, with duplication between child and parent owners removed |
| `aggregate_share_count_institutions` | MATRIX | 100% | 计数型 | ts_sum/trade_when/ts_backfill；禁 ts_delta/ts_max_diff | Total number of shares of the security currently held by all institutional investors at the reporting date |
| `count_institutional_buyers_security` | MATRIX | 100% | 计数型 | ts_sum/trade_when/ts_backfill；禁 ts_delta/ts_max_diff | Number of institutional investors who purchased shares of the security during the reporting period |
| `count_institutional_holders_security` | MATRIX | 100% | 计数型 | ts_sum/trade_when/ts_backfill；禁 ts_delta/ts_max_diff | Number of institutional investors currently holding shares (with holdings greater than zero) for the security at the rep |
| `count_institutional_sellers_security` | MATRIX | 100% | 计数型 | ts_sum/trade_when/ts_backfill；禁 ts_delta/ts_max_diff | Number of institutional investors who sold shares of the security during the reporting period |
| `market_value_institutional_shares_acquired` | MATRIX | 100% | 连续数值型 | ts_mean/ts_delta/rank/ts_zscore/ts_corr/ts_regression；禁 ts_std_dev/ts_max_diff | Aggregate dollar value of shares of the security purchased by institutional investors during the reporting period |
| `market_value_institutional_shares_disposed` | MATRIX | 100% | 连续数值型 | ts_mean/ts_delta/rank/ts_zscore/ts_corr/ts_regression；禁 ts_std_dev/ts_max_diff | Aggregate dollar value of shares of the security sold by institutional investors during the reporting period |
| `quantity_institutional_shares_acquired` | MATRIX | 100% | 连续数值型 | ts_mean/ts_delta/rank/ts_zscore/ts_corr/ts_regression；禁 ts_std_dev/ts_max_diff | Total number of shares of the security purchased by institutional investors during the reporting period |
| `quantity_institutional_shares_disposed` | MATRIX | 100% | 连续数值型 | ts_mean/ts_delta/rank/ts_zscore/ts_corr/ts_regression；禁 ts_std_dev/ts_max_diff | Total number of shares of the security sold by institutional investors during the reporting period |

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

### `market_value_institutional_shares_disposed`（MATRIX）
- **测什么**：Aggregate dollar value of shares of the security sold by institutional investors during the reporting period
- **覆盖率**：1.0
- **字段名语义**：`market_value_institutional_shares_disposed` 的命名前缀用于字段族聚类（S1 前缀扫描）

### `aggregate_share_count_institutions`（MATRIX）
- **测什么**：Total number of shares of the security currently held by all institutional investors at the reporting date
- **覆盖率**：1.0
- **字段名语义**：`aggregate_share_count_institutions` 的命名前缀用于字段族聚类（S1 前缀扫描）

### `aggregate_share_count_all_owners`（MATRIX）
- **测什么**：Aggregate number of shares of the security held by all owners, with duplication between child and parent owners removed
- **覆盖率**：1.0
- **字段名语义**：`aggregate_share_count_all_owners` 的命名前缀用于字段族聚类（S1 前缀扫描）

### `count_institutional_sellers_security`（MATRIX）
- **测什么**：Number of institutional investors who sold shares of the security during the reporting period
- **覆盖率**：1.0
- **字段名语义**：`count_institutional_sellers_security` 的命名前缀用于字段族聚类（S1 前缀扫描）

### `quantity_institutional_shares_disposed`（MATRIX）
- **测什么**：Total number of shares of the security sold by institutional investors during the reporting period
- **覆盖率**：1.0
- **字段名语义**：`quantity_institutional_shares_disposed` 的命名前缀用于字段族聚类（S1 前缀扫描）

### `market_value_institutional_shares_acquired`（MATRIX）
- **测什么**：Aggregate dollar value of shares of the security purchased by institutional investors during the reporting period
- **覆盖率**：1.0
- **字段名语义**：`market_value_institutional_shares_acquired` 的命名前缀用于字段族聚类（S1 前缀扫描）

### `count_institutional_buyers_security`（MATRIX）
- **测什么**：Number of institutional investors who purchased shares of the security during the reporting period
- **覆盖率**：1.0
- **字段名语义**：`count_institutional_buyers_security` 的命名前缀用于字段族聚类（S1 前缀扫描）

### `aggregate_equity_value_all_owners`（MATRIX）
- **测什么**：Aggregate dollar value of shares of the security held by all owners, with duplication between child and parent owners removed
- **覆盖率**：1.0
- **字段名语义**：`aggregate_equity_value_all_owners` 的命名前缀用于字段族聚类（S1 前缀扫描）

## 预处理决策（Preprocessing）

- group_zscore / group_rank：MATRIX 字段截面中性化（cross-sectional）

## 特征概念（8 问框架，模板化）

### Q1 稳定性/不变量
- **使用字段**：`market_value_institutional_shares_disposed`, `aggregate_share_count_institutions`
- **建议**：ts_mean / ts_std_dev 度量字段的长期水平与稳定性

### Q2 变化
- **使用字段**：`market_value_institutional_shares_disposed`, `aggregate_share_count_institutions`
- **建议**：ts_delta / ts_scale 捕捉变化率与动量

### Q3 异常
- **使用字段**：`market_value_institutional_shares_disposed`, `aggregate_share_count_institutions`
- **建议**：zscore / ts_rank 识别截面与时间序列上的离群

### Q4 交互
- **使用字段**：`market_value_institutional_shares_disposed`, `aggregate_share_count_institutions`
- **建议**：两字段 add/multiply 合成新含义，注意先各自中性化

### Q5 结构
- **使用字段**：`market_value_institutional_shares_disposed`, `aggregate_share_count_institutions`
- **建议**：字段占比 / 比例关系（如 components 型字段）

### Q6 累积
- **使用字段**：`market_value_institutional_shares_disposed`, `aggregate_share_count_institutions`
- **建议**：ts_sum / ts_decay_linear 累积与衰减记忆

### Q7 相对
- **使用字段**：`market_value_institutional_shares_disposed`, `aggregate_share_count_institutions`
- **建议**：rank / group_rank 相对定位与归一化

### Q8 本质
- **使用字段**：`market_value_institutional_shares_disposed`, `aggregate_share_count_institutions`
- **建议**：第一性原理直取原始字段，剥离过拟合包装

## GEM 兼容模板（Concept Blocks）

> 以下 Concept 块供 S2 `brain-make-some-gem` 直接消费（`--ideas-file` 注入）。
> 占位符 `{field_id}` 为字段白名单中的真实字段 id，run_pipeline 可解析绑定。

**Concept**: market_value_institutional_shares_disposed 长期水平稳定（Q1）
- **Mechanism**: ts_mean 度量字段长期水平，rank 截面归一化
- **Fields Used**: `market_value_institutional_shares_disposed`, `aggregate_share_count_institutions`
- **Implementation Example**: `rank(ts_mean({market_value_institutional_shares_disposed}, 66))`
- **Direction**: High → long

**Concept**: aggregate_share_count_institutions 变化动量（Q2）
- **Mechanism**: ts_delta 捕捉 21 日变化率，rank 截面归一化
- **Fields Used**: `aggregate_share_count_institutions`, `market_value_institutional_shares_disposed`
- **Implementation Example**: `rank(ts_delta({aggregate_share_count_institutions}, 21))`
- **Direction**: High → long

**Concept**: count_institutional_sellers_security 截面离群（Q3）
- **Mechanism**: zscore 识别截面离群，rank 归一化
- **Fields Used**: `count_institutional_sellers_security`, `market_value_institutional_shares_disposed`
- **Implementation Example**: `rank(zscore({count_institutional_sellers_security}))`
- **Direction**: High → long

**Concept**: quantity_institutional_shares_disposed 交互（Q4）
- **Mechanism**: 两字段各自 ts_zscore 中性化后 multiply 合成
- **Fields Used**: `quantity_institutional_shares_disposed`, `market_value_institutional_shares_disposed`
- **Implementation Example**: `rank(multiply(ts_zscore({quantity_institutional_shares_disposed}, 66), ts_zscore({market_value_institutional_shares_disposed}, 66)))`
- **Direction**: High → long

**Concept**: aggregate_share_count_all_owners 结构占比（Q5）
- **Mechanism**: divide 构造比例关系，rank 截面归一化
- **Fields Used**: `aggregate_share_count_all_owners`, `market_value_institutional_shares_disposed`
- **Implementation Example**: `rank(divide({aggregate_share_count_all_owners}, {market_value_institutional_shares_disposed}))`
- **Direction**: High → long

**Concept**: market_value_institutional_shares_acquired 累积衰减（Q6）
- **Mechanism**: ts_decay_linear 累积记忆衰减，rank 归一化
- **Fields Used**: `market_value_institutional_shares_acquired`, `market_value_institutional_shares_disposed`
- **Implementation Example**: `rank(ts_decay_linear({market_value_institutional_shares_acquired}, 21))`
- **Direction**: High → long

**Concept**: count_institutional_buyers_security 截面相对定位（Q7）
- **Mechanism**: ts_backfill 稀疏回填 + group_rank 行业内相对定位
- **Fields Used**: `count_institutional_buyers_security`, `market_value_institutional_shares_disposed`
- **Implementation Example**: `group_rank(ts_backfill({count_institutional_buyers_security}, 66), industry)`
- **Direction**: High → long

**Concept**: aggregate_equity_value_all_owners 本质直取（Q8）
- **Mechanism**: 第一性原理直取原始字段，rank 截面归一化
- **Fields Used**: `aggregate_equity_value_all_owners`, `market_value_institutional_shares_disposed`
- **Implementation Example**: `rank({aggregate_equity_value_all_owners})`
- **Direction**: High → long

## 字段白名单（Field Whitelist）

```
aggregate_equity_value_all_owners
aggregate_equity_value_institutions
aggregate_share_count_all_owners
aggregate_share_count_institutions
count_institutional_buyers_security
count_institutional_holders_security
count_institutional_sellers_security
market_value_institutional_shares_acquired
market_value_institutional_shares_disposed
quantity_institutional_shares_acquired
quantity_institutional_shares_disposed
```

*Report generated: 2026-09-12T03:15:00.000000*