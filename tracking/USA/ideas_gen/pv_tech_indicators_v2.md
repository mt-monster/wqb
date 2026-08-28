**Dataset**: pv_tech_indicators  
**Region**: USA  
**Delay**: 1  
**Universe**: TOP3000

**Concept**: Recency of peak conviction on momentum_shift_indicator (ts_arg_max, 20d)
- **Mechanism**: Generic Path-1 diversity concept for dry-run extensibility validation on dataset pv_tech_indicators. The operator topology (ts_arg_max/ts_arg_min timing features plus level/difference probes) is what matters here, not signal semantics.
- **Fields**: `momentum_shift_indicator`, `momentum_strength_index`
- **Implementation Example**: `quantile(-ts_arg_max(ts_backfill({momentum_shift_indicator}, 66), 20))`
- **Direction**: High → long.
- **Why not crowded**: ts_arg timing features are outside the saturated level/revision probe family.

**Concept**: Recency of trough conviction on momentum_shift_indicator (ts_arg_min, 20d)
- **Mechanism**: Generic Path-1 diversity concept for dry-run extensibility validation on dataset pv_tech_indicators. The operator topology (ts_arg_max/ts_arg_min timing features plus level/difference probes) is what matters here, not signal semantics.
- **Fields**: `momentum_shift_indicator`, `momentum_strength_index`
- **Implementation Example**: `quantile(ts_arg_min(ts_backfill({momentum_shift_indicator}, 66), 20))`
- **Direction**: High → long.
- **Why not crowded**: ts_arg timing features are outside the saturated level/revision probe family.

**Concept**: Revision of momentum_shift_indicator (5-day change)
- **Mechanism**: Generic Path-1 diversity concept for dry-run extensibility validation on dataset pv_tech_indicators. The operator topology (ts_arg_max/ts_arg_min timing features plus level/difference probes) is what matters here, not signal semantics.
- **Fields**: `momentum_shift_indicator`, `momentum_strength_index`
- **Implementation Example**: `quantile(ts_delta(ts_backfill({momentum_shift_indicator}, 66), 5))`
- **Direction**: High → long.
- **Why not crowded**: ts_arg timing features are outside the saturated level/revision probe family.

**Concept**: Recency of peak signal on momentum_strength_index (ts_arg_max, 10d)
- **Mechanism**: Generic Path-1 diversity concept for dry-run extensibility validation on dataset pv_tech_indicators. The operator topology (ts_arg_max/ts_arg_min timing features plus level/difference probes) is what matters here, not signal semantics.
- **Fields**: `momentum_shift_indicator`, `momentum_strength_index`
- **Implementation Example**: `quantile(-ts_arg_max(ts_backfill({momentum_strength_index}, 66), 10))`
- **Direction**: High → long.
- **Why not crowded**: ts_arg timing features are outside the saturated level/revision probe family.

**Concept**: Recency of trough signal on momentum_strength_index (ts_arg_min, 10d)
- **Mechanism**: Generic Path-1 diversity concept for dry-run extensibility validation on dataset pv_tech_indicators. The operator topology (ts_arg_max/ts_arg_min timing features plus level/difference probes) is what matters here, not signal semantics.
- **Fields**: `momentum_shift_indicator`, `momentum_strength_index`
- **Implementation Example**: `quantile(ts_arg_min(ts_backfill({momentum_strength_index}, 66), 10))`
- **Direction**: High → long.
- **Why not crowded**: ts_arg timing features are outside the saturated level/revision probe family.

**Concept**: Cross spread momentum_shift_indicator minus momentum_strength_index
- **Mechanism**: Generic Path-1 diversity concept for dry-run extensibility validation on dataset pv_tech_indicators. The operator topology (ts_arg_max/ts_arg_min timing features plus level/difference probes) is what matters here, not signal semantics.
- **Fields**: `momentum_shift_indicator`, `momentum_strength_index`
- **Implementation Example**: `quantile(subtract(ts_backfill({momentum_shift_indicator}, 66), ts_backfill({momentum_strength_index}, 66)))`
- **Direction**: High → long.
- **Why not crowded**: ts_arg timing features are outside the saturated level/revision probe family.

**Concept**: Level rank of momentum_strength_index
- **Mechanism**: Generic Path-1 diversity concept for dry-run extensibility validation on dataset pv_tech_indicators. The operator topology (ts_arg_max/ts_arg_min timing features plus level/difference probes) is what matters here, not signal semantics.
- **Fields**: `momentum_shift_indicator`, `momentum_strength_index`
- **Implementation Example**: `quantile(rank(ts_backfill({momentum_strength_index}, 66)))`
- **Direction**: High → long.
- **Why not crowded**: ts_arg timing features are outside the saturated level/revision probe family.
