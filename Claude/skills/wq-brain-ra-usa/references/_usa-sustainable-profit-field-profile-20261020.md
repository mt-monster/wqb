# 数据集画像：`sustainable_profit`（USA / D1 / TOP3000）

> as_of 2026-10-20。未点亮 **other** 塔（`USA/D1/OTHER` multiplier 1.4；未点亮）。
> 选入理由：USA `other` 类 56 集中**字段数最多（122）且拥挤度中低（数据集 aC 101 / uC 65 / valueScore 5）**、
> `get_dead_ends(USA)` 33 条无任何条目覆盖、经济语义可直接陈述（可持续盈利能力 = 经常性利润 × 稳定性）。
> 结构：**全部 122 字段均为 VECTOR**（无 MATRIX / GROUP），必须先 `vec_avg` 聚合再进标量算子。

## 0. 数据集元数据

| 项 | 值 | 来源 |
|---|---|---|
| dataset id | `sustainable_profit` | `get_datafields` |
| 字段数 | 122（全部 VECTOR） | 同上 |
| 覆盖率 | 0.5219–0.6493（数据集中位数 ≈0.61） | 同上 |
| 字段级拥挤 | aC：0 占 80%+；最高 `gross_profitability_net_operating_assets` 65（uC 43）、`cash_flow_return_on_noa` 19、`operating_asset_turnover_ratio` 16 | 同上 |
| 数据集拥挤 | aC 101 / uC 65 / valueScore 5 | `get_datasets(category=other)` |
| 更新频率 | 财报驱动（TTM 比率 + YoY 变化），季度更新；无日频字段 | 字段描述 |
| 平台过滤 | `sharpe_filter_removed = 0`（未被平台按 Sharpe 预筛掉任何字段） | `get_datafields` |
| 塔位 | `USA/D1/OTHER`（未点亮） | `get_pyramid_alphas` / 画像先验 |

**机制文献锚**：Novy-Marx (2013) gross profitability；Ball, Gerakos, Linnainmaa & Nikolaev (2016, 2020)
operating profitability / **recurring vs transitory income**；Asness, Frazzini & Pedersen (2019) QMJ
（profitability / growth / **stability** 三支柱）；Cooper, Gulen & Schill (2008) asset growth；
Sloan (1996) 盈余质量（暂时性利润反转）。

## 1. 字段画像（全 122 字段，按机制族分组）

> 覆盖率为字段级 coverage；aC/uC 为该字段的 platform alphaCount / userCount（仅列非零者）。
> 所有字段都需 `vec_avg(...)`；VECTOR 维度按描述应为同一比率的多个报告期/口径取值，取均值即 TTM 水平。

### 1.1 盈利能力水平（Levels，21）

| 字段 | cov | aC |
|---|---:|---:|
| `operating_return_on_noa` | 0.6193 | 0 |
| `operating_return_on_operating_assets` | 0.6192 | 0 |
| `operating_return_on_assets_ratio` | 0.6212 | 0 |
| `operating_return_on_equity` | 0.6212 | 0 |
| `operating_return_on_invested_capital` | 0.6212 | 0 |
| `operating_return_on_net_capital` | 0.6193 | 0 |
| `operating_return_on_invested_assets` | 0.6465 | 0 |
| `recurring_return_on_assets` | 0.6212 | 1 |
| `recurring_return_on_equity` | 0.6212 | 0 |
| `recurring_return_on_invested_capital` | 0.6212 | 0 |
| `recurring_return_on_noa` | 0.6193 | 0 |
| `recurring_return_on_operating_assets` | 0.6192 | 0 |
| `recurring_return_on_noncore_capital` | 0.6193 | 0 |
| `return_on_noncore_capital` | 0.6465 | 1 |
| `return_on_operating_assets` | 0.6464 | 0 |
| `transitory_return_on_equity` | 0.6212 | 0 |
| `cash_flow_return_on_noa` | 0.6465 | 19 |
| `cash_flow_return_on_operating_assets` | 0.6464 | 2 |
| `net_nonoperating_net_assets` | 0.6487 | 0 |
| `gross_profitability_net_operating_assets` | 0.6465 | 65 |
| `gross_profitability_operating_assets` | 0.6464 | 5 |

