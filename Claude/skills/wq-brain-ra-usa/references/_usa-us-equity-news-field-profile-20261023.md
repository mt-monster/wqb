# USA / D1 `us_equity_news`（US Equity Quantitative News Sentiment）字段画像与波 1 设计（2026-10-23）

> **定位**：USA 未点亮塔补挖的第 5 个数据集（`risk60` / `pv106` / `chart_return_model` / `pv149` 之后）。
> 平台类别 **OTHER（×1.4，该塔 0 颗 ACTIVE ⇒ 未点亮）**，满足「已点亮塔的数据集不作主挖掘目标」
> 用户规则（2026-09-19 定案；已亮塔 = ANALYST 6 / MODEL 4）。
>
> **时效声明（用户 2026-10-23 指令 #1）**：本文件的**全部数据集/字段数字**来自 2026-10-23 的
> 平台实时读（`get_datasets` / `get_datafields` / `preflight_expressions`）+ 本地库只读计数。
> **旧画像、旧台账、旧判死结论一律不作为本数据集死活的证据**；本文件明确推翻了
> `_usa-pv149-field-profile-20261023.md` §1 里「`us_equity_news` … 情绪域已饱和 … 不投」
> 这一**基于 2026-09-17 SPRE 快照**的判断（依据见 §1.2）。
> 标「结构判读（未抽样）」的项是语义推断，**不是实测分布**，不得当已知。

## 1. 为什么选它（S0 选集，2026-10-23 实时口径）

### 1.1 数据集级硬事实（平台实时）

| 项 | 值 | 判读 |
|---|---|---|
| `id` | `us_equity_news` | — |
| 名称 | US Equity Quantitative News Sentiment | 量化新闻情绪（非深度学习黑盒） |
| 类别 | `other` | OTHER 塔 ×1.4，**0 颗 ACTIVE ⇒ 未点亮** |
| 覆盖 | **0.9627** | TOP3000 中 96.27% 股票有定义 |
| 字段数 | **8**（全部 VECTOR） | 面小、语义清晰、无同族冗余 |
| 用户数 | **61** | 远低于主流情绪集（ai_news_scores 66 / event_sentiment_signals 72） |
| 平台 alphaCount | **140**（字段级 17–34） | 低拥挤：对比 pv149 字段 1–20、OBI 已判死集数千 |
| valueScore | 4 | 平台估值中等 |
| 金字塔乘数 | 1.4 | OTHER 塔 |

### 1.2 推翻旧「情绪域饱和」判断的依据

旧 SPRE 快照（`tracking/USA/config/settings.json._spre_20260917`）写的是
「情绪域已饱和（prod 0.72–0.82 死）」「`news_sentiment` 在 excluded_families」。
按用户 2026-10-23 指令 #1，该快照**不能作证**，理由逐条：

1. **它说的是另一批对象**：那条结论来自 `probability_3` 差分 5 变体的 prod 0.72–0.82，
   属另一数据集的另一构造；**本数据集 8 个字段在本地库 0 条表达式 / 0 条回测**
   （只读实测：`backtest_results.dataset='us_equity_news'` = 0、`expressions` = 0、
   `payload_json like '%us_equity_news%'` = 0、字段名全库 0 命中），从未被测过。
2. **相关性可被结构改写**：论坛 51 票实证（post 35294898626711）同一新闻字段
   从价量核换到新闻 high-pass 核，prod 相关从 **0.70 → 0.44**；
   即「情绪域 prod 高」不是字段属性，而是**构造属性**。
3. **快照自身已过期**：`_spre_20260917` 还写着 `current_wave: 79`，而当前已到
   波 100+ 与多轮未点亮塔补挖；该快照的选集面（345 数据集）也与平台实时
   166 数据集不一致。

⚠ **流程处置**：本轮**不经 `build_wave` 选集**（其会读 `excluded_families`），
而是「画像 → 手工设计 → 显式表达式 → `submit_batch.py` 显式派发」，
因此没有绕过任何闸门；若后续要回到 `build_wave` 流程，须先更新该 SPRE 快照并写明理由，
**不得静默改闸**。

