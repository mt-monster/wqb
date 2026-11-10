# KOR × TOP600 × D1 · ATOM REGULAR 已验收交付快照（6 / 20）

> 快照时点：2026-11-08 · 区间 2014-01-01 ~ 2023-12-31 · 全部 get_alpha_details 实测复核
> 目标 20 颗，当前已验收 **6 颗**（缺口 14；KOR 现实上限受 prod 白空间 + 新机制普遍弱约束）。
> 本文件为干净交付件清单；滚动战役日志见 `DELIVERY_KOR_ATOM.md`。

## 验收口径（全部满足）
type=REGULAR 且单数据集 ATOM · failed_ra_count=0 · S≥1.58 · 2Y≥1.58 · F≥1.0 · 2014–2023 逐年 longCount>0 且 pnl≠0 · self<0.70 · prod<0.70 · 算子数≤12 · 篮子互相关全对<0.5。

## 交付清单（6 颗）

| # | alpha | 数据集 | 塔 | S | F | 2Y | TO | subU | self | prod | 算子数 | 状态 |
|---|---|---|---|---:|---:|---:|---:|---:|---:|---:|---:|---|
| 1 | omERn83n | risk70 | RISK | 1.62 | 1.23 | 2.27 | 0.1319 | 1.31 | 0.4211 | 0.6898 | 9 | 待提交 |
| 2 | qMLOooX1 | analyst10 | ANALYST | 1.94 | 1.74 | 1.76 | 0.0972 | 1.71 | 0.3939 | 0.6941 | 6 | 待提交 |
| 3 | RRE9NkVj | insiders5 | INSIDERS | 1.76 | 1.63 | 2.77 | 0.0968 | 1.70 | 0.3104 | 0.6605 | 4 | **已上线 ACTIVE** |
| 4 | d5Wvpmbx | risk68 | RISK | 1.82 | 1.25 | 4.10 | 0.2461 | 1.75 | 0.2023 | 0.6906 | 5 | 待提交 |
| 5 | ZYQ116ln | intraday_pv_feats | PV | 1.86 | 1.10 | 1.80 | 0.2205 | 1.55 | 0.1426 | 0.6981 | 3 | 待提交 |
| 6 | LLZ6wZO2 | oth466 | FUNDAMENTAL | 1.99 | 1.53 | 2.24 | 0.1440 | 1.21 | 0.6760 | 0.6762 | 5 | 待提交 |

**篮子互相关**：全对 <0.5（最大对 0.3176，compute_mutual_correlation threshold=0.5 最大独立集=6）。

## 逐颗明细（表达式 / 核心字段 / 算子逻辑 / 设置）

### 1. omERn83n · risk70（分析师情绪载荷正交化）
```
ts_target_tvr_decay(signed_power(group_rank(winsorize(vector_neut(rank(ts_backfill(rsk70_mfm2_asetrd_anlystsn, 40)), rank(ts_backfill(rsk70_mfm2_asetrd_momentum, 22))), std=0.38), sector), 2.5), target_tvr=0.22)
```
- 核心字段：rsk70_mfm2_asetrd_anlystsn（信号）/ rsk70_mfm2_asetrd_momentum（正交腿）
- 逻辑：rank→vector_neut 剥动量共线→winsorize→signed_power(2.5)→group_rank(sector)→ts_target_tvr_decay(0.22) 控换手
- 设置：REVERSION_AND_MOMENTUM · decay1 · trunc0.04 · nanON
- 画像：reference/datasets/risk70.md

### 2. qMLOooX1 · analyst10（SmartEstimate 双惊喜共振）
```
group_neutralize(multiply(group_rank(ts_av_diff(anl10_smartest_sal_fy2_pred_surps_v1,250),sector),group_rank(ts_av_diff(anl10_smartest_net_fy1_pred_surps_v1,250),sector)),industry)
```
- 核心字段：anl10_smartest_sal_fy2_pred_surps_v1 / anl10_smartest_net_fy1_pred_surps_v1
- 逻辑：FY2 营收惊喜与 FY1 净利惊喜各 ts_av_diff(250)→group_rank(sector)→相乘共振→group_neutralize(industry)
- 设置：REVERSION_AND_MOMENTUM · decay4 · trunc0.08 · nanON

### 3. RRE9NkVj · insiders5（内部人申报分歧度，Miller 1977）
```
subtract(0.5, group_rank(ts_mean(vec_stddev(insd5_vol_chg), 55), sector))
```
- 核心字段：insd5_vol_chg（内部人股数变动，VECTOR）
- 逻辑：vec_stddev 取多笔申报分歧度→ts_mean(55) 平滑稀疏事件→group_rank(sector)→subtract(0.5,·) 做多低分歧/做空高分歧
- 设置：REVERSION_AND_MOMENTUM · decay4 · trunc0.08 · nanOFF
- 画像：campaign_20261106_insiders_atom/s1_field_profile_insiders5.md · 已提交 2026-11-06

### 4. d5Wvpmbx · risk68（波动权重价差）
```
subtract(group_rank(ts_delta(rsk68_weight_volatility_short, 22), sector), group_rank(ts_delta(rsk68_weight_dadv, 22), sector))
```
- 核心字段：rsk68_weight_volatility_short / rsk68_weight_dadv
- 逻辑：双权重各 ts_delta(22)→group_rank(sector)→价差（同源单经济含义合规）
- 设置：REVERSION_AND_MOMENTUM · decay4 · trunc0.08 · nanOFF

### 5. ZYQ116ln · intraday_pv_feats（买价-买量相关反转）
```
subtract(0.5, group_rank(ts_mean(corr_bid_price_with_bid_size, 22), industry))
```
- 核心字段：corr_bid_price_with_bid_size
- 逻辑：ts_mean(22)→group_rank(industry)→subtract(0.5,·) 真反臂；SLOW+decay2 破 prod 墙（0.7827→0.6981）
- 设置：SLOW · decay2 · trunc0.08 · nanOFF

### 6. LLZ6wZO2 · oth466（盈利质量 ROA 窗口谷）
```
quantile(group_rank(ts_rank(group_rank(divide(oth466_is_consol_net_inc_q, oth466_bs_assets_tot_q), industry), 420), market))
```
- 核心字段：oth466_is_consol_net_inc_q / oth466_bs_assets_tot_q（合并净利/总资产）
- 逻辑：divide(ROA)→group_rank(industry)→ts_rank(420) 窗口谷压 prod→group_rank(market)→quantile
- 设置：STATISTICAL · decay4 · trunc0.08 · nanOFF

## 提交说明
除 RRE9NkVj 已 ACTIVE 外，其余 **5 颗 UNSUBMITTED 待用户明确确认**后走 worldquant-submit-alpha（提交当刻须 refresh 重测 prod）。

## 字段画像存档索引
- risk70：reference/datasets/risk70.md
- insiders5：campaign_20261106_insiders_atom/s1_field_profile_insiders5.md
- 本战役新测画像：reference/datasets/other424.md / other436.md / other327.md（均弱死）；other335.md（弱活 S1.14）
- 全塔审计闭合：DELIVERY_KOR_ATOM.md §20.11–20.12
