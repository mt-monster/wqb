# news_transformer_scores 字段画像与批次 22 预登记（USA / TOP3000 / D1）

as_of 2026-10-22　｜　平台：USA　｜　delay 1　｜　universe TOP3000
数据来源：`GET /data-fields?dataset.id=news_transformer_scores&region=USA&delay=1&universe=TOP3000`，全量 315 字段。

## 0. 数据集元信息与切换理由

| 项 | 值 |
|---|---|
| 数据集 id | `news_transformer_scores`（Sentiment 类别，**未点亮塔**） |
| 字段数 | **315（全部 MATRIX，无 VECTOR）** ⇒ 不需要 `vec_*` 聚合，单字段即可成 ATOM 腿 |
| 覆盖率 | 四档：**0.8810**（105 字段）/ 0.7586（63）/ 0.7585（42）/ **0.6923**（105）；全部 > 0.4，无需 `ts_backfill` 兜底 |
| 拥挤度 | 数据集 aC **292** / uC 140；但 **165 字段（52%）aC = 0**，拥挤集中在少数水平均值字段 |
| valueScore / multiplier | **5 / 1.4** —— USA sentiment 类 10 个数据集中 valueScore 最高的一档 |
| 语义 | Benzinga NewsQuantified 的 **transformer 情绪打分**：对盘前 / 盘中 / 盘后新闻逐条打分后聚合。三种极性（positive / negative / neutral）各有 105 个字段，覆盖均值、中位、峰谷、标准差、置信区间端点 |
| 是否点亮 | 未点亮（USA/D1 本季亮塔 = model 4 / analyst 1 / earnings 1） |
| 管线位置 | `pyramid = USA/D1/SENTIMENT`，multiplier 1.4 |

### 0.1 为什么在这里换数据集（过程约束「不得频繁切换」的留痕）

1. **上一个数据集已按预登记判死**：`order_flow_imb` 12 条腿（批次 20 的 4 条 + 批次 21 的 8 条）最高 S = 0.73 < 预登记的 1.00 苗子线，且 `risk_neutralized_sharpe ≤ 0.57` ⇒ 判 low-yield，见 [`_usa-order-flow-imb-field-profile-20261021.md`](_usa-order-flow-imb-field-profile-20261021.md) §5.3。
2. **本地库存已核**：`search_alphas_by_sharpe`（USA，min_sharpe 1.55，60 行）里 10 条 IS 全闸通过的记录**全部已是 ACTIVE**，没有可免费认领的未提交候选。
3. **Fundamental 库存已归零**：交付报告证 fnd67 / fnd93 / fnd91 / fnd1 / fnd2 / fnd21 全部判死或待封存，fnd22 于 2026-10-21 触发预登记判死线 ⇒ 缺口只能来自**未点亮塔的新机制**。
4. **为什么是 sentiment 而不是别的塔**：`get_datasets(category="news")` 在 USA 返回 **0 个**数据集（新闻类只能走 sentiment 类）；`get_datasets(category="sentiment")` 返回 10 个，其中本集 valueScore = 5 为最高，且 `news_sentiment_transfer`（23 字段）/ `sentiment22`（210 字段）保留为备选。
5. **本集相对已死族的正交性**：交付报告里曾经把 prod 顶到 0.72–0.83 的是 `positive_sentiment_probability_* − negative_sentiment_probability_*` 这类**水平极性差**（5 种中性化全在 0.72+）。本集的主攻面选在 **置信区间宽度 / 标准差（离散度）**，与「情绪水平」不是同一个信号概念。

## 1. 字段结构（315 = 3 极性 × 105）

### 1.1 三轴分解

