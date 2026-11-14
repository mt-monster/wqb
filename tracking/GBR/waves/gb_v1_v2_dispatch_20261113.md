# GBR 波次 GB-V1/V2/PROF 档案（2026-11-13 21:40-22:0x GMT+8）

> 塔位前提（11-13 实拉）：已点亮禁投 model6/news3/analyst3/pv4/fund3/shrt4；可投 other2/institutions0/insiders0/earnings0/sentiment0/risk0/option0/socialmedia0/macro0/imbalance0。
> 选集：coverage audit(11-09) 的 4 个「有数据零回测」处女集（探针背书 longCount 343/650/210/424）+ risk 塔五集（sentiment/risk 优先序）。

## GB-V1A nan=ON/SUBIND/decay4  id=3LEfp0cas56WbaqV1AosXaI（8/8 COMPLETE）
A1 ess净情绪sum kqa5oz2O S0.19 | A2 ess事件链tail RReLbGW0 S-0.10 | A3 ess改进分zscore xAva3JgN S0.19 | A4 ess事件计数Δ gJazbnpg S-0.38 | A5 搜索1y水平 kqa5oz5d S-0.32 TO.71 | A6 搜索14dΔ LLKxN0x1 S0.37 TO.78 | A7 社媒watch时序位 gJazbnzg S-0.21 | A8 ess负面分反向 GrmvbZVJ S0.69 sub0.69 TO.051（本波最强）

## GB-V1B nan=OFF  id=14YzBb5dM4hZ9EQuupTuuvN（8/8 COMPLETE）
B1 ess sum nanOFF 6XMbK1nL S0.55（vs A1 0.19：nan OFF +0.36 复证 EUR 教训）| B2 搜索1y反转 0mPWrdb1 S0.32 TO.71 2Y1.4 | B3 社媒反转 MP6A3XPM S0.21 | B4 ess keydriver gz XgaEJLg5 S0.68 sub0.85 | B5 ess vec_max j2aQ8X2W S0.49 | B6 other78 NLP置信 78YV6Q8x S0.44 TO1.35 | B7 搜索Δ反转 omaeWvml S-0.37 | B8 ess正面分 xAvabQAb S0.02

## GB-V2 ess 负面族定向 nan=OFF  id=1pwVAR8Hx4UmbN0e61celd4（8/8 COMPLETE）
1YW5jo7z kf_neg_score_2 S0.24 | 0mPWjA76 section_neg_score S0.30 | leaZM7Vn sent_sec_neg_d1 S0.36 | qM7ZEnlZ neg_event_count S0.29 | LLKx5n1n 窗口252 S0.22 | 88NqvOQv ts_zscore252 S-0.64（符号反转：变化量纲与水平量纲反号）| Jj8LPnO2 trade_when量能门控 S0.26 | bla38NdZ 除词数强度 S0.18

## 判定（覆盖证书）
- event_sentiment_signals：判死。16 结构 x 7 字段 x 2 极性 x 2 nan 档，max S 0.69 < 零假设地板 0.7-1.0；tail 事件链在 GBR 反效；nan OFF +0.36 有效。
- socialmedia39：判死。唯一字段正反对称（+0.21/-0.21）。
- other78：判死。语义闸（会议/联系元数据）+ NLP 置信臂 TO 1.35。
- stock_search_trends：暂停不判死。TO 墙 0.71-0.78 + 弱 S；10 字段未测，低优先。

## GB-PROF risk 六法画像批 NONE/decay0/nanOFF/P0Y0M0D  id=gROxG8ei4xmbIUEaMbwS6E（在跑）
P1 vec_sum(rsk60_offer) 法1 | P2 offer!=0 法2 | P3 offer ts_std5 法3 | P4 offer ts_std66 法3 | P5 vec_avg(rsk60_crowding) 法1 | P6 crowding ts_std5 法3 | P7 rsk68_residual_return 法1 | P8 rsk68_beta 法1

## GB-V3 risk 机制探针 SUBIND/decay4/nanON  id=4hCUir8zq4srb9t1h7DgYq7v（在跑）
R1 借券费水平 | R2 借券费Δ | R3 做空拥挤 | R4 BAB beta | R5 低波 | R6 残差反转ts_rank形态 | R7 risk71残差 | R8 规模（alternative_market_cap_usd）

## GB-PROF 六法画像收割（id=gROxG8ei4xmbIUEaMbwS6E，8/8 COMPLETE，2026-11-13）
| 探针 | 字段/方法 | longCount | shortCount | 读数 | → 交 FE |
|---|---|---:|---:|---|---|
| xAva1Grw | rsk60_offer 法1 | 536 | 0 | 覆盖 77%（536/700），全正 | 费率恒正单边：裸读=市场暴露假象，必须截面标准化 |
| rK7mdGRJ | offer!=0 法2 | 536 | 0 | 与法1相同 | 无零膨胀，数据稠密 |
| 0mPWjgYr | offer ts_std5 法3 | 210 | 0 | 5天内仅30%变动 | 更新慢，窗口下限 66 |
| j2aQeGYk | offer ts_std66 法3 | 469 | 0 | 66天内67%变动 | 确认窗口下限 66 |
| omaeoGa5 | rsk60_crowding 法1 | 76 | 70 | 覆盖仅 21%，TO 1.68 | 无法独立撑全池信号，只能门控/轴 |
| 9qlQEMlK | crowding ts_std5 | 271 | 0 | 更新面广于覆盖面 | 残差：字段部分更新、部分缺失 |
| 58JVj5Jz | rsk68_residual_return 法1 | 408 | 425 | 全覆盖双横（833 席位），TO 1.48 | risk 塔唯一合格主信号材料；裸 TO 高，必须聚合压缩 |
| pwagvGa3 | rsk68_beta 法1 | 824 | 9 | 全覆盖但单边正、极粘滞 TO 0.01 | 需中心化（减1/group）才能截面用；BAB 死区确认 |

## GB-V3 收割详情（id=4hCUir8zq4srb9t1h7DgYq7v，8/8 COMPLETE）
| 臂 | alpha | S | F | TO | 2Y | sub | fails |
|---|---|---|---:|---:|---:|---:|---:|
| R7 risk71残差 top2500 ts_rank66 | rK7md55J | 1.34 | 0.35 | 0.874 | 0.37 | 0.86 | 4 |
| R6 残差反转 ts_sum22+ts_rank252 | omaeo665 | 1.22 | 0.67 | 0.189 | 0.65 | 0.61 | 3 |
| R3 做空拥挤 | 0mPWjRwK | -0.34 | | 0.145 | -0.65 | -0.87 | 4 |
| R8 规模 | e7aJ6996 | 0.34 | | 0.070 | 0.41 | 0.02 | 4 |
| R4 BAB | npabAK7d | -0.33 | | 0.061 | 0.54 | 0.11 | 3 |
| R1 借券费水平 | E5QAVvGP | 0.28 | | 0.106 | -0.08 | 0.30 | 3 |
| R2 借券费Δ | 3q0Wj9lZ | 0.14 | | 0.139 | 0.01 | 0.28 | 3 |
| R5 低波 | A1xdQ0lE | -0.13 | | 0.169 | 0.06 | 0.33 | 3 |

## GB-V4 算子穷尽升级波（2026-11-13 用户指令：截面形态试遍截面算子、时序同）
底座：R6 = multiply(-1, ts_rank(ts_sum(rsk68_residual_return, 22), 252)) S1.22/TO0.19（历史对照：裸 zscore 残差反转形态曾撞 prod 墙 0.71-0.76×3）
- GB-V4A 时序形态族 id=Gns6ngNH4PKcABVnb217ER：ts_mean/ts_decay_linear 内核、ts_zscore/ts_quantile 外层、窗口 5/66、ts_std_dev 二阶矩、ts_arg_max 时效量纲，8 臂，SUBIND/decay4/nanON
- GB-V4B 截面形态族 id=190wqOaOO4wybdTGGFdis6v：rank/zscore/group_rank(subind/ind)/group_zscore(sector)/group_neutralize(sector)/signed_power(2)/winsorize(std2)，8 臂，同设置
读数判据：S≥1.58 且 2Y 分档过线 → 全闸；1.0-1.58 → 归因续升；<1.0 → 该算子形态记死。

## GB-V4B 截面形态族收割（id=190wqOaOO4wybdTGGFdis6v，8/8 COMPLETE，2026-11-13 22:0x）
| 臂 | alpha | S | F | TO | 2Y | sub | fails |
|---|---|---:|---:|---:|---:|---:|---:|
| group_zscore(ts_sum22, sector) | GrmvW0PO | **1.23** | **0.84** | 0.182 | **0.79** | 0.68 | 3 |
| group_neutralize(ts_rank 形态, sector) | zqdz3wZG | 1.22 | 0.67 | 0.189 | 0.65 | 0.61 | 3 |
| winsorize(ts_rank 形态, std2) | wpoVQwmY | 1.21 | 0.66 | 0.189 | 0.64 | 0.61 | 3 |
| signed_power(ts_rank 形态, 2) | ZYaLQw53 | 1.20 | 0.65 | 0.191 | 0.71 | 0.54 | 4 |
| group_rank(ts_sum22, industry) | Jj8Le0qn | 1.15 | 0.64 | 0.187 | 0.69 | 0.59 | 3 |
| rank(ts_sum22) | E5QA60OR | 1.14 | 0.67 | 0.180 | 0.64 | 0.64 | 3 |
| zscore(ts_sum22) | vRAV1nwb | 1.10 | 0.78 | 0.181 | 0.74 | 0.68 | 3 |
| group_rank(ts_sum22, subindustry) | rK7mR6Y3 | 1.10 | 0.58 | 0.185 | 0.72 | 0.49 | 4 |

读数：8 算子全落 1.10-1.23 稳健带（机制真实非形态运气）；group_zscore(sector) 三项最优；两个等价性确认（group_neutralize 后置 ≈ R6 原式 1.22 全等；winsorize 对 ts_rank 近无操作）。**无一破 1.58，全进归因续升带。**

## GB-V5 整合波派发（id=16G10k8YG4WH9CNX6kyTFQ6，在跑）
最优形态 group_zscore(sector) × 窗口阶梯 5/10/44/66/126 × risk72/risk71 姊妹集迁移 × ts_delta 动量形态。SUBIND/decay4/nanON。
## GB-V4A 时序形态族收割（id=Gns6ngNH4PKcABVnb217ER，8/8 COMPLETE）
| 臂 | alpha | S | F | TO | 2Y | sub | fails |
|---|---|---:|---:|---:|---:|---:|---:|
| ts_quantile(ts_sum22,252,gaussian) | xAvarmaW | **1.32** | 0.76 | 0.198 | 0.75 | 0.62 | 4 |
| ts_rank(ts_decay_linear22,252) | aka3KW32 | 1.21 | 0.64 | 0.221 | 0.13 | **0.98** | 3 |
| ts_rank(ts_mean22,252) | 6XMbdYOJ | 1.20 | 0.66 | 0.191 | 0.55 | 0.76 | 3 |
| ts_zscore(ts_sum22,252) | RReLEkL1 | 1.17 | 0.67 | 0.205 | **0.82** | 0.58 | 3 |
| ts_rank(ts_sum66,504) | VkNoxYoA | 1.03 | 0.67 | 0.118 | **1.45** | 0.64 | 3 |
| ts_rank(ts_sum5,126) | Jj8Le5ll | 0.76 | 0.24 | 0.411 | 0.04 | 0.68 | 3 |
| ts_rank(ts_arg_max22,252) | E5QA6r3m | 0.25 | | 0.283 | 1.12 | -0.21 | 4 |
| ts_rank(ts_std_dev22,252) | j2aQYdLZ | 0.01 | | 0.146 | 0.58 | 0.11 | 3 |

读数：ts_quantile(gaussian) 外层 S 1.32 新王；**窗口阶梯揭示 S↔2Y 权衡**（22→66：S 1.22→1.03 但 2Y 0.65→1.45，逼近 1.58 第一档）；ts_decay_linear 内核 sub 0.98 极佳但 2Y 塌（0.13）；ts_arg_max/ts_std_dev 死区（残差波动率无反转信号，只有水平有）。

## GB-V6 设置档轴波（decay 15）派发
最优 6 形态 × 窗口 22/66/126 @ decay 15（A/B 对照 decay 4）：ts_quantile/gz(sector)/ts_zscore/ts_rank × 2 窗，8 臂。id=hEgXlbk459caxl1ahq68HIz
## GB-V5 整合波收割（id=16G10k8YG4WH9CNX6kyTFQ6，8/8 COMPLETE）
| 臂 | alpha | S | F | TO | 2Y | sub | fails |
|---|---|---:|---:|---:|---:|---:|---:|
| **gz·ts_sum(risk71 top2500, 22) sector** | omaeEoZE | **1.36** | **0.95** | 0.180 | 1.09 | 0.81 | 3 |
| gz·ts_sum(risk72 top2500, 22) sector | d5awWKvx | 1.29 | 0.87 | 0.182 | 0.99 | 0.79 | 3 |
| gz·ts_sum(rsk68, 10) sector | XgaE9RMm | 1.23 | 0.70 | 0.276 | 0.43 | 0.84 | 3 |
| gz·ts_sum(rsk68, 5) sector | 0mPWYj62 | 1.10 | 0.50 | 0.412 | 0.51 | 0.84 | 3 |
| gz·ts_sum(rsk68, 44) sector | GrmvWg9J | 1.01 | 0.76 | 0.129 | 0.80 | 0.64 | 3 |
| gz·ts_delta(rsk68, 22) sector | 9qlQxEk2 | 0.97 | 0.27 | 0.858 | 0.05 | 0.89 | 4 |
| gz·ts_sum(rsk68, 66) sector | aka3KVG2 | 0.88 | 0.65 | 0.107 | 1.11 | 0.56 | 3 |
| gz·ts_sum(rsk68, 126) sector | omaeEoZn | 0.19 | 0.07 | 0.080 | 0.41 | -0.06 | 4 |

读数：**risk71「可复现残差」平移成功且全场新王**（S 1.36/F 0.95/2Y 1.09/sub 0.81/TO 0.18，还修复 R7 换手墙 0.87→0.18）；risk72 同口径 1.29 平移确认；rsk68 窗口阶梯 S 单调降（gz 形态）；ts_delta 动量形态死。新王字段 residualized_return_top2500 的窗口/形态/分组响应面未扫 → GB-V7。

## GB-V7 risk71 响应面波派发：窗口 10/44/66 + ts_quantile/ts_rank 形态 + sector group_rank/industry/subindustry 分组轴，8 臂 @ SUBIND/decay4。id=9wRKx2Jw4lz90FKgCU63Hy

## GB-V6 decay15 收割（id=hEgXlbk459caxl1ahq68HIz，8/8 COMPLETE）
| 臂（@decay15） | alpha | S | S@decay4 | 2Y | 2Y@decay4 | TO | F | fails |
|---|---|---:|---:|---:|---:|---:|---:|---:|
| ts_quantile(ts_sum22,252) | xAvarLll | 1.30 | 1.32 | **1.12** | 0.75 | 0.116 | 0.91 | 4 |
| ts_zscore(ts_sum22,252) | kqa5Nwvk | 1.10 | 1.17 | 1.12 | 0.82 | 0.131 | 0.74 | 4 |
| gz·ts_sum22 sector | 58JVEmrn | 1.06 | 1.23 | 0.79 | 0.79 | 0.112 | 0.79 | 4 |
| ts_quantile(ts_sum66,504) | A1xdVpeE | 0.98 | — | **1.40** | — | 0.073 | 0.64 | 3 |
| ts_rank(ts_sum66,504) | j2aQYpo9 | 0.88 | 1.03 | 1.37 | 1.45 | 0.068 | 0.53 | 3 |
| ts_zscore(ts_sum66,504) | xAvarLVJ | 0.74 | — | 1.17 | — | 0.094 | 0.44 | 4 |
| gz·ts_sum66 sector | vRAV1EZr | 0.67 | 0.88 | 1.05 | 1.11 | 0.065 | 0.42 | 3 |
| ts_rank(ts_sum126,504) | zqdz3xgR | 0.22 | — | 0.57 | — | 0.055 | 0.07 | 4 |

**decay15 结论：不破 S 闸，S↔2Y 再置换**（ts_quantile 形态 2Y +0.37 但 S 持平；gz 形态 S 反降）。残差面 S 前沿汇总：max S 1.36（risk71@22 gz sector decay4）、max 2Y 1.45（rsk68@66 ts_rank decay4）。S↔2Y 前沿点集（V6 时）：(1.36,1.09) (1.30,1.12) (1.03,1.45) (0.98,1.40)。

## GB-V7 risk71 响应面收割（id=9wRKx2Jw4lz90FKgCU63Hy，8/8 COMPLETE）★★ S 闸破
| 臂 | alpha | S | F | TO | 2Y | sub | fails |
|---|---|---:|---:|---:|---:|---:|---:|
| **gz·ts_sum(w10) sector** | XgaEamR5 | **1.65** | **1.05** | 0.274 | 1.08 | **1.06** | **1** |
| ts_quantile(ts_sum22,252) | A1xdxjQe | 1.57 | 0.94 | 0.198 | 0.92 | 0.79 | 3 |
| ts_rank(ts_sum22,504) | xAvavO1p | 1.53 | 0.91 | 0.186 | 1.00 | 0.82 | 3 |
| group_rank(ts_sum22) sector | KPgRglJj | 1.53 | 0.97 | 0.177 | 1.03 | 0.85 | 3 |
| gz·ts_sum22 industry | kqa5aENK | 1.44 | 0.95 | 0.181 | 0.99 | 0.80 | 3 |
| gz·ts_sum22 subindustry | 78YVY7LL | 1.39 | 0.85 | 0.178 | 0.74 | 0.76 | 3 |
| gz·ts_sum44 sector | qM7Z79EP | 1.09 | 0.83 | 0.128 | 0.93 | 0.75 | 3 |
| gz·ts_sum66 sector | E5QAQOVG | 1.00 | 0.75 | 0.106 | 1.14 | 0.72 | 3 |

**读数：窗口 10 破 S 闸**（risk71 的窗口曲线与 rsk68 相反：越短越强，w10→1.65 / w22→1.36 / w44→1.09 / w66→1.00）；sector 轴 > industry > subindustry。XgaEamR5 = S1.65✓ F1.05✓ TO0.27✓ sub1.06✓ **逐年 10/10 全正无空窗**（最弱 2017 S0.10/+0.42%），**只剩 2Y 1.08 一闸**（差 0.50；TO 0.27 高换手带可能适用 ~1.90 档位，待平台确认）。

## GB-V8 双波派发（2Y 冲刺）
- **V8a decay15** id=2MbT0R4NS5biaErdwR5CWru：w5/10/15 + add 双窗(10+66) + trade_when 量能门控 + ts_decay_linear 表达式级平滑 + ts_quantile/group_rank @ w10，8 臂
- **V8b STATISTICAL** id=3UVU06gca4XccJkM7poAEmy：w5/10/15/22 + ts_quantile/group_rank/add双窗/ts_rank，8 臂（wave57 的 8/8 孪生提升证据轨）
判定：任一臂 2Y≥1.58（或平台确认高换手档位≤其 2Y）且 S/F/TO 全过 → 逐年+self→prod 终验链启动。

## GB-V8b STATISTICAL 收割（id=3UVU06gca4XccJkM7poAEmy，8/8 COMPLETE）★★★ 双星全闸破
| 臂 | alpha | S | F | TO | 2Y | sub | fails | ops |
|---|---|---:|---:|---:|---:|---:|---:|---:|
| **gz·ts_sum(w22) @STAT** | **j2aQa1qo** | **1.81** | **1.22** | 0.198 | **1.84** | 1.17 | **0** | **3** |
| **gz·ts_sum(w15) @STAT** | **leaZaro8** | 1.77 | 1.10 | 0.235 | 1.70 | **1.29** | **0** | 3 |
| group_rank(w10) @STAT | QP0d0Q1X | 1.73 | 0.80 | 0.275 | 1.60 | 1.15 | 1 | 3 |
| gz·ts_sum(w10) @STAT | 9qlQlJn2 | 1.69 | 0.95 | 0.286 | 1.54 | 1.18 | 2 | 3 |
| ts_rank(w10) @STAT | XgaEaKjb | 1.65 | 0.71 | 0.280 | 1.24 | 1.20 | 2 | 4 |
| ts_quantile(w10) @STAT | omaeaVxb | 1.61 | 0.71 | 0.289 | 1.13 | 1.22 | 2 | 4 |
| gz·ts_sum(w5) @STAT | 6XMbMz5Y | 1.50 | 0.67 | 0.418 | 1.03 | 1.04 | 3 | 3 |
| add 双窗(10+66) @STAT | WjlmlgEN | **-1.79** | -1.20 | 0.219 | -1.51 | -1.24 | 4 | 5 |

**★ 关键结论：STATISTICAL 中性化打破 S↔2Y 剪刀差，同抬双指标**（对照 SUBINDUSTRY 同式：S 1.36→1.81 (+0.45)、2Y 1.09→1.84 (+0.75)、F 0.95→1.22）——wave57 的 8/8 孪生提升证据在残差反转族完整复现。add 双窗臂在 STAT 档符号翻转（-1.79）记录为结构异常。

**★ 终验链进度（j2aQa1qo，3 ops 纯 ATOM：risk71 单字段 residualized_return_top2500）**：
- IS 全闸：S 1.81✓ F 1.22✓ TO 0.198✓ 2Y 1.84✓ sub 1.17✓ fails=0✓（平台权威）
- 逐年：10/10 全正无空窗（2014-2023，最弱 2015 S0.16/+61k）✓
- self：0.465 < 0.7 ✓（本地）
- 互相关：与篮子 4 颗全对 <0.7 ✓（最大对 = 6XdkW08J×omExeqLb 0.6123，新件与全篮干净）
- **prod：待测（平台单并发槽被占，240s 后重试）**——历史残差族墙 0.71-0.76 是裸 zscore 形态，本形态已换轨
- leaZaro8（w15 变体）同年验通过（10/10 正、self 0.443），与 j2aQa1qo 同族互斥，留作变体

## GB-V8a decay15 收割（id=2MbT0R4NS5biaErdwR5CWru，8/8 COMPLETE，@SUBIND/decay15）
| 臂 | alpha | S | F | TO | 2Y | sub | fails |
|---|---|---:|---:|---:|---:|---:|---:|
| group_rank(w10) sector | aka3a12v | **1.87** | 1.33 | 0.168 | 1.43 | 1.09 | 1(2Y) |
| gz·w5 | 78YVYzgO | 1.81 | 1.31 | 0.225 | 1.38 | 1.14 | 1 |
| ts_quantile(w10) | wpoVoawp | 1.77 | 1.19 | 0.172 | 1.09 | 1.09 | 1 |
| gz·w10 | leaZaWxn | 1.61 | 1.23 | 0.169 | 1.34 | 0.96 | 1 |
| gz·w15 | E5QAQGor | 1.31 | 0.99 | 0.138 | 1.17 | 0.74 | 3 |
| trade_when 量能门控 | KPgRgGxg | 1.31 | 0.93 | 0.153 | 1.21 | 0.58 | 4 |
| ts_decay_linear 外层 | 0mPWPpn6 | 1.30 | 0.93 | 0.142 | 1.25 | 0.71 | 3 |
| add 双窗(10+66) | rK7m72Qj | **-1.22** | -1.0 | 0.114 | -1.27 | -0.79 | 4 |

读数：decay15 抬 S（group_rank w10 → 1.87 全场最高）但 SUBIND 下 2Y 卡 1.43；**add 双窗形态在 V8b/V8a 双档系统性反号**（-1.79/-1.22）确认弃用；trade_when 量能门控弱于基线。

## ★ 决定性负结果：j2aQa1qo prod 终验 FAIL（2026-11-13 22:48）
**prod = 0.8496 ≥ 0.7 FAIL**（refresh=True 触发计算、MCP 120s 超时后 refresh=False 取回）。
⇒ risk71 残差反转面 IS 完美（S1.81/F1.22/2Y1.84/fails0/逐年10/10/self0.465/互相关干净）但 **prod 深度饱和**：历史裸 zscore 形态墙 0.71-0.76，本形态反升 0.85——机制层拥挤（残差反转是平台最重挖掘面之一）。leaZaro8 同族同字段，prod 预计同档，不再消耗相关性槽。
**处置**：V9（STATISTICAL×decay15 组合矩阵，已派发 IovC7d2h54yaYOt4aXxknI）读数后挑 fails=0 最优臂做 1 次 prod 实测；若仍 ≥0.7 → 按破墙处方做一次「改持仓类」结构变体（trade_when 分层/bucket 自造轴）；再 ≥0.7 → 残差面判「prod 饱和」收档转 insider_agg_matrix。

## GB-V9 收割（id=IovC7d2h54yaYOt4aXxknI，8/8 COMPLETE）★★★ 全 8 臂 fails=0，两杠杆复合
| 臂 | alpha | S | F | TO | 2Y | sub | fails | 逐年判定 | self |
|---|---|---:|---:|---:|---:|---:|---:|---|---|
| group_rank w10 | npabeXjd | **2.19** | 1.42 | 0.180 | **2.41** | 1.45 | 0 | ✗ 2015 负年(-32k) 淘汰 | 0.531✓ |
| group_rank w5 | mLak0lEp | 2.17 | 1.23 | 0.241 | 1.98 | 1.52 | 0 | ✓ 10/10 正 | 0.525✓ 备胎 |
| group_rank w22 | KPgR52WE | 2.16 | **1.65** | 0.125 | 2.25 | 1.30 | 0 | ✓ 10/10 正 | ✗ **0.70015 超线 0.0002** |
| **group_rank w15** | **RReLlvG0** | **2.14** | 1.49 | 0.150 | **2.32** | 1.38 | 0 | ✓ 10/10 正（最弱 2015 +46k） | **0.608✓ 入篮候选** |
| gz w5 | gJazg02M | 1.95 | 1.26 | 0.239 | 1.82 | 1.32 | 0 | — | — |
| gz w10 | A1xdr2AW | 1.87 | 1.29 | 0.188 | 1.96 | 1.25 | 0 | — | — |
| gz w22 | e7aJVWj6 | 1.86 | 1.45 | 0.136 | 1.93 | 1.10 | 0 | — | — |
| gz w15 | wpoV2vrv | 1.80 | 1.29 | 0.161 | 1.90 | 1.16 | 0 | — | — |

