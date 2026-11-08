# USA / GLB READY 池普查（2026-11-06）—— 本战役最大净增量发现

> 触发：此前战役只反复深耕 EUR/GBR/IND/HKG/KOR/CHN，从未对 **USA** 与 **GLB** 做过 READY 普查。
> 一次 `get_submit_ready(region=...)` 就读到全部，且多数行自带 `self` / `prod` ⇒ **零平台配额**。

---

## §1 USA：13 条 READY，3 颗全绿（含 2 颗纯单数据集 ATOM）

### 1.1 可直接判定全绿（自带 self/prod 双低）

| alpha | S | F | TO | 2Y | self | prod | type | 设置 | 字段来源 |
|---|---:|---:|---:|---:|---:|---:|---|---|---|
| `zqrgna91` | 2.67 | 1.66 | 15.8% | 1.68 | 0.287 | **0.6877** | REGULAR | USA/TOP2000/decay0/STATISTICAL/trunc0.08/nan ON | `buzz_intensity_score_2/11`（SOCIALMEDIA，单集 ⇒ **纯 ATOM**） |
| `N1eLE1de` | 2.63 | 1.54 | 14.1% | 2.07 | 0.275 | **0.6916** | REGULAR | 同上 | `credit_risk_model_score_5/7`（单集 ⇒ **纯 ATOM**） |
| `YPMvZZvv` | 1.79 | 1.06 | 6.2% | 1.68 | 0.411 | 0.6958 | REGULAR | 同上 | `mean_estimate_targetprice_annual12_tribes`（ANALYST，纯 ATOM） |

**三颗均 `fails=[]` / `fRA=0` / `status=UNSUBMITTED`** —— 已实读 `get_alpha_details` 确认。
⚠️ `zqrgna91` 余量 0.0123、`N1eLE1de` 余量 0.0084、`YPMvZZvv` 余量 0.0042 ⇒ **平台重算敏感，提交前须当场复测 prod**。已入 prod 队列。

### 1.2 骨架（都是极简，算子 3–8，远低于上限 12）

```
zqrgna91  signed_power(ts_decay_linear(group_rank(ts_zscore(ts_backfill(subtract(vec_avg(buzz_intensity_score_2), vec_avg(buzz_intensity_score_11)), 252), 252), market), 5), 0.8)   // 8 ops
N1eLE1de  ts_decay_linear(group_rank(ts_zscore(ts_backfill(subtract(vec_avg(credit_risk_model_score_5), vec_avg(credit_risk_model_score_7)), 252), 252), subindustry), 5)  // 6 ops
YPMvZZvv  group_rank(ts_zscore(mean_estimate_targetprice_annual12_tribes, 175), subindustry)                                                                                        // 3 ops
```

**共同机制 = 「两个同族字段相减取其差」**：`score_2 - score_11`、`score_5 - score_7`。这是本战役第一次系统性验证的**同族字段差分模板**（而非单字段水平）。
⇒ 可迁移：任一同族编号字段（如 `buzz_intensity_score_1..N`、`credit_risk_model_score_1..N`）两两相减即得正交信号，
且差分天然去掉了共同的水平成分 ⇒ 低换手（TO 6–16%）+ 高 2Y。

### 1.3 排除项

- `78LAAm92` / `78LAAZx1` / `P0MRkP0M` / `LL5rpRY2`：表达式为 `generate_stats(alpha); self_corr(...); reduce_max(...)` ⇒ **SUPER 选择式**，非 REGULAR，一律排除（与 `zq3zKgd8` 同类陷阱）。
- `P0od2pOp` / `pwdAPALb` / `E56XvX90` / `akKqLq56` / `6Xd7A5V7`：五条全是 `assetutilization_sentiment_polarity` 的变体（S 1.61–1.77 / TO 3–5% / 2Y 1.9–2.5），**同族 5 写 ⇒ 至多取 1**；且需先测 self/prod。
- `wpbagVMY`（S 2.03 / TO 6.6%）：字段与 `YPMvZZvv` 完全相同，只是窗口 400 vs 175、分组 market vs subindustry ⇒ 与 `YPMvZZvv` 高度相关，**二者只能留一**（已选 prod 已知的 `YPMvZZvv`）。

