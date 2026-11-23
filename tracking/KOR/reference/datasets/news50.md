# news50 字段画像（KOR / TOP600 / Delay=1）— RavenPack 事件情绪与新颖度

> 2026-11-21 建。平台 `get_datafields(news50, filter_sharpe=false, sort_by=dateCreated)` 实读 **complete=true / 81/81**（pages_fetched=2）。
> 塔：**NEWS（0/3 未点亮）**，倍率 1.6，category = NEWS（非 OTHER ⇒ 在挖掘范围内）。
> **本集此前从未回测、无画像档案**（与已封口的 news85 / news54 / news76 / news38 均非同一集）。

## 0. 元信息

| 项 | 值 |
|---|---|
| dataset id | `news50` |
| 语义 | RavenPack 事件级情绪（多分类器分数）+ 事件新颖度（ENS）+ 事件量/正事件比 + 相关性 |
| 结构 | **81 字段全部 VECTOR** ⇒ 必须先 `vec_avg` / `vec_sum` 降维 |
| coverage | **.3484–.7855**（三档：.3484 新颖度族 / .5389–.6812 主体 / .7855 属性族） |
| dateCreated | 2023-01-01（主体 44 字段）/ 2025-11-01（d0·twn 多切点变体 44 字段） |
| 拥挤度 | 头部 `mws50_evaluation_method` aC **17**、`mws50_ber` **15**、`mws50_category` 12、`mws50_ssc` 10；多数 0–5 |

## 0.1 字段全表与实测读数（全 81 字段，平台实读 cov / aC）