**★ 两杠杆复合**（vs V8a 同式 SUBIND/dec15：S+0.32/2Y+0.98；vs V8b STAT/dec4：S+0.33/2Y+0.48）——STATISTICAL×decay15 打破 S↔2Y 剪刀差，非置换而是同抬。
**RReLlvG0 终验链**：IS 全闸✓ / 逐年 10/10 正✓ / self 0.608✓ / 与篮子 4 颗互相关全对✓ / **prod 待测（账号单并发槽整晚被并行会话占用，多次 correlation_busy）**。

## ★ 事故档案：insider 画像批 D0 误参（2026-11-13 22:41）
首派 id=2Bjddlf5R4L9cmDmHdTgddo **全 8 子 FAIL**：把六法 skill 的「decay 0」误写成「delay 0」——D0 分区字段不存在自然全灭，且违反「D0 不投入」纪律（误参数化非有意开采，1 个 multisim 配额损失）。同时按 §2.7 量纲规则修正「带单位字段 vs 裸常数」的 != 0 比较为 divide(F,F) 非零探针（x/x 在非零处=1、零/缺失处=NaN，天然无量纲）。修参重发 id=3oi1pJbXW4XDbHiovjfsU74（delay1/decay0/NONE/nanOFF/P0Y0M0D）。

## ★★ 残差面终审：RReLlvG0 prod=0.8746 FAIL——机制层饱和盖棺（2026-11-13 23:07）
CLI prod_wait 实测（117s 平台计算）：RReLlvG0（gr w15 @STAT/dec15，S2.14/F1.49/2Y2.32/fails0）**prod 0.8746**。
合并 j2aQa1qo 0.8496：窗口（15/22）×形态（gz/gr）×decay（4/15）全维度组合均 0.85+，生产池残差反转与本族产出相关深度饱和。
**判定：risk 塔残差反转面 prod 死墙收档**（IS 完美×prod 死亡的组合第三例）；risk 塔其余面（借券费/BAB/低波/规模）V3 已证 IS 死区 ⇒ **risk 塔整体暂停**。RISK 塔 0 保持。
mLak0lEp（w5 备胎）不再消耗 prod 槽（同族同判）。

## GB-W1/W2 双塔机制波派发（2026-11-13 23:08，用户流程：画像报告已发+设计已呈，ask_user 60s 超时自动选「批准」未确认）
- **GB-W1 insider**（id=VjjJ7adZ4Q3ccCBlxPxrua，@SUBIND/decay4）：董事净买入（Loughrey-Yi）——di 聚合 66/126 × group_rank/gz/ts_rank/backfill × buy-sell 排名差 × 方向探针，8 臂
- **GB-W2 institutions**（id=4dTXqucpk4jRauH5Zjt8xmA，@STATISTICAL/decay15）：机构做空活跃度负压——activity ts_mean 22/66/126 + position_change 聚合 22/66 + concentration zscore，8 臂（V9 破闸组合验证于新面）

## GB-W2 institutions 收割（id=4dTXqucpk4jRauH5Zjt8xmA，8/8 COMPLETE）→ ★ 判死（D15 快杀）
| 臂 | alpha | S | 2Y | sub | fails |
|---|---|---:|---:|---:|---:|
| activity ts_mean66 rank（反向） | vRAVP0qv | -0.35 | 0.46 | -0.51 | 4 |
| activity ts_mean66 ts_zscore（反向） | VkNoenjV | -0.14 | 0.36 | -0.35 | 4 |
| activity ts_mean22 gz industry（反向） | E5QAx37L | -0.11 | 0.26 | -0.18 | 4 |
| activity ts_mean22 group_rank sector（反向） | gJazLv60 | 0.13 | -0.39 | -0.13 | 4 |
| position_change ts_sum66（反向） | kqa59RrK | 0.13 | 0.35 | -0.12 | 4 |
| position_change ts_sum22 industry（反向） | aka3GJZx | 0.08 | 0.06 | 0.32 | 3 |
| concentration ts_zscore66 | A1xdE6Ze | -0.03 | 0.65 | 0.18 | 3 |
| activity ts_mean126 ts_rank（反向） | E5QAx3WL | 0.00 | -0.40 | -0.14 | 4 |

**判定：institutions25 判死（D15：8 探针无 |S|≥0.5 快杀；max 0.35）**——activity 负压/仓位流/拥挤度三假设全死。STAT/dec15 组合在新面失效（残差面的破闸组合不迁移到无信号面——组合放大信号但不创造信号）。institutions 塔收档（该塔在 GBR 可开采池中仅此一集）。

## GB-W1 insider 收割（id=VjjJ7adZ4Q3ccCBlxPxrua，8/8 COMPLETE）→ ★ 判死（D15 快杀）
| 臂 | S | 2Y | fails |
|---|---:|---:|---:|
| gz·ts_sum(di,66) subindustry | 0.28 | 0.43 | 3 |
| buy-sell 排名差 | 0.28 | -0.04 | 3 |
| group_rank(di,126) sector | 0.19 | 0.33 | 3 |
| rank(di,126) | 0.19 | 0.35 | 3 |
| group_rank(di,22) 反向 | 0.15 | -0.46 | 4 |
| 其余 3 臂 | 0.00-0.14 | | 3 |
**判定：insider_agg_matrix 判死（max |S| 0.28）**——Loughrey-Yi 董事净买入机制在 GBR 不成立（66/126 聚合已按画像处方执行）。insiders 塔收档（该塔仅此一集）。

## GB-W3 CDS×STAT/dec15 派发（id=2nnMyg9HB5fh9m1DwiOkuex，@STATISTICAL/decay15/maxTrade ON）
**战略转向**：W1/W2 双判死后，未点亮塔的活面只剩 other169 CDS（2026-10-13 唯一活机制，S 1.52/2Y 1.57 双差 0.01 卡闸）× V9 发现的 STATISTICAL×decay15 复合杠杆（残差面实证 +0.3S/+0.5 2Y）。
8 臂：基线原式/换轴 gz(sector/subind)/窗口 22/66/126/价差变化反向/quote-spread 姊妹字段。机制：宽 CDS 价差→高后续回报（信用风险溢价，GBR value-tilt），全平台仅 6 颗使用（白空间）。

## GB-W3 CDS×STAT/dec15 收割（id=2nnMyg9HB5fh9m1DwiOkuex，8/8 COMPLETE）→ ★ 复合杠杆反噬，CDS 面闸结构死确认
| 臂 | alpha | S | 2Y | 读数 |
|---|---|---:|---:|---|
| 基线原式 @STAT/dec15 | 2r5kex3P | 1.10 | 1.04 | 从基线 1.52 下滑——复合杠杆削弱 CDS |
| gz(sector) | xAva5pKN | **-0.59** | -0.58 | 负号！ |
| gz(subindustry)/gz(w22)/gz(w126)/gz(quote) | 4 臂 | -0.51~-0.16 | | 全负 |
| delta 反向 | d5awvr2Y | 0.57 | 0 | 弱 |

**★ 机制级判词（镜像互补发现）**：CDS 价差的 alpha = 信用风险溢价本身。STATISTICAL（风险模型中性化）剥掉的正是信号承载的溢价 ⇒ 剩余为噪声（S 反转 -0.59）。与残差面配对成规则：**纯残差信号（特质收益反转）→ STATISTICAL 放大（+0.3S/+0.5 2Y）；风险溢价信号（CDS/价值/利差类）→ STATISTICAL 摧毁。前者的破闸杠杆是后者的毒药。**
**CDS 面终局**：10-13 的 65 条扫描（窗口/算子/聚合/外层/轴/11 中性化/decay）+ 今晚 8 条复合档 = 73 条全证；基线 S 1.52/F 1.07 真实但低换手档（TO 0.026）2Y 闸 1.58 悬崖缺 0.002 结构性不可达。**闸结构死，收档。**

## 战略分叉裁定（2026-11-13 23:24，用户实答）：继续磨剩余薄面
用户在 ask_user 三选一中选「继续磨剩余薄面」（真实应答非超时）。执行：GB-X1/X2 双波。

## GB-X1 order_book_imbalance 新字段波派发（id=dlLj6v85dG8Ult0d9yPbC，@SUBIND/dec4，8 臂）
已测 14/240 最高 0.56（nonaddressable_trade_volume mean22）⇒ 本波打其同族兄妹与 bilateral 家族（cov 0.4294 同档）：
nonaddressable_trade_count / nonaddressable_trade_notional_value / bilateral_trade_{volume,notional,count} / auction_order_imbalance_absolute / closing_auction_dislocation_5min + 方向探针。形态：rank(mean22) 与 group_rank(sector) A/B。

## GB-X2 薄面混合探针派发（id=3HTpUf5bH4JUctnDiVVJTnn，@SUBIND/dec4，8 臂）
macro27 招聘信号 4 臂（num_jobs_active 水平 / created Δ / removed Δ反向 / mean_days 持续期——Belo-Lin-Bazdresch 劳动雇佣文献）+ imbalance5 SHIELD-OIL 2 臂（zscore252 水平 / Δ66）+ ern6 股息面 2 臂（backfill 水平 / Δ——与在篮 starval 股息率的互相关风险在读数后预检）。

## GB-X1 收割（id=dlLj6v85dG8Ult0d9yPbC，8/8 COMPLETE，@SUBIND/dec4/nanON）
| 臂 | alpha | S | 2Y | lc/sc | 读数 |
|---|---|---:|---:|---|---|
| closing_auction_dislocation_5min rank(mean22) | kqa5YgMO | **-0.73** | -1.29 | 43/43 | 全场最强且为负号 ⇒ 翻号 +0.73；但**只有 86 名有数据**、sub -0.77，窄面 |
| auction_order_imbalance_absolute gz2(sector) | VkNoR0L8 | 0.31 | 0.22 | 126/412 | 弱 |
| bilateral_trade_notional gz2(sector) | E5QA2RMJ | 0.19 | 0.53 | 274/433 | 弱 |
| nonaddressable_trade_notional/count rank | XgaEOJO8/3q0W2V2Z | 0.19/0.16 | 0.84/0.03 | 121/134 | 弱 |
| 其余 4 臂（bilateral vol/count、方向探针） | — | -0.16~0.19 | | | 死区 |
**判词**：order_book_imbalance 240 字段累计已测 22/240，本波 8 臂证实「nonaddressable/bilateral 家族弱、唯一活口是 closing auction dislocation（窄面 + 翻号）」。按穷尽度硬约束**不判死**，标记为「窄面活口」，若要开采需专门解决 86 名覆盖问题（与 TOP700 主宇宙不兼容）。

## GB-X2 收割（id=3HTpUf5bH4JUctnDiVVJTnn，8/8 COMPLETE，@SUBIND/dec4/nanON）
| 族 | alpha | S | 2Y | 读数 |
|---|---|---:|---:|---|
| macro 招聘 num_jobs_active ts_mean66 | wpoVvZbp | -0.04 | 0.98 | TO 0.019 死 |
| macro 招聘 Δcreated / Δremoved / mean_days | d5awPb1E / O0Wv2N8R / leaZNvMx | 0.19 / -0.08 / 0.14 | 1.67 / -1.2 / 0.08 | 全弱 |
| imbalance5 db5_score zscore252 / Δ66 | d5awPbKK / bla3Kb6N | 0.23 / 0.07 | 0.14 / 0.12 | sub 1.22/0.84 但 S 死 |
| ern6_x_dividend backfill 水平 / Δ250 | QP0dobvg / gJaz0bav | 0.26 / **0.45** | 0.97 / 1.68 | 本批最高 0.45，sub 1.11，仍远低于 1.58 |
**判词**：macro 劳动雇佣（Belo-Lin-Bazdresch 机制）在 GBR TOP700 无信号；imbalance5 单一 score 字段无信号；股息面 0.45 弱且与在篮 starval 股息率同族，**不升级、不耗互相关预检**。

## ★数据集普查（2026-11-13 23:35，get_datasets 177 集全拉）——战役级发现
未点亮 10 塔共 **65 个数据集**，此前只勘探过约 14 个；塔级判死（sentiment 枯竭 / socialmedia 判死 / insiders 判死）只覆盖每塔 1-2 个数据集 ⇒ **塔级判死不成立，必须按数据集逐个体检**。按元数据（valueScore/alphaCount/真实 cov）重排后新面：
- **sentiment33** [255f cov0.32 ac224 vs5]——sentiment 塔最大未探集
- **event_ml_signals** [104f ac125 vs7]——other 塔 valueScore 7，企业事件旗标库（M&A/指引/回购/股息/困境/增发/指数调整）
- **earningscall_sentiment** [167f ac66 vs6]、**other696** [220f ac39]、**ai_news_scores** [105f ac122 vs5]
- **insider_matrix** [33f cov0.606 ac617]、**insider_trx_matrix** [33f cov0.6005 ac236]、**insiders1** [9f cov0.594]——insiders 塔未探
- **institutions1/4/6、fund_holdings_panel** [cov0.91 ac321]——institutions 塔未探
- **socialmedia5/12**、**sentiment7**、**option_chart_model** 未探

## GB-Z1/Z2 派发（新面首探，@SUBIND/dec0/nanOFF，各 8 臂）
- **GB-Z1 event_ml_signals** `4uMF3gbli4O4crNcKC6QHHu`：8 个经济机制族各 1 臂——①M&A 传闻+公告（并购溢价）②交易取消（-，并购失败）③M&A 电话会（事件强度）④增发（-，稀释/信号）⑤指引上调−下调（PEAD 类）⑥股息增−减 ⑦审计持续经营疑虑（-，困境）⑧指数纳入−剔除。全部 ts_sum(250)+group_rank(sector)，≤6 ops。
- **GB-Z2 sentiment33** `1USC78J34mhcnCkfq4x7rO`：8 形态臂——①pos−neg ts_sum66（事件频率加权）②pos−neg ts_mean66（逐事件均值）③同式 ts_mean250（长窗水平）④fkw1 vs fkw5 关键词集分歧 ⑤method1 vs method3 模型分歧 ⑥neg 单边（-）⑦neut 占比（-，歧义度）⑧情绪×注意力（valid_tokens 加权）。

## GB-Z1 收割（event_ml_signals，4uMF3gbli4O4crNcKC6QHHu，8/8 COMPLETE）→ 覆盖面大、两处弱活口
| 机制族 | alpha | S | 2Y | TO | lc/sc |
|---|---|---:|---:|---:|---|
| 股息增−减 | **KPgRpPLx** | **0.52** | **1.43** | 0.042 | 418/405 |
| 指数纳入−剔除 | **vRAVbRmb** | **0.52** | 1.12 | 0.045 | 411/412 |
| M&A 电话会强度 | npablp3z | -0.23 | 0.87 | 0.039 | 422/401 |
| 审计持续经营疑虑(-) | j2aQJ2ge | 0.20 | -0.88 | 0.039 | 400/423 |
| 增发(-) | omaeXmV6 | 0.17 | -0.87 | 0.039 | 401/422 |
| M&A 传闻+公告 | pwagkwno | -0.16 | 0.93 | 0.039 | 422/401 |
| M&A 取消(-) | 0mPWLmzq | 0.13 | -0.95 | 0.039 | 401/422 |
| 指引上调−下调 | d5aw65dJ | 0.05 | 0.57 | 0.044 | 422/401 |

**关键读数**：本集 **真实横截面覆盖 400-423/700**（元数据 cov=0 完全失真）⇒ 这是今晚唯一「全宇宙级」的新面。方向全部符合经济学先验（股息增为正、增发为负、M&A 取消为负、持续经营疑虑为负），但强度只有 0.5 档。**两处活口**：股息政策变更（0.52/2Y1.43）、指数成分变更（0.52/2Y1.12）。二波升级方向：窗口阶梯(126/250/504)、差值改比值、decay 近因加权、加 initiation/cancellation 同族腿、STAT/dec15 放大档。

## GB-Z2 收割（sentiment33，1USC78J34mhcnCkfq4x7rO，8/8 COMPLETE）→ 弱且覆盖窄
| 形态臂 | alpha | S | 2Y | lc/sc |
|---|---|---:|---:|---|
| pos−neg ts_sum66 | XgaEO035 | **-0.40** | -0.57 | 122/121 |
| neut 占比(-) | ZYaL1JJY | 0.34 | -0.28 | 121/123 |
| pos−neg ts_mean66 | 2r5k2YgZ | -0.29 | 0.00 | 121/123 |
| 情绪×注意力 | Wjlmx55k | -0.28 | 0.07 | 122/122 |
| pos−neg ts_mean250 | vRAVoQEv | -0.23 | -0.05 | 156/154 |
| neg 单边(-) | 9qlQ2nee | 0.18 | 0.12 | 120/124 |
| method1−method3 | d5awPGMv | -0.07 | 0.51 | 122/122 |
| fkw1−fkw5 分歧 | 1YW52M8W | -0.05 | 0.59 | 121/121 |

**判词**：一是**极性差全为负**（情绪非漂移而是反转，符合长期情绪反转文献），翻号后仅 +0.40；二是**覆盖只有 244/700**（cov 0.32 真实）。TO 0.08-0.13 偏低。**sentiment33 单点初探判弱**（8 臂 × 一个设置档，未达判死穷尽度，标 provisional）。

## GB-Z3 收割（earningscall_sentiment，bBzH037N4PzbtI5H4P98GN，8/8 COMPLETE）→ 弱，但章节结构有信息
| 臂 | alpha | S | 2Y | lc/sc |
|---|---|---:|---:|---|
| cashflow_answer + profitability_answer 复合 | wpoVA6w2 | **0.43** | 0.27 | 266/265 |
| profitability_answer | O0WvjeKv | 0.39 | 0.20 | 266/265 |
| valuation_presentation | pwagk0Qx | 0.32 | 0.67 | 274/269 |
| leverage_summary | RReLoXZn | 0.30 | -0.01 | 274/268 |
| cashflow_question（Q&A） | qM7ZpbbE | 0.24 | -0.58 | 256/262 |
| cashflow_answer | E5QAM3AL | 0.23 | 0.08 | 266/265 |
| assetutilization_question | 6XMbQxPE | -0.19 | -1.36 | 256/262 |
| 负面 cashflow Q&A(-) | 78YVrOq5 | 0.07 | -1.16 | 256/263 |

**判词**：语气方向为正（正面语气 → 正收益），章节（answer vs question vs presentation）与财务维度都有差异但强度 ≤0.43；覆盖 530/700。Matsumoto-Pronk-Wu 的「Q&A 信息含量更高」在 GBR 未显（question 臂 0.24 < answer 0.23 相当）。**provisional 判弱**。

## GB-Z4/Z4b techindi_model 模型变体扫描（★富矿主线）
**Z4a 事故**：字段名把 horizon 段写成 `_d10_q1`（正确为 `_r10_q1`，且 ah3 变体名含 `_ah3_glb_` 双段）⇒ 8/8 ERROR 整批作废（4lI0SidFW4B49sU4gXt4dua）。重发 **Z4b = 3Tpmy71p04zybPM19xLmHuhw**（正确命名，7 模型变体 × 3 周期）。
设计依据：篮内 omEdka3v（S 2.51）的选股腿就是 `group_rank(ts_zscore(tm_17_r1_r5_r10_rh_ah3_glb_d1_r10_q1,126), sector)` ⇒ techindi 是 GBR 唯一验证过的强选股信号源，扫描其余 6 变体（tm_1/8/15/16/18/19）与 5/1 日周期。

## GB-Z5 期权曲面波（option_chart_model，4twa2V2Oc4GAbLls2aB2lU0，8 臂）
13 个期限参考点 × call IV / put IV / put-call parity——GBR 全新机制面（此前 option1 被判定近静态，option_chart_model 从未探）。8 臂：put−call IV 偏斜（期限 4/8/11）、call 期限结构、put 期限结构、call IV 水平(-)、倒挂期限结构(-)、put-call parity(-)。文献：Xing-Zhang-赵（偏斜 → 横截面收益）、Cremers-Weinbaum（IV 差）。**与价格/模型类信号族天然低相关 ⇒ prod 友好候选**。

## GB-Z4b 收割（techindi 变体扫描，3Tpmy71p04zybPM19xLmHuhw，8/8 COMPLETE）→ ★★ 富矿确认，全场最强
| 臂 | alpha | S | F | TO | 2Y | sub | ops |
|---|---|---:|---:|---:|---:|---:|---:|
| tm_16 d5 | A1xd5nmR | **2.85** | 1.35 | 0.421 | 1.21✗ | 1.82 | 2 |
| **tm_19 d10** | **O0Wvjnzv** | **2.81** | **1.40** | 0.380 | **2.13✓** | 1.95 | **2** |
| tm_8 d10 | O0WvjnMv | 2.70 | 1.31 | 0.377 | 0.79✗ | 1.80 | 2 |
| tm_16 d10 | A1xd5nee | 2.68 | 1.27 | 0.380 | 1.04✗ | 1.73 | 2 |
| tm_16 d1 | E5QAMqLr | 2.53 | 1.05 | 0.536 | 1.29✗ | 1.45 | 2 |
| tm_15 d10 | e7aJPnVz | 2.39 | 1.08 | 0.389 | 1.16✗ | 1.83 | 2 |
| tm_18 d10 | wpoVA522 | 1.67 | 0.64 | 0.369 | 1.06✗ | 1.42 | 2 |
| tm_1 d10 | 0mPWLAgp | 1.04 | 0.32 | 0.352 | 0.64✗ | 0.88 | 2 |

**判词**：techindi 是 GBR 唯一「8/8 臂 S≥1.0、6/8 臂 S≥2.3」的选股富矿（覆盖 415/410 真实横截面）。**2Y 是族内瓶颈**（8 臂仅 tm_19 d10 过 2.02 高档线，tm_16 d5 差 0.37）——与残差族相反（那边是 S 瓶颈）。⇒ 后续升级方向聚焦「抬 2Y」而非抬 S。
**O0Wvjnzv 全闸核验（2026-11-14 00:5x）**：platform checks.fail = **[]**（LOW_SHARPE/LOW_FITNESS/LOW_2Y/LOW_SUB/CLUSTER_TEST 全 pass）；逐年 2014-2023 **10/10 正**（S 2.73/4.57/2.85/3.33/3.68/2.40/3.15/2.58/2.56/1.70，最弱 2023 仍 1.70）；self **0.1346**（top 外部件 WjAV89jG 0.13）；与篮子 4 颗互相关 **max 0.2624**（omEdka3v），pairs_over_threshold=[] ⇒ 可入篮。**只差 prod。**

## GB-Z5 收割（option_chart_model，4twa2V2Oc4GAbLls2aB2lU0，8/8 COMPLETE）→ S 死、2Y 有近期强度
| 臂 | S | 2Y | lc/sc |
|---|---:|---:|---|
| call IV level6(-) | -0.34 | -0.65 | 457/278 |
| put−call IV 偏斜（期限4） | 0.27 | **1.43** | 289/447 |
| call 期限结构 0→11 | 0.27 | **1.34** | 284/452 |
| put−call IV 偏斜（期限8） | 0.24 | **1.53** | 289/446 |
| put−call IV 偏斜（期限11） | -0.22 | -1.54 | 447/288 |
| put 期限结构 | 0.17 | 1.49 | 283/452 |
| put-call parity(-) | -0.13 | -0.48 | 447/288 |
| call 期限倒挂(-) | -0.12 | -0.68 | 450/285 |
**判词**：期权曲面**全周期 S ≤0.34**，但多臂 2Y 1.34-1.53 ⇒ 近期才有效、全样本无效（regime-dependent）。GBR 期权覆盖 283-457 名（不对称 lc/sc 提示 IV 缺失结构性）。**不升级，provisional 判弱**。

## ★prod 归因三层结论（补 2026-11-13 未做的归因，用户质询后补）
**第一层（族内几何同质度，本地免费）**：V9 四臂互相关
| 对 | 相关 |
|---|---:|
| RReLlvG0 × npabeXjd | **0.9495** |
| RReLlvG0 × KPgR52WE | 0.9413 |
| npabeXjd × KPgR52WE | 0.8532 |
| RReLlvG0 × j2aQa1qo（跨波：gz/短窗/不同设置） | 0.8001 |
⇒ **窗口/形态/decay/中性化档的差异只让持仓变 5%-20%，本质是同一个持仓**。所以「换几何」不可能把 prod 从 0.87 拉下来——这解释了 j2aQa1qo(0.8496) 与 RReLlvG0(0.8746) 只差 0.025。
**第二层（自身书 vs 外部池）**：RReLlvG0 self max = **0.6079**（KPNgQApj），OS 池 29 颗 ⇒ 自身书重叠只到 0.61，**prod 0.8746 的主体来自外部生产池**（别人已提交的同类残差反转），不是我自己的书堆出来的。
**第三层（对比实验的处置）**：omaeEoZE（V5 冠军 gz w22 @SUBIND/dec4）与 XgaEamR5（w10 @SUBIND/dec4，S1.65）的 prod 对比测试**已排队但被 O0Wvjnzv 终验插队**（prod 单槽）——若二者也在 0.85 档，则「中性化档/窗口不移动 prod」得到跨波独立验证；若显著低，则中性化档是 prod 杠杆、残差族应回炉。

## GB-Z6 收割（tm_19 四轴深挖，3mDTrNfPl4qK90koO4xd5z，8/8 COMPLETE，@SUBIND/dec4）→ ★★ 新科冠军 aka39XYx
| 臂（变换轴） | alpha | S | F | TO | 2Y | sub |
|---|---|---:|---:|---:|---:|---:|
| **周期 r5**（替代 r10） | **aka39XYx** | **2.99** | 1.48 | 0.423 | **2.32** | **2.15** |
| 基准复现 w126 / r10 | (O0Wvjnzv) | 2.81 | 1.40 | 0.380 | 2.13 | 1.95 |
| 窗口 66 | vRAVXaMw | 2.80 | 1.39 | 0.384 | 1.82 | 1.86 |
| group_zscore 替代 group_rank | A1xd8qMR | 2.80 | 1.38 | 0.395 | 2.09 | 2.05 |
| ts_rank 替代 ts_zscore | 1YW5A6Q6 | 2.74 | 1.29 | 0.395 | 2.16 | 2.02 |
| subindustry 轴替代 sector | XgaEAXQa | 2.70 | 1.25 | 0.397 | 2.01 | 1.81 |
| 窗口 252 | VkNobKjY | 2.57 | 1.23 | 0.378 | 2.13 | 2.10 |
| 周期 r1 | LLKxYOj2 | 2.42 | 1.01 | 0.527 | 1.74 | 1.90 |
| hump=0.01 | leaZPJbA | 0.19 | 0.04 | 0.016 | 1.39 | -0.01 |

