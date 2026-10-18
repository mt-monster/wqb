# KOR Analyst 类字段画像方法（2026-10-14，基于实测数据）

## 一、现状盘点（KOR / category=ANALYST|MODEL）
**19 个有效数据集 / 6662 字段**（碎片化极高，必须先做数据集级分层，不能直接扫字段）

| 数据集 | 字段 | VECTOR | cov | alphaCount | valueScore | 分层判定 |
|---|---|---|---|---|---|---|
| `analyst_earnings_ibes` | 28 | 0 | **1.000** | **9** | **6** | ★**最优白空间**（全覆盖 + 零拥挤 + 最高价值分）|
| `analyst_revision_horizons` | 1026 | 0 | 0.659 | 34 | **6** | ★**大白空间**（修正广度计数，全 MATRIX，aCnt=0 字段海量）|
| `analyst11` | 210 | 0 | 0.583 | 31 | **6** | ★ESG/治理新机制（慢变，未被挖）|
| `analyst_consensus` | 2343 | **2325** | 0.690 | 30 | 5 | 大型 VECTOR 池（稀疏 + 低拥挤）|
| `analyst10` | 640 | 165 | 0.731 | 206 | 4 | 混合型 |
| `analyst44` | 540 | 374 | 0.773 | **950** | 4 | 中度拥挤 |
| `analyst48` | 70 | 70 | 0.441 | 233 | 4 | 混合型 |
| `analyst16` | 109 | 109 | 0.653 | 229 | 4 | 全 VECTOR |
| `analyst9` | 48 | 47 | 0.567 | 95 | 4 | 修正计数（已浅测）|
| `analyst45` | 241 | 241 | **0.253** | 91 | 5 | 极稀疏 VECTOR |
| `analyst81` | 5 | 0 | **0.265** | 10 | 6 | 信用违约概率（极稀疏但未饱和）|
| `analyst46` | 6 | 0 | 0.421 | 34 | 5 | 文本情绪复合分 |
| `analyst_base_ref` | 14 | 10 | 0.732 | 19 | 5 | 基准参考 |
| **饱和区（避）** | | | | | | |
| `analyst15` | 304 | 0 | 0.525 | **12004** | 1 | ❌ 极饱和 |
| `analyst4` | 308 | 48 | 0.633 | **3883** | 2 | ❌ |
| `analyst14` | 461 | 9 | 0.500 | **3655** | 2 | ❌ |
| `analyst25` | 207 | 207 | 0.500 | **3504** | 2 | ❌ |
| `analyst39` | 43 | 0 | 0.895 | **1946** | 2 | ❌ |

## 二、字段画像的 5 个维度（Analyst 类专用）
1. **拥挤度** `alpha_count` / `user_count` —— 决定白空间。**aCnt ≤ 50 且 uCnt ≤ 40 才算未占**。
2. **覆盖率** `coverage` —— 分三档：`≥0.65 稠密`（可直接用）/ `0.4–0.65 中稀疏`（需 backfill 或门控）/ `<0.4 稀疏`（先验弱，需最小验证）。
3. **dataType**（★最易踩坑）—— Analyst 类**同集内 MATRIX/VECTOR 混杂**：
   `analyst_consensus` 2343 中 2325 是 VECTOR，而 `analyst_revision_horizons` 1026 全 MATRIX；
   ⇒ **同名字段前缀不能推断类型，必须逐字段查**。MATRIX 误套 `vec_avg` ⇒ 整批 CANCELLED。
4. **语义档位（description 解析）** —— 决定骨架映射（见下表）。
5. **编码冗余检测** —— `*_rank` 与 `*_percentile`、`*_score` 与 `*_indicator` 常并存同一信息
   （`analyst11.board_independence_{industry,sector,subsector}_{rank,percentile}` 共 6 个字段同源）⇒ **只取一族测**。

