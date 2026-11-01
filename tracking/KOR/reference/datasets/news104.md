# news104 字段画像（KOR / D1 / TOP600）

> 快照日：2026-10-30。来源：`mcp__wq_brain_http__get_datafields(dataset_id=news104, filter_sharpe=false)` 全量拉取（11/11，complete=true）。
> 定位：NEWS 塔（平台倍率 **1.6**，KOR/D1 **未点亮**）。本集是 news 类里**唯一带「数值型预期收益」字段**的数据集，
> 机制与已判死的 tone / attention-count / novelty-relevance 三族**均不同**，故单列。

## 1. 数据集级读数

| 项 | 读数 | 判读 |
|---|---|---|
| category | news（×1.6，未点亮） | 未点亮塔里最高倍率 |
| 字段数 | 11，**全部 VECTOR**（平台 field_count=11，目录 11/11） | 全部须 `vec_*` 降维 |
| 覆盖率 | 全部字段 **0.2671** 完全一致 | 约 1/4 股票日有新闻；**十年连续性必须实测**（用户约束 4） |
| alphaCount | 2–40（`nws104_automessage` 40 最高，`marketimpactscore` 仅 **3**） | 近乎未开垦，prod 墙风险低 |
| valueScore | 4 | 平台自评偏高 |
| DB `dataset_profile.coverage` | 0.2671（与字段一致） | ⚠ 与 `query_dataset_profile` 里其他 news 集报出的 0.78–0.95 **不同源**；以后者筛集会误判，**一律以字段级 coverage 为准** |

## 2. 字段清单与语义（按 description 分类，禁按字段名）

**A. 数值型影响预测（⭐ 本集独有）**

| 字段 | cov | aC | 语义 |
|---|---|---|---|
| `nws104_marketimpactscore` | .2671 | **3** | 估计的**风险调整后 1 分钟前向收益**，约 −5…+5 ⇒ 是「消息冲击幅度」的**带符号数值**，不是文本情绪 |

**B. 情绪概率三元组（文本情绪族，已知在 KOR 全灭）**

| 字段 | aC | 语义 |
|---|---|---|
| `nws104_prob_pos` / `nws104_prob_ntr` / `nws104_prob_neg` | 2 / 3 / 8 | 三分类概率（0–1），三者互斥 |
| `nws104_sentiment` | 2 | 三值分类 1/0/−1 |
| `nws104_confidence` | 3 | 情绪标注置信度（**只能当权重/门控**，不能当信号主体） |

**C. 事件结构标记（本集第二个新轴）**

| 字段 | aC | 语义 |
|---|---|---|
| `nws104_novelty` | 5 | **1 = 首次报道；>1 = 24h 内重复/更新**（编号有方向但非连续量） |
| `nws104_automessage` | 40 | 1 = 系统定时生成（日历事件/机器 feed），0 = 人工稿 |
| `nws104_headlineonly` | 7 | 1 = 只有标题（快讯），0 = 有正文 |
| `nws104_relevance` | 1 | 1 = 主体是该公司，<1 = 次要提及 ⇒ **门控用** |
| `nws104_timestamp` | 5 | UTC Unix 秒 ⇒ **时间戳，禁作信号** |

## 3. 六法体检预判

- **更新频率**：事件驱动日频，`zero_inflated` 显著（cov .2671）。
- **中心趋势**：`marketimpactscore` **对称**（−5…+5）⇒ 铁律 A 不适用（不需要强制 `ts_delta`）。
- **量纲**：impact score 有界 ±5；概率 [0,1]；`novelty` 是计数比（1,2,3…）⇒ **不可与概率相加**。
- **覆盖**：无新闻日为空 ⇒ `trade_when(<有新闻>, …)`，**禁裸 rank**；`ts_backfill` 对事件型输入不适用（本区实证）。
- **稀疏性来源**：只有 1/4 股票日有新闻 ⇒ 排序型信号在空日是 NaN，中性化后权重集中 ⇒ **CW 风险是第一顺位检查项**。
- **crowding**：`marketimpactscore` aC=3 ⇒ 无 prod 同类墙风险。

## 4. A-1 五问（决定骨架方向）

| # | 问 | 答 | ⇒ 骨架 |
|---|---|---|---|
| 1 时间维度 | 存量/流量？ | 流量（每条新闻一次冲击） | 窗口内聚合（5 / 22d） |
| 2 相对性 | 水平/排序？ | 排序（行业内相对冲击） | `group_rank(·, sector)` |
| 3 被定价的是谁 | 广度/强度？ | **强度**（单条消息冲击幅度 + 符号） | 带符号聚合后取排序 |
| 4 有无博弈 | 拥挤/可投资性？ | 否（aC=3）；但空日持仓需门控 | 不上规模壳；`trade_when` 或 `hump` 控权重 |
| 5 事件性 | 稀疏事件？ | **是**（cov .2671） | `trade_when`，**禁裸 rank** |

## 5. A-2 收益来源声明（硬门）

- **谁在被定价**：对快讯反应过度的散户/算法（1 分钟级冲击被外推到日频）。
- **为什么会被错**：**过度反应**（Chan 2003, JFE：极端新闻组后续反转，无新闻组才漂移）+ 有限注意力（Barber & Odean 2008）。平台的 `marketimpactscore` 是**1 分钟前向收益**预测，D1 建仓时该冲击**已经走完**，剩下的是均值回复。
- **错了多久修复**：**数日**（2–10 日）⇒ 窗口 5 / 22d。
- **预期方向**：**当日/近日冲击越正 ⇒ 后续越跑输**（反转）；冲击越负 ⇒ 后续越跑赢。**方向必须按铁律 B 正反各测**。
- **边界**：无新闻日不建仓；`novelty>1`（重复播报）不含新增信息 ⇒ 只保留 `novelty==1` 的首次报道。

