# Robustness audit — 78jdv6b1 (2026-08-24)

Decision: **CONDITIONAL / platform READY**. Failed RA = 0. Submit-layer GET `/alphas/78jdv6b1/submit` exited **SUBMITTABLE**. Do not auto-submit.

## Candidate
- id: `78jdv6b1`
- expr: `0.30` invert capacq industry residual + `0.40` invert `avg_similarity_v_reversal_bottom` + `0.30` invert `avg_similarity_falling_wedge_pattern`
- settings: EUR TOP2500 D1 SUBINDUSTRY decay4 truncation 0.08 maxTrade ON
- pyramids: EUR/D1/PV + EUR/D1/MODEL

## Phase A (forum)
Search `IS_LADDER_SHARPE yearly stats overfitting` returned 15 posts; follow-up `过拟合 overfitting yearly sharpe` and `prod correlation 0.7 self correlation submit` returned 50+50. High-vote anchors: JX79797 (98) yearly CV scoring; FZ60707 (41) factory-shape years; XC66172 (16) rank_by_side for ladder; 隐性过拟合 (16); 降 Prod Correlation 实践 (15); PPAC/prod 报错帖 (91). Recent-3yr regime from skill (2026-06-20) used as primary year gate. 论坛语料 ≥30。

## Phase B
| Metric | Value |
|---|---|
| Sharpe / Fitness / TVR / Margin | 1.74 / 1.11 / 5.47% / 18.7 bp |
| SUB / 2Y ladder / RN | 1.13 / **2.05 PASS** / 1.06 |
| prod / self vs Wj71Q12o | **0.6945** / **-0.008** |
| Failed RA / PPA | **0 / 0** |
| Book after (performance_comparison) | Sharpe 1.81→2.35, Fitness 1.15→1.50 (positive marginal) |

Yearly Sharpe: 2014 2.86, 2015 3.00, 2016 1.31, **2017 -1.68**, 2018 0.70, 2019 3.10, 2020 2.40, 2021 1.73, 2022 0.79, 2023 3.16.

Recent-3yr (2021–23): all positive; mean 1.89; pop CV ≈ 0.52 (CONDITIONAL); max/min 3.16/0.79 = 4.00 (CONDITIONAL); decay 3.16/1.74 = 1.82 PASS; 0 flat years PASS.

2017 hole is full-history soft-flag only (not REJECT).

## Phase C
- Failed count: PASS
- Recent-3yr strength: PASS (2Y 2.05, last 3 yrs > 0)
- Recent-3yr CV: CONDITIONAL
- Decay: PASS
- max/min: CONDITIONAL
- Margin: PASS
- Operators (add/subtract/rank/ts_backfill/group_mean): 5 PASS
- Interpretability: PASS (slow over-investment residual vs fast chart mean-reversion)

## Judge
- Regular (Power Pool theme = GLB Liquid TOPDIV3000, EUR mismatch → not PPA)
- MATCHES_THEMES warning expected; not a RA blocker
- Quota: daily_remaining 4, rolling remaining 2
- Sibling `YP7AEMKq` (0.28/0.42/0.30) also RA=0 prod 0.6963 — same family, do not submit both
- Verdict: **READY** for user confirm. Soft flags: 2022 softness, 2017 old-year hole.
