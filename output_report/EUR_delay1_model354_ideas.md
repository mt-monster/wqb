# EUR D1 model354 ideas (Wave66 — agent S1; GEM LLM 402)

Dataset: `model354` VECTOR valuation/consensus. NEWS 概念轨已尽（38/36/84/85）。
OS ACTIVE=3. No resid×PV. Skip sector_* duplicates, country/item, `pt1d1ntr` returns.

## Preprocess
- VECTOR: `vec_avg(field)` then `ts_backfill(..., 66)`
- Use `mdl354_group_*` only

## Concepts
1. FY2 forward earnings yield invert — `mdl354_group_pt12yf_dlyspe` (alphaCount 0)
2. NTM forward earnings yield invert — `mdl354_group_pt1mtn_dlyspe`
3. Trailing FCF yield invert — `mdl354_group_pt1dlyfcf`
4. Forward CFO yield — `mdl354_group_pt1cfoyld_fy1`
5. Trailing dividend yield invert — `mdl354_group_pt1divyld_trl`
6. Sales / EV invert — `mdl354_group_pt1sale_ev`
7. FY1 vs LTM earnings-yield disagreement — `mdl354_group_pt11yf_dlyspe` − `mdl354_group_pt1b_mtl_dlyspe`

Cheap-value invert is the economic default; each slot also includes non-invert / industry residual / window variants.
