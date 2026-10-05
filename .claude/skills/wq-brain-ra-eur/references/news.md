# EUR × news（组合分支）

> 回到 [EUR 区域流程](../SKILL.md) · [EUR profile（证据与历史）](../../wq-brain-ra-pipeline/references/regions/EUR.md) · 实时生效画像：`$WQ_PY -m wqb.profiles explain --region EUR --category news`

<!-- profiles:cell-panel:start -->
**状态**：probe（跟区域入场 probe-only）　**分组**：News-Sentiment　**类别卡**：news

**涉及数据集**：news17、news20、news21、news29、news31、news36、news38、news46、news48、news50、news54、news73、news84、news85、predictive_starmine × news73、{'dataset': 'news54', 'max_sharpe': 0.4, 'reason': 'mws54_factor semi-annual+单边恒正+稀疏', 'tower': 'news'}

### 回测设置（进仿真的值）

| 设置 | 值 | 来源 |
|---|---|---|
| instrumentType | EQUITY | 区域 settings.json |
| region | EUR | 区域 settings.json |
| universe | TOPCS1600 | 区域 settings.json |
| delay | 1 | 区域 settings.json |
| neutralization | SUBINDUSTRY | 区域 settings.json |
| decay | 4 | 区域 settings.json |
| truncation | 0.08 | 区域 settings.json |
| maxTrade | ON | 区域 settings.json |
| pasteurization | ON | 区域 settings.json |
| unitHandling | VERIFY | 区域 settings.json |
| nanHandling | ON | 区域 settings.json |
| language | FASTEXPR | 区域 settings.json |
| visualization | false | 区域 settings.json |
| startDate | 2014-01-01 | 区域 settings.json |
| endDate | 2023-12-31 | 区域 settings.json |

### 阈值

- Mode B 主闸 sharpe / fitness：1.25 / 0.8（default；下限锁生效，实时值看 explain）
- 其余阈值跟区域 thresholds.json（本组合无覆盖）

### 证据（2026-10-04 只读汇总）

| 回测 | RA 全过 | prod 已测 | 其中低于上限 | 判死 | 胜绩 |
|---|---|---|---|---|---|
| 46 | 0 | 0 | 0 | 16 | 0 |

主要数据集（回测数）：news46（15）、news21（8）、news50（8）、news54（7）、news73（4）、news29（4）

### S1 字段理解

- VECTOR 稀疏：vec_count / vec_avg 后再进常规算子；直接用易 CONCENTRATED_WEIGHT
- 深挖（5 家族 × 6 桶）走 brain-alpha-research-news-sentiment
- 窗口（类别卡，均在白名单内）：event 1/5/22

### S2 生成

- **类别通用原语**（类别卡，跨区）：
  - disagreement: primary vs secondary / source A vs source B sentiment
  - intensity-weighted tone: sentiment scaled by item count or novelty
  - revision of tone: ts_delta of backfilled sentiment, not the level
  - skew / polarization: fat-tail of sentiment vs the mean
  - event clustering: news count spikes vs baseline (ts_zscore of count)
  - source credibility: tier-1 vs tier-2 source sentiment divergence
- **跨区结论**（USA/EUR/IND/KOR/AMR/GLB；negative）：新闻 / 情绪作主信号在多区同型全灭（robust 墙、CW 或换手墙）（证据：AMR profile 跨区负先验；KOR 新闻情绪四连死（news38/50/54/79）；IND sentiment21 robust 0.24；GLB-NEWS23-MNA-EVENT-DEAD、GLB news73 sentiment 判死） <!-- lint:const-ok 证据原文 -->
- **跨区结论**（ASI/GLB；lever）：新闻计数作子集门控腿有效（主信号仍来自别的类别）（证据：ASI normalized_news_article_count、GLB vec_count(nws73_headlines)（2026-09-21 门控模板）） <!-- lint:const-ok 证据原文 -->
- **跨区结论**（GLB/KOR/HKG/AMR；negative）：emotion 系（含 sentiment / mood 命名的变体）跨区死路（证据：GLB 铁律（registry cross_region 层）；KOR / HKG / AMR profile 排除） <!-- lint:const-ok 证据原文 -->
- **禁止**（类别卡）：禁止使用 ts_entropy / ts_skewness / ts_percentage / ts_decay_exp_window（幽灵算子，整批 CANCELLED 连坐）
- **禁止**（类别卡）：禁止使用裸 rank(sentiment_score)（必须 group_neutralize 或 ts_delta）
- **禁止**（全局锁定）：禁止两条独立信号腿相加：加权（0.4×A + 0.6×B）、等权 add(rank(A), rank(B))、中缀 + 都算；第二个数据集只以条件（trade_when / if_else）、分组（group_rank / bucket）或残差（regression_neut / vector_neut）入场
- **禁止**（全局锁定）：禁止 ts_event_* 系列（平台没有）与幽灵算子；字段名逐一经 get_datafields 验证

