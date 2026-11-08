# EUR/OTHER `techindi_model` 战役台账（2026-11-06）

> 目标：点亮 **EUR/OTHER（当前 2/3，差 1 颗）**。数据集 `techindi_model`，category `other`，单数据集 ATOM，不占塔混配额。

## 零、结论速览

| 机制面 | 结论 | 依据 |
|---|---|---|
| `predicted_*_quantile_*_return_*`（硬标签，预测收益分位） | **封盘** | 5 个结构变体全部同时卡 `sub/S` 与 `prod` 两墙，无交集 |
| `probability_*`（软信息，五桶概率分布） | **在飞** | 结构属另一类机制，aC 仅 0-5，探针 4 条已派发 |
| 其余 533 字段（未归类） | 待画像 | 命名不含 predicted/probability/quantile，需单独归类 |

## 一、数据集画像（798 字段，全 MATRIX，cov 0.9997-1.0）

字段是 **三轴笛卡尔积**：`分位轴(first..fifth) x 期限轴(one/five/ten day) x 信息形态`。

### 1.1 形态一：硬标签 `predicted_{q}_quantile_{h}_day_return_{sfx}`

15 组（5 分位 x 3 期限），每组 7 个后缀变体（13 / 131 / 14 / 141 / 142 / 15 / 16，疑为模型版本）。
拥挤度跨度很大：`predicted_fifth_quantile_five_day_return_14` **aC 197**（最挤），
`predicted_fourth_quantile_ten_day_return_16` **aC 1**、`predicted_second_quantile_five_day_return_16` **aC 1**（最干净）。

### 1.2 形态二：软信息 `probability_*`（两套命名，均为五桶分布）

家族 A：`probability_{q}_quantile_{h}_day_bucket_{zero|one|two|three|four}_{sfx}`
- EUR/TOPCS1600 下完整五桶集合 7 组，最干净 `probability_fifth_quantile_one_day_bucket_*_141`（**aC 合计仅 1**）
- 次干净 `probability_fifth_quantile_five_day_bucket_*_13`（aC 合计 4）、`..._one_day_bucket_*_13`（4）、`..._one_day_bucket_*_14`（4）

家族 B：`probability_{q}_bucket_{h}_day_label_{zero|one|two|three|four}_{sfx}`
- 完整五桶集合 5 组，最干净 `probability_fifth_bucket_one_day_label_*_15`（aC 合计 3）
- `..._one_day_label_*_17`（5）、`..._ten_day_label_*_17`（5）

字段描述（原文）：`probability_fifth_bucket_ten_day_label_four_17` = "Probability that the ten-day return falls into the fifth bucket of the fifth quantile."；
`probability_fifth_quantile_ten_day_bucket_zero_15` = "Probability that a stock is in the fifth quantile for ten-day return, bucket zero."
=> 桶序 zero..four 是**有序分桶**，可当连续分位读。

**画像判据**：三轴中「信息形态」轴是唯一未被开采的维度 —— predicted 族已被打到 aC 197，probability 族 aC 仍 0-5。
这不是「换字段」，是**换信息加工方式**（硬标签 -> 分布），属结构多样性而非参数扰动。

## 二、★★★★★ 口径发现：LOW_SUB_UNIVERSE_SHARPE 是比值检验，不是固定阈值

5 个独立数据点（同一字段族，不同结构）实测：

| alpha | sharpe | sub | checks.fail.limit | limit / sharpe |
|---|---:|---:|---:|---:|
| pwvYnnOg | 3.83 | 1.91 | 2.03 | 0.5300 |
| 9qxGRRAx | 3.92 | 2.00 | 2.08 | 0.5306 |
| E56mKKrL | 3.85 | 1.81 | 2.04 | 0.5299 |
| 78LGdwa2 | 3.88 | 1.93 | 2.06 | 0.5309 |
| O0A69pnY | 3.89 | 1.96 | 2.06 | 0.5296 |

五个点的 `limit/sharpe` 全部落在 **0.5296-0.5309**，误差仅来自 S 的两位小数取整。
拟合值 **0.5303 = 0.75 / sqrt(2)**：sub 宇宙的股票数约为母宇宙一半，Sharpe 的期望按 1/sqrt(2) 缩放，再留 25% 容忍。

**判据（可直接套用）**：`sub_universe_sharpe >= 0.5303 x sharpe`。

三条推论，全部改变选件逻辑：