**判词**：① **周期轴有效**——r5 **2.99 反超 r10 2.81，且 2Y 2.32 / sub 2.15 同步抬**，r1 最弱 2.42 ⇒ 中期预测（5 日）优于 10 日与 1 日；② **窗口/形态/中性化轴全部无效**（66/252/ts_rank/group_zscore/subindustry 均在 2.57-2.80 带内，与基准 ±0.24），再次印证「几何微调不移动信号」；③ **hump 毁信号**（0.19，TO 压到 0.016 把 alpha 磨平）——与 Z4b 结论一致，禁止再上 hump。
**aka39XYx 全闸核验**：checks.fail = **[]**；逐年 2014-2023 **10/10 正**（2.92/4.51/3.20/3.37/3.90/2.64/3.38/2.87/2.69/1.95，**最弱年 1.95 也是全篮最强**）；self **0.1490**（pool 29）；与篮子 4 颗互相关 **0.31 / 0.04 / -0.04 / 0.07** ⇒ 空位级低相关。**只差 prod。**

## techindi 族内互相关矩阵（决定「只能取一颗」）
aka39XYx × O0Wvjnzv **0.9771**、× XgaEAXQa 0.9341、× 1YW5A6Q6 0.8715、× A1xd8qMR 0.8682、× VkNobKjY 0.8782、× vRAVXaMw 0.8175、× LLKxYOj2 0.8940；A1xd8qMR × 1YW5A6Q6 **0.9641**。
⇒ **techindi 全族是一个持仓**（0.62-0.98），几何/周期/分位只在 0.62-0.98 内换皮。**篮子里只能放 1 颗 techindi**，取 S 最高者（aka39XYx 2.99 > O0Wvjnzv 2.81）。O0Wvjnzv 的 prod 因此可作全族（含 aka39XYx）的**同族代理读数**（0.977 同持仓）。

## GB-Z7 收割（分位轴 q1-q5 扫描，4gEKy61vN4yhc6h1b1vg3a95，8/8 COMPLETE）
| 臂 | alpha | S | F | TO | 2Y | sub |
|---|---|---:|---:|---:|---:|---:|
| tm_19 q5 | ZYaLv7K3 | 2.35 | 1.02 | 0.424 | 1.44 | 1.49 |
| tm_19 q4 | RReLw78g | 2.21 | 0.93 | 0.421 | 1.61 | 1.14 |
| tm_17 q3 | zqdznkRG | 2.07 | 0.88 | 0.369 | 0.78 | 1.67 |
| tm_17 q2 | N1Pol7Rp | 2.06 | 0.85 | 0.413 | 0.37 | 1.34 |
| tm_19 q3 | zqdznkmG | 1.84 | 0.76 | 0.345 | 0.63 | 0.89 |
| tm_16 q2 | O0WvX7G1 | 1.65 | 0.62 | 0.401 | 0.17 | 1.09 |
| tm_19 q2 | Grmv5lLO | 1.61 | 0.62 | 0.383 | 0.91 | 0.82 |
| tm_18 q2 | E5QAPlGJ | 1.16 | 0.39 | 0.361 | 0.42 | 0.95 |

**判词**：tm_19 分位轴 **q1 2.99 > q5 2.35 > q4 2.21 > q3 1.84 > q2 1.61 单调递减**；2Y 同样 q1(2.32) 断层第一。**分位轴穷尽、无新入篮件**（q2/q3 在 tm_17/16/18 上也全线走弱，且与 q1 同族 0.8+ 相关）。⇒ 分位维度**关闭**。

## GB-Z8 派发（insiders 塔 insider_matrix 首探，3daERi59Q4ARb68AGbMSLh9，8 臂）
**字段结构**：33 个 MATRIX，cov **0.5938**（真实事件型），结构 = **买/卖 × 均值/总额 × 6 个分组粒度**（aggregated / signal / director / director_signal / top / top_director / top_signal），单位 EUR。alphaCount 最高 eur_signal_value_2（206，买入总额）、eur_signal_value_4（136，卖出总额）⇒ 拥挤集中在这两条。
**机制**（Lakonishok-Lee 2001；Seyhun 1986）：内部人**净买入**预测正收益，卖出因流动性/分散化需求而信息含量低 ⇒ 主腿取「买入−卖出」，并保留买入单边 / 卖出单边反向做对照。粒度先验：**高管（top_signal）> 董事 > 全体**。
**8 臂**：①signal 净买(水平) ②signal 净买(ts_zscore252，剔规模) ③top_signal 净买(水平) ④top_signal 净买(zscore) ⑤director_signal 净买 ⑥aggregated 净买 ⑦买入单边 ⑧均值口径净买。设置：**@SUBINDUSTRY / decay 0 / nan OFF**（事件型标配，见 Z1/Z2 与 memory「nan ON 毁事件型信号」）。

## GB-Z8 收割（insiders，3daERi59Q4ARb68AGbMSLh9，8/8 COMPLETE）→ 方向对、换手爆表
| 臂 | alpha | S | F | TO | 2Y | sub |
|---|---|---:|---:|---:|---:|---:|
| director_signal 净买(水平) | wpoVkN6p | **1.32** | 0.70 | **1.455** | **1.95** | 0.23 |
| signal 净买(水平) | zqdznApV | **1.30** | 0.67 | **1.476** | 1.64 | 0.15 |
| signal 买入单边 | RReLw5Xd | 1.23 | 0.65 | **1.280** | 1.42 | 0.42 |
| 均值口径净买 | QP0dpWeG | 1.21 | 0.60 | **1.476** | 1.04 | 0.19 |
| top_signal 净买(水平) | ZYaLvXL0 | 1.20 | 0.68 | **1.328** | 1.54 | 0.37 |
| signal 净买 zscore252 | RReLw5Ld | 0.66 | 0.24 | 1.505 | 1.10 | 0.65 |
| top_signal 净买 zscore252 | P05EmPEx | 0.58 | 0.20 | 1.431 | 0.57 | 0.64 |
| aggregated 净买 | 78YVRGOO | 0.58 | 0.19 | 1.541 | 1.84 | 0.37 |
**判词**：① **方向全部符合 Lakonishok-Lee**——净买入为正（1.20-1.32），粒度上 **director_signal ≈ signal > top_signal**（高管层反而略弱，与 Seyhun「高管更强」先验相反）；② **换手率 1.28-1.54，全部爆穿 0.70 上限 2 倍以上**，这是唯一但致命的闸；③ sub 仅 0.15-0.42（噪声重）；④ ts_zscore 形式把 S 砍半（0.66）⇒ 内部人数据要**保水平信息**，不能做自身历史标准化。
⇒ 升级路径明确：**同一信号加时序平滑压换手**（Z10）。

## GB-Z10 收割（insiders 平滑，sooGbbkT4Uu9HhimsDNgn8）→ 换手解决了，信号跟着死
| 平滑形式 | alpha | S | F | TO | 2Y | sub |
|---|---|---:|---:|---:|---:|---:|
| ts_decay_linear 22 | rK7mazWE | 1.27 | 0.65 | **1.464** | 1.49 | 0.34 |
| ts_mean 21 | 58JVK6Mk | 1.11 | 0.59 | **0.216** | 0.46 | 0.51 |
| ts_mean 21(director) | qM7Z2zg2 | 1.02 | 0.52 | 0.216 | 0.34 | 0.33 |
| ts_zscore(ts_mean21,252) | aka3mPO9 | 0.89 | 0.38 | 0.249 | 0.85 | 0.58 |
| ts_sum 66(top) | 0mPWZQ8p | 0.86 | 0.45 | 0.073 | 0.25 | 0.62 |
| ts_mean 66 | npabGz3q | 0.69 | 0.32 | 0.079 | 0.40 | 0.66 |
| ts_mean 66(director) | d5awJ7QX | 0.56 | 0.23 | 0.079 | 0.23 | 0.38 |
| ts_mean 126 | leaZwz0A | 0.35 | 0.11 | 0.050 | 0.61 | 0.52 |
**判词**：ts_mean21 把 TO 从 1.46 压到 **0.216（↓85%）** 但 S 从 1.30 掉到 1.11、**2Y 从 1.64 塌到 0.46**；窗口越长两头一起塌（ts_mean66 S 0.69 / ts_mean126 S 0.35）。ts_decay_linear22 保住了 S 1.27 但 TO 仍 1.46（对稀疏事件序列而言 decay 线性加权≈原序列）。⇒ **insiders 的信息集中在"当日事件"，任何平滑都把近两年 alpha 磨掉**；不平滑则换手爆闸 2 倍。**两难无解，provisional 判弱**（累计 16 臂 × 2 设置档，方向、粒度、平滑三轴已覆盖）。

## GB-Z11 收割（techindi winsorize 预处理，3fdZUbbMx4vUbYn5k1ID4Td）→ ★ 确认平台文档要求的 winsorize 在此式里是 no-op
| 臂 | alpha | S | F | TO | 2Y | sub | ops |
|---|---|---:|---:|---:|---:|---:|---:|
| **r5 + winsorize std=2 + w126** | **78YVP2LL** | **3.01** | 1.49 | 0.425 | 2.32 | 2.17 | 3 |
| r5 + winsorize std=3 | 9qlQ52xe | 3.00 | 1.49 | 0.424 | 2.31 | 2.15 | 3 |
| r5 + winsorize std=4 | kqa5pY88 | 3.00 | 1.49 | 0.423 | 2.31 | 2.14 | 3 |
| r5 + winsorize + w66 | gJazN0rm | 2.98 | 1.47 | 0.429 | 2.01 | 2.04 | 3 |
| r10 + winsorize std=2 | Wjlmrxlk | 2.82 | 1.41 | 0.382 | 2.13 | 1.95 | 3 |
| r5 + winsorize + w252 | E5QAn2m1 | 2.73 | 1.30 | 0.423 | 2.29 | **2.27** | 3 |
| r5 + winsorize（无 ts_zscore） | A1xdX2xe | 2.55 | 1.25 | 0.400 | **2.43** | 2.29 | 2 |
**判词**：① 字段描述明确写 "**requires winsorization before use**"（tm_19 是预测 10 日前向市场中性收益的连续回归输出），实测加上 winsorize 只从 **2.99 → 3.01（+0.02，噪声级）**，且 **std=2/3/4 三档差 ≤0.01** ⇒ **后面接 ts_zscore 时 winsorize 完全冗余**（ts_zscore 自身已完成尺度化）——保留 2 ops 的 aka39XYx 而非 3 ops 的 78YVP2LL（同等绩效取算子少者）。② **去掉 ts_zscore 只用 winsorize** 时 2Y 抬到 **2.43（全族最高）**、sub 2.29，但 S 掉到 2.55 ⇒ 「2Y 与 S 互换」的另一种配比。③ 窗口 252 同样抬 2Y（2.29）压 S（2.73）。

## GB-Z12 收割（sentiment7 = Wikipedia 页面浏览量，BRcK8dAt4LScmxRD63PCfQ，8 臂）→ provisional 判弱
字段：仅 3 个 VECTOR（snt7_views / snt7_all_languages_views / snt7_timestamp），cov **0.582**。
| 臂 | alpha | S | F | TO | 2Y | sub |
|---|---|---:|---:|---:|---:|---:|
| 全语种注意力 z252 | 78YVPlvv | **0.61** | 0.15 | 0.494 | 0.70 | 0.66 |
| 英文注意力 z66 | LLKxo3Ev | 0.59 | 0.11 | 0.612 | 0.25 | 0.38 |
| 英文注意力 z252 | Grmvj9XO | 0.45 | 0.08 | 0.525 | 0.35 | 0.75 |
| 注意力 Δ22 | Jj8LarWn | 0.45 | 0.07 | **0.765** | -0.56 | 0.33 |
| 英文注意力 z252 反向 | P05ELKz7 | -0.45 | -0.08 | 0.525 | -0.35 | -0.75 |
| 注意力比率(views/mean252) | 3q0WmJkZ | 0.44 | 0.08 | 0.489 | 0.23 | 0.53 |
| 注意力波动 std66 | 78YVPlM8 | 0.35 | 0.12 | 0.027 | -0.10 | 0.30 |
| 国际占比 | 1YW530Kk | -0.07 | -0.01 | 0.123 | -0.28 | -0.14 |
**判词**：Da-Engelberg-Gao 的注意力→短期价格压力机制在 GBR **不成立**（正反向对称 0.45/-0.45，纯噪声）；全语种比纯英文强（0.61 vs 0.45）是唯一结构信号。TO 0.49-0.77（Δ22 已爆 0.70 上限）。**provisional 判弱，不升级**。

## ★流程纠偏（2026-11-14 00:1x 用户「我是这个意思」）
拿到字段后必须先走 brain-datafield-exploration-general 六法评测，**根据结果**匹配机制模板，模板走 brain-make-some-gem + 论坛（brain-forum-browse）+ 外部金融论文三方补足，改好交用户审后才派发。当晚 Z13/Z14 在纠正前已派出，降级为「机制预探」计入读数，不作为模板依据；后续 S1 六法批为正式评估。

## GB-Z13 收割（risk60 借券费率机制预探，3ueVtW4Nm4mLcvo9zvLsKdz，8/8 COMPLETE）→ provisional 判弱
| 臂 | alpha | S | F | TO | 2Y | sub |
|---|---|---:|---:|---:|---:|---:|
| crowding 反向(-) | ZYaL8ob8 | 0.37 | 0.07 | 0.479 | 0.32 | 0.40 |
| crowding 正向 | e7aJYrQJ | -0.37 | -0.07 | 0.479 | -0.32 | -0.40 |
| 费率水平(-) | xAvaLn1q | 0.14 | 0.03 | 0.163 | -0.03 | 0.33 |
| 费率 Δ66 | E5QAjKpm | 0.12 | 0.02 | 0.314 | -0.36 | -0.10 |
| 费率均值66 | Grmv2oOo | -0.12 | -0.03 | 0.034 | 0.08 | -0.30 |
| 费率 z252 | N1PodOaq | 0.11 | 0.02 | 0.202 | 0.66 | -0.02 |
| 费率 z252 反向 | zqdzxW88 | -0.11 | -0.02 | 0.202 | -0.66 | 0.02 |
| 借出费 z252 | LLKxvRZm | 0.08 | 0.01 | 0.208 | 0.35 | -0.03 |
**判词**：**全族 |S| ≤ 0.37**——Drechsler & Drechsler 的 shorting premium（CME 组合月毛 1.31%）在 GBR TOP700 横截面不成立（cov 0.67 + GC 大盘股费率同质化是可能原因；论坛 risk59 帖「绝大多数大盘股处于基础借券费率」与读数一致）。方向上费率 z252 与 2Y 0.66 有微弱一致性但量级死。**risk60 provisional 判弱**（8 臂覆盖水平/动量/拥挤三形式 × 双方向），不再投六法。

## GB-Z14 收割（sentiment27 流行度机制预探，1KlDPwaLU4gHcJNwzrzVPWZ，8/8 COMPLETE）→ ★totaldomains 亮点
| 臂 | alpha | S | F | TO | 2Y | sub |
|---|---|---:|---:|---:|---:|---:|
| **totaldomains 水平** | **pwag2n2v** | **0.57** | 0.28 | **0.045** | **1.69** | **0.87** |
| snt27_rank 反向 z252（=流行度正向） | aka30N0w | 0.54 | 0.17 | 0.169 | 0.45 | -0.41 |
| relpopularity Δ66 反向 | gJazlmlK | 0.40 | 0.13 | 0.118 | -0.54 | 0.99 |
| relpopularity Δ66 正向 | QP0dxnxX | -0.40 | -0.13 | 0.118 | 0.54 | -0.99 |
| relpopularity z252 反向 | vRAVE57Q | 0.29 | 0.08 | 0.107 | -0.09 | 0.60 |
| skewness 水平 | d5awMnG2 | 0.19 | 0.04 | 0.103 | 0.75 | 0.09 |
| topranking 反向 z252 | e7aJYnYO | 0.09 | 0.01 | 0.099 | 0.74 | -0.37 |
| relpopularity z252 正向 | RReLONxz | -0.29 | -0.08 | 0.107 | 0.09 | -0.60 |
**判词**：三臂方向一致——**流行度水平↑、人气变化↑、域名广度↑ → 正收益**（GBR 的水平效应未被套利干净，与 DEU 帖「水平无效须脉冲」不同）。**pwag2n2v（域名广度）是全场唯一亮点**：S 0.57 / 2Y 1.69 / sub 0.87 / TO 0.045（低频慢信号）。S 离 1.58 闸远，但 2Y/sub 强 + TO 极低 ⇒ 升级候选：作为辅助腿/组合腿、设置档扫描、或与 DEU 脉冲模板（ts_max5+ts_ir22+vector_neut relpopularity08）移植组合。

## S1 六法在线评测（sentiment27，vzlw1Cy4i3ckgzYyHosoD，@NONE/dec0/P0Y0M0D/nanOFF，8/8 COMPLETE）
| 法 | 表达式 | lc | 读数 → 下游决策 |
|---|---|---:|---|
| 法1 覆盖 | vec_avg(snl27_totaldomains) | **644**/700 | 92% ⇒ **不需 ts_backfill** |
| 法1 覆盖 | vec_avg(snl27_relpopularity1) | **644**/700 | 92% |
| 法1 覆盖 | vec_avg(snt27_rank) | **657**/700 | 94% |
| 法2 非零 | divide(td, td) | 644 | 与法1 同 ⇒ 零值可忽略，**不需 trade_when** |
| 法2 非零 | divide(rp1, rp1) | 644 | 同上 |
| 法3 频率 N=22 | divide(ts_std_dev(td,22), 同) | **364**/644=57% | totaldomains = **月/季更慢变量** ⇒ 窗口下限 120+，低换手轨道 |
| 法3 频率 N=5 | divide(ts_std_dev(td,5), 同) | **201**/644=31% | 变化不均，部分公司在持续增删域名 |
| 法3 频率 N=22 | divide(ts_std_dev(rp1,22), 同) | **649**≈100% | relpopularity1 = **日更** ⇒ 短窗脉冲（22）可用 |
**法6/形态（预探回读）**：counts 右偏 ⇒ group_rank（pwag2n2v 实证）；TO 0.045 印证低频。

## S2 六法扩展集派发（totaldomains 法4/5/6 无量纲形式 + kurtosis 法1/2，2UgfiI22u51wbRGZVswG8dw）
§2.7 量纲防线：counts 字段不与裸常数直接比较，法4/5 一律用「当前/自身1年均值」比值（无量纲），法6 用 ts_zscore 分位计数（k=0/1/2 对 50%/16%/2.3% 正态参考）。

## S2 六法扩展集收割（2UgfiI22u51wbRGZVswG8dw，8/8 COMPLETE）→ 法1-6 全部闭合
| 法 | 表达式 | lc/sc | 读数 → 下游决策 |
|---|---|---|---|
| 法4 量纲 | td / ts_mean(td,252) | 644/0 | 92% 覆盖，比值形式无量纲可用 |
| 法4 量纲 | 上 > 2（翻倍） | **1**/0 | 仅 1 只翻倍 ⇒ **结构性扩张是极端稀有事**，不做该档 |
| 法5 中心 | 上 > 1 | 256/0 | 36.6% 高于自身1年均值（对 50% 参考）⇒ 多数公司在存量平台期 |
| 法6 k=0 | ts_zscore(td,252) > 0 | 256/0 | **36.6% vs 50% 参考 ⇒ 右偏**（高于均值者不足半数） |
| 法6 k=1 | 上 > 1 | 122/0 | 17.4% vs 16% ⇒ 右尾近似正态 |
| 法6 k=2 | 上 > 2 | 38/0 | **5.4% vs 2.3% ⇒ 右尾厚 2.3 倍**（须 winsorize 或 rank） |
| kurtosis 法1 | vec_avg(snl27_kurtosis) | **40/488** | ★**极不对称：以负值为主（分布扁平）⇒ 裸用即空头暴露**（S -0.89 就是这么来的） |
| kurtosis 法2 | divide(kurt,kurt) | 528/0 | 真实有效覆盖 **75%**（元数据 cov 待核） |
## ★prod 终验结果：aka39XYx prod = 0.929（FAIL，不入篮）
后台 `bg_0617d85b` 第 6 次重试成功（21 次查询/228s）：`{"alpha":"aka39XYx","max":0.929,"status":"ok"}` → 产物 `results/prod_wait_aka39XYx.json`。
**判词**：S 2.99 / 2Y 2.32 的 techindi 新科冠军，prod **0.929 远超 0.7 门槛** ⇒ **不可提交**。这第二次实证了「prod 由机制族拥挤度决定，不由 S 高低决定」（上次 RReLlvG0 S1.81→prod 0.875；本次 aka39XYx S2.99→0.929）。techindi 族整族（含 O0Wvjnzv 0.977 同持仓）**在 prod 维度已判死**，不再投入终验配额。
**技术侧收获**：① 僵尸槽最终由平台侧释放，prod 端点恢复正常（此前一轮曾报 `platform_unavailable`）；② `prod_wait.py` 的 45 分钟窗口内第 6 次重试成功，验证「按 retry_after 退避、不轰炸」的纪律正确。

## GB-Z15 收割（sentiment27 首波：4 GEM 基线 + 4 机制核心，GUUXl2h4zfc8JtrlZr1XU，8/8 COMPLETE，@SUBIND/dec4/nanOFF）
**派发前置修正**：`ts_max` **不在平台 103 算子目录**（toolkit 静态闸整批拒），DEU 获胜式的 5 日峰值腿改用 **`ts_rank(x, 5)`** 等价替代（当前值在 5 日窗内的分位，接近 1 = 今日即峰值，语义无损且算子可用）。
| 臂类 | alpha | S | F | TO | 2Y | sub | 表达式 |
|---|---|---:|---:|---:|---:|---:|---|
| **基线** | **1YW5rlq6** | **0.66** | 0.32 | **0.024** | **1.58** | 0.58 | `group_rank(ts_mean(vec_avg(snl27_relpopularity1),66), industry)` |
| 基线 | pwag2n2v | 0.57 | 0.28 | 0.045 | **1.69** | **0.87** | `group_rank(vec_avg(snl27_totaldomains), sector)` |
| 机制·脉冲 | KPgRW5Kk | 0.56 | 0.15 | 0.242 | 0.08 | 0.45 | `group_rank(ts_ir(ts_rank(bf(vec_avg(snt7_all),22),5),22), sector)` |
| 基线 | aka30N0w | 0.54 | 0.17 | 0.169 | 0.45 | -0.41 | `multiply(-1, group_rank(ts_zscore(vec_avg(snt27_rank),252), sector))` |
| 基线 | zqdzlglV | 0.47 | 0.19 | **0.020** | **1.51** | 0.81 | `group_rank(ts_mean(vec_avg(snl27_totaldomains),252), subindustry)` |
| 机制·去规模 | e7aJXVlz | 0.32 | 0.07 | 0.242 | -0.26 | -0.23 | `group_rank(vector_neut(脉冲, bf(vec_avg(rp08),22)), sector)` |
| 机制·反转 | XgaEdvja | -0.30 | -0.08 | 0.137 | 0.64 | 0.69 | `multiply(-1, group_rank(ts_ir(ts_rank(rp1,5),22), sector))` |
| 机制·趋势 | j2aQqP5O | 0.14 | 0.03 | 0.079 | 0.26 | -0.08 | `group_rank(divide(ts_mean(rp1,22), ts_mean(rp1,66)), sector)` |
**判词（★区域结论与 DEU 相反）**：
1. **GBR 有效的是「慢速水平」，不是「脉冲」**——4 个机制核心臂（脉冲 0.56 / 去规模 0.32 / 反转 -0.30 / 趋势 0.14）全部弱于 4 个基线臂（0.66/0.57/0.54/0.47）。DEU 帖"水平不可交易、只有脉冲可交易"的结论**在 GBR 不成立**，与 Z12（Wikipedia 水平/动量 max 0.61）一致。
2. **最强臂 1YW5rlq6**（relpopularity1 66 日均值 + industry 轴）S 0.66 / 2Y 1.58 / **TO 0.024**（极低换手、2Y 贴 1.58 线）；**sub 仅 0.58** 是短板。换 industry 轴比 sector 强（0.66 vs 未测）。
3. **totaldomains 两臂稳健**（0.57/2Y1.69/sub0.87 与 0.47/2Y1.51/sub0.81）——水平慢信号在 sector 与 subindustry 轴上都有效，是本数据集最可靠的一条。
4. 距离 1.58 主闸仍有 0.9 差距，**但 TO 0.02 档意味着它适合做低换手轨道或组合辅助腿**，不是单腿破闸的料。

## ★对比实验第三层收割（prod 归因补完，2026-11-14 00:39）
| alpha | 族 | 设置 | S | prod | 判定 |
|---|---|---|---:|---:|---|
| RReLlvG0 | 残差反转 | SUBIND/dec4 | 1.81 | **0.8746** | FAIL |
| j2aQa1qo | 残差反转（gz/短窗） | SUBIND/dec4 | 2.14 | **0.8496** | FAIL |
| **omaeEoZE** | **残差（V5 冠军 gz w22）** | **SUBIND/dec4** | **1.36** | **0.8077** | FAIL |
| aka39XYx | techindi tm_19 r5 | SUBIND/dec4 | 2.99 | **0.929** | FAIL |
| 篮内 4 颗 | 选股腿+借券腿 | SUBIND/dec4 | 2.43-2.60 | 0.60-0.63 | PASS |
**判词（第三层结论闭合）**：同族（残差）内部换形态/窗口，prod 从 0.8746 → 0.8496 → 0.8077，**最大跨度仅 0.067**；跨族（残差 vs techindi）也只有 0.81-0.93。⇒ **几何微调（窗口/形态/中性化/周期）不能把 prod 从 0.81-0.93 拉进 0.70 以内**——几何维度最多动 0.07，缺口是 0.11-0.23。
**唯一能过 prod 的结构是「选股腿 + 借券腿」组合**（篮内 4 颗 0.60-0.63）：借券腿（loaned_share_count）把持仓推向「借券市场拥挤度」维度，与纯选股信号族的持仓空间不重叠。这是 GBR 当前的**唯一可复制 PASS 配方**。

