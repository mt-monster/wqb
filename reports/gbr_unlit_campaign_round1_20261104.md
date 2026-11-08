# GBR 未点亮塔战役 —— 第一轮合并归因（W1–W3，32 臂）

日期：2026-11-04 · 区域 GBR / TOP700 / D1 / decay 4 / truncation 0.08 / 2014-01-01–2023-12-31

## 1. 本轮结论一句话

**只有「预测收益类字段 + 无门控双窗 add 骨架 + 换手 20%–27%」这一组合能出闸级 Sharpe；其余三个方向（形态相似度、事件/情绪水平、门控变体）全部为噪声。** 已产生 **1 条全闸 PASS 候选**（`RREbjXre`）。

## 2. 逐臂明细

### W1-A · pattern_scores（PV 塔） · 中性化 SUBINDUSTRY · 8 臂全灭

| alpha | 模板 | S | F | TO | 2Y | sub |
|---|---|---:|---:|---:|---:|---:|
| zq38vxJK | T1 gap_up/gap_down 价差 | −0.30 | −0.08 | 1.56% | 0.37 | −0.04 |
| E56pZjrK | T2 asc_triangle delta+门控 | 0.15 | 0.03 | 9.08% | 0.23 | 0.12 |
| VkxavrYM | T3 对称三角离散度 | 0.04 | 0.00 | 2.00% | −0.37 | −0.29 |
| 0mYXbVK2 | T4 v_reversal/continuation 比值 | −0.01 | −0.00 | 1.79% | −0.25 | 0.08 |
| bl6bYmop | T5 falling/rising wedge 价差 | −0.42 | −0.15 | 7.09% | 0.33 | −0.18 |
| E56pZjgK | T6 gap_up q95 事件门控 | −0.14 | −0.02 | 1.60% | 0.94 | −0.14 |
| rKRO1qJd | T7 desc_triangle ts_quantile | −0.28 | −0.07 | 1.63% | −0.54 | −0.36 |
| 0mYXbVe2 | T8 gap_up max 长窗 | −0.01 | −0.00 | 1.61% | −0.88 | 0.07 |

8 条 `MATCHES_PYRAMID` 全 PASS ⇒ 塔位无误，是信号本身无效。

### W1-B · other567 / institutions25 / insiders12 · SUBINDUSTRY · 8 臂全灭（最好 S 0.40）

| alpha | 数据集 | 模板 | S | F | TO | 2Y |
|---|---|---|---:|---:|---:|---:|
| WjObjmkQ | other567 | T3 利差动量 | 0.40 | 0.14 | 6.44% | 0.52 |
| A1VN1ddQ | other567 | T2 outlook−culture 利差 | 0.17 | 0.04 | 4.76% | 0.47 |
| Xg9bgE6m | institutions25 | T2 仓位变动 | 0.14 | 0.03 | 6.35% | 0.66 |
| 78LN8VVQ | other567 | T1 overall 门控 | 0.10 | 0.02 | 2.30% | −0.13 |
| 88Rj8q1V | insiders12 | T2 持股比例变动 | −0.13 | −0.03 | 3.48% | 0.23 |
| LLMNLxA1 | institutions25 | T1 做空情绪门控 | −0.18 | −0.04 | 3.30% | −0.70 |
| leAveZZe | insiders12 | T3 买入强度比值 | −0.24 | −0.08 | 1.98% | −0.62 |
| E56p5AJK | insiders12 | T1 净买入额 | −0.25 | −0.07 | 2.18% | −0.24 |

（另有 5 条首派因 `winsorize` 吃 VECTOR 输入全批连坐报错，已修正重派 —— 见 §5。）

### W2 · techindi_model（OTHER 塔） · 中性化 CROWDING · **4/8 出正 Sharpe，1 条全闸 PASS**

| alpha | 骨架 | 核心字段 | S | F | TO | 2Y | sub | 平台 fail |
|---|---|---|---|---:|---:|---:|---:|---:|---|
| **RREbjXre** | **P** | tm_8 … **r5_q1** | **2.23** | **1.39** | **23.59%** | **3.28** | **2.36** | **无** |
| 78LN7Ow1 | S | tm_16 … r10 q5_p4 − q5_p0 | 2.25 | 1.27 | 24.56% | **0.46** | 1.98 | 无（2Y 仅 warning） |
| 3qoXQdAO | P | tm_15 … r10_q1 | 1.74 | 0.93 | 24.08% | 2.30 | 2.10 | 无（F 仅 warning） |
| omEL82Yv | P | tm_1 … r1_q1 | 0.74 | 0.24 | 27.05% | 1.63 | 0.80 | LOW_SHARPE, LOW_FITNESS |
| P0o2QepJ | Q | tm_16 … r1_q5_p4（门控） | 0.72 | 0.33 | 8.82% | 0.95 | 0.61 | +LOW_2Y |
| pwdRY06o | R | tm_8 … r5_q5_p3（delta 门控） | −0.21 | −0.04 | 17.83% | −0.49 | −0.12 | 多项 |
| bl6bGpLN | R | tm_15 … r1_q3_p1（delta 门控） | −0.80 | −0.31 | 18.95% | −1.06 | −0.47 | 多项 |
| N1NaxMpo | Q | tm_1 … r10_q3_p1（门控） | −0.82 | −0.39 | 8.04% | −0.79 | −0.50 | 多项 |

### W3 · other567 / other696 / institutions25 / insiders12 · SUBINDUSTRY · 8 臂全灭

最高 S 仅 0.38（V2 other567 trendrating−overall），其余 −0.80 ~ 0.11。**全部换手 2.1%–9.0%**。

## 3. 归因：三个变量各自的作用

### 3.1 骨架（最重要）
- **P 骨架（无门控双窗 add）**：3/3 正，S = 0.74 / 1.74 / **2.23**，均值 1.57。
- **Q/R 骨架（`trade_when` 门控 + ts_zscore / ts_delta）**：0/4 正，S = −0.82 ~ 0.72。
- **S 骨架（概率利差 top−bottom）**：1/1，S 2.25 但 2Y 0.46。

⇒ **门控是杀手，不是保护。** `trade_when` 把样本切成稀疏子集，在 TOP700 这种 700 只票的单一国家池里，稀疏化直接摧毁横截面宽度；同时把换手压到 8%（vs P 族的 24%），而换手正是本族收益的来源。P 骨架不做任何事件筛选，只用「1 日 + 60 日双窗」把短周期预测与长周期趋势叠在一起，信息密度最高、换手自然落在 24%。

### 3.2 换手率与 Sharpe 的关系（本轮最强规律）
把所有 32 臂按 TO 分桶：

