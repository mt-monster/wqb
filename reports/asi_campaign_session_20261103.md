# ASI 战役会话报告（2026-11-03）

**目标**：在 ASI 未点亮塔（本赛季提交 <3）挖掘 20 个 REGULAR alpha，优先 ATOM 单数据集。
**固定设置**：ASI / MINVOL1M / D1 / SLOW / decay=4 / truncation=0.08 / nanHandling=ON / maxTrade=ON / pasteurization=ON。
**本地台账**：`data/wqb.db` 最新波次 20260963 记录「已点亮塔 0/16」，主墙 `LOW_ROBUST_UNIVERSE_RETURNS (29/29 near)`。

---

## 1. 战略转向：PV → FUNDAMENTAL

论坛实证（6 篇 ASI 专项帖）把「中性化档位」确立为 ASI 双闸（JPN + robust）的第一杠杆，而**它是不是利好取决于信号快慢**：

| 信号类型 | STATISTICAL 最优 S | SLOW 最优 S | 判定 |
|---|---:|---:|---|
| PV 快信号（intraday_pv_feats） | **2.17**（批 L） | 1.77（批 S） | SLOW 是毒性 |
| fundamental 慢信号（fundamental23） | — | **2.29**（批 T，零 FAIL） | SLOW 是决定性 |

⇒ **SLOW 只对季度级慢变量有效**；对日频价格信号反而毁伤。这条判据写死为选档规则。

论坛来源：
- `42692435210903` 双重 group 标准化（内层 `group_zscore(F,country)` + 结尾归一 + `winsorize std=2.0–2.7`）：robust 0.849 FAIL → 0.905 PASS。
- `43783812201879` robust 门槛 = 0.9×IS Sharpe；Japan 病根在平滑度。
- `37473718017175` `winsorize std=5` + 流动性过滤 + `group_cartesian_product(country, bucket(rank(cap)))`。
- `43454103307031` W≥40 消除 JPN；换分组字段无效；加 `ts_decay_linear` 平滑腿破坏效果；decay=10 恶化。
- `42258807786391` **SLOW 是 ASI 最优中性化**（2.03 > COUNTRY 1.43 > SUBINDUSTRY 1.10），数据集优先级 Fundamental 2.66 / Imbalance 2.73 / PV 仅 1.18。
- `43624312881943` **同一排序只换权重形状，prod 一过一不过**；MINVOL1M 最好、MINVOL10M 与 TOP500 全面变差；分组轴要「交叉」不要「嵌套」。

已排除方向（不再重试）：`TOP500` / `MINVOL10M` universe、`group_rank` 替代 `group_zscore`（丢幅度）、量能门控改 robust 比例、`add(multiply(...))` 加权混腿（静态门禁 `[POISON] weighted_leg_mix_func_prefix` 整批拒绝）。

---

## 2. 零 FAIL 候选（塔位 ASI/D1/FUNDAMENTAL，本赛季 0 颗）

| alpha | 表达式 | S | F | TO | 2Y | sub | dd | RA fail | prod |
|---|---|---:|---:|---:|---:|---:|---:|---:|---|
| **bl6jJRKp** | `rank(ts_delta(ts_zscore(divide(ebit, assets), 252), 252))` | 2.29 | 1.27 | 5.84% | 2.15 | 1.11 | 1.93% | **0** | **0.8576 ✗** |
| **N1N73kRw** | 同上，内层 zscore 窗口 504 | 2.21 | 1.22 | 5.61% | 2.37 | 1.10 | 2.00% | **0** | 待取（inflight） |
| **xArjWXNp** | `ebit/sales` 版 | 2.06 | 1.08 | 6.16% | 2.47 | 1.18 | 2.07% | **0** | 待取（inflight） |
| **leAjP90e** | `rank(ts_decay_linear(ts_delta(ts_zscore(divide(ebit, assets), 252), 252), 5))` | **2.27** | 1.26 | 5.5% | 2.23 | 1.12 | — | **0** | 待取（inflight） |

- self 相关性全部极低：bl6jJRKp **−0.047**、N1N73kRw −0.0337、xArjWXNp −0.0362（阈值 0.7，pool_size 5）。
- bl6jJRKp 逐年覆盖完美：2014–2023 十年 longCount 1575–2288、shortCount 1560–2235、**每年 pnl 均为正**、年度 Sharpe 0.91–3.58。
- bl6jJRKp prod 直方图：[0.8,0.9) 3 颗 + [0.7,0.8) 25 颗 = 深钉厚尾，来源是 `ebit`(aC 2490) / `assets`(aC 6064)。

**唯一残留障碍 = prod 相关性**。⚠ 按纪律：`correlation_busy` / 120s 超时 **不得据此判死**，需重查取真值。

---

## 3. 批 Y 归因：单杠杆消融（批 `2oiouWgp45hBcwESGWvP5qA`，10 条，同一核心几何）

核心 `C = rank(ts_delta(ts_zscore(divide(ebit, assets), 252), 252))`（基线 S 2.29 / 0 FAIL）。

| alpha | 改动杠杆 | S | F | 2Y | sub | fail |
|---|---|---:|---:|---:|---:|---:|
| `omEq0rYn` | 换序 `ts_zscore(ts_delta(...))` | **2.34** | 1.32 | 1.75 | 1.22 | 1 (robust ratio) |
| `leAjP90e` | 外层 `ts_decay_linear(...,5)` | 2.27 | 1.26 | 2.23 | 1.12 | **0** |
| `6XdlLJEJ` | `group_neutralize(..., industry)` | 2.26 | 1.24 | 2.06 | 1.07 | 1 (JPN) |
| `9qxXOmw2` | `group_zscore(..., subindustry)` | 2.08 | 1.07 | 1.95 | 0.83 | 2 |
| `6XdlLJzJ` | 内层 `winsorize(std=3)` | 1.76 | 0.85 | 1.33 | 1.17 | 3 |
| `E56lPLkK` | `vector_neut(C, rank(ebit/assets))` | 1.71 | 0.82 | 1.68 | 0.74 | 2 |
| `qMLjJ3Av` | `ebit/sales` + vector_neut | 1.54 | 0.70 | 1.97 | 0.87 | 2 |
| `leAjP9Ve` | 外层 delta 窗口 126 | 1.37 | 0.58 | 0.68 | 0.36 | 6 |
| `3qol5gRP` | 外层 delta 窗口 504 | 1.43 | 0.61 | 1.48 | 0.88 | 6 |
| `xArjpWxN` | zscore504 + vector_neut | 0.98 | 0.35 | 1.44 | 0.66 | 3 |

**四条可复用结论**：
1. **`vector_neut` 是 prod 破墙的死路**：无论对 `rank(ebit/assets)` 还是 `rank(ts_zscore(ebit/assets))`，S 都从 2.29 掉到 1.71/0.98，且新增 JPN、FITNESS 失败。残差化把机制本身削掉了。
2. **外层窗口 252 是尖峰**：126 → S 1.37（6 项挂）、504 → S 1.43（6 项挂）。窗口不是平滑旋钮，252 是唯一谷底。
3. **权重平滑 `ts_decay_linear(...,5)` 是「无损杠杆」**：S 2.29→2.27、2Y 2.15→2.23、sub 1.11→1.12，仍零 FAIL。它只改权重形状不改排序 —— 正好对上论坛「同一排序只换权重形状，prod 一过一不过」的机制，是当前**最有希望的 prod 破墙点**。
4. **换序 `ts_zscore(ts_delta(...))` 抬 S 但毁 2Y**（2.15→1.75），且引入 robust ratio 墙 —— 不能用。

---

## 4. 模板库（≥10 结构互异，按机制归因）

| # | 模板 | 结构 | 来源 | 实测状态 |
|---|---|---|---|---|
| 1 | 水平量 + 截面 rank | `rank(F)` | 自建 | W 批 2Y 挂 |
| 2 | 时序 zscore + 一阶差分 | `rank(ts_delta(ts_zscore(F,W),W))` | 自建 | **✓ 零 FAIL ×3** |
| 3 | 权重平滑 | 外层 `ts_decay_linear(·,5)` | 论坛 43624312881943 | **✓ 零 FAIL** |
| 4 | 换序差分 | `rank(ts_zscore(ts_delta(F,W),W))` | 自建 | S 2.34 / 1 挂 |
| 5 | 组内中性化 | `group_neutralize(·, industry)` | 论坛 37473718017175 | 1 挂 JPN |
| 6 | 组内 zscore | `group_zscore(·, subindustry)` | 论坛 42692435210903 | 2 挂 |
| 7 | 向量残差化 | `vector_neut(·, rank(crowded))` | 自建 | ✗ 全灭 |
| 8 | 缩尾 | `winsorize(·, std=k)` | 论坛 42692435210903 | 3 挂 |
| 9 | 覆盖率兜底分域 | `if_else(greater(S,k), vector_neut(C,S), vector_neut(C,L))` | 自建 | 待测 |
| 10 | 更新门控 | `trade_when(less(days_from_last_change(F),55), …, -1)` | 论坛 43809344542359 | Z 批在飞 |
| 11 | 概率差 | `subtract(prob_q5, prob_q2)` | 论坛 43809407730071 | Z 批在飞 |
| 12 | 信心加权 | `multiply(pred, confidence)` | 论坛 43809407730071 | Z 批在飞 |
| 13 | 期限结构差 | `subtract(ts_mean(F_120d,5), ts_mean(F_60d,5))` | 自建 | Z 批在飞 |
| 14 | 多尺度背离 | `subtract(ts_zscore(F,66), ts_zscore(F,252))` | 自建 | Z/AB 批 |
| 15 | 二阶矩 | `rank(ts_std_dev(F,W))` | 自建 | Z/AB 批 |
| 16 | 双口径分歧 | `subtract(rank(F_local), rank(F_global))` | 自建 | AB 批待发 |

---

## 5. 数据集画像（ASI / MINVOL1M / D1）

### fundamental23（FUNDAMENTAL，374 字段，cov 0.754）
字段名干净无前缀：`ebit / assets / sales / cogs / debt / cash / cashflow_op / return_equity / return_assets / receivable / inventory / ppent / goodwill / income_tax / pretax_income / ebitda`。
筛出 **120 个 cov≥0.85 且 alphaCount≤400** 的低拥挤字段，最低 aC：`long_term_contract_liabilities`(5) / `long_term_debt_total`(7) / `retained_earnings_liabilities`(7) / `total_assets_annual_atot`(9) / `total_current_assets_4`(10) / `fnd23_cpca`(50) / `fnd23_vnis`(71) / `fnd23_crta`(74) / `fnd23_dttl`(94) / `fnd23_fcff`(78) / `fnd23_fcis`(93)。

### fundamental44（FUNDAMENTAL，12 字段，cov 0.875）—— 会计质量/操纵检测
`fnd44_cashflow_accruals`(aC 113) / `fnd44_factor_benford`(226) / `fnd44_fscore`(113) / `fnd44_jones_cf_accruals`(70) / `fnd44_modified_jones_cf_accruals`(71) / `fnd44_mscore`(158) / `fnd44_perc_accruals`(128) / `fnd44_probability_restatement`(108) / `fnd44_probability_restatement_global`(165) / `fnd44_score`(121) / `fnd44_working_capital_accruals`(264) / `fnd44_yoon_wc_accruals`(155)。
经济学：Sloan(1996) 应计异象（高应计→低未来收益）、Beneish M-Score（操纵风险→做空）、Jones/Modified-Jones（可操纵应计）。

### chart_cnn_alpha（MODEL，1010 字段，cov 0.953）—— 最处女的一块
**517 个字段 cov≥0.99 且 aC≤20**。家族：`cnn_predicted_prob_*`(53) / `cnn_confidence_score*`(28) / `img*`(418) / `probability_*`(178) / `imgpred_*`(49) / `imgfeat_*`(31) / `relative_*`(15) / `rank1-5_next*_return_*`(17)。aC=0 的满覆盖字段大量存在。

### dl_riskfree_returns（OTHER，57 字段，cov 1.0）—— ASI 最强新族
全部 MATRIX、覆盖满格。两个子族：
- `quantile_label_{1..5}bucket_{5,20,60}day_ohlcv` — 未来 N 日**市场中性收益的连续回归预测**（浮点，需缩尾）
- `probability_label{0,1}_{2,3,4,5}quantile_{5,20,60}day_ohlcv` — 落入某分位桶的**概率**

**aC 极低的处女字段**：`probability_label2_4quantile_20day_ohlcv_2`(**9**) / `probability_label1_3quantile_60day_ohlcv`(**15**) / `probability_label1_3quantile_5day_ohlcv_2`(**16**) / `probability_label3_5quantile_5day_ohlcv_2`(**17**) / `probability_label2_4quantile_5day_ohlcv`(19) / `probability_label1_4quantile_60day_ohlcv`(22) / `probability_label0_4quantile_60day_ohlcv`(23) / `probability_label0_3quantile_60day_ohlcv`(26) / `probability_label1_3quantile_20day_ohlcv`(29) / `quantile_label_2bucket_60day_ohlcv`(**41**) / `quantile_label_3bucket_60day_ohlcv`(88) / `quantile_label_3bucket_5day_ohlcv`(92)。

⚠ 已被大量开采的：`quantile_label_1bucket_5day_ohlcv_2`(1137) / `quantile_label_1bucket_20day_ohlcv`(**810**，即 P0o7Ra1W 用的那颗) / `probability_label2_3quantile_5day_ohlcv`(1715)。
⇒ 这一族**同机制换期限**（20d→60d、1bucket→2/3bucket）是合法的降拥挤路径：机制不变、字段更新鲜。


