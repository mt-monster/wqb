# news_sentiment_dl · EUR / TOPCS1600 / D1 字段画像

> 类型 **VECTOR（全部 66 字段,须 `vec_*` 归约）** · 覆盖率 0.7443（bbgnews_enhanced）/ 0.7723（inferess）/ 0.7508（trna）
> 金字塔 category = **other**（multiplier 1.5,未点亮塔）
> 采集：`get_datafields(dataset_id=news_sentiment_dl, region=EUR, delay=1, universe=TOPCS1600)`,2026-11-06
> 全场竞争度：αC 总计仅 **2**（66 字段里只有 2 个字段被人用过 1 次）——全 EUR 最低竞争数据集,valueScore 6

## 0. 字段目录（22 语义 × 3 供应商结构,非 66 个独立字段）

**关键结构发现：本集是「3 家供应商（bbgnews_enhanced / inferess / trna）× 22 个同名语义字段」的平行矩阵**——每个语义字段有 3 个供应商变体,覆盖率/定义几乎一致。同一语义在 3 个变体上的读数应高度相关（预期互相关 >0.9,同 insiders1 的 shares/holdings 姊妹腿形态）,**每语义只测 1–2 个变体即可覆盖**。

| 语义字段（×3 供应商） | 类型 | 经济含义 |
|---|---|---|
| `max/mean/min_positive_word_sentiment_*` | 情绪强度 | 正面词情绪得分的最值/均值——**极性主轴** |
| `max/mean/min_negative_word_sentiment_*` | 情绪强度 | 负面词情绪得分——负面词的「最坏程度」可能是更强的尾部信号 |
| `positive/negative_word_count_*` | 计数 | 正/负情绪词数量——**关注度/密度轴**（EUR news 类成功样本用的是「条数=关注度」,不是极性分） |
| `positive/negative_word_sentiment_entropy_*` | 分布 | 情绪分布熵——分歧度代理（熵高=观点分散） |
| `positive/negative_word_sentiment_stddev_*` | 分布 | 情绪标准差——分歧度另一代理 |
| `output_metric_1..4_*` | 黑盒 | 供应商自定义输出指标（DL 模型输出,含义未公开）——**vS=6 的来源大概率是这 12 个** |
| `text_perplexity_*` | 文本复杂度 | 困惑度——文本不可预测性（高困惑度=意外新闻?） |
| `text_complexity_score_*` | 文本复杂度 | 语言复杂度 |
| `avg_words_per_sentence_*` / `avg_syllables_per_word_*` / `sentence_count_*` / `vocab_coverage_ratio_*` | 文本统计 | 可读性/篇幅——**元数据类,大概率无直接信号,只作辅助** |

## 1. 字段画像五问

| # | 问 | 答 |
|---|---|---|
| 1 时间维度 | 事件流量（逐日新闻聚合,VECTOR） | 稀疏事件型——`ts_sum` 累加、禁 `ts_decay_linear`（insider_agg_matrix §7 实证）、TO 控制靠窗口+decay |
| 2 相对性 | 极性分跨公司可比? | 词级情绪分是标准化量（-1..1 或 0..1）,**横截面可比性优于 insiders 的原始股数**——可直接 rank/zscore,无需分母 |
| 3 被定价的是谁 | 关注度 vs 极性 | **EUR news 类历史教训（region skill ⑥）**：成功样本用「新闻条数=关注度」（`mws46_ravenpack_sum_story_count`）,按极性分去测的 77 条全部 S<0.6——**本集第一批探针必须先测计数轴（word_count）,极性轴第二** |
| 4 有无博弈 | 拥挤度 | αC=2,全场最低——无拥挤,但「无人挖」也可能是「无信号」的信号,快速探针验证 |
| 5 事件性 | 稀疏 | VECTOR 事件输入——所有逐元素/比较算子必须先 `vec_*` 归约（insiders1 §4 工程坑,通用规则） |

## 2. 机制假设（第一批探针设计）

