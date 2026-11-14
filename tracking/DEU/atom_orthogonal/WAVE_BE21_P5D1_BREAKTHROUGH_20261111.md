# BE21 结论：_p5_d1 变体大幅提分，但被 I7 共享锁死相关性

## 一、八臂结果（sim CEkuA2v14xIaNqlpOj9QRK，complete=8 error=0）

骨架统一：`group_zscore(add(-group_rank(ts_delta(ts_backfill(vec_avg(F),132),220),sector), I7), market)`

| 臂 | 字段 | S | F | TO | longCount | sub | 2Y | 判定 |
|---|---|---:|---:|---:|---:|---:|---:|---|
| 1 | loan_rate_volatility（基础，对照） | 1.40 | 1.10 | 0.1143 | 125 | 0.72 | 2.45 | 基线 |
| **2** | **loan_rate_volatility_p5_d1** | **1.58** | **1.20** | 0.1445 | **148** | 0.73 | 2.37 | ✅ 全闸 |
| **4** | **mean_loan_rate_p5_d1** | **1.88** | **1.44** | 0.1664 | 146 | **0.85** | 2.38 | ✅ 全闸 |
| **5** | **max_loan_rate_p5_d1** | **1.91** | **1.57** | 0.1446 | 147 | **0.85** | **2.72** | ✅ 全闸（最强） |
| 7 | average_loan_duration_days_p5_d1 | 1.45 | 1.07 | 0.1373 | 148 | 0.75 | 1.54 | 差 S |
| 3 | loaned_market_value_usd_p5_d1 | 1.18 | 0.84 | 0.1152 | 148 | 0.27 | 1.58 | 弱 |
| 6 | loaned_share_count_p5_d1 | 1.20 | 0.86 | 0.1147 | 148 | 0.26 | 2.36 | 弱 |
| 8 | 双高覆盖腿组合 | 1.13 | 0.74 | 0.1308 | 151 | 0.36 | 2.07 | 弱 |

## 二、核心发现：_p5_d1 变体是免费增量面

| 对比 | 基础版 | _p5_d1 版 | 差异 |
|---|---|---|---|
| 覆盖率 | 0.653 | **0.783** | +0.130 |
| longCount（实测） | 125 | **148** | +23 |
| S（同骨架） | 1.40 | **1.58** | +0.18 |
| 更强字段的 S | — | **1.91**（max_loan_rate） | — |

**机制**：_p5_d1 = 前 5 日滚动至 D1 口径，覆盖率更高 ⇒ 更多股票进入组合 ⇒ longCount 125→148
⇒ 横截面信号更宽、更稳 ⇒ S 与 sub 同步提升。**这是零成本的增量面**（不需要新机制/新模板）。

## 三、但四颗高 S 候选全部被 I7 锁死相关性

对 9 件 + 4 新候选做 13 件互相关：

| 候选 | S | 与 9 件最大相关 | 对端 | 判定 |
|---|---:|---:|---|---|
| ZYaRM7Vj | 1.91 | **0.885** | qM7KxkQV | ❌ 冲突 |
| LLKPr7oe | 1.88 | **0.876** | qM7KxkQV | ❌ 冲突 |
| WjlE072P | 1.58 | **0.866** | qM7KxkQV | ❌ 冲突 |
| Grmqxlj5 | 1.45 | **0.850** | qM7KxkQV | ❌ 冲突 |

候选之间也相关 **0.834-0.949**。
原因：它们与 qM7KxkQV **共享同一个 I7 第二腿**（insd1_holdings ts_rank252），
高 S 来自「借券腿 × I7」这个组合，不是新机制。
⇒ `max_mutually_below_subset_size` 仍为 **9**，这四颗**不增加交付数量**。

## 四、由此推导的正确方向（BE22 已派）

强腿已确认存在（max_loan_rate_p5_d1 单独能撑到 1.91），瓶颈只是**共享 I7**。
⇒ 用这条强腿换一个**非 I7 的第二腿**，即可同时获得高分与低相关。

BE22 八臂（sim 14MDYi5iQ4AOai11arjhHoxN）：
1. max_loan_rate_p5_d1 × oth47 流量变化
2. max_loan_rate_p5_d1 × nws20 情绪
3. max_loan_rate_p5_d1 × inst25 集中度
4. max_loan_rate_p5_d1 × insd1_tradesignificance（避 holdings）
5. mean_loan_rate_p5_d1 × oth47
6. max_loan_rate_p5_d1 × mean_loan_rate_p5_d1（双强腿不同窗口）
7. max_loan_rate_p5_d1 × average_loan_duration_days_p5_d1
8. max_loan_rate_p5_d1 × oth47_rank