# News / Sentiment Dataset Portfolio (Tiering)

> **Snapshot, 2026-04-23 — a candidate source, not a routing rule.** Used by
> `Claude/skills/brain-alpha-research-news-sentiment`. There is no refresh command
> (`wqb news-refresh-portfolio` never existed): when you need current numbers read
> `mcp__wq-brain-http__get_datasets(category="news"|"sentiment", region, delay, universe)`
> (fieldCount / alphaCount / pyramidMultiplier) and RA step 2's `recommend_datasets`;
> those override every number below. Route only after the dead-end / cross-region-weak /
> lit-pyramid checks in the skill.

## Selection criteria
- **Tier A (candidate for cold-start):** `fieldCount ≥ 50`, `pyramidMultiplier ≥ 1.2`,
  `alphaCount / fieldCount ≤ 5` (community not yet saturated), and typed-catalog coverage
  usable (RA step 3 completion: ≥ 10 fields with coverage > 0).
- **Tier B (saturated):** `alphaCount` in the tens-to-hundreds of thousands — require
  highly-asymmetric structures to clear `ProdCorr < 0.70`.

## Tier A — candidates (each still needs the routing checks)
| Dataset | Notes |
|---------|-------|
| `news_transformer_scores` | transformer-derived, low alphaCount |
| `sentiment22` | strong fieldCount |
| `sentiment23` | strong fieldCount |
| `event_return_model` | event-anchored |
| `news94` | good balance |
| `news29` | good balance |
| `news73` | good balance |
| `news23` | good balance |
| `news59` | Tier-A anchor (KOR sweet spot, sharpe ~0.60) |
| `creator_signal_perf` | creator/social signal |
| `twitter_sentiment_l2` | L2 social sentiment |

## Tier B — saturated, flag before mining
| Dataset | alphaCount | Why hard |
|---------|-----------|----------|
| `news12` | ~120K α | exhausted template space (USA/D1 microstructure) |
| `news18` | ~40K α | heavy competition |
| `socialmedia12` | ~43K α | heavy competition |

> On Tier B, tell the user, then switch to the **hypothesis-first** workflow
> (`Claude/skills/brain-alpha-research-hypothesis-first`; RA step 2 constraint 6) instead
> of template sampling — template sampling on ≥10K-α datasets produces pseudo-signals
> (UNITS WARN, field-substitutable).

## Operational notes
- Per-dataset overrides for the 5-family classifier live in
  `src/wqb/research/news_field_classifier.py::DATASET_OVERRIDES` — today only `news12`
  has one; every other dataset goes through the keyword rules (review the result).
- Always re-check coverage: fields with `coverage < 0.4` need `ts_backfill` /
  `group_backfill` or must be dropped regardless of tier.
