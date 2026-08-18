"""wqb.research.evidence — curated evidence base driving design decisions.

Each ``Evidence`` links a source (paper, platform guidance, measured run) to
a design implication and an actionable rule enforced elsewhere in wqb.
"""

from __future__ import annotations

from dataclasses import dataclass, asdict
from typing import List, Optional


@dataclass
class Evidence:
    source: str
    source_type: str
    category: str
    design_implication: str
    actionable_rule: str
    date: str

    def to_dict(self) -> dict:
        return asdict(self)


EVIDENCE_REGISTRY: List[Evidence] = [
    Evidence(
        source="WorldQuant BRAIN platform guidance + campaign ledgers",
        source_type="platform",
        category="structure_diversity",
        design_implication="Uniform batches correlate internally and burn "
                           "correlation quota at submission.",
        actionable_rule="Enforce ≥2 shape signatures and ≥2 outer wrappers "
                        "per batch via check_batch before dispatch.",
        date="2026-04-20",
    ),
    Evidence(
        source="2026-04-23 operator audit vs live get_operators",
        source_type="measurement",
        category="operator_hygiene",
        design_implication="Catalog-declared operators missing from the live "
                           "platform (ghosts) cause guaranteed sim errors.",
        actionable_rule="Run operator_audit at session start and block ghost "
                        "operators via ensure_safe_for_dispatch.",
        date="2026-04-23",
    ),
    Evidence(
        source="USA D1 news campaign trajectory ledger",
        source_type="measurement",
        category="observability",
        design_implication="Sessions without event/trajectory logs cannot be "
                           "replayed or mined for insights.",
        actionable_rule="Emit events for every batch and record trajectories "
                        "in SimulationDB each session.",
        date="2026-05-02",
    ),
    Evidence(
        source="WebDataScope quality reports (USA/EUR/KOR d1)",
        source_type="measurement",
        category="data_quality",
        design_implication="Fields with poor coverage or degenerate shape "
                           "produce low-fitness alphas regardless of idea.",
        actionable_rule="Gate dataset entry on coverage/shape inspection "
                        "before expression generation.",
        date="2026-06-10",
    ),
]


def get_evidence(category: Optional[str] = None) -> List[Evidence]:
    """Return all evidence, optionally filtered by category."""
    if category is None:
        return list(EVIDENCE_REGISTRY)
    return [e for e in EVIDENCE_REGISTRY if e.category == category]


def add_evidence(evidence: Evidence) -> None:
    """Register a new evidence entry (validates type and required fields)."""
    if not isinstance(evidence, Evidence):
        raise TypeError(f"Expected Evidence, got {type(evidence).__name__}")
    if not evidence.source:
        raise ValueError("Evidence.source must be non-empty")
    if not evidence.date:
        raise ValueError("Evidence.date must be non-empty")
    EVIDENCE_REGISTRY.append(evidence)