## ★方向纠正与 ATOM 优先纪律（2026-11-14 00:47 用户「在回测完GEM后，是不是应该先在同数据集探究组ATOM优先」）
**问题**：GEM 产出 55 条后我只测了 4 条基线就转去 socialmedia12，**违反 CLAUDE.md「优先寻找单数据集 atom alpha」与「均匀点塔」**。ATOM = 单数据集 alpha，是点塔（3 颗亮一塔）的最短路径；跨集组腿有 5 个总量上限，是稀缺资源。
**修正后的固定顺序**：①GEM 全批回测（GEM 产物天然是同数据集 ATOM 候选）→ ②同数据集内穷尽 ATOM 组装（骨架×字段×窗口×分组轴去重覆盖）→ ③同集 ATOM 确认无解后才考虑跨集组腿 → ④最后才换数据集。
**ATOM 选样方法**（本轮落地）：按 `字段|骨架|分组轴` 分桶，每桶取一条代表（优先 252/66 标准窗），剔除平台不可用算子（ts_max）与已测臂。

## socialmedia12 ATOM 波（2026-11-14 01:0x，@INDUSTRY/dec6/nanOFF，论坛最优设置档）→ provisional 判弱
**GEM 渲染**：`gem_1794589036_c8ab39` → **31 条入 db**（8 概念全部渲染到，质量明显优于 sentiment27 那次：短 backfill(5)、industry 轴、分歧臂、group_std_dev 离散度、反转臂齐全）。
**ATOM 16 臂收割（两批）**：
| alpha | S | F | TO | 2Y | sub | 表达式 |
|---|---:|---:|---:|---:|---:|---|
| 88NA5j07 | **-0.50** | -0.15 | 0.158 | -0.77 | -0.32 | 动量 `ts_mean(ts_rank(bf(sent,5),22),22)/industry`（★论坛最强模式在 GBR 反号） |
| j2aLzjge | 0.26 | 0.03 | **1.019** | -0.05 | 0.38 | `ts_zscore(buzz,66)`（TO 爆闸） |
| xAvMOjRl | -0.23 | -0.07 | 0.046 | 0.91 | 0.16 | buzz mean66/industry |
| vRA0wrEQ | 0.22 | 0.03 | 0.473 | 1.04 | 0.53 | buzz 水平/industry |
| 其余 12 臂 | -0.18~0.15 | — | 0.02-1.02 | -1.01~1.47 | -0.42~0.44 | 含分歧臂 -0.18、离散度 -0.02、反转 -0.11 |
**判词**：
1. **全族 |S| ≤ 0.50 且最强臂为负**——论坛 HS65681 的 USA D0「`ts_mean(ts_rank(field,20),20)` 最强模式（1.3-1.5）」在 GBR **反号到 -0.50**，与 sentiment7/27 的「GBR 注意力类信号无效或反转」完全一致（第三次独立复现）。
2. **INDUSTRY 中性化没有救回来**（论坛 USA 实证 1.38 vs STATISTICAL 0.72 vs NONE 0.41，GBR 实测 top 0.22）⇒ 该设置杠杆是区域依赖的，不能跨区套用。
3. TO 分化极大（0.02-1.02），buzz 系普遍高换手（0.47-1.02）⇒ buzz 是「关注度流量」类快变量，与慢情绪不同源但都无效。
4. **GBR 社媒/注意力三集（sentiment7 / sentiment27 / socialmedia12）全部 provisional 判弱**，跨三集 × 40+ 臂的一致性足够支撑「注意力类信号在 GBR 不可单腿交付」的结论。

## other696 判死（六法实测，Ka7mffTV5bM8BL12SR6d5V7，2026-11-14 01:0x）
**字段结构**（重要发现，值得跨区复用）：220 个 VECTOR，其中 **85 个主题成对**（95 positive + 91 negative），主题覆盖全部基本面维度——acquisitions / backlog / balancesheet / cashflow / debt / demand / dividend / growth / inventory / lawsuit / margin / marketshare / pricepower / supplychain / stockbuyback / stockprice / tax / technology / workforce / cyber / csr / ghgemissions 等；另有无配对的中性与加权情绪（combined_sentiment_score / dl_sentiment_score / growthweighted / valueweighted）。
**六法实测（@NONE/dec0/nanOFF）**：
| 表达式 | lc | sc |
|---|---:|---:|
| vec_sum(oth696_demand_positive) | **0** | 0 |
| divide(vec_sum(demand_positive), 同) | 0 | 0 |
| divide(ts_std_dev(vec_sum(demand_positive),22), 同) | 0 | 0 |
| vec_sum(oth696_demand_negative) | **0** | 0 |
| vec_sum(oth696_orders_positive) | **0** | 0 |
| vec_sum(oth696_combined_sentiment_score) | **5** | 0 |
| vec_sum(oth696_margin_positive) | **4** | 0 |
**判词**：**GBR 区域该数据集无可用数据**（4-5 只是极少数跨市场上市票的残留）。与 sentiment33/event_ml_signals「元数据 cov=0 但实测 400-423 覆盖」相反——**cov=0 有两种含义，必须实测区分**（本轮两次实证：event_ml_signals 失真 vs other696 真实无数据）。**判死，不再投入**；若未来要挖该集，须先换区域。
**教训（写入须记住）**：同一塔内数据集可用性差异极大，**塔级判死不成立（此前已修正），但「元数据 cov=0」也不能反向乐观**——唯一可靠判据是六法在线实测 lc/sc。

## ★跨集组腿波（GB-Z16，Ze2105cE4K794gtwfBLsX6，8/8 COMPLETE，@SUBIND/dec4/nanOFF）→ 关键诊断：借券腿单独只有 0.93
平台原始借券腿（先 `get_alpha_details` 核实，非凭记忆）：
`reverse(group_rank(ts_zscore(ts_backfill(vec_sum(loaned_share_count_main), 250), 504), <轴>))`
| alpha | S | F | TO | 2Y | sub | 构造 |
|---|---:|---:|---:|---:|---:|---|
| gJav60kO | **0.93** | 0.48 | 0.107 | 1.73 | **1.46** | 借券腿单独 / sector（诊断） |
| 88NAb2bo | **0.93** | 0.48 | 0.103 | 1.75 | 1.44 | 借券腿单独 / market（诊断） |
| YPaZ69LW | 0.81 | 0.46 | 0.108 | 1.53 | 1.25 | totaldomains 水平 + 借券 |
| 2r5EM2Mw | 0.81 | 0.44 | 0.084 | 1.42 | 1.33 | totaldomains 252/industry + 借券 |
| N1PM020g | 0.78 | 0.44 | 0.104 | 1.49 | 1.21 | totaldomains + 借券(market 轴) |
| blapXKGR | 0.75 | 0.40 | 0.085 | 1.40 | 1.08 | relpopularity1 66/industry + 借券 |
| RReXMvjo | 0.65 | 0.31 | 0.073 | 1.40 | 1.20 | countrydomains 252/subind + 借券 |
| xAvMqEqp | 0.37 | 0.12 | 0.156 | 1.55 | 0.81 | totaldomains zscore + 借券 |
**判词（★推翻重要假设）**：
1. **借券腿单独 = 0.93**（sector 与 market 轴几乎相同，2Y 1.73-1.75、sub 1.44-1.46、TO 0.10）——它是个**中强腿（0.9 档），不是主腿**。
2. ⇒ 篮内 4 颗 S 2.43-2.60 的构成真相：**主贡献来自选股腿（techindi 2.8-3.0 / 估值 rank），借券腿的核心价值不是抬 S，而是压 prod**（把持仓推到借券拥挤度维度）。
3. **弱选股腿（0.5-0.66 档）叠加会稀释借券腿**：0.93 → 0.81/0.78/0.75/0.65，全部低于借券腿单独。⇒ 「弱选股腿 + 借券腿」不是有效配方，本波 6 个组合臂全败于诊断臂。
4. 唯一例外方向：`xAvMqEqp`（totaldomains zscore 版）S 0.37 最差，与该字段 ATOM 读数（0.04）一致—— zscore 化在 totaldomains 上稳定有害。
5. **结论**：sentiment27 不能当选股腿用（0.5-0.66 档太弱）。要复制「选股腿+借券腿」配方，选股腿必须 ≥2.3 档（techindi 2.99 / 估値 2.6 那种），而这两条在 GBR 的 prod 已分别被判 0.929 / 0.60-0.63——**techindi 已被 prod 封死，估值腿已在篮内**。

## ★塔级扫描第二轮（用户裁定「优先做除 other 外的其它未点亮塔」，2026-11-14 01:5x）
**9 座未亮塔（排除 other）的未探数据集清单**：
| 塔 | 未探 | 实测结论 |
|---|---|---|
| insiders | insider_agg_matrix(cov0.6175/ac612/34f)、insiders12(cov0/ac448) | ★ **insider_agg_matrix 实测仅 14-24 只**（MATRIX 元数据 cov 0.59/1.0 严重失真）；**insiders12 percent 实测 524/700 = 74% 覆盖**（真可用） |
| earnings | earnings_sent_matrix(ac659) | 实测 **14 只**（日内容转录稿情绪概率 POS/NTR/NEG）⇒ 不可用 |
| macro | macro27(ac492/13f) | 招聘族；**num_jobs_active 实测 402/700 = 57%**（裸 S 0.89，需中性化复核） |
| institutions | institutions4(cov0.39)、institutions25(ac100) | institutions4 **percent_of_shares_outstanding 158/700**（裸 S 0.82）；**持仓变化首次双边 86/147** |
| socialmedia | socialmedia39(单字段 cov0.49) | 未测（同 hitscore 族已判弱） |
| sentiment/risk/option/imbalance | 无 | 已全覆盖 |

**探针读数（@NONE/dec0/nanOFF）**：
| 表达式 | lc/sc | S | 判定 |
|---|---|---:|---|
| directional_indicator | 24/0 | 0.66 | 覆盖不足 |
| directional_indicator_2 | 23/0 | 0.79 | 覆盖不足 |
| avg_buy−avg_sell | 9/11 | 0.87 | 覆盖 20 只 |
| earnings pos 概率 | 14/0 | 0.47 | 覆盖 14 只 |
| institutions4 持仓变化 | **86/147** | 0.05 | ★双边但 S 死 |
| institutions4 占流通比 | 158/0 | **0.82** | 单边 |
| **insd12_percent** | **524/0** | **0.68** | ★**74% 覆盖** |
| insd12 变动额 | 275/241 | -0.54 | 双边、负 |
| **num_jobs_active** | **402/0** | **0.89** | ★57% 覆盖 |
| num_jobs_created | 196/0 | 0.85 | 28% 覆盖 |
**关键教训**：**同一塔内 MATRIX 与 VECTOR 数据集可用性可能天差地别**——insider_agg_matrix（MATRIX，元数据 cov 0.59）实测 14-24 只，insiders12（VECTOR，元数据 cov 0）实测 524 只。**元数据 cov 与类型都不能预测真实覆盖，只有六法实测可靠**（本轮第三次验证：event_ml_signals 失真高覆盖 / other696 真实零覆盖 / insider_agg 高cov低覆盖）。
**文献支撑（本轮新增）**：Lakonishok-Lee (2001) 聚合内部人买入预测正异常收益、**群聚模式信息量最高**；**Cohen-Malloy-Pomorski (2012) 预测力集中在「机会型」交易，常规（10b5-1 计划）交易无信息**⇒ 模板必须区分常规/机会型，不能直接用原始买卖总量。KK37637 财报电话会帖（24 赞）：语调 + 可读性 + **不同发言人相对情绪**（CEO vs 其他人）。

## ★★★ 用户指令：算子场景必须全部吃透 + 归因/对照（2026-11-14 02:0x）
原话：「在根据模板组alpha的时候，一定要记住，先把平台允许我用的所有算子场景吃透，都要深度尝试并对结果归因分析和对照分析」。
**执行标准**：组 alpha 前先建「算子场景矩阵」——以主字段固定、窗口固定，**逐类更换算子**做纯净对照（时序 30 / 截面 6 / 分组 11 / 变换 4 / 算数 16 / 向量 8 / 逻辑 11），每臂记录 S/2Y/sub/TO/lc-sc 并归因「为什么这个算子类更强/更弱」，不得零散试算子。
**平台算子全景（103 个，9 类）**：Arithmetic 16 / Logical 11 / Time Series 30 / Cross Sectional 6 / Vector 8 / Transformational 4 / Group 11 / Special 3 / Reduce 14（Reduce 与 Special 多数仅 COMBO scope，REGULAR 不可用）。
**已发现的不可用算子**：`ts_max`、`ts_min`（toolkit 静态闸拒，用 `ts_rank(x,5)` 等价替代峰值语义）；`ts_min_max_cps`/`ts_min_max_diff`（平台 inaccessible）。

## ★ insiders12 的 EVENT 类型陷阱（2026-11-14 02:0x 实证）
**现象**：`group_rank(ts_sum(insd12_positionchangetransactionamount, 66), sector)` 整批 ERROR，报 `Operator ts_sum does not support event inputs`；而同批 `vec_avg(insd12_percent)` 正常。
**根因**：insd12_* 字段虽在元数据标 VECTOR，平台侧按 **EVENT 输入**处理——`ts_*` 系列不能直接作用于裸向量字段，**必须先 `vec_*` 聚合**（`vec_sum`/`vec_avg`/`vec_max`…），聚合后输出标量序列才能进 ts_*。
**纪律**：insiders12（以及所有 insiders/news/shortinterest 系 VECTOR/EVENT 集）的所有表达式，**最内层必须 vec_ 聚合**；单条探针验证 `vec_avg(F)` 通过不代表 `ts_*(F)` 通过——必须验证 `ts_*(vec_avg(F))` 形式。此前六法探针只测了 `vec_avg` 与 `divide` 形式，因此漏掉了这个坑，白烧 2 个 multisim（ATOM 批1 + 矩阵 A 首版）。

### 算子场景矩阵 A：时序族 8 算子对照（24LPUF9sW4gG8GjTWc8bySh，字段=vec_sum(amt) 固定、窗口 66 固定、轴 sector 固定）
| 算子 | S | TO | 2Y | sub | 类属 |
|---|---:|---:|---:|---:|---|
| ts_ir | **-0.09** | 0.040 | -0.26 | -0.09 | 相对化 |
| ts_rank | -0.10 | 0.117 | -0.12 | -0.05 | 相对化 |
| ts_zscore | -0.12 | 0.101 | 0.01 | -0.16 | 相对化 |
| ts_av_diff | -0.19 | 0.073 | 0.08 | -0.32 | 水平偏离 |
| ts_delta | -0.35 | 0.072 | -0.08 | -0.42 | 一阶差 |
| ts_sum | -0.60 | 0.023 | -0.41 | -0.44 | 水平 |
| ts_mean | -0.62 | 0.023 | -0.44 | -0.44 | 水平 |
| ts_decay_linear | **-0.66** | 0.024 | -0.47 | -0.50 | 水平+加权 |
**归因（纯净对照，唯一变量是算子）**：
1. **单调梯度**：相对化算子（ts_ir/ts_rank/ts_zscore）≈ -0.1 ⇒ 水平算子（ts_sum/ts_mean）≈ -0.6 ⇒ 衰减加权 -0.66。**越依赖绝对水平，负向越强**。
2. ⇒ **该字段的绝对金额水平携带强负向信息**（内部人卖出金额大 → 后续跑输），而相对化把这份信息抹掉了。
3. ⇒ ATOM 批1 中 `multiply(-1, ts_sum(amt,5))` 得 **+0.64**（反向=卖压做多对手方）正是这条梯度的直接推论，**不是碰巧**。
4. 与文献先验相反：LLS(2001)「卖出预测力弱于买入」在 GBR insiders12 上**不成立**——GRB 的 amt 字段以卖出信息为主。
5. TO 也随之分化：相对化算子 0.04-0.12，水平算子 0.022-0.024（水平更慢）。

### insiders12 ATOM 批1（2elujZ7VG5hXch5r5PfpBm7，8/8）→ 唯一活口 = 卖压反向
| S | F | TO | 2Y | sub | 表达式 |
|---:|---:|---:|---:|---:|---|
| **0.64** | 0.28 | 0.031 | 0.62 | 0.56 | `multiply(-1, group_rank(ts_sum(vec_sum(amt),5), sector))` ★卖压反向 |
| 0.13 | 0.03 | 0.016 | -0.15 | 0.00 | `rank(ts_mean(vec_avg(percent),66))` |
| 0.11 | 0.02 | 0.020 | -0.17 | -0.06 | percent 66 / industry |
| -0.07 | -0.01 | 0.147 | 0.37 | 0.11 | percent Δ22 / industry |
| -0.36 | -0.15 | 0.016 | 0.28 | 0.17 | sharesheld 252 / industry |
| -0.44 | -0.16 | 0.024 | -0.08 | -0.23 | amt 66 / industry |
| -0.48 | -0.19 | 0.023 | -0.17 | -0.42 | amt/held 相对规模 |
| -0.63 | -0.27 | 0.028 | -0.83 | -0.53 | 方向一致性 |
**判词**：percent / sharesheld 两类负面（持股水平与持仓比重在 GBR 无正预测力），**唯一活口是卖压反向 0.64**（TO 0.031 极低、2Y 0.62）。但 0.64 距 1.58 仍差 0.94 ⇒ 需算子/组合升级。

### 算子场景矩阵 B：截面族 6 + 分组族 2 对照（L1voD6xx4uWa4DCjae2SkO，同信号 ts_sum(amt,66)）
| 算子 | S | F | TO | 2Y | sub |
|---|---:|---:|---:|---:|---:|
| rank | **-0.59** | -0.25 | 0.0191 | -0.44 | -0.43 |
| zscore | -0.64 | -0.37 | **0.0186** | -0.56 | -0.52 |
| scale | -0.64 | -0.37 | **0.0186** | -0.56 | -0.52 |
| normalize | -0.64 | -0.37 | **0.0186** | -0.56 | -0.52 |
| group_neutralize(industry) | -0.64 | -0.37 | 0.0188 | -0.55 | -0.52 |
| quantile | -0.67 | -0.31 | 0.019 | -0.54 | -0.52 |
| **winsorize(std=2)** | **-0.85** | -0.52 | 0.019 | -0.55 | **-0.75** |
| **group_zscore(industry)** | **-0.85** | -0.47 | 0.0197 | **-0.70** | -0.74 |
**归因（两条硬结论）**：
1. **zscore ≡ scale ≡ normalize（-0.64 / F-0.37 / TO0.0186 三项完全相同）** ⇒ 平台实现上三者对同一输入**完全等价**，是同一个变换。**记忆中「归一化形式互换约等价」在本字段得到三项逐位相同的强证据**。⇒ 界面维度只剩 rank（-0.59，温和）/ quantile（-0.67）/ **winsorize 与 group_zscore（-0.85，最强）** 三种真实选择。
2. **winsorize(std=2) 与 group_zscore(industry) 并列最强（-0.85）**——截尾保留极值、分组标准化保留行业内偏离，两者都放大了原始信号的负向强度（比 rank 强 44%）。⇒ **若反向使用（做多卖压小的），winsorize/group_zscore 是最优形态**。

### 算子场景矩阵 C：变换族 4 + 算数族 4 对照（3JBVBj8xr4w48Bbi3XCO2w4，同信号）
| 算子 | S | TO | 2Y | sub | 归因 |
|---|---:|---:|---:|---:|---|
| sign（纯符号） | **-0.30** | 0.024 | 0.09 | -0.18 | ★丢 50% 信息（-0.60→-0.30） |
| sqrt(abs) | -0.31 | 0.022 | -0.17 | 0.07 | 压幅度同损 |
| tail(lower=0.25) | -0.33 | 0.046 | -0.61 | -0.32 | 截尾 25% 损信号 |
| hump(0.02) | -0.33 | **0.010** | 0.13 | -0.45 | 压换手同时把信号砍半 |
| group_rank(bucket 自定分组轴) | -0.55 | 0.031 | -0.55 | -0.39 | 弱于 sector 轴 |
| trade_when(σ>0 门控) | -0.58 | 0.022 | -0.37 | -0.42 | 门控几乎无损 |
| signed_power(zscore,0.5) | -0.60 | 0.023 | -0.41 | -0.44 | 与基线持平 |
| signed_power(group_rank,2) | -0.61 | 0.023 | -0.43 | -0.35 | 与基线持平 |
**归因（硬结论）**：**任何幅度压缩/符号化都会削弱该信号 40-50%**（sign/sqrt/tail/hump 全部从 -0.60 降到 -0.30~-0.33），而保留幅度的势变（signed_power）与门控（trade_when）与基线持平。⇒ **该信号强度完全来自幅度信息**（卖出金额有多大），不能截断也不能符号化。
**矩阵 A+B+C 综合结论（insiders12 的算子全谱）**：
- 时序族：相对化毁信号（-0.1），**水平类最强**（ts_sum/ts_mean -0.60，decay -0.66）
- 截面族：**winsorize / group_zscore 最强（-0.85）**；zscore≡scale≡normalize（三项逐位相同）
- 变换/算数族：**压缩即毁**（sign/sqrt/tail/hump 都 -0.30 档）
⇒ **最优形态 = 水平求和(慢窗) + winsorize/std 或 group_zscore + 反向**，与 ATOM 批的 0.64 活口方向一致。
**bucket 语法教训**：`bucket(...)` 输出 GROUP 类型，**只能作 group_* 的分组参数**，不能嵌套在 group_rank 第一个位置当信号（静态闸报 `Incompatible unit for input of "group_rank" at index 0, expected "Unit[]", found "Unit[Group:1]"`）。

### insiders12 升级波（LwnrR6tw56Kc2pP9qSeWbl，8/8）→ 形态验证成立：0.64 → 0.87
| alpha | S | F | TO | 2Y | sub | 形态 |
|---|---:|---:|---:|---:|---:|---|
| **j2aLNm95** | **0.87** | 0.48 | 0.020 | 0.65 | **0.76** | `-group_zscore(winsorize(ts_sum(amt,66),std=2), industry)` |
| 58JRNWaJ | 0.80 | 0.46 | 0.024 | 0.22 | **0.80** | 同上（22/252 变体） |
| oma2QO32 | 0.68 | 0.31 | 0.026 | 0.57 | 0.57 | `-group_rank(winsorize(ts_sum(amt,66)), sector)` |
| YPaZXq2J | 0.57 | 0.29 | **0.017** | **0.93** | 0.56 | group_zscore 慢窗（2Y 最强） |
**结论**：矩阵 B 的归因（winsorize/group_zscore 最强）**在反向形态上直接兑现**——0.64（group_rank 裸）→ **0.87**（group_zscore+winsorize），**+36%**。这是「先吃透算子场景再做 alpha」的第一份可量化收益。
但 0.87 距 1.58 主闸仍差 0.71 ⇒ insiders12 单腿不够，需组合或换更强机制。

### 算子场景矩阵 D：向量聚合族 8 对照（3zzwFT8U04jHabVVru0rTZh）
| 聚合/变换 | S | 2Y | sub | 归因 |
|---|---:|---:|---:|---|
| **vec_sum（金额求和）** | **-0.60** | -0.41 | -0.44 | ★唯一携带强信号 |
| vector_neut(规模) | -0.60 | -0.32 | -0.36 | 与基线持平 ⇒ **信号与规模正交** |
| 除以持股规模 | -0.48 | -0.17 | -0.42 | 归一化反而削弱 |
| vec_max | -0.30 | -0.24 | 0.04 | 单笔极值丢总量信息 |
| vec_stddev | -0.24 | -0.41 | 0.13 | 离散度无信息 |
| vec_range | -0.20 | 0.00 | 0.20 | 极差无信息 |
| vec_count | -0.18 | 0.92 | 0.01 | 事件计数无信息 |
| 计数反向强化式 | 0.17 | -1.03 | 0.05 | 计数族全无效 |
**归因**：**信号本质 = 交易金额总量**（vec_sum），不是事件频率（count）、不是单笔极值（max）、不是离散度（stddev/range）。且 **vector_neut 与基线持平 ⇒ 与公司规模正交**（这是有利性质：无规模暴露负担）。

## macro27 / institutions4 最优形态试打（CnJlgf0q4BsadkQLAkT9nu，8 臂）→ 均不足
| alpha | S | F | TO | 2Y | sub | 来源 |
|---|---:|---:|---:|---:|---:|---|
| kqaReG5K | **0.82** | 0.40 | 0.135 | 1.05 | **0.17** | macro27 `gz(wins(ts_zscore(num_jobs_active,252)))` |
| 1YWv6K5M | 0.18 | 0.05 | 0.036 | -1.37 | -0.01 | macro27 招聘删除反向 |
| Jj8lRzlx | 0.04 | 0.01 | 0.021 | -0.71 | -0.13 | institutions4 持仓变化反向 |
| 0mPongWk | 0.01 | 0.00 | 0.031 | 1.29 | 0.08 | macro27 岗位 22 日 |
| 3q0dgPd6 | -0.04 | -0.01 | 0.021 | 0.71 | 0.13 | institutions4 持仓变化正向 |
| QP0emzXw | -0.08 | -0.01 | 0.026 | 1.00 | 0.04 | macro27 岗位 66 日 |
| A1x6qzde | -0.11 | -0.02 | 0.035 | 1.38 | 0.10 | macro27 新增岗位 |
| LLKeOzea | -0.24 | -0.08 | 0.021 | -0.53 | -0.57 | institutions4 占流通比 |
**判词**：
- **macro27**：最优形态（gz+wins+ts_zscore）得 0.82 但 **sub 仅 0.17** ⇒ 覆盖 57% 的稀疏性把 sub 打穿，不可交付。招聘族在 GBR **第二次判弱**（第一次 macro 招聘 S -0.04~0.19）。
- **institutions4**：**全族 |S| ≤ 0.24**，机构持仓变化（首次双边）也无信号 ⇒ 与 EUR 实证一致（institutions6 中性化后衰减 -84%）。

### 算子场景矩阵 E：Logical 族 8 对照（oRaXC1oO58l9aRs3uOzsww）
| 形式 | S | TO | 归因 |
|---|---:|---:|---|
| if_else(less(R,0.2), R, 0) | **+0.20** | 0.057 | 只留下尾（当前向做多下尾时为正） |
| or(双尾) | -0.16 | 0.044 | 双尾旗标无信息 |
| not_equal(Δ,0) | -0.30 | 0.099 | 变化旗标弱 |
| and(双条件) | -0.31 | 0.033 | 条件与变弱 |
| if_else(greater(R,0.5),1,0) | -0.35 | 0.032 | ★二元化丢幅度 |
| if_else(greater(R,0.8),R,0) | -0.56 | 0.028 | 只留上尾 |
| if_else(greater(R,0.5),σ,0) | -0.61 | 0.051 | 门控×波动 |
| if_else(greater(ts_rank,0.5),·,0) | **-0.66** | 0.043 | 分位门控最强，仅与基线持平 |
**归因**：**Logical 族整体不增益**——最好的门控形式（-0.66）仅与 ts_decay_linear 基线持平，其余全部更弱；**二元化/条件化破坏幅度信息**（与矩阵 C 的 sign 结论同源）。⇒ 该信号不适合任何逻辑门控。

