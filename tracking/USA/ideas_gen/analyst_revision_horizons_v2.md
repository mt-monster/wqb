**Dataset**: analyst_revision_horizons  
**Region**: USA  
**Delay**: 1  
**Universe**: TOP3000

**Concept**: Recency of peak conviction on analyst_count_decrease_estimate_quarter_short (ts_arg_max, 20d)
- **Mechanism**: Generic Path-1 diversity concept for dry-run extensibility validation on dataset analyst_revision_horizons. The operator topology (ts_arg_max/ts_arg_min timing features plus level/difference probes) is what matters here, not signal semantics.
- **Fields**: `analyst_count_decrease_estimate_quarter_short`, `analyst_count_decreasing_annual_ebitda_30d_short`
- **Implementation Example**: `quantile(-ts_arg_max(ts_backfill({analyst_count_decrease_estimate_quarter_short}, 66), 20))`
- **Direction**: High → long.
- **Why not crowded**: ts_arg timing features are outside the saturated level/revision probe family.

**Concept**: Recency of trough conviction on analyst_count_decrease_estimate_quarter_short (ts_arg_min, 20d)
- **Mechanism**: Generic Path-1 diversity concept for dry-run extensibility validation on dataset analyst_revision_horizons. The operator topology (ts_arg_max/ts_arg_min timing features plus level/difference probes) is what matters here, not signal semantics.
- **Fields**: `analyst_count_decrease_estimate_quarter_short`, `analyst_count_decreasing_annual_ebitda_30d_short`
- **Implementation Example**: `quantile(ts_arg_min(ts_backfill({analyst_count_decrease_estimate_quarter_short}, 66), 20))`
- **Direction**: High → long.
- **Why not crowded**: ts_arg timing features are outside the saturated level/revision probe family.

**Concept**: Revision of analyst_count_decrease_estimate_quarter_short (5-day change)
- **Mechanism**: Generic Path-1 diversity concept for dry-run extensibility validation on dataset analyst_revision_horizons. The operator topology (ts_arg_max/ts_arg_min timing features plus level/difference probes) is what matters here, not signal semantics.
- **Fields**: `analyst_count_decrease_estimate_quarter_short`, `analyst_count_decreasing_annual_ebitda_30d_short`
- **Implementation Example**: `quantile(ts_delta(ts_backfill({analyst_count_decrease_estimate_quarter_short}, 66), 5))`
- **Direction**: High → long.
- **Why not crowded**: ts_arg timing features are outside the saturated level/revision probe family.

**Concept**: Recency of peak signal on analyst_count_decreasing_annual_ebitda_30d_short (ts_arg_max, 10d)
- **Mechanism**: Generic Path-1 diversity concept for dry-run extensibility validation on dataset analyst_revision_horizons. The operator topology (ts_arg_max/ts_arg_min timing features plus level/difference probes) is what matters here, not signal semantics.
- **Fields**: `analyst_count_decrease_estimate_quarter_short`, `analyst_count_decreasing_annual_ebitda_30d_short`
- **Implementation Example**: `quantile(-ts_arg_max(ts_backfill({analyst_count_decreasing_annual_ebitda_30d_short}, 66), 10))`
- **Direction**: High → long.
- **Why not crowded**: ts_arg timing features are outside the saturated level/revision probe family.

**Concept**: Recency of trough signal on analyst_count_decreasing_annual_ebitda_30d_short (ts_arg_min, 10d)
- **Mechanism**: Generic Path-1 diversity concept for dry-run extensibility validation on dataset analyst_revision_horizons. The operator topology (ts_arg_max/ts_arg_min timing features plus level/difference probes) is what matters here, not signal semantics.
- **Fields**: `analyst_count_decrease_estimate_quarter_short`, `analyst_count_decreasing_annual_ebitda_30d_short`
- **Implementation Example**: `quantile(ts_arg_min(ts_backfill({analyst_count_decreasing_annual_ebitda_30d_short}, 66), 10))`
- **Direction**: High → long.
- **Why not crowded**: ts_arg timing features are outside the saturated level/revision probe family.

**Concept**: Cross spread analyst_count_decrease_estimate_quarter_short minus analyst_count_decreasing_annual_ebitda_30d_short
- **Mechanism**: Generic Path-1 diversity concept for dry-run extensibility validation on dataset analyst_revision_horizons. The operator topology (ts_arg_max/ts_arg_min timing features plus level/difference probes) is what matters here, not signal semantics.
- **Fields**: `analyst_count_decrease_estimate_quarter_short`, `analyst_count_decreasing_annual_ebitda_30d_short`
- **Implementation Example**: `quantile(subtract(ts_backfill({analyst_count_decrease_estimate_quarter_short}, 66), ts_backfill({analyst_count_decreasing_annual_ebitda_30d_short}, 66)))`
- **Direction**: High → long.
- **Why not crowded**: ts_arg timing features are outside the saturated level/revision probe family.

**Concept**: Level rank of analyst_count_decreasing_annual_ebitda_30d_short
- **Mechanism**: Generic Path-1 diversity concept for dry-run extensibility validation on dataset analyst_revision_horizons. The operator topology (ts_arg_max/ts_arg_min timing features plus level/difference probes) is what matters here, not signal semantics.
- **Fields**: `analyst_count_decrease_estimate_quarter_short`, `analyst_count_decreasing_annual_ebitda_30d_short`
- **Implementation Example**: `quantile(rank(ts_backfill({analyst_count_decreasing_annual_ebitda_30d_short}, 66)))`
- **Direction**: High → long.
- **Why not crowded**: ts_arg timing features are outside the saturated level/revision probe family.
