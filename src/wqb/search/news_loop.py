"""News/sentiment closed-loop mining orchestrator.

Implements the 6-bucket news framework (orchestrator §15, 2026-04-23) for
news, sentiment, and socialmedia datasets.  Uses Beta-posterior bucket
sampling biased toward Dispersion / Event-conditioned / Propagation (the
HIGH-priority trio), cross-family field pairing, event-gated template
inclusion, and failure attribution per result.

The 6 buckets
-------------
1. **LEVEL** — raw field level (e.g. sentiment score).
2. **CHANGE** — short-horizon change or delta.
3. **SURPRISE** — deviation from baseline / expectation.
4. **DISPERSION** — stddev, novelty, uncertainty, disagreement (HIGH).
5. **EVENT_CONDITIONED** — alpha only trades on event/anomaly days (HIGH).
6. **PROPAGATION** — cross-stock or cross-sector spillover (HIGH).

Public API
----------
- :class:`NewsBucket` — enum of the 6 buckets.
- :class:`NewsLoop` — closed-loop mining orchestrator.
- :data:`HIGH_PRIORITY_BUCKETS` — set of HIGH-priority buckets.
- :data:`MAX_ATTEMPTS` — max structurally-distinct attempts (50).
- :data:`EARLY_STOP_CONSECUTIVE_ZERO` — early-stop threshold (15).
"""

from __future__ import annotations

import math
import random
from enum import Enum
from typing import Dict, List, Optional, Tuple

from ..expression.operator_audit import GhostOperatorError, ensure_safe_for_dispatch
from ..expression.validator import check_batch


# ---------------------------------------------------------------------------
# NewsBucket enum
# ---------------------------------------------------------------------------


class NewsBucket(str, Enum):
    """The 6 news/sentiment mining buckets.

    Inherits ``str`` so members are JSON-serialisable and can be used as
    dict keys directly.
    """

    LEVEL = "level"
    CHANGE = "change"
    SURPRISE = "surprise"
    DISPERSION = "dispersion"
    EVENT_CONDITIONED = "event_conditioned"
    PROPAGATION = "propagation"


# HIGH-priority buckets: Dispersion, Event-conditioned, Propagation.
HIGH_PRIORITY_BUCKETS: set = {
    NewsBucket.DISPERSION,
    NewsBucket.EVENT_CONDITIONED,
    NewsBucket.PROPAGATION,
}

# Escalation: 30 → 50 structurally-distinct attempts (more shots on goal).
MAX_ATTEMPTS: int = 50

# Early-stop after 15 consecutive zero-PASS iterations clustering in ≤2 buckets.
EARLY_STOP_CONSECUTIVE_ZERO: int = 15

# Field families (from news_field_classifier.py).
FIELD_FAMILIES: tuple = (
    "direction",
    "attention",
    "dispersion",
    "event_type",
    "peer_context",
)

# Default Beta prior parameters for bucket sampling.
# Alpha/Beta biased toward HIGH-priority buckets (D/E/P).
_BETA_PRIORS: Dict[NewsBucket, Tuple[float, float]] = {
    NewsBucket.LEVEL: (2.0, 3.0),
    NewsBucket.CHANGE: (3.0, 2.0),
    NewsBucket.SURPRISE: (3.0, 2.0),
    NewsBucket.DISPERSION: (5.0, 1.5),       # HIGH
    NewsBucket.EVENT_CONDITIONED: (5.0, 1.5),  # HIGH
    NewsBucket.PROPAGATION: (4.5, 1.5),       # HIGH
}

# Bucket → compatible field family pairs.
_BUCKET_FAMILY_MAP: Dict[NewsBucket, List[Tuple[str, str]]] = {
    NewsBucket.LEVEL: [
        ("direction", "direction"),
        ("direction", "attention"),
    ],
    NewsBucket.CHANGE: [
        ("direction", "direction"),
        ("attention", "attention"),
    ],
    NewsBucket.SURPRISE: [
        ("direction", "dispersion"),
        ("attention", "dispersion"),
    ],
    NewsBucket.DISPERSION: [
        ("dispersion", "dispersion"),
        ("dispersion", "direction"),
    ],
    NewsBucket.EVENT_CONDITIONED: [
        ("event_type", "direction"),
        ("event_type", "attention"),
    ],
    NewsBucket.PROPAGATION: [
        ("peer_context", "direction"),
        ("peer_context", "attention"),
    ],
}

