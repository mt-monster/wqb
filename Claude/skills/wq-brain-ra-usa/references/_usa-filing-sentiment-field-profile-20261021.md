# USA · `filing_sentiment`（Regulatory Filing Sentiment Analytics）字段画像

> as_of 2026-10-21 · region USA / delay 1 / universe TOP3000 · 塔位 **other（未点亮）**
> 角色：本档案只服务本集，不替代 S0 体检；机制与止损在回测前预注册（§2.3）。

## 1. 数据集元数据与字段全集

| 项 | 值 | 来源 |
|---|---|---|
| dataset id | `filing_sentiment` | `get_datasets` |
| 名称 / 类别 | Regulatory Filing Sentiment Analytics / **other**（未点亮塔） | 同上 |
| coverage | **0.5396**（数据集级） | 同上 |
| fieldCount | **21（全部 VECTOR）** | 同上 |
| userCount | 27 | 同上 |
| **alphaCount** | **42** | 同上 |
| valueScore / 金字塔乘数 | 5 / **1.4** | 同上 |

**覆盖双档结构**（与 pv173 同形，但命名更乱）：`_2` 后缀 = 高覆盖档 **0.7266**；无后缀 / `_3` = 低覆盖档 **0.5443**；
少数 `_2` 其实是 0.0256 的窄档（`mean_sentiment_score_2` / `sentiment_term_quantity_2` / `major_section_quantity_2`），**不要按后缀猜档次**。

### 1.1 字段全集（21 / 21，按覆盖档分组）

| 字段 id | 覆盖 | users | **aC** | 含义 |
|---|---|---|---|---|
| `mean_sentiment_score` | 0.5443 | 0 | **0** | 该节内被标注词/短语情绪分的**均值** |
| `mean_sentiment_score_2` | 0.0256 | 2 | 2 | 同上（窄档） |
| `aggregate_sentiment_score_3` | 0.5443 | 0 | **0** | 该节内情绪分**总和** |
| `aggregate_sentiment_score_2` | 0.7266 | 5 | 8 | 同上（高覆盖档） |
| `negative_sentiment_term_count` | 0.5443 | 0 | **0** | 负面词/短语数（分 < 0） |
| `negative_sentiment_term_count_2` | 0.7266 | 11 | **14** | 同上（全集最高 aC） |
| `positive_sentiment_term_count` | 0.5443 | 1 | 1 | 正面词/短语数（分 > 0） |
| `positive_sentiment_term_count_2` | 0.7266 | 2 | 2 | 同上 |
| `sentiment_term_quantity` | 0.5443 | 0 | **0** | 该节正+负命中词总数 |
| `sentiment_term_quantity_2` | 0.0256 | 2 | 3 | 同上（窄档） |
| `total_word_quantity` | 0.5443 | 0 | **0** | 该节**词数** |
| `total_word_quantity_2` | 0.7266 | 2 | 2 | 同上 |
| `financial_note_quantity` | 0.5443 | 1 | 2 | 合并报表附注的**条目数** |
| `financial_note_quantity_2` | 0.7266 | 1 | 1 | 同上 |
| `subsection_quantity` | 0.5443 | 0 | **0** | 该节**子节数** |
| `subsection_quantity_2` | 0.7266 | 3 | 3 | 同上 |
| `major_section_quantity` | 0.5443 | 1 | 1 | 申报文件的**主章节数** |
| `major_section_quantity_2` | 0.0256 | 2 | 2 | 8-K 解析出的主要部分数（窄档） |
| `regulatory_item_quantity` | 0.5443 | 0 | **0** | 全部章节内的**监管条目数** |
| `regulatory_item_quantity_2` | 0.7266 | 10 | 13 | 同上 |
| `sentiment_analysis_granularity_2` | 0.7266 | 6 | 7 | 情绪分析粒度（**元数据**，不作信号） |

### 1.2 三条结构性观察

1. **这是本战役见过的"最干净"字段面**：无后缀 / `_3` 档 9 个字段里 **7 个 aC = 0、userCount = 0**；最高的 `negative_sentiment_term_count_2` 也只有 14。
   对比 pv173（aC 88）与 order_book_imbalance（aC 97）——那两集的**数据集级 aC 骗人**（order_book 的两条近失 prod 0.81/0.80，直方图 `[0.7,0.8)` n=70/36）。
   本集的优势在**字段级**：几乎没有 prod alpha 用过这些具体字段。这是当前最强的"未被挖过"证据。
