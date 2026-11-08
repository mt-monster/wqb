# FINDING P91 · intraday_pv_feats 反转臂全闸突破（2026-11-08）

数据集：`intraday_pv_feats`（category=pv，574 字段，alphaCount=147）· KOR/TOP600/D1
设置：REVERSION_AND_MOMENTUM · decay 8 · trunc 0.08 · nanHandling OFF · 2014-2023
批次：`3jYIT2aSH4Eoa441gbOD2ehJ`（10 条，0 错）

## 一、核心突破：真反臂把 −3.04 变成 +2.82

P90 裸臂 `group_rank(corr_ask_price_with_volume, industry)` = **S −3.04 / TO 0.7238**。
P91 改用 `subtract(0.5, group_rank(...))` 做真反臂（零均值，见铁律「multiply(-1) 不是镜像」），并加 `ts_mean(22)` 平滑，得到全闸候选族。

| alpha | 表达式（简） | S | F | 2Y | TO | ret | raF |
|---|---|---:|---:|---:|---:|---:|---:|
| d5Wvb6Yj | subtract(0.5, group_rank(corr_ask_price_with_volume, industry)) | **2.82** | 1.60 | 2.11 | 0.5513 | 0.1765 | 1 (CONCENTRATED_WEIGHT) |
| akKGb8w9 | subtract(0.5, multiply(rank(momentum1_vwap_first_half_volume), rank(corr_ask_price_with_volume))) | 2.23 | 1.08 | 1.71 | 0.6048 | 0.1421 | 1 |
| **O0AgNjgv** | **subtract(0.5, group_rank(ts_mean(corr_bid_price_with_volume, 22), industry))** | **1.99** | **1.99** | **2.72** | **0.1299** | 0.1304 | **0** |
| omEZLXJJ | ts_target_tvr_decay(反臂, target_tvr=0.30) | 1.97 | 1.64 | 1.58 | 0.2005 | 0.1385 | 1 |
| A1VEN5ze | subtract(0.5, group_rank(ts_mean(corr_high_price_with_volume, 22), industry)) | 1.93 | 1.93 | **2.89** | 0.1302 | 0.1301 | 0 |
| YP1YbOYM | subtract(0.5, group_rank(ts_mean(corr_last_trade_price_with_volume, 22), industry)) | 1.93 | 1.87 | 2.66 | 0.1309 | 0.1228 | 0 |
| QPv6bAOw | subtract(0.5, group_rank(ts_mean(corr_ask_price_with_volume, 22), industry)) | 1.86 | 1.84 | 2.85 | 0.1309 | 0.1275 | 0 |
| JjerNkzm | subtract(0.5, group_rank(ts_rank(corr_high_price_with_volume, 22), country)) | 1.51 | 0.57 | 0.84 | 0.6182 | 0.0887 | 4 |
| MPYVane8 | subtract(0.5, group_rank(ts_mean(corr_ask_price_with_volume, 66), industry)) | 1.35 | 1.21 | 1.81 | 0.0904 | 0.1003 | 1 |
| VkxeaL5Y | subtract(0.5, group_rank(ts_mean(kurtosis_last_trade_price_interval, 22), industry)) | 0.51 | 0.23 | 1.15 | 0.1246 | 0.0249 | 4 |

## 二、四条 raF=0 全闸候选是同一个信号

`compute_mutual_correlation([O0AgNjgv, A1VEN5ze, YP1YbOYM, QPv6bAOw])`：
两两 **0.9744 – 0.9907**，`all_below_threshold=false`，`max_mutually_below_subset_size = 1`。

⇒ **四者只能取 1 颗**。选 **O0AgNjgv**（S 1.99 最高、F 1.99 最高、2Y 2.72、TO 0.1299）。
原因：`corr_bid/ask/high/last_trade_price_with_volume` 是同族字段（价格-成交量相关系数），语义高度重叠，不构成结构位移。与既有铁律「只换字段而同族 → 不算新颗」一致。

## 三、三条新铁律

### 铁律 A：`ts_mean(22)` 平滑对「裸臂高换手」信号是提 S + 降 TO 的双赢，不是妥协
- 裸臂 `corr_ask_price_with_volume`：S −3.04 / TO 0.7238（TO 超 0.7 闸）；
- 加 `ts_mean(22)` 后反臂：S +1.86 / TO 0.1309（TO 降 82%、S 仍 1.86）；
- `ts_mean(66)` 过度平滑：S 1.35（衰减）。**22 日是谷底（周/月同尺度）**。
这与 chart_cnn 上的结论相反——那里裸信号 TO 0.2551 已低通，再平滑就死。**判据是裸臂 TO**：TO>0.5 必须平滑且平滑是增益；TO<0.35 禁止平滑。

### 铁律 B：相关性类字段（`corr_X_with_Y`）在 KOR 上系统性反向有效
四个价格-成交量相关字段的反臂全部 S 1.86–1.99、2Y 2.66–2.89、TO 0.13。
经济机制：日内「价涨量增」相关越高 = 追涨散户越多 / 动量拥挤，次月反转。KOR 散户占比高，与 Heston-Korajczyk-Sadka (2010) 的日内截面可预测性一致。
⇒ 该族可作为「短周期反转」的杠杆源，反臂（`subtract(0.5, rank(...))`）才是正收益方向。

### 铁律 C：高 S 裸臂会被 CONCENTRATED_WEIGHT 卡，而平滑版同时解决这个闸
`d5Wvb6Yj` S 2.82 但 raF=1（CONCENTRATED_WEIGHT，TO 0.5513 集中持仓）；`O0AgNjgv` 平滑后 TO 0.1299 → 权重分散 → CONCENTRATED_WEIGHT 消失且 S 仍 1.99。
**不要为了保高 S 去死磕集中度闸，改平滑即可同时拿 S + 过闸**。

## 四、待办
- [ ] O0AgNjgv prod 相关性（`zq3eb7No` 占用后已启动，pending）
- [ ] 通过后提交（交付第 5 颗）
- [ ] 该数据集第二颗：必须换非 `corr_*_with_volume` 的语义族（`skew_bid_size_to_ask_size_ratio` / `kurtosis_*` / `momentum1_vwap_*`）