| field | cov | aC | 族 | 裁决 |
|---|---|---|---|---|
| `analyst_recommendation_change_score_d0` | .6528 | 0 | F1 情绪(分析) | ✅ d0 变体 |
| `analyst_recommendation_change_score_twn` | .6528 | 1 | F1 情绪(分析) | ⚠ twn 与 d0 同源，只取一 |
| `composite_story_sentiment_score_d0` | .6528 | 0 | F1 情绪(综合) | ✅ |
| `composite_story_sentiment_score_twn` | .6528 | 0 | F1 情绪(综合) | ⚠ 同源 |
| `corporate_action_report_sentiment_score_d0` | .6528 | 0 | F1 情绪(公司行动) | ✅ |
| `corporate_action_report_sentiment_score_twn` | .6528 | 1 | F1 情绪(公司行动) | ⚠ 同源 |
| `earnings_evaluation_sentiment_score_d0` | .6528 | 1 | F1 情绪(财报评估) | ✅ |
| `earnings_evaluation_sentiment_score_twn` | .6528 | 0 | F1 情绪(财报评估) | ⚠ 同源 |
| `earnings_release_sentiment_score_d0` | .6528 | 0 | F1 情绪(财报发布) | ✅ |
| `earnings_release_sentiment_score_twn` | .6528 | 0 | F1 情绪(财报发布) | ⚠ 同源 |
| `editorial_commentary_sentiment_score_d0` | .6528 | 0 | F1 情绪(评论) | ✅ |
| `editorial_commentary_sentiment_score_twn` | .6528 | 0 | F1 情绪(评论) | ⚠ 同源 |
| `entity_record_count_per_story_d0` | .6528 | 0 | F4 事件量 | ⚠ 只作门控 |
| `entity_record_count_per_story_twn` | .6528 | 0 | F4 事件量 | ⚠ 只作门控 |
| `entity_relevance_score_d0` | .6528 | 1 | F5 相关性 | ⚠ 只作门控/权重 |
| `entity_relevance_score_twn` | .6528 | 0 | F5 相关性 | ⚠ 只作门控/权重 |
| `event_novelty_score_d0` | .6528 | 0 | F3 新颖度 | ✅ 0–100，24h 窗 |
| `event_novelty_score_twn` | .6528 | 0 | F3 新颖度 | ⚠ 同源 |
| `event_sentiment_score_d0` | .6528 | 1 | F1 情绪(事件) | ✅ 0–100 |
| `event_sentiment_score_twn` | .6528 | 0 | F1 情绪(事件) | ⚠ 同源 |
| `global_equities_sentiment_score_d0` | .6528 | 1 | F1 情绪(全球股) | ✅ |
| `global_equities_sentiment_score_twn` | .6528 | 0 | F1 情绪(全球股) | ⚠ 同源 |
| `global_event_novelty_score_d0` | .6528 | 0 | F3 新颖度 | ✅ |
| `global_event_novelty_score_twn` | .6528 | 0 | F3 新颖度 | ⚠ 同源 |
| `global_novelty_elapsed_milliseconds_d0` | .6528 | 0 | F3 新颖度 | ⚠ 毫秒时长，量纲改用比值 |
| `global_novelty_elapsed_milliseconds_twn` | .6528 | 0 | F3 新颖度 | ⚠ 同上 |
| `global_novelty_similarity_gap_days_d0` | .6528 | 1 | F3 新颖度 | ✅ 距上次相似故事天数 |
| `global_novelty_similarity_gap_days_twn` | .6528 | 0 | F3 新颖度 | ⚠ 同源 |
| `merger_acquisition_sentiment_score_d0` | .6528 | 0 | F1 情绪(并购) | ✅ |
| `merger_acquisition_sentiment_score_twn` | .6528 | 0 | F1 情绪(并购) | ⚠ 同源 |
| `multi_classifier_equity_sentiment_score_d0` | .6528 | 0 | F1 情绪(多分类器) | ✅ |
| `multi_classifier_equity_sentiment_score_twn` | .6528 | 0 | F1 情绪(多分类器) | ⚠ 同源 |
| `news_story_classification_2` | .6528 | 0 | F9 元数据 | ✗ 故事分类码 |
| `news_story_classification_d0` | .6528 | 0 | F9 元数据 | ✗ 故事分类码 |
| `news_volatility_projection_score_d0` | .6528 | 0 | F6 冲击预测 | ✅ 预期市场冲击 |
| `news_volatility_projection_score_twn` | .6528 | 0 | F6 冲击预测 | ⚠ 同源 |
| `non_neutral_event_count_rolling_window_d0` | .6528 | 0 | F4 事件量 | ⚠ 只作门控 |
| `non_neutral_event_count_rolling_window_twn` | .6528 | 0 | F4 事件量 | ⚠ 只作门控 |
| `novelty_elapsed_milliseconds_d0` | .6528 | 0 | F3 新颖度 | ⚠ 量纲 |
| `novelty_elapsed_milliseconds_twn` | .6528 | 1 | F3 新颖度 | ⚠ 量纲 |
| `novelty_similarity_gap_days_d0` | .6528 | 0 | F3 新颖度 | ✅ 0–1 相似度 |
| `novelty_similarity_gap_days_twn` | .6528 | 1 | F3 新颖度 | ⚠ 同源 |
| `positive_event_ratio_score_d0` | .6528 | 0 | F2 正事件比 | ✅ 91 日滚动 |
| `positive_event_ratio_score_twn` | .6528 | 0 | F2 正事件比 | ⚠ 同源 |
| `mws50_acb` | .6812 | 2 | F1 情绪(公司行动分类器) | ✅ |
| `mws50_aes` | .6812 | 5 | F2 正事件比 | ✅ 91 日正事件比 |
| `mws50_bam` | .6812 | 1 | F1 情绪(并购分类器) | ✅ |
| `mws50_bee` | .6812 | 0 | F1 情绪(财报评估) | ✅ |
| `mws50_ber` | .6812 | 15 | F1 情绪(财报发布) | ⭐ 本集最高 aC 情绪字段 |
| `mws50_category` | .5389 | 12 | F9 元数据 | ✗ 事件类目标签 |
| `mws50_country_code` | .6812 | 1 | F9 元数据 | ✗ 国家码 |
| `mws50_ens` | .3484 | 2 | F3 新颖度 | ⚠ cov 低于 0.5 地板 |
| `mws50_ens_elapsed` | .3484 | 0 | F3 新颖度 | ⚠ cov 低于 0.5 地板 |
| `mws50_ens_key` | .5389 | 0 | F9 元数据 | ✗ 链键 |
| `mws50_ens_similarity_gap` | .3626 | 9 | F3 新颖度 | ⚠ cov 低于 0.5 地板 |
| `mws50_ess` | .3484 | 2 | F1 情绪(细分) | ⚠ cov 低于 0.5 地板 |
| `mws50_evaluation_method` | .7855 | 17 | F9 元数据 | ✗ 评估期属性 |
| `mws50_g_ens` | .3484 | 1 | F3 新颖度 | ⚠ cov 低于 0.5 地板 |
| `mws50_g_ens_elapsed` | .3484 | 4 | F3 新颖度 | ⚠ cov 低于 0.5 地板 |
| `mws50_g_ens_key` | .5389 | 0 | F9 元数据 | ✗ 链键 |
| `mws50_g_ens_similarity_gap` | .3626 | 2 | F3 新颖度 | ⚠ cov 低于 0.5 地板 |
| `mws50_ghc_lna` | .6812 | 1 | F1 情绪(分析) | ✅ |
| `mws50_group` | .5389 | 0 | F9 元数据 | ✗ 事件分组 |
| `mws50_maturity` | .7855 | 2 | F9 元数据 | ✗ 债券期限属性 |
| `mws50_news_type` | .6812 | 2 | F9 元数据 | ✗ 新闻类型码 |
| `mws50_nip` | .6812 | 5 | F6 冲击预测 | ✅ 2 小时冲击预测 0–100 |
| `mws50_position_name` | .7855 | 6 | F9 元数据 | ✗ 人物职位 |
| `mws50_product_key` | .5389 | 8 | F9 元数据 | ✗ 订阅包键 |
| `mws50_property` | .5389 | 0 | F9 元数据 | ✗ 事件属性串 |
| `mws50_qcm` | .6812 | 1 | F1 情绪(多分类器) | ✅ |
| `mws50_qep` | .6812 | 4 | F1 情绪(全球股 PEQ) | ✅ |
| `mws50_qmb` | .6812 | 0 | F1 情绪(评论分类器) | ✅ |
| `mws50_relevance` | .6812 | 1 | F5 相关性 | ⚠ 只作门控/权重 |
| `mws50_rp_story_event_count` | .6812 | 1 | F4 事件量 | ⚠ 只作门控 |
| `mws50_rp_story_event_index` | .6812 | 0 | F9 元数据 | ✗ 序数位 |
| `mws50_ssc` | .6812 | 10 | F1 情绪(综合) | ⭐ 主体综合情绪分 0–100 |
| `mws50_sub_type` | .5389 | 1 | F9 元数据 | ✗ 事件子类 |
| `mws50_time` | .6812 | 1 | F9 元数据 | ✗ 时刻码 |
| `mws50_topic` | .5389 | 3 | F9 元数据 | ✗ 主题标签 |
| `mws50_type` | .5389 | 1 | F9 元数据 | ✗ 事件类 |
| `mws50_vea` | .6812 | 2 | F4 事件量 | ⚠ 只作门控（91 日事件量） |