### 1.2 盈利能力变化（YoY，25）

`operating_return_on_noa_change` 0.5775 · `operating_return_on_assets_change` 0.6038 ·
`operating_return_on_equity_change` 0.6037（aC1） · `operating_return_on_invested_capital_change` 0.6038 ·
`operating_return_on_operating_assets_change` 0.5773（aC1） · `operating_return_on_noncore_change` 0.5775 ·
`recurring_return_on_assets_change` 0.6038 · `recurring_return_on_equity_change` 0.6037 ·
`recurring_return_on_invested_capital_change` 0.6038 · `recurring_return_on_noncore_capital_change` 0.5775 ·
`recurring_return_on_operating_assets_change` 0.5775 · `recurring_rooa_yearly_change` 0.5773 ·
`return_on_net_operating_assets_change` 0.5992 · `return_on_noncore_capital_change` 0.5992（aC1） ·
`return_on_operating_assets_change` 0.599（aC2） · `transitory_return_on_equity_change` 0.6037（aC4） ·
`cash_flow_return_noa_change` 0.5992 · `cash_flow_return_on_operating_assets_change` 0.599 ·
`gross_profitability_noa_change` 0.5992（aC1） · `gross_profitability_oa_change` 0.599 ·
`net_nonoperating_net_assets_change` 0.6449 · `nopat_margin_change` 0.6025（aC1） ·
`nopat_as_percent_change` 0.6038 · `operating_asset_turnover_change` 0.599 ·
`operating_asset_turnover_next_year_change` 0.5928（aC1）

### 1.3 利润率（4）

`nopat_profit_margin` 0.6199 · `recurring_profit_margin` 0.6199 ·
`net_operating_profit_margin_percent` 0.6212 · `recurring_profit_margin_change` 0.6025

### 1.4 增长（23）

`net_operating_assets_growth_rate` 0.5992 · `net_operating_assets_per_share_growth` 0.599 ·
`operating_assets_growth_rate` 0.5992 · `operating_assets_per_share_growth` 0.5989 ·
`operating_liabilities_growth_rate` 0.6426 · `operating_liabilities_per_share_growth` 0.6369 ·
`nonoperating_liabilities_growth_rate` 0.635 · `nonoperating_liabilities_per_share_growth` 0.6295 ·
`nonoperating_asset_growth_rate` 0.6426 · `nonoperating_assets_per_share_growth` 0.637 ·
`net_nonoperating_asset_growth` 0.6452 · `net_nonoperating_assets_per_share_growth` 0.6396 ·
`financial_assets_growth_rate` 0.522 · `financial_assets_per_share_growth` 0.5219 ·
`net_capital_growth_rate` 0.5993 · `net_capital_per_share_growth` 0.599 ·
`net_financial_assets_growth_rate` 0.6167 · `nopat_per_share_growth` 0.6008 ·
`net_operating_profit_growth_rate` 0.6039 · `recurring_income_growth_rate` 0.6039 ·
`recurring_income_per_share_growth` 0.6008 · `transitory_income_growth_rate` 0.5633 ·
`nonoperating_income_growth_rate` 0.6342

### 1.5 杠杆与融资（19）

