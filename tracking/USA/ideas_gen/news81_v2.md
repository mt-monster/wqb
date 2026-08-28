**Dataset**: news81  
**Region**: USA  
**Delay**: 1  
**Universe**: TOP3000

**Concept**: Recency of peak conviction on headline_news_count_normalized (ts_arg_max, 20d)
- **Mechanism**: Generic Path-1 diversity concept for dry-run extensibility validation on dataset news81. The operator topology (ts_arg_max/ts_arg_min timing features plus level/difference probes) is what matters here, not signal semantics.
- **Fields**: `headline_news_count_normalized`, `headline_news_item_count`
- **Implementation Example**: `quantile(-ts_arg_max(ts_backfill({headline_news_count_normalized}, 66), 20))`
- **Direction**: High → long.
- **Why not crowded**: ts_arg timing features are outside the saturated level/revision probe family.

**Concept**: Recency of trough conviction on headline_news_count_normalized (ts_arg_min, 20d)
- **Mechanism**: Generic Path-1 diversity concept for dry-run extensibility validation on dataset news81. The operator topology (ts_arg_max/ts_arg_min timing features plus level/difference probes) is what matters here, not signal semantics.
- **Fields**: `headline_news_count_normalized`, `headline_news_item_count`
- **Implementation Example**: `quantile(ts_arg_min(ts_backfill({headline_news_count_normalized}, 66), 20))`
- **Direction**: High → long.
- **Why not crowded**: ts_arg timing features are outside the saturated level/revision probe family.

**Concept**: Revision of headline_news_count_normalized (5-day change)
- **Mechanism**: Generic Path-1 diversity concept for dry-run extensibility validation on dataset news81. The operator topology (ts_arg_max/ts_arg_min timing features plus level/difference probes) is what matters here, not signal semantics.
- **Fields**: `headline_news_count_normalized`, `headline_news_item_count`
- **Implementation Example**: `quantile(ts_delta(ts_backfill({headline_news_count_normalized}, 66), 5))`
- **Direction**: High → long.
- **Why not crowded**: ts_arg timing features are outside the saturated level/revision probe family.

**Concept**: Recency of peak signal on headline_news_item_count (ts_arg_max, 10d)
- **Mechanism**: Generic Path-1 diversity concept for dry-run extensibility validation on dataset news81. The operator topology (ts_arg_max/ts_arg_min timing features plus level/difference probes) is what matters here, not signal semantics.
- **Fields**: `headline_news_count_normalized`, `headline_news_item_count`
- **Implementation Example**: `quantile(-ts_arg_max(ts_backfill({headline_news_item_count}, 66), 10))`
- **Direction**: High → long.
- **Why not crowded**: ts_arg timing features are outside the saturated level/revision probe family.

**Concept**: Recency of trough signal on headline_news_item_count (ts_arg_min, 10d)
- **Mechanism**: Generic Path-1 diversity concept for dry-run extensibility validation on dataset news81. The operator topology (ts_arg_max/ts_arg_min timing features plus level/difference probes) is what matters here, not signal semantics.
- **Fields**: `headline_news_count_normalized`, `headline_news_item_count`
- **Implementation Example**: `quantile(ts_arg_min(ts_backfill({headline_news_item_count}, 66), 10))`
- **Direction**: High → long.
- **Why not crowded**: ts_arg timing features are outside the saturated level/revision probe family.

**Concept**: Cross spread headline_news_count_normalized minus headline_news_item_count
- **Mechanism**: Generic Path-1 diversity concept for dry-run extensibility validation on dataset news81. The operator topology (ts_arg_max/ts_arg_min timing features plus level/difference probes) is what matters here, not signal semantics.
- **Fields**: `headline_news_count_normalized`, `headline_news_item_count`
- **Implementation Example**: `quantile(subtract(ts_backfill({headline_news_count_normalized}, 66), ts_backfill({headline_news_item_count}, 66)))`
- **Direction**: High → long.
- **Why not crowded**: ts_arg timing features are outside the saturated level/revision probe family.

**Concept**: Level rank of headline_news_item_count
- **Mechanism**: Generic Path-1 diversity concept for dry-run extensibility validation on dataset news81. The operator topology (ts_arg_max/ts_arg_min timing features plus level/difference probes) is what matters here, not signal semantics.
- **Fields**: `headline_news_count_normalized`, `headline_news_item_count`
- **Implementation Example**: `quantile(rank(ts_backfill({headline_news_item_count}, 66)))`
- **Direction**: High → long.
- **Why not crowded**: ts_arg timing features are outside the saturated level/revision probe family.
