# S0 · KOR Institutions 全数据集扫描（2026-11-07）

> 来源：MCP `get_datasets(region=KOR, delay=1, universe=TOP600, category=institutions)` → **count=2**（平台全量，无遗漏）
> 对照：`category=institution`（单数）→ **count=0**；`category=institutional` → **count=0**。
> ⇒ 平台真实类别名是复数 `institutions`。2026-11-06 上一轮因传单数判「无此类别」，属口径错误，本轮已纠正。
> 字段：MCP `get_datafields(..., filter_sharpe=false)`，两个数据集均返回 `complete=true / platform_count` 全覆盖。
> 设置基准（KOR 唯一合法档，`get_platform_setting_options` + 存量全绿件 `LLZ6wZO2` 双重确认）：
> KOR / TOP600 / Delay=1 / EQUITY · decay 4 · truncation 0.08 · STATISTICAL · unitHandling VERIFY ·
> nanHandling OFF · pasteurization ON · maxTrade OFF · 2014-01-01 ~ 2023-12-31（**10 个完整年**）· FASTEXPR

## 1. 类别内全量数据集（2 个）

| # | dataset | 名称 | 字段 | 类型 | cov | aC | user | valueScore | 本轮裁定 |
|---|---|---|---:|---|---:|---:|---:|---:|---|
| 1 | **institutions6** | Institutions and Beneficial Stake Ownership | **11** | 全 MATRIX | **.9996** | **1013** | 317 | 2.0 | ⭐ **主攻**（覆盖率满、字段全为成对流量，可构净额/价差/广度） |
| 2 | fund_holdings_panel | Global Institutional Fund Holdings | **30** | MATRIX 12 / VECTOR 18 | .8093 | 228 | 117 | 4.0 | ⚠ **次攻**（仅取未被判死的「存量/持久变动」子轴，见 §3） |

## 2. institutions6 字段清单（11/11，`filter_sharpe=false`）

| # | 字段 | 类型 | cov | aC | user | 经济含义（description 原文意译） |
|---|---|---|---:|---:|---:|---|
| 1 | `aggregate_equity_value_all_owners` | MATRIX | 1.0 | 91 | 64 | 全体股东（去母子重复）持有市值 |
| 2 | `aggregate_equity_value_institutions` | MATRIX | .9976 | 119 | 85 | 机构持有市值 |
| 3 | `aggregate_share_count_all_owners` | MATRIX | 1.0 | 212 | 124 | 全体股东持股数 |
| 4 | `aggregate_share_count_institutions` | MATRIX | .9976 | **257** | **147** | 机构持股数（**本集 aC 头部 = 机构持股规模轴**） |
| 5 | `count_institutional_buyers_security` | MATRIX | 1.0 | 88 | 64 | 报告期内**买入**的机构家数 |
| 6 | `count_institutional_holders_security` | MATRIX | 1.0 | 63 | 41 | 报告期末**持有**（>0）的机构家数 |
| 7 | `count_institutional_sellers_security` | MATRIX | 1.0 | 101 | 71 | 报告期内**卖出**的机构家数 |
| 8 | `market_value_institutional_shares_acquired` | MATRIX | 1.0 | 112 | 61 | 报告期内机构**买入**金额 |
| 9 | `market_value_institutional_shares_disposed` | MATRIX | 1.0 | 62 | 46 | 报告期内机构**卖出**金额 |
| 10 | `quantity_institutional_shares_acquired` | MATRIX | 1.0 | 119 | 72 | 报告期内机构**买入**股数 |
| 11 | `quantity_institutional_shares_disposed` | MATRIX | 1.0 | 107 | 57 | 报告期内机构**卖出**股数 |

### 2.1 名 vs description 差异表（0.2 强制项）