| TO 区间 | 臂数 | 平均 S | 最高 S |
|---|---:|---:|---:|
| < 5% | 15 | −0.10 | 0.38 |
| 5%–10% | 7 | −0.05 | 0.72 |
| 10%–20% | 2 | −0.51 | −0.21 |
| **20%–30%** | **4** | **1.72** | **2.25** |

**TO < 5% 的臂无一例外是噪声**。机制解释：字段本身慢变（员工评分季度更新、机构持仓月更、形态相似度是长窗统计量），经过 `rank → winsorize → ts_target_tvr_decay` 后组合几乎不动，等于买入一个静态截面组合持有十年 —— 而 GBR 十年市场中性收益没有静态截面可套。预测收益类字段（techindi_model）每天更新且本身带方向，才能支撑 24% 换手。

⇒ **下一波一律以 target_tvr 0.40–0.50 起步，禁止往 0.35 以下压**（W2 的 Q/R 用 0.35，W3 用 0.35，全部失败）。

### 3.3 数据集
- **techindi_model（预测收益元数据）≫ pattern_scores（形态相似度）≈ 事件/情绪水平数据集**。
- 根因：`tm_*` 字段的语义就是「未来 N 日市场中性收益的预测」，`rank()` 之后直接就是组合权重，无需二次方向映射；而 `avg_overall_company_score`（1–5 分）、`inst25_sentiment`、形态相似度（0–1）这些**水平量本身不含方向**，rank 后得到的是「谁更高」而不是「谁会涨」，横截面排序与未来收益无因果关系。
- 逐字段 `alphaCount`：techindi 的 `q1` 系列 22–1217、`_p*` 系列 40–288；other567 0–2；pattern_scores 多 0–100。**低 alphaCount + 有方向语义**才是富矿，单看 alphaCount 会误判 other567 是富矿。

### 3.4 2Y 与 S 的关系
P 族 S 与 2Y **同向且放大**（0.74→1.63、1.74→2.30、2.23→3.28），说明该信号在 2022–2023 尤其强。
S 族是唯一例外：S 2.25 但 2Y 0.46 ⇒ 概率利差信号在最近两年失效，**不可用**（虽平台只给 warning）。

## 4. 互相关实测（★★★ 决定产能上限）

| 对 | 互相关 |
|---|---:|
| RREbjXre × 3qoXQdAO | **0.6191** |
| RREbjXre × 78LN7Ow1 | 0.1173 |
| 3qoXQdAO × 78LN7Ow1 | 0.1678 |

self 相关：RREbjXre **0.2292** / 3qoXQdAO 0.2195 / 78LN7Ow1 0.2046（全部远低于 0.70）。

⇒ **同骨架同族（P 族）内部 0.62，已接近 0.70 红线**：P 族最多共存 2 颗。跨骨架（P × S）仅 0.12，独立性极好但 S 族 2Y 不达标。
**产量上限的瓶颈是「互异核心条数」，不是候选条数。**

## 5. 已确认的坑（写入 SOP）

1. `winsorize` / 任何标量算子不能吃 VECTOR 字段，必须先 `vec_avg(F)` 聚合：写 `winsorize(vec_avg(F), std=4)`，不能写 `vec_avg(winsorize(F))`。**一条类型错会连坐整批 8 条 CANCELLED。**
2. `preflight_expressions` 对上述类型错照样返回 `valid: true`，只有真跑才暴露。
3. GBR 不能用 `COUNTRY` 中性化（单一国家）。
4. prod 相关性全账号单槽位，未缓存项 ~13 分钟；命中缓存 5 秒返回。**按族抽样测 2 条即可判族死活。**
5. 平台闸的 fail/warning 分级与本地阈值不一致：`LOW_2Y_SHARPE 0.46` 与 `LOW_FITNESS 0.93` 在平台上是 **warning（不阻断提交）**，但按本地 SOP（2Y≥1.6、F≥1.0）应判不合格。**入库一律以本地阈值为准。**

## 6. 模板库登记（结构互异 ≥10，本轮累计 15）

| # | 模板 | 结构 | 来源 | 结果 |
|---|---|---|---|---|
| T1 | 价差（gap_up − gap_down） | subtract(rank, rank) | 自建 | 灭 |
| T2 | delta + 门控 | ts_delta + trade_when | 自建 | 灭 |
| T3 | 对称离散度 | 多字段标准差 | 自建 | 灭 |
| T4 | 形态比值 | divide(rank, rank) | 自建 | 灭 |
| T5 | wedge 价差 | subtract(rank, rank) | 自建 | 灭 |
| T6 | q95 事件门控 | ts_quantile 阈值 + trade_when | 自建 | 灭 |
| T7 | 分位变换 | ts_quantile | 自建 | 灭 |
| T8 | 最大值长窗 | ts_max 水平 | 自建 | 灭 |
| T9 | 水平直接 rank | rank(level) | 自建 | 弱 |
| T10 | 趋势偏离利差 | subtract(trendrating, level) | 自建 | 弱 |
| T11 | 两维情绪利差 | subtract(outlook, culture) | 自建 | 灭 |
| T12 | 比率归一 | divide(pos, pos+neg) | 自建 | 灭 |
| T13 | **P：双窗 add 无门控** | add(ts_mean(·,1), ts_mean(·,60)) | 自建 | **★★★ 成功** |
| T14 | **S：概率利差 top−bottom** | subtract(logp_high, logp_low) | 自建 | S 高但 2Y 崩 |
| T15 | 门控（zscore / delta） | trade_when 包装 | 自建 | 灭 |
| T16 | **D：离散度（二阶矩）** | subtract(ts_std_dev, ts_mean(ts_std_dev)) | 自建 | W4 在飞 |

## 7. 下一波原则

1. **只做 techindi_model 的 P 族横向扩展**（版本 tm_1/8/15/16 × 周期 r1/r5/r10 × 连续核心 q1 / 概率核心 _p*），target_tvr ≥ 0.40。
2. **禁止门控**（Q/R 骨架作废），**禁止事件/情绪水平数据集**（other567/other696/institutions25/insiders12 判弱族）。
3. 分组轴做 A/B（sector / subindustry / industry）确认轴效应，供后续所有波次固定。
4. 每批收完先跑 `compute_mutual_correlation`，>0.70 的只留 1 颗。
5. pattern_scores 的 PV 路线在本区走死（形态相似度无方向），需另找 PV 有方向字段才能点亮 pv 塔。

---

## 8. W4 增补（2026-11-04 晚）——本轮最重要的两条定律

