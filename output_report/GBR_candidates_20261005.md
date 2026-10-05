# GBR 战役候选清单（2026-10-05 18:20 生成）

## 平台已提交 ACTIVE/OS：**11 颗 / 目标 20 颗**（还差 9 颗）

| # | alpha_id | S | F | 2Y | prod | self | 提交日 |
|---|---|---:|---:|---:|---:|---:|---|
| 1 | `WjAV89jG` | 1.62 | 1.1 | 1.7 | 0.6882 | - | 2026-08-09 |
| 2 | `A1G7o1EE` | 1.61 | 1.13 | 1.64 | 0.6971 | 0.5697 | 2026-08-10 |
| 3 | `vRNk56mz` | 1.8 | 1.2 | 1.82 | 0.6271 | 0.2456 | 2026-08-11 |
| 4 | `GrlqxwKx` | 1.8 | 1.28 | 1.62 | 0.5001 | 0.5001 | 2026-08-17 |
| 5 | `KPNgQApj` | 1.69 | 1.05 | 1.77 | 0.683 | 0.3342 | 2026-09-25 |
| 6 | `rKO0GOVj` | 1.65 | 1.27 | 1.7 | 0.6986 | 0.2818 | 2026-09-25 |
| 7 | `GrbQ9JWO` | 1.97 | 1.72 | 2.1 | 0.6829 | 0.6797 | 2026-09-25 |
| 8 | `npdm0mrq` | 1.76 | 1.1 | 1.98 | 0.5557 | 0.3322 | 2026-09-27 |
| 9 | `E5p2r7VL` | 1.92 | 1.54 | 2.07 | 0.6967 | 0.6329 | 2026-09-27 |
| 10 | `9qWaRGEK` | 1.67 | 1.02 | 1.89 | 0.6591 | 0.6064 | 2026-10-04 |
| 11 | `3qVa2Lze` | 1.7 | 1.04 | 2.13 | 0.538 | 0.495 | 2026-10-05 |

## ✅ 可信候选储备：**4 颗**（全闸通过 + prod 最近一次提交后实测）

### `P0gv3AO7`  —  prod 0.5685 / self 0.2825

| S | F | margin | TO | 2Y | DD |
|---:|---:|---:|---:|---:|---:|
| 1.69 | 1.07 | 8.04bp | 0.1362 | 过线 | 0.0327 |

```
group_rank(ts_target_tvr_decay(rank(ts_delta(ts_backfill(expected_dividend_yield,500),11)),lambda_min=0,lambda_max=1,target_tvr=0.15),industry)
```

### `JjQbYdGW`  —  prod 0.6072 / self 0.3620

| S | F | margin | TO | 2Y | DD |
|---:|---:|---:|---:|---:|---:|
| 1.62 | 1 | 7.60bp | 0.1312 | 过线 | 0.0407 |

```
group_rank(ts_target_tvr_decay(rank(ts_delta(ts_backfill(mdl28_sm_structural_credit_structural_pd_pct,250),13)),lambda_min=0,lambda_max=1,target_tvr=0.13),industry)
```

### `omWVV6Y2`  —  prod 0.6579 / self 0.5007

| S | F | margin | TO | 2Y | DD |
|---:|---:|---:|---:|---:|---:|
| 1.62 | 1.02 | 8.00bp | 0.1283 | 过线 | 0.0527 |

```
group_rank(ts_target_tvr_decay(rank(ts_delta(ts_backfill(mdl28_sm_structural_multiple_credit_structural_leverage,500),8)),lambda_min=0,lambda_max=1,target_tvr=0.15),industry)
```

### `RR6NOlma`  —  prod 0.6861 / self 0.6348

| S | F | margin | TO | 2Y | DD |
|---:|---:|---:|---:|---:|---:|
| 1.7 | 1.02 | 7.34bp | 0.1224 | 过线 | 0.0301 |

```
group_rank(ts_target_tvr_decay(rank(ts_delta(ts_backfill(ep_yield_pct_smest_fy1_3,250),20)),lambda_min=0,lambda_max=1,target_tvr=0.13),industry)
```

## 四颗候选**互不同源**（可同时提交，不会互相污染 prod）

| alpha_id | 信息维度 | 数据集 | self 最近邻 |
|---|---|---|---|
| **`P0gv3AO7`** | **预期股息率变化** | `model109` | GrbQ9JWO 0.283（最低） |
| `JjQbYdGW` | **结构化信用：违约概率变化** | `model28` | 3qVa2Lze 0.362 |
| `omWVV6Y2` | **结构化信用：杠杆变化** | `model28` | KPNgQApj 0.501 |
| `RR6NOlma` | **估值变化**（EP fy1） | `108`/predictive_starmine | 9qWaRGEK 0.635 |