`net_debt_to_equity_ratio` 0.648 · `net_debt_to_equity_change` 0.6017 ·
`new_debt_to_net_capital` 0.6465 · `new_debt_to_net_capital_change` 0.5992 ·
`long_term_debt_to_net_capital` 0.6465（aC1） · `long_term_debt_to_net_capital_change` 0.5992 ·
`net_borrowing_cost_ratio` 0.647 · `financial_return_spread` 0.6182 ·
`external_funding_of_noa` 0.6465（aC6） · `external_funding_noa_change` 0.5992 ·
`operating_funding_ratio` 0.6464 · `operating_creditor_funding_ratio` 0.6464 ·
`cash_flow_to_debt_ratio` 0.6054 · `cash_flow_to_operating_liabilities` 0.6456（aC1） ·
`financial_leverage_impact_on_returns` 0.6182（aC1） · `nonoperating_activities_impact` 0.6192 ·
`nonoperating_activities_scale` 0.6491 · `nonoperating_return_spread` 0.6192 ·
`financial_expense_coverage_ratio` 0.5995

### 1.6 盈利稳定性（9）— 本集的差异化字段族

`operating_assets_return_relative_volatility` 0.6368 · `operating_return_on_assets_volatility` 0.6094（aC1） ·
`operating_roa_relative_volatility` 0.6039（aC1） · `operating_rooa_relative_volatility_2` 0.6072 ·
`operating_roe_volatility` 0.6089 · `recurring_roa_volatility` 0.6094（aC1） ·
`recurring_roe_volatility` 0.6089 · `recurring_rooa_relative_volatility` 0.6073 ·
`recurring_return_on_assets_relative_volatility` 0.6039（aC1）

### 1.7 暂时性 / 非经营性利润与亏损频率（8）

`mean_transitory_income_to_sales_ratio` 0.6113 · `mean_transitory_income_to_sales_change` 0.5974 ·
`mean_nonoperating_income_to_sales_ratio` 0.6325 · `mean_nonoperating_income_to_sales_change` 0.6256 ·
`negative_nonoperating_income_frequency` 0.6493 · `negative_nopat_frequency` 0.6493（aC1） ·
`negative_recurring_income_frequency` 0.6493（aC1） · `negative_transitory_income_frequency` 0.6493

### 1.8 资产结构与周转（11）

`operating_asset_turnover_ratio` 0.6464（aC16） · `operating_asset_turnover_next_year` 0.6403（描述仅 "Revenue"，口径可疑） ·
`net_operating_assets_percent` 0.6465 · `operating_assets_as_percent_total_assets` 0.6465 ·
`financial_assets_as_percent_total_assets` 0.6481（aC2） ·
`nonoperating_assets_as_percent_total_assets` 0.6491（aC1） · `net_nonoperating_assets_percent` 0.6491（aC1） ·
`nonoperating_assets_percent` 0.6244 · `net_financial_assets_percent` 0.6244 ·
`net_operating_assets_to_cogs_ratio` 0.6274（aC1） · `operating_assets_to_cogs_ratio` 0.6274

### 1.9 其他变动（2）

`net_financial_assets_percent_change` 0.6069 · `nonoperating_assets_percent_change` 0.6069

### 1.10 画像结论（可用性）

1. **无日频字段**：全部为财报比率的 TTM 水平或 YoY 变化，最低覆盖 0.522，最高 0.649 ⇒ 必须
   `ts_backfill(vec_avg(...), 252)`；覆盖率 ≈0.6 在 USA/TOP3000 仍可交易约 1800 只，不触 CW 墙。
2. **aC 极低（>80% 字段为 0）**：未被社区消耗，prod 先验**低**；但同时说明「无既有配方」，不能照抄论坛。
3. **盈利稳定性（1.6）是唯一「可持续」字面相关的字段族**（9 字段，全部 aC≤1），是本文最值得先测的差异化轴。
4. **1.4 增长族与 1.5 融资族高度同构**（NOA/OA/净资本/每股四套版本），16 探针内只需各取 1–2 个代表字段。
5. `operating_asset_turnover_next_year` 的描述与名字不符（仅 "Revenue"）⇒ 不直接使用，改用它带 `_change` 的字段。

## 2. 适用模板（机制优先，模板不封顶 8 个）

