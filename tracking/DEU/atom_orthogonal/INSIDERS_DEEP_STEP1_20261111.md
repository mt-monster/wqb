# INSIDERS 深挖战役 · Step 1（BE113/BE114，2026-11-11）

> 用户指令：专注 INSIDERS，深入挖掘，一步步走。
> DEU INSIDERS 类仅 2 集：insiders1（8 VECTOR，cov 0.53）+ insider_agg_matrix（34 MATRIX，cov 0.53/1.0）。
> 已知最优：insd1 ts_delta(ts_mean(H,66),66) S 1.06 / F 0.88；agg SV1/adv20 0.86；SV1 Σ66 0.85（2Y 1.57）。

## Step 1 · BE113 insiders1 未测机制（4wwcACdf64HIaDQdQKx88Z3）

| # | 构造 | 机制（来源） | 为何是新的 |
|---|---|---|---|
| 1 | Σ66 shares/(holdings+shares) | **真实仓位占比**（70赞帖的严格版：交易前持仓占比） | 旧版 shares/holdings 用交易后持仓当分母 |
| 2 | Σ66 valueeur/adv20(mean66) | 规模中性化价值流（Lakonishok-Lee 市值标准化） | insiders1 从未做规模中性 |
| 3 | Σ66 sig==3 × 仓位占比 | **只留高重要性交易**（供应商 1-3 分，3=高） | 旧版是乘法加权，未做硬门控 |
| 4 | ts_rank(holdings,252) | 持仓时序分位（内部人长期信心位置） | 未测 |
| 5 | ts_zscore(holdings,252) | 持仓时序标准化 | 未测 |
| 6 | Δ66 平滑 · **subindustry 轴** | 分组轴下沉（sector→subindustry） | 未测该轴 |
| 7 | decay22(Δ66 平滑) | 变化腿记忆平滑 | 未测该组合 |
| 8 | ts_rank(price,66) | 交易价格趋势（内部人成交价动量） | 未测 |
| 9 | tail 去并列（0.25/1.0）on 仓位占比 | 事件型低覆盖标准后处理（记忆配方） | 未测该腿 |
| 10 | Δ66 平滑 · **market 轴** | 分组轴升到全市场（对照） | 未测 |

## Step 2 · BE114 insider_agg_matrix 未测机制（4ggMhRamn4Dt9gqT765ypm2）

| # | 构造 | 机制 | 为何是新的 |
|---|---|---|---|
| 1 | Σ66 **top_significant_value_1** | **高管专属**最大单笔（CMP 2012：高管比董事知情） | 旧测的是全体 significant_value_1 |
| 2 | Σ66 directional_significant_value_1 | 方向调整后大额 | 未测 |
| 3 | directional_indicator_2 水平 | 供应商第二方向指标（cov 1.0） | 未测（旧测的是 indicator_1 且 TO 偏置） |
| 4 | avg_buy/total_buy | **鲸鱼集中度**（1/笔数，越大=单笔越重） | 未测 |
| 5 | total_buy/avg_buy | 买入**笔数代理**（广度） | 未测 |
| 6 | total_buy_shares/total_sell_shares | 股数口径买卖比（旧测的是金额口径 0.62） | 口径不同 |
| 7 | ts_rank(SV1,252) | 大额交易时序分位 | 未测 |
| 8 | ts_zscore(SV1,252) | 大额交易标准化 | 未测 |
| 9 | Σ66 significant_value_2 | 第二大笔（分散 vs 集中） | 未测 |
| 10 | Σ66 top_directional_significant_value_1 | 高管×方向×大额 | 未测 |

## 纪律

- 分母一律不加纯数 epsilon（count/share/price 字段会触发单位闸，BE103/112 两次实证）
- MATRIX 直接裸用，VECTOR 用 vec_avg
- 收割后 |S|≥1.2 必查 lc/sc（空心件拦截）

## 判读线

|S| ≥1.2 满波 / 1.0-1.2 定向补 / <1.0 换机制族。两批均与既有最优（1.06 / 0.86）对照归因。