# Bucket → expression template strings.
_BUCKET_TEMPLATES: Dict[NewsBucket, List[str]] = {
    NewsBucket.LEVEL: [
        "rank({a}) - rank({b})",
        "zscore({a}) - zscore({b})",
    ],
    NewsBucket.CHANGE: [
        "ts_delta({a}, 5) - ts_delta({b}, 5)",
        "ts_av_diff({a}, 10) - ts_av_diff({b}, 10)",
    ],
    NewsBucket.SURPRISE: [
        "({a} - ts_mean({a}, 20)) / ts_std_dev({a}, 20)",
        "({b} - ts_mean({b}, 20)) * rank({a})",
    ],
    NewsBucket.DISPERSION: [
        "ts_std_dev({a}, 10) - ts_std_dev({b}, 10)",
        "rank(ts_std_dev({a}, 20)) * sign({b})",
    ],
    NewsBucket.EVENT_CONDITIONED: [
        "trade_when(ts_std_dev({a}, 5) > ts_std_dev({a}, 60), {b}, 0)",
        "trade_when(rank({a}) > 0.8, ts_delta({b}, 5), 0)",
    ],
    NewsBucket.PROPAGATION: [
        "group_rank({a}, sector) - group_rank({b}, sector)",
        "ts_delay(rank({a}), 5) - rank({b})",
    ],
}

# Vector operators for vec_op rotation when fields are VECTOR type.
_VEC_OPS: List[str] = ["vec_avg", "vec_sum", "vec_max", "vec_min", "vec_norm"]


# ---------------------------------------------------------------------------
# NewsLoop
# ---------------------------------------------------------------------------


