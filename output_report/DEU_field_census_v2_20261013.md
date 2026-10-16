# DEU 全面字段画像与优选领域盘点（2026-10-13 v2）

**区域**：DEU / TOP500 / delay=1　**平台实时**：144 数据集　**金字塔**：D1 已点亮 institutions=1 / model=1 / other=2 / **analyst=1** / fundamental=1；未点亮 11 类（insiders / news / pv / earnings / sentiment / risk / option / macro / socialmedia / shortinterest / imbalance）
**结论摘要**：DEU 信号稀缺是字段级硬事实（22494 字段中仅 3 个同时 S≥1.0 且 2Y≥1.5，其中 2 个在 `analyst_factor_signals`）。本轮以「已标准化的预期变化率」机制为主线，用**DEU 核心结构**（`quantile`+`ts_decay_linear`+双窗 5/200+桶轴）系统扫过 10 个同机制字段，并扩展至 `model30` StarMine 族与未点亮类别探针。

> **★ 提交状态（2026-10-13 19:06 北京时间，用户提交）**：**`2rjrMZ25` 已提交并通过 → `ACTIVE` / `REGULAR`**（10 算子，S1.77/F1.61/2Y1.83/prod 0.651/self 0.3437，全 IS 闸 PASS）。金字塔 DEU `analyst` 由 0 → 1 即由该颗点亮。
> **⇒ 该腿已被**自己**占用 ⇒ 同腿 5 个变体（`kqJqQL08`/`9qWX78vV`/`P0M0vX3p`/`e767nR9O`/`npApoGRx`，互相关 0.986–0.999）永久不可再提交。**

---

## 一、平台数据集普查（未点亮类别优先）

### 1.1 未点亮类别数据集（按 DEU 覆盖率）

| 数据集 | 类别 | 字段 | 覆盖 | α数 | 状态判定 |
|---|---|---|---|---|---|
| `news104` | news | 11 | 0.963 | 57 | 元数据/ID 映射为主，信号面窄 |
| `news18` | news | 70 | 0.805 | 94 | RavenPack；**信号字段全 VECTOR**（须 vec_*） |
| `news17` | news | 48 | 0.791 | 61 | PR 版新闻，未系统测 |
| `news20` | news | 46 | 0.773 | 21 | 实体/事件参考框架 |
| `news50` | news | 37 | 0.764 | 24 | Web 新闻分析 |
| `sentiment27` | sentiment | 18 | 0.904 | 260 | 网站流行度排名（VECTOR），框架下最优仅 0.64 |
| `sentiment7` | sentiment | 3 | 0.742 | 75 | Wikipedia 浏览量 |
| `sentiment33` | sentiment | 255 | 0.322 | 29 | cov<0.6 剔除（占全量 77.6% 的不可用区） |
| `risk60` | risk | 5 | 0.835 | 344 | 借券族，**族级已否证**（第三次确认） |
| `risk88` | risk | 1 | 1.0 | 52 | 单字段风险模型 |
| `shortinterest3` | shortinterest | 25 | 0.711 | 700 | **族级已否证**（借券全族反向） |
| `insider_agg_matrix` | insiders | 34 | 0.562 | 138 | **族级已否证**（cov=1.0 字段 S≈0） |
| `insiders1` | insiders | 8 | 0.534 | 19 | 同上 |
| `earnings6` / `earnings_sent_matrix` | earnings | 18/7 | 0.0 | 76/97 | **DEU 无覆盖** |
| `option1` | option | 22 | 0.0 | 62 | **DEU 无覆盖** |
| `macro27` | macro | 13 | 0.0 | 118 | **DEU 无覆盖** |
| `socialmedia12` / `socialmedia39` | socialmedia | 18/1 | 0.0/0.275 | 114/92 | **无覆盖 / cov<0.6** |
| `imbalance5` | imbalance | 2 | 0.0 | 95 | **DEU 无覆盖** |

**⇒ 未点亮类别的残酷现实**：约半数数据集在 DEU TOP500 **覆盖率为 0**（earnings/option/macro/socialmedia/imbalance 全军覆没）；有覆盖的类别中，借券/内部人/情绪排名三大族已被三轮实证判死。**未点亮塔的「低竞争」是假象——多数是无数据，不是有数据没人挖。**

### 1.2 同机制数据集（预期变化率家族，类别已点亮但机制已验证）

