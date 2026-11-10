# GBR D1 fundamental6 挖掘经验（唯一量产线）

范围：2026-10-30。GBR/TOP700/D1 的 `fnd6_<科目> / cap` 跨量纲族。本文件只记录**已实测**的
13 条 S≥1.58 候选与 3 条 prod 实测值；不外推为 fundamental6 全数据集结论（该集
`alphaCount = 11550`、平台标记 `value_score = 1`，属重度拥挤集）。

数据集画像（DB `datasets` 表实读，id=368）：category `FUNDAMENTAL`、`field_count 342`、
`coverage 0.5`、`alpha_count 11550`、`value_score 1`、`pyramid_multiplier 1.5`、`delay 1`、
`tier STANDARD`。

## ★ 核心结论：`X / cap` 与裸 `X / Y` 是两种不同的东西

`registry_empirical` 的 `GBR-FUNDAMENTAL6-CEILING`（2026-09-12 判死）证据是
**33 条同量纲会计比率**（`akLevrVw` = `oancf-oiadp/atq`、`ts_zscore(atq/revt,66)`），
最强仅 `sharpe 0.37 / 2Y 1.08 / rn 0.33`，且 `rn_range -0.25 ~ -0.73` 说明裸
`rank/group_rank(fnd6_*_atq/revt)` 全是规模因子暴露。

2026-10-30 新增的 `X / cap` 跨量纲形式**从未被那条判死覆盖** —— 它的真实变量是**分母**
（`cap` 把会计科目转成「每单位市值的会计含量」），不是设置档。⇒ 判死范围已收窄为
「同量纲 `X/Y` 会计比率」，`X/cap` 形式放行（payload 内 `scope_correction_20261030`）。

## 骨料与设置档

主骨架（论坛 `44089095804439` 基本面 Δ 因子族模板的本区落地）：

```
rank(ts_quantile(ts_av_diff(divide(fnd6_<科目>, cap), 252), 84, driver=gaussian))
```

族级设置档（**全 13 条共用**）：`INDUSTRY` 中性化 + `decay 10` + `truncation 0.05`
+ `nanHandling OFF` + `maxTrade OFF`，universe `TOP700`，delay 1。

## 已测证据（13 条，平台 `failed_ra_count = 0`）

| Alpha | 科目 / 方向 | S | F | TO | 2Y | SUB | prod |
|---|---|---:|---:|---:|---:|---:|---:|
| rKRkL9QE | `capxy/cap`，`rank` | 2.21 | 2.05 | 8.33% | 2.51 | 1.77 | **0.6783** |
| QPveQvOg | `capxy/cap`，二阶 `ts_av_diff` | 2.06 | 1.78 | 7.49% | 2.47 | 1.68 | 未测 ★ |
| N1NM5WK8 | `capxy/cap`，换 `group_rank(·,industry)` | 2.05 | 1.80 | 8.98% | 2.26 | 1.68 | **0.9651 ⛔** |
| P0oerpjp | `capxy/cap`，W168/Q56 | 1.98 | 1.70 | 8.26% | 2.10 | 1.70 | 未测 ★ |
| 0mYoANkv | `cap/newa2_re`，反向 | 1.89 | 1.54 | 11.66% | 2.08 | 1.12 | **0.6932** |
| RREXA1qn | `cptnewq_atq/cap`，`subindustry` | 1.77 | 1.44 | 11.08% | 1.55 | 1.20 | 未测 ⚠ |
| 6XdxzNb5 | `newa2_re/cap` | 1.75 | 1.40 | 11.67% | 2.22 | 1.27 | 未测 ★ |
| 0mYo9Ok1 | `gpy/cap`，W168/Q56 | 1.73 | 1.39 | 8.41% | 1.47 | 1.55 | 未测 ★ |
| WjOkLGWx | `newq_cheq/cap`，`subindustry` | 1.72 | 1.26 | 9.31% | 2.09 | 0.94 | **0.6577** |
| kqNRXm5k | `capxy/cap`，`ts_zscore` 替 `ts_av_diff` | 1.70 | 1.33 | 7.98% | 2.02 | 1.52 | 未测 ⚠ |
| 88RAnmAX | `cap/ewq_teqq`，反向 | 1.67 | 1.40 | 12.26% | 1.89 | 1.06 | 未测 ⚠ |
| P0oeqZap | `capxy/cap`，`ts_delta` 替 `ts_av_diff` | 1.64 | 1.32 | 11.21% | 1.32 | 1.15 | 未测 ⚠ |
| 9qxoa3mx | `cap/cptnewq_ceqq`，反向 | 1.59 | 1.35 | 12.25% | 1.89 | 1.00 | 未测 ⚠ |

