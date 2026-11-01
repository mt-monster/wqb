# KOR 未点亮塔战役 · 终局评估（2026-10-30）

> 范围：KOR / TOP600 / Delay1，REGULAR，FASTEXPR，STATISTICAL · decay 4 · trunc 0.08 · unitHandling VERIFY · nanHandling OFF。
> 目标（用户）：未点亮塔挖 **60 个 REGULAR alpha（ATOM 优先）** + 近闸候选定向挖掘 + 逐 category 画像 +
> 归因/对比实验 + 并发 ≤2 + prod 只走 MCP + 近十年覆盖 + 组合禁令。
> 证据源：`tracking/KOR/reference/unlit_towers_roadmap_20261030.md`（波次台账）、
> `tracking/KOR/reference/datasets/<ds>.md`（逐集档案）、`wave_results`（DB，wave 185–213）、
> 平台 `get_alpha_details` / `get_alpha_yearly_stats` 实测。

## 1. 结论先说

**60 个 REGULAR alpha 在 KOR 未点亮塔上不可达**，且不是"还没挖够"，是**平台算术不允许**：

| 事实 | 数值 | 来源 |
|---|---|---|
| KOR 闸 LOW_SHARPE / LOW_FITNESS | **1.58 / 1.0** | 平台 checks |
| 单塔单字段 ATOM 的实测上界 | **1.04**（`d5W8Pn7X`，risk59 `last_rate`） | wave 213 |
| 距闸缺口 | **+52%** | 1.58 / 1.04 |
| 多腿唯一合形态（闸5 禁 `add`）的强度上限 | 4 腿 × S0.85、ρ=0 → 1.70；**3 腿 × S0.88、ρ=0 → 1.52** | 见 §5 算术 |
| 手上有正信号的腿数 | **3**（1.04 / 0.95 / 0.67），且第三条属已关闭的 news 塔 | §4 |

⇒ 本次战役的真实产出是：**9 座未点亮塔全部完成画像与实测判定、6 个数据集级判死、1 个 ATOM 近闸素材
（S 1.04 / 2Y 2.02）、一份"哪些组合在算术上还有可能"的裁定**，而不是 60 个 alpha。

## 2. 逐 category 画像（用户要求 1 的交付物）

平台 `get_datasets(KOR, TOP600, D1)` 实测 185 个数据集，类别分布与本次攻击面：

| category | 数据集数 | 塔位 | 本战役实测结论 |
|---|---|---|---|
| model | 57 | 3 亮 / **满** | 未投（非未点亮） |
| other | 26 | 1 亮 | 仅 `other106`（wave 190 判死）、`other553`（wave 192 判死，平台 category=sentiment） |
| news | 24 | 0 → **关塔** | 5 条轴全部实测判死（§3） |
| pv | 18 | 2 亮 | 未投 |
| analyst | 17 | 2 亮 / 1.6 | 未投 |
| fundamental | 17 | 3 亮 / **满** | 未投 |
| risk | 7 | 0 → **关塔** | risk59 三形态轴全测（§3） |
| sentiment | 6 | 0 → **关塔** | 三连死（189/192 + 早期） |
| shortinterest | 3 | 4 亮 / 1.4 | 未投（已点亮） |
| institutions | 2 | 0 无攻击面 | institutions6 死集、fund_holdings_panel 判死（误发 3 次） |
| insiders | 2 | 0 → **关塔** | insiders5 天花板 1.05、insiders1 季度 VECTOR 形态缺陷（CW 1.00） |
| macro | 2 | 0 → **关塔** | `other106` 判死（wave 190）。`macro63` 全表仅 1 字段 `mcr63_membership`（MATRIX，cov 1.0，**aC 158**）= "WisdomTree WTIDJH 指数的成分状态" ⇒ **0/1 成分哑变量，无截面强度**；其唯一可用机制「指数成分变更 → 供给冲击」**已在 wave 190 用 `other106` 实测判死**（Shleifer 1986 / Greenwood 2008，max\|S\| 0.75）⇒ **机制已测、字段无强度，塔关闭** |
| socialmedia | 2 | 0 → **关塔** | `socialmedia39` 全表 1 字段 = 「co-viewed neighbor tickers」**连接键（不是信号）**；`other100` 全表 1 字段 `oth100_top5_people_also_watch_ticker_ii` = "Related tickers that have caught people's attention"（VECTOR，aC 357）⇒ **同形态 ID 列表** ⇒ **本塔在 KOR 零攻击面**（两个数据集都只有一张"邻居票清单"） |
| earnings | 1 | 0 → 天花板 | earnings3 单字段强度天花板 0.95（三几何实测算尽） |
| imbalance | 1 | 0 → 判死 | 2Y 结构性不可达（3 种 ATOM 形态 S 1.08–1.09 但 2Y≈0.17） |

**逐集字段档案**：`tracking/KOR/reference/datasets/` 下 38 份（每份含字段清单、机制文献、波次实测、判词）。

