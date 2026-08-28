**Dataset**: option_horizon_decomp  
**Region**: USA  
**Delay**: 1  
**Universe**: TOP3000

**Concept**: Recency of peak conviction on put_call_open_interest_ratio_1080d_long_term_2 (ts_arg_max, 20d)
- **Mechanism**: Generic Path-1 diversity concept for dry-run extensibility validation on dataset option_horizon_decomp. The operator topology (ts_arg_max/ts_arg_min timing features plus level/difference probes) is what matters here, not signal semantics.
- **Fields**: `put_call_open_interest_ratio_1080d_long_term_2`, `put_call_open_interest_ratio_1080d_medium_term_2`
- **Implementation Example**: `quantile(-ts_arg_max(ts_backfill({put_call_open_interest_ratio_1080d_long_term_2}, 66), 20))`
- **Direction**: High → long.
- **Why not crowded**: ts_arg timing features are outside the saturated level/revision probe family.

**Concept**: Recency of trough conviction on put_call_open_interest_ratio_1080d_long_term_2 (ts_arg_min, 20d)
- **Mechanism**: Generic Path-1 diversity concept for dry-run extensibility validation on dataset option_horizon_decomp. The operator topology (ts_arg_max/ts_arg_min timing features plus level/difference probes) is what matters here, not signal semantics.
- **Fields**: `put_call_open_interest_ratio_1080d_long_term_2`, `put_call_open_interest_ratio_1080d_medium_term_2`
- **Implementation Example**: `quantile(ts_arg_min(ts_backfill({put_call_open_interest_ratio_1080d_long_term_2}, 66), 20))`
- **Direction**: High → long.
- **Why not crowded**: ts_arg timing features are outside the saturated level/revision probe family.

**Concept**: Revision of put_call_open_interest_ratio_1080d_long_term_2 (5-day change)
- **Mechanism**: Generic Path-1 diversity concept for dry-run extensibility validation on dataset option_horizon_decomp. The operator topology (ts_arg_max/ts_arg_min timing features plus level/difference probes) is what matters here, not signal semantics.
- **Fields**: `put_call_open_interest_ratio_1080d_long_term_2`, `put_call_open_interest_ratio_1080d_medium_term_2`
- **Implementation Example**: `quantile(ts_delta(ts_backfill({put_call_open_interest_ratio_1080d_long_term_2}, 66), 5))`
- **Direction**: High → long.
- **Why not crowded**: ts_arg timing features are outside the saturated level/revision probe family.

**Concept**: Recency of peak signal on put_call_open_interest_ratio_1080d_medium_term_2 (ts_arg_max, 10d)
- **Mechanism**: Generic Path-1 diversity concept for dry-run extensibility validation on dataset option_horizon_decomp. The operator topology (ts_arg_max/ts_arg_min timing features plus level/difference probes) is what matters here, not signal semantics.
- **Fields**: `put_call_open_interest_ratio_1080d_long_term_2`, `put_call_open_interest_ratio_1080d_medium_term_2`
- **Implementation Example**: `quantile(-ts_arg_max(ts_backfill({put_call_open_interest_ratio_1080d_medium_term_2}, 66), 10))`
- **Direction**: High → long.
- **Why not crowded**: ts_arg timing features are outside the saturated level/revision probe family.

**Concept**: Recency of trough signal on put_call_open_interest_ratio_1080d_medium_term_2 (ts_arg_min, 10d)
- **Mechanism**: Generic Path-1 diversity concept for dry-run extensibility validation on dataset option_horizon_decomp. The operator topology (ts_arg_max/ts_arg_min timing features plus level/difference probes) is what matters here, not signal semantics.
- **Fields**: `put_call_open_interest_ratio_1080d_long_term_2`, `put_call_open_interest_ratio_1080d_medium_term_2`
- **Implementation Example**: `quantile(ts_arg_min(ts_backfill({put_call_open_interest_ratio_1080d_medium_term_2}, 66), 10))`
- **Direction**: High → long.
- **Why not crowded**: ts_arg timing features are outside the saturated level/revision probe family.

**Concept**: Cross spread put_call_open_interest_ratio_1080d_long_term_2 minus put_call_open_interest_ratio_1080d_medium_term_2
- **Mechanism**: Generic Path-1 diversity concept for dry-run extensibility validation on dataset option_horizon_decomp. The operator topology (ts_arg_max/ts_arg_min timing features plus level/difference probes) is what matters here, not signal semantics.
- **Fields**: `put_call_open_interest_ratio_1080d_long_term_2`, `put_call_open_interest_ratio_1080d_medium_term_2`
- **Implementation Example**: `quantile(subtract(ts_backfill({put_call_open_interest_ratio_1080d_long_term_2}, 66), ts_backfill({put_call_open_interest_ratio_1080d_medium_term_2}, 66)))`
- **Direction**: High → long.
- **Why not crowded**: ts_arg timing features are outside the saturated level/revision probe family.

**Concept**: Level rank of put_call_open_interest_ratio_1080d_medium_term_2
- **Mechanism**: Generic Path-1 diversity concept for dry-run extensibility validation on dataset option_horizon_decomp. The operator topology (ts_arg_max/ts_arg_min timing features plus level/difference probes) is what matters here, not signal semantics.
- **Fields**: `put_call_open_interest_ratio_1080d_long_term_2`, `put_call_open_interest_ratio_1080d_medium_term_2`
- **Implementation Example**: `quantile(rank(ts_backfill({put_call_open_interest_ratio_1080d_medium_term_2}, 66)))`
- **Direction**: High → long.
- **Why not crowded**: ts_arg timing features are outside the saturated level/revision probe family.