标注含义：★ = 换财务科目、值得投 prod 时隙；⚠ = 与已测三条同科目或只换外层，**先算
互相关再决定**，不直接烧 prod。

## ★ 一鱼两塔：`divide(F, cap)` 天生同时点 PV + FUNDAMENTAL

平台 `is.checks[MATCHES_PYRAMID]` 实读（`alpha_pyramids` 表）：

| Alpha | effective | towers | 倍率和 |
|---|---:|---|---:|
| rKRkL9QE / WjOkLGWx / 0mYoANkv | **2** | `GBR/D1/PV ×1.4` + `GBR/D1/FUNDAMENTAL ×1.6` | **3.0** |

GBR D1 当时塔位（`get_pyramid_alphas` 实读）：model 5 ✅ / analyst 3 ✅ / **pv 1** /
other 1 / **fundamental 0** / sentiment 0 / 其余 10 塔 0。
⇒ 提交任意一条该族候选可同时把 PV 与 FUNDAMENTAL 从「未点亮/未满」推进一格，
是当时**唯一**能补 FUNDAMENTAL 的路径。

`X/cap` 为什么归 PV：分母 `cap` 是价格量，分子是会计量 ⇒ 信号随市值/价格变动，
平台据此判定其含 PV 属性。这也是「不可从 `dataset_id` 推断塔位」的典型反例。

## 后续边界（薄余量扩招纪律）

- **prod 余量只有 0.007 ~ 0.042**（0.6783 / 0.6577 / 0.6932 对阈值 0.70）⇒ 这是**薄余量族**，
  不是安全族。任何新候选都要当场 `check_correlation(refresh=True)` 终验，不得引用旧值。
- **扩招必须换财务科目，不许换窗口**：同科目只改 `ts_av_diff` 的 W/Q 是伪多样性
  （`kqNRXm5k` 与 `rKRkL9QE` 同字段同窗口只换外层 Z 统计量）。
- **`N1NM5WK8` 不投 prod 时隙**：它只把 `rank` 换成 `group_rank(·,industry)`，在
  `INDUSTRY` 中性化下等价于再中性化一次，实测 prod **0.9651** ⇒ 换分组轴在这族上是
  自锁，不是降相关杠杆。
- `fnd6_` 字段池余量充足（2233 个 `fnd6_*` 字段），但**只有带量纲差异的分母**
  （`cap` / `ts_mean(cap,252)` 之外的市值类量）才构成新机制；`leAxRdb8`
  （分母 `ts_mean(cap,252)`）实测已撞墙，不再重试。
- 后续若要继续，优先顺序：①`6XdxzNb5`（`newa2_re`，与 capxy 不同会计科目）
  ②`0mYo9Ok1`（`gpy`）③`P0oerpjp`（同科目换窗口，最后）。
- 判死口径提醒：本地 `alphas` 表把该族记成 `dataset_id = 291`（真实 fundamental6 是
  **368**）、`region_id = 7`（会混 EUR）⇒ **不能按本地 `dataset_id` 归集这族候选**，
  必须按表达式里的字段名归集。

## 证据落点

- 平台塔位权威：`mcp__wq-brain-http__get_pyramid_alphas` + `get_pyramid_multipliers`
- 本地塔位指纹：`alpha_pyramids` 表（`tools/backfill_alpha_pyramids.py --region GBR --source ready`）
- 判死条目：`registry_empirical` → `GBR-FUNDAMENTAL6-CEILING`（含 `scope_correction_20261030`）
- 族弹药库全表：`Claude/skills/wq-brain-ra-gbr/references/fundamental.md`
- 论坛模板来源：`44089095804439`（GBR 基本面 Δ 因子族，6 赞）


---

## 2026-11-08 增补：设置杠杆 + 族容量实测

### ★ 突破 2Y 闸的设置杠杆：`SUBINDUSTRY` 替 `INDUSTRY`

上表 13 条用的族级档是 `INDUSTRY + decay 10 + truncation 0.05 + nanHandling OFF`。本轮在
**同一骨架、同一字段**上只改中性化与 decay，2Y 闸从「压线不过」直接变成「大幅通过」：