### 1.3 五层排除后的存活位

已排除：已亮塔（ANALYST/MODEL）主数据集、本地库已判死/已封存集（OBI prod 0.8808、
other699 40 sims、14 个 other 集 2026-10-20 全判、fundamentals 23 集、earnings 塔单槽已占）、
覆盖率 <0.65、字段 <5、映射表型伪数据集（BBID/RIC/BBGID）、ETF 级 `risk65`。
`us_equity_news` 是**低拥挤 + 高覆盖 + 小字段面 + 零测试历史**的交集，且属未点亮 OTHER 塔。

## 2. 字段清单与画像（8 字段，全 VECTOR，覆盖均 0.9627）

| 字段 | 平台原文含义 | 类型 | 覆盖 | users | aC | 归约算子 | 家族 |
|---|---|---|---:|---:|---:|---|---|
| `mean_sentiment_score_article` | Average sentiment score calculated for the article | VECTOR | 0.9627 | 15 | 21 | `vec_avg` | **A 语调强度** |
| `maximum_sentiment_score` | Highest sentiment score found within the article | VECTOR | 0.9627 | 19 | 29 | `vec_max` | A 语调强度 |
| `minimum_sentiment_score` | Lowest sentiment score found within the article | VECTOR | 0.9627 | 14 | 20 | `vec_min` | A 语调强度 |
| `count_positive_phrases` | Number of positive words or phrases in the article | VECTOR | 0.9627 | 19 | 34 | `vec_avg`/`vec_sum` | **B 极性短语** |
| `count_negative_phrases` | Number of negative words or phrases in the article | VECTOR | 0.9627 | 14 | 26 | `vec_avg`/`vec_sum` | B 极性短语 |
| `sentiment_tagged_phrase_count` | Number of words or phrases tagged with sentiment | VECTOR | 0.9627 | 13 | 17 | `vec_avg` | B 极性短语 |
| `total_word_count_article` | Total number of words in the article | VECTOR | 0.9627 | 10 | 18 | `vec_avg` | **C 文章结构** |
| `security_relevance_percentage` | Percentage indicating how relevant the article is to the referenced security | VECTOR | 0.9627 | 13 | 19 | `vec_avg` | **C 文章结构** |

### 2.1 结构判读（未抽样；Labs 抽样需用户另行授权）

- **A 家族（语调分数）**：文章级分数，跨文章形成 VECTOR；单篇分数有界（供应商未公布值域，
  不得假设 ±1）。`mean` 是中心，`max/min` 是**文章内极值**，不是跨文章极值。
- **B 家族（短语计数）**：非负整数计数，**右偏 + 零膨胀**（大量文章 0 个极性短语）。
  裸值跨股票不可比（文章数不同）⇒ 必须比值化或按文章平均。
- **C 家族（结构）**：`total_word_count_article` 是规模变量，**不能单独当信号**
  （长度与信息量非线性），只作密度分母；`security_relevance_percentage` 是 0–100 的
  相关度，用于**门控/加权**，不单独当方向信号（论坛 post 42659817284375 的核心手法）。
- **更新频率**：日频；文章是**事件型**到达（无新闻日无新文章）。VECTOR 长度
  = 当日该股票的文章数，因此 `vec_count(mean_sentiment_score_article)` 本身就是
  **媒体关注度**的一天截面。具体非零率/刷新率未抽样。
- **缺失**：覆盖 0.9627 ⇒ 3.73% 股票日无定义，由 `nanHandling=ON` 承接为 NaN，不参与排序。
- **可用性**：`preflight_expressions` 实测 8/8 字段存在、`unknown_fields=[]`、
  `any_changed=false`（11 条表达式都已被正确 `vec_*` 包裹，无遗漏）。
- **量纲**：A 家族为分数、B 家族为计数、C 家族为比例/词数 ⇒ 任何跨家族算术都必须先
  各自归一（本次统一用横截面 `rank` + 时序 `ts_zscore`），不得裸加。

## 3. 机制假设（发批前写定，收批时不得改判据）

