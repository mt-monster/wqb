**Dataset**: ai_factor_transfer  
**Region**: USA  
**Delay**: 1  
**Universe**: TOP3000

**Concept**: Recency of peak conviction on balanced_price_oscillator (ts_arg_max, 20d)
- **Mechanism**: Generic Path-1 diversity concept for dry-run extensibility validation on dataset ai_factor_transfer. The operator topology (ts_arg_max/ts_arg_min timing features plus level/difference probes) is what matters here, not signal semantics.
- **Fields**: `balanced_price_oscillator`, `balanced_price_oscillator_2`
- **Implementation Example**: `quantile(-ts_arg_max(ts_backfill({balanced_price_oscillator}, 66), 20))`
- **Direction**: High → long.
- **Why not crowded**: ts_arg timing features are outside the saturated level/revision probe family.

**Concept**: Recency of trough conviction on balanced_price_oscillator (ts_arg_min, 20d)
- **Mechanism**: Generic Path-1 diversity concept for dry-run extensibility validation on dataset ai_factor_transfer. The operator topology (ts_arg_max/ts_arg_min timing features plus level/difference probes) is what matters here, not signal semantics.
- **Fields**: `balanced_price_oscillator`, `balanced_price_oscillator_2`
- **Implementation Example**: `quantile(ts_arg_min(ts_backfill({balanced_price_oscillator}, 66), 20))`
- **Direction**: High → long.
- **Why not crowded**: ts_arg timing features are outside the saturated level/revision probe family.

**Concept**: Revision of balanced_price_oscillator (5-day change)
- **Mechanism**: Generic Path-1 diversity concept for dry-run extensibility validation on dataset ai_factor_transfer. The operator topology (ts_arg_max/ts_arg_min timing features plus level/difference probes) is what matters here, not signal semantics.
- **Fields**: `balanced_price_oscillator`, `balanced_price_oscillator_2`
- **Implementation Example**: `quantile(ts_delta(ts_backfill({balanced_price_oscillator}, 66), 5))`
- **Direction**: High → long.
- **Why not crowded**: ts_arg timing features are outside the saturated level/revision probe family.

**Concept**: Recency of peak signal on balanced_price_oscillator_2 (ts_arg_max, 10d)
- **Mechanism**: Generic Path-1 diversity concept for dry-run extensibility validation on dataset ai_factor_transfer. The operator topology (ts_arg_max/ts_arg_min timing features plus level/difference probes) is what matters here, not signal semantics.
- **Fields**: `balanced_price_oscillator`, `balanced_price_oscillator_2`
- **Implementation Example**: `quantile(-ts_arg_max(ts_backfill({balanced_price_oscillator_2}, 66), 10))`
- **Direction**: High → long.
- **Why not crowded**: ts_arg timing features are outside the saturated level/revision probe family.

**Concept**: Recency of trough signal on balanced_price_oscillator_2 (ts_arg_min, 10d)
- **Mechanism**: Generic Path-1 diversity concept for dry-run extensibility validation on dataset ai_factor_transfer. The operator topology (ts_arg_max/ts_arg_min timing features plus level/difference probes) is what matters here, not signal semantics.
- **Fields**: `balanced_price_oscillator`, `balanced_price_oscillator_2`
- **Implementation Example**: `quantile(ts_arg_min(ts_backfill({balanced_price_oscillator_2}, 66), 10))`
- **Direction**: High → long.
- **Why not crowded**: ts_arg timing features are outside the saturated level/revision probe family.

**Concept**: Cross spread balanced_price_oscillator minus balanced_price_oscillator_2
- **Mechanism**: Generic Path-1 diversity concept for dry-run extensibility validation on dataset ai_factor_transfer. The operator topology (ts_arg_max/ts_arg_min timing features plus level/difference probes) is what matters here, not signal semantics.
- **Fields**: `balanced_price_oscillator`, `balanced_price_oscillator_2`
- **Implementation Example**: `quantile(subtract(ts_backfill({balanced_price_oscillator}, 66), ts_backfill({balanced_price_oscillator_2}, 66)))`
- **Direction**: High → long.
- **Why not crowded**: ts_arg timing features are outside the saturated level/revision probe family.

**Concept**: Level rank of balanced_price_oscillator_2
- **Mechanism**: Generic Path-1 diversity concept for dry-run extensibility validation on dataset ai_factor_transfer. The operator topology (ts_arg_max/ts_arg_min timing features plus level/difference probes) is what matters here, not signal semantics.
- **Fields**: `balanced_price_oscillator`, `balanced_price_oscillator_2`
- **Implementation Example**: `quantile(rank(ts_backfill({balanced_price_oscillator_2}, 66)))`
- **Direction**: High → long.
- **Why not crowded**: ts_arg timing features are outside the saturated level/revision probe family.