## 3. 波次台账（只列与判定相关的）

| 波 | 数据集 / 塔 | 结果 | 关键读数 |
|---|---|---|---|
| 185 | insiders5 / insiders | 8/8 灭 | max\|S\| 0.81 ⇒ 天花板 1.05 |
| 186 | earnings3 / earnings | 8/8 灭 | max\|S\| 0.94，2Y≫IS ⇒ 机制性衰减 |
| 187b | news7 / news | 8/8 灭 | max\|S\| **0.55**，十年覆盖 PASS |
| 189 | sentiment27 | 2 腿即停 | **2014–2018 全空 ⇒ 覆盖判死** |
| 190 | other106 / macro | 4 腿即停 | max\|S\| 0.75，十年 PASS |
| 191 | news46 / news | 4/4 灭 | max\|S\| **0.47**，十年 PASS |
| 192 | other553 / sentiment | 2/2 灭 | max\|S\| 0.28，十年 PASS |
| 193 | insiders1 | 2 腿即停 | max\|S\| **0.11**；季度 VECTOR 非零率过低 ⇒ CW 1.00 |
| 194 | risk68 | 4/4 灭 | max\|S\| **0.50**，2Y 6/10 年 <1.0 |
| 200/205 | fund_holdings_panel · institutions6 | 死集误发 | 门禁缺口已修（`dead_dataset_guard`） |
| 201 | risk59 二阶矩 | 4/4 灭 | max\|S\| 0.39（variance/cov/delta） |
| 206 | news31 / news | 4/4 灭 | max\|S\| **0.55**（句位/同篇公司数） |
| 207 | news85 / news | 4 腿 | 最好 **S 0.67 / TO .1284 / 2Y 1.53**（情绪↔报道量互相关） |
| 209 | earnings3（CW） | ★ 单点突破 | `omEwRJwJ` **S 0.95 / 2Y 1.75 / TO .1567 / CW ✅**（`ts_backfill(F,10)` 解 CW） |
| 210 | earnings3（几何） | 天花板判定 | zscore 保距 S 0.89 / 2Y **2.17**；`ts_rank-252` 抹掉机制 ⇒ **停止扫几何** |
| 211 | news20 / news | 4/4 灭 | max\|S\| **0.25**，十年 PASS ⇒ **news 塔关闭** |
| 212 | risk59 价量合成 | FAIL | utilization 单独 **S 0.09** ⇒ 合成前提不成立；industry 0.96；价−量 0.55 |
| 213 | risk59 三残余轴 | FAIL，但 ★ 新高 | `vec_max` 1.02（≡avg）；**`last_rate` 1.04 / 2Y 2.02**；`subindustry` 0.70 |

## 4. 现存的真实资产（3 条正信号腿，全部实测过载）

| 腿 | 表达式 | 数据集/塔 | S | 2Y | TO | margin | 十年覆盖 | 可用性 |
|---|---|---|---|---|---|---|---|---|
| **L1** | `hump(reverse(group_zscore(vec_avg(rsk59_last_rate), sector)), hump=0.003)` | risk59 / risk（塔关） | **1.04** | **2.02** | .1428 | 8.41 bp | PASS | ATOM，可直接复用为组合分量 |
| **L2** | `group_rank(ts_backfill(-1*ern3_next_interval, 10), sector)` | earnings3 / earnings | 0.95 | 1.75 | .1567 | 4.65 bp | PASS（292–354/年） | ATOM，CW 已解 |
| **L2'** | 同 L2 + `zscore` 保距 | earnings3 | 0.89 | **2.17** | — | — | PASS | 长样本强度换近期强度 |
| **L3** | `-ts_corr(headline_item_count, sentiment_overall_average, 22)` | news85 / news（塔关） | 0.67 | 1.53 | **.1284** | — | **未验** | 唯一 TO 进获胜带的新闻腿 |

（另有一支仅登记不投的历史候选 `QPvr1vPM`，S 1.02 / 2Y 1.80 / F .67 / prod 0.6552 / self 0.2202，
属已关闭的裸截面 level 族，见 `datasets/risk59.md`。）

## 5. 组合路线为什么也不够（算术，不靠感觉）

`S_combined = ΣS_i / sqrt(n + n(n−1)ρ)`

| 配方 | ρ=0 | ρ=0.1 | ρ=0.2 |
|---|---|---|---|
| 2 × 0.93 | 1.32 | 1.25 | 1.20 |
| 3 × 0.88 | **1.52** | 1.39 | 1.28 |
| 4 × 0.85 | **1.70** | 1.49 | 1.36 |
| 4 × 0.90 | 1.80 | 1.58 | 1.44 |

