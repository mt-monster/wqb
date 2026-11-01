# news46 数据集画像（KOR / TOP600 / Delay=1）

> 手工维护。数据源：**平台 `get_datafields(KOR, TOP600, D1, dataset=news46, filter_sharpe=false)` 实测 44/44 字段**（2026-10-30，权威）。
> 塔：**NEWS**（未点亮，倍率 1.6）。字段全部来自 **RavenPack 新闻分析**（`mws46_*` = market-wide story 46）。

## 0. 元信息

| 项 | 值 |
|---|---|
| dataset id | `news46` |
| category | **NEWS**（塔 0 点亮，乘数 1.6） |
| 字段数 | **44**：**40 VECTOR + 4 MATRIX**（`mws46_ravenpack_*` 聚合族是 MATRIX） |
| 覆盖率 | **两档：.3935（64%）/ .2497（36%）** —— 均 **< 0.4**，须 `ts_backfill` |
| 拥挤度 | **极低**：单字段 aC 最高 22（`sum_ssc`）/ 21（`sum_nip`）/ 20（`sum_ssc`），多数 = 0–2 |
| 性质 | 供应商（RavenPack）新闻结构化：情绪分(ESS/SSC) + **新颖度(ENS)** + **冲击预测(NIP)** + **相关度(relevance)** + 故事计数 |

⚠ **覆盖率只有两档** ⇒ 实际是同两套抽取口径：`.3935` 档（含 `story_count` / `relevance` / `ssc` / `nip` / 公司行为分）与 `.2497` 档（**新颖度 ENS 全族 + `ess`**）。
**新颖度族的覆盖明显更小**（.2497）⇒ 十年覆盖风险在该族最高，**必须首波实核**。

## 1. 字段分类（按 description 语义）

### A. 新颖度 / 事件新鲜度（VECTOR，cov .2497）—— ★ 本集**唯一机制独立**的轴

| 字段 | aC | 语义 |
|---|---|---|
| `mws46_ens` / `mws46_g_ens` | 0 / **2** | 事件新颖度 0–100（24h 内故事有多"新"）；`g_` = 跨供应商全局口径 |
| `event_novelty_rating` / `global_event_novelty_rating` | 0 / 0 | 同上的长名版本（**疑同源重复**） |
| `mws46_ens_elapsed` / `mws46_g_ens_elapsed` / `global_novelty_time_difference` / `event_novelty_time_difference` | 0 / 2 / 0 / 0 | **距链首故事经过的毫秒数** ⇒ 越小 = 越早拿到消息 |
| `mws46_ens_key` / `mws46_ens_key_off` | 0 / 0 | **事件链 ID（字母数字）** ⇒ 标识符，禁作信号 |

⇒ **可作信号的只有 `ens`（分）+ `ens_elapsed`（时滞）**。`_key` 是字符串 ID。

### B. 相关度 / 显著度（VECTOR cov .3942 或 MATRIX cov .3935）

| 字段 | aC | 语义 |
|---|---|---|
| `entity_news_relevance_score` / `mws46_relevance` | 0 / 0 | 实体与故事的相关强度 0–100 |
| `mws46_ravenpack_mean_relevance` / `sum_relevance` | **12** / **17** | 同上，MATRIX 聚合版 ⇒ ⭐ **本集最不拥挤却可用的一支** |

**机制价值**：相关度是**信噪比闸**——低相关度消息是噪声，不该触发交易；高相关度才是真信息。
⇒ 正解是**门控**（`trade_when(relevance>T, 情绪信号, -1)`）而不是直接当收益来源。

### C. 冲击预测（VECTOR cov .3942 / MATRIX cov .3935）

| 字段 | aC | 语义 |
|---|---|---|
| `mws46_nip` / `news_volatility_impact_projection` | 2 / 0 | 预测**未来 2 小时**的市场冲击 0–100（按时段缩放） |
| `mws46_ravenpack_mean_nip` / `sum_nip` | 15 / 21 | 同上，MATRIX 版 |

⚠ **NIP 是供应商的预测值**，不是可观测基本面 ⇒ 用它等于用第三方 alpha，**且 `sum_nip` aC=21 已是最拥挤支**。机制上它有极强经济含义（预测冲击），但**窗口只有 2 小时 = 日频采样根本抓不住** ⇒ 日频上它退化为「当天消息强度」。按假说处理。

