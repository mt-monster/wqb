**Dataset**: chart_return_model  
**Region**: USA  
**Delay**: 1  
**Universe**: TOP3000

**Concept**: Recency of peak conviction on fifth_ask_price_int60 (ts_arg_max, 20d)
- **Mechanism**: Generic Path-1 diversity concept for dry-run extensibility validation on dataset chart_return_model. The operator topology (ts_arg_max/ts_arg_min timing features plus level/difference probes) is what matters here, not signal semantics.
- **Fields**: `fifth_ask_price_int60`, `fifth_bid_price_int60`
- **Implementation Example**: `quantile(-ts_arg_max(ts_backfill({fifth_ask_price_int60}, 66), 20))`
- **Direction**: High → long.
- **Why not crowded**: ts_arg timing features are outside the saturated level/revision probe family.

**Concept**: Recency of trough conviction on fifth_ask_price_int60 (ts_arg_min, 20d)
- **Mechanism**: Generic Path-1 diversity concept for dry-run extensibility validation on dataset chart_return_model. The operator topology (ts_arg_max/ts_arg_min timing features plus level/difference probes) is what matters here, not signal semantics.
- **Fields**: `fifth_ask_price_int60`, `fifth_bid_price_int60`
- **Implementation Example**: `quantile(ts_arg_min(ts_backfill({fifth_ask_price_int60}, 66), 20))`
- **Direction**: High → long.
- **Why not crowded**: ts_arg timing features are outside the saturated level/revision probe family.

**Concept**: Revision of fifth_ask_price_int60 (5-day change)
- **Mechanism**: Generic Path-1 diversity concept for dry-run extensibility validation on dataset chart_return_model. The operator topology (ts_arg_max/ts_arg_min timing features plus level/difference probes) is what matters here, not signal semantics.
- **Fields**: `fifth_ask_price_int60`, `fifth_bid_price_int60`
- **Implementation Example**: `quantile(ts_delta(ts_backfill({fifth_ask_price_int60}, 66), 5))`
- **Direction**: High → long.
- **Why not crowded**: ts_arg timing features are outside the saturated level/revision probe family.

**Concept**: Recency of peak signal on fifth_bid_price_int60 (ts_arg_max, 10d)
- **Mechanism**: Generic Path-1 diversity concept for dry-run extensibility validation on dataset chart_return_model. The operator topology (ts_arg_max/ts_arg_min timing features plus level/difference probes) is what matters here, not signal semantics.
- **Fields**: `fifth_ask_price_int60`, `fifth_bid_price_int60`
- **Implementation Example**: `quantile(-ts_arg_max(ts_backfill({fifth_bid_price_int60}, 66), 10))`
- **Direction**: High → long.
- **Why not crowded**: ts_arg timing features are outside the saturated level/revision probe family.

**Concept**: Recency of trough signal on fifth_bid_price_int60 (ts_arg_min, 10d)
- **Mechanism**: Generic Path-1 diversity concept for dry-run extensibility validation on dataset chart_return_model. The operator topology (ts_arg_max/ts_arg_min timing features plus level/difference probes) is what matters here, not signal semantics.
- **Fields**: `fifth_ask_price_int60`, `fifth_bid_price_int60`
- **Implementation Example**: `quantile(ts_arg_min(ts_backfill({fifth_bid_price_int60}, 66), 10))`
- **Direction**: High → long.
- **Why not crowded**: ts_arg timing features are outside the saturated level/revision probe family.

**Concept**: Cross spread fifth_ask_price_int60 minus fifth_bid_price_int60
- **Mechanism**: Generic Path-1 diversity concept for dry-run extensibility validation on dataset chart_return_model. The operator topology (ts_arg_max/ts_arg_min timing features plus level/difference probes) is what matters here, not signal semantics.
- **Fields**: `fifth_ask_price_int60`, `fifth_bid_price_int60`
- **Implementation Example**: `quantile(subtract(ts_backfill({fifth_ask_price_int60}, 66), ts_backfill({fifth_bid_price_int60}, 66)))`
- **Direction**: High → long.
- **Why not crowded**: ts_arg timing features are outside the saturated level/revision probe family.

**Concept**: Level rank of fifth_bid_price_int60
- **Mechanism**: Generic Path-1 diversity concept for dry-run extensibility validation on dataset chart_return_model. The operator topology (ts_arg_max/ts_arg_min timing features plus level/difference probes) is what matters here, not signal semantics.
- **Fields**: `fifth_ask_price_int60`, `fifth_bid_price_int60`
- **Implementation Example**: `quantile(rank(ts_backfill({fifth_bid_price_int60}, 66)))`
- **Direction**: High → long.
- **Why not crowded**: ts_arg timing features are outside the saturated level/revision probe family.