2. **全部 VECTOR**：每个元素 = 一个申报**章节**。必须先 `vec_*` 聚合才能进标量算子。
   这个结构带来一个别的数据集没有的自由度：**跨章节的截面统计**（`vec_stddev` / `vec_range`）= 文件内部的**语气分歧**，属 news-sentiment skill 的 HIGH 优桶（Dispersion），而绝大多数 filing alpha 只用了整体语气。
3. **更新频率是季度（10-K/10-Q）+ 事件驱动（8-K）**：日频序列大部分日子是 NaN，`ts_backfill` 必带。
   慢变量 ⇒ 换手天然低 ⇒ F 公式 `F = S·√(R/0.125)` 对低换手有利；但 2Y 会吃"最近两年只有 8 个申报点"的亏——这是本集最大的风险面（§2.3 第 6 条）。

## 2. 机制与表达式设计

### 2.1 机制清单（M1–M7，文献锚点）

| # | 机制 | 字段 | 方向 | 文献锚点 |
|---|---|---|---|---|
| **M1** | **语气水平**：负面语气预示负收益 | `mean_sentiment_score` / `aggregate_sentiment_score_2`（取负号） | 负 | Loughran & McDonald (2011) *When Is a Liability Not a Liability?* — 负面词表在 10-K 中显著预测低收益 |
| **M2** | **跨章节语气分歧**（HIGH 桶） | `vec_stddev(mean_sentiment_score)` | 待定 | 披露内部不一致 / 管理层"各章说法不一"⇒ 不确定性折价；与 Loughran-McDonald (2014) 可读性一族同源 |
| **M3** | **语气漂移**：相对自身历史的恶化 | `ts_av_diff(vec_avg(mean_sentiment_score), 252)` · `ts_delta(..., 66)` | 负 | 语气持续性/反转文献；季度申报的同比语气变化 |
| **M4** | **申报长度异常**（复杂性） | `ts_zscore(vec_avg(total_word_quantity_2), 252)` | 负 | Loughran & McDonald (2014) *Measuring Readability*：更长的 10-K ⇒ 更低后续收益（信息遮蔽） |
| **M5** | **附注/子节复杂度** | `ts_zscore(vec_avg(financial_note_quantity_2), 252)` | 负 | 会计复杂度折价（附注越多 ⇒ 越难估值） |
| **M6** | **事件强度**：监管条目数异常 | `ts_zscore(vec_avg(regulatory_item_quantity_2), 252)` | 负 | 条目数飙升 = 非例行事项（并购/减值/诉讼）⇒ 风险溢价 |
| **M7** | **长度归一化语气率** | `neg/(pos+ε)`、`pos/(neg+ε)` | 负 / 正 | 把 M1 从"词数"里剥出来；对申报长度稳健 |

### 2.2 通用壳（与 pv173 同壳，便于跨集比较）

```
quantile(group_rank(winsorize(ts_backfill(<SIG>, 252), std=4), subindustry))
```

- 必须 `vec_*` **先**聚合，再进 `ts_backfill`（VECTOR 直接给 ts_* 会报类型错）。
- `std=4` 的 `std` 会被 `preflight_expressions` 误报为未知字段（已知误报，不是错误）⇒ 派发用 `validate_fields=false`。
- **`vec_range` 不进本批**：平台 `get_operators` 有它，但 `preflight` 的算子表不识别（报 `unknown_fields: ["vec_range"]`）。
  一个语法/算子错会 CANCELLED 整批 ⇒ 探针批只用预检认得的 `vec_avg` / `vec_stddev`。

### 2.2.1 批 1 表达式清单（10 条 = 5 机制 + 1 反号对照 + 2 覆盖档对照 + 2 复杂度）