| 轴 | 取值 | 说明 |
|---|---|---|
| **极性** | `positive` / `negative` / `neutral` | **各 105 个，完全对称**（同一套统计量在三种极性上各算一遍） |
| **统计量** | `average` / `mean_value` / `mean_score` / `typical_value` · `middle_value` / `middle_score` · `peak_value` / `peak_score` / `maximum` · `least_value` / `least_score` / `minimum` · `standard_deviation` / `dispersion` · `confidence_*` | 均值 / 中位 / 峰 / 谷 / 标准差 / 置信区间端点 |
| **窗口 / 时段** | base（259）/ `_post`（21）/ `_12`（19）/ `_pre5`（16）；另有数字后缀 `_2`…`_12` | 盘前窗口长度（小时）与盘后口径。**同一统计量在不同窗口下是不同字段**，这是自带的一组窗口网格 |

### 1.2 覆盖率分层（三档与极性无关，按窗口变）

| cov | 字段数 | 对应面 |
|---|---|---|
| 0.8810 | 105 | 盘前长窗（含 `_12` / `_pre5`） |
| 0.7586 / 0.7585 | 63 / 42 | 盘中 / 短窗 |
| 0.6923 | 105 | 盘后 `_post` 与短窗尾段 |

**所有档位都 > 0.4**，不需要 `ts_backfill` 兜底；但跨档换字段会同时换「覆盖样本」，读数不可直接横向比较（2026-10-21 fnd22 的轮换批正是栽在这一点上：覆盖率没变而字段变了，读数仍不可分辨）。

### 1.3 置信区间族（90 字段，本集的核心冷门面）

端点命名有 6 套同义写法：`confidence_floor` / `confidence_base`（下界）、`confidence_ceiling` / `confidence_upper` / `confidence_top`（上界）、`confidence_lower`（下界）。合计 **90 个字段**，逐字段 aC 见下（区间宽度 = 上界 − 下界）：

| 极性 | 端点家族 | aC 区间 | 代表字段（cov / aC） |
|---|---|---|---|
| positive | floor / lower | 0–6 | `positive_sentiment_confidence_floor`（0.881 / 1）、`positive_sentiment_confidence_lower_pre5`（0.881 / 2） |
| positive | ceiling / upper / top | 0–6 | `positive_sentiment_confidence_ceiling_12`（0.881 / 3）、`positive_sentiment_confidence_upper_7`（0.881 / 2） |
| negative | floor / lower | 0–5 | `negative_sentiment_confidence_floor`（0.881 / 5）、`negative_sentiment_confidence_lower_post`（0.692 / 1） |
| negative | ceiling / upper / top | 0–5 | `negative_sentiment_confidence_ceiling_4`（0.881 / 5）、`negative_sentiment_confidence_upper_12`（0.881 / 1） |
| neutral | floor / lower | 0–2 | `neutral_sentiment_confidence_floor_9`（0.759 / 2） |
| neutral | ceiling / upper / top | 0–2 | `neutral_sentiment_confidence_upper_2`（0.759 / 2） |

⇒ **CI 宽度是整张表最冷的一组可用面**（端点 aC 全是 0–6），且经济含义明确，不需要背包袱式回填。

## 2. 字段分型与机制映射（6 桶）

| 桶 | 字段 | 依据 | 表达式雏形 |
|---|---|---|---|
| **Dispersion（HIGH，主攻）** | `*_standard_deviation*`、`*_dispersion*`、**CI 宽度 = ceiling − floor** | 同一天多条新闻的**打分分歧**；分歧大 = 信息不一致 / 关注度低 | `ts_backfill(ceil − floor, 66)` → `group_rank` |
| **Change** | 同上做 `ts_av_diff` | 分歧的**变化**（情绪从一致转向分裂） | `ts_av_diff(stddev, 22)` |
| **Surprise** | `*_average_pre5` / `*_mean_score_12` | 情绪水平相对自身历史基线的偏离 | `ts_zscore(ts_backfill(avg,22), 252)` |
| **Level** | `*_average` / `*_middle_value` / `*_peak_value` | 原始情绪水平 | `group_rank(avg, subindustry)` |
| **Event-conditioned** | 用 stddev 高分位作门控 | 只在「新闻分歧异常日」交易 | `trade_when(ts_rank(stddev,252) > 0.8, …, -1)` |
| **Propagation** | — | 本集无跨资产 / 滞后结构，**本批不测** | — |

