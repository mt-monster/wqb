# analyst45 数据集分析文档（KOR / TOP600 / D1）

> 字段分类**一律以平台 `description` 为准**，字段名仅作索引，禁作语义依据。
> 画像源：`reference/field_profile/kor_analyst45_profile.json`（241 字段）
> 区域 KOR（不换）｜universe TOP600（本区唯一合法）｜delay 1

---

## 一、分析思路

1. **先用 description 做零假设重分类**，不看字段名 —— 字段名会骗人（description 是唯一语义依据）。
2. 与「按字段名分类」对照，**记录差异**（差异往往就是被漏掉的资产）。
3. 每类映射到经济学机制：说清「收益从哪来」，说不出的不进骨架。
4. 机制 → 骨架 → 候选；**骨架形态由体检体征决定，壳层由经济机制决定**。
5. 双通道取证（论坛 + 论文）后本区实测，结论回写本文档。

## 二、数据集总览

| 指标 | 值 |
|---|---|
| 字段总数 | 241 |
| 类型分布 | VECTOR 241 |
| coverage ≥ 0.5 | 0 / 241 |
| 白空间（alphaCount ≤ 2） | 225 / 241 |
| 平均 coverage | 0.2527 |

## 三、字段分类（★ 以 description 为准）

| 类 | 经济学角色 | 条数 | 覆盖 | 类型 | 白空间 |
|---|---|---:|---:|---|---:|
| **未分类** | — | 172 | 0 | VECTOR172 | 159 |
| **共识均值** | 预期水平 | 33 | 0 | VECTOR33 | 30 |
| **币种/元信息** | 元数据 | 30 | 0 | VECTOR30 | 30 |
| **已实现/实际值** | 事后真值 | 6 | 0 | VECTOR6 | 6 |

### 与「按字段名分类」的差异

| 字段名前缀 | 条数 |
|---|---:|
| `anl_` | 83 |
| `benchmark_` | 16 |
| `relative_` | 12 |
| `average_` | 6 |
| `investment_` | 6 |
| `realized_` | 6 |
| `reference_` | 6 |
| `total_` | 6 |
| `currency_` | 5 |
| `unrealized_` | 5 |
| `avg_` | 4 |
| `net_` | 4 |

> ⚠ 字段名分类**仅供参考**。凡名与 description 冲突的，一律以 description 为准；
> 差异条目须在下方逐条记录，因为差异往往指向被漏掉的信号结构。

## 四、类别 → 经济学骨架映射

### 共识均值 → 骨架：**预期水平 + 修正幅度**

- **收益来源**：共识的变化（非水平）是修正信号
- **合规/工程注意**：未缩放修正有效、缩放后失效（Jung 2019）
- **字段数**：33｜代表：`average_idea_age_period_2`, `anl45_avg_dur`, `average_idea_age_period`

### 币种/元信息 → 骨架：**—**

- **收益来源**：元数据，无收益来源
- **合规/工程注意**：不进信号；仅可作 group 参数
- **字段数**：30｜代表：`benchmark_currency_code_2`, `currency_of_investment`, `security_trading_currency_5`

### 已实现/实际值 → 骨架：**盈余惊喜 SUE（须与共识配对）**

- **收益来源**：实际 − 预期 = 惊喜，市场对惊喜反应不足
- **合规/工程注意**：配对相减属跨字段价差，须声明经济含义
- **字段数**：6｜代表：`anl45_real_ret`, `anl45_real_value`, `anl45_real_ret_today`

### ⚠ 未分类 172 条（须逐条人工判读）

