# GBR × news（组合分支）

> 回到 [GBR 区域流程](../SKILL.md) · [GBR profile（证据与历史）](../../wq-brain-ra-pipeline/references/regions/GBR.md) · 实时生效画像：`$WQ_PY -m wqb.profiles explain --region GBR --category news`

<!-- profiles:cell-panel:start -->
**状态**：active（跟区域入场 active）　**分组**：News-Sentiment　**类别卡**：news

**涉及数据集**：news104、news17、news18、news20

### 回测设置（进仿真的值）

| 设置 | 值 | 来源 |
|---|---|---|
| instrumentType | EQUITY | 区域 settings.json |
| region | GBR | 区域 settings.json |
| universe | TOP700 | 区域 settings.json |
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
| 56 | 0 | 0 | 0 | 5 | 0 |

主要数据集（回测数）：news104（43）、news18（13）

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

- 资格判定：`$WQ_PY tools/mode_b_qualify.py evaluate --region GBR --sharpe <S> --fitness <F> --two-year-sharpe <2Y>`（喂全指标，旁路 A–E 才会生效）
- 提交链：`submit_verdict` 只否决；prod 与 self 双端点实测（`check_correlation(refresh=True)`）；用户明确确认后才 `workflow_submit_alpha(confirm_submit=True)`——见 `worldquant-submit-alpha`

### 判死记录（不要重试；「归属」= payload 绑定 / 由条目名推断 / 关键词推断）

| 条目 | 族 | 下次怎么办 / 说明 | 数据集 | 归属 |
|---|---|---|---|---|
| GBR-NEWS17-DEAD | news17 | 不生成 news17 表达式 | news17 | inferred | <!-- lint:const-ok 证据原文 -->
| GBR-NEWS18-EVENTGATE-DEAD | news18_event_gated | news18 不再生成任何结构（常规 quantile/ts_corr/group + 事件门控 trade_when 均判死）；GBR news 塔无可用信号 | news18 | payload | <!-- lint:const-ok 证据原文 -->
| GBR-NEWS18-STRUCTURAL-WEAK | news18 | news18 仅剩事件门控类结构（trade_when + ts_arg_max 事件爆发时间）未验证；常规 quantile/ts_corr/group 结构不再生成（软判死） | news18 | inferred | <!-- lint:const-ok 证据原文 -->
| GBR-NEWS20-DEAD | news20 | 不生成 news20 表达式 | news20 | inferred | <!-- lint:const-ok 证据原文 -->
| NEWS104-IMPACT-CEILING | news104 marketimpactscore 冲击动量域 | same-family-ceiling | news104 | inferred | <!-- lint:const-ok 证据原文 -->
<!-- profiles:cell-panel:end -->

## 补充说明（手写）

<!-- profiles:manual:start -->
### 2026-10-28 · news50 首次开波（NEWS 塔 0/3 未点亮）

**选集依据**：`news50` 是 S0 排名（177 集）里**唯一**既通过硬闸（cov 0.691 ≥ 0.3、37 字段 ≥ 5）又属未点亮塔的集。news 域其余集（17/18/20/38/48/104）全部已判死。

**跨区死路交叉验证（不构成 GBR 封禁）**：

- `EUR-W246-news50-mechanisms-D1`（EUR TOPCS1600，8 条概念原式 max S 0.32）——原文明写「仅封存所测机制，**不宣称全数据集无效**」，且 EUR 是 TOPCS1600 口径；
- `DEU-NEWS18-ALLDEAD` 的 rule 覆盖 news50（德国新闻情绪不成立）；
- `KOR-NEWS50-EVENTSCORE-WEAK`（KOR 12 结构 max S 0.54）——rule 原文限定 **KOR**，且死的是 **tone/event-score** 族。

⇒ 本波机制**刻意避开纯 tone/event-score**，走 novelty / relevance 离散度 / 事件量 / index 占比四族（与 KOR 死路正交）。

**★ GBR news 域三个 prod 雷区骨架（闸 PF 实测）**：`group_rank→ts_delta`、`group_rank→ts_decay_linear`、`rank→ts_quantile`。
⇒ 「group_rank + 时序变化」在 GBR 反复撞 prod 墙；等价替换用 `group_rank(ts_zscore(..., 252), axis)` 或 `ts_zscore(...)` 裸用。

**★ 闸 OPS 铁律实战**：表达式内**函数调用点须 < 10**。GEM 生成的 `if_else(cond, rank(x), reverse(rank(x)))` 恰好 10 点被拦；门控形态改写为 `if_else(cond, rank(x), 0)` 才合规。

**★ 门禁 diversity_gate 判的是结构/构造链**（`diversity_ok=true`），机制熵只是提示级；但机制熵低会触发 QUOTA 告警，补机制仍值得做。

**跨区参照**：论坛 93 票经典配方 `ts_corr(<sent_field>, returns, d)` + 外层 `group_zscore`、中性化 FAST —— 本波已用 `ts_corr(mws50_nip, mws50_ess, 22)` 覆盖 corr 族。

