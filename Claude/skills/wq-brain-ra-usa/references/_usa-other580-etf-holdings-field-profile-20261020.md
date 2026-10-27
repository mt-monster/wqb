# other580（Standardized Daily ETF Holdings）字段画像与批 1 预注册（USA / D1 / TOP3000，2026-10-20）

> 用途：board_gov_stats（insiders 塔）被封存后，交付 7→10 的第 8–10 颗主线的候选池第一名。
> 选它的三条理由：① **未点亮塔**（USA/D1 已点亮只有 model=4 / analyst=5 / earnings=1）；
> ② **低拥挤**（数据集 aC 200，绝大多数字段 aC 0–7）；③ **机制与已交付的 7 颗全 analyst 族正交**——
> 前 7 颗全是「分析师预期/修正」，本集是「ETF 申赎流量驱动的需求压力」，数据产生方完全不同。
> 本档按「字段画像 → 适用模板 → 回测结果及指标」组织；**本档不含提交动作，任何提交都须用户明确确认。**

---

## 0. 数据集坐标（`get_datasets` / `get_datafields` 2026-10-20 实测）

| 项 | 值 | 备注 |
|---|---|---|
| dataset id | `other580` | "Standardized Daily ETF Holdings" |
| 类别 / 塔位 | `other` / **未点亮** | 非 model/analyst/earnings |
| 字段数 | 403（`get_datafields` 翻页返回 **300**，达到接口单次上限） | 全部 **MATRIX** |
| 覆盖率 | 计数族 **1.000**；变化/位置族 **0.8876–0.9154** | 覆盖高且稳定，`ts_backfill 252` 足够 |
| 数据集 alphaCount | **200** | 低拥挤（对比 analyst_consensus 数万、pv103 9679） |
| 字段 alphaCount | **0–45**；仅 6 个字段 ≥10 | 「变化/计数」子域几乎空白 |
| valueScore / 乘数 | **5** / 1.4 | 平台质量评分最高档 |
| 更新频率 | **日频**（字段名含 5d / 20d / 60d 滚动窗，另有 predicted 族） | D1 下无需特殊处理 |
| 描述 | 「changes in fund constituents over time … holding deltas」 | ETF 持仓份额（shares held）的标准化聚合 |

**数据集的经济角色**：不是「ETF 持有了什么」的静态快照，而是**每只 ETF 对某股票的持仓份额变化**
（= 申赎/再平衡产生的交易流量）在截面上聚合后的统计量。因此它的 alpha 来源不是估值，而是
**flow-induced demand pressure**（ETF 申购 → 成分股被动买入 → 短期价格压力）。

---

## 1. 字段画像（七族 + 两个高拥挤例外）

### 1.1 流量水平族（signed，本集最直接的方向信号）

| 字段 | 含义 | cov | aC | uC |
|---|---|---:|---:|---:|
| `percent_change_average_5d` | 各 ETF 5 日持股**百分比变化**的等权均值（有符号） | 0.9139 | 3 | 1 |
| `percent_change_average` | 同上，20 日窗 | 0.9082 | 2 | 2 |
| `change_average_2` | 各 ETF 5 日 **绝对**变化的均值（无量纲方向） | 0.9139 | 0 | 0 |
| `change_average` | 20 日绝对变化均值 | 0.9082 | 1 | 1 |
| `change_average_60d` | 60 日绝对变化均值 | 0.8948 | 0 | 0 |
| `change_sum_5d` | 5 日变化之和（跨 ETF，**含符号**） | 0.9139 | 1 | 1 |

> 判读：`percent_change_*` 是**唯一自带方向的流量字段**；`change_average*` 是幅度（churn），
> 需要与负向/正向分量相除才能变方向。`change_average_60d` 的 aC=0 ⇒ 60 日窗基本无人挖。

### 1.2 流量方向分解族（正/负分量的均值与计数）

