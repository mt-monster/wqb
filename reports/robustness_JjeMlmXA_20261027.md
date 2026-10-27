# Robustness Audit — JjeMlmXA (GLB)

**Date:** 2026-10-27  
**Alpha ID:** `JjeMlmXA`  
**Verdict:** **PASS** (10/10 positive PnL, resilient, dual pyramid ×1.3, prod 0.6658)

## Expression
```
group_rank(
  subtract(
    group_zscore(ts_decay_linear(
      winsorize(ts_delta(ts_backfill(rel_val_region_rank_score_41, 22), 11), std=1),
      5
    ), industry),
    group_zscore(ts_decay_linear(corr_high_price_with_volume, 5), industry)
  ),
  industry
)
```

**Structure:** Cross-dataset blend — **Leg 1** `rel_val_region_rank_score_41` from `predictive_starmine` (same as gJeY2Qrm base), **Leg 2** `corr_high_price_with_volume` from `intraday_pv_feats` (same as 6Xdm3pXL base). Both `group_zscore(ts_decay_linear(x, 5), industry)`, then subtracted and `group_rank`ed on industry. Cross-dataset ⇒ no ATOM, but keeps both parents in the pool.

**Mechanism:** Value ranking minus microstructure efficiency. High-value stocks with poor microstructure → overweight.

## Settings (GLB authoritative)
| Param | Value |
|---|---|
| Region / Universe | GLB / MINVOL1M |
| Delay / Decay | 1 / 10 |
| Neutralization | STATISTICAL |
| Truncation / nanHandling / maxTrade | 0.08 / OFF / OFF |
| Period | 2014-01-01 → 2023-12-31 |

## Metrics
| Metric | Value | Gate | Result |
|---|---|---|---|
| Sharpe | 3.04 | ≥ 1.58 | ✅ |
| **Fitness** | **1.11** | ≥ 1.0 | ✅ |
| 2Y Sharpe | 3.00 | ≥ 1.58 | ✅ |
| IS Ladder | 2-window | — | ✅ (passes, cross-dataset) |
| Sub-Universe | 1.54 | ≥ 1.0 | ✅ |
| Turnover | 0.3193 | 0.01–0.7 | ✅ |
| Returns | 0.0425 | — | — |
| Drawdown | 0.0099 | — | — |
| Invest. Sharpe | 2.65 | — | ✅ |
| Invest. Fitness | 0.99 | — | ⚠️ (warning only) |

**RA:** `failed_ra_count=0`, `failed_ppa_count=0`  
**Pyramid:** GLB/D1/PV ×1.0 + GLB/D1/MODEL ×1.3 → **`effective=2`, effective mult=1.3**  
**Warning:** CLUSTER_TEST 1.16 < 1.58 (warning, non-blocking)

## 10-Year PnL Profile (2014–2023)

| Year | PnL ($) | Returns | Sharpe | Fitness |
|---|---|---|---|---|
| 2014 | 610,319 | 5.85% | 5.09 | 2.19 |
| 2015 | 510,221 | 4.89% | 4.23 | 1.67 |
| 2016 | 383,953 | 3.68% | 3.09 | 1.05 |
| 2017 | 207,240 | 1.99% | 2.09 | 0.51 |
| 2018 | 229,180 | 2.20% | 1.86 | 0.49 |
| 2019 | 477,747 | 4.58% | 3.56 | 1.35 |
| 2020 | 681,697 | 7.10% | 3.36 | 1.58 |
| 2021 | 282,112 | 2.70% | 1.87 | 0.55 |
| 2022 | 466,013 | 4.48% | 2.51 | 0.94 |
| 2023 | 547,533 | 5.26% | 3.75 | 1.50 |
| **Total** | **4,396,015** | — | — | — |

### Regime Resilience
| Regime | Year | PnL | Verdict |
|---|---|---|---|
| 2015 QE Exit | 2015 | 510,221 | ✅ resilient |
| 2016 UK / Vol spike | 2016 | 383,953 | ✅ |
| 2018 Q4 RV Collapse | 2018 | 229,180 | ✅ **resilient** |
| 2020 COVID Crash | 2020 | **681,697** | ✅ **strongest year** |
| 2022 Rate hikes | 2022 | 466,013 | ✅ |
| 2023 AI boom | 2023 | 547,533 | ✅ |

## Correlation
| Metric | Value | Limit | Verdict |
|---|---|---|---|
| Prod correlation | **0.6658** | < 0.70 | ✅ (0.034 headroom) |
| Self correlation | **0.6055** | < 0.70 | ✅ (top: 6Xdm3pXL 0.605, gJeY2Qrm 0.582) |

⚠ Self corr to both parents > 0.5 — cross-dataset blending shares the underlying signal but keeps prod under 0.70.

## Criteria Checklist
| Criterion | Threshold | Actual | Verdict |
|---|---|---|---|
| Positive years | ≥ 8/10 | 10/10 | ✅ |
| Negative PnL years | 0 | 0 | ✅ |
| Top-year share | < 25% | 15.5% | ✅ |
| 2018 PnL | > 0 | +229k | ✅ |
| 2020 PnL | > 0 | +682k | ✅ |
| IS Ladder | pass | pass | ✅ |
| Prod corr | < 0.70 | 0.6658 | ✅ |
| Self corr | < 0.70 | 0.6055 | ✅ |

## Verdict
**PASS — JjeMlmXA is robust and deliverable.** All structural robustness checks pass. Prod/self under 0.70 with headroom.

**Comparison to parents:**
| Metric | gJeY2Qrm | 6Xdm3pXL | JjeMlmXA (blend) |
|---|---|---|---|
| Dataset | predictive_starmine | intraday_pv_feats | **cross** |
| Fields | 3 (rel_val) | 3 (microstructure) | **2 (1+1)** |
| Sharpe | 2.34 | 3.66 | **3.04** |
| Fitness | 1.00 | 1.11 | **1.11** |
| 2Y Sharpe | 1.77 | 2.92 | **3.00** |
| Sub-Universe | 1.71 | 2.25 | 1.54 |
| Turnover | 0.168 | 0.564 | 0.319 |
| Pyramid effective | 1 (MODEL ×1.3) | 1 (PV ×1.0) | **2 (PV+MODEL ×1.3)** |
| Prod corr | 0.662 | pending | **0.6658** |
| Self corr | 0.172 | pending | 0.606 |
| Positive years | 10/10 | 10/10 | **10/10** |
| Top-year share | 16% | 14.3% | **15.5%** |
| 2018 PnL | +73k | +435k | **+229k** |
| 2020 PnL | +73k (approx) | +629k | **+682k** |
| Turnover profile | low | high | **mid** |

**JjeMlmXA is the best of both parents:** better 2Y than gJeY2Qrm, more diversified than 6Xdm3pXL, dual pyramid gives ×1.3 weight, mid-turnover. Only weakness is sub_universe_sharpe 1.54 (below 6Xdm3pXL's 2.25) — worth noting but not a blocker.
