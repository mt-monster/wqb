# other47（Web Intelligence / SEMrush 网站流量）— GBR/TOP700/D1 模板库

> 建立日期：2026-10-30　区域：GBR / universe TOP700 / delay 1
> 目的：为**纯 OTHER 塔**找零配额入口（OTHER 塔当前 GBR/D1 仅 1 颗，需 3 颗点亮）
> 模板数量：**10 个结构互异模板 + 2 个备用**，来源标注见每行

---

## 0. 一个必须记住的认知纠正

**`other47` 的官方 name/description 是错的。** 平台写的是
"Web Intelligence Data … mapping between Bloomberg IDs and Reuters Instrument Codes（RIC/BBID 映射）"，
实际字段全部是 **SEMrush 网站流量与搜索广告**指标。同类问题在 `other250` / `other296` / `other315` /
`other323` / `other424` / `other425` / `other455` / `other567` / `other734` / `other78` 上也都出现
（描述被同一套 RIC/BBID 模板文案污染）。

⇒ **判断数据集内容只能看 `get_datafields` 的字段名 + 字段描述，绝不能信数据集级的 description。**

## 1. 字段清单（`get_datafields(dataset_id="other47", region="GBR", universe="TOP700", delay=1)` 实读）

全部 **VECTOR** 类型（必须过 `vec_*` 聚合才能进 `ts_*` / `divide` / `rank`）。共 18 个，分两档覆盖：

### 档 A — coverage **0.6068**（9 个，优先用）

| 字段 ID | 单位 | 语义 | 平台 alphaCount |
|---|---|---|---|
| `oth47_organic_traffic` | visits | 自然搜索月访问量（**注意力水平主信号**） | 2 |
| `oth47_organic_keywords` | count | 自然搜索排名关键词数（**信息需求宽度**） | 1 |
| `oth47_organic_cost` | USD | 买等量自然流量的广告成本（注意力"价格"） | 0 |
| `oth47_rank` | rank | SEMrush 自然流量排名，**越低越可见** | 3 |
| `paid_search_budget_estimate` | USD | Google Ads 月支出（**广告强度**） | 1 |
| `paid_search_terms_count` | count | 付费关键词数 | 0 |
| `paid_search_visitors` | visits | 付费广告月访问量 | 2 |
| `product_listing_ad_terms` | count | PLA 关键词数 | 0 |
| `unique_product_listing_ads` | count | PLA 唯一关键词数 | 0 |

### 档 B — coverage **0.4275**（9 个 `*_enriched`，备用，覆盖更稀）

`organic_search_budget_enriched` / `organic_search_terms_enriched` / `organic_search_visitors_enriched` /
`paid_search_budget_estimate_enriched` / `paid_search_terms_count_enriched` / `paid_search_visitors_enriched` /
`product_listing_ad_terms_enriched` / `unique_product_listing_ads_enriched` / `website_traffic_rank_enriched`

### ★ 命名陷阱（本轮实测踩到）

**同一数据集内前缀不统一**：只有 4 个字段带 `oth47_` 前缀（`oth47_organic_traffic` /
`oth47_organic_keywords` / `oth47_organic_cost` / `oth47_rank`），其余 5 个是**裸名**
（`paid_search_budget_estimate` 等）。
⇒ 写表达式前**必须原样复制 `get_datafields` 返回的 `id`**，不能自己加前缀，也不能靠"看起来像"推断。
（教训来源：本轮首次 preflight 我把 `paid_search_budget_estimate` 写成
`oth47_paid_search_budget_estimate`，被判 `unknown_soft`——平台判得对，是我错。）

## 2. 学术依据（按模板引用）