| # | 假设 | 经济机制 | 方向先验 |
|---|---|---|---|
| H1 | 语调冲击 | 新闻语调的**变化**（相对自身 10 日）预测短期收益；水平已被定价 | 冲击↑ → 多 |
| H2 | 相关度加权语调 | 只有与该公司高度相关的文章才含信息；低相关文章是噪声 | 高相关×高语调 → 多 |
| H3 | 正负短语净语调 | 词典法极性净差，剔除分数模型的平滑 | 净正 → 多 |
| H4 | 媒体关注度 | 高覆盖 → 注意力已耗尽 → 未来收益低（Fang-Peress） | 覆盖↑ → 空 |
| H5 | 跨文章分歧 | 同日文章语调分歧 = 观点分化 → 高估 → 未来低（Miller） | 分歧↑ → 空 |
| H6 | 关注-语调同向性 | 语调随文章数同涨 = hype，反转 | 同向性↑ → 空 |
| H7 | 负正协方差 | 负/正短语共同放大 = 争议性新闻，论坛原样模板 | 协方差↑ → 空（取负） |
| H8 | 情绪词密度 | 情绪词占比高 = 主观性强 = 信息含量低/情绪驱动 | 密度↑ → 多（待裁） |
| H9 | 最负短语极值 | 下行语调尾部（文章内最负）驱动风险溢价 | 极值↑（较不负面）→ 多 |
| H10 | 文章内极差 | 同一文章自相矛盾 = 不确定性 | 极差↑ → 空 |

## 4. 模板来源（三轨：论坛 + 论文 + 字段画像推导）

### 4.1 论坛（2026-10-23 实读，含票数/评论数）

| 帖子 ID | 标题 | 票 | 采纳的模板/手法 | 落到本波 |
|---|---|---:|---|---|
| `42659817284375` | 新闻情绪因子：别再用裸 sentiment 了——relevance 加权 + 新颖度过滤 | 31 | ① `sentiment × security_relevance_percentage` 或 relevance>60 过滤；② 新颖度 `event_similarity_days`（**本数据集无此字段，N/A**）；③ 变化型高换手需配 `ts_decay_linear`，水平型先平滑再横截面 rank | H2（M2）、全部水平臂的平滑+rank 壳 |
| `37140180319127` | MCP 七十二变模板之 news-sentiment 点塔 | 36 | `group_zscore(-ts_corr(<news>, <sentiment>, <days>), <group>)`；评论提示 `ts_delay(news,1)` 与混信号风险 | H6（M6，改为 `-ts_corr(tone, count, 22)`，单数据集内部两字段，不跨源混信号） |
| `35294898626711` | 情绪数据中用 ts_covariance 构建 alpha 模板 | 51 | ① 已提交模板 `-ts_covariance(neg, pos, d)`，d=63/252/504；② `ts_backfill` 强制（无回填 S 0.89/ht 0.64 → 回填 120 S 1.53/ht 0.83，20 vs 120 逐位相同）；③ 已证 high-pass：`ts_zscore(rank(ts_backfill(f,120) − ts_mean(ts_backfill(f,120), W)), 250)`，W=5/10/22/44 → S 1.25/1.53/1.46/1.28；④ 纯水平 `ts_zscore` → S 0.38；⑤ `ts_delta(f,1)` → S −0.52/TO 1.2；⑥ 新闻 high-pass 的 prod 相关 0.44 vs 价量核 0.70 | H1（M1，W=10 原样）、H7（M7，d=63） |
| `41449516289687` | 【sentiment 模板】帮助点 sentiment 塔 | 18 | `group_neutralize(reverse(vec_max(subtract(pos_dispersion, neg_dispersion)), group))` ⚠ 原稿写 `ts_max`：**平台不可访问算子**（整批 CANCELLED 元凶），VECTOR 字段须走 `vec_*`，days=5 | H5 的同族（本波用 `vec_stddev` 跨文章分歧，波 2 再上 dispersion 极值版） |

### 4.2 外部金融论文（模板级，不是背景引用）