---

## §2 GLB：21 条 READY，去重后真实净产出 5–6 颗

### 2.1 ★ 关键去重发现：`mean_last_trade_price_return_30m_pre_close_2` 的 **7 种写法其实是同一个 alpha**

| alpha | 写法 | 窗口 | S | F | 2Y | self | prod |
|---|---|---:|---:|---:|---:|---:|---:|
| `LLNlZKMa` | `-group_zscore(ts_decay_linear(X,10), country)` | 10 | 2.53 | 1.58 | 1.84 | 0.473 | 0.5066 |
| `88jKRbRz` | `multiply(-1, group_zscore(...,5))` | 5 | 2.75 | 1.48 | 2.01 | 0.337 | 0.5624 |
| `akbWK6V5` | `-1*group_zscore(...,5)` | 5 | 2.78 | 1.48 | 1.97 | 0.400 | 0.5190 |
| `YPbW161l` | `multiply(-1.0, group_zscore(...,5))` | 5 | 2.87 | 1.47 | 1.71 | 0.406 | 0.5070 |
| `xA3mrqrw` | `-1.0*group_zscore(...,5)` | 5 | 2.68 | 1.45 | 1.93 | 0.394 | 0.5324 |
| `6XjYZVQ7` | `multiply(-1, group_zscore(...,5))` | 5 | 2.70 | 1.41 | 1.86 | 0.383 | **0.4951** |
| `3qXn1rJN` | `-group_zscore(ts_decay_linear(...,5), country)` | 5 | 2.70 | 1.18 | 1.67 | 0.231 | 0.5116 |
| `vRrJZMoA` | `-1.0*group_zscore(...,5)` | 5 | 2.49 | 1.09 | 1.88 | 0.315 | **0.4770** |

**同一字段 + 同一骨架 + 只改负号写法/窗口 ⇒ 互相相关性 ≈ 1，8 条里只能提交 1 条。**
这与 GBR `pv47` 族、IND 同族变体是**同一个陷阱的第三次复现**：`self` 全部 0.23–0.47 看起来每颗都能过，
但 `self` 只回答「与已提交池冲不冲突」，**不回答「这 8 颗彼此冲不冲突」**。
⇒ 唯一正确的做法是先跑 `compute_mutual_correlation`，不能按 self 通过条数计数。

**选 1 颗**：取 prod 余量最大的 `vRrJZMoA`（0.4770）或 `6XjYZVQ7`（0.4951）；`LLNlZKMa` 因窗口 10 与其余 7 条不同，可作第二颗候选（需实测互相关 < 0.7 才成立）。

### 2.2 独立族（可各出 1 颗）

| 族 | alpha | 骨架 | S | F | TO | 2Y | self | prod | 备注 |
|---|---|---|---:|---:|---:|---:|---:|---:|---|
| **RISK×市值桶** | `gJbxzpNQ` | `-group_zscore(ts_decay_linear(vec_avg(rsk60_offer),5), bucket(rank(cap),'0,1,0.1'))` | 2.51 | **3.23** | 10.8% | 4.02 | ? | **?** | fRA=1 = `CONCENTRATED_WEIGHT`（warning 级） |
| **RISK×波动桶** | `GrbkvJjZ` | 同上，桶换成 `bucket(rank(ts_std_dev(returns,66)),'0,1,0.1')` | 2.74 | **2.94** | 12.4% | 4.67 | ? | **?** | 同上；两桶不同 ⇒ 互相关可能 <0.7 |
| **图像 ML 预测** | `N1angWQp` | `trade_when(rank(vol/ts_mean(volume,22))>0.6, signed_power(subtract(group_rank(probability_label1_2quantile_20day_ohlcv_img,country),0.5),0.5), ...)` | 3.59 | 1.38 | 55.9% | 4.01 | ? | ? | 7 条同族（`single_bucket_5day/20day_*_ohlcv_img`）⇒ 取 1 |
| **量价相关** | `qMxzRqoP` / `O0Nm3jKg` | `-group_rank(ts_mean(corr_last_trade_price_with_volume,5), industry)` | 2.29/2.37 | 1.07/1.00 | 22.5/30.9% | 2.53/2.40 | ? | ? | 2 写 ⇒ 取 1 |
| **相对排名** | `ZYAPP6p3` | `signed_power(subtract(group_zscore(ts_mean(vec_avg(region_relative_rank_score),22),country),0.5),0.5)` | 1.59 | 1.11 | **2.17%** | 1.94 | ? | ? | 极低换手，可作冷腿储备 |