### 算子场景矩阵 F：Group 族 6 + 更细轴 2（10DlTD22458mbSrvVWXtvwW）
| 算子 | S | TO | 2Y | sub | 归因 |
|---|---:|---:|---:|---:|---|
| group_sum | +0.20 | **0.821** | 0.01 | 0.20 | ★换手爆表（组内求和放大绝对规模） |
| group_std_dev | -0.01 | **0.805** | 0.38 | 0.05 | ★换手爆表 |
| group_count | -0.19 | **0.773** | -1.15 | -0.49 | ★换手爆表 |
| group_backfill | -0.43 | 0.021 | -0.41 | -0.70 | 回填无损但不及基线 |
| group_zscore(subindustry) | -0.57 | 0.019 | -0.76 | -0.42 | 细轴略弱于 industry |
| subtract 与 group_mean(3 参) | -0.64 | 0.019 | -0.55 | -0.52 | 组内去均值 ≡ group_neutralize |
| group_scale | -0.68 | 0.020 | -0.55 | -0.54 | 略强于去均值 |
| **group_neutralize(winsorize)** | **-0.85** | 0.019 | -0.54 | **-0.75** | ★最强（复现矩阵 B） |
**归因**：① **group_sum / group_std_dev / group_count 三者的 TO 0.77-0.82 全部爆穿 0.70 上限**——组内聚合把绝对规模带回信号，是**换手毒药**；② 组内去均值（`subtract(x, group_mean(x,1,g))`）与 `group_neutralize` **数值完全相同（-0.64）** ⇒ 两者等价；③ **group_neutralize(winsorize) 仍是最强（-0.85）**，与矩阵 B 的 group_zscore 并列。
**语法修正**：`group_mean` 需 **3 参数**（`group_mean(x, weight, group)`）；`self_corr` 平台侧 **inaccessible**（目录里有但不可用，与 ts_max 同类）。

### ★组合腿突破（2Yxvk2bgF55rbFJ1feUQrQDd，2026-11-14 02:5x）
| alpha | S | F | TO | 2Y | sub | 构造 |
|---|---:|---:|---:|---:|---:|---|
| **KPgeY5nk** | **1.16** | **0.80** | 0.044 | 1.10 | **1.06** | 卖压反向(66) + 借券腿(sector) |
| d5aq83nX | 1.15 | 0.79 | 0.046 | 1.10 | 1.06 | 卖压反向(66) + 借券腿(market) |
| blap2rNK | 1.14 | 0.77 | 0.048 | 0.95 | **1.10** | 卖压反向(252) + 借券腿(sector) |
| N1PMWJne | 0.90 | 0.56 | 0.045 | **1.45** | 0.85 | 卖压反向(22) + 借券腿 |
| LLKebmka | 0.85 | 0.51 | 0.019 | 0.54 | 0.75 | 卖压反向 group_neutralize 换档 |
| 6XMxPozE | 0.79 | 0.46 | 0.023 | 0.26 | 0.77 | 双信号对偶（66+5 同集） |
**结论**：**（选股腿 0.87 + 借券腿 0.93）组合出 1.16 / F 0.80 / sub 1.06**——加法效应 +0.29，且 Fitness 从 0.48 → **0.80**（这是单腿从未达到的）。TO 0.044 仍在安全区。距 1.58 差 0.42。
⇒ **本组合消耗跨集组腿配额 1/5**（insiders × shortinterest，均非 PV/MODEL/OTHER，合规）。**须查与篮内 4 颗互相关**（篮内都含同一借券腿，有相关性风险）。

## institutions25 / socialmedia5 六法实测（94XSu7JN5adaHCoeLUdeyy）→ 双判弱
| 表达式 | lc/sc | S | TO |
|---|---|---:|---:|
| scl5_hitscore_wordcount | — | **0.51** | **0.917** |
| inst25_crowding | — | 0.48 | 0.179 |
| inst25_concentration | — | 0.47 | 0.033 |
| inst25_activity | — | 0.47 | 0.514 |
| scl5_accountrating | — | 0.42 | **1.273** |
| scl5_avg_sentiment | — | 0.36 | **1.498** |
| scl5_duplicatecount | — | 0.36 | **1.167** |
| inst25_position_change | — | 0.33 | **1.763** |
**判词**：① **socialmedia5 全族 TO 0.92-1.76 爆穿 0.70 上限**（帖级 VECTOR 逐帖聚合天然高换手），S 最高 0.51 ⇒ 不可交付；② **institutions25 |S| ≤ 0.48**，机构行为的 crowding/concentration/activity 三轴全无效 ⇒ 与 institutions4/6/1 一致，**institutions 塔第四次判弱**。
⇒ **至此 9 座未亮塔（除 other）的数据集已全部探完**：sentiment(3)/risk(5)/option(2)/imbalance(2)/macro(2)/socialmedia(3)/insiders(4)/institutions(5)/earnings(2) 共 28 个数据集。

### 8 算子压缩版组合波（1c3NcFgBG599aTs12XADm3Bs）→ 压缩有代价
| alpha | S | F | TO | 2Y | sub | 形态 |
|---|---:|---:|---:|---:|---:|---|
| **78YO0qa2** | **1.04** | 0.71 | 0.054 | 1.13 | 1.01 | `subtract(borrow_simple(market), gz_ts_sum_66_sector)` **8 ops** |
| 9qlobP91 | 1.04 | 0.71 | 0.056 | 1.12 | 1.02 | 同上 sector 轴 |
| O0Weqwnb | 1.00 | 0.67 | 0.056 | 0.96 | 1.03 | 252 窗 |
| Jj8lY0nW | 0.97 | 0.58 | 0.045 | **1.30** | 0.85 | 22 窗 |
| A1x6YJkd | 0.60 | 0.27 | 0.082 | 0.98 | 0.64 | 弱形态对照 |
**关键取舍（算子闸 ≤8 的代价）**：完整形态（winsorize + 回填借券腿）10 算子是 **1.16**；压到 8 算子（去 winsorize、去借券腿回填）只剩 **1.04（-0.12）**。⇒ **算子闸与绩效在 0.1 量级上冲突**，必须按用户闸优先（≤8），即本轮可交付上限 = 1.04。
**结论**：insiders12 组合线的最优合规件 = 78YO0qa2（S 1.04 / F 0.71 / sub 1.01 / TO 0.054），仍差 SHARPE 0.54 与 FITNESS 0.29，**不可交付**。

### 三腿结构波（2XPQz1eWc53jc9m2oTCPhTw）→ S 提升但 2Y 塌
| alpha | S | F | TO | 2Y | sub | 结构（全部 ≤8 ops） |
|---|---:|---:|---:|---:|---:|---|
| **N1PMq72L** | **1.06** | **0.78** | 0.075 | **0.38** | **1.01** | 广度 − 卖压 − 借券（subtract(subtract)） |
| akaJM7G5 | 1.05 | 0.75 | 0.070 | 0.44 | 0.85 | 人气版三腿 |
| MP6wq7V6 | 1.04 | 0.76 | 0.072 | 0.32 | 0.97 | 三腿（借券 sector 轴） |
| qM7bvjpK | 1.00 | 0.70 | 0.066 | 0.65 | 0.79 | 四腿（10 ops 超闸，仅上界参照） |
| ZYaZq71j | 0.40 | 0.17 | 0.053 | 0.97 | 0.35 | 两腿（广度−卖压） |
| GrmVYl75 | -0.45 | -0.22 | 0.068 | 0.38 | -0.43 | 广度+借券（符号错） |
| d5aqgjPw | -0.69 | -0.41 | 0.058 | 0.20 | -0.70 | 借券−卖压（符号错） |
| **Wjlkn7xP** | **-0.92** | -0.62 | 0.063 | -0.07 | **-1.49** | ★借券腿最简形态单独（2 ops） |
**三条硬结论**：
1. **借券腿最简形态 = -0.92（sub -1.49）**，与 Z16 的完整形态（+0.93 反向）**符号相反但绝对值相近** ⇒ 简化丢掉 ts_zscore(504) 后**方向翻转**，说明「借券水平」与「借券历史偏离」是两个不同信号：**水平高 → 未来跑输（-0.92）**，而**历史偏离高 → 反向做多（+0.93）**。这是本塔最重要的机制区分。
2. 三腿（1.06）**略优于**两腿强形态（1.04）与两腿弱形态（1.00），但 **2Y 从 1.13 塌到 0.32-0.44** ⇒ 三腿牺牲了近期稳健性。
3. 汇总当前 insiders12 线全部合规件的上界：**S 1.04-1.06 / F 0.71-0.78 / 2Y 0.32-1.13**，均未过闸。

### 强形态窗口/轴变体波（wnxbNcLG4ArcmG2qHH8jl2）→ 揭示 reverse 的实质作用
| alpha | S | F | TO | 2Y | sub | 构造差异 |
|---|---:|---:|---:|---:|---:|---|
| oma2AP5n | **0.41** | 0.16 | 0.048 | 0.24 | 0.32 | 借券(504)+卖压(industry)，**无 reverse** |
| wpo6ONMx | 0.36 | 0.14 | 0.063 | -0.02 | 0.34 | 借券 252 窗 |
| YPaZnlKR | 0.18 | 0.05 | 0.059 | -0.42 | 0.26 | 卖压 126 窗 |
| ZYaZqX3Q | 0.17 | 0.04 | 0.046 | 0.22 | 0.05 | 卖压 22 窗 |
| blapVx5p | 0.16 | 0.04 | 0.053 | -0.15 | 0.20 | 借券 1008 窗 |
| 78YO0GEQ | -0.25 | -0.08 | 0.072 | -0.47 | -0.31 | market/market 轴 |
**关键发现（★纠正符号认知）**：本批全部是 `subtract(group_rank(ts_zscore(loan,...)), group_zscore(ts_sum(amt,...)))`，最高仅 **0.41**；而 78YO0qa2 同样结构但**多了 `reverse`** 就是 **1.04**。
⇒ **`reverse` 在借券腿上不是装饰，而是决定符号的关键**：`group_rank(ts_zscore(loan,504))` 是「借券历史偏离高」，直接减去它是做空高借券股（错向）；套 reverse 后才是做多高借券股（正确，轧空逻辑）。**此前我以为 subtract 能替代 reverse 省算子——错，reverse 是语义必需，不能用组合顺序替代**。
⇒ 合规最优件仍是 **78YO0qa2（S 1.04 / F 0.71 / sub 1.01 / 2Y 1.13）**，8 ops 满配。

## ★回到 other 塔（依据：非 other 的 9 座 28 集已全部探完；other 塔 2/3 仅剩这一塔未亮；goal 只排除「已点亮塔」）
### other545（NEMO 2.0 网络动量，cov 0.47）六法 + ATOM 16 臂 → 判弱
**六法**：score 覆盖 **329/700**、pln_omen 276、mpd 329；日更；**形态对称（ts_zscore>0 占 50.2%，罕见好性质）**；子分数 S 0.60-0.65 高度同源。
**GEM**：`gem_1794596728_87cfaa` → 41 条 / 17 桶（7 概念全覆盖）。
**ATOM 16 臂（@SUBIND/dec4）**：
| alpha | S | F | TO | 2Y | sub | 字段 |
|---|---:|---:|---:|---:|---:|---|
| RReXYVl0 | **0.54** | 0.27 | 0.054 | 0.09 | 0.54 | mpd 22/sector |
| zqdajY2K | 0.37 | 0.15 | 0.052 | 0.57 | 0.41 | score 22/sector |
| leax2jMe | 0.37 | 0.15 | 0.045 | 0.48 | 0.45 | score 22 裸 rank |
| O0Wek78q | 0.37 | 0.14 | 0.033 | -0.09 | 0.38 | mpd 66/industry |
| YPaZm58l | 0.29 | 0.12 | 0.048 | -0.41 | 0.19 | mpd−pln 分歧 |
| 6XMx1lKJ | 0.29 | 0.08 | **0.182** | 0.07 | 0.49 | score z252 |
| **pln_omen 全族 5 臂** | **-0.11~0.09** | — | 0.025-0.045 | 0.12-0.62 | -0.15~0.27 | ★网络联动分无信息 |
**判词**：① **最强 = mpd（动态价格动量）0.54**；综合分 score 0.37；**网络文本联动 pln_omen 全族 ≈ 0** ⇒ **NEMO 的价值全在价格动量成分，网络联动增量在 GBR 不存在**；② 这是「网络/关联类信号在 GBR 失效」的**第四次独立复现**（sentiment7/27、socialmedia12 前三次）；③ 文献（供应链联动 107bp/月、Cohen-Frazzini）在 GBR 不成立。
**⇒ other545 provisional 判弱，不升级。**

### other567 / other128 六法实测（1VC3YHbI24QDaYY13X2xqz6B）→ 均判不可用（覆盖过低）
| 字段 | lc/sc | 覆盖 | S（无意义） |
|---|---|---:|---:|
| avg_overall_company_score | 19/0 | **19/700 = 2.7%** | 0.91 |
| avg_ceo_approval_score | 19/0 | 19 | 0.90 |
| avg_business_outlook_score | 19/0 | 19 | 0.91 |
| avg_senior_management_score | 19/0 | 19 | 0.91 |
| oth128_ceo_cash_compensation | 9/4 | **13/700** | 0.32 |
| oth128_ceo_tenure | 5/6 | 11 | -0.27 |
| chief_exec_investor_sentiment | 1/1 | **2/700** | -0.11 |
| oth128_executive_efficiency_output | 7/6 | 13 | 0.69 |
**判词**：**other567（员工评价）与 other128（高管薪酬/任期）在 GBR 均只有 2-19 只覆盖**（元数据 cov=0 为真），S 读数无统计意义 ⇒ **双判死**。Edmans 员工满意度机制与高管激励机制在 GBR 无数据支撑。

## ★other 塔真实可用性总表（本轮经验汇总）
| 数据集 | 字段数 | 实测覆盖 | 判定 |
|---|---:|---:|---|
| techindi_model | 399 | **415/700** | ★强信号（2.39-2.99）但 prod 0.929 死 |
| event_ml_signals | 104 | **400-423/700** | 弱活口（股息/指数纳入 0.52） |
| other545 (NEMO) | 4 | **329/700** | 判弱（mpd 0.54，网络联动≈0） |
| other250 (电商) | 12 | **325/700** | 待深挖（rating/review 裸读 0.70-0.75） |
| other696 | 220 | **0-5** | 无数据 |
| other567 (员工评价) | 48 | **19** | 无数据 |
| other128 (高管薪酬) | 14 | **2-13** | 无数据 |
| **规律** | **字段数越多、越"非结构化语义" 的数据集，GBR 覆盖越差**；真正可用的都是「模型输出型」（techindi/NEMO/event_ml）或「电商量化型」（other250） | | |

### other250（电商商品数据，cov 0.46）六法 + ATOM 16 臂 → ★规模暴露陷阱实证
**六法（@NONE）**：item_rating 325、review_count 325、rank/sales_position_rank 342、display_price 326；日更；形态 54% 右偏轻。
★**八字段裸读全部 0.70-0.79**（rating 0.75 / review 0.70 / rank 0.74 / **price 0.79**），而 lc/sc 一律 **325/0 单边** ⇒ 高度同源，本质是「电商规模/热度」暴露。
**ATOM 16 臂（@INDUSTRY 中性化后）**：
| alpha | S | F | TO | 2Y | sub | 字段 |
|---|---:|---:|---:|---:|---:|---|
| RReXa6W0 | **0.21** | 0.05 | 0.034 | 0.22 | 0.15 | **display_price 66**（规模代理最强，验证） |
| akaJPbrR | 0.17 | 0.04 | 0.049 | -0.51 | 0.20 | rating−review 背离 |
| RReXabJg | 0.17 | 0.03 | 0.025 | 0.57 | 0.26 | rating 252 |
| 其余 13 臂 | -0.16~0.08 | — | 0.021-0.106 | -0.54~0.57 | -0.28~0.26 | 含 rating 66/-0.03、rank 反向 -0.12 |
**判词**：**裸读 0.70-0.79 → 中性化后 ≤0.21，衰减 -73%**——这是「NONE 档高读数 = 规模暴露」的**又一次干净实证**（与 EUR institutions6 的 0.97→0.16 同型）。
⇒ **other250 provisional 判弱**：消费者评价/热度信号在剥离规模后无独立信息。文献（京东评论 8 周效应、品牌权益代理）在 GBR 不成立。
**方法论沉淀（跨集通用）**：任何「NONE 档读 0.6-0.8 且 lc/sc 单边」的集，先按规模暴露打折 70-80% 再评估预期，不要被裸读数误导。

## ★event_ml_signals 深度再探（GF1 + 频率验证，2026-11-14 03:3x）
**背景**：该集 104 字段中此前 Z1 只测 8 个机制，**83 个未测**（回购族/困境族/维权股东族/拆分特别股息/分拆剥离/诉讼监管/高管变动）。
### GF1 八机制族（@SUBIND/dec4）
| alpha | S | F | TO | 2Y | sub | 机制 |
|---|---:|---:|---:|---:|---:|---|
| 2r5En1pw | 0.11 | 0.02 | 0.0276 | -1.38 | -0.09 | 诉讼+监管（反向） |
| KPgewK9p | 0.09 | 0.02 | 0.0275 | -1.34 | -0.13 | 困境族（反向） |
| Jj8l5VGm | 0.09 | 0.02 | 0.0276 | -1.34 | -0.11 | 减值+重述（反向） |
| xAvMmKdb | -0.06 | -0.01 | 0.0276 | 1.33 | 0.14 | 拆股+特别股息 |
| oma291ll | -0.09 | -0.02 | 0.0276 | 1.36 | 0.12 | 回购族 |
| GrmV3qe0 | -0.09 | -0.02 | 0.0275 | 1.35 | 0.13 | 维权股东族 |
| O0We51xd | -0.10 | -0.02 | 0.0275 | 1.34 | 0.11 | 分拆剥离 |
| E5Q3rZGL | -0.14 | -0.04 | 0.0277 | 1.27 | 0.03 | 高管+审计变动 |
**★关键异常**：**8 臂 TO 全部 0.0275-0.0277（几乎完全相同）、|S| ≤ 0.14、2Y 呈 ±1.3 对称** ⇒ 说明各机制**没有区分度**。
### 频率验证（2gZGCZ5Qc5d5bCvdRa6AXJE）→ 找到根因
| 字段 | lc | S |
|---|---:|---:|
| buyback_transaction_announcement | **195** | 0.78 |
| bankruptcy_event | **195** | 0.76 |
| activist_nomination_event | **195** | 0.77 |
| lawsuit_legal_issue_event | **195** | 0.76 |
| ma_transaction_announcement_event（已知活跃） | **195** | 0.76 |
| earnings_call_event（ac17 活跃） | **195** | 0.82 |
| dividend_increase_event（Z1 曾出 0.52） | **195** | 0.81 |
| share_repurchase_completion | **195** | 0.78 |
**根因**：**所有事件字段的 lc 完全相同（195）、裸读数全部 0.76-0.82** ⇒ 在 NONE 档下这些字段输出的是**同一个「有记录掩码」**，不同事件类型之间**零区分度**。195/700 = 28% 是该集在 GBR 的**真实可分辨覆盖**（Z1 时期报 400-423 应是 SUBINDUSTRY 中性化下的不同统计口径）。
**判词**：**event_ml_signals 的事件类型维度不可用**——虽然 104 个字段名各不相同、描述各异，但实际只有「有/无记录」一个维度，**不能再按事件类型做机制区分**。Z1 的两个活口（股息 0.52 / 指数纳入 0.52）本质也是同一个掩码的不同加权。
⇒ **GF1 判死，该集不再按事件类型投入。**

## ★★★ sentiment27 系列的致命缺陷：2014-2018 无数据（2026-11-14 05:0x）
**实证**：`add(add(估值腿, group_rank(vec_avg(snl27_totaldomains), industry)), 借券腿)`（j2aL0QA5 / 0mPoEEYG）
→ **逐年 lc=0/sc=0 连续 5 年（2014-2018）**，2019 才开始有持仓（410/393）。
**★`filter=true` 无法修复**：`add(..., filter=true)` 版本（0mPoEEYG S2.76）仍 2014-2018 全 0/0 ⇒ 不是 NaN 求和语义问题，而是 **sentiment27 数据集在 GBR 的起点约 2019 年**。
**影响面**：**所有含 sentiment27/sentiment7 的组合都不可交付**（空窗一票否决），尽管 j2aL0QA5 的 **prod 仅 0.4535**（全场最低）、S 2.65 / F 2.24 —— 指标很美但时间序列不合格。
**纪律**：新数据集入场前必须**先跑一条最简表达式看逐年 lc/sc**，确认 10 年都有持仓，再投入机制设计。sentiment27/sentiment7/socialmedia12 大概率都是 2019 年起步。

## ★★★ 第 6 颗入篮：xAvMdaOl（techindi tm_19 × 借券腿B）全闸通过（2026-11-14 05:11）
`add(group_rank(ts_zscore(tm_19_r1_r5_r10_rh_ah3_glb_d1_r10_q1, 126), sector), reverse(group_rank(ts_zscore(ts_backfill(vec_sum(loaned_market_value_usd_main), 250), 504), sector)))`
GBR/TOP700/D1/**SLOW**/decay 4/trunc 0.08 · **8 ops**
| 闸 | 读数 | 结论 |
|---|---|---|
| S / F / TO | **2.85 / 1.48 / 0.282** | ✓ |
| 2Y / sub | **2.58 / 2.28** | ✓ |
| lc/sc | **454/456 = 910** | ✓ |
| checks.fail / pass | **[]** / 显式含 LOW_SHARPE+LOW_FITNESS+IS_LADDER 共 9 项 | ✓ |
| 逐年 | 2014:S3.38 2015:S4.59 2016:S3.05 2017:S1.60 2018:S2.55 2019:S3.24 2020:S2.27 2021:S2.99 2022:S3.59 2023:S1.61 —— **10/10 全正无空窗** | ✓ |
| 篮子互相关 | omEdka3v **0.4726** / 6XdkW08J 0.429 / A1x63v7Y 0.409 / omExeqLb 0.375 / pwdd7Za6 0.350 | ✓ |
| self / **prod** | **0.4146** / **0.6014** | ✓ |
**成功机制**：**两个字段同时换**（选股腿 tm_17→**tm_19**，借券腿 share_count→**market_value**）⇒ 与 omEdka3v 互相关 0.47、prod 0.60（对比 techindi 纯选股 0.929）。

## ★★★第 7 颗入篮：xAvMjnam（形态反转族 × 借券腿B）全闸通过（2026-11-14 05:45）
`add(multiply(-1, group_rank(v_shape_reversal_bottom_max_similarity, sector)), reverse(group_rank(ts_zscore(ts_backfill(vec_sum(loaned_market_value_usd_main), 250), 504), sector)))`
GBR/TOP700/D1/**SLOW**/decay 4/trunc 0.08 · **8 ops**
| 闸 | 读数 | 结论 |
|---|---|---|
| S / F / TO | **1.81 / 1.02 / 0.157** | ✓ |
| 2Y / sub | **2.03 / 1.84** | ✓（2Y≥1.58 ⇒ 线 2.02，贴线通过） |
| 覆盖 | **456/453 = 909** | ✓ |
| checks.fail / pass | **[]** / 显式含 **LOW_SHARPE+LOW_FITNESS+IS_LADDER** 等 9 项 | ✓★真过闸 |
| 逐年 | 2014:1.42 2015:1.40 2016:0.91 2017:0.86 2018:1.40 2019:1.58 2020:2.88 2021:3.06 2022:2.05 2023:2.03 —— **10/10 全正无空窗** | ✓ |
| 篮子互相关 | **max 0.5474**（xAvMdaOl） | ✓ |
| self / prod | **0.2833 / 0.5861** | ✓ |
**★★★第 5 族发现：pattern_scores（价格形态相似度，cov 0.9998）——技术形态是反向指标**
| 形态字段（正向用法） | S | 含义 |
|---|---:|---|
| V 型底相似度 | -1.34 | 越像 V 型底反转 → 越跑输 |
| V 型顶（反向用法） | -1.38 | 越像 V 型顶 → 也越跑输 |
| 对称三角上涨 | -1.25 | 越像上涨三角 → 越跑输 |
| 跳空上涨 | -1.21 | 越像向上跳空 → 越跑输 |
| 下跌三角（反向） | -1.15 | 同向 |
| 跳空下跌（反向） | -1.14 | 同向 |
⇒ **全部形态相似度负向预测**（技术形态=散户追涨信号，机构借机出货），与现有 4 族机制完全不同源，互相关仅 0.51-0.55、prod 0.53-0.59。

## ★★★第 8 颗入篮：1YWvNaXk（starmine 行业相对估值 × 借券腿B）全闸通过（2026-11-14 07:26）
`add(group_rank(rel_val_industry_rank_score_3, sector), reverse(group_rank(ts_zscore(ts_backfill(vec_sum(loaned_market_value_usd_main), 250), 504), sector)))`
数据集：**model/predictive_starmine**（631 字段、alphaCount 5089、覆盖 0.87-0.93，**此前从未探测**）
GBR/TOP700/D1/**SLOW**/decay 4/trunc 0.08 · **6 ops**
| 闸 | 读数 | 结论 |
|---|---|---|
| S / F / TO | **1.77 / 1.06 / 0.104** | ✓ |
| 2Y / sub | **2.04 / 1.49** | ✓ |
| 覆盖 | **471/438 = 909** | ✓ |
| fail / pass | **[]** / 显式含 LOW_SHARPE+LOW_FITNESS+IS_LADDER 共 9 项 | ✓ |
| 逐年 | 2014:1.79 2015:2.24 2016:**0.09** 2017:1.93 2018:1.33 2019:2.34 2020:2.07 2021:2.11 2022:2.58 2023:1.41 —— 10/10 有持仓无负年 | ✓ |
| 篮子互相关 / self / **prod** | **0.605 / 0.4322 / 0.5909** | ✓ |

