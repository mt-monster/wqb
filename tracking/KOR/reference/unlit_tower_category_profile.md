# KOR 未点亮塔 · category × dataset 画像与 60 颗排期

> 2026-10-30 · 数据源：平台 `get_pyramid_alphas`（塔位）+ 平台 `get_datafields`（字段存在性）+ 本地 `fields`/`datasets`（字段数与 alphaCount，离线零配额）
> 配套逐数据集专档：`tracking/KOR/reference/datasets/insiders5.md`（已建）；其余在首次开波前补齐同结构。
>
> ⚠ **本文件 = 机制读法（为什么打这个字段）**；
> **波次排程与数据集存活态的唯一权威是 [`unlit_towers_roadmap_20261030.md`](unlit_towers_roadmap_20261030.md)**（依据 `get_dead_datasets` / `get_dead_ends` 两张表）。
> 两文件冲突时**以 roadmap 为准**，并回来修本文件——2026-10-30 就因两处各写一套而误把 `institutions6` / `imbalance5` / `news79` 记成「未判死」。

## 0. 判据与边界

| 项 | 定义 |
|---|---|
| **未点亮塔** | 平台金字塔 alpha 计数 = 0。本日实测：`earnings 0/3`、`imbalance 0`、`insiders 0/3`、`institutions 0`、`macro 0`、`news 0`、`risk 0`、`sentiment 0`、`socialmedia 0` |
| **已点亮塔（不属本目标）** | `analyst 2`、`pv 2`、`other 1`、`fundamental 3`、`model 3`、`shortinterest 4` |
| **ATOM** | 单数据集（仅分组键 country/exchange/market/sector/industry/subindustry 可跨集）+ 单信号腿；`inst_pnl()`/`convert()` 记 pv1 |
| **用户约束 5** | PV / MODEL / OTHER **两两之间禁组腿**（PV+PV、PV+MODEL、MODEL+OTHER、OTHER+OTHER…）；它们与非 PV/MODEL/OTHER 类（如 NEWS）组腿**全库累计 ≤5 颗** |
| **10 年覆盖** | 覆盖率可动态调整，但必须有近十年数据；平台不暴露起始日 ⇒ 用**首波逐条 `get_alpha_yearly_stats` 反证**，某年 PnL 平坦且无持仓即判该年无数据 |
| **ATOM vs 组合** | 本目标优先 ATOM；跨类组腿只在单集挖尽且 prod 余量足够时做，且受 ≤5 约束 |

## 1. 总表（KOR 全部未点亮 category 的数据集；**存活态以 roadmap §1 为准**）

