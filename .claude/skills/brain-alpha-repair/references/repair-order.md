# Repair Order

1. Fix invalid structure.
2. Fix dataset purity or field lineage.
3. Fix turnover and coverage.
4. Re-check correlation and crowding.
5. Only then tune decay, truncation, or neutralization.
6. **体检硬门复验（2026-08-05 新增）** — 修复后必须通过 `check_expr_against_inspect(expr, field_inspect_result)` 校验（同 orchestrator step 19）。从 `tracking/field_inspect_<region>.json` 查出所用字段的体检结果；若 `ok=False`，按 violations 回到第 1-3 步继续修复（如"低覆盖未含 backfill"→ 回第 3 步补 `ts_backfill`），直到 `ok=True` 才允许进入 `create_multi_simulation`。5 条硬门：低覆盖(cr<0.4)须 `ts_backfill`/`group_backfill`；高偏度(|skew|>2)须 `rank`/`winsorize`/`signed_power`；厚尾(kurt>8)须 `rank`/`winsorize`；单边恒正/负须 `ts_delta`/`rank`/`bucket`；稀疏事件须 `trade_when`。
