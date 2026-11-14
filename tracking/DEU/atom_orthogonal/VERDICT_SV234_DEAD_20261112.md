# 判死：只有 SV1（最大单笔交易）有信息，SV2/3/4 全无

日期：2026-11-12
BE168 multisim BQmxS9G24S1a8tT8PhDjsv（10 臂）

## 实测全灭

| 核心 | 搭档 | alpha | S | F | 2Y | sub | fail |
|---|---|---|---:|---:|---:|---:|---:|
| **SV2（第二大）** | AS3 | 6XM7ZEmL | **1.61** | 0.96 | 1.48 | 1.07 | 2 |
| SV2 | AS4 | 78YW3dAL | 1.58 | 1.24 | 1.56 | 0.89 | 1 |
| SV2+SV3+SV4 | AS3 | Jj8qodwm | 1.20 | 0.64 | 1.40 | 0.73 | 3 |
| SV3+SV4 | AS3 | O0WOR9Od | 1.00 | 0.52 | 1.12 | 0.65 | 3 |
| SV3 | AS3 | j2avogvW | 1.00 | 0.52 | 1.09 | 0.65 | 3 |
| SV4 | AS3 | 1YWeOgeW | 1.00 | 0.52 | 1.13 | 0.65 | 3 |
| SV3 | O4 | 1YWeOg9M | 0.93 | 0.61 | 1.58 | **0.07** | 4 |
| SV4 | O4 | P05Nx1aE | 0.93 | 0.61 | 1.53 | **0.08** | 4 |
| **SV2 单腿** | — | oma7RY5J | 0.82 | 0.46 | 1.57 | 0.41 | 3 |
| SV2+SV3+SV4 | AN1 | wpoq3exl | 0.62 | 0.32 | 0.79 | 0.66 | 3 |

## 判死结论

**insider_agg_matrix 的 `significant_value_1`（最大单笔）是唯一有信息的显著性字段。**
`significant_value_2/3/4`（第 2/3/4 大）全部无 alpha。

## 经济含义解释

这与「最重要的一笔交易最有信息量」的直觉一致：
- 最大单笔交易通常来自**最高级别的内部人**（CEO/CFO）或**最大规模的持仓变动**，
  这是最强信号；
- 第 2 大及以后的交易多为常规性小额操作（股权激励行权、例行减持），信息含量递减且被噪声主导；
- 与 HHI 用法一致：HHI = SV1/(SV1+SV2+SV3+SV4) 之所以只对 SV1 敏感，正因为分子是决定性的。

## insiders 数据集最终完整判决

| 维度 | 字段/定义 | 判定 |
|---|---|---|
| **持仓存量** | insd1_holdings（Δ66 / ts_ir / ts_rank252）| ✅ **核心，唯一强信号** |
| **最大单笔集中度** | significant_value_1 / (SV1+SV2+SV3+SV4) @66 | ✅ **最强单腿核心（C）** |
| 第 2/3/4 大交易 | significant_value_2/3/4 | ❌ 判死（本波）|
| 交易金额 | insd1_valueeur / insd1_value | ❌ 判死 |
| 交易股数占比 | insd1_shares / holdings | ❌ 判死 |
| 显著度评级 | insd1_tradesignificance | ❌ 判死 |
| 交易价 | insd1_price | ❌ 判死 |
| 方向指标 | directional_indicator（长窗 ts_sum 252）| ⚠ 单腿 0.51，仅可作辅助 |
| 买卖股数比 | total_buy/total_sell_shares | ❌ 判死 |
| 高管维度 | avg_top_buy/sell_shares | ❌ 判死 |

⇒ **insiders 的两个可用信息维只有：① holdings 存量变化 ② SV1 集中度。**
⇒ 所有可挖组合已穷尽，17 颗是按互相关<0.7 得到的实际上限附近。