| 论文 | 结论 | 落到本波 |
|---|---|---|
| Tetlock (2007), *Giving Content to Investor Sentiment*, JF | 媒体语调（尤其负面）预测个股收益与成交量；**水平有短期反转** | H1 语调冲击、H9 最负极值 |
| Tetlock, Saar-Tsechansky & Macskassy (2008), *More Than Words*, JF | 否定词/情态词比例比全文语调更能预测基本面 | H3 正负短语净差、H8 词密度 |
| Fang & Peress (2009), *Media Coverage and the Cross-section of Stock Returns*, JF | 高媒体覆盖 → 低未来收益（注意力/摩擦渠道） | H4 覆盖度取负 |
| Heston & Sinha (2017), *News vs. Sentiment*, FAJ | 新闻的**结构化情绪**在短窗有预测力，长窗衰减 | 全部臂的 22/63/250 窗选择与衰减 |
| Miller (1977), *Risk, Uncertainty, and Divergence of Opinion*, JF | 观点分歧 + 卖空约束 → 高估 | H5 跨文章分歧取负 |

### 4.3 字段画像推导（无外部模板可抄的部分）

H6/H10 是把 VECTOR 的**结构量**（文章数、文章内极差）当作信号本体，属本数据集独有；
论坛与论文都只给机制、不给表达式，故按 §2 的结构判读手工构造，并在波 1 单列，
不与已证模板混在一起归因。

## 5. 波 1 十一臂设计（`uen_w1`）

设置（除 D0 外全部一致）：USA / TOP3000 / D1 / **SUBINDUSTRY** / decay 5 / truncation 0.08 /
`nanHandling=ON` / `maxTrade=OFF` / `pasteurization=ON` / `unitHandling=VERIFY` /
2014-01-01 → 2023-12-31 / REGULAR。算子调用点实测 5–8（上限 <10）。

| # | 假设 | 表达式核心 | 角色 |
|---:|---|---|---|
| M1 | H1 | `ts_zscore(rank(ts_backfill(vec_avg(tone),120) − ts_mean(ts_backfill(vec_avg(tone),120),10)), 250)` | 论坛已证 high-pass 原样 |
| M2 | H2 | `ts_zscore(rank(ts_mean(ts_backfill(vec_avg(tone) * vec_avg(relevance),120),22)),250)` | relevance 乘积门控（**近似版**：均值乘积，非逐篇加权；逐篇版待波 2） |
| M3 | H3 | `ts_zscore(rank(ts_mean(ts_backfill((vec_avg(pos)−vec_avg(neg))/add(add(vec_avg(pos), vec_avg(neg)), 1),120),22)),250)` | 词典净语调 |
| M4 | H4 | `-ts_zscore(rank(ts_mean(ts_backfill(vec_count(tone),120),22)),250)` | 覆盖度（取负） |
| M5 | H5 | `-ts_zscore(rank(ts_mean(ts_backfill(vec_stddev(tone),120),22)),250)` | 跨文章分歧（取负） |
| M6 | H6 | `-ts_corr(ts_backfill(vec_avg(tone),120), ts_backfill(vec_count(tone),120), 22)` | 关注-语调同向性（取负） |
| M7 | H7 | `-ts_covariance(ts_backfill(vec_sum(neg),120), ts_backfill(vec_sum(pos),120), 63)` | 论坛协方差原样 |
| M8 | H8 | `ts_zscore(rank(ts_mean(ts_backfill(vec_avg(tagged)/(vec_avg(words)+1),120),22)),250)` | 情绪词密度 |
| M9 | H9 | `ts_zscore(rank(ts_mean(ts_backfill(vec_min(minimum_sentiment_score),120),22)),250)` | 最负短语极值 |
| M10 | H10 | `-ts_zscore(rank(ts_mean(ts_backfill(vec_max(max)−vec_min(min),120),22)),250)` | 文章内极差（取负） |
| D0 | 去壳诊断 | M1 的 high-pass 内核，去掉 `ts_zscore(,250)`，**NONE / decay 0** | 原生换手 + 裸信号 |

（`tone` = `mean_sentiment_score_article`，`pos/neg` = `count_positive_phrases`/`count_negative_phrases`，
`relevance` = `security_relevance_percentage`。）

