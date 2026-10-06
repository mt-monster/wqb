# GBR 候选清单（2026-10-06 12:45 生成）

## 平台已提交 ACTIVE/OS：**11 颗 / 目标 20 颗**（还差 9 颗；另有 5 颗储备）

> **catalog 体检**：GBR 覆盖率 86.3% | 真盲区 28 (已确认本区空 28) | ★可行动盲区 0

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

## ✅ 可信候选储备：**5 颗**

### `P0gv3AO7`  —  prod 0.5685 / self 0.2825

| S | F | margin | TO | DD |
|---:|---:|---:|---:|---:|
| 1.69 | 1.07 | 8.04bp | 0.1362 | 0.0327 |

```
group_rank(ts_target_tvr_decay(rank(ts_delta(ts_backfill(expected_dividend_yield,500),11)),lambda_min=0,lambda_max=1,target_tvr=0.15),industry)
```

### `9qWwZ3oe`  —  prod 0.6267 / self 0.3536

| S | F | margin | TO | DD |
|---:|---:|---:|---:|---:|
| 1.8 | 1.17 | 8.42bp | 0.1398 | 0.0451 |

```
group_zscore(ts_target_tvr_decay(rank(ts_delta(ts_backfill(mdl28_sm_structural_credit_structural_pd_pct,500),13)), lambda_min=0, lambda_max=1, target_tvr=0.15), industry)
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

### `9qWwZ3go`  —  prod 0.6890 / self 0.4589

| S | F | margin | TO | DD |
|---:|---:|---:|---:|---:|
| 1.67 | 1.09 | 8.48bp | 0.1340 | 0.0453 |

```
group_zscore(ts_target_tvr_decay(-rank(ts_delta(ts_backfill(mdl28_sm_structural_credit_structural_asset_drift_pct,500),8)), lambda_min=0, lambda_max=1, target_tvr=0.15), industry)
```

## 5 颗候选互不同源（可同时提交）

| alpha_id | 信息维度 | 数据集 | self 最近邻 |
|---|---|---|---|
| `9qWwZ3oe` | **结构化信用：违约概率变化**（`group_zscore`） | `model28` | JjQbYdGW 0.945（同族，取本颗） |
| `P0gv3AO7` | **预期股息率变化** | `model109` | GrbQ9JWO 0.283（最低） |
| `RR6NOlma` | **估值变化**（EP fy1） | `predictive_starmine` | 9qWaRGEK 0.635 |
| `omWVV6Y2` | **结构化信用：杠杆变化** | `model28` | KPNgQApj 0.501 |
| `9qWwZ3go` | **结构化信用：资产漂移变化**（`group_zscore`） | `model28` | 互相关 <0.62（独立注） |

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

### ★★★★ 2026-10-06 新增：三个从未扫过的维度（明细见 memory `2026-10-06.md` §110/§111）

**① `group_zscore` = 与「换字段/换窗/换轴/换中性化」并列的第 5 个杠杆**
（此前 100% 只用 `group_rank`；同信号同参数只换外层算子）
| 信号 | `group_rank` | `group_zscore` | 2Y |
|---|---|---|---|
| pd_pct | 1.62/1.00 | **1.80/1.17** | **3.01** ✅ |
| asset_drift | 1.57/0.99 | **1.67/1.09** | 2.21 ✅ |
| leverage | 1.62/1.02 | 1.63/1.07 | 1.58 ==限 ❌ |
| ep_yield fy1_3 | 1.70/1.02 | 1.69/1.06（sector）| 1.61，但 prod 0.7828 ❌ |
- **用法铁律**：只对**2Y 有余量**的信号用；2Y 贴线的信号会被打到限上。
- 粒度同 EUR：`industry`/`sector` 好，`subindustry` 差。

**② ★★★ 真正的闸是 2Y，不是 S/F** —— 前瞻价格比族（`smest_price_ratio_*`，9 字段）全体阵亡
| 字段 | S | F | **2Y** |
|---|---:|---:|---:|
| `smest_price_ratio_fy1_revenue_4` | **1.97** | **1.25** | **1.36** ✗ |
| `smest_price_ratio_fy2_earnings_4` | 1.70 | 1.01 | 1.39 ✗ |
| `smest_price_ratio_fy2_revenue_3` | 1.77 | 1.07 | 0.48 ✗ |
- S 高达 1.97 但 **2Y 全部 0.20–1.39**（无一个过 1.58）⇒ **S 高是假象**。
- `decay` 救不了（decay60 → 2Y 0.94；decay160 → S 崩到 1.15）⇒ **GBR 的 decay 与 EUR 相反，大档只伤信号**。

**③ `model38` = star value 族（20+ 字段）—— S/F/2Y 三项最强，但撞族级 prod 墙**
| alpha | 字段 | S | F | 2Y | prod |
|---|---|---:|---:|---:|---:|
| `RR6p33qd` | `star_val_piv_ratio`（取反） | **2.15** | **1.52** | **2.22** | **0.7530** ✗ |
| `XgJprrw0` | `star_val_pcf` | 1.85 | 1.26 | 1.73 | **0.8946** ✗ |
| `Wjepqqwo` | `star_val_ev_sales` | 1.99 | 1.40 | 1.45 | **0.7564** ✗ |
- ⚠ **self 仅 0.37–0.42**（对我们极新），但 **prod 直方图 [0.7,0.8) 桶 n=9** ⇒ 按族级判据（n≥8 判死）**该价值比族撞平台公共因子，判死**。
- 族内非价值比子族（rank / projection）另测（批 `1G93ha2bV518cGmwglnMA4E`）。
- ⚠ 平台不存在 `star_val_earnings_measure_type`（本地 catalog 有）—— 又一次「本地 ≠ 平台」。

**④ 本轮判死的副族**：`smest_growth_*` 前瞻增速（±0.07/±0.30）、
**水平口径**（去掉 `ts_delta` 只留 `rank`，S 0.19–0.56、TO 塌到 0.06）、`decay` 60/160。

**⑤ 5 颗储备全部通过「互不相关 + 与已提交池不相关」双重核验**
`compute_mutual_correlation`（本地零消耗）：5 储备 + 11 已提交**两两全 < 0.7**，最大 `RR6NOlma`↔`9qWaRGEK` 0.6348。
⇒ **同字段 ≠ 同族**：`RR6NOlma` 与已提交 `vRNk56mz` 同用 `ep_yield_pct_smest_fy1_3`，互相关仅 **0.5358**。

### 提交纪律（硬约束）
1. **提交会污染全池 prod**：提 1 颗把同族候选从 0.65 抬到 0.90+（实测 `3qVa2Lze` 提交后 `wpZ3RP96` 0.6865→0.9036）。
2. **DB 里 prod 凡在最近一次提交之前测的一律作废**；提交前必 `corr <id>` 实测。
3. **同族铁律**：prod 差异 <0.01 ⇒ 同族，只提 1 颗。
4. **优化判据是 prod 余量，不是 S 高低**。
5. 提交需**用户逐次明示**（全局闸 `ALLOW_ALPHA_SUBMIT=False`）。