| 字段 | 含义 | cov | aC | uC |
|---|---|---:|---:|---:|
| `positive_change_average` | 仅「增持 ETF」的 20 日绝对变化均值 | 0.9043 | 1 | 1 |
| `negative_change_average` | 仅「减持 ETF」的 20 日绝对变化均值 | 0.9029 | 0 | 0 |
| `positive_change_average_5d` | 同上，5 日窗 | 0.9096 | 0 | 0 |
| `negative_change_average_5d` | 同上，5 日窗 | 0.9089 | 0 | 0 |
| `positive_change_count` | 增持的 ETF **只数**（20 日） | 1.000 | 6 | 4 |
| `negative_change_count` | 减持的 ETF **只数**（20 日） | 1.000 | 7 | 6 |
| `change_count` | 有效变化的总 ETF 只数（20 日） | 1.000 | 5 | 4 |
| `change_count_5d` | 同上，5 日窗 | 1.000 | 2 | 2 |
| `negative_percent_change_count` | 出现**负百分比变化**的 ETF 只数 | 1.000 | 4 | 3 |

> 判读：这一族是本集的**结构性优势**——「广度」（多少只 ETF 在买）与「幅度」（平均买了多少）
> 可以分离，得到两个正交机制：**breadth vs magnitude**。计数族 cov 全 1.0，没有覆盖缺口。

### 1.3 流量离散/集中族（herding 与 fragility）

| 字段 | 含义 | cov | aC | uC |
|---|---|---:|---:|---:|
| `change_variance` | 各 ETF 5 日绝对变化的**方差** | 0.9018 | 0 | 0 |
| `change_skewness` | 持仓变化的**偏度**（默认期） | 0.8965 | 0 | 0 |
| `change_skewness_2` | 持仓变化偏度（5 日窗） | 0.9010 | 0 | 0 |
| `change_cubed_sum_5d` | 5 日变化的**立方和**（三阶矩） | 0.9139 | 0 | 0 |
| `change_cubed_sum` / `_60d` | 20 日 / 60 日立方和 | 0.8948–0.9082 | 0 | 0 |
| `negative_change_cubed_sum_5d` | 仅负向变化的立方和 | 0.9089 | 1 | 1 |

> 判读：**全部 aC=0**，是本集最冷的一组。立方和 / 方差可组合出「少数大 ETF 主导变化」
> ＝流量集中度（herding），与「多数小 ETF 同步变化」＝广泛再平衡，经济含义相反。

### 1.4 持仓位置族（水平量，偏风格）

| 字段 | 含义 | cov | aC | uC |
|---|---|---:|---:|---:|
| `oth580_mv_mean` | 各 ETF 对股票 1 日绝对变化的等权均值 | 0.9153 | **45** | 19 |
| `oth580_mv_sisum` | 股票在 ETF 组合中的**总市值持仓** | 0.9153 | 20 | 20 |
| `oth580_mv_cusum` | 持仓市值的三阶累积和 | 0.9153 | 17 | 14 |
| `oth580_mv_sqsum` | 持仓市值平方和 | 0.9153 | 5 | 5 |
| `oth580_mv_skew` | 持仓市值在 ETF 间的**偏度** | 0.9005 | 8 | 7 |
| `oth580_tnc_vm` | 股票在 ETF 内的**价值加权平均换手率** | 1.000 | **25** | 17 |
| `oth580_rav_vm` | 价值加权的**风险调整后价值**均值 | 0.9029 | 10 | 10 |

> 判读：`mv_mean`(aC45)/`tnc_vm`(25)/`mv_sisum`(20) 是本集**被挖得最多**的三个字段——它们大概率是
> size/流动性风格的代理（预期 risk-neut 低）。保留一条作对照（M07），不作为主攻方向。

### 1.5 预测/意外族

| 字段 | 含义 | cov | aC | uC |
|---|---|---:|---:|---:|
| `change_average_predicted` | 预测的平均持仓变化（供应商模型） | 0.9154 | 3 | 3 |
| `average_predicted_holding_change_20d` | 预测的 20 日平均持仓变化 | 0.9122 | 3 | 3 |
| `change_average_predicted` 同族 `change_log_weighted_average_predicted` | 对数权重版预测 | 0.9131 | 0 | 0 |

> 判读：有了「预测」，就能构造 **实际 − 预测 = 意外再平衡**（M05）。这是本集唯一能分离
> 「可预期的指数再平衡」与「意外流量」的机制，且 aC 仅 3。

