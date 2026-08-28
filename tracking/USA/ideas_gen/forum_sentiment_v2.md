**Dataset**: forum_sentiment  
**Region**: USA  
**Delay**: 1  
**Universe**: TOP3000

**Concept**: Recency of peak conviction on afinn_lexicon_sentiment_score (ts_arg_max, 20d)
- **Mechanism**: Generic Path-1 diversity concept for dry-run extensibility validation on dataset forum_sentiment. The operator topology (ts_arg_max/ts_arg_min timing features plus level/difference probes) is what matters here, not signal semantics.
- **Fields**: `afinn_lexicon_sentiment_score`, `average_character_count_text`
- **Implementation Example**: `quantile(-ts_arg_max(ts_backfill(vec_avg({afinn_lexicon_sentiment_score}), 66), 20))`
- **Direction**: High → long.
- **Why not crowded**: ts_arg timing features are outside the saturated level/revision probe family.

**Concept**: Recency of trough conviction on afinn_lexicon_sentiment_score (ts_arg_min, 20d)
- **Mechanism**: Generic Path-1 diversity concept for dry-run extensibility validation on dataset forum_sentiment. The operator topology (ts_arg_max/ts_arg_min timing features plus level/difference probes) is what matters here, not signal semantics.
- **Fields**: `afinn_lexicon_sentiment_score`, `average_character_count_text`
- **Implementation Example**: `quantile(ts_arg_min(ts_backfill(vec_avg({afinn_lexicon_sentiment_score}), 66), 20))`
- **Direction**: High → long.
- **Why not crowded**: ts_arg timing features are outside the saturated level/revision probe family.

**Concept**: Revision of afinn_lexicon_sentiment_score (5-day change)
- **Mechanism**: Generic Path-1 diversity concept for dry-run extensibility validation on dataset forum_sentiment. The operator topology (ts_arg_max/ts_arg_min timing features plus level/difference probes) is what matters here, not signal semantics.
- **Fields**: `afinn_lexicon_sentiment_score`, `average_character_count_text`
- **Implementation Example**: `quantile(ts_delta(ts_backfill(vec_avg({afinn_lexicon_sentiment_score}), 66), 5))`
- **Direction**: High → long.
- **Why not crowded**: ts_arg timing features are outside the saturated level/revision probe family.

**Concept**: Recency of peak signal on average_character_count_text (ts_arg_max, 10d)
- **Mechanism**: Generic Path-1 diversity concept for dry-run extensibility validation on dataset forum_sentiment. The operator topology (ts_arg_max/ts_arg_min timing features plus level/difference probes) is what matters here, not signal semantics.
- **Fields**: `afinn_lexicon_sentiment_score`, `average_character_count_text`
- **Implementation Example**: `quantile(-ts_arg_max(ts_backfill(vec_avg({average_character_count_text}), 66), 10))`
- **Direction**: High → long.
- **Why not crowded**: ts_arg timing features are outside the saturated level/revision probe family.

**Concept**: Recency of trough signal on average_character_count_text (ts_arg_min, 10d)
- **Mechanism**: Generic Path-1 diversity concept for dry-run extensibility validation on dataset forum_sentiment. The operator topology (ts_arg_max/ts_arg_min timing features plus level/difference probes) is what matters here, not signal semantics.
- **Fields**: `afinn_lexicon_sentiment_score`, `average_character_count_text`
- **Implementation Example**: `quantile(ts_arg_min(ts_backfill(vec_avg({average_character_count_text}), 66), 10))`
- **Direction**: High → long.
- **Why not crowded**: ts_arg timing features are outside the saturated level/revision probe family.

**Concept**: Cross spread afinn_lexicon_sentiment_score minus average_character_count_text
- **Mechanism**: Generic Path-1 diversity concept for dry-run extensibility validation on dataset forum_sentiment. The operator topology (ts_arg_max/ts_arg_min timing features plus level/difference probes) is what matters here, not signal semantics.
- **Fields**: `afinn_lexicon_sentiment_score`, `average_character_count_text`
- **Implementation Example**: `quantile(subtract(ts_backfill(vec_avg({afinn_lexicon_sentiment_score}), 66), ts_backfill(vec_avg({average_character_count_text}), 66)))`
- **Direction**: High → long.
- **Why not crowded**: ts_arg timing features are outside the saturated level/revision probe family.

**Concept**: Level rank of average_character_count_text
- **Mechanism**: Generic Path-1 diversity concept for dry-run extensibility validation on dataset forum_sentiment. The operator topology (ts_arg_max/ts_arg_min timing features plus level/difference probes) is what matters here, not signal semantics.
- **Fields**: `afinn_lexicon_sentiment_score`, `average_character_count_text`
- **Implementation Example**: `quantile(rank(ts_backfill(vec_avg({average_character_count_text}), 66)))`
- **Direction**: High → long.
- **Why not crowded**: ts_arg timing features are outside the saturated level/revision probe family.
