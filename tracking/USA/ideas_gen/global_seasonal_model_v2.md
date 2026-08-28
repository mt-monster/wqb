**Dataset**: global_seasonal_model  
**Region**: USA  
**Delay**: 1  
**Universe**: TOP3000

**Concept**: Recency of peak conviction on analyst_metadata_feature1 (ts_arg_max, 20d)
- **Mechanism**: Generic Path-1 diversity concept for dry-run extensibility validation on dataset global_seasonal_model. The operator topology (ts_arg_max/ts_arg_min timing features plus level/difference probes) is what matters here, not signal semantics.
- **Fields**: `analyst_metadata_feature1`, `iso_week_number`
- **Implementation Example**: `quantile(-ts_arg_max(ts_backfill({analyst_metadata_feature1}, 66), 20))`
- **Direction**: High → long.
- **Why not crowded**: ts_arg timing features are outside the saturated level/revision probe family.

**Concept**: Recency of trough conviction on analyst_metadata_feature1 (ts_arg_min, 20d)
- **Mechanism**: Generic Path-1 diversity concept for dry-run extensibility validation on dataset global_seasonal_model. The operator topology (ts_arg_max/ts_arg_min timing features plus level/difference probes) is what matters here, not signal semantics.
- **Fields**: `analyst_metadata_feature1`, `iso_week_number`
- **Implementation Example**: `quantile(ts_arg_min(ts_backfill({analyst_metadata_feature1}, 66), 20))`
- **Direction**: High → long.
- **Why not crowded**: ts_arg timing features are outside the saturated level/revision probe family.

**Concept**: Revision of analyst_metadata_feature1 (5-day change)
- **Mechanism**: Generic Path-1 diversity concept for dry-run extensibility validation on dataset global_seasonal_model. The operator topology (ts_arg_max/ts_arg_min timing features plus level/difference probes) is what matters here, not signal semantics.
- **Fields**: `analyst_metadata_feature1`, `iso_week_number`
- **Implementation Example**: `quantile(ts_delta(ts_backfill({analyst_metadata_feature1}, 66), 5))`
- **Direction**: High → long.
- **Why not crowded**: ts_arg timing features are outside the saturated level/revision probe family.

**Concept**: Recency of peak signal on iso_week_number (ts_arg_max, 10d)
- **Mechanism**: Generic Path-1 diversity concept for dry-run extensibility validation on dataset global_seasonal_model. The operator topology (ts_arg_max/ts_arg_min timing features plus level/difference probes) is what matters here, not signal semantics.
- **Fields**: `analyst_metadata_feature1`, `iso_week_number`
- **Implementation Example**: `quantile(-ts_arg_max(ts_backfill({iso_week_number}, 66), 10))`
- **Direction**: High → long.
- **Why not crowded**: ts_arg timing features are outside the saturated level/revision probe family.

**Concept**: Recency of trough signal on iso_week_number (ts_arg_min, 10d)
- **Mechanism**: Generic Path-1 diversity concept for dry-run extensibility validation on dataset global_seasonal_model. The operator topology (ts_arg_max/ts_arg_min timing features plus level/difference probes) is what matters here, not signal semantics.
- **Fields**: `analyst_metadata_feature1`, `iso_week_number`
- **Implementation Example**: `quantile(ts_arg_min(ts_backfill({iso_week_number}, 66), 10))`
- **Direction**: High → long.
- **Why not crowded**: ts_arg timing features are outside the saturated level/revision probe family.

**Concept**: Cross spread analyst_metadata_feature1 minus iso_week_number
- **Mechanism**: Generic Path-1 diversity concept for dry-run extensibility validation on dataset global_seasonal_model. The operator topology (ts_arg_max/ts_arg_min timing features plus level/difference probes) is what matters here, not signal semantics.
- **Fields**: `analyst_metadata_feature1`, `iso_week_number`
- **Implementation Example**: `quantile(subtract(ts_backfill({analyst_metadata_feature1}, 66), ts_backfill({iso_week_number}, 66)))`
- **Direction**: High → long.
- **Why not crowded**: ts_arg timing features are outside the saturated level/revision probe family.

**Concept**: Level rank of iso_week_number
- **Mechanism**: Generic Path-1 diversity concept for dry-run extensibility validation on dataset global_seasonal_model. The operator topology (ts_arg_max/ts_arg_min timing features plus level/difference probes) is what matters here, not signal semantics.
- **Fields**: `analyst_metadata_feature1`, `iso_week_number`
- **Implementation Example**: `quantile(rank(ts_backfill({iso_week_number}, 66)))`
- **Direction**: High → long.
- **Why not crowded**: ts_arg timing features are outside the saturated level/revision probe family.
