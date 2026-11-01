# news21 · KOR/D1/TOP600 字段画像（**判定：无可投信号，不投配额**）

> 画像日：2026-10-30（平台 `get_datafields` 实测，13 字段全量，`filter_sharpe=false`）
> 数据集级：coverage **0.7435**（`get_datasets`）/ fieldCount 13 / userCount 70 / alphaCount 143 / category **news** / 塔乘数 **1.6**
> 名字：Macro Economic Event Data（平台描述：公司重大事件的实时摘要，按 topic/significance 打标）

## §1 全字段清单与可用性判定

| 字段 | 类型 | cov | aC | description 实质 | 判定 |
|---|---|---|---|---|---|
| `nws21_event_freq` | MATRIX | **.967** | **115** | number of events（事件条数） | ⚠ **唯一数值信号**，但属**计数轴** |
| `estimated_next_shareholder_meeting_date` | MATRIX | .593 | 3 | 下次股东大会**日期整数** YYYYMMDD | ⛔ 日期字段，不得作信号 |
| `next_earnings_estimate_date` | MATRIX | .467 | 5 | 下次财报**预估日期** YYYYMMDD | ⛔ 日期字段 |
| `previous_shareholder_meeting_date` | MATRIX | .388 | 5 | 上次股东大会日期 | ⛔ 日期字段 |
| `previous_ex_dividend_event_date` | MATRIX | .330 | 4 | 上次除息日（**USA module**） | ⛔ 日期字段 + 口径是美股 |
| `event_start_time_2` / `event_end_time` | VECTOR | .865 | 2/1 | 事件开始/结束**本地时间** | ⛔ 时刻字段 |
| `event_start_date_type` / `event_end_date_type` | VECTOR | .865 | 2/0 | 日期类型标签（actual/estimated） | ⛔ 分类标签 |
| `event_start_date_is_estimated` / `event_end_date_is_estimated` | VECTOR | .865 | 2/1 | 是否预估（0/1 flag） | ⛔ 二值 flag，无横截面分辨力 |
| `event_fiscal_year` | VECTOR | .865 | 2 | 财年标签 | ⛔ 标签 |
| `event_quarter_label` | VECTOR | .865 | 0 | 季度标签 | ⛔ 标签，αC=0 |

**结论：13 个字段里 12 个是日期 / 时刻 / 标签 / flag，只有 1 个数值量 `nws21_event_freq`。**

## §2 为什么唯一数值字段也不投

- `nws21_event_freq` = **事件计数轴**。KOR news 塔的计数轴**已两度判死**：
  - `news7`（Real Time News Feed，注意力计数）：wave187b 8/8 全灭，max\|S\|=**0.55**（`tracking/KOR/reference/datasets/news7.md` §7.1）
  - `other106`（KOSPI 成分/公司行为供给冲击）：wave190 max\|S\|=0.75，机制判死
- 本集计数是**全事件类型混合计数**（M&A/分红/股东大会/财报全算一类），比 news7 的「新闻条数」信息含量更低，
  且没有可分离的事件类型维度（类型只存在于 VECTOR 标签字段，进不了常规算子）。
- cv .967 的高覆盖来自**日历事件本身覆盖全**，不代表信息量。

## §3 裁决

- ⛔ **news21 不投配额**：无机制、唯一数值字段落在已判死的计数轴、其余字段全是日期/标签。
- ⛔ 本集**不进** dead 表（它只是「没有可投字段」，不构成机制级判死证据链），
  但后续任何「news21 事件计数」提案须先引用本页否决。
- 迁移价值：无。若将来要做财报时点类信号，走 **earnings3**（8 字段纯日历，`ern3_next_interval` 已验证 S 0.94 / 2Y 1.68）。
