# FINDING P85–P90：三个新数据集首轮定性与「强负信号」线索

日期：2026-11-08 · KOR / TOP600 / D1

## 一、判死清单（本轮新增）

| 数据集 | 类别 | 字段 | 最优读数 | 判死依据 |
|---|---|---:|---|---|
| predictive_starmine | model | 645 | S0.73 / 2Y0.83 | 10 模板全落 0.08–0.73，ARM/预测惊喜/修订广度全军覆没 |
| chart_cnn_alpha | model | 1010 | S1.36 / 2Y1.87 | 2Y 已过线但 S 天花板 1.36，几何/放大/正交全扫尽 |
| pattern_scores | pv | 504 | — | 同族 continuation_score 已证伪（最高 0.94），不重复投入 |
| fund_holdings_panel | institutions | 30 | — | 交付文档 §5.2 已判死（四几何最高 0.87） |

## 二、chart_cnn_alpha：2Y 解决但 S 卡死（最有价值的失败）

| alpha | 几何 | S | F | 2Y | TO | raF |
|---|---|---:|---:|---:|---:|---:|
| 3qoJ9MxP | group_rank(prob4 x confscore4, industry) | **1.36** | 0.79 | 1.63 | 0.2545 | 2 |
| d5WvO27j | prob4-prob0 @ sector | 1.30 | 0.77 | 1.62 | 0.2445 | 2 |
| 88RX3Yel | signed_power(·, 1.5) | 1.35 | 0.49 | 1.60 | 0.5253 | 2 |
| xAr5YKmb | ts_mean(prob4 x confscore4, 5) | 1.23 | 0.78 | **1.87** | 0.1695 | 2 |
| rKR85V29 | ts_target_tvr_decay 控换手 | 1.23 | 0.71 | 1.64 | 0.2286 | 2 |

**结论**：2Y 已经不是本数据集的问题（1.6–1.9），问题纯粹是 Sharpe 差 0.22。
已扫尽的 S 杠杆：分组轴 4 种 / decay 4·22 / 单腿·价差·加权·双桶和 / leaps 换族 / signed_power 1.5·2·2.5 / ts_mean 平滑 / tvr 控换手。

### ★ vector_neut 正交化在此类数据集上会杀死信号（新铁律）

复用 risk70 已验证的正交化骨架（`vector_neut(rank(A), rank(B))`）在本集完全失效：

| 组合 | S | 2Y |
|---|---:|---:|
| vector_neut(rank(prob4), rank(leaps_quintile4)) | **-0.00** | -0.18 |
| vector_neut(rank(prob4xconf), rank(leaps)) | 0.52 | 0.47 |
| vector_neut(rank(prob4), rank(confscore)) | -0.82 | -1.13 |

**机理**：risk70 的正交化之所以有效，是因为两条腿都是**因子载荷**（存在大额共同市场分量，剥离后残余仍有信息）。
而这里的概率/置信度腿是 **CNN 输出的有界概率 [0,1]**，`rank()` 后几乎全是共同单调分量，投影后残余趋零。
**判据**：正交化只适用于「同类载荷、高共同分量」的双腿（风险因子暴露、行业暴露）；概率/置信度类双腿禁用 vector_neut，改用 `multiply`（共振）或 `subtract`（价差）。

## 三、intraday_pv_feats：首轮全负，但暴露强负信号（本轮最大线索）

| alpha | 几何 | S | 2Y | TO |
|---|---:|---:|---:|---:|
| WjOJP58x | group_rank(corr_ask_price_with_volume, industry) | **-3.04** | -2.64 | 0.7238 |
| kqN9VA5d | momentum1_vwap x corr_ask_price_with_volume | **-2.78** | -2.23 | 0.7581 |
| 78LlZpOZ | ts_rank(corr_high_price_with_volume, 8) | -1.88 | -1.21 | 0.8216 |
| E56xvdAm | group_rank(kurtosis_last_trade_price_interval) | -1.39 | -1.82 | 0.7841 |
| mLoQgvkx | group_rank(skew_bid_size_to_ask_size_ratio) | -0.69 | -0.48 | 0.6828 |

全 10 条仅一条微弱正（0.11），其余全负。**负得越强的恰是「价量相关性」族**（ask/bid/last 价格与成交量的日内相关系数）。
经济含义：日内「价格上涨伴随放量」越强（追涨），后续负收益越强 —— 韩国的日内追涨反转效应。

**两个待解问题**（P91 正在测）：
1. 真反臂是否成立：按铁律必须写 `subtract(0.5, group_rank(x))`，不能用 `multiply(...,-1)`。
2. 换手：原臂 TO 0.68–0.82，超出 HIGH_TURNOVER 闸；P91 用 ts_mean(22/66) + decay8 + ts_target_tvr_decay 三条路径降 TO。

## 四、metrics 读表坑

两年 Sharpe 的键名是 **two_year_sharpe**，不是 sharpe_2y。误读会误判「2Y 缺失」。
