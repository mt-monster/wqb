# EUR 变体轴归因矩阵（回溯）

生成：2026-10-26　｜　可归因集：32（max_s≥1.2）

## 赢家族 Top10

| 模板族 | 成为赢家次数 | 轴语义 |
|---|---|---|
| `pp` | 10 | 后处理电池（L4 截面） |
| `lvl_rk` | 5 | 水平量·截面秩 |
| `sw_u2500` | 2 | 其他 |
| `lvl_tr` | 2 | 水平量·时序秩 |
| `d1_va` | 1 | 其他 |
| `d2_rk` | 1 | 二阶差分·秩 |
| `dw` | 1 | 双窗（L3 时间结构） |
| `rep` | 1 | 语义代表值 |
| `pv_correlation_mix` | 1 | 其他 |
| `rel_val_rank_mix` | 1 | 其他 |

## 各轴平均差距（相对族内赢家）

| 轴 | 样本数 | 平均 ΔS |
|---|---|---|
| 后处理电池（L4 截面） | 23 | -0.068 |
| 水平量·截面秩 | 23 | -0.294 |
| 双窗（L3 时间结构） | 23 | -0.506 |
| 水平量·时序秩 | 20 | -0.546 |
| 水平量·分位 | 18 | -0.573 |
| 水平量·zscore | 18 | -0.581 |
| 水平量·scale | 18 | -0.608 |
| 变化量·秩 | 15 | -0.715 |
| 其他 | 83 | -0.755 |
| 一阶差分·秩 | 22 | -0.782 |
| 二阶差分·秩 | 17 | -1.045 |
| 语义代表值 | 8 | -1.094 |

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
| `fundamental17` | BORDERLINE | 1.43 | `lvl_tr` | 1.5 | 族内 lvl_tr 与 pp 并列（1.43 vs 1.41）⇒ 该字段对这两个轴同样敏感 |
| `quant_factor_lib` | INVALID_SAMPLE | 1.33 | `d2_rk` | 1.41 | 族内 d2_rk 与 pp 并列（1.33 vs 1.33）⇒ 该字段对这两个轴同样敏感 |
| `dl_riskfree_returns` | BORDERLINE | 1.69 | `pp` | 1.4 | 族内 pp 与 lvl_rk 并列（1.69 vs 1.65）⇒ 该字段对这两个轴同样敏感 |
| `techindi_model` | ALIVE | 1.91 | `pp` | 1.39 | 族内 pp 与 lvl_rk 并列（1.91 vs 1.9）⇒ 该字段对这两个轴同样敏感 |
| `risk68` | BORDERLINE | 1.39 | `sw_u2500` | 1.26 | 族内最优 sw_u2500（1.39），次优 pp（1.2），差 0.19 ⇒ 该字段主要吃「其他」 |
| `risk70` | DEAD | 1.24 | `pp` | 1.22 | 族内最优 pp（1.24），次优 sw_u2500（1.18），差 0.06 ⇒ 该字段主要吃「后处理电池（L4 截面）」 |
| `analyst45` | DEAD | 1.28 | `lvl_rk` | 1.19 | 族内 lvl_rk 与 lvl_qc 并列（1.28 vs 1.28）⇒ 该字段对这两个轴同样敏感 |
| `fundamental23` | BORDERLINE | 1.47 | `rep` | 1.12 | 族内 rep 与 lvl_qt 并列（1.47 vs 1.45）⇒ 该字段对这两个轴同样敏感 |
| `other553` | DEAD | 1.23 | `pp` | 1.09 | 族内 pp 与 lvl_tr 并列（1.23 vs 1.22）⇒ 该字段对这两个轴同样敏感 |
| `ai_equity_alpha` | ALIVE | 1.62 | `lvl_rk` | 0.94 | 族内 lvl_rk 与 pp 并列（1.62 vs 1.6）⇒ 该字段对这两个轴同样敏感 |
| `news_sentiment_nlp` | DEAD | 1.2 | `d1_va` | 0.87 | 族内最优 d1_va（1.2），次优 pp（1.15），差 0.05 ⇒ 该字段主要吃「其他」 |
| `pv37` | BORDERLINE | 1.33 | `lvl_tr` | 0.86 | 族内 lvl_tr 与 sw_u2500 并列（1.33 vs 1.3）⇒ 该字段对这两个轴同样敏感 |
| `sentiment26` | INVALID_SAMPLE | 1.54 | `pp` | 0.82 | 族内最优 pp（1.54），次优 sw_u2500（1.17），差 0.37 ⇒ 该字段主要吃「后处理电池（L4 截面）」 |
| `multi_source_model` | DEAD | 1.25 | `pp` | 0.8 | 族内最优 pp（1.25），次优 lvl_rk（1.18），差 0.07 ⇒ 该字段主要吃「后处理电池（L4 截面）」 |
| `earnings6` | DEAD | 1.2 | `lvl_rk` | 0.7 | 族内 lvl_rk 与 pp 并列（1.2 vs 1.19）⇒ 该字段对这两个轴同样敏感 |
| `global_seasonal_model` | DEAD | 1.22 | `pp` | 0.66 | 族内 pp 与 lvl_rk 并列（1.22 vs 1.2）⇒ 该字段对这两个轴同样敏感 |
| `sentiment27` | INVALID_SAMPLE | 1.31 | `pp` | 0.64 | 族内最优 pp（1.31），次优 d1_va（1.18），差 0.13 ⇒ 该字段主要吃「后处理电池（L4 截面）」 |
| `ind_risk_residual` | ALIVE | 3.35 | `resid_momentum_industry` | 0.6 | 族内最优 resid_momentum_industry（3.35），次优 resid_momentum_sector（2.75），差 0.60 ⇒ 该字段主要吃「其他」 |
| `predictive_starmine` | ALIVE | 2.34 | `rel_val_rank_mix` | 0.0 | 仅 1 个族，无法横向归因（轴效应不可分离） |
| `starmine_pv_hybrid` | ALIVE | 3.04 | `relval_micro_mix` | 0.0 | 仅 1 个族，无法横向归因（轴效应不可分离） |
| `risk_other_hybrid` | ALIVE | 3.23 | `risk_other_mix` | 0.0 | 仅 1 个族，无法横向归因（轴效应不可分离） |
| `other_model_hybrid` | ALIVE | 2.53 | `other_model_mix` | 0.0 | 仅 1 个族，无法横向归因（轴效应不可分离） |
| `eur_fund_pv_hybrid` | ALIVE | 1.87 | `signed_power_mix` | 0.0 | 仅 1 个族，无法横向归因（轴效应不可分离） |
| `institutions_other_hybrid` | ALIVE | 4.81 | `trade_when_inst_other` | 0.0 | 仅 1 个族，无法横向归因（轴效应不可分离） |
| `eur_inst_analyst_hybrid` | ALIVE | 2.12 | `inst_analyst_mix` | 0.0 | 仅 1 个族，无法横向归因（轴效应不可分离） |