### 1.6 权重加权变体（log 权重 / sqrt 权重）

`change_log_weighted_average*`（aC 0–2）、`change_sqrt_weighted_*`（aC 0–1）等 **99 个** log/sqrt 加权字段：
对持仓规模做 log/sqrt 变换后再聚合，等价于**降低大 ETF 的支配力**。它们是 1.2–1.3 族的「抗集中度版本」，
不是独立机制，**留作后续抗 herding 的替换口径**，第 1 批不占探针位。

### 1.7 高拥挤例外（不建议作主信号）

`oth580_mv_mean`(aC45)、`oth580_tnc_vm`(25)、`oth580_mv_sisum`(20)、`oth580_mv_cusum`(17) 四个
位置/换手字段占全数据集中被使用量的绝大头。**经验：aC 高的字段在 USA/D1 通常是风格代理**，
第 1 批只让 `tnc_vm` 占 1 个探针位作对照。

---

## 2. 适用模板（M01–M12，机制不封顶 8，批 1 只取前 8 个）

> 壳层统一用通用壳 `quantile(group_rank(ts_backfill(winsorize(SIG, std=4), 252), industry))`。
> ATOM 合规：唯一非豁免字段来自 `other580`；`industry` 是 6 个豁免分组字段之一。
> 方向按经济先验写死；**每条主候选的反号变体在同批内成对出现**（M01+ / M02− 即一对）。

| # | 机制 | 字段 | 经济先验与方向 | 预期风险 |
|---|---|---|---|---|
| **M01** | **流量动量（5d）** | `percent_change_average_5d` | ETF 净申购 → 被动买入 → 价格压力延续（Ben-David 2018）⇒ **正向** | 短窗噪声；TO 可能高 |
| **M02** | **流量反转（20d）** | `percent_change_average` | 月度累积流量已过度定价 → 回落（Da & Shive 2018）⇒ **反向** | 与 M01 同族异窗，self-corr 可能偏高 |
| **M03** | **累积广度** | `(positive_change_count − negative_change_count)/change_count` | 增持 ETF 只数占比 = 广泛需求；广度比幅度更抗单只大 ETF 噪声 ⇒ **正向** | 计数族 cov 1.0，最干净 |
| **M04** | **流量不对称（幅度）** | `positive_change_average / (positive_change_average + negative_change_average)` | 正向流量占**总量**的比例 ∈[0,1]，无量纲；与 M03 的「只数」正交 ⇒ **正向** | 分母为 0 → NaN（nanHandling ON） |
| **M05** | **意外再平衡** | `change_average − change_average_predicted` | 实际 churn 超出预测 = 未被定价的再平衡冲击 → 不确定性折价 ⇒ **反向** | 预测族仅 3 个使用者，先验未知 |
| **M06** | **流量离散** | `change_variance` | 各 ETF 变化方差大 = 流量集中于少数 ETF = fragility ⇒ **反向** | aC=0，纯冷门 |
| **M07** | **ETF 内换手强度** | `oth580_tnc_vm` | 股票在 ETF 组合内被高频交易 → 关注度/流动性溢价 ⇒ **正向** | **aC=25，预期是风格代理**，作对照 |
| **M08** | **持仓集中度** | `oth580_mv_skew` | 持仓市值在 ETF 间偏度高 = 单一大 ETF 主导 = 抛售脆弱 ⇒ **反向** | aC=8；可能撞 size |
| M09 | 60 日流量反转 | `percent_change_average` 的 60d 对应字段（如 `change_average_60d` 需配合方向族） | 更长窗 = 更慢的过度反应 | 批 2 备选 |
| M10 | 立方和 herding | `change_cubed_sum_5d / change_variance`（三阶/二阶矩） | 标准化偏度：少数大 ETF 主导 ⇒ 反向 | 批 2 备选（aC=0） |
| M11 | 广度×幅度交互 | M03 × M04（同数据集两字段，**非加信号**，是同一机制的两个测度相乘） | 广度与幅度同时高 = 需求压力最强 | 批 2 备选；需先证 M03/M04 单独有效 |
| M12 | log 权重抗集中 | `change_log_weighted_average_2` | 降低大 ETF 支配后的流量方向 | 批 2 备选 |

