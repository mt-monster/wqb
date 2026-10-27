# EUR 变体轴归因矩阵（回溯）

生成：2026-10-26　｜　可归因集：15（max_s≥1.5）

## 赢家族 Top10

| 模板族 | 成为赢家次数 | 轴语义 |
|---|---|---|
| `pp` | 5 | 后处理电池（L4 截面） |
| `lvl_rk` | 3 | 水平量·截面秩 |
| `dw` | 1 | 双窗（L3 时间结构） |
| `pv_correlation_mix` | 1 | 其他 |
| `sw_u2500` | 1 | 其他 |
| `rel_val_rank_mix` | 1 | 其他 |
| `relval_micro_mix` | 1 | 其他 |
| `risk_other_mix` | 1 | 其他 |
| `other_model_mix` | 1 | 其他 |

## 各轴平均差距（相对族内赢家）

| 轴 | 样本数 | 平均 ΔS |
|---|---|---|
| 后处理电池（L4 截面） | 10 | -0.068 |
| 水平量·截面秩 | 10 | -0.195 |
| 双窗（L3 时间结构） | 11 | -0.564 |
| 水平量·分位 | 6 | -0.898 |
| 水平量·scale | 6 | -0.903 |
| 水平量·zscore | 6 | -0.908 |
| 水平量·时序秩 | 7 | -0.913 |
| 变化量·秩 | 6 | -1.000 |
| 一阶差分·秩 | 10 | -1.041 |
| 其他 | 37 | -1.196 |
| 二阶差分·秩 | 8 | -1.412 |

## 逐集明细（按族间跨度降序，跨度大=该字段对轴敏感）

| 集 | verdict | maxS | 赢家族 | 跨度 | 归因结论 |
|---|---|---|---|---|---|
| `intraday_pv_feats` | ALIVE | 3.66 | `pv_correlation_mix` | 3.46 | 族内最优 pv_correlation_mix（3.66），次优 cs（1.32），差 2.34 ⇒ 该字段主要吃「其他」 |
| `other315` | INVALID_SAMPLE | 2.91 | `pp` | 2.58 | 族内最优 pp（2.91），次优 lvl_rk（1.96），差 0.95 ⇒ 该字段主要吃「后处理电池（L4 截面）」 |
| `model28` | BORDERLINE | 1.58 | `lvl_rk` | 2.19 | 族内 lvl_rk 与 pp 并列（1.58 vs 1.58）⇒ 该字段对这两个轴同样敏感 |
| `model31` | ALIVE | 1.86 | `lvl_rk` | 2.15 | 族内 lvl_rk 与 pp 并列（1.86 vs 1.86）⇒ 该字段对这两个轴同样敏感 |
| `model25` | ALIVE | 1.86 | `pp` | 1.98 | 族内 pp 与 lvl_rk 并列（1.86 vs 1.85）⇒ 该字段对这两个轴同样敏感 |
| `other401` | BORDERLINE | 1.55 | `dw` | 1.7 | 族内 dw 与 lvl_rk 并列（1.55 vs 1.53）⇒ 该字段对这两个轴同样敏感 |
| `other335` | BORDERLINE | 1.83 | `sw_u2500` | 1.59 | 族内最优 sw_u2500（1.83），次优 lvl_rk（1.59），差 0.24 ⇒ 该字段主要吃「其他」 |
| `dl_riskfree_returns` | BORDERLINE | 1.69 | `pp` | 1.4 | 族内 pp 与 lvl_rk 并列（1.69 vs 1.65）⇒ 该字段对这两个轴同样敏感 |
| `techindi_model` | ALIVE | 1.91 | `pp` | 1.39 | 族内 pp 与 lvl_rk 并列（1.91 vs 1.9）⇒ 该字段对这两个轴同样敏感 |
| `ai_equity_alpha` | ALIVE | 1.62 | `lvl_rk` | 0.94 | 族内 lvl_rk 与 pp 并列（1.62 vs 1.6）⇒ 该字段对这两个轴同样敏感 |
| `sentiment26` | INVALID_SAMPLE | 1.54 | `pp` | 0.82 | 族内最优 pp（1.54），次优 sw_u2500（1.17），差 0.37 ⇒ 该字段主要吃「后处理电池（L4 截面）」 |
| `predictive_starmine` | ALIVE | 2.34 | `rel_val_rank_mix` | 0.0 | 仅 1 个族，无法横向归因（轴效应不可分离） |
| `starmine_pv_hybrid` | ALIVE | 3.04 | `relval_micro_mix` | 0.0 | 仅 1 个族，无法横向归因（轴效应不可分离） |
| `risk_other_hybrid` | ALIVE | 3.23 | `risk_other_mix` | 0.0 | 仅 1 个族，无法横向归因（轴效应不可分离） |
| `other_model_hybrid` | ALIVE | 2.53 | `other_model_mix` | 0.0 | 仅 1 个族，无法横向归因（轴效应不可分离） |
