# forum_sentiment 字段画像与首批回测（USA / TOP3000 / D1，2026-10-20）

> 命名规范：单数据集档案 = `_usa-<字段前缀>-field-profile-<asOf>.md`；本集字段前缀 `forum`。
> 三段式：**字段画像 → 适用模板 → 回测结果及指标**；末尾附判读与下一步。
> 换集理由（承接 `_usa-finnews-field-profile-20261020.md` §5.2）：finnews 的极性水平/短窗创新/分歧/事件门控四类机制全部实测失败，turnover 指纹（1.1–1.4%）证明其字段在平台侧是持久特征而非事件序列。本集是**消息级 VECTOR**，可以构造 finnews 无法构造的「消息间分歧」与「发帖关注度」两个维度。

## 0. 路由与数据集元数据

| 项 | 值 |
|---|---|
| dataset id | `forum_sentiment` |
| 平台类别 | `sentiment`（StockTwits 散户消息情绪） |
| 字段数 | **13**（全 VECTOR，无 MATRIX） |
| 覆盖率 | **1.00**（逐字段均 1.00，平台口径） |
| 平台 alphaCount / userCount | 约 16 / 单字段最高 5（极低拥挤） |
| 频率 | 日频；按「股票 × 日」聚合当日 StockTwits 消息 |
| 塔状态 | sentiment 塔在 USA 未点亮（2026-10 实测 2/16 点亮：model/analyst/earnings） |
| S0 三查 | 判死列表无本集；无跨区弱记录；lit=N → 通过 |
| 关键差异 | 13 个字段**全部是 VECTOR**，必须先 `vec_*` 聚合才能进横截面/时序算子 |

## 1. 字段画像

### 1.1 字段全表（13/13）

| 字段 | 含义 | aC | 家族 | 可用机制 |
|---|---|---:|---|---|
| `vader_compound_sentiment_score` | VADER 复合情绪（社媒语言调优） | 2 | direction | 水平 / 变化 / 事件门控 |
| `vader_mean_sentiment_value` | VADER 平均情绪值 | 5 | direction | 水平 / 变化 |
| `afinn_lexicon_sentiment_score` | AFINN 词典情绪 | 1 | direction | 跨词典分歧 |
| `loughran_mcdonald_sentiment_score` | Loughran–McDonald 金融词典情绪 | 1 | direction | 金融语境情绪 |
| `text_classification_f_score` | 消息信息量/信噪比评分 | 1 | attention | 信息量加权 |
| `finance_term_weighting_score` | 金融词汇占比（知情程度） | 0 | attention | 知情度加权 / 门控 |
| `english_language_weighting` | 英语内容占比 | 1 | event_type | 数据质量门控（预计近似常数） |
| `filtered_word_total_count` | 去噪后词数（体量） | 0 | attention | 关注度 / 归一化 |
| `common_word_frequency_count` | 停用词数（啰嗦度） | 3 | attention | 噪声代理 |
| `average_character_count_text` | 平均消息长度 | 0 | attention | 噪声/详细度代理 |
| `punctuation_symbol_total` | 标点总数 | 0 | attention | 情绪强度代理 |
| `non_year_digit_occurrence` | 数字 token 数（非年份） | 0 | attention | 技术/价格讨论代理 |
| `year_mention_frequency` | 年份 token 数 | 0 | event_type | 低价值（预计噪声） |

### 1.2 VECTOR 语义与聚合口径

- 每个字段是该股票当日**消息数组**；`vec_count` = 当日消息条数（关注度），`vec_avg` = 消息均值（方向水平），`vec_stddev` = 消息间分歧（Dispersion，HIGH 桶），`vec_range` = 极差（极化）。
- **无消息日**：向量为空 ⇒ 聚合结果为 NaN。覆盖率 1.0 是「字段有定义」，不等于「每日每股都有消息」；首批用 turnover 与持仓数间接核验。
- 聚合必须先于一切矩阵算子：`vec_avg(field)` → `ts_zscore` → `group_neutralize`。**禁止**把 VECTOR 字段直接放进 rank/group 算子。
- 情绪分数预计落在 [-1, 1]（VADER/AFINN 量纲），均值接近 0；分歧非负右偏；消息条数右偏、零膨胀。

