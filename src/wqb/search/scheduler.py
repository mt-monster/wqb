"""Scheduler: budget allocation and session-pack generation.

Implements the planning layer (orchestrator §3).  The scheduler allocates
simulation budget by uncovered category, region priority, and search
coverage.  It also generates and validates handoff session packs for MCP
execution.

Public API
----------
- :class:`Scheduler` — budget allocator and plan generator.
"""

from __future__ import annotations

import json
import os
from datetime import datetime, timezone
from typing import Dict, List, Optional

from ..config import (
    REGIONS,
    REGION_PRIORITY,
    PARADIGMS,
    neutralization_search_order,
    default_universe,
    get_categories,
    is_news_dataset,
)
from . import failure_memory


# ---------------------------------------------------------------------------
# Default dataset catalogue (seed for planning)
# ---------------------------------------------------------------------------

# A minimal dataset catalogue used when no external catalogue is provided.
# Maps category -> list of {"dataset": id, "region": region, "priority": int}.
_SEED_DATASETS: Dict[str, List[dict]] = {
    "fundamental": [
        {"dataset": "fundamental6", "region": "USA"},
        {"dataset": "fundamental2", "region": "USA"},
    ],
    "analyst": [
        {"dataset": "analyst4", "region": "USA"},
        {"dataset": "analyst11", "region": "USA"},
        {"dataset": "analyst14", "region": "USA"},
    ],
    "news": [
        {"dataset": "news12", "region": "USA"},
        {"dataset": "news94", "region": "USA"},
        {"dataset": "news29", "region": "USA"},
    ],
    "sentiment": [
        {"dataset": "sentiment22", "region": "USA"},
        {"dataset": "sentiment23", "region": "USA"},
    ],
    "socialmedia": [
        {"dataset": "socialmedia12", "region": "USA"},
    ],
    "model": [
        {"dataset": "model26", "region": "USA"},
        {"dataset": "model165", "region": "USA"},
    ],
    "option": [
        {"dataset": "option3", "region": "USA"},
        {"dataset": "option6", "region": "USA"},
    ],
    "risk": [
        {"dataset": "risk60", "region": "USA"},
        {"dataset": "risk88", "region": "USA"},
    ],
    "pricevolume": [
        {"dataset": "pricevolume10", "region": "USA"},
    ],
}


# ---------------------------------------------------------------------------
# Scheduler
# ---------------------------------------------------------------------------


