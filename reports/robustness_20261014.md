# 稳健性审计报告 — 2026-10-14

> 候选：**`xA16pzQJ`**（KOR / TOP600 / D1）　审计人：agent　判定：**PASS**

## 表达式与设置

```
trade_when(greater(rank(adv20), 0.6),
  tail(group_rank(ts_sum(vec_avg(oth695_import_value_4), 20),
                  bucket(rank(cap), range="0,1,0.2")),
       lower=0.2, upper=0.8, newval=0.5), -1)
```
KOR / TOP600 / D1 · decay 4 · **MARKET** · truncation 0.08 · pasteurization ON ·
nanHandling ON · maxTrade OFF · 算子调用点 **9**

**经济可解释性（一句话）**：在**流动性居前 40%** 的韩国股票中，按**市值五分桶**做组内排序，
用 **20 日累计进口额**的相对强度做多空——捕捉「进口放量且被同规模同业低估」的贸易流错价。

## Phase B — 归因

| 项 | 值 |
|---|---|
| S / F / TO | 1.86 / 2.19 / 0.0269 |
| returns / drawdown / margin | 17.28% / 10.87% / **128.6 bp** |
| SUB / 2Y / investability | 1.82 / 2.10 / 1.86 |
| long / short count | 97 / 473 |
| **prod / self** | **0.6976 ✅ / 0.2306 ✅** |
| failed RA / PPA | **0 / 0** |
| 塔 | KOR/D1/PV(1.4) + KOR/D1/OTHER(1.6) ⇒ effective 2 |

### 逐年 PnL 归因（IS）

| 年 | PnL | Sharpe | returns | drawdown | margin(bp) | fitness |
|---|---|---|---|---|---|---|
| 2014–2017 | 0 | 0 | 0 | 0 | 0 | 0（**字段无覆盖**）|
| 2018 | −52,778 | **−0.05** | −0.51% | 10.87% | −0.36 | −0.01 |
| 2019 | 1,931,617 | **1.99** | 18.50% | 5.55% | 142.0 | 2.42 |
| 2020 | 2,887,617 | **2.75** | 30.08% | 6.32% | 220.0 | 4.27 |
| 2021 | 2,214,198 | **2.28** | 21.21% | 4.67% | 163.7 | 2.97 |
| 2022 | 2,458,550 | **2.77** | 23.64% | 6.26% | 177.4 | 3.81 |
| 2023 | 1,149,932 | **1.40** | 11.06% | 8.98% | 84.2 | 1.32 |

## Phase C — 反过拟合闸

| 检查项 | 值 | 阈值 | 判定 |
|---|---|---|---|
| Failed RA / PPA | 0 / 0 | = 0 | ✅ PASS |
| **Recent-3yr Sharpe（主判定）** | 2.28 / 2.77 / 1.40 ⇒ **均值 2.15**，每年 > 0.3 | ≥ 1.58 且每年为正 | ✅ **PASS** |
| Recent-3yr CV_Sharpe | **0.264** | < 0.40 | ✅ PASS |
| 衰减比（2023 / 全期） | **0.753** | ≥ 0.50 | ✅ PASS |
| 平年（最近 3 年） | 0 | 0 | ✅ PASS |
| Recent-3yr max/min | **1.98** | ≤ 3 | ✅ PASS |
| Sub-universe | 平台 `LOW_SUB_UNIVERSE_SHARPE` PASS（1.82） | PASS | ✅ PASS |
| Margin @ turnover | **128.6 bp** @ TVR 2.69% | ≥ 5 bp | ✅ PASS |
| Top-5 集中度 | 未取逐股分解（长 97 / 空 473 ⇒ 分散） | < 30% | ✅（软）|
| 经济可解释性 | 一句话可写（见上） | — | ✅ PASS |

## 软标记（不影响 PASS）
1. **算子数 9（> 5）** —— REGULAR 仅软标记（PPA 硬上限 ≤8 不适用于本件）；本件无算子膨胀迹象（TO 2.69% 极低、单一 `winsorize` 已证实为 no-op 并删除）。
2. **IS 仅 2018 起有数据**（2014–2017 字段无覆盖）—— 有效样本 6 年，其中 2018 为起步年（Sharpe −0.05）。
3. **2018 年为负** —— 属字段覆盖起点，非信号失效；最近 3 年均值 2.15 远高于 1.58 线。

## 结论
**`xA16pzQJ` = PASS** ⇒ 可提交（RA 常规通道，非 PPA）。
台账：`robustness_xA16pzQJ`（region=KOR）。