### ⚠ 批 AD 决定性负结果（chart_cnn_alpha 517 个处女字段）
套 10 个结构互异模板（概率差 / 分位排序 / 端点差 / 概率比 / 一阶差分 / 平滑+行业排序 / 信心加权 / 多尺度背离 / 二阶矩 / 反向）→ **10/10 全灭，最好 S 仅 1.25**（`subtract(rank5_next30d_return_equity_star6, rank1_next30d_return_equity_star6)`），多数为负。
⇒ **aC≤20 + cov≥0.99 + 名字漂亮，三件事同时成立仍然可以零信号。** 低 aC 必须按「待验证」处理，先派原子探针。

## 9. OTHER 塔 `dl_riskfree_returns` —— 双近闸定位（本轮最强族）

**代表候选** `Jje76aWl` = `group_rank(ts_mean(winsorize(quantile_label_1bucket_20day_ohlcv, std=3), 5), sector)`，塔位 **ASI/D1/OTHER（倍率 1.4）**

| 指标 | 值 | 闸门 | 判定 |
|---|---:|---|---|
| Sharpe | **5.11** | ≥1.58 | ✅ |
| Fitness | **4.40** | ≥1.0 | ✅ |
| 2Y Sharpe | **3.94** | ≥1.58 | ✅ |
| sub-universe | **2.91** | ≥0.517×5.11 = 2.64 | ✅ |
| ROBUST_UNIVERSE_SHARPE.WITH_RATIO | **4.22** | **4.60**（= 0.9×IS） | ❌ 差 **8.3%** |
| ROBUST_UNIVERSE_RETURNS | **0.0776** | **0.0834** | ❌ 差 **7.5%** |
| **prod** | **0.7607** | <0.70 | ❌ 超线 **8.6%** |

### 关键判读

1. **robust 是浅钉不是深钉**：两条都只差 7–8%，按「浅钉先归因后破墙」纪律不判死。
2. **20+ 结构变体全部撞同一面墙**（批 AC 10 条 + 批 AF 9 条）：换分组轴（sector/industry/country/subindustry）、平滑 5/10/22 日、缩尾 2/3/5、回填 60 日、外层 decay、外层 ts_rank、换期限字段 —— S 全部 3.4–5.2，robust 两条**无一例外全挂**。⇒ 这是信号本身在小盘/大票上的分布问题，**表达式层无解**。
3. **换 universe 的路断了**：`dl_riskfree_returns` 的字段在 ASI 的 TOP3000 / TOP1200 上 `unknown_fields`，只存在于 MINVOL1M 系。
4. **prod = 0.7607 落在灰区 0.70–0.80**：按族代表判据，同族**最多再测 2 颗**；且这一族同机制换期限的字段 aC 只有 9–41（代表字段 aC 810），是最有希望把 prod 压下去的方向 → 批 AE。
5. ⚠ **`cap` 会给 alpha 加上 PV 塔**：批 AF 里所有 `bucket(rank(cap))` 变体的塔位变成 `ASI/D1/PV + ASI/D1/OTHER` 双塔 —— 触碰「PV 与 OTHER 禁两两组合」的硬约束，**整批 AF 作废，cap 不可再用**。

### 批 AB 决定性负结果（fundamental44 会计质量）
12 字段套 10 个结构互异模板（Sloan 应计水平/一阶差分/二阶矩/行业 zscore/多尺度背离/长周期变化/双口径分歧/缩尾平滑/Benford 法证/现金流-经营应计差）→ **10/10 全灭，|S| ≤ 0.45**。会计质量机制在 ASI **无信号**。


### 其他低拥挤 MODEL 数据集
`price_signal_dl`(28 字段, cov 0.913, aC 138) — `normalized_trend_indicator_0..6`(aC 3–11) / `normalized_volume_indicator_0..6`(aC 1–4) / `raw_*`(aC 1–15)。
`multi_source_model`(60 字段, cov 0.951, aC 160) — `price_volume_quantile{1,5}_{5,20,60}d_pred`、`long_term_quantile{1,5}_{60,120}d_pred`、`analyst_quantile{1,5}_{60,120}d_pred`、`*_confidence_*_pred`（最低 aC=0）。
`event_stock_model`(3, aC 36) / `behavioral_signals`(7, aC 63) — 均为 **VECTOR**，需 `vec_avg`/`vec_sum`。
高拥挤需回避：`model25`(aC 43811) / `model110`(99767) / `model26`(61828) / `other176`(38394)。

### ASI 数据集总量
158 个数据集，category 分布：analyst / broker / earnings / fundamental / imbalance / insiders / institutions / macro / model / news / other / pv / risk / sentiment / shortinterest / socialmedia。

---

## 6. 在飞与已收批次

| 批次 | multisim_id | 内容 | 状态 |
|---|---|---|---|
| K | `222Xh1d4y4peaKH1RC4Xo2H` | MINVOL10M/STATISTICAL | 完成，全灭（最好 0.83） |
| L | `dfy2maxK59dazd16eVUr1OY` | MINVOL1M/STATISTICAL，country 分组 | 完成，S 2.17 |
| M | `18sp4wdIM4CsbFhtta5xDuM` | 量能门控 | 完成，ratio 0.70 不动 |
| O | `2TRvRJCC4vlcAb9BEZnVHr` | country 几何变体 | 完成，最好 1.97 |
| P | `1kfEUv3i95ipcMhvccxq4rm` | MINVOL10M/country | 完成，全灭 |
| S | `2wpBcm1XV5fw9RbLbJeOofB` | SLOW + PV | 完成，SLOW 对 PV 有害 |
| T | `aOUM83T24ICaiH10tbSSINP` | fundamental23 SLOW | 完成，**3 条零 FAIL** |
| V | `HHQUPgfJ4XU9bY1bLvdmo5f` | 同 T，prod 变体 | 完成，**2 条零 FAIL** |
| W | `ZWMrVeR04pSbV28obr1sPq` | fundamental 质量 | 完成，最好 S 2.03 但 2Y 0.62 挂 |
| X | `2FzxGp6wj527c8gaQFvPgWw` | 低 aC 字段 | **卡死**（40+ 分钟无子任务，Y/Z 后发先至）→ 作废 |
| **Y** | `2oiouWgp45hBcwESGWvP5qA` | prod 破墙 10 杠杆 | **完成，出 1 条零 FAIL（leAjP90e）** |
| **Z** | `21gT0D7xE4AVcGPnra8VtMG` | MODEL 塔 10 模板 | 在飞 |
| **AA** | `16lrHDeJr4zlbGO16fD88yvY` | fundamental23 低拥挤字段扫 | 在飞 |

---

## 7. 下一步优先级

1. **prod 取真值**：leAjP90e（权重平滑变体，最可能破墙）→ xArjWXNp → N1N73kRw。`correlation_busy` 不是判死依据。
2. **MODEL 塔**（Z 批）：1010 字段中 517 个近乎零拥挤，是 prod 天然去相关的方向。
3. **低拥挤字段扫**（AA 批）：把 `ebit/assets` 换成 aC≤100 的字段，直接切掉 prod 钉子的来源。
4. **会计质量机制**（AB 批，已预检）：fundamental44，Sloan 应计 / Beneish M / 重述概率，与 ROA 改善完全不同的经济学。
5. 攒够候选后按塔归因，凑齐 20 个 REGULAR alpha。

---

## 8. 批 AA 决定性负结果（2026-11-03）—— 「换低拥挤字段破 prod」在信号层就断了

批 AA（`16lrHDeJr4zlbGO16fD88yvY`）把已证零 FAIL 的几何 `rank(ts_decay_linear(ts_delta(ts_zscore(X,252),252),5))` 原封不动地套到 fundamental23 里 10 个 aC≤100 的低拥挤字段上：

| 字段（aC） | S | 2Y | 判定 |
|---|---:|---:|---|
| `fnd23_fcff/assets`(78) | 0.22 | 1.65 | 全灭 |
| `fnd23_fcff`(78) | 0.38 | 1.56 | 全灭 |
| `fnd23_crta`(74) | −0.32 | 0.18 | 反向 |
| `fnd23_cpca`(50) | −0.51 | −0.90 | 反向 |
| `retained_earnings_liabilities/assets`(7) | −0.23 | −0.09 | 反向 |
| `long_term_debt_total/assets`(7) | −0.73 | 0.07 | 反向 |
| `total_current_assets_4/assets`(10) | −0.34 | −0.45 | 反向 |
| `fnd23_fcis/assets`(93) | −0.65 | −1.58 | 反向 |
| `fnd23_dttl/assets`(94) | 0.18 | 0.37 | 全灭 |
| `long_term_contract_liabilities/assets`(5) | −0.45 | −1.46 | 反向 |

**10/10 全灭，|S| ≤ 0.73。** 对照：同几何下 `ebit/assets` S 2.29、`ebit/sales` S 2.06。

### 结论（本轮最重要的一条）

1. **信号只住在盈利比率里，不住在「同类但低拥挤」的字段里。** 自由现金流、资本支出强度、流动比率、留存收益、长期杠杆、流动资产、投资现金流、总债务、长期合约负债 —— 换成这些字段后结构还在、秩序全无。`ebit/assets` 的 aC=6064 不是偶然：**它拥挤，正是因为它有信号。拥挤度与信号强度是同一枚硬币的两面。**
2. **「字段替换」不是破 prod 的杠杆**，它是「换机制」。换机制就必须重新验证有没有信号，不能假定同族可迁移。
3. 破 prod 必须走**真正换机制**（MODEL/OTHER 塔的模型预测、会计质量、新闻情绪），或换**包装**（权重形状 / universe / 中性化），而不是换字段。

### 对照：prod 的族级判据（技能 `wq-prod-corr-read` §四·1）

`bl6jJRKp` prod **0.8576 > 0.80** ⇒ ROA 改善这一族**族级撞墙**。同族的 `N1N73kRw`（同字段、zscore 窗口 504）、`leAjP90e`（同字段、加 5 日权重平滑）、`xArjWXNp`（`ebit/sales`）**不再消耗 prod 时隙**——逐颗去测属于明确的反模式。既有候选留档，量产计划转向其它族。
---

## 10. 第二批：跨 category 扫荡（AH–AN）

前 13 批只覆盖 fundamental / model / other 三个 category，而 ASI 共 **16 个 category**。本轮先补全地形再横扫。

### 10.1 ASI 数据集地形（158 个，按 category）

| category | 数据集数 | category | 数据集数 |
|---|---:|---|---:|
| model | 41 | news | 22 |
| other | 27 | pv | 19 |
| analyst | 13 | fundamental | 11 |
| sentiment | 7 | socialmedia | 5 |
| risk | 4 | institutions | 2 |
| insiders | 2 | broker / earnings / imbalance / macro / shortinterest | 各 1 |

**十年满覆盖（cov ≥ 0.93）的可挖池只有 12 个**：`macro63`(1.0) / `institutions6`(1.0) / `insiders5`(0.9991) / `risk68`(0.989) / `shortinterest5`(0.9624) / `news_sentiment_transfer`(0.9592) / `news59`(0.9585) / `socialmedia39`(0.9414) / `risk60`(0.9389) / `dl_riskfree_returns`(1.0) / `chart_cnn_alpha`(0.953) / `multi_source_model`(0.951)。

### 10.2 按 category 的判死清单（本轮新增）

| 数据集 | 塔 | 最优 S | 判定 | 依据 |
|---|---|---:|---|---|
| `fund_holdings_panel` | institutions | 1.11 | **判死** | 10 模板全弱，HHI/账户数/信心持仓均无信号 |
| `news_sentiment_transfer` | sentiment | 0.55 | **判死** | 10 模板 |S|<0.6，换手 40–75% 爆表；再次验证 NEWS 系天花板 ~0.9 |
| `shortinterest5` 涨跌停 | shortinterest | **0.00** | **判死** | 10/10 Sharpe=0、turnover=0 —— 涨跌幅限制是**截面常数**（多为 10%），经 SLOW 中性化后被完全抹平 |
| `insiders5` | insiders | — | **排除** | 全数据集唯一字段 `insd5_nm_kor` 是内部人**韩文姓名**，纯文本属性 |
| `analyst` 全 category（13 个） | analyst | — | **整类排除** | 覆盖最高仅 `analyst39` 0.798（`analyst4` 0.603），**无一满足十年满覆盖硬要求** |
| `macro63` | macro | — | 低优先 | 只有 1 个 `mcr63_membership` 会员标记，机制单薄 |

### 10.3 `institutions6`（13F 机构持仓）：方向不对称的重要发现

11 个 MATRIX 字段、**cov 1.0**、aC 137–330、属 institutions（非禁混集合，纯 ATOM）。批 AJ 十模板实测：

| 口径 | 表达式骨架 | S | 判定 |
|---|---|---:|---|
| **家数差取反** | `group_rank(multiply(-1, ts_mean(subtract(buyers, sellers), 63)), subindustry)` | **1.17** | 最优（sub 1.01、sub/S 0.86 健康） |
| 股数差取反 | `group_rank(multiply(-1, ts_mean(subtract(qty_acq, qty_dis), W)), industry)` | −0.74 / −0.78 / −0.13 | **取反后为负 ⇒ 股数差本身是正向动量** |
| 反转×拥挤 | `... × ts_rank(holders, 252)` | −0.38 | 不成立 |
| 门控 / 非线性 / 期限差 | — | −0.49 / 0.38 / 0.26 | 均弱 |