| # | 机制 | 桶 | 信号 | 说明 |
|---|---|---|---|---|
| 1 | M1 语气水平 | Level/Direction | `vec_avg(mean_sentiment_score)` | 低覆盖档（0.544）主证 |
| 2 | M1 语气水平 | Level/Direction | `vec_avg(aggregate_sentiment_score_2)` | 高覆盖档（0.7266）主证 |
| 3 | M7 归一化语气率 | Direction | `neg/(pos+1e-4)` | **负向**主证 |
| 4 | M7 反号对照 | Direction | `pos/(neg+1e-4)` | 与 #3 成对（skill 要求的反号变体） |
| 5 | **M2 跨章节分歧** | **Dispersion（HIGH）** | `vec_stddev(mean_sentiment_score)` | 低覆盖档 |
| 6 | **M2 跨章节分歧** | **Dispersion（HIGH）** | `vec_stddev(aggregate_sentiment_score_2)` | 高覆盖档（覆盖对照） |
| 7 | M3 语气漂移 | Change | `ts_av_diff(vec_avg(mean_sentiment_score), 252)` | 2Y 杠杆预置（USA override 指定 `ts_av_diff`） |
| 8 | M3 季度语气变化 | Change | `ts_delta(vec_avg(aggregate_sentiment_score_2), 66)` | 66 ≈ 一个季度 |
| 9 | M4 申报长度异常 | Complexity | `ts_zscore(vec_avg(total_word_quantity_2), 252)` | 高覆盖档 |
| 10 | M6 监管条目异常 | Event intensity | `ts_zscore(vec_avg(regulatory_item_quantity_2), 252)` | 高覆盖档 |

桶覆盖：Level/Direction（4）+ Dispersion（2，≥1 HIGH ✓）+ Change（2）+ Complexity/Event（2）= **5 个桶**。
形状：均值 / 比率 / 标准差 / 差分 / z 分 = **5 种**。

### 2.3 预注册止损（先写死，回测后不得改判据）

1. **7 条底层信号全部 `|S| < 1.0`** ⇒ 判弱封存 `USA-FILINGSENT-WEAK`，不补批。
   （21 个字段全部落在"语气 / 长度 / 结构计数"三类，剩余自由度是覆盖档与 `vec_*` 聚合，属同族磨参。）
2. 全部 `risk_neutralized_sharpe < 0.3` ⇒ 纯情绪/规模风格 beta，直接封存。
3. 任一 `|S| ∈ [1.25, 1.58)` 且 rns ≥ 0.5 ⇒ Mode A，**先测 prod**（D0-P）。
4. 任一 RA 全闸 ⇒ 立刻 `check_correlation(refresh=True)`；prod ≥ 0.7 按 D0-P 留池/封存，< 0.7 才报为可交付候选（提交仍需用户确认）。 <!-- from config.prod_corr_max -->
5. **换手 > 0.3 不许缩窗救**：申报是季度事件，缩窗只会把信号变成申报日的脉冲；宁可换机制。
6. `2Y < 1.6` 但 S/F 过 ⇒ 只跑一轮 `ts_av_diff` 短窗杠杆（`252 → 66`），不灵即判该机制不耐 2Y。
7. `CONCENTRATED_WEIGHT` ⇒ 先归因（本集两档覆盖 0.544 / 0.7266 **均 > 0.4**，CW 不该出现；出现即说明 `vec_*` 聚合产生了单点权重）。

### 2.4 数据集切换理由（pv173 → filing_sentiment）

1. **pv173 已按预注册规则 #1 封存**（8 信号全 `|S| < 1.0`，最高 0.72），见 `_usa-pv173-field-profile-20261021.md` §3–§5。继续在 pv173 补批 = 违反自家止损。
2. **order_book_imbalance 的两条近失已测 prod，均判族级死**：`XgbZ2aaX`（S 1.78 / rns 1.94）prod **0.8133**、`O0NdbW61`（S 2.23 / rns 2.24）prod **0.7975**；
   直方图 `[0.7,0.8)` 分别是 **n=70 / n=36** ⇒ 按族级判据（n≥1 必死）不可救。**该集数据集级 aC 97 完全掩盖了信号族的拥挤度。**
3. **剩余面盘点（166 个 USA 数据集全量拉取，2026-10-21）**：未点亮塔且 aC < 300 的有 47 个；剔除
   ① 纯元数据映射表（`other250` / `other128` / `other424` 的描述都是 BBID↔RIC 映射，无信号）、
   ② 本战役已结案集（fundamental 23 集 / other 14 集 / pv173 / order_book / shortinterest / institutions）、
   ③ analyst 修正族近亲（`other685` = StarMine EQ + **ARM**，与已判死的 revision 族同源）、
   之后剩 `filing_sentiment`（aC 42）、`workforce_flow_skills`（aC 67）、`stock_cluster_dl`（aC 8）、`other359`（aC 84）、`other699`（aC 219）。