---

## 3. 批 1 预注册（8 探针，写死不再改）

**设置**：EQUITY / USA / TOP3000 / D1 / SUBINDUSTRY / decay **5** / trunc **0.08** /
pasteurization ON / unitHandling VERIFY / nanHandling ON / maxTrade OFF / FASTEXPR；
平台缺省区间 2014-01-01 → 2023-12-31。

| # | 表达式 |
|---|---|
| P1 (M01) | `quantile(group_rank(ts_backfill(winsorize(percent_change_average_5d, std=4), 252), industry))` |
| P2 (M02) | `-quantile(group_rank(ts_backfill(winsorize(percent_change_average, std=4), 252), industry))` |
| P3 (M03) | `quantile(group_rank(ts_backfill(winsorize((positive_change_count - negative_change_count) / (change_count + 1), std=4), 252), industry))` |
| P4 (M04) | `quantile(group_rank(ts_backfill(winsorize(positive_change_average / (positive_change_average + negative_change_average), std=4), 252), industry))` | <!-- lint:counterexample: 比率分母，买卖/正负两侧合计，非信号腿相加 -->
| P5 (M05) | `-quantile(group_rank(ts_backfill(winsorize(change_average - change_average_predicted, std=4), 252), industry))` |
| P6 (M06) | `-quantile(group_rank(ts_backfill(winsorize(change_variance, std=4), 252), industry))` |
| P7 (M07) | `quantile(group_rank(ts_backfill(winsorize(oth580_tnc_vm, std=4), 252), industry))` |
| P8 (M08) | `-quantile(group_rank(ts_backfill(winsorize(oth580_mv_skew, std=4), 252), industry))` |

**预注册判据（收割前写死）**：

- 任一 `S≥1.58 / F≥1.0 / 2Y≥1.58 / SUB PASS / TO 1%–70%` 且 `fail=0` ⇒ 立即 `check_correlation(refresh=True)`；
  prod ≥0.75 或踩线失败 ⇒ 决策表 D0-P 判死，**不做同族磨参数**。
- **M01 与 M02 必须互为镜像**（同族异窗）：若两者同号且 |S| 差 <0.2 ⇒ 拆窗无效，合并为单一「流量水平」机制。
- **全部 TO <1%** ⇒ 流量是月度级慢变量，批 2 改 60d 窗 + `ts_mean` 平滑；**TO >40%** ⇒ 流量日频噪声太大，
  批 2 改 `ts_mean(…,5)` 或提高 decay，不再直接换窗。
- **M03 与 M04 的 S 差 <0.15** ⇒ 广度与幅度不独立，批 2 不做 M11 交互。
- **M07（aC=25 对照）S 最高但 risk-neut <0.3** ⇒ 证实「高 aC = 风格代理」，之后本集只信 aC≤10 的字段。
- **全批 |S|<0.8 且 TO 健康** ⇒ 流量无信号，本集判弱（与 pv115 同型），换 `other546`/`other699` 前必须写明归因。
- **SUB 卡死但 S 高** ⇒ 按方法论 §10 先换测量口径（`ts_zscore(…,252)`），不换数据集。

---

## 4. 外部证据（论坛 + 文献）

- **论坛 FF56620**（insider_trx_matrix 复现帖）的可迁移结论：量价类因子在 USA/D1 的 PnL 相关性墙
  **是结构性的**；要迁移「反应不足」这一行为机制，必须找**低拥挤的另类流量数据**承载。ETF 持仓流量
  正属于此类（另类、非价格、低 aC），因此本集优先于再挖一条 PV 族。
- **Ben-David, Franzoni, Moussawi (2018, JF) "Do ETFs Increase Volatility?"**：ETF 持仓越高、流量越大，
  成分股波动与换手越高；机制是**flow-induced trading**（非基本面交易传导到价格）。
  ⇒ 支持 M01（短窗流量＝价格压力）与 M06（流量集中＝波动放大）。
- **Da & Shive (2018, JFE) "Exchange traded funds and asset return correlations"**：ETF 流量带来
  短期价格压力、随后部分反转。⇒ 支持 M02（20d 反向）作为 M01 的对偶。
