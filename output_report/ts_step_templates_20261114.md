# `ts_step(1)` 模板调研与回测（2026-11-14 19:1x GMT+8）

> **一句话**：`ts_step(1)` 的正确用法不是「趋势斜率」，而是**当时间轴做去趋势残差**。论坛 268 赞的斜率模板在本账号/本时段几乎无预测力（|S| ≤ 0.08）；把同一算子改到 `rettype=0` 做去趋势均值回复，IND 能打到 **S 1.76 / F 1.35**，但被 `robust universe 0.85` 与 `2Y 1.14` 双卡，仍不可提交。

**共回测 21 条，零提交、零配额消耗。**

## 0 模板溯源（三源独立印证）

| 来源 | 内容 | 对本轮的作用 |
|---|---|---|
| **论坛 268 赞**《Alpha模版·60天点亮60个塔》(LR93609, 295 atom/64 塔) | 一元模板 index 0：`ts_regression(ts_zscore({a}, 500), ts_step(1), 500, rettype=2)` = 斜率；作者注 252 对 daily、500 对季度 | 本轮 A 族原式 |
| **论坛 24 赞**《ts_regression 算子探索》(MY82844) | 钉死 rettype 全表 + 转述原作者警告「这个模版很多人都用了，overfitting 风险也比较高，慎用」 | rettype 语义据此处 |
| **论文 SSRN 6731259**《Trading the Chart: Trend Slope, Trend Strength, and Retail Extrapolation》 | 分解为 trend slope 与 trend strength（R² of cumulative returns on time），先按 strength 排序、direction within；long smooth uptrends / short noisy downtrends，7.9% 年化 (t=3.44) | B 族 TM=β×R² |
| **论文 arXiv 2412.12350** | **Trended Momentum TM = β̂ × R²**（12 个月日价格回归，排除最近一月） | B 族同构 |
| **AQR《Trends Everywhere》** | 1–12 月趋势持续、>12 月反转 | 窗口选择依据 |

`rettype` 官方语义（`GET /operators/ts_regression`，**不在 get_operators 摘要里**）：

| rettype | 官方 return | 本轮用法 |
|---:|---|---|
| 0 | Error Term | **C 族：去趋势残差（DPO 等价）** |
| 2 | slope (β) | A 族：趋势速度 |
| 6 | R-Square | B 族：趋势清晰度 |
| 8 | Standard Error of β | D 族：β/SE(β) = 趋势 t 值 |

## 1 第一轮：13 条（5 族 × 4 载体）

设置：USA/TOP3000 或 GBR/TOP700，D1，decay 4，SUBINDUSTRY，trunc 0.08，2014–2023。