### 2026-10-28 · news50 首波实测（38 条 / 7 批）——★ vea 是本域唯一活机制

**vea = Aggregate Event Volume（91 日事件量）均值回复**：`reverse(ts_zscore(ts_backfill(vec_avg(mws50_vea), N), 252))`

| 变体（一次动一个变量） | S | F | 2Y | SUB | TO | PPA |
|---|---|---|---|---|---|---|
| backfill **5** + `group_neutralize(subindustry)` | **1.04** | 0.53 | 1.14 | **0.87** | 0.160 | ✅ 合格 |
| backfill 5 + `group_neutralize(sector)` | 1.02 | 0.52 | 1.13 | 0.87 | 0.161 | ✅ 合格 |
| backfill 5 / zscore 252 | 1.03 | 0.53 | 1.15 | 0.87 | 0.161 | ✅ 合格 |
| backfill 1 / zscore 252 | 1.03 | 0.46 | 0.98 | 0.87 | 0.224 | ✅ 合格 |
| backfill 22 / zscore 252 | 0.99 | 0.51 | 1.18 | 0.76 | 0.147 | ✅ 合格 |
| backfill 22 / zscore 504 | 0.89 | 0.45 | 0.97 | 0.72 | 0.141 | ✗ |
| backfill 22 / zscore 1008 | 0.98 | 0.54 | 0.99 | 0.76 | 0.136 | ✗ |
| backfill 22 / zscore 1260 | 0.99 | 0.53 | 0.95 | 0.78 | 0.148 | ✗ |
| backfill 66 / zscore 252 | 0.94 | 0.47 | 1.19 | 0.73 | 0.146 | ✗ |
| backfill 22 / `ts_rank` 252 | 0.93 | 0.46 | 0.94 | 0.63 | 0.146 | ✗ |
| backfill 22 / `ts_delta` 22 | 0.53 | 0.18 | 0.16 | 0.37 | 0.198 | ✗ |
| backfill 22 / `ts_mean` 22 | 0.22 | 0.09 | -0.48 | 0.21 | 0.032 | ✗ |
| backfill 22 / `group_rank` 版 | 0.52 | 0.24 | 0.86 | 0.51 | 0.104 | ✗ |

**★★ 三条硬结论**：

1. **vea 族成立但被 S=1.58 闸挡住**（最佳 1.04，差 34%）：5 颗 `checks.fail=[]` / `ppa_failed=false`（**PPA 合格**，PPA 是独立提交线），但 REGULAR 硬闸 LOW_SHARPE=1.58 未过。
2. **★ 必须用 `group_neutralize` 而非 `group_rank`**：`group_rank` 版 S 从 1.03 掉到 0.52（腰斩），`group_neutralize` 版 1.04 ⇒ 与 ess 族同结论，**信号含行业层面成分**，保序排序会抹掉它。
3. **★ 必须反向**（均值回复）：vea 正向为负信号。

**★ 三条负面实证（同批）**：

- **news 极性是 beta 不是 alpha**：`ts_zscore(ts_delta(ts_backfill(vec_avg(mws50_ess),22),5),252)` 裸用 S=+0.67 → 包 `group_rank(subindustry)` 变 **-0.22**；`trade_when(vea>0, group_rank(...), -1)` 同样 -0.19 ⇒ 极性信号在行业内排序后消失。
- **bucket 分组轴结构性爆**：3 条 `bucket(rank(...))` 表达式 TO 1.44-1.47、longCount 29-47、CW 0.5 ⇒ **news 域禁用 bucket 轴**。
- **重复字段**：`mws50_ens_elapsed` 与 `mws50_g_ens_similarity_gap` 产出完全相同 PnL（-6055485）⇒ 二者在 GBR 恒等。

**★ 工程坑（maxTrade 静默降级）**：`mcp__wq-brain-http__create_multi_simulation` 传 `max_trade="ON"` 时，平台实际 settings 仍写 `maxTrade="OFF"`（首两批 16 条全部如此）；同表达式 `reverse(ts_zscore(ts_backfill(vec_avg(mws50_vea),22),252))` 在 OFF 档 S=0.73/2Y=0.67/TO=0.236，在 ON 档 S=0.99/2Y=1.18/TO=0.147 ⇒ **同一表达式差 +0.26 S / +0.51 2Y**。⇒ 派发后必须读回子 alpha 的 `settings.maxTrade` 复核，不能信工具参数。

### 2026-10-28 · ★★★ 等价算子替换突破（本域最高杠杆）

基线 `reverse(ts_zscore(ts_backfill(vec_avg(mws50_vea), 5), 252))` S1.03/F0.53/2Y1.15/TO0.161
→ 外层加**一层** `ts_decay_linear(., 22)`：

