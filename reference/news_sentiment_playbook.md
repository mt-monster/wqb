# News / Sentiment / Social-media Mining Playbook

> Canonical reference for the 6-bucket news framework used by `brain-alpha-orchestrator`
> (step 15) and `brain-alpha-research` (step 10/11). Contains **motifs and design
> targets, not formulas** — concrete operators live in the skill SKILL.md and in
> `references/forum-template-library.md`.

## 1. When this applies
Switch to this playbook when the target dataset `category ∈ {news, sentiment, socialmedia}`
OR its id matches `news*` / `nws*` / `sentiment*` / `snt*`. Do **not** run the default
P1/P2/P4/P5 rotation on these — long windows destroy the event signal.

## 2. Five-family field classification
Every candidate field is classified into exactly one family (classifier:
`src/wqb/research/news_field_classifier.py`; cache: `data/field_taxonomy/<region>_<dataset>.json`):

| Family | Meaning | Example signals |
|--------|---------|----------------|
| **direction** | signed sentiment / tone | `news_ton_last`, EPS-revision sign |
| **attention** | relevance / volume / mention count | `news_vol_*`, mention frequency |
| **dispersion** | stddev, novelty, uncertainty, disagreement | `news_vol_stddev`, disagreement proxies |
| **event_type** | topic codes, significance, deal types, intraday/front-page | `nws12_mainz_vol_ratio`, `atrratio` |
| **peer_context** | pre-aggregated peer values | sector-relative attention |

Rule: never put three fields from the same family in one batch.

## 3. Six-bucket framework
Each batch is sampled across buckets (closed-loop orchestrator:
`src/wqb/search/news_loop.py`). **HIGH-priority buckets are emphasised** (Beta
posterior biased toward D/E/P in sampling).

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
Detailed pairing matrix lives in `news_bucket_field_map.md §4`. Summary:
- direction × attention → Surprise / Event-conditioned
- dispersion × peer_context → Dispersion
- event_type × direction → Propagation / Event-conditioned
- sentiment–price divergence (sentiment vs returns/volume/volatility) is a *different*
  motif than sentiment–sentiment subtraction — pair sentiment with a non-sentiment
  input when the single-dataset constraint is soft.
- VECTOR fields: rotate `vec_op` across families; require ≥2 distinct `vec_op` per batch.

## 5. Ghost-operator substitution table (hand-edited expressions)
The following operators were purged on 2026-04-23 (never on the live platform).
If a forum post cites one, rewrite with the real-op substitute **before** pasting:

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

## 6. Hard gates (per batch)
- ≥3 distinct buckets per batch
- ≥1 HIGH-priority bucket (Dispersion / Event-conditioned / Propagation)
- ≥2 distinct `vec_op` when VECTOR fields present
- `check_batch` shape_variety ≥ 2
- Coverage < 0.4 fields require `ts_backfill` / `group_backfill` or are dropped
  (raw low-coverage fields produce 5–10-stock concentrated alphas that fail
  `CONCENTRATED_WEIGHT`)

## 7. Escalation & early-stop
- Escalation raised 30 → 50 structurally-distinct attempts.
- Early-stop after 15 consecutive zero-PASS iterations clustering in ≤2 buckets
  (framework drift, not a sampling problem).