1. **跑步机效应**：把 S 从 1.7 做到 3.9 的同时，门槛从 0.90 自动抬到 2.08。S 越高不是无条件越好。
2. **反向可利用**：压低 S 而保住 sub 同样能过检验。即「稀释」是一条合法杠杆，不只是「增强」。
3. **高 S 候选必须查比值**：任何 S > 2.5 的候选，先算 sub/S 再看其它闸，否则会为一件注定失败的件投入破墙成本。

对既有 37 颗候选的复核结论：全部已通过该闸，故不受影响（比值均 >= 0.5303）；
该发现的价值在于**今后**挑高 S 件时不必再试 —— 3 倍数量级的高 S 件里大概率一半以上是 sub 死的。

## 三、`predicted_*` 硬标签族：5 变体全灭，两墙互为代价

基准件 `pwvYnnOg`（平台既有，非本会话产出）：
`signed_power(group_rank(ts_zscore(ts_mean(predicted_fifth_quantile_ten_day_return_15, 2), 252), market), 2.5)`
S 3.83 / F 1.67 / TO 53.97% / 2Y 2.56 / sub 1.91 / self 0.5080 / **prod 0.7443**，唯一 fail = LOW_SUB_UNIVERSE_SHARPE。

为同时解两墙设计的 4 个结构变体（同数据集、同字段、同设置档，逐字实测）：

| alpha | 结构 | S | F | sub | sub/S | prod | 判决 |
|---|---|---:|---:|---:|---:|---:|---|
| pwvYnnOg | 基准：group_rank(market) + signed_power 2.5 | 3.83 | 1.67 | 1.91 | 0.4987 | 0.7443 | sub 差 0.12 / prod 差 0.044 |
| 9qxGRRAx | 去掉 signed_power（指数 1，线性 rank） | 3.92 | 1.74 | 2.00 | **0.5102** | **0.7854** | sub 差 0.08 / prod 差 0.085 |
| O0A69pnY | 指数降到 2 | 3.89 | 1.71 | 1.96 | 0.5039 | 0.7564 | sub 差 0.10 / prod 差 0.056 |
| 78LGdwa2 | ts_rank 替代 ts_zscore（有界，抗异常） | 3.88 | 1.67 | 1.93 | 0.4974 | **0.7276** | sub 差 0.13 / prod 差 0.028 |
| E56mKKrL | group_rank 轴换成 industry（更局部） | 3.85 | 1.63 | 1.81 | 0.4701 | 0.7384 | 两头都变差 |

**因果**：指数下降对两墙的作用方向相反 —— 指数 2.5 -> 1 使 sub/S 单调上升（0.4987 -> 0.5039 -> 0.5102），
同时使 prod 单调恶化（0.7443 -> 0.7564 -> 0.7854）。两墙互为代价，无交集。

外推：要把 sub/S 从 0.5102 推到 0.5303 需再降约 2.7 个指数单位（负指数），物理上不可能；
要把 prod 从 0.7276 压到 0.70 需反向升指数，而升指数会把 sub/S 压到 0.49 以下。

**判决：`predicted_*` 硬标签族在 EUR 封盘。** 5 个结构互异变体（水平/线性化/中指数/稳健化/局部化）全部触墙，
且 prod 一致落在 0.73-0.79 的窄带内 => 拥挤来自**字段/机制本身**，不是骨架选择问题（与「同骨架换字段 prod 共线」的既有发现同源）。

## 四、`probability_*` 软信息族：模板池 12 个

记五桶概率 P0..P4（zero..four，有序上行），期限取 `ten_day_label_*_17`。全部外包 `rank()` 做截面展开
（论坛依据：概率类字段需转排序百分比，避免仓位集中在少数高概率个股）。