**结论（可复用的机制判读）**：
1. **家数口径（多少家机构在买）= 拥挤反转信号（负向）** —— 与论坛帖「共同基金拥挤反转」独立吻合；
2. **股数口径（买了多少股）= 聪明钱动量信号（正向）** —— 两者方向相反，**不可混用同一符号**；
3. 论坛实证的「股数差优于市值差」（市值被价格污染，APAC 0.23→1.23）在 ASI 成立，但**必须不取反**；
4. 天花板 1.17，仍差 LOW_SHARPE 1.58 门槛 0.41，**整族暂判不足**，但方向信息已锁定。

### 10.4 ROA 族 prod 墙的最终确认

`N1N73kRw`（同字段、内层 zscore 窗口 252→504）prod = **0.857**，与 `bl6jJRKp` 的 0.8576 几乎相同。
⇒ **换窗口不改变 prod**，ROA 改善的 0.857 是机制级常数，整族封盘。

同时确认 `bl6jJRKp` 的 `checks.fail = []`：robust 双闸、JPN、2Y、sub、CONCENTRATED_WEIGHT 全 PASS，**唯一障碍就是 prod**。

### 10.5 新机会：`probability_label` 族取反

批 AE 十模板里 `probability_label*` 系列全部为**负 Sharpe**：`probability_label0_4quantile_60day_ohlcv` −1.71、`probability_label1_3quantile_5day_ohlcv_2` −1.61、`probability_label1_3quantile_60day_ohlcv` −0.95。

关键：这些字段 **aC 仅 9–29**（对照 `quantile_label_1bucket_20day_ohlcv` aC=810）。低拥挤度意味着 prod 大概率低，而取反后 S 已达 1.71。
⇒ 批 AN 用 10 个结构互异模板系统验证该族（不同期限/分位 × 平滑/zscore/衰减/zscore立方/时序分位/一阶差分/期限差 × sector/industry/country/subindustry）。

**为什么这条特别值得试**：S 1.71 时 robust 闸只需 ≥1.54，远比 S 5.11 时要求 4.60 容易过；两个历史障碍（prod、robust）同时被绕开的可能性最高。

### 10.6 本轮在飞与待办

- 批 AM：`1g5Xzqbf05arc7VPVYsT0Z6` —— ROA 核心 10 变体搬到 **MINVOL10M**（universe 正交杠杆破 prod；已验证 `ebit`/`assets` 在 MINVOL10M 可用、TOP3000 不可用）
- 批 AN：`3EasdV8NM4kpaDHhDZdTcRD` —— `probability_label` 取反 10 模板
- 环境瓶颈：仿真队列拥堵（AH/AJ 曾连续 15+ 分钟 `child_count=0`）、prod 端点账号级单并发 + MCP 120s 硬超时、后台 peek 长期「空体」


## 11. 绗笁鎵癸細RISK 濉斿垽姝?+ CROWDING 涓€у寲鐮?JPN锛?026-11-03 缁級

### 11.1 RISK 濉斿湪 ASI 鏃犳硶鐐逛寒锛? 涓暟鎹泦鍏ㄥ簾锛?
| 鏁版嵁闆?| 鍚嶇О | 瀛楁 | 瀹炴祴 |
|---|---|---|---|
| risk68 | "Forecast Data" | rsk68_beta / residual_return / weight_*锛?锛孧ATRIX锛?| 10 鏉″叏 ERROR |
| risk60 | "Securities Lending Insight" | rsk60_offer / crowding / last / lending_fee_bid_rate锛?锛孷ECTOR锛?| 10 鏉″叏 ERROR |
| risk70 | "Multi-Factor Model" | 79 瀛楁锛宑ov 0.9015锛宎C 47891 | 鍏冩暟鎹敊浣嶏紝鏈淳 |
| risk72 | "Specific return of extended factors" | 8 瀛楁锛宑ov 0.453 | 涓嶆弧瓒冲崄骞磋鐩?|

**鍒ゅ埆娉曪紙鏂板锛岄浂鎴愭湰锛?*锛歚get_datasets` 杩斿洖鐨?`name`/`description` 涓庡疄闄呭瓧娈靛唴瀹?*閿欎綅** 鈬?璇ユ暟鎹泦鍦ㄦ湰鍖哄彧鏄洰褰曞崰浣嶃€佹棤鐪熷疄鏁版嵁锛屾淳鍙戝繀鐒跺叏鎵?ERROR銆?瀹炰緥锛歳isk68 鍚?Forecast Data"銆佹弿杩拌璁㈠崟绨?tick-level锛屽瓧娈靛嵈鏄?beta 涓庢畫宸紱risk60 鎻忚堪璁?RIC/BBID 鏄犲皠锛屽瓧娈靛嵈鏄€熻捶璐圭巼锛況isk70 鎻忚堪璁叉満鏋勬寔浠擄紝瀛楁鍗存槸澶氬洜瀛愭ā鍨嬨€?鍙﹁瘉锛歚rsk68_beta` 瀛楁鎻忚堪鍐欑潃 "for a **European** asset" 鈥斺€?EUR 鏁版嵁闆嗕覆鍒颁簡 ASI 鐩綍銆?**鈬?RISK 濉旓紙ASI 4 涓暟鎹泦锛夋暣浣撴斁寮冿紝璇ュ鏈尯鏃犳硶鐐逛寒銆?*

### 11.2 鈽?CROWDING 涓€у寲鏄?ASI JPN 闂哥殑瑙ｈ嵂

姝ゅ墠 `SLOW` 涓€у寲涓嬶紝JPN 闂革紙`LOW_ASI_JPN_SHARPE` 闇€ 鈮?锛夋槸鍑犱箮蹇呮寕鐨勭粨鏋勬€у銆傛崲 `CROWDING` 鍚庯細

| 琛ㄨ揪寮忥紙CROWDING / decay4 / trunc0.08 / MINVOL1M锛?| S | F | TO | 2Y | sub | fail | JPN |
|---|---:|---:|---:|---:|---:|---:|---|
| `group_rank(quantile_label_1bucket_20day_ohlcv, country)` 鈫?**bl6RqkrR** | **4.12** | 3.70 | 17.7% | 4.74 | 3.27 | **2** | **PASS** |
| `group_rank(quantile_label_1bucket_60day_ohlcv, country)` 鈫?O0ArZYMd | 3.24 | 2.72 | 17.2% | 3.91 | 2.58 | 2 | PASS |
| `group_rank(quantile_label_5bucket_60day_ohlcv_2, country)` 鈫?e7590pGg | 2.69 | 1.89 | 18.4% | 3.11 | 2.26 | 2 | PASS |

涓夋潯**鍙寕 robust 鍙岄椄**锛坄LOW_ROBUST_UNIVERSE_SHARPE.WITH_RATIO` + `LOW_ROBUST_UNIVERSE_RETURNS`锛夛紝宸窛 0.8%鈥?%銆?**鍚屾壒 probability_label 鏃忓湪 CROWDING 涓嬮泦浣撳穿婧?*锛?.23 / 1.37 / 鈭?.36 / 鈭?.57 / 鈭?.52锛夆噿 涓€у寲涓庡瓧娈垫棌寮鸿€﹀悎锛屼笉鑳借法鏃忕収鎼€?
**CROWDING 涓嶅吋瀹圭函 fundamental**锛歊OA 鏃忥紙`divide(ebit, assets)`锛?0 鏉″叏 ERROR 鈬?鎷ユ尋搴︽暈鍙ｉ渶瑕佷环鏍肩被鏁版嵁鎵嶈兘绠椼€?
### 11.3 鈽呪槄 prod 涓?Sharpe 鍗曡皟鍙嶅悜锛堟湰杞渶閲嶈鐨勫彲澶嶇敤瑙勫緥锛?
| alpha | 淇″彿 | S | prod |
|---|---|---:|---:|
| bl6RqkrR | quantile_1bucket_20day | **4.12** | **0.8062** |
| O0ArZYMd | quantile_1bucket_60day | 3.24 | 0.8393 |
| wpQY5221 | probability_1_4quantile_60day (SLOW) | 2.84 | 0.8643 |
| e7590pGg | quantile_5bucket_60day_2 | 2.69 | 0.9051 |

**瑙勫緥**锛氬悓涓€鏁版嵁闆嗗唴锛屼俊鍙疯秺寮?鈬?prod 瓒婁綆銆傛満鍒讹細寮变俊鍙蜂俊鍣瘮浣庯紝PnL 鏇村鏄撹鐢熶骇姹犻噷鐨勫叕鍏卞洜瀛愶紙瀹藉熀鍔ㄩ噺/鍙嶈浆锛夎В閲婏紱寮轰俊鍙锋惡甯︾嫭绔?alpha 鎴愬垎銆?**搴旂敤**锛氭敾 prod 涓嶈鍦?*寮?*鍊欓€変笂纾紝鎸?*鏈€楂?S** 鐨勯偅棰楋紱S 4+ 绔?prod 宸查檷鍒?0.81锛屾槸绂?0.70 鏈€杩戠殑璧风偣銆?
### 11.4 prod 鐩存柟鍥鹃璇伙紙e7590pGg锛岄棬妲?0.70锛?
140 涓囨潯鐢熶骇 alpha 鐨勭浉鍏崇郴鏁板垎甯冿細`[0.6,0.7]` 浠?106 鏉°€乣[0.7,0.8]` 10 鏉°€乣[0.8,0.9]` 1 鏉°€乣[0.9,1]` 1 鏉★紱max 0.9051銆乵in 鈭?.5811銆?鈬?**0.70 闃堝€兼湰韬彲杈?*锛?9.99% 鐨勭敓浜?alpha 閮藉湪 0.7 浠ヤ笅锛夛紝鍗′綇鎴戠殑鏄瀬灏戞暟 1鈥?0 鏉￠珮搴﹂噸鍚堢殑鐢熶骇 alpha锛岃€岄潪"ASI 姹犳暣浣撳お鎸?銆?
### 11.5 universe 鏉犳潌褰诲簳灏佹

