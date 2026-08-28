**Dataset**: multi_horizon_alpha  
**Region**: USA  
**Delay**: 1  
**Universe**: TOP3000

**Concept**: Recency of peak conviction on long_term_alert_rank_2 (ts_arg_max, 20d)
- **Mechanism**: Generic Path-1 diversity concept for dry-run extensibility validation on dataset multi_horizon_alpha. The operator topology (ts_arg_max/ts_arg_min timing features plus level/difference probes) is what matters here, not signal semantics.
- **Fields**: `long_term_alert_rank_2`, `long_term_alert_rank_3`
- **Implementation Example**: `quantile(-ts_arg_max(ts_backfill({long_term_alert_rank_2}, 66), 20))`
- **Direction**: High → long.
- **Why not crowded**: ts_arg timing features are outside the saturated level/revision probe family.

**Concept**: Recency of trough conviction on long_term_alert_rank_2 (ts_arg_min, 20d)
- **Mechanism**: Generic Path-1 diversity concept for dry-run extensibility validation on dataset multi_horizon_alpha. The operator topology (ts_arg_max/ts_arg_min timing features plus level/difference probes) is what matters here, not signal semantics.
- **Fields**: `long_term_alert_rank_2`, `long_term_alert_rank_3`
- **Implementation Example**: `quantile(ts_arg_min(ts_backfill({long_term_alert_rank_2}, 66), 20))`
- **Direction**: High → long.
- **Why not crowded**: ts_arg timing features are outside the saturated level/revision probe family.

**Concept**: Revision of long_term_alert_rank_2 (5-day change)
- **Mechanism**: Generic Path-1 diversity concept for dry-run extensibility validation on dataset multi_horizon_alpha. The operator topology (ts_arg_max/ts_arg_min timing features plus level/difference probes) is what matters here, not signal semantics.
- **Fields**: `long_term_alert_rank_2`, `long_term_alert_rank_3`
- **Implementation Example**: `quantile(ts_delta(ts_backfill({long_term_alert_rank_2}, 66), 5))`
- **Direction**: High → long.
- **Why not crowded**: ts_arg timing features are outside the saturated level/revision probe family.

**Concept**: Recency of peak signal on long_term_alert_rank_3 (ts_arg_max, 10d)
- **Mechanism**: Generic Path-1 diversity concept for dry-run extensibility validation on dataset multi_horizon_alpha. The operator topology (ts_arg_max/ts_arg_min timing features plus level/difference probes) is what matters here, not signal semantics.
- **Fields**: `long_term_alert_rank_2`, `long_term_alert_rank_3`
- **Implementation Example**: `quantile(-ts_arg_max(ts_backfill({long_term_alert_rank_3}, 66), 10))`
- **Direction**: High → long.
- **Why not crowded**: ts_arg timing features are outside the saturated level/revision probe family.

**Concept**: Recency of trough signal on long_term_alert_rank_3 (ts_arg_min, 10d)
- **Mechanism**: Generic Path-1 diversity concept for dry-run extensibility validation on dataset multi_horizon_alpha. The operator topology (ts_arg_max/ts_arg_min timing features plus level/difference probes) is what matters here, not signal semantics.
- **Fields**: `long_term_alert_rank_2`, `long_term_alert_rank_3`
- **Implementation Example**: `quantile(ts_arg_min(ts_backfill({long_term_alert_rank_3}, 66), 10))`
- **Direction**: High → long.
- **Why not crowded**: ts_arg timing features are outside the saturated level/revision probe family.

**Concept**: Cross spread long_term_alert_rank_2 minus long_term_alert_rank_3
- **Mechanism**: Generic Path-1 diversity concept for dry-run extensibility validation on dataset multi_horizon_alpha. The operator topology (ts_arg_max/ts_arg_min timing features plus level/difference probes) is what matters here, not signal semantics.
- **Fields**: `long_term_alert_rank_2`, `long_term_alert_rank_3`
- **Implementation Example**: `quantile(subtract(ts_backfill({long_term_alert_rank_2}, 66), ts_backfill({long_term_alert_rank_3}, 66)))`
- **Direction**: High → long.
- **Why not crowded**: ts_arg timing features are outside the saturated level/revision probe family.

**Concept**: Level rank of long_term_alert_rank_3
- **Mechanism**: Generic Path-1 diversity concept for dry-run extensibility validation on dataset multi_horizon_alpha. The operator topology (ts_arg_max/ts_arg_min timing features plus level/difference probes) is what matters here, not signal semantics.
- **Fields**: `long_term_alert_rank_2`, `long_term_alert_rank_3`
- **Implementation Example**: `quantile(rank(ts_backfill({long_term_alert_rank_3}, 66)))`
- **Direction**: High → long.
- **Why not crowded**: ts_arg timing features are outside the saturated level/revision probe family.
