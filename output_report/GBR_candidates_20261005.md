# GBR 候选清单（2026-10-06 03:02 生成）

## 平台已提交 ACTIVE/OS：**11 颗 / 目标 20 颗**（还差 9 颗；另有 4 颗储备）

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

## ✅ 可信候选储备：**4 颗**

### `P0gv3AO7`  —  prod 0.5685 / self 0.2825

| S | F | margin | TO | DD |
|---:|---:|---:|---:|---:|
| 1.69 | 1.07 | 8.04bp | 0.1362 | 0.0327 |

```
group_rank(ts_target_tvr_decay(rank(ts_delta(ts_backfill(expected_dividend_yield,500),11)),lambda_min=0,lambda_max=1,target_tvr=0.15),industry)
```

### `JjQbYdGW`  —  prod 0.6072 / self 0.3620

| S | F | margin | TO | DD |
|---:|---:|---:|---:|---:|
| 1.62 | 1 | 7.60bp | 0.1312 | 0.0407 |

```
group_rank(ts_target_tvr_decay(rank(ts_delta(ts_backfill(mdl28_sm_structural_credit_structural_pd_pct,250),13)),lambda_min=0,lambda_max=1,target_tvr=0.13),industry)
```

### `omWVV6Y2`  —  prod 0.6579 / self 0.5007

| S | F | margin | TO | DD |
|---:|---:|---:|---:|---:|
| 1.62 | 1.02 | 8.00bp | 0.1283 | 0.0527 |

```
group_rank(ts_target_tvr_decay(rank(ts_delta(ts_backfill(mdl28_sm_structural_multiple_credit_structural_leverage,500),8)),lambda_min=0,lambda_max=1,target_tvr=0.15),industry)
```

### `RR6NOlma`  —  prod 0.6861 / self 0.6348

| S | F | margin | TO | DD |
|---:|---:|---:|---:|---:|
| 1.7 | 1.02 | 7.34bp | 0.1224 | 0.0301 |

```
group_rank(ts_target_tvr_decay(rank(ts_delta(ts_backfill(ep_yield_pct_smest_fy1_3,250),20)),lambda_min=0,lambda_max=1,target_tvr=0.13),industry)
```

## 4 颗候选互不同源（可同时提交）

| alpha_id | 信息维度 | 数据集 | self 最近邻 |
|---|---|---|---|
| `P0gv3AO7` | **预期股息率变化** | `model109` | GrbQ9JWO 0.283（最低） |
| `RR6NOlma` | **估值变化**（EP fy1） | `predictive_starmine` | 9qWaRGEK 0.635 |
| `JjQbYdGW` | **结构化信用：违约概率变化** | `model28` | 3qVa2Lze 0.362 |
| `omWVV6Y2` | **结构化信用：杠杆变化** | `model28` | KPNgQApj 0.501 |

---

## 战役结论摘要（2026-10-05 全天，明细见 `.workbuddy/memory/2026-10-05.md`）

### ★★★ 唯一有效判据：「原始量 + ts_delta 短窗」 vs 「派生分一律无效」
> **拿到新字段先问：它是「原始量」还是「派生分」？**
> - **派生分**（PCA / 概率 / 百分位 / 评分 / 聚类 / 复合分量）⇒ **直接跳过**（GBR 上五次验证全部无效）。
> - **原始量**（财务科目 / 信用量 / 股息 / 价格）⇒ 用 `ts_delta` + **短窗 8–13** 试。
> - 例外：能表达成**收益率口径**的前瞻量也有效（`expected_dividend_yield` S1.69）。

### 全 category 扫描（15 类）
| category | 结论 |
|---|---|
| **MODEL** | ✅ **唯一有信号**（13 数据集 / 921 低拥挤字段）：`model28` 结构化信用、`model109` 预期股息率、`predictive_starmine` 估值 |
| OTHER | ⚠ 弱（`other455` 供应链图嵌入最好 0.99）|
| PV / ANALYST / FUNDAMENTAL / INSIDERS | ❌ 全灭（ANALYST 32 条、PV 537 字段几乎全是已测死的 `pattern_scores`）|
| INSTITUTIONS / RISK | 无低拥挤字段 |
| SOCIALMEDIA / SHORTINTEREST / SENTIMENT / OPTION / NEWS / MACRO / EARNINGS | **无任何可用 MATRIX 字段** |

### 批级参数扫描结论（六维空间已全部扫过）
| 参数 | 结论 |
|---|---|
| **`neutralization`**（11 档） | ⭐ **唯一有效强杠杆**（F 最高 +0.35）：`SLOW` 对 leverage、`CROWDING` 对 ep_yield、`MARKET` 对 ep_yield。**但与 prod 锁步上升 ⇒ 只能打磨，不能造候选**。避开 `FAST`/`SLOW_AND_FAST`/`REVERSION_AND_MOMENTUM` |
| `truncation`（0.02/0.05/0.1/0.15） | ❌ **no-op**（460 持仓下平均权重 0.2%，远低于阈值，从不触发）|
| `decay`（0/4/12/30） | 12 最优；大改破坏信号 |
| `universe` / `delay` | GBR 各只有一档（TOP700 / 1）|

### 重要副产：两个结构性规律
1. **后缀 = 数据质量档**：`ep_yield_pct_smest_fy2_**3**` S1.76 vs `fy2_**7**` S1.38 ⇒ **优先低后缀**。
2. **PD 族期限**：**2 年最优**（1.70）；5 年 1.15、7 年 0.87 ⇒ 期限越长越弱。
   `mdl53_ms5_*`（另一套 PD 模型）更弱（0.15–0.34）——同族 ≠ 同强度。

### 最高 S/F 记录（均被 prod 拦下）
| 表达式 | S | F | prod |
|---|---:|---:|---:|
| leverage × SLOW | **1.94** | **1.37** | 0.7243 ✗ |
| asset_drift × SLOW | **1.77** | **1.21** | 0.7169 ✗ |
| ep_yield × MARKET | 1.74 | 1.15 | 0.7047 ✗ |
| ep_yield × CROWDING | 1.70 | 1.11 | **0.6919** ✅（但与 RR6NOlma 同族）|

### 提交纪律（硬约束）
1. **提交会污染全池 prod**：提 1 颗把同族候选从 0.65 抬到 0.90+（实测 `3qVa2Lze` 提交后 `wpZ3RP96` 0.6865→0.9036）。
2. **DB 里 prod 凡在最近一次提交之前测的一律作废**；提交前必 `corr <id>` 实测。
3. **同族铁律**：prod 差异 <0.01 ⇒ 同族，只提 1 颗。
4. **优化判据是 prod 余量，不是 S 高低**。
5. 提交需**用户逐次明示**（全局闸 `ALLOW_ALPHA_SUBMIT=False`）。