| 科目 | 设置档 | S | F | TO | 2Y | fails |
|---|---|---:|---:|---:|---:|---:|
| `newa2_ppegt` | INDUSTRY / d10 / t0.05 / nanOFF（原档） | 1.72 | 1.48 | 10.4% | **1.58** | 1（2Y 压线） |
| `newa2_ppegt` | INDUSTRY / d4 / t0.08 / nanOFF | 1.72 | 1.34 | 15.7% | **1.46** | 1 |
| `newa2_ppegt` | **SUBINDUSTRY / d10 / t0.05** | 1.95 | 1.77 | 10.9% | **2.21** | **0** |
| `newa2_ppegt` | **SUBINDUSTRY / d4 / t0.08** | 1.91 | 1.51 | 16.5% | **2.16** | **0** |
| `txty` | INDUSTRY / d4 / t0.08 | 1.70 | 1.28 | 11.6% | 1.49 | 1 |
| `txty` | SUBINDUSTRY / d10 / t0.05 | 1.66 | 1.24 | 8.0% | 1.52 | 1 |
| `txty` | SUBINDUSTRY / d4 / t0.08 | 1.68 | 1.28 | 12.1% | 1.54 | 1 |

**结论**：该族的 2Y 闸是**设置敏感**的，不是字段决定的。`SUBINDUSTRY` 把 2Y 抬升 0.4–0.6；
`txty` 无论怎么换档都停在 1.49–1.54 ⇒ **换档救不了机制本身弱的字段，只救「机制对但被行业共同因子遮蔽」的字段**。
扩招时的标准动作：先用原档跑一遍科目筛掉机制弱的，再把通过的科目换成 `SUBINDUSTRY` 复跑一遍破 2Y。

### 本轮新增 5 个全闸科目（fl = failed_ra_count = 0）

骨架统一为 `rank(ts_quantile(ts_av_diff(divide(fnd6_<科目>, cap), 252), 84, driver=gaussian))`：

| Alpha | 科目 | 经济机制 | 设置档 | S | F | TO | 2Y |
|---|---|---|---|---:|---:|---:|---:|
| **A1V8dj2e** | `newa2_ppent` | 净固定资产扩张 | SUB/d4/t0.08 | **1.99** | 1.62 | 15.7% | **2.32** |
| **Xg9A6rGl** | `newa2_ppegt` | 毛固定资产扩张 | SUB/d4/t0.08 | 1.91 | 1.51 | 16.5% | 2.16 |
| **gJeVpvlO** | `newa2_ppegt` | 同上（d10 档） | SUB/d10/t0.05 | 1.95 | 1.77 | 10.9% | 2.21 |
| **d5WrwkPj** | `capxy` | 资本开支强度 | SUB/d4/t0.08 | 1.85 | 1.56 | 13.2% | 2.04 |
| **pwdegovq** | `newq_rectq` | 应收账款堆积（盈余质量） | SUB/d6/t0.08 | **1.60** | 1.34 | 12.5% | **1.97** |
| 2rAokgMb | `newa2_xsga` | 销售管理费用率 | SUB/d4/t0.08, W60 | 1.63 | 1.18 | 17.3% | 2.05 |
| kqN65Azd | `newa2_xsga` | 同上（d3 档） | SUB/d3/t0.08 | 1.59 | 1.14 | 17.4% | 2.15 |

近失（fl=1，只差一项）：`xint` S1.58–1.60 但 2Y 1.48–1.56；`xsga` 原档 S1.57（差 0.01）；`rectq` d8 S1.59 但 2Y 1.55。

### ★★ 族容量实测：`X/cap` 是**一个机制**，0.5 口径下最多进 2 颗

把 9 个全闸/近全闸候选一起跑互相关（`compute_mutual_correlation(threshold=0.5, years=4)`），
超线 29 对，平台精确解 `max_mutually_below_subset = [A1V8dj2e, QPveQvOg]`，**size 恰为 2**。

集群结构（≥0.5 连边）：

| 集群 | 成员 | 内部相关 |
|---|---|---:|
| 权益/估值分母群 | `88RAnmAX`(teqq) ↔ `9qxoa3mx`(ceqq) | 0.9584 |
| 固定资产群 | `A1V8dj2e`(ppent) ↔ `Xg9A6rGl`(ppegt) | 0.9347 |
| 营收群 | `0mYoANkv`(newa2_re) ↔ `6XdxzNb5` | 0.8903 |
| 资本开支群 | `rKRkL9QE` ↔ `QPveQvOg` ↔ `d5WrwkPj` | 0.87 / 0.86 |
| 费用群 | `2rAokgMb` ↔ `kqN65Azd`(xsga 两窗口) | 0.9777 |

