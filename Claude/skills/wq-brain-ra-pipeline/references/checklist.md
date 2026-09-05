# Orchestrator Checklist

- Enforce single-dataset purity unless the strategy explicitly requires otherwise.
- Do not reuse an identical simulation payload without consulting the hash cache.
- Do not spend all budget on one region or one setting family.
- Prefer regions or categories with lower recent submission density.
- Correlation checks should respect rate-limit state.
- Before `check_correlation` or `set_alpha_properties`, compute WebDataScope failed counts from `is.checks`.
- REGULAR candidates require `Failed RA == 0`; PPA candidates require `Failed PPA == 0`.
- Failed-count details live in `webdatascope-failed-gates.md`; report every counted check by name, limit, and value.
- Before `create_multi_simulation`, run `check_expr_against_inspect` on every expression against the field inspection JSON (`tracking/field_inspect_<region>.json`). Reject any expression with `ok=False`; fix and re-validate before dispatching. See orchestrator step 19.