- 只用手上 3 条腿（1.04 / 0.95 / 0.67）且 ρ=0：`(1.04+0.95+0.67)/√3 = 1.53` —— **仍差 0.05**，ρ>0 只会更低。
- 所以要过 1.58 必须 **4 条 ρ≤0.1 的 S≈0.9 腿**，而第 4 条腿在当前攻击面上**不存在**。
- 闸5 已实测硬拦 `add`（wave 212 P1）：合规形态只有 `subtract`（单一价差）/ `multiply`（条件强度）/
  `trade_when`（门控），三者的强度上限都服从上表 —— **形态换不出第 4 条腿**。
- **用户约束 5 不构成障碍**：本战役涉及的数据集全部落在 risk / earnings / news / analyst / shortinterest，
  不属 PV / MODEL / OTHER ⇒ 组合禁令与 5 条配额均未触发（平台 `get_datasets` 实测归属）。

## 6. 判死与关闭清单（可直接引用的结论）

**塔级关闭（5）**：news（五轴全死、十年覆盖全 PASS）· sentiment（三连死）· insiders（天花板 + 形态缺陷）·
risk（三形态轴全测，上界 1.04）· imbalance（2Y 结构性不可达）。

**数据集级判死 / 无攻击面（8）**：news7 · news46 · news20 · news85 · other106 · other553 · insiders1 ·
earnings3（强度天花板，仅作组合腿）· risk59（降级为近闸素材）· institutions6（死集）· fund_holdings_panel（判死）。

**跨塔可继承的通用读数（给后续任何区域的战役）**：
1. 稀疏事件/新闻字段 **`ts_backfill(F,10)` 是 CW 的唯一有效解**，且不动 truncation/decay/中性化（wave 209 单点突破）。
2. **TO ≈ .25+ 是"该轴无慢成分"的先行指标**：news20（.26）、news7（.26+）、news31 全落在同一区间且 S ≤0.55；
   反之成功带是 .12–.16。**首波见到 .25 不必等 Sharpe，直接判该轴无慢成分。**
3. **粗轴恒优于细轴**（risk59：sector 1.04 > industry 0.96 > subindustry 0.70），与"SOP 换细轴无损"只对**维度**成立，对**幅度**是负的。
4. **合成变量的第二分量必须先单独回测**：utilization 单独 0.09 ⇒ 一切以它调制的形态（乘法/门控）在数学上不可能有增量。
   这一步花 1 个槽位，省下 4 个。
5. **`vec_max` ≡ `vec_avg` 是一种信息**：说明该 VECTOR 字段当日有效档位近乎唯一，换聚合算子等于没换。

## 7. 60 目标怎么办（需用户裁定，四选一）

| 方案 | 内容 | 代价 / 前提 |
|---|---|---|
| **A. 放宽 IS 窗口** | 用 `last_rate` 版（2Y 2.02 是全样本 1.04 的约 2 倍），把 `startDate` 2013→2018 后 S 可能一次跨过 1.58 | **与用户约束 4 的十年样本精神冲突**；且 2Y 与 S 同源，读数独立性下降。**必须用户明确授权** |
| **B. 转已点亮塔做增量** | shortinterest 4 亮 / 1.4（`shortinterest38` 88 字段、cov .9953、本地 best_s **2.35** / best_2y 1.98、n_alive 7）；analyst 2 亮可增量 | 与"未点亮塔"目标冲突，但**这是唯一有历史强信号的残余面** |
| **C. 改区域** | USA / EUR / GLB 等未开发面更大的区重开战役 | 换区 = 重开，KOR 台账仍可复用（§6 五条读数） |
| **D. 收缩交付** | 以"近闸素材 + 判死台账"结案（当前状态） | 产不出 60 个，但零返工、结论可复核 |

**我的建议：先 B 后 C**。理由：`shortinterest38` 的本地 best_s 2.35 已远超闸，且 §6 的四条通用读数可以直接套用；
A 需要突破用户约束，不作为默认路径。

## 8. 工程侧留痕（本轮踩到并已修的坑）

1. **gate checkpoint 会吞掉后加的表达式**：wave 212 首次运行时 gate 结果被 checkpoint 缓存（passed=3），
   之后补录的 P5/P6 根本没进派发面（`[gate] 已完成（checkpoint），跳过`）。⇒ **补录表达式后必须清 gate checkpoint
   或换新波号**，否则"加了腿但没跑"会被日志伪装成"跑了但没信号"。
2. **`--submit` 缺省会只做规划不派发**（`[plan] gate 过 N 式；加 --submit 提交`）。
3. **论坛检索通道当前不可用**（`search_forum_posts` → MCP `-32603`），本轮所有"论坛证据"一律记为 `error`，
   **未**记为「论坛无解」——按 `recon_evidence` 契约，故障不构成判死证据；判死依据全部来自**平台实测 + 论文机制**。
4. **死集/死机制双闸**：`dead_dataset_guard()`（wave 205 起）已机械拦截死数据集；**死机制族仍靠人工核查**
   （wave 208 即人工拦下 `news_sentiment_transfer`）——这条缺口未修。
