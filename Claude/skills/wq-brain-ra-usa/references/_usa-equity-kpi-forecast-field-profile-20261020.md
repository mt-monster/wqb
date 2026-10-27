# USA · `equity_kpi_forecast` 字段画像与机制设计（ATOM / other 塔）

> 快照日：2026-10-20　|　区域：USA / D1 / TOP3000　|　平台类别：other（未点亮塔）
> 关联：[`_usa-atom-delivery-log-20261020.md`](_usa-atom-delivery-log-20261020.md) · [`_usa-field-profile-playbook-20261018.md`](_usa-field-profile-playbook-20261018.md)

## §0 元数据（`get_datasets` / `get_datafields` / `get_dead_ends` 实检）

| 项 | 值 |
|---|---|
| 数据集 | `equity_kpi_forecast`（KPI Forecast / OdinUltra 预测 vs 街道共识） |
| 字段数 | **22**，**全部 VECTOR** |
| 覆盖率 | 0.3565–0.3804（字段间差异 < 2.4pt ⇒ 覆盖由股票池决定，不由字段决定） |
| userCount / alphaCount | uC 合计 **97**（0–18）；aC 合计 **139**（0–32） |
| 塔位 | other / 未点亮（2026-10-20 复核） |
| dead_end | `get_dead_ends(USA)` **无**该集条目 |
| 平台语义 | OdinUltra（量化模型）对多个 KPI 的**点预测**、相对街道共识的**偏差与方向**、历史**准确度/精度/置信度**元数据、**财报日时点** |

### §0.1 VECTOR 语义与三条硬约束

VECTOR 的第二维 = **KPI metric**（营收 / EPS / 利润率 / 现金流等），同一行内各元素单位不同。

1. **比例 / 标志 / 计数类可跨指标聚合**：`vec_avg` 得到「多指标平均 beat 率 / 平均置信度 / 平均 beat 次数」，经济含义清晰。
2. **原始金额类禁止直接 `vec_avg`**：`analyst_consensus_value`、`predicted_metric_value` 的单位随 metric 变化（$B / $ / %），跨指标平均是**单位混合的伪信号**；本集不做同 metric 内差分，故这两个字段不入选。
3. **非信号字段**：`data_backfill_flag`（行是否为历史回填）、`quarter_duration_days`（财季日历天数）不入候选。

### §0.2 更新频率与分布（文档级）

- **更新频率**：事件驱动，按 `Action_Date` 逐季（每个 metric 每季一行）；日频面板上由 `ts_backfill(…,252)` 携带。`data_backfill_flag` 标明历史回填行。
- **值域 / 形态（文档级，未跑 Labs 数值直方图）**：计数 0–12（右偏）；比率 0–100（近似正态或右偏）；指示器 0/1；`days_until_earnings_release` 整数、负值表示财报已过（锯齿状）；`forecast_consensus_surprise_percent` 描述写 0–100 但实为「模型−共识」差值，**实际可负**（同 `forecast_accuracy_advantage_percent` 的「负=更准」说明，两处 0–100 标注不可字面理解）。
- **可用性**：cov≈0.37 ⇒ 必须 `ts_backfill(…,252)`；覆盖不足以支撑 TOP3000 全截面时靠行业组内排名 + `nanHandling=ON`；首批需核 `longCount` 与 CW。

## §1 全字段画像（22/22）

