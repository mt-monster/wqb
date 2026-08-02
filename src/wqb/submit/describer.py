"""Alpha describer: generate submission descriptions with economic stories.

Implements the submission description generator (robustness Phase D.4,
orchestrator submission stage).  Every alpha submitted to BRAIN needs a
human-readable description that includes:

1. An **economic story** — a single sentence articulating the signal
   direction and why it should predict returns.
2. **Key metric summary** — Sharpe, fitness, turnover, returns, drawdown.
3. **Structural characteristics** — paradigm, operators, window, group.

When a candidate passes robustness with CONDITIONAL flags, the surviving
soft-flags are annotated into the description via
:func:`annotate_soft_flags` — this creates a legible audit trail for OS
performance review.

Public API
----------
- :data:`ECONOMIC_STORY_TEMPLATE` — string template for economic stories.
- :func:`format_economic_story` — generate an economic interpretability
  story from expression + dataset + region.
- :func:`describe_alpha` — full submission description.
- :func:`annotate_soft_flags` — append surviving soft-flags.
"""

from __future__ import annotations

import re
from typing import List, Optional


# ---------------------------------------------------------------------------
# Economic story template
# ---------------------------------------------------------------------------

ECONOMIC_STORY_TEMPLATE: str = (
    "This alpha captures {signal_description} from the {dataset} dataset "
    "in the {region} market. The signal is constructed by {construction_method}, "
    "exploiting the economic intuition that {economic_intuition}. "
    "The expression uses {operator_summary} to transform raw data into "
    "a cross-sectional signal that predicts {return_direction} returns."
)


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

# Operator extraction regex (identifier followed by '(')
_OP_RE = re.compile(r"([a-zA-Z_][a-zA-Z0-9_]*)\s*\(")

# Window extraction regex (number inside ts_* operators)
_WINDOW_RE = re.compile(r"ts_\w+\([^,]+,\s*(\d+)")

# Group variable extraction
_GROUP_RE = re.compile(r"group_\w+\([^,]+,\s*([a-zA-Z_]+)\s*\)")


def _extract_operators(expression: str) -> List[str]:
    """Extract operator names from an expression string."""
    return _OP_RE.findall(expression)


def _extract_windows(expression: str) -> List[int]:
    """Extract window lengths from ts_* operators."""
    return [int(m) for m in _WINDOW_RE.findall(expression)]


def _extract_groups(expression: str) -> List[str]:
    """Extract group variable names from group_* operators."""
    return _GROUP_RE.findall(expression)


def _classify_signal_type(expression: str) -> str:
    """Classify the broad signal type from the expression structure."""
    expr_lower = expression.lower()
    if "ts_delta" in expr_lower or "ts_av_diff" in expr_lower:
        return "momentum"
    if "ts_std_dev" in expr_lower:
        return "dispersion"
    if "trade_when" in expr_lower:
        return "event_gated"
    if "group_rank" in expr_lower or "group_zscore" in expr_lower:
        return "cross_sectional_grouped"
    if "ts_rank" in expr_lower or "ts_zscore" in expr_lower:
        return "time_series_normalized"
    if "rank(" in expr_lower or "zscore(" in expr_lower:
        return "cross_sectional"
    if "signed_power" in expr_lower:
        return "nonlinear_transform"
    if "subtract" in expr_lower or " - " in expr_lower:
        return "spread"
    if "divide" in expr_lower or " / " in expr_lower:
        return "ratio"
    return "composite"


def _get_construction_method(expression: str) -> str:
    """Describe how the signal is constructed from the expression."""
    signal_type = _classify_signal_type(expression)
    descriptions = {
        "momentum": "computing short-horizon changes in the input fields",
        "dispersion": "measuring the dispersion/volatility of the input fields",
        "event_gated": "activating the signal only on event-anomaly days",
        "cross_sectional_grouped": "ranking within peer groups defined by sector/industry",
        "time_series_normalized": "normalizing inputs relative to their recent time-series distribution",
        "cross_sectional": "ranking inputs cross-sectionally across the stock universe",
        "nonlinear_transform": "applying a nonlinear signed-power transformation",
        "spread": "computing the spread between two input fields",
        "ratio": "computing the ratio between two input fields",
        "composite": "combining multiple transformations of the input fields",
    }
    return descriptions.get(signal_type, "transforming input fields")