`multi_source_model` 涓?`dl_riskfree_returns` 閮?*鍙?*瀛樺湪浜?MINVOL1M / MINVOL10M锛?- TOP3000 / TOP1200 / TOP600 鈫?`unknown_fields`
- MINVOL10M 鈫?浠跨湡鎭掑崱 `progress 0.15锝?.35`銆乣child_count=0`锛屼粠鏈畬鎴愶紙鎵?AM / AP / AQ / AS / AX 浜旀澶嶇幇锛?
鈬?"鎹?universe 鐮?prod"锛圗UR 宸查獙璇佹湁鏁堢殑姝ｄ氦鏉犳潌锛夊湪 ASI **涓嶅彲鐢?*銆?
### 11.6 MODEL 濉?multi_source_model 鐨勬棌绾т笁闂稿

country 鍒嗙粍閲嶈瘯鍚庡嚭鏁版瀬寮猴紝浣嗗洓鏉″叏閮ㄥ彧鎸?*鍚屼竴缁勪笁闂?*锛?
| alpha | 琛ㄨ揪寮?| S | JPN | robust ratio | robust ret | fail |
|---|---|---:|---|---|---|---:|
| xArYRWLN | `group_rank(short_term_regime4_quantile1_5d_pred, country)` | 3.24 | 0.70 | 2.14<2.92 | 0.0349<0.0467 | 3 |
| LLM9krv1 | `group_rank(short_term_seasonal_quantile1_5d_pred, subindustry)` | 3.01 | 0.63 | 2.06<2.71 | 0.0326<0.042 | 3 |
| P0oZv8RK | `group_rank(ts_rank(short_term_quantile1_20d_pred, 66), country)` | 2.74 | 0.54 | 1.87<2.47 | 0.0305<0.0393 | 3 |
| N1NQA3dX | `group_rank(long_term_quantile1_120d_pred, country)` | 2.25 | 0.85 | 1.70<2.02 | 0.025<0.0289 | 3 |

robust ratio 鎭掍负 `0.66鈥?.76 脳 S`锛岄棬妲涙亽涓?`0.90 脳 S` 鈬?**鎶?S 鏃犳晥**锛屽繀椤昏澶хエ瀛愰泦鐩稿鍙樺己銆傝繖鍥涙潯棰勬祴淇″彿浣忓湪寰洏绔€?
### 11.7 鏂板垽姝绘竻鍗?
| 鏁版嵁闆?| 濉?| 鍒ゆ嵁 |
|---|---|---|
| news59 | news | 浠?2 涓簨浠跺厓鏁版嵁瀛楁锛堣储骞淬€佷簨浠舵椂闂达級锛屾棤鏁板€间俊鍙?|
| socialmedia39 | socialmedia | 浠?1 涓叡瑙?ticker ID 鍒楄〃瀛楁 |
| risk68 / risk60 / risk70 / risk72 | risk | 瑙?11.1锛屾暣濉旀湰鍖烘棤鏁版嵁 |
| fundamental23 脳 CROWDING | fundamental | CROWDING 涓庣函 fundamental 涓嶅吋瀹癸紝鍏ㄦ壒 ERROR |

### 11.8 褰撳墠鏈€浼樺€欓€夋帓搴忥紙鎸?绂诲彲鎻愪氦璺濈"锛?
1. **bl6RqkrR** 鈥?S 4.12 / fail 2锛坮obust ratio 宸?6.7%銆乺obust ret 宸?7.3%锛? **prod 0.8062** 鈫?鍞竴鍚屾椂楂?S 涓斾綆 prod
2. O0ArZYMd 鈥?S 3.24 / fail 2 / prod 0.8393
3. wpQY5221 鈥?S 2.84 / **fail 0** / prod 0.8643
4. e7590pGg 鈥?S 2.69 / fail 2锛堜粎宸?0.8% / 2.4%锛? prod 0.9051
5. bl6jJRKp锛圧OA锛夆€?S 2.29 / **fail 0** / prod 0.8576锛堟棌绾у皝鐩橈級


---

## 12. 杞悜闈炰环鏍间俊鍙凤細琛屼负閲戣瀺 / 鎶€鏈寚鏍?/ 鏂伴椈鎯呯华涓夋潯鏂扮嚎锛?026-11-04 缁級

### 12.1 鎴樼暐鍒ゆ柇锛歱rod 澧欐槸缁撴瀯鎬х殑锛屽繀椤绘崲銆岄潪浠锋牸娲剧敓銆嶆暟鎹?
绗?8 鑺傚凡纭 prod 涓?Sharpe 鍗曡皟鍙嶅悜銆佸湴鏉?鈮?.75銆傛湰鑺傜殑鎺ㄨ锛?*鍦版澘鏈韩鐢辨暟鎹€ц川鍐冲畾**銆?`dl_riskfree_returns` 鐨勬弿杩版槸"鐢ㄩ噺浠峰簭鍒楄浆 2D 鍥俱€侀璁粌 CNN 棰勬祴 risk-free returns" 鈬?瀹冩槸**浠锋牸鐨勫啀缂栫爜**锛?涓庣敓浜ф睜锛堝悓鏍蜂互浠锋牸 alpha 涓轰富浣擄級澶╃劧楂樺害鐩稿叧銆?*鍦ㄥ悓涓€绫讳环鏍兼淳鐢熸暟鎹噷鎹㈠嚑浣曪紝prob 鍦版澘涓嶄細鍔ㄣ€?*

鈬?**瑕佽繃 prod 0.70锛屽繀椤绘崲鎴?淇℃伅涓嶆槸浠庝环鏍兼帹鍑烘潵鐨?鏁版嵁闆?*銆傛嵁姝ら噸鎺?ASI 158 涓暟鎹泦鐨勪紭鍏堢骇銆?
### 12.2 ASI 鏁版嵁闆嗗叏閲忕洏鐐癸紙158 涓紝鎸?category锛?
| category | 鏁版嵁闆嗘暟 | cov鈮?.9 | 鏈€楂樿鐩?| 鏈垬褰圭姸鎬?|
|---|---:|---:|---|---|
| model | 41 | **15** | ai_factor_transfer / analyst_earnings_ibes (cov 1.000) | 浠呰瘯杩?multi_source_model |
| other | 27 | 2 | dl_riskfree_returns (1.000) | 宸插垽涓嶅彲鎻愪氦 |
| news | 22 | 1 | news59 (0.9585) | 浠呰瘯杩?news59(姝? / sentiment_transfer |
| pv | 19 | **9** | continuation_score / pattern_scores / pv1 (1.000) | **瀹屽叏鏈祴** |
| analyst | 13 | 0 | analyst69 (0.8154) | 13 涓叏涓嶆弧瓒冲崄骞磋鐩?|
| fundamental | 11 | 0 | fundamental44 (0.875) | 浠?fundamental23 ROA 鏃?|
| sentiment | 7 | 1 | news_sentiment_transfer (0.9592) | 浠?sentiment_transfer |
| socialmedia | 5 | 1 | socialmedia39 (0.9414) | 鍒ゆ |
| risk | 4 | 3 | risk68 (0.989) | 鏁村鏃犳暟鎹?|
| institutions | 2 | 1 | institutions6 (0.9991) | 鍒ゆ |
| insiders | 2 | 1 | insiders5 (0.9991) | 鍒ゆ |
| macro / earnings / imbalance / shortinterest / broker | 鍚?1 | 鈥?| 鍧囧垽姝绘垨瑕嗙洊涓嶈冻 | 鈥?|

**鏂板闆舵垚鏈帓闄わ紙鏈疆瀹炴祴瀛楁锛?*锛?
| 鏁版嵁闆?| 缁撹 |
|---|---|
| `pv149` (cov 1.0, aC 31, 1 瀛楁) | 鍞竴瀛楁鏄?`pv149_status_5` **鐘舵€佺爜**锛屾棤淇″彿 |
| `univ1` (cov 1.0, 3 瀛楁) | 涓変釜瀛楁鍏ㄦ槸 **universe 瀹氫箟**锛坢invol1m/minvol10m/top500锛夛紝闈炰俊鍙?|
| `analyst_earnings_ibes` (model, cov 1.0, 28 瀛楁) | 瀛楁鍏ㄦ槸 OHLCV 鍘熷浠烽噺锛坉lr1=Americas / dlr2=Europe锛夛紝**绾环鏍?*锛屽悕瀛楀甫 analyst 浣嗘棤鍒嗘瀽甯堝唴瀹?|
| `behavioral_signals` | 瀛楁鐪熷疄浣嗕俊鍙峰急锛堣 12.3锛?|

### 12.3 behavioral_signals锛圡ODEL 濉旓級鈥斺€斿瓧娈电湡瀹炪€佷俊鍙峰亸寮?
7 涓?VECTOR 瀛楁锛宑ov 0.88锛?*aC 浠?2鈥?4锛圓SI 鏈€涓嶆嫢鎸ゆ棌涔嬩竴锛?*锛屽唴瀹规槸鐪熻涓洪噾铻嶆瀯閫狅細
`salience_weighted_return_score`(aC7, 鏄捐憲鎬х悊璁? / `extreme_daily_return_indicator`(aC4, 褰╃エ鍋忓ソ)
/ `price_path_curvature_measure`(aC10, 璺緞鍑告€? / `consecutive_return_streak_length`(aC24, 杩炴定)
/ `chronological_return_sequence_correlation`(aC10) / `visual_price_path_shape_score`(aC9)
/ `total_equity_market_value_usd`(aC2, 甯傚€尖€斺€?*鏁版嵁闆嗗唴鑷甫甯傚€艰酱**)

鎵?BG锛坄RbAEh5Cd4ZI8BV19GIOfryG`锛孲LOW/decay4/MINVOL1M锛? 鏉″叏 COMPLETE銆? error锛夛細

| alpha | 琛ㄨ揪寮?| S | F | TO | 2Y |
|---|---|---:|---:|---:|---:|
| 9qxVjeXe | `multiply(-1, group_rank(vec_avg(salience_weighted_return_score), country))` | **鈭?.70** | 鈭?.18 | 20.2% | 0.00 |
| ZYQ0b80Y | `multiply(-1, group_rank(vec_avg(extreme_daily_return_indicator), country))` | **鈭?.64** | 鈭?.16 | 21.1% | 鈭?.22 |
| KPJONoOj | `group_rank(vec_avg(price_path_curvature_measure), country)` | 0.49 | 0.10 | 27.0% | 0.25 |

**绗﹀彿缁撹锛堟瘮鏁板€兼洿鏈夌敤锛?*锛氭樉钁楁€х悊璁哄彇鍙嶅悗涓鸿礋 鈬?**姝ｅ悜鎵嶆槸瀵圭殑鏂瑰悜**锛?0.70锛夛紱褰╃エ鍋忓ソ鍚岀悊锛?0.64锛夈€?杩欎笌 Bali(2011) MAX 鏁堝簲锛堜綆 MAX 鑲¤窇璧級**鐩稿弽**锛岃鏄?ASI/MINVOL1M 鐨勫皬甯傚€煎煙閲屽姩閲忎负鐜嬨€佸僵绁ㄦ孩浠蜂笉鎴愮珛銆?**鍒?*锛氬崟瀛楁寮哄害 `|S| 鈮?0.5鈥?.7`锛屼笉瓒充互鍗曠嫭杩囬椄锛岄渶缁勫悎鎴栨崲鐭┿€?**鐣欑敤鐐?*锛氭暟鎹泦鑷甫 `total_equity_market_value_usd`锛圡ODEL 濉斿唴锛夛紝鍙负 robust-universe 闂告彁渚?*涓嶅紩鍏?PV 濉?*鐨勫競鍊艰酱銆?
### 12.4 news38 / news7 鈥斺€?鏈疆鏈€楂樹环鍊肩殑鏈祴绾跨储

**涓轰粈涔堟渶楂樹环鍊?*锛氭柊闂绘儏缁俊鎭?*涓嶆槸浠庝环鏍兼帹鍑烘潵鐨?*锛屼笌鐢熶骇姹犵殑鍏叡鍥犲瓙缁撴瀯鎬ф浜?鈬?鍗充究 S 鍙湁 1.5鈥?.5锛?prod 涔熷彲鑳借惤鍦?0.3鈥?.6锛堝姣斾环鏍兼淳鐢熸棌鍦版澘 0.75锛夈€傝繖鏄敮涓€鑳藉悓鏃舵弧瓒炽€屼綆 S 涔熻兘鎻愪氦銆嶇殑璺緞銆?
| 鏁版嵁闆?| 鍏抽敭瀛楁 | 绫诲瀷 | cov | aC |
|---|---|---|---:|---:|
| news38 | `mws38_tone_score` | VECTOR | 0.91 | 41 |
| news38 | `mws38_positive_score` / `mws38_negative_score` | VECTOR | 0.91 | 62 / 50 |
| news38 | `mws38_tc_tone_score` / `tc_positive_score` / `tc_negative_score` | VECTOR | 0.91 | 55 / 47 / 34 |
| news38 | `mws38_positive_freq` / `mws38_negative_freq` | VECTOR | 0.91 | 22 / 20 |
| news38 | `mws38_score`锛堟渶鎷ユ尋锛? `mws38_d1_related_num` | VECTOR | 0.92/0.91 | 325 / 44 |
| news38 | `story_analytics_metric_value` / `market_impact_indicator` | VECTOR | 0.82 / 0.58 | 8 / 2 |
| news7 | `headline_overall_tone_score_2` | **MATRIX** | 0.84 | **22** |
| news7 | `headline_positive_tone_score_2` | **MATRIX** | 0.84 | **15** |
| news7 | `headline_positive_mention_count_2` | MATRIX | 0.84 | **9** |
| news7 | `headline_mention_count_2`锛堟渶鎷ユ尋锛?| MATRIX | 0.84 | 893 |
| news7 | `news_mention_frequency_d0` / `_twn` | MATRIX | 0.94 | 16 / 12 |
| news7 | `nws7_news_freq_qerf` / `nws7_newsfreq_1_d1_qerf` | MATRIX | 0.80 | 10 / 11 |

**娉?*锛歚news7` 鏈?MATRIX 瀛楁锛堝厤 vec 绠楀瓙锛変笖 aC 9鈥?2 鏋佷笉鎷ユ尋锛屾瘮 news38 鏇存槗缁勮銆?**鏂伴椈鏁版嵁绋€鐤?* 鈬?蹇呴』 `ts_backfill(x, 120)` 鍓嶅悜濉厖锛屽惁鍒?NaN 鎺夋牱鏈鑷?LOW_COVERAGE銆?
鎵?BH锛坄3yBiul7Ih50ebLL1hfhdJGn7`锛夐鎺?3 鏉★細鎯呯华**姘村钩** / 鎯呯华**涓€闃跺樊鍒?22d)** / news7 姝ｉ潰璇嶅崰姣?鈥斺€?瑕嗙洊"姘村钩路鍙樺寲路璺ㄦ暟鎹泦"涓夌鐭╋紝缁撴灉寰呮敹銆?
### 12.5 ai_factor_transfer锛圡ODEL 濉旓紝cov 1.000锛?0 MATRIX锛宎C 17鈥?6锛夆€斺€斿鐢ㄧ嚎

20 涓粡鍏告妧鏈寚鏍囷紙鍏ㄩ儴 cov 1.0锛夛細`typical_price_bollinger_band_position`(aC19) / `momentum_williams_r_adjusted_2`(aC17)
/ `volume_anomaly_price_positioning_2`(aC17) / `liquidity_weighted_returns_ma_2`(aC23) / `balanced_price_oscillator_2`(aC33)
/ `volume_trend_money_flow_interaction_2`(aC58) / `money_flow_strength_typical_price`(aC36) 绛夈€?**椋庨櫓**锛氱函浠锋牸娲剧敓 鈬?prod 棰勬湡浠嶉珮锛堜笌 dl_riskfree 鍚屾€ц川锛夛紝鍙湪鏂伴椈绾垮け璐ュ悗浣滀负琛ヤ綅銆?**娉ㄦ剰**锛氳鏁版嵁闆?name鈫攄escription 瀛樺湪閿欎綅锛堝 `cumulative_money_flow_volume_adjusted` 鎻忚堪鍐欐垚 "Relative Strength (RSI)"锛夛紝
浣?aC 17鈥?6 涓?cov 1.0 鈬?灞?*鐪熷疄鏁版嵁 + 鎻忚堪鏍囨敞閿欎贡**锛屼笉鍚屼簬 risk68 閭ｇ銆屾湁鐩綍鏃犳暟鎹€嶃€?
### 12.6 鏈疆杩愮淮鏁欒锛堟柊澧烇級

1. **`harvest_multisim_alphas` 鐨勫弬鏁板悕鏄?`multisimulation_location`锛圲RL锛夛紝涓嶆槸 `multisimulation_id`**锛涗紶閿欎細 PTC_ARGUMENT_VALIDATION_FAILED銆?2. **`batch_status` 鐨?`child_count` 闀挎湡涓?0 鏃讹紝鏀圭敤 `lookINTO_SimError_message` 鐪嬬埗鎵?`raw.progress`**锛?   progress 宸插埌 0.9/1.0 涓?status=COMPLETE 鈬?鐖舵壒鍏跺疄璺戝畬浜嗭紝鍙槸 batch_status 娌℃寕涓婂瓙鑺傜偣锛?*鐩存帴 harvest 鍗冲彲鎷垮洖 alpha**銆?   鏈疆 BE 鎵癸紙progress 0.90 鍗℃锛変笌 BG 鎵癸紙status COMPLETE 浣?child_count 0锛夐兘鏄繖涓幇璞°€?3. **鍗℃鎵规鐨勫垽姝讳笌閲婃斁**锛欱E 涓?BF 鍧囬暱鏃堕棿 progress 涓嶅啀鍙樺寲涓?child_count=0 鈬?`DELETE /simulations/{id}` 杩斿洖 200 閲婃斁妲戒綅鍚庨噸娲俱€?   BF锛圡INVOL10M锛夌 6 娆′粛鍗?0.15 鈬?**universe 鏉犳潌锛圡INVOL10M锛夋案涔呭叧闂?*銆?4. 鍗曚釜 run_code 绋嬪簭閲屾斁澶鏁版嵁澶勭悊浼氳Е鍙?`compute_budget_exceeded`锛屽彇鏁拌绮剧畝瀛楁銆?

