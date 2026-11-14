# 第 12 颗候选 LLKPwej2 被否 + BE24 结论（2026-11-11 23:0x）

## 一、LLKPwej2 指标亮眼但 self 判死

| 项 | 值 | 判定 |
|---|---|---|
| S | 1.69 | ✅ |
| F | 1.29 | ✅ |
| sub | 0.89 | ✅ |
| 2Y | 2.20 | ✅ |
| TO | 0.1484 | ✅ |
| 平台 checks | NONE | ✅ |
| ra_failed | 0 | ✅ |
| 塔 | SHORTINTEREST 单塔（严格 ATOM） | ✅ |
| **self** | **0.7161** | ❌ **>0.7 不通过** |

**表达式**：`max_loan_rate_p5_d1 × shrt3_bar`（两腿同属 shortinterest3）

**死因**：两条腿在已提交池里都有对应件——
- 第一腿 `max_loan_rate_p5_d1` 由 d5a2vxzY 代表；
- 第二腿 `shrt3_bar` 由 78Yk8VR1 / qM7KxkQV / Jj8VQwoe 代表。

⇒ 再次验证「强腿配额」约束：**用已占腿组合出的件，平台自池直接拦下**。
这是本轮第 4 次撞到同一条墙（前三次：rK71dLbE 0.845 撞 qM7KxkQV、E569ZE7L 1.0 撞 78Yk8VR1、四颗 _p5_d1 件 0.85-0.885 撞 qM7KxkQV）。

## 二、BE24 结论：借券族的非利率维度全部无效

| 臂 | 组合 | S | F | sub | 2Y | 判定 |
|---|---|---:|---:|---:|---:|---|
| 7 | max_rate × **shrt3_bar** | 1.69 | 1.29 | 0.89 | 2.20 | self 判死 |
| 3 | max_rate × 负 min_rate | 1.65 | 1.18 | 0.74 | 1.91 | sub 差 0.04 |
| 1 | max_rate × **transaction_count** | **0.77** | 0.32 | 0.47 | -0.17 | ❌ |
| 5 | rate_vol × transaction_count | 0.59 | 0.22 | 0.40 | 0.08 | ❌ |
| 2 | max_rate × min_rate（正） | 0.47 | 0.15 | 0.23 | 0.93 | ❌ |
| 6 | duration × transaction_count | 0.43 | 0.14 | 0.58 | -0.06 | ❌ |
| 8 | txn_count × shrt3_bar | 0.29 | 0.07 | 0.58 | -0.74 | ❌ |
| 4 | loaned_share × txn_count | 0.28 | 0.07 | 0.08 | 0.59 | ❌ |

**`transaction_count`（交易笔数=流动性代理）作为第二腿全面失败**（最高 0.77），
说明「借券市场流动性」这个机制在 DEU 不成立。
⇒ shortinterest3 里真正有效的只有 **利率维度** 和 **shrt3_bar 借款需求评分**。

## 三、shortinterest3 的有效面收口

| 维度 | 字段 | 与其他维度组合效果 |
|---|---|---|
| 利率 - 最高 | max_loan_rate_p5_d1 | ✅ 最强（×mean=1.60 全闸 / ×nws20=1.86 全闸） |
| 利率 - 平均 | mean_loan_rate_p5_d1 | ✅ 可用（×max=1.60 全闸） |
| 利率 - 最低 | min_loan_rate_p5_d1 | ⚠ 偏弱（×max=1.65 但 sub 差 0.04） |
| 利率 - 波动 | loan_rate_volatility_p5_d1 | ⚠ 偏弱（最高 1.13-1.20） |
| 借款需求评分 | shrt3_bar | ⚠ self 受限（已有多件占用） |
| 借出市值 | loaned_market_value_usd_p5_d1 | ❌ 弱（1.13-1.18） |
| 借出股数 | loaned_share_count_p5_d1 | ❌ 弱（1.20） |
| 交易笔数 | transaction_count_p5_d1 | ❌ 无效（≤0.77） |
| 借券期限 | average_loan_duration_days_p5_d1 | ❌ 弱（≤1.45） |

⇒ **shortinterest3 单塔的有效组合已基本穷尽**：利率三维度（max/mean/min）互配已试尽，
非利率维度全部偏弱或无效。**单塔继续产出的空间很小**。

## 四、对 goal「20 个 ATOM」的现实评估

| 口径 | 当前 | 目标 | 缺口 |
|---|---:|---:|---:|
| 严格 ATOM（单数据集单塔） | **5** | 20 | 15 |
| ATOM + regular 合计 | **11**（含 9qlz29Oe） | 20 | 9 |
| 正文第 4 条要求 | **10 已达成** | 10 | 0 |

**严格 ATOM 缺口 15 颗的现实约束**：
1. DEU D1 只有 4 个有效字段族（shortinterest3 / analyst-anl93 / insiders1 / other47）；
2. 单塔 ATOM 必须单数据集，而这 4 族中 insiders1 与 other47 单用天花板低（0.65/0.85）；
3. shortinterest3 单塔有效组合已穷尽（见第三节）；
4. analyst 族已有 4 颗已提交件占用，新增会撞 self。

⇒ **严格 ATOM 20 颗在 DEU D1 内不可达**，这是区域容量问题，不是探索不足。
正文第 4 条的 10 颗已达成（含 regular），符合用户「实现不了 ATOM 就考虑 regular」的授权。