| # | 字段 | 类型 | cov | uC | aC | 值域/形态 | 语义与信号面 | 可用性 |
|---|---|---|---:|---:|---:|---|---|---|
| 1 | `analyst_consensus_value` | VECTOR | 0.3804 | 2 | 2 | 金额（随 metric） | 街道/汇总分析师共识估计 | ❌ 单位混合，仅同 metric 内可用 |
| 2 | `analyst_yoy_change_percent` | VECTOR | 0.3690 | 9 | 9 | 0–100% | 共识估计的 YoY 变化（街道增长预期） | ✅ 增长预期水平 / 与模型增长做差 |
| 3 | `beat_precision_rate` | VECTOR | 0.3658 | 3 | 7 | 0–100 | 历史「beat 预测」的精确率 | ◐ 多头腿门控 |
| 4 | `composite_confidence_flag` | VECTOR | 0.3656 | 0 | 0 | 0–100 合成分 | 多模型分量合成置信度 | ◐ 门控；**uC/aC 双 0** = 社区完全未用 |
| 5 | `consensus_mape_percent` | VECTOR | 0.3784 | 18 | 32 | 0–100 | 共识 vs 实际的历史平均误差 | ◐ 质量门控；**全集中 aC 最高**，拥挤先验 |
| 6 | `data_backfill_flag` | VECTOR | 0.3804 | 1 | 1 | 0/1 | 该行是否历史回填 | ❌ 非信号 |
| 7 | `days_until_earnings_release` | VECTOR | 0.3804 | 11 | 12 | 整数，负=财报后 | Action_Date → 财报日天数 | ✅ 事件时点（`-abs` 邻近度） |
| 8 | `directional_accuracy_rate` | VECTOR | 0.3656 | 4 | 9 | 0–100 | 模型 beat/miss **方向**预测的历史准确率 | ◐ 门控（方向可信度） |
| 9 | `directional_confidence_flag` | VECTOR | 0.3696 | 1 | 1 | 0–100 | 「相对共识的方向」正确置信度 | ◐ 门控 |
| 10 | `forecast_accuracy_advantage_percent` | VECTOR | 0.3651 | 5 | 13 | 百分数，**负=模型更准** | 模型历史误差 − 共识误差 | ◐ 质量门控（越负越可信） |
| 11 | `forecast_beat_indicator` | VECTOR | 0.3804 | 2 | 2 | 0/1 | **模型预测高于共识**（不是公司实际 beat） | ✅ 核心方向（与 #14 成对） |
| 12 | `forecast_consensus_surprise_percent` | VECTOR | 0.3804 | 2 | 2 | 百分数，实际可负 | （模型点预测 − 共识）/ 共识 | ✅ 核心方向 + 幅度 |
| 13 | `forecast_mape_percent` | VECTOR | 0.3655 | 7 | 7 | 0–100 | 模型历史平均绝对误差 | ◐ 质量门控（越高越不可信） |
| 14 | `forecast_miss_indicator` | VECTOR | 0.3804 | 3 | 6 | 0/1 | **模型预测低于共识** | ✅ 核心方向 |
| 15 | `forecasted_yoy_change_percent` | VECTOR | 0.3690 | 6 | 8 | 0–100% | 模型预测的 YoY 增长 | ✅ 模型增长（与街道做差） |
| 16 | `miss_precision_rate` | VECTOR | 0.3565 | 3 | 3 | 0–100 | 历史「miss 预测」精确率 | ◐ 空头腿门控（覆盖率最低） |
| 17 | `model_confidence_flag` | VECTOR | 0.3654 | 4 | 5 | 0/1 | **模型−共识偏差 > 模型历史误差** | ✅ 本集独有的价值门控 |
| 18 | `numerical_confidence_flag` | VECTOR | 0.3651 | 3 | 5 | 0–100 | 预测幅度准确的置信度 | ◐ 门控 |
| 19 | `predicted_metric_value` | VECTOR | 0.3804 | 3 | 3 | 金额（随 metric） | 模型点预测 | ❌ 单位混合 |
| 20 | `prior_beat_count` | VECTOR | 0.3666 | 5 | 7 | 0–12 | **近 12 季公司实际 beat 共识次数** | ✅ 已实现 PEAD 强度 |
| 21 | `prior_miss_count` | VECTOR | 0.3666 | 1 | 1 | 0–12 | 近 12 季实际 miss 次数 | ✅ 负向不对称 |
| 22 | `quarter_duration_days` | VECTOR | 0.3804 | 4 | 4 | 整数 | 财季日历天数 | ❌ 非信号 |

**两个世界必须分开**（本集最容易犯的语义错误）：

- **已实现世界**：`prior_beat_count` / `prior_miss_count` = 公司过去 12 季**实际** beat/miss 共识 ⇒ 经典 PEAD 历史强度。
- **模型观点世界**：`forecast_beat_indicator` / `forecast_miss_indicator` / `forecast_consensus_surprise_percent` = **OdinUltra 模型与街道共识的分歧** ⇒ 量化模型的信息优势（或过度自信）。
- 两者同名异义，不可当成同一机制的两种测量面。

## §2 机制表

