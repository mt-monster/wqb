**Dataset**: news84  
**Region**: USA  
**Delay**: 1  
**Universe**: TOP3000

**Concept**: Recency of peak conviction on max_primary_sentiment_score_transfer (ts_arg_max, 20d)
- **Mechanism**: Generic Path-1 diversity concept for dry-run extensibility validation on dataset news84. The operator topology (ts_arg_max/ts_arg_min timing features plus level/difference probes) is what matters here, not signal semantics.
- **Fields**: `max_primary_sentiment_score_transfer`, `max_secondary_sentiment_score_transfer`
- **Implementation Example**: `quantile(-ts_arg_max(ts_backfill({max_primary_sentiment_score_transfer}, 66), 20))`
- **Direction**: High → long.
- **Why not crowded**: ts_arg timing features are outside the saturated level/revision probe family.

**Concept**: Recency of trough conviction on max_primary_sentiment_score_transfer (ts_arg_min, 20d)
- **Mechanism**: Generic Path-1 diversity concept for dry-run extensibility validation on dataset news84. The operator topology (ts_arg_max/ts_arg_min timing features plus level/difference probes) is what matters here, not signal semantics.
- **Fields**: `max_primary_sentiment_score_transfer`, `max_secondary_sentiment_score_transfer`
- **Implementation Example**: `quantile(ts_arg_min(ts_backfill({max_primary_sentiment_score_transfer}, 66), 20))`
- **Direction**: High → long.
- **Why not crowded**: ts_arg timing features are outside the saturated level/revision probe family.

**Concept**: Revision of max_primary_sentiment_score_transfer (5-day change)
- **Mechanism**: Generic Path-1 diversity concept for dry-run extensibility validation on dataset news84. The operator topology (ts_arg_max/ts_arg_min timing features plus level/difference probes) is what matters here, not signal semantics.
- **Fields**: `max_primary_sentiment_score_transfer`, `max_secondary_sentiment_score_transfer`
- **Implementation Example**: `quantile(ts_delta(ts_backfill({max_primary_sentiment_score_transfer}, 66), 5))`
- **Direction**: High → long.
- **Why not crowded**: ts_arg timing features are outside the saturated level/revision probe family.

**Concept**: Recency of peak signal on max_secondary_sentiment_score_transfer (ts_arg_max, 10d)
- **Mechanism**: Generic Path-1 diversity concept for dry-run extensibility validation on dataset news84. The operator topology (ts_arg_max/ts_arg_min timing features plus level/difference probes) is what matters here, not signal semantics.
- **Fields**: `max_primary_sentiment_score_transfer`, `max_secondary_sentiment_score_transfer`
- **Implementation Example**: `quantile(-ts_arg_max(ts_backfill({max_secondary_sentiment_score_transfer}, 66), 10))`
- **Direction**: High → long.
- **Why not crowded**: ts_arg timing features are outside the saturated level/revision probe family.

**Concept**: Recency of trough signal on max_secondary_sentiment_score_transfer (ts_arg_min, 10d)
- **Mechanism**: Generic Path-1 diversity concept for dry-run extensibility validation on dataset news84. The operator topology (ts_arg_max/ts_arg_min timing features plus level/difference probes) is what matters here, not signal semantics.
- **Fields**: `max_primary_sentiment_score_transfer`, `max_secondary_sentiment_score_transfer`
- **Implementation Example**: `quantile(ts_arg_min(ts_backfill({max_secondary_sentiment_score_transfer}, 66), 10))`
- **Direction**: High → long.
- **Why not crowded**: ts_arg timing features are outside the saturated level/revision probe family.

**Concept**: Cross spread max_primary_sentiment_score_transfer minus max_secondary_sentiment_score_transfer
- **Mechanism**: Generic Path-1 diversity concept for dry-run extensibility validation on dataset news84. The operator topology (ts_arg_max/ts_arg_min timing features plus level/difference probes) is what matters here, not signal semantics.
- **Fields**: `max_primary_sentiment_score_transfer`, `max_secondary_sentiment_score_transfer`
- **Implementation Example**: `quantile(subtract(ts_backfill({max_primary_sentiment_score_transfer}, 66), ts_backfill({max_secondary_sentiment_score_transfer}, 66)))`
- **Direction**: High → long.
- **Why not crowded**: ts_arg timing features are outside the saturated level/revision probe family.

**Concept**: Level rank of max_secondary_sentiment_score_transfer
- **Mechanism**: Generic Path-1 diversity concept for dry-run extensibility validation on dataset news84. The operator topology (ts_arg_max/ts_arg_min timing features plus level/difference probes) is what matters here, not signal semantics.
- **Fields**: `max_primary_sentiment_score_transfer`, `max_secondary_sentiment_score_transfer`
- **Implementation Example**: `quantile(rank(ts_backfill({max_secondary_sentiment_score_transfer}, 66)))`
- **Direction**: High → long.
- **Why not crowded**: ts_arg timing features are outside the saturated level/revision probe family.