4. **选 `filing_sentiment` 的判据**：① **字段级** aC 中位数 0（不是数据集级 42）——9 个字段从未被任何 alpha 用过；
   ② 21 个 VECTOR 字段提供 `vec_stddev` 这个 HIGH 桶自由度（其余四个候选都是标量集）；
   ③ 监管申报是**原始 Fundamental 披露**，与已交付 5 颗的 analyst 修正/增长/偏度机制正交；
   ④ valueScore 5 + 金字塔乘数 1.4（other 塔未点亮）。
5. **本集只此一批探针**；未出信号即按 §2.3 封存，不再换视图/覆盖档重试。

### 2.5 论坛取证（负结果）

两轮检索（`10-K filing sentiment tone` / 公司债 z-spread）**均无专题帖**：命中的是 MCP 七十二变模板汇总与 K-means 选 alpha 的通用帖，没有 filing 语气/申报结构的实证。
记录：**"论坛没有 filing_sentiment 的现成经验"**——与字段级 aC≈0 一致；反过来说，本集的任何结论都要靠自测，没有二手背书。

---

## 3. 回测结果

批 1 `VYL9AbA35ic9vHLhaHXvtl`（10 表达式 / 10 COMPLETE / **0 ERROR**），设置 USA / TOP3000 / D1 / SUBINDUSTRY / decay 5 / trunc 0.08 / nan ON / maxTrade OFF。金字塔全部 `USA/D1/OTHER ×1.4`（未点亮）。

| # | 机制 | 信号 | alpha id | S | F | TO | R | DD | 2Y | SUB | rns | 失败闸 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 1 | M1 水平 | `mean_sentiment_score` | E5VpQ1GP | 0.28 | 0.07 | 1.68% | 0.88% | 8.07% | **−0.65** | 0.27 | −0.39 | S/F/2Y |
| 2 | M1 水平 | `aggregate_sentiment_score_2` | 0mjXPqwK | 0.36 | 0.11 | 6.86% | 1.09% | 11.73% | 0.41 | 0.29 | −0.25 | S/F/2Y |
| 3 | M7 负/正比 | `neg_2 / pos_2` | 2rjw5Ml5 | 0.38 | 0.12 | 6.84% | 1.29% | 5.54% | 0.14 | 0.28 | −0.50 | S/F/2Y |
| 4 | M7 反号 | `pos_2 / neg_2` | RRAbeM7g | 0.32 | 0.09 | 6.87% | 0.97% | 6.86% | −0.06 | **0.09** | −0.16 | S/F/**SUB**/2Y |
| 5 | M2 分歧（HIGH） | `vec_stddev(mean_sentiment_score)` | 0mjXPqRK | 0.55 | 0.21 | 1.70% | 1.80% | 6.98% | 0.38 | 0.42 | **−0.04** | S/F/2Y |
| 6 | M2 分歧（HIGH） | `vec_stddev(aggregate_sentiment_score_2)` | j2eAav3e | 0.32 | 0.09 | 6.92% | 0.99% | 11.30% | 0.50 | **0.02** | −0.30 | S/F/**SUB**/2Y |
| 7 | M3 漂移 | `ts_av_diff(mean_sentiment_score, 252)` | vROrA8kb | **0.64** | **0.26** | 2.37% | 2.07% | 5.26% | 0.54 | 0.51 | **+0.23** | S/F/2Y |
| 8 | M3 变化 | `ts_delta(aggregate_sentiment_score_2, 66)` | xA13vq3w | 0.36 | 0.09 | 1.72% | 0.82% | 5.88% | 0.30 | 0.35 | −0.28 | S/F/2Y |
| 9 | M4 篇幅异常 | `ts_zscore(total_word_quantity_2, 252)` | WjLblMbP | 0.52 | 0.19 | 7.27% | 1.75% | 7.44% | **0.66** | 0.41 | −0.23 | S/F/2Y |
| 10 | M6 条目强度 | `ts_zscore(regulatory_item_quantity_2, 252)` | bl8baXbm | 0.38 | 0.12 | 7.03% | 1.28% | 9.84% | **0.68** | **0.05** | −0.37 | S/F/**SUB**/2Y |

