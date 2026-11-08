# S1 · Risk 字段画像与机制声明（KOR / TOP600 / D1）

## risk59 Securities Lending（16 VECTOR，cov 0.981）
| 字段 | aC | 语义 | 角色 |
|---|---:|---|---|
| rsk59_indicativeavailability | 122 | 可借券量 | 供给 |
| rsk59_daystocover10day | 104 | 空头回补天数(10d) | **主信号** |
| rsk59_s3utilization | 67 | 空头占可借量比 | **主信号** |
| rsk59_squeeze_risk | 58 | 挤压风险综合分 | **主信号** |
| rsk59_bid_rate | 56 | 出借费率(年化%) | **主信号** |
| rsk59_daystocover30day | 49 | DTC(30d) | 稳健版 |
| rsk59_short_interest | 40 | 实时空头股数 | 存量 |
| rsk59_shortinterestpct | 25 | 空头占流通比 | 存量 |
| rsk59_crowded_score | 18 | 空头拥挤分 | 辅 |
| rsk59_short_momentum | 13 | 空头动量 | 辅 |

## risk70 MFM2（96 MATRIX，cov 0.980，aC 8018 **最挤**）
| 字段 | aC | 语义 | 角色 |
|---|---:|---|---|
| rsk70_mfm2_asetrd_dsrt | 1063 | 特异收益 | **主信号（反转）** |
| rsk70_mfm2_asetrd_resvol | 1006 | 残差波动载荷 | **主信号（idvol）** |
| rsk70_mfm2_asetrd_srisku | 588 | 未调整初始特异风险 | 风险量 |
| rsk70_mfm2_asetrd_srisk | 473 | 最终特异风险 | 风险量 |
| rsk70_mfm2_asetrd_cnt_kor | 428 | **韩国国家因子载荷** | KOR 专属 |
| rsk70_mfm2_asetrd_srtindcnt | 1431 | 行业载荷 | 中性化轴候选 |

> 其余 90 个为风格载荷（anlystsn/earnyild/btop/size/momentum/ltrevrsl…）——**纯风格暴露，prod 易撞墙**，后置。

## risk68 Forecast（5 MATRIX，cov 0.991）
| 字段 | aC | 语义 | 角色 |
|---|---:|---|---|
| rsk68_weight_volatility_short | 525 | 短期波动估计 | idvol |
| rsk68_residual_return | 180 | 特质 1 日收益 | **主信号（反转）** |
| rsk68_weight_edadv | 99 | 指数衰减美元成交额 | 规模/流动性壳 |
| rsk68_beta | 74 | beta | **主信号（BAB）** |

## risk88 / 71 / 72
- risk88：`rsk88_mfm_ase1_dsrt`(297) 特异收益；`ri_*` 风格载荷；`ind_*` 行业载荷（ASI 前缀）
- risk71/72：`*_dsrt` 特异收益，cov 0.62–0.76 偏低，**需逐年空窗复核**

## A-2 收益来源声明（五问）

### M1 特异收益反转（rsk68_residual_return / rsk70_dsrt）
- 谁被定价：**流动性提供者**（吃下特质性订单流的一方）
- 为什么错：特质性价格压力无信息含量，做市方要求补偿；散户过度外推
- 修复期：**数日**（5–22 日）
- 预期方向：特异收益高 ⇒ 后续**跌** ⇒ 反臂做空高 dsrt

### M2 融券约束溢价（rsk59_bid_rate / s3utilization / shortinterestpct）
- 谁被定价：**受借券约束的卖空方**
- 为什么错：借券稀缺 ⇒ 卖空受限 ⇒ 高估无法被套利纠正（D'Avolio 2002）
- 修复期：**数周–数季**
- 预期方向：费率高/利用率高 ⇒ 未来**负**收益

### M3 空头挤压（rsk59_squeeze_risk）
- 谁被定价：**拥挤空头**
- 为什么错：逼平引发正反馈买盘，价格超调
- 修复期：**数日–数周**
- 预期方向：挤压风险高 ⇒ 短期**正**收益（做多高挤压）

### M4 特异波动异象（rsk70_resvol / srisk / rsk68_weight_volatility_short）
- 谁被定价：**彩票偏好投资者**
- 为什么错：高特质波动被高估（Ang et al. 2006）
- 修复期：**数季**
- 预期方向：高 idvol ⇒ 未来**低**收益

### M5 低 beta 异象（rsk68_beta）
- 谁被定价：**杠杆受限投资者**
- 为什么错：追高 beta 抬价（Frazzini-Pedersen BAB）
- 修复期：**数月**
- 预期方向：高 beta ⇒ 风险调整后**低**收益

## 禁用/慎用
- `rsk70_*_srtindcnt`（行业载荷）：直接当信号=行业轮动，应先作中性化轴
- 纯风格载荷（earnyild/btop/size/momentum）：属其他塔经济内容，prod 易撞
- risk59/60 全为 VECTOR ⇒ **必须 vec_avg**
