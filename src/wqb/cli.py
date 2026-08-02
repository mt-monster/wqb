"""CLI entry point for the WQB toolkit.

Uses ``argparse`` (zero external dependencies — no click required).

Subcommands
-----------
- ``plan``                 — Generate a search plan for a date.
- ``doctor``               — Check bookkeeping tables and system health.
- ``operator-audit``       — Diff library operators vs platform.
- ``research``             — Show research evidence and design signals.
- ``settings``             — Print the current search space configuration.
- ``validate-session-pack`` — Validate a handoff session pack.
- ``prepare-session-pack`` — Generate a session pack for MCP handoff.
- ``news-refresh-portfolio`` — Refresh the news dataset portfolio.

Usage::

    wqb plan --date 2026-04-22 --region USA --budget 300
    wqb doctor
    wqb operator-audit --live-operators rank,zscore,ts_mean
    wqb research --category news
    wqb settings
    wqb validate-session-pack tracking/sessions/2026-04-22
    wqb prepare-session-pack --date 2026-04-22 --materialize
    wqb news-refresh-portfolio

Also works as::

    python -m wqb plan --date 2026-04-22
"""

from __future__ import annotations

import argparse
import json
import os
import sys
from typing import List, Optional


# ---------------------------------------------------------------------------
# Subcommand handlers
# ---------------------------------------------------------------------------


def cmd_plan(args: argparse.Namespace) -> int:
    """Generate a search plan for the given date."""
    from .search.scheduler import Scheduler

    sched = Scheduler()
    plan = sched.plan(
        date=args.date,
        region=args.region,
        universe=args.universe,
        delay=args.delay,
        budget=args.budget,
    )

    print(f"# WQB Plan — {plan['date']}")
    print(f"Region: {plan['region']}  Universe: {plan['universe']}  "
          f"Delay: {plan['delay']}  Budget: {plan['budget']}")
    print()

    # Neutralization sweep
    print("## Neutralization Sweep")
    for i, neut in enumerate(plan["neutralization_sweep"], 1):
        print(f"  {i}. {neut}")
    print()

    # Arms
    print("## Arms")
    print(f"{'#':>3}  {'Category':<16} {'Dataset':<24} {'Universe':<12} "
          f"{'Paradigms':<20} {'Budget':>6}")
    print("-" * 90)
    for i, arm in enumerate(plan["arms"], 1):
        paradigms = ", ".join(arm["paradigms"][:3])
        if len(arm["paradigms"]) > 3:
            paradigms += f" (+{len(arm['paradigms']) - 3})"
        print(f"{i:>3}  {arm['category']:<16} {arm['dataset']:<24} "
              f"{arm['universe']:<12} {paradigms:<20} {arm['budget_allocation']:>6}")

    # Emit event
    try:
        from .memory.events import emit, EVENT_SCHEDULER_PLAN
        emit(
            EVENT_SCHEDULER_PLAN,
            date=plan["date"],
            region=plan["region"],
            universe=plan["universe"],
            budget=plan["budget"],
            arm_count=len(plan["arms"]),
            neutralization_count=len(plan["neutralization_sweep"]),
        )
    except Exception:
        pass  # event logging is best-effort

    return 0


def cmd_doctor(args: argparse.Namespace) -> int:
    """Check bookkeeping tables and system health."""
    from .memory.db import SimulationDB

    db = SimulationDB(args.db_path)
    db.init_tables()
    report = db.doctor()

    print("# WQB Doctor")
    print()

    if report["ok"]:
        print("Status: OK — all tables present")
    else:
        print(f"Status: FAIL — missing tables: {report['missing_tables']}")

    print()
    print("## Table Counts")
    print(f"{'Table':<20} {'Rows':>8}")
    print("-" * 30)
    for table, count in report["table_counts"].items():
        marker = " (MISSING)" if count < 0 else ""
        print(f"{table:<20} {count:>8}{marker}")

    db.close()

    # Also check data directories
    print()
    print("## Data Directories")
    dirs_to_check = [
        "data",
        "data/events",
        "data/operators_verified.json",
        "data/failure_memory.jsonl",
    ]
    for d in dirs_to_check:
        exists = os.path.exists(d)
        status = "OK" if exists else "MISSING"
        print(f"  {d}: {status}")

    return 0 if report["ok"] else 1