---

## 13. 闈炰环鏍间笁鏉＄嚎鐨勫疄娴嬬粨鏋滐紙2026-11-04 缁級

### 13.1 鏂伴椈鎯呯华绾匡紙news38 / news7锛夆€斺€斿垽寮?
鎵?BH锛坄3yBiul7Ih50ebLL1hfhdJGn7`锛孲LOW/decay4/MINVOL1M锛? 鏉″叏 COMPLETE銆? error锛夛細

| alpha | 琛ㄨ揪寮?| S | F | TO | 2Y | sub |
|---|---|---:|---:|---:|---:|---:|
| e7596nmO | `group_rank(ts_backfill(vec_avg(mws38_tone_score), 120), country)` | **0.13** | 0.02 | 8.8% | 0.22 | 0.49 |
| npvKAn9a | `group_rank(ts_delta(ts_backfill(vec_avg(mws38_tone_score), 120), 22), country)` | **0.07** | 0.01 | 13.6% | 鈭?.18 | 0.56 |
| 2rAOjvM6 | `group_rank(ts_backfill(headline_positive_tone_score_2, 120), country)` | **0.42** | 0.14 | 6.1% | 0.30 | 0.67 |

**鍒?*锛氭柊闂?tone **姘村钩**涓?*涓€闃跺樊鍒?*閮借繎涔庨浂棰勬祴鍔涳紙0.13 / 0.07锛夛紝璺ㄦ暟鎹泦鐨勬璐熼潰璇嶅崰姣旓紙0.42锛夋槸鍚屾壒鏈€濂戒絾浠嶈繙涓嶅銆?**鍏抽敭鎯呮姤**锛歚get_alpha_details` 鏄剧ず ASI 鐨?`LOW_SHARPE` 闂ㄦ鏄?**1.58**锛堜笉鏄父瑙佺殑 1.25锛夈€乣LOW_2Y_SHARPE` 涔熸槸 **1.58**
鈬?**ASI 鏄竴涓珮 Sharpe 闂ㄦ鍖?*锛屽急淇″彿鍦?ASI 娌℃湁鐢熷瓨绌洪棿銆傝繖瑙ｉ噴浜嗕负浠€涔堜綆 S 鐨勯潪浠锋牸鏁版嵁鍏ㄩ儴涓嶅彲鐢ㄣ€?`ts_backfill(120)` 涓嶄細鎺╃洊淇″彿鏂瑰悜锛堜笁鏉￠兘鍋氳繃濉厖锛夛紝鎵€浠ヤ笉鏄澶勭悊闂锛屾槸淇″彿鏈韩涓嶅瓨鍦ㄣ€?**缁撹**锛歯ews38/news7 鎯呯华鏃忓湪 ASI/MINVOL1M **鍒ゅ急**锛岄櫎闈炴壘鍒板ぇ骞呮彁楂樺己搴︾殑缁勮鏂瑰紡锛屽惁鍒欎笉鍐嶆姇鍏ャ€?
### 13.2 浼氳鍙栬瘉绾匡紙fundamental44锛夆€斺€斾俊鍙峰急銆侀€愬勾涓嶇ǔ銆佺鍙峰弽鐩磋

**鏁版嵁闆嗚祫璐紙浼樹簬缁濆ぇ澶氭暟 ASI 鏁版嵁闆嗭級**锛?2 涓?MATRIX 瀛楁銆乧ov 0.875銆?*2014鈥?023 閫愬勾 longCount 1800鈥?400 涓?pnl鈮?锛堝崄骞存弧瑕嗙洊锛屾弧瓒崇敤鎴风 4 鏉＄‖瑕佹眰锛?*銆?瀛楁鏄函浼氳鍙栬瘉鏋勯€狅紝淇℃伅**涓嶄粠浠锋牸鎺ㄥ嚭**锛歋loan 搴旇锛坄fnd44_cashflow_accruals` aC113 / `fnd44_perc_accruals` aC128
/ `fnd44_working_capital_accruals` aC264 / `fnd44_yoon_wc_accruals` aC155锛夈€丅eneish M-Score锛坅C158锛夈€?Piotroski F-Score锛坅C113锛夈€丅enford 鑸炲紛鍒嗭紙aC226锛夈€丣ones / Modified-Jones 搴旇锛坅C70/71锛夈€?閲嶈堪姒傜巼锛坅C108 / `_global` aC165锛夈€佺患鍚堝垎锛坅C121锛夈€?
鎵?BJ锛坄1GmsTz5Q54wLcGtsnR7zFk3`锛孲LOW/decay4锛夆€斺€?*姘村钩鍑犱綍**锛?
| alpha | 琛ㄨ揪寮?| S | F | TO | 2Y |
|---|---|---:|---:|---:|---:|
| gJeQeG0M | `multiply(-1, group_rank(fnd44_cashflow_accruals, country))` | **鈭?.18** | 鈭?.06 | 15.1% | 0.79 |
| MPY1Yz26 | `multiply(-1, group_rank(fnd44_mscore, country))` | **0.33** | 0.16 | 15.5% | 0.42 |
| kqNVNGYO | `group_rank(fnd44_fscore, country)` | **鈭?.40** | 鈭?.21 | 15.3% | 鈭?.49 |

**涓変釜鍙嶇洿瑙夌粨璁猴紙閮芥槸鏈変环鍊肩殑璐熷悜鎯呮姤锛?*锛?1. **Sloan 搴旇寮傝薄鍦?ASI 涓嶆垚绔?*锛氬彇鍙嶅悗浠嶄负 鈭?.18 鈬?姝ｅ悜鎵嶆湁 +0.18锛屽嵆銆岄珮搴旇 鈫?鍚庣画璺戣耽銆嶏紝涓?Sloan(1996)銆岄珮搴旇璺戣緭銆?*绗﹀彿鐩稿弽**銆?2. **Beneish M-Score 鏂瑰悜瀵逛絾澶急**锛氬彇鍙嶅悗 +0.33锛堢鍚?楂樻搷绾甸闄╁仛绌?锛夛紝寮哄害涓嶈冻闂ㄦ鐨?1/5銆?3. **Piotroski F-Score 绗﹀彿瀹屽叏鍙嶄簡**锛氭鍚?F-Score 寰?**鈭?.40** 鈬?鍦?ASI 灏忓競鍊煎煙**楂樿川閲忚窇杈?*锛岃川閲忓洜瀛愭槸鍙嶅悜鐨勩€?   杩欎笌 12.3 鑺?behavioral_signals 鐨勫僵绁ㄥ亸濂藉弽鍚戯紙楂?MAX 璺戣耽锛夊唴鍦ㄤ竴鑷达細**ASI/MINVOL1M 鏄?鍨冨溇鑲?momentum"鍩燂紝璐ㄩ噺/浣庨闄╁洜瀛愬弽鍚戝畾浠?*銆?
**閫愬勾绋冲畾鎬э紙gJeQeG0M锛?*锛? / 鈭?.15 / 鈭?.74 / 鈭?.25 / 鈭?.30 / 0.07 / 鈭?.58 / 鈭?.92 / 0.50 / 1.02 鈬?**绗﹀彿鍦ㄥ勾浠介棿缈昏浆锛屼笉鏄ǔ瀹氬紓璞?*銆?鍙﹀彂鐜?**2018 骞存崲鎵嬬巼浠?33% 鏂礀璺屽埌 3%**锛屾槸鏁版嵁渚涚粰/骞冲彴澶勭悊鐨勭粨鏋勬€ф柇鐐癸紝鍋氶暱绐楀彛鐮旂┒鏃跺繀椤婚伩寮€璺ㄦ柇鐐硅仛鍚堛€?
### 13.3 绱Н鍒ゆ/鍒ゅ急鐭╅樀锛堟埅鑷虫湰杞紝31 鎵?~240 鏉?ASI 鍥炴祴锛?
| 绾?| 鏁版嵁闆?| 鏈€濂界粨鏋?| 鍒?|
|---|---|---|---|
| 浠锋牸 ML | dl_riskfree_returns (OTHER) | **S 5.61 / F 4.10 / prod 0.7532** | 涓嶅彲鎻愪氦锛歳obust 鍙岄椄 + prod 鍦版澘 |
| 浠锋牸 ML | multi_source_model (MODEL) | S 3.24 | 涓嶅彲鎻愪氦锛欽PN + robust 涓夐椄 |
| 鎶€鏈寚鏍?| ai_factor_transfer (MODEL) | 鏈祴锛堝悓浠锋牸鎬ц川锛岄鏈熷悓 dl_riskfree锛?| 澶囩敤 |
| 琛屼负閲戣瀺 | behavioral_signals (MODEL) | S 0.70 | 鍒ゅ急 |
| 鏂伴椈鎯呯华 | news38 / news7 | S 0.42 | 鍒ゅ急 |
| 浼氳鍙栬瘉 | fundamental44 (FUNDAMENTAL) | S 0.33锛堢鍙峰鏁板弽鐩磋锛?| 鍒ゅ急锛堜絾瑕嗙洊鏈€浼樸€佸彲浣滅粍鍚堣吙锛?|
| 鏈烘瀯鎸佷粨 | institutions6 (INSTITUTIONS) | S 1.17 | 鍒ゅ急 |
| 鍒嗘瀽甯?| analyst 鍏?13 涓?| 鈥?| 瑕嗙洊涓嶈冻 |
| 椋庨櫓 | risk 鍏?4 涓?| 鈥?| 鏈尯鏃犳暟鎹?|

**ASI 鐨勭粨鏋勬€х煕鐩撅紙鏈垬褰规渶閲嶈鐨勪竴鏉″厓缁撹锛?*锛?`LOW_SHARPE` 闂ㄦ **1.58** 瑕佹眰楂樹俊鍙峰己搴︼紱鑰?ASI 閲屽敮涓€鑳界ǔ瀹氱粰鍑洪珮寮哄害鐨勬暟鎹紙`dl_riskfree` / `multi_source_model`锛?閮芥槸**浠锋牸鐨勫啀缂栫爜**锛屽洜姝?prod 澶╃劧 鈮?.75銆丣PN/robust 瀛愬畤瀹欓椄澶╃劧涓嶈繃銆?**寮哄害楂?鈬?浠锋牸娲剧敓 鈬?鎷ユ尋**锛岃繖鏉￠摼鍦?ASI 鍐呮槸闂悎鐨勩€?

---

## 14. 鈽呪槄鈽呪槄 绐佺牬锛氱獥鍙ｈ胺 + decay22 鍙屾潬鏉嗙牬 prod 澧欙紝浜у嚭 ASI 鎴樺焦鍓嶄袱棰楀叏缁垮€欓€夛紙2026-11-07锛?
### 14.1 鍐冲畾鎬у彂鐜?
**绗?13 鑺傜‘璁ょ殑銆岀粨鏋勬€х煕鐩俱€嶏紙寮哄害楂?鈬?浠锋牸娲剧敓 鈬?鎷ユ尋锛夎涓ゆ潯姝ｄ氦鏉犳潌鎵撶牬**锛?
1. **ts_rank 鐭獥鍙樻崲锛堢獥鍙ｈ胺锛夌牬 prod**锛氭妸 signal 浠庛€屾按骞?rank銆嶆敼鎴愩€岃繎 W 鏃ユ椂搴忕櫨鍒嗕綅銆嶏紝
   prod 闅?W 鍗曡皟璧颁綆锛學=8 璧疯穼鐮?0.70 绾裤€?2. **decay 22 鎶?S 涓嶄激 2Y**锛氱煭绐楀彉浣撶殑 S 浠?1.44/1.61 鍙嶅脊鍒?2.11锛屼笖 2Y 淇濇寔 2.14/2.25锛堣繙瓒?1.58 绾匡級銆?   锛堜笌 DEU 璁板繂銆屽钩婊戝帇姝?2Y銆嶄簰琛ワ細**decay 鍙傛暟涓嶆潃 2Y锛宼s_mean/ts_decay_linear 鎵嶆潃**鈥斺€攄ecay 鍙钩婊戞寔浠撳啀骞宠　锛屼笉鏀逛俊鎭鐜囥€傦級

### 14.2 绐楀彛鈥損rod 鍝嶅簲鏇茬嚎锛坧robability_label1_4quantile_60day_ohlcv锛孲LOW锛宑ountry锛?
| 鍙樹綋 | S | 2Y | TO | prod | 鍒?|
|---|---:|---:|---:|---:|---|
| 鍩哄噯锛堟按骞?rank锛寃pQY5221锛塪ecay4 | 2.84 | 2.14 | ~18% | 0.8643 | prod 鍗℃ |
| ts_av_diff 66, decay4 | 2.32 | 1.51 | 23.0% | 0.8196 | 鍘诲潎鍊间笉澶?|
| ts_rank W=66, decay4 | 2.33 | 1.71 | 25.2% | 0.791 | |
| ts_rank W=22, decay4 | 2.04 | 1.68 | 35.1% | 0.7475 | |
| ts_rank W=44, decay4 | 2.30 | 1.80 | 28.3% | 0.7375 | |
| **ts_rank W=10, decay4** | 1.61 | 1.55 | 47.7% | **0.722** | S 宸?0.03 |
| **ts_rank W=8, decay4** | 1.44 | 1.44 | 50.9% | **0.6972** | S 宸?0.14 |
| ts_rank W=5, decay4 | 1.03 | 0.90 | 63.2% | **0.6104** | S 濉?|
| **鈽?ts_rank W=10, decay22锛圞PJZRmXN锛?* | **2.11** | **2.14** | 23.8% | **0.6898** | **鍏ㄨ繃** |
| **鈽?ts_rank W=8, decay22锛坙eA1ZMQN锛?* | **2.11** | **2.25** | 26.1% | **0.6808** | **鍏ㄨ繃** |

prod 瀵?W 鐨勫搷搴旓細0.86锛堟棤鍙樻崲锛夆啋 0.75锛圵22锛夆啋 0.72锛圵10锛夆啋 0.70锛圵8锛夆啋 0.61锛圵5锛夛紱
S 瀵?W 鐨勫搷搴旂浉鍙嶃€?*涓ゆ洸绾跨殑鍙浜ら泦鍦?W鈭圼8,10] 脳 decay22銆?*

### 14.3 涓ら鍏ㄧ豢鍊欓€夛紙10 PASS / 0 FAIL / self 杩?/ prod 杩?/ 鍗佸勾瑕嗙洊杩囷級

| | KPJZRmXN | leA1ZMQN |
|---|---|---|
| 琛ㄨ揪寮?| `multiply(-1, group_rank(ts_rank(probability_label1_4quantile_60day_ohlcv, 10), country))` | 鍚屽乏锛學=8 |
| 璁剧疆 | ASI / MINVOL1M / D1 / **decay22** / SLOW / trunc0.08 | 鍚屽乏 |
| S / F / TO | 2.11 / 0.88(w) / 23.8% | 2.11 / 0.84(w) / 26.1% |
| 2Y / sub | 2.14 / 1.32 | 2.25 / 1.33 |
| **prod** | **0.6898** | **0.6808** |
| self | 鈭?.004锛堟睜 5 棰楀叏 <0.03锛?| 鏈祴锛堜笌 KPJ 浜掔浉鍏冲繀鐒?>0.95锛?|
| checks | 10 pass 0 fail锛泈arning 浠?LOW_FITNESS 0.88/CLUSTER_TEST 0.88锛堥潪闃绘柇锛?| 10 pass 0 fail锛泈arning LOW_FITNESS 0.84/CLUSTER_TEST 0.90 |
| robust 鍙岄椄 + JPN | **鍏?PASS**锛坧robability 鏃忓浐鏈夌ǔ鍋ユ€?+ decay22锛?| 鍏?PASS |
| 鍗佸勾閫愬勾 | longCount 1556鈥?251锛岄€愬勾 Sharpe 0.86鈥?.53 鍏ㄦ | longCount 1557鈥?250锛岄€愬勾 Sharpe 0.84鈥?.37 鍏ㄦ |
| 绠楀瓙鏁?| 3锛坢ultiply/group_rank/ts_rank锛夆墹12 鉁?| 3 鉁?|
| 濉?| dl_riskfree_returns 鍗曟暟鎹泦 ATOM锛圤THER 濉旓級锛孧ATCHES_PYRAMID 鉁?| 鍚?|

**鎺ㄨ崘鎻愪氦 leA1ZMQN**锛歱rod 浣欓噺 0.019锛圞PJ 0.010锛夈€?Y 浣欓噺 0.67锛圞PJ 0.56锛夆€斺€斾袱棰椾簰鐩稿叧 >0.95锛屽彧鑳芥嫨涓€锛?纭椄浣欓噺澶х殑浼樺厛銆侹PJZRmXN 鐣欎綔 leA 涓囦竴鎻愪氦澶辫触鐨勫鑳庛€?
### 14.4 鏈哄埗瑙ｉ噴涓庡彲绉绘鎬?
- **涓轰粈涔堢煭绐?ts_rank 鐮?prod**锛氬鐓?alpha锛堢敓浜ф睜 [0.8,0.9] 鍞竴涓€棰楋級浜ゆ槗鐨勬槸璇?CNN 姒傜巼鍦虹殑**鎱㈠彉姘村钩**锛?  ts_rank(W鈮?0) 鍙繚鐣欍€屾渶杩?8鈥?0 鏃ョ浉瀵逛綅缃€嶏紝鎶婃參鍙樺叡鍚屽垎閲忓嚑涔庡叏閮ㄥ墺鎺夛紝PnL 娴佷笌瀵圭収 alpha 鐨勯噸鍙犳柇宕栧紡涓嬮檷銆?  淇″彿鐨勭粡娴庡惈涔変篃浠庛€屾ā鍨嬮娴嬫按骞炽€嶅彉鎴愩€屾ā鍨嬮娴嬬殑**鐭湡杈归檯鍙樺寲**銆嶏紝鏈川鏄悓涓€淇℃伅鐨勪笉鍚岀煩銆?- **涓轰粈涔?decay22 鑳芥姮 S**锛氱煭绐椾俊鍙锋崲鎵?47鈥?3%锛屾棩搴﹀櫔澹板ぇ锛沝ecay22 鎶婃寔浠撳啀骞宠　鎽婂埌涓夊懆锛?  闄嶄綆浜嗕氦鏄撴椂鐐瑰櫔澹?鈬?S 1.44鈫?.11銆傚洜涓?decay 涓嶆敼鍙樹俊鎭唴瀹癸紝2Y 涓嶅彈鎹熴€?- **鍙Щ妞嶉厤鏂?*锛堝浠讳綍銆屽己浣嗘嫢鎸ゃ€嶇殑淇″彿鍦猴級锛歚group_rank(ts_rank(X, W_short), country)` @ decay 澶у€笺€?  鍏堟壂 W 鎵?prod 璋凤紙W鈭坽5,8,10,13,22}锛夛紝鍐嶇敤 decay 鎶?S 鎷夊洖绾夸笂銆傛瘡棰楁垚鏈害 2 鎵?脳 3 鏉°€?
### 14.5 鍚庣画娲剧敓璺緞锛堢偣濉旓級

