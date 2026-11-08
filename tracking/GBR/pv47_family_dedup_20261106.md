# GBR pv47 族去重清单与模板族划分（2026-11-06）

> GBR READY 池 31 条里有 15 条来自 `pv47_spret`（特质收益）派生。
> 全部为 **PV 塔单数据集 ATOM ⇒ 不受塔混配额约束**，是本池最有价值的产出点。
> 但 15 条里存在大量仅换分组轴/窗口的近重复，必须先去重再测 self，否则白耗平台配额。

## 近重复组（同表达式，仅换一个维度）

### 组 1：`group_neutralize` 轴四胞胎 + 一个无 neutralize 版

```
A1QW6xpE  1.74  group_rank(ts_decay_linear(group_neutralize(-ts_sum(pv47_spret, 5), industry), 22), industry)
58jb7JLn  1.72  group_rank(ts_decay_linear(group_neutralize(-ts_sum(pv47_spret, 5), market),   22), industry)
mLY32aZ1  1.72  group_rank(ts_decay_linear(group_neutralize(-ts_sum(pv47_spret, 5), exchange), 22), industry)
P0MWqZ1E  1.72  group_rank(ts_decay_linear(group_neutralize(-ts_sum(pv47_spret, 5), country),  22), industry)
RRA3qVro  1.72  group_rank(ts_decay_linear(group_neutralize(-ts_sum(pv47_spret, 5), currency), 22), industry)
58jbVxXz  1.71  group_rank(ts_decay_linear(-ts_sum(pv47_spret, 5), 22), sector)      ← 无 neutralize
```

⇒ 六条本质是**同一个信号**（5 日特质收益反转 + 22 日线性衰减 + 双重分组排名），
差异只在 `group_neutralize` 的分组键。**只保留 S 最高的 `A1QW6xpE`(1.74) 一条**，其余五条弃用。

## 去重后的 11 个结构互异模板族

| 族 | alpha | S | 表达式骨架 | 差异维度 |
|---|---|---:|---|---|
| A | `QPYJZ7bG` | 1.97 | `-rank(ts_quantile(ts_backfill(ts_target_tvr_decay(ts_sum(spret,5), tvr), 504), 504))` | 分位数变换 + 换手目标 |
| B | `vROqwj2z` | 1.93 | `-rank(ts_quantile(ts_zscore(ts_sum(spret,11),504),504))` | 11 日 + 504 zscore 双层归一 |
| C | `1Yj9e7EJ` | 1.83 | `-rank(ts_quantile(ts_target_tvr_decay(ts_decay_linear(ts_sum(spret,5),22),tvr),504))` | 先衰减再换手约束 |
| D | `mLY3L6gX` | 1.79 | `-rank(ts_quantile(ts_target_tvr_decay(ts_zscore(ts_sum(spret,11),252),tvr),504))` | 252 中窗 + 换手目标 |
| E | `A1QW6xpE` | 1.74 | `group_rank(ts_decay_linear(group_neutralize(-ts_sum(spret,5),industry),22),industry)` | 中性化后二次分组 |
| F | `LLZ5ewlM` | 1.73 | `-ts_decay_linear(rank(ts_quantile(ts_sum(pv47_for_statssimple_only_spret,22),504)),5)` | 换用 `_for_statssimple_only_` 字段变体 |
| G | `vRO8QQgb` | 1.69 | `-rank(ts_rank(ts_target_tvr_decay(ts_sum(spret,11),tvr=0.13),252))` | ts_rank 替代 ts_quantile |
| H | `wpb96AJp` | 1.69 | `-ts_decay_linear(rank(ts_zscore(ts_sum(spret,22),252)),5)` | 22 日累加 + 衰减（最简骨架） |
| I | `d51Kq6lE` | 1.65 | `-ts_decay_linear(group_rank(ts_quantile(ts_sum(spret,22),252), bucket(rank(ts_std_dev(spret,66)),range="0,1,0.1")),5)` | 波动率分桶内排名 |
| J | `58gjR165` | 1.62 | `-ts_decay_linear(rank(divide(ts_sum(spret,22), ts_std_dev(spret,66))),5)` | 夏普比式（累加/波动） |
| K | `QPYJZ7bG` 族 | — | 见 A | — |

⇒ **10 个结构互异族**（A–J），满足「模板库 ≥10 个」硬要求。
差异落在：分位/秩变换类型、归一化层数（单层 zscore / 双层 zscore+zscore / zscore+quantile）、
换手约束位置（内层/外层）、分组轴（industry/sector/bucket）、字段变体（spret vs _for_statssimple_only_spret）、
矩操作（累加直除 vs 累加/波动）。

## 测试顺序（self 免费，prod 单并发按 S 降序）

1. 先测 A / B / C / D / E 五族 self（覆盖 S 1.74–1.97 区间，是产出概率最高的一段）
2. self 过线的按 S 降序排 prod 单队列
3. 注意：`A1QW6xpE` 已与 `58jb7JLn`/`mLY32aZ1`/`P0MWqZ1E`/`RRA3qVro` 互斥，测 A1QW6xpE 后其余不必再测

## 已确认的 GBR 全绿（5 颗，来自 `get_submit_ready` 自带 self/prod 字段）

