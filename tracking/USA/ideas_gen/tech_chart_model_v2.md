**Dataset**: tech_chart_model  
**Region**: USA  
**Delay**: 1  
**Universe**: TOP3000

**Concept**: Recency of peak conviction on absolute_price_oscillator_10d (ts_arg_max, 20d)
- **Mechanism**: Generic Path-1 diversity concept for dry-run extensibility validation on dataset tech_chart_model. The operator topology (ts_arg_max/ts_arg_min timing features plus level/difference probes) is what matters here, not signal semantics.
- **Fields**: `absolute_price_oscillator_10d`, `absolute_price_oscillator_50d`
- **Implementation Example**: `quantile(-ts_arg_max(ts_backfill({absolute_price_oscillator_10d}, 66), 20))`
- **Direction**: High → long.
- **Why not crowded**: ts_arg timing features are outside the saturated level/revision probe family.

**Concept**: Recency of trough conviction on absolute_price_oscillator_10d (ts_arg_min, 20d)
- **Mechanism**: Generic Path-1 diversity concept for dry-run extensibility validation on dataset tech_chart_model. The operator topology (ts_arg_max/ts_arg_min timing features plus level/difference probes) is what matters here, not signal semantics.
- **Fields**: `absolute_price_oscillator_10d`, `absolute_price_oscillator_50d`
- **Implementation Example**: `quantile(ts_arg_min(ts_backfill({absolute_price_oscillator_10d}, 66), 20))`
- **Direction**: High → long.
- **Why not crowded**: ts_arg timing features are outside the saturated level/revision probe family.

**Concept**: Revision of absolute_price_oscillator_10d (5-day change)
- **Mechanism**: Generic Path-1 diversity concept for dry-run extensibility validation on dataset tech_chart_model. The operator topology (ts_arg_max/ts_arg_min timing features plus level/difference probes) is what matters here, not signal semantics.
- **Fields**: `absolute_price_oscillator_10d`, `absolute_price_oscillator_50d`
- **Implementation Example**: `quantile(ts_delta(ts_backfill({absolute_price_oscillator_10d}, 66), 5))`
- **Direction**: High → long.
- **Why not crowded**: ts_arg timing features are outside the saturated level/revision probe family.

**Concept**: Recency of peak signal on absolute_price_oscillator_50d (ts_arg_max, 10d)
- **Mechanism**: Generic Path-1 diversity concept for dry-run extensibility validation on dataset tech_chart_model. The operator topology (ts_arg_max/ts_arg_min timing features plus level/difference probes) is what matters here, not signal semantics.
- **Fields**: `absolute_price_oscillator_10d`, `absolute_price_oscillator_50d`
- **Implementation Example**: `quantile(-ts_arg_max(ts_backfill({absolute_price_oscillator_50d}, 66), 10))`
- **Direction**: High → long.
- **Why not crowded**: ts_arg timing features are outside the saturated level/revision probe family.

**Concept**: Recency of trough signal on absolute_price_oscillator_50d (ts_arg_min, 10d)
- **Mechanism**: Generic Path-1 diversity concept for dry-run extensibility validation on dataset tech_chart_model. The operator topology (ts_arg_max/ts_arg_min timing features plus level/difference probes) is what matters here, not signal semantics.
- **Fields**: `absolute_price_oscillator_10d`, `absolute_price_oscillator_50d`
- **Implementation Example**: `quantile(ts_arg_min(ts_backfill({absolute_price_oscillator_50d}, 66), 10))`
- **Direction**: High → long.
- **Why not crowded**: ts_arg timing features are outside the saturated level/revision probe family.

**Concept**: Cross spread absolute_price_oscillator_10d minus absolute_price_oscillator_50d
- **Mechanism**: Generic Path-1 diversity concept for dry-run extensibility validation on dataset tech_chart_model. The operator topology (ts_arg_max/ts_arg_min timing features plus level/difference probes) is what matters here, not signal semantics.
- **Fields**: `absolute_price_oscillator_10d`, `absolute_price_oscillator_50d`
- **Implementation Example**: `quantile(subtract(ts_backfill({absolute_price_oscillator_10d}, 66), ts_backfill({absolute_price_oscillator_50d}, 66)))`
- **Direction**: High → long.
- **Why not crowded**: ts_arg timing features are outside the saturated level/revision probe family.

**Concept**: Level rank of absolute_price_oscillator_50d
- **Mechanism**: Generic Path-1 diversity concept for dry-run extensibility validation on dataset tech_chart_model. The operator topology (ts_arg_max/ts_arg_min timing features plus level/difference probes) is what matters here, not signal semantics.
- **Fields**: `absolute_price_oscillator_10d`, `absolute_price_oscillator_50d`
- **Implementation Example**: `quantile(rank(ts_backfill({absolute_price_oscillator_50d}, 66)))`
- **Direction**: High → long.
- **Why not crowded**: ts_arg timing features are outside the saturated level/revision probe family.