## pattern_scores other 78 字段扫描（continuation V 型，1hZ0T5e4b4Zv9lw13WBMHD2m，8 臂）→ 判弱
| alpha | S | F | TO | 2Y | sub | 字段 |
|---|---:|---:|---:|---:|---:|---|
| YPaZ8dvR | **0.76** | 0.29 | 0.149 | 1.54 | 1.29 | 延续底−延续顶 对偶 |
| gJavXz8g | 0.20 | 0.03 | 0.211 | 0.46 | 0.42 | min 延续顶 反向 |
| E5Q3NAGK | 0.07 | 0.01 | 0.149 | 1.10 | 0.49 | cont_v_top_q95 反向 |
| 其余 5 臂 | -0.07~0.06 | ≤0.01 | 0.14-0.21 | 0.55-1.10 | 0.39-0.49 | 单字段/中位/最大/最小 |
**判词**：**continuation V 型（趋势延续）全部无效**（最高 S 0.76），与 reversal V 型（-1.34 强信号）形成鲜明对照 ⇒ **只有「反转形态」在 GBR 有预测力，「延续形态」没有**（散户追涨形态延续买入 → 反向；机构已在反转形态中出货）。
**⇒ pattern_scores 504 字段全部扫描完毕**：有效维度仅 v_shape 反转（-1.34）+ gap/wedge 组合（-1.19），已分别用于 xAvMjnam 与跨形态合成（后者 2Y 卡 1.50）。
## ★pv30 聚类分组轴实验（11IR004z45fza1ghm07hVpt，8 臂，@SLOW/dec4，2026-11-14 08:2x）
**动机**：pv30 有 GROUP 型聚类标签（`factor1_group10_top800_513` / `factor1_group20_top800_513`，**覆盖 1.0**），尝试用「统计聚类」替代行业轴，看能否产生新的持仓维度。
| alpha | S | F | TO | 2Y | sub | 覆盖 | 与篮子 max | 判定 |
|---|---:|---:|---:|---:|---:|---:|---:|---|
| **58JRGdnJ**（star + **聚类group20** + 借券A） | **2.57** | **1.82** | 0.162 | 2.40 | **2.25** | 909 | **0.9104**（6XdkW08J） | ✗ |
| xAvMlpOm（tm_19 + 聚类group10 + 借券B） | 2.83 | 1.47 | 0.282 | 2.53 | 2.24 | 910 | **0.9899** | ✗ |
| E5Q3mPO0（估值 + 聚类group10 + 借券A） | 2.10 | 1.50 | 0.120 | 1.56 | 1.95 | 910 | 0.8886 | ✗ |
| 88NAGx5l / A1x6L8jd（估值 + 聚类） | 2.10/2.07 | 1.50/1.47 | 0.119 | 2.13/2.37 | 1.84/1.92 | 909 | 0.8833/0.8965 | ✗ |
| KPgeVMlN（形态 + 聚类） | 1.85 | 1.05 | 0.158 | 2.28 | 1.82 | 909 | 0.9856 | ✗ |
| QP0eWpZQ（starmine + 聚类） | 1.79 | 1.08 | 0.105 | 2.10 | 1.50 | 909 | 0.9706 | ✗ |
**★关键判词**：**聚类轴在信号强度上优于行业轴**（58JRGdnJ S 2.57/F 1.82 vs omExeqLb S 2.43/F 1.78，同为 star 腿），**但与被替换的件互相关 0.88-0.99** ⇒ **换分组轴只改「组内相对化方式」，不改变信号本体的持仓空间**。
**⇒ 分组轴不是创造新独立维度的杠杆。**（这与早先「中性化档可移动 prod 0.11」不同：中性化档动的是风格暴露，分组轴动的是相对化基准，后者在大盘股上几乎同构。）
## news 塔探针（news18/news17，33JQ8Ea2a5eyaYm14BmVAUy2，8 臂，2026-11-14 08:1x）→ 判弱
**首轮字段名错误**：把 news17 的 `nws17_multiple_comp_event_relevance` 写成 `nws18_multiple_comp_event_relevance` ⇒ unknown variable 连坐整批 CANCELLED（教训：跨集字段前缀必须逐个核对）。
| alpha | S | F | TO | 2Y | sub | 覆盖 | 字段 |
|---|---:|---:|---:|---:|---:|---:|---|
| MP6wgLVo | **0.33** | 0.11 | 0.053 | -0.17 | 0.17 | 474 | news18 nip（影响分） |
| N1PMKR8o | 0.33 | 0.13 | 0.046 | -0.65 | -0.07 | 472 | news17 nip |
| WjlkYVJj | 0.11 | 0.02 | 0.055 | 0.52 | -0.44 | 819 | news18 multiple_comp_ssc |
| 0mPoGM5q | -0.01 | 0.00 | 0.050 | 0.25 | -0.52 | 818 | news18 multiple_comp_qmb |
| npa068rz | -0.06 | -0.01 | 0.058 | 0.61 | 0.00 | 473 | 情绪×相关性加权 |
| Jj8l3vrE | -0.14 | -0.03 | 0.059 | -0.30 | -0.18 | 474 | news18 ssc |
| YPaZlgYq | -0.17 | -0.04 | 0.053 | 0.68 | -0.12 | 473 | news17 ssc |
**判词**：**全族 |S| ≤ 0.33、F ≤ 0.13** ⇒ 新闻情绪/影响分在 GBR 无横截面信号。这是「注意力/情绪类信号在 GBR 失效」的**第五次独立复现**（前四次：sentiment7、sentiment27、socialmedia12、NEMO 网络联动）。
**⇒ news 塔（news18/news17/news104）作为选股腿判弱，不再投入。**
### starmine 剩余维度收割（2E087e3F14ZkaxK13oaeLbmm，8/8 COMPLETE）
| alpha | S | F | TO | 2Y | sub | 覆盖 | 维度 |
|---|---:|---:|---:|---:|---:|---:|---|
| 88NAG9Ra | **1.43** | 0.80 | 0.098 | 1.42 | 1.20 | 909 | EV/EBITDA（score_31） |
| oma2P5Em | 1.41 | 0.77 | 0.107 | 1.48 | **1.53** | 909 | smest 本期vs上期盈利增长 |
| KPgeVdJk | 1.23 | 0.62 | 0.114 | 1.23 | 1.30 | 909 | 隐含5年CAGR + 实际增长合成 |
| j2aLVRej | 0.96 | 0.43 | 0.112 | 1.09 | 1.00 | 909 | 隐含 5 年 EPS CAGR 单独 |
| xAvMl81p | 0.85 | 0.36 | 0.102 | 1.29 | 0.73 | 909 | 隐含 10 年 CAGR |
| RReX5QEn | 0.55 | 0.19 | 0.111 | 1.02 | 0.36 | 909 | 下期vs本期收入增长 |
| QP0eWkvr | 0.47 | 0.16 | 0.101 | 0.81 | 0.76 | 909 | EBITDA 倍数（fy1） |
| **WjlkYQOG** | **-0.03** | 0.00 | 0.117 | 0.19 | 0.24 | 910 | **隐含−实际背离（判高估核心形式）** |
**判词**：**全部 S ≤1.43、F ≤0.80**，无一接近闸线。特别是「隐含增长率−实际增长率」的背离形式（理论上判高估的最强形式）读出 **-0.03**，说明**市场隐含增长预期在 GBR 不构成横截面定价错误**。
**⇒ starmine 维度排查彻底结束：9 个维度全部实测，只有「行业相对估值」1 个达标 ⇒ 该族最终贡献 1 颗（1YWvNaXk）。**
### starmine 剩余维度探针（2E087e3F14ZkaxK13oaeLbmm，8 臂，2026-11-14 07:5x）
动机：starmine 尚有 EBITDA 倍数（90 字段）、growth（13）、PS/CAGR（8）未测；重点测 **iv_market_implied_5yr_eps_cagr_3**（市场隐含 5 年 EPS 增长率，cov 0.873）——这是「市场对未来增长的预期」维度，与已用的估值/修正/形态均不同源。
8 臂：隐含 5 年 CAGR / 隐含 10 年 CAGR / smest 本期vs上期盈利增长 / 下期vs本期收入增长 / EBITDA 倍数 ×2 / 隐含+实际增长合成 / **隐含−实际背离**（后者是判高估的核心形式）。
（读数待收，批次平台侧较慢，进度长时间停在 0.35）
### ZYaZQ2bj 复核 → 不算过闸（2Y 缺口）
| 项 | 读数 | 说明 |
|---|---|---|
| S / F / TO | 1.58 / 1.00 / 0.096 | 贴线 |
| **2Y** | **1.52** | **< 1.58 ⇒ 未达** |
| checks.fail | [] | — |
| **checks.pass** | LOW_SHARPE, LOW_FITNESS, LOW_TURNOVER, HIGH_TURNOVER, LOW_SUB_UNIVERSE_SHARPE, CLUSTER_TEST, MATCHES_PYRAMID | **★缺 IS_LADDER_SHARPE** ⇒ 2Y 未过 |
| prod | 0.4819 | 通过 |
**印证纪律**：**2Y 未达线时平台既不列入 fail 也不列入 pass**（与 F 未达线同理）⇒ 必须逐项核对 pass 清单中的 IS_LADDER_SHARPE，只看 fails=[] 会误判。
### 盈利预测修正维度深挖（1MAOkS62L4NXan2193Lm8DvG，8 臂）
| alpha | S | F | TO | **2Y** | sub | 结构 |
|---|---:|---:|---:|---:|---:|---|
| Xgaqab3a | **1.81** | **1.22** | 0.119 | **1.27** | 0.98 | gz+wins(修正+收入修正) + 借券B |
| d5aqabGX | 1.81 | 1.22 | 0.119 | 1.24 | 0.98 | 三字段合成 |
| npa0adjq | 1.65 | 0.96 | 0.101 | **1.82** | 1.27 | 修正+估值排名 + 借券B |
| 其余 5 臂 | 0.22-0.78 | ≤0.33 | — | — | — | 弱 |
**判词**：修正维度**S/F 可达 1.81/1.22（优秀）但 2Y 只有 1.27**（该族预测力集中在近两年以外？实际是近年衰减）⇒ 不可交付。
**⇒ starmine 最终贡献 = 1 颗（1YWvNaXk 行业相对估值）。行业相对估值是该族唯一 S/F/2Y 三全的维度。**
### starmine 631 字段的估值维度排查（1nev2Z3sU4xecllT8ekrOqP + 2NkDfP3SH4Zt8FZ13qJkLkU1，16 臂）
| 维度族 | 字段数 | 代表字段 | 组合后 S | F | 2Y | 判定 |
|---|---:|---|---:|---:|---:|---|
| **行业相对估值** | 111 | rel_val_industry_rank_score_3 | **1.77** | **1.06** | 2.04 | ★**入篮** |
| 全局估值排名 | 111 | rel_val_global_rank_score_3 | 1.65 | 0.96 | 1.75 | ✗ F 差 0.04 |
| 价格/内在价值(DCF) | 11 | price_to_intrinsic_value_region_rank_3 | 1.61 | 0.92 | 1.43 | ✗ F |
| **盈利预测修正** | 127 | mean_estimate_change_pct_f12m_earnings_90d | 1.55 | 0.89 | **2.17** | ✗ S 差 0.03 + F |
| P/E 分位 | 26 | rel_val_pe_component_score_3 | 1.49 | 0.82 | 1.17 | ✗ |
| FCF 收益率变化 | 5 | eq_vr_dlra2_cashflow_component_change | 1.42 | 0.85 | 1.53 | ✗ |
| EV/EBITDA | 2 | rel_val_ev_ebitda_component_score_3 | 1.33 | 0.71 | 1.35 | ✗ |
| P/B | 2 | rel_val_p_book_component_score_3 | 1.12 | 0.54 | 0.99 | ✗ |
| 股息收益率 | 36 | rel_val_dividend_yield_component_score_3 | 1.08 | 0.50 | 0.92 | ✗ |
**加强形态（group_zscore+winsorize）复测 8 臂**：F 全部 0.21-0.93，**无一突破 1.00** ⇒ 提升 F 不是形态问题，而是这些维度的收益/换手比本身不够。
**⇒ starmine 贡献 1 颗（行业相对估值），其余 8 个维度 F 不足。**
## model25/model26 第 6 族探针（447CqRa3K4lt8Ea16UwqQv0j，2026-11-14 07:0x）→ 判弱
**首轮平台内部错误**（2sHiTn9nj57k8QqvqXr5TCq，8 臂全 ERROR "error while running the simulation"）⇒ 重派即正常，属平台偶发。
| alpha | 覆盖 | S | F | TO | 2Y | field |
|---|---:|---:|---:|---:|---:|---|
| pwa0vPJq | **448** | **1.07** | 0.76 | 0.089 | 0.28 | model26 analyst_revision_primary_earnings |
| 0mPojRn6 | 408 | 0.94 | 0.57 | 0.024 | 0.31 | model25 earnings_quality_raw_score |
| YPaZx5Xo | 422 | 0.78 | 0.43 | 0.027 | -0.06 | model25 accruals_component |
| npa0AKkx | 418 | 0.43 | 0.16 | 0.099 | -0.66 | model26 analyst_recommendation |
| leaxM8Jn | 426 | 0.41 | 0.15 | 0.029 | 0.61 | model25 exclusions_component |
| QP0eY3mG | 445 | 0.34 | 0.15 | 0.100 | -0.11 | model25 global_momentum_percentile（cov 1.0） |
| 6XMxArgG | 446 | 0.31 | 0.13 | 0.062 | -0.18 | model25 long_term_momentum |
| 88NAv3gv | 256 | -0.17 | -0.04 | 0.181 | 0.23 | model25 industry_momentum_2 |
**判词**：model25/model26 虽 alphaCount 极高（2.3-2.7 万），但**实测覆盖仅 256-448 只**（元数据 cov 1.0 严重高估）、**S ≤ 1.07**、**2Y ≤ 0.61** ⇒ **判弱，不能作第 6 族**。
**⇒ 第 6 族候选池已彻底排查完毕**（共 9 个数据集：dl_riskfree / model238 / model264 / model25 / model26 / news104 / pv30 / insiders12 / analyst7），**全部不满足「S≥2.0 选股腿 + 覆盖≥400 + 10 年全历史 + 与现有 5 族正交」**。
## 形态族子族扫描（wedge/triangle，2026-11-14 06:5x）
**pattern_scores 504 字段的形态分布**：gap 112 / triangle 135 / wedge 112 / reversal 43 / v_shape 24 / other 78。
| 探针（@SUBIND 裸形态） | 覆盖 | S | 说明 |
|---|---:|---:|---|
| min_similarity_continuation_rising_wedge_120 | 803 | **0.83** | wedge 族最强 |
| avg_similarity_rising_wedge_pattern_120 | 802 | 0.70 | — |
| asc_triangle_down_mean_simscore_120 | 802 | 0.64 | 上升三角 |
| cont_falling_wedge_min_simscore_60 | 816 | 0.24 | — |
| **avg_similarity_falling_wedge + breakaway_gap_up 合成** | 803 | **-1.19** | ★跨形态合成反向即 +1.19 |
**判词**：**V 型底是 pattern_scores 中信息量最集中的形态**（-1.34），wedge/triangle 单独只有 0.24-0.83；但**跨形态合成**（wedge+gap）可达 1.19。
### 跨形态合成 + 借券腿（4D7lk93Gw4nJbmyJSAatfSf，8 臂，@SLOW）
| alpha | S | F | TO | **2Y** | sub | 覆盖 | 篮子 max |
|---|---:|---:|---:|---:|---:|---:|---:|
| **LLKe5LnM**（wedge+gapUp60+commonGapUp120） | **1.83** | **1.07** | 0.154 | **1.50** | 1.53 | 909 | **0.6339 ✓** |
| N1PMe1gE（wedge+gapUp60） | 1.60 | 0.88 | 0.153 | 1.25 | 1.49 | 910 | 0.5978 ✓ |
| WjlkLjao（楔形+三角） | 1.52 | 0.80 | 0.153 | 1.19 | 1.58 | 910 | **0.5235 ✓** |
| 其余 5 臂 | 1.10-1.30 | ≤0.70 | — | — | — | — | — |
### 2Y 提升尝试（JXBV65IC504blchhjWVCgP，7 臂）→ 未突破
换轴（industry/subindustry）、换借券腿、换 q95 变体、ts_mean10 平滑、掺 V 型底 —— **2Y 全部停在 0.72-1.50**，最高仅 1.50（0mPojWwG，S 1.66/F 0.92）。
**⇒ 形态族跨形态合成的上限：S 1.83 / F 1.07 可达，但 2Y 无法越过 1.50**（差 0.08）⇒ **形态族容量确认 = 1 颗（xAvMjnam）**。
## techindi 族容量再验证（1OSei0aT352XceoZGqE7DjS，8 臂，@SLOW/dec4，2026-11-14 06:4x）
**动机**：A1x63v7Y 证明了「同族换窗口+轴」可产生 0.6793 的低相关变体，故系统扫 techindi 其他模型变体（tm_15/tm_16/tm_18 此前未用作选股腿）。
| alpha | S | F | TO | **2Y** | sub | 覆盖 | 与篮子 max | 判定 |
|---|---:|---:|---:|---:|---:|---:|---:|---|
| 1YWvZdwK（tm_19r5+tm_15 双变体） | **3.21** | 1.57 | 0.367 | 2.38 | 2.46 | 909 | 0.8554（xAvMdaOl） | ✗ 相关 |
| XgaqJn7X（tm_19 换轴） | **3.07** | 1.56 | 0.320 | **2.92** | 2.45 | 910 | **0.9683** | ✗ 相关 |
| j2aL80j9（tm_16 w252） | 2.86 | 1.40 | 0.315 | 1.36 | 2.44 | 909 | 0.7670 | ✗ 相关 |
| gJavZMjl（tm_16+tm_18） | 2.73 | 1.25 | 0.351 | 1.08 | 2.34 | 910 | — | ✗ 2Y |
| **6XMxK9l5**（tm_16 w252/industry + 借券B） | **2.70** | 1.28 | 0.316 | **1.11** | 2.48 | 909 | **0.6982 ✓** | ✗ **2Y 1.11<1.58** |
| zqdabmkR（tm_15） | 2.45 | 1.16 | 0.303 | 2.22 | 2.12 | 909 | 0.7768 | ✗ 相关 |
| MP6w3Q1o（tm_15 换轴） | 2.32 | 1.06 | 0.303 | 1.38 | 2.15 | 909 | 0.7163 | ✗ 相关+2Y |
| RReX687e（tm_18） | 1.78 | 0.72 | 0.293 | 1.33 | 1.76 | 909 | — | ✗ F+2Y |
**判词**：①techindi 全族 S 极高（2.32-3.21）、sub 极强（2.12-2.48），但**互相关被 xAvMdaOl 挡住 0.72-0.97**；②**6XMxK9l5 是唯一互相关通过的（0.6982）**，但 **2Y 仅 1.11**（差 0.47）⇒ 不可交付。
**⇒ techindi 族容量确认 = 2 颗**（omEdka3v tm_17 + xAvMdaOl tm_19），与早先「tm_17/tm_19 各占一颗」一致；tm_15/tm_16/tm_18 均无法通过双闸。
## ★★第 6 族新发现：dl_riskfree_returns（深度学习前向收益分位概率，cov 1.0）
**机制**：`probability_label0_2quantile_{5,20,60}day_ohlcv` = 模型预测「未来 N 日市场中性收益落入**下跌分位**」的对数概率 ⇒ **概率高 = 看跌**，故取负向。
| 探针 | 覆盖 | S | TO | 含义 |
|---|---:|---:|---:|---|
| P5（5 日） | **825** | **-1.18** | 0.243 | 概率高 → 跑输（符合逻辑）✓ |
| P20（20 日） | 826 | -1.17 | 0.248 | 同上 |
| P60（60 日） | 825 | -0.81 | 0.244 | 长窗口衰减 |
**⇒ 单腿反向即 +1.17/+1.18 档（覆盖 825 只）——这是第 6 族候选中最强的一条。**
### 与借券腿组合（33540D67R4TacnP4oz8vLOy，8 臂，@SLOW）
| alpha | S | F | TO | **2Y** | sub | 结构 |
|---|---:|---:|---:|---:|---:|---|
| A1x6Nozw | **1.82** | 0.89 | 0.203 | **0.92** | 1.75 | P5反向 + 借券A |
| LLKeN0z9 | 1.69 | 0.79 | 0.206 | 0.72 | 1.84 | P5反向 + 借券B |
| xAvM3JGp | 1.69 | 0.79 | 0.205 | 0.70 | 1.83 | P5+P20 合成 + 借券A |
| 2r5Ew36Z | 1.65 | 0.77 | 0.203 | 0.70 | 1.76 | P20反向 + 借券A |
| Jj8lN61m | 1.52 | 0.62 | 0.252 | 0.15 | 1.43 | gz+wins 版 |
| KPgeNWQj（纯腿） | 1.39 | 0.53 | 0.251 | -0.28 | 1.01 | 无借券对照 |
**判词**：**S 1.65-1.82 达标，但 2Y 全线 0.15-0.92（要求 1.58）⇒ 致命**。说明该 DL 模型的预测力集中在近期/特定区间，10 年跨度上不稳定。F 0.62-0.89 也未达 1.00。
**⇒ dl_riskfree_returns 判**：S 够但 **2Y 与 F 双不达标**，不升级。
**第 6 族已排除清单**：model238（455 覆盖/0.78）、model264（单字段不稳）、pv30（全 GROUP）、news104（S≤0.35）、insiders12（0.87 弱）、dl_riskfree（2Y 死）。
## 第 6 族候选探针（VbimW4NE4FBbn1JodCUhfS，2026-11-14 06:2x）→ 均偏弱
| alpha | 覆盖 | S | F | TO | 2Y | sub | 字段 |
|---|---:|---:|---:|---:|---:|---:|---|
| N1PMaAN7 | 762 | **0.94** | 0.39 | 0.311 | 0.91 | 0.85 | model264 `3l_vlc`（概率） |
| 3q0dXzog | **453** | 0.78 | 0.42 | 0.119 | 1.11 | 0.36 | model238 industry_rank |
| Wjlkb9ON | 458 | 0.76 | 0.42 | 0.076 | 0.75 | 0.47 | model238 global_screening |
| j2aLA1eo | 458 | 0.73 | 0.39 | 0.112 | 0.88 | 0.40 | model238 global_rank |
| qM7bxgEV | 458 | 0.73 | 0.39 | 0.112 | 0.87 | 0.40 | model238 region_rank |
| vRA0rdOQ / mLaOmZYW | 457 | 0.50/0.49 | 0.17/0.16 | 0.181 | 1.00 | 0.24 | model238 change_rank |
| e7aAbL5O | 761 | -0.43 | -0.17 | 0.191 | -0.38 | -0.44 | model264 `1l_bb` |
**判词**：①**model238（Smart Holdings 评分）有效持仓仅 453-461 只**（元数据 cov 1.0 高估），S 0.49-0.78 ⇒ 不够配借券腿（需 ≥2.0 档）；②**model264 概率字段**：`3l_vlc` 0.94（762 覆盖）、`1l_bb` -0.43 ⇒ 单字段不稳定，但**覆盖 762 只、TO 0.31** 说明该族数据真实；
**⇒ 第 6 族仍需继续找。已排除：model238、pv30（全 GROUP 只能作分组轴）、insiders12（0.87 弱）、model264 单字段布局**。
**⇒ 剩余候选**：news104（cov 0.9695/ac449/f11）、shortinterest3（cov0.849/ac1786）、model25/analyst7（ac 2.4 万但 vs1 拥挤度极高）、other/dl_riskfree_returns（cov0.76/ac1029/f133）。
## 形态族第 2 颗的提 F 尝试（380VHW6jG4xOcsw13tGCfiLg + 2WTQLP7zA4nHca4DwxgeYVy，2026-11-14 06:1x）
### 波1：多形态合成 / 掺估值·star 三腿
| alpha | S | F | TO | 2Y | sub | 与篮子 max | 判定 |
|---|---:|---:|---:|---:|---:|---:|---|
| gJavQrqM（跳空多字段 + **估值** + 借券） | **2.31** | **1.55** | 0.166 | 1.52 | 1.89 | **0.7544**（6XdkW08J） | ✗ |
| QP0e3Wr5（跳空多字段 + **star** + 借券） | 2.06 | 1.37 | 0.146 | 2.08 | 1.73 | **0.7845**（A1x63v7Y） | ✗ |
| 其余纯跳空/三角单字段 | 0.66-1.45 | ≤0.73 | — | — | — | — | ✗ |
**失败原因**：掺入估值或 star 腿后，与篮内对应件互相关 0.75-0.78 超标 ⇒ **形态族第 2 颗不能掺已有 4 族的腿**。
### 波2：纯形态（不掺其他族）+ 平滑/换轴/换借券腿
| alpha | S | F | TO | 2Y | sub | 备注 |
|---|---:|---:|---:|---:|---:|---|
| kqaRox2z（跳空+三角+V顶 ts_mean5） | **1.59** | **0.85** | 0.148 | **2.44** | 1.35 | 最强纯形态 |
| O0WeN1Ev | 1.42 | 0.74 | 0.138 | 1.53 | 1.16 | — |
| zqda8v6V / E5Q3pZX1 / rK7kO1vj | 1.35/1.22/1.18 | 0.63-0.69 | — | — | — | — |
**判词**：**纯形态（非 V 型底）的 F 上限 ≈ 0.85**，因为形态信息量本身弱于 V 型底 ⇒ **F 差 0.15 无法补足**（掺其他族会触发互相关超标）。
**⇒ 形态族对篮子的净增量确认 = 1 颗（xAvMjnam）。**
**⇒ 当前 5 个选股腿族的实际容量**：valuation 2 / star 1 / techindi 2 / transaction 1 / pattern 1 = **7 颗**，与篮子现状一致。
## 形态族容量与变体实测（xpXec9j74gjb4USwAKq4fs 第二批 + 2fEeP9d9T4i19Vr18XSIW0DA 强化波，2026-11-14 05:5x）
**第二批（其他形态字段 + 借券腿，@SLOW）**：
| alpha | S | F | TO | 2Y | sub | 与篮子 max | F 闸 |
|---|---:|---:|---:|---:|---:|---:|---|
| E5Q3ln30（跳空上涨 q95 反向） | **1.69** | 0.88 | 0.171 | 1.79 | 1.50 | **0.6662** ✓ | ✗ F<1 |
| 9qloX5o1（跳空上涨 mean 反向） | 1.61 | 0.84 | 0.166 | 1.58 | 1.49 | **0.5680** ✓ | ✗ F<1 |
| rK7kjako（V型底 ts_mean22） | 1.47 | 0.82 | 0.120 | 1.52 | 1.33 | 0.7327 ✗ | ✗ |
| LLKe7oe6（跳空下跌 q95 反向） | 1.38 | 0.75 | 0.120 | 1.20 | 1.39 | 0.5511 ✓ | ✗ |
| RReX7xXj / 9qloX5o9 / oma2qjeb / 2r5ElVk6 | 0.36~-0.23 | ≤0.1 | — | — | — | — | ✗ |
**V型底强化波（8 臂，提 F 尝试）**：
| alpha | S | F | TO | 2Y | sub | 与 xAvMjnam 相关 |
|---|---:|---:|---:|---:|---:|---:|
| zqdaYoeo（V型底+对称三角） | **1.96** | **1.16** | 0.157 | 2.07 | 1.81 | **0.9394** ✗ |
| RReXVaP1 | 1.89 | 1.08 | 0.161 | 2.04 | 1.82 | 0.9047 ✗ |
| 6XMxrqNJ（ts_mean5） | 1.86 | 1.13 | 0.137 | 2.13 | 1.73 | **0.9789** ✗ |
| pwa0Pz3X（gz+wins） | 1.75 | 1.00 | 0.142 | 2.17 | 1.82 | 0.9427 ✗ |
| WjlkPX0x / 9qloV6kV | 1.62/1.57 | 0.84/0.80 | 0.172 | 2.04/2.25 | 1.58/1.61 | 0.90-0.94 ✗ |
**结论**：①**V 型底族内部只能放 1 颗**（变体互相关 0.90-0.98，xAvMjnam 已占位）；②**其他形态字段（跳空/三角）虽然与篮子互相关 0.55-0.67 有空间，但 F 只有 0.75-0.88 未达 1.00** ⇒ 形态族对篮子的**净增量仍是 1 颗**。
**⇒ 篮子 7/20 已稳，形态族第 2 颗需要把 F 从 0.85 提到 1.00 以上**（可用多形态合成、或与其它独立腿组合提升稳定性）。
## ★F 闸的隐形判定（2026-11-14 05:48 重要区分）
| alpha | S | **F** | 2Y | prod | checks.pass 是否含 LOW_FITNESS | 判定 |
|---|---:|---:|---:|---:|---|---|
| **xAvMjnam** | 1.81 | **1.02** | 2.03 | 0.5861 | **含** | ✓ 真过闸 |
| QP0e7QdX | 1.73 | **0.94** | 2.16 | 0.5339 | **不含** | ✗ 不算过闸 |
**纪律强化**：**F<1.00 时平台不会把 LOW_FITNESS 列入 fail（因为没触发），也不会列入 pass** ⇒ 必须逐项核对 pass 清单，不能只看 fails=[]。同理 S/2Y 未达线时也要核对。
## insiders12 卖压作第 5 族选股腿实测（1PONYXfKJ58gbqBS0KVaZJ6，8 臂，@SLOW/dec4）→ 强度不足
| alpha | S | F | TO | 2Y | sub | 结构 |
|---|---:|---:|---:|---:|---:|---|
| vRA0NO0z | **0.90** | 0.43 | 0.086 | **1.17** | **1.14** | 借券A − 卖压(66) |
| 1YWvpjvz | 0.77 | 0.34 | 0.088 | 0.71 | 0.98 | 借券B − 卖压(66) |
| blapQ87N | 0.74 | 0.36 | 0.074 | 0.53 | 0.75 | 借券A − 卖压rank(66) |
| 1YWvpjvK | 0.61 | 0.26 | 0.080 | 0.56 | 0.30 | 估值+卖压 三腿 |
| 6XMxpAx5 | 0.32 | 0.11 | 0.056 | 0.08 | 0.42 | 卖压纯选股 |
**判词**：**卖压腿最高只有 0.90（单腿 0.87 档）**，与借券腿组合后仅 0.90/0.77 —— 远低于现有 4 族组合的 2.2-2.8。
**根因**：**弱选股腿（0.87）与中强借券腿（0.93）组合只能达到约 0.9**，而非加法叠加（Z16 已实证：弱腿会稀释）。⇒ **选股腿必须 ≥2.0 档才配得上借券腿组合**，insiders12 不满足。
**⇒ 第 5 族选股腿的目标画像**：S ≥ 2.0、覆盖 ≥ 400、10 年全历史、与现有 4 族相关 <0.5。GBR 已探数据集中只有 techindi（2.99 但已用 tm_17/tm_19）、估值（2.6）、star（2.4）达标——**它们就是现有 4 族本身**。
⇒ **GBR TOP700 在 current 数据集范围下的可交付容量 ≈ 6 颗，已达上限**。
## 第三借券族（_p5_d1 变体）实测（4d2bjy5J24CabAqxNThq5rT，8 臂，@SLOW/dec4）
| alpha | S | F | TO | 2Y | sub | 选股腿 × 借券腿 | 与篮子 max | 判定 |
|---|---:|---:|---:|---:|---:|---|---:|---|
| Jj8lGEje | **2.87** | 1.50 | 0.283 | 2.46 | 2.25 | tm_19 × **market_value_usd_p5_d1** | 0.9814（xAvMdaOl） | ✗ |
| 3q0dprqz | 2.72 | 1.39 | 0.284 | 2.34 | 2.26 | tm_19 × **share_count_p5_d1** | 0.9095（xAvMdaOl） | ✗ |
| pwa0Nrw3 | 2.58 | 1.86 | 0.159 | 2.42 | 2.18 | star × **share_count_p5_d1** | 0.9105（6XdkW08J） | ✗ |
| oma2N5m5 | 2.29 | 1.72 | 0.122 | 2.05 | 1.83 | val504 × market_value_p5_d1 | 0.9552（A1x63v7Y） | ✗ |
| xAvMN8KJ | 2.22 | 1.64 | 0.123 | 2.45 | 1.94 | val504 × share_count_p5_d1 | 0.9940（A1x63v7Y） | ✗ |
| **d5aqZVkw** | 2.37 | 1.03 | 0.345 | 1.48 | 1.80 | tm_19 × **market_value_usd**（无 main） | **0.7044**（xAvMdaOl） | ✗（差 0.0044） |
**结论**：**换借券字段族（_main / _p5_d1 / 无后缀）也救不了互相关**——因为同一选股腿的变体在不同借券腿下持仓仍高度重叠（0.70-0.99）。
**★容量判定的本质**：篮子容量不是由「腿的数量」决定，而是由**选股腿的独立维度数**决定。当前 6 颗背后的选股腿只有 4 族（valuation/star/techindi/transaction），而 valuation 占了 2 颗、techindi 占 2 颗（omEdka3v tm_17 + xAvMdaOl tm_19）⇒ **容量已达 4 族的理论上限附近**。
**要再扩容的唯一路径**：引入**第 5 族选股腿**（与现有 4 族相关性 <0.5 的独立信号）。
## ★交叉换腿空间饱和实测（41cE2P4Ws4uPapOm03CRZjP，8 臂）
| 候选 | 选股腿 × 借券腿 | S | F | TO | 2Y | 与篮子 max | 判定 |
|---|---|---:|---:|---:|---:|---:|---|
| gJav9gpg | tm_19 × **A** | **3.04** | 1.58 | 0.303 | 2.73 | **0.9884**（xAvMdaOl） | ✗ |
| 0mPoMNv2 | tm_16 × A | 2.89 | 1.47 | 0.303 | 1.33 | 0.7963（xAvMdaOl） | ✗ |
| xAvMd2aN | tm_16 × B | 2.74 | 1.34 | 0.304 | 1.06 | 0.7322（xAvMdaOl） | ✗ |
| leax35Ze | val66 × B | 2.61 | 1.97 | 0.149 | 2.07 | **0.9626**（6XdkW08J） | ✗ |
| akaJEQ32 | val252 × B | 2.58 | 2.02 | 0.131 | 2.31 | 0.8561（A1x63v7Y） | ✗ |
| O0WexMa7 | **star × A** | 2.57 | 1.84 | 0.159 | 2.37 | **0.9186**（6XdkW08J） | ✗ |
**结论**：**8 种交叉配对已全部试过，6 颗入篮后剩余变体互相关 0.73-0.99 全部超标** ⇒ 该腿库的容量上限 = **6 颗**。要再增件必须引入**全新选股腿族**（现有 4 族已用尽）或**新借券字段**。
## ★★篮内 5 颗的腿构成全貌（资产盘点，2026-11-14 05:0x）
| alpha | 选股腿 | 借券腿 | S | prod |
|---|---|---|---:|---:|
| omEdka3v | techindi **tm_17** w126/sector | **loaned_share_count_main** sector | 2.51 | 0.6026 |
| 6XdkW08J | **valuation_rank w66**/market | loaned_share_count_main **market** | 2.60 | 0.6267 |
| omExeqLb | **star_val_sector_rank w66**/sector | **loaned_market_value_usd_main** sector | 2.43 | 0.6238 |
| pwdd7Za6 | **transaction_count/volume 比率**（非借券结构） | — | 1.69 | — |
| **A1x63v7Y** | **valuation_rank w504**/industry | loaned_share_count_main sector | 2.20 | 0.6303 |
**可用腿库（全历史、高覆盖）**：
- 选股腿 4 族：valuation_rank / star_val_sector_rank / techindi(tm_*) / transaction_count÷volume
- 借券腿 2 族：loaned_share_count_main / loaned_market_value_usd_main
⇒ **交叉换腿 = 4×2 = 8 种配对**，已用 4 种（其中 valuation 用了 2 次不同窗口）。**剩余空间：star×count、techindi×market_value、transaction×任一借券** 等。
## 估值腿族容量上限实测（2026-11-14 04:5x）→ 该族只能放 2 颗
**SLOW 档网格 8 臂（yaITFbJX4Lv8XR10aQd4NTJ）**，覆盖全部 909-910 只、passSharpe 全 true：
| alpha | S | F | TO | 2Y | sub | 与篮子 max 相关 | 结论 |
|---|---:|---:|---:|---:|---:|---:|---|
| leaxVYAx | **2.62** | 1.95 | 0.146 | 2.04 | 2.07 | **0.8686**（6XdkW08J） | ✗ |
| zqda9E3R | 2.53 | 1.94 | 0.132 | 2.27 | 2.05 | **0.8933**（A1x63v7Y） | ✗ |
| 88NAzZNq | 2.33 | 1.77 | 0.123 | 2.21 | 2.00 | 0.8574（A1x63v7Y） | ✗ |
| e7aAOPad | 2.28 | 1.53 | 0.153 | 1.54 | 1.82 | — | ✗（2Y 未过） |
| npa0glad | 2.23 | 1.61 | 0.131 | **2.53** | 1.92 | **0.9655** | ✗ |
| d5aqx6WK | 2.17 | 1.58 | 0.117 | 2.02 | 1.98 | 0.9235 | ✗ |
| A1x6w5VE | 1.99 | 1.39 | 0.117 | 2.24 | 1.87 | 0.9118 | ✗ |
**结论**：8 个网格变体**全部因与篮内互相关 0.86-0.97 超标**（pairs_over_threshold 26 对）⇒ **「估值腿 + 借券腿」族在 SLOW 档下的容量上限是 2 颗**（6XdkW08J w66/market + A1x63v7Y w504/industry）。窗口/轴变体不再提供分离度。
⇒ **要再增件必须换「不同的选股腿」**（不是同族变体）：可用候选只剩高覆盖的 totaldomains（覆盖 556）、relpopularity1（578）、借券腿单独（730）等 0.5-0.9 档信号。
## ★★★★ 第 5 颗入篮：A1x63v7Y 全闸通过（2026-11-14 04:36）
`add(group_rank(ts_zscore(region_relative_valuation_rank, 504), industry), reverse(group_rank(ts_zscore(ts_backfill(vec_sum(loaned_share_count_main), 250), 504), sector)))`
GBR/TOP700/D1/**SLOW**/decay 4/trunc 0.08 · **8 ops**
| 闸 | 读数 | 线 | 结论 |
|---|---|---:|---|
| S | **2.20** | 1.58 | ✓ |
| F | **1.61** | 1.00 | ✓ |
| TO | **0.124** | 0.01-0.70 | ✓ |
| 2Y | **2.41** | 2.02（2Y≥1.58 高档） | ✓ |
| sub | **1.95** | platform | ✓ |
| lc/sc | **453/457 = 910** | ≥300 | ✓ |
| checks.fail | **[]** | — | ✓ |
| **checks.pass** | 显式含 LOW_SHARPE/LOW_FITNESS/LOW_TURNOVER/HIGH_TURNOVER/CONCENTRATED_WEIGHT/LOW_SUB_UNIVERSE_SHARPE/**IS_LADDER_SHARPE**/CLUSTER_TEST/MATCHES_PYRAMID | — | ✓★真过闸 |
| 逐年 | 2014:2.68 / 2016:0.42 / 2018:1.68 / 2020:2.48 / 2022:2.16 | 无负年 | ✓ |
| 篮子互相关 | 6XdkW08J **0.6793** / omExeqLb 0.5134 / pwdd7Za6 0.2566 / omEdka3v 0.2317 | <0.7 | ✓ |
| self | **0.2902** | <0.7 | ✓ |
| **prod** | **0.6303** | <0.7 | ✓ |
**⇒ 篮子 4 → 5 颗（缺口 15）**
**关键成功要素**：①**SLOW 档是 prod 的救命档**（同结构 SUBIND 0.74 / INDUSTRY 0.72 / SLOW 0.63）；②**选股腿换成 504 窗 + industry 轴**（避开已在篮的 6XdkW08J：w66+market，互相关从 0.87-0.92 降到 0.6793）；③借券腿结构不变（已验证过 prod 的成熟腿）。
**杠杆优先级（本族实测）**：中性化档（-0.11）> 选股腿窗口（-0.18，用于降互相关）>> truncation/decay（无效，反而 +0.02）。
## prod 杠杆穷举结果（估值+借券族，2026-11-14 04:2x）
| 设置 | alpha | S | F | TO | 2Y | 覆盖 | **prod** |
|---|---|---:|---:|---:|---:|---:|---:|
| **SLOW**（已在篮） | 6XdkW08J | 2.60 | 1.95 | 0.148 | 2.55 | 909 | **0.6267 ✓** |
| INDUSTRY / trunc0.08 / dec4 / w126 | E5Q3kv91 | 2.57 | 2.51 | 0.116 | 2.63 | 501 | **0.7180 ✗** |
| INDUSTRY / **trunc0.02** / **dec8** / w66 | rK7kW1Wa | 2.60 | 2.44 | 0.114 | 2.68 | 497 | **0.7344 ✗** |
| SUBINDUSTRY / trunc0.08 / dec4 | kqaRQ2d8 | 2.80 | 2.64 | 0.142 | 2.81 | 428 | **0.7387 ✗** |
**结论：truncation（0.08→0.02）与 decay（4→8）都不是 prod 杠杆**（0.718→0.734，不降反升）；**唯一确定有效的是中性化档**（SLOW 0.63 vs INDUSTRY 0.72 vs SUBINDUSTRY 0.74），但 SLOW 档已被 6XdkW08J 占用。
⇒ 同结构变体无法通过换档位把 prod 压进 0.70（除已被占用的 SLOW）。若要用 SLOW 档必须换**选股腿**（不同信号）以避开 6XdkW08J 的持仓。
## ★★★ 中性化档可移动 prod 0.11（2026-11-14 04:2x，修正此前「几何全线不可动」结论）
**证据（同结构 add(估值腿, 借券腿)，只换中性化档）**：
| alpha | 中性化 | S | F | TO | 2Y | sub | lc/sc | **prod** |
|---|---|---:|---:|---:|---:|---:|---:|---:|
| 6XdkW08J（已在篮） | **SLOW** | 2.60 | 1.95 | 0.148 | 2.55 | 2.12 | 451/458 | **0.6267 ✓** |
| kqaRQ2d8 | SUBINDUSTRY | 2.80 | 2.64 | 0.142 | 2.81 | 1.97 | 214/214 | **0.7387 ✗**（差 0.04） |
⇒ **中性化档可移动 prod 约 0.11**（SLOW 0.63 vs SUBIND 0.74）。
**修正此前结论**：早先「几何微调只动 prod 0.07」的证据全部来自**残差族**（RReLlvG0/j2aQa1qo/omaeEoZE/XgaEamR5，全 0.81-0.87）；**估值+借券族对中性化档敏感**，SLOW 与 SUBIND 差 0.11 ⇒ 「几何不可移动 prod」**不能跨族推广**，必须逐族实测。
**同时**：中性化档在「篮子互相关」维度提供约 0.4 的分离度（6XdkW08J×kqaRQ2d8 = 0.6196），使同族变体可以各自入篮。

