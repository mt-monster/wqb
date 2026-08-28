**Dataset**: other623  
**Region**: USA  
**Delay**: 1  
**Universe**: TOP3000

**Concept**: Recency of peak conviction on oth623_comp_textblob_polarity (ts_arg_max, 20d)
- **Mechanism**: Generic Path-1 diversity concept for dry-run extensibility validation on dataset other623. The operator topology (ts_arg_max/ts_arg_min timing features plus level/difference probes) is what matters here, not signal semantics.
- **Fields**: `oth623_comp_textblob_polarity`, `oth623_comp_textblob_subjectivity`
- **Implementation Example**: `quantile(-ts_arg_max(ts_backfill(vec_avg({oth623_comp_textblob_polarity}), 66), 20))`
- **Direction**: High → long.
- **Why not crowded**: ts_arg timing features are outside the saturated level/revision probe family.

**Concept**: Recency of trough conviction on oth623_comp_textblob_polarity (ts_arg_min, 20d)
- **Mechanism**: Generic Path-1 diversity concept for dry-run extensibility validation on dataset other623. The operator topology (ts_arg_max/ts_arg_min timing features plus level/difference probes) is what matters here, not signal semantics.
- **Fields**: `oth623_comp_textblob_polarity`, `oth623_comp_textblob_subjectivity`
- **Implementation Example**: `quantile(ts_arg_min(ts_backfill(vec_avg({oth623_comp_textblob_polarity}), 66), 20))`
- **Direction**: High → long.
- **Why not crowded**: ts_arg timing features are outside the saturated level/revision probe family.

**Concept**: Revision of oth623_comp_textblob_polarity (5-day change)
- **Mechanism**: Generic Path-1 diversity concept for dry-run extensibility validation on dataset other623. The operator topology (ts_arg_max/ts_arg_min timing features plus level/difference probes) is what matters here, not signal semantics.
- **Fields**: `oth623_comp_textblob_polarity`, `oth623_comp_textblob_subjectivity`
- **Implementation Example**: `quantile(ts_delta(ts_backfill(vec_avg({oth623_comp_textblob_polarity}), 66), 5))`
- **Direction**: High → long.
- **Why not crowded**: ts_arg timing features are outside the saturated level/revision probe family.

**Concept**: Recency of peak signal on oth623_comp_textblob_subjectivity (ts_arg_max, 10d)
- **Mechanism**: Generic Path-1 diversity concept for dry-run extensibility validation on dataset other623. The operator topology (ts_arg_max/ts_arg_min timing features plus level/difference probes) is what matters here, not signal semantics.
- **Fields**: `oth623_comp_textblob_polarity`, `oth623_comp_textblob_subjectivity`
- **Implementation Example**: `quantile(-ts_arg_max(ts_backfill(vec_avg({oth623_comp_textblob_subjectivity}), 66), 10))`
- **Direction**: High → long.
- **Why not crowded**: ts_arg timing features are outside the saturated level/revision probe family.

**Concept**: Recency of trough signal on oth623_comp_textblob_subjectivity (ts_arg_min, 10d)
- **Mechanism**: Generic Path-1 diversity concept for dry-run extensibility validation on dataset other623. The operator topology (ts_arg_max/ts_arg_min timing features plus level/difference probes) is what matters here, not signal semantics.
- **Fields**: `oth623_comp_textblob_polarity`, `oth623_comp_textblob_subjectivity`
- **Implementation Example**: `quantile(ts_arg_min(ts_backfill(vec_avg({oth623_comp_textblob_subjectivity}), 66), 10))`
- **Direction**: High → long.
- **Why not crowded**: ts_arg timing features are outside the saturated level/revision probe family.

**Concept**: Cross spread oth623_comp_textblob_polarity minus oth623_comp_textblob_subjectivity
- **Mechanism**: Generic Path-1 diversity concept for dry-run extensibility validation on dataset other623. The operator topology (ts_arg_max/ts_arg_min timing features plus level/difference probes) is what matters here, not signal semantics.
- **Fields**: `oth623_comp_textblob_polarity`, `oth623_comp_textblob_subjectivity`
- **Implementation Example**: `quantile(subtract(ts_backfill(vec_avg({oth623_comp_textblob_polarity}), 66), ts_backfill(vec_avg({oth623_comp_textblob_subjectivity}), 66)))`
- **Direction**: High → long.
- **Why not crowded**: ts_arg timing features are outside the saturated level/revision probe family.

**Concept**: Level rank of oth623_comp_textblob_subjectivity
- **Mechanism**: Generic Path-1 diversity concept for dry-run extensibility validation on dataset other623. The operator topology (ts_arg_max/ts_arg_min timing features plus level/difference probes) is what matters here, not signal semantics.
- **Fields**: `oth623_comp_textblob_polarity`, `oth623_comp_textblob_subjectivity`
- **Implementation Example**: `quantile(rank(ts_backfill(vec_avg({oth623_comp_textblob_subjectivity}), 66)))`
- **Direction**: High → long.
- **Why not crowded**: ts_arg timing features are outside the saturated level/revision probe family.
