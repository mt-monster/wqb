**Dataset**: pattern_scores  
**Region**: USA  
**Delay**: 1  
**Universe**: TOP3000

**Concept**: Recency of peak conviction on continuation_downward_wedge_max_similarity_40d (ts_arg_max, 20d)
- **Mechanism**: Generic Path-1 diversity concept for dry-run extensibility validation on dataset pattern_scores. The operator topology (ts_arg_max/ts_arg_min timing features plus level/difference probes) is what matters here, not signal semantics.
- **Fields**: `continuation_downward_wedge_max_similarity_40d`, `continuation_downward_wedge_median_similarity_40d`
- **Implementation Example**: `quantile(-ts_arg_max(ts_backfill({continuation_downward_wedge_max_similarity_40d}, 66), 20))`
- **Direction**: High → long.
- **Why not crowded**: ts_arg timing features are outside the saturated level/revision probe family.

**Concept**: Recency of trough conviction on continuation_downward_wedge_max_similarity_40d (ts_arg_min, 20d)
- **Mechanism**: Generic Path-1 diversity concept for dry-run extensibility validation on dataset pattern_scores. The operator topology (ts_arg_max/ts_arg_min timing features plus level/difference probes) is what matters here, not signal semantics.
- **Fields**: `continuation_downward_wedge_max_similarity_40d`, `continuation_downward_wedge_median_similarity_40d`
- **Implementation Example**: `quantile(ts_arg_min(ts_backfill({continuation_downward_wedge_max_similarity_40d}, 66), 20))`
- **Direction**: High → long.
- **Why not crowded**: ts_arg timing features are outside the saturated level/revision probe family.

**Concept**: Revision of continuation_downward_wedge_max_similarity_40d (5-day change)
- **Mechanism**: Generic Path-1 diversity concept for dry-run extensibility validation on dataset pattern_scores. The operator topology (ts_arg_max/ts_arg_min timing features plus level/difference probes) is what matters here, not signal semantics.
- **Fields**: `continuation_downward_wedge_max_similarity_40d`, `continuation_downward_wedge_median_similarity_40d`
- **Implementation Example**: `quantile(ts_delta(ts_backfill({continuation_downward_wedge_max_similarity_40d}, 66), 5))`
- **Direction**: High → long.
- **Why not crowded**: ts_arg timing features are outside the saturated level/revision probe family.

**Concept**: Recency of peak signal on continuation_downward_wedge_median_similarity_40d (ts_arg_max, 10d)
- **Mechanism**: Generic Path-1 diversity concept for dry-run extensibility validation on dataset pattern_scores. The operator topology (ts_arg_max/ts_arg_min timing features plus level/difference probes) is what matters here, not signal semantics.
- **Fields**: `continuation_downward_wedge_max_similarity_40d`, `continuation_downward_wedge_median_similarity_40d`
- **Implementation Example**: `quantile(-ts_arg_max(ts_backfill({continuation_downward_wedge_median_similarity_40d}, 66), 10))`
- **Direction**: High → long.
- **Why not crowded**: ts_arg timing features are outside the saturated level/revision probe family.

**Concept**: Recency of trough signal on continuation_downward_wedge_median_similarity_40d (ts_arg_min, 10d)
- **Mechanism**: Generic Path-1 diversity concept for dry-run extensibility validation on dataset pattern_scores. The operator topology (ts_arg_max/ts_arg_min timing features plus level/difference probes) is what matters here, not signal semantics.
- **Fields**: `continuation_downward_wedge_max_similarity_40d`, `continuation_downward_wedge_median_similarity_40d`
- **Implementation Example**: `quantile(ts_arg_min(ts_backfill({continuation_downward_wedge_median_similarity_40d}, 66), 10))`
- **Direction**: High → long.
- **Why not crowded**: ts_arg timing features are outside the saturated level/revision probe family.

**Concept**: Cross spread continuation_downward_wedge_max_similarity_40d minus continuation_downward_wedge_median_similarity_40d
- **Mechanism**: Generic Path-1 diversity concept for dry-run extensibility validation on dataset pattern_scores. The operator topology (ts_arg_max/ts_arg_min timing features plus level/difference probes) is what matters here, not signal semantics.
- **Fields**: `continuation_downward_wedge_max_similarity_40d`, `continuation_downward_wedge_median_similarity_40d`
- **Implementation Example**: `quantile(subtract(ts_backfill({continuation_downward_wedge_max_similarity_40d}, 66), ts_backfill({continuation_downward_wedge_median_similarity_40d}, 66)))`
- **Direction**: High → long.
- **Why not crowded**: ts_arg timing features are outside the saturated level/revision probe family.

**Concept**: Level rank of continuation_downward_wedge_median_similarity_40d
- **Mechanism**: Generic Path-1 diversity concept for dry-run extensibility validation on dataset pattern_scores. The operator topology (ts_arg_max/ts_arg_min timing features plus level/difference probes) is what matters here, not signal semantics.
- **Fields**: `continuation_downward_wedge_max_similarity_40d`, `continuation_downward_wedge_median_similarity_40d`
- **Implementation Example**: `quantile(rank(ts_backfill({continuation_downward_wedge_median_similarity_40d}, 66)))`
- **Direction**: High → long.
- **Why not crowded**: ts_arg timing features are outside the saturated level/revision probe family.