## ★★INDUSTRY 档产出两个强候选（1QaD9q6Uh4KibyX1dCdt1Yb2）
| alpha | lc/sc | 总持仓 | S | F | TO | 2Y | sub | pass 含 Sharpe | 篮子互相关（max） | self |
|---|---:|---:|---:|---:|---:|---:|---:|---|---|---:|
| MP6wk1ra | 249/249 | 498 | **2.77** | 2.71 | 0.137 | 2.69 | 2.06 | ✓ | **0.7032 ✗（6XdkW08J）** | 0.4752 |
| **E5Q3kv91** | 250/251 | **501** | **2.57** | **2.51** | **0.116** | **2.63** | 1.98 | ✓ | **0.6615 ✓**（6XdkW08J）/ omExeqLb 0.664 / omEdka3v 0.342 / pwdd7Za6 0.273 | **0.4789 ✓** |
- E5Q3kv91 = `add(group_rank(ts_zscore(region_relative_valuation_rank, 126), market), 借券腿)` @**INDUSTRY**/dec4，8 ops
- MP6wk1ra 因 6XdkW08J 0.7032 略超线被排除；两者彼此 0.9466 ⇒ 只能取一个
- **E5Q3kv91 prod 测量中**（bg_8bbf4e4d）

## ★★篮内 4 颗交付前核验（2026-11-14 04:1x，按新纪律执行）
| alpha | lc/sc | 总持仓 | S | F | TO | 2Y | sub | fails |
|---|---:|---:|---:|---:|---:|---:|---:|---|
| omEdka3v | 361/361 | 722 | 2.51 | 1.40 | 0.282 | 2.37 | 2.46 | 空 |
| 6XdkW08J | 451/458 | 909 | 2.60 | 1.95 | 0.148 | 2.55 | 2.12 | 空 |
| pwdd7Za6 | 418/491 | 909 | 1.69 | 1.04 | 0.105 | 2.49 | 1.70 | 空 |
| omExeqLb | 447/462 | 909 | 2.43 | 1.78 | 0.170 | 2.12 | 2.14 | 空 |
⇒ **篮内 4 颗覆盖 722-909 只、TO 0.10-0.30、fails 全空 ⇒ 交付基础稳固。**

## ★★★ 第 5 颗候选：kqaRQ2d8（估值腿 × 中性化档变体）IS 全闸通过
`add(group_rank(ts_zscore(region_relative_valuation_rank, 66), market), reverse(group_rank(ts_zscore(ts_backfill(vec_sum(loaned_share_count_main), 250), 504), sector)))`
GBR/TOP700/D1/**SUBINDUSTRY**/decay 4/trunc 0.08 · **8 ops**
| 闸 | 读数 | 结论 |
|---|---|---|
| S | **2.80** | ✓（线 1.58） |
| F | **2.64** | ✓（线 1.00） |
| TO | **0.142** | ✓ |
| 2Y | **2.81** | ✓（≥1.58 ⇒ 线 2.02） |
| sub | **1.97** | ✓ |
| lc/sc | **214/214** | ⚠ 428 只（61%）达标但不宽裕 |
| checks.fail | **[]** | ✓ |
| **checks.pass** | 显式含 **LOW_SHARPE / LOW_FITNESS / IS_LADDER_SHARPE** 等 9 项 | ✓★真过闸 |
| 篮子互相关 | 6XdkW08J 0.6196 / omExeqLb 0.6091 / omEdka3v 0.4238 / pwdd7Za6 0.2248，pairs_over_threshold=[] | ✓ |
| self | **0.4707**（pool 29） | ✓ |
| prod | 后台 bg_45157bb3 测量中 | 待定 |
**意义**：与 6XdkW08J **同结构不同中性化档**（6XdkW08J @SLOW，本条 @SUBIND），读数 2.60→**2.80** 且互相关仅 0.62 ⇒ **中性化档在「篮子互相关」维度提供约 0.4 的分离度**，足以让同族变体各自入篮（与"几何不能移动 prod"不矛盾：移动的是互相关不是 prod）。

## ★insider_matrix 深度复测（2026-11-14 03:4x-04:0x）→ 高 S 但覆盖极窄，不可交付
**类型坑纠正**：insider_matrix 字段是 **MATRIX 型**，**不能包 `vec_*`**（我误加 vec_sum 导致 3 批 FAIL；裸字段才正确 —— 与 Z8 一致）。
### 处方波（@SUBIND/dec4，MATRIX 裸字段）
| alpha | S | F | TO | 2Y | sub | 形态 |
|---|---:|---:|---:|---:|---:|---|
| npa0Z678 | **1.41** | 0.78 | **1.396** ✗ | 1.43 | 0.40 | `group_rank(winsorize(TOP,std=2), sector)` |
| YPaZ2lvW | 1.39 | 0.73 | **1.491** ✗ | 1.58 | 0.32 | `group_rank(winsorize(NET,std=2), sector)` |
| 6XMxaGlO | 1.34 | 0.70 | 1.480 ✗ | 1.41 | 0.40 | decay_linear 66 |
| 2r5EaGpw | 1.30 | 0.67 | 1.472 ✗ | **1.93** | 0.04 | group_zscore(winsorize(NET)) |
| oma23PNJ | 0.62 | 0.27 | 0.067 ✓ | 0.44 | 0.59 | ts_sum 66 |
### 降换手尝试（全部失败）
- `ts_target_tvr_decay(..., target_tvr=0.6/0.4)`：**TO 不降反升（1.48-1.51）、S 塌到 0.08/-0.56** ⇒ 该算子对事件型稀疏信号无效
- **平台设置 decay=20 / decay=40**：TO 仍 1.39-1.49 ⇒ 高换手来自**信号日频变动本身**，设置档无效
- 长窗 ts_sum 126/252/504：S 0.27/0.19/0.36，信号磨平
### 混合形态（时序均值 + 截面截尾）→ 找到 TO 平衡点，但暴露覆盖真相
| alpha | S | F | TO | 2Y | sub | **lc/sc** | 持仓数 |
|---|---:|---:|---:|---:|---:|---:|---:|
| mLaOqjbK | **1.38** | 0.66 | **0.694** ✓ | 0.94 | 0.77 | **19/19** | **38** |
| 2r5EvlLw | 1.30 | 0.67 | 1.464 ✗ | 1.59 | 0.27 | **2/2** | **4** |
| Jj8ln7Om | 1.20 | 0.58 | 0.399 ✓ | 0.85 | 0.34 | 43/42 | 85 |
| WjlkN7Gk | 1.04 | 0.56 | 0.195 ✓ | 0.35 | 0.44 | 90/93 | 183 |
| VkNnX7PV | 1.02 | 0.55 | 0.219 ✓ | 0.70 | 0.55 | 93/89 | 182 |
**★★关键结论（自我纠正）**：**S 与覆盖率严格单调反向**——1.38→38 只、1.30→4 只、1.20→85 只、1.02→182 只。
且 **mLaOqjbK 的 checks.pass 里根本没有 LOW_SHARPE/LOW_FITNESS/LOW_2Y**（对比 KPgeY5nk 明确列出失败项）⇒ **稀疏持仓导致平台跳过 Sharpe 类检查**，fails=[] 是假象，**不是真过闸**。
⇒ **insider_matrix 在 GBR TOP700 有效持仓仅 4-183 只（eur_* 元数据 cov 0.59 严重高估）**，与最初六法 lc 14-24 的读数一致。**判不可交付**；教训：**看到高 S 必须先核对 lc/sc，覆盖率不足时的高 S 是样本假象**。


### event_sentiment_signals 六法实测（3cD4im1vG5cZco6oUoI6yOx）→ 判死
| 字段 | lc | S |
|---|---:|---:|
| key_factor_positive_event_count_section | **3** | -0.11 |
| key_factor_negative_event_count_section | **3** | -0.11 |
| event_count_in_section_aggregation | **3** | -0.12 |
| event_weight_aggregation | **3** | -0.11 |
| key_factor_positive_score_section | **3** | -0.11 |
| key_factor_negative_score_section | **3** | -0.11 |
**判词**：**仅 3 只股票有数据**（3/700 = 0.4%）⇒ 判死。且与 event_ml_signals 同一模式（所有字段 lc 相同、读数相同）⇒ **该数据源在 GBR 基本不落地**。

## ★★★ other 塔勘探闭合（2026-11-14 03:4x，7 个数据集全部实测）
| 数据集 | 字段数 | **真实覆盖** | 最强读数 | 判定 |
|---|---:|---:|---:|---|
| techindi_model | 399 | **415/700** | **2.99** | ★强信号但 prod 0.929 封死 |
| event_ml_signals | 104 | **195/700（可分辨）** | 0.52（股息/指数纳入） | 事件类型维度无区分度，判死 |
| other545 (NEMO) | 4 | 329/700 | 0.54（mpd） | 判弱（网络联动≈0） |
| other250 (电商) | 12 | 325/700 | **中性化后 0.21** | 判弱（裸读 0.79 是规模暴露） |
| other696 | 220 | 0-5 | — | 无数据 |
| other567 (员工评价) | 48 | 19 | — | 无数据 |
| other128 (高管薪酬) | 14 | 2-13 | — | 无数据 |
| event_sentiment_signals | 52 | **3** | — | 无数据 |
**★other 塔的覆盖规律（可跨区复用）**：**字段数越多、越偏「非结构化语义解析」的数据集，GBR 覆盖越差**（220→0、52→3、48→19、14→13）；真正可用的只有两类——①**模型输出型**（techindi 399 字段但覆盖 415、NEMO 4 字段覆盖 329），②**量化计数型**（event_ml 104 字段覆盖 195、other250 12 字段覆盖 325）。⇒ **选数据集时"字段数"是负向指标，"是否模型输出/量化计数"是正向指标**。





