## 6. 预登记判据（收批时逐条执行，不临时加码）

1. **任一臂 RA 全过**（S ≥ 1.58、F ≥ 1.0、SUB/S ≥ 0.435、2Y ≥ 1.58、TO ∈ (0.01,0.70)、CW ≤ 0.1）
   ⇒ **立即**做 `check_correlation(refresh=True)` prod 探针，不先扩同族（`risk60` 教训）。
2. **方向纪律**：反向臂只在能写出经济机制时才反号；「反向 S 更高」本身不构成理由
   （`pv106` 教训）。
3. **归因优先于扩批**：若某臂 1–2 闸不过，先看是 **2Y 断层 / SUB 断层 / Fitness 墙 / 换手墙**
   哪一类，再决定换窗、换壳还是换字段；**不得盲扫**（用户过程约束）。
4. **D0 必读**：D0 turnover < 2% 且重壳臂也 < 2% ⇒ 字段准静态，本集停；
   D0 turnover 很高而重壳臂被压平 ⇒ 是壳压平，波 2 换中档壳（decay 0/2 + 短窗）。
5. **全弱判据**：10 个机制臂全部 `|S| < 0.8` ⇒ 信号幅度不足，停投本集，换下一个未点亮塔数据集
   （这条只在**全部**机制都试过后成立，不得用部分臂下结论）。
6. **prod 判死**：任一 RA 全过臂 prod ≥ 0.75 ⇒ 按 D0-P 记 `dead_end`；
   `[0.7,0.8)` 每出现 1 颗即记「拥挤族」；`[0.9,1]` ≥10 颗才算饱和。
7. **2Y 结构性墙**：若 ≥6 臂 S/SUB/F 均过而 2Y 系统性 < 1.58，则先做窗口/衰减设置轴，
   仍不过再判「本集 2Y 结构性不可修」。

## 7. 派发与验证口径

- **门禁**：`preflight_expressions` → `valid=true`、8/8 字段存在、VECTOR 包裹 0 改动；
  `wqb.expression.op_arity.check_expressions` → 11/11 通过（signatures 101）；
  算子调用点 5–8（<10）。
- **派发**：`tools/submit_batch.py --spec tracking/USA/runs/usa_uen_w1_spec.json`
  - `usa_uen_w1_batch_a.txt`（M1–M10，SUBINDUSTRY/decay 5）→ multisim `27Qacl1Wh5ek9Pq15zioFr2w`
  - `usa_uen_w1_batch_d0.txt`（D0，NONE/decay 0）→ single `3XBWXT1No4Wl9Gy2IzBL0ok`
- **验证标准**（不可放宽）：平台 RA 全闸 PASS + `check_correlation(refresh=True)`
  的 prod **与** self 均 < 0.7 <!-- from config.prod_corr_max -->；提交需用户逐颗明确确认。
- **金字塔核验**：每个候选提交前用 `get_alpha_details` 读 `pyramids`，确认落在
  OTHER 塔未点亮格；已点亮格不得作为主候选。

## 8. 结果与裁决

### 8.1 波 1 收批（2026-10-23，multisim `27Qacl1Wh5ek9Pq15zioFr2w` + single `3XBWXT1No4Wl9Gy2IzBL0ok`）