def _get_economic_intuition(signal_type: str, dataset: str) -> str:
    """Generate the economic intuition sentence based on signal type and dataset."""
    dataset_lower = dataset.lower()
    is_news = dataset_lower.startswith(("news", "nws", "sentiment", "snt"))

    if is_news:
        intuitions = {
            "momentum": "short-term shifts in news/sentiment momentum precede price adjustments as information is gradually incorporated",
            "dispersion": "disagreement in news/sentiment signals predicts future volatility and mean-reversion opportunities",
            "event_gated": "significant news events create temporary mispricings that are corrected as the market digests new information",
            "cross_sectional_grouped": "relative news/sentiment positioning within industry peers predicts cross-sectional return differentials",
            "time_series_normalized": "deviations of news/sentiment from their recent norms signal overreaction that subsequently reverts",
            "cross_sectional": "stocks with more favorable news/sentiment signals outperform those with less favorable signals",
            "nonlinear_transform": "the relationship between news/sentiment and returns is nonlinear, with extreme values carrying disproportionate predictive power",
            "spread": "the differential between news/sentiment measures across fields captures information not priced by the market",
            "ratio": "the relative balance between news/sentiment components signals fundamental shifts in market perception",
            "composite": "the combination of news/sentiment transformations captures information orthogonal to standard price-based signals",
        }
    else:
        intuitions = {
            "momentum": "short-term changes in fundamental/analyst signals precede price adjustments as information diffuses",
            "dispersion": "disagreement in analyst estimates or fundamental measures predicts future volatility and returns",
            "event_gated": "significant fundamental events create temporary mispricings that correct as the market processes new data",
            "cross_sectional_grouped": "relative fundamental positioning within industry peers predicts cross-sectional return differentials",
            "time_series_normalized": "deviations of fundamentals from their recent norms signal overreaction that subsequently reverts",
            "cross_sectional": "stocks with stronger fundamental signals outperform those with weaker signals",
            "nonlinear_transform": "the relationship between fundamentals and returns is nonlinear, with extreme values carrying disproportionate signal",
            "spread": "the spread between fundamental measures captures value-relevant information not fully priced by the market",
            "ratio": "the relative balance between fundamental components signals shifts in valuation that predict returns",
            "composite": "the combination of fundamental transformations captures information orthogonal to standard price-based signals",
        }

    return intuitions.get(signal_type, "the signal captures information not fully reflected in current prices")


def _get_return_direction(expression: str) -> str:
    """Determine whether the signal predicts positive or negative returns."""
    # If the expression contains a leading '-' or 'reverse', it's likely
    # a contrarian signal.
    expr_stripped = expression.strip()
    if expr_stripped.startswith("-") or "reverse(" in expr_stripped:
        return "negative (contrarian)"
    return "positive"


def _summarize_operators(expression: str) -> str:
    """Create a short summary of the operators used in the expression."""
    ops = _extract_operators(expression)
    if not ops:
        return "direct field comparison"

    # Deduplicate while preserving order
    seen = set()
    unique_ops = []
    for op in ops:
        if op not in seen:
            seen.add(op)
            unique_ops.append(op)

    if len(unique_ops) <= 3:
        return ", ".join(unique_ops)
    return ", ".join(unique_ops[:3]) + f" (and {len(unique_ops) - 3} more)"


# ---------------------------------------------------------------------------
# Public API
# ---------------------------------------------------------------------------


def format_economic_story(
    expression: str,
    dataset: str,
    region: str,
) -> str:
    """Generate an economic interpretability story for an alpha.

    The story must be writable in one sentence (robustness decision table:
    "Economic interpretability — writable in 1 sentence").  This function
    produces a template-based story that can be reviewed and refined.

    Parameters
    ----------
    expression : str
        Alpha expression string.
    dataset : str
        Dataset ID (e.g. ``"news12"``).
    region : str
        Region code (e.g. ``"USA"``).

    Returns
    -------
    str
        A one-paragraph economic story explaining the signal's direction
        and economic rationale.
    """
    signal_type = _classify_signal_type(expression)
    construction = _get_construction_method(expression)
    intuition = _get_economic_intuition(signal_type, dataset)
    operator_summary = _summarize_operators(expression)
    return_direction = _get_return_direction(expression)

    signal_description = f"a {signal_type.replace('_', ' ')} signal"

    return ECONOMIC_STORY_TEMPLATE.format(
        signal_description=signal_description,
        dataset=dataset,
        region=region,
        construction_method=construction,
        economic_intuition=intuition,
        operator_summary=operator_summary,
        return_direction=return_direction,
    )


