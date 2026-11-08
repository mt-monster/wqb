# HKG / predictive_starmine 波次 1 模板池（2026-11-06）

## 为什么开这个面

1. **HKG 14 个塔全部未点亮**（连 pv 都只有 1），是当前未点亮塔最多的区域。
2. `predictive_starmine` 在 **GBR 已实证出货**：`3qV7Q2dO` S 1.77 / `RR62bMje` S 1.67 / `wpbRKA6l` S 1.69，
   全部 `prod<0.7`、`fRA=0` ⇒ 属「已验证可迁移配方」，优先在 HKG 复刻。
3. HKG 该集画像：**645 个字段、全部 MATRIX、coverage 0.71–0.88、alphaCount 普遍为 0–1（处女字段）**，
   平台总 alphaCount 仅 **9**、userCount **4** ⇒ 极低拥挤。
4. 该集在 HKG 归 **model 塔**（GBR 上 pyramids 亦为 model），可同时推进未点亮的 model 塔。

## 字段族（HKG 实测存在，`validate_expressions` 已确认 `unknown_fields=[]`）

| 族 | 字段 | 经济含义 |
|---|---|---|
| 估值收益 | `ep_yield_pct_smest_f12m` | 未来 12 个月预期盈利收益率 |
| 价格倍数 | `smest_price_ratio_fy2_revenue_3` | FY2 市销率预期 |
| 实际值 | `actual_last_year_earnings_2` / `_ebitda_2` / `_revenue_2` | 上年实际盈利/EBITDA/营收 |
| 分析师行为 | `analyst_downgrade_count_14d_2` | 14 日下调评级家数 |

## 10 个结构互异模板（差异落在骨架/矩/分组轴/非线性，不是换窗口）

| # | 模板 | 表达式骨架 | 差异维度 | 来源 |
|---|---|---|---|---|
| T1 | 水平偏移 + 行业排名 | `group_rank(ts_av_diff(ts_backfill(F,126),40), industry)` | 水平矩 + 一阶平滑差分 | GBR `RR62bMje` 实证 S1.67 |
| T2 | 目标换手衰减 + 一阶差分 | `group_rank(ts_target_tvr_decay(-rank(ts_delta(ts_backfill(F,500),11)), target_tvr=0.15), industry)` | 差分矩 + 换手约束 | GBR `3qV7Q2dO` 实证 S1.77 |
| T3 | 分析师行为 × 估值交互 | `group_rank(multiply(rank(ts_mean(analyst_downgrade_count_14d_2,66)), rank(ts_zscore(F,252))), sector)` | 双信号乘法交互 | 论坛《分析师预测分歧度——从一致预期的收敛中寻找Alpha》 |
| T4 | 实际 vs 预期错误定价 | `group_rank(divide(subtract(F, divide(actual_last_year_earnings_2, close)), abs(actual_last_year_earnings_2)), subindustry)` | 横截面价差（两字段） | 论坛《【Alpha 模板】分析师预期的动态估值因子》(15 票) |
| T5 | 二阶矩（离散度） | `group_rank(ts_std_dev(divide(F, ts_mean(F,252)), 66), industry)` | 二阶方差归一 | 论坛《分析师预测分歧度》 |
| T6 | 市值分桶内标准化 | `group_rank(ts_zscore(F,252), bucket(rank(cap), range="0,1,0.2"))` | 分组轴换成市值桶 | 论坛《机构持仓变化与拥挤反转》市值分桶归一化 |
| T7 | 长窗反转 | `reverse(group_rank(ts_zscore(ts_backfill(F,504),504), subindustry))` | 符号反转 + 504 长窗 | 自建（GBR `3qV7Q2dO` 已含 target 的 reverse 方向） |
| T8 | 三阶偏度 | `group_rank(ts_skewness(ts_zscore(F,66), 252), sector)` | 分布形态（三阶） | 自建（HKG 情绪面曾用偏度矩） |
| T9 | 变化率 + 目标换手 hump | `ts_target_tvr_hump(rank(ts_delta(ts_backfill(F,252),63)), target_tvr=0.2)` | 长差分 + hump 平滑 | GBR `d51O1kOX` analyst7 族结构 |
| T10 | 双实际值横截面差 | `subtract(rank(actual_last_year_ebitda_2), rank(ep_yield_pct_smest_f12m))` | 纯横截面 rank 差（零时序） | 论坛《分析师第一印象偏差因子》 |

**结构互异性自检**：水平 / 差分 / 交互 / 价差 / 二阶矩 / 桶分组 / 反转 / 三阶矩 / 长差分 / 纯横截面，
10 个模板在「矩阶 × 分组轴 × 非线性类型」三个维度上无重复 ⇒ 满足 ≥10 结构互异要求。

## 波次 1 已派发（2 条，批级设置单一）

