# Forum-mined anti-overfit + attribution techniques

> Fallback ledger compiled from the 2026-04-22 forum scan (~55 distinct posts across
> `过拟合 overfitting alpha`, `归因分析 yearly stats alpha sharpe`, `sub-universe 参数敏感 稳健性测试`).
> Each rule cites the highest-vote source. Use this file only when live Phase A
> search is unavailable; otherwise prefer freshly pulled posts.

## A · Attribution metrics (MCP-backed)

- **Yearly Sharpe CV** — `yearly_sharpe.std() / yearly_sharpe.mean()`.
  Source: JX79797 "OC2025 多维度评分" (96 votes). Default flag ≥ 0.60.
- **Decay ratio** — `last_year_sharpe / full_period_sharpe`.
  Source: the AGENTS §3 yearly-gate table (`YEARLY_GATES.decay_ratio_min = 0.30`) is built on this. Flag < 0.30.
- **厂字形 year-skipping** — count of years with `|sharpe| < 0.3`.
  Source: FZ60707 "排除厂或者缺失多年数据alpha" (40 votes). Flag if ≥ 2 flat years.
- **Year max/min Sharpe ratio** — single-year-driven red flag.
  Source: MH33574 "VF 0.9+ 顾问分享" (36 votes) — "a factor driven by one year is not a factor".
- **Stock concentration** — top-5-stock contribution to cumulative PnL.
  Source: LJ46725 "AI 过拟合套路" (15 votes, 14 comments): "5–10 stocks carrying the Sharpe in TOP3000 is noise-fit".
- **Turnover × margin sanity** — high TVR + low margin = cost-eaten signal.
  Source: LJ46725 again. Hard flag: TVR > 60 % & margin < 3 bp.
- **Risk-Neutralized view** — post-factor-stripping Sharpe; catches alphas whose high IS Sharpe is a systematic-factor exposure.
  Source: JG21054 "[Risk Neutralized]" (65 votes). Pull via `get_alpha_details` risk-neutralized field if available.
- **Performance Comparison** — pool-relative contribution (pos / neg against existing pool).
  Source: AL13375 "Performance Comparison" (74 votes). Soft flag if contribution is negative.

## B · Structural / parameter robustness

- **Sub-Universe test** — Sharpe should hold across nested universes TOP3000 → TOP1000 → TOP500 → TOP200.
  Source: XB37939 "如何优化 Sub-universe Sharpe" (27 votes). BRAIN platform gate. Reject if 2+ sub-universes fail.
- **Robust Universe test** — extended sub-universe over region/neutralization cross-product.
  Source: SZ83096 "ASI robust FAIL 优化小技巧" (75 votes) — "robust 合格的条件是收益保持率".
- **Hump-wrap for sub-universe** — `hump(alpha, 0.02)` dampens extreme-stock-driven Sharpe that fails sub-universe.
  Source: YW79016 "浅谈 hump 操作符解决 Sub-universe Sharpe" (36 votes).
- **Multi-Neutralization sweep** — run the full region-supported neutralization list; a signal that survives only 1 neut is regime-fragile.
  Source: AGENTS §4 `USA_NEUTRALIZATION_SWEEP` + DZ31817 "浅探对 robust test 结果的观测方法" (62 votes).
- **Parameter-sensitivity sweep** — vary decay ∈ {0, 2, 4, 8}, window ±50 %, and confirm Sharpe does not collapse.
  Source: DZ31817 same post; MY49971 "alpha 调参经验" (22 votes).
- **Operator-count bar** — forum consensus among VF 0.9+ consultants: alphas with > 5 scalar operators are suspect; VF 0.9+ submitter FL39657 explicitly caps at ~3 operators ("鼠鼠选取 alpha 的经验" 25 / 68 votes).
- **Economic interpretability** — every alpha must be writable as a 1-sentence economic story.
  Source: YX23928 "Super Alpha 选择及防过拟合技巧" (25 votes): "avoid purely statistical screening".
- **D0 / D1 cross-check** — when a field has both delays, confirm the signal is directionally consistent.
  Source: FF56620 "MCP Workflow 自动化找 alpha" (94 votes).

## C · Composite robustness scoring (for batch audits)

- **一键穩健性評分** — JL98779 (21 votes, 8 comments): single-function `get_alpha_robust_score(alpha_id)` → float in [0, 1]. Combines yearly CV, decay ratio, sub-universe survival, neutralization-sweep survival.
- **Osmosis V2 多维度评分** — CC21336 (6 votes; see also JX79797 96 votes): yearly-stats-driven alpha pool filter. Treats yearly CV as the dominant term.
- **WorldQuant BRAIN 智能分数分配系统** — JX79797 (6 votes): composite robustness formula combining CV_Sharpe, pool-contribution, and margin sanity.

## D · When in doubt

MH33574 (36 votes): **"when you feel not right, it is not right"**. A candidate that passes all quantitative gates but makes the reviewer uneasy about economic justification should be demoted to CONDITIONAL — the OS reality usually validates the intuition.