**本轮 ATOM 批**：55 条 → 23 桶 → 剔重后 **18 条纯 ATOM**（单集 sentiment27，2-3 算子），分 3 批：
- 批1 `Pcg7n7mP4nL8ZY195WfwKrH`：relpopularity1 ×{率比/rank/zscore/3 轴} 5 臂 + kurtosis ×{gr_z/rank/zscore} 3 臂
- 批2 `2xQdrIbKu4qbchw14E5QY3JB`：kurtosis ×{subind/industry} 2 臂 + totalcountrydomains ×{lvl/rank/zscore/2 轴} 5 臂 + totaldomains rank 1 臂

### ATOM 批1/批2 收割（18 臂单集 sentiment27，@SUBIND/dec4/nanOFF）→ ATOM 空间已穷尽，上限 0.66
| alpha | S | F | TO | 2Y | sub | 表达式 |
|---|---:|---:|---:|---:|---:|---|
| 1YW5rlq6(Z15) | **0.66** | 0.32 | 0.024 | 1.58 | 0.58 | relpop1 mean66 / industry |
| GrmVrE5x | 0.58 | 0.27 | 0.022 | 1.41 | 0.61 | relpop1 mean**252** / industry |
| pwag2n2v(Z15) | 0.57 | 0.28 | 0.045 | **1.69** | **0.87** | totaldomains 水平 / sector |
| zqdzlglV(Z15) | 0.47 | 0.19 | 0.020 | 1.51 | 0.81 | totaldomains mean252 / subind |
| RReXR0wn | 0.44 | 0.19 | 0.019 | 1.38 | 0.55 | relpop1 mean252 裸 rank |
| vRA0RJaQ | 0.43 | 0.16 | 0.020 | 1.50 | 0.73 | countrydomains mean252 / subind |
| 1YWvYnVQ | 0.41 | 0.16 | 0.021 | 1.46 | 0.73 | countrydomains mean252 / industry |
| ZYaZYWkZ | 0.40 | 0.16 | 0.044 | 1.54 | **0.89** | countrydomains 水平 / sector |
| YPaZPWwv | 0.39 | 0.16 | 0.018 | 1.40 | 0.75 | totaldomains mean252 裸 rank |
| N1PM1kle | 0.38 | 0.14 | 0.020 | 1.26 | 0.41 | relpop1 mean252 / subind |
| WjlkjWKN | 0.27 | 0.09 | 0.018 | 1.22 | 0.74 | countrydomains mean252 裸 rank |
| kurtosis 全族 5 臂 | -0.25~0.20 | — | 0.02-0.18 | 0.14-0.84 | -0.37~0.33 | 含 gr_z/rank/zscore×3 轴 |
| **totalcountrydomains zscore252** | **-0.97** | -0.50 | 0.170 | 0.16 | -0.37 | ★强负读数（相对自身历史扩张 → 跑输） |
**判词**：
1. **ATOM 上限 = 0.66**（relpopularity1 66/industry），与 Z15 一致；**18 臂 × 4 字段 × 3 骨架 × 3 轴 × 3 窗口已覆盖，无新入篮件**。
2. 结构性发现：totaldomains/totalcountrydomains 的**水平**与**长窗均值**都有效（0.39-0.57，2Y 1.4-1.7，sub 0.73-0.89），但**自身历史 zscore 化会毁信号甚至反号**（countrydomains zscore = **-0.97**）⇒ 这两字段含**慢速水平信息**，不能做时序相对化——与 kurtosis 的处理方式正好相反（kurtosis 必须时序相对化）。这是本集最重要的方法学结论。
3. kurtosis 即便对称化后仍无信号（≤0.25）⇒ 概念 7 判死。
4. 全部臂 TO 0.018-0.18（极低换手）、sub 0.4-0.89，说明这是**慢速质量/认知因子**，不是破闸料。
- 批3 `1FPkYe9Gx4FubPoRE2Y9BcV` 收割：`88NA8RYq`（totaldomains mean252 / **industry** 轴）S **0.51** / 2Y 1.53 / sub **0.86** / TO 0.021；`ts_zscore(totaldomains,252)` 仅 0.04 ⇒ 再次印证「慢速水平字段时序相对化即失效」。

## ★对比实验第三层最终读数（2026-11-14 00:55 全部完成）
| alpha | 族 | 形态 | S | **prod** |
|---|---|---|---:|---:|
| RReLlvG0 | 残差反转 | gz w22 | 1.81 | **0.8746** |
| j2aQa1qo | 残差反转 | gz 短窗 + 跨波设置 | 2.14 | **0.8496** |
| omaeEoZE | 残差反转 | V5 冠军 gz w22 | 1.36 | **0.8077** |
| **XgaEamR5** | 残差反转 | w10 | 1.65 | **0.8112** |
| aka39XYx | techindi | tm_19 r5 | 2.99 | **0.929** |
**⇒ 第三层结论（用户质询的对比实验已完成）**：同一残差族内 **4 个变体覆盖窗口(10/22)、形态(gz)、设置档，prod 全部落在 0.808-0.875，极差仅 0.067**。结合第一层「族内相关 0.80-0.95」与第二层「self 0.608 / 篮内 0.29 vs prod 0.87」，归因三层闭合：**prod 由机制族的持仓空间决定，几何微调最多动 0.07，不可能把 0.81-0.93 拉进 0.70**。⇒ 要过 prod 只有两条路：①换机制族（新持仓空间）；②用「选股腿 + 借券腿」这类结构性组合把持仓推到借券拥挤度维度（篮内 4 颗 0.60-0.63 是唯一 PASS 配方）。





## GEM 渲染（sentiment27，2026-11-14 00:26）→ 55 条入 db
- 前置：`assemble-priors` 成功（快照 2026-11-14 00:23，非 stale）；`workflow_gem` 首次失败（`infer_data_category()` 需显式 `data_category="sentiment"`）；第二次失败因 ideas 文档头部 **Dataset 行写成了「sentiment27（+跨集辅助：sentiment7）」被原样当 dataset_id 解析** ⇒ 修为纯 sentiment27（跨集说明移入正文）。
- 结果：`success=true`，字段池 18 → 绑定 14，预闸 in=79 kept=55（**同骨架换字段变体封顶 12/骨架，丢 24 条**），`[db] expressions/GBR/s2_sentiment27_d1 n=55 status=gem`。
- **质量观察**：渲染结果以 family-mode 模板展开为主（rank/ts_zscore × 22/66/252 × sector/subindustry/industry 的笛卡尔枚举），**未覆盖关键机制概念**——脉冲（ts_max5+ts_ir22）、vector_neut 去规模、DEU 配方移植均缺席。⇒ 这批只作「基线骨架覆盖」，机制核心需手工补批。

**六法结论（→ 交 FE）**：
1. totaldomains：92% 覆盖 / 右偏厚尾 / 季更慢变量 ⇒ **group_rank 保留**（预处理核心），窗口 ≥120，不做翻倍档。
2. kurtosis：**lc/sc 40/488 严重不对称** ⇒ 概念必须改为**对称形式**（group_zscore 或先减自身历史均值再 rank），否则量到的是「大多数公司峰度为负」的结构性空头暴露；覆盖 75% ⇒ 若入波需 ts_backfill。
3. relpopularity1/08：日更 / 92% 覆盖 / 无非零问题 ⇒ 短窗脉冲（5/22）可用，与 DEU 配方一致。


## ★三方补足记录（论坛 + 外部论文，2026-11-14）
**论坛**：
- risk59 帖《融券借贷的隐形成本》（29 赞）：借券费是**双刃信号**——高费=专业空头重仓（利空）但也是**轧空高危区**（利好刺激下暴力反弹）；**GC vs 特殊券**：绝大多数大盘股处于基础费率，只有稀缺券异动 ⇒ 费率信号必须剔 GC 基线；费率+补库天数组合评估白热化。
- **LC97552 DEU 帖《维基百科关注度的"突压"信号在 DEU 市场的因子化尝试》**：DEU/D1/SENTIMENT 金字塔（x1.9）**Sharpe 2.04 / Fitness 1.92 / 17 项硬检查全 PASS**。获胜式 `np7nn69l` = `vector_neut(quantile(ts_ir(ts_mean(ts_max(ts_backfill(vec_avg(snt7_all_languages_views),22),5),5),22),120), ts_backfill(vec_avg(snl27_relpopularity08),22))`。方法论：①**脉冲而非水平**（ts_max5 提突增去周期基线）②**相对强度归一**（ts_ir22：+100 浏览对 50 次/日是巨变、对 10000 次/日是噪声）③**vector_neut 去规模**（剔高人气公司系统偏高）④ts_backfill22 防 CW。文献：Jacobs & Lauber (2025 媒体信息中介)、Chalamandaris (2026「情绪水平不可测量不可交易、只有动态可交易」)。
- ARC2026 热门字段帖：rsk60_crowding 全域 alphaCount 1407（最拥挤）、rsk60_datatime 995、lending_fee_bid_rate 311。

**外部论文**：
- **Drechsler & Drechsler《The Shorting Premium and Asset Pricing Anomalies》(AFA 2016)**：借券费是横截面强预测（CME 便宜-昂贵做空组合月毛 **1.31%**、净 0.78%、四因子 α 1.44%）；**八大异象在低费 80% 股票中消失、在高费股中放大**；机制=集中做空风险的补偿（空侧 → 抬价而非压价）；Miller (1977) 分歧+卖空约束→高估。**GBR 实证相反（|S|≤0.37）⇒ 区域差异，判弱**。
- **Pyun (2024, Economics Letters 241)《The Wikipedia Effect》**：维基浏览量**变化**→正收益；高-低组合有显著 α；电信/耐用消费/高科技行业浏览量增幅最大。**注意与 DEG (2011) 反转结论相反**。
- **Merton (1987) 投资者认知 + NTU《Firm Websites and firm risk》**：网站流量/存在度↑ ⇒ 权益成本、收益波动率、分析师预测分歧**均下降**（信息不对称降低 + 投资者认知扩大）⇒ 支撑 totaldomains 水平概念。

## ★GEM ideas 文档（sentiment27，2026-11-14 已写盘待用户审）
`tracking/GBR/reference/gbr_sentiment27_gem_ideas.md`（6455B）：8 概念 = 数字存在广度(2ops) / 国际触达(2ops) / 人气水平存量(3ops) / 人气突增反转(5ops) / Wikipedia 脉冲(5ops,DEU 移植) / 脉冲去规模(6ops,DEU 完整版) / 品牌聚焦(2ops) / 需求趋势确认(6ops)。多样性：6 种 Expected Exposure × 3 字段族 × 4 时间尺度，全部 ≤6 ops。



## ★prod 阻塞根因（2026-11-14 00:0x 查实）
check_correlation 返回 `holder: "corr:get_production_correlation(1YW5RMOM)"`——**账号级唯一 prod 计算槽被一颗 EUR 遗留 alpha（1YW5RMOM，`group_zscore(quantile(ts_rank(min_similarity_reversal_v_top_pattern,500),driver=gaussian,sigma=2.0),industry)` @SECTOR/dec4，S1.59）的僵尸计算占住**，该任务平台侧永远返回空体（peek 两次也是空体）⇒ 本账号**任何** alpha 的 prod 读取都只能拿到 `correlation_busy` / 空响应。**判别口诀**：prod 长时间 pending 时不要只怀疑自己那颗——看 `holder` 字段是否指向**别的 alpha**。**处置**：等平台侧超时释放；期间不要反复重打（会累加熔断冷却）。


## GB-Z10 派发（insiders 平滑降换手波，sooGbbkT4Uu9HhimsDNgn8，8 臂）
同 Z8 的净买信号 × 平滑算子族：ts_mean 21/66/126（signal）、ts_mean 21/66（director_signal）、ts_decay_linear 22（signal）、ts_sum 66（top_signal）、ts_zscore(ts_mean21,252)（组合式）。设置同 Z8（@SUBINDUSTRY/dec0/nanOFF）。

## GB-Z9 派发与收割（institutions6 机构广度，1lxLbVcoW4lAbov11GoJMglg，8/8 COMPLETE）→ provisional 判弱
**字段体检**：11 个 MATRIX、**cov 全部 1.0**（GBR 唯一全覆盖新面），结构 = 机构**买/卖家数**（breadth）、**买入/卖出美元额**、**买入/卖出股数**、**持股机构数**、机构持股总市值。拥挤集中在 count_institutional_sellers_security（ac 212）/ buyers（181）。
**机制**：Chen-Hong-Stein (2002) 持股广度 → 收益；Bennett-Sias-Stark (2003) 机构交易方向。
| 臂 | alpha | S | F | TO | 2Y | sub |
|---|---|---:|---:|---:|---:|---:|
| 美元净买 zscore252 | mLakWEk5 | **0.44** | 0.15 | 0.076 | 0.52 | 0.26 |
| 买家占比 | wpoVk0gp | 0.24 | 0.07 | 0.056 | -0.63 | -0.09 |
| 股数净买 | vRAVXWgr | -0.22 | -0.07 | 0.029 | 1.02 | -0.02 |
| 买−卖家数(水平) | KPgRMWjg | 0.21 | 0.06 | 0.044 | -1.23 | -0.24 |
| 美元净买(水平) | omae0xOv | -0.13 | -0.03 | 0.029 | 1.06 | 0.18 |
| 买−卖家数 Δ66 | 3q0Wv8WO | -0.11 | -0.02 | 0.103 | -0.61 | -0.32 |
| 机构持股总市值 | pwage9go | -0.09 | -0.02 | 0.021 | 0.95 | 0.19 |
| 持股机构数 | Wjlm2vmj | -0.01 | 0.00 | 0.020 | 1.12 | 0.44 |
**判词**：**全族 |S| ≤ 0.44、符号还乱**（买−卖家数水平 +0.21 但 Δ66 为 -0.11，美元净买水平 -0.13 但 zscore +0.44）⇒ 无稳定方向。TO 0.02-0.10 是季度披露的天然低频，**贴近 LOW_TURNOVER 0.01 地板**，即使有信号也难满足下界。与 EUR 实证（institutions6 六法 0.97 → 中性化后 0.16，衰减 -84%）一致：**该族量到的是单边规模暴露，中性化后归零**。**provisional 判弱，不升级**（未达判死穷尽度）。

## ★★数据集清单再核验 + 未探 unlit 塔尽调筛选波（2026-11-14 09:5x）
**动因**：goal 恢复后复核「容量≈8」结论——重拉 GBR 全量数据集（177 集）与金字塔，逐一核对已探/未探。
**发现 1｜金字塔各塔点亮计数（GBR/D1）**：
- 已点亮（>0）：model 6、pv 4、shortinterest 4、news 3、analyst 3、fundamental 3、other 2
- 未点亮（=0）：institutions、insiders、earnings、sentiment、risk、option、socialmedia、macro、imbalance（9 塔）；D0 全 0（按用户裁定不投入）
**发现 2｜47 个「未探 + vs≥1.5 + ac≥100」数据集全部落在已点亮塔**（model/analyst/fundamental/pv/news/shortinterest）⇒ 按 goal「已点亮塔不纳入」被排除。例：other455(1500f,cov0.94)、analyst_revision_horizons(855f,ac4724)、analyst_consensus(1772f,ac961)、fundamental6(197f,ac4420)、shortinterest3(ac1786)、analyst_earnings_ibes(cov0.997)。
**发现 3｜unlit 塔内仅剩 7 个未探数据集**：insider_trx_matrix(33f,cov0.60)、other78(112f,NLP会议元数据)、other566(112f,TA指标)、other335(10f,combined信号)、search_interest(7f,Google趋势)、stock_cluster_dl(5f,PC特征)、news_sentiment_nlp(23f,标题情绪)——除前三个外全为薄面。
**结论**：容量瓶颈是**结构性**的——高价值未探集恰在已点亮塔（硬约束排除），unlit 塔只剩薄面；与「选股腿独立维度封顶」互为印证。
**尽调筛选波（id=2K5a3j4q94Ad8Kp15gPUwvws，@SUBIND/dec4/nanOFF，8 臂）**：insider_trx_matrix×3（directional_indicator_score cov1.0 / 净买笔数 / usd_primary_signal_value）+ other335×2（combined_all_region_mind/linear）+ other566×3（momentum / linreg_slope / ADX）。validate 通过（8/8 无 unknown）。

## ★unlit 塔尽调筛选波收割（id=2K5a3j4q94Ad8Kp15gPUwvws，8/8 COMPLETE，@SUBIND/dec4/nanOFF）→ **unlit 塔确认穷尽**
| alpha | 数据/字段 | S | F | TO | lc/sc | 判定 |
|---|---|---:|---:|---:|---|---|
| WjlkxMqo | insider_trx_matrix directional_indicator_score | 0 | 0 | 0 | 0/0 | **无数据**（元数据 cov1.0 失真） |
| leaxNdqn | insider_trx_matrix 净买笔数 | 1.01 | 0.47 | 1.386 | **1/1** | **仅 2 只**（与 insider_matrix 同病） |
| GrmV7PAP | insider_trx_matrix usd_primary_signal_value | 0.66 | 0.31 | 0.912 | 0/0 | 无覆盖 |
| 78YO2WbO | other335 combined_all_region_mind | 1.05 | 0.47 | 0.233 | 108/109 | 弱 + 仅 31% 覆盖（fail=[] 是覆盖不足跳过检查的假象） |
| vRA0o8Mz | other335 combined_all_region_linear | 0.97 | 0.42 | 0.230 | 108/108 | 弱 |
| **LLKe2Wan** | other566 momentum_indicator_value | **-1.23** | -0.58 | 0.278 | 404/404 | ★**全宇宙覆盖(808)**但 2Y -0.33（翻号仍不过闸） |
| RReXvMQd | other566 linear_regression_slope_value | -1.01 | -0.43 | 0.279 | 408/407 | 同上，2Y -0.16 |
| 9qlo2Y1r | other566 average_directional_index_value | -0.02 | 0 | 0.339 | 405/413 | 死 |
**判词**：**unlit 塔最后一轮尽调全部弱/无覆盖** —— insider_trx_matrix 与 insider_matrix 同病（元数据 cov 失真，实测 0-2 只）；other335 弱且仅 31% 覆盖；other566 的 TA 动量族**唯一优点=全宇宙覆盖(808/815)**，但 |S| 1.0-1.23 且 2Y 仅 0.16-0.33（远低于 1.58 档）。⇒ **unlit 塔（institutions/insiders/earnings/sentiment/risk/option/socialmedia/macro/imbalance + other）已穷尽**，与「选股腿独立维度封顶 4 族」互为最终印证。剩余未测仅 cov=0 的 f≤66 薄面（other78/other384/other47/other699/stock_cluster_dl 等）。

## ★用户裁定（2026-11-14 10:0x）：已点亮的塔不优先投入
用户原话「已点亮的塔不优先投入」。**规则**：已点亮塔只作**低优先回落项**，不作首选——先把未点亮塔吃透，确已穷尽才回落已点亮塔（**不是绝对禁令**，campaign 交付件本就用了 pv/model/fundamental）。**执行**：unlit 穷尽后，按低优先原则回落已点亮塔筛选。

## 回落波（已点亮塔，低优先）：credit / analyst-revision 新机制筛选（id=46SXEegGv504ber1bXSMMTgD，@SUBIND/dec4/nanOFF，8 臂）
未点亮塔穷尽后按「低优先回落」原则，筛两个**当前篮子完全不存在的新机制**（正交潜力最大）：
- **model28 结构信用模型 ×4**：distance_to_default / pd_percent / leverage / global_rank（Merton DD 机制，cov 0.58-1.0）
- **model216 分析师修正模型 ×4**：estimaterevisioncombinationrank / preferredrevisionscore / globalcombinationscore / recommendationscore（PEAD/修正动量机制，VECTOR→vec_avg，cov 0.56）
validate 8/8 通过；在跑。

## ★回落波收割（id=46SXEegGv504ber1bXSMMTgD，8/8 COMPLETE，@SUBIND/dec4/nanOFF）→ 信用族「正交但弱」，修正族死
| alpha | 字段 | S | F | TO | 2Y | lc/sc | 判定 |
|---|---|---:|---:|---:|---:|---|---|
| **RReXvaqa** | mdl28 credit **leverage** | **1.47** | **1.06** | 0.146 | **1.15** | 225/224 | ★**与篮子 8 颗互相关全 <0.7**（all_below_threshold=true / subset 9）＝**全新正交机制**；但 S/2Y 未达线（warning: LOW_SHARPE 1.47<1.58、LOW_2Y 1.15<1.58） |
| 78YO2X0b | mdl28 credit pd_percent | 1.05 | 0.66 | 0.139 | 0.64 | 219/219 | 2Y 缺口大 |
| YPaZ9kwJ | mdl28 distance_to_default | -1.00 | -0.61 | 0.140 | -0.58 | 217/216 | 翻号 1.00/0.58，弱 |
| d5aqP7gj | mdl28 credit global_rank | 0.34 | 0.16 | 0.030 | — | 222/219 | 弱 |
| **mdl216 修正族 ×4** | estimate/preferred/global/recommendation score | 0.20-0.39 | ≤0.13 | 0.12-0.14 | 弱 | 154-201 | **全死** |
**判词**：① **mdl28 结构信用族＝唯一「正交但弱」的新面**（leverage 1.47/1.06/2Y1.15，449 覆盖、TO 0.146），属「弱腿」档（<2.0）——按 Z16 实证「弱选股腿配借券只能到 ~0.9」且借券腿会**稀释** S ⇒ **直接组合不达线**；② mdl216（分析师修正模型）全死（0.20-0.39）；③ 关键收获：**信用族与篮子全 8 颗互相关 <0.7** ⇒ 新维度确证，其价值在「正交」非「强度」。
**★修正「fail=[] 即过闸」的判读**：RReXvaqa checks.fail=[] 但 **checks.warning 里挂着 LOW_SHARPE/LOW_2Y_SHARPE** ⇒ 未达线的项进 warning 而非 fail，**必读 checks 三列（pass/warning/fail）**。

## ★新机制候选清单（未探高价值集，字段已拉）
- **model36 `star_sr_*`**：StarMine 结构质量分，**cov 1.0** —— profitability/growth/leverage/coverage/liquidity d1；另有 credit_risk_*_score_d1（cov0.60）
- **analyst_factor_signals**：EPS 修正族 —— eps_y1_estimate_change_3mo(cov0.76,ac550) / eps_y1_consensus_value(cov0.73,ac397) / eps_revision_magnitude(cov0.76,ac134) / eps_estimate_trend_slope_1yr
- **model30**：star_new_eps_smart_estimate_fy1(ac74) / star_new_eps_surprise_prediction_fy1(ac124)（StarMine EPS 智能估计/超预期预测）
- **analyst93**：anl93_analyst_accuracy/consistency（VECTOR cov0.59，分析师准确度）
- **model250**：mdl250_maltahc_eq_score(ac268) / malta_eq_score(ac129)（MALTA 模型）

## 回落筛选波②（id=nDwlx6Nq4l7cAujcVQDra9，@SUBIND/dec4/nanOFF，8 臂，在跑）
StarMine star_sr（profitability/growth/leverage，cov1.0）×3 + EPS 修正族 ×5（eps_y1_estimate_change_3mo / eps_revision_magnitude / eps_y1_consensus_value / star_new_eps_smart_estimate_fy1 / star_new_eps_surprise_prediction_fy1）。

## ★信用族 prod 实测（2026-11-14 10:12）→ 纯选股腿 prod 0.7619 FAIL
`RReXvaqa`（mdl28 credit leverage，纯选股腿无借券）**prod = 0.7619** ✗。
⇒ **确认模式**：纯选股腿 prod ≈ 0.76（与本篮子互相关 <0.7 但**生产池拥挤**）；**只有配对借券腿才能把 prod 压到 ~0.60**（篮内 8 颗实证 0.586-0.630）。
⇒ 新机制要交付，必须是**强选股腿（S≥~1.8，足以承受借券腿稀释）**；弱腿（1.0-1.5）无论纯度都过不了（pure→prod 死；+borrow→S 稀释死）。

## ★回落筛选波②收割（nDwlx6Nq4l7cAujcVQDra9，8/8 COMPLETE，@SUBIND/dec4/nanOFF）→ 全弱
star_sr_profitability_d1 0.67/2Y0.35 · growth 0.23/2Y-0.61 · leverage -0.26 · eps_y1_estimate_change_3mo 0.32 · eps_revision_magnitude 0.09 · eps_y1_consensus_value 0.86 · **star_new_eps_smart_estimate_fy1 1.00/2Y0.70** · surprise_prediction 0.38。
**判词**：StarMine star_sr 质量分与 EPS 修正族**全弱（≤1.00）**；**且 star_sr_* 元数据 cov=1.0 实测 lc/sc 仅 186-207（53-59%）** ⇒ 又一次「元数据 cov 不可信」。

## ★★★ 容量 ≈8 的三重结构根因（2026-11-14 10:1x）
1. **≤5 组腿预算已用 4/5**：goal「禁止 PV/MODEL/OTHER 内部及相互两两组腿，但允许与其它 category 组腿，总计 ≤5」。已交付 8 颗中 **4 颗属此类**（omEdka3v/xAvMdaOl=OTHER+shortinterest、xAvMjnam=PV+shortinterest、1YWvNaXk=MODEL+shortinterest）⇒ **只剩 1 个名额**。
2. **2Y 有效线 = 2.02**：纯腿件 2Y 普遍 1.35-2.01（leaxEAv2 纯 techindi **2.01**、2r5E9AwN 纯 star 1.37、QP0eOv3p 纯估值 1.35）⇒ 纯腿几乎全卡 2Y；而**借券腿把 2Y 从 2.01 抬到 2.58**（xAvMdaOl vs leaxEAv2）⇒ 借券腿「降 prod + 抬 2Y」双重功能、不可替代但受名额限制。
3. **纯腿 prod ≈0.76**（RReXvaqa 实测 0.7619）：与本篮子正交 ≠ 与生产池不拥挤。
**⇒ 三重根因：≤5 组腿名额 + 2Y 2.02 档 + 机制族拥挤度。** 更根本的是：**GBR TOP700 池中「强（S≥2、2Y≥2）且正交」的选股腿族只有 5-6 个**，已全部用尽。

## 未点亮塔残余尽调（2026-11-14 10:1x）→ 确认为空壳
other 塔残余 8 个最大未探集实测字段：other78（conference/entity 元数据 SYMBOL/VECTOR）、other384（会议出席/名称匹配分）、other546（网络相似度）、other169（CDS 债券价差，cov0）、other315（利率互换名义额）、other425（关联方日价格）——**全为 NLP/元数据/无覆盖空壳**；other47（digital search marketing，cov0.43-0.61）与 other296（电话会情绪 prob_pos ac13）为仅有的 cov>0 边际件。⇒ **unlit 塔确认穷尽（字段级证据）**。