## 1. 字段族与角色白名单

| 族 | 可用字段 | 允许形态 | 禁作 |
|---|---|---|---|
| **F1 情绪水平** | `mws50_ssc`(aC10) / `mws50_ber`(aC15) / `mws50_qep` / `mws50_qcm` / 各 `*_sentiment_score_d0` | `vec_avg` → `ts_mean(22)` → `group_rank` | 裸情绪直排；d0 与 twn 同时进一条腿（同源） |
| **F2 正事件比** | `mws50_aes` / `positive_event_ratio_score_d0` | 91 日滚动比，慢变量，可直接 `group_rank` | 当作短期信号 |
| **F3 新颖度** | `event_novelty_score_d0` / `global_event_novelty_score_d0` / `global_novelty_similarity_gap_days_d0` / `novelty_similarity_gap_days_d0` | 新颖度高 ⇒ 信息未被消化 | cov .3484 的 `mws50_ens*` 系列（低于地板） |
| **F4 事件量** | `non_neutral_event_count_rolling_window_d0` / `mws50_vea` / `entity_record_count_per_story_d0` | **门控**（`trade_when`） | 裸计数当信号 |
| **F5 相关性** | `entity_relevance_score_d0` / `mws50_relevance` | 只作权重/门控 | 作主信号 |
| **F6 冲击预测** | `mws50_nip` / `news_volatility_projection_score_d0` | 0–100 预测，可作主信号 | 与情绪同腿相加（不同机制混腿） |
| **F9 元数据** | `mws50_category/group/type/sub_type/topic/property/product_key/country_code/news_type/time/position_name/maturity/evaluation_method/ens_key/g_ens_key/rp_story_event_index`、`news_story_classification*` | 禁用 | 一切信号用途 |

**d0 / twn 双切点**：两者是同一条新闻记录的两种切点口径（description 明写 multicutoff variant）⇒ **同源，只取其一**，不得相加。

## 2. 机制与证据

| 机制 | 定义 | 方向 | 证据 |
|---|---|---|---|
| **M1 事件情绪水平** | 事件级情绪分被渐进吸收 | 正向 | paper_search `news sentiment cross-section stock returns`：5 篇 / 4 作者，diverse_ok |
| **M2 新颖度溢价** | 新颖事件信息未消化 ⇒ 后续漂移大；陈旧（echo）事件已定价 | 正向（新颖度高 ⇒ 后续强） | RavenPack ENS 语义 + 论坛 42659817284375「新颖度过滤」 |
| **M3 冲击预测门控** | NIP 高 ⇒ 短期波动放大，情绪信号被噪声淹没 | 门控 | 论坛 37140180319127「注意力×情绪解耦」 |

## 3. 预处理与设置

