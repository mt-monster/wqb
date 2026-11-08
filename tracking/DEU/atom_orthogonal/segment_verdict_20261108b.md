# DEU ATOM 正交挖掘 — 本段判定台账（2026-11-08 · 段 B）

> 上游台账：`verdicts_wave_20261108.md`（段 A）、`segment_open_20261107.md`（主台账）
> 本文件记录：段 A 两批收割结果、全局互相关天花板、PV 塔开掘、论坛检索结论。

---

## 一、本段新判死（4 个目标）

### 1. `institutions6` 判死（批次 `JOQZ73Dj549aZX1dDIMqeBR`，8 条全 COMPLETE）

设置：SUBINDUSTRY / decay 9 / trunc 0.03 / TOP500 / D1

| alpha | 模板 | S | F | 2Y | TO | RA fail |
|---|---|---:|---:|---:|---:|---:|
| qMLVM1aK | 新鲜度门（ts_arg_max<66）+ 渗透率 ts_quantile 252 | **0.56** | 0.28 | **1.26** | 0.0680 | 4 |
| bl6Alkmm | 机构化率 = 机构市值/全体市值 | 0.25 | 0.08 | 0.92 | 0.0144 | 4 |
| 88RX8o0z | 净买/总活跃 =（buyers−sellers）/（buyers+sellers） | 0.17 | 0.05 | −0.06 | 0.0233 | 3 |
| omEZmpdn | 每股买入额 = 买入市值/（buyers+1） | 0.10 | 0.02 | **1.45** | 0.0210 | 3 |
| LLM3LjQe | 持有人数 ts_delta 252 | 0.09 | 0.02 | 0.05 | 0.0194 | 3 |
| d5Wv5XMw | 净买卖人数 / 持有人数均值 | 0.05 | 0.01 | −0.26 | 0.0224 | 3 |
| 1YN0Y9MX | 净买入天数占比（greater→ts_mean 252） | −0.18 | −0.05 | −1.04 | 0.0178 | 3 |
| YP1YPrVl | 美元净买入 / 机构总市值 | −0.24 | −0.08 | −0.23 | 0.0210 | 3 |

prescreen 8/8 REJECT。

**归因**：数据集本身干净（cov 1.0、11 字段全 MATRIX、ac 282 低拥挤），但**全部模板 S ≤ 0.56**，是「字段有数据、无预测力」的典型。
注意 `qMLVM1aK`（2Y 1.26）与 `omEZmpdn`（2Y 1.45）出现**S 与 2Y 反向背离** —— 近年有效、全期被早期拖死，
与 `VkxekE1w`（2Y 2.27 / S 0.26）同型。这是 DEU 的**结构性特征**：披露类数据只有近 2 年有信号。
⇒ **不能只看 2Y 判断机制成立**，DEU 必须双过 1.58。

**INSTITUTIONS 塔在 DEU 彻底封盘**：三个数据集全灭（institutions25 cov=0 / institutions1 最高 0.71 / institutions6 最高 0.56）。

### 2. `predictive_starmine` **revenue 族**判死（批次 `2zdYN22IN5cea6dx2CdmNHg`，8 条全 COMPLETE）

设置：基线 SUBINDUSTRY / decay 4 / trunc 0.08

| alpha | 模板 | S | F | 2Y | TO |
|---|---|---:|---:|---:|---:|
| JjerjmjO | `mean_estimate_change_pct_fy1_revenue_30d_5` ts_mean 22 | **0.79** | 0.43 | 0.69 | 0.0930 |
| rKR8KLKm | `mean_estimate_change_pct_f12m_revenue_7d_4` ts_mean 22 | 0.53 | 0.24 | −0.24 | 0.1163 |
| xAr5AQKW | 上调/下调修正计数净额 占比版 ts_mean 66 | 0.52 | 0.23 | 0.06 | 0.0453 |
| JjerjmjVl | 上调/下调修正计数净额 ts_mean 66 | 0.47 | 0.20 | −0.14 | 0.0396 |
| VkxekE1w | −`mean_estimate_price_ratio_f12m_revenue_5` ts_mean 66 | 0.26 | 0.09 | **2.27** | 0.0174 |
| 2rAerRr6 | `predicted_surprise_pct_f12m_revenue_4` ts_mean 22 | 0.22 | 0.06 | −0.20 | 0.0651 |
| npvrpoxa | `arm_revenue_component_score_3` ts_mean 22 | 0.18 | 0.05 | −0.91 | 0.0394 |
| xAr5AQOq | `smest_growth_next_vs_this_yr − vs_last_yr` 加速 | −0.27 | −0.09 | −0.26 | 0.0729 |