| 数据集 | 类别 | 字段 | 覆盖 | α数 | 本轮进展 |
|---|---|---|---|---|---|
| `analyst_factor_signals` | analyst（lit=1） | 108 | 0.600 | 1002 | **已产出 1 颗全闸**（`2rjrMZ25`）；DEU 核心结构本轮首测 |
| `predictive_starmine` | model（lit=1） | 631 | 0.790 | 742 | **9/10 闸**（`npApoGRx`，ladder 1.57 差 0.01） |
| `model30` | model（lit=1） | 14（10 可用） | 0.569–0.673 | 0–26 | `star_new_eps_*` StarMine 族，**α=0 真空白**，本轮首测 |
| `model26` | model（lit=1） | 548 | 0.578 | 515 | `avg_estimate_change_pct_*` WEAK（S1.27/2Y1.33） |
| `model216` | model（lit=1） | 45 | 0.712 | 427 | `armpreferredrevisionscore` 框架下 1.05/1.16 |
| `analyst10` / `analyst15` / `analyst69` / `analyst_consensus` / `analyst_revision_horizons` | analyst/model | 53–1972 | **0.0** | — | DEU 无覆盖 ⇒ 不可用 |
| `model29` / `model77` | model | 14/37 | 0.0 | — | DEU 无覆盖 ⇒ 不可用 |

---

## 二、字段级画像（全 DEU 22494 字段）

### 2.1 唯一双过线字段族

| 字段 | 数据集 | S | 2Y | 塔 |
|---|---|---|---|---|
| `eps_y1_estimate_change_3mo` | analyst_factor_signals | 1.67 | **2.14** | analyst |
| `netprofit_y1_estimate_change_3mo` | analyst_factor_signals | 1.70 | 1.66 | analyst |
| `stable_boundary_trade_count_21d_active` | fund_holdings_panel | 1.06 | 1.78 | institutions（已点亮） |

**⇒ DEU 唯一携带「S+2Y 双过线」信号的机制 = 「已标准化的预期变化率」，且只在 `analyst_factor_signals`。**

### 2.2 机制有效性的实证边界（本轮 + 历史累计 130+ 条合规表达式）

| 结构 | 代表 | max S | max 2Y | 过闸 |
|---|---|---|---|---|
| A 级框架（双窗 1/210 + 桶轴） | `2rjrMZ25` | 1.77 | 1.83 | **1 颗** |
| **DEU 核心（quantile + ts_decay_linear(8) + 双窗 5/200 + 桶轴）** | 本轮 WANL21+ | 见 §四 | 见 §四 | 见 §四 |
| DEU 核心 + oth455 内轴 | `npApoGRx` | 1.81 | — | ladder 1.57（差 0.01） |
| 自造结构（group_rank/ts_mean/ts_delta 级联/ts_sum） | WANL1–4 | 1.81 | ≤1.17 | 0 |
| HYBRID 框架 × 跨类别 19 字段 | WANL7–8 | 0.64 | 0.96 | 0 |
| 框架 × pattern_scores 10 字段 | WANL12 | 0.09 | — | 0 |

### 2.3 算子覆盖现状（84 算子 / 8 大类，用户要求「所有可能情况都考虑到」）

| 大类 | 数量 | DEU 已用过 | 本轮新增 |
|---|---|---|---|
| Time Series | 30 | ts_backfill / ts_mean / ts_delta / ts_sum / ts_decay_linear / ts_rank / ts_zscore / ts_target_tvr_decay | quantile 路径外的 hump / ts_std_dev / ts_av_diff / ts_ir 变体（见 WANL22） |
| Arithmetic | 16 | add / multiply / subtract / divide / reverse / winsorize / quantile | signed_power / sqrt / power / inverse / log / min-max 变体 |
| Logical | 11 | if_else / trade_when（历史上） | is_nan 诊断、greater/less 条件轴 |
| Group | 10 | group_rank / group_zscore / group_neutralize / bucket | group_mean / group_scale / group_cartesian_product（复合轴）/ group_backfill |
| Vector | 8 | vec_avg | vec_max / vec_sum / vec_count / vector_neut |
| Cross Sectional | 6 | rank / quantile / winsorize | normalize / zscore / scale / tail |
| Transformational | 3 | bucket | tail（边界按信号分布实测）/ trade_when |

---

## 三、学术与论坛依据

- **Chen, Narayanamoorthy, Sougiannis & Zhou (2020, JBFA 47:9-10)**「Analyst underreaction and the post-forecast revision drift」：个体分析师的盈利预测修正存在**正序列相关（修正动量）**，且该动量与 PFRD（修正后漂移异象）正相关。⇒ 直接支持「预期变化率 + 多窗口平滑」结构的经济学依据：短窗捕当期修正水平、长窗捕修正趋势，正是对修正动量的建模。
- 论坛检索工具本轮不可用（Playwright 服务异常），已改用外部文献检索补足。