class NewsLoop:
    """Closed-loop news/sentiment mining orchestrator.

    Parameters
    ----------
    dataset_id : str
        Target dataset ID (e.g. ``"news12"``).
    region : str
        Region code (default ``"USA"``).
    universe : str
        Trading universe (default ``"TOP3000"``).
    delay : int
        Data delay (default 1).

    Examples
    --------
    >>> loop = NewsLoop("news12", region="USA", universe="TOP3000", delay=1)
    >>> batch = [{"expression": "rank(a) - rank(b)", "bucket": NewsBucket.LEVEL}]
    >>> ok, reason, details = loop.enforce_batch_diversity(batch)
    """

    def __init__(
        self,
        dataset_id: str,
        region: str = "USA",
        universe: str = "TOP3000",
        delay: int = 1,
    ):
        self.dataset_id = dataset_id
        self.region = region
        self.universe = universe
        self.delay = delay

        # Beta posteriors: (alpha, beta) per bucket, updated by results.
        self._posteriors: Dict[NewsBucket, Tuple[float, float]] = {
            bucket: priors for bucket, priors in _BETA_PRIORS.items()
        }

        # Tracking for early-stop
        self._consecutive_zero: int = 0
        self._recent_buckets: List[NewsBucket] = []

    # ------------------------------------------------------------------
    # Batch diversity enforcement
    # ------------------------------------------------------------------

    def enforce_batch_diversity(
        self,
        batch: List[dict],
    ) -> Tuple[bool, str, dict]:
        """Validate batch diversity for the news 6-bucket framework.

        Enforces:
        1. **≥3 distinct buckets** per batch.
        2. **≥1 HIGH-priority bucket** (Dispersion / Event-conditioned /
           Propagation).
        3. **≥2 distinct vec_ops** when vector fields are present.
        4. **check_batch shape_variety ≥2** (delegates to
           :func:`wqb.expression.validator.check_batch`).

        Parameters
        ----------
        batch : list[dict]
            List of batch items.  Each item should have at least an
            ``"expression"`` key and a ``"bucket"`` key (NewsBucket or str).

        Returns
        -------
        tuple[bool, str, dict]
            ``(ok, reason, details)`` where *ok* is True iff all gates pass.
        """
        if not batch:
            return False, "empty batch", {"gate": "empty"}

        # Extract buckets
        buckets: List[NewsBucket] = []
        for item in batch:
            b = item.get("bucket")
            if isinstance(b, str):
                try:
                    b = NewsBucket(b)
                except ValueError:
                    b = None
            if b is not None:
                buckets.append(b)

        # Gate 1: ≥3 distinct buckets
        distinct_buckets = set(buckets)
        if len(distinct_buckets) < 3:
            return (
                False,
                f"distinct buckets {len(distinct_buckets)} < 3",
                {
                    "gate": "distinct_buckets",
                    "required": 3,
                    "actual": len(distinct_buckets),
                    "buckets": [b.value for b in distinct_buckets],
                },
            )

        # Gate 2: ≥1 HIGH-priority bucket
        high_count = len(distinct_buckets & HIGH_PRIORITY_BUCKETS)
        if high_count < 1:
            return (
                False,
                "no HIGH-priority bucket (need ≥1 of Dispersion/Event/Propagation)",
                {
                    "gate": "high_priority",
                    "required": 1,
                    "actual": 0,
                    "buckets": [b.value for b in distinct_buckets],
                },
            )

        # Gate 3: ≥2 distinct vec_ops when vectors present
        vec_ops_found: set = set()
        has_vectors = any(
            item.get("field_type") == "VECTOR" or item.get("is_vector", False)
            for item in batch
        )
        if has_vectors:
            for item in batch:
                vop = item.get("vec_op")
                if vop:
                    vec_ops_found.add(vop)
            if len(vec_ops_found) < 2:
                return (
                    False,
                    f"distinct vec_ops {len(vec_ops_found)} < 2 (vectors present)",
                    {
                        "gate": "vec_ops",
                        "required": 2,
                        "actual": len(vec_ops_found),
                        "vec_ops": sorted(vec_ops_found),
                    },
                )

        # Gate 4: check_batch shape_variety ≥2
        expressions = [item.get("expression", "") for item in batch]
        expressions = [e for e in expressions if e]
        if expressions:
            ok, reason, details = check_batch(expressions)
            if not ok:
                # Check specifically for shape_variety failure
                gates = details.get("gates", {})
                shape_gate = gates.get("shape_signatures", {})
                if not shape_gate.get("passed", True):
                    return (
                        False,
                        f"check_batch shape_variety failed: {reason}",
                        {
                            "gate": "shape_variety",
                            "required": 2,
                            "actual": details.get("distinct_shape_count", 0),
                            "validator_details": details,
                        },
                    )
                # Other check_batch failures also fail diversity
                return (
                    False,
                    f"check_batch failed: {reason}",
                    {
                        "gate": "check_batch",
                        "reason": reason,
                        "validator_details": details,
                    },
                )

        return (
            True,
            "all diversity gates passed",
            {
                "gate": "all_passed",
                "distinct_buckets": len(distinct_buckets),
                "high_priority_count": high_count,
                "buckets": [b.value for b in distinct_buckets],
                "vec_ops": sorted(vec_ops_found) if has_vectors else [],
                "expression_count": len(expressions),
            },
        )

    # ------------------------------------------------------------------
    # Ghost operator guard
    # ------------------------------------------------------------------

    def ensure_safe_for_dispatch(self, expressions: List[str]) -> None:
        """Check for ghost operators before dispatch.

        Calls :func:`wqb.expression.operator_audit.ensure_safe_for_dispatch`.
        If a ghost operator is found, raises :class:`GhostOperatorError`
        before the MCP ``create_multi_simulation`` call.

        Parameters
        ----------
        expressions : list[str]
            Batch of expression strings about to be dispatched.

        Raises
        ------
        GhostOperatorError
            If any expression contains an operator not verified on the
            platform.
        """
        ensure_safe_for_dispatch(expressions)

    # ------------------------------------------------------------------
    # Beta-posterior bucket sampling
    # ------------------------------------------------------------------

    def sample_buckets(
        self,
        field_families: dict,
        max_attempts: int = MAX_ATTEMPTS,
    ) -> List[dict]:
        """Sample buckets using Beta posteriors, biased toward D/E/P.

        The Beta posterior for each bucket is updated by simulation results:
        a PASS increments alpha, a FAIL increments beta.  The sampling is
        biased toward HIGH-priority buckets (Dispersion, Event-conditioned,
        Propagation) via higher prior alpha values.

        Parameters
        ----------
        field_families : dict
            Mapping of field name → family name (e.g.
            ``{"news_ton_last": "direction", "news_vol_stddev": "dispersion"}``).
            Used to determine which buckets are feasible (a bucket is
            feasible if the required field families are present).
        max_attempts : int
            Maximum sampling attempts (default 50).

        Returns
        -------
        list[dict]
            List of sampled bucket descriptors, each:
            ``{"bucket": NewsBucket, "fields": [str, str], "template": str}``
        """
        available_families = set(field_families.values())
        all_buckets = list(NewsBucket)
        sampled: List[dict] = []
        attempts = 0

        while len(sampled) < 4 and attempts < max_attempts:
            attempts += 1

            # Sample a bucket using Beta posterior
            bucket = self._sample_one_bucket(all_buckets, available_families)
            if bucket is None:
                continue

            # Find compatible field pair
            pair = self._find_field_pair(bucket, field_families, available_families)
            if pair is None:
                continue

            # Pick a template
            templates = _BUCKET_TEMPLATES.get(bucket, [])
            if not templates:
                continue
            template = random.choice(templates)

            # Avoid duplicate (bucket, template) combinations
            is_dup = any(
                s["bucket"] == bucket and s["template"] == template
                for s in sampled
            )
            if is_dup:
                continue

            sampled.append({
                "bucket": bucket,
                "fields": list(pair),
                "template": template,
            })

        return sampled

    def _sample_one_bucket(
        self,
        buckets: List[NewsBucket],
        available_families: set,
    ) -> Optional[NewsBucket]:
        """Sample one bucket from the Beta posterior, filtered by feasibility."""
        feasible = [
            b for b in buckets
            if self._is_bucket_feasible(b, available_families)
        ]
        if not feasible:
            return None

        # Sample using Beta posterior
        weights: List[float] = []
        for b in feasible:
            alpha, beta = self._posteriors[b]
            # Expected value of Beta(alpha, beta)
            weights.append(alpha / (alpha + beta))

        total = sum(weights)
        if total <= 0:
            return random.choice(feasible)

        r = random.random() * total
        cumulative = 0.0
        for i, w in enumerate(weights):
            cumulative += w
            if r <= cumulative:
                return feasible[i]
        return feasible[-1]

    def _is_bucket_feasible(
        self,
        bucket: NewsBucket,
        available_families: set,
    ) -> bool:
        """Check if a bucket is feasible given available field families."""
        family_pairs = _BUCKET_FAMILY_MAP.get(bucket, [])
        for fam_a, fam_b in family_pairs:
            if fam_a in available_families and fam_b in available_families:
                return True
        return False

    def _find_field_pair(
        self,
        bucket: NewsBucket,
        field_families: dict,
        available_families: set,
    ) -> Optional[Tuple[str, str]]:
        """Find a compatible field pair for a bucket."""
        family_pairs = _BUCKET_FAMILY_MAP.get(bucket, [])
        for fam_a, fam_b in family_pairs:
            if fam_a not in available_families or fam_b not in available_families:
                continue
            # Find actual fields
            fields_a = [f for f, fam in field_families.items() if fam == fam_a]
            fields_b = [f for f, fam in field_families.items() if fam == fam_b]
            if not fields_a or not fields_b:
                continue
            # Pick one field from each family (avoid same field)
            for fa in fields_a:
                for fb in fields_b:
                    if fa != fb:
                        return (fa, fb)
        return None

    # ------------------------------------------------------------------
    # Posterior update
    # ------------------------------------------------------------------

    def update_posterior(self, bucket: NewsBucket, passed: bool) -> None:
        """Update the Beta posterior for a bucket after a simulation.

        Parameters
        ----------
        bucket : NewsBucket
            The bucket that was simulated.
        passed : bool
            Whether the simulation passed qualification gates.
        """
        alpha, beta = self._posteriors[bucket]
        if passed:
            self._posteriors[bucket] = (alpha + 1.0, beta)
        else:
            self._posteriors[bucket] = (alpha, beta + 1.0)

    def get_posteriors(self) -> Dict[str, Tuple[float, float]]:
        """Return the current Beta posteriors as a dict."""
        return {b.value: v for b, v in self._posteriors.items()}

    # ------------------------------------------------------------------
    # Early-stop check
    # ------------------------------------------------------------------

    def check_early_stop(self, passed: bool, bucket: NewsBucket) -> bool:
        """Check whether the loop should early-stop.

        Early-stop after :data:`EARLY_STOP_CONSECUTIVE_ZERO` consecutive
        zero-PASS iterations that cluster in ≤2 buckets — that's framework
        drift, not a sampling problem.

        Parameters
        ----------
        passed : bool
            Whether the latest iteration produced any PASS.
        bucket : NewsBucket
            The bucket of the latest iteration.

        Returns
        -------
        bool
            ``True`` if the loop should stop.
        """
        if passed:
            self._consecutive_zero = 0
            self._recent_buckets = []
            return False

        self._consecutive_zero += 1
        self._recent_buckets.append(bucket)

        if self._consecutive_zero >= EARLY_STOP_CONSECUTIVE_ZERO:
            distinct = set(self._recent_buckets[-EARLY_STOP_CONSECUTIVE_ZERO:])
            if len(distinct) <= 2:
                return True

        return False

    # ------------------------------------------------------------------
    # Cross-family field pairing
    # ------------------------------------------------------------------

    def pair_fields(
        self,
        fields: List[dict],
        families: dict,
    ) -> List[Tuple[str, str]]:
        """Pair fields across families, avoiding same-family triplets.

        Rules (research SKILL §10):
        - Never three fields from the same family in a batch.
        - Prefer cross-family pairs (direction × dispersion, event × direction, etc.).
        - Avoid pairing two fields from the same family unless necessary.

        Parameters
        ----------
        fields : list[dict]
            List of field descriptors, each with at least a ``"name"`` key.
        families : dict
            Mapping of field name → family name.

        Returns
        -------
        list[tuple[str, str]]
            List of (field_a, field_b) pairs.
        """
        # Group fields by family
        by_family: Dict[str, List[str]] = {}
        for field in fields:
            name = field.get("name", field) if isinstance(field, dict) else str(field)
            fam = families.get(name, "unknown")
            by_family.setdefault(fam, []).append(name)

        families_list = list(by_family.keys())
        pairs: List[Tuple[str, str]] = []

        # First pass: cross-family pairs
        for i, fam_a in enumerate(families_list):
            for fam_b in families_list[i + 1:]:
                for fa in by_family[fam_a]:
                    for fb in by_family[fam_b]:
                        pairs.append((fa, fb))

        # Second pass: same-family pairs (only if we need more)
        for fam, field_list in by_family.items():
            if len(field_list) >= 2:
                for i in range(len(field_list)):
                    for j in range(i + 1, len(field_list)):
                        pairs.append((field_list[i], field_list[j]))

        return pairs

    # ------------------------------------------------------------------
    # Batch generation
    # ------------------------------------------------------------------

    def run_batch(
        self,
        fields: List,
        templates: List,
    ) -> List[str]:
        """Generate a batch of expressions from fields and templates.

        Parameters
        ----------
        fields : list
            List of field names or descriptors.  If a list of dicts, the
            ``"name"`` key is used.
        templates : list
            List of template strings with ``{a}`` and ``{b}`` placeholders.

        Returns
        -------
        list[str]
            List of rendered expression strings (up to 4, matching the
            ``create_multi_simulation`` batch size).
        """
        # Normalise field names
        field_names: List[str] = []
        for f in fields:
            if isinstance(f, dict):
                field_names.append(f.get("name", ""))
            else:
                field_names.append(str(f))
        field_names = [f for f in field_names if f]

        if len(field_names) < 2 or not templates:
            return []

        expressions: List[str] = []
        # Generate up to 4 expressions
        for i, template in enumerate(templates):
            if len(expressions) >= 4:
                break
            # Cycle through field pairs
            a = field_names[i % len(field_names)]
            b = field_names[(i + 1) % len(field_names)]
            if a == b and len(field_names) > 2:
                b = field_names[(i + 2) % len(field_names)]
            try:
                expr = template.format(a=a, b=b)
                expressions.append(expr)
            except (KeyError, IndexError):
                continue

        return expressions

    # ------------------------------------------------------------------
    # Failure attribution
    # ------------------------------------------------------------------

    def attribute_failure(self, result: dict) -> dict:
        """Attribute failure reasons for a simulation result.

        Examines the result's ``is.checks`` array and metric values to
        determine the structural cause of failure.  This drives the failure
        memory record so future attempts rotate shape even if the paradigm
        repeats.

        Parameters
        ----------
        result : dict
            Simulation result dict.  Expected to have an ``is`` key with
            ``checks`` array, and metric fields like ``sharpe``, ``fitness``,
            ``turnover``, ``returns``, ``drawdown``.

        Returns
        -------
        dict
            ``{"primary_cause": str, "failed_checks": list[str],
            "metrics": dict, "structural_cause": str}``
        """
        is_data = result.get("is", result)
        checks = is_data.get("checks", [])

        # Collect failed check names
        failed_checks: List[str] = []
        for check in checks:
            if isinstance(check, dict):
                if check.get("result") not in ("PASS", "PENDING"):
                    failed_checks.append(check.get("name", "unknown"))

        # Extract metrics
        metrics = {
            "sharpe": is_data.get("sharpe", result.get("sharpe", 0)),
            "fitness": is_data.get("fitness", result.get("fitness", 0)),
            "turnover": is_data.get("turnover", result.get("turnover", 0)),
            "returns": is_data.get("returns", result.get("returns", 0)),
            "drawdown": is_data.get("drawdown", result.get("drawdown", 0)),
            "margin": is_data.get("margin", result.get("margin", 0)),
        }

        # Determine primary cause
        primary_cause = "unknown"
        if "HIGH_TURNOVER" in failed_checks:
            primary_cause = "high_turnover"
        elif "LOW_TURNOVER" in failed_checks:
            primary_cause = "low_turnover"
        elif "LOW_SHARPE" in failed_checks:
            primary_cause = "low_sharpe"
        elif "LOW_FITNESS" in failed_checks:
            primary_cause = "low_fitness"
        elif "LOW_RETURNS" in failed_checks:
            primary_cause = "low_returns"
        elif "CONCENTRATED_WEIGHT" in failed_checks:
            primary_cause = "concentrated_weight"
        elif "LOW_SUB_UNIVERSE_SHARPE" in failed_checks:
            primary_cause = "sub_universe_fragile"
        elif "LOW_2Y_SHARPE" in failed_checks:
            primary_cause = "recent_decay"
        elif failed_checks:
            primary_cause = failed_checks[0].lower()

        # Structural cause for failure memory
        structural_cause = primary_cause
        if primary_cause in ("concentrated_weight",):
            structural_cause = "coverage_insufficient"
        elif primary_cause in ("high_turnover",):
            structural_cause = "signal_too_noisy"
        elif primary_cause in ("low_sharpe", "low_fitness", "low_returns"):
            structural_cause = "weak_signal"
        elif primary_cause in ("sub_universe_fragile", "recent_decay"):
            structural_cause = "regime_fragile"

        return {
            "primary_cause": primary_cause,
            "failed_checks": failed_checks,
            "metrics": metrics,
            "structural_cause": structural_cause,
        }
