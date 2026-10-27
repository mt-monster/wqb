# Robustness Audit Report — 2026-10-26

## Alpha: `gJeY2Qrm` (GLB/MINVOL1M)

**Expression**:
```
group_zscore(ts_decay_linear(winsorize(ts_delta(ts_backfill(
  0.40*rel_val_region_rank_score_41
+ 0.35*rel_val_industry_rank_score_31
+ 0.25*rel_val_sector_rank_score_31, 22), 11), std=1), 5), industry)
```

**Dataset**: predictive_starmine (single-dataset, ATOM preserved, effective=1)
**Settings**: GLB / MINVOL1M / d1 / decay 12 / STATISTICAL / trunc 0.08 / nanHandling OFF / maxTrade OFF

## Phase B — Year-by-Year PnL Attribution

| Year | Sharpe | PnL ($) | Returns | Fitness |
|------|-------:|--------:|--------:|--------:|
| 2014 | 4.06 | 477,852 | 4.58% | 2.10 |
| 2015 | 2.93 | 357,665 | 3.43% | 1.32 |
| 2016 | 2.66 | 331,136 | 3.17% | 1.15 |
| 2017 | 0.50 | 55,376  | 0.53% | 0.09 |
| 2018 | 0.63 | 72,645  | 0.70% | 0.13 |
| 2019 | 3.30 | 424,584 | 4.07% | 1.62 |
| 2020 | 3.05 | 566,482 | 5.90% | 1.80 |
| 2021 | 2.66 | 373,011 | 3.57% | 1.23 |
| 2022 | 2.32 | 351,129 | 3.38% | 1.05 |
| 2023 | 1.08 | 131,523 | 1.26% | 0.30 |

**Totals**: PnL 3,142,407 | 10 years | Avg Sharpe 2.34

## Phase C — Verdict: PASS

- 10y full coverage, no late_start
- No negative-PnL years (base j2Y5xKN5 had -21k in 2018; gJeY2Qrm +73k in 2018 — the blend fixed the regime collapse)
- Top-year share 18% (below 25% fragility threshold)
- Recent 2-yr Sharpe avg 1.70 (above 1.0)
- Prod corr 0.662 (<0.70, 0.038 headroom)
- Sub 1.71 (>=1.0)
- RA 7/7 pass
- Pyramid effective=1 ATOM preserved

Auditor: SenseNova agent, 2026-10-26, per user explicit authorization.
