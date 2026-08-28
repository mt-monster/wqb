**Dataset**: news97  
**Region**: USA  
**Delay**: 1  
**Universe**: TOP3000

**Concept**: Recency of peak conviction on nws97_2dts_gen (ts_arg_max, 20d)
- **Mechanism**: Generic Path-1 diversity concept for dry-run extensibility validation on dataset news97. The operator topology (ts_arg_max/ts_arg_min timing features plus level/difference probes) is what matters here, not signal semantics.
- **Fields**: `nws97_2dts_gen`, `nws97_2dts_sop`
- **Implementation Example**: `quantile(-ts_arg_max(ts_backfill({nws97_2dts_gen}, 66), 20))`
- **Direction**: High → long.
- **Why not crowded**: ts_arg timing features are outside the saturated level/revision probe family.

**Concept**: Recency of trough conviction on nws97_2dts_gen (ts_arg_min, 20d)
- **Mechanism**: Generic Path-1 diversity concept for dry-run extensibility validation on dataset news97. The operator topology (ts_arg_max/ts_arg_min timing features plus level/difference probes) is what matters here, not signal semantics.
- **Fields**: `nws97_2dts_gen`, `nws97_2dts_sop`
- **Implementation Example**: `quantile(ts_arg_min(ts_backfill({nws97_2dts_gen}, 66), 20))`
- **Direction**: High → long.
- **Why not crowded**: ts_arg timing features are outside the saturated level/revision probe family.

**Concept**: Revision of nws97_2dts_gen (5-day change)
- **Mechanism**: Generic Path-1 diversity concept for dry-run extensibility validation on dataset news97. The operator topology (ts_arg_max/ts_arg_min timing features plus level/difference probes) is what matters here, not signal semantics.
- **Fields**: `nws97_2dts_gen`, `nws97_2dts_sop`
- **Implementation Example**: `quantile(ts_delta(ts_backfill({nws97_2dts_gen}, 66), 5))`
- **Direction**: High → long.
- **Why not crowded**: ts_arg timing features are outside the saturated level/revision probe family.

**Concept**: Recency of peak signal on nws97_2dts_sop (ts_arg_max, 10d)
- **Mechanism**: Generic Path-1 diversity concept for dry-run extensibility validation on dataset news97. The operator topology (ts_arg_max/ts_arg_min timing features plus level/difference probes) is what matters here, not signal semantics.
- **Fields**: `nws97_2dts_gen`, `nws97_2dts_sop`
- **Implementation Example**: `quantile(-ts_arg_max(ts_backfill({nws97_2dts_sop}, 66), 10))`
- **Direction**: High → long.
- **Why not crowded**: ts_arg timing features are outside the saturated level/revision probe family.

**Concept**: Recency of trough signal on nws97_2dts_sop (ts_arg_min, 10d)
- **Mechanism**: Generic Path-1 diversity concept for dry-run extensibility validation on dataset news97. The operator topology (ts_arg_max/ts_arg_min timing features plus level/difference probes) is what matters here, not signal semantics.
- **Fields**: `nws97_2dts_gen`, `nws97_2dts_sop`
- **Implementation Example**: `quantile(ts_arg_min(ts_backfill({nws97_2dts_sop}, 66), 10))`
- **Direction**: High → long.
- **Why not crowded**: ts_arg timing features are outside the saturated level/revision probe family.

**Concept**: Cross spread nws97_2dts_gen minus nws97_2dts_sop
- **Mechanism**: Generic Path-1 diversity concept for dry-run extensibility validation on dataset news97. The operator topology (ts_arg_max/ts_arg_min timing features plus level/difference probes) is what matters here, not signal semantics.
- **Fields**: `nws97_2dts_gen`, `nws97_2dts_sop`
- **Implementation Example**: `quantile(subtract(ts_backfill({nws97_2dts_gen}, 66), ts_backfill({nws97_2dts_sop}, 66)))`
- **Direction**: High → long.
- **Why not crowded**: ts_arg timing features are outside the saturated level/revision probe family.

**Concept**: Level rank of nws97_2dts_sop
- **Mechanism**: Generic Path-1 diversity concept for dry-run extensibility validation on dataset news97. The operator topology (ts_arg_max/ts_arg_min timing features plus level/difference probes) is what matters here, not signal semantics.
- **Fields**: `nws97_2dts_gen`, `nws97_2dts_sop`
- **Implementation Example**: `quantile(rank(ts_backfill({nws97_2dts_sop}, 66)))`
- **Direction**: High → long.
- **Why not crowded**: ts_arg timing features are outside the saturated level/revision probe family.
