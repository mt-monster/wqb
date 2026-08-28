**Dataset**: nlp_news_scores  
**Region**: USA  
**Delay**: 1  
**Universe**: TOP3000

**Concept**: Recency of peak conviction on negative_sentiment_average (ts_arg_max, 20d)
- **Mechanism**: Generic Path-1 diversity concept for dry-run extensibility validation on dataset nlp_news_scores. The operator topology (ts_arg_max/ts_arg_min timing features plus level/difference probes) is what matters here, not signal semantics.
- **Fields**: `negative_sentiment_average`, `negative_sentiment_average_3`
- **Implementation Example**: `quantile(-ts_arg_max(ts_backfill({negative_sentiment_average}, 66), 20))`
- **Direction**: High → long.
- **Why not crowded**: ts_arg timing features are outside the saturated level/revision probe family.

**Concept**: Recency of trough conviction on negative_sentiment_average (ts_arg_min, 20d)
- **Mechanism**: Generic Path-1 diversity concept for dry-run extensibility validation on dataset nlp_news_scores. The operator topology (ts_arg_max/ts_arg_min timing features plus level/difference probes) is what matters here, not signal semantics.
- **Fields**: `negative_sentiment_average`, `negative_sentiment_average_3`
- **Implementation Example**: `quantile(ts_arg_min(ts_backfill({negative_sentiment_average}, 66), 20))`
- **Direction**: High → long.
- **Why not crowded**: ts_arg timing features are outside the saturated level/revision probe family.

**Concept**: Revision of negative_sentiment_average (5-day change)
- **Mechanism**: Generic Path-1 diversity concept for dry-run extensibility validation on dataset nlp_news_scores. The operator topology (ts_arg_max/ts_arg_min timing features plus level/difference probes) is what matters here, not signal semantics.
- **Fields**: `negative_sentiment_average`, `negative_sentiment_average_3`
- **Implementation Example**: `quantile(ts_delta(ts_backfill({negative_sentiment_average}, 66), 5))`
- **Direction**: High → long.
- **Why not crowded**: ts_arg timing features are outside the saturated level/revision probe family.

**Concept**: Recency of peak signal on negative_sentiment_average_3 (ts_arg_max, 10d)
- **Mechanism**: Generic Path-1 diversity concept for dry-run extensibility validation on dataset nlp_news_scores. The operator topology (ts_arg_max/ts_arg_min timing features plus level/difference probes) is what matters here, not signal semantics.
- **Fields**: `negative_sentiment_average`, `negative_sentiment_average_3`
- **Implementation Example**: `quantile(-ts_arg_max(ts_backfill({negative_sentiment_average_3}, 66), 10))`
- **Direction**: High → long.
- **Why not crowded**: ts_arg timing features are outside the saturated level/revision probe family.

**Concept**: Recency of trough signal on negative_sentiment_average_3 (ts_arg_min, 10d)
- **Mechanism**: Generic Path-1 diversity concept for dry-run extensibility validation on dataset nlp_news_scores. The operator topology (ts_arg_max/ts_arg_min timing features plus level/difference probes) is what matters here, not signal semantics.
- **Fields**: `negative_sentiment_average`, `negative_sentiment_average_3`
- **Implementation Example**: `quantile(ts_arg_min(ts_backfill({negative_sentiment_average_3}, 66), 10))`
- **Direction**: High → long.
- **Why not crowded**: ts_arg timing features are outside the saturated level/revision probe family.

**Concept**: Cross spread negative_sentiment_average minus negative_sentiment_average_3
- **Mechanism**: Generic Path-1 diversity concept for dry-run extensibility validation on dataset nlp_news_scores. The operator topology (ts_arg_max/ts_arg_min timing features plus level/difference probes) is what matters here, not signal semantics.
- **Fields**: `negative_sentiment_average`, `negative_sentiment_average_3`
- **Implementation Example**: `quantile(subtract(ts_backfill({negative_sentiment_average}, 66), ts_backfill({negative_sentiment_average_3}, 66)))`
- **Direction**: High → long.
- **Why not crowded**: ts_arg timing features are outside the saturated level/revision probe family.

**Concept**: Level rank of negative_sentiment_average_3
- **Mechanism**: Generic Path-1 diversity concept for dry-run extensibility validation on dataset nlp_news_scores. The operator topology (ts_arg_max/ts_arg_min timing features plus level/difference probes) is what matters here, not signal semantics.
- **Fields**: `negative_sentiment_average`, `negative_sentiment_average_3`
- **Implementation Example**: `quantile(rank(ts_backfill({negative_sentiment_average_3}, 66)))`
- **Direction**: High → long.
- **Why not crowded**: ts_arg timing features are outside the saturated level/revision probe family.