### D. 情绪分（VECTOR cov .2497–.3942 / MATRIX cov .2536–.3935）—— ⛔ **红线：本族与已判死的 news 情绪/事件评分族同机制**

`mws46_ess` / `event_specific_sentiment_score`（aC 1）/ `mws46_ssc` / `composite_story_sentiment_score` /
`mws46_ravenpack_mean_ess`(**17**) / `sum_ess`(18) / `mean_ssc`(**22**) / `sum_ssc`(20) /
`positive_negative_word_sentiment_score` / `editorial_commentary_sentiment_score` / `future_earnings_projection_sentiment` /
`merger_acquisition_sentiment_score_3` / `corporate_action_sentiment_score` / `mws46_mcp` / `mws46_mcr` / `mws46_mcv` / `mws46_mce`

⇒ 按 roadmap §4，**新闻情绪 / 标题语气 / 事件评分族在 KOR 已多次判死**（news38、news50、news87/96/141、mmp_nlp、model37、news_sentiment_transfer；本campaign wave 188 又死一次）。
**本族只有在「被 A 族新颖度或 B 族相关度门控」时才允许试，且必须标注为复用已死机制。**

### E. 计数 / 标识符（禁作信号）

`mws46_story_count`(2) / `mws46_ravenpack_sum_story_count`(10) / `story_entity_record_count`(1) —— **注意力计数族，wave 188 已在 news7 上判死**（S 0.55 / 2Y −0.34）。
`mws46_story_index` / `mws46_time`（发布时间）/ `mws46_news_type`（编码）/ `mws46_elw`（词表命中分）—— 标识符或编码，**禁作信号**（时戳类同 roadmap §4 `oth496_*_t` 禁令）。

## 2. 名 vs description 差异表（★ 陷阱）

| 字段 | 名字暗示 | description 实际 | 处置 |
|---|---|---|---|
| `mws46_g_ens` | 全局新颖度 | "across **all providers**" vs `mws46_ens` 的 "within the given **package**" | 两者**口径不同不可互换**：`g_` 是跨供应商去重，`ens` 是包内去重。**正解 = 二者之比 = 跨供应商扩散度**（同源价差，合规） |
| `mws46_ens_elapsed` | 新颖度 | 实际是 **"Elapsed time in milliseconds"** ⇒ 量纲 1e4–1e6 | **禁裸当连续值**，必须 `rank`/`ts_rank`；且**越小越"早"**，符号与 `ens` 相反 |
| `event_novelty_rating` vs `mws46_ens` | 两个字段 | description 几乎逐字相同（同为 0–100 24h 新颖度） | **疑同源重复**：不可当两个独立信号铺量 |
| `mws46_ravenpack_mean_*` vs `sum_*` | 均值 vs 和 | `sum` = 窗口内聚合总和，`mean` = 均值 | `sum` = **强度 × 条数**（混了注意力），`mean` = **纯强度** ⇒ **选 `mean`**（避开已死的注意力轴） |
| `mws46_nip` | 冲击 | "over the next **two hours**" | 日频采样下窗口不匹配 ⇒ 当"消息强度"用，不是真冲击预测 |

## 3. 字段画像五问（A-1）

1. **时间维度**：**流量 / 事件**（每条故事一个分），不是存量 ⇒ 需 `ts_mean`/`ts_decay_linear` 聚合成日频强度。
2. **相对性**：**横截面排序差异**为主（0–100 分本身可比）；`elapsed` 是量纲型 ⇒ 必须秩化。
3. **被定价的是谁**：**信息到达速度**（谁先看到）+ **信噪比**（消息有多相关）。不是情绪方向。
4. **有无博弈**：有。消息新鲜度是**争先**博弈，2 小时窗口内的高频资金吃掉大部分，日频只剩残差 ⇒ **强度预期偏低**。
5. **事件性**：**是**（无消息日为空）；cov .25–.39 ⇒ `ts_backfill` 必须，且**禁裸 `rank`**。

## 4. A-2 收益来源声明（主机制：信息新鲜度 × 信噪比 → 反应不足/过度反应）