W4 在 techindi_model 上跑 8 臂（全部 CROWDING / sector 除 A/B 臂），**4 条过本地全闸**：

| alpha | 模板 / 杠杆 | 核心 | S | F | TO | 2Y | sub | 平台 fail |
|---|---|---|---|---:|---:|---:|---:|---:|---|
| **zq38KdX1** | P · 换版本 | tm_**16** … r5_q1 | **2.33** | **1.44** | 23.23% | 1.61 | 2.20 | 无 |
| **ZYQbPakn** | P · 换周期 | tm_8 … **r10**_q1 | **2.14** | **1.30** | 23.68% | **3.10** | 2.35 | 无 |
| **akKbja26** | P · 分组轴 industry | tm_8 … r5_q1 | **1.97** | **1.08** | 24.30% | 2.69 | 1.82 | 无 |
| **xAr3OvXm** | P · 换周期 | tm_8 … **r1**_q1 | 1.78 | 1.01 | 24.82% | 2.97 | 1.95 | 无 |
| wpQZKoXd | P · 分组轴 subindustry | tm_8 … r5_q1 | 1.77 | 0.88 | 25.48% | 2.18 | 1.77 | 无（F<1.0） |
| 0mYXOPnG | P · 换版本 | tm_1 … r5_q1 | 1.00 | 0.36 | 26.22% | 0.94 | 0.98 | 无（F/S 不达标） |
| N1NaxPk8 | P · 概率核心 | tm_16 … r5_q5_p4 | 0.88 | 0.41 | 20.04% | −0.67 | 0.65 | 3 项 |
| 78LN7Yqb | D · 离散度二阶矩 | tm_16 … r5_q1 | 0.30 | 0.08 | 6.77% | −0.27 | −0.09 | 4 项 |

### 8.1 定律一：独立维度是「模型版本」，不是周期 / 分组轴 / 分位桶

7 条 techindi 候选两两互相关矩阵：

| | tm_8 r5 | tm_8 r10 | tm_8 r1 | tm_8+industry | tm_8+subind | tm_16 r5 | tm_1 r5 |
|---|---:|---:|---:|---:|---:|---:|---:|
| **tm_8 r5**（RREbjXre） | 1 | 0.966 | 0.861 | 0.934 | 0.839 | **0.216** | **0.266** |
| tm_8 r10（ZYQbPakn） | 0.966 | 1 | 0.825 | 0.908 | 0.821 | 0.190 | 0.253 |
| tm_8 r1（xAr3OvXm） | 0.861 | 0.825 | 1 | 0.811 | 0.727 | **0.031** | 0.182 |
| tm_8+industry（akKbja26） | 0.934 | 0.908 | 0.811 | 1 | 0.887 | 0.178 | 0.288 |
| tm_8+subind（wpQZKoXd） | 0.839 | 0.821 | 0.727 | 0.887 | 1 | 0.139 | 0.283 |
| **tm_16 r5（zq38KdX1）** | 0.216 | 0.190 | 0.031 | 0.178 | 0.139 | 1 | 0.224 |
| tm_1 r5（0mYXOPnG） | 0.266 | 0.253 | 0.182 | 0.288 | 0.283 | 0.224 | 1 |

**最大「两两 <0.70」子集 = 3 条**（RREbjXre + zq38KdX1 + 0mYXOPnG），其中 0mYXOPnG 质量不达标 ⇒ **techindi_model 实际只能出 2 颗**。

⇒ 一条数据集的产量上限 = **它有几个互异「模型/版本/训练目标」**，不是有几个字段 / 几个周期 / 几个分组轴。

### 8.2 定律二：GBR 单国家池分组轴越粗越好（与 GLB 相反）

同核心同骨架只换轴：**sector 2.23 / 1.39 → industry 1.97 / 1.08 → subindustry 1.77 / 0.88**（S / F），2Y 同序 3.28 → 2.69 → 2.18。
机制：TOP700 只有约 700 票，subindustry 分组后每组只剩个位数，`group_rank` 逐组噪声化。

### 8.3 prod 墙：RREbjXre = 0.7965（超 0.70）

本地全闸通过的 RREbjXre 实测 **prod 0.7965**，被生产池相关性挡住。self 仅 0.2292 ⇒ 再次印证「**self 干净 ≠ prod 干净**」。
⇒ W5 专攻降 prod：`signed_power(·,3)`（改持仓结构、Sharpe 基本不变）、`bucket(rank(cap),range="0,1,0.1")` 市值分桶轴（论坛 35 票贴的模板）、`ts_rank` 时序分位变换（改信息加工）。

### 8.4 修订后的产量估算

| 来源 | 上限 | 已得 |
|---|---:|---:|
| techindi_model（OTHER，4 版本） | 4 | 2（tm_8 族 1 + tm_16 1） |
| pattern_scores（PV） | 0 | 0（形态无方向，判死） |
| other567 / other696 / institutions25 / insiders12 | 0 | 0（TO 2–9%，判弱族） |
| **合计** | **≤4** | **2** |

⇒ **要达到 20 颗，必须再找 4–5 个「多版本预测类 / 模型输出类」数据集**，靠单一 techindi_model 数学上不可能。下一阶段主线任务 = 在 GBR 177 个数据集里筛出同类结构。


---

## §9 W6 / W7 归因（2026-11-04 增补）—— 两波 16 臂全灭的根因

### 9.1 W6（other566，Image-Based Financial Prediction）multisim `qhWHC3eL4LycpWtgmieK4O`

| # | 臂 | 模板 | 核心字段 | S | F | TO | 2Y |
|---|---|---|---|---:|---:|---:|---:|
| Q1 | pred-r10 | P | `quantile1_predicted_label_r10` | −0.06 | −0.01 | 11.4% | 0.13 |
| Q2 | pred-r20 | P | `quantile1_predicted_label_r20` | −0.21 | −0.06 | 11.5% | −0.21 |
| Q3 | probspread5-r10 | SPREAD | `quantile5_label4−0_probability_r10` | 0.16 | 0.05 | 11.2% | 0.09 |
| Q4 | probspread5-r20 | SPREAD | `quantile5_label4−0_probability_r20` | 0.07 | 0.01 | 10.9% | 0.02 |
| Q5 | probspread3-r10 | SPREAD | `quantile3_label2−0_probability_r10` | 0.08 | 0.02 | 11.1% | 0.04 |
| S1 | surprise | SURPRISE | `time_series_forecast_value` | 1.00 | 0.40 | 36.2% | **0.15** |
| T1 | ppo | P | `percentage_price_oscillator_value` | **−0.94** | −0.46 | 23.6% | −0.25 |
| T2 | rsi | P | `relative_strength_index_value` | **−1.22** | −0.64 | 20.5% | −0.78 |