prescreen 8/8 REJECT。

**归因**：revenue 族 8 个独立语义面（修正计数 / 修正幅度 7d / 30d / 营收超预期 / 估值比 / ARM 评分 / 增长加速）**无一过 0.8**。
与已交付件的 earnings 族（QPvzNNGG S 1.70）形成鲜明对照 ⇒ **同一数据集内部不同财务口径的信号强度极不对称**。
⇒ `predictive_starmine` 真正能出货的只有 `mean_estimate_change_pct_f12m_earnings_14d_4` + `predicted_surprise_f12m_ebitda_4` 这一对腿，
**不构成第 4 颗**。该数据集容量到顶 = 3 颗（对应已交付 QPvzNNGG / LLMzYrZe + E56pROb9 的模型腿）。

### 3. `macro27` 判死
cov **0.0**（13 字段，ac 165）。MACRO 塔在 DEU 只有这 1 个数据集 ⇒ **MACRO 塔整塔无数据**。

### 4. `imbalance5` 判死
cov **0.0**（2 字段，ac 144）⇒ **IMBALANCE 塔整塔无数据**。

**DEU 全字段 cov=0 判死清单累计 10 个**：`event_ml_signals`(104) / `risk72`(31) / `socialmedia12`(18) / `earnings6`(18) / `earnings_sent_matrix`(7) / `risk68`(5) / `risk71`(10) / `institutions25`(24) / **`macro27`(13)** / **`imbalance5`(2)**。

---

## 二、★★★ 关键结构性发现：DEU 现有成品的互相关天花板 = 5

对 5 颗合格件 + 6 颗备用件共 11 颗跑 `compute_mutual_correlation`（years=3，782 个点）：

```
max_mutually_below_subset = [LLMzYrZe, mLox6Mg2, MPY9VNY9, E56pROb9, QPvzNNGG]
max_mutually_below_subset_size = 5
max_subset_exact = true          ← 已是最优解，不是启发式近似
```

10 对超 0.7 的冲突：

| 对 | 相关 | 冲突块 |
|---|---:|---|
| mLox6Mg2 ↔ QPveY7Kg | **0.9921** | 情绪块 |
| MPY9VNY9 ↔ npvwXA8l | **0.9198** | 做空块 |
| A1Vvqded ↔ QPveY7Kg | 0.9182 | 情绪块 |
| mLox6Mg2 ↔ A1Vvqded | 0.9095 | 情绪块 |
| Vkx3MjW8 ↔ Xg9WNVvl | 0.8644 | 模型-mdl264 块 |
| wpQYNvZp ↔ Xg9WNVvl | 0.8278 | 模型块 |
| wpQYNvZp ↔ Vkx3MjW8 | 0.7852 | 模型块 |
| LLMzYrZe ↔ wpQYNvZp | 0.7319 | 跨数据集模型块 |
| LLMzYrZe ↔ Vkx3MjW8 | 0.7098 | 跨数据集模型块 |
| LLMzYrZe ↔ Xg9WNVvl | 0.7075 | 跨数据集模型块 |