| 项 | 内容 |
|---|---|
| **谁在被定价** | **信息处理能力受限的投资者**（日频资金）。供应商给出「这条消息有多新」与「这个实体在消息里有多核心」，但**日频价格只消化其中一部分**。 |
| **为什么会被错** | **注意力分配摩擦**（限注意力）：高新颖度消息需要更多加工成本才被定价 ⇒ 反应不足；低相关度消息却是噪声，会引发过度反应。两者是**相反方向**的错误。 |
| **错了多久修复** | 新颖度 ⇒ 数日到 2 周（`ens_elapsed` 以毫秒计 ⇒ 原始事件尺度是分钟到小时，日频只剩长尾）；相关度门控 ⇒ 1–4 周。 |
| **预期方向** | **新颖度高 + 相关度高 ⇒ 反应不足 ⇒ 做多信息方向**；但本集没有"信息方向"的干净代理（情绪族已判死）⇒ 只能做**排序型**：新颖度相对高的股票 → 后续相对跑赢。**方向必须正反各测**（铁律 B）。 |
| **失效条件** | ① 日频采样丢失 2 小时窗口（NIP 尤其）；② `ens` 覆盖 .2497 ⇒ 一半股票无读数，横截面排序被覆盖差主导；③ KOR 新闻供应商覆盖以大盘为主 ⇒ 与规模因子混淆。 |

## 5. 双通道取证

**通道 A（论坛）** —— ✅ **已取证（2026-10-30 04:25:12）**：`tools/forum_recon.py`，检索式 `event novelty`，`found=true / 5 篇`，
`question_key=20fb5f46f6`，`status=ok`（**不是工具故障**），写入 `KB/community_tpl_kb.forum_recon_entries[6..10]`。

| 帖 | 票 | 与本机制的关系 | 可继承内容 |
|---|---|---|---|
| `33566303033751` **Data Idea 系列3：Global News Data_news48** | 16 | ⚠ **不同数据集**（news48），只是同一「新闻字段逐个探索」的系列帖 | 无表达式可搬；只提供「先逐字段 LAB 探索再组装」的流程样板 |
| `42683370522775` **trade_when 的正确打开方式：止盈止损与月度调仓** | 30 | 通用算子帖，不涉新闻 | ⭐ **可继承**：`trade_when` 的月度调仓模式可作压 TO 的备选（本集是日频新闻，TO 是主要风险） |
| `34967922443543` **寻找阿尔法：新闻与社交媒体** | 0 | 唯一直接谈 RavenPack 语义的帖 | ⭐ **语义纠正**：作者称 `rp_nip_assets` 表示**新颖性/独特性**（而本画像 C 族按「冲击预测」归类）⇒ **NIP 语义存在两种解释，表达式中两个方向都要测**（本波已按 ± 各一条设计） |
| `33554030316183` **Data Idea 系列2：News Sentiment Data_news54** | 13 | 情绪族系列帖，作者自述**上一期无人找到 alpha** | ⚠ 反向证据：与本画像「D 族情绪分同族已判死」方向一致 |
| `42545425026071` **【Vector 字段】报错不等于不可用** | 20 | 纯算子纪律 | ⭐ **可继承**：VECTOR 字段必须用 `vector_*` 包裹（报错 ≠ 不可用）；本集 `mws46_*` 有 40 个 VECTOR ⇒ 与 `vec_avg` 降维口径一致 |

**通道 A 裁决：无本机制专属表达模板**（5 篇里 0 篇给出 news46 新颖度/相关度的可用表达式）。
只捞到三条非机制纪律：① NIP 语义二义（± 都测）；② `trade_when` 月度调仓可压 TO；③ VECTOR 必须 `vector_*` 包裹。
⚠ 与 other106 那轮同形（`status=ok` 但无专属模板）⇒ **下波不应再用 `event novelty` 检索式空转**；若再查，换
`"ravenpack ens"` / `"information novelty decay"` / `"news relevance threshold"`，且先读 `Data Idea 系列3` 正文（本集最接近的一篇）。

**通道 B（论文）**：