全部 10 条 **通过** `LOW_TURNOVER` / `HIGH_TURNOVER` / `CONCENTRATED_WEIGHT` / `MATCHES_PYRAMID`；`CLUSTER_TEST` 仅 warning（0.24–0.50，线 1.58）。**无一条 RA 全闸 ⇒ 未消耗 prod 槽位**（预注册规则 #4 未触发）。

**平台读数自洽校验**（F 公式，`TO < 12.5%` 时 `F = S·√(R/0.125)`）：#7 `0.64·√(0.0207/0.125)=0.26`、#5 `0.55·√(0.0180/0.125)=0.21`、#1 `0.28·√(0.0088/0.125)=0.07`，三条逐位命中平台值 ⇒ 本批读数无异常口径。

## 4. 归因

### 4.1 预注册规则 #1 触发：7 条底层信号全部 `|S| < 1.0`（最高 0.64）

| 机制 | 代表 | S | 判读 |
|---|---|---|---|
| M1 语气水平 | #1/#2 | 0.28 / 0.36 | 语气**水平**在美国大盘无截面预测力——与 Loughran-McDonald 的"语气解释力来自**变化**而非水平"一致 |
| M2 分歧（HIGH 桶） | #5/#6 | 0.55 / 0.32 | 见 §4.2，**效率最高但 rns ≈ 0** |
| M3 漂移 | #7/#8 | **0.64** / 0.36 | 本批最强，`ts_av_diff(252)` 是同族唯一有 rns 的形态 |
| M4 篇幅 | #9 | 0.52 | 近期（2Y 0.66）比全期强，但强度不足 |
| M6 条目强度 | #10 | 0.38 | 2Y 0.68 最高、SUB 0.05 最差 ⇒ 近期单边行情，不可靠 |
| M7 负/正比 | #3/#4 | 0.38 / 0.32 | 符号方向对（负向词权重更高），但反号版 SUB 0.09 vs 原版 0.28 ⇒ 原方向是正确的一侧 |

**整体判断：这不是"某一机制没找准"，而是数据集信息量上限。** 21 个字段全部属于"语气 / 篇幅 / 结构计数"三类，且都在**季度申报**频率上更新；`ts_backfill(252)` 之后日频上大部分交易日是同一份申报的同值，截面排序的变化来源只有申报事件本身。同族再换聚合（`vec_min` / `vec_max` / 覆盖档 `_2` / 窗口）只能改噪声的相位，不可能把 0.64 推到 1.58。

### 4.2 HIGH 桶（`vec_stddev` 分歧）的失败方式：效率冠军、alpha 为零

`vec_stddev(mean_sentiment_score)`（#5）是全批**边际效率冠军**：margin **0.2112%**（其余 0.028–0.104%）、R/TO = 1.06（其余 0.11–0.48）。但 `rns = **−0.04**` ⇒ 这份收益在风格中性化后归零，即它卖的是**规模 / 波动 / 覆盖度**的截面暴露（申报语气离散度天然与大市值、多分析师覆盖负相关），而不是独立的申报信息。

这与 pv173 的价差水平族（`rns −0.02`，SUB 0.55 / 2Y 1.39 却毫无残差）构成**第二次同形实证**：**USA/D1 上"横截面分歧 / 离散度"类构造极易退化为风格 beta；`SUB` 与 `2Y` 都测不出来，只有 `rns` 能当场识破。** 该判据已写入交付日志 §4 方法论。

### 4.3 覆盖档假设被证伪：高覆盖 `_2` 档没有任何优势

预注册时把 `_2` 档（覆盖 0.7266）当"更可靠"的一侧，实测相反：

| 同一机制 | 低覆盖档（0.5443） | 高覆盖档 `_2`（0.7266） |
|---|---|---|
| 水平 | 0.28（TO 1.68% / R 0.88%） | 0.36（TO 6.86% / R 1.09%） |
| 分歧 | **0.55**（margin 0.2112%） | 0.32（margin 0.0285%） |
| 变化 | **0.64**（ts_av_diff，R 2.07%） | 0.36（ts_delta） |

高覆盖档的代价是**换手翻 4 倍**（1.7% → 6.9%），收益只多 0.2pp ⇒ 覆盖率买来的是更多申报事件（噪声），不是更多信息。**"选字段先看覆盖"这条先验在本集反向成立**：覆盖 0.544 + `ts_backfill(252)` 已足够覆盖 ~2950/3000 只（long 1374 / short 1678，0 CW），再高的覆盖只是把噪声灌进来。