**归因一（决定性）**：预测标签族 Q1–Q5 五条 S 全落在 ±0.21，TO 全部 11.0–11.5%。
五种不同的概率组合（单标签 / 5 类利差 / 3 类利差）× 两个窗口，**方差近乎为零** ⇒
`other566` 的预测族**整体无横截面 alpha**，是数据本身没有信息，不是模板选错。
TO 11% 恰落在本项目「TO<20% 平均 S 为负」的死区，也印证这些字段的日度变化近乎噪声。

**归因二（意外收获）**：原始技术振荡器在 GBR 上**方向为负**——RSI −1.22、PPO −0.94。
取反后约 +1.22 / +0.94，虽未达 1.58 闸线，但证明「超买超卖 → 反向」在 GBR 成立。
这条方向先验直接决定了 W10 的分族设计（超买超卖族反向、资金流族正向）。

**归因三**：surprise 模板 S 1.00 / F 0.40 / TO 36.2% / **2Y 0.15** —— 典型的「2Y 崩」形态，
按 §6 定律（2Y 是两年合池、早年单年必须 ≥1.6）判死，不再投入。

### 9.2 W7（chart_cnn_alpha，Deep Learning Chart-Based Alpha）multisim `1R2vSzgNe4sX8OJIXYYFLUl`

先前的 `lookINTO` 返回 `Simulation did not get through`（status=null）**是临时状态误报**，
该批实际被受理并跑完 8/8。教训：status=null 不等于未受理，需以轮询的 children 出现为准。

| # | 臂 | 核心 | S | F | TO | 2Y |
|---|---|---|---|---:|---:|---:|---:|
| 1 | leapstar6_r5 label | `img_leapstar6_r5_q1_quantile_label` | 0.26 | 0.05 | 18.0% | 0.09 |
| 2 | leapstar6_r30 label | `img_leapstar6_r30_q1_quantile_label` | 0.14 | 0.02 | 13.0% | −0.13 |
| 3 | malta2_r50 label | `img_malta2_r50_q1_quantile_label` | −0.11 | −0.03 | 5.2% | 0.28 |
| 4 | malta2_r80 label | `img_malta2_r80_q1_quantile_label` | −0.12 | −0.03 | 5.4% | 0.27 |
| 5 | malta1_r180 label | `img_malta1_r180_q1_quantile_label` | −0.07 | −0.01 | 3.5% | −0.07 |
| 6 | leapstar6 spread | `prob_class4−prob_class0` | 0.12 | 0.02 | 12.8% | −0.14 |
| 7 | option IV 期限结构 | `option_put_iv_level_6 − option_call_iv_level_6` | **0.30** | 0.13 | 10.1% | **1.47** |
| 8 | 高管因子 | `vec_avg(oth128_dmexusscore)` | 0.02 | 0.00 | 2.5% | 0.15 |

**归因四（关键设计缺陷）**：W7 的 6 条图像臂全部用了 `q1_quantile_label`——这是**离散分位标签**，
横截面只有 5 档，经 P 骨架平滑后区分度被彻底抹平。真正有信息的是 `prob_class` 连续概率。
W6 的教训（离散 label 无用）+ W7 的教训（label 无用）指向同一条：**预测类数据集必须取连续概率/回归输出，绝不用离散 label**。

**归因五**：7 号臂（期权 IV 期限结构 put−call）S 虽低（0.30）但 **2Y 1.47 远优于同批其他臂（−0.14~0.28）**，
是唯一表现出长周期一致性的结构 ⇒ `option_chart_model` 值得单独开一波（option 塔当前 0 颗）。

**归因六**：`oth128_dmexusscore`（高管持股因子）TO 仅 2.5%，落在死区，单字段无杠杆可用。

### 9.3 新增结构定律

**定律四（算子预算的结构约束）**：P 骨架 `add(ts_mean(core,1), ts_mean(core,60))` 里 **core 出现两次**，
因此 core 自身的算子数要 **×2** 计入总算子预算。techindi 能压到 10 ops 是因为 core 是单字段（0 ops）。
任何「两个概率字段相减」的 core（3 ops）经骨架复制后变 6 ops，总 16 ops **超限**。
⇒ 用多字段 core 时必须改用单算子聚合（如 `add(p3,p4)` 而非 `subtract(add(p0,p1),add(p3,p4))`）。

**定律五（预测类数据集的取数铁律）**：预测类数据集的字段必须取**连续**形态——
回归输出（`q1` 连续值）、概率（`prob_class*`、`*_probability`）；
**离散分位标签（`quantile_label`、`predicted_label`）一律不用**，横截面 5 档经骨架平滑后无区分度。
这条同时解释了 techindi 成功（`q1` 连续回归输出）与 other566/chart_cnn 的 label 臂失败。

**定律六（数据集产量的真正判据）**：一个预测类数据集能出几颗，取决于它有多少个**互异的预测目标/模型**，
而不是字段数。other566 112 字段 → 0 颗（全是同一预测目标的变体）；chart_cnn 122 字段 → 至多 3 颗（3 个模型）；
techindi 399 字段 → 至多 2 颗（4 版本中 2 个 F 不达标）；**model135 137 字段 → 23 个互异技术指标，理论上限最高**。

---

## §10 W8–W11 归因 + 十二波总复盘（2026-11-04）

### 10.1 四波 32 臂结果

**W8 multi_source_model（16 种互异预测来源）`2c1AfugYU4VSavYqwzbA8xE`** —— 全灭
S −0.16~0.32，**TO 全部 3.3%–10.6%**。8 条臂覆盖 fundamental/analyst/price_volume/long_horizon_hedge3/
short_horizon_hedge3/long_term_seasonal/long_term_regime2/regime4_embedding，全部无信号。
最好 `88Rjolnz`（S 0.32 / sub 1.11 / TO 5.94%）。

**W9 chart_cnn 概率连续化 `Jaiv08CW4UO8AqkXEP2MeD`** —— 全灭
改用 `add(prob_class3, prob_class4)` 连续概率（替代 W7 的离散 label），3 个模型 × 2 窗口。
S −0.13~0.16，TO 2.2%–20.2%。**改成连续概率也没有救回来** ⇒ chart_cnn 整体无效。

**W10 model135（23 个经典技术指标 × 5 参数版本）`1k0oSA6VK4mR9tFt2LUptzF`** —— 全灭
超买超卖族反向（isr/icc/os/isrs）+ 资金流族正向（lda/vbo/ifm）+ 趋势族（xda）。
S −0.38~0.26，**TO 全部 9.1%–12.7%**。
资金流族正向全负（lda −0.38 / vbo −0.24 / ifm −0.27）⇒ 量价资金流在 GBR 也是反向。