**结论**：
1. **备用池 6 颗没有任何一颗能加入现有 5 颗** —— 不是「暂时不入账」，是数学上不可能。之前把 wpQYNvZp / Vkx3MjW8 等当「备用可补缺口」的判断必须作废。
2. DEU 信号空间目前只张成 **3 个独立维度**：SENTIMENT、MODEL 修正链、SHORTINTEREST。
3. `LLMzYrZe ↔ wpQYNvZp 0.7319` 跨两个数据集仍超 0.7 ⇒ 印证记忆「共用一条腿就足以把互相关顶到 0.84」，且**跨数据集的同机制腿同样共用**。
4. 要凑到 10 颗，**必须新开 ≥5 个独立维度**，没有存量捷径。

---

## 三、DEU 塔点亮表（`get_pyramid_alphas`，只统计已提交件）

| 塔 | D1 已提交 | 状态 | 可否开采 |
|---|---:|---|---|
| **pv** | **0** | 未点亮 | ✅ 优先 |
| risk | 0 | 未点亮 | ✅（RISK60-B 在飞） |
| earnings | 0 | 未点亮 | ⚠️ 仅 2 个数据集且 cov=0 |
| news | 0 | 未点亮 | ⚠️ news18 已判死 |
| macro | 0 | 未点亮 | ❌ cov=0 |
| socialmedia | 0 | 未点亮 | ❌ cov=0 |
| insiders | 0 | 未点亮 | ⚠️ insider_matrix 死，仅 insiders1 未测 |
| imbalance | 0 | 未点亮 | ❌ cov=0 |
| option | 0 | 未点亮 | 未查 |
| institutions | 1 | 未点亮 | ❌ 三数据集全灭 |
| model | 1 | 未点亮 | 饱和（容量 3 颗已满） |
| sentiment | 1 | 未点亮 | 块内饱和 |
| fundamental | 1 | 未点亮 | 未系统测 |
| analyst | 2 | 未点亮（近点亮） | ⚠️ analyst93 已死 |
| other | 2 | 未点亮 | 未系统测 |
| shortinterest | 2 | 未点亮（近点亮） | ✅ MPY9VNY9 已出 |

---

## 四、新开维度：`pattern_scores`（PV 塔，cov 0.9888）

### 为什么选它
- DEU PV 塔 **0 颗已提交**（未点亮），符合「已点亮塔不选」约束。
- coverage **0.9888**，504 字段，**alphaCount 仅 277 / userCount 165** —— 对 PV 类数据集是极低拥挤度。
- 单字段 alphaCount 多为 0–7，大量 virgin 字段（如 `asc_triangle_std_simscore_lookback60` ac=0）。
- 技术形态与既有三个维度（情绪 / 分析师修正 / 做空）**天然正交**。

### 字段命名规则（三种族）
```
族A  {pattern}_{stat}_simscore_lookback{60|120}
     stat  ∈ {mean, max, min, std, median, q95, dynamic}
     已确认 pattern：asc_triangle / asc_triangle_down / breakaway_gap_up / breakaway_gap_down
                    common_gap_up / common_gap_down

族B  avg_similarity_{描述名}[_120]
     已确认：upward_breakaway_gap / downward_breakaway_gap /
             upward_symmetrical_triangle / downward_symmetrical_triangle /
             falling_wedge_pattern / rising_wedge_pattern /
             continuation_falling_wedge / continuation_rising_wedge /
             falling_support_flat_resistance / rising_support_flat_resistance /
             downward_price_gap_pattern / v_reversal_bottom / v_continuation_top

族C  adaptive_similarity_{描述名}[_120]
     已确认：upward_breakaway_gap_120 / upward_gap_pattern
```

### 覆盖率参照
- `_120` 尾缀版：cov **0.9917**
- lookback120 版：cov **0.9917**
- 无尾缀 / lookback60 版：cov **0.9647 / 0.9991**

---

## 五、PATTERN-A 波次设计（已派发 `y2tyaePx5dEcBzO5M2MuNx`，10 条）

设置：基线 SUBINDUSTRY / decay 4 / trunc 0.08 / TOP500 / D1