> 通用壳：`quantile(group_rank(winsorize(ts_backfill(vec_avg(<SIG>), 252), std=4), industry))`；
> 分组轴 industry（本区先验劣于 subindustry 只在中性化层面；分组轴 industry 在分析师族已复证）。
> 所有机制均**单数据集**（ATOM 合规：非豁免字段全部来自 `sustainable_profit`）。

| 码 | 机制 | 经济陈述（收益从哪来） | 代表字段 | 方向 | 预期失败模式 |
|---|---|---|---|---|---|
| **M1** | 可持续盈利水平 | 高 RNOA 公司持续赚取超额回报，市场低估其持续性 | `operating_return_on_noa` | + | prod 高（质量族饱和）、rns≈0 |
| **M2** | 经常性盈利水平 | 剔除暂时性项目后的核心盈利能力更可外推 | `recurring_return_on_assets` | + | 与 M1 高度相关（同族对照） |
| **M3** | 盈利稳定性 | 盈利波动低的公司现金流更可预测，享有持续性溢价（QMJ stability） | `operating_roa_relative_volatility`、`recurring_roa_volatility` | − | S 偏低、TO 低 |
| **M4** | 投资 / 资产扩张 | 资产扩张速度快的公司后续回报低（CGSchill） | `net_operating_assets_growth_rate` | − | 已被广泛定价 ⇒ prod 高 |
| **M5** | 暂时性利润占比（盈余质量） | 利润中暂时性成分高 ⇒ 不可持续、后续反转 | `mean_transitory_income_to_sales_ratio` | − | 信号稀、TO 低 |
| **M6** | 亏损频率（困境） | 负 NOPAT 季度占比高 ⇒ 盈利持续性差、风险溢价被高估 | `negative_nopat_frequency` | − | 与规模/困境风格重合，rns≈0 |
| **M7** | 财务利差 | 经营回报率高于净借款成本 ⇒ 真实价值创造 | `financial_return_spread` | + | 覆盖 0.6182，弱于 M1 |
| **M8** | 经营融资结构 | 依靠经营负债融资（无息）的公司资本效率更高 | `operating_funding_ratio` / `operating_creditor_funding_ratio` | +/− | 机制弱、方向先验不清 ⇒ 留第二批 |
| **M9** | 利润率扩张 | 经常性利润率 YoY 扩张 ⇒ 经营杠杆释放 | `recurring_profit_margin_change` | + | 与 M1/M2 相关 |
| **M10** | 前瞻营收 / 周转 | FY1 营收变化 ⇒ 需求加速 | `operating_asset_turnover_next_year_change` | + | 描述口径可疑，需单独核 |

### 2.1 批 1 设计（8 探针，6 个机制）

| # | 机制 | 字段 | 方向 | 表达式 |
|---|---|---|---|---|
| S1 | M1 | `operating_return_on_noa` | + | 通用壳 |
| S2 | M2 | `recurring_return_on_assets` | + | 通用壳 |
| S3 | M3 | `operating_roa_relative_volatility` | − | 通用壳 + 前置负号 |
| S4 | M3b | `recurring_roa_volatility` | − | 通用壳 + 前置负号 |
| S5 | M4 | `net_operating_assets_growth_rate` | − | 通用壳 + 前置负号 |
| S6 | M5 | `mean_transitory_income_to_sales_ratio` | − | 通用壳 + 前置负号 |
| S7 | M6 | `negative_nopat_frequency` | − | 通用壳 + 前置负号 |
| S8 | M7 | `financial_return_spread` | + | 通用壳 |

设置：USA / TOP3000 / D1 / **SUBINDUSTRY** / decay 5 / trunc 0.08 / VERIFY / nan ON /
pasteurization ON / maxTrade OFF / validate_fields false。
multisim：`2jI6ez5Gf4vZbtJzMYBhqfW`（2026-10-20 发批）。