跨集群普遍 0.5–0.78（如 xsga × ppent 0.776、xsga × rectq 0.759）⇒ **换财务科目带来的只是
「同一资产增长/应计因子」的不同投影，不是新机制**。`QPveQvOg`（capxy 二阶 `ts_av_diff`）
是唯一与几乎所有成员都 <0.5 的枢纽（与 xsga 0.5143、与 ppent 未超线）。

**扩招纪律更新**：该族每轮只能贡献 **2 颗**；想靠它凑到 3 颗以上必须换机制族，不是换科目。

### 已判死：`X/cap` 的**水平**（估值）形态

同一分母、把 `ts_av_diff` 换成裸水平（8 条结构互异探针）：

| 表达式 | S | F | 2Y |
|---|---:|---:|---:|
| `rank(divide(fnd6_newa2_pi, cap))`（E/P） | 0.76 | 0.42 | 1.16 |
| `rank(divide(fnd6_newq_lseq, cap))`（B/P） | 0.38 | 0.17 | 1.25 |
| `rank(divide(fnd6_newa2_oancf, cap))`（CF/P） | 0.82 | 0.54 | 2.10 |
| `rank(divide(fnd6_newa2_revt, cap))`（S/P） | 0.56 | 0.30 | 1.56 |
| `group_rank(divide(fnd6_newa2_pi, cap), sector)` | 0.79 | 0.44 | 1.10 |
| `ts_zscore(divide(fnd6_newa2_pi, cap), 1008)` | 0.80 | 0.48 | 1.27 |
| `rank(divide(fnd6_newa2_seq, cap))` | 0.56 | 0.29 | 1.50 |
| `rank(divide(fnd6_newq_cheq, cap))` | 0.50 | 0.23 | 0.96 |

最强 S 0.82、TO 全部 ≤4.3% ⇒ **估值水平形态在 GBR TOP700 无预测力**（对应经典 value 因子在本区失效）。
该族的全部强度来自 **Δ（同比变化）**，不是水平。这条与上表一起构成 `X/cap` 的完整边界：
**Δ 形态有效、水平形态无效；Δ 形态内部只有一个机制、容量 2 颗。**


### ★★ 2026-11-08 傍晚边界修正：`cap` 属 `pv1` ⇒ 本族实为 PV×FUNDAMENTAL 双塔；换 RISK 分母可复现但只值 1 席

**① `cap` 的归属实读（`get_datafields(dataset_id=pv1)`）**：`cap` = "Daily market capitalization (in millions)"，
与 `close/volume/returns/adv20/sharesout/vwap/market` 同属 **pv1（23 字段）**。⇒ 本族 **不是** fundamental6 单塔
ATOM，而是 **PV × FUNDAMENTAL 两腿**（与本文件上文的「一鱼两塔」自洽）。组腿判据须按此登记：
本轮 GBR 请求允许 PV/MODEL/OTHER「与其它 category 组腿」并计入 ≤5 配额，故合法；但若换到把 FUNDAMENTAL
也并入禁混集合的战役（如 EUR 2026-11-03 口径），本族**整族不可用**。

**② 分母不是可选件，它就是收益本体 —— 10 条「纯 fnd6 内部比值」全灭（决定性反证）**

把 `cap` 换成 `fnd6_cptnewq_atq`（报表总资产，同量纲、纯 fnd6 单数据集 ATOM），10 个结构互异模板实测：

