**Dataset**: analyst_consensus  
**Region**: USA  
**Delay**: 1  
**Universe**: TOP3000

**Concept**: Recency of peak conviction on estimate_count_current_period_eps_annual12_3 (ts_arg_max, 20d)
- **Mechanism**: Generic Path-1 diversity concept for dry-run extensibility validation on dataset analyst_consensus. The operator topology (ts_arg_max/ts_arg_min timing features plus level/difference probes) is what matters here, not signal semantics.
- **Fields**: `estimate_count_current_period_eps_annual12_3`, `estimate_count_flash_period_eps_annual12_3`
- **Implementation Example**: `quantile(-ts_arg_max(ts_backfill(vec_avg({estimate_count_current_period_eps_annual12_3}), 66), 20))`
- **Direction**: High → long.
- **Why not crowded**: ts_arg timing features are outside the saturated level/revision probe family.

**Concept**: Recency of trough conviction on estimate_count_current_period_eps_annual12_3 (ts_arg_min, 20d)
- **Mechanism**: Generic Path-1 diversity concept for dry-run extensibility validation on dataset analyst_consensus. The operator topology (ts_arg_max/ts_arg_min timing features plus level/difference probes) is what matters here, not signal semantics.
- **Fields**: `estimate_count_current_period_eps_annual12_3`, `estimate_count_flash_period_eps_annual12_3`
- **Implementation Example**: `quantile(ts_arg_min(ts_backfill(vec_avg({estimate_count_current_period_eps_annual12_3}), 66), 20))`
- **Direction**: High → long.
- **Why not crowded**: ts_arg timing features are outside the saturated level/revision probe family.

**Concept**: Revision of estimate_count_current_period_eps_annual12_3 (5-day change)
- **Mechanism**: Generic Path-1 diversity concept for dry-run extensibility validation on dataset analyst_consensus. The operator topology (ts_arg_max/ts_arg_min timing features plus level/difference probes) is what matters here, not signal semantics.
- **Fields**: `estimate_count_current_period_eps_annual12_3`, `estimate_count_flash_period_eps_annual12_3`
- **Implementation Example**: `quantile(ts_delta(ts_backfill(vec_avg({estimate_count_current_period_eps_annual12_3}), 66), 5))`
- **Direction**: High → long.
- **Why not crowded**: ts_arg timing features are outside the saturated level/revision probe family.

**Concept**: Recency of peak signal on estimate_count_flash_period_eps_annual12_3 (ts_arg_max, 10d)
- **Mechanism**: Generic Path-1 diversity concept for dry-run extensibility validation on dataset analyst_consensus. The operator topology (ts_arg_max/ts_arg_min timing features plus level/difference probes) is what matters here, not signal semantics.
- **Fields**: `estimate_count_current_period_eps_annual12_3`, `estimate_count_flash_period_eps_annual12_3`
- **Implementation Example**: `quantile(-ts_arg_max(ts_backfill(vec_avg({estimate_count_flash_period_eps_annual12_3}), 66), 10))`
- **Direction**: High → long.
- **Why not crowded**: ts_arg timing features are outside the saturated level/revision probe family.

**Concept**: Recency of trough signal on estimate_count_flash_period_eps_annual12_3 (ts_arg_min, 10d)
- **Mechanism**: Generic Path-1 diversity concept for dry-run extensibility validation on dataset analyst_consensus. The operator topology (ts_arg_max/ts_arg_min timing features plus level/difference probes) is what matters here, not signal semantics.
- **Fields**: `estimate_count_current_period_eps_annual12_3`, `estimate_count_flash_period_eps_annual12_3`
- **Implementation Example**: `quantile(ts_arg_min(ts_backfill(vec_avg({estimate_count_flash_period_eps_annual12_3}), 66), 10))`
- **Direction**: High → long.
- **Why not crowded**: ts_arg timing features are outside the saturated level/revision probe family.

**Concept**: Cross spread estimate_count_current_period_eps_annual12_3 minus estimate_count_flash_period_eps_annual12_3
- **Mechanism**: Generic Path-1 diversity concept for dry-run extensibility validation on dataset analyst_consensus. The operator topology (ts_arg_max/ts_arg_min timing features plus level/difference probes) is what matters here, not signal semantics.
- **Fields**: `estimate_count_current_period_eps_annual12_3`, `estimate_count_flash_period_eps_annual12_3`
- **Implementation Example**: `quantile(subtract(ts_backfill(vec_avg({estimate_count_current_period_eps_annual12_3}), 66), ts_backfill(vec_avg({estimate_count_flash_period_eps_annual12_3}), 66)))`
- **Direction**: High → long.
- **Why not crowded**: ts_arg timing features are outside the saturated level/revision probe family.

**Concept**: Level rank of estimate_count_flash_period_eps_annual12_3
- **Mechanism**: Generic Path-1 diversity concept for dry-run extensibility validation on dataset analyst_consensus. The operator topology (ts_arg_max/ts_arg_min timing features plus level/difference probes) is what matters here, not signal semantics.
- **Fields**: `estimate_count_current_period_eps_annual12_3`, `estimate_count_flash_period_eps_annual12_3`
- **Implementation Example**: `quantile(rank(ts_backfill(vec_avg({estimate_count_flash_period_eps_annual12_3}), 66)))`
- **Direction**: High → long.
- **Why not crowded**: ts_arg timing features are outside the saturated level/revision probe family.
