# News Bucket ↔ Field-Family Pairing Map

> Companion to `news_sentiment_playbook.md`. Defines how the five field families
> (§2 of the playbook) pair into the six buckets, and the sampling / rotation rules
> enforced by `src/wqb/search/news_loop.py`.

## 1. Family → Bucket compatibility matrix

| Family | Level | Change | Surprise | Dispersion | Event-cond. | Propagation |
|--------|:-----:|:------:|:--------:|:----------:|:-----------:|:-----------:|
| direction | ○ | ● | ● | ○ | ○ | ◐ |
| attention | ◐ | ● | ◐ | ○ | ● | ◐ |
| dispersion | ○ | ○ | ○ | ● | ○ | ◐ |
| event_type | ○ | ◐ | ● | ○ | ● | ● |
| peer_context | ○ | ◐ | ○ | ● | ○ | ◐ |

● strong · ◐ possible · ○ weak. HIGH-priority buckets (Dispersion / Event-cond. /
Propagation) must be fed by their ● families.

## 2. Bucket sampling (Beta posterior)
The orchestrator samples buckets with a Beta posterior biased toward D / E / P
(Dispersion / Event-conditioned / Propagation) so HIGH-priority coverage is
guaranteed even early in a session. Per-batch draw respects the hard gates
(≥3 buckets, ≥1 HIGH).

## 3. Cross-family field pairing rules (§4 referenced by playbook)
- Pair across families, never 3-from-1.
- `direction × attention` → Surprise / Event-conditioned (attention gates the
  direction signal to anomaly days).
- `dispersion × peer_context` → Dispersion (spread of peer distribution).
- `event_type × direction` → Propagation / Event-conditioned.
- When the single-dataset constraint is soft, prefer pairing a sentiment field with a
  **non-sentiment** input (returns / volume / volatility) — sentiment–price divergence
  is a distinct motif from sentiment–sentiment subtraction.

## 4. VECTOR-field handling
When fields are VECTOR (per-horizon arrays):
- Rotate `vec_op` (e.g. `ts_mean`, `ts_zscore`, `ts_av_diff`, `vec_avg`) so every
  batch uses ≥2 distinct `vec_op`.
- `vec_op` choice is logged for `check_batch` shape-variety enforcement.
- Never summarize a VECTOR field with a scalar op before `vec_avg` / aggregation.

## 5. Event-gated template inclusion
- `P15_EVENT_CONDITIONED` is included only when the dataset exposes event timestamps
  or an attention/anomaly field (attention family). Without it, fall back to
  Surprise / Change.

## 6. Reversed-sign variant inclusion
- Every primary candidate also emits a reversed-sign variant (`-rank(...)` /
  `reverse(...)`). The reversed sign is a first-line de-correlation weapon
  (see `brain-alpha-repair` step 2, weapon 4) and frequently recovers signal when
  raw direction is already priced in.

## 7. Failure attribution per result
Each result is tagged with which (family, bucket, vec_op) combination produced it, so
the scheduler's failure memory can deprioritise a (category, dataset, bucket, shape)
arm after repeated rejects.
