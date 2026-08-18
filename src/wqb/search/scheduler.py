"""wqb.search.scheduler — daily mining plan + session pack generation.

``Scheduler.plan`` builds the region arms and budget split; the session
pack (agent-brief.md + mcp-plan.json under tracking/sessions/<date>/)
hands the plan to the MCP-driven execution session.
"""

from __future__ import annotations

import json
import os
from datetime import datetime, timezone
from typing import Dict, List, Optional

from wqb.config import (
    PARADIGMS,
    REGIONS,
    default_delay,
    default_universe,
    neutralization_search_order,
)
from wqb.search import failure_memory

# Category → representative datasets for arm construction.
ARM_CATALOG: Dict[str, List[str]] = {
    "fundamental": ["fundamental6", "fundamental2"],
    "sentiment": ["sentiment22", "sentiment23"],
    "news": ["news12", "news29"],
    "analyst": ["analyst4", "analyst11", "analyst14"],
    "option": ["option3", "option6"],
    "short_interest": ["shortinterest6", "shortinterest7"],
    "model": ["model11", "model54"],
    "earnings": ["earnings3", "earnings5"],
    "event": ["event12"],
}

MIN_PER_ARM = 4

HARD_RULES: List[str] = [
    "Enforce single-dataset purity unless strategy explicitly requires otherwise.",
    "Do not reuse an identical simulation payload without consulting the hash cache.",
    "Before create_multi_simulation, pass expressions through wqb.expression.validator.check_batch.",
    "Before check_correlation or set_alpha_properties, compute WebDataScope failed counts.",
    "REGULAR candidates require Failed RA == 0; PPA candidates require Failed PPA == 0.",
    "Run wqb operator-audit at session start to catch ghost operators.",
    "Update batch-log after every create_multi_simulation batch.",
    "Traverse the full region-supported neutralization order.",
]

TOOL_ORDER: List[str] = [
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
]

_REQUIRED_PLAN_KEYS = [
    "date", "region", "universe", "budget", "arms",
    "neutralization_sweep", "hard_rules", "tool_order",
]
_REQUIRED_PACK_FILES = ["agent-brief.md", "mcp-plan.json",
                        "snapshot.results.json"]