- 批 id：`46PuSudgj59u9AXsq4M2GBQ`
- 设置：HKG / TOP800 / D1 / decay 4 / **SECTOR** / trunc 0.08 / unit VERIFY / **nan ON** / pasteurization ON / maxTrade OFF
- T1：`group_rank(ts_av_diff(ts_backfill(ep_yield_pct_smest_f12m, 126), 40), industry)`（算子 3）
- T2：`group_rank(ts_target_tvr_decay(-rank(ts_delta(ts_backfill(smest_price_ratio_fy2_revenue_3, 500), 11)), lambda_min=0, lambda_max=1, target_tvr=0.15), industry)`（算子 5）

验收判据（HKG LOW_SHARPE limit = 1.58，`checks.fail[].limit` 实读为准）：
- 任一条 |S| ≥ 1.0 ⇒ 该面有效，进第二代模板（T3–T10）
- 两条 |S| < 0.5 且 TO 落 5–30% ⇒ 该面在 HKG 无效，换面
- 两条 TO > 40% ⇒ 高频刷新噪声面，直接判死不救

## 与前两个 HKG 判死面的区分

| 面 | TO 实测 | |S| 实测 | 判据档位 |
|---|---|---|---|
| `news_sentiment_transfer` | 42–50% | ≤0.25 | 高频刷新噪声 ⇒ 判死 |
| `other553` | 45–47% | ≤0.51 | 高频刷新噪声 ⇒ 判死 |
| `fund_holdings_panel` | 1.65–2.24% | ≤0.42 | 慢变结构描述符 ⇒ 判死 |
| **`predictive_starmine`** | **10.6–11.0%** | **0.62** | **常规有效区（5–30%）⇒ 活，但不够强** |

## 波次 1 收批结果（批 `46PuSudgj59u9AXsq4M2GBQ`，2/2 COMPLETE，0 error）

| alpha | 模板 | S | F | TO | ret | 2Y | sub | fRA | 塔 |
|---|---|---:|---:|---:|---:|---:|---:|---:|---|
| `akKR2Zrv` | T1 `ep_yield_pct_smest_f12m` 水平偏移 | **0.62** | 0.37 | **11.01%** | 4.40% | 0.50 | **0.88** | 3 | HKG/D1/MODEL |
| `vR1YnMKz` | T2 `smest_price_ratio_fy2_revenue_3` 换手衰减+一阶差分 | 0.28 | 0.11 | 10.58% | 1.97% | 0.15 | 0.59 | 3 | HKG/D1/MODEL |

两条 `checks.fail` 均为 `LOW_SHARPE / LOW_FITNESS / LOW_2Y_SHARPE`，HKG 线 1.58。

## ★ 核心结论：TO 谱系三档第一次在 HKG 出现「常规有效区」

| HKG 已试面 | TO 实测 | |S| 最优 | 谱系档位 | 判决 |
|---|---|---|---|---|
| `news_sentiment_transfer` | 42–50% | 0.25 | 高频刷新噪声 | 判死 |
| `other553` | 45–47% | 0.51 | 高频刷新噪声 | 判死 |
| `fund_holdings_panel` | 1.65–2.24% | 0.42 | 慢变结构描述符 | 判死 |
| **`predictive_starmine`** | **10.6–11.0%** | **0.62** | **常规有效区（5–30%）** | **活，但不够强** |

⇒ **判据增量**：TO 落 5–30% 只说明「字段不是刷新率噪声、也不是恒定描述符」，
**不等于有足够信号**。`predictive_starmine` 是活面，但 |S| 0.62 距 1.58 差 **0.96**。

### 为什么 0.62 很难推到 1.58

1. **Sharpe 不受杠杆影响**（是收益/波动比）⇒ 放大仓位无效。
2. 单信号组合上界：两个 Sharpe 0.62 / 0.42、相关性 0 的信号组合后
   `sqrt(0.62² + 0.42²) = 0.75`，仍远低于 1.58 ⇒ **靠 HKG 现有弱信号堆叠到不了线**。
3. 同一模板在 GBR 上 `RR62bMje` 是 **S 1.67**，HKG 只有 0.62 ⇒ **HKG 该字段信号强度弱 1.05**，
   是区域属性不是骨架选错（模板已由 GBR 实证）。
4. `sub 0.88 > S 0.62` 说明小盘端更强，但 TOP800 已是 HKG 最大可用宇宙，没有更小合法宇宙可切。

### 处置

- **`predictive_starmine` 不判死**（TO 在常规区、方向符合「预期盈利收益率↑⇒收益↑」先验），
  但**不投入第二代 T3–T10**：10 个模板全做完的最好情况也只有 |S| ≈ 0.8–1.0，达不到 1.58。
- **HKG 降级为低优先级副战场**。已试 3 个面、覆盖 news/sentiment/institutions/model 四类，
  最优 |S| 0.62 ⇒ 该区字段面普遍弱，与「HKG 一个塔都未点亮」的现状互相印证。
- 保留 `3qoGgeZP`（fund_holdings, TO 1.65%）与 `akKR2Zrv`（starmine, TO 11%, sub 0.88）作为**低换手冷腿**储备。
- 209 个 HKG 数据集还剩 206 个未试，但按当前证据继续在 HKG 扫面属低 ROI；
  优先级地图已存 `hkg_unlit_dataset_priority_map_20261106.md`，留给后续有明确新机制假设时再开。

