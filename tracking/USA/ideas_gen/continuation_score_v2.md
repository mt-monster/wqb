**Dataset**: continuation_score  
**Region**: USA  
**Delay**: 1  
**Universe**: TOP3000

**Concept**: Recency of peak conviction on avg_similarity_ascending_channel (ts_arg_max, 20d)
- **Mechanism**: Generic Path-1 diversity concept for dry-run extensibility validation on dataset continuation_score. The operator topology (ts_arg_max/ts_arg_min timing features plus level/difference probes) is what matters here, not signal semantics.
- **Fields**: `avg_similarity_ascending_channel`, `avg_similarity_ascending_staircase`
- **Implementation Example**: `quantile(-ts_arg_max(ts_backfill({avg_similarity_ascending_channel}, 66), 20))`
- **Direction**: High → long.
- **Why not crowded**: ts_arg timing features are outside the saturated level/revision probe family.

**Concept**: Recency of trough conviction on avg_similarity_ascending_channel (ts_arg_min, 20d)
- **Mechanism**: Generic Path-1 diversity concept for dry-run extensibility validation on dataset continuation_score. The operator topology (ts_arg_max/ts_arg_min timing features plus level/difference probes) is what matters here, not signal semantics.
- **Fields**: `avg_similarity_ascending_channel`, `avg_similarity_ascending_staircase`
- **Implementation Example**: `quantile(ts_arg_min(ts_backfill({avg_similarity_ascending_channel}, 66), 20))`
- **Direction**: High → long.
- **Why not crowded**: ts_arg timing features are outside the saturated level/revision probe family.

**Concept**: Revision of avg_similarity_ascending_channel (5-day change)
- **Mechanism**: Generic Path-1 diversity concept for dry-run extensibility validation on dataset continuation_score. The operator topology (ts_arg_max/ts_arg_min timing features plus level/difference probes) is what matters here, not signal semantics.
- **Fields**: `avg_similarity_ascending_channel`, `avg_similarity_ascending_staircase`
- **Implementation Example**: `quantile(ts_delta(ts_backfill({avg_similarity_ascending_channel}, 66), 5))`
- **Direction**: High → long.
- **Why not crowded**: ts_arg timing features are outside the saturated level/revision probe family.

**Concept**: Recency of peak signal on avg_similarity_ascending_staircase (ts_arg_max, 10d)
- **Mechanism**: Generic Path-1 diversity concept for dry-run extensibility validation on dataset continuation_score. The operator topology (ts_arg_max/ts_arg_min timing features plus level/difference probes) is what matters here, not signal semantics.
- **Fields**: `avg_similarity_ascending_channel`, `avg_similarity_ascending_staircase`
- **Implementation Example**: `quantile(-ts_arg_max(ts_backfill({avg_similarity_ascending_staircase}, 66), 10))`
- **Direction**: High → long.
- **Why not crowded**: ts_arg timing features are outside the saturated level/revision probe family.

**Concept**: Recency of trough signal on avg_similarity_ascending_staircase (ts_arg_min, 10d)
- **Mechanism**: Generic Path-1 diversity concept for dry-run extensibility validation on dataset continuation_score. The operator topology (ts_arg_max/ts_arg_min timing features plus level/difference probes) is what matters here, not signal semantics.
- **Fields**: `avg_similarity_ascending_channel`, `avg_similarity_ascending_staircase`
- **Implementation Example**: `quantile(ts_arg_min(ts_backfill({avg_similarity_ascending_staircase}, 66), 10))`
- **Direction**: High → long.
- **Why not crowded**: ts_arg timing features are outside the saturated level/revision probe family.

**Concept**: Cross spread avg_similarity_ascending_channel minus avg_similarity_ascending_staircase
- **Mechanism**: Generic Path-1 diversity concept for dry-run extensibility validation on dataset continuation_score. The operator topology (ts_arg_max/ts_arg_min timing features plus level/difference probes) is what matters here, not signal semantics.
- **Fields**: `avg_similarity_ascending_channel`, `avg_similarity_ascending_staircase`
- **Implementation Example**: `quantile(subtract(ts_backfill({avg_similarity_ascending_channel}, 66), ts_backfill({avg_similarity_ascending_staircase}, 66)))`
- **Direction**: High → long.
- **Why not crowded**: ts_arg timing features are outside the saturated level/revision probe family.

**Concept**: Level rank of avg_similarity_ascending_staircase
- **Mechanism**: Generic Path-1 diversity concept for dry-run extensibility validation on dataset continuation_score. The operator topology (ts_arg_max/ts_arg_min timing features plus level/difference probes) is what matters here, not signal semantics.
- **Fields**: `avg_similarity_ascending_channel`, `avg_similarity_ascending_staircase`
- **Implementation Example**: `quantile(rank(ts_backfill({avg_similarity_ascending_staircase}, 66)))`
- **Direction**: High → long.
- **Why not crowded**: ts_arg timing features are outside the saturated level/revision probe family.
