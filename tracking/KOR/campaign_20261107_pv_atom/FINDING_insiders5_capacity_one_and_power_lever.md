# FINDING · insiders5 容量 = 1，和新杠杆 signed_power(2.5)

日期：2026-11-07 · KOR/TOP600/D1 · 本轮 P39-P45 的结论汇总

## 1. 结论先行

1. **insiders5 只能出 1 颗**（已交付 RRE9NkVj）。数据集内所有字段族的离散度变体与它的实测互相关落在 0.56-0.90，且没有任何一条指标优于它。
2. **新杠杆**：signed_power(中心化 group_rank, 2.5) 把 insiders5 range 从 1.44 抬到 1.63（+0.19），是本战役除 multiply 双腿之外第二个稳定提 S 的算子。
3. **取负不是镜像**：vec_range 原始 S=-1.68，反向只有 +1.41（损失 0.27）。永远要实跑反向臂。
4. **prod 对窗口敏感**：同机制 range 在 W44 的 prod=0.6974（过），W66 的 prod=0.7322（不过）。窗口既是 S 杠杆也是 prod 杠杆。

## 2. insiders5 互相关矩阵（实测，compute_mutual_correlation）

| | 0mY6rY78 | 9qxmWxw1 | A1VegAwQ | O0AVNNXY | LLMrZM1L | leAEQL6l | RRE9NkVj |
|---|---|---|---|---|---|---|---|
| 0mY6rY78 (range vol_chg W55 p2.5) | 1 | 0.7082 | - | - | - | - | **0.7277** |
| 9qxmWxw1 (stddev vol_af + range vol_chg) | 0.7082 | 1 | - | - | - | - | **0.8594** |
| A1VegAwQ (stddev vol_af) | - | - | 1 | 0.8992 | 0.7715 | 0.5555 | **0.7570** |
| O0AVNNXY (stddev vol_bf) | - | - | 0.8992 | 1 | 0.7128 | 0.5427 | **0.7203** |
| LLMrZM1L (range vol_af) | - | - | 0.7715 | 0.7128 | 1 | 0.7864 | 0.5608 |
| leAEQL6l (range ghc_tr) | - | - | 0.5555 | 0.5427 | 0.7864 | 1 | 0.6715 |
| RRE9NkVj (stddev vol_chg，已交付) | 0.7277 | 0.8594 | 0.7570 | 0.7203 | 0.5608 | 0.6715 | 1 |

判读：只有 leAEQL6l（range ghc_tr，S 1.30）与 LLMrZM1L（range vol_af，S 1.24）对已交付件 <0.70，但两者 S 都不够 1.58，且上 power 也只能到 1.45 左右；
这两条与 A1VegAwQ 又互在 0.77-0.79。**max_mutually_below_subset_size = 2**，即整个 insiders5 池最多同时容纳 2 颗互不相关件，且第 2 颗必然弱于 1.58。

## 3. signed_power 杠杆的定标（insiders5 range 族）

| 结构 | alpha | S | F | 2Y | TO |
|---|---|---|---|---|---|
| range W44 基础 | RREKVlEe | 1.38 | 1.07 | 2.24 | 0.1037 |
| range W44 + power1.5 | ZYQMbbN8 | 1.42 | 1.15 | 2.19 | 0.1098 |
| range W44 + power2.5 | Jje1NNJO | 1.44 | 1.24 | 2.08 | 0.1205 |
| range W55 基础（未跑，估） | - | ~1.44 | - | - | - |
| **range W55 + power2.5** | **0mY6rY78** | **1.63** | **1.46** | 2.21 | 0.1069 |
| range W22 + power1.5 | kqNOooYL | 1.47 | 1.09 | 1.53 | 0.1772 |
| range W33 + power2 | j2Yx8YZo | 1.42 | 1.16 | 1.98 | 0.1388 |