| # | alpha | 族 | 含义 | S | F | TO | 2Y | sub | CW | FAIL |
|---:|---|---|---|---:|---:|---:|---:|---:|:---:|---|
| 1 | `zqdXVKnG` | A1 | 价格趋势斜率 252（论坛268赞原式） | -0.05 | -0.01 | +0.0257 | -0.77 | +0.05 | PASS | LOW_SHARPE,LOW_FITNESS,LOW_2Y_SHARPE |
| 2 | `QP0m8ZRM` | A2 | 量能趋势斜率 252 | +0.13 | +0.02 | +0.0995 | -0.34 | +0.15 | PASS | LOW_SHARPE,LOW_FITNESS,LOW_2Y_SHARPE |
| 3 | `xAvXZO7w` | A3 | 营收趋势斜率 500 | +0.57 | +0.24 | +0.0163 | +0.34 | +0.40 | PASS | LOW_SHARPE,LOW_FITNESS,LOW_2Y_SHARPE |
| 4 | `6XMgkm6p` | A4 | 分析师EBT趋势斜率 500 | +0.45 | +0.18 | +0.0163 | +0.57 | +0.44 | PASS | LOW_SHARPE,LOW_FITNESS,LOW_2Y_SHARPE |
| 5 | `YPaXeL3l` | A5 | 营业利润趋势斜率 500 | +0.15 | +0.03 | +0.0173 | -0.29 | +0.22 | PASS | LOW_SHARPE,LOW_FITNESS,LOW_2Y_SHARPE |
| 6 | `qM7eR9aK` | B1 | 价格TM=β×R² | -0.08 | -0.02 | +0.0251 | -0.93 | +0.07 | PASS | LOW_SHARPE,LOW_FITNESS,LOW_2Y_SHARPE |
| 7 | `xAvXZOLw` | B3 | 分析师TM=β×R² | +0.49 | +0.20 | +0.0164 | +0.66 | +0.52 | PASS | LOW_SHARPE,LOW_FITNESS,LOW_2Y_SHARPE |
| 8 | `KPgx1loE` | D1 | 价格趋势t值β/SE(β) | -0.07 | -0.01 | +0.0239 | -1.00 | +0.13 | PASS | LOW_SHARPE,LOW_FITNESS,LOW_2Y_SHARPE |
| 9 | `N1PkZxdL` | D2 | 分析师趋势t值β/SE(β) | +0.53 | +0.22 | +0.0164 | +0.72 | +0.62 | PASS | LOW_SHARPE,LOW_FITNESS,LOW_2Y_SHARPE |
| 10 | `78Ygp7p8` | E1 | 趋势线性度corr(price,t) | -0.08 | -0.01 | +0.0239 | -0.97 | +0.11 | PASS | LOW_SHARPE,LOW_FITNESS,LOW_2Y_SHARPE |
| 11 | `e7aejkEp` | C1 | 价格去趋势残差252（DPO） | +1.02 | +0.66 | +0.1081 | +0.98 | +0.52 | PASS | **无** |
| 12 | `npawExrz` | C2 | 价格去趋势残差63 | +0.67 | +0.26 | +0.2042 | -0.38 | +0.31 | PASS | LOW_SHARPE,LOW_FITNESS,LOW_SUB_UNIVERSE_SHARPE,LOW_2Y_SHARPE |
| 13 | `78Ygp7l1` | C3 | 分析师去趋势残差500 | +0.39 | +0.14 | +0.0427 | -0.55 | -0.26 | PASS | LOW_SHARPE,LOW_FITNESS,LOW_SUB_UNIVERSE_SHARPE,LOW_2Y_SHARPE |

**最关键的一列是 S 的符号**：

| 族 | 载体 | S 区间 | 判读 |
|---|---|---|---|
| A1/B1/D1/E1 | 价格 `close` | **−0.08 ~ −0.05**，2Y −0.77 ~ −1.00 | 价格对时间的线性回归**几乎没有预测力**，且近两年更偏反转 |
| A2/A5 | 量能 / 营业利润 | 0.13 / 0.15 | 弱正 |
| A3/A4/B3/D2 | 营收 / 分析师预期 | **0.45 ~ 0.57**，2Y 0.34 ~ 0.72 | 正但弱，2Y 拖后腿 |
| C1 | 价格去趋势 252 | **+1.02**，零 FAIL | 唯一有生命力 |

⇒ **论坛 268 赞的斜率模板不可复现**：`rank(slope)` 在 USA 上 S = −0.05，即「斜率越高、未来越跌」，反向也只有 +0.05。幅度本身就接近零，不是符号问题。

## 2 第二轮：C 族跨区 × 窗口（8 条）