| 机制 | 经济陈述 | 字段 | 方向 | 拥挤先验 |
|---|---|---|---|---|
| **M1 已实现 PEAD 强度** | 连续多季 beat 共识的公司存在盈余漂移；beat−miss 净次数是强度代理 | `prior_beat_count − prior_miss_count` | + | 高（PEAD 经典、USA 最饱和） |
| **M1b 负向不对称** | 连续 miss 的负向漂移强于 beat 的正向漂移（损失厌恶 / 空头约束） | `prior_miss_count` | − | 中 |
| **M2 模型分歧方向** | 模型系统性高于共识 ⇒ 模型认为街道低估；若模型有信息优势，正向预测收益 | `beat_indicator − miss_indicator` | + | 低（本集独有） |
| **M2b 方向频率（论坛配方）** | 单次分歧的**方向**比幅度更有预测性；一年内净乐观频率是去噪后的模型观点 | `ts_mean(sign(surprise),252)` | + | 低 |
| **M3 分歧幅度** | 模型−共识的相对偏离幅度：若为过度自信则反向，若有信息则正向——先验由数据裁决 | `forecast_consensus_surprise_percent` | ?（首发测正向） | 低 |
| **M4 增长预期分歧** | 模型预测增长高于街道 ⇒ 增长重估空间；同单位百分比差，非跨信号相加 | `forecasted_yoy − analyst_yoy` | + | 中（增长族在 USA 饱和，但「模型−街道差」不饱和） |
| **M5 财报邻近度** | 财报公告溢价：临近公告日收益更高（Frazzini–Lamont） | `−abs(days_until_earnings_release)` | +（越近越高） | 中低 |
| **M6 置信门控** | 只有「偏差 > 模型自身历史误差」的模型分歧才值得下注 | `model_confidence_flag` × M2 | + | 极低（aC=5） |

## §2.1 批 1 设计（8 探针，6 机制）

**通用壳**（与 sustainable_profit / earnings_risk 同源，保证跨集可比）：

```
quantile(group_rank(winsorize(ts_backfill(<SIG>, 252), std=4), industry))
```

负向探针在壳外前置负号；VECTOR 一律**先 `vec_avg` 标量化再参与运算**（不用向量-向量算术，避免维度对齐风险）。

设置：USA / TOP3000 / D1 / **SUBINDUSTRY** / decay 5 / truncation 0.08 / VERIFY / nanHandling ON /
pasteurization ON / maxTrade OFF / validate_fields false。multisim 一批 8 条。

| # | 机制 | SIG（填入 <SIG>） | 方向 | 备注 |
|---|---|---|---|---|
| P1 | M1 | `vec_avg(prior_beat_count) - vec_avg(prior_miss_count)` | + | 净 beat 次数（−12…+12） |
| P2 | M1b | `vec_avg(prior_miss_count)` | − | 壳外前置负号 |
| P3 | M2 | `vec_avg(forecast_beat_indicator) - vec_avg(forecast_miss_indicator)` | + | 模型净乐观（快照方向） |
| P4 | M2b | `ts_mean(sign(ts_backfill(vec_avg(forecast_consensus_surprise_percent), 252)), 252)` | + | MY82844 论坛配方：只看方向频率 |
| P5 | M3 | `vec_avg(forecast_consensus_surprise_percent)` | + | 幅度/方向原始面，用于裁决过度自信 vs 信息优势 |
| P6 | M4 | `vec_avg(forecasted_yoy_change_percent) - vec_avg(analyst_yoy_change_percent)` | + | 模型增长 − 街道增长 |
| P7 | M5 | `-abs(vec_avg(days_until_earnings_release))` | + | 临近财报；壳内已是「越大越好」 |
| P8 | M6 | `ts_mean((vec_avg(forecast_beat_indicator) - vec_avg(forecast_miss_indicator)) * ts_backfill(vec_avg(model_confidence_flag), 252), 252)` | + | 只累计「偏差 > 模型历史误差」的方向 |

**预注册止损**（发批前固定，收批后不得改）：

1. 全批 `|S| < 1.0` ⇒ 判弱封存，不补批（同 earnings_risk / insiders4 / sustainable_profit 纪律）。
2. 任一机制 `|S| ∈ [1.25,1.58)` 且其余闸健康 ⇒ 该机制进 Mode A / 壳层加强（唯一允许的补批理由）。
3. 任一全闸候选 ⇒ 立即 `check_correlation(refresh=True)` 实测 prod；`[0.8,0.9)` n≥1 或 `[0.9,1]` n≥10 ⇒ 按 D0-P 判族级饱和，不磨参数。
4. **门控补批的条件前置**：只有 M2 方向（P3/P4）本身 `|S| ≥ 1.0` 时，才允许用 M6 门控做补批；若方向面本身无梯度，门控不作为补批理由。
5. 事件时点（M5）若 S 低但 `rns ≥ 0.5` ⇒ 登记为「低 S 高特异」慢腿，不在本集强行磨 S。