| 字段名暗示 | description 实际 | 差异后果 |
|---|---|---|
| `aggregate_*` 易被当作「全市场汇总」 | 实际是**逐证券横截面**（每只股票一行），`all_owners` 与 `institutions` 是同一标的的两口径 | 可安全做 `institutions / all_owners` 占比，**不是**常数序列 |
| `count_*_buyers` 易被当作「买入股数」 | 实际是**家数**（number of investors） | 与 `quantity_*_acquired`（股数）是**两个量纲**，可构「广度 vs 强度」分离 |
| `quantity_*` 与 `market_value_*` 易被当作同义 | 前者股数、后者美元金额 ⇒ 相除 = **机构成交均价** | 提供「买卖均价价差」这一独立轴（W1-07） |
| `_acquired` / `_disposed` 看似孪生 | 是**报告期内流量**，不是期末存量 | 必须用流量/存量比率或净额/总额比率去量纲，**禁裸水平**（铁律 A 的变形） |

### 2.2 成对结构（这是本集唯一可构「净额」的资产）

| 对 | 腿 A | 腿 B | 净额构造 | 价差构造 |
|---|---|---|---|---|
| 市值流量 | `market_value_institutional_shares_acquired` | `market_value_institutional_shares_disposed` | (A−B)/(A+B) | — |
| 股数流量 | `quantity_institutional_shares_acquired` | `quantity_institutional_shares_disposed` | (A−B)/(A+B) | — |
| 家数 | `count_institutional_buyers_security` | `count_institutional_sellers_security` | (A−B)/holders | — |
| 存量占比 | `aggregate_share_count_institutions` | `aggregate_share_count_all_owners` | 比值一阶差分 | — |
| 均价 | mv/qty（买） | mv/qty（卖） | — | log(买均价/卖均价) |

⚠ 这四对腿**必须靠 `filter_sharpe=false` 才能拉全**：默认 `filter_sharpe=true` 只返回 4/11，缺的正是
`quantity_*_disposed` / `market_value_*_acquired` / `count_*_buyers` 等对侧腿，缺腿 = 缺机制。

## 3. fund_holdings_panel 字段清单（30/30）与逐字段裁定

### 3.1 MATRIX（12）—— 存量与集中度

| 字段 | cov | aC | 裁定 |
|---|---:|---:|---|
| `holder_account_total` | .9553 | 30 | ✅ 持有人**广度**（Chen-Hong-Stein 2002 广度轴） |
| `top_weighted_account_number` | .9553 | 15 | ✅ **信念持仓**机构家数（top30% 权重） |
| `mean_security_weight` | .9553 | 12 | ✅ 户均权重 = 信念强度 |
| `security_holding_usd_value` | .9553 | 7 | ✅ 持仓总额（规模轴，需去量纲） |
| `herfindahl_index_holdings` | .9553 | 31 | ✅ 持仓集中度 HHI（拥挤度轴） |
| `holding_value_distribution_score` | .9553 | 19 | ✅ 拥挤度自定义指标（与 HHI 共线） |
| `holder_account_total_active` | .7666 | 6 | ⚠ 覆盖率 76.7%，仅作备选 |
| `top_weighted_account_number_active` | .7666 | 11 | ⚠ 同上 |
| `mean_security_weight_active` | .7666 | 10 | ⚠ 同上 |
| `security_holding_usd_value_active` | .7666 | 6 | ⚠ 同上 |
| `herfindahl_index_holdings_active` | .7666 | 11 | ⚠ 同上 |
| `holding_value_distribution_score_active` | .7666 | 7 | ⚠ 同上 |

### 3.2 VECTOR（18）—— 流量与交易事件（★ 大部分落在历史判死族）