### 1.3 机制假设（可证伪）

1. **分歧（Dispersion，HIGH）**：当日消息情绪分歧高 → 不确定性溢价 → 后续跑输；反向（低分歧 → 多）同样要测。
2. **方向水平（Level）**：散户净情绪偏高 → 后续超额（或散户过度乐观 → 反转，方向由首批裁决）。
3. **方向变化（Change）**：情绪 5 日改善 → 动量。
4. **关注度（Attention，HIGH）**：消息量异常放大 → 散户拥挤 → 后续反转（预期负号）。
5. **事件条件（Event-conditioned，HIGH）**：只在关注度异常日交易情绪，其余日平仓。
6. **信息量加权**：情绪 × 消息信息量 → 过滤噪声后的知情散户方向。
7. **跨词典分歧**：AFINN − VADER → 词典模型间不一致度，作为「文本歧义」代理。

## 2. 适用模板

沿用已验证的「归一 + 内层中性化 + 稳健化」壳，只替换信号核：

```
quantile(group_rank(hump(ts_backfill(winsorize(group_neutralize(SIGNAL, industry), std=4), 252), hump=0.01), subindustry))
```

- `SIGNAL`：先 `vec_*` 聚合，再 `ts_zscore(..., 22)`（水平/分歧/加权）或 `ts_av_diff(..., 5)`（变化）。
- 反向候选 = 整体 `reverse(quantile(...))`。
- 设置：USA / TOP3000 / D1，neutralization **SUBINDUSTRY**，**decay 1**（社媒快信号，先压 turn<30%），truncation 0.08，pasteurization ON，unitHandling VERIFY，nanHandling ON，maxTrade OFF，FASTEXPR，start 2013-01-01 / end 2023-12-31。
- ⚠ VECTOR 字段必须先聚合；`vec_stddev`/`vec_count` 是矩阵值，不能再套 `vec_*`。

## 3. 首批回测设计（批 23）

**4 机制 × 双向 + 3 条加权/门控 = 8 条**，全部字段来自本数据集（ATOM 约束）：

| # | 机制 | 桶 | 核心量（聚合后） | 方向 |
|---:|---|---|---|---|
| 1 | 消息分歧 | Dispersion | `ts_zscore(vec_stddev(vader_compound_sentiment_score), 22)` | 高分歧 → 多 |
| 2 | 消息分歧 | Dispersion | 同上 | 反向 |
| 3 | 情绪水平 | Level | `ts_zscore(vec_avg(vader_compound_sentiment_score), 22)` | 高情绪 → 多 |
| 4 | 情绪变化 | Change | `ts_zscore(ts_av_diff(vec_avg(vader_mean_sentiment_value), 5), 22)` | 改善 → 多 |
| 5 | 关注度 | Attention | `ts_zscore(vec_count(vader_compound_sentiment_score), 22)` | **反向**（高关注 → 空） |
| 6 | 事件条件 | Event-conditioned | `trade_when(ts_zscore(vec_count(vader_compound_sentiment_score),22)>1, ts_zscore(vec_avg(vader_compound_sentiment_score),22), -1)` | 异常关注日做多情绪 |
| 7 | 信息量加权 | Surprise | `ts_zscore(vec_avg(vader_compound_sentiment_score) * vec_avg(text_classification_f_score), 22)` | 知情情绪 → 多 |
| 8 | 跨词典分歧 | Dispersion | `ts_zscore(vec_avg(afinn_lexicon_sentiment_score) − vec_avg(vader_compound_sentiment_score), 22)` | 高歧义 → 空（先测原向） |

判读规则（预先写死）：
- 若全部 8 条 turnover **>30%** ⇒ 聚合太噪，下一批统一加 `ts_decay_linear(...,5)` 或 `hump` 加深；若 <2% ⇒ 与 finnews 同病（聚合后成静态特征），本集也判死。
- 若分歧族（#1/#2）双向 |S| 均 <0.6 ⇒ 消息分歧机制否决，不再在本集磨。
- 若关注度（#5）|S|≥1.0 ⇒ 散户拥挤反转成立，进 batch 24 做「关注度 × 情绪」二维条件。
- 任何候选 S≥1.5 才进 prod/self 相关性实测。

