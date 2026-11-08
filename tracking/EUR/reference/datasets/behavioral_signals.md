# behavioral_signals · EUR / TOPCS1600 / D1 字段画像

> 类型 VECTOR · 7 字段 · cov **0.557** · category = **model**（×1.3）· αC 合计 2
> 采集：2026-11-07 · 行为金融合成因子（Bordalo et al. salience theory / Barberis et al. 2019 风格）

## 0. 字段

| 字段 | 经济含义 | 机制方向 |
|---|---|---|
| `salience_weighted_return_score` | 显著性加权收益 vs 等权——彩票特征 | 高→反转（Bordalo 2012 salience） |
| `extreme_daily_return_indicator` | 极端日收益度（波动归一） | MAX 效应,高→低收益 |
| `price_path_curvature_measure` | 价格路径凸性 | 凸路径→外推者追入→反转 |
| `visual_price_path_shape_score` | 路径形状分（首尾连线以上占比） | 同上 |
| `chronological_return_sequence_correlation` | 收益幅×时序相关（近因偏差） | 高近因权重→反转 |
| `consecutive_return_streak_length` | 连涨连跌长度 | 连涨→博彩偏好→反转 |
| `total_equity_market_value_usd` | 市值（分组轴用） | — |

## 1. 机制假设

全部因子都是「彩票/外推偏好」族——EUR 文献（IVOL 谜题同源）预期**反向**：高 salience/极端/凸性 → 后续低收益。骨架用本战役结构最优的 `ts_rank` 自身基线（对合成因子友好,无单位问题）+ reverse。

## 2. 实测

**第一批 reverse 自身基线（已终态,multisim `xO9pT5wc4L6b6x8Troy8Nz`,FAST/decay15）——反向全部负读数 = 正向动量成立但强度不足**：

| 字段 | alpha id | reverse S | 含义 |
|---|---|---|---|
| salience | `gJegQapv` | −0.48 | 高显著性→继续跑赢（动量非反转） |
| extreme | `leA58aXl` | −0.35 | 同上 |
| curvature | `2rAXO5d5` | −0.40 | 凸路径→继续 |
| streak | `vR1pkAgb` | **−0.74** | 连涨→继续涨 |
| recency | `3qok90WZ` | −0.73 | 近因偏差→延续 |

**第二批正向/截面栈（已终态,multisim `4k5XNJbtZ4WT9YCGbQtY0n`）**：

| 变体 | alpha id | S | F | 2Y | sub | robust |
|---|---|---|---|---|---|---|
| streak 正向 66/252 | `rKRNOW1j` | **0.74** | 0.29 | 1.01 | 0.48 | 0.58 |
| salience 正向 | `QPvNbQ1r` | 0.48 | 0.15 | −0.38 | 0.38 | 0.51 |
| salience 截面 zscore 栈 | `58EAzvZ5` | −0.22 | | | | |
| streak reverse 截面栈 | `pwdMR7wq` | −0.13 | | | | |

**归因**：① 全族反向证伪——**EUR 的行为金融合成因子不呈现彩票反转,而呈现「动量延续」**（连涨→继续涨 0.74）,与 KOR 的 IVOL 反转机制相反;截面积分（group_zscore 栈）反而把信号磨没（−0.22）——**该族信息在自身时序基线里,不在截面相对位置**（与 news18 密度模板同构,与 insider 强度族相反——「合成因子吃时序、原始流量吃截面」假设成立）。② 正向最高 0.74,距闸 2.1×,**9 探针无达标候选,快判死归档**。model 塔本集关闭。