| category | 数据集 | 字段/类型 | cov | sumAC | 判定 | 机制一句话 |
|---|---|---|---|---|---|---|
| **INSIDERS** | `insiders5` | 53 V | .892 | 6422 | ⛔ **已判死**（`KOR-INSIDERS5-CEILING-20260909`，天花板 1.05；wave185 8 全灭 max\|S\|=0.81） | 内部人交易流量 = 私有信息显影 |
| | `insiders1` | 9 V | .353 | 529 | ✅ 唯一残值（cov<0.4 需 backfill） | 另一供应商口径 |
| **NEWS** | `news7` | 56（37V/19M） | .633 | 409 | ⭐ **主攻**（wave 188 在飞；机制 = 注意力计数，非语气） | 新闻注意力广度 |
| | `news18` | 29（20V/9M） | .571 | 989 | ✅ 待画像（注意：**事件情绪族**与已死族同源风险高） | 事件情绪/影响投影（rp_*） |
| | `news50` | 81 V | .625 | 104 | ⛔ **已判死**（`KOR-NEWS50-EVENTSCORE-WEAK`） | 事件分类/职位/话题 + 情绪 |
| | `news23` | 93 V | .329 | 48 | ✅ 事件研究型（cov 低需 backfill） | M&A/VC 交易规模与估值 |
| | `news38` | 45 V | .797 | 247 | ⛔ **已判死**（`KOR-NEWS38-HEADLINETONE-DEAD`） | 故事热力/相关度/词频 |
| | `news54` | 40 V | .691 | 24 | ⛔ **已判死**（`KOR-FORUM-DEAD`） | 财报电话会/公告时点 |
| | `news59` | 2 V | 1.0 | 3011 | ⚠ **仅门控**（极拥挤） | 事件财年/事件时间 |
| | `news76` | 6 V | .659 | 15 | 弱（情绪打分 ⇒ 撞已死族） | 情绪打分+版本号 |
| | `news17`/`news46` | 24/44 V | .269/.342 | 207/166 | ✅ 弱（覆盖低，需 backfill） | —— |
| **EARNINGS** | `earnings3` | 8 M | .660 | 2862 | ⚠ **wave186 FAIL**（max\|S\|=0.94 / F 0.49；2Y≫IS ⇒ 机制性衰减）；未封死但不再投主攻槽 | 财报事件时点（PEAD 窗口） |
| **RISK** | `risk88` | 64 M | .973 | 1589 | ⛔ **已判死**（`KOR-RSK88-STYLOAD-WEAK`，风格载荷） | 风险分解（波动/偏度/β） |
| | `risk70` | 96 M | .980 | 18720 | ⛔ 极拥挤 + 既往 KOR 失败 | 因子载荷/特异收益 |
| | `risk68` / `risk72` | 5 / 5 M | 1.0 / .602 | 193 / 39 | ✅ 残值探针级 | 待体检 |
| | `risk71` / `risk60` | 7 / 5 M | — | — | ⛔ `KOR-RISK71-RESIDUAL-REVERSAL-2Y-DEAD` / `KOR-RISK60-CROWDDING-NOSIGNAL` | —— |
| | `risk59` | 16 V | .981 | 629 | ⛔ **已判死**（`KOR-WAVE96-UNLIT-BARE-SIGNAL-DEAD` 明文含 risk59 裸信号） | 借券/空头指标 |
| **IMBALANCE** | `imbalance5` | 2 M | .856 | 850 | ⚠ **实测 2Y 结构性不可达**（3 形态 S 1.08–1.09 全 2Y≈0.17）；未封死，待 `seal_dead_end` | 油价冲击韧性评分（**注意：不是订单失衡**，名字骗人） |
| **MACRO** | `other106` | 15 V | .404 | 324 | ✅ 次选（cov<0.4 需 backfill） | 宏观暴露 |
| | `macro63` | 1 M | 1.0 | 158 | ⚠ **仅门控**（无截面差异） | 单一宏观序列 |
| **SENTIMENT** | `sentiment27` | 29 V | .399 | 1841 | ✅ 次选（10Y 风险高，先 1 条探针） | 网络关注/情绪 |
| | `sentiment26` | 19 V | — | 19 | 弱（aC<50） | —— |
| | `sentiment21` | 138 V | .966 | 687 | ⛔ **死集**（`get_dead_datasets`） | —— |
| **SOCIALMEDIA** | `socialmedia39` / `other100` | 各 1 V | 1.0 | 484/357 | ⚠ 探针级（10Y 风险最高） | 社媒关注/情绪 |
| **INSTITUTIONS** | `institutions6`（死集）/`fund_holdings_panel`（`KOR-FUND-HOLDINGS-PANEL-DEAD`） | — | — | — | ⛔ **本塔无可攻数据集** | 需新数据集授权才能开 |

**塔乘数（平台 `get_pyramid_multipliers`）**：news / sentiment 1.6 ＞ institutions / macro 1.4 ＞ risk 1.3 ＞ insiders 1.2 ＞ earnings 1.1 ＞ imbalance / socialmedia 1.0。
⇒ 排期按「乘数 × 可挖空间」：**NEWS 先开**（乘数最高 + 空间最大），SENTIMENT 接续；INSIDERS 因 wave185 全灭已退出主攻。
（2026-10-30 更正：初版写「INSIDERS 先开」是基于当时误认 insiders5 未判死。）

## 2. 逐 category 读法（画像 → 机制）

### 2.1 NEWS（空间最大，乘数 1.6）