| 变体 | S | F | 2Y | SUB | TO | failed_ra |
|---|---|---|---|---|---|---|
| **`reverse(group_neutralize(ts_decay_linear(ts_zscore(backfill(vea,5),252),22), subindustry))`** | **1.26** | **0.80** | **1.79** | 0.89 | 0.088 | **2**（只差 LOW_SHARPE/LOW_FITNESS） |
| `reverse(ts_decay_linear(ts_zscore(backfill(vea,5),252),22))` | 1.24 | 0.79 | 1.77 | 0.89 | 0.090 | 2 |
| `reverse(ts_decay_linear(ts_zscore(backfill(vea,22),252),22))` | 1.24 | 0.78 | 1.79 | 0.77 | **0.0704** | 2 |
| `reverse(ts_decay_linear(group_neutralize(ts_zscore(backfill(vea,5),252),sector),22))` | 1.23 | 0.77 | 1.77 | 0.89 | 0.089 | 2 |

**同位置替换全弱** ⇒ 瓶颈是**噪声/换手**不是形状：

| 替换 | S | F | 2Y |
|---|---|---|---|
| `ts_decay_linear(.,22)` | **1.24** | **0.79** | **1.77** |
| `winsorize(.,std=3)` | 1.07 | 0.55 | 1.13 |
| `ts_rank(.,252)` | 1.06 | 0.53 | 1.02 |
| `signed_power(.,0.5)` | 1.04 | 0.53 | 1.07 |
| 基线 `ts_zscore` | 1.03 | 0.51 | 1.15 |
| `ts_scale(.,252)` | 0.88 | 0.43 | 0.84 |
| `quantile(.)` | 0.69 | 0.41 | -0.53 |

**decay 窗对比（22 最优）**：22 → S1.24/2Y1.77；5 → S1.14/2Y1.42；66 → S1.06/2Y1.57；126 → S0.85/2Y1.18。

**REGULAR 现状**：最佳 S=1.26，距 LOW_SHARPE 1.58 差 0.32；**已过 Mode B 主闸 1.25 与 LOW_2Y_SHARPE 1.58**。下一波方向 = 抬 S（decay 档位 / 慢化 / 结构换轴），不追 F。

**★ decay 档位对照（decay 是强度闸，跨档不可比）**：

| 档 | 最佳表达式 | S | F | 2Y | TO | margin |
|---|---|---|---|---|---|---|
| **decay 4**（权威档） | `reverse(group_neutralize(ts_decay_linear(ts_zscore(backfill(vea,5),252),22), subindustry))` | **1.26** | 0.80 | 1.79 | 0.088 | 0.00116 |
| decay 8 | `reverse(ts_decay_linear(ts_zscore(backfill(vea,22),252),22))` | 1.25 | 0.79 | 1.86 | **0.0668** | 0.00149 |
| decay 20 | `reverse(group_neutralize(ts_decay_linear(ts_zscore(backfill(vea,22),252),22), subindustry))` | 1.24 | 0.78 | 1.91 | **0.0579** | **0.00169** |

⇒ **decay 档位只降换手、抬 margin，不抬 S**（S 1.26→1.25→1.24 单调微降）。**decay 不是抬 S 的杠杆**，且降档会推高 self 相关性（EUR wave274 教训）⇒ 保持权威档 decay 4。

**★ 本波 S 天花板判定**：vea 机制在 GBR 的 S 稳定在 **1.24-1.26**，覆盖 backfill(5/22/66) × 窗口(22/252/504/1008/1260) × decay(4/8/20) × 平滑窗(5/22/44/66/126) × 轴(裸/group_neutralize×subindustry/sector/group_rank) ⇒ **参数维度已穷尽**（>40 结构）。要过 REGULAR LOW_SHARPE 1.58 必须**换机制或换数据集**，不得再刷参数。

### 2026-10-28 · ★ ATOM 放宽的边界（本波实测澄清，避免下轮误判）

本波 74 颗**全是 ATOM**（单数据集）。为确认「ATOM 享近 2 年 Sharpe 放宽」到底放宽了什么，查官方文档 + 平台实测：

| 检查 | ATOM 候选（`1YNEqJbQ`）的平台读数 | 是否豁免 |
|---|---|---|
| `LOW_2Y_SHARPE` | **PASS**（2Y=1.79） | — 常规线本就过 |
| `IS_LADDER_SHARPE` | **不在 checks 里** | ✅ **唯一被豁免的**（ATOM 改用 Last-2Y 判；官方表在平台文档，TO<30% 时该 PASS 阈值 ×0.85） |
| `LOW_SHARPE`（全期） | warning（1.26 vs limit 1.58） | ❌ **不豁免**（在 RA 名单内，WARNING 计失败） |
| `LOW_FITNESS` | warning（0.80 vs limit 1.0） | ❌ **不豁免** |

⇒ **★ ATOM 省掉的是「ladder 那一步」，不是「全期 S 1.58」**。`submit_verdict` 对 `1YNEqJbQ` 判 **BLOCKED**（LOW_SHARPE + LOW_FITNESS），与平台一致，**不是本库口径 bug**。

⇒ **对 ATOM 候选的优化目标要改口径**：抬**近 2 年 Sharpe**（本波已到 1.79-1.91）并不够，还要把**全期 S 抬到 ≥1.58、F 抬到 ≥1.0**；两者同时满足才有提交资格。

<!-- profiles:manual:end -->