| alpha | 区 | 含义 | S | F | TO | 2Y | sub | robust | FAIL |
|---|---|---|---:|---:|---:|---:|---:|---:|---|
| `KPgx11jE` | GBR | 去趋势残差 500 日 | +1.20 | +0.81 | +0.0849 | +1.05 | +0.57 | — | **无** |
| `qM7eRRqK` | GBR | 去趋势残差 126 日 | +1.16 | +0.69 | +0.1462 | +1.01 | +0.82 | — | **无** |
| `e7aejkEp` | GBR | 去趋势残差 252 日（第一轮基线） | +1.02 | +0.66 | +0.1081 | +0.98 | +0.52 | — | **无** |
| `N1PkZZvL` | GBR | 去趋势用 returns 作载体 | +1.19 | +0.34 | +0.8433 | +0.53 | +0.95 | — | LOW_FITNESS,HIGH_TURNOVER,LOW_2Y_SHARPE |
| `N1PkZGQE` | EUR | 去趋势残差 252（跨区） | +1.39 | +0.94 | +0.1030 | +0.50 | +0.58 | — | LOW_FITNESS,LOW_2Y_SHARPE,LOW_SUB_UNIVERSE_SHARPE |
| `qM7eQdbE` | USA | 去趋势残差 252（跨区） | +0.60 | +0.30 | +0.0952 | +0.45 | +0.28 | — | LOW_SHARPE,LOW_FITNESS,LOW_2Y_SHARPE |
| `gJa7neNv` | IND | 去趋势残差 252（跨区） | +1.55 | +1.30 | +0.1106 | +1.69 | +0.82 | +0.51 | LOW_ROBUST_UNIVERSE_SHARPE |
| `2r5q1Kex` | IND | 去趋势残差 252 + STATISTICAL 中性化 | +1.76 | +1.35 | +0.1346 | +1.14 | — | +0.85 | LOW_ROBUST_UNIVERSE_SHARPE |
| `2r5q1VK5` | IND | 去趋势残差 252 + truncation 0.04 | +1.55 | +1.30 | +0.1106 | — | — | +0.51 | LOW_ROBUST_UNIVERSE_SHARPE |

### 2.1 跨区：有效性 ∝ 宇宙小市值程度

同一条 `rank(-ts_regression(ts_zscore(close,252), ts_step(1),252, rettype=0))`：

| 区 / 宇宙 | S | F | 判读 |
|---|---:|---:|---|
| USA / TOP3000 | **0.60** | 0.30 | 大盘失效 |
| GBR / TOP700 | 1.02 → 1.20 | 0.66 → 0.81 | 中等 |
| EUR / TOP2500 | **1.39** | 0.94 | 较强，但 2Y 0.50 崩 |
| **IND / TOP500** | **1.55** | **1.30** | 最强，2Y 1.69 也过 |

**结论**：长期去趋势均值回复在小市值/低流动性宇宙更有效。这是机制层面的规律，不是 GBR 的区域特性。

### 2.2 窗口：500 日最优，126 与 252 接近，越短越差

| GBR 窗口 | S | F | 2Y | sub |
|---|---:|---:|---:|---:|
| 126 | 1.16 | 0.69 | 1.01 | 0.82 |
| 252 | 1.02 | 0.66 | 0.98 | 0.52 |
| **500** | **1.20** | **0.81** | **1.05** | 0.57 |

### 2.3 载体：必须用价格水平，不能用 returns

`C1-ret` 用 `ts_zscore(returns, 252)` 作载体：**TO 0.8433（84% 换手）**、F 0.34、多条 FAIL。原因是 returns 本身是零均值高噪声序列，它的 z 分数在 0 附近反复穿越，去趋势残差的符号也随之剧烈翻转。**去趋势必须建立在有水平漂移的变量上**（价格、财务存量），不能建立在 flow 变量上。

## 3 IND 优化：唯一接近 RA 的一颗

`C1-IND`（`gJa7neNv`）S 1.55 / F 1.30 / 2Y 1.69 / sub 0.82 / CW PASS，**唯一 FAIL 是 `LOW_ROBUST_UNIVERSE_SHARPE` 0.51**。IND 只有 TOP500 一个 universe 档位，无法换宇宙，只能降持仓集中度。两个杠杆实测：

| 变体 | S | F | TO | robust | 结论 |
|---|---:|---:|---:|---:|---|
| 基线 SUBINDUSTRY | 1.55 | 1.30 | 0.1106 | **0.51** | 原版 |
| truncation 0.04 | 1.55 | 1.30 | 0.1106 | **0.51** | **逐位相同 ⇒ 无效** |
| **STATISTICAL** | **1.76** | **1.35** | 0.1346 | **0.85** | **S +0.21、robust +0.34** |

