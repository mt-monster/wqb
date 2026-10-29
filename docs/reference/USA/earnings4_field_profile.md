# USA · `earnings4` 字段画像

> 由 `tools/fields/profile_dataset_fields.py` 生成，输入为 `get_datafields` 原始返回。零平台配额。

## 1 规模与完整性

| 项 | 值 |
|---|---|
| 本次返回字段数 | 375 |
| 平台声明数 `platform_count` | 375 |
| 返回 `count` | 375 |
| 是否完整 `complete` | True |
| 类型分布 | {'MATRIX': 250, 'VECTOR': 125} |
| 平均 coverage | 0.9692 |
| 判定 | ✅ 完整 |

## 2 可用性分档

### 2.1 coverage

| 档 | 字段数 |
|---|---|
| ≥0.90（可直接做尽） | 375 |

### 2.2 拥挤度（决定 prod 相关性风险）

| 档 | 字段数 |
|---|---|
| 低拥挤（≤50 alpha） | 275 |
| 中拥挤（51–500） | 95 |
| 高拥挤（501–5000） | 4 |
| 零竞争 | 1 |

零竞争字段（`userCount==0`）：**1** / 375；描述带单位标注：0

## 3 语义结构

| 语义族 | 字段数 | 示例字段 |
|---|---|---|
| 未归类 | 187 | `abs_avg_pct_move_announcements_12`, `absolute_average_announcement_percent_move`, `aggregate_option_open_interest`, `aggregate_option_open_interest_2` |
| 流动性/风险 | 179 | `atm_volatility_month1`, `atm_volatility_month2`, `atm_volatility_month3`, `best_fit_implied_announcement_effect` |
| 盈利能力 | 9 | `ern4_fairmth2xieevol90d`, `ern4_fairvol90d`, `ern4_fairxieevol90d`, `fair_vol_month2_xiee_90d` |

**时间朝向**（`forecast`=前瞻/预测，`realized`=已实现/事后，`mixed`=差值构造）：

| 朝向 | 字段数 |
|---|---|
| unknown | 375 |

## 4 名字前缀聚类（前 15）

| 前缀 | 字段数 |
|---|---|
| `ninety_day` | 18 |
| `twenty_day` | 13 |
| `sixty_day` | 12 |
| `ten_day` | 12 |
| `five_day` | 8 |
| `month_one` | 7 |
| `pct_move` | 7 |
| `second_month` | 7 |
| `straddle_price` | 7 |
| `announcement_effect` | 6 |
| `one_year` | 6 |
| `five_hundred` | 5 |
| `one_thousand` | 5 |
| `first_event` | 4 |
| `ninth_historical` | 4 |

## 5 候选短名单（Top 25，按打分排序）

打分 = 覆盖 40 + 低拥挤 25 + 语义可解释 20 + 前瞻 5（非信号 −30）。**只做排序参考**，仍须过单位闸与机制假设。