## 4. 回测结果及指标

### 4.1 批 23 全表（multisim `17WeFg5Gw4kE8TZvKfLoQmb`，8/8 COMPLETE）

设置：USA / TOP3000 / D1，decay **1**，SUBINDUSTRY，truncation 0.08，pasteurization ON，VERIFY，nanHandling ON，maxTrade OFF，FASTEXPR，2014-01-01 → 2023-12-31。

| # | alpha id | 机制 | S | F | 2Y | SUB | turnover | returns | 失败闸 |
|---:|---|---|---:|---:|---:|---:|---:|---:|---|
| 1 | `wp9EXMQx` | 消息分歧（高→多） | −0.16 | −0.02 | 0.64 | −0.51 | 0.92% | −0.27% | 5 闸（含 SUB） |
| 2 | `O0JxKEA7` | 消息分歧反向 | 0.16 | 0.02 | −0.64 | 0.51 | 0.92% | 0.27% | 4 闸 |
| 3 | `gJW97EaJ` | 情绪水平 | 0.00 | 0.00 | −0.41 | 0.47 | 0.87% | 0.00% | 4 闸 |
| 4 | `wp9EXMo5` | 情绪 5 日变化 | 0.29 | 0.06 | −0.20 | 0.33 | 0.87% | 0.52% | 4 闸 |
| 5 | `RRA10nez` | 关注度（反向） | 0.22 | 0.04 | −1.02 | −0.25 | 0.89% | 0.39% | 5 闸（含 SUB） |
| 6 | `JjPvRZ3l` | 事件条件（关注异常日） | **0.42** | 0.10 | **1.44** | −0.09 | 0.83% | 0.74% | 5 闸（含 SUB） |
| 7 | `omogQMPE` | 信息量加权情绪 | 0.00 | 0.00 | −0.45 | 0.50 | 0.87% | 0.00% | 4 闸 |
| 8 | `QPY9mLOX` | 跨词典分歧 AFINN−VADER | −0.08 | −0.01 | −0.23 | −0.43 | 0.86% | −0.15% | 5 闸（含 SUB） |

八条**全部触发 `LOW_TURNOVER`（平台下限 1%）**，最高 S 仅 0.42。

### 4.2 归因

**指纹 1（决定性）：turnover 0.83–0.92%，8 条换了机制却几乎不动（极差 0.09pp），且比 finnews（1.1–1.4%）更低。**
若 turnover 由信号构造决定，`vec_count`（关注度）与 `ts_av_diff(...,5)`（5 日变化）必然明显高于水平类；实测三者一致 ⇒ **turnover 由字段本身的更新/取值结构决定，不由壳决定**。
与 finnews 同一指纹但更极端：消息级 VECTOR 在「股票 × 日」上的聚合值在平台侧表现为**慢变/半静态特征**。

**指纹 2：机制方向全灭，且不是方向做反。**
分歧双向 |S| 只有 0.16；水平 0.00；变化 0.29；关注度反向 0.22；信息量加权 0.00；跨词典分歧 −0.08。
双向都测的只有分歧族（#1/#2），正负对称且都接近 0 ⇒ **不是符号问题，是幅度问题**。

**指纹 3：唯一有结构的是事件条件（#6）：S 0.42，但 2Y **1.44**、F 0.10。**
全期弱而近两年强 ⇒ 该机制（关注异常日的散户情绪）**样本期后段才有效**，与 finnews 的「近期失效」相反，但幅度仍远不够（2Y 需 1.58）。
它也是八条里唯一 2Y 为正且 >1.0 的，说明「关注度门控」是本集唯一未被否证的维度。

**预注册规则命中**：全部 turnover <2% ⇒ 本集判死；分歧族 |S| 均 <0.6 ⇒ 分歧机制否决；关注度 |S|=0.22 <1.0 ⇒ 不进二维条件批。

### 4.3 判死前的混淆排除（批 24 诊断，必做）