**`STATISTICAL` 是本轮唯一有效的 robust universe 杠杆**：把纯风险因子中性化后，持仓从「行业内相对偏移」变成「风险因子暴露对齐」，宽宇宙重测时衰减明显减小（0.51 → 0.85）。但仍差 0.15 未过 1.0。

`2r5q1Kex` 的完整状态：

- **PASS**：LOW_SHARPE 1.76、LOW_FITNESS 1.35、LOW_TURNOVER、HIGH_TURNOVER、CONCENTRATED_WEIGHT、LOW_SUB_UNIVERSE_SHARPE、MATCHES_PYRAMID
- **FAIL**：`LOW_ROBUST_UNIVERSE_SHARPE` 0.85 < 1.0
- **WARNING**：`LOW_2Y_SHARPE` **1.14 < 1.58**、`CLUSTER_TEST` 0.79、`REVERSION_COMPONENT`
- 按项目铁律「2Y 类 WARNING 视同 FAIL」⇒ **2Y 1.14 实质不达标**，两颗杠杆叠加仍不可提交。

## 4 结构性发现：`REVERSION_COMPONENT` 对整族普适触发

**21 条里 21 条全带** `REVERSION_COMPONENT` WARNING，包括：

- 纯基本面载体 `ts_regression(ts_zscore(revenue, 500), ts_step(1), 500)` —— 完全不碰价格；
- 纯分析师载体 `est_12m_ebt_mean`；
- 反向的「趋势」模板与正向的「去趋势」模板。

原文：`Alpha expression includes a reversion component so we may not accept these alphas in the future, try working on different alpha ideas.`

判读：平台的反转检测**不是**按字段，而是按「对时间回归」这一结构在日频持仓上的表现——长窗口回归产生缓慢变化的持仓，其收益与短期反转因子天然相关。这是 WARNING 不是 ERROR（本轮 21 条全部有完整指标），但它是**结构性提交风险**：该族即便调到 S 1.76，也带着「未来可能不被接受」的标记。

## 5 可复用结论（4 条）

1. **`ts_step(1)` 的价值在 `rettype=0`（去趋势残差），不在 `rettype=2`（斜率）。** 斜率族在 USA 的 |S| ≤ 0.08，等于无信号；同一算子的残差族在 IND 能到 1.76。选 rettype 比选窗口重要一个数量级。
2. **去趋势必须建在有水平漂移的变量上。** 价格 z 分数 ⇒ 可用；returns z 分数 ⇒ TO 84% 报废。判据：载体是否零均值。
3. **长期均值回复的有效性 ∝ 宇宙小市值程度**（USA 0.60 / GBR 1.20 / EUR 1.39 / IND 1.55）。要挖这类信号，直接去 IND / GBR / KOR 这类小宇宙，不要在 USA 上磨。
4. **`STATISTICAL` 中性化是 `robust universe sharpe` 的专用杠杆**（0.51→0.85，S 同时 +0.21）；`truncation` 对它完全无效（逐位相同）。

## 6 边界与纪律

- **零提交**：21 条全部 `UNSUBMITTED`，未调用任何 submit 接口，未消耗 REGULAR 配额。
- **未做 prod/self 判定**：本轮无一条达到「值得进闸」的门槛（最强件仍有 2 项实质 FAIL），按纪律不浪费平台相关性槽。
- **已过发批五闸**：op_arity / 算子存在性（REGULAR scope）/ 字段存在性 / 单位闸 / ops ≤ 8，签核写入 `results/op_coverage_signoff.jsonl`。
- **`2Y` 口径**：`LOW_2Y_SHARPE` 为 WARNING 时按项目铁律视同 FAIL，因此 `2r5q1Kex` 的 1.14 判为不达标，不当成「只差 robust 一项」。
- **可继续的方向**（若要救 IND 那颗）：robust universe 0.85 差 0.15，剩余杠杆只有 `SLOW_AND_FAST` 中性化、或改用 `group_neutralize` 二次分散；但 `REVERSION_COMPONENT` + 2Y 1.14 两条已构成实质障碍，建议**换机制而非继续磨**。
