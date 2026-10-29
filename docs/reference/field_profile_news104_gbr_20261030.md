# news104（News Sentiment Analytics）字段画像与模板池 — GBR / TOP700 / D1

> 建立日期：2026-10-30
> 区域：GBR ｜ Universe：TOP700 ｜ Delay：1
> 目标塔：**NEWS**（本季度 GBR/D1 塔位 0/3，完全未点亮）
> 平台 category：`news`（**非 PV / MODEL / OTHER**，不触碰 trio 禁混约束）

---

## 1. 数据集级画像

| 属性 | 值 |
|---|---|
| dataset id | `news104` |
| 类别 | news |
| 字段数 | 11（全 VECTOR，无 MATRIX） |
| 覆盖率 | **0.9695**（GBR 全部候选中最高档） |
| pyramidMultiplier | **1.6** |
| platform alphaCount | 88（字段级 8–120） |
| 来源 | 新闻文章级 NLP 情绪打分（第三方厂商预计算） |

### 1.1 关键前提：年代跨度必须实测

**数据集级 `coverage` 不含时间轴信息。** 同批次的 `sentiment27` 显示 coverage 0.8003，实测 yearly stats 2014–2018 五年 `longCount=0`，只有 2019–2023 有数据，当场判死。因此 news104 进入正式波次前**必须先跑一条探针 + `get_alpha_yearly_stats`**，逐年核 `longCount` / `pnl`，`longCount=0` 的年份即无数据年份。硬门槛：2014–2023 十年连续。

---

## 2. 字段清单与语义分类

| 字段 | 类型 | cov | alphaCount | 语义 | 信号角色 |
|---|---|---|---|---|---|
| `nws104_sentiment` | VECTOR | 0.9695 | 62 | 三值情绪分类 −1/0/+1 | **主信号** |
| `nws104_prob_pos` | VECTOR | 0.9695 | **120** | 正面概率 [0,1] | 主信号（最拥挤） |
| `nws104_prob_neg` | VECTOR | 0.9695 | 83 | 负面概率 [0,1] | 主信号 |
| `nws104_prob_ntr` | VECTOR | 0.9695 | **17** | 中性概率 [0,1] | **最不拥挤**，偏辅助 |
| `nws104_marketimpactscore` | VECTOR | 0.9695 | 91 | 厂商预估 1 分钟前瞻风险调整收益，约 −5~+5 | 外部先验 / 对照臂 |
| `nws104_novelty` | VECTOR | 0.9695 | 88 | 1=首报，>1=24h 内重复/更新 | **质量分层**（越低越新） |
| `nws104_confidence` | VECTOR | 0.9695 | 19 | 情绪打分置信度 [0,1] | **权重** |
| `nws104_relevance` | VECTOR | 0.9695 | 23 | 新闻对公司聚焦度，1=主体 | **权重** |
| `nws104_automessage` | VECTOR | 0.9695 | 10 | 1=日程类自动生成，0=人工 | **门控 / 反向** |
| `nws104_headlineonly` | VECTOR | 0.9695 | 8 | 1=仅标题，0=含全文 | **信息深度分层** |
| `nws104_timestamp` | VECTOR | 0.9695 | 8 | 文章发布 UTC 秒 | 非信号（PIT） |

**角色三分**（按用户「区分主信号与辅助信号」准则）：
- **主信号腿**：`sentiment` / `prob_pos` / `prob_neg` / `prob_ntr` / `marketimpactscore`
- **权重腿**（不可单独当信号）：`relevance` / `confidence`
- **分组/门控腿**（不可单独当信号）：`novelty` / `automessage` / `headlineonly`

---

## 3. 八问机制地图

| # | 问题 | 机制 | 对应模板 |
|---|---|---|---|
| Q1 | 新闻语调**水平**能不能定价？ | 媒体悲观 → 下行压力 → 随后反转（Tetlock 2007） | T1 / T3 |
| Q2 | 语调**变化**（创新量）比水平更有信息吗？ | 信息逐步扩散，语调改善 → 漂移 | T2 |
| Q3 | 同期语调动**分歧**代表什么？ | 分歧 = 信息不确定 → 折价（Miller 1977 分歧溢价反向） | T4 |
| Q4 | **新闻条数**（关注度）本身有信号吗？ | 关注度 → 散户买压 → 反转（Barber-Odean 2008） | T5 |
| Q5 | 加权口径能否提纯？ | 只信聚焦度高的文章 / 只信模型有把握的判断 | T6 / T7 |
| Q6 | **首报 vs 转载**有区别吗？ | 首报信息含量高，转载是已定价噪声 | T8 |
| Q7 | 厂商预计算的**预期收益**还有 alpha 吗？ | 已高度拥挤（alphaCount 91），预期接近套利干净 | T9（对照臂） |
| Q8 | **自动生成新闻**与**仅标题**说明什么？ | 自动日程新闻 = 无真实事件；仅标题 = 信息浅 | T10 / T11 |
| Q9 | 模型情绪与厂商冲击评分**背离**呢？ | 两套独立预测不一致 = 未被定价的信息 | T12 |