### 4.4 2Y 不是约束：近期并不比全期差

预注册规则 #6 原本防备"季度事件不耐 2Y"。实测 2Y 值 0.14–0.68，其中 **#9 (0.66) / #10 (0.68) / #7 (0.54) 高于自己的全期 S**；只有 #1 的 2Y 为负（−0.65）。⇒ **失败不是 regime 依赖，而是全期信噪比不足**。这条反过来排除了"换 2Y 杠杆能救"的路径（规则 #6 的短窗杠杆本批**不执行**：S/F 从未过线，执行它就是磨参）。

### 4.5 换手双峰结构 = 字段更新频率指纹

TO 明显分成两簇：**~1.7%**（`mean_sentiment_score` 的水平 / 分歧 / ts_delta 与 `ts_av_diff`、`ts_delta` 落在 1.72–2.37%）与 **~6.9%**（所有 `aggregate_sentiment_score_2` 与两个计数 z 分、比率）。前者是低频聚合（多年平滑），后者随申报事件跳变。两簇的 S 分布（1.7% 簇含 0.28/0.55/0.64/0.36；6.9% 簇含 0.36/0.32/0.38/0.32/0.52/0.38）说明**换手高低与信号强弱无关**——高换手组全部落在 0.32–0.52，没有一条靠"更多事件"换来强度。

### 4.6 论坛取证（负结果，与 §2.5 一致）

本批结论无二手背书：论坛无 filing sentiment 专题，回测后也未出现与公开文献冲突的读数。Loughran & McDonald 的"语气变化 > 语气水平"在方向上被验证（M3 0.64 > M1 0.28–0.36），但**幅度不足以在 USA/D1 的 1.58 线下成交易信号**——这是一条可复用的负结论：**文本语气类信号在美国大盘的可用窗口已被分析师修正族吃干，原始申报语气只剩风格 beta 残渣。**

## 5. 决策

**按预注册规则 #1 封存：`USA-FILINGSENT-WEAK`。不补批、不入池、不报告为候选。**

- **不补批的依据**：最高 `|S| = 0.64`（距 1.25 的 RA 线还有 0.61，距 1.58 的平台显示线 0.94），且失败面覆盖全部 7 个机制、2 个覆盖档、5 种形状。剩余自由度（`vec_min` / `vec_max` / 窗口 / 中性化）全部属同族磨参，按纪律禁入。
- **不测 prod**：无一条 RA 全闸，预注册规则 #4 不触发；本集未消耗任何 prod 相关性槽位。
- **不入 salvage**：`S < 1.0` 的弱候选不满足收集门槛（salvage 收集宽、动用严，但下限仍需 ≥1.0）——见 `_usa-atom-delivery-log-20261020.md` §4。
- **交付计数不变：5 / 10**（ACTIVE：`omoK1A5m` / `akVnvzX5` / `gJWoaJqv` / `kqJLawqP` / `e76xgXkM`）。

### 5.1 三条可复用结论（已同步至交付日志 §4）

1. **带符号的 `rns` 是本轮唯一能识破"高效率假信号"的读数**：`vec_stddev` 分歧族 margin 0.2112%（同批 2–7 倍）、R/TO 1.06，但 `rns −0.04`；pv173 价差水平族同形（`rns −0.02`）。**结论：先看 rns 再看 SUB/2Y——SUB 0.42–0.55 + 2Y 1.3–1.4 可以和 rns≈0 并存。**
2. **覆盖档先验在申报类数据上反向**：高覆盖 `_2` 档（0.7266）把换手抬 4 倍（1.7% → 6.9%）只换来 +0.2pp 收益；覆盖 0.5443 + `ts_backfill(252)` 已足够交易 ~2950/3000 只。**低覆盖 + 长 backfill 的"弱字段"未必比高覆盖差。**
3. **文本语气类在 USA/D1 的可用窗口已被分析师修正族占满**：Loughran & McDonald 的"变化 > 水平"方向成立（0.64 vs 0.28–0.36），但绝对强度只有 RA 线的 40%。后续再遇到同族数据集（`ai_news_scores` / `event_sentiment_signals` / `sentiment21` / `forum_sentiment` 已全部判死或判弱），**不要重复开批**，直接引用本条。