| # | alpha id | S | F | TO | 2Y | SUB | SUB/S | RA 失败 | 裁决 |
|---|---|---:|---:|---:|---:|---:|---:|---|---|
| M1 | `vROpdgJr` | **−1.45** | −0.37 | 50.8% | −1.88 | **0.51** | 0.35（反向后同） | S/F/2Y/SUB | 机制显著但**方向与论坛先验相反**（语调冲击 → 反转）；反向 S 1.45 < 1.58 且 SUB 仍不达标 ⇒ 不作候选，仅作机制证据 |
| M2 | `kqJWQl1k` | 0.35 | 0.09 | 12.0% | 0.42 | −0.55 | — | S/F/2Y/SUB | 死 |
| M3 | `LL5mkJgM` | −0.03 | 0.00 | 11.4% | −0.29 | −0.64 | — | S/F/2Y/SUB | 死（词典净语调无信息） |
| M4 | `RRAldW2g` | −0.70 | −0.33 | 12.7% | −0.76 | −0.56 | — | S/F/2Y/SUB | 死（覆盖度取负方向对但幅度不足） |
| M5 | `P0MYv9nq` | −0.23 | −0.05 | 11.9% | −0.31 | −0.71 | — | S/F/2Y/SUB | 死（跨文章分歧） |
| **M6** | **`qMEYgqnO`** | **2.95** | **2.66** | **14.0%** | **2.56** | **0.78** | **0.264** | **仅 SUB（0.78 < 1.28）** | **唯一强信号；进入 SUB 修复波** |
| M7 | `VkdmOJOJ` | 0.15 | 0.04 | 4.3% | 0.29 | −0.08 | — | S/F/2Y/SUB | 死（论坛协方差模板在本集不成立） |
| M8 | `j2eP1m1e` | 0.00 | 0.00 | 12.2% | 0.46 | 0.19 | — | S/F/2Y | 死（情绪词密度无方向） |
| M9 | `E5V8kJKJ` | 0.77 | 0.30 | 12.7% | 0.98 | 0.20 | 0.26 | S/F/2Y/SUB | 弱（最负短语极值） |
| M10 | `N1eJA9OL` | 0.62 | 0.23 | 12.8% | 0.73 | 0.05 | 0.08 | S/F/2Y/SUB | 弱（文章内极差） |
| D0 | `1YjlJm96` | −0.04 | −0.01 | **37.95%** | −0.06 | 0.74 | — | S/F/2Y | 去壳（无 `ts_zscore`、NONE、decay 0）后无信号且 MDD 72% ⇒ 壳/中性化/衰减共同构成必要支撑；三者各自的贡献需在波 2 分离，**不能单独归因给 `ts_zscore`** |

### 8.2 M6 明细（`qMEYgqnO`）

- 表达式：`-ts_corr(ts_backfill(vec_avg(mean_sentiment_score_article),120),ts_backfill(vec_count(mean_sentiment_score_article),120),22)`
- 设置：USA / TOP3000 / D1 / SUBINDUSTRY / decay 5 / trunc 0.08 / nanHandling ON / 2014–2023。
- 指标：S **2.95**、F **2.66**、TO 13.99%、RET 11.38%、MDD 1.88%、margin 16.26 bp、
  long 1524 / short 1402、risk-neutralized S **2.35**、investability S 3.09。
- RA：`LOW_SHARPE` / `LOW_FITNESS` / `LOW_TURNOVER` / `HIGH_TURNOVER` /
  `CONCENTRATED_WEIGHT` / `CLUSTER_TEST` / `LOW_2Y_SHARPE` / `MATCHES_PYRAMID` 全 PASS；
  **唯一 FAIL = `LOW_SUB_UNIVERSE_SHARPE`：0.78 < 1.28（= 0.435 × S）**。
- 塔位：`pyramids = [{USA/D1/OTHER, ×1.4}]`，`effective=1` ⇒ **未点亮塔**。
- **逐年（关键画像事实）**：2014–2020 全部 `pnl=0`（无数据），
  2021 S 2.80 / 2022 S 3.43 / 2023 S 1.41。
  ⇒ 本数据集**有效样本自 2021 起**，全期 S/F/2Y 实际上都建立在 2021–2023 上。
  这解释了为什么 2014 起的 `ts_zscore(,250)` 壳（M1–M5、M8–M10）大量失效：
  它们把有限的样本又切掉一段。M6 只用 22 日窗，是唯一吃满有效样本的构造。

### 8.3 归因（用户约束：先归因再推进）

1. **数据集有真信号，但只在一个机制上**：10 个机制里只有 M6 过 1.0 Sharpe，
   其余 9 个 `|S| ≤ 1.45` 且 8 个 `|S| ≤ 0.77`。⇒ 信息不在语调**水平**、
   不在短语**计数**、不在文章**结构**，而在**语调与关注度的联合动态**（H6）。
