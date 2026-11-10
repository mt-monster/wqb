# DEU 第三席：波 AF / AG 突破记录（2026-11-10 上午末）

> **本轮最重要的产出**：借券塔（shortinterest）**可以出 2 席** —— 判据 MY「族内扩容第一顺位是换字段」被证实。

## 一、波 AF：shortinterest3 不同字段（借券塔第二席）

10 条，全部用 264/132 双窗口加速度 × target_tvr_decay 骨架，取负（反向持有）。

| 候选 | 字段 | S | F | 2Y | TO | lc | 判定 |
|---|---|---:|---:|---:|---:|---:|---|
| **1YNrQMr6** | `max_loan_rate_p5_d1` | **1.77** | **1.32** | 1.60 | 0.1156 | 214 | **四闸全过**（failed_ra=0） |
| **E569Xd91** | `max_loan_rate_main` | **1.61** | **1.16** | 1.94 | 0.1149 | 228 | **四闸全过**（failed_ra=0） |
| npvLMEEq | `mean_loan_rate_main` | 1.46 | 0.98 | 2.17 | — | 220 | F 0.98 未过 |
| zq3l1VVV | `mean_loan_rate_p5_d1` | 1.46 | 0.99 | 1.23 | — | 207 | F + 2Y 未过 |
| 3qo8ZN8X / N1NYvZYE / d5WNAGNE / P0okdVkx / 2rA3b31b / vR1W3WKz | 其余字段 | 0.76~1.24 | — | — | — | — | 未过 |

### ★ 判据 MY 证实：族内扩容的第一顺位是换字段，不是换参数

`compute_mutual_correlation(threshold=0.7, years=4)`，21 颗全算：

| 配对 | 互相关 | 结论 |
|---|---:|---|
| **E569ZE7L ~ 1YNrQMr6** | **0.6025** | ✅ **< 0.7 ⇒ 借券塔两席成立** |
| E569ZE7L ~ E569Xd91 | 0.7095 | ✗ 超线（同为借券费率，信息面太近） |
| 1YNrQMr6 ~ E569Xd91 | 0.8789 | ✗ 超线（同信息面） |
| 1YNrQMr6 ~ xArzm3Mn | 0.3417 | ✅ |
| 1YNrQMr6 ~ 1YNMAA8M | 0.1351 | ✅ |

**最大独立集 = 20**（E569ZE7L + 1YNrQMr6 + 1YNMAA8M + 17 件 OS）

信息面分层清晰：
- `shrt3_bar`（借券**需求评级**）↔ `max_loan_rate*`（借券**费率**）= 不同信息面 ⇒ 互相关仅 0.60
- `max_loan_rate_p5_d1` ↔ `max_loan_rate_main` = 同一信息面 ⇒ 互相关 0.88

### 稳健性判定（按 Phase C 判定表，总体 sd 口径）

| 候选 | 近3年 | 均值 | CV | 衰减比 | 平年 | max/min | 主判 | 总判定 |
|---|---|---:|---:|---:|---:|---:|---|---|
| 1YNrQMr6 | 0.85 / 3.04 / **0.12** | 1.337 | 0.928 | **0.068** | 1 | **25.33** | REJECT | **REJECT** |
| E569Xd91 | **-0.07** / 3.23 / 0.63 | 1.263 | 1.124 | — | — | — | REJECT（负年） | **REJECT** |

⇒ 两件都因**末年/单年崩塌**被稳健性闸拦下（1YNrQMr6 的 2023 S=0.12；E569Xd91 的 2021 S=-0.07）。
但**它们证明借券塔的族容量是 2**（不是 1）⇒ 波 AH 定向修复第二席。

## 二、波 AG：institutions6 机构持仓买卖流（新骨架重测）—— 判死

10 条（S -0.33 ~ +0.33，2Y -1.02 ~ +1.66），全部判死，**符号混乱**。

覆盖 lc 184~196（满覆盖）⇒ 排除覆盖因素。
字段：market_value/quantity_institutional_shares_acquired·disposed、
count_institutional_buyers·sellers·holders_security、aggregate_equity_value_institutions。

**结论**：institutions6 即使用新骨架（264/132 加速度）仍然符号混乱 ⇒ **真噪声，终局判死**。
（与 shortinterest3 的区别：后者是「方向反了可翻转」+ 强度可挖；前者是无信号。）

**判据 MZ 的补充**：新骨架重测后仍符号混乱 ⇒ 该族判死升级为终局，不再重测。

## 三、本轮新增判据

| 编号 | 判据 | 要点 |
|---|---|---|
| MX | **已判死族要用新骨架重测** —— 族级判死只在当时骨架下成立；shortinterest3 旧判死(S≤0.90) → 新骨架出货 8+ 颗 | 台账记判死要**连同当时骨架**一起记 |
| MY | **族内扩容第一顺位 = 换字段，不是换参数** | 同信息面（rate_p5_d1 vs rate_main）互相关 0.88；跨信息面（需求评级 vs 费率）仅 0.60 |
| MZ | 新骨架重测后仍符号混乱 ⇒ 判死升级终局 | institutions6 二次判死 |

## 四、DEU 域内可交付上限（修正）

**借券塔可出 2 席**（E569ZE7L + 1YNrQMr6 的字段组合），
加上 1YNMAA8M 与 2 颗已 ACTIVE ⇒ **上限 = 5 颗**（原估 4 颗）。

当前待授权提交（均四闸全过）：
| alpha_id | 稳健性 | 备注 |
|---|---|---|
| 1YNMAA8M | **PASS** | 无争议 |
| E569ZE7L | CONDITIONAL | CV 0.511 + max/min 4.80，repair 第1轮已跑完 |
| 1YNrQMr6 | REJECT | 2023 崩塌，**波 AH 修复中** |
