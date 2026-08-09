# Researcher Workflow — Hypothesis-First Mining (RD-Agent style)

> Referenced by `brain-alpha-orchestrator` (step 15a) and `brain-alpha-research`
> (step 13). Use this workflow on **saturated datasets (≥10K existing alphas)** where
> template sampling is exhausted. Template sampling there produces pseudo-signals
> (UNITS WARN, field-substitutable) that look promising but waste compute; this
> workflow catches them in batch 1.

## 1. When to switch
- Dataset has ≥10K alphas (e.g. `news12` at 120K α / 21K users).
- A 90-sim template session plateaus (e.g. news12 Fit ≈ 0.42 wall, 2026-04-23).
- The 80-vote Gemini-CLI template workflow (forum HZ32281) and similar automation
  have already mined the template space to its ceiling.

## 2. Build `data/field_semantics/<region>_<dataset>.yaml`
Per-field semantic metadata:
```yaml
- name: anl14_mean_ndebt_fy1
  physical_unit: ratio
  causal_chain_to_returns: "balance-sheet leverage signal -> default risk repricing"
  anchor_only: false          # anchor-only fields (news_spy_close, news_eod_close) NEVER primary signal
  correlated_fields: [anl14_mean_ndebt_fy2]
```
`anchor_only: true` fields must never be used as the primary signal.

## 3. Build `data/hypothesis_catalog/<dataset>_hypotheses.yaml`
20+ falsifiable hypotheses, each:
```yaml
- id: H_overreaction_earnings
  class: over_reaction
  minimal_expression: "rank(ts_zscore(returns, 20))"
  ablation_no_gate: "rank(ts_zscore(returns, 20))"   # same but without event gate
  control_constant: "rank(ts_zscore(volume, 20))"     # constant/control
  variant: "rank(ts_zscore(returns, 20)) * sign(...)"
```
Hypothesis classes: `over_reaction / under_reaction / dispersion / event_conditional /
propagation / information_asymmetry / cross_dataset / horizon_spread / regime /
residual / slow_diffusion / urgency`.

## 4. Dispatch — `run_hypothesis_round`
`src/wqb/research/hypothesis_miner.py::run_hypothesis_round(catalog_path, max_hypotheses=1)`
auto-dispatches **one experiment = 4 alphas**: primary + ablation_no_gate + control_constant + variant.
Computes attribution deltas (primary vs control Sharpe).

## 5. Judge — verdict drives next action
`judge()` returns one of:
- **rejected** → hypothesis done in 1 batch (saves ~40 sims of variant-chasing).
- **partially_supported** → refine specific knobs per the diagnostic.
- **supported** → if it meets user spec, hand off to `brain-alpha-robustness` audit.
- **needs_refinement** → loop with adjusted expression.

> Pseudo-signals (primary Sharpe ≈ control Sharpe) get REJECTED at batch 1.

## 6. Ledger
Accumulate cross-session knowledge in `data/hypothesis_ledger/<session>.jsonl`.
Meta-learning over hypothesis classes replaces per-arm bandit posteriors.

## 7. Relationship to other skills
- Diagnose first with `brain-alpha-repair` if a candidate needs fixing.
- Validate with `brain-alpha-robustness` before `submit_alpha`.
- Field quality prior (`get_datafields` `alphaCount`/`userCount`) still applies as a
  seed ranking, subject to all theme/pyramid/coverage gates.
