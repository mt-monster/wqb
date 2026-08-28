**Dataset**: predictive_starmine  
**Region**: USA  
**Delay**: 1  
**Universe**: TOP3000

**Concept**: Recency of peak conviction on analyst_downgrade_count_14d (ts_arg_max, 20d)
- **Mechanism**: Generic Path-1 diversity concept for dry-run extensibility validation on dataset predictive_starmine. The operator topology (ts_arg_max/ts_arg_min timing features plus level/difference probes) is what matters here, not signal semantics.
- **Fields**: `analyst_downgrade_count_14d`, `analyst_downgrade_count_14d_21`
- **Implementation Example**: `quantile(-ts_arg_max(ts_backfill({analyst_downgrade_count_14d}, 66), 20))`
- **Direction**: High → long.
- **Why not crowded**: ts_arg timing features are outside the saturated level/revision probe family.

**Concept**: Recency of trough conviction on analyst_downgrade_count_14d (ts_arg_min, 20d)
- **Mechanism**: Generic Path-1 diversity concept for dry-run extensibility validation on dataset predictive_starmine. The operator topology (ts_arg_max/ts_arg_min timing features plus level/difference probes) is what matters here, not signal semantics.
- **Fields**: `analyst_downgrade_count_14d`, `analyst_downgrade_count_14d_21`
- **Implementation Example**: `quantile(ts_arg_min(ts_backfill({analyst_downgrade_count_14d}, 66), 20))`
- **Direction**: High → long.
- **Why not crowded**: ts_arg timing features are outside the saturated level/revision probe family.

**Concept**: Revision of analyst_downgrade_count_14d (5-day change)
- **Mechanism**: Generic Path-1 diversity concept for dry-run extensibility validation on dataset predictive_starmine. The operator topology (ts_arg_max/ts_arg_min timing features plus level/difference probes) is what matters here, not signal semantics.
- **Fields**: `analyst_downgrade_count_14d`, `analyst_downgrade_count_14d_21`
- **Implementation Example**: `quantile(ts_delta(ts_backfill({analyst_downgrade_count_14d}, 66), 5))`
- **Direction**: High → long.
- **Why not crowded**: ts_arg timing features are outside the saturated level/revision probe family.

**Concept**: Recency of peak signal on analyst_downgrade_count_14d_21 (ts_arg_max, 10d)
- **Mechanism**: Generic Path-1 diversity concept for dry-run extensibility validation on dataset predictive_starmine. The operator topology (ts_arg_max/ts_arg_min timing features plus level/difference probes) is what matters here, not signal semantics.
- **Fields**: `analyst_downgrade_count_14d`, `analyst_downgrade_count_14d_21`
- **Implementation Example**: `quantile(-ts_arg_max(ts_backfill({analyst_downgrade_count_14d_21}, 66), 10))`
- **Direction**: High → long.
- **Why not crowded**: ts_arg timing features are outside the saturated level/revision probe family.

**Concept**: Recency of trough signal on analyst_downgrade_count_14d_21 (ts_arg_min, 10d)
- **Mechanism**: Generic Path-1 diversity concept for dry-run extensibility validation on dataset predictive_starmine. The operator topology (ts_arg_max/ts_arg_min timing features plus level/difference probes) is what matters here, not signal semantics.
- **Fields**: `analyst_downgrade_count_14d`, `analyst_downgrade_count_14d_21`
- **Implementation Example**: `quantile(ts_arg_min(ts_backfill({analyst_downgrade_count_14d_21}, 66), 10))`
- **Direction**: High → long.
- **Why not crowded**: ts_arg timing features are outside the saturated level/revision probe family.

**Concept**: Cross spread analyst_downgrade_count_14d minus analyst_downgrade_count_14d_21
- **Mechanism**: Generic Path-1 diversity concept for dry-run extensibility validation on dataset predictive_starmine. The operator topology (ts_arg_max/ts_arg_min timing features plus level/difference probes) is what matters here, not signal semantics.
- **Fields**: `analyst_downgrade_count_14d`, `analyst_downgrade_count_14d_21`
- **Implementation Example**: `quantile(subtract(ts_backfill({analyst_downgrade_count_14d}, 66), ts_backfill({analyst_downgrade_count_14d_21}, 66)))`
- **Direction**: High → long.
- **Why not crowded**: ts_arg timing features are outside the saturated level/revision probe family.

**Concept**: Level rank of analyst_downgrade_count_14d_21
- **Mechanism**: Generic Path-1 diversity concept for dry-run extensibility validation on dataset predictive_starmine. The operator topology (ts_arg_max/ts_arg_min timing features plus level/difference probes) is what matters here, not signal semantics.
- **Fields**: `analyst_downgrade_count_14d`, `analyst_downgrade_count_14d_21`
- **Implementation Example**: `quantile(rank(ts_backfill({analyst_downgrade_count_14d_21}, 66)))`
- **Direction**: High → long.
- **Why not crowded**: ts_arg timing features are outside the saturated level/revision probe family.
