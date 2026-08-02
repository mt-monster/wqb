"""Hypothesis-first mining for saturated datasets (RD-Agent style).

On datasets with >= 10K existing community alphas the template-sampling
approach is exhausted: the community has already mined the obvious
combinations and remaining hits are pseudo-signals that waste compute.
This module implements the **hypothesis-first** workflow:

1. A catalog of falsifiable hypotheses is maintained as YAML
   (``data/hypothesis_catalog/<dataset>_hypotheses.yaml``).
2. Each hypothesis is dispatched as a **4-alpha experiment**:
   * **primary** -- the minimal expression that tests the hypothesis.
   * **ablation_no_gate** -- the primary expression with the event gate /
     condition removed, to measure the gate's contribution.
   * **control_constant** -- a constant / trivial signal to establish a
     baseline (pseudo-signal detection).
   * **variant** -- a parameter variant of the primary to test robustness.
3. ``judge()`` compares the four results and returns a verdict:
   ``REJECTED``, ``PARTIALLY_SUPPORTED``, ``SUPPORTED``, or
   ``NEEDS_REFINEMENT``.
4. Verdicts are persisted to a JSONL ledger so meta-learning can accumulate
   across sessions.

The key insight (from the 2026-04-23 session on news12 at 120K alphas):
pseudo-signals -- where ``primary_sharpe ~= control_sharpe`` -- can be
rejected in a single 4-alpha batch instead of wasting ~40 simulations
chasing parameter variants.
"""

from __future__ import annotations

import json
from dataclasses import asdict, dataclass
from enum import Enum
from pathlib import Path
from typing import Any, Optional

__all__ = [
    "HypothesisVerdict",
    "HYPOTHESIS_CLASSES",
    "Hypothesis",
    "ExperimentResult",
    "run_hypothesis_round",
    "judge",
    "save_to_ledger",
    "load_catalog",
]


# ---------------------------------------------------------------------------
# Verdicts
# ---------------------------------------------------------------------------

class HypothesisVerdict(Enum):
    """The outcome of a hypothesis experiment after ``judge()`` evaluation."""

    REJECTED = "rejected"
    PARTIALLY_SUPPORTED = "partially_supported"
    SUPPORTED = "supported"
    NEEDS_REFINEMENT = "needs_refinement"

    def __str__(self) -> str:
        return self.value


#: The 12 hypothesis classes from the research SKILL.md (step 13).
HYPOTHESIS_CLASSES: list[str] = [
    "over_reaction",
    "under_reaction",
    "dispersion",
    "event_conditional",
    "propagation",
    "information_asymmetry",
    "cross_dataset",
    "horizon_spread",
    "regime",
    "residual",
    "slow_diffusion",
    "urgency",
]


# ---------------------------------------------------------------------------
# Data classes
# ---------------------------------------------------------------------------

@dataclass
class Hypothesis:
    """A single falsifiable hypothesis from the catalog.

    Attributes
    ----------
    hypothesis_id : str
        Unique identifier (e.g. ``"news12_over_reaction_01"``).
    hypothesis_class : str
        One of the 12 classes in ``HYPOTHESIS_CLASSES``.
    description : str
        Human-readable statement of the economic hypothesis being tested.
    minimal_expression : str
        The simplest BRAIN expression that tests the hypothesis.
    ablation_no_gate : str
        The primary expression with any event gate / ``trade_when`` removed,
        to isolate the gate's marginal contribution.
    control_constant : str
        A trivial / constant expression (e.g. ``"1"``) that establishes the
        baseline for pseudo-signal detection.
    variant : str
        A parameter variant of the primary expression (e.g. different
        decay window or power exponent) to test parameter sensitivity.
    expected_direction : str
        ``"positive"``, ``"negative"``, or ``"neutral"`` -- the expected
        sign of the primary signal's Sharpe if the hypothesis is true.
    """

    hypothesis_id: str
    hypothesis_class: str
    description: str
    minimal_expression: str
    ablation_no_gate: str
    control_constant: str
    variant: str
    expected_direction: str

    def to_dict(self) -> dict:
        """Serialise to a plain ``dict`` suitable for JSON / YAML output."""
        return asdict(self)


