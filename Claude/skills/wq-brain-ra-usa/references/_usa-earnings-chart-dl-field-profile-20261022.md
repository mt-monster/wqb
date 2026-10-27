# earnings_chart_dl 字段画像（USA / TOP3000 / D1）

> **as_of 2026-10-22** · 类别 `earnings`（本季提交 1 次，**未点亮** → 可挖） · 平台实测字段 100 个
> 数据集级：cov 0.991 / aC 1006 / uC 540 / valueScore 2 / pyramidMultiplier 1.2 / 全 MATRIX
> 数据来源：`get_datafields(dataset_id="earnings_chart_dl", region=USA, universe=TOP3000, delay=1)` 全量 100 字段（非 300 截断）

## 0. 数据集机制

财报日历**图像模型**（earnings-calendar CNN）：把个股财报日历与历史价格窗口渲染成图像，用 CNN
输出未来收益 / 波动的**预测分布**。三类输出头并存：

1. **连续回归头**（`quantile_1_assignment_*`）：无约束预测收益值，可直接当"模型的预期收益"；
2. **分桶分类头**（`quantile_N_assignment_*`）：0-based 整数桶号；
3. **置信度头**（`prob_quantile_N_bucket_*` / `likelihood_*`）：log-softmax 对数概率。

关键含义：**只有连续回归头能当"预期收益"用**；分桶头是离散序数（直接 rank 会退化成 N 档，
极易 CONCENTRATED_WEIGHT）；log 概率是**模型置信度**，单桶水平会随模型整体 confidence 漂移，
必须取**桶间差**（对数几率）才有排序含义。

## 1. 字段分族

| 族 | 字段数 | 形态 | cov | 机制 |
|---|---|---|---|---|
| **A 1 日分位头** | 5 | close 为连续预测；open/high/low 为二值 assignment | 1.000 | 1 日 forward 收益/波动方向 |
| **B1 连续回归头** | 5 | 连续、无约束 | 0.987 | 5 / 10 / 20 / 50 日预期收益 + 5 日预期波动 |
| **B2–B5 分桶头** | 20 | 0-based 整数（2/3/4/5 档） | 1.000 | 横截面分位归属 |
| **C2–C5 对数概率头** | 68 | log-softmax（≤0） | 0.987–1.000 | 各桶置信度，差分 = 对数几率 |
| **D likelihood** | 2 | log-softmax | 0.987 | 只有 group_0 / group_2（3/4 档缺失，不可做完整差） |
| **E 上下文** | 1 | 连续 | 1.000 | `rolling_250day_return`，非预测，只作条件/基准 |

族内计数：A_1day=4 / B1_regression=5 / B2_bucket=5 / B3_bucket=5 / B4_bucket=5 / B5_bucket=5 / C2_logprob=10 / C3_logprob=15 / C4_logprob=20 / C5_logprob=23 / D_likelihood=2 / E_context=1

## 2. 逐字段清单（100 个）