## 本轮优化结果（2026-10-05 18:40）

| 候选 | 优化前 | 优化后 | 结论 |
|---|---|---|---|
| `RR6NOlma` 族 | S1.70/F1.02/prod **0.6861** | `P0gvv5gE`(bf500) S1.72/F1.03/prod **0.6905**；`d51ddaWX`(窗22) prod **0.6975** | ❌ **不换**：S↑ 但 prod 更贴墙 |
| `QPKErLvX` 族 | S1.59/F1.00/prod 0.6593 | **`omWVV6Y2`**(bf500,窗8) S**1.62**/F**1.02**/prod **0.6579** | ✅ **换**：三项全面更优 |
| `JjQbYdGW` 族 | S1.62/F1.00/prod **0.6072** | `N1VAAQn8`(bf500) 等价 | ❌ **不换**：原版 margin 略高 |

**★ 教训**：优化时 S↑ 往往伴随 prod↑（`追 S 必撞 prod`）。**判断标准应是 prod 余量，不是 S 高低**。
`RR6NOlma` 族就因盲目提 S 而 prod 从 0.6861 升到 0.6975 ⇒ **原版才是最优**。

## 重要纪律（2026-10-05 实测得出）

1. **提交会污染整个候选池的 prod**：提交 1 颗会把同族候选 prod 从 0.65 抬到 0.90+。
   实测：`wpZ3RP96` 记录 0.6865、`VkaZYdbG` 0.6849 → `3qVa2Lze` 提交后刷新 → **0.9036 / 0.9899**。
2. **DB 里的 prod 凡在最近一次提交之前测的，一律作废**；提交前必须
   `check_correlation(alpha_id, refresh=True)`。
3. **同族铁律**：同批候选 prod 差异 <0.01 ⇒ 判同族，只提 1 颗。
   ⚠ `mdl28` leverage 的多个窗（5/8/9/11/22）**属同族**，只能提 1 颗（选 `QPKErLvX`）。

## 本轮新增活族：`model28` 结构化信用（Merton 类）

原为"负 S"族，实测发现**方向性**后翻盘：

| 字段 | 正确方向 | S | F |
|---|---|---:|---:|
| `..._multiple_..._leverage`（窗8, tvr0.15） | 正向 | **1.59** | **1.00** ✅ |
| `..._credit_..._pd_pct`（窗13, tvr0.13） | 正向 | **1.62** | **1.00** ✅ |
| `..._credit_..._asset_drift_pct`（窗8, tvr0.13） | **取反** | 1.57 | 0.99（差 0.01）|
| `..._credit_..._distance_to_default` | **取反** | 1.29 | 0.73 |

**规律**：`ts_delta` 窗**越短越好**（8–13 为甜点；33/44/66 迅速衰减）；tvr 0.13–0.15。

## 本轮判死清单（10-05 全天，12 族 / 约 100 条实测）

| 族 | 最好 S | 死因 |
|---|---:|---|
| `sta1_*` 统计聚类分组轴 | 0.59 | 簇内无离散度，把 S 从 1.66 打到 0.30 |
| `dl_riskfree_returns`（OTHER 塔） | 1.08 | ML 分位概率横截面太弱 |
| `model264` 趋势方向概率 | 0.43 | 无横截面信号 |
| `model238` Smart Holdings 拥挤度 | 0.55 | 同上 |
| `model36` 违约风险百分位 | 0.27 | 同上 |
| **`pattern_scores`（PV 塔 504 字段）** | 0.26 | 图表形态相似度无横截面信号 |
| **`model106`** 熊市敏感度 | 0.26 | 同上 |
| **`model250`** ML 复合分 | −0.36 | 同上 |
| **3 个 insider 数据集** | 0.23 | cov 仅 0.59 太稀疏 |
| `analyst44`/`news17`/`analyst7` 系列 | — | 全 VECTOR，GBR 不可用 |
| `pv30`/`pv29` | — | 全 GROUP（是轴不是信号） |
| `108` 族 `ep_*` 兄弟字段 | — | 估值维 prod 已饱和 0.69–0.72 |

## 结论

- **GBR 能提取横截面信号的只有三类维度**：① 估值水平/变化（prod 已饱和）；② 信用违约（`model53` 已用）；
  ③ **结构化信用 `model28`（本轮新发现，仍有余量）**。
- **规律**：**"派生/复合"字段（概率、百分位、聚类、模型分）在 GBR 窄截面普遍无区分度**；
  有效的是**原始财务/信用量在时间上的变化**（`ts_delta` + 短窗）。
- **点塔**：本季 GBR D1 全为 MODEL 塔；实测 OTHER/NEWS/INSTITUTIONS/PV(pattern_scores)/INSIDERS 均无效
  ⇒ **非 MODEL 塔暂无解**。