- **Petajisto (2017) "Inefficiency in the pricing of ETF arbitrage"** / **Israeli, Lee, Sridharan (2017, RFS)**：
  ETF 持仓/流量改变成分股的信息效率与 comovement，效应集中在**高 ETF 持仓**股票。
  ⇒ 支持 M08（持仓集中度）作为条件变量，但预期其单独作信号偏弱。
- **Cheng & Madhavan (2009)**：ETF 申赎是「一篮子」交易，流量方向在截面上可预测短期收益。
- 结论：**本集的四个先验机制（动量 / 反转 / 广度 / 集中度）在文献里都有独立支持**，不是纯数据挖掘。

---

## 5. 回测结果及指标

**批 1**：multisim `bRhlKcpN5bc9a5fPnSenKv`，8/8 COMPLETE（2026-10-20 收割，设置见 §3）。
`SUB 限` 为平台动态值，按 `0.43×S` 估算；`rns` = `risk_neutralized_sharpe`。

| # | alpha | 机制 | S | F | 2Y | SUB | TO | returns | DD | rns | fail |
|---|---|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| P1 | `1YjzdEpW` | M01 5d 流量动量 | 0.43 | 0.11 | 0.11 | 0.22 | 32.83% | 1.96% | 8.99% | 0.21 | 3 |
| P2 | `9qE7r0pe` | M02 20d 流量反转（负号） | −0.58 | −0.22 | −0.47 | −0.55 | 17.84% | −2.53% | 28.99% | 0.16 | 4 |
| P3 | `Vkd3PJ7V` | M03 累积广度 | **0.65** | 0.20 | **0.99** | **0.80 PASS** | 29.83% | 2.77% | 8.62% | 0.33 | 3 |
| P4 | `0mjMEvwk` | M04 流量不对称 | 0.44 | 0.11 | 0.38 | 0.30 | 29.25% | 1.97% | 9.17% | −0.20 | 3 |
| P5 | `akVEnv7x` | M05 意外再平衡（负号） | −0.48 | −0.15 | −0.42 | −0.51 | 20.32% | −2.02% | 21.57% | 0.34 | 4 |
| P6 | `E5VeEJlL` | M06 流量离散（负号） | −0.35 | −0.13 | −0.58 | −0.27 | 14.36% | −2.03% | 30.35% | 0.72 | 4 |
| P7 | `QPY9VX7w` | M07 ETF 换手（aC=25 对照） | 0.63 | **0.38** | 0.97 | 0.37 | 4.49% | **4.60%** | 26.54% | **−0.33** | 3 |
| P8 | `6XAe9OrO` | M08 持仓偏度（负号） | −0.33 | −0.07 | −0.26 | 0.01 | 44.38% | −1.79% | 30.69% | 0.21 | 3 |

P3 另有 `investability_sharpe = 0.98`（全批最高）；P7 为全批最高 returns / fitness。

### 5.1 读数与归因（逐条对照 §3 预注册判据）

1. **预注册止损命中**：全批 `max|S| = 0.65`（P3），8 条无一触及 1.58；TO 4.49%–44.38% 全部落在 1%–70% 健康区。
   ⇒ 「全批 |S|<0.8 且 TO 健康 ⇒ 本集判弱」成立，**本集不进入补批**。
2. **流量水平是真方向、但只有闸线的约 1/3**：P2 = −(20d 流量)，S −0.58 ⇒ 原始 20d 流量 S≈+0.58；
   P1（5d）S +0.43。两窗同号、|S| 差 0.15 < 0.2 ⇒ 按预注册「拆窗无效」，合并为**单一「ETF 流量水平」机制**，
   强度区间 0.43–0.58。与 Ben-David 2018 的 flow-induced trading 方向一致，但在 USA/D1 已被定价到只剩零头。
3. **广度是唯一过 SUB 且 2Y 近 1 的轴**：P3 S0.65 / 2Y0.99 / SUB0.80 PASS / investability 0.98 / DD 8.62%。
   2Y 明显高于全期 S，说明效应集中在近年（指数化加速期），是「近年慢因子」而非全期 alpha — 与 board_gov G2、
   insiders4 薪酬族的 2Y>S 结构同型。**留作 salvage**，不作批 2 起点。