| 文献 | 结论 | 对应模板 |
|---|---|---|
| **Da, Engelberg & Gao (2011), "In Search of Attention", Journal of Finance 66(5)** | ASVI（异常搜索量指数）在短期预示更高收益，随后反转；散户注意力驱动的净买入造成价格压力 | W1, W2 |
| **Preis, Moat & Stanley (2013), "Quantifying Trading Behavior in Financial Markets Using Google Trends", Sci. Rep.** | 搜索量变动领先价格变动，可作交易信号 | W2 |
| **Bank, Larch & Peter (2011), "Google Search Volume and Its Influence on Liquidity and Returns"** | 搜索量主要预测**波动率与成交量**，对收益方向预测弱 | W7 |
| **Drake, Roulstone & Thornock (2012), "Investor Information Demand", J. Accounting Research** | 财报前后投资者信息需求（搜索/浏览）激增，信息需求宽度与后续定价效率相关 | W5, W10 |
| **Lou (2014), "Attitudes to Advertising: Do Investors Buy What They Know?", RFS** | 广告支出增长 → 吸引散户注意力 → 短期流入推高股价、长期反转 | W8, W11 |
| **Barber & Odean (2008), "All That Glitters", RFS** | 注意力驱动的买入是散户主导现象，个人投资者只买吸引注意力的股票 | W1, W9 |
| **Vlastakis & Markellos (2012), "Information demand and stock market volatility", J. Banking & Finance** | 信息需求（搜索）与波动率正相关 | W7 |
| **Takeda & Wakao (2014), "Google search intensity and its relationship to the returns and liquidity of Japanese startup stocks"** | 搜索强度的动量/反转随市值而变 | W6 |
| **论坛帖 `44089095804439`（6 赞）** | GBR 基本面 Δ 因子族骨架 `rank(ts_quantile(ts_av_diff(divide(F,D),168),56,driver=gaussian))`；84/28→2.07、168/56→2.71、252/84→2.43；**但安慰剂 Δ(1/市值) S 1.89，说明该骨架高 Sharpe 有大量价格成分** | W8 |
| **论坛帖 `33120494662423`（28 赞）** | `trade_when(x, y, z)` 三参数语义：触发条件 / alpha 表达式 / 退出条件；`-1` 表示不退出 | W10 |
| **论坛帖 `35090833341207`（101 赞 / 20 评论）** | Other 类字段的关系分类法：行为对称型（buy vs sell）、行为推导型（净买入 = 买−卖）、实体层级型；**净额有量纲、比值无量纲** ⇒ 优先做比值 | W4, W12 |

## 3. 十个结构互异模板

缩写：`T = vec_sum(oth47_organic_traffic)`（visits）、`K = vec_sum(oth47_organic_keywords)`（count）、
`R = vec_avg(oth47_rank)`、`B = vec_sum(paid_search_budget_estimate)`（USD）、
`V = vec_sum(paid_search_visitors)`（visits）、`OC = vec_sum(oth47_organic_cost)`（USD）

| # | 名称 | 来源 | 几何结构 | 表达式 | 窗口理由 |
|---|---|---|---|---|---|
| **W1** | ASVI 异常搜索量（水平） | paper: Da et al. 2011 | 季度 zscore → 行业横截面 rank | `group_rank(ts_zscore(vec_sum(oth47_organic_traffic), 66), sector)` | 66=季度。Da 原文用 4 周 ASVI，D1 日频下 4 周残差噪声过大，取季度捕捉注意力衰减周期；白名单值 |
| **W2** | 关注度变化率 | paper: Preis et al. 2013 | 月度一阶差分 → 子行业 rank | `group_rank(ts_av_diff(vec_sum(oth47_organic_traffic), 22), subindustry)` | 22=月度，对应 SEMrush 月频刷新节奏；白名单值 |
| **W3** | 可见度排名反转 | 自建 | 排名均值反向 → 行业 rank | `reverse(group_rank(ts_mean(vec_avg(oth47_rank), 22), sector))` | 22=月度平滑掉单月排名抖动；SEMrush rank 越低越可见，故 reverse |
| **W4** | 流量-关键词效率 | 自建（forum 35090833341207 比值原则） | 同数据集内比值 → zscore | `group_rank(ts_zscore(divide(vec_sum(oth47_organic_traffic), vec_sum(oth47_organic_keywords)), 66), sector)` | 每关键词带来的访问量＝关注"深度"；66=季度基线 |
| **W5** | 信息需求宽度水平 | paper: Drake et al. 2012 | 年度 zscore | `group_rank(ts_zscore(vec_sum(oth47_organic_keywords), 252), sector)` | 252=年度基线，关键词数变化慢，短窗全是噪声 |
| **W6** | 关注度稳定性 IR | 自建 | mean/std 252 | `group_rank(ts_ir(vec_sum(oth47_organic_traffic), 252), industry)` | 252=年度，IR 需要足够样本估波动；对应 Takeda-Wakao 的"持续关注" |
| **W7** | 关注度二阶矩（反向） | paper: Bank-Larch-Peter 2011 + Vlastakis-Markellos 2012 | std_dev → reverse | `reverse(group_rank(ts_std_dev(vec_sum(oth47_organic_traffic), 66), sector))` | 66=季度波动窗口；文献说搜索量预测波动率，故把"高关注波动"当作风险规避 |
| **W8** | 广告预算位移 + 分位 | forum 44089095804439 + paper: Lou 2014 | av_diff 66 → ts_quantile 252 gaussian | `rank(ts_quantile(ts_av_diff(vec_sum(paid_search_budget_estimate), 66), 252, driver=gaussian))` | 66/252 落在论坛实测最优点（168/56→2.71）附近且在白名单内；分位化去掉量纲 |
| **W9** | 按可见度分桶后的异常关注度 | 自建（`bucket` 作 group 轴） | bucket(rank(R)) 当分组 → zscore | `group_rank(ts_zscore(vec_sum(oth47_organic_traffic), 66), bucket(rank(vec_avg(oth47_rank)), range="0,1,0.1"))` | 先在"网站可见度"10 桶内比较，剥离"大公司网站流量天然大"的规模效应；**分组轴来自同一数据集，不跨塔、不占配额** |
| **W10** | 高信息需求门控 | forum 33120494662423 + paper: Drake et al. 2012 | `trade_when` 门控 | `trade_when(greater(rank(vec_sum(oth47_organic_keywords)), 0.7), group_rank(ts_zscore(vec_sum(oth47_organic_traffic), 66), sector), -1)` | 只在信息需求前 30% 的标的上表达注意力信号；`rank` 输出无量纲，可与常数 0.7 比较（避开 `cap` 那类单位陷阱） |

