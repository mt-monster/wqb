**Dataset**: chart_cnn_alpha  
**Region**: USA  
**Delay**: 1  
**Universe**: TOP3000

**Concept**: Recency of peak conviction on img_feat1_pca1batch3_us_day1 (ts_arg_max, 20d)
- **Mechanism**: Generic Path-1 diversity concept for dry-run extensibility validation on dataset chart_cnn_alpha. The operator topology (ts_arg_max/ts_arg_min timing features plus level/difference probes) is what matters here, not signal semantics.
- **Fields**: `img_feat1_pca1batch3_us_day1`, `img_feat1_pca6_us_day1`
- **Implementation Example**: `quantile(-ts_arg_max(ts_backfill({img_feat1_pca1batch3_us_day1}, 66), 20))`
- **Direction**: High → long.
- **Why not crowded**: ts_arg timing features are outside the saturated level/revision probe family.

**Concept**: Recency of trough conviction on img_feat1_pca1batch3_us_day1 (ts_arg_min, 20d)
- **Mechanism**: Generic Path-1 diversity concept for dry-run extensibility validation on dataset chart_cnn_alpha. The operator topology (ts_arg_max/ts_arg_min timing features plus level/difference probes) is what matters here, not signal semantics.
- **Fields**: `img_feat1_pca1batch3_us_day1`, `img_feat1_pca6_us_day1`
- **Implementation Example**: `quantile(ts_arg_min(ts_backfill({img_feat1_pca1batch3_us_day1}, 66), 20))`
- **Direction**: High → long.
- **Why not crowded**: ts_arg timing features are outside the saturated level/revision probe family.

**Concept**: Revision of img_feat1_pca1batch3_us_day1 (5-day change)
- **Mechanism**: Generic Path-1 diversity concept for dry-run extensibility validation on dataset chart_cnn_alpha. The operator topology (ts_arg_max/ts_arg_min timing features plus level/difference probes) is what matters here, not signal semantics.
- **Fields**: `img_feat1_pca1batch3_us_day1`, `img_feat1_pca6_us_day1`
- **Implementation Example**: `quantile(ts_delta(ts_backfill({img_feat1_pca1batch3_us_day1}, 66), 5))`
- **Direction**: High → long.
- **Why not crowded**: ts_arg timing features are outside the saturated level/revision probe family.

**Concept**: Recency of peak signal on img_feat1_pca6_us_day1 (ts_arg_max, 10d)
- **Mechanism**: Generic Path-1 diversity concept for dry-run extensibility validation on dataset chart_cnn_alpha. The operator topology (ts_arg_max/ts_arg_min timing features plus level/difference probes) is what matters here, not signal semantics.
- **Fields**: `img_feat1_pca1batch3_us_day1`, `img_feat1_pca6_us_day1`
- **Implementation Example**: `quantile(-ts_arg_max(ts_backfill({img_feat1_pca6_us_day1}, 66), 10))`
- **Direction**: High → long.
- **Why not crowded**: ts_arg timing features are outside the saturated level/revision probe family.

**Concept**: Recency of trough signal on img_feat1_pca6_us_day1 (ts_arg_min, 10d)
- **Mechanism**: Generic Path-1 diversity concept for dry-run extensibility validation on dataset chart_cnn_alpha. The operator topology (ts_arg_max/ts_arg_min timing features plus level/difference probes) is what matters here, not signal semantics.
- **Fields**: `img_feat1_pca1batch3_us_day1`, `img_feat1_pca6_us_day1`
- **Implementation Example**: `quantile(ts_arg_min(ts_backfill({img_feat1_pca6_us_day1}, 66), 10))`
- **Direction**: High → long.
- **Why not crowded**: ts_arg timing features are outside the saturated level/revision probe family.

**Concept**: Cross spread img_feat1_pca1batch3_us_day1 minus img_feat1_pca6_us_day1
- **Mechanism**: Generic Path-1 diversity concept for dry-run extensibility validation on dataset chart_cnn_alpha. The operator topology (ts_arg_max/ts_arg_min timing features plus level/difference probes) is what matters here, not signal semantics.
- **Fields**: `img_feat1_pca1batch3_us_day1`, `img_feat1_pca6_us_day1`
- **Implementation Example**: `quantile(subtract(ts_backfill({img_feat1_pca1batch3_us_day1}, 66), ts_backfill({img_feat1_pca6_us_day1}, 66)))`
- **Direction**: High → long.
- **Why not crowded**: ts_arg timing features are outside the saturated level/revision probe family.

**Concept**: Level rank of img_feat1_pca6_us_day1
- **Mechanism**: Generic Path-1 diversity concept for dry-run extensibility validation on dataset chart_cnn_alpha. The operator topology (ts_arg_max/ts_arg_min timing features plus level/difference probes) is what matters here, not signal semantics.
- **Fields**: `img_feat1_pca1batch3_us_day1`, `img_feat1_pca6_us_day1`
- **Implementation Example**: `quantile(rank(ts_backfill({img_feat1_pca6_us_day1}, 66)))`
- **Direction**: High → long.
- **Why not crowded**: ts_arg timing features are outside the saturated level/revision probe family.
