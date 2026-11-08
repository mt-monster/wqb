# risk70 深挖 P58-P59：冷门字段与未测 asetrd 族（2026-11-07）

## P58 risk70 冷门字段族（MATRIX cov 1.0，aC 0-44）

| # | alpha | S | F | TO | 2Y | raF |
|---|---|---:|---:|---:|---:|---:|
| 8 | `-group_rank(ts_sum(short_term_industry_country_factor,5),sector)` | 1.07 | 0.35 | **0.792** | -0.49 | 6 |
| 4 | `group_rank(ts_mean(sector_relative_momentum,22),sector)` | **-1.07** | -0.94 | 0.090 | -1.45 | 5 |
| 3 | `-group_rank(ts_delta(hedge_fund_number_owners,66),sector)` | -0.57 | -0.26 | 0.091 | -1.03 | 4 |
| 2 | `group_rank(ts_mean(hedge_fund_number_owners,22),sector)` | -0.51 | -0.24 | 0.061 | -1.26 | 5 |
| 1 | `group_rank(ts_delta(hedge_fund_ownership_percentage,66),sector)` | -0.42 | -0.16 | 0.091 | -1.32 | 5 |
| 5 | `-group_rank(ts_mean(us_equity_short_interest_ratio,22),sector)` | 0.07 | 0.01 | 0.066 | -0.56 | 5 |
| 9 | `-group_rank(ts_mean(broad_market_exposure_factor,22),sector)` | 0 | 0 | 0 | - | 5 |

读数要点：
- **对冲基金持股族（ownership_percentage / number_owners，aC 20/22）全灭**（|S|≤0.57 且 2Y 为负）；「冷门」再次不等于有信号。
- `sector_relative_momentum` 正向 S **−1.07** ⇒ **取负镜像约 +1.07**，是反转而非动量：行业相对动量在 KOR 失效、反向有效。
- `broad_market_exposure_factor` 收益率为 0（因子为常数或全 NaN），不可用。
- `us_equity_short_interest_ratio`（aC 10）0.07 ⇒ 美股空头比率对 KOR 无传导。

## P59 risk70 未测 asetrd 族（57 字段中此前只测过 anlystsn / momentum）

| # | 字段 | 表达式方向 | S | F | TO | 2Y | raF |
|---|---|---|---:|---:|---:|---:|---:|
| 1 | dsrt | 5d 反转 | **1.40** | 0.48 | **0.867** | -0.02 | 6 |
| 4 | btop | 空高 B/P（反向） | -0.91 | -0.70 | 0.070 | -1.68 | 5 |
| 8 | strevrsl | 22d 短反转（负向乘） | -0.94 | -0.45 | 0.279 | -0.53 | 5 |
| 2 | resvol | 低残差波动 | 0.75 | 0.55 | 0.078 | 1.30 | 3 |
| 3 | earnyild | 空高 E/P | -0.63 | -0.39 | 0.070 | -1.68 | 5 |
| 9 | earnqlty | 空高盈利质量 | -0.57 | -0.27 | 0.052 | -1.33 | 5 |
| 5 | divyild | 空高股息率 | -0.51 | -0.23 | 0.050 | 0.19 | 4 |
| 6/7/10 | earnvar / cnt_kor / invsqlty | - | 0.13/-0.11/-0.18 | - | - | - | 4-5 |

读数要点：
- **价值族方向被反向验证**：btop −0.91、earnyild −0.63 ⇒ 取正号（多头高 B/P、高 E/P）约 +0.91/+0.63，但都远低于 1.58。
- `dsrt` 5d 反转 S1.40 是 risk70 的最强单腿，但 **TO 0.867** 把 fitness 压到 0.48，与 risk88 同型：
  KOR 的特定收益反转在 5 日尺度有信号（1.3-1.4），但换手率结构性过高，降换手杠杆（decay_linear / ts_mean / 长窗）全部会把 S 打到 1.0 以下。
- `strevrsl` 正向为负 ⇒ 镜像 +0.94；`resvol` 低残差波动 0.75/2Y1.30 是唯一「S 低但 2Y 健康」的腿。

## 结论

risk70 第二颗**不可得**：96 个字段里除已用的 anlystsn×momentum 外，最强单腿 dsrt 反转 1.40 但换手 0.867，价值族 ≤0.91，冷门族 ≤1.07。
KOR 交付维持 **4/10**（含待确认的 d5Wvpmbx）。