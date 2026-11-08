# Wave N5 中期台账（dl_riskfree 置信度激增精修，3/5 批已收）— 2026-11-07 上午

基线（N3）：wpQG55Pv = subtract(group_rank(ts_delta(P5, 5), sector), 0.5)
S 1.73 / F 0.89 / 2Y 1.50 / TO 0.3611，raFail 3

| 精修 | alpha | S | F | 2Y | TO | raFail |
|---|---|---:|---:|---:|---:|---:|
| ts_mean(ts_delta,5) 平滑 | RREz80ez | 1.38 | 0.70 | 0.95 | 0.2756 | 3 |
| **delta W10** | omEGlQab | **1.67** | **0.97** | 1.38 | 0.2683 | **2** |
| delta W22 | MPYzLQjo | 1.53 | 0.89 | **1.97** | 0.2544 | 2 |
| delta 换 20d 概率源 | leAG3lLx | 1.53 | 0.73 | 1.20 | 0.3660 | 4 |
| delta 换 60d 概率源 | RREzmR1g | 1.11 | 0.45 | 0.84 | 0.3727 | 4 |
| winsorize 后置 | 1YNKpYpk | 1.72 | 0.89 | 1.48 | 0.3586 | 3 |

## 窗口/2Y 拉扯谱（激增臂）
delta5: 1.73/0.89/1.50 · delta10: 1.67/0.97/1.38 · delta22: 1.53/0.89/1.97
⇒ S 随窗口单调降、2Y 在 W22 反弹、F 在 W10 最好——还没有单项全过；W10 离全过最近（差 F 0.03 + 2Y 0.20）。
平滑（ts_mean5）毁全部；60d 源死；winsorize 后置无效（幂等再证）。

待收：industry / delta×P20 水平合取 / ts_mean22 平滑 / subindustry（第 4-5 批在飞）。
合取（delta 动量 × 20d 水平 2Y 1.74）是同时借两族 2Y 力的最后希望。