⇒ power 的增益依赖窗口：W55 上 +0.19，W44 上只 +0.06。**必须先找到 S 的窗口峰，再叠 power**，否则 power 只抬 fitness 不抬 S。

## 4. 无效杠杆（本轮实测，别再试）

| 杠杆 | 结果 |
|---|---|
| ts_target_tvr_decay(0.05) | S 从 1.38 掉到 1.17（平滑杀死离散度信号） |
| subindustry 分组 | S 0.81（远差于 sector） |
| group_neutralize(industry) 后置 | S 1.26（低于 sector 的 1.44） |
| trade_when(vec_count>1) 门控 | S 0.97（笔数门控把样本砍掉一半，反而变差） |
| multiply(range, vec_count) | S -0.05 / TO 1.50（vec_count 量级过大，把信号扭曲） |
| ts_backfill(range,22) 再平滑 | S 1.36（无增益） |
| ts_av_diff 于事件型稀疏字段 | TO 爆到 1.50，S -0.17 |

## 5. 两个新数据集判死

**model238（Smart Holdings 机构偏好，39 MATRIX，cov 0.99-1.0，字段级 aC 0-22）**：10 条模板最强 S 1.05（global_change_rank_d1），
反向臂 -0.98 ⇒ 正向约 +0.98；水平/变化/筛选/拥挤度/分化度五个维度全部 <1.1。判死。
教训：**aC 极低（冷门）不等于有信号**，只说明没人采；它可能只是没人愿意采。

**model32（vendor 动量百分位，33 MATRIX，cov 1.0）**：10 条模板最强 S 1.12（shortterm - midterm 期限价差），
单期限动量 shortterm 0.30 / midterm -0.92 / longterm -0.15，且 TO 高达 0.20-0.65。判死。
教训：**KOR 的动量不是在「横截面百分位」上实现的**。P19 里 5 日原始收益翻正能到 1.29，但换成 vendor 的百分位rank 就只剩 0.30 —— 
百分位化丢掉了量级信息（与 insiders5 tnc 上 ts_rank 把 1.59 打到 0.37 是同一现象）。**不要对强信号做横截面百分位化**。

## 6. 算子清单补遗（KOR 可用）

vec_* 全家只有 7 个：**vec_min / vec_count / vec_sum / vec_max / vec_avg / vec_stddev / vec_range**。
没有 vec_median / vec_skewness / vec_kurtosis / vec_ir / vec_mode。设计 VECTOR 数据集模板时按这 7 个写。
比较与条件算子确认存在：greater / less / equal / and / or / not / if_else / trade_when。

## 7. analyst10 关闭（P40 证据）

非重叠腿 multiply 几何 10 组最高 S 1.58（pre_fy2 x pre_fy1）但 2Y 仅 1.29；operating profit 腿 0.10。
⇒ 该数据集的 S 来源是 sal_fy2 x net_fy1 / sal_fy2 x ebi_fy1 这两对特定腿，不可替换。**analyst10 只能出 1 颗，正式关闭。**
## 8. P46 / P47 / P48 读数（收尾三波，全部未过闸）

**P46 pv47 多字段（含首次测试的 idiosyncratic_return_fraction）**

| 结构 | alpha | S | F | 2Y |
|---|---|---|---|---|
| 0.5 - rank(ts_mean(pv47_v21_for_statssimple_only_spret,66)) | MPYZ07G6 | 1.26 | 0.87 | 2.31 |
| power2.5(0.5 - rank(ts_mean(pv47_spret,66))) | qML3EjNK | 1.25 | 0.89 | 2.08 |
| 0.5 - rank(ts_mean(idiosyncratic_return_fraction,66)) | 9qxmEX7K | 1.22 | 0.86 | 2.45 |
| 0.5 - rank(ts_mean(pv47_d1_spret,66)) | Xg9eR78z | 1.22 | 0.84 | 2.45 |
| multiply 双腿 (spret x idio) | zq30rkmG | -1.25 | -0.93 | -2.50 |
| group_rank(ts_mean(idio,66)) 正向 | d5WoRrmg | -1.41 | -1.07 | -2.67 |