**W11 option_chart_model（call/put IV 13 档 + 平价偏离 13 档）`2JghdBekD4t89H68JkUcx77`** —— S 不达标但有重大发现
S 0.16–0.33，TO 7.2%–9.8%，**但 2Y 全部 1.27–1.93**。
其中 `QPvbkVeg`（call 期限斜率，2Y **1.83**）与 `e75bw0ep`（put 期限斜率，2Y **1.93**）
**只 FAIL LOW_SHARPE / LOW_FITNESS，2Y 闸通过** —— 这是全部 88 臂里 2Y 最强的结构。

### 10.2 定律七（本轮最重要的发现）

**TO 不是可调参数，而是字段「信息新鲜度」的外在表现。**
`ts_target_tvr_decay(target_tvr=0.45)` 只能**压低**换手，不能**抬高**——字段本身变化慢时，TO 就停在它的自然水平。

实证分布（12 波 88 臂）：

| 字段族 | 自然 TO | 最好 S | 判定 |
|---|---:|---:|---|
| techindi `tm_*_q1`（模型每日重新预测） | **23–25%** | **2.33** | ✓ 出货 |
| other566 技术振荡器（10 日滚动统计） | 20–24% | −1.22 | ✗ 方向反且幅度不足 |
| model135 技术指标（10 日滚动统计） | 9–13% | 0.26 | ✗ |
| option IV（13 档水平/斜率） | 7–10% | 0.33 | ✗（但 2Y 1.9） |
| chart_cnn 概率（模型输出） | 2–20% | 0.16 | ✗ |
| multi_source_model（5d–120d 预测） | 3–11% | 0.32 | ✗ |
| other566 预测标签族 | 11% | 0.16 | ✗ |

**判据**：**只有「每个交易日都在重新估计」的字段才有高 TO**。
techindi 的 `q1` 是模型对未来的逐日预测（每天重估）；技术指标是 10 日窗口的滚动统计（每天只换 1/10）。
这个差异决定了 TO 差 2–7 倍，也决定了唯一出货的数据集是哪一个。

### 10.3 十二波总复盘

| 波 | 数据集 | 塔 | 臂 | 最好 S | 结果 |
|---|---|---|---:|---:|---|
| W1-A | pattern_scores | pv | 8 | 0.15 | 全灭 |
| W1-B | other567/696/128 等 | other | 8 | 0.40 | 全灭 |
| W2 | techindi_model | other | 8 | **2.23** | **2 颗过闸** |
| W3 | 空白数据集 | - | 8 | 0.38 | 全灭 |
| W4 | techindi_model 横向 | other | 8 | **2.33** | **4 颗过闸** |
| W5 | techindi + 降 prod 杠杆 | other | 8 | 2.64 | 3 颗过闸 |
| W6 | other566 | other | 8 | 1.00 | 全灭 |
| W7 | chart_cnn_alpha | model | 8 | 0.30 | 全灭 |
| W8 | multi_source_model | model | 8 | 0.32 | 全灭 |
| W9 | chart_cnn 概率化 | model | 8 | 0.16 | 全灭 |
| W10 | model135 | model | 8 | 0.26 | 全灭 |
| W11 | option_chart_model | option | 8 | 0.33 | 全灭（2Y 1.9） |
| **合计** | | | **96** | | **1 个数据集出货 / 12 波** |

**命中率 1/12**。所有产出集中在 techindi_model 一个数据集，而它的 4 个版本中只有 tm_8 / tm_16 的
Fitness 过 1.0，互相关矩阵又决定同族最多出 2 颗 ⇒ **techindi 的产量硬上限是 2**。

### 10.4 下一阶段的三条具体路线

1. **中性化对照（W12 已派）**：12 波全部使用 CROWDING，从未与 config 默认的 SUBINDUSTRY 对照过。
   若 SUBINDUSTRY 下 tm_15（F 0.93）/ tm_1 的 Fitness 翻过 1.0，则 techindi 的产量上限从 2 抬到 4，
   且证明「中性化」是本项目最大的未验证变量。
2. **期权期限斜率（2Y 1.83–1.93）**：唯一表现出强长周期一致性的结构。S 仅 0.25，需要找
   2014–2021 段也有效的增量腿才有救；单靠参数调不动。
3. **未点亮塔的真实矿脉**：GBR 177 个数据集里，0 塔 category 尚存的活数据集为
   risk60/68/71/72（risk）、institutions1/25、insiders1/12、sentiment27/33、socialmedia5/12、
   earnings6、imbalance5。其中 **sentiment33（255 字段，多情绪抽取方法 × 6 极性 × 4 窗口）**
   最符合「多版本」定律，是下一批的首选。

---

## §11 W13 突破：tm_15 定向破墙成功（2026-11-04）

### 11.1 设计逻辑

W12 的互相关矩阵揭示：**tm_15 与 tm_8/tm_16 互相关仅 0.53–0.58**，是全项目唯一真正正交的核心；
但 tm_15 r5 的 Fitness 只有 0.93，差 0.07 不能进提交篮。W13 因此对 tm_15 做**单杠杆定向破墙**，
基准为 W5-V1（tm_15 r5 / sector / CROWDING）= S 1.74 / F 0.93 / 2Y 2.30 / TO 24.08%。

### 11.2 八臂结果

| 臂 | 杠杆 | S | F | TO | 2Y | sub | 平台 fail |
|---|---|---:|---:|---:|---:|---:|---|
| A1VNMX6R | cap bucket | 1.92 | 1.02 | 24.3% | 1.57 | 1.84 | IS_LADDER_SHARPE |
| xAr307Mn | market 分组 | 1.61 | 0.87 | 24.0% | 1.71 | 1.97 | 无 |
| **58EzoKR5** | market+cap 混合轴 | 1.89 | **1.00** | 24.8% | **2.02** | 1.89 | **无** |
| wpQZM7Xp | industry 分组 | 1.51 | 0.74 | 24.7% | 1.25 | 1.73 | 无 |
| omELMjQv | cap bucket (r10) | 1.88 | 0.97 | 24.4% | 2.10 | 1.79 | LOW_FITNESS |
| QPvbLRmG | cap bucket (r1) | 1.89 | 0.96 | 26.0% | 1.56 | 1.74 | LOW_FITNESS + IS_LADDER |
| 6Xdjv6gG | cap bucket + signed_power3 | 1.63 | 0.78 | 24.2% | 1.58 | 1.54 | LOW_FITNESS + IS_LADDER |
| **Xg9b5ZX0** | **cap bucket + target_tvr 0.50** | **2.07** | **1.07** | 27.2% | **2.09** | 1.93 | **无** |