### S4 改进（按顺序试：组合 → 类别卡 → 全局）

1. [全局] 判「无解 / 天花板」前先扫等价算子替换：signed_power → quantile、ts_scale → quantile / normalize。数值路径不同，一次动多个闸（含 prod，要读全部闸）（KOR/GLB 复现：KOR other466 signed_power→quantile：2Y 1.51→1.56、prod 0.6544→0.6397；GLB quantile 替 ts_scale：S +0.20、F +0.06、prod 0.475→0.565（DEC-72）） <!-- lint:const-ok 证据原文 -->
   - 注意：效应量逐区实测，禁外推；quantile 只收 1 个参数
2. [全局] 强但撞 prod 墙的快信号：用一个经济子集门控（trade_when 进 >0.5 出 <0.4 的慢变量，或 rank(cap)>0.2 ∩ 子集）只在子集里持仓（GLB/ASI/IND 复现：GLB-DL20D-SUBSET-GATE-FAMILY-20260921（prod 0.82→0.60–0.67）；ASI LLNgdpw2 / 88jaV5lv；IND ZYbqREW1 / levk5JYN（prod 0.54–0.55）） <!-- lint:const-ok 证据原文 -->
   - 前提：未门控的基础信号 IS sharpe 不低于 2.5、fitness 不低于 1.5（GLB 2026-09-27 铁律：门控只修 prod / robust，不造强度）；慢信号门控后换手会升，只用于快信号
- 提醒：prod 与 self 两个端点都取 max、都过线才可提；不改持仓的降 prod 杠杆（hump、加大 decay）会把 self 推爆（EUR wave274） <!-- lint:const-ok 证据原文 -->
- 提醒：设置是强度闸：nanHandling / maxTrade / decay / 中性化换档等于换信号，跨档结果不可比（IND 行为族 S 2.19→0.46） <!-- lint:const-ok 证据原文 -->
- 提醒：decay 匹配信号速度：快信号上 decay 越大越差；decay 0 与 1 逐位相同，只留一个 <!-- lint:const-ok 证据原文 -->
- 提醒：prod 墙先看直方图分单颗钉子 / 密墙 / 可破三型，再决定换分母、换设置档或分组轴（决策表 D0-P 诊断前置） <!-- lint:const-ok 证据原文 -->

### S5 提交前

- 资格判定：`$WQ_PY tools/mode_b_qualify.py evaluate --region EUR --sharpe <S> --fitness <F> --two-year-sharpe <2Y>`（喂全指标，旁路 A–E 才会生效）
- 提交链：`submit_verdict` 只否决；prod 与 self 双端点实测（`check_correlation(refresh=True)`）；用户明确确认后才 `workflow_submit_alpha(confirm_submit=True)`——见 `worldquant-submit-alpha`

### 判死记录（不要重试；「归属」= payload 绑定 / 由条目名推断 / 关键词推断）

