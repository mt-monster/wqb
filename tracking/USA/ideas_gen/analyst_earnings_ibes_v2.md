**Dataset**: analyst_earnings_ibes  
**Region**: USA  
**Delay**: 1  
**Universe**: TOP3000

**Concept**: Recency of peak conviction on closing_price_dlr1 (ts_arg_max, 20d)
- **Mechanism**: Generic Path-1 diversity concept for dry-run extensibility validation on dataset analyst_earnings_ibes. The operator topology (ts_arg_max/ts_arg_min timing features plus level/difference probes) is what matters here, not signal semantics.
- **Fields**: `closing_price_dlr1`, `closing_price_dlr2`
- **Implementation Example**: `quantile(-ts_arg_max(ts_backfill({closing_price_dlr1}, 66), 20))`
- **Direction**: High → long.
- **Why not crowded**: ts_arg timing features are outside the saturated level/revision probe family.

**Concept**: Recency of trough conviction on closing_price_dlr1 (ts_arg_min, 20d)
- **Mechanism**: Generic Path-1 diversity concept for dry-run extensibility validation on dataset analyst_earnings_ibes. The operator topology (ts_arg_max/ts_arg_min timing features plus level/difference probes) is what matters here, not signal semantics.
- **Fields**: `closing_price_dlr1`, `closing_price_dlr2`
- **Implementation Example**: `quantile(ts_arg_min(ts_backfill({closing_price_dlr1}, 66), 20))`
- **Direction**: High → long.
- **Why not crowded**: ts_arg timing features are outside the saturated level/revision probe family.

**Concept**: Revision of closing_price_dlr1 (5-day change)
- **Mechanism**: Generic Path-1 diversity concept for dry-run extensibility validation on dataset analyst_earnings_ibes. The operator topology (ts_arg_max/ts_arg_min timing features plus level/difference probes) is what matters here, not signal semantics.
- **Fields**: `closing_price_dlr1`, `closing_price_dlr2`
- **Implementation Example**: `quantile(ts_delta(ts_backfill({closing_price_dlr1}, 66), 5))`
- **Direction**: High → long.
- **Why not crowded**: ts_arg timing features are outside the saturated level/revision probe family.

**Concept**: Recency of peak signal on closing_price_dlr2 (ts_arg_max, 10d)
- **Mechanism**: Generic Path-1 diversity concept for dry-run extensibility validation on dataset analyst_earnings_ibes. The operator topology (ts_arg_max/ts_arg_min timing features plus level/difference probes) is what matters here, not signal semantics.
- **Fields**: `closing_price_dlr1`, `closing_price_dlr2`
- **Implementation Example**: `quantile(-ts_arg_max(ts_backfill({closing_price_dlr2}, 66), 10))`
- **Direction**: High → long.
- **Why not crowded**: ts_arg timing features are outside the saturated level/revision probe family.

**Concept**: Recency of trough signal on closing_price_dlr2 (ts_arg_min, 10d)
- **Mechanism**: Generic Path-1 diversity concept for dry-run extensibility validation on dataset analyst_earnings_ibes. The operator topology (ts_arg_max/ts_arg_min timing features plus level/difference probes) is what matters here, not signal semantics.
- **Fields**: `closing_price_dlr1`, `closing_price_dlr2`
- **Implementation Example**: `quantile(ts_arg_min(ts_backfill({closing_price_dlr2}, 66), 10))`
- **Direction**: High → long.
- **Why not crowded**: ts_arg timing features are outside the saturated level/revision probe family.

**Concept**: Cross spread closing_price_dlr1 minus closing_price_dlr2
- **Mechanism**: Generic Path-1 diversity concept for dry-run extensibility validation on dataset analyst_earnings_ibes. The operator topology (ts_arg_max/ts_arg_min timing features plus level/difference probes) is what matters here, not signal semantics.
- **Fields**: `closing_price_dlr1`, `closing_price_dlr2`
- **Implementation Example**: `quantile(subtract(ts_backfill({closing_price_dlr1}, 66), ts_backfill({closing_price_dlr2}, 66)))`
- **Direction**: High → long.
- **Why not crowded**: ts_arg timing features are outside the saturated level/revision probe family.

**Concept**: Level rank of closing_price_dlr2
- **Mechanism**: Generic Path-1 diversity concept for dry-run extensibility validation on dataset analyst_earnings_ibes. The operator topology (ts_arg_max/ts_arg_min timing features plus level/difference probes) is what matters here, not signal semantics.
- **Fields**: `closing_price_dlr1`, `closing_price_dlr2`
- **Implementation Example**: `quantile(rank(ts_backfill({closing_price_dlr2}, 66)))`
- **Direction**: High → long.
- **Why not crowded**: ts_arg timing features are outside the saturated level/revision probe family.
