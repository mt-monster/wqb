# News Bucket ↔ Field-Family Pairing Map

> Companion to `news_sentiment_playbook.md`. Defines how the five field families
> (§2 of the playbook) pair into the six buckets, plus pairing / rotation rules.
> **Design guidance only — no code enforces any of it** (the `news_loop.py` that older
> versions cite does not exist). The batch-level diversity gate is toolkit gate 6
> (`check_batch_diversity`); the skill that carries this map is
> `Claude/skills/brain-alpha-research-news-sentiment`.

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

## 2. Bucket sampling (by hand)
When designing one batch, spread it over buckets and lean toward D / E / P
(Dispersion / Event-conditioned / Propagation) so HIGH-priority coverage exists even
in the first wave. Targets for a batch: ≥3 buckets, ≥1 HIGH. There is no sampler that
draws buckets for you (no Beta posterior anywhere in `src/wqb/search/`).

## 3. Cross-family field pairing rules
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
- Note the `vec_op` choice per expression in your batch notes (nothing logs it for you;
  `wqb.expression.validator.check_batch` has no callers and is not a gate).
- Never summarize a VECTOR field with a scalar op before `vec_avg` / aggregation.

## 5. Event-gated designs
- Event-conditioned designs (`trade_when` on an attention anomaly) only make sense when
  the dataset exposes event timestamps or an attention/anomaly field (attention
  family). Without one, fall back to Surprise / Change. (No template named
  `P15_EVENT_CONDITIONED` exists in code.)

## 6. Reversed-sign variant inclusion
- Every primary candidate also emits a reversed-sign variant (`-rank(...)` /
  `reverse(...)`): it frequently recovers signal when the raw direction is already priced
  in. Whether it also lowers correlation is an empirical question — measure it
  (`check_correlation`), do not assume it.

## 7. Failure attribution per result
Tag each result with the (family, bucket, vec_op) combination that produced it, in the
wave's `key_findings` (RA step 9). `wqb.search.failure_memory` keys arms on
(region, dataset, paradigm, shape_bucket) — news buckets are not part of that key, so
bucket-level lessons live in the notes, not in the scheduler.