| # | 机制 | 表达式骨架（vec_sum 归约后） | 经济来源 |
|---|---|---|---|
| 1 | **关注度**（正词数+负词数=新闻密度） | `rank(group_zscore(ts_sum(add(vec_sum(positive_word_count_X), vec_sum(negative_word_count_X)), 22), industry), ...)` | Barber-Odean attention;EUR news 胜绩配方（条数=关注度） |
| 2 | 负面词密度 | `rank(group_zscore(ts_sum(vec_sum(negative_word_count_X), 22), industry), ...)` | 负面新闻的不对称影响（负面关注度更稀有） |
| 3 | 净情绪 | `rank(group_zscore(ts_sum(subtract(vec_sum(positive_word_count_X), vec_sum(negative_word_count_X)), 22), industry), ...)` | 极性差（对照组:若比 #1 强,极性轴有效） |
| 4 | 分歧度（负词熵） | `rank(group_zscore(ts_sum(vec_sum(negative_word_sentiment_entropy_X), 22), industry), ...)` | 分歧→后续反转/溢价 |
| 5 | DL 黑盒 output_metric | `rank(group_zscore(ts_sum(vec_sum(output_metric_1_X), 22), industry), ...)` | 供应商 DL 模型输出（黑盒,但 vS=6 来源） |

注:X ∈ {trna, inferess, bbgnews_enhanced},第一批只用 trna（覆盖 0.7508 居中,字段名最干净）。窗口 22d（新闻半衰期短,月度起步;66d 作对照第二批）。归一化栈用本战役新杠杆：`rank(group_scale(tail(winsorize(group_zscore(...)), industry)))`。

## 3. 实测记录

（待第一批探针回填）

**命名陷阱（2026-11-06 实测）**：trna 供应商的字段名后缀**不统一**——`negative_word_count_trna_enhanced` 带 `_enhanced` 而 `positive_word_count_trna` 不带,`negative_word_sentiment_entropy_trna` 不带——同供应商内部命名混杂,逐字段 `validate_expressions` 后才能进批,不可按目录名字面抄。

**第一批探针（已终态,multisim `2ITpnq9ak4Sdaxe1dVwXVwRd`,22d 窗口,zscore 栈,SLOW_AND_FAST）——五个机制方向全部负读数,但全部在「反向可用」区间**：

| # | 机制 | alpha id | S | F | 2Y | sub | robust | 读数 |
|---|---|---|---|---|---|---|---|---|
| 1 | 关注度（正+负词数） | `E568YKdm` | **−0.91** | −0.35 | −0.99 | −0.04 | −0.10 | 强反向 |
| 2 | 负面词密度 | `vR1pxmQQ` | −0.79 | −0.28 | −0.54 | 0.16 | 0.16 | 反向 |
| 3 | 净情绪（正−负） | `O0AMq9lY` | −0.68 | −0.21 | −1.08 | −0.07 | 0.00 | 反向 |
| 4 | 负词熵（分歧度） | `88RE7LM7` | −0.43 | −0.11 | −0.40 | 0.05 | 0.12 | 弱反向 |
| 5 | DL 黑盒 output_metric_1 | `WjOongvN` | **−0.87** | −0.33 | −1.13 | 0.01 | −0.15 | 强反向 |

**归因**：① 五个方向全负且方向一致——**「行业内相对新闻强度高的股票跑输」**,这不是五个独立失败,是同一个反向信号（关注度/新闻密度 → 负收益）的五个读数;#1 与 #5 的 S 只差 0.04（−0.91 vs −0.87）,证实 output_metric_1 与总词数高度共线（DL 黑盒大概率以词频特征为主成分）。② 反向机制有文献基础：**过度关注度效应**（Barber-Odean 2008 attention-induced buying;Da-Engelberg-Gao 2011 搜索量→短期冲高后反转;Tetlock 2007 高负面媒体语气→下压后回归）——但反向后 2Y 仍为 −0.99~−1.13 的绝对值水平（0.99–1.13）,不足以过闸;且 #1/#5 反向后 sub≈0（−0.04/0.01）,反向读数的子宇宙一致性存疑。③ **结论：正向与反向均不构成候选,但「关注度反向」是唯一有经济根基的活口**——第二批做反向+66d 窗口对照（注意力效应的半衰期是「数日冲高+数周反转」,22d 可能太短正反都不显著）,若 66d 反向 S>1.0 则继续,否则按快判死规则（8 探针无 |S|≥0.5——已 5 探针,第一批 5 条反向后 |S| 最大 0.91 达标线附近）记录。第二批同时覆盖 inferess 变体（不同供应商的字段定义差异可能携带独立信息）。