**预注册止损**（发批前固定，收批后不得改）：
- 全批 `|S| < 1.0` ⇒ 判弱封存，不补批（同 earnings_risk / insiders4 纪律）；
- 任一机制 `|S| ∈ [1.25,1.58)` 且其余闸健康 ⇒ 该机制进 Mode A / 壳层加强（唯一允许的补批理由）；
- 任一全闸候选 ⇒ 立即 `check_correlation(refresh=True)` 实测 prod；`[0.8,0.9)` n≥1 或 `[0.9,1]` n≥10 ⇒ 按 D0-P 判族级，不磨参数；
- 稳定性族（M3）若 S 低但 `rns ≥ 0.5` ⇒ 登记为「低 S 高特异」慢腿，不在本集强行磨 S。

### 2.2 论坛与文献取证（2026-10-20 `search_forum_posts` 实检）

| 来源 | 关键内容 | 对本集的意义 |
|---|---|---|
| 【Alpha灵感】基于企业毛利润率的因子构建（JS29024, 2025-12-07, 14 赞 / 7 评） | 基于 *Profitability, R&D Investments and the Cross-Section of Stock Returns* 构建毛利率因子 | 毛利 / GPA 族在社区**高度普及** ⇒ 水平类 prod 先验高；本批刻意避开 `gross_profitability_*` 字段（该集 aC 最高的两个恰是它们） |
| 【Alpha Idea】KOR 毛利单字段：先看自身历史位置，再处理换手（JB71859, 2026-09-26, 28 赞） | Novy-Marx (2013) 毛利资产比；做法是**先看自身时序位置（ts_rank），再单独处理换手** | 与本区 board_gov `ts_rank504` 经验一致：慢基本面的最优测量面常是自身历史位置而非原始水平 ⇒ 批 1 若水平构造失败，第二批允许**一次性**换到 `ts_rank(...,504)` 口径 |
| 【Alpha灵感】Quality Minus Junk-inspiration（BC52452, 2023-10-29, 11 赞） | QMJ 用 profitability / growth / safety 三支柱描述质量 | 机制映射外部锚：M1/M2 = profitability，M3 = safety/stability，M4 = growth（负向） |
| 【Alpha灵感】研发投入、盈利能力与股票回报（BB13527, 25 赞） | 主因子 `rank(GPA)`，并讨论 R&D 数据口径问题 | 再次确认 GPA 截面 rank 是社区模板级做法 |
| 【Alpha灵感】盈利不确定性和公司关注度（DZ54968） | 盈利不确定性溢价**只在高关注度股票显著** | ATOM 禁跨数据集 attention 门控 ⇒ 该放大器在本约束下不可用（与 `earnings_risk` IV skew 同一结论，**第二次复证**） |
| 【论文合集】量化研究推荐论文（KJ42842, 107 赞） | 列 *Earnings Quality on the Street*、*Earnings Volatility* 等 | 支持 M3（波动稳定性）/ M5（盈余质量）的文献路径 |

**跨区警示**：KOR 配方不能直接迁移 USA（`insider_trx_matrix` 的 ILLIQUID universe 结构性不可复现、`MFRP` 跨区先例）；
上表只取**方法论**（测量面选择、机制拆分），不取参数与阈值。

## 3. 回测结果

### 3.1 批 1（multisim `2jI6ez5Gf4vZbtJzMYBhqfW`，8 条，2026-10-20 收齐 8/8 COMPLETE）

设置：USA / TOP3000 / D1 / SUBINDUSTRY / decay 5 / trunc 0.08 / VERIFY / nan ON /
pasteurization ON / maxTrade OFF。壳：`quantile(group_rank(winsorize(ts_backfill(vec_avg(<SIG>), 252), std=4), industry))`。