**两条全闸通过**，其中 **Xg9b5ZX0** 全项最优：相对基准 S +19%（1.74→2.07）、F +15%（0.93→1.07），
2Y 仍保持 2.09，TO 27.2% 在 30% 上限内。

### 11.3 破墙杠杆的有效性排序（tm_15 r5 单变量）

| 杠杆 | ΔS | ΔF | 判定 |
|---|---:|---:|---|
| **cap bucket + target_tvr 0.45→0.50** | **+0.33** | **+0.14** | ★ 最强，双增 |
| cap bucket（单独） | +0.18 | +0.09 | 有效但 2Y 掉到 1.57 |
| market+cap 混合轴 | +0.15 | +0.07 | 有效，2Y 保住 2.02 |
| industry 分组 | −0.23 | −0.19 | 反向 |
| market 分组（单独） | −0.13 | −0.06 | 反向 |
| signed_power3 | −0.11 | −0.15 | 反向（与 W5 结论一致） |

**结论**：对 tm_15，**cap bucket 是唯一正向的分组轴改造**，且与 target_tvr 0.50 有叠加增益；
market / industry 单用都反向，signed_power3 一律反向（三次实证一致）。

### 11.4 最终提交篮（3 颗正交全闸件）

| alpha | 核心 | S | F | TO | 2Y | sub | self | prod |
|---|---|---:|---:|---:|---:|---:|---:|---:|
| **Xg9b5ZX0** | tm_15 r5 + cap + tvr50 | 2.07 | 1.07 | 27.2% | 2.09 | 1.93 | 0.213 | 待测 |
| **zq38KdX1** | tm_16 r5 sector | 2.33 | 1.44 | 23.2% | 1.61 | 2.20 | 0.229* | 待测 |
| **YP1bGkGq** | tm_8 r5 SUBINDUSTRY | 1.91 | 1.03 | 25.0% | 2.20 | 2.10 | 0.235 | 待测 |

**两两互相关**：Xg9b5ZX0×zq38KdX1 = **0.2331**，Xg9b5ZX0×YP1bGkGq = **0.4681**，
zq38KdX1×YP1bGkGq < 0.70。三条构成合法的 3 颗独立件。

### 11.5 prod 锁的真相（排障结论）

此前把 prod 长时间 `pending` 判为「平台僵死锁」，实际排查发现 **holder 从 `bl6bYRPN` 轮转为 `wpQYNvZp`**
——是**本项目遗留的后台 prod 队列任务**（`bg_7351c8a3`「prod 队列 W4 五条」）在持续占用全账号唯一的
in-flight 槽位，把后续所有候选排队阻塞。停掉该任务后槽位即恢复。

**教训**：平台 prod 只允许一个 in-flight 计算；**任何后台轮询队列必须先确认没有长期占用槽位**，
否则表现为「候选永远 pending」，极易误判为平台故障。此外 `holder` 字段是判断「谁在占用」的唯一入口，
每次 `correlation_busy` 都应读 holder 并核对是否为自己的任务。

---

## §12 W14（sentiment33）归因 —— 全部波次中 TO 最低的一族

### 12.1 结果

八臂 = 4 种互异情绪抽取方法（method 1–4）× 2 个窗口（fkw1 / fkw3），核心为净情绪
`subtract(vec_avg(pos), vec_avg(neg))`，采用**单窗情绪骨架**（core 只出现一次，压到 10 ops）：

`group_rank(ts_target_tvr_decay(winsorize(rank(group_neutralize(ts_mean(ts_backfill(CORE,500),5), sector)), std=0.2), lambda_min=0, lambda_max=1, target_tvr=0.45), sector)`

| alpha | method/窗口 | S | F | TO | 2Y | sub |
|---|---|---:|---:|---:|---:|---:|
| akKbv8ZW | m1 fkw1 | −0.21 | −0.06 | 3.11% | 1.10 | 0.12 |
| P0o29baL | m2 fkw1 | −0.03 | −0.00 | 3.14% | 1.34 | 0.31 |
| wpQZgAM6 | m3 fkw1 | −0.09 | −0.02 | 3.17% | 1.39 | 0.19 |
| O0ANajEJ | m4 fkw1 | −0.15 | −0.04 | 3.18% | 1.20 | 0.24 |
| 1YNXERQM | m1 fkw3 | −0.15 | −0.04 | 3.24% | 1.12 | 0.16 |
| MPYamnm8 | m2 fkw3 | −0.22 | −0.07 | 3.20% | 1.37 | 0.02 |
| akKbv8vx | m3 fkw3 | −0.16 | −0.04 | 3.21% | 1.10 | 0.17 |
| 9qxj030e | m4 fkw3 | −0.20 | −0.06 | 3.25% | **1.50** | 0.09 |

### 12.2 归因

**八臂 TO 全落在 3.11%–3.25%** —— 四个互异 NLP 方法、两个窗口、八条完全不同的表达式，
TO 方差不足 0.15 个百分点。这是**数据本身没有日频变化**的铁证：情绪得分按天聚合后几乎不动。

**2Y 普遍 1.10–1.50 但 S 为负**：说明情绪信号在 2022–2023 段方向是正的，而 2014–2021 段把它抹平了，
且 TO 3% 意味着每年只交易 7 次左右，无法累积收益。

### 12.3 对产品含义

sentiment 塔（GBR 当前 0 颗）在 sentiment33 上**没有可行路径**。该数据集 255 字段、
多方法多极性看似是富矿，但受限于 3% 的自然换手，任何模板都会落在死区。
若要点亮 sentiment 塔，应改用**事件驱动**形态（新闻发布日前后集中建仓）而非水平/净差形态，
即用 `trade_when` 把交易压缩到事件日，把 TO 从 3% 拉高——但这需要先找到事件日期字段。

---

## §13 W15（risk/imbalance）+ 定律七的重要修正

### 13.1 W15 结果（multisim `2srojp1V84igaLbUmYcNCPO`）—— 全灭

八臂覆盖 risk71 的三个 universe 残差收益、risk60 的券借贷费用/拥挤度、risk68 的残差收益与 DADV 权重、
imbalance5 的订单失衡分数。**全部 FAIL LOW_SHARPE / LOW_FITNESS / LOW_2Y_SHARPE**。

