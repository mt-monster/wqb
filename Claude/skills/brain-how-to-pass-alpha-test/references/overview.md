# BRAIN Alpha Submission Tests: Requirements and Improvement Tips

This document compiles the key requirements for passing alpha submission tests on the WorldQuant BRAIN platform, based on official documentation and community experiences from the forum. I've focused on the main tests (Fitness, Sharpe, Turnover, Weight, Sub-universe, and Self-Correlation). For each, I'll outline the thresholds, explanations, and strategies to improve or pass them, drawing from doc pages like "Clear these tests before submitting an Alpha" and forum searches on specific topics.

> **本页的定位（2026-09-29 瘦身）**：只保留 6 项提交测试的**官方文档要求与社区技巧**（§1–§6）。检查名 → 线 → 读哪节的总表、数值例与本库的口径见 [`SKILL.md`](SKILL.md) §0；此前混在这里的「想法层通识」（idea 来源、arXiv、ATOM、6 种字段探测、社区模板、官方例子，共 63 行）已删——它们与提交测试阈值无关，且与 `wq-brain-alpha-optimization-v1` Mode B、`brain-datafield-exploration-general` 重复（arXiv 用法见 optimization-v1 的 `arXiv_API_Tool_Manual.md`）。
> **阈值以 `wqb.config` 为准**（`PLATFORM_CHECK_LINES` / `GATES_INTERNAL` / `GATES_PLATFORM`）；下面各节里的数字是官方文档原文，与 config 出入时以 config / `is.checks` 的 `limit` 为准。

## What Are Alpha Tests?
Alphas must pass a series of pre-submission checks (viewable via `mcp__wq-brain-http__get_alpha_details` → `is.checks`) before they can be submitted for out-of-sample (OS) testing; only submitted alphas contribute to scoring and payments. The real list of checks that count is the 18 `RA_CHECK_NAMES` (see SKILL §0), plus `SELF_CORRELATION` / `PROD_CORRELATION`. Failing tests result in errors like "Sub-universe Sharpe NaN is not above cutoff" or low fitness; failure messages guide improvements (e.g., "Improve fitness" or "Reduce max correlation").

## General Guidance on Passing Tests
- **Start Simple**: Use basic operators like `ts_rank` or `ts_corr` on price-volume data.
- **Universe / neutralization**: use the region's default universe (`wqb.config.REGIONS`); neutralization affects correlation but **not** `CONCENTRATED_WEIGHT` (SKILL §4).
- **Improve Metrics**: `ts_decay_linear` for stability, `scale` for normalization; check correlation with `mcp__wq-brain-http__check_correlation` (read-only).
- **Common Pitfalls**: high correlation, NaN data (fix with `ts_backfill`), low IR / Fitness.

## 1. Fitness
### Requirements
- At least "Average": Greater than 1.3 for Delay-0 or Greater than 1 for Delay-1.
- Fitness = Sharpe * sqrt(abs(Returns) / max(Turnover, 0.125)).
- Ratings: Spectacular (>2.5 Delay-1 or >3.25 Delay-0), Excellent (>2 or >2.6), etc.

### Explanation
Fitness balances Sharpe, Returns, and Turnover. High fitness indicates a robust alpha. It's a key metric for alpha quality.

### Tips to Improve
- **From Docs**: Increase Sharpe/Returns and reduce Turnover. Optimize by balancing these—improving one may hurt another. Aim for upward PnL trends with minimal drawdown.
- **Forum Experiences** (from searches on "increase fitness alpha"):
  - Use group operators (e.g., with pv13) to boost fitness without overcomplicating expressions.
  - Screen alphas with author_fitness >=2 or similar in competitions like Super Alpha.
  - Manage alphas via databases or tags; query for high-fitness ones (e.g., via API with fitness filters).
  - In hand-crafting alphas, iteratively add operators like left_tail and group to push fitness over thresholds, but watch for overfitting.
  - Community shares: High-fitness alphas (e.g., >2) often come from multi-factor fusions or careful data field selection.

## 2. Sharpe Ratio
### Requirements
- Greater than 2 for Delay-0 or Greater than 1.25 for Delay-1.
- Sharpe = sqrt(252) * IR, where IR = mean(PnL) / stdev(PnL).

### Explanation
Measures risk-adjusted returns. Higher Sharpe means more consistent performance. For GLB alphas, additional sub-geography Sharpes (>=1 for AMER, APAC, EMEA).

### Tips to Improve
- **From Docs**: Focus on consistent PnL with low volatility. Use visualization to ensure upward trends. For sub-geography, incorporate region-specific signals (e.g., earnings for AMER, microstructure for APAC).
- **Forum Experiences** (from searches on "improve Sharpe ratio alpha"):
  - Decay signals separately for liquid/non-liquid stocks (e.g., ts_decay_linear with rank(volume*close)).
  - Avoid size-related multipliers (e.g., rank(-assets)) that shift weights to illiquid stocks.
  - Check yearly Sharpe data via API and store in databases for analysis.
  - In templates like CCI-based, combine with z-score and delay to stabilize Sharpe.
  - Community tip: Prune low-Sharpe alphas in pools using weighted methods to retain high-Sharpe ones.
  - **Flipping Negative Sharpe**: For non-CHN regions, if an alpha shows negative Sharpe (e.g., -1 to -2), add a minus sign to the expression (e.g., `-original_expression`) to flip it positive. This preserves the signal while improving metrics; verify it doesn't introduce correlation issues.