「TO<2%」有两种解释，判死前必须分开：
- **H1（字段静态）**：聚合值本身日频几乎不变 ⇒ 数据集死，任何壳都救不回；
- **H2（壳致静态）**：`ts_backfill(252)` + `hump` + `quantile(group_rank)` 把变化抹平 ⇒ 换壳可救。

诊断批（decay **0**、无 backfill / hump / quantile，只保留 `group_neutralize(..., industry)`）：

| # | 诊断表达式 | 回答什么 |
|---:|---|---|
| 1 | `group_neutralize(vec_avg(vader_compound_sentiment_score), industry)` | 水平值的**原生**日换手 |
| 2 | `group_neutralize(ts_av_diff(vec_avg(vader_mean_sentiment_value), 5), industry)` | 5 日变化是否真的每天在变 |
| 3 | `group_neutralize(vec_count(vader_compound_sentiment_score), industry)` | 消息条数（关注度）是否日频更新 |
| 4 | `group_neutralize(ts_zscore(vec_stddev(vader_compound_sentiment_score), 22), industry)` | 消息间分歧是否日频更新 |

判据（写死）：**#2 或 #3 的 turnover ≥5% ⇒ H2（壳的错，换壳重做）；四条全部 <2% ⇒ H1（字段静态，判死）**。

**批 24 实测（multisim `1ZwuTBgWx4olcrX1ftKwEaXG`，decay 0 / NONE / trunc 0.08，4/4 COMPLETE）**：

| # | alpha | 诊断表达式 | S | 2Y | TO | 结论 |
|---|---|---|---:|---:|---:|---|
| 1 | `QPY9mKzX` | 情绪水平 `vec_avg` | 0.48 | −0.46 | **148.5%** | 动态，但收益 1.39% |
| 2 | `P0MOjgzw` | 5 日变化 `ts_av_diff(vec_avg,5)` | 0.05 | −0.62 | **155.0%** | 动态，几乎无收益 |
| 3 | `e76xeQGO` | 关注度 `vec_count` | −1.15 | −1.60 | **66.8%** | 动态，方向为负 |
| 4 | `pwvKQ5Gv` | 分歧 `ts_zscore(vec_stddev,22)` | 0.22 | 1.46 | **152.3%** | 动态，近两年略强 |

**判定：H2 成立（字段日频在变）——但「换壳可救」不成立。**

- 四条原生 TO 66.8–155%（远超 5% 判据），彻底否证 H1「字段静态」；
  §4.1 的 0.83–0.92% 是重壳（`ts_backfill(252)` + `hump` + `quantile(group_rank)`）造成的，
  **指纹 1 的归因需更正为「半静态是壳的产物」**。
- 但去掉壳后 S 反而全线更差：最高 0.48（水平族），变化族 0.05，分歧族 0.22，
  关注度族 −1.15 ⇒ **原生信号的幅度不足，不是被壳抹掉，而是壳此前压低了换手、
  同时把本就很弱的信号进一步平滑到不可用**。
- 「换壳重做」在本集没有可用的中间态：要压 TO 到 25% 以下又保留 S，
  等价于要求原生 S 在 25–100% 换手下仍有 ~1.6 的净信号；实测最高 0.48，差 3 倍以上。
- **本集最终判定：`forum_sentiment` 对 ATOM 不可用（信号幅度不足 + 原生换手极高）。
  不再投回测槽。** 与 finnews 的差别：finnews 是慢字段（TO 1.1–1.4%），
  forum_sentiment 是快字段（66–155%）但无信号——两者死于不同原因，判死依据都保留在本页。

## 5. 判读与下一步

- **保留结论（可迁移）**：`turnover <2%` 不能直接判字段静态，必须先跑「去壳诊断批」
  （decay 0 + 仅 `group_neutralize`），否则会把「壳压平」误记成「字段静态」。
  代价 4 条回测，值得。
- 本集不再投入；ATOM 挖掘重心回到 `analyst_consensus`（目标价族已交付 2 颗，
  Δ63 覆盖人数修正 `pwvKQN7x` 差 F 0.08，另有 surprise 族未测）。
