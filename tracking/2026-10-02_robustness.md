# Robustness 审计报告 — 2026-10-02

## d51A3nqY — USA/TOP2000/D1 · MODEL · ai_equity_alpha_pairdiff

**表达式**
```
ts_decay_linear(group_rank(ts_zscore(ts_backfill(subtract(vec_avg(business_model_clarity_score_2),
vec_avg(business_model_clarity_score_3)), 252), 252), industry), 5)
```
**设置**：USA / TOP2000 / D1 / decay 0 / STATISTICAL / trunc 0.08 / nanHandling ON
**stage**：IS（未提交）

### Phase B.0 — WebDataScope failed-count 门
| 项 | 值 | 判定 |
|---|---|---|
| failed_ra | 0 | PASS |
| failed_ppa | 0 | PASS |
| pending 名单内 | SELF_CORRELATION / DATA_DIVERSITY / PROD_CORRELATION / REGULAR_SUBMISSION / POWER_POOL_CORRELATION（提交层，非 failed） | 继续 |

### Phase B.1–B.5 — 归因

**顶层指标**：Sharpe **2.45** / Fitness **1.47** / Turnover 0.0948 / Returns 0.0451 / Drawdown 0.0227 / Margin 0.000951 / long 1025 / short 1054

**逐年（`get_alpha_yearly_stats`）**

| 年 | Sharpe | Returns | Drawdown | Fitness | Turnover |
|---|---|---|---|---|---|
| 2014 | 4.74 | 0.0758 | 0.0059 | 3.69 | 0.1015 |
| 2015 | 3.95 | 0.0618 | 0.0094 | 2.78 | 0.0893 |
| 2016 | 1.65 | 0.0273 | 0.0122 | 0.77 | 0.0868 |
| 2017 | 1.74 | 0.0283 | 0.0131 | 0.83 | 0.0871 |
| 2018 | 2.67 | 0.0437 | 0.0065 | 1.58 | 0.0919 |
| 2019 | 1.83 | 0.0298 | 0.0077 | 0.89 | 0.0933 |
| 2020 | 3.61 | 0.0775 | 0.0072 | 2.84 | 0.0968 |
| 2021 | 1.41 | 0.0314 | 0.0184 | 0.71 | 0.1026 |
| 2022 | 2.41 | 0.0539 | 0.0155 | 1.58 | 0.1012 |
| 2023 | 1.27 | 0.0238 | 0.0227 | 0.55 | 0.0980 |

### Phase C — 反过拟合闸（最近 3 IS 年 = 2021/2022/2023）

| 检查项 | 值 | 门限 | 判定 |
|---|---|---|---|
| WebDataScope failed | 0 | =0 | PASS |
| **Recent-3yr Sharpe（主判定）** | 1.41 / 2.41 / 1.27，全为正 | ≥ 用户 2Y 线 1.58（平台 2Y = **1.89**）且每年 >0.3 | **PASS** |
| Recent-3yr CV_Sharpe | **0.299** | < 0.40 | PASS |
| 衰减比 | **0.518**（1.27/2.45） | ≥ 0.50 | PASS（贴线） |
| 平年 | 0 | 0 | PASS |
| max/min Sharpe 比 | 1.90 | ≤ 3 | PASS |
| 全历史早年疲软 | 早年强（2014/15 = 4.74/3.95），无厂字形 | — | 软标记：无 |
| Sub-universe | 平台 LOW_SUB_UNIVERSE_SHARPE = **PASS**（1.58） | PASS | PASS |
| 算子数 | 6（ts_decay_linear / group_rank / ts_zscore / ts_backfill / subtract / vec_avg） | 软标记 >5 | 软标记 |
| Margin @ turnover | T≈9.5%（<60%），margin 正常 | ≥5bp | PASS |
| Top-5 集中度 | long~1025 / short~1054（千股级，极分散） | <30% | PASS |
| 经济可解释性 | 一句话：公司**业务模型清晰度评分**的多空认知差（score_2 − score_3），行业中性下捕捉市场对业务模式清晰度定价不足 | — | PASS |

### 相关性（本报告自含）
- prod = **0.4910**（<0.7 PASS，`check_correlation` 2026-10-02 实测）
- self = **−0.027**（<0.7 PASS）

### 判定
**PASS** — 全部硬闸通过。软标记：衰减比 0.518 贴线、2023 sharpe 1.27 为近年最低、CLUSTER_TEST WARNING(1.03<1.58)。

台账：`robustness_d51A3nqY`（region=USA）= PASS。

---