@dataclass
class ExperimentResult:
    """The four-alpha experiment results for a single hypothesis.

    Attributes
    ----------
    hypothesis_id : str
        The hypothesis this experiment tests.
    primary_sharpe : float
        IS Sharpe ratio of the ``minimal_expression`` alpha.
    ablation_sharpe : float
        IS Sharpe ratio of the ``ablation_no_gate`` alpha.
    control_sharpe : float
        IS Sharpe ratio of the ``control_constant`` alpha.
    variant_sharpe : float
        IS Sharpe ratio of the ``variant`` alpha.
    primary_fitness : float
        IS fitness of the primary alpha (Sharpe * sqrt(returns/turnover)).
    control_fitness : float
        IS fitness of the control alpha.
    """

    hypothesis_id: str
    primary_sharpe: float
    ablation_sharpe: float
    control_sharpe: float
    variant_sharpe: float
    primary_fitness: float = 0.0
    control_fitness: float = 0.0

    def to_dict(self) -> dict:
        """Serialise to a plain ``dict`` suitable for JSON output."""
        return asdict(self)


# ---------------------------------------------------------------------------
# Catalog loading
# ---------------------------------------------------------------------------

def load_catalog(catalog_path: str) -> list[Hypothesis]:
    """Load a hypothesis catalog from a YAML file.

    The YAML file should contain a top-level ``hypotheses`` key whose value
    is a list of dicts, each with the fields of :class:`Hypothesis`.

    If the ``yaml`` package is not available, a JSON file (same structure)
    is loaded as a fallback.

    Parameters
    ----------
    catalog_path : str
        Path to the YAML (or JSON) catalog file.

    Returns
    -------
    list[Hypothesis]
        Parsed hypothesis records.  Returns an empty list if the file
        exists but contains no hypotheses.

    Raises
    ------
    FileNotFoundError
        If the file does not exist.
    ValueError
        If the file format is unrecognised or a hypothesis dict is missing
        required fields.
    """
    path = Path(catalog_path)
    if not path.exists():
        raise FileNotFoundError(f"Hypothesis catalog not found: {catalog_path}")

    raw: Any = None
    suffix = path.suffix.lower()

    if suffix in (".yaml", ".yml"):
        try:
            import yaml
        except ImportError:
            # Fall back to JSON if yaml is unavailable and the file is
            # actually JSON-formatted.
            try:
                with open(path, "r", encoding="utf-8") as fh:
                    raw = json.load(fh)
            except json.JSONDecodeError:
                raise ImportError(
                    "PyYAML is required to load .yaml catalogs. "
                    "Install it with: pip install pyyaml"
                )
        else:
            with open(path, "r", encoding="utf-8") as fh:
                raw = yaml.safe_load(fh)
    elif suffix == ".json":
        with open(path, "r", encoding="utf-8") as fh:
            raw = json.load(fh)
    else:
        # Try YAML first, then JSON.
        try:
            import yaml
            with open(path, "r", encoding="utf-8") as fh:
                raw = yaml.safe_load(fh)
        except ImportError:
            with open(path, "r", encoding="utf-8") as fh:
                raw = json.load(fh)

    if raw is None:
        return []

    items = raw.get("hypotheses", []) if isinstance(raw, dict) else raw
    if not isinstance(items, list):
        raise ValueError(
            f"Catalog must contain a 'hypotheses' list, got {type(items).__name__}"
        )

    required_fields = {
        "hypothesis_id",
        "hypothesis_class",
        "description",
        "minimal_expression",
        "ablation_no_gate",
        "control_constant",
        "variant",
        "expected_direction",
    }

    hypotheses: list[Hypothesis] = []
    for i, item in enumerate(items):
        if not isinstance(item, dict):
            raise ValueError(f"Hypothesis #{i} is not a dict: {item!r}")
        missing = required_fields - set(item.keys())
        if missing:
            raise ValueError(
                f"Hypothesis #{i} missing required fields: {sorted(missing)}"
            )
        hypotheses.append(Hypothesis(
            hypothesis_id=item["hypothesis_id"],
            hypothesis_class=item["hypothesis_class"],
            description=item["description"],
            minimal_expression=item["minimal_expression"],
            ablation_no_gate=item["ablation_no_gate"],
            control_constant=item["control_constant"],
            variant=item["variant"],
            expected_direction=item["expected_direction"],
        ))
    return hypotheses


# ---------------------------------------------------------------------------
# Experiment dispatch
# ---------------------------------------------------------------------------