### 2.3 GLB 设置（实读 `gJbxzpNQ.settings`）

```
GLB / MINVOL1M / delay 1 / decay 6 / COUNTRY / trunc 0.02 / nanHandling OFF / pasteurization ON
```

`MINVOL1M` 是 GLB 的低波动子宇宙，trunc 0.02 比 EUR 的 0.08 更严 ⇒ GLB 天然偏保守、TO 低。

### 2.4 ★ `CONCENTRATED_WEIGHT` 陷阱

`gJbxzpNQ` / `GrbkvJjZ` 的 `ra_failed_checks = ["CONCENTRATED_WEIGHT"]`，`failed_ra_count = 1`、`ra_failed = true`，
但 `checks.fail = []`、该检查只出现在 `checks.warning`。
⇒ **`failed_ra_count` 会把 warning 级检查也计进去**，所以 `fRA>0` 不等于 `checks.fail` 非空；
反过来 `checks.fail=[]` 也不保证 `fRA=0`。**两个字段必须都读**，不能互推。
处理方向：GLB trunc 已是 0.02，再压只能动 `bucket` 的桶数（`0,1,0.1` → `0,1,0.2`）或加 `group_neutralize`。

---

## §3 待办

1. prod 实测：`gJbxzpNQ` / `GrbkvJjZ`（未知）+ `zqrgna91` / `N1eLE1de`（余量极薄，复测）—— 已入后台串行队列 `bg_63f6f009`。
2. GLB 同族去重：对 `mean_last_trade_price_return_30m_pre_close_2` 的 8 条 + `ohlcv_img` 的 7 条跑 `compute_mutual_correlation`，定死每组取 1。
3. USA `assetutilization_sentiment_polarity` 五条：先 `check_self_correlation`，再互相关，取 1。
4. ~~`gJbxzpNQ`/`GrbkvJjZ` 若 prod 过关…~~ → **已判死，见 §4**。

---

## §4 ★ prod 实测结果（2026-11-06 06:00–06:04，串行单队列）

| alpha | 区域 | S | F | 2Y | TO | prod | 判定 |
|---|---|---:|---:|---:|---:|---:|---|
| `zqrgna91` | USA | 2.67 | 1.66 | 1.68 | 15.8% | **0.6877** | ✅ 通过（复测 = 库内值，无缓存失真） |
| `N1eLE1de` | USA | 2.63 | 1.54 | 2.07 | 14.1% | **0.6916** | ✅ 通过（复测 = 库内值） |
| `gJbxzpNQ` | GLB | 2.51 | 3.23 | 4.02 | 10.8% | **0.8794** | ❌ 深钉判死 |
| `GrbkvJjZ` | GLB | 2.74 | 2.94 | 4.67 | 12.4% | **0.8453** | ❌ 深钉判死 |

### 4.1 ★★ 最大的方法学教训：**fitness 与 prod 完全无关**

`gJbxzpNQ` / `GrbkvJjZ` 拥有全战役最漂亮的一切：**F 3.23 / 2.94**（远超所有其他候选）、2Y **4.02 / 4.67**、
TO 仅 10.8% / 12.4%、GLB trunc 0.02（比 EUR 的 0.08 更严）、MINVOL1M 低波宇宙。**结果 prod 0.85–0.88，双双深钉。**

反观 USA 两颗：F 只有 1.66 / 1.54、2Y 1.68 / 2.07，却双双过关。

