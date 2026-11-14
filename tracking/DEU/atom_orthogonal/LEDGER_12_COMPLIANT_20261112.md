# 台账更新：合规交付 12 颗（新增 KPg3NZX8）

日期：2026-11-12

## 新增合规件（BE139 news 族唯一独立件）

| alpha | 构造 | S | F | 2Y | sub | TO | 塔 | checks |
|---|---|---:|---:|---:|---:|---:|---|---|
| **KPg3NZX8** | `S7 + 相关度加权新闻情绪` | **1.72** | **1.36** | **2.10** | **1.07** | 13.8% | **PV+INSIDERS+NEWS** | **fail=[] 9 PASS** |

```
S7 = A×C + B×FR + C + B
A  = group_rank(ts_delta(ts_mean(vec_avg(insd1_holdings),66),66),sector)
B  = group_rank(ts_ir(vec_avg(insd1_holdings),66),sector)
C  = group_rank(ts_mean(SV1/(SV1+SV2+SV3+SV4),66),sector)
FR = group_rank(1/(days_from_last_change(insd1_holdings)+1),sector)
NEWS腿 = group_rank(ts_mean(multiply(vec_avg(nws104_sentiment), vec_avg(nws104_relevance)),66),sector)
外层 = signed_power(group_zscore(group_zscore(group_neutralize(·,bucket(rank(cap),range="0,1,0.1")),sector),market),1.3)
```

**合规性**：塔 = PV + INSIDERS + NEWS，trio 成员只有 **PV** 一个 ⇒ 合规（PV+NEWS 是 goal 原文举例允许的组合）。
**注**：`pyramids.effective = 0`（三塔被判 0），不影响闸通过，但**不贡献塔倍率**。

## 同批被否的件

| alpha | S | 原因 |
|---|---:|---|
| N1P0a857 | 1.68 | 与 KPg3NZX8 **0.9936** 同源 ⇒ 只能取 1 颗 |
| 1YWeX0aQ | 1.70 | fail=IS_LADDER_SHARPE |
| vRA8rPeQ | 1.67 | fail=IS_LADDER_SHARPE |
| vRA8rP5a / 3q0wXJEe / oma7LZ9b | 1.56-1.62 | fail 1 |
| npa9drZa | 1.49 | S 不足 + fail 3 |
| MP6OaVbz / qM78xVg1 | 0.46 / 0.53 | news 单腿弱（对照确认 news 必须作辅助腿）|

## 交付进度

| 项 | 数 |
|---|---:|
| 已 ACTIVE | 6 |
| 待授权合规（存量）| 5 |
| **新增合规** | **1**（KPg3NZX8）|
| **合规合计** | **12 / 20（60%）** |
| 缺口 | **8** |

## 关键规律（已成方法论）

**每个「搭档族」只贡献约 1 颗独立件**（该族内部变体互相关 0.99）。
⇒ 要补 8 颗，必须**换 8 个不同搭档族**，而不是在同一族里做变体。

DEU D1 可用搭档族（均为非 trio，可与 insiders 组腿）：
NEWS ✅已用 / RISK / EARNINGS / FUNDAMENTAL / SENTIMENT / ANALYST / SHORTINTEREST / INSTITUTIONS / MACRO / SOCIALMEDIA / OPTION / IMBALANCE
trio 成员（PV/MODEL/OTHER）**最多只能选一个**。
