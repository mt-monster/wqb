# MODEL 类别新矿脉盘点（2026-11-07）

KOR/MODEL 共 **57 个数据集**，此前只开采过 global_seasonal_model 与 model138（反解 OS 池得来）。
按 `coverage 降序 + alphaCount 升序 + valueScore` 三重筛，得到 4 个高价值新目标：

## 1. analyst_earnings_ibes — cov **1.0**，28 MATRIX，aC 108，vs 5（最高优先）
名字误导：字段**全是价量**，不是预期。但它是**多期限收益序列**，天然可做期限结构：
```
one_day_total_return_dlr1 / five_day_ / twenty_day_ / sixty_day_ / one_twenty_day_ / two_fifty_day_total_return_dlr1
closing_price / highest_price / lowest_price / opening_price / volume_weighted_avg_price / trading_volume / market_capitalization / shares_outstanding
```
机制：**动量期限结构**（Jegadeesh–Titman 1993 + Novy-Marx 2012 "intermediate horizon"）——
长窗收益（250d）扣掉短窗（20d）得到"中间期动量"；短窗反转 × 长窗动量乘积。
这是我现有 3 颗交付件（analyst 修正 / risk 持仓 / insider 波动）**完全未覆盖的机制面**，且 cov 1.0 十年无空窗风险。

## 2. behavioral_signals — cov 0.8682，7 VECTOR，aC **0–6**（最不拥挤）
```
salience_weighted_return_score        (aC 6)  Salience Theory 显著性加权
extreme_daily_return_indicator        (aC 1)  极端日收益（彩票偏好）
price_path_curvature_measure          (aC 4)  价格路径凸性
chronological_return_sequence_correlation (aC 3) 收益时序相关
consecutive_return_streak_length      (aC 0)  连涨连跌长度（带方向）
visual_price_path_shape_score         (aC 0)  路径形状
total_equity_market_value_usd         (aC 2)  市值（控制变量）
```
机制：Bordalo–Gennaioli–Shleifer (2012) **显著性理论**（高显著性上行 → 高估 → 低未来收益）+ 彩票偏好（Bali-Cakici-Whitelaw 2011）。
aC≈0 是双刃：memory 记「aC≈0 通常意味着没信号」，但 salience 是已发表稳健异象 ⇒ 值得 1 个探针批。

## 3. ai_factor_transfer — cov **1.0**，20 MATRIX，aC 215
经典技术指标在 KOR 的原生实现：RBO / CCI / RSI / Williams %R / 布林带位置 / CMF / PVO / DPO / ADL / RTN63D / ABN_VOLM。
机制：技术指标**反转组合**（超买超卖 + 量价背离）。cov 1.0，适合做负向反转。

## 4. price_signal_dl — cov 0.99，28 MATRIX，aC 0–62
`normalized_trend_indicator_0..6` + `normalized_volume_indicator_0..6` + raw 版。DL 价格信号，已成归一化（省算子）。
机制：趋势 × 量能二维状态的横截面排序。

## 排除
- model25（554 字段 aC **11900**）、model39（aC 2599）、model110（aC 2658）、model28（aC 2117）、global_seasonal_model（aC 2177）、multifactor_return_pred（aC 1401）—— 拥挤度已到饱和区，prod 墙必深，不值得花批次。

## 队列（按 EV）
P18 MPYZPkKL 调优（已备，S 1.52/2Y 1.51 差一步）> P17 analyst16 > P19 analyst_earnings_ibes（cov 1.0 新机制面）> P20 behavioral_signals > P21 ai_factor_transfer