| 子族 | 代表字段 | 性格 | 机制 | 骨架倾向 |
|---|---|---|---|---|
| 注意力/广度 | `headline_mention_count_2`、`news_mention_frequency_*`（cov .93） | MATRIX、稠密、右偏 | 注意力驱动（Barber-Odean 2008）：异常关注 ⇒ 短期买压后反转 | `ts_zscore`/`group_rank` + 多窗（5/22） |
| 语气/情绪 | `headline_overall_tone_score_2`、`nws7_2_d1_tone_score` | MATRIX、近似正态 | 情绪漂移（Tetlock 2007）：负面语气 ⇒ 下行压力后反转 | `ts_mean` 平滑 → `group_rank`，方向双测 |
| 事件情绪 | `rp_ess_*` / `rp_css_*` / `rp_nip_*`（news18，cov .5） | MATRIX，事件期非零 | 事件情绪的反应不足（PEAD 变体） | `trade_when(事件非零, rank, -1)` 或长窗聚合 |
| 故事热力 | `mws38_hotlevel`、`mws38_relevances`、`mws38_positive_score` | VECTOR，cov .89 | ⛔ **news38 已判死**（`KOR-NEWS38-HEADLINETONE-DEAD`）—— 保留此行为历史机制读法 | 勿用 |
| 分类情绪 | `mws50_ssc`、`mws50_ber`、`mws50_nip`、`mws50_qep` | VECTOR，cov .68，aC 低 | ⛔ **news50 已判死**（`KOR-NEWS50-EVENTSCORE-WEAK`） | 勿用 |
| M&A/VC | `nws23_target_*`、`investment_*` | VECTOR，cov .31 | 公告效应（交易规模/估值） | 事件窗 + 规模轴 |
| 日历 | `mws59_event_time_value`、`mws54_*_calendaryear` | VECTOR，cov 1.0 / .7 | **不是信号**，是时点门控；⚠ news54 集本身已判死（`KOR-FORUM-DEAD`），只剩 news59 可当门控 | `trade_when` 的时点轴 |

⚠ **news38 的 `*_entitlement` / `mws50_product_key` 是权限/产品标识**，不参与建模（描述明确写 "should not be used"）。
⚠ news59 aC ≈ 3000/字段 ⇒ 平台极度拥挤，做信号必然高 prod；只当门控。

### 2.2 INSIDERS（详见 `datasets/insiders5.md`）
交易流量族（cov .73）是唯一带方向的轴；存量持股（cov .9996）是结构轴；库藏股（cov .87）是资本回报代理。

### 2.3 EARNINGS（唯一数据集 earnings3，乘数 1.1）
8 个 MATRIX 字段、cov .66、sumAC 2862（**高拥挤**）。字段是财报事件的时间/属性（财年、财季、公告时刻）。
- 机制：PEAD（公告后漂移）+ 公告时点效应（盘前/盘后披露的信息含量不同）。
- 骨架：`trade_when(距公告 N 日, 方向, -1)`；方向侧可用同数据集的「属性」而非情绪 ⇒ 容易变成纯日历信号（无截面 alpha）。
- 判定：**能出 2–4 颗，但难出 6 颗**；不要把它当主塔。

### 2.4 RISK（空间被压到只剩 2 集，乘数 1.3）
- `risk88`：⛔ **已判死**（`KOR-RSK88-STYLOAD-WEAK` —— 收益来自 `ri_*` 风格载荷，不是 alpha）。
- `risk70`：aC 18720 ⇒ 全平台最拥挤之一，既往 KOR 已有失败证据 ⇒ 不开。
- `risk59` / `risk60` / `risk71`：⛔ 全部已判死（分别是裸信号 / 拥挤活动+费率 / 残差反转 2Y）。
- **残值 = `risk68`（5 字段、cov 1.0、αC 193）与 `risk72`（5 字段、cov .602、αC 39）**，探针级，各 ≤2 颗。

### 2.5 IMBALANCE / MACRO / SENTIMENT / SOCIALMEDIA
- `imbalance5`（2 字段）：⚠ **机制名字骗人 —— 不是订单失衡，是 SHIELD-OIL 油价冲击韧性评分**
  （`imb5_score` 0–1 有界复合分 + `imb5_mktcap`）。实测 rank / 规模中性 / `ts_delta(66)` 三形态 S 1.08–1.09
  但 **2Y 全部 ≈0.17** ⇒ 2Y 闸结构性不可达，且 αC 1109 极拥挤。**唯一资产**是 `imb5_mktcap` 同集
  ⇒ 可做 `vector_neut(score, rank(mktcap))` 的**真 ATOM 规模中性化**（这个技巧可迁移到别处）。
- `other106`（15 字段，cov .404）：宏观暴露；cov<0.4 ⇒ 必须 `ts_backfill`，且需验证 2013 起是否有值。
- `macro63`（1 字段，cov 1.0）：单一宏观序列，**无截面差异**，只能当门控/择时权重。
- `sentiment27`（cov .399，aC 1841）：网络关注类，**代际风险**（数据源起步晚），10 年覆盖大概率不满足 ⇒ 开波前先用 1 条探针验证 2013–2015 是否有 PnL。⚠ `sentiment21` 是**死集**，勿混。
- `socialmedia39`/`other100`：单字段、cov 1.0，10 年风险最高；只做探针，不排主路径。