## 三、Analyst 字段的 4 类语义原型 → 骨架映射（决定测什么）
| 原型 | 字段命名特征 | KOR 实例 | 对应骨架（族）|
|---|---|---|---|
| **① 修正广度/方向** | `_increasing_/_decreasing_`、`numup/numdn`、`revision`、`_cnt` | `analyst_revision_horizons.analyst_count_increasing_*`、`analyst9.anl9_s_numup` | `analyst_revision_breadth`：`group_rank(ts_delta(vec_avg(cnt),W), group)` |
| **② 目标价 / 评级** | `target_prc_*`、`tp_all_delay_*`、`rating`、`recommend` | `analyst39.anl39_tp_all_delay_1_mean` | `target_price_premium`：`group_rank(divide(vec_avg(tp), close), group)` |
| **③ 打分 / 情绪复合** | `*_score`、`*_indicator`、`*_percentile`、`*_rank`、`prob`、`likelihood` | `analyst46.anl46_indicator`、`anl81_probability_of_default_percent`、`analyst11.*_percentile` | `ceiling_suppress`：`winsorize(rank(x),std)`；`discrete_score_bucket`：`group_rank(x, group)` |
| **④ ESG / 治理 KPI** | `board_*`、`governance`、`*_policy_*`、`emission` | `analyst11.board_independence_*`、`anti_pollution_policy_*` | **无现成族** ⇒ 用已验证的破墙配方（bucket(cap)+liqGate）单独测 |

## 四、4 个 KOR Analyst 特有陷阱
1. **同集混型**（MATRIX/VECTOR）—— 见维度 3，本轮已实测踩坑（整批 CANCELLED）。
2. **`analyst_earnings_ibes` 名不副实**：28 字段实为 `closing_price_*` / `*_total_return_*` / `market_capitalization_*`
   ⇒ **本质是价格派生（pv1 风格）**，crowded 风险高、alpha 空间小，**不应按「分析师预期」预期**。
3. **稀疏 ≠ 无信号**：`analyst81` cov 0.265 但 aCnt 仅 1–4；`analyst45` cov 0.253 / 91。
   ⇒ 低覆盖字段要用**最小验证波**（单字段 × 2 构型 × 8 槽）先探，不按 cov 直接判死。
4. **饱和集必须先排**：`analyst15/4/14/25/39` 的 alphaCount 已是数千 ⇒ 同腿提交后 self 会冲 0.99+，**无提交价值**。

## 五、推荐执行顺序（白空间优先）
1. **`analyst_revision_horizons`（1026 字段，aCnt≈34，vScore 6）** ← 首选。
   起步字段：`analyst_count_increasing_current_year_ebitda_*` / `analyst_count_decreasing_next_quarter_revenue_*`；
   骨架：`group_rank(ts_delta(<cnt>, 22), sector)` + 已验证的 `bucket(rank(cap),0.2)` 与 `trade_when(rank(adv20),0.6)` 组合。
2. **`analyst11`（ESG/治理，210 字段，aCnt 31，vScore 6）** ← 次选（全新机制，慢变，理论上有 2Y）。
3. **`analyst_consensus`（2325 VECTOR，cov 0.69，aCnt 30）** ← 大池子，但需先做字段抽样（按 description 聚类）。
4. **`analyst_earnings_ibes`** ← 最后（本质是价格派生）。

## 六、复用命令（DB 侧零成本筛选）
```sql
-- KOR analyst 未占字段（aCnt<=50, cov>=0.4），按数据集分组
SELECT d.name, COUNT(*) nf, AVG(f.coverage) cov
FROM fields f JOIN datasets d ON d.id=f.dataset_id
WHERE d.region_id=2 AND d.category IN ('ANALYST','MODEL')
  AND f.alpha_count<=50 AND f.coverage>=0.4
GROUP BY d.name ORDER BY nf DESC;
```

---

