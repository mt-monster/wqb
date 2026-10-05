# PPA 候选交接单（USA / D1 / FUNDAMENTAL）— 2026-10-02

> **agent 到此停下并交接**：PPA 只能由用户在平台 **web UI** 提交（MCP 通道会被拦）。
> 提交后运行 `python tools/ppa_handoff.py record --alpha-id <ID>` 回写台账。

## 当期主题匹配证据

平台 2026-10-01 公告「**D1 Power Pool Oct'26**」（28 Sep – 11 Oct'26）：
> Power Pool Alpha must be **Delay 1**, **single data category**, and use **either price-volume or fundamental** data category.

| 主题要求 | 本批候选 | 匹配 |
|---|---|---|
| Delay 1 | D1 | ✅ |
| 单数据类别 | FUNDAMENTAL | ✅ |
| PV 或 FUNDAMENTAL | FUNDAMENTAL | ✅ |

## 三支候选（均 UNSUBMITTED，PPA 条件全过）

| # | alpha_id | 数据集 · 字段 | Sharpe | 2Y | SUB | **PPAC** | 算子 | 字段 |
|---|---|---|---|---|---|---|---|---|
| 1 | **`2rmEZlKx`** | fundamental110 · `fnd110_value_fast_d1` | **1.29** | 2.00 | 0.74 | **0.4884** | 5 | 1 |
| 2 | **`mL6Ozm72`** | fundamental110 · `fnd110_original_value_fast_d1` | **1.29** | 1.95 | 0.75 | **0.4885** | 5 | 1 |
| 3 | **`zqbaoRwR`** | fundamental3 · `fnd3_qacctadj_longdebt_fast_d1` | **1.27** | 1.30 | 0.89 | **0.4568** | 4 | 1 |

**表达式**
```
1. ts_decay_linear(group_rank(ts_zscore(ts_backfill(vec_avg(fnd110_value_fast_d1), 252), 252), subindustry), 200)
2. ts_decay_linear(group_rank(ts_zscore(ts_backfill(vec_avg(fnd110_original_value_fast_d1), 252), 252), subindustry), 200)
3. ts_decay_linear(group_rank(ts_zscore(ts_backfill(fnd3_qacctadj_longdebt_fast_d1, 252), 252), subindustry), 200)
```
**设置**：USA / TOP3000 / D1 / decay 66 / SUBINDUSTRY / truncation 0.08

## PPA 条件逐项核对（自动部分）

| 条件 | 门槛 | 候选值 | 判定 |
|---|---|---|---|
| Sharpe | ≥ 1.0 | 1.29 / 1.29 / 1.27 | ✅ |
| 算子数 | ≤ 8 | 5 / 5 / 4 | ✅ |
| 字段数 | ≤ 3 | 1 | ✅ |
| **PPAC** | **< 0.5** | **0.4884 / 0.4885 / 0.4568** | ✅ |
| Failed PPA | == 0 | 0 / 0 / 0 | ✅ |
| Delay / 类别 | D1 + FUNDAMENTAL | 匹配 | ✅ |

## ★ 收益路径（为什么 PPA 是突破口）

- **PPAC 的对比池只有 3 颗**（`ppac_ids_cached=3`），远小于 prod 的 133 颗 OS 池
  ⇒ 同样拥挤的概念，**PPAC 比 prod 好过得多**（analyst 冠军 prod=0.90 但 PPAC 仅 0.64；本批更是 0.46–0.49）。
- **Sharpe 门槛 1.0**（而非 1.58）⇒ 不需要把信号推到极限。
- **塔归属**：三支都落在 **USA/D1/FUNDAMENTAL**（`MATCHES_PYRAMID` PASS，multiplier 1.1）—— **该塔当前只有 1 颗提交，本批可把它推到 2–4 颗。**

## 用户需人工确认的最后一步

1. 平台右上角铃铛 → 确认 **PPA 主题窗口仍活跃**，且 `MATCHES_THEMES` 显示收到（非活跃区会报 "does not match any Power Pool Theme"）。
2. 在 alpha 详情页点 **Submit to Power Pool**（或 Power Pool 提交入口）。
3. 提交成功后跑 `python tools/ppa_handoff.py record --alpha-id <ID>` 回写。

**注意**：PPAC 为**本地估算**（池仅 3 颗），平台实测可能不同 —— 提交响应会给出真实值；若平台 PPAC ≥ 0.5 则该颗被拒，换下一颗。

## 附：候选来源扫描

`tracking/USA/candidates/exprs_usa_ppa_pvfund.json`（42 条，覆盖 PV 30 集 + FUNDAMENTAL 24 集，**此前覆盖率 0%**）。
- FUNDAMENTAL 段最强：fundamental110 (S 1.29) / fundamental3 (1.27) / fundamental23 (0.93) / fundamental21 (0.91, 2Y 1.68)
- PV 段整体弱（max S 0.47）：水平骨架不适用于 PV 的流量/事件类字段，需改 `ts_delta`/`rank`/门控结构。