## 3. 60 颗排期

**已迁出本文件** —— 波次排程、数据集存活态、每波结论唯一权威在
[`unlit_towers_roadmap_20261030.md`](unlit_towers_roadmap_20261030.md) §3。

初版在这里写死过一套「P1 INSIDERS 12 / P2 NEWS 20 / P3 RISK 10 …」的排期，**已于 2026-10-30 作废**：
它把已判死的 insiders5 / news50 / risk88 / risk70 / imbalance5 都当成了主攻，
按那张表排波等于按周烧配额去打已封存的机制。教训：**排期必须由 DB 两张表（`get_dead_datasets` / `get_dead_ends`）生成，
不能从画像印象手写**。

### 3.1 60 颗怎么凑（按 roadmap §1 的存活态推）

| 塔 | 乘数 | 乐观颗数 | 依据 |
|---|---:|---:|---|
| news | 1.6 | 20–24 | news7 注意力族 + news18/news46/news31/news21/news23 各 3–5，**唯一能撑起半壁的塔** |
| sentiment | 1.6 | 8–12 | sentiment27 / sentiment26，但需先过 10Y 探针 |
| macro | 1.4 | 4–6 | other106（cov .404，backfill 后可能只剩 2–3 颗）+ macro63 门控型 |
| risk | 1.3 | 4–6 | risk68 / risk72 各 5 字段，探针级 |
| insiders | 1.2 | 2–4 | insiders1 单集 9 字段 |
| socialmedia | 1.0 | 2–4 | socialmedia39 / other100 各 1 字段 |
| earnings | 1.1 | 0–2 | wave186 已 FAIL，存量机制挖尽 |
| imbalance | 1.0 | 0 | 2Y 结构性不可达 |
| institutions | 1.4 | **0** | 本塔无攻击面 |
| **合计** | | **40–58** | ⚠ **纯 ATOM 大概率到不了 60** |

⇒ 结论：**60 颗在纯 ATOM + 未点亮塔的约束下是高概率不可达的**。缺口只能靠
① 跨类组腿（PV/MODEL/OTHER × 非 PV/MODEL/OTHER，全库 ≤5 颗，用户约束 5）；
② 已点亮塔的增量（analyst/pv/other 仍可加，但不计未点亮塔目标）。
**这两条都是口径问题，需用户在缺口出现时拍板，不在本文件自行放宽。**

## 4. 覆盖率动态调整口径（要求 4）

1. **字段级**：cov<0.4 ⇒ 先 `ts_backfill(F, 22/66)`；仍 <0.4 ⇒ 换字段（`filter_sharpe=false` 拉全量后再选）。
2. **时间级**：首波收批后逐条看 yearly stats；某年 PnL 恒 0/无持仓 ⇒ 该年无数据。若缺失年份在近十年内 ⇒ **该数据集判不满足要求 4**（除非缺失仅为首年且其余 9 年完整）。
3. **横截面**：TOP600 内有效票数 <100 的因子不做（`LOW_SUB_UNIVERSE_SHARPE` 风险）。

## 5. 禁碰清单（本战役）

- 死数据集：`acquisition_model`、`fundamental44`、`institutions6`、`model109`、`model170`、`model192`、`model230`、`model30`、`model32`、`model53`、`multi_source_model`、`news79`、`sentiment21`、`shortinterest3`、`smoke_ds`、`wave30_model252`；战役级死：`other455`、`chart_cnn_alpha`、`predictive_starmine`、`ai_equity_alpha`、`pattern_scores`、`continuation_score`、`analyst_earnings_ibes`、`fund_holdings_panel`、`quant_factor_lib`、`model313`、`ai_factor_transfer`、`price_signal_dl`、`ml_factor_proj`、`behavioral_signals`、`news_sentiment_transfer`
- entitlement/内部字段：`*_entitlement`、`*_product_key`
- 用户约束 5：PV / MODEL / OTHER 两两组腿；与非 PV/MODEL/OTHER 类组合累计 >5
- 混信号：`add`/`multiply` 两条独立信号腿（`POISON:equal_weight_leg_add`，秩化不豁免）
