**Dataset**: intraday_pv_feats  
**Region**: USA  
**Delay**: 1  
**Universe**: TOP3000

**Concept**: Recency of peak conviction on kurtosis_last_trade_price_interval (ts_arg_max, 20d)
- **Mechanism**: Generic Path-1 diversity concept for dry-run extensibility validation on dataset intraday_pv_feats. The operator topology (ts_arg_max/ts_arg_min timing features plus level/difference probes) is what matters here, not signal semantics.
- **Fields**: `kurtosis_last_trade_price_interval`, `last_trade_price_30m_post_open`
- **Implementation Example**: `quantile(-ts_arg_max(ts_backfill({kurtosis_last_trade_price_interval}, 66), 20))`
- **Direction**: High → long.
- **Why not crowded**: ts_arg timing features are outside the saturated level/revision probe family.

**Concept**: Recency of trough conviction on kurtosis_last_trade_price_interval (ts_arg_min, 20d)
- **Mechanism**: Generic Path-1 diversity concept for dry-run extensibility validation on dataset intraday_pv_feats. The operator topology (ts_arg_max/ts_arg_min timing features plus level/difference probes) is what matters here, not signal semantics.
- **Fields**: `kurtosis_last_trade_price_interval`, `last_trade_price_30m_post_open`
- **Implementation Example**: `quantile(ts_arg_min(ts_backfill({kurtosis_last_trade_price_interval}, 66), 20))`
- **Direction**: High → long.
- **Why not crowded**: ts_arg timing features are outside the saturated level/revision probe family.

**Concept**: Revision of kurtosis_last_trade_price_interval (5-day change)
- **Mechanism**: Generic Path-1 diversity concept for dry-run extensibility validation on dataset intraday_pv_feats. The operator topology (ts_arg_max/ts_arg_min timing features plus level/difference probes) is what matters here, not signal semantics.
- **Fields**: `kurtosis_last_trade_price_interval`, `last_trade_price_30m_post_open`
- **Implementation Example**: `quantile(ts_delta(ts_backfill({kurtosis_last_trade_price_interval}, 66), 5))`
- **Direction**: High → long.
- **Why not crowded**: ts_arg timing features are outside the saturated level/revision probe family.

**Concept**: Recency of peak signal on last_trade_price_30m_post_open (ts_arg_max, 10d)
- **Mechanism**: Generic Path-1 diversity concept for dry-run extensibility validation on dataset intraday_pv_feats. The operator topology (ts_arg_max/ts_arg_min timing features plus level/difference probes) is what matters here, not signal semantics.
- **Fields**: `kurtosis_last_trade_price_interval`, `last_trade_price_30m_post_open`
- **Implementation Example**: `quantile(-ts_arg_max(ts_backfill({last_trade_price_30m_post_open}, 66), 10))`
- **Direction**: High → long.
- **Why not crowded**: ts_arg timing features are outside the saturated level/revision probe family.

**Concept**: Recency of trough signal on last_trade_price_30m_post_open (ts_arg_min, 10d)
- **Mechanism**: Generic Path-1 diversity concept for dry-run extensibility validation on dataset intraday_pv_feats. The operator topology (ts_arg_max/ts_arg_min timing features plus level/difference probes) is what matters here, not signal semantics.
- **Fields**: `kurtosis_last_trade_price_interval`, `last_trade_price_30m_post_open`
- **Implementation Example**: `quantile(ts_arg_min(ts_backfill({last_trade_price_30m_post_open}, 66), 10))`
- **Direction**: High → long.
- **Why not crowded**: ts_arg timing features are outside the saturated level/revision probe family.

**Concept**: Cross spread kurtosis_last_trade_price_interval minus last_trade_price_30m_post_open
- **Mechanism**: Generic Path-1 diversity concept for dry-run extensibility validation on dataset intraday_pv_feats. The operator topology (ts_arg_max/ts_arg_min timing features plus level/difference probes) is what matters here, not signal semantics.
- **Fields**: `kurtosis_last_trade_price_interval`, `last_trade_price_30m_post_open`
- **Implementation Example**: `quantile(subtract(ts_backfill({kurtosis_last_trade_price_interval}, 66), ts_backfill({last_trade_price_30m_post_open}, 66)))`
- **Direction**: High → long.
- **Why not crowded**: ts_arg timing features are outside the saturated level/revision probe family.

**Concept**: Level rank of last_trade_price_30m_post_open
- **Mechanism**: Generic Path-1 diversity concept for dry-run extensibility validation on dataset intraday_pv_feats. The operator topology (ts_arg_max/ts_arg_min timing features plus level/difference probes) is what matters here, not signal semantics.
- **Fields**: `kurtosis_last_trade_price_interval`, `last_trade_price_30m_post_open`
- **Implementation Example**: `quantile(rank(ts_backfill({last_trade_price_30m_post_open}, 66)))`
- **Direction**: High → long.
- **Why not crowded**: ts_arg timing features are outside the saturated level/revision probe family.