| 机制 | 表达式（骨架） | S | F | TO | 2Y | fail |
|---|---|---:|---:|---:|---:|---:|
| 资本开支强度 | `rank(ts_quantile(ts_av_diff(divide(fnd6_capxy, fnd6_cptnewq_atq),252),84,gaussian))` | **0.74** | 0.37 | 4.6% | 0.64 | 3 |
| 应计（Sloan） | `reverse(group_rank(ts_backfill(divide(subtract(fnd6_iby,fnd6_oancfy),fnd6_cptnewq_atq),132),sector))` | 0.60 | 0.29 | 2.8% | 1.05 | 3 |
| 资产周转率 | `ts_rank(ts_backfill(divide(fnd6_newa2_revt,fnd6_cptnewq_atq),66),504)` | 0.33 | 0.10 | 3.2% | 0.46 | 3 |
| 杠杆下降 | `reverse(rank(ts_av_diff(divide(fnd6_cptnewq_dlttq,fnd6_cptnewq_atq),252)))` | 0.22 | 0.06 | 3.2% | −0.21 | 3 |
| ROE 变化 | `rank(ts_av_diff(divide(fnd6_iby,fnd6_newq_seqq),252))` | 0.21 | 0.06 | 3.8% | 0.60 | 4 |
| 净固定资产强度 | `rank(ts_quantile(ts_av_diff(divide(fnd6_newa2_ppent,fnd6_cptnewq_atq),252),84,gaussian))` | 0.15 | 0.03 | 5.0% | 0.23 | 4 |
| ROA 水平 | `group_rank(ts_backfill(divide(fnd6_newa2_oiadp,fnd6_cptnewq_atq),66),sector)` | 0.14 | 0.03 | 2.0% | −1.00 | 3 |
| ROA 动量 | `group_neutralize(rank(ts_delta(divide(fnd6_newa2_oiadp,fnd6_cptnewq_atq),252)),sector)` | 0.13 | 0.03 | 3.8% | −0.46 | 4 |
| 营业利润率 | `group_rank(ts_zscore(ts_backfill(divide(fnd6_newa2_oiadp,fnd6_newa2_revt),66),504),industry)` | −0.15 | −0.03 | 2.6% | −0.63 | 3 |
| 权益比率 | `group_rank(ts_backfill(divide(fnd6_newa2_seq,fnd6_cptnewq_atq),66),subindustry)` | −0.43 | −0.17 | 1.8% | −0.33 | 4 |

**长仓 200–474 只、覆盖不薄**，所以这不是覆盖率问题而是机制问题：**fnd6 的会计内容本身在 GBR TOP700 无预测力；
本族的全部强度来自「每单位市值的会计含量」这个价值/投资-to-price 比**。上节「同量纲 X/Y 判死」由此
从 33 条扩证到 **43 条、覆盖盈利/效率/偿债/应计/投资 5 类机制**。

**③ 合法替代分母：`alternative_market_cap_usd`（dataset `risk88`，RISK 类，coverage 1.0）**

`risk88` 全数据集**只有 1 个字段** `alternative_market_cap_usd`（"Market capitalization of each stock expressed in USD"，
MATRIX，cov 1.0，ac 567）。用它替换 `cap` 后机制完整复现，且组腿变成 **FUNDAMENTAL × RISK**（避开 PV）：

| alpha | 表达式差异 | S | F | TO | 2Y | SUB | fail |
|---|---|---:|---:|---:|---:|---:|---:|
| `d5Wr8mzw` | `fnd6_newa2_ppent / alternative_market_cap_usd` Δ | **1.99** | 1.57 | 16.55% | 2.08 | 1.47 | **0** |
| `LLMYb6z1` | `fnd6_capxy / alternative_market_cap_usd` Δ | 1.83 | 1.52 | 13.52% | 2.09 | 1.34 | **0** |
| `6XdLP10J` | `fnd6_newa2_xsga / alternative_market_cap_usd` Δ | 1.63 | 1.23 | 16.06% | 2.06 | 1.07 | **0** |
| `0mY2kdg2` | `fnd6_newq_rectq / alternative_market_cap_usd` Δ | 1.62 | 1.21 | 15.86% | 2.04 | 0.89 | **0** |
| `VkxbwEzM` | `fnd6_newa2_seq / alternative_market_cap_usd` **水平**（B/M） | 0.39 | 0.17 | 2.41% | 1.45 | 0.27 | 3 |

**⚠ 但这 4 条只值 1 席**：0.5 互相关矩阵实测彼此 **0.5729 / 0.6525 / 0.6616 / 0.7166 / 0.7768 / 0.7872**（六对全超线），
即 4 条构成一个全连通 >0.5 团 ⇒ 最大独立集 **1**。它们与既有 6 颗篮子的相关仅 **−0.07 ~ 0.21**（很干净，但进不去）。
⇒ **换分母只解决「合规」，不解决「容量」；`X/市值` 这一机制在 GBR 的容量硬上限仍是 2 席**（`cap` 版）/ 1 席（`altcap` 版）。

**④ 顺带判死：`sentiment7`（Wikipedia 页面浏览量，注意力因子）**

`snt7_views`(cov 0.5766) / `snt7_all_languages_views`(0.5819) 全 3 字段 VECTOR。5 个结构互异模板（abnormal attention /
YoY 变化 / 多语言 / 自历史分位 / 66d 正向）实测 S **−0.49 ~ 0.37**，TO 25%–53%，3 条挂 CONCENTRATED_WEIGHT
⇒ Da-Engelberg-Gao「注意力」机制在 GBR TOP700 不成立。**sentiment 塔除 sentiment27 外再添一个判死集。**