## §2.2 论坛与文献取证（2026-10-20 `search_forum_posts` / `read_forum_post` 实检）

| 来源 | 关键内容 | 对本集的意义 |
|---|---|---|
| 【Community Leader 💎】质而不邪，使用 ts_mean 在 analyst 数据集构造预测偏差因子（MY82844, 2025-12-04, 12 赞 / 9 评） | 在 analyst10 的 predicted-surprise 字段上，常规算子不过提交检验；**`ts_mean(sign(x), 252)` 只看方向、不看幅度**反而点亮绿钮（可作为 PPA+ATOM）。评论复证：`sign` 后按年计正负比例，忽略强度表现更好；极端值风险被消掉。改进方向：加 `group` / `signed_power` 提升 fitness。跨区提示：不同 region 需不同 backfill | **直接支撑 P4**：本集同样有「预测 surprise」字段，且幅度噪声大。P4/P5 构成方向频率 vs 幅度的对照。 |
| 【Alpha Idea】ASI 双字段组合：模型预测看同行，置信度看国家（JB71859, 2026-09-28, 31 赞） | 两个 `group_rank` 直接相乘（预测按 subindustry、置信度按 country），再 `ts_target_tvr_decay(target_tvr=0.028)`；实际 TO 5.80% ≠ 目标值。作者自省：`vec_sum` 混入「有效记录数」信息，必须用 `vec_avg` 对照；先缩尾再谈窗口 | ① **country 分组在 USA = 全市场**（USA 单国），不可照搬双分组；② 确认本批统一 `vec_avg`、先 `winsorize(std=4)`；③ `target_tvr` 不是最终 TO，本批不用该算子。 |
| 【Alpha灵感】通过 surprise 预测收益（QQ68782, 2025-01-12, 35 赞） | StarMine 的 `star_eps_surprise_prediction_fq1` / `star_rev_surprise_prediction_fq1` 是成熟预测型 surprise 机制 | 「预测 surprise」在社区是成熟路径；但 **StarMine EQ+ARM 已在 other685 判弱** ⇒ 同类先验存在天花板，必须靠本集独有的「模型 vs 共识」差异取胜，不能只做 surprise 复刻。 |
| 【数据集随笔】analyst14 分析师预期差的经济直觉（WL27618, 2026-09-13, 29 赞） | 超额收益核心 = **Earnings Surprise + 分析师集体修正动量**，而不是预测准确度本身 | 支撑 M2/M4（分歧与增长差），**弱化「准确率/置信度单独当信号」**；质量字段的正确定位是门控（M6），不是主信号。 |
| Growth Expectation Gap（WL27618, 2026-08-12, 30 赞） | StarMine 同时给「模型预测增长」与「隐含增长」，两者之差捕捉重估空间 | 与 M4 同构：**同一单位的两套增长预期之差**才可做，跨单位不可做。 |
| 文献：Bernard & Thomas (1989), *Post-Earnings-Announcement Drift* | 盈余意外后的价格漂移 | M1/M1b 的经典锚。 |
| 文献：Frazzini & Lamont (2007), *The Earnings Announcement Premium and Trading Volume* | 财报公告前存在正溢价 | M5 的经典锚。 |
| 文献：Abarbanell & Bernard (1992), *Tests of Analysts' Overreaction/Underreaction…* | 分析师对盈余信息反应不足 ⇒ 修正动量 | M2/M4 的行为金融锚。 |

**跨区警示**：以上只取**方法论与机制**，不取参数与阈值。`OdinUltra` 在本论坛检索 **0 命中** ⇒ 本集无社区现成配方，机制举证自行完成；USA 为最深最饱和市场，PEAD / 增长水平先验拥挤，prod 必须实测。

## §3 回测结果

### 3.1 批 1（multisim `4qyMOx37v4Ac8zhMRVUwDwl`，8/8 COMPLETE，2026-10-20）

设置：USA / TOP3000 / D1 / SUBINDUSTRY / decay 5 / trunc 0.08 / VERIFY / nan ON / pasteurization ON / maxTrade OFF。

