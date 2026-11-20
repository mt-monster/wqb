# 截图 11 颗 alpha 提交价值评估（2026-11-16 19:2x）

> 用户截图 11 个 id，要求并入全量清单一起评估。3 个 id 因截图字符歧义读错（9q1av→9qlav、78YaQpNl→78YaQPnL、ZYQ1161n→ZYQ116ln），用平台 404 + 本地 DB 前缀匹配纠正后全部命中。
> **结论：这 11 颗是同一个 KOR「价量/概率腿 − insd5 内部人腿」双腿差分矩阵族，全 Ra=0、全 UNSUBMITTED、prod 全有当天权威缓存。族内高度抱团，但无一与今日已提交 Jj85OR7e 封死。值得提交 5 颗（互不冲突），其中 1 颗 prod 贴线。只挖不提交。**

## 0 全族结构（关键：同族抱团）

所有 11 颗 = `subtract(腿A, 腿B)`，共享腿B = insd5 内部人波动离散度 `group_rank(ts_mean(vec_stddev(insd5_vol_* ), 44/55), sector)`；腿A 换不同价量相关（corr_bid/ask/high price×volume）或概率分位字段。
- **塔**：8 颗混 `KOR/INSIDERS(1.2) + PV(1.4)/ANALYST(1.6)/OTHER(1.6)`，effective=2（短板 1.2）；1 颗纯 PV(1.4)；1 颗 INSIDERS+ANALYST。
- **KOR 当季塔基线**：INSIDERS=2、ANALYST=4(亮)、PV=2、OTHER=1 ⇒ 这些件的 insiders 腿 2→3 **可点亮**（若交 insiders 腿载体）。

## 1 互相关矩阵（决定性）

`compute_mutual_correlation`（1023 日收益点，threshold 0.7）：

**与已提交 `Jj85OR7e` 全部 <0.7**（最高 QP02jR9w .6118）⇒ **无提交孪生封死**。

族内 ≥0.7 的高相关对（互斥，不能同时交）：
- wpoJRxW5 ↔ A1xOPqGE **.9930**（概率 4/5 vs 1/2 分位，几乎同一腿）
- ZYa2xVKY ↔ N1Pg6ERg **.9764**、N1Pg6ERg ↔ QP02J90p **.9702**、ZYa2xVKY ↔ QP02J90p **.9677**（corr 族三兄弟，同腿 B）
- QP02jR9w ↔ QP02J90p .8451；78YaAnYZ ↔ 78YaQPnL .8215；wpoJRxW5 ↔ 9qlav7E2 .8143

**最大互不冲突集 = 5 颗未提交**（`max_mutually_below_subset` 去掉已交 Jj85OR7e 后）：
`78LpqZYQ` / `wpoJRxW5` / `ZYa2xVKY` / `78YaAnYZ` / `ZYQ116ln`

## 2 排序清单（全 11 颗，逐颗全维度）

判序：prod 硬闸 → self → 族内互斥 → 塔边际 → 六维 → 指标。
prod/self 均为当天权威 `alpha_corr_cache`（check_correlation，4.9h 内，48h 保鲜）。

### A 档：值得提交（互不冲突，prod 余量足）

