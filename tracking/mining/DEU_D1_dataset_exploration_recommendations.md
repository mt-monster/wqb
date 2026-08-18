# DEU D1 TOP500 数据探索报告 — PPA 因子挖掘候选推荐
# 生成时间: 2026-08-10
# 工具: brain-dataset-exploration-general + brain-datafield-exploration-general 工作流
# 数据源: get_datasets 全类别枚举 + get_datafields 字段级验证 + get_pyramid_multipliers

## 0. 区域背景（决定挖掘策略）

| 维度 | 现状 |
|------|------|
| 金字塔状态 | **DEU D1 全域 16 个类别全部为 0 alpha（全空白）** |
| 倍率 | 全域统一 1.9×（institutions/insiders/model/news/other/analyst/pv/fundamental/sentiment/option/macro 均 1.9×；仅 shortinterest 1.7×） |
| 竞争度 | 平台上几乎无人点亮 DEU D1 任何金字塔 → PPA 点塔无竞争 |
| 已知瓶颈 | ⚠ sub_universe 结构性墙：limit ≈ 0.47×sharpe（DEU 需要 0.8，此前实测仅 0.30）— 已在 model264/model238/model53/pattern_scores/news104/analyst_earnings_ibes/institutions6/sentiment27 上验证 |

## 1. 全量数据集盘点（~130 数据集，16 类别）

### 通过 PPA 硬门槛（cov ≥ 0.85）的完整名单

| 数据集 | 类别 | Cov | Fields | AlphaCnt | Users | ValueScore | 状态 |
|--------|------|-----|--------|----------|-------|-----------|------|
| **fund_holdings_panel** | institutions | 0.90 | 18 | **0** | **0** | 8.0 | 🆕 未测试 |
| **institutions6** | institutions | 1.00 | 11 | 5 | 5 | 6.0 | 已测（墙） |
| **other455** | other | 0.95 | 1500 | 4 | 4 | 7.0 | 部分测试 |
| **model53** | model | 0.91 | 22 | 1 | 1 | 7.0 | 已测（墙） |
| **pv29** | pv | 1.00 | 50 | 1 | 1 | 6.0 | 未测试（行业分类，非信号） |
| **news104** | news | 0.96 | 11 | 2 | 2 | 5.0 | 已测（墙） |
| pattern_scores | pv | 0.99 | 504 | 7 | 5 | 6.0 | 部分测试 |
| model238 | model | 0.86 | 22 | 11 | 5 | 6.0 | 已测（墙，max 0.88） |
| sentiment27 | sentiment | 0.90 | 18 | 7 | 5 | 6.0 | 已测（墙） |
| analyst_earnings_ibes | model | 1.00 | 42 | 20 | 12 | 6.0 | 已测（墙） |
| model264 | model | 1.00 | 380 | 17 | 10 | 6.0 | 已测（墙） |

### 字段级验证发现的新白空间（本次探索核心产出）

以下数据集的**字段级** userCount/alphaCount 均为 0（数据集级可能因其他区域或历史使用≠0，DEU 上无人在用）：

| 数据集 | 字段数 | 字段级覆盖 | 字段类型 | 信号语义 | 推荐度 |
|--------|--------|-----------|---------|---------|--------|
| **fund_holdings_panel** | 18 | 0.876–0.928 | VECTOR | 基金边界交易（新建仓/清仓）、HHI 集中度、>50bps 大额交易、21d 稳定边界交易（持久信号）、重仓股 conviction 交易、账户数 | ⭐⭐⭐⭐⭐ |
| **insider_agg_matrix** | 34 | **directional_indicator cov=1.00**，其余 0.53 | MATRIX | 内部人净方向指标（100%覆盖+0 alpha!）、买卖股数、显著交易 top4 值 | ⭐⭐⭐⭐⭐ |
| **analyst93** | 100 | 0.63–0.65 | VECTOR | 欧洲分析师历史盈利性（跟单收益 profitability1/2 × 20/60/120d）、准确度、一致性、修订正确率、同行相对排名 | ⭐⭐⭐⭐ |
| **analyst44** | 72 | 0.32–0.69 | VECTOR | 事件式经纪商估计修订（EPS/Sales/NetProfit/ROE/DPS/EBITDA 的 prevalue→value 修订对） | ⭐⭐⭐⭐ |
| **model262** | 159 | 0.25–0.46 | MATRIX | 市场隐含财务预测（DNN 反推 Compustat 项）+ MAD/MAE 预测不确定性诊断 | ⭐⭐⭐ |
| **other47** | 18 | 0.50–0.65 | VECTOR | SEMrush 搜索流量/关键词数/广告预算/网站排名（网页智能） | ⭐⭐⭐ |

## 2. 推荐挖掘选项（按优先级）