**第二批：反向 × 66d（已终态,multisim `1eNVv4aYq5blbkrg7TmpzCV`）——反向成立但强度不够**：

| # | 变体 | alpha id | S | F | 2Y | sub | robust |
|---|---|---|---|---|---|---|---|
| 1 | reverse 关注度 trna 66d | `N1NJjXQL` | **0.65** | 0.22 | **1.61 PASS** | 0.33 FAIL | 0.28 FAIL |
| 2 | reverse output_metric_1 66d | `2rAXZ1OY` | **0.68** | 0.23 | **1.88 PASS** | 0.27 FAIL | 0.42 FAIL |
| 3 | reverse 关注度 inferess 66d | `omEJz1L5` | −0.08 | −0.01 | 1.51 | 0.04 | 0.39 | 供应商不迁移 |
| 4 | reverse + ts_mean(·,5) trna | `xAr2zK3w` | 0.65 | 0.22 | 1.59 | 0.33 | 0.31 | 平滑无增益 |
| 5 | reverse 关注度 bbgnews 66d | `3qok6MXz` | 0.52 | 0.15 | 1.27 | 0.36 | 0.45 | 弱于 trna |

**归因**：① 反向把号翻正且 2Y 意外达标（1.61–1.88）——过度关注度反转机制方向正确；但 S 0.65–0.68 距闸 1.58 差 2.3×。② 第一批 22d **正向** S=−0.91 ⇒ reverse(22d) 预期 ≈+0.91，比 66d 反向更强——22d 更贴注意力冲高后反转的短半衰期，已提交 reverse(22d) 补测。③ inferess 反向归零（−0.08）——供应商间不共线，trna 是唯一有信号的源。④ 平滑/bbgnews 均不改善。**下一步：reverse(22d) 确认天花板；若 S<1.0 则本集关注度轴按「方向对、强度不足」归档，转测极性强度字段或换集。**

**第三批：reverse(22d)/5d/极性强度（已终态,multisim `4zQhte3HM5czciY1eBpaA8cv`）——天花板确认 S=0.91，sub/robust 结构性不可修**：

| # | 变体 | alpha id | S | F | 2Y | sub | robust |
|---|---|---|---|---|---|---|---|
| 1 | reverse 关注度 trna 22d | `gJegP1GO` | **0.91** | 0.35 | 0.99 | **0.04 FAIL** | **0.10 FAIL** |
| 2 | reverse output_metric_1 22d | `pwdMz6G6` | 0.87 | 0.33 | 1.13 | −0.01 | 0.15 |
| 3 | reverse 关注度 5d | `mLo0z87K` | 0.74 | 0.18 | 1.27 | 0.25 | 0.10 | TO .26 偏高 |
| 4 | reverse 负词情绪均值 22d | `1YNlm7KM` | 0.86 | 0.32 | 0.57 | −0.10 | −0.13 |

**终裁**：① reverse(22d) 精确翻号（−0.91→+0.91），但 sub 0.04 / robust 0.10——**信号集中在稳健子宇宙之外**，与 `significant_value_1` 同构的结构性失败。② 5d/极性强度均不改善。③ 论坛「relevance 加权 / 新颖度」模板依赖 news20 专属字段，本集无对应字段，不可迁移；SI（缓慢吸收新闻）模板需 returns 分桶 = PV+OTHER 组腿，违反本战役禁令。④ **累计探针 ≥14 条，最大 |S|=0.91，模板族 ≥4（关注度/极性/熵/DL 黑盒 × 正反向 × 3 窗口 × 3 供应商）——本集按「方向对、强度与结构双不足」归档，不再投入**。换下一集 `news54`（Key Developments，αC=3，cov 0.90，news ×1.3）。