def cmd_operator_audit(args: argparse.Namespace) -> int:
    """Diff library operators against the live platform."""
    from .expression.operator_audit import operator_audit, get_verified_operators

    live_ops: Optional[List[str]] = None
    if args.live_operators:
        live_ops = [op.strip() for op in args.live_operators.split(",") if op.strip()]
    elif args.live_operators_file:
        with open(args.live_operators_file, "r", encoding="utf-8") as f:
            live_ops = [line.strip() for line in f if line.strip()]

    # If no live operators provided, fall back to the library's verified set
    # (offline mode — assumes all non-ghost library ops are present).
    if not live_ops:
        live_ops = sorted(get_verified_operators())

    report = operator_audit(live_operators=live_ops, output_path=args.output)

    summary = report.get("summary", {})
    print("# Operator Audit")
    print()
    print(f"Library operators:  {summary.get('total_library_declared', 0)}")
    print(f"Live operators:     {summary.get('total_live', 0)}")
    print(f"Verified operators: {summary.get('total_verified', 0)}")
    print()

    ghost_ops = report.get("ghost", [])
    if ghost_ops:
        print("## Ghost Operators (in library, NOT on platform)")
        for op in ghost_ops:
            print(f"  - {op}")
        print()
    else:
        print("No ghost operators detected.")
        print()

    missing_ops = report.get("missing", [])
    if missing_ops:
        print("## New Operators (on platform, not in library)")
        for op in missing_ops:
            print(f"  - {op}")
        print()

    print(f"Verified file written to: {args.output}")

    return 0 if not ghost_ops else 1


def cmd_research(args: argparse.Namespace) -> int:
    """Show research evidence and design signals."""
    from .config import REGIONS, get_categories, is_news_dataset

    print("# WQB Research")
    print()

    if args.category:
        print(f"## Category: {args.category}")
        print()

        # Check if it's a news/sentiment category
        if is_news_dataset("", args.category):
            print("This is a news/sentiment/socialmedia category.")
            print("Use the 6-bucket news framework (NewsLoop) for mining.")
            print()
            print("Buckets: LEVEL, CHANGE, SURPRISE, DISPERSION, EVENT_CONDITIONED, PROPAGATION")
            print("HIGH-priority: DISPERSION, EVENT_CONDITIONED, PROPAGATION")
        else:
            print("Use the standard 13-paradigm rotation for mining.")
            print()
            from .config import PARADIGMS
            print("Paradigms:")
            for p in PARADIGMS:
                print(f"  - {p}")
    else:
        print("## Available Categories by Region")
        print()
        for region, info in REGIONS.items():
            cats = info.get("categories", [])
            print(f"  {region}: {', '.join(cats)}")
        print()

        print("## Design Signals")
        print()
        signals = [
            "Prefer high-alphaCount fields (community-validated signal density prior).",
            "Route cold-start news mining to Tier A datasets (fieldCount >= 50, pyramidMultiplier >= 1.2).",
            "On saturated datasets (>=10K alphas), switch to hypothesis-first mining.",
            "Use WebDataScope data package for zero-cost pre-screening before simulation.",
            "Coverage < 0.4 fields require ts_backfill / group_backfill.",
            "Traverse the full region-supported neutralization order (never collapse).",
            "For USA REGULAR mining, keep primary universe at TOP3000.",
            "Run operator-audit at session start to catch ghost operators.",
            "Before create_multi_simulation, pass expressions through check_batch.",
            "Before check_correlation, compute WebDataScope failed counts.",
        ]
        for i, signal in enumerate(signals, 1):
            print(f"  {i}. {signal}")

    return 0


def cmd_settings(args: argparse.Namespace) -> int:
    """Print the current search space configuration."""
    from .config import (
        REGIONS,
        OP_FAMILIES,
        PARADIGMS,
        USA_DEFAULT_UNIVERSE,
        USA_NEUTRALIZATION_SWEEP,
        GHOST_OPERATORS,
        neutralization_search_order,
    )

    print("# WQB Settings")
    print()

    print("## Regions")
    print(f"{'Region':<8} {'Default Universe':<18} {'Delay':<6} {'#Neuts':<8} {'#Categories':<12}")
    print("-" * 60)
    for region, info in REGIONS.items():
        delays = info.get("delays", [1])
        default_d = delays[-1] if delays else 1
        print(f"{region:<8} {info.get('default_universe', 'N/A'):<18} "
              f"{default_d:<6} {len(info['neutralizations']):<8} "
              f"{len(info['categories']):<12}")
    print()

    print("## USA Neutralization Sweep (11 options)")
    for i, neut in enumerate(USA_NEUTRALIZATION_SWEEP, 1):
        print(f"  {i}. {neut}")
    print()

    print("## Operator Families")
    for family, ops in OP_FAMILIES.items():
        print(f"  {family} ({len(ops)} ops): {', '.join(ops[:5])}"
              + (f" +{len(ops) - 5} more" if len(ops) > 5 else ""))
    print()

    print("## Paradigms (P1-P13)")
    for p in PARADIGMS:
        print(f"  - {p}")
    print()

    print("## Ghost Operators (purged, NOT on platform)")
    for op in sorted(GHOST_OPERATORS):
        print(f"  - {op}")
    print()

    print(f"USA default universe: {USA_DEFAULT_UNIVERSE}")

    return 0