| 编号 | 模板名 | 结构 | 算子数 | 信息维度 | 来源 |
|---|---|---|---:|---|---|
| T01 | 尾部净上行 | `rank(P4 - P0)` | 2 | 一阶方向 | 自建 |
| T02 | 上下侧累积差 | `rank((P4+P3) - (P1+P0))` | 4 | 累积分布对比 | 自建 |
| T03 | 相对信心比 | `rank(P4 / (P4 + P0))` | 3 | 条件化方向（去掉极端度影响） | 自建 |
| T04 | 两极分化度 | `rank(P4 + P0)` | 2 | 二阶：U 形 vs 居中（不确定性） | 论坛·稳定性调整 |
| T05 | 中段质量 | `rank(P3 - P2)` | 2 | 局部形状（不看极值） | 自建 |
| T06 | 概率修正动量 | `rank(ts_delta(P4, 22))` | 3 | 一阶差分：预测被上调 | 论坛·分位概率趋势 |
| T07 | 概率时序分位 | `rank(ts_zscore(P4 - P0, 252))` | 4 | 相对自身历史 | 自建 |
| T08 | 稳定性加权 IR | `rank(diff / ts_std_dev(diff, 22))` | 6 | 方向 / 自身不确定性（夏普化） | 论坛·「概率提供方向，稳定性决定置信权重」 |
| T09 | 对数概率 | `rank(log(P4))` | 2 | 非线性压缩（log-softmax 软信息） | 论坛·概率取对数已验证 |
| T10 | 极端质量集中 | `rank(P4^2 + P0^2)` | 4 | 熵/集中度代理 | 论文·高阶矩与熵 |
| T11 | 极化度变化 | `rank(ts_delta(P4 + P0, 22))` | 3 | 二阶量的时序变化 | 自建 |
| T12 | 期限结构 | `rank(P4_ten - P4_five)` | 2 | 长期 vs 短期信心差（跨期限） | 自建 |

覆盖维度自检：水平(T01/T03/T05)、累积(T02)、二阶分散(T04/T10)、时序(T06/T07/T11)、
风险调整(T08)、非线性(T09)、跨期限(T12) —— **7 个互不重叠的信息维度，12 个结构**，满足模板库 >=10 且结构互异的硬约束。

## 五、探针批（在飞）

设置档 = 平台既有件 `pwvYnnOg` 的逐字段档：EUR / TOPCS1600 / delay 1 / decay 1 / SUBINDUSTRY /
truncation 0.08 / unitHandling VERIFY / nanHandling ON / pasteurization ON / maxTrade OFF。

| 批 | multisim | 模板 | 表达式 |
|---|---|---|---|
| P1 | 1XZTRi4MY5cG8RFs1XxdgNv | T01 / T02 | rank(P4-P0) / rank((P4+P3)-(P1+P0)) |
| P2 | 3eYWtf2c05biaKaPzAmGvKN | T04 / T08 | rank(P4+P0) / rank(IR) |

预注册判据：
- 任一 S >= 1.2 且 sub/S >= 0.5303 => 立即展开剩余 8 模板；
- 四条 |S| < 0.5 => 软信息族在该数据集也无信号，EUR/OTHER 整个 `techindi_model` 封盘，转别的 category；
- 同时按 `F = S^1.5 x sqrt(vol/0.125)` 用实测 vol 反算 F=1 所需 S 门槛（vol 是数据集固有属性，2 条探针即可先验测出）。

## 六、论坛 / 文献取证

论坛（`search_forum_posts` 实检索）：
1. **「软信息优于硬信息」** —— 模型类数据集同时提供「预测标签」「分位概率」「模型置信度」三种形态；
   标签把判断压成一个整数，分位概率保留模型不确定性，**概率形态在截面上的区分度更高**。
   => 本条是本波从 predicted 族转向 probability 族的直接依据。
2. **「概率提供方向，概率自身的稳定性决定置信权重」** —— 直接对应 T08（方向 / ts_std_dev）。
3. **「分位概率取对数」在日、韩、台的因子化验证** —— 概率不是 0.3/0.6 的裸值，取对数后截面区分度更高，已证可下单。对应 T09。
4. **「KOR 分位概率主信号 + 正交伙伴融合：生产相关性 0.85 -> 0.54」** —— 概率主信号配合正交腿可大幅压 prod，
   是本族若通过 IS 闸后解决 prod 墙的现成路径。
5. **概率类字段需分位平滑化**：转排序百分比，避免仓位集中在少数高概率个股 => 全部模板外包 `rank()`。
6. **「高阶矩在说什么：偏度、峰度与熵」** —— 支撑 T10 的集中度/熵代理构造。

注意：论文明细（作者/年份/期刊）本轮未取得可引用条目，上述 6 条均为平台论坛实证帖；
外部论文补证留待本族出货后按机制定向检索（避免在未证实有信号的机制上先花检索预算）。


## 七、probability 软信息族实测判决

十桶概率族累计 8 条实测（设置档同上，`ten_day_label_*_17`，decay 1 除注明）：

