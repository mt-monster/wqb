
# 稳健性审计报告 — 2026-10-09

## 候选 `2rmGAPqN`（REGULAR，DEU / TOP500 / d1）

> **用户明确指令放宽**：`max/min (近3年) = 6.19 > 5` 一项经用户知情后放行
> （2026-10-09，用户裁决原文：「提交 2rmGAPqN（推荐）」）。其余项全部 PASS。

### 表达式与设置
```
tail(winsorize(group_rank(multiply(
  ts_sum(divide(vec_sum(inst1_valueeur),add(vec_sum(inst1_holdings),0.0001)),220),
  if_else(and(greater(ts_sum(同上,220),0),
              greater(ts_sum(vec_avg(inst1_tradesignificance),66),2.0)),1,0)),
  oth455_partner_n2v_p50_q200_w1_pca_fact2_cluster_20),std=2),
  lower=0.25,upper=0.75,newval=0.5)
```
settings：`DEU / TOP500 / d1 / decay 4 / FAST / truncation 0.08 / nanHandling ON / pasteurization ON`

### 顶层指标
| 指标 | 值 |
|---|---|
| sharpe | **1.81** |
| fitness | **1.48** |
| two_year | **2.55** |
| sub_universe | **1.30** |
| turnover | 0.1296 |
| margin | 13.4 bp |
| investability | 1.82 / 1.53 |
| 金字塔 | `DEU/D1/INSTITUTIONS ×1.6` + `DEU/D1/OTHER ×1.8` |

### Phase B.0 失败门（硬前置）
`Failed RA = 0`；`Failed PPA = 0`；`checks.fail` 为空；9 项硬闸全 PASS。**通过。**

### Phase B.2 逐年归因（2014–2017 无持仓，数据覆盖原因）
| 年 | 2018 | 2019 | 2020 | 2021 | 2022 | 2023 |
|---|---|---|---|---|---|---|
| sharpe | 1.40 | 2.07 | 1.20 | 0.52 | 1.95 | 3.22 |
| margin(bp) | 14.6 | 13.1 | 9.9 | 4.1 | 16.5 | 21.7 |

### Phase C 反过拟合闸

| 检查项 | 值 | 判定 |
|---|---|---|
| WebDataScope failed count | 0，无 PENDING | **PASS** |
| Recent-3yr Sharpe（0.52/1.95/3.22） | mean **1.90** ≥ 1.58，每年 > 0.3 | **PASS** |
| Recent-3yr CV_Sharpe | **0.582** | **CONDITIONAL**（0.40–0.60） |
| 衰减比 | 3.22 / 1.81 = **1.78** | **PASS** |
| 平年（近3年） | **0 个** | **PASS** |
| **Recent-3yr max/min** | 3.22 / 0.52 = **6.19** | **★ 超 5 —— 按用户指令放宽** |
| 全历史早年疲软 | 无（2018–2020 均正） | 软标记：无 |
| Sub-universe | 平台 PASS | **PASS** |
| Margin @ turnover | 13.4 bp ≥ 5 bp | **PASS** |
| Top-5 集中度 | 不可得（无逐股分解） | 未评 |
| 经济可解释性 | 「内部人**买入侧** + **高交易显著性（机会型）** 的信念强度，按供应链合作伙伴图谱簇内排序」 | **PASS** |

### 判定

**`CONDITIONAL`（含 1 项经用户指令放宽的硬标记）**

- 主判定（近3年强度、CV、衰减比、平年、sub、margin、可解释性）**全部通过**；
- 唯一超标项 `max/min = 6.19`，成因是 **2023 年异常高（3.22）**，而非 2021 年极端差
  （2021 的 0.52 > 0.3 平年线，非「单年行情驱动」形态）；
- 该项经用户**明确指令**放宽（skill 规定：放宽入口 = 用户明确指令，须留痕 soft_flags）。

### 修复过程（从触发硬阈到达标）

| 阶段 | S | 近3年 CV | max/min |
|---|---|---|---|
| 原始 `58gGQmlN`（窗口 66） | 1.62 | 0.732 ❌ | 22.5 ❌ |
| `GrOQgewQ`（窗口 132） | 1.68 | 0.594 ✅ | 6.96 ❌ |
| **`2rmGAPqN`（窗口 220）** | **1.81** | **0.582 ✅** | **6.19 ❌**（放宽） |

修复手段六类（W243–W246，32 条）系统尝试：阈值调整 / `ts_rank`·`ts_zscore` 年度无关化 /
流动性·波动门控 / 多轴嵌套 / 双窗 / 时序平滑 —— **唯一有效 = 加长窗口**（2021 年 S: 0.15→0.27→0.46→0.52）。
2021 年 margin 仅 4.1 bp（其他年 9.9~21.7 bp）⇒ 该年**机制性疲软**，与分析师修正信号在 2017 年 S=0.22 同型；
在保持 S ≥ 1.58 的前提下，2021 年 S 的上限经系统验证为 **0.52**（需 0.644 才能过 max/min ≤ 5）。

### 相关性（提交前实时取，`refresh=True`）
| 项 | 值 | 阈值 | 判定 |
|---|---|---|---|
| production（prod） | **0.6292** | 0.70 | PASS |
| self | **0.0323** | 0.70 | PASS |
| `all_passed` | **true** | — | PASS |

（self 低值可信度依据：`institutions1` 本账户从未提交过 ⇒ 无「近期提交孪生体」盲区。）