| # | 机制 | alpha | 字段 | S | F | 2Y | SUB | TO | returns | DD | rns | 失败闸（RA） |
|---|---|---|---|---:|---:|---:|---:|---:|---:|---:|---:|---|
| S1 | M1 | `2rjNlX8b` | `operating_return_on_noa` (+) | 0.59 | 0.34 | 1.00 | 0.52 | 1.67% | 4.15% | 28.87% | **0.00** | SHARPE / FITNESS / 2Y |
| S2 | M2 | `A1Q7lrjY` | `recurring_return_on_assets` (+) | 0.56 | 0.33 | 0.97 | 0.46 | 1.42% | 4.39% | 33.53% | **−0.01** | SHARPE / FITNESS / 2Y |
| S3 | M3 | `1Yjzwlkz` | `operating_roa_relative_volatility` (−) | **0.97** | 0.60 | **1.50** | 0.64 | 1.29% | 4.78% | **7.16%** | **0.36** | SHARPE / FITNESS / 2Y |
| S4 | M3b | `gJW9jgke` | `recurring_roa_volatility` (−) | 0.71 | 0.39 | 1.33 | 0.56 | 1.21% | 3.83% | 17.63% | 0.29 | SHARPE / FITNESS / 2Y |
| S5 | M4 | `0mjMwNO6` | `net_operating_assets_growth_rate` (−) | 0.64 | 0.37 | 1.21 | 0.37 | 2.64% | 4.13% | 18.29% | −0.19 | SHARPE / FITNESS / 2Y |
| S6 | M5 | `kqJZjWEz` | `mean_transitory_income_to_sales_ratio` (−) | 0.78 | 0.43 | 1.18 | 0.55 | 1.27% | 3.88% | 7.02% | 0.12 | SHARPE / FITNESS / 2Y |
| S7 | M6 | `akVE7Q6v` | `negative_nopat_frequency` (−) | **0.23** | 0.08 | 0.74 | 0.17 | 1.29% | 1.60% | **36.12%** | **−0.55** | SHARPE / FITNESS / 2Y |
| S8 | M7 | `LL5d7mWn` | `financial_return_spread` (+) | 0.58 | 0.33 | 1.00 | 0.54 | 1.80% | 3.97% | 28.28% | **0.00** | SHARPE / FITNESS / 2Y |

共性：**8/8 全部通过 LOW_TURNOVER / HIGH_TURNOVER / CONCENTRATED_WEIGHT / LOW_SUB_UNIVERSE_SHARPE /
MATCHES_PYRAMID**（SUB 0.17–0.64 全过，因 SUB 门槛随 S 走 ≈0.43×S）；CLUSTER_TEST 0.19–0.75 全不拥挤；
失败项结构完全一致（SHARPE + FITNESS + 2Y）⇒ **构造层问题，不是设置层或多样性层问题**。
longCount 1212–1441 / TOP3000，无形变集中。

## 4. 归因（收批后立即，未再发批）

**A1｜水平盈利族是纯风格 beta，不是弱 alpha。** M1/M2/M8 三条 S 0.56–0.59，而
`risk_neutralized_sharpe` = **0.00 / −0.01 / 0.00**，DD 全部 28–34%。剥离风格后信息归零，
这与 value/quality/book 在 USA 的饱和先验完全一致；也复证 `USA-GEM-QUANTILE-WRAPPER-DEAD`
里「水平质量类配裸壳在 USA 结构性太弱」。**故论坛给的 `ts_rank(...,504)` 换测量面在本族
不成立**：失败原因不是测量面（水平 vs 自身历史位置），而是**去掉风格后没有剩余信息**
——换 ts_rank 只改变风格暴露的时点，不会造出特异信息。

**A2｜稳定性族（M3）是本集唯一有特异信息的轴，但不足以成 alpha。**
`operating_roa_relative_volatility`（−）S0.97 / F0.60 / **2Y 1.50**（距闸 0.08）/ SUB0.64 /
**DD 7.16%（全批最低，仅为水平族的 1/4）** / TO1.29% / **rns 0.36（全批最高）**。
方向与 QMJ「safety/stability」支柱一致：稳定盈利公司风险调整后更优。但 S 距 1.58 差 0.61，
且 rns 0.36 **未达预注册的 0.5 慢腿线** ⇒ 按 §2.1 不进补批、不登记慢腿。