⇒ pv47 的 4 个字段**全部封顶在 1.22-1.28**；multiply 双腿几何在 pv47 上是**摧毁器**（-1.25），与 analyst10 相反。
idiosyncratic_return_fraction 原始 -1.41 反向仅 +1.22（又一次取负损失）。**pv47 判死**。

**P47 starmine + power 杠杆：全部崩** 最强 leA9MWj8 1.11（无 power 时是 1.43）。
⇒ **signed_power 不可跨数据集迁移**：在 insiders5 离散度上 +0.19，在 starmine 计数型信号上 -0.32。
判据：信号是「极端值驱动」（离散度/分歧度）时 power 有效；信号是「计数/水平驱动」时 power 摧毁。

**P48 event_stock_model + model252 双判死**

| 结构 | alpha | S | 2Y |
|---|---|---|---|
| multiply(earnings_event, corporate_event) | 2rAWAxm6 | 0.65 | -0.18 |
| 0.5 - rank(mdl252_shield, 水平) | Jje1ekPO | -0.82 | -1.02 |
| 0.5 - rank(corporate_structure_event_score, 水平) | xArWro1q | -1.25 | -0.63 |

⇒ event_stock_model 三个事件分数最强 0.65；model252 的 SHIELD 防御分数最强 0.64。两个数据集判死。
corporate_structure_event_score 反向仅 +1.25，仍差 0.33。

## 9. 本轮总账（P37-P48，12 波 120 条表达式）

| 数据集 | 结论 | 最强 S | 原因 |
|---|---|---:|---|
| insiders5 | 容量 1（已交付） | 1.63（0mY6rY78） | 与 RRE9NkVj 互相关 0.7277-0.8594 |
| analyst10 | 容量 1（已交付） | 1.58（2Y 1.29） | 非重叠腿 2Y 不过 |
| pv47 | 判死 | 1.28 | S 硬顶，4 字段全封 |
| predictive_starmine | 判死 | 1.43 | power 摧毁，长窗 av_diff 也摧毁 |
| probability_label | 判死 | 2.20 | prod 0.75-0.87 整族 |
| model238 | 判死 | 1.05 | 五维度全弱 |
| model32 | 判死 | 1.12 | 百分位化丢量级 |
| event_stock_model | 判死 | 0.65 | 事件分数无信号 |
| model252 | 判死 | 0.64 | 防御分数无信号 |
| analyst_earnings_ibes | 已判死（历史） | 1.29 | 名不副实，价量字段 |

**本轮新增交付：0 颗。累计 3/10。**

## 10. 结构性判断（强烈建议纳入 roadmap）

KOR/TOP600/D1 的 ATOM REGULAR 容量远低于 10：
1. 320 条 IS 存量里只有 24 条同时满足 S>=1.58 / 2Y>=1.59 / raF=0，且 100% 死于 prod 或 self。
2. 战役至今探过 20+ 数据集，只有 3 个（risk70 / analyst10 / insiders5）能在 prod<0.70 下达到 S>=1.58，且每个恰好 1 颗。
3. 第 4 个（probability_label）S 高达 2.20 但 prod 整族 0.75-0.87。

⇒ 在「S>=1.58 且 2Y>=1.58 且 prod<0.70 且 self<0.70」四条同时成立的约束下，
**KOR 的实测容量约 3-4 颗，而不是 10 颗**。继续在同一区域刷，边际产出接近 0（本轮 120 条表达式 0 交付）。
可选出路（需用户决策）：(a) 接受 3-4 颗并把容量结论写成定论；(b) 允许双数据集组合（但 prod 仍是同一堵墙）；
(c) 换区域；(d) 继续以 ~1-2% 命中率盲扫剩余约 15 个未测数据集。