| # | 模板 | 设计机制 | 算子数 |
|---|---|---|---:|
| 1 | `group_rank(subtract(common_gap_up_mean_simscore_lookback120, common_gap_down_mean_simscore_lookback120), sector)` | 缺口方向共识（普通缺口向上 vs 向下） | 3 |
| 2 | `group_rank(subtract(avg_similarity_falling_wedge_pattern_120, avg_similarity_rising_wedge_pattern_120), sector)` | 楔形反转不对称（下降楔=看涨 / 上升楔=看跌） | 3 |
| 3 | `group_rank(subtract(avg_similarity_v_reversal_bottom_120, avg_similarity_v_continuation_top), subindustry)` | V 形反转底 − V 形顶部延续 | 3 |
| 4 | `group_rank(subtract(avg_similarity_upward_symmetrical_triangle, avg_similarity_downward_symmetrical_triangle), sector)` | 对称三角形突破方向偏置 | 3 |
| 5 | `-group_rank(ts_mean(asc_triangle_std_simscore_lookback60, 22), sector)` | **形态歧义度折价**（二阶方差：形态识别不稳定 ⇒ 噪声 ⇒ 减分） | 3 |
| 6 | `group_rank(subtract(asc_triangle_max_simscore_lookback120, asc_triangle_mean_simscore_lookback120), subindustry)` | **形态尖峰度**（极差：单日强匹配 vs 均值） | 3 |
| 7 | `group_rank(subtract(asc_triangle_dynamic_simscore_lookback120, asc_triangle_mean_simscore_lookback120), sector)` | **形态形成动量**（近端加权 − 等权，信息加工方式差异） | 3 |
| 8 | `group_rank(subtract(asc_triangle_mean_simscore_lookback60, asc_triangle_mean_simscore_lookback120), sector)` | **跨周期一致性**（双视界 60d − 120d） | 3 |
| 9 | `group_rank(subtract(breakaway_gap_up_q95_simscore_lookback60, breakaway_gap_down_q95_simscore_lookback60), sector)` | **尾部形态强度**（q95 分位算子，上缺口 − 下缺口） | 3 |
| 10 | `group_rank(subtract(adaptive_similarity_upward_breakaway_gap_120, avg_similarity_downward_breakaway_gap_120), subindustry)` | 自适应加权族净压力 | 3 |

**模板互异维度**：矩（水平 / 一阶差分 / 二阶方差 std / 极差 max−mean / 分位 q95）、
信息加工（等权 vs 动态加权 vs 双视界）、方向构造（跨形态差值 vs 时序偏离）、分组轴（sector / subindustry）。
全部算子数 3 ≤ 12。

**preflight**：17 字段中 16 通过；`asc_triangle_std_simscore_lookback120` 不存在（词表里是 `..._lookback60`），已修正。

---

## 六、论坛检索结论（机制前置，用户流程要求）

检索词：`chart pattern similarity 形态 技术形态 pattern_scores 图表模式 相似度 alpha 模板`

### 命中 1：`【AlphaIdea】K线形态Peak统计量的做空因子化 — ASI市场技术反转Alpha`（YZ29225，2026-09-07）
> `continuation_score` 数据集的生产级实现思路。560 个技术形态相似度字段，MATRIX 类型极稀有（仅 1 位用户提交过 alpha，覆盖率 1.0）。核心发现是该数据集中 **peak 统计量**……

**可复用**：形态的 **Peak 统计量应做空因子化** ⇒ `max_simscore` 类字段方向偏**负**（形态匹配到峰值后反转）。
本波 #6 的 `max − mean` 我需要留意方向可能应取负。

### 命中 2：`【Alpha Idea】看跌矩形做空中空 + 上升通道做多的跨数据集组合`（YZ29225，2026-09-08）
> 传统技术分析中「矩形形态」需人工判断。BRAIN 通过算法自动识别每种形态的相似度（0~1）：① **量化与一致性**——将主观形态判断转化为客观数值，消除人为偏差……

**可复用**：形态相似度是**主观判断的客观化**，其 alpha 来源是「散户按形态交易造成的可预测流」。支持族B 的方向性构造。