def run_hypothesis_round(
    catalog_path: str,
    max_hypotheses: int = 1,
) -> dict:
    """Build a 4-alpha experiment plan for one or more hypotheses.

    This function does **not** execute simulations.  It loads the catalog,
    selects up to ``max_hypotheses`` entries, and returns a dict keyed by
    ``hypothesis_id`` where each value contains the four expressions ready
    for ``create_multi_simulation``.

    Parameters
    ----------
    catalog_path : str
        Path to the hypothesis catalog YAML file.
    max_hypotheses : int, optional
        Maximum number of hypotheses to include in this round (default 1,
        i.e. one 4-alpha experiment per batch).

    Returns
    -------
    dict
        ``{hypothesis_id: {"expressions": [str, ...], "hypothesis": Hypothesis}}``

    Raises
    ------
    ValueError
        If ``max_hypotheses`` is not positive.
    FileNotFoundError
        If the catalog file does not exist.
    """
    if max_hypotheses < 1:
        raise ValueError("max_hypotheses must be >= 1")

    catalog = load_catalog(catalog_path)
    selected = catalog[:max_hypotheses]

    experiments: dict[str, dict] = {}
    for hyp in selected:
        experiments[hyp.hypothesis_id] = {
            "expressions": [
                hyp.minimal_expression,
                hyp.ablation_no_gate,
                hyp.control_constant,
                hyp.variant,
            ],
            "hypothesis": hyp,
        }
    return experiments


# ---------------------------------------------------------------------------
# Judging
# ---------------------------------------------------------------------------

#: Sharpe-difference threshold below which primary ~= control is a pseudo-signal.
_PSEUDO_SIGNAL_THRESHOLD: float = 0.1

#: Sharpe-difference threshold for PARTIALLY_SUPPORTED (above control by this much).
_PARTIAL_THRESHOLD: float = 0.1

#: Sharpe-difference threshold for SUPPORTED (above control by this much).
_SUPPORTED_THRESHOLD: float = 0.3

#: Minimum primary Sharpe below which the hypothesis needs refinement.
_REFINEMENT_FLOOR: float = 0.3

#: Minimum primary fitness for SUPPORTED verdict.
_SUPPORTED_FITNESS: float = 0.8


def judge(result: ExperimentResult) -> dict:
    """Evaluate an experiment result and return a verdict.

    Decision logic (applied in order):

    1. **REJECTED** -- ``primary_sharpe`` is within
       ``_PSEUDO_SIGNAL_THRESHOLD`` of ``control_sharpe``.  This means the
       "signal" is no better than a constant; it's a pseudo-signal.

    2. **NEEDS_REFINEMENT** -- ``primary_sharpe`` is below
       ``_REFINEMENT_FLOOR`` (the hypothesis is too weak to be worth
       chasing in its current form).

    3. **SUPPORTED** -- ``primary_sharpe`` exceeds ``control_sharpe`` by
       more than ``_SUPPORTED_THRESHOLD`` **and** ``primary_fitness`` is
       above ``_SUPPORTED_FITNESS``.

    4. **PARTIALLY_SUPPORTED** -- ``primary_sharpe`` exceeds
       ``control_sharpe`` by more than ``_PARTIAL_THRESHOLD`` but does not
       meet the SUPPORTED bar.

    Parameters
    ----------
    result : ExperimentResult
        The four-alpha experiment results.

    Returns
    -------
    dict
        ``{
            "status": HypothesisVerdict,
            "reason": str,
            "diagnostics": {
                "sharpe_delta": float,
                "ablation_delta": float,
                "variant_delta": float,
                "fitness_delta": float,
                "pseudo_signal": bool,
            }
        }``
    """
    sharpe_delta = result.primary_sharpe - result.control_sharpe
    ablation_delta = result.primary_sharpe - result.ablation_sharpe
    variant_delta = result.primary_sharpe - result.variant_sharpe
    fitness_delta = result.primary_fitness - result.control_fitness
    pseudo_signal = abs(sharpe_delta) < _PSEUDO_SIGNAL_THRESHOLD

    diagnostics: dict[str, Any] = {
        "sharpe_delta": round(sharpe_delta, 4),
        "ablation_delta": round(ablation_delta, 4),
        "variant_delta": round(variant_delta, 4),
        "fitness_delta": round(fitness_delta, 4),
        "pseudo_signal": pseudo_signal,
    }

    # 1. Pseudo-signal: primary ~= control
    if pseudo_signal:
        return {
            "status": HypothesisVerdict.REJECTED,
            "reason": (
                f"Pseudo-signal: primary Sharpe ({result.primary_sharpe:.4f}) is "
                f"within {_PSEUDO_SIGNAL_THRESHOLD} of control Sharpe "
                f"({result.control_sharpe:.4f}). The 'signal' is no better "
                f"than a constant."
            ),
            "diagnostics": diagnostics,
        }

    # 2. Too weak to be worth chasing
    if result.primary_sharpe < _REFINEMENT_FLOOR:
        return {
            "status": HypothesisVerdict.NEEDS_REFINEMENT,
            "reason": (
                f"Primary Sharpe ({result.primary_sharpe:.4f}) is below the "
                f"refinement floor ({_REFINEMENT_FLOOR}). The hypothesis "
                f"needs a stronger formulation before further testing."
            ),
            "diagnostics": diagnostics,
        }

    # 3. Supported: strong signal above control AND good fitness
    if sharpe_delta > _SUPPORTED_THRESHOLD and result.primary_fitness > _SUPPORTED_FITNESS:
        return {
            "status": HypothesisVerdict.SUPPORTED,
            "reason": (
                f"Primary Sharpe ({result.primary_sharpe:.4f}) exceeds control "
                f"by {sharpe_delta:.4f} (>{_SUPPORTED_THRESHOLD}) and fitness "
                f"({result.primary_fitness:.4f}) is above "
                f"{_SUPPORTED_FITNESS}. Hypothesis is supported."
            ),
            "diagnostics": diagnostics,
        }

    # 4. Partially supported: above control but not strong enough
    if sharpe_delta > _PARTIAL_THRESHOLD:
        return {
            "status": HypothesisVerdict.PARTIALLY_SUPPORTED,
            "reason": (
                f"Primary Sharpe ({result.primary_sharpe:.4f}) exceeds control "
                f"by {sharpe_delta:.4f} (>{_PARTIAL_THRESHOLD}) but does not "
                f"meet SUPPORTED bar (Sharpe delta >{_SUPPORTED_THRESHOLD} "
                f"and fitness >{_SUPPORTED_FITNESS}). Current fitness = "
                f"{result.primary_fitness:.4f}."
            ),
            "diagnostics": diagnostics,
        }

    # 5. Default: needs refinement (signal exists but is marginal)
    return {
        "status": HypothesisVerdict.NEEDS_REFINEMENT,
        "reason": (
            f"Primary Sharpe ({result.primary_sharpe:.4f}) is above the "
            f"refinement floor but only exceeds control by {sharpe_delta:.4f} "
            f"(<= {_PARTIAL_THRESHOLD}). The hypothesis shows a weak effect "
            f"that needs refinement."
        ),
        "diagnostics": diagnostics,
    }


