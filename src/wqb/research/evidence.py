"""Evidence registry for design signals.

This module captures recent papers, platform guidance, and forum wisdom as
**machine-usable records** -- not prose-only notes.  Each ``Evidence`` entry
encodes a concise *design implication* and an *actionable rule* that downstream
code (scheduler, news-loop, robustness audit) can read and apply automatically.

The registry is seeded with the design signals referenced across the five
brain-alpha SKILL.md files.  New evidence can be appended at runtime via
``add_evidence``.
"""

from __future__ import annotations

from dataclasses import asdict, dataclass
from typing import Optional

__all__ = [
    "Evidence",
    "EVIDENCE_REGISTRY",
    "get_evidence",
    "add_evidence",
]


# ---------------------------------------------------------------------------
# Valid category / source-type values (documented for clarity; not enforced
# at runtime so that new categories can be added without code changes).
# ---------------------------------------------------------------------------
_VALID_CATEGORIES = {
    "structure_diversity",
    "setting_diversity",
    "category_coverage",
    "memory_dedup",
    "observability",
}

_VALID_SOURCE_TYPES = {
    "paper",
    "forum",
    "official_doc",
    "platform_update",
}


@dataclass
class Evidence:
    """A single machine-usable design-signal record.

    Attributes
    ----------
    source : str
        Human-readable provenance -- a paper title, forum post ID, or
        official documentation section.
    source_type : str
        One of ``"paper"``, ``"forum"``, ``"official_doc"``,
        ``"platform_update"``.
    category : str
        The aspect of the mining workflow this evidence influences:
        ``"structure_diversity"``, ``"setting_diversity"``,
        ``"category_coverage"``, ``"memory_dedup"``, or
        ``"observability"``.
    design_implication : str
        A one-sentence statement of what the evidence implies for alpha
        design.
    actionable_rule : str
        A concrete, executable rule that operationalises the implication
        (e.g. a threshold, a ranking instruction, an operator choice).
    date : str
        ``YYYY-MM-DD`` date string for the evidence.
    votes : int
        Forum post vote count (0 for non-forum sources).
    """

    source: str
    source_type: str
    category: str
    design_implication: str
    actionable_rule: str
    date: str
    votes: int = 0

    def to_dict(self) -> dict:
        """Serialise to a plain ``dict`` suitable for JSON output."""
        return asdict(self)