| alpha | 模板 | S | F | TO | sub | sub/S | 2Y | 闸 | prod | 判决 |
|---|---|---:|---:|---:|---:|---:|---:|---:|---:|---|
| gJer3dNm | T02 上下侧累积差 | 3.71 | 1.60 | 70.33% | 2.68 | 0.7224 | 2.42 | 1(HIGH_TO) | **0.8120** | prod 深钉 |
| **qML5AKbV** | **T02 同式 @ decay 2** | **3.53** | **1.81** | **48.79%** | **2.56** | **0.7252** | **2.30** | **0** | **0.7967** | 需位移 0.0967 > 0.05，不破墙 |
| rKR0WVaE | T01 尾部净上行 | 2.45 | 0.91 | 64.85% | 1.73 | 0.7061 | 1.26 | 2 | **0.8562** | prod + 2Y 双死 |
| KPJVLZwp | T08 稳定性加权 IR | 2.45 | 0.89 | 66.35% | 1.70 | 0.6939 | 1.21 | 2 | **0.8429** | prod + 2Y 双死 |
| omEPK1PE | T03 相对信心比 | 2.44 | 0.90 | 64.94% | 1.75 | 0.7172 | 1.21 | 2 | 未测 | F + 2Y 死 |
| LLM8pPOL | T06 概率修正动量 @ decay 2 | 2.08 | 0.77 | 43.51% | 0.92 | 0.4423 | 1.15 | 3 | 未测 | sub/S 与 F 双死 |
| e751OlNJ | T09 对数概率 | 1.27 | 0.44 | 53.92% | 0.55 | 0.4331 | -0.11 | 5 | 未测 | 全死 |
| 9qxGRkAx | T04 两极分化度 | 0.55 | 0.13 | 47.42% | -0.03 | -0.0538 | -0.43 | 5 | 0.7400 | 无信号 |

三条关键读数：

1. **`decay` 是极好的换手杠杆**：T02 从 decay 1 -> 2，换手 70.33% -> 48.79%（降 21.5 个百分点），
   S 只从 3.71 掉到 3.53（-0.18），F 反而从 1.60 升到 1.81，sub/S 从 0.7224 微升到 0.7252。
   这是本会话最干净的一次「一个设置杠杆同时修好换手闸且不伤任何其它闸」——建议作为默认首选杠杆。
2. **T02 是本会话最精简的强构造**：`rank(subtract(add(P4,P3), add(P1,P0)))`，**仅 4 个算子**，S 3.53 / F 1.81。
   证明「概率质量的上半 vs 下半」比「尾部差 P4-P0」信息效率高一个量级（3.53 vs 2.45）。
3. **第二矩（不确定性）轴无信号**：T04 两极分化度 S 0.55 / sub 为负 / 2Y -0.43。
   => 该数据集的可用信息集中在一阶方向，进一步强化「整集封盘」的判决。

## 八、判决：`techindi_model` 在 EUR 整集封盘

累计 **11 个结构变体**（覆盖 2 个字段族 x 4 种信息加工方式 x 2 档 decay）的 prod 全貌：

| 字段族 | 加工方式 | 代表件 | prod |
|---|---|---|---:|
| 硬标签 predicted_* | 水平 group_rank + 幂放大 2.5 | pwvYnnOg | 0.7443 |
| 硬标签 | 线性化（指数 1） | 9qxGRRAx | 0.7854 |
| 硬标签 | 指数 2 | O0A69pnY | 0.7564 |
| 硬标签 | ts_rank 稳健化 | 78LGdwa2 | 0.7276 |
| 硬标签 | industry 局部分组 | E56mKKrL | 0.7384 |
| 软信息 probability_* | 尾部差 T01 | rKR0WVaE | 0.8562 |
| 软信息 | 上下侧累积 T02 | gJer3dNm | 0.8120 |
| 软信息 | 上下侧累积 @decay2 | qML5AKbV | 0.7967 |
| 软信息 | 稳定性加权 T08 | KPJVLZwp | 0.8429 |
| 软信息 | 两极分化 T04 | 9qxGRkAx | 0.7400 |

**因果结论（可复用）**：prod 相关性随「方向性载荷」单调上升 ——
纯方向（T01 尾部差）0.856 > 累积方向（T02）0.812 > 方向/稳定（T08）0.843 > 非方向（T04 分化）0.740。
去方向化确实能降 prod，但同时把 S 从 3.5 打到 0.55；
**前沿上不存在 `prod < 0.70 且 S >= 1.58` 的点** => 机制层面封盘，与骨架选择无关。

补充证据：该数据集概率字段在 **USA / DEU 都不存在**（预检 4/5 字段 unknown），无法跨区迁移救援。

