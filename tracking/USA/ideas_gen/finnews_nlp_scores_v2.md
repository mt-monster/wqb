**Dataset**: finnews_nlp_scores  
**Region**: USA  
**Delay**: 1  
**Universe**: TOP3000

**Concept**: Recency of peak conviction on average_negative_sentiment_score_1 (ts_arg_max, 20d)
- **Mechanism**: Generic Path-1 diversity concept for dry-run extensibility validation on dataset finnews_nlp_scores. The operator topology (ts_arg_max/ts_arg_min timing features plus level/difference probes) is what matters here, not signal semantics.
- **Fields**: `average_negative_sentiment_score_1`, `average_negative_sentiment_score_2`
- **Implementation Example**: `quantile(-ts_arg_max(ts_backfill({average_negative_sentiment_score_1}, 66), 20))`
- **Direction**: High → long.
- **Why not crowded**: ts_arg timing features are outside the saturated level/revision probe family.

**Concept**: Recency of trough conviction on average_negative_sentiment_score_1 (ts_arg_min, 20d)
- **Mechanism**: Generic Path-1 diversity concept for dry-run extensibility validation on dataset finnews_nlp_scores. The operator topology (ts_arg_max/ts_arg_min timing features plus level/difference probes) is what matters here, not signal semantics.
- **Fields**: `average_negative_sentiment_score_1`, `average_negative_sentiment_score_2`
- **Implementation Example**: `quantile(ts_arg_min(ts_backfill({average_negative_sentiment_score_1}, 66), 20))`
- **Direction**: High → long.
- **Why not crowded**: ts_arg timing features are outside the saturated level/revision probe family.

**Concept**: Revision of average_negative_sentiment_score_1 (5-day change)
- **Mechanism**: Generic Path-1 diversity concept for dry-run extensibility validation on dataset finnews_nlp_scores. The operator topology (ts_arg_max/ts_arg_min timing features plus level/difference probes) is what matters here, not signal semantics.
- **Fields**: `average_negative_sentiment_score_1`, `average_negative_sentiment_score_2`
- **Implementation Example**: `quantile(ts_delta(ts_backfill({average_negative_sentiment_score_1}, 66), 5))`
- **Direction**: High → long.
- **Why not crowded**: ts_arg timing features are outside the saturated level/revision probe family.

**Concept**: Recency of peak signal on average_negative_sentiment_score_2 (ts_arg_max, 10d)
- **Mechanism**: Generic Path-1 diversity concept for dry-run extensibility validation on dataset finnews_nlp_scores. The operator topology (ts_arg_max/ts_arg_min timing features plus level/difference probes) is what matters here, not signal semantics.
- **Fields**: `average_negative_sentiment_score_1`, `average_negative_sentiment_score_2`
- **Implementation Example**: `quantile(-ts_arg_max(ts_backfill({average_negative_sentiment_score_2}, 66), 10))`
- **Direction**: High → long.
- **Why not crowded**: ts_arg timing features are outside the saturated level/revision probe family.

**Concept**: Recency of trough signal on average_negative_sentiment_score_2 (ts_arg_min, 10d)
- **Mechanism**: Generic Path-1 diversity concept for dry-run extensibility validation on dataset finnews_nlp_scores. The operator topology (ts_arg_max/ts_arg_min timing features plus level/difference probes) is what matters here, not signal semantics.
- **Fields**: `average_negative_sentiment_score_1`, `average_negative_sentiment_score_2`
- **Implementation Example**: `quantile(ts_arg_min(ts_backfill({average_negative_sentiment_score_2}, 66), 10))`
- **Direction**: High → long.
- **Why not crowded**: ts_arg timing features are outside the saturated level/revision probe family.

**Concept**: Cross spread average_negative_sentiment_score_1 minus average_negative_sentiment_score_2
- **Mechanism**: Generic Path-1 diversity concept for dry-run extensibility validation on dataset finnews_nlp_scores. The operator topology (ts_arg_max/ts_arg_min timing features plus level/difference probes) is what matters here, not signal semantics.
- **Fields**: `average_negative_sentiment_score_1`, `average_negative_sentiment_score_2`
- **Implementation Example**: `quantile(subtract(ts_backfill({average_negative_sentiment_score_1}, 66), ts_backfill({average_negative_sentiment_score_2}, 66)))`
- **Direction**: High → long.
- **Why not crowded**: ts_arg timing features are outside the saturated level/revision probe family.

**Concept**: Level rank of average_negative_sentiment_score_2
- **Mechanism**: Generic Path-1 diversity concept for dry-run extensibility validation on dataset finnews_nlp_scores. The operator topology (ts_arg_max/ts_arg_min timing features plus level/difference probes) is what matters here, not signal semantics.
- **Fields**: `average_negative_sentiment_score_1`, `average_negative_sentiment_score_2`
- **Implementation Example**: `quantile(rank(ts_backfill({average_negative_sentiment_score_2}, 66)))`
- **Direction**: High → long.
- **Why not crowded**: ts_arg timing features are outside the saturated level/revision probe family.
