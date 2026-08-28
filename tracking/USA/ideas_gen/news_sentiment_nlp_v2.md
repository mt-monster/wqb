**Dataset**: news_sentiment_nlp  
**Region**: USA  
**Delay**: 1  
**Universe**: TOP3000

**Concept**: Recency of peak conviction on headline_average_sentence_length (ts_arg_max, 20d)
- **Mechanism**: Generic Path-1 diversity concept for dry-run extensibility validation on dataset news_sentiment_nlp. The operator topology (ts_arg_max/ts_arg_min timing features plus level/difference probes) is what matters here, not signal semantics.
- **Fields**: `headline_average_sentence_length`, `headline_flesch_kincaid_score`
- **Implementation Example**: `quantile(-ts_arg_max(ts_backfill(vec_avg({headline_average_sentence_length}), 66), 20))`
- **Direction**: High → long.
- **Why not crowded**: ts_arg timing features are outside the saturated level/revision probe family.

**Concept**: Recency of trough conviction on headline_average_sentence_length (ts_arg_min, 20d)
- **Mechanism**: Generic Path-1 diversity concept for dry-run extensibility validation on dataset news_sentiment_nlp. The operator topology (ts_arg_max/ts_arg_min timing features plus level/difference probes) is what matters here, not signal semantics.
- **Fields**: `headline_average_sentence_length`, `headline_flesch_kincaid_score`
- **Implementation Example**: `quantile(ts_arg_min(ts_backfill(vec_avg({headline_average_sentence_length}), 66), 20))`
- **Direction**: High → long.
- **Why not crowded**: ts_arg timing features are outside the saturated level/revision probe family.

**Concept**: Revision of headline_average_sentence_length (5-day change)
- **Mechanism**: Generic Path-1 diversity concept for dry-run extensibility validation on dataset news_sentiment_nlp. The operator topology (ts_arg_max/ts_arg_min timing features plus level/difference probes) is what matters here, not signal semantics.
- **Fields**: `headline_average_sentence_length`, `headline_flesch_kincaid_score`
- **Implementation Example**: `quantile(ts_delta(ts_backfill(vec_avg({headline_average_sentence_length}), 66), 5))`
- **Direction**: High → long.
- **Why not crowded**: ts_arg timing features are outside the saturated level/revision probe family.

**Concept**: Recency of peak signal on headline_flesch_kincaid_score (ts_arg_max, 10d)
- **Mechanism**: Generic Path-1 diversity concept for dry-run extensibility validation on dataset news_sentiment_nlp. The operator topology (ts_arg_max/ts_arg_min timing features plus level/difference probes) is what matters here, not signal semantics.
- **Fields**: `headline_average_sentence_length`, `headline_flesch_kincaid_score`
- **Implementation Example**: `quantile(-ts_arg_max(ts_backfill(vec_avg({headline_flesch_kincaid_score}), 66), 10))`
- **Direction**: High → long.
- **Why not crowded**: ts_arg timing features are outside the saturated level/revision probe family.

**Concept**: Recency of trough signal on headline_flesch_kincaid_score (ts_arg_min, 10d)
- **Mechanism**: Generic Path-1 diversity concept for dry-run extensibility validation on dataset news_sentiment_nlp. The operator topology (ts_arg_max/ts_arg_min timing features plus level/difference probes) is what matters here, not signal semantics.
- **Fields**: `headline_average_sentence_length`, `headline_flesch_kincaid_score`
- **Implementation Example**: `quantile(ts_arg_min(ts_backfill(vec_avg({headline_flesch_kincaid_score}), 66), 10))`
- **Direction**: High → long.
- **Why not crowded**: ts_arg timing features are outside the saturated level/revision probe family.

**Concept**: Cross spread headline_average_sentence_length minus headline_flesch_kincaid_score
- **Mechanism**: Generic Path-1 diversity concept for dry-run extensibility validation on dataset news_sentiment_nlp. The operator topology (ts_arg_max/ts_arg_min timing features plus level/difference probes) is what matters here, not signal semantics.
- **Fields**: `headline_average_sentence_length`, `headline_flesch_kincaid_score`
- **Implementation Example**: `quantile(subtract(ts_backfill(vec_avg({headline_average_sentence_length}), 66), ts_backfill(vec_avg({headline_flesch_kincaid_score}), 66)))`
- **Direction**: High → long.
- **Why not crowded**: ts_arg timing features are outside the saturated level/revision probe family.

**Concept**: Level rank of headline_flesch_kincaid_score
- **Mechanism**: Generic Path-1 diversity concept for dry-run extensibility validation on dataset news_sentiment_nlp. The operator topology (ts_arg_max/ts_arg_min timing features plus level/difference probes) is what matters here, not signal semantics.
- **Fields**: `headline_average_sentence_length`, `headline_flesch_kincaid_score`
- **Implementation Example**: `quantile(rank(ts_backfill(vec_avg({headline_flesch_kincaid_score}), 66)))`
- **Direction**: High → long.
- **Why not crowded**: ts_arg timing features are outside the saturated level/revision probe family.