- `absolute_price_change_today_2` ｜ Change in the stock price since the previous day’s close
- `adjusted_bias_return` ｜ Non-functional field; not in use
- `aggregate_realized_unrealized_return` ｜ Sum of realised and unrealised returns for the idea
- `anl45_avg_initial_prc_wfee` ｜ The avg initial price adjusted to include fee payment when fees are applied
- `anl45_beta` ｜ A measure of the volatility or systematic risk of a security compared to the market, updated monthly based on 
- `anl45_bias_weighted_ret` ｜ Non-Functional
- `anl45_bm_ret` ｜ Return of the benchmark index
- `anl45_bm_ret_wo_fx` ｜ Benchmark’s return excluding foreign exchange effects (raw benchmark return)
- `anl45_closed_prc` ｜ Price at which the idea was closed
- `anl45_current_inv` ｜ Current investment amount, including increases and partial closures
- `anl45_days_since_inception` ｜ Number of trading days since the idea was submitted
- `anl45_idea_count` ｜ Number of ideas in a group, useful when grouping ideas
- `anl45_index_period_end_prc` ｜ Benchmark or index end price for the selected performance period
- `anl45_index_period_start_prc` ｜ Benchmark or index start price for the selected performance period
- `anl45_index_ret_per` ｜ Return percentage had the investment been made in the selected index
- `anl45_initial_inv` ｜ Initial investment amount allocated to the idea
- `anl45_jensensalpha` ｜ Risk-adjusted performance measure representing return over market
- `anl45_latest_prc` ｜ The current price of the stock in the idea
- `anl45_limited_beta` ｜ Beta of the security relative to the market, updated monthly using ~20 months of data
- `anl45_limited_bias_weighted_ret` ｜ Non-Functional
- `anl45_limited_current_inv` ｜ Current invested amount in the idea, including increases and partial closures
- `anl45_limited_idea_count` ｜ Number of ideas in a group, useful for grouping views
- `anl45_limited_index_period_start_prc` ｜ Benchmark/Index start price based on the performance period you chose
- `anl45_limited_initial_inv` ｜ Initial investment amount for the Idea
- `anl45_limited_net_market_exposure` ｜ Net exposure to the market, difference between long and short values
- `anl45_limited_period_end_prc` ｜ Close price on day at end of selected period
- `anl45_limited_period_start_prc` ｜ Close price on day before start of selected period
- `anl45_limited_prc_change_today` ｜ Change in the stock price since the previous day’s close
- `anl45_limited_real_value` ｜ The value of realised (closed) parts of an idea
- `anl45_limited_risk_free_rate` ｜ The unrealised return on an open idea
- … 另有 142 条

## 四·补、字段质量先验（alphaCount TOP30 看轴）

> 依据 `brain-alpha-research-field-quality` §1：**高使用量字段揭示该数据集最强的经济轴**。
> 按 `alphaCount` 降序（同分按 `userCount`）取前 ~30 名看轴。**此步不可跳**。