def cmd_validate_session_pack(args: argparse.Namespace) -> int:
    """Validate a handoff session pack."""
    from .search.scheduler import Scheduler

    sched = Scheduler()
    result = sched.validate_session_pack(args.dir)

    print("# Session Pack Validation")
    print(f"Directory: {args.dir}")
    print()

    if result["ok"]:
        print("Status: OK — pack is valid")
    else:
        print("Status: FAIL — errors found:")
        for err in result["errors"]:
            print(f"  - {err}")

    return 0 if result["ok"] else 1


def cmd_prepare_session_pack(args: argparse.Namespace) -> int:
    """Generate a session pack for MCP handoff."""
    from .search.scheduler import Scheduler

    sched = Scheduler()
    pack_dir = sched.prepare_session_pack(
        date=args.date,
        materialize=args.materialize,
        submission_policy=args.submission_policy,
    )

    print("# Session Pack Prepared")
    print(f"Directory: {pack_dir}")
    print(f"Materialized: {args.materialize}")
    print(f"Submission policy: {args.submission_policy}")

    if args.materialize:
        print()
        print("Files:")
        for fname in ["agent-brief.md", "mcp-plan.json"]:
            fpath = os.path.join(pack_dir, fname)
            exists = os.path.exists(fpath)
            print(f"  {fname}: {'created' if exists else 'NOT created'}")

    print()
    print("Next steps:")
    print("  1. Review agent-brief.md for hard rules and batch sequence.")
    print("  2. Execute MCP tools per mcp-plan.json.")
    print("  3. Fill snapshot.results.json with simulation results.")
    print("  4. Run: wqb validate-session-pack " + pack_dir)

    return 0


def cmd_news_refresh_portfolio(args: argparse.Namespace) -> int:
    """Refresh the news dataset portfolio."""
    from .config import REGIONS, is_news_dataset
    from .search.news_loop import NewsBucket, HIGH_PRIORITY_BUCKETS, MAX_ATTEMPTS

    print("# News Dataset Portfolio Refresh")
    print()

    # List known news/sentiment datasets
    news_datasets = [
        {"id": "news_transformer_scores", "tier": "A", "fieldCount": 80, "alphaCount": 500},
        {"id": "sentiment22", "tier": "A", "fieldCount": 60, "alphaCount": 200},
        {"id": "sentiment23", "tier": "A", "fieldCount": 55, "alphaCount": 150},
        {"id": "event_return_model", "tier": "A", "fieldCount": 50, "alphaCount": 100},
        {"id": "news94", "tier": "A", "fieldCount": 94, "alphaCount": 300},
        {"id": "news29", "tier": "A", "fieldCount": 70, "alphaCount": 250},
        {"id": "news73", "tier": "A", "fieldCount": 65, "alphaCount": 180},
        {"id": "news12", "tier": "B", "fieldCount": 45, "alphaCount": 120000},
        {"id": "news18", "tier": "B", "fieldCount": 40, "alphaCount": 40000},
        {"id": "socialmedia12", "tier": "B", "fieldCount": 35, "alphaCount": 43000},
    ]

    print("## Tier A (cold-start recommended)")
    print(f"{'Dataset':<28} {'Fields':>6} {'Alphas':>8} {'Ratio':>8}")
    print("-" * 55)
    for ds in news_datasets:
        if ds["tier"] != "A":
            continue
        ratio = ds["alphaCount"] / ds["fieldCount"] if ds["fieldCount"] else 0
        print(f"{ds['id']:<28} {ds['fieldCount']:>6} {ds['alphaCount']:>8} {ratio:>8.1f}")

    print()
    print("## Tier B (saturated — flag before mining)")
    print(f"{'Dataset':<28} {'Fields':>6} {'Alphas':>8} {'Ratio':>8}")
    print("-" * 55)
    for ds in news_datasets:
        if ds["tier"] != "B":
            continue
        ratio = ds["alphaCount"] / ds["fieldCount"] if ds["fieldCount"] else 0
        print(f"{ds['id']:<28} {ds['fieldCount']:>6} {ds['alphaCount']:>8} {ratio:>8.1f}")

    print()
    print("## 6-Bucket Framework")
    print(f"  Buckets: {', '.join(b.value for b in NewsBucket)}")
    print(f"  HIGH-priority: {', '.join(b.value for b in HIGH_PRIORITY_BUCKETS)}")
    print(f"  Max attempts: {MAX_ATTEMPTS}")
    print()
    print("Recommendation: Route cold-start to Tier A. Flag Tier B before mining.")
    print("On saturated datasets (>=10K alphas), switch to hypothesis-first mining.")

    return 0


# ---------------------------------------------------------------------------
# Argument parser construction
# ---------------------------------------------------------------------------