**经济机制假设（可证伪，双向预登记）**：

- **H1 分歧溢价（做空）**：CI 宽度大 ⇒ 市场对基本面解读不一致。Miller (1977) 的异议—卖空受限框架下，这类股票**被高估**，未来收益偏负 ⇒ 宽度取**负号**。
- **H2 关注度不足（做多）**：同一宽度也等于「报道条数少 / 措辞模糊」⇒ 低关注溢价（Merton 1987 的 neglected-firm effect），未来收益偏正 ⇒ 宽度取**正号**。
- **H1 与 H2 方向相反**，所以批次 22 对每个宽度家族**同时发正负两个号**，按读数判哪个先验在平台上成立（sign test，不做事后挑边）。
- **H3 标准差 ≠ CI 宽度**：`standard_deviation` 是逐条打分的样本离散，CI 宽度是**均值的不确定度**（∝ σ/√n）。若 H2 成立，两者应同号；若只有宽度有信号，说明驱动因素是**报道条数 n** 而不是分歧本身 —— 这是可分辨的机制指纹。

## 3. 批次 22：预登记（发批前写定，事后不得放宽）

**闸线（USA/D1）**：S ≥ 1.58；F ≥ 1.0；2Y ≥ 1.58；TO ∈ [0.01, 0.70]；SUB ≥ 0.43 × S；CW ≤ 0.1。
**prod**：只在 IS 全过后测（D0-P）；`<0.60` 正常，`0.60–0.70` 不做变体，`0.70–0.75` 只做一次结构化尝试，`≥0.75` 判死。

**本批要回答的问题**：

1. 置信区间宽度（离散度）在 USA/D1 上是否有**方向性**信息？若有，是 H1（负号）还是 H2（正号）？
2. 分歧族能否自然换手 > 12.5%（Fitness 地板）？新闻是**每日到达**的事件流，理论上换手应显著高于 fnd22 的 1–3%。
3. SUB 在 0.881 / 0.693 两档覆盖上是否自然过线？盘后 `_post` 档（0.6923）是否因样本更少而 SUB 更差？
4. `_12` / `_pre5` 窗口与 base 口径谁的读数更高 —— 盘前窗口长度是不是有效的第二维？

**预登记判死线**：若批次 22 的 8 条**无一**满足 `S ≥ 1.00 且 F ≥ 0.60`，则 `news_transformer_scores` 判 **low-yield**，第二批只做**字段轮换**（neutral 极性 / `_post` 盘后档 / `*_dispersion*` 同义面），不追加壳层；若轮换批仍全灭，则按统计族口径走 `seal_dead_end`（需 forum recon 闸 + 人工确认）。

**约束（用户铁律）**：禁 `add A,B` 混信号与混合权重调参；本批 8 臂全部**单表达式**，`ceiling − floor` 属同一统计量（置信区间）的两个端点，是一个信号而非两信号相加，满足 ATOM。

**发批设置**：两台 multisim（≤2 并发槽），USA / TOP3000 / D1，`decay 10`、`neutralization SUBINDUSTRY`、`truncation 0.08`、`unit_handling VERIFY`、`nan_handling ON`、`language FASTEXPR`、`pasteurization ON`、`max_trade OFF`。发批前已过 `preflight_expressions`（8 条全部 `valid`，`unknown_fields` 为空，`any_changed=false`）。

### 3.1 A 组（`4h8YHzca15iacvjQbhLTh9S`）：CI 宽度 × 双极性 × 双向

