# analyst9 Skeleton Ideas — Breakout Recipe Injection (A/B arm: skeleton-constrained GEM)

**Dataset**: analyst9
**Region**: GBR
**Delay**: 1


**Concept**: Momentum-gated monthly improvement of a slow-moving analyst consensus level
- **Implementation Example**: `trade_when(greater(five_day_total_return_dlr2, 0.0135), group_rank(ts_delta(ts_backfill({variable}, 66), 22), sector), -1)`
- **Rationale**: Consensus levels are already priced; trading their MONTHLY improvement, gated on short-term momentum confirmation, strips production-pool overlap. This exact structure passed prod gate in GBR (prod 0.848 to 0.6986 with threshold 0.0135). Prefer slow-moving fields with low alphaCount for the {variable} slot.

**Concept**: Ungated monthly improvement of slow-moving consensus estimate
- **Implementation Example**: `group_rank(ts_delta(ts_backfill({variable}, 66), 22), sector)`
- **Rationale**: Delta form isolates the change signal from the level signal; levels are consumed by the production pool but monthly changes retain residual alpha. Works best on slow-moving estimate fields.

**Concept**: Backfill level form for very slow-moving fields
- **Implementation Example**: `group_rank(ts_backfill({variable}, 66), sector)`
- **Rationale**: For extremely slow-moving skill/consistency-like fields the level itself is not yet priced; ts_backfill widens data visibility and the level form beat delta form in GBR consistency experiments (S 0.80 vs -0.19).

**Concept**: Gated level form on consensus breadth fields
- **Implementation Example**: `trade_when(greater(five_day_total_return_dlr2, 0.0135), group_rank({variable}, sector), -1)`
- **Rationale**: Breadth/coverage fields (analyst counts) change slowly and encode attention; gating the level on momentum separates attention-driven drift from static coverage.

**Concept**: Revision-balance count signal from analyst revision counts
- **Implementation Example**: `group_rank(vec_avg({variable}), sector)`
- **Rationale**: Up/down revision counts encode directional analyst action; aggregated revision pressure predicts near-term drift. Use vec_avg on VECTOR fields; do not mix with other fields via weights.

Settings constraint for all variants: decay=12, truncation=0.1, neutralization=SUBINDUSTRY, region=GBR, universe=TOP700, delay=1. NO weighted mixing. VECTOR fields need vec_avg()/vec_max(). operatorCount <= 8.