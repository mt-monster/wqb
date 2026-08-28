**Dataset**: model354  
**Region**: USA  
**Delay**: 1  
**Universe**: TOP3000

**Concept**: Recency of peak conviction on mdl354_group_pt11yf_dlyspe (ts_arg_max, 20d)
- **Mechanism**: Generic Path-1 diversity concept for dry-run extensibility validation on dataset model354. The operator topology (ts_arg_max/ts_arg_min timing features plus level/difference probes) is what matters here, not signal semantics.
- **Fields**: `mdl354_group_pt11yf_dlyspe`, `mdl354_group_pt11yf_ep`
- **Implementation Example**: `quantile(-ts_arg_max(ts_backfill(vec_avg({mdl354_group_pt11yf_dlyspe}), 66), 20))`
- **Direction**: High → long.
- **Why not crowded**: ts_arg timing features are outside the saturated level/revision probe family.

**Concept**: Recency of trough conviction on mdl354_group_pt11yf_dlyspe (ts_arg_min, 20d)
- **Mechanism**: Generic Path-1 diversity concept for dry-run extensibility validation on dataset model354. The operator topology (ts_arg_max/ts_arg_min timing features plus level/difference probes) is what matters here, not signal semantics.
- **Fields**: `mdl354_group_pt11yf_dlyspe`, `mdl354_group_pt11yf_ep`
- **Implementation Example**: `quantile(ts_arg_min(ts_backfill(vec_avg({mdl354_group_pt11yf_dlyspe}), 66), 20))`
- **Direction**: High → long.
- **Why not crowded**: ts_arg timing features are outside the saturated level/revision probe family.

**Concept**: Revision of mdl354_group_pt11yf_dlyspe (5-day change)
- **Mechanism**: Generic Path-1 diversity concept for dry-run extensibility validation on dataset model354. The operator topology (ts_arg_max/ts_arg_min timing features plus level/difference probes) is what matters here, not signal semantics.
- **Fields**: `mdl354_group_pt11yf_dlyspe`, `mdl354_group_pt11yf_ep`
- **Implementation Example**: `quantile(ts_delta(ts_backfill(vec_avg({mdl354_group_pt11yf_dlyspe}), 66), 5))`
- **Direction**: High → long.
- **Why not crowded**: ts_arg timing features are outside the saturated level/revision probe family.

**Concept**: Recency of peak signal on mdl354_group_pt11yf_ep (ts_arg_max, 10d)
- **Mechanism**: Generic Path-1 diversity concept for dry-run extensibility validation on dataset model354. The operator topology (ts_arg_max/ts_arg_min timing features plus level/difference probes) is what matters here, not signal semantics.
- **Fields**: `mdl354_group_pt11yf_dlyspe`, `mdl354_group_pt11yf_ep`
- **Implementation Example**: `quantile(-ts_arg_max(ts_backfill(vec_avg({mdl354_group_pt11yf_ep}), 66), 10))`
- **Direction**: High → long.
- **Why not crowded**: ts_arg timing features are outside the saturated level/revision probe family.

**Concept**: Recency of trough signal on mdl354_group_pt11yf_ep (ts_arg_min, 10d)
- **Mechanism**: Generic Path-1 diversity concept for dry-run extensibility validation on dataset model354. The operator topology (ts_arg_max/ts_arg_min timing features plus level/difference probes) is what matters here, not signal semantics.
- **Fields**: `mdl354_group_pt11yf_dlyspe`, `mdl354_group_pt11yf_ep`
- **Implementation Example**: `quantile(ts_arg_min(ts_backfill(vec_avg({mdl354_group_pt11yf_ep}), 66), 10))`
- **Direction**: High → long.
- **Why not crowded**: ts_arg timing features are outside the saturated level/revision probe family.

**Concept**: Cross spread mdl354_group_pt11yf_dlyspe minus mdl354_group_pt11yf_ep
- **Mechanism**: Generic Path-1 diversity concept for dry-run extensibility validation on dataset model354. The operator topology (ts_arg_max/ts_arg_min timing features plus level/difference probes) is what matters here, not signal semantics.
- **Fields**: `mdl354_group_pt11yf_dlyspe`, `mdl354_group_pt11yf_ep`
- **Implementation Example**: `quantile(subtract(ts_backfill(vec_avg({mdl354_group_pt11yf_dlyspe}), 66), ts_backfill(vec_avg({mdl354_group_pt11yf_ep}), 66)))`
- **Direction**: High → long.
- **Why not crowded**: ts_arg timing features are outside the saturated level/revision probe family.

**Concept**: Level rank of mdl354_group_pt11yf_ep
- **Mechanism**: Generic Path-1 diversity concept for dry-run extensibility validation on dataset model354. The operator topology (ts_arg_max/ts_arg_min timing features plus level/difference probes) is what matters here, not signal semantics.
- **Fields**: `mdl354_group_pt11yf_dlyspe`, `mdl354_group_pt11yf_ep`
- **Implementation Example**: `quantile(rank(ts_backfill(vec_avg({mdl354_group_pt11yf_ep}), 66)))`
- **Direction**: High → long.
- **Why not crowded**: ts_arg timing features are outside the saturated level/revision probe family.