⇒ **IS 侧的任何一个质量维度（Sharpe / fitness / 2Y / 低换手 / 严格 trunc / 低波宇宙）都不预测 prod 相关性。**
⇒ 派 prod 队列时**不要按 fitness 或 Sharpe 排序**——排序与结果无关。应按「塔位缺口 / 是否纯 ATOM / prod 余量未知」排序。

### 4.2 ★ GLB 家族剩余全部测完 —— **4 个独立家族 0 上岸**

| alpha | 族 | S | F | TO | 2Y | prod | 判定 |
|---|---|---:|---:|---:|---:|---:|---|
| `qMxzRqoP` | 量价相关 | 2.29 | 1.07 | 22.5% | 2.53 | **0.7738** | ❌ 浅钉 |
| `O0Nm3jKg` | 量价相关（PCA 分组） | 2.37 | 1.00 | 30.9% | 2.40 | **0.8552** | ❌ 深钉 |
| `N1angWQp` | 图像 ML 预测（7 写取 1） | 3.59 | 1.38 | 55.9% | 4.01 | **0.7532** | ❌ 浅钉（耗时 206s） |
| `ZYAPP6p3` | 相对排名（TO 2.17%） | 1.59 | 1.11 | 2.17% | 1.94 | **0.8734** | ❌ 深钉 |

加上 §4 的 `gJbxzpNQ` 0.8794 / `GrbkvJjZ` 0.8453：**GLB 读数 6 项，5 项落在 0.75–0.88，全部判死。**

### ★ GLB 最终结论：**全区域只有 1 个可提交族**

唯一过关的是 `mean_last_trade_price_return_30m_pre_close_2` 族（8 条写法的 prod 全部 0.4770–0.5624）。
而这 8 条**数学上等价**（`-X` / `multiply(-1,X)` / `-1*X` / `-1.0*X` 是同一个表达式，只有 `LLNlZKMa` 的 `ts_decay_linear` 窗口是 10 而非 5），
⇒ **净产出 = 1 颗**（候选 `vRrJZMoA` prod 0.4770，余量最大），`LLNlZKMa` 可争取做第 2 颗但必须先实测互相关。

**规律**：GLB 是覆盖全球多国的大宇宙，`COUNTRY` 中性化把同一因子在各国的共同成分抠出来 ⇒ 与其他用户的全球宏观/量价类 alpha 高度重叠，prod 天然偏高。
唯一过关的那一族是 **30 分钟盘前微观结构残差**（`mean_last_trade_price_return_30m_pre_close_2`）—— 属于少数人做的日内微结构，所以拥挤度低。
⇒ **GLB 的正确打法：只做日内微观结构 / 盘前盘后成交类字段，不做横截面的水平类、风险载荷类、图像 ML 预测类。**

### 4.2b 原待测清单（已全部结案）

| alpha | 族 | S | F | TO | 2Y | prod 状态 |
|---|---|---:|---:|---:|---:|---|
| `qMxzRqoP` | 量价相关 | 2.29 | 1.07 | 22.5% | 2.53 | 待测 |
| `O0Nm3jKg` | 量价相关（PCA 分组版） | 2.37 | 1.00 | 30.9% | 2.40 | 待测 |
| `N1angWQp` | 图像 ML 预测（7 写取 1） | 3.59 | 1.38 | 55.9% | 4.01 | 待测 |
| `ZYAPP6p3` | 相对排名（TO 2.17%） | 1.59 | 1.11 | 2.17% | 1.94 | 待测 |

### 4.3 GLB `mean_last_trade_price_return_30m_pre_close_2` 族已自带 prod，无需再测

8 条 prod 全部 0.4770–0.5624（全过线），但彼此数学等价，**只能提交 1 条**。
选取建议：`vRrJZMoA`（prod 0.4770，余量最大）或 `6XjYZVQ7`（0.4951）；
`LLNlZKMa` 窗口 10 与其余 7 条不同，可作第 2 颗候选，**但必须先跑 `compute_mutual_correlation` 实测 <0.7**。