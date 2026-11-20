# EUR / pv109（可转债）全字段画像（2026-11-20）

> 平台实查 `get_datafields(dataset_id=pv109, region=EUR, universe=TOP2500, delay=1)`：**25/25 字段，complete=True**（全部 VECTOR）。
> 类别 pv ⇒ EUR/D1/**PV 塔 2/3（差 1 席）**；mult 1.1；**cov 0.4397**；**aC 0–11（极冷门）**；2025-10 新代 21 个 + 2022-12 老代 4 个。
> 命名规则 `eur_<category>_<dataset>_profile_<YYYYMMDD>.md`。**PV 类按用户红线不得两两组腿 ⇒ 本集只能单集 ATOM。**

## 1. 字段结构总览（6 语义族）

| 语义族 | 字段数 | 说明 |
|---|---:|---|
| 转股收益率 | 3 | ask/bid/midpoint 的转股收益率 = 转股溢价的倒数（**核心族**） |
| 信用收益率 | 5 | ask/bid/midpoint 的到期收益率 + 重复字段 |
| 报价 | 5 | 中间价/最新价/最高买/最低卖 → 可构造买卖价差 |
| 票息 | 3 | 名义票息/当期票息/付息频率 |
| 规模 | 4 | 面值/发行总额/未偿本金/赎回金额 |
| 事件 | 2 | 公告日/到期日 |

## 字段全表（25 字段逐字段平台读数，cov 均 0.4397）

| 字段 | 类型 | cov | uC | aC | 语义族 | 说明 |
|---|---|---:|---:|---:|---|---|
| `ask_side_conversion_yield` | VECTOR | 0.4397 | 4 | 4 | 转股收益率 | 按卖价算的转股收益率（转股溢价倒数） |
| `ask_side_yield_to_maturity` | VECTOR | 0.4397 | 1 | 1 | 信用收益率 | 按卖价算的到期收益率 |
| `bid_side_conversion_yield` | VECTOR | 0.4397 | 2 | 2 | 转股收益率 | 按买价算的转股收益率 |
| `bid_side_yield_to_maturity` | VECTOR | 0.4397 | 1 | 1 | 信用收益率 | 按买价算的到期收益率 |
| `bid_side_yield_to_maturity_duplicate` | VECTOR | 0.4397 | 2 | 2 | 信用收益率 | 按买价算的到期收益率（重复字段） |
| `bond_coupon_rate` | VECTOR | 0.4397 | 2 | 3 | 票息 | 名义票息率 |
| `coupon_payment_frequency` | VECTOR | 0.4397 | 1 | 1 | 票息 | 付息频率代码 |
| `current_coupon_rate` | VECTOR | 0.4397 | 1 | 1 | 票息 | 当期适用票息率 |
| `face_value_amount` | VECTOR | 0.4397 | 4 | 5 | 规模 | 面值/本金 |
| `highest_bid_price` | VECTOR | 0.4397 | 3 | 3 | 报价 | 最高买价 |
| `initial_issue_price` | VECTOR | 0.4397 | 3 | 3 | 价格 | 发行价 |
| `interest_day_count_basis` | VECTOR | 0.4397 | 1 | 1 | 元数据 | 计息天数基准代码 |
| `last_traded_price` | VECTOR | 0.4397 | 2 | 2 | 报价 | 最近成交价 |
| `lowest_ask_price` | VECTOR | 0.4397 | 2 | 2 | 报价 | 最低卖价 |
| `midpoint_conversion_yield` | VECTOR | 0.4397 | 1 | 1 | 转股收益率 | 按中间价算的转股收益率 |
| `midpoint_trade_price` | VECTOR | 0.4397 | 4 | 4 | 报价 | 中间成交价 |
| `midpoint_yield_to_maturity` | VECTOR | 0.4397 | 2 | 2 | 信用收益率 | 按中间价算的到期收益率 |
| `minimum_bond_denomination` | VECTOR | 0.4397 | 1 | 1 | 元数据 | 最小交易面值 |
| `minimum_trade_increment` | VECTOR | 0.4397 | 0 | 0 | 元数据 | 最小价格变动单位 |
| `pv109_amt_issued` | VECTOR | 0.4397 | 2 | 3 | 规模 | 发行总额 |
| `pv109_amt_outstanding` | VECTOR | 0.4397 | 1 | 1 | 规模 | 当前未偿还本金 |
| `pv109_announce_dt` | VECTOR | 0.4397 | 2 | 2 | 事件 | 发行/事件公告日 |
| `pv109_maturity` | VECTOR | 0.4397 | 3 | 3 | 事件 | 到期日 |
| `redemption_value_amount` | VECTOR | 0.4397 | 10 | 11 | 规模 | 赎回/到期偿付金额 |
| `total_traded_volume` | VECTOR | 0.4397 | 2 | 2 | 成交 | 债券当日成交量 |

## 2. 六维画像

- **类型**：25/25 全 VECTOR ⇒ 必须 vec_avg/vec_sum 降维；比率类字段须先各自标准化再相减（量纲）。
- **覆盖率**：cov 0.4397（约 4/9 宇宙有值）——**中等覆盖、非极稀疏** ⇒ presence 门控判据（cov<0.6）适用但预期弱于 earningscall/investor_activity。
- **更新频率**：债券报价与收益率随交易日更新；发行/到期事件稀疏。
- **分布特征**：价格类（面值/报价）= 正数有量纲；收益率类 = 百分比（可正可负）；规模类 = 金额（重尾）。
- **可用性**：**aC 0–11 极冷门**（对照 pv1 的 44048、pv20 的 595）⇒ **prod 友好窗口期，且是全新信息源（债市）**。
- **适用性**：主信号 = **转股收益率**（转股溢价）与**信用利差**（YTM−票息）；辅助 = 买卖价差（债市流动性/不确定性）、发行规模（供给冲击）；排除 = 日期/代码/最小单位类元数据。

## 3. 机制假设（三路证据后）

- **论文**（12 篇/10 作者，多样闸 PASS）：*Can convertible bond trading predict stock returns? Evidence from China*（PACF 2023）、
  *Long-run Stock Returns Following Convertible Bond Issuance and Insider Trading*（2025）、
  *Mispricing and the Cross-Section of Stock Returns*（JFE 2008）等
  ⇒ 可转债市场对正股的定价含**增量信息**；转股溢价高 ⇒ 正股被高估 ⇒ 后续收益低（负向）。
- **论坛**：本会话未取该集专帖（字段冷门，aC 0–11）。
- **三支机制**：
  ① **转股溢价**：`midpoint_conversion_yield` 高 ⇒ 正股相对贵 ⇒ 后续收益低（负向）；
  ② **信用利差**：`midpoint_yield_to_maturity − bond_coupon_rate` 高 ⇒ 信用风险被重新定价 ⇒ 后续收益低；
  ③ **债市信息领先/供给冲击**：`total_traded_volume` 与 `pv109_amt_issued` 变化 ⇒ 债市先于股票市场知情（正/负向待实证）。

## 4. TemplatePlan（每字段族一行）

| 字段族 | 合法模板 | 排除 | 依据 |
|---|---|---|---|
| 转股收益率 | `group_rank(ts_zscore(ts_backfill(vec_avg(midpoint_conversion_yield),66),252),industry)`（正向+反向各一） | 裸 rank | 论文① |
| 信用收益率 | `midpoint_yield_to_maturity` 水平；与 `bond_coupon_rate` 的**差**（须各自 rank 化后相减，量纲不可直接减） | 裸 rank、裸减 | 论文② |
| 报价 | 买卖价差 = `rank(highest_bid) − rank(lowest_ask)`（债市不确定性/流动性）；`midpoint_trade_price ÷ face_value_amount`（折价率，须 rank 化） | 裸价格 rank | 机制③ |
| 成交 | `total_traded_volume` 的对数/变化率（债市关注度） | 裸 rank | 机制③ |
| 规模 | `pv109_amt_issued ÷ pv109_amt_outstanding`（供给压力，须 rank 化）；`redemption_value_amount ÷ face_value_amount`（赎回溢价） | 裸 rank | 机制③ |
| 票息 | `bond_coupon_rate` 与 `current_coupon_rate` 的差（票息调整） | 裸 rank | 辅助 |
| 事件/元数据 | **排除**（公告日/到期日/最小单位/计息基准 = 元数据） | 主信号 | — |

## 5. 探针计划（12 臂）

主骨架 `group_rank(ts_zscore(ts_backfill(vec_avg(F),66),252),industry)`：
转股收益率 3 + 信用利差 3 + 价差/折价 3 + 成交/供给 3。
⚠ 先做**存在性与覆盖探针**（本集从未回测）：确认 25 字段哪些在 EUR 真有值，避免又做一个空字段族。