| 字段 | 族 | 类型 | cov | aC | uC | 平台描述（截断） |
|---|---|---|---|---|---|---|
| `close_return_quantile_1_1day` | A_1day | MATRIX | 1.0000 | 418 | 277 | Continuous predicted 1-day forward close-to-close return from the earnings ca… |
| `high_return_quantile_1_1day` | A_1day | MATRIX | 1.0000 | 54 | 41 | Assignment of the stock to quantile 1 based on predicted high-to-high 1-day r… |
| `low_return_quantile_1_1day` | A_1day | MATRIX | 1.0000 | 51 | 39 | Assignment of the stock to quantile 1 based on predicted low-to-low 1-day ret… |
| `open_return_quantile_1_1day` | A_1day | MATRIX | 1.0000 | 82 | 60 | Assignment of the stock to quantile 1 based on predicted open-to-open 1-day r… |
| `quantile_1_assignment_10day_return` | B1_regression | MATRIX | 0.9865 | 10 | 10 | Continuous, unconstrained predicted 10-day forward return regression output f… |
| `quantile_1_assignment_20day_return` | B1_regression | MATRIX | 0.9865 | 11 | 10 | Continuous predicted 20-day forward return (regression output) for the stock,… |
| `quantile_1_assignment_50day_return` | B1_regression | MATRIX | 0.9865 | 8 | 8 | Assignment of the stock to quantile 1 for predicted 50-day return. |
| `quantile_1_assignment_5day_return` | B1_regression | MATRIX | 0.9865 | 12 | 11 | Continuous unconstrained regression prediction of 5-day forward return |
| `quantile_1_assignment_5day_volatility` | B1_regression | MATRIX | 0.9865 | 8 | 7 | Continuous regression prediction of unconstrained 5-day forward return |
| `quantile_2_assignment_10day_return` | B2_bucket | MATRIX | 1.0000 | 3 | 3 | Integer quantile assignment (0-based) to one of two cross-sectional buckets f… |
| `quantile_2_assignment_20day_return` | B2_bucket | MATRIX | 1.0000 | 10 | 9 | Quantile assignment index (0-based) for 2 quantiles (halves) of forward retur… |
| `quantile_2_assignment_50day_return` | B2_bucket | MATRIX | 1.0000 | 4 | 4 | Integer quantile assignment (0-based) of the stock-date to one of 2 quantile … |
| `quantile_2_assignment_5day_return` | B2_bucket | MATRIX | 1.0000 | 4 | 4 | 0-based assignment to one of 2 quantile buckets for predicted 5-day forward r… |
| `quantile_2_assignment_5day_volatility` | B2_bucket | MATRIX | 1.0000 | 5 | 4 | Quantile assignment indicating whether the stock's predicted 5-day forward re… |
| `quantile_3_assignment_10day_return` | B3_bucket | MATRIX | 1.0000 | 11 | 11 | 0-based assignment to one of three quantile buckets for 10-day forward return… |
| `quantile_3_assignment_20day_return` | B3_bucket | MATRIX | 1.0000 | 5 | 5 | Quantile assignment index (0-based) for 3 quantiles of forward return predict… |
| `quantile_3_assignment_50day_return` | B3_bucket | MATRIX | 1.0000 | 4 | 4 | Integer quantile assignment (0-based) of the stock-date to one of 3 quantile … |
| `quantile_3_assignment_5day_return` | B3_bucket | MATRIX | 1.0000 | 9 | 5 | 0-based assignment to one of 3 quantile buckets for predicted 5-day forward r… |
| `quantile_3_assignment_5day_volatility` | B3_bucket | MATRIX | 1.0000 | 16 | 11 | Quantile assignment indicating which third (0=bottom,1=middle,2=top) the stoc… |
| `quantile_4_assignment_10day_return` | B4_bucket | MATRIX | 1.0000 | 4 | 4 | 0-based assignment to one of four quantile buckets for 10-day forward return … |
| `quantile_4_assignment_20day_return` | B4_bucket | MATRIX | 1.0000 | 8 | 8 | Integer assignment (0-based) of the stock to one of 4 quantiles based on pred… |
| `quantile_4_assignment_50day_return` | B4_bucket | MATRIX | 1.0000 | 6 | 5 | Integer quantile assignment (0-based) of the stock-date to one of 4 quantile … |
| `quantile_4_assignment_5day_return` | B4_bucket | MATRIX | 1.0000 | 4 | 4 | Integer quantile assignment (0-based) to one of 4 buckets for 5-day forward r… |
| `quantile_4_assignment_5day_volatility` | B4_bucket | MATRIX | 1.0000 | 19 | 17 | Quantile assignment (0-based) to one of four forward return buckets at 5-day … |
| `quantile_5_assignment_10day_return` | B5_bucket | MATRIX | 1.0000 | 35 | 23 | Integer quantile assignment (0-based) to one of five cross-sectional buckets … |
| `quantile_5_assignment_20day_return` | B5_bucket | MATRIX | 1.0000 | 18 | 12 | Quantile assignment index (0-based) for 5 quantiles of forward return predict… |
| `quantile_5_assignment_50day_return` | B5_bucket | MATRIX | 1.0000 | 9 | 7 | Integer quantile assignment (0-based) of the stock-date to one of 5 quantile … |
| `quantile_5_assignment_5day_return` | B5_bucket | MATRIX | 1.0000 | 9 | 8 | 0-based assignment to one of 5 quantile buckets for predicted 5-day forward r… |
| `quantile_5_assignment_5day_volatility` | B5_bucket | MATRIX | 1.0000 | 15 | 11 | Quantile assignment (0-based) to one of five forward return buckets at 5-day … |
| `prob_quantile_2_bucket_0_10day_return` | C2_logprob | MATRIX | 0.9865 | 7 | 5 | Log-probability (log-softmax confidence) that the stock-date belongs to the b… |
| `prob_quantile_2_bucket_0_20day_return` | C2_logprob | MATRIX | 0.9865 | 6 | 6 | Log-probability that the stock-date belongs to the lower half (quantile 0) in… |
| `prob_quantile_2_bucket_0_50day_return` | C2_logprob | MATRIX | 0.9865 | 4 | 4 | Log-probability confidence (log-softmax) of the stock-date belonging to quant… |
| `prob_quantile_2_bucket_0_5day_return` | C2_logprob | MATRIX | 0.9865 | 6 | 6 | Log-probability (log-softmax) confidence that the stock is in the 0th quantil… |
| `prob_quantile_2_bucket_0_5day_volatility` | C2_logprob | MATRIX | 0.9865 | 2 | 2 | Log-probability of belonging to the bottom half quantile (quantile 0 of 2) fo… |
| `prob_quantile_2_bucket_1_10day_return` | C2_logprob | MATRIX | 0.9865 | 20 | 16 | Log-probability confidence for being in the top half quantile (quantile 1 out… |
| `prob_quantile_2_bucket_1_20day_return` | C2_logprob | MATRIX | 0.9865 | 10 | 8 | Log-probability (log-softmax confidence) that the stock-date belongs to the u… |
| `prob_quantile_2_bucket_1_50day_return` | C2_logprob | MATRIX | 0.9865 | 5 | 5 | Log-probability confidence (log-softmax) of the stock-date belonging to quant… |
| `prob_quantile_2_bucket_1_5day_return` | C2_logprob | MATRIX | 1.0000 | 20 | 19 | Log-probability confidence that the stock is in the 1st quantile bucket (top … |
| `prob_quantile_2_bucket_1_5day_volatility` | C2_logprob | MATRIX | 0.9865 | 5 | 5 | Log-probability of belonging to the top half quantile (quantile 1 of 2) for 5… |
| `prob_quantile_3_bucket_0_10day_return` | C3_logprob | MATRIX | 0.9865 | 7 | 5 | Log-probability confidence for being in the bottom quantile (quantile 0 out o… |
| `prob_quantile_3_bucket_0_20day_return` | C3_logprob | MATRIX | 0.9865 | 6 | 6 | Log-probability (log-softmax confidence) that the stock's 20-day forward retu… |
| `prob_quantile_3_bucket_0_50day_return` | C3_logprob | MATRIX | 0.9865 | 2 | 2 | Probability that the stock falls into bucket 0 of quantile 3 for predicted 50… |
| `prob_quantile_3_bucket_0_5day_return` | C3_logprob | MATRIX | 0.9865 | 6 | 5 | Log-probability confidence for the stock belonging to the 0th quantile (botto… |
| `prob_quantile_3_bucket_0_5day_volatility` | C3_logprob | MATRIX | 0.9865 | 1 | 1 | Log-probability of belonging to the bottom third quantile (quantile 0 of 3) f… |
| `prob_quantile_3_bucket_1_10day_return` | C3_logprob | MATRIX | 0.9865 | 1 | 1 | Log-probability confidence for being in the middle quantile (quantile 1 out o… |
| `prob_quantile_3_bucket_1_20day_return` | C3_logprob | MATRIX | 1.0000 | 6 | 6 | Log-probability (log-softmax confidence) that the stock's 20-day forward retu… |
| `prob_quantile_3_bucket_1_50day_return` | C3_logprob | MATRIX | 0.9865 | 4 | 4 | Probability that the stock falls into bucket 1 of quantile 3 for predicted 50… |
| `prob_quantile_3_bucket_1_5day_return` | C3_logprob | MATRIX | 1.0000 | 3 | 2 | Log-probability confidence for the stock belonging to the 1st quantile (middl… |
| `prob_quantile_3_bucket_1_5day_volatility` | C3_logprob | MATRIX | 0.9865 | 2 | 2 | Log-softmax confidence score that the stock belongs to the 1st quantile bucke… |
| `prob_quantile_3_bucket_2_10day_return` | C3_logprob | MATRIX | 0.9865 | 15 | 10 | Log-probability (log-softmax confidence) that the stock-date belongs to the t… |
| `prob_quantile_3_bucket_2_20day_return` | C3_logprob | MATRIX | 0.9865 | 6 | 6 | Log-probability that the stock-date belongs to the top third quantile (quanti… |
| `prob_quantile_3_bucket_2_50day_return` | C3_logprob | MATRIX | 0.9865 | 3 | 3 | Probability that the stock falls into bucket 2 of quantile 3 for predicted 50… |
| `prob_quantile_3_bucket_2_5day_return` | C3_logprob | MATRIX | 0.9865 | 6 | 6 | Probability that the stock falls into bucket 2 of quantile 3 for predicted 5-… |
| `prob_quantile_3_bucket_2_5day_volatility` | C3_logprob | MATRIX | 1.0000 | 2 | 2 | Log-softmax confidence score that the stock belongs to the 2nd quantile bucke… |
| `prob_quantile_4_bucket_0_10day_return` | C4_logprob | MATRIX | 0.9865 | 16 | 13 | Log-probability confidence for being in the bottom quantile (quantile 0 out o… |
| `prob_quantile_4_bucket_0_20day_return` | C4_logprob | MATRIX | 0.9865 | 13 | 11 | Log-probability (log-softmax confidence) that the stock's 20-day forward retu… |
| `prob_quantile_4_bucket_0_50day_return` | C4_logprob | MATRIX | 0.9865 | 5 | 4 | Log-probability confidence (log-softmax) of the stock-date belonging to quant… |
| `prob_quantile_4_bucket_0_5day_return` | C4_logprob | MATRIX | 0.9865 | 6 | 6 | Probability that the stock falls into bucket 0 of quantile 4 for predicted 5-… |
| `prob_quantile_4_bucket_0_5day_volatility` | C4_logprob | MATRIX | 0.9865 | 4 | 4 | Log-probability of belonging to the lowest quartile (quantile 0 of 4) for 5-d… |
| `prob_quantile_4_bucket_1_10day_return` | C4_logprob | MATRIX | 0.9865 | 6 | 6 | Log-probability (log-softmax confidence) that the stock-date belongs to the 2… |
| `prob_quantile_4_bucket_1_20day_return` | C4_logprob | MATRIX | 0.9865 | 2 | 2 | Log-probability that the stock-date belongs to the 2nd quartile (quantile 1) … |
| `prob_quantile_4_bucket_1_50day_return` | C4_logprob | MATRIX | 0.9865 | 3 | 3 | Log-probability confidence (log-softmax) of the stock-date belonging to quant… |
| `prob_quantile_4_bucket_1_5day_return` | C4_logprob | MATRIX | 0.9865 | 3 | 3 | Log-probability confidence for the stock belonging to the 1st quantile (secon… |
| `prob_quantile_4_bucket_1_5day_volatility` | C4_logprob | MATRIX | 0.9865 | 7 | 4 | Log-probability of belonging to the second lowest quartile (quantile 1 of 4) … |
| `prob_quantile_4_bucket_2_10day_return` | C4_logprob | MATRIX | 0.9865 | 4 | 4 | Log-probability (log-softmax confidence) that the stock-date belongs to the 3… |
| `prob_quantile_4_bucket_2_20day_return` | C4_logprob | MATRIX | 0.9865 | 6 | 4 | Log-probability (log-softmax confidence) that the stock's 20-day forward retu… |
| `prob_quantile_4_bucket_2_50day_return` | C4_logprob | MATRIX | 0.9865 | 5 | 5 | Log-probability confidence (log-softmax) of the stock-date belonging to quant… |
| `prob_quantile_4_bucket_2_5day_return` | C4_logprob | MATRIX | 1.0000 | 3 | 3 | Probability that the stock falls into bucket 2 of quantile 4 for predicted 5-… |
| `prob_quantile_4_bucket_2_5day_volatility` | C4_logprob | MATRIX | 0.9865 | 1 | 1 | Log-softmax confidence score that the stock belongs to the 2nd quantile bucke… |
| `prob_quantile_4_bucket_3_10day_return` | C4_logprob | MATRIX | 0.9865 | 15 | 15 | Log-probability confidence for being in the top quantile (quantile 3 out of 4… |
| `prob_quantile_4_bucket_3_20day_return` | C4_logprob | MATRIX | 0.9865 | 27 | 24 | Log-probability that the stock-date belongs to the top quartile (quantile 3) … |
| `prob_quantile_4_bucket_3_50day_return` | C4_logprob | MATRIX | 0.9865 | 8 | 6 | Log-probability (log-softmax confidence) that the stock-date belongs to the 3… |
| `prob_quantile_4_bucket_3_5day_return` | C4_logprob | MATRIX | 0.9865 | 16 | 14 | Probability that the stock falls into bucket 3 of quantile 4 for predicted 5-… |
| `prob_quantile_4_bucket_3_5day_volatility` | C4_logprob | MATRIX | 0.9865 | 1 | 1 | Log-softmax confidence score that the stock belongs to the 4th quantile bucke… |
| `prob_quantile_5_bucket_0_10day_return` | C5_logprob | MATRIX | 0.9865 | 21 | 17 | Log-probability confidence for being in the bottom quantile (quantile 0 out o… |
| `prob_quantile_5_bucket_0_20day_return` | C5_logprob | MATRIX | 1.0000 | 29 | 25 | Log-probability (log-softmax confidence) that the stock's 20-day forward retu… |
| `prob_quantile_5_bucket_0_5day_return` | C5_logprob | MATRIX | 0.9865 | 9 | 7 | Probability that the stock falls into bucket 0 of quantile 5 for predicted 5-… |
| `prob_quantile_5_bucket_0_5day_volatility` | C5_logprob | MATRIX | 0.9865 | 3 | 3 | Log-softmax confidence score that the stock belongs to the 0th (lowest) quant… |
| `prob_quantile_5_bucket_1_10day_return` | C5_logprob | MATRIX | 0.9865 | 3 | 3 | Log-probability (log-softmax confidence) that the stock-date belongs to the 2… |
| `prob_quantile_5_bucket_1_20day_return` | C5_logprob | MATRIX | 0.9865 | 1 | 1 | Log-probability (log-softmax confidence) that the stock's 20-day forward retu… |
| `prob_quantile_5_bucket_1_50day_return` | C5_logprob | MATRIX | 0.9865 | 4 | 2 | Log-probability confidence (log-softmax) of the stock-date belonging to quant… |
| `prob_quantile_5_bucket_1_5day_return` | C5_logprob | MATRIX | 0.9865 | 1 | 1 | Log-probability confidence for the stock belonging to the 1st quantile (secon… |
| `prob_quantile_5_bucket_1_5day_volatility` | C5_logprob | MATRIX | 0.9865 | 1 | 1 | Log-probability of belonging to the second quantile (quantile 1 of 5) for 5-d… |
| `prob_quantile_5_bucket_2_10day_return` | C5_logprob | MATRIX | 0.9865 | 8 | 7 | Log-probability (log-softmax confidence) that the stock-date belongs to the 3… |
| `prob_quantile_5_bucket_2_20day_return` | C5_logprob | MATRIX | 1.0000 | 13 | 4 | Log-probability (log-softmax confidence) that the stock's 20-day forward retu… |
| `prob_quantile_5_bucket_2_5day_return` | C5_logprob | MATRIX | 1.0000 | 2 | 2 | Log-probability confidence for the stock belonging to the 2nd quantile (third… |
| `prob_quantile_5_bucket_2_5day_volatility` | C5_logprob | MATRIX | 0.9865 | 4 | 4 | Log-softmax confidence score that the stock belongs to the 2nd quantile bucke… |
| `prob_quantile_5_bucket_3_10day_return` | C5_logprob | MATRIX | 0.9865 | 6 | 6 | Log-probability confidence for being in the 4th quantile (quantile 3 out of 5… |
| `prob_quantile_5_bucket_3_20day_return` | C5_logprob | MATRIX | 0.9865 | 2 | 2 | Log-probability that the stock-date belongs to the 4th quantile (index 3) out… |
| `prob_quantile_5_bucket_3_50day_return` | C5_logprob | MATRIX | 0.9865 | 4 | 3 | Log-probability confidence (log-softmax) of the stock-date belonging to quant… |
| `prob_quantile_5_bucket_3_5day_return` | C5_logprob | MATRIX | 0.9865 | 4 | 4 | Probability that the stock falls into bucket 3 of quantile 5 for predicted 5-… |
| `prob_quantile_5_bucket_3_5day_volatility` | C5_logprob | MATRIX | 0.9865 | 1 | 1 | Log-softmax confidence score that the stock belongs to the 3rd quantile bucke… |
| `prob_quantile_5_bucket_4_10day_return` | C5_logprob | MATRIX | 0.9865 | 30 | 24 | Log-probability (log-softmax confidence) that the stock-date belongs to the t… |
| `prob_quantile_5_bucket_4_20day_return` | C5_logprob | MATRIX | 0.9865 | 48 | 37 | Log-probability that the stock-date belongs to the highest quintile (quantile… |
| `prob_quantile_5_bucket_4_50day_return` | C5_logprob | MATRIX | 0.9865 | 3 | 3 | Log-probability (log-softmax confidence) that the stock-date belongs to the 4… |
| `prob_quantile_5_bucket_4_5day_return` | C5_logprob | MATRIX | 0.9865 | 10 | 8 | Log-probability confidence for the stock belonging to the 4th quantile (top b… |
| `prob_quantile_5_bucket_4_5day_volatility` | C5_logprob | MATRIX | 0.9865 | 2 | 2 | Log-probability (log-softmax confidence) of the stock-date belonging to the t… |
| `likelihood_quantile_5_group_0_50day_return` | D_likelihood | MATRIX | 0.9865 | 6 | 6 | Log-probability confidence (log-softmax) of the stock-date belonging to quant… |
| `likelihood_quantile_5_group_2_50day_return` | D_likelihood | MATRIX | 0.9865 | 2 | 1 | Log-probability confidence (log-softmax) of the stock-date belonging to quant… |
| `rolling_250day_return` | E_context | MATRIX | 1.0000 | 19 | 18 | Return calculated over the previous 250 trading days. |

## 3. 设计含义（写死，后续波次照此）

1. **连续回归头是唯一可直接作"预期收益"的信号族**：`quantile_1_assignment_{5,10,20,50}day_return`。
   aC 仅 8–12 ⇒ 本数据集**最冷门**的可用族，正交性优先从这里取。
2. **分桶头不作主信号**：整数桶经 `group_rank` 只剩 N 档，权重天然集中。只作
   `trade_when` 条件 / `group_rank` 分组 / 与连续头的交叉验证。
3. **对数概率必须取差**：`prob_..._bucket_4_X − prob_..._bucket_0_X` 是 top/bottom 的对数几率，
   等价于模型隐含的排序分数；单桶绝对值混入了"模型整体确定性"，不可比。
4. **cov 0.987 ⇒ 必带 `ts_backfill(·, 252)`**（3% 缺失不 backfill 会掉覆盖、触发 CW）。
5. **aC 结构极端**：`close_return_quantile_1_1day` aC 418（占全集中近一半使用量，拥挤）；
   其余 99 个字段 aC ≤ 54。⇒ **正交空间在冷门字段侧**，1 日 close 只作基准对照。
6. **6 个 horizon（5/10/20/50 日收益 + 5 日波动）构成期限结构**：同机制的跨 horizon 一致性
   是最廉价的正交/稳健检验（若 5d 与 50d 同号同强，则信号不是单一时点噪声）。

## 4. Wave 47A 设计（10 臂 / 5 机制）

统一壳（USA 冠军壳，2026-10-18 起跨数据集复现）：

```
quantile(group_rank(hump(ts_backfill(winsorize({core}, std=4), 252), hump=0.01), subindustry))
```

设置：USA / TOP3000 / D1 / SUBINDUSTRY / decay 5 / truncation 0.08 / VERIFY / nan ON。

| # | tag | core | 机制 | 可证伪假设 |
|---|---|---|---|---|
| A1 | pred20_level | `quantile_1_assignment_20day_return` | M1 预期收益水平 | 20 日预期收益的横截面排序有正 IC |
| A2 | pred5_level | `quantile_1_assignment_5day_return` | M1 | 短端（5d）IC 强于 20d ⇒ 信号是短期反应而非漂移 |
| A3 | pred10_level | `quantile_1_assignment_10day_return` | M1 | 10d 位于 5/20 之间，用于确认 horizon 单调性 |
| A4 | pred50_level | `quantile_1_assignment_50day_return` | M1 | 50d 更慢 ⇒ 换手更低、Sharpe 可能更高（慢变量优势） |
| A5 | logodds20 | `prob_q5_b4_20d − prob_q5_b0_20d` | M2 对数几率 | 概率差比连续回归头更抗噪（分类头样本更多） |
| A6 | logodds10 | `prob_q5_b4_10d − prob_q5_b0_10d` | M2 | 同 A5，短端 |
| A7 | logodds5 | `prob_q5_b4_5d − prob_q5_b0_5d` | M2 | 5d 对数几率若最弱 ⇒ 短端是噪声 |
| A8 | revision22 | `ts_av_diff(quantile_1_assignment_20day_return, 22)` | M3 模型修正 | 预测的**变化量**（修正）比水平更正交（analyst 族已验证的机制） |
| A9 | term_20m5 | `pred20 − pred5` | M4 期限结构 | 长端相对短端的增量有独立信息（预期加速） |
| A10 | pred1d_close | `close_return_quantile_1_1day` | M5 1 日连续（基准） | 最拥挤字段（aC 418）作对照，用于估计"饱和度" |

**预注册判据**（收批即判，不事后调口径）：S ≥ 1.58 / F ≥ 1.0 / 2Y ≥ 1.58 / TO 0.01–0.70 /
SUB ≥ 0.43×S / risk_neut ≥ 0.3。任一条不过先归因（是 horizon、是算子壳、还是信号本身弱），
再决定下一波是加固还是判死；**同族不得磨参数**。

## 5. 结果（47A 收批，10/10 入库）

multisim `1a5MlW4S94Jn8VFQ5ci7wJz`，10 子模拟全部 COMPLETE，10 行已入 `backtest_results`
（wave = `s2_earnings_chart_dl_d1`，verdict = **FAIL** 0/10）。

| # | tag | alpha | S | F | TO | RET | 2Y | DD | 判决 |
|---|---|---|---:|---:|---:|---:|---:|---:|---|
| A1 | pred20_level | `3qjG7226` | 0.53 | 0.16 | 0.74% | 1.11% | — | 5.81% | ✗ |
| A2 | pred5_level | `kqJ83YY8` | −0.04 | −0.00 | 0.76% | −0.08% | — | 7.16% | ✗ |
| A3 | pred10_level | `LL58p2wa` | 0.43 | 0.11 | 0.74% | 0.85% | — | 4.56% | ✗ |
| A4 | pred50_level | `vROYLobz` | 0.67 | 0.23 | 0.75% | 1.45% | — | 4.43% | ✗ |
| A5 | logodds20 | `3qjG72OX` | 0.57 | 0.18 | 0.78% | 1.23% | — | 5.15% | ✗ |
| A6 | logodds10 | `YPxlp9Oo` | 0.66 | 0.23 | 0.76% | 1.55% | — | 8.77% | ✗ |
| A7 | logodds5 | `qME5AwJZ` | 0.47 | 0.14 | 0.81% | 1.10% | — | 8.49% | ✗ |
| A8 | revision22 | `xA1lxEpn` | **−0.37** | −0.11 | 0.72% | −1.12% | — | **15.71%** | ✗ |
| **A9** | **term_20m5** | **`P0MPpAmx`** | **0.69** | **0.23** | 0.75% | **1.34%** | — | 4.59% | ✗ 全批最强 |
| A10 | pred1d_close | `leMgVNPn` | 0.07 | 0.01 | 0.75% | 0.13% | — | 6.78% | ✗ |

**五条归因（先归因后判死，不磨参数）**

1. **缺口在 returns，不在 turnover —— 这条决定了「不能靠调设置救」。**
   全批 TO 0.72%–0.81%，10/10 吃 `LOW_TURNOVER`。但 `F = S × sqrt(|RET| / max(TO, 0.125))`，
   **TO < 12.5% 时分母恒为 0.125** ⇒ 把换手从 0.75% 抬到 12% 对 F **一个点都不加**。
   要 F ≥ 1.0 在 S 1.58 时需要 **RET ≥ 5.0%**，而本批最高 RET = 1.55%（A6）——**差 3.2 倍**。
   ⇒ 后续任何「修换手 / 加 decay / 换 hump 档」的尝试都是错方向，这是 46B 结论在本集的第二次复现。
2. **模型信号是慢的、长端的；短端是噪声。** horizon 单调链 **A4(50d) 0.67 > A1(20d) 0.53 >
   A3(10d) 0.43 > A2(5d) −0.04** 完整成立；A9（20d−5d 期限结构）0.69 为全批最高，说明
   「长端相对短端的增量」比任一端单独都干净。A10（1 日头，aC 418 全数据集最拥挤）S 0.07 平掉，
   **拥挤度与信号强度在本集无关**——它不是「被人挖走了」，是这个 1 日头本身就是噪声。
3. **`ts_av_diff` 修正腿是反向的（−0.37，DD 15.71% 全批最差）。**
   与 analyst 族（`e76xgXkM`，修正方向正、S 1.89）**符号相反**。解释：分析师修正反映
   *信息扩散的滞后*（post-revision drift）；CNN 预测的变化反映*预测自身的均值回复*（模型对
   近期价格过度反应后再回摆）。⇒ **「修正」这类机制不可跨数据源移植**，必须按数据源的生产
   过程重新定向，不能套用同一条算子。
4. **分类头（log-odds）只在 10d 优于连续回归头**（A6 0.66 vs A3 0.43），20d 基本相同
   （0.57 vs 0.53），5d 反向（0.47 vs −0.04，但两者都无意义）。分类头样本更多、对尾部更稳健，
   但**不足以把弱信号变成强信号**——它改的是信噪比的小数位，不是量级。
5. **最强臂 0.69 距 S ≥ 1.58 差 2.3 倍，且没有任何一条设置/壳层杠杆能提供这种量级的乘数**
   （全仓历史最大单杠杆跨度约 1.4×：见 pv20 中性化 0.93→1.37、46B `ts_av_diff` 1.13→1.31）。
   ⇒ **D15 探针失败**，本数据集判死，不再加变体；字段本身（图像模型的三个输出头）不构成本区的
   可挖信号源。

> **可复用结论（写入跨数据集经验）**：**「低频 + 低换手 + 低 aC」不等于「有 alpha」。**
> earnings_chart_dl 同时满足三个「看起来好」的先验（cov 0.991、aC 1006 属中低拥挤、100 字段
> 全是 DL 预测），但 10 臂最高 S 0.69 / RET 1.55%。真正的判据是**该字段是否携带对未来收益的
> 横截面排序信息**——DL 预测头预测的是「收益的幅度与分位」，不是「相对强弱」，在
> `group_rank` 壳下被中和掉大半。**下次选 DL 集时先看输出头语义是 cross-sectional score
> 还是 return forecast，后者要换成「相对预测」的构造（如 `pred_i − group_mean(pred)`）
> 才可能出信号。**