| # | 机制 | alpha | S | F | 2Y | SUB | TO | ret | DD | rns | 失败闸 |
|---|---|---|---:|---:|---:|---:|---:|---:|---:|---:|---|
| P1 | M1 prior beat−miss | `Vkd363O5` | 1.20 | 0.88 | 1.22 | 0.76 | 3.79% | 6.78% | 13.15% | **1.07** | S / F / **CW 0.499992** / 2Y |
| P2 | M1b −prior miss | `JjPvxvdj` | **−1.27** | −1.02 | −1.24 | −0.59 | 3.66% | −8.01% | 60.08% | **−1.47** | S / F / CW / SUB / 2Y（**方向反**） |
| P3 | M2 模型净乐观（快照） | `npA8K8Ww` | 1.26 | 0.94 | 1.21 | 0.68 | 4.07% | 6.92% | 10.68% | **1.67** | S / F / 2Y |
| P4 | M2b 方向频率（MY82844 配方） | `omog6gYl` | 1.26 | 0.94 | 1.23 | 0.78 | **1.28%** | 6.96% | 10.55% | **1.76** | S / F / 2Y |
| P5 | M3 分歧幅度 | `O0Jxrx9J` | **1.39** | **1.05** | 1.34 | 0.68 | 3.87% | 7.17% | **9.18%** | **1.82** | S / 2Y |
| P6 | M4 模型−街道增长差 | `omog6gYJ` | 1.37 | **1.07** | 1.29 | 0.68 | 4.04% | 7.65% | 10.66% | **1.57** | S / **CW 0.2626** / 2Y |
| P7 | M5 财报邻近 `−abs(days)` | `O0Jxrx9d` | **1.46** | **1.19** | **1.36** | **0.89** | 4.21% | **8.37%** | 10.20% | **2.52** | S / 2Y |
| P8 | M6 置信门控方向频率 | `ZYmK0KpY` | 1.37 | **1.13** | 1.25 | **0.89** | **1.43%** | **8.56%** | 11.97% | **1.63** | S / **CW 0.499994** / 2Y |

**结论：0 颗全闸，但 6/8 落入 `|S| ∈ [1.25,1.58)` 且 rns ≥1.57** —— 触发 §2.1 预注册止损第 2 条（Mode A / 壳层加强），**不判弱、不换集**。

### 3.2 批 2（multisim `4sI2kWe3855MalXsv6Mqjjv`，8/8 COMPLETE，2026-10-20）

设置与批 1 完全一致（multisim 共享设置，杠杆全部落在表达式层）。

| # | 母体 / 杠杆 | alpha | S | F | 2Y | SUB | TO | ret | DD | rns | 失败闸 |
|---|---|---|---:|---:|---:|---:|---:|---:|---:|---:|---|
| Q1 | P7 + `ts_decay_linear(20)` | `wp9EZgMv` | 1.50 | 1.21 | **1.43** | 0.84 | 4.30% | 8.14% | **9.86%** | 2.40 | S / 2Y |
| Q2 | P7 仅公告前 `if_else(d>0,−d,0)` | `zqrR8ppK` | **−1.12** | −0.75 | −1.29 | −0.64 | 2.94% | −5.67% | 49.33% | −1.02 | S / F / SUB / 2Y |
| Q3 | P7 改 `subindustry` 分组 | `LL5dNJJe` | 1.46 | 1.16 | 1.37 | 0.87 | 3.78% | 7.86% | 10.26% | 2.52 | S / 2Y |
| Q4 | P5 + `ts_decay_linear(20)` | `1YjzXEEm` | 1.35 | 1.01 | 1.30 | 0.70 | 2.51% | 6.97% | 9.55% | 1.66 | S / 2Y |
| Q5 | P5 改 `ts_rank(...,504)` | `xA1d3ggN` | 1.22 | 0.88 | 1.22 | 0.59 | 5.26% | 6.54% | 10.07% | 1.65 | S / F / 2Y |
| Q6 | P5 × `directional_accuracy_rate` | `88vej11V` | 1.23 | 0.93 | 1.13 | 0.64 | 4.38% | 7.10% | 12.42% | 1.25 | S / F / **CW 0.499992** / 2Y |
| Q7 | P8 方向×`group_backfill(confidence)` + `ts_mean(252)` | `JjPvNKKA` | **1.58** | **1.33** | 1.28 | **0.93** | **1.22%** | **8.92%** | 11.00% | 2.27 | **仅 2Y**（其余全 PASS，CW 通过） |
| Q8 | P6 增长差先 `group_backfill` + `ts_decay_linear(20)` | `wp9EZgVx` | −0.05 | −0.01 | −0.57 | −0.26 | 5.51% | −0.15% | 9.73% | 0.08 | S / F / **CW 0.18329** / SUB / 2Y |

