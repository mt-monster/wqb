# DEU D1 核心数据集字段画像（2026-11-11，支撑 9 颗交付件）

> goal 第 2 条要求：对每个数据集全部字段做画像（类型/覆盖率/更新频率/分布/可用性）。
> 本文覆盖 9 颗交付件实际使用的 3 个核心数据集 + 3 个辅助族。

## 一、shortinterest3（借券数据，支撑 3 颗交付件）

| 属性 | 值 |
|---|---|
| 字段数 | **25** |
| 字段类型 | **全部 VECTOR**（须 `vec_avg` / `vec_sum` 聚合） |
| 覆盖率 | min 0.653 / median 0.687 / **max 0.783** |
| 更新频率 | 日频（`_p5_d1` 后缀 = 前 5 日滚动至 D1） |
| 支撑交付件 | 78Yk8VR1 / qM7KxkQV / Jj8VQwoe |

**高覆盖字段（cov=0.783）**：`average_loan_duration_days_p5_d1`、`loan_rate_volatility_p5_d1`、
`loaned_market_value_usd_p5_d1`、`loaned_share_count_p5_d1`、`max_loan_rate_p5_d1`、`mean_loan_rate_p5_d1`。

**关键发现**：`_p5_d1` 变体（cov 0.783）比基础版（cov 0.653-0.687）**覆盖率更高**，
而我此前 BE13b 测 `loan_rate_volatility` 用的是**基础版**（得 S1.40）。
⇒ **`_p5_d1` 变体是尚未系统利用的更高覆盖面**，值得后续在同类机制里优先选。

## 二、insiders1（内部人交易，支撑 1 颗交付件 qM7KxkQV）

| 属性 | 值 |
|---|---|
| 字段数 | **8** |
| 字段类型 | **全部 VECTOR** |
| 覆盖率 | 全部 **0.534**（一致） |
| 可用字段 | `insd1_holdings`（总持股）/ `insd1_shares`（交易股数）/ `insd1_value`（交易金额）/ `insd1_price` / `insd1_tradesignificance`（交易显著性）/ `insd1_gvkey` |

**机制**：`insd1_holdings` 是「内部人持股占总股本比例」，配合 `ts_rank(·, 252)` 得到 52 周持股位置。
高持股位置 = 内部人长期看多信号（Lakonishok-Lee 信息优势假说）。

## 三、other47（网站流量替代数据，支撑 1 颗交付件 Jj8VQwoe）

| 属性 | 值 |
|---|---|
| 字段数 | **18** |
| 字段类型 | **全部 VECTOR** |
| 覆盖率 | min 0.502 / median 0.652 / **max 0.652** |
| 更新频率 | 月频（SEMrush 口径） |

**高覆盖字段（cov=0.652）**：`oth47_organic_traffic`（自然流量月访问）、`oth47_organic_keywords`
（关键词数）、`oth47_organic_cost`（等效购买成本）、`oth47_rank`（SEMrush 排名）、
`paid_search_budget_estimate`、`paid_search_terms_count`。

**机制**：自然流量变化（`ts_delta` 66 日）反映基本面景气变化，取 `ts_quantile(·, 252)` 分位数位置
（做多流量改善股）。月频数据用 66 日差分可平滑掉季节性。

## 四、analyst 预估族（支撑 4 颗 ATOM 件）

| 数据集 | 支撑件 | 核心字段 |
|---|---|---|
| analyst（est_12m_*） | zq3eb7No / RREPm361 | `est_12m_ebt_mean`、`est_12m_pre_mean`、`est_12m_ebi_median` |
| anl93（分析师准确度） | GrW9OxmG | `anl93_recprofitabilityprev_estimator_profitability2` |
| analyst（预估变化） | rKRx2Alj / bl6AvMkN | `mean_estimate_change_pct_f12m_earnings_7d_4`、`netprofit_y1_estimate_change_3mo` |

**共性**：analyst 族字段是 MATRIX/VECTOR 混合，覆盖率普遍 0.5-0.7，更新频率为事件驱动（预估修正日）
非固定周期，因此须用 `ts_zscore(·, 240)` 或 `ts_mean(·, 长窗)` 做时间对齐。

## 五、可用性结论（对后续挖掘）

1. **DEU D1 的可用面高度集中在 VECTOR 类型**（3 个核心集全部 VECTOR），必须做 `vec_avg` 聚合；
2. **覆盖率天花板约 0.78**（shortinterest3 `_p5_d1`），低于 USA 类的 0.9+；
3. **`_p5_d1` 后缀变体覆盖率系统性更高**（0.783 vs 0.653），是未被利用的增量面；
4. 三个核心集的覆盖率换算到 TOP500 后，实际 longCount 约 149-160（qM7KxkQV 实测 149/146），
   与覆盖率 ~0.6 相符 ⇒ **平台 coverage 字段在 0.5-0.78 区间是可信的**；
   但在 fundamental89 上显示 0.0 却实际有数据，说明 **coverage=0 必须用回测 longCount 复核**。