## 七、★ 「比抽样更好的开扫方案」：零成本预筛 → **description 机制族聚类** → 结构冻结 → 按族判死

### ⚠ 纠错 1：**按命名前缀聚类是错的**（违反「description 是唯一语义依据，名字会骗人」铁律）
| 错误 | 证据（`analyst_revision_horizons` 1026 字段）|
|---|---|
| **拆分不足** | **79 个命名前缀中 64 个（81%）横跨多个 description 族**；`analyst_count` 一个前缀含 **151 个不同 desc 族**、`avg_estimate` 含 91 个 |
| **过度拆分** | desc 最大族 **n=18「average change in analyst recommendations over the past days horizon」横跨 4 个命名前缀**（`analyst_opinion`/`mean_analyst`/`avg_analyst`/`avg_recommendation`）|

⇒ 字段名只是命名约定，不承载语义。**必须按 `description` 聚类。**

### ⚠ 纠错 2：**词边界匹配会漏掉复数**（本轮真正的坑）
第一版用 `re.search(r'estimate', d)` 判「预期」类 ⇒ **匹配不到复数 "estimates"** ⇒ 325 个字段掉进「其它」。
**修正**：常规词用**词干子串匹配**（`'estimate' in d` 同时命中 estimate/estimates/estimated）；
**仅对「危险词」用词边界**（`count` 防 "co**unt**ry"）。

### ★ 完整同义词表（description 归一化，按语义）
| 语义 | 同义词（词干子串，大小写不敏感）|
|---|---|
| **预期/预测** | `estimate`, `consensus`, `forecast`, `forward`, `predict`, `expect`, `smartestimate`, `projection` |
| **变动** | `change`, `revision`, `revise`, `shift`, `movement`, `drift` |
| **差异** | `difference`, `discrepancy`, `gap `, `deviation` |
| **方向（上调/下调）** | `upgrade`, `downgrade`, `raise`, `lower`, `increase`, `decrease`, `upward`, `downward` |
| **广度/计数** | `count`（⚠ 词边界）, `number of analysts` |
| **排名** | `percentile`, `rank`, `quantile` |
| **模型评分** | `model score`, `component`, `arm score`, `revision score`, `overall arm` |
| **比率** | `ratio`, `price-to-earnings`, `p/e`, `yield`, `price to`, `p e` |
| **意外** | `surprise` |
| **价格技术位** | `price change`, `moving average`, `week low/high`, `52week` |
| **实际** | `actual`, `reported` |
| **平均** | `average`, `mean`, `median` |
| **元数据** | `scaling factor`, `divisor`, `adjustment factor` |
| **相对指数** | `minus`, `index` + `return/relative` |