2. **M1 的负号不是失败而是机制证据**：新闻语调冲击在 USA 是**反转**（S −1.45 / 2Y −1.88），
   与论坛在其它区域的「冲击→动量」相反。方向先验必须按区域改，但不能靠反号救活
   （反向 S 1.45 仍不够，且 SUB 更差）。
3. **SUB 是比值闸**：门槛 1.28 = 0.435 × 2.95；抬 S 会同步抬门槛，**不能靠抬 S 破**。
   必须先判「信号是否只存在于小市值」——由 TOP1000 / TOP2000 宇宙迁移直接回答（波 2a）。
4. **短样本约束**：有效样本 2021–2023，任何 250 日归一壳都会损失 1/3 样本；
   修复波应优先用 ≤63 日窗与结构归一，而不是加长窗。

### 8.4 宇宙迁移诊断（波 2a，回答 §8.3 第 3 条）

同一 M6 表达式（22 日窗、SUBINDUSTRY、decay 5）换 universe 直测：

| universe | S | 2Y | SUB | SUB 门槛 | 判定 |
|---|---:|---:|---:|---:|---|
| TOP3000 | 2.95 | 2.56 | 0.78 | 1.28 | 不达标 |
| TOP2000 | 1.82 | 1.28 | 0.68 | 0.79 | 不达标（2Y 同时破） |
| TOP1000 | 0.68 | — | 0.94 | 0.30 | 比值过、**绝对 S 崩** |

**结论：换 universe 不是修复路径。** 它只是把门槛一起降低，并未提高大盘股信号强度；
TOP1000 上绝对 Sharpe 崩到 0.68，说明信号厚度确实集中在小市值段。
⇒ SUB 必须在 TOP3000 上解决（中性化/结构），不能靠收缩宇宙。

### 8.5 修复波（波 2r，10 臂）与两条可复用归因

全部 TOP3000/D1、trunc 0.08、nanHandling ON、2014–2023；`SUB 门槛 = 0.435 × S`。

| # | 臂 | alpha | S | F | 2Y | SUB | TO | RA 失败 |
|---|---|---|---:|---:|---:|---:|---:|---:|
| R1 | `rank(-corr22)` | `d5K3xLNK` | 0.28 | 0.10 | 1.96 | −0.27 | 5.0% | 3 |
| R2 | high-pass（快−慢） | `omoJKe16` | −0.42 | −0.11 | −0.28 | −1.38 | 16.6% | 4 |
| **R3** | **窗 44**（SUBIND） | **`O0JM9jLR`** | **3.14** | **3.32** | **2.69** | 1.30（门槛 1.36） | 9.2% | 1（SUB） |
| R4 | backfill 20 | `P0MY1bVq` | 3.00 | 2.72 | 2.63 | 0.84 | 14.0% | 1 |
| R5 | STATISTICAL | `mLY08wp9` | 2.90 | 2.12 | 2.71 | 0.74 | 14.6% | 1 |
| **R6** | **MARKET** | **`pwvM7Lx6`** | **2.78** | **2.81** | **2.50** | **1.29**（门槛 1.21） | 13.1% | **0** |
| R7 | 关注度加权 `rank×rank` | `N1eJpWjE` | 0.71 | 0.32 | 0.64 | 0.13 | 13.7% | 4 |
| R8 | `ts_rank(,250)` | `78ovwqKO` | 1.24 | 0.65 | −0.06 | −0.93 | 14.4% | 4 |
| R9 | trunc .15 / decay 10 | `j2ePZE29` | 2.98 | 2.89 | 2.60 | 0.70 | 11.8% | 1 |

两条**可复用**结论：

1. **绝对幅度本身承载信息**。`rank` / `ts_rank` / 覆盖率加权三条改造把 S 从 ~3 打到 ≤1.24，
   说明信息不在「相对排序」里，而在跨股票可比的**相关性强弱本身**。
   ⇒ 本族后续（若在别的区复用）应避免先取横截面 rank。