### 命中 3：`CHN Python Alpha 踩坑实录`（LQ99002，9 赞 / 18 评论）
> `..._similarity_cup_and_handle_similarity_maximum_h60` / `recent_similarity_inverse_cup_handle`
> 经济学（一句话）：**逆杯柄形态相似度在峰值相对近期基线「过度延伸」后均值回归**

**可复用（下一波 PATTERN-B 首选）**：`subtract(max_simscore_W, ts_mean(simscore, shortW))` = 峰值相对近期基线的**时序过度延伸** ⇒ 均值回归（取负）。
与我本波 #6 的横截面 `max − mean`（同窗口内）**不同**：论坛版是**时序**偏离，需两个不同窗口。

### 命中 4：`【Alpha Idea】CNN预测分歧度的年度偏离信号（GLB）`（QQ38141，2026-09-28）
> 预测分布的**宽度** = 模型对这只股票的「不确定性读数」。第五分位和第一分位离得很远 ⇒ 同时读出强烈多空两种可能 ⇒ 它「拿不准」；两个分位收得很拢 ⇒ 形态指向明确。

**可复用（PATTERN-B 首选）**：用 **`q95 − min`（或 q95 − q5）作为分歧宽度**，比 std 更稳健（抗单点极值）。
pattern_scores 有 `q95` 字段（`breakaway_gap_up_q95_simscore_lookback60` 已确认存在）。
本波 #5 用 std 是初版，PATTERN-B 应换成 `subtract(q95, min)` 或 `subtract(max, q95)` 的右尾集中度。

### 命中 5：`10个超级高效好用的ARC/GLB模板`（CQ89422，146 赞 / 68 评论）
> 十个模板家族，按使用频率排序。`F1a — vector_neut / ts_arg_min 主模板（比较高效）`

**可复用**：`F1a` 主模板 = `vector_neut` / `ts_arg_min` 骨架。可作 PATTERN-B 的模板补充来源。

---

## 七、PATTERN-B 预设计（尚未派发，PATTERN-A 收割后定稿）

方向 1（论坛#3 时序过度延伸）：`-group_rank(ts_zscore(subtract(asc_triangle_max_simscore_lookback120, ts_mean(asc_triangle_mean_simscore_lookback120, 22)), 252), sector)`

方向 2（论坛#4 分歧宽度右尾）：`-group_rank(subtract(asc_triangle_max_simscore_lookback120, asc_triangle_q95_simscore_lookback120), sector)`
※ 需先确认 `asc_triangle_q95_simscore_lookback120` 是否存在（词表只确认了 `breakaway_gap_*_q95_simscore_lookback60`）。

方向 3（论坛#1 peak 做空）：`-group_rank(ts_rank(breakaway_gap_up_max_simscore_lookback120, 252), sector)`

方向 4（论坛#5 F1a）：`group_rank(ts_arg_min(ts_backfill(avg_similarity_v_reversal_bottom_120, 22), 66), sector)` —— 距最近一次强 V 反转形态的天数

---

## 八、本段新增工具坑

```text
// get_pyramid_alphas 返回的是「已提交」计数，UNSUBMITTED 件不计入。
// ⇒ 手上 5 颗全闸通过件提交后，DEU 塔点亮表会整体抬升，届时要重算选集约束。
```

```text
// compute_mutual_correlation 的 max_mutually_below_subset 是精确解（max_subset_exact=true 时）。
// 判「能不能再加一颗」不要自己枚举组合，直接读 max_mutually_below_subset_size。
```

```text
// pattern_scores 的 std 族存在 _lookback60 但没有 _lookback120（asc_triangle）。
// ⇒ 同族字段的窗口可用性不齐，必须靠 preflight 的 unknown_fields 逐个验，不能按命名规则外推。
```

```text
// DEU 存在「S 低但 2Y 极高」的反向背离型字段（VkxekE1w S0.26/2Y2.27、qMLVM1aK S0.56/2Y1.26、omEZmpdn S0.10/2Y1.45）。
// 这类件不能因 2Y 高就判机制成立 —— DEU 是双过线（S≥1.58 且 2Y≥1.58），单项高无意义。
```