| 字段 | cov | aC | 裁定 |
|---|---:|---:|---|
| `stable_boundary_trade_count_21d` | .887 | 13 | ⭐ **唯一未判死流轴**：剔除 21 日内反复进出的「持久建仓/清仓」计数 |
| `stable_boundary_trade_count_21d_active` | .6626 | 1 | ⚠ 覆盖不足 |
| `boundary_transaction_total` / `_usd_value` | .887 | 35 / 6 | ⛔ 判死族（事件聚合流量=噪声） |
| `boundary_transaction_total_active` / `_usd_value_active` | .6626 | 4 / 2 | ⛔ 判死族 + 覆盖不足 |
| `transaction_account_total` / `_active` | .887 / .6626 | 6 / **0** | ⛔ `_active` 平台 **0 用户 0 alpha**，疑似空字段 |
| `herfindahl_index_transactions` / `_active` | .887 / .6626 | 2 / 5 | ⛔ 判死族 |
| `large_trade_count_50bps` / `_active` | .887 / .6626 | 3 / 1 | ⛔ 判死族 |
| `security_transaction_usd_value` / `_active` | .887 / .6626 | 3 / 1 | ⛔ 判死族 |
| `top_weighted_transaction_number` / `_active` | .887 / .6626 | 8 / 1 | ⛔ 判死族 |
| `transaction_value_distribution_score` / `_active` | .887 / .6626 | 4 / 3 | ⛔ 判死族 |

### 3.3 历史判死记录与本次重新开案的边界（必须写清）

| 条目 | 来源 | 原文 | 本轮如何遵守 / 为何仍开案 |
|---|---|---|---|
| `KOR-FUND-HOLDINGS-PANEL-DEAD` | [institutions.md](../../../../C:/Users/MENGTAO/.agents/skills/wq-brain-ra-kor/references/institutions.md) | 「do not probe fund_holdings_panel again; **event-aggregate flow fields** here are noise」 | **逐字遵守**：3.2 表中所有 `boundary_transaction_*` / `transaction_*` / `large_trade_*` / `*_distribution_score` **全部不投**。仅开 3.1 MATRIX 存量轴 + `stable_boundary_trade_count_21d` 一条（带 21 日持久性过滤，**不属于** event-aggregate flow） |
| 跨区 negative | 同上 | 「institutions6 作主信号判死；作慢门控腿可用」 | ⚠ **已被 2026-11-06 新证据部分推翻**：[s1_institutions6_wave1_template_pool.md](../s1_institutions6_wave1_template_pool.md) 记录 IND 由该集派生 14 颗全绿（S 1.64–3.20）；KOR 侧同集字段名逐字一致、cov 1.0 ⇒ 该条判死是「裸水平直用」层面的，**不覆盖净额/占比/广度结构**。本轮以实测为准 |

## 4. 覆盖率与「近十年都要有数据」（约束 6）

| 数据集 | 平台 cov | 判读 | 本轮动作 |
|---|---:|---|---|
| institutions6 | **.9996** | 全 TOP600 几乎满覆盖 | ✅ 直接可用，无需动态放宽 |
| fund_holdings_panel | .8093 | 约 8 成标的 | ✅ 仍在「动态可调」范围；但入池候选**必须**过 `get_alpha_yearly_stats` 十年逐年 `longCount>0` |

> 覆盖率按字段再分层（见 §3）：panel 的 `.9553` 族可作主信号，`.7666` 族只作备选，`.6626` VECTOR 族不投。

## 5. 数据集潜力评分与排序（S0 决策）

| 排名 | 数据集 | 广度（字段数×覆盖） | 结构多样性 | 拥挤度（aC） | 历史包袱 | **综合** |
|---|---|---:|---|---|---|---|
| 1 | **institutions6** | 11 × 1.0 | 5 类成对结构（净额/价差/广度/占比/户数） | 高（1013） | 裸水平已判死 | ⭐ **主攻，先打 10 条结构** |
| 2 | fund_holdings_panel | 30 × .81 | 存量/集中度/信念/持久流量 | 低（228） | 流量族判死 | ⚠ **备选，只打 5 条存量轴** |

**结论**：本类别只有 2 个数据集，且 `institutions6` 在覆盖与结构上全面占优 ⇒ **不换数据集**，
按用户约束「不频繁切换数据集」，前 2 波全部在 `institutions6` 上做纵深；
只有当 `institutions6` 的 5 类结构全部实测确认为弱（S 全 < 0.5）时，才切 `fund_holdings_panel` 并存案说明原因。