| 臂 | 机制 | 表达式 | alpha |
|---|---|---|---|
| A1 | Dispersion +（H2） | `quantile(group_rank(ts_backfill(positive_sentiment_confidence_ceiling_12 - positive_sentiment_confidence_floor_12, 66), subindustry))` | 待填 |
| A2 | Dispersion −（H1） | `quantile(group_rank(ts_backfill(-1 * (positive_sentiment_confidence_ceiling_12 - positive_sentiment_confidence_floor_12), 66), subindustry))` | 待填 |
| A3 | Dispersion +（H2） | `quantile(group_rank(ts_backfill(negative_sentiment_confidence_ceiling - negative_sentiment_confidence_floor, 66), subindustry))` | 待填 |
| A4 | Dispersion −（H1） | `quantile(group_rank(ts_backfill(-1 * (negative_sentiment_confidence_ceiling - negative_sentiment_confidence_floor, 66), subindustry))` | 待填 |

### 3.2 B 组（`3TMeCI6oY4rMcsQO6KlSYO3`）：标准差双向 + 水平对照 + 意外

| 臂 | 机制 | 表达式 | alpha |
|---|---|---|---|
| B1 | Dispersion（标准差，+） | `quantile(group_rank(ts_backfill(positive_sentiment_standard_deviation_pre5, 66), subindustry))` | 待填 |
| B2 | Dispersion（标准差，−） | `quantile(group_rank(ts_backfill(-1 * positive_sentiment_standard_deviation_pre5, 66), subindustry))` | 待填 |
| B3 | Level（对照） | `quantile(group_rank(ts_backfill(positive_sentiment_average_pre5, 22), subindustry))` | 待填 |
| B4 | Surprise | `quantile(group_rank(ts_zscore(ts_backfill(positive_sentiment_average_pre5, 22), 252), subindustry))` | 待填 |

- B3 是**对照臂**：如果它也强，说明读到的不是「分歧」而是「情绪水平」，与已死族同源；如果 B1/B2 强而 B3 弱，才是真分歧信号。
- B4 与 B3 同字段，只换壳（z-score 252 vs 原始水平），用于分辨「水平」与「意外」两个桶。

## 4. 批次 22 回测读数

**发批记录**：A = `4h8YHzca15iacvjQbhLTh9S`（A1–A4），B = `3TMeCI6oY4rMcsQO6KlSYO3`（B1–B4）；两批 8/8 COMPLETE，子任务状态 `WARNING` 只因「距每日仿真限额 452 次」提示，指标完整。

| 臂 | 机制 | 表达式 | alpha | S | F | 2Y | SUB | TO | RET | rns | 判决 |
|---|---|---|---|---|---|---|---|---|---|---|---|
| A1 | CI 宽度 +（H2） | `q(group_rank(ts_backfill(pos_ceil_12 − pos_floor_12, 66), subindustry))` | `KPmJz0zx` | 0.40 | 0.10 | 0.16 | 0.58 | 7.39% | 0.86% | **0.06** | FAIL |
| A2 | CI 宽度 −（H1） | 同 A1 取反 | `N1eNzwzp` | -0.41 | -0.11 | -0.94 | -0.44 | 7.47% | -0.94% | **-0.48** | FAIL |
| A3 | CI 宽度 +（H2） | `q(group_rank(ts_backfill(neg_ceil − neg_floor, 66), subindustry))` | `2rjA6065` | 0.39 | 0.11 | -0.05 | 0.83 | 7.88% | 1.01% | **0.19** | FAIL |
| A4 | CI 宽度 −（H1） | 同 A3 取反 | `RRAEz3zg` | -0.50 | -0.15 | -0.84 | -0.70 | 7.91% | -1.09% | **-0.58** | FAIL |
| B1 | 标准差 + | `q(group_rank(ts_backfill(pos_std_pre5, 66), subindustry))` | `E5V6zWWG` | 0.46 | 0.13 | 0.24 | 0.58 | 7.45% | 1.01% | **0.09** | FAIL |
| B2 | 标准差 − | 同 B1 取反 | `QPYvzkkW` | -0.45 | -0.13 | -0.96 | -0.37 | 7.52% | -1.05% | **-0.48** | FAIL |
| B3 | **Level 对照** | `q(group_rank(ts_backfill(pos_avg_pre5, 22), subindustry))` | `RRAEzQQo` | **-0.42** | -0.12 | -1.37 | -0.31 | 11.00% | -1.08% | **-0.37** | FAIL |
| B4 | Surprise | `q(group_rank(ts_zscore(ts_backfill(pos_avg_pre5, 22), 252), subindustry))` | `gJWeGOEO` | -0.02 | 0.00 | -0.27 | 0.11 | 10.88% | -0.05% | **-0.10** | FAIL |

