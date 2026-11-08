# risk59 / risk68 收割与判死 · 2026-11-07

## risk59（证券借贷/做空，16 VECTOR 字段，cov 0.9806）

| alpha | 表达式 | S | F | 2Y | sub | TO | raFail |
|---|---|---:|---:|---:|---:|---:|---:|
| **9qxMnXg1** | **group_rank(vec_avg(rsk59_daystocover90day), sector)** | **+1.02** | 0.82 | 1.28 | **0.98** | 0.0864 | 3 |
| A1VzAdYX | −group_rank(vec_avg(rsk59_short_interest), sector) | −0.97 | −0.69 | −1.21 | −0.94 | 0.0682 | 5 |
| leAGoax8 | −group_rank(vec_avg(rsk59_short_momentum), sector) | −0.62 | −0.19 | −0.67 | −0.48 | 0.4325 | 6 |
| zq3GVzQ8 | −group_rank(vec_avg(rsk59_shortinterestpct), sector) | −0.53 | −0.28 | −1.15 | −0.51 | 0.0709 | 5 |
| leAGmjJ8 | −group_rank(vec_avg(rsk59_s3utilization), sector) | −0.49 | −0.24 | −0.79 | −0.23 | 0.0715 | 4 |
| 58E5PJRM | −group_rank(vec_avg(rsk59_crowded_score), sector) | −0.18 | −0.05 | −0.18 | 0.00 | 0.0786 | 4 |

### 读数
1. **符号整体反转**：经典「高空头 → 跑输」在 KOR 反向。翻正后 short_interest S +0.97 / 2Y +1.21；shortinterestpct +0.53 / 2Y +1.15。
   经济解释：KOR 空头拥挤度高 → 轧空压力大 → 后续跑赢。这与「逆向 + 低流动性溢价」的韩股画像一致。
2. **daystocover90day 是唯一独立强腿**：S **1.02**、sub **0.98**（全战役最高）、TO 0.0864。
   sub 闸判据 sub ≥ 0.474×S：推到 S 1.58 只需 sub ≥ 0.75，当前 0.98 有 30% 冗余 ⇒ **这条腿不会被 sub 闸拖死**，罕见。
3. crowded_score S −0.18 / sub 0.00 ⇒ 该字段无信息，弃。

## risk68（beta / dadv / 波动权重，3 MATRIX 字段，cov 1.0）—— 数据集判死

| alpha | 表达式 | S | F | 2Y | sub | TO |
|---|---|---:|---:|---:|---:|---:|
| bl6zezLZ | −group_rank(rsk68_weight_volatility_short, sector) | +0.34 | 0.17 | 0.06 | 0.44 | 0.1532 |
| MPYzJMaa | −group_rank(rsk68_beta, sector) | −0.53 | −0.28 | −0.96 | −0.47 | 0.0716 |
| YP1zRzAo | −group_rank(ts_zscore(rsk68_beta, 250), sector) | −0.53 | −0.25 | 0.24 | −0.28 | 0.0978 |
| omEGx8Wm | −group_rank(ts_av_diff(rsk68_beta, 66), sector) | −0.57 | −0.29 | −0.09 | −0.30 | 0.1307 |

**判死**：4 个字段、4 种几何（水平 / 年化 zscore / 时序去均值 / 波动权重），最大 |S| **0.57**。
低 beta 异象（BAB, Frazzini-Pedersen）在 KOR **反向**（高 beta 跑赢），但反向强度也只有 0.53，远不足 1.58。
⇒ risk68 整集封盘。

## 累计判死数据集（本战役）
news50 · news38 · news_sentiment_transfer · institutions6 · risk68 · insiders1(覆盖0.35) · imbalance5(单字段) · sentiment23(覆盖0.285) · sentiment21(覆盖0.35-0.47) · socialmedia39/other100(单字段) · macro63(单字段)

## 活口（唯一）
**risk59 / rsk59_daystocover90day** —— 精修波 P13 已派发。

## 论坛范式补充（31 赞帖：ts_min / ts_max 高维构建）
新增可复用几何：
- **Stochastic min-max 归一化**：`divide(subtract(X, ts_min(X,d)), add(subtract(ts_max(X,d), ts_min(X,d)), 0.0001))`
  作用：把任意字段压到 [0,1] 相对区间，**稳定截面权重、降 truncation loss 与 turnover**（相比 ts_zscore 不易被肥尾拉爆）。
- **通道挤压 regime 门**：`trade_when(channel_width < ts_min(channel_width,252)*1.25, signal, -1)`，用波动率挤压做开仓时机，大幅降 TO。
- **极值时间衰减**：`group_normalize(-ts_arg_max(volume,60), subindustry)` —— 刚发生突变（天数近）有短线信息溢价。
- **52 周新高锚定**：`close / ts_max(high, 252)`（George & Hwang 2004），比单纯动量更强更持久。**注意此式会引入内置价量字段，不适用于单数据集 ATOM。**
- **基本面突破挤压**：`income / ts_max(ts_delay(income,1), 756)`（突破 3 年盈利天花板）。

已把 min-max 归一化纳入 P13（替换冗余的 ts_mean(22) 变体）。