**相关性实测（`check_correlation(refresh=True)`，2026-10-20）**：`JjPvNKKA` prod **0.9146**（`[0.9,1]` n=4、`[0.8,0.9)` n=1305）；`wp9EZgMv` prod **0.9066**（`[0.9,1]` n=3、`[0.8,0.9)` n=1380）；对照批 1 的 P5 `O0Jxrx9J` prod **0.9050**（n=5 / 1491）。三条互不相同的机制全部落在同一相关簇。

## §4 归因

**A1｜本集与 sustainable_profit 是两类数据。** 6 条候选 `rns` 1.57–2.52（对照 sustainable_profit 全批 rns ≈0）⇒ 剥离风格后仍有特异信息。经济上合理：这些字段编码的是「模型与共识的分歧」「已实现 beat 历史」「财报时点」，不是价值/质量/规模 beta。**本集值得继续投入。**

**A2｜已实现 PEAD 的两条腿符号相反，净合被稀释。** P1（beat−miss）S1.20，而 P2（−miss）S**−1.27** ⇒ 近 12 季**miss 越多，后续收益越高**（困境反转 / 预期门槛低），与经典 PEAD 正向漂移相反；beat 腿的正向不足以抵消。这解释了 P1 为何弱于模型分歧族。可复用结论：**`prior_beat_count − prior_miss_count` 不是好构造，两条腿应分开建模**；本集不把 miss 反向作为主攻（其 DD 60.08% 且依赖反转 regime），仅登记。

**A3｜模型分歧三面同向且一致，幅度优于频率。** P3（方向快照）1.26 / P4（方向频率）1.26 / P5（幅度）**1.39** ⇒ ① 模型相对共识的乐观确实有预测性，不是过度自信；② 论坛「sign 只看方向更强」在本集**不复现**（幅度 1.39 > 频率 1.26）。但 P4 用 **1.28% 换手**拿到与 P3 相同的 S，margin 1.09% vs P3 0.34% ⇒ **频率化是干净的换手杠杆**，适合作为组合腿/门控底座。

**A4｜增长分歧与分歧幅度同族，量级相近。** P6（模型−街道 YoY 增长差）1.37 / rns 1.57，与 P5 1.39 接近 ⇒ 二者共享「模型相对街道更乐观」的同一信息核，后续不应作为两条独立腿同时投入（同族）。

**A5｜财报邻近度是全场最优，且风险中性后更强。** P7 S1.46 / F1.19 / SUB0.89 / DD10.20% / **rns 2.52** ⇒ 公告溢价机制在 USA 成立，且不是风险风格代理（rns 反而放大）。TO 4.21% 是它的主要代价，但 F 仍 >1。**这是本集最优先做壳层加强的机制。**

**A6｜置信门控改善「单位换手质量」，但引入集中度。** P8（只累计偏差>模型历史误差的方向）S1.37 / TO1.43% / rns1.63 ⇒ 门控把 P3 的 4.07% 换手压到 1.43% 且 S 更高。但 CW 0.499994（2017-01-06）⇒ 低覆盖字段（cov 0.365–0.367）在样本早期的**整段缺失**导致少数股票独占权重。

**A7｜CW 是数据覆盖问题，不是信号问题。** CW 只出现在 cov ≤0.3690 的字段（P1/P2/P6/P8），cov 0.3804 的字段（P3/P4/P5/P7）全部 CW 通过 ⇒ 需要的是覆盖修复（更长 backfill / 分组回填 / 换聚合），不是换机制。**修覆盖时不得引入跨数据集字段（ATOM）。**

**A8｜2Y Sharpe 1.21–1.36 是统一短板。** 全批 2Y 都低于 1.58，且与 rns 无关 ⇒ 更可能是 2022–2023 利率上行 regime 对盈利类因子的整体压制，而非单条构造失败。壳层加强应优先试：**decay/时序平滑**（提升稳定性）、**subindustry 分组**（与中性化口径一致）、**长窗 ts_rank 测量面**（适应 regime）。若三种都不动 2Y，则应判定为 regime 墙，不无限磨参。