# ---------------------------------------------------------------------------
# Pre-seeded registry -- drawn from the brain-alpha-research SKILL.md,
# orchestrator SKILL.md, robustness SKILL.md, and WebDataScope references.
# ---------------------------------------------------------------------------
EVIDENCE_REGISTRY: list[Evidence] = [
    Evidence(
        source="User directive: recent-3yr robustness",
        source_type="official_doc",
        category="observability",
        design_implication=(
            "Robustness should be judged on the last ~3 IS years, not the full "
            "10-year history; requiring all 10 years strong kills live signals."
        ),
        actionable_rule=(
            "When running yearly-stats attribution, gate on recent-3yr Sharpe "
            "(>= user 2Y bar, each year positive) and decay ratio. Treat "
            "full-history CV / flat years as informational soft-flags only."
        ),
        date="2026-06-20",
        votes=0,
    ),
    Evidence(
        source="WebDataScope data package (V0.10.9)",
        source_type="platform_update",
        category="category_coverage",
        design_implication=(
            "The 'sweet-spot' dataset zone -- 100-3000 community submissions "
            "with Sharpe >= 1.1x the regional mean -- offers the best "
            "ProdCorr-free mining opportunity."
        ),
        actionable_rule=(
            "Before simulating, rank datasets by isos.dataset count/sharpe. "
            "Prioritise sweet-spot datasets; skip count<50 (unverified) and "
            "avoid cold-starting on >30K (saturated)."
        ),
        date="2026-07-29",
        votes=0,
    ),
    Evidence(
        source="WebDataScope data package (V0.10.9)",
        source_type="platform_update",
        category="setting_diversity",
        design_implication=(
            "Neutralisation choice should be ranked per-dataset by historical "
            "Sharpe, not swept blindly in a fixed global order."
        ),
        actionable_rule=(
            "Query neutralization.dataset[<ds>] and place the top 2-3 Sharpe "
            "neutralisations (count>=20, osis_count>=20) at the front of the "
            "traversal plan. Fall back to neutralization.category for "
            "low-sample datasets."
        ),
        date="2026-07-29",
        votes=0,
    ),
    Evidence(
        source="WebDataScope data package (V0.10.9)",
        source_type="platform_update",
        category="observability",
        design_implication=(
            "Fields with CoverageRatio < 0.4 produce concentrated-weight "
            "alphas that fail the CONCENTRATED_WEIGHT check even when IS "
            "metrics look strong."
        ),
        actionable_rule=(
            "For any field with coverage < 0.4, apply ts_backfill or "
            "group_backfill before using it as a signal; otherwise drop the "
            "field from the candidate pool."
        ),
        date="2026-07-29",
        votes=0,
    ),
    Evidence(
        source="brain-alpha-research SKILL.md step 10 (news 5-family gate)",
        source_type="official_doc",
        category="structure_diversity",
        design_implication=(
            "News/sentiment/socialmedia fields fall into five families "
            "(direction, attention, dispersion, event_type, peer_context); "
            "a single batch must never contain three fields from the same "
            "family."
        ),
        actionable_rule=(
            "Classify every candidate field via news_field_classifier "
            "before batching. Enforce cross-family pairing: >=3 distinct "
            "buckets, >=1 HIGH-priority (Event/Dispersion/Propagation) "
            "bucket per batch."
        ),
        date="2026-04-23",
        votes=0,
    ),
    Evidence(
        source="brain-alpha-research SKILL.md step 13 (hypothesis-first)",
        source_type="official_doc",
        category="structure_diversity",
        design_implication=(
            "On saturated datasets (>=10K alphas) template sampling is "
            "exhausted by the community; switch to hypothesis-first mining "
            "with ablation experiments to catch pseudo-signals in batch 1."
        ),
        actionable_rule=(
            "When dataset alphaCount >= 10000, load the hypothesis catalog "
            "and dispatch 4-alpha experiments (primary + ablation + control "
            "+ variant). REJECTED verdict (primary Sharpe ~= control Sharpe) "
            "stops the hypothesis in 1 batch."
        ),
        date="2026-04-23",
        votes=0,
    ),
    Evidence(
        source="User directive: field-quality prior (alphaCount)",
        source_type="official_doc",
        category="category_coverage",
        design_implication=(
            "High alphaCount fields are battle-tested for coverage, "
            "robustness, and economic content; they are a strong data-quality "
            "prior and should seed candidate construction first."
        ),
        actionable_rule=(
            "Before designing any batch, sort the dataset's fields by "
            "alphaCount desc (tie-break userCount). Inspect the top ~30 "
            "fields first; only reach for low-usage fields for deliberate "
            "decorrelation plays."
        ),
        date="2026-06-19",
        votes=0,
    ),
    Evidence(
        source="Experiment validation: shape convexity breaks ProdCorr dead zone",
        source_type="platform_update",
        category="structure_diversity",
        design_implication=(
            "Applying signed_power (convex transformation) to one side of a "
            "binary combiner is the strongest single technique for breaking "
            "through the ProdCorr < 0.70 wall on saturated datasets."
        ),
        actionable_rule=(
            "When ProdCorr is stuck above 0.70, inject signed_power(x, "
            "0.5) or rank-based asymmetric pre-ops on the A-side of the "
            "expression to increase shape diversity."
        ),
        date="2026-04-23",
        votes=0,
    ),
    Evidence(
        source="Mathematical relationship: fitness decomposition",
        source_type="official_doc",
        category="observability",
        design_implication=(
            "Fitness = Sharpe * sqrt(returns / turnover); the last mile to "
            "fitness达标 is almost always about compressing turnover, not "
            "raising Sharpe."
        ),
        actionable_rule=(
            "When a candidate passes Sharpe but fails fitness, apply "
            "turnover-reduction operators (ts_decay_linear, trade_when, "
            "hump, jump_decay) before attempting further signal enhancement."
        ),
        date="2026-04-22",
        votes=0,
    ),
]


# ---------------------------------------------------------------------------
# Public API
# ---------------------------------------------------------------------------

def get_evidence(category: Optional[str] = None) -> list[Evidence]:
    """Return evidence records, optionally filtered by *category*.

    Parameters
    ----------
    category : str or None
        If provided, return only evidence whose ``category`` matches.
        Must be one of the valid category strings; ``None`` returns all.

    Returns
    -------
    list[Evidence]
        A (possibly empty) list of matching evidence records, ordered as
        they appear in the registry.
    """
    if category is None:
        return list(EVIDENCE_REGISTRY)
    return [e for e in EVIDENCE_REGISTRY if e.category == category]


def add_evidence(evidence: Evidence) -> None:
    """Append a new *evidence* record to the in-memory registry.

    Parameters
    ----------
    evidence : Evidence
        The evidence record to add.  No deduplication is performed; callers
        are responsible for checking ``EVIDENCE_REGISTRY`` if they want to
        avoid duplicates.

    Raises
    ------
    TypeError
        If *evidence* is not an ``Evidence`` instance.
    ValueError
        If required string fields are empty.
    """
    if not isinstance(evidence, Evidence):
        raise TypeError(f"Expected Evidence, got {type(evidence).__name__}")
    if not evidence.source or not evidence.source.strip():
        raise ValueError("Evidence.source must not be empty")
    if not evidence.source_type or not evidence.source_type.strip():
        raise ValueError("Evidence.source_type must not be empty")
    if not evidence.category or not evidence.category.strip():
        raise ValueError("Evidence.category must not be empty")
    if not evidence.design_implication or not evidence.design_implication.strip():
        raise ValueError("Evidence.design_implication must not be empty")
    if not evidence.actionable_rule or not evidence.actionable_rule.strip():
        raise ValueError("Evidence.actionable_rule must not be empty")
    if not evidence.date or not evidence.date.strip():
        raise ValueError("Evidence.date must not be empty")
    EVIDENCE_REGISTRY.append(evidence)