| 文献 | 可证伪结论 | 本区可迁移性 |
|---|---|---|
| **Tetlock (2011, RFS) "All the News That's Fit to Reprint"** | **重复（陈旧）新闻** ⇒ 投资者反应更弱、后续反转更小；**新信息** ⇒ 反应更强 | ⭐ 直接给 `ens`（新颖度）的方向句 |
| **Chan (2003, JFE) "Stock Price Reaction to News and No-News"** | 有新闻组的动量强于无新闻组 ⇒ 消息触发**反应不足** | ⭐ 给「新颖度 ⇒ 漂移」的持有期（1–12 月，本区取 22–66 日） |
| **Huberman & Regev (2001, JF)** | 同一信息**重复报道**即推动股价 ⇒ 媒体本身是定价因子 | 给「重复 ⇒ 过度反应」的反向腿 |
| **Boudoukh, Feldman, Kogan & Richardson (2013, RFS)** | 新闻**时效衰减极快**（数日），慢变量才是长期驱动 | ⚠ 预警：日频上新颖度信号可能已衰减殆尽 |
| **Fang & Peress (2009, JF)** | 无覆盖股有信息摩擦溢价 | 本集 cov .25–.39 ⇒ **覆盖差本身是混淆项**，须在表达式中控覆盖 |

⚠ **文献偏误**：全部 USA 样本；KOR 新闻供应商结构与英文不同。**先当假说**。
⚠ **本集还有一个更根本的偏误**：RavenPack 的 `ens`/`nip` 是**供应商自己的模型输出**，用它们等于复刻供应商 alpha ⇒ 若论坛已有大量人用，prod 相关性会高（虽然当前 aC 只有 0–2，说明还没人用）。

## 6. 近十年覆盖验证（用户约束 4）

⚠ **本集覆盖风险是全部候选中最高的一档**（.2497 的新颖度族 + 供应商数据）。
**判定法**：首波回测后立刻 `get_alpha_yearly_stats`；**首 3 年任一为空 ⇒ 整集退出**，不再投后续槽。

✅ **实测结论（2026-10-30，wave 191 批 1）**：`58ENYomN` 逐年 longCount **291–340（2014–2023 全覆盖）** ⇒ **本集覆盖合格**，
但因机制判死而不再投主攻槽（详见 §7.1）。

## 7. 波次设计（**wave 191** 实发版，8 条；已 `preflight_expressions` 全清 `valid:true / unknown_fields:[]`）

> 与初稿（§7 早期草表）的差异：改用 **MATRIX 预聚合族 `mws46_ravenpack_mean_*`**（平台已替我们做过聚合，aC 6–22 说明是"被用过的版本"，
> 比自己在 VECTOR 上写 `vec_avg` 少一层自由度）；`mws46_nip` / `entity_news_relevance_score` 留作次波（本轮不铺）。
> ⚠ 第 8 条是**阴性对照**：`sum_story_count` 属 wave 188 已判死的注意力计数族 —— 它若出强信号，说明本波读数被注意力轴污染。

| 序 | 表达式 | 机制 / 目的 |
|---|---|---|
| 1 | `group_rank(ts_rank(ts_backfill(divide(vec_avg(mws46_ens), add(1, vec_avg(mws46_g_ens))), 22), 252), sector)` | ⭐ **同源比值** = 包内新颖度 / 全局新颖度 ⇒ **信息扩散度**（本波主假设） |
| 2 | `group_rank(multiply(-1, ts_rank(ts_backfill(divide(vec_avg(mws46_ens), add(1, vec_avg(mws46_g_ens))), 22), 252)), sector)` | 铁律 B：显式反号（`reverse()` 非精确反号） |
| 3 | `group_rank(ts_rank(ts_backfill(mws46_ravenpack_mean_ens, 22), 252), sector)` | A 族 新颖度**水平**（MATRIX 预聚合版） |
| 4 | `group_rank(ts_rank(ts_backfill(mws46_ravenpack_mean_relevance, 22), 252), sector)` | B 族 相关度水平 = 信噪比 |
| 5 | `group_rank(ts_rank(ts_backfill(mws46_ravenpack_mean_nip, 22), 252), sector)` | C 族 冲击强度（NIP 语义二义，见 §5 A 通道 ⇒ 正反各一） |
| 6 | `group_rank(multiply(-1, ts_rank(ts_backfill(mws46_ravenpack_mean_nip, 22), 252)), sector)` | 同上反号 |
| 7 | `group_rank(multiply(-1, ts_rank(ts_backfill(vec_avg(mws46_g_ens_elapsed), 22), 252)), sector)` | 时滞（越短越新）⇒ 反号后 = **新鲜度** |
| 8 | `group_rank(ts_rank(ts_backfill(mws46_ravenpack_sum_story_count, 22), 252), sector)` | ⚠ **阴性对照**（注意力计数族已判死）；出信号即整波读数不可信 |

