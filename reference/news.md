# news12 Field Reference (USA/D1 microstructure)

> Referenced by `brain-alpha-research` (step 11). `news12` on USA/D1 has **no
> tone/polarity scalar** — it is a price-reaction microstructure dataset keyed on news
> events (RavenPack-style). The generic five-family taxonomy applies with the
> remappings below.

## 1. R/A/V/M/T field families
| Code | Meaning | Example fields |
|------|---------|----------------|
| **R** (reaction) | price reaction to news | `news_pct_*min`, `news_max_up_ret`, `news_max_dn_ret` |
| **A** (attention) | relevance / volume / mention | `news_vol_*`, mention count, relevance score |
| **V** (range/volatility-context) | dispersion / uncertainty | `news_vol_stddev` |
| **M** (microstructure/context) | event trigger proxy | `nws12_mainz_vol_ratio`, `atrratio` |
| **T** (duration-of-reaction) | how long the reaction lasts | `news_ton_last` (duration proxy) |

## 2. Remapping to five-family taxonomy
| Code | → Family |
|------|----------|
| R | **direction** |
| A | **attention** |
| V | **dispersion** |
| M | **event_type** (news12 lacks true event codes → use `nws12_mainz_vol_ratio` / `atrratio` as synthetic triggers) |
| T | **event_type** |

## 3. REACTION-centric motifs → 6-bucket mapping
| Motif | Bucket(s) |
|-------|-----------|
| M1 | Surprise |
| M2 | Event-conditioned |
| M3 | Surprise |
| M4 | Surprise or Change |
| M5 | Event-conditioned |
| M6 | Event-conditioned |

## 4. Mining notes
- `news12` is Tier B (saturated, ~120K α) → prefer hypothesis-first workflow
  (`researcher_workflow/README.md`), not template sampling.
- No tone scalar ⇒ do not build "sentiment polarity" alphas; use reaction magnitude
  and attention gating instead.
- Coverage < 0.4 fields (typical for sparse event fields) need `ts_backfill` /
  `group_backfill` or must be dropped.