2. **只有 MARKET 中性化放出了大市值腿**。STATISTICAL（SUB 0.74）、trunc .15+decay 10（0.70）、
   backfill 20（0.84）都仍卡 SUB。⇒ 先前「信号只在小市值」的归因**需更正**：
   瓶颈不是市值集中，而是 **SUBINDUSTRY 中性化把大市值腿一并抵掉了**。
   同一表达式换 MARKET 后 SUB 1.29 > 1.21，RA 全绿。

**R6 明细（`pwvM7Lx6`）**：S 2.78 / F 2.81 / TO 13.1% / 2Y 2.50 / SUB 1.29 /
risk-neutralized S 2.26 / investability S 3.13 / long 1581 · short 1414 / RET 13.46% / MDD 2.40%；
RA `failed_ra_count=0`、`fail=[]`（仅 MATCHES_THEMES / OSMOSIS_ALLOCATION 两条 warning）；
塔位 `USA/D1/OTHER` ×1.4、`effective=1`（未点亮）。

### 8.6 prod 裁决：族级饱和，封存

R6 的 IS 唯一障碍是 prod 相关性。做三次独立实测（`check_correlation(refresh=True)`，
每次强制回源平台）：

| alpha | 窗 | S | TO | prod | `[0.7,0.8)` 桶 n | self | 判定 |
|---|---:|---:|---:|---:|---:|---:|---|
| `pwvM7Lx6` | 22 | 2.78 | 13.1% | **0.7643** | 8 | 0.5755 | fail |
| `A1QrwLzR` | 44 | 2.77 | 8.54% | **0.7811** | 18 | — | fail |
| `0mjN7Gg6` | 66 | 2.93 | 6.83% | **0.7834** | 18 | — | fail |

- 三颗全部 **RA 全绿**（`failed_ra_count=0`，`fail=[]`），收益/风险画像稳定：
  `A1QrwLzR` S 2.77 / F 3.08 / 2Y 2.40 / SUB 1.60（门槛 1.20）/ TO 8.54%；
  `0mjN7Gg6` S 2.93 / F 3.50 / 2Y 2.60 / SUB 1.64（门槛 1.27）/ TO 6.83%。
- 但 prod 无论 22 / 44 / 66 日窗都落在 **0.76–0.78**，且 `[0.7,0.8)` 桶 n 从 8 升到 18。
- **双独立判据同时命中**：
  ① D0-P：prod ≥ 0.75 ⇒ `dead_end`；
  ② 窗口谷法则：`[0.7,0.8)` n ≥ 1 ⇒ 族级拥挤、窗口微调不可救（n=18，无谷）。
- **裁决：`us_equity_news` 按「prod 饱和」封存**，不再开盲扫波。
  口径必须写清：**不是「字段无信号」**（S ~2.8–2.95、F ~2.8–3.5、RA 全绿、跨三个窗口稳定），
  而是**该信号已被生产池覆盖**。同族后续任何新构造，先查 prod 直方图再投入回测额度。

**为什么不再试 hump/decay/结构改写**：这些是「不改持仓」的平滑杠杆，不改信号来源；
而 prod 0.76–0.78 + 桶 n=18 说明相关性来自**信号本体**，不是换手噪声。三窗同区间即为证据。

## 9. 归档索引

- 本文件：`Claude/skills/wq-brain-ra-usa/references/_usa-us-equity-news-field-profile-20261023.md`
- 候选：`tracking/USA/runs/usa_uen_w1_candidates.json`
- 波 1 派发：`usa_uen_w1_batch_a.txt` / `usa_uen_w1_batch_d0.txt` / `usa_uen_w1_spec.json`
- 波 2a 宇宙：`usa_uen_w2_spec_univ.json` / `usa_uen_w2_top1000.txt` / `usa_uen_w2_top2000.txt`
- 波 2r 修复：`usa_uen_w2r_spec.json` + `usa_uen_w2r_{struct,window,weight,base_stat,base_mkt,base_trunc}.txt`
- 波 3 窗口探针：`usa_uen_w3_spec.json` / `usa_uen_w3_mkt_win.txt`（multisim `37IUf5Uy5jKaYdUHnMfwbN`）
- 交付总表：`output_report/USA_regular_alpha_delivery_20261021.md`