---

## 4. 十二模板池（结构互异，全部过单位闸）

> 窗口白名单：1 / 5 / 22 / 66 / 252 / 504 / 1008 / 1260。daily 用 [5,22]，quarterly 用 [66,252]。
> `unit_handling=VERIFY`：**禁止给带单位字段加无量纲常数**；比值一律同单位相除。本数据集全部字段无量纲（概率/计数/评分/flag），比值安全。

| # | 模板 | 表达式 | 机制 / 先验方向 |
|---|---|---|---|
| **T1** | 情绪水平（三值均值） | `ts_mean(vec_avg(nws104_sentiment), 5)` | Q1；Tetlock 2007 → 正向漂移 or 反转，**需 A/B 定符号** |
| **T2** | 情绪变化（创新量） | `ts_delta(ts_mean(vec_avg(nws104_sentiment), 5), 22)` | Q2；语调改善 → 正向 |
| **T3** | 情绪概率差（连续版） | `ts_mean(subtract(vec_avg(nws104_prob_pos), vec_avg(nws104_prob_neg)), 5)` | Q1 去量化损失；比 T1 更细 |
| **T4** | 跨文章语调分歧 | `multiply(-1, ts_mean(vec_stddev(nws104_sentiment), 22))` | Q3；分歧高 → 折价 → 取负 |
| **T5** | 新闻强度（关注度） | `ts_mean(vec_count(nws104_sentiment), 22)` | Q4；关注度 → 短买压；**双向待测** |
| **T6** | 聚焦度加权情绪 | `ts_mean(divide(vec_sum(multiply(nws104_sentiment, nws104_relevance)), vec_sum(nws104_relevance)), 5)` | Q5；只信主体新闻 |
| **T7** | 置信度加权正面概率 | `ts_mean(divide(vec_sum(multiply(nws104_prob_pos, nws104_confidence)), vec_sum(nws104_confidence)), 5)` | Q5；只信高置信判断 |
| **T8** | 首报溢价（novelty 反向） | `multiply(-1, ts_mean(vec_avg(nws104_novelty), 22))` | Q6；novelty 越低=首报占比越高 → 取负让首报为高 |
| **T9** | 厂商冲击评分（对照臂） | `ts_mean(vec_avg(nws104_marketimpactscore), 5)` | Q7；拥挤对照，用于测「厂商先验是否已被套利干净」 |
| **T10** | 自动新闻占比（关注真空） | `multiply(-1, ts_mean(divide(vec_sum(nws104_automessage), vec_count(nws104_automessage)), 22))` | Q8；自动新闻多 = 无真实事件 → 取负 |
| **T11** | 仅标题占比（信息浅） | `ts_mean(divide(vec_sum(nws104_headlineonly), vec_count(nws104_headlineonly)), 22)` | Q8；信息深度分层 |
| **T12** | 情绪 × 冲击背离 | `subtract(rank(ts_mean(vec_avg(nws104_sentiment), 5)), rank(ts_mean(vec_avg(nws104_marketimpactscore), 5)))` | Q9；两 rank 相减无量纲，背离=未定价信息 |

**结构互异性说明**：T1/T3 同属「水平」但一个是三值离散、一个是连续概率；T2 是时间差分；T4 是二阶矩；T5 是计数；T6/T7 是两种不同权重的加权平均；T8 是质量分层反向；T9 是外部先验；T10/T11 是两种 flag 占比；T12 是双预测背离。12 个模板分属 8 个不同数学结构（均值 / 差分 / 标准差 / 计数 / 加权比 / 反向分层 / 外部评分 / 双 rank 差）。

---

## 5. 单位闸自查

