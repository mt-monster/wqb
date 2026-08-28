**Dataset**: news_sentiment_transfer  
**Region**: USA  
**Delay**: 1  
**Universe**: TOP3000

**Concept**: Recency of peak conviction on news_article_count (ts_arg_max, 20d)
- **Mechanism**: Generic Path-1 diversity concept for dry-run extensibility validation on dataset news_sentiment_transfer. The operator topology (ts_arg_max/ts_arg_min timing features plus level/difference probes) is what matters here, not signal semantics.
- **Fields**: `news_article_count`, `normalized_news_article_count`
- **Implementation Example**: `quantile(-ts_arg_max(ts_backfill({news_article_count}, 66), 20))`
- **Direction**: High → long.
- **Why not crowded**: ts_arg timing features are outside the saturated level/revision probe family.

**Concept**: Recency of trough conviction on news_article_count (ts_arg_min, 20d)
- **Mechanism**: Generic Path-1 diversity concept for dry-run extensibility validation on dataset news_sentiment_transfer. The operator topology (ts_arg_max/ts_arg_min timing features plus level/difference probes) is what matters here, not signal semantics.
- **Fields**: `news_article_count`, `normalized_news_article_count`
- **Implementation Example**: `quantile(ts_arg_min(ts_backfill({news_article_count}, 66), 20))`
- **Direction**: High → long.
- **Why not crowded**: ts_arg timing features are outside the saturated level/revision probe family.

**Concept**: Revision of news_article_count (5-day change)
- **Mechanism**: Generic Path-1 diversity concept for dry-run extensibility validation on dataset news_sentiment_transfer. The operator topology (ts_arg_max/ts_arg_min timing features plus level/difference probes) is what matters here, not signal semantics.
- **Fields**: `news_article_count`, `normalized_news_article_count`
- **Implementation Example**: `quantile(ts_delta(ts_backfill({news_article_count}, 66), 5))`
- **Direction**: High → long.
- **Why not crowded**: ts_arg timing features are outside the saturated level/revision probe family.

**Concept**: Recency of peak signal on normalized_news_article_count (ts_arg_max, 10d)
- **Mechanism**: Generic Path-1 diversity concept for dry-run extensibility validation on dataset news_sentiment_transfer. The operator topology (ts_arg_max/ts_arg_min timing features plus level/difference probes) is what matters here, not signal semantics.
- **Fields**: `news_article_count`, `normalized_news_article_count`
- **Implementation Example**: `quantile(-ts_arg_max(ts_backfill({normalized_news_article_count}, 66), 10))`
- **Direction**: High → long.
- **Why not crowded**: ts_arg timing features are outside the saturated level/revision probe family.

**Concept**: Recency of trough signal on normalized_news_article_count (ts_arg_min, 10d)
- **Mechanism**: Generic Path-1 diversity concept for dry-run extensibility validation on dataset news_sentiment_transfer. The operator topology (ts_arg_max/ts_arg_min timing features plus level/difference probes) is what matters here, not signal semantics.
- **Fields**: `news_article_count`, `normalized_news_article_count`
- **Implementation Example**: `quantile(ts_arg_min(ts_backfill({normalized_news_article_count}, 66), 10))`
- **Direction**: High → long.
- **Why not crowded**: ts_arg timing features are outside the saturated level/revision probe family.

**Concept**: Cross spread news_article_count minus normalized_news_article_count
- **Mechanism**: Generic Path-1 diversity concept for dry-run extensibility validation on dataset news_sentiment_transfer. The operator topology (ts_arg_max/ts_arg_min timing features plus level/difference probes) is what matters here, not signal semantics.
- **Fields**: `news_article_count`, `normalized_news_article_count`
- **Implementation Example**: `quantile(subtract(ts_backfill({news_article_count}, 66), ts_backfill({normalized_news_article_count}, 66)))`
- **Direction**: High → long.
- **Why not crowded**: ts_arg timing features are outside the saturated level/revision probe family.

**Concept**: Level rank of normalized_news_article_count
- **Mechanism**: Generic Path-1 diversity concept for dry-run extensibility validation on dataset news_sentiment_transfer. The operator topology (ts_arg_max/ts_arg_min timing features plus level/difference probes) is what matters here, not signal semantics.
- **Fields**: `news_article_count`, `normalized_news_article_count`
- **Implementation Example**: `quantile(rank(ts_backfill({normalized_news_article_count}, 66)))`
- **Direction**: High → long.
- **Why not crowded**: ts_arg timing features are outside the saturated level/revision probe family.