| # | 字段 | 类型 | cov | user | alpha | 语义族 | 朝向 | 分 | 描述（截断） |
|---|---|---|---|---|---|---|---|---|---|
| 1 | `sixty_day_ex_announcement_close_volatility` | MATRIX | 0.969 | 0 | 0 | 流动性/风险 | - | 85.0 | 60-day close-to-close historical volatility excluding earnings announcement days. |
| 2 | `atm_volatility_month3` | MATRIX | 0.969 | 25 | 31 | 流动性/风险 | - | 80.0 | At-the-money implied volatility for month 3 |
| 3 | `ern4_10dclshvxern` | VECTOR | 0.969 | 24 | 40 | 流动性/风险 | - | 80.0 | 10-day close-to-close historical volatility excluding earnings-day effects, annualized pe… |
| 4 | `ern4_10dexerniv` | VECTOR | 0.969 | 30 | 46 | 流动性/风险 | - | 80.0 | 10-day constant-maturity implied volatility with earnings effect removed |
| 5 | `ern4_10dorhv` | VECTOR | 0.969 | 33 | 50 | 流动性/风险 | - | 80.0 | 10-day ORATS open-range historical tick volatility (annualized), including earnings days |
| 6 | `ern4_10dorhvxern` | VECTOR | 0.969 | 24 | 49 | 流动性/风险 | - | 80.0 | 10-day ORATS open-range historical tick volatility (annualized), excluding the earnings d… |
| 7 | `ern4_20dclshvxern` | VECTOR | 0.969 | 24 | 44 | 流动性/风险 | - | 80.0 | 20-day close-to-close historical volatility excluding earnings-day effects, annualized pe… |
| 8 | `ern4_20dexerniv` | VECTOR | 0.969 | 22 | 34 | 流动性/风险 | - | 80.0 | 20-day constant-maturity implied volatility with earnings effect removed |
| 9 | `ern4_20dorhvxern` | VECTOR | 0.969 | 34 | 50 | 流动性/风险 | - | 80.0 | 20-day ORATS open-range historical tick volatility (annualized), excluding the earnings d… |
| 10 | `ern4_500dorhvxern` | VECTOR | 0.969 | 35 | 46 | 流动性/风险 | - | 80.0 | 500-day open-range (intraday) historical volatility with earnings days excluded, annualiz… |
| 11 | `ern4_5dclshv` | VECTOR | 0.969 | 14 | 20 | 流动性/风险 | - | 80.0 | 5-day close-to-close historical volatility, annualized percent |
| 12 | `ern4_5dclshvxern` | VECTOR | 0.969 | 16 | 25 | 流动性/风险 | - | 80.0 | 5-day close-to-close historical volatility excluding earnings-day effects, annualized per… |
| 13 | `ern4_5dorhv` | VECTOR | 0.969 | 23 | 37 | 流动性/风险 | - | 80.0 | 5-day ORATS open-range historical tick volatility (annualized), including earnings days |
| 14 | `ern4_5dorhvxern` | VECTOR | 0.969 | 23 | 46 | 流动性/风险 | - | 80.0 | 5-day ORATS open-range historical tick volatility (annualized), excluding the earnings day |
| 15 | `ern4_60dclshv` | VECTOR | 0.969 | 29 | 45 | 流动性/风险 | - | 80.0 | 60-day close-to-close historical volatility, annualized percent |
| 16 | `ern4_60dclshvxern` | VECTOR | 0.969 | 20 | 39 | 流动性/风险 | - | 80.0 | 60-day close-to-close historical volatility excluding earnings-day effects, annualized pe… |
| 17 | `ern4_60dexerniv` | VECTOR | 0.969 | 16 | 26 | 流动性/风险 | - | 80.0 | 60-day constant-maturity implied volatility with earnings effect removed |
| 18 | `ern4_60dorhvxern` | VECTOR | 0.969 | 24 | 41 | 流动性/风险 | - | 80.0 | 60-day ORATS open-range historical tick volatility (annualized), excluding the earnings d… |
| 19 | `ern4_6mexerniv` | VECTOR | 0.969 | 8 | 14 | 流动性/风险 | - | 80.0 | 6-month constant-maturity implied volatility with earnings effect removed |
| 20 | `ern4_90dclshvxern` | VECTOR | 0.969 | 30 | 45 | 流动性/风险 | - | 80.0 | 90-day close-to-close historical volatility excluding earnings-day effects, annualized pe… |
| 21 | `ern4_90dexerniv` | VECTOR | 0.969 | 31 | 42 | 流动性/风险 | - | 80.0 | 90-day constant-maturity implied volatility with earnings effect removed |
| 22 | `ern4_impernmv` | VECTOR | 0.969 | 19 | 23 | 流动性/风险 | - | 80.0 | Implied Earnings Move in the market over the fitXearnings implied volatility for the firs… |
| 23 | `ern4_impmth2ernmv` | VECTOR | 0.969 | 15 | 30 | 流动性/风险 | - | 80.0 | Implied Earnings Move in the market over the fit implied volatility for the second earnin… |
| 24 | `ern4_m1atmiv` | VECTOR | 0.969 | 20 | 27 | 流动性/风险 | - | 80.0 | At-the-money implied volatility for month 1 (front-month) options, annualized (decimal) |
| 25 | `fair_vol_month2_xiee_90d` | MATRIX | 0.969 | 8 | 13 | 盈利能力 | - | 80.0 | Adjusted 90-day implied volatility for the second earnings month: 90d IV minus the implie… |
