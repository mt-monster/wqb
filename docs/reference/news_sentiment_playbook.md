# News / Sentiment / Social-media Mining Playbook

> Reference for the 6-bucket news framework used by
> `Claude/skills/brain-alpha-research-news-sentiment` and by `brain-alpha-repair`
> (news / sentiment correlation repairs). Contains **motifs and design targets, not
> formulas** — concrete operators live in
> `Claude/skills/brain-alpha-research/references/forum-template-library.md`.
> **Guidance, not gates**: nothing in code enforces the buckets or the §6 targets.

## 1. When this applies
Switch to this playbook when the target dataset `category ∈ {news, sentiment, socialmedia}`
OR its id matches `news*` / `nws*` / `sentiment*` / `snt*`. Prefer short, event-scale windows
on these (long windows smooth away the event signal — 2026-04 experience, not re-measured);
the S0 probe battery (`probe_battery` P1–P8) is a level probe, not a design rotation.

## 2. Five-family field classification
Every candidate field is classified into exactly one family (classifier:
`src/wqb/research/news_field_classifier.py`; cache: `tracking/taxonomies/taxonomy_<dataset>_<region>.json`):

| Family | Meaning | Example signals |
|--------|---------|----------------|
| **direction** | signed sentiment / tone | `news_ton_last`, EPS-revision sign |
| **attention** | relevance / volume / mention count / novelty (the classifier keyword table files `novelty` here) | `news_vol_*`, mention frequency |
| **dispersion** | stddev, variance, uncertainty, disagreement | `news_vol_stddev`, disagreement proxies |
| **event_type** | topic codes, significance, deal types, intraday/front-page | `nws12_mainz_vol_ratio`, `atrratio` |
| **peer_context** | pre-aggregated peer values | sector-relative attention |

Rule: never put three fields from the same family in one batch.

## 3. Six-bucket framework
Design each batch across buckets by hand. **HIGH-priority buckets are emphasised**
(lean toward D/E/P); no sampler or orchestrator picks buckets for you.

| Bucket | Definition | Design target | Priority |
|--------|------------|---------------|----------|
| **Level** | raw signal level | regime/surprise extraction when level is unusually stable & uncrowded | normal |
| **Change** | short-horizon change / deviation-from-baseline | std / zscore of recent vs baseline | normal |
| **Surprise** | unexpected jump vs expectation | event-minus-expected | normal |
| **Dispersion** | cross-sectional spread of the field | stddev / disagreement of peer distribution | **HIGH** |
| **Event-conditioned** | trade only on attention-anomaly days | `trade_when(attention > thr)` gating | **HIGH** |
| **Propagation** | spillover across assets / lagged diffusion | lead-lag / cross-asset correlation | **HIGH** |

Motif reminder: prefer *regime-change or surprise extraction* over raw level unless
Labs/WebDataScope shows level behaviour is unusually stable and uncrowded.

## 4. Cross-family field pairing rules
Detailed pairing matrix lives in `news_bucket_field_map.md` §1 (matrix) and §3 (rules). Summary:
- direction × attention → Surprise / Event-conditioned
- dispersion × peer_context → Dispersion
- event_type × direction → Propagation / Event-conditioned
- sentiment–price divergence (sentiment vs returns/volume/volatility) is a *different*
  motif than sentiment–sentiment subtraction — pair sentiment with a non-sentiment
  input when the single-dataset constraint is soft.
- VECTOR fields: rotate `vec_op` across families; require ≥2 distinct `vec_op` per batch.

## 5. Ghost-operator substitution hints (hand-edited expressions)
Authority for *which* operators are ghosts = `wqb.config.GHOST_OPERATORS` (18 names; the
table below must list exactly those — pinned by `tests/unit/test_se_docs.py`). These
operators were never on the live platform. If a forum post cites one, rewrite with the
real-op substitute **before** pasting:

| Ghost op (DO NOT USE) | Real substitute |
|-----------------------|-----------------|
| `ts_entropy` | `ts_av_diff` / `rank`-based concentration |
| `ts_percentage` | `ts_rank` / `ts_zscore` |
| `ts_skewness` | `ts_zscore` / `winsorize` |
| `ts_median` | `ts_mean` / `rank` |
| `ts_min_max_diff` | `ts_max_diff` |
| `ts_min_max_cps` | `ts_decay_linear` |
| `ts_partial_corr` | `ts_regression(...,).residual` / `ts_corr` |
| `ts_co_kurtosis` | `ts_kurtosis` (if present) or drop |
| `ts_delta_limit` | `ts_delta` |
| `group_normalize` | `group_rank` / `group_zscore` |
| `group_median` | `group_mean` |
| `group_percentage` | `group_rank` |
| `group_vector_proj` | `ts_zscore(vec_avg(...))` |
| `tanh` | `signed_power(x, 1)` / `rank` |
| `sigmoid` | `signed_power(x, 0.5)` |
| `s_log_1p` | `log(1+abs(x))*sign(x)` / `winsorize` |
| `ts_decay_exp_window` | `ts_decay_linear` |
| `neutralize` | `group_neutralize(x, g)` (the platform has no bare `neutralize` expression operator) |

## 6. Per-batch design targets (guidance — no code gate)
- ≥3 distinct buckets per batch
- ≥1 HIGH-priority bucket (Dispersion / Event-conditioned / Propagation)
- ≥2 distinct `vec_op` when VECTOR fields present
- ≥2 distinct expression shapes per batch (the enforced version of this is toolkit gate 6
  `check_batch_diversity`; `validator.check_batch` has no callers)
- Coverage < 0.4 fields require `ts_backfill` / `group_backfill` or are dropped
  (raw low-coverage fields produce 5–10-stock concentrated alphas that fail
  `CONCENTRATED_WEIGHT`) — this one **is** enforced (inspect hard gate, check 1).

## 7. Escalation & early-stop (heuristics from 2026-04; unmeasured since)
- Allow up to ~50 structurally-distinct attempts before giving up on a news idea
  (was 30; raised in 2026-04).
- Early-stop after 15 consecutive zero-PASS iterations clustering in ≤2 buckets
  (framework drift, not a sampling problem).
- RA's own stop rules (`loop-and-stop.md`) still apply on top of these.