def build_parser() -> argparse.ArgumentParser:
    """Build the top-level argument parser.

    Returns
    -------
    argparse.ArgumentParser
        The configured parser with all subcommands.
    """
    parser = argparse.ArgumentParser(
        prog="wqb",
        description="WorldQuant BRAIN alpha mining toolkit.",
    )
    subparsers = parser.add_subparsers(
        dest="command",
        help="Available subcommands",
    )

    # --- plan ---
    p_plan = subparsers.add_parser(
        "plan",
        help="Generate a search plan for a date.",
        description="Allocate simulation budget across category/dataset/paradigm arms.",
    )
    p_plan.add_argument("--date", required=True, help="Planning date (YYYY-MM-DD).")
    p_plan.add_argument("--region", default="USA", help="Region code (default: USA).")
    p_plan.add_argument("--universe", default="TOP3000", help="Trading universe (default: TOP3000).")
    p_plan.add_argument("--delay", type=int, default=1, help="Data delay (default: 1).")
    p_plan.add_argument("--budget", type=int, default=300, help="Total simulation budget (default: 300).")
    p_plan.set_defaults(func=cmd_plan)

    # --- doctor ---
    p_doctor = subparsers.add_parser(
        "doctor",
        help="Check bookkeeping tables and system health.",
        description="Verify SQLite tables exist and report row counts.",
    )
    p_doctor.add_argument("--db-path", default="data/wqb.db", help="Database path (default: data/wqb.db).")
    p_doctor.set_defaults(func=cmd_doctor)

    # --- operator-audit ---
    p_audit = subparsers.add_parser(
        "operator-audit",
        help="Diff library operators vs platform.",
        description="Check for ghost operators not present on the BRAIN platform.",
    )
    op_source = p_audit.add_mutually_exclusive_group()
    op_source.add_argument(
        "--live-operators",
        help="Comma-separated list of live operator names from get_operators.",
    )
    op_source.add_argument(
        "--live-operators-file",
        help="File with one operator name per line from get_operators.",
    )
    p_audit.add_argument(
        "--output",
        default="data/operators_verified.json",
        help="Output file for verified operators (default: data/operators_verified.json).",
    )
    p_audit.set_defaults(func=cmd_operator_audit)

    # --- research ---
    p_research = subparsers.add_parser(
        "research",
        help="Show research evidence and design signals.",
        description="Display available categories, paradigms, and design signals.",
    )
    p_research.add_argument("--category", default=None, help="Filter to a specific category.")
    p_research.set_defaults(func=cmd_research)

    # --- settings ---
    p_settings = subparsers.add_parser(
        "settings",
        help="Print the current search space configuration.",
        description="Display regions, neutralizations, operators, paradigms, and ghost list.",
    )
    p_settings.set_defaults(func=cmd_settings)

    # --- validate-session-pack ---
    p_validate = subparsers.add_parser(
        "validate-session-pack",
        help="Validate a handoff session pack.",
        description="Check that a session pack directory has the required files and valid JSON.",
    )
    p_validate.add_argument("dir", help="Path to the session pack directory.")
    p_validate.set_defaults(func=cmd_validate_session_pack)

    # --- prepare-session-pack ---
    p_prepare = subparsers.add_parser(
        "prepare-session-pack",
        help="Generate a session pack for MCP handoff.",
        description="Create agent-brief.md and mcp-plan.json for MCP execution.",
    )
    p_prepare.add_argument("--date", required=True, help="Session date (YYYY-MM-DD).")
    p_prepare.add_argument("--materialize", action="store_true", help="Create files on disk.")
    p_prepare.add_argument(
        "--submission-policy",
        default="manual_review",
        choices=["manual_review", "auto_submit"],
        help="Submission policy (default: manual_review).",
    )
    p_prepare.set_defaults(func=cmd_prepare_session_pack)

    # --- news-refresh-portfolio ---
    p_news = subparsers.add_parser(
        "news-refresh-portfolio",
        help="Refresh the news dataset portfolio.",
        description="Display Tier A/B datasets and 6-bucket framework status.",
    )
    p_news.set_defaults(func=cmd_news_refresh_portfolio)

    return parser


# ---------------------------------------------------------------------------
# Main entry point
# ---------------------------------------------------------------------------


def main(argv: Optional[List[str]] = None) -> int:
    """Main CLI entry point.

    Parameters
    ----------
    argv : list[str] or None
        Command-line arguments.  If ``None``, uses ``sys.argv[1:]``.

    Returns
    -------
    int
        Exit code (0 for success, non-zero for failure).
    """
    parser = build_parser()
    args = parser.parse_args(argv)

    if not hasattr(args, "func"):
        parser.print_help()
        return 1

    try:
        return args.func(args)
    except KeyboardInterrupt:
        print("\nInterrupted.", file=sys.stderr)
        return 130
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    sys.exit(main())