| αC | users | cov | 字段 | description 摘要 |
|---:|---:|---:|---|---|
| 11 | 8 | 0.334 | `anl45_ad_rel_ret_per` | Average daily index relative return percentage |
| 10 | 4 | 0.308 | `anl45_jensensalpha` | Risk-adjusted performance measure representing return over market |
| 10 | 3 | 0.281 | `anl45_prc_change_today` | Change in stock price since previous day close |
| 9 | 4 | 0.358 | `anl45_avg_dur` | Average age of the idea limited to the selected period |
| 9 | 3 | 0.289 | `anl45_bm_ret` | Return of the benchmark index |
| 7 | 5 | 0.334 | `anl45_rel_index_ret_per` | Difference in return percentage between the idea and the comparative i |
| 7 | 2 | 0.358 | `anl45_net_market_exposure` | Difference in fractional total value between long and short ideas (net |
| 5 | 4 | 0.281 | `absolute_price_change_today_2` | Change in the stock price since the previous day’s close |
| 4 | 2 | 0.358 | `anl45_days_since_inception` | Number of trading days since the idea was submitted |
| 4 | 2 | 0.273 | `anl45_period_end_prc` | Close price on day at end of selected period |
| 4 | 2 | 0.276 | `anl45_period_start_prc` | Close price on day before start of selected period |
| 3 | 2 | 0.339 | `anl45_index_ret_per` | Return percentage had the investment been made in the selected index |
| 3 | 2 | 0.338 | `anl45_tot_ret_per` | Total return as a percentage of average investment |
| 3 | 1 | 0.214 | `anl45_latest_prc` | The current price of the stock in the idea |
| 3 | 1 | 0.281 | `anl45_ret_today` | Increase in realised return since last market close |
| 3 | 1 | 0.260 | `anl45_target_prc` | Author’s stated likely exit price for the idea |
| 2 | 2 | 0.276 | `anl45_avg_initial_prc_wfee` | The avg initial price adjusted to include fee payment when fees are ap |
| 2 | 2 | 0.358 | `anl45_idea_count` | Number of ideas in a group, useful when grouping ideas |
| 2 | 2 | 0.338 | `anl45_prc_change_per_today` | Percent change in stock price since previous close of day price |
| 2 | 2 | 0.333 | `anl45_rel_ret_per_today` | Relative return percentage today |
| 2 | 2 | 0.316 | `benchmark_fx_return_value_2` | Foreign exchange return made by the benchmark over the period |
| 2 | 1 | 0.258 | `anl45_stock_ret_per_relative` | Average daily return percentage had the investment been made in the re |
| 2 | 1 | 0.273 | `anl45_unreal_value` | Unrealised value of an open idea |
| 1 | 1 | 0.338 | `aggregate_return_percentage` | Total return over the idea’s lifetime expressed as a percentage of ave |
| 1 | 1 | 0.276 | `anl45_avg_initial_prc` | Average share price weighted by volume of each share purchase |
| 1 | 1 | 0.332 | `anl45_beta` | A measure of the volatility or systematic risk of a security compared  |
| 1 | 1 | 0.316 | `anl45_bm_fx_ret` | FX return made by the benchmark due to currency movements |
| 1 | 1 | 0.303 | `anl45_closed_prc` | Price at which the idea was closed |
| 1 | 1 | 0.358 | `anl45_current_inv` | Current investment amount, including increases and partial closures |
| 1 | 1 | 0.307 | `anl45_index_period_start_prc` | Benchmark or index start price for the selected performance period |

**★ 轴判读**（头部字段指向的经济轴，供人工确认 / 修正）：

- 头部字段集中于：`anl45_ad_rel_ret_per`(αC 11)；`anl45_jensensalpha`(αC 10)；`anl45_prc_change_today`(αC 10)；`anl45_avg_dur`(αC 9)；`anl45_bm_ret`(αC 9)
- ⇒ **开波前须先确认本集「最强轴」是否与拟挖方向一致**；
  若头部字段指向的轴与拟挖方向不同，**方向本身可能已偏**（见 analyst_consensus 打样实例）。

## 四·补二、字段画像五问与预处理决策

> 五问 = 测的是什么？怎么测的？时间维度（瞬时/累计/变化率）？为何存在？可靠性如何？

| 类 | 测什么 | 怎么测 | 时间维度 | 为何存在 | 可靠性 |
|---|---|---|---|---|---|
| 共识均值 | — | — | — | — | cov≥0.5 0/33；类型 VECTOR |
| 已实现/实际值 | — | — | — | — | cov≥0.5 0/6；类型 VECTOR |

**预处理决策（由画像推导，不由拍脑袋）**：

| 画像读数 | 预处理决策 | 依据 |
|---|---|---|
| VECTOR 占比高 | **必须 `vec_avg`/`vec_sum` 降维** | 裸用 `rank`/`ts_*` 秒拒；一条错整批 CANCELLED |
| cov < 0.4 的字段 | 先 `ts_backfill`/`group_backfill` | 体检硬门检查 1 |
| 季频更新（报告日） | 窗口下限 ≥ 63d | 窗口低于更新周期 = 噪声 |
| 单边恒正 | 改变化率 | 体检读数映射 |
| 离散评分型 | 禁 `winsorize`/`signed_power` | 无连续尾部，零效果 |

## 五、本区实测与死因

> **待回填**：本数据集在 KOR/TOP600/D1 的实测读数（S / TO / RN_S / 2Y）与死因归因。
> 死因判据三条：① TO 是否 <0.10（近静态）；② 有效持仓占比；③ risk_neutralized_S vs raw_S。
> ⚠ 预筛更严版：**TO < 0.03 的候选连差分都不要做**（差分只会更低）。

## 六、双通道取证

- **通道 A（论坛）**：`search_forum_posts` 长中文 query 会炸，砍短关键词；`read_forum_post` 必传 `include_comments=false`（true 会 30s 超时）。
- **通道 B（论文）**：`domain_search`。
- **待回填**：本数据集相关的论坛模板与文献机制。

## 七、下一步

> **待回填**：本数据集尚未证伪的假设、下一波设计（须满足铁律 G：候选数 ≤ 上波 1/3，且写明继承/准入/收窄）。