- **全 VECTOR ⇒ 必须 `vec_avg` 降维**，禁裸字段。
- cov .6812（主体）/.6528（d0·twn）/.5389–.7855（属性）/**.3484（新颖度族，低于 0.5 地板 ⇒ 排除）**。
- 日频事件型 ⇒ `ts_mean(x, 22)` 聚合后 `group_rank`；**禁 hump**（news_sentiment_transfer 实测压书到 42 只、CW 1.0）。
- 标准档 **SUBINDUSTRY**，decay 4，truncation 0.08，nanHandling OFF。
- 十年覆盖：2003 批字段 dateCreated 2023-01-01 ⇒ 首波后必须 `get_alpha_yearly_stats` 核 2014–2023。

## 4. 波次记录（wave 208 起）

| wave | 腿 | 机制 | 表达式 | alpha | S | 2Y | F | TO | 结论 |
|---|---|---|---|---|---|---|---|---|---|
| 208 | A | M1 情绪水平 | `group_rank(ts_mean(vec_avg(mws50_ssc), 22), sector)` | mLaKJWKx | **−0.06** | −0.56 | −0.01 | .1506 | 无信号 |
| 208 | B | M1' 财报情绪（aC15） | `group_rank(ts_mean(vec_avg(mws50_ber), 22), sector)` | rK70EM0d | **0.17** | −0.12 | 0.04 | .1461 | 近零信号 |

**wave 208 判定（2026-11-21）**：首轮 2 腿全灭。
- 两条臂的 TO（.15/.146）都在 KOR 配方带内、书规模正常、CW 未报错 ⇒ **不是包装问题**；
- 本集**最高 aC 的财报情绪字段**（`mws50_ber`，aC 15）S 仅 **0.17**，综合情绪（aC 10）S **−0.06** ⇒ 与 news85（天花板 .69）/news38（−0.36 / 0.00）/news_sentiment_transfer（0.41）同形：**KOR news 家族的情绪水平轴无定价力**；
- 记 **PROVISIONAL 信号层封顶**（不判集死）。复活条件：换到**新颖度（F3）/冲击预测（F6）**轴并先验十年覆盖（本集 2025-11 批字段的起点未知）。

## 5 「≥5 结构互异族 + 每族完整梯度」补齐复核（2026-11-22）
> 用户要求按严格标准补齐梯度。本节执行档案 §4 点名的复活方向（F3 新颖度 / F6 冲击预测）。论文闸档案 §2 已 PASS。KOR/TOP600/D1/SUBINDUSTRY/decay4/trunc0.08。

### 5.1 L1 外层全类别替换（逐族推进）
| 族 | wave | 最优 | S | 2Y | 判 |
|---|---|---|---:|---:|---|
| F3 新颖度（复活方向） | `s2_news50_T1_novelty_L1_d1` | `O0WjZxap` `trade_when(relevance>50,ens)` | 0.48 | 0.60 | 相关度门控×新颖度是本集最强；裸新颖度 S≤0.16；decay 臂 S0.71 但 TO1.10/CW1.0 超闸 |
| F6 冲击 + F2 正事件比 + F1 情绪长窗 | `s2_news50_T2_nip_ratio_L1_d1` | `QP0A9mkM` `mws50_aes` | 0.38 | 0.22 | NIP 双向≤0.35、正事件比 S0.38/2Y0.22、情绪 ssc44 −0.16；全灭 |

### 5.2 L2 内层时序全类别替换（在最强 F3 门控族推进）
| 族 | wave | 内层替换最优 | S | 判 |
|---|---|---|---:|---|
| F3 新颖度门控 | `s2_news50_T1_novelty_L2_d1` | `d5a6Zxdj` `relevance>60` | 0.39 | 内层换窗/门控阈值全劣化，L1 的 22 窗+rel>50 S0.48 仍最优；2Y 主墙（5/8）；F3 族收敛 |

### 5.3 收口判定（2026-11-22）
**news50 按严格标准补齐梯度：F3 新颖度（档案复活方向）、F6 冲击 NIP + F2 正事件比 + F1 情绪长窗 × L1+L2 = 3 wave / 24 臂，全部入库。**
- **族数诚实标注**：合法信号族为 F3 新颖度（event/global novelty、相似度间隙）、F6 冲击（NIP）、F2 正事件比（aes）、F1 情绪水平（ssc/ber/qep）；F4 事件量/F5 相关性只作门控、F9 元数据禁作信号 ⇒ 主体是情绪+新颖度两大家族，d0/twn 同源只取其一，**受字段落地性限制凑不满独立 5 族**，不硬凑。
- **0 全闸、无 near**：全集天花板 F3 门控 `O0WjZxap` S0.48/F0.28/2Y0.60/CW过（relevance>50×新颖度22窗），比 wave208 情绪两腿（−0.06/0.17）改善但仍距闸远；L2 全灭确认天花板。
- **档案复活方向失败**：§4 点名"换新颖度 F3/冲击 F6"——本轮两轴全测仍全灭（NIP 双向≤0.35、新颖度裸≤0.16、门控 S0.48），PROVISIONAL 信号层封顶得到确认。
- **不判死**：记「梯度证据完整、信号层弱」；翻案须外部新信息源。论文闸 PASS（档案 §2 news sentiment cross-section 5篇/4作者）。全程前台 MCP、无后台任务、未提交任何 alpha。
