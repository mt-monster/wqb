"""wqb.research.hypothesis_miner — hypothesis-driven alpha experiments.

A hypothesis couples a minimal expression with an ablation (gate removed),
a constant control and a variant. ``judge`` turns the four Sharpe readings
into a verdict recorded in the session ledger.
"""

from __future__ import annotations

import json
import os
from dataclasses import dataclass, asdict
from datetime import datetime, timezone
from enum import Enum
from typing import Dict, List, Optional

HYPOTHESIS_CLASSES: List[str] = [
    "over_reaction",
    "under_reaction",
    "momentum",
    "mean_reversion",
    "volatility_risk",
    "liquidity",
    "information_flow",
    "event_driven",
    "sentiment_drift",
    "peer_relative",
    "coverage_gap",
    "decay_structure",
]

_PSEUDO_SIGNAL_TOLERANCE = 0.1
_MIN_PRIMARY_SHARPE = 0.3
_SUPPORTED_SHARPE_DELTA = 0.5
_SUPPORTED_FITNESS = 0.8

_REQUIRED_FIELDS = [
    "hypothesis_id",
    "hypothesis_class",
    "description",
    "minimal_expression",
    "ablation_no_gate",
    "control_constant",
    "variant",
    "expected_direction",
]


class HypothesisVerdict(Enum):
    REJECTED = "rejected"
    SUPPORTED = "supported"
    NEEDS_REFINEMENT = "needs_refinement"
    PARTIALLY_SUPPORTED = "partially_supported"


@dataclass
class Hypothesis:
    hypothesis_id: str
    hypothesis_class: str
    description: str
    minimal_expression: str
    ablation_no_gate: str
    control_constant: str
    variant: str
    expected_direction: str

    def to_dict(self) -> dict:
        return asdict(self)


@dataclass
class ExperimentResult:
    hypothesis_id: str
    primary_sharpe: float
    ablation_sharpe: float
    control_sharpe: float
    variant_sharpe: float
    primary_fitness: float = 0.0
    control_fitness: float = 0.0


def judge(result: ExperimentResult) -> Dict:
    """Turn an experiment's readings into a verdict with diagnostics."""
    sharpe_delta = result.primary_sharpe - result.control_sharpe
    ablation_delta = result.primary_sharpe - result.ablation_sharpe
    variant_delta = result.primary_sharpe - result.variant_sharpe
    pseudo_signal = abs(sharpe_delta) <= _PSEUDO_SIGNAL_TOLERANCE

    diagnostics = {
        "sharpe_delta": sharpe_delta,
        "ablation_delta": ablation_delta,
        "variant_delta": variant_delta,
        "pseudo_signal": pseudo_signal,
    }

    if pseudo_signal:
        status = HypothesisVerdict.REJECTED
        reason = ("Primary Sharpe within "
                  f"{_PSEUDO_SIGNAL_TOLERANCE} of the constant control: "
                  "signal is not attributable to the gate.")
    elif result.primary_sharpe < _MIN_PRIMARY_SHARPE:
        status = HypothesisVerdict.NEEDS_REFINEMENT
        reason = (f"Primary Sharpe {result.primary_sharpe:.2f} below "
                  f"{_MIN_PRIMARY_SHARPE}; refine before judging.")
    elif (sharpe_delta > _SUPPORTED_SHARPE_DELTA
          and result.primary_fitness > _SUPPORTED_FITNESS):
        status = HypothesisVerdict.SUPPORTED
        reason = ("Strong delta over control with fitness "
                  f"{result.primary_fitness:.2f} > {_SUPPORTED_FITNESS}.")
    else:
        status = HypothesisVerdict.PARTIALLY_SUPPORTED
        reason = "Delta over control exists but strength/fitness insufficient."

    return {"status": status, "reason": reason, "diagnostics": diagnostics}


def load_catalog(path: str) -> List[Hypothesis]:
    """Load a hypothesis catalog (JSON). Raises on missing file/fields."""
    if not os.path.exists(path):
        raise FileNotFoundError(f"Catalog not found: {path}")
    with open(path, "r", encoding="utf-8") as f:
        data = json.load(f)
    hypotheses: List[Hypothesis] = []
    for entry in data.get("hypotheses", []):
        missing = [k for k in _REQUIRED_FIELDS if k not in entry]
        if missing:
            raise ValueError(
                f"Hypothesis entry missing required fields: {missing}")
        hypotheses.append(Hypothesis(**{k: entry[k] for k in _REQUIRED_FIELDS}))
    return hypotheses


def run_hypothesis_round(catalog_path: str,
                         max_hypotheses: int = 1) -> Dict[str, Dict]:
    """Build one experiment round: 4 expressions per selected hypothesis.

    Expressions: minimal, ablation (no gate), control constant, variant.
    """
    if max_hypotheses < 1:
        raise ValueError("max_hypotheses must be >= 1")
    hypotheses = load_catalog(catalog_path)
    experiments: Dict[str, Dict] = {}
    for h in hypotheses[:max_hypotheses]:
        experiments[h.hypothesis_id] = {
            "hypothesis": h.to_dict(),
            "expressions": [
                h.minimal_expression,
                h.ablation_no_gate,
                h.control_constant,
                h.variant,
            ],
        }
    return experiments


def save_to_ledger(verdict: Dict, session_id: str,
                   ledger_dir: Optional[str] = None) -> str:
    """Append a verdict record to the hypothesis ledger (JSONL)."""
    ledger_dir = ledger_dir or os.path.join("tracking", "hypotheses")
    os.makedirs(ledger_dir, exist_ok=True)
    path = os.path.join(ledger_dir, "ledger.jsonl")
    status = verdict.get("status")
    if isinstance(status, HypothesisVerdict):
        status = status.value
    record = {
        "session_id": session_id,
        "status": status,
        "reason": verdict.get("reason", ""),
        "diagnostics": verdict.get("diagnostics", {}),
        "timestamp": datetime.now(timezone.utc).isoformat(),
    }
    with open(path, "a", encoding="utf-8") as f:
        f.write(json.dumps(record, ensure_ascii=False) + "\n")
    return path