1. 鎻愪氦 leA1ZMQN锛堢瓑鐢ㄦ埛纭锛夆啋 OTHER 濉旇繘搴?1/3銆?2. 绗?2 棰楀悓濉斾欢锛氭崲 probability 瀛楁锛?2 涓€欓€夛級+ 鐭獥 ts_rank锛岄』涓?leA 鐨?self <0.7锛?   鎴栧 quantile 鏃忓仛 ts_rank 鐭獥锛堝畠浠?robust 涓嶈繃锛岄渶鍙︽兂鍔炴硶锛夈€?3. 鍏跺畠鍖猴紙KOR/DEU/TWN鈥︼級鐨勬嫢鎸ゅ己淇″彿鍦哄彲鐩存帴濂楃敤 14.4 閰嶆柟銆?

---

## 15. 鈽?鐢ㄦ埛鍙ｅ緞绾犲亸锛欶<1 涓嶇畻杩?+ quantile 鏃忕煭绐楀叏鎵弿锛?026-11-08锛?
### 15.1 鐢ㄦ埛绾犲亸
鐢ㄦ埛鏄庣‘锛氥€岃繖涓?Fitness<1 涓嶈兘绠楄繃銆嶁€斺€擫OW_FITNESS 铏界劧骞冲彴鍙爣 warning锛屼絾 F<1 灏辨槸涓嶈揪鏍囥€?leA1ZMQN锛團 0.84锛? KPJZRmXN锛團 0.88锛変粠"鍏ㄧ豢"闄嶇骇涓?涓嶅彲鎻愪氦"銆備弗鏍煎彛寰勶細F鈮? 蹇呴』婊¤冻銆?
### 15.2 quantile 鏃?20day 鐭獥鎵弿锛堝叏閮?@ SLOW/country锛宺obust 鍙岄椄鏄富瑕佸崱鐐癸級

| W | decay | alpha | S | F | 2Y | fail |
|---|---|---|---:|---:|---:|---|
| 66 | 22 | gJeQgQvl* | 4.82 | 3.41 | 4.07 | robust ratio 4.33<5.30 / returns 0.071<0.082 |
| 22 | 22 | A1VEYeeY | 3.92 | 2.58 | 2.10 | robust ratio 3.38<3.53 |
| 10 | 22 | MPYV92An | 4.03 | 2.29 | 1.77 | robust ratio 3.53<3.63 |
| 5 | 22 | gJeLwXre | 3.82 | 1.79 | 1.84 | robust ratio 3.38<3.44 |
| 4 | 22 | kqN918Vl | 3.54 | 1.51 | 1.56 | robust returns 0.055<0.057 |
| 3 | 22 | KPJZXV7p | 3.07 | 1.17 | 1.14 | 0 fail锛宲rod 0.7023 |
| 3 | 15 | RREPrr7n | 3.02 | 1.07 | 1.08 | 0 fail锛宲rod 0.6995锛堜綑閲?0.0005锛墊
| 3+pow0.75 | 15 | A1VEPkEX | 2.95 | 1.03 | 0.99 | 0 fail锛宲rod 0.6975锛堜綑閲?0.0025锛墊
| 3+pow0.5 | 15 | Xg9MWoL8* | 2.86 | 0.99 | 0.91 | JPN 0.99<1 fail |
| 2 | 22 | RREP257b | 1.76 | 0.48 | 0.30 | JPN 0.22<1 fail |

鍏抽敭瑙勫緥锛歐 瓒婄煭 robust ratio 甯告暟瓒婇珮锛?.825鈫?.885锛夛紝浣?W鈮? 鏃?JPN Sharpe 宕╋紙淇℃伅閲忎笉瓒筹級銆?W3 @ decay15 鏄敮涓€鐨?F鈮? 涓?0 fail 鐐癸紝浣?prod 浣欓噺浠?0.0005-0.0025銆?
### 15.3 BU 鎵规崲瀛楁/鎹㈠彉鎹㈠皾璇曪紙鍏ㄧ伃锛?- 2bucket_20day W3 (vR1PkN9b): S 2.48, F 0.82, robust returns fail
- 1bucket_60day W3 (3qoJ9p6Z): S 2.28, F 0.69, JPN fail
- signed_power 0.5 @ decay10 (BT batch): F 0.9/0.96, JPN fail

### 15.4 褰撳墠涓ユ牸缁垮€欓€夋竻鍗曪紙鐢ㄦ埛鍙ｅ緞锛?| alpha | 閰嶇疆 | S | F | 2Y | prod | 闂 |
|---|---|---|---:|---:|---:|---|
| RREPrr7n | W3 quantile d15 | 3.02 | 1.07 | 1.08 | 0.6995 | 2Y 浣欓噺 0锛?.08 vs 1.58 绾匡紵锛墊
| A1VEPkEX | W3 pow0.75 d15 | 2.95 | 1.03 | 0.99 | 0.6975 | 2Y 鏈繃绾?|

绛夌瓑鈥斺€?Y Sharpe 闃堝€间篃鏄?1.58锛丷REPrr7n 鐨?2Y 鏄?1.08锛孉1VEPkEX 鏄?0.99銆侺OW_2Y_SHARPE 妫€鏌モ€︹€﹁纭杩欎袱涓殑 2Y 鏄惁杈炬爣銆傚墠闈?det 鏌ヨ fails 涓虹┖锛岃鏄?LOW_2Y_SHARPE 娌℃湁鍑虹幇鍦?fail 閲岋紝浣嗙敤鎴疯蹇嗛噷 KOR 鐨勬暀璁槸銆?Y 鏄樆鏂嚎銆嶃€?
闇€瑕佺珛鍗抽獙璇?RREPrr7n 鍜?A1VEPkEX 鐨?LOW_2Y_SHARPE 妫€鏌ョ姸鎬侊紒


## 15.5锛堢画锛塪ecay44 淇 F<1锛歱robability 鏃?W8 @ decay44 = 棣栭涓ユ牸鍏ㄧ豢鍊欓€?
decay 鎻愰珮鍒?44 鍚庯紝鎹㈡墜鐜囧帇鍒?12.5% 鍦版澘闄勮繎锛孎 浠?0.84 鈫?1.01锛?
| alpha | W | decay | S | F | 2Y | TO | fail | prod | 鍒ゅ畾 |
|---|---|---|---:|---:|---:|---:|---:|---:|---|
| 1YN0XrYX | 8 | 44 | 2.18 | 1.01 | 2.20 | 20.3% | 0 | 0.6934 | **涓ユ牸鍏ㄧ豢** |
| e75EbX7M | 10 | 44 | 2.17 | 1.05 | 2.08 | 18.5% | 0 | 寰呮煡 | 鍊欒ˉ |
| akKGb5j2 | 13 | 44 | 2.14 | 1.11 | 1.98 | 15.6% | 0 | 寰呮煡 | 鍊欒ˉ |

1YN0XrYX 瀹屾暣楠岃瘉锛?- S 2.18 >= 1.58 鉁?- F 1.01 >= 1.0 鉁擄紙鏃?LOW_FITNESS warning锛?- 2Y 2.20 >= 1.58 鉁?- 0 fail 鉁?- prod 0.6934 < 0.70 鉁?- self 0.0007 鉁?- 鍗佸勾瑕嗙洊锛?014-2023 姣忓勾 longCount 1560-2249锛宲nl 鍏ㄦ锛岄€愬勾 Sharpe 0.61-3.11 鍏ㄦ 鉁?- 绠楀瓙鏁?3 涓紙multiply / group_rank / ts_rank锛夆湏