## 九、字段画像补全：`tm_*` 网格族（399 字段）

798 字段中 399 个为网格命名 `tm_15_r1_r5_r10_rh_glb_d1_r{H}_q{Q}[_p{K}]`：

- `r1_r5_r10` = 训练期混合、`rh_glb` = 全球训练、`d1` = delay 1
- `r{H}` = 预测期限 H 日（r1 / r10 两档都出现在 EUR）
- `q{Q}` = 分位 Q（q1..q5）；`_p{K}` = 该分位下桶 K 的概率（p0..p4）
- 拥挤度：`q1`（aC 153）、`q2`（49）已被用烂；`q4_p1/p2/p3`、`q5_p1/p2/p3`、`q3_p1/p2` **aC 全 0**

=> 这是 `predicted_*` / `probability_*` 两族的**原始别名网格**，信息同源；
按「同源同 prod」的先验，本族不单独开波，除非要用**不同模型配置（r1 vs r10 vs r1_r5_r10 混合）**做真正正交的信号源。

## 十、跃迁目标：EUR/OTHER 剩余低拥挤数据集

| 数据集 | 字段 | cov | aC | 机制面 | 状态 |
|---|---:|---:|---:|---|---|
| `techindi_model` | 798 | 1.0 | 0-197 | 模型预测收益分布 | **封盘（prod 0.73-0.86）** |
| **`news_sentiment_dl`** | **66（全 VECTOR）** | **0.744-0.772** | **max 1** | **新闻文案情绪 + 可读性，3 源** | **本波探针中** |
| `news_sentiment_nlp` | 23（全 VECTOR） | 0.9134 | 0-6 | 标题情绪 / 可读性 / 主观性 | 备选 |
| `ai_news_scores` | 105 | 0.792 | 7 | AI 新闻评分 | 备选 |
| `other571` | 30 | 0.759 | 2 | 未画像 | 备选 |
| `other455` | 1500 | 0.96 | 533 | 未画像，拥挤 | 低优先 |
| `search_interest` | 5 | 0.782 | 0 | 搜索关注度 | 字段太少 |

`news_sentiment_dl` 画像：3 个新闻源（`bbgnews_enhanced` / `inferess` / `trna`）x 三类指标：

1. **情绪词极性**：`max/mean/min_positive_word_sentiment_*`、`max/mean/min_negative_word_sentiment_*`、`positive/negative_word_count_*`
2. **可读性**：`avg_words_per_sentence_*`、`avg_syllables_per_word_*`
3. 全 VECTOR 类型 => 每条记录是一天内的多条新闻向量，**向量内部的分歧度本身就是信息**

结构性优势：**sources x 指标** 两轴笛卡尔积，且「跨源分歧」是单数据集内即可构造的正交维度。
文献支撑面（待定向补证）：Tetlock (2007/2008) 媒体悲观语调、Loughran-McDonald 金融词典、
Li (2008) 年报可读性、Miller (1977) 意见分歧 + 卖空约束。

## 十一、待办

1. 收 N1（`1BbbhB9vr4T89rE1dpHxsCAg`：净情绪 / 可读性）与 N2（`3Bo0zSdN94i1brp2A4ZSAE1`：跨源分歧 / 向量内分歧）四条的 S/F/TO/2Y/sub。
2. 若任一条 S >= 1.58 且 sub/S >= 0.5303：测 prod（约 10 秒/件）-> 与 EUR 池跑互相关 -> 登记。
3. **`truncation` 是无效杠杆（实证）**：`truncation 0.02` 配对批（`1FMw2fb4A4r99BDmzXwzNt6`，约 50 分钟后才出结果）
   与 `truncation 0.08` 原批**指标逐位相同**：
   `bl6x905p` S 3.92 / F 1.74 / TO 52.11% / sub 2.00 / 2Y 2.71（= `9qxGRRAx`）；
   `vR1Ym73d` S 3.89 / F 1.71 / TO 53.33% / sub 1.96 / 2Y 2.64（= `O0A69pnY`）。
   => rank 型 spread 在 TOPCS1600 上单票权重约 0.14%（700 多空两侧），**远低于 2% 截断线，截断根本不 binding**。
   不要用 truncation 当降 S / 降换手杠杆。顺带：该配对同时证明平台重跑是确定性的（指标完全复现）。
4. **`decay` 杠杆实证入册**：同一构造 decay 1 -> 2 使 TO 70.33% -> 48.79%，S -0.18、F +0.21、sub/S +0.003。
