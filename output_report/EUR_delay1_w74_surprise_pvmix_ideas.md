# EUR D1 surprise × unused PV ideas (Wave74 — agent S1)

Wave73 rec-change / smest levels FAIL. Surprise `ak7d0ZKR` S1.04 F0.40 TVR2.1% **2Y=0.95** (not a year-regime accident like RelVal 0.02). RN 0.38 / SUB 0.52. Cheap gate not passed; salvage as slow leg.

Win recipe: 0.40 slow + 0.60 fast PV, SUBINDUSTRY decay4.
Forbidden PV: v_rev, falling_wedge, breakaway, rising_wedge, symmetrical triangle, continuation.
OS ACTIVE=3. No 0.30/0.40/0.30 three-leg.

## Slow
`rank(ts_mean(surprise_pct_last_year_earnings_3, 22))` and naked `rank(surprise_pct_last_year_earnings_3)`

## Fast PV
1. common gap up — `common_gap_up_mean_simscore_lookback120`
2. common gap down — `common_gap_down_mean_simscore_lookback120`
3. desc triangle dynamic — `dynamic_similarity_desc_triangle`
4. downward price gap — `avg_similarity_downward_price_gap_pattern`
5. desc triangle upward mean — `mean_similarity_desc_triangle_upward`
6. desc triangle mean 60 — `desc_triangle_mean_simscore_lookback60`
7. two unused PV 0.5/0.5 (common_gap_up + desc_triangle)
