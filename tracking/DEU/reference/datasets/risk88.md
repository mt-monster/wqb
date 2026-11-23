# risk88 字段画像（DEU / TOP500 / D1）

> 建档 2026-11-23。数据源 `get_datafields(region=DEU, universe=TOP500, delay=1, dataset_id="risk88", filter_sharpe=false)`。

## 字段全表（1 字段，MATRIX）

| 字段 id | 类型 | coverage | alphaCount | userCount | dateCreated | description |
|---|---|---:|---:|---:|---|---|
| `alternative_market_cap_usd` | **MATRIX** | **1.0** | 82 | 48 | 2026-07-01 | Market capitalization of each stock expressed in US dollars (stocks×dates matrix used for weighting/normalization) |

**机制：1 条 —— 规模因子（size premium）。** 单字段数据集，模板空间只来自「如何刻画规模」。

## 实测（2026-11-23，10 臂 L1 结构筛，SUBINDUSTRY / d8 / trunc 0.08 / nan ON）

| 结构 | 表达式 | alpha | S | F | 2Y | TO | sub | sub/S | RA |
|---|---|---|---:|---:|---:|---:|---:|---:|---:|
| 相对 252 日均值 | `group_rank(divide(mcap,ts_mean(mcap,252)),sector)` | `vRA7dO6z` | **0.54** | 0.34 | 0.31 | 5.3% | **0.54** | **1.00 ✓** | 3 |
| 水平 z-score 252 | `group_rank(ts_zscore(mcap,252),sector)` | `ZYaVrmz0` | 0.52 | 0.29 | 0.27 | 6.9% | 0.42 | 0.81 ✓ | 3 |
| 水平 z-score 504 | `group_rank(ts_zscore(mcap,504),sector)` | `Jj8abPz2` | 0.52 | 0.30 | 0.22 | 5.5% | 0.46 | 0.88 ✓ | 3 |
| 时序分位 252 | `group_rank(ts_rank(mcap,252),sector)` | `npaG3AQx` | 0.51 | 0.28 | 0.30 | 8.8% | 0.42 | 0.82 ✓ | 3 |
| 规模变动 66 日 | `group_rank(ts_returns(mcap,66),sector)` | `omajVor6` | 0.12 | 0.03 | −0.08 | 8.0% | 0.42 | — | 3 |
| 规模波动率 | `group_rank(ts_std_dev(ts_returns(mcap,1),252),sector)` | `kqapQJ9k` | 0.12 | 0.04 | −0.49 | 2.4% | 0.08 | — | 3 |
| 规模变动 252 日 | `group_rank(ts_delta(mcap,252),sector)` | `Wjlr9LJj` | 0.01 | 0.00 | 0.39 | 4.7% | 0.18 | — | 3 |
| 22 日平滑变动 | `group_zscore(ts_mean(ts_returns(mcap,22),22),sector)` | `58JKMj2n` | −0.01 | −0.00 | −0.36 | 8.3% | 0.01 | — | 3 |
| 变动×规模相关 | `group_rank(ts_corr(ts_returns(mcap,1),mcap,252),sector)` | `mLanZYQ5` | −0.28 | −0.10 | −0.04 | 6.2% | −0.35 | ✗ | 4 |
| 变动对规模的残差 | `group_zscore(vector_neut(ts_returns(mcap,66),ts_zscore(mcap,252)),sector)` | `1YW3Jj0K` | −0.24 | −0.10 | −0.32 | 8.9% | 0.30 | — | 3 |

**三条结论**

1. **只有「规模水平」类结构有信号**（|S| 0.51–0.54），**全部低于 S 闸 1.58 达 1.04**，且 2Y 只有 0.22–0.31。
2. **变动/波动/相关/残差类结构全灭**（|S| ≤ 0.28）—— 与 risk60 相反：规模的信息在**水平**里，不在动态里。
3. 有意思的是 `divide(mcap, ts_mean(mcap,252))` 的 **sub·S⁻¹ = 1.00**（sub 与 S 同量级），
   说明「相对自身规模」这一形态的稳健性最好，但强度不足。

## 终判

**risks88 PROVISIONAL 关闭：单字段规模因子在 DEU 天花板 |S| 0.54，距闸 1.04。**
不再投入（S 差超过 1.0 时，任何层/轴/组合都无望，历史最成功的杠杆单层上限也只有 +0.27）。

## RISK 塔（DEU D1，0/3）汇总

| 数据集 | 字段数 | 机制 | 天花板 S | 卡点 | 状态 |
|---|---:|---|---:|---|---|
| risk60 | 5（全 VECTOR） | 借券费率 | **1.25** | S 差 0.33（其余全闸过 RA-1） | PROVISIONAL 关闭 |
| risk68 | 5（全 MATRIX） | 残差收益反转 | 1.51 | S↔2Y 严格互斥，无配置同时过 | 关闭 |
| risk71 | 10（全 cov 0.0） | 残差收益 | 1.27 | **TO 属性死**（裸 TO 90%，压制即死） | 关闭 |
| risk72 | 31（同族） | 残差收益 | — | 同 risk71 机制 | 未开波（同族） |
| risk88 | 1 | 规模因子 | 0.54 | S 差 1.04 | PROVISIONAL 关闭 |

**⇒ DEU RISK 塔（0/3）在当前字段集下不可点亮。**
