**Dataset**: mmp_nlp_sentiment  
**Region**: USA  
**Delay**: 1  
**Universe**: TOP3000

**Concept**: Recency of peak conviction on advertisement_mention_total (ts_arg_max, 20d)
- **Mechanism**: Generic Path-1 diversity concept for dry-run extensibility validation on dataset mmp_nlp_sentiment. The operator topology (ts_arg_max/ts_arg_min timing features plus level/difference probes) is what matters here, not signal semantics.
- **Fields**: `advertisement_mention_total`, `afinn_negative_sentiment_count`
- **Implementation Example**: `quantile(-ts_arg_max(ts_backfill({advertisement_mention_total}, 66), 20))`
- **Direction**: High → long.
- **Why not crowded**: ts_arg timing features are outside the saturated level/revision probe family.

**Concept**: Recency of trough conviction on advertisement_mention_total (ts_arg_min, 20d)
- **Mechanism**: Generic Path-1 diversity concept for dry-run extensibility validation on dataset mmp_nlp_sentiment. The operator topology (ts_arg_max/ts_arg_min timing features plus level/difference probes) is what matters here, not signal semantics.
- **Fields**: `advertisement_mention_total`, `afinn_negative_sentiment_count`
- **Implementation Example**: `quantile(ts_arg_min(ts_backfill({advertisement_mention_total}, 66), 20))`
- **Direction**: High → long.
- **Why not crowded**: ts_arg timing features are outside the saturated level/revision probe family.

**Concept**: Revision of advertisement_mention_total (5-day change)
- **Mechanism**: Generic Path-1 diversity concept for dry-run extensibility validation on dataset mmp_nlp_sentiment. The operator topology (ts_arg_max/ts_arg_min timing features plus level/difference probes) is what matters here, not signal semantics.
- **Fields**: `advertisement_mention_total`, `afinn_negative_sentiment_count`
- **Implementation Example**: `quantile(ts_delta(ts_backfill({advertisement_mention_total}, 66), 5))`
- **Direction**: High → long.
- **Why not crowded**: ts_arg timing features are outside the saturated level/revision probe family.

**Concept**: Recency of peak signal on afinn_negative_sentiment_count (ts_arg_max, 10d)
- **Mechanism**: Generic Path-1 diversity concept for dry-run extensibility validation on dataset mmp_nlp_sentiment. The operator topology (ts_arg_max/ts_arg_min timing features plus level/difference probes) is what matters here, not signal semantics.
- **Fields**: `advertisement_mention_total`, `afinn_negative_sentiment_count`
- **Implementation Example**: `quantile(-ts_arg_max(ts_backfill({afinn_negative_sentiment_count}, 66), 10))`
- **Direction**: High → long.
- **Why not crowded**: ts_arg timing features are outside the saturated level/revision probe family.

**Concept**: Recency of trough signal on afinn_negative_sentiment_count (ts_arg_min, 10d)
- **Mechanism**: Generic Path-1 diversity concept for dry-run extensibility validation on dataset mmp_nlp_sentiment. The operator topology (ts_arg_max/ts_arg_min timing features plus level/difference probes) is what matters here, not signal semantics.
- **Fields**: `advertisement_mention_total`, `afinn_negative_sentiment_count`
- **Implementation Example**: `quantile(ts_arg_min(ts_backfill({afinn_negative_sentiment_count}, 66), 10))`
- **Direction**: High → long.
- **Why not crowded**: ts_arg timing features are outside the saturated level/revision probe family.

**Concept**: Cross spread advertisement_mention_total minus afinn_negative_sentiment_count
- **Mechanism**: Generic Path-1 diversity concept for dry-run extensibility validation on dataset mmp_nlp_sentiment. The operator topology (ts_arg_max/ts_arg_min timing features plus level/difference probes) is what matters here, not signal semantics.
- **Fields**: `advertisement_mention_total`, `afinn_negative_sentiment_count`
- **Implementation Example**: `quantile(subtract(ts_backfill({advertisement_mention_total}, 66), ts_backfill({afinn_negative_sentiment_count}, 66)))`
- **Direction**: High → long.
- **Why not crowded**: ts_arg timing features are outside the saturated level/revision probe family.

**Concept**: Level rank of afinn_negative_sentiment_count
- **Mechanism**: Generic Path-1 diversity concept for dry-run extensibility validation on dataset mmp_nlp_sentiment. The operator topology (ts_arg_max/ts_arg_min timing features plus level/difference probes) is what matters here, not signal semantics.
- **Fields**: `advertisement_mention_total`, `afinn_negative_sentiment_count`
- **Implementation Example**: `quantile(rank(ts_backfill({afinn_negative_sentiment_count}, 66)))`
- **Direction**: High → long.
- **Why not crowded**: ts_arg timing features are outside the saturated level/revision probe family.
