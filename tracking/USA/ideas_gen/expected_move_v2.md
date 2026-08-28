**Dataset**: expected_move  
**Region**: USA  
**Delay**: 1  
**Universe**: TOP3000

**Concept**: Recency of peak conviction on daily_option_contracts_traded_7 (ts_arg_max, 20d)
- **Mechanism**: Generic Path-1 diversity concept for dry-run extensibility validation on dataset expected_move. The operator topology (ts_arg_max/ts_arg_min timing features plus level/difference probes) is what matters here, not signal semantics.
- **Fields**: `daily_option_contracts_traded_7`, `straddle_move_percent_7`
- **Implementation Example**: `quantile(-ts_arg_max(ts_backfill({daily_option_contracts_traded_7}, 66), 20))`
- **Direction**: High → long.
- **Why not crowded**: ts_arg timing features are outside the saturated level/revision probe family.

**Concept**: Recency of trough conviction on daily_option_contracts_traded_7 (ts_arg_min, 20d)
- **Mechanism**: Generic Path-1 diversity concept for dry-run extensibility validation on dataset expected_move. The operator topology (ts_arg_max/ts_arg_min timing features plus level/difference probes) is what matters here, not signal semantics.
- **Fields**: `daily_option_contracts_traded_7`, `straddle_move_percent_7`
- **Implementation Example**: `quantile(ts_arg_min(ts_backfill({daily_option_contracts_traded_7}, 66), 20))`
- **Direction**: High → long.
- **Why not crowded**: ts_arg timing features are outside the saturated level/revision probe family.

**Concept**: Revision of daily_option_contracts_traded_7 (5-day change)
- **Mechanism**: Generic Path-1 diversity concept for dry-run extensibility validation on dataset expected_move. The operator topology (ts_arg_max/ts_arg_min timing features plus level/difference probes) is what matters here, not signal semantics.
- **Fields**: `daily_option_contracts_traded_7`, `straddle_move_percent_7`
- **Implementation Example**: `quantile(ts_delta(ts_backfill({daily_option_contracts_traded_7}, 66), 5))`
- **Direction**: High → long.
- **Why not crowded**: ts_arg timing features are outside the saturated level/revision probe family.

**Concept**: Recency of peak signal on straddle_move_percent_7 (ts_arg_max, 10d)
- **Mechanism**: Generic Path-1 diversity concept for dry-run extensibility validation on dataset expected_move. The operator topology (ts_arg_max/ts_arg_min timing features plus level/difference probes) is what matters here, not signal semantics.
- **Fields**: `daily_option_contracts_traded_7`, `straddle_move_percent_7`
- **Implementation Example**: `quantile(-ts_arg_max(ts_backfill({straddle_move_percent_7}, 66), 10))`
- **Direction**: High → long.
- **Why not crowded**: ts_arg timing features are outside the saturated level/revision probe family.

**Concept**: Recency of trough signal on straddle_move_percent_7 (ts_arg_min, 10d)
- **Mechanism**: Generic Path-1 diversity concept for dry-run extensibility validation on dataset expected_move. The operator topology (ts_arg_max/ts_arg_min timing features plus level/difference probes) is what matters here, not signal semantics.
- **Fields**: `daily_option_contracts_traded_7`, `straddle_move_percent_7`
- **Implementation Example**: `quantile(ts_arg_min(ts_backfill({straddle_move_percent_7}, 66), 10))`
- **Direction**: High → long.
- **Why not crowded**: ts_arg timing features are outside the saturated level/revision probe family.

**Concept**: Cross spread daily_option_contracts_traded_7 minus straddle_move_percent_7
- **Mechanism**: Generic Path-1 diversity concept for dry-run extensibility validation on dataset expected_move. The operator topology (ts_arg_max/ts_arg_min timing features plus level/difference probes) is what matters here, not signal semantics.
- **Fields**: `daily_option_contracts_traded_7`, `straddle_move_percent_7`
- **Implementation Example**: `quantile(subtract(ts_backfill({daily_option_contracts_traded_7}, 66), ts_backfill({straddle_move_percent_7}, 66)))`
- **Direction**: High → long.
- **Why not crowded**: ts_arg timing features are outside the saturated level/revision probe family.

**Concept**: Level rank of straddle_move_percent_7
- **Mechanism**: Generic Path-1 diversity concept for dry-run extensibility validation on dataset expected_move. The operator topology (ts_arg_max/ts_arg_min timing features plus level/difference probes) is what matters here, not signal semantics.
- **Fields**: `daily_option_contracts_traded_7`, `straddle_move_percent_7`
- **Implementation Example**: `quantile(rank(ts_backfill({straddle_move_percent_7}, 66)))`
- **Direction**: High → long.
- **Why not crowded**: ts_arg timing features are outside the saturated level/revision probe family.