**准入**：
- 分组轴 **只用 `sector`/`market`，禁 `industry`**（KOR：三星+海力士 >50% 市值）。
- VECTOR 族一律 `vec_avg` 降维（§5 A 通道：VECTOR 必须 `vector_*` 包裹，报错≠不可用）。
- **禁 D 族情绪分裸用**；如后续要试，必须挂在 A/B 族门控下并标注复用已死机制。
- 每批 2 条串行（`--set _multi_sim_batch_size=2 --serial`）；**批 1 落地后第一件事读 `get_alpha_yearly_stats`**（本集覆盖风险最高，验完再谈 S）。
- **砍波判据（预置，照 wave 189/190 的纪律）**：批 1（第 1–2 条，主假设）落地后若 `max|S| < 1.0` **且** `max|2Y| < 1.0` ⇒ 主机制无信号，**剩余 6 条不发即 kill**，只写归因。

### 7.1 实测结果（wave 191，2026-10-30 收官；⛔ 机制判死）

**批 1**（multisim `1dLVy35Yb53ybmh1eLsNVY1z`）→ **判据触发，剩余 6 条未发即 kill**（批 2 在判据判定前已自动补槽，故实发 4 条）。

| 序 | alpha | S | F | 2Y | TO | 结论 |
|---|---|---|---|---|---|---|
| 1 | `58ENYomN` | **−0.36** | −0.11 | **−0.47** | .2382 | REJECT（主假设反向都不成立） |
| 2 | `qMLeVoaE` | +0.23 | +0.05 | +0.15 | .2381 | REJECT（铁律 B 反号后仍不显著） |
| 3 | `O0AKgZd1` | −0.35 | −0.10 | −0.10 | .2400 | REJECT（新颖度水平） |
| 4 | `JjeRrOan` | −0.47 | −0.13 | **−1.08** | .2801 | REJECT（相关度水平；IS 弱 2Y 强 ⇒ 背离不可信） |
| 5–8 | — | — | — | — | — | **NOT_DISPATCHED** |

- **覆盖判定 = ⭐ PASS（本集首次实测）**：`get_alpha_yearly_stats(58ENYomN)` 显示 **2014–2023 逐年 longCount 291–340**，全部有数
  ⇒ 满足用户约束 4；**死因是机制，不是数据**（与 sentiment27 的 2014–2018 连续零覆盖形成对照）。
- **CW = PASS**（4/4 未触发 0.1 线）：稀疏新闻型数据在 `ts_rank-252 + ts_backfill` 归一后权重健康 —— 这条读数可继承。
- **TO .238–.280** 是 KOR 成功带（.075–.136）的 2–3 倍，但 F 全负且随 S 同向 ⇒ 降 TO 只修 F 不改 S，**不构成救援路径**。
- **机制结论**：RavenPack 的 **新颖度（ens）/ 相关度（relevance）/ 新颖度净值率** 三个轴在 KOR 全部无信号。
  与 news7 注意力计数族（max|S| 0.55）合并看，**news 塔的"文本内容强度"与"注意力计数"两条大轴都已判死**。
- **继承给下一波**：news46 覆盖可用这条结论保留（可作跨塔门控字段的备选源），但**不再投 news46 主攻槽**；
  若未来再攻 news 塔，只剩「事件计数 / 时间模式」轴，且必须先过 `trade_when` 门控 + CW 实测。

## 8. 禁区

- `mws46_ens_key` / `mws46_ens_key_off` / `mws46_story_index` / `mws46_time` / `mws46_news_type` —— **标识符 / 编码 / 时戳，禁作信号**。
- `mws46_story_count` / `sum_story_count` / `story_entity_record_count` —— **注意力计数族已判死**（news7 wave 188）。
- D 族情绪分（ESS/SSC/各类 sentiment_score）**单用禁入**：与 news38/50/87/96/141 同族，KOR 多次判死。
- `mean_*` 与 `sum_*` **不可同时用**（`sum` 混入条数 = 注意力轴，已被证伪）。
- 本集属 **NEWS** ⇒ 不得与 PV/MODEL/OTHER 组腿（用户约束 5）；与其它非 PV/MODEL/OTHER 类组腿须单独申请配额。
- 全 VECTOR ⇒ 必须 `vec_avg`；cov < .4 ⇒ 必须 `ts_backfill`。