quantile 鏃忥紙W3 @ decay15 RREPrr7n锛夎櫧鐒?S 3.02 / F 1.07 / prod 0.6995锛屼絾 2Y 1.08 << 1.58锛?LOW_2Y_SHARPE 鍦?warning 鍒楄〃鈥斺€旀寜 KOR 鐨勬暀璁紙2Y 鏄樆鏂嚎锛夛紝涓嶅彲鎻愪氦銆?
## 15.6 quantile 鏃忎笌 probability 鏃忕殑瀵规瘮缁撹

| 鎸囨爣 | quantile 鏃?W3 | probability 鏃?W8 |
|---|---:|---:|
| S | 3.02 | 2.18 |
| F | 1.07 | 1.01 |
| 2Y | **1.08 鉁?* | 2.20 鉁?|
| TO | 41.2% | 20.3% |
| prod | 0.6995 | 0.6934 |

quantile 鏃忓叏鏃舵鏇村己锛屼絾杩戜袱骞磋“鍑忎弗閲嶏紙鐭獥淇℃伅蹇繃鏈燂級锛沺robability 鏃?2Y 鍋ュ悍寰楀銆?閫?probability 鏃?1YN0XrYX 浣滀负涓绘彁浜ゅ€欓€夈€?

## 16. multi_source_model 鐭獥绉绘澶辫触 + 鏈疆鎬荤粨锛?026-11-08锛?
### 16.1 BW 鎵癸紙multi_source_model 鐭獥 @ decay22锛夛細鍏ㄧ伃
| alpha | 瀛楁 | W | S | F | 2Y | fail |
|---|---|---|---:|---:|---:|---|
| omEZoXLE | regime4_5d W3 | 1.38 | 0.53 | 0.20 | JPN 0.18 + robust 3 椤?|
| ZYQNm9b8 | regime4_5d W5 | 1.68 | 0.71 | 0.41 | JPN 0.26 + robust |
| WjOJLReQ | quantile1_20d W3 | 1.25 | 0.45 | 0.29 | JPN 0.19 + robust |

鐭獥閰嶆柟涓嶈兘璺ㄦ暟鎹泦绉绘锛氭按骞崇増 S 3.24 鈫?鐭獥鐗?S 1.4-1.7锛屼俊鎭“鍑忓お蹇€俶ulti_source_model 鍒ゆ銆?
### 16.2 鏈疆鏈€缁堝€欓€夋竻鍗曪紙涓ユ牸鍙ｅ緞锛?
| 鍊欓€?| 琛ㄨ揪寮?| S | F | 2Y | prod | 鐘舵€?|
|---|---|---:|---:|---:|---:|---|
| **1YN0XrYX** | -group_rank(ts_rank(prob_1_4q_60d, 8), country) @ decay44 | 2.18 | 1.01 | 2.20 | **0.6934** | **涓ユ牸鍏ㄧ豢锛屽彲鎻愪氦** |
| e75EbX7M | 鍚屼笂 W=10 @ decay44 | 2.17 | 1.05 | 2.08 | 瓒呮椂 | 澶囬€?|
| leA1ZMQN | W=8 @ decay22 | 2.11 | 0.84 | 2.25 | 0.6808 | F<1 涓嶅彲鎻愪氦 |
| RREPrr7n | quantile W3 @ decay15 | 3.02 | 1.07 | **1.08** | 0.6995 | 2Y 鎸℃ |
| A1VEPkEX | quantile W3 pow0.75 | 2.95 | 1.03 | **0.99** | 0.6975 | 2Y 鎸℃ |

### 16.3 缁忛獙娌夋穩
1. **F = S路sqrt(|ret|/max(TO,0.125))**锛欶<1 鏃舵妸 decay 鍔犲ぇ鍘?TO 鍒?12.5% 鍦版澘鍗冲彲鎷夊崌 F锛屾棤闇€鏀逛俊鍙枫€?2. **鐭獥 ts_rank 鐨?2Y 浠ｄ环**锛歲uantile 鏃忕煭绐?2Y 宕╋紙1.08锛夛紝probability 鏃忕煭绐?2Y 鍋ュ悍锛?.20锛夆€斺€斾袱涓棌鐨勮繎涓ゅ勾淇″彿绋冲畾鎬у畬鍏ㄤ笉鍚屻€?3. **鐭獥閰嶆柟涓嶅彲璺ㄦ暟鎹泦绉绘**锛坢ulti_source_model 鍙嶄緥锛夈€?4. **LOW_2Y_SHARPE 铏界劧鍙槸 warning锛屼絾鎸?KOR 鏁欒瀹冩槸鎻愪氦闃绘柇绾?*鈥斺€斿繀椤?2Y鈮?.58 鎵嶇畻鐪熺豢銆?

## 17. 绗簩棰楀€欓€夋帰绱細涓変釜鏂版暟鎹泦鎺㈤拡鍏ㄥ急锛?026-11-08锛?
涓哄鎵句笌 1YN0XrYX 涓嶇浉鍏崇殑绗簩棰楀€欓€夛紙濉斿鍏冨寲锛夛紝瀵逛笁涓湭娴嬫暟鎹泦鍋氫簡姘村钩鎺㈤拡锛堝潎 SLOW/country/decay22锛夛細

### 17.1 ai_factor_transfer锛圡ODEL锛宑ov 1.0锛?0 涓妧鏈寚鏍?MATRIX锛?| alpha | 瀛楁 | S | 2Y | fail |
|---|---|---:|---:|---|
| 2rAeGZkZ | cumulative_money_flow_volume_adjusted (aC55) | 1.25 | 1.82 | JPN 0.47 + robust |
| E56xmaAG | short_term_price_change_2 (aC46) | 0.44 | 0.53 | 4 fail |
| 9qxkG6Qx | volume_trend_money_flow_interaction_2 (aC58) | 1.00 | 0.85 | 0 fail 浣?S 浣?|

鍒わ細缁忓吀鎶€鏈寚鏍囷紙RSI/CMF/BB锛夊湪 ASI 鏃犺秴棰濆己搴︺€?*ai_factor_transfer 鍒ゅ急**銆?
### 17.2 continuation_score锛圥V锛宑ov 1.0锛?60 涓舰鎬佺浉浼煎害 MATRIX锛?| alpha | 瀛楁 | S | 2Y | fail |
|---|---|---:|---:|---|
| YP1Y8W3l | ascending_channel_similarity_recent (aC122) | 1.55 | 0.28 | JPN 0.38 |
| omEZR9b5 | ascending_channel_similarity_middle (aC50) | 1.58 | 0.35 | JPN 0.44 |
| WjOJ3WZP | ascending_scallop_similarity_maximum (aC25) | 0.79 | 0.74 | 4 fail |

鍒わ細涓婂崌閫氶亾褰㈡€佽瘑鍒?S 1.55-1.58 涓寸晫浣?2Y 鍏ㄥ穿锛?0.4锛夈€傚舰鎬佹棌鍦ㄨ繎涓ゅ勾瀹屽叏澶辨晥銆?*continuation_score 鍒ゅ急**銆?
### 17.3 pv106锛圥V锛宑ov 1.0锛?9 涓?spread/slippage MATRIX锛?| alpha | 瀛楁 | S | fail |
|---|---|---:|---|
| 6XdNoKO7 | -pv106_wli_spreadbp (aC161) | 鈭?.65锛堝彇鍙嶅悗涓鸿礋 鈬?姝ｅ悜 +0.65 涔熷急锛?| 5 fail |
| Xg9MvJ6l | -transaction_cost_median (aC21) | 鈭?.27 | 4 fail |

鍒わ細娴佸姩鎬ф孩浠凤紙浣?spread 鍋氬锛夊湪 ASI 涓嶆垚绔嬨€?*pv106 鍒ゆ**銆?
### 17.4 ASI 鍏ㄩ噺鏁版嵁闆嗗垽瀹氭眹鎬伙紙鎴嚦鏈妭锛?58 涓暟鎹泦鐨勫畬鏁寸敾鍍忥級