**A3（新方法论）｜稳定性必须用「相对波动」，不能用「绝对波动」。** M3 vs M3b 同机制同方向：
0.97/2Y1.50/DD7.16% vs 0.71/2Y1.33/DD17.63%。相对波动（operating ROA relative volatility）
已剔除行业/规模波动水平，是更干净的 stability 测量面；绝对波动（recurring ROA volatility）
混入规模与行业波动 ⇒ 信息被稀释、回撤翻倍。后续任何「稳定性」类构造优先取 `*_relative_*` 口径。

**A4｜盈余质量（M5）有微弱特异信息但不够。** 暂时性利润占比（−）S0.78 / 2Y1.18 / DD7.02% /
rns0.12 / TO1.27%。TO 刚过 1% 线（全批最薄），说明字段更新慢（季度）；S 与 2Y 同时不足 ⇒
`mean_transitory_income_to_sales_ratio` 的单字段截面区分度有限，若要复用只能作组合腿。

**A5｜投资因子（M4）反向暴露不是 alpha。** 资产扩张（−）S0.64 但 **rns −0.19**、SUB 0.37（全批最低）。
「低扩张」组在剥离风格后反而跑输 ⇒ 该构造实际是多低 beta / 大盘的代理，与 CG-Schill 的投资效应
在 USA 已被套利掉一致。**不要再用「反向投资」当独立质量信号**。

**A6｜亏损频率（M6）是困境/信用 beta，且方向被宏观主导。** S0.23 / DD36.12% / **rns −0.55（全批最负）**。
rns 的符号与量级说明：负 NOPAT 频率高的公司不是「被低估的困境反转」，而是纯 distress 暴露；
ATOM 纪律下不能用宏观/信用对冲腿，故该机制在本约束内**结构性不可用**。

**A7｜换手不是本集的限制项。** TO 1.21–2.64% 全部高于 LOW_TURNOVER 1%，慢基本面 + decay5
在本数据集不触发换手闸（与 workforce/board 的情形不同）。⇒ 后续同族数据集不必先做「抬 TO」批，
应直接回答 S 是否有特异信息（先看 rns）。

**A8｜覆盖率不是问题。** cov 0.52–0.65 经 `ts_backfill(...,252)` 后 longCount 1212–1441，
无 CW / 无集中持仓；`vec_avg` 两段式聚合正常（122 字段全 VECTOR）。

## 5. 决策

**❌ 判弱封存：`USA-SUSTAINABLE-PROFIT-WEAK`（1 批 / 8 条）。** 触发 §2.1 预注册止损第一条
（全批 |S| < 1.0，最高 0.97），**不发第 2 批、不磨窗口/中性化/decay**。

- 本集**不登记慢腿**：M3 的 rns 0.36 < 预注册门槛 0.5；仅在本画像留档（S0.97 / 2Y1.50 / DD7.16% /
  TO1.29%），若未来做 SUPER 或组合层再评估。
- 不写 DB `dead_end`：本判定基于结构证据（rns≈0、S 上限），**无可靠 `forum_recon_*` 取证**；
  按 pv63 / pv115 先例只做文档级封存，不 `force_seal`。
- **可复用结论**：① 质量族在 USA 的唯一活口是「相对波动」稳定性，但单字段上限 ~1.0；
  ② 一切水平型盈利字段先看 rns，≈0 就别换壳；③ 亏损频率 = distress beta，排除。

**下一个数据集**：`equity_kpi_forecast`（22 字段 / cov 0.3717 / aC 139 / valueScore 5，未点亮 other 塔）。
切换理由：sustainable_profit 已按预注册止损封存，6 个机制 × 8 探针全部 |S|<1.0，构造层无可用轴。