| # | id | S/F/2Y/sub | prod(时龄) | self | 塔六元组（席位｜倍率｜当季→交后｜点亮｜边际） | ops/fields | 六维 | 判据 |
|---:|---|---|---|---|---|---|---|---|
| 1 | **wpoJRxW5** | 2.04/1.15/2.55/1.95 | **.504**(4.8h) | .4399 | INSIDERS 1.2 + OTHER 1.6，短板 **1.2**｜INSIDERS 2→3 **点亮**｜+1 | 5/3 | T1+.001/T2+.003/T3flat/**T4+1新字段** | prod 余量最大(.196)、T4 新字段、塔可点亮；与 A1xOPqGE 互斥（取本件） |
| 2 | **ZYa2xVKY** | 1.71/1.13/2.77/1.51 | .5991(0.2h) | .1201 | INSIDERS 1.2 + PV 1.4，短板 **1.2**｜INSIDERS 2→3 点亮｜+1 | 4/2 | T1−.0016/T2+.0004/T3flat/T4flat | self 最低、prod 新鲜；与 N1Pg6ERg/QP02J90p 互斥（取本件） |
| 3 | **78YaAnYZ** | 1.77/1.16/2.11/1.58 | .5797(3.3h) | .1319 | INSIDERS 1.2 + PV 1.4，短板 1.2｜INSIDERS 2→3 点亮｜+1 | 4/2 | T1−.0016/T2+.0004/T3flat/**T4+1** | T4 新字段 corr_bid_price_with_bid_size；与 78YaQPnL 互斥 |

### B 档：可交但 prod 贴线 / 塔重复

| # | id | S/F/2Y/sub | prod | self | 塔 | ops/fields | 判据 |
|---:|---|---|---|---|---|---|---|
| 4 | **ZYQ116ln** | 1.86/1.10/1.80/1.55 | **.6981**(4.9h) | .2129 | 纯 PV 1.4（PV=2 未亮）｜边际 0 | 3/1 | prod 余量仅 .0019，贴线高危；T1/T2 双降（最省算子）但塔边际 0 ⇒ 不占配额 |
| 5 | **78LpqZYQ** | 2.12/**2.09**/2.59/2.30 | **.6970**(4.9h) | .477 | INSIDERS 1.2 + ANALYST 1.6(亮)，短板 1.2｜INSIDERS 2→3 点亮｜+1 | 5/2 | **F 2.09 全族最强**、margin 28.3bp、TO 8.6%；但 prod 余量 .003 贴线，与 wpoJRxW5 同族可点亮同席（互斥由塔席位决定） |

> `78LpqZYQ` 与 `wpoJRxW5` 互相关仅 .2981（不互斥），但**同抢 KOR/INSIDERS 2→3 这一席**——只能点亮一次，优先 prod 余量大的 wpoJRxW5。若追求指标可选 78LpqZYQ 但 prod 贴线需当刻 refresh。

### C 档：族内孪生（与上表互斥，二选一后不交）

| id | S/F | prod | 与谁互斥（ρ） | 判定 |
|---|---|---|---|---|
| A1xOPqGE | 1.92/1.04 | .5112 | wpoJRxW5 (.993) | 孪生，留 wpoJRxW5 |
| N1Pg6ERg | 1.72/1.15 | .6128 | ZYa2xVKY (.976) | 孪生，留 ZYa2xVKY |
| QP02J90p | 1.84/1.28 | .6157 | ZYa2xVKY (.968) | 孪生，留 ZYa2xVKY |
| QP02jR9w | 1.93/1.35 | .6115 | QP02J90p (.845)、N1Pg6ERg (.814) | 同簇，2Y 3.23 强但与 ZYa2xVKY .811 互斥 |
| 78YaQPnL | 1.73/1.12 | .5745 | 78YaAnYZ (.8215) | 孪生，留 78YaAnYZ；且有 CLUSTER_TEST WARNING(0.97<1) |
| 9qlav7E2 | 1.97/1.08 | .5274 | wpoJRxW5 (.814)、A1xOPqGE (.807) | 同概率腿簇，prod 低但与 A 档 #1 互斥 |

## 3 建议（并入全量清单）

- 这 11 颗里**最多交 3 颗不冲突且塔可点亮**：`wpoJRxW5`（#1，prod .504 最优）+ `ZYa2xVKY`（#2，self 最低）+ `78YaAnYZ`（#3，T4 新字段）。三颗互相关分别 .4845 / .4614 / .6781，全 <0.7。
- 但三颗**同抢 KOR/INSIDERS 2→3 一席**——塔只能点亮一次。真正最优是**只交 1 颗**（`wpoJRxW5`，prod 余量最大），其余因塔边际重复降为备选。
- `78LpqZYQ` 指标最强（F2.09）但 prod .697 贴线，且与 wpoJRxW5 同席，仅在追求单颗极致指标时替换。
- 全部与已提交 Jj85OR7e 解耦（<0.7），无封死风险。

## 4 提交前必做（未做，本轮零提交）

① prod 虽 48h 内可信，但贴线件（78LpqZYQ/ZYQ116ln）当刻 refresh；② 稳健审计（11 颗均无 robustness 台账）③ 方案 D；④ 同席互相关已测（本报告 §1）；⑤ ET 配额（11-16 剩 2 席）。