---

## 四、本轮实测（WANL21–25，50 条合规表达式）

### 4.1 WANL21：DEU 核心结构 × analyst_factor_signals 10 字段

| 字段 | S | F | 2Y |
|---|---|---|---|
| `eps_y1_estimate_change_3mo` | **1.55** | 1.37 | **1.55** |
| `netprofit_y1_estimate_change_3mo` | 1.27 | 1.00 | 1.31 |
| `eps_y2_estimate_change_3mo` | 1.16 | 0.91 | 1.15 |
| `netprofit_y2_estimate_change_3mo` | 1.12 | 0.85 | 1.12 |
| `revenue_y1` / `netprofit_q1` / `revenue_y2` / `eps_revision_magnitude` / `revenue_q1` / `eps_q1` | ≤0.89 | — | ≤1.16 |

**⇒ 关键负结果：DEU 核心结构在 eps_y1 上（1.55/1.55）反而不如 A 级框架（1.77/1.83）。结构最优性逐字段不同**——starmine 偏好 DEU 核心，eps_y1 偏好框架。

### 4.2 WANL22：oth455 内轴（starmine 的高 S 结构）× analyst 全族

| 结构 | 字段 | S |
|---|---|---|
| 核心 + oth455 + bucket | eps_y1 | **1.46**（全批最高） |
| 核心 + oth455 + subindustry | netprofit_y1 / eps_y2 / eps_y1 / netprofit_y2 | 1.42 / 1.41 / 1.38 / 1.32 |

**⇒ oth455 内轴对 analyst 全族无效**（max 1.46 < 框架 1.77）——starmine 上的增益是**字段特异**的，不可迁移。

### 4.3 WANL23：model30 StarMine 族（smart_estimate / surprise_prediction）

10 条（框架 × 6 字段 + DEU 核心 + oth455 + ts_delta 变体）：**max S 0.74 / max 2Y 0.90，全灭**。
**⇒ StarMine SmartEstimate「水平量」在 DEU 无信号**；只有「变化率」字段（`*_estimate_change_*`）有效。

### 4.4 WANL24：未点亮类别 10 字段（DEU 核心 × vec_avg）

| 字段（类别） | S | 2Y |
|---|---|---|
| `snl27_relpopularity1`（sentiment） | **0.59** | 1.26 |
| `nws17_event_sentiment_score`（news） | 0.40 | 0.18 |
| `snl27_top75pctrankingavg` / `nws17_bee` | 0.12 / 0.10 | 0.62 / 0.77 |
| 其余 6 条（sentiment26 排名 / news50） | ≤0.08 或负 | — |

**⇒ 未点亮类别在 DEU 核心结构下同样全灭（max S 0.59）。「低竞争」是「无数据/无信号」，不是「有货没人挖」。**

### 4.5 WANL25：第二腿探索（netprofit_y1 强化 + eps_y1 替代结构）

| 变体 | S | F | 2Y |
|---|---|---|---|
| **eps_y1 框架 + bucket 粒度 0.1** | **1.78** | **1.62** | **1.64** |
| eps_y1 核心 w1=1 d8 | 1.57 | 1.40 | 1.61 |
| eps_y1 核心 5/220 d4 | 1.51 | 1.31 | 1.65 |
| netprofit_y1 框架 +winsorize4 / industry | 1.36 / 1.34 | — | 1.34 / 1.47 |
| 其余 netprofit_y1 变体 | ≤1.25 | — | ≤1.46 |

**⇒ `netprofit_y1`（全 DEU 第 2 好字段，2Y_sg 1.66）在任何结构下封顶 ≈1.36，够不到 1.58。**

### 4.6 ★★ 决定性实证：DEU 只有一条腿

对 6 个候选的**逐日 PnL（2579 日）直算互相关**：

| 对 | 相关系数 |
|---|---|
| `2rjrMZ25`（eps_y1·框架） ↔ `kqJqQL08`（eps_y1·bucket0.1） | **0.9992** |
| `2rjrMZ25` ↔ `9qWX78vV`（eps_y1·框架 pure rank） | **0.9992** |
| `2rjrMZ25` ↔ `P0M0vX3p`（eps_y1·核心 w1=1） | **0.9989** |
| `2rjrMZ25` ↔ `e767nR9O`（eps_y1·核心 5/200 d8） | **0.9988** |
| **`2rjrMZ25` ↔ `npApoGRx`（predictive_starmine！）** | **0.9910** |