| alpha | 核心 | S | F | TO | 2Y | sub |
|---|---|---:|---:|---:|---:|---:|
| omELeVPv | risk71 top600 残差 | −0.17 | −0.05 | 7.8% | 0.75 | 0.22 |
| 1YNX5JGz | risk71 top800 残差 | −0.30 | −0.11 | 8.6% | 0.42 | −0.13 |
| P0o2EvPx | risk71 top1200 残差 | −0.46 | −0.19 | 11.8% | −0.18 | −0.34 |
| Xg9bE1N0 | risk60 拥挤度 | 0.02 | 0.00 | 11.3% | 1.26 | −0.11 |
| 2rAwkJ9b | risk60 借券费 | 0.07 | 0.01 | 5.6% | 0.39 | −0.11 |
| omELeVRv | risk68 残差 | **−1.01** | −0.56 | 17.8% | −0.59 | −0.60 |
| 1YNX5JOz | risk68 DADV | −0.01 | −0.00 | 3.8% | 0.37 | 0.58 |
| RREbLd9e | imb5 订单失衡 | 0.23 | 0.09 | 4.5% | −0.04 | **1.34** |

### 13.2 定律七的重要修正（关键）

W15 的 1/3/6 号臂用的是**纯日频残差收益**——理论上每天都是新信息，TO 应该很高。
但实测 TO 只有 7.8% / 11.8% / 17.8%。**这说明 TO 被 P 骨架压低了，不只是字段的问题**。

P 骨架 `add(ts_mean(core,1), ts_mean(core,60))` 里的 **`ts_mean(core,60)` 是 60 日平滑项**，
它把一个日频信号抹成两个月尺度的慢变量，权重占一半 ⇒ TO 被腰斩。

**修正后的表述**：
- 字段的「自然 TO」= 字段每日更新的信息量；
- 骨架的「平滑衰减」= `ts_mean(core,W)` 的 W 越大，TO 越低；
- **实测 TO ≈ min(字段自然 TO, 骨架允许 TO)**。
- techindi 能拿 23–27% 是因为字段本身信息足够强，即使被 60 日项平滑后仍剩 23%；
- 日频残差收益被同一骨架压到 8–18%，是因为它的信号强度不足以穿透 60 日平滑。

**应用**：**先判断信号的时间尺度，再选骨架的窗口**——日频反转/残差类必须用 `ts_mean(·,1)+ts_mean(·,5)`
或更短的短窗骨架；只有当信号本身是月度以上尺度（如 techindi 的模型预测）时才用 1+60。
把长窗骨架套在日频信号上，等于人为把 alpha 抹掉。W17 即为这次修正的直接验证（短窗 1+5 / 1+22 对照）。

### 13.3 risk / imbalance 塔的判读

- **risk 塔（0 颗）**：risk71 残差收益、risk60 券借贷、risk68 残差与 DADV 在长窗骨架下全灭。
  W17 用短窗重测后若仍无效，则 risk 塔应判为不可达。
- **imbalance5（0 颗）**：只有 2 个字段（`imb5_score` / `imb5_mktcap`），互异性不足以产出多颗；
  `RREbLd9e` 的 sub_universe_sharpe 1.34 是唯一亮点，但 S 仅 0.23。


---

## §14 W16–W22 归因：18 波只出一个数据集的根因被找到了（2026-11-04 续）

### 14.1 新增波次总表

| 波 | 数据集 / 主题 | 臂 | 最好 S | 结论 |
|---|---|---:|---:|---|
| W16 | global_seasonal_model 置信度桶 | 8 | 0.87 | 全灭 |
| W17 | risk71/risk68/imbalance5 短窗骨架对照 | 8 | 0.25 | 全灭；但暴露 risk68 强反转 |
| W18 | institutions25 / insiders12 / insiders1 / institutions1 / earnings6 / sentiment27 | 8 | 0.42 | 水平形态全灭（最好 earnings 0.42 / sentiment 0.35） |
| W19 | risk68 反转 × 8 几何 + socialmedia12 | 8 | **1.04** | 反转确认；杠杆钉死 1.04；socialmedia 弱 |
| W20 | earnings6 × 8 结构互异模板 | 8 | — | **全批 CANCELLED**（VECTOR 算子误用） |
| W22a | 论坛口径重建（earnings SUE / institutions1 信念强度） | 4 | 在飞 | — |

### 14.2 W17 的关键残留发现：GBR 残差收益是强反转

`rsk68_residual_return` 在**长窗（1+60）与短窗（1+5 / 1+22）下 Sharpe 均为 −1.01 ~ −1.04**，
换手 18–20%，说明这不是窗口效应而是**机制**：GBR 的个股特质残差收益呈强负自相关。

W19 取反后 **S 精确变为 +1.01**（`WjObkV6Q`）——符号翻转完全对齐，证实读数可靠。
但八种杠杆只把它推到 **1.04**：

| 杠杆 | S | 2Y | TO | 备注 |
|---|---:|---:|---:|---|
| 基线 sector（取反） | 1.01 | 0.59 | 17.8% | 对照 |
| cap bucket | 1.00 | 0.86 | 18.0% | 塔位变 **risk/pv**（cap 属 PV） |
| cap bucket + tvr 0.50 | 1.03 | 0.85 | 19.9% | 同上，最好 S |
| market 内层 + cap 外层 | 0.92 | 0.66 | 20.0% | 同上 |
| 窗 1+22 | **1.04** | 0.32 | 18.0% | 最好 S，2Y 最差 |
| beta 水平 | 0.39 | 0.76 | 2.8% | 无信号 |

⇒ **risk 塔经 risk68 残差反转的天花板 ≈ 1.04**，距 1.58 差 52%，单靠几何/参数不可能补上。

### 14.3 W18：五个未点亮塔的水平形态全部无效

| 臂 | 数据集 | 塔 | S | TO |
|---|---|---|---:|---:|
| 空头持仓水平 | institutions25 | institutions | −0.07 | 4.5% |
| 空头持仓 22 日变化 | institutions25 | institutions | −0.05 | 5.4% |
| 空头集中度 | institutions25 | institutions | −0.05 | 4.5% |
| 内部人仓位变动额（带符号） | insiders12 | insiders | −0.20 | 3.3% |
| 内部人交易金额 | insiders1 | insiders | 0.07 | 9.3% |
| 机构交易金额 | institutions1 | institutions | −0.12 | 3.8% |
| **盈余惊喜（实际−估计）** | earnings6 | earnings | **0.42** | 4.4% |
| **网站关注度** | sentiment27 | sentiment | **0.35** | 2.9% |