## 3. Turnover
### Requirements
- 1% < Turnover < 70%.
- Turnover = Dollar trading volume / Book size.

### Explanation
Indicates trading frequency. Low turnover reduces costs; extremes fail submission.

### Tips to Improve
- **From Docs**: Aim for balanced trading—too low means inactive, too high means over-trading.
- **Forum Experiences**: (Note: Specific turnover searches weren't direct, but tied to fitness/Sharpe improvements)
  - Use decay functions to smooth signals, reducing unnecessary trades.
  - In multi-alpha simulations, filter by turnover thresholds in code to pre-select candidates.

## 4. Weight Test
### Requirements
- Max weight in any stock <10%.
- Sufficient instruments assigned weight (varies by universe, e.g., TOP3000).

### Explanation
Ensures diversification; fails if concentrated or too few stocks weighted.

### Tips to Improve
- **From Docs**: Avoid expressions that overly concentrate weights. Assign weights broadly after simulation start.
- **Forum Experiences**: (Limited direct posts; inferred from general submission tips)
  - ⚠ The forum tip "use neutralization to distribute weights" was **tested and found ineffective** for `CONCENTRATED_WEIGHT` (SKILL §4, [evidence](references/concentrated-weight-evidence.md)): the effective fix is time smoothing of instantaneous count/event signals.
  - Check via simulation stats.

## 5. Sub-universe Test
### Requirements
- Sub-universe Sharpe >= 0.75 * sqrt(subuniverse_size / alpha_universe_size) * alpha_sharpe.
- Ensures robustness in more liquid sub-universes (e.g., TOP1000 for TOP3000).

### Explanation
Tests if alpha performs in liquid stocks, avoiding over-reliance on illiquid ones.

### Tips to Improve
- **From Docs**: Avoid size-related multipliers. Decay liquid / non-liquid parts separately — express the split with `bucket` / `group_*` (optimization-v1 `references/structural-interaction-forms.md`, family F4), **not** by adding two differently-decayed copies of the signal with rank(volume*close) weights: that is a weighted sum of two signal legs (the docs' original example), which the project's gate 5 blocks (`infix_leg_sum` / weighted mix).
  - Step-by-step improvements; discard non-robust signals.
- **Forum Experiences**: (From "how to pass submission tests")
  - Improve overall Sharpe first, as it scales the threshold.
  - Use pasteurize to handle NaNs and ensure even distribution.

## 6. Self-Correlation
### Requirements
- <0.7 PnL correlation with own submitted alphas.
- Or Sharpe at least 10% greater than correlated alphas. (**This repo does not implement the second path**: `GATES_PLATFORM['self_corr_max']` / `submit_queue.LIM['self']` are single thresholds — SKILL §6a has a numeric example.)

### Explanation
Promotes diversity; based on 4-year PnL window. Allows improvements if new alpha is significantly better.

### Tips to Improve
- **From Docs**: Submit diverse ideas. Use correlation table in results to identify issues.
- **Forum Experiences** (from searches on "reduce correlation self alphas"):
  - Local computation of self-correlation (e.g., via PnL matrices) to pre-filter before submission.
  - Code optimizations: Prune high-correlation alphas, use clustering or weighted pruning (e.g., Sharpe-weighted) to retain diverse sets.
  - Handle negatives: transform negatively correlated alphas (e.g., in China market) by inversion or adjustments. (Forum wording, **semantics not verified here** — do not apply without a platform check.)
  - Scripts for batch checking: Use machine_lib modifications to print correlations and pyramid info.
  - Community shares: Differences between local and platform calculations (e.g., due to NaN handling); align by using full PnL data.

### Evaluating Whole Alpha Quality
Before final submission, perform these checks on simulation results:

- **Yearly Stats Quality Check**: Review yearly statistics. If records are missing for >5 years, it indicates low data quality (e.g., sparse coverage). Fix with ts_backfill, data selection, or alternative fields to ensure robust performance across tests.

This complements per-test improvements by validating overall alpha reliability.

## General Advice
- Start with broad simulations, narrow based on stats.
- `mcp__wq-brain-http__workflow_submit_alpha` has two very different modes selected by one boolean: **`confirm_submit=False` (default) = local pre-check + status query only**; **`confirm_submit=True` = a real, irreversible submission** that needs the user's explicit authorization (see `worldquant-submit-alpha`). Never call it with `True` just to "pre-check".
- Forum consensus: Automate with Python scripts for efficiency (e.g., threading for simulates, databases for alpha management).
- Risks: Overfitting in manual tweaks; validate with train/test splits.

This guide is based on tool-gathered data. For updates, check BRAIN docs or forum.