### 🥇 A 档：零竞争 + 高覆盖 + 信号族独特（最推荐）

**A1. fund_holdings_panel（institutions 类别，×1.9）**
- 为什么：DEU 字段级 0 用户 0 alpha；cov 0.93；institutions 是 DEU D1 未点亮金字塔
- 候选字段：
  - `vec_sum(boundary_transaction_usd_value)` — 基金新建仓/清仓总金额（机构行为动量）
  - `vec_sum(stable_boundary_trade_count_21d)` — 21 天无前序交易的"持久性"边界交易（最强信号，剔除了倒仓噪声）
  - `vec_sum(top_weighted_transaction_number)` — 重仓股（conviction）交易计数
  - `herfindahl_index_transactions` — 交易集中度（分散→集中 的变化）
- 建议构造：`ts_delta(vec_sum(stable_boundary_trade_count_21d), 22)` 类事件驱动 + 持久性过滤
- 风险：VECTOR 字段需先 `vec_sum/vec_mean` 归约，算子预算友好

**A2. insider_agg_matrix / insider_matrix / insider_trx_matrix（insiders + other 类别，×1.9）**
- 为什么：`directional_indicator` **字段级 cov=1.00 且 alphaCount=0**（同族 `directional_indicator_2` 也是 1.00/0）— 全 DEU 最干净的点塔素材
- 候选字段：
  - `directional_indicator` / `directional_indicator_2` — 内部人净方向（±1 或连续分）
  - `total_buy_shares - total_sell_shares` 或 `total_top_buy_shares - total_top_sell_shares` — 高管买卖净额
  - `top_directional_significant_value_1` — 最大显著方向交易
- 建议构造：`ts_sum(directional_indicator, 63)` 事件累积 + `rank` 截面化
- 注意：DEU 内部人披露节奏稀疏 → 需 ts_rank/ts_sum 平滑，关注 turnover

### 🥈 B 档：未测试 + 中等覆盖（第二梯队）

**B1. analyst93（Europe Analyst Estimate，analyst 类别，×1.9）**
- 为什么：欧洲专属分析师绩效数据；`*_profitability1/2_120d` 是"过去 120 天跟单该分析师的平均日收益"——**信息量最直接的因子**（历史准确的分析师 → 未来预测可靠）
- 候选：`anl93_profitabilityprev_estimator_profitability1_120d`、`anl93_analyst_accuracy1`、`anl93_estimator_correct_revision_ratio`
- 建议：按分析师盈利性加权修订信号（类似于 SmartEstimate 思想但用真实历史收益）

**B2. analyst44（Integrated Broker Estimates，analyst 类别，×1.9）**
- 为什么：72 字段全空白；事件式结构 `*_prevalue` vs `*_value` 天然是修订幅度信号；coverage 0.69 中等
- 候选：`anl44_2_eps_value - anl44_2_eps_prevalue`（需 vec 归约后处理）、sales/netprofit 修订
- 风险：事件型字段稀疏，跨截面信号弱，适合事件窗口聚合

### 🥉 C 档：已有数据集深挖（低增量价值但零成本）

**C1. other455（1500 字段）** — 只测过一小部分；AI/ML 关系增强信号，alphaCount 仅 4
**C2. pattern_scores（504 字段）** — 已测部分撞墙，但剩余 ~400 字段未覆盖
**C3. model36（SmartRatios，cov 0.849 边缘）** — alphaCount=1，接近门槛

## 3. 明确不推荐（已穷尽/结构问题）

| 数据集 | 原因 |
|--------|------|
| model264 / model238 / model53 / news104 / institutions6 / sentiment27 / analyst_earnings_ibes | 已充分测试，全部撞 sub_universe 墙（max|S| 0.30 vs 需 0.8） |
| analyst7 / analyst_factor_signals / model25 / model38 / pv1 / techindi_model | alphaCount ≥ 50 拥挤或 DEU cov=0 |
| ml_factor_proj / news_sentiment_nlp / stock_cluster_dl | DEU 无覆盖（cov=0），EUR 可用但非本区域 |

## 4. 行动建议

1. **首轮 8 模拟验证**（NONE/decay0 快速筛）：fund_holdings_panel 4 字段 × (boundary/stability/concentration) + insider_agg_matrix 2 字段
2. **命中后**套用已验证的 × vol 范式 + INDUSTRY 中性化提升 Sharpe（DEU 已验证 0.81→1.79 的路径）
3. **硬门槛复核**：即便 Sharpe 达标，仍需验证 sub_universe 是否突破 0.8 —— A 档两个数据集属于「行为/资金流」信号族，与之前「预测模型」信号族不同源，值得一次性验证边际
4. 若 A 档仍撞墙 → DEU D1 结论维持"结构性不可达"，转向 GBR D0（全域 2.0× 同样全空白）
