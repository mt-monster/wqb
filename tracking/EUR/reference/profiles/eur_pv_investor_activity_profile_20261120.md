# EUR / investor_activity 全字段画像（2026-11-20）

> 平台实查 `get_datafields(dataset_id=investor_activity, region=EUR, universe=TOP2500, delay=1)`：**47/47 字段，complete=True**（全部 VECTOR）。
> category=pv ⇒ 落 EUR/D1/**PV 塔（2/3，差 1 席）**；mult 1.1；**cov 0.1644**（稀疏）；2026-03-01 新 onboard；**绝大多数字段 aC ≤ 5（极冷门，prod 友好）**。
> 命名规则 `eur_<category>_<dataset>_profile_<YYYYMMDD>.md`。**注意：PV 类数据按用户红线不得两两组腿 ⇒ 本集只能单集 ATOM 使用。**

## 1. 字段结构总览（6 语义族）

| 语义族 | 字段数 | 说明 |
|---|---:|---|
| 散户净流量 | 4 | `net_retail_buying_selling_value{,_eur}` + 散户买入/卖出股数 |
| 专业净流量 | 4 | `net_professional_buying_selling_value{,_eur}` + 专业买入/卖出股数 |
| 成交额/量 | 6 | 散户/专业/全市场 turnover 与成交股数 |
| 成交价格 | 12 | 均价（散户/专业/全市场 × 本币/EUR）+ 开高低收 + 最高最低 |
| 订单数 | 3 | `total_orders_placed_daily` + 散户/专业订单数 |
| 规模 | 4 | 市值 / 股权估值 / 总股本 |

## 字段全表（47 字段逐字段平台读数，cov 均 0.1644）

| 字段 | 类型 | cov | aC | 语义 |
|---|---|---:|---:|---|
| `net_retail_buying_selling_value_eur` | VECTOR | 0.1644 | 120 | 散户净买入额(EUR) |
| `shares_purchased_retail_investors_daily` | VECTOR | 0.1644 | 44 | 散户当日买入股数 |
| `net_professional_buying_selling_value_eur` | VECTOR | 0.1644 | 42 | 专业净买入额(EUR) |
| `retail_investor_trading_turnover_eur` | VECTOR | 0.1644 | 38 | 散户总成交额(EUR) |
| `shares_sold_retail_investors_daily` | VECTOR | 0.1644 | 36 | 散户当日卖出股数 |
| `net_retail_buying_selling_value` | VECTOR | 0.1644 | 29 | 散户净买入额(本币) |
| `shares_traded_retail_investors_daily` | VECTOR | 0.1644 | 24 | 散户当日成交股数 |
| `total_trading_turnover_eur` | VECTOR | 0.1644 | 15 | 全市场总成交额(EUR) |
| `shares_sold_professional_investors_daily` | VECTOR | 0.1644 | 13 | 专业当日卖出股数 |
| `shares_purchased_professional_investors_daily` | VECTOR | 0.1644 | 12 | 专业当日买入股数 |
| `professional_investor_trading_turnover_eur` | VECTOR | 0.1644 | 11 | 专业总成交额(EUR) |
| `net_professional_buying_selling_value` | VECTOR | 0.1644 | 8 | 专业净买入额(本币) |
| `retail_investor_trading_turnover` | VECTOR | 0.1644 | 7 | 散户总成交额(本币) |
| `average_trade_price_eur` | VECTOR | 0.1644 | 5 | 全市场成交量加权均价(EUR) |
| `total_trading_turnover_value` | VECTOR | 0.1644 | 5 | 全市场总成交额(本币) |
| `closing_trade_price_eur` | VECTOR | 0.1644 | 3 | 收盘成交价(EUR) |
| `highest_executed_price_retail_eur` | VECTOR | 0.1644 | 3 | 散户最高成交价(EUR) |
| `total_orders_placed_daily` | VECTOR | 0.1644 | 3 | 全市场当日订单数 |
| `average_trade_price_professional_eur` | VECTOR | 0.1644 | 2 | 专业成交量加权均价(EUR) |
| `average_trade_price_retail` | VECTOR | 0.1644 | 2 | 散户成交量加权均价(本币) |
| `company_equity_valuation_amount` | VECTOR | 0.1644 | 2 | 公司股权估值(本币) |
| `highest_executed_price_professional_eur` | VECTOR | 0.1644 | 2 | 专业最高成交价(EUR) |
| `lowest_executed_price_professional` | VECTOR | 0.1644 | 2 | 专业最低成交价(本币) |
| `lowest_executed_price_professional_eur` | VECTOR | 0.1644 | 2 | 专业最低成交价(EUR) |
| `market_capitalization_eur` | VECTOR | 0.1644 | 2 | 市值(EUR) |
| `opening_trade_price` | VECTOR | 0.1644 | 2 | 当日首笔成交价(本币) |
| `orders_placed_retail_investors_daily` | VECTOR | 0.1644 | 2 | 散户当日订单数 |
| `average_trade_price_professional` | VECTOR | 0.1644 | 1 | 专业成交量加权均价(本币) |
| `average_trade_price_retail_eur` | VECTOR | 0.1644 | 1 | 散户成交量加权均价(EUR) |
| `highest_executed_price_retail` | VECTOR | 0.1644 | 1 | 散户最高成交价(本币) |
| `highest_executed_trade_price` | VECTOR | 0.1644 | 1 | 全市场最高成交价(本币) |
| `highest_executed_trade_price_eur` | VECTOR | 0.1644 | 1 | 全市场最高成交价(EUR) |
| `lowest_executed_price_retail_eur` | VECTOR | 0.1644 | 1 | 散户最低成交价(EUR) |
| `lowest_executed_trade_price` | VECTOR | 0.1644 | 1 | 全市场最低成交价(本币) |
| `lowest_executed_trade_price_eur` | VECTOR | 0.1644 | 1 | 全市场最低成交价(EUR) |
| `total_shares_purchased_daily` | VECTOR | 0.1644 | 1 | 全市场当日买入股数 |
| `total_shares_traded_daily` | VECTOR | 0.1644 | 1 | 全市场当日成交股数 |
| `average_trade_price` | VECTOR | 0.1644 | 1 | 全市场成交量加权均价(本币) |
| `closing_trade_price` | VECTOR | 0.1644 | 0 | 收盘成交价(本币) |
| `highest_executed_price_professional` | VECTOR | 0.1644 | 0 | 专业最高成交价(本币) |
| `lowest_executed_price_retail` | VECTOR | 0.1644 | 0 | 散户最低成交价(本币) |
| `opening_trade_price_eur` | VECTOR | 0.1644 | 0 | 当日首笔成交价(EUR) |
| `orders_placed_professional_investors_daily` | VECTOR | 0.1644 | 0 | 专业当日订单数 |
| `professional_investor_trading_turnover` | VECTOR | 0.1644 | 0 | 专业总成交额(本币) |
| `shares_traded_professional_investors_daily` | VECTOR | 0.1644 | 0 | 专业当日成交股数 |
| `total_shares_listed` | VECTOR | 0.1644 | 0 | 总流通股本 |
| `total_shares_sold_daily` | VECTOR | 0.1644 | 0 | 全市场当日卖出股数 |

## 2. 六维画像

- **类型**：47/47 全 VECTOR ⇒ **必须 vec_avg/vec_sum 降维**。
- **覆盖率**：全族 cov 0.1644（仅约 1/6 宇宙有值）⇒ **事件/稀疏型** ⇒ 按 2026-11-20 判据
  「cov<0.6 的稀疏型 ⇒ presence 门控是强杠杆（earningscall 实测 S 0.51→1.76）」，**本集应优先试门控**。
- **更新频率**：日频（零售/专业成交拆分为 Nordic & Baltic 市场口径）。
- **分布特征**：金额/股数类为非负或有正负（净额）；价格类为正数且量纲为价格（EUR/本币）⇒ 与无量纲量做算术须先 rank() 化。
- **可用性**：**几乎全部字段 aC ≤ 5**（最高的 `net_retail_buying_selling_value_eur` 也只有 120）⇒ 拥挤度极低，prod 友好窗口期。
- **适用性**：主信号 = **散户 vs 专业的行为分歧**（净买入差、成交均价差、订单失衡）；辅助 = 成交额占比；
  排除 = 市值/股本规模类（是规模变量不是行为变量）。

## 3. 机制假设（三路证据后）

- **论文**（12 篇/8 作者，多样闸 PASS）：
  *Active Attention, Retail Investor Base, and Stock Returns*（JBF 2023）、
  *Individual Investor Trading and Stock Returns*（JFE 2008，Barber Odean）、
  *Retail investor attention and stock liquidity*（JIMF 2015）
  ⇒ 散户是噪声交易者 ⇒ **散户净买入的过度反应随后反转（负向）**；散户活跃度本身预测低质量/高波动。
- **论坛**：无该集专帖；沿用通用纪律（门控、组内相对化）。
- **机制三支**：
  ① **散户净买入（反向）**：散户净买入 ⇒ 后续收益低（买在情绪高点）；
  ② **散户 vs 专业分歧**：散户净买入 − 专业净买入 ⇒ 分歧越大后续收益越低；
  ③ **成交均价差**：散户均价 − 专业均价 = 散户成本溢价 ⇒ 正值意味着散户买贵了 ⇒ 后续跑输。

## 4. TemplatePlan（每字段族一行）

| 字段族 | 合法模板 | 排除 | 依据 |
|---|---|---|---|
| 散户净流量 | `group_rank(ts_zscore(ts_backfill(vec_avg(net_retail_buying_selling_value_eur),66),252),industry)`（正向与**反向**各一） | 裸 rank | 论文① |
| 专业净流量 | 同上骨架换 `net_professional_buying_selling_value_eur`；与散户净流量**差分** | 裸 rank | 论文② |
| 成交额 | 散户成交额/总成交额（占比，需 rank 化无量纲）；专业成交额占比 | 裸 rank | 论文③ |
| 成交价格 | 散户均价 − 专业均价（差值需先各自 rank 化，否则量纲不可减） | 裸价格 | 论文③ |
| 订单数 | 散户订单数 − 专业订单数（失衡）；订单数 / 成交额 | 裸 rank | 微观结构 |
| 规模 | **排除**（市值/股本是规模变量） | 主信号 | — |
| 门控 | `trade_when(vec_avg(total_orders_placed_daily) > 0, <骨架>, -1)`（cov 0.164 稀疏 ⇒ 门控强杠杆） | — | 今日门控判据 |

## 5. 段1 回测计划（12 臂）

主骨架 `group_rank(ts_zscore(ts_backfill(vec_avg(F),66),252),industry)`。
覆盖：散户净流入正/反 2 + 专业净流入 1 + 散户−专业差分 1 + 成交额占比 2 + 均价差 2 + 订单失衡 2 + 门控 2。

## 6. 段1 实测（2026-11-20，12 臂：8 COMPLETE + 4 UNITS WARNING）

### 6.1 ★ 突破：presence 门控把 S 从 0.91 抬到 2.36

| 形态 | alpha | S | F | 2Y | sub | TO | failed_ra |
|---|---|---:|---:|---:|---:|---:|---:|
| **门控（总成交额>0）+ 散户−专业净买入差分** | **rK7dx1z3** | **2.36** | **1.00** | **3.12** | 1.55 | 59.4% | **0** |
| 无门控：散户净买入（正向） | O0WJ3vGb | 0.91 | 0.62 | −0.08 | 0.79 | 14.3% | 3 |
| 无门控：散户−专业差分 | A1xQAd0d | 0.91 | 0.62 | −0.08 | 0.79 | 14.3% | 3 |
| 无门控：散户均价−专业均价 | 78YopVNx | 0.66 | 0.42 | −0.18 | 0.63 | 11.8% | 3 |
| 无门控：订单失衡 | XgaR0EJ5 | 0.56 | 0.32 | −0.30 | 0.60 | 11.6% | 3 |
| 无门控：总订单数 | A1xQAdvw | 0.59 | 0.35 | −0.54 | 0.46 | 11.5% | 3 |
| 无门控：专业净买入 | 58JjXVlJ | 0.25 | 0.09 | −0.76 | 0.28 | 14.3% | 3 |
| 无门控：均价差（反向） | 88NvwqjX | 0.52 | 0.28 | −0.60 | 0.42 | 11.8% | 3 |

**门控效应**：S 0.91→**2.36**（+1.45）、2Y −0.08→**3.12**（+3.20）、sub 0.79→1.55、failed_ra 3→**0**。
**方向确认**：无门控版的 2Y 全负（−0.08~−0.76）⇒ 散户vs专业分歧的**近端两年**信号极弱，
而**门控后近端极强** ⇒ 该族的信息**只存在于「有成交的日子」，其余时间的读数是稀释噪声**（与 earningscall 同构）。

**★ 今日门控判据第三次验证**：cov 0.164 的稀疏事件型 ⇒ presence 门控是强杠杆（earningscall cov0.51：S 0.51→1.76；
institutions cov0.88：门控 8 臂全灭）。**判据「cov<0.6 才试门控」成立。**

### 6.2 工程坑：净流量字段带量纲

`net_*_buying_selling_value_eur` 等金额字段量纲 = `Unit[CSPrice:1,CSShare:1]` ⇒
与常数 0/1 做算术（`subtract(0,x)` / `add(y,1)`）**直接撞 UNITS**（4 臂 WARNING）；
**同量纲相减（散户−专业）是合法的**，`subtract(0, x)` 须先 `rank()` 化。