class Scheduler:
    """Builds daily mining plans and session handoff packs."""

    def __init__(self, failure_memory_file: Optional[str] = None):
        self.failure_memory_file = (
            failure_memory_file or failure_memory.DEFAULT_MEMORY_FILE
        )
        self._last_plan: Optional[dict] = None

    # ------------------------------------------------------------------
    # Planning
    # ------------------------------------------------------------------

    def plan(self, date: str, region: str = "USA", budget: int = 100,
             universe: Optional[str] = None) -> Dict:
        """Build the mining plan for a date/region/budget."""
        region = region.upper()
        if region not in REGIONS:
            raise ValueError(f"Unknown region: {region}")
        universe = universe or default_universe(region)
        delay = default_delay(region)

        arms: List[Dict] = []
        for category in REGIONS[region]["categories"]:
            for dataset in ARM_CATALOG.get(category, []):
                if failure_memory.is_deprioritized(
                        category, dataset, universe, "",
                        memory_file=self.failure_memory_file):
                    continue
                arms.append({
                    "category": category,
                    "dataset": dataset,
                    "universe": universe,
                    "paradigms": list(PARADIGMS),
                })
        arms = self.allocate_budget(arms, budget)

        plan = {
            "date": date,
            "region": region,
            "universe": universe,
            "delay": delay,
            "budget": budget,
            "arms": arms,
            "neutralization_sweep": neutralization_search_order(region),
            "submission_policy": "manual_review",
            "hard_rules": list(HARD_RULES),
            "tool_order": list(TOOL_ORDER),
            "generated_at": datetime.now(timezone.utc).isoformat(),
        }
        self._last_plan = plan
        return plan

    def allocate_budget(self, arms: List[Dict], budget: int) -> List[Dict]:
        """Distribute budget across arms (min 4 per funded arm).

        Guarantees ``sum(budget_allocation) == budget`` for budget > 0;
        zero/negative budgets allocate zero everywhere.
        """
        for arm in arms:
            arm["budget_allocation"] = 0
        if budget <= 0 or not arms:
            return arms

        remaining = budget
        funded = 0
        for arm in arms:
            if remaining >= MIN_PER_ARM:
                arm["budget_allocation"] = MIN_PER_ARM
                remaining -= MIN_PER_ARM
                funded += 1
            else:
                break

        if remaining > 0:
            if funded == 0:
                arms[0]["budget_allocation"] += remaining
            else:
                base, extra = divmod(remaining, funded)
                for arm in arms:
                    if arm["budget_allocation"] <= 0:
                        continue
                    bonus = 1 if extra > 0 else 0
                    if bonus:
                        extra -= 1
                    arm["budget_allocation"] += base + bonus
        return arms

    # ------------------------------------------------------------------
    # Session pack
    # ------------------------------------------------------------------

    def prepare_session_pack(self, date: str,
                             materialize: bool = False) -> str:
        """Return (and optionally materialize) the session pack directory."""
        pack_dir = os.path.join("tracking", "sessions", date)
        if not materialize:
            return pack_dir

        plan = self._last_plan or self.plan(date)
        os.makedirs(pack_dir, exist_ok=True)
        brief_path = os.path.join(pack_dir, "agent-brief.md")
        with open(brief_path, "w", encoding="utf-8") as f:
            f.write(self._render_agent_brief(plan))
        mcp_path = os.path.join(pack_dir, "mcp-plan.json")
        with open(mcp_path, "w", encoding="utf-8") as f:
            json.dump(plan, f, indent=2, ensure_ascii=False)
        return pack_dir

    def _render_agent_brief(self, plan: Dict) -> str:
        lines = [
            f"# WQB Session Brief — {plan['date']}",
            "",
            f"**Region:** {plan['region']}",
            f"**Universe:** {plan['universe']}",
            f"**Delay:** {plan.get('delay')}",
            f"**Budget:** {plan['budget']} simulations",
            f"**Submission policy:** {plan.get('submission_policy', 'manual_review')}",
            "",
            "## Neutralization Sweep",
            "",
        ]
        for i, neut in enumerate(plan["neutralization_sweep"], 1):
            lines.append(f"{i}. {neut}")
        lines += ["", "## Arms", "",
                  "| # | Category | Dataset | Universe | Paradigms | Budget |",
                  "|---|----------|---------|----------|-----------|--------|"]
        for i, arm in enumerate(plan["arms"], 1):
            paradigms = ", ".join(arm["paradigms"][:3])
            extra = len(arm["paradigms"]) - 3
            if extra > 0:
                paradigms += f" (+{extra})"
            lines.append(
                f"| {i} | {arm['category']} | {arm['dataset']} | "
                f"{arm['universe']} | {paradigms} | "
                f"{arm['budget_allocation']} |")
        lines += ["", "## Hard Rules", ""]
        for rule in plan["hard_rules"]:
            lines.append(f"- {rule}")
        lines += ["", "## Batch Sequence", ""]
        steps = [
            "Authenticate and fetch operators.",
            "Run operator audit; verify no ghost operators.",
            "For each arm: fetch datafields, generate 4-expression batch.",
            "Validate batch diversity via check_batch.",
            "Dispatch create_multi_simulation.",
            "Check simulation cache for duplicates before re-simulating.",
            "Record batch in batch_log.",
            "For passing candidates: compute WebDataScope failed counts.",
            "If failed count == 0: run check_correlation.",
            "Hand off to robustness audit before submission.",
        ]
        for i, step in enumerate(steps, 1):
            lines.append(f"{i}. {step}")
        return "\n".join(lines) + "\n"

    # ------------------------------------------------------------------
    # Validation
    # ------------------------------------------------------------------

    def validate_session_pack(self, pack_dir: str) -> Dict:
        """Validate a materialized session pack directory."""
        errors: List[str] = []
        if not os.path.isdir(pack_dir):
            return {"ok": False,
                    "errors": [f"Directory not found: {pack_dir}"]}

        for name in _REQUIRED_PACK_FILES:
            if not os.path.exists(os.path.join(pack_dir, name)):
                errors.append(f"Missing required file: {name}")

        mcp_path = os.path.join(pack_dir, "mcp-plan.json")
        if os.path.exists(mcp_path):
            try:
                with open(mcp_path, "r", encoding="utf-8") as f:
                    plan = json.load(f)
            except json.JSONDecodeError:
                errors.append("mcp-plan.json is not valid JSON")
            else:
                missing = [k for k in _REQUIRED_PLAN_KEYS if k not in plan]
                if missing:
                    errors.append(f"mcp-plan.json missing keys: {missing}")

        snapshot_path = os.path.join(pack_dir, "snapshot.results.json")
        if os.path.exists(snapshot_path):
            try:
                with open(snapshot_path, "r", encoding="utf-8") as f:
                    snapshot = json.load(f)
            except json.JSONDecodeError:
                errors.append("snapshot.results.json is not valid JSON")
            else:
                if not isinstance(snapshot.get("results"), list):
                    errors.append(
                        "snapshot.results.json: results must be a list")

        return {"ok": not errors, "errors": errors}