### ★ 最终分类结果：**16 个机制族 / 1026 字段（M13 其它仅剩 1 个）**
| 机制族 | n | cov中位 | aCnt=0 | cov=1.000 | 族内「cov最高+aCnt=0」代表 |
|---|---|---|---|---|---|
| **M5 预期估计变动率** | **244** | 0.624 | 229 | 0 | `avg_estimate_change_pct_current_year_sales_7d_long` (0.692) |
| **M4 模型评分分量** | **197** | 0.702 | 179 | **9** | `secondary_earnings_revision_component_medium_term_51` (**1.000**) |
| **M6 修正广度计数** | **147** | 0.702 | 128 | 0 | `count_smartestimate_analysts_quarterly_eps_long` (0.768) |
| **M7 估值比率** | 115 | 0.667 | 114 | 0 | `median_historical_f12m_pe_short_term` (0.751) |
| **M10 预期水平值** | 85 | 0.623 | 84 | 0 | `bold_estimate_flag_quarterly_eps_short_2` (0.768) |
| **M3 相对排名百分位** | 73 | 0.690 | 72 | **6** | `global_percentile_rank_long_term_5` (**1.000**) |
| **M1 评级变动** | 62 | 0.702 | 61 | **3** | `recommendation_change_component_medium_term_4` (**1.000**) |
| **M9 价格技术位** | 49 | **0.795** | 44 | 0 | `pct_change_from_52week_low_medium_term` (0.796) |
| **M14 实际报告值** | 17 | 0.636 | 0 | 0 | （aCnt 全 ≥1 ⇒ 已有人占）|
| **M12 标志位** | 12 | 0.792 | 12 | 0 | `model_new_activity_flag_short` (0.796) |
| **M8 意外度** | 7 | 0.421 | 7 | 0 | `predicted_surprise_flag_quarterly_eps_long_2` (0.768) |
| **M16 相对指数超额收益** | 7 | **0.795** | 7 | 0 | `price_change_vs_europe_index_30d_long_term` (0.795) |
| **M2 评级水平** | 4 | 0.711 | 4 | **2** | `mean_analyst_recommendation_prior_7d_short` (0.711) |
| **M15 元数据/缩放因子** | 3 | 0.441 | 3 | 0 | `divisor_quarterly_eps_long` (0.441) |
| **M11 增长率** | 3 | 0.562 | 3 | 0 | `five_year_historical_growth_rate_medium_term` (0.562) |
| **M13 其它（残留）** | **1** | 0.726 | 1 | 0 | `pct_diff_current_vs_historical_pe_medium_term` (0.726) |

### 第 1 层：零成本预筛（不发一枪仿真）
`field_type=MATRIX`（1026 个全是）→ `coverage` 降序 → `alpha_count=0` → `user_count` 升序。
实测：`cov=1.000` **18** / `0.75–1.0` **129** / `0.65–0.75` **549** / `0.4–0.65` **306** / `<0.4` **24**；
**`aCnt=0` 占 948/1026 = 92.4%** ⇒ 白空间极大、self 风险极低。

### 第 3 层：结构冻结的首波（8 槽）—— 只测「字段」一个变量
```
trade_when(greater(rank(adv20), 0.6),
  tail(group_rank(ts_sum(<FIELD>, 20), bucket(rank(cap), range="0,1,0.2")),
       lower=0.2, upper=0.8, newval=0.5), -1)      # MARKET · decay4 · trunc0.08
```
**8 槽配额（按 16 族取「体量最大或覆盖最高」）**：
| # | 字段 | cov | 族 |
|---|---|---|---|
| 1 | `secondary_earnings_revision_component_medium_term_51` | **1.000** | M4 |
| 2 | `global_percentile_rank_long_term_5` | **1.000** | M3 |
| 3 | `recommendation_change_component_medium_term_4` | **1.000** | M1 |
| 4 | `count_smartestimate_analysts_quarterly_eps_long` | 0.768 | M6 |
| 5 | `median_historical_f12m_pe_short_term` | 0.751 | M7 |
| 6 | `avg_estimate_change_pct_current_year_sales_7d_long` | 0.692 | M5 |
| 7 | `pct_change_from_52week_low_medium_term` | **0.796** | M9 |
| 8 | `price_change_vs_europe_index_30d_long_term` | **0.795** | M16 |

**优于抽样的量化**：随机抽 8/1026 命中 `cov=1.000` 概率仅 **13%**；分层 8 槽 **3/8 = 37.5%**、覆盖 8/16 机制族，且**结构冻结隔离变量**。

### 第 4 层：按族判死，不按字段判死
某族首字段 FAIL ⇒ **整族放弃**（16 族 ⇒ 一波砍掉该族全部字段）；某族过 ⇒ 第二波只扫该族**子轴**
（同一 desc 语义下的 `short/medium/long_term` × `_3/_4/_5/_41/_51` 后缀 × 不同 fiscal 期限 × 不同指标 earnings/revenue/ebitda/eps）。

### 抽样唯一更优的场景
字段集**无系统结构**（命名不反映机制、覆盖/拥挤度无差异、desc 归一化不出族）时才用抽样。