两个正值臂的共同特征：**换手极低（2.9%–4.4%）但 margin 极高（16.6–22.3bp）**。
earnings 臂还额外 fail `CONCENTRATED_WEIGHT`（事件稀疏导致单票权重超限）。
⇒ 信号存在但在 GBR/TOP700 上太稀薄，靠单一字段水平做不出截面 alpha。

### 14.4 W20 全批 CANCELLED：VECTOR 字段的算子协议

三条臂分别报错，**其余 5 条被连坐 CANCELLED**：

- `Required attribute "k" must have a value` → `kth_element(x, d, k)` 的 k **必须具名** `k=1`
- `Operator days_from_last_change does not support event inputs` → **VECTOR 只接受 `vec_*` / `reduce_*` / `kth_element(k=)` 作为第一跳**

合法写法：`days_from_last_change(vec_avg(F))`、`ts_rank(ts_mean(vec_sum(F),5),252)`。
这条与此前 `winsorize does not support event inputs` 是同一类错误，已并入 memory。

### 14.5 ★★★ 论坛三帖给出三条「反向修正」——我的实现恰好全踩在错的一侧

**(1) 内部人/机构交易的信息在「比值」里，不在「金额」里**（帖 43178926004887，DEU institutions1 实盘 S 1.68 / F 1.34 / TO 7.36% / 2Y 2.40 / prod 0.52 / self 0.11）

    divide(vec_sum(inst1_valueeur), add(vec_sum(inst1_holdings), 0.0001))

三篇文献支撑：Jeng-Metrick-Zeckhauser(2003) 内部人**买入**才有超额、卖出没有；Lakonishok-Lee(2001) 必须按**规模**标准化；Cohen-Malloy-Pomorski(2012) 只有**偏离例行**的交易有信息。
"这笔占我整个仓位的比例" 天然做了规模标准化，例行的定投会被大分母压成 ~0。**去掉分母里的 ε，Sharpe 掉 0.3**。
⇒ W18 我用的是 `vec_avg(inst1_value)` **金额水平**，正是文献说没有信息的那一列。

**(2) 盈余惊喜必须除以 |共识|，且不能用移动平均抹平台阶**（帖 43568407275287）

    sue = (actual − estimate) / max(abs(estimate), 0.01)
    group_zscore(ts_backfill(sue, 80), densify(industry))

- `ts_backfill` 只填**季报空档（80 天）**，**绝不能当日频均线**——"`ts_mean(EPS, 252)` 等于把台阶抹平"。
  我的 S1d/S2 骨架恰好用 `ts_mean(…,1)`+`ts_mean(…,60)`，对这个字段是**结构性错误**。
- **日历字段（距下次公告还有几天）只进 `trade_when`，不要 rank**——"没有『越大越好』的经济学"。
  我在 W20 的 E5/E7（report-breadth / event-recency 走 rank）违反此条。
- `densify(industry)` 是配合 `group_zscore` 的推荐分组写法（此前从未用过）。

**(3) 社交媒体用「时序分位」而非水平，且金字塔倍率 1.5（最高）**（帖 41858767008279）

    ts_rank(ts_mean(sentiment, 5), 252)
    ts_rank(ts_delta(sentiment, 1), 252)

"社交媒体信号衰减快、噪音大、覆盖不足"——需要短窗 + 时序百分位 + 更宽 universe。我用 `scl12_buzz/sentiment` 的**水平**做（W19，S 0.15/0.10），方向没错但形态错。

### 14.6 模板库 v2（12 个结构互异模板，来源标注）

| # | 模板 | 差异维度 | 来源 |
|---|---|---|---|
| T1 | 事件取最新值 `kth_element(F,d,k=1)` | 聚合=最新而非均值 | 自建 |
| T2 | 比值而非差额（流量/存量） | 标准化方式 | forum 43178926004887 |
| T3 | 惊喜/共识归一 `(a−b)/max(\|b\|,0.01)` | 无量纲化 | forum 43568407275287 |
| T4 | 日历只进 `trade_when` 开窗 | 事件门控 | forum 43568407275287 |
| T5 | 时序分位 `ts_rank(x,252)` | 自身历史定位 | forum 41858767008279 |
| T6 | 多视界时序分位相加（252+504） | 矩=多尺度分位 | 自建 |
| T7 | 波动率缩放 `mean/ts_std_dev` | 风险调整 | 自建 |
| T8 | `hump` 稀疏化（只留大变动） | 非线性压缩 | 算子目录 |
| T9 | `ts_decay_linear` 多视界 | 加权几何 | 算子目录 |
| T10 | `ts_zscore(·,252)+ts_zscore(·,504)` | 矩=标准化 | 自建 |
| T11 | 分组轴 = 另一字段 `bucket(rank(B),…)` | 条件化（不叠加 P&L） | CLAUDE.md 指引 |
| T12 | `group_zscore(x, densify(industry))` | 分组写法 | forum 43568407275287 |

T11 是与「禁止两条独立信号腿相加」相容的组合方式：**把 B 当分组轴去评价 A，而不是把 A、B 的收益加在一起。**

### 14.7 ★ 战略重估：20 颗目标 vs GBR 的实际矿脉

`get_pyramid_alphas` 实测我的 GBR D1 金字塔合计 **17 颗**（model 5 / news 3 / analyst 3 / fundamental 3 / pv 2 / other 1）。
"再挖 20 颗"等于**把整个 GBR 的战果翻倍以上**，而未点亮塔里活着的数据集只有 **15 个**：

| 塔 | 活数据集 | 已测机制 | 最好 S |
|---|---|---|---|
| institutions | institutions1, institutions25 | 金额水平、空头持仓水平/变化/集中度 | 0.07 |
| insiders | insiders1, insiders12 | 金额水平、带符号变动额 | 0.20 |
| earnings | earnings6 | 惊喜差额（未归一） | 0.42 |
| sentiment | sentiment27, sentiment33 | 关注度水平、净情绪水平 | 0.35 |
| risk | risk60, risk68, risk71, risk72 | 残差收益反转、beta、券借贷、残差 | **1.04** |
| socialmedia | socialmedia5, socialmedia12 | buzz/sentiment 水平 | 0.15 |
| imbalance | imbalance5 | 分数水平 | 0.25（sub 1.45） |
| option | option_chart_model | IV 期限斜率 | 0.33（2Y 1.93） |
| macro / shortinterest | 无活数据集 | — | 不可达 |

**硬结论**：以现有 15 个数据集 × 已测机制，**可交付量级是 0–2 颗（risk68 反转最接近）**，
不是 20 颗。要把量做上去，只能靠 §14.6 模板库 v2 把每个塔的**机制形态**换掉重测一遍——
这正是 W22 之后的路线，而不是继续在同一骨架上换字段。