| alpha | S | self | prod | 族 |
|---|---:|---:|---:|---|
| `d51O1kOX` | 1.97 | 0.1129 | 0.6793 | analyst7 `est_12m_pre_raisednum` |
| `blORMJwm` | 1.91 | 0.0623 | 0.6950 | analyst7 4wk 变体 |
| `3qV7Q2dO` | 1.77 | 0.3669 | 0.6596 | starmine `price_ratio_fy2_revenue_3` |
| `RR62bMje` | 1.67 | 0.6066 | 0.6573 | starmine `ep_yield_pct_smest_f12m` |
| `mL68wNOK` | 1.63 | 0.4979 | 0.6608 | model28 structural leverage |

⚠️ `blORMJwm` prod 0.6950 距红线仅 **0.005**，提交瞬间平台重算有顶过 0.7 的风险。

## ★★★ 实测结论：pv47 族 6 条 self 全过，但彼此互相关 0.72–0.95 ⇒ 净产出只有 1 颗

对去重后的 6 个互异族逐条 `check_self_correlation`（全部 <0.7，看似都可提交）：

| alpha | S | self |
|---|---:|---:|
| `QPYJZ7bG` | 1.97 | 0.6544 |
| `vROqwj2z` | 1.93 | 0.4551 |
| `1Yj9e7EJ` | 1.83 | 0.6123 |
| `mLY3L6gX` | 1.79 | 0.5861 |
| `A1QW6xpE` | 1.74 | 0.5974 |
| `LLZ5ewlM` | 1.73 | 0.6710 |

但 `compute_mutual_correlation` 揭示它们**互相之间**高度重合：

| 对 | 相关 |
|---|---:|
| `QPYJZ7bG` × `1Yj9e7EJ` | **0.9456** |
| `1Yj9e7EJ` × `mLY3L6gX` | 0.9270 |
| `QPYJZ7bG` × `LLZ5ewlM` | 0.9113 |
| `1Yj9e7EJ` × `LLZ5ewlM` | 0.9077 |
| `QPYJZ7bG` × `mLY3L6gX` | 0.8885 |
| `1Yj9e7EJ` × `A1QW6xpE` | 0.8781 |
| （其余 9 对均在 0.72–0.87） | |

**0.7 阈值下的最大互不冲突子集 = 1 颗（`QPYJZ7bG`）**。

### ⇒ 判据（跨区通用，写进方法论）

**`check_self_correlation` 只回答「这颗与已提交池冲不冲突」，不回答「这批候选彼此冲不冲突」。**
同族候选必须再跑一次 `compute_mutual_correlation`，否则会把「6 条 self 全过」误读成「6 颗可提交」。

为什么 IND 池没这个问题：IND 的 18 颗骨架相同但**信号源来自 8 个不同数据集**
（institutions6 / earnings3 / sentiment21 / analyst44 / imbalance5 / macro63 / insd1 / other532），
按 0.7 阈值只互相排除 1 颗（`vRO9nG3w` ↔ `E5VNe67L` 0.711）。
而 GBR pv47 族是**同一个字段 `pv47_spret` 的 11 种变换**⇒ 经济含义同源，互相关必然爆表。

**推论**：一个数据集的 `alphaCount` 高不代表已挖尽，但**同一字段的变换族存在硬上限**，
通常是 1–2 颗。判断一个池的「真实可提交数」必须用互相关矩阵，不能用 self 通过条数。

## analyst47 族：8 条只有 1 条过 self

| alpha | S | self | 判定 |
|---|---:|---:|---|
| `Vkd93wOw` | 2.13 | **0.6433** | ✅ 过，待 prod |
| `vROqOYkv` | 2.16 | 0.99999 | ✗ 完全镜像 |
| `wp9m9MW1` | 2.14 | **0.9990** | ✗ 判死（**订正**：此前只知 prod 0.548，误以为可用） |
| `O0JYJ67b` | 2.04 | 0.9783 | ✗ |
| `RRA3AnPg` | 2.02 | 0.8371 | ✗ |
| `e76p6oWd` | 2.02 | 0.8370 | ✗ |
| `zqrMr1LG` | 2.02 | 0.8370 | ✗ |
| `WjLqPzpQ` | 2.02 | 0.8372 | ✗ 判死（**订正**：prod 0.6801 但 self 0.837） |

⇒ **`prod < 0.7` 完全不能推出可提交**：`wp9m9MW1` prod 0.548、`WjLqPzpQ` prod 0.6801 都过，
但 self 分别是 0.9990 / 0.8372，双双拦下。

## GBR 池最终账

| 类别 | 数量 | 明细 |
|---|---:|---|
| 已全绿（可直接提交） | **5** | `d51O1kOX` / `blORMJwm` / `3qV7Q2dO` / `RR62bMje` / `mL68wNOK` |
| 待 prod | **2** | `QPYJZ7bG`(1.97) / `Vkd93wOw`(2.13) |
| pv47 族其余 5 条 | 0 | 被互相关 0.72–0.95 全部排除 |
| analyst47 族其余 7 条 | 0 | 被 self 0.84–1.00 全部拦下 |
| 剩余未测 | 3 | `P0gxk2dx`(1.67, techindi_model) / `wpbRKA6l`(1.69, starmine) / 4 条 pv47 尾族 |

⇒ GBR 31 条的**真实上限约 7 颗**（已得 5 颗 + 待测 2 颗），不是「31 条全可交」。

