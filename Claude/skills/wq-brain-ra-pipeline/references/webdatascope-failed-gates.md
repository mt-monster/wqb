# WebDataScope Failed Gate Counts

Source: `WebDataScope-1.3.1/src/background/background.js` `getAlphaCheckStates(...)` (注入到 MAIN world 的 fetch 拦截器内，L270；2026-08-05 已核对 1.3.1 与 1.0.6 的 L268-358 逻辑一致)。

Use these counts as hard qualification gates for alpha mining:

- REGULAR alpha candidate: `Failed RA == 0`
- PPA candidate: `Failed PPA == 0`

Do not treat user-specified metric thresholds as substitutes for these gates. A candidate can have excellent Sharpe, Fitness, 2Y Sharpe, ProdCorr, and SelfCorr and still be invalid if the relevant failed-count is nonzero.

## Failed RA

Count checks whose `name` is in this set and whose `result` is neither `PASS` nor `PENDING`:

```text
HIGH_TURNOVER
LOW_TURNOVER
LOW_FITNESS
LOW_RETURNS
LOW_SHARPE
LOW_GLB_AMER_SHARPE
LOW_GLB_APAC_SHARPE
LOW_GLB_EMEA_SHARPE
LOW_ASI_JPN_SHARPE
IS_LADDER_SHARPE
LOW_2Y_SHARPE
LOW_SUB_UNIVERSE_SHARPE
LOW_ROBUST_UNIVERSE_SHARPE
LOW_AFTER_COST_ILLIQUID_UNIVERSE_SHARPE
LOW_INVESTABILITY_CONSTRAINED_SHARPE
LOW_ROBUST_UNIVERSE_RETURNS
CONCENTRATED_WEIGHT
```

## Failed PPA

Count checks whose `name` is in this set and whose `result` is neither `PASS` nor `PENDING`:

```text
LOW_TURNOVER
HIGH_TURNOVER
LOW_SUB_UNIVERSE_SHARPE
LOW_ROBUST_UNIVERSE_SHARPE
LOW_ROBUST_UNIVERSE_SHARPE.WITH_RATIO
LOW_ROBUST_UNIVERSE_RETURNS
LOW_INVESTABILITY_CONSTRAINED_SHARPE
```

Also count `LOW_SHARPE` as a Failed PPA item when `value < 1`, regardless of its displayed result state.

## Pseudocode

```python
PASS_STATES = {"PASS", "PENDING"}

failed_ra = sum(
    check["name"] in RA_CHECK_NAMES and check.get("result") not in PASS_STATES
    for check in is_checks
)

failed_ppa = sum(
    (
        check["name"] in PPA_CHECK_NAMES
        and check.get("result") not in PASS_STATES
    )
    or (
        check["name"] == "LOW_SHARPE"
        and check.get("value", 0) < 1
    )
    for check in is_checks
)
```

Report the names, limits, and values for every counted item. Do not call `set_alpha_properties` for a mining result unless the relevant failed count is zero.
