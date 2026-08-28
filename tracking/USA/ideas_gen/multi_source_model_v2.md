**Dataset**: multi_source_model  
**Region**: USA  
**Delay**: 1  
**Universe**: TOP3000

**Concept**: Recency of peak conviction on event_embedding_quantile2_60d_pred (ts_arg_max, 20d)
- **Mechanism**: Generic Path-1 diversity concept for dry-run extensibility validation on dataset multi_source_model. The operator topology (ts_arg_max/ts_arg_min timing features plus level/difference probes) is what matters here, not signal semantics.
- **Fields**: `event_embedding_quantile2_60d_pred`, `event_embedding_quantile2_confidence_60d_pred`
- **Implementation Example**: `quantile(-ts_arg_max(ts_backfill({event_embedding_quantile2_60d_pred}, 66), 20))`
- **Direction**: High → long.
- **Why not crowded**: ts_arg timing features are outside the saturated level/revision probe family.

**Concept**: Recency of trough conviction on event_embedding_quantile2_60d_pred (ts_arg_min, 20d)
- **Mechanism**: Generic Path-1 diversity concept for dry-run extensibility validation on dataset multi_source_model. The operator topology (ts_arg_max/ts_arg_min timing features plus level/difference probes) is what matters here, not signal semantics.
- **Fields**: `event_embedding_quantile2_60d_pred`, `event_embedding_quantile2_confidence_60d_pred`
- **Implementation Example**: `quantile(ts_arg_min(ts_backfill({event_embedding_quantile2_60d_pred}, 66), 20))`
- **Direction**: High → long.
- **Why not crowded**: ts_arg timing features are outside the saturated level/revision probe family.

**Concept**: Revision of event_embedding_quantile2_60d_pred (5-day change)
- **Mechanism**: Generic Path-1 diversity concept for dry-run extensibility validation on dataset multi_source_model. The operator topology (ts_arg_max/ts_arg_min timing features plus level/difference probes) is what matters here, not signal semantics.
- **Fields**: `event_embedding_quantile2_60d_pred`, `event_embedding_quantile2_confidence_60d_pred`
- **Implementation Example**: `quantile(ts_delta(ts_backfill({event_embedding_quantile2_60d_pred}, 66), 5))`
- **Direction**: High → long.
- **Why not crowded**: ts_arg timing features are outside the saturated level/revision probe family.

**Concept**: Recency of peak signal on event_embedding_quantile2_confidence_60d_pred (ts_arg_max, 10d)
- **Mechanism**: Generic Path-1 diversity concept for dry-run extensibility validation on dataset multi_source_model. The operator topology (ts_arg_max/ts_arg_min timing features plus level/difference probes) is what matters here, not signal semantics.
- **Fields**: `event_embedding_quantile2_60d_pred`, `event_embedding_quantile2_confidence_60d_pred`
- **Implementation Example**: `quantile(-ts_arg_max(ts_backfill({event_embedding_quantile2_confidence_60d_pred}, 66), 10))`
- **Direction**: High → long.
- **Why not crowded**: ts_arg timing features are outside the saturated level/revision probe family.

**Concept**: Recency of trough signal on event_embedding_quantile2_confidence_60d_pred (ts_arg_min, 10d)
- **Mechanism**: Generic Path-1 diversity concept for dry-run extensibility validation on dataset multi_source_model. The operator topology (ts_arg_max/ts_arg_min timing features plus level/difference probes) is what matters here, not signal semantics.
- **Fields**: `event_embedding_quantile2_60d_pred`, `event_embedding_quantile2_confidence_60d_pred`
- **Implementation Example**: `quantile(ts_arg_min(ts_backfill({event_embedding_quantile2_confidence_60d_pred}, 66), 10))`
- **Direction**: High → long.
- **Why not crowded**: ts_arg timing features are outside the saturated level/revision probe family.

**Concept**: Cross spread event_embedding_quantile2_60d_pred minus event_embedding_quantile2_confidence_60d_pred
- **Mechanism**: Generic Path-1 diversity concept for dry-run extensibility validation on dataset multi_source_model. The operator topology (ts_arg_max/ts_arg_min timing features plus level/difference probes) is what matters here, not signal semantics.
- **Fields**: `event_embedding_quantile2_60d_pred`, `event_embedding_quantile2_confidence_60d_pred`
- **Implementation Example**: `quantile(subtract(ts_backfill({event_embedding_quantile2_60d_pred}, 66), ts_backfill({event_embedding_quantile2_confidence_60d_pred}, 66)))`
- **Direction**: High → long.
- **Why not crowded**: ts_arg timing features are outside the saturated level/revision probe family.

**Concept**: Level rank of event_embedding_quantile2_confidence_60d_pred
- **Mechanism**: Generic Path-1 diversity concept for dry-run extensibility validation on dataset multi_source_model. The operator topology (ts_arg_max/ts_arg_min timing features plus level/difference probes) is what matters here, not signal semantics.
- **Fields**: `event_embedding_quantile2_60d_pred`, `event_embedding_quantile2_confidence_60d_pred`
- **Implementation Example**: `quantile(rank(ts_backfill({event_embedding_quantile2_confidence_60d_pred}, 66)))`
- **Direction**: High → long.
- **Why not crowded**: ts_arg timing features are outside the saturated level/revision probe family.