def describe_alpha(
    alpha_details: dict,
    robustness_report: Optional[dict] = None,
) -> str:
    """Generate a full alpha submission description.

    The description includes:
    1. Economic story (one sentence).
    2. Key metric summary (Sharpe, fitness, turnover, returns, drawdown).
    3. Structural characteristics (paradigm, operators, window, group).

    If a robustness report is provided and the candidate passed with
    CONDITIONAL flags, the surviving soft-flags are annotated.

    Parameters
    ----------
    alpha_details : dict
        Alpha details from ``get_alpha_details`` or a simulation result.
        Expected keys: ``expression``, ``dataset`` (or ``settings.dataset``),
        ``region`` (or ``settings.region``), and IS metrics.
    robustness_report : dict or None
        Optional robustness audit report.  If provided and the decision is
        ``"PASS"`` with CONDITIONAL flags, they are annotated.

    Returns
    -------
    str
        Multi-line description string suitable for ``set_alpha_properties``.
    """
    expression = alpha_details.get("expression", alpha_details.get("regular", ""))
    settings = alpha_details.get("settings", {})
    dataset = alpha_details.get("dataset", settings.get("dataset", "unknown"))
    region = alpha_details.get("region", settings.get("region", "USA"))

    is_data = alpha_details.get("is", alpha_details)
    metrics = {
        "sharpe": is_data.get("sharpe", alpha_details.get("sharpe", "N/A")),
        "fitness": is_data.get("fitness", alpha_details.get("fitness", "N/A")),
        "turnover": is_data.get("turnover", alpha_details.get("turnover", "N/A")),
        "returns": is_data.get("returns", alpha_details.get("returns", "N/A")),
        "drawdown": is_data.get("drawdown", alpha_details.get("drawdown", "N/A")),
        "margin": is_data.get("margin", alpha_details.get("margin", "N/A")),
    }

    # Format metrics
    def _fmt(v) -> str:
        if isinstance(v, (int, float)):
            return f"{v:.4f}" if abs(v) < 1000 else str(v)
        return str(v)

    lines: List[str] = []

    # 1. Economic story
    story = format_economic_story(expression, dataset, region)
    lines.append(story)
    lines.append("")

    # 2. Key metrics
    lines.append("Key Metrics:")
    lines.append(f"  - Sharpe: {_fmt(metrics['sharpe'])}")
    lines.append(f"  - Fitness: {_fmt(metrics['fitness'])}")
    lines.append(f"  - Turnover: {_fmt(metrics['turnover'])}")
    lines.append(f"  - Returns: {_fmt(metrics['returns'])}")
    lines.append(f"  - Drawdown: {_fmt(metrics['drawdown'])}")
    lines.append(f"  - Margin: {_fmt(metrics['margin'])} bp")
    lines.append("")

    # 3. Structural characteristics
    ops = _extract_operators(expression)
    windows = _extract_windows(expression)
    groups = _extract_groups(expression)
    signal_type = _classify_signal_type(expression)

    lines.append("Structural Characteristics:")
    lines.append(f"  - Signal type: {signal_type}")
    lines.append(f"  - Operators: {_summarize_operators(expression)}")
    lines.append(f"  - Operator count: {len(ops)}")
    if windows:
        lines.append(f"  - Windows: {windows}")
    if groups:
        lines.append(f"  - Group variables: {', '.join(set(groups))}")
    lines.append(f"  - Neutralization: {settings.get('neutralization', 'N/A')}")
    lines.append(f"  - Decay: {settings.get('decay', 'N/A')}")
    lines.append(f"  - Universe: {settings.get('universe', 'N/A')}")
    lines.append("")

    # 4. Robustness annotation
    if robustness_report:
        decision = robustness_report.get("decision", "UNKNOWN")
        lines.append(f"Robustness: {decision}")
        failing_checks = robustness_report.get("failing_checks", [])
        if failing_checks:
            lines.append(f"  - Failing checks: {', '.join(failing_checks)}")
        soft_flags = robustness_report.get("soft_flags", [])
        if soft_flags:
            lines.append(f"  - Soft flags: {', '.join(soft_flags)}")
        lines.append("")

    return "\n".join(lines).strip()


def annotate_soft_flags(
    description: str,
    soft_flags: List[str],
) -> str:
    """Append surviving soft-flags to an alpha description.

    When a candidate passes robustness with CONDITIONAL flags, the surviving
    soft-flags are annotated into the description.  This creates a legible
    audit trail when the user reviews OS performance a year later
    (robustness Phase D.4).

    Parameters
    ----------
    description : str
        The existing alpha description.
    soft_flags : list[str]
        List of soft-flag strings (e.g. ``["full_history_cv=0.72",
        "old_year_2015_flat"]``).

    Returns
    -------
    str
        The description with an appended soft-flags section.  If
        *soft_flags* is empty, the original description is returned unchanged.
    """
    if not soft_flags:
        return description

    flag_lines = "\n".join(f"  - {flag}" for flag in soft_flags)
    annotation = (
        f"\n\nSurviving Soft-Flags (informational, not rejection):\n{flag_lines}"
    )

    return description + annotation
