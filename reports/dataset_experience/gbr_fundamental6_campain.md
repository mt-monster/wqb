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
