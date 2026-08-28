**Dataset**: other596  
**Region**: USA  
**Delay**: 1  
**Universe**: TOP3000

**Concept**: Recency of peak conviction on oth596_2dts_gen_441 (ts_arg_max, 20d)
- **Mechanism**: Generic Path-1 diversity concept for dry-run extensibility validation on dataset other596. The operator topology (ts_arg_max/ts_arg_min timing features plus level/difference probes) is what matters here, not signal semantics.
- **Fields**: `oth596_2dts_gen_441`, `oth596_2dts_sop_428`
- **Implementation Example**: `quantile(-ts_arg_max(ts_backfill({oth596_2dts_gen_441}, 66), 20))`
- **Direction**: High → long.
- **Why not crowded**: ts_arg timing features are outside the saturated level/revision probe family.

**Concept**: Recency of trough conviction on oth596_2dts_gen_441 (ts_arg_min, 20d)
- **Mechanism**: Generic Path-1 diversity concept for dry-run extensibility validation on dataset other596. The operator topology (ts_arg_max/ts_arg_min timing features plus level/difference probes) is what matters here, not signal semantics.
- **Fields**: `oth596_2dts_gen_441`, `oth596_2dts_sop_428`
- **Implementation Example**: `quantile(ts_arg_min(ts_backfill({oth596_2dts_gen_441}, 66), 20))`
- **Direction**: High → long.
- **Why not crowded**: ts_arg timing features are outside the saturated level/revision probe family.

**Concept**: Revision of oth596_2dts_gen_441 (5-day change)
- **Mechanism**: Generic Path-1 diversity concept for dry-run extensibility validation on dataset other596. The operator topology (ts_arg_max/ts_arg_min timing features plus level/difference probes) is what matters here, not signal semantics.
- **Fields**: `oth596_2dts_gen_441`, `oth596_2dts_sop_428`
- **Implementation Example**: `quantile(ts_delta(ts_backfill({oth596_2dts_gen_441}, 66), 5))`
- **Direction**: High → long.
- **Why not crowded**: ts_arg timing features are outside the saturated level/revision probe family.

**Concept**: Recency of peak signal on oth596_2dts_sop_428 (ts_arg_max, 10d)
- **Mechanism**: Generic Path-1 diversity concept for dry-run extensibility validation on dataset other596. The operator topology (ts_arg_max/ts_arg_min timing features plus level/difference probes) is what matters here, not signal semantics.
- **Fields**: `oth596_2dts_gen_441`, `oth596_2dts_sop_428`
- **Implementation Example**: `quantile(-ts_arg_max(ts_backfill({oth596_2dts_sop_428}, 66), 10))`
- **Direction**: High → long.
- **Why not crowded**: ts_arg timing features are outside the saturated level/revision probe family.

**Concept**: Recency of trough signal on oth596_2dts_sop_428 (ts_arg_min, 10d)
- **Mechanism**: Generic Path-1 diversity concept for dry-run extensibility validation on dataset other596. The operator topology (ts_arg_max/ts_arg_min timing features plus level/difference probes) is what matters here, not signal semantics.
- **Fields**: `oth596_2dts_gen_441`, `oth596_2dts_sop_428`
- **Implementation Example**: `quantile(ts_arg_min(ts_backfill({oth596_2dts_sop_428}, 66), 10))`
- **Direction**: High → long.
- **Why not crowded**: ts_arg timing features are outside the saturated level/revision probe family.

**Concept**: Cross spread oth596_2dts_gen_441 minus oth596_2dts_sop_428
- **Mechanism**: Generic Path-1 diversity concept for dry-run extensibility validation on dataset other596. The operator topology (ts_arg_max/ts_arg_min timing features plus level/difference probes) is what matters here, not signal semantics.
- **Fields**: `oth596_2dts_gen_441`, `oth596_2dts_sop_428`
- **Implementation Example**: `quantile(subtract(ts_backfill({oth596_2dts_gen_441}, 66), ts_backfill({oth596_2dts_sop_428}, 66)))`
- **Direction**: High → long.
- **Why not crowded**: ts_arg timing features are outside the saturated level/revision probe family.

**Concept**: Level rank of oth596_2dts_sop_428
- **Mechanism**: Generic Path-1 diversity concept for dry-run extensibility validation on dataset other596. The operator topology (ts_arg_max/ts_arg_min timing features plus level/difference probes) is what matters here, not signal semantics.
- **Fields**: `oth596_2dts_gen_441`, `oth596_2dts_sop_428`
- **Implementation Example**: `quantile(rank(ts_backfill({oth596_2dts_sop_428}, 66)))`
- **Direction**: High → long.
- **Why not crowded**: ts_arg timing features are outside the saturated level/revision probe family.