**A9｜批 2 的杠杆归因：decay 是唯一有效的 2Y 旋钮，其余三种全败。** ① `ts_decay_linear(20)` 把 P7 的 2Y 1.36→**1.43**、S 1.46→1.50、DD 10.20→9.86（Q1）；② `subindustry` 分组**零增益**（Q3 1.46/1.37 ≈ P7）；③ `ts_rank(504)` 反而把 P5 的 S 1.39→1.22（Q7 长窗测量面不适用）；④ `group_backfill(..., industry, 252)` 把 P6 增长差从 1.37 **打成 −0.05**（Q8）——分组回填抹平了跨行业的增长差信息，**修覆盖不能无条件用 group_backfill**。⑤ 机制纯度检验：只保留公告前（Q2）翻成 **−1.12** ⇒ `−|days|` 的收益**不是** Frazzini–Lamont 公告前溢价，而是由**公告后邻近度**承载（公告后越近越强）。这是对 §2 机制叙述的更正。

**A10｜三条机制 prod 全部 0.905–0.915，数据集级饱和。** `JjPvNKKA` 0.9146、`wp9EZgMv` 0.9066、`O0Jxrx9J` 0.9050；三者分别代表「置信门控方向频率」「财报邻近」「模型分歧幅度」，经济含义互不相同，却撞在同一 `[0.8,0.9)` 1300–1500 条的生产簇上。⇒ **不是参数/窗口问题，是该数据集的信息已被社区广泛实现**（OdinUltra 模型−共识这一主题在 USA/D1 已被充分定价）。按 D0-P 判交付路径死。

**A11｜Q7 证明「单闸可修」，但修完也过不了 prod。** Q7 是本集唯一让 LOW_SHARPE 精确过线（1.58）的构造，且 TO 1.22%、F 1.33、SUB 0.93、CW 通过，只剩 2Y 1.28；即使把 2Y 修到 1.58，prod 0.9146 仍是硬墙。**可复用纪律：Mode A 的目标函数应是「三闸（S/F/2Y）中最后一条可修的闸」，在 prod 未测前不要为单闸投入整批；本集若先测 prod，可省下批 2 的 8 条。**

## §5 决策

- **❌ 交付路径封存：`USA-EQUITY-KPI-FORECAST-PROD-WALL`**（文档级；无 `forum_recon_*` 证据，不强行 `seal_dead_end`）。两批 16 条、6 机制，IS 已证明有真实特异信息（rns 1.57–2.52），但三条主线的 prod 全部 0.905–0.915 ⇒ 按 D0-P 判数据集级饱和。**不是判弱**，是「IS 强、prod 撞簇」。
- **不再发第 3 批**：2Y/ CW 的剩余杠杆（decay、subindustry、ts_rank504、group_backfill、accuracy 门控）已在批 2 逐一实测，除 decay 外全部无效或有害；即便全部修好，prod 墙仍在。
- **salvage（转 SUPER 组合腿候选）**：`JjPvNKKA`（S1.58/F1.33/TO1.22%/rns2.27）、`wp9EZgMv`（1.50/1.21/2.40）、`O0Jxrx9d`（1.46/1.19/rns2.52）、`O0Jxrx9J`（1.39/1.05/1.82）。组合层需另行实测 prod，不得据单腿数值推断。
- **可复用结论（已回写 §4 A9–A11）**：
  1. 本集 `ts_decay_linear(20)` 是 2Y 的唯一正向杠杆（+0.07），subindustry 组零增益，`ts_rank(504)` 与 `group_backfill(industry)` 有害；
  2. `−|days_until_earnings|` 的收益来自**公告后邻近度**，不是公告前溢价（仅公告前版本 −1.12）；
  3. **Mode A 前先测 prod**：单闸近线候选（Q7）投入前应确认其所在机制簇未饱和，否则 8 条批次买不到任何可交付物。
- **下一数据集（原因必须写明）**：本集交付路径已死且不再有未测杠杆 ⇒ 按用户「不得频繁换集，无计可施才换」的约束，换到剩余池中**拥挤度最低**的两集：`cre_exposure_model`（uC 3 / aC 3，2 字段）与 `other327`（uC 17–21 / aC 69–91，3 字段）。两集各 8 探针可**完整穷尽**（字段数 2–3），不属高频切换。`event_relation` 因 6/9 字段为分类整数码、ATOM 内无法做网络传播而降优先；`other567`（aC 544）与 `risk72`（pv47 同族 prod 饱和）押后。