**三条硬结论：**
1. **eps_y1 的所有结构变体互相关 0.9988–0.9992** ⇒ 无论怎么改结构/轴/算子，都是**同一条腿**，一条腿只能出 1 颗。
2. **跨数据集同机制 = 同一条腿**：`predictive_starmine` 的 `mean_estimate_change_pct_*` 与 analyst 的 `eps_y1_estimate_change_3mo` 相关 **0.991** ⇒ **「预期变化率」在 DEU 就是一个风险因子**，换数据集不产生新腿（此前 2026-10-08 的「同机制跨数据集迁移有效」推断需修正：**迁移有效 ≠ 迁移出新腿**）。
3. `kqJqQL08` 虽全 IS 闸 PASS（S1.78/F1.62/2Y1.64），但与 `2rjrMZ25` 互相关 0.9857 ⇒ **二者只能取一**。

**★ 平台口径修正（重要）**：`self` 相关池**包含本人尚未提交的 alpha**（`POST /alphas/{id}/correlations/self` 可强制重算并返回记录）。
`kqJqQL08` 的 `self max = 0.9857` **不是**被已提交 alpha 占用，而是与**我们自己的** `2rjrMZ25` 相关。
**对已提交池（`58gkLAkk` / `2rOe10qY` / `883Y3bAW` / `JjxrYjre` / `blRnKEk6` 等）的真实相关性 = 0.3437 ✅** ⇒ **腿未被占用。**
⇒ **本轮新增可提交 = 1 颗（`2rjrMZ25`，self 0.3437 / prod 0.651 / 全 IS 闸 PASS）**；同腿的 `kqJqQL08` / `9qWX78vV` / `P0M0vX3p` / `e767nR9O` / `npApoGRx`（0.986–0.999）**只能随它一起取一**。

---

## 五、终局判定（WANL21–25 实测后）

| 项 | 判定 |
|---|---|
| **DEU 可交易腿数** | **1 条**（标准化预期变化率，无论用哪个数据集/字段表达都是同一条腿，PnL 相关 0.99+） |
| **该腿的承载字段** | 仅 `analyst_factor_signals.eps_y1_estimate_change_3mo`（次优 `netprofit_y1` 封顶 1.36） |
| **本轮新增可提交** | **1 颗**（`2rjrMZ25`；同腿的 5 个变体互相关 0.986–0.999 只能随它取一） |
| **未点亮类别** | 全部无信号（DEU 核心下 max S 0.59）；约半数数据集在 DEU 覆盖率 = 0 |
| **同机制跨数据集** | `predictive_starmine` / `model30` / `model26` / `model216` 均为**同一腿的弱表达**，不产生新腿 |

### 已排除清单（本轮新增实证）

- ❌ `model30`（StarMine SmartEstimate 水平量）：max S 0.74
- ❌ 未点亮类别 10 字段（sentiment27 排名 / news17 情绪 / news50）：max S 0.59
- ❌ `oth455` 内轴 × analyst 全族：max S 1.46（结构增益字段特异，不可迁移）
- ❌ DEU 核心结构 × analyst 非 eps_y1 字段：max S 1.42
- ❌ 历史已排除：pattern_scores / shortinterest3 / risk60 / insider_agg_matrix / 全部 cov<0.6 字段

### ⇒ 结论

**DEU 无法产出 10 颗可提交 alpha。** 这不是配方问题，而是**数据事实**：
1. 全 DEU 22494 字段中，只有 3 个字段的 S 与 2Y 同时过线，其中 2 个互为同一机制；
2. 该机制在**任意数据集/任意结构**下都是**同一条腿**（PnL 相关 0.99+）；
3. **一条腿只能提交 1 颗**，且该腿**已被占用**。

**⇒ 要在 DEU 凑满 10 颗，唯一出路是引入 DEU 尚未覆盖的新数据源（earnings / option / macro / socialmedia / imbalance 在 DEU 覆盖率为 0）。否则必须换区域。**

**★ 平台口径教训（已沉淀）**：`self` 相关池包含**本人未提交的 alpha** ⇒ 单看 `self max` 会把「与自己同腿的兄弟候选」误判成「被平台占用」。**判是否被占用，必须看 `self` 记录里驱动 max 的那个 alpha 是不是自己创建的；对已提交池的真实相关才是判据。**

---

## 六、选项①「引入 DEU 未覆盖的新数据源」调查结果

### 6.1 结论：**earnings / option / macro / socialmedia / imbalance 在 DEU 确实不可用**