### 4.1 归因

1. **判死线触发**：8 条最高 `|S| = 0.50`（A4 负向）/ 正向最高 0.46（B1），远低于预登记的 `S ≥ 1.00 且 F ≥ 0.60` ⇒ `news_transformer_scores` 首批 **无苗**。
2. **符号检验（本批唯一的机制结论）**：三个离散度家族（pos CI 宽度 / neg CI 宽度 / pos 标准差）**正向一致取正号**（+0.40 / +0.39 / +0.46），负号一致取负（−0.41 / −0.50 / −0.45）⇒ **H2（低关注 / neglected 溢价，做多高分歧）在方向上成立，H1（Miller 高估，做空高分歧）被证伪**。但幅度只有 0.4–0.5，是「方向对、强度不够」。
3. **`rns` 抹掉了大部分**：A1 0.06 / B1 0.09 / A3 0.19 ⇒ 离散度信号几乎全是风格暴露（小盘 / 低价 / 低流动性）。相对而言 **B3 水平的 rns = −0.37**（占 S 的 88%）说明**情绪水平本身才是"真"信号**，离散度只是它的一个噪声投影。
4. **B3 的符号是负的、且很强**：`positive_sentiment_average_pre5` 直接做多 → **S −0.42 / 2Y −1.37**。即「高正面情绪 → 未来跑输」，与情绪过度定价文献一致。其镜像（做空高正面情绪）S ≈ +0.42、rns ≈ +0.37 —— 是本批**唯一接近"残余 alpha"** 的腿，但仍只有 0.42，且该族是已证 prod 0.72–0.83 的人群面。
5. **换手全程低于 Fitness 地板**：8 臂 TO 7.4–11.0% 全 < 12.5%，按 `F = S·√(RET/max(TO,0.125))` 反推，F 0.10–0.13 完全由「S 只有 0.4 + RET 只有 1%」决定。**本集不是换手问题，是收益量级问题**，与 fnd22 同形。
6. **意外（B4）把信号打到零**（−0.02）：与 `pv63` 定律 12（流量型日频数据「水平 > 意外」）一致 —— 新闻情绪也是**状态量**，时序标准化会摧毁截面信息。

### 4.2 终判与轮换批取舍

预登记的第二批是「只做字段轮换（neutral 极性 / `_post` 盘后档 / `*_dispersion*` 同义面）」。按纪律本轮**不执行**该轮换，理由已写入预登记之外的可复核事实：

- 轮换只换字段、壳层固定，而**壳层对 S 是零位移**（交付报告定律 16/20 三度复证），字段轮换在本集的最佳预期是「A1/B1 同量级的另一个 0.4–0.5」；
- 三个独立家族（CI 宽度 ×2、标准差 ×1）在**同一壳层**下给出的 S 极差只有 0.07（0.39–0.46）⇒ 字段不是变量，机制才是；
- 该机制的强度上限已被 `rns ≤ 0.19` 限定为风格 beta。

⇒ `news_transformer_scores` 判 **low-yield（首批无苗，不再投入仿真）**；`seal_dead_end` 需 forum recon 闸 + 人工确认，本文件只作预登记。
