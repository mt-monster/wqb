**Dataset**: price_signal_dl  
**Region**: USA  
**Delay**: 1  
**Universe**: TOP3000

**Concept**: Recency of peak conviction on normalized_trend_indicator_3 (ts_arg_max, 20d)
- **Mechanism**: Generic Path-1 diversity concept for dry-run extensibility validation on dataset price_signal_dl. The operator topology (ts_arg_max/ts_arg_min timing features plus level/difference probes) is what matters here, not signal semantics.
- **Fields**: `normalized_trend_indicator_3`, `normalized_trend_indicator_4`
- **Implementation Example**: `quantile(-ts_arg_max(ts_backfill({normalized_trend_indicator_3}, 66), 20))`
- **Direction**: High → long.
- **Why not crowded**: ts_arg timing features are outside the saturated level/revision probe family.

**Concept**: Recency of trough conviction on normalized_trend_indicator_3 (ts_arg_min, 20d)
- **Mechanism**: Generic Path-1 diversity concept for dry-run extensibility validation on dataset price_signal_dl. The operator topology (ts_arg_max/ts_arg_min timing features plus level/difference probes) is what matters here, not signal semantics.
- **Fields**: `normalized_trend_indicator_3`, `normalized_trend_indicator_4`
- **Implementation Example**: `quantile(ts_arg_min(ts_backfill({normalized_trend_indicator_3}, 66), 20))`
- **Direction**: High → long.
- **Why not crowded**: ts_arg timing features are outside the saturated level/revision probe family.

**Concept**: Revision of normalized_trend_indicator_3 (5-day change)
- **Mechanism**: Generic Path-1 diversity concept for dry-run extensibility validation on dataset price_signal_dl. The operator topology (ts_arg_max/ts_arg_min timing features plus level/difference probes) is what matters here, not signal semantics.
- **Fields**: `normalized_trend_indicator_3`, `normalized_trend_indicator_4`
- **Implementation Example**: `quantile(ts_delta(ts_backfill({normalized_trend_indicator_3}, 66), 5))`
- **Direction**: High → long.
- **Why not crowded**: ts_arg timing features are outside the saturated level/revision probe family.

**Concept**: Recency of peak signal on normalized_trend_indicator_4 (ts_arg_max, 10d)
- **Mechanism**: Generic Path-1 diversity concept for dry-run extensibility validation on dataset price_signal_dl. The operator topology (ts_arg_max/ts_arg_min timing features plus level/difference probes) is what matters here, not signal semantics.
- **Fields**: `normalized_trend_indicator_3`, `normalized_trend_indicator_4`
- **Implementation Example**: `quantile(-ts_arg_max(ts_backfill({normalized_trend_indicator_4}, 66), 10))`
- **Direction**: High → long.
- **Why not crowded**: ts_arg timing features are outside the saturated level/revision probe family.

**Concept**: Recency of trough signal on normalized_trend_indicator_4 (ts_arg_min, 10d)
- **Mechanism**: Generic Path-1 diversity concept for dry-run extensibility validation on dataset price_signal_dl. The operator topology (ts_arg_max/ts_arg_min timing features plus level/difference probes) is what matters here, not signal semantics.
- **Fields**: `normalized_trend_indicator_3`, `normalized_trend_indicator_4`
- **Implementation Example**: `quantile(ts_arg_min(ts_backfill({normalized_trend_indicator_4}, 66), 10))`
- **Direction**: High → long.
- **Why not crowded**: ts_arg timing features are outside the saturated level/revision probe family.

**Concept**: Cross spread normalized_trend_indicator_3 minus normalized_trend_indicator_4
- **Mechanism**: Generic Path-1 diversity concept for dry-run extensibility validation on dataset price_signal_dl. The operator topology (ts_arg_max/ts_arg_min timing features plus level/difference probes) is what matters here, not signal semantics.
- **Fields**: `normalized_trend_indicator_3`, `normalized_trend_indicator_4`
- **Implementation Example**: `quantile(subtract(ts_backfill({normalized_trend_indicator_3}, 66), ts_backfill({normalized_trend_indicator_4}, 66)))`
- **Direction**: High → long.
- **Why not crowded**: ts_arg timing features are outside the saturated level/revision probe family.

**Concept**: Level rank of normalized_trend_indicator_4
- **Mechanism**: Generic Path-1 diversity concept for dry-run extensibility validation on dataset price_signal_dl. The operator topology (ts_arg_max/ts_arg_min timing features plus level/difference probes) is what matters here, not signal semantics.
- **Fields**: `normalized_trend_indicator_3`, `normalized_trend_indicator_4`
- **Implementation Example**: `quantile(rank(ts_backfill({normalized_trend_indicator_4}, 66)))`
- **Direction**: High → long.
- **Why not crowded**: ts_arg timing features are outside the saturated level/revision probe family.
