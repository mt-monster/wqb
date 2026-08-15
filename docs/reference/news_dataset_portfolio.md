# News / Sentiment Dataset Portfolio (Tiering)

> Used by `brain-alpha-research` (step 12) and `brain-alpha-orchestrator` (step 15)
> to route cold-start work. Refresh with `wqb news-refresh-portfolio` when pyramid
> multipliers change.

## Selection criteria
- **Tier A (preferred cold-start):** `fieldCount ≥ 50`, `pyramidMultiplier ≥ 1.2`,
  `alphaCount` low (community not yet saturated).
- **Tier B (saturated):** `alphaCount` in the tens-to-hundreds of thousands — require
  highly-asymmetric structures to clear `ProdCorr < 0.70`.

## Tier A — route new work here
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

> On Tier B, switch to the **hypothesis-first** workflow (see
> `researcher_workflow/README.md`) instead of template sampling — template sampling
> on ≥10K-α datasets produces pseudo-signals (UNITS WARN, field-substitutable).

## Operational notes
- Per-dataset overrides (news12/news29/news73/news94) for the 5-family classifier live
  in `src/wqb/research/news_field_classifier.py`.
- Always re-check coverage: fields with `coverage < 0.4` need `ts_backfill` /
  `group_backfill` or must be dropped regardless of tier.