### 备用（前 10 个出结果后按需启用）

| # | 名称 | 来源 | 表达式 |
|---|---|---|---|
| **W11** | 注意力"价格"反向 | paper: Lou 2014 | `reverse(group_rank(ts_zscore(vec_sum(oth47_organic_cost), 252), sector))` |
| **W12** | 自然 vs 付费关注结构 | 自建 | `rank(subtract(rank(vec_sum(oth47_organic_traffic)), rank(vec_sum(paid_search_visitors))))` |

## 4. 回测设置（本轮实证档）

```
region=GBR  universe=TOP700  delay=1
neutralization=STATISTICAL   decay=4   truncation=0.08
nanHandling=ON   maxTrade=ON   pasteurization=ON   unitHandling=VERIFY
```

依据：
- `STATISTICAL` — `GBR-NEUTRALIZATION-AXIS-EXHAUSTED` 判死条目实测「4 条最强表达式全面最优」，且本轮 prod 能过的族全部用 STATISTICAL。
- `decay 4` — SEMrush 数据本身**月频刷新**，换手天然低，不需要高 decay；`GBR-DECAY-LEVER-NEGATIVE-TURNOVER-FLOOR` 记录该区 8 条 ΔF 全负。
- `nanHandling ON` — coverage 0.6068，缺 39% 不能直接丢弃。

## 5. 风险与预警（派发前已知）

1. **coverage 0.6068 = 子宇宙风险**。`sentiment7`（cov 0.58）与 `earnings6` 都是死在
   `LOW_SUB_UNIVERSE_SHARPE`（limit = 0.4743 × sharpe），不是死在骨架。**这是本数据集最大的单一风险**，
   首批 4 条回测拿到 results 后**第一件事查 `sub_universe_sharpe`，不是查 sharpe**。
2. **注意力因子 = 价格动量代理的风险**。`dl_riskfree` 本轮就是被判"实为动量代理"（2022 −1.63 / 2023 0.07）。
   验收时必须做逐年 `get_alpha_yearly_stats`，看近三年是否出现符号翻转。
3. **W8 的骨架带价格成分**。论坛原文自己给了安慰剂：`Δ(1/市值)` 单独 S 1.89。W8 用的是广告预算（非价格），
   理论上干净，但若 W8 显著强于其他 9 个模板，要优先怀疑是骨架在偷价格信息而不是字段有信号。
4. **prod 未知**。`other47` 在 GBR 单塔零历史，没有可参考的 prod 先验；同族 `other455` 已判
   `GBR-PROD-SATURATED`。**任何一条过闸后必须先测 prod 再谈提交。**

## 6. 派发记录

| 批次 | multisim id | 模板 | 状态 |
|---|---|---|---|
| A | `3XGIid7OF4lab1NRoieJrSG` | W1, W7 | 已派发（2026-10-30） |
| B | `W06hjd4V4nX9CYEdBpazRh` | W4, W8 | 已派发（2026-10-30） |
| C（待定） | — | W3, W6 | 视 A/B 结果 |
| D（待定） | — | W5, W2 | 视 A/B 结果 |
| E（待定） | — | W9, W10 | 视 A/B 结果 |
