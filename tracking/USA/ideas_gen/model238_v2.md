**Dataset**: model238  
**Region**: USA  
**Delay**: 1  
**Universe**: TOP3000

**Concept**: Recency of peak conviction on country_relative_investment_rank (ts_arg_max, 20d)
- **Mechanism**: Generic Path-1 diversity concept for dry-run extensibility validation on dataset model238. The operator topology (ts_arg_max/ts_arg_min timing features plus level/difference probes) is what matters here, not signal semantics.
- **Fields**: `country_relative_investment_rank`, `global_institutional_preference_rank`
- **Implementation Example**: `quantile(-ts_arg_max(ts_backfill({country_relative_investment_rank}, 66), 20))`
- **Direction**: High → long.
- **Why not crowded**: ts_arg timing features are outside the saturated level/revision probe family.

**Concept**: Recency of trough conviction on country_relative_investment_rank (ts_arg_min, 20d)
- **Mechanism**: Generic Path-1 diversity concept for dry-run extensibility validation on dataset model238. The operator topology (ts_arg_max/ts_arg_min timing features plus level/difference probes) is what matters here, not signal semantics.
- **Fields**: `country_relative_investment_rank`, `global_institutional_preference_rank`
- **Implementation Example**: `quantile(ts_arg_min(ts_backfill({country_relative_investment_rank}, 66), 20))`
- **Direction**: High → long.
- **Why not crowded**: ts_arg timing features are outside the saturated level/revision probe family.

**Concept**: Revision of country_relative_investment_rank (5-day change)
- **Mechanism**: Generic Path-1 diversity concept for dry-run extensibility validation on dataset model238. The operator topology (ts_arg_max/ts_arg_min timing features plus level/difference probes) is what matters here, not signal semantics.
- **Fields**: `country_relative_investment_rank`, `global_institutional_preference_rank`
- **Implementation Example**: `quantile(ts_delta(ts_backfill({country_relative_investment_rank}, 66), 5))`
- **Direction**: High → long.
- **Why not crowded**: ts_arg timing features are outside the saturated level/revision probe family.

**Concept**: Recency of peak signal on global_institutional_preference_rank (ts_arg_max, 10d)
- **Mechanism**: Generic Path-1 diversity concept for dry-run extensibility validation on dataset model238. The operator topology (ts_arg_max/ts_arg_min timing features plus level/difference probes) is what matters here, not signal semantics.
- **Fields**: `country_relative_investment_rank`, `global_institutional_preference_rank`
- **Implementation Example**: `quantile(-ts_arg_max(ts_backfill({global_institutional_preference_rank}, 66), 10))`
- **Direction**: High → long.
- **Why not crowded**: ts_arg timing features are outside the saturated level/revision probe family.

**Concept**: Recency of trough signal on global_institutional_preference_rank (ts_arg_min, 10d)
- **Mechanism**: Generic Path-1 diversity concept for dry-run extensibility validation on dataset model238. The operator topology (ts_arg_max/ts_arg_min timing features plus level/difference probes) is what matters here, not signal semantics.
- **Fields**: `country_relative_investment_rank`, `global_institutional_preference_rank`
- **Implementation Example**: `quantile(ts_arg_min(ts_backfill({global_institutional_preference_rank}, 66), 10))`
- **Direction**: High → long.
- **Why not crowded**: ts_arg timing features are outside the saturated level/revision probe family.

**Concept**: Cross spread country_relative_investment_rank minus global_institutional_preference_rank
- **Mechanism**: Generic Path-1 diversity concept for dry-run extensibility validation on dataset model238. The operator topology (ts_arg_max/ts_arg_min timing features plus level/difference probes) is what matters here, not signal semantics.
- **Fields**: `country_relative_investment_rank`, `global_institutional_preference_rank`
- **Implementation Example**: `quantile(subtract(ts_backfill({country_relative_investment_rank}, 66), ts_backfill({global_institutional_preference_rank}, 66)))`
- **Direction**: High → long.
- **Why not crowded**: ts_arg timing features are outside the saturated level/revision probe family.

**Concept**: Level rank of global_institutional_preference_rank
- **Mechanism**: Generic Path-1 diversity concept for dry-run extensibility validation on dataset model238. The operator topology (ts_arg_max/ts_arg_min timing features plus level/difference probes) is what matters here, not signal semantics.
- **Fields**: `country_relative_investment_rank`, `global_institutional_preference_rank`
- **Implementation Example**: `quantile(rank(ts_backfill({global_institutional_preference_rank}, 66)))`
- **Direction**: High → long.
- **Why not crowded**: ts_arg timing features are outside the saturated level/revision probe family.