# ---------------------------------------------------------------------------
# Ledger persistence
# ---------------------------------------------------------------------------

def save_to_ledger(
    result: dict,
    session_id: str,
    ledger_dir: str = "data/hypothesis_ledger",
) -> str:
    """Append a judge result to the hypothesis ledger (JSONL).

    The ledger accumulates across sessions and powers meta-learning over
    hypothesis classes.  Each line is a JSON object containing the session
    id, the verdict, the reason, the diagnostics, and a UTC timestamp.

    Parameters
    ----------
    result : dict
        The dict returned by ``judge()``.  Must contain ``"status"``,
        ``"reason"``, and ``"diagnostics"`` keys.  If the dict also
        contains an ``"experiment_result"`` key (an ``ExperimentResult``),
        it is serialised alongside.
    session_id : str
        An identifier for the current mining session (e.g.
        ``"2026-04-23_news12_hypothesis"``).
    ledger_dir : str, optional
        Directory where ledger files are stored.

    Returns
    -------
    str
        The absolute path to the ledger file (as a string).
    """
    from datetime import datetime, timezone

    ledger_path = Path(ledger_dir) / f"{session_id}.jsonl"
    ledger_path.parent.mkdir(parents=True, exist_ok=True)

    # Extract and serialise the ExperimentResult if present
    experiment_result = result.get("experiment_result")
    experiment_dict: Optional[dict] = None
    if isinstance(experiment_result, ExperimentResult):
        experiment_dict = experiment_result.to_dict()
    elif isinstance(experiment_result, dict):
        experiment_dict = experiment_result

    # Extract and serialise the Hypothesis if present
    hypothesis = result.get("hypothesis")
    hypothesis_dict: Optional[dict] = None
    if isinstance(hypothesis, Hypothesis):
        hypothesis_dict = hypothesis.to_dict()
    elif isinstance(hypothesis, dict):
        hypothesis_dict = hypothesis

    status = result.get("status")
    status_value = status.value if isinstance(status, HypothesisVerdict) else status

    record = {
        "session_id": session_id,
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "status": status_value,
        "reason": result.get("reason", ""),
        "diagnostics": result.get("diagnostics", {}),
        "experiment_result": experiment_dict,
        "hypothesis": hypothesis_dict,
    }

    with open(ledger_path, "a", encoding="utf-8") as fh:
        fh.write(json.dumps(record, ensure_ascii=False) + "\n")

    return str(ledger_path.resolve())