## 6. 双通道取证

- **通道 A（BRAIN 论坛，2026-10-30 实检）**：`search_forum_posts("news reversal overreaction market impact score D1")` 命中 10 篇，
  全部是**论文合集帖**（`【论文合集】量化研究推荐论文` 等，108 赞 / 1 评论），其中列有
  *Intraday News Trading: The Reciprocal Relationships Between the Stock Market and Economic News* 与 *Announcements* 两条参考文献，
  **无本机制专属模板、无 market impact score 的实盘表达** ⇒ 判 **A 无对应表达**。
  叠加本区既有反证：news 类 tone / hotlevel 族全灭（wave 141/144/157）、novelty/relevance 全灭（wave 191）、
  注意力计数全灭（wave 187b）、事件情绪背离全灭（wave 197）、`ts_corr(nip, returns)` 全灭（wave 199）。
  ⇒ **本波必须与上述五族做机制区分**：本波唯一新增量是「带符号的数值型冲击幅度」，不是文本极性、也不是报道计数。
- **通道 B（文献）**：
  - **Chan, W.S. (2003), JFE 68(2)**: "Stock price reaction to news and no-news: drift and reversal after headlines" —— 极端新闻组**反转**、无新闻组**漂移**（US，日频，持有 1 个月）。
  - Tetlock (2007, JF) / Tetlock et al. (2008, JF)：媒体悲观 → 下行（US）。
  - Da, Engelberg & Gao (2011, JF)：注意力冲击 → 短期买压 → 两周反转（US）。
  - **文献偏误**：全部 US 样本、多为大盘股；KOR 小宇宙（TOP600）+ 散户占比高 ⇒ 反转可能更强，但属**假说**。
- **裁决**：A 无表达 / B 有机制 ⇒ 按 `wq-brain-ra-kor` ②.d「**B 有机制、A 无对应表达**」档：**自建骨架**（用论文的方向句 + 持有期定形态），
  且**先做 4 条小批对照**，不铺 8 条。

## 7. 波次设计（wave 202，待实测，不是结论）

铁律 B（方向互测）+ 铁律 G（新线 ≤8 探针，本波取 4）+ 单波单机制族。

| leg | 表达式骨架 | 检验什么 |
|---|---|---|
| T1 | `hump(reverse(group_rank(ts_sum(vec_avg(nws104_marketimpactscore), 22), sector)), hump=0.003)` | 主假设：冲击反转（22d 累积冲击，取负向） |
| T2 | `hump(group_rank(ts_sum(vec_avg(nws104_marketimpactscore), 22), sector), hump=0.003)` | 铁律 B 反向对照（若 T2 显著优于 T1 ⇒ 方向是动量不是反转） |
| T3 | `hump(reverse(group_rank(ts_sum(vec_avg(nws104_marketimpactscore), 5), sector)), hump=0.003)` | 窗口对照：短窗（5d）冲击是否更贴反转 |
| T4 | `hump(trade_when(equal(vec_avg(nws104_novelty), 1), reverse(group_rank(ts_mean(vec_avg(nws104_marketimpactscore), 5), sector)), -1), hump=0.003)` | 机制精化：只保留**首次报道**（novelty==1），滤掉重复播报 |

⚠ **统一壳层 `hump=0.003`（同波一致）**：KOR 冠军壳，只为把换手压进 .075–.136 甜区——
wave 197 同族（news18）换手 0.1435–0.4374 曾把读数搅成「换手失败 vs 信号失败」不可分辨。
四条腿同加，**不影响腿间比较**；如实测全腿 TO 仍 >0.3，则下一波改壳而不是改核心信号。

⚠ **不加 `ts_backfill`**：VECTOR / 事件型输入在 KOR 不支持 `ts_backfill`；覆盖由 `ts_sum`/`ts_mean` 的窗口自然累积（cov .2671）。
⚠ **不裸 `rank`**：稀疏事件族，`trade_when(<novelty≥1>, …, -1)` 的持有语义由 T4 承担，T1–T3 用 `group_rank` + `ts_sum` 平滑。

**预置判死判据（写死，回测前不可改）**：若 4 腿 `max|S| < 0.8` 或 `max|2Y| < 0.8` 或全部 CW > 0.1 ⇒
判 **机制不成立**，本集关闭，不扫 decay / 窗口 / 中性化档。

## 8. 禁碰清单

- `nws104_timestamp`（时间戳）**禁作信号**；`nws104_prob_pos/ntr/neg` / `sentiment` 属**已判死文本情绪族**，只能当门控。
- `nws104_confidence` 只能当权重/门控，不能当信号主体。
- **禁与 PV / MODEL 数据集字段组腿**（用户硬约束 #5；PV+NEWS 全库上限 5，**当前已用 4**）。
- `news104` 与 `news76` / `news73` / `news3` / `news36` / `news84` / `news85` 同属 news 文本族 ⇒ **同机制只出一条腿**，
  本集 `marketimpactscore` 是唯一「数值型冲击」字段，不与上述文本字段同波。