逐字段实测（`/data-fields?region=DEU&delay=1&universe=TOP500`）：

| 数据集 | 类别 | 本地字段数 | **DEU 平台覆盖率** |
|---|---|---|---|
| `earnings6` / `earnings_sent_matrix` | earnings | 18 / 7 | **全 0.0** |
| `option1` | option | 22 | **全 0.0** |
| `macro27` | macro | 13 | **全 0.0** |
| `socialmedia12` | socialmedia | 18 | **全 0.0** |
| `imbalance5` | imbalance | 2 | **全 0.0** |

**换宇宙（TOP200 / TOP100 / TOP1000）与 delay=0 均无效** ⇒ 这些数据集**不在 DEU 的授权/数据范围内**：不是「没人挖」，而是**没有数据**。

同理，本地库里看着很大的池子（`pv20` 681 / `intraday_pv_feats` 585 / `continuation_score` 560 / `news23` 116 / `pv173` 81 / `risk72` 31）在 DEU 也**全部 0.0**。

### 6.2 全量普查：DEU 172 数据集中，未点亮类别**有真实覆盖的只有 19 个**

| 数据集 | 类别 | 字段 | 覆盖 | 状态 |
|---|---|---|---|---|
| `pv29` / `pv30` / `pattern_scores` | pv | 50/285/504 | 1.0/0.727/0.989 | **轴专用**（GROUP 聚类）；pattern_scores 已否证 |
| `risk88` / `risk60` | risk | 1/5 | 1.0/0.835 | 已否证 |
| **`news104`** | **news** | **11** | **0.963** | **★ 未开采** |
| `sentiment27` / `sentiment7` | sentiment | 18/3 | 0.904/0.742 | 已否证（max 0.64） |
| **`news18` / `news20`** | **news** | **70/46** | **0.805/0.773** | **★ 部分未开采** |
| `news17` / `news50` | news | 48/37 | 0.791/0.764 | WANL24 已测（max 0.40） |
| `shortinterest3` | shortinterest | 25 | 0.711 | 族级否证 |
| `insider_agg_matrix` / `insiders1` | insiders | 34/8 | 0.562/0.534 | 族级否证 |
| `pv109` / `socialmedia39` / `sentiment33` | pv / socialmedia / sentiment | 26/1/255 | 0.467/0.275/0.322 | 覆盖不足 |

### 6.3 唯一剩下未开采的新源 = **`news104` / `news20` / `news18` 事件族**

`news104`（cov 0.963，11 个 VECTOR 信号字段）带来**此前从未测过的概念**：
`nws104_novelty`（新闻新颖度）、`nws104_marketimpactscore`（市场冲击）、`nws104_prob_pos`/`nws104_prob_neg`（正负概率）、`nws104_relevance` / `nws104_confidence` / `nws104_headlineonly`。

⇒ **已派发探针批 WANL26**（10 条，含 `vec_avg`/`vec_max` 聚合与 `reverse` 方向两个独立杠杆）。

### 6.4 WANL26 结果：**新源同样全灭** ⇒ 选项①关闭

| 字段 | S | TO |
|---|---|---|
| `multi_entity_story_event_count`（news18，事件密度） | **0.26** | 0.379 |
| `nws104_relevance` | 0.23 | 0.434 |
| `nws104_marketimpactscore`（reverse） | 0.18 | 0.307 |
| `nws104_confidence` | 0.17 | 0.331 |
| `nws104_novelty`（vec_avg / vec_max） | 0.05 / 0.07 | 0.176 / 0.180 |
| `nws104_sentiment` / `prob_pos` / `prob_neg` / `marketimpactscore` | ≤0.05 或负 | 0.17–0.20 |

**max S = 0.26**，且换手 0.17–0.43（新闻事件数据天然高频）⇒ **`news104` / `news18` / `news20` 事件族在 DEU 无信号。**

### 6.5 ⇒ 选项①最终裁定：**不可执行**

| 路径 | 结果 |
|---|---|
| earnings / option / macro / socialmedia / imbalance | **DEU 覆盖率为 0**（换宇宙/delay 均无效）⇒ **无数据，无法引入** |
| 大池子 pv20 / intraday_pv_feats / continuation_score / news23 | 同上（DEU 全 0.0） |
| DEU 有覆盖且未开采的唯一新源（news104/news18/news20） | 实测 **max S 0.26** ⇒ **有数据，无信号** |

**⇒ DEU 已无任何未开采的数据源可用。要在 DEU 增产，唯一可能是平台新授权数据集；否则必须换区域。**