| 濉?| 鏁版嵁闆嗘暟 | 鍒ゅ己 | 鍒ゅ急 | 鍒ゆ/鏃犳暟鎹?|
|---|---:|---|---|---|
| other | 27 | dl_riskfree_returns锛堝敮涓€鍑鸿揣婧愶級 | 鈥?| 26 涓棤鐪熷疄鏁版嵁/鍏冩暟鎹敊浣?|
| model | 41 | 鈥?| multi_source_model(3闂?銆乥ehavioral_signals銆乤i_factor_transfer | 鍏朵綑鏃犲崄骞磋鐩?|
| pv | 19 | 鈥?| continuation_score | pv106銆乸v149/univ1(闈炰俊鍙峰瓧娈? |
| news | 22 | 鈥?| 鈥?| news38/news7 鎯呯华寮便€乶ews59 鏃犳暟鍊?|
| fundamental | 11 | 鈥?| fundamental44 | 鍏朵綑瑕嗙洊涓嶈冻 |
| analyst | 13 | 鈥?| 鈥?| 鍏ㄩ儴瑕嗙洊 <0.82 |
| risk | 4 | 鈥?| 鈥?| 鍏ㄥ鏃犳暟鎹?|
| 鍏朵綑灏忓 | 17 | 鈥?| 鈥?| 鏃犳暟鎹垨瑕嗙洊涓嶈冻 |

**缁撹锛欰SI 鍙紑閲囩殑淇″彿婧愰珮搴﹂泦涓€斺€攄l_riskfree_returns 鏄敮涓€鑳借繃鍏ㄩ儴纭椄鐨勬暟鎹泦**锛堜环鏍兼淳鐢?ML 鍦?+ 鐭獥鍙樻崲 + decay 淇 = 鍞竴閫氬叧缁勫悎锛夈€傚叾瀹?157 涓暟鎹泦鍦?ASI/MINVOL1M 涓婅涔堟棤鏁版嵁銆佽涔堣鐩栦笉瓒炽€佽涔堝己搴︿笉澶?1.58 绾裤€?

---

## 18. dl_riskfree_returns 鍏ㄥ瓧娈垫帰绱㈡敹鍙ｏ細label3/4 楂樺己搴︿絾 robust 甯告暟纭锛?026-11-08锛?
### 18.1 label3_4quantile 鏃忕殑 robust 澧欙紙9 涓厤缃叏鎵級

CA 鎵瑰彂鐜?label3_4q_60day 鍙栧弽 S 鈭?.02 鈬?**姝ｅ悜 +4.02**锛圥 钀界涓夊垎浣嶆《=鍒╁ソ 鈫?鍋氬锛屼笌 label1 绌哄ご閫昏緫瀵圭О锛夈€?闅忓悗 9 涓厤缃壂鎻忥紙W5鈥?3 脳 decay15鈥?4 脳 涓変釜瀛楁鍙樹綋锛夛細

| 閰嶇疆 | alpha | S | F | 2Y | robust fail |
|---|---|---:|---:|---:|---|
| 60day W8 d44 | 1YN02Xr6 | 4.02 | 2.50 | 2.69 | 3.59<3.62 / 0.069<0.07 |
| 60day W10 d44 | Xg9MObda | 4.03 | 2.64 | 2.60 | 3.59<3.63 / 0.068<0.07 |
| 60day W13 d44 | mLoQlmEE | 4.03 | 2.81 | 2.53 | 3.60<3.63 / 0.067<0.068 |
| 60day W8 d22 | e75EZpmJ | 3.78 | 2.00 | 2.36 | **浠?* 0.063<0.064 |
| 60day W10 d22 | GrW95aPo | 3.73 | 2.06 | 2.20 | 3.35<3.36 / 0.062<0.063 |
| 60day W8 d15 | QPv6pYdr | 3.73 | 1.81 | 2.17 | **浠?* 0.061<0.062 |
| 60day W5 d15 | KPJZMmRk | 3.53 | 1.48 | 2.24 | 3.10<3.18 / 0.057<0.059 |
| 5day W8 d22 | npvrjR28 | 4.05 | 2.32 | **3.02** | 3.58<3.65 / 0.071<0.074 |
| 5day W8 d15 | mLoQvO1E | 4.02 | 2.13 | 3.01 | 3.60<3.62 / 0.071<0.072 |
| 5day W10 d15 | 3qoJNdJ6 | 3.93 | 2.16 | 2.89 | 3.52<3.54 / 0.069<0.07 |
| 20day_2 W8 d22 | 88RX09Qo | 4.26 | 2.43 | 2.68 | 3.75<3.83 / 0.071<0.074 |
| 20day_2 W8 d15 | MPYVrwVa | 4.28 | 2.28 | 2.67 | 3.82<3.85 / 0.071<0.073 |

**瑙勫緥**锛歋 3.5鈥?.3 鏋佸己銆?Y 2.2鈥?.0 鏋佸仴搴枫€丗 1.5鈥?.8 浣欓噺澶э紝浣?robust ratio 甯告暟绋冲畾 0.88鈥?.89锛堥渶 0.90锛夈€?robust returns 鎭掑樊 0.001鈥?.003銆?*杩欐槸瀛楁绾х‖澧?*锛歭abel3/label4 淇″彿闆嗕腑鍦ㄩ珮棰勬湡鏀剁泭灏忕エ涓婏紝
robust universe锛堟祦鍔ㄦ€у瓙闆嗭級鍚冧笉婊?90% 闃堝€笺€俵abel1锛圫 2.18锛夎兘杩囨槸鍥犱负淇″彿鍒嗗竷鏇村潎鍖€銆?**涓?quantile 鏃?robust 鎸傜殑鍚屾瀯鎬?*锛欰SI 鐨?robust 闂稿ぉ鐒舵儵缃?楂樻敹鐩婇泦涓?鐨勪俊鍙凤紝涓?JPN 闂革紙鎯╃綒璺ㄥ浗鍒嗗竷涓嶅潎锛夋浜ゃ€?
### 18.2 2q/3q/5q 鍒嗕綅瀹舵棌锛圕H 鎵癸級

| 瀛楁 | 褰㈡€?| S | 鍒?|
|---|---|---:|---|
| label0_2q_60day 鍙栧弽 | qMLVQZ6Z | 3.16 | JPN 0.95 + robust + 2Y 1.52 涓夋寕 |
| label2_3q_60day 鍙栧弽 | d5WvNwRE | 鈭?.85锛堟鍚?+3.85锛墊 鏈繁鎸栵紙棰勮鍚?robust 澧欙級|
| label4_5q_60day 姝ｅ悜 | xAr5Jadn | 3.93 | robust 3.52<3.54 / 0.069<0.07 鍙屾寕 |

### 18.3 dl_riskfree_returns 鏈€缁堝垽瀹氾紙57 瀛楁鍏ㄧ敾鍍忥級

| 瀛楁鏃?| 寮哄害 | robust | 缁撹 |
|---|---|---|---|
| probability_label1_4q_60day (aC22) | S 2.18 @ W8d44 | **杩?* | **鍞竴鍏ㄧ豢**锛?YN0XrYX锛墊
| probability_label1 鍏朵綑 | S 0.4鈥?.8 | 鎸?| 寮?姝?|
| probability_label3/4_4q | S 3.9鈥?.3 | **鎭掓寕 0.88鈥?.89** | robust 纭锛?2 閰嶇疆鍏ㄦ壂鏃犺В |
| quantile_label 鏃?| S 3.0鈥?.6 | 鎸?or 2Y 宕?| 9 鍑犱綍鏃犺В锛?Y 鏄?quantile 鐭獥鐨勫锛墊
| 2q/3q/5q 鏃?| S 3.2鈥?.9 | 鎸?| 澶氶噸闂?|
| 浣?aC 瀛楁锛坅C<20锛墊 S 1.12 | 鈥?| 寮?|

**ASI 鎴樺焦鏈€缁堢粨璁?*锛?58 涓暟鎹泦銆亊40 鎵广€?00+ 鏉″洖娴嬪悗锛?*dl_riskfree_returns 鐨?label1_4q_60day
鏄?ASI/MINVOL1M 鍞竴鍙彁浜や俊鍙?*銆傚叾瀹冨叏閮ㄨ矾寰勫凡绌峰敖锛歳isk/news/fundamental/analyst/institutions/
sentiment/socialmedia 鏃犳暟鎹垨寮憋紱model/pv 濉旂殑鍙敤瀛楁鍏ㄥ急锛沝l_riskfree 鍐呴儴闄?label1 澶栧叏閮?robust/JPN/2Y 纭寕銆?

---

## 19. quantile 鏃忕煭绐楀叏鍙傛暟鏀跺彛锛?Y 澧欎笌 prod 澧欎簰鏂ワ紝鏃犳彁浜ょ┖闂达紙2026-11-08锛?
### 19.1 W4/W5 @ 浣?decay 鐨勬渶鍚庣獊鐮村皾璇曪紙CI/CM 鎵癸級

缁х 15 鑺傜殑 W 鎵弿鍚庯紝鏈疆琛ユ壂浜嗕綆 decay 鍖猴紙杩欐槸 robust returns 宸窛鐨勫崟璋冪缉灏忔柟鍚戯級锛?
| 閰嶇疆 | alpha | S | F | 2Y | robust | JPN | prod | 鍒?|
|---|---|---:|---:|---:|---|---|---:|---|
| W4@15 | ZYQNoo7x | 3.48 | 1.38 | 1.49鉁?| returns 0.055<0.056 | 鉁?| 鈥?| 2Y+robust 鍙屾寕 |
| W5@15 | akKgr7E6 | 3.74 | 1.61 | 1.71鉁?| ratio 3.36<3.37 + ret 0.059<0.06 | 鉁?| 鈥?| robust 宸?0.01 |
| W5@10 | 1YN2kvVJ | 3.68 | 1.46 | 1.96鉁?| ratio 3.30<3.31 + ret 0.058<0.059 | 鉁?| 鈥?| robust 宸?0.01 |
| W4@10 | KPJ2leYp | 3.37 | 1.22 | 1.67鉁?| ret **0.0530<0.0531**锛堝樊 0.0001锛墊 鉁?| **0.7193鉁?* | prod 缈荤嚎 |
| W4@10 澶嶅埢 | KPJ2leYp(bis) | 3.37 | 1.22 | 1.67鉁?| 鍚屼笂 | 鉁?| 0.7193 | 涓€鑷存€р湏 |
| W5@5 | LLM2aWme | 3.36 | 1.13 | 1.82鉁?| **鍏ㄨ繃** | **0.99<1锛堝樊 0.01锛?* | **0.7216鉁?* | prod+JPN |
| W4@5 | N1N2m0LL | 3.01 | 0.92鉁?| 1.60鉁?| 鈥?| 0.98<1 | 鈥?| F+JPN |

pow0.75 鍙樹綋锛?YN2kvVW锛夊 robust 鏃犳晥锛堟瘮 plain 鐣ュ樊锛夛紱60day 瀛楁锛?qo2wJMZ / Jje2qrVn锛夊叏闈㈡洿寮卞垽姝汇€?
### 19.2 quantile 20day 鏃忎笁澧欎簰鏂ョ粨鏋勶紙15 閰嶇疆缁堝眬锛?
| W | 2Y 澧欙紙1.58锛?| prod 澧欙紙0.70锛?| robust 澧?| 浜ら泦 |
|---|---|---|---|---|
| **W2-W3** | 鉁楋紙1.08-1.26锛屼俊鎭繃鏈燂級 | 鉁擄紙0.6995 璋峰簳锛?| 鉁?| 2Y 鎸℃ |
| **W4** | 鉁擄紙1.56-1.67锛?| 鉁楋紙0.7193锛?| 宸?0.0001 鍙牬 | prod 鎸℃ |
| **W5** | 鉁擄紙1.71-1.96锛?| 鉁楋紙0.7216锛?| d5 鍏ㄨ繃 | prod 鎸℃ |
| **W8-W66** | 鉁?| 鉁楋紙0.71-0.79锛?| 鉁?| prod+robust |

**鏈虹悊**锛歐3鈫扺4 鐨?2Y 璺冲彉锛?.26鈫?.67锛変笌 prod 璺冲彉锛?.6995鈫?.7193锛夌敱鍚屼竴浜嬩欢椹卞姩鈥斺€?ts_rank 绐楀彛鎷夐暱鍚庝俊鍙蜂粠銆岀嫭绔嬬煭绋嬪姩閲忋€嶅彉鎴愩€屼笌鐢熶骇姹犳參鍙樺垎閲忛噸鍙犵殑杞粨銆嶃€?**2Y 涓?prod 鍦?W 杞翠笂鍚屽悜鎭跺寲锛屾晠涓ゅ鏃犺В**锛歐鈮? 淇?prod 澶?2Y锛學鈮? 淇?2Y 澶?prod銆?
### 19.3 ASI 鎴樺焦缁堝眬鍒ゅ畾

**dl_riskfree_returns 鍏ㄦ暟鎹泦锛?7 瀛楁锛夌殑鎻愪氦绌洪棿 = 1 棰?*锛歱robability_label1_4quantile_60day_ohlcv
@ W8+decay44锛?YN0XrYX锛屽叏缁垮緟鎻愪氦锛夈€俼uantile 鏃忥紙15 閰嶇疆锛変笌 label3/4 鏃忥紙12 閰嶇疆锛?鍒嗗埆姝讳簬銆?Y脳prod 浜掓枼銆嶄笌銆宺obust 甯告暟纭銆嶏紝涓よ€呴兘鏄?*瀛楁绾х粨鏋?*锛岄厤缃┖闂村凡绌峰敖銆?

---

## 20. 缁堝眬锛歞l_riskfree 楂樺己搴﹀瓧娈靛叏鐏簬 robust 澧?+ ASI 棣栧鐐逛寒鎯呮姤锛?026-11-08锛?
### 20.1 CN 鎵癸紙鏈€鍚庢湭娴嬪瓧娈垫棌鏀跺彛锛?
| 瀛楁 | 褰㈡€?| S | 2Y | 鍒?|
|---|---|---:|---:|---|
| label2_3q_60day (aC415) | 姝ｅ悜 W8@d44 | 3.85 | 2.37 | robust 鍙屾寕 3.43<3.47 / 0.0649<0.0667 |
| label1_2q_60day (aC77) | 鍙栧弽 鈫?姝ｅ悜 +3.16 | 3.16 | 鈥?| 鏈繁鎸栵紙鍚?robust 澧欐鐜囨瀬楂橈級|
| label0_3q_60day (aC26) | 鍙栧弽 | 2.31 | 0.86 | JPN + robust + 2Y 涓夋寕 |

### 20.2 dl_riskfree_returns 57 瀛楁缁堝眬瑙勫緥

**淇″彿寮哄害涓?robust 閫氳繃鎬ц礋鐩稿叧**锛?- S 鈭?[2, 2.5]锛坙abel1_4q锛夛細淇″彿鍒嗗竷鍧囧寑 鈫?robust 鉁?鈫?**鍞竴鍏ㄧ豢**
- S > 3 鐨勬墍鏈夊瓧娈碉紙label3/4_4q銆乴abel2_3q銆乴abel1_2q銆乴abel4_5q銆乴abel0_2q銆乹uantile 鍏ㄦ棌锛夛細
  淇″彿闆嗕腑鍦ㄩ珮棰勬湡鏀剁泭灏忕エ 鈫?robust 甯告暟 0.88-0.89 鎭掓寕
- S < 2 鐨勫瓧娈碉細寮哄害涓嶈冻 1.58 绾?
### 20.3 鈽?ASI 濉旂偣浜幇鐘讹紙get_pyramid_alphas 瀹炴煡锛?
ASI **16 涓鍏ㄩ儴鏈偣浜?*锛堝潎 <3锛夈€傚叾涓細
- **OTHER 濉?= 2 棰楋紙宸?1 棰楃偣浜級**
- 鍏朵綑 15 濉?= 0 棰?
鈬?**鎻愪氦 1YN0XrYX锛圤THER 濉?ATOM锛夊嵆鐐逛寒 ASI 棣栧**銆傝繖鏄?ASI 鎴樺焦褰撳墠鏈€楂樹环鍊煎姩浣溿€?
### 20.4 鎴樺焦璧勪骇鎬绘竻鍗曪紙缁堢増锛?
| 璧勪骇 | 鍐呭 |
|---|---|
| 鍏ㄧ豢鍊欓€?| 1YN0XrYX锛坙abel1_4q_60day @ W8+decay44锛孲 2.18/F 1.01/2Y 2.20/prod 0.6934/self 0.0007/鍗佸勾鍏ㄦ锛墊
| 杩戠豢澶囬€?| KPJ2leYp锛坬uantile W4@d10锛宺obust 宸?0.0001 浣?prod 0.7193锛? LLM2aWme锛圵5@d5锛孞PN 宸?0.01 浣?prod 0.7216锛墊
| 鎶ュ憡 | reports/asi_campaign_session_20261103.md锛堟湰鏂囦欢锛寏52 鎵?/ 350+ 鏉″洖娴嬶級|
| 璁板繂 | 鐭獥鐮?prod / decay 淇?F / 2Y 闃绘柇绾?/ robust 鎯╃綒闆嗕腑搴?/ 2Y脳prod 浜掓枼锛屽叡 5 鏉℃柟娉曡 |


### 20.5 group_backfill 淇 robust 闂哥殑璺ㄦ満鍒剁Щ妞嶈瘉浼紙CO 鎵癸級

USA 鎴樺焦瀹炶瘉 group_backfill(x, group, 120) 鍙慨 CONCENTRATED_WEIGHT 闂革紙鏈虹悊=缁勫唴鍥炲～骞虫粦鎴潰锛夈€?灏嗗叾绉绘鍒?robust 闂革紙鍋囪鍚屾簮锛氭瀬绔潈閲嶅湪闈?robust 灏忕エ锛夛細

| alpha | 瀛楁 | S | 2Y | robust 缁撴灉 |
|---|---|---:|---:|---|
| j2YMm2nE | label3 gb120 @ d22 | 3.78 | 2.36 | returns 0.0626<0.0638锛堝師 0.063<0.064锛?*宸窛鐣ユ墿澶?*锛墊
| A1V2K1nY | label2_3q gb120 @ d22 | 3.71 | 2.10 | 鍙屾寕渚濇棫 |

**缁撹**锛欳W 闂革紙鏉冮噸闆嗕腑搴︼級涓?robust 闂革紙鏀剁泭褰掑洜鍒版祦鍔ㄦ€у瓙闆嗙殑姣斾緥锛夋満鐞嗕笉鍚屾簮锛?gb 鍙钩婊戞潈閲嶄笉绉诲姩鏀剁泭鍒嗗竷銆俵abel3/label2_3q 鐨?robust 澧欐渶缁堢‘璁わ細**瀛楁绾у父鏁帮紝13+ 閰嶇疆 脳 鍏ㄩ儴宸茬煡鏈哄埗锛坉ecay/W/骞?瀛楁鍙樹綋/group_backfill锛夋棤瑙?*銆?