4. **广度与幅度不独立**：P3 0.65 vs P4 0.44，差 0.21 > 0.15（预注册线）⇒ 不合并；但两者都没过 0.8，
   M11（广度×幅度）缺少「两轴各自有效」的前提，**不开发**。
5. **意外再平衡方向与先验相反且弱**：P5 = −(actual − predicted) S −0.48 ⇒ 原始 surprise S≈+0.48。
   实际 churn 高于预测对应**正**收益，与「不确定性折价」先验相反；aC=3 的冷门字段未提供增量。
6. **离散 / 偏度先验被证伪**：P6 −0.35、P8 −0.33 ⇒ 原始 variance / skew 方向为 +0.35 / +0.33，
   强度低于噪音阈值；P6 的 rns 0.72 是「剥离风格后剩下的负号噪声」，returns 与 DD 双负（−2.03% / 30.35%），不可用。
7. **高 aC 对照如预期是风格代理**：P7 `oth580_tnc_vm`（aC=25）returns 4.60% / F0.38 全批最高，但
   **rns = −0.33 < 0.3** ⇒ 收益全部来自风格 beta，按判死口径不可用。本集此后只信 aC≤10 字段。
8. **换手结构**：流量族 TO 14–44%，说明 ETF 持仓流量是**真日频更新**（与 pv103 的 <1% 慢变量结构相反），
   不存在「TO 结构性踩线」问题 — 本集失败纯粹是**方向强度不足**，不是换手/覆盖/权重问题。

### 5.2 决策

- **判弱封存**：`USA-OTHER580-FLOW-WEAK`。8 探针已覆盖 7 个机制族 + 1 个高 aC 对照，字段画像 §1 的
  流量 / 分解 / 离散 / 位置四族各有代表，不存在「漏掉的强字段族」。
- **不开发批 2**：唯一残值轴 P3 距闸线 0.93 Sharpe；用 `ts_zscore` / 换中性化 / 换窗口把它推到 1.58
  属于同族磨参数（D0-P 禁止），且 2Y 0.99 已结构性说明它是近年慢因子。
- **salvage 登记**：P3「ETF 广度」可作未来 COMBO/SUPER 的慢腿（S0.65、SUB PASS、investability 0.98、
  与 pv/analyst 收益源正交），**不用于本轮 ATOM 交付**。
- **向下一数据集切换的理由（按过程约束写明）**：本集 8 条全 `fail≥3`，max|S| 0.65，方向强度与风格纠缠
  已归因清楚；继续在本集投入只会撞 D0-P 与「同族磨参数」红线 ⇒ 转 `other546`（13 VECTOR，需先聚合）
  与 `other699`（16 VECTOR，需构造方向）。

---

## 6. 风险与预判

- **`change_*` 字段的「变化」可能包含指数成分调整（inclusion/exclusion）而非纯申赎**：若某股票被纳入
  某只 ETF，其 shares held 会跳变，产生与价格无关的假信号。M05（实际−预测）是对此的**唯一解药**——
  预测族大概率已把指数事件纳入模型。批 2 若 M05 有效，优先围绕它展开。
- **覆盖率 ~0.90 且计数族为 1.0**：说明所有股票都有 ETF 持仓，**不是稀疏事件集**，无 pv115/insiders4 的
  事件双墙风险。
- **aC=0 的字段既是蓝海也可能是坑**：本集 300 个可见字段中位 aC=0，若 8 个机制全灭，不能只判「字段冷」，
  还要看是否「没人挖过」；判死时必须引 yearly 诊断证明不是数据起始假象。
- **ATOM 合规**：批 1 八条全部只引用 `other580` 字段 + 豁免分组 `industry`，无跨数据集混用。
- **SUB 结构性风险**：ETF 流量在小盘股上更极端（ETF 持仓集中在小盘），可能重演 analyst 族的
  「S 高但 SUB 卡」；若出现，按方法论 §10 用 `ts_zscore` 自波动归一，不改 universe。
