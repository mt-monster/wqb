**Dataset**: other635  
**Region**: USA  
**Delay**: 1  
**Universe**: TOP3000

**Concept**: Recency of peak conviction on oth635_char_count (ts_arg_max, 20d)
- **Mechanism**: Generic Path-1 diversity concept for dry-run extensibility validation on dataset other635. The operator topology (ts_arg_max/ts_arg_min timing features plus level/difference probes) is what matters here, not signal semantics.
- **Fields**: `oth635_char_count`, `oth635_sentiment`
- **Implementation Example**: `quantile(-ts_arg_max(ts_backfill(vec_avg({oth635_char_count}), 66), 20))`
- **Direction**: High → long.
- **Why not crowded**: ts_arg timing features are outside the saturated level/revision probe family.

**Concept**: Recency of trough conviction on oth635_char_count (ts_arg_min, 20d)
- **Mechanism**: Generic Path-1 diversity concept for dry-run extensibility validation on dataset other635. The operator topology (ts_arg_max/ts_arg_min timing features plus level/difference probes) is what matters here, not signal semantics.
- **Fields**: `oth635_char_count`, `oth635_sentiment`
- **Implementation Example**: `quantile(ts_arg_min(ts_backfill(vec_avg({oth635_char_count}), 66), 20))`
- **Direction**: High → long.
- **Why not crowded**: ts_arg timing features are outside the saturated level/revision probe family.

**Concept**: Revision of oth635_char_count (5-day change)
- **Mechanism**: Generic Path-1 diversity concept for dry-run extensibility validation on dataset other635. The operator topology (ts_arg_max/ts_arg_min timing features plus level/difference probes) is what matters here, not signal semantics.
- **Fields**: `oth635_char_count`, `oth635_sentiment`
- **Implementation Example**: `quantile(ts_delta(ts_backfill(vec_avg({oth635_char_count}), 66), 5))`
- **Direction**: High → long.
- **Why not crowded**: ts_arg timing features are outside the saturated level/revision probe family.

**Concept**: Recency of peak signal on oth635_sentiment (ts_arg_max, 10d)
- **Mechanism**: Generic Path-1 diversity concept for dry-run extensibility validation on dataset other635. The operator topology (ts_arg_max/ts_arg_min timing features plus level/difference probes) is what matters here, not signal semantics.
- **Fields**: `oth635_char_count`, `oth635_sentiment`
- **Implementation Example**: `quantile(-ts_arg_max(ts_backfill(vec_avg({oth635_sentiment}), 66), 10))`
- **Direction**: High → long.
- **Why not crowded**: ts_arg timing features are outside the saturated level/revision probe family.

**Concept**: Recency of trough signal on oth635_sentiment (ts_arg_min, 10d)
- **Mechanism**: Generic Path-1 diversity concept for dry-run extensibility validation on dataset other635. The operator topology (ts_arg_max/ts_arg_min timing features plus level/difference probes) is what matters here, not signal semantics.
- **Fields**: `oth635_char_count`, `oth635_sentiment`
- **Implementation Example**: `quantile(ts_arg_min(ts_backfill(vec_avg({oth635_sentiment}), 66), 10))`
- **Direction**: High → long.
- **Why not crowded**: ts_arg timing features are outside the saturated level/revision probe family.

**Concept**: Cross spread oth635_char_count minus oth635_sentiment
- **Mechanism**: Generic Path-1 diversity concept for dry-run extensibility validation on dataset other635. The operator topology (ts_arg_max/ts_arg_min timing features plus level/difference probes) is what matters here, not signal semantics.
- **Fields**: `oth635_char_count`, `oth635_sentiment`
- **Implementation Example**: `quantile(subtract(ts_backfill(vec_avg({oth635_char_count}), 66), ts_backfill(vec_avg({oth635_sentiment}), 66)))`
- **Direction**: High → long.
- **Why not crowded**: ts_arg timing features are outside the saturated level/revision probe family.

**Concept**: Level rank of oth635_sentiment
- **Mechanism**: Generic Path-1 diversity concept for dry-run extensibility validation on dataset other635. The operator topology (ts_arg_max/ts_arg_min timing features plus level/difference probes) is what matters here, not signal semantics.
- **Fields**: `oth635_char_count`, `oth635_sentiment`
- **Implementation Example**: `quantile(rank(ts_backfill(vec_avg({oth635_sentiment}), 66)))`
- **Direction**: High → long.
- **Why not crowded**: ts_arg timing features are outside the saturated level/revision probe family.
