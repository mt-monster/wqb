# WQB Session Brief — 2026-04-22

**Region:** USA
**Universe:** TOP3000
**Delay:** 1
**Budget:** 300 simulations
**Submission policy:** manual_review

## Neutralization Sweep

1. STATISTICAL
2. SUBINDUSTRY
3. INDUSTRY
4. FAST
5. SLOW
6. CROWDING
7. NONE
8. MARKET
9. SECTOR
10. REVERSION_AND_MOMENTUM
11. SLOW_AND_FAST

## Arms

| # | Category | Dataset | Universe | Paradigms | Budget |
|---|----------|---------|----------|-----------|--------|
| 1 | fundamental | fundamental6 | TOP3000 | P1_SPREAD, P2_RATIO, P3_MOMENTUM (+10) | 37 |
| 2 | fundamental | fundamental2 | TOP3000 | P1_SPREAD, P2_RATIO, P3_MOMENTUM (+10) | 37 |
| 3 | sentiment | sentiment22 | TOP3000 | P1_SPREAD, P2_RATIO, P3_MOMENTUM (+10) | 37 |
| 4 | sentiment | sentiment23 | TOP3000 | P1_SPREAD, P2_RATIO, P3_MOMENTUM (+10) | 37 |
| 5 | option | option3 | TOP3000 | P1_SPREAD, P2_RATIO, P3_MOMENTUM (+10) | 37 |
| 6 | option | option6 | TOP3000 | P1_SPREAD, P2_RATIO, P3_MOMENTUM (+10) | 37 |
| 7 | analyst | analyst4 | TOP3000 | P1_SPREAD, P2_RATIO, P3_MOMENTUM (+10) | 26 |
| 8 | analyst | analyst11 | TOP3000 | P1_SPREAD, P2_RATIO, P3_MOMENTUM (+10) | 26 |
| 9 | analyst | analyst14 | TOP3000 | P1_SPREAD, P2_RATIO, P3_MOMENTUM (+10) | 26 |

## Hard Rules

- Enforce single-dataset purity unless the strategy explicitly requires otherwise.
- Do not reuse an identical simulation payload without consulting the hash cache.
- Before `create_multi_simulation`, pass expressions through `wqb.expression.validator.check_batch`.
- Before `create_multi_simulation`, run `check_expr_against_inspect` on every expression against `tracking/field_inspect_<region>.json`. Reject any expression with `ok=False`; fix and re-validate before dispatching. See orchestrator step 19.
- Before `check_correlation` or `set_alpha_properties`, compute WebDataScope failed counts.
- REGULAR candidates require `Failed RA == 0`; PPA candidates require `Failed PPA == 0`.
- Run `wqb operator-audit` at session start to catch ghost operators.
- Update `batch-log` after every `create_multi_simulation` batch.
- For USA REGULAR mining, keep primary universe at `TOP3000`.
- Traverse the full region-supported neutralization order.
- Record every meaningful step to the event log and trajectory ledger.

## Dataset / Field Prior (from WebDataScope inspection)

> Populate this section by running `python tools/webdata_quality.py --zip WebData_*.zip --region <REG> --delay <N> --fields <ds1>,<ds2> --export-expr tracking/field_inspect_<region>.json --neut <best_neut>` in the research phase. Each arm should list its top fields with coverage/shape/preprocessing requirements.

| Arm | Dataset | Best Neut | Top Field | Coverage | Shape | Preprocessing Required |
|-----|---------|-----------|-----------|----------|-------|------------------------|
| 1 | fundamental6 | SUBINDUSTRY | _fill_ | _fill_ | _fill_ | _fill_ |
| 2 | fundamental2 | _check if degraded_ | | | | |
| 3 | sentiment22 | _fill_ | | | | |
| ... | ... | ... | | | | |

Inspection JSON path: `tracking/field_inspect_<region>.json` (consumed by `check_expr_against_inspect` in the batch sequence below).

## Batch Sequence

1. Authenticate and fetch operators.
2. Run operator audit; verify no ghost operators.
3. For each arm: fetch datafields, generate 4-expression batch.
4. Validate batch diversity via `check_batch`.
5. **Validate preprocessing alignment via `check_expr_against_inspect` against `tracking/field_inspect_<region>.json`**. Reject and fix any expression with `ok=False`.
6. Dispatch `create_multi_simulation`.
7. Check simulation cache for duplicates before re-simulating.
8. Record batch in `batch_log`.
9. For passing candidates: compute WebDataScope failed counts.
10. If failed count == 0: run `check_correlation`.
11. Hand off to robustness audit before submission.