| 条目 | 族 | 下次怎么办 / 说明 | 数据集 | 归属 |
|---|---|---|---|---|
| EUR-NEWS17-INSPECT-GATE-WALL | news17 comp_d1 分数族 | news17 体检硬门系统性拦截（单边恒正 monthly/quarterly 分数 raw 水平+短窗错配+稀疏未 trade_when），GEM 池两轮收敛后仍违规，零配额判死。根因=GEM 生成侧未消费字段画像。NEWS 塔在 pre | news17 | inferred | <!-- lint:const-ok 证据原文 -->
| EUR-NEWS20-INSPECT-GATE-WALL | news20 multiple_comp 事件分族 | news20 体检硬门系统性拦截（单边恒正 monthly/quarterly 分数 raw 水平+短窗错配+稀疏未 trade_when），GEM 池两轮收敛后仍违规，零配额判死。根因=GEM 生成侧未消费字段画像。NEWS 塔在 pre | news20 | inferred | <!-- lint:const-ok 证据原文 -->
| EUR-NEWS21-EVENT-CALENDAR-DEAD | news21 event calendar / transcript tone (post-call drift, pr | EUR news tower: event-calendar family closed | news21 | payload | <!-- lint:const-ok 证据原文 -->
| EUR-NEWS29-WEAK | news29 主题显著性族（nws29_topic/significance VECTOR） | wave244 4 探针全灭 best ／sharpe／=0.25（另 4 条 group_rank 单位错误被隔离）→ fast_kill 判死。NEWS 族五集全灭。 | news29 | inferred | <!-- lint:const-ok 证据原文 -->
| EUR-NEWS31-INSPECT-GATE-WALL | news31 事件/相似度分族 | news31 体检硬门系统性拦截（单边恒正 monthly/quarterly 分数 raw 水平+短窗错配+稀疏未 trade_when），GEM 池两轮收敛后仍违规，零配额判死。根因=GEM 生成侧未消费字段画像。NEWS 塔在 pre | news31 | inferred | <!-- lint:const-ok 证据原文 -->
| EUR-NEWS36-NOVELTY-SENT-WEAK | news36 novelty/phrase/word/confidence concepts | Leave news36 standalone novelty/sentiment densify. NEWS whitelist concept track exhausted (news38/36/84/85). Skip news54 | news36 | payload | <!-- lint:const-ok 证据原文 -->
| EUR-NEWS38-CONCEPT-WEAK | news38 densified tone/polarity/relevance concepts | Leave news38 standalone densify concepts. Do not mix v_rev/wedge. Skip news54 timestamps/headline-text. Next NEWS=news36 | news38 | payload | <!-- lint:const-ok 证据原文 -->
| EUR-NEWS46-ZERO-IS-SIGNAL | mws46_* ravenpack news sentiment/impact MATRIX | 两轮实测均无 IS 信号：wave245 基础探针(单字段 rank/ts_delta/rank差) best／S／=0.46 n=5；wave257 复合结构第二轮(group_rank 新中性化几何 + trade_when 事件门控跨 | news46 | inferred | <!-- lint:const-ok 证据原文 -->
| EUR-NEWS48-INSPECT-GATE-WALL | news48 ENS 情绪分族 | news48 体检硬门系统性拦截（单边恒正 monthly/quarterly 分数 raw 水平+短窗错配+稀疏未 trade_when），GEM 池两轮收敛后仍违规，零配额判死。根因=GEM 生成侧未消费字段画像。NEWS 塔在 pre | news48 | inferred | <!-- lint:const-ok 证据原文 -->
| EUR-NEWS84-SENTIMENT-MATRIX-WEAK | news84 migration sentiment MATRIX probe | Leave news84/news85. Do not occupy another slot with EUR news sentiment MATRIX probes. | news84 | payload | <!-- lint:const-ok 证据原文 -->
| EUR-NEWS85-SENTIMENT-MATRIX-WEAK | news85 DNN sentiment MATRIX probe | Leave news85. Do not second-round probe. | news85 | payload | <!-- lint:const-ok 证据原文 -->
| EUR-NONMODEL-TOWER-CEILING | non_model_tower_sparse_event_sentiment_analyst |  | {'dataset': 'news54', 'max_sharpe': 0.4, 'reason': 'mws54_factor semi-annual+单边恒正+稀疏', 'tower': 'news'} | payload | <!-- lint:const-ok 证据原文 -->
| EUR-W245-news46-mechanisms-D1 | news46_cashless_news_mechanism_probe | EUR TOPCS1600 D1 本轮5条概念原式 max S=0.42, max ／S／=0.46; 无 S>=1.25 且 F>=0.8，停止本轮机制增强。仅封存所测机制，不宣称全数据集无效。 | news46 | inferred | <!-- lint:const-ok 证据原文 -->
| EUR-W246-news50-mechanisms-D1 | news50_cashless_news_mechanism_probe | EUR TOPCS1600 D1 本轮8条概念原式 max S=0.32, max ／S／=0.52; 无 S>=1.25 且 F>=0.8，停止本轮机制增强。仅封存所测机制，不宣称全数据集无效。 | news50 | inferred | <!-- lint:const-ok 证据原文 -->
| EUR-news54-TIMESTAMP-INVALID | news54 event timestamp fields | Leave news54 timestamp fields in EUR. Do not use ts_mean/ts_delta on UNIX timestamp fields; convert to days_from_last_ch | news54 | payload | <!-- lint:const-ok 证据原文 -->
| EUR-predictive_starmine-NEWS-MIX-WEAK | predictive_starmine × news73 sentiment mix | Do not mix predictive_starmine surprise with news73 sentiment fields in EUR TOP2500 — weak signal combination | predictive_starmine × news73 | payload | <!-- lint:const-ok 证据原文 -->
<!-- profiles:cell-panel:end -->

## 补充说明（手写）

<!-- profiles:manual:start -->
<!-- profiles:manual:end -->