| 表达式片段 | 分子单位 | 分母单位 | 结论 |
|---|---|---|---|
| `divide(vec_sum(sentiment×relevance), vec_sum(relevance))` | 无量纲×无量纲 | 无量纲 | ✅ |
| `divide(vec_sum(prob_pos×confidence), vec_sum(confidence))` | 无量纲×无量纲 | 无量纲 | ✅ |
| `divide(vec_sum(automessage), vec_count(automessage))` | 计数 | 计数 | ✅ 约掉 |
| `divide(vec_sum(headlineonly), vec_count(headlineonly))` | 计数 | 计数 | ✅ 约掉 |
| `subtract(rank(a), rank(b))` | 无量纲 | — | ✅ 同单位相减 |

**未使用任何 ε 常数**，全部靠同单位相除天然无量纲。

---

## 6. 外部证据

### 6.1 论坛

- **`43179860065303`**（72 赞 / 50 评论，DEU sentiment27 维基关注度脉冲）：核心结论「**情绪水平无效、情绪突增动态才有效**」，引 Chalandamparis (2026)「情绪状态可测量不可交易」；同帖实证 `rank` 包装在本类信号上有害（每剥一层 rank 约 +Fitness 0.3–0.65），`ts_zscore(x,252)` 替换 `ts_ir` 会全结构崩盘。→ 直接支撑 **T2 优先于 T1**，且 **T3 不用 rank 包装**。
- **评论区二手教训**：注意力/情绪类数据平台存量供给很密，同族信号迁区后 prod corr 达 0.78–0.84 → 本数据集建仓前必须预留 prod 预算，不能指望「换区就降相关」。
- **`40433238987159`**（100 赞 / 28 评论，双字段 alpha 提示词）：`trade_when(sentiment > 0, alpha_main, -1)` 的本质是**降噪提 hit-rate，不是增强强度** → T10/T11 这类 flag 应该做**门控**而非独立信号腿。

### 6.2 外部论文

| 文献 | 结论 | 对应模板 |
|---|---|---|
| Tetlock (2007), *Giving Content to Investor Sentiment*, JF | 媒体悲观度预测下行压力，随后反转 | T1 / T3 |
| Tetlock, Saar-Tsechansky & Macskassy (2008), JF | 负面词汇比例预测负向盈余 | T1 |
| Barber & Odean (2008), *All That Glitters* | 关注度驱动散户买入 | T5 |
| Miller (1977), JF | 意见分歧 + 卖空受限 → 高估 | T4 |
| Da, Engelberg & Gao (2011), *In Search of Attention*, JF | 关注度代理（搜索量）→ 短期上涨后反转 | T5 / T2 方向参考 |

---

## 7. 已确认的算子约束（平台实测）

`operator_audit` 实测 GBR/D1 平台 live 算子 103 个。本模板池用到的全部在列：
`ts_mean` / `ts_delta` / `ts_std_dev` / `vec_avg` / `vec_sum` / `vec_count` / `vec_stddev` / `divide` / `subtract` / `multiply` / `rank` / `ts_ir` / `ts_av_diff` / `ts_backfill` / `vector_neut` / `quantile` / `group_rank` / `bucket`。

**不存在（幽灵，勿用）**：`ts_max` / `ts_min` / `ts_skewness` / `ts_median` / `ts_percentage` / `ts_entropy` / `ts_decay_exp_window` / `ts_delta_limit` / `group_median` / `group_normalize` / `neutralize` / `sigmoid` / `tanh` / `to_nan` / `ts_min_max_diff` / `ts_min_max_cps` / `ts_partial_corr` / `ts_co_kurtosis` / `group_percentage` / `group_vector_proj` / `s_log_1p`。

> ⚠️ 论坛模板里的 `ts_max(_, 5)` 在本平台不可用 ⇒ 提取「窗口峰值/脉冲」改用 `ts_av_diff(x, 5)`（x − 5 日均值，等价脉冲）或 `ts_rank(x, 5)`（当前值在 5 日窗内的时序分位，有界不易爆值）。

---

## 8. 执行序

1. 探针 A `T1` + 探针 B `T2`（已派发）→ **先判年代跨度**，不过十年即整集判死、止损。
2. 过十年 → 按 T1/T3/T4/T5 补齐四臂，把「水平 / 变化 / 分歧 / 强度」四条正交轴各自定符号。
3. 胜出轴做中性化 11 档扫描（**GBR 有 11 档**，禁跨区外推；si3 实测 FAST 最优）。
4. 再上 T6–T12 六个结构，凑够 10 个互异模板的实际回测证据。
5. 依 `eff = sqrt(returns/turnover)` 判「字段有无收益承载能力」：eff 低换字段，eff 高而 S 低才调骨架。