class Scheduler:
    """Budget allocator and search-plan generator.

    Parameters
    ----------
    db : SimulationDB or None
        Optional simulation database for coverage queries.  If ``None``,
        budget allocation uses category coverage heuristics only.
    failure_memory_file : str
        Path to the failure memory JSONL file.  Used to deprioritise
        arms that have already failed.

    Examples
    --------
    >>> sched = Scheduler()
    >>> plan = sched.plan("2026-04-22", region="USA", budget=300)
    >>> plan["budget"]
    300
    >>> len(plan["neutralization_sweep"])  # USA has 11 neutralizations
    11
    """

    def __init__(
        self,
        db=None,
        failure_memory_file: str = "data/failure_memory.jsonl",
    ):
        self.db = db
        self.failure_memory_file = failure_memory_file

    # ------------------------------------------------------------------
    # Plan
    # ------------------------------------------------------------------

    def plan(
        self,
        date: str,
        region: str = "USA",
        universe: str = "TOP3000",
        delay: int = 1,
        budget: int = 300,
    ) -> dict:
        """Generate a search plan for the given date and region.

        The plan allocates simulation budget across category/dataset/paradigm
        arms, deprioritising arms that have been recorded as failures.

        Parameters
        ----------
        date : str
            Planning date in ``YYYY-MM-DD`` format.
        region : str
            Region code (default ``"USA"``).
        universe : str
            Trading universe.  For USA REGULAR mining this defaults to
            ``"TOP3000"`` (orchestrator rule §4).
        delay : int
            Data delay (0 or 1).  Default 1.
        budget : int
            Total simulation budget for the day.

        Returns
        -------
        dict
            ``{"date": str, "region": str, "universe": str, "delay": int,
            "arms": list[dict], "budget": int, "neutralization_sweep": list[str]}``

            Each arm is:
            ``{"category": str, "dataset": str, "universe": str,
            "paradigms": list[str], "budget_allocation": int}``
        """
        # Validate region
        if region not in REGIONS:
            raise ValueError(
                f"Unknown region: {region!r}. Known: {sorted(REGIONS)}"
            )

        # For USA, enforce default universe if not specified explicitly
        if region == "USA" and universe is None:
            universe = default_universe("USA")

        # Get neutralization sweep for the region (full, never collapsed)
        neut_sweep = neutralization_search_order(region)

        # Get categories for the region
        categories = get_categories(region)

        # Build candidate arms
        raw_arms = self._build_arms(categories, region, universe)

        # Filter out deprioritised arms (failure memory)
        active_arms = self._filter_failed_arms(raw_arms)

        # Allocate budget across arms
        arms_with_budget = self.allocate_budget(active_arms, budget)

        return {
            "date": date,
            "region": region,
            "universe": universe,
            "delay": delay,
            "arms": arms_with_budget,
            "budget": budget,
            "neutralization_sweep": neut_sweep,
        }

    # ------------------------------------------------------------------
    # Arm construction
    # ------------------------------------------------------------------

    def _build_arms(
        self,
        categories: List[str],
        region: str,
        universe: str,
    ) -> List[dict]:
        """Build candidate arms from the dataset catalogue.

        Each arm is a (category, dataset, universe, paradigms) tuple.
        Paradigms are filtered to those applicable to the dataset type.
        """
        arms: List[dict] = []
        for category in categories:
            datasets = _SEED_DATASETS.get(category, [])
            for ds_info in datasets:
                # Only include datasets for the target region
                if ds_info.get("region", region) != region:
                    continue
                dataset_id = ds_info["dataset"]

                # Select paradigms appropriate for the dataset
                paradigms = self._select_paradigms(category, dataset_id)

                arms.append({
                    "category": category,
                    "dataset": dataset_id,
                    "universe": universe,
                    "paradigms": paradigms,
                    "budget_allocation": 0,  # will be set by allocate_budget
                })

        # If no seed datasets matched, create at least one arm per category
        if not arms:
            for category in categories:
                paradigms = self._select_paradigms(category, "")
                arms.append({
                    "category": category,
                    "dataset": f"{category}_default",
                    "universe": universe,
                    "paradigms": paradigms,
                    "budget_allocation": 0,
                })

        return arms

    def _select_paradigms(self, category: str, dataset_id: str) -> List[str]:
        """Select paradigms appropriate for a dataset.

        For news/sentiment datasets, all 13 paradigms are eligible (the
        news_loop will further filter by bucket).  For other categories,
        all paradigms are also eligible — the scheduler does not pre-filter
        paradigm coverage; that is the job of the search loop.
        """
        return list(PARADIGMS)

    def _filter_failed_arms(self, arms: List[dict]) -> List[dict]:
        """Remove arms that have been recorded as failures.

        Checks the failure memory for each arm's signature.  An arm is
        deprioritised if *all* of its paradigms have failed for the given
        (category, dataset, universe) combination.
        """
        if not arms:
            return arms

        filtered: List[dict] = []
        for arm in arms:
            paradigms = arm.get("paradigms", [])
            # Check if ALL paradigms for this arm have failed
            all_failed = True
            for paradigm in paradigms:
                if not failure_memory.is_deprioritized(
                    category=arm["category"],
                    dataset=arm["dataset"],
                    universe=arm["universe"],
                    paradigm=paradigm,
                    shape_bucket="",  # any shape
                    memory_file=self.failure_memory_file,
                ):
                    all_failed = False
                    break

            if not all_failed:
                filtered.append(arm)

        return filtered

    # ------------------------------------------------------------------
    # Budget allocation
    # ------------------------------------------------------------------

    def allocate_budget(
        self,
        arms: List[dict],
        total_budget: int,
    ) -> List[dict]:
        """Allocate budget across arms by category coverage and priority.

        The allocation strategy:
        1. Count arms per category.
        2. Weight categories by inverse coverage (fewer arms = higher weight)
           and region priority.
        3. Distribute budget proportionally, ensuring each arm gets at least
           a minimum allocation (enough for one batch of 4 simulations).

        Parameters
        ----------
        arms : list[dict]
            List of arm dicts (each with ``category``, ``dataset``,
            ``universe``, ``paradigms``).
        total_budget : int
            Total simulation budget to distribute.

        Returns
        -------
        list[dict]
            The same arms with ``budget_allocation`` set.
        """
        if not arms:
            return arms

        if total_budget <= 0:
            for arm in arms:
                arm["budget_allocation"] = 0
            return arms

        # Minimum allocation per arm (one batch = 4 sims)
        min_per_arm = 4
        n_arms = len(arms)

        # If budget is too small, give minimum to as many arms as possible
        if total_budget < min_per_arm * n_arms:
            # Give minimum to the first arms that fit
            remaining = total_budget
            for arm in arms:
                if remaining >= min_per_arm:
                    arm["budget_allocation"] = min_per_arm
                    remaining -= min_per_arm
                else:
                    arm["budget_allocation"] = remaining
                    remaining = 0
            return arms

        # Count arms per category for coverage weighting
        category_counts: Dict[str, int] = {}
        for arm in arms:
            cat = arm["category"]
            category_counts[cat] = category_counts.get(cat, 0) + 1

        # Compute weight per arm: inverse category coverage × region priority
        # Categories with fewer arms get higher per-arm weight.
        weights: List[float] = []
        for arm in arms:
            cat = arm["category"]
            coverage = category_counts[cat]
            # Inverse coverage: fewer arms in category → higher weight
            inv_coverage = 1.0 / max(coverage, 1)
            # Region priority (default to medium)
            region = arm.get("region", "USA")
            priority = REGION_PRIORITY.get(region, 1)
            weights.append(inv_coverage * priority)

        total_weight = sum(weights)
        if total_weight <= 0:
            # Equal distribution fallback
            per_arm = total_budget // n_arms
            remainder = total_budget - per_arm * n_arms
            for i, arm in enumerate(arms):
                arm["budget_allocation"] = per_arm + (1 if i < remainder else 0)
            return arms

        # Proportional allocation with minimum floor
        reserved = min_per_arm * n_arms
        flexible = total_budget - reserved

        for i, arm in enumerate(arms):
            base = min_per_arm
            extra = int(flexible * weights[i] / total_weight)
            arm["budget_allocation"] = base + extra

        # Distribute any remainder from integer truncation
        allocated = sum(a["budget_allocation"] for a in arms)
        remainder = total_budget - allocated
        idx = 0
        while remainder > 0 and arms:
            arms[idx % n_arms]["budget_allocation"] += 1
            remainder -= 1
            idx += 1

        return arms

    # ------------------------------------------------------------------
    # Session pack
    # ------------------------------------------------------------------

    def prepare_session_pack(
        self,
        date: str,
        materialize: bool = False,
        submission_policy: str = "manual_review",
    ) -> str:
        """Generate a session pack directory for MCP handoff.

        The pack contains:

        - ``agent-brief.md`` — human-readable brief with hard rules,
          trajectory coverage, and batch sequence.
        - ``mcp-plan.json`` — machine-readable plan with arms, budget,
          neutralization sweep, and MCP tool call order.

        Parameters
        ----------
        date : str
            Session date in ``YYYY-MM-DD`` format.
        materialize : bool
            If ``True``, create the directory and write files.  If ``False``,
            return the path without writing.
        submission_policy : str
            Submission policy (``"manual_review"`` or ``"auto_submit"``).

        Returns
        -------
        str
            Path to the session pack directory.
        """
        # Generate the plan
        plan = self.plan(date)

        pack_dir = os.path.join("tracking", "sessions", date)

        if not materialize:
            return pack_dir

        os.makedirs(pack_dir, exist_ok=True)

        # Write agent-brief.md
        brief_path = os.path.join(pack_dir, "agent-brief.md")
        with open(brief_path, "w", encoding="utf-8") as f:
            f.write(self._render_agent_brief(plan, submission_policy))

        # Write mcp-plan.json
        mcp_plan_path = os.path.join(pack_dir, "mcp-plan.json")
        mcp_plan = {
            "date": plan["date"],
            "region": plan["region"],
            "universe": plan["universe"],
            "delay": plan["delay"],
            "budget": plan["budget"],
            "neutralization_sweep": plan["neutralization_sweep"],
            "arms": plan["arms"],
            "submission_policy": submission_policy,
            "hard_rules": [
                "Enforce single-dataset purity unless strategy explicitly requires otherwise.",
                "Do not reuse an identical simulation payload without consulting the hash cache.",
                "Before create_multi_simulation, pass expressions through wqb.expression.validator.check_batch.",
                "Before check_correlation or set_alpha_properties, compute WebDataScope failed counts.",
                "REGULAR candidates require Failed RA == 0; PPA candidates require Failed PPA == 0.",
                "Run wqb operator-audit at session start to catch ghost operators.",
                "Update batch-log after every create_multi_simulation batch.",
                "For USA REGULAR mining, keep primary universe at TOP3000.",
                "Traverse the full region-supported neutralization order.",
            ],
            "tool_order": [
                "authenticate",
                "get_operators",
                "get_datafields",
                "create_multi_simulation",
                "get_simulation_result",
                "check_correlation",
                "get_alpha_details",
                "get_alpha_yearly_stats",
                "get_alpha_pnl",
                "performance_comparison",
                "set_alpha_properties",
                "submit_alpha",
            ],
            "generated_at": datetime.now(timezone.utc).isoformat(),
        }
        with open(mcp_plan_path, "w", encoding="utf-8") as f:
            json.dump(mcp_plan, f, indent=2, ensure_ascii=False)

        return pack_dir

    def _render_agent_brief(self, plan: dict, submission_policy: str) -> str:
        """Render the agent-brief.md content from a plan."""
        lines: List[str] = []
        lines.append(f"# WQB Session Brief — {plan['date']}")
        lines.append("")
        lines.append(f"**Region:** {plan['region']}")
        lines.append(f"**Universe:** {plan['universe']}")
        lines.append(f"**Delay:** {plan['delay']}")
        lines.append(f"**Budget:** {plan['budget']} simulations")
        lines.append(f"**Submission policy:** {submission_policy}")
        lines.append("")

        lines.append("## Neutralization Sweep")
        lines.append("")
        for i, neut in enumerate(plan["neutralization_sweep"], 1):
            lines.append(f"{i}. {neut}")
        lines.append("")

        lines.append("## Arms")
        lines.append("")
        lines.append("| # | Category | Dataset | Universe | Paradigms | Budget |")
        lines.append("|---|----------|---------|----------|-----------|--------|")
        for i, arm in enumerate(plan["arms"], 1):
            paradigms_str = ", ".join(arm["paradigms"][:3])
            if len(arm["paradigms"]) > 3:
                paradigms_str += f" (+{len(arm['paradigms']) - 3})"
            lines.append(
                f"| {i} | {arm['category']} | {arm['dataset']} | "
                f"{arm['universe']} | {paradigms_str} | {arm['budget_allocation']} |"
            )
        lines.append("")

        lines.append("## Hard Rules")
        lines.append("")
        rules = [
            "Enforce single-dataset purity unless the strategy explicitly requires otherwise.",
            "Do not reuse an identical simulation payload without consulting the hash cache.",
            "Before `create_multi_simulation`, pass expressions through `wqb.expression.validator.check_batch`.",
            "Before `check_correlation` or `set_alpha_properties`, compute WebDataScope failed counts.",
            "REGULAR candidates require `Failed RA == 0`; PPA candidates require `Failed PPA == 0`.",
            "Run `wqb operator-audit` at session start to catch ghost operators.",
            "Update `batch-log` after every `create_multi_simulation` batch.",
            "For USA REGULAR mining, keep primary universe at `TOP3000`.",
            "Traverse the full region-supported neutralization order.",
            "Record every meaningful step to the event log and trajectory ledger.",
        ]
        for rule in rules:
            lines.append(f"- {rule}")
        lines.append("")

        lines.append("## Batch Sequence")
        lines.append("")
        lines.append("1. Authenticate and fetch operators.")
        lines.append("2. Run operator audit; verify no ghost operators.")
        lines.append("3. For each arm: fetch datafields, generate 4-expression batch.")
        lines.append("4. Validate batch diversity via `check_batch`.")
        lines.append("5. Dispatch `create_multi_simulation`.")
        lines.append("6. Check simulation cache for duplicates before re-simulating.")
        lines.append("7. Record batch in `batch_log`.")
        lines.append("8. For passing candidates: compute WebDataScope failed counts.")
        lines.append("9. If failed count == 0: run `check_correlation`.")
        lines.append("10. Hand off to robustness audit before submission.")
        lines.append("")

        return "\n".join(lines)

    # ------------------------------------------------------------------
    # Session pack validation
    # ------------------------------------------------------------------

    def validate_session_pack(self, pack_dir: str) -> dict:
        """Validate a session pack directory.

        Checks that the pack contains the required files and that
        ``snapshot.results.json`` (if present) has the correct format.

        Parameters
        ----------
        pack_dir : str
            Path to the session pack directory.

        Returns
        -------
        dict
            ``{"ok": bool, "errors": list[str]}``
        """
        errors: List[str] = []

        # Check directory exists
        if not os.path.isdir(pack_dir):
            return {"ok": False, "errors": [f"Pack directory does not exist: {pack_dir}"]}

        # Check required files
        required_files = ["agent-brief.md", "mcp-plan.json"]
        for fname in required_files:
            fpath = os.path.join(pack_dir, fname)
            if not os.path.exists(fpath):
                errors.append(f"Missing required file: {fname}")

        # Validate mcp-plan.json format if it exists
        mcp_plan_path = os.path.join(pack_dir, "mcp-plan.json")
        if os.path.exists(mcp_plan_path):
            try:
                with open(mcp_plan_path, "r", encoding="utf-8") as f:
                    mcp_plan = json.load(f)
                required_keys = {"date", "region", "universe", "budget", "arms", "neutralization_sweep"}
                missing_keys = required_keys - set(mcp_plan.keys())
                if missing_keys:
                    errors.append(
                        f"mcp-plan.json missing keys: {sorted(missing_keys)}"
                    )
            except json.JSONDecodeError as e:
                errors.append(f"mcp-plan.json is not valid JSON: {e}")

        # Validate snapshot.results.json if it exists
        snapshot_path = os.path.join(pack_dir, "snapshot.results.json")
        if os.path.exists(snapshot_path):
            try:
                with open(snapshot_path, "r", encoding="utf-8") as f:
                    snapshot = json.load(f)

                # snapshot.results.json must be a dict with "results" key
                if not isinstance(snapshot, dict):
                    errors.append("snapshot.results.json must be a JSON object")
                elif "results" not in snapshot:
                    errors.append('snapshot.results.json missing "results" key')
                else:
                    results = snapshot["results"]
                    if not isinstance(results, list):
                        errors.append('"results" in snapshot.results.json must be a list')
                    else:
                        for i, item in enumerate(results):
                            if not isinstance(item, dict):
                                errors.append(
                                    f"results[{i}] must be a JSON object, got {type(item).__name__}"
                                )
                                continue
                            if "expression" not in item:
                                errors.append(f'results[{i}] missing "expression" key')
                            if "settings" not in item and "result" not in item:
                                errors.append(
                                    f'results[{i}] missing "settings" or "result" key'
                                )
            except json.JSONDecodeError as e:
                errors.append(f"snapshot.results.json is not valid JSON: {e}")
        else:
            # snapshot.results.json is expected to be filled before ingestion
            errors.append("Missing snapshot.results.json (fill before ingestion)")

        return {"ok": len(errors) == 0, "errors": errors}
