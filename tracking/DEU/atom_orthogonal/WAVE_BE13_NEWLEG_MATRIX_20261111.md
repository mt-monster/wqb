# BE13 / BE13b 新族第一腿矩阵（2026-11-11）

> 目的：篮子被「4 纯 analyst 预估族 + 3 借券族」占满，news/earnings/institutions/sentiment/risk/option/macro/workforce 零覆盖。
> 用已验证骨架（`group_zscore(add(新腿, 第二腿), market)` + `sector` 内层 + `ts_backfill 132`）只换第一腿。

## 一、九臂结果（BE13b，sim FLQKabM4oA8Z8MbUkx8QY）

| alpha | 第一腿 × 第二腿 | S | F | sub | 2Y | 塔标记 | 判定 |
|---|---|---:|---:|---:|---:|---|---|
| **rK71dLbE** | loan_rate_volatility Δ220 × I7 | **1.40** | **1.10** | 0.72 | **2.45** | SHORT+INSIDERS | 强但**与 qM7KxkQV 0.8451 互斥** |
| **P05JM61x** | nws20_sentiment Δ66 × I7 | **1.46** | 0.79 | 0.61 | 1.36 | INSIDERS+NEWS | **与篮子 ≤0.519，可救** |
| Grmqg6Mx | lending_fee_bid_rate Δ220 × shrt3 Δ132 | 1.10 | 0.66 | 0.58 | 1.35 | SHORT+RISK | 弱 |
| kqaxJXn8 | loaned_market_value_usd Δ220 × shrt3 Δ220 | 1.15 | 0.71 | 0.41 | 2.40 | SHORT | 弱 |
| 58JZj9M5 | rsk60_crowding Δ66 × I7 | 0.93 | 0.48 | 0.30 | 0.87 | RISK+INSIDERS | 弱 |
| oma1ovYv | inst25_concentration Δ66 × shrt3 Δ220 | 0.90 | 0.50 | 0.65 | 1.28 | SHORT+INSTIT | 弱 |
| d5a2KmdX | opt1_p_deltasurface_d1_vi Δ66 × I7 | 0.56 | 0.29 | 0.48 | -0.19 | INSIDERS+OPTION | 死 |
| 9qlzEKJr | opt1_p_deltasurface_d1_vi Δ66 × shrt3 Δ220 | 0.62 | 0.30 | 0.66 | -0.00 | SHORT+OPTION | 死 |
| akarVldv | rsk60_crowding Δ66 × opt1_vi Δ66 | -0.15 | -0.03 | 0.17 | -1.17 | RISK+OPTION | 死 |

另：BE13 中 lending_fee × I7 已由 **KPgKm6Xk** 建出：S1.20 / F0.88 / sub0.47 / 2Y1.11 / 塔 RISK+INSIDERS。

## 二、六条新结论

| # | 结论 | 证据 |
|---:|---|---|
| N-1 | **OPTION 族对 DEU 无效**（3 臂全低于 0.62，2Y 非负即零） | d5a2KmdX 0.56 / 9qlzEKJr 0.62 / akarVldv -0.15 |
| N-2 | **lending_fee_bid_rate 归属 RISK 类**（非 SHORTINTEREST） | KPgKm6Xk 塔标记 ['RISK','INSIDERS'] |
| N-3 | **loan_rate_volatility 是强腿**（F1.10 过线、2Y2.45），但**只能配非 I7 的第二腿** | rK71dLbE vs qM7KxkQV = 0.8451 |
| N-4 | **I7 第二腿是把双刃剑**：提 S/sub/2Y 极有效，但凡两件都用 I7 就会撞 0.7-0.85 | rK71dLbE 0.8451、Jj8VQwoe(共 shrt3) 0.8924 |
| N-5 | **news 情绪是唯一既干净又有信号的候选面** | P05JM61x 与篮子 ≤0.519，S1.46 |
| N-6 | **新族腿 × shrt3 组合普遍弱于 × I7**（Grmqg6Mx 1.10 / kqaxJXn8 1.15 / oma1ovYv 0.90 vs I7 系 1.40-1.46） | 本波对照 |

## 三、方法论修正：第二腿配对前必须先查互相关

本波最大浪费点：rK71dLbE 花了整波推 S 之前若先算互相关，就会发现与 qM7KxkQV 0.8451。
**新纪律**：设计「新第一腿 × 已验证强第二腿」时，**先看该第二腿已被哪件占用**——
- I7 已被 qM7KxkQV 占用 ⇒ 任何"I7 系"新件都会 0.7+ 撞它。
- shrt3 Δ220 已被 qM7KxkQV/Jj8VQwoe 占用。
⇒ 想要低相关，**新件必须同时换掉两条腿**，或第二腿换成尚未被占用的（如 insd1_tradesignificance / oth47 / 新族腿）。

## 四、下波方向（BE14 已派发）

**P05JM61x（nws20_sentiment Δ66 × I7，S1.46 / F0.79 / TO0.2361 / sub0.61）**：
- 与篮子全对 ≤0.519 ⇒ 干净
- 短板：TO 0.2361 偏高（>0.125 阈值），F 0.79 不足，S 差 0.12
- **降 TO 可同时提 F**：TO 0.2361→0.125 约提 F ×1.37 ⇒ 0.79→1.08 ❌仍不够，需同时提 S
- BE14 十臂：ts_mean 平滑(22/44)、水平 zscore、长窗 rank、Δ132/Δ264、外层 group_rank、I7 换 ts_mean22 版、hump 降换手、第二腿换 insd1_